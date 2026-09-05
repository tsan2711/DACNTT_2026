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


def test_empty_parse_is_parse_empty() -> None:
    result = MathVerifyAdapter(
        "default",
        parse_fn=lambda _text, **_k: [],
        verify_fn=lambda *_a, **_k: True,
    ).verify("1/2", "0.5")

    assert result.accepted is False
    assert result.reason_guess == "parse_empty"
    assert result.gold_parsed_empty is True
