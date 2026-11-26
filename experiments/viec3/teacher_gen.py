"""B1 (plan 2026-11-15): generate full teacher solutions for the final-round selection pool and keep the correct ones.

Pool = exactly the 300 MATH-train problems that run.py draws for --train-pool-n 300 --seed S (same code path).
Teacher = Qwen2.5-7B-Instruct split over both T4s (device_map=auto); fallback --model Qwen/Qwen2.5-3B-Instruct.
A sample is kept only if BOTH graders accept it (V' = math-verify with patched gold, and the normalised string match)
and it finished (a \\boxed answer, fewer than max_tokens-4 tokens). One random kept sample per problem, then a random
subset of --keep problems (298 = the dose of the loop arm at seed 1).

    PYTHONPATH=src:. python -u -m experiments.viec3.teacher_gen --out results/viec3/teacher-gen-7b
Resumable: re-running skips problems already in generations.jsonl.
Outputs: generations.jsonl (every sample + both grades), teacher_solutions.jsonl (training file for
run.py --train-on-gold --teacher-solutions), summary.json.
"""
from __future__ import annotations

import argparse
import json
import random
import statistics as st
import sys
from pathlib import Path

REPO = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(REPO / "src"))
sys.path.insert(0, str(REPO))

from dacntt.gold.load import load_gold  # noqa: E402
from dacntt.gold.sources import MATHTRAIN  # noqa: E402
from dacntt.gvt.generate import user_prompt  # noqa: E402
from dacntt.verify.adapter import MathVerifyAdapter  # noqa: E402
from experiments.viec3.regrade_all import string_ok  # noqa: E402


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--model", default="Qwen/Qwen2.5-7B-Instruct")
    ap.add_argument("--out", type=Path, required=True)
    ap.add_argument("--seed", type=int, default=1, help="same as the gate/loop seed (defines the pool)")
    ap.add_argument("--pool", type=int, default=300)
    ap.add_argument("--k", type=int, default=4)
    ap.add_argument("--max-tokens", type=int, default=1024)
    ap.add_argument("--temp", type=float, default=0.8)
    ap.add_argument("--batch", type=int, default=8, help="problems per generate() call (x k sequences)")
    ap.add_argument("--keep", type=int, default=298, help="number of problems kept")
    ap.add_argument("--per-problem", type=int, default=1,
                    help="distinct verified solutions kept per problem (up to this many; 1 = old behaviour)")
    ap.add_argument("--max-problems", type=int, default=None, help="debug: only the first N pool problems")
    ap.add_argument("--cache", type=Path, default=REPO / "data" / "gold")
    args = ap.parse_args()
    args.out.mkdir(parents=True, exist_ok=True)

    pool = load_gold(MATHTRAIN, 12000, args.cache, fix_gold=True)
    pool = random.Random(args.seed or 0).sample(pool, args.pool)
    if args.max_problems:
        pool = pool[: args.max_problems]
    gen_path = args.out / "generations.jsonl"
    done = set()
    if gen_path.exists():
        done = {json.loads(l)["item_id"] for l in gen_path.open(encoding="utf-8") if l.strip()}
    todo = [it for it in pool if it.item_id not in done]
    print(f"pool {len(pool)}, already done {len(done)}, to do {len(todo)}", flush=True)

    ver = MathVerifyAdapter("reward", timeout_seconds=10, normalize_frac_commands=True, normalize_gold_boxed=True)

    if todo:
        import torch
        from transformers import AutoModelForCausalLM, AutoTokenizer

        tok = AutoTokenizer.from_pretrained(args.model)
        if tok.pad_token is None:
            tok.pad_token = tok.eos_token
        tok.padding_side = "left"
        ngpu = torch.cuda.device_count()
        mm = None
        if ngpu >= 2:
            mm = {0: "11GiB", 1: "13GiB"}  # weights ~15 GB for 7B fp16; leave room for the KV cache
        print(f"loading {args.model} on {ngpu} GPU(s), max_memory={mm}", flush=True)
        model = AutoModelForCausalLM.from_pretrained(args.model, dtype=torch.float16, device_map="auto", max_memory=mm)
        model.eval()
        print("loaded", flush=True)
        with gen_path.open("a", encoding="utf-8") as fh:
            for s in range(0, len(todo), args.batch):
                chunk = todo[s : s + args.batch]
                prompts = [tok.apply_chat_template([{"role": "user", "content": user_prompt(it.problem)}],
                                                   add_generation_prompt=True, tokenize=False) for it in chunk]
                inp = tok(prompts, return_tensors="pt", padding=True).to(model.device)
                with torch.no_grad():
                    out = model.generate(**inp, max_new_tokens=args.max_tokens, do_sample=True,
                                         temperature=args.temp, num_return_sequences=args.k,
                                         pad_token_id=tok.pad_token_id)
                plen = inp["input_ids"].shape[1]
                rows = out[:, plen:]
                for i, it in enumerate(chunk):
                    texts, ntoks = [], []
                    for r in rows[i * args.k : (i + 1) * args.k]:
                        ids = r.tolist()
                        n = len(ids)
                        while n and ids[n - 1] == tok.pad_token_id:
                            n -= 1
                        ntoks.append(n)
                        texts.append(tok.decode(r, skip_special_tokens=True))
                    v = [bool(ver.verify(it.gold, t).accepted) for t in texts]
                    sm = [string_ok(it.gold, t) for t in texts]
                    fh.write(json.dumps({"dataset": it.dataset, "item_id": it.item_id, "gold": it.gold,
                                         "texts": texts, "ntok": ntoks, "v": v, "s": sm},
                                        ensure_ascii=False) + "\n")
                fh.flush()
                print(f"  {min(s + args.batch, len(todo))}/{len(todo)} problems", flush=True)

    # ---- select
    rec = [json.loads(l) for l in gen_path.open(encoding="utf-8") if l.strip()]
    rng = random.Random(args.seed)
    cap = args.max_tokens - 4
    cands = {}
    n_samples = n_v = n_s = n_both = 0
    lens_all, lens_ok = [], []
    for r in rec:
        good = []
        for t, n, v, s in zip(r["texts"], r["ntok"], r["v"], r["s"]):
            n_samples += 1
            n_v += v
            n_s += s
            n_both += v and s
            lens_all.append(len(t))
            if v and s and n < cap and "\\boxed" in t:
                good.append(t)
                lens_ok.append(len(t))
        if good:
            uniq = list(dict.fromkeys(good))
            rng.shuffle(uniq)
            cands[r["item_id"]] = (r["dataset"], uniq[: args.per_problem])
    ids = sorted(cands)
    rng.shuffle(ids)
    kept = ids[: args.keep]
    with (args.out / "teacher_solutions.jsonl").open("w", encoding="utf-8") as fh:
        for i in kept:
            ds, sols = cands[i]
            for sol in sols:
                fh.write(json.dumps({"dataset": ds, "item_id": i, "solution": sol}, ensure_ascii=False) + "\n")
    summary = {
        "model": args.model, "k": args.k, "max_tokens": args.max_tokens, "temp": args.temp,
        "problems": len(rec), "samples": n_samples,
        "sample_acc_v": n_v / max(n_samples, 1), "sample_acc_string": n_s / max(n_samples, 1),
        "sample_acc_both": n_both / max(n_samples, 1),
        "problems_with_a_kept_solution": len(cands), "kept_for_training": len(kept),
        "solutions_kept": sum(len(cands[i][1]) for i in kept), "per_problem": args.per_problem,
        "median_chars_all": st.median(lens_all) if lens_all else None,
        "median_chars_kept": st.median(lens_ok) if lens_ok else None,
    }
    (args.out / "summary.json").write_text(json.dumps(summary, indent=1))
    print(json.dumps(summary, indent=1), flush=True)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
