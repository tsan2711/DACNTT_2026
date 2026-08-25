"""Fetch and load gold answers into ``data/gold/``."""

from __future__ import annotations

import json
import urllib.request
from dataclasses import dataclass
from pathlib import Path

from dacntt.gold.extract import extract_gsm8k_gold, extract_math500_gold
from dacntt.gold.sources import DATASETS, GSM8K, MATH500, SOURCES, GoldSource

_USER_AGENT = "dacntt-viec1/0.1 (research; gold answers only)"


@dataclass(frozen=True)
class GoldItem:
    dataset: str
    item_id: str
    gold: str
    problem: str = ""


def load_gold(
    dataset: str,
    n: int,
    cache_dir: Path,
    *,
    fetch: bool = True,
) -> list[GoldItem]:
    """Return the first ``n`` gold answers for ``dataset`` (``gsm8k`` or ``math500``)."""
    if dataset not in SOURCES:
        raise ValueError(f"unknown dataset {dataset!r}; expected one of {DATASETS}")
    if n < 1:
        raise ValueError(f"n must be >= 1, got {n}")
    source = SOURCES[dataset]
    path = cache_dir / source.filename
    if fetch:
        ensure_cached(source, path)
    elif not path.is_file():
        raise FileNotFoundError(f"gold cache missing: {path}")
    return _parse_jsonl(dataset, path)[:n]


def ensure_cached(source: GoldSource, dest: Path) -> Path:
    dest.parent.mkdir(parents=True, exist_ok=True)
    if dest.is_file() and dest.stat().st_size > 0:
        return dest
    request = urllib.request.Request(
        source.url,
        headers={"User-Agent": _USER_AGENT},
    )
    with urllib.request.urlopen(request, timeout=60) as response:
        dest.write_bytes(response.read())
    return dest


def _parse_jsonl(dataset: str, path: Path) -> list[GoldItem]:
    items: list[GoldItem] = []
    with path.open(encoding="utf-8") as handle:
        for index, line in enumerate(handle):
            line = line.strip()
            if not line:
                continue
            row = json.loads(line)
            items.append(_row_to_item(dataset, index, row))
    return items


def _row_to_item(dataset: str, index: int, row: dict) -> GoldItem:
    if dataset == GSM8K:
        return GoldItem(
            dataset=dataset,
            item_id=str(index),
            gold=extract_gsm8k_gold(row["answer"]),
            problem=str(row.get("question", "")),
        )
    if dataset == MATH500:
        return GoldItem(
            dataset=dataset,
            item_id=str(row.get("unique_id", index)),
            gold=extract_math500_gold(row["answer"]),
            problem=str(row.get("problem", "")),
        )
    raise ValueError(f"unknown dataset {dataset!r}")
