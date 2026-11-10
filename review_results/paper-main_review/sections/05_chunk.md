Table 4. The false-reject audit for the gold-storage defect (post hoc), in percent (all 500
problems), round 0 → last round, with the change and a 95% problem-level bootstrap
interval (2,000 resamples). “Boxed only” restricts to predictions containing \boxed;
“aﬀected, parseable” to problems where the defect ever ﬁres and V can parse the gold.
Pool: examples per round from aﬀected problems that V accepts (and so avoid the
defect).

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



(440 → 542 at round 0); the ﬁrst number alone shows the patch control could
not detect an eﬀect.
    (iv) Match training dose across designs. Our pooled design trained on about
4.5× more examples per round than the isolated one, so its sharp decline cannot
be attributed to pooling.
    Check (i) in RLVR. There a false reject gives the correct answer zero reward,
a direct pressure that SFT lacks, and Egashira et al. already observe the policy
unlearning behaviour that triggers false negatives. The audit needs only check-
points, their generations on ﬁxed problems and a repaired veriﬁer, so it can be
run on public RLVR checkpoints, with the conditioning above; we have not done
so.


6     Limitations
Unequal training doses confound every cross-arm comparison. The controls are
underpowered: the patch changes 0–4 training examples, and the no-ﬁlter and
train-on-gold controls have two seeds each. Intervals cover only problem draw
and sampling, not training-seed variance; several conditions have one seed, and
no multiplicity correction is applied. The learning-rate grid is coarse, with three
rounds and k = 4, and it changes k, rounds, dose and metric along with the rate.
14     T. S. Nguyen and D. A. Tran

The power is limited: with 150 exam problems only gains of about 10 points of
pass@1 or 3.5–5.5 of sample accuracy would be detected. The adaptation audit
is weak: 24–28 problems, 2–12 training examples per round that could teach the
avoidance, and no positive control. Cap-hit is reconstructed from decoded text.
The veriﬁer audit used other models’ solutions and inspected only rejections;
the gold-storage defect was measured afterwards and ran unvaried through every
run. Every headline number is graded by the biased veriﬁer that also selects the
data. The 512-token cap binds from the start, and the equal training limit, which
includes the prompt, truncates a quarter of the pool. Scope: one model family
(Qwen2.5) and one size in Design I, one veriﬁer, one LoRA recipe with loss over
the prompt, a restart-from-base design that leaves compounding little room,
and possible test-set contamination. No arm improves on round 0, so we have
no positive reference showing this recipe can help a 1.5B model. Supplementary
Appendix ?? gives the full list.


7    Conclusion

We asked whether generate–verify–select–train iterations make a 1.5B model bet-
ter at mathematics or only teach it to write what a rule-based veriﬁer accepts.
On a held-out exam, the ﬁrst answer is no gain that this design could detect: on
pass@1 and pass@k, the pre-set accuracy measures, no run improves detectably,
though gains below about 10 and 8–10 points could have been missed; the in-
tervals for sample accuracy (a primary measure chosen after the runs) exclude
gains above about 2.2 points, a loose bound because they omit training-seed
variance and are not an equivalence test. No arm improves, including training
on reference solutions, so this is a null for the recipe. The second question stays
open, because our pre-set rule for it could only ﬁre if accuracy rose, and the post
hoc \boxed share falls in a way that imitation of the less-boxed training pool and
drift would both produce. A post hoc per-round false-reject audit, carried over
from RLVR, ﬁnds no sign that the model learns to avoid one veriﬁer defect once
the falling \boxed share is accounted for, but with about 25 aﬀected problems,
a handful of training examples per round and no positive control it cannot rule
such learning out. In a post hoc description, most clearly at the highest rate, the
model becomes less accurate on the solutions it does ﬁnish; more generations
hit the token cap only at the highest rate, and clearly only at one of its two
seeds, where the change in cap-hit share accounts for 12–30% of the decline in
the original seed-1 runs and 52–72% at seed 2; a character-length heuristic we
ﬁrst used overstated that part. Reference-solution training degrades the model
more, with much shorter answers. Patching a rare veriﬁer defect and removing
the ﬁlter made no diﬀerence of consistent sign across measures and seeds (pass@1
ﬂips sign between seeds; removing the ﬁlter lowers pass@4 at both seeds, within
noise; single-seed intervals sometimes exclude zero), neither control could have
detected a small eﬀect, and a frequent defect in our gold storage, which rejects
about one in six correct solutions, ran unvaried through every experiment. A
sharp decline seen in an earlier pooled design does not reproduce under isolation
                                                  Mathematics or the Veriﬁer?        15

and held-out scoring, and because that design also trained several times longer
per round, we leave its cause open. We report the earlier readings that did not
hold up because the designs that produced them are common.
   A rising score, in self-training or in RLVR, does not by itself show that
a model learned mathematics rather than its veriﬁer. A per-round false-reject
audit asks part of that question whether accuracy rises or falls, but our data
show it must be conditioned on answer format and on the problems where the
defect can be avoided, and it needs a positive control; applying it so to public
RLVR checkpoints, where the pressure to adapt is direct, is a natural next step.
Future work, including a dose-matched control for the gold-storage defect, is
outlined in Supplementary Appendix ??.

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