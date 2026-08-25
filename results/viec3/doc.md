# Việc 3 — đọc số (Mac toy, không phải paper)

Câu đề: sau vòng generate → verify → select → train với `math-verify` (không sửa cô), SLM giỏi toán hơn hay chỉ viết kiểu cô ưa?

**Đúng** luôn = cô chịu. Select lúc dạy = preset `reward`. Exam ghi cả `reward` và `default`.

## Đã chạy trên máy này (2026-08-16)

| Lần | File | Máy | n | k | vòng | Ý nghĩa |
|-----|------|-----|---|---|------|---------|
| Dry | `table.md` (thư mục này) | không gọi Qwen | 100 GSM8K | 4 | 2 | Chứng minh chọn bài + pass@* + đếm chữ. Train no-op. |
| mlx | `mlx-toy/` | Qwen 2.5 0.5B 4bit, LoRA SFT vài bước | 8 GSM8K | 4 | 2 | Thử code trên Mac. **Không** lấy số này viết paper. |

Dry: mỗi đề 4 chữ có sẵn (hộp / câu / `\dfrac` / `18.0`). Cô GSM8K chịu hộp+câu+`18.0`, **gạch `\dfrac`**. Giữ 300/400. pass@1 = 100% vì lần đầu luôn `\boxed{gold}` — đó là kịch bản ống, không phải học sinh giỏi.

mlx: học sinh thật, max 48 token, 8 đề. pass@1 0% cả hai vòng; pass@4 12.5% đứng; gần như không `\boxed` (cắt token). Số nhỏ, nhiễu. Paper = Kaggle T4, xem `experiments/viec3/KAGGLE.md`.

## Cách đọc (cùng TOI-HIEU)

- pass@1 tăng + pass@k đứng/giảm + chữ tụ một kiểu → manh mối mạnh: học chữ cô.
- Cả hai pass tăng, chữ còn nhiều kiểu → chưa kết luận.
- A/B/C: A thêm đề theo cô, B cùng đề lần đầu hay đúng hơn, C mất đề.

Không sửa máy chấm.
