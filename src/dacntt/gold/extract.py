"""Pull the book answer out of a raw dataset row."""

from __future__ import annotations

import re

_GSM8K_TAIL = re.compile(r"####\s*(.+)\s*$")


def extract_gsm8k_gold(answer: str) -> str:
    """GSM8K stores reasoning plus ``#### <number>``."""
    match = _GSM8K_TAIL.search(answer.strip())
    if match is None:
        return answer.strip()
    tail = match.group(1).strip()
    if re.fullmatch(r"-?[\d,]+(?:\.\d+)?", tail):
        return tail.replace(",", "")
    return tail


def extract_math500_gold(answer: str) -> str:
    return answer.strip()


# MATH golds sometimes use TeX shorthand (``\frac43``, ``\frac 59``,
# ``11\sqrt2``) that math-verify parses to a truncated value even inside
# ``\boxed{}``. Measured 2026-11-09: with the gold wrapped in ``\boxed{}``
# only 8/500 MATH-500 golds fail to verify against themselves, all of this
# kind (plus ``\text{ degrees}``). Rewriting them to braced form fixes that
# without changing the value.
_FRAC_SHORT = re.compile(r"\\([dt]?frac)\s*(\d)\s*(\d)(?!\d)")
_FRAC_HALF1 = re.compile(r"\\([dt]?frac)\s*(\d)\s*\{")
_FRAC_HALF2 = re.compile(r"\\([dt]?frac)\s*\{([^{}]*)\}\s*(\d)(?!\d)")
_SQRT_SHORT = re.compile(r"\\sqrt\s*(\d)(?!\d)")
_TEXT_UNIT = re.compile(r"\s*\\text\{\s*[A-Za-z ]+\}\s*$")


def normalise_math_gold(gold: str) -> str:
    """Rewrite TeX shorthand in a MATH gold to braced form (value unchanged)."""
    out = gold.strip()
    out = _FRAC_SHORT.sub(r"\\\1{\2}{\3}", out)
    out = _FRAC_HALF1.sub(r"\\\1{\2}{", out)
    out = _FRAC_HALF2.sub(r"\\\1{\2}{\3}", out)
    out = _SQRT_SHORT.sub(r"\\sqrt{\1}", out)
    stripped = _TEXT_UNIT.sub("", out)
    return stripped if stripped else out


_GSM8K_CALC = re.compile(r"<<[^>]*>>")


def normalise_gsm8k_solution(answer: str, gold: str) -> str:
    """GSM8K's worked solution, rewritten to end the way we prompt for.

    The raw field carries calculator annotations (``<<48/2=24>>``) that never
    appear in model output, and terminates with ``#### 18`` rather than a
    boxed answer. Training on it verbatim would teach a format the verifier
    then has to parse differently from everything else the model writes, so
    the control would confound "gold vs self-generated" with "format shift".
    """
    body = _GSM8K_CALC.sub("", answer.strip())
    body = _GSM8K_TAIL.sub("", body).strip()
    return f"{body}\nThe final answer is $\\boxed{{{gold}}}$."


def normalise_math500_solution(solution: str, gold: str) -> str:
    """MATH-500 solutions are already LaTeX and usually already boxed."""
    body = solution.strip()
    if "\\boxed" in body:
        return body
    return f"{body}\nThe final answer is $\\boxed{{{gold}}}$."
