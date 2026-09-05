"""Giai đoạn 0.2 CLI (papers/KE-HOACH-MO-RONG.md): re-verify a saved
`generations.jsonl` and split pass@1/pass@k by dataset (GSM8K vs MATH-500)
instead of the pooled number `table.md` reports.

Why this matters: GSM8K's verifier false-negative rate is ~0%, MATH-500's is
~7.8% (Việc 1-2). If GSM8K declines much less than MATH-500 across the same
rounds, that's suggestive (not causal — see the KE-HOACH-MO-RONG.md note on
why this isn't a controlled comparison) evidence that verifier bias, not the
shrinking-pool mechanism alone, drives the decline. Needs no GPU — only
`generations.jsonl` (already has each solution's real text and gold, so
pass@* can be recomputed exactly as the original run did) and a local
math-verify install.

Usage:
  python -m experiments.viec3.analyze_by_dataset \
      --generations results/viec3/qwen15b-n500/generations.jsonl \
      --out results/viec3/qwen15b-n500/by_dataset.md
"""

from __future__ import annotations

import argparse
import json
import sys
from collections import defaultdict
from pathlib import Path

_REPO_ROOT = Path(__file__).resolve().parents[2]
_SRC = _REPO_ROOT / "src"
if str(_SRC) not in sys.path:
    sys.path.insert(0, str(_SRC))

from dacntt.gvt.measure import pass_at
from dacntt.verify.adapter import MathVerifyAdapter
from dacntt.verify.presets import PRESETS


def main(argv: list[str] | None = None) -> int:
    args = _parse_args(argv)
    rows = list(_read_jsonl(args.generations))
    if not rows:
        print(f"no rows in {args.generations}", file=sys.stderr)
        return 1

    k = max(len(row["texts"]) for row in rows)
    adapters = {preset: MathVerifyAdapter(preset) for preset in PRESETS}

    # (round, dataset) -> preset -> list of per-item accept-flag rows
    flags: dict[tuple[int, str], dict[str, list[list[bool]]]] = defaultdict(
        lambda: {preset: [] for preset in PRESETS}
    )
    for row in rows:
        key = (row["round"], row["dataset"])
        for preset, adapter in adapters.items():
            flags[key][preset].append(
                [adapter.verify(row["gold"], text).accepted for text in row["texts"]]
            )

    lines = [
        "# Giai đoạn 0.2 — pass@1/pass@k tách theo bộ đề (không phải số gộp)",
        "",
        f"Tái tính từ `{args.generations.name}` (không gọi lại model, chỉ chạy lại "
        "`math-verify` trên đúng lời giải đã sinh). Số gộp gốc nằm ở `table.md` "
        "cùng thư mục.",
        "",
        "**Đọc thế nào:** nếu GSM8K (verifier gần sạch, FN≈0%) sụp ít hơn hẳn "
        "MATH-500 (verifier lệch, FN≈7.8%) qua cùng các vòng, đó là bằng chứng "
        "gợi ý (không phải control có kiểm soát biến — hai bộ đề còn khác nhau "
        "về độ khó) cho câu hỏi \"có phải verifier lệch gây ra sụp\". Xem "
        "`papers/KE-HOACH-MO-RONG.md` Giai đoạn 0.2 để biết giới hạn của cách đọc này.",
        "",
        f"| Bộ đề | Preset | Vòng | pass@1 | pass@{k} | n đề |",
        "|---|---|---|---|---|---|",
    ]
    for (round_index, dataset), preset_flags in sorted(flags.items()):
        for preset in PRESETS:
            rows_for_preset = preset_flags[preset]
            lines.append(
                f"| {dataset} | {preset} | {round_index} | "
                f"{pass_at(rows_for_preset, 1):.1%} | {pass_at(rows_for_preset, k):.1%} | "
                f"{len(rows_for_preset)} |"
            )

    # One shared adapter is trained each round on the *pooled* accepted
    # solutions from both datasets — so a dataset's own pass@* isn't
    # decided in isolation. This shows whether the training pool's
    # dataset mix shifts across rounds (e.g. one dataset's solutions get
    # crowded out), which would explain cross-dataset interference in the
    # pass@* table above instead of a clean per-dataset verifier-bias story.
    lines += [
        "",
        "## Tỉ lệ mỗi bộ đề trong tập được giữ để train mỗi vòng (preset `reward`)",
        "",
        "Một adapter LoRA chung train trên tập gộp cả hai bộ mỗi vòng — số "
        "dưới đây cho biết tập đó lệch về bộ nào qua từng vòng, có thể giải "
        "thích vì sao pass@* của một bộ bị ảnh hưởng bởi chuyện xảy ra ở bộ "
        "kia (nhiễu chéo giữa hai domain), thay vì mỗi bộ tự sụp độc lập vì "
        "verifier riêng của nó.",
        "",
        "| Vòng | Số lời giải giữ (GSM8K) | Số lời giải giữ (MATH-500) | % GSM8K trong tập train |",
        "|---|---|---|---|",
    ]
    rounds = sorted({r for r, _ in flags})
    for round_index in rounds:
        n_gsm8k = sum(sum(row) for row in flags[(round_index, "gsm8k")]["reward"])
        n_math = sum(sum(row) for row in flags[(round_index, "math500")]["reward"])
        total = n_gsm8k + n_math
        share = n_gsm8k / total if total else 0.0
        lines.append(f"| {round_index} | {n_gsm8k} | {n_math} | {share:.1%} |")

    args.out.parent.mkdir(parents=True, exist_ok=True)
    args.out.write_text("\n".join(lines) + "\n", encoding="utf-8")
    print(f"wrote {args.out}", file=sys.stderr)
    return 0


def _read_jsonl(path: Path):
    with path.open(encoding="utf-8") as handle:
        for line in handle:
            line = line.strip()
            if line:
                yield json.loads(line)


def _parse_args(argv: list[str] | None) -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Giai đoạn 0.2: pass@* split by dataset")
    parser.add_argument("--generations", type=Path, required=True)
    parser.add_argument("--out", type=Path, required=True)
    return parser.parse_args(argv)


if __name__ == "__main__":
    raise SystemExit(main())
