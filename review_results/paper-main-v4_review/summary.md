# Paper Summary: Mathematics or the Verifier? No Detectable Gain from Verifier-Filtered Self-Training of a 1.5B Model

## Research Question
After several generate-verify-train (GVT) rounds with offline LoRA SFT on Qwen2.5-1.5B-Instruct and math-verify, does the model get better at math, or only learn to write what the verifier accepts?

## Core Hypothesis / Thesis
No pass@1/pass@k gain is detectable at any LR (null concerns this recipe only, because a positive gate (train on gold) fails). A post hoc false-reject audit (r_t) of a storage defect is uninformative about adaptation (no positive control).

## Methodology Overview
Design P (pooled, 2 datasets, 1000 problems, selection==eval) vs Design I (isolated, 500 problems, 150 exam / 350 selection). Runs A (orig verifier), B (patched \dfrac->\frac), C (GSM8K). LRs 1e-5 (k=8, 5 rounds), 1e-4/2e-4/5e-4 (k=4, 3 rounds). Controls: no-filter, train-on-gold. Final round: corrected recipe (completion-only loss, all-linear LoRA, 1024 cap, 300 MATH-train pool, 500 exam, k=2, 2 rounds, LR 1e-4), 3 seeds loop, 1 seed gate; injected-bias controls.

## Key Definitions & Notation
- r_t = #{accepted by V' but rejected by V}/#{accepted by V'}; V' wraps gold in \boxed{} when prediction contains one.
- sample accuracy: mean over k samples; pass@1 = first sample only.
- Detectable effect ≈ 2.8h/1.96 from CI half-width h.
- Finished, matched: accuracy of generations below 512-token cap minus untrained accuracy on same problem mix.

## Key Numerical Parameters
- Format-probe FN 7.8% (10/128, Wilson 4.3–13.8) on MATH-500, 0% GSM8K; 51/500 golds unparseable (10.2%).
- Gold-storage defect rejects 15.5–18.3% of V'-accepted; pool 440→542 (+23%).
- Pass@1 detectable ≈10 pts (6 in final round); replicate pair differs 3.2 pts; B−A flips +5.3 → −7.3.
- Final round: loop −4.8/−3.2/−4.2 pass@1 (mean −4.1, t-interval [−6.1,−2.1]); gate 49.2→17.0 (−32.2); 2e-5 rerun 49.2→20.6.
- Table 5 r_t changes −2.6, −2.6, −1.5; gold +3.3, +2.1.
- Sample-accuracy bound "about 2.2 points" (largest upper limit among observed intervals).
- Design P: pass@1 50.0→18.6, pass@8 72.6→48.6; pool 3,962 vs 872 (~4.5x).

## Main Claims (with evidence location)
1. No gain detectable at any LR — Table 2, 4.2–4.4
2. Final round loop falls in all 3 seeds — Table 4
3. Gate fails so null is about recipe — 4.6
4. r_t fall matches boxed share; audit uninformative — 5.3, Table 5
5. At 5e-4 finished accuracy drops 5.5–10.6 pts; cap-share decomposition — 4.5, Table S9
6. Patch control and no-filter control show no consistent difference but are dose-confounded — 4.3, 4.4

## Section Map
- 1 Intro: GVT, RLVR context, pre-set reading rule (one-sided), post hoc list
- 2 Related work
- 3 Setup: loop, verifier bias, designs, metrics, uncertainty
- 4 Results: 4.1 Design P, 4.2 I @1e-5, 4.3 patch control, 4.4 higher LR (Tables 1–3), 4.5 anatomy, 4.6 final round (Table 4)
- 5 Discussion incl. proposed audit (Table 5)
- 6 Limitations, 7 Conclusion

## Notable Cross-References
- Table S-appendices (supplementary) referenced for Design P, power, cap decomposition.
- Table 2 vs Table 1/3 numbers; Section 3.4 vs 5.1 "2.2 point" bound; Section 4.6 gate vs Abstract.
