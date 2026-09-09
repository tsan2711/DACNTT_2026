# Kết quả các lần chạy cô lập A / B / C — số liệu và suy luận để viết vào bài

> **Mục đích file này:** chỗ ghi bền để lần sau (kể cả agent) đọc lại được đầy
> đủ: (1) số thật của các lần chạy cô lập, (2) những gì dự đoán ban đầu đã
> **sai**, (3) những gì **đã kết luận được** và **chưa**. Đây là vật liệu sẽ
> viết thẳng vào `papers/latex/paper.tex` — câu chuyện "dự đoán sai → thu gọn
> scope" chính là thứ làm bài thuyết phục hơn, không phải thứ để giấu.
>
> Cập nhật lần cuối: 2026-09-10 (A và B đều đã có 2 seed; C mới 1 seed).
> Còn thiếu: seed 1 của C, ablation không lọc.

---

## 1. Các lần chạy — config và nguồn file

Tất cả: `--mode hf --model Qwen/Qwen2.5-1.5B-Instruct --n 500 --rounds 5
--k 8 --max-tokens 512 --holdout-frac 0.3 --seed 0`, verifier gốc
(`--patch-verifier` KHÔNG bật). Chỉ khác `--dataset`. Chấm trên tập
**held-out exam** 150 đề (350 đề còn lại chỉ dùng để chọn lời giải train).

| Run | `--dataset` | Thư mục | Ngày chạy | GPU |
|---|---|---|---|---|
| A | `math500` | `results/viec3/qwen15b-math500-a/` | 2026-09-05 | ~ (chưa ghi) |
| B | `math500` + `--patch-verifier` | `results/viec3/qwen15b-math500-b/` | 2026-09-06 | ~ (chưa ghi) |
| C | `gsm8k` | `results/viec3/qwen15b-gsm8k-c/` | 2026-09-06 | ~5.5 giờ |
| A-seed1 | `math500`, `--seed 1` | `results/viec3/qwen15b-math500-a-seed1/` | 2026-09-08 | ~ (chưa ghi) |
| B-seed1 | `math500`, `--patch-verifier`, `--seed 1` | `results/viec3/qwen15b-math500-b-seed1/` | 2026-09-09 | ~ (chưa ghi) |

**Lưu ý về `--seed`:** seed điều khiển **cả** cách chia train/test. Đổi seed
⇒ 150 đề thi khác hẳn ⇒ vòng 0 (model gốc, chưa train) cũng ra điểm khác.
Đây không phải lỗi, và nó cho ta một thước đo phương sai quý (xem mục 2).

Log tham chiếu cũ (thiết kế **gộp** `--dataset both`, n=1000, KHÔNG có
holdout — chấm trên chính đề đã train): `results/viec3/qwen15b-n500/`
(bảng tách theo dataset ở `by_dataset.md`).

---

## 2. Số thật

### Run A — MATH-500 cô lập, verifier gốc

| Vòng | 0 | 1 | 2 | 3 | 4 |
|---|---|---|---|---|---|
| pass@1 | 32.0% | 29.3% | 28.0% | 29.3% | 29.3% |
| pass@8 | 57.3% | 56.7% | 54.7% | 57.3% | 56.0% |

- Đa dạng đáp án trước lọc (unique/k): 0.542 → 0.554 (đi ngang, hơi tăng).
- % đề cả 8 lần ra cùng 1 đáp án: 14.6% → 12.0%.
- Train loss cuối vòng: 0.38 → 0.41 → 0.39 → 0.41 → 0.43.
- **Đọc:** pass@1 giảm ~2.7 điểm rồi ổn định; pass@8 đứng yên. Không sụp.

### Run A, seed 1 — lặp lại A với `--seed 1`

| Vòng | 0 | 1 | 2 | 3 | 4 |
|---|---|---|---|---|---|
| pass@1 | 36.7% | 32.7% | 32.7% | 31.3% | 33.3% |
| pass@8 | 58.7% | 60.7% | 59.3% | 59.3% | 58.7% |

- Đa dạng đáp án: 0.528 → 0.549; % đề cả k lần cùng đáp án: 16.0% → 12.6%.
- Train loss cuối vòng: 0.40 → 0.32 → 0.43 → 0.36 → 0.43 (không giảm đều).
- Tập giữ để train: 833 → 804 (−3.5%).

**So seed 0 vs seed 1 (cùng cấu hình A, chỉ khác seed):**

| | seed 0 | seed 1 |
|---|---|---|
| pass@1 vòng 0→4 | 32.0 → 29.3 (**−2.7**) | 36.7 → 33.3 (**−3.4**) |
| pass@8 vòng 0→4 | 57.3 → 56.0 (**−1.3**) | 58.7 → 58.7 (**0.0**) |
| đa dạng đáp án | 0.542 → 0.554 | 0.528 → 0.549 |

⇒ **Hai seed độc lập cùng một hình dạng**: pass@1 rơi ~3 điểm ở vòng 1 rồi
đứng; pass@8 phẳng. Đây là lần **đầu tiên** trong cả đề tài một dự đoán
(đưa ra sau khi có A/B/C) được xác nhận đúng.

### ⭐⭐ PHÁT HIỆN LỚN NHẤT: severity ≠ prevalence — lý do bản vá vô tác dụng

Đây là mảnh ghép giải thích mà bài thiếu suốt từ đầu. Nó biến kết quả null
từ "không hiểu vì sao" thành "hiểu rõ vì sao".

**Đo trực tiếp tác dụng của bản vá, không confound gì cả.** Ở **vòng 0**,
A và B cùng seed thì dùng cùng model gốc, cùng seed sinh, **chưa train gì**
→ sinh ra **đúng cùng một bộ lời giải** (kiểm chứng: số đếm `\dfrac` trùng
khít, seed 1 đều = 29). Khác biệt duy nhất ở vòng 0 là **verifier nào chấm**.
Kết quả:

| | pass@1 vòng 0 (A, gốc) | pass@1 vòng 0 (B, vá) | chênh |
|---|---|---|---|
| seed 0 | 32.0% | 32.0% | **0 đề / 150** |
| seed 1 | 36.7% | 37.3% | **1 đề / 150** |

Tức là toàn bộ đòn bẩy nhân quả của giả thuyết, đo sạch không nhiễu, tác
động lên **0–1 đề trên 150**.

**Vì sao ít vậy — đếm tần suất `\dfrac`/`\tfrac` thật sự xuất hiện:**

| Bộ đề | Token | Số lần / 4000 lời giải mỗi vòng |
|---|---|---|
| MATH-500 | `\dfrac` | 20–29 (**≈0.55%**) |
| MATH-500 | `\tfrac` | **0** (không bao giờ xuất hiện) |
| GSM8K | `\dfrac`, `\tfrac` | **0** ở mọi vòng |

**Lý luận chốt:** format probe đo được "gạch 100%" — nhưng đó là **severity
có điều kiện** (khi format xuất hiện). Cái chi phối tập train là
**severity × prevalence** = 100% × 0.55% = **0.55% lời giải bị loại oan mỗi
vòng**. Tập train hụt nửa phần trăm thì không thể gây sụp 20 điểm.

Kiểm chứng chéo: trong 10 false negative đã audit thủ công trên MATH-500,
chỉ **2** là format rewrite, **8** là verifier trích nhầm token từ lời giải
dài — mà bản vá **không** xử lý nhóm 8 đó.

**Bài học tổng quát (phần đáng giá nhất để viết vào bài):** các con số
verifier-bias trong literature (14% FN của From-Accuracy-to-Robustness, tỉ
lệ gạch lớn của TinyV) đều là **severity có điều kiện** đo trên một phân bố
tham chiếu nào đó. Muốn biết nó có hại trong pipeline của mình không thì
phải đếm **prevalence trong chính output model của mình** — việc rất rẻ, mà
nhóm em không đếm cho tới khi giả thuyết đã sụp đổ.

### ⭐ Phương sai do chia tập đề — con số hiệu chỉnh quan trọng nhất

Vòng 0 là **model gốc, chưa train gì**. Hai seed lẽ ra phải đo cùng một
model — nhưng ra:

| | seed 0 | seed 1 | chênh |
|---|---|---|---|
| pass@1 vòng 0 | 32.0% | 36.7% | **4.7 điểm** |
| pass@8 vòng 0 | 57.3% | 58.7% | 1.4 điểm |

Toàn bộ 4.7 điểm này đến từ việc bốc 150 đề thi khác nhau, **không** từ
train. Nghĩa là: **phương sai do chọn tập đề (4.7 điểm) LỚN HƠN toàn bộ
"hiệu ứng" ta đang đo** (A giảm 2.7–3.4 điểm qua 5 vòng).

Hệ quả cho cách viết bài:
1. Củng cố mạnh kết luận null của A vs B: chênh lệch 0.6 điểm là cực nhỏ so
   với thang nhiễu tự nhiên của thiết lập này.
2. Nhưng phải nói chính xác: A-seed0 và B-seed0 dùng **cùng** seed nên
   **cùng** split — 0.6 điểm giữa chúng KHÔNG bị ảnh hưởng bởi phương sai
   split này. 4.7 điểm là thước đo "một hiệu ứng phải lớn cỡ nào mới đáng
   tin", không phải thanh sai số trực tiếp cho phép so A vs B.
3. Mọi phát biểu về mức giảm vài điểm (kể cả −12.7 của Run C) phải đặt cạnh
   thang nhiễu này.

### Run B — MATH-500 cô lập, verifier ĐÃ VÁ (control thật cho A)

| Vòng | 0 | 1 | 2 | 3 | 4 |
|---|---|---|---|---|---|
| pass@1 | 32.0% | 28.7% | 28.7% | 28.7% | 28.7% |
| pass@8 | 57.3% | 55.3% | 52.0% | 57.3% | 53.3% |

- Đa dạng đáp án trước lọc (unique/k): 0.542 → 0.555.
- Train loss cuối vòng: 0.39 → 0.40 → 0.38 → 0.37 → 0.44.
- **So trực tiếp A vs B** (chỉ khác đúng 1 biến — `--patch-verifier`, mọi
  thứ khác giống hệt: seed 0, holdout 0.3, math500):

  | | A (gốc) | B (vá) |
  |---|---|---|
  | pass@1 0→4 | 32.0→29.3 (−2.7) | 32.0→28.7 (−3.3) |
  | pass@8 0→4 | 57.3→56.0 (−1.3) | 57.3→53.3 (−4.0) |

  Chênh lệch A/B nằm trong khoảng nhiễu (exam 150 đề, mỗi điểm ≈0.67%),
  không có hướng hệ thống. **Vá đúng chỗ verifier lệch không đổi gì đáng
  kể.** Đây là control sạch nhất trong cả 3 lần chạy (chỉ đổi 1 biến) và là
  bằng chứng trực tiếp bác bỏ giả thuyết gốc, không còn phải suy luận qua
  nhiễm chéo hay thiết kế đo nữa.

### Run B, seed 1

| Vòng | 0 | 1 | 2 | 3 | 4 |
|---|---|---|---|---|---|
| pass@1 | 37.3% | 32.0% | 32.7% | 31.3% | 33.3% |
| pass@8 | 59.3% | 60.7% | 58.0% | 58.7% | 58.7% |

**So A-seed1 vs B-seed1:** từ vòng 2 trở đi pass@1 **trùng khít** (32.7,
31.3, 33.3 ở cả hai). Cặp control giờ có 2 seed, cả 2 đều null.

### Run C — GSM8K cô lập, verifier gốc

| Vòng | 0 | 1 | 2 | 3 | 4 |
|---|---|---|---|---|---|
| pass@1 | 66.7% | 66.7% | 65.3% | 63.3% | 54.0% |
| pass@8 | 92.7% | 90.7% | 93.3% | 90.0% | 90.0% |

- Đa dạng đáp án trước lọc (unique/k): 0.359 → 0.500 (**tăng rõ**).
- % đề cả 8 lần ra cùng 1 đáp án: 33.6% → 16.0% (**giảm rõ** — tản ra).
- Train loss cuối vòng: 0.43 → 0.50 → 0.42 → 0.47 → 0.56.
- **Đọc:** pass@1 giảm ~12.7 điểm, gần hết cú giảm dồn vào vòng 4
  (63.3→54.0); pass@8 gần như phẳng. Model không mất năng lực giải, chỉ
  kém tin cậy ở lần lấy đầu tiên, và đáp án **phân tán hơn** theo vòng.

### Log gộp cũ (tham chiếu, `--dataset both`, KHÔNG holdout)

| | pass@1 vòng 0→4 | pass@8 vòng 0→4 |
|---|---|---|
| GSM8K | 69.6 → 62.0 → 61.0 → 45.6 → **26.6** (−43.0) | 91.4 → … → **65.8** (−25.6) |
| MATH-500 | 30.4 → 30.4 → 28.0 → 19.2 → **10.6** (−19.8) | 53.8 → … → **31.4** (−22.4) |

Tỉ lệ GSM8K trong tập train chung: ~68.8% → 70.2% suốt 5 vòng (ổn định).

---

## 3. Dự đoán ban đầu SAI ở đâu (xếp theo mức độ quan trọng cho bài)

**(1) Sai lớn nhất — verifier lệch format KHÔNG phải nguyên nhân chính.**
Giả thuyết trung tâm của bản nháp: verifier phạt oan `\dfrac`/`\tfrac` →
lọc mất lời giải MATH-500 đúng → tập train lệch dần → tự khuếch đại →
MATH-500 sụp. Run A giữ **nguyên** verifier lệch đó, MATH-500 chạy một
mình: pass@1 −2.7, pass@8 đứng. Cơ chế mà cả bài dựng quanh nó, khi cô
lập, gần như không tạo ra hiệu ứng.

**(2) Sai hướng — đoán nhầm bộ đề nào mong manh.**
Dự đoán: MATH-500 (verifier lệch) dễ sụp, GSM8K (verifier sạch, FN≈0) là
control ổn định. Thực tế ngược, **hai lần độc lập**: (a) 0.5B gộp — GSM8K
sụp mạnh hơn MATH-500; (b) 1.5B cô lập — C mất pass@1 −12.7 so với A −2.7.
Giả định "verifier sạch ⇒ an toàn" sai.

**(3) Sai khi đọc cú sụp nặng của các lần chạy headline cũ là bản chất
vòng lặp GVT.** Log gộp: pass@8 mất 22–26 điểm ở cả hai bộ đề (mất năng
lực thật). Cô lập: pass@8 của **cả A lẫn C đều phẳng**. Phần "mất năng
lực" gần như biến mất khi bỏ train gộp + chấm trên held-out.

**(4) Sai khi gộp "pass@1 giảm" và "sụp năng lực" làm một.** Thiết kế cô
lập tách được: pass@8 (giải được trong k lần) giữ nguyên, chỉ pass@1 (độ
tin lần đầu) trôi. Hiện tượng thật nhẹ hơn và **khác loại** so với "model
collapse".

**(5) Sai về chiều đa dạng.** Bản nháp dựa một phần vào chuyện self-training
làm output hội tụ/nghèo đi. Run C: đa dạng đáp án **tăng** theo vòng
(unique 0.359→0.500; % đề ra cùng 1 đáp án 33.6→16.0). Vòng lặp cô lập làm
đáp án **tản ra**, không đồng nhất hoá — ngược narrative mode-collapse.
(Ghi chú: bản cập nhật 2026-09-05 trong `KE-HOACH-MO-RONG.md` đã bắt đầu
sửa điểm này — "style hội tụ, nội dung đáp án phân tán".)

---

## 4. Kết luận rút được (cập nhật 2026-09-10)

### Đủ vững để viết — kết quả âm tính / phương pháp luận

- **Cú sụp năng lực nặng (pass@8 −22…−26) trong các lần chạy `--dataset
  both` không tái lập** khi mỗi bộ đề được train cô lập trên adapter riêng
  + chấm trên tập held-out. Nó phần lớn là **hiện vật của thiết kế đo**
  (train gộp nhiều domain trên một adapter chung, và/hoặc chấm trên chính
  đề đã train), không phải bằng chứng verifier lệch, không phải bản chất
  GVT.
- **Vá verifier không đổi gì đáng kể (Run A vs Run B, control 1-biến
  sạch).** Đây không còn là suy luận gián tiếp nữa — đo trực tiếp, cùng
  seed/holdout, chỉ khác `--patch-verifier`, hai đường cong gần như trùng
  nhau. Giả thuyết trung tâm của đề tài (verifier lệch → tự khuếch đại →
  sụp) **bị bác bỏ trực tiếp**.

- **MATH-500 cô lập không sụp — đã có 2 seed xác nhận** (A seed 0 và seed
  1): pass@1 rơi ~3 điểm ở vòng 1 rồi đứng, pass@8 phẳng (−1.3 và 0.0).
  Đây là phát biểu vững nhất hiện có.
- **Phương sai do chia tập đề ≈ 4.7 điểm pass@1** ở vòng 0 (mục 2). Cho ta
  thang nhiễu định lượng để đọc mọi con số khác trong bài.
- **Vá verifier không có tác dụng — đã có 2 cặp seed xác nhận** (A vs B ở
  seed 0 và seed 1; ở seed 1 pass@1 từ vòng 2 trở đi trùng khít). Cặp
  control coi như đã chốt.
- **Đã giải thích được VÌ SAO null: severity ≠ prevalence** (mục 2). Format
  bị gạch 100% nhưng chỉ xuất hiện ở ≈0.55% lời giải (và 0% trên GSM8K), nên
  chỉ ~0.55% tập train bị loại oan — không đủ gây sụp. Đo trực tiếp ở vòng 0:
  bản vá đổi kết quả của **0–1 đề trên 150**.

### Tạm thời — cần thêm seed mới chốt

- Erosion pass@1 của Run C (−12.7 điểm GSM8K, dồn vào vòng cuối) — mới 1
  seed. Cần C-seed1 để biết thật hay nhiễu. Lưu ý: −12.7 vẫn **lớn hơn**
  thang nhiễu 4.7 điểm, nên nhiều khả năng là thật, nhưng chưa chứng minh.
  **Đây là nội dung *dương* duy nhất còn sống của bài** — mọi thứ khác đã
  chốt thành kết quả null/phương pháp luận.
- Vòng lặp cô lập làm **tăng** độ phân tán đáp án (rõ ở GSM8K, nhẹ ở
  MATH-500 nhưng nhất quán qua cả 2 seed).

### Chưa kết luận được

- Ablation không lọc (`--no-filter`) — chưa chạy, nên chưa tách được ảnh
  hưởng của khâu **lọc qua verifier** khỏi self-training thông thường.
- Design I mới chỉ có 1 cỡ model (1.5B) — không biết pattern "model to sụp
  nặng hơn" của Design P có tan biến khi cô lập không.

---

## 5. Hệ quả cho luận điểm bài — thu gọn scope

Luận điểm chính cần dịch:

> **Cũ:** "verifier lệch hướng (directional bias) gây sụp năng lực trong
> iterative self-training của LLM nhỏ."
>
> **Mới:** "Chúng tôi định đo sụp-do-verifier-lệch. Khi cô lập confound
> (train riêng từng bộ đề, chấm trên held-out), cú sụp nặng ban đầu hoá ra
> **chủ yếu là hiện vật của thiết kế đo** — train một adapter chung trên
> hỗn hợp nhiều domain đã lọc. Verifier lệch một mình chỉ gây erosion
> pass@1 nhẹ, pass@8 được giữ. Đóng góp của bài là **cảnh báo phương pháp
> luận**: đánh giá GVT/STaR/ReST-EM trên tập gộp nhiều bộ đề dễ tạo ra
> hiện tượng 'collapse' giả."

Yếu hơn tham vọng ban đầu nhưng trung thực, tra lại được, và vẫn là đóng
góp đăng được ở mức workshop LNCS. **Cách kể**: trình bày thẳng chuỗi
"giả thuyết → dự đoán → đo → dự đoán sai → thu hẹp claim" như một điểm
mạnh về tính khắt khe, không phải lỗ hổng cần lấp.

---

## 6. Caveat khi so log cũ ↔ A/C (phải ghi vào Limitations)

Giữa log gộp cũ và A/C có **3 thứ đổi cùng lúc**, không quy sạch được khác
biệt cho riêng "cô lập":

1. Bỏ gộp dataset (`both` → `gsm8k`/`math500` riêng).
2. Thêm `--holdout-frac 0.3` — chấm trên đề **chưa từng** vào tập train
   (log cũ chấm trên chính đề đã train → điểm cao giả, rồi rơi khi hết
   overfit). Riêng yếu tố này đủ giải thích vì sao đường cong cũ "tăng rồi
   sụp" còn đường mới phẳng hơn.
3. n giảm 1000 → 500.

⇒ So sánh **sạch** chỉ tồn tại trong nội bộ A vs C vs B (cùng config).
Log cũ chỉ là mốc tham chiếu lỏng, không dùng làm bằng chứng nhân quả.

---

## 7. Việc còn phải làm trước khi viết mục Results mới

- [x] Run B (`--dataset math500 --patch-verifier --seed 0 --holdout-frac 0.3`)
      — xong 2026-09-06/08. A vs B gần trùng nhau — bác bỏ trực tiếp giả
      thuyết verifier lệch.
- [x] Chạy `analyze_mechanism.py` gộp cả A/B/C
      (`results/viec3/mechanism-ABC.md`) — bảng train-loss + diversity cạnh
      nhau đã có.
- [x] Cập nhật bảng quyết định ở `KE-HOACH-MO-RONG.md` Giai đoạn 1 với
      "hàng thứ 4" (A không sụp, C sụp nhẹ pass@1, B ≈ A).
- [x] **Viết lại `papers/latex/paper.tex`** (2026-09-09) — đổi title
      ("Verifier Bias Is Not Enough"), Abstract, Introduction, Contributions,
      Related Work (Egashira giờ *đồng thuận* chứ không còn mâu thuẫn),
      Setup (thêm §3.3 "Two Experimental Designs" P vs I), Results (§4.1
      Design P → §4.2 confound → §4.3 Design I → §4.4 control A vs B → §4.5
      diversity), Discussion (rút lại claim shrinking-pool; §5.2 thừa nhận
      3-biến-đổi-cùng-lúc), Limitations (6 mục), Conclusion. 2 hình cũ giữ
      nguyên nhưng caption đã ghi rõ là Design P.
- [x] **Viết lại `THUYET-TRINH.md`** (2026-09-09) — kịch bản nói với thầy
      theo đúng câu chuyện mới, kèm mục "nếu thầy hỏi thêm" cho các câu khó
      ("đề tài còn giá trị không", "sao không thấy sớm hơn", "có chắc không").
- [x] **Đánh dấu `papers/DRAFT.md` là lỗi thời** — giữ lại để tra lịch sử,
      không dùng làm nguồn viết bài nữa.
- [x] **Seed 1 cho Run A** — xong 2026-09-08/09. Xác nhận seed 0 (pass@8
      phẳng ở cả hai), và cho ra thang nhiễu 4.7 điểm. Đã đưa vào paper.tex.
- [x] **Seed 1 cho Run B** — xong 2026-09-09/10. Null lặp lại ở seed thứ 2
      (từ vòng 2 pass@1 trùng khít A). Cặp control coi như **đã chốt**. Đồng
      thời phát hiện severity≠prevalence (xem mục 2) — mảnh giải thích cơ
      chế mà bài thiếu suốt từ đầu. Đã đưa vào paper.tex §4.5.
- [ ] **Seed 1 cho Run C** — **việc chạy kế tiếp, ưu tiên cao nhất**. −12.7
      điểm pass@1 của GSM8K là hiệu ứng duy nhất vượt thang nhiễu 4.7 điểm,
      và là nội dung *dương* duy nhất còn sống của bài.
- [ ] Ablation `--no-filter` trên cấu hình headline.
- [ ] Vẽ lại hình cho Design I (hiện chỉ có 2 hình của Design P). Cần một
      hình A/B/C pass@1+pass@8 theo vòng để Results §4.3 không chỉ có bảng.
- [ ] Kiểm tra compile LaTeX qua Overleaf (chưa compile thử bản mới), đếm
      lại độ dài Abstract (LNCS yêu cầu 150–250 từ — bản mới đang dài hơn
      bản cũ, nhiều khả năng vượt, cần cắt).
