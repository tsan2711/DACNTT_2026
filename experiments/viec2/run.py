"""Việc 2: real model writeups × math-verify, then read gold vs extracted answer.

python -m experiments.viec2.run --n 200 --presets reward,default
"""

from __future__ import annotations

import argparse
import csv
import json
import sys
from collections import Counter
from dataclasses import dataclass
from pathlib import Path

_REPO_ROOT = Path(__file__).resolve().parents[2]
_SRC = _REPO_ROOT / "src"
if str(_SRC) not in sys.path:
    sys.path.insert(0, str(_SRC))

from dacntt.read import extract_final, human_equal
from dacntt.report.manifest import write_manifest
from dacntt.verify.adapter import MathVerifyAdapter
from dacntt.verify.presets import PRESETS
from .traces import (
    GSM8K_MODEL,
    GSM8K_TRACE_URL,
    MATH_MODEL,
    MATH_TRACE_URL,
    TraceItem,
    load_gsm8k_traces,
    load_math500_traces,
)

FN_EXTRACT = "extract_wrong"
FN_WRITE = "write_unrecognized"
FN_AMBIGUOUS = "ambiguous"


@dataclass(frozen=True)
class ScoredItem:
    dataset: str
    item_id: str
    preset: str
    gold: str
    extracted: str | None
    actually_correct: bool
    gold_parsed_empty: bool
    accepted: bool
    verify_reason: str
    fn_kind: str | None
    boxed_only_reason: str | None


@dataclass(frozen=True)
class SummaryRow:
    dataset: str
    preset: str
    n: int
    n_gold_unparsed: int
    n_actually_correct: int
    n_fn: int
    n_extract_wrong: int
    n_write_unrecognized: int
    n_ambiguous: int


def main(argv: list[str] | None = None) -> int:
    args = _parse_args(argv)
    presets = _presets(args.presets)
    cache_dir: Path = args.cache
    gold_dir: Path = args.gold
    out_dir: Path = args.out

    traces: list[TraceItem] = []
    if args.dataset in ("gsm8k", "both"):
        traces.extend(load_gsm8k_traces(args.n, cache_dir, gold_dir))
        print(f"loaded {sum(1 for t in traces if t.dataset == 'gsm8k')} gsm8k traces", file=sys.stderr)
    if args.dataset in ("math500", "both"):
        traces.extend(load_math500_traces(args.n, cache_dir))
        print(f"loaded {sum(1 for t in traces if t.dataset == 'math500')} math500 traces", file=sys.stderr)

    adapters = {preset: MathVerifyAdapter(preset) for preset in presets}
    scored: list[ScoredItem] = []
    for preset in presets:
        adapter = adapters[preset]
        for item in traces:
            scored.append(_score(item, adapter))
            if len(scored) % 50 == 0:
                print(f"scored {len(scored)}", file=sys.stderr)

    rows = _summarize(scored)
    write_reports(rows, scored, out_dir)
    write_manifest(out_dir / "manifest.json", _manifest(args, presets, traces, scored))
    print(f"wrote {out_dir / 'table.md'}", file=sys.stderr)
    return 0


def _score(item: TraceItem, adapter: MathVerifyAdapter) -> ScoredItem:
    extracted = extract_final(item.solution)
    actually_correct = human_equal(item.gold, extracted)
    result = adapter.verify(item.gold, item.solution)
    fn_kind = None
    boxed_reason = None
    if actually_correct and not result.accepted and not result.gold_parsed_empty:
        boxed_text = extracted if extracted is not None else ""
        boxed_result = adapter.verify(item.gold, boxed_text)
        boxed_reason = boxed_result.reason_guess
        if boxed_result.accepted:
            fn_kind = FN_EXTRACT
        elif extracted is None:
            fn_kind = FN_AMBIGUOUS
        else:
            fn_kind = FN_WRITE
    return ScoredItem(
        dataset=item.dataset,
        item_id=item.item_id,
        preset=adapter.preset,
        gold=item.gold,
        extracted=extracted,
        actually_correct=actually_correct,
        gold_parsed_empty=result.gold_parsed_empty,
        accepted=result.accepted,
        verify_reason=result.reason_guess,
        fn_kind=fn_kind,
        boxed_only_reason=boxed_reason,
    )


def _summarize(scored: list[ScoredItem]) -> list[SummaryRow]:
    keys = sorted({(item.dataset, item.preset) for item in scored})
    rows: list[SummaryRow] = []
    for dataset, preset in keys:
        subset = [item for item in scored if item.dataset == dataset and item.preset == preset]
        correct = [
            item
            for item in subset
            if item.actually_correct and not item.gold_parsed_empty
        ]
        fn = [item for item in correct if not item.accepted]
        kinds = Counter(item.fn_kind for item in fn)
        rows.append(
            SummaryRow(
                dataset=dataset,
                preset=preset,
                n=len(subset),
                n_gold_unparsed=sum(1 for item in subset if item.gold_parsed_empty),
                n_actually_correct=len(correct),
                n_fn=len(fn),
                n_extract_wrong=kinds[FN_EXTRACT],
                n_write_unrecognized=kinds[FN_WRITE],
                n_ambiguous=kinds[FN_AMBIGUOUS],
            )
        )
    return rows


def write_reports(rows: list[SummaryRow], scored: list[ScoredItem], out_dir: Path) -> None:
    out_dir.mkdir(parents=True, exist_ok=True)
    _write_csv(rows, out_dir / "table.csv")
    _write_markdown(rows, out_dir / "table.md")
    _write_fn_samples(scored, out_dir / "fn_samples.md")
    _write_scored_csv(scored, out_dir / "scored.csv")


def _write_csv(rows: list[SummaryRow], path: Path) -> None:
    fieldnames = [
        "dataset",
        "preset",
        "n",
        "n_gold_unparsed",
        "n_actually_correct",
        "n_fn",
        "fn_rate",
        "n_extract_wrong",
        "n_write_unrecognized",
        "n_ambiguous",
    ]
    with path.open("w", encoding="utf-8", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=fieldnames)
        writer.writeheader()
        for row in rows:
            writer.writerow(
                {
                    "dataset": row.dataset,
                    "preset": row.preset,
                    "n": row.n,
                    "n_gold_unparsed": row.n_gold_unparsed,
                    "n_actually_correct": row.n_actually_correct,
                    "n_fn": row.n_fn,
                    "fn_rate": _rate(row.n_fn, row.n_actually_correct),
                    "n_extract_wrong": row.n_extract_wrong,
                    "n_write_unrecognized": row.n_write_unrecognized,
                    "n_ambiguous": row.n_ambiguous,
                }
            )


def _write_markdown(rows: list[SummaryRow], path: Path) -> None:
    lines = [
        "# Việc 2 — máy chấm gạch nhầm bài model thật",
        "",
        "Lấy lời giải model có sẵn. Cô chấm. Trong các bài **đúng thật** (đọc gold + chỗ khoanh), cô gạch bao nhiêu.",
        "",
        "- **FN** = đúng thật mà cô gạch.",
        "- **lôi nhầm số** = chỉ đưa chỗ khoanh thì cô chịu, đưa cả bài thì gạch.",
        "- **viết đúng máy không nhận** = chỗ khoanh đã đúng gold mà cô vẫn gạch (parse_empty / compare_false).",
        "",
        "| Bộ bài | Preset | Bài | Sách không đọc | Đúng thật | Gạch nhầm / đúng thật | FN | lôi nhầm số | viết không nhận | chưa rõ |",
        "|--------|--------|-----|----------------|-----------|------------------------|----|-------------|-----------------|--------|",
    ]
    for row in rows:
        rate = _rate_pct(row.n_fn, row.n_actually_correct)
        lines.append(
            f"| {row.dataset} | {row.preset} | {row.n} | {row.n_gold_unparsed} | {row.n_actually_correct} "
            f"| {row.n_fn} / {row.n_actually_correct} | {rate} "
            f"| {row.n_extract_wrong} | {row.n_write_unrecognized} | {row.n_ambiguous} |"
        )
    lines.append("")
    path.write_text("\n".join(lines), encoding="utf-8")


def _write_fn_samples(scored: list[ScoredItem], path: Path) -> None:
    lines = [
        "# Việc 2 — vài bài gạch nhầm (đọc gold + chỗ khoanh)",
        "",
        "Mỗi khối: sách, chỗ ta đọc ra, lý do cô, loại FN. Cắt lời dài.",
        "",
    ]
    by_key: dict[tuple[str, str], list[ScoredItem]] = {}
    for item in scored:
        if item.fn_kind is None:
            continue
        by_key.setdefault((item.dataset, item.preset), []).append(item)
    for key in sorted(by_key):
        dataset, preset = key
        lines.append(f"## {dataset} / {preset}")
        lines.append("")
        for item in by_key[key][:8]:
            lines.append(f"- **{item.item_id}** · FN `{item.fn_kind}` · cô `{item.verify_reason}`")
            lines.append(f"  - sách: `{_short(item.gold)}`")
            lines.append(f"  - chỗ khoanh đọc được: `{_short(item.extracted or '—')}`")
            if item.boxed_only_reason:
                lines.append(f"  - chỉ chấm chỗ khoanh: `{item.boxed_only_reason}`")
            lines.append("")
    path.write_text("\n".join(lines), encoding="utf-8")


def _write_scored_csv(scored: list[ScoredItem], path: Path) -> None:
    fieldnames = [
        "dataset",
        "item_id",
        "preset",
        "gold",
        "extracted",
        "actually_correct",
        "gold_parsed_empty",
        "accepted",
        "verify_reason",
        "fn_kind",
        "boxed_only_reason",
    ]
    with path.open("w", encoding="utf-8", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=fieldnames)
        writer.writeheader()
        for item in scored:
            writer.writerow(
                {
                    "dataset": item.dataset,
                    "item_id": item.item_id,
                    "preset": item.preset,
                    "gold": item.gold,
                    "extracted": item.extracted or "",
                    "actually_correct": item.actually_correct,
                    "gold_parsed_empty": item.gold_parsed_empty,
                    "accepted": item.accepted,
                    "verify_reason": item.verify_reason,
                    "fn_kind": item.fn_kind or "",
                    "boxed_only_reason": item.boxed_only_reason or "",
                }
            )


def _manifest(
    args: argparse.Namespace,
    presets: tuple[str, ...],
    traces: list[TraceItem],
    scored: list[ScoredItem],
) -> dict:
    from dacntt.report.manifest import _pkg_version
    from datetime import date, datetime, timezone

    models = sorted({item.model for item in traces})
    return {
        "date": date.today().isoformat(),
        "utc": datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ"),
        "n": args.n,
        "datasets": sorted({item.dataset for item in traces}),
        "presets": list(presets),
        "math_verify_version": _pkg_version("math-verify"),
        "antlr4_version": _pkg_version("antlr4-python3-runtime"),
        "models": models,
        "sources": {
            "gsm8k": {
                "model": GSM8K_MODEL,
                "url": GSM8K_TRACE_URL,
                "note": (
                    "accepted traces (train split). "
                    "Source stored reasoning + answer as JSON fields; "
                    "we join as reasoning + 'The answer is {answer}'. "
                    "Gold from official GSM8K train #### tail."
                ),
            },
            "math500": {
                "model": MATH_MODEL,
                "url": MATH_TRACE_URL,
                "note": "sample_index==0 only (one generation per problem), first n problems.",
            },
        },
        "n_scored": len(scored),
        "human_read": "src/dacntt/read.py extract_final + human_equal (substitutes đọc tay)",
    }


def _parse_args(argv: list[str] | None) -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Việc 2: FN rate on real model traces")
    parser.add_argument("--dataset", choices=("gsm8k", "math500", "both"), default="both")
    parser.add_argument("--n", type=int, default=200, help="traces per dataset")
    parser.add_argument("--presets", default="reward,default")
    parser.add_argument("--out", type=Path, default=_REPO_ROOT / "results" / "viec2")
    parser.add_argument("--cache", type=Path, default=_REPO_ROOT / "data" / "traces")
    parser.add_argument("--gold", type=Path, default=_REPO_ROOT / "data" / "gold")
    return parser.parse_args(argv)


def _presets(raw: str) -> tuple[str, ...]:
    names = tuple(part.strip() for part in raw.split(",") if part.strip())
    unknown = [name for name in names if name not in PRESETS]
    if unknown:
        raise ValueError(f"unknown presets {unknown}; expected {PRESETS}")
    return names


def _rate(num: int, den: int) -> str:
    if den == 0:
        return ""
    return f"{num / den:.4f}"


def _rate_pct(num: int, den: int) -> str:
    if den == 0:
        return "—"
    return f"{num / den:.1%}"


def _short(text: str, limit: int = 120) -> str:
    compact = " ".join(text.split())
    if len(compact) <= limit:
        return compact
    return compact[: limit - 1] + "…"


if __name__ == "__main__":
    raise SystemExit(main())
