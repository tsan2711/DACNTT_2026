
Mathematics or the Veriﬁer?
15
about 10 and 8–10 points could have been missed (6 in a ﬁnal 500-problem round,
where pass@1 falls 3.2–4.8 points in all three seeds), and the sample-accuracy
ﬁgure of about 2.2 points is a post hoc upper limit, not a power statement,
that omits training-seed variance. No arm improves, and training on reference
solutions lowers pass@1 by about 30 points even with a corrected recipe, so
this is a null for the recipe, and the failed gate means it says little about self-
training. The second question stays open: our pre-set rule could only ﬁre if
accuracy rose. A post hoc per-round false-reject audit, carried over from RLVR,
is uninformative about whether the model learns to avoid one veriﬁer defect: its
fall matches the falling \boxed share, which adaptation would also produce, and
with about 25 aﬀected problems, a handful of training examples per round and
two injected-bias controls that showed no selective avoidance, it has little power.
At the highest rate the model is less accurate on the solutions it ﬁnishes. Patching
a rare veriﬁer defect and removing the ﬁlter made no consistent diﬀerence, but
neither control could detect a small one. The pooled design’s decline does not
reproduce under isolation.
A per-round false-reject audit asks part of the question whether accuracy
rises or falls, but it must be conditioned on answer format and on the problems
where the defect can be avoided, and it needs a positive control. A dose-matched
control for the gold-storage defect and a recipe that passes the positive gate come
ﬁrst (Supplementary Appendix K).
Acknowledgments. This work was carried out as an undergraduate research project.
No external funding was received.
Disclosure of Interests. The authors have no competing interests to declare that
are relevant to the content of this article.
Code availability Code, saved generations and analysis scripts are at https://github.
com/tsan2711/DACNTT_2026 (tag paper-2026-11). Generation-time token counts,
Design P’s training logs and the 1,536-token re-scoring outputs were not saved.
Use of AI tools The authors used Claude (Anthropic), through Claude Code, to help
write the manuscript, the analysis and training scripts, and to run automated reviews.
The authors designed the study, ran the experiments and take responsibility for the
content.
References
1. Cai, X.-Q., Wang, W., Liu, F., Liu, T., Niu, G., Sugiyama, M.: Reinforce-
ment Learning with Veriﬁable yet Noisy Rewards under Imperfect Veriﬁers.
arXiv:2510.00915 (2025)
2. Cobbe, K., Kosaraju, V., Bavarian, M., Chen, M., Jun, H., Kaiser, L., Plappert,
M., Tworek, J., Hilton, J., Nakano, R., Hesse, C., Schulman, J.: Training Veriﬁers
to Solve Math Word Problems. arXiv:2110.14168 (2021)
3. Dang, Q.-A., Ngo, C.: Reinforcement Learning for Reasoning in Small LLMs: What
Works and What Doesn’t. arXiv:2503.16219 (2025)


16
T. S. Nguyen and D. A. Tran
4. Egashira, K., Vero, M., Dekoninck, J., Dörner, F.E., Staab, R., Vechev, M.: Delay,
Plateau, or Collapse: Evaluating the Impact of Systematic Veriﬁcation Error on
RLVR. arXiv:2605.02909 (2026)
5. Hendrycks, D., Burns, C., Kadavath, S., Arora, A., Basart, S., Tang, E., Song,
D., Steinhardt, J.: Measuring Mathematical Problem Solving With the MATH
Dataset. arXiv:2103.03874 (2021)
6. Huang, Y., Zeng, W., Zeng, X., Zhu, Q., He, J.: From Accuracy to Robust-
ness: A Study of Rule- and Model-based Veriﬁers in Mathematical Reasoning.
arXiv:2505.22203 (2025)
7. Lightman, H., Kosaraju, V., Burda, Y., Edwards, H., Baker, B., Lee, T., Leike, J.,
Schulman, J., Sutskever, I., Cobbe, K.: Let’s Verify Step by Step. arXiv:2305.20050
(2023)
8. Kim, J., Luo, X., Kim, M., Lee, S., Kim, D., Jeon, J., Li, D., Yang, Y.: Why
Does Self-Distillation (Sometimes) Degrade the Reasoning Capability of LLMs?
arXiv:2603.24472 (2026)
9. Qiao, X., Du, X., Liu, W., Zhang, J., Mai, P., Zhang, M., Pang, Y.: When Sample
Selection Bias Precipitates Model Collapse. arXiv:2606.13732 (2026)
10. Shao, R., Li, S.S., Xin, R., Geng, S., Wang, Y., Oh, S., Du, S.S., Lambert, N., Min,
S., Krishna, R., Tsvetkov, Y., Hajishirzi, H., Koh, P.W., Zettlemoyer, L.: Spurious
Rewards: Rethinking Training Signals in RLVR. arXiv:2506.10947 (2025)
11. Shumailov, I., Shumaylov, Z., Zhao, Y., Papernot, N., Anderson, R., Gal, Y.: AI
models collapse when trained on recursively generated data. Nature (2024). https:
//doi.org/10.1038/s41586-024-07566-y
12. Singh, A., Co-Reyes, J.D., Agarwal, R., et al.: Beyond Human Data: Scaling Self-
Training for Problem-Solving with Language Models. arXiv:2312.06585 (2023)
13. Gulcehre, C., Le Paine, T., Srinivasan, S., et al.: Reinforced Self-Training (ReST)
for Language Modeling. arXiv:2308.08998 (2023)
14. Strozzi, I.L.: Teacher-Free Self-Training Ampliﬁes but Does Not Compound: A
Pass@k Crossover on a Free-Veriﬁer Domain. arXiv:2606.07856 (2026)
15. Wang, Y., Yang, Q., Zeng, Z., Ren, L., Liu, L., Peng, B., Cheng, H., He, X., Wang,
K., Gao, J., Chen, W., Wang, S., Du, S.S., Shen, Y.: Reinforcement Learning for
Reasoning in Large Language Models with One Training Example. In: NeurIPS
(2025). arXiv:2504.20571
16. Xu, C., Yan, N., Chen, L., Kechadi, M.-T.: Phantom Gains: Auditing Self-
Improvement Against a Measured Null. arXiv:2608.20290 (2026)
17. Xu, Z., Li, Y., Jiang, F., Ramasubramanian, B., Niu, L., Lin, B., Poovendran, R.:
TinyV: Reducing False Negatives in Veriﬁcation Improves RL for LLM Reasoning.
arXiv:2505.14625 (2025)
18. Yuan, Z., Yuan, H., Li, C., Dong, G., Lu, K., Tan, C., Zhou, C., Zhou, J.: Scaling
Relationship on Learning Mathematical Reasoning with Large Language Models.
arXiv:2308.01825 (2023)
19. Yue, Y., Chen, Z., Lu, R., Zhao, A., Wang, Z., Yue, Y., Song, S., Huang, G.: Does
Reinforcement Learning Really Incentivize Reasoning Capacity in LLMs Beyond
the Base Model? arXiv:2504.13837 (2025)
20. Zelikman, E., Wu, Y., Mu, J., Goodman, N.D.: STaR: Bootstrapping Reasoning
With Reasoning. arXiv:2203.14465 (2022)
21. Zeng, W., Huang, Y., Liu, Q., Liu, W., He, K., Ma, Z., He, J.: SimpleRL-Zoo:
Investigating and Taming Zero Reinforcement Learning for Open Base Models in
the Wild. arXiv:2503.18892 (2025)
