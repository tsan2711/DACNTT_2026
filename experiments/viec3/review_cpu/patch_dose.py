"""Re-verify with the two patches (dfrac->frac = Run B; wrap gold in boxed = Run D) to measure the dose
of each patch on the training pool and on exam scores, CPU only."""
import json, sys
from multiprocessing import Pool
from pathlib import Path

REPO = Path("/Users/tsangcuteso1/Documents/GitHub/DACNTT_2026")
sys.path.insert(0, str(REPO / "src"))
from dacntt.verify.adapter import MathVerifyAdapter  # noqa

OUT = Path(__file__).parent / "patched"
OUT.mkdir(exist_ok=True)
VARIANTS = {"frac": (True, False), "boxed": (False, True), "both": (True, True)}
_AD = {}


def ad(v):
    if v not in _AD:
        f, b = VARIANTS[v]
        _AD[v] = MathVerifyAdapter("reward", timeout_seconds=5, normalize_frac_commands=f, normalize_gold_boxed=b)
    return _AD[v]


def work(rec):
    return {"round": rec["round"], "item_id": rec["item_id"],
            **{v: [bool(ad(v).verify(rec["gold"], t).accepted) for t in rec["texts"]] for v in VARIANTS}}


if __name__ == "__main__":
    with Pool(8) as pool:
        for run in sys.argv[1:]:
            dst = OUT / f"{run}.json"
            if dst.exists():
                continue
            recs = [json.loads(l) for l in open(REPO / "results/viec3" / run / "generations.jsonl")]
            dst.write_text(json.dumps(pool.map(work, recs, chunksize=8)))
            print("done", run, flush=True)
