# Việc 3 trên Kaggle (GPU T4) — số paper

Mac chỉ thử code. Số liệu bài báo lấy ở đây. Không sửa `math-verify`.

Cùng thiết kế với Mac: mỗi vòng generate k lần/đề → máy chấm giữ bài đúng →
**SFT** (không phải GRPO) dạy lại model trên đúng những bài đó → lặp. Chỉ đổi
`mlx-lm` (Mac) sang `transformers` + `peft` + TRL `SFTTrainer` (Kaggle GPU).

## Máy

- GPU: T4 16GB (Kaggle)
- Model: `Qwen/Qwen2.5-0.5B-Instruct` rồi `Qwen/Qwen2.5-1.5B-Instruct`
- Train: LoRA + TRL `SFTTrainer` (fresh adapter từ base mỗi vòng, chỉ train trên bài vòng đó được giữ — giống hệt Mac)
- Generate: `transformers` (`model.generate`, `num_return_sequences=k`)
- Chấm: cùng `math-verify==0.9.0` + antlr 4.13.2; **select = reward**; exam ghi cả `default` và `reward`

## Ô 1 — cài

```python
%pip install -q "math-verify[antlr4_13_2]==0.9.0" torch transformers accelerate peft trl datasets
```

Clone repo (hoặc Upload) rồi:

```python
import sys
from pathlib import Path
root = Path("/kaggle/working/DACNTT_2026")
sys.path.insert(0, str(root / "src"))
sys.path.insert(0, str(root))
```

## Ô 2 — chạy cả vòng (một lệnh, giống hệt lệnh Mac)

```bash
python -m experiments.viec3.run \
  --mode hf \
  --model Qwen/Qwen2.5-0.5B-Instruct \
  --dataset both \
  --n 500 \
  --rounds 5 \
  --k 8 \
  --max-tokens 512 \
  --select-preset reward \
  --exam-presets reward,default \
  --out /kaggle/working/results/viec3/qwen05b
```

Đề + gold lấy tự động qua `dacntt.gold.load.load_gold` (GSM8K + MATH-500 test split — Mac toy dùng test để chứng minh ống, đây vẫn là test vì repo chưa tách train/test riêng; nếu cần tách train/test cho paper, làm ở bước load_gold trước khi chạy, không sửa trong lúc chạy).

Đổi model sang 1.5B: thêm `--model Qwen/Qwen2.5-1.5B-Instruct --out .../qwen15b`; giảm `--hf-batch-size` nếu OOM.

`train.py:HfLoraSftTrain` và `generate.py:HfGenerate` là code thật (không phải notebook cell dán tay) — nếu lỗi (version TRL/transformers lệch), sửa trực tiếp trong `src/dacntt/gvt/train.py` / `generate.py`, không vá riêng trong notebook.

## Ô 3 — đọc số

Mở `table.md` trong `--out`. Câu đề:

- pass@1 tăng, pass@k đứng/giảm, chữ tụ (`boxed` / `dfrac` / thập phân) → học chữ cô.
- Cả pass@1 lẫn pass@k tăng, chữ còn nhiều kiểu → chưa kết luận chỉ học chữ.
- Bảng A/B/C: A = thêm đề theo cô, C = mất đề, B = cùng đề lần đầu hay đúng hơn.

Không sửa máy chấm nếu `\dfrac` vẫn gạch. Đó là tín hiệu đề, không phải bug.

Ghi `manifest.json`: model, k, select=reward, exam presets, lora_r/lora_alpha/hf_epochs, `paper_quality: true` chỉ khi đã chạy đủ GSM8K+MATH, 0.5B rồi 1.5B.

## Thời gian thô (T4, ước lượng — chưa đo thật)

| Cấu hình | Thô |
|----------|-----|
| 0.5B, 500 đề, k=8, 5 vòng, LoRA SFT | vài giờ / bộ |
| 1.5B, cùng vậy | dài hơn; giảm `--hf-batch-size` nếu OOM |

Không chạy full trên Mac (không có CUDA).
