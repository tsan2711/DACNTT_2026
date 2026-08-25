"""Select: keep solutions math-verify accepts. Does not rewrite the verifier."""

from __future__ import annotations

from collections.abc import Sequence
from typing import Protocol, runtime_checkable

from dacntt.verify.adapter import MathVerifyAdapter


@runtime_checkable
class Select(Protocol):
    """Giữ bài máy chấm chịu, bỏ bài bị gạch."""

    def select(self, solution: str, accepted: bool) -> str | None:
        """Return ``solution`` if accepted, otherwise ``None``."""
        ...


class KeepIfAccepted:
    def select(self, solution: str, accepted: bool) -> str | None:
        return solution if accepted else None


def select_batch(
    gold: str,
    solutions: Sequence[str],
    adapter: MathVerifyAdapter,
) -> list[str]:
    """Verify each solution against gold; keep the ones the teacher accepts."""
    gate = KeepIfAccepted()
    kept: list[str] = []
    for solution in solutions:
        accepted = adapter.verify(gold, solution).accepted
        selected = gate.select(solution, accepted)
        if selected is not None:
            kept.append(selected)
    return kept
