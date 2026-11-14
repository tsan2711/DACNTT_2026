# File nào sinh bảng nào (bản nộp 15/11/2026)

Mọi số trong bài chính và phụ lục lấy từ **một lần chấm lại** bằng V′ (math-verify 0.9.0 + vá phân số/gold-box, timeout 10 s, thử lại 60 s) và grader khớp chuỗi.

| Bước | Lệnh | Đầu ra |
|---|---|---|
| Chấm lại 28 run từ `generations.jsonl` + bootstrap | `python -m experiments.viec3.regrade_all --B 10000` (đặt `TOKENIZER_JSON` = tokenizer Qwen2.5 để có cap-hit) | `results/viec3/regrade/{summary.csv,ci.json,ci.md,flags/}` |
| Hàng cho Bảng lrseries, ci, controls, final | `python -m experiments.viec3.regrade_tables` | `results/viec3/regrade/tables.tex` |
| Hàng cho Bảng anatomy, decomp (phụ lục) | `python -m experiments.viec3.regrade_anatomy` | in ra màn hình |
| Giải phẫu gate (boxed, acc theo boxed, độ dài) | `experiments/viec3/review_cpu/gate_anatomy.py` | in ra màn hình |
| Lời giải teacher cho gate G2 | `experiments/viec3/teacher_gen.py` (Kaggle, xem `experiments/viec3/KAGGLE-TEACHER.md`) | `teacher_solutions.jsonl` |

Bài: `papers/latex/paper_main.tex` (15 trang), phụ lục: `papers/latex/supplementary.tex`. Bản nháp cũ (`_archive/nhap/`: `25-10-2026/`, `paper_long_25p.tex`) và zip nộp cũ (`_archive/nop-cu/`) không thuộc bản nộp.
