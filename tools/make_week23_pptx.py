"""Combined week 2-3 progress deck — modern rebuild.

One arc, not two: hypothesis -> apparent confirmation -> the confound -> the
corrected experiment -> refutation -> cause -> narrowed scope.

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
OUT = f"{REPO}/BaoCaoTienDo_Tuan2-3_52300057_52300006.pptx"
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
tb(s, L, 1180000, W, 300000, "BÁO CÁO TIẾN ĐỘ  ·  TUẦN 2 – 3",
   size=12, bold=True, color=CRIMSON)
tb(s, L, 1700000, 10200000, 1900000,
   "Giả thuyết trung tâm bị bác bỏ\nbằng thí nghiệm đối chứng",
   size=40, font=DISPLAY, bold=True, color=INK, line_spacing=1.08)
tb(s, L, 3850000, 8900000, 1000000,
   "Hai tuần: từ chỗ tưởng đã xác nhận được giả thuyết, đến chỗ phát hiện thiết kế đo có lỗ hổng,\n"
   "làm lại cho sạch, và bác bỏ chính giả thuyết của mình.",
   size=15, color=BODY, line_spacing=1.4)
rule(s, L, 5250000, 2400000, color=CRIMSON, pt=2.0)
tb(s, L, 5480000, 6000000, 300000, "Nguyễn Tấn Sang", size=13, bold=True, color=INK)
tb(s, L, 5820000, 6000000, 300000, "12 tháng 9, 2026", size=12, color=MUTED)

# =========================================================== 2 · agenda
s = new()
header(s, 1, "NỘI DUNG", "Những gì trình bày hôm nay")
items = [
    ("Câu hỏi nghiên cứu", "và độ lệch của máy chấm, đã đo trước khi chạy"),
    ("Kết quả đầu tiên", "cả hai model đều sụp — tưởng đã xác nhận"),
    ("Phát hiện", "thiết kế đo có hai lỗ hổng"),
    ("Làm lại cho sạch", "năm lần chạy cô lập, có đối chứng"),
    ("Đối chứng quyết định", "và vì sao kết quả lại như vậy"),
    ("Đề tài thu hẹp lại", "phạm vi mới, và việc còn phải làm"),
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

# =========================================================== 3 · question
s = new()
header(s, 2, "CÂU HỎI NGHIÊN CỨU", "Máy chấm tự động có làm ảo hoá\nviệc “tự cải thiện”?")
panel(s, L - 120000, 1980000, W + 240000, 1420000)
tb(s, L + 120000, 2130000, W - 240000, 1150000,
   "Cho model tự sinh lời giải, dùng máy chấm tự động lọc bài đúng, rồi dạy lại chính nó, lặp nhiều\n"
   "vòng. Nếu máy chấm sai có quy luật, liệu model có chỉ giỏi lên ở việc viết đúng kiểu máy chấm\n"
   "ưa, thay vì giỏi toán thật?",
   size=14, font=DISPLAY, color=INK, line_spacing=1.35)
tb(s, L, 3620000, W, 300000, "Độ lệch máy chấm — đã đo trước khi chạy, không giả định",
   size=11, bold=True, color=MUTED)
for i, (big, colour, cap) in enumerate([
    ("100%", CRIMSON, "lời giải ĐÚNG nhưng viết \\dfrac\nthay vì \\frac bị gạch — 146/146 lần"),
    ("7,8%", ORANGE, "tỉ lệ gạch nhầm bài đúng trên\nMATH-500, kiểm tra thủ công"),
    ("0%", GREEN, "trên GSM8K — đáp án là số nguyên,\nmáy chấm gần như không lệch"),
]):
    x = L + i * 3560000
    tb(s, x, 3900000, 3300000, 700000, big, size=42, font=DISPLAY, bold=True, color=colour)
    tb(s, x, 4750000, 3300000, 800000, cap, size=12, color=BODY, line_spacing=1.3)
tb(s, L, 5850000, W, 400000,
   "Giả thuyết: độ lệch một chiều này lặp qua nhiều vòng sẽ làm tập train co hẹp và lệch dần → model sụp.",
   size=12, bold=True, color=INK)

# =========================================================== 4 · GVT loop
s = new()
header(s, 3, "QUY TRÌNH", "Một vòng Generate → Verify → Train")
for i, (n, h, d) in enumerate([
    ("1", "Generate", "Model sinh k lời giải cho mỗi\nđề (k=8), bằng sampling."),
    ("2", "Verify", "Máy chấm so đáp án cuối với\nđáp án chuẩn — chỉ giữ bài đúng."),
    ("3", "Train", "Fine-tune LoRA trên đúng các\nlời giải vừa giữ, rồi lặp lại."),
]):
    x = L + i * 3560000
    panel(s, x, 2050000, 3300000, 1620000)
    tb(s, x + 240000, 2230000, 400000, 330000, n, size=17, font=DISPLAY,
       bold=True, color=CRIMSON)
    tb(s, x + 240000, 2650000, 2900000, 330000, h, size=15, bold=True, color=INK)
    tb(s, x + 240000, 3030000, 2900000, 600000, d, size=12, color=BODY, line_spacing=1.3)
rule(s, L, 3980000, W)
tb(s, L, 4180000, W, 1100000,
   "Điểm mấu chốt: mỗi vòng train một adapter MỚI từ model gốc, chỉ học trên tập bài mà máy chấm đã\n"
   "chấp nhận ở vòng trước. Nếu máy chấm gạch oan theo một hướng cố định, tập train mỗi vòng lệch dần\n"
   "theo hướng đó — và vì tập đó do chính vòng trước sinh ra, độ lệch không tự triệt tiêu.",
   size=13, color=BODY, line_spacing=1.45)
panel(s, L - 120000, 5450000, W + 240000, 620000)
tb(s, L + 120000, 5640000, W - 240000, 300000,
   "Hai thước đo dùng xuyên suốt:   pass@1 = làm 1 lần có đúng không.   "
   "pass@8 = cho làm 8 lần, có lần nào đúng không.",
   size=12.5, bold=True, color=INK)

# =========================================================== 5 · first results
s = new()
header(s, 4, "KẾT QUẢ ĐẦU TIÊN", "Cả hai model đều sụp — tưởng đã xác nhận")
cols = [(L, 3100000, "ĐO TRÊN"), (L + 3300000, 2200000, "PASS@1  VÒNG 0→4"),
        (L + 5600000, 2200000, "PASS@8  VÒNG 0→4"), (L + 7900000, 2600000, "MỨC GIẢM PASS@8")]
rows = [
    ("Qwen 0.5B — gộp 2 bộ đề", "31,1% → 27,4%", "60,5% → 54,9%", "−5,6 điểm"),
    ("Qwen 1.5B — gộp 2 bộ đề", "50,0% → 18,6%", "72,6% → 48,6%", "−24,0 điểm"),
    ("1.5B, tách riêng GSM8K", "69,6% → 26,6%", "91,4% → 65,8%", "−25,6 điểm"),
    ("1.5B, tách riêng MATH-500", "30,4% → 10,6%", "53,8% → 31,4%", "−22,4 điểm"),
]
y = table(s, 2050000, cols, rows, emph=lambda i: i == 1)
tb(s, L, y + 330000, W, 800000,
   "Giảm liên tục qua cả 5 vòng, không vòng nào tăng lại, model to hơn sụp nặng hơn hẳn.\n"
   "Nếu dừng ở đây, đây là một kết quả rất đẹp cho giả thuyết ban đầu.",
   size=13, color=BODY, line_spacing=1.4)
panel(s, L - 120000, y + 1180000, W + 240000, 560000, fill=RGBColor(0xFD, 0xF3, 0xF3))
tb(s, L + 120000, y + 1350000, W - 240000, 300000,
   "Nhưng có một chi tiết không khớp:  GSM8K — bộ mà máy chấm gần như KHÔNG lệch — lại sụp nhiều nhất.",
   size=12.5, bold=True, color=CRIMSON)

# =========================================================== 6 · confound
s = new()
header(s, 5, "PHÁT HIỆN", "Thiết kế đo có hai lỗ hổng")
tb(s, L, 1620000, W, 300000, "LỖ HỔNG 1 — hai bộ đề bị trộn chung vào MỘT adapter khi train",
   size=11.5, bold=True, color=CRIMSON)
cols = [(L, 3100000, "TỈ LỆ TRONG TẬP TRAIN"), (L + 3400000, 1400000, "VÒNG 0"),
        (L + 4800000, 1400000, "1"), (L + 6200000, 1400000, "2"),
        (L + 7600000, 1400000, "3"), (L + 9000000, 1400000, "4")]
rows = [
    ("Lời giải giữ — GSM8K", "2725", "2551", "2356", "1837", "1100"),
    ("Lời giải giữ — MATH-500", "1237", "1179", "1039", "800", "466"),
    ("% GSM8K trong tập train", "68,8%", "68,4%", "69,4%", "69,7%", "70,2%"),
]
y = table(s, 2000000, cols, rows, rowh=400000, rsize=11.5, emph=lambda i: i == 2)
tb(s, L, y + 280000, W, 600000,
   "Tập train luôn nghiêng ~69% về GSM8K. Điểm của MATH-500 vì thế phụ thuộc vào chuyện xảy ra bên\n"
   "GSM8K, và ngược lại — không cách nào tách “tại verifier lệch” khỏi “tại lây từ bộ kia”.",
   size=12.5, color=BODY, line_spacing=1.4)
panel(s, L - 120000, y + 1040000, W + 240000, 880000, fill=RGBColor(0xFD, 0xF3, 0xF3))
tb(s, L + 120000, y + 1180000, W - 240000, 640000,
   "LỖ HỔNG 2 — chấm điểm trên chính những đề đã dùng để chọn bài train.\n"
   "Nên “sụp” có thể chỉ là hết thuộc bài, không phải mất năng lực thật.",
   size=12.5, bold=True, color=CRIMSON, line_spacing=1.35)

# =========================================================== 7 · redesign
s = new()
header(s, 6, "LÀM LẠI CHO SẠCH", "Năm lần chạy cô lập, có đối chứng kiểm soát biến",
       sub="Tất cả: Qwen2.5-1.5B · 500 đề · 5 vòng · k=8 · tách riêng 30% đề làm đề thi chưa từng dùng để train.")
cols = [(L, 2700000, "LẦN CHẠY"), (L + 2900000, 2300000, "BỘ ĐỀ"),
        (L + 5200000, 2300000, "VERIFIER"), (L + 7500000, 1400000, "SEED"),
        (L + 8900000, 1600000, "GPU")]
rows = [
    ("A", "MATH-500", "gốc", "0", "~5 giờ"),
    ("A — lặp lại", "MATH-500", "gốc", "1", "~5 giờ"),
    ("B  ·  đối chứng", "MATH-500", "ĐÃ VÁ", "0", "~5 giờ"),
    ("B — lặp lại", "MATH-500", "ĐÃ VÁ", "1", "~5 giờ"),
    ("C", "GSM8K", "gốc", "0", "~5,5 giờ"),
]
y = table(s, 2150000, cols, rows, rowh=430000, rsize=12,
          emph=lambda i: i in (2, 3))
panel(s, L - 120000, y + 300000, W + 240000, 780000, fill=RGBColor(0xF0, 0xF6, 0xFA))
tb(s, L + 120000, y + 460000, W - 240000, 520000,
   "A và B khác nhau đúng MỘT biến: verifier có được vá hay không. Đây là thí nghiệm đối chứng mà thiết\n"
   "kế cũ không thể có — và là phép thử trực tiếp cho giả thuyết của đề tài.",
   size=12.5, bold=True, color=BLUE, line_spacing=1.35)
tb(s, L, 6350000, W, 300000,
   "Tổng ~25 giờ GPU Kaggle, chia nhiều phiên; kết quả lưu sau mỗi vòng để không mất khi phiên bị ngắt.",
   size=10, color=MUTED)

# =========================================================== 8 · chart: collapse
s = new()
header(s, 7, "KẾT QUẢ", "Cú sụp không tái lập khi đo đúng cách")
s.shapes.add_picture(f"{FIG}/deck_collapse.png", Emu((SW - 9300000) // 2), Emu(1720000),
                     width=Emu(9300000))
tb(s, L, 5830000, W, 500000,
   "pass@8 đo “model còn giải được bài không nếu cho thử 8 lần”. Thiết kế gộp mất 22–26 điểm;\n"
   "cô lập xong thì đi ngang. Phần “mất năng lực” đến từ cách đo, không phải từ verifier.",
   size=12.5, color=BODY, line_spacing=1.4)

# =========================================================== 9 · chart: control
s = new()
header(s, 8, "ĐỐI CHỨNG QUYẾT ĐỊNH", "Vá verifier không thay đổi bất cứ điều gì")
s.shapes.add_picture(f"{FIG}/deck_control.png", Emu((SW - 9300000) // 2), Emu(1720000),
                     width=Emu(9300000))
tb(s, L, 5660000, W, 700000,
   "Hai đường nằm chồng lên nhau ở cả hai seed. Vá đúng chỗ verifier lệch — thứ mà cả đề tài đặt giả\n"
   "thuyết là nguyên nhân — không tạo ra khác biệt đo được.",
   size=12.5, color=BODY, line_spacing=1.4)
tb(s, L, 6400000, W, 300000,
   "Đề thi 150 đề, 1 đề ≈ 0,67 điểm. Khoảng cách A–B lớn nhất là 0,6 điểm — đúng một đề.",
   size=10, color=MUTED)

# =========================================================== 10 · why (dark)
s = new()
bg(s, DARK)
tb(s, L, 430000, 7000000, 250000, "VÌ SAO", size=10.5, bold=True, color=RGBColor(0xE8, 0x8A, 0x92))
tb(s, L, 830000, W, 620000, "Mức độ nặng khác với tần suất xảy ra",
   size=29, font=DISPLAY, bold=True, color=WHITE)
for i, (big, cap) in enumerate([
    ("100%", "tỉ lệ máy chấm gạch SAI\nkhi gặp \\dfrac — nghe rất nặng"),
    ("0,55%", "nhưng cách viết đó chỉ xuất hiện\n22/4000 lời giải. GSM8K: 0 lần"),
    ("0,55%", "nhân hai số — phần tập train bị\nloại oan. Không thể gây sụp 20 điểm"),
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
   "Đo trực tiếp: ở vòng 0 model chưa học gì, A và B sinh ra ĐÚNG CÙNG bộ lời giải — khác nhau duy nhất là\n"
   "verifier nào chấm. Bản vá đổi kết quả của 0 đề (seed 0) và 1 đề (seed 1) trên 150 đề.",
   size=13, color=RGBColor(0xD6, 0xD7, 0xDC), line_spacing=1.45)
tb(s, L, 5750000, W, 400000,
   "Các con số “verifier sai X%” trong bài báo khác đều là mức-nặng-có-điều-kiện. Tác động thật = mức nặng × tần suất.",
   size=12.5, bold=True, color=RGBColor(0xFF, 0xC9, 0x4D))

# =========================================================== 11 · pivot
s = new()
header(s, 10, "ĐỀ TÀI THU HẸP LẠI", "Từ ‘phát hiện cơ chế gây hại’ sang ‘cảnh báo cách đo’")
panel(s, L - 120000, 1950000, 5100000, 3120000)
pill(s, L + 120000, 2150000, "ĐÃ BỊ BÁC BỎ", fill=MUTED, width=1500000, height=300000)
tb(s, L + 120000, 2650000, 4700000, 900000,
   "“Verifier lệch vì văn phong gây\nsụp năng lực trong self-training\nlặp vòng.”",
   size=15, font=DISPLAY, bold=True, color=MUTED, line_spacing=1.3)
tb(s, L + 120000, 3950000, 4700000, 800000,
   "Bị bác bỏ bởi chính thí nghiệm đối chứng\ndựng ra để kiểm tra nó — đo trực tiếp,\n2 lần lặp độc lập.",
   size=12, color=MUTED, line_spacing=1.35)

panel(s, L + 5400000, 1950000, 5310000, 3120000, fill=RGBColor(0xF0, 0xF6, 0xFA))
pill(s, L + 5640000, 2150000, "TUYÊN BỐ MỚI", fill=BLUE, width=1600000, height=300000)
tb(s, L + 5640000, 2650000, 4800000, 900000,
   "“Gộp nhiều bộ đề vào một lần train,\ncộng với chấm điểm trên chính đề đã\nhọc, đủ để tạo ra hiện tượng ‘sụp’ giả.”",
   size=15, font=DISPLAY, bold=True, color=INK, line_spacing=1.3)
tb(s, L + 5640000, 3950000, 4800000, 800000,
   "Kèm quy tắc đọc số: tác động thật của một\nlỗi verifier = mức nặng × tần suất, và tần\nsuất phải đo trong chính pipeline của mình.",
   size=12, color=BODY, line_spacing=1.35)

tb(s, L, 5330000, W, 700000,
   "Phạm vi hẹp hơn dự tính ban đầu, nhưng trung thực và tra lại được — và cái bẫy phương pháp này đang\n"
   "khá phổ biến, nên vẫn là đóng góp dùng lại được.",
   size=13, color=BODY, line_spacing=1.4)

# =========================================================== 12 · open question
s = new()
header(s, 11, "CÂU HỎI CÒN MỞ", "Một khả năng chưa loại trừ được")
tb(s, L, 1620000, W, 700000,
   "Trong cả 7 lần chạy, pass@1 luôn rớt ~3 điểm ở vòng 1 rồi đứng yên. Nhưng STaR, RFT, ReST-EM\n"
   "đều báo cáo self-training làm model KHÁ LÊN. Vì sao của em ngược?",
   size=14, color=INK, line_spacing=1.4)
panel(s, L - 120000, 2550000, W + 240000, 820000)
tb(s, L + 120000, 2720000, W - 240000, 550000,
   "Cách giải thích tầm thường chưa loại trừ: model đã được tinh chỉnh kỹ sẵn. Một lần SFT ngắn (~40 bước)\n"
   "có thể chỉ làm nó xê dịch khỏi trạng thái đã tinh chỉnh — bất kể dạy nó bằng dữ liệu gì.",
   size=12.5, color=BODY, line_spacing=1.4)
tb(s, L, 3650000, W, 300000, "THÍ NGHIỆM PHÂN ĐỊNH — đã viết code xong, đang chờ GPU",
   size=11, bold=True, color=MUTED)
for i, (colour, lbl, txt) in enumerate([
    (GREEN, "Nếu KHÁ LÊN", "vòng lặp lành mạnh → “học từ output của chính mình”\nđúng là cái gây hại. Đề tài có phát hiện dương."),
    (ORANGE, "Nếu CŨNG RỚT", "cú rớt là chi phí của SFT, không phải của self-training\n→ phải viết lại kết luận lần nữa."),
]):
    x = L + i * 5400000
    panel(s, x, 4100000, 5190000, 1350000)
    pill(s, x + 240000, 4280000, lbl, fill=colour, width=1700000, height=310000)
    tb(s, x + 240000, 4750000, 4700000, 600000, txt, size=12, color=BODY, line_spacing=1.35)
tb(s, L, 5750000, W, 300000,
   "Chạy lại đúng vòng lặp nhưng dạy bằng lời giải mẫu của bộ đề, thay vì lời giải model tự sinh.",
   size=10.5, color=MUTED)

# =========================================================== 13 · limitations
s = new()
header(s, 12, "THẢO LUẬN", "Giới hạn — nói trước, không giấu")
lim = [
    ("Đề thi chỉ 150 đề",
     "Một đề ≈ 0,67 điểm. Riêng việc đổi cách bốc đề thi đã làm điểm vòng 0 lệch 4,7 điểm — lớn hơn cả hiệu ứng đang đo."),
    ("Chỉ mới 2 lần lặp cho A và B",
     "C và các lần chạy cũ mới 1 lần. Chưa đủ để nói chắc về cú rớt 12,7 điểm của GSM8K."),
    ("So sánh cũ–mới đổi 3 thứ cùng lúc",
     "Bỏ gộp, thêm đề thi riêng, giảm số đề. Nên kết luận bác bỏ chỉ dựa trên so sánh A với B — hai lần chạy giống hệt, khác đúng một biến."),
]
y = 2000000
for i, (h, d) in enumerate(lim, 1):
    panel(s, L - 120000, y, W + 240000, 1150000)
    tb(s, L + 120000, y + 200000, 400000, 300000, f"{i:02d}", size=13,
       font=DISPLAY, bold=True, color=CRIMSON)
    tb(s, L + 700000, y + 190000, 9500000, 300000, h, size=14, bold=True, color=INK)
    tb(s, L + 700000, y + 600000, 9500000, 450000, d, size=12, color=BODY, line_spacing=1.3)
    y += 1330000

# =========================================================== 14 · summary
s = new()
header(s, 13, "TÓM TẮT", "Hai tuần, và việc tiếp theo")
panel(s, L - 120000, 1900000, W + 240000, 1460000, fill=RGBColor(0xF0, 0xF6, 0xFA))
tb(s, L + 120000, 2100000, W - 240000, 900000,
   "Thí nghiệm đối chứng bác bỏ giả thuyết trung tâm của đề tài. Nguyên nhân đã đo được: lỗi verifier\n"
   "tuy nặng 100% nhưng chỉ xảy ra ở 0,55% lời giải. Đề tài chuyển sang cảnh báo về cách đo —\n"
   "hẹp hơn, nhưng đứng vững.",
   size=14, font=DISPLAY, color=INK, line_spacing=1.4)
for i, (lbl, txt) in enumerate([
    ("ĐÃ LÀM", "7 lần chạy (~40 giờ GPU), phát hiện và sửa lỗ hổng thiết kế đo, dựng thí nghiệm đối chứng."),
    ("KẾT QUẢ", "bác bỏ giả thuyết ban đầu, và đo được nguyên nhân vì sao nó không đúng."),
    ("PHÁT HIỆN", "mức-nặng × tần-suất — quy tắc đọc lại mọi con số verifier-bias, kể cả của bài khác."),
    ("ĐANG CHẠY", "thí nghiệm phân định “chi phí SFT” với “tác hại của self-training”."),
]):
    yy = 3560000 + i * 570000
    tb(s, L, yy, 1700000, 300000, lbl, size=11, bold=True, color=CRIMSON)
    tb(s, L + 1800000, yy - 15000, 8700000, 330000, txt, size=12.5, color=BODY)
rule(s, L, 5850000, W)
tb(s, L, 6050000, W, 300000, "Cảm ơn thầy đã theo dõi — rất mong nhận góp ý.",
   size=12.5, color=MUTED)

prs.save(OUT)
print("saved", OUT, "| slides:", len(prs.slides._sldIdLst))
