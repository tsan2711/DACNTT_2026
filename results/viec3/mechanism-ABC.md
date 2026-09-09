# Giai đoạn 5 — tốc độ fit + đa dạng trước lọc, theo model

Đọc từ `generations.jsonl` (đa dạng trước lọc) và `train_logs/round_*.json` (loss cuối mỗi vòng, chỉ có nếu chạy `--mode hf`). Không cần GPU để chạy file này.

## runA_seed0 (`results/viec3/qwen15b-math500-a`)

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

## runA_seed1 (`results/viec3/qwen15b-math500-a-seed1`)

**Đa dạng output trước khi lọc qua verifier.** Text thô gần như luôn ~1.0 (sampling ở temperature>0 hiếm khi lặp y hệt từng chữ) — cột đáng đọc là đáp án đã trích (`extract_final`+chuẩn hoá), vì đó mới bắt được hội tụ thật (nhiều cách viết khác nhau nhưng cùng ra một đáp án):

| Vòng | n đề | unique text/k | unique đáp án/k | % đề cả k lần ra CÙNG 1 đáp án |
|---|---|---|---|---|
| 0 | 500 | 1.000 | 0.528 | 16.0% |
| 1 | 500 | 1.000 | 0.539 | 15.2% |
| 2 | 500 | 1.000 | 0.548 | 13.2% |
| 3 | 500 | 0.999 | 0.543 | 13.8% |
| 4 | 500 | 1.000 | 0.549 | 12.6% |

**Train loss cuối mỗi vòng** (SFTTrainer, trên đúng tập được giữ vòng đó):

| Vòng | Loss cuối | Số bước log |
|---|---|---|
| 0 | 0.4037 | 41 |
| 1 | 0.3230 | 40 |
| 2 | 0.4305 | 40 |
| 3 | 0.3573 | 41 |
| 4 | 0.4277 | 40 |

## runB_seed0 (`results/viec3/qwen15b-math500-b`)

**Đa dạng output trước khi lọc qua verifier.** Text thô gần như luôn ~1.0 (sampling ở temperature>0 hiếm khi lặp y hệt từng chữ) — cột đáng đọc là đáp án đã trích (`extract_final`+chuẩn hoá), vì đó mới bắt được hội tụ thật (nhiều cách viết khác nhau nhưng cùng ra một đáp án):

| Vòng | n đề | unique text/k | unique đáp án/k | % đề cả k lần ra CÙNG 1 đáp án |
|---|---|---|---|---|
| 0 | 500 | 1.000 | 0.542 | 14.6% |
| 1 | 500 | 1.000 | 0.546 | 13.8% |
| 2 | 500 | 0.999 | 0.545 | 14.2% |
| 3 | 500 | 1.000 | 0.547 | 12.2% |
| 4 | 500 | 0.999 | 0.555 | 12.2% |

**Train loss cuối mỗi vòng** (SFTTrainer, trên đúng tập được giữ vòng đó):

| Vòng | Loss cuối | Số bước log |
|---|---|---|
| 0 | 0.3921 | 43 |
| 1 | 0.3976 | 43 |
| 2 | 0.3827 | 43 |
| 3 | 0.3723 | 42 |
| 4 | 0.4417 | 42 |

## runC_seed0 (`results/viec3/qwen15b-gsm8k-c`)

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
