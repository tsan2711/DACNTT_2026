"""Variant registry: gold ``1/2`` must produce the mục 6 strings. No grader outcomes."""

from dacntt.variants.registry import apply_all
from dacntt.variants.rewrite import rewrite_int_float


def test_half_yields_ten_muc6_strings() -> None:
    by_id = {spec.id: text for spec, text in apply_all("1/2")}
    ten = {
        "plain": "1/2",
        "decimal": "0.5",
        "frac": r"\frac{1}{2}",
        "dfrac": r"\dfrac{1}{2}",
        "tfrac": r"\tfrac{1}{2}",
        "boxed": r"\boxed{1/2}",
        "dollar": "$1/2$",
        "sentence": "The answer is 1/2",
        "assignment": "x = 1/2",
        "unit": "1/2 apples",
    }
    assert len(ten) == 10
    assert {key: by_id[key] for key in ten} == ten
    assert "int_float" not in by_id


def test_decimal_trailing_zero_is_separate_form() -> None:
    by_id = {spec.id: text for spec, text in apply_all("1/2")}
    assert by_id["decimal_trailing"] == "0.50"


def test_int_float_swaps_18_and_18_dot_0() -> None:
    assert rewrite_int_float("18") == "18.0"
    assert rewrite_int_float("18.0") == "18"
    assert rewrite_int_float("1/2") is None


def test_int_float_applies_on_gsm8k() -> None:
    by_id = {spec.id: text for spec, text in apply_all("18", dataset="gsm8k")}
    assert by_id["int_float"] == "18.0"
    assert by_id["plain"] == "18"
    assert "decimal" not in by_id
