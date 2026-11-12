
Mathematics or the Veriﬁer?
15
any single recipe change. Truncation: the 512-token cap binds from the start (a
quarter of the pool is cut). Scope: one model family and size, all instruction-
tuned (no base model), one veriﬁer, a restart-from-base design that leaves com-
pounding little room (no continued training), possible Qwen2.5 contamination
on MATH/GSM8K (unquantiﬁed), and a default repetition penalty (1.1) that
may depress the baseline.
7
Conclusion
We asked whether generate–verify–select–train iterations make a 1.5B model
better at mathematics or only teach it to write what a rule-based veriﬁer accepts.
The design detected no pass@1 or pass@k gain at any rate (it could see only gains
of about 10 and 8–10 points; 6 in a ﬁnal 500-problem round, where pass@1 falls
3.2–4.8 points in all three seeds). Because training on reference solutions lowers
pass@1 by about 30 points even with a revised recipe, this is a null for the recipe
and says little about self-training, and since scores are graded by the selecting
veriﬁer (apart from one string-match check), neither branch of the question is
answered. The post hoc false-reject audit is uninformative about adaptation:
its fall is tied to the falling \boxed share by an identity, and it has little power
(about 25 aﬀected problems, a handful of avoidance examples per round, no valid
positive control). At the highest rate the model is less accurate on the solutions
it ﬁnishes. The pooled design’s decline is absent in the isolated runs at 10−5,
which use about 4.5× fewer examples, so dose and pooling are confounded.
A dose-matched control for the gold-storage defect, a recipe that passes the
positive gate, and a second grader come ﬁrst (Supplementary Appendix K).
Acknowledgments. This work was carried out as an undergraduate research project.
No external funding was received.
Disclosure of Interests. The authors have no competing interests to declare that
are relevant to the content of this article.
Code availability Code, saved generations and analysis scripts are at https://github.
com/tsan2711/DACNTT_2026 (tag paper-2026-11b). Generation-time token counts,
Design P’s training logs and the 1,536-token re-scoring outputs were not saved.
Use of AI tools The authors used Claude (Anthropic), through Claude Code, to help
write the manuscript, the analysis and training scripts, and to run automated reviews.
The authors designed the study, ran the experiments and take responsibility for the
content.
References
1. Cai, X.-Q., Wang, W., Liu, F., Liu, T., Niu, G., Sugiyama, M.: Reinforce-
ment Learning with Veriﬁable yet Noisy Rewards under Imperfect Veriﬁers.
arXiv:2510.00915 (2025)


16
T. S. Nguyen and D. A. Tran
2. Cobbe, K., Kosaraju, V., Bavarian, M., Chen, M., Jun, H., Kaiser, L., Plappert,
M., Tworek, J., Hilton, J., Nakano, R., Hesse, C., Schulman, J.: Training Veriﬁers
to Solve Math Word Problems. arXiv:2110.14168 (2021)
3. Dang, Q.-A., Ngo, C.: Reinforcement Learning for Reasoning in Small LLMs: What
Works and What Doesn’t. arXiv:2503.16219 (2025)
4. Egashira, K., Vero, M., Dekoninck, J., Dörner, F.E., Staab, R., Vechev, M.: Delay,
Plateau, or Collapse: Evaluating the Impact of Systematic Veriﬁcation Error on
RLVR. arXiv:2605.02909 (2026)
5. Hendrycks, D., Burns, C., Kadavath, S., Arora, A., Basart, S., Tang, E., Song,
D., Steinhardt, J.: Measuring Mathematical Problem Solving With the MATH
Dataset. arXiv:2103.03874 (2021)
6. Huang, Y., Zeng, W., Zeng, X., Zhu, Q., He, J.: From Accuracy to Robust-
ness: A Study of Rule- and Model-based Veriﬁers in Mathematical Reasoning.
arXiv:2505.22203 (2025)
7. Kim, J., Luo, X., Kim, M., Lee, S., Kim, D., Jeon, J., Li, D., Yang, Y.: Why
Does Self-Distillation (Sometimes) Degrade the Reasoning Capability of LLMs?
arXiv:2603.24472 (2026)
8. Qiao, X., Du, X., Liu, W., Zhang, J., Mai, P., Zhang, M., Pang, Y.: When Sample
Selection Bias Precipitates Model Collapse. arXiv:2606.13732 (2026)
9. Shao, R., Li, S.S., Xin, R., Geng, S., Wang, Y., Oh, S., Du, S.S., Lambert, N., Min,
S., Krishna, R., Tsvetkov, Y., Hajishirzi, H., Koh, P.W., Zettlemoyer, L.: Spurious
Rewards: Rethinking Training Signals in RLVR. arXiv:2506.10947 (2025)
10. Shumailov, I., Shumaylov, Z., Zhao, Y., Papernot, N., Anderson, R., Gal, Y.: AI
models collapse when trained on recursively generated data. Nature (2024). https:
//doi.org/10.1038/s41586-024-07566-y
11. Singh, A., Co-Reyes, J.D., Agarwal, R., et al.: Beyond Human Data: Scaling Self-
Training for Problem-Solving with Language Models. arXiv:2312.06585 (2023)
12. Gulcehre, C., Le Paine, T., Srinivasan, S., et al.: Reinforced Self-Training (ReST)
for Language Modeling. arXiv:2308.08998 (2023)
13. Strozzi, I.L.: Teacher-Free Self-Training Ampliﬁes but Does Not Compound: A
Pass@k Crossover on a Free-Veriﬁer Domain. arXiv:2606.07856 (2026)
14. Wang, Y., Yang, Q., Zeng, Z., Ren, L., Liu, L., Peng, B., Cheng, H., He, X., Wang,
K., Gao, J., Chen, W., Wang, S., Du, S.S., Shen, Y.: Reinforcement Learning for
Reasoning in Large Language Models with One Training Example. In: NeurIPS
(2025). arXiv:2504.20571
15. Xu, C., Yan, N., Chen, L., Kechadi, M.-T.: Phantom Gains: Auditing Self-
Improvement Against a Measured Null. arXiv:2608.20290 (2026)
16. Xu, Z., Li, Y., Jiang, F., Ramasubramanian, B., Niu, L., Lin, B., Poovendran, R.:
TinyV: Reducing False Negatives in Veriﬁcation Improves RL for LLM Reasoning.
arXiv:2505.14625 (2025)
17. Yuan, Z., Yuan, H., Li, C., Dong, G., Lu, K., Tan, C., Zhou, C., Zhou, J.: Scaling
Relationship on Learning Mathematical Reasoning with Large Language Models.
arXiv:2308.01825 (2023)
18. Yue, Y., Chen, Z., Lu, R., Zhao, A., Wang, Z., Yue, Y., Song, S., Huang, G.: Does
Reinforcement Learning Really Incentivize Reasoning Capacity in LLMs Beyond
the Base Model? arXiv:2504.13837 (2025)
19. Zelikman, E., Wu, Y., Mu, J., Goodman, N.D.: STaR: Bootstrapping Reasoning
With Reasoning. arXiv:2203.14465 (2022)
20. Zeng, W., Huang, Y., Liu, Q., Liu, W., He, K., Ma, Z., He, J.: SimpleRL-Zoo:
Investigating and Taming Zero Reinforcement Learning for Open Base Models in
the Wild. arXiv:2503.18892 (2025)
