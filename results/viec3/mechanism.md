# Giai đoạn 5 — tốc độ fit + đa dạng trước lọc, theo model

Đọc từ `generations.jsonl` (đa dạng trước lọc) và `train_logs/round_*.json` (loss cuối mỗi vòng, chỉ có nếu chạy `--mode hf`). Không cần GPU để chạy file này.

## 0.5B (`results/viec3/qwen05b-n500`)

**Đa dạng output trước khi lọc qua verifier.** Text thô gần như luôn ~1.0 (sampling ở temperature>0 hiếm khi lặp y hệt từng chữ) — cột đáng đọc là đáp án đã trích (`extract_final`+chuẩn hoá), vì đó mới bắt được hội tụ thật (nhiều cách viết khác nhau nhưng cùng ra một đáp án):

| Vòng | n đề | unique text/k | unique đáp án/k | % đề cả k lần ra CÙNG 1 đáp án |
|---|---|---|---|---|
| 0 | 1000 | 0.999 | 0.600 | 10.5% |
| 1 | 1000 | 0.999 | 0.601 | 10.8% |
| 2 | 1000 | 1.000 | 0.608 | 9.2% |
| 3 | 1000 | 0.998 | 0.620 | 9.1% |
| 4 | 1000 | 0.999 | 0.649 | 7.3% |

_Không thấy `results/viec3/qwen05b-n500/train_logs/round_*.json` — bỏ qua phần train loss (chỉ `--mode hf` mới ghi log này)._

## 1.5B (`results/viec3/qwen15b-n500`)

**Đa dạng output trước khi lọc qua verifier.** Text thô gần như luôn ~1.0 (sampling ở temperature>0 hiếm khi lặp y hệt từng chữ) — cột đáng đọc là đáp án đã trích (`extract_final`+chuẩn hoá), vì đó mới bắt được hội tụ thật (nhiều cách viết khác nhau nhưng cùng ra một đáp án):

| Vòng | n đề | unique text/k | unique đáp án/k | % đề cả k lần ra CÙNG 1 đáp án |
|---|---|---|---|---|
| 0 | 1000 | 1.000 | 0.443 | 24.8% |
| 1 | 1000 | 0.999 | 0.482 | 21.4% |
| 2 | 1000 | 0.999 | 0.543 | 14.5% |
| 3 | 1000 | 1.000 | 0.634 | 6.6% |
| 4 | 1000 | 1.000 | 0.712 | 1.7% |

_Không thấy `results/viec3/qwen15b-n500/train_logs/round_*.json` — bỏ qua phần train loss (chỉ `--mode hf` mới ghi log này)._
