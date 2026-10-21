"""state: RoundRecord survives a JSON round trip (int pass@ keys, nested flags)."""

from dacntt.gvt.loop import RoundRecord
from dacntt.gvt.state import load_records, save_records


def test_round_trip(tmp_path):
    record = RoundRecord(
        round=1,
        pass_at={1: {"reward": 0.25}, 4: {"reward": 0.5}},
        styles={"boxed": 3},
        n_selected=7,
        abc={"A": 1, "B": 2, "C": 0},
        flags={"reward": [[True, False], [False, False]]},
        generations=[["x", "y"], ["z", "w"]],
        n_examples_trained=7,
    )
    path = tmp_path / "state.json"
    save_records(path, [record], rounds_total=3)
    assert load_records(path) == [record]
    assert not list(tmp_path.glob("*.tmp"))
