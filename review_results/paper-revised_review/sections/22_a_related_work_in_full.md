## A Related Work in Full
Self-training and its limits. STaR [19] introduced the generate–filter–retrain
loop, and ReST [12], ReST-EM [11] and RFT [17] formalise it; ReST-EM, which
like us restarts fine-tuning from the base model each iteration, reports dimin-
ishing test gains after the first round and a one-round regression on APPS.
ReST filters machine-translation samples with a learned reward model and a
rising threshold; the others filter by answer correctness. None of them mea-
sures how the filter’s errors depend on the form of the answer, and they mostly
use larger models than ours. Yue et al. [18] show that RL raises pass@1 while
the base model wins at large pass@k, and Teacher-Free Self-Training [13] ob-
serves a pass@8 versus pass@64 crossover on a free-verifier domain, concluding
that self-training “amplifies but does not compound”. Training repeatedly on
model-generated data erodes distribution tails [10], and Qiao et al. [8] argue
theoretically that a selector seeing only a narrow slice of the target distribution
accelerates collapse.
Verifier error. TinyV [16] measures that rule-based verifiers reject many correct
solutions and repairs them with an LLM check. From Accuracy to Robustness [6]
reports an average recall of 86% for rule-based verifiers, i.e. about 14% of correct
responses rejected, but for math-verify itself on their MATH subset a recall of
0.95 (about 5% false negatives; their Table 5, on DeepSeek-R1-Distill-Qwen-32B
outputs). Our MATH-500 audit gives 7.8% (95% Wilson interval 4.3–13.8%)
on another model’s solutions, a figure whose relation to the loop’s own rate is
not known (Section B), and a pipeline-specific defect alone rejects 15.5–18.4%
of the loop’s own solutions that a repaired verifier accepts. These figures dif-
fer in verifier version, solution source and denominator, so we compare them
only in order of magnitude. Imperfect Verifiers [1] gives the most formal noise
model, with fixed false-accept and false-reject probabilities, and notes that real
noise can depend on formatting but then assumes content-independent rates.
Egashira et al. [4] classify verifier errors in RLVR on a synthetic arithmetic task
(Qwen3-1.7B-Base and OLMo3-7B, with Qwen2.5-1.5B-Instruct, our model, in
an appendix) with hand-designed patterns such as format-based false negatives,
and find that systematic false negatives behave like random noise whereas false
positives (rewards given to answers that are near the truth, or that contain a
keyword) can cause plateau or collapse; they also note that a domain whose
queries are always rejected can at best plateau, which is the position of our
unparseable-gold problems. Our setting differs in paradigm (oﬄine rejection-
sampling SFT with a fresh adapter per round, not on-policy RL) and in task
(real benchmark problems). Our patch control cannot test their false-negative
finding, because it changes too little of the training pool (Section F), and the
much larger false-negative class we measured afterwards is present in both arms.
Nor does our no-filter control test their false-positive finding: their false positives
are systematic (a fixed wrong pattern that is always accepted), whereas no-filter
admits every sample, about two thirds of them incorrect in unstructured ways,

Mathematics or the Verifier?
17
under SFT with a 3–4× larger training dose. It did not end consistently worse
than the filtered run, which we report only as a related observation.
Auditing self-improvement. Xu et al. [15] audit three rounds of rank-32 LoRA
self-training of Qwen3-8B (η = 10−4; filters by answer match or majority vote,
plus a distillation arm from an external teacher as a positive control) against
a frozen untrained control, and identify seven measurement failures that each
invert a reported finding when its control is absent, including training-seed vari-
ance and a fixed token cap under style drift: their distillation arm, the most
effective one, scored as the most destructive because its truncation rate rose
from 16.5% to 65.3%. Self-training does not improve rarely-solved problems and
corrupts problems solved at baseline. This is the study closest to ours in spirit.
Our per-problem added/lost counts point the same way (more problems lost
than gained), though without their frozen control and with net counts that only
restate the change in pass@k (Section 3.4), and our adapters also drift in style
(longer outputs, fewer \boxed answers), and a fixed token cap matters in our
setting too: the untrained model already hits it in 41–48% of MATH-500 genera-
tions. Their finding is a warning that a decline under a fixed cap can be misread
as lost capability; this is why we separate finished accuracy from termination
and re-score at a larger cap (Section H). Their setup differs in model size, rank
and filters; we lack their per-round frozen arm (we re-score the untrained model
once, Section H) and a distillation arm, and we add a measured format-biased
verifier, a learning-rate series and reference-solution and no-filter controls.
Reference-guided training.
Kim et al. [7] show that self-distillation condi-
tioned on the ground-truth solution can cut mathematical accuracy by up to
40% (Qwen3-1.7B/8B, DeepSeek-Distill-Qwen-7B and Olmo3-7B-Instruct) while
shortening responses, which they trace to suppressed epistemic verbalization.
Our train-on-gold control is plain SFT on human reference solutions, not self-
distillation, so it is at most a loose analogue; it shows a similar surface signature
(shorter responses, lower accuracy) that may simply come from imitating terse
references. We did not measure epistemic markers.
Positioning. In the literature we surveyed (searched through October 2026) we
found no multi-round self-training study that uses a rule-based verifier with
a measured format bias together with a matched patched-verifier control; the
closest are Egashira et al. and Xu et al. Given that the patch turned out to
be too weak to test anything (Section F), we do not present this combination
as the contribution. The contribution is the absence of a detectable gain under
four pre-set measures with intervals, the description of what training at higher
rates changes, and the design lessons. Among these, what we did not find in
the surveyed studies is a test of verifier adaptation that does not depend on the
direction of accuracy: Xu et al. calibrate per-problem transition statistics against
a measured null, TinyV and Huang et al. measure false-reject rates to repair or
compare verifiers, and Egashira et al. inject hand-designed error patterns; none
of them, as far as we read, uses the verifier’s false-reject rate on the loop’s own

18
T. S. Nguyen and D. A. Tran
outputs, round by round, as a test of whether the model adapts to the verifier.
Section 5.3 proposes this test, with a decomposition of declines under a fixed
cap and two dose checks, as an audit protocol.