---
layout: post
title: "Interior-Point Method, KKT Condition, and Lagrangian: Why Barrier Methods Look Like Perturbed KKT Conditions"
title_ko: "내점법, KKT 조건, 라그랑지안: 배리어 방법이 교란된 KKT 조건처럼 보이는 이유"
date: 2026-06-02
category: stochastic-nonlinear-optimization
category_label: "Stochastic & Nonlinear Optimization"
research_group: algorithmic_reviews
research_category: stochastic-nonlinear-optimization
research_category_label: "Stochastic & Nonlinear Optimization"
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
  - interior-point-method
  - kkt-conditions
  - lagrangian
  - barrier-methods
  - constrained-optimization
excerpt: "A conceptual note explaining how log-barrier interior-point methods can be read as a path of perturbed KKT systems whose complementarity residual vanishes."
excerpt_ko: "로그 배리어 내점법을 상보성 잔차가 사라지는 교란된 KKT 시스템의 경로로 이해하는 개념 노트."
language: "en-ko"
has_korean_note: false
---

## Positioning

Constrained optimization is often introduced through the Karush-Kuhn-Tucker (KKT) conditions. At first, KKT conditions can feel like a collection of algebraic rules: primal feasibility, dual feasibility, stationarity, and complementary slackness. However, these conditions have a clear geometric meaning. They describe the point at which the objective wants to improve further, but the feasible region blocks every improving direction.

Interior-point methods (IPMs) can be understood as a numerical strategy for reaching such a KKT point without explicitly guessing which constraints will be active. The key idea is to stay strictly inside the feasible region and gradually move toward the boundary only when the true optimum requires it.

## Problem setting

Consider the constrained optimization problem

<math display="block" aria-label="Constrained optimization problem">
  <munder>
    <mi>min</mi>
    <mi>x</mi>
  </munder>
  <mspace width="0.4em"></mspace>
  <msub><mi>f</mi><mn>0</mn></msub>
  <mo>(</mo><mi>x</mi><mo>)</mo>
</math>

subject to

<math display="block" aria-label="Inequality and equality constraints">
  <msub><mi>f</mi><mi>i</mi></msub>
  <mo>(</mo><mi>x</mi><mo>)</mo>
  <mo>&le;</mo>
  <mn>0</mn>
  <mo>,</mo>
  <mspace width="0.4em"></mspace>
  <mi>i</mi>
  <mo>=</mo>
  <mn>1</mn>
  <mo>,</mo>
  <mo>&hellip;</mo>
  <mo>,</mo>
  <mi>m</mi>
  <mo>,</mo>
  <mspace width="1em"></mspace>
  <mi>A</mi><mi>x</mi>
  <mo>=</mo>
  <mi>b</mi>
  <mo>.</mo>
</math>

Here, <math><msub><mi>f</mi><mn>0</mn></msub><mo>(</mo><mi>x</mi><mo>)</mo></math> is the objective function, <math><msub><mi>f</mi><mi>i</mi></msub><mo>(</mo><mi>x</mi><mo>)</mo><mo>&le;</mo><mn>0</mn></math> are inequality constraints, and <math><mi>A</mi><mi>x</mi><mo>=</mo><mi>b</mi></math> represents equality constraints.

The Lagrangian is

<math display="block" aria-label="Lagrangian of constrained optimization problem">
  <mi mathvariant="script">L</mi>
  <mo>(</mo><mi>x</mi><mo>,</mo><mi>&lambda;</mi><mo>,</mo><mi>&nu;</mi><mo>)</mo>
  <mo>=</mo>
  <msub><mi>f</mi><mn>0</mn></msub>
  <mo>(</mo><mi>x</mi><mo>)</mo>
  <mo>+</mo>
  <munderover>
    <mo>&sum;</mo>
    <mrow><mi>i</mi><mo>=</mo><mn>1</mn></mrow>
    <mi>m</mi>
  </munderover>
  <msub><mi>&lambda;</mi><mi>i</mi></msub>
  <msub><mi>f</mi><mi>i</mi></msub>
  <mo>(</mo><mi>x</mi><mo>)</mo>
  <mo>+</mo>
  <msup><mi>&nu;</mi><mi>T</mi></msup>
  <mo>(</mo><mi>A</mi><mi>x</mi><mo>-</mo><mi>b</mi><mo>)</mo>
  <mo>.</mo>
</math>

The multipliers <math><msub><mi>&lambda;</mi><mi>i</mi></msub><mo>&ge;</mo><mn>0</mn></math> correspond to inequality constraints, while <math><mi>&nu;</mi></math> corresponds to equality constraints.

## Prior research gap

The KKT conditions are

<math display="block" aria-label="KKT conditions">
  <mtable>
    <mtr>
      <mtd>
        <msub><mi>f</mi><mi>i</mi></msub>
        <mo>(</mo><msup><mi>x</mi><mo>*</mo></msup><mo>)</mo>
        <mo>&le;</mo>
        <mn>0</mn>
        <mo>,</mo>
        <mspace width="0.6em"></mspace>
        <mi>A</mi><msup><mi>x</mi><mo>*</mo></msup>
        <mo>=</mo>
        <mi>b</mi>
        <mo>,</mo>
      </mtd>
    </mtr>
    <mtr>
      <mtd>
        <msubsup><mi>&lambda;</mi><mi>i</mi><mo>*</mo></msubsup>
        <mo>&ge;</mo>
        <mn>0</mn>
        <mo>,</mo>
      </mtd>
    </mtr>
    <mtr>
      <mtd>
        <msubsup><mi>&lambda;</mi><mi>i</mi><mo>*</mo></msubsup>
        <msub><mi>f</mi><mi>i</mi></msub>
        <mo>(</mo><msup><mi>x</mi><mo>*</mo></msup><mo>)</mo>
        <mo>=</mo>
        <mn>0</mn>
        <mo>,</mo>
        <mspace width="0.4em"></mspace>
        <mi>i</mi>
        <mo>=</mo>
        <mn>1</mn>
        <mo>,</mo>
        <mo>&hellip;</mo>
        <mo>,</mo>
        <mi>m</mi>
        <mo>,</mo>
      </mtd>
    </mtr>
    <mtr>
      <mtd>
        <mi>&nabla;</mi><msub><mi>f</mi><mn>0</mn></msub>
        <mo>(</mo><msup><mi>x</mi><mo>*</mo></msup><mo>)</mo>
        <mo>+</mo>
        <munderover>
          <mo>&sum;</mo>
          <mrow><mi>i</mi><mo>=</mo><mn>1</mn></mrow>
          <mi>m</mi>
        </munderover>
        <msubsup><mi>&lambda;</mi><mi>i</mi><mo>*</mo></msubsup>
        <mi>&nabla;</mi><msub><mi>f</mi><mi>i</mi></msub>
        <mo>(</mo><msup><mi>x</mi><mo>*</mo></msup><mo>)</mo>
        <mo>+</mo>
        <msup><mi>A</mi><mi>T</mi></msup>
        <msup><mi>&nu;</mi><mo>*</mo></msup>
        <mo>=</mo>
        <mn>0</mn>
        <mo>.</mo>
      </mtd>
    </mtr>
  </mtable>
</math>

Among these, the most unintuitive one is often complementary slackness:

<math display="block" aria-label="Complementary slackness condition">
  <msubsup><mi>&lambda;</mi><mi>i</mi><mo>*</mo></msubsup>
  <msub><mi>f</mi><mi>i</mi></msub>
  <mo>(</mo><msup><mi>x</mi><mo>*</mo></msup><mo>)</mo>
  <mo>=</mo>
  <mn>0</mn>
  <mo>.</mo>
</math>

Because <math><msub><mi>f</mi><mi>i</mi></msub><mo>(</mo><msup><mi>x</mi><mo>*</mo></msup><mo>)</mo><mo>&le;</mo><mn>0</mn></math> and <math><msubsup><mi>&lambda;</mi><mi>i</mi><mo>*</mo></msubsup><mo>&ge;</mo><mn>0</mn></math>, this condition means that each inequality constraint must fall into one of two cases.

If the constraint is inactive, <math><msub><mi>f</mi><mi>i</mi></msub><mo>(</mo><msup><mi>x</mi><mo>*</mo></msup><mo>)</mo><mo>&lt;</mo><mn>0</mn></math>. Then the solution is strictly inside that constraint. The constraint has slack. It does not restrict the optimum. Therefore, <math><msubsup><mi>&lambda;</mi><mi>i</mi><mo>*</mo></msubsup><mo>=</mo><mn>0</mn></math>.

If the constraint is active, <math><msub><mi>f</mi><mi>i</mi></msub><mo>(</mo><msup><mi>x</mi><mo>*</mo></msup><mo>)</mo><mo>=</mo><mn>0</mn></math>. Then the optimum lies on the boundary of that constraint. In this case, <math><msubsup><mi>&lambda;</mi><mi>i</mi><mo>*</mo></msubsup></math> can be positive. A positive multiplier means that the constraint is actually preventing the objective from improving further.

This is the economic interpretation of Lagrange multipliers: <math><msubsup><mi>&lambda;</mi><mi>i</mi><mo>*</mo></msubsup></math> is the shadow price of constraint <math><mi>i</mi></math>. If relaxing the constraint slightly would improve the objective, then that constraint has positive marginal value. If the constraint is not binding, relaxing it changes nothing, so its shadow price is zero.

Geometrically, the stationarity condition means that the gradient of the objective is balanced by the normal vectors of the active constraints. The objective may still want to move in some direction, but the feasible region blocks that movement. The active constraints provide the opposing force.

## Core idea

This is where interior-point methods enter.

Instead of directly solving the constrained problem, a log-barrier IPM solves a sequence of unconstrained or equality-constrained problems:

<math display="block" aria-label="Log-barrier interior-point problem">
  <munder>
    <mi>min</mi>
    <mi>x</mi>
  </munder>
  <mspace width="0.4em"></mspace>
  <msub><mi>f</mi><mn>0</mn></msub>
  <mo>(</mo><mi>x</mi><mo>)</mo>
  <mo>-</mo>
  <mfrac>
    <mn>1</mn>
    <mi>t</mi>
  </mfrac>
  <munderover>
    <mo>&sum;</mo>
    <mrow><mi>i</mi><mo>=</mo><mn>1</mn></mrow>
    <mi>m</mi>
  </munderover>
  <mi>log</mi>
  <mo>(</mo><mo>-</mo><msub><mi>f</mi><mi>i</mi></msub><mo>(</mo><mi>x</mi><mo>)</mo><mo>)</mo>
</math>

subject to <math><mi>A</mi><mi>x</mi><mo>=</mo><mi>b</mi></math>.

The logarithmic barrier is defined only when <math><msub><mi>f</mi><mi>i</mi></msub><mo>(</mo><mi>x</mi><mo>)</mo><mo>&lt;</mo><mn>0</mn></math>. Therefore, the method stays strictly inside the feasible region. If <math><mi>x</mi></math> approaches the boundary <math><msub><mi>f</mi><mi>i</mi></msub><mo>(</mo><mi>x</mi><mo>)</mo><mo>=</mo><mn>0</mn></math>, then <math><mo>-</mo><mi>log</mi><mo>(</mo><mo>-</mo><msub><mi>f</mi><mi>i</mi></msub><mo>(</mo><mi>x</mi><mo>)</mo><mo>)</mo></math> becomes very large. The barrier prevents the iterate from hitting or crossing the constraint boundary.

The parameter <math><mi>t</mi><mo>></mo><mn>0</mn></math> controls the strength of the barrier. When <math><mi>t</mi></math> is small, <math><mn>1</mn><mo>/</mo><mi>t</mi></math> is large, so the barrier is strong. The solution stays well inside the feasible region. When <math><mi>t</mi></math> becomes large, <math><mn>1</mn><mo>/</mo><mi>t</mi></math> becomes small, so the barrier weakens. The solution is then allowed to approach the boundary if doing so improves the original objective.

## Mathematical structure

The stationarity condition of the barrier problem is

<math display="block" aria-label="Stationarity of the barrier problem">
  <mi>&nabla;</mi><msub><mi>f</mi><mn>0</mn></msub>
  <mo>(</mo><mi>x</mi><mo>)</mo>
  <mo>-</mo>
  <mfrac>
    <mn>1</mn>
    <mi>t</mi>
  </mfrac>
  <munderover>
    <mo>&sum;</mo>
    <mrow><mi>i</mi><mo>=</mo><mn>1</mn></mrow>
    <mi>m</mi>
  </munderover>
  <mfrac>
    <mn>1</mn>
    <mrow><msub><mi>f</mi><mi>i</mi></msub><mo>(</mo><mi>x</mi><mo>)</mo></mrow>
  </mfrac>
  <mi>&nabla;</mi><msub><mi>f</mi><mi>i</mi></msub>
  <mo>(</mo><mi>x</mi><mo>)</mo>
  <mo>+</mo>
  <msup><mi>A</mi><mi>T</mi></msup>
  <mi>&nu;</mi>
  <mo>=</mo>
  <mn>0</mn>
  <mo>.</mo>
</math>

This expression can be rewritten in a form that resembles the KKT stationarity condition by defining

<math display="block" aria-label="Interior-point multiplier definition">
  <msub><mi>&lambda;</mi><mi>i</mi></msub>
  <mo>=</mo>
  <mo>-</mo>
  <mfrac>
    <mn>1</mn>
    <mrow><mi>t</mi><msub><mi>f</mi><mi>i</mi></msub><mo>(</mo><mi>x</mi><mo>)</mo></mrow>
  </mfrac>
  <mo>.</mo>
</math>

Since the interior-point solution satisfies <math><msub><mi>f</mi><mi>i</mi></msub><mo>(</mo><mi>x</mi><mo>)</mo><mo>&lt;</mo><mn>0</mn></math>, this gives <math><msub><mi>&lambda;</mi><mi>i</mi></msub><mo>></mo><mn>0</mn></math>.

Substituting this definition into the stationarity condition gives

<math display="block" aria-label="KKT-form stationarity from barrier problem">
  <mi>&nabla;</mi><msub><mi>f</mi><mn>0</mn></msub>
  <mo>(</mo><mi>x</mi><mo>)</mo>
  <mo>+</mo>
  <munderover>
    <mo>&sum;</mo>
    <mrow><mi>i</mi><mo>=</mo><mn>1</mn></mrow>
    <mi>m</mi>
  </munderover>
  <msub><mi>&lambda;</mi><mi>i</mi></msub>
  <mi>&nabla;</mi><msub><mi>f</mi><mi>i</mi></msub>
  <mo>(</mo><mi>x</mi><mo>)</mo>
  <mo>+</mo>
  <msup><mi>A</mi><mi>T</mi></msup>
  <mi>&nu;</mi>
  <mo>=</mo>
  <mn>0</mn>
  <mo>.</mo>
</math>

This is exactly the same form as the KKT stationarity condition. The difference appears in complementary slackness. From the multiplier definition, we obtain

<math display="block" aria-label="Perturbed complementarity in original inequality form">
  <mo>-</mo>
  <msub><mi>&lambda;</mi><mi>i</mi></msub>
  <msub><mi>f</mi><mi>i</mi></msub>
  <mo>(</mo><mi>x</mi><mo>)</mo>
  <mo>=</mo>
  <mfrac>
    <mn>1</mn>
    <mi>t</mi>
  </mfrac>
  <mo>.</mo>
</math>

If we define the slack variable <math><msub><mi>s</mi><mi>i</mi></msub><mo>=</mo><mo>-</mo><msub><mi>f</mi><mi>i</mi></msub><mo>(</mo><mi>x</mi><mo>)</mo><mo>></mo><mn>0</mn></math>, then this becomes

<math display="block" aria-label="Perturbed complementarity with slack variable">
  <msub><mi>&lambda;</mi><mi>i</mi></msub>
  <msub><mi>s</mi><mi>i</mi></msub>
  <mo>=</mo>
  <mfrac>
    <mn>1</mn>
    <mi>t</mi>
  </mfrac>
  <mo>.</mo>
</math>

This is the central idea of IPM:

<math display="block" aria-label="Central path complementarity">
  <msub><mi>&lambda;</mi><mi>i</mi></msub>
  <msub><mi>s</mi><mi>i</mi></msub>
  <mo>=</mo>
  <mi>&mu;</mi>
  <mo>,</mo>
  <mspace width="0.8em"></mspace>
  <mi>&mu;</mi>
  <mo>=</mo>
  <mfrac>
    <mn>1</mn>
    <mi>t</mi>
  </mfrac>
  <mo>.</mo>
</math>

The original KKT condition requires <math><msub><mi>&lambda;</mi><mi>i</mi></msub><msub><mi>s</mi><mi>i</mi></msub><mo>=</mo><mn>0</mn></math>. The interior-point method instead follows a perturbed version, <math><msub><mi>&lambda;</mi><mi>i</mi></msub><msub><mi>s</mi><mi>i</mi></msub><mo>=</mo><mi>&mu;</mi><mo>></mo><mn>0</mn></math>. As <math><mi>&mu;</mi><mo>&downarrow;</mo><mn>0</mn></math>, the perturbed condition approaches the exact KKT complementary slackness condition.

## Why it can work

This gives a useful interpretation of the central path. IPM does not initially decide which constraints are active and which are inactive. Instead, every inequality constraint has positive slack <math><msub><mi>s</mi><mi>i</mi></msub><mo>></mo><mn>0</mn></math> and positive multiplier <math><msub><mi>&lambda;</mi><mi>i</mi></msub><mo>></mo><mn>0</mn></math>, satisfying <math><msub><mi>&lambda;</mi><mi>i</mi></msub><msub><mi>s</mi><mi>i</mi></msub><mo>=</mo><mi>&mu;</mi></math>.

As <math><mi>&mu;</mi></math> decreases, the solution approaches the KKT point. For constraints that become active at the optimum, the slack <math><msub><mi>s</mi><mi>i</mi></msub></math> goes to zero while <math><msub><mi>&lambda;</mi><mi>i</mi></msub></math> may remain positive. For inactive constraints, the slack remains positive while <math><msub><mi>&lambda;</mi><mi>i</mi></msub></math> goes to zero.

Therefore, IPM gradually discovers the active set implicitly.

## Assumptions and limitations

A common misunderstanding is to say that IPM first satisfies constraints more strictly and then gradually relaxes them. This is not quite correct. The inequality constraints are not relaxed. In fact, the method maintains <math><msub><mi>f</mi><mi>i</mi></msub><mo>(</mo><mi>x</mi><mo>)</mo><mo>&lt;</mo><mn>0</mn></math> throughout the interior path.

What is relaxed is not primal feasibility, but complementary slackness.

At the beginning, <math><mi>&mu;</mi></math> is relatively large, so <math><msub><mi>&lambda;</mi><mi>i</mi></msub><msub><mi>s</mi><mi>i</mi></msub><mo>=</mo><mi>&mu;</mi></math> is far from the exact KKT condition <math><msub><mi>&lambda;</mi><mi>i</mi></msub><msub><mi>s</mi><mi>i</mi></msub><mo>=</mo><mn>0</mn></math>. As the algorithm proceeds, <math><mi>&mu;</mi></math> becomes smaller. The solution then satisfies complementary slackness more accurately and moves closer to the true constrained optimum.

So the correct intuition is this: the method keeps the iterate strictly feasible, starts with a strong barrier that avoids the boundary, and gradually weakens the barrier so that the solution can approach the boundary if the optimum lies there. During this process, it follows a perturbed KKT system whose perturbation vanishes as <math><mi>&mu;</mi><mo>&rarr;</mo><mn>0</mn></math>.

## Critical assessment

This is why IPM is deeply connected to KKT conditions. It is not merely a heuristic barrier method. It can be seen as a systematic way of solving a sequence of perturbed KKT systems:

<math display="block" aria-label="Perturbed KKT system followed by an interior-point method">
  <mtable>
    <mtr>
      <mtd>
        <msub><mi>f</mi><mi>i</mi></msub>
        <mo>(</mo><mi>x</mi><mo>)</mo>
        <mo>&lt;</mo>
        <mn>0</mn>
        <mo>,</mo>
      </mtd>
    </mtr>
    <mtr>
      <mtd>
        <msub><mi>&lambda;</mi><mi>i</mi></msub>
        <mo>></mo>
        <mn>0</mn>
        <mo>,</mo>
      </mtd>
    </mtr>
    <mtr>
      <mtd>
        <msub><mi>&lambda;</mi><mi>i</mi></msub>
        <msub><mi>s</mi><mi>i</mi></msub>
        <mo>=</mo>
        <mi>&mu;</mi>
        <mo>,</mo>
      </mtd>
    </mtr>
    <mtr>
      <mtd>
        <mi>&nabla;</mi><msub><mi>f</mi><mn>0</mn></msub>
        <mo>(</mo><mi>x</mi><mo>)</mo>
        <mo>+</mo>
        <munderover>
          <mo>&sum;</mo>
          <mrow><mi>i</mi><mo>=</mo><mn>1</mn></mrow>
          <mi>m</mi>
        </munderover>
        <msub><mi>&lambda;</mi><mi>i</mi></msub>
        <mi>&nabla;</mi><msub><mi>f</mi><mi>i</mi></msub>
        <mo>(</mo><mi>x</mi><mo>)</mo>
        <mo>+</mo>
        <msup><mi>A</mi><mi>T</mi></msup>
        <mi>&nu;</mi>
        <mo>=</mo>
        <mn>0</mn>
        <mo>,</mo>
      </mtd>
    </mtr>
    <mtr>
      <mtd>
        <mi>A</mi><mi>x</mi>
        <mo>=</mo>
        <mi>b</mi>
        <mo>.</mo>
      </mtd>
    </mtr>
  </mtable>
</math>

As <math><mi>&mu;</mi><mo>&downarrow;</mo><mn>0</mn></math>, this system converges to the original KKT system.

The Lagrangian explains the force balance at the optimum. The KKT conditions describe the exact optimality structure. The interior-point method provides a computational path toward that structure by replacing exact complementary slackness with a smooth, positive perturbation.

In short:

<math display="block" aria-label="Relationship between Lagrangian KKT and IPM">
  <mtable>
    <mtr>
      <mtd>
        <mtext>Lagrangian</mtext>
        <mspace width="0.5em"></mspace>
        <mo>&rArr;</mo>
        <mspace width="0.5em"></mspace>
        <mtext>stationarity and multipliers</mtext>
      </mtd>
    </mtr>
    <mtr>
      <mtd>
        <mtext>KKT conditions</mtext>
        <mspace width="0.5em"></mspace>
        <mo>&rArr;</mo>
        <mspace width="0.5em"></mspace>
        <mtext>exact constrained optimality</mtext>
      </mtd>
    </mtr>
    <mtr>
      <mtd>
        <mtext>IPM</mtext>
        <mspace width="0.5em"></mspace>
        <mo>&rArr;</mo>
        <mspace width="0.5em"></mspace>
        <mtext>perturbed KKT path approaching exact KKT</mtext>
      </mtd>
    </mtr>
  </mtable>
</math>

This is the cleanest way to understand the relationship between IPM, KKT conditions, and the Lagrangian.

## References

- Focal paper: not applicable. This is a conceptual research note based on the supplied text.
- References from the focal paper: not applicable.

<!-- ko -->

## 포지셔닝

제약 최적화는 보통 Karush-Kuhn-Tucker(KKT) 조건을 통해 처음 소개된다. 처음에는 KKT 조건이 primal feasibility, dual feasibility, stationarity, complementary slackness라는 대수적 규칙들의 묶음처럼 느껴질 수 있다. 그러나 이 조건들은 분명한 기하학적 의미를 갖는다. 목적함수는 더 개선되고 싶지만 feasible region이 모든 개선 방향을 막는 지점을 설명한다.

내점법(interior-point method, IPM)은 어떤 제약이 active가 될지 명시적으로 추측하지 않고도 그런 KKT 지점에 도달하기 위한 수치적 전략으로 이해할 수 있다. 핵심 아이디어는 feasible region의 내부에 엄격히 머무르면서, 진짜 최적해가 필요로 할 때에만 점진적으로 경계에 가까워지는 것이다.

## 문제 설정

다음 제약 최적화 문제를 생각하자.

<math display="block" aria-label="Constrained optimization problem">
  <munder>
    <mi>min</mi>
    <mi>x</mi>
  </munder>
  <mspace width="0.4em"></mspace>
  <msub><mi>f</mi><mn>0</mn></msub>
  <mo>(</mo><mi>x</mi><mo>)</mo>
</math>

제약조건은 다음과 같다.

<math display="block" aria-label="Inequality and equality constraints">
  <msub><mi>f</mi><mi>i</mi></msub>
  <mo>(</mo><mi>x</mi><mo>)</mo>
  <mo>&le;</mo>
  <mn>0</mn>
  <mo>,</mo>
  <mspace width="0.4em"></mspace>
  <mi>i</mi>
  <mo>=</mo>
  <mn>1</mn>
  <mo>,</mo>
  <mo>&hellip;</mo>
  <mo>,</mo>
  <mi>m</mi>
  <mo>,</mo>
  <mspace width="1em"></mspace>
  <mi>A</mi><mi>x</mi>
  <mo>=</mo>
  <mi>b</mi>
  <mo>.</mo>
</math>

여기서 <math><msub><mi>f</mi><mn>0</mn></msub><mo>(</mo><mi>x</mi><mo>)</mo></math>는 목적함수이고, <math><msub><mi>f</mi><mi>i</mi></msub><mo>(</mo><mi>x</mi><mo>)</mo><mo>&le;</mo><mn>0</mn></math>는 부등식 제약조건이며, <math><mi>A</mi><mi>x</mi><mo>=</mo><mi>b</mi></math>는 등식 제약조건을 나타낸다.

라그랑지안은 다음과 같다.

<math display="block" aria-label="Lagrangian of constrained optimization problem">
  <mi mathvariant="script">L</mi>
  <mo>(</mo><mi>x</mi><mo>,</mo><mi>&lambda;</mi><mo>,</mo><mi>&nu;</mi><mo>)</mo>
  <mo>=</mo>
  <msub><mi>f</mi><mn>0</mn></msub>
  <mo>(</mo><mi>x</mi><mo>)</mo>
  <mo>+</mo>
  <munderover>
    <mo>&sum;</mo>
    <mrow><mi>i</mi><mo>=</mo><mn>1</mn></mrow>
    <mi>m</mi>
  </munderover>
  <msub><mi>&lambda;</mi><mi>i</mi></msub>
  <msub><mi>f</mi><mi>i</mi></msub>
  <mo>(</mo><mi>x</mi><mo>)</mo>
  <mo>+</mo>
  <msup><mi>&nu;</mi><mi>T</mi></msup>
  <mo>(</mo><mi>A</mi><mi>x</mi><mo>-</mo><mi>b</mi><mo>)</mo>
  <mo>.</mo>
</math>

승수 <math><msub><mi>&lambda;</mi><mi>i</mi></msub><mo>&ge;</mo><mn>0</mn></math>는 부등식 제약조건에 대응하고, <math><mi>&nu;</mi></math>는 등식 제약조건에 대응한다.

## 선행 연구 공백

KKT 조건은 다음과 같다.

<math display="block" aria-label="KKT conditions">
  <mtable>
    <mtr>
      <mtd>
        <msub><mi>f</mi><mi>i</mi></msub>
        <mo>(</mo><msup><mi>x</mi><mo>*</mo></msup><mo>)</mo>
        <mo>&le;</mo>
        <mn>0</mn>
        <mo>,</mo>
        <mspace width="0.6em"></mspace>
        <mi>A</mi><msup><mi>x</mi><mo>*</mo></msup>
        <mo>=</mo>
        <mi>b</mi>
        <mo>,</mo>
      </mtd>
    </mtr>
    <mtr>
      <mtd>
        <msubsup><mi>&lambda;</mi><mi>i</mi><mo>*</mo></msubsup>
        <mo>&ge;</mo>
        <mn>0</mn>
        <mo>,</mo>
      </mtd>
    </mtr>
    <mtr>
      <mtd>
        <msubsup><mi>&lambda;</mi><mi>i</mi><mo>*</mo></msubsup>
        <msub><mi>f</mi><mi>i</mi></msub>
        <mo>(</mo><msup><mi>x</mi><mo>*</mo></msup><mo>)</mo>
        <mo>=</mo>
        <mn>0</mn>
        <mo>,</mo>
        <mspace width="0.4em"></mspace>
        <mi>i</mi>
        <mo>=</mo>
        <mn>1</mn>
        <mo>,</mo>
        <mo>&hellip;</mo>
        <mo>,</mo>
        <mi>m</mi>
        <mo>,</mo>
      </mtd>
    </mtr>
    <mtr>
      <mtd>
        <mi>&nabla;</mi><msub><mi>f</mi><mn>0</mn></msub>
        <mo>(</mo><msup><mi>x</mi><mo>*</mo></msup><mo>)</mo>
        <mo>+</mo>
        <munderover>
          <mo>&sum;</mo>
          <mrow><mi>i</mi><mo>=</mo><mn>1</mn></mrow>
          <mi>m</mi>
        </munderover>
        <msubsup><mi>&lambda;</mi><mi>i</mi><mo>*</mo></msubsup>
        <mi>&nabla;</mi><msub><mi>f</mi><mi>i</mi></msub>
        <mo>(</mo><msup><mi>x</mi><mo>*</mo></msup><mo>)</mo>
        <mo>+</mo>
        <msup><mi>A</mi><mi>T</mi></msup>
        <msup><mi>&nu;</mi><mo>*</mo></msup>
        <mo>=</mo>
        <mn>0</mn>
        <mo>.</mo>
      </mtd>
    </mtr>
  </mtable>
</math>

이 중 가장 직관적이지 않은 조건은 대개 complementary slackness이다.

<math display="block" aria-label="Complementary slackness condition">
  <msubsup><mi>&lambda;</mi><mi>i</mi><mo>*</mo></msubsup>
  <msub><mi>f</mi><mi>i</mi></msub>
  <mo>(</mo><msup><mi>x</mi><mo>*</mo></msup><mo>)</mo>
  <mo>=</mo>
  <mn>0</mn>
  <mo>.</mo>
</math>

<math><msub><mi>f</mi><mi>i</mi></msub><mo>(</mo><msup><mi>x</mi><mo>*</mo></msup><mo>)</mo><mo>&le;</mo><mn>0</mn></math>이고 <math><msubsup><mi>&lambda;</mi><mi>i</mi><mo>*</mo></msubsup><mo>&ge;</mo><mn>0</mn></math>이므로, 이 조건은 각 부등식 제약조건이 두 경우 중 하나에 속해야 함을 뜻한다.

제약조건이 inactive라면 <math><msub><mi>f</mi><mi>i</mi></msub><mo>(</mo><msup><mi>x</mi><mo>*</mo></msup><mo>)</mo><mo>&lt;</mo><mn>0</mn></math>이다. 그러면 해는 그 제약조건의 내부에 엄격히 놓여 있다. 제약에는 여유가 있고, 최적해를 제한하지 않는다. 따라서 <math><msubsup><mi>&lambda;</mi><mi>i</mi><mo>*</mo></msubsup><mo>=</mo><mn>0</mn></math>이다.

제약조건이 active라면 <math><msub><mi>f</mi><mi>i</mi></msub><mo>(</mo><msup><mi>x</mi><mo>*</mo></msup><mo>)</mo><mo>=</mo><mn>0</mn></math>이다. 그러면 최적해는 그 제약조건의 경계 위에 있다. 이 경우 <math><msubsup><mi>&lambda;</mi><mi>i</mi><mo>*</mo></msubsup></math>는 양수일 수 있다. 양의 승수는 해당 제약조건이 실제로 목적함수의 추가 개선을 막고 있음을 뜻한다.

이것이 라그랑주 승수의 경제적 해석이다. <math><msubsup><mi>&lambda;</mi><mi>i</mi><mo>*</mo></msubsup></math>는 제약조건 <math><mi>i</mi></math>의 shadow price이다. 제약조건을 조금 완화했을 때 목적함수가 개선된다면, 그 제약조건은 양의 한계 가치를 가진다. 제약조건이 binding이 아니라면 완화해도 아무것도 바뀌지 않으므로 shadow price는 0이다.

기하학적으로 stationarity 조건은 목적함수의 gradient가 active constraint들의 normal vector에 의해 균형을 이룬다는 뜻이다. 목적함수는 여전히 어떤 방향으로 움직이고 싶을 수 있지만, feasible region이 그 움직임을 막는다. active constraint들이 반대 힘을 제공한다.

## 핵심 아이디어

여기에서 내점법이 등장한다.

제약 문제를 직접 푸는 대신, 로그 배리어 IPM은 다음과 같은 비제약 또는 등식 제약 문제의 sequence를 푼다.

<math display="block" aria-label="Log-barrier interior-point problem">
  <munder>
    <mi>min</mi>
    <mi>x</mi>
  </munder>
  <mspace width="0.4em"></mspace>
  <msub><mi>f</mi><mn>0</mn></msub>
  <mo>(</mo><mi>x</mi><mo>)</mo>
  <mo>-</mo>
  <mfrac>
    <mn>1</mn>
    <mi>t</mi>
  </mfrac>
  <munderover>
    <mo>&sum;</mo>
    <mrow><mi>i</mi><mo>=</mo><mn>1</mn></mrow>
    <mi>m</mi>
  </munderover>
  <mi>log</mi>
  <mo>(</mo><mo>-</mo><msub><mi>f</mi><mi>i</mi></msub><mo>(</mo><mi>x</mi><mo>)</mo><mo>)</mo>
</math>

subject to <math><mi>A</mi><mi>x</mi><mo>=</mo><mi>b</mi></math>.

로그 배리어는 <math><msub><mi>f</mi><mi>i</mi></msub><mo>(</mo><mi>x</mi><mo>)</mo><mo>&lt;</mo><mn>0</mn></math>일 때만 정의된다. 따라서 이 방법은 feasible region의 내부에 엄격히 머문다. <math><mi>x</mi></math>가 경계 <math><msub><mi>f</mi><mi>i</mi></msub><mo>(</mo><mi>x</mi><mo>)</mo><mo>=</mo><mn>0</mn></math>에 가까워지면 <math><mo>-</mo><mi>log</mi><mo>(</mo><mo>-</mo><msub><mi>f</mi><mi>i</mi></msub><mo>(</mo><mi>x</mi><mo>)</mo><mo>)</mo></math>가 매우 커진다. 배리어는 iterate가 제약 경계에 닿거나 이를 넘어가는 것을 막는다.

파라미터 <math><mi>t</mi><mo>></mo><mn>0</mn></math>는 배리어의 강도를 조절한다. <math><mi>t</mi></math>가 작으면 <math><mn>1</mn><mo>/</mo><mi>t</mi></math>가 크기 때문에 배리어가 강하다. 해는 feasible region의 깊은 내부에 머문다. <math><mi>t</mi></math>가 커지면 <math><mn>1</mn><mo>/</mo><mi>t</mi></math>가 작아져 배리어가 약해진다. 그러면 원래 목적함수를 개선하는 데 필요할 경우 해가 경계에 가까워질 수 있다.

## 수학적 구조

배리어 문제의 stationarity 조건은 다음과 같다.

<math display="block" aria-label="Stationarity of the barrier problem">
  <mi>&nabla;</mi><msub><mi>f</mi><mn>0</mn></msub>
  <mo>(</mo><mi>x</mi><mo>)</mo>
  <mo>-</mo>
  <mfrac>
    <mn>1</mn>
    <mi>t</mi>
  </mfrac>
  <munderover>
    <mo>&sum;</mo>
    <mrow><mi>i</mi><mo>=</mo><mn>1</mn></mrow>
    <mi>m</mi>
  </munderover>
  <mfrac>
    <mn>1</mn>
    <mrow><msub><mi>f</mi><mi>i</mi></msub><mo>(</mo><mi>x</mi><mo>)</mo></mrow>
  </mfrac>
  <mi>&nabla;</mi><msub><mi>f</mi><mi>i</mi></msub>
  <mo>(</mo><mi>x</mi><mo>)</mo>
  <mo>+</mo>
  <msup><mi>A</mi><mi>T</mi></msup>
  <mi>&nu;</mi>
  <mo>=</mo>
  <mn>0</mn>
  <mo>.</mo>
</math>

이 식은 다음과 같이 정의하면 KKT stationarity 조건과 닮은 형태로 다시 쓸 수 있다.

<math display="block" aria-label="Interior-point multiplier definition">
  <msub><mi>&lambda;</mi><mi>i</mi></msub>
  <mo>=</mo>
  <mo>-</mo>
  <mfrac>
    <mn>1</mn>
    <mrow><mi>t</mi><msub><mi>f</mi><mi>i</mi></msub><mo>(</mo><mi>x</mi><mo>)</mo></mrow>
  </mfrac>
  <mo>.</mo>
</math>

내점법의 해는 <math><msub><mi>f</mi><mi>i</mi></msub><mo>(</mo><mi>x</mi><mo>)</mo><mo>&lt;</mo><mn>0</mn></math>을 만족하므로, 이 정의는 <math><msub><mi>&lambda;</mi><mi>i</mi></msub><mo>></mo><mn>0</mn></math>을 준다.

이 정의를 stationarity 조건에 대입하면 다음을 얻는다.

<math display="block" aria-label="KKT-form stationarity from barrier problem">
  <mi>&nabla;</mi><msub><mi>f</mi><mn>0</mn></msub>
  <mo>(</mo><mi>x</mi><mo>)</mo>
  <mo>+</mo>
  <munderover>
    <mo>&sum;</mo>
    <mrow><mi>i</mi><mo>=</mo><mn>1</mn></mrow>
    <mi>m</mi>
  </munderover>
  <msub><mi>&lambda;</mi><mi>i</mi></msub>
  <mi>&nabla;</mi><msub><mi>f</mi><mi>i</mi></msub>
  <mo>(</mo><mi>x</mi><mo>)</mo>
  <mo>+</mo>
  <msup><mi>A</mi><mi>T</mi></msup>
  <mi>&nu;</mi>
  <mo>=</mo>
  <mn>0</mn>
  <mo>.</mo>
</math>

이는 KKT stationarity 조건과 정확히 같은 형태이다. 차이는 complementary slackness에서 나타난다. 승수 정의로부터 다음을 얻는다.

<math display="block" aria-label="Perturbed complementarity in original inequality form">
  <mo>-</mo>
  <msub><mi>&lambda;</mi><mi>i</mi></msub>
  <msub><mi>f</mi><mi>i</mi></msub>
  <mo>(</mo><mi>x</mi><mo>)</mo>
  <mo>=</mo>
  <mfrac>
    <mn>1</mn>
    <mi>t</mi>
  </mfrac>
  <mo>.</mo>
</math>

slack variable을 <math><msub><mi>s</mi><mi>i</mi></msub><mo>=</mo><mo>-</mo><msub><mi>f</mi><mi>i</mi></msub><mo>(</mo><mi>x</mi><mo>)</mo><mo>></mo><mn>0</mn></math>로 정의하면 이것은 다음이 된다.

<math display="block" aria-label="Perturbed complementarity with slack variable">
  <msub><mi>&lambda;</mi><mi>i</mi></msub>
  <msub><mi>s</mi><mi>i</mi></msub>
  <mo>=</mo>
  <mfrac>
    <mn>1</mn>
    <mi>t</mi>
  </mfrac>
  <mo>.</mo>
</math>

이것이 IPM의 중심 아이디어이다.

<math display="block" aria-label="Central path complementarity">
  <msub><mi>&lambda;</mi><mi>i</mi></msub>
  <msub><mi>s</mi><mi>i</mi></msub>
  <mo>=</mo>
  <mi>&mu;</mi>
  <mo>,</mo>
  <mspace width="0.8em"></mspace>
  <mi>&mu;</mi>
  <mo>=</mo>
  <mfrac>
    <mn>1</mn>
    <mi>t</mi>
  </mfrac>
  <mo>.</mo>
</math>

원래 KKT 조건은 <math><msub><mi>&lambda;</mi><mi>i</mi></msub><msub><mi>s</mi><mi>i</mi></msub><mo>=</mo><mn>0</mn></math>을 요구한다. 반면 내점법은 <math><msub><mi>&lambda;</mi><mi>i</mi></msub><msub><mi>s</mi><mi>i</mi></msub><mo>=</mo><mi>&mu;</mi><mo>></mo><mn>0</mn></math>이라는 교란된 버전을 따른다. <math><mi>&mu;</mi><mo>&downarrow;</mo><mn>0</mn></math>이 되면, 이 교란된 조건은 정확한 KKT complementary slackness 조건에 가까워진다.

## 왜 작동할 수 있는가

이는 central path에 대한 유용한 해석을 준다. IPM은 처음부터 어떤 제약이 active이고 어떤 제약이 inactive인지 결정하지 않는다. 대신 모든 부등식 제약조건이 양의 slack <math><msub><mi>s</mi><mi>i</mi></msub><mo>></mo><mn>0</mn></math>과 양의 multiplier <math><msub><mi>&lambda;</mi><mi>i</mi></msub><mo>></mo><mn>0</mn></math>를 가지며, <math><msub><mi>&lambda;</mi><mi>i</mi></msub><msub><mi>s</mi><mi>i</mi></msub><mo>=</mo><mi>&mu;</mi></math>를 만족한다.

<math><mi>&mu;</mi></math>가 감소하면서 해는 KKT 지점에 접근한다. 최적해에서 active가 되는 제약조건에서는 slack <math><msub><mi>s</mi><mi>i</mi></msub></math>가 0으로 가고 <math><msub><mi>&lambda;</mi><mi>i</mi></msub></math>는 양수로 남을 수 있다. inactive 제약조건에서는 slack이 양수로 남고 <math><msub><mi>&lambda;</mi><mi>i</mi></msub></math>가 0으로 간다.

따라서 IPM은 active set을 암묵적으로 점진적으로 발견한다.

## 가정과 한계

흔한 오해는 IPM이 처음에는 제약을 더 엄격하게 만족하다가 이후 점차 제약을 완화한다고 말하는 것이다. 이는 정확하지 않다. 부등식 제약조건은 완화되지 않는다. 실제로 이 방법은 interior path 전체에서 <math><msub><mi>f</mi><mi>i</mi></msub><mo>(</mo><mi>x</mi><mo>)</mo><mo>&lt;</mo><mn>0</mn></math>을 유지한다.

완화되는 것은 primal feasibility가 아니라 complementary slackness이다.

초기에는 <math><mi>&mu;</mi></math>가 상대적으로 크므로 <math><msub><mi>&lambda;</mi><mi>i</mi></msub><msub><mi>s</mi><mi>i</mi></msub><mo>=</mo><mi>&mu;</mi></math>는 정확한 KKT 조건 <math><msub><mi>&lambda;</mi><mi>i</mi></msub><msub><mi>s</mi><mi>i</mi></msub><mo>=</mo><mn>0</mn></math>과 거리가 멀다. 알고리즘이 진행되면서 <math><mi>&mu;</mi></math>는 작아진다. 그러면 해는 complementary slackness를 더 정확히 만족하며 진짜 제약 최적해에 가까워진다.

따라서 올바른 직관은 다음과 같다. 이 방법은 iterate를 엄격히 feasible하게 유지하고, 처음에는 경계를 피하는 강한 배리어에서 시작하며, 최적해가 경계에 있을 경우 그 경계에 가까워질 수 있도록 배리어를 점차 약화한다. 이 과정에서 <math><mi>&mu;</mi><mo>&rarr;</mo><mn>0</mn></math>일 때 사라지는 perturbation을 가진 KKT 시스템을 따른다.

## 비판적 평가

이것이 IPM이 KKT 조건과 깊게 연결되는 이유이다. IPM은 단순한 heuristic barrier method가 아니다. 다음과 같은 교란된 KKT 시스템의 sequence를 체계적으로 푸는 방법으로 볼 수 있다.

<math display="block" aria-label="Perturbed KKT system followed by an interior-point method">
  <mtable>
    <mtr>
      <mtd>
        <msub><mi>f</mi><mi>i</mi></msub>
        <mo>(</mo><mi>x</mi><mo>)</mo>
        <mo>&lt;</mo>
        <mn>0</mn>
        <mo>,</mo>
      </mtd>
    </mtr>
    <mtr>
      <mtd>
        <msub><mi>&lambda;</mi><mi>i</mi></msub>
        <mo>></mo>
        <mn>0</mn>
        <mo>,</mo>
      </mtd>
    </mtr>
    <mtr>
      <mtd>
        <msub><mi>&lambda;</mi><mi>i</mi></msub>
        <msub><mi>s</mi><mi>i</mi></msub>
        <mo>=</mo>
        <mi>&mu;</mi>
        <mo>,</mo>
      </mtd>
    </mtr>
    <mtr>
      <mtd>
        <mi>&nabla;</mi><msub><mi>f</mi><mn>0</mn></msub>
        <mo>(</mo><mi>x</mi><mo>)</mo>
        <mo>+</mo>
        <munderover>
          <mo>&sum;</mo>
          <mrow><mi>i</mi><mo>=</mo><mn>1</mn></mrow>
          <mi>m</mi>
        </munderover>
        <msub><mi>&lambda;</mi><mi>i</mi></msub>
        <mi>&nabla;</mi><msub><mi>f</mi><mi>i</mi></msub>
        <mo>(</mo><mi>x</mi><mo>)</mo>
        <mo>+</mo>
        <msup><mi>A</mi><mi>T</mi></msup>
        <mi>&nu;</mi>
        <mo>=</mo>
        <mn>0</mn>
        <mo>,</mo>
      </mtd>
    </mtr>
    <mtr>
      <mtd>
        <mi>A</mi><mi>x</mi>
        <mo>=</mo>
        <mi>b</mi>
        <mo>.</mo>
      </mtd>
    </mtr>
  </mtable>
</math>

<math><mi>&mu;</mi><mo>&downarrow;</mo><mn>0</mn></math>이면 이 시스템은 원래 KKT 시스템으로 수렴한다.

라그랑지안은 최적점에서의 힘의 균형을 설명한다. KKT 조건은 정확한 최적성 구조를 설명한다. 내점법은 정확한 complementary slackness를 매끄럽고 양의 perturbation으로 대체함으로써 그 구조를 향해 가는 계산 경로를 제공한다.

간단히 말하면 다음과 같다.

<math display="block" aria-label="Relationship between Lagrangian KKT and IPM">
  <mtable>
    <mtr>
      <mtd>
        <mtext>Lagrangian</mtext>
        <mspace width="0.5em"></mspace>
        <mo>&rArr;</mo>
        <mspace width="0.5em"></mspace>
        <mtext>stationarity and multipliers</mtext>
      </mtd>
    </mtr>
    <mtr>
      <mtd>
        <mtext>KKT conditions</mtext>
        <mspace width="0.5em"></mspace>
        <mo>&rArr;</mo>
        <mspace width="0.5em"></mspace>
        <mtext>exact constrained optimality</mtext>
      </mtd>
    </mtr>
    <mtr>
      <mtd>
        <mtext>IPM</mtext>
        <mspace width="0.5em"></mspace>
        <mo>&rArr;</mo>
        <mspace width="0.5em"></mspace>
        <mtext>perturbed KKT path approaching exact KKT</mtext>
      </mtd>
    </mtr>
  </mtable>
</math>

이것이 IPM, KKT 조건, 라그랑지안의 관계를 이해하는 가장 깔끔한 방식이다.

## 참고문헌

- 대상 논문: 해당 없음. 이 글은 제공된 텍스트를 바탕으로 한 개념적 연구 노트이다.
- 대상 논문의 참고문헌: 해당 없음.
