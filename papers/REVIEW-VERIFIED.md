# Kiểm chứng 49 issue của review (final_issues.json) trên dữ liệu thô

Ngày: 2026-10-18. Người kiểm: evaluator agent. Nguồn issue:
`paper-review-tools/review_results/paper_review/final_issues.json` (0–8 major, 9–33 moderate, 34–48 minor).
Mọi con số dưới đây đều được tính lại bằng Python từ `results/viec3/<run>/{generations.jsonl, metrics.csv,
styles.csv, table.md, manifest.json, train_logs/round_*.json}` và `results/viec1|viec2/table.md`. Việc re-verify
dùng chính `MathVerifyAdapter("reward", normalize_frac_commands=<manifest.patch_verifier>)` của repo
(math-verify 0.9.0 trong `.venv`). Exam split tái tạo đúng như `run.py._split_train_test`: sort id,
`random.Random(seed).shuffle`, 150 đề đầu. Kết quả pass@1/pass@k tính lại **khớp đúng metrics.csv** ở mọi run và
mọi round (ví dụ A s1 33.3/50.0 → 32.7/49.3 → 23.3/42.7; C 5e-4 70.7/86.0 → 48.7/76.7). Bootstrap là paired
bootstrap theo đề trên 150 đề exam, 2000 lần lặp, 95% percentile CI.

Trích dẫn paper ứng với bản đã review. `paper.tex` đang được agent khác sửa song song, nên số dòng có thể đã lệch.

Ký hiệu run: A = `a-math500-lr-fixed` (seed 1), A s2 = `-seed2`, B = `b-math500-lr-fixed(-seed2)`,
NF = `nofilter-*`, GOLD = `gold-*`, 1e-5 = `qwen15b-math500-{a,b}(-seed1)`, `qwen15b-gsm8k-c`; C 5e-4 = `c-gsm8k-lr5e4`.

## Hai phát hiện mới từ CPU làm thay đổi bức tranh (đọc trước bảng)

**(F1) Proxy "degenerate" bỏ sót phần lớn generation bị cắt ở 512 token.** Mình re-tokenize từng generation bằng
tokenizer Qwen2.5-1.5B-Instruct. Ở round 0, 942/2000 generation của A s1 (toàn bộ 500 đề) có **đúng 512 token**,
tức là bị cắt giữa câu. Trên exam, tỉ lệ cap-hit (≥508 token) ở R0 là **43.2%**, trong khi proxy ">1500 ký tự và
không có \boxed" chỉ bắt được **9.8%**. Đo bằng tín hiệu trực tiếp này:

| run | cap-hit R0→R_last | finished (không cap-hit) acc R0→R_last | R0 reweight theo mix finished của R_last | Δ finished so với reweight [95% CI] |
|---|---|---|---|---|
| A s1 5e-4 | 43.2→46.2 | 54.0→43.0 | 52.2 | −9.1 [−14.2, −4.2] |
| A s2 5e-4 | 43.0→51.2 | 50.6→45.4 | 50.9 | −5.5 [−11.7, +0.1] |
| B s1 | 43.2→47.8 | 54.0→46.3 | 53.1 | −6.8 [−12.4, −1.0] |
| B s2 | 43.0→54.0 | 51.2→44.2 | 50.1 | −5.9 [−10.9, −1.0] |
| NF s1 | 43.2→45.5 | 54.0→43.1 | 53.7 | −10.6 [−16.4, −5.5] |
| NF s2 | 43.0→57.2 | 50.6→43.6 | 50.2 | −6.6 [−11.4, −2.0] |
| keep (replicate) 5e-4 | 43.2→43.0 | 54.0→45.9 | 50.9 | −5.0 [−9.7, −0.3] |
| msl1024 5e-4 | 43.2→43.8 | 54.0→45.4 | 51.1 | −5.7 [−11.2, −0.3] |
| 2e-4 s1 / s2 | 43.2→40.8 / 43.0→39.7 | 54.0→46.5 / 50.6→41.7 | 50.5 / 46.4 | −4.0 [−8.9, +0.5] / −4.7 [−10.1, +1.0] |
| 1e-4 s1 / s2 / s3 | 43.2→42.7 / 43.0→42.8 / 48.2→45.7 | 54.0→48.5 / 50.6→44.6 / 50.2→47.5 | 52.8 / 48.1 / 48.2 | −4.3 / −3.5 / −0.6 (CI đều chứa 0) |
| C 5e-4 (GSM8K) | 3.8→15.0 | 71.9→63.3 | 75.5 | −12.1 [−16.6, −7.9] |
| C 1e-5 (GSM8K, R4) | 3.5→4.2 | 73.4→60.3 | 73.1 | −12.8 [−16.5, −9.4] |
| A 1e-5 s0 / s1 (R4) | 46.9→47.4 / 40.7→41.8 | 54.8→51.0 / 55.2→54.3 | 54.8 / 56.6 | −3.8 [−7.2, −0.5] / −2.3 [−5.9, +1.2] |
| GOLD s1 / s2 | 43.2→7.2 / 43.0→8.3 | 54.0→14.7 / 50.6→12.5 | 40.4 / 38.5 | −25.6 / −25.9 |

Từ bảng này rút ra ba điều:
- Ở 1e-4 và 2e-4, tỉ lệ cap-hit **không tăng** (thậm chí giảm), trong khi proxy degenerate tăng 8.8→19.5–25.0%.
  Ở 5e-4, cap-hit chỉ tăng +2 đến +14 điểm, còn proxy tăng +26 đến +34 điểm.
- Phần lớn mức tăng của proxy là do text bị cắt **dài chữ hơn**: chars/token của nhóm degenerate là 3.3 ở R0 và 4.9–5.1
  ở R2, so với 2.8–3.0 ở nhóm còn lại. Không phải do bị cắt **thường xuyên hơn**.
- Shapley decomposition theo cap-hit cho thấy 35–74% mức giảm sample acc ở 5e-4 đến từ việc finished acc giảm:
  A s1 −6.1/−8.3, A s2 −2.8/−4.7, B s1 −4.2/−6.6, B s2 −3.6/−9.2, NF s1 −6.1/−8.2, NF s2 −3.5/−10.1.

Kết luận "decline chủ yếu là non-termination, finished acc giữ nguyên" của Section 4.6 / Contribution 4 / abstract
**không đứng được** khi đo bằng tín hiệu trực tiếp (liên quan issue 5, 6, 12, 29, 30, 47).
Script: `scratchpad/caphit.py`, `capanat.py`, `tokdist.py`.

**(F2) Lỗi gold-boxed (lớp của Run D) lớn hơn nhiều so với ước lượng 4.4% trong paper.** Mình re-verify mọi generation
với ba biến thể: frac (Run B), boxed (Run D) và both (`scratchpad/patch_dose.py`, `dose.py`).
- Patch boxed làm **thêm 102 / 92 mẫu vào kept pool ở R0** (A s1 / A s2), tức +23.2% / +21.7% kept pool và 7.3% /
  6.6% số generation trên selection set. Patch frac (Run B) chỉ thêm +2 / −1.
- Ở 1e-5 (A s0) patch boxed thêm +194 (+22.2%), còn patch frac +4.
- Exam pass@1 tăng **+6.7 đến +8.0 điểm ở mọi round**: A s1 33.3→40.0 ở R0, 23.3→28.0 ở R2; A 1e-5 R0 32.0→40.0.
- Tính trên các lời giải đúng (theo verifier đã vá) trong vòng lặp, lớp lỗi này một mình đã chiếm **16.0–18.6%** là FN
  (`a-math500-lr-fixed` R0: 642 vs 789 accepted trên 2000).
- Mình kiểm tay 30 flip ngẫu nhiên: 29 là đáp án đúng thật (`\frac43` vs `\frac{4}{3}`, `(15,-29)` vs `(15, -29)`...), 1 flip
  có box cuối rỗng. 144 flip ở R0 trải trên 47 đề.

Vậy mọi accuracy tuyệt đối trong paper đều bị đánh giá thấp khoảng 7 điểm. Các **độ giảm** thì vẫn còn sau khi vá cả
hai lớp: A s1 40.0→28.0 so với bản gốc 33.3→23.3; GOLD s1 40.0→16.0, GOLD s2 38.0→13.3. Tuy vậy, câu "Run B là control
verifier-bias" chỉ đúng với một lớp chiếm khoảng 0.1% pool (liên quan issue 1, 2, 15, 16, 20, 21, 33, 43).

## Bảng 49 issue

| # | Tiêu đề (rút gọn) | Verdict | Số liệu đã sửa / bằng chứng (nguồn) |
|---|---|---|---|
| 0 | "Pooling + selection-set scoring tạo ra collapse" chỉ là khẳng định, confound với training dose | CONFIRMED | Pool round-0 của Design P là 3962 mẫu (≈1981 step), so với 872/833 của A 1e-5 s0/s1 (`qwen15b-n500/table.md`, `qwen15b-math500-a*/table.md`), tức gấp ~4.5× số step ở cùng lr 1e-5. Thêm bằng chứng: selection-set scoring **không** thổi phồng hay kéo tụt điểm ở Design I. Sample acc sel/exam theo round của A 1e-5 s0 là 31.1/32.4 → 30.1/30.0 (analyze §9). Không có run nào tách pooling khỏi scoring. |
| 1 | Control A-vs-B không thể phát hiện hiệu ứng | CONFIRMED | Dose thật của Run B: pool +4 (872→876) và +3 (833→836) trên 2800 generation của selection set (0.14%/0.11%; 0.46%/0.36% kept pool). Ở 5e-4 là +3 và 0. B−A ở R4 (1e-5): pass@1 −0.7 [−3.3, +2.0] và 0.0 [−2.7, +2.7]. Ở 5e-4 R2: +5.3 [−2.0, +12.7] và −7.3 [−14.0, −1.3]. Số đếm \dfrac đã có sẵn từ R0 trước khi train (`styles.csv`: 20–29/4000). |
| 2 | "Systematic FN là tolerable" dựa trên control undertrained, đổi dấu | CONFIRMED | Như #1. Thêm F2: lớp FN lớn hơn (gold-boxed, 16–19% số lời giải đúng, +22% kept pool) có mặt ở **cả hai** arm, nên "systematic FN" chưa hề được test ở dose đáng kể. NF−A sample acc ở R2: +0.2 [−3.2, +3.7] và **−5.5 [−9.0, −2.0]**, tức seed 2 cho thấy bỏ filter làm tệ hơn. |
| 3 | Không có CI hay test; noise floor 4.7 điểm là ad hoc | CONFIRMED | CI đã tính (analyze §2). R0→R2 pass@1: A s1 −10.0 [−16.7, −3.3], A s2 −4.0 [−11.3, +2.7], B s1 −4.7 [−12.0, +2.7], B s2 −11.3 [−18.0, −5.3]. Sample acc thì cả 4 run đều có CI loại trừ 0: −8.3 [−12.3, −4.3], −4.7 [−8.2, −1.2], −6.7 [−10.3, −2.7], −9.2 [−12.7, −5.7]. Sign test: 4/4 cho p = 0.0625, 2/2 cho p = 0.25. |
| 4 | "Verifier không phải driver" dựa trên null 2 seed, budget không bằng nhau | CONFIRMED | Số step (train_logs): NF 700/700/700 (~640 s/round), A 220/196/163 và 212/193/175, GOLD 175×3. NF−A ở R2: pass@1 +4.0 [−2.7, +10.7] và −4.7 [−12.0, +2.7]; pass@4 −2.0 / −5.3; sample acc +0.2 / −5.5 [−9.0, −2.0]. Không có equivalence margin nào. |
| 5 | "Non-degenerate accuracy giữ nguyên" đảo chiều khi điều chỉnh độ khó; counterfactual 35.7% cùng lỗi | CONFIRMED (mạnh hơn) | Tái tạo đúng: R0 reweight (p0_all) **44.7 / 38.8**, so với finished acc R2 **38.9 / 36.6**. Δ (p0_fin) −6.5 [−11.5, −1.6] và −2.4 [−6.5, +2.0]. Đề có ≥2/4 degenerate có acc R0 16.6% (n=74) và 17.6% (n=64), còn lại 50.3 / 40.7. Counterfactual naive tái tạo được 35.7%, nhưng tính per-problem chỉ còn **28.4%** (< 33.7 của R0). Theo F1 (cap-hit), finished acc giảm 54.0→43.0 và 50.6→45.4. |
| 6 | "Accuracy trên finished solutions giữ nguyên" bị khái quát hóa quá mức | CONFIRMED (mạnh hơn) | C 5e-4: finished acc 71.5→64.6, pass@1 70.7→48.7 (−22.0 [−29.3, −15.3]), degenerate 2.5→16.7%. Shapley theo proxy: Δsample acc −15.3 = termination −9.1 + finished −6.2. Theo F1, MATH-500 cũng mâu thuẫn với claim này. |
| 7 | Claim "loss không giảm ở 1e-5" bị train log phủ nhận | CONFIRMED | `qwen15b-math500-a/train_logs/round_0.json`: lr ≈ 9.8e-6, loss 0.716→0.375, trung bình theo quartile 0.619/0.493/0.430/0.381. Seed 1: 0.700→0.404. C: 0.934→0.431. train_loss cuối 0.47–0.51. |
| 8 | Title/abstract/contributions vẫn dẫn bằng framing 1e-5 đã lỗi thời | CONFIRMED | Đây là phán đoán về framing; các dữ kiện đi kèm (#1, #7) đều đúng. Bản `paper.tex` đang sửa vẫn còn "≈0.55% of generations" ở abstract (dòng ~44) và "half a percent of the training pool" (dòng ~101, ~856). |
| 9 | Restart từ base mỗi round khiến compounding gần như không có đường | PARTLY | Đúng là adapter mới mỗi round (train.py). Nhưng ở 5e-4 kênh dữ liệu có tác dụng thật: độ giảm tăng tốc ở R2 (A s1 pass@1 33.3→32.7→23.3, proxy degenerate 9.8→14.2→41.3, pool 440→391→326). "Gần như không có đường" chỉ đúng ở 1e-5 (pool 872→843, −3.3%). |
| 10 | Implication xếp held-out evaluation là "nguyên nhân khả dĩ nhất" | CONFIRMED | Mâu thuẫn với câu "cannot apportion" của Sec 5.1. Data §9 (#0) cho thấy selection-set scoring tự nó không làm lệch điểm ở Design I. |
| 11 | Practical implications khái quát quá dữ liệu | CONFIRMED | "Degraded whatever the data": 1e-4 pass@1 R0→R2 là 0.0 [−7.3, +7.3], −3.3 [−10.0, +2.7], −2.7 [−10.0, +4.7]. Chỉ 3 nguồn dữ liệu, 1 model. |
| 12 | Dose-response accuracy dựa trên 2–3 seed, kéo chủ yếu bởi seed 1 | CONFIRMED | Δsample acc per seed: 1e-4 −1.8 / −3.7 / −1.0; 2e-4 −3.5 / −3.7; 5e-4 −8.3 / −4.7. Trung bình 2.2 / 3.6 / 6.5 (review ghi 2.0/3.7/6.5, lệch ≤0.2). Seed 2 gần phẳng. Thêm F1: chuỗi degenerate "sạch hơn" mà review đề xuất dùng thay thì lại là artifact mật độ ký tự, vì cap-hit không tăng ở 1e-4/2e-4. |
| 13 | Train-on-gold "real loss" bị chấm bằng chính verifier bị bias sau format shift | PARTLY | Phần "chưa audit thủ công" đúng. Nhưng re-verify với cả hai patch thì độ giảm vẫn còn: GOLD s1 pass@1 40.0→16.0 (gốc 33.3→15.3), s2 38.0→13.3 (gốc 31.3→10.0). Cap-hit giảm còn 7%, nên không phải do truncation. Finished acc reweight là −25.6 / −25.9. FN của dạng `$...$` chưa được kiểm. Style: dollar 103→1968, boxed 1038→1715 (`gold-math500-lr-fixed/styles.csv`). |
| 14 | Kết luận Run C dựa trên run đơn, noise reference sai, budget lệch | CONFIRMED | C 1e-5 là seed 0, C 5e-4 là seed 1 (manifest), nên partition khác nhau. R3→R4 chiếm 9.3 trong 12.7 điểm giảm. Bootstrap theo đề: −12.7 [−21.3, −3.3], vượt sampling noise nhưng không nói gì về run-to-run noise. |
| 15 | Verifier mang lỗi hệ thống ~8× lớn hơn lỗi đã vá, headline không nhắc | CONFIRMED (lớn hơn ước lượng) | Đo trên chính generation của vòng lặp (F2): +102 so với +2 mẫu kept ở R0 (A s1), tức ≈50×, không phải 8×. Bằng 7.3% số generation của selection set, so với 4.4% paper ước lượng. Ngoài ra 24/41 boxed rejection trong probe là do gold không parse được (`results/viec1/table.md`). |
| 16 | Run D không thể cho thông tin | PARTLY | Phần mẫu số đúng: 17/41 = 41.5%, không phải 8.5%. 8.5% = 17/200 theo comment trong `src/dacntt/verify/adapter.py`. Phần "dose ≤4.4%, chắc chắn null" thì **sai**: dose thật của Run D là +22% kept pool (≈35–50× Run B). Lập luận về noise vẫn đứng: run cùng config lệch 9–13 điểm (#30). |
| 17 | Noise floor 4.7 điểm đánh giá thấp; pass@4 R0 của seed 3 thấp hơn 10–11 điểm | CONFIRMED | pass@4 R0: seed 3 là 40.0, seed 1 là 50.0, seed 2 là 51.3 (`a-lr1e4-seed3/metrics.csv`). |
| 18 | "Không có dấu nhất quán" giữa NF và A bị phủ nhận ở pass@4 | CONFIRMED | NF−A pass@4 ở R2: −2.0 [−9.3, +4.7] và −5.3 [−12.0, +1.3], âm ở cả hai seed (từng CI riêng vẫn chứa 0). |
| 19 | Mức giảm pass@4 của train-on-gold nằm trong khoảng "collapse" của Design P | CONFIRMED | GOLD pass@4 R0→R2: −20.7 [−28.7, −12.0] và −20.7 (R1 −22.7). |
| 20 | "0.55% bị loại sai" trộn tần suất xuất hiện với số bị loại, sai mẫu số | CONFIRMED | Số flip pool thật là +4/2800 (0.14%) và +3/2800 (0.11%) ở 1e-5; ở 5e-4 là +2/1400 và −1. 20–29/4000 tương ứng 0.50–0.73%. Tính trên kept pool thì là 0.46% / 0.36%, nên câu "half a percent of the training pool" gần đúng còn "0.55% of solutions wrongly discarded" thì sai. |
| 21 | Theo luật severity × prevalence của chính paper, patch nhắm vào lớp lỗi nhỏ | CONFIRMED | Định lượng trên vòng lặp: lớp \dfrac chiếm 0.07–0.21% số generation của selection set, lớp gold-boxed 4.3–7.4% (`dose.py`). viec2: 8/10 FN là wrong-number extraction. Boxed chiếm 53% số generation (2136/4000). |
| 22 | Control NF mâu thuẫn với kết quả false positive của Egashira et al. | PARTLY | Dữ kiện nội bộ đúng: NF train trên 1400 mẫu, phần kept chỉ 31.4/27.9/23.3% và 30.3/27.6/25.0%. Nhưng NF s2 **tệ hơn** A có ý nghĩa ở sample acc (−5.5 [−9.0, −2.0]), nên độ "tension" yếu hơn review nói. Nội dung của Egashira là UNVERIFIABLE (chưa WebFetch bài). |
| 23 | Novelty là phép giao hẹp, phần đặc trưng hóa ra không tác dụng, trùng với Xu et al. | PARTLY | Phần dữ liệu đúng: lớp format-bias được vá chỉ chiếm 0.1% pool. Mức trùng với Xu et al. là UNVERIFIABLE (chưa tra bài). |
| 24 | Thiếu thảo luận ReST-EM, RFT, STaR | UNVERIFIABLE | Là issue về văn liệu. Theo CLAUDE.md, cần WebSearch/WebFetch để xác nhận nội dung các bài trước khi trích. Chưa làm. |
| 25 | "Pool contraction và collapse tách nhau" chỉ đúng với pass@8 | CONFIRMED | C 1e-5: pool 1901→1515 (−20.3%), pass@1 −12.7, pass@8 92.7→90.0. A 1e-5 s0: pool −3.3%, pass@1 −2.7. |
| 26 | Sec 4.4 không có bảng diversity; metric chính không được báo cáo | CONFIRMED | `mechanism.md` / `mechanism-ABC.md` có unique-answer ratio nhưng paper không báo cáo, và số được tính trên toàn bộ 500/1000 đề chứ không phải exam. |
| 27 | All-k agreement gắn cơ học với accuracy và non-answer | CONFIRMED | Agreement: P 1.5B 24.8→1.7, 0.5B 10.5→7.3, A s0 14.6→12.0, B s0 14.6→12.2. Thứ tự này trùng thứ tự Δpass@1, đúng như cơ chế p^k dự đoán. |
| 28 | "Replicates across four runs" đếm 2 cặp gần giống nhau thành 4 | CONFIRMED | A và B cùng seed có R0 giống hệt (33.3/33.3, 31.3/31.3), pool R0 440/443 và 424/424. Kết luận định tính vẫn đứng nhờ sample acc (CI ở #3). |
| 29 | Heuristic degenerate chọn sau khi nhìn dữ liệu, không có sensitivity check, "non-degenerate" ≠ "finished" | CONFIRMED (mạnh hơn) | Số của review tái tạo đúng: A s1 R0 có 44.5% không boxed, 34.7% ngắn và không boxed (acc 11.1%); R2 là 20.3%; max len 3941. Sensitivity: degenerate/finished acc với ngưỡng 1200/1500/1800/2000 là R0 36.2/9.8/2.7/0.3% và R2 53.5/41.3/33.3/28.3%. Finished acc R0 48.6/37.2/34.4/33.8, tức ngưỡng thay đổi thì kết luận thay đổi. Cap-hit trực tiếp: xem F1. |
| 30 | Test 1024-limit đơn seed không loại trừ được truncation | CONFIRMED | Replicate (`a-lr5e4-keep`) so với A s1, cùng config: degenerate R2 28.5 so với 41.3, chênh **−12.8 [−16.5, −9.2]**. msl1024−A: pass@1 +9.3 [+2.0, +16.0]. Cap-hit (F1) của keep / msl1024 / A s1 ở R2 là 43.0 / 43.8 / 46.2%. |
| 31 | Lập luận token cap: "gains as much" sai | CONFIRMED | Sample acc từ 512 lên 1536 (reeval): base +6.8, replicate +5.8, 1024-limit +2.0, 2e-4 +3.5. |
| 32 | Thiếu chi tiết tái lập (prompt, decoding, optimizer, LoRA targets, masking...) | CONFIRMED | Code có, paper thì không: prompt "Put the final answer in \boxed{}" (`src/dacntt/gvt/generate.py:10`), chat template, target q_proj/v_proj (`train.py:136`). `max_length=512` chỉ xuất hiện ở Sec 4.6. |
| 33 | FN audit: mẫu số không rõ, chạy trên output của model khác, không chứng minh được không có FP | PARTLY | Mẫu số đã làm rõ: 200 lời giải, 24 gold không parse được, 128 lời giải đúng thật, 10 FN, nên 10/128 là FN rate (`results/viec2/table.md`). Các điểm còn lại đúng. Đo trên vòng lặp (F2), riêng lớp gold-boxed đã chiếm 16–19% số lời giải đúng, gấp hơn 2× con số 7.8%. |
| 34 | "Lost at any cap" khái quát từ 2 cap, 1 seed | CONFIRMED | Degenerate ở 1536 của adapter 1e-4 s2/s3: 6.17% và 12.83%. Max shift của reeval so với R2 của chính run là 6.7 điểm (msl1024 32.7→26.0). |
| 35 | Điểm đồng thuận với Xu et al. là chung chung | UNVERIFIABLE | Cần đọc bài Xu et al. thật. Phần nội bộ ("A–B đổi dấu") thì đúng (#1). |
| 36 | "Sharply for two model sizes" phóng đại mức giảm của 0.5B | CONFIRMED | Design P 1.5B: pass@1 50.0→18.6, pass@8 72.6→48.6. 0.5B: pass@1 −3.7, pass@8 −5.6. |
| 37 | Độ dài tăng 41–52%, không phải "40–50%" | CONFIRMED | +42.8 / +42.3 / +41.2 / +49.8 / +41.9 / +52.1% (A s1, A s2, B s1, B s2, NF s1, NF s2). |
| 38 | "Gate giữ khoảng 31%" chỉ đúng ở R0 | CONFIRMED | 31.4/27.9/23.3% và 30.3/27.6/25.0%. |
| 39 | "0–3 problems" sai đơn vị (là mẫu chứ không phải đề) | CONFIRMED | 440 vs 443 và 424 vs 424 mẫu; 872 vs 876 và 833 vs 836. |
| 40 | Giá trị theo dataset của Design P không giống nhau giữa các preset | CONFIRMED | MATH R3 pass@8: 45.0 (default) so với 44.8 (reward) (`by_dataset.md`). |
| 41 | Khoảng degen acc 1.7–7.8% loại trừ C và gold (0%) | CONFIRMED (rộng hơn) | Tính cả R1 thì khoảng là 0.0–12.8%: B s1 R1 11.3%, C R1 12.8%, keep R1 0.0%, 1e-4 s1 R1 0.0%, C R0 0/15, GOLD s2 R2 0/2. |
| 42 | So sánh "một pha RLVR" với "nhiều round SFT" gây hiểu lầm | PARTLY | Dữ kiện về thiết kế đúng (fresh LoRA mỗi round, chỉ kế thừa dữ liệu). Mô tả Egashira như "một pha" là UNVERIFIABLE khi chưa đọc bài. |
| 43 | "~14% FN … consistent with ours" không khớp với 7.8% | CONFIRMED | Wilson 95% CI của 10/128 là [4.3%, 13.8%], 0/200 trên GSM8K. (Ghi chú: FN trên vòng lặp ≥16% theo F2, nên "consistent" có thể đúng, nhưng vì lý do khác với lý do paper đưa ra.) |
| 44 | "One-off cost of the first round" đọc từ thay đổi ~3 điểm | CONFIRMED | Pass@1 R0→R1 ở 1e-5: −2.7 và −4.0. R0→R4: −2.7 [−10.0, +4.0] và −3.3 [−10.0, +3.3]. |
| 45 | pass@8 "tương đối nguyên vẹn" mâu thuẫn với Design P | CONFIRMED | Design P 1.5B: agreement 24.8→1.7 nhưng pass@8 72.6→48.6. |
| 46 | "Replicate fine-tunes" của gold đo sampling noise | CONFIRMED | train_loss của GOLD là 0.653/0.652/0.652 và 0.659/0.658/0.658, loss từng step giống hệt nhau giữa các round. Training gần như deterministic. |
| 47 | Mô tả định tính về degenerate dựa trên 1 đoạn trích | CONFIRMED | Theo F1: ở R0, 43% generation trên exam là lời giải hợp lệ bị cắt ở 512 token (`tokdist.py`: 942/2000 có đúng 512 token), nên câu "not long legitimate solutions cut by the cap" sai với phần lớn truncation. chars/token của nhóm proxy-degenerate ở R2 là 4.9–5.1, so với 2.9–3.0, phù hợp với lối văn xuôi. |
| 48 | "n = 500" so với split 150/350; pass@1 từ 1 mẫu | CONFIRMED | pass@1 R0 cùng partition: 36.67 (k=8, 1e-5 seed 1) so với 33.33 (k=4), lệch 3.4 điểm chỉ do sampling. |

**Tổng verdict:** CONFIRMED 40, PARTLY 7 (#9, 13, 16, 22, 23, 33, 42), FALSE POSITIVE 0, UNVERIFIABLE 2 (#24, 35).
Cả 9 issue major đều CONFIRMED. Trong đó #5 và #6 mạnh hơn review nói (F1), còn #1, #2 (và #15, #16) có bằng chứng mới về
dose (F2).

## Cần chạy Kaggle không?

**Không bắt buộc.** Không issue major nào **cần** GPU mới để sửa một cách trung thực. Mỗi issue đều sửa được bằng cách
thu hẹp claim, thêm CI, hoặc tính lại trên CPU, và phần CPU mình đã chạy xong ở mục dưới:
- **#0, #10, #11:** hạ xuống "suggestive", ghi thêm dose 3962 so với 872 vào danh sách confound.
- **#1, #2, #4:** báo cáo CI (đã có) và nói thẳng rằng Run B chỉ test một lớp lỗi chiếm 0.1% pool. Bỏ câu "systematic FN
  tolerable", thay bằng "không phát hiện được hiệu ứng; trên ±5–7 điểm thì không loại trừ được".
- **#3:** thay noise floor bằng các CI ở bảng trên.
- **#5, #6:** viết lại anatomy theo cap-hit (F1). Kết luận đúng là: ở 5e-4 phần lớn độ giảm là accuracy trên các lời
  giải đã finish, cap-hit chỉ tăng nhẹ.
- **#7, #8:** sửa câu chữ.

Không có run mới nào thay được việc thu hẹp claim. Nếu muốn **giữ** một claim khẳng định về verifier bias (thay vì thu
hẹp), có đúng một run tùy chọn đáng cân nhắc:

| Run tùy chọn | Sửa issue | Flags `experiments/viec3/run.py` (qua `kaggle_driver.py`, `--resume --rounds-per-process 1`) | GPU-h | Kết quả nào đổi kết luận nào |
|---|---|---|---|---|
| Run D ở 5e-4, seed 1 (seed 2 là tùy chọn thêm) | #1, #2, #16, #21 (biến null "dose 0.1%" thành test có dose ~22% pool) | `--mode hf --dataset math500 --n 500 --rounds 3 --k 4 --max-tokens 512 --seed 1 --holdout-frac 0.3 --learning-rate 5e-4 --patch-verifier-boxed --out results/viec3/d-math500-lr-fixed` (seed 2: `--seed 2 --out results/viec3/d-math500-seed2`) | ~2.2 h/seed (KAGGLE.md đo ~45 phút/round × 3 trên T4; pool lớn hơn ~22% làm train lâu thêm khoảng 0.5 phút/round). Hai seed khoảng 4.5 h, vừa một notebook. | Nếu D−A ở R2 (chấm bằng verifier **gốc** để so cùng thước) nằm trong CI, ví dụ sample acc ±4 điểm, thì có thể nói "sửa lớp FN chiếm 16–19% lời giải đúng vẫn không thay đổi được độ giảm". Đây là bằng chứng thật đầu tiên cho câu "verifier bias không phải driver". Nếu D tốt hơn A vượt CI ở cả hai seed thì claim "systematic FN tolerable" bị **đảo ngược**. |

Lưu ý thực tế để quyết định: run-to-run noise ở 5e-4 lớn. Replicate cùng config lệch 12.8 điểm degenerate, còn
msl1024−A lệch +9.3 pass@1. Control NF (thay đổi dữ liệu mạnh hơn nhiều) cũng đã cho null. Khả năng Run D cho kết quả
"không phân biệt được" là cao. Với quota hẹp, lỗi treo khi có ô GPU thứ hai, và quyết định "không chạy thêm thí
nghiệm", khuyến nghị là **không chạy**: thu hẹp claim và báo cáo F2 như một giới hạn. Phải chạy cả hai seed trong **một**
ô qua `kaggle_driver` (mỗi round một process), không được tách thành hai ô GPU.

## Phân tích CPU đã chạy

Tất cả script nằm trong scratchpad của session
(`/private/tmp/claude-501/.../scratchpad/`; thư mục này bị xóa mỗi ngày, cần thì chép ra). Chạy bằng `.venv/bin/python`.

1. **`score_all.py`**: re-verify toàn bộ generation của 21 run viec3 bằng `MathVerifyAdapter("reward")` với patch
   theo manifest. Pass@1 / pass@k tính lại khớp metrics.csv ở mọi run và round.
2. **`analyze.py` → `analysis.md`**:
   - Bảng anatomy theo round.
   - Paired bootstrap CI cho R0→R_last và cho hiệu giữa các run (đã dẫn ở #1, #3, #4, #18, #30).
   - Difficulty reweighting (#5: tái tạo 44.7/38.8 so với 38.9/36.6). Δ p0_fin của 14 run: 5e-4 MATH từ −2.4 đến −6.7,
     C 5e-4 −11.7 [−16.2, −7.2].
   - Counterfactual per-problem 28.4%.
   - Shapley theo proxy: ở 5e-4 MATH, termination −7.3 đến −10.8 và finished từ +0.6 đến +2.7. Với C: −9.1 / −6.2.
     Với GOLD: +2.3 / −22.0.
   - Sensitivity ngưỡng (#29), length growth (#37), selection so với exam (#0), sign test, Wilson CI.
3. **`caphit.py`, `tokdist.py`, `capanat.py`**: cap-hit bằng tokenizer Qwen, decomposition và reweighting theo cap-hit
   (F1). Shapley theo cap-hit ở 5e-4 MATH cho thấy finished acc chiếm 35–74% độ giảm sample acc.
4. **`patch_dose.py`, `dose.py`, `flips.py`**: dose của patch frac (Run B) và patch boxed (Run D) trên pool và exam
   (F2). Kiểm tay 30 flip. Tính FN rate trên vòng lặp: 15.5–18.6% mỗi round (A s1, A s2, A 1e-5).
5. **Đọc log**: step count, loss từ train_logs (#4, #7, #46), wall time (train_runtime A 165/146/122 s, NF 638/640/653 s;
   ~45 phút/round toàn bộ theo `experiments/viec3/KAGGLE.md`).

Hạn chế của phân tích CPU:
- Cap-hit được suy ra bằng cách re-tokenize text đã decode (`skip_special_tokens`), không phải số token mà generator thực
  sự trả về. Tuy vậy phân phối có đỉnh rõ ở đúng 512 (942/2000), nên sai số không đáng kể.
- Verifier đã vá chưa được audit FP ngoài 30 flip kiểm tay.
- Các issue văn liệu (#22–24, 35, 42) cần WebSearch/WebFetch theo luật của repo trước khi kết luận.
