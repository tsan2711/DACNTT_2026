"""Check that every final-round value in results/viec3/regrade/ci.md appears in paper_main.tex
(Table 4 format: $-4.8$ [$-9.0,-0.6$]). Exit 1 on any miss.
Usage: python3 tools/check_numbers.py"""
import re, sys
ci = open("results/viec3/regrade/ci.md").read().splitlines()
tex = (open("papers/latex/paper_main.tex").read() + open("papers/latex/supplementary.tex").read()).replace("{,}", ",")
def t(x):  # '-4.8' -> '$-4.8$'
    return "$" + x.replace("+", "+") + "$"
miss = 0; n = 0
for row in ci:
    if not row.startswith(("| FINAL_", "| G3_")) or "gold_2e-5" in row: continue  # 2e-5 rerun only quoted as absolute pass@1 in text
    cells = [c.strip() for c in row.strip("|").split("|")]
    name = cells[0]
    for c in cells[3:6]:  # pass@1, pass@k, sample acc
        m = re.match(r"([+-][\d.]+) \[([+-][\d.]+), ([+-][\d.]+)\]", c)
        if not m: continue
        d, lo, hi = m.groups(); n += 1
        d_t = d.replace("-", "$-$") if False else d
        pats = [f"{d}", f"{lo},{hi}"]
        ok = all(p.replace("-", "-") in tex.replace("$", "") .replace("−", "-") for p in pats)
        if not ok:
            miss += 1; print("MISS", name, c)
print(f"checked {n} cells, {miss} missing")
sys.exit(1 if miss else 0)
