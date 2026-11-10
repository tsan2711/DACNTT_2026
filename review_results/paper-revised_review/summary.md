# Paper Summary: Mathematics or the Verifier? A Direction-Free Test of Verifier Adaptation, Applied to Self-Training of Qwen2.5-1.5B

## Research Question
After several Generate–Verify–Train (GVT) rounds of offline rejection-sampling LoRA SFT, is Qwen2.5-1.5B-Instruct better at mathematics, or has it only learned to write what the rule-based verifier (math-verify 0.9.0) accepts?

## Core Hypothesis / Thesis
(1) No detectable gain on held-out problems at any of four learning rates; (2) the pre-registered rule for "verifier-style learning" is one-sided (fires only if accuracy rises), so the authors propose post hoc a "direction-free" test: r_t = share of V'-accepted generations rejected by V (V' = repaired verifier) per round; r_t should fall if the model adapts to V. For the gold-storage defect r_t stays 15.5–18.4% → "the model does not adapt to this defect". (3) At the highest LR (5e-4) accuracy declines, mostly via less accurate finished solutions, partly via more cap-hits.

## Methodology Overview
GVT loop: generate k samples, verify with math-verify, keep accepted, train a FRESH LoRA adapter on base model each round (restart-from-base). Design P (pooled GSM8K+MATH-500, scored on selection set, 0.5B & 1.5B) vs Design I (one dataset, 350 selection / 150 held-out exam, 1.5B). Runs A (MATH-500 original verifier), B (\dfrac patch), C (GSM8K); LR 1e-5 (k=8, 5 rounds), and 1e-4, 2e-4, 5e-4 (k=4, 3 rounds R0–R2); controls no-filter and train-on-gold at 5e-4. Paired problem-level bootstrap intervals (150 problems); post hoc cap-hit decomposition; post hoc gold-storage re-score.

## Key Definitions & Notation
- GVT: Generate–Verify–(Select)–Train loop.
- Round 0: untrained base; round t model = base + adapter trained on pool accepted at round t−1.
- pass@1: correctness of first of k samples (one draw). pass@k: any of k accepted. Sample accuracy: mean over k (chosen as primary post hoc).
- "Correct" = accepted by the verifier (preset reward); same verifier selects and grades.
- Cap-hit: re-tokenised decoded text ≥508 tokens (cap 512).
- Matched finished accuracy: last-round finished acc minus round-0 finished acc weighted on same problem mix.
- Decomposition: Δacc = s̄Δf + Δs(f̄−c̄) + (1−s̄)Δc.
- r_t = #{accepted by V' but rejected by V} / #{accepted by V'}.
- Gold-storage defect: gold stored without delimiter; math-verify only fully parses LaTeX inside \boxed{}/$; bare gold parsed to first number, so correct boxed prediction fails.
- \dfrac patch: rewrite \dfrac/\tfrac → \frac (Run B).

## Key Numerical Parameters
- Temperature 0.8, top-p 0.8, top-k 20, rep penalty 1.1, 512 new-token cap; training max_length 512 incl. prompt (24–26% of pool truncated).
- LoRA r=16, α=32, q_proj/v_proj, batch 2, 1 epoch, AdamW linear decay no warmup, loss over whole sequence incl prompt, fp16 T4.
- Pools: Design P 1.5B 3,962 at R0 (≈4.5× Run A 872); Run C 1,901; 5e-4 Run A 440/424; no-filter 1,400; gold 350.
- Verifier: \dfrac rejected 100%; FN 7.8% (10/128) MATH-500 on Qwen2.5-7B solutions, 0% GSM8K; 51/500 unparseable golds (10.2%); gold-storage defect rejects 15.5–18.4%, pool +~22–23% if fixed; \dfrac patch changes 0–4 examples.
- Understatement factor 0.73–0.78; 2.2-pt bound on sample-accuracy gain (≈3 on rescored scale).
- Cap-hit at R0 41–48% MATH-500, 3.5–3.8% GSM8K.
- 76 intervals in Table 5, no multiplicity correction.

## Main Claims (with evidence location)
1. "no pass@1 or pass@k gain has a problem-level bootstrap interval excluding zero ... sample-accuracy intervals exclude gains above 2.2 points" — Abstract, §5.1, Table 5.
2. "that share does not fall over rounds: the model does not adapt to this defect" — Abstract, §3.2, §5.3(i), App B (three runs, no interval).
3. "At the highest rate accuracy falls in every run, and finished solutions become 5–11 points less accurate" — §4.4, §4.5, Tables 5, 7, 11.
4. Design P collapse (50.0→18.6 pass@1) does not reproduce under isolation; cause unidentified (dose 4.5×) — §4.1, App D.
5. Patch control uninformative (0–4 examples) — §4.3, App F.
6. \boxed share falls; cannot separate imitation vs drift; train-on-gold strong style convergence and large decline (pass@4 −21) — §4.4, App G.
7. Cap-share part = 12–30% (seed 1), 52–72% (seed 2) of decline at 5e-4 — §4.5, Table 7.
8. Test applies to RLVR checkpoints (not run) — §5.3.
9. Novelty: no prior per-round false-reject test of verifier adaptation — §2, App A.

## Section Map
- Abstract/§1: motivation (RLVR spurious rewards), research question, pre-set measures, contributions.
- §2 / App A: related work; positioning.
- §3.1 GVT loop; §3.2 verifier & defects; §3.3 Designs P/I; §3.4 models, metrics, uncertainty; App B verifier in full; App C uncertainty.
- §4.1 Design P (Table 2, 9; App D); §4.2 Design I at 1e-5 (Table 3, Fig 1; App E); §4.3 patch control (App F); §4.4 higher LRs + controls (Tables 4, 5, 6, 10; App G); §4.5 anatomy (Tables 7, 11, 12; App H).
- §5.1 answer; §5.2 interpretation; §5.3 proposed audit (r_t test, decomposition, dose checks); App I.
- §6 / App J limitations; §7 conclusion; App K future work.

## Notable Cross-References
- §3.2 → App B for gold-storage analysis and r_t numbers.
- §4.1 → App D for selection-set scoring check (numbers that partly disagree with main text: at 1e-5 selection falls less).
- §4.2 → App E (sample-acc intervals: only B seed 0 excludes zero, while §4.2 implies A and B).
- §5.3 r_t "17% ... 20% throughout at 1e-5" vs abstract range 15.5–18.4% (different denominators).
- Table 5 / Table 7 / Table 11 matched finished values must agree.
- App D selection-set comparisons cite exam declines (−1.4, −15.4, −13.0) that differ slightly from Table 5 (−1.5, −15.3, −13.1).
