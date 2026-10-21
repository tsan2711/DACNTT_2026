"""Re-verify every generation of every viec3 run with the project's MathVerifyAdapter.
Writes scratchpad/scored/<run>.json: list of {round,item_id,dataset,flags,lens,boxed}."""
import json, sys, os
from multiprocessing import Pool
from pathlib import Path

REPO = Path("/Users/tsangcuteso1/Documents/GitHub/DACNTT_2026")
sys.path.insert(0, str(REPO / "src"))
from dacntt.verify.adapter import MathVerifyAdapter  # noqa

OUT = Path(__file__).parent / "scored"
OUT.mkdir(exist_ok=True)
_AD = {}


def _ad(patch):
    if patch not in _AD:
        _AD[patch] = MathVerifyAdapter("reward", timeout_seconds=5, normalize_frac_commands=patch)
    return _AD[patch]


def work(args):
    rec, patch = args
    ad = _ad(patch)
    flags = [bool(ad.verify(rec["gold"], t).accepted) for t in rec["texts"]]
    return {
        "round": rec["round"], "item_id": rec["item_id"], "dataset": rec["dataset"],
        "flags": flags, "lens": [len(t) for t in rec["texts"]],
        "boxed": ["\\boxed" in t for t in rec["texts"]],
        "dfrac": ["\\dfrac" in t for t in rec["texts"]],
        "tfrac": ["\\tfrac" in t for t in rec["texts"]],
    }


def main(runs):
    with Pool(8) as pool:
        for run in runs:
            d = REPO / "results/viec3" / run
            dst = OUT / f"{run}.json"
            if dst.exists():
                continue
            m = json.loads((d / "manifest.json").read_text())
            patch = bool(m.get("patch_verifier"))
            recs = [json.loads(l) for l in open(d / "generations.jsonl")]
            res = pool.map(work, [(r, patch) for r in recs], chunksize=8)
            dst.write_text(json.dumps(res))
            print("done", run, len(res), "patch", patch, flush=True)


if __name__ == "__main__":
    main(sys.argv[1:])
