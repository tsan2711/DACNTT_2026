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

### Ô 2b — test siêu nhỏ (~5 phút), cả 2 dataset, để bắt lỗi timeout verify

Ô 2 chỉ dùng GSM8K, không đụng tới MATH — mà log timeout thật
(`Timeout during comparison`, do `math-verify` gặp biểu thức SymPy khó, xem
mục "Tốc độ" bên dưới) chỉ xảy ra khi có MATH trong đề. Dùng lệnh này để bắt
lỗi đó rẻ, không phải chờ hết cả full run mới thấy:

```bash
PYTHONPATH=src:. python -m experiments.viec3.run \
  --mode hf --model Qwen/Qwen2.5-0.5B-Instruct --dataset both \
  --n 5 --rounds 1 --k 2 --max-tokens 128 --verify-timeout 2 \
  --select-preset reward --exam-presets reward,default \
  --out /kaggle/working/results/viec3/tiny
```

Ước tính (đo thật 2026-08-27, xem log `notebook3132693bf1.log`): với
`--dataset gsm8k --n 20 --rounds 2 --k 4 --max-tokens 256` một vòng
generate+verify mất ~264s. Cấu hình Ô 2b nhỏ hơn nhiều — 10 đề (5+5) × k=2 ×
max-tokens 128, 1 vòng — nên nằm gọn trong ~5 phút kể cả thời gian tải model
lần đầu (~1 phút nếu chưa cache). Không dùng để đọc số (n quá nhỏ), chỉ để
xác nhận: (1) code chạy hết pipeline không crash, (2) nếu có
`Timeout during comparison` thì verifier vẫn trả về đúng `reason=timeout`
(tính là sai, không crash, không treo) — xem `MathVerifyAdapter` trong
`src/dacntt/verify/adapter.py`.

`--verify-timeout` (mới thêm, mặc định 5s giống hành vi cũ) giới hạn số giây
`math-verify` được phép tốn cho MỖI lần parse/so sánh trước khi bỏ cuộc.
Hạ xuống 1-2s khi test cho nhanh; giữ mặc định 5s khi chạy lấy số paper (Ô 3)
để không bỏ sót bài đúng chỉ vì so sánh SymPy hơi chậm.

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

## Tốc độ (2026-08-26 — sửa sau khi thấy 1 vòng full > 1 tiếng)

Hai nguyên nhân chậm đã sửa trong code (không phải vá tay notebook):

1. **dtype sai trên T4**: `torch_dtype="auto"` từng nạp model ở `bfloat16`
   (dtype gốc của checkpoint Qwen2.5) — T4 (Turing) không có tensor core
   bf16, phải giả lập bằng fp32, chậm hẳn. Đã đổi sang `torch.float16` khi
   có CUDA, ở cả `HfGenerate` (generate.py) và `HfLoraSftTrain`
   (`bf16=True` → `fp16=True` trong `SFTConfig`, train.py).
2. **Generate không batch qua nhiều đề**: trước đây gọi `model.generate()`
   riêng từng đề (n=500 lần/vòng), GPU không đủ việc để bận. Giờ
   `HfGenerate.generate_batch()` gom nhiều đề vào 1 lần gọi (mặc định
   `--gen-batch-size 8`, chỉnh theo VRAM còn trống); `loop.py` tự dùng
   `generate_batch` nếu generator có (MLX/dry vẫn gọi `generate` từng đề
   như cũ, không đổi).

Tăng `--gen-batch-size` (16, 32...) nếu T4 còn dư VRAM sau khi nạp model —
xem log OOM để biết trần. Nếu OOM ở bước train, giảm `--hf-batch-size`
trước, không phải `--gen-batch-size` (hai batch size độc lập nhau, một cho
generate, một cho SFTTrainer).

## Thời gian thô (T4 — đo thật 2026-08-27, xem `notebook3132693bf1.log`)

| Cấu hình | Thô |
|----------|-----|
| 0.5B, 500+500 đề (both), k=8, max-tokens 512, 1 vòng (fp16 + gen-batch mặc định 8) | **~6.7 tiếng/vòng** — trong đó generate+verify chiếm ~6 tiếng, train (1302 step LoRA) chỉ ~29 phút. Với 5 vòng ước **~33+ tiếng** — **vượt trần 12h/phiên của Kaggle**, không chạy hết trong 1 phiên. |
| 0.5B, 20 đề gsm8k, k=4, max-tokens 256, 1 vòng | ~264s (~4.4 phút) — dùng làm bench nhỏ, xem Ô 2. |
| 1.5B, cùng cấu hình full | chưa đo thật, kỳ vọng chậm hơn 0.5B; giảm `--hf-batch-size` nếu OOM lúc train, giảm `--gen-batch-size` nếu OOM lúc generate. |

**Hệ quả thực tế:** cấu hình full ở Ô 3 (500 đề, 5 vòng) không chạy vừa 1
phiên Kaggle. Trước khi chạy full, hoặc: (a) giảm `--n`/`--k`/`--rounds` để
vừa ~10-12h/phiên, hoặc (b) chia làm nhiều phiên nối tiếp — mỗi vòng đã ghi
kết quả riêng ra `--out` (xem `_save_partial` trong `run.py`), nên phiên sau
có thể tiếp tục đọc dữ liệu vòng trước, không mất trắng nếu phiên bị Kaggle
tự ngắt giữa chừng.

`Timeout during comparison` (log do chính `math-verify` in ra, không phải
lỗi trong code) xuất hiện vài lần trên MATH500 khi SymPy so sánh biểu thức
quá `--verify-timeout` giây (mặc định 5s) — đã được `MathVerifyAdapter` bắt
và trả `reason=timeout` (tính là sai), không làm crash hay treo pipeline.
Chỉ tốn thêm vài chục giây tổng cộng trên cả nghìn lần so sánh, không phải
nguyên nhân chính khiến 1 vòng mất ~6.7 tiếng — thời gian đó chủ yếu do bước
GENERATE (500+500 đề × k=8 lần sinh trên T4).

Không chạy full trên Mac (không có CUDA).

## Ô 5 — Giai đoạn 1–4 (papers/KE-HOACH-MO-RONG.md, chạy A/B/C)

**Cập nhật 2026-09-05 — bỏ thiết kế `--dataset both`, chuyển sang cô lập
từng bộ đề.** Lý do: phân tích lại 2 lần chạy gốc (tách pass@1/pass@k theo
GSM8K/MATH-500 từ `generations.jsonl` tìm lại được trên Kaggle) cho thấy
`--dataset both` khiến một adapter chung train mỗi vòng trên tập gộp cả hai
bộ — nhiễm chéo giữa hai domain, không tách được "tại verifier lệch" khỏi
"tại lây từ bộ kia". Xem chi tiết ở đầu `papers/KE-HOACH-MO-RONG.md`.

Cờ dùng ở đây (Track A, không đổi hành vi mặc định — không truyền gì thì
chạy y hệt như trước):

- `--dataset math500` hoặc `--dataset gsm8k`: chạy **một** bộ đề, không gộp
  — cô lập hoàn toàn, tránh nhiễm chéo. (Khác `--dataset both` dùng ở 2 lần
  chạy gốc.)
- `--holdout-frac 0.3`: tách 30% đề riêng cho `exam`, không lẫn vào `select`
  — dùng cho cả A/B/C, cũng là cách vá luôn Giai đoạn 2 (tách train/test).
- `--patch-verifier`: vá `\dfrac`/`\tfrac` → `\frac` trước khi `math-verify`
  chấm — chỉ dùng cho chạy B.
- `--seed N`: cố định `random`/`torch` — dùng cùng seed cho A/B/C (so sánh
  công bằng), đổi seed khi lặp lại ở Giai đoạn 2.
- `--no-filter`: bỏ hẳn bước lọc verifier — dùng cho ablation Giai đoạn 3.

```bash
# A — MATH-500 cô lập, verifier gốc (headline mới + mốc so sánh cho B)
python -m experiments.viec3.run --mode hf --model Qwen/Qwen2.5-1.5B-Instruct \
  --dataset math500 --n 500 --rounds 5 --k 8 --max-tokens 512 \
  --seed 1 --holdout-frac 0.3 \
  --out /kaggle/working/results/viec3/a-math500-original

# B — MATH-500 cô lập, verifier vá (control: đúng 1 biến khác A)
python -m experiments.viec3.run --mode hf --model Qwen/Qwen2.5-1.5B-Instruct \
  --dataset math500 --n 500 --rounds 5 --k 8 --max-tokens 512 \
  --seed 1 --holdout-frac 0.3 --patch-verifier \
  --out /kaggle/working/results/viec3/b-math500-patched

# C — GSM8K cô lập, verifier gốc (verifier gần sạch tự nhiên ở bộ này —
# không cần --patch-verifier, \dfrac/\tfrac gần như không xuất hiện)
python -m experiments.viec3.run --mode hf --model Qwen/Qwen2.5-1.5B-Instruct \
  --dataset gsm8k --n 500 --rounds 5 --k 8 --max-tokens 512 \
  --seed 1 --holdout-frac 0.3 \
  --out /kaggle/working/results/viec3/c-gsm8k-isolated

# Giai đoạn 2 — seed thứ 2/3, lặp lại đúng cấu hình được chọn làm headline
# (nhiều khả năng là A hoặc B), chỉ đổi --seed
python -m experiments.viec3.run --mode hf --model Qwen/Qwen2.5-1.5B-Instruct \
  --dataset math500 --n 500 --rounds 5 --k 8 --max-tokens 512 \
  --seed 2 --holdout-frac 0.3 \
  --out /kaggle/working/results/viec3/seed2-math500

# Giai đoạn 3 — ablation không lọc, cùng dataset/model với headline
python -m experiments.viec3.run --mode hf --model Qwen/Qwen2.5-1.5B-Instruct \
  --dataset math500 --n 500 --rounds 5 --k 8 --max-tokens 512 \
  --seed 1 --holdout-frac 0.3 --no-filter \
  --out /kaggle/working/results/viec3/no-filter-math500
```

**Sau MỖI lần chạy (dù full hay bị Kaggle ngắt giữa chừng), tải về máy/Drive
trước khi đóng notebook:**

- `--out/generations.jsonl` — bắt buộc, cần cho `analyze_by_dataset.py` (dù
  giờ mỗi lần chỉ có 1 dataset, vẫn cần để soát lại số) và
  `analyze_mechanism.py` (Giai đoạn 4).
- `--out/train_logs/round_*.json` — train-loss cho Giai đoạn 4, chỉ
  `HfLoraSftTrain` mới ghi.
- `--out/table.md` + `manifest.json` — như cũ.

Hai lần chạy gốc (`qwen05b-n500`, `qwen15b-n500`, dùng `--dataset both`) đã
tìm lại được `generations.jsonl` từ Kaggle output (2026-09-05) — giữ nguyên
làm số tham chiếu/pooled, không chạy lại. Số chính của bài từ nay lấy từ
A/B/C (cô lập), không phải 2 lần chạy gộp cũ.

### Ngân sách thời gian thật (quan trọng — đọc trước khi lên lịch)

Đo thật ở mục "Thời gian thô" phía trên: **0.5B, 500+500 đề (`both`), k=8,
1 vòng ≈ 6.7 tiếng.** Vì A/B/C chỉ chạy **một** bộ đề (n=500, không phải
n=1000 như `both`), ước tính mỗi vòng của A/B/C nhẹ hơn khoảng **một nửa**
— tức 1 lần chạy full 5 vòng của A/B/C ước tính **~15-17 tiếng cho 0.5B**,
1.5B chưa đo thật nhưng kỳ vọng chậm hơn. Vẫn vượt trần 12h/phiên nhưng gần
vừa 1 tuần quota/lần, đỡ hơn hẳn ~33h của thiết kế `both` cũ.

Hệ quả: mỗi lần A/B/C/seed/ablation vẫn cần chia nhiều phiên nối tiếp
(`_save_partial` đã tự ghi kết quả sau mỗi vòng nên phiên sau đọc tiếp
được), nhưng nhẹ hơn thiết kế cũ đáng kể — 6 lần chạy cô lập tổng GPU-giờ
ước tính **thấp hơn hoặc tương đương** 5 lần chạy `both` của kế hoạch trước.

Nếu vẫn quá chậm so với deadline thật: cân nhắc giảm `--k` (8→4) hoặc
`--rounds` (5→3) cho **cả 3 chạy A/B/C cùng lúc** (không phải chỉ một trong
ba — giữ cấu hình giống hệt nhau giữa A/B/C mới so sánh được) — đánh đổi độ
chi tiết lấy tốc độ, ghi rõ trong Limitations nếu làm vậy.
