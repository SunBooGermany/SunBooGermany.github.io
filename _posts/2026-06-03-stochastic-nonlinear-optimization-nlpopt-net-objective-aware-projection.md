---
layout: post
title: "NLPOpt-Net: Objective-Aware Projection for Parametric Nonlinear Programs"
title_ko: "NLPOpt-Net: 파라메트릭 비선형계획을 위한 목적함수 인식 projection"
date: 2026-06-03
category: stochastic-nonlinear-optimization
category_label: "Mathematical Optimization"
research_group: algorithmic_reviews
research_category: stochastic-nonlinear-optimization
research_category_label: "Mathematical Optimization"
application_category: ""
application_category_label: ""
method_category: "stochastic-nonlinear-optimization"
method_category_label: "Mathematical Optimization"
paper_title: "NLPOpt-Net: A Learning Method for Nonlinear Optimization with Feasibility Guarantees"
authors: "Roy, B. N.; Golder, R.; Hasan, M. M."
venue: "arXiv preprint"
year: "2026"
doi: ""
arxiv: "2605.00260"
source_url: "https://arxiv.org/abs/2605.00260"
tags:
  - "parametric NLP"
  - "differentiable optimization"
  - "projection layer"
  - "Chambolle-Pock"
  - "implicit differentiation"
  - "feasibility"
excerpt: "A critical note on NLPOpt-Net, which learns a parametric NLP solution map with a neural warm start and an objective-aware differentiable projection layer."
excerpt_ko: "NLPOpt-Net을 신경망 warm start와 목적함수 인식 differentiable projection layer가 결합된 파라메트릭 NLP solution-map 학습법으로 정리한 비판적 노트."
language: "en-ko"
has_korean_note: false
---

## Problem: learning a feasible solution map, not solving one NLP once

The problem addressed here is not simply "solve one nonlinear optimization problem." It is closer to learning the solution map of a constrained parametric nonlinear program. A parameter vector <math><mi>x</mi></math> changes across instances, and the desired output is a fast prediction of the optimizer <math><msup><mi>y</mi><mo>*</mo></msup><mo>(</mo><mi>x</mi><mo>)</mo></math> that still respects the constraints of the instance.

The original problem has the form

<math display="block" aria-label="Parametric constrained nonlinear program">
  <munder><mi>min</mi><mi>y</mi></munder>
  <mspace width="0.4em"></mspace>
  <mi>f</mi><mo>(</mo><mi>x</mi><mo>,</mo><mi>y</mi><mo>)</mo>
  <mspace width="1em"></mspace>
  <mtext>subject to</mtext>
  <mspace width="0.4em"></mspace>
  <mi>h</mi><mo>(</mo><mi>x</mi><mo>,</mo><mi>y</mi><mo>)</mo><mo>=</mo><mn>0</mn><mo>,</mo>
  <mspace width="0.4em"></mspace>
  <mi>g</mi><mo>(</mo><mi>x</mi><mo>,</mo><mi>y</mi><mo>)</mo><mo>&le;</mo><mn>0</mn><mo>,</mo>
  <mspace width="0.4em"></mspace>
  <mi>l</mi><mo>(</mo><mi>x</mi><mo>)</mo><mo>&le;</mo><mi>y</mi><mo>&le;</mo><mi>u</mi><mo>(</mo><mi>x</mi><mo>)</mo><mo>.</mo>
</math>

A plain neural network can map <math><mi>x</mi></math> to a candidate <math><mover accent="true"><mi>y</mi><mo>^</mo></mover><mo>=</mo><msub><mi>&Phi;</mi><mi>&theta;</mi></msub><mo>(</mo><mi>x</mi><mo>)</mo></math>. The difficulty is that this candidate may violate equality constraints, inequality constraints, or bounds. Soft penalties can reduce violation, but they do not by themselves give a clean feasibility story, and the penalty weight can distort the objective.

NLPOpt-Net takes a different view:

```text
x -> backbone neural network -> predicted primal-dual point -> projection layer -> feasible polished point
```

The neural network is therefore a warm-start generator, not the whole optimizer. The projection layer performs a constrained optimization step that tries to move the prediction into the feasible set while remaining aware of the original objective.

## Why not ordinary Euclidean projection?

The most direct repair would be Euclidean projection:

<math display="block" aria-label="Euclidean projection onto feasible set">
  <munder><mi>min</mi><mrow><mi>y</mi><mo>&isin;</mo><mi>S</mi><mo>(</mo><mi>x</mi><mo>)</mo></mrow></munder>
  <mspace width="0.4em"></mspace>
  <msup>
    <mrow><mo>&Vert;</mo><mi>y</mi><mo>-</mo><mover accent="true"><mi>y</mi><mo>^</mo></mover><mo>&Vert;</mo></mrow>
    <mn>2</mn>
  </msup>
  <mo>.</mo>
</math>

This guarantees feasibility if the projection is solved exactly, but it is blind to the objective. The nearest feasible point in Euclidean distance can be a poor point for <math><mi>f</mi><mo>(</mo><mi>x</mi><mo>,</mo><mi>y</mi><mo>)</mo></math>. In other words, the projection may correct constraints while moving in a direction that worsens the optimization objective.

The central idea of NLPOpt-Net is objective-aware projection. Around the current prediction, the method builds a local quadratic approximation of the original objective and solves a constrained subproblem. The projection is not just "closest feasible point"; it is a local optimization step.

This is the right way to read the method. NLPOpt-Net is a learning-augmented sequential quadratic projection scheme: the network predicts a good primal-dual starting point, and the projection layer performs constrained polishing.

## Architecture

The backbone network predicts both primal and dual variables:

<math display="block" aria-label="Predicted primal and dual variables">
  <mover accent="true"><mi>z</mi><mo>^</mo></mover>
  <mo>=</mo>
  <msub><mi>&Phi;</mi><mi>&theta;</mi></msub><mo>(</mo><mi>x</mi><mo>)</mo>
  <mo>,</mo>
  <mspace width="0.6em"></mspace>
  <mover accent="true"><mi>z</mi><mo>^</mo></mover>
  <mo>=</mo>
  <mo>(</mo><mover accent="true"><mi>y</mi><mo>^</mo></mover><mo>,</mo>
  <mover accent="true"><mi>&lambda;</mi><mo>^</mo></mover><mo>,</mo>
  <mover accent="true"><mi>&mu;</mi><mo>^</mo></mover><mo>)</mo><mo>.</mo>
</math>

Then a projection operator maps this prediction to

<math display="block" aria-label="Projection output">
  <mover accent="true"><mi>z</mi><mo>~</mo></mover>
  <mo>=</mo>
  <msub><mi>P</mi><mi>o</mi></msub>
  <mo>(</mo><mi>x</mi><mo>,</mo><mover accent="true"><mi>z</mi><mo>^</mo></mover><mo>)</mo><mo>.</mo>
</math>

The operator is implemented as a composition of <math><mi>k</mi></math> projection sublayers. Each sublayer solves a local QP obtained by linearizing the nonlinear constraints at the current point and using a diagonal quadratic model of the objective.

The training objective combines the original objective, constraint-related Lagrangian terms, and a consistency term that keeps the network prediction close to the projected output. In simplified form:

<math display="block" aria-label="Training loss with consistency">
  <mi>L</mi>
  <mo>&approx;</mo>
  <mi>f</mi><mo>(</mo><mi>x</mi><mo>,</mo><mover accent="true"><mi>y</mi><mo>~</mo></mover><mo>)</mo>
  <mo>+</mo>
  <msup><mrow><mo>&Vert;</mo><msup><mover accent="true"><mi>&lambda;</mi><mo>~</mo></mover><mi>T</mi></msup><mi>h</mi><mo>(</mo><mi>x</mi><mo>,</mo><mover accent="true"><mi>y</mi><mo>~</mo></mover><mo>)</mo><mo>&Vert;</mo></mrow><mn>2</mn></msup>
  <mo>+</mo>
  <msup><mover accent="true"><mi>&mu;</mi><mo>~</mo></mover><mi>T</mi></msup>
  <mi>ReLU</mi><mo>(</mo><mi>g</mi><mo>(</mo><mi>x</mi><mo>,</mo><mover accent="true"><mi>y</mi><mo>~</mo></mover><mo>)</mo><mo>)</mo>
  <mo>+</mo>
  <msub><mi>M</mi><mi>&alpha;</mi></msub>
  <msup><mrow><mo>&Vert;</mo><mover accent="true"><mi>z</mi><mo>^</mo></mover><mo>-</mo><mover accent="true"><mi>z</mi><mo>~</mo></mover><mo>&Vert;</mo></mrow><mn>2</mn></msup>
  <mo>.</mo>
</math>

The last term matters practically. It trains the backbone so that the projection layer does not need to make a large correction at every inference call.

## Projection as local quadratic optimization

At a current point <math><msub><mi>y</mi><mi>i</mi></msub></math>, the method approximates the objective by a local quadratic model. The idealized form around <math><mover accent="true"><mi>y</mi><mo>^</mo></mover></math> is

<math display="block" aria-label="Local quadratic objective model">
  <mover accent="true"><mi>f</mi><mo>^</mo></mover>
  <mo>(</mo><mi>x</mi><mo>,</mo><mi>y</mi><mo>;</mo><mover accent="true"><mi>y</mi><mo>^</mo></mover><mo>)</mo>
  <mo>=</mo>
  <mi>f</mi><mo>(</mo><mi>x</mi><mo>,</mo><mover accent="true"><mi>y</mi><mo>^</mo></mover><mo>)</mo>
  <mo>+</mo>
  <msub><mo>&nabla;</mo><mi>y</mi></msub><mi>f</mi><mo>(</mo><mi>x</mi><mo>,</mo><mover accent="true"><mi>y</mi><mo>^</mo></mover><mo>)</mo>
  <msup><mrow></mrow><mi>T</mi></msup>
  <mo>(</mo><mi>y</mi><mo>-</mo><mover accent="true"><mi>y</mi><mo>^</mo></mover><mo>)</mo>
  <mo>+</mo>
  <mfrac><mn>1</mn><mn>2</mn></mfrac>
  <msup><mrow><mo>(</mo><mi>y</mi><mo>-</mo><mover accent="true"><mi>y</mi><mo>^</mo></mover><mo>)</mo></mrow><mi>T</mi></msup>
  <msub><mi>H</mi><mi>d</mi></msub>
  <mo>(</mo><mi>y</mi><mo>-</mo><mover accent="true"><mi>y</mi><mo>^</mo></mover><mo>)</mo><mo>.</mo>
</math>

Instead of using the full Hessian, the projection layer uses a diagonal approximation, written in the supplied summary as <math><msub><mi>H</mi><mi>d</mi></msub><mo>=</mo><mi>&rho;</mi><mi>diag</mi><mo>(</mo><msubsup><mo>&nabla;</mo><mrow><mi>y</mi><mi>y</mi></mrow><mn>2</mn></msubsup><mi>f</mi><mo>(</mo><mi>x</mi><mo>,</mo><mover accent="true"><mi>y</mi><mo>^</mo></mover><mo>)</mo><mo>)</mo></math>. This sacrifices curvature coupling between variables, but it makes the inner QP much cheaper.

Each projection sublayer solves a QP of the form

<math display="block" aria-label="Local QP projection subproblem">
  <munder><mi>min</mi><mi>y</mi></munder>
  <mspace width="0.4em"></mspace>
  <mfrac><mn>1</mn><mn>2</mn></mfrac>
  <msup><mi>y</mi><mi>T</mi></msup><msub><mi>Q</mi><mi>i</mi></msub><mi>y</mi>
  <mo>+</mo>
  <msubsup><mi>c</mi><mi>i</mi><mi>T</mi></msubsup><mi>y</mi>
  <mspace width="1em"></mspace>
  <mtext>subject to</mtext>
  <mspace width="0.4em"></mspace>
  <msub><mi>A</mi><mi>i</mi></msub><mi>y</mi><mo>=</mo><msub><mi>b</mi><mi>i</mi></msub><mo>,</mo>
  <mspace width="0.4em"></mspace>
  <msub><mi>C</mi><mi>i</mi></msub><mi>y</mi><mo>&le;</mo><msub><mi>d</mi><mi>i</mi></msub><mo>,</mo>
  <mspace width="0.4em"></mspace>
  <mi>l</mi><mo>(</mo><mi>x</mi><mo>)</mo><mo>&le;</mo><mi>y</mi><mo>&le;</mo><mi>u</mi><mo>(</mo><mi>x</mi><mo>)</mo><mo>.</mo>
</math>

The nonlinear constraints are replaced by first-order linearizations:

<math display="block" aria-label="Constraint linearization">
  <msub><mi>A</mi><mi>i</mi></msub><mo>=</mo><msub><mi>J</mi><mi>h</mi></msub><mo>(</mo><mi>x</mi><mo>,</mo><msub><mi>y</mi><mi>i</mi></msub><mo>)</mo><mo>,</mo>
  <mspace width="0.5em"></mspace>
  <msub><mi>b</mi><mi>i</mi></msub><mo>=</mo><msub><mi>J</mi><mi>h</mi></msub><mo>(</mo><mi>x</mi><mo>,</mo><msub><mi>y</mi><mi>i</mi></msub><mo>)</mo><msub><mi>y</mi><mi>i</mi></msub><mo>-</mo><mi>h</mi><mo>(</mo><mi>x</mi><mo>,</mo><msub><mi>y</mi><mi>i</mi></msub><mo>)</mo><mo>,</mo>
  <mspace width="0.5em"></mspace>
  <msub><mi>C</mi><mi>i</mi></msub><mo>=</mo><msub><mi>J</mi><mi>g</mi></msub><mo>(</mo><mi>x</mi><mo>,</mo><msub><mi>y</mi><mi>i</mi></msub><mo>)</mo><mo>,</mo>
  <mspace width="0.5em"></mspace>
  <msub><mi>d</mi><mi>i</mi></msub><mo>=</mo><msub><mi>J</mi><mi>g</mi></msub><mo>(</mo><mi>x</mi><mo>,</mo><msub><mi>y</mi><mi>i</mi></msub><mo>)</mo><msub><mi>y</mi><mi>i</mi></msub><mo>-</mo><mi>g</mi><mo>(</mo><mi>x</mi><mo>,</mo><msub><mi>y</mi><mi>i</mi></msub><mo>)</mo><mo>.</mo>
</math>

The objective terms are

<math display="block" aria-label="QP objective terms">
  <msub><mi>Q</mi><mi>i</mi></msub><mo>=</mo><mi>&rho;</mi><mi>diag</mi><mo>(</mo><msup><mo>&nabla;</mo><mn>2</mn></msup><mi>f</mi><mo>(</mo><mi>x</mi><mo>,</mo><msub><mi>y</mi><mi>i</mi></msub><mo>)</mo><mo>)</mo><mo>,</mo>
  <mspace width="0.6em"></mspace>
  <msub><mi>c</mi><mi>i</mi></msub><mo>=</mo><mo>&nabla;</mo><mi>f</mi><mo>(</mo><mi>x</mi><mo>,</mo><msub><mi>y</mi><mi>i</mi></msub><mo>)</mo><mo>-</mo><msub><mi>Q</mi><mi>i</mi></msub><msub><mi>y</mi><mi>i</mi></msub><mo>.</mo>
</math>

This is SQP-like, but it is not a full SQP method. It uses diagonal objective curvature and linearized constraints as a lightweight projection mechanism inside a neural architecture.

## Feasibility and descent: what is actually guaranteed?

The feasibility story is strongest when the constraints are affine. If

<math display="block" aria-label="Affine constraints">
  <mi>h</mi><mo>(</mo><mi>x</mi><mo>,</mo><mi>y</mi><mo>)</mo><mo>=</mo><mi>A</mi><mo>(</mo><mi>x</mi><mo>)</mo><mi>y</mi><mo>-</mo><mi>b</mi><mo>(</mo><mi>x</mi><mo>)</mo><mo>,</mo>
  <mspace width="0.6em"></mspace>
  <mi>g</mi><mo>(</mo><mi>x</mi><mo>,</mo><mi>y</mi><mo>)</mo><mo>=</mo><mi>C</mi><mo>(</mo><mi>x</mi><mo>)</mo><mi>y</mi><mo>-</mo><mi>d</mi><mo>(</mo><mi>x</mi><mo>)</mo><mo>,</mo>
</math>

then the linearization is the original constraint. One exact projection layer can therefore enforce the affine constraints, subject to the accuracy of the QP solve.

For nonlinear constraints, the claim is more conditional. A finite number of projection layers does not magically remove linearization error. Under smoothness, regularity, nonsingular KKT conditions, and second-order sufficient conditions, the iterative projection can be interpreted as a local polishing procedure with local convergence behavior. But in deployed inference, feasibility also depends on <math><mi>k</mi></math>, solver tolerance, numerical conditioning, and how close the neural prediction is to the relevant local solution.

The descent story relies on a majorization argument. If <math><mi>f</mi></math> has an <math><mi>L</mi></math>-Lipschitz gradient and the diagonal quadratic term satisfies <math><msub><mi>H</mi><mi>d</mi></msub><mo>&succeq;</mo><mi>L</mi><mi>I</mi></math>, then the quadratic model upper-bounds the true objective locally:

<math display="block" aria-label="Quadratic upper bound intuition">
  <mi>f</mi><mo>(</mo><mi>x</mi><mo>,</mo><mi>y</mi><mo>)</mo>
  <mo>&le;</mo>
  <mover accent="true"><mi>f</mi><mo>^</mo></mover>
  <mo>(</mo><mi>x</mi><mo>,</mo><mi>y</mi><mo>;</mo><mover accent="true"><mi>y</mi><mo>^</mo></mover><mo>)</mo><mo>.</mo>
</math>

This explains why objective-aware projection is preferable to distance-only projection. The projection is designed so that feasibility repair is aligned with a local model of objective improvement. The important limitation is that the argument is local and assumption-dependent; it should not be read as a general global optimality guarantee for arbitrary nonconvex NLPs.

## Inner QP solver: modified Chambolle-Pock

Each projection subproblem is solved using a primal-dual Chambolle-Pock style iteration. The dual variables respond to equality and inequality violation, while the primal variable is updated against the objective and projected onto the box constraints.

A representative update is

<math display="block" aria-label="Primal dual update">
  <msup><mi>&lambda;</mi><mrow><mi>t</mi><mo>+</mo><mn>1</mn></mrow></msup>
  <mo>=</mo>
  <msup><mi>&lambda;</mi><mi>t</mi></msup>
  <mo>+</mo><mi>&sigma;</mi><mo>(</mo><mi>A</mi><msup><mover accent="true"><mi>y</mi><mo>&OverBar;</mo></mover><mi>t</mi></msup><mo>-</mo><mi>b</mi><mo>)</mo><mo>,</mo>
  <mspace width="0.6em"></mspace>
  <msup><mi>&mu;</mi><mrow><mi>t</mi><mo>+</mo><mn>1</mn></mrow></msup>
  <mo>=</mo>
  <mi>max</mi><mo>{</mo><mn>0</mn><mo>,</mo><msup><mi>&mu;</mi><mi>t</mi></msup><mo>+</mo><mi>&sigma;</mi><mo>(</mo><mi>C</mi><msup><mover accent="true"><mi>y</mi><mo>&OverBar;</mo></mover><mi>t</mi></msup><mo>-</mo><mi>d</mi><mo>)</mo><mo>}</mo><mo>.</mo>
</math>

The primal update includes

<math display="block" aria-label="Diagonal inverse structure">
  <mi>P</mi><mo>=</mo><msup><mrow><mo>(</mo><mi>I</mi><mo>+</mo><mi>&tau;</mi><mi>Q</mi><mo>)</mo></mrow><mrow><mo>-</mo><mn>1</mn></mrow></msup><mo>.</mo>
</math>

Because <math><mi>Q</mi></math> is diagonal, this inverse is elementwise division rather than a dense matrix inverse. This is the practical meaning of the "inversion-free" design: the projection layer can run many primal-dual steps without repeatedly solving a large linear system.

## Differentiating through the projection

A direct automatic differentiation route would unroll all Chambolle-Pock iterations in memory. NLPOpt-Net instead uses implicit differentiation at the fixed point of the projection solver.

Let the fixed point be

<math display="block" aria-label="Fixed point equation">
  <msup><mi>z</mi><mo>*</mo></msup><mo>=</mo><mi>F</mi><mo>(</mo><msup><mi>z</mi><mo>*</mo></msup><mo>;</mo><mi>w</mi><mo>)</mo><mo>,</mo>
  <mspace width="0.6em"></mspace>
  <mi>w</mi><mo>=</mo><mi>M</mi><mo>(</mo><mi>x</mi><mo>,</mo><mover accent="true"><mi>z</mi><mo>^</mo></mover><mo>)</mo><mo>,</mo>
</math>

where <math><mi>w</mi></math> denotes the QP data. Define the residual

<math display="block" aria-label="Fixed point residual">
  <mi>G</mi><mo>(</mo><mi>z</mi><mo>,</mo><mi>w</mi><mo>)</mo>
  <mo>=</mo>
  <mi>F</mi><mo>(</mo><mi>z</mi><mo>;</mo><mi>w</mi><mo>)</mo><mo>-</mo><mi>z</mi><mo>.</mo>
</math>

Then gradients can be computed by solving an adjoint linear system such as

<math display="block" aria-label="Implicit differentiation adjoint system">
  <msup><mrow><mo>(</mo><mi>I</mi><mo>-</mo><msub><mi>J</mi><mi>F</mi></msub><mo>(</mo><msup><mi>z</mi><mo>*</mo></msup><mo>)</mo><mo>)</mo></mrow><mi>T</mi></msup>
  <mi>v</mi>
  <mo>=</mo>
  <msub><mi>g</mi><mi>z</mi></msub><mo>.</mo>
</math>

The point is not just mathematical elegance. It avoids storing every solver iterate during training and makes the projection layer a differentiable module with a custom VJP-style backward route.

## Experimental reading

The reported experiments cover convex QP, convex QCQP, convex NLP, and a simple nonconvex NLP setting. The important pattern is that NLPOpt-Net matches solver-level objectives closely in convex settings while reporting zero equality and inequality violation in the main tables. In the convex QP case, for example, it is reported to reach the same objective value as OSQP, while soft-constrained neural approaches and DC3 leave larger gaps or violations.

The nonlinear cases are more expensive because they use multiple projection layers. This is expected: every additional layer is another linearize-and-solve polishing step. The method trades a slightly heavier inference path for stronger feasibility repair than a plain feedforward predictor.

The nonconvex result should be read carefully. It is useful empirical evidence that the architecture can work beyond clean convex cases, but it is not a general nonconvex guarantee. The theoretical story is fundamentally tied to convexity, regularity, local approximation quality, and solver accuracy.

## Critical assessment

The strongest contribution is the design choice to put a real constrained optimization operation inside the network, but to make that operation lightweight enough to use as a layer. Compared with soft penalties, the feasibility mechanism is more direct. Compared with Euclidean projection, the correction is less likely to destroy the objective. Compared with classic differentiable QP layers, the method tries to handle nonlinear constraints by sequential local QP projection.

There are also clear limits.

First, "guaranteed feasibility" is conditional. It is strong for affine constraints and exact solves. For nonlinear constraints, finite projection depth, finite Chambolle-Pock iterations, and linearization error make the practical statement closer to feasibility within tolerance.

Second, convexity and regularity matter. Convex objective and constraints, affine equality constraints, Lipschitz gradients, feasible instances, and well-behaved KKT systems are not minor technicalities. They are the scaffolding behind the theoretical claims.

Third, the diagonal Hessian approximation is a computational compromise. It enables cheap updates, but it ignores cross-variable curvature. For NLPs with strong variable coupling, the projection direction may be less accurate, and the method may need more projection layers or iterations.

My reading is therefore: NLPOpt-Net should not be described as a neural network that directly solves NLPs. It is better understood as a hybrid method in which a neural network predicts a warm start, and an objective-aware differentiable projection layer performs local constrained optimization. Its value lies in this disciplined combination of solution-map learning, sequential QP approximation, primal-dual first-order solving, and implicit differentiation.

## References

Roy, B. N., Golder, R., & Hasan, M. M. (2026). NLPOpt-Net: A Learning Method for Nonlinear Optimization with Feasibility Guarantees. arXiv preprint arXiv:2605.00260.

<!-- ko -->

## 문제 설정: 하나의 NLP가 아니라 feasible solution map을 학습하는 문제

이 논문이 다루는 문제는 "비선형 최적화 문제 하나를 푼다"는 형태보다, 파라미터가 바뀔 때마다 대응되는 최적해의 map을 빠르게 예측하는 문제에 가깝다. 파라미터 <math><mi>x</mi></math>가 계속 바뀌고, 목표는 constrained parametric NLP의 해 <math><msup><mi>y</mi><mo>*</mo></msup><mo>(</mo><mi>x</mi><mo>)</mo></math>를 빠르게 예측하되 constraint violation을 통제하는 것이다.

문제는 다음 형태로 주어진다.

<math display="block" aria-label="Parametric constrained nonlinear program">
  <munder><mi>min</mi><mi>y</mi></munder>
  <mspace width="0.4em"></mspace>
  <mi>f</mi><mo>(</mo><mi>x</mi><mo>,</mo><mi>y</mi><mo>)</mo>
  <mspace width="1em"></mspace>
  <mtext>subject to</mtext>
  <mspace width="0.4em"></mspace>
  <mi>h</mi><mo>(</mo><mi>x</mi><mo>,</mo><mi>y</mi><mo>)</mo><mo>=</mo><mn>0</mn><mo>,</mo>
  <mspace width="0.4em"></mspace>
  <mi>g</mi><mo>(</mo><mi>x</mi><mo>,</mo><mi>y</mi><mo>)</mo><mo>&le;</mo><mn>0</mn><mo>,</mo>
  <mspace width="0.4em"></mspace>
  <mi>l</mi><mo>(</mo><mi>x</mi><mo>)</mo><mo>&le;</mo><mi>y</mi><mo>&le;</mo><mi>u</mi><mo>(</mo><mi>x</mi><mo>)</mo><mo>.</mo>
</math>

일반적인 neural network는 <math><mi>x</mi></math>를 받아 <math><mover accent="true"><mi>y</mi><mo>^</mo></mover><mo>=</mo><msub><mi>&Phi;</mi><mi>&theta;</mi></msub><mo>(</mo><mi>x</mi><mo>)</mo></math>를 출력할 수 있다. 하지만 이 예측값은 equality constraint, inequality constraint, bound constraint를 어길 수 있다. Soft penalty 방식은 violation을 줄일 수는 있지만, penalty weight에 민감하고 objective를 왜곡할 수 있다.

NLPOpt-Net의 관점은 다르다.

```text
x -> backbone neural network -> predicted primal-dual point -> projection layer -> feasible polished point
```

즉 neural network는 전체 optimizer가 아니라 warm start 생성기다. Projection layer가 constraint를 만족하도록 보정하면서 동시에 원래 objective를 의식한 local optimization step을 수행한다.

## 왜 단순 Euclidean projection이 아닌가?

가장 단순한 보정은 feasible set으로의 Euclidean projection이다.

<math display="block" aria-label="Euclidean projection onto feasible set">
  <munder><mi>min</mi><mrow><mi>y</mi><mo>&isin;</mo><mi>S</mi><mo>(</mo><mi>x</mi><mo>)</mo></mrow></munder>
  <mspace width="0.4em"></mspace>
  <msup>
    <mrow><mo>&Vert;</mo><mi>y</mi><mo>-</mo><mover accent="true"><mi>y</mi><mo>^</mo></mover><mo>&Vert;</mo></mrow>
    <mn>2</mn>
  </msup>
  <mo>.</mo>
</math>

이 방식은 projection을 정확히 풀면 feasibility를 얻을 수 있다. 그러나 objective와 무관하다. Euclidean distance 기준으로 가장 가까운 feasible point가 <math><mi>f</mi><mo>(</mo><mi>x</mi><mo>,</mo><mi>y</mi><mo>)</mo></math> 관점에서도 좋은 점이라는 보장은 없다. NN이 좋은 해 근처를 예측했는데, projection이 objective를 나쁘게 만드는 방향으로 이동할 수도 있다.

NLPOpt-Net의 핵심은 objective-aware projection이다. 현재 예측점 주변에서 원래 objective의 local quadratic approximation을 만들고, 이 근사 objective와 linearized constraint를 함께 사용해 constrained subproblem을 푼다. 따라서 projection은 단순히 "가장 가까운 feasible point"를 찾는 과정이 아니라 local optimization step이다.

이 점이 이 방법의 정체성이다. NLPOpt-Net은 learning-augmented sequential quadratic projection scheme으로 보는 것이 정확하다. Network는 primal-dual warm start를 주고, projection layer가 constrained polishing을 맡는다.

## 전체 구조

Backbone network는 primal variable뿐 아니라 dual variable도 예측한다.

<math display="block" aria-label="Predicted primal and dual variables">
  <mover accent="true"><mi>z</mi><mo>^</mo></mover>
  <mo>=</mo>
  <msub><mi>&Phi;</mi><mi>&theta;</mi></msub><mo>(</mo><mi>x</mi><mo>)</mo>
  <mo>,</mo>
  <mspace width="0.6em"></mspace>
  <mover accent="true"><mi>z</mi><mo>^</mo></mover>
  <mo>=</mo>
  <mo>(</mo><mover accent="true"><mi>y</mi><mo>^</mo></mover><mo>,</mo>
  <mover accent="true"><mi>&lambda;</mi><mo>^</mo></mover><mo>,</mo>
  <mover accent="true"><mi>&mu;</mi><mo>^</mo></mover><mo>)</mo><mo>.</mo>
</math>

이후 projection operator가

<math display="block" aria-label="Projection output">
  <mover accent="true"><mi>z</mi><mo>~</mo></mover>
  <mo>=</mo>
  <msub><mi>P</mi><mi>o</mi></msub>
  <mo>(</mo><mi>x</mi><mo>,</mo><mover accent="true"><mi>z</mi><mo>^</mo></mover><mo>)</mo>
</math>

를 계산한다. 이 operator는 <math><mi>k</mi></math>개의 projection sublayer의 composition으로 구현된다. 각 sublayer는 현재점에서 nonlinear constraint를 linearization하고, diagonal quadratic objective model을 사용한 local QP를 하나 푼다.

Training loss는 원래 objective, constraint 관련 Lagrangian term, 그리고 consistency term을 결합한다. 단순화해 쓰면 다음과 같다.

<math display="block" aria-label="Training loss with consistency">
  <mi>L</mi>
  <mo>&approx;</mo>
  <mi>f</mi><mo>(</mo><mi>x</mi><mo>,</mo><mover accent="true"><mi>y</mi><mo>~</mo></mover><mo>)</mo>
  <mo>+</mo>
  <msup><mrow><mo>&Vert;</mo><msup><mover accent="true"><mi>&lambda;</mi><mo>~</mo></mover><mi>T</mi></msup><mi>h</mi><mo>(</mo><mi>x</mi><mo>,</mo><mover accent="true"><mi>y</mi><mo>~</mo></mover><mo>)</mo><mo>&Vert;</mo></mrow><mn>2</mn></msup>
  <mo>+</mo>
  <msup><mover accent="true"><mi>&mu;</mi><mo>~</mo></mover><mi>T</mi></msup>
  <mi>ReLU</mi><mo>(</mo><mi>g</mi><mo>(</mo><mi>x</mi><mo>,</mo><mover accent="true"><mi>y</mi><mo>~</mo></mover><mo>)</mo><mo>)</mo>
  <mo>+</mo>
  <msub><mi>M</mi><mi>&alpha;</mi></msub>
  <msup><mrow><mo>&Vert;</mo><mover accent="true"><mi>z</mi><mo>^</mo></mover><mo>-</mo><mover accent="true"><mi>z</mi><mo>~</mo></mover><mo>&Vert;</mo></mrow><mn>2</mn></msup>
  <mo>.</mo>
</math>

마지막 항은 consistency loss다. Projection 결과와 NN prediction이 가까워지도록 학습시키기 때문에, inference 때 projection layer가 매번 큰 수정을 하지 않아도 되도록 만든다.

## Projection layer: local quadratic optimization

현재점 <math><msub><mi>y</mi><mi>i</mi></msub></math> 주변에서 objective를 local quadratic model로 근사한다. 이상화된 형태는 다음과 같다.

<math display="block" aria-label="Local quadratic objective model">
  <mover accent="true"><mi>f</mi><mo>^</mo></mover>
  <mo>(</mo><mi>x</mi><mo>,</mo><mi>y</mi><mo>;</mo><mover accent="true"><mi>y</mi><mo>^</mo></mover><mo>)</mo>
  <mo>=</mo>
  <mi>f</mi><mo>(</mo><mi>x</mi><mo>,</mo><mover accent="true"><mi>y</mi><mo>^</mo></mover><mo>)</mo>
  <mo>+</mo>
  <msub><mo>&nabla;</mo><mi>y</mi></msub><mi>f</mi><mo>(</mo><mi>x</mi><mo>,</mo><mover accent="true"><mi>y</mi><mo>^</mo></mover><mo>)</mo>
  <msup><mrow></mrow><mi>T</mi></msup>
  <mo>(</mo><mi>y</mi><mo>-</mo><mover accent="true"><mi>y</mi><mo>^</mo></mover><mo>)</mo>
  <mo>+</mo>
  <mfrac><mn>1</mn><mn>2</mn></mfrac>
  <msup><mrow><mo>(</mo><mi>y</mi><mo>-</mo><mover accent="true"><mi>y</mi><mo>^</mo></mover><mo>)</mo></mrow><mi>T</mi></msup>
  <msub><mi>H</mi><mi>d</mi></msub>
  <mo>(</mo><mi>y</mi><mo>-</mo><mover accent="true"><mi>y</mi><mo>^</mo></mover><mo>)</mo><mo>.</mo>
</math>

논문은 full Hessian 대신 diagonal approximation을 사용한다. 요약에서 제시된 형태로 쓰면 <math><msub><mi>H</mi><mi>d</mi></msub><mo>=</mo><mi>&rho;</mi><mi>diag</mi><mo>(</mo><msubsup><mo>&nabla;</mo><mrow><mi>y</mi><mi>y</mi></mrow><mn>2</mn></msubsup><mi>f</mi><mo>(</mo><mi>x</mi><mo>,</mo><mover accent="true"><mi>y</mi><mo>^</mo></mover><mo>)</mo><mo>)</mo></math>이다. 변수 간 curvature coupling은 버리지만, 내부 QP solver를 훨씬 싸게 만들 수 있다.

각 projection sublayer는 다음 QP를 푼다.

<math display="block" aria-label="Local QP projection subproblem">
  <munder><mi>min</mi><mi>y</mi></munder>
  <mspace width="0.4em"></mspace>
  <mfrac><mn>1</mn><mn>2</mn></mfrac>
  <msup><mi>y</mi><mi>T</mi></msup><msub><mi>Q</mi><mi>i</mi></msub><mi>y</mi>
  <mo>+</mo>
  <msubsup><mi>c</mi><mi>i</mi><mi>T</mi></msubsup><mi>y</mi>
  <mspace width="1em"></mspace>
  <mtext>subject to</mtext>
  <mspace width="0.4em"></mspace>
  <msub><mi>A</mi><mi>i</mi></msub><mi>y</mi><mo>=</mo><msub><mi>b</mi><mi>i</mi></msub><mo>,</mo>
  <mspace width="0.4em"></mspace>
  <msub><mi>C</mi><mi>i</mi></msub><mi>y</mi><mo>&le;</mo><msub><mi>d</mi><mi>i</mi></msub><mo>,</mo>
  <mspace width="0.4em"></mspace>
  <mi>l</mi><mo>(</mo><mi>x</mi><mo>)</mo><mo>&le;</mo><mi>y</mi><mo>&le;</mo><mi>u</mi><mo>(</mo><mi>x</mi><mo>)</mo><mo>.</mo>
</math>

Nonlinear constraint는 현재점에서 linearization한다.

<math display="block" aria-label="Constraint linearization">
  <msub><mi>A</mi><mi>i</mi></msub><mo>=</mo><msub><mi>J</mi><mi>h</mi></msub><mo>(</mo><mi>x</mi><mo>,</mo><msub><mi>y</mi><mi>i</mi></msub><mo>)</mo><mo>,</mo>
  <mspace width="0.5em"></mspace>
  <msub><mi>b</mi><mi>i</mi></msub><mo>=</mo><msub><mi>J</mi><mi>h</mi></msub><mo>(</mo><mi>x</mi><mo>,</mo><msub><mi>y</mi><mi>i</mi></msub><mo>)</mo><msub><mi>y</mi><mi>i</mi></msub><mo>-</mo><mi>h</mi><mo>(</mo><mi>x</mi><mo>,</mo><msub><mi>y</mi><mi>i</mi></msub><mo>)</mo><mo>,</mo>
  <mspace width="0.5em"></mspace>
  <msub><mi>C</mi><mi>i</mi></msub><mo>=</mo><msub><mi>J</mi><mi>g</mi></msub><mo>(</mo><mi>x</mi><mo>,</mo><msub><mi>y</mi><mi>i</mi></msub><mo>)</mo><mo>,</mo>
  <mspace width="0.5em"></mspace>
  <msub><mi>d</mi><mi>i</mi></msub><mo>=</mo><msub><mi>J</mi><mi>g</mi></msub><mo>(</mo><mi>x</mi><mo>,</mo><msub><mi>y</mi><mi>i</mi></msub><mo>)</mo><msub><mi>y</mi><mi>i</mi></msub><mo>-</mo><mi>g</mi><mo>(</mo><mi>x</mi><mo>,</mo><msub><mi>y</mi><mi>i</mi></msub><mo>)</mo><mo>.</mo>
</math>

Objective 쪽은

<math display="block" aria-label="QP objective terms">
  <msub><mi>Q</mi><mi>i</mi></msub><mo>=</mo><mi>&rho;</mi><mi>diag</mi><mo>(</mo><msup><mo>&nabla;</mo><mn>2</mn></msup><mi>f</mi><mo>(</mo><mi>x</mi><mo>,</mo><msub><mi>y</mi><mi>i</mi></msub><mo>)</mo><mo>)</mo><mo>,</mo>
  <mspace width="0.6em"></mspace>
  <msub><mi>c</mi><mi>i</mi></msub><mo>=</mo><mo>&nabla;</mo><mi>f</mi><mo>(</mo><mi>x</mi><mo>,</mo><msub><mi>y</mi><mi>i</mi></msub><mo>)</mo><mo>-</mo><msub><mi>Q</mi><mi>i</mi></msub><msub><mi>y</mi><mi>i</mi></msub><mo>.</mo>
</math>

따라서 전체적으로는 SQP와 닮았지만, full Lagrangian Hessian을 쓰는 정통 SQP는 아니다. Diagonal objective curvature와 linearized constraints를 이용하는 lightweight projection layer에 가깝다.

## Feasibility와 descent: 실제로 무엇이 보장되는가?

Feasibility 주장은 affine constraint에서 가장 강하다. 만약

<math display="block" aria-label="Affine constraints">
  <mi>h</mi><mo>(</mo><mi>x</mi><mo>,</mo><mi>y</mi><mo>)</mo><mo>=</mo><mi>A</mi><mo>(</mo><mi>x</mi><mo>)</mo><mi>y</mi><mo>-</mo><mi>b</mi><mo>(</mo><mi>x</mi><mo>)</mo><mo>,</mo>
  <mspace width="0.6em"></mspace>
  <mi>g</mi><mo>(</mo><mi>x</mi><mo>,</mo><mi>y</mi><mo>)</mo><mo>=</mo><mi>C</mi><mo>(</mo><mi>x</mi><mo>)</mo><mi>y</mi><mo>-</mo><mi>d</mi><mo>(</mo><mi>x</mi><mo>)</mo>
</math>

라면 linearization이 원래 constraint와 같다. 따라서 QP를 정확히 풀 수 있다면 한 projection layer만으로도 affine constraint를 만족시킬 수 있다.

Nonlinear constraint에서는 더 조심해야 한다. Finite number of layers가 linearization error를 자동으로 없애지는 않는다. Smoothness, regularity, nonsingular KKT condition, second-order sufficient condition 같은 조건 아래에서는 이 반복을 local polishing procedure로 해석할 수 있다. 하지만 실제 inference에서 feasibility는 <math><mi>k</mi></math>, solver tolerance, numerical conditioning, 그리고 NN prediction이 local solution 근처에 얼마나 잘 놓였는지에 의존한다.

Descent property는 majorization argument에 기대고 있다. <math><mi>f</mi></math>의 gradient가 <math><mi>L</mi></math>-Lipschitz이고 diagonal quadratic term이 <math><msub><mi>H</mi><mi>d</mi></msub><mo>&succeq;</mo><mi>L</mi><mi>I</mi></math>를 만족하면, local quadratic model은 true objective의 upper bound가 된다.

<math display="block" aria-label="Quadratic upper bound intuition">
  <mi>f</mi><mo>(</mo><mi>x</mi><mo>,</mo><mi>y</mi><mo>)</mo>
  <mo>&le;</mo>
  <mover accent="true"><mi>f</mi><mo>^</mo></mover>
  <mo>(</mo><mi>x</mi><mo>,</mo><mi>y</mi><mo>;</mo><mover accent="true"><mi>y</mi><mo>^</mo></mover><mo>)</mo><mo>.</mo>
</math>

이 때문에 objective-aware projection은 distance-only projection보다 낫다. Constraint repair가 objective의 local model과 정렬되기 때문이다. 다만 이 주장은 local하고 assumption-dependent하다. 임의의 nonconvex NLP에서 global optimality를 보장한다고 읽으면 안 된다.

## QP subproblem solver: modified Chambolle-Pock

각 projection subproblem은 primal-dual Chambolle-Pock style iteration으로 풀린다. Dual variables는 equality와 inequality violation에 반응하고, primal variable은 objective 방향으로 움직이면서 box constraint 안으로 projection된다.

대표적인 dual update는 다음과 같다.

<math display="block" aria-label="Primal dual update">
  <msup><mi>&lambda;</mi><mrow><mi>t</mi><mo>+</mo><mn>1</mn></mrow></msup>
  <mo>=</mo>
  <msup><mi>&lambda;</mi><mi>t</mi></msup>
  <mo>+</mo><mi>&sigma;</mi><mo>(</mo><mi>A</mi><msup><mover accent="true"><mi>y</mi><mo>&OverBar;</mo></mover><mi>t</mi></msup><mo>-</mo><mi>b</mi><mo>)</mo><mo>,</mo>
  <mspace width="0.6em"></mspace>
  <msup><mi>&mu;</mi><mrow><mi>t</mi><mo>+</mo><mn>1</mn></mrow></msup>
  <mo>=</mo>
  <mi>max</mi><mo>{</mo><mn>0</mn><mo>,</mo><msup><mi>&mu;</mi><mi>t</mi></msup><mo>+</mo><mi>&sigma;</mi><mo>(</mo><mi>C</mi><msup><mover accent="true"><mi>y</mi><mo>&OverBar;</mo></mover><mi>t</mi></msup><mo>-</mo><mi>d</mi><mo>)</mo><mo>}</mo><mo>.</mo>
</math>

Primal update에는 다음 행렬이 들어간다.

<math display="block" aria-label="Diagonal inverse structure">
  <mi>P</mi><mo>=</mo><msup><mrow><mo>(</mo><mi>I</mi><mo>+</mo><mi>&tau;</mi><mi>Q</mi><mo>)</mo></mrow><mrow><mo>-</mo><mn>1</mn></mrow></msup><mo>.</mo>
</math>

여기서 <math><mi>Q</mi></math>가 diagonal이므로 inverse는 dense matrix inverse가 아니라 elementwise division이 된다. 이것이 inversion-free design의 실질적 의미다. Projection layer 안에서 많은 primal-dual step을 돌려도 큰 linear system을 반복적으로 풀 필요가 없다.

## Projection layer를 어떻게 미분하는가?

Projection layer 내부의 Chambolle-Pock iteration을 그대로 automatic differentiation하면 모든 iteration을 unroll해야 하므로 memory와 시간이 커진다. NLPOpt-Net은 solver의 fixed point에서 implicit differentiation을 사용한다.

Fixed point를

<math display="block" aria-label="Fixed point equation">
  <msup><mi>z</mi><mo>*</mo></msup><mo>=</mo><mi>F</mi><mo>(</mo><msup><mi>z</mi><mo>*</mo></msup><mo>;</mo><mi>w</mi><mo>)</mo><mo>,</mo>
  <mspace width="0.6em"></mspace>
  <mi>w</mi><mo>=</mo><mi>M</mi><mo>(</mo><mi>x</mi><mo>,</mo><mover accent="true"><mi>z</mi><mo>^</mo></mover><mo>)</mo>
</math>

라고 쓰자. 여기서 <math><mi>w</mi></math>는 QP data다. Residual을

<math display="block" aria-label="Fixed point residual">
  <mi>G</mi><mo>(</mo><mi>z</mi><mo>,</mo><mi>w</mi><mo>)</mo>
  <mo>=</mo>
  <mi>F</mi><mo>(</mo><mi>z</mi><mo>;</mo><mi>w</mi><mo>)</mo><mo>-</mo><mi>z</mi>
</math>

로 두면, backward pass는 다음과 같은 adjoint linear system을 푸는 형태가 된다.

<math display="block" aria-label="Implicit differentiation adjoint system">
  <msup><mrow><mo>(</mo><mi>I</mi><mo>-</mo><msub><mi>J</mi><mi>F</mi></msub><mo>(</mo><msup><mi>z</mi><mo>*</mo></msup><mo>)</mo><mo>)</mo></mrow><mi>T</mi></msup>
  <mi>v</mi>
  <mo>=</mo>
  <msub><mi>g</mi><mi>z</mi></msub><mo>.</mo>
</math>

즉 forward에서는 CP solver로 projection을 계산하고, backward에서는 fixed-point implicit differentiation으로 gradient를 계산한다. 이는 solver unrolling 비용을 줄이기 위한 custom VJP route로 이해할 수 있다.

## 실험 결과를 어떻게 읽어야 하는가?

논문은 convex QP, convex QCQP, convex NLP, simple nonconvex NLP를 실험한다. 중요한 패턴은 convex setting에서 NLPOpt-Net이 solver-level objective에 가깝게 접근하면서 주요 table에서 equality와 inequality violation을 0으로 보고한다는 점이다. Convex QP case에서는 OSQP와 같은 objective value를 얻고, soft-constrained NN이나 DC3보다 violation과 objective gap이 작게 보고된다.

Nonlinear case에서는 여러 projection layer를 사용하므로 inference cost가 커진다. 이는 자연스러운 tradeoff다. Plain feedforward predictor보다 더 강한 feasibility repair를 얻는 대신, inference 과정에서 linearize-and-solve polishing step을 여러 번 수행한다.

Nonconvex result는 조심해서 읽어야 한다. Architecture가 clean convex case 밖에서도 작동할 수 있다는 유용한 empirical evidence이지만, general nonconvex guarantee는 아니다. 이론적 설명은 기본적으로 convexity, regularity, local approximation quality, solver accuracy에 의존한다.

## 비판적 평가

가장 강한 기여는 neural network 안에 실제 constrained optimization operation을 넣되, 이를 layer로 사용할 수 있을 만큼 가볍게 만든 설계다. Soft penalty보다 feasibility mechanism이 직접적이고, Euclidean projection보다 objective를 덜 망가뜨릴 가능성이 높다. 또한 classic differentiable QP layer와 비교하면 nonlinear constraint를 sequential local QP projection으로 다루려 한다.

하지만 한계도 분명하다.

첫째, "guaranteed feasibility"는 조건부다. Affine constraint와 exact solve에서는 강하다. 그러나 nonlinear constraint에서는 finite projection depth, finite Chambolle-Pock iterations, linearization error가 모두 영향을 준다. 실제 표현은 feasibility within tolerance에 가깝다.

둘째, convexity와 regularity assumption이 핵심이다. Convex objective와 constraint, affine equality constraint, Lipschitz gradient, feasible instances, well-behaved KKT system은 단순한 기술 조건이 아니라 이론적 claim을 떠받치는 구조다.

셋째, diagonal Hessian approximation은 계산상 타협이다. Update를 싸게 만들지만 cross-variable curvature를 버린다. 변수 간 coupling이 강한 NLP에서는 projection direction이 부정확해질 수 있고, 더 많은 projection layer나 solver iteration이 필요할 수 있다.

따라서 이 논문을 "neural network가 NLP를 직접 푼다"라고 설명하는 것은 부정확하다. 더 정확한 해석은 neural network가 warm start를 예측하고, objective-aware differentiable projection layer가 local constrained optimization을 수행하는 hybrid method라는 것이다. Solution-map learning, sequential QP approximation, primal-dual first-order solving, implicit differentiation을 규율 있게 결합한 점이 이 연구의 본질이다.

## References

Roy, B. N., Golder, R., & Hasan, M. M. (2026). NLPOpt-Net: A Learning Method for Nonlinear Optimization with Feasibility Guarantees. arXiv preprint arXiv:2605.00260.
