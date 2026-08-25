"""Download slim model traces. Stream JSONL; do not clone training repos."""

from __future__ import annotations

import json
import sys
import urllib.request
from dataclasses import dataclass
from pathlib import Path

from dacntt.gold.extract import extract_gsm8k_gold

_USER_AGENT = "dacntt-viec2/0.1 (research; model traces subset)"

GSM8K_TRACE_URL = (
    "https://huggingface.co/datasets/jerryjsjsj/gsm8k-qwen3.5-teacher-traces/"
    "resolve/main/data/accepted.jsonl"
)
GSM8K_TRAIN_GOLD_URL = (
    "https://raw.githubusercontent.com/openai/grade-school-math/"
    "master/grade_school_math/data/train.jsonl"
)
MATH_TRACE_URL = (
    "https://huggingface.co/datasets/YYYYYYibo/VSR-MATH500-Qwen2.5-7B-Rollouts/"
    "resolve/main/math500_qwen25_7b_sources_8k.jsonl"
)

GSM8K_MODEL = "qwen3.5-397b-a17b"
MATH_MODEL = "Qwen/Qwen2.5-7B-Instruct"


@dataclass(frozen=True)
class TraceItem:
    dataset: str
    item_id: str
    gold: str
    solution: str
    model: str
    source_url: str


def load_gsm8k_traces(n: int, cache_dir: Path, gold_dir: Path) -> list[TraceItem]:
    slim_path = cache_dir / "gsm8k_qwen35_accepted.jsonl"
    _stream_jsonl(GSM8K_TRACE_URL, slim_path, n, keep=lambda _row: True, slim=_slim_gsm8k)
    gold_by_index = _gsm8k_train_gold(gold_dir)
    items: list[TraceItem] = []
    for row in _read_jsonl(slim_path)[:n]:
        gold = gold_by_index.get(int(row["source_index"]))
        if not gold:
            continue
        reasoning = str(row.get("teacher_reasoning") or "").strip()
        answer = str(row.get("teacher_answer") or row.get("generated_answer") or "").strip()
        solution = f"{reasoning}\nThe answer is {answer}".strip() if answer else reasoning
        items.append(
            TraceItem(
                dataset="gsm8k",
                item_id=str(row.get("id") or row["source_index"]),
                gold=gold,
                solution=solution,
                model=str(row.get("teacher_model") or GSM8K_MODEL),
                source_url=GSM8K_TRACE_URL,
            )
        )
    return items[:n]


def load_math500_traces(n: int, cache_dir: Path) -> list[TraceItem]:
    slim_path = cache_dir / "math500_qwen25_7b_sample0.jsonl"
    _stream_jsonl(
        MATH_TRACE_URL,
        slim_path,
        n,
        keep=lambda row: int(row.get("sample_index", -1)) == 0,
        slim=_slim_math,
    )
    items: list[TraceItem] = []
    for row in _read_jsonl(slim_path)[:n]:
        items.append(
            TraceItem(
                dataset="math500",
                item_id=str(row.get("problem_id") or row.get("dataset_index")),
                gold=str(row["gold"]),
                solution=str(row["solution"]),
                model=str(row.get("model") or MATH_MODEL),
                source_url=MATH_TRACE_URL,
            )
        )
    return items[:n]


def _slim_gsm8k(row: dict) -> dict:
    return {
        "id": row.get("id"),
        "source_index": row.get("source_index"),
        "teacher_model": row.get("teacher_model"),
        "teacher_reasoning": row.get("teacher_reasoning"),
        "teacher_answer": row.get("teacher_answer"),
        "generated_answer": row.get("generated_answer"),
    }


def _slim_math(row: dict) -> dict:
    return {
        "problem_id": row.get("problem_id"),
        "dataset_index": row.get("dataset_index"),
        "gold": row.get("reference_answer_raw"),
        "solution": row.get("response_text"),
        "extracted_answer_raw": row.get("extracted_answer_raw"),
        "is_correct_string_match": row.get("is_correct_string_match"),
        "model": row.get("model"),
        "sample_index": row.get("sample_index"),
    }


def _gsm8k_train_gold(gold_dir: Path) -> dict[int, str]:
    path = gold_dir / "gsm8k_train.jsonl"
    _download_if_missing(GSM8K_TRAIN_GOLD_URL, path)
    golds: dict[int, str] = {}
    for index, row in enumerate(_read_jsonl(path)):
        golds[index] = extract_gsm8k_gold(row["answer"])
    return golds


def _stream_jsonl(
    url: str,
    dest: Path,
    n: int,
    *,
    keep,
    slim,
) -> Path:
    dest.parent.mkdir(parents=True, exist_ok=True)
    if dest.is_file() and dest.stat().st_size > 0:
        existing = sum(1 for _ in dest.open(encoding="utf-8"))
        if existing >= n:
            return dest
    request = urllib.request.Request(url, headers={"User-Agent": _USER_AGENT})
    kept = 0
    with urllib.request.urlopen(request, timeout=120) as response, dest.open(
        "w", encoding="utf-8"
    ) as handle:
        for raw in response:
            row = json.loads(raw)
            if not keep(row):
                continue
            handle.write(json.dumps(slim(row), ensure_ascii=False) + "\n")
            kept += 1
            if kept % 20 == 0 or kept >= n:
                print(f"streamed {kept}/{n} from {url.rsplit('/', 1)[-1]}", file=sys.stderr)
            if kept >= n:
                break
    if kept < n:
        raise RuntimeError(f"only streamed {kept} traces from {url}, wanted {n}")
    return dest


def _download_if_missing(url: str, dest: Path) -> Path:
    dest.parent.mkdir(parents=True, exist_ok=True)
    if dest.is_file() and dest.stat().st_size > 0:
        return dest
    request = urllib.request.Request(url, headers={"User-Agent": _USER_AGENT})
    with urllib.request.urlopen(request, timeout=120) as response:
        dest.write_bytes(response.read())
    return dest


def _read_jsonl(path: Path) -> list[dict]:
    rows: list[dict] = []
    with path.open(encoding="utf-8") as handle:
        for line in handle:
            line = line.strip()
            if line:
                rows.append(json.loads(line))
    return rows
