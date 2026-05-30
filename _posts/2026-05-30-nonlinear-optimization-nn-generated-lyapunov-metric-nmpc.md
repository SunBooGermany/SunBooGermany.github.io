---
layout: post
title: "NN-Generated Lyapunov Metrics for Fast NMPC: What Is Actually Guaranteed?"
date: 2026-05-30
category: nonlinear-optimization
category_label: "Nonlinear Optimization"
research_group: algorithmic_reviews
research_category: nonlinear-optimization
research_category_label: "Nonlinear Optimization"
application_category: ""
application_category_label: ""
method_category: stochastic-nonlinear-optimization
method_category_label: "Stochastic & Nonlinear Optimization"
paper_title: ""
authors: ""
venue: ""
year: ""
doi: ""
arxiv: ""
source_url: ""
tags:
  - nonlinear-mpc
  - lyapunov-function
  - terminal-cost
  - neural-network-surrogate
  - continuation-value
  - stability
excerpt: "A critical note on learned Lyapunov terminal costs for NMPC, focusing on Cholesky-structured positive-definite surrogates, horizon compression, and the unresolved role of approximation error."
language: "en-ko"
has_korean_note: true
---

## Positioning: why this problem matters in real systems

Nonlinear model predictive control is attractive because it can handle nonlinear dynamics, constraints, changing references, and multi-step tradeoffs in one optimization problem. That is why NMPC appears naturally in chemical process control, robotic motion, autonomous parking, energy storage operation, hydrogen supply chains, and other systems where the controller must reason ahead while respecting physical limits.

The difficulty is timing. At every sampling instant, NMPC solves a nonlinear optimization problem over a finite horizon. A longer horizon usually gives better foresight: the controller can avoid myopic actions, anticipate delayed constraint effects, and approximate stabilizing behavior more reliably. But a long horizon also increases the online nonlinear programming burden.

A short-horizon NMPC controller is faster, but it can be shortsighted. It may choose an action that looks good over one or two steps but makes the later problem difficult, expensive, or infeasible. The central question of this note is therefore practical: can a learned terminal or continuation cost preserve some of the value of a long horizon while allowing a much shorter online horizon?

In Korean terms, the issue is not simply "NN을 쓰느냐" but "미래 비용과 안정화 구조를 어떤 형태로 압축하느냐"이다. The architecture matters because a generic scalar neural value function and a positive-definite Lyapunov-compatible metric are not the same object.

## Problem setting

The control problem is a parameterized NMPC problem. The state is <math><mi>x</mi></math>, the control is optimized online, and <math><mi>p</mi></math> denotes a parameter vector such as a reference, operating condition, exogenous signal, or steady-state descriptor. The desired state or steady-state target is written as <math><msub><mi>x</mi><mi>s</mi></msub></math>.

Long-horizon NMPC implicitly computes a continuation value: the cost-to-go after the first action. If that continuation value were known exactly, a one-step online problem plus the exact continuation value could reproduce the first decision of the long-horizon problem under the same modeling assumptions. This is the Bellman-style horizon-compression intuition behind the method.

The supplied material describes an online horizon of <math><mi>N</mi><mo>=</mo><mn>1</mn></math>. The missing information is replaced by a learned terminal/continuation surrogate. This reduces the online decision dimension, but it does not remove nonlinear dynamics, nonconvexity, local optima, numerical conditioning, or feasibility issues. It compresses the horizon; it does not turn NMPC into a trivial lookup table.

## Prior research gap

Classical stabilizing NMPC usually relies on three terminal ingredients:

- a terminal set <math><msub><mi>X</mi><mi>f</mi></msub></math>,
- a terminal cost <math><mi>F</mi></math>,
- and a local stabilizing controller <math><msub><mi>&kappa;</mi><mi>f</mi></msub></math>.

These ingredients give a route to recursive feasibility and Lyapunov decrease, but they can be hard to design for strongly nonlinear systems, changing operating points, and high-dimensional parameterized tasks. Long-horizon terminal-constraint-free NMPC can sometimes recover stabilizing behavior by making the finite horizon sufficiently long, but that moves the burden into online computation.

Explicit MPC and neural-network approximate MPC reduce online cost by approximating either the policy or the optimization map. The tradeoff is that approximation often weakens the clean stability and feasibility story. A generic learned terminal cost can approximate a value function, but an arbitrary scalar neural network does not naturally guarantee positive definiteness, nor does it automatically behave like a Lyapunov function.

This is the gap the method is trying to occupy: learn a continuation surrogate that is computationally useful online, but impose enough structure that the terminal cost has at least a Lyapunov-compatible metric form.

## Core idea

The core idea is data-driven horizon compression. Offline, the method uses long-horizon NMPC solutions to supervise a terminal/continuation surrogate. Online, the controller solves a much shorter NMPC problem, potentially with <math><mi>N</mi><mo>=</mo><mn>1</mn></math>, and relies on the learned terminal term to represent the omitted future.

If the exact continuation value <math><msup><mi>V</mi><mo>*</mo></msup><mo>(</mo><mi>x</mi><mo>,</mo><mi>p</mi><mo>)</mo></math> were available, the one-step decomposition would be conceptually clean:

<math display="block" aria-label="One-step NMPC with exact continuation value">
  <munder>
    <mrow><mi>min</mi></mrow>
    <mi>u</mi>
  </munder>
  <mspace width="0.4em"></mspace>
  <mi>&ell;</mi><mo>(</mo><mi>x</mi><mo>,</mo><mi>u</mi><mo>,</mo><mi>p</mi><mo>)</mo>
  <mo>+</mo>
  <msup><mi>V</mi><mo>*</mo></msup>
  <mo>(</mo><msup><mi>x</mi><mo>+</mo></msup><mo>,</mo><msup><mi>p</mi><mo>+</mo></msup><mo>)</mo>
</math>

Here, <math><mi>&ell;</mi></math> is the one-step stage cost, <math><msup><mi>x</mi><mo>+</mo></msup></math> is the next state produced by the nonlinear dynamics, and <math><msup><mi>p</mi><mo>+</mo></msup></math> is the updated parameter. The problem is that <math><msup><mi>V</mi><mo>*</mo></msup></math> is generally unknown. The paper therefore learns a surrogate, but with a special structure: the neural network generates a positive-definite terminal matrix rather than directly outputting an arbitrary scalar cost.

## Mathematical structure: key architecture

The distinctive architecture is this: a feedforward neural network receives <math><mi>p</mi></math> and outputs the lower-triangular entries of a matrix <math><msub><mi>L</mi><mi>&theta;</mi></msub><mo>(</mo><mi>p</mi><mo>)</mo></math>. The terminal matrix is then constructed as

<math display="block" aria-label="Neural-network-generated positive-definite terminal matrix">
  <msub><mi>P</mi><mi>&theta;</mi></msub>
  <mo>(</mo><mi>p</mi><mo>)</mo>
  <mo>=</mo>
  <msub><mi>L</mi><mi>&theta;</mi></msub>
  <mo>(</mo><mi>p</mi><mo>)</mo>
  <msup>
    <mrow><msub><mi>L</mi><mi>&theta;</mi></msub><mo>(</mo><mi>p</mi><mo>)</mo></mrow>
    <mi>T</mi>
  </msup>
  <mo>+</mo>
  <mi>&epsilon;</mi><mi>I</mi><mo>.</mo>
</math>

The term <math><msub><mi>L</mi><mi>&theta;</mi></msub><mo>(</mo><mi>p</mi><mo>)</mo></math> is the lower-triangular factor generated by the neural network. The matrix <math><msub><mi>P</mi><mi>&theta;</mi></msub><mo>(</mo><mi>p</mi><mo>)</mo></math> is the learned terminal metric. The scalar <math><mi>&epsilon;</mi><mo>></mo><mn>0</mn></math> is a fixed positive regularization constant, and <math><mi>I</mi></math> is the identity matrix.

The learned terminal/continuation surrogate is

<math display="block" aria-label="Learned Lyapunov-compatible terminal cost">
  <msub><mover accent="true"><mi>V</mi><mo>^</mo></mover><mi>&theta;</mi></msub>
  <mo>(</mo><mi>x</mi><mo>,</mo><mi>p</mi><mo>)</mo>
  <mo>=</mo>
  <msup>
    <mrow><mo>(</mo><mi>x</mi><mo>-</mo><msub><mi>x</mi><mi>s</mi></msub><mo>)</mo></mrow>
    <mi>T</mi>
  </msup>
  <msub><mi>P</mi><mi>&theta;</mi></msub>
  <mo>(</mo><mi>p</mi><mo>)</mo>
  <mo>(</mo><mi>x</mi><mo>-</mo><msub><mi>x</mi><mi>s</mi></msub><mo>)</mo><mo>.</mo>
</math>

This equation says that the terminal cost is quadratic in the state error <math><mi>x</mi><mo>-</mo><msub><mi>x</mi><mi>s</mi></msub></math>, but the quadratic metric changes with the parameter <math><mi>p</mi></math>. The neural network is therefore not simply "the value function." It is a generator of a Cholesky-type Lyapunov metric.

The information flow is compact:

```text
parameter p
   |
   v
Feedforward NN f_theta(p)
   |
   v
lower-triangular L_theta(p)
   |
   v
P_theta(p)=L_theta(p)L_theta(p)^T + epsilon I
   |
   v
Vhat_theta(x,p)=(x-xs)^T P_theta(p)(x-xs)
```

## Why epsilon I is added

The product <math><msub><mi>L</mi><mi>&theta;</mi></msub><mo>(</mo><mi>p</mi><mo>)</mo><msup><mrow><msub><mi>L</mi><mi>&theta;</mi></msub><mo>(</mo><mi>p</mi><mo>)</mo></mrow><mi>T</mi></msup></math> is always positive semidefinite. That is useful, but it is not enough. If <math><msub><mi>L</mi><mi>&theta;</mi></msub></math> is rank deficient, or if some diagonal entries are zero, the product may have zero eigenvalues. In that case the terminal cost may fail to be strictly positive for nonzero state errors in some directions.

Adding <math><mi>&epsilon;</mi><mi>I</mi></math> shifts every eigenvalue upward by <math><mi>&epsilon;</mi></math>. Therefore,

<math display="block" aria-label="Positive definiteness of the learned terminal matrix">
  <msub><mi>P</mi><mi>&theta;</mi></msub>
  <mo>(</mo><mi>p</mi><mo>)</mo>
  <mo>&succ;</mo>
  <mn>0</mn>
  <mspace width="0.4em"></mspace>
  <mtext>for every parameter </mtext>
  <mi>p</mi><mo>.</mo>
</math>

This is a structural guarantee. It does not depend on the training data being perfect. It follows from the matrix construction itself. Numerically, it also protects the terminal metric from becoming singular or nearly degenerate in directions where the network outputs a weak factor.

## Why it can work

The method can work because it uses offline computation to amortize part of the long-horizon NMPC problem. The expensive long-horizon solves teach the terminal surrogate what future cost may look like, while the online controller solves a much smaller nonlinear program.

There is also a useful inductive bias. Many stabilizing control designs use quadratic Lyapunov-like functions near an equilibrium or steady state. A parameter-dependent positive-definite metric can be interpreted as learning how the local geometry of the terminal cost should change across operating regimes. This is more structured than asking an unconstrained network to output any scalar value.

But the evidence and the guarantee must be separated. The supplied material supports the following reading:

- the positive definiteness of <math><msub><mi>P</mi><mi>&theta;</mi></msub><mo>(</mo><mi>p</mi><mo>)</mo></math> is guaranteed by construction;
- the positive definiteness of <math><msub><mover accent="true"><mi>V</mi><mo>^</mo></mover><mi>&theta;</mi></msub></math> with respect to <math><mi>x</mi><mo>-</mo><msub><mi>x</mi><mi>s</mi></msub></math> is guaranteed by construction;
- exact horizon compression is valid only if the surrogate equals the true continuation value;
- closed-loop NMPC stability still depends on Lyapunov decrease, feasibility, terminal-set logic, or equivalent assumptions.

This distinction is the heart of the note. The paper's strongest idea is the neural network generated Cholesky-type metric. Its weakest unresolved point is that this algebraic positive definiteness is weaker than a closed-loop stability guarantee when approximation error is present.

## Assumptions and limitations

Positive definiteness does not imply Lyapunov decrease. A function can be strictly positive away from the target and still increase along closed-loop trajectories. Therefore, from

<math display="block" aria-label="Positive definiteness of the learned terminal cost">
  <msub><mover accent="true"><mi>V</mi><mo>^</mo></mover><mi>&theta;</mi></msub>
  <mo>(</mo><mi>x</mi><mo>,</mo><mi>p</mi><mo>)</mo>
  <mo>></mo>
  <mn>0</mn>
  <mspace width="0.4em"></mspace>
  <mtext>for </mtext>
  <mi>x</mi><mo>&ne;</mo><msub><mi>x</mi><mi>s</mi></msub>
</math>

one cannot conclude that

<math display="block" aria-label="Desired Lyapunov decrease condition">
  <msub><mover accent="true"><mi>V</mi><mo>^</mo></mover><mi>&theta;</mi></msub>
  <mo>(</mo><msup><mi>x</mi><mo>+</mo></msup><mo>,</mo><msup><mi>p</mi><mo>+</mo></msup><mo>)</mo>
  <mo>-</mo>
  <msub><mover accent="true"><mi>V</mi><mo>^</mo></mover><mi>&theta;</mi></msub>
  <mo>(</mo><mi>x</mi><mo>,</mo><mi>p</mi><mo>)</mo>
  <mo>&le;</mo>
  <mo>-</mo>
  <mi>&alpha;</mi>
  <mo>(</mo><mo>|</mo><mi>x</mi><mo>-</mo><msub><mi>x</mi><mi>s</mi></msub><mo>|</mo><mo>)</mo>
  <mo>.</mo>
</math>

The first statement is a shape property of the terminal cost. The second is a trajectory property of the closed-loop system. They are not equivalent.

Several limitations follow.

- Sampled decrease penalties do not imply global decrease over all states and parameters.
- Offline training coverage does not guarantee behavior outside the training distribution.
- The online optimization problem remains nonlinear when the dynamics are nonlinear.
- Reducing the NLP horizon reduces dimension, but does not remove local optima or numerical failures.
- The quadratic-in-state-error form may be too restrictive for strongly nonquadratic value landscapes.
- Recursive feasibility is not automatically guaranteed by this learned terminal cost.
- Classical terminal sets and Lyapunov ingredients are not fully removed; much of their role is shifted into offline data generation, supervision, and empirical validation.

This is a fair tradeoff, not a fatal flaw. The method is useful precisely because it buys online speed with offline computation and structural bias. The important point is to state what is bought and what remains unpaid.

## Critical assessment: approximation-error critique

The most important missing analysis is approximation-error-aware stability or performance. The clean Bellman-style argument depends on the learned surrogate being exact. In practice, the relevant error is

<math display="block" aria-label="Continuation value approximation error">
  <mo>|</mo>
  <msub><mover accent="true"><mi>V</mi><mo>^</mo></mover><mi>&theta;</mi></msub>
  <mo>(</mo><mi>x</mi><mo>,</mo><mi>p</mi><mo>)</mo>
  <mo>-</mo>
  <msup><mi>V</mi><mo>*</mo></msup>
  <mo>(</mo><mi>x</mi><mo>,</mo><mi>p</mi><mo>)</mo>
  <mo>|</mo><mo>.</mo>
</math>

If this error is nonzero, the one-step controller is no longer solving the exact horizon-compressed problem. A stronger paper would specify what remains true under a bound such as

<math display="block" aria-label="Uniform continuation value approximation error bound">
  <mo>|</mo>
  <msub><mover accent="true"><mi>V</mi><mo>^</mo></mover><mi>&theta;</mi></msub>
  <mo>(</mo><mi>x</mi><mo>,</mo><mi>p</mi><mo>)</mo>
  <mo>-</mo>
  <msup><mi>V</mi><mo>*</mo></msup>
  <mo>(</mo><mi>x</mi><mo>,</mo><mi>p</mi><mo>)</mo>
  <mo>|</mo>
  <mo>&le;</mo>
  <msub><mi>&epsilon;</mi><mi>V</mi></msub>
  <mo>.</mo>
</math>

Here, <math><msub><mi>&epsilon;</mi><mi>V</mi></msub></math> would measure the worst-case value approximation error over a specified domain. Such a result would not automatically give asymptotic stability, but it could support bounded performance degradation if the domain, dynamics, and optimization errors are controlled.

Even more directly, one could ask for a practical Lyapunov decrease statement:

<math display="block" aria-label="Approximate Lyapunov decrease with residual error">
  <msub><mover accent="true"><mi>V</mi><mo>^</mo></mover><mi>&theta;</mi></msub>
  <mo>(</mo><msup><mi>x</mi><mo>+</mo></msup><mo>,</mo><msup><mi>p</mi><mo>+</mo></msup><mo>)</mo>
  <mo>-</mo>
  <msub><mover accent="true"><mi>V</mi><mo>^</mo></mover><mi>&theta;</mi></msub>
  <mo>(</mo><mi>x</mi><mo>,</mo><mi>p</mi><mo>)</mo>
  <mo>&le;</mo>
  <mo>-</mo>
  <mi>&alpha;</mi>
  <mo>(</mo><mo>|</mo><mi>x</mi><mo>-</mo><msub><mi>x</mi><mi>s</mi></msub><mo>|</mo><mo>)</mo>
  <mo>+</mo>
  <msub><mi>&epsilon;</mi><mtext>dec</mtext></msub>
  <mo>.</mo>
</math>

The term <math><msub><mi>&epsilon;</mi><mtext>dec</mtext></msub></math> would represent the residual decrease error. If it is small, the conclusion would likely be practical stability or bounded ultimate behavior, not exact asymptotic convergence. That would be a more honest and useful guarantee for a learned terminal cost.

The supplied material does not establish that such an error-aware theorem is proved. Therefore, the correct reading is conservative: the structure guarantees a positive-definite terminal metric, while closed-loop behavior under approximation error remains a separate analytical question.

## Balanced takeaway

This method is best understood as a data-driven horizon-compression method for NMPC. Its main contribution is not that a neural network appears in the controller. The contribution is the NN-generated Cholesky/Lyapunov metric:

```text
NN predicts a matrix factor, not an arbitrary scalar value.
The factor creates a positive-definite terminal metric.
The metric defines a Lyapunov-compatible quadratic terminal cost.
```

That is a meaningful design choice. It gives the learned terminal cost a control-theoretic shape that generic value approximation lacks.

The limitation is equally clear. Structural positive definiteness is not the same as recursive feasibility, closed-loop Lyapunov decrease, global stability, or exact continuation-value approximation. The method can reduce online computation, but it requires offline long-horizon NMPC solves and inherits the usual risks of function approximation, training distribution mismatch, nonlinear optimization, and feasibility-critical control.

So the right claim is moderate: this is a promising structured surrogate for fast NMPC, especially when long-horizon solutions can be generated offline and the operating domain is well covered. It should not be read as proving that neural networks replace stabilizing MPC design or that global NMPC stability is solved.

<details id="korean-note" class="korean-note-block" lang="ko">
  <summary>한국어 기술 노트 / Korean Technical Note</summary>

  이 글의 핵심은 "신경망 terminal cost"가 아니라 "신경망이 양의 정부호 terminal metric을 생성한다"는 점이다. 네트워크가 스칼라 값함수를 바로 출력하면 값의 부호, 곡률, Lyapunov 형태가 자연스럽게 보장되지 않는다. 반면 이 구조에서는 네트워크가 <math><msub><mi>L</mi><mi>&theta;</mi></msub><mo>(</mo><mi>p</mi><mo>)</mo></math>의 하삼각 성분을 출력하고, <math><msub><mi>P</mi><mi>&theta;</mi></msub><mo>(</mo><mi>p</mi><mo>)</mo><mo>=</mo><msub><mi>L</mi><mi>&theta;</mi></msub><mo>(</mo><mi>p</mi><mo>)</mo><msup><mrow><msub><mi>L</mi><mi>&theta;</mi></msub><mo>(</mo><mi>p</mi><mo>)</mo></mrow><mi>T</mi></msup><mo>+</mo><mi>&epsilon;</mi><mi>I</mi></math>로 terminal matrix를 만든다. 그래서 <math><mi>&epsilon;</mi><mo>></mo><mn>0</mn></math>이면 <math><msub><mi>P</mi><mi>&theta;</mi></msub><mo>(</mo><mi>p</mi><mo>)</mo><mo>&succ;</mo><mn>0</mn></math>가 구조적으로 보장된다.

  하지만 이것이 곧 closed-loop 안정성을 의미하지는 않는다. Lyapunov 함수가 되려면 양의 정부호성뿐 아니라 폐루프 궤적을 따라 감소해야 한다. 즉 <math><msub><mover accent="true"><mi>V</mi><mo>^</mo></mover><mi>&theta;</mi></msub><mo>(</mo><msup><mi>x</mi><mo>+</mo></msup><mo>,</mo><msup><mi>p</mi><mo>+</mo></msup><mo>)</mo><mo>-</mo><msub><mover accent="true"><mi>V</mi><mo>^</mo></mover><mi>&theta;</mi></msub><mo>(</mo><mi>x</mi><mo>,</mo><mi>p</mi><mo>)</mo></math>가 음의 방향으로 제어되는지가 별도로 필요하다. 특히 <math><msub><mover accent="true"><mi>V</mi><mo>^</mo></mover><mi>&theta;</mi></msub></math>와 실제 continuation value <math><msup><mi>V</mi><mo>*</mo></msup></math> 사이의 근사 오차가 있을 때 어떤 practical stability 또는 성능 열화 bound가 남는지 분석해야 한다. 이 부분이 이 접근법의 가장 중요한 미해결 지점이다.
</details>

## References

- Focal paper: bibliographic metadata was not provided in the supplied source material. This note is based on the supplied description of a learned terminal/continuation cost for NMPC using an NN-generated Cholesky-type positive-definite metric.
- References from the focal paper: not provided in the supplied material.
