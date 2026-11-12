"""Reviewer-driven pipeline fixes (2026-11): gold shorthand, SFT row format, MATH-train pool."""

import json

import pytest

from dacntt.gold.extract import normalise_math_gold
from dacntt.gold.load import load_gold
from dacntt.gvt.train import TrainExample, _sft_row, _write_sft_jsonl
from dacntt.verify.adapter import MathVerifyAdapter


@pytest.mark.parametrize(
    "raw,fixed",
    [
        ("\\frac43", "\\frac{4}{3}"),
        ("\\frac 59", "\\frac{5}{9}"),
        ("\\frac9{19}", "\\frac{9}{19}"),
        ("\\frac{270}7\\text{ degrees}", "\\frac{270}{7}"),
        ("11\\sqrt2", "11\\sqrt{2}"),
        ("\\frac{1}{2}", "\\frac{1}{2}"),
        ("12", "12"),
        ("x^2+1", "x^2+1"),
    ],
)
def test_normalise_math_gold(raw, fixed):
    assert normalise_math_gold(raw) == fixed


def test_fixed_gold_verifies_against_itself_boxed():
    v = MathVerifyAdapter("reward", normalize_gold_boxed=True)
    for raw in ["\\frac43", "11\\sqrt2", "\\frac 59", "\\frac{270}7\\text{ degrees}"]:
        g = normalise_math_gold(raw)
        assert v.verify(g, "\\boxed{" + g + "}").accepted, raw


def test_sft_row_formats():
    ex = TrainExample(problem="1+1?", solution="2 \\boxed{2}")
    old = _sft_row(ex, False)
    new = _sft_row(ex, True)
    assert list(old) == ["messages"] and len(old["messages"]) == 2
    assert list(new) == ["prompt", "completion"]
    assert new["prompt"][0]["role"] == "user"
    assert new["completion"][0] == {"role": "assistant", "content": "2 \\boxed{2}"}


def test_write_sft_jsonl_completion_only(tmp_path):
    _write_sft_jsonl(tmp_path, [TrainExample("p", "s")], completion_only=True)
    row = json.loads((tmp_path / "train.jsonl").read_text().splitlines()[0])
    assert "prompt" in row and "completion" in row


def test_load_gold_fix_flag(tmp_path):
    rows = [{"problem": "p", "solution": "s", "answer": "\\frac43", "unique_id": "a/1"}]
    (tmp_path / "math500_test.jsonl").write_text("\n".join(json.dumps(r) for r in rows))
    assert load_gold("math500", 1, tmp_path, fetch=False)[0].gold == "\\frac43"
    assert load_gold("math500", 1, tmp_path, fetch=False, fix_gold=True)[0].gold == "\\frac{4}{3}"


def test_mathtrain_source_registered():
    from dacntt.gold.sources import DATASETS, MATHTRAIN, SOURCES

    assert MATHTRAIN in SOURCES and MATHTRAIN not in DATASETS


def test_max_train_examples_caps_dose():
    from dacntt.gold.load import GoldItem
    from dacntt.gvt.generate import ScriptedGenerate
    from dacntt.gvt.loop import run_rounds

    items = [GoldItem("gsm8k", str(i), "1", problem="p") for i in range(12)]

    class Spy:
        def __init__(self):
            self.sizes = []
            self.examples = []

        def train(self, examples, *, round=None):
            self.sizes.append(len(examples))

    spy = Spy()
    adapter = MathVerifyAdapter("reward")
    run_rounds(
        items,
        generator=ScriptedGenerate.from_gold(items, 2),
        trainer=spy,
        select_adapter=adapter,
        exam_adapters={"reward": adapter},
        rounds=2,
        k=2,
        max_train_examples=5,
    )
    assert spy.sizes and all(n <= 5 for n in spy.sizes)


def test_injected_boxed_bias_is_selective_and_deterministic():
    golds = [str(i) for i in range(400)]
    clean = MathVerifyAdapter("reward")
    biased = MathVerifyAdapter("reward", inject_boxed_bias=0.3)
    rej = [g for g in golds if not biased.verify(g, f"so \\boxed{{{g}}}").accepted]
    ok = [g for g in golds if clean.verify(g, f"so \\boxed{{{g}}}").accepted]
    assert len(ok) == 400
    assert 0.2 < len(rej) / 400 < 0.4
    # deterministic, and only boxed answers are affected
    assert rej == [g for g in golds if not biased.verify(g, f"so \\boxed{{{g}}}").accepted]
    assert all(biased.verify(g, f"the answer is {g}").accepted == clean.verify(g, f"the answer is {g}").accepted for g in rej[:20])


def test_content_bias_rejects_boxed_fraction_golds_only():
    biased = MathVerifyAdapter("reward", inject_bias_content=True)
    assert not biased.verify("\\frac{1}{2}", "so \\boxed{\\frac{1}{2}}").accepted
    assert biased.verify("\\frac{1}{2}", "the answer is 1/2").accepted
    assert biased.verify("7", "so \\boxed{7}").accepted
