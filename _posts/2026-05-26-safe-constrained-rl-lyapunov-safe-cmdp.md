---
layout: post
title: "Lyapunov-Based Safe Policy Improvement for CMDPs"
date: 2026-05-26
category: safe-constrained-rl
category_label: "Safe & Constrained RL"
paper_title: ""
authors: ""
venue: ""
year: ""
doi: ""
arxiv: ""
source_url: ""
tags:
  - safe reinforcement learning
  - constrained MDP
  - Lyapunov function
  - policy iteration
  - safe DQN
excerpt: "Lyapunov constraints turn an expected cumulative safety budget in a CMDP into local restrictions on policy improvement. This note examines the exact certificate logic and the weaker status of neural approximations."
language: "en-ko"
---

## Positioning: Why the problem matters

In robotics, autonomous systems, process control, energy operation, and supply-chain control under uncertainty, a policy cannot be judged only by reward or operating cost. A controller may improve throughput while accumulating thermal exposure, unsafe transitions, resource shortage, or reliability risk beyond an acceptable budget. Recommendation systems have an analogous issue when repeated actions can accumulate undesirable long-run effects.

Ordinary reinforcement learning optimizes an expected cumulative objective. A constrained Markov decision process (CMDP) instead asks for a good policy among policies that also control expected cumulative constraint cost. In cost-minimization form, the safety condition is

```text
D^π(x₀) ≤ d₀,
```

where `D^π(x₀)` is the expected cumulative constraint cost from initial state `x₀` under policy `π`, and `d₀` is the permitted budget. This is a trajectory-level expectation constraint: it controls cumulative safety burden over an episode, not merely whether each individual action passes a one-step rule.

## Problem setting

Let `c(x,a)` denote an objective stage cost and `d(x,a)` a constraint stage cost. For an episodic CMDP, the objective is to choose `π` so that

```text
minimize over π      C^π(x₀) = E_π[ Σ_t c(x_t, a_t) | x₀ ]
subject to           D^π(x₀) = E_π[ Σ_t d(x_t, a_t) | x₀ ] ≤ d₀.
```

The distinction between `C^π` and `D^π` matters. Performance can be traded against other performance terms, but a feasibility-critical budget should not be silently spent simply because a reward improvement is large. Equally, the CMDP statement is not pathwise safety: an expected bound alone does not rule out every unsafe realized trajectory.

## Prior research gap

Before the Lyapunov formulation, several approaches exposed a tension between tractability and safety during learning.

- **Lagrangian CMDPs** penalize constraint cost with a multiplier. This is mathematically natural, but multiplier adaptation may pass through policies that violate the original budget, and primal-dual learning can be unstable.
- **Occupation-measure or dual LP formulations** give an elegant global solution for finite CMDPs with known dynamics. They become expensive in large state-action spaces and awkward when the transition model is unknown.
- **Step-wise surrogate constraints** can prevent immediate excess use of budget, but dividing a global allowance uniformly across time is often conservative: a harmless early expenditure may be rejected even when future behavior compensates.
- **Supermartingale or conservative surrogate methods** can preserve a safety condition, while potentially shrinking the feasible policy set enough to harm useful improvement.
- **CPO/TRPO-style constrained optimization** is designed for scalable policy updates, but does not provide the same direct policy-iteration interpretation for arbitrary RL algorithms.

The central question is therefore whether cumulative feasibility can be expressed as local admissibility tests that retain a feasible baseline while still allowing policy improvement.

## Core idea

The method replaces the global expected cumulative constraint

```text
D^π(x₀) ≤ d₀
```

with Lyapunov-type local inequalities:

```text
T_{π,d}[L](x) ≤ L(x),     for every relevant state x.
```

Here, `L(x)` can be interpreted as an upper bound on future cumulative constraint cost, or as a state-dependent remaining safety budget. The operator `T_{π,d}` adds the immediate constraint cost and the expected continuation certificate after one transition under policy `π`. Thus the inequality says that taking one policy step does not consume more certified safety burden than the current envelope permits.

If

```text
T_{π,d}[L](x) ≤ L(x)  for all x,       and       L(x₀) ≤ d₀,
```

then repeatedly applying the local inequality gives `D^π(x₀) ≤ d₀` under the exact CMDP assumptions. The construction is useful precisely because it turns a global budget into local constraints on action distributions.

## Mathematical structure: Local LP interpretation

Let `π_B` be a currently feasible baseline policy used to construct the Lyapunov budget. It is not simply an arbitrary initialization: its known feasibility anchors the certificate and keeps the induced policy set nonempty.

For a finite action space, a candidate improvement at state `x` can be obtained from the local linear program

```text
π′(·|x) ∈ arg min_{π ∈ Δ}   π(·|x)ᵀ Q(x,·)

subject to                  (π(·|x) - π_B(·|x))ᵀ Q_L(x,·) ≤ ε̃(x).
```

In this expression:

- `Δ` is the probability simplex over actions.
- `Q(x,·)` is the objective cost-to-go vector, so minimizing its expectation is a local performance-improvement step.
- `Q_L(x,·)` is the Lyapunov safety-burden vector associated with taking each action and continuing.
- `π(·|x)ᵀ Q_L(x,·)` is the expected Lyapunov burden of the candidate action distribution.
- `(π - π_B)ᵀ Q_L` is its increase in burden relative to the feasible baseline.
- `ε̃(x)` is the permitted local increase in certified safety burden.

The LP therefore has a precise reading: improve objective value at this state while admitting only a bounded increase in Lyapunov safety burden relative to a policy already used to certify feasibility.

## Algorithmic structure: Safe DQN / Safe DPI

Exact dynamic programming is generally unavailable in large or unknown MDPs. In the approximate architecture described in the supplied material, the learner estimates three state-action quantities:

```text
objective Q-function:          Q̂(x,a; θ)
constraint-cost Q-function:    Q̂_D(x,a; θ_D)
stopping-time Q-function:      Q̂_T(x,a; θ_T)
```

It then constructs a state-action Lyapunov estimate:

```text
Q̂_L(x,a) = Q̂_D(x,a) + ε̃ Q̂_T(x,a).
```

`Q_T` must not be mistaken for another safety cost. `Q_T(x,a)` estimates the expected number of remaining steps until termination after action `a` is selected in state `x` and the baseline policy is subsequently followed. It is the Q-function of an auxiliary episodic MDP whose per-step cost is `1`.

Consequently, `Q_D(x,a)` estimates real expected cumulative constraint cost, while `ε̃ Q_T(x,a)` accumulates an auxiliary per-step safety allowance over the expected remaining horizon. In short:

```text
Q_L = real constraint burden + cumulative auxiliary slack burden.
```

The approximate policy-update pipeline is:

```text
Replay buffer
    -> learn objective Q̂
    -> learn constraint Q̂_D
    -> learn stopping-time Q̂_T
    -> construct Q̂_L = Q̂_D + ε̃ Q̂_T
    -> solve local Lyapunov-safe LP
    -> distill LP policy into neural policy
    -> execute/update feasible-policy approximation
```

The LP acts on a local action distribution. Distillation is a separate approximation step: the neural policy executed later may differ from the LP solution that satisfied the estimated constraint.

## Why it can work

There are structurally defensible reasons for this approach, without claiming that it must outperform alternatives.

- Compared with Lagrangian learning, it restricts the admissible policy set through a certificate inequality rather than relying only on penalties for violation.
- Compared with uniform step-wise constraints, its Lyapunov budget is state-dependent and can allow less conservative allocation of cumulative budget.
- Compared with a global occupation-measure LP, an update is reduced to local LPs over action distributions when the action set is finite.
- Compared with unconstrained function approximation, local LP projection and distillation provide a safety-shaped target policy rather than only an objective-improving target.

## Mathematical guarantees

The theorem-level conclusions belong to an exact value/model setting and should not be automatically transferred to deep implementations.

- If an exact `L` satisfies `T_{π,d}[L](x) ≤ L(x)` for every relevant state and `L(x₀) ≤ d₀`, then the policy satisfies the global expected cumulative constraint `D^π(x₀) ≤ d₀`.
- If a feasible baseline policy exists and the Lyapunov set is constructed from it as stipulated, that feasible set is nonempty because it includes the baseline.
- Under strong assumptions that the feasible baseline is sufficiently close to the unknown optimal constrained policy, the Lyapunov-induced feasible set can contain an optimal policy.
- A safe Bellman operator can recover the CMDP optimum only when such strong inclusion or baseline-closeness assumptions hold.
- Safe Policy Iteration can preserve feasibility and provide monotonic objective improvement in the exact model/value setting.

These claims establish a clean certificate mechanism. They do not prove hard real-world safety for an approximate neural policy.

## Assumptions and limitations: Weaknesses and strong assumptions

A feasible baseline policy is required. In a physical process or autonomous system, obtaining that baseline can itself be a significant robust-control or operations-design problem.

The optimality result depends on baseline closeness to an unknown optimal feasible policy. This condition may be informative in analysis, but is difficult to verify before solving the constrained problem of interest.

Safety is expressed as expected cumulative constraint cost, not pathwise avoidance of unsafe outcomes. If rare but severe violations are unacceptable, an expectation-constrained CMDP requires additional risk-sensitive, robust, or chance-constrained machinery.

Function approximation weakens hard guarantees. When `Q̂_L ≈ Q_L`, a local LP based on `Q̂_L` may certify a policy that is infeasible under the true constraint values. Distilling the LP action distribution into a neural policy introduces a further deviation. For strict inference-time safety, the LP projection would need to remain active at execution, or conservative margins would need to cover both estimation and distillation errors.

Finally, any evaluation concentrated on grid-world-style tasks establishes mechanism rather than general scalability. It should not be generalized without evidence to high-dimensional nonlinear continuous control, process dynamics, or long-horizon energy and supply-chain operation.

## Critical assessment

The conceptual strength is that safety is handled as membership in an admissible policy set, not merely as a penalty term. The baseline/certificate/candidate relationship makes clear why a local improvement may remain feasible in the exact setting.

Its practical vulnerability is equally clear. Certificate quality, baseline availability, and approximation error determine whether the elegant local condition remains meaningful outside a finite exact CMDP. Neural experiments can demonstrate useful empirical constraint behavior; they cannot by themselves re-establish the exact Lyapunov guarantee.

## Connection to my research

For optimization-compatible safe RL, the main takeaway is that a learned continuation value is not enough for safety. A PICNN or convex surrogate would support stronger novelty only if it preserves a one-sided feasibility residual, a Lyapunov decrease inequality, or another conservative safety certificate, rather than merely approximating value accurately.

## Possible extension

A possible extension is an action-convex Lyapunov surrogate embedded in nonlinear stochastic MPC or feasibility-critical clean-energy planning. Such a surrogate could make local safe projections computationally compatible with downstream optimization while adding an explicit residual margin for approximation error. This is a proposed direction, not a result of the discussed method.

## Korean technical note

이 논문의 핵심은 safety를 위반에 대한 **penalty**로만 처리하는 것이 아니라, 정책 개선이 머물러야 하는 **admissible policy set**으로 다루는 데 있다. 전역 제약 `D^π(x₀) ≤ d₀`를 만족시키기 위해, 각 상태에서 Lyapunov 함수가 허용하는 국소 정책 집합 안에서만 성능을 개선한다.

`Q_T`는 constraint cost가 아니다. 상태 `x`에서 행동 `a`를 선택한 뒤 baseline policy를 따를 때 terminal 상태까지 남은 expected step 수를 추정하는 보조 Q-function이며, 매 step의 cost가 `1`인 auxiliary MDP의 값으로 해석된다. 따라서 `ε̃ Q_T`는 step당 허용한 safety slack이 남은 expected horizon 동안 누적된 양이다. 반면 `Q_D`는 실제 누적 constraint cost를 나타낸다.

국소 LP 제약

```text
(π(·|x) - π_B(·|x))ᵀ Q_L(x,·) ≤ ε̃(x)
```

은 candidate policy가 feasible baseline policy보다 Lyapunov safety burden을 얼마나 더 사용할 수 있는지를 제한한다. 즉, objective Q를 개선하더라도 인증된 safety allowance를 과도하게 소비하는 action distribution은 허용하지 않는다.

이 구조는 exact finite CMDP에서는 깔끔하다. 그러나 neural approximation으로 넘어가면 `Q̂_L`의 추정 오차와 LP policy를 neural policy로 distill하는 오차가 생기므로 hard safety guarantee는 약해진다. 실제 운용에서 강한 safety가 필요하다면 실행 시 projection을 유지하거나 보수적 오차 margin을 설계해야 한다.

## Citation and metadata

This note is based only on the supplied discussion of Lyapunov-based safe reinforcement learning for CMDPs, including its Safe Policy Iteration, Safe DQN, and Safe DPI constructions. No verifiable paper title, author list, venue, publication year, DOI, arXiv identifier, or stable source URL was supplied in the repository material; these front matter fields are intentionally blank.
