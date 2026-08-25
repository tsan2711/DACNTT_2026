"""Human-read helpers: extract the circled answer and compare to gold."""

from dacntt.read import extract_final, human_equal, normalize_math


def test_extract_prefers_last_boxed() -> None:
    text = r"3 x 4 = 12, then 12 - 2 = 10. \boxed{10}"
    assert extract_final(text) == "10"


def test_extract_answer_cue() -> None:
    assert extract_final("Natalia sold 48 + 24.\nThe answer is 72") == "72"


def test_human_equal_dfrac_and_half() -> None:
    assert human_equal(r"\frac{1}{2}", r"\dfrac{1}{2}")
    assert human_equal("1/2", "0.50")
    assert not human_equal("1/3", "0.33")


def test_human_equal_left_right_and_text() -> None:
    gold = r"\left( 3, \frac{\pi}{2} \right)"
    pred = r"(3, \frac{\pi}{2})"
    assert human_equal(gold, pred)
    assert human_equal(r"\text{Evelyn}", "Evelyn")
    assert normalize_math("p - q") == normalize_math("p-q")
