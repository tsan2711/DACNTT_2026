# Bản thảo LaTeX (mẫu Springer LNCS)

`paper.tex` — bài báo đầy đủ, tiếng Anh, dựng trên mẫu LNCS
(`llncs.cls` v2.21, style trích dẫn `splncs04`).

## Biên dịch

Máy này **chưa cài TeX**. Hai cách:

1. **Overleaf** (nhanh nhất): tạo project mới → upload cả thư mục `latex/`
   (gồm `paper.tex`, `llncs.cls`, `splncs04.bst`, 2 file `.png`) → chọn
   compiler **pdfLaTeX** → Recompile.
2. **Cài MacTeX** rồi: `pdflatex paper.tex` (chạy 2 lần cho mục lục/tham chiếu).

Bibliography đã nhúng thẳng bằng `thebibliography`, không cần chạy BibTeX.

## Cần verify trước khi nộp

- **Tên tác giả + đơn vị + email** ở đầu `paper.tex` (đang để placeholder).
- **Mọi con số** trong Section 4 — đối chiếu với
  `results/viec3/qwen05b-n500/table.md` và `qwen15b-n500/table.md`.
- Câu "we did not observe the verifier accepting an incorrect final answer"
  (Sec 3.2 + 3.3): đây là suy luận cấu trúc + quan sát từ Việc 2, **không
  phải** một phép đo false-positive riêng. Nếu thầy hỏi, cần nói rõ.
- 14 tài liệu tham khảo: arXiv ID lấy từ `papers/KHAO-SAT.md` (đã tra web).
  Danh sách tác giả đầy đủ của vài bài mới (2606.*, 2605.*) nên xem lại
  trên arXiv một lần nữa.
- Abstract đang ~210 từ (mẫu yêu cầu 150–250) — đạt.

## Nội dung lấy từ đâu

- Khung + lập luận: `papers/DRAFT.md`
- Số liệu: `results/viec1/`, `results/viec2/`, `results/viec3/`
- Đối chiếu công trình liên quan: `papers/KHAO-SAT.md` (32 bài)
