# Báo cáo 25/10/2026 — Nguyễn Tấn Sang (52300057), Trần Duy Anh (52300006)

| File | Dùng để |
|---|---|
| `BaoCaoNhanh_25-10_52300057_52300006.pptx` | **Deck trình bày chính**: 10 slide, mỗi slide một ý, khoảng 10 phút. Có ghi chú người nói. |
| `BaoCaoDayDu_25-10_52300057_52300006.pptx` | Deck đầy đủ 15 slide, mở khi thầy hỏi sâu (thiết kế, 4 thước đo, bảng số). |
| `paper_revised.pdf` | Paper: 12 trang thân bài + tài liệu tham khảo, phụ lục A–K giữ nguyên văn mọi phân tích chi tiết. |
| `demo_verifier.py` | Demo máy chấm loại nhầm lời giải đúng (chỉ cần CPU, ~10 giây). |
| `demo_output.txt` | Kết quả demo đã chạy sẵn, mở nếu máy lỗi khi demo. |

## Chạy demo (ở thư mục gốc repo DACNTT_2026)

```bash
.venv/bin/python 25-10-2026/demo_verifier.py --live 200
```

Nhấn Enter để qua từng phần; thêm `--no-pause` để chạy một mạch. Phần 4 (`--live`) chấm lại mẫu ngẫu nhiên
nên tỉ lệ dao động theo cỡ mẫu (200 mẫu có thể ra ~13–20%); con số để trích dẫn là bảng phần 3 (15,5–18,4%).

Tạo lại deck: `.venv/bin/python tools/make_quick_pptx.py` (ghi đè file deck nhanh trong thư mục này).
