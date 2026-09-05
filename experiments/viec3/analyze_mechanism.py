"""Giai đoạn 5 CLI: compare fitting speed / pre-filter diversity across runs.

No GPU needed — reads files a Kaggle run already writes (once downloaded):
`generations.jsonl` (always written) and `train_logs/round_*.json` (written
when the run used `--mode hf`, since HfLoraSftTrain is the only trainer that
logs per-round loss).

Usage:
  python -m experiments.viec3.analyze_mechanism \
      --run 0.5B=results/viec3/qwen05b-n500 \
      --run 1.5B=results/viec3/qwen15b-n500 \
      --out results/viec3/mechanism.md

See papers/KE-HOACH-MO-RONG.md, Giai đoạn 5.
"""

from __future__ import annotations

import argparse
import sys
from pathlib import Path

_REPO_ROOT = Path(__file__).resolve().parents[2]
_SRC = _REPO_ROOT / "src"
if str(_SRC) not in sys.path:
    sys.path.insert(0, str(_SRC))

from dacntt.report.mechanism import diversity_by_round, train_loss_by_round


def main(argv: list[str] | None = None) -> int:
    args = _parse_args(argv)
    runs = dict(_parse_run(spec) for spec in args.run)

    lines = [
        "# Giai đoạn 5 — tốc độ fit + đa dạng trước lọc, theo model",
        "",
        "Đọc từ `generations.jsonl` (đa dạng trước lọc) và "
        "`train_logs/round_*.json` (loss cuối mỗi vòng, chỉ có nếu chạy "
        "`--mode hf`). Không cần GPU để chạy file này.",
        "",
    ]
    any_data = False
    for label, run_dir in runs.items():
        lines.append(f"## {label} (`{run_dir}`)")
        lines.append("")

        gen_path = run_dir / "generations.jsonl"
        if gen_path.is_file():
            any_data = True
            rows = diversity_by_round(gen_path)
            lines.append(
                "**Đa dạng output trước khi lọc qua verifier.** Text thô gần như "
                "luôn ~1.0 (sampling ở temperature>0 hiếm khi lặp y hệt từng chữ) — "
                "cột đáng đọc là đáp án đã trích (`extract_final`+chuẩn hoá), vì đó "
                "mới bắt được hội tụ thật (nhiều cách viết khác nhau nhưng cùng ra "
                "một đáp án):"
            )
            lines.append("")
            lines.append(
                "| Vòng | n đề | unique text/k | unique đáp án/k | % đề cả k lần "
                "ra CÙNG 1 đáp án |"
            )
            lines.append("|---|---|---|---|---|")
            for row in rows:
                lines.append(
                    f"| {row.round} | {row.n_items} | {row.mean_unique_text_ratio:.3f} | "
                    f"{row.mean_unique_answer_ratio:.3f} | {row.all_same_answer_frac:.1%} |"
                )
            lines.append("")
        else:
            lines.append(f"_Không thấy `{gen_path}` — bỏ qua phần đa dạng._")
            lines.append("")

        log_dir = run_dir / "train_logs"
        if log_dir.is_dir() and any(log_dir.glob("round_*.json")):
            any_data = True
            rows = train_loss_by_round(log_dir)
            lines.append("**Train loss cuối mỗi vòng** (SFTTrainer, trên đúng tập được giữ vòng đó):")
            lines.append("")
            lines.append("| Vòng | Loss cuối | Số bước log |")
            lines.append("|---|---|---|")
            for row in rows:
                loss_str = f"{row.final_loss:.4f}" if row.final_loss is not None else "—"
                lines.append(f"| {row.round} | {loss_str} | {row.n_log_steps} |")
            lines.append("")
        else:
            lines.append(
                f"_Không thấy `{log_dir}/round_*.json` — bỏ qua phần train loss "
                "(chỉ `--mode hf` mới ghi log này)._"
            )
            lines.append("")

    if not any_data:
        print(
            "Không tìm thấy generations.jsonl/train_logs nào trong các --run đã cho — "
            "kiểm tra lại đường dẫn, hoặc tải file từ Kaggle output về trước.",
            file=sys.stderr,
        )
        return 1

    args.out.parent.mkdir(parents=True, exist_ok=True)
    args.out.write_text("\n".join(lines), encoding="utf-8")
    print(f"wrote {args.out}", file=sys.stderr)
    return 0


def _parse_run(spec: str) -> tuple[str, Path]:
    if "=" not in spec:
        raise ValueError(f"--run must be LABEL=PATH, got {spec!r}")
    label, path = spec.split("=", 1)
    return label.strip(), Path(path.strip())


def _parse_args(argv: list[str] | None) -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Giai đoạn 5: mechanism analysis, no GPU")
    parser.add_argument(
        "--run",
        action="append",
        required=True,
        help="LABEL=PATH, repeatable (e.g. --run 0.5B=results/viec3/qwen05b-n500)",
    )
    parser.add_argument(
        "--out", type=Path, default=_REPO_ROOT / "results" / "viec3" / "mechanism.md"
    )
    return parser.parse_args(argv)


if __name__ == "__main__":
    raise SystemExit(main())
