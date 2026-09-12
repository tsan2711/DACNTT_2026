"""Wrapper contract: gold first, True/False recorded, timeout does not kill the run."""

from dacntt.verify.adapter import MathVerifyAdapter


def test_gold_is_first_verify_argument() -> None:
    seen: list[tuple[object, object]] = []

    def fake_parse(text: str, **_kwargs: object) -> list[str]:
        return [text]

    def fake_verify(gold: object, pred: object, **_kwargs: object) -> bool:
        seen.append((gold, pred))
        return True

    adapter = MathVerifyAdapter("default", parse_fn=fake_parse, verify_fn=fake_verify)
    result = adapter.verify("BOOK", "STYLE")

    assert result.accepted is True
    assert seen == [(["BOOK"], ["STYLE"])]


def test_records_true_and_false() -> None:
    def fake_parse(text: str, **_kwargs: object) -> list[str]:
        return [text]

    accepted = MathVerifyAdapter(
        "default",
        parse_fn=fake_parse,
        verify_fn=lambda gold, pred, **_k: True,
    ).verify("1/2", "1/2")
    rejected = MathVerifyAdapter(
        "default",
        parse_fn=fake_parse,
        verify_fn=lambda gold, pred, **_k: False,
    ).verify("1/2", "0.5")

    assert accepted.accepted is True
    assert accepted.reason_guess == "ok"
    assert rejected.accepted is False
    assert rejected.reason_guess == "compare_false"


def test_timeout_does_not_kill_run() -> None:
    def boom(_text: str, **_kwargs: object) -> list[str]:
        raise TimeoutError("parse timeout")

    result = MathVerifyAdapter(
        "default",
        parse_fn=boom,
        verify_fn=lambda *_a, **_k: True,
    ).verify("1/2", "0.5")

    assert result.accepted is False
    assert result.reason_guess == "timeout"


def test_normalize_frac_commands_flips_dfrac_tfrac_to_frac() -> None:
    """Giai đoạn 1 control (papers/KE-HOACH-MO-RONG.md): the one variable
    that changes vs. the original verifier. Real math-verify, not a fake —
    this is the exact fix that must turn Việc 1's 100%-rejected \\dfrac case
    into an accept."""
    plain = MathVerifyAdapter("reward")
    patched = MathVerifyAdapter("reward", normalize_frac_commands=True)
    gold, pred = "1/2", r"\dfrac{1}{2}"

    assert plain.verify(gold, pred).accepted is False
    assert plain.verify(gold, pred).reason_guess == "parse_empty"

    result = patched.verify(gold, pred)
    assert result.accepted is True
    assert result.reason_guess == "ok"


def test_normalize_gold_boxed_fixes_compound_gold_vs_boxed_prediction() -> None:
    """Giai đoạn 7 control (papers/KET-QUA-CO-LAP-AC.md): math-verify only runs
    its rich LaTeX extraction inside a delimiter (\\boxed{...} or $...$); bare
    gold falls back to a naive "first plain number" parse that drops the rest
    of a compound expression. Real math-verify, not a fake — these are exact
    MATH-500 gold values measured compare_false 2026-09-12 (17/200, the
    boxed-specific share of the 41/200 in results/viec1/table.csv, the rest
    being the pre-existing unrelated unreadable-gold formats VIEC-SAU.md
    already names)."""
    plain = MathVerifyAdapter("reward")
    patched = MathVerifyAdapter("reward", normalize_gold_boxed=True)
    cases = ["3\\sqrt{13}", "6+9i", "1,-2", "1 \\pm \\sqrt{19}", "10,\\!080"]

    for gold in cases:
        pred = f"\\boxed{{{gold}}}"
        before = plain.verify(gold, pred)
        assert before.accepted is False, gold
        assert before.reason_guess == "compare_false", gold

        after = patched.verify(gold, pred)
        assert after.accepted is True, gold
        assert after.reason_guess == "ok", gold


def test_normalize_gold_boxed_finds_boxed_inside_longer_solution() -> None:
    """The real GVT case: \\boxed{...} sits at the end of a reasoning trace,
    not as the whole prediction string."""
    patched = MathVerifyAdapter("reward", normalize_gold_boxed=True)
    gold = "3\\sqrt{13}"
    pred = "Working through the steps, the length is 3 times sqrt(13), so \\boxed{3\\sqrt{13}}."

    result = patched.verify(gold, pred)

    assert result.accepted is True
    assert result.reason_guess == "ok"


def test_normalize_gold_boxed_leaves_unboxed_predictions_untouched() -> None:
    """Must not fire when the prediction never boxes its answer — otherwise it
    would just move the same truncation bug from gold-only to both sides (see
    papers/KET-QUA-CO-LAP-AC.md for the regression this avoids: a naive
    unconditional gold-boxed-wrap broke the plain/sentence/assignment/unit
    writing-style variants)."""
    plain = MathVerifyAdapter("reward")
    patched = MathVerifyAdapter("reward", normalize_gold_boxed=True)
    gold, pred = "3\\sqrt{13}", "3\\sqrt{13}"

    assert plain.verify(gold, pred).accepted == patched.verify(gold, pred).accepted


def test_empty_parse_is_parse_empty() -> None:
    result = MathVerifyAdapter(
        "default",
        parse_fn=lambda _text, **_k: [],
        verify_fn=lambda *_a, **_k: True,
    ).verify("1/2", "0.5")

    assert result.accepted is False
    assert result.reason_guess == "parse_empty"
    assert result.gold_parsed_empty is True
