// Tạo BaoCaoThucNghiem_20261011.docx (báo cáo tiến độ thực nghiệm gửi giảng viên).
// Chạy: NODE_PATH=<thư mục có node_modules/docx> node tools/make_report_20261011.js BaoCaoThucNghiem_20261011.docx
const fs = require("fs");
const {
  Document, Packer, Paragraph, TextRun, Table, TableRow, TableCell, WidthType, AlignmentType,
  BorderStyle, ShadingType, HeadingLevel, LevelFormat, Footer, PageNumber, VerticalAlign,
} = require("docx");

const FONT = "Times New Roman";
const W = 9026;

function runs(text, base = {}) {
  const out = [];
  const re = /(\*\*[^*]+\*\*)/g;
  let last = 0, m;
  while ((m = re.exec(text))) {
    if (m.index > last) out.push(new TextRun({ text: text.slice(last, m.index), font: FONT, size: 24, ...base }));
    out.push(new TextRun({ text: m[0].slice(2, -2), bold: true, font: FONT, size: 24, ...base }));
    last = m.index + m[0].length;
  }
  if (last < text.length) out.push(new TextRun({ text: text.slice(last), font: FONT, size: 24, ...base }));
  return out;
}
const P = (t, o = {}) => new Paragraph({ spacing: { after: 120, line: 300 }, alignment: AlignmentType.JUSTIFIED, ...o, children: runs(t) });
const H1 = (t) => new Paragraph({ heading: HeadingLevel.HEADING_1, spacing: { before: 280, after: 120 }, keepNext: true,
  children: [new TextRun({ text: t, bold: true, font: FONT, size: 28 })] });
const H2 = (t) => new Paragraph({ heading: HeadingLevel.HEADING_2, spacing: { before: 200, after: 100 }, keepNext: true,
  children: [new TextRun({ text: t, bold: true, font: FONT, size: 25 })] });
const B = (t) => new Paragraph({ numbering: { reference: "bul", level: 0 }, spacing: { after: 80, line: 290 },
  alignment: AlignmentType.JUSTIFIED, children: runs(t) });

const thin = { style: BorderStyle.SINGLE, size: 4, color: "808080" };
const borders = { top: thin, bottom: thin, left: thin, right: thin };
const none = { style: BorderStyle.NONE, size: 0, color: "FFFFFF" };
const noBorders = { top: none, bottom: none, left: none, right: none };
const L = AlignmentType.LEFT;

function cell(text, w, { head = false, align = AlignmentType.CENTER } = {}) {
  return new TableCell({
    width: { size: w, type: WidthType.DXA }, borders, verticalAlign: VerticalAlign.CENTER,
    shading: head ? { type: ShadingType.CLEAR, fill: "E7ECF2", color: "auto" } : undefined,
    margins: { top: 60, bottom: 60, left: 90, right: 90 },
    children: [new Paragraph({ alignment: align, spacing: { after: 0 }, children: runs(text, { size: 21, bold: head }) })],
  });
}
function table(cols, header, rows, aligns) {
  const total = cols.reduce((a, b) => a + b, 0);
  return new Table({
    width: { size: total, type: WidthType.DXA }, columnWidths: cols,
    rows: [
      new TableRow({ tableHeader: true, children: header.map((h, i) => cell(h, cols[i], { head: true })) }),
      ...rows.map((r) => new TableRow({ cantSplit: true, children: r.map((c, i) => cell(c, cols[i], { align: aligns[i] || AlignmentType.CENTER })) })),
    ],
  });
}
const gap = () => new Paragraph({ spacing: { after: 100 }, children: [] });
const caption = (t) => new Paragraph({ spacing: { before: 60, after: 160 }, children: [new TextRun({ text: t, italics: true, font: FONT, size: 21 })] });
function kv(k, v) {
  return new TableRow({ children: [
    new TableCell({ width: { size: 2300, type: WidthType.DXA }, borders: noBorders, margins: { top: 40, bottom: 40, left: 0, right: 90 },
      children: [new Paragraph({ spacing: { after: 0 }, children: [new TextRun({ text: k, bold: true, font: FONT, size: 24 })] })] }),
    new TableCell({ width: { size: W - 2300, type: WidthType.DXA }, borders: noBorders, margins: { top: 40, bottom: 40, left: 90, right: 0 },
      children: [new Paragraph({ spacing: { after: 0 }, children: [new TextRun({ text: v, font: FONT, size: 24 })] })] }),
  ] });
}

const children = [
  new Paragraph({ alignment: AlignmentType.CENTER, spacing: { after: 40 }, children: [new TextRun({ text: "TRƯỜNG ĐẠI HỌC TÔN ĐỨC THẮNG", bold: true, font: FONT, size: 26 })] }),
  new Paragraph({ alignment: AlignmentType.CENTER, spacing: { after: 240 }, children: [new TextRun({ text: "[Tên môn học / mã đề tài]", font: FONT, size: 24 })] }),
  new Paragraph({ alignment: AlignmentType.CENTER, spacing: { after: 120 }, children: [new TextRun({ text: "BÁO CÁO TIẾN ĐỘ THỰC NGHIỆM", bold: true, font: FONT, size: 34 })] }),
  new Paragraph({ alignment: AlignmentType.CENTER, spacing: { after: 280, line: 280 },
    children: [new TextRun({ text: "Đề tài: Verifier Bias Is Not Enough: A Controlled Re-examination of Capability Collapse in Iterative Self-Training of Small Reasoning Models", italics: true, font: FONT, size: 24 })] }),
  new Table({ width: { size: W, type: WidthType.DXA }, columnWidths: [2300, W - 2300], rows: [
    kv("Kính gửi", "Thầy/Cô [Tên giảng viên hướng dẫn]"),
    kv("Sinh viên thực hiện", "Nguyễn Tấn Sang (52300057) — Trần Duy Anh (52300006)"),
    kv("Đơn vị", "Trường Đại học Tôn Đức Thắng, TP. Hồ Chí Minh"),
    kv("Ngày báo cáo", "11/10/2026"),
  ] }),
  gap(),

  P("Em xin gửi Thầy/Cô báo cáo tiến độ tuần này. Tuần trước em báo nghi vấn learning rate 1e-5 quá thấp để model học được. Tuần này em đã chạy lại ở nhiều mức learning rate, và **kết quả làm thay đổi một phần kết luận của bài báo**. Báo cáo gồm: kết quả chính, số liệu mới, những gì đã sửa trong bài, và điều em xin trao đổi."),

  H1("1. Kết quả chính tuần này"),
  B("**“Đường cong phẳng” trước đây là do model chưa được huấn luyện thật.** Ở learning rate 1e-5, loss gần như không giảm (0,84 → 0,72). Khi tăng learning rate, mức giảm độ chính xác tăng dần: ở 1e-4 (ba seed) độ chính xác mẫu ở vòng 2 giảm trung bình 2,0 điểm (trong phạm vi nhiễu); ở 2e-4 (hai seed) giảm 3,7 điểm; ở 5e-4 (hai seed) giảm 6,5 điểm, và cả 4 lần chạy A/B đều giảm pass@4 từ 2,0 đến 11,3 điểm."),
  B("**Bản vá verifier vẫn không có tác dụng nhất quán.** Ở 5e-4, seed 1 cho Run B (đã vá) cao hơn Run A 5,4 điểm pass@1 ở vòng 2; seed 2 lại thấp hơn 7,3 điểm. Dấu đổi theo seed nên chênh lệch này là nhiễu."),
  B("**Mức giảm không do verifier hay bộ lọc.** Bỏ hẳn bộ lọc cho kết quả gần như bằng có lọc; huấn luyện trên lời giải mẫu (train-on-gold) còn giảm nặng hơn (pass@1 33,3% → 15,3%)."),
  B("**Cấu tạo của mức giảm:** ở self-training, độ chính xác trên những lời giải model viết xong **không giảm** (37,2% → 38,9%); thứ tăng lên là tỉ lệ đầu ra lan man không bao giờ ra đáp án (từ ~10% lên ~40% ở 5e-4). Tăng giới hạn token khi đánh giá **không** làm hết hiện tượng này vì model gốc cũng được lợi tương đương. Ở train-on-gold thì ngược lại: lời giải ngắn đi 59% và độ chính xác thật sự giảm (37% → 14%)."),
  B("**Chưa có lần chạy nào cho thấy model giỏi lên bền vững**, khớp với hướng “khuếch đại, không tích lũy” mà bài đã trích dẫn."),

  H1("2. Bối cảnh: kết luận trước khi có kết quả mới"),
  P("Bài nghiên cứu vòng lặp tự huấn luyện Generate–Verify–Train (GVT): model tự sinh lời giải, máy chấm dựa trên luật (math-verify) chọn lời giải đúng, model được huấn luyện lại trên đó, lặp nhiều vòng. Câu hỏi: nếu verifier thiên lệch một chiều (từ chối oan cách viết \\dfrac/\\tfrac, tỉ lệ 100% khi xảy ra) thì có gây sụp đổ năng lực qua nhiều vòng không?"),
  P("Kết luận trước đây, toàn bộ ở learning rate 1e-5: (1) thiết kế gộp hai bộ dữ liệu (Design P) cho thấy sụp đổ mạnh (pass@8 của model 1.5B giảm 72,6% → 48,6%) nhưng phần lớn là hiện vật của thiết kế (một adapter chung và chấm trên chính tập đã chọn dữ liệu); (2) thiết kế tách riêng (Design I) cho pass@8 phẳng ở cả hai seed; (3) vá verifier không đổi gì đo được vì lỗi \\dfrac chỉ chiếm khoảng 0,55% lời giải. Phần (1) vẫn đứng vững; phần (2) và (3) là phần tuần này thay đổi."),

  H1("3. Công việc em làm trong tuần"),
  H2("3.1. Chạy lại ở nhiều mức learning rate"),
  P("Cấu hình giữ nguyên (MATH-500, Qwen2.5-1.5B, 150 bài thi giữ riêng) trừ hai điều chỉnh vì giới hạn tài nguyên: 3 vòng thay cho 5 và k = 4 mẫu mỗi bài thay cho 8 (nên dùng pass@4). Mỗi seed chia tập thi khác nhau."),
  table([1500, 800, 1400, 1400, 1500, 1426, 1000],
    ["Learning rate", "Seed", "pass@1 v0 → v2", "pass@4 v0 → v2", "Chính xác mẫu v0 → v2", "Lan man ở v2", "Run"],
    [
      ["1e-4", "1", "33,3 → 34,0", "50,0 → 49,3", "33,7 → 32,2", "19,5%", "A"],
      ["1e-4", "2", "31,3 → 28,0", "51,3 → 45,3", "30,8 → 27,2", "19,5%", "A"],
      ["1e-4", "3", "29,3 → 26,7", "40,0 → 41,3", "28,5 → 27,5", "22,7%", "A"],
      ["2e-4", "1", "33,3 → 31,3", "50,0 → 46,7", "33,7 → 30,2", "25,0%", "A"],
      ["2e-4", "2", "31,3 → 25,3", "51,3 → 45,3", "30,8 → 27,0", "22,2%", "A"],
      ["5e-4", "1", "33,3 → 23,3", "50,0 → 42,7", "33,7 → 25,3", "41,3%", "A"],
      ["5e-4", "1", "33,3 → 28,7", "50,7 → 48,7", "33,8 → 27,2", "35,7%", "B (đã vá)"],
      ["5e-4", "2", "31,3 → 27,3", "51,3 → 44,7", "30,8 → 26,2", "36,3%", "A"],
      ["5e-4", "2", "31,3 → 20,0", "52,0 → 40,7", "31,2 → 22,0", "41,7%", "B (đã vá)"],
    ], [L]),
  caption("Bảng 1. Run A và B ở các mức learning rate (đơn vị %; “lan man” = lời giải dài hơn 1.500 ký tự và không có \\boxed). Một bài thi = 0,67 điểm."),
  P("Nhìn chung độ chính xác mẫu giảm theo learning rate: trung bình −2,0 điểm ở 1e-4 (ba seed), −3,7 ở 2e-4 (hai seed), −6,5 ở 5e-4 (hai seed); tỉ lệ lan man tăng tương ứng, từ 8,8% ở 1e-5 lên 19,5–22,7% ở 1e-4, 22–25% ở 2e-4 và 36–42% ở 5e-4. Về bản vá: chênh B − A ở vòng 2 là +5,4 (pass@1) ở seed 1 và −7,3 ở seed 2 nên không có hiệu ứng nhất quán."),

  H2("3.2. Hai đối chứng ở learning rate 5e-4 (hai seed)"),
  B("**Không lọc (no-filter):** huấn luyện trên mọi mẫu model sinh ra (1.400 ví dụ, khoảng hai phần ba verifier sẽ từ chối), bỏ hẳn verifier khỏi vòng lặp."),
  B("**Train-on-gold:** bỏ qua mẫu của model, huấn luyện trên 350 lời giải mẫu, giống nhau mỗi vòng; các vòng của nó là các lần fine-tune lặp lại từ model gốc."),
  table([2300, 700, 1000, 1000, 1000, 1000, 1013, 1013],
    ["Lần chạy", "Seed", "pass@1 v0", "pass@1 v1", "pass@1 v2", "pass@4 v0", "pass@4 v1", "pass@4 v2"],
    [
      ["A (có lọc)", "1", "33,3", "32,7", "23,3", "50,0", "49,3", "42,7"],
      ["Không lọc", "1", "33,3", "26,7", "27,3", "50,0", "49,3", "40,7"],
      ["Train-on-gold", "1", "33,3", "18,0", "15,3", "50,0", "33,3", "29,3"],
      ["A (có lọc)", "2", "31,3", "31,3", "27,3", "51,3", "46,0", "44,7"],
      ["Không lọc", "2", "31,3", "34,7", "22,7", "51,3", "48,7", "39,3"],
      ["Train-on-gold", "2", "31,3", "8,7", "10,0", "51,3", "28,7", "30,7"],
    ], [L]),
  caption("Bảng 2. Hai đối chứng ở lr = 5e-4 (%), mỗi seed dùng tập thi của Run A cùng seed."),
  P("Cả hai kết quả đều tái hiện ở seed thứ hai. Bỏ bộ lọc không giúp gì (seed 1: 27,3 và 40,7; seed 2: 22,7 và 39,3, so với Run A 23,3 và 42,7; 27,3 và 44,7), trong khi bộ lọc chỉ giữ khoảng 31% số mẫu. Huấn luyện trên lời giải mẫu **tệ hơn** self-training: chỉ một lần fine-tune đã kéo pass@1 từ 33,3% xuống 18,0% ở seed 1 và từ 31,3% xuống 8,7% ở seed 2, và model chuyển hẳn sang văn phong lời giải mẫu (tỉ lệ dùng ký hiệu $…$ từ 5% lên 98% ở seed 1). Kết luận: mức giảm không phụ thuộc vào verifier hay việc lọc dữ liệu; lời giải mẫu gây hại nhiều hơn, dữ liệu tự sinh “nhẹ tay” hơn (em chưa kiểm tra nguyên nhân)."),

  P("**Run C (GSM8K) ở 5e-4** (seed 1, 3 vòng, k = 4): pass@1 giảm 70,7% → 64,7% → 48,7% và pass@4 86,0% → 86,0% → 76,7%, nhanh hơn mọi run MATH-500 (ở 1e-5, pass@1 vòng 2 là 65,3%). Tỉ lệ lan man tăng từ 2,5% lên 16,7%, và khác với MATH-500, độ chính xác trên những lời giải làm xong cũng giảm (71,5% → 64,6%). Vậy hiệu ứng suy giảm độ tin cậy lần đầu ở GSM8K mà bài ghi nhận trước đây phụ thuộc learning rate và lớn hơn ở 5e-4."),

  H2("3.3. Mức giảm thực sự gồm những gì"),
  P("Độ chính xác trên mỗi mẫu trộn hai thứ: model viết xong lời giải thì đúng bao nhiêu, và model có viết xong hay không. Em tách chúng ra, coi một lời giải là “lan man” nếu dài hơn 1.500 ký tự và không có \\boxed."),
  table([2100, 700, 1700, 1500, 1726, 1300],
    ["Lần chạy", "Seed", "Độ dài (ký tự) v0 → v2", "Lan man v0 → v2", "Chính xác trên phần còn lại v0 → v2", "Ví dụ train bị cắt"],
    [
      ["A (verifier gốc), 5e-4", "1", "1175 → 1678", "9,8% → 41,3%", "37,2% → 38,9%", "24,5%"],
      ["B (đã vá), 5e-4", "1", "1175 → 1659", "9,8% → 35,7%", "37,2% → 40,2%", "24,6%"],
      ["A (verifier gốc), 5e-4", "2", "1154 → 1641", "8,7% → 36,3%", "33,2% → 36,6%", "24,5%"],
      ["B (đã vá), 5e-4", "2", "1154 → 1728", "8,7% → 41,7%", "33,6% → 34,9%", "24,5%"],
      ["Không lọc, 5e-4", "1", "1175 → 1668", "9,8% → 38,8%", "37,2% → 38,4%", "62,4%"],
      ["Không lọc, 5e-4", "2", "1154 → 1755", "8,7% → 42,7%", "33,2% → 34,0%", "—"],
      ["Train-on-gold, 5e-4", "1", "1175 → 485", "9,8% → 0,0%", "37,2% → 14,0%", "17,4%"],
      ["Train-on-gold, 5e-4", "2", "1154 → 516", "8,7% → 0,3%", "33,2% → 12,2%", "—"],
    ], [L]),
  caption("Bảng 3. Cấu tạo của mức giảm ở vòng 2. “Ví dụ train bị cắt” là tỉ lệ ví dụ huấn luyện vòng 0 dài hơn giới hạn 512 token."),
  P("Ở cả các run self-training, tỉ lệ lan man tăng mạnh nhưng độ chính xác trên phần còn lại **không giảm**. Nếu giữ tỉ lệ lan man ở mức vòng 0, Run A seed 1 sẽ đạt 35,7% ở vòng 2, cao hơn 33,7% của vòng 0. Các mẫu lan man mở đầu bình thường rồi trôi sang chuỗi từ ngẫu nhiên (ví dụ “acknowledged hurdles acknowledged setbacks…”), ít lặp chính xác nên không phải vòng lặp. Đây là phân tích mô tả: nếu các bài khó là các bài hay bị lan man thì độ chính xác trên phần còn lại có thể tăng giả tạo."),
  P("**Hai giả thuyết về pipeline, em đã kiểm tra:**"),
  B("**Cắt cụt ví dụ huấn luyện.** Giới hạn độ dài khi huấn luyện (512 token) bằng giới hạn khi sinh nên 24–26% ví dụ bị cắt, mất đáp án cuối và token kết thúc. Huấn luyện lại với giới hạn 1.024 token (không ví dụ nào bị cắt) vẫn cho tỉ lệ lan man 37,2% (so với 30,0% ở bản đối chứng) nên **đây không phải nguyên nhân**."),
  B("**Giới hạn token khi đánh giá.** Đánh giá lại cùng adapter vòng 2 với 1.536 token thay vì 512, và đánh giá cả model gốc: độ chính xác mẫu của model gốc tăng từ 36,3% lên 43,2% (lan man 8,7% → 2,5%), còn của adapter từ 28,3% lên 34,2% (replicate) và từ 27,5% lên 29,5% (huấn luyện 1.024). Khoảng cách với model gốc không thu hẹp (−8,0 → −9,0 và −8,8 → −13,7 điểm). Model gốc ra đáp án ở 97,5% số mẫu, adapter chỉ 67–77%. Vậy **đây không phải do giới hạn token**: adapter có vấn đề không dừng kéo dài dù cho thêm token."),

  H2("3.4. Cách em xử lý sự cố treo trên Kaggle"),
  P("Tuần trước các lần chạy lại liên tục bị treo đến hết trần 12 giờ mỗi phiên mà không ra kết quả. Em chưa giải thích được nguyên nhân gốc (nhiều giả thuyết đều bị bác bỏ khi kiểm tra), nên chọn cách làm không phụ thuộc vào nguyên nhân: mỗi vòng chạy trong một tiến trình riêng và lưu trạng thái để chạy tiếp; một bộ điều phối bên ngoài tự dừng và chạy lại tiến trình nếu GPU rảnh liên tục quá 20 phút và ghi lại vị trí các luồng đang kẹt. Em kiểm tra bằng một lần chạy thử 8 phút cố ý gây treo; sau đó toàn bộ các lần chạy chính của tuần này (mười run, hai lượt đánh giá lại) đều hoàn tất sạch, không có lần dừng nào."),

  H1("4. Đối chiếu với các bài liên quan gần nhất"),
  P("Em tra lại tài liệu và đọc toàn văn ba bài gần nhất. Em chưa tìm thấy bài nào kết hợp đúng ba thứ: verifier có thiên lệch định dạng được đo thật, nhiều vòng self-training liên tiếp, và đối chứng vá verifier. Nhưng đề tài chung đã có nhiều người làm, nên bài của em nên được trình bày như một kiểm chứng bổ sung."),
  B("**Xu và cộng sự (arXiv 2608.20290, 08/2026) — kiểm toán self-improvement.** Qwen3-8B, LoRA rank 32, 3 vòng, so với một model đóng băng; chỉ ra 7 lỗi đo lường làm đảo ngược kết luận, gồm “giới hạn token cố định khi văn phong thay đổi” và độ biến thiên theo seed. Đây là bài gần nhất về tinh thần. Kết quả của em gặp họ ở: chênh lệch A–B đổi dấu theo seed, tập thi nhỏ chỉ phân giải được hiệu ứng lớn, và văn phong trôi. Khác biệt: họ cố định bộ lọc và learning rate, không có verifier thiên lệch định dạng được đo; em có các thứ đó nhưng không có đối chứng đóng băng."),
  B("**Kim và cộng sự (arXiv 2603.24472, COLM 2026) — self-distillation làm giảm khả năng suy luận.** Teacher biết lời giải đúng làm lời giải ngắn đi và độ chính xác giảm tới 40%. Train-on-gold của em cho cùng dấu hiệu ở quy mô nhỏ (ngắn đi 59%, chính xác trên bài làm xong 37% → 14%); em không đo được cơ chế. Self-training của em đi theo hướng ngược lại (dài ra và lan man), điều bài đó không dự đoán."),
  B("**Egashira và cộng sự (arXiv 2605.02909, COLM 2026) — lỗi verifier có hệ thống.** Số học tổng hợp, RLVR, lỗi thiết kế tay; kết luận false negative có hệ thống giống nhiễu ngẫu nhiên. Đối chứng của em cho cùng kết luận với verifier thật, dữ liệu thật, nhiều vòng SFT."),

  H1("5. Bài báo đã cập nhật"),
  B("Viết lại theo kết quả mới: mục kiểm tra learning rate, mục cấu tạo của mức giảm, bảng đánh giá lại với giới hạn token lớn hơn kèm model gốc, Related Work với Xu và Kim, Abstract, Kết luận, Hạn chế."),
  B("Tinh gọn từ 25 xuống 18 trang (sau khi thêm kết quả mới): bỏ hình và bảng phụ của thiết kế gộp, gộp các mục trùng nhau, Abstract còn khoảng 240 từ."),

  H1("6. Hạn chế và việc tiếp theo"),
  B("Run C ở learning rate mới và phần đánh giá lại với giới hạn token mới chỉ có một seed; lưới learning rate còn thưa; chỉ 3 vòng, k = 4, tập thi 150 bài."),
  B("Chỉ báo “lan man” là ngưỡng gần đúng (độ dài và không có \\boxed)."),
  P("Nếu còn thời gian GPU (quota Kaggle còn khoảng 1,8h, reset 17/10), em dự định thêm seed và mức learning rate cho Run C (GSM8K) và làm mịn lưới learning rate giữa 1e-4 và 5e-4."),

  H1("7. Điều em xin trao đổi với Thầy/Cô"),
  B("**Khung trình bày và tiêu đề.** Kết quả mới cho thấy mức giảm không do verifier hay bộ lọc, tăng theo learning rate, và có cấu tạo khác nhau giữa self-training (không kết thúc lời giải) và train-on-gold (ngắn đi, kém đi thật). Em nên giữ khung “verifier bias không phải nguyên nhân”, hay chuyển sang khung rộng hơn về kiểm toán đo lường self-training (gần với Xu và cộng sự)?"),
  B("**Giới hạn số trang.** Bài hiện 18 trang, hơi dài so với chuẩn LNCS phổ biến (12–15 trang); em chưa biết giới hạn thật của nơi nộp, nếu cần cắt thêm thì em chuyển các bảng phụ xuống phụ lục."),
  B("**Phạm vi thực nghiệm còn lại.** Với số seed và số vòng hiện có, Thầy/Cô thấy em nên dừng thêm thí nghiệm để hoàn thiện bài, hay chạy thêm seed cho các đối chứng?"),
  gap(),
  P("Em cảm ơn Thầy/Cô đã dành thời gian xem báo cáo. Em xin nhận góp ý của Thầy/Cô về các điểm trên.", { alignment: AlignmentType.LEFT }),
  new Paragraph({ alignment: AlignmentType.RIGHT, spacing: { before: 200, after: 40 }, children: [new TextRun({ text: "Nhóm thực hiện", bold: true, font: FONT, size: 24 })] }),
  new Paragraph({ alignment: AlignmentType.RIGHT, spacing: { after: 0 }, children: [new TextRun({ text: "Nguyễn Tấn Sang (52300057) — Trần Duy Anh (52300006)", font: FONT, size: 24 })] }),
];

const doc = new Document({
  creator: "Nguyễn Tấn Sang, Trần Duy Anh", title: "Báo cáo tiến độ thực nghiệm",
  styles: { default: { document: { run: { font: FONT, size: 24 } } },
    paragraphStyles: [
      { id: "Heading1", name: "Heading 1", basedOn: "Normal", next: "Normal", quickFormat: true, run: { size: 28, bold: true, font: FONT }, paragraph: { outlineLevel: 0 } },
      { id: "Heading2", name: "Heading 2", basedOn: "Normal", next: "Normal", quickFormat: true, run: { size: 25, bold: true, font: FONT }, paragraph: { outlineLevel: 1 } },
    ] },
  numbering: { config: [{ reference: "bul", levels: [{ level: 0, format: LevelFormat.BULLET, text: "•", alignment: AlignmentType.LEFT,
    style: { paragraph: { indent: { left: 540, hanging: 270 } } } }] }] },
  sections: [{
    properties: { page: { size: { width: 11906, height: 16838 }, margin: { top: 1440, right: 1440, bottom: 1300, left: 1440 } } },
    footers: { default: new Footer({ children: [new Paragraph({ alignment: AlignmentType.CENTER,
      children: [new TextRun({ children: ["Trang ", PageNumber.CURRENT, " / ", PageNumber.TOTAL_PAGES], font: FONT, size: 20 })] })] }) },
    children,
  }],
});
Packer.toBuffer(doc).then((buf) => { fs.writeFileSync(process.argv[2], buf); console.log("written", process.argv[2]); });
