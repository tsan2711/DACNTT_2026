# Paper Summary: Mathematics or the Verifier? No Detectable Gain from Verifier-Filtered Self-Training of a 1.5B Model

NOTE: this is the working draft (paper_main.tex built to PDF). The abstract has bold placeholders ([N], [K], [MDE], [X], [RESULT], [UPDATE after new round]) awaiting a new GPU round. Supplementary refs ("Table ??", "Appendix ??") are unresolved in the standalone PDF because the appendix is a separate supplementary.tex. Treat placeholders/unresolved refs as known WIP, not as findings, except where they hide a substantive gap.

## Research Question
After several generate-verify-select-train (GVT) rounds with offline LoRA SFT, is a 1.5B model better at math, or has it only learned to write what a rule-based verifier (math-verify) accepts?

## Core Hypothesis / Thesis
Negative result: no detectable gain on a held-out exam at any learning rate; no arm (even train-on-gold) improves, so the null concerns this recipe, not self-training. Whether the model learns verifier style is unresolved (pre-set rule is one-sided). A post hoc per-round false-reject audit finds no adaptation to a gold-storage defect but has low power and no positive control.

## Methodology Overview
Qwen2.5-1.5B-Instruct (0.5B in pooled Design P), MATH-500 and GSM8K (first 500 each). Design P pooled (both datasets, one adapter, scored on selection problems); Design I isolated (one dataset, 150-problem exam, 350 selection). LoRA r=16 on q/v, 1 epoch, fresh adapter per round from base, fp16 T4, 512-token gen cap = 512 train limit incl. prompt, loss over prompt. Paired problem-level bootstrap CIs (no seed variance, no multiplicity correction).

## Key Definitions & Notation
- V: original math-verify pipeline; V': repaired verifier wrapping gold in \boxed{}.
- r_t: share of V'-accepted generations that V rejects (false-reject share).
- Patch: \dfrac/\tfrac -> \frac. Gold-storage defect: gold stored without delimiter, rejects 15.5-18.4% of V'-accepted.
- Sample accuracy: mean over all k samples (post hoc primary). pass@1 = first of k samples.
- Cap-hit: re-tokenised text >= 508 tokens.

## Key Numerical Parameters
- Runs: 10^-5 (k=8, 5 rounds), 10^-4 (3 seeds), 2e-4 (2), 5e-4 (2) with k=4, 3 rounds; no-filter and train-on-gold controls at 5e-4.
- Detectable effect (80% power): ~10 pts pass@1, 8-10 pass@k, 3.5-5.5 sample acc, computed as 2.8h/1.96.
- 2.2-pt bound on sample-accuracy gains (post hoc; omits seed variance); replicate pair ends 3.2 pts apart.
- V false-negative rate 7.8% (10/128), 51/500 golds unparsable (10.2%).
- Gold-storage defect fires on 54-62 problems, rejects 94-98% there; 24-28 problems where an escaping form exists; pool 2-12 examples/round.
- r_t falls 1.5-2.6 pts overall; boxed-only changes -0.4 to +0.7.
- Cap-hit decomposition: 12-30% of decline (seed 1), 52-72% (seed 2). Finished-matched loss 5.5-10.6 at 5e-4.
- 24-26% of round-0 pool truncated in training; no-filter 62.4%.

## Main Claims (with evidence location)
1. No detectable gain at any LR — Sec 4.2/4.4, Table 2, Sec 5.1.
2. Sample-accuracy intervals exclude gains > 2.2 pts — Sec 5.1 (loose bound).
3. No arm improves, so null is about recipe — Sec 4.4, Table 3.
4. At highest rate accuracy falls in every run; finished solutions 5.5-10.6 pts worse — Sec 4.4/4.5.
5. Audit finds no adaptation to gold-storage defect (r_t falls, explained by boxed share) — Sec 5.3, Table 4.
6. Patch/no-filter controls cannot detect an effect — Sec 4.3/4.4.
7. Pooled collapse (pass@1 50.0 -> 18.6) does not reproduce under isolation — Sec 4.1, 5.1.

## Section Map
- 1 Intro: GVT loop, RLVR context, pre-set rule, post hoc list, contributions.
- 2 Related Work: STaR/ReST, RLVR small scale, verifier error, auditing self-improvement.
- 3 Setup: loop, verifier bias, designs P/I, models/training/metrics, uncertainty, power.
- 4 Results: 4.1 Design P collapse, 4.2 Design I @1e-5, 4.3 patch control, 4.4 higher LR + controls (Tables 1-3), 4.5 anatomy of decline.
- 5 Discussion: 5.1 answers, 5.2 interpretation, 5.3 proposed audit (Table 4).
- 6 Limitations, 7 Conclusion.

## Notable Cross-References
- Sec 3.4 power calculation feeds Abstract/Intro/5.1/7 headline "about 10 / 8-10 / 3.5-5.5".
- Table 2 vs. Sec 4.2/4.4/5.1 text (ranges of pass@1 changes, interval claims).
- Table 4 vs. Sec 5.3 text and Sec 3.2 (15.5-18.4%, 54-62 problems).
- Table 1 vs. Table 2 vs. Table 3 (A seed 1/2 values at 5e-4).
- Sec 4.5 decomposition vs. Sec 5.3(ii) and Conclusion.
