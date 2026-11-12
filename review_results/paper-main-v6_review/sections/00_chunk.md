# Mathematics or the Verifier? A Null Result for One Verifier-Filtered Self-Training Recipe on a 1.5B Model

Mathematics or the Veriﬁer? A Null Result for
One Veriﬁer-Filtered Self-Training Recipe on a
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
bootstrap interval excluding zero; in the ﬁnal round, with a revised (not
validated) recipe, pass@1 falls 3.2–4.8 points in each of three seeds (mean
−4.1; two of three intervals exclude zero). The design detects only gains
of about 10 points of pass@1 (6 in the ﬁnal round; 80% power, inter-
vals without seed variance, so likely more). A positive gate fails: training
on reference solutions lowers pass@1 by 32.2 points, which we did not
diagnose (a pipeline defect would also produce it), so the null concerns
this recipe only and cannot show that self-training fails. Accuracies are
graded by the veriﬁer that selects the data (the ﬁnal round also by a
string-match grader), so neither the mathematics nor the veriﬁer ques-
tion is answered. As a post hoc audit we track the share of the loop’s
own correct solutions that a storage defect in our pipeline rejects (about
one in six). It falls by 1.5–2.6 points with intervals reaching zero; this fall
is tied to the falling \boxed share by an identity, so it is no evidence of
adaptation. Two injected-bias runs, one whose rule is visible in the gold
answer, show no selective avoidance but are not valid positive controls
(one cannot elicit avoidance by construction, the other is a single run
without rt), so the audit is uninformative about adaptation. Two con-
trols, patching a rarer defect and removing the ﬁlter, show no consistent
diﬀerence (no ﬁlter is lower on pass@k, at 3–4× the dose) but are dose-
confounded or too small to detect one. Scores before the ﬁnal round use
the veriﬁer with the defect.
Keywords: self-training · self-improvement · veriﬁer bias · mathe-
matical reasoning · small language models · veriﬁable rewards · null
result.


2
T. S. Nguyen and D. A. Tran
1
Introduction
A common recipe for improving the mathematical reasoning of a small lan-
guage model (SLM) without human annotation is to let the model generate its
own solutions, keep those an automated veriﬁer judges correct, and ﬁne-tune on
them, for several rounds. We call this the Generate–Verify–Train (GVT) loop;
it underlies STaR [19], ReST [12], ReST-EM [11] and rejection-sampling ﬁne-
tuning [17]. But the veriﬁer never reads the reasoning: a rule-based veriﬁer such
as math-verify1 only extracts a ﬁnal answer and compares it with the gold, and
it rejects some correct answers written in forms it does not parse (Section 3.2).
The training signal is “was the ﬁnal string accepted”, not “were the steps right”.
The same gap runs through reinforcement learning with veriﬁable rewards
(RLVR), which reports large gains at this scale [14,3,20], though only 8.6 of one
study’s 37.6 points lie beyond format correction. Shao et al. [9] ﬁnd that GRPO
with random rewards raises Qwen2.5-Math-7B by 21.4 points on MATH-500,
against 29.1 with ground-truth rewards. A rising score therefore does not by itself
show that a model has learned to solve more problems, rather than to surface
behaviour it already had or to produce what its reward accepts. In RLVR, per-
step false-negative rates on the policy’s own rollouts have been tracked [4,16];
we study the question in a cheap and common form of the loop, oﬄine rejection-
sampling SFT, where a false reject removes a training example (and, if bound to
a problem, the problem), and apply a per-round false-reject measurement there,
post hoc, for one defect of our pipeline.
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
omit training-seed variance), and no arm of this recipe improves, so the result
concerns the recipe. The second branch is untested: no run varies the frequent
veriﬁer defect, scores are graded by the selecting veriﬁer (one string-match check
on the ﬁnal round), and the post hoc audit of Section 5.3 is uninformative about
adaptation. What appears, most clearly at the highest rate, is lower accuracy
on the solutions the model does ﬁnish, though on one seed the cap share carries
more of it (Section 4.5). A sharp pooled decline is absent in the isolated runs at
1 https://github.com/huggingface/math-verify, version 0.9.0 with antlr4 4.13.2 in this
work.