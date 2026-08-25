"""pass@1, pass@k, writing-style counts, A/B/C. 'Correct' = verifier accepted."""

from __future__ import annotations

import re
from collections.abc import Sequence

from dacntt.read import extract_final

# Same ids as việc 1 variants, counted on model text (not gold rewrites).
STYLE_IDS = (
    "boxed",
    "dfrac",
    "tfrac",
    "frac",
    "dollar",
    "sentence",
    "assignment",
    "unit",
    "decimal",
    "decimal_trailing",
    "int_float",
)

_FRAC_PLAIN = re.compile(r"(?<![dt])\\frac")
_INT_FLOAT = re.compile(r"-?\d+\.0+\b")
_TRAILING = re.compile(r"-?\d+\.\d*0\b")
_DECIMAL = re.compile(r"-?\d+\.\d+")


def pass_at(flags: Sequence[Sequence[bool]], k: int) -> float:
    if not flags:
        return 0.0
    if k <= 1:
        return sum(1 for row in flags if row and row[0]) / len(flags)
    return sum(1 for row in flags if any(row[:k])) / len(flags)


def abc_shift(
    prev: Sequence[Sequence[bool]],
    now: Sequence[Sequence[bool]],
) -> dict[str, int]:
    """A = newly pass@k; B = already pass@k, pass@1 newly true; C = lost pass@k."""
    added = stabler = lost = 0
    for old_row, new_row in zip(prev, now):
        old_k = any(old_row)
        new_k = any(new_row)
        old_1 = bool(old_row and old_row[0])
        new_1 = bool(new_row and new_row[0])
        if not old_k and new_k:
            added += 1
        elif old_k and new_k and (not old_1) and new_1:
            stabler += 1
        elif old_k and not new_k:
            lost += 1
    return {"A": added, "B": stabler, "C": lost}


def count_styles(texts: Sequence[str]) -> dict[str, int]:
    counts = {name: 0 for name in STYLE_IDS}
    counts["n"] = len(texts)
    for text in texts:
        for name, on in style_flags(text).items():
            if on:
                counts[name] += 1
    return counts


def style_flags(text: str) -> dict[str, bool]:
    extracted = extract_final(text) or text
    int_float = bool(_INT_FLOAT.search(extracted) or _INT_FLOAT.search(text))
    trailing = (not int_float) and bool(
        _TRAILING.search(extracted) or _TRAILING.search(text)
    )
    decimal = (not int_float) and (not trailing) and bool(
        _DECIMAL.search(extracted) or _DECIMAL.search(text)
    )
    dfrac = r"\dfrac" in text
    tfrac = r"\tfrac" in text
    return {
        "boxed": r"\boxed" in text,
        "dfrac": dfrac,
        "tfrac": tfrac,
        "frac": bool(_FRAC_PLAIN.search(text)) and not dfrac and not tfrac,
        "dollar": "$" in text,
        "sentence": bool(re.search(r"the\s+answer\s+is", text, re.I)),
        "assignment": bool(re.search(r"\bx\s*=", text, re.I)),
        "unit": bool(re.search(r"\bapples\b", text, re.I)),
        "decimal": decimal,
        "decimal_trailing": trailing,
        "int_float": int_float,
    }
