---
layout: post
title: "Lyapunov Projection for Continuous-Action Safe Reinforcement Learning"
date: 2026-05-28
category: safe-constrained-rl
category_label: "Safe & Constrained RL"
paper_title: "Lyapunov-based Safe Policy Optimization for Continuous Control"
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
language: "en"
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
