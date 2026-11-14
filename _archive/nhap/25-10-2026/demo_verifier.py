"""Demo cho buổi báo cáo: lỗi lưu gold làm verifier loại nhầm lời giải đúng. Chỉ cần CPU.

    .venv/bin/python tools/demo_verifier.py            # 3 phần: ví dụ tay, ví dụ thật, bảng tổng
    .venv/bin/python tools/demo_verifier.py --live 200 # thêm: chấm lại trực tiếp 200 lời giải

Phần 1 và 2 chấm trực tiếp bằng math-verify. Phần 3 đọc kết quả đã chấm sẵn trong
experiments/viec3/review_cpu/{scored,patched}/ (chấm lại cả 2000 lời giải mất vài phút).
"""
import argparse
import csv
import json
import random
import sys
from collections import Counter
from pathlib import Path

REPO = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(REPO / "src"))
from dacntt.verify.adapter import MathVerifyAdapter  # noqa: E402

CPU = REPO / "experiments/viec3/review_cpu"
GEN = REPO / "results/viec3"
RUN = "a-math500-lr-fixed"

ORIG = MathVerifyAdapter("reward", timeout_seconds=5)
FIXED = MathVerifyAdapter("reward", timeout_seconds=5, normalize_gold_boxed=True)


def mark(ok):
    return "\033[32mĐÚNG\033[0m" if ok else "\033[31mSAI\033[0m"


def last_box(text):
    i = text.rfind("\\boxed{")
    if i < 0:
        return None
    j = start = i + 7
    depth = 1
    while j < len(text) and depth:
        depth += {"{": 1, "}": -1}.get(text[j], 0)
        j += 1
    return text[start:j - 1]


def pause(args):
    if not args.no_pause:
        input("\n  [Enter để tiếp] ")


def part1(args):
    print("\n=== 1. Ví dụ tay: cùng một đáp án 4/3 ===")
    gold = "\\frac43"
    pred = "... Vậy đáp số là \\boxed{\\frac{4}{3}}."
    print(f"  gold lưu trong dataset : {gold}")
    print(f"  model viết             : {pred}")
    print(f"  verifier gốc           : {mark(ORIG.verify(gold, pred).accepted)}")
    print(f"  verifier đã vá         : {mark(FIXED.verify(gold, pred).accepted)}"
          f"   (vá = bọc gold vào \\boxed{{}} trước khi so)")
    pause(args)


def part2(args):
    print(f"\n=== 2. Ví dụ thật: lời giải của model ở vòng 0 ({RUN}) ===")
    problems = {}
    for line in open(REPO / "data/gold/math500_test.jsonl"):
        r = json.loads(line)
        problems[r.get("unique_id") or r.get("item_id")] = r["problem"]
    flips = []
    for line in open(GEN / RUN / "generations.jsonl"):
        r = json.loads(line)
        if r["round"] != 0:
            continue
        for t in r["texts"]:
            box = last_box(t)
            if box and box.strip() and not ORIG.verify(r["gold"], t).accepted \
                    and FIXED.verify(r["gold"], t).accepted:
                flips.append((r["item_id"], r["gold"], box))
                break
        if len(flips) >= 40:
            break
    for item, gold, box in random.Random(args.seed).sample(flips, 3):
        prob = problems.get(item, "")
        print(f"\n  đề {item}: {prob[:160]}{'...' if len(prob) > 160 else ''}")
        print(f"    gold      : {gold}")
        print(f"    model ghi : \\boxed{{{box}}}")
        print("    verifier gốc " + mark(False) + "  /  đã vá " + mark(True))
    pause(args)


def part3(args):
    print("\n=== 3. Trên toàn bộ 500 đề MATH-500, mọi lời giải của mọi vòng (số đã chấm sẵn) ===")
    print("  (2 run đầu: mỗi đề 4 lời giải; qwen15b-math500-a: mỗi đề 8 lời giải)")
    print("  run                     vòng   gốc nhận / vá nhận   bị loại nhầm")
    for run in ["a-math500-lr-fixed", "a-math500-lr-fixed-seed2", "qwen15b-math500-a"]:
        orig, fixed = Counter(), Counter()
        for r in json.loads((CPU / "scored" / f"{run}.json").read_text()):
            orig[r["round"]] += sum(r["flags"])
        for r in json.loads((CPU / "patched" / f"{run}.json").read_text()):
            fixed[r["round"]] += sum(r["boxed"])
        for k in sorted(fixed):
            print(f"  {run:24s} {k:>3}    {orig[k]:>5} / {fixed[k]:<5}       "
                  f"{(fixed[k] - orig[k]) / fixed[k] * 100:5.1f}%")
    print("\n  → khoảng 15.5–18.4%: cứ ~6 lời giải đúng thì verifier gốc vứt 1 khỏi tập train.")
    pause(args)


# (tên hiển thị, run, nhóm) — lần chạy 1 của mỗi cấu hình, cùng 150 đề thi; khớp Bảng 3, 4, 6 của paper
SCORE_RUNS = [
    ("tốc độ học 1e-5 (Run A, 5 vòng)", "qwen15b-math500-a", "lr"),
    ("tốc độ học 1e-4", "a-math500-lr1e4", "lr"),
    ("tốc độ học 2e-4", "a-lr2e4-seed1", "lr"),
    ("tốc độ học 5e-4", "a-math500-lr-fixed", "lr"),
    ("không lọc (học cả bài sai)", "nofilter-math500-lr-fixed", "ctl"),
    ("học lời giải mẫu của sách", "gold-math500-lr-fixed", "ctl"),
]


def bar(p, width=40):
    return "█" * round(p * width)


def part4(args):
    print("\n=== 4. Kết quả chính: model có giỏi lên qua các vòng tự học không? ===")
    print("  Điểm pass@1 trên 150 đề thi model không được học (lần chạy 1).")
    print("  Vòng 0 = model gốc chưa học. Mỗi █ = 2,5 điểm.\n")
    for name, run, group in SCORE_RUNS:
        if group == "ctl" and name == SCORE_RUNS[4][0]:
            print("  -- đối chứng ở tốc độ học 5e-4 --")
        rows = [r for r in csv.DictReader(open(GEN / run / "metrics.csv")) if r["preset"] == "reward"]
        print(f"  {name}")
        for r in rows:
            p = float(r["pass_at_1"])
            print(f"    vòng {r['round']}  {p * 100:5.1f}%  {bar(p)}")
        d = (float(rows[-1]["pass_at_1"]) - float(rows[0]["pass_at_1"])) * 100
        print(f"    → vòng cuối so với vòng 0: {d:+.1f} điểm\n")
    print("  → Không cấu hình nào giỏi lên rõ ràng. Học nhanh (5e-4) thì tụt.")
    print("    Lệch dưới ~7 điểm nằm trong sai số của 150 đề (khoảng tin cậy ở Bảng 5 paper).")
    pause(args)


# Hai đề MATH-500 model gốc làm đúng cả 4 lần, model vòng 2 (lr 5e-4) sai cả 4 lần
BEFORE_AFTER = [
    ("test/prealgebra/572.json", "viết dài lan man, hết 512 token chưa ra đáp số"),
    ("test/algebra/858.json", "viết xong hẳn nhưng ra đáp số sai"),
]


def part5(args):
    print("\n=== 5. Cùng một đề: model gốc so với model sau 2 vòng học (lr 5e-4) ===")
    print("  Hai lý do model tụt (paper mục 4.5): bị cắt vì viết quá dài, và làm xong mà sai.")
    problems, gold = {}, {}
    for line in open(REPO / "data/gold/math500_test.jsonl"):
        r = json.loads(line)
        problems[r.get("unique_id") or r.get("item_id")] = r["problem"]
    texts = {}
    for line in open(GEN / RUN / "generations.jsonl"):
        r = json.loads(line)
        if r["item_id"] in dict(BEFORE_AFTER) and r["round"] in (0, 2):
            texts[r["item_id"], r["round"]] = r["texts"][0]
            gold[r["item_id"]] = r["gold"]
    for item, why in BEFORE_AFTER:
        print(f"\n  đề: {problems[item]}   (đáp án sách: {gold[item]})")
        for rd, label in ((0, "model gốc"), (2, "sau 2 vòng")):
            t = texts[item, rd]
            box = last_box(t)
            tail = " ".join(t[-260:].split())
            print(f"\n   [{label}] dài {len(t)} ký tự, đáp số: {box if box else '(không có, bị cắt)'}"
                  f"  {mark(rd == 0)}")
            print(f"     ...{tail}")
        print(f"\n   → lý do: {why}")
        pause(args)


def live(args):
    print(f"\n=== 6. Chấm lại trực tiếp {args.live} lời giải ngẫu nhiên (máy gốc so với máy vá) ===")
    pairs = []
    for line in open(GEN / RUN / "generations.jsonl"):
        r = json.loads(line)
        if r["round"] == 0:
            pairs += [(r["gold"], t) for t in r["texts"]]
    pairs = random.Random(args.seed).sample(pairs, args.live)
    o = f = 0
    for i, (g, t) in enumerate(pairs, 1):
        o += ORIG.verify(g, t).accepted
        f += FIXED.verify(g, t).accepted
        print(f"\r  {i}/{len(pairs)}  gốc nhận {o}, vá nhận {f}", end="", flush=True)
    print(f"\n  bị loại nhầm: {(f - o) / max(f, 1) * 100:.1f}% số lời giải đúng")


if __name__ == "__main__":
    ap = argparse.ArgumentParser()
    ap.add_argument("--live", type=int, default=0)
    ap.add_argument("--seed", type=int, default=0)
    ap.add_argument("--no-pause", action="store_true")
    a = ap.parse_args()
    part1(a)
    part2(a)
    part3(a)
    part4(a)
    part5(a)
    if a.live:
        live(a)
