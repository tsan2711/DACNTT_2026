"""Quick report deck, 25/10/2026: 10 slides, one idea per slide, plain Vietnamese.

Condensed from make_final_pptx.py (same helpers and design system; that script stays as the
full 15-slide backup). Numbers come from paper_revised.tex.

    .venv/bin/python tools/make_quick_pptx.py
"""


import json
from collections import Counter

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt  # noqa: E402
from pptx import Presentation  # noqa: E402
from pptx.util import Emu, Pt  # noqa: E402
from pptx.dml.color import RGBColor  # noqa: E402
from pptx.enum.text import PP_ALIGN, MSO_ANCHOR  # noqa: E402
from pptx.enum.shapes import MSO_CONNECTOR, MSO_SHAPE  # noqa: E402

REPO = "/Users/tsangcuteso1/Documents/GitHub/DACNTT_2026"
OUT = f"{REPO}/25-10-2026/BaoCaoNhanh_25-10_52300057_52300006.pptx"
FIG = f"{REPO}/papers/figures"
CPU = f"{REPO}/experiments/viec3/review_cpu"

INK = RGBColor(0x16, 0x16, 0x1A)
BODY = RGBColor(0x3F, 0x41, 0x49)
MUTED = RGBColor(0x8A, 0x8D, 0x96)
HAIR = RGBColor(0xE6, 0xE6, 0xEA)
SURFACE = RGBColor(0xF5, 0xF5, 0xF7)
WHITE = RGBColor(0xFF, 0xFF, 0xFF)
DARK = RGBColor(0x16, 0x16, 0x1A)
DARKMUTED = RGBColor(0x9A, 0x9C, 0xA5)

CRIMSON = RGBColor(0x9E, 0x2B, 0x34)
BLUE = RGBColor(0x01, 0x73, 0xB2)
ORANGE = RGBColor(0xB8, 0x5C, 0x00)
GREEN = RGBColor(0x02, 0x9E, 0x73)
GREY = RGBColor(0x6B, 0x6E, 0x78)

DISPLAY = "Georgia"
SANS = "Helvetica Neue"

SW, SH = 12191695, 6858000
L = 800100
W = 10591495
R = L + W


# ---------------------------------------------------------------- charts
def _style(ax):
    for side in ("top", "right", "left"):
        ax.spines[side].set_visible(False)
    ax.spines["bottom"].set_color("#C9CAD0")
    ax.tick_params(colors="#6B6E78", length=0, labelsize=12)
    ax.yaxis.grid(True, color="#E6E6EA", lw=1)
    ax.set_axisbelow(True)


def chart_lr(path):
    """Sample-accuracy change R0->R2 per learning rate (paper Table lrseries / ci)."""
    plt.rcParams["font.family"] = ["Helvetica Neue", "Arial", "DejaVu Sans"]
    rates = ["1e-4", "2e-4", "5e-4"]
    s1 = [-1.5, -3.5, -8.3]
    s2 = [-3.7, -3.8, -4.7]
    fig, ax = plt.subplots(figsize=(8.4, 4.2), dpi=220)
    x = range(len(rates))
    b1 = ax.bar([i - 0.19 for i in x], s1, 0.36, color="#0173B2", label="seed 1")
    b2 = ax.bar([i + 0.19 for i in x], s2, 0.36, color="#B85C00", label="seed 2")
    for bars in (b1, b2):
        for b in bars:
            ax.text(b.get_x() + b.get_width() / 2, b.get_height() - 0.35,
                    f"{b.get_height():+.1f}", ha="center", va="top", fontsize=12,
                    color="#16161A")
    ax.axhline(0, color="#16161A", lw=1)
    ax.set_xticks(list(x), [f"lr {r}" for r in rates])
    ax.set_ylim(-10.5, 1)
    ax.set_ylabel("độ chính xác mẫu, vòng 2 − vòng 0 (điểm)", color="#6B6E78", fontsize=11)
    _style(ax)
    ax.legend(frameon=False, fontsize=12, loc="lower left")
    fig.tight_layout()
    fig.savefig(path, transparent=False, facecolor="white")
    plt.close(fig)


def chart_verifier(path):
    """Accepted by original vs patched verifier, per round, Run A seed 1 (saved re-scores)."""
    run = "a-math500-lr-fixed"
    orig, fixed = Counter(), Counter()
    for r in json.load(open(f"{CPU}/scored/{run}.json")):
        orig[r["round"]] += sum(r["flags"])
    for r in json.load(open(f"{CPU}/patched/{run}.json")):
        fixed[r["round"]] += sum(r["boxed"])
    rounds = sorted(fixed)
    fig, ax = plt.subplots(figsize=(7.2, 4.2), dpi=220)
    ax.bar([i - 0.19 for i in rounds], [fixed[k] for k in rounds], 0.36, color="#029E73",
           label="verifier đã vá nhận")
    ax.bar([i + 0.19 for i in rounds], [orig[k] for k in rounds], 0.36, color="#9E2B34",
           label="verifier gốc nhận")
    for k in rounds:
        pct = (fixed[k] - orig[k]) / fixed[k] * 100
        ax.text(k, fixed[k] + 25, f"−{pct:.1f}%", ha="center", fontsize=13,
                color="#9E2B34", fontweight="bold")
    ax.set_xticks(rounds, [f"vòng {k}" for k in rounds])
    ax.set_ylim(0, 900)
    ax.set_ylabel("số lời giải được nhận (trên 2.000)", color="#6B6E78", fontsize=11)
    _style(ax)
    ax.legend(frameon=False, fontsize=11, loc="upper right")
    fig.tight_layout()
    fig.savefig(path, facecolor="white")
    plt.close(fig)


chart_lr(f"{FIG}/final_lr.png")
chart_verifier(f"{FIG}/final_verifier.png")

# ---------------------------------------------------------------- helpers
prs = Presentation()
prs.slide_width = Emu(SW)
prs.slide_height = Emu(SH)
BLANK = prs.slide_layouts[6]


def tb(slide, left, top, width, height, text, *, size, font=SANS, bold=False,
       color=INK, align=PP_ALIGN.LEFT, spacing=6, line_spacing=None):
    box = slide.shapes.add_textbox(Emu(left), Emu(top), Emu(width), Emu(height))
    tf = box.text_frame
    tf.word_wrap = True
    tf.margin_left = tf.margin_right = tf.margin_top = tf.margin_bottom = 0
    for i, line in enumerate(text.split("\n")):
        p = tf.paragraphs[0] if i == 0 else tf.add_paragraph()
        p.alignment = align
        p.space_after = Pt(spacing)
        if line_spacing:
            p.line_spacing = line_spacing
        r = p.add_run()
        r.text = line
        r.font.name = font
        r.font.size = Pt(size)
        r.font.bold = bold
        r.font.color.rgb = color
    return box


def panel(slide, left, top, width, height, *, fill=SURFACE, radius=0.04):
    sh = slide.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, Emu(left), Emu(top),
                                Emu(width), Emu(height))
    sh.fill.solid()
    sh.fill.fore_color.rgb = fill
    sh.line.fill.background()
    sh.shadow.inherit = False
    try:
        sh.adjustments[0] = radius
    except Exception:
        pass
    return sh


def pill(slide, left, top, text, *, fill, width=1750000, height=330000, size=10.5):
    sh = panel(slide, left, top, width, height, fill=fill, radius=0.5)
    tf = sh.text_frame
    tf.word_wrap = False
    tf.margin_left = tf.margin_right = 0
    tf.vertical_anchor = MSO_ANCHOR.MIDDLE
    p = tf.paragraphs[0]
    p.alignment = PP_ALIGN.CENTER
    r = p.add_run()
    r.text = text
    r.font.name = SANS
    r.font.size = Pt(size)
    r.font.bold = True
    r.font.color.rgb = WHITE
    return sh


def rule(slide, left, top, width, color=HAIR, pt=0.75):
    c = slide.shapes.add_connector(MSO_CONNECTOR.STRAIGHT, Emu(left), Emu(top),
                                   Emu(left + width), Emu(top))
    c.line.color.rgb = color
    c.line.width = Pt(pt)
    return c


def bg(slide, color):
    sh = slide.shapes.add_shape(MSO_SHAPE.RECTANGLE, 0, 0, Emu(SW), Emu(SH))
    sh.fill.solid()
    sh.fill.fore_color.rgb = color
    sh.line.fill.background()
    sh.shadow.inherit = False
    return sh


def header(slide, num, label, title, *, sub=None):
    tb(slide, L, 430000, 7000000, 250000, label, size=10.5, bold=True, color=CRIMSON)
    tb(slide, R - 900000, 400000, 900000, 400000, f"{num:02d}", size=15,
       font=DISPLAY, bold=True, color=HAIR, align=PP_ALIGN.RIGHT)
    tb(slide, L, 790000, W, 620000, title, size=28, font=DISPLAY, bold=True,
       color=INK, line_spacing=1.05)
    if sub:
        tb(slide, L, 1500000, W, 420000, sub, size=13, color=MUTED, line_spacing=1.25)


def table(slide, top, cols, rows, *, rowh=430000, hsize=11, rsize=12,
          pad=170000, emph=None, pills=None):
    for x, w, h in cols:
        tb(slide, x, top, w, 300000, h, size=hsize, bold=True, color=MUTED)
    ptop = top + 380000
    pheight = rowh * len(rows) + pad
    panel(slide, L - 120000, ptop, W + 240000, pheight)
    y = ptop + pad // 2
    for i, row in enumerate(rows):
        is_emph = emph(i) if emph else False
        for j, ((x, w, _), val) in enumerate(zip(cols, row)):
            if pills and (i, j) in pills:
                colour, txt = pills[(i, j)]
                pill(slide, x, y + 25000, txt, fill=colour, width=min(w, 1850000))
                continue
            tb(slide, x, y + 55000, w, 330000, val, size=rsize,
               bold=is_emph, color=INK if is_emph else BODY)
        y += rowh
        if i < len(rows) - 1:
            rule(slide, L - 40000, y, W + 80000, color=RGBColor(0xE9, 0xE9, 0xED))
    return ptop + pheight


def takeaway(slide, top, text, *, height=620000):
    panel(slide, L - 120000, top, W + 240000, height)
    rule_x = L + 60000
    bar = slide.shapes.add_shape(MSO_SHAPE.RECTANGLE, Emu(L - 120000), Emu(top),
                                 Emu(60000), Emu(height))
    bar.fill.solid()
    bar.fill.fore_color.rgb = CRIMSON
    bar.line.fill.background()
    tb(slide, rule_x + 120000, top + 150000, W - 300000, height - 200000, text,
       size=14, font=DISPLAY, color=INK, line_spacing=1.3)


def notes(slide, text):
    slide.notes_slide.notes_text_frame.text = text


def new():
    return prs.slides.add_slide(BLANK)


n = 0


def num():
    global n
    n += 1
    return n



# =========================================================== 1 title
s = new()
panel(s, 0, 0, SW, 150000, fill=CRIMSON, radius=0)
tb(s, L, 1180000, W, 300000, "ĐỒ ÁN CÔNG NGHỆ THÔNG TIN  ·  BÁO CÁO KẾT QUẢ",
   size=12, bold=True, color=CRIMSON)
tb(s, L, 1700000, 10400000, 1900000,
   "Tự học có làm model nhỏ\ngiỏi toán hơn không?",
   size=42, font=DISPLAY, bold=True, color=INK, line_spacing=1.08)
tb(s, L, 3800000, 9600000, 1000000,
   "Câu trả lời ngắn: không thấy tiến bộ nào đo được.\n"
   "Qwen2.5-1.5B · LoRA · máy chấm math-verify · MATH-500 và GSM8K",
   size=16, color=BODY, line_spacing=1.4)
rule(s, L, 5150000, 2400000, color=CRIMSON, pt=2.0)
tb(s, L, 5380000, 8000000, 300000,
   "Nguyễn Tấn Sang (52300057)  ·  Trần Duy Anh (52300006)", size=13, bold=True, color=INK)
tb(s, L, 5720000, 6000000, 300000, "25 tháng 10, 2026", size=12, color=MUTED)
notes(s, "Mở đầu bằng câu trả lời luôn, rồi đi qua: câu hỏi, cách làm, 3 kết quả, demo, kết luận. "
         "Khoảng 10 phút.")

# =========================================================== 2 question
s = new()
header(s, num(), "CÂU HỎI", "Model tự làm bài, tự chọn bài đúng để học lại")
for i, (k, h, d) in enumerate([
    ("1", "Làm bài", "Model giải mỗi đề\nnhiều lần."),
    ("2", "Chấm", "Máy chấm chỉ so\nđáp án cuối."),
    ("3", "Học lại", "Fine-tune trên các\nlời giải được nhận."),
]):
    x = L + i * 3560000
    panel(s, x, 1700000, 3300000, 1800000)
    tb(s, x + 240000, 1860000, 400000, 330000, k, size=17, font=DISPLAY, bold=True, color=CRIMSON)
    tb(s, x + 240000, 2250000, 2900000, 330000, h, size=16, bold=True, color=INK)
    tb(s, x + 240000, 2630000, 2900000, 600000, d, size=13, color=BODY, line_spacing=1.3)
tb(s, L, 3700000, W, 300000, "Lặp 3–5 vòng. Đây là vòng lặp của STaR, ReST, RFT.",
   size=13, color=MUTED)
takeaway(s, 4200000,
         "Sau nhiều vòng: model giỏi toán hơn thật,\n"
         "hay chỉ học cách viết mà máy chấm chịu nhận?", height=1000000)
tb(s, L, 5450000, W, 600000,
   "Đo trên 150 đề thi riêng model không được học: pass@1, pass@k, kiểu chữ (\\boxed), số đề thêm/mất.",
   size=12.5, color=MUTED, line_spacing=1.35)
notes(s, "Máy chấm không đọc lời giải, chỉ nhìn đáp án cuối. Vì vậy có nhánh thứ hai của câu hỏi. "
         "4 thước đo được chốt TRƯỚC khi chạy.")

# =========================================================== 3 setup
s = new()
header(s, num(), "CÁCH LÀM", "Thử đủ nhiều cấu hình để không bỏ sót tiến bộ")
for i, (big, colr, cap) in enumerate([
    ("4", INK, "learning rate\n1e-5 → 5e-4"),
    ("2–3", INK, "seed mỗi cấu hình\n(đề thi khác nhau)"),
    ("3", INK, "đối chứng: vá máy chấm,\nbỏ lọc, học lời giải gốc"),
    ("150", INK, "đề thi tách riêng,\nkhoảng tin cậy bootstrap"),
]):
    x = L + i * 2680000
    panel(s, x - 60000, 1750000, 2500000, 1900000)
    tb(s, x + 120000, 1950000, 2200000, 700000, big, size=36, font=DISPLAY, bold=True, color=colr)
    tb(s, x + 120000, 2750000, 2200000, 800000, cap, size=13, color=BODY, line_spacing=1.3)
takeaway(s, 4050000,
         "Lần đầu (trộn 2 bộ dữ liệu, chấm trên chính tập train) model tụt 50 → 18,6%.\n"
         "Làm lại cho sạch thì cú sụp đó không lặp lại.", height=1000000)
notes(s, "Thiết kế gộp P khác thiết kế cô lập I ở nhiều điểm cùng lúc, trong đó P train nhiều bước hơn "
         "khoảng 4,5 lần mỗi vòng. Nên nhóm không kết luận nguyên nhân cú sụp.")

# =========================================================== 4 result 1
s = new()
header(s, num(), "KẾT QUẢ 1", "Không learning rate nào làm model giỏi lên",
       sub="Thay đổi độ chính xác sau 2 vòng, MATH-500. Mọi cột đều âm.")
s.shapes.add_picture(f"{FIG}/final_lr.png", Emu(L - 100000), Emu(2000000), width=Emu(6900000))
x = L + 7100000
for j, (big, colr, cap) in enumerate([
    ("0", INK, "run nào tăng pass@1 hay pass@k\nmột cách chắc chắn"),
    ("≤ +2,2", INK, "điểm: mức tăng lớn nhất\ndữ liệu còn cho phép"),
    ("lr cao", ORANGE, "→ tụt rõ: lời giải viết xong\nkém chính xác hơn"),
]):
    yy = 2100000 + j * 1150000
    tb(s, x, yy, 3500000, 500000, big, size=26, font=DISPLAY, bold=True, color=colr)
    tb(s, x, yy + 520000, 3500000, 600000, cap, size=12.5, color=BODY, line_spacing=1.3)
notes(s, "Cận 2,2 điểm là cận lỏng: tính trên độ chính xác mẫu (chọn sau khi chạy) và không tính nhiễu "
         "giữa các lần train (chạy lặp cùng cấu hình lệch 3,2 điểm). 'lr càng cao càng tụt' mới rõ ở 1 seed.")

# =========================================================== 5 result 2
s = new()
header(s, num(), "KẾT QUẢ 2", "Sửa máy chấm hay bỏ máy chấm: không khác biệt rõ",
       sub="pass@1 ở vòng 2 (%), lr 5e-4. Model gốc: 33,3 (seed 1) và 31,3 (seed 2).")
cols = [(L, 4200000, "CÁCH CHỌN DỮ LIỆU HỌC"), (L + 4300000, 1500000, "SEED 1"),
        (L + 5900000, 1500000, "SEED 2"), (L + 7500000, 3100000, "ĐỌC")]
rows = [
    ("Máy chấm gốc", "23,3", "27,3", "mốc"),
    ("Máy chấm đã vá \\dfrac", "28,7", "20,0", ""),
    ("Không lọc, học tất cả", "27,3", "22,7", ""),
    ("Học lời giải mẫu của người", "15,3", "10,0", ""),
]
end = table(s, 2100000, cols, rows, rowh=480000, rsize=14,
            pills={(1, 3): (GREY, "đổi chiều theo seed"), (2, 3): (GREY, "đổi chiều theo seed"),
                   (3, 3): (CRIMSON, "tụt mạnh nhất")})
takeaway(s, end + 300000,
         "Bản vá \\dfrac chỉ đổi 0–4 bài trong tập học, quá nhỏ để đo ra tác dụng.\n"
         "Bài học: đếm tần suất lỗi trước khi xây thí nghiệm.", height=820000)
notes(s, "Bỏ lọc train gấp 3–4 lần số bước nên cũng không phải đối chứng sạch. Học lời giải mẫu: "
         "model chuyển hẳn sang kiểu viết của lời giải mẫu và tụt mạnh.")

# =========================================================== 6 finding
s = new()
header(s, num(), "PHÁT HIỆN", "Máy chấm loại nhầm khoảng 1/6 lời giải đúng",
       sub="Nguyên nhân: đáp án gốc lưu không có \\boxed{}, model lại viết \\boxed{}.")
s.shapes.add_picture(f"{FIG}/final_verifier.png", Emu(L - 100000), Emu(2000000), width=Emu(6300000))
x = L + 6500000
tb(s, x, 2100000, 4000000, 700000, "15,5–18,4%", size=34, font=DISPLAY, bold=True, color=CRIMSON)
tb(s, x, 2800000, 4000000, 400000, "lời giải đúng bị chấm sai, ở mọi vòng", size=13, color=BODY)
tb(s, x, 3450000, 4000000, 1500000,
   "Ví dụ: gold \\frac43,\nmodel viết \\boxed{\\frac{4}{3}} → SAI.\n\n"
   "Chấm lại không có lỗi này:\nmodel vẫn tụt, kết luận giữ nguyên.",
   size=13.5, color=BODY, line_spacing=1.4)
pill(s, x, 5500000, "XEM DEMO →", fill=CRIMSON, width=2200000)
notes(s, "Lỗi có trong mọi thí nghiệm, cả hai nhánh, nên không làm sai phép so sánh, nhưng kéo pass@1 "
         "tuyệt đối thấp 4,7–8,0 điểm. Sửa lỗi này sẽ làm tập học lớn thêm ~1/5 (440 → 542).")

# =========================================================== 7 demo
s = new()
bg(s, DARK)
tb(s, L, 600000, W, 300000, "DEMO", size=11, bold=True, color=RGBColor(0xE0, 0x7A, 0x82))
tb(s, L, 1000000, W, 700000, "Xem máy chấm loại nhầm lời giải đúng", size=30, font=DISPLAY,
   bold=True, color=WHITE)
for i, (h, d) in enumerate([
    ("1. Ví dụ tay", "cùng đáp án 4/3: máy chấm gốc SAI, bản vá ĐÚNG"),
    ("2. Ví dụ thật", "3 lời giải thật của model bị loại nhầm"),
    ("3. Bảng tổng", "15,5–18,4% trên 500 đề, mọi vòng"),
    ("4. Chấm trực tiếp", "chấm lại lời giải ngẫu nhiên ngay trên máy"),
]):
    y = 2100000 + i * 720000
    tb(s, L, y, 3000000, 330000, h, size=15, bold=True, color=WHITE)
    tb(s, L + 3100000, y + 20000, 7400000, 400000, d, size=14, color=DARKMUTED)
panel(s, L - 120000, 5200000, W + 240000, 620000, fill=RGBColor(0x2A, 0x2A, 0x30))
tb(s, L + 120000, 5370000, W - 240000, 330000,
   ".venv/bin/python 25-10-2026/demo_verifier.py --live 200", size=15,
   font="Menlo", color=RGBColor(0x7F, 0xD8, 0xB4))
notes(s, "Chạy ở thư mục gốc repo, chỉ cần CPU. Nếu lỗi: mở 25-10-2026/demo_output.txt.")

# =========================================================== 8 answer
s = new()
header(s, num(), "KẾT LUẬN", "Trả lời câu hỏi đề tài")
for i, (q, verdict, colr, d) in enumerate([
    ("Model có giỏi toán hơn không?", "KHÔNG THẤY", CRIMSON,
     "Ở cả 4 learning rate, không run nào tăng chắc chắn. Learning rate cao thì còn tụt."),
    ("Có học cách viết của máy chấm không?", "CHƯA RÕ", GREY,
     "Dấu hiệu chốt trước cần pass@1 tăng, mà pass@1 không tăng, nên không kết luận được."),
]):
    y = 1650000 + i * 1800000
    panel(s, L - 120000, y, W + 240000, 1600000)
    tb(s, L + 120000, y + 200000, 7000000, 400000, q, size=18, font=DISPLAY, bold=True, color=INK)
    pill(s, R - 2200000, y + 190000, verdict, fill=colr, width=2000000, size=11)
    tb(s, L + 120000, y + 780000, W - 300000, 700000, d, size=14, color=BODY, line_spacing=1.4)
tb(s, L, 5400000, W, 600000,
   "Ở quy mô 1.5B, LoRA, một máy chấm luật: vòng lặp tự học không cho thấy tiến bộ.",
   size=14, font=DISPLAY, color=INK)
notes(s, "Điểm yếu tự nhận: luật đọc kết quả chỉ một chiều, nhóm nhận ra sau khi chạy.")

# =========================================================== 9 related work
s = new()
header(s, num(), "SO SÁNH", "Kết quả khớp với các nghiên cứu kiểm chứng gần đây",
       sub="Mục 2 (Related Work) của paper.")
cols = [(L, 3300000, "BÀI"), (L + 3400000, 4600000, "HỌ TÌM THẤY"),
        (L + 8100000, W - 8100000, "SO VỚI NHÓM")]
rows = [
    ("STaR (NeurIPS 2022)", "Đề xuất vòng sinh – lọc – học lại", "Khác"),
    ("ReST-EM (DeepMind)", "Có tiến bộ, nhưng giảm dần sau vòng đầu; model lớn", "Khác"),
    ("Yue và cs. (NeurIPS 2025)", "RL tăng pass@1; pass@k lớn thì model gốc thắng", "Giống"),
    ("Phantom Gains (2026)", "Có đối chứng thì nhiều tiến bộ hoá ra là ảo", "Giống"),
    ("TinyV (ICML 2025)", "Máy chấm luật loại nhầm nhiều lời giải đúng", "Cùng hiện tượng"),
]
bottom = table(s, 1950000, cols, rows, rowh=470000, rsize=12.5,
               pills={(0, 2): (GREY, "KHÁC"), (1, 2): (GREY, "KHÁC"),
                      (2, 2): (CRIMSON, "GIỐNG"), (3, 2): (CRIMSON, "GIỐNG"),
                      (4, 2): (CRIMSON, "CÙNG HIỆN TƯỢNG")})
takeaway(s, bottom + 220000,
         "Bài báo cáo tiến bộ dùng model lớn. Ở 1.5B, nhóm thấy như các bài kiểm chứng: "
         "vòng tự học không mở rộng năng lực thật.", height=700000)
notes(s, "Tra arXiv 24/10/2026: STaR 2203.14465, ReST-EM 2312.06585, Yue 2504.13837, Phantom Gains 2608.20290, "
         "TinyV 2505.14625. Phantom Gains là bài gần nhóm nhất (paper mục 2). "
         "Chỉ trích số TinyV: >38% false negative, tăng tới 10%.")

# =========================================================== 10 limits + next
s = new()
header(s, num(), "GIỚI HẠN & TIẾP THEO", "Chưa nói được gì, và nên làm gì tiếp")
tb(s, L, 1650000, 5000000, 300000, "GIỚI HẠN", size=11, bold=True, color=MUTED)
tb(s, L + 5500000, 1650000, 5000000, 300000, "VIỆC TIẾP THEO", size=11, bold=True, color=CRIMSON)
lims = ["Ít seed (2–3 mỗi cấu hình)", "Một model, một máy chấm, không phải RL",
        "Một số thước đo thêm sau khi chạy", "Lỗi \\boxed chưa được vá khi train"]
nxt = ["Train lại với bản vá \\boxed, nhiều seed", "Tách nguyên nhân cú sụp thiết kế gộp",
       "Đối chứng dương để biết đo được hiệu ứng cỡ nào", "Giới hạn token lớn hơn 512"]
for i, (a, b) in enumerate(zip(lims, nxt)):
    y = 2100000 + i * 800000
    panel(s, L - 120000, y, 5100000, 640000)
    tb(s, L + 80000, y + 170000, 4800000, 330000, a, size=14, color=BODY)
    panel(s, L + 5400000, y, 5100000, 640000)
    tb(s, L + 5600000, y + 170000, 4800000, 330000, b, size=14, color=INK)
notes(s, "Bản vá \\boxed là thí nghiệm máy chấm có tác động thật: đổi ~1/5 tập học, gấp 34–49 lần bản vá "
         "\\dfrac. Cần cố định số bước train khi so sánh.")

# =========================================================== 11 thanks
s = new()
bg(s, DARK)
tb(s, L, 2300000, W, 900000, "Cảm ơn thầy đã lắng nghe", size=38, font=DISPLAY,
   bold=True, color=WHITE)
tb(s, L, 3400000, W, 400000, "Nhóm sẵn sàng trả lời câu hỏi.", size=16, color=DARKMUTED)
rule(s, L, 4300000, 2400000, color=CRIMSON, pt=2.0)
tb(s, L, 4500000, W, 300000,
   "Paper: 25-10-2026/paper_revised.pdf  ·  Bản slide đầy đủ: 25-10-2026/BaoCaoDayDu_*.pptx",
   size=12, color=DARKMUTED)

prs.save(OUT)
print("saved", OUT, len(prs.slides), "slides")
