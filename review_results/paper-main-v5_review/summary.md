# Paper Summary: Mathematics or the Verifier? A Null Result for One Verifier-Filtered Self-Training Recipe on a 1.5B Model

## Research Question
After several generate-verify-train (GVT) rounds with offline LoRA SFT on Qwen2.5-1.5B-Instruct and the rule-based verifier math-verify 0.9.0, does the model get better at math, or only learn to write what the verifier accepts?

## Core Hypothesis / Thesis
No pass@1/pass@k gain is detectable at any learning rate. The null concerns this recipe only, because a positive gate (train on reference solutions) fails (49.2 -> 17.0). All scores are graded by the same verifier that selects the data, so neither branch of the question is answered. A post hoc false-reject audit (r_t) of a storage defect is uninformative about adaptation (r_t fall is an identity with the boxed share; no valid positive control).

## Methodology Overview
Design P (pooled, both datasets, 1000 problems, selection == eval) vs Design I (isolated, 500 problems, 150 exam / 350 selection). Runs A (original verifier), B (patched \dfrac->\frac), C (GSM8K). LR 1e-5 (k=8, 5 rounds); 1e-4/2e-4/5e-4 (k=4, 3 rounds). Controls at 5e-4: no-filter, train-on-gold. Final round (Section 4.6): "revised recipe" with seven simultaneous changes (completion-only loss, all-linear LoRA, 1024 cap, normalised gold, 300 MATH-train pool, 500 exam, k=2, 1 adapter, LR 1e-4), 3 loop seeds, 1 gate seed, 2 injected-bias runs. Independent string-match grader for final-round generations (Section 5.1).

## Key Definitions & Notation
- V: original verifier (gold stored bare). V': gold wrapped in \boxed{} when the prediction contains one.
- r_t = #{accepted by V' but rejected by V}/#{accepted by V'}; identity r_t = r_boxed_t x (boxed share among V'-accepted).
- pass@1 = first sample only; sample accuracy = mean over k samples; pass@k = any of k.
- Detectable effect ~ 2.8h/1.96 from CI half-width h (80% power, 5% level), omits training-seed variance.
- "Finished, matched": accuracy of generations below the 512-token cap minus untrained accuracy on the same problem mix.
- Cap-hit: re-tokenised generation >= 508 tokens.

## Key Numerical Parameters
- Format probe FN 7.8% (10/128, Wilson 4.3-13.8) MATH-500; 0% GSM8K. 51/500 golds unparseable by V (10.2%), 11-18 per 150-problem exam partition.
- Gold-storage defect rejects 15.5-18.3% of V'-accepted; round-0 pool 440 -> 542 (+23%); lowers pass@1 by 4.7-8.0; fires on 54-62 problems, 29-34 with unparseable gold.
- Pass@1 detectable ~10 pts (6 in final round); replicate pair differs 3.2 pts; B-A flips +5.3 -> -7.3.
- Final round: loop pass@1 -4.8/-3.2/-4.2 (mean -4.1, t-interval [-6.1,-2.1]); sample acc -2.9/-5.3/-5.4 (mean -4.5, [-8.1,-1.0]); gate 49.2 -> 17.0 (-32.2); 2e-5 rerun 49.2 -> 20.6; 60 of 1600 -> 1577 of 1600 $-spans.
- Independent grader: pass@1 -3.6/-2.2/-4.6, gold -30.0; sample acc -2.5/-5.5/-5.3.
- Injected bias: hash 30% (boxed share -4.9 vs -3.1, diff -0.1); content rule: 49 of 300 selection problems, 263 kept vs 298, 70 of 500 exam problems; share 95.0% stays vs 90.2 -> 87.4 (+2.8 [-2.8,+8.3]); pass@1 -7.0 [-11.2,-3.0].
- Table 5 r_t changes -2.6, -2.6, -1.5 (self-training), gold +3.3, +2.1.
- Cap decomposition: 12-30% (seed 1 originals), -2 and 5% (two further runs), 52-72% (seed 2).
- Sample-accuracy bound "about 2.2 points" (largest upper limit among observed intervals).
- Design P: pass@1 50.0 -> 18.6, pass@8 72.6 -> 48.6; pool 3,962 vs 872 (~4.5x).
- Trainer: transformers 5.0.0, peft 0.19.1, TRL 1.10.0; rank 16, alpha 32, q/v proj; dropout 0, wd 0, clip 1.0, seed 42; batch 2, no accumulation.

## Main Claims (with evidence location)
1. No gain detectable at any LR -- Tables 1-2, Sections 4.2-4.4
2. Final-round loop falls in all 3 seeds; gate fails, so null is about the recipe -- Table 4, Section 4.6
3. All scores graded by the selecting verifier; independent grader on final round only -- Sections 3.4, 5.1
4. r_t fall matches boxed share (identity); audit uninformative -- Section 5.3, Table 5
5. At 5e-4 finished accuracy drops 5.5-10.6 pts; cap-share decomposition -- Section 4.5
6. Patch and no-filter controls show no consistent difference but are dose-confounded -- Sections 4.3, 4.4, Table 3
7. Pooled collapse does not reproduce under isolation (dose/pooling confounded) -- Section 4.1

## Section Map
- Abstract, 1 Intro (chunks 00-01), 2 Related Work (01)
- 3 Setup: 3.1 loop, 3.2 verifier bias and V', 3.3 designs, 3.4 models/training/metrics/uncertainty (chunks 01-03)
- 4 Results: 4.1 Design P, 4.2 Design I at 1e-5, 4.3 patch control, 4.4 higher LR (Tables 1-3), 4.5 anatomy (chunks 03-05)
- 4.6 final round (Table 4, injected bias) (chunks 05-06)
- 5 Discussion incl. 5.3 audit (Table 5), 6 Limitations, 7 Conclusion (chunks 06-07)
- References (chunk 07). Supplementary appendices are NOT in this text; only referenced.

## Notable Cross-References
- Intro/abstract claims vs Sections 4.6 and 5.3.
- 2.2-point bound (Section 5.1) vs Section 3.4 and Intro "3.5-5.5 sample accuracy".
- "re-scoring five runs with V'" (Section 3.2 / 5.1 / 5.3) vs Table 5 (three self-training runs + 2 gold).
- Section 3.2 "51 golds unparseable, offset cancels only if..." vs Section 5.3 "29-34 unparseable gold".
- Table 3 vs Table 2 vs Table S6 (A rows).
- Section 4.6 sample sizes (gate 1 seed, bias controls 1 seed each) vs Limitations.
