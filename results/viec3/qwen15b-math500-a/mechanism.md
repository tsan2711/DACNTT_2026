# Giai đoạn 5 — tốc độ fit + đa dạng trước lọc, theo model

Đọc từ `generations.jsonl` (đa dạng trước lọc) và `train_logs/round_*.json` (loss cuối mỗi vòng, chỉ có nếu chạy `--mode hf`). Không cần GPU để chạy file này.

## runA (`results/viec3/qwen15b-math500-a`)

**Đa dạng output trước khi lọc qua verifier.** Text thô gần như luôn ~1.0 (sampling ở temperature>0 hiếm khi lặp y hệt từng chữ) — cột đáng đọc là đáp án đã trích (`extract_final`+chuẩn hoá), vì đó mới bắt được hội tụ thật (nhiều cách viết khác nhau nhưng cùng ra một đáp án):

| Vòng | n đề | unique text/k | unique đáp án/k | % đề cả k lần ra CÙNG 1 đáp án |
|---|---|---|---|---|
| 0 | 500 | 1.000 | 0.542 | 14.6% |
| 1 | 500 | 1.000 | 0.545 | 13.4% |
| 2 | 500 | 0.999 | 0.545 | 13.2% |
| 3 | 500 | 1.000 | 0.546 | 12.2% |
| 4 | 500 | 0.999 | 0.554 | 12.0% |

**Train loss cuối mỗi vòng** (SFTTrainer, trên đúng tập được giữ vòng đó):

| Vòng | Loss cuối | Số bước log |
|---|---|---|
| 0 | 0.3755 | 43 |
| 1 | 0.4102 | 43 |
| 2 | 0.3891 | 43 |
| 3 | 0.4081 | 42 |
| 4 | 0.4257 | 42 |
