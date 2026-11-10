### 4.1 Design P: An Apparent Collapse
In the pooled design the 1.5B model declines severely and with acceleration
(pass@1 50.0% →18.6%, pass@8 72.6% →48.6%; Table 2), on both datasets
(Table 9); the 0.5B decline is small. The accepted pool contracts every round
and \boxed{} falls from 5,608 to 2,693 of 8,000 generations. This design cannot
be read causally: one adapter trains on both datasets’ pools; it scores on the
problems it selects from; and it trains on about 4.5× as many examples per
round as the isolated MATH-500 run (3,962 against 872 at round 0). Selection-
set scoring is unlikely to have masked a decline (in Design I the selection problems
fall as much as the exam), and dose explains at most the level of the decline,
not its acceleration under shrinking pools. No run separates these explanations
(Appendix D).
Table 2. Design P: pass@1 and pass@8 over five GVT rounds, pooled GSM8K +
MATH-500, scored on the selection set. Round 0 is the untrained base model. Sec-
tion 4.1 explains why these numbers cannot be attributed to any single cause.
Model Metric
R0
R1
R2
R3
R4
∆(R0→R4)
0.5B
pass@1 31.1% 31.9% 29.9% 28.9% 27.4%
−3.7 pt
0.5B
pass@8 60.5% 58.9% 56.1% 55.5% 54.9%
−5.6 pt
1.5B
pass@1 50.0% 46.2% 44.5% 32.4% 18.6%
−31.4 pt
1.5B
pass@8 72.6% 71.5% 70.2% 63.6% 48.6%
−24.0 pt