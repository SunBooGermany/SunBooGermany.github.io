---
layout: post
title: "NN-Generated Lyapunov Metrics for Fast NMPC: What Is Actually Guaranteed?"
title_ko: "빠른 NMPC를 위한 신경망 생성 Lyapunov 메트릭: 실제로 무엇이 보장되는가?"
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
excerpt_ko: "NMPC의 학습 기반 Lyapunov terminal cost를 비판적으로 읽는 글로, Cholesky 구조의 양의 정부호 surrogate, horizon compression, 그리고 approximation error의 미해결 역할을 중심으로 다룬다."
language: "en-ko"
has_korean_note: false
---

## Positioning: why this problem matters in real systems

Nonlinear model predictive control is attractive because it can handle nonlinear dynamics, constraints, changing references, and multi-step tradeoffs in one optimization problem. That is why NMPC appears naturally in chemical process control, robotic motion, autonomous parking, energy storage operation, hydrogen supply chains, and other systems where the controller must reason ahead while respecting physical limits.

The difficulty is timing. At every sampling instant, NMPC solves a nonlinear optimization problem over a finite horizon. A longer horizon usually gives better foresight: the controller can avoid myopic actions, anticipate delayed constraint effects, and approximate stabilizing behavior more reliably. But a long horizon also increases the online nonlinear programming burden.

A short-horizon NMPC controller is faster, but it can be shortsighted. It may choose an action that looks good over one or two steps but makes the later problem difficult, expensive, or infeasible. The central question of this note is therefore practical: can a learned terminal or continuation cost preserve some of the value of a long horizon while allowing a much shorter online horizon?

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

## References

- Focal paper: bibliographic metadata was not provided in the supplied source material. This note is based on the supplied description of a learned terminal/continuation cost for NMPC using an NN-generated Cholesky-type positive-definite metric.
- References from the focal paper: not provided in the supplied material.

<!-- ko -->

## 포지셔닝: 실제 시스템에서 이 문제가 중요한 이유

비선형 모델 예측 제어(NMPC)는 비선형 동역학, 제약조건, 변하는 기준값, 여러 단계에 걸친 비용-제약 tradeoff를 하나의 최적화 문제 안에서 다룰 수 있기 때문에 매력적이다. 그래서 NMPC는 화학공정 제어, 로봇 모션, 자율주차, 에너지 저장장치 운전, 수소 공급망처럼 물리적 한계를 지키면서 미래를 내다봐야 하는 시스템에서 자연스럽게 등장한다.

문제는 시간이다. NMPC는 매 샘플링 시점마다 유한 horizon의 비선형 최적화 문제를 푼다. 긴 horizon은 보통 더 나은 예측성을 준다. 제어기는 근시안적 행동을 피하고, 지연되어 나타나는 제약 효과를 예상하며, 안정화 행동을 더 신뢰성 있게 근사할 수 있다. 그러나 긴 horizon은 온라인 비선형계획 문제의 계산 부담도 키운다.

짧은 horizon의 NMPC는 빠르지만 근시안적일 수 있다. 한두 단계에서는 좋아 보이는 입력이 이후의 문제를 어렵게 만들거나, 비용을 키우거나, 심지어 infeasible하게 만들 수 있다. 따라서 이 글의 핵심 질문은 실용적이다. 학습된 terminal cost 또는 continuation cost가 긴 horizon의 가치를 어느 정도 보존하면서 온라인 horizon을 크게 줄일 수 있는가?

## 문제 설정

이 제어 문제는 parameterized NMPC 문제이다. 상태는 <math><mi>x</mi></math>, 제어입력은 온라인에서 최적화되는 변수이고, <math><mi>p</mi></math>는 reference, 운전 조건, 외생 신호, 또는 정상상태 정보를 담는 parameter vector를 뜻한다. 목표 상태 또는 정상상태 target은 <math><msub><mi>x</mi><mi>s</mi></msub></math>로 쓴다.

긴 horizon의 NMPC는 첫 번째 입력 이후의 미래 비용, 즉 continuation value를 암묵적으로 계산한다. 만약 이 continuation value를 정확히 알고 있다면, 같은 모델링 가정 아래에서 one-step 온라인 문제에 정확한 continuation value를 더하는 것만으로도 긴 horizon 문제의 첫 번째 결정을 재현할 수 있다. 이것이 이 방법의 Bellman-style horizon compression 직관이다.

제공된 자료에서 온라인 horizon은 <math><mi>N</mi><mo>=</mo><mn>1</mn></math>로 설명된다. 빠진 미래 정보는 학습된 terminal/continuation surrogate로 대체된다. 이는 온라인 decision dimension을 줄이지만 비선형 동역학, nonconvexity, local optimum, 수치적 conditioning, feasibility 문제를 제거하지는 않는다. horizon을 압축하는 것이지, NMPC를 단순한 lookup table로 바꾸는 것은 아니다.

## 선행 연구 흐름과 한계

고전적인 안정화 NMPC는 보통 세 가지 terminal ingredient에 의존한다.

- terminal set <math><msub><mi>X</mi><mi>f</mi></msub></math>,
- terminal cost <math><mi>F</mi></math>,
- local stabilizing controller <math><msub><mi>&kappa;</mi><mi>f</mi></msub></math>.

이 요소들은 recursive feasibility와 Lyapunov decrease를 보이는 경로를 제공하지만, 강한 비선형 시스템, 변하는 운전점, 고차원 parameterized task에서는 설계가 어렵다. 긴 horizon의 terminal-constraint-free NMPC는 horizon을 충분히 길게 잡으면 안정화 행동을 회복할 수 있는 경우가 있지만, 그 부담은 온라인 계산으로 이동한다.

Explicit MPC와 neural-network approximate MPC는 policy 또는 optimization map을 근사하여 온라인 계산 비용을 줄인다. 그러나 그 대가로 안정성 및 feasibility 보장의 구조가 약해지는 경우가 많다. 일반적인 learned terminal cost는 value function을 근사할 수 있지만, 임의의 scalar neural network가 자연스럽게 positive definiteness를 보장하거나 Lyapunov 함수처럼 행동하는 것은 아니다.

이 방법이 겨냥하는 간격은 여기에 있다. 온라인 계산에는 유용한 continuation surrogate를 학습하되, terminal cost가 적어도 Lyapunov-compatible metric 형태를 갖도록 충분한 구조를 부여하는 것이다.

## 핵심 아이디어

핵심 아이디어는 data-driven horizon compression이다. 오프라인에서는 긴 horizon의 NMPC 해를 사용해 terminal/continuation surrogate를 지도학습한다. 온라인에서는 훨씬 짧은 NMPC 문제, 잠재적으로 <math><mi>N</mi><mo>=</mo><mn>1</mn></math>인 문제를 풀고, 생략된 미래는 학습된 terminal term에 맡긴다.

정확한 continuation value <math><msup><mi>V</mi><mo>*</mo></msup><mo>(</mo><mi>x</mi><mo>,</mo><mi>p</mi><mo>)</mo></math>를 알고 있다면 one-step decomposition은 개념적으로 깔끔하다.

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

여기서 <math><mi>&ell;</mi></math>은 one-step stage cost이고, <math><msup><mi>x</mi><mo>+</mo></msup></math>는 비선형 동역학이 만드는 다음 상태이며, <math><msup><mi>p</mi><mo>+</mo></msup></math>는 업데이트된 parameter이다. 문제는 <math><msup><mi>V</mi><mo>*</mo></msup></math>를 일반적으로 알 수 없다는 점이다. 따라서 논문은 surrogate를 학습하지만, 특별한 구조를 둔다. neural network가 임의의 scalar cost를 직접 출력하는 것이 아니라 positive-definite terminal matrix를 생성한다.

## 수학적 구조: 핵심 아키텍처

이 아키텍처의 특징은 다음과 같다. feedforward neural network가 <math><mi>p</mi></math>를 입력으로 받고, 행렬 <math><msub><mi>L</mi><mi>&theta;</mi></msub><mo>(</mo><mi>p</mi><mo>)</mo></math>의 lower-triangular entries를 출력한다. terminal matrix는 다음과 같이 구성된다.

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

여기서 <math><msub><mi>L</mi><mi>&theta;</mi></msub><mo>(</mo><mi>p</mi><mo>)</mo></math>는 neural network가 생성한 lower-triangular factor이다. <math><msub><mi>P</mi><mi>&theta;</mi></msub><mo>(</mo><mi>p</mi><mo>)</mo></math>는 학습된 terminal metric이다. <math><mi>&epsilon;</mi><mo>></mo><mn>0</mn></math>는 고정된 양의 regularization constant이고, <math><mi>I</mi></math>는 identity matrix이다.

학습된 terminal/continuation surrogate는 다음과 같다.

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

이 식은 terminal cost가 state error <math><mi>x</mi><mo>-</mo><msub><mi>x</mi><mi>s</mi></msub></math>에 대해 quadratic이며, 그 quadratic metric이 parameter <math><mi>p</mi></math>에 따라 변한다는 뜻이다. 따라서 neural network는 단순히 value function 자체가 아니다. Cholesky-type Lyapunov metric을 생성하는 장치이다.

정보 흐름은 다음처럼 요약할 수 있다.

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

## 왜 epsilon I를 더하는가

곱 <math><msub><mi>L</mi><mi>&theta;</mi></msub><mo>(</mo><mi>p</mi><mo>)</mo><msup><mrow><msub><mi>L</mi><mi>&theta;</mi></msub><mo>(</mo><mi>p</mi><mo>)</mo></mrow><mi>T</mi></msup></math>는 항상 positive semidefinite이다. 이는 유용하지만 충분하지는 않다. <math><msub><mi>L</mi><mi>&theta;</mi></msub></math>가 rank deficient이거나 일부 diagonal entry가 0이면, 이 곱은 0 eigenvalue를 가질 수 있다. 그러면 특정 방향의 nonzero state error에 대해 terminal cost가 strictly positive하지 않을 수 있다.

<math><mi>&epsilon;</mi><mi>I</mi></math>를 더하면 모든 eigenvalue가 <math><mi>&epsilon;</mi></math>만큼 위로 이동한다. 따라서

<math display="block" aria-label="Positive definiteness of the learned terminal matrix">
  <msub><mi>P</mi><mi>&theta;</mi></msub>
  <mo>(</mo><mi>p</mi><mo>)</mo>
  <mo>&succ;</mo>
  <mn>0</mn>
  <mspace width="0.4em"></mspace>
  <mtext>for every parameter </mtext>
  <mi>p</mi><mo>.</mo>
</math>

이는 구조적으로 보장되는 성질이다. training data가 완벽한지 여부에 의존하지 않는다. matrix construction 자체에서 나온다. 수치적으로도 network가 약한 factor를 출력하는 방향에서 terminal metric이 singular하거나 nearly degenerate해지는 것을 막아준다.

## 왜 작동할 수 있는가

이 방법은 긴 horizon NMPC 문제의 일부를 offline computation으로 amortize하기 때문에 작동할 수 있다. 비용이 큰 long-horizon solve가 terminal surrogate에게 미래 비용의 형태를 가르치고, online controller는 훨씬 작은 nonlinear program을 푼다.

또한 유용한 inductive bias가 있다. 많은 안정화 제어 설계는 equilibrium 또는 steady state 근처에서 quadratic Lyapunov-like function을 사용한다. parameter-dependent positive-definite metric은 operating regime에 따라 terminal cost의 local geometry가 어떻게 바뀌어야 하는지를 학습하는 것으로 해석할 수 있다. 이는 unconstrained network에게 아무 scalar value나 출력하라고 하는 것보다 더 구조적이다.

하지만 evidence와 guarantee는 구분되어야 한다. 제공된 자료가 뒷받침하는 해석은 다음과 같다.

- <math><msub><mi>P</mi><mi>&theta;</mi></msub><mo>(</mo><mi>p</mi><mo>)</mo></math>의 positive definiteness는 construction으로 보장된다.
- <math><msub><mover accent="true"><mi>V</mi><mo>^</mo></mover><mi>&theta;</mi></msub></math>가 <math><mi>x</mi><mo>-</mo><msub><mi>x</mi><mi>s</mi></msub></math>에 대해 positive definite라는 점도 construction으로 보장된다.
- exact horizon compression은 surrogate가 true continuation value와 같을 때에만 성립한다.
- closed-loop NMPC stability는 여전히 Lyapunov decrease, feasibility, terminal-set logic, 또는 그에 상응하는 가정에 의존한다.

이 구분이 이 글의 핵심이다. 논문의 가장 강한 아이디어는 neural network generated Cholesky-type metric이다. 가장 약한 미해결 지점은 이러한 algebraic positive definiteness가 approximation error가 존재할 때의 closed-loop stability guarantee보다 훨씬 약하다는 점이다.

## 가정과 한계

Positive definiteness는 Lyapunov decrease를 의미하지 않는다. 어떤 함수가 target 밖에서 strictly positive하더라도 closed-loop trajectory를 따라 증가할 수 있다. 따라서

<math display="block" aria-label="Positive definiteness of the learned terminal cost">
  <msub><mover accent="true"><mi>V</mi><mo>^</mo></mover><mi>&theta;</mi></msub>
  <mo>(</mo><mi>x</mi><mo>,</mo><mi>p</mi><mo>)</mo>
  <mo>></mo>
  <mn>0</mn>
  <mspace width="0.4em"></mspace>
  <mtext>for </mtext>
  <mi>x</mi><mo>&ne;</mo><msub><mi>x</mi><mi>s</mi></msub>
</math>

라는 사실만으로는

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

를 결론낼 수 없다. 첫 번째 문장은 terminal cost의 shape property이다. 두 번째 문장은 closed-loop system의 trajectory property이다. 둘은 같지 않다.

그 결과 몇 가지 한계가 따라온다.

- sampled decrease penalty는 모든 state와 parameter에 대한 global decrease를 의미하지 않는다.
- offline training coverage는 out-of-distribution behavior를 보장하지 않는다.
- dynamics가 nonlinear이면 online optimization problem도 여전히 nonlinear이다.
- NLP horizon을 줄이면 dimension은 줄지만 local optimum이나 numerical failure가 사라지는 것은 아니다.
- state error에 대한 quadratic form은 strongly nonquadratic value landscape를 표현하기에 너무 제한적일 수 있다.
- recursive feasibility는 이 learned terminal cost만으로 자동 보장되지 않는다.
- classical terminal set과 Lyapunov ingredient가 완전히 제거되는 것이 아니라, 그 역할의 상당 부분이 offline data generation, supervision, empirical validation으로 이동한다.

이는 치명적 결함이라기보다 공정한 tradeoff이다. 이 방법은 offline computation과 structural bias를 대가로 online speed를 얻기 때문에 유용하다. 중요한 것은 무엇을 얻었고 무엇이 아직 남아 있는지를 정확히 말하는 것이다.

## 비판적 평가: approximation error 문제

가장 중요한 미해결 분석은 approximation-error-aware stability 또는 performance이다. 깔끔한 Bellman-style argument는 learned surrogate가 정확하다는 데 의존한다. 실제로 중요한 오차는 다음이다.

<math display="block" aria-label="Continuation value approximation error">
  <mo>|</mo>
  <msub><mover accent="true"><mi>V</mi><mo>^</mo></mover><mi>&theta;</mi></msub>
  <mo>(</mo><mi>x</mi><mo>,</mo><mi>p</mi><mo>)</mo>
  <mo>-</mo>
  <msup><mi>V</mi><mo>*</mo></msup>
  <mo>(</mo><mi>x</mi><mo>,</mo><mi>p</mi><mo>)</mo>
  <mo>|</mo><mo>.</mo>
</math>

이 오차가 0이 아니라면 one-step controller는 더 이상 정확한 horizon-compressed problem을 푸는 것이 아니다. 더 강한 논문이라면 다음과 같은 bound 아래에서 무엇이 남는지 명시해야 한다.

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

여기서 <math><msub><mi>&epsilon;</mi><mi>V</mi></msub></math>는 특정 domain에서의 worst-case value approximation error를 뜻한다. 이런 결과가 곧 asymptotic stability를 주지는 않겠지만, domain, dynamics, optimization error가 통제된다면 bounded performance degradation을 논의할 수 있다.

더 직접적으로는 practical Lyapunov decrease statement가 필요할 수 있다.

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

<math><msub><mi>&epsilon;</mi><mtext>dec</mtext></msub></math>는 residual decrease error를 나타낸다. 이것이 작다면 결론은 exact asymptotic convergence가 아니라 practical stability 또는 bounded ultimate behavior에 가까울 것이다. 이는 learned terminal cost에 대해 더 정직하고 유용한 보장이다.

제공된 자료는 이런 error-aware theorem이 증명되었다고 말하지 않는다. 따라서 보수적으로 읽어야 한다. 구조는 positive-definite terminal metric을 보장하지만, approximation error 아래의 closed-loop behavior는 별도의 분석 문제로 남아 있다.

## 균형 잡힌 결론

이 방법은 NMPC를 위한 data-driven horizon-compression method로 이해하는 것이 가장 적절하다. 핵심 기여는 controller 안에 neural network가 들어간다는 사실이 아니다. 핵심은 NN-generated Cholesky/Lyapunov metric이다.

```text
NN predicts a matrix factor, not an arbitrary scalar value.
The factor creates a positive-definite terminal metric.
The metric defines a Lyapunov-compatible quadratic terminal cost.
```

이는 의미 있는 설계 선택이다. generic value approximation에는 없는 control-theoretic shape를 learned terminal cost에 부여한다.

한계도 뚜렷하다. Structural positive definiteness는 recursive feasibility, closed-loop Lyapunov decrease, global stability, 또는 exact continuation-value approximation과 같지 않다. 이 방법은 online computation을 줄일 수 있지만, offline long-horizon NMPC solve가 필요하고 function approximation, training distribution mismatch, nonlinear optimization, feasibility-critical control의 일반적인 위험을 그대로 갖는다.

따라서 올바른 주장은 온건해야 한다. 이 방법은 long-horizon solution을 offline에서 생성할 수 있고 operating domain이 충분히 잘 덮여 있을 때 빠른 NMPC를 위한 promising structured surrogate이다. neural network가 stabilizing MPC design을 대체한다거나 global NMPC stability 문제가 해결되었다고 읽어서는 안 된다.

## 참고문헌

- 대상 논문: 제공된 source material에는 bibliographic metadata가 없었다. 이 글은 NN-generated Cholesky-type positive-definite metric을 사용하는 NMPC용 learned terminal/continuation cost에 대한 제공 설명을 바탕으로 작성되었다.
- 대상 논문의 참고문헌: 제공된 자료에 포함되어 있지 않았다.
