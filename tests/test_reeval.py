"""reeval.summarize: accuracy splits into finished vs degenerate generations."""

import sys

sys.path.insert(0, "experiments/viec3")
from reeval import is_degenerate, summarize  # noqa: E402


def test_is_degenerate_needs_long_and_no_box():
    assert is_degenerate("x" * 1600)
    assert not is_degenerate("x" * 1600 + "\\boxed{3}")
    assert not is_degenerate("short")


def test_summarize_splits_accuracy():
    golds = ["1", "2"]
    texts = [["\\boxed{1}", "x" * 1600], ["\\boxed{3}", "\\boxed{2}"]]
    out = summarize(golds, texts, lambda g, t: f"\\boxed{{{g}}}" in t)
    assert out["pass_at_1"] == 0.5
    assert out["pass_at_k"] == 1.0
    assert out["sample_acc"] == 0.5
    assert out["degenerate_share"] == 0.25
    assert out["acc_finished"] == 2 / 3
