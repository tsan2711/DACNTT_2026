"""math-verify wrapper. Gold is always the first ``verify`` argument — the API is not symmetric."""

from __future__ import annotations

from collections.abc import Callable, Sequence
from dataclasses import dataclass
from typing import Any

from dacntt.verify.presets import PRESETS, extraction_config

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
    ) -> None:
        if preset not in PRESETS:
            raise ValueError(f"unknown preset {preset!r}; expected one of {PRESETS}")
        self.preset = preset
        self.timeout_seconds = timeout_seconds
        self._parse = parse_fn
        self._verify = verify_fn
        self._pred_config = None if parse_fn is not None else extraction_config(preset)

    def verify(self, gold: str, prediction: str) -> VerifyResult:
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
