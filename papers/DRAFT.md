# Khung bài báo — bản nháp (2026-09-03)

Viết bằng tiếng Việt để dễ chỉnh, dịch sang tiếng Anh sau khi nội dung chốt
(nếu yêu cầu nộp là tiếng Anh — kiểm tra `CAU-HOI-THAY.md`). Mỗi mục ghi rõ
**[XONG]** (đã có số/nội dung thật) hay **[CẦN LÀM]** (còn thiếu) để biết
việc gì còn lại.

---

## Tiêu đề (nháp)

*"When the Grader Has a Style: How a Format-Biased Verifier Degrades
Iterative Self-Training in Small Reasoning Models"*

(nháp tiếng Việt: "Khi máy chấm có gu: verifier lệch-vì-văn-phong làm hỏng
tự-huấn-luyện lặp vòng ở model suy luận nhỏ")

**[CẦN LÀM]** — chốt lại sau khi có kết luận cuối, tên hiện tại nhấn đúng
phát hiện chính (sụp, không chỉ "học chữ").

---

## Abstract (nháp ngắn)

Iterative self-training loops (generate → verify → select → train, "GVT")
are used to improve small language models on math reasoning without human
labels, on the assumption that an automated verifier reliably separates
correct from incorrect solutions. We show that when the verifier is
rule-based and exhibits a *directional* bias — rejecting correct solutions
written in unexpected but valid formats (false negatives), while almost
never accepting incorrect ones (near-zero false positives) — this bias
compounds across self-training rounds and can cause **outright capability
degradation**, not merely stylistic convergence. Running the GVT loop for
5 rounds on GSM8K and MATH-500 with `math-verify` as the verifier, we find
that both pass@1 and pass@8 *decline* monotonically for two model sizes
(Qwen2.5-0.5B and 1.5B), with the larger model degrading substantially more
(pass@1: 50.0%→18.6% vs 31.1%→27.4%). Writing style converges alongside the
decline (e.g. `\boxed{}` usage drops by over half at 1.5B). We connect this
to a shrinking-training-pool mechanism: the verifier-accepted example pool
shrinks every round (by ~60% at round 5 for the 1.5B model), so each
round's fresh LoRA adapter is trained on an increasingly narrow, biased
sample. Unlike prior work that studies verifier bias in a single round
(TinyV, From Accuracy to Robustness) or multi-round self-training with a
near-perfect verifier (ReST-EM, Teacher-Free Self-Training), we are — to
our knowledge — the first to combine format-biased verification with
multi-round self-training and measure both capability and stylistic drift
together, on a realistic rule-based math verifier.

**[XONG]** khung nội dung, số liệu thật đã có. **[CẦN LÀM]** rút gọn còn
~150-200 từ đúng chuẩn abstract khi nộp, và xác nhận lại câu so sánh với
Teacher-Free sau khi đọc bản đầy đủ (không chỉ abstract).

---

## 1. Introduction

**[CẦN LÀM]** viết văn xuôi đầy đủ. Ý chính theo thứ tự:

1. GVT-style self-training (STaR/ReST family) là hướng phổ biến để giảm
   phụ thuộc dữ liệu người gán nhãn.
2. Giả định ngầm: verifier đáng tin cậy 100%. Giả định này gần như luôn sai
   trong thực tế với verifier luật (rule-based) trên toán — dẫn số liệu
   Việc 1/Việc 2 (FN thật đo được: GSM8K ~0%, MATH ~7.8%, một số kiểu viết
   bị gạch 100% dù đúng giá trị).
3. Câu hỏi: verifier lệch đó có hại gì khi LẶP NHIỀU VÒNG, không phải 1 lần?
4. Đóng góp (contributions), liệt kê rõ 3 gạch đầu dòng:
   - Đo thật hiện tượng verifier lệch tích luỹ qua 5 vòng, 2 cỡ model.
   - Phát hiện: không chỉ "học lệch văn phong" mà là **sụp khả năng thật**
     (pass@1 và pass@k cùng giảm) — mạnh hơn giả thuyết ban đầu trong tài
     liệu (dự đoán chỉ tính tới 2 kịch bản: giỏi thật, hoặc học-chữ-mà-
     không-giỏi-thêm; kết quả rơi vào kịch bản thứ 3 chưa lường).
   - Phát hiện phụ: mức độ sụp tăng theo cỡ model (1.5B sụp mạnh hơn 0.5B).

---

## 2. Related Work — khác biệt đã xác nhận qua khảo sát 29 bài

**[XONG]** bảng dưới, dựa trên `papers/KHAO-SAT.md` (đã tra lại qua
WebSearch/WebFetch/Semantic Scholar). **[CẦN LÀM]** viết thành văn xuôi liền
mạch thay vì bảng khi hoàn thiện bản nộp.

| Bài | Khung self-training nhiều vòng? | Verifier lệch-vì-format? | Đo văn phong hội tụ? | Khác biệt với bài này |
|---|---|---|---|---|
| ReST-EM (2312.06585) | Có — đúng khung GVT | Không nhắc tới | Không | Họ tin verifier sạch; bài này không tin, đo trực tiếp hậu quả |
| Teacher-Free Self-Training (2606.07856) | Có (đo pass@8 vs pass@64) | **Không** — verifier "chính xác tuyệt đối" (tự thừa nhận, "free exact verifier") | Không | Verifier của họ không lệch; bài này dùng verifier có FN thật đo được |
| From Accuracy to Robustness (2505.22203) | Không — 1 vòng RLVR | **Có** — xác nhận verifier luật gạch nhầm vì format | Không | Họ dừng ở 1 vòng; bài này đo tích luỹ qua nhiều vòng |
| TinyV (2505.14625) | Không — 1 lần train | Có, đo FN ~38% | Không | Cùng hướng nhưng họ SỬA verifier; bài này giữ nguyên verifier, chỉ đo hậu quả |
| Imperfect Verifiers (2510.00915) | Không — 1 vòng RL | Có, dạng nhiễu ρ0/ρ1 | Không | Có framework nhiễu nhưng không phải self-training nhiều vòng |

**Chốt:** chưa bài nào ghép đủ 3 mảnh (verifier lệch-vì-format + nhiều vòng
+ đo văn phong hội tụ). Đây là khoảng trống bài này lấp — đã xác nhận qua
29 bài, xác nhận lại 2 lần (2026-08-23, 2026-08-24).

**[CẦN LÀM — ưu tiên cao]:** đọc **bản đầy đủ** (không chỉ abstract) của
Teacher-Free Self-Training để xác nhận chắc: pass@8/pass@64 của họ có phải
đo qua **nhiều vòng self-training lặp lại** (giống GVT) hay chỉ so 1 model
đã train với chính base model ở các ngân sách khác nhau. Điều này quyết
định câu so sánh trong Related Work có chính xác không.

---

## 3. Method

**[XONG]** nội dung kỹ thuật, đã chạy thật. **[CẦN LÀM]** viết văn xuôi.

- **Vòng lặp GVT:** generate (k mẫu/đề) → verify (`math-verify==0.9.0`,
  antlr4 4.13.2) → select (giữ mẫu verifier chấm đúng) → train (LoRA mới
  từ base, không cộng dồn qua vòng) → lặp.
- **Model:** Qwen2.5-0.5B-Instruct, Qwen2.5-1.5B-Instruct.
- **Dữ liệu:** GSM8K + MATH-500, 500 đề/bộ, k=8 mẫu/đề/vòng, 5 vòng.
- **Train:** LoRA (r=16, alpha=32), SFT qua `transformers`+`peft`+TRL
  `SFTTrainer`, 1 epoch/vòng, không phải GRPO/RL trực tiếp — quyết định có
  ghi lại lý do trong `HUONG-DAN.md` (GRPO không khớp thiết kế select→train
  sẵn có).
- **Đo:** pass@1, pass@8 (per exam preset `default`/`reward`), đếm văn
  phong (11 nhãn: `boxed`, `dfrac`, `tfrac`, `frac`, `dollar`, `sentence`,
  `assignment`, `unit`, `decimal`, `decimal_trailing`, `int_float`), bảng
  A/B/C (đề mới giải được / ổn định / mất đề) so vòng liền trước.
- **Hạ tầng:** Kaggle T4, chạy qua `experiments/viec3/run.py --mode hf`
  (code: `src/dacntt/gvt/`).

**[CẦN LÀM]** ghi rõ 2 giới hạn kỹ thuật vào chính mục Method (không chỉ
Limitations): (1) select và exam đều dùng tập TEST của GSM8K/MATH-500, chưa
tách train/test riêng; (2) mỗi cấu hình chỉ chạy 1 lần, chưa lặp seed.

---

## 4. Results

**[XONG]** — số thật, lấy nguyên từ `results/viec3/qwen05b-n500/table.md`
và `results/viec3/qwen15b-n500/table.md`.

### 4.1 pass@1 và pass@8 qua các vòng

| Model | Vòng 0 | Vòng 1 | Vòng 2 | Vòng 3 | Vòng 4 | Δ (vòng 0→4) |
|---|---|---|---|---|---|---|
| 0.5B pass@1 | 31.1% | 31.9% | 29.9% | 28.9% | 27.4% | −3.7 điểm (−12%) |
| 0.5B pass@8 | 60.5% | 58.9% | 56.1% | 55.5% | 54.9% | −5.6 điểm (−9%) |
| 1.5B pass@1 | 50.0% | 46.2% | 44.5% | 32.4% | 18.6% | **−31.4 điểm (−63%)** |
| 1.5B pass@8 | 72.6% | 71.5% | 70.2% | 63.6% | 48.6% | **−24.0 điểm (−33%)** |

Cả 4 chuỗi đều giảm đơn điệu hoặc gần đơn điệu (0.5B pass@1 có 1 điểm tăng
nhẹ ở vòng 1, còn lại giảm đều) — không phải dao động nhiễu ngẫu nhiên.

### 4.2 Kích thước tập huấn luyện co hẹp dần

| Model | Vòng 0 | Vòng 4 | Giảm |
|---|---|---|---|
| 0.5B (n giữ để ôn) | 2533 | 2123 | −16% |
| 1.5B (n giữ để ôn) | 3962 | 1566 | **−60%** |

### 4.3 Văn phong hội tụ

1.5B, `\boxed{}`: 5608 → 2693 lần (trên 8000 lần viết/vòng) — giảm hơn nửa.
`$...$` (dollar): 1453 → 3406 — tăng hơn gấp đôi. Chi tiết đầy đủ 11 nhãn ở
2 file `table.md` gốc.

### 4.4 Bảng A/B/C (đề thêm/ổn định/mất, 1.5B)

| Vòng | A (thêm) | B (ổn định) | C (mất) |
|---|---|---|---|
| 1 | 47 | 75 | 58 |
| 2 | 53 | 88 | 66 |
| 3 | 51 | 60 | **117** |
| 4 | 44 | 43 | **194** |

C vượt A ở cả 4/4 vòng, khoảng cách nới rộng mạnh ở 2 vòng cuối — đúng dạng
sụp tăng tốc.

**[CẦN LÀM]** vẽ biểu đồ (line chart pass@1/pass@8 theo vòng, 2 model) —
chữ số dạng bảng khó thuyết phục bằng hình khi trình bày.

---

## 5. Discussion — vì sao sụp, vì sao 1.5B sụp nặng hơn

**[CẦN LÀM]** viết đầy đủ, giữ đúng mức độ chắc chắn (giả thuyết, chưa
chứng minh):

- Cơ chế đề xuất: mỗi vòng train 1 adapter LoRA MỚI (từ base) chỉ trên tập
  mẫu verifier-chấp-nhận của vòng trước; vì verifier lệch, tập đó vừa co
  hẹp vừa nghiêng về 1 kiểu viết — vòng sau học từ tập càng hẹp/lệch hơn.
  Đây là một dạng feedback loop tự-siết, gần với "model collapse"
  (Shumailov et al., xem `papers/KHAO-SAT.md` nhóm 4) nhưng xảy ra trên dữ
  liệu ĐÃ QUA LỌC của verifier lệch, không phải toàn bộ dữ liệu tự sinh.
- Giả thuyết vì sao 1.5B sụp nặng hơn: cùng 1 epoch, model có nhiều tham số
  hơn có thể khớp (overfit) nhanh hơn vào đúng tập mẫu đã hẹp — **chưa
  chứng minh trực tiếp**, cần thêm thí nghiệm (ví dụ đo train loss/overfit
  tốc độ mỗi vòng) nếu muốn khẳng định chắc thay vì chỉ nêu giả thuyết.

---

## 6. Limitations

**[XONG]** liệt kê trung thực:

1. Mỗi cấu hình (model × dataset) chỉ chạy **1 lần** — chưa đo phương sai
   qua nhiều seed. Xu hướng giảm khá đều nên khó là nhiễu thuần, nhưng
   không loại trừ hoàn toàn.
2. `select`/`exam` đều dùng **tập test** GSM8K/MATH-500, chưa tách train/
   test riêng — nếu cần chuẩn academic chặt, phải tách trước khi coi là số
   liệu cuối cùng.
3. Chỉ 2 cỡ model (0.5B, 1.5B), chưa rõ xu hướng "to hơn sụp nặng hơn" có
   tiếp tục ở cỡ lớn hơn (7B+) hay đảo chiều ở đâu đó.
4. Chỉ 5 vòng — chưa biết đường cong có tiếp tục giảm, chững lại, hay hồi
   phục nếu chạy thêm vòng.

---

## 7. Conclusion

**[CẦN LÀM]** viết sau khi mục 1 (Introduction) và mục 5 (Discussion) chốt
— tránh viết trước rồi phải sửa lại khi phần thân đổi.

---

## Việc còn lại để hoàn thiện bản thảo, theo thứ tự

1. Đọc bản đầy đủ Teacher-Free Self-Training (2606.07856) — xác nhận rõ
   cấu trúc nhiều-vòng của họ trước khi viết chắc câu so sánh ở mục 2.
2. Đọc bản đầy đủ ReST-EM (2312.06585) — lấy số liệu bảng của họ (nếu có)
   để trích dẫn cụ thể thay vì chỉ nói chung chung "không đo văn phong".
3. Viết văn xuôi đầy đủ mục 1, 2, 3, 5, 7 (hiện đang là gạch đầu dòng/bảng).
4. Vẽ biểu đồ cho mục 4.
5. Quyết định ngôn ngữ nộp (Việt/Anh) sau khi có câu trả lời `CAU-HOI-THAY.md`.
