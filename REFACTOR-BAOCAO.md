# Refactor báo cáo: neo vào câu hỏi gốc

Tạo ngày 18/10/2026, sau khi báo cáo 11/10 bị nhận xét "AI làm từ đầu tới cuối, người làm không hiểu vấn đề".

Cách dùng file này: mỗi bước có 3 phần.
- **Làm gì.**
- **Hợp lý không?** Lập luận và kiểm tra lại bằng số thật.
- **Câu tự kiểm tra.** Sang và Duy Anh tự trả lời bằng lời của mình. Chưa trả lời được thì chưa sang bước sau.

Văn báo cáo do nhóm tự viết. File này chỉ là khung và lập luận.

---

## Bước 0. Điểm neo

Đề và câu hỏi đã chốt ngày 16/08 trong `TOI-HIEU.md`. Không đổi:

> Học sinh có giỏi toán hơn thật không, hay chỉ học chữ giáo viên ưa?

Từ đầu đã đặt **4 thước đo**:
1. pass@1
2. pass@k
3. chữ viết: tỉ lệ có `\boxed`, `\dfrac`… lấy từ bảng `styles` trong `table.md`
4. bảng đề A/B/C: A = thêm đề, B = ổn định hơn, C = mất đề

Luật đọc kết quả:
- Chỉ khi có đủ ba dấu hiệu là pass@1 tăng, pass@k đứng yên, chữ tụ về một kiểu thì mới được nói "học chữ".
- Thiếu bất kỳ mảnh nào thì chỉ được nói "chưa chắc".

**Hợp lý không?** Báo cáo 11/10 lại đặt đề là *"Verifier Bias Is Not Enough… Capability Collapse"*, tức là câu hỏi "lỗi máy chấm có gây sụp đổ không". Đó là câu hỏi phụ, lại nằm sát vùng `KHONG-LAM.md` đã loại trừ (sửa máy chấm). **Đây là chỗ trôi đề lớn nhất.** Mọi bước dưới đây đều đo lại theo câu hỏi gốc và 4 thước đo gốc.

**Câu tự kiểm tra:**
- (0a) pass@k với k = 4 nghĩa là gì?
- (0b) Vì sao pass@1 tăng thôi thì chưa nói được là model giỏi toán hơn?

---

## Bước 1. Chuỗi việc từ đầu, kiểm tra xem có liền mạch không

| Việc | Hỏi gì | Kết quả | Dẫn tới |
|---|---|---|---|
| 1 | Máy chấm có gạch bài đúng vì cách viết không? | Có. `\dfrac` bị gạch 100%, thập phân `0.50` bị gạch 59% (MATH) | Đi tiếp việc 2 |
| 2 | Trên bài model thật, máy chấm gạch nhầm bao nhiêu? | MATH 7,8% (10/128), GSM8K 0%. 8/10 ca là **lôi nhầm số**, chỉ 2/10 là do cách viết | Đi tiếp việc 3 |
| 3 | Chạy vòng GVT, model có giỏi lên không? | Xem bước 2 | |

**Hợp lý không?** Việc 1 → 2 → 3 liền mạch, và đây là phần nhóm tự viết, giọng đơn giản, đúng đề. Nhưng có một lỗ hổng mà lẽ ra phải thấy trước khi chạy Run B:
- Bản vá của Run B chỉ đổi `\dfrac`/`\tfrac` thành `\frac` (`src/dacntt/read.py:50`).
- Ở vòng 0, model chỉ viết `\dfrac` trong **12/2000 lời giải (0,6%)** (`results/viec3/a-math500-lr-fixed/table.md`).
- Vậy A và B chỉ khác nhau ở khoảng 0,6% dữ liệu. **Kết quả "vá không có tác dụng" đoán được từ trước, chỉ bằng một phép đếm.**

Đây không phải phát hiện, mà là một bài học về thiết kế. Nên nói thẳng điều này trong báo cáo.

**Câu tự kiểm tra:**
- (1a) "Lôi nhầm số" và "viết đúng mà máy không nhận" khác nhau thế nào? Cho một ví dụ mỗi loại từ `results/viec2/fn_samples.md`.
- (1b) Vì sao chỉ đếm `\dfrac` ở vòng 0 là đã đoán được A ≈ B?

---

## Bước 2. Trả lời câu hỏi gốc bằng 4 thước đo gốc

Số lấy thẳng từ `results/viec3/*/table.md`, đã kiểm tra lại ngày 18/10.

- **Chữ** = tỉ lệ lời giải có `\boxed`.
- **Thêm / mất** = tổng số đề A và C qua vòng 1 và vòng 2 (so vòng sau với vòng trước, trên 150 đề).

| Lần chạy | lr | seed | pass@1 v0→v2 | pass@4 v0→v2 | \boxed v0→v2 | thêm / mất |
|---|---|---|---|---|---|---|
| Self-train (A) | 1e-4 | 1 | 33,3→34,0 | 50,0→49,3 | 52→46% | 20 / 21 |
| | 1e-4 | 2 | 31,3→28,0 | 51,3→45,3 | 54→48% | 25 / 34 |
| | 1e-4 | 3 | 29,3→26,7 | 40,0→41,3 | 54→47% | 16 / 14 |
| | 2e-4 | 1 | 33,3→31,3 | 50,0→46,7 | 52→45% | 23 / 28 |
| | 2e-4 | 2 | 31,3→25,3 | 51,3→45,3 | 54→50% | 21 / 30 |
| | 5e-4 | 1 | 33,3→23,3 | 50,0→42,7 | 52→36% | 22 / 33 |
| | 5e-4 | 2 | 31,3→27,3 | 51,3→44,7 | 54→37% | 26 / 36 |
| Không lọc | 5e-4 | 1 | 33,3→27,3 | 50,0→40,7 | 52→38% | 21 / 35 |
| | 5e-4 | 2 | 31,3→22,7 | 51,3→39,3 | 54→34% | 22 / 40 |
| Học lời giải mẫu | 5e-4 | 1 | 33,3→15,3 | 50,0→29,3 | 52→**86%** | 15 / 46 |
| | 5e-4 | 2 | 31,3→10,0 | 51,3→30,7 | 54→**84%** | 23 / 54 |

**Đọc theo luật ở bước 0:**
1. **pass@1 không tăng ở lần chạy nào.** Vế "tự cải thiện" của đề không đứng được ở model 1,5B với cách huấn luyện này.
2. **Self-train không "học chữ máy chấm ưa".** Máy chấm đọc đáp án trong `\boxed`, vậy mà tỉ lệ `\boxed` lại **giảm** (52% → 36% ở 5e-4). Model chạy *xa khỏi* kiểu viết máy chấm ưa: viết dài ra và không chốt đáp án.
3. **Ca "học chữ" rõ nhất lại là ca không có máy chấm:** học lời giải mẫu. Chữ tụ hẳn về một kiểu (`\boxed` 52% → 86%, dấu `$` 5% → 98%), nhưng điểm sụp. Đây là trường hợp 4 trong `TOI-HIEU.md`, chỉ chữ tụ mà không có điểm đi kèm, và thực tế còn tệ hơn vì điểm giảm.
4. **Ở mọi mức lr, số đề mất ≥ số đề thêm.** Kể cả ở 1e-4, nơi pass@k gần như đứng yên, mỗi vòng vẫn có khoảng 10 đề được thêm và khoảng 10 đề bị mất. Phần lớn là xáo trộn, không phải học được đề mới.

**Hợp lý không? (kiểm tra nhiễu)**
- Model gốc chưa huấn luyện, cùng 150 đề thi của seed 1, chỉ lấy mẫu lại một lần (`results/viec3/base-reeval/reeval_0.json`, giới hạn 512 token): pass@1 **36,0** so với 33,3 ở vòng 0. Độ chính xác mẫu 36,3 so với 33,7.
- **Chỉ riêng việc lấy mẫu lại đã lệch khoảng 2,7 điểm.**
- Vậy:
  - mức giảm ở 1e-4 (khoảng 2 điểm) **nằm trong nhiễu**;
  - mức giảm ở 5e-4 (khoảng 6–10 điểm pass@1) lớn hơn nhiễu khoảng 2–4 lần;
  - chênh A–B (+5,4 rồi −7,3) **nằm trong nhiễu**.
- Đây mới là một lần lấy mẫu lại, chưa phải khoảng tin cậy. Muốn có khoảng tin cậy thì dùng bootstrap trên `generations.jsonl`: nhóm tự tính, chạy CPU, không cần GPU.

**Câu tự kiểm tra:**
- (2a) Vì sao tỉ lệ `\boxed` giảm lại là bằng chứng *chống lại* giả thuyết "học chữ máy chấm ưa"?
- (2b) Vì sao học lời giải mẫu (dữ liệu sạch, đúng 100%) lại tệ hơn tự học? Nhóm có *chứng minh* được nguyên nhân không? (Đáp án: chưa. Chỉ có giả thuyết.)
- (2c) Một đề 1 = 0,67 điểm. Chênh 2,7 điểm là khoảng bao nhiêu đề?

---

## Bước 3. Giữ, hạ giọng, hay bỏ từng ý trong báo cáo cũ

| Ý trong báo cáo 11/10 | Quyết định | Lý do (so với neo) |
|---|---|---|
| Đề tiếng Anh "Verifier Bias Is Not Enough…" | **Bỏ**, quay về đề gốc | Trôi đề, xem bước 0 |
| Learning rate 1e-5 quá thấp, đường cong phẳng là do chưa học | **Giữ**, kể như *lỗi của nhóm* | Đây là bài học thật: phải xem đường loss trước khi kết luận |
| Mức giảm tăng theo lr | **Giữ** | Là kết quả mạnh nhất, có 7 lần chạy, 3 mức lr |
| "Bản vá không có tác dụng" | **Hạ giọng**: "không đo được khác biệt, và đoán được từ trước vì `\dfrac` chỉ 0,6%" | Xem bước 1 |
| Không lọc ≈ có lọc | **Giữ** | Trả lời trực tiếp vế "verify/select" của đề: bộ lọc không tạo khác biệt |
| Học lời giải mẫu tệ hơn | **Giữ kết quả, bỏ giải thích** | Số bước huấn luyện các đối chứng không bằng nhau (1.400 / ~430 / 350 ví dụ), cơ chế chưa kiểm chứng |
| Chỉ số "lan man" (>1.500 ký tự, không `\boxed`) | **Hạ xuống phụ**, dùng tỉ lệ `\boxed` làm chính | `\boxed` là thước đo đặt từ đầu. "Lan man" là ngưỡng đặt ra sau khi đã nhìn thấy dữ liệu |
| Cắt cụt 512 token, giới hạn token khi đánh giá | **Bỏ khỏi báo cáo chính** (để phụ lục nếu cần) | Kiểm tra kỹ thuật, không trả lời câu hỏi gốc |
| Run C (GSM8K, 5e-4) | **Giữ một dòng**, ghi rõ chỉ có 1 seed | Có ích để so dữ liệu dễ / khó, nhưng còn yếu |
| Mục 3.4 xử lý treo Kaggle | **Bỏ** | Hạ tầng, không phải nghiên cứu |
| Related work (Xu, Kim, Egashira) | **Chỉ giữ bài nào nhóm đã tự đọc** và nói được 1 câu bằng lời mình | Không đọc thì không trích |
| 3 vòng, k = 4 (đề cương 5 vòng, k = 8) | **Nói rõ trong phần giới hạn** | Lý do là quota GPU. Các lần chạy lr 1e-5 cũ có đủ 5 vòng, k = 8 |

**Câu tự kiểm tra:**
- (3a) Vì sao một thước đo đặt ra *sau khi* nhìn dữ liệu lại yếu hơn thước đo đặt trước?

---

## Bước 4. Khung báo cáo mới (2–3 trang, nhóm tự viết văn)

1. **Đề và câu hỏi** (5 dòng). Dùng câu neo, kèm ví dụ "học sinh và giáo viên keo".
2. **Đã làm gì.** Việc 1 → 2 → 3, mỗi việc 2–3 dòng, kèm 1 con số.
3. **Kết quả chính.** Một bảng rút từ bước 2 (chọn 1 seed cho mỗi dòng, ghi kết quả seed kia trong ngoặc) và **một hình**: tỉ lệ `\boxed` ở vòng 2 theo lr, 3 điểm, vẽ bằng tay hoặc Excel cũng được.
4. **Trả lời câu hỏi gốc.**
   - Không thấy tự cải thiện.
   - Không thấy học chữ máy chấm.
   - Huấn luyện càng mạnh thì model càng bỏ chốt đáp án.
5. **Nhóm đã sai ở đâu.**
   - lr 1e-5 không được kiểm tra suốt nhiều tuần.
   - Run B đoán được trước.
   - Câu chuyện đã đổi 3 lần, và vì sao.
6. **Giới hạn.** 150 đề, nhiễu khoảng 2,7 điểm, 3 vòng, k = 4, 2–3 seed.
7. **Khai báo dùng AI.** Phần nào AI làm, phần nào nhóm tự kiểm tra.

---

## Bước 5. Đánh giá lại tổng thể

Mục này làm *sau khi* nhóm viết xong bản mới. Kiểm tra theo danh sách:

- [ ] Mỗi kết luận trong bản mới trả lời được câu neo, hoặc nói rõ là ý phụ?
- [ ] Mỗi con số tra ngược được về một file trong `results/`?
- [ ] Không còn câu nào khẳng định cơ chế mà chưa kiểm chứng?
- [ ] Mỗi chênh lệch được báo cáo đều so với mức nhiễu khoảng 2,7 điểm?
- [ ] Cả hai người trả lời được hết các câu tự kiểm tra 0a–3a mà không mở tài liệu?
- [ ] Đọc to bản báo cáo: có câu nào mình không tự nói ra được không? Câu đó viết lại.

**Đánh giá sơ bộ của agent, ngày 18/10, trước khi nhóm viết:**
- Dữ liệu đủ để trả lời câu hỏi gốc, **không cần chạy thêm GPU**.
- Câu trả lời trung thực là kết quả âm, có một phát hiện phụ rõ ràng (lr ↔ bỏ chốt đáp án), cộng với hai bài học về thiết kế.
- Điểm yếu còn lại: chưa có khoảng tin cậy, và số seed ít.
- Rủi ro lớn nhất không nằm ở dữ liệu, mà ở việc nhóm có giải thích được các câu tự kiểm tra hay không.
