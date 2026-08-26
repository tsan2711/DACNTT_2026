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
%pip install -q "math-verify[antlr4_13_2]==0.9.0" torch transformers accelerate peft trl datasets "torchao>=0.16.0"
```

`torchao>=0.16.0` bắt buộc — Kaggle cài sẵn bản cũ hơn (0.10.0), không tương
thích với `peft`. Sau lệnh này **restart session** rồi chạy lại ô cài (bản
`torchao` mới chỉ áp dụng sau restart — xác nhận thật trên Kaggle 2026-08-26).

Clone repo (khuyên dùng, dễ cập nhật fix hơn upload zip — cần repo public
hoặc dùng token):

```python
!git clone https://github.com/<tài-khoản>/DACNTT_2026.git /kaggle/working/DACNTT_2026
%cd /kaggle/working/DACNTT_2026
```

```python
import sys
from pathlib import Path
root = Path("/kaggle/working/DACNTT_2026")
sys.path.insert(0, str(root / "src"))
sys.path.insert(0, str(root))
```

Nếu notebook tạo với **"GPU T4 x2"** (2 GPU) thay vì 1 GPU: không cần đổi gì
thêm — `run.py` đã tự ép `CUDA_VISIBLE_DEVICES=0` (chỉ dùng 1 GPU, đúng
thiết kế single-GPU của nhánh `hf`; để lộ cả 2 GPU sẽ làm `transformers.Trainer`
tự bọc `nn.DataParallel` và crash vì input/model lệch device — đã gặp và sửa
thật, xem lịch sử commit `run.py`).

## Ô 2 — chạy thử NHỎ trước (bắt lỗi rẻ, đừng chạy full ngay lần đầu)

```bash
PYTHONPATH=src:. python -m experiments.viec3.run \
  --mode hf --model Qwen/Qwen2.5-0.5B-Instruct --dataset gsm8k \
  --n 20 --rounds 2 --k 4 --max-tokens 256 \
  --select-preset reward --exam-presets reward,default \
  --out /kaggle/working/results/viec3/smoke
```

**Xác nhận đã chạy được (2026-08-26, notebook Kaggle thật, `transformers==5.0.0`,
`trl==1.10.0`, `peft==0.19.1`)** — 3 lỗi gặp phải và đã sửa trong code (không
phải vá tay trong notebook):
1. `SFTConfig.__init__() got an unexpected keyword argument 'max_seq_length'` — TRL 1.10.0 đổi tên thành `max_length`.
2. `ImportError: Found an incompatible version of torchao` — cần nâng `torchao` lên `>=0.16.0` (xem Ô 1).
3. `AttributeError: 'functools.partial' object has no attribute '__func__'` — do tự load model với `device_map="auto"`, khiến `accelerate` bọc `forward` thành `functools.partial`, TRL không đọc được signature. Đã bỏ `device_map="auto"`, dùng `.to("cuda")` trực tiếp (T4 chỉ 1 GPU, không cần `device_map="auto"` vốn dành cho multi-GPU/nhiều máy). Xác nhận qua issue đã đóng `huggingface/trl#6483`.

Nếu bản `transformers`/`trl`/`peft` trên Kaggle đổi tiếp (rất có thể, đây đều
là thư viện cập nhật nhanh), khả năng cao sẽ vướng lỗi mới khác — sửa trực
tiếp trong `src/dacntt/gvt/train.py` / `generate.py`, đừng vá riêng trong
notebook.

## Ô 3 — chạy full lấy số paper (chỉ sau khi Ô 2 chạy sạch)

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

## Ô 4 — đọc số

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
