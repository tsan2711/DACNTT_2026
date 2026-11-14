# Response to Reviewer — DA148

**"Mathematics or the Verifier? No Detectable Gain from Verifier-Filtered Self-Training of a 1.5B Model"**
Resubmission, deadline 2026-11-14. Main text: 16 pages (was 17 + 21 appendix pages in one file; the appendices are now a separate `supplementary.tex`).
Code, saved generations and scripts: https://github.com/tsan2711/DACNTT_2026 (tag `paper-2026-11`).

Thank you for the careful review, and for recomputing the tables. We agree with the central criticism: the original experiments could not answer the research question, because no arm, including training on reference solutions, improved the model. We responded with one new round of experiments. **That round did not fix the problem: the positive gate still fails.** The paper now says so in the abstract and the conclusion. Below, each point is marked DONE, PARTLY DONE or NOT DONE.

---

## Major comments

### M1. Working recipe and a positive control — PARTLY DONE (gate still fails)

**Done.** We ran a final round with the recipe changes you listed (Section 4.6): loss on the completion only, LoRA on all linear layers, generation and training cap of 1,024 tokens, normalised gold answers.

**Result.** The positive gate fails. Training on the 300 reference solutions lowers pass@1 on MATH-500 from 49.2% to 17.0% (−32.2, 95% bootstrap CI [−36.8, −27.6]). Because a high learning rate could be the cause, we reran at 2×10⁻⁵: 49.2% → 20.6% (−28.6). In both runs the model adopts the reference style (`$`-delimited spans in 1,577 and 1,558 of 1,600 generations). So the failure is not the learning rate, and we have no recipe that raises accuracy. The verifier-filtered loop, now run with **three seeds**, loses pass@1 in every seed: −4.8 [−9.2, −0.6], −3.2 [−6.8, +0.6], −4.2 [−8.4, −0.2] (mean −4.1, t-interval over three seeds [−6.1, −2.1]); sample accuracy −2.9, −5.3, −5.4. We read this as no gain and probably a small loss, cause not isolated.

**Not done.**
- We did not find a recipe that passes the gate.
- We did not try distillation from a stronger teacher, which you suggested. Doing so would not test self-training.
- We did not try a different way of making the reference solutions usable, for example rewriting them in the model's own style. We think this is the most likely fix, but we have not tested it.

**Consequence in the paper.** The title, abstract and conclusion say the null concerns the recipe, not self-training in general. We make no claim about self-training.

### M2. Gold-storage defect, rerun, injected bias — PARTLY DONE

**Done.**
- Gold answers are normalised in the final round only (Section 4.6).
- The final round uses a clean exam verifier.
- Following your suggestion and our Appendix K, we ran two injected-bias positive controls for the audit (one seed each, 10⁻⁴): (a) the selection verifier rejects every `\boxed` answer on a hash-chosen 30% of problems; (b) new, learnable from the problem: it rejects every `\boxed` answer whose gold contains `\frac` (70 of 500 problems).
- The per-round false-reject rate r_t is fixed at 15.5–18.3% (the old range was inconsistent) and now comes from one script, `rt_audit`.

**Limits of this control (stated in the paper).** The biased set is chosen by a hash, so it cannot be learned from problem content: the control could not elicit selective avoidance by design, and we report no r_t for it. It therefore does not validate the audit, and the paper now calls the audit "uninformative about adaptation" rather than "no adaptation found".

**Result of the learnable bias (b).** The `\boxed` share on the penalised problems stays at 95.0% (change +0.0, [−4.6, +5.0]); on the others it goes 90.2% → 87.4%. The difference is +2.8 ([−2.8, +8.3]), against −3.7, −2.7 and −5.5 for the same split in the three unbiased seeds. pass@1 falls 7.0 points ([−11.2, −3.0]). The model does not stop boxing where boxing is penalised in two rounds. No r_t is reported.

**Result of the hash bias (a).** The `\boxed` share on the affected problems falls 4.9 points and 3.1 points on the others. The group difference relative to the unbiased run is −0.1 ([−6.1, +6.0]). The model drops `\boxed` in general and not selectively, and one seed cannot show avoidance in either direction. **The audit therefore still has no positive control that shows an effect, and the second research question stays open.** The paper says this.

**Not done.**
- The earlier runs (all MATH-500 and GSM8K runs before the final round) were **not rerun** with the corrected gold. Their scores still come from the biased verifier, as the Limitations section states.
- The 51 unparseable gold answers were handled by normalisation in the final round, but we did not repair them in the old runs.
- Reporting a single set of scores for the old runs (your B3.1/B3.2) is therefore still not done; the small discrepancies between Tables 3 and 5 that you found (math-verify timeouts, a separate re-score) have not been removed. *(Check before sending whether the paper still explains them.)*

### M3. Power — PARTLY DONE

**Done.** The final round selects from a pool of 300 problems from the MATH training split and evaluates on all 500 MATH-500 problems. The detectable effect drops from about 10 to about 6 points of pass@1 (5 for pass@2).

**Done in part.** The final-round verifier-filtered loop now has three seeds (1, 2, 3). Intervals still omit training-seed variance per run; the three-seed spread is reported.

**Not done.**
- The gold arm and both injected-bias runs still have **one seed**. We did not run three seeds per condition.
- The old runs keep the 150-problem exam and the MDE of about 10 points.
- The detectable-effect figures are now stated as **lower bounds**: the intervals omit seed variance, and the paper's own replicate pair (3.2 points apart) and the B−A sign flip (+5.3 / −7.3 on near-identical pools) show that this variance is as large as the quoted effects. The abstract now says "about 10 points (6 in the one-seed final round) … so likely more".
- The 2.2-point sample-accuracy figure is described as the largest observed upper limit, a post hoc figure, not a power statement. The abstract does not use it.

### M4. Dose matching — PARTLY DONE

**Done.** The final round uses a fixed pool of 300 problems. In the one comparison where we checked directly (the round-1 pools of 392 and 386 examples), the dose is about 195 optimizer steps.

**Not done.** Dose is **not** matched across all arms of the earlier grid. The Limitations section still lists "unequal training doses confound every cross-arm comparison". We did not rerun the older arms with a fixed step count. The no-filter and Design P comparisons remain dose-confounded, and the paper's wording on them is that their cause is open.

### M5. Length and repetition — DONE (with a cost)

The main text is 16 pages including references. The appendices are in a separate `supplementary.tex` (24 pages) with cross-references. We removed the version-history passages ("earlier versions of this paper…"). The abstract and the conclusion state each caveat once.

**Cost.** The Limitations section is a single dense paragraph, and the supplement is longer than the main text. If the venue counts the supplement toward the limit, the paper is still over it.

---

## Minor comments

### m1. Title, question, abstract — PARTLY DONE
The title is shorter (the clause after the colon was dropped) and states the null result. The abstract is shortened, but it still contains many numbers. We kept the second question ("the verifier") in the title because the audit is part of the study, but the paper says it remains open.

### m2. Base model, second model family — NOT DONE
We ran only Qwen2.5-1.5B-Instruct. We have **no base model and no second family**. This is listed under Scope in the Limitations. Contamination of MATH-500/GSM8K cannot be excluded. We had no GPU quota left for it.

### m3. Public repository — DONE
Link and tag in the paper (Code availability): https://github.com/tsan2711/DACNTT_2026, tag `paper-2026-11`. Generations and scores for the runs are in `results/`. The paper says which items were *not* saved: generation-time token counts, Design P's training logs and the 1,536-token re-scoring outputs.
*(Before sending: confirm the tag and latest commit are actually on the remote. Pushes failed on 2026-11-11 with "Connection reset by peer", so this is unverified.)*

### m4. Wang et al. — DONE
The text now says: the MATH-500 gain of 36.0% → 73.6% (37.6 points) contains only 8.6 points beyond format correction, as the authors' abstract states (arXiv:2504.20571, checked against the abstract on 2026-11-11). Thank you for pointing this out.

### m5. AI-use statement — DONE
"Use of AI tools" section added: Claude (Anthropic) via Claude Code was used for the manuscript, scripts and automated reviews; the authors designed the study, ran the experiments and take responsibility.

---

## Other points in the review

- **B1.3 / reading rule that fires only if accuracy rises.** Not changed. The rule is still one-sided. We removed the claim that the question is answered.
- **B2.3 learning-rate grid.** Not rerun. The grid still mixes k, number of rounds, dose and metric; only the three high rates are comparable. Stated in the Limitations.
- **B2.4 grading with the corrected verifier.** Not done for the old runs.
- **B2.5 continued training.** Not done. The restart-from-base design leaves little room for compounding; stated in the Limitations.
- **B2.6 pass@1 from one sample.** Sample accuracy is reported alongside; it was chosen post hoc, and the paper says so.
- **B4 contribution beyond Xu et al.** The Related Work section says the closest work is Xu et al. (Phantom Gains), and that our per-round false-reject measurement is not new (it is the per-step tracking of Egashira et al. and TinyV). We no longer claim the combination as a contribution.
- **B4 Lightman et al.** Cited (arXiv:2305.20050). The PRM800K grader normalises `\dfrac` and `\frac43`; we did **not** run it as a second verifier.
- **Reference accuracy.** We rechecked the cited numbers against the arXiv papers on 2026-11-11 (see below). Two sentences were narrowed.

### Citation re-check (2026-11-11, against arXiv)
| Reference | Checked | Result |
|---|---|---|
| Wang et al. 2504.20571 | 36.0→73.6 MATH500; 8.6 beyond format | matches abstract |
| Shao et al. 2506.10947 | +21.4 random, +29.1 ground truth | matches abstract |
| Dang & Ngo 2503.16219 | AMC23 63→80, ~7,000 samples | matches abstract |
| Huang et al. 2505.22203 | recall 86%; 0.95 math-verify | 86% is in the paper's text, but its own Table 5 averages about 90.5%; 0.95 is Math-Verify on the MATH column (DeepSeek-R1-Distill-Qwen-32B subset) |
| TinyV 2505.14625 | rule-based verifier false negatives | abstract: 38% of responses in Big-Math-RL-Verified; abstract says "verifiers", not only rule-based |
| Egashira et al. 2605.02909 | per-step FNR tracking; unlearning | confirmed in Sections 4.1 and 4.2, **only for format-based false negatives** — we changed our text to say so |
| Xu et al. 2608.20290 | Qwen3-8B LoRA; seven failures | confirmed; seed variance (F5) and fixed token cap (F3) are among the seven |
| Kim et al. 2603.24472 | self-distillation degrades, shortens | confirmed; the teacher sees the correct solution (SDPO) — we changed "self-distillation on ground-truth solutions" to match |

---

## What remains unresolved
1. The positive gate fails, at 10⁻⁴ and 2×10⁻⁵. We have no recipe known to improve the model.
2. The gold gate and both injected-bias controls have one seed; the loop has three.
3. The older runs were not rerun with the normalised gold; their numbers still come from the biased verifier.
4. Doses are unequal across the older arms; the learning-rate grid is still confounded.
5. One model, instruction-tuned only; no base model, no second family, no continued training.
6. The second research question (does the model learn the verifier?) is open.

We believe the paper is now an honest null result for one recipe, with an audit method and its limits, and we have written it that way.
