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
        rule-based veriﬁer math-verify, on a held-out exam of [N] problems at
        [K] learning rates on MATH-500 and GSM8K. No pass@1 or pass@k gain
        has a problem-level bootstrap interval excluding zero [UPDATE after
        new round]. The design detects only gains of about [MDE] points of
        pass@1 (80% power), and no arm, including training on reference solu-
        tions, improves on the untrained model, so this null concerns the recipe,
        not self-training in general. At the highest rate accuracy falls in every
        run. As a post hoc audit we track the share of the loop’s own correct
        solutions that a storage defect in our pipeline rejects (about one in six).
        It falls by [X] points, which a falling \boxed share accounts for, so we
        ﬁnd no adaptation to the defect but cannot exclude it. Two controls,
        patching a rarer defect and removing the ﬁlter, [RESULT].

        Keywords: self-training · self-improvement · veriﬁer bias · mathe-
        matical reasoning · small language models · veriﬁable rewards · neg-
        ative result.


1     Introduction
A common recipe for improving the mathematical reasoning of a small lan-
guage model (SLM) without human annotation is to let the model generate its
own solutions, keep those an automated veriﬁer judges correct, and ﬁne-tune on
them, for several rounds. We call this the Generate–Verify–Train (GVT) loop;
it underlies STaR [19], ReST [12], ReST-EM [11] and rejection-sampling ﬁne-
tuning [17]. But the veriﬁer never reads the reasoning: a rule-based veriﬁer such
as math-verify1 only extracts a ﬁnal answer and compares it with the gold, and
it rejects some correct answers written in forms it does not parse (Section 3.2).
The training signal is “was the ﬁnal string accepted”, not “were the steps right”.
1
    https://github.com/huggingface/math-verify, version 0.9.0 with antlr4 4.13.2 in this
    work.
2         T. S. Nguyen and D. A. Tran

    The same gap runs through reinforcement learning with veriﬁable rewards
(RLVR), which reports large gains at this scale: GRPO on a single training
example lifts Qwen2.5-Math-1.5B from 36.0% to 73.6% on MATH-500 [14], a
gain whose authors report only 8.6 points beyond format correction, and similar
recipes improve DeepSeek-R1-Distill-Qwen-1.5B [3] and open base models from
0.5B up [20]. Yet Shao et al. [9] ﬁnd that GRPO with random rewards raises
Qwen2.5-Math-7B by 21.4 points on MATH-500, against 29.1 with ground-truth
rewards. A rising score therefore does not by itself show that a model has learned
to solve more problems, rather than to surface behaviour it already had or to
produce what its reward accepts. In RLVR, per-step false-negative rates on the
policy’s own rollouts have been tracked [4,16], and Egashira et al. report that
a policy ﬁrst unlearns the behaviour that triggers false negatives. This paper
studies the question in the cheapest and most widely used form of the loop, oﬄine
rejection-sampling SFT, where a false reject only removes a training example,
and applies the same kind of per-round false-reject measurement there, post hoc,
for one defect of our pipeline.
    We ask: after several GVT rounds, is the model better at mathematics, or
has it only learned to write what the veriﬁer accepts? We ﬁxed four measures
in advance: (i) pass@1; (ii) pass@k; (iii) output style, chieﬂy the share of gen-
erations containing \boxed; and (iv) per-problem transitions (problems added
and lost between rounds). The pre-set reading rule was that “learning the veri-
ﬁer’s style” requires pass@1 to rise, pass@k to stay ﬂat and style to converge at
once. In hindsight the rule is one-sided: it can only ﬁre when accuracy rises (Sec-
tion 5.1). Only these measures and the rule were ﬁxed in advance. The higher
learning rates, the controls, the round count and k at those rates, sample ac-
curacy as primary measure, the termination measures and the re-scoring for a
second veriﬁer defect were all chosen after seeing earlier runs; we mark them as
post hoc.
    Our answer is negative on the ﬁrst branch, within the power of the design: we
detect no improvement on held-out problems at any learning rate we tried, but
gains below about 10 points of pass@1 or 3.5–5.5 of sample accuracy could have
been missed, and no arm of this recipe improves at all. On the second branch
the pre-set rule is silent. The post hoc audit of Section 5.3 ﬁnds no sign that
the model learns to avoid one veriﬁer defect, but it has little power to see such
learning. What appears, most clearly at the highest rate, is lower accuracy on
the solutions the model does ﬁnish and, clearly at only one of two seeds, more
generations that run out of tokens. Two earlier readings did not hold up, and
we report why: a pooled design whose sharp decline did not reproduce under
isolation (Section 4.1), and an isolated design at a learning rate that changed
the outputs little (Section 4.2).

Contributions.

    – For a 1.5B model, LoRA SFT and one rule-based veriﬁer, no gain is de-
      tectable on a held-out exam at any learning rate we tried, with problem-level
      bootstrap intervals and the smallest eﬀects the design could detect. No arm
                                              Mathematics or the Veriﬁer?       3

   improves, not even training on reference solutions, so this is a null for the
   recipe, not for self-training.
 – A post hoc per-round false-reject audit of one veriﬁer defect, carried over
   from RLVR [4,16] to oﬄine SFT self-training. The rejected share falls by
   1.5–2.6 points, which a falling \boxed share accounts for, and is ﬂat on the
   aﬀected problems; the test has little power and no positive control (Sec-
   tion 5.3).
 – A decomposition of an accuracy decline under a ﬁxed token cap into a
   ﬁnished-accuracy part and a cap-share part: at the highest rate, ﬁnished
   generations lose 5.5–10.6 points against the untrained model on the same
   problem mix, and the cap-hit share rises only at that rate.


2   Related Work

Self-training and its limits. STaR [19] introduced the generate–ﬁlter–retrain
loop, and ReST [12], ReST-EM [11] and RFT [17] formalise it; ReST-EM, which
like us restarts from the base model each iteration, reports diminishing gains af-
ter the ﬁrst round. None measures how the ﬁlter’s errors depend on the form of
the answer. Yue et al. [18] show that RL raises pass@1 while the base model wins
at large pass@k, and Teacher-Free Self-Training [13] concludes that self-training
“ampliﬁes but does not compound”. Training repeatedly on model-generated
data erodes distribution tails [10], and a narrow selector can accelerate col-
lapse [8].