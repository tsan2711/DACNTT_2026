"""Re-score one saved round-N model with different generation token caps.

    python -m experiments.viec3.reeval --out DIR --snapshot 2 --caps 512 1536 \
        --model Qwen/Qwen2.5-1.5B-Instruct --dataset math500 --n 500 \
        --seed 1 --holdout-frac 0.3 --k 4

``adapters_ckpt_N`` (kept by run.py --keep-snapshots) is the adapter that took
round N's exam. Generating the same exam problems from it under a small and a
large cap, with everything else fixed, tests whether a decline is the model
losing accuracy or finishing fewer solutions inside the cap (the fixed-token-cap
failure of Xu et al., arXiv:2608.20290). Writes DIR/reeval_N.json.
"""

from __future__ import annotations

import os

os.environ.setdefault("CUDA_VISIBLE_DEVICES", "0")

import argparse
import json
import statistics
import sys
from pathlib import Path

_REPO_ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(_REPO_ROOT / "src"))
sys.path.insert(0, str(_REPO_ROOT))

DEGENERATE_CHARS = 1500


def is_degenerate(text: str) -> bool:
    return len(text) > DEGENERATE_CHARS and "\\boxed" not in text


def summarize(golds: list[str], texts_by_item: list[list[str]], accepts) -> dict:
    """pass@1 (first sample), pass@k, sample accuracy, length, and the split of
    accuracy into degenerate (long, no \\boxed) and finished generations."""
    flags = [[accepts(g, t) for t in texts] for g, texts in zip(golds, texts_by_item)]
    flat_texts = [t for texts in texts_by_item for t in texts]
    flat_flags = [f for row in flags for f in row]
    degenerate = [is_degenerate(t) for t in flat_texts]
    done = [f for f, d in zip(flat_flags, degenerate) if not d]
    return {
        "pass_at_1": sum(1 for row in flags if row and row[0]) / len(flags),
        "pass_at_k": sum(1 for row in flags if any(row)) / len(flags),
        "sample_acc": sum(flat_flags) / len(flat_flags),
        "mean_chars": statistics.mean(len(t) for t in flat_texts),
        "degenerate_share": sum(degenerate) / len(degenerate),
        "acc_finished": (sum(done) / len(done)) if done else None,
    }


def main(argv: list[str] | None = None) -> int:
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--out", type=Path, required=True)
    ap.add_argument("--snapshot", type=int, required=True, help="N in adapters_ckpt_N; 0 = base model, no adapter")
    ap.add_argument("--caps", type=int, nargs="+", default=[512, 1536])
    ap.add_argument("--model", default="Qwen/Qwen2.5-1.5B-Instruct")
    ap.add_argument("--dataset", default="math500")
    ap.add_argument("--n", type=int, default=500)
    ap.add_argument("--seed", type=int, default=1)
    ap.add_argument("--holdout-frac", type=float, default=0.3)
    ap.add_argument("--k", type=int, default=4)
    ap.add_argument("--temp", type=float, default=0.8)
    ap.add_argument("--gen-batch-size", type=int, default=8)
    ap.add_argument("--patch-verifier", action="store_true")
    args = ap.parse_args(argv)

    from experiments.viec3.run import _prefetch_then_go_offline, _seed_everything, _split_train_test
    from dacntt.gold.load import load_gold
    from dacntt.gvt.generate import HfGenerate
    from dacntt.verify.adapter import MathVerifyAdapter

    args.out.mkdir(parents=True, exist_ok=True)
    adapter_dir = args.out / f"adapters_ckpt_{args.snapshot}"
    if args.snapshot > 0 and not adapter_dir.exists():
        raise SystemExit(f"{adapter_dir} missing — run with --keep-snapshots")
    adapter_path = str(adapter_dir) if args.snapshot > 0 else None  # snapshot 0 = untrained base
    items = load_gold(args.dataset, args.n, _REPO_ROOT / "data" / "gold")
    _, test_ids = _split_train_test(items, args.holdout_frac, args.seed)
    exam = [it for it in items if f"{it.dataset}:{it.item_id}" in test_ids]
    verifier = MathVerifyAdapter("reward", timeout_seconds=3, normalize_frac_commands=args.patch_verifier)
    _prefetch_then_go_offline(args.model)

    result: dict = {"snapshot": args.snapshot, "n_exam": len(exam), "k": args.k, "caps": {}}
    for cap in args.caps:
        _seed_everything(args.seed + 1000)
        gen = HfGenerate(args.model, adapter_path=adapter_path, max_tokens=cap,
                         temp=args.temp, gen_batch_size=args.gen_batch_size)
        texts = gen.generate_batch([it.problem for it in exam], k=args.k)
        result["caps"][str(cap)] = summarize(
            [it.gold for it in exam], texts, lambda g, t: verifier.verify(g, t).accepted
        )
        print(f"cap {cap}: {result['caps'][str(cap)]}", flush=True)
        del gen
    (args.out / f"reeval_{args.snapshot}.json").write_text(json.dumps(result, indent=1), encoding="utf-8")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
