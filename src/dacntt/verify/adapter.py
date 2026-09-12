"""math-verify wrapper. Gold is always the first ``verify`` argument — the API is not symmetric."""

from __future__ import annotations

import re
from collections.abc import Callable, Sequence
from dataclasses import dataclass
from typing import Any

from dacntt.verify.presets import PRESETS, extraction_config

# Việc 1: \dfrac / \tfrac are rejected 100% of the time on MATH-500 even
# though the value is correct (parse_empty — math-verify doesn't recognise
# the command). Used for the Giai đoạn 1 control run: same dataset, same
# model, only the verifier changes (\dfrac/\tfrac -> \frac before parsing).
_DFRAC_TFRAC = re.compile(r"\\[dt]frac(?=\{|\s)")

# Giai đoạn 7: math-verify only runs its rich LaTeX extraction (sqrt, complex
# numbers, tuples/lists, polynomials, matrices, ...) inside a recognised
# delimiter (\boxed{...} or $...$); undelimited bare text falls back to a
# naive "grab the first plain number" heuristic that silently drops the rest
# of the expression. Dataset gold is stored bare (no delimiter), so whenever
# a real model writes a correct compound answer inside \boxed{...} — which is
# what every GVT prompt asks for — gold gets the naive truncated parse while
# the prediction gets the rich one, and the two compare unequal even though
# they're the same value (measured 2026-09-12: 17/200 MATH-500 gold answers,
# 8.5%, e.g. "3\sqrt{13}" parses to just "3" unless boxed). The fix mirrors
# gold onto the same delimited path the prediction is already on, so both
# sides get the same extraction. Only triggers when the prediction actually
# contains \boxed{...} and gold doesn't already, so it leaves every other
# writing-style variant (plain/sentence/assignment/unit/...) untouched — see
# tests/test_verify_adapter.py for the full-survey regression check.
_HAS_BOXED = re.compile(r"\\boxed\{")
_WHOLE_BOXED = re.compile(r"^\\boxed\{.*\}$", re.DOTALL)

ParseFn = Callable[..., Sequence[Any]]
VerifyFn = Callable[..., bool]

REASON_OK = "ok"
REASON_PARSE_EMPTY = "parse_empty"
REASON_TIMEOUT = "timeout"
REASON_COMPARE_FALSE = "compare_false"


@dataclass(frozen=True)
class VerifyResult:
    accepted: bool
    reason_guess: str
    gold_parsed_empty: bool
    pred_parsed_empty: bool


class MathVerifyAdapter:
    """Parse gold, parse the writing variant, then ``verify(gold, variant)``."""

    def __init__(
        self,
        preset: str,
        *,
        parse_fn: ParseFn | None = None,
        verify_fn: VerifyFn | None = None,
        timeout_seconds: int = 5,
        normalize_frac_commands: bool = False,
        normalize_gold_boxed: bool = False,
    ) -> None:
        if preset not in PRESETS:
            raise ValueError(f"unknown preset {preset!r}; expected one of {PRESETS}")
        self.preset = preset
        self.timeout_seconds = timeout_seconds
        self.normalize_frac_commands = normalize_frac_commands
        self.normalize_gold_boxed = normalize_gold_boxed
        self._parse = parse_fn
        self._verify = verify_fn
        self._pred_config = None if parse_fn is not None else extraction_config(preset)

    def verify(self, gold: str, prediction: str) -> VerifyResult:
        if self.normalize_frac_commands:
            gold = _DFRAC_TFRAC.sub(r"\\frac", gold)
            prediction = _DFRAC_TFRAC.sub(r"\\frac", prediction)
        if self.normalize_gold_boxed:
            if _HAS_BOXED.search(prediction) and not _WHOLE_BOXED.match(gold.strip()):
                gold = f"\\boxed{{{gold}}}"
        parse_fn, verify_fn = self._resolve_fns()
        gold_parsed, gold_timeout, gold_empty = self._parse_one(parse_fn, gold, for_gold=True)
        if gold_timeout:
            return VerifyResult(False, REASON_TIMEOUT, gold_empty, False)
        pred_parsed, pred_timeout, pred_empty = self._parse_one(
            parse_fn, prediction, for_gold=False
        )
        if pred_timeout:
            return VerifyResult(False, REASON_TIMEOUT, gold_empty, pred_empty)
        if gold_empty or pred_empty:
            return VerifyResult(False, REASON_PARSE_EMPTY, gold_empty, pred_empty)
        try:
            accepted = bool(verify_fn(gold_parsed, pred_parsed, timeout_seconds=self.timeout_seconds))
        except TypeError:
            accepted = bool(verify_fn(gold_parsed, pred_parsed))
        except Exception as exc:
            if _is_timeout(exc):
                return VerifyResult(False, REASON_TIMEOUT, False, False)
            return VerifyResult(False, REASON_COMPARE_FALSE, False, False)
        if accepted:
            return VerifyResult(True, REASON_OK, False, False)
        return VerifyResult(False, REASON_COMPARE_FALSE, False, False)

    def _resolve_fns(self) -> tuple[ParseFn, VerifyFn]:
        if self._parse is not None and self._verify is not None:
            return self._parse, self._verify
        from math_verify import parse, verify

        return self._parse or parse, self._verify or verify

    def _parse_one(
        self,
        parse_fn: ParseFn,
        text: str,
        *,
        for_gold: bool,
    ) -> tuple[Sequence[Any], bool, bool]:
        kwargs: dict[str, Any] = {"parsing_timeout": self.timeout_seconds}
        if not for_gold and self._pred_config is not None:
            kwargs["extraction_config"] = self._pred_config
        try:
            parsed = parse_fn(text, **kwargs)
        except TypeError:
            try:
                parsed = parse_fn(text)
            except Exception as exc:
                return [], _is_timeout(exc), True
        except Exception as exc:
            return [], _is_timeout(exc), True
        empty = parsed is None or len(parsed) == 0
        return parsed or [], False, empty


def _is_timeout(exc: BaseException) -> bool:
    if isinstance(exc, TimeoutError):
        return True
    return "timeout" in type(exc).__name__.lower()
