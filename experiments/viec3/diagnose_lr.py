"""Giai đoạn 8 — kiểm tra nghi vấn tốc độ học (learning rate) quá thấp.

Bối cảnh: `HfLoraSftTrain` (src/dacntt/gvt/train.py) dùng learning_rate=1e-5
cho LoRA r=16 (chỉ q_proj/v_proj) từ commit đầu tiên, chưa ai kiểm tra lại.
Tài liệu tra được cho LoRA r=16 trên tác vụ toán tương đương (MetaMath,
LoRA-Adam) khuyến nghị ~5e-4 (arXiv 2602.04998) — thấp hơn khoảng 50 lần.
Nếu đúng, mỗi vòng train gần như không dịch chuyển được adapter, bất kể đưa
dữ liệu gì vào — giải thích tầm thường hơn cho cả hai hiện tượng đang thấy:
pass@1 đứng yên, và A so B (vá verifier) không khác nhau.

Việc script này làm: lấy lại đúng tập được `select` giữ ở VÒNG 0 của Run A
(dữ liệu đã tải về, không cần GPU Kaggle mới), train hai lần — một lần với
learning_rate=1e-5 (tái lập mặc định hiện tại), một lần với 5e-4 — mọi tham
số khác giữ y hệt (lora_r=16, target_modules=(q_proj,v_proj), 1 epoch, cùng
seed, cùng dữ liệu). So sánh đường loss.

Không sửa gì trong train.py/run.py — chỉ dùng lại đúng các hàm select/verify
đã có, không viết lại logic lọc.

Máy Mac không có torch/transformers/peft/trl (đúng quy ước KHONG-LAM.md:
Mac chỉ thử code, số liệu thật lấy trên Kaggle). Nên script tách 2 bước:

  Bước 1 — chạy trên Mac, không cần GPU, không cần torch. Chọn lại đúng tập
  round-0 mà `select` đã giữ trong Run A, ghi ra một JSONL nhỏ:
      .venv/bin/python -m experiments.viec3.diagnose_lr --select-only \
          --n-examples 120

  Bước 2 — chạy trên Kaggle (đã có sẵn torch/transformers/peft/trl, dùng
  đúng notebook đang chạy các lần R1-R5), sau khi upload
  results/viec3/diagnose-lr/sft_examples.jsonl làm input dataset:
      !PYTHONPATH=src:. python -m experiments.viec3.diagnose_lr \
          --examples-jsonl /kaggle/input/<dataset>/sft_examples.jsonl \
          --out /kaggle/working/diagnose-lr
  Tải lại results/diagnose-lr/comparison.json về máy sau khi chạy xong.
"""

from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path

_REPO_ROOT = Path(__file__).resolve().parents[2]
_SRC = _REPO_ROOT / "src"
if str(_SRC) not in sys.path:
    sys.path.insert(0, str(_SRC))

from dacntt.gold.load import load_gold  # noqa: E402
from dacntt.gvt.select import select_batch  # noqa: E402
from dacntt.gvt.train import TrainExample  # noqa: E402
from dacntt.verify.adapter import MathVerifyAdapter  # noqa: E402

DEFAULT_GEN = _REPO_ROOT / "results/viec3/qwen15b-math500-a/generations.jsonl"
MODEL_ID = "Qwen/Qwen2.5-1.5B-Instruct"


def _load_round0_examples(generations_path: Path, n_examples: int) -> list[TrainExample]:
    """Rebuild the exact (problem, solution) pairs Run A's round-0 `select`
    kept, using the *same* select_batch + reward-preset verifier real runs
    use — not a hand-rolled filter."""
    rows = []
    with generations_path.open(encoding="utf-8") as f:
        for line in f:
            row = json.loads(line)
            if row["round"] == 0 and row["dataset"] == "math500":
                rows.append(row)
    if not rows:
        raise SystemExit(f"no round-0 math500 rows found in {generations_path}")

    # item_id in generations.jsonl is the dataset's own path-like id
    # (e.g. "test/precalculus/807.json"); load_gold returns items in the
    # same fixed order the run used, keyed the same way — match by item_id.
    cache_dir = _REPO_ROOT / "data" / "gold"
    gold_items = {item.item_id: item for item in load_gold("math500", 500, cache_dir)}

    select_adapter = MathVerifyAdapter("reward")
    examples: list[TrainExample] = []
    for row in rows:
        item = gold_items.get(row["item_id"])
        if item is None or not item.problem:
            continue
        kept = select_batch(row["gold"], row["texts"], select_adapter)
        examples.extend(TrainExample(problem=item.problem, solution=s) for s in kept)
        if len(examples) >= n_examples:
            break
    return examples[:n_examples]


def _train_one(
    examples: list[TrainExample],
    *,
    learning_rate: float,
    out_dir: Path,
) -> list[dict]:
    """Run one LoRA SFT pass with HfLoraSftTrain's own code path (not a
    reimplementation), just with adapter_path/log_dir redirected to a
    scratch dir per learning rate, and return trainer.state.log_history."""
    from dacntt.gvt.train import HfLoraSftTrain

    trainer = HfLoraSftTrain(
        MODEL_ID,
        out_dir,
        learning_rate=learning_rate,
        log_dir=out_dir / "logs",
    )
    trainer.train(examples, round=0)
    log_path = out_dir / "logs" / "round_0.json"
    if log_path.exists():
        return json.loads(log_path.read_text(encoding="utf-8"))
    return []


def _write_examples_jsonl(examples: list[TrainExample], path: Path) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", encoding="utf-8") as f:
        for ex in examples:
            f.write(json.dumps({"problem": ex.problem, "solution": ex.solution}, ensure_ascii=False) + "\n")


def _read_examples_jsonl(path: Path) -> list[TrainExample]:
    examples = []
    with path.open(encoding="utf-8") as f:
        for line in f:
            row = json.loads(line)
            examples.append(TrainExample(problem=row["problem"], solution=row["solution"]))
    return examples


def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--generations", type=Path, default=DEFAULT_GEN)
    ap.add_argument("--n-examples", type=int, default=120, help="cap for a fast local check")
    ap.add_argument("--lr-a", type=float, default=1e-5, help="current default (suspect too low)")
    ap.add_argument("--lr-b", type=float, default=5e-4, help="candidate fix (arXiv 2602.04998, r=16 math)")
    ap.add_argument("--out", type=Path, default=_REPO_ROOT / "results/viec3/diagnose-lr")
    ap.add_argument(
        "--select-only", action="store_true",
        help="Bước 1 (chạy trên Mac, không cần torch): chỉ chọn lại tập round-0, ghi JSONL rồi dừng.",
    )
    ap.add_argument(
        "--examples-jsonl", type=Path, default=None,
        help="Bước 2 (chạy trên Kaggle): đọc tập đã chọn từ đây thay vì tự chọn lại (cần khi máy không có torch).",
    )
    args = ap.parse_args()

    if args.examples_jsonl is not None:
        examples = _read_examples_jsonl(args.examples_jsonl)
        print(f"loaded {len(examples)} examples from {args.examples_jsonl}", file=sys.stderr)
    else:
        examples = _load_round0_examples(args.generations, args.n_examples)
        print(f"round-0 examples reselected: {len(examples)} (cap {args.n_examples})", file=sys.stderr)

    if len(examples) < 10:
        print("too few examples to read anything from a loss curve — raise --n-examples", file=sys.stderr)
        return 1

    if args.select_only:
        out_path = args.out / "sft_examples.jsonl"
        _write_examples_jsonl(examples, out_path)
        print(f"wrote {out_path} ({len(examples)} examples) — upload this as a Kaggle dataset,", file=sys.stderr)
        print("then run this script again ON KAGGLE with --examples-jsonl pointing at it.", file=sys.stderr)
        return 0

    results = {}
    for label, lr in (("lr_a_current", args.lr_a), ("lr_b_candidate", args.lr_b)):
        print(f"\n=== training with learning_rate={lr} ({label}) ===", file=sys.stderr)
        history = _train_one(examples, learning_rate=lr, out_dir=args.out / label)
        losses = [h["loss"] for h in history if "loss" in h]
        results[label] = {"learning_rate": lr, "losses": losses}
        if losses:
            print(f"  loss: first={losses[0]:.4f} last={losses[-1]:.4f} (n={len(losses)} logged steps)", file=sys.stderr)
        else:
            print("  no loss logged (too few steps for logging_steps=10?) — lower --n-examples's batch or check log path", file=sys.stderr)

    out_json = args.out / "comparison.json"
    args.out.mkdir(parents=True, exist_ok=True)
    out_json.write_text(json.dumps(results, indent=2), encoding="utf-8")

    print("\n=== so sánh ===", file=sys.stderr)
    for label, r in results.items():
        losses = r["losses"]
        tail = f"{losses[0]:.4f} -> {losses[-1]:.4f}" if losses else "(rỗng)"
        print(f"{label:16s} lr={r['learning_rate']:<10g} loss {tail}", file=sys.stderr)
    print(f"\nĐọc kết quả: nếu lr_b_candidate tụt SÂU HƠN RÕ RỆT so với lr_a_current,", file=sys.stderr)
    print("tốc độ học hiện tại (1e-5) đúng là quá thấp — cần chạy lại A/B/C với lr đã sửa", file=sys.stderr)
    print("trước khi chạy 3 thí nghiệm đang hàng chờ. Chi tiết: " + str(out_json), file=sys.stderr)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
