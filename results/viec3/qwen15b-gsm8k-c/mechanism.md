# Giai đoạn 5 — tốc độ fit + đa dạng trước lọc, theo model

Đọc từ `generations.jsonl` (đa dạng trước lọc) và `train_logs/round_*.json` (loss cuối mỗi vòng, chỉ có nếu chạy `--mode hf`). Không cần GPU để chạy file này.

## runC (`results/viec3/qwen15b-gsm8k-c`)

**Đa dạng output trước khi lọc qua verifier.** Text thô gần như luôn ~1.0 (sampling ở temperature>0 hiếm khi lặp y hệt từng chữ) — cột đáng đọc là đáp án đã trích (`extract_final`+chuẩn hoá), vì đó mới bắt được hội tụ thật (nhiều cách viết khác nhau nhưng cùng ra một đáp án):

| Vòng | n đề | unique text/k | unique đáp án/k | % đề cả k lần ra CÙNG 1 đáp án |
|---|---|---|---|---|
| 0 | 500 | 1.000 | 0.359 | 33.6% |
| 1 | 500 | 1.000 | 0.364 | 32.4% |
| 2 | 500 | 1.000 | 0.413 | 25.2% |
| 3 | 500 | 1.000 | 0.444 | 18.8% |
| 4 | 500 | 1.000 | 0.500 | 16.0% |

**Train loss cuối mỗi vòng** (SFTTrainer, trên đúng tập được giữ vòng đó):

| Vòng | Loss cuối | Số bước log |
|---|---|---|
| 0 | 0.4313 | 95 |
| 1 | 0.4986 | 93 |
| 2 | 0.4206 | 88 |
| 3 | 0.4672 | 84 |
| 4 | 0.5574 | 75 |
