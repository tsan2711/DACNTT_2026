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


def test_select_all_keeps_rejected_solutions_too() -> None:
    """Giai đoạn 4 ablation: verifier gate skipped, every generated solution
    becomes a training example — even ones the same adapter would reject."""
    adapter = _adapter({r"\boxed{10}": True})
    kept = select_batch("10", [r"\boxed{10}", "11", "nope"], adapter, select_all=True)
    assert kept == [r"\boxed{10}", "11", "nope"]


def test_train_on_gold_ignores_generations_entirely() -> None:
    """Giai đoạn 6 control: with --train-on-gold the training set is the
    dataset's reference solutions, one per train problem, regardless of what
    the model generated or what the verifier thought of it."""
    from dacntt.gold.load import GoldItem

    items = [
        GoldItem(
            dataset="toy",
            item_id=str(i),
            gold="10",
            problem=f"q{i}?",
            solution=f"reference working {i}. The final answer is $\\boxed{{10}}$.",
        )
        for i in range(3)
    ]
    # Every generation is wrong, so a normal GVT round would train on nothing.
    generator = ScriptedGenerate({f"q{i}?": ["99", "98"] for i in range(3)})
    adapter = _adapter({"99": False, "98": False})
    trainer = NoOpTrain()

    records = run_rounds(
        items,
        generator=generator,
        trainer=trainer,
        select_adapter=adapter,
        exam_adapters={"reward": adapter},
        rounds=1,
        k=2,
        train_on_gold=True,
    )

    assert records[0].n_selected == 3, "one example per problem, not per sample"
    assert [ex.solution for ex in trainer.examples] == [it.solution for it in items]
    assert all("99" not in ex.solution for ex in trainer.examples)


def test_train_on_gold_respects_the_holdout_split() -> None:
    """The control must not leak exam problems into training just because it
    stopped reading generations."""
    from dacntt.gold.load import GoldItem

    items = [
        GoldItem(
            dataset="toy", item_id=str(i), gold="10", problem=f"q{i}?", solution=f"sol{i}"
        )
        for i in range(4)
    ]
    generator = ScriptedGenerate({f"q{i}?": ["10", "11"] for i in range(4)})
    trainer = NoOpTrain()

    run_rounds(
        items,
        generator=generator,
        trainer=trainer,
        select_adapter=_adapter({"10": True, "11": False}),
        exam_adapters={"reward": _adapter({"10": True, "11": False})},
        rounds=1,
        k=2,
        train_item_ids=frozenset({"toy:0", "toy:1"}),
        test_item_ids=frozenset({"toy:2", "toy:3"}),
        train_on_gold=True,
    )

    assert [ex.solution for ex in trainer.examples] == ["sol0", "sol1"]


def test_gsm8k_reference_solution_is_reformatted_for_the_prompt() -> None:
    """Raw GSM8K solutions carry calculator spans and a `#### N` tail, neither
    of which the model is prompted to produce. Training on them verbatim would
    confound the control with a format shift."""
    from dacntt.gold.extract import normalise_gsm8k_solution

    raw = "She had 48 clips.\nShe sold <<48/2=24>>24 of them.\n#### 24"
    out = normalise_gsm8k_solution(raw, "24")

    assert "<<" not in out and ">>" not in out
    assert "####" not in out
    assert out.endswith("The final answer is $\\boxed{24}$.")
    assert "She had 48 clips." in out


def test_holdout_split_train_and_exam_never_overlap() -> None:
    """Giai đoạn 2: `select` only trains on train_item_ids, `exam` only scores
    test_item_ids — the fix for select+exam sharing the same test set."""
    items = [_item(str(i), f"q{i}?", "10") for i in range(4)]
    generator = ScriptedGenerate(
        {f"q{i}?": [r"\boxed{10}", "11"] for i in range(4)}
    )
    adapter = _adapter({r"\boxed{10}": True, "11": False})
    trainer = NoOpTrain()
    train_ids = frozenset({"toy:0", "toy:1"})
    test_ids = frozenset({"toy:2", "toy:3"})

    records = run_rounds(
        items,
        generator=generator,
        trainer=trainer,
        select_adapter=adapter,
        exam_adapters={"reward": adapter},
        rounds=1,
        k=2,
        train=True,
        train_item_ids=train_ids,
        test_item_ids=test_ids,
    )

    # exam only scored the 2 held-out items, not all 4
    assert len(records[0].flags["reward"]) == 2
    # every trained example's problem came from the train split ("q0?"/"q1?"),
    # never from the held-out exam split ("q2?"/"q3?")
    trained_problems = {ex.problem for ex in trainer.examples}
    assert trained_problems == {"q0?", "q1?"}


def test_gold_loads_problem_text() -> None:
    from pathlib import Path

    cache = Path("data/gold")
    items = load_gold("gsm8k", 1, cache, fetch=False)
    assert items[0].gold == "18"
    assert "ducks" in items[0].problem.lower()


def _item(item_id: str, problem: str, gold: str):
    from dacntt.gold.load import GoldItem

    return GoldItem(dataset="toy", item_id=item_id, gold=gold, problem=problem)
