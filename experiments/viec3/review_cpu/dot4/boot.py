# Bootstrap theo bài (paired, 2000 lần) cho: thay đổi cap-hit, và ba phần của decomposition.
import sys, random; sys.argv=[sys.argv[0]]
sys.path.insert(0, "/Users/tsangcuteso1/Documents/GitHub/DACNTT_2026/experiments/viec3/review_cpu")
import tokenizers
class _T:
    @staticmethod
    def from_file(p): return None
tokenizers.Tokenizer=_T
import glob as _g; _og=_g.glob; _g.glob=lambda p: (["x"] if "tokenizer.json" in p else _og(p))
import capanat as C
runs = ["a-math500-lr-fixed","b-math500-lr-fixed","a-math500-lr-fixed-seed2","b-math500-lr-fixed-seed2",
        "nofilter-math500-lr-fixed","nofilter-math500-seed2","a-lr5e4-keep","a-lr5e4-msl1024","c-gsm8k-lr5e4",
        "a-lr2e4-seed1","a-lr2e4-seed2","a-math500-lr1e4","a-lr1e4-seed2","a-lr1e4-seed3"]
def parts(ex, flags, toks, last):
    def st(rd):
        F=[f for i in ex for f in flags[(rd,i)]]; N=[n for i in ex for n in toks[(rd,i)]]
        fin=[f for f,n in zip(F,N) if n<C.CAP]; cap=[f for f,n in zip(F,N) if n>=C.CAP]
        return len(fin)/len(F), sum(fin)/max(len(fin),1), (sum(cap)/len(cap) if cap else 0), sum(F)/len(F)
    s0,f0,c0,a0=st(0); s1,f1,c1,a1=st(last)
    sb=(s0+s1)/2; fb=(f0+f1)/2; cb=(c0+c1)/2
    return (s0-s1)*100, sb*(f1-f0)*100, (s1-s0)*(fb-cb)*100, (1-sb)*(c1-c0)*100, (a1-a0)*100
def q(xs): xs=sorted(xs); return xs[int(.025*len(xs))], xs[int(.975*len(xs))-1]
rng=random.Random(0)
for run in runs:
    m, flags, toks, ex = C.load(run); last=max(rd for rd,_ in flags); ex=list(ex)
    dcap,pf,ps,pc,d = parts(ex,flags,toks,last)
    B=[parts([rng.choice(ex) for _ in ex],flags,toks,last) for _ in range(2000)]
    sh=[b[1]/b[4] for b in B if b[4]<0]
    print(f"{run:26s} dCap {dcap:+.1f} [{q([b[0] for b in B])[0]:+.1f},{q([b[0] for b in B])[1]:+.1f}] | dAcc {d:+.1f} = fin {pf:+.1f} capshare {ps:+.1f} capacc {pc:+.1f} | fin share {pf/d*100:.0f}% [{q(sh)[0]*100:.0f},{q(sh)[1]*100:.0f}] (n={len(sh)})")
