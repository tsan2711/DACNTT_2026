# Kích thước pool mỗi vòng của Design P (0.5B, 1.5B): đếm lời giải được verifier preset reward nhận.
import json, sys
from collections import Counter
from multiprocessing import Pool
from pathlib import Path
REPO = Path("/Users/tsangcuteso1/Documents/GitHub/DACNTT_2026"); sys.path.insert(0, str(REPO/"src"))
from dacntt.verify.adapter import MathVerifyAdapter
_A = []
def work(rec):
    if not _A: _A.append(MathVerifyAdapter("reward", timeout_seconds=5))
    return rec["round"], sum(bool(_A[0].verify(rec["gold"], t).accepted) for t in rec["texts"])
if __name__ == "__main__":
    for run in ["qwen05b-n500", "qwen15b-n500"]:
        recs = [json.loads(l) for l in open(REPO/"results/viec3"/run/"generations.jsonl")]
        c = Counter()
        with Pool(8) as p:
            for rd, n in p.imap_unordered(work, recs, chunksize=16): c[rd] += n
        print(run, dict(sorted(c.items())), flush=True)
