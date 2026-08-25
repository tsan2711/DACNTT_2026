"""Read a final answer out of a writeup and compare it to gold (thay 'đọc tay')."""

from __future__ import annotations

import re
from fractions import Fraction

_ANSWER_CUE = re.compile(
    r"(?:the\s+answer\s+is|final\s+answer(?:\s+is)?|####)\s*[:.]?\s*(.+)$",
    re.IGNORECASE | re.MULTILINE,
)
_PLAIN_FRAC = re.compile(r"^(-?\d+)\s*/\s*(-?\d+)$")
_LATEX_FRAC = re.compile(r"^\\(?:d|t)?frac\{(-?[^}]+)\}\{(-?[^}]+)\}$")
_INT = re.compile(r"^-?\d+$")
_FLOAT = re.compile(r"^-?\d+\.\d+$")


def extract_final(text: str) -> str | None:
    """Prefer the last ``\\boxed{}``, then an answer cue, then a trailing number."""
    boxed = _last_boxed(text)
    if boxed is not None:
        return boxed
    for match in _ANSWER_CUE.finditer(text):
        candidate = match.group(1).strip().rstrip(".")
        if candidate:
            return candidate
    return _trailing_number(text)


def human_equal(gold: str, prediction: str | None) -> bool:
    """Same value to a person: strip latex wrappers, compare fractions / text."""
    if prediction is None:
        return False
    left = normalize_math(gold)
    right = normalize_math(prediction)
    if not left or not right:
        return False
    if left == right:
        return True
    left_frac = _as_fraction(left)
    right_frac = _as_fraction(right)
    if left_frac is not None and right_frac is not None:
        return left_frac == right_frac
    return False


def normalize_math(text: str) -> str:
    current = text.strip()
    current = _strip_wrappers(current)
    current = current.replace(r"\dfrac", r"\frac").replace(r"\tfrac", r"\frac")
    current = re.sub(r"\\(?:left|right)\s*", "", current)
    current = re.sub(r"\\(?:mathrm|text|mathbf|operatorname)\{([^{}]*)\}", r"\1", current)
    current = current.replace("$", "")
    current = current.replace(r"\,", "").replace(r"\;", "").replace(r"\:", "")
    current = current.replace(" ", "").replace("{", "").replace("}", "")
    current = current.replace(",", "")
    return current


def _last_boxed(text: str) -> str | None:
    key = r"\boxed"
    start_at = text.rfind(key)
    if start_at < 0:
        return None
    index = start_at + len(key)
    while index < len(text) and text[index].isspace():
        index += 1
    if index >= len(text) or text[index] != "{":
        return None
    depth = 0
    inner_start = index + 1
    for cursor in range(index, len(text)):
        char = text[cursor]
        if char == "{":
            depth += 1
        elif char == "}":
            depth -= 1
            if depth == 0:
                return text[inner_start:cursor].strip()
    return None


def _strip_wrappers(text: str) -> str:
    current = text.strip()
    changed = True
    while changed:
        changed = False
        if current.startswith(r"\boxed{") and current.endswith("}"):
            current = current[len(r"\boxed{") : -1].strip()
            changed = True
            continue
        if current.startswith("$") and current.endswith("$") and len(current) > 2:
            current = current.strip("$").strip()
            changed = True
    return current


def _as_fraction(text: str) -> Fraction | None:
    core = _strip_wrappers(text)
    core = core.replace(r"\dfrac", r"\frac").replace(r"\tfrac", r"\frac")
    plain = _PLAIN_FRAC.fullmatch(core)
    if plain:
        return Fraction(int(plain.group(1)), int(plain.group(2)))
    latex = _LATEX_FRAC.fullmatch(core)
    if latex and _INT.fullmatch(latex.group(1)) and _INT.fullmatch(latex.group(2)):
        return Fraction(int(latex.group(1)), int(latex.group(2)))
    if _INT.fullmatch(core):
        return Fraction(int(core), 1)
    if _FLOAT.fullmatch(core):
        return Fraction(core)
    return None


def _trailing_number(text: str) -> str | None:
    matches = re.findall(r"-?\d+(?:/\d+|\.\d+)?", text)
    return matches[-1] if matches else None
