"""Việc 3 CLI: generate → verify → select → train, measure pass@* and writing style.

Mac toy (not paper numbers):
  .venv/bin/python -m experiments.viec3.run --mode dry --n 20 --rounds 2 --k 4
  .venv/bin/python -m experiments.viec3.run --mode mlx --n 20 --rounds 2 --k 4

Paper numbers (Kaggle T4, needs CUDA — will not run on Mac):
  python -m experiments.viec3.run --mode hf --dataset both --n 500 --rounds 5 --k 8 \
      --model Qwen/Qwen2.5-0.5B-Instruct --max-tokens 512 --out results/viec3/kaggle-0.5b

See experiments/viec3/KAGGLE.md for setup.
"""

from __future__ import annotations

import argparse
import csv
import json
import sys
from pathlib import Path

_REPO_ROOT = Path(__file__).resolve().parents[2]
_SRC = _REPO_ROOT / "src"
if str(_SRC) not in sys.path:
    sys.path.insert(0, str(_SRC))

from dacntt.gold.load import load_gold
from dacntt.gold.sources import DATASETS, GSM8K, MATH500, SOURCES
from dacntt.gvt.generate import HfGenerate, MlxGenerate, ScriptedGenerate
from dacntt.gvt.loop import RoundRecord, run_rounds
from dacntt.gvt.measure import STYLE_IDS
from dacntt.gvt.train import HfLoraSftTrain, MlxLoraTrain, NoOpTrain
from dacntt.report.manifest import _pkg_version, write_manifest
from dacntt.verify.adapter import MathVerifyAdapter
from dacntt.verify.presets import PRESETS

DEFAULT_MLX_MODEL = "mlx-community/Qwen2.5-0.5B-Instruct-4bit"
DEFAULT_HF_MODEL = "Qwen/Qwen2.5-0.5B-Instruct"


def main(argv: list[str] | None = None) -> int:
    args = _parse_args(argv)
    mode = _resolve_mode(args.mode)
    datasets = _datasets(args.dataset)
    exam_presets = _presets(args.exam_presets)
    if args.select_preset not in PRESETS:
        raise ValueError(f"unknown select preset {args.select_preset!r}")
    out_dir: Path = args.out
    cache_dir: Path = args.cache

    if args.model is None:
        args.model = DEFAULT_HF_MODEL if mode == "hf" else DEFAULT_MLX_MODEL

    items = []
    for dataset in datasets:
        items.extend(load_gold(dataset, args.n, cache_dir))
        print(f"loaded {args.n} {dataset} problems", file=sys.stderr)

    select_adapter = MathVerifyAdapter(args.select_preset)
    exam_adapters = {name: MathVerifyAdapter(name) for name in exam_presets}
    if args.select_preset not in exam_adapters:
        exam_adapters[args.select_preset] = select_adapter

    generator, trainer, note = _backend(mode, args, out_dir, items)
    print(note, file=sys.stderr)

    records = run_rounds(
        items,
        generator=generator,
        trainer=trainer,
        select_adapter=select_adapter,
        exam_adapters=exam_adapters,
        rounds=args.rounds,
        k=args.k,
        train=not args.no_train,
        extra_exam=args.extra_exam,
        locked_exam=args.select_preset,
    )
    write_reports(records, items, out_dir, args.k, args.select_preset)
    write_manifest(out_dir / "manifest.json", _manifest(args, mode, note, records, items))
    print(f"wrote {out_dir / 'table.md'}", file=sys.stderr)
    return 0


def _backend(mode: str, args: argparse.Namespace, out_dir: Path, items: list):
    if mode == "dry":
        generator = ScriptedGenerate.from_gold(items, args.k)
        trainer = NoOpTrain()
        note = (
            "mode=dry: scripted generate from gold writing-styles; "
            "real math-verify select+metrics; train is no-op. Not a model run."
        )
        return generator, trainer, note
    if mode == "hf":
        generator = HfGenerate(args.model, max_tokens=args.max_tokens, temp=args.temp)
        trainer = HfLoraSftTrain(
            args.model,
            out_dir / "adapters",
            epochs=args.hf_epochs,
            batch_size=args.hf_batch_size,
            lora_r=args.lora_r,
            lora_alpha=args.lora_alpha,
            max_seq_length=args.max_seq_length,
        )
        note = (
            f"mode=hf: {args.model} LoRA SFT via transformers+peft+TRL. "
            "Kaggle T4 — paper numbers path (experiments/viec3/KAGGLE.md)."
        )
        return generator, trainer, note
    generator = MlxGenerate(
        args.model,
        max_tokens=args.max_tokens,
        temp=args.temp,
    )
    trainer = MlxLoraTrain(
        args.model,
        out_dir / "adapters",
        iters=args.lora_iters,
        batch_size=1,
        num_layers=args.lora_layers,
        max_seq_length=args.max_seq_length,
    )
    note = (
        f"mode=mlx: {args.model} LoRA SFT. "
        "Mac toy — do not treat pass@* as paper numbers."
    )
    return generator, trainer, note


def _resolve_mode(mode: str) -> str:
    if mode in ("dry", "mlx", "hf"):
        return mode
    try:
        import mlx_lm  # noqa: F401

        return "mlx"
    except ImportError:
        return "dry"


def write_reports(
    records: list[RoundRecord],
    items: list,
    out_dir: Path,
    k: int,
    locked: str,
) -> None:
    out_dir.mkdir(parents=True, exist_ok=True)
    _write_metrics_csv(records, out_dir / "metrics.csv", k)
    _write_styles_csv(records, out_dir / "styles.csv")
    _write_abc_csv(records, out_dir / "abc.csv")
    _write_markdown(records, out_dir / "table.md", k, locked)
    _write_generations(records, items, out_dir / "generations.jsonl")


def _write_metrics_csv(records: list[RoundRecord], path: Path, k: int) -> None:
    fieldnames = ["round", "preset", "pass_at_1", "pass_at_k", "k", "n_selected", "n_trained"]
    with path.open("w", encoding="utf-8", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=fieldnames)
        writer.writeheader()
        for record in records:
            presets = sorted({name for kind in record.pass_at.values() for name in kind})
            for preset in presets:
                writer.writerow(
                    {
                        "round": record.round,
                        "preset": preset,
                        "pass_at_1": f"{record.pass_at[1][preset]:.4f}",
                        "pass_at_k": f"{record.pass_at[k][preset]:.4f}",
                        "k": k,
                        "n_selected": record.n_selected,
                        "n_trained": record.n_examples_trained,
                    }
                )


def _write_styles_csv(records: list[RoundRecord], path: Path) -> None:
    fieldnames = ["round", "n", *STYLE_IDS]
    with path.open("w", encoding="utf-8", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=fieldnames)
        writer.writeheader()
        for record in records:
            row = {"round": record.round, "n": record.styles.get("n", 0)}
            for name in STYLE_IDS:
                row[name] = record.styles.get(name, 0)
            writer.writerow(row)


def _write_abc_csv(records: list[RoundRecord], path: Path) -> None:
    with path.open("w", encoding="utf-8", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=["round", "A", "B", "C"])
        writer.writeheader()
        for record in records:
            shift = record.abc or {"A": "", "B": "", "C": ""}
            writer.writerow({"round": record.round, **shift})


def _write_markdown(records: list[RoundRecord], path: Path, k: int, locked: str) -> None:
    lines = [
        "# Việc 3 — vòng generate-verify-select-train",
        "",
        "Mỗi vòng: học sinh làm k lần → cô chấm → giữ bài chịu → ôn. "
        "**Đúng** = máy chấm chịu. Mac toy ≠ số paper.",
        "",
        f"Select (dạy): preset `{locked}`. Exam: mọi preset trong bảng.",
        "",
        f"| Vòng | Preset | pass@1 | pass@{k} | Giữ / ôn | A thêm đề | B ổn định | C mất đề |",
        "|------|--------|--------|----------|----------|-----------|-----------|----------|",
    ]
    for record in records:
        presets = sorted({name for kind in record.pass_at.values() for name in kind})
        abc = record.abc or {"A": "—", "B": "—", "C": "—"}
        for preset in presets:
            lines.append(
                f"| {record.round} | {preset} | {record.pass_at[1][preset]:.1%} | "
                f"{record.pass_at[k][preset]:.1%} | {record.n_selected} | "
                f"{abc['A']} | {abc['B']} | {abc['C']} |"
            )
    lines.extend(["", "## Chữ viết (đếm trên mọi lần làm)", ""])
    header = "| Vòng | n |" + "".join(f" {name} |" for name in STYLE_IDS)
    sep = "|------|---|" + "".join("--------|" for _ in STYLE_IDS)
    lines.append(header)
    lines.append(sep)
    for record in records:
        cells = " | ".join(str(record.styles.get(name, 0)) for name in STYLE_IDS)
        lines.append(f"| {record.round} | {record.styles.get('n', 0)} | {cells} |")
    lines.extend(
        [
            "",
            "Cách đọc (TOI-HIEU): pass@1 tăng **và** pass@k đứng/giảm **và** chữ tụ một kiểu "
            "→ manh mối mạnh đang học chữ cô, không học toán. Một mình một cột thì chưa đủ.",
            "",
        ]
    )
    path.write_text("\n".join(lines), encoding="utf-8")


def _write_generations(records: list[RoundRecord], items: list, path: Path) -> None:
    with path.open("w", encoding="utf-8") as handle:
        for record in records:
            for item, texts in zip(items, record.generations):
                handle.write(
                    json.dumps(
                        {
                            "round": record.round,
                            "item_id": item.item_id,
                            "dataset": item.dataset,
                            "gold": item.gold,
                            "texts": texts,
                        },
                        ensure_ascii=False,
                    )
                    + "\n"
                )


def _manifest(args, mode: str, note: str, records: list[RoundRecord], items: list) -> dict:
    from datetime import date, datetime, timezone

    return {
        "date": date.today().isoformat(),
        "utc": datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ"),
        "viec": 3,
        "mode": mode,
        "note": note,
        "paper_quality": False,
        "n": args.n,
        "rounds": args.rounds,
        "k": args.k,
        "max_tokens": args.max_tokens,
        "datasets": sorted({item.dataset for item in items}),
        "select_preset": args.select_preset,
        "exam_presets": [p.strip() for p in args.exam_presets.split(",") if p.strip()],
        "locked_exam": args.select_preset,
        "model": args.model if mode in ("mlx", "hf") else "scripted-from-gold",
        "train": {"mlx": "mlx-lora-sft", "hf": "hf-lora-sft"}.get(mode, "noop"),
        "lora_iters": args.lora_iters if mode == "mlx" else 0,
        "lora_r": args.lora_r if mode == "hf" else 0,
        "lora_alpha": args.lora_alpha if mode == "hf" else 0,
        "hf_epochs": args.hf_epochs if mode == "hf" else 0,
        "math_verify_version": _pkg_version("math-verify"),
        "antlr4_version": _pkg_version("antlr4-python3-runtime"),
        "mlx_lm_version": _pkg_version("mlx-lm"),
        "transformers_version": _pkg_version("transformers"),
        "peft_version": _pkg_version("peft"),
        "trl_version": _pkg_version("trl"),
        "n_records": len(records),
        "gold_urls": {item.dataset: SOURCES[item.dataset].url for item in items},
    }


def _parse_args(argv: list[str] | None) -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Việc 3: GVT loop + pass@* / style")
    parser.add_argument("--mode", choices=("auto", "dry", "mlx", "hf"), default="auto")
    parser.add_argument("--dataset", choices=("gsm8k", "math500", "both"), default="gsm8k")
    parser.add_argument("--n", type=int, default=100, help="problems (Mac cap 100)")
    parser.add_argument("--rounds", type=int, default=2)
    parser.add_argument("--k", type=int, default=4, help="samples/problem; 8 if the box allows")
    parser.add_argument("--max-tokens", type=int, default=96)
    parser.add_argument("--temp", type=float, default=0.8)
    parser.add_argument("--select-preset", default="reward")
    parser.add_argument("--exam-presets", default="reward,default")
    parser.add_argument("--model", default=None, help="default depends on --mode")
    parser.add_argument("--lora-iters", type=int, default=30, help="mlx mode only")
    parser.add_argument("--lora-layers", type=int, default=8, help="mlx mode only")
    parser.add_argument("--lora-r", type=int, default=16, help="hf mode only")
    parser.add_argument("--lora-alpha", type=int, default=32, help="hf mode only")
    parser.add_argument("--hf-epochs", type=float, default=1.0, help="hf mode only")
    parser.add_argument("--hf-batch-size", type=int, default=2, help="hf mode only")
    parser.add_argument("--max-seq-length", type=int, default=512)
    parser.add_argument("--no-train", action="store_true")
    parser.add_argument(
        "--extra-exam",
        action="store_true",
        help="one more generate after the last train",
    )
    parser.add_argument("--out", type=Path, default=_REPO_ROOT / "results" / "viec3")
    parser.add_argument("--cache", type=Path, default=_REPO_ROOT / "data" / "gold")
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
