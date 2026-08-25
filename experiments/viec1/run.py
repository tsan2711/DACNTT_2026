"""Việc 1 CLI: gold answers × writing styles × math-verify presets → table.

python -m experiments.viec1.run --dataset both --n 200 --presets default,reward
python -m experiments.viec1.run --dataset gsm8k --limit 20
"""

from __future__ import annotations

import argparse
import sys
from pathlib import Path

_REPO_ROOT = Path(__file__).resolve().parents[2]
_SRC = _REPO_ROOT / "src"
if str(_SRC) not in sys.path:
    sys.path.insert(0, str(_SRC))

from dacntt.gold.load import GoldItem, load_gold
from dacntt.gold.sources import DATASETS, GSM8K, MATH500, SOURCES
from dacntt.report.manifest import build_manifest, write_manifest
from dacntt.report.table import TableRow, majority_reasons, write_reports
from dacntt.variants.registry import VariantSpec, variants_for
from dacntt.verify.adapter import MathVerifyAdapter
from dacntt.verify.presets import PRESETS


def main(argv: list[str] | None = None) -> int:
    args = _parse_args(argv)
    datasets = _datasets(args.dataset)
    presets = _presets(args.presets)
    n = args.limit if args.limit is not None else args.n
    out_dir: Path = args.out
    cache_dir: Path = args.cache

    rows: list[TableRow] = []
    adapters = {preset: MathVerifyAdapter(preset) for preset in presets}
    for dataset in datasets:
        items = load_gold(dataset, n, cache_dir)
        print(f"loaded {len(items)} gold answers from {dataset}", file=sys.stderr)
        for spec in variants_for(dataset):
            for preset in presets:
                row = _run_cell(items, spec, adapters[preset])
                rows.append(row)
                print(
                    f"{row.dataset} | {row.variant_id} | {row.preset}: "
                    f"{row.n_reject}/{row.n}",
                    file=sys.stderr,
                )

    write_reports(rows, out_dir)
    write_manifest(
        out_dir / "manifest.json",
        build_manifest(
            presets=list(presets),
            n=n,
            limit=args.limit,
            datasets=list(datasets),
            gold_urls={name: SOURCES[name].url for name in datasets},
        ),
    )
    print(f"wrote {out_dir / 'table.md'}", file=sys.stderr)
    return 0


def _run_cell(items: list[GoldItem], spec: VariantSpec, adapter: MathVerifyAdapter) -> TableRow:
    reject_reasons: list[str] = []
    n = 0
    n_reject = 0
    dataset = items[0].dataset if items else ""
    for item in items:
        text = spec.rewrite(item.gold)
        if text is None:
            continue
        n += 1
        result = adapter.verify(item.gold, text)
        if not result.accepted:
            n_reject += 1
            reject_reasons.append(result.reason_guess)
    return TableRow(
        dataset=dataset,
        variant_id=spec.id,
        variant_label=spec.label,
        preset=adapter.preset,
        n_reject=n_reject,
        n=n,
        reason_guess=majority_reasons(reject_reasons),
    )


def _parse_args(argv: list[str] | None) -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Việc 1: verifier writing-style table")
    parser.add_argument(
        "--dataset",
        choices=("gsm8k", "math500", "both"),
        default="both",
    )
    parser.add_argument("--n", type=int, default=200, help="gold answers per dataset")
    parser.add_argument("--limit", type=int, default=None, help="smoke cap (overrides --n)")
    parser.add_argument(
        "--presets",
        default="default,reward",
        help="comma-separated: default,reward",
    )
    parser.add_argument(
        "--out",
        type=Path,
        default=_REPO_ROOT / "results" / "viec1",
    )
    parser.add_argument(
        "--cache",
        type=Path,
        default=_REPO_ROOT / "data" / "gold",
    )
    return parser.parse_args(argv)


def _datasets(name: str) -> tuple[str, ...]:
    if name == "both":
        return DATASETS
    if name in (GSM8K, MATH500):
        return (name,)
    raise ValueError(name)


def _presets(raw: str) -> tuple[str, ...]:
    names = tuple(part.strip() for part in raw.split(",") if part.strip())
    unknown = [name for name in names if name not in PRESETS]
    if unknown:
        raise ValueError(f"unknown presets {unknown}; expected {PRESETS}")
    return names


if __name__ == "__main__":
    raise SystemExit(main())
