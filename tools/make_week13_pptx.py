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
   "Em kiểm tra lại giả thuyết\ncủa mình, và nó sai",
   size=40, font=DISPLAY, bold=True, color=INK, line_spacing=1.08)
tb(s, L, 3850000, 9200000, 1000000,
   "Ba tuần đầu em chạy thí nghiệm và tưởng đã chứng minh được điều mình nghĩ. Sau đó em phát hiện\n"
   "cách đo của mình có lỗi. Em đo lại cho đúng, và kết quả ngược với giả thuyết ban đầu.",
   size=15, color=BODY, line_spacing=1.4)
rule(s, L, 5250000, 2400000, color=CRIMSON, pt=2.0)
tb(s, L, 5480000, 6000000, 300000, "Nguyễn Tấn Sang", size=13, bold=True, color=INK)
tb(s, L, 5820000, 6000000, 300000, "12 tháng 9, 2026", size=12, color=MUTED)

# =========================================================== 2 · agenda
s = new()
header(s, 1, "NỘI DUNG", "Em sẽ trình bày theo thứ tự này")
items = [
    ("Đề tài của em là gì", "và một vòng thí nghiệm chạy ra sao"),
    ("Máy chấm sai ở chỗ nào", "em đo được trước khi chạy"),
    ("Tuần 1 và tuần 2", "chạy thật, và cả hai model đều tụt điểm"),
    ("Chỗ em thấy không ổn", "cách đo của em có hai lỗi"),
    ("Đo lại cho đúng", "năm lần chạy mới, kết quả ngược lại"),
    ("Vì sao lại như vậy", "và đề tài đi tiếp thế nào"),
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
   "Máy chấm của em có sai, và sai theo một quy luật cố định. Vậy sau nhiều vòng tự học,\n"
   "model có bị dở đi không?",
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
   "Mỗi vòng em dạy lại từ model gốc, chỉ bằng những bài của vòng trước. Nên nếu máy chấm bỏ sót\n"
   "một kiểu bài nào đó, thì vòng sau model càng ít gặp kiểu bài đó. Vòng sau nữa lại càng ít hơn.",
   size=13, color=BODY, line_spacing=1.45)
panel(s, L - 120000, 4950000, W + 240000, 1400000)
tb(s, L + 120000, 5180000, W - 240000, 750000,
   "Hai con số em dùng để đo suốt bài:\n"
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
panel(s, L - 120000, 5550000, W + 240000, 620000)
tb(s, L + 120000, 5740000, W - 240000, 300000,
   "Em kiểm tra tay 128 bài đúng trên MATH-500: máy gạch nhầm 10 bài, tức 7,8%. Trên GSM8K thì không gạch nhầm bài nào.",
   size=12.5, bold=True, color=INK)

# =========================================================== 6 · week 1
s = new()
header(s, 5, "TUẦN 1", "Lần chạy đầu tiên, model nhỏ")
tb(s, L, 1700000, W, 400000,
   "Em chạy model Qwen 0.5B, 500 đề mỗi bộ, 5 vòng, trên GPU của Kaggle.",
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
   "Cả hai con số đều tụt. Em thấy vậy là khớp với điều mình nghĩ: máy chấm gạch nhầm bài đúng,\n"
   "model học thiếu, nên dở đi. Nhưng model này nhỏ, mức tụt cũng ít, nên em chưa dám chắc.",
   size=13.5, color=BODY, line_spacing=1.45)
panel(s, L - 120000, 5050000, W + 240000, 620000, fill=RGBColor(0xF0, 0xF6, 0xFA))
tb(s, L + 120000, 5240000, W - 240000, 300000,
   "Nên tuần 2 em chạy lại với model to gấp ba, xem hiện tượng có rõ hơn không.",
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
   "Model 1.5B tụt rất sâu, vòng nào cũng tụt, không vòng nào gượng lại. Đến đây em gần như tin chắc\n"
   "là giả thuyết của mình đúng.",
   size=13, color=BODY, line_spacing=1.45)
panel(s, L - 120000, y + 1000000, W + 240000, 830000, fill=RGBColor(0xFD, 0xF3, 0xF3))
tb(s, L + 120000, y + 1160000, W - 240000, 460000,
   "Nhưng có một chỗ em thấy lạ: bộ GSM8K lại tụt nhiều nhất.\n"
   "Mà GSM8K là bộ máy chấm gần như không gạch nhầm bài nào.",
   size=12.5, bold=True, color=CRIMSON, line_spacing=1.4)

# =========================================================== 8 · the flaw
s = new()
header(s, 7, "CHỖ EM THẤY KHÔNG ỔN", "Cách đo của em có hai lỗi")
tb(s, L, 1620000, W, 300000, "LỖI 1 — em gộp hai bộ đề lại rồi dạy chung một lần",
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
   "xảy ra bên GSM8K. Em không tách được hai thứ đó ra khỏi nhau.",
   size=12.5, color=BODY, line_spacing=1.4)
panel(s, L - 120000, y + 1040000, W + 240000, 880000, fill=RGBColor(0xFD, 0xF3, 0xF3))
tb(s, L + 120000, y + 1180000, W - 240000, 640000,
   "LỖI 2 — em chấm điểm trên chính những đề đã dùng để chọn bài dạy.\n"
   "Nên điểm tụt có thể chỉ là model quên bài cũ, chứ không phải nó dở đi thật.",
   size=12.5, bold=True, color=CRIMSON, line_spacing=1.35)

# =========================================================== 9 · redo
s = new()
header(s, 8, "ĐO LẠI CHO ĐÚNG", "Năm lần chạy mới, sửa cả hai lỗi",
       sub="Mỗi lần chỉ chạy một bộ đề. Giữ riêng 30% số đề làm đề thi, chưa từng cho model học.")
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
   "A và B giống hệt nhau, chỉ khác đúng một chỗ: B em đã sửa lỗi của máy chấm.\n"
   "Nếu giả thuyết của em đúng thì B phải khá hơn A rõ rệt.",
   size=12.5, bold=True, color=BLUE, line_spacing=1.35)
tb(s, L, 6350000, W, 300000,
   "Tổng khoảng 25 giờ GPU, chia nhiều phiên vì Kaggle giới hạn 12 tiếng một lần.",
   size=10, color=MUTED)

# =========================================================== 10 · chart 1
s = new()
header(s, 9, "KẾT QUẢ", "Đo lại cho đúng thì không còn thấy tụt nữa")
s.shapes.add_picture(f"{FIG}/deck_collapse.png", Emu((SW - 9300000) // 2), Emu(1720000),
                     width=Emu(9300000))
tb(s, L, 5830000, W, 500000,
   "Hai đường cam là cách đo cũ, tụt 22 đến 26 điểm. Ba đường còn lại là cách đo mới, gần như nằm ngang.\n"
   "Vậy cú tụt kia là do em đo sai, không phải do máy chấm.",
   size=12.5, color=BODY, line_spacing=1.4)

# =========================================================== 11 · chart 2
s = new()
header(s, 10, "THÍ NGHIỆM QUAN TRỌNG NHẤT", "Sửa máy chấm rồi mà không đổi gì cả")
s.shapes.add_picture(f"{FIG}/deck_control.png", Emu((SW - 9300000) // 2), Emu(1720000),
                     width=Emu(9300000))
tb(s, L, 5660000, W, 700000,
   "Hai đường nằm chồng lên nhau ở cả hai lần chạy. Em sửa đúng cái lỗi mà cả đề tài cho là nguyên nhân,\n"
   "mà điểm không nhúc nhích. Chỗ này là bằng chứng mạnh nhất cho thấy em đã nghĩ sai.",
   size=12.5, color=BODY, line_spacing=1.4)
tb(s, L, 6400000, W, 300000,
   "Đề thi có 150 đề, nên mỗi đề đáng 0,67 điểm. A và B chênh nhau nhiều nhất 0,6 điểm, tức là đúng một đề.",
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
   "Em còn đo được trực tiếp. Ở vòng 0 model chưa học gì, nên A và B làm ra y hệt một bộ bài. Khác nhau\n"
   "chỉ là máy chấm nào chấm. Sửa máy chấm xong, kết quả đổi đúng 1 đề trên 150 đề.",
   size=13, color=RGBColor(0xD6, 0xD7, 0xDC), line_spacing=1.45)
tb(s, L, 5750000, W, 400000,
   "Bài học: một lỗi nặng tới đâu cũng chỉ hại được đúng bằng số lần nó thật sự xảy ra.",
   size=13, bold=True, color=RGBColor(0xFF, 0xC9, 0x4D))

# =========================================================== 13 · pivot
s = new()
header(s, 11, "ĐỀ TÀI ĐI TIẾP THẾ NÀO", "Kết luận nhỏ lại, nhưng em chắc chắn về nó")
panel(s, L - 120000, 1950000, 5100000, 3120000)
pill(s, L + 120000, 2150000, "ĐÃ BỎ", fill=MUTED, width=1200000, height=300000)
tb(s, L + 120000, 2650000, 4700000, 900000,
   "“Máy chấm gạch nhầm theo\nmột kiểu cố định sẽ làm\nmodel dở đi qua từng vòng.”",
   size=15, font=DISPLAY, bold=True, color=MUTED, line_spacing=1.3)
tb(s, L + 120000, 3950000, 4700000, 800000,
   "Em đã tự kiểm tra bằng thí nghiệm đối\nchứng, chạy hai lần cho chắc. Không đúng.",
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
   "Kết luận này nhỏ hơn cái em định làm lúc đầu. Nhưng cái bẫy em vấp phải thì nhiều người cũng đang\n"
   "vấp, nên em nghĩ vẫn đáng viết ra.",
   size=13, color=BODY, line_spacing=1.4)

# =========================================================== 14 · open question
s = new()
header(s, 12, "MỘT CHỖ EM CÒN CHƯA CHẮC", "Và em đang chạy thí nghiệm để kiểm tra")
tb(s, L, 1620000, W, 700000,
   "Cả 7 lần chạy, điểm đều tụt khoảng 3 điểm ngay ở vòng 1 rồi đứng yên. Nhưng mấy bài báo lớn\n"
   "về tự học đều báo là model KHÁ LÊN. Em chưa giải thích được vì sao của em ngược lại.",
   size=14, color=INK, line_spacing=1.4)
panel(s, L - 120000, 2550000, W + 240000, 900000)
tb(s, L + 120000, 2720000, W - 240000, 640000,
   "Có một khả năng đơn giản mà em chưa loại trừ được: model này vốn đã được tinh chỉnh rất kỹ rồi.\n"
   "Em dạy thêm một chút nữa có thể chỉ làm nó lệch khỏi trạng thái tốt sẵn có, bất kể em dạy bằng gì.",
   size=12.5, color=BODY, line_spacing=1.45)
tb(s, L, 3720000, W, 300000, "EM SẼ THỬ: dạy bằng lời giải mẫu của sách, thay vì bài model tự làm",
   size=11, bold=True, color=MUTED)
for i, (colour, lbl, txt) in enumerate([
    (GREEN, "Nếu khá lên", "thì vòng lặp không sao, và cái hại đúng là\ndo model học từ bài của chính nó."),
    (ORANGE, "Nếu cũng tụt", "thì cú tụt là do việc dạy thêm, không liên\nquan tự học. Em phải sửa kết luận lần nữa."),
]):
    x = L + i * 5400000
    panel(s, x, 4180000, 5190000, 1350000)
    pill(s, x + 240000, 4360000, lbl, fill=colour, width=1500000, height=310000)
    tb(s, x + 240000, 4830000, 4700000, 600000, txt, size=12, color=BODY, line_spacing=1.35)
tb(s, L, 5800000, W, 300000,
   "Code đã viết xong, đang chờ tới lượt GPU.", size=10.5, color=MUTED)

# =========================================================== 15 · limits
s = new()
header(s, 13, "NHỮNG CHỖ CÒN YẾU", "Em xin nói trước")
lim = [
    ("Đề thi chỉ có 150 đề",
     "Mỗi đề đáng 0,67 điểm. Chỉ cần đổi cách bốc đề thi thôi là điểm vòng 0 đã lệch 4,7 điểm, nhiều hơn cả cái em đang đo."),
    ("Mỗi cấu hình mới chạy 2 lần",
     "Riêng lần chạy C và mấy lần cũ thì mới 1 lần. Nên em chưa dám chắc về cú tụt 12,7 điểm của GSM8K."),
    ("Lần chạy mới khác lần cũ ba chỗ",
     "Bỏ gộp bộ đề, thêm đề thi riêng, và giảm số đề. Nên em chỉ dám kết luận dựa trên so sánh A với B, vì hai lần đó chỉ khác nhau một chỗ."),
]
y = 2000000
for i, (h, d) in enumerate(lim, 1):
    panel(s, L - 120000, y, W + 240000, 1150000)
    tb(s, L + 120000, y + 200000, 400000, 300000, f"{i:02d}", size=13,
       font=DISPLAY, bold=True, color=CRIMSON)
    tb(s, L + 700000, y + 190000, 9500000, 300000, h, size=14, bold=True, color=INK)
    tb(s, L + 700000, y + 600000, 9500000, 450000, d, size=12, color=BODY, line_spacing=1.3)
    y += 1330000

# =========================================================== 16 · summary
s = new()
header(s, 14, "TÓM TẮT", "Ba tuần vừa rồi, và việc sắp tới")
panel(s, L - 120000, 1900000, W + 240000, 1460000, fill=RGBColor(0xF0, 0xF6, 0xFA))
tb(s, L + 120000, 2100000, W - 240000, 1100000,
   "Em dựng một thí nghiệm để kiểm tra giả thuyết của chính mình, và nó cho thấy em sai.\n"
   "Lý do em cũng tìm ra: lỗi của máy chấm tuy nặng nhưng chỉ xảy ra ở 0,55% số bài.\n"
   "Đề tài chuyển sang cảnh báo về cách đo, nhỏ hơn nhưng em chắc chắn.",
   size=14, font=DISPLAY, color=INK, line_spacing=1.4)
for i, (lbl, txt) in enumerate([
    ("ĐÃ LÀM", "7 lần chạy, khoảng 40 giờ GPU. Tìm ra lỗi trong cách đo và sửa lại."),
    ("KẾT QUẢ", "Giả thuyết ban đầu không đúng, và em đo được vì sao nó không đúng."),
    ("ĐANG CHẠY", "Thí nghiệm để biết cú tụt là do tự học, hay chỉ do việc dạy thêm."),
    ("SẮP TỚI", "Chạy lặp thêm cho chắc, rồi viết lại bài báo theo kết luận mới."),
]):
    yy = 3560000 + i * 570000
    tb(s, L, yy, 1700000, 300000, lbl, size=11, bold=True, color=CRIMSON)
    tb(s, L + 1800000, yy - 15000, 8700000, 330000, txt, size=12.5, color=BODY)
rule(s, L, 5900000, W)
tb(s, L, 6100000, W, 300000, "Em cảm ơn thầy. Mong thầy góp ý giúp em.",
   size=12.5, color=MUTED)

prs.save(OUT)
print("saved", OUT, "| slides:", len(prs.slides._sldIdLst))
