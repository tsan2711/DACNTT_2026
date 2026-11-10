   Run                      rt subset            R0 Last         ∆ 95% interval Pool
               −4
   A, 5 × 10        , seed 1 all                18.3     15.7 −2.6     [−5.3, 0.3]   3–5
                             boxed only         20.0     20.7 +0.7     [−2.9, 4.3]
                             aﬀected, parseable 92.8     87.2 −5.5    [−20.1, 6.3]
   A, 5 × 10−4 , seed 2 all                18.1          15.5 −2.6     [−5.2, 0.1]   2–3
                        boxed only         19.4          19.8 +0.4     [−2.8, 3.4]
                        aﬀected, parseable 95.1          93.5 −1.6    [−14.7, 9.5]
   A, 10−5 , seed 0         all                18.3      16.8 −1.5     [−2.9, 0.0] 9–12
                            boxed only         19.9      19.5 −0.4     [−2.0, 1.2]
                            aﬀected, parseable 92.3      92.0 −0.2     [−4.9, 4.6]
   Gold, seed 1             all                18.2      21.5 +3.3     [−1.2, 8.1]   —
                            boxed only         20.0      22.8 +2.8     [−2.0, 7.7]
                            aﬀected, parseable 95.5      94.7 −0.7     [−9.1, 6.2]
   Gold, seed 2             all                18.0      20.2 +2.1     [−2.2, 6.7]   —
                            boxed only         19.4      21.1 +1.7     [−3.3, 6.5]
                            aﬀected, parseable 95.1      97.6 +2.5    [−4.8, 11.9]
14     T. S. Nguyen and D. A. Tran

    (ii) Decompose declines under a ﬁxed cap. Report the change in sample ac-
curacy split into a ﬁnished-accuracy part and a cap-share part (Table ??, Sup-
plementary Appendix ??). Here the split is descriptive and its balance diﬀers by
partition: at 5 × 10−4 the cap share accounts for 12–30% of the decline in the
three original seed-1 runs and 52–72% at seed 2.
    (iii) Check the dose of a control before running it. Count how many training
examples the treatment changes. Our \dfrac patch changed 0–4 examples, while
the unvaried gold-storage defect would have changed about a ﬁfth to a quarter
of the pool (440 → 542 at round 0); the ﬁrst number alone shows the patch
control could not detect an eﬀect.
    (iv) Match training dose across designs. Our pooled design trained on about
4.5× more examples per round than the isolated one, so its sharp decline cannot
be attributed to pooling.
    Check (i) in RLVR. There a false reject gives the correct answer zero reward,
a direct pressure that SFT lacks, so the audit could be run on public RLVR
checkpoints with the conditioning above; we have not done so.


6    Limitations
Unequal training doses confound every cross-arm comparison, and the controls
are underpowered: the patch changes 0–4 training examples, and the no-ﬁlter
and train-on-gold controls have two seeds each. Intervals cover only problem
draw and sampling, not training-seed variance; several conditions have one seed,
and no multiplicity correction is applied. The learning-rate grid is coarse and
changes k, rounds, dose and metric along with the rate. The power is limited:
with 150 exam problems only gains of about 10 points of pass@1 would be
detected (6 with the 500 of Section 4.6, a single seed at one rate with k = 2
and two rounds). The adaptation audit is weak: 24–28 problems, 2–12 training
examples per round that could teach the avoidance, and no positive control. The
veriﬁer audit used other models’ solutions and inspected only rejections; the
gold-storage defect was measured afterwards and ran unvaried through every
run, and every headline number is graded by the biased veriﬁer that also selects
the data. Truncation: the 512-token cap binds from the start and truncates a
quarter of the pool in the main runs. Scope: one model family and size, one
veriﬁer, a restart-from-base design that leaves compounding little room, and
possible test-set contamination. No arm improves on round 0, and the gate on
reference solutions failed even with the corrected recipe, so we have no positive
reference showing that any recipe can help a 1.5B model here. Supplementary
Appendix ?? gives the full list.


7    Conclusion
We asked whether generate–verify–select–train iterations make a 1.5B model
better at mathematics or only teach it to write what a rule-based veriﬁer accepts.
On held-out exams the ﬁrst answer is no gain that this design could detect: no run
                                                  Mathematics or the Veriﬁer?        15

improves pass@1 or pass@k, though gains below about 10 and 8–10 points could
have been missed (6 in a ﬁnal 500-problem round, where pass@1 falls 4.8 points),
and the sample-accuracy bound of about 2.2 points is loose because it omits
training-seed variance. No arm improves, and training on reference solutions
lowers pass@1 by about 30 points even with a corrected recipe, so this is a null for
the recipe, not for self-training. The second question stays open: our pre-set rule
could only ﬁre if accuracy rose, and the post hoc \boxed share falls in a way that
imitation of the less-boxed pool and drift would both produce. A post hoc per-
round false-reject audit, carried over from RLVR, ﬁnds no sign that the model
learns to avoid one veriﬁer defect once the falling \boxed share is accounted
for, but with about 25 aﬀected problems, a handful of training examples per
round and no positive control it cannot rule such learning out. Most clearly at
the highest rate the model becomes less accurate on the solutions it does ﬁnish,
and more generations hit the token cap, clearly at one of two seeds. Patching
a rare veriﬁer defect and removing the ﬁlter made no diﬀerence of consistent
sign, neither control could have detected a small eﬀect, and a frequent defect in
our gold storage, which rejects about one in six correct solutions, ran unvaried
through every experiment. A sharp decline seen in an earlier pooled design does
not reproduce under isolation, and because that design also trained several times
longer per round we leave its cause open.
    A rising score, in self-training or in RLVR, does not by itself show that
a model learned mathematics rather than its veriﬁer. A per-round false-reject
audit asks part of that question whether accuracy rises or falls, but it must
be conditioned on answer format and on the problems where the defect can be
avoided, and it needs a positive control; applying it to public RLVR checkpoints,
where the pressure to adapt is direct, is a natural next step. A dose-matched
control for the gold-storage defect and a recipe that passes the positive gate
come ﬁrst (Supplementary Appendix ??).
Acknowledgments. This work was carried out as an undergraduate research project.
No external funding was received.

Disclosure of Interests. The authors have no competing interests to declare that
are relevant to the content of this article.

Code availability Code, saved generations and analysis scripts are at https://github.
com/tsan2711/DACNTT_2026.

Use of AI tools The authors used Claude (Anthropic), through Claude Code, to
help write and revise the manuscript, to write analysis and training scripts, and to run
automated paper reviews. The authors designed the study, ran the experiments and
take responsibility for the content.


References
 1. Cai, X.-Q., Wang, W., Liu, F., Liu, T., Niu, G., Sugiyama, M.: Reinforce-
    ment Learning with Veriﬁable yet Noisy Rewards under Imperfect Veriﬁers.
    arXiv:2510.00915 (2025)
16      T. S. Nguyen and D. A. Tran