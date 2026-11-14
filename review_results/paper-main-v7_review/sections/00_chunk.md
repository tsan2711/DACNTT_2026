# Mathematics or the Verifier? A Null Result for One Verifier-Filtered Self-Training Recipe on a 1.5B Model

Mathematics or the Veriﬁer? A Null Result for
One Veriﬁer-Filtered Self-Training Recipe on a
1.5B Model
Dinh-Hong Vu1 , Tan Sang Nguyen2 , and Duy Anh Tran2
1

Natural Language Processing and Knowledge Discovery Research Group, Faculty of
Information Technology, Ton Duc Thang University, Ho Chi Minh City, Vietnam
2
Faculty of Information Technology, Ton Duc Thang University, Ho Chi Minh City,
Vietnam
vudinhhong@tdtu.edu.vn, 52300057@student.tdtu.edu.vn,
52300006@student.tdtu.edu.vn
Corresponding author: 52300057@student.tdtu.edu.vn (Tan Sang Nguyen)

Abstract. Self-training and reinforcement learning with veriﬁable rewards report large gains for small language models, but a rising score
does not show that a model learned mathematics rather than what its
veriﬁer accepts. We study the cheapest form of the loop, generate–verify–
select–train with oﬄine LoRA SFT, on Qwen2.5-1.5B-Instruct with the
rule-based veriﬁer math-verify, on held-out MATH-500 and GSM8K exams (150 problems; 500 in a ﬁnal round). No pass@1 or pass@k gain at
any of four learning rates has a problem-level bootstrap interval excluding zero; in the ﬁnal round, with a revised recipe, pass@1 falls 3.2–4.8
points in each of three seeds (mean −4.1). The design detects only gains
of about 10 points of pass@1 (6 in the ﬁnal round). A positive gate fails:
training on reference solutions lowers pass@1 by 32.2 points. The boxed
share is unchanged (90.6 → 90.3%) while accuracy among boxed answers
falls (48.5 → 17.1%) and solutions shorten 3.2×, so the model imitates
terse references and loses reasoning, which makes the gate a weak control.
The null therefore concerns this recipe only. All runs are graded by one
patched veriﬁer and a string-match check, so neither the mathematics
nor the veriﬁer question is answered; a post hoc audit of a gold-storage
defect (about one in six correct solutions rejected) is uninformative about
adaptation.
Keywords: self-training · self-improvement · veriﬁer bias · mathematical reasoning · small language models · veriﬁable rewards · null
result.

1

Introduction

A common recipe for improving the mathematical reasoning of a small language model (SLM) without human annotation is to let the model generate its
own solutions, keep those an automated veriﬁer judges correct, and ﬁne-tune on

2

D.-H. Vu et al.

them, for several rounds. We call this the Generate–Verify–Train (GVT) loop;
it underlies STaR [19], ReST [12], ReST-EM [11] and rejection-sampling ﬁnetuning [17]. But the veriﬁer never reads the reasoning: a rule-based veriﬁer such
as math-verify3 only extracts a ﬁnal answer and compares it with the gold, and
it rejects some correct answers written in forms it does not parse (Section 3.2).
The training signal is “was the ﬁnal string accepted”, not “were the steps right”.
The same gap runs through reinforcement learning with veriﬁable rewards
(RLVR): only 8.6 of one study’s 37.6 points lie beyond format correction [14],
and GRPO with random rewards raises Qwen2.5-Math-7B by 21.4 points on
MATH-500, against 29.1 with ground-truth rewards [9]. A rising score does not
by itself show that a model learned to solve more problems rather than to surface
behaviour it had or to produce what its reward accepts. We study the question
in a cheap and common form of the loop, oﬄine rejection-sampling SFT, where
a false reject removes a training example, and apply a per-round false-reject
measurement there, post hoc, for one defect of our pipeline.
We ask: after several GVT rounds, is the model better at mathematics, or has
it only learned to write what the veriﬁer accepts? We ﬁxed four measures in advance: (i) pass@1; (ii) pass@k; (iii) output style, chieﬂy the share of generations
containing \boxed; and (iv) per-problem transitions (problems added and lost
between rounds). The pre-set reading rule was that “learning the veriﬁer’s style”
requires pass@1 to rise, pass@k to stay ﬂat and style to converge at once. In
hindsight the rule is one-sided: it can only ﬁre when accuracy rises (Section 5.1).
The higher learning rates, the controls, sample accuracy as primary measure,
the termination measures, the re-scoring and the ﬁnal 500-problem round (Section 4.6) were added after seeing earlier runs; all are post hoc.
We detect no improvement at any learning rate, though gains below about 10
points of pass@1 or 4–6.5 of sample accuracy could have been missed (intervals
omit training-seed variance), and no arm of this recipe improves, so the result
concerns the recipe. The second branch is untested: no run varies the frequent
veriﬁer defect, scores are graded by a veriﬁer of the selecting family (V ′ , with
a string-match check), and the post hoc audit of Section 5.3 is uninformative
about adaptation. Most clearly at the highest rate, accuracy falls on the solutions the model does ﬁnish, though on one seed the cap share carries more of
it (Section 4.5). A sharp pooled decline is absent in the isolated runs at 10−5 ,
which train on about 4.5× fewer examples; dose and pooling are confounded.
Contributions.
– For a 1.5B model, LoRA SFT and one rule-based veriﬁer, no gain is detectable on a held-out exam at any learning rate we tried (a coarse grid that
also changes k and rounds), with bootstrap intervals and the smallest eﬀects
the design could detect. No arm improves, not even training on reference
solutions, so this is a null for the recipe, not a statement about self-training.
3

https://github.com/huggingface/math-verify, version 0.9.0 with antlr4 4.13.2 in this
work.

Mathematics or the Veriﬁer?

3