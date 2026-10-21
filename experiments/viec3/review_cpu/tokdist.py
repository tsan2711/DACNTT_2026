import json, glob, os, collections
from tokenizers import Tokenizer
tok = Tokenizer.from_file(glob.glob(os.path.expanduser("~/.cache/huggingface/hub/models--Qwen--Qwen2.5-1.5B-Instruct/snapshots/*/tokenizer.json"))[0])
R="/Users/tsangcuteso1/Documents/GitHub/DACNTT_2026/results/viec3/a-math500-lr-fixed/generations.jsonl"
c=collections.Counter(); boxed_end=0; n=0
for l in open(R):
    r=json.loads(l)
    if r["round"]!=0: continue
    for t in r["texts"]:
        k=len(tok.encode(t,add_special_tokens=False).ids); n+=1
        c[min(k//16*16,560)]+=1
print(n, sorted(c.items())[-8:])
print("exact counts 500-515:", {k:v for k,v in c.items() if k>=480})
