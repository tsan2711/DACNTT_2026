# Mathematics or the Verifier? No Detectable Gain from

Mathematics or the Veriﬁer? No Detectable
Gain from Veriﬁer-Filtered Self-Training of a
1.5B Model
Tan Sang Nguyen1 and Duy Anh Tran1
Ton Duc Thang University, Ho Chi Minh City, Vietnam
52300057@student.tdtu.edu.vn, 52300006@student.tdtu.edu.vn
Abstract. Self-training and reinforcement learning with veriﬁable re-
wards report large gains for small language models, but a rising score
does not show that a model learned mathematics rather than what its
veriﬁer accepts. We study the cheapest form of the loop, generate–verify–
select–train with oﬄine LoRA SFT, on Qwen2.5-1.5B-Instruct with the
rule-based veriﬁer math-verify, on held-out MATH-500 and GSM8K ex-
ams (150 problems; 500 in a ﬁnal round) at four learning rates on MATH-
500 and two on GSM8K. No pass@1 or pass@k gain has a problem-level
bootstrap interval excluding zero; in the ﬁnal round, with a corrected
recipe, pass@1 falls 3.2–4.8 points in each of three seeds (mean −4.1).
The design detects only gains of about 10 points of pass@1 (6 in the
ﬁnal round; 80% power, intervals without seed variance, so likely more).
A positive gate fails: training on reference solutions lowers pass@1 by
32.2 points, so the null concerns this recipe and cannot show that self-
training fails. As a post hoc audit we track the share of the loop’s own
correct solutions that a storage defect in our pipeline rejects (about one
in six). It falls by 1.5–2.6 points with intervals reaching zero, matching
a falling \boxed share. Two injected-bias controls, one learnable from
the problem, show no selective avoidance, so the audit has no positive
control and is uninformative about adaptation. Two controls, patching
a rarer defect and removing the ﬁlter, show no consistent diﬀerence but
are dose-confounded or too small to detect one. Scores before the ﬁnal
round use the veriﬁer with the defect.
Keywords: self-training · self-improvement · veriﬁer bias · mathe-
matical reasoning · small language models · veriﬁable rewards · neg-
ative result.
1
Introduction
A common recipe for improving the mathematical reasoning of a small lan-
guage model (SLM) without human annotation is to let the model generate its
own solutions, keep those an automated veriﬁer judges correct, and ﬁne-tune on
them, for several rounds. We call this the Generate–Verify–Train (GVT) loop;
it underlies STaR [20], ReST [13], ReST-EM [12] and rejection-sampling ﬁne-
tuning [18]. But the veriﬁer never reads the reasoning: a rule-based veriﬁer such


2
T. S. Nguyen and D. A. Tran
as math-verify1 only extracts a ﬁnal answer and compares it with the gold, and
it rejects some correct answers written in forms it does not parse (Section 3.2).
The training signal is “was the ﬁnal string accepted”, not “were the steps right”.
The same gap runs through reinforcement learning with veriﬁable rewards
(RLVR), which reports large gains at this scale: GRPO on a single training
example lifts Qwen2.5-Math-1.5B from 36.0% to 73.6% on MATH-500 [15], a
gain whose authors report only 8.6 points beyond format correction, and similar
recipes improve DeepSeek-R1-Distill-Qwen-1.5B [3] and open base models from
0.5B up [21]. Yet Shao et al. [10] ﬁnd that GRPO with random rewards raises
Qwen2.5-Math-7B by 21.4 points on MATH-500, against 29.1 with ground-truth
rewards. A rising score therefore does not by itself show that a model has learned
to solve more problems, rather than to surface behaviour it already had or to
produce what its reward accepts. In RLVR, per-step false-negative rates on the
policy’s own rollouts have been tracked [4,17], and Egashira et al. report that,
for format-based false negatives, a policy ﬁrst unlearns the behaviour that trig-
gers them. This paper studies the question in the cheapest and most widely
used form of the loop, oﬄine rejection-sampling SFT, where a false reject only
removes a training example, and applies the same kind of per-round false-reject
measurement there, post hoc, for one defect of our pipeline.
We ask: after several GVT rounds, is the model better at mathematics, or
has it only learned to write what the veriﬁer accepts? We ﬁxed four measures
in advance: (i) pass@1; (ii) pass@k; (iii) output style, chieﬂy the share of gen-
erations containing \boxed; and (iv) per-problem transitions (problems added
and lost between rounds). The pre-set reading rule was that “learning the ver-
iﬁer’s style” requires pass@1 to rise, pass@k to stay ﬂat and style to converge
at once. In hindsight the rule is one-sided: it can only ﬁre when accuracy rises
(Section 5.1). The higher learning rates, the controls, the round count and k
at those rates, sample accuracy as primary measure, the termination measures
and the re-scoring for a second veriﬁer defect, and the ﬁnal 500-problem round
(Section 4.6) were all added after seeing earlier runs; all are post hoc.
We detect no improvement at any learning rate, though gains below about 10
points of pass@1 or 3.5–5.5 of sample accuracy could have been missed (intervals
omit training-seed variance, so these bounds are optimistic), and no arm of this
recipe improves, so the result concerns the recipe. The second branch is untested:
the pre-set rule is silent, no run varies the frequent veriﬁer defect, and the post
hoc audit of Section 5.3 is uninformative about whether the model learns to
avoid it. What appears, most clearly at the highest rate, is lower accuracy on
the solutions the model does ﬁnish. A sharp decline in a pooled design does not
reproduce under isolation (Section 4.1), and an isolated design at a learning rate
of 10−5 changed the outputs little (Section 4.2).
Contributions.
1 https://github.com/huggingface/math-verify, version 0.9.0 with antlr4 4.13.2 in this
work.