"""Week-3 progress deck — matches the week-2 deck's design system exactly.

Design constants were recovered by introspecting
BaoCaoTienDo_Tuan2_52300057_52300006.pptx, so the two decks read as one series.
"""

from pptx import Presentation
from pptx.util import Emu, Pt
from pptx.dml.color import RGBColor
from pptx.enum.text import PP_ALIGN

OUT = "/Users/tsangcuteso1/Documents/GitHub/DACNTT_2026/BaoCaoTienDo_Tuan3_52300057_52300006.pptx"

RED = RGBColor(0x7A, 0x1F, 0x2B)
INK = RGBColor(0x2A, 0x25, 0x1D)
MUTED = RGBColor(0x5C, 0x54, 0x47)
GOLD = RGBColor(0x9C, 0x77, 0x2B)
FONT = "Cambria"

L = 777240                # left margin
W = 10637215              # content width
KICKER = "TUẦN 3 — GIẢ THUYẾT BỊ BÁC BỎ, THU HẸP PHẠM VI ĐỀ TÀI"

prs = Presentation()
prs.slide_width = Emu(12191695)
prs.slide_height = Emu(6858000)
BLANK = prs.slide_layouts[6]


def tb(slide, left, top, width, height, text, *, size, bold=False, color=INK,
       align=PP_ALIGN.LEFT, spacing=None):
    box = slide.shapes.add_textbox(Emu(left), Emu(top), Emu(width), Emu(height))
    tf = box.text_frame
    tf.word_wrap = True
    lines = text.split("\n")
    for i, line in enumerate(lines):
        para = tf.paragraphs[0] if i == 0 else tf.add_paragraph()
        para.alignment = align
        if spacing:
            para.space_after = Pt(spacing)
        run = para.add_run()
        run.text = line
        run.font.name = FONT
        run.font.size = Pt(size)
        run.font.bold = bold
        run.font.color.rgb = color
    return box


def rule(slide, left, top, width):
    from pptx.enum.shapes import MSO_CONNECTOR
    c = slide.shapes.add_connector(MSO_CONNECTOR.STRAIGHT, Emu(left), Emu(top),
                                   Emu(left + width), Emu(top))
    c.line.color.rgb = RGBColor(0xD8, 0xD2, 0xC6)
    c.line.width = Pt(0.75)
    return c


def vrule(slide, left, top, height):
    from pptx.enum.shapes import MSO_CONNECTOR
    c = slide.shapes.add_connector(MSO_CONNECTOR.STRAIGHT, Emu(left), Emu(top),
                                   Emu(left), Emu(top + height))
    c.line.color.rgb = GOLD
    c.line.width = Pt(1.5)
    return c


def header(slide, num, label, title):
    tb(slide, L, 320040, 7315200, 274320, KICKER, size=9.5, color=MUTED)
    tb(slide, 10042855, 320040, 1371600, 274320, f"{num:02d}", size=9.5, color=MUTED)
    rule(slide, L, 621792, W)
    tb(slide, L, 777240, W, 320040, label, size=13, bold=True, color=RED)
    tb(slide, L, 1078992, W, 868680, title, size=27, bold=True, color=INK)


def footnote(slide, text):
    tb(slide, L, 6355080, W, 365760, text, size=9.5, color=MUTED)


def new():
    return prs.slides.add_slide(BLANK)


# ---------------------------------------------------------------- 1. title
s = new()
rule(s, L, 822960, 1005840)
tb(s, L, 960120, W, 365760, "BÁO CÁO TIẾN ĐỘ TUẦN 3", size=14, bold=True, color=RED)
tb(s, L, 1554480, 10515600, 1750000,
   "Giả thuyết trung tâm bị bác bỏ bằng\nthí nghiệm đối chứng — và vì sao",
   size=32, bold=True, color=INK)
rule(s, L, 3400000, 10607040)
tb(s, L, 3620000, 10515600, 1100000,
   "Tuần 3: chạy 5 thí nghiệm cô lập, thêm đối chứng có kiểm soát biến. Kết quả không\n"
   "ủng hộ giả thuyết ban đầu. Báo cáo này trình bày bằng chứng, nguyên nhân, và\n"
   "phạm vi đề tài được thu hẹp lại như thế nào.",
   size=16, color=MUTED, spacing=6)
tb(s, L, 5806440, 8229600, 548640, "Nguyễn Tấn Sang   ·   12 tháng 9, 2026",
   size=13, bold=True, color=INK)

# ---------------------------------------------------------------- 2. agenda
s = new()
header(s, 1, "NỘI DUNG", "Những gì trình bày hôm nay")
items = [
    "Nhắc lại: tuần 2 dừng ở đâu và nghi ngờ điều gì",
    "Đã chạy gì tuần này — 5 thí nghiệm cô lập, có đối chứng",
    "Kết quả: cú sụp không tái lập khi đo đúng cách",
    "Đối chứng quyết định: vá verifier không thay đổi gì",
    "Vì sao — mức độ nặng khác với tần suất xảy ra",
    "Đề tài thu hẹp lại ra sao, và việc còn phải làm",
]
y = 2057399
for i, t in enumerate(items, 1):
    tb(s, L, y, 548640, 420000, f"{i:02d}", size=14, bold=True, color=GOLD)
    tb(s, 1417320, y, 9997135, 420000, t, size=14.5, color=INK)
    rule(s, 1417320, y + 480000, 9997135)
    y += 620000

# ------------------------------------------------- 3. recap week 2
s = new()
header(s, 2, "NHẮC LẠI TUẦN 2", "Nghi ngờ: hai bộ đề bị trộn chung khi train")
vrule(s, L, 1920239, 1150000)
tb(s, 1033272, 1874519, 10381183, 1100000,
   "“Tuần 2 báo cáo: model sụp mạnh qua 5 vòng. Nhưng tập train mỗi vòng luôn\n"
   "nghiêng ~69% về GSM8K — một adapter chung học chủ yếu từ bộ này rồi áp cho\n"
   "cả hai. Chưa tách được ‘tại verifier lệch’ khỏi ‘tại lây từ bộ đề kia’.”",
   size=15, color=INK, spacing=4)
rule(s, L, 3450000, W)
tb(s, L, 3700000, W, 400000,
   "Tuần 3 đặt ra hai việc phải làm cho dứt điểm:", size=13, bold=True, color=MUTED)
for i, (h, d) in enumerate([
    ("Cô lập từng bộ đề", "Mỗi bộ đề chạy riêng, adapter riêng — hết nhiễm chéo."),
    ("Tách đề thi riêng", "30% đề giữ lại làm đề thi, chưa từng dùng để chọn bài train."),
    ("Thêm đối chứng thật", "Chạy lại y hệt, chỉ vá verifier — đúng một biến khác nhau."),
]):
    x = L + i * 3579000
    tb(s, x, 4200000, 3400000, 400000, h, size=15, bold=True, color=GOLD)
    tb(s, x, 4650000, 3400000, 1100000, d, size=12.5, color=INK, spacing=3)
footnote(s, "Chi tiết nghi ngờ nhiễm chéo đã trình bày ở báo cáo tuần 2.")

# ------------------------------------------------- 4. what was run
s = new()
header(s, 3, "ĐÃ CHẠY GÌ", "Năm lần chạy trên Kaggle, cùng một cấu hình gốc")
tb(s, L, 1947672, W, 420000,
   "Tất cả: Qwen2.5-1.5B, 500 đề, 5 vòng, k=8, tách 30% đề thi. Chỉ khác đúng cột được in đậm.",
   size=12.5, color=MUTED)
cols = [(L, 2600000, "Lần chạy"), (3400000, 2500000, "Bộ đề"),
        (5900000, 2500000, "Verifier"), (8400000, 1500000, "Seed"),
        (9900000, 1500000, "GPU")]
for x, w, h in cols:
    tb(s, x, 2500000, w, 420000, h, size=12, bold=True, color=GOLD)
rule(s, L, 2920000, W)
rows = [
    ("A", "MATH-500", "gốc", "0", "~5 giờ"),
    ("A — lặp lại", "MATH-500", "gốc", "1", "~5 giờ"),
    ("B  (đối chứng)", "MATH-500", "ĐÃ VÁ", "0", "~5 giờ"),
    ("B — lặp lại", "MATH-500", "ĐÃ VÁ", "1", "~5 giờ"),
    ("C", "GSM8K", "gốc", "0", "~5,5 giờ"),
]
y = 2920000
for name, ds, vf, sd, gpu in rows:
    bold = "VÁ" in vf
    for (x, w, _), val in zip(cols, (name, ds, vf, sd, gpu)):
        tb(s, x, y + 60000, w, 420000, val, size=12,
           bold=(bold and val == vf), color=INK)
    y += 480000
    rule(s, L, y, W)
tb(s, L, y + 180000, W, 900000,
   "A và B khác nhau đúng MỘT biến: verifier có được vá hay không. Đây là thí nghiệm đối chứng\n"
   "mà thiết kế cũ không thể có — và là phép thử trực tiếp cho giả thuyết của đề tài.",
   size=12.5, color=INK, spacing=4)
footnote(s, "Tổng ~25 giờ GPU Kaggle, chia nhiều phiên; kết quả lưu sau mỗi vòng để không mất khi phiên bị ngắt.")

# ------------------------------------------------- 5. collapse gone
s = new()
header(s, 4, "KẾT QUẢ CHÍNH", "Cú sụp không tái lập khi đo đúng cách")
hdr = [(L, 3200000, "Đo trên"), (3977240, 2300000, "pass@1 vòng 0→4"),
       (6277240, 2300000, "pass@8 vòng 0→4"), (8577240, 2800000, "Kết luận")]
for x, w, h in hdr:
    tb(s, x, 2000000, w, 420000, h, size=12, bold=True, color=GOLD)
rule(s, L, 2420000, W)
data = [
    ("Thiết kế CŨ — gộp, GSM8K", "69,6% → 26,6%", "91,4% → 65,8%", "sụp nặng"),
    ("Thiết kế CŨ — gộp, MATH-500", "30,4% → 10,6%", "53,8% → 31,4%", "sụp nặng"),
    ("A — MATH-500 cô lập", "32,0% → 29,3%", "57,3% → 56,0%", "KHÔNG sụp"),
    ("A — lặp lại seed khác", "36,7% → 33,3%", "58,7% → 58,7%", "KHÔNG sụp"),
    ("C — GSM8K cô lập", "66,7% → 54,0%", "92,7% → 90,0%", "pass@8 giữ nguyên"),
]
y = 2420000
for i, (a, b, c, d) in enumerate(data):
    strong = i >= 2
    for (x, w, _), val, bold in zip(hdr, (a, b, c, d), (False, False, False, strong)):
        tb(s, x, y + 60000, w, 420000, val, size=11.5, bold=bold,
           color=INK if strong else MUTED)
    y += 470000
    rule(s, L, y, W)
tb(s, L, y + 180000, W, 950000,
   "Cột pass@8 là cột quan trọng: nó đo “model còn giải được bài không nếu cho thử 8 lần”.\n"
   "Thiết kế cũ mất 22–26 điểm. Cô lập xong, pass@8 gần như đứng yên ở cả ba lần chạy.\n"
   "Phần “mất năng lực” biến mất — nó đến từ cách đo, không phải từ verifier.",
   size=12.5, color=INK, spacing=4)

# ------------------------------------------------- 6. the control
s = new()
header(s, 5, "ĐỐI CHỨNG QUYẾT ĐỊNH", "Vá verifier không thay đổi bất cứ điều gì")
tb(s, L, 1947672, W, 400000,
   "A và B giống hệt nhau mọi mặt, chỉ khác: B đã vá đúng chỗ verifier chấm sai.",
   size=13, color=MUTED)
hdr = [(L, 2600000, "pass@1 mỗi vòng"), (3400000, 1500000, "Vòng 0"),
       (4900000, 1500000, "1"), (6400000, 1500000, "2"),
       (7900000, 1500000, "3"), (9400000, 1500000, "4")]
for x, w, h in hdr:
    tb(s, x, 2450000, w, 420000, h, size=11.5, bold=True, color=GOLD)
rule(s, L, 2870000, W)
y = 2870000
for name, vals, bold in [
    ("A seed 0 — verifier gốc", ("32,0%", "29,3%", "28,0%", "29,3%", "29,3%"), False),
    ("B seed 0 — ĐÃ VÁ", ("32,0%", "28,7%", "28,7%", "28,7%", "28,7%"), True),
    ("A seed 1 — verifier gốc", ("36,7%", "32,7%", "32,7%", "31,3%", "33,3%"), False),
    ("B seed 1 — ĐÃ VÁ", ("37,3%", "32,0%", "32,7%", "31,3%", "33,3%"), True),
]:
    tb(s, L, y + 55000, 2600000, 420000, name, size=11.5, bold=bold, color=INK)
    for (x, w, _), v in zip(hdr[1:], vals):
        tb(s, x, y + 55000, w, 420000, v, size=11.5, bold=bold, color=INK)
    y += 460000
    rule(s, L, y, W)
tb(s, L, y + 170000, W, 1000000,
   "Hai đường gần như trùng nhau. Ở seed 1, từ vòng 2 trở đi con số GIỐNG HỆT nhau.\n"
   "Vá đúng chỗ verifier lệch — thứ mà cả đề tài đặt giả thuyết là nguyên nhân — không tạo ra\n"
   "khác biệt đo được, ở cả hai lần lặp độc lập.",
   size=12.5, color=INK, spacing=4)
footnote(s, "Đề thi 150 đề, nên 1 đề ≈ 0,67 điểm phần trăm. Khoảng cách A–B lớn nhất là 0,6 điểm — đúng một đề.")

# ------------------------------------------------- 7. severity x prevalence
s = new()
header(s, 6, "VÌ SAO", "Mức độ nặng khác với tần suất xảy ra")
tb(s, L, 1947672, W, 900000,
   "Đây là phần em thấy giá trị nhất tuần này: không chỉ biết “vá không có tác dụng”,\n"
   "mà đo được vì sao nó không có tác dụng.",
   size=13.5, color=INK, spacing=4)
rule(s, L, 2800000, W)
for i, (big, cap) in enumerate([
    ("100%", "Tỉ lệ verifier chấm SAI khi gặp\ncách viết \\dfrac — đo bằng thực nghiệm.\nNghe rất nặng."),
    ("0,55%", "Nhưng cách viết đó chỉ xuất hiện\n22/4000 lời giải mỗi vòng.\nTrên GSM8K: 0 lần."),
    ("0,55%", "Nhân hai số lại — đó mới là phần\ntập train bị loại oan mỗi vòng.\nKhông thể gây sụp 20 điểm."),
]):
    x = L + i * 3579000
    tb(s, x, 3050000, 3400000, 700000, big, size=40, bold=True, color=GOLD)
    tb(s, x, 3850000, 3400000, 1300000, cap, size=12, color=INK, spacing=3)
rule(s, L, 5300000, W)
tb(s, L, 5480000, W, 800000,
   "Đo trực tiếp: ở vòng 0 model chưa học gì, A và B sinh ra ĐÚNG CÙNG bộ lời giải — khác nhau duy nhất\n"
   "là verifier nào chấm. Bản vá đổi kết quả của 0 đề (seed 0) và 1 đề (seed 1) trên 150 đề.",
   size=12, color=MUTED, spacing=4)

# ------------------------------------------------- 8. pivot
s = new()
header(s, 7, "ĐỀ TÀI THU HẸP LẠI", "Từ ‘phát hiện cơ chế gây hại’ sang ‘cảnh báo cách đo’")
tb(s, L, 1947672, 5100000, 400000, "TUYÊN BỐ CŨ — đã bị bác bỏ", size=12, bold=True, color=RED)
tb(s, L, 2400000, 5100000, 1500000,
   "“Verifier lệch vì văn phong gây sụp\nnăng lực trong self-training lặp vòng.”",
   size=15, bold=True, color=MUTED, spacing=4)
tb(s, L, 3900000, 5100000, 1400000,
   "Bị bác bỏ bởi chính thí nghiệm đối chứng\ndựng ra để kiểm tra nó. Không phải suy\nluận gián tiếp — đo trực tiếp, 2 lần lặp.",
   size=12, color=MUTED, spacing=3)
vrule(s, 6100000, 1947672, 3400000)
tb(s, 6400000, 1947672, 5000000, 400000, "TUYÊN BỐ MỚI — được số liệu chống lưng", size=12, bold=True, color=RED)
tb(s, 6400000, 2400000, 5000000, 1500000,
   "“Gộp nhiều bộ đề vào một lần train, cộng\nvới chấm điểm trên chính đề đã học, đủ\nđể tạo ra một hiện tượng ‘sụp’ giả.”",
   size=15, bold=True, color=INK, spacing=4)
tb(s, 6400000, 3900000, 5000000, 1400000,
   "Kèm quy tắc đọc số: các con số “verifier sai\nX%” trong bài báo khác là mức-nặng-có-điều-kiện.\nTác động thật = mức nặng × tần suất.",
   size=12, color=INK, spacing=3)
rule(s, L, 5500000, W)
tb(s, L, 5680000, W, 700000,
   "Phạm vi hẹp hơn dự tính ban đầu, nhưng trung thực và tra lại được — và cái bẫy phương pháp này\n"
   "đang khá phổ biến, nên vẫn là đóng góp dùng lại được.",
   size=12.5, color=INK, spacing=4)

# ------------------------------------------------- 9. open question
s = new()
header(s, 8, "CÂU HỎI CÒN MỞ", "Một khả năng chưa loại trừ được — đang chạy để kiểm tra")
tb(s, L, 1947672, W, 1000000,
   "Trong cả 7 lần chạy, pass@1 luôn rớt ~3 điểm ở vòng 1 rồi đứng yên. Nhưng các bài báo\n"
   "lớn (STaR, RFT, ReST-EM) đều báo cáo self-training làm model KHÁ LÊN. Vì sao của em ngược?",
   size=13.5, color=INK, spacing=4)
rule(s, L, 3000000, W)
tb(s, L, 3200000, W, 400000,
   "Có một cách giải thích tầm thường chưa loại trừ được:", size=12.5, bold=True, color=MUTED)
tb(s, L, 3650000, W, 700000,
   "Model đã được tinh chỉnh kỹ sẵn. Một lần SFT ngắn (~40 bước) có thể chỉ đơn giản làm nó\n"
   "xê dịch khỏi trạng thái đã tinh chỉnh — bất kể dạy nó bằng dữ liệu gì.",
   size=13, color=INK, spacing=4)
tb(s, L, 4500000, W, 400000,
   "Thí nghiệm phân định (đã viết code xong, đang chờ GPU):", size=12.5, bold=True, color=MUTED)
for i, (lbl, txt) in enumerate([
    ("Nếu KHÁ LÊN", "vòng lặp lành mạnh → “học từ output của chính mình” đúng là cái gây hại."),
    ("Nếu CŨNG RỚT", "cú rớt là chi phí của SFT, không phải của self-training → phải viết lại lần nữa."),
]):
    yy = 4950000 + i * 620000
    tb(s, L, yy, 2200000, 420000, lbl, size=12.5, bold=True, color=GOLD)
    tb(s, 3100000, yy, 8300000, 420000, txt, size=12.5, color=INK)
footnote(s, "Chạy lại đúng vòng lặp nhưng dạy bằng lời giải mẫu của bộ đề, thay vì lời giải model tự sinh.")

# ------------------------------------------------- 10. limitations
s = new()
header(s, 9, "THẢO LUẬN", "Giới hạn — nói trước, không giấu")
lim = [
    ("Đề thi chỉ 150 đề", "Một đề ≈ 0,67 điểm. Riêng việc đổi cách bốc đề thi đã làm điểm vòng 0 lệch 4,7 điểm — lớn hơn cả hiệu ứng đang đo."),
    ("Chỉ mới 2 lần lặp cho A và B", "C và các lần chạy cũ mới 1 lần. Chưa đủ để nói chắc về cú rớt 12,7 điểm của GSM8K."),
    ("So sánh cũ–mới đổi 3 thứ cùng lúc", "Bỏ gộp, thêm đề thi riêng, giảm số đề. Nên kết luận bác bỏ chỉ dựa trên so sánh A với B — hai lần chạy giống hệt, khác đúng một biến."),
]
y = 1947672
for h, d in lim:
    tb(s, L, y, W, 400000, h, size=14, bold=True, color=INK)
    tb(s, L, y + 420000, W, 700000, d, size=12.5, color=MUTED, spacing=3)
    rule(s, L, y + 1180000, W)
    y += 1350000

# ------------------------------------------------- 11. summary
s = new()
header(s, 10, "TÓM TẮT", "Tuần 3 và việc tiếp theo")
vrule(s, L, 1920000, 1150000)
tb(s, 1033272, 1880000, 10381183, 1150000,
   "“Thí nghiệm đối chứng bác bỏ giả thuyết trung tâm của đề tài. Nguyên nhân đã đo được:\n"
   "lỗi verifier tuy nặng 100% nhưng chỉ xảy ra ở 0,55% lời giải. Đề tài chuyển sang cảnh\n"
   "báo về cách đo — hẹp hơn, nhưng đứng vững.”",
   size=15, color=INK, spacing=4)
for i, t in enumerate([
    "—  Đã làm: 5 lần chạy cô lập có đối chứng, ~25 giờ GPU; bác bỏ giả thuyết và đo được nguyên nhân.",
    "—  Phát hiện: mức-nặng × tần-suất — quy tắc đọc lại mọi con số verifier-bias, kể cả của bài khác.",
    "—  Đang chạy: thí nghiệm phân định “chi phí SFT” với “tác hại của self-training”.",
    "—  Bài báo: đã viết lại toàn bộ theo kết luận mới, chờ số liệu cuối để khoá bảng kết quả.",
]):
    tb(s, L, 3350000 + i * 620000, W, 600000, t, size=12.5, bold=True, color=GOLD)
tb(s, L, 5950000, W, 400000,
   "Cảm ơn thầy đã theo dõi — rất mong nhận góp ý.", size=13, color=MUTED)

prs.save(OUT)
print("saved", OUT, "| slides:", len(prs.slides._sldIdLst))
