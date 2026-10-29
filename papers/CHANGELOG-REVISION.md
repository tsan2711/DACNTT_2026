# CHANGELOG — sửa `paper.tex` thành `paper_revised.tex` (2026-10-18)

Phạm vi: chỉ sửa bản sao `papers/latex/paper_revised.tex`. `paper.tex` và `paper.pdf` giữ nguyên.
Không chạy thí nghiệm mới, không dùng GPU, không thêm trích dẫn mới. Riêng một câu mới về ReST-EM
("fine-tune lại từ base model mỗi vòng") đã được tra trực tiếp trên arXiv 2312.06585.
Mã issue `#n` là thứ tự trong `paper-review-tools/review_results/paper_review/final_issues.json`
(49 issue: 9 major, 25 moderate, 15 minor).

**Lưu ý về cách làm.** Memory "tutor-not-ghostwriter" ghi rằng Bi tự viết, Claude chỉ hỏi và kiểm tra. Lần này
Bi yêu cầu rõ là Claude sửa văn bản, nên phần prose trong `paper_revised.tex` là Claude viết. Vì vậy file này
được viết để Bi **tự bảo vệ được từng thay đổi**: mỗi mục có câu cũ, câu mới, bằng chứng, và lý do câu cũ sai.
Trước khi nộp, Bi nên đọc lại từng mục và viết lại bằng giọng của mình những chỗ mình chưa nói lại được.

---

## 0. Công cụ mới: khoảng tin cậy (CI)

- Script: `experiments/viec3/bootstrap_ci.py`. Chạy bằng
  `.venv/bin/python -m experiments.viec3.bootstrap_ci` (chỉ cần CPU, khoảng 25 phút với 7 worker).
- Output: `results/viec3/ci/ci.md` và `ci.json`. Cache chấm lại từng sample nằm ở `results/viec3/ci/flags/*.json`.
- Phương pháp: chấm lại toàn bộ generation của exam set bằng đúng `math-verify` (preset `reward`). Run B dùng bản
  patched. Sau đó làm **paired bootstrap theo bài toán**: lấy mẫu có hoàn lại 150 bài exam, B=10000, rồi lấy
  percentile 2.5 / 97.5. Resample theo bài, không theo sample, vì k sample của cùng một bài không độc lập với nhau.
- Kiểm tra tái lập: kết quả chấm lại khớp `metrics.csv` ở mọi vòng, trừ 6 giá trị lệch 1 bài (0.6–0.7 điểm). Gần như
  chắc là do `math-verify` timeout khi so sánh (log có "Timeout during comparison"). Đã ghi trong paper.
- **Giới hạn quan trọng:** CI này chỉ bao gồm độ ngẫu nhiên do chọn bài và do sampling. Nó **không** bao gồm
  phương sai giữa các lần train (training-seed variance). Ngay trong data của mình đã có bằng chứng: ở 5e-4 seed 2,
  Run A và Run B có pool vòng 0 bằng nhau (424/424) mà pass@1 R2 vẫn lệch −7.3 [−14.0, −0.7], loại trừ 0 dù gần như
  không khác gì ngoài độ ngẫu nhiên lúc train. Paper đã ghi câu này. (Bản trước dùng ví dụ "replicate lệch 12.8 điểm
  degenerate"; đã bỏ ở đợt sửa thứ hai vì proxy degenerate sai, xem mục 5b.)
- Wilson interval cho FN audit: 10/128 = 7.8% [4.3, 13.8]; GSM8K 0/200, cận trên 1.9%.

---

## 1. Khung bài (title / abstract / contributions) — #9

**Câu cũ (title):** "Verifier Bias Is Not Enough: A Controlled Re-examination of Capability Collapse in Iterative
Self-Training of Small Reasoning Models"

**Câu mới:** "Generate–Verify–Train Iterations Do Not Self-Improve a Small Reasoning Model: A Negative Result with
Qwen2.5-1.5B and a Rule-Based Verifier"

**Abstract cũ (ý chính):** pooled run "appeared to confirm" collapse; isolation thì "the collapse disappears",
"patching changes nothing", "impact is severity × prevalence", "show the verifier is not the driver", "accuracy on
finished solutions holds", "the untrained model gains as much from it".

**Abstract mới (ý chính):** trả lời thẳng câu hỏi trong TOI-HIEU ("học sinh giỏi toán hơn thật, hay chỉ học chữ giáo
viên ưa?") bằng 4 thước đo đã chốt trước:
1. Không có tiến bộ trên held-out: không CI nào của gain pass@1/pass@k loại trừ 0. Số bài mất bằng hoặc nhiều hơn số
   bài thêm ở mọi run trừ một.
2. Không thấy học style verifier: tỉ lệ `\boxed` **giảm** (52→36%).
3. ~~Train mạnh hơn chủ yếu làm model không viết xong~~ (đã thay ở đợt sửa thứ hai, mục 5b): train mạnh hơn làm
   accuracy giảm **kể cả trên lời giải viết xong**; tỉ lệ chạm trần 512 token chỉ tăng 2–14 điểm ở 5e-4, không tăng ở
   lr thấp hơn.
3b. (mới, mục 5b) Một lỗi verifier đo được trên output của chính loop: gold lưu trần, prediction có `\boxed`, loại oan
   16–19% lời giải đúng, làm pass@1 tuyệt đối thấp đi khoảng 5–8 điểm; độ giảm vẫn còn sau khi chỉnh.
4. Hai control (patch, no-filter) thiếu power và khác training dose.
5. Collapse của Design P không lặp lại, nhưng chưa xác định được nguyên nhân vì Design P train ~4.5× nhiều example.

**Vì sao câu cũ sai:** bằng chứng cuối cùng (5e-4, control, anatomy) trả lời câu hỏi "có tự cải thiện không", nhưng
title và abstract cũ vẫn kể chuyện "verifier bias gây collapse", là giả thuyết đã bị bác bỏ.

Contributions viết lại thành 4 ý: (i) câu trả lời âm có CI; (ii) không thấy học style; (iii) ~~termination drift~~
→ (đợt 2) accuracy trên lời giải xong giảm, đo bằng cap-hit, và proxy cũ phóng đại phần "không viết xong"; (iv) bài
học thiết kế (prevalence count, dose; đợt 2 thêm: lỗi gold-storage chiếm khoảng 1/5 lời giải đúng mà chưa được test).
Title không đổi ở đợt 2 vì không nhắc tới "unfinished generations".

---

## 2. Các issue major

### #1 — "pooled design manufactures a collapse"
- **Cũ:** "We show that a pooled design with selection-set scoring manufactures a collapse that isolation and held-out
  evaluation do not reproduce".
- **Mới:** "A sharp decline in an earlier pooled design does not reproduce under isolation and held-out scoring, but
  that design also trained on about 4.5× more examples per round, so its cause is not identified." Mục 4.1 thêm lý
  do thứ ba (training dose) và một câu: chấm trên selection set nếu có ảnh hưởng thì sẽ làm điểm **tăng**, nên không
  giải thích được một cú giảm.
- **Bằng chứng:** pool vòng 0 của Design P 1.5B là 3962 (`results/viec2`/bảng cũ). Run A seed 0 ở 1e-5 là 872
  (`results/viec3/qwen15b-math500-a/metrics.csv`). 3962/872 ≈ 4.5. Design P không lưu train_logs, nên số step là
  suy ra (batch 2, 1 epoch).
- **Vì sao sai:** "manufactures" là một khẳng định nhân quả, nhưng chưa có run nào chỉ đổi pooling, hoặc chỉ đổi cách
  chấm, mà giữ nguyên dose.

### #2, #3, #5 — A/B control không phát hiện được gì; "systematic FN tolerable"; "verifier is not the driver"
- **Cũ:** "The reason is prevalence…", "no-filter and train-on-gold controls show the verifier is not the driver",
  "two quite different setups converging on 'systematic false negatives are tolerable' is the most useful positive
  statement".
- **Mới:** mục 4.3 đổi tên thành "The Patch Control Could Not Detect an Effect". Kết luận chỉ còn: "removing one rare
  format defect had no detectable effect, which the prevalence count alone predicts; it is not evidence about
  directional verifier bias in general." Phần Discussion nói rõ: dữ liệu không trả lời được việc FN có hại hay không.
- **Bằng chứng:**
  - Pool A vs B: 872/876 (seed 0), 833/836 (seed 1) ở 1e-5; 440/443 và 424/424 ở 5e-4.
  - CI của B−A tại R4 ở 1e-5: −0.7 [−3.3, 2.0] và 0.0 [−2.7, 2.7].
  - Ở 5e-4, R2: +5.3 [−2.0, 12.0] (seed 1) và **−7.3 [−14.0, −0.7]** (seed 2, loại trừ 0 nhưng ngược dấu với
    seed 1).
  - Nguồn: `results/viec3/ci/ci.md`.
- **Vì sao sai:** treatment chỉ đổi 0–4 example trên ~870, tức dưới 0.5% pool. Một thiết kế như vậy cho kết quả "null"
  bất kể sự thật là gì, nên null đó không chứng minh được "tolerable" hay "not the driver". Ngoài ra no-filter train
  700 step/vòng, Run A chỉ 163–220 step, nên dose khác nhau.

### #4 — Không có CI, dùng "noise floor 4.7" tự đặt
- **Cũ:** đoạn "Noise floor" (4.7 điểm giữa hai partition) và "exceed the 4.7-point partition noise".
- **Mới:** thêm đoạn "Uncertainty" ở §3.4 mô tả bootstrap, và thêm **Table 7** gồm 19 run, mỗi run có Δpass@1,
  Δpass@k, Δsample acc và finished-matched kèm CI. (Đợt 2: cột finished-matched thay bằng bản theo cap-hit từ
  `experiments/viec3/review_cpu/capanat.py`, B=2000.) Đoạn "Noise" giờ nói thẳng là không dùng một "noise floor" nữa.
- **Bằng chứng:** `results/viec3/ci/ci.md`.
- **Vì sao sai:** 4.7 là chênh lệch giữa hai partition. Nó không phải sai số của phép so sánh paired trong cùng
  partition, và seed 3 còn lệch 10–11 điểm pass@4 (#18).

### #6, #7 — "accuracy on finished solutions holds"
> **Đợt 2 thay thế mục này** (xem mục 5b, F1). Con số "2.2–5.8 điểm" dưới đây dùng proxy degenerate, và đã bị thay
> bằng số theo cap-hit: −5.5 đến −10.6 điểm ở 5e-4. Câu "accounts for much, but not all" đã bị bỏ.

- **Cũ:** "while accuracy on finished solutions holds"; "with accuracy on finished solutions unchanged".
- **Mới:** "accounts for much, but not all, of the decline". Trong §4.6, sau khi so khớp theo độ khó: "the round-2
  finished generations are 2.2–5.8 points less accurate in the four filtered runs (two intervals exclude zero) and
  5.9 and 6.7 points in the no-filter runs… we do not claim that accuracy on finished solutions holds." Trên GSM8K
  thì nói rõ phần finished giảm mạnh.
- **Bằng chứng:**
  - `ci.md`, bảng "Difficulty-matched": A 5e-4 s1 −5.8 [−10.8, −1.0]; s2 −2.2 [−6.4, 2.1]; B s1 −2.8; B s2 −5.7
    [−10.5, −1.2]; NF −5.9 / −6.7.
  - Run C 5e-4: −11.1 [−15.6, −6.8]. Run C 1e-5: −12.0 [−15.6, −8.6].
- **Vì sao sai:** degenerate tập trung ở bài khó. Bỏ chúng đi thì phần còn lại toàn bài dễ hơn, nên accuracy "giữ
  nguyên" chỉ là ảo giác do thay đổi tập bài. So trên cùng tập bài thì accuracy có giảm.

### #8 — "loss does not fall" ở 1e-5
- **Cũ:** "training loss oscillates between 0.68 and 0.84 with no downward trend".
- **Mới:** "The training loss does fall at this rate: within round 0 of Run A it goes from 0.72 to 0.38 (seed 0) and
  from 0.70 to 0.40 (seed 1) over about 420 steps, with an epoch mean of 0.47… The adapter therefore learns, but
  slowly, and it changes the outputs little."
- **Bằng chứng:** `results/viec3/qwen15b-math500-a/train_logs` vòng 0: loss 0.716 → 0.375, train_loss 0.47.
  `…-a-seed1`: 0.700 → 0.404. Số 0.68–0.84 cũ lấy từ `diagnose-lr` chỉ có 120 example
  (`results/viec3/diagnose-lr/sft_examples.jsonl`, 120 dòng).
- **Vì sao sai:** câu cũ trích một diagnostic nhỏ rồi gán cho run thật. Log của run thật cho thấy loss có giảm.
  Bằng chứng "1e-5 gần như không đổi model" chỉ đứng được nhờ hành vi: độ dài 1158→1146, cap-hit 46.9→47.4% và
  40.7→41.8% (đợt 2 đổi từ "degenerate 8.8→9.2%").

### #9 — xem mục 1.

---

## 3. Các issue moderate

| # | Câu cũ (rút gọn) | Câu mới (rút gọn) | Bằng chứng | Vì sao câu cũ sai |
|---|---|---|---|---|
| 10 | (không nói) | §3.1 và Limitation 7: fresh adapter từ base mỗi vòng khiến compounding có rất ít chỗ để xảy ra | `train.py` (adapter mới mỗi vòng) | "Không compound" một phần là do thiết kế, không chỉ là phát hiện |
| 11 | "Hold out evaluation items…, the single change most likely to manufacture…"; "isolation costs less than it appears" | "our data do not rank these factors" | Không có run nào tách riêng từng yếu tố | Xếp hạng nhân quả mà không có thí nghiệm tách biến |
| 12 | "six precautions" viết như luật chung | "These suggestions come from one 1.5B model, one verifier, LoRA SFT and at most three seeds" | — | Tổng quát hoá vượt phạm vi dữ liệu |
| 13 | "loss grows with the learning rate" | "consistent with a dependence… means monotone, but seed 2 alone is almost flat (−3.6, −3.8, −4.6)" | `tab:lrseries`; CI 1e-4/2e-4 chứa 0 | Xu hướng chủ yếu do seed 1 kéo; các bước ở lr thấp nằm trong nhiễu |
| 14 | "accuracy truly falls" (gold) | "part of this drop could be verifier error… have not shown it" | Chưa audit output của gold run | Gold run đổi format rất mạnh (`$` 5→98%), mà vẫn chấm bằng verifier có bias format |
| 15 | Run C "residual effect"; nối các lr với nhau | Run C 1e-5: CI [−21.3, −4.0], 1 run, dose gấp ~2 (951 vs 436 step); 5e-4 khác partition/k/số vòng, chỉ so được Δ trong run | `train_logs` Run C; `ci.md` | 1 seed; so chéo giữa các run không tương đương |
| 16 | "eight times the dfrac class… untested" | **Đợt 2 thay:** bỏ ước lượng 4.4%; thay bằng số đo trên output thật (FN 15.5–18.6%, pool +17–23%), xem mục 5b F2 | `review_cpu/patch_dose.py`, `dose.py` | 4.4% là probe × boxed share; đo thật thì lớn gấp ~4 lần |
| 17 | Run D là "decisive next control" | **Đợt 2 thay:** Run D sẽ đổi pool khoảng 17–23% (≈35–50× Run B), nên khác Run B là nó thật sự tác động lên data; nhưng 1 seed mỗi arm vẫn chỉ phát hiện được hiệu ứng lớn | `dose.py` | Câu đợt 1 ("gần như chắc thiếu power") dựa trên dose 4.4%, sai |
| 18 | "4.7 points" là noise | Thêm seed 3: pass@4 vòng 0 là 40.0 so với 50.0/51.3 | `results/viec3/a-lr1e4-seed3/metrics.csv` | Nhiễu giữa partition lớn gấp đôi con số cũ |
| 19 | "no consistent sign" (no-filter vs A) | pass@1 trái dấu; pass@4 −2.0 / −5.3 âm ở cả hai seed; sample acc seed 2 −5.5 [−9.2, −1.8] | `ci.md` contrasts | pass@4 có dấu nhất quán |
| 20 | gold "2–11 points" | gold pass@4 giảm ~21 điểm, ngang Design P | `ci.md`: −20.7 [−28.7, −12.7] và [−29.3, −12.7] | Câu cũ gộp gold vào khoảng của self-training |
| 21 | "0.55% of solutions wrongly discarded" | `\dfrac` xuất hiện ở 20–29/4000 generation (0.50–0.73%), và chỉ phần đúng trong số đó bị loại oan; pool lệch 0–4 example | `styles.csv` các run 1e-5 | Nhầm tần suất format với số lời giải đúng bị loại |
| 22 | Patch được trình bày như "sửa verifier" | "The patched verifier is therefore still biased: it keeps the wrong-token extractions (8 of 10…)" | `results/viec2/table.md` | Patch chỉ sửa một lớp lỗi nhỏ |
| 23 | (không bàn) | Thêm đoạn: no-filter (~2/3 sample sai) không tệ hơn rõ rệt, căng với phát hiện FP của Egashira; nhưng 2 seed, SFT chứ không phải RL, dose khác | `tab:controls` | Bỏ qua một mâu thuẫn rõ ràng với tài liệu |
| 24 | Novelty = tổ hợp "verifier đo được bias + nhiều vòng + patch control" | Positioning hạ giọng: phần đặc trưng (patch) hoá ra trơ, nên không lấy nó làm đóng góp | — | **Chỉ sửa một phần:** muốn so kỹ hơn thì cần trích dẫn mới, mà quy định là phải tra live; lần này không thêm |
| 25 | ReST-EM chỉ được nhắc qua | Thêm: ReST-EM cũng fine-tune lại từ base mỗi vòng | Tra arXiv 2312.06585: "each Improve step fine-tunes the base model instead of the model obtained from the previous ReST iteration" | Bỏ sót điểm giống nhất với thiết kế của mình |
| 26 | "pool contraction and collapse… come apart" | Pool size gần như là định nghĩa (= sample acc × số sample); trên pass@1 nó đi cùng chiều | Run C pool −20%, pass@1 −12.7 | Chỉ đúng với pass@8 |
| 27 | Đo diversity nhưng không báo metric chính | Báo unique-answer fraction 0.542→0.554 (A s0); rút gọn mục 4.4 | `results/viec3/mechanism-ABC.md` | **Một phần:** không thêm bảng, chỉ thêm số và hạ kết luận |
| 28 | "This fits… first-attempt reliability rather than stylistic convergence" | Agreement gắn cơ học với accuracy và với generation chạm trần token; không loại trừ được hội tụ style | — | Bài đúng hết k lần thì tự động là bài "đồng thuận" |
| 29 | "all four runs" xem như 4 replicate | "closer to two independent replicates than four" | A và B cùng seed chung partition và chung output vòng 0 | Đếm trùng |
| 30 | Ngưỡng degenerate 1500 ký tự không kiểm tra | **Đợt 2 thay:** bỏ hẳn proxy khỏi phần phân tích chính; dùng cap-hit (re-tokenize, ≥508 token). Kiểm tra độ nhạy theo ngưỡng ký tự ở đợt 1 đã bị xoá vì chính proxy sai, không phải ngưỡng | `review_cpu/caphit.py`, `capanat.py` | Đợt 1 kiểm ngưỡng nhưng không kiểm proxy có đo đúng "chạm trần" hay không; nó không đo đúng |
| 31 | "Removing the truncation did not reduce the drift" như một kết luận | **Đợt 2:** "changed little in this one run: cap-hit R2 43.8% (limit 1024) vs 43.0% (replicate) vs 46.2% (A gốc); matched finished −5.7 / −5.0 / −9.1. With one run per arm this can only exclude a large truncation effect" | `capanat.py` trên `a-lr5e4-msl1024`, `a-lr5e4-keep` | Một run mỗi arm không phân biệt được với nhiễu giữa các lần train |
| 32 | "the untrained model gains as much" | "gains **more**… (+6.9 vs +5.9, +2.0, +3.5)" | `tab:reeval`: 36.3→43.2; 28.3→34.2; 27.5→29.5; 28.5→32.0 | Sai số học trên chính bảng của paper |
| 33 | Thiếu chi tiết reproduce | Thêm prompt, T=0.8, cap 512, q_proj/v_proj, batch 2, AdamW, linear decay, loss trên toàn chuỗi, max_length 512 tính cả prompt, định nghĩa pass@1 = sample đầu | `generate.py` (MATH_USER), `train.py` (SFTConfig; dataset dạng `messages`, không bật assistant-only loss) | — |
| 34 | "checked manually" | "established by a scripted comparison of the boxed answer with the gold string (src/dacntt/read.py)… only rejected solutions inspected, so no FP rate" | `src/dacntt/read.py`; `results/viec2/table.md` (128 = 200 − 24 gold không parse được − số sai) | Không phải đọc tay; đó là so sánh bằng script |

---

## 4. Các issue minor

| # | Cũ → Mới | Bằng chứng |
|---|---|---|
| 35 | "lost at any cap" → "tripling the cap does not remove the gap, for single adapters on one partition" | 2 cap, 1 partition |
| 36 | Điểm đồng thuận với Xu et al. → nêu cụ thể (lost > added) và nói rõ mình thiếu frozen arm theo từng vòng | — |
| 37 | "sharply for two model sizes" → 0.5B chỉ giảm −3.7 / −5.6 | `tab:passk` |
| 38 | "40–50%" → "41–52%" | +42.8, +41.2, +42.2, +49.7, +42.0, +52.1 (`tab:anatomy`) |
| 39 | "keeps about 31%" → "31% at round 0 and 23–25% by round 2" | 440/1400, 424/1400; 326/1400 = 23.3%, 350/1400 = 25.0% |
| 40 | "0–3 problems" → "0–3 examples" (và 0–4 ở 1e-5) | pool A/B |
| 41 | MATH-500 R3 pass@8 45.0 → 44.8 (preset reward, preset dùng để chọn), chú thích bản default 45.0 | `results/viec2` per-dataset |
| 42 | "1.7–7.8% in every run" → "0–7.8%" (đợt 2: câu này bị xoá cùng proxy) | Run C và gold có degenerate với 0% accuracy |
| 43 | "one RLVR phase" → "offline rejection-sampling SFT with a fresh adapter per round, not on-policy RL" | — |
| 44 | "about 14%… consistent with ours" → "7.8% (Wilson 4.3–13.8%)… same order of magnitude, with different verifier version, source and error mix" | `ci.md` Wilson |
| 45 | "one-off cost of the first round" → "cannot be distinguished from noise… only no evidence of compounding". Khoảng R0→R1 đổi thành 2.7–5.3 | `ci.md` cột R0→R1: −2.7, −4.0, −3.3, −5.3, mọi CI chứa 0 |
| 46 | "pass@8 comparatively intact" → bỏ (Design P có agreement giảm mạnh nhất và pass@8 cũng giảm mạnh nhất) | — |
| 47 | gold "replicate round" → rounds là replicate fine-tune trên data giống hệt (loss 0.6527/0.6524/0.6524), nên chênh R1/R2 chủ yếu là sampling noise | `train_logs` gold |
| 48 | Mô tả văn bản degenerate → ghi "word 5-gram repeat ratio" và "rests on inspection of examples, not systematic annotation" | **Một phần:** chưa annotate có hệ thống |
| 49 | "n = 500" → nói rõ 350 selection / 150 exam; pass@1 là một lần lấy mẫu | `run.py _split_train_test` |

**Sửa số nhỏ khác:**
- Table 4: A seed 1 Δpass@1 −3.4 → −3.3. Giá trị đúng là 36.67 − 33.33 = 3.33; con số cũ lấy hiệu của hai số đã làm
  tròn.
- Table 8: dòng 1e-5 đổi từ "8.8→8.8%, 38.5→37.2%" thành **R0→R4** "8.8→9.2%, 38.5→36.9%". Số cũ thật ra là vòng 2,
  trong khi caption ghi R0→R4. Nguồn: `ci.json` levels A_1e-5_s1. (Đợt 2: cả bảng đổi sang cột cap-hit, xem mục 5b.)
- Bỏ dòng comment "generated draft, pending author verification", thay bằng comment ghi chú bản sửa, trỏ tới file này.

---

## 5. Issue chưa sửa được hoặc chỉ sửa một phần, và lý do

- **#24** (novelty): chỉ hạ giọng. Muốn so kỹ với các bài khác thì phải thêm trích dẫn đã tra live; lần này cố ý không
  thêm.
- **#27, #48**: thêm số và hạ kết luận, nhưng không làm bảng diversity hay annotate hệ thống.
- **#14**: chỉ nêu giới hạn. Audit tay output của gold run là việc **CPU**, Bi tự làm được, không cần Kaggle.
- **Table 9 (re-eval)**: không có CI, vì `reeval.py` chỉ lưu JSON tổng hợp, không có dữ liệu theo từng bài. Đã ghi
  trong caption.

### Các run Kaggle chỉ cần nếu muốn khẳng định lại những điều đã rút bỏ (KHÔNG chạy)

| Mục đích | Config | Lý do |
|---|---|---|
| Tách "chấm trên selection set" khỏi "pooling" | `run.py --dataset both --holdout-frac 0.3 --seed 0 --k 8 --rounds 5`, lr 1e-5 (default cũ), 1.5B | Muốn nói lại câu "pooling gây collapse" (#1) |
| Tách dose khỏi pooling | Isolated MATH-500, lr 1e-5, nhưng cho số optimizer step bằng Design P (~1981 step ở vòng 0, ví dụ lặp ~4.5 epoch, hoặc ghép thêm data) | #1: Design P train ~4.5× |
| Positive control cho A/B | Verifier cố ý từ chối một format phổ biến (ví dụ mọi đáp án có `\boxed` chứa phân số), MATH-500, 5e-4, k=4, 3 vòng, 2 seed | Chứng minh thiết kế phát hiện được hiệu ứng (#2) |
| Frozen arm mỗi vòng | Model chưa train sample lại mỗi vòng, cùng partition, k=4, 3 vòng | So với Xu et al. (#36) |
| Thêm seed Run C | `--dataset gsm8k --holdout-frac 0.3 --seed 2/3 --k 4 --rounds 3 --lr 5e-4` | #15: Run C hiện chỉ có 1 run mỗi lr |
| Run D (đợt 2) | `run.py --mode hf --model Qwen/Qwen2.5-1.5B-Instruct --dataset math500 --n 500 --rounds 3 --k 4 --max-tokens 512 --seed 1 --holdout-frac 0.3 --learning-rate 5e-4 --patch-verifier-boxed --out results/viec3/d-math500-lr-fixed` (seed 2: `--seed 2 --out results/viec3/d-math500-seed2`). Flag `--patch-verifier-boxed` có trong `run.py` dòng 725. Chấm D−A bằng verifier **gốc** để so cùng thước | Muốn nói gì về "FN có hệ thống có hại không" (#2, #3). Paper hiện không khẳng định điều đó, nên run này không bắt buộc |

Không run nào ở trên là bắt buộc cho các khẳng định **hiện có** trong `paper_revised.tex`. Mọi khẳng định đã được hạ
xuống mức mà dữ liệu hiện tại đỡ được.

---

## 5b. Đợt sửa thứ hai: hai phát hiện của evaluator (F1, F2)

Nguồn: `papers/REVIEW-VERIFIED.md` và `experiments/viec3/review_cpu/`. Mình **chạy lại** script của evaluator
(chép sang scratchpad, token cache mới, tokenizer Qwen2.5-1.5B-Instruct local): `caphit.py` (2 run), `capanat.py`
(21 run), `dose.py`, `flips.py`, và `patch_dose.py` cho A 5e-4 seed 1. Mọi số dưới đây là số mình chạy ra, không
chép từ báo cáo. Vẫn không chạy GPU, không chạy Kaggle.

### F1 — proxy "degenerate" phóng đại vai trò của generation không viết xong

**Bằng chứng (chạy lại):**
- Cap-hit = text đã decode, tokenize lại ra ≥508 token (trần sinh là 512). Base model, MATH-500 exam: **43.0–43.2%**
  generation chạm trần (seed 3: 48.2%; GSM8K 3.5–3.8%). Proxy (>1500 ký tự, không `\boxed`) chỉ bắt **9.8%**. Giao
  của hai tập ở R0 chỉ có 59/600 generation (A 5e-4 s1).
- Ký tự/token: text bị proxy gắn cờ có 3.31 (R0), 4.93–5.03 (R2); phần còn lại 2.73–3.04. Nghĩa là text trôi dạt
  "dài theo ký tự" nhưng không dài hơn theo token.
- Cap-hit R0→R2 ở 5e-4: A 43.2→46.2, 43.0→51.2; B 43.2→47.8, 43.0→54.0; NF 43.2→45.5, 43.0→57.2 (tăng **2.3–14.2**
  điểm). Ở 1e-4: 43.2→42.7, 43.0→42.8, 48.2→45.7; ở 2e-4: 43.2→40.8, 43.0→39.7 (**không tăng**). Trong khi đó proxy
  ở các lr này tăng từ 9% lên 19.5–25%.
- Finished acc (dưới trần) R0→R2: A s1 54.0→43.0, A s2 50.6→45.4. Matched theo độ khó, B=2000:
  A −9.1 [−14.2, −4.2], −5.5 [−11.7, +0.1]; B −6.8 [−12.4, −1.0], −5.9 [−10.9, −1.0]; NF −10.6 [−16.4, −5.5],
  −6.6 [−11.4, −2.0]; 1e-4: −4.3, −3.5, −0.6; 2e-4: −4.0, −4.7 (CI đều chứa 0); Run C 5e-4 −12.1 [−16.6, −7.9].
- Phân rã đối xứng Δsample acc = phần finished + phần tỉ lệ cap-hit + phần acc trong cap-hit (script riêng của mình,
  ở scratchpad, không commit): phần finished chiếm 34–73% ở 6 run 5e-4. REVIEW (Shapley) ra 35–74%; khớp, lệch do
  làm tròn.

**Thay đổi trong paper (câu cũ → câu mới, rút gọn):**

| Chỗ | Cũ | Mới |
|---|---|---|
| Abstract | "Stronger training mostly makes the model stop finishing: generations that run long without an answer rise from about 9% to 36–43%… accounts for much, but not all, of the decline." | "Stronger training lowers accuracy, including on the generations that finish within the token cap: matched for problem difficulty, finished accuracy falls 5–11 points at 5×10⁻⁴, while the share… that hit the 512-token cap, already 43% for the untrained model, rises only 2–14 points at that rate and not at all at lower rates." |
| Intro | "What does appear… is a rise in generations that never reach an answer." | "…lower accuracy on the solutions the model does finish, with a smaller rise in generations that run out of tokens." |
| Contribution 3 | "unfinished, drifting generations grow with the learning rate… account for much but not all" | Finished acc (matched) giảm ở mọi lr > 1e-5, chiếm khoảng 1/3–3/4 mức giảm ở 5e-4; cap-hit chỉ tăng ở 5e-4, 2–14 điểm; "A character-length heuristic we first used overstated the role of unfinished generations, and we show why." |
| §3.4 Uncertainty | Ví dụ "replicate lệch 12.8 điểm degenerate" | Ví dụ A−B seed 2 ở 5e-4: −7.3 [−14.0, −0.7] |
| §4.2 (1e-5) | "share of long unboxed generations essentially unchanged" | cap-hit 46.9→47.4%, 40.7→41.8% |
| §4.5 | "The degenerate share… gives a clearer rate dependence than accuracy does." | "The share… that hit the token cap does *not* follow the rate: it is flat or falls at 1e-4 and 2e-4 and rises only at 5e-4." |
| Table lrseries | Cột "Degen. (R2)": 19.5, 19.5, 22.7, 25.0, 22.2, 41.3, 36.3 | Cột "Cap-hit (R2)": 42.7, 42.8, 45.7, 40.8, 39.7, 46.2, 51.2; caption ghi R0 = 43.0–43.2% (48.2% seed 3) |
| Table ci | Cột "Finished, matched" theo proxy | Theo cap-hit, từ `capanat.py` (B=2000) |
| §4.6 + Table anatomy | Cột Degenerate / Non-degen acc; câu "termination failure accounts for much of the decline"; câu độ nhạy ngưỡng 1200–2000 | Cột Cap-hit / Finished acc / Matched Δ. Đoạn mới "An earlier proxy overstated termination" (9.8% vs 43.2%, ký tự/token). Đoạn "Stronger training lowers accuracy on finished solutions". Câu độ nhạy ngưỡng bị xoá |
| Run C 5e-4 | degenerate 2.5→16.7%, finished 71.5→64.6 | cap-hit 3.8→15.0%, finished 71.9→63.3, matched −12.1 |
| Run C 1e-5 | "degenerate share rises only 2 points" | cap-hit 3.5→4.2%, matched −12.8 |
| Kiểm tra truncation | degenerate 37.2% vs 30.0% (re-eval) | cap-hit R2 43.8 (limit 1024) / 43.0 (replicate) / 46.2 (A gốc); matched −5.7 / −5.0 / −9.1 |
| Table reeval | Caption không cảnh báo | Ghi rõ cột Degenerate / Acc. finished dùng proxy, đếm thiếu cap-hit, chỉ để tham khảo (re-eval chỉ lưu JSON tổng, không tính lại cap-hit được) |
| Discussion, Practical, Limitation 4–5, Conclusion, Future work | "model increasingly fails to finish…" | "less accurate on the solutions it does finish… more generations hit the cap only at 5e-4"; suggestion "save token counts and report cap-hit directly"; Limitation 5: cap-hit là tái dựng bằng re-tokenize |

**Vì sao câu cũ sai:** proxy được chọn theo ký tự, mà text trôi dạt có nhiều ký tự/token hơn. Vì vậy proxy tăng
mạnh khi style đổi, kể cả khi số generation chạm trần không đổi (1e-4, 2e-4). Đồng thời nó bỏ sót phần lớn
generation chạm trần ngay từ base model. Kể "train mạnh làm model không viết xong" là đọc nhầm thay đổi style thành
thay đổi termination. Kiểm tra độ nhạy theo ngưỡng ở đợt 1 không bắt được lỗi này, vì lỗi nằm ở đại lượng được đo.

### F2 — lỗi gold-boxed (lớp của Run D) đo trên output của chính loop

**Bằng chứng (chạy lại `dose.py`, `flips.py`; `patch_dose.py` chạy lại cho A s1, các run khác dùng file `patched/`
có sẵn):**
- Kept pool khi thêm patch boxed: A 5e-4 s1 R0 440→542 (+23.2%), R1 +21.0%, R2 +18.8%; A s2 R0 +21.7%, R2 +17.1%;
  A 1e-5 s0 R0 872→1066 (+22.2%), R1–R4 +19.7–21.3%. Patch `\dfrac` (Run B) chỉ đổi 0–4 example.
- Tỉ lệ FN trong lời giải đúng (patched − gốc)/patched, trên 500 bài: A s1 18.6/16.9/16.2%; A s2 17.9/17.9/15.5%;
  A 1e-5 s0 18.3/17.9/17.5/16.8/16.8%. Khoảng **15.5–18.6%**, với giả định verifier đã patch không false-accept.
- pass@1 exam, gốc → patched: A s1 33.3→40.0 (R0), 23.3→28.0 (R2); A s2 31.3→38.0, 27.3→32.0; A 1e-5 s0 R0
  32.0→40.0, R4 29.3→36.7; gold s1 R1/R2 +0.7, gold s2 +2.6/+3.3. Vậy offset là **+6.7 đến +8.0** ở R0 và suốt 1e-5,
  **+4.7** ở R2 của 5e-4, nhỏ hơn với gold. Không phải "đều 7 điểm".
- `flips.py`: 143 flip (evaluator ghi 144; lệch 1 do timeout của math-verify). Mình đọc 30 cặp (gold | boxed cuối)
  trong mẫu của mình: cả 30 đều cùng giá trị, ví dụ `\frac43` vs `\frac{4}{3}`, `(15,-29)` vs `(15, -29)`. Evaluator
  ghi 29/30, có một ca hộp rỗng. Mẫu của mình lệch nhẹ (143 vs 144 flip), nên không có ca đó. Paper ghi theo con số
  thận trọng hơn: 29/30.
- Độ giảm vẫn còn sau khi patch: A s1 40.0→28.0, A s2 38.0→32.0, gold 40.0→16.0 và 38.0→13.3, A 1e-5 s0 40.0→36.7.
- 17/41 vs 17/200: comment trong `src/dacntt/verify/adapter.py` dòng 26–27 ghi "17/200 MATH-500 gold answers, 8.5%".
  Đúng: 8.5% = 17/200. 17 là một phần của 41 boxed rewrite bị từ chối.

**Thay đổi trong paper:**

| Chỗ | Cũ | Mới |
|---|---|---|
| §3.2 format probe | "Of those 41, 24 are gold answers… (Section conclusion)." | Thêm: "The other 17 (17 of the 200 boxed probes, 8.5%) are compound answers such as 3√13: the gold is stored without a delimiter…" |
| §3.2 đoạn mới | (không có) | "The gold-storage defect in the loop's own outputs": FN 15.5–18.6%, pool +17–23% (440→542; 872→1,066), 29/30 flip là cùng giá trị, giả định không FP, offset pass@1 (+6.7–8.0 ở R0 và 1e-5; +4.7 ở R2 5e-4; +0.7–3.3 gold sau R0), giá trị patched R0→cuối. Nguồn: `review_cpu/patch_dose.py`, `dose.py`, `flips.py`. **Không** thay số trong các bảng, theo yêu cầu: các bảng giữ verifier gốc (verifier loop thật sự dùng) và câu này nói rõ offset |
| Abstract | "Patching one verifier defect…" | Thêm câu về defect 16–19%, offset 5–8 điểm pass@1 của self-training, độ giảm còn sau khi chỉnh; "Patching a rarer defect…" |
| Related work | "Our MATH-500 audit gives 7.8%…" | Thêm: "a pipeline-specific defect alone rejects 15.5–18.6% of the loop's own correct solutions" |
| Egashira | "patch control cannot test their FN finding…" | Thêm: "…and the much larger false-negative class we measured afterwards is present in both arms" |
| §4.3 patch control | "…not evidence about directional verifier bias in general." | Thêm: Run B không đụng tới defect gold-storage, defect này có ở cả hai arm |
| §5.2 Interpretation | "Whether systematic FN are harmless… cannot say." | Thêm: FN có hệ thống duy nhất đo được là phổ biến, có ở mọi run, chưa từng được thay đổi |
| Contribution 4 | — | Thêm "a second, untested defect… affects about a fifth of the loop's correct solutions" |
| Limitation 6 | "Both A and B carry the larger gold-storage defect described in Section conclusion." | Đo lại bằng re-scoring; offset 5–8 điểm; có ở mọi run; chưa từng thay đổi trong run train; giả định không FP |
| Conclusion | "Patching one verifier defect…" | "Patching a rare verifier defect…" và thêm: defect gold-storage loại khoảng 1/6 lời giải đúng, có mặt không đổi ở mọi thí nghiệm |
| Future work | "17 of the 41… i.e. 17/200 = 8.5%… ≈52% boxed share… rough damage estimate of 4.4%… check on the pipeline" | Run D sẽ đổi pool 17–23%, khoảng 35–50 lần Run B, nên thật sự tác động lên data; 1 seed mỗi arm vẫn chỉ phát hiện được hiệu ứng lớn |

**Vì sao câu cũ sai:** 4.4% là kết quả nhân severity của probe (trên gold được viết lại) với tỉ lệ `\boxed`, chứ
không phải phép đo trên output thật. Đo trên output thật thì lớp lỗi này lớn hơn khoảng 4 lần, và lớn hơn lớp `\dfrac`
hơn 30 lần. Hệ quả: (a) mọi accuracy tuyệt đối trong paper thấp hơn thực tế khoảng 5–8 điểm; (b) câu kiểu "Run B cho
thấy FN không quan trọng" càng không đứng được, vì Run B chỉ test lớp ~0.1%. Lớp lớn thì có mặt ở cả hai arm.

---

## 6. Biên dịch

`pdflatex` và `latexmk` không có trên máy. Đã biên dịch bằng `tectonic` (đã cài sẵn ở `/opt/homebrew/bin`, engine
XeTeX), output vào scratchpad rồi chép ra `papers/latex/paper_revised.pdf`. `paper.pdf` không bị đụng. Kết quả: 20
trang (bản cũ 18 trang), không còn overfull box và không còn reference chưa định nghĩa. **Sau đợt 2: 21 trang**,
vẫn sạch (không overfull, không undefined reference). Bản dài hơn chủ yếu vì thêm
Table 7 (CI). Nếu cần đúng 18 trang thì có thể chuyển Table 7 sang phụ lục.

---

## 7. Câu giáo sư có thể hỏi (và câu trả lời thật)

1. **"Vậy rốt cuộc GVT có giúp gì không?"** Trên setup này thì không. Không run nào tăng pass@1 hay pass@k với CI
   loại trừ 0. Số bài mất bằng hoặc nhiều hơn số bài thêm ở 18/19 run. Đây là kết quả cho 1.5B, LoRA r=16 trên
   q/v, một verifier, tối đa 5 vòng, restart từ base. Không suy rộng ra RL hay model lớn.

2. **"Các em nói collapse của Design P là do pooling, giờ lại bảo không biết?"** Đúng, bản cũ khẳng định quá mức.
   Design P khác Design I ít nhất bốn thứ cùng lúc, trong đó có dose gấp ~4.5×. Mà chính dữ liệu của bọn em cho thấy
   train mạnh hơn thì giảm nhiều hơn. Muốn biết thật thì cần run pooled có held-out, hoặc run isolated với dose khớp
   Design P (mục 5).

3. **"Control A/B null thì có nghĩa là verifier bias vô hại không?"** Không. Patch chỉ đổi 0–4 example, dưới 0.5%
   pool. Thiết kế này không thể phát hiện hiệu ứng nào, và đếm prevalence trước khi chạy là đã biết điều đó. Đây là
   bài học thiết kế, không phải bằng chứng.

4. **"CI của các em có tin được không?"** Tin được cho phần nó đo: chọn bài và sampling, với một adapter cố định. Nó
   không đo nhiễu giữa các lần train. Bằng chứng: A và B ở 5e-4 seed 2, pool vòng 0 như nhau, mà pass@1 R2 lệch −7.3
   [−14.0, −0.7], CI vẫn loại trừ 0. Nên "CI loại trừ 0" là điều kiện cần, chưa đủ.

5. **"Sao ở 1e-5 nói 'loss không giảm' mà log lại giảm?"** Câu cũ sai. Nó lấy diagnostic 120 example, không phải log
   của run thật. Log thật giảm 0.72→0.38. Lập luận đúng là: model có học, nhưng đầu ra gần như không đổi (độ dài,
   tỉ lệ chạm trần token đi ngang: 46.9→47.4%, 40.7→41.8%).

6. **"Accuracy trên lời giải viết xong có giữ không?"** (trả lời đợt 2) Không. Đo "viết xong" bằng số token thật
   (dưới 508/512), so trên cùng tập bài thì ở 5e-4 nó giảm 5.5–10.6 điểm, 5/6 CI loại trừ 0. Ở 1e-4, 2e-4 giảm
   0.6–4.7 điểm, CI chứa 0. Trên GSM8K giảm khoảng 12–13 điểm. Ở 5e-4, phần giảm accuracy trên lời giải xong chiếm
   khoảng 1/3 đến 3/4 mức giảm sample acc. Phần "không viết xong" chỉ đáng kể ở 5e-4. Câu trả lời đợt 1 ("phần lớn là
   do không viết xong") là sai, vì nó dựa trên proxy ký tự.

7. **"No-filter không tệ hơn, vậy verifier có tác dụng gì?"** Ở 2 seed, pass@4 nghiêng về có filter (−2.0, −5.3),
   sample acc seed 2 −5.5 (CI loại trừ 0), seed 1 thì +0.2. No-filter lại train gấp 3–4 lần step. Bọn em không kết
   luận được gì mạnh theo chiều nào.

8. **"Train-on-gold giảm 20 điểm, có phải do verifier chấm sai format không?"** Có thể là một phần. Gold run đổi
   format rất mạnh, và bọn em chưa audit tay output của nó. Bọn em nghĩ verifier không giải thích được hết cú giảm
   33→15%, nhưng chưa chứng minh. Việc audit này làm bằng CPU được.

9. **"'Degenerate' định nghĩa kiểu gì, có phải chọn sau khi thấy data không?"** (trả lời đợt 2) Có, nó được chọn
   sau khi thấy data, và nó **sai**. Re-tokenize lại text thì base model đã chạm trần 512 token ở 43% generation,
   còn proxy chỉ bắt được 9.8%. Proxy tăng theo lr chủ yếu vì text trôi dạt có nhiều ký tự/token hơn (3.3 → 4.9–5.0,
   so với 2.7–3.0), không phải vì chạm trần nhiều hơn. Kiểm tra ngưỡng 1200/2000 ở đợt 1 không phát hiện ra điều
   này, vì lỗi nằm ở cách đo chứ không ở ngưỡng. Paper bản sửa đã bỏ proxy và ghi rõ điều này ở §4.6.

10. **"Vì sao lr gốc là 1e-5?"** Đó là default của code, không được tune. Đây là giới hạn đã ghi (Limitation 4).

11. **"Bao nhiêu phần bài này do AI viết?"** Phần văn bản sửa đổi lần này do Claude soạn theo yêu cầu của Bi. Số
    liệu đều lấy từ `results/viec3` và được kiểm lại bằng script. Bi cần tự nói lại được từng mục trong file này
    trước khi nộp.

12. **"Nếu verifier loại oan 16–19% lời giải đúng, thì mọi con số trong bài đều sai à?"** Số tuyệt đối thì thấp hơn
    thực tế khoảng 5–8 điểm pass@1 ở các run self-training: +6.7–8.0 ở vòng 0 và ở 1e-5, +4.7 ở vòng 2 của 5e-4.
    Bọn em giữ số của verifier gốc trong bảng vì đó là verifier mà loop thật sự dùng để chọn data. Kết luận chính là
    về **thay đổi** qua các vòng, và nó vẫn đúng sau khi chấm lại: ví dụ A 5e-4 seed 1 là 40.0→28.0 thay vì 33.3→23.3.
    Tỉ lệ 16–19% là cận trên theo nghĩa nó giả định verifier đã patch không chấp nhận nhầm. Bọn em chỉ kiểm tay 30 flip.

13. **"Sao không chạy Run D luôn?"** Lúc đó bọn em ước lượng dose chỉ 4.4% nên nghĩ nó sẽ null. Đo lại thì nó đổi
    khoảng 1/5 pool, nên nó là control đáng chạy. Config đã ghi ở mục 5, nhưng theo quyết định "không thêm thí nghiệm"
    thì bọn em không chạy. Paper không khẳng định gì cần tới Run D.

14. **"Hồi trước nói train mạnh làm model 'không viết xong', giờ lại nói ngược?"** Đúng, bản trước đọc sai. Phép đo
    ký tự gắn cờ text trôi dạt, nhưng số generation chạm trần token gần như không đổi ở lr thấp, và chỉ tăng 2–14 điểm
    ở 5e-4. Phần lớn mức giảm là model làm sai nhiều hơn trên chính những lời giải viết xong.
    **(Đợt 3 sửa câu cuối:** "phần lớn" chỉ đúng cho 4/6 run ở 5e-4. Tách 3 phần thì phần "finished" là 34–74% tùy run;
    ở B seed 2 và no-filter seed 2 thì phần termination lớn hơn (61%, 66%). Xem mục 8.)

---

## 8. Đợt sửa thứ ba (2026-10-21): sửa theo review `/openaireview` của `paper_revised.pdf`

Nguồn issue: `~/Documents/GitHub/paper-review-tools/review_results/paper-revised_review/final_issues.json`
(47 issue). Đánh giá chung của review: các con số phần lớn tái lập được; vấn đề là **câu tiêu đề nói mạnh hơn data**
(i) "No run improves" dựa trên non-significance mà không có biên tương đương; (ii) nhánh "học viết theo verifier"
được trình bày như đã bác bỏ, trong khi luật đặt trước **không thể bật** khi accuracy giảm; (iii) tỉ lệ termination
được mô tả ba kiểu mâu thuẫn nhau. Đợt này **không chạy thí nghiệm mới**: mọi số mới đều tính lại trên CPU từ
`results/viec3`. `paper.tex`/`paper.pdf` không đụng tới.

Bản trước đợt 3 (để so diff): `paper_revised.before-dot3.tex` trong scratchpad của session (tạm thời). Có thể
khôi phục từ git nếu Bi commit trước khi so.

### 8.0 Script dùng ở đợt này (`experiments/viec3/review_cpu/dot3/`)

| Script | Tính gì | Chạy |
|---|---|---|
| `decomp.py` | tách Δsacc thành 3 phần đối xứng: finished = s̄·Δf, cap-share = Δs·(f̄−c̄), cap-acc = (1−s̄)·Δc | `.venv/bin/python decomp.py` |
| `extra.py` | tỉ lệ `\boxed` (tất cả / finished / pool), proxy ∩ cap-hit, độ nhạy ngưỡng 500/512, selection vs exam sacc, số đề bị loại khỏi matched metric | `.venv/bin/python extra.py [run...]` |
| `rescored_ci.py` | bootstrap CI cho các run chấm lại sau khi sửa lỗi gold-storage (`review_cpu/patched/*.json`, trường `boxed`) | `.venv/bin/python rescored_ci.py` |
| `gold_audit.py` | trong các câu verifier loại ở run train-on-gold, đếm câu có `\boxed{}` trùng gold (so chuỗi sau chuẩn hóa nhẹ) | `.venv/bin/python gold_audit.py` |

Cả bốn đọc `review_cpu/scored/` và `review_cpu/tokcache/` (token count đã re-tokenize sẵn). Không cần tokenizer của Qwen.

Tra cứu trực tiếp (theo CLAUDE.md của repo):
- `generation_config.json` của Qwen2.5-1.5B-Instruct trên HF: `top_p 0.8`, `top_k 20`, `repetition_penalty 1.1`
  (temperature 0.7 bị code mình ghi đè thành 0.8).
- Huang et al., arXiv 2505.22203: "average recall rate of only 86%"; Bảng 5: HF Math-Verify recall trên Math = 0.95
  (output của DeepSeek-R1-Distill-Qwen-32B).
- ReST, arXiv 2308.08998: dịch máy, reward model học từ preference của người, ngưỡng tăng dần.

### 8.1 Khung bài: title, abstract, intro, contributions

| Chỗ | Cũ | Mới | Bằng chứng | Lý do |
|---|---|---|---|---|
| Title | (khẳng định không self-improve) | "No **Detectable** Self-Improvement from Generate–Verify–Train Iterations: A Negative Result with Qwen2.5-1.5B, LoRA SFT and a Rule-Based Verifier" | — | Không có test tương đương, chỉ nói được "không phát hiện được" |
| Abstract | "no run improves"; hai nhánh đều "no" | nhánh 1: CI của sacc loại trừ mức tăng > 2.2 điểm (không phải test tương đương); nhánh 2: "not established either way"; các phép đo post hoc được gắn nhãn | `results/viec3/ci/ci.json` (cận trên lớn nhất của Δsacc) | Luật đọc nhánh 2 cần pass@1 tăng, nên im lặng ≠ bằng chứng |
| Abstract | scope chung chung | "MATH-500 ở 4 lr (2–3 seed mỗi lr); GSM8K ở 2 lr (1 seed mỗi lr)" | manifest các run | Người đọc cần biết mỗi kết luận dựa trên bao nhiêu seed |
| Abstract | "16–19%" FN | "15.5–18.6%", "one in six" | `review_cpu/patched/` | Số chính xác |
| Abstract/Contrib. | "finished accuracy giải thích phần lớn" | finished acc giảm 5–11 điểm (matched); phần finished = 34–74% mức giảm tùy run; ở lr thấp cap-hit đổi ≤ ~1 điểm | `decomp.py` | Ba chỗ cũ mô tả tỉ lệ termination theo ba cách khác nhau |
| Intro | luật đọc trình bày như hai chiều | ghi rõ luật **một chiều** (chỉ bật được khi accuracy tăng); câu trả lời "âm tính ở nhánh 1, còn mở ở nhánh 2" | — | Issue major của review |

### 8.2 Related work và verifier

| Chỗ | Cũ | Mới | Bằng chứng | Lý do |
|---|---|---|---|---|
| ReST | mô tả sai domain | "lọc sample dịch máy bằng reward model học được, ngưỡng tăng dần" | arXiv 2308.08998 | Sai sự thật |
| Huang et al. | so FN của mình với "14%" | recall trung bình 86% (~14% FN) nhưng **math-verify** trên subset MATH của họ có recall 0.95 (~5% FN), trên output của model 32B; chỉ so được bậc độ lớn | 2505.22203 Bảng 5 | Con số 14% là trung bình nhiều verifier, không phải math-verify |
| Egashira | no-filter như kiểm tra phát hiện của họ | no-filter **không** phải test cho phát hiện FP của họ | — | Khác thiết kế |
| Xu et al. | số đề gained/lost như bằng chứng thêm | added − lost = 150 × Δpass@k, chỉ là viết lại | đại số | Không phải bằng chứng độc lập |
| Audit FN | 0/… | Wilson 0–1.9%, cận một phía 1.3%; ghi hai bias làm ước lượng 7.8% **thấp** (oracle so chuỗi, loại 24 đề) | `ci.md` dòng "FN GSM8K audit" | Thiếu khoảng tin cậy và hướng bias |
| Đoạn mới "Unparseable gold" | (không có) | 51/500 gold không parse được (10.2%); 11–18 mỗi exam partition; luôn tính là chưa giải, triệt tiêu khi so trong cùng run | `VerifyResult.gold_parsed_empty` | Người đọc cần biết trần accuracy |
| Gold-storage (post hoc) | chỉ có offset | Δsacc sau chấm lại kèm CI: A 5e-4 s1 −10.7 [−14.8, −6.7], s2 −6.0 [−9.7, −2.2] (gốc −8.3/−4.7); A 1e-5 s0 −3.3 [−5.9, −0.7] (gốc −2.4); gold −24.7, −22.0; pass@1 s2 [−14.0, +2.0]; "chỉ 5 run được chấm lại" | `rescored_ci.py` | Lỗi lớn nhất ở vòng 0 nên verifier gốc, nếu có, **đánh giá thấp** mức giảm. (Bản nháp đợt 3 từng viết ngược lại, đã sửa) |

### 8.3 Setup và uncertainty

| Chỗ | Mới | Bằng chứng |
|---|---|---|
| Config | decoding top-p 0.8, top-k 20, rep. penalty 1.1 (từ generation config); transformers 5.0.0, peft 0.19.1, TRL 1.10.0; LoRA dropout và weight decay để default; định nghĩa "solved"; sacc là thước đo chính; verifier chọn data cũng là verifier chấm | HF generation_config, `src/dacntt/gvt/train.py` |
| A/B seed 2 | pool vòng 0 giống hệt (424 mỗi bên); patch đổi cách chấm < 1% generation; pool sau đó 386 vs 398, 350 vs 332 | manifest |
| Multiplicity (mới) | 76 khoảng tin cậy, ~4 cái sẽ loại trừ 0 do ngẫu nhiên | đếm trong Bảng CI |

### 8.4 Results

| Chỗ | Cũ | Mới | Bằng chứng | Lý do |
|---|---|---|---|---|
| Design P | số tính lúc chạy, không ghi | "as computed during the run" + ghi chú tính lại; caption Bảng 3: pass@8 vòng 3 tính lại 63.5% (reward) / 63.6% (default) | tính lại từ generations | Nhất quán |
| Design P | không có | selection-set vs exam: sacc selection −8.2/−5.3 vs exam −8.3/−4.7 ở 5e-4; ở 1e-4 s1 −6.2 vs −1.5 | `extra.py` | Kiểm tra "chấm trên selection set có phóng đại không" |
| Design P | giải thích bằng dose | dose là giải thích dựa trên 2 giả định chưa kiểm; Run C là comparator duy nhất | — | Nói quá |
| §4.2 tiêu đề | (không giảm) | "Small Declines, a Larger One on GSM8K"; matched −1.1 đến −4.2 ở 1e-5, loại trừ 0 ở seed 0 cho A và B | `ci.json` | Bản cũ nói "không đổi" trong khi CI loại trừ 0 |
| Run C 1e-5 | | "9.3 trong vòng cuối"; pass@8 −2.7 CI chứa 0; decomposition 97% finished | `decomp.py` | |
| Bỏ so sánh với pooled | "bằng cỡ pooled decline" | bỏ (ở §4.2, caption hình, đoạn controls) | — | Hai thiết kế khác dose, partition, n; không so được |
| Bảng anatomy | thiếu A 1e-5 s0 | thêm dòng `A, 1e-5, 0: 1158→1147, 46.9→47.4, 54.8→51.0, −3.8` | `capanat.py` | |
| Bảng 4 | B s1 pass@8 Δ −0.6 | −0.7 | `ci.json` | Làm tròn sai |
| §4.5 lr | "trung bình theo seed: 2.0 / 3.7 / 6.5", −8.4, −4.6, −3.6 | so **cùng seed**: seed 1 −1.5/−3.5/−8.3 (đơn điệu), seed 2 −3.7/−3.8/−4.7 (gần như phẳng); seed 3 chỉ có ở 1e-4 (−1.0); "gợi ý, chưa chứng minh" | `ci.json` | Trung bình trộn seed 3 vào một mức lr → không so được; số làm tròn sai |
| §4.5 boxed | không có | pool 89–91% boxed ở vòng 0, 73–77% vòng 2; generation 50–52%; trong các generation finished boxed giảm 95.6→69.7 (A s1), 98.5→82.9 (A s2) | `extra.py` | Bằng chứng post hoc cho nhánh 2 |
| Patch 5e-4 | "pool gần như không đổi" | pool vòng 0 gần như giống; pool sau đó lệch 1–18 ví dụ khi quỹ đạo tách ra | manifest | Chính xác hơn |
| Controls: no-filter | "makes no consistent difference" | "no effect of consistent sign"; seed 2 sacc −5.5 [−9.2, −1.8] **loại trừ 0, nghiêng về giữ filter**; seed 1 quanh 0 | `ci.json` | Câu cũ che mất một CI loại trừ 0 |
| Controls: train-on-gold | "chưa audit, nghĩ là không giải thích được phần lớn" | audit chuỗi: câu bị loại mà boxed = gold là 14/600 (s1), 11/600 (s2), ≈ +2 điểm nếu tính đúng; chấm lại gold-storage vẫn −24.7/−22.0 | `gold_audit.py`, `rescored_ci.py` | Bản cũ thừa nhận chưa kiểm; giờ kiểm được một phần trên CPU |
| Controls | "No verifier-filtered run shows a pass@k gain" | "... **at this rate**" | 1e-4 seed 3 pass@4 +1.3 | Câu cũ sai với 1e-4 s3 |
| Run C 5e-4 | "mainly not a termination effect" | khoảng một nửa (51% finished / 49% termination), một run duy nhất | `decomp.py` | Câu cũ sai với chính decomposition |

### 8.5 §4.6 Anatomy (phần bị review nặng nhất)

| Chỗ | Mới | Bằng chứng |
|---|---|---|
| Mở đầu | Toàn bộ mục là **post hoc**; mô tả, không xác định nguyên nhân | — |
| Ngưỡng 508 | 22–37/600 generation nằm ở 480–507 token; ngưỡng 500 tăng tỉ lệ ≤ ~1.6 điểm, 512 giảm ≤ ~4.7; với cả hai, tỉ lệ vẫn chỉ tăng ở 5e-4 | `extra.py` |
| Proxy | Mọi generation bị proxy gắn cờ đều là cap-hit, nhưng proxy chỉ bắt 19–25% cap-hit ở vòng 0 và 65–75% ở vòng 2 (5e-4). Ở 1e-4/2e-4 proxy tăng 2.0–2.9× (seed 1: 9.8→19.5 ở 1e-4, 9.8→25.0 ở 2e-4) trong khi cap-hit phẳng/giảm | `extra.py` |
| Matched metric | định nghĩa đủ: loại đề không có sample finished ở vòng cuối (22–45/150); fallback về mọi sample vòng 0 nếu vòng 0 không có sample finished (6–21 đề; 34–37 ở run gold); 2,000 bootstrap; ghi rõ nó **điều kiện trên một kết quả của training** nên chỉ là mô tả | `extra.py` |
| Decomposition | công thức 3 phần ghi trong bài; theo từng run: finished 73% (A s1), 62% (B s1), 74% (NF s1), 59% (A s2), 39% (B s2), 34% (NF s2). Termination 26–41% ở 4 run, là phần **lớn hơn** ở B s2 (61%) và NF s2 (66%). Ở 1e-4/2e-4 phần finished > 100% vì cap-hit giảm | `decomp.py` |
| Câu kết | "not as its main part" → "chỉ ở lr cao nhất, tỉ lệ từ khoảng 1/4 đến 2/3 tùy run" | như trên |
| Gold | "shorten by about 59%" → "55–59%" (1175→485 = −58.7%; 1154→516 = −55.3%); thêm: sụp đổ có thể một phần do recipe (loss tính cả prompt; lời giải gốc ngắn), chưa thử loss chỉ trên response | Bảng anatomy; `train.py` (1 epoch) |
| Truncation check | thêm: chênh giữa 3 arm nằm trong độ dao động giữa các replicate cùng config; giới hạn 1024 không bỏ hết ví dụ không có EOS: 43/440 (9.8%) ví dụ được nhận ở vòng 0 là cap-hit, không có EOS ở bất kỳ giới hạn nào | `extra.py` (pool caphit) |
| Re-score 1536 | "shows" → "consistent with ... does not establish"; một adapter mỗi dòng, không có CI; chấm lại cùng adapter đã lệch tới 6.7 điểm pass@1 nên chênh 1–3 điểm giữa các dòng không đọc được | caption Bảng reeval |

### 8.6 Discussion, Limitations, Conclusion

| Chỗ | Cũ | Mới | Lý do |
|---|---|---|---|
| §5.1 nhánh 1 | "Not detectably" | thêm cận 2.2 điểm (không phải test tương đương); gained/lost chỉ viết lại dấu của Δpass@k; churn "about 5 to 18" thay "about ten" | Số đo thật: 5–18 mỗi chuyển vòng (1e-5: 5–8.5) |
| §5.1 nhánh 2 | "We see no sign of it" | "The data cannot settle this": luật một chiều; bằng chứng post hoc pool vs generation boxed; caveat lỗi gold-storage phạt một số câu boxed nhưng pool vẫn chủ yếu boxed | Issue major |
| §5.1 "What changes" | "on both datasets and at every rate above 1e-5"; "minority to at most two thirds" | CI matched loại trừ 0 ở 5/6 run MATH-500 5e-4, cả hai run GSM8K, và MATH-500 1e-5 cho A, B seed 0; ở 1e-4/2e-4 điểm ước lượng âm nhưng CI chứa 0; termination 26–41% ở 4 run, 61–66% ở 2 run | Câu cũ sai: 1e-4/2e-4 CI chứa 0, còn 1e-5 lại loại trừ 0 |
| §5.2 shrinking pool | "The data do not support it" | "no support, but do not rule it out": patch kiểm **độ nặng** của bias hiếm, không kiểm bias phổ biến có tích lũy không; no-filter lẫn dose (3–4×); giải thích bằng dose cũng chưa kiểm trực tiếp | Lập luận cũ dùng hai control không đủ sức |
| Limitations (5 mục mới) | — | verifier chọn data cũng chấm; trần 512 token đang ràng buộc (43% base đã chạm, ~1/4 pool bị cắt); không có biên tương đương + 76 CI không hiệu chỉnh; có thể nhiễm test set (MATH/GSM8K công khai), chưa kiểm; recipe (loss cả prompt, một cấu hình LoRA r16 q/v) | Review chỉ ra thiếu |
| Conclusion | "answer is neither"; "problems lost match or outnumber"; "through shorter answers"; "made no detectable difference" | nhánh 1 "no" với cận 2.2; nhánh 2 "stays open"; termination 1/4–2/3 tùy run; "with much shorter answers"; patch/no-filter "no difference of consistent sign (dấu đổi giữa seed, CI một seed đôi khi loại trừ 0)"; bỏ câu lost/gained | Đồng bộ với thân bài |
| Future work | "17–23% of the kept pool" | thêm mẫu số: so với kích thước pool vòng 0 (440→542; 872→1,066) | `dose.py` |
| §4.4 diversity | "Over all 500 problems" | ghi rõ là trên 500 đề selection + exam (Design I), không phải chỉ exam; độ đo distinct-answer chỉ tính cho một run (A 1e-5 s0) | Issue minor #38 |

### 8.7 Chưa giải quyết được (cần ghi nhận khi bị hỏi)

1. **Không có biên tương đương đặt trước.** Cận 2.2 điểm đọc ra từ CI sau khi chạy. Không sửa được nếu không chạy lại
   với margin đăng ký trước.
2. **Multiplicity.** 76 CI, không hiệu chỉnh. Bài chỉ cảnh báo, không áp Bonferroni/Holm.
3. **Một seed** cho Run C ở 5e-4, cho truncation check (mỗi arm một run) và cho re-score 1536 (một adapter mỗi dòng).
4. **Nhiễm test set** chưa kiểm.
5. **Loss chỉ trên response** chưa thử; có thể ảnh hưởng tới run train-on-gold.
6. Audit string của train-on-gold chỉ là **cận dưới** của FN (chỉ bắt câu trùng chuỗi), không phải audit tay.
7. Run D (patch gold-storage) vẫn không chạy, theo quyết định "không thêm thí nghiệm".

### 8.8 Biên dịch

`tectonic -X compile paper_revised.tex` → `papers/latex/paper_revised.pdf`, **25 trang** (ghi "21" trước đây là sai; bản commit `8902360` cũng 25 trang). Không có overfull box,
không có reference undefined; chỉ còn các underfull vbox ở trang float (vô hại).

### 8.9 Câu giáo sư có thể hỏi thêm (đợt 3)

15. **"Không có hiệu ứng" hay "không phát hiện được hiệu ứng"?** Không phát hiện được. CI của sample accuracy loại
    trừ mức tăng lớn hơn khoảng 2.2 điểm, nhưng bọn em không đặt trước margin tương đương, nên đó không phải test
    tương đương.

16. **"Vậy model có học viết theo verifier không?"** Bọn em không trả lời được. Luật đặt trước cần pass@1 tăng mới
    bật, mà pass@1 không bao giờ tăng. Bằng chứng post hoc: pool train 90% có `\boxed`, nhưng tỉ lệ `\boxed` trong
    output lại giảm (95.6→69.7% trên các lời giải viết xong). Điều đó không giống học theo verifier, nhưng không loại
    trừ được.

17. **"Mức giảm do làm sai hay do viết không xong?"** Tùy run. Ở 5e-4, phần "làm sai trên lời giải viết xong" là
    34–74%; ở hai run seed 2 (B, no-filter) phần "không viết xong" lớn hơn. Ở lr thấp hơn thì toàn bộ là phần làm sai,
    nhưng CI chứa 0.

18. **"Train-on-gold giảm 20 điểm, có phải do verifier chấm sai format mới không?"** Bọn em kiểm hai cách trên CPU:
    câu bị loại mà `\boxed{}` trùng gold chỉ 14/600 và 11/600 (~2 điểm); chấm lại với bản sửa gold-storage thì vẫn
    giảm 24.7 và 22.0 điểm. Cả hai đều nhỏ hơn rất nhiều so với mức giảm, dù không phải audit tay.

> **Sửa Q16 (đợt 4):** câu trả lời trên ("không giống học theo verifier") sai hướng. Pool 89–91% `\boxed` nhưng
> các lời giải *viết xong* ở vòng 0 còn boxed hơn (95.6/98.5%), rồi giảm xuống 69.7/82.9% trong khi pool cũng giảm
> (73–77% ở vòng 2). Tức là giảm *về phía* pool — học theo pool hay trôi đều cho ra như vậy. Trả lời đúng: "tỉ lệ
> `\boxed` không phân biệt được hai giả thuyết". Ngoài ra pass@1 có tăng một lần (+0.7 ở 1e-4 seed 1, CI chứa 0),
> nên nói "không bao giờ tăng *có ý nghĩa*".
>
> **Sửa Q17 (đợt 4):** "ở lr thấp hơn thì toàn bộ là phần làm sai" không chính xác. Ở 1e-4/2e-4 phần finished là
> 93–169% của mức giảm (4/5 run vượt 100%, run 1e-4 seed 2 là 93%). Ở 1e-5 seed 1, termination chiếm 63% của mức giảm
> 1.4 điểm, nhưng mức giảm này nằm trong nhiễu. Ngay cả ở 5e-4, replicate và msl1024 không tăng cap-hit (phần
> finished 89%/85%).

## 9. Đợt sửa thứ tư (2026-10-21): sửa theo re-review `/openaireview` của bản round 3

Review: `~/Documents/GitHub/paper-review-tools/review_results/paper-revised-r3_review/` (52 issue: 6 major, 27
moderate, 19 minor; trạng thái 47 issue cũ ở `comments/prior_issue_status.md`: 35 resolved, 11 partial, 1 unresolved).
Đợt này chỉ sửa **6 major + các lỗi số rõ ràng**; các moderate/minor còn lại để Bi xem và quyết.

### 9.0 Số liệu kiểm lại trước khi sửa (CPU, chỉ đọc)

| Script | Kết quả dùng |
|---|---|
| `dot3/rescored_ci.py` | train-on-gold seed 2 re-score: **38.0→13.3** (không phải 40.0) — cùng partition với Run A seed 2 |
| `dot3/extra.py` | proxy&cap/proxy vòng 2 = 80–98% (vòng 0 = 100%); tỉ số proxy ở 1e-4/2e-4 = 1.99–2.55×; ngưỡng ≥512 giảm tối đa **4.0** (B seed 2, 54.0→50.0); ≥500 tăng tối đa 1.6 |
| `dot3/decomp.py` (chạy bằng `.venv/bin/python`) | 1e-4 seed 2: phần finished = **93%** (không "vượt toàn bộ"); replicate 5e-4 s1: cap 43.2→43.0, finished 89%; msl1024: 43.8, 85%; 1e-5 s1: termination 63% của mức giảm 1.4 |
| `results/viec3/ci/ci.md` | replicate − A (5e-4 s1) sample acc **+3.2**; cận trên lớn nhất pass@1 **+8.0** (1e-4 s1), pass@k **+7.3** (1e-4 s3); C 1e-5: −12.7 pass@1 tới vòng 4, −13.1 sample acc |

### 9.1 Sáu lỗi major

| # | Lỗi | Sửa ở đâu | Sửa thành |
|---|---|---|---|
| M1 | Abstract "at lower rates the cap-hit share moves by at most about one point" — sai (2e-4: −2.4/−3.3; 1e-4 s3: −2.5). Do mình viết ở đợt 3 | Abstract, contributions, §5.1 | "does not rise (changes of −3.3 to +1.1 points)"; thêm "2–14 points in six runs (not in a replicate)" |
| M2 | "Stronger training lowers accuracy" nói như sự thật, trong khi §4.5 tự gọi là "suggestive, not established" | Abstract, intro, contributions, §4.1, §4.5 (controls), §4.6 tiêu đề đoạn, §5.1, Conclusion | "Accuracy falls in every run at the highest rate; that the decline grows with the rate rests on one seed"; "most clearly at the highest rate"; §4.1 "suggests, on the evidence of one seed"; bỏ chữ ký "pass@1 falls faster than pass@k" (chỉ đúng 2/4 run ở 5e-4) |
| M3 | Cận 2.2 điểm dùng CI không tính seed variance, và hedge mất dần từ abstract → contributions → conclusion | Abstract, contributions, §5.1, Conclusion | Mọi chỗ nhắc 2.2 đều kèm: CI bỏ seed variance (replicate lệch 3.2 điểm), không phải equivalence test → "loose bound" |
| M4 | Lập luận `\boxed` so pool với *toàn bộ* generation; so với generation viết xong thì giảm về phía pool → "runs against the training data" không đứng | §4.5 (đoạn 5e-4), §5.1, contributions, abstract, Conclusion | "The style shift does not separate imitation from drift"; bỏ "does not converge on the form it is trained on", bỏ "verifier's preferred \boxed form" |
| M5 | Cận 2.2 dựa trên sample accuracy — không nằm trong 4 measure đặt trước, được chọn làm primary sau khi chạy | §3.4, abstract, §5.1, contributions, Conclusion | §3.4 nói rõ "after the runs we chose it… post hoc in the choice of measure"; báo kèm cận trên của pass@1/pass@k đặt trước (+8.0/+7.3) |
| M6 | Mức giảm ở 1e-5 dựa trên CI vừa sát 0 từ A/B seed 0 (gần như một replicate) | §4.2, §5.1 | "possible small decline at this rate, not an established one"; nêu cận trên (−0.6, 0.0; −0.5, −0.9), A/B seed 0 gần một replicate, seed 1 không CI nào loại 0, ~4/76 CI loại 0 do ngẫu nhiên |

### 9.2 Lỗi số

| Chỗ | Cũ | Mới | Nguồn |
|---|---|---|---|
| §3.2 re-score train-on-gold seed 2 | "from 40.0% to 16.0% and 13.3%" | "…and from 38.0% to 13.3%" | `rescored_ci.py` |
| §4.5 B seed 1 Δpass@1 | 4.6 | 4.7 | 50/150→43/150; Table 7 |
| §4.5 Run C 1e-5 vòng 2 | −1.4 | −1.3 (thêm: −12.7 tới vòng 4) | ci.json 100→98/150 |
| §4.5 boxed của generation vòng 0 | 50–52% | 52–54% (Table 5) | Table 5 |
| §4.5 gate retention | 31% | 30–31% | 440/1400, 424/1400 |
| §4.6 ngưỡng 512 | "at most about 4.7" | 4.0 | `extra.py` |
| §4.6 proxy | "Every proxy-flagged generation is a cap-hit"; 2.0–2.9× | "At round 0 every…(at round 2, 80–98% are)"; 2.0–2.6× | `extra.py` |
| §4.6 decomposition 1e-4/2e-4 | "finished part exceeds the whole change" | "in four of the five runs and is 93% in the fifth" | `decomp.py` |
| §4.6 | "Termination contributes only at the highest rate" | "contributes materially only at the highest rate… about a tenth to two thirds" + replicate/msl1024 + 1e-5 s1 63% | `decomp.py` |
| §5.1 churn | "about 5 to 18" | "about 2 to 20" | table.md (agent kiểm) |
| §5.1 | "pass@1 never rises" | "never rises detectably (largest +0.7 [−6.7, +8.0])" | Table 7 |
| Conclusion | "the sign flips between seeds" | "pass@1 flips sign between seeds; removing the filter lowers pass@4 at both seeds, within noise" | Table 8 / ci.md |
| §4.2 | "no evidence of compounding at this rate" | "…on MATH-500 at this rate (Run C… loses most of its pass@1 in its last round)" | Table 4 |
| §4.5 controls | "Since stronger training produces more decline, dose and data differ at once in both" | train-on-gold gần khớp step với Run A (175 vs 163–220) → chủ yếu khác data; no-filter 3–4× step | Table 8 |

### 9.3 Chưa sửa (moderate/minor còn lại trong `final_issues.json`)

Ví dụ đáng cân nhắc: decomposition không có CI; "termination" gồm cả phần cap-accuracy; B−A lẫn offset chấm điểm;
gold-storage suy rộng sang run không re-score; Table 10 (1536) chỉ về non-termination hơn là "what adapters write";
Xu et al./Egashira et al. mô tả thiếu; contamination không "affects all arms alike". Abstract giờ khá dài — Bi nên
cắt khi polish.

### 9.4 Biên dịch

`tectonic paper_revised.tex` → 25 trang, không lỗi.

### 9.5 Câu giáo sư có thể hỏi thêm (đợt 4)

19. **"Cận 2.2 điểm có tin được không?"** Chỉ là cận lỏng: (a) đọc từ CI sau khi chạy, không có margin đặt trước;
    (b) dùng sample accuracy, chọn làm primary sau khi chạy (trên pass@1/pass@k đặt trước, cận trên tới +8.0/+7.3);
    (c) CI không tính seed variance — một replicate cùng cấu hình đã lệch 3.2 điểm.

20. **"Lr cao hơn thì giảm nhiều hơn — chắc không?"** Không chắc. Seed 1 giảm đều (−1.5/−3.5/−8.3), seed 2 gần phẳng
    (−3.7/−3.8/−4.7). Chỉ chắc là ở 5e-4 mọi run đều giảm.

## 10. Đợt sửa thứ năm (2026-10-22): sửa nốt moderate/minor của re-review r3

Bi yêu cầu "phải làm paper hoàn thiện", nên đợt này sửa nốt các mục ở 9.3 và phần moderate/minor còn lại trong
`paper-revised-r3_review/final_issues.json`. Không chạy thí nghiệm mới, chỉ phân tích lại trên CPU từ log có sẵn.

### 10.0 Script mới (CPU, chỉ đọc) — `experiments/viec3/review_cpu/dot4/`

| Script | Làm gì | Kết quả dùng |
|---|---|---|
| `boot.py` | Bootstrap ghép cặp theo bài (2000 lần) cho ΔCap và 3 phần của decomposition (finished s̄Δf / cap-share Δs(f̄−c̄) / cap-accuracy (1−s̄)Δc) | ΔCap ở 5e-4: seed 1 +2.3 tới +4.7 (chỉ B loại 0: [0.2, 9.5]); seed 2 +8.2 tới +14.2 (đều loại 0). Phần cap-share chiếm 12–30% mức giảm ở seed 1, 52–72% ở seed 2. Replicate −0.2, msl1024 +0.7. Kết quả ở `boot.txt` |
| `unparsed.py` | Bọc 51 gold không parse được vào `\boxed{}` rồi chấm lại | 46/51 parse được và được chấp nhận → sửa gold-storage và loại gold-không-parse **chồng nhau**, không được cộng |
| `poolP.py` | Đếm pool từng vòng của Design P | 0.5B: 2533→2123; 1.5B: 3962→3730→3395→2638→1566 |

Kiểm tra trực tuyến (WebFetch trang arxiv.org/html): Egashira et al. (2608.20290) và Xu et al. (2605.02909), dùng để
sửa đoạn mô tả hai bài trong Related work.

### 10.1 Các thay đổi chính, theo mục

| Mục | Vấn đề review | Sửa thành | Bằng chứng |
|---|---|---|---|
| §4.6 decomposition | Không có CI; "termination" gộp cả phần cap-accuracy | Chỉ gọi phần **cap-share** là termination; thêm **bảng mới `tab:decomp`** gồm mọi run 5e-4, kèm CI; đoạn đọc: rõ ràng chỉ ở seed 2, ở seed 1 mức tăng cỡ chênh lệch do sampling (43.2 vs 40.7) | `boot.py` |
| Abstract, contributions, §5.1, Conclusion | "termination accounts for a quarter to two thirds" | "12–30% ở seed 1, 52–72% ở seed 2; cap-hit tăng rõ chỉ ở một seed, không có trong replicate"; phần finished lớn hơn ở 4/6 run | `boot.py` |
| Cả bài | Cap-hit của model chưa train ghi "43%" | "41–48%" (40.7–48.2 theo split của seed) | Table cap-hit |
| §3.2 | 7.8% "biased low"; quan hệ với tỉ lệ trong vòng lặp | Nêu rõ 7.8% ước lượng cái gì; chiều lệch so với tỉ lệ trong vòng lặp **chưa biết**; 8 ca "wrong token" phần lớn là đáp án ghép (trùng với lớp compound của probe) | audit cũ |
| §3.2 gold-storage | Pool tăng "17–23%"; tỉ lệ offset; suy rộng sang run không re-score | "Khoảng một phần năm" (440→542, 872→1066); offset 4.7–8.0 điểm chỉ ở 3 run self-training đã re-score, run khác là ngoại suy; tỉ số thay đổi gốc/re-score 0.73–0.78, nên cận 2.2 trên thang re-score gần 3 | `rescored_ci.py`, `unparsed.py` |
| Bảng mới `tab:inventory` (§3.3) | Không có chỗ nào liệt kê đủ các run | Bảng liệt kê mọi run có dữ liệu: rate, k, số vòng, seed, pool vòng 0; một seed cố định cùng lúc partition, tập selection và randomness lúc train | metrics.csv |
| §3.4 | B−A được dùng làm ví dụ seed variance; số CI | Ví dụ chính là replicate (3.2 điểm); "một CI loại 0 chưa đủ, một CI chứa 0 không loại được hiệu ứng"; Table 8 có 76 CI cộng khoảng 10 CI trong text, không độc lập; nói rõ các measure post hoc dùng bản re-score riêng (`review_cpu/scored/`) | ci.md |
| §4.1 | Giải thích Design P bằng dose | Thêm đoạn: mức giảm lớn nhất (−12.1, −13.8) đến từ pool **nhỏ nhất** (3395, 2638); model 0.5B có 2533 mẫu (≈2.9× Run A) nhưng giảm ít → dose không giải thích hết | `poolP.py` |
| §4.2, §4.3 | "Little change at 1e-5" nói chung chung | Chỉ đúng cho các run MATH-500 ở 420–436 step; là tính chất của rate × số step. Offset chấm điểm của B (vòng 0 seed 1 +0.6) | Table 5 |
| §4.5 | No-filter / train-on-gold diễn giải quá mức | No-filter "chưa bao giờ tốt hơn… kém hơn về pass@4 ở cả hai seed, nhưng không quy được cho filter"; check 1 của train-on-gold là cận dưới, check 2 làm mức giảm lớn hơn (−24.7/−22.0) nhưng đo một defect khác | ci.md |
| §5.1 | Phần "style" | Tỉ lệ boxed đặt trước đã được đánh giá và **không đạt**: không hội tụ mà giảm (52→36, 54→37) | Table 5 |
| Related work | Mô tả Xu, Egashira thiếu và sai | Egashira: Qwen2.5-1.5B-Instruct ở appendix, định nghĩa FP, plateau của domain luôn bị reject (liên quan gold không parse); Xu: filter là answer match / majority vote, có nhánh distillation làm positive control, F3 truncation 16.5→65.3% | WebFetch |
| Limitation 3 (#46) | Liệt kê thiếu điều kiện chỉ có một seed | Liệt kê đủ: Run C ở cả hai rate, truncation check (một cặp replicate + một run msl1024), từng lần re-score theo token cap | inventory |
| Limitation 6 | "5–8 điểm cho mọi run" | 4.7–8.0 ở 3 run đã re-score, run khác là ngoại suy; nêu chồng lấn 46/51 với gold không parse | `unparsed.py` |
| Limitation 9, Future work | "43%" | "41–48%" | — |
| Limitation 10 | "76 intervals… about four by chance" | 76 trong Table 8 cộng khoảng 10 trong text, không độc lập, "about four" chỉ là ước chừng | — |
| Limitation 11 (#28) | Contamination "affects all arms alike" | Không nhất thiết: nếu self-training làm quên các bài đã thuộc, một phần mức giảm trong run có thể là mất phần đã thuộc chứ không phải mất kỹ năng | lập luận |
| Limitation 12 (#47) | Recipe | Không nhánh nào cải thiện rõ so với vòng 0, kể cả train-on-gold → không có positive reference cho thấy recipe này giúp được model 1.5B; mức giảm có thể một phần do recipe | Table 8 |
| Future work (#29) | Patch gold-storage: chưa nói cách khớp dose | Giữ dose cố định (subsample pool đã patch về cỡ pool cũ, hoặc cố định số step); cần nhiều seed mỗi nhánh | — |

### 10.2 Biên dịch

`tectonic paper_revised.tex` → **29 trang** (trước là 25, do thêm hai bảng `tab:inventory` và `tab:decomp` cùng các đoạn
giải thích), không có reference hay citation bị undefined.

### 10.3 Câu giáo sư có thể hỏi thêm (đợt 5)

21. **"Termination là gì, chiếm bao nhiêu?"** Mức giảm accuracy tách được thành 3 phần: (a) đúng ít hơn trên các bài
    viết xong, (b) **nhiều generation chạm cap hơn** (cap-share), (c) đúng ít hơn trên các generation chạm cap. Chỉ (b)
    là termination. Ở 5e-4 nó chiếm 12–30% ở seed 1 và 52–72% ở seed 2, và chỉ ở seed 2 thì cap-hit tăng rõ (CI loại 0).
    Bản trước gộp (b) với (c), nên nói "a quarter to two thirds".

22. **"Tại sao cận 2.2 lại thành khoảng 3?"** Defect gold-storage làm mọi thay đổi trên thang gốc chỉ còn khoảng
    0.73–0.78 lần thay đổi trên thang re-score. 2.2 / 0.75 ≈ 3. Vậy trên thang đúng thì cận còn lỏng hơn.

23. **"46/51 gold là sao?"** Có 51 gold không parse được, đã bị loại khỏi audit. Bọc chúng vào `\boxed{}` thì 46 cái
    parse được và được chấp nhận. Tức là phần lớn chúng **cùng một lỗi** với defect gold-storage, nên hai mức sửa
    không được cộng dồn.

24. **"Design P giảm mạnh có phải do train nhiều step hơn không?"** Không hẳn. Mức giảm tăng tốc đúng lúc pool **nhỏ
    đi** (3395, 2638 mẫu), và model 0.5B có pool gấp khoảng 2.9 lần Run A nhưng giảm ít. Nên dose không giải thích hết,
    và nguyên nhân vẫn để ngỏ.

25. **"Có nhánh nào làm model tốt lên không?"** Không, kể cả train trên lời giải tham chiếu. Vì vậy không loại được
    khả năng chính recipe (loss tính cả prompt, LoRA r16 q/v) đã gây hại. Cái này nằm ở Limitation 12.

## Soát số lần 3 (2026-10-24)

Soát từng con số trong `papers/latex/paper_revised.tex` với dữ liệu thô (không chạy thí nghiệm mới, không đổi lập luận).
Chỉ sửa chỗ sai số hoặc hai phần mâu thuẫn nhau, sửa ít nhất có thể. `paper.tex`/`paper.pdf` không động tới.
Biên dịch lại bằng `tectonic paper_revised.tex`: 29 trang, không có tham chiếu nào chưa định nghĩa.

| # | Chỗ | Cũ → Mới | Bằng chứng |
|---|-----|----------|------------|
| 1 | Bảng `tab:decomp`, dòng "B, 1", cột Δcap-hit | `+4.6` → `+4.7` (chưa làm tròn: 43.17→47.83) | `experiments/viec3/review_cpu/dot4/boot.txt` dòng `b-math500-lr-fixed` |
| 2 | §4.6, độ nhạy ngưỡng 500 | "at most about 1.6 points" → "about 2 points" (lớn nhất 2.0 ở 1e-4 seed 1 và 2, vòng 2: 44.7 với 42.7, 44.8 với 42.8) | chạy lại `experiments/viec3/review_cpu/dot3/extra.py` |
| 3 | §4.6, số mẫu gần ngưỡng | "22–37 of 600 ... have 480–507 tokens" → "at most 37 of 600" (msl1024 chỉ có 15–18, gold chỉ có 1–11) | `extra.py` / `capanat.py` (scratch `anat_check.py`) |
| 4 | §4.6, proxy bắt cap-hit ở vòng 2 tại 5e-4 | "65–75%" → "58–75%" (replicate `a-lr5e4-keep` là 58%) | `capanat.py` trên `a-lr5e4-keep` |
| 5 | §4.1, selection-set và exam | "falls as much as or more ... not checked at 10^-5" → giới hạn câu này cho Run A ở hai learning rate cao hơn; thêm số ở 1e-5: A −1.0/−1.1 trên selection, −2.4/−1.4 trên exam; Run C 5e-4 −11.3 với −15.4; Run C 1e-5 −13.8 với −13.0 | `experiments/viec3/review_cpu/analysis.md` §9 |
| 6 | §4.4, tỉ lệ đáp án khác nhau | "0.542→0.554 for Run A, seed 0, the only run for which we computed it" → gần như đứng yên ở các run MATH-500 (thêm B seed 1: 0.528→0.543), nhưng tăng ở Run C (0.359→0.500) và Design P (0.443→0.712) | `results/viec3/mechanism-ABC.md`, `results/viec3/mechanism.md` |
| 7 | Contributions | "a second, untested defect ... affects about one in six" → "measured post hoc but never varied in a training run, rejects about one in six (15.5–18.6%)". Đây là chỗ còn sót của câu chuyện cũ. | §3.2 cùng file; `REVIEW-VERIFIED.md` |
| 8 | §3.2, tỉ lệ lỗi gold trên tập selection | "where the share is slightly higher" → "about the same (17.8–18.8% at round 0)". So với cả 500 đề: 18.4/17.9/18.3% | dữ liệu `patched/`, scratch `fn.py` |
| 9 | §4.6, đoạn sau bảng `tab:reeval` | mức tăng sample accuracy "+6.9 ... +5.9" → "+6.8 ... +5.8". Tính từ số chưa làm tròn, giống cách tính các deficit −8.0/−8.8/… ngay sau đó | `results/viec3/base-reeval/reeval_0.json`, `a-lr5e4-keep/reeval_2.json` |

**Đã kiểm, khớp:**
- Các bảng isolated, lrcheck, lrseries, controls, passk, bydataset, `tab:ci` (với `results/viec3/ci/ci.md`), anatomy.
- Bảng `tab:reeval`, cả 8 dòng (với các file `reeval_*.json`). Mức dao động khi re-score là 2.7–6.7.
- Re-score gold-boxed, pool +22/23%, 51 gold không parse được, các số Design P.
- Steps, loss, phần trăm boxed, số dfrac, số mẫu dropped/fallback.
- Câu "manufactured" (dòng ~1336) đang phủ nhận claim cũ, giữ nguyên.
- "degenerate" chỉ còn dùng cho proxy ký tự, đã giải thích. Không còn "4.4%", "driver", hay "finished accuracy holds".

**Không kiểm được:**
- Giá trị matched của B ở 1e-5 (−4.2 [−7.8,−0.9] và −1.1 [−4.6,2.6]) và số ký tự/token (3.3; 4.9–5.0; 2.7–3.0). Máy không có tokenizer Qwen, và không có tokcache cho `qwen15b-math500-b`/`b-seed1`.
- Cận trên 18.6%. Dữ liệu `patched/` lưu được chỉ cho 15.5–18.4% trên 500 đề (A seed 1 R0 là 642/787). `REVIEW-VERIFIED.md` ghi 642/789 (18.6%), và tập exam lên tới 18.6%. Giữ nguyên, ghi lại để Bi xem.
- "about 2 to 20" (churn) và "35–50 times" là số xấp xỉ. Thực tế lost tối đa 25 ở NF seed 2; 102/3≈34, 194/4≈48.5. Không sửa.

**Đã sửa sau đó (2026-10-24, trước buổi báo cáo):**
- `15.5–18.6%` → `15.5–18.4%` ở cả 7 chỗ (abstract, contributions, §3.2 ×2, §4, discussion, conclusion). Tính lại từ `scored/` (verifier gốc) và `patched/` (bản vá boxed): A s1 18.4/16.9/15.7; A s2 17.9/17.9/15.5; A 1e-5 s0 18.3/17.9/17.5/16.7/16.8. Mẫu số chốt là cả 500 đề; 18.6% chỉ có ở tập exam nên không dùng. Ô `18.6%` trong bảng ở dòng ~556 là số khác, không đụng.
- "about 2 to 20" → "about 2 to 25".
- "roughly 35–50 times" → "roughly 34–49 times".
- PDF biên dịch lại bằng `tectonic`, vẫn 29 trang.

## Rút gọn 16 trang (2026-10-24, trước buổi báo cáo 25/10)

Mục tiêu: thân bài + tài liệu tham khảo ≤ 16 trang LNCS, phụ lục không giới hạn, không mất nội dung.
Kết quả: 29 → 33 trang tổng; thân bài + references = **12 trang** (references kết thúc trang 12, phụ lục
từ trang 13). Abstract 468 → ~240 từ.

Cách làm: thân bài viết lại dạng tóm tắt (giữ nguyên các label `sec:*` để ref cũ vẫn trỏ đúng);
**mọi đoạn và bảng gốc chép nguyên văn** xuống phụ lục sau bibliography. Trong bản chép, ref tới
`sec:verifier/pooled/isolated/control/lrcheck/anatomy/answer/limitations` đổi sang `app:*` tương ứng.

Bản đồ chuyển:
| Phụ lục | Nội dung gốc (dòng trong bản trước khi cắt) |
|---|---|
| A Related Work in Full | 163–258 (cả Positioning) |
| B The Verifier in Full | 280–383 |
| C Uncertainty in Full | 487–520 |
| D Design P in Full | tab:designs, 528–618 (tab:bydataset) |
| E Design I at 1e-5 in Full | 623–652, 689–718 |
| F Patch Control and Answer Diversity | 724–749, 754–769 |
| G Higher Learning Rates in Full | 774–858 (tab:lrcheck), 935–947, 973–1028 |
| H Anatomy in Full | 1033–1269 (tab:anatomy, tab:reeval) |
| I Discussion in Full | 1277–1395 (gồm Practical Suggestions) |
| J Limitations in Full | 1400–1472 |
| K Future Work | 1505–1524 |

Ở lại thân bài: tab:inventory, tab:passk, fig:isolated, tab:isolated, tab:lrseries, tab:ci,
tab:controls, tab:decomp; Conclusion giữ nguyên văn.

Kiểm tra: tập số trong .tex trước/sau giống hệt (491 số khác nhau, không số nào mất); không ref `??`;
không label trùng; 33 label cũ còn đủ, thêm 11 label `app:*`. Không chạy thêm thí nghiệm nào.

## Thêm đề xuất kiểm toán (2026-10-29)

Lý do: Bi yêu cầu paper "phải đề xuất một cái gì đó mới hơn" so với các bài khác. Không chạy thí nghiệm mới;
mọi số lấy từ phần chấm lại đã có ở phụ lục B và bảng phân rã (`tab:decomp`).

- **Mục mới §5.3 "A Proposed Audit for GVT with a Biased Verifier"** (`sec:audit`), bốn kiểm tra, ghi rõ post hoc:
  1. Kiểm định thích nghi verifier không phụ thuộc chiều của accuracy: $r_t$ = tỉ lệ lời giải được verifier đã sửa
     chấp nhận nhưng verifier gốc từ chối, trên chính mẫu của vòng lặp, theo từng vòng. Số: 15,5–18,4% ở mọi vòng
     của 3 run (phụ lục B, dòng "Over all 500 problems…"); tính theo pass@1 chấm lại là 17% (seed 1) và 20% (1e-5).
     Giới hạn ghi trong mục: 1 loại lỗi, 3 run, 3–5 vòng, không có khoảng tin cậy cho $r_t$.
  2. Phân rã độ giảm dưới cap token cố định (12–30% / 52–72%, `tab:decomp`).
  3. Kiểm tra liều của đối chứng trước khi chạy (patch đổi 0–4 ví dụ; lỗi gold-storage đổi 440→542).
  4. Ghép liều giữa thiết kế gộp và tách (khoảng 4,5×).
- **Contributions:** thêm gạch đầu dòng cho (1); viết lại gạch đầu dòng về learning rate cao thành "phân rã" (2).
- **Related Work (thân bài) và Positioning (phụ lục A):** thêm câu định vị. Câu so với TinyV/Huang được viết
  hẹp ("dùng tỉ lệ từ chối sai để sửa hoặc so verifier") vì abstract TinyV không nói rõ có theo dõi theo bước train
  hay không. Phantom Gains (arXiv 2608.20290) theo abstract: kiểm định từng bài so với null đo riêng, FDR.
- **§5.1, abstract, kết luận:** mỗi chỗ thêm một câu nhắc tới kiểm định (1).
- Biên dịch: 34 trang, thân bài + references hết trang 14 (≤ 16). Không có ref undefined. Một overfull ở bảng
  `tab:inventory` có từ trước (bản HEAD cũng có).
- `25-10-2026/paper_revised.pdf` giữ nguyên bản đã báo cáo 25/10.

Bi cần tự bảo vệ được: vì sao $r_t$ không giảm thì nói "không thích nghi". Trả lời: nếu model học viết theo cái
verifier chấp nhận, nó sẽ ít viết dạng bị lỗi này từ chối hơn, nên $r_t$ phải giảm. $r_t$ phẳng chỉ loại được
thích nghi mạnh với lỗi này, không loại được thích nghi yếu hay với lỗi khác.

## Xoay khung bài quanh "điểm tăng chưa phải học thật" (2026-10-29, đợt 2)

Lý do: Bi hỏi "đã có bài RL chính xác hơn thì bài mình đóng góp gì". Trả lời: bài không cạnh tranh độ chính xác;
bài hỏi điểm tăng có phải học thật không, và đề xuất phép kiểm §5.3 áp được cho cả SFT lẫn RL.

- **Abstract viết lại** (348 → khoảng 245 từ): mở bằng vấn đề (RL/self-training báo gain lớn, nhưng RL với reward
  ngẫu nhiên cũng tăng điểm), rồi phép kiểm, rồi kết quả. Bỏ khỏi abstract câu về thiết kế gộp (vẫn ở thân bài).
- **Mở đầu:** thêm đoạn thứ hai về RLVR ở cỡ 1.5B và *Spurious Rewards*; câu "open on the second" đổi thành
  "phép kiểm trả lời cho một loại lỗi".
- **Contributions:** phép kiểm lên đầu, thêm ý "chỉ cần generation của checkpoint + verifier đã sửa nên áp được cho RLVR".
- **Related Work:** đoạn mới "RL with verifiable rewards at small scale".
- **§5.3:** đoạn mới "Applying check (i) to RLVR"; ghi rõ **chưa chạy** trên checkpoint RL.
- **Kết luận:** thêm 2 câu đóng khung; bước tiếp là áp phép kiểm cho checkpoint RLVR công khai.
- **Trích dẫn mới (4), đã tra arXiv 29/10:** Shao et al. 2506.10947 (random reward +21,4 vs ground truth +29,1 trên
  Qwen2.5-Math-7B, MATH-500); Wang et al. 2504.20571, NeurIPS 2025 (Qwen2.5-Math-1.5B, 36,0% → 73,6%);
  Dang & Ngo 2503.16219 (R1-Distill-1.5B, AMC23 63% → 80%, khoảng 7.000 mẫu); Zeng et al. 2503.18892 (10 base
  model, gồm Qwen2.5 từ 0.5B).
- Build: 35 trang; thân bài + references kết thúc trước trang 16; không có ref undefined.

Bi cần tự bảo vệ được: "Sao không tự chạy phép kiểm trên RL?" → cần GPU để sinh lời giải từ checkpoint RL; quota
hết và đợt chạy vừa rồi đã chốt là cuối. Paper ghi rõ là chưa làm, coi là bước tiếp theo.

- **Tiêu đề đổi** (29/10): "No Detectable Self-Improvement from Generate–Verify–Train Iterations: A Negative
  Result with Qwen2.5-1.5B, LoRA SFT and a Rule-Based Verifier" → "Mathematics or the Verifier? A Direction-Free
  Test of Verifier Adaptation, Applied to Self-Training of Qwen2.5-1.5B". Tiêu đề chạy: "Mathematics or the Verifier?".
