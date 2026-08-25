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
