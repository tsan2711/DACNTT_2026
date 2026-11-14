# Kế hoạch nước rút — hạn nộp 23:00 ngày 15/11/2026

Trạng thái: bắt đầu 14/11 sáng. **Đóng băng bản nộp 18:00 ngày 15/11** (còn 5 giờ đệm).
Điều kiện đã chốt (Bi, 14/11): Kaggle còn 30/30 giờ; **giữ nguyên tiêu đề** (đổi quá rủi ro); hệ thống nộp **có nhận file thứ hai** (supplementary).

Quy ước: `[ ]` chưa làm, `[x]` xong. Làm xong mục nào thì tick ở đây **và** ghi vào memory `final-sprint-2026-11-15`.

Ràng buộc cứng:
- Bài chính **≤ 15 trang**, không ref undefined, không Overfull.
- Mọi số liệu / tên bài / arXiv ID phải tra thật (WebFetch/WebSearch hoặc tính từ file kết quả), không lấy từ trí nhớ (CLAUDE.md của repo).
- Kaggle: **một GPU cell mỗi container**, bọc `supervise.py` + `heartbeat.py` (xem memory `kaggle-freeze-and-quota`), không chạy smoke cell trước.
- Không commit / push / dời tag khi chưa có lệnh của Bi.

---

## Nhánh A — CPU (làm ngay)

- [ ] **A1. Chấm lại mọi run cũ từ generation đã lưu, một bộ số duy nhất** (phản biện M3, B2.1, B1.2)
  - Verifier V′ (gold bọc `\boxed{}`) + grader khớp chuỗi (`indep_grade.py`); cố định timeout `math-verify`.
  - Đầu ra: một CSV tổng; cập nhật Bảng 1–3 và Mục 4.3 (bỏ cột "run-log"), đồng bộ phụ lục.
  - Rủi ro: số đổi nhẹ → kiểm lại mọi câu trích số trong bài.
- [ ] **A2. Phân tích `gate_anatomy.py` cho run cũ** (boxed, accuracy theo boxed, độ dài) — nếu A1 xong thì làm luôn; ghi một dòng vào bài.
- [ ] **A3. So với Xu et al. [15] cụ thể** (Phantom Gains, arXiv:2608.20290): đọc bài thật, thay câu "We differ in scale and in the verifier" bằng 2–3 điểm khác biệt đã kiểm chứng.
- [ ] **A4. Trích PRM800K / Lightman et al. 2023 (2305.20050)**: xác nhận tiêu đề + ID + ngày; thêm `\bibitem`; dùng làm grader thứ hai nếu chạy được trên CPU.
- [ ] **A5. Tiêu đề: GIỮ NGUYÊN.** (đã chốt, không làm gì)
- [ ] **A6. Trình bày**: abstract ~269 → ~200 từ; tách đoạn dài ở Mục 3.4; sửa chỗ ngắt trang trong danh sách Contributions. Giữ 15 trang (trang 15 hiện đầy tới 659 pt, chừa dư địa bằng cách cắt chữ, không bằng chữ nhỏ).
- [ ] **A7. Supplementary**: nộp như file thứ hai (đã có `baocao-phu-luc.pdf` trong zip). Trong bài ghi rõ "Supplementary (file riêng)" ở lần nhắc đầu tiên + đường dẫn repo.
- [ ] **A8. Repo gọn**: README ngắn "file nào sinh bảng nào"; tách thư mục nháp (`25-10-2026/`, `paper_long_25p.tex`) khỏi bản phát hành. Làm cuối, sau khi đóng băng nội dung.

## Nhánh B — GPU Kaggle (30 giờ, chỉ dùng cho gate)

Mục tiêu duy nhất: **một positive gate hợp lệ** (huấn luyện trên lời giải có lập luận đầy đủ làm accuracy tăng hoặc không giảm). Đây là điều phản biện nói sẽ làm họ đổi khuyến nghị.

Thiết lập giữ nguyên recipe vòng cuối (completion-only, all-linear LoRA, cap 1024, lr 1e-4, 1 vòng, exam 500 câu MATH-500) để so được với gate cũ (49,2 → 17,0).

- [ ] **B0. Chuẩn bị (CPU, ~1 giờ)**: viết/kiểm notebook theo `experiments/viec3/KAGGLE.md`; thêm chế độ "train-on-teacher" (dữ liệu SFT = lời giải teacher đã kiểm đúng, cắt về **298 mẫu** để cùng dose với loop); kiểm tra bằng 1 mẫu cục bộ nếu được.
- [ ] **B1. Sinh lời giải teacher** (Kaggle session 1, ≤ ~3 giờ GPU): Qwen2.5-7B-Instruct chia 2×T4 (`device_map=auto`; **chỉ dùng cho bước sinh này**, vì driver gate ép 1 GPU). Dự phòng: Qwen2.5-3B-Instruct 1 GPU. 300 câu pool (MATH train), k = 4, cap 1024. Lọc đúng bằng grader sạch (V′ **và** khớp chuỗi, hai grader cùng đúng). Lưu mọi generation + điểm từng mẫu.
- [ ] **B2. Gate G2 (teacher)** seed 1 (session 2, ~2–3 giờ): SFT trên lời giải teacher đã lọc → đo exam 500 câu: pass@1, sample accuracy, tỷ lệ `\boxed`, accuracy theo `\boxed`, độ dài trung vị (`gate_anatomy.py`).
- [ ] **B3. G2 seed 2** (session 3) — nếu B2 cho tín hiệu rõ (tăng hoặc ≥ ngang round 0); nếu B2 vẫn sụp, **dừng**, ghi nhận "ngay cả teacher cũng không qua gate" và chuyển B5.
- [ ] **B4. (Chỉ nếu G2 qua gate) Gate lời giải của chính model** (session 4): SFT trên lời giải đúng của chính Qwen2.5-1.5B (đã có sẵn ở round 0, chọn bằng grader độc lập) — chính là vòng loop nhưng có grader sạch. Hai lần chạy cho so sánh dose-matched.
- [ ] **B5. Cập nhật Mục 4.6 + abstract + Limitations + Conclusion** theo kết quả (qua hay không qua gate). Không đổi tiêu đề. Nếu G2 qua gate: viết "loop giảm trong khi gate-teacher không giảm → null có thông tin hơn cho recipe"; nếu không qua: nêu là ngay cả lời giải đầy đủ cũng không cứu được recipe.

Ngân sách GPU dự kiến: B1 ~3h, B2 ~3h, B3 ~3h, B4 ~6h → ≤ 15 giờ trong 30 giờ. Còn dư 15 giờ cho phiên bị treo (từng có 5 phiên × 12h treo; nếu 1 phiên treo > 2 giờ không tiến triển → kill, chạy lại theo heartbeat).

**Không làm**: loop nhiều vòng k ≥ 4 × 3 seed (quá tốn); base model / họ model khác; continued training (đã ghi ở Limitations).

## Kết hợp openaireview

- [ ] **R7** — cuối nhánh A (chiều 14/11): chạy review trên PDF mới. Tránh script ghi đè workspace (từng lấy nhầm bài arXiv): dùng `full_text.md` đã trích + venv python trong scratchpad; lưu kết quả `review_results/paper-main-v7_review/`. Sửa mọi major + moderate còn lại.
- [ ] **R8** — sau B5 (sáng 15/11): review lần cuối. Chỉ sửa lỗi, không mở rộng.
- [ ] **Chốt (≤ 18:00 15/11)**: build 2 lần → kiểm ≤ 15 trang / undefined / overfull; đóng zip `52300057_NguyenTanSang_52300006_TranDuyAnh.zip`; **giải nén thử và compile lại**; bỏ `kehoach.pdf` (scan chữ ký GVHD) và `baocao - turnitin.pdf` vào cùng cấp `baocao.pdf`; hỏi Bi trước khi commit / push / dời tag `paper-2026-11b` (nhớ cập nhật mục "Code availability" cho khớp commit cuối).

## Lịch

| Thời điểm | Việc |
|---|---|
| 14/11 sáng | A1, A3, A4 (CPU) + B0 |
| 14/11 trưa | Đẩy B1 lên Kaggle ngay khi B0 xong (chạy nền trong lúc làm A) |
| 14/11 chiều | A2, A6, A7 → R7 → sửa theo R7 |
| 14/11 tối | B2 (G2 seed 1) chạy qua đêm |
| 15/11 sáng | B3 / B4 theo kết quả; B5 cập nhật bài; A8 |
| 15/11 trưa | R8 → sửa lỗi nhỏ |
| 15/11 18:00 | Đóng băng, zip, giải nén thử, hỏi Bi push |
| 15/11 18:00–23:00 | Đệm; chỉ sửa sự cố |

## Nếu mọi thứ hỏng
Giữ bản hiện tại (đã sửa N1, [14], PRM800K split, abstract ~269 từ, 15 trang) và nộp zip hiện tại. Mọi bước ở trên đều không phá bản này, vì làm trên `paper_main.tex` có backup `paper_main.15p_20261114.tex` (tạo lúc bắt đầu).
