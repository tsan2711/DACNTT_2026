"""load_with_timeout kills a hung load even when it holds the GIL.

The watchdog terminates the whole process, so the hang cases run in a
subprocess.
"""

import subprocess
import sys
import textwrap
import time

import pytest

from dacntt.gvt._load_timeout import load_with_timeout


def _run(body: str) -> tuple[subprocess.CompletedProcess, float]:
    code = textwrap.dedent(
        """
        import ctypes, sys, time
        sys.path.insert(0, "src")
        from dacntt.gvt._load_timeout import load_with_timeout
        """
    ) + textwrap.dedent(body)
    t0 = time.time()
    proc = subprocess.run([sys.executable, "-c", code], capture_output=True, text=True, timeout=60)
    return proc, time.time() - t0


def test_returns_result_when_fast():
    assert load_with_timeout(lambda: 42, what="fast call") == 42


def test_propagates_exception_from_load_fn():
    def boom():
        raise ValueError("bad checkpoint")

    with pytest.raises(ValueError, match="bad checkpoint"):
        load_with_timeout(boom, what="boom call")


@pytest.mark.parametrize(
    "hang",
    [
        "time.sleep(30)",
        "ctypes.PyDLL(None).sleep(30)",  # native call that keeps the GIL
    ],
)
def test_hung_load_exits_fast_with_traceback(hang):
    proc, elapsed = _run(f'load_with_timeout(lambda: {hang}, what="fake hang", timeout_s=1)')
    assert proc.returncode != 0
    assert elapsed < 15
    assert "Timeout" in proc.stderr
