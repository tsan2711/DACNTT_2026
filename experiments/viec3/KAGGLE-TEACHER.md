# Positive gate "teacher" trên Kaggle (B1 → B2) — hướng dẫn từng bước cho Bi

Mục tiêu: SFT 1.5B trên **lời giải đầy đủ của teacher** (Qwen2.5-7B-Instruct), lọc đúng bằng hai grader, 298 mẫu
(cùng dose với loop), recipe vòng cuối giữ nguyên (completion-only, all-linear LoRA, cap 1024, lr 1e-4, 1 vòng,
exam 500 câu). So với gate cũ 49,2 → 17,0. Luật Kaggle: **1 ô GPU mỗi container, không smoke cell**; phiên treo
> 2 giờ không nhích → Stop session, chạy lại.

## B1 — sinh lời giải teacher (≈ 1–3 giờ GPU)

Notebook đã dựng sẵn: `experiments/viec3/kaggle_nb/b1_teacher_gen/` (nhúng code mới dưới dạng tar base64; ô 0 = cài + clone +
overlay + heartbeat, ô 1 = `teacher_gen.py` bọc bởi kill-khi-GPU-0%, tự chạy lại tối đa 4 lần, resumable).

1. Kaggle → New Notebook → File → **Import notebook** → chọn `notebook3132693bf1.ipynb` ở thư mục trên.
   (Hoặc `kaggle kernels push -p experiments/viec3/kaggle_nb/b1_teacher_gen`, rồi vào UI đổi accelerator.)
2. Settings: **Accelerator = GPU T4 x2**, **Internet = On**, Persistence = None.
3. **Save & Run All** (Save Version → "Save & Run All (Commit)").
4. Theo dõi: log `/kaggle/working/run_teacher-gen-7b.log` (mỗi batch in `N/300 problems`); `heartbeat.log` cho GPU.
   Nếu > 2 giờ không thêm dòng `N/300` → Stop, chạy lại (resumable: nó bỏ qua bài đã sinh).
5. Xong: tải `results/viec3/teacher-gen-7b/` (4 file: `generations.jsonl`, `teacher_solutions.jsonl`, `summary.json`)
   về `results/viec3/teacher-gen-7b/` trong repo
   (`kaggle kernels output <id> -p results/viec3/teacher-gen-7b --file-pattern 'teacher.*|summary\.json|generations\.jsonl'`).
6. **Dự phòng 3B** (nếu 7B OOM / quá chậm): dựng lại với `--model Qwen/Qwen2.5-3B-Instruct --name teacher-gen-3b`, 1 GPU T4 đủ.
7. Đọc `summary.json`: `problems_with_a_kept_solution` phải ≥ ~298; nếu thấp hơn, dose thấp hơn 298 → ghi vào bài.

## B2 — gate G2 seed 1 (≈ 2–3 giờ GPU, 1 GPU T4)

1. Dựng notebook (cần file teacher thật):
   `python tools/build_teacher_notebooks.py b2 --meta experiments/viec3/kaggle_nb/b1_teacher_gen/kernel-metadata.json --out experiments/viec3/kaggle_nb/b2_gate_teacher --teacher results/viec3/teacher-gen-7b/teacher_solutions.jsonl --seed 1`
2. Import như B1; Accelerator = **GPU T4 x1** (hoặc x2 cũng được — `run.py` ép 1 GPU), Internet On. Save & Run All.
3. Theo dõi `run_gate-teacher-s1.log`. Vòng 0 (sinh exam 500 + pool 300, k=2) ~1 giờ; train ~10 phút; vòng 1 ~1 giờ.
4. Xong: tải `results/viec3/gate-teacher-s1/` về cùng tên; ô cuối đã in `gate_anatomy` (boxed, acc|boxed, độ dài trung vị).
   Gửi lại cho Claude: nó sẽ chấm lại bằng `regrade_all.py` và cập nhật Mục 4.6.

Chỉ chạy B3 (seed 2) nếu B2 cho tín hiệu rõ; nếu vẫn sụp → dừng, ghi "ngay cả teacher cũng không qua gate".
