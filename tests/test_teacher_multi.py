from dacntt.gold.load import GoldItem
from dacntt.gvt.loop import _select_examples


def test_train_on_gold_uses_extra_teacher_solutions():
    item = GoldItem("math500", "1", "2", problem="p", solution="s0", extra_solutions=("s1", "s2"))
    empty = GoldItem("math500", "2", "3", problem="q")
    ex = _select_examples([item, empty], [[], []], adapter=None, train_on_gold=True)
    assert [e.solution for e in ex] == ["s0", "s1", "s2"]
