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
