## J Limitations in Full
1. Unequal training doses. With one epoch and batch size 2, optimizer steps
are half the pool size: round 0 takes about 1,981 steps (inferred) in Design P,
436 in Run A and 951 in Run C at 10−5, 220 in Run A at 5 × 10−4, 700 for
no-filter and 175 for train-on-gold. Every cross-arm comparison mixes the
intended variable with dose, and the cause of the Design P decline is not
identified.
2. Underpowered controls. The patch changes 0–4 training examples; at 10−5
the adapter also changes the outputs little. Its null is expected whatever the
truth, and we report no equivalence bound. The no-filter and train-on-gold
controls have two seeds each.
3. Intervals cover only part of the uncertainty. The bootstrap intervals cover
problem draw and generation sampling, not training-seed variance. Most

34
T. S. Nguyen and D. A. Tran
conditions have two or three seeds; the following have one: Run C at both
rates, the truncation check (one replicate pair at 5×10−4 and one run with a
1024-token training limit), and each token-cap re-scoring. pass@1 is a single
draw per problem.
4. Learning rate. The original 10−5 was an untuned default; the evidence that it
changes outputs little is behavioural (unchanged length and cap-hit share),
since its loss does fall. The higher-rate grid is coarse and uses three rounds
and k = 4.
5. Cap-hit is reconstructed: token counts were not saved, so we re-tokenise the
decoded text and count a generation as a cap hit at ≥508 of 512 tokens. The
token-cap re-scorings saved only summary statistics, so their termination
figures still rest on the character proxy, which we show undercounts cap
hits.
6. Verifier measurements. The false-negative audit used other models’ solu-
tions and a scripted correctness check, inspected only rejections (so no false-
positive rate). The gold-storage defect was measured afterwards on the loop’s
own outputs by re-scoring (Section B); it lowers absolute pass@1 by 4.7–8.0
points in the three self-training runs we re-scored (other runs are extrapo-
lation), was present in every run including both arms of the patch control,
and was never varied in a training run. It overlaps with the unparseable-gold
correction (46 of the 51 unparseable golds become parseable once boxed), so
the two corrections must not be added. The re-scored false-negative share
assumes the re-scored verifier makes no false accepts.
7. Restart-from-base design and scope. A fresh adapter on the base model each
round leaves compounding little room, so the absence of compounding is
partly a property of the design. One model size in Design I, one verifier, one
training method, at most five rounds; full fine-tuning, continued training and
online RL are untested.
8. The selecting verifier also grades. The same math-verify configuration that
chooses the training data scores the exam, so any systematic verifier error
enters both selection and measurement. The gold-storage re-score (Section B)
and the string audit of the train-on-gold runs bound part of this, but only
for five runs and one defect class.
9. A binding token cap. At 512 tokens the untrained model already fails to fin-
ish 41–48% of MATH-500 generations (depending on the seed’s exam split),
so every measure is taken in a regime where length and accuracy are entan-
gled, and the 512-token training limit truncates about a quarter of the kept
pool. Our conclusions are about this regime; a larger cap during the loop is
untested.
10. No equivalence margin and many intervals. We did not fix in advance how
small a gain would count as “no gain”, so the 2.2-point bound is read off
the observed intervals. Table 5 alone holds 76 intervals and the text reports
about ten more, none with a multiplicity correction. They are not indepen-
dent (they share runs and problems), so “about four would exclude zero by
chance” is only a rough guide, but single intervals that only just exclude zero
should be read cautiously.

Mathematics or the Verifier?
35
11. Possible test-set contamination. MATH-500 and GSM8K are public and may
be in Qwen2.5’s training data. This would raise absolute accuracy, and it
need not affect all arms or rounds alike: if training on self-generated solutions
makes the model forget memorised items, part of a within-run decline could
be loss of memorisation rather than of skill. We did not test it.
12. Training recipe. The loss covers the prompt as well as the response, and we
tried one LoRA configuration (rank 16 on query and value projections). Both
could matter, most plausibly for the train-on-gold collapse, and neither was
varied. No arm in any design improves detectably on its round 0, including
training on reference solutions, so we have no positive reference showing that
this recipe can help a 1.5B model at all; the declines may partly reflect the
recipe rather than self-training.