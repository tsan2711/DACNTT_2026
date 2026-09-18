"""Watchdog for from_pretrained() calls that can hang indefinitely.

Kaggle T4 sessions have shown intermittent stalls mid weight-load (tqdm
"Loading weights: X%|... Materializing param=...") that never crash or
progress — confirmed hanging a full 12h Kaggle session with zero further
output (see experiments/viec3/KAGGLE.md, Run A 2026-09-18). A stuck call
can't be recovered in-process (the OS-level read/allocation it's blocked
on doesn't respond to a Python-level timeout), so this fails the whole
process fast instead — a fresh Kaggle session can then be retried in
minutes instead of losing a full 12h session for nothing.

Runs the call on a daemon thread rather than a ThreadPoolExecutor: a pool's
context manager calls shutdown(wait=True) on exit, which blocks until the
stuck worker finishes — i.e. never, for a genuine hang. A daemon thread
doesn't hold the process open, so main() can actually exit after this
raises instead of hanging a second time waiting for the same stuck call.

train.py reloads the base model fresh every round (see its module
docstring), so this guards every round of a run, not just the first.
"""

from __future__ import annotations

import threading
from typing import Callable, TypeVar

T = TypeVar("T")

DEFAULT_TIMEOUT_S = 180


def load_with_timeout(load_fn: Callable[[], T], *, what: str, timeout_s: float = DEFAULT_TIMEOUT_S) -> T:
    outcome: dict[str, object] = {}

    def _run() -> None:
        try:
            outcome["value"] = load_fn()
        except BaseException as exc:  # re-raised on the caller's thread below
            outcome["error"] = exc

    thread = threading.Thread(target=_run, daemon=True)
    thread.start()
    thread.join(timeout_s)

    if thread.is_alive():
        raise RuntimeError(
            f"{what} didn't return within {timeout_s}s — known intermittent Kaggle "
            "GPU/disk stall during weight loading (see experiments/viec3/KAGGLE.md). "
            "Not recoverable in-process; exit and retry in a fresh Kaggle session."
        )
    if "error" in outcome:
        raise outcome["error"]  # type: ignore[misc]
    return outcome["value"]  # type: ignore[return-value]
