"""Persist finished rounds so a killed run can resume at the next round."""

from __future__ import annotations

import json
from dataclasses import asdict
from pathlib import Path
from typing import Sequence

from dacntt.gvt.loop import RoundRecord


def save_records(path: Path, records: Sequence[RoundRecord], *, rounds_total: int) -> None:
    payload = {"rounds_total": rounds_total, "records": [asdict(r) for r in records]}
    tmp = path.with_suffix(path.suffix + ".tmp")
    tmp.write_text(json.dumps(payload, ensure_ascii=False), encoding="utf-8")
    tmp.replace(path)


def load_records(path: Path) -> list[RoundRecord]:
    payload = json.loads(path.read_text(encoding="utf-8"))
    return [
        RoundRecord(
            round=row["round"],
            pass_at={int(k): v for k, v in row["pass_at"].items()},
            styles=row["styles"],
            n_selected=row["n_selected"],
            abc=row["abc"],
            flags=row["flags"],
            generations=row["generations"],
            n_examples_trained=row["n_examples_trained"],
        )
        for row in payload["records"]
    ]
