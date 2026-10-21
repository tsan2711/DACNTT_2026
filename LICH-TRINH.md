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
4. **Seed thứ 2 cho Run C** — ưu tiên cao nhất còn lại. Chưa chạy.
5. **Ablation không lọc** — cùng dataset/model với headline, thêm
   `--no-filter`. Chưa chạy.
6. **Run D (Giai đoạn 7, mới 2026-09-12)** — cùng config headline, thêm
   `--patch-verifier-boxed`: vá bug thứ hai (gold đọc thiếu khi bài dự đoán
   đóng `\boxed{}` mà gold không), chẩn đoán + code + test xong, chỉ còn
   thiếu lượt chạy. Xem `papers/KET-QUA-CO-LAP-AC.md` mục 8 và
   `experiments/viec3/KAGGLE.md`.

**Không bắt buộc, chỉ chạy nếu còn GPU-giờ dư:** model thứ ba, chạy dài hơn
5 vòng, họ model khác (Giai đoạn 5 trong `KE-HOACH-MO-RONG.md`).

> **Chốt 2026-09-13 — đây là vòng chạy cuối cùng.** Câu hỏi gốc của đề tài
> (model có giỏi lên không / verifier lệch có phải nguyên nhân) đã có câu
> trả lời đầy đủ từ A/B/C: **không** và **không**. Ba việc dưới đây (seed 2
> cho GSM8K, ablation `--no-filter`, control `--train-on-gold`) chỉ giải
> thích thêm phần dư nhỏ còn lại (tụt 2,7–3,4 điểm ở MATH-500), **không bắt
> buộc** để bài báo hoàn chỉnh. Chạy xong ba cái này — dù kết quả ra sao,
> kể cả mơ hồ — thì **dừng, viết bài báo với kết quả có sẵn, không mở thêm
> thí nghiệm mới**. Xem lý do đầy đủ ở `papers/KET-QUA-CO-LAP-AC.md`.

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
      rút lại claim shrinking-pool, Limitations 6 mục, Conclusion). **Cập
      nhật 2026-09-18: bảng `tab:isolated` đã có đủ seed 0 + seed 1 cho Run
      A/B, không còn hedging "single seed"** — xác nhận qua compile thật
      (xem C3). Còn thiếu: ablation `--no-filter` (đang chờ chạy, xem mục
      "vòng chạy cuối cùng" phía trên). **Cập nhật 2026-09-30: nghi vấn
      learning rate đã đưa vào bài** — Limitations mục 1 (mới, đặt lên đầu)
      trình bày kết quả thật của `diagnose_lr.py` (1 round LoRA SFT,
      lr=1e-5 loss dao động 0.68–0.84 không giảm, lr=5e-4 tụt sạch xuống
      ~0.24–0.28), footnote ở §3.4 Training trỏ tới mục này, và Future Work
      đặt việc rerun Design I ở lr=5e-4 lên ưu tiên số 1. Nói rõ trong bài:
      Run A-lr-mới **chưa chạy xong** (quota Kaggle cạn, 6 lần treo liên
      tiếp), nên kết luận null hiện tại được ghi là **provisional** chứ
      không khẳng định chắc. Khi Run A-lr-mới có kết quả thật (xem
      `kaggle-freeze-and-quota.md`), nếu đổi kết quả A/B/C thì viết lại
      đoạn này; nếu không đổi, sửa "provisional" thành đã xác nhận. Bản
      nháp cũ `papers/DRAFT.md` đã đánh dấu lỗi thời, không dùng nữa.
      **Cập nhật 2026-10-04: Run A lr=5e-4 đã chạy xong** (3 vòng, k=4,
      seed 1): pass@1 33.3→32.7→23.3, pass@4 50.0→49.3→42.7 — KHÔNG còn
      phẳng như lr=1e-5. Đã viết vào bài: mục Results mới
      `sec:lrcheck` (Bảng `tab:lrcheck`), abstract/intro/discussion/
      conclusion đổi sang "null chỉ đúng ở lr=1e-5", Limitations mục 1 viết
      lại, Future work đặt B/C/seed 2 ở lr mới lên đầu. Dữ liệu:
      `results/viec3/a-math500-lr-fixed/`. Chưa chạy lại B (control vá
      verifier) và C ở lr mới — chưa kết luận được verifier có liên quan.
      **Cập nhật 2026-10-04 (tối): Run B lr=5e-4 cũng xong** (cùng cấu hình
      A + `--patch-verifier`): pass@1 33.3→35.3→28.7, pass@4 50.7→50.0→48.7
      (A: 23.3 / 42.7 ở vòng 2). B giảm ÍT hơn A ~5.4 điểm pass@1 / 6.0
      pass@4, đúng chiều giả thuyết gốc nhưng cỡ ngang nhiễu và chỉ 1 seed;
      B vẫn giảm nên \dfrac không giải thích hết. Bài đã ghi: control
      "null ở 1e-5, chưa kết luận được ở lr mới". Còn thiếu: Run C + seed 2
      của A/B ở lr mới. Dữ liệu: `results/viec3/b-math500-lr-fixed/`.
      **Cập nhật 2026-10-07: seed 2 của A và B ở lr=5e-4 xong** (v55, 4.5h).
      Seed 2 vòng 2: A 27.3/44.7, B 20.0/40.7 (pass@1/pass@4) — B giảm NHIỀU
      hơn A, ngược seed 1 (B hơn A 5.4/6.0). Cả 4 run đều giảm (pass@4 −2.0
      đến −11.3) ⇒ "phẳng" ở 1e-5 là hiện vật của undertrain; còn bản vá
      verifier không có tác dụng nhất quán (dấu lật theo seed) ⇒ control vẫn
      đứng. Bài đã viết lại sec:lrcheck (4 run, 21 trang), abstract,
      conclusion, limitations, future work (no-filter / train-on-gold / C ở
      lr mới / 5 vòng k=8). Dữ liệu: `results/viec3/{a,b}-math500-lr-fixed-seed2/`.
      **Cập nhật 2026-10-08: no-filter + train-on-gold ở lr=5e-4 xong** (v56,
      4.95h, seed 1). Vòng 2 pass@1/pass@4: A 23.3/42.7, no-filter 27.3/40.7,
      train-on-gold 15.3/29.3 (rơi ngay vòng 1: 18.0/33.3; văn phong chuyển
      sang lời giải mẫu: `$` 5%→98%). ⇒ mức giảm là do bước SFT ở lr này,
      không do dữ liệu tự sinh hay verifier; lọc hay không lọc gần như
      không khác. Bài thêm bảng `tab:controls` + đoạn "Two controls", sửa
      abstract/conclusion/limitations/future work (22 trang). Dữ liệu:
      `results/viec3/{nofilter,gold}-math500-lr-fixed/`. Còn thiếu: quét
      lr trung gian, seed thêm cho 2 control, Run C ở lr mới, 5 vòng k=8.
      **Cập nhật 2026-10-08: phân tích cấu tạo mức giảm + đối chiếu tài liệu.**
      Self-training: tỉ lệ đầu ra lan man (>1500 ký tự, không có \boxed) tăng
      ~10%→~40%, độ chính xác trên bài làm xong KHÔNG giảm; train-on-gold:
      lời giải ngắn đi 59%, chính xác giảm 37%→14%. Phát hiện lỗi pipeline:
      max_length huấn luyện 512 = trần sinh 512 ⇒ 24–26% ví dụ bị cắt cụt
      (no-filter 62–68% nhưng không lan man hơn ⇒ chưa chứng minh nhân quả).
      Bài thêm mục "Anatomy of the Decline" + Related Work (Xu 2608.20290,
      Kim 2603.24472, Egashira đọc lại toàn văn) — 24 trang. CHƯA CHẠY:
      Run A với --max-seq-length 1024 + đánh giá lại với trần token lớn hơn
      (chờ quota reset 10/10). **lr=1e-4 (v57) xong:** pass@1 33.3→29.3→34.0,
      pass@4 50.0→50.7→49.3 (loss 0.65→0.28 ⇒ có học nhưng KHÔNG giảm);
      lan man vòng 2: 8.8% (1e-5) / 19.5% (1e-4) / 41.3% (5e-4) ⇒ trôi tăng
      theo lr (dose–response). Bài 25 trang, đã viết lại abstract/conclusion
      ("phẳng" đúng ở 1e-5 và 1e-4, giảm ở 5e-4). Dữ liệu:
      `results/viec3/a-math500-lr1e4/`.
      **Cập nhật 2026-10-11: v58 (msl1024 + đánh giá lại với trần token).**
      Bản lặp lại A seed 1 (msl 512) tái hiện mức giảm (25.3/44.0 ở vòng 2).
      Train với max_length 1024 (không ví dụ nào bị cắt): lan man vẫn 37.2%
      (so 30.0%) ⇒ cắt cụt ví dụ huấn luyện KHÔNG phải nguyên nhân. Đánh giá
      lại adapter vòng 2 với trần 1536 token: độ chính xác mẫu 28.3→34.2%
      (bản lặp) và 27.5→29.5% (msl1024); lan man chỉ giảm 30→23% / 37→33% ⇒
      trần token góp một phần, không giải thích hết. Bài đã thêm Bảng
      `tab:reeval`. Dữ liệu: `results/viec3/a-lr5e4-keep/`, `a-lr5e4-msl1024/`.
      Đợt 3 (v59) đang chạy: đánh giá lại model gốc ở 512/1536 (mốc so
      sánh còn thiếu) + lr 1e-4 seed 2, 3 + lr 2e-4 seed 1.
      **2026-10-11: REFACTOR bài 25 → 16 trang.** Bỏ 2 hình + 2 bảng phụ của
      Design P (pass_at_k, selected_pool, poolmix, prevalence, answer-
      diversity), gộp control+prevalence, gộp 3 mục Discussion đầu, nén
      Related Work/Intro/Limitations (7 mục gọn), Abstract ~240 từ. Giữ đủ:
      Bảng passk, bydataset, isolated(+hình), lrcheck, controls, anatomy,
      reeval. Bản trước refactor: /tmp/refs/paper.tex.pre_refactor (không
      nằm trong git!). Còn chờ v59 để chèn số: base@1536, 1e-4 seed 2/3,
      2e-4 seed 1 (sửa Table lrcheck/anatomy/reeval, Abstract, Conclusion,
      Limitations #2).
      **2026-10-11 (tối): v59 xong (11.4h)** — lr 1e-4 seed 2,3 / 2e-4 seed 1
      + đánh giá lại model gốc. Kết quả: độ chính xác mẫu vòng 2 giảm
      2.0 (1e-4, 3 seed) / 3.5 (2e-4) / 6.5 (5e-4); lan man 20.6 / 25.0 /
      38.8% ⇒ dose–response. Model gốc ở trần 1536 cũng tăng (36.3→43.2%,
      lan man 8.7→2.5%) ⇒ khoảng cách adapter–gốc KHÔNG thu hẹp ⇒ KHÔNG
      phải lỗi trần token (đảo ngược nhận định của v58). Bài cập nhật
      (17 trang), báo cáo viết lại (5 trang; generator ở
      tools/make_report_20261011.js). Zip nộp: ...TranDuyAnh-nop.zip.
      **2026-10-12: v60 xong (8.9h)** — no-filter seed 2, train-on-gold seed 2,
      lr 2e-4 seed 2, Run C (GSM8K) 5e-4. Hai đối chứng TÁI HIỆN ở seed 2
      (gold: pass@1 31.3→10.0; no-filter 31.3→22.7); 2e-4 trung bình −3.7
      điểm chính xác mẫu; Run C GSM8K giảm mạnh (pass@1 70.7→48.7, pass@4
      86.0→76.7, chính xác trên bài làm xong cũng giảm 71.5→64.6). Bài 18
      trang, báo cáo 6 trang, zip làm lại. Quota còn 1.8h (reset 17/10).
- [x] **C3. Compile thử** — **xong 2026-09-18, dùng `tectonic` (cài qua
      brew, không cần MacTeX ~4GB) thay vì Overleaf.** Compile sạch, ra
      `paper.pdf` (18 trang, không lỗi fatal). 4 cảnh báo overfull/underfull
      hbox/vbox — đã xem trực tiếp trang PDF tương ứng, không phải lỗi thấy
      được, bỏ qua an toàn. **2 việc cần làm trước khi nộp thật:**
      (1) trang đầu vẫn ghi `First Author`/`Second Author`/`example.edu`
      (dòng 1 file có comment "pending author verification") — cần tên
      thật + email thật, không tự đoán; (2) 18 trang hơi dài so với chuẩn
      LNCS phổ biến (12–15 trang) — chưa rõ giới hạn trang thật của nơi
      nộp, cần kiểm tra lại yêu cầu cụ thể trước khi tính có phải cắt bớt
      không.
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
