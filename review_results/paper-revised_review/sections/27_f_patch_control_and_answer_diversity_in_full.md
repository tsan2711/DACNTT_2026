## F Patch Control and Answer Diversity in Full
Runs A and B are identical in dataset, seed, split, model and training configu-
ration and differ only in whether \dfrac/\tfrac are normalised before verifi-
cation. Their curves are close (Table 3): at round 4, B minus A is −0.7 [−3.3,

24
T. S. Nguyen and D. A. Tran
+2.0] points of pass@1 at seed 0 and +0.0 [−2.7, +2.7] at seed 1 (95% intervals).
Run B’s exam is graded with the patched verifier, so these differences also con-
tain a grading offset: at seed 1 the identical round-0 generations already score
0.6 points higher in B, so the model part of the seed-1 difference is about −0.6.
Narrow intervals here bound the difference between two nearly identical trajec-
tories, not a patch effect. This null is uninformative, for two reasons we should
have checked before running it. First, the treatment is tiny: \dfrac appears in
20–29 of the 4,000 generations per round (0.50–0.73%), \tfrac never, and only
the correct ones among those are wrongly discarded; the kept pools of A and B
differ by 4 examples at seed 0 (872 vs 876) and 3 at seed 1 (833 vs 836), under
0.5% of the pool. Second, at 10−5 and the step count of these MATH-500 runs
the adapter changes the outputs little (Section E), so two nearly identical pools
would give nearly identical models whatever the verifier did. We cannot sepa-
rate these two explanations. The result is therefore: removing one rare format
defect had no detectable effect, which the prevalence count alone predicts; it is
not evidence about directional verifier bias in general, and it leaves untouched
the gold-storage defect, which rejects 15.5–18.4% of correct in-loop solutions in
both arms (Section B). Verifier-bias figures in the literature, such as the ∼14%
of [6], are likewise conditional on a reference distribution; what matters for a
loop is how often the affected forms occur in that loop’s own output, which is
cheap to count.
Pre-filter answer diversity. Over all problems of each run (in Design I the 500
selection and exam items together, not the exam alone) we also measured, before
filtering, the fraction of problems on which all k = 8 samples give the same
extracted answer, for Design P’s 1.5B run and the 10−5 Design I runs at seed 0.
It falls in every one: 24.8% →1.7% for Design P’s 1.5B run, 33.6% →16.0%
for Run C, 14.6% →12.0% (A) and 14.6% →12.2% (B). This agreement is
mechanically tied to accuracy (problems on which every sample is correct are all-
agreement problems) and to generations that hit the token cap, so it adds little
beyond the accuracy change and does not by itself rule out stylistic convergence,
which concerns how answers are written rather than which answer is given. The
fraction of distinct answers among the k samples, which we had planned as
the primary diversity measure, barely moves at 10−5 in the MATH-500 runs
(0.542 →0.554 for Run A, seed 0; 0.528 →0.543 for Run B, seed 1) but rises
for Run C (0.359 →0.500) and in Design P (0.443 →0.712). We report both for
completeness and draw no conclusion from them.