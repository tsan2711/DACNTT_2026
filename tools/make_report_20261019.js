// Tạo BaoCaoThucNghiem_20261019.docx (báo cáo tiến độ thực nghiệm gửi giảng viên).
// Chạy: NODE_PATH=<thư mục có node_modules/docx> node tools/make_report_20261019.js BaoCaoThucNghiem_20261019.docx
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
  new Paragraph({ alignment: AlignmentType.CENTER, spacing: { after: 120 }, children: [new TextRun({ text: "BÁO CÁO TIẾN ĐỘ THỰC NGHIỆM", bold: true, font: FONT, size: 34 })] }),
  new Paragraph({ alignment: AlignmentType.CENTER, spacing: { after: 280, line: 280 },
    children: [new TextRun({ text: "Đề tài: Generate–Verify–Train Iterations Do Not Self-Improve a Small Reasoning Model: A Negative Result with Qwen2.5-1.5B and a Rule-Based Verifier", italics: true, font: FONT, size: 24 })] }),

  P("Em xin gửi thầy báo cáo thực nghiệm đã cập nhật theo bản bài báo mới nhất (paper_revised, 18/10/2026). So với báo cáo 11/10, có **hai thay đổi lớn**: (1) bài và báo cáo quay về đúng câu hỏi gốc của đề tài, “model có giỏi toán hơn thật, hay chỉ học cách viết hợp máy chấm?”, trả lời bằng bốn thước đo đã chốt từ đầu và có khoảng tin cậy; (2) một số nhận định trong báo cáo 11/10 đã bị em sửa vì không đứng vững khi kiểm tra lại (mục 5). Báo cáo gồm: kết quả chính, các số liệu, đối chiếu tài liệu, những gì đã sửa trong bài, và hạn chế."),

  H1("1. Kết quả chính"),
  B("**Không có lần chạy nào cho thấy model giỏi toán hơn.** Trên 150 bài thi giữ riêng, ở bốn mức learning rate (1e-5 đến 5e-4), hai hoặc ba seed và ba đối chứng, không mức tăng pass@1 hay pass@k nào có khoảng tin cậy bootstrap (theo từng bài) loại trừ 0. Ở mọi lần chạy MATH-500, trừ 1e-4 seed 3 (16 thêm / 14 mất), số bài bị mất bằng hoặc nhiều hơn số bài được thêm."),
  B("**Không thấy dấu hiệu model học cách viết hợp máy chấm.** Tỉ lệ lời giải dùng \\boxed, dạng mà math-verify đọc, **giảm** khi self-training (52% → 36% và 54% → 37% ở 5e-4). Kiểu hình “pass@1 tăng, pass@k đứng yên, chữ viết hội tụ” mà ta đặt ra từ đầu không xuất hiện vì pass@1 không bao giờ tăng."),
  B("**Huấn luyện mạnh hơn làm model kém hơn, kể cả trên lời giải nó viết xong.** Khi so cùng độ khó, độ chính xác trên các lời giải chưa chạm trần 512 token giảm 5,5 đến 10,6 điểm ở 5e-4 (năm trong sáu lần chạy có khoảng tin cậy loại trừ 0). Tỉ lệ chạm trần chỉ tăng 2–14 điểm ở 5e-4 và không tăng ở learning rate thấp hơn; model gốc đã chạm trần ở 43% lời giải."),
  B("**Máy chấm có một lỗi đo được, lớn hơn lỗi \\dfrac nhiều lần.** Đáp án chuẩn của em lưu dạng trần (ví dụ 3\\sqrt{13}) còn dự đoán nằm trong \\boxed{}, nên math-verify không khớp: nó loại oan 15,5–18,6% lời giải đúng của chính vòng lặp và làm pass@1 tuyệt đối thấp đi khoảng 5–8 điểm. Mức giảm qua các vòng vẫn còn sau khi chấm lại."),
  B("**Hai đối chứng đều không phát hiện được gì, và không nên đọc là “máy chấm vô hại”.** Bản vá \\dfrac chỉ đổi 0–4 ví dụ trong mỗi pool (dưới 1%), còn bỏ bộ lọc thì khác liều huấn luyện 3–4 lần. Huấn luyện trên lời giải mẫu (train-on-gold) giảm nặng nhất: pass@4 giảm khoảng 21 điểm ở cả hai seed."),
  B("**Sụp đổ của thiết kế gộp (Design P) không tái hiện khi tách riêng, nhưng em chưa xác định được nguyên nhân.** Design P huấn luyện nhiều hơn khoảng 4,5 lần số ví dụ mỗi vòng, nên không tách được ảnh hưởng của việc gộp, của cách chấm và của liều huấn luyện."),

  H1("2. Bối cảnh và câu hỏi"),
  P("Vòng lặp Generate–Verify–Train (GVT): model nhỏ tự sinh lời giải, máy chấm dựa trên luật (math-verify) giữ lời giải có đáp án cuối khớp đáp án sách, model được huấn luyện lại bằng LoRA trên các lời giải đó, lặp nhiều vòng. Tuyên bố cần kiểm: model **tự cải thiện suy luận mà không cần nhãn mới**. Máy chấm chỉ nhìn đáp án cuối, không chấm các bước, và có thể gạch oan cách viết khác nhau của cùng một giá trị. Vì vậy điểm tăng chưa chắc là suy luận tốt hơn; câu hỏi là model giỏi toán hơn thật, hay chỉ học cách viết hợp máy chấm."),
  P("Bốn thước đo đã chốt trước: pass@1, pass@k, kiểu chữ viết (tỉ lệ \\boxed, ký hiệu $…$, \\dfrac) và số bài được thêm/mất theo từng bài. Luật đọc: chỉ khi pass@1 tăng, pass@k đứng yên và chữ viết hội tụ về một kiểu thì mới được nói “học chữ”. Thiếu bất kỳ mảnh nào chỉ được nói “chưa chắc”. Cấu hình chính: Qwen2.5-1.5B-Instruct, LoRA, MATH-500 và GSM8K, tập thi giữ riêng 150 bài mỗi dataset (350 bài còn lại dùng để chọn lời giải huấn luyện), pass@1 là một lần lấy mẫu mỗi bài."),

  H1("3. Công việc và số liệu"),
  H2("3.1. Đo lại máy chấm"),
  P("Em viết lại cách trình bày lỗi máy chấm thành ba lớp. **Lớp \\dfrac/\\tfrac:** bị loại 100% khi xuất hiện (146/146 trên MATH-500, 200/200 trên GSM8K) nhưng chỉ xuất hiện ở 0,5–0,7% lời giải của vòng lặp. **Tỉ lệ loại oan trên lời giải thật:** 7,8% trên MATH-500 (10/128, khoảng Wilson 95% là 4,3–13,8%), 0% trên GSM8K (0/200); đây là lời giải của model khác và em chỉ xem các lời giải bị loại, nên không đo được tỉ lệ chấp nhận nhầm. **Lỗi lưu đáp án chuẩn (mới):** chấm lại các lời giải đã lưu của chính vòng lặp thì lỗi này loại oan 15,5–18,6% số lời giải mà bản chấm lại chấp nhận, và nếu sửa thì pool huấn luyện lớn thêm 17–23% (ví dụ Run A seed 1: 440 → 542). Em kiểm tay 30 trường hợp lật kết quả: 29 là cùng một giá trị viết khác đi (ví dụ \\frac43 và \\frac{4}{3}). Con số 15,5–18,6% giả định bản chấm lại không chấp nhận sai, điều em chưa đo. Mọi bảng dưới đây vẫn dùng máy chấm gốc, vì đó là máy chấm vòng lặp thật sự dùng."),

  H2("3.2. Thay đổi learning rate"),
  P("Learning rate 1e-5 (mặc định của code, chưa từng được tune) làm đầu ra gần như không đổi: độ dài 1158 → 1146 ký tự, tỉ lệ chạm trần 40,7% → 41,8%. Loss ở vòng 0 vẫn giảm (0,72 → 0,38), nên model có học nhưng chậm. Em chạy lại MATH-500 với ngân sách nhỏ hơn (3 vòng, k = 4, nên dùng pass@4): Run A ở 1e-4 (ba seed), 2e-4 (hai seed), và Run A, B ở 5e-4 (hai seed). Mỗi seed chia tập thi khác nhau, và các run này không so trực tiếp được với bảng 5 vòng, k = 8 ở 1e-5."),
  table([1250, 650, 1100, 1450, 1450, 2000, 1126],
    ["Learning rate", "Seed", "Run", "pass@1 v0 → v2", "pass@4 v0 → v2", "Δ pass@1 [KTC 95%]", "Chạm trần v2"],
    [
      ["1e-4", "1", "A", "33,3 → 34,0", "50,0 → 49,3", "+0,7 [−6,7; +8,0]", "42,7%"],
      ["1e-4", "2", "A", "31,3 → 28,0", "51,3 → 45,3", "−3,3 [−9,3; +2,7]", "42,8%"],
      ["1e-4", "3", "A", "29,3 → 26,7", "40,0 → 41,3", "−2,7 [−10,0; +4,0]", "45,7%"],
      ["2e-4", "1", "A", "33,3 → 31,3", "50,0 → 46,7", "−2,0 [−8,0; +4,0]", "40,8%"],
      ["2e-4", "2", "A", "31,3 → 25,3", "51,3 → 45,3", "−6,0 [−12,7; +0,7]", "39,7%"],
      ["5e-4", "1", "A", "33,3 → 23,3", "50,0 → 42,7", "−10,0 [−16,7; −3,3]", "46,2%"],
      ["5e-4", "1", "B (đã vá)", "33,3 → 28,7", "50,7 → 48,7", "−4,7 [−12,0; +2,7]", "47,8%"],
      ["5e-4", "2", "A", "31,3 → 27,3", "51,3 → 44,7", "−4,0 [−11,3; +3,3]", "51,2%"],
      ["5e-4", "2", "B (đã vá)", "31,3 → 20,0", "52,0 → 40,7", "−11,3 [−17,3; −5,3]", "54,0%"],
    ], [L]),
  caption("Bảng 1. Run A và B ở các mức learning rate (đơn vị %, MATH-500, tập thi 150 bài). KTC = khoảng tin cậy bootstrap theo từng bài, chưa gồm phương sai giữa các lần train. “Chạm trần” = lời giải có ít nhất 508 token sau khi tokenize lại; ở vòng 0 là 43,0–43,2% (48,2% ở seed 3)."),
  P("Ở 5e-4, cả bốn lần chạy đều giảm; khoảng tin cậy của pass@1 loại trừ 0 ở hai trong bốn, của pass@4 ở một. A và B cùng seed dùng chung tập thi, chung lời giải vòng 0 và gần như chung pool đầu, nên bốn lần chạy gần với hai bản lặp độc lập hơn là bốn. Trung bình hai seed, độ chính xác theo mẫu ở vòng 2 giảm 2,0 điểm ở 1e-4 (ba seed), 3,7 ở 2e-4 và 6,5 ở 5e-4: cùng chiều với learning rate, nhưng seed 2 gần như phẳng (−3,6; −3,8; −4,6) và ở 1e-4, 2e-4 mức giảm cỡ nhiễu lấy mẫu. **Bản vá không có tác dụng nhất quán:** B − A ở vòng 2 là +5,3 [−2,0; +12,0] điểm pass@1 ở seed 1 và −7,3 [−14,0; −0,7] ở seed 2. Dấu đổi theo seed, và hai lần chạy cùng seed có pool đầu giống hệt (424/424) vẫn kết thúc cách nhau 7,3 điểm, nên khoảng tin cậy ở trên chưa bao gồm nhiễu giữa các lần train."),

  H2("3.3. Hai đối chứng ở 5e-4 và Run C (GSM8K)"),
  B("**Không lọc (no-filter):** huấn luyện trên mọi mẫu model sinh ra (1.400 ví dụ mỗi vòng), không dùng máy chấm."),
  B("**Train-on-gold:** bỏ qua mẫu của model, huấn luyện trên 350 lời giải mẫu của bộ dữ liệu, giống nhau mỗi vòng."),
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
  P("**Không lọc** không khác nhất quán so với có lọc: ở vòng 2, hiệu pass@1 là +4,0 [−2,7; +10,7] (seed 1) và −4,7 [−12,0; +2,7] (seed 2), hiệu pass@4 là −2,0 và −5,3, âm ở cả hai seed nhưng khoảng tin cậy chứa 0. Máy chấm giữ 31% số mẫu ở vòng 0 và 23–25% ở vòng 2. Vì no-filter huấn luyện 700 bước mỗi vòng, so với 163–220 bước của Run A, liều huấn luyện và dữ liệu khác nhau cùng lúc, nên em chỉ kết luận được là hiệu ứng vài điểm theo cả hai chiều chưa bị loại trừ. **Train-on-gold** giảm nặng nhất (pass@4 giảm khoảng 21 điểm, khoảng tin cậy cao nhất −12,7), model chuyển hẳn sang văn phong lời giải mẫu (ký hiệu $…$ từ 5% lên 98%, \\boxed từ 52% lên 86%). Em chưa kiểm tay các đáp án bị loại của run này, nên một phần mức giảm có thể là lỗi máy chấm sau khi định dạng đổi mạnh; em cho rằng khó giải thích được phần lớn mức giảm từ 33% xuống 15%, nhưng chưa chứng minh."),
  P("**Run C (GSM8K) ở 5e-4** (seed 1, 3 vòng, k = 4): pass@1 70,7% → 64,7% → 48,7% (thay đổi vòng 0 → 2 là −22,0 [−29,3; −15,3]) và pass@4 86,0% → 86,0% → 76,7%. Tỉ lệ chạm trần tăng 3,8% → 15,0%, độ chính xác trên lời giải viết xong cũng giảm (71,9% → 63,3%; −12,1 điểm khi so cùng độ khó). Run C ở 1e-5 có phân vùng, k và số vòng khác, nên chỉ so được mức thay đổi trong từng run (−1,4 điểm pass@1 ở 1e-5, −22,0 ở 5e-4); đây là gợi ý có phụ thuộc learning rate, từ một lần chạy mỗi mức."),

  H2("3.4. Mức giảm gồm những gì"),
  P("Độ chính xác trên mỗi mẫu trộn hai thứ: model viết xong thì đúng bao nhiêu, và model có viết xong trong 512 token hay không. Em không lưu số token lúc sinh, nên tokenize lại văn bản đã lưu và coi là “chạm trần” nếu có ít nhất 508 token (caphit.py, capanat.py). Model gốc đã chạm trần ở 43,0–43,2% lời giải MATH-500 và chỉ 4–7% trong số đó được chấm đúng, tức là trần 512 token bó buộc ngay từ đầu, không phải hậu quả của huấn luyện. Để so công bằng, em so độ chính xác trên lời giải viết xong của vòng cuối với độ chính xác của model gốc trên **cùng cơ cấu bài** (mỗi bài được trọng số theo số mẫu viết xong của nó ở vòng cuối), vì các bài còn viết xong đã thay đổi."),
  table([2300, 700, 1600, 1500, 1626, 1300],
    ["Lần chạy", "Seed", "Độ dài (ký tự) v0 → v2", "Chạm trần v0 → v2 (%)", "Chính xác phần viết xong (%)", "Δ so cùng độ khó"],
    [
      ["A (verifier gốc), 5e-4", "1", "1175 → 1678", "43,2 → 46,2", "54,0 → 43,0", "−9,1"],
      ["B (đã vá), 5e-4", "1", "1175 → 1659", "43,2 → 47,8", "54,0 → 46,3", "−6,8"],
      ["A (verifier gốc), 5e-4", "2", "1154 → 1641", "43,0 → 51,2", "50,6 → 45,4", "−5,5"],
      ["B (đã vá), 5e-4", "2", "1154 → 1728", "43,0 → 54,0", "51,2 → 44,2", "−5,9"],
      ["Không lọc, 5e-4", "1", "1175 → 1668", "43,2 → 45,5", "54,0 → 43,1", "−10,6"],
      ["Không lọc, 5e-4", "2", "1154 → 1755", "43,0 → 57,2", "50,6 → 43,6", "−6,6"],
      ["A, 2e-4", "1", "1175 → 1433", "43,2 → 40,8", "54,0 → 46,5", "−4,0"],
      ["A, 2e-4", "2", "1154 → 1431", "43,0 → 39,7", "50,6 → 41,7", "−4,7"],
      ["A, 1e-4", "1", "1175 → 1276", "43,2 → 42,7", "54,0 → 48,5", "−4,3"],
      ["A, 1e-4", "2", "1154 → 1284", "43,0 → 42,8", "50,6 → 44,6", "−3,5"],
      ["A, 1e-4", "3", "1178 → 1355", "48,2 → 45,7", "50,2 → 47,5", "−0,6"],
      ["A, 1e-5 (v0 → v4)", "1", "1158 → 1146", "40,7 → 41,8", "55,2 → 54,3", "−2,3"],
      ["Train-on-gold, 5e-4", "1", "1175 → 485", "43,2 → 7,2", "54,0 → 14,7", "−25,6"],
      ["Train-on-gold, 5e-4", "2", "1154 → 516", "43,0 → 8,3", "50,6 → 12,5", "−25,9"],
    ], [L]),
  caption("Bảng 3. Cấu tạo của mức giảm (MATH-500, vòng 0 → vòng cuối; dòng 1e-5 là run gốc, k = 8, 5 vòng, liều huấn luyện không so được). Khoảng tin cậy của cột cuối nằm ở bảng khoảng tin cậy trong bài."),
  P("Ở sáu lần self-training ở 5e-4, độ dài trung bình tăng 41–52% nhưng tỉ lệ chạm trần chỉ tăng 2,3–14,2 điểm, trong khi độ chính xác trên lời giải viết xong giảm từ 50,6–54,0% xuống 43,0–46,3%. Khi so cùng độ khó, phần viết xong mất 5,5–10,6 điểm, năm trên sáu khoảng tin cậy loại trừ 0. Ở 1e-4 và 2e-4 tỉ lệ chạm trần không tăng, toàn bộ mức giảm (nhỏ hơn) nằm ở độ chính xác phần viết xong (−0,6 đến −4,7 điểm, khoảng tin cậy chứa 0). Vậy việc không viết xong chỉ góp vào mức giảm ở learning rate cao nhất, và không phải phần chính (khoảng một phần ba đến ba phần tư mức giảm là do độ chính xác phần viết xong). Các lời giải dài thường mở đầu bình thường rồi trôi sang văn xuôi ít liên quan (ví dụ “acknowledged hurdles acknowledged setbacks…”), ít lặp chính xác; mô tả này dựa trên xem ví dụ, chưa gán nhãn có hệ thống. Train-on-gold khác hẳn: lời giải ngắn đi khoảng 59%, chạm trần giảm từ 43% xuống 7–8%, độ chính xác phần viết xong sụp xuống (−25,6 và −25,9 điểm)."),
  P("**Hai kiểm tra pipeline.** Giới hạn huấn luyện (max_length = 512 token, gồm cả đề) bằng giới hạn sinh, nên 24–26% ví dụ trong pool bị cắt cụt, mất đáp án cuối và token kết thúc. Em chạy lại Run A seed 1 ở 5e-4 với giới hạn 1.024 token (không ví dụ nào bị cắt), kèm một bản lặp giữ 512: tỉ lệ chạm trần ở vòng 2 là 43,8% (giới hạn 1.024), 43,0% (bản lặp) và 46,2% (Run A gốc); độ chính xác phần viết xong so cùng độ khó giảm 5,7; 5,0 và 9,1 điểm. Với một lần chạy mỗi nhánh, kết quả chỉ loại trừ được hiệu ứng cắt cụt lớn. Kiểm tra thứ hai: chấm lại cùng adapter vòng 2 với trần sinh 1.536 token (Bảng 4)."),
  table([3000, 800, 1300, 1300, 1300, 1326],
    ["Model", "Trần", "pass@1", "pass@4", "Chính xác mẫu", "Chênh so với model gốc"],
    [
      ["Model gốc", "512", "36,0%", "52,0%", "36,3%", "—"],
      ["", "1536", "40,7%", "59,3%", "43,2%", "—"],
      ["5e-4, bản lặp (giới hạn 512)", "512", "29,3%", "46,7%", "28,3%", "−8,0"],
      ["", "1536", "35,3%", "52,0%", "34,2%", "−9,0"],
      ["5e-4, giới hạn 1.024", "512", "26,0%", "45,3%", "27,5%", "−8,8"],
      ["", "1536", "30,7%", "50,7%", "29,5%", "−13,7"],
      ["2e-4", "512", "27,3%", "48,7%", "28,5%", "−7,8"],
      ["", "1536", "32,0%", "52,7%", "32,0%", "−11,2"],
    ], [L]),
  caption("Bảng 4. Chấm lại adapter vòng 2 trên cùng tập thi (seed 1, k = 4) với hai trần sinh. Mỗi dòng là một adapter; chấm lại cùng adapter làm pass@1 lệch 2,7–6,7 điểm so với giá trị trong run. Chỉ lưu số liệu tổng hợp nên không có khoảng tin cậy."),
  P("Model gốc được lợi từ trần lớn **nhiều hơn** các adapter (độ chính xác mẫu +6,9 điểm so với +5,9; +2,0; +3,5), nên khoảng cách giữa adapter và model gốc không thu hẹp mà rộng ra, phù hợp với việc phần thiếu hụt nằm ở nội dung adapter viết hơn là ở chỗ bị cắt. Dữ liệu chỉ cho thấy trần gấp ba không xóa được khoảng cách, với từng adapter đơn lẻ trên một phân vùng; chúng không nói gì về trần lớn hơn nữa."),

  H2("3.5. Cách em xử lý sự cố treo trên Kaggle"),
  P("Các lần chạy trước bị treo đến hết trần 12 giờ mỗi phiên. Em chưa giải thích được nguyên nhân gốc (nhiều giả thuyết đều bị bác bỏ khi kiểm tra), nên chọn cách không phụ thuộc nguyên nhân: mỗi vòng chạy trong một tiến trình riêng và lưu trạng thái để chạy tiếp; một bộ điều phối bên ngoài tự dừng và chạy lại nếu GPU rảnh liên tục trên 20 phút. Cơ chế được kiểm bằng một lần chạy thử 8 phút có chủ đích gây treo ở vòng 1; sau đó các lần chạy chính hoàn tất sạch. Phần này chỉ ảnh hưởng độ tin cậy của việc chạy, không ảnh hưởng số liệu."),

  H1("4. Đối chiếu với các bài liên quan gần nhất"),
  P("Em tra lại tài liệu (đến tháng 10/2026) và đọc toàn văn các bài gần nhất. Em chưa tìm thấy bài nào kết hợp một máy chấm có thiên lệch định dạng được đo thật, nhiều vòng self-training liên tiếp và một đối chứng vá máy chấm. Tuy nhiên bản vá hóa ra quá yếu để kiểm tra điều gì, nên em **không còn xem tổ hợp này là đóng góp**; đóng góp là câu trả lời âm cho câu hỏi tự cải thiện bằng bốn thước đo xác định trước, kèm khoảng tin cậy, mô tả xem huấn luyện mạnh hơn làm thay đổi cái gì, và các bài học thiết kế."),
  B("**Xu và cộng sự (arXiv 2608.20290, 08/2026) — kiểm toán self-improvement.** Qwen3-8B, LoRA rank 32, 3 vòng, so với một model đóng băng làm đối chứng; chỉ ra 7 lỗi đo lường mà mỗi lỗi đảo ngược một kết luận nếu thiếu đối chứng, trong đó có giới hạn token cố định khi văn phong trôi và phương sai theo seed. Đây là bài gần nhất về tinh thần. Em gặp họ ở ba điểm: số bài mất nhiều hơn số bài thêm, văn phong trôi, và trần token vẫn bó buộc (model gốc chạm trần 43%). Khác biệt: em thiếu nhánh model đóng băng theo từng vòng và nhánh distillation; em có thêm máy chấm có lỗi định dạng được đo, chuỗi learning rate, và hai đối chứng no-filter, train-on-gold."),
  B("**Kim và cộng sự (arXiv 2603.24472, COLM 2026) — self-distillation làm giảm khả năng suy luận.** Teacher biết lời giải đúng làm lời giải ngắn đi và độ chính xác giảm tới 40%. Train-on-gold của em chỉ là SFT trên lời giải mẫu chứ không phải self-distillation, nên chỉ là một phép tương tự lỏng: có cùng dấu hiệu bề mặt (lời giải ngắn đi 59%, độ chính xác giảm) nhưng có thể chỉ do bắt chước lời giải mẫu ngắn. Em không đo được cơ chế mà họ đề xuất."),
  B("**Egashira và cộng sự (arXiv 2605.02909, COLM 2026) — lỗi máy chấm trong RLVR.** Bài toán số học tổng hợp, lỗi thiết kế tay; kết luận lỗi false negative có hệ thống hành xử như nhiễu ngẫu nhiên, còn false positive có thể gây plateau hoặc sụp đổ. Đối chứng của em **không kiểm được** kết luận về false negative, vì bản vá đổi quá ít và lỗi lưu đáp án chuẩn có mặt ở mọi run và không được thay đổi. Run no-filter (khoảng hai phần ba mẫu sai) không tệ hơn rõ rệt, nghe có vẻ căng với kết luận về false positive của họ, nhưng với hai seed, liều huấn luyện khác và SFT thay vì RL, em không coi đó là bằng chứng ngược lại."),

  H1("5. Những điều đã sửa so với báo cáo 11/10 và so với bài trước"),
  P("Phần này em ghi riêng vì các nhận định cũ đã được nêu với thầy trong báo cáo trước. Bản bài mới là paper_revised.tex, paper.tex giữ nguyên để đối chiếu; chi tiết từng thay đổi và bằng chứng ở papers/CHANGELOG-REVISION.md."),
  B("**Câu hỏi và tiêu đề.** Báo cáo 11/10 đặt đề quanh “thiên lệch máy chấm có gây sụp đổ năng lực không”, lệch khỏi câu hỏi gốc trong TOI-HIEU.md. Tiêu đề mới: “Generate–Verify–Train Iterations Do Not Self-Improve a Small Reasoning Model”, và bài trả lời bằng bốn thước đo đã chốt."),
  B("**Có khoảng tin cậy.** Em thêm bootstrap theo từng bài (10.000 lần lấy mẫu lại trong 150 bài, bootstrap_ci.py, kết quả ở results/viec3/ci/) thay cho “ngưỡng nhiễu 4,7” tự đặt. Khoảng này không gồm phương sai giữa các lần train."),
  B("**Chỉ báo “lan man” đã bỏ.** Báo cáo 11/10 nói tỉ lệ lan man tăng từ ~10% lên ~40% và độ chính xác phần viết xong **không giảm**. Đo lại bằng số token thật: model gốc đã chạm trần ở 43%, chỉ báo cũ chỉ bắt được 9,8%, và nó tăng chủ yếu vì văn bản trôi có nhiều ký tự trên mỗi token (3,3 → 4,9–5,0). Khi so cùng độ khó, độ chính xác phần viết xong **giảm** 5,5–10,6 điểm. Kết luận “mức giảm chủ yếu là không viết xong” là sai."),
  B("**“Loss không giảm ở 1e-5” là sai.** Con số 0,68–0,84 lấy từ một chẩn đoán nhỏ 120 ví dụ; log thật của run cho thấy loss giảm 0,72 → 0,38. Lập luận đúng là model có học nhưng đầu ra gần như không đổi."),
  B("**“Sụp đổ của Design P là hiện vật” đổi thành “chưa xác định nguyên nhân”,** vì Design P huấn luyện nhiều hơn ~4,5 lần số ví dụ mỗi vòng và chính dữ liệu của em cho thấy huấn luyện mạnh hơn làm giảm nhiều hơn."),
  B("**Bản vá không chứng minh “máy chấm không phải nguyên nhân”.** Nó đổi dưới 1% pool nên null là điều chắc chắn xảy ra bất kể sự thật. Phát biểu còn lại rất hẹp: bỏ một lỗi định dạng hiếm hoặc bỏ cả bộ lọc không tạo khác biệt nhất quán ở độ phân giải này."),
  B("**Sửa số học:** model gốc được lợi từ trần 1.536 token **nhiều hơn** adapter (+6,9 so với +5,9; +2,0; +3,5), không phải “tương đương”; hiệu pass@1 của run A seed 1 là −3,3 chứ không phải −3,4."),
  P("Bài hiện dài 21 trang. Em không chạy thêm thí nghiệm nào cho đợt sửa này và không dùng GPU; mọi con số đều lấy từ results/viec3 và được chấm lại bằng script trên CPU."),

  H1("6. Hạn chế và việc tiếp theo"),
  B("**Liều huấn luyện không đều.** Với một epoch, batch 2, số bước tối ưu bằng nửa pool: khoảng 1.981 bước ở Design P (suy ra), 436 ở Run A và 951 ở Run C với 1e-5, 220 ở Run A với 5e-4, 700 ở no-filter và 175 ở train-on-gold. Mọi so sánh giữa các nhánh trộn biến cần kiểm với liều."),
  B("**Đối chứng thiếu sức mạnh.** Bản vá đổi 0–4 ví dụ; no-filter và train-on-gold chỉ có hai seed. Em không báo cáo giới hạn tương đương."),
  B("**Khoảng tin cậy chỉ bao phần nhiễu chọn bài và lấy mẫu.** Phần lớn điều kiện có hai hoặc ba seed; Run C ở learning rate cao và các lần chấm lại với trần token chỉ có một lần chạy."),
  B("**Learning rate và phạm vi.** 1e-5 là mặc định chưa tune; lưới learning rate thưa, 3 vòng, k = 4. Mỗi vòng huấn luyện adapter mới từ model gốc nên khả năng tích lũy qua vòng ít chỗ xảy ra; chỉ một model 1,5B, một máy chấm, tối đa 5 vòng; full fine-tuning và RL trực tuyến chưa thử."),
  B("**“Chạm trần” được dựng lại** từ văn bản đã lưu (ngưỡng ≥ 508 trên 512 token), và các lần chấm lại với trần 1.536 chỉ có chỉ báo ký tự cũ."),
  P("Theo hướng đã thống nhất là không thêm thí nghiệm, em chỉ ghi các việc sau như hướng phát triển: một lần chạy gộp có chấm trên tập giữ riêng và một lần chạy tách riêng có cùng số bước tối ưu với Design P để tách nguyên nhân của sụp đổ gộp; lưu số token ngay lúc sinh và thử trần lớn hơn trong vòng lặp; tinh lưới learning rate và lặp Run C; một đối chứng dương (máy chấm cố ý thiên lệch với một định dạng phổ biến) để biết thiết kế này phát hiện được hiệu ứng cỡ nào; và đối chứng vá lỗi lưu đáp án chuẩn (đã viết và kiểm thử đơn vị, sẽ đổi 17–23% pool nên mới là đối chứng thực sự)."),
  gap(),
  P("Em cảm ơn thầy đã dành thời gian xem báo cáo. Em xin nhận góp ý của thầy về các điểm trên.", { alignment: AlignmentType.LEFT }),
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
