# Giai đoạn 0.2 — pass@1/pass@k tách theo bộ đề (không phải số gộp)

Tái tính từ `generations.jsonl` (không gọi lại model, chỉ chạy lại `math-verify` trên đúng lời giải đã sinh). Số gộp gốc nằm ở `table.md` cùng thư mục.

**Đọc thế nào:** nếu GSM8K (verifier gần sạch, FN≈0%) sụp ít hơn hẳn MATH-500 (verifier lệch, FN≈7.8%) qua cùng các vòng, đó là bằng chứng gợi ý (không phải control có kiểm soát biến — hai bộ đề còn khác nhau về độ khó) cho câu hỏi "có phải verifier lệch gây ra sụp". Xem `papers/KE-HOACH-MO-RONG.md` Giai đoạn 0.2 để biết giới hạn của cách đọc này.

| Bộ đề | Preset | Vòng | pass@1 | pass@8 | n đề |
|---|---|---|---|---|---|
| gsm8k | default | 0 | 44.4% | 77.2% | 500 |
| gsm8k | reward | 0 | 44.4% | 77.2% | 500 |
| math500 | default | 0 | 17.8% | 43.8% | 500 |
| math500 | reward | 0 | 17.8% | 43.8% | 500 |
| gsm8k | default | 1 | 43.2% | 74.8% | 500 |
| gsm8k | reward | 1 | 43.2% | 74.8% | 500 |
| math500 | default | 1 | 20.6% | 43.0% | 500 |
| math500 | reward | 1 | 20.6% | 43.0% | 500 |
| gsm8k | default | 2 | 41.6% | 71.4% | 500 |
| gsm8k | reward | 2 | 41.6% | 71.4% | 500 |
| math500 | default | 2 | 18.2% | 40.8% | 500 |
| math500 | reward | 2 | 18.2% | 40.8% | 500 |
| gsm8k | default | 3 | 41.0% | 72.0% | 500 |
| gsm8k | reward | 3 | 41.0% | 72.0% | 500 |
| math500 | default | 3 | 16.8% | 39.0% | 500 |
| math500 | reward | 3 | 16.8% | 39.0% | 500 |
| gsm8k | default | 4 | 36.0% | 69.0% | 500 |
| gsm8k | reward | 4 | 36.0% | 69.0% | 500 |
| math500 | default | 4 | 18.8% | 40.8% | 500 |
| math500 | reward | 4 | 18.8% | 40.8% | 500 |

## Tỉ lệ mỗi bộ đề trong tập được giữ để train mỗi vòng (preset `reward`)

Một adapter LoRA chung train trên tập gộp cả hai bộ mỗi vòng — số dưới đây cho biết tập đó lệch về bộ nào qua từng vòng, có thể giải thích vì sao pass@* của một bộ bị ảnh hưởng bởi chuyện xảy ra ở bộ kia (nhiễu chéo giữa hai domain), thay vì mỗi bộ tự sụp độc lập vì verifier riêng của nó.

| Vòng | Số lời giải giữ (GSM8K) | Số lời giải giữ (MATH-500) | % GSM8K trong tập train |
|---|---|---|---|
| 0 | 1756 | 777 | 69.3% |
| 1 | 1678 | 776 | 68.4% |
| 2 | 1614 | 725 | 69.0% |
| 3 | 1588 | 679 | 70.0% |
| 4 | 1459 | 664 | 68.7% |
