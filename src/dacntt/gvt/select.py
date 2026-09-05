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
    *,
    select_all: bool = False,
) -> list[str]:
    """Verify each solution against gold; keep the ones the teacher accepts.

    ``select_all=True`` is the Giai đoạn 4 ablation: skip the verifier gate
    entirely and keep every generated solution, to test whether the shrinking
    training pool alone (independent of verifier bias) is enough to cause the
    same decline — see papers/KE-HOACH-MO-RONG.md.
    """
    if select_all:
        return list(solutions)
    gate = KeepIfAccepted()
    kept: list[str] = []
    for solution in solutions:
        accepted = adapter.verify(gold, solution).accepted
        selected = gate.select(solution, accepted)
        if selected is not None:
            kept.append(selected)
    return kept
