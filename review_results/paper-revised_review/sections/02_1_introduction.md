## 1 Introduction
A common recipe for improving the mathematical reasoning of a small lan-
guage model (SLM) without human annotation is to let the model generate its
own solutions, keep those an automated verifier judges correct, and fine-tune on
them, for several rounds. We call this the Generate–Verify–Train (GVT) loop;
it underlies STaR [19], ReST [12], ReST-EM [11] and rejection-sampling fine-
tuning [17]. But the verifier never reads the reasoning: a rule-based verifier such

2
T. S. Nguyen and D. A. Tran
as math-verify1 only extracts a final answer and compares it with the gold, and
it rejects some correct answers written in forms it does not parse (Section 3.2).
The training signal is “was the final string accepted”, not “were the steps right”.
The same gap runs through reinforcement learning with verifiable rewards
(RLVR), which reports large gains at this scale: GRPO on a single training ex-
ample lifts Qwen2.5-Math-1.5B from 36.0% to 73.6% on MATH-500 [14], and
similar recipes improve DeepSeek-R1-Distill-Qwen-1.5B [3] and open base mod-
els from 0.5B up [20]. Yet Shao et al. [9] find that GRPO with random rewards
raises Qwen2.5-Math-7B by 21.4 points on MATH-500, against 29.1 with ground-
truth rewards. A rising score therefore does not by itself show that a model has
learned to solve more problems, rather than to surface behaviour it already had
or to produce what its reward accepts. What is missing is a test that separates
“better at mathematics” from “better at what the verifier accepts” and that
does not presuppose that accuracy rises. This paper studies that question in the
cheapest and most widely used form of the loop, oﬄine rejection-sampling SFT,
and proposes such a test.
We ask: after several GVT rounds, is the model better at mathematics, or
has it only learned to write what the verifier accepts? We fixed four measures in
advance: (i) pass@1; (ii) pass@k; (iii) output style, chiefly the share of generations
containing \boxed; and (iv) per-problem transitions (problems added and lost
between rounds). The pre-set reading rule was that “learning the verifier’s style”
requires pass@1 to rise, pass@k to stay flat and style to converge at once. In
hindsight the rule is one-sided: it can only fire when accuracy rises (Section 5.1).
Measures of termination and the re-scoring for a second verifier defect were
added after the runs; we mark them as post hoc.
Our answer is negative on the first branch. On the second, the pre-set rule
is silent, and the test we propose in its place (Section 5.3) answers it for one
verifier defect: the model does not learn to avoid it. We detect no improvement
on held-out problems at any learning rate we tried. What appears, most clearly
at the highest rate, is lower accuracy on the solutions the model does finish and
more generations that run out of tokens. Two earlier readings did not hold up,
and we report why: a pooled design whose sharp decline did not reproduce under
isolation (Section 4.1), and an isolated design at a learning rate that changed
the outputs little (Section 4.2).
Contributions.
– A test of verifier adaptation that does not depend on the direction of accu-
racy (defined post hoc, Section 5.3): per round, the share of the loop’s own
correct solutions that a known verifier defect rejects. A model that learns
to write what the verifier accepts should drive this share down, whether ac-
curacy rises or falls. The test needs only each checkpoint’s generations and
a repaired verifier, so it applies to RLVR as well as to SFT. For the one
1 https://github.com/huggingface/math-verify, version 0.9.0 with antlr4 4.13.2 in this
work.

Mathematics or the Verifier?
3
frequent defect we measured it stays at about one in six in every round of
three runs, so for that defect the model does not adapt.
– For a 1.5B model, LoRA SFT and one rule-based verifier, no gain is de-
tectable on a held-out exam at four learning rates on MATH-500 or two on
GSM8K, with problem-level bootstrap intervals for every comparison.
– An observation on style with its limits: the \boxed share falls under self-
training in a way that cannot tell imitation of the pool from drift; the one
strong style convergence occurs when training on reference solutions, with
no verifier in the loop.
– A decomposition of an accuracy decline under a fixed token cap into a
finished-accuracy part and a cap-share part, applied post hoc to what train-
ing at the highest rate changes: finished generations lose 5.5–10.6 points
against the untrained model on the same problems, and the cap-hit share
rises only at that rate.
– Design lessons: a verifier-patch control whose treatment changes 0–4 training
examples cannot detect an effect, while a second, unvaried defect rejects
about one in six correct solutions; and pooled and isolated designs differ in
training dose as well as in the variables we meant to vary.