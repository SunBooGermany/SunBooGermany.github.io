---
layout: post
title: "Lyapunov-Based Safe Policy Improvement for CMDPs"
date: 2026-05-26
category: safe-constrained-rl
category_label: "Safe & Constrained RL"
paper_title: "A lyapunov-based approach to safe reinforcement learning"
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
language: "en-ko"
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
