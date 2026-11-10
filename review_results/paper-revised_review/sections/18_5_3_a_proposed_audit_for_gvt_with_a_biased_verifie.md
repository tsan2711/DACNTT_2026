### 5.3 A Proposed Audit for GVT with a Biased Verifier
Our pre-set reading rule failed in a predictable way: it tied “learning the verifier’s
style” to rising accuracy, so it could not speak once accuracy fell. From the
analyses we added after the runs we propose four checks for self-training with
a rule-based verifier. All four were defined post hoc here; we offer them as a
protocol for future studies, not as tested methods.
(i) A direction-free adaptation test. Fix a repaired verifier V ′ that corrects a
known defect class of the training verifier V . At each round t, on the loop’s own
generations, compute
rt = #{accepted by V ′ but rejected by V }
#{accepted by V ′}
.

Mathematics or the Verifier?
13
If the model learns to write what V accepts, rt should fall over rounds, whatever
happens to accuracy. For the gold-storage defect (Section 3.2) rt is 15.5–18.4%
in every round of the three runs we re-scored (Run A at 5×10−4, two seeds, and
at 10−5), with no downward trend; as a share of re-scored pass@1 it is 17% at
round 0 and round 2 at seed 1 and 20% throughout at 10−5 (Appendix B). This
covers one defect class, three runs and three to five rounds, with no interval on rt;
it rules out strong adaptation to this defect, not weak adaptation or adaptation
to others.
(ii) Decompose declines under a fixed cap. Report the change in sample ac-
curacy split into a finished-accuracy part and a cap-share part (Table 7). Here
the split moves the reading: at 5 × 10−4 the cap share accounts for 12–30% of
the decline at one seed and 52–72% at the other.
(iii) Check the dose of a control before running it. Count how many training
examples the treatment changes. Our \dfrac patch changed 0–4 examples, while
the unvaried gold-storage defect would have changed about a fifth of the pool
(440 →542 at round 0); the first number alone shows the patch control could
not detect an effect.
(iv) Match training dose across designs. Our pooled design trained on about
4.5× more examples per round than the isolated one, so its sharp decline cannot
be attributed to pooling.
Applying check (i) to RLVR. The test needs no training: only a set of check-
points, their generations on fixed problems, and a repaired verifier V ′. In RLVR
a false reject gives the correct answer zero reward, so a policy that adapts to V
should write the rejected form less often and rt should fall over training steps.
Given the gains of Section 2, and Shao et al.’s finding that even random rewards
raise accuracy [9], this is where the test would be most informative: a gain with
flat rt is evidence against adaptation to that defect, a gain with falling rt is
evidence for it. We have not run it on RL checkpoints.