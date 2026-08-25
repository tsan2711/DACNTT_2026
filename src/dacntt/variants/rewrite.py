"""Rewrite a gold answer into one writing style. Add a function, then a spec row."""

from __future__ import annotations

import re
from fractions import Fraction

_BOXED = re.compile(r"^\\boxed\{(.*)\}$", re.DOTALL)
_DOLLAR = re.compile(r"^\$+(.*)\$+$", re.DOTALL)
_PLAIN_FRAC = re.compile(r"^(-?\d+)\s*/\s*(-?\d+)$")
_LATEX_FRAC = re.compile(r"^\\(?:d|t)?frac\{(-?[^}]+)\}\{(-?[^}]+)\}$")
_INT = re.compile(r"^-?\d+$")
_FLOAT = re.compile(r"^-?\d+\.\d+$")


def unwrap(text: str) -> str:
    """Strip outer ``$...$`` / ``\\boxed{}`` so conversion sees the core."""
    current = text.strip()
    changed = True
    while changed:
        changed = False
        boxed = _BOXED.match(current)
        if boxed:
            current = boxed.group(1).strip()
            changed = True
            continue
        dollar = _DOLLAR.match(current)
        if dollar:
            current = dollar.group(1).strip()
            changed = True
    return current


def rewrite_plain(gold: str) -> str:
    return gold


def rewrite_decimal(gold: str) -> str | None:
    fraction = _as_fraction(gold)
    if fraction is None or fraction.denominator == 1:
        return None
    return _format_decimal(fraction, trailing=False)


def rewrite_decimal_trailing(gold: str) -> str | None:
    fraction = _as_fraction(gold)
    if fraction is None or fraction.denominator == 1:
        return None
    return _format_decimal(fraction, trailing=True)


def rewrite_frac(gold: str) -> str | None:
    return _latex_frac(gold, "frac")


def rewrite_dfrac(gold: str) -> str | None:
    return _latex_frac(gold, "dfrac")


def rewrite_tfrac(gold: str) -> str | None:
    return _latex_frac(gold, "tfrac")


def rewrite_boxed(gold: str) -> str:
    return rf"\boxed{{{gold}}}"


def rewrite_dollar(gold: str) -> str:
    return f"${gold}$"


def rewrite_sentence(gold: str) -> str:
    return f"The answer is {gold}"


def rewrite_assignment(gold: str) -> str:
    return f"x = {gold}"


def rewrite_unit(gold: str) -> str:
    return f"{gold} apples"


def rewrite_int_float(gold: str) -> str | None:
    """``18`` → ``18.0`` and ``18.0`` → ``18``. GSM8K-oriented."""
    core = unwrap(gold)
    if _INT.fullmatch(core):
        return f"{core}.0"
    match = re.fullmatch(r"(-?\d+)\.0+", core)
    if match:
        return match.group(1)
    return None


def _as_fraction(gold: str) -> Fraction | None:
    core = unwrap(gold)
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


def _frac_parts(gold: str) -> tuple[str, str] | None:
    core = unwrap(gold)
    plain = _PLAIN_FRAC.fullmatch(core)
    if plain:
        return plain.group(1), plain.group(2)
    latex = _LATEX_FRAC.fullmatch(core)
    if latex:
        return latex.group(1), latex.group(2)
    if _INT.fullmatch(core):
        return core, "1"
    if _FLOAT.fullmatch(core):
        fraction = Fraction(core).limit_denominator()
        return str(fraction.numerator), str(fraction.denominator)
    return None


def _latex_frac(gold: str, command: str) -> str | None:
    parts = _frac_parts(gold)
    if parts is None:
        return None
    numerator, denominator = parts
    return rf"\{command}{{{numerator}}}{{{denominator}}}"


def _format_decimal(fraction: Fraction, *, trailing: bool) -> str:
    value = fraction.numerator / fraction.denominator
    if trailing:
        return f"{value:.2f}"
    if _terminates(fraction):
        return format(value, "g")
    return f"{value:.6f}".rstrip("0").rstrip(".")


def _terminates(fraction: Fraction) -> bool:
    denominator = fraction.denominator
    while denominator % 2 == 0:
        denominator //= 2
    while denominator % 5 == 0:
        denominator //= 5
    return denominator == 1
