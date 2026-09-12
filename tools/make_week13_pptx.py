"""Progress deck, weeks 1-3 — one continuous explanation.

Covers the project from the start, because the audience has to follow the
reversal and cannot do that without the setup: what the topic is -> what the
grader gets wrong -> week 1's first run -> week 2's bigger run -> the flaw in
how it was measured -> the corrected experiments -> the refutation -> why.

Wording is deliberately plain. This is a student talking to their advisor,
not a paper abstract, so: short sentences, no aphorisms, no em-dash
parallelism, and every number said out loud in words the listener can hold.

Design system (rebuilt 2026-09-11 for a cleaner, more current look):
  type    Georgia for display, Helvetica Neue for body and data. Both exist
          on macOS and Windows, and Helvetica Neue falls back to Arial almost
          identically, so the file survives being emailed.
  colour  near-black ink on white, one crimson accent, and the CVD-safe data
          trio already validated for the paper figure (blue/orange/green), so
          the deck and the paper agree visually.
  layout  tinted panels instead of hairline-ruled tables, coloured verdict
          pills, hero numerals, two real charts, and one inverted slide at the
          turning point.
"""

from pptx import Presentation
from pptx.util import Emu, Pt
from pptx.dml.color import RGBColor
from pptx.enum.text import PP_ALIGN, MSO_ANCHOR
from pptx.enum.shapes import MSO_CONNECTOR, MSO_SHAPE

REPO = "/Users/tsangcuteso1/Documents/GitHub/DACNTT_2026"
OUT = f"{REPO}/BaoCaoTienDo_Tuan1-3_52300057_52300006.pptx"
FIG = f"{REPO}/papers/figures"

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

DISPLAY = "Georgia"
SANS = "Helvetica Neue"

SW, SH = 12191695, 6858000
L = 800100                       # left margin
W = 10591495                     # content width
R = L + W

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
    sh = slide.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, Emu(left), Emu(top),
                                Emu(width), Emu(height))
    sh.fill.solid()
    sh.fill.fore_color.rgb = fill
    sh.line.fill.background()
    sh.shadow.inherit = False
    try:
        sh.adjustments[0] = 0.5
    except Exception:
        pass
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
    tb(slide, L, 790000, W, 620000, title, size=29, font=DISPLAY, bold=True,
       color=INK, line_spacing=1.05)
    if sub:
        tb(slide, L, 1520000, W, 420000, sub, size=13, color=MUTED, line_spacing=1.25)


def table(slide, top, cols, rows, *, rowh=430000, hsize=11, rsize=12,
          pad=170000, emph=None, pills=None):
    """Tinted panel behind the rows; header row sits above it."""
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


def new():
    return prs.slides.add_slide(BLANK)


# =========================================================== 1 · title
s = new()
panel(s, 0, 0, SW, 150000, fill=CRIMSON, radius=0)
tb(s, L, 1180000, W, 300000, "BÁO CÁO TIẾN ĐỘ  ·  TUẦN 1 ĐẾN TUẦN 3",
   size=12, bold=True, color=CRIMSON)
tb(s, L, 1700000, 10200000, 1900000,
   "Thí nghiệm đối chứng cho thấy\ngiả thuyết ban đầu không đúng",
   size=40, font=DISPLAY, bold=True, color=INK, line_spacing=1.08)
tb(s, L, 3850000, 9200000, 1000000,
   "Ba tuần đầu, kết quả thí nghiệm tưởng như đã xác nhận giả thuyết. Sau đó phát hiện thiết kế đo\n"
   "có lỗi. Đo lại cho đúng thì kết quả ngược lại."
   ,
   size=15, color=BODY, line_spacing=1.4)
rule(s, L, 5250000, 2400000, color=CRIMSON, pt=2.0)
tb(s, L, 5480000, 6000000, 300000, "Nguyễn Tấn Sang", size=13, bold=True, color=INK)
tb(s, L, 5820000, 6000000, 300000, "12 tháng 9, 2026", size=12, color=MUTED)

# =========================================================== 2 · agenda
s = new()
header(s, 1, "NỘI DUNG", "Thứ tự trình bày")
items = [
    ("Bối cảnh đề tài", "và quy trình một vòng thí nghiệm"),
    ("Lỗi của máy chấm", "đo được trước khi chạy thí nghiệm"),
    ("Kết quả tuần 1 và tuần 2", "cả hai model đều tụt điểm"),
    ("Vấn đề trong thiết kế", "hai lỗi khiến số liệu không dùng được"),
    ("Thí nghiệm làm lại", "năm lần chạy mới, kết quả ngược lại"),
    ("Nguyên nhân và đề tài tiếp theo", "hướng nghiên cứu sau khi điều chỉnh"),
]
y = 2150000
for i, (h, d) in enumerate(items, 1):
    tb(s, L, y + 20000, 500000, 330000, f"{i:02d}", size=13, font=DISPLAY,
       bold=True, color=CRIMSON)
    tb(s, L + 700000, y, 4200000, 330000, h, size=14.5, bold=True, color=INK)
    tb(s, L + 4300000, y + 20000, 6200000, 330000, d, size=13, color=MUTED)
    y += 560000
    if i < len(items):
        rule(s, L + 700000, y - 130000, W - 700000)

# =========================================================== 3 · what is the topic
s = new()
header(s, 2, "ĐỀ TÀI", "Cho model tự học, không cần người dạy")
tb(s, L, 1700000, W, 900000,
   "Muốn model giải toán giỏi hơn thì bình thường phải có người soạn lời giải mẫu cho nó học.\n"
   "Việc đó rất tốn công. Nên người ta nghĩ ra cách cho model tự làm bài, rồi dùng một máy chấm\n"
   "tự động chọn ra bài nào nó làm đúng, lấy đúng những bài đó dạy lại cho nó. Làm đi làm lại\n"
   "nhiều vòng. Cách này tên là tự học (self-training).",
   size=14, color=BODY, line_spacing=1.45)
panel(s, L - 120000, 3300000, W + 240000, 900000)
tb(s, L + 120000, 3480000, W - 240000, 600000,
   "Toàn bộ cách làm này dựa trên một niềm tin: máy chấm phải chấm đúng. Nếu máy chấm sai,\n"
   "model sẽ học nhầm, mà không ai biết.",
   size=14, font=DISPLAY, color=INK, line_spacing=1.4)
tb(s, L, 4500000, W, 300000, "CÂU HỎI CỦA ĐỀ TÀI", size=11, bold=True, color=MUTED)
tb(s, L, 4870000, W, 700000,
   "Máy chấm có sai, và sai theo một quy luật cố định.\nSau nhiều vòng tự học, model có bị dở đi không?",
   size=16, font=DISPLAY, bold=True, color=CRIMSON, line_spacing=1.35)

# =========================================================== 4 · the loop
s = new()
header(s, 3, "MỘT VÒNG CHẠY", "Ba bước, lặp lại năm lần")
for i, (n, h, d) in enumerate([
    ("1", "Làm bài", "Model tự làm mỗi đề 8 lần,\nra 8 lời giải khác nhau."),
    ("2", "Chấm", "Máy chấm so đáp án cuối với\nđáp án trong sách. Sai thì bỏ."),
    ("3", "Học lại", "Lấy đúng những bài vừa được\nchấm đúng, dạy lại cho model."),
]):
    x = L + i * 3560000
    panel(s, x, 1900000, 3300000, 1620000)
    tb(s, x + 240000, 2080000, 400000, 330000, n, size=17, font=DISPLAY,
       bold=True, color=CRIMSON)
    tb(s, x + 240000, 2500000, 2900000, 330000, h, size=15, bold=True, color=INK)
    tb(s, x + 240000, 2880000, 2900000, 600000, d, size=12, color=BODY, line_spacing=1.3)
rule(s, L, 3800000, W)
tb(s, L, 3990000, W, 800000,
   "Mỗi vòng dạy lại từ model gốc, chỉ bằng bài của vòng trước. Nên nếu máy chấm bỏ sót một kiểu\n"
   "bài nào đó, vòng sau model càng ít gặp kiểu bài đó. Vòng sau nữa lại càng ít hơn.",
   size=13, color=BODY, line_spacing=1.45)
panel(s, L - 120000, 4950000, W + 240000, 1400000)
tb(s, L + 120000, 5180000, W - 240000, 750000,
   "Hai chỉ số dùng xuyên suốt:\n"
   "pass@1  —  cho model làm 1 lần, đúng bao nhiêu phần trăm số đề.\n"
   "pass@8  —  cho làm 8 lần, chỉ cần 1 lần đúng là tính đúng. Đo xem model còn giải nổi bài không.",
   size=13, color=INK, line_spacing=1.45)

# =========================================================== 5 · the bug (figure)
s = new()
header(s, 4, "MÁY CHẤM SAI Ở ĐÂU", "Cùng một đáp án, viết khác kiểu là bị gạch")
s.shapes.add_picture(f"{FIG}/deck_verifier_bug.png", Emu((SW - 9900000) // 2),
                     Emu(1780000), width=Emu(9900000))
tb(s, L, 4650000, W, 700000,
   "Máy chấm không đọc cách giải. Nó chỉ lấy đáp án cuối rồi so chữ với đáp án trong sách.\n"
   "Hai cách viết trên cho ra cùng một phân số, nhưng nó chỉ nhận một cách.",
   size=13.5, color=BODY, line_spacing=1.45)
panel(s, L - 120000, 5480000, W + 240000, 800000)
tb(s, L + 120000, 5650000, W - 240000, 520000,
   "7,8% là tỉ lệ máy chấm gạch OAN bài model làm ĐÚNG (10/128 bài, kiểm tra tay) — không phải tỉ lệ model làm sai.\n"
   "Trên GSM8K con số này là 0%: máy chấm ở đó không gạch oan bài nào, nên điểm đo được là năng lực thật của model.",
   size=12.5, bold=True, color=INK)

# =========================================================== 6 · week 1
s = new()
header(s, 5, "TUẦN 1", "Lần chạy đầu tiên trên model nhỏ")
tb(s, L, 1700000, W, 400000,
   "Cấu hình: Qwen 0.5B, 500 đề mỗi bộ, 5 vòng, chạy trên GPU của Kaggle.",
   size=13.5, color=BODY)
for i, (lbl, a, b, note) in enumerate([
    ("pass@1", "31,1%", "27,4%", "làm 1 lần đúng"),
    ("pass@8", "60,5%", "54,9%", "cho làm 8 lần"),
]):
    x = L + i * 5400000
    panel(s, x, 2250000, 5190000, 1500000)
    tb(s, x + 260000, 2420000, 2000000, 300000, lbl, size=12, bold=True, color=MUTED)
    tb(s, x + 260000, 2780000, 4700000, 550000, f"{a}  →  {b}",
       size=30, font=DISPLAY, bold=True, color=INK)
    tb(s, x + 260000, 3400000, 4700000, 300000, f"{note}, sau 5 vòng",
       size=12, color=MUTED)
tb(s, L, 4000000, W, 800000,
   "Cả hai chỉ số đều tụt, khớp với giả thuyết: máy chấm gạch nhầm bài đúng, model học thiếu nên\n"
   "dở đi. Nhưng model này nhỏ và mức tụt cũng ít, chưa đủ cơ sở để kết luận.",
   size=13.5, color=BODY, line_spacing=1.45)
panel(s, L - 120000, 5050000, W + 240000, 620000, fill=RGBColor(0xF0, 0xF6, 0xFA))
tb(s, L + 120000, 5240000, W - 240000, 300000,
   "Tuần 2 chạy lại với model to gấp ba, để xem hiện tượng có rõ hơn không.",
   size=12.5, bold=True, color=BLUE)

# =========================================================== 7 · week 2
s = new()
header(s, 6, "TUẦN 2", "Model to gấp ba, tụt mạnh hơn hẳn")
cols = [(L, 3100000, "ĐO TRÊN"), (L + 3300000, 2200000, "PASS@1  VÒNG 0 → 4"),
        (L + 5600000, 2200000, "PASS@8  VÒNG 0 → 4"), (L + 7900000, 2600000, "TỤT BAO NHIÊU")]
rows = [
    ("Qwen 0.5B  (tuần 1)", "31,1% → 27,4%", "60,5% → 54,9%", "5,6 điểm"),
    ("Qwen 1.5B  (tuần 2)", "50,0% → 18,6%", "72,6% → 48,6%", "24,0 điểm"),
    ("1.5B, riêng bộ GSM8K", "69,6% → 26,6%", "91,4% → 65,8%", "25,6 điểm"),
    ("1.5B, riêng bộ MATH-500", "30,4% → 10,6%", "53,8% → 31,4%", "22,4 điểm"),
]
y = table(s, 1950000, cols, rows, emph=lambda i: i == 1)
tb(s, L, y + 300000, W, 500000,
   "Vòng 0 là model gốc chưa học gì. 69,6% trên GSM8K là năng lực thật của nó — 30,4% còn lại nó làm\n"
   "sai thật, máy chấm gạch đúng. Sau 5 vòng chỉ còn 26,6%, và vì máy chấm ở GSM8K không gạch oan,\n"
   "cú tụt này là tụt thật, không phải sai số đo.",
   size=13, color=BODY, line_spacing=1.45)
panel(s, L - 120000, y + 1320000, W + 240000, 830000, fill=RGBColor(0xFD, 0xF3, 0xF3))
tb(s, L + 120000, y + 1480000, W - 240000, 460000,
   "Nhưng có một điểm bất thường: GSM8K lại tụt nhiều nhất.\n"
   "Mà GSM8K chính là bộ máy chấm gần như không gạch nhầm bài nào.",
   size=12.5, bold=True, color=CRIMSON, line_spacing=1.4)

# =========================================================== 8 · the flaw
s = new()
header(s, 7, "VẤN ĐỀ TRONG THIẾT KẾ", "Thiết kế đo có hai lỗi")
tb(s, L, 1620000, W, 300000, "LỖI 1 — hai bộ đề bị gộp chung trong cùng một lần dạy",
   size=11.5, bold=True, color=CRIMSON)
cols = [(L, 3100000, "TỈ LỆ BÀI ĐEM ĐI DẠY"), (L + 3400000, 1400000, "VÒNG 0"),
        (L + 4800000, 1400000, "1"), (L + 6200000, 1400000, "2"),
        (L + 7600000, 1400000, "3"), (L + 9000000, 1400000, "4")]
rows = [
    ("Số bài giữ được — GSM8K", "2725", "2551", "2356", "1837", "1100"),
    ("Số bài giữ được — MATH-500", "1237", "1179", "1039", "800", "466"),
    ("GSM8K chiếm bao nhiêu", "68,8%", "68,4%", "69,4%", "69,7%", "70,2%"),
]
y = table(s, 2000000, cols, rows, rowh=400000, rsize=11.5, emph=lambda i: i == 2)
tb(s, L, y + 280000, W, 600000,
   "Gần 70% bài đem đi dạy là của GSM8K. Nên điểm của MATH-500 thật ra bị ảnh hưởng bởi chuyện\n"
   "xảy ra bên GSM8K. Không tách được hai yếu tố này ra khỏi nhau.",
   size=12.5, color=BODY, line_spacing=1.4)
panel(s, L - 120000, y + 1040000, W + 240000, 880000, fill=RGBColor(0xFD, 0xF3, 0xF3))
tb(s, L + 120000, y + 1180000, W - 240000, 640000,
   "LỖI 2 — chấm điểm trên chính những đề đã dùng để chọn bài dạy.\n"
   "Nên điểm tụt có thể chỉ là model quên bài cũ, chứ chưa chắc năng lực giảm thật.",
   size=12.5, bold=True, color=CRIMSON, line_spacing=1.35)

# =========================================================== 9 · redo
s = new()
header(s, 8, "THÍ NGHIỆM LÀM LẠI", "Năm lần chạy mới, sửa cả hai lỗi",
       sub="Mỗi lần chỉ chạy một bộ đề. Giữ riêng 30% số đề làm đề thi, model chưa từng được học.")
cols = [(L, 2700000, "LẦN CHẠY"), (L + 2900000, 2300000, "BỘ ĐỀ"),
        (L + 5200000, 2300000, "MÁY CHẤM"), (L + 7500000, 1400000, "SEED"),
        (L + 8900000, 1600000, "GPU")]
rows = [
    ("A", "MATH-500", "để nguyên", "0", "~5 giờ"),
    ("A  chạy lại", "MATH-500", "để nguyên", "1", "~5 giờ"),
    ("B", "MATH-500", "ĐÃ SỬA", "0", "~5 giờ"),
    ("B  chạy lại", "MATH-500", "ĐÃ SỬA", "1", "~5 giờ"),
    ("C", "GSM8K", "để nguyên", "0", "~5,5 giờ"),
]
y = table(s, 2150000, cols, rows, rowh=430000, rsize=12,
          emph=lambda i: i in (2, 3))
panel(s, L - 120000, y + 300000, W + 240000, 780000, fill=RGBColor(0xF0, 0xF6, 0xFA))
tb(s, L + 120000, y + 460000, W - 240000, 520000,
   "A và B giống hệt nhau, chỉ khác đúng một chỗ: ở B, lỗi của máy chấm đã được sửa.\n"
   "Nếu giả thuyết ban đầu đúng thì B phải khá hơn A rõ rệt.",
   size=12.5, bold=True, color=BLUE, line_spacing=1.35)
tb(s, L, 6350000, W, 300000,
   "Tổng khoảng 25 giờ GPU, chia nhiều phiên vì Kaggle giới hạn 12 tiếng một lần.",
   size=10, color=MUTED)

# =========================================================== 10 · chart 1
s = new()
header(s, 9, "KẾT QUẢ", "Đo đúng cách thì không còn thấy tụt")
s.shapes.add_picture(f"{FIG}/deck_collapse.png", Emu((SW - 9300000) // 2), Emu(1720000),
                     width=Emu(9300000))
tb(s, L, 5830000, W, 500000,
   "Hai đường cam là cách đo cũ, tụt 22 đến 26 điểm. Ba đường còn lại là cách đo mới, gần như nằm ngang.\n"
   "Cú tụt ban đầu đến từ thiết kế đo, không phải từ máy chấm.",
   size=12.5, color=BODY, line_spacing=1.4)

# =========================================================== 11 · chart 2
s = new()
header(s, 10, "THÍ NGHIỆM ĐỐI CHỨNG", "Sửa máy chấm nhưng kết quả không đổi")
s.shapes.add_picture(f"{FIG}/deck_control.png", Emu((SW - 9300000) // 2), Emu(1720000),
                     width=Emu(9300000))
tb(s, L, 5660000, W, 700000,
   "Hai đường nằm chồng lên nhau ở cả hai lần chạy. Đúng cái lỗi mà đề tài cho là nguyên nhân đã được\n"
   "sửa, nhưng điểm không nhúc nhích. Đây là bằng chứng mạnh nhất bác bỏ giả thuyết ban đầu.",
   size=12.5, color=BODY, line_spacing=1.4)
tb(s, L, 6400000, W, 300000,
   "Đề thi có 150 đề nên mỗi đề đáng 0,67 điểm. A và B chênh nhau nhiều nhất 0,6 điểm, tức đúng một đề.",
   size=10, color=MUTED)

# =========================================================== 12 · why (dark)
s = new()
bg(s, DARK)
tb(s, L, 430000, 7000000, 250000, "VÌ SAO", size=10.5, bold=True, color=RGBColor(0xE8, 0x8A, 0x92))
tb(s, L, 830000, W, 620000, "Lỗi đó nặng thật, nhưng rất hiếm khi xảy ra",
   size=29, font=DISPLAY, bold=True, color=WHITE)
for i, (big, cap) in enumerate([
    ("100%", "gặp cách viết đó là máy chấm\ngạch, không trượt lần nào"),
    ("0,55%", "nhưng trong 4000 bài model làm\nmỗi vòng, chỉ 22 bài viết kiểu đó"),
    ("0,55%", "nhân lại, đó là phần bài bị gạch\noan. Quá ít để làm tụt 20 điểm"),
]):
    x = L + i * 3560000
    tb(s, x, 2150000, 3300000, 800000, big, size=52, font=DISPLAY, bold=True,
       color=WHITE if i < 2 else RGBColor(0xFF, 0xC9, 0x4D))
    tb(s, x, 3150000, 3300000, 800000, cap, size=12.5, color=DARKMUTED, line_spacing=1.35)
    if i < 2:
        tb(s, x + 3180000, 2300000, 300000, 500000, "×" if i == 0 else "=",
           size=24, color=RGBColor(0x5A, 0x5C, 0x66))
rule(s, L, 4350000, W, color=RGBColor(0x33, 0x34, 0x3B))
tb(s, L, 4600000, W, 900000,
   "Đo trực tiếp: ở vòng 0 model chưa học gì, nên A và B làm ra y hệt một bộ bài. Khác nhau duy nhất\n"
   "là máy chấm nào chấm. Sửa máy chấm xong, kết quả đổi đúng 1 đề trên 150 đề.",
   size=13, color=RGBColor(0xD6, 0xD7, 0xDC), line_spacing=1.45)
tb(s, L, 5750000, W, 400000,
   "Bài học: một lỗi nặng tới đâu cũng chỉ hại được đúng bằng số lần nó thật sự xảy ra.",
   size=13, bold=True, color=RGBColor(0xFF, 0xC9, 0x4D))

# =========================================================== 13 · pivot
s = new()
header(s, 11, "PHẠM VI ĐỀ TÀI", "Kết luận thu hẹp lại, nhưng có cơ sở vững")
panel(s, L - 120000, 1950000, 5100000, 3120000)
pill(s, L + 120000, 2150000, "ĐÃ BỎ", fill=MUTED, width=1200000, height=300000)
tb(s, L + 120000, 2650000, 4700000, 900000,
   "“Máy chấm gạch nhầm theo\nmột kiểu cố định sẽ làm\nmodel dở đi qua từng vòng.”",
   size=15, font=DISPLAY, bold=True, color=MUTED, line_spacing=1.3)
tb(s, L + 120000, 3950000, 4700000, 800000,
   "Đã kiểm tra bằng thí nghiệm đối chứng,\nchạy lặp hai lần. Không đúng.",
   size=12, color=MUTED, line_spacing=1.35)

panel(s, L + 5400000, 1950000, 5310000, 3120000, fill=RGBColor(0xF0, 0xF6, 0xFA))
pill(s, L + 5640000, 2150000, "GIỮ LẠI", fill=BLUE, width=1300000, height=300000)
tb(s, L + 5640000, 2650000, 4800000, 900000,
   "“Gộp nhiều bộ đề dạy chung,\nrồi chấm trên chính đề đã học,\nsẽ tạo ra cú tụt giả.”",
   size=15, font=DISPLAY, bold=True, color=INK, line_spacing=1.3)
tb(s, L + 5640000, 3950000, 4800000, 800000,
   "Kèm một lưu ý cho người sau: muốn biết\nmột lỗi máy chấm có hại không thì phải\nđếm xem nó xảy ra bao nhiêu lần.",
   size=12, color=BODY, line_spacing=1.35)

tb(s, L, 5330000, W, 700000,
   "Kết luận này hẹp hơn mục tiêu ban đầu. Nhưng cái bẫy thiết kế ở đây khá phổ biến trong các\n"
   "nghiên cứu cùng hướng, nên vẫn là đóng góp có ích.",
   size=13, color=BODY, line_spacing=1.4)

# =========================================================== 14 · the map
s = new()
header(s, 12, "BÀI HỌC RÚT RA", "Lần vừa rồi chọn nhầm chỗ để tìm hiệu ứng")
tb(s, L, 1600000, W, 330000,
   "Cả hai con số dưới đây đều là số đã đo của đề tài, không phải ước lượng.",
   size=12.5, color=BODY)
cols = [(L, 3000000, "CÁCH VIẾT ĐÁP ÁN"), (L + 3200000, 2500000, "MODEL DÙNG BAO NHIÊU"),
        (L + 5700000, 2400000, "MÁY CHẤM GẠCH"), (L + 8100000, 2400000, "THIỆT HẠI THỰC TẾ")]
rows = [
    ("\\frac", "55,8%", "0%", "0%"),
    ("\\boxed", "51,5%", "8,5%", "4,4%"),
    ("số thập phân", "11,6%", "thấp", "thấp"),
    ("0,50  (thừa số 0)", "1,2%", "59%", "0,7%"),
    ("\\dfrac", "0,55%", "100%", "0,55%"),
    ("\\tfrac", "0%", "100%", "0%"),
]
y = table(s, 2050000, cols, rows, rowh=390000, rsize=11.5,
          emph=lambda i: i == 4)
tb(s, L, y + 260000, W, 700000,
   "Thiệt hại thực tế bằng tỉ lệ gạch nhân tần suất. Cách viết đã đem ra thử là \\dfrac — gạch nặng nhất,\n"
   "nhưng cũng hiếm nhất. Đó là ô cho hiệu ứng nhỏ nhất trong cả bảng.",
   size=12.5, color=BODY, line_spacing=1.4)
panel(s, L - 120000, y + 930000, W + 240000, 560000, fill=RGBColor(0xF0, 0xF6, 0xFA))
tb(s, L + 120000, y + 1045000, W - 240000, 330000,
   "Vùng đáng quan tâm — cách viết vừa phổ biến vừa bị gạch — đã tìm ra nguyên nhân và vá xong.",
   size=12.5, bold=True, color=BLUE)
tb(s, L, 6560000, W, 260000,
   "Cột \\boxed đã sửa: 8,5%/4,4% là phần lỗi thật do boxed gây ra (17/200), tách khỏi 24/200 đề gốc "
   "vốn đã không đọc được kể cả không đóng hộp (lỗi khác, đã biết từ trước).",
   size=9.5, color=MUTED)

# =========================================================== 15 · new direction
s = new()
header(s, 13, "ĐỀ TÀI TIẾP THEO",
       "Đo ngưỡng: lỗi phải phổ biến tới mức nào mới gây hại?")
tb(s, L, 1600000, W, 700000,
   "Cách làm giữ nguyên toàn bộ vòng lặp, chỉ đổi chỗ máy chấm bị lệch. Mỗi lần chạy là một điểm\n"
   "trên trục tần suất. Điểm đầu tiên đã có sẵn; điểm thứ hai đã tìm ra nguyên nhân và vá xong,\n"
   "chỉ còn thiếu lượt chạy GPU.",
   size=13.5, color=BODY, line_spacing=1.45)
for i, (tag, fmt, freq, colour, fill, note) in enumerate([
    ("ĐIỂM 1 — ĐÃ CÓ", "\\dfrac", "0,55%", MUTED, SURFACE,
     "Không thấy ảnh hưởng.\nĐây là kết quả ba tuần vừa rồi."),
    ("ĐIỂM 2 — ĐÃ VÁ, CHỜ GPU", "\\boxed", "51%", BLUE, RGBColor(0xF0, 0xF6, 0xFA),
     "Nguyên nhân: máy chấm đọc đề gốc thiếu\nkhi không đóng hộp. Đã vá + có test, chỉ\ncòn chạy — khoảng 5 giờ GPU."),
]):
    x = L + i * 5400000
    panel(s, x, 2500000, 5190000, 1800000, fill=fill)
    pill(s, x + 260000, 2680000, tag, fill=colour, width=1900000, height=300000)
    tb(s, x + 260000, 3130000, 2400000, 400000, fmt, size=19, color=INK)
    tb(s, x + 2900000, 3130000, 2100000, 400000, freq, size=26, font=DISPLAY,
       bold=True, color=colour)
    tb(s, x + 260000, 3670000, 4700000, 550000, note, size=12, color=BODY,
       line_spacing=1.3)
tb(s, L, 4520000, W, 300000, "HAI KHẢ NĂNG, CẢ HAI ĐỀU RA KẾT QUẢ DÙNG ĐƯỢC",
   size=11, bold=True, color=MUTED)
for i, (colour, lbl, txt) in enumerate([
    (GREEN, "Nếu tụt điểm", "quy luật được chứng minh bằng thực nghiệm, và đề tài\ncó một ngưỡng cụ thể để cảnh báo người dùng."),
    (ORANGE, "Nếu vẫn không tụt", "thì lỗi máy chấm không phải thứ đáng lo trong\nself-training, cũng là một kết luận rõ ràng."),
]):
    x = L + i * 5400000
    pill(s, x, 4930000, lbl, fill=colour, width=1750000, height=310000)
    tb(s, x, 5400000, 5000000, 600000, txt, size=12, color=BODY, line_spacing=1.35)
tb(s, L, 6300000, W, 300000,
   "Cờ --patch-verifier-boxed đã code + có test (tests/test_verify_adapter.py); toàn bộ vòng lặp và "
   "dữ liệu cũ dùng lại nguyên, chỉ còn thiếu lượt chạy GPU.",
   size=10.5, color=MUTED)

# =========================================================== 16 · open question
s = new()
header(s, 14, "CÂU HỎI CHƯA TRẢ LỜI ĐƯỢC", "Thí nghiệm kiểm chứng đang chạy")
tb(s, L, 1620000, W, 700000,
   "Cả 7 lần chạy, điểm đều tụt khoảng 3 điểm ngay ở vòng 1 rồi đứng yên. Nhưng các công trình lớn\n"
   "về tự học đều báo cáo model KHÁ LÊN. Chưa giải thích được vì sao kết quả ở đây ngược lại.",
   size=14, color=INK, line_spacing=1.4)
panel(s, L - 120000, 2550000, W + 240000, 900000)
tb(s, L + 120000, 2720000, W - 240000, 640000,
   "Có một khả năng đơn giản chưa loại trừ được: model này vốn đã được tinh chỉnh rất kỹ. Dạy thêm\n"
   "một lượng nhỏ có thể chỉ làm nó lệch khỏi trạng thái tốt sẵn có, bất kể dạy bằng dữ liệu gì.",
   size=12.5, color=BODY, line_spacing=1.45)
tb(s, L, 3720000, W, 300000, "THÍ NGHIỆM PHÂN ĐỊNH: dạy bằng lời giải mẫu của sách, thay vì bài model tự làm",
   size=11, bold=True, color=MUTED)
for i, (colour, lbl, txt) in enumerate([
    (GREEN, "Nếu khá lên", "thì vòng lặp không sao, và cái hại đúng là\ndo model học từ bài của chính nó."),
    (ORANGE, "Nếu cũng tụt", "thì cú tụt là do việc dạy thêm, không liên\nquan tự học. Kết luận phải sửa lần nữa."),
]):
    x = L + i * 5400000
    panel(s, x, 4180000, 5190000, 1350000)
    pill(s, x + 240000, 4360000, lbl, fill=colour, width=1500000, height=310000)
    tb(s, x + 240000, 4830000, 4700000, 600000, txt, size=12, color=BODY, line_spacing=1.35)
tb(s, L, 5800000, W, 300000,
   "Phần code đã hoàn tất, đang chờ tới lượt GPU.", size=10.5, color=MUTED)

# =========================================================== 17 · limits
s = new()
header(s, 15, "HẠN CHẾ", "Ba điểm cần lưu ý khi đọc kết quả")
lim = [
    ("Đề thi chỉ có 150 đề",
     "Mỗi đề đáng 0,67 điểm. Chỉ đổi cách bốc đề thi thôi là điểm vòng 0 đã lệch 4,7 điểm, lớn hơn cả hiệu ứng đang đo."),
    ("Mỗi cấu hình mới chạy 2 lần",
     "Riêng lần chạy C và các lần chạy cũ mới có 1 lần. Chưa đủ cơ sở để khẳng định về cú tụt 12,7 điểm của GSM8K."),
    ("Lần chạy mới khác lần cũ ba chỗ",
     "Bỏ gộp bộ đề, thêm đề thi riêng, giảm số đề. Nên kết luận chỉ dựa trên so sánh A với B, vì hai lần chạy đó chỉ khác nhau đúng một biến."),
]
y = 2000000
for i, (h, d) in enumerate(lim, 1):
    panel(s, L - 120000, y, W + 240000, 1150000)
    tb(s, L + 120000, y + 200000, 400000, 300000, f"{i:02d}", size=13,
       font=DISPLAY, bold=True, color=CRIMSON)
    tb(s, L + 700000, y + 190000, 9500000, 300000, h, size=14, bold=True, color=INK)
    tb(s, L + 700000, y + 600000, 9500000, 450000, d, size=12, color=BODY, line_spacing=1.3)
    y += 1330000

# =========================================================== 18 · summary
s = new()
header(s, 16, "TÓM TẮT", "Kết quả ba tuần và hướng tiếp theo")
panel(s, L - 120000, 1900000, W + 240000, 1460000, fill=RGBColor(0xF0, 0xF6, 0xFA))
tb(s, L + 120000, 2100000, W - 240000, 1100000,
   "Thí nghiệm đối chứng cho thấy giả thuyết ban đầu không đúng. Nguyên nhân đã xác định được:\n"
   "lỗi của máy chấm tuy nặng nhưng chỉ xảy ra ở 0,55% số bài.\n"
   "Đề tài chuyển sang cảnh báo về thiết kế đo — hẹp hơn, nhưng có cơ sở vững.",
   size=14, font=DISPLAY, color=INK, line_spacing=1.4)
for i, (lbl, txt) in enumerate([
    ("ĐÃ LÀM", "7 lần chạy, khoảng 40 giờ GPU. Phát hiện lỗi trong thiết kế đo và sửa lại."),
    ("KẾT QUẢ", "Giả thuyết ban đầu không đúng, và đo được nguyên nhân vì sao."),
    ("ĐANG CHẠY", "Thí nghiệm để biết cú tụt là do tự học, hay chỉ do việc dạy thêm."),
    ("SẮP TỚI", "Thí nghiệm điều khiển tần suất lỗi, để tìm ngưỡng gây hại."),
]):
    yy = 3560000 + i * 570000
    tb(s, L, yy, 1700000, 300000, lbl, size=11, bold=True, color=CRIMSON)
    tb(s, L + 1800000, yy - 15000, 8700000, 330000, txt, size=12.5, color=BODY)
rule(s, L, 5900000, W)
tb(s, L, 6100000, W, 300000, "Cảm ơn đã theo dõi. Rất mong nhận được góp ý.",
   size=12.5, color=MUTED)

prs.save(OUT)
print("saved", OUT, "| slides:", len(prs.slides._sldIdLst))
