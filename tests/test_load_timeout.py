"""load_with_timeout: fails fast instead of hanging (see KAGGLE.md Run A 2026-09-18)."""

import time

import pytest

from dacntt.gvt._load_timeout import load_with_timeout


def test_returns_result_when_fast():
    assert load_with_timeout(lambda: 42, what="fast call") == 42


def test_raises_runtime_error_on_timeout():
    def slow():
        time.sleep(5)
        return 1

    with pytest.raises(RuntimeError, match="didn't return within"):
        load_with_timeout(slow, what="slow call", timeout_s=0.05)


def test_propagates_exception_from_load_fn():
    def boom():
        raise ValueError("bad checkpoint")

    with pytest.raises(ValueError, match="bad checkpoint"):
        load_with_timeout(boom, what="boom call")
