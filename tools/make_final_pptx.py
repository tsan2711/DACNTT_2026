"""Final report deck, 25/10/2026 — matches paper_revised.tex after the r3 re-review.

Same design system as make_week13_pptx.py (Georgia display, Helvetica Neue body,
one crimson accent, CVD-safe blue/orange/green data colours). Every number on a
slide comes from paper_revised.tex or experiments/viec3/review_cpu/; the slide
says which table when it matters, so Bi can trace it during Q&A.

    .venv/bin/python tools/make_final_pptx.py
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
OUT = f"{REPO}/BaoCaoCuoiKy_25-10_52300057_52300006.pptx"
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


# =========================================================== title
s = new()
panel(s, 0, 0, SW, 150000, fill=CRIMSON, radius=0)
tb(s, L, 1180000, W, 300000, "ĐỒ ÁN CÔNG NGHỆ THÔNG TIN  ·  BÁO CÁO KẾT QUẢ",
   size=12, bold=True, color=CRIMSON)
tb(s, L, 1700000, 10400000, 1900000,
   "Tự học có làm model nhỏ\ngiỏi toán hơn không?",
   size=42, font=DISPLAY, bold=True, color=INK, line_spacing=1.08)
tb(s, L, 3800000, 9600000, 1000000,
   "Kiểm tra vòng lặp Sinh lời giải → Chấm → Chọn → Huấn luyện (GVT)\n"
   "trên Qwen2.5-1.5B với máy chấm math-verify.",
   size=16, color=BODY, line_spacing=1.4)
rule(s, L, 5150000, 2400000, color=CRIMSON, pt=2.0)
tb(s, L, 5380000, 8000000, 300000,
   "Nguyễn Tấn Sang (52300057)  ·  Trần Duy Anh (52300006)", size=13, bold=True, color=INK)
tb(s, L, 5720000, 6000000, 300000, "25 tháng 10, 2026", size=12, color=MUTED)

# =========================================================== agenda
s = new()
header(s, num(), "NỘI DUNG", "Thứ tự trình bày")
items = [
    ("Câu hỏi và cách đo", "4 thước đo chốt trước khi chạy"),
    ("Máy chấm và lỗi của nó", "chấm sai theo cách viết đáp án"),
    ("Hai thiết kế thí nghiệm", "thiết kế gộp, rồi thiết kế cô lập"),
    ("Kết quả", "không thấy tiến bộ, lr cao thì tụt"),
    ("Đối chứng và lỗi lưu đáp án", "kèm demo chạy trực tiếp"),
    ("Trả lời câu hỏi, giới hạn, việc tiếp theo", ""),
]
y = 2100000
for i, (h, d) in enumerate(items, 1):
    tb(s, L, y + 20000, 500000, 330000, f"{i:02d}", size=13, font=DISPLAY,
       bold=True, color=CRIMSON)
    tb(s, L + 700000, y, 4600000, 330000, h, size=14.5, bold=True, color=INK)
    tb(s, L + 5400000, y + 20000, 5100000, 330000, d, size=13, color=MUTED)
    y += 560000
    if i < len(items):
        rule(s, L + 700000, y - 130000, W - 700000)

# =========================================================== question + loop
s = new()
header(s, num(), "ĐỀ TÀI", "Model tự làm bài, tự chọn bài đúng để học lại")
for i, (k, h, d) in enumerate([
    ("1", "Sinh", "Model làm mỗi đề k lần\n(k = 4 hoặc 8), nhiệt độ 0,8."),
    ("2", "Chấm", "math-verify so đáp án cuối\nvới đáp án gốc. Không đọc lời giải."),
    ("3", "Chọn + học", "Giữ lời giải được nhận,\nfine-tune LoRA từ model gốc."),
]):
    x = L + i * 3560000
    panel(s, x, 1700000, 3300000, 1700000)
    tb(s, x + 240000, 1860000, 400000, 330000, k, size=17, font=DISPLAY, bold=True, color=CRIMSON)
    tb(s, x + 240000, 2260000, 2900000, 330000, h, size=15, bold=True, color=INK)
    tb(s, x + 240000, 2620000, 2900000, 600000, d, size=12, color=BODY, line_spacing=1.3)
tb(s, L, 3600000, W, 300000, "Lặp lại 3–5 vòng. Các bài STaR, ReST, ReST-EM, RFT đều dùng vòng này.",
   size=12.5, color=MUTED)
tb(s, L, 4000000, W, 300000, "CÂU HỎI CỦA ĐỀ TÀI", size=11, bold=True, color=MUTED)
takeaway(s, 4350000,
         "Sau nhiều vòng, model giỏi toán hơn thật,\n"
         "hay chỉ học cách viết mà máy chấm chịu nhận?", height=1000000)
notes(s, "Máy chấm chỉ nhìn đáp án cuối. Tín hiệu huấn luyện vì vậy là 'chuỗi cuối có được nhận "
         "không', không phải 'các bước có đúng không'. Đó là lý do câu hỏi có hai nhánh.")

# =========================================================== measures
s = new()
header(s, num(), "CÁCH ĐO", "Bốn thước đo chốt trước khi chạy",
       sub="Tất cả đo trên 150 đề thi riêng mà model không bao giờ được học.")
cols = [(L, 2600000, "THƯỚC ĐO"), (L + 2700000, 7800000, "NGHĨA LÀ")]
rows = [
    ("pass@1", "Lời giải đầu tiên có đúng không"),
    ("pass@k", "Trong k lần làm, có ít nhất 1 lần đúng không (đo khả năng, không đo độ ổn định)"),
    ("Kiểu chữ", "Tỉ lệ lời giải có \\boxed, \\dfrac... (dấu hiệu bắt chước cách viết)"),
    ("Thêm / mất đề", "Đề mới giải được, và đề trước giải được nay mất"),
]
end = table(s, 2150000, cols, rows, rowh=460000, rsize=13)
tb(s, L, end + 280000, W, 300000, "LUẬT ĐỌC KẾT QUẢ (CHỐT TRƯỚC)", size=11, bold=True, color=MUTED)
tb(s, L, end + 620000, W, 700000,
   "\"Học chữ máy chấm\" chỉ khi đủ cả ba: pass@1 tăng, pass@k đứng yên, kiểu chữ tụ về một dạng.\n"
   "Thiếu một mảnh thì chỉ được nói \"chưa xác định\".",
   size=13.5, color=BODY, line_spacing=1.35)
notes(s, "Câu hỏi tự kiểm: vì sao pass@1 tăng thôi thì chưa nói được model giỏi hơn? Vì có thể "
         "chỉ là ổn định hơn ở những đề vốn đã làm được; pass@k mới cho biết có giải thêm được đề mới không.")

# =========================================================== verifier
s = new()
header(s, num(), "MÁY CHẤM", "math-verify từ chối một số đáp án đúng",
       sub="Lỗi phụ thuộc vào cách viết, không phải ngẫu nhiên. Có hai loại trong pipeline của nhóm.")
for i, (tag, colr, h, d, big) in enumerate([
    ("LỖI 1 · \\dfrac", BLUE, "Viết \\dfrac thay vì \\frac",
     "Đo trước khi chạy. Rất hiếm trong output\nthật: bản vá chỉ đổi 0–4 bài trong tập train.", "< 1%"),
    ("LỖI 2 · gold không có \\boxed", CRIMSON, "Đáp án gốc lưu trơn, model viết \\boxed{}",
     "Đo sau khi chạy xong, trên chính output\ncủa vòng lặp. Có mặt trong mọi thí nghiệm.", "15,5–18,4%"),
]):
    x = L + i * 5420000
    panel(s, x - 120000, 2150000, 5170000, 3000000)
    tb(s, x + 120000, 2330000, 4700000, 300000, tag, size=11, bold=True, color=colr)
    tb(s, x + 120000, 2720000, 4700000, 700000, big, size=40, font=DISPLAY, bold=True, color=colr)
    tb(s, x + 120000, 3550000, 4700000, 330000, h, size=14, bold=True, color=INK)
    tb(s, x + 120000, 3980000, 4700000, 800000, d, size=12.5, color=BODY, line_spacing=1.35)
tb(s, L, 5450000, W, 600000,
   "Lỗi 2 nghĩa là: cứ khoảng 6 lời giải đúng thì 1 lời giải bị loại khỏi tập train. Ví dụ gold \\frac43, "
   "model viết \\boxed{\\frac{4}{3}} → bị chấm sai.",
   size=12.5, color=MUTED, line_spacing=1.35)
notes(s, "Số 15,5–18,4% là trên cả 500 đề, Run A seed 1, seed 2 và lr 1e-5 seed 0, mọi vòng. "
         "Giả định verifier đã vá không nhận nhầm đáp án sai — chưa đo, nên là cận trên. "
         "Kiểm tay 30 cặp lật: 29 cặp cùng giá trị, chỉ khác cách viết.")

# =========================================================== designs
s = new()
header(s, num(), "THIẾT KẾ", "Hai thiết kế thí nghiệm")
cols = [(L, 1900000, ""), (L + 2000000, 4200000, "P · GỘP (làm trước)"),
        (L + 6300000, 4300000, "I · CÔ LẬP (làm lại)")]
rows = [
    ("Dữ liệu", "GSM8K + MATH-500 trộn chung", "Mỗi bộ chạy riêng"),
    ("Chấm điểm ở đâu", "Trên chính tập chọn bài train", "150 đề thi tách riêng"),
    ("Số vòng, k", "5 vòng, k = 8", "3–5 vòng, k = 4 hoặc 8"),
    ("Learning rate", "1e-5", "1e-5, 1e-4, 2e-4, 5e-4"),
    ("Seed", "1 lần chạy", "2–3 seed mỗi cấu hình"),
    ("Đối chứng", "không có", "vá verifier, bỏ lọc, train trên gold"),
]
end = table(s, 1650000, cols, rows, rowh=440000, rsize=12.5,
            emph=lambda i: i == 1)
takeaway(s, end + 300000,
         "Thiết kế P chấm trên tập dùng để chọn bài và huấn luyện lâu hơn ~4,5 lần mỗi vòng,\n"
         "nên nhóm làm lại bằng thiết kế I để có số đo sạch.", height=820000)

# =========================================================== design P collapse
s = new()
header(s, num(), "KẾT QUẢ 1", "Thiết kế gộp tụt mạnh, nhưng không lặp lại được")
s.shapes.add_picture(f"{FIG}/deck_collapse.png", Emu(L - 100000), Emu(1550000), width=Emu(7300000))
x = L + 7400000
tb(s, x, 1700000, 3200000, 300000, "1.5B, THIẾT KẾ P", size=11, bold=True, color=MUTED)
tb(s, x, 2050000, 3200000, 700000, "50,0 → 18,6%", size=30, font=DISPLAY, bold=True, color=ORANGE)
tb(s, x, 2750000, 3200000, 300000, "pass@1 sau 5 vòng (−31,4 điểm)", size=12, color=BODY)
tb(s, x, 3350000, 3200000, 300000, "THIẾT KẾ I, CÙNG LR 1e-5", size=11, bold=True, color=MUTED)
tb(s, x, 3700000, 3200000, 1400000,
   "pass@8 đi ngang, lệch không quá 4 điểm.\nMATH-500: pass@1 giảm 2,7–4,0 điểm,\n"
   "khoảng tin cậy đều chứa 0.\nGSM8K (1 lần): pass@1 giảm 12,7 điểm.",
   size=12.5, color=BODY, line_spacing=1.4)
takeaway(s, 5500000,
         "Cú sụp ở thiết kế P chưa rõ nguyên nhân: khác cả cách chấm lẫn lượng huấn luyện.",
         height=560000)
notes(s, "Không được nói 'self-training gây sụp đổ'. Thiết kế P vừa chấm trên tập chọn, vừa "
         "train ~4,5 lần nhiều bước hơn. Hai yếu tố đó chưa tách được.")

# =========================================================== learning rate
s = new()
header(s, num(), "KẾT QUẢ 2", "Không lr nào làm model giỏi lên; lr cao thì tụt",
       sub="Run A, MATH-500, 3 vòng, k = 4. Ở lr 1e-5, model thay đổi rất ít nên nhóm thử lr cao hơn.")
s.shapes.add_picture(f"{FIG}/final_lr.png", Emu(L - 100000), Emu(2000000), width=Emu(6900000))
x = L + 7100000
for j, (big, colr, cap) in enumerate([
    ("≤ +2,2", INK, "điểm: mức tăng lớn nhất còn\nphù hợp dữ liệu (độ chính xác mẫu)"),
    ("4 / 4", ORANGE, "run ở lr 5e-4 đều giảm\nđộ chính xác mẫu, khoảng tin cậy loại 0"),
    ("1 seed", GREY, "mới thấy rõ \"lr càng cao tụt\ncàng nhiều\" (seed 2 gần như phẳng)"),
]):
    yy = 2100000 + j * 1150000
    tb(s, x, yy, 3500000, 500000, big, size=26, font=DISPLAY, bold=True, color=colr)
    tb(s, x, yy + 520000, 3500000, 600000, cap, size=12, color=BODY, line_spacing=1.3)
notes(s, "Độ chính xác mẫu = trung bình đúng trên cả k lời giải; ít nhiễu hơn pass@1. Chọn làm thước "
         "đo chính SAU khi chạy, nên con số 2,2 là post hoc. Khoảng bootstrap không tính nhiễu giữa các "
         "lần train: chạy lặp cùng cấu hình đã lệch 3,2 điểm. Vì vậy cận 2,2 là lỏng.")

# =========================================================== controls
s = new()
header(s, num(), "ĐỐI CHỨNG", "Vá verifier hay bỏ lọc đều không tạo khác biệt nhất quán",
       sub="lr 5e-4, MATH-500, pass@1 ở vòng 2 (%). Vòng 0 = model gốc: 33,3 (seed 1), 31,3 (seed 2).")
cols = [(L, 3600000, "RUN"), (L + 3700000, 1500000, "SEED 1"),
        (L + 5300000, 1500000, "SEED 2"), (L + 6900000, 3700000, "ĐỌC")]
rows = [
    ("A · verifier gốc", "23,3", "27,3", "mốc so sánh"),
    ("B · vá \\dfrac", "28,7", "20,0", "đổi dấu theo seed"),
    ("Bỏ lọc (học mọi lời giải)", "27,3", "22,7", "đổi dấu, train gấp 3–4 lần"),
    ("Train trên lời giải gold", "15,3", "10,0", "tụt mạnh nhất"),
]
end = table(s, 2100000, cols, rows, rowh=470000, rsize=13,
            pills={(1, 3): (GREY, "đổi dấu theo seed"), (3, 3): (CRIMSON, "tụt mạnh nhất")})
takeaway(s, end + 300000,
         "Bài học thiết kế: bản vá \\dfrac chỉ đổi 0–4 bài train, nên không thể đo ra tác dụng.\n"
         "Đếm tần suất lỗi trước khi chạy sẽ thấy điều này ngay.", height=820000)
notes(s, "A và B cùng seed bắt đầu từ gần như cùng tập train, vậy mà cuối cùng lệch 5–7 điểm. "
         "Đó là nhiễu quỹ đạo huấn luyện, không phải tác dụng của bản vá.")

# =========================================================== gold boxed defect
s = new()
header(s, num(), "PHÁT HIỆN", "Lỗi lưu đáp án gốc loại ~1/6 lời giải đúng",
       sub="Run A, lr 5e-4, seed 1. Chấm lại output đã lưu bằng verifier đã vá (bọc gold vào \\boxed{}).")
s.shapes.add_picture(f"{FIG}/final_verifier.png", Emu(L - 100000), Emu(2000000), width=Emu(6300000))
x = L + 6500000
tb(s, x, 2150000, 4000000, 1500000,
   "Nếu sửa lỗi này, tập train vòng 0 lớn thêm\nkhoảng 1/5 (440 → 542 bài).\n\n"
   "Gấp 34–49 lần tác động của bản vá \\dfrac.",
   size=13.5, color=BODY, line_spacing=1.4)
tb(s, x, 3900000, 4000000, 300000, "ẢNH HƯỞNG TỚI KẾT LUẬN", size=11, bold=True, color=MUTED)
tb(s, x, 4250000, 4000000, 1300000,
   "pass@1 tuyệt đối bị kéo thấp 4,7–8,0 điểm.\nChấm lại không có lỗi này: độ chính xác mẫu\n"
   "vẫn giảm ở cả 5 run đã chấm lại.",
   size=13, color=BODY, line_spacing=1.4)
pill(s, x, 5650000, "DEMO: tools/demo_verifier.py", fill=CRIMSON, width=3400000)
notes(s, "Lỗi này có trong cả hai nhánh mọi thí nghiệm, nên không làm sai phép so sánh, nhưng làm "
         "thấp số tuyệt đối. Nhóm chưa chạy thí nghiệm huấn luyện với bản vá này.")

# =========================================================== demo
s = new()
bg(s, DARK)
tb(s, L, 600000, W, 300000, "DEMO", size=11, bold=True, color=RGBColor(0xE0, 0x7A, 0x82))
tb(s, L, 1000000, W, 700000, "Máy chấm loại nhầm lời giải đúng", size=30, font=DISPLAY,
   bold=True, color=WHITE)
for i, (h, d) in enumerate([
    ("1. Ví dụ tay", "gold \\frac43, model viết \\boxed{\\frac{4}{3}}: gốc SAI, đã vá ĐÚNG"),
    ("2. Ví dụ thật", "3 lời giải của model ở vòng 0, đọc đề và đáp án"),
    ("3. Bảng tổng", "15,5–18,4% trên 500 đề, mọi vòng, 3 run"),
    ("4. Chấm trực tiếp", "chấm lại 200 lời giải ngẫu nhiên ngay trên máy (~10 giây)"),
]):
    y = 2100000 + i * 720000
    tb(s, L, y, 3000000, 330000, h, size=15, bold=True, color=WHITE)
    tb(s, L + 3100000, y + 20000, 7400000, 400000, d, size=14, color=DARKMUTED)
panel(s, L - 120000, 5200000, W + 240000, 620000, fill=RGBColor(0x2A, 0x2A, 0x30))
tb(s, L + 120000, 5370000, W - 240000, 330000,
   ".venv/bin/python tools/demo_verifier.py --live 200", size=15,
   font="Menlo", color=RGBColor(0x7F, 0xD8, 0xB4))
notes(s, "Chỉ cần CPU. Nếu máy lỗi, mở ảnh chụp dự phòng. Chạy ở thư mục gốc repo.")

# =========================================================== answer
s = new()
header(s, num(), "TRẢ LỜI", "Câu trả lời cho câu hỏi đề tài")
for i, (q, verdict, colr, d) in enumerate([
    ("Model có giỏi toán hơn không?", "KHÔNG THẤY", CRIMSON,
     "Không run nào tăng pass@1 hay pass@k với khoảng tin cậy loại 0, ở cả 4 lr. "
     "Độ chính xác mẫu loại trừ mức tăng trên ~2,2 điểm (cận lỏng)."),
    ("Có học chữ máy chấm không?", "CHƯA XÁC ĐỊNH", GREY,
     "Luật chốt trước chỉ bật khi pass@1 tăng, mà pass@1 không tăng, nên luật im lặng không chứng "
     "minh gì. Tỉ lệ \\boxed giảm theo kiểu mà bắt chước hay trôi dạt đều giải thích được."),
]):
    y = 1650000 + i * 1950000
    panel(s, L - 120000, y, W + 240000, 1750000)
    tb(s, L + 120000, y + 200000, 6500000, 400000, q, size=17, font=DISPLAY, bold=True, color=INK)
    pill(s, R - 2200000, y + 190000, verdict, fill=colr, width=2000000, size=11)
    tb(s, L + 120000, y + 750000, W - 300000, 900000, d, size=13, color=BODY, line_spacing=1.4)
tb(s, L, 5650000, W, 600000,
   "Thấy thêm (post hoc, rõ nhất ở lr 5e-4): model kém chính xác hơn trên chính những lời giải nó viết xong, "
   "và ở một seed có nhiều lời giải chạm giới hạn 512 token hơn.",
   size=12.5, color=MUTED, line_spacing=1.35)
notes(s, "Điểm yếu tự nhận: luật đọc kết quả là một chiều. Nhóm nhận ra điều này sau khi chạy.")

# =========================================================== limitations
s = new()
header(s, num(), "GIỚI HẠN", "Những gì kết quả này chưa nói được")
lims = [
    ("Ít seed", "2–3 seed mỗi cấu hình; chạy lặp cùng cấu hình đã lệch 3,2 điểm."),
    ("Thước đo chọn sau", "Độ chính xác mẫu và các phép đo chạm-giới-hạn được thêm sau khi chạy."),
    ("Cận trên 18,4%", "Chưa đo verifier đã vá có nhận nhầm đáp án sai không."),
    ("Một model, một verifier", "Qwen2.5-1.5B, LoRA SFT, math-verify; không phải RL."),
    ("Thiết kế P", "Cú sụp chưa tách được giữa cách chấm và lượng huấn luyện."),
]
y = 1750000
for i, (h, d) in enumerate(lims):
    tb(s, L, y, 3300000, 330000, h, size=14.5, bold=True, color=INK)
    tb(s, L + 3400000, y + 20000, 7100000, 400000, d, size=13, color=BODY)
    y += 700000
    if i < len(lims) - 1:
        rule(s, L, y - 180000, W)

# =========================================================== next steps
s = new()
header(s, num(), "VIỆC TIẾP THEO", "Nếu tiếp tục đề tài")
nxt = [
    ("Chạy với bản vá \\boxed", "Thí nghiệm verifier có tác động thật (đổi ~1/5 tập train); cần nhiều seed, giữ cố định số bước."),
    ("Tách nguyên nhân thiết kế P", "Chạy gộp nhưng chấm trên đề thi riêng; chạy cô lập với cùng số bước."),
    ("Đối chứng dương", "Cố tình làm verifier lệch với một kiểu viết phổ biến, để biết thiết kế đo được hiệu ứng cỡ nào."),
    ("Giới hạn token", "Thử giới hạn lớn hơn 512: model gốc đã chạm giới hạn ở 41–48% lời giải."),
]
y = 1750000
for i, (h, d) in enumerate(nxt, 1):
    tb(s, L, y + 20000, 500000, 330000, f"{i:02d}", size=13, font=DISPLAY, bold=True, color=CRIMSON)
    tb(s, L + 700000, y, W - 700000, 330000, h, size=14.5, bold=True, color=INK)
    tb(s, L + 700000, y + 400000, W - 700000, 400000, d, size=12.5, color=BODY)
    y += 950000

# =========================================================== thanks
s = new()
bg(s, DARK)
tb(s, L, 2300000, W, 900000, "Cảm ơn thầy đã lắng nghe", size=38, font=DISPLAY,
   bold=True, color=WHITE)
tb(s, L, 3400000, W, 400000, "Nhóm sẵn sàng trả lời câu hỏi.", size=16, color=DARKMUTED)
rule(s, L, 4300000, 2400000, color=CRIMSON, pt=2.0)
tb(s, L, 4500000, W, 300000,
   "Mã nguồn, dữ liệu, paper: repo DACNTT_2026 · paper: papers/latex/paper_revised.pdf",
   size=12, color=DARKMUTED)

prs.save(OUT)
print("saved", OUT, len(prs.slides), "slides")
