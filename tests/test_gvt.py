"""GVT loop: select, pass@*, writing-style counts, A/B/C. No grader-outcome claims."""

from dacntt.gold.load import load_gold
from dacntt.gvt.generate import ScriptedGenerate
from dacntt.gvt.loop import RoundRecord, run_rounds
from dacntt.gvt.measure import abc_shift, count_styles, pass_at
from dacntt.gvt.select import KeepIfAccepted, select_batch
from dacntt.gvt.train import NoOpTrain, TrainExample
from dacntt.verify.adapter import MathVerifyAdapter


def _adapter(accepted_map: dict[str, bool]) -> MathVerifyAdapter:
    def fake_parse(text: str, **_kwargs: object) -> list[str]:
        return [text]

    def fake_verify(_gold: object, pred: object, **_kwargs: object) -> bool:
        key = pred[0] if isinstance(pred, list) else str(pred)
        return accepted_map.get(key, False)

    return MathVerifyAdapter("reward", parse_fn=fake_parse, verify_fn=fake_verify)


def test_select_keeps_only_verifier_accepted() -> None:
    adapter = _adapter({r"\boxed{10}": True, "11": False, "The answer is 10": True})
    kept = select_batch("10", [r"\boxed{10}", "11", "The answer is 10"], adapter)
    assert kept == [r"\boxed{10}", "The answer is 10"]
    assert KeepIfAccepted().select("11", False) is None
    assert KeepIfAccepted().select(r"\boxed{10}", True) == r"\boxed{10}"


def test_style_counts_match_viec1_taxonomy() -> None:
    texts = [
        r"steps \boxed{1/2}",
        r"\dfrac{1}{2}",
        r"\frac{1}{2}",
        r"\tfrac{1}{3}",
        "The answer is 0.5",
        "0.50",
        "x = 10",
        "10 apples",
        "$18$",
        "18.0",
    ]
    counts = count_styles(texts)
    assert counts["n"] == 10
    assert counts["boxed"] == 1
    assert counts["dfrac"] == 1
    assert counts["tfrac"] == 1
    assert counts["frac"] == 1
    assert counts["sentence"] == 1
    assert counts["decimal"] == 1
    assert counts["decimal_trailing"] == 1
    assert counts["assignment"] == 1
    assert counts["unit"] == 1
    assert counts["dollar"] == 1
    assert counts["int_float"] == 1


def test_pass_at_one_and_k() -> None:
    flags = [
        [True, False, False, False],
        [False, False, False, True],
        [False, False, False, False],
    ]
    assert pass_at(flags, 1) == 1 / 3
    assert pass_at(flags, 4) == 2 / 3


def test_abc_shift_added_stabler_lost() -> None:
    prev = [
        [False, False, False, False],
        [False, True, False, False],
        [True, False, False, False],
    ]
    now = [
        [False, False, True, False],
        [True, True, False, False],
        [False, False, False, False],
    ]
    shift = abc_shift(prev, now)
    assert shift == {"A": 1, "B": 1, "C": 1}


def test_dry_rounds_select_then_measure() -> None:
    items = [
        _item("a", "10 apples?", "10"),
        _item("b", "half?", "1/2"),
    ]
    generator = ScriptedGenerate(
        {
            "10 apples?": [r"\boxed{10}", "11", r"\boxed{10}", "11"],
            "half?": [r"\dfrac{1}{2}", "0.5", r"\frac{1}{2}", "nope"],
        }
    )
    adapter = _adapter(
        {
            r"\boxed{10}": True,
            "11": False,
            r"\dfrac{1}{2}": False,
            "0.5": True,
            r"\frac{1}{2}": True,
            "nope": False,
        }
    )
    trainer = NoOpTrain()
    records = run_rounds(
        items,
        generator=generator,
        trainer=trainer,
        select_adapter=adapter,
        exam_adapters={"reward": adapter},
        rounds=2,
        k=4,
        train=True,
    )
    assert len(records) == 2
    first = records[0]
    assert isinstance(first, RoundRecord)
    assert first.round == 0
    assert first.pass_at[1]["reward"] == 0.5
    assert first.pass_at[4]["reward"] == 1.0
    assert first.n_selected == 4
    assert trainer.examples
    assert all(isinstance(ex, TrainExample) for ex in trainer.examples)


def test_gold_loads_problem_text() -> None:
    from pathlib import Path

    cache = Path("data/gold")
    items = load_gold("gsm8k", 1, cache, fetch=False)
    assert items[0].gold == "18"
    assert "ducks" in items[0].problem.lower()


def _item(item_id: str, problem: str, gold: str):
    from dacntt.gold.load import GoldItem

    return GoldItem(dataset="toy", item_id=item_id, gold=gold, problem=problem)
