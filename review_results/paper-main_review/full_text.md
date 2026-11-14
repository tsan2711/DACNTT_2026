# Reinforcement Learning with Verifiable yet Noisy Rewards under Imperfect Verifiers

Abstract
    

Reinforcement Learning with Verifiable Rewards (RLVR) replaces costly human labeling with automated verifiers. To reduce verifier hacking, many RLVR systems binarize rewards to {0,1}\{0,1\}, but imperfect verifiers inevitably introduce false negatives (FN, rejecting correct answers) and false positives (FP, accepting incorrect ones). We formalize verifier unreliability as a stochastic reward channel with asymmetric noise rates ρ0\rho_{0} and ρ1\rho_{1}—the FP rate and the FN rate, respectively. From this abstraction we derive two lightweight corrections: (i) a backward correction that yields an unbiased surrogate reward and thus an unbiased policy-gradient estimator in expectation, and (ii) a forward correction that reweights score-function terms so the expected update aligns with the clean gradient direction and requires only the FN rate. We implement both as lightweight hooks in a group relative policy optimization pipeline, both corrections improve RLVR reasoning under synthetic and real verifier noise, with the forward variant being more stable under heavier noise. We further use a lightweight appeals mechanism to estimate FN rates online and show that the correction can complement stronger verifier-side baselines.

  

## 1 Introduction

Reinforcement Learning with Verifiable Rewards (RLVR) offers a scalable paradigm for improving the reasoning abilities of Large Language Models (LLMs) by replacing expensive human annotation with automated feedback (Wen et al., 2025). In this problem, a policy is trained using rewards from a verifier that automatically checks the correctness of a model’s output (Shao et al., 2024). The efficacy of this approach, however, heavily depends on the verifier’s reliability. Emerging evidence reveals that verifiers are systematically fallible in two critical ways: they can accept incorrect solutions (false positives; FPs) or reject correct ones (false negatives; FNs) (Xu et al., 2025; Zhao et al., 2025).

FPs have been widely documented as a vulnerability of LLM-based verifiers. Recent studies showed that LLM judges can be swayed by superficial cues—e.g., popular specialized verifiers, such as GPT-4o, give 35 % – 66.8% FP rate when the answer starts with Let’s solve this problem step by step (Zhao et al., 2025; Shi et al., 2025; Shi et al., 2024; Chen et al., 2024). Conversely, FNs are common with rule-based verifiers. These checkers, while highly precise, are often brittle; they may reject valid solutions that are formatted differently, expressed in an algebraically equivalent form, or embedded in explanatory text (Hugging Face, 2025). A recent analysis of a math-RL dataset found that over 38% of responses flagged as incorrect by a rule-based system were in fact correct, a gap that a lightweight LLM verifier could partially close (Xu et al., 2025). Both FPs and FNs materially degrade RLVR training: FNs deprive the agent of informative gradients and slow convergence, while FPs reward hackable patterns and inflate returns during policy optimization (Xu et al., 2025; Huang et al., 2025).

Figure 1: Verifier-noise flow in RLVR. An AI agent produces candidate solutions that are scored by automated verifiers. While verifiers would yield false negatives (1236\frac{12}{36} vs. 13\frac{1}{3}, reaching 38%38\% rates (Xu et al., 2025)) and false positives (mislead by “Let’s solve it step by step…”, reaching 35%−66.8%35\%-66.8\% rates (Zhao et al., 2025)), confusing the agent; applying our backward/forward corrections restores correct signals.

Motivated by these failures, we address these challenges by explicitly treating verifier errors as noise in the reward signal. We model the verifier as a stochastic reward channel that corrupts the true, latent reward with verifier-conditional probabilities—the FP rate and the FN rate. Building on this formulation, we derive two estimators to counteract this noise. Our first method, noisy Policy Gradient with Backward Correction (PGBC), inverts the noise process to compute an unbiased estimator of the true reward, which can be used as a drop-in replacement in any advantage-estimation in RL. Our second method, noisy Policy Gradient with Forward Correction (PGFC), directly reweights the terms of the policy gradient to ensure its expected direction aligns with the clean gradient. This approach requires only an estimate of the FN rate to achieve directional correctness, making it suitable for the often harder-to-estimate FP rate (Xu et al., 2025). The pipeline is illustrated in Figure 1.

We integrate these corrections into a group relative policy optimization (GRPO) (Shao et al., 2024)-based RLVR pipeline and demonstrate their effectiveness on competitive math reasoning benchmarks (Shao et al., 2024). Both methods consistently outperform uncorrected training and achieve performance nearly equivalent to that of noise-free scenarios, with the forward correction offering the fastest and most stable convergence. We also propose a practical online estimation scheme for the FN rate: a querying mechanism where a low-cost LLM verifier like TinyV (Xu et al., 2025) re-evaluates outputs rejected by a primary rule-based checker. This hybrid approach provides a reliable estimate of the FN rate with minimal computational overhead, recovering near-oracle performance. Furthermore, we stress-test our approach under complex, non-i.i.d. noise distributions that violate our FP and FN modeling, but both PGBC and PGFC corrections remain robust and effective even in these more challenging conditions. Our contributions are: (i) a formal verifier-channel model for RLVR that captures the prevalent FP and FN errors; (ii) backward and forward corrections derived from RL principles to calibrate policy learning; and (iii) a practical implementation for online noise estimation that makes these corrections viable in real-world systems.

## 2 Related Works

#### Reasoning with LLMs.

A large body of work improves LLM reasoning through prompting and search at inference time. Chain-of-Thought (CoT) prompting elicits step-by-step rationales and boosts arithmetic and commonsense reasoning (Wei et al., 2022), while self-consistency aggregates diverse reasoning paths to further improve robustness (Wang et al., 2023). Decomposition-based prompting, such as Least-to-Most, solves complex problems via ordered sub-problems (Zhou et al., 2023); search-based schemes like Tree-of-Thoughts explicitly explore and evaluate alternative reasoning branches (Yao et al., 2023). Orthogonally, training-time verifier signals can be used to re-rank candidate solutions, as in Cobbe et al. (2021). Our work is complementary: rather than proposing a new inference-time strategy or re-ranking scheme, we address how to perform policy optimization when the reward itself—supplied by a verifier—is noisy.

#### RLVR and verifier reliability.

Recent math-RL pipelines combine on-policy RL (e.g., GRPO) with programmatic or LLM-based verifiers to yield verifiable rewards (Mroueh, 2025). However, LLM-as-a-judge is prone to systematic biases, including position bias and prompt-based attacks, producing FPs (accepting incorrect solutions) (Gu et al., 2024; Thakur et al., 2024; Shi et al., 2025; Zhao et al., 2025; Shi et al., 2024). Conversely, exact-match or brittle parsers in rule-based checkers can miss algebraic equivalences and text-formatted answers, leading to widespread FNs (Li et al., 2025; Huang et al., 2025). A recent study showed that over 38% of model responses labeled incorrect by a rule-based pipeline were in fact correct, and introduced a lightweight verifier (TinyV) that recovers many such cases with minimal overhead (Xu et al., 2025). Prior efforts therefore improved the verifier (e.g., better judges or appeals) or evaluation suites; in contrast, we treat verifier errors as verifier-conditional noise and directly correct the policy gradient so that learning remains aligned with the clean objective even when the verifier is imperfect.

#### Learning with noisy labels.

While our method is derived from RL, it shares intuition with the literature on learning with label noise. Wang et al. (2020) modeled reward corruption via a class-conditional confusion matrix and derived an unbiased surrogate reward for Q-learning algorithms to solve control tasks. In supervised learning, a central thread is to make empirical-risk minimization robust either by correcting the loss given a noise-transition model or by avoiding or down-weighting suspected noisy examples (Song et al., 2022; Li et al., 2021). The former includes the unbiased-risk estimators of Natarajan et al. (2013) and the now-standard loss corrections of Patrini et al. (2017). A second family avoids the noise explicitly by relying on the “small-loss first” memorization dynamics of deep nets: mentor methods (MentorNet) learn a weighting network that feeds cleaner samples to the student, and Co-teaching (Han et al., 2018) trains two peers that exchange their selected small-loss examples; semi-supervised hybrids such as DivideMix (Li et al., 2020) split data into clean/noisy partitions via mixture modeling and co-train with consistency regularization (Jiang et al., 2018). Unlike them, we target the policy gradient estimator in RLVR: we instantiate both backward and forward corrections inside the policy gradient estimator to stabilize and align RL under verifier noise, instead of a direct supervised-loss substitution.

## 3 Problem Setup and Algorithms

In this section, we introduce the problem formulations and our proposed algorithms.

### 3.1 Problem Setup

We consider the standard RLVR setting where a stochastic policy πθ​(y|x)\pi_{\theta}(y|x) generates a response yy for a given prompt xx, where θ\theta denotes learnable parameters. The goal is to maximize an objective based on the true, or clean, reward R∗​(x,y)∈{0,1}R^{*}(x,y)\in\{0,1\}, which indicates whether the response yy is genuinely correct. This objective is typically regularized by a KL-divergence term to a reference policy πref\pi_{\mathrm{ref}} to maintain stability:

maxθJβ(θ)=𝔼x𝔼y∼πθ(⋅∣x)[R∗(x,y)−βKL(πθ(⋅∣x)∥πref(⋅∣x))],\max_{\theta}\;J_{\beta}(\theta)\;=\;\mathbb{E}_{x}\,\mathbb{E}_{y\sim\pi_{\theta}(\cdot\mid x)}\!\Big[\,R^{*}(x,y)-\beta\,\mathrm{KL}(\pi_{\theta}(\cdot\mid x)\,\|\,\pi_{\mathrm{ref}}(\cdot\mid x))\,\Big],

(1)

in which KL\mathrm{KL} denotes the Kullback-Leibler (KL)-divergence. The policy gradient with respect to the unregularized reward is given by the REINFORCE estimator (Sutton et al., 1999), ∇θJ​(θ)=𝔼⁡[R∗​(x,y)​∑tGt]\nabla_{\theta}J(\theta)=\mathbb{E}[R^{*}(x,y)\,\sum_{t}G_{t}], where Gt=∇θ​log​πθ​(yt∣x,y<t)G_{t}=\nabla_{\!\theta}\log\pi_{\theta}(y_{t}\mid x,y_{<t}) is the score function for the token at step tt, and y<ty_{<t} denotes the sequence of tokens generated prior to step
tt. In the following, we will denote R⁡(x,y)R(x,y) with RR for brevity. In practice, the clean reward R∗R^{*} is unavailable. Instead, the agent receives a noisy reward R~​(x,y)∈{0,1}\tilde{R}(x,y)\in\{0,1\} from an automated verifier. We model this verifier as a stochastic reward channel that flips the latent clean reward to an observed noisy one. This channel is characterized by asymmetric, verifier-conditional noise rates.

Definition 3.1 (Verifier Reward Channel).

The observed verifier reward R~\tilde{R} is generated from the latent clean reward R∗R^{*} according to the following conditional probabilities:

ℙ⁡(R~=1∣R∗=0)=ρ0,ℙ⁡(R~=0∣R∗=1)=ρ1,\mathbb{P}\bigl(\tilde{R}=1\mid R^{*}=0\bigr)=\rho_{0},\mathbb{P}\bigl(\tilde{R}=0\mid R^{*}=1\bigr)=\rho_{1},

(2)

where ρ0,ρ1∈[0,1)\rho_{0},\rho_{1}\in[0,1) and ρ0+ρ1<1\rho_{0}+\rho_{1}<1.

The condition ρ0+ρ1<1\rho_{0}+\rho_{1}<1 implies that the verifier channel is informative and invertible. Equivalently, the 2×22\times 2 binary transition matrix has determinant 1−ρ0−ρ1>01-\rho_{0}-\rho_{1}>0.

#### Assumptions and scope of the verifier channel.

Definition 3.1 is a deliberately lightweight abstraction of verifier unreliability.
It assumes (i) instance-independent class-conditional noise rates (ρ0,ρ1)(\rho_{0},\rho_{1}) that do not vary with (x,y)(x,y), and (ii) conditional independence: given the latent correctness R∗​(x,y)R^{*}(x,y), the verifier’s stochastic flip R~\tilde{R} is independent of the policy’s sampling randomness (hence independent of the score-function terms used by policy gradients).
These assumptions are standard in class-conditional noise models and allow closed-form reward/gradient corrections.
In real RLVR deployments, verifier errors can be content-dependent (e.g., spurious phrases can increase FPs), which violates (i) and can partially violate (ii).
We therefore view (ρ0,ρ1)(\rho_{0},\rho_{1}) as effective noise rates, and empirically test robustness to mis-specification in Section 4.4;
we further estimate ρ1\rho_{1} online via a low-cost appeals mechanism in Section 4.3.
When rates are instance-dependent, the same formulas are treated as correcting an effective marginal channel rather than eliminating all bias; Appendix B gives the resulting covariance residual.

Based on this noise model, we establish a linear relationship between the expected noisy reward and the clean reward, which is presented in Proposition 3.2.

Proposition 3.2 (Connection between Corrupted Rewards and True Rewards).

Under the Verifier Reward Channel model, the expectation of the noisy reward R~\tilde{R} conditioned on the clean reward R∗R^{*} is an affine transformation of R∗R^{*}:

𝔼⁡[R~∣R∗]=(1−ρ0−ρ1)​R∗+ρ0.\mathbb{E}[\tilde{R}\mid R^{*}]\;=\;(1-\rho_{0}-\rho_{1})\,R^{*}+\rho_{0}.

The proof is provided in Appendix D.1. The central challenge of RLVR is that naively optimizing with the noisy reward R~\tilde{R} leads to a biased policy gradient, causing the policy to learn from mistakes of the verifier. Our goal is to develop policy gradient estimators that use only the observable noisy reward R~\tilde{R} but the expectation is either identical or parallel to the true policy gradient ∇θJ​(θ)\nabla_{\theta}J(\theta). We integrate these estimators within REINFORCE-style policy gradient algorithms widely used for reasoning tasks that compute normalized advantages over a group of sampled trajectories (Shao et al., 2024).

### 3.2 Noisy Policy Gradient with Backward Correction (PGBC)

Our first proposed approach aims to construct an unbiased estimator of the true reward R∗R^{*} by “inverting” the noise process. Since the expected noisy reward 𝔼⁡[R~∣R∗]\mathbb{E}[\tilde{R}\mid R^{*}] is an affine transformation of the clean reward R∗R^{*} in Proposition 3.2, we can solve for R∗R^{*} to derive a corrected reward estimator, R^\widehat{R}, that is unbiased in expectation.

Theorem 3.3 (Oracle-Rate Unbiased Reward Estimator for the Binary Verifier Channel).

Given the verifier channel with known noise rates ρ0\rho_{0} and ρ1\rho_{1} with ρ0+ρ1<1\rho_{0}+\rho_{1}<1, the estimator

R^=R~−ρ0 1−ρ0−ρ1\widehat{R}=\frac{\tilde{R}-\rho_{0}}{\,1-\rho_{0}-\rho_{1}\,}

(3)

is an unbiased estimator of the true reward R∗​(x,y)R^{*}(x,y), i.e., 𝔼⁡[R^]=R∗\mathbb{E}[\widehat{R}]=R^{*}.

The proof is provided in Appendix D.2. The theorem is an oracle-rate population statement: unbiasedness holds when the channel rates used in the correction equal the true effective rates and before finite-sample GRPO normalization, clipping, or KL terms are applied. Theorem 3.3 shows that, by replacing the noisy reward R~\tilde{R} with R^\widehat{R} in any standard policy gradient formulation, we obtain an unbiased estimate of the true policy gradient. This allows R^\widehat{R} to serve as a drop-in replacement for the reward signal in complex RL algorithms, seamlessly integrating with advantage estimation and other machinery.
The details of the algorithm are summarized in Algorithm 1. After rolling out a set of trajectories and obtaining their rewards, we use the corrected rewards to compute the policy gradients for model update.

Algorithm 1  Noisy Policy Gradient with Backward Correction (PGBC)

              
              
             Input: Initial policy θ0\theta_{0}; learning rate η\eta; batch size MM; estimates of noise rates, (ρ^0,ρ^1)(\hat{\rho}_{0},\hat{\rho}_{1}).

              
              
             loop

              
              
              Roll out MM trajectories {(xi,yi)}i=1M\{(x_{i},y_{i})\}_{i=1}^{M}, obtaining observed rewards {R~i}i=1M\{\tilde{R}_{i}\}_{i=1}^{M}.

              
              
              For each trajectory ii, compute the unbiased reward estimate:

R^i←R~i−ρ^01−ρ^0−ρ^1.\widehat{R}_{i}\leftarrow\frac{\tilde{R}_{i}-\hat{\rho}_{0}}{1-\hat{\rho}_{0}-\hat{\rho}_{1}}.

              
              
              Compute the policy gradient using the corrected rewards {R^i}i=1M\{\widehat{R}_{i}\}_{i=1}^{M}.

              
              
              Update parameters: θ←θ+η​Δ​θ\theta\leftarrow\theta+\eta\,\Delta\theta.

              
              
             end loop

### 3.3 Noisy Policy Gradient with Forward Correction (PGFC)

While PGBC provides an elegant unbiased estimator, it faces two practical challenges. First, the denominator (1−ρ0−ρ1)(1-\rho_{0}-\rho_{1}) can be small if the total noise rate is high, leading to high variance in the reward estimate R^\widehat{R} and potentially unstable training. Second, it requires accurate estimation of both the false positive rate ρ0\rho_{0} and the false negative rate ρ1\rho_{1}, which are usually difficult to obtain in practice. The PGFC approach is introduced to mitigate these issues.

Instead of correcting the reward itself, this method directly modifies the policy gradient estimator to ensure its expectation is correctly aligned. The core idea is to reweight the score function GtG_{t} under the tt-th token based on the observed noisy reward R~\tilde{R}. We define an update term ht=wR~​Gth_{t}=w_{\tilde{R}}G_{t} and choose the forward weights w0w_{0} (for R~=0\tilde{R}=0) and w1w_{1} (for R~=1\tilde{R}=1) such that the expected update 𝔼⁡[ht]\mathbb{E}[h_{t}] is parallel to the clean gradient ∇θJ​(θ)\nabla_{\theta}J(\theta). The key insight is to choose the forward weights so that the conditional expectations given the true reward R∗R^{*} have a specific structure.

Proposition 3.4 (Conditional Expectation of Forward Weights).

Let the forward weights be defined as w0=ρ1−1w_{0}=\rho_{1}-1 and w1=ρ1w_{1}=\rho_{1}. Under the Verifier Reward Channel model, the conditional expectations of the corresponding weight wR~w_{\tilde{R}} given the true reward R∗R^{*} are:

• 1. 

𝔼⁡[wR~∣R∗=1]= 0\mathbb{E}[w_{\tilde{R}}\mid R^{*}=1]\;=\;0.

• 2. 

𝔼⁡[wR~∣R∗=0]=−(1−ρ0−ρ1)\mathbb{E}[w_{\tilde{R}}\mid R^{*}=0]\;=\;-(1-\rho_{0}-\rho_{1}).

The proof can be found in Appendix D.3. Proposition 3.4 reveals that, in expectation, the forward weights are chosen so that their conditional expectation vanishes when R∗=1R^{*}=1, i.e., truly positive cases do not require correction. Consequently, the explicit contribution to the correction term arises from samples with R∗=0R^{*}=0. This structure allows us to recover the correct gradient direction, as shown in the following theorem.

Theorem 3.5 (REINFORCE-Style Directional Alignment of the Forward Correction).

Let the gradient-update term be Δ​θ=1M​∑wR~​Gt\Delta\theta=\frac{1}{M}\sum w_{\tilde{R}}\,G_{t}, where w0=ρ1−1w_{0}=\rho_{1}-1 and w1=ρ1w_{1}=\rho_{1} with MM trajectories. Under the Verifier Reward Channel model, the expected update is parallel to the clean policy gradient:

𝔼⁡[Δ​θ]=c​∇θJ​(θ),\mathbb{E}[\Delta\theta]\;=\;c\,\nabla_{\theta}J(\theta),

(4)

in which c=(1−ρ0−ρ1)c=(1-\rho_{0}-\rho_{1}).

The proof is given in Appendix D.4. Since 1−ρ0−ρ1>01-\rho_{0}-\rho_{1}>0, Theorem 3.5 guarantees that the expected update of the policy is in the same direction as the true gradient; meanwhile, the positive scaling factor (1−ρ0−ρ1)(1-\rho_{0}-\rho_{1}) can be absorbed into the learning rate. By avoiding the inverse operation of PGBC, PGFC circumvents the variance-inflation problem.

Algorithm 2  Noisy Policy Gradient with Forward Correction (PGFC)

              
              
             Input: Initial policy θ0\theta_{0}; learning rate η\eta; batch size MM; an estimate of the false negative rate, ρ^1\hat{\rho}_{1}.

              
              
             loop

              
              
              Roll out MM trajectories and observe rewards {R~i}i=1M\{\tilde{R}_{i}\}_{i=1}^{M}.

              
              
              For each trajectory ii, define the weight based on the observed reward R~i\tilde{R}_{i}:

wR~i←{ρ^1−1,if ​R~i=0,ρ^1,if ​R~i=1.w_{\tilde{R}_{i}}\;\leftarrow\;\begin{cases}\hat{\rho}_{1}-1,&\text{if }\tilde{R}_{i}=0,\\
\hat{\rho}_{1},&\text{if }\tilde{R}_{i}=1.\end{cases}

              
              
              For each trajectory ii, compute the score-function term GiG_{i} and the weighted term hi←wR~i​Gih_{i}\leftarrow w_{\tilde{R}_{i}}\,G_{i}.

              
              
              Form the policy gradient estimate: g^←1M​∑i=1Mhi\hat{g}\leftarrow\frac{1}{M}\sum_{i=1}^{M}h_{i}.

              
              
              Update parameters: θ←θ+η​g^\theta\leftarrow\theta+\eta\,\hat{g}.

              
              
             end loop

(a) Qwen2.5-Math-1.5B

(b) DeepSeek-R1-Distill-Qwen-1.5B

(c) Llama-3.2-3B-Instruct

(d) Qwen2.5-Math-7B

Figure 2: Synthetic-Noise Results (pass@1) with 16 samples and 5 random seeds. Base: baseline without RL; Oracle: Training with clean rewards; Noise: Training with noisy verifier rewards; Noise_BC: Training with noise under backward correction; Noise_FC: Training with noise under forward correction.

In practice, we estimate ρ^1\hat{\rho}_{1} during training by appealing a small, uniformly random subset of rule-based negatives to a lightweight LLM verifier (e.g., TinyV (Xu et al., 2025)) and then smoothing the empirical flip rate. Concretely, at step tt, let 𝒩R(t)\mathcal{N}_{\mathrm{R}}^{(t)} be items labeled negative by the rule-based verifier, 𝒫R(t)\mathcal{P}_{\mathrm{R}}^{(t)} the rule-based positives, and sample a fraction q∈(0,1]q\in(0,1] of 𝒩R(t)\mathcal{N}_{\mathrm{R}}^{(t)} for appeal; denote by 𝒫L(t)\mathcal{P}_{\mathrm{L}}^{(t)} those appealed items that the LLM flips to positive. Using a Horvitz–Thompson correction (Karwa and Airoldi, 2023), we estimate the number of FNs as |𝒫L(t)|/q|\mathcal{P}_{\mathrm{L}}^{(t)}|/q, treat |𝒫R(t)||\mathcal{P}_{\mathrm{R}}^{(t)}| as true positives in the rule-checker regime, and set ρ^1(t)=|𝒫L(t)|/q+α|𝒫L(t)|/q+|𝒫R(t)|+α+β\hat{\rho}_{1}^{(t)}=\frac{|\mathcal{P}_{\mathrm{L}}^{(t)}|/q+\alpha}{|\mathcal{P}_{\mathrm{L}}^{(t)}|/q+|\mathcal{P}_{\mathrm{R}}^{(t)}|+\alpha+\beta} with small Beta-prior pseudocounts α,β=10−5\alpha,\beta=10^{-5}. We then apply exponential moving average (EMA) smoothing over a sliding window. If both ρ^0\hat{\rho}_{0} and ρ^1\hat{\rho}_{1} are available, one can use PGBC; if only ρ^1\hat{\rho}_{1} is available, PGFC is the default. We released our code in  https://github.com/caixq1996/noisy-RLVR. More details of appealing mechanism can be found in Appendix E.4.

#### Bridging REINFORCE-Style Corrections to GRPO Updates

Our analysis is stated for the reward-gradient component of a score-function estimator, while GRPO implements this component through scalar trajectory coefficients broadcast as token-level advantages inside a clipped surrogate. We therefore insert each correction at the coefficient level that best matches its estimator: PGBC is implemented as a corrected-utility coefficient based on r^i=(r~i−ρ^0)/(1−ρ^0−ρ^1)\widehat{r}_{i}=(\tilde{r}_{i}-\hat{\rho}_{0})/(1-\hat{\rho}_{0}-\hat{\rho}_{1}), whereas PGFC is implemented as a score-level coefficient wr~i∈{ρ^1−1,ρ^1}w_{\tilde{r}_{i}}\in\{\hat{\rho}_{1}-1,\hat{\rho}_{1}\}, not as a reward proxy. In both cases, the corrected coefficient is passed directly to the GRPO surrogate, with the KL term unchanged. This implementation avoids a subtle binary-reward degeneracy: any pre-normalization proxy affine in r~i\tilde{r}_{i} can be removed by group centering and standardization, making the corrected update identical to uncorrected noisy-reward GRPO. Appendix A states the centered-update guarantee and Appendix B gives the implementation recipe.

## 4 Experiments

We evaluate our approach under both synthetic and real-world verifier noise. We first spell out the experimental protocol, and then present main and ablation results. Additional experimental results, including training dynamics, pass@8 performance under real-world noise, appeals statistics, complementarity with stronger verifiers, and non-math evaluations are provided in Appendix C.

### 4.1 Experimental Setup

We train on three small backbones, Qwen2.5-Math-1.5B, DeepSeek-R1-Distill-Qwen-1.5B, and Llama-3.2-3B-Instruct, and probe scale with Qwen2.5-Math-7B. Rewards come from either (i) a rule-based checker that extracts the final \boxed{\cdot} answer and tests numeric/rational equivalence or (ii) a lightweight LLM verifier (TinyV 1.5B) used for appeals/estimation; prior work motivates explicit noise modeling due to systematic FP/FN behavior in these verifiers. Unless stated otherwise, we follow the DeepScaleR corpus and a GRPO-style on-policy recipe with BoN sampling, implementing our backward and forward corrections as drop-in hooks at the advantage-construction stage within VERL. Evaluation uses six verifiable math suites—AIME-2024, AIME-2025, AMC-2023, MATH500, Minerva MATH, and OlympiadBench—reporting Pass@1 and Pass@8 with 16 samples and 5 random seeds in average. Compute is 8×\timesA100 (40GB) GPUs servers; unless noted, KL schedules, sampling temperatures, and other rollout settings are kept identical across compared conditions.
We estimate pass@kk as 1−(n−cokk)/(nk)1-\binom{n-c_{\rm ok}}{k}/\binom{n}{k}, where n=16n=16, cokc_{\rm ok} is the number of correct samples, and k∈{1,8}k\in\{1,8\} (Chen et al., 2021). More details can be found in Appendix E.

### 4.2 Synthetic Noise

To disentangle optimization effects from verifier unreliability, we inject verifier-conditional noise into the binary reward stream during training. Concretely, when the latent clean reward is R∗∈{0,1}R^{*}\!\in\{0,1\}, the observed reward R~\tilde{R} is drawn from a reward channel with Pr⁡(R~=∣R∗=0)=ρ0\Pr(\tilde{R}{=}1\!\mid\!R^{*}{=}0)=\rho_{0} and Pr⁡(R~=∣R∗=1)=ρ1\Pr(\tilde{R}{=}0\!\mid\!R^{*}{=}1)=\rho_{1}; unless stated otherwise we use ρ0=0.1\rho_{0}{=}0.1 and ρ1=0.2\rho_{1}{=}0.2. We train GRPO on DeepScaleR with identical sampling and KL settings across conditions, and evaluate Pass@1 (16 samples) and Pass@8 on AIME-2024/2025, AMC-2023, MATH500, Minerva MATH, and OlympiadBench. We compare five variants: Base (no RL), Oracle (clean rewards), Noise (uncorrected), and our two corrections—PGBC (backward correction using R^=R~−ρ01−ρ0−ρ1\widehat{R}=\frac{\tilde{R}-\rho_{0}}{1-\rho_{0}-\rho_{1}}) and PGFC (forward correction that rescales the gradient using ρ1\rho_{1} only).
Figure 3 complements the pass@1 results with synthetic-noise pass@8: on the Qwen and Llama backbones, PGBC and PGFC improve over Noise and remain close to Oracle in the six-benchmark average.

(a) Qwen2.5-Math-1.5B

(b) DeepSeek-R1-Distill-Qwen-1.5B

(c) Llama-3.2-3B-Instruct

(d) Qwen2.5-Math-7B

Figure 3: Synthetic-Noise Results (pass@8) with 16 samples and 5 random seeds. Base: baseline without RL; Oracle: Training with clean rewards; Noise: Training with noisy verifier rewards; Noise_BC: Training with noise under backward correction; Noise_FC: Training with noise under forward correction.

### 4.3 Real-World Noise

As discussed above, automated verifiers exhibit both false positives (LLM judges over-crediting incorrect solutions) and false negatives (rule-based checkers rejecting correct ones) (Gu et al., 2024; Xu et al., 2025; Huang et al., 2025; Li et al., 2025). In math RL pipelines, the latter is particularly prevalent: brittle exact-match or limited equivalence rules lead to many valid answers being scored as incorrect, depriving the agent of learning signal. Motivated by this, in this subsection we specifically investigate whether denoising false negatives, i.e., estimating ρ^1\hat{\rho}_{1} as in Section 3.3, can measurably improve policy optimization. Concretely, we keep a fast rule-based checker as the primary reward source with a lightweight LLM verifier (TinyV) (Xu et al., 2025). From disagreements on negatives we maintain an online estimate ρ^1\hat{\rho}_{1} (EMA over a sliding window to track policy drift).

Results in Table 1 show a consistent pattern across backbones and benchmarks. Direct LLM-judge rewards underperform Rule on the six-benchmark average for each backbone, although individual task outcomes vary. Employing appeals to recheck rule-based negatives (Appeals) recovers some FNs, but its downstream benefit varies across models and benchmarks. In contrast, Appeals+PGFC uses the same appeals stream to estimate ρ^1\hat{\rho}_{1} and directly applies the FN correction to the policy gradient via weights wR~∈{ρ^1−1,ρ^1}w_{\tilde{R}}\!\in\!\{\hat{\rho}_{1}-1,\hat{\rho}_{1}\}, improving over Appeals in 22 of 24 cells.

Table 1: Real-world pass@1. Rule: uncorrected rule-based rewards; LLM-as-Judge: direct LLM-judge rewards; Appeals: rule-based reward plus LLM appeals on negative samples without gradient correction; Appeals+PGFC: appeals-based FN-rate estimation plus forward correction.

Dataset
AIME2024
AIME2025
AMC2023
MATH500
Minerva MATH
Olympiad Bench
Average

Qwen2.5-Math-1.5B

Base
6.0 ±\pm 1.9
4.0 ±\pm 0.6
34.2 ±\pm 0.2
47.5 ±\pm 0.3
5.1 ±\pm 0.4
25.1 ±\pm 0.4
20.3 ±\pm 0.6

Rule
15.0 ±\pm 0.4
5.6 ±\pm 0.6
50.3 ±\pm 0.6
69.4 ±\pm 0.4
17.8 ±\pm 0.6
31.6 ±\pm 0.0
31.6 ±\pm 0.4

LLM-as-Judge
10.9 ±\pm 1.3
4.7 ±\pm 1.0
42.1 ±\pm 1.8
63.0 ±\pm 0.7
15.9 ±\pm 0.7
25.3 ±\pm 0.5
27.0 ±\pm 1.0

Appeals
11.9 ±\pm 0.6
5.8 ±\pm 1.2
47.8 ±\pm 1.2
68.3 ±\pm 0.1
16.7 ±\pm 0.6
29.8 ±\pm 0.1
30.1 ±\pm 0.6

Appeals+PGFC (Ours)
20.3 ±\pm 0.0
10.7 ±\pm 1.7
53.3 ±\pm 1.4
68.6 ±\pm 0.8
16.5 ±\pm 0.4
32.9 ±\pm 0.2
33.7 ±\pm 0.8

DeepSeek-R1-Distill-Qwen-1.5B

Base
29.5 ±\pm 0.4
20.6 ±\pm 0.9
69.3 ±\pm 0.6
83.1 ±\pm 0.3
24.9 ±\pm 0.6
43.6 ±\pm 0.5
45.2 ±\pm 0.6

Rule
31.0 ±\pm 0.7
26.3 ±\pm 0.5
79.1 ±\pm 0.9
88.7 ±\pm 0.4
29.5 ±\pm 0.1
50.1 ±\pm 0.2
50.8 ±\pm 0.5

LLM-as-Judge
30.2 ±\pm 1.0
27.0 ±\pm 0.8
79.5 ±\pm 0.9
85.8 ±\pm 0.7
27.7 ±\pm 0.9
47.2 ±\pm 1.0
49.6 ±\pm 0.9

Appeals
34.0 ±\pm 1.2
27.8 ±\pm 0.9
78.7 ±\pm 1.1
88.0 ±\pm 0.8
29.0 ±\pm 1.0
49.6 ±\pm 1.1
51.2 ±\pm 1.0

Appeals+PGFC (Ours)
35.8 ±\pm 0.7
29.1 ±\pm 0.8
81.7 ±\pm 0.6
88.8 ±\pm 0.5
31.1 ±\pm 0.7
52.4 ±\pm 0.6
53.2 ±\pm 0.7

Llama-3.2-3B-Instruct

Base
5.7 ±\pm 1.2
0.6 ±\pm 0.4
17.2 ±\pm 1.5
34.8 ±\pm 0.7
4.8 ±\pm 0.3
12.7 ±\pm 0.2
12.6 ±\pm 0.2

Rule
6.0 ±\pm 1.0
1.0 ±\pm 0.4
24.3 ±\pm 1.7
40.4 ±\pm 0.5
8.9 ±\pm 0.7
15.0 ±\pm 0.5
15.9 ±\pm 0.8

LLM-as-Judge
1.4 ±\pm 1.1
0.1 ±\pm 0.3
12.7 ±\pm 2.1
26.4 ±\pm 0.2
4.1 ±\pm 0.2
7.7 ±\pm 0.4
8.7 ±\pm 0.6

Appeals
3.8 ±\pm 1.4
0.6 ±\pm 0.7
16.9 ±\pm 1.8
40.8 ±\pm 0.3
9.0 ±\pm 0.4
13.7 ±\pm 0.3
14.1 ±\pm 0.4

Appeals+PGFC (Ours)
9.4 ±\pm 1.9
0.4 ±\pm 0.6
21.2 ±\pm 1.3
46.4 ±\pm 0.3
9.9 ±\pm 0.8
16.3 ±\pm 0.3
17.3 ±\pm 0.9

Qwen2.5-Math-7B

Base
12.7 ±\pm 0.9
5.8 ±\pm 0.7
44.4 ±\pm 2.2
52.0 ±\pm 0.4
9.8 ±\pm 0.7
26.4 ±\pm 0.4
25.2 ±\pm 0.9

Rule
29.2 ±\pm 2.5
13.5 ±\pm 1.2
62.8 ±\pm 1.9
78.9 ±\pm 0.5
24.2 ±\pm 0.7
37.8 ±\pm 0.5
41.1 ±\pm 1.2

LLM-as-Judge
16.8 ±\pm 2.1
6.8 ±\pm 1.4
50.2 ±\pm 1.8
62.5 ±\pm 1.0
10.1 ±\pm 0.4
31.0 ±\pm 0.9
29.6 ±\pm 1.3

Appeals
27.4 ±\pm 1.9
11.8 ±\pm 1.9
63.7 ±\pm 1.6
74.9 ±\pm 0.7
20.6 ±\pm 0.8
37.6 ±\pm 0.3
39.3 ±\pm 1.2

Appeals+PGFC (Ours)
31.0 ±\pm 1.5
14.6 ±\pm 1.2
65.7 ±\pm 1.4
81.6 ±\pm 0.4
26.2 ±\pm 0.5
39.3 ±\pm 0.5
43.1 ±\pm 0.9

### 4.4 Robustness to Noise Mis-Specification

There now exist practical procedures to estimate verifier FP/FN rates via rule-based equivalence checkers (e.g., Math-Verify), lightweight appeals/judges such as TinyV, and meta-evaluation suites that quantify verifier reliability (Hugging Face, 2025; Xu et al., 2025; Li et al., 2025). In real deployments, however, these estimates can be imperfect. We therefore test how backward and forward corrections behave under mis-specified noise rates. We follow the synthetic-noise setting from Section 4.2 with Qwen2.5-math-1.5B: rewards are corrupted at data-time with ρ0=0.1,ρ1=0.2\rho_{0}{=}0.1,\ \rho_{1}{=}0.2. During training, we intentionally feed each algorithm mis-specified rates from a grid ρ^0∈[0.0,0.2]\hat{\rho}_{0}\in[0.0,0.2], ρ^1∈[0.1,0.3]\hat{\rho}_{1}\in[0.1,0.3], and report the Average Pass@1 (16 samples) across our six math benchmarks. Because the forward method only requires the false negative rate, we vary ρ^1\hat{\rho}_{1} for forward correction while keeping ρ^0\hat{\rho}_{0} unused, as shown in Fig. 4.

(a) BC: ρ^0=0.1\hat{\rho}_{0}{=}0.1, ρ^1∈[0.1,0.3]\hat{\rho}_{1}\!\in\![0.1,0.3]

(b) BC: ρ^1=0.2\hat{\rho}_{1}{=}0.2, ρ^0∈[0.0,0.2]\hat{\rho}_{0}\!\in\![0.0,0.2]

(c) FC: ρ^0=0.1\hat{\rho}_{0}{=}0.1, ρ^1∈[0.1,0.3]\hat{\rho}_{1}\!\in\![0.1,0.3]

Figure 4: Robustness results. (a) Backward correction (BC) with ρ^0\hat{\rho}_{0} fixed and sweeping ρ^1\hat{\rho}_{1}; (b) Backward correction (BC) with ρ^1\hat{\rho}_{1} fixed and sweeping ρ^0\hat{\rho}_{0}; (c) Forward correction (FC) with ρ^0\hat{\rho}_{0} fixed and sweeping ρ^1\hat{\rho}_{1}.

Backward correction remains strong when the total noise is underestimated, but performance degrades as we overestimate the rates (i.e., as 1−ρ^0−ρ^11-\hat{\rho}_{0}-\hat{\rho}_{1} shrinks). Intuitively, the unbiased de-biasing,
R^=R~−ρ^01−ρ^0−ρ^1\widehat{R}=\frac{\tilde{R}-\hat{\rho}_{0}}{1-\hat{\rho}_{0}-\hat{\rho}_{1}},
involves an inverse factor that amplifies reward variance and accentuates estimation error when the effective denominator becomes small. In contrast, forward correction exhibits a notably flat response curve around the true ρ1\rho_{1}; perturbing ρ^1\hat{\rho}_{1} changes only the per-sample weights and avoids any inverse operation, yielding lower-variance policy gradient estimates.

We also stress-test the constant-channel assumption using format-dependent, non-iid verifier noise with the same Qwen2.5-Math-1.5B / DeepScaleR setup. Both the FN and FP rates depend on a prompt-level tag and a response-level format tag (e.g., decimal or missing boxed answer vs. canonical format). Specifically, we use a shared FP rate of ρ0=0.2\rho_{0}=0.2 but a format-dependent FN rate: ρ1=0.05\rho_{1}=0.05 for low-risk formats and ρ1=0.45\rho_{1}=0.45 for high-risk formats, with the actual flip decision made by hashing (data_source, ground_truth, solution_str). This explicitly violates the instance-independent channel model. Table 2 shows that both corrections still improve over uncorrected training and base model under this non-iid noise setting, with PGFC again strongest performance in most cases.

Table 2: Format-dependent non-iid verifier-noise setting on Qwen2.5-Math-1.5B. Each cell reports pass@1 / pass@8.

Method
MATH500
AIME2024
AIME2025
AMC2023
Minerva Math
OlympiadBench
Average

Base
47.5 / 62.8
6.0 / 32.4
4.0 / 16.7
34.2 / 79.3
5.1 / 15.5
25.1 / 31.3
20.3 / 39.7

Noise
40.7 / 60.5
7.5 / 26.5
2.2 / 15.8
30.0 / 72.4
3.8 / 11.6
21.5 / 25.8
17.6 / 35.4

PGBC
67.7 / 67.9
11.5 / 33.0
7.4 / 22.4
49.1 / 81.8
20.7 / 21.1
30.5 / 31.7
31.2 / 43.0

PGFC
68.1 / 69.9
12.8 / 32.4
8.0 / 22.6
49.6 / 79.5
21.8 / 23.8
31.1 / 33.6
31.9 / 43.6

## 5 Conclusion

Reinforcement Learning with Verifiable Rewards (RLVR) has emerged as a practical and popular paradigm for training reasoning-focused large language models (LLMs). Yet binarized rewards inevitably suffer from false positives (FP) and false negatives (FN). Prior efforts largely mitigated these errors from the verifier side—e.g., debiasing LLM judges or strengthening equivalence checking—to reduce the downstream impact on learning (Li et al., 2025; Huang et al., 2025). In contrast, we modeled verifier unreliability as a verifier-conditional noise channel with the FP and FN rates, and introduced two theory-driven corrections that act directly at the policy-learning interface. The backward correction de-biases the observed reward to yield an unbiased gradient estimator; it requires estimates of the FP and FN rates but is agnostic to the choice of policy-optimization algorithm and can thus be used beyond policy gradient methods. The forward correction rescales score-function terms so that the expected update is aligned with the clean gradient; notably, it needs only the FN rate estimate, which is often the dominant source of real-world noise due to rule-based FNs (Huang et al., 2025; Xu et al., 2025).

While we instantiated appeals with a lightweight LLM verifier for efficiency, the same backward/forward correction mechanisms should also gain from stronger verifiers (Xu et al., 2025). Meanwhile, although modeled with the constant noise rates, the proposed methods already show clear advantages, even under a more challenging non-iid verifier noise setting. On the other hand, real-world noise can depend on content, formatting, prompt style, and verifier family, motivating future work on instance-dependent reliability models and adversarially robust verifiers.

## Appendix A From REINFORCE-Style Corrections to GRPO Updates

#### Setup (single prompt and group).

Fix a prompt xx and sample a group of KK i.i.d. responses y1,…,yK∼πθ(⋅∣x)y_{1},\dots,y_{K}\sim\pi_{\theta}(\cdot\mid x).
Let Gi≜∑t=1|yi|∇θ​log​πθ​(yi,t∣x,yi,<t)G_{i}\triangleq\sum_{t=1}^{|y_{i}|}\nabla_{\theta}\log\pi_{\theta}(y_{i,t}\mid x,y_{i,<t}) denote the trajectory score-function.
Let uiu_{i} be any scalar proxy reward computed from the trajectory. For PGBC, ui=r^iu_{i}=\widehat{r}_{i}. For the population PGFC theorem, the score-function term is weighted as wr~i​Giw_{\tilde{r}_{i}}G_{i}; the hypothetical pre-centering proxy ui=r~i​wr~iu_{i}=\tilde{r}_{i}w_{\tilde{r}_{i}} is analyzed below only as a degeneracy example, not as our default implementation.
Define the group mean u¯=1K​∑j=1Kuj\bar{u}=\frac{1}{K}\sum_{j=1}^{K}u_{j}.
Consider the centered score-function update

Δcenter​(θ)≜1K​∑i=1K(ui−u¯)​Gi.\Delta_{\text{center}}(\theta)\;\triangleq\;\frac{1}{K}\sum_{i=1}^{K}(u_{i}-\bar{u})\,G_{i}.

(5)

Proposition A.1 (Group centering preserves expected direction).

Assume {(ui,Gi)}i=1K\{(u_{i},G_{i})\}_{i=1}^{K} are i.i.d. under πθ(⋅∣x)\pi_{\theta}(\cdot\mid x) and 𝔼⁡[Gi∣x]=0\mathbb{E}[G_{i}\mid x]=0 (the standard score-function identity (Williams, 1992; Sutton et al., 1999)).
Then the centered update in (5) satisfies

𝔼⁡[Δcenter​(θ)∣x]=(1−1K)​𝔼​[u​G∣x].\mathbb{E}\!\left[\Delta_{\text{center}}(\theta)\mid x\right]\;=\;\Bigl(1-\frac{1}{K}\Bigr)\,\mathbb{E}\!\left[u\,G\mid x\right].

(6)

In particular, if 𝔼⁡[u​G∣x]\mathbb{E}[u\,G\mid x] is parallel to the clean gradient direction for the prompt-conditioned objective, then so is 𝔼​[Δcenter​(θ)∣x]\mathbb{E}[\Delta_{\text{center}}(\theta)\mid x].

Proof.

Expand Δcenter=1K∑iuiGi−u¯⋅1K∑iGi\Delta_{\text{center}}=\frac{1}{K}\sum_{i}u_{i}G_{i}-\bar{u}\cdot\frac{1}{K}\sum_{i}G_{i}.
Taking expectation conditioned on xx yields

𝔼[u¯⋅1K∑iGi∣x]=1K2∑i,j𝔼[ujGi∣x].\mathbb{E}[\bar{u}\cdot\tfrac{1}{K}\sum_{i}G_{i}\mid x]=\frac{1}{K^{2}}\sum_{i,j}\mathbb{E}[u_{j}G_{i}\mid x].

The i=ji=j terms contribute KK2​𝔼​[u​G∣x]\frac{K}{K^{2}}\mathbb{E}[uG\mid x].
For i≠ji\neq j, independence gives 𝔼⁡[uj​Gi∣x]=𝔼⁡[u∣x]​𝔼​[G∣x]=0\mathbb{E}[u_{j}G_{i}\mid x]=\mathbb{E}[u\mid x]\mathbb{E}[G\mid x]=0.
Thus 𝔼[u¯⋅1K∑iGi∣x]=1K𝔼[uG∣x]\mathbb{E}[\bar{u}\cdot\tfrac{1}{K}\sum_{i}G_{i}\mid x]=\frac{1}{K}\mathbb{E}[uG\mid x], implying (6).
∎

Corollary A.2 (Directional correctness of PGFC under centered GRPO-style updates).

Under the Verifier Reward Channel (Definition 3.1) and the conditional-independence assumption stated above, let u=wR~u=w_{\tilde{R}} with w0=ρ1−1w_{0}=\rho_{1}-1 and w1=ρ1w_{1}=\rho_{1} as in Proposition 3.4.
Then for each prompt xx,

𝔼⁡[Δcenter​(θ)∣x]=(1−1K)​(1−ρ0−ρ1)​∇θJ​(θ∣x),\mathbb{E}\!\left[\Delta_{\text{center}}(\theta)\mid x\right]\;=\;\Bigl(1-\frac{1}{K}\Bigr)(1-\rho_{0}-\rho_{1})\,\nabla_{\theta}J(\theta\mid x),

so the expected centered update remains aligned with the clean policy-gradient direction.

#### Binary-proxy equivalence caveat.

The corollary explains how centering interacts with a generic proxy whose score-function expectation is aligned with the clean gradient. It does not by itself prove that every PGFC proxy creates a distinct GRPO update. For binary rewards, wr~=r~+ρ1−1w_{\tilde{r}}=\tilde{r}+\rho_{1}-1 differs from r~\tilde{r} by an additive constant, so group centering removes the difference. Likewise, the hypothetical pre-centering proxy u=r~​wr~=ρ1​r~u=\tilde{r}\,w_{\tilde{r}}=\rho_{1}\tilde{r} is a positive rescaling of r~\tilde{r}; if within-group standardization is enabled, this rescaling also cancels.

#### Standardization, clipping, and KL (what is guaranteed, and what is approximate).

GRPO further divides centered proxy rewards by the within-group standard deviation to form normalized advantages, and then applies a PPO-style clipping on token-level ratios and an explicit KL penalty to πref\pi_{\mathrm{ref}} (Shao et al., 2024).
The exact direction-preservation statement in Proposition A.1 covers the centering step, which is the main nontrivial departure from vanilla REINFORCE.
Clipping and the KL penalty add further stabilizers: in the small-update regime (encouraged by the KL term and typical learning rates), clipping is rarely active and the update is close to the unclipped score-function form; when clipping activates, it intentionally limits step size and may deviate from the exact REINFORCE direction.
Importantly, our corrections target the reward-gradient component; the KL gradient is unchanged, so any global scaling factor (e.g., 1−ρ0−ρ11-\rho_{0}-\rho_{1}) can be absorbed into the effective learning rate and/or interpreted as modifying the reward–KL trade-off.

## Appendix B Implementation Details

This appendix describes the implementation of PGBC and PGFC inside a GRPO-style RLVR pipeline.
The key design choice is to insert each correction at the level of the scalar coefficient multiplying the score-function term.
PGBC is a corrected-utility method: it replaces the observed verifier reward by an estimate of the clean reward.
PGFC is a score-corrected method: it replaces the usual reward-derived advantage by a signed channel-calibrated multiplier.
In both cases, the corrected coefficient is passed directly to the PPO-style GRPO surrogate and is not converted into a binary reward proxy that is subsequently group-standardized.

### B.1 Notation and GRPO Surrogate

For a prompt xx, GRPO samples a group of KK responses

y1,…,yK∼πθold(⋅∣x).y_{1},\ldots,y_{K}\sim\pi_{\theta_{\mathrm{old}}}(\cdot\mid x).

Let r~i∈{0,1}\tilde{r}_{i}\in\{0,1\} be the observed verifier reward for response yiy_{i}.
For token tt in response ii, define the policy ratio

ri,t​(θ)=πθ​(yi,t∣x,yi,<t)πθold​(yi,t∣x,yi,<t).r_{i,t}(\theta)=\frac{\pi_{\theta}(y_{i,t}\mid x,y_{i,<t})}{\pi_{\theta_{\mathrm{old}}}(y_{i,t}\mid x,y_{i,<t})}.

Given a scalar trajectory coefficient aia_{i}, we broadcast it to all response tokens:

Ai,t≡ai,t=1,…,|yi|.A_{i,t}\equiv a_{i},\qquad t=1,\ldots,|y_{i}|.

The clipped GRPO reward surrogate is then

ℒGRPOrew​(θ)=1K​∑i=1K1|yi|​∑t=1|yi|min⁡(ri,t​(θ)​Ai,t,clip⁡(ri,t​(θ),1−ε,1+ε)​Ai,t).\mathcal{L}_{\mathrm{GRPO}}^{\mathrm{rew}}(\theta)=\frac{1}{K}\sum_{i=1}^{K}\frac{1}{|y_{i}|}\sum_{t=1}^{|y_{i}|}\min\!\left(r_{i,t}(\theta)A_{i,t},\operatorname{clip}(r_{i,t}(\theta),1-\varepsilon,1+\varepsilon)A_{i,t}\right).

The full objective keeps the usual KL penalty:

ℒGRPO(θ)=ℒGRPOrew(θ)−βKL(πθ(⋅∣x)∥πref(⋅∣x)).\mathcal{L}_{\mathrm{GRPO}}(\theta)=\mathcal{L}_{\mathrm{GRPO}}^{\mathrm{rew}}(\theta)-\beta\,\mathrm{KL}\!\left(\pi_{\theta}(\cdot\mid x)\,\|\,\pi_{\mathrm{ref}}(\cdot\mid x)\right).

At θ=θold\theta=\theta_{\mathrm{old}}, when clipping is inactive, the reward-gradient component reduces to the score-function update

∇θℒGRPOrew​(θ)=1K​∑i=1Kai​(1|yi|​∑t=1|yi|∇θ​log​πθ​(yi,t∣x,yi,<t)),\nabla_{\theta}\mathcal{L}_{\mathrm{GRPO}}^{\mathrm{rew}}(\theta)=\frac{1}{K}\sum_{i=1}^{K}a_{i}\left(\frac{1}{|y_{i}|}\sum_{t=1}^{|y_{i}|}\nabla_{\theta}\log\pi_{\theta}(y_{i,t}\mid x,y_{i,<t})\right),

up to the conventional length normalization used by the implementation.
Therefore, the scalar coefficient aia_{i} is the correct place to insert PGBC or PGFC.

### B.2 PGBC: Corrected-Utility GRPO

PGBC estimates the clean binary reward by inverting the verifier channel.
Given estimates ρ^0,ρ^1\hat{\rho}_{0},\hat{\rho}_{1}, define

c^=1−ρ^0−ρ^1.\hat{c}=1-\hat{\rho}_{0}-\hat{\rho}_{1}.

We require c^>0\hat{c}>0 and in code clamp it below by a small constant ϵc>0\epsilon_{c}>0 for numerical safety.
The corrected utility is

r^i=r~i−ρ^0c^.\widehat{r}_{i}=\frac{\tilde{r}_{i}-\hat{\rho}_{0}}{\hat{c}}.

This quantity is used as the trajectory coefficient, optionally with a variance-reduction baseline:

aiBC=r^i−biBCsBC.a_{i}^{\mathrm{BC}}=\frac{\widehat{r}_{i}-b_{i}^{\mathrm{BC}}}{s_{\mathrm{BC}}}.

Here sBC>0s_{\mathrm{BC}}>0 is a fixed or slowly moving positive scale, such as an EMA scale, and should not be the current group’s standard deviation.
The default baseline is leave-one-out:

biBC=1K−1​∑j≠ir^j(K>1),b_{i}^{\mathrm{BC}}=\frac{1}{K-1}\sum_{j\neq i}\widehat{r}_{j}\qquad(K>1),

with biBC=0b_{i}^{\mathrm{BC}}=0 when K=1K=1.
The leave-one-out baseline is independent of GiG_{i} conditional on xx, so before clipping and KL it preserves the expected score-function update:

𝔼⁡[1K​∑i=1K(r^i−biBC)​Gi|x]=𝔼⁡[r^​G∣x].\mathbb{E}\!\left[\frac{1}{K}\sum_{i=1}^{K}(\widehat{r}_{i}-b_{i}^{\mathrm{BC}})G_{i}\,\middle|\,x\right]=\mathbb{E}[\widehat{r}\,G\mid x].

When the channel rates are correct, 𝔼⁡[r^​G∣x]\mathbb{E}[\widehat{r}\,G\mid x] equals the clean reward-gradient component.
Using the group mean including the ii-th sample is also possible, but it introduces the familiar multiplicative factor 1−1/K1-1/K.

The corrected coefficient aiBCa_{i}^{\mathrm{BC}} is then broadcast to all tokens:

Ai,tBC≡aiBC.A_{i,t}^{\mathrm{BC}}\equiv a_{i}^{\mathrm{BC}}.

No current-group zz-score standardization is applied to {r^i}i=1K\{\widehat{r}_{i}\}_{i=1}^{K}, because such standardization would remove the affine calibration induced by PGBC in the binary-reward case.

### B.3 PGFC: Score-Corrected GRPO

PGFC is implemented as a score-level correction rather than as a reward proxy.
Given an estimate ρ^1\hat{\rho}_{1}, define the signed score multiplier

wr~i=r~i−(1−ρ^1)={ρ^1−1,r~i=0,ρ^1,r~i=1.w_{\tilde{r}_{i}}=\tilde{r}_{i}-(1-\hat{\rho}_{1})=\begin{cases}\hat{\rho}_{1}-1,&\tilde{r}_{i}=0,\\
\hat{\rho}_{1},&\tilde{r}_{i}=1.\end{cases}

The trajectory coefficient is

aiFC=wr~i−biFCsFC.a_{i}^{\mathrm{FC}}=\frac{w_{\tilde{r}_{i}}-b_{i}^{\mathrm{FC}}}{s_{\mathrm{FC}}}.

Our default is

biFC=0.b_{i}^{\mathrm{FC}}=0.

The reason is that subtracting the current group mean of wr~iw_{\tilde{r}_{i}} would reduce PGFC to an ordinary relative noisy-reward update, because wr~iw_{\tilde{r}_{i}} is an affine function of r~i\tilde{r}_{i}.
A fixed or historical baseline independent of the current sampled actions may be used, but current-group centering is not the default.

The scale sFC>0s_{\mathrm{FC}}>0 controls the reward–KL trade-off.
For pure score-function direction, any fixed positive scale preserves the direction.
When both noise rates are available, one may set

sFC=1−ρ^0−ρ^1s_{\mathrm{FC}}=1-\hat{\rho}_{0}-\hat{\rho}_{1}

to approximately match the clean reward-gradient magnitude.
In the FN-dominant rule-checker regime where ρ0≈0\rho_{0}\approx 0, a practical choice is

sFC=1−ρ^1.s_{\mathrm{FC}}=1-\hat{\rho}_{1}.

If no calibrated scale is desired, we set sFC=1s_{\mathrm{FC}}=1 and tune β\beta or the learning rate as usual.

The token-level advantage is

Ai,tFC≡aiFC.A_{i,t}^{\mathrm{FC}}\equiv a_{i}^{\mathrm{FC}}.

Before clipping and KL, if ρ^1=ρ1\hat{\rho}_{1}=\rho_{1}, the population score-function component satisfies

𝔼⁡[aiFC​Gi∣x]=1−ρ0−ρ1sFC​∇θJ​(θ∣x).\mathbb{E}[a_{i}^{\mathrm{FC}}G_{i}\mid x]=\frac{1-\rho_{0}-\rho_{1}}{s_{\mathrm{FC}}}\nabla_{\theta}J(\theta\mid x).

Thus PGFC preserves the clean reward-gradient direction and, with a suitable positive scale, can also calibrate the reward-gradient magnitude.
The KL gradient is not corrected; therefore sFCs_{\mathrm{FC}} and β\beta jointly determine the effective reward–KL trade-off.

#### Remark on the role of ρ^1\hat{\rho}_{1}.

The theoretical conditional-cancellation identity for PGFC uses the true ρ1\rho_{1}.
In an unclipped population score-function estimator, adding any action-independent constant to r~i\tilde{r}_{i} has zero expected gradient by the score-function identity.
However, in finite-batch GRPO with clipping, KL regularization, length normalization, and nonstationary rollouts, the fixed channel baseline 1−ρ^11-\hat{\rho}_{1} affects the realized signed advantages and the clipped surrogate.

### B.4 Why We Do Not Use Direct-Group zz-Scoring for Binary Channel Corrections

Let Zi​(u)Z_{i}(u) denote the standard group-normalized advantage

Zi​(u)=ui−u¯std⁡({uj}j=1K)+ϵ,u¯=1K​∑j=1Kuj.Z_{i}(u)=\frac{u_{i}-\bar{u}}{\operatorname{std}(\{u_{j}\}_{j=1}^{K})+\epsilon},\qquad\bar{u}=\frac{1}{K}\sum_{j=1}^{K}u_{j}.

If ui=a​r~i+bu_{i}=a\tilde{r}_{i}+b with a>0a>0, then

ui−u¯=a⁡(r~i−r~¯),std⁡({uj})=a​std⁡({r~j}),u_{i}-\bar{u}=a(\tilde{r}_{i}-\bar{\tilde{r}}),\qquad\operatorname{std}(\{u_{j}\})=a\,\operatorname{std}(\{\tilde{r}_{j}\}),

and therefore

Zi​(u)=r~i−r~¯std⁡({r~j})+ϵ/a.Z_{i}(u)=\frac{\tilde{r}_{i}-\bar{\tilde{r}}}{\operatorname{std}(\{\tilde{r}_{j}\})+\epsilon/a}.

When ϵ\epsilon is small and the group is non-degenerate, this is numerically identical to the uncorrected noisy-reward advantage.

This degeneracy applies to the most obvious binary implementations of both corrections:

r^i=r~i−ρ^01−ρ^0−ρ^1is affine in ​r~i,\widehat{r}_{i}=\frac{\tilde{r}_{i}-\hat{\rho}_{0}}{1-\hat{\rho}_{0}-\hat{\rho}_{1}}\quad\text{is affine in }\tilde{r}_{i},

and

wr~i=r~i+ρ^1−1,r~i​wr~i=ρ^1​r~ifor ​r~i∈{0,1}.w_{\tilde{r}_{i}}=\tilde{r}_{i}+\hat{\rho}_{1}-1,\qquad\tilde{r}_{i}w_{\tilde{r}_{i}}=\hat{\rho}_{1}\tilde{r}_{i}\quad\text{for }\tilde{r}_{i}\in\{0,1\}.

Thus, feeding any of these quantities into the usual current-group zz-score advantage construction can make the corrected method exactly equivalent to the uncorrected noisy baseline.
For this reason, our corrected implementations use the scalar coefficients aiBCa_{i}^{\mathrm{BC}} and aiFCa_{i}^{\mathrm{FC}} directly, with only fixed or running positive scales.

### B.5 Process-Supervised Extension

For process supervision, suppose response yiy_{i} has step-level verifier rewards

r~i(1),…,r~i(Ji)\tilde{r}_{i}^{(1)},\ldots,\tilde{r}_{i}^{(J_{i})}

attached to step boundaries

τi(1)<⋯<τi(Ji).\tau_{i}^{(1)}<\cdots<\tau_{i}^{(J_{i})}.

PGBC is applied to each step reward:

r^i(j)=r~i(j)−ρ^01−ρ^0−ρ^1.\widehat{r}_{i}^{(j)}=\frac{\tilde{r}_{i}^{(j)}-\hat{\rho}_{0}}{1-\hat{\rho}_{0}-\hat{\rho}_{1}}.

The token coefficient is the return-to-go of corrected utilities:

Ai,tBC=1sBC∑j:τi(j)≥t(r^i(j)−bi,jBC),A_{i,t}^{\mathrm{BC}}=\frac{1}{s_{\mathrm{BC}}}\sum_{j:\tau_{i}^{(j)}\geq t}\left(\widehat{r}_{i}^{(j)}-b_{i,j}^{\mathrm{BC}}\right),

where bi,jBCb_{i,j}^{\mathrm{BC}} is an optional leave-one-out or historical baseline for the corresponding step.

PGFC is applied as a step-level signed score multiplier:

wi(j)=r~i(j)−(1−ρ^1),w_{i}^{(j)}=\tilde{r}_{i}^{(j)}-(1-\hat{\rho}_{1}),

and the token coefficient is

Ai,tFC=1sFC∑j:τi(j)≥twi(j).A_{i,t}^{\mathrm{FC}}=\frac{1}{s_{\mathrm{FC}}}\sum_{j:\tau_{i}^{(j)}\geq t}w_{i}^{(j)}.

As in the outcome case, we avoid current-batch zz-scoring of these binary affine quantities.
If a positive normalization is needed for numerical stability, we use a fixed or EMA scale rather than the current batch’s standard deviation.

### B.6 When Conditional Independence Is Violated (Bias Decomposition).

Our directional-alignment results rely on conditional independence to factorize
𝔼⁡[wR~​G∣R∗]=𝔼⁡[wR~∣R∗]​𝔼​[G∣R∗]\mathbb{E}[w_{\tilde{R}}G\mid R^{*}]=\mathbb{E}[w_{\tilde{R}}\mid R^{*}]\mathbb{E}[G\mid R^{*}].
If verifier errors depend on trajectory features beyond correctness (e.g., style-based FP hacks), the update admits the decomposition

𝔼⁡[wR~​G∣R∗]=𝔼⁡[wR~∣R∗]​𝔼​[G∣R∗]+Cov⁡(wR~,G∣R∗),\mathbb{E}[w_{\tilde{R}}G\mid R^{*}]\;=\;\mathbb{E}[w_{\tilde{R}}\mid R^{*}]\mathbb{E}[G\mid R^{*}]\;+\;\mathrm{Cov}(w_{\tilde{R}},G\mid R^{*}),

so the residual bias is governed by the conditional covariance term.
This highlights a practical diagnostic: if verifier decisions are strongly predictable from superficial cues that also affect generation likelihood, Cov⁡(wR~,G∣R∗)\mathrm{Cov}(w_{\tilde{R}},G\mid R^{*}) may be non-negligible and one should combine channel-based correction with verifier hardening or instance-dependent reliability modeling.

### B.7 Online FN-Rate Estimation via Appeals

In the FN-dominant rule-checker regime, PGFC requires an estimate of the false-negative rate ρ1\rho_{1}.
At training step tt, let

𝒩R(t)={i:r~i=0},𝒫R(t)={i:r~i=1}\mathcal{N}_{\mathrm{R}}^{(t)}=\{i:\tilde{r}_{i}=0\},\qquad\mathcal{P}_{\mathrm{R}}^{(t)}=\{i:\tilde{r}_{i}=1\}

be the rule-based negatives and positives.
We appeal each rule-negative item independently with probability q∈(0,1]q\in(0,1] using a lightweight auxiliary verifier.
Let S(t)⊆𝒩R(t)S^{(t)}\subseteq\mathcal{N}_{\mathrm{R}}^{(t)} be the appealed subset, and let

𝒫L(t)⊆S(t)\mathcal{P}_{\mathrm{L}}^{(t)}\subseteq S^{(t)}

be the appealed items flipped to positive by the auxiliary verifier.
The Horvitz–Thompson estimate of the number of false negatives is

FN^(t)=|𝒫L(t)|q.\widehat{\mathrm{FN}}^{(t)}=\frac{|\mathcal{P}_{\mathrm{L}}^{(t)}|}{q}.

Assuming rule-based positives have negligible FP rate, we estimate

ρ^1(t)=FN^(t)+αFN^(t)+|𝒫R(t)|+α+β,\hat{\rho}_{1}^{(t)}=\frac{\widehat{\mathrm{FN}}^{(t)}+\alpha}{\widehat{\mathrm{FN}}^{(t)}+|\mathcal{P}_{\mathrm{R}}^{(t)}|+\alpha+\beta},

where α,β>0\alpha,\beta>0 are small pseudocounts.
To track policy drift, we use EMA smoothing:

ρ¯1(t)=λ​ρ¯1(t−1)+(1−λ)​ρ^1(t).\bar{\rho}_{1}^{(t)}=\lambda\bar{\rho}_{1}^{(t-1)}+(1-\lambda)\hat{\rho}_{1}^{(t)}.

The smoothed value ρ¯1(t)\bar{\rho}_{1}^{(t)} is used as ρ^1\hat{\rho}_{1} in PGFC.
The expected number of auxiliary verifier calls per update is

q​|𝒩R(t)|.q\,|\mathcal{N}_{\mathrm{R}}^{(t)}|.

For PGBC, both ρ0\rho_{0} and ρ1\rho_{1} are needed.
When ρ0\rho_{0} is unavailable or unreliable, we prefer PGFC in the FN-dominant setting.
When both rates can be estimated from a calibration set or from a dual-verifier protocol, PGBC can be used with the corrected utility above.

## Appendix C Additional Experimental Results

### C.1 Performance under Pass@8 Metric

Table 3 retains the measured pass@8 results for the four backbones. The conclusion remains consistent with the pass@1 results: PGBC and PGFC provide reliable improvements over the noisy baseline.

### C.2 Complementarity with Stronger Verifiers

We additionally investigate whether the proposed correction mechanisms are synergistic with more capable verifiers. While our main experiments instantiated the appeal process with a lightweight LLM verifier (TinyV) to minimize computational overhead, Table 5 demonstrates that the forward correction yields consistent improvements even when complementing stronger verifier baselines. Specifically, we compare against a “Stronger checker” that extracts the final \boxed{} answer and applies numeric/rational equivalence checking, using the Math-Verify library as a robust baseline. Concretely, we parse the gold answer using a gold-appropriate extraction configuration (ExprExtractionConfig for plain expressions or LatexExtractionConfig for LaTeX), and parse model predictions using LatexExtractionConfig together with ExprExtractionConfig. Verification is then performed by Math-Verify’s parse-and-verify pipeline with reward-verification-oriented normalization. Under this setup, PGFC uses the standard rule-based reward as the primary signal and calls the auxiliary Math-Verify checker only on appealed rule-negative samples. With the synthetic noise rates fixed at ρ0=0.1\rho_{0}=0.1 and ρ1=0.2\rho_{1}=0.2 as in the main paper, our Appeals+PGFC method achieves notable gains over the strong baseline (e.g., on MATH500 and AMC2023). These results suggest that the theoretical corrections act orthogonally to verifier engineering: regardless of how accurate the underlying verifier is, explicitly modeling and correcting for the residual false-negative rate provides a reliable performance lift.

### C.3 Training Dynamics under Synthetic Noise

To better understand how the proposed corrections influence the learning process, we analyze the training dynamics under synthetic i.i.d. noise. As shown in Figure 5, we monitor the group reward standard deviation, normalized advantage standard deviation, and gradient norm across training steps. The purpose of this analysis is to verify that the backward and forward corrections actively modify the advantage construction during training, rather than merely shifting the final endpoint scores. The results demonstrate that both PGBC and PGFC measurably alter these intermediate training statistics relative to the uncorrected noisy baseline, providing evidence that our corrections dynamically adjust the policy gradient throughout the optimization process.

Figure 5: Training dynamics under synthetic iid noise. PGBC and PGFC change the group reward standard deviation, normalized advantage standard deviation, and gradient norm relative to uncorrected noisy training, illustrating that the correction is active inside advantage construction rather than only changing endpoint scores.

Table 3: Pass@8 under real-world noise.

Dataset
AIME2024
AIME2025
AMC2023
MATH500
Minerva MATH
Olympiad Bench
Average

Qwen2.5-Math-1.5B

Base
32.4 ±\pm 0.5
16.7 ±\pm 0.7
79.3 ±\pm 1.4
62.8 ±\pm 1.3
15.5 ±\pm 1.1
31.3 ±\pm 0.8
39.7 ±\pm 1.0

Rule
34.3 ±\pm 1.2
19.9 ±\pm 1.1
80.7 ±\pm 1.4
69.6 ±\pm 0.5
18.0 ±\pm 0.6
32.8 ±\pm 1.2
42.6 ±\pm 1.0

LLM-as-Judge
29.6 ±\pm 1.1
15.4 ±\pm 0.4
80.0 ±\pm 0.6
63.4 ±\pm 1.2
16.2 ±\pm 0.8
28.6 ±\pm 0.3
38.9 ±\pm 0.7

Appeals
30.5 ±\pm 0.2
20.5 ±\pm 0.7
80.7 ±\pm 0.9
68.9 ±\pm 1.3
17.6 ±\pm 1.0
30.5 ±\pm 0.5
41.5 ±\pm 0.8

Appeals+PGFC (Ours)
31.0 ±\pm 0.2
20.0 ±\pm 0.6
82.2 ±\pm 0.4
69.8 ±\pm 1.1
18.2 ±\pm 0.5
33.3 ±\pm 0.3
42.4 ±\pm 0.5

DeepSeek-R1-Distill-Qwen-1.5B

Base
44.8 ±\pm 0.8
32.8 ±\pm 0.7
88.2 ±\pm 0.1
85.9 ±\pm 0.6
27.8 ±\pm 0.3
48.6 ±\pm 0.3
54.7 ±\pm 0.4

Rule
55.1 ±\pm 0.6
40.1 ±\pm 0.4
96.1 ±\pm 0.2
96.6 ±\pm 0.1
44.6 ±\pm 0.1
64.9 ±\pm 0.1
66.2 ±\pm 0.1

LLM-as-Judge
55.4 ±\pm 0.9
39.8 ±\pm 0.7
96.2 ±\pm 0.2
95.7 ±\pm 0.2
43.2 ±\pm 0.7
62.8 ±\pm 0.7
65.5 ±\pm 0.3

Appeals
57.7 ±\pm 1.0
42.5 ±\pm 0.8
96.0 ±\pm 0.2
96.4 ±\pm 0.2
44.2 ±\pm 0.8
64.5 ±\pm 0.8
66.9 ±\pm 0.3

Appeals+PGFC (Ours)
61.3 ±\pm 0.6
44.6 ±\pm 0.7
98.6 ±\pm 0.1
97.1 ±\pm 0.2
46.8 ±\pm 0.6
66.1 ±\pm 0.4
69.1 ±\pm 0.2

Llama-3.2-3B-Instruct

Base
18.8 ±\pm 1.1
3.3 ±\pm 0.2
54.7 ±\pm 1.4
40.8 ±\pm 0.8
5.2 ±\pm 1.1
16.4 ±\pm 0.5
23.2 ±\pm 0.8

Rule
22.4 ±\pm 1.0
6.7 ±\pm 1.4
60.0 ±\pm 1.3
44.8 ±\pm 0.6
13.3 ±\pm 0.7
18.7 ±\pm 1.5
27.7 ±\pm 1.1

LLM-as-Judge
10.0 ±\pm 0.9
0.8 ±\pm 0.9
44.4 ±\pm 1.4
27.2 ±\pm 0.9
6.7 ±\pm 1.4
9.5 ±\pm 0.2
16.4 ±\pm 0.9

Appeals
17.5 ±\pm 0.2
4.2 ±\pm 1.0
53.8 ±\pm 0.2
42.3 ±\pm 1.5
10.8 ±\pm 1.6
14.9 ±\pm 1.2
23.9 ±\pm 0.9

Appeals+PGFC (Ours)
20.8 ±\pm 0.9
3.3 ±\pm 1.5
58.1 ±\pm 1.3
47.6 ±\pm 0.6
12.6 ±\pm 1.7
18.5 ±\pm 0.6
26.8 ±\pm 1.0

Qwen2.5-Math-7B

Base
36.2 ±\pm 1.2
23.3 ±\pm 1.0
81.9 ±\pm 1.3
66.6 ±\pm 0.5
11.8 ±\pm 0.6
33.9 ±\pm 0.7
42.3 ±\pm 0.9

Rule
50.0 ±\pm 0.1
28.7 ±\pm 0.8
83.4 ±\pm 0.6
82.8 ±\pm 0.5
29.0 ±\pm 1.1
45.8 ±\pm 1.3
53.3 ±\pm 0.7

LLM-as-Judge
41.7 ±\pm 0.3
22.1 ±\pm 0.3
81.9 ±\pm 1.5
69.0 ±\pm 0.2
13.2 ±\pm 1.2
39.4 ±\pm 1.1
44.6 ±\pm 0.8

Appeals
47.1 ±\pm 1.0
30.4 ±\pm 0.3
84.4 ±\pm 1.2
80.8 ±\pm 0.3
23.5 ±\pm 1.3
45.6 ±\pm 0.5
52.0 ±\pm 0.8

Appeals+PGFC (Ours)
54.6 ±\pm 1.4
30.4 ±\pm 1.2
82.8 ±\pm 0.2
83.2 ±\pm 1.3
29.0 ±\pm 0.6
47.6 ±\pm 0.9
54.6 ±\pm 0.9

### C.4 Appeals Statistics and Computational Overhead

To quantify the computational cost and the empirical behavior of the appeal mechanism under real-world verifier noise, we track the appeal and flip statistics during training on Qwen2.5-Math-1.5B. As detailed in Table 4, we measure the appeal rate (the fraction of rollout responses that trigger an appeal) and the flip rate (the fraction of appealed responses that are successfully overturned by the LLM judge). The two methods use the same negative-side appeal mechanism. Within Appeals+PGFC, these calls support both reward recovery and online FN-rate estimation, without a separate post-appeal verifier pass. The total number of auxiliary TinyV calls remains small relative to the total number of training rollouts, demonstrating that our online false-negative rate estimation and forward correction are highly computationally efficient.

Table 4: Appeals statistics for Qwen2.5-Math-1.5B real-world verifier noise. Appeals+PGFC uses the same appeal stream both for recovery and for online FN-rate estimation.

Method
Avg pass@1
Avg pass@8
Appeal rate
Flip rate
TinyV calls

Rule
31.6±0.431.6{\pm}0.4
42.6±1.0\mathbf{42.6{\pm}1.0}
0.000
0.0000
0

Appeals
30.1±0.630.1{\pm}0.6
41.5±0.841.5{\pm}0.8
0.081
0.2288
7,963

Appeals+PGFC
33.7±0.8\mathbf{33.7{\pm}0.8}
42.4±0.542.4{\pm}0.5
0.093
0.2745
8,255

Table 5: Complementarity with a stronger verifier-side baseline on Qwen2.5-Math-1.5B. The correction still improves over a stronger checker, indicating that PGFC is not merely replacing verifier engineering.

Method
MATH500
AIME2024
AIME2025
AMC2023
Minerva Math
OlympiadBench
Average

Stronger checker
68.1 / 69.2
12.3 / 18.4
7.2 / 12.3
47.9 / 59.7
17.8 / 18.6
30.9 / 33.1
30.7 / 35.2

Appeals+PGFC
72.0 / 75.1
14.2 / 21.6
8.8 / 15.8
51.8 / 65.8
20.9 / 23.8
33.3 / 37.2
33.5 / 39.9

### C.5 General Capability Retention

We also check whether the corrections preserve non-math general benchmark performance relative to noisy training. Table 6 reports that PGBC and PGFC recover most of the retention loss caused by uncorrected noisy rewards and remain close to Base/Oracle on these auxiliary evaluations.

Table 6: General capability retention after RLVR training on Llama-3.2-3B-Instruct. Metrics are accuracies.

Method
MMLU
ARC-Challenge
HellaSwag
GPQA

Base
60.7
73.9
55.0
28.4

Oracle
61.1
73.9
55.9
29.1

Noise
50.0
43.9
33.9
19.4

PGBC
60.8
73.8
55.6
28.8

PGFC
61.3
74.2
56.1
29.2

## Appendix D Proofs and Derivations

### D.1 Proof of Proposition 3.2

Proof.

We compute the expectation of the noisy reward R~\tilde{R} conditioned on the clean reward R∗R^{*}, which is a binary variable. By the definition of expectation:

𝔼⁡[R~]\displaystyle\mathbb{E}[\tilde{R}]
=1⋅ℙ⁡(R~=1∣R∗)+0⋅ℙ⁡(R~=0∣R∗)\displaystyle=1\cdot\mathbb{P}(\tilde{R}=1\mid R^{*})+0\cdot\mathbb{P}(\tilde{R}=0\mid R^{*})

=ℙ⁡(R~=1∣R∗).\displaystyle=\mathbb{P}(\tilde{R}=1\mid R^{*}).

We can expand this using the law of total probability, conditioning on the value of R∗∈{0,1}R^{*}\in\{0,1\}:

𝔼⁡[R~∣R∗]\displaystyle\mathbb{E}[\tilde{R}\mid R^{*}]
=R∗⋅ℙ⁡(R~=1∣R∗=1)+(1−R∗)⋅ℙ⁡(R~=1∣R∗=0).\displaystyle=R^{*}\cdot\mathbb{P}(\tilde{R}=1\mid R^{*}=1)+(1-R^{*})\cdot\mathbb{P}(\tilde{R}=1\mid R^{*}=0).

From Definition 3.1, we have ℙ⁡(R~=1∣R∗=0)=ρ0\mathbb{P}(\tilde{R}=1\mid R^{*}=0)=\rho_{0} and ℙ⁡(R~=0∣R∗=1)=ρ1\mathbb{P}(\tilde{R}=0\mid R^{*}=1)=\rho_{1}, which implies ℙ⁡(R~=1∣R∗=1)=1−ρ1\mathbb{P}(\tilde{R}=1\mid R^{*}=1)=1-\rho_{1}. Substituting these values:

𝔼⁡[R~∣R∗]\displaystyle\mathbb{E}[\tilde{R}\mid R^{*}]
=R∗​(1−ρ1)+(1−R∗)​ρ0\displaystyle=R^{*}(1-\rho_{1})+(1-R^{*})\rho_{0}

=R∗−ρ1​R∗+ρ0−ρ0​R∗\displaystyle=R^{*}-\rho_{1}R^{*}+\rho_{0}-\rho_{0}R^{*}

=(1−ρ0−ρ1)​R∗+ρ0.\displaystyle=(1-\rho_{0}-\rho_{1})R^{*}+\rho_{0}.

This completes the proof.
∎

### D.2 Proof of Theorem 3.3

Proof.

Recall the verifier reward channel (Definition 3.1): for the latent clean reward
R∗∈{0,1}R^{*}\in\{0,1\} and the observed noisy reward R~∈{0,1}\tilde{R}\in\{0,1\},

Pr⁡(R~=1∣R∗=0)=ρ0,Pr⁡(R~=0∣R∗=1)=ρ1,\Pr(\tilde{R}=1\mid R^{*}=0)=\rho_{0},\qquad\Pr(\tilde{R}=0\mid R^{*}=1)=\rho_{1},

hence Pr⁡(R~=1∣R∗=1)=1−ρ1\Pr(\tilde{R}=1\mid R^{*}=1)=1-\rho_{1} and Pr⁡(R~=0∣R∗=0)=1−ρ0\Pr(\tilde{R}=0\mid R^{*}=0)=1-\rho_{0}.
Since 1−ρ0−ρ1>01-\rho_{0}-\rho_{1}>0, the estimator

R^≜R~−ρ01−ρ0−ρ1\widehat{R}\;\triangleq\;\frac{\tilde{R}-\rho_{0}}{1-\rho_{0}-\rho_{1}}

is well-defined.

We prove unbiasedness by computing the conditional expectation given R∗R^{*}.
First note that because R~\tilde{R} is binary,

𝔼⁡[R~∣R∗]= 1⋅Pr⁡(R~=1∣R∗)+0⋅Pr⁡(R~=0∣R∗)=Pr⁡(R~=1∣R∗).\mathbb{E}[\tilde{R}\mid R^{*}]\;=\;1\cdot\Pr(\tilde{R}=1\mid R^{*})+0\cdot\Pr(\tilde{R}=0\mid R^{*})\;=\;\Pr(\tilde{R}=1\mid R^{*}).

(7)

By the channel definition, for the two possible values of R∗R^{*} we have

𝔼⁡[R~∣R∗=1]=1−ρ1,𝔼⁡[R~∣R∗=0]=ρ0.\mathbb{E}[\tilde{R}\mid R^{*}=1]=1-\rho_{1},\qquad\mathbb{E}[\tilde{R}\mid R^{*}=0]=\rho_{0}.

These two cases can be written compactly as the affine form (Proposition 3.2)

𝔼⁡[R~∣R∗]=(1−ρ0−ρ1)​R∗+ρ0.\mathbb{E}[\tilde{R}\mid R^{*}]=(1-\rho_{0}-\rho_{1})R^{*}+\rho_{0}.

(8)

Now take the conditional expectation of R^\widehat{R}:

𝔼⁡[R^∣R∗]\displaystyle\mathbb{E}[\widehat{R}\mid R^{*}]
=𝔼[R~−ρ01−ρ0−ρ1|R∗]\displaystyle=\mathbb{E}\left[\left.\frac{\tilde{R}-\rho_{0}}{1-\rho_{0}-\rho_{1}}\right|R^{*}\right]

=𝔼⁡[R~∣R∗]−ρ01−ρ0−ρ1\displaystyle=\frac{\mathbb{E}[\tilde{R}\mid R^{*}]-\rho_{0}}{1-\rho_{0}-\rho_{1}}

=(1−ρ0−ρ1)​R∗+ρ0−ρ01−ρ0−ρ1(by (8))\displaystyle=\frac{(1-\rho_{0}-\rho_{1})R^{*}+\rho_{0}-\rho_{0}}{1-\rho_{0}-\rho_{1}}\quad\text{(by \eqref{eq:affine})}

=R∗.\displaystyle=R^{*}.

(9)

Equation (9) shows that R^\widehat{R} is an unbiased estimator of the
latent clean reward in the conditional sense.

Finally, taking total expectation (law of iterated expectation) yields

𝔼⁡[R^]=𝔼⁡[𝔼⁡[R^∣R∗]]=𝔼⁡[R∗],\mathbb{E}[\widehat{R}]=\mathbb{E}\bigl[\mathbb{E}[\widehat{R}\mid R^{*}]\bigr]=\mathbb{E}[R^{*}],

so R^\widehat{R} is unbiased for the clean reward both conditionally and unconditionally.
∎

### D.3 Proof of Proposition 3.4

Proof.

The proposition states two claims about the conditional expectation of the forward weights. The weights are defined as:

wR~={w0=ρ1−1if ​R~=0,w1=ρ1if ​R~=1.w_{\tilde{R}}\;=\;\begin{cases}w_{0}=\rho_{1}-1&\text{if }\tilde{R}=0,\\
w_{1}=\rho_{1}&\text{if }\tilde{R}=1.\end{cases}

The noise model provides the conditional probabilities:

Pr⁡(R~=0∣R∗=1)\displaystyle\Pr(\tilde{R}=0\mid R^{*}=1)
=ρ1,Pr⁡(R~=1∣R∗=1)=1−ρ1\displaystyle=\rho_{1},\qquad\Pr(\tilde{R}=1\mid R^{*}=1)=1-\rho_{1}

Pr⁡(R~=1∣R∗=0)\displaystyle\Pr(\tilde{R}=1\mid R^{*}=0)
=ρ0,Pr⁡(R~=0∣R∗=0)=1−ρ0\displaystyle=\rho_{0},\qquad\Pr(\tilde{R}=0\mid R^{*}=0)=1-\rho_{0}

#### Part 1: Proof of 𝔼⁡[wR~∣R∗=1]=0\mathbb{E}[w_{\tilde{R}}\mid R^{*}=1]=0

We compute the expectation of wR~w_{\tilde{R}} conditioned on the true reward being positive (R∗=1R^{*}=1):

𝔼⁡[wR~∣R∗=1]\displaystyle\mathbb{E}[w_{\tilde{R}}\mid R^{*}=1]
=∑k∈{0,1}wk⋅Pr⁡(R~=k∣R∗=1)\displaystyle=\sum_{k\in\{0,1\}}w_{k}\cdot\Pr(\tilde{R}=k\mid R^{*}=1)

=w0⋅Pr⁡(R~=0∣R∗=1)+w1⋅Pr⁡(R~=1∣R∗=1)\displaystyle=w_{0}\cdot\Pr(\tilde{R}=0\mid R^{*}=1)+w_{1}\cdot\Pr(\tilde{R}=1\mid R^{*}=1)

=(ρ1−1)⋅(ρ1)+(ρ1)⋅(1−ρ1)\displaystyle=(\rho_{1}-1)\cdot(\rho_{1})+(\rho_{1})\cdot(1-\rho_{1})

=(ρ12−ρ1)+(ρ1−ρ12)\displaystyle=(\rho_{1}^{2}-\rho_{1})+(\rho_{1}-\rho_{1}^{2})

=0.\displaystyle=0.

#### Part 2: Proof of 𝔼⁡[wR~∣R∗=0]=−(1−ρ0−ρ1)\mathbb{E}[w_{\tilde{R}}\mid R^{*}=0]=-(1-\rho_{0}-\rho_{1})

Next, we compute the expectation of wR~w_{\tilde{R}} conditioned on the true reward being negative (R∗=0R^{*}=0):

𝔼⁡[wR~∣R∗=0]\displaystyle\mathbb{E}[w_{\tilde{R}}\mid R^{*}=0]
=∑k∈{0,1}wk⋅Pr⁡(R~=k∣R∗=0)\displaystyle=\sum_{k\in\{0,1\}}w_{k}\cdot\Pr(\tilde{R}=k\mid R^{*}=0)

=w0⋅Pr⁡(R~=0∣R∗=0)+w1⋅Pr⁡(R~=1∣R∗=0)\displaystyle=w_{0}\cdot\Pr(\tilde{R}=0\mid R^{*}=0)+w_{1}\cdot\Pr(\tilde{R}=1\mid R^{*}=0)

=(ρ1−1)⋅(1−ρ0)+(ρ1)⋅(ρ0)\displaystyle=(\rho_{1}-1)\cdot(1-\rho_{0})+(\rho_{1})\cdot(\rho_{0})

=(ρ1−ρ0​ρ1−1+ρ0)+ρ0​ρ1\displaystyle=(\rho_{1}-\rho_{0}\rho_{1}-1+\rho_{0})+\rho_{0}\rho_{1}

=ρ1+ρ0−1\displaystyle=\rho_{1}+\rho_{0}-1

=−(1−ρ0−ρ1).\displaystyle=-(1-\rho_{0}-\rho_{1}).

This proves both claims of the proposition.
∎

### D.4 Proof of Theorem 3.5

Proof.

We want to show that 𝔼⁡[Δ​θ]=(1−ρ0−ρ1)​∇θJ​(θ)\mathbb{E}[\Delta\theta]=(1-\rho_{0}-\rho_{1})\,\nabla_{\theta}J(\theta), where Δ​θ=1M​∑t=1Mht\Delta\theta=\frac{1}{M}\sum_{t=1}^{M}h_{t} and ht=wR~​Gth_{t}=w_{\tilde{R}}G_{t}. By linearity of expectation and assuming i.i.d. samples, it suffices to show this for a single sample’s contribution, 𝔼⁡[ht]\mathbb{E}[h_{t}].

We use the law of total expectation, conditioning on the latent true reward R∗∈{0,1}R^{*}\in\{0,1\}:

𝔼⁡[ht]=𝔼⁡[wR~​Gt]\displaystyle\mathbb{E}[h_{t}]=\mathbb{E}[w_{\tilde{R}}G_{t}]
=𝔼⁡[𝔼⁡[wR~​Gt∣R∗]]\displaystyle=\mathbb{E}\left[\mathbb{E}[w_{\tilde{R}}G_{t}\mid R^{*}]\right]

=Pr⁡(R∗=1)​𝔼​[wR~​Gt∣R∗=1]+Pr⁡(R∗=0)​𝔼​[wR~​Gt∣R∗=0].\displaystyle=\Pr(R^{*}=1)\,\mathbb{E}[w_{\tilde{R}}G_{t}\mid R^{*}=1]+\Pr(R^{*}=0)\,\mathbb{E}[w_{\tilde{R}}G_{t}\mid R^{*}=0].

The noise process generating R~\tilde{R} is independent of the policy’s action generation process (which produces GtG_{t}), conditional on the true reward R∗R^{*}. Thus, we can separate the expectations:

𝔼⁡[wR~​Gt∣R∗]=𝔼⁡[wR~∣R∗]⋅𝔼⁡[Gt∣R∗].\mathbb{E}[w_{\tilde{R}}G_{t}\mid R^{*}]=\mathbb{E}[w_{\tilde{R}}\mid R^{*}]\cdot\mathbb{E}[G_{t}\mid R^{*}].

Using the results from Proposition 3.4:

• • 

𝔼⁡[wR~∣R∗=1]=0\mathbb{E}[w_{\tilde{R}}\mid R^{*}=1]=0.

• • 

𝔼⁡[wR~∣R∗=0]=−(1−ρ0−ρ1)\mathbb{E}[w_{\tilde{R}}\mid R^{*}=0]=-(1-\rho_{0}-\rho_{1}).

Substituting these back into the main expectation formula:

𝔼⁡[wR~​Gt]\displaystyle\mathbb{E}[w_{\tilde{R}}G_{t}]
=Pr⁡(R∗=1)⋅(0)⋅𝔼⁡[Gt∣R∗=1]\displaystyle=\Pr(R^{*}=1)\cdot(0)\cdot\mathbb{E}[G_{t}\mid R^{*}=1]

+Pr(R∗=0)⋅(−(1−ρ0−ρ1))⋅𝔼[Gt∣R∗=0]\displaystyle\quad+\Pr(R^{*}=0)\cdot(-(1-\rho_{0}-\rho_{1}))\cdot\mathbb{E}[G_{t}\mid R^{*}=0]

=−(1−ρ0−ρ1)⋅Pr(R∗=0)𝔼[Gt∣R∗=0]\displaystyle=-(1-\rho_{0}-\rho_{1})\cdot\Pr(R^{*}=0)\mathbb{E}[G_{t}\mid R^{*}=0]

=−(1−ρ0−ρ1)⋅𝔼[𝟏{R∗=0}Gt],\displaystyle=-(1-\rho_{0}-\rho_{1})\cdot\mathbb{E}[\mathbf{1}_{\{R^{*}=0\}}G_{t}],

where 𝟏{⋅}\mathbf{1}_{\{\cdot\}} is the indicator function.
From two fundamental properties of the score function:

• 1. 

The unconditional expectation is zero: 𝔼⁡[Gt]=0\mathbb{E}[G_{t}]=0 (Williams, 1992; Sutton et al., 1999).

• 2. 

The clean policy gradient is ∇θJ​(θ)=𝔼⁡[R∗​Gt]\nabla_{\theta}J(\theta)=\mathbb{E}[R^{*}G_{t}].

From property 1, we have 𝔼[Gt]=𝔼[(𝟏{R∗=1}+𝟏{R∗=0})Gt]=𝔼[R∗Gt]+𝔼[𝟏{R∗=0}Gt]=0\mathbb{E}[G_{t}]=\mathbb{E}[(\mathbf{1}_{\{R^{*}=1\}}+\mathbf{1}_{\{R^{*}=0\}})G_{t}]=\mathbb{E}[R^{*}G_{t}]+\mathbb{E}[\mathbf{1}_{\{R^{*}=0\}}G_{t}]=0.
This implies that 𝔼[𝟏{R∗=0}Gt]=−𝔼[R∗Gt]=−∇θJ(θ)\mathbb{E}[\mathbf{1}_{\{R^{*}=0\}}G_{t}]=-\mathbb{E}[R^{*}G_{t}]=-\nabla_{\theta}J(\theta).

Finally, we substitute this back into our expression for the expected update direction:

𝔼⁡[ht]\displaystyle\mathbb{E}[h_{t}]
=𝔼⁡[wR~​Gt]\displaystyle=\mathbb{E}[w_{\tilde{R}}G_{t}]

=−(1−ρ0−ρ1)⋅𝔼[𝟏{R∗=0}Gt]\displaystyle=-(1-\rho_{0}-\rho_{1})\cdot\mathbb{E}[\mathbf{1}_{\{R^{*}=0\}}G_{t}]

=−(1−ρ0−ρ1)⋅(−∇θJ(θ))\displaystyle=-(1-\rho_{0}-\rho_{1})\cdot(-\nabla_{\theta}J(\theta))

=(1−ρ0−ρ1)​∇θJ​(θ).\displaystyle=(1-\rho_{0}-\rho_{1})\nabla_{\theta}J(\theta).

Therefore, the expectation of the full update is 𝔼⁡[Δ​θ]=1M​∑𝔼⁡[ht]=(1−ρ0−ρ1)​∇θJ​(θ)\mathbb{E}[\Delta\theta]=\frac{1}{M}\sum\mathbb{E}[h_{t}]=(1-\rho_{0}-\rho_{1})\nabla_{\theta}J(\theta). This completes the proof.
∎

## Appendix E Prompt Templates and Training/Evaluation Details

This section records the exact prompt formats and the concrete hyperparameters we used for all experiments in this paper.

### E.1 Prompt Templates

#### Training (generation) prompt.

For each math problem xx (a plain-text question), the user message is built by concatenating the raw question with a short instruction that elicits chain-of-thought and enforces a verifiable answer format.

⬇
<user>

{QUESTION}

Let’s think step by step and enclose the reasoning process within <think> and </think> tags.

The final result in the answer MUST BE within \boxed{}.

</user>

During data preprocessing, we write chat-style JSON with a single user turn as shown above and attach the rule-based ground-truth answer for reward checking.

#### Evaluation (validation/test) prompt.

We use the same prompt template as training for validation and test-time generation so that the rule-based verifier can parse the boxed answer consistently.

#### Verifier I/O.

The rule-based checker operates on the model’s final string and extracts the last \boxed{...} expression; it then applies numeric/rational parsing and equality tests to produce a binary reward R~∈{0,1}\tilde{R}\in\{0,1\}.
When the LLM verifier is enabled, it receives the pair (problem,model solution)(\text{problem},\text{model solution}) and returns a binary correctness decision used only to estimate the false negative rate ρ1\rho_{1} over a sliding window. The LLM verifier does not replace the rule-based reward.

### E.2 Data Preprocessing

We load the preview split of the math-reasoning corpus and map each example to a chat-style record as above, keeping the reference (ground-truth) answer for programmatic checking.

### E.3 Training Configuration

Table 7: Core training settings.

Training (GRPO)

Train batch size
128

Rollouts per question (group size)
8

Max prompt length (tokens)
512

Max response length (tokens)
3072

Sampling temperature (rollouts)
1.0

Advantage estimator
GRPO

KL regularization
Enabled

KL coefficient β\beta
0.001

Entropy coefficient
0.0

Optimizer
AdamW

Learning rate
3e-6

Total epochs
1

#### Model/backbone.

We load the base model from local cache (HuggingFace layout), enable FSDP2 for actor/ref, and use shared-memory weights with remove-padding for efficient vLLM rollouts. The KL is computed w.r.t. a frozen reference initialized from the same base.

### E.4 Online FN-Rate Estimation Hyperparameters and Ablations

This subsection reports the concrete hyperparameters for our online false-negative (FN) rate estimation ρ^1\hat{\rho}_{1} used in the real-world-noise experiments (Section 4.3).

#### Appeals protocol and estimator.

At training step tt, let 𝒩R(t)\mathcal{N}_{\mathrm{R}}^{(t)} and 𝒫R(t)\mathcal{P}_{\mathrm{R}}^{(t)} be the sets labeled negative/positive by the primary rule-based verifier.
We appeal each item in 𝒩R(t)\mathcal{N}_{\mathrm{R}}^{(t)} independently with probability q∈(0,1]q\in(0,1] and re-evaluate it with a lightweight LLM verifier (TinyV).
Let 𝒫L(t)\mathcal{P}_{\mathrm{L}}^{(t)} be the appealed negatives that TinyV flips to positive.
We use the Horvitz–Thompson estimator

FN^(t)=|𝒫L(t)|q\widehat{\mathrm{FN}}^{(t)}\;=\;\frac{|\mathcal{P}_{\mathrm{L}}^{(t)}|}{q}

(10)

and estimate the FN rate with a Beta prior:

ρ^1(t)=FN^(t)+αFN^(t)+|𝒫R(t)|+α+β.\hat{\rho}_{1}^{(t)}\;=\;\frac{\widehat{\mathrm{FN}}^{(t)}+\alpha}{\widehat{\mathrm{FN}}^{(t)}+|\mathcal{P}_{\mathrm{R}}^{(t)}|+\alpha+\beta}\,.

(11)

We then apply exponential moving average (EMA) smoothing

ρ¯1(t)=λ​ρ¯1(t−1)+(1−λ)​ρ^1(t),\bar{\rho}_{1}^{(t)}\;=\;\lambda\,\bar{\rho}_{1}^{(t-1)}+(1-\lambda)\,\hat{\rho}_{1}^{(t)}\,,

(12)

and use ρ¯1(t)\bar{\rho}_{1}^{(t)} as the plug-in estimate for PGFC weights wr~∈{ρ¯1(t)−1,ρ¯1(t)}w_{\tilde{r}}\in\{\bar{\rho}_{1}^{(t)}-1,\ \bar{\rho}_{1}^{(t)}\}.

#### Default hyperparameters.

Unless otherwise stated, real-world-noise runs use:
(i) appeal probability q=0.1q=0.1;
(ii) Beta prior pseudocounts α=β=10−5\alpha=\beta=10^{-5} in Eq. (11);
(iii) EMA decay λ=0.9\lambda=0.9 in Eq. (12).
We compute ρ^1(t)\hat{\rho}_{1}^{(t)} and update ρ¯1(t)\bar{\rho}_{1}^{(t)} once per policy-update step.
The expected number of TinyV calls per update is q⋅|𝒩R(t)|q\cdot|\mathcal{N}_{\mathrm{R}}^{(t)}|.

### E.5 Datasets

#### Training.

• • 

DeepScaleR (Luo et al., 2025): the math-reasoning corpus used for RLVR rollouts and policy updates.

#### Evaluation.

We evaluate with the standard official/problem releases for each benchmark.

• • 

MATH500 (Lightman et al., 2024): a verifiable subset of math reasoning problems for reliable evaluation.

• • 

AIME 2024 (HuggingFaceH4, 2024): the 2024 American Invitational Mathematics Examination set.

• • 

AIME 2025 (OpenCompass, 2025): the 2025 AIME set.

• • 

AMC 2023 (math-ai, 2025): problems from the 2023 American Mathematics Competitions.

• • 

Minerva Math (Lewkowycz et al., 2022): the Minerva math evaluation suite.

• • 

OlympiadBench (He et al., 2024): olympiad-level mathematics benchmark.

• • 

MMLU (Hendrycks et al., 2021): a broad multi-task benchmark covering 57 academic and professional subjects for evaluating world knowledge and problem solving.

• • 

ARC-C (Clark et al., 2018): the Challenge split of the AI2 Reasoning Challenge, consisting of grade-school science questions that are difficult for retrieval and word co-occurrence baselines.

• • 

HellaSwag (Zellers et al., 2019): a commonsense natural language inference benchmark for physically grounded sentence-completion reasoning.

• • 

GPQA (Rein et al., 2024): a graduate-level, Google-proof multiple-choice QA benchmark written by domain experts in biology, physics, and chemistry.

## Appendix F False Positive (FP) and False Negative (FN) Examples

We also provide typical failure modes observed during math RL with automated verifiers on Qwen2.5-Math-7B under MATH500 dataset. For rule-based verifier: 52 FNs and 0 FP out of 500 items (marginal rates 10.4% and 0%); for LLM verifier: 81 FNs and 168 FPs out of 500 items (marginal rates 16.2% and 33.6%). The FP case shows an LLM judge over-crediting a malformed solution, while the FN case shows a rule-based checker rejecting a numerically correct answer due to formatting. The raw JSON context for these examples is provided below.

False Positive (FP). 
Problem. Compute: 1−2+3−4+⋯+99−1001-2+3-4+\dots+99-100. 
Ground truth. −50\boxed{-50} 

Model response (excerpt).
⬇
Compute: $1+2-3-4+5+6-7-8+\dots+97+98-99-100$.

\boxed{ } \boxed{ } \boxed{ } \dots

Verifier signals. Rule-based checker: ✗ (incorrect); LLM judge: ✓ (incorrectly accepts)  ⇒\Rightarrow FP.

False Negative (FN). 
Problem. Each of seven islands independently has treasure with probability 15\tfrac{1}{5}. What is the probability that exactly four islands have treasure? 
Correct answer. 44815625\displaystyle\boxed{\frac{448}{15625}} (equals 0.0286720.028672). 

Model answer. 0.028672\boxed{0.028672} 
Verifier signals. Rule-based exact-match: ✗ (expects a fraction); numeric equivalence check: ✓ (values match)  ⇒\Rightarrow FN.

We provide FP and FN examples using Qwen2.5-Math-7B base model on MATH500.

#### FP

⬇
{

    "idx": 16,

    "question": "Compute: $1-2+3-4+5- \\dots +99-100$.",

    "model_prediction": "{}",

    "model_response": "Compute: $1+2-3-4+5+6-7-8+ \\dots +97+98-99-100$.  \\boxed{{}}. \\boxed{{}}. \\boxed{{}}. \\boxed{{}}. \\boxed{{}}. \\boxed{{}}. \\boxed{{}}. \\boxed{{}}. \\boxed{{}}. \\boxed{{}}. \\boxed{{}}. \\boxed{{}}. \\boxed{{}}. \\boxed{{}}. \\boxed{{}}. \\boxed{{}}. \\boxed{{}}. \\boxed{{}}. \\boxed{{}}. \\boxed{{}}. \\boxed{{}}. \\boxed{{}}. \\boxed{{}}. \\boxed{{}}. \\boxed{{}}. \\boxed{{}}. \\boxed{{}}. \\boxed{{}}. \\boxed{{}}. \\boxed{{}}. \\boxed{{}}. \\boxed{{}}. \\boxed{{}}. \\boxed{{}}. \\boxed{{}}. \\boxed{{}}. \\boxed{{}}. \\boxed{{}}. \\boxed{{}}. \\boxed{{}}. \\boxed{{}}. \\boxed{{}}. \\boxed{{}}. \\boxed{{}}. \\boxed{{}}. \\boxed{{}}. \\boxed{{}}. \\boxed{{}}. \\boxed{{}}. \\boxed{{}}. \\boxed{{}}. \\boxed{{}}. \\boxed{{}}. \\boxed{{}}. \\boxed{{}}. \\boxed{{}}. \\boxed{{}}. \\boxed{{}}. \\boxed{{}}. \\boxed{{}}. \\boxed{{}}. \\boxed{{}}. \\boxed{{}}. \\boxed{{}}. \\boxed{{}}. \\boxed{{}}. \\boxed{{}}. \\boxed{{}}. \\boxed{{}}. \\boxed{{}}. \\boxed{{}}. \\boxed{{}}. \\boxed{{}}. \\boxed{{}}. \\boxed{{}}. \\boxed{{}}. \\boxed{{}}. \\boxed{{}}. \\boxed{{}}. \\boxed{{}}.  \\",

    "ground_truth": "-50",

    "rule_based": false,

    "llm_verifier": true,

    "llm_verifier_score": 1.0,

    "llm_verifier_raw_value": "1.0",

    "math_verify": false,

    "math_verify_score": 0.0

  },

#### FN

⬇
{

    "idx": 92,

    "question": "A pirate searches seven islands for buried treasure. If each island has a $\\frac{1}{5}$ chance of having treasure, what is the probability that exactly 4 of the islands have treasure?",

    "answer": "\\frac{448}{15625}",

    "model_prediction": "0.028672",

    "model_response": "To solve this problem, we can use the binomial probability formula. The probability of having exactly $k$ successes in $n$ independent Bernoulli trials (each with success probability $p$) is given by:\n\n\\[ P(X = k) = \\binom{n}{k} p^k (1-p)^{n-k} \\]\n\nHere, $n = 7$ (the number of islands), $k = 4$ (the number of islands with treasure), and $p = \\frac{1}{5}$ (the probability that a single island has treasure).\n\nThe binomial coefficient $\\binom{n}{k}$ is the number of ways to choose $k$ successes out of $n$ trials, and it is calculated as:\n\n\\[ \\binom{n}{k} = \\frac{n!}{k!(n-k)!} \\]\n\n So, the probability that exactly 4 of the 7 islands have treasure is:\n\n\\[ P(X = 4) = \\binom{7}{4} \\left(\\frac{1}{5}\\right)^4 \\left(\\frac{4}{5}\\right)^{3} \\]\n\nLet’s calculate this using Python.\n‘‘‘python\nimport math\n\n# Number of islands\nn = 7\n# Number of islands with treasure\nk = 4\n# Probability of a single island having treasure\np = 1/5\n\n# Binomial coefficient\nbinom_coeff = math.comb(n, k)\n\n# Probability calculation\nprobability = binom_coeff * (p**k) * ((1-p)**(n-k))\nprint(probability)\n‘‘‘\n‘‘‘output\n0.02867200000000001\n‘‘‘\nThe probability that exactly 4 of the 7 islands have treasure is \\(\\boxed{0.028672}\\).",

    "ground_truth": "\\frac{448}{15625}",

    "rule_based": false,

    "llm_verifier": false,

    "llm_verifier_score": 0.0,

    "llm_verifier_raw_value": "0.0",

    "math_verify": true,

    "math_verify_score": 1.0

  }

## Appendix G Additional Evaluations and Analysis

### G.1 Estimated-Rate Corrections with CompassVerifier

TinyV appeals a random subset of rule-negative responses and supports false-negative-rate estimation under the FN-dominant assumption. This stream does not independently audit rule-positive outputs and therefore does not supply a calibrated estimate of ρ0\rho_{0}. PGBC additionally requires that rate. We evaluate Qwen2.5-Math-1.5B with CompassVerifier-3B (Liu et al., 2025) using stratified audits of both rule-negative and rule-positive outputs. PGFC uses the negative-side estimate of ρ1\rho_{1}, while PGBC uses estimates of both rates. Both corrections improve over direct verifier training and Compass Appeals in Table 8.

Table 8: Qwen2.5-Math-1.5B with CompassVerifier-3B and estimated channel rates. Scores are percentages.

Method
AIME 2024
AIME 2025
AMC 2023
MATH-500
Minerva MATH
OlympiadBench

Rule
15.0±0.415.0\pm 0.4
5.6±0.65.6\pm 0.6
50.3±0.650.3\pm 0.6
69.4±0.469.4\pm 0.4
17.8±0.617.8\pm 0.6
31.6±0.031.6\pm 0.0

LLM-Verifier
16.4±1.016.4\pm 1.0
7.2±0.97.2\pm 0.9
51.5±1.051.5\pm 1.0
70.8±0.770.8\pm 0.7
18.5±0.818.5\pm 0.8
32.0±0.632.0\pm 0.6

Compass Appeals
16.7±0.816.7\pm 0.8
7.4±0.87.4\pm 0.8
51.8±0.851.8\pm 0.8
71.0±0.671.0\pm 0.6
18.9±0.718.9\pm 0.7
32.3±0.532.3\pm 0.5

Compass Appeals+PGBC
18.7±0.718.7\pm 0.7
8.9±0.88.9\pm 0.8
53.0±0.753.0\pm 0.7
71.7±0.571.7\pm 0.5
21.5±0.621.5\pm 0.6
33.1±0.533.1\pm 0.5

Compass Appeals+PGFC
19.8±0.419.8\pm 0.4
9.8±0.19.8\pm 0.1
54.0±0.354.0\pm 0.3
72.1±0.772.1\pm 0.7
20.1±0.320.1\pm 0.3
33.8±0.933.8\pm 0.9

### G.2 Varying the True Noise Channel

The rate-misspecification experiment varies supplied estimates around a fixed true channel. Table 9 instead changes the true input channel and reports average accuracy across the six math datasets. PGBC performance decreases as c=1−ρ0−ρ1c=1-\rho_{0}-\rho_{1} shrinks, while PGFC is more stable over the tested range. This pattern is consistent with the inverse factor in PGBC; it does not imply that PGFC can recover a signal from an uninformative channel.

Table 9: True-channel sweep: average accuracy (%) across six math benchmarks.

ρ0\rho_{0}
ρ1\rho_{1}
cc
Noise
PGBC
PGFC
Oracle

0.05
0.10
0.85
27.0±0.827.0\pm 0.8
31.5±0.631.5\pm 0.6
31.1±0.331.1\pm 0.3
31.8±0.531.8\pm 0.5

0.10
0.20
0.70
20.4±0.820.4\pm 0.8
31.1±0.631.1\pm 0.6
31.6±0.631.6\pm 0.6
31.8±0.531.8\pm 0.5

0.15
0.30
0.55
17.2±1.017.2\pm 1.0
29.4±0.829.4\pm 0.8
30.7±0.730.7\pm 0.7
31.8±0.531.8\pm 0.5

0.20
0.40
0.40
14.5±1.214.5\pm 1.2
26.4±1.026.4\pm 1.0
30.5±0.930.5\pm 0.9
31.8±0.531.8\pm 0.5

### G.3 Auxiliary-Verifier Calibration and Estimation Error

Let ss and ff be the auxiliary verifier’s sensitivity and false-positive rate on appealed rule negatives, and let π\pi denote the prevalence of true false negatives in that pool. Provided s≠fs\neq f, calibration gives

pflip\displaystyle p_{\mathrm{flip}}
=f+(s−f)​π,\displaystyle=f+(s-f)\pi,
π^\displaystyle\widehat{\pi}
=clip[0,1]⁡(p^flip−f^s^−f^),\displaystyle=\operatorname{clip}_{[0,1]}\!\left(\frac{\widehat{p}_{\mathrm{flip}}-\widehat{f}}{\widehat{s}-\widehat{f}}\right),

(13)

ρ^1\displaystyle\widehat{\rho}_{1}
=|𝒩R|​π^|𝒩R|​π^+|𝒫R|.\displaystyle=\frac{|\mathcal{N}_{\mathrm{R}}|\widehat{\pi}}{|\mathcal{N}_{\mathrm{R}}|\widehat{\pi}+|\mathcal{P}_{\mathrm{R}}|}.

(14)

The final expression assumes negligible false positives from the rule verifier. The uncalibrated estimator corresponds to s=1s=1 and f=0f=0 before smoothing and pseudocounts. Deployment-time calibration of TinyV on appealed rule negatives yields Table 10.

Table 10: Reported deployment-time calibration on appealed rule-negative responses.

Statistic
Value

Sensitivity on true false negatives
0.93

False-positive rate on true negatives
0.03

Naive ρ^1\widehat{\rho}_{1}
0.785

Calibration-corrected ρ^1\widehat{\rho}_{1}
0.780

For an estimate based on historical data and independent of the current rollout, condition on its error δ=ρ^1−ρ1\delta=\widehat{\rho}_{1}-\rho_{1}. Both PGFC weights shift by the same constant: w^R~=wR~+δ\widehat{w}_{\widetilde{R}}=w_{\widetilde{R}}+\delta. With G=∇θ​log​πθ​(y∣x)G=\nabla_{\theta}\log\pi_{\theta}(y\mid x), the score identity 𝔼⁡[G]=0\mathbb{E}[G]=0 implies

𝔼⁡[w^R~​G]\displaystyle\mathbb{E}[\widehat{w}_{\widetilde{R}}G]
=𝔼⁡[wR~​G],\displaystyle=\mathbb{E}[w_{\widetilde{R}}G],

(15)

𝔼⁡[‖g^​(ρ^1)−g^​(ρ1)‖2]\displaystyle\mathbb{E}\!\left[\|\widehat{g}(\widehat{\rho}_{1})-\widehat{g}(\rho_{1})\|^{2}\right]
=δ2M​tr⁡(Cov⁡(G))\displaystyle=\frac{\delta^{2}}{M}\operatorname{tr}\!\left(\operatorname{Cov}(G)\right)

(16)

for the average of MM independent rollouts. Thus this ideal unclipped estimator has no population-gradient bias from a fixed rate error, and the mean-square finite-sample perturbation is quadratic in δ\delta. Same-batch estimation and clipping can introduce residual effects; this identity is not a guarantee for the full clipped training objective.

### G.4 Conditional Advantage and Gradient Variance

We pool final trajectory-level advantages across rollout groups conditional on clean correctness. For method mm, define ℐr={(b,i):Rb​i∗=r}\mathcal{I}_{r}=\{(b,i):R^{*}_{bi}=r\}, nr=|ℐr|n_{r}=|\mathcal{I}_{r}|, and a¯r(m)=nr−1​∑(b,i)∈ℐrab​i(m)\bar{a}_{r}^{(m)}=n_{r}^{-1}\sum_{(b,i)\in\mathcal{I}_{r}}a_{bi}^{(m)}. The conditional sample variance is

Var^​(a(m)∣R∗=r)=1nr−1​∑(b,i)∈ℐr(ab​i(m)−a¯r(m))2,r∈{0,1}.\widehat{\operatorname{Var}}(a^{(m)}\mid R^{*}=r)=\frac{1}{n_{r}-1}\sum_{(b,i)\in\mathcal{I}_{r}}\left(a_{bi}^{(m)}-\bar{a}_{r}^{(m)}\right)^{2},\qquad r\in\{0,1\}.

(17)

Table 11 also reports gradient covariance trace relative to Noise and the coefficient of variation (CV) of gradient norms. PGBC has larger conditional advantage variance in both classes and a larger covariance trace than either Noise or PGFC in this measurement.

Table 11: Direct variance measurements. Gradient covariance trace is normalized to the Noise value.

Method
Var^​(a∣R∗=0)\widehat{\operatorname{Var}}(a\mid R^{*}=0)
Var^​(a∣R∗=1)\widehat{\operatorname{Var}}(a\mid R^{*}=1)
tr⁡Cov^​(g)\operatorname{tr}\widehat{\operatorname{Cov}}(g)
Gradient-norm CV

Noise
0.107
0.482
1.000×1.000\times
0.729

PGBC
0.671
1.194
3.046×3.046\times
0.873

PGFC
0.181
0.382
0.905×0.905\times
0.730

### G.5 Direct-Coefficient REINFORCE

To examine the corrections outside the clipped GRPO variant, we additionally optimize a direct-coefficient REINFORCE estimator. For each response, set

ui={Ri∗,Oracle,R~i,Noise,(R~i−ρ^0)/(1−ρ^0−ρ^1),PGBC,R~i−(1−ρ^1),PGFC.u_{i}=\begin{cases}R_{i}^{*},&\text{Oracle},\\
\widetilde{R}_{i},&\text{Noise},\\
(\widetilde{R}_{i}-\widehat{\rho}_{0})/(1-\widehat{\rho}_{0}-\widehat{\rho}_{1}),&\text{PGBC},\\
\widetilde{R}_{i}-(1-\widehat{\rho}_{1}),&\text{PGFC}.\end{cases}

(18)

Broadcasting Ai,t=uiA_{i,t}=u_{i} to response tokens yields

g^=1K​∑i=1Kui​∑t∇θ​log​πθ​(yi,t∣x,yi,<t).\widehat{g}=\frac{1}{K}\sum_{i=1}^{K}u_{i}\sum_{t}\nabla_{\theta}\log\pi_{\theta}(y_{i,t}\mid x,y_{i,<t}).

(19)

Both corrections improve over Noise on every benchmark in Table 12. This comparison provides evidence for the correction beyond the clipped surrogate used in the main experiments.

Table 12: Additional direct-coefficient REINFORCE results on Qwen2.5-Math-1.5B.

Method
AIME 2024
AIME 2025
AMC 2023
MATH-500
Minerva MATH
OlympiadBench

Oracle
10.8±0.210.8\pm 0.2
7.6±0.17.6\pm 0.1
50.9±0.450.9\pm 0.4
69.3±0.169.3\pm 0.1
29.2±0.529.2\pm 0.5
33.4±0.333.4\pm 0.3

Noise
7.1±0.77.1\pm 0.7
4.2±0.64.2\pm 0.6
37.8±0.837.8\pm 0.8
54.6±0.554.6\pm 0.5
15.8±1.015.8\pm 1.0
25.9±0.625.9\pm 0.6

PGBC
10.2±0.510.2\pm 0.5
9.1±0.49.1\pm 0.4
47.8±0.747.8\pm 0.7
67.9±0.467.9\pm 0.4
30.6±0.830.6\pm 0.8
31.4±0.531.4\pm 0.5

PGFC
11.1±0.411.1\pm 0.4
9.4±0.39.4\pm 0.3
48.4±0.548.4\pm 0.5
69.2±0.369.2\pm 0.3
30.0±0.730.0\pm 0.7
32.2±0.432.2\pm 0.4

### G.6 Increasing the Rollout Count

Table 13 compares Qwen2.5-Math-1.5B with K∈{8,16,32}K\in\{8,16,32\} rollouts. Increasing the sample count improves Noise, but a gap to Oracle remains at every tested KK. More rollouts reduce Monte Carlo variance; they do not remove the underlying reward-channel distortion.

Table 13: Additional rollout-count comparison on Qwen2.5-Math-1.5B.

Rollouts KK
Oracle
Noise
PGBC
PGFC

8
33.5±0.333.5\pm 0.3
24.2±0.724.2\pm 0.7
32.8±0.632.8\pm 0.6
33.4±0.533.4\pm 0.5

16
34.0±0.534.0\pm 0.5
26.0±0.826.0\pm 0.8
33.2±0.433.2\pm 0.4
33.8±0.233.8\pm 0.2

32
35.2±0.335.2\pm 0.3
28.7±0.428.7\pm 0.4
34.4±0.534.4\pm 0.5
35.0±0.435.0\pm 0.4

## Appendix H Additional Scope Clarifications

### H.1 Informative, Uninformative, and Reversed Channels

The assumption ρ0+ρ1<1\rho_{0}+\rho_{1}<1 means that correct responses are more likely to receive positive reward than incorrect responses:

Pr⁡(R~=1∣R∗=1)=1−ρ1>ρ0=Pr⁡(R~=1∣R∗=0).\Pr(\widetilde{R}=1\mid R^{*}=1)=1-\rho_{1}>\rho_{0}=\Pr(\widetilde{R}=1\mid R^{*}=0).

(20)

At ρ0+ρ1=1\rho_{0}+\rho_{1}=1, the two conditional reward distributions coincide and the transition matrix is singular; observed rewards alone carry no correctness information under this channel model. If ρ0+ρ1>1\rho_{0}+\rho_{1}>1, the channel is anti-informative. When a calibration set identifies that orientation, complementing R~′=1−R~\widetilde{R}^{\prime}=1-\widetilde{R} gives ρ0′=1−ρ0\rho^{\prime}_{0}=1-\rho_{0} and ρ1′=1−ρ1\rho^{\prime}_{1}=1-\rho_{1}, so ρ0′+ρ1′=2−(ρ0+ρ1)<1\rho^{\prime}_{0}+\rho^{\prime}_{1}=2-(\rho_{0}+\rho_{1})<1. The correction can then use the complemented channel. As c=1−ρ0−ρ1c=1-\rho_{0}-\rho_{1} approaches zero from above, PGBC amplifies coefficients through 1/c1/c, whereas PGFC’s expected signal shrinks proportionally to cc.

For content-dependent errors ρ0​(x,y)\rho_{0}(x,y) and ρ1​(x,y)\rho_{1}(x,y), constant-rate corrections operate on an effective channel. Dependence between verifier errors and score terms can leave a residual such as Cov⁡(wR~,G∣R∗)\operatorname{Cov}(w_{\widetilde{R}},G\mid R^{*}). The non-i.i.d. experiment tests empirical behavior under this misspecification; it does not extend the exact population theorem to arbitrary content-dependent noise.

### H.2 Single-Reward Functions and Nonlinear Group Objectives

Every function of one binary reward is affine:

f⁡(R∗)=f⁡(0)+(f⁡(1)−f⁡(0))​R∗.f(R^{*})=f(0)+\bigl(f(1)-f(0)\bigr)R^{*}.

(21)

Replacing R∗R^{*} by its backward-corrected estimator therefore provides an unbiased estimate of f⁡(R∗)f(R^{*}) under the stated channel assumptions. For a function F⁡(R1∗,…,RK∗)F(R_{1}^{*},\ldots,R_{K}^{*}) of an entire group with independent verifier noise, the channel is T⊗KT^{\otimes K}. Inverting this channel can in principle produce an unbiased estimator when TT is invertible, but direct inversion becomes poorly conditioned as group size increases for a noisy channel.

For example, the clean pass@KK outcome is 1−∏j=1K(1−Rj∗)1-\prod_{j=1}^{K}(1-R_{j}^{*}). With independent verifier noise and correctly specified rates, an unbiased estimator is

1−∏j=1K(1−R^j),1-\prod_{j=1}^{K}(1-\widehat{R}_{j}),

(22)

where R^j\widehat{R}_{j} is the backward-corrected reward. A policy gradient for this group objective includes score terms from all KK sampled responses. For a nonlinear function g⁡(px)g(p_{x}) of prompt success probability,

px=𝔼⁡[R~∣x]−ρ01−ρ0−ρ1,p_{x}=\frac{\mathbb{E}[\widetilde{R}\mid x]-\rho_{0}}{1-\rho_{0}-\rho_{1}},

(23)

but the plug-in estimate g⁡(p^x)g(\widehat{p}_{x}) is generally not finite-sample unbiased. Clipping or shrinking p^x\widehat{p}_{x} and using uncertainty-aware weights may be useful practical extensions, but these require separate analysis and experimental validation.

  
    Experimental support, please
    view the build logs
    for errors. Generated by
    
      
        L
        A
        T
        E
      
      xml
      
    .
  
  
    Instructions for reporting errors
    
We are continuing to improve HTML versions of papers, and your feedback helps enhance accessibility and mobile
      support. To report errors in the HTML that will help us improve conversion and rendering, choose any of the
      methods listed below:

    
      
• Click the "Report Issue" (
            
          ) button, located in the page header.
    
    
Tip: You can select the relevant text first, to include it in your report.

    
Our team has already identified the following issues. We appreciate your time reviewing and reporting rendering errors we
      may not have found yet. Your efforts will help us improve the HTML versions for all readers, because disability
      should not be a barrier to accessing research. Thank you for your continued support in championing open access for
      all.

    
Have a free development cycle? Help support accessibility at arXiv! Our collaborators at LaTeXML maintain a list of packages that need conversion, and welcome developer contributions.

  

  
    
      
        We gratefully acknowledge support from our major funders,
        member institutions, ,
        and all contributors.