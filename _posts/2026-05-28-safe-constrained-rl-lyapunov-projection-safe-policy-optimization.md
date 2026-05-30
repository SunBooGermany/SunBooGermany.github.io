---
layout: post
title: "Lyapunov Projection for Continuous-Action Safe Reinforcement Learning"
title_ko: "연속 행동 안전 강화학습을 위한 Lyapunov 투영"
date: 2026-05-28
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
paper_title: "Lyapunov-based Safe Policy Optimization for Continuous Control"
paper_title_ko: "연속 제어를 위한 Lyapunov 기반 안전 정책 최적화"
authors: "Yinlam Chow, Ofir Nachum, Aleksandra Faust, Edgar Duenez-Guzman, Mohammad Ghavamzadeh"
venue: "arXiv preprint"
year: "2019"
doi: "10.48550/arXiv.1901.10031"
arxiv: "1901.10031"
source_url: "https://arxiv.org/abs/1901.10031"
tags:
  - safe reinforcement learning
  - CMDP
  - Lyapunov function
  - policy gradient
  - projection
  - safety layer
  - continuous control
excerpt: "This note reads Lyapunov-based safe policy optimization as a practical projection bridge from finite CMDP safe policy iteration to continuous-action deep reinforcement learning, while separating exact CMDP guarantees from local approximation behavior."
excerpt_ko: "이 노트는 Lyapunov 기반 안전 정책 최적화를 유한 CMDP의 안전 정책 반복과 연속 행동 심층 강화학습을 잇는 실용적 투영 구조로 읽는다. 동시에 정확한 CMDP 보장과 국소 근사에서의 경험적 안전성을 구분한다."
language: "en-ko"
has_korean_note: true
---

## Why this problem matters

Safety-critical learning is rarely satisfied by a controller that becomes safe only after enough exploration. A robot navigating near people, a chemical process controller near pressure or temperature limits, an energy-system operator balancing reliability and emissions, or an autonomous platform operating under actuator limits may not be allowed to spend many unsafe trials before converging. In these settings, the learning trajectory matters, not only the final reward curve.

Standard reinforcement learning with a Lagrangian penalty can reduce constraint violations on average, but the penalty multiplier is itself learned or tuned. If the multiplier is too small, if the constraint critic is inaccurate, or if the policy update is too aggressive, the learner can still pass through unsafe intermediate policies.

A constrained Markov decision process (CMDP) makes the safety question more explicit by constraining expected cumulative constraint cost. That is useful, but it should not be confused with hard pathwise safety. A CMDP bound can say that the expected discounted collision cost, energy impact, or violation burden is below a budget; it does not, by itself, rule out every unsafe realized trajectory.

## What the earlier Lyapunov CMDP approach could do - and where it breaks

The earlier Lyapunov safe-RL idea starts from a finite CMDP and converts a global expected cumulative constraint into state-wise Lyapunov feasibility conditions. In its cleanest exact form, the certificate can be summarized as

<math display="block" aria-label="Lyapunov state-wise condition implies expected constraint feasibility">
  <mtable columnalign="center" rowspacing="0.4em">
    <mtr>
      <mtd>
        <msub><mi>T</mi><mrow><mi>&pi;</mi><mo>,</mo><mi>d</mi></mrow></msub>
        <mo>[</mo><mi>L</mi><mo>]</mo>
        <mo>(</mo><mi>x</mi><mo>)</mo>
        <mo>&le;</mo>
        <mi>L</mi><mo>(</mo><mi>x</mi><mo>)</mo><mo>,</mo>
        <mspace width="0.5em"></mspace>
        <mo>&forall;</mo><mi>x</mi><mo>,</mo>
      </mtd>
    </mtr>
    <mtr>
      <mtd>
        <mi>L</mi><mo>(</mo><msub><mi>x</mi><mn>0</mn></msub><mo>)</mo>
        <mo>&le;</mo>
        <msub><mi>d</mi><mn>0</mn></msub>
        <mspace width="0.8em"></mspace>
        <mo>&Rightarrow;</mo>
        <mspace width="0.8em"></mspace>
        <msup><mi>D</mi><mi>&pi;</mi></msup>
        <mo>(</mo><msub><mi>x</mi><mn>0</mn></msub><mo>)</mo>
        <mo>&le;</mo>
        <msub><mi>d</mi><mn>0</mn></msub><mo>.</mo>
      </mtd>
    </mtr>
  </mtable>
</math>

Here, <math><msup><mi>D</mi><mi>&pi;</mi></msup><mo>(</mo><msub><mi>x</mi><mn>0</mn></msub><mo>)</mo></math> is the discounted cumulative constraint cost under policy <math><mi>&pi;</mi></math>, and <math><msub><mi>d</mi><mn>0</mn></msub></math> is the allowed budget. The function <math><mi>L</mi><mo>(</mo><mi>x</mi><mo>)</mo></math> is a Lyapunov upper bound on future constraint cost, or equivalently a state-dependent remaining safety envelope. The operator <math><msub><mi>T</mi><mrow><mi>&pi;</mi><mo>,</mo><mi>d</mi></mrow></msub></math> is Bellman-like: it adds immediate constraint cost and expected future Lyapunov burden after one transition under the policy.

The strength of this formulation is its locality. Instead of checking only the global budget after the fact, the policy is restricted by a state-wise condition. But the finite-CMDP machinery does not transfer smoothly to continuous control. Continuous actions turn the action sum into an integral that is generally hard to evaluate exactly. Continuous states turn the Lyapunov feasibility condition into an infinite-dimensional family of constraints, one for every state. Exact value iteration or policy iteration is therefore no longer a practical implementation route.

## Main idea of the follow-up paper

The follow-up paper changes the algorithmic object. Rather than solving safe policy iteration exactly, it starts from a standard policy-gradient method such as DDPG or PPO and inserts a Lyapunov-induced projection into the learning pipeline. The architecture is best read as

```text
state x
  |-- actor pi_theta -> nominal action u
  |-- task critic Q(x,a)
  `-- constraint/Lyapunov critic Q_D(x,a), Q_L(x,a)
          |
          v
   Lyapunov constraint gradient
          |
          v
   projection module
          |
          v
   safe policy update or safe action
```

In short:

```text
standard policy-gradient algorithm
+ Lyapunov critic / constraint critic
+ projection mechanism
= safe policy optimization
```

The contribution is not merely "using Lyapunov functions for safe RL." The more specific contribution is to combine Lyapunov safe policy iteration with continuous-action policy-gradient training and projection-based updates.

The paper develops two projection views. The <math><mi>&theta;</mi></math>-projection modifies the policy parameter update. The <math><mi>a</mi></math>-projection, also described as a Lyapunov safety layer, modifies only the action produced at the current state.

## θ-projection: projecting the policy update

The <math><mi>&theta;</mi></math>-projection acts at the level of policy parameters. In the ideal constrained update, the new parameter is chosen to improve the objective while satisfying a Lyapunov-induced constraint against a feasible baseline policy:

<math display="block" aria-label="Theta projection constrained policy update">
  <mtable columnalign="right left" columnspacing="1em" rowspacing="0.45em">
    <mtr>
      <mtd>
        <msup><mi>&theta;</mi><mo>+</mo></msup>
      </mtd>
      <mtd>
        <mo>=</mo>
        <munder>
          <mrow><mi>arg</mi><mo>&#x2061;</mo><mi>min</mi></mrow>
          <mi>&theta;</mi>
        </munder>
        <mspace width="0.4em"></mspace>
        <msup><mi>C</mi><msub><mi>&pi;</mi><mi>&theta;</mi></msub></msup>
        <mo>(</mo><msub><mi>x</mi><mn>0</mn></msub><mo>)</mo>
      </mtd>
    </mtr>
    <mtr>
      <mtd><mtext>subject to</mtext></mtd>
      <mtd>
        <msub><mo>&int;</mo><mi>A</mi></msub>
        <mo>[</mo>
        <msub><mi>&pi;</mi><mi>&theta;</mi></msub>
        <mo>(</mo><mi>a</mi><mo>|</mo><mi>x</mi><mo>)</mo>
        <mo>-</mo>
        <msub><mi>&pi;</mi><mi>B</mi></msub>
        <mo>(</mo><mi>a</mi><mo>|</mo><mi>x</mi><mo>)</mo>
        <mo>]</mo>
        <msubsup><mi>Q</mi><mi>L</mi><msub><mi>&pi;</mi><mi>B</mi></msub></msubsup>
        <mo>(</mo><mi>x</mi><mo>,</mo><mi>a</mi><mo>)</mo>
        <mi>d</mi><mi>a</mi>
        <mo>&le;</mo>
        <mover accent="true"><mi>&epsilon;</mi><mo>~</mo></mover>
        <mo>(</mo><mi>x</mi><mo>)</mo><mo>,</mo>
        <mspace width="0.5em"></mspace>
        <mo>&forall;</mo><mi>x</mi><mo>.</mo>
      </mtd>
    </mtr>
  </mtable>
</math>

This expression is the right conceptual object, but it is too hard to solve directly in deep continuous control. The objective is therefore approximated by a conservative policy-gradient or KL-regularized local surrogate, connecting the method to TRPO/CPO-style local update logic. The Lyapunov constraint is linearized around baseline parameters <math><msub><mi>&theta;</mi><mi>B</mi></msub></math>, and the infinite state-wise constraint family is replaced in practice by sampled or averaged constraints.

The intuition is simple: the policy update is not allowed to move in an arbitrary reward-improving direction. It must remain inside a local approximation of the Lyapunov-safe update set. Here, feasibility is represented as a restriction on the update geometry, not only as a scalar penalty added to the loss.

The drawback is that a parameter-level restriction can be blunt. A small change in <math><mi>&theta;</mi></math> may cause large action changes in sensitive regions of the state space, while a strict parameter projection may also overcorrect a policy when only a local action adjustment is needed. Thus <math><mi>&theta;</mi></math>-projection is theoretically natural but can be conservative in practice.

## a-projection / Lyapunov safety layer

The <math><mi>a</mi></math>-projection is more direct. The actor first proposes an unconstrained action

<math display="block" aria-label="Nominal actor action">
  <mi>u</mi>
  <mo>=</mo>
  <msub><mi>&pi;</mi><mi>&theta;</mi></msub>
  <mo>(</mo><mi>x</mi><mo>)</mo><mo>.</mo>
</math>

The safety layer then chooses the closest action that satisfies a local Lyapunov constraint relative to the baseline action <math><msub><mi>a</mi><mi>B</mi></msub><mo>=</mo><msub><mi>&pi;</mi><mi>B</mi></msub><mo>(</mo><mi>x</mi><mo>)</mo></math>:

<math display="block" aria-label="Action projection with nonlinear Lyapunov constraint">
  <mtable columnalign="right left" columnspacing="1em" rowspacing="0.45em">
    <mtr>
      <mtd>
        <msup><mi>a</mi><mo>*</mo></msup>
      </mtd>
      <mtd>
        <mo>=</mo>
        <munder>
          <mrow><mi>arg</mi><mo>&#x2061;</mo><mi>min</mi></mrow>
          <mi>a</mi>
        </munder>
        <mspace width="0.4em"></mspace>
        <mfrac><mn>1</mn><mn>2</mn></mfrac>
        <msup>
          <mrow><mo>||</mo><mi>a</mi><mo>-</mo><mi>u</mi><mo>||</mo></mrow>
          <mn>2</mn>
        </msup>
      </mtd>
    </mtr>
    <mtr>
      <mtd><mtext>subject to</mtext></mtd>
      <mtd>
        <msubsup><mi>Q</mi><mi>L</mi><msub><mi>&pi;</mi><mi>B</mi></msub></msubsup>
        <mo>(</mo><mi>x</mi><mo>,</mo><mi>a</mi><mo>)</mo>
        <mo>-</mo>
        <msubsup><mi>Q</mi><mi>L</mi><msub><mi>&pi;</mi><mi>B</mi></msub></msubsup>
        <mo>(</mo><mi>x</mi><mo>,</mo><msub><mi>a</mi><mi>B</mi></msub><mo>)</mo>
        <mo>&le;</mo>
        <mover accent="true"><mi>&epsilon;</mi><mo>~</mo></mover>
        <mo>(</mo><mi>x</mi><mo>)</mo><mo>.</mo>
      </mtd>
    </mtr>
  </mtable>
</math>

Because <math><msub><mi>Q</mi><mi>L</mi></msub><mo>(</mo><mi>x</mi><mo>,</mo><mi>a</mi><mo>)</mo></math> is generally nonlinear in <math><mi>a</mi></math>, the paper uses a first-order local approximation around <math><msub><mi>a</mi><mi>B</mi></msub></math>:

<math display="block" aria-label="First order Lyapunov critic linearization">
  <mtable columnalign="left" rowspacing="0.4em">
    <mtr>
      <mtd>
        <msubsup><mi>Q</mi><mi>L</mi><msub><mi>&pi;</mi><mi>B</mi></msub></msubsup>
        <mo>(</mo><mi>x</mi><mo>,</mo><mi>a</mi><mo>)</mo>
        <mo>-</mo>
        <msubsup><mi>Q</mi><mi>L</mi><msub><mi>&pi;</mi><mi>B</mi></msub></msubsup>
        <mo>(</mo><mi>x</mi><mo>,</mo><msub><mi>a</mi><mi>B</mi></msub><mo>)</mo>
        <mo>&approx;</mo>
        <msup>
          <mrow><mo>(</mo><mi>a</mi><mo>-</mo><msub><mi>a</mi><mi>B</mi></msub><mo>)</mo></mrow>
          <mi>T</mi>
        </msup>
        <msub><mi>g</mi><mi>L</mi></msub>
        <mo>(</mo><mi>x</mi><mo>)</mo><mo>,</mo>
      </mtd>
    </mtr>
    <mtr>
      <mtd>
        <msub><mi>g</mi><mi>L</mi></msub>
        <mo>(</mo><mi>x</mi><mo>)</mo>
        <mo>=</mo>
        <msub>
          <mrow><msub><mo>&nabla;</mo><mi>a</mi></msub>
          <msubsup><mi>Q</mi><mi>L</mi><msub><mi>&pi;</mi><mi>B</mi></msub></msubsup>
          <mo>(</mo><mi>x</mi><mo>,</mo><mi>a</mi><mo>)</mo></mrow>
          <mrow><mi>a</mi><mo>=</mo><msub><mi>a</mi><mi>B</mi></msub></mrow>
        </msub><mo>.</mo>
      </mtd>
    </mtr>
  </mtable>
</math>

The projection then becomes a Euclidean projection onto a half-space:

<math display="block" aria-label="Action projection onto a Lyapunov half space">
  <mtable columnalign="right left" columnspacing="1em" rowspacing="0.45em">
    <mtr>
      <mtd>
        <msup><mi>a</mi><mo>*</mo></msup>
      </mtd>
      <mtd>
        <mo>=</mo>
        <munder>
          <mrow><mi>arg</mi><mo>&#x2061;</mo><mi>min</mi></mrow>
          <mi>a</mi>
        </munder>
        <mspace width="0.4em"></mspace>
        <mfrac><mn>1</mn><mn>2</mn></mfrac>
        <msup>
          <mrow><mo>||</mo><mi>a</mi><mo>-</mo><mi>u</mi><mo>||</mo></mrow>
          <mn>2</mn>
        </msup>
      </mtd>
    </mtr>
    <mtr>
      <mtd><mtext>subject to</mtext></mtd>
      <mtd>
        <msup>
          <mrow><mo>(</mo><mi>a</mi><mo>-</mo><msub><mi>a</mi><mi>B</mi></msub><mo>)</mo></mrow>
          <mi>T</mi>
        </msup>
        <msub><mi>g</mi><mi>L</mi></msub>
        <mo>(</mo><mi>x</mi><mo>)</mo>
        <mo>&le;</mo>
        <mover accent="true"><mi>&epsilon;</mi><mo>~</mo></mover>
        <mo>(</mo><mi>x</mi><mo>)</mo><mo>.</mo>
      </mtd>
    </mtr>
  </mtable>
</math>

This is attractive because the objective is strongly convex, the constraint is linear, and the single-constraint projection has a closed form. It also modifies only the current action rather than the full policy. For continuous control, that locality is often exactly what one wants: when a nominal action is unsafe only at this state, there is no need to reshape the entire actor network.

The caveat is equally important. The projection is exact for the linearized Lyapunov constraint, not for the true nonlinear constraint. The implementation must also check the sign convention carefully. If the half-space is written as <math><msup><mrow><mo>(</mo><mi>a</mi><mo>-</mo><msub><mi>a</mi><mi>B</mi></msub><mo>)</mo></mrow><mi>T</mi></msup><msub><mi>g</mi><mi>L</mi></msub><mo>&le;</mo><mover accent="true"><mi>&epsilon;</mi><mo>~</mo></mover></math>, a violating nominal action should be corrected in the direction that reduces the left-hand side, not increases it. This is not a fatal conceptual issue; it is an implementation-level convention that must be tested against the actual critic definition.

## Why this can work better than Lagrangian safe RL

A Lagrangian method typically follows a gradient shaped by both task and constraint terms:

<math display="block" aria-label="Lagrangian policy gradient direction">
  <msub><mo>&nabla;</mo><mi>&theta;</mi></msub>
  <mo>[</mo>
  <msup><mi>C</mi><mi>&pi;</mi></msup>
  <mo>+</mo>
  <mi>&lambda;</mi>
  <msup><mi>D</mi><mi>&pi;</mi></msup>
  <mo>]</mo><mo>.</mo>
</math>

This penalizes constraint cost, but it does not directly force each update to satisfy a Lyapunov feasibility condition. If <math><mi>&lambda;</mi></math> is too small, adaptation is delayed, or the critic underestimates constraint cost, an unsafe update can still occur.

The Lyapunov projection approach instead restricts the candidate update or action itself:

```text
Lagrangian:
unsafe update can happen if lambda is too small or critic estimates are wrong.

Lyapunov projection:
the candidate update/action is explicitly projected into a local safe set.
```

This difference is structural. The projection step introduces a local feasibility geometry before execution or parameter acceptance. The <math><mi>a</mi></math>-projection may be less conservative than the <math><mi>&theta;</mi></math>-projection because it corrects only the current action. By contrast, <math><mi>&theta;</mi></math>-projection modifies the global policy parameters, which can be necessary for policy-level improvement but can also suppress useful behavior in states that did not require correction.

## What is mathematically guaranteed?

The guarantees should be separated into layers. The exact finite-CMDP logic is much stronger than the practical deep continuous-control approximation.

### Exact finite CMDP theory

In finite known CMDPs, with exact transition and value information, a state-wise Lyapunov condition implies expected cumulative constraint feasibility. More precisely, if an exact Lyapunov function satisfies

<math display="block" aria-label="Exact Lyapunov condition for finite CMDP">
  <msub><mi>T</mi><mrow><mi>&pi;</mi><mo>,</mo><mi>d</mi></mrow></msub>
  <mo>[</mo><mi>L</mi><mo>]</mo>
  <mo>(</mo><mi>x</mi><mo>)</mo>
  <mo>&le;</mo>
  <mi>L</mi><mo>(</mo><mi>x</mi><mo>)</mo>
  <mspace width="0.4em"></mspace><mtext>for all </mtext><mi>x</mi>
</math>

and <math><mi>L</mi><mo>(</mo><msub><mi>x</mi><mn>0</mn></msub><mo>)</mo><mo>&le;</mo><msub><mi>d</mi><mn>0</mn></msub></math>, then the expected cumulative constraint cost satisfies <math><msup><mi>D</mi><mi>&pi;</mi></msup><mo>(</mo><msub><mi>x</mi><mn>0</mn></msub><mo>)</mo><mo>&le;</mo><msub><mi>d</mi><mn>0</mn></msub></math>. This is the strongest theoretical part of the framework.

### θ-projection local approximation

For <math><mi>&theta;</mi></math>-projection, the practical guarantee depends on function approximation error, Taylor approximation quality, the sampled-state representation of an originally state-wise condition, and the validity of the KL or surrogate trust-region model. These are local approximation assumptions, not a global hard-safety theorem.

### a-projection convex projection

Given the linearized half-space constraint, the <math><mi>a</mi></math>-projection is a convex quadratic program with a unique solution. That statement is rigorous for the surrogate projection problem. However, satisfying the linearized half-space does not necessarily imply satisfying the true nonlinear Lyapunov constraint, especially when the action move is large or the learned Lyapunov critic has substantial error.

## Experiments and empirical interpretation

The memo reports continuous-control evaluations on MuJoCo-style safety tasks: HalfCheetah-Safe, Point-Circle, Point-Gather, and Ant-Gather. It also describes a real-world indoor robot-navigation setting with noisy lidar, relative goal position, robot orientation, linear and angular velocity actions, and collision impact energy as the constraint cost.

The empirical interpretation should be conservative. Lyapunov-based projection methods tend to reduce constraint violations relative to unconstrained or Lagrangian baselines while maintaining reasonable task performance. This is meaningful evidence that the projection architecture can improve the learning tradeoff.

It is not evidence of hard real-world safety. The robot experiment still lives with stochasticity, function approximation, and imperfect sensing. The memo also notes that the paper acknowledges premature convergence above the constraint threshold. That observation matters: even when the projection mechanism improves constraint behavior, the deployed deep-RL system can remain only approximately safe.

## Weak assumptions and limitations

First, a feasible baseline policy is required. This is not a minor detail. In robotics, process control, or energy-system operation, obtaining a baseline that is both useful and constraint-feasible can itself require conservative control design, domain knowledge, or robust optimization.

Second, CMDP safety is expectation-based. It controls expected cumulative constraint cost, not trajectory-wise hard avoidance. Rare but severe events require additional risk-sensitive, robust, chance-constrained, barrier, or verification machinery.

Third, continuous-state Lyapunov constraints are approximated by sampled states. If the sampled distribution misses rare but critical states, the learned projection can look feasible during training while failing where safety matters most.

Fourth, the Taylor linearization is local. The half-space safety layer is elegant precisely because it linearizes the Lyapunov critic, but that also means the certificate can degrade when the nominal action is far from the baseline action or when the critic curvature is strong.

Fifth, constraint-critic approximation error can break safety. A projection based on an underestimated <math><msub><mi>Q</mi><mi>L</mi></msub></math> may certify an action that is unsafe under the true constraint dynamics. This is a central limitation of deep safe RL, not just a numerical inconvenience.

Sixth, multiple simultaneous constraints are harder than the single-constraint closed-form projection case. With several active constraints, the projection becomes a multi-constraint QP, and feasibility, conditioning, and conflict among constraints become more important.

Seventh, process systems make this limitation concrete. Pressure, temperature, inventories, emissions, ramping limits, actuator bounds, quality specifications, and energy-market constraints can all become active at once. A single half-space safety layer may be too weak for such coupled nonlinear feasibility geometry.

## Takeaway

This paper is best understood as a practical bridge from finite CMDP Lyapunov safe policy iteration to continuous-control deep safe RL. Its main value is not a global hard-safety theorem, but a projection-based architecture that makes Lyapunov safety ideas usable with DDPG/PPO-style policy-gradient methods.

The useful lesson is structural: instead of hoping that a penalty term eventually discourages unsafe behavior, the algorithm reshapes the update/action space so that learning is locally biased toward Lyapunov-feasible directions.

## References

Chow Y, Nachum O, Faust A, Duenez-Guzman E, Ghavamzadeh M. Lyapunov-based Safe Policy Optimization for Continuous Control. arXiv preprint arXiv:1901.10031. 2019. doi:10.48550/arXiv.1901.10031.

Chow Y, Nachum O, Duenez-Guzman E, Ghavamzadeh M. A lyapunov-based approach to safe reinforcement learning. Advances in neural information processing systems. 2018;31.

<!-- ko -->

## 왜 이 문제가 중요한가

안전이 중요한 학습 문제에서는 제어기가 충분히 탐색한 뒤에야 안전해지는 것으로는 부족한 경우가 많다. 사람 가까이에서 움직이는 로봇, 압력이나 온도 한계 근처의 화학 공정 제어기, 신뢰도와 배출을 함께 맞춰야 하는 에너지 시스템 운영자, 구동기 한계 아래에서 작동하는 자율 플랫폼은 수많은 unsafe trial을 소비한 뒤 수렴하는 방식을 허용하지 않을 수 있다. 이런 설정에서는 최종 reward curve뿐 아니라 학습 궤적 자체가 중요하다.

Lagrangian penalty를 쓰는 표준 강화학습은 평균적인 제약 위반을 줄일 수 있지만, penalty multiplier 자체가 학습되거나 조정된다. 승수가 너무 작거나, constraint critic이 부정확하거나, 정책 업데이트가 과격하면 학습자는 여전히 unsafe intermediate policy를 지나갈 수 있다.

CMDP는 기대 누적 제약 비용을 제한함으로써 안전 문제를 더 명시적으로 만든다. 다만 이것은 hard pathwise safety와 다르다. CMDP bound는 기대 할인 충돌 비용, 에너지 impact, violation burden이 예산 아래에 있다고 말할 수 있지만, 그것만으로 모든 실제 unsafe trajectory를 배제하지는 않는다.

## 앞선 Lyapunov CMDP 접근이 할 수 있었던 것과 깨지는 지점

앞선 Lyapunov safe-RL 아이디어는 유한 CMDP에서 출발해 전역 기대 누적 제약을 상태별 Lyapunov 실행 가능성 조건으로 바꾼다. 가장 깨끗한 정확한 형태에서 certificate는 다음처럼 요약된다.

<math display="block" aria-label="Lyapunov state-wise condition implies expected constraint feasibility">
  <mtable columnalign="center" rowspacing="0.4em">
    <mtr>
      <mtd>
        <msub><mi>T</mi><mrow><mi>&pi;</mi><mo>,</mo><mi>d</mi></mrow></msub>
        <mo>[</mo><mi>L</mi><mo>]</mo>
        <mo>(</mo><mi>x</mi><mo>)</mo>
        <mo>&le;</mo>
        <mi>L</mi><mo>(</mo><mi>x</mi><mo>)</mo><mo>,</mo>
        <mspace width="0.5em"></mspace>
        <mo>&forall;</mo><mi>x</mi><mo>,</mo>
      </mtd>
    </mtr>
    <mtr>
      <mtd>
        <mi>L</mi><mo>(</mo><msub><mi>x</mi><mn>0</mn></msub><mo>)</mo>
        <mo>&le;</mo>
        <msub><mi>d</mi><mn>0</mn></msub>
        <mspace width="0.8em"></mspace>
        <mo>&Rightarrow;</mo>
        <mspace width="0.8em"></mspace>
        <msup><mi>D</mi><mi>&pi;</mi></msup>
        <mo>(</mo><msub><mi>x</mi><mn>0</mn></msub><mo>)</mo>
        <mo>&le;</mo>
        <msub><mi>d</mi><mn>0</mn></msub><mo>.</mo>
      </mtd>
    </mtr>
  </mtable>
</math>

여기서 <math><msup><mi>D</mi><mi>&pi;</mi></msup><mo>(</mo><msub><mi>x</mi><mn>0</mn></msub><mo>)</mo></math>는 정책 <math><mi>&pi;</mi></math>의 할인 누적 제약 비용이고, <math><msub><mi>d</mi><mn>0</mn></msub></math>는 허용 예산이다. <math><mi>L</mi><mo>(</mo><mi>x</mi><mo>)</mo></math>는 미래 제약 비용의 Lyapunov 상한 또는 상태 의존적인 남은 안전 envelope다. <math><msub><mi>T</mi><mrow><mi>&pi;</mi><mo>,</mo><mi>d</mi></mrow></msub></math>는 Bellman-like operator로, 즉각 제약 비용과 한 번 전이한 뒤의 기대 Lyapunov burden을 더한다.

이 형식의 강점은 국소성이다. 전역 예산을 사후에만 확인하는 것이 아니라, 정책 자체를 상태별 조건으로 제한한다. 하지만 유한 CMDP 장치는 연속 제어로 매끄럽게 옮겨가지 않는다. 연속 행동에서는 행동 합이 적분이 되어 일반적으로 정확하게 평가하기 어렵다. 연속 상태에서는 Lyapunov 실행 가능성 조건이 모든 상태에 대한 무한 차원 제약족이 된다. 따라서 정확한 value iteration이나 policy iteration은 더 이상 실용적인 구현 경로가 아니다.

## 후속 논문의 핵심 아이디어

후속 논문은 알고리즘의 대상을 바꾼다. 안전 정책 반복을 정확히 푸는 대신 DDPG나 PPO 같은 표준 policy-gradient 방법에서 출발해, 학습 파이프라인 안에 Lyapunov-induced projection을 삽입한다. 구조는 다음처럼 읽을 수 있다.

```text
state x
  |-- actor pi_theta -> nominal action u
  |-- task critic Q(x,a)
  `-- constraint/Lyapunov critic Q_D(x,a), Q_L(x,a)
          |
          v
   Lyapunov constraint gradient
          |
          v
   projection module
          |
          v
   safe policy update or safe action
```

요약하면 다음과 같다.

```text
standard policy-gradient algorithm
+ Lyapunov critic / constraint critic
+ projection mechanism
= safe policy optimization
```

기여는 단순히 "Lyapunov function을 safe RL에 썼다"가 아니다. 더 구체적으로는 Lyapunov safe policy iteration을 연속 행동 policy-gradient training 및 projection-based update와 결합한 것이다.

논문은 두 가지 projection 관점을 전개한다. <math><mi>&theta;</mi></math>-projection은 정책 파라미터 업데이트를 수정한다. <math><mi>a</mi></math>-projection, 또는 Lyapunov safety layer는 현재 상태에서 생성된 행동만 수정한다.

## θ-projection: 정책 업데이트의 투영

<math><mi>&theta;</mi></math>-projection은 정책 파라미터 수준에서 작동한다. 이상적인 제약 업데이트에서는 새 파라미터가 목적을 개선하면서 feasible baseline policy에 대한 Lyapunov-induced constraint를 만족하도록 선택된다.

<math display="block" aria-label="Theta projection constrained policy update">
  <mtable columnalign="right left" columnspacing="1em" rowspacing="0.45em">
    <mtr>
      <mtd>
        <msup><mi>&theta;</mi><mo>+</mo></msup>
      </mtd>
      <mtd>
        <mo>=</mo>
        <munder>
          <mrow><mi>arg</mi><mo>&#x2061;</mo><mi>min</mi></mrow>
          <mi>&theta;</mi>
        </munder>
        <mspace width="0.4em"></mspace>
        <msup><mi>C</mi><msub><mi>&pi;</mi><mi>&theta;</mi></msub></msup>
        <mo>(</mo><msub><mi>x</mi><mn>0</mn></msub><mo>)</mo>
      </mtd>
    </mtr>
    <mtr>
      <mtd><mtext>subject to</mtext></mtd>
      <mtd>
        <msub><mo>&int;</mo><mi>A</mi></msub>
        <mo>[</mo>
        <msub><mi>&pi;</mi><mi>&theta;</mi></msub>
        <mo>(</mo><mi>a</mi><mo>|</mo><mi>x</mi><mo>)</mo>
        <mo>-</mo>
        <msub><mi>&pi;</mi><mi>B</mi></msub>
        <mo>(</mo><mi>a</mi><mo>|</mo><mi>x</mi><mo>)</mo>
        <mo>]</mo>
        <msubsup><mi>Q</mi><mi>L</mi><msub><mi>&pi;</mi><mi>B</mi></msub></msubsup>
        <mo>(</mo><mi>x</mi><mo>,</mo><mi>a</mi><mo>)</mo>
        <mi>d</mi><mi>a</mi>
        <mo>&le;</mo>
        <mover accent="true"><mi>&epsilon;</mi><mo>~</mo></mover>
        <mo>(</mo><mi>x</mi><mo>)</mo><mo>,</mo>
        <mspace width="0.5em"></mspace>
        <mo>&forall;</mo><mi>x</mi><mo>.</mo>
      </mtd>
    </mtr>
  </mtable>
</math>

이 식은 올바른 개념적 대상이지만 deep continuous control에서 직접 풀기에는 너무 어렵다. 따라서 목적함수는 conservative policy-gradient 또는 KL-regularized local surrogate로 근사된다. 이 점에서 방법은 TRPO/CPO 계열의 국소 업데이트 논리와 연결된다. Lyapunov 제약은 baseline parameter <math><msub><mi>&theta;</mi><mi>B</mi></msub></math> 주변에서 선형화되고, 모든 상태에 대한 무한 제약족은 실제로는 sampled 또는 averaged constraint로 대체된다.

직관은 단순하다. 정책 업데이트는 임의의 reward-improving 방향으로 움직일 수 없다. Lyapunov-safe update set의 국소 근사 안에 남아야 한다. 여기서 실행 가능성은 손실함수에 더해진 scalar penalty가 아니라 update geometry에 대한 제한으로 표현된다.

단점은 parameter-level restriction이 둔할 수 있다는 점이다. <math><mi>&theta;</mi></math>의 작은 변화가 민감한 상태 영역에서 큰 행동 변화를 만들 수 있고, 엄격한 parameter projection은 실제로는 국소 행동 조정만 필요할 때도 정책 전체를 과도하게 보정할 수 있다. 따라서 <math><mi>&theta;</mi></math>-projection은 이론적으로 자연스럽지만 실제로는 보수적일 수 있다.

## a-projection / Lyapunov safety layer

<math><mi>a</mi></math>-projection은 더 직접적이다. actor가 먼저 무제약 nominal action을 제안한다.

<math display="block" aria-label="Nominal actor action">
  <mi>u</mi>
  <mo>=</mo>
  <msub><mi>&pi;</mi><mi>&theta;</mi></msub>
  <mo>(</mo><mi>x</mi><mo>)</mo><mo>.</mo>
</math>

그다음 safety layer는 baseline action <math><msub><mi>a</mi><mi>B</mi></msub><mo>=</mo><msub><mi>&pi;</mi><mi>B</mi></msub><mo>(</mo><mi>x</mi><mo>)</mo></math>에 대한 국소 Lyapunov constraint를 만족하는 가장 가까운 행동을 선택한다.

<math display="block" aria-label="Action projection with nonlinear Lyapunov constraint">
  <mtable columnalign="right left" columnspacing="1em" rowspacing="0.45em">
    <mtr>
      <mtd>
        <msup><mi>a</mi><mo>*</mo></msup>
      </mtd>
      <mtd>
        <mo>=</mo>
        <munder>
          <mrow><mi>arg</mi><mo>&#x2061;</mo><mi>min</mi></mrow>
          <mi>a</mi>
        </munder>
        <mspace width="0.4em"></mspace>
        <mfrac><mn>1</mn><mn>2</mn></mfrac>
        <msup>
          <mrow><mo>||</mo><mi>a</mi><mo>-</mo><mi>u</mi><mo>||</mo></mrow>
          <mn>2</mn>
        </msup>
      </mtd>
    </mtr>
    <mtr>
      <mtd><mtext>subject to</mtext></mtd>
      <mtd>
        <msubsup><mi>Q</mi><mi>L</mi><msub><mi>&pi;</mi><mi>B</mi></msub></msubsup>
        <mo>(</mo><mi>x</mi><mo>,</mo><mi>a</mi><mo>)</mo>
        <mo>-</mo>
        <msubsup><mi>Q</mi><mi>L</mi><msub><mi>&pi;</mi><mi>B</mi></msub></msubsup>
        <mo>(</mo><mi>x</mi><mo>,</mo><msub><mi>a</mi><mi>B</mi></msub><mo>)</mo>
        <mo>&le;</mo>
        <mover accent="true"><mi>&epsilon;</mi><mo>~</mo></mover>
        <mo>(</mo><mi>x</mi><mo>)</mo><mo>.</mo>
      </mtd>
    </mtr>
  </mtable>
</math>

<math><msub><mi>Q</mi><mi>L</mi></msub><mo>(</mo><mi>x</mi><mo>,</mo><mi>a</mi><mo>)</mo></math>는 일반적으로 행동 <math><mi>a</mi></math>에 대해 비선형이므로, 논문은 baseline action <math><msub><mi>a</mi><mi>B</mi></msub></math> 주변의 1차 국소 근사를 사용한다. 그러면 projection은 하나의 반공간(half-space)에 대한 Euclidean projection이 된다.

<math display="block" aria-label="Action projection onto a Lyapunov half space">
  <mtable columnalign="right left" columnspacing="1em" rowspacing="0.45em">
    <mtr>
      <mtd>
        <msup><mi>a</mi><mo>*</mo></msup>
      </mtd>
      <mtd>
        <mo>=</mo>
        <munder>
          <mrow><mi>arg</mi><mo>&#x2061;</mo><mi>min</mi></mrow>
          <mi>a</mi>
        </munder>
        <mspace width="0.4em"></mspace>
        <mfrac><mn>1</mn><mn>2</mn></mfrac>
        <msup>
          <mrow><mo>||</mo><mi>a</mi><mo>-</mo><mi>u</mi><mo>||</mo></mrow>
          <mn>2</mn>
        </msup>
      </mtd>
    </mtr>
    <mtr>
      <mtd><mtext>subject to</mtext></mtd>
      <mtd>
        <msup>
          <mrow><mo>(</mo><mi>a</mi><mo>-</mo><msub><mi>a</mi><mi>B</mi></msub><mo>)</mo></mrow>
          <mi>T</mi>
        </msup>
        <msub><mi>g</mi><mi>L</mi></msub>
        <mo>(</mo><mi>x</mi><mo>)</mo>
        <mo>&le;</mo>
        <mover accent="true"><mi>&epsilon;</mi><mo>~</mo></mover>
        <mo>(</mo><mi>x</mi><mo>)</mo><mo>.</mo>
      </mtd>
    </mtr>
  </mtable>
</math>

이것은 목적함수가 strongly convex이고 제약이 선형이며, 단일 제약 projection에는 닫힌형 해가 있다는 점에서 매력적이다. 또한 정책 전체가 아니라 현재 행동만 수정한다. 연속 제어에서는 이 국소성이 중요하다. nominal action이 현재 상태에서만 unsafe하다면 actor network 전체를 다시 만드는 것이 필요하지 않을 수 있다.

하지만 caveat도 중요하다. projection은 선형화된 Lyapunov 제약에 대해서 정확할 뿐, 실제 비선형 제약에 대해서 정확한 것은 아니다. 구현은 부호 관례도 조심해야 한다. half-space가 <math><msup><mrow><mo>(</mo><mi>a</mi><mo>-</mo><msub><mi>a</mi><mi>B</mi></msub><mo>)</mo></mrow><mi>T</mi></msup><msub><mi>g</mi><mi>L</mi></msub><mo>&le;</mo><mover accent="true"><mi>&epsilon;</mi><mo>~</mo></mover></math>로 쓰이면, 위반한 nominal action은 좌변을 줄이는 방향으로 보정되어야 한다. 이것은 개념의 치명적 결함이라기보다, critic 정의에 맞춰 테스트해야 하는 구현 관례 문제다.

## 왜 Lagrangian safe RL보다 나을 수 있는가

Lagrangian 방법은 보통 task와 constraint 항이 결합된 gradient를 따른다.

<math display="block" aria-label="Lagrangian policy gradient direction">
  <msub><mo>&nabla;</mo><mi>&theta;</mi></msub>
  <mo>[</mo>
  <msup><mi>C</mi><mi>&pi;</mi></msup>
  <mo>+</mo>
  <mi>&lambda;</mi>
  <msup><mi>D</mi><mi>&pi;</mi></msup>
  <mo>]</mo><mo>.</mo>
</math>

이 방식은 제약 비용을 벌점화하지만, 각 업데이트가 Lyapunov 실행 가능성 조건을 만족하도록 직접 강제하지는 않는다. <math><mi>&lambda;</mi></math>가 너무 작거나, adaptation이 늦거나, critic이 제약 비용을 과소평가하면 unsafe update가 여전히 발생할 수 있다.

Lyapunov projection 접근은 후보 업데이트 또는 행동 자체를 제한한다.

```text
Lagrangian:
lambda가 너무 작거나 critic 추정이 틀리면 unsafe update가 발생할 수 있다.

Lyapunov projection:
candidate update/action을 국소 safe set 안으로 명시적으로 투영한다.
```

차이는 구조적이다. projection step은 실행 또는 파라미터 수용 전에 국소 실행 가능성 geometry를 도입한다. <math><mi>a</mi></math>-projection은 현재 행동만 보정하므로 <math><mi>&theta;</mi></math>-projection보다 덜 보수적일 수 있다. 반대로 <math><mi>&theta;</mi></math>-projection은 policy-level improvement에는 필요할 수 있지만, 보정이 필요 없던 상태의 유용한 행동까지 억제할 수 있다.

## 무엇이 수학적으로 보장되는가?

보장은 여러 층으로 분리해야 한다. 정확한 유한 CMDP 논리는 실용적인 deep continuous-control 근사보다 훨씬 강하다.

### 정확한 유한 CMDP 이론

유한하고 알려진 CMDP에서, 정확한 전이와 value 정보가 있으면 state-wise Lyapunov 조건은 기대 누적 제약 실행 가능성을 함의한다. 정확한 Lyapunov 함수가 모든 상태에서 <math><msub><mi>T</mi><mrow><mi>&pi;</mi><mo>,</mo><mi>d</mi></mrow></msub><mo>[</mo><mi>L</mi><mo>]</mo><mo>(</mo><mi>x</mi><mo>)</mo><mo>&le;</mo><mi>L</mi><mo>(</mo><mi>x</mi><mo>)</mo></math>를 만족하고 <math><mi>L</mi><mo>(</mo><msub><mi>x</mi><mn>0</mn></msub><mo>)</mo><mo>&le;</mo><msub><mi>d</mi><mn>0</mn></msub></math>이면, 기대 누적 제약 비용은 <math><msup><mi>D</mi><mi>&pi;</mi></msup><mo>(</mo><msub><mi>x</mi><mn>0</mn></msub><mo>)</mo><mo>&le;</mo><msub><mi>d</mi><mn>0</mn></msub></math>를 만족한다. 이것이 프레임워크에서 가장 강한 이론적 부분이다.

### θ-projection의 국소 근사

<math><mi>&theta;</mi></math>-projection의 실제 보장은 함수근사 오차, Taylor 근사 품질, 원래 상태별 조건을 sampled-state로 대표하는 방식, KL 또는 surrogate trust-region 모델의 타당성에 의존한다. 이는 전역 hard-safety theorem이 아니라 국소 근사 가정이다.

### a-projection의 볼록 projection

선형화된 half-space 제약이 주어지면 <math><mi>a</mi></math>-projection은 유일한 해를 갖는 convex quadratic program이다. 이 문장은 surrogate projection 문제에 대해서는 엄밀하다. 그러나 선형화된 half-space를 만족한다고 해서 실제 비선형 Lyapunov 제약을 반드시 만족하는 것은 아니다. 특히 action move가 크거나 학습된 Lyapunov critic의 오차가 클 때 그렇다.

## 실험과 경험적 해석

메모는 HalfCheetah-Safe, Point-Circle, Point-Gather, Ant-Gather 같은 MuJoCo 스타일 안전 task와 실내 로봇 navigation 실험을 보고한다. 로봇 설정에는 noisy lidar, 상대 goal position, robot orientation, 선속도 및 각속도 action, collision impact energy 제약 비용이 포함된다.

해석은 보수적이어야 한다. Lyapunov-based projection 방법이 무제약 또는 Lagrangian baseline에 비해 제약 위반을 줄이면서 합리적인 task performance를 유지하는 경향은 의미 있는 증거다. projection architecture가 학습 tradeoff를 개선할 수 있다는 것을 보여 준다.

그러나 hard real-world safety의 증거는 아니다. 로봇 실험도 stochasticity, function approximation, imperfect sensing을 안고 있다. 메모는 논문이 constraint threshold 위에서 premature convergence가 나타날 수 있음을 인정한다고 기록한다. 이것은 중요하다. projection mechanism이 제약 행동을 개선하더라도, 배포된 deep-RL system은 여전히 approximate safety에 머물 수 있다.

## 약한 가정과 한계

첫째, feasible baseline policy가 필요하다. 로보틱스, 공정 제어, 에너지 시스템 운영에서 유용하면서 제약을 만족하는 baseline을 얻는 일은 보수적 제어 설계, domain knowledge, robust optimization을 요구할 수 있다.

둘째, CMDP safety는 expectation-based다. 기대 누적 제약 비용을 통제하지만 trajectory-wise hard avoidance는 아니다. 드물지만 심각한 사건은 risk-sensitive, robust, chance-constrained, barrier, verification 기법을 추가로 요구한다.

셋째, 연속 상태 Lyapunov 제약은 sampled states로 근사된다. 샘플 분포가 드물지만 중요한 상태를 놓치면, 학습 중에는 feasible해 보이는 projection이 안전이 중요한 곳에서 실패할 수 있다.

넷째, Taylor linearization은 국소적이다. half-space safety layer가 우아한 이유는 Lyapunov critic을 선형화하기 때문이지만, nominal action이 baseline action에서 멀거나 critic curvature가 강할 때 certificate가 약해질 수 있다.

다섯째, constraint-critic approximation error는 안전을 깨뜨릴 수 있다. 과소평가된 <math><msub><mi>Q</mi><mi>L</mi></msub></math>에 기반한 projection은 실제 제약 동역학에서는 unsafe한 행동을 인증할 수 있다. 이것은 단순한 수치 문제가 아니라 deep safe RL의 중심 한계다.

여섯째, 여러 제약이 동시에 있을 때는 단일 제약 closed-form projection보다 훨씬 어렵다. 여러 제약이 활성화되면 projection은 multi-constraint QP가 되고, feasibility, conditioning, constraint conflict가 더 중요해진다.

일곱째, process systems는 이 한계를 구체적으로 보여 준다. 압력, 온도, 재고, 배출, ramping limit, actuator bound, 품질 specification, 에너지 시장 제약이 모두 동시에 활성화될 수 있다. 단일 half-space safety layer는 이런 결합 비선형 실행 가능성 geometry에는 약할 수 있다.

## 핵심 정리

이 논문은 유한 CMDP의 Lyapunov safe policy iteration에서 연속 제어 deep safe RL로 가는 실용적 다리로 이해하는 것이 가장 좋다. 주된 가치는 전역 hard-safety theorem이 아니라, DDPG/PPO 스타일 policy-gradient 방법에서 Lyapunov safety 아이디어를 사용할 수 있게 하는 projection-based architecture다.

유용한 교훈은 구조적이다. unsafe behavior가 penalty term에 의해 언젠가 줄어들기를 기대하는 대신, 알고리즘은 update/action space 자체를 reshape해서 학습이 국소적으로 Lyapunov-feasible direction을 향하도록 만든다.

## 참고문헌

Chow Y, Nachum O, Faust A, Duenez-Guzman E, Ghavamzadeh M. Lyapunov-based Safe Policy Optimization for Continuous Control. arXiv preprint arXiv:1901.10031. 2019. doi:10.48550/arXiv.1901.10031.

Chow Y, Nachum O, Duenez-Guzman E, Ghavamzadeh M. A lyapunov-based approach to safe reinforcement learning. Advances in neural information processing systems. 2018;31.
