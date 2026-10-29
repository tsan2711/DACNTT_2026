# Kịch bản nói: trình bày thẳng trên `paper_revised.pdf`

Kịch bản đi một chiều từ trang 1 tới trang 12, không lật ngược. Tổng thời gian **khoảng 15 phút**, chia như sau:
- **Trang 1–7 (bối cảnh): khoảng 4 phút.** Nói nhanh, chỉ đủ để hiểu các bảng phía sau.
- **Trang 8–11 (các lần chạy gần nhất, Bảng 4–7): khoảng 9 phút.** Đây là phần chính.
- **Trang 12 (kết luận): khoảng 1 phút.**

Phụ lục (trang 14–33) chỉ mở khi thầy hỏi; xem bảng tra ở cuối file.

Quy ước trong kịch bản:
- *[chỉ: …]* là chỗ đưa chuột hoặc ngón tay vào trên trang.
- Các đoạn trích dẫn là lời nói.

---

# PHẦN 1 · BỐI CẢNH (trang 1–7, ≈4 phút)

## Trang 1: tiêu đề, Introduction

*[chỉ: tiêu đề]*

> Thưa thầy, đề tài của nhóm em kiểm tra câu hỏi: model nhỏ có tự giỏi toán lên được không, nếu cho nó tự
> giải bài, tự chọn bài đúng rồi học lại từ chính các bài đó. Vòng lặp này gọi là GVT: sinh lời giải, chấm,
> chọn, huấn luyện. Nhóm thử trên Qwen2.5-1.5B, fine-tune bằng LoRA, máy chấm là math-verify. Kết quả
> là kết quả âm, như tiêu đề ghi: không phát hiện được tiến bộ.

*[chỉ: đoạn 2 mục 1, câu in nghiêng]*

> Máy chấm chỉ so đáp án cuối, không đọc lời giải. Vì vậy câu hỏi có hai nhánh: model giỏi toán hơn thật,
> hay chỉ học cách viết mà máy chấm chịu nhận. Bốn thước đo được chốt trước khi chạy: pass@1, pass@k, kiểu
> chữ (tỉ lệ `\boxed`), và số đề thêm/mất qua từng vòng.

## Trang 2–3: Contributions, Related Work (lướt qua)

*[trang 2, chỉ: Contributions. Sang trang 3, chỉ: "Auditing self-improvement"]*

> Bài gần nhóm em nhất là Xu et al.: nếu không kiểm soát nhiễu giữa các lần train hay giới hạn token, kết
> luận có thể bị lật ngược. Vì vậy ở các lần chạy gần nhất, nhóm tách riêng "lời giải viết xong có đúng
> không" và "lời giải có bị cắt ngang không".

## Trang 3–4: 3.1 vòng lặp, 3.2 máy chấm

*[trang 3, chỉ: mục 3.1]*

> Mỗi vòng gắn một adapter mới lên model gốc. Vòng trước chỉ ảnh hưởng vòng sau qua dữ liệu nó sinh ra.

*[chỉ: mục 3.2, đoạn đầu và "The patch."]*

> Máy chấm từ chối 100% đáp án viết bằng `\dfrac`. Nhóm vá lỗi này để làm đối chứng (Run B).

*[trang 4, chỉ: "The gold-storage defect (post hoc)", ví dụ `\frac43`]*

> Đây là phát hiện mới nhất của nhóm, rút ra khi chấm lại output của các lần chạy gần đây. Đáp án gốc
> được lưu không có `\boxed`, model lại viết `\boxed{}`. Ví dụ gold `\frac43`, model viết
> `\boxed{\frac{4}{3}}`, cùng giá trị nhưng bị chấm sai. Lỗi này loại **15,5–18,4%** lời giải đúng ở mọi
> vòng, khoảng 1 trên 6. Lát nữa khi xem các bảng, thầy lưu ý hai điều. Một: mọi bảng vẫn dùng máy chấm
> gốc, nên mức tụt thật còn **lớn hơn** số trong bảng. Ví dụ Run A ở lr 5e-4 tụt 8,3 và 4,7 điểm; chấm lại
> thì tụt 10,7 và 6,0. Hai: tỉ lệ bị loại nhầm không giảm qua các vòng, tức là model không học cách né lỗi
> này.

## Trang 4–5: 3.3 hai thiết kế, 3.4 cấu hình, Bảng 1, Uncertainty

*[trang 4, chỉ: mục 3.3]*

> Thiết kế P trộn hai bộ dữ liệu và chấm trên chính đề dùng để train. Thiết kế I tách riêng 150 đề thi mà
> model không bao giờ được học. **Mọi bảng gần đây đều là thiết kế I.**

*[trang 4, chỉ: mục 3.4]*

> Model sinh với giới hạn 512 token. Ngoài bốn thước đo chốt trước, nhóm dùng thêm **độ chính xác mẫu**
> (trung bình đúng trên cả k lời giải, ít nhiễu hơn pass@1); thước đo này được chọn sau khi chạy.

*[trang 5, chỉ: Bảng 1, bốn dòng cuối]*

> Bảng 1 liệt kê mọi run. Các lần chạy gần nhất là bốn dòng cuối, đều ở lr 5e-4: A và B, nhánh không lọc,
> nhánh học lời giải gốc, một bản chạy lặp, và Run C trên GSM8K.

*[chỉ: "Uncertainty."]*

> Mọi thay đổi đều kèm khoảng tin cậy 95%, tính bằng bootstrap trên 150 đề thi. Khoảng này không tính nhiễu
> giữa các lần train: chạy lặp cùng cấu hình đã lệch 3,2 điểm. Vì vậy nhóm chỉ tin những xu hướng lặp lại
> qua nhiều run.

## Trang 6–7: 4.1, 4.2 (vì sao phải chạy lại ở lr cao)

*[trang 6, chỉ: Bảng 2, dòng 1.5B pass@1]*

> Thiết kế gộp ban đầu tụt từ 50,0 xuống 18,6%. Nhưng thiết kế đó chấm trên tập train và train nhiều hơn
> khoảng 4,5 lần mỗi vòng, nên chưa kết luận được nguyên nhân.

*[trang 7, chỉ: Hình 1]*

> Làm lại bằng thiết kế cô lập ở lr 1e-5 thì đường gần như đi ngang. Nhưng nhóm kiểm tra thấy ở lr này
> output gần như không đổi, tức là bước train làm được quá ít. **Đó là lý do có loạt chạy gần nhất ở
> learning rate cao hơn**, em xin đi vào phần chính.

---

# PHẦN 2 · CÁC LẦN CHẠY GẦN NHẤT (trang 8–11, ≈9 phút)

## Trang 8: 4.3 (nói 1 câu), rồi 4.4 và Bảng 4

*[trang 8, chỉ: mục 4.3]*

> Một câu về đối chứng vá `\dfrac`: nó không đo được gì, vì `\dfrac` chỉ có trong 0,50–0,73% lời giải nên
> tập train của A và B chỉ khác nhau 3–4 bài.

*[chỉ: mục 4.4, rồi Bảng 4]*

> Loạt chạy mới dùng 3 lr cao hơn (1e-4, 2e-4, 5e-4), 3 vòng, mỗi đề 4 lời giải. Mỗi lr chạy 2–3 seed,
> mỗi seed là một bộ đề thi khác nhau. Bảng 4 là Run A qua các lr. Em xin đọc theo cột.

*[chỉ: cột "pass@1" và "pass@4"]*

> **Không dòng nào tăng thật sự.** Dòng tốt nhất là 1e-4 seed 1, pass@1 từ 33,3 lên 34,0, chỉ 0,7 điểm,
> nằm trong nhiễu. Ở 5e-4 cả hai seed đều tụt: pass@1 còn 23,3 và 27,3.

*[chỉ: cột "Sample acc."]*

> Độ chính xác mẫu giảm ở mọi dòng. Ở seed 1, mức giảm tăng dần theo lr: 1,5, rồi 3,5, rồi 8,3 điểm. Còn ở
> seed 2 thì gần như phẳng: 3,7, 3,8, 4,7. Nên "lr càng cao càng tụt" mới chỉ là gợi ý, thấy rõ ở một seed.

*[chỉ: cột "Cap-hit (R2)"]*

> Cột này là tỉ lệ lời giải chạm giới hạn 512 token, tức bị cắt ngang. Ở vòng 0, model gốc đã chạm giới hạn
> ở khoảng 43%. Ở 1e-4 và 2e-4 tỉ lệ này đứng yên hoặc giảm; chỉ ở 5e-4 mới tăng, lên 46,2 và 51,2%.

*[chỉ: cột "Added/lost"]*

> Cột cuối là số đề mới giải được so với số đề mất đi. Mọi dòng đều mất bằng hoặc nhiều hơn được, trừ
> 1e-4 seed 3 (16/14).

> Cũng ở 5e-4, A và B (bản vá) cho chênh lệch đổi chiều theo seed: +5,3 ở seed 1, −7,3 ở seed 2, dù tập
> train ban đầu gần như giống hệt nhau. Nhiễu giữa các lần train lớn cỡ vài điểm.

## Trang 9: Bảng 5 (bảng khoảng tin cậy, bảng quan trọng nhất)

*[trang 9, chỉ: tiêu đề Bảng 5]*

> Bảng 5 gom mọi run vào một chỗ: thay đổi từ vòng 0 tới vòng cuối, kèm khoảng tin cậy 95% trong ngoặc.

*[chỉ: cột "∆pass@1" và "∆pass@k"]*

> Thầy có thể dò cả hai cột: không khoảng nào nằm hẳn trên 0. Không có bằng chứng tiến bộ ở bất kỳ run nào.

*[chỉ: cột "∆sample acc.", hai dòng có +2,2]*

> Ở cột độ chính xác mẫu, đầu trên của khoảng cao nhất là +2,2. Từ đó nhóm nói: mức tăng trên khoảng 2,2
> điểm không phù hợp với dữ liệu. Đây là cận lỏng, vì không tính nhiễu giữa các lần train, và nếu chấm lại
> không có lỗi `\boxed` thì cận này gần 3 điểm.

*[chỉ: khối "Learning rate 5×10⁻⁴"]*

> Khối 5e-4 là các lần chạy gần nhất. Cả bốn run A và B đều giảm độ chính xác mẫu, và khoảng tin cậy đều
> loại 0: −8,3, −4,7, −6,7, −9,2. Nhánh không lọc giảm −8,2 và −10,2. Học lời giải gốc giảm mạnh nhất:
> −19,7 và −18,7. Run C trên GSM8K giảm −15,3.

*[chỉ: cột cuối "Finished, matched"]*

> Cột cuối là phép đo mới: độ chính xác chỉ tính trên lời giải viết xong, so với model gốc trên đúng các đề
> đó. Ở 5e-4, lời giải viết xong kém chính xác hơn 5,5–10,6 điểm. Năm trên sáu run self-training có khoảng
> tin cậy loại 0.

*[chỉ: đoạn "Two controls at 5×10⁻⁴"]*

> Ở 5e-4 nhóm chạy thêm hai đối chứng, mỗi cái hai seed. **Không lọc**: model học mọi lời giải, đúng sai
> đều học (1.400 bài mỗi vòng), tức là bỏ hẳn máy chấm. **Học lời giải gốc**: bỏ qua output của model, học
> 350 lời giải mẫu do người viết.

## Trang 10: Bảng 6 (đối chứng), rồi 4.5

*[trang 10, chỉ: Bảng 6, cột "Pool"]*

> Lưu ý cột Pool. Nhánh không lọc train 1.400 bài mỗi vòng, gấp 3–4 lần nhánh A. Nhánh học lời giải gốc
> train 350 bài, gần bằng A.

*[chỉ: dòng "No filter" so với dòng "A"]*

> Bỏ lọc so với giữ lọc, ở vòng 2: pass@1 chênh +4,0 ở seed 1 và −4,7 ở seed 2, đổi chiều. pass@4 kém hơn ở
> cả hai seed (−2,0 và −5,3) nhưng khoảng tin cậy vẫn chứa 0. Kết luận: bỏ máy chấm không tốt hơn. Nhưng vì
> lượng train khác nhau quá nhiều, nhóm không quy kết quả này cho máy chấm.

*[chỉ: dòng "Train on gold"]*

> Kết quả bất ngờ nhất: học lời giải mẫu của người lại tụt mạnh nhất. pass@1 ở vòng 2 còn 15,3 và 10,0,
> pass@4 giảm khoảng 21 điểm. Model chuyển hẳn sang kiểu viết của lời giải mẫu: lời giải có ký hiệu `$` đi
> từ 5% lên 98%. Nhóm kiểm tra xem đây có phải máy chấm chấm sai kiểu viết mới không: phần chấm sai đó chỉ
> cỡ 2 điểm, còn độ chính xác trên lời giải viết xong rơi xuống 12–15%. Nên phần lớn mức tụt là thật.

*[chỉ: mục 4.5, đoạn đầu]*

> Mục 4.5 trả lời câu hỏi "tụt kiểu gì". Model gốc đã chạm giới hạn 512 token ở 41–48% lời giải MATH-500,
> nghĩa là giới hạn này bó ngay từ đầu. Mức tụt có hai nguồn: lời giải viết xong kém chính xác hơn, và lời
> giải bị cắt ngang nhiều hơn. Bảng 7 ở đầu trang sau tách hai nguồn này.

## Trang 11: Bảng 7, rồi 5.1 và 5.2

*[trang 11, chỉ: Bảng 7, cột "∆cap-hit"]*

> Cột đầu là mức tăng tỉ lệ bị cắt ngang. Ở seed 2, cả ba run tăng rõ (+8,2, +11,0, +14,2), khoảng tin cậy
> loại 0. Ở seed 1 thì nhỏ, phần lớn chứa 0.

*[chỉ: hai dòng "A replicate" và "A, 1024 limit"]*

> Hai dòng này là hai lần chạy mới nhất. "A replicate" chạy lặp đúng cấu hình Run A. "1024 limit" train với
> giới hạn 1.024 token để không lời giải nào bị cắt khi train. Cả hai đều vẫn tụt (−5,2 và −5,7) mà tỉ lệ
> cắt ngang không tăng. Vậy việc cắt lời giải khi train không phải nguyên nhân chính.

*[chỉ: cột "Fin. share"]*

> Cột cuối cho biết phần mức tụt do lời giải kém chính xác: 62–74% ở seed 1, 34–59% ở seed 2. Ở lr 1e-4 và
> 2e-4, gần như toàn bộ mức tụt là do lời giải kém chính xác. Tóm lại: ở lr cao nhất cả hai nguồn cùng góp,
> tỉ lệ khác nhau theo bộ đề; ở lr thấp hơn chỉ có nguồn "kém chính xác".

*[chỉ: mục 5.1. Mục bắt đầu ở cuối trang 10; trên trang 11 chỉ vào hai câu in nghiêng]*

> Trả lời câu hỏi đề tài. **Model có giỏi toán hơn không?** Không phát hiện được, ở cả bốn lr, như Bảng 5.
> **Có học chữ của máy chấm không?** Chưa xác định được: luật chốt trước cần pass@1 tăng, mà pass@1 không
> tăng. **Cú sụp ở thiết kế gộp từ đâu ra?** Chưa biết, vì thiết kế đó còn train nhiều gấp khoảng 4,5 lần.

*[chỉ: mục 5.2, câu in nghiêng]*

> Kết luận hẹp mà nhóm dám nói: bỏ một lỗi định dạng có trong dưới 1% lời giải, hoặc bỏ hẳn máy chấm,
> không tạo khác biệt nhất quán ở độ phân giải của thí nghiệm này.

---

# PHẦN 3 · KẾT (trang 12, ≈1 phút)

*[trang 12, chỉ: mục 6]*

> Giới hạn: lượng train giữa các nhánh không bằng nhau; đa số cấu hình chỉ có hai seed; chỉ một model và
> một máy chấm. Không nhánh nào, kể cả học lời giải mẫu, tốt hơn vòng 0.

*[chỉ: mục 7]*

> Tóm lại: ở quy mô 1.5B, với LoRA và máy chấm luật, vòng lặp tự học không cho thấy tiến bộ đo được. Ở lr
> cao thì model tụt, chủ yếu vì lời giải viết xong kém chính xác hơn. Việc tiếp theo hợp lý nhất là train
> lại với bản vá `\boxed`: bản vá này đổi khoảng 1/5 tập train (440 lên 542 bài), có tác động thật, khác
> hẳn bản vá `\dfrac`.

> Em xin hết phần trình bày. Nhóm có demo chạy trực tiếp lỗi máy chấm nếu thầy muốn xem.

---

## Demo (nếu thầy cho, ≈1 phút)

Chạy ở thư mục gốc repo:

```bash
.venv/bin/python 25-10-2026/demo_verifier.py --live 200
```

- Nhấn Enter để qua 4 phần: ví dụ `\frac43` → ví dụ thật → bảng 15,5–18,4% → chấm trực tiếp.
- Nếu máy lỗi, mở `25-10-2026/demo_output.txt`.
- Phần chấm trực tiếp dao động theo mẫu (13–20%), nên khi nói hãy trích bảng ở phần 3.

## Khi thầy hỏi sâu thì mở phụ lục

| Câu hỏi | Mở |
|---|---|
| Số chấm lại không có lỗi `\boxed` cho từng run? | B · trang 15–17 |
| Bootstrap làm thế nào, có sửa đa so sánh không? | C · trang 18 |
| Thiết kế P tách theo từng bộ dữ liệu? | D · trang 18–19 (Bảng 8, 9) |
| Loss có giảm ở 1e-5 không? | E · trang 20 |
| Bảng A/B đầy đủ ở 5e-4, tỉ lệ `\boxed` từng vòng, Run C ở 5e-4? | G · trang 22–23 (Bảng 10) |
| Độ dài lời giải, tỉ lệ bị cắt ở từng run; chấm lại với giới hạn 1.536 token? | H · trang 25–28 (Bảng 11, 12) |
| So với các bài khác? | A · trang 14 |
| Giới hạn đầy đủ / hướng tiếp theo? | J · trang 31 / K · trang 33 |
