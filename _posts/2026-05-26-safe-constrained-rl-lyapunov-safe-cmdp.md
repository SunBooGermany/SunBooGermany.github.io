---
layout: post
title: "Lyapunov-Based Safe Policy Improvement for CMDPs"
title_ko: "CMDP를 위한 Lyapunov 기반 안전 정책 개선"
date: 2026-05-26
category: safe-constrained-rl
category_label: "Safe & Constrained RL"
category_label_ko: "안전 및 제약 강화학습"
research_group: algorithmic_reviews
research_category: safe-constrained-rl
research_category_label: "Safe & Constrained RL"
research_category_label_ko: "안전 및 제약 강화학습"
application_category: ""
application_category_label: ""
method_category: safe-constrained-rl
method_category_label: "Safe & Constrained RL"
method_category_label_ko: "안전 및 제약 강화학습"
paper_title: "A lyapunov-based approach to safe reinforcement learning"
paper_title_ko: "안전 강화학습을 위한 Lyapunov 기반 접근"
authors: "Chow Y, Nachum O, Duenez-Guzman E, Ghavamzadeh M"
venue: "Advances in neural information processing systems"
year: "2018"
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
excerpt_ko: "Lyapunov 제약은 CMDP의 기대 누적 안전 예산을 정책 개선의 국소 제약으로 바꾼다. 이 노트는 정확한 인증 논리와 신경망 근사에서 약해지는 보장 수준을 구분해 읽는다."
language: "en-ko"
has_korean_note: true
---

## Positioning: Why the problem matters

In robotics, autonomous systems, process control, energy operation, and supply-chain control under uncertainty, a policy cannot be judged only by reward or operating cost. A controller may improve throughput while accumulating thermal exposure, unsafe transitions, resource shortage, or reliability risk beyond an acceptable budget. Recommendation systems have an analogous issue when repeated actions can accumulate undesirable long-run effects.

Ordinary reinforcement learning optimizes an expected cumulative objective. A constrained Markov decision process (CMDP) instead asks for a good policy among policies that also control expected cumulative constraint cost. In cost-minimization form, the safety condition is

<math display="block" aria-label="D pi of x zero is less than or equal to d zero">
  <msup><mi>D</mi><mi>&pi;</mi></msup>
  <mo>(</mo><msub><mi>x</mi><mn>0</mn></msub><mo>)</mo>
  <mo>&le;</mo>
  <msub><mi>d</mi><mn>0</mn></msub>
</math>

where <math><msup><mi>D</mi><mi>&pi;</mi></msup><mo>(</mo><msub><mi>x</mi><mn>0</mn></msub><mo>)</mo></math> is the expected cumulative constraint cost from initial state <math><msub><mi>x</mi><mn>0</mn></msub></math> under policy <math><mi>&pi;</mi></math>, and <math><msub><mi>d</mi><mn>0</mn></msub></math> is the permitted budget. This is a trajectory-level expectation constraint: it controls cumulative safety burden over an episode, not merely whether each individual action passes a one-step rule.

## Problem setting

Let <math><mi>c</mi><mo>(</mo><mi>x</mi><mo>,</mo><mi>a</mi><mo>)</mo></math> denote an objective stage cost and <math><mi>d</mi><mo>(</mo><mi>x</mi><mo>,</mo><mi>a</mi><mo>)</mo></math> a constraint stage cost. For an episodic CMDP, the objective is to choose <math><mi>&pi;</mi></math> so that

<math display="block" aria-label="CMDP optimization problem">
  <mtable columnalign="right left" columnspacing="1em">
    <mtr>
      <mtd><mtext>minimize over </mtext><mi>&pi;</mi></mtd>
      <mtd>
        <msup><mi>C</mi><mi>&pi;</mi></msup><mo>(</mo><msub><mi>x</mi><mn>0</mn></msub><mo>)</mo>
        <mo>=</mo>
        <msub><mi mathvariant="double-struck">E</mi><mi>&pi;</mi></msub>
        <mo>[</mo><msub><mo>&sum;</mo><mi>t</mi></msub>
        <mi>c</mi><mo>(</mo><msub><mi>x</mi><mi>t</mi></msub><mo>,</mo><msub><mi>a</mi><mi>t</mi></msub><mo>)</mo>
        <mo>|</mo><msub><mi>x</mi><mn>0</mn></msub><mo>]</mo>
      </mtd>
    </mtr>
    <mtr>
      <mtd><mtext>subject to</mtext></mtd>
      <mtd>
        <msup><mi>D</mi><mi>&pi;</mi></msup><mo>(</mo><msub><mi>x</mi><mn>0</mn></msub><mo>)</mo>
        <mo>=</mo>
        <msub><mi mathvariant="double-struck">E</mi><mi>&pi;</mi></msub>
        <mo>[</mo><msub><mo>&sum;</mo><mi>t</mi></msub>
        <mi>d</mi><mo>(</mo><msub><mi>x</mi><mi>t</mi></msub><mo>,</mo><msub><mi>a</mi><mi>t</mi></msub><mo>)</mo>
        <mo>|</mo><msub><mi>x</mi><mn>0</mn></msub><mo>]</mo>
        <mo>&le;</mo><msub><mi>d</mi><mn>0</mn></msub>
      </mtd>
    </mtr>
  </mtable>
</math>

The distinction between <math><msup><mi>C</mi><mi>&pi;</mi></msup></math> and <math><msup><mi>D</mi><mi>&pi;</mi></msup></math> matters. Performance can be traded against other performance terms, but a feasibility-critical budget should not be silently spent simply because a reward improvement is large. Equally, the CMDP statement is not pathwise safety: an expected bound alone does not rule out every unsafe realized trajectory.

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

<math display="block" aria-label="D pi of x zero is less than or equal to d zero">
  <msup><mi>D</mi><mi>&pi;</mi></msup>
  <mo>(</mo><msub><mi>x</mi><mn>0</mn></msub><mo>)</mo>
  <mo>&le;</mo>
  <msub><mi>d</mi><mn>0</mn></msub>
</math>

with Lyapunov-type local inequalities:

<math display="block" aria-label="Local Lyapunov inequality">
  <msub><mi>T</mi><mrow><mi>&pi;</mi><mo>,</mo><mi>d</mi></mrow></msub>
  <mo>[</mo><mi>L</mi><mo>]</mo><mo>(</mo><mi>x</mi><mo>)</mo>
  <mo>&le;</mo>
  <mi>L</mi><mo>(</mo><mi>x</mi><mo>)</mo><mo>,</mo>
  <mspace width="1em"></mspace>
  <mtext>for every relevant state </mtext><mi>x</mi><mo>.</mo>
</math>

Here, <math><mi>L</mi><mo>(</mo><mi>x</mi><mo>)</mo></math> can be interpreted as an upper bound on future cumulative constraint cost, or as a state-dependent remaining safety budget. The operator <math><msub><mi>T</mi><mrow><mi>&pi;</mi><mo>,</mo><mi>d</mi></mrow></msub></math> adds the immediate constraint cost and the expected continuation certificate after one transition under policy <math><mi>&pi;</mi></math>. Thus the inequality says that taking one policy step does not consume more certified safety burden than the current envelope permits.

If

<math display="block" aria-label="Lyapunov feasibility conditions">
  <msub><mi>T</mi><mrow><mi>&pi;</mi><mo>,</mo><mi>d</mi></mrow></msub>
  <mo>[</mo><mi>L</mi><mo>]</mo><mo>(</mo><mi>x</mi><mo>)</mo>
  <mo>&le;</mo>
  <mi>L</mi><mo>(</mo><mi>x</mi><mo>)</mo>
  <mspace width="0.4em"></mspace><mtext>for all </mtext><mi>x</mi><mo>,</mo>
  <mspace width="1.5em"></mspace><mtext>and</mtext><mspace width="1.5em"></mspace>
  <mi>L</mi><mo>(</mo><msub><mi>x</mi><mn>0</mn></msub><mo>)</mo>
  <mo>&le;</mo><msub><mi>d</mi><mn>0</mn></msub><mo>,</mo>
</math>

then repeatedly applying the local inequality gives <math><msup><mi>D</mi><mi>&pi;</mi></msup><mo>(</mo><msub><mi>x</mi><mn>0</mn></msub><mo>)</mo><mo>&le;</mo><msub><mi>d</mi><mn>0</mn></msub></math> under the exact CMDP assumptions. The construction is useful precisely because it turns a global budget into local constraints on action distributions.

## Mathematical structure: Local LP interpretation

Let <math><msub><mi>&pi;</mi><mi>B</mi></msub></math> be a currently feasible baseline policy used to construct the Lyapunov budget. It is not simply an arbitrary initialization: its known feasibility anchors the certificate and keeps the induced policy set nonempty.

For a finite action space, a candidate improvement at state <math><mi>x</mi></math> can be obtained from the local linear program

<math display="block" aria-label="Local Lyapunov-safe policy improvement linear program">
  <mtable columnalign="right left" columnspacing="1em">
    <mtr>
      <mtd>
        <msup><mi>&pi;</mi><mo>&prime;</mo></msup>
        <mo>(</mo><mo>&middot;</mo><mo>|</mo><mi>x</mi><mo>)</mo>
        <mo>&in;</mo>
      </mtd>
      <mtd>
        <munder>
          <mrow><mi>arg</mi><mspace width="0.2em"></mspace><mi>min</mi></mrow>
          <mrow><mi>&pi;</mi><mo>&in;</mo><mi>&Delta;</mi></mrow>
        </munder>
        <msup>
          <mrow><mi>&pi;</mi><mo>(</mo><mo>&middot;</mo><mo>|</mo><mi>x</mi><mo>)</mo></mrow>
          <mi>T</mi>
        </msup>
        <mi>Q</mi><mo>(</mo><mi>x</mi><mo>,</mo><mo>&middot;</mo><mo>)</mo>
      </mtd>
    </mtr>
    <mtr>
      <mtd><mtext>subject to</mtext></mtd>
      <mtd>
        <msup>
          <mrow>
            <mo>(</mo>
            <mi>&pi;</mi><mo>(</mo><mo>&middot;</mo><mo>|</mo><mi>x</mi><mo>)</mo>
            <mo>-</mo>
            <msub><mi>&pi;</mi><mi>B</mi></msub><mo>(</mo><mo>&middot;</mo><mo>|</mo><mi>x</mi><mo>)</mo>
            <mo>)</mo>
          </mrow>
          <mi>T</mi>
        </msup>
        <msub><mi>Q</mi><mi>L</mi></msub><mo>(</mo><mi>x</mi><mo>,</mo><mo>&middot;</mo><mo>)</mo>
        <mo>&le;</mo>
        <mover accent="true"><mi>&epsilon;</mi><mo>~</mo></mover><mo>(</mo><mi>x</mi><mo>)</mo><mo>.</mo>
      </mtd>
    </mtr>
  </mtable>
</math>

In this expression:

- <math><mi>&Delta;</mi></math> is the probability simplex over actions.
- <math><mi>Q</mi><mo>(</mo><mi>x</mi><mo>,</mo><mo>&middot;</mo><mo>)</mo></math> is the objective cost-to-go vector, so minimizing its expectation is a local performance-improvement step.
- <math><msub><mi>Q</mi><mi>L</mi></msub><mo>(</mo><mi>x</mi><mo>,</mo><mo>&middot;</mo><mo>)</mo></math> is the Lyapunov safety-burden vector associated with taking each action and continuing.
- <math><msup><mrow><mi>&pi;</mi><mo>(</mo><mo>&middot;</mo><mo>|</mo><mi>x</mi><mo>)</mo></mrow><mi>T</mi></msup><msub><mi>Q</mi><mi>L</mi></msub><mo>(</mo><mi>x</mi><mo>,</mo><mo>&middot;</mo><mo>)</mo></math> is the expected Lyapunov burden of the candidate action distribution.
- <math><msup><mrow><mo>(</mo><mi>&pi;</mi><mo>-</mo><msub><mi>&pi;</mi><mi>B</mi></msub><mo>)</mo></mrow><mi>T</mi></msup><msub><mi>Q</mi><mi>L</mi></msub></math> is its increase in burden relative to the feasible baseline.
- <math><mover accent="true"><mi>&epsilon;</mi><mo>~</mo></mover><mo>(</mo><mi>x</mi><mo>)</mo></math> is the permitted local increase in certified safety burden.

The LP therefore has a precise reading: improve objective value at this state while admitting only a bounded increase in Lyapunov safety burden relative to a policy already used to certify feasibility.

## Algorithmic structure: Safe DQN / Safe DPI

Exact dynamic programming is generally unavailable in large or unknown MDPs. In the approximate architecture described in the supplied material, the learner estimates three state-action quantities:

<math display="block" aria-label="Learned state-action quantities">
  <mtable columnalign="left left" columnspacing="1.5em">
    <mtr>
      <mtd><mtext>objective Q-function:</mtext></mtd>
      <mtd>
        <mover accent="true"><mi>Q</mi><mo>^</mo></mover>
        <mo>(</mo><mi>x</mi><mo>,</mo><mi>a</mi><mo>;</mo><mi>&theta;</mi><mo>)</mo>
      </mtd>
    </mtr>
    <mtr>
      <mtd><mtext>constraint-cost Q-function:</mtext></mtd>
      <mtd>
        <msub><mover accent="true"><mi>Q</mi><mo>^</mo></mover><mi>D</mi></msub>
        <mo>(</mo><mi>x</mi><mo>,</mo><mi>a</mi><mo>;</mo><msub><mi>&theta;</mi><mi>D</mi></msub><mo>)</mo>
      </mtd>
    </mtr>
    <mtr>
      <mtd><mtext>stopping-time Q-function:</mtext></mtd>
      <mtd>
        <msub><mover accent="true"><mi>Q</mi><mo>^</mo></mover><mi>T</mi></msub>
        <mo>(</mo><mi>x</mi><mo>,</mo><mi>a</mi><mo>;</mo><msub><mi>&theta;</mi><mi>T</mi></msub><mo>)</mo>
      </mtd>
    </mtr>
  </mtable>
</math>

It then constructs a state-action Lyapunov estimate:

<math display="block" aria-label="Estimated state-action Lyapunov function">
  <msub><mover accent="true"><mi>Q</mi><mo>^</mo></mover><mi>L</mi></msub>
  <mo>(</mo><mi>x</mi><mo>,</mo><mi>a</mi><mo>)</mo>
  <mo>=</mo>
  <msub><mover accent="true"><mi>Q</mi><mo>^</mo></mover><mi>D</mi></msub>
  <mo>(</mo><mi>x</mi><mo>,</mo><mi>a</mi><mo>)</mo>
  <mo>+</mo>
  <mover accent="true"><mi>&epsilon;</mi><mo>~</mo></mover>
  <msub><mover accent="true"><mi>Q</mi><mo>^</mo></mover><mi>T</mi></msub>
  <mo>(</mo><mi>x</mi><mo>,</mo><mi>a</mi><mo>)</mo><mo>.</mo>
</math>

<math><msub><mi>Q</mi><mi>T</mi></msub></math> must not be mistaken for another safety cost. <math><msub><mi>Q</mi><mi>T</mi></msub><mo>(</mo><mi>x</mi><mo>,</mo><mi>a</mi><mo>)</mo></math> estimates the expected number of remaining steps until termination after action <math><mi>a</mi></math> is selected in state <math><mi>x</mi></math> and the baseline policy is subsequently followed. It is the Q-function of an auxiliary episodic MDP whose per-step cost is <math><mn>1</mn></math>.

Consequently, <math><msub><mi>Q</mi><mi>D</mi></msub><mo>(</mo><mi>x</mi><mo>,</mo><mi>a</mi><mo>)</mo></math> estimates real expected cumulative constraint cost, while <math><mover accent="true"><mi>&epsilon;</mi><mo>~</mo></mover><msub><mi>Q</mi><mi>T</mi></msub><mo>(</mo><mi>x</mi><mo>,</mo><mi>a</mi><mo>)</mo></math> accumulates an auxiliary per-step safety allowance over the expected remaining horizon. In short:

<math display="block" aria-label="Lyapunov burden interpretation">
  <msub><mi>Q</mi><mi>L</mi></msub>
  <mo>=</mo>
  <mtext>real constraint burden</mtext>
  <mo>+</mo>
  <mtext>cumulative auxiliary slack burden.</mtext>
</math>

The approximate policy-update pipeline is:

```text
Replay buffer
    -> learn objective action value
    -> learn constraint-cost action value
    -> learn stopping-time action value
    -> construct the Lyapunov estimate
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

- If an exact <math><mi>L</mi></math> satisfies <math><msub><mi>T</mi><mrow><mi>&pi;</mi><mo>,</mo><mi>d</mi></mrow></msub><mo>[</mo><mi>L</mi><mo>]</mo><mo>(</mo><mi>x</mi><mo>)</mo><mo>&le;</mo><mi>L</mi><mo>(</mo><mi>x</mi><mo>)</mo></math> for every relevant state and <math><mi>L</mi><mo>(</mo><msub><mi>x</mi><mn>0</mn></msub><mo>)</mo><mo>&le;</mo><msub><mi>d</mi><mn>0</mn></msub></math>, then the policy satisfies the global expected cumulative constraint <math><msup><mi>D</mi><mi>&pi;</mi></msup><mo>(</mo><msub><mi>x</mi><mn>0</mn></msub><mo>)</mo><mo>&le;</mo><msub><mi>d</mi><mn>0</mn></msub></math>.
- If a feasible baseline policy exists and the Lyapunov set is constructed from it as stipulated, that feasible set is nonempty because it includes the baseline.
- Under strong assumptions that the feasible baseline is sufficiently close to the unknown optimal constrained policy, the Lyapunov-induced feasible set can contain an optimal policy.
- A safe Bellman operator can recover the CMDP optimum only when such strong inclusion or baseline-closeness assumptions hold.
- Safe Policy Iteration can preserve feasibility and provide monotonic objective improvement in the exact model/value setting.

These claims establish a clean certificate mechanism. They do not prove hard real-world safety for an approximate neural policy.

## Assumptions and limitations: Weaknesses and strong assumptions

A feasible baseline policy is required. In a physical process or autonomous system, obtaining that baseline can itself be a significant robust-control or operations-design problem.

The optimality result depends on baseline closeness to an unknown optimal feasible policy. This condition may be informative in analysis, but is difficult to verify before solving the constrained problem of interest.

Safety is expressed as expected cumulative constraint cost, not pathwise avoidance of unsafe outcomes. If rare but severe violations are unacceptable, an expectation-constrained CMDP requires additional risk-sensitive, robust, or chance-constrained machinery.

Function approximation weakens hard guarantees. When <math><msub><mover accent="true"><mi>Q</mi><mo>^</mo></mover><mi>L</mi></msub><mo>&approx;</mo><msub><mi>Q</mi><mi>L</mi></msub></math>, a local LP based on <math><msub><mover accent="true"><mi>Q</mi><mo>^</mo></mover><mi>L</mi></msub></math> may certify a policy that is infeasible under the true constraint values. Distilling the LP action distribution into a neural policy introduces a further deviation. For strict inference-time safety, the LP projection would need to remain active at execution, or conservative margins would need to cover both estimation and distillation errors.

Finally, any evaluation concentrated on grid-world-style tasks establishes mechanism rather than general scalability. It should not be generalized without evidence to high-dimensional nonlinear continuous control, process dynamics, or long-horizon energy and supply-chain operation.

## Critical assessment

The conceptual strength is that safety is handled as membership in an admissible policy set, not merely as a penalty term. The baseline/certificate/candidate relationship makes clear why a local improvement may remain feasible in the exact setting.

Its practical vulnerability is equally clear. Certificate quality, baseline availability, and approximation error determine whether the elegant local condition remains meaningful outside a finite exact CMDP. Neural experiments can demonstrate useful empirical constraint behavior; they cannot by themselves re-establish the exact Lyapunov guarantee.

## Reference

Chow Y, Nachum O, Duenez-Guzman E, Ghavamzadeh M. A lyapunov-based approach to safe reinforcement learning. Advances in neural information processing systems. 2018;31.

<!-- ko -->

## 포지셔닝: 왜 이 문제가 중요한가

로보틱스, 자율 시스템, 공정 제어, 에너지 운영, 불확실성 하의 공급망 제어에서 정책은 보상이나 운전 비용만으로 평가될 수 없다. 어떤 제어기는 처리량을 개선하면서도 열 노출, 위험한 상태 전이, 자원 부족, 신뢰도 위험을 허용 가능한 예산 이상으로 누적시킬 수 있다. 추천 시스템에서도 반복 행동이 장기적으로 바람직하지 않은 효과를 누적시킬 수 있다는 점에서 유사한 문제가 생긴다.

일반적인 강화학습은 기대 누적 목적함수를 최적화한다. 제약 Markov decision process(CMDP)는 여기에 더해 기대 누적 제약 비용을 통제하는 정책 중에서 좋은 정책을 찾는다. 비용 최소화 형태에서 안전 조건은 다음과 같다.

<math display="block" aria-label="D pi of x zero is less than or equal to d zero">
  <msup><mi>D</mi><mi>&pi;</mi></msup>
  <mo>(</mo><msub><mi>x</mi><mn>0</mn></msub><mo>)</mo>
  <mo>&le;</mo>
  <msub><mi>d</mi><mn>0</mn></msub>
</math>

여기서 <math><msup><mi>D</mi><mi>&pi;</mi></msup><mo>(</mo><msub><mi>x</mi><mn>0</mn></msub><mo>)</mo></math>는 초기 상태 <math><msub><mi>x</mi><mn>0</mn></msub></math>에서 정책 <math><mi>&pi;</mi></math>를 따를 때의 기대 누적 제약 비용이고, <math><msub><mi>d</mi><mn>0</mn></msub></math>는 허용 예산이다. 이것은 궤적 수준의 기대 제약이다. 각 행동이 한 단계 규칙을 통과하는지만 보는 것이 아니라, 에피소드 전체에 걸친 안전 부담의 누적을 통제한다.

## 문제 설정

<math><mi>c</mi><mo>(</mo><mi>x</mi><mo>,</mo><mi>a</mi><mo>)</mo></math>를 목적 stage cost, <math><mi>d</mi><mo>(</mo><mi>x</mi><mo>,</mo><mi>a</mi><mo>)</mo></math>를 제약 stage cost라고 하자. 에피소드 CMDP의 목표는 다음 조건을 만족하는 정책 <math><mi>&pi;</mi></math>를 선택하는 것이다.

<math display="block" aria-label="CMDP optimization problem">
  <mtable columnalign="right left" columnspacing="1em">
    <mtr>
      <mtd><mtext>minimize over </mtext><mi>&pi;</mi></mtd>
      <mtd>
        <msup><mi>C</mi><mi>&pi;</mi></msup><mo>(</mo><msub><mi>x</mi><mn>0</mn></msub><mo>)</mo>
        <mo>=</mo>
        <msub><mi mathvariant="double-struck">E</mi><mi>&pi;</mi></msub>
        <mo>[</mo><msub><mo>&sum;</mo><mi>t</mi></msub>
        <mi>c</mi><mo>(</mo><msub><mi>x</mi><mi>t</mi></msub><mo>,</mo><msub><mi>a</mi><mi>t</mi></msub><mo>)</mo>
        <mo>|</mo><msub><mi>x</mi><mn>0</mn></msub><mo>]</mo>
      </mtd>
    </mtr>
    <mtr>
      <mtd><mtext>subject to</mtext></mtd>
      <mtd>
        <msup><mi>D</mi><mi>&pi;</mi></msup><mo>(</mo><msub><mi>x</mi><mn>0</mn></msub><mo>)</mo>
        <mo>=</mo>
        <msub><mi mathvariant="double-struck">E</mi><mi>&pi;</mi></msub>
        <mo>[</mo><msub><mo>&sum;</mo><mi>t</mi></msub>
        <mi>d</mi><mo>(</mo><msub><mi>x</mi><mi>t</mi></msub><mo>,</mo><msub><mi>a</mi><mi>t</mi></msub><mo>)</mo>
        <mo>|</mo><msub><mi>x</mi><mn>0</mn></msub><mo>]</mo>
        <mo>&le;</mo><msub><mi>d</mi><mn>0</mn></msub>
      </mtd>
    </mtr>
  </mtable>
</math>

<math><msup><mi>C</mi><mi>&pi;</mi></msup></math>와 <math><msup><mi>D</mi><mi>&pi;</mi></msup></math>의 구분은 중요하다. 성능 항들은 서로 절충될 수 있지만, 실행 가능성이 중요한 안전 예산은 보상 개선이 크다는 이유만으로 조용히 소모되어서는 안 된다. 또한 CMDP 제약은 pathwise safety가 아니다. 기대값 상한은 모든 실제 궤적의 위험을 배제하지 않는다.

## 기존 연구의 공백

Lyapunov 형식화 이전의 여러 접근은 학습 중 안전성과 계산 가능성 사이의 긴장을 드러냈다.

- **Lagrangian CMDP**는 제약 비용에 승수를 붙여 벌점화한다. 수학적으로 자연스럽지만 승수 적응 과정에서 원래 예산을 위반하는 정책을 지나갈 수 있고, primal-dual 학습은 불안정할 수 있다.
- **Occupation-measure 또는 dual LP 형식**은 유한 CMDP와 알려진 동역학에서는 우아한 전역 해법을 제공한다. 그러나 큰 상태-행동 공간에서는 비싸고, 전이 모델이 알려져 있지 않을 때 다루기 어렵다.
- **단계별 대리 제약**은 즉각적인 예산 초과를 막을 수 있지만, 전역 허용량을 시간에 균등하게 나누면 지나치게 보수적일 수 있다.
- **Supermartingale 또는 보수적 대리 방법**은 안전 조건을 보존할 수 있지만, 가능한 정책 집합을 너무 줄여 유용한 개선을 방해할 수 있다.
- **CPO/TRPO 계열 제약 최적화**는 확장 가능한 정책 업데이트를 위해 설계되었지만, 임의의 RL 알고리즘에 대해 같은 직접적 정책 반복 해석을 제공하지는 않는다.

따라서 핵심 질문은 누적 실행 가능성을, 안전한 baseline을 유지하면서도 정책 개선을 허용하는 국소 admissibility test로 표현할 수 있는가이다.

## 핵심 아이디어

이 방법은 전역 기대 누적 제약

<math display="block" aria-label="D pi of x zero is less than or equal to d zero">
  <msup><mi>D</mi><mi>&pi;</mi></msup>
  <mo>(</mo><msub><mi>x</mi><mn>0</mn></msub><mo>)</mo>
  <mo>&le;</mo>
  <msub><mi>d</mi><mn>0</mn></msub>
</math>

을 Lyapunov 형태의 국소 부등식으로 바꾼다.

<math display="block" aria-label="Local Lyapunov inequality">
  <msub><mi>T</mi><mrow><mi>&pi;</mi><mo>,</mo><mi>d</mi></mrow></msub>
  <mo>[</mo><mi>L</mi><mo>]</mo><mo>(</mo><mi>x</mi><mo>)</mo>
  <mo>&le;</mo>
  <mi>L</mi><mo>(</mo><mi>x</mi><mo>)</mo><mo>,</mo>
  <mspace width="1em"></mspace>
  <mtext>for every relevant state </mtext><mi>x</mi><mo>.</mo>
</math>

<math><mi>L</mi><mo>(</mo><mi>x</mi><mo>)</mo></math>는 미래 누적 제약 비용의 상한, 또는 상태 의존적인 남은 안전 예산으로 해석할 수 있다. 연산자 <math><msub><mi>T</mi><mrow><mi>&pi;</mi><mo>,</mo><mi>d</mi></mrow></msub></math>는 즉각 제약 비용과 정책 <math><mi>&pi;</mi></math> 하에서 한 번 전이한 뒤의 기대 continuation certificate를 더한다. 따라서 이 부등식은 한 정책 단계가 현재 envelope가 허용하는 인증된 안전 부담보다 더 많이 소비하지 않는다는 뜻이다.

만약 모든 관련 상태에서 이 국소 부등식이 성립하고 <math><mi>L</mi><mo>(</mo><msub><mi>x</mi><mn>0</mn></msub><mo>)</mo><mo>&le;</mo><msub><mi>d</mi><mn>0</mn></msub></math>라면, 정확한 CMDP 가정 하에서는 국소 부등식을 반복 적용해 <math><msup><mi>D</mi><mi>&pi;</mi></msup><mo>(</mo><msub><mi>x</mi><mn>0</mn></msub><mo>)</mo><mo>&le;</mo><msub><mi>d</mi><mn>0</mn></msub></math>를 얻는다. 이 구성이 유용한 이유는 전역 예산을 행동 분포에 대한 국소 제약으로 바꾸기 때문이다.

## 수학적 구조: 국소 LP 해석

<math><msub><mi>&pi;</mi><mi>B</mi></msub></math>를 Lyapunov 예산을 구성하는 데 쓰는 현재 feasible baseline policy라고 하자. 이것은 임의의 초기 정책이 아니다. baseline의 알려진 실행 가능성이 certificate를 고정하고, 유도된 정책 집합이 비어 있지 않게 만든다.

유한 행동 공간에서 상태 <math><mi>x</mi></math>의 후보 개선은 다음 국소 선형계획으로 얻을 수 있다.

<math display="block" aria-label="Local Lyapunov-safe policy improvement linear program">
  <mtable columnalign="right left" columnspacing="1em">
    <mtr>
      <mtd>
        <msup><mi>&pi;</mi><mo>&prime;</mo></msup>
        <mo>(</mo><mo>&middot;</mo><mo>|</mo><mi>x</mi><mo>)</mo>
        <mo>&in;</mo>
      </mtd>
      <mtd>
        <munder>
          <mrow><mi>arg</mi><mspace width="0.2em"></mspace><mi>min</mi></mrow>
          <mrow><mi>&pi;</mi><mo>&in;</mo><mi>&Delta;</mi></mrow>
        </munder>
        <msup>
          <mrow><mi>&pi;</mi><mo>(</mo><mo>&middot;</mo><mo>|</mo><mi>x</mi><mo>)</mo></mrow>
          <mi>T</mi>
        </msup>
        <mi>Q</mi><mo>(</mo><mi>x</mi><mo>,</mo><mo>&middot;</mo><mo>)</mo>
      </mtd>
    </mtr>
    <mtr>
      <mtd><mtext>subject to</mtext></mtd>
      <mtd>
        <msup>
          <mrow>
            <mo>(</mo>
            <mi>&pi;</mi><mo>(</mo><mo>&middot;</mo><mo>|</mo><mi>x</mi><mo>)</mo>
            <mo>-</mo>
            <msub><mi>&pi;</mi><mi>B</mi></msub><mo>(</mo><mo>&middot;</mo><mo>|</mo><mi>x</mi><mo>)</mo>
            <mo>)</mo>
          </mrow>
          <mi>T</mi>
        </msup>
        <msub><mi>Q</mi><mi>L</mi></msub><mo>(</mo><mi>x</mi><mo>,</mo><mo>&middot;</mo><mo>)</mo>
        <mo>&le;</mo>
        <mover accent="true"><mi>&epsilon;</mi><mo>~</mo></mover><mo>(</mo><mi>x</mi><mo>)</mo><mo>.</mo>
      </mtd>
    </mtr>
  </mtable>
</math>

이 표현에서 <math><mi>&Delta;</mi></math>는 행동에 대한 확률 단체(simplex), <math><mi>Q</mi><mo>(</mo><mi>x</mi><mo>,</mo><mo>&middot;</mo><mo>)</mo></math>는 목적 cost-to-go 벡터, <math><msub><mi>Q</mi><mi>L</mi></msub></math>는 각 행동을 취하고 계속 진행할 때의 Lyapunov safety-burden 벡터다. 제약식은 후보 행동 분포가 feasible baseline에 비해 얼마나 더 많은 Lyapunov 부담을 만드는지 제한한다. 즉 이 LP는 이미 실행 가능성을 인증하는 데 쓰인 정책에 비해 안전 부담 증가를 제한하면서, 해당 상태에서 목적값을 개선하라는 의미를 갖는다.

## 알고리즘 구조: Safe DQN / Safe DPI

큰 MDP나 알려지지 않은 MDP에서는 정확한 동적계획법을 쓰기 어렵다. 제공된 자료에서 설명된 근사 구조는 세 가지 state-action quantity를 학습한다.

<math display="block" aria-label="Learned state-action quantities">
  <mtable columnalign="left left" columnspacing="1.5em">
    <mtr>
      <mtd><mtext>objective Q-function:</mtext></mtd>
      <mtd>
        <mover accent="true"><mi>Q</mi><mo>^</mo></mover>
        <mo>(</mo><mi>x</mi><mo>,</mo><mi>a</mi><mo>;</mo><mi>&theta;</mi><mo>)</mo>
      </mtd>
    </mtr>
    <mtr>
      <mtd><mtext>constraint-cost Q-function:</mtext></mtd>
      <mtd>
        <msub><mover accent="true"><mi>Q</mi><mo>^</mo></mover><mi>D</mi></msub>
        <mo>(</mo><mi>x</mi><mo>,</mo><mi>a</mi><mo>;</mo><msub><mi>&theta;</mi><mi>D</mi></msub><mo>)</mo>
      </mtd>
    </mtr>
    <mtr>
      <mtd><mtext>stopping-time Q-function:</mtext></mtd>
      <mtd>
        <msub><mover accent="true"><mi>Q</mi><mo>^</mo></mover><mi>T</mi></msub>
        <mo>(</mo><mi>x</mi><mo>,</mo><mi>a</mi><mo>;</mo><msub><mi>&theta;</mi><mi>T</mi></msub><mo>)</mo>
      </mtd>
    </mtr>
  </mtable>
</math>

그다음 state-action Lyapunov 추정치를 다음처럼 구성한다.

<math display="block" aria-label="Estimated state-action Lyapunov function">
  <msub><mover accent="true"><mi>Q</mi><mo>^</mo></mover><mi>L</mi></msub>
  <mo>(</mo><mi>x</mi><mo>,</mo><mi>a</mi><mo>)</mo>
  <mo>=</mo>
  <msub><mover accent="true"><mi>Q</mi><mo>^</mo></mover><mi>D</mi></msub>
  <mo>(</mo><mi>x</mi><mo>,</mo><mi>a</mi><mo>)</mo>
  <mo>+</mo>
  <mover accent="true"><mi>&epsilon;</mi><mo>~</mo></mover>
  <msub><mover accent="true"><mi>Q</mi><mo>^</mo></mover><mi>T</mi></msub>
  <mo>(</mo><mi>x</mi><mo>,</mo><mi>a</mi><mo>)</mo><mo>.</mo>
</math>

여기서 <math><msub><mi>Q</mi><mi>T</mi></msub></math>는 또 다른 안전 비용이 아니다. <math><msub><mi>Q</mi><mi>T</mi></msub><mo>(</mo><mi>x</mi><mo>,</mo><mi>a</mi><mo>)</mo></math>는 상태 <math><mi>x</mi></math>에서 행동 <math><mi>a</mi></math>를 고른 뒤 baseline policy를 따를 때 종료까지 남은 기대 단계 수를 추정한다. 따라서 <math><msub><mi>Q</mi><mi>D</mi></msub></math>는 실제 기대 누적 제약 비용이고, <math><mover accent="true"><mi>&epsilon;</mi><mo>~</mo></mover><msub><mi>Q</mi><mi>T</mi></msub></math>는 남은 기대 horizon에 걸쳐 쌓이는 보조 slack burden이다.

근사 정책 업데이트 파이프라인은 다음처럼 읽을 수 있다.

```text
Replay buffer
    -> objective action value 학습
    -> constraint-cost action value 학습
    -> stopping-time action value 학습
    -> Lyapunov 추정치 구성
    -> 국소 Lyapunov-safe LP 풀이
    -> LP 정책을 신경망 정책으로 distillation
    -> feasible-policy 근사 실행/업데이트
```

LP는 국소 행동 분포에 작용한다. Distillation은 별도의 근사 단계다. 나중에 실행되는 신경망 정책은 추정 제약을 만족한 LP 해와 달라질 수 있다.

## 왜 작동할 수 있는가

이 접근이 항상 다른 방법보다 낫다고 주장하지 않아도, 구조적으로 설득력 있는 이유는 있다.

- Lagrangian 학습과 달리, 위반 벌점에만 의존하지 않고 certificate inequality를 통해 허용 가능한 정책 집합을 제한한다.
- 균등한 단계별 제약보다 상태 의존 Lyapunov 예산을 쓰므로 누적 예산 배분이 덜 보수적일 수 있다.
- 전역 occupation-measure LP에 비해, 유한 행동 집합에서는 업데이트가 행동 분포에 대한 국소 LP로 줄어든다.
- 무제약 함수근사와 달리, 국소 LP projection과 distillation은 단순히 목적을 개선하는 target이 아니라 안전 구조가 반영된 target policy를 제공한다.

## 수학적 보장

정리 수준의 결론은 정확한 value/model 설정에 속하며, deep implementation으로 자동 이전되어서는 안 된다.

- 정확한 <math><mi>L</mi></math>이 모든 관련 상태에서 <math><msub><mi>T</mi><mrow><mi>&pi;</mi><mo>,</mo><mi>d</mi></mrow></msub><mo>[</mo><mi>L</mi><mo>]</mo><mo>(</mo><mi>x</mi><mo>)</mo><mo>&le;</mo><mi>L</mi><mo>(</mo><mi>x</mi><mo>)</mo></math>를 만족하고 <math><mi>L</mi><mo>(</mo><msub><mi>x</mi><mn>0</mn></msub><mo>)</mo><mo>&le;</mo><msub><mi>d</mi><mn>0</mn></msub></math>이면, 정책은 전역 기대 누적 제약 <math><msup><mi>D</mi><mi>&pi;</mi></msup><mo>(</mo><msub><mi>x</mi><mn>0</mn></msub><mo>)</mo><mo>&le;</mo><msub><mi>d</mi><mn>0</mn></msub></math>를 만족한다.
- feasible baseline policy가 존재하고 Lyapunov set이 명시된 방식으로 구성되면, 그 feasible set은 baseline을 포함하므로 비어 있지 않다.
- feasible baseline이 미지의 optimal constrained policy에 충분히 가깝다는 강한 가정 아래에서는 Lyapunov-induced feasible set이 optimal policy를 포함할 수 있다.
- safe Bellman operator가 CMDP optimum을 회복한다는 주장은 이러한 강한 포함 조건 또는 baseline closeness 조건이 성립할 때에만 가능하다.
- Safe Policy Iteration은 정확한 model/value 설정에서 실행 가능성을 보존하고 목적의 단조 개선을 제공할 수 있다.

이 결과들은 명확한 certificate mechanism을 세운다. 그러나 근사 신경망 정책에 대해 실제 세계의 hard safety를 증명하는 것은 아니다.

## 가정과 한계

feasible baseline policy가 필요하다. 물리 공정이나 자율 시스템에서는 그 baseline을 얻는 일 자체가 중요한 robust control 또는 operations design 문제가 될 수 있다.

최적성 결과는 baseline이 미지의 최적 feasible policy에 가깝다는 가정에 의존한다. 이 조건은 분석적으로는 유익하지만, 관심 있는 제약 문제를 풀기 전에 검증하기 어렵다.

안전은 기대 누적 제약 비용으로 표현된다. unsafe outcome의 pathwise avoidance가 아니다. 드물지만 심각한 위반이 허용될 수 없다면 risk-sensitive, robust, chance-constrained 기법이 추가로 필요하다.

함수근사는 hard guarantee를 약화시킨다. <math><msub><mover accent="true"><mi>Q</mi><mo>^</mo></mover><mi>L</mi></msub><mo>&approx;</mo><msub><mi>Q</mi><mi>L</mi></msub></math>일 때, 추정치에 기반한 국소 LP는 실제 제약 값에서는 infeasible한 정책을 인증할 수 있다. LP 행동 분포를 신경망 정책으로 distill하는 과정도 추가 오차를 만든다. 엄격한 inference-time safety가 필요하다면 LP projection이 실행 시점에도 유지되거나, 추정 및 distillation 오차를 덮는 보수적 margin이 필요하다.

마지막으로 grid-world 스타일 평가에 집중한 실험은 메커니즘을 보여 주는 것이지 일반적인 확장성을 입증하는 것은 아니다. 고차원 비선형 연속 제어, 공정 동역학, 장기 에너지 및 공급망 운영으로 일반화하려면 별도의 근거가 필요하다.

## 비판적 평가

개념적 강점은 안전을 단순 벌점항이 아니라 admissible policy set의 membership으로 다룬다는 점이다. baseline, certificate, candidate의 관계는 정확한 설정에서 왜 국소 개선이 실행 가능성을 유지할 수 있는지 분명히 보여 준다.

실천적 취약점도 분명하다. certificate의 품질, baseline의 존재, 근사 오차가 이 우아한 국소 조건이 유한 정확 CMDP 밖에서도 의미를 유지하는지를 결정한다. 신경망 실험은 유용한 경험적 제약 행동을 보여 줄 수 있지만, 그것만으로 정확한 Lyapunov 보장을 다시 세우지는 못한다.

## 참고문헌

Chow Y, Nachum O, Duenez-Guzman E, Ghavamzadeh M. A lyapunov-based approach to safe reinforcement learning. Advances in neural information processing systems. 2018;31.
