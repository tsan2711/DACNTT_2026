# Lịch trình hoàn thiện — chia theo công việc, không chia theo tuần

Có agent hỗ trợ, phần code/viết/phân tích làm nhanh hơn nhiều so với tốc độ
người tự gõ — chia theo tuần chỉ tạo trần giả. Cấu trúc đúng là một **chuỗi
việc có phụ thuộc (dependency chain)**, xoay quanh một nút thắt thật duy
nhất.

> **Cập nhật 2026-09-05:** Track A đã xong toàn bộ về mặt code (xem bên
> dưới). Ngoài ra, tìm lại được `generations.jsonl` gốc của 2 lần chạy
> Kaggle cũ (tưởng mất), phân tích thử cho thấy thiết kế `--dataset both`
> (gộp 2 bộ đề) bị **nhiễm chéo** — không tách được "tại verifier lệch"
> khỏi "tại lây từ bộ đề kia". Track B đổi thiết kế: từ "R1–R5 trên
> `--dataset both`" sang **3 lần chạy cô lập từng bộ đề (A/B/C)** + seed +
> ablation. Xem lý do đầy đủ ở `papers/KE-HOACH-MO-RONG.md`.
>
> **Nhịp báo cáo (2026-09-05):** code đã xong nhanh hơn nhịp báo cáo hàng
> tuần thật — để báo cáo tuần cho thầy không bị nhảy cóc kiểu "tuần này
> làm xong cả một track", nội dung Track A được *tiết lộ dần* qua 2 kỳ báo
> cáo thay vì dồn hết vào tuần 2: tuần 2 chỉ báo cáo phần "phát hiện nhiễm
> chéo" (không nói đã code xong 4 cờ + 3 công cụ + test); phần hạ tầng
> code (`--seed/--patch-verifier/--holdout-frac/--no-filter`, công cụ phân
> tích, 21/21 test) và kế hoạch A/B/C chi tiết dời sang báo cáo tuần 3.
> Đây chỉ là nhịp *trình bày*, không phải nhịp *code thật* — file này vẫn
> ghi trạng thái code thật (đã xong) để tự theo dõi.

## Nút thắt duy nhất: GPU-giờ Kaggle

Mọi việc code/viết/phân tích agent làm gần như ngay lập tức. Cái không rút
ngắn được là **thời gian chạy thật trên GPU**. Số đo thật
(`experiments/viec3/KAGGLE.md`, đo 2026-08-27): 0.5B, 500+500 đề (`both`),
k=8, 1 vòng ≈ 6.7 tiếng → 1 lần chạy full 5 vòng ≈ 33+ tiếng GPU với thiết
kế gộp cũ. Thiết kế cô lập mới (A/B/C, mỗi lần chỉ 1 bộ đề, n=500 thay vì
n=1000) ước tính nhẹ hơn khoảng một nửa: **~15–17 tiếng/lần cho 0.5B**, 1.5B
kỳ vọng chậm hơn.

Vẫn vượt trần 12h/phiên Kaggle free tier, nên mỗi lần chạy vẫn cần chia
nhiều phiên nối tiếp (`_save_partial` đã tự ghi kết quả sau mỗi vòng, phiên
sau đọc tiếp được, không mất trắng nếu Kaggle tự ngắt giữa chừng) — nhưng
nhẹ hơn hẳn thiết kế gộp cũ, và 6 lần chạy cô lập (A, B, C, 2 seed, 1
ablation) tổng GPU-giờ ước tính **thấp hơn hoặc tương đương** 5 lần chạy gộp
của kế hoạch trước.

Vì vậy: **làm hết mọi việc không cần GPU trước (Track A — đã xong), dồn hết
GPU-giờ cho đúng thứ tự lần chạy cần thiết (Track B).**

---

## Track A — đã xong (không tốn GPU)

- [x] **A1. `generations.jsonl` luôn được lưu** — hoá ra code đã làm việc
      này từ commit đầu tiên, không cần sửa. 2 lần chạy cũ chỉ thiếu vì
      chưa tải file về từ Kaggle, không phải lỗi code.
- [x] **A2. Tìm lại log gốc 2 lần chạy Kaggle cũ** — tìm được qua link
      Kaggle output signed-URL, tải về `results/viec3/{qwen05b,qwen15b}-n500/generations.jsonl`.
      Đã chạy `analyze_by_dataset.py`: phát hiện nhiễm chéo (xem cập nhật ở
      đầu file này và `papers/KE-HOACH-MO-RONG.md`).
- [x] **A3. `--seed`, `--patch-verifier`, `--holdout-frac`, `--no-filter`**
      — cả 4 cờ đã thêm vào `experiments/viec3/run.py` (mặc định giữ nguyên
      hành vi cũ), có test (`tests/test_gvt.py`, `tests/test_verify_adapter.py`),
      21/21 test pass.
- [x] **A4/A5/A6.** Nằm trong A3 — verifier vá (`normalize_frac_commands`),
      chia train/test (`train_item_ids`/`test_item_ids`), ablation không lọc
      (`select_all`) đều đã code và test xong.
- [x] **A7. Phân tích cơ chế** — `src/dacntt/report/mechanism.py` +
      `experiments/viec3/analyze_mechanism.py` (train loss + đa dạng đáp
      án), và `experiments/viec3/analyze_by_dataset.py` (tách theo dataset +
      tỉ lệ pool). Đã chạy trên log cũ, kết quả có trong
      `results/viec3/mechanism.md` và `results/viec3/*/by_dataset.md`.
- [ ] **A8. Đọc-hiểu `CHECKLIST-TUAN-2.md`** — việc của Bi, agent không làm
      thay được.

---

## Track B — hàng đợi GPU, làm tuần tự theo đúng thứ tự này

Lệnh chạy đầy đủ cho từng bước nằm ở `experiments/viec3/KAGGLE.md` (mục
"Ô 5"). Tất cả dùng `--model Qwen/Qwen2.5-1.5B-Instruct --n 500 --rounds 5
--k 8 --max-tokens 512 --holdout-frac 0.3`, chỉ khác `--dataset`/
`--patch-verifier`/`--seed`/`--no-filter`.

> **Cập nhật 2026-09-08:** A, B, C đã chạy xong đủ cả 3 (`results/viec3/
> qwen15b-math500-a/`, `-b/`, `results/viec3/qwen15b-gsm8k-c/`). Kết quả
> **không khớp dự đoán ở cả 3 lần**: A không sụp (pass@1 −2.7, pass@8 đứng);
> B (verifier đã vá) gần trùng A — vá verifier không đổi gì đáng kể, **bác
> bỏ trực tiếp** giả thuyết gốc; C sụp nhẹ pass@1 (−12.7, dồn vòng cuối),
> pass@8 vẫn phẳng. Cú sụp nặng trong log gộp cũ phần lớn là hiện vật thiết
> kế đo (train gộp + chấm trên đề đã train), không phải verifier lệch. Số
> thật + suy luận đầy đủ + việc còn lại: `papers/KET-QUA-CO-LAP-AC.md`.

1. [x] **A — MATH-500 cô lập, verifier gốc.** Xong 2026-09-05. Số headline
   mới (đã tách train/test, không còn nhiễm GSM8K), mốc so sánh cho B.
2. [x] **C — GSM8K cô lập, verifier gốc.** Xong 2026-09-06 (~5.5h GPU).
   Verifier ở đây gần sạch tự nhiên — vẫn erode pass@1 nhẹ nhưng KHÔNG sụp
   pass@8, và đáp án phân tán hơn theo vòng (ngược mode-collapse).
3. [x] **B — MATH-500 cô lập, verifier vá.** Xong 2026-09-06/08. So A vs B
   (control 1-biến sạch): hai đường cong gần như trùng nhau — vá verifier
   không tạo khác biệt đo được. **Bộ 3 A/B/C đã đủ.**
4. **Seed thứ 2/3** — lặp lại đúng cấu hình được chọn làm headline sau khi
   thấy A/B/C (nhiều khả năng A hoặc B trên MATH-500), chỉ đổi `--seed`.
5. **Ablation không lọc** — cùng dataset/model với headline, thêm
   `--no-filter`.

**Không bắt buộc, chỉ chạy nếu còn GPU-giờ dư:** model thứ ba, chạy dài hơn
5 vòng, họ model khác (Giai đoạn 5 trong `KE-HOACH-MO-RONG.md`).

**Không được nhảy cóc bỏ A hoặc C** — cả hai là ranh giới cứng đã chốt
(xem "Nếu GPU-giờ bị hạn chế" bên dưới).

---

## Track C — chỉ làm được sau khi có dữ liệu từ Track B

- [x] **C1. Chạy `analyze_mechanism.py` trên log A/B/C** — xong 2026-09-08,
      kết quả gộp ở `results/viec3/mechanism-ABC.md` (train-loss + đa dạng
      đáp án của cả 3 lần chạy cạnh nhau).
- [~] **C2. Gộp số liệu mới vào `papers/latex/paper.tex`** — **đã viết lại
      toàn bộ bài 2026-09-09** theo kết luận A/B/C (đổi title, Abstract,
      Introduction, thêm §3.3 hai thiết kế P/I, Results §4.1–4.5, Discussion
      rút lại claim shrinking-pool, Limitations 6 mục, Conclusion). Còn
      thiếu: số seed lặp + ablation → khi có thì khoá bảng `tab:isolated`
      và bỏ hedging "single seed". Bản nháp cũ `papers/DRAFT.md` đã đánh dấu
      lỗi thời, không dùng nữa.
- [ ] **C3. Compile thử qua Overleaf** — **chưa làm, máy không có LaTeX**.
      Đã tự kiểm tra bằng script: ngoặc cân, 6 table / 2 figure / 6 tabular
      khớp begin-end, không có `\ref`/`\cite` treo, Abstract 246 từ (trong
      giới hạn LNCS 150–250). Nhưng chưa chạy `pdflatex` thật lần nào.
- [ ] **C4. Tự đọc lại toàn bài bằng giọng của mình** (việc của Bi).
- [x] **C5. Cập nhật `THUYET-TRINH.md`** — xong 2026-09-09, viết lại theo
      câu chuyện mới (giả thuyết → tưởng đúng → phát hiện confound → làm
      lại sạch → bị bác bỏ → thu gọn scope), kèm mục "nếu thầy hỏi thêm".

---

## Báo cáo Chủ nhật hàng tuần — điểm chốt trạng thái, không phải deadline ép việc

Mỗi Chủ nhật: báo cáo đã tới đâu trong chuỗi A→C→B→seed→ablation, không phải
"tuần này phải xong việc gì". Nếu Kaggle nghẽn quota, báo đang chờ, không
dồn ép chạy ẩu.

---

## Nếu GPU-giờ bị hạn chế: thứ tự cắt giảm

1. Cắt trước: model thứ ba, chạy dài hơn, họ model khác (không nằm trong
   Track B bắt buộc).
2. Cắt tiếp nếu vẫn thiếu: seed thứ 3 — dùng 2 seed thay vì 3.
3. Cắt tiếp nếu vẫn thiếu: ablation không lọc — ghi rõ vào Limitations là
   chưa làm được.
4. **Không được cắt: A và C.** Đây là ranh giới cứng — A là headline mới, C
   là thí nghiệm duy nhất trả lời được câu hỏi "verifier lệch có thật sự là
   nguyên nhân, hay do chính cơ chế lặp vòng". Bỏ A hoặc C thì bài quay lại
   đúng tình trạng "trông ảo, kết luận sai người" đã phát hiện hôm nay.
5. B (control patch-verifier) có thể lùi sau A/C nếu GPU thật sự cạn, nhưng
   không nên bỏ hẳn — nếu bỏ, phải ghi rõ trong Limitations là chưa có
   control kiểm soát biến thật, chỉ có bằng chứng cô lập (A vs C).
