import sys; sys.argv=[sys.argv[0]]
sys.path.insert(0, "/Users/tsangcuteso1/Documents/GitHub/DACNTT_2026/experiments/viec3/review_cpu")
import tokenizers
class _T:
    @staticmethod
    def from_file(p): return None
tokenizers.Tokenizer=_T
import glob as _g; _og=_g.glob; _g.glob=lambda p: (["x"] if "tokenizer.json" in p else _og(p))
import capanat as C
runs = ["a-math500-lr-fixed","b-math500-lr-fixed","a-math500-lr-fixed-seed2","b-math500-lr-fixed-seed2",
        "nofilter-math500-lr-fixed","nofilter-math500-seed2","a-lr2e4-seed1","a-lr2e4-seed2",
        "a-math500-lr1e4","a-lr1e4-seed2","a-lr1e4-seed3","qwen15b-math500-a-seed1","qwen15b-math500-a","qwen15b-gsm8k-c",
        "c-gsm8k-lr5e4","gold-math500-lr-fixed","gold-math500-seed2","a-lr5e4-keep","a-lr5e4-msl1024"]
for run in runs:
    try: m, flags, toks, ex = C.load(run)
    except Exception as e: print(run, "ERR", e); continue
    last = max(rd for rd,_ in flags)
    def st(rd):
        F=[f for i in ex for f in flags[(rd,i)]]; N=[n for i in ex for n in toks[(rd,i)]]
        fin=[f for f,n in zip(F,N) if n<C.CAP]; cap=[f for f,n in zip(F,N) if n>=C.CAP]
        s=len(fin)/len(F); return s, sum(fin)/len(fin), (sum(cap)/len(cap) if cap else 0), sum(F)/len(F)
    s0,f0,c0,a0=st(0); s1,f1,c1,a1=st(last)
    sb=(s0+s1)/2; fb=(f0+f1)/2; cb=(c0+c1)/2
    pf=sb*(f1-f0); ps=(s1-s0)*(fb-cb); pc=(1-sb)*(c1-c0); d=a1-a0
    # boxed share all gens and on finished
    print(f"{run:28s} R{last} dAcc {100*d:+.2f} = fin {100*pf:+.2f} ({pf/d*100 if d else 0:.0f}%) capshare {100*ps:+.2f} ({ps/d*100 if d else 0:.0f}%) capacc {100*pc:+.2f} ({pc/d*100 if d else 0:.0f}%) | caphit {100*(1-s0):.1f}->{100*(1-s1):.1f} capacc {100*c0:.1f}->{100*c1:.1f}")
