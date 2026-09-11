---
layout: post
title: "PEAR: Tangent-Space Projection for Decision-Focused Learning—and Where the Exact Gradient Claim Stops"
title_ko: "PEAR: 의사결정 중심 학습의 접공간 투영과 정확한 gradient 주장의 경계"
date: 2026-09-11
category: stochastic-nonlinear-optimization
category_label: "Mathematical Optimization"
research_group: algorithmic_reviews
research_category: stochastic-nonlinear-optimization
research_category_label: "Mathematical Optimization"
application_category: ""
application_category_label: ""
method_category: "stochastic-nonlinear-optimization"
method_category_label: "Mathematical Optimization"
paper_title: "Decision-Focused Learning via Tangent-Space Projection of Prediction Error"
authors: "Junhyeong Lee, Sangjin Jin, and Yongjae Lee"
venue: "ICML"
year: "2026"
doi: ""
arxiv: ""
source_url: ""
tags:
  - "decision-focused learning"
  - "predict-then-optimize"
  - "tangent-space projection"
  - "KKT sensitivity"
  - "quadratic programming"
  - "linear programming"
excerpt: "PEAR turns the local regret gradient of a strictly convex predict-then-optimize problem into a curvature-scaled tangent-space projection of prediction error. The theorem is clean, but the LP heuristic and covariance-dependent portfolio experiment sit outside its exact scope."
excerpt_ko: "PEAR는 strictly convex predict-then-optimize 문제의 local regret gradient를 curvature-scaled tangent-space projection으로 바꾼다. 정리는 깔끔하지만 LP heuristic과 covariance-dependent portfolio 실험은 그 정확한 적용 범위를 벗어난다."
language: "en-ko"
has_korean_note: false
---

## The theorem is cleaner than the method's broadest claims

*Decision-Focused Learning via Tangent-Space Projection of Prediction Error* is interesting because it does not introduce another neural architecture. It reinterprets the gradient in decision-focused learning (DFL) geometrically. Under a strictly convex optimization model and a locally fixed active set, differentiating the solver reduces to two operations: rescale the prediction error by objective curvature, then project it onto the tangent space of the active constraints.

That result is clean. It says that DFL need not abandon prediction error; it can filter that error through downstream decision geometry. But the exact statement has a narrower scope than the full method and experiments. The linear-programming version adds quadratic smoothing and a normal-space injection, so its update is no longer the true gradient of the original LP regret. The portfolio QP also lets the predicted returns determine the covariance matrix, while the released PEAR backward pass stops the covariance gradient. The theorem remains valid. The issue is that some experimental claims extend beyond the problem covered by the theorem.

## The predict-then-optimize problem

Let <math><mi>x</mi></math> be observed features and <math><mi>c</mi><mo>&isin;</mo><msup><mi>&Ropf;</mi><mi>n</mi></msup></math> the unknown objective coefficient. A neural network predicts

<math display="block" aria-label="Predicted cost parameter">
  <mover accent="true"><mi>c</mi><mo>^</mo></mover>
  <mo>=</mo><msub><mi>f</mi><mi>&theta;</mi></msub><mo>(</mo><mi>x</mi><mo>)</mo><mo>,</mo>
</math>

and the predicted coefficient is passed to an optimization problem:

<math display="block" aria-label="Predict then optimize problem">
  <msup><mi>z</mi><mo>*</mo></msup><mo>(</mo><mover accent="true"><mi>c</mi><mo>^</mo></mover><mo>)</mo>
  <mo>=</mo>
  <munder><mo>arg min</mo><mi>z</mi></munder>
  <mrow><mo>[</mo><mi>&phi;</mi><mo>(</mo><mi>z</mi><mo>)</mo><mo>+</mo><msup><mover accent="true"><mi>c</mi><mo>^</mo></mover><mo>&top;</mo></msup><mi>z</mi><mo>]</mo></mrow>
  <mspace width="0.8em"/><mtext>subject to</mtext><mspace width="0.5em"/>
  <mi>A</mi><mi>z</mi><mo>=</mo><mi>b</mi><mo>,</mo>
  <mspace width="0.4em"/><mi>G</mi><mi>z</mi><mo>&le;</mo><mi>h</mi><mo>.</mo>
</math>

Ordinary prediction learning minimizes a loss such as

<math display="block" aria-label="Mean squared prediction loss">
  <msub><mi>L</mi><mtext>MSE</mtext></msub>
  <mo>=</mo><mfrac><mn>1</mn><mn>2</mn></mfrac>
  <msup><mrow><mo>&Vert;</mo><mover accent="true"><mi>c</mi><mo>^</mo></mover><mo>&minus;</mo><mi>c</mi><mo>&Vert;</mo></mrow><mn>2</mn></msup><mo>.</mo>
</math>

DFL instead evaluates the decision made with the prediction under the true coefficient:

<math display="block" aria-label="Decision regret">
  <mi mathvariant="script">R</mi><mo>(</mo><mover accent="true"><mi>c</mi><mo>^</mo></mover><mo>;</mo><mi>c</mi><mo>)</mo>
  <mo>=</mo>
  <mi>&phi;</mi><mo>(</mo><msup><mi>z</mi><mo>*</mo></msup><mo>(</mo><mover accent="true"><mi>c</mi><mo>^</mo></mover><mo>)</mo><mo>)</mo>
  <mo>+</mo><msup><mi>c</mi><mo>&top;</mo></msup><msup><mi>z</mi><mo>*</mo></msup><mo>(</mo><mover accent="true"><mi>c</mi><mo>^</mo></mover><mo>)</mo>
  <mo>&minus;</mo>
  <mrow><mo>[</mo><mi>&phi;</mi><mo>(</mo><msup><mi>z</mi><mo>*</mo></msup><mo>(</mo><mi>c</mi><mo>)</mo><mo>)</mo>
  <mo>+</mo><msup><mi>c</mi><mo>&top;</mo></msup><msup><mi>z</mi><mo>*</mo></msup><mo>(</mo><mi>c</mi><mo>)</mo><mo>]</mo></mrow><mo>.</mo>
</math>

The difficult term in backpropagation is the solution sensitivity <math><mo>&part;</mo><msup><mi>z</mi><mo>*</mo></msup><mo>/</mo><mo>&part;</mo><mover accent="true"><mi>c</mi><mo>^</mo></mover></math>. Differentiable optimization layers obtain it from a KKT system, surrogate methods replace the regret, and perturbation methods repeatedly solve nearby optimization problems. PEAR attacks this sensitivity term directly.

## Why only tangent error changes a decision

Consider the constraint <math><msub><mi>z</mi><mn>1</mn></msub><mo>+</mo><msub><mi>z</mi><mn>2</mn></msub><mo>=</mo><mn>1</mn></math>. Feasible decisions lie on a line. The error direction <math><mo>(</mo><mn>1</mn><mo>,</mo><mo>&minus;</mo><mn>1</mn><mo>)</mo></math> runs along that line and can change the optimizer. The direction <math><mo>(</mo><mn>1</mn><mo>,</mo><mn>1</mn><mo>)</mo></math> is normal to it. Adding the latter to the objective coefficients only adds the same constant to every feasible objective value:

<math display="block" aria-label="Normal objective shift is constant on the feasible set">
  <mo>(</mo><msub><mi>c</mi><mn>1</mn></msub><mo>+</mo><mn>1</mn><mo>)</mo><msub><mi>z</mi><mn>1</mn></msub>
  <mo>+</mo><mo>(</mo><msub><mi>c</mi><mn>2</mn></msub><mo>+</mo><mn>1</mn><mo>)</mo><msub><mi>z</mi><mn>2</mn></msub>
  <mo>=</mo><msub><mi>c</mi><mn>1</mn></msub><msub><mi>z</mi><mn>1</mn></msub>
  <mo>+</mo><msub><mi>c</mi><mn>2</mn></msub><msub><mi>z</mi><mn>2</mn></msub><mo>+</mo><mn>1</mn><mo>.</mo>
</math>

The prediction error can therefore be large in Euclidean norm yet irrelevant to the decision.

At the current optimum, collect the equality constraints and active inequalities in

<math display="block" aria-label="Active constraint Jacobian">
  <mi>J</mi><mo>=</mo>
  <mrow><mo>[</mo><mtable><mtr><mtd><mi>A</mi></mtd></mtr><mtr><mtd><msub><mi>G</mi><mi mathvariant="script">A</mi></msub></mtd></mtr></mtable><mo>]</mo></mrow><mo>.</mo>
</math>

A locally feasible displacement <math><mi>d</mi><mi>z</mi></math> must satisfy <math><mi>J</mi><mi>d</mi><mi>z</mi><mo>=</mo><mn>0</mn></math>. Hence the tangent and normal spaces are

<math display="block" aria-label="Tangent and normal spaces">
  <mi mathvariant="script">T</mi><mo>=</mo><mi>ker</mi><mo>(</mo><mi>J</mi><mo>)</mo><mo>,</mo>
  <mspace width="1em"/>
  <mi mathvariant="script">N</mi><mo>=</mo><mi>range</mi><mo>(</mo><msup><mi>J</mi><mo>&top;</mo></msup><mo>)</mo><mo>.</mo>
</math>

PEAR keeps the part of prediction error that can move the decision along <math><mi mathvariant="script">T</mi></math>.

## KKT sensitivity becomes a curvature-aware projection

Suppose the active set stays fixed in a neighborhood of the current solution. Locally, the KKT conditions are

<math display="block" aria-label="Local KKT conditions">
  <mo>&nabla;</mo><mi>&phi;</mi><mo>(</mo><msup><mi>z</mi><mo>*</mo></msup><mo>)</mo>
  <mo>+</mo><mover accent="true"><mi>c</mi><mo>^</mo></mover>
  <mo>+</mo><msup><mi>J</mi><mo>&top;</mo></msup><msup><mi>y</mi><mo>*</mo></msup><mo>=</mo><mn>0</mn><mo>,</mo>
  <mspace width="0.8em"/>
  <mi>J</mi><msup><mi>z</mi><mo>*</mo></msup><mo>=</mo><mover><mi>b</mi><mo>~</mo></mover><mo>.</mo>
</math>

Let <math><mi>H</mi><mo>=</mo><msup><mo>&nabla;</mo><mn>2</mn></msup><mi>&phi;</mi><mo>(</mo><msup><mi>z</mi><mo>*</mo></msup><mo>)</mo></math>. Differentiating the KKT system gives

<math display="block" aria-label="Differentiated KKT system">
  <mrow><mo>[</mo><mtable>
    <mtr><mtd><mi>H</mi></mtd><mtd><msup><mi>J</mi><mo>&top;</mo></msup></mtd></mtr>
    <mtr><mtd><mi>J</mi></mtd><mtd><mn>0</mn></mtd></mtr>
  </mtable><mo>]</mo></mrow>
  <mrow><mo>[</mo><mtable>
    <mtr><mtd><mi>d</mi><mi>z</mi></mtd></mtr>
    <mtr><mtd><mi>d</mi><mi>y</mi></mtd></mtr>
  </mtable><mo>]</mo></mrow>
  <mo>=</mo>
  <mrow><mo>[</mo><mtable>
    <mtr><mtd><mo>&minus;</mo><mi>d</mi><mover accent="true"><mi>c</mi><mo>^</mo></mover></mtd></mtr>
    <mtr><mtd><mn>0</mn></mtd></mtr>
  </mtable><mo>]</mo></mrow><mo>.</mo>
</math>

Eliminating the dual displacement with a Schur complement yields

<math display="block" aria-label="Curvature scaled tangent projection operator">
  <mi>d</mi><mi>z</mi><mo>=</mo><mo>&minus;</mo><msub><mi>P</mi><mi>H</mi></msub><mi>d</mi><mover accent="true"><mi>c</mi><mo>^</mo></mover><mo>,</mo>
  <mspace width="0.8em"/>
  <msub><mi>P</mi><mi>H</mi></msub>
  <mo>=</mo><msup><mi>H</mi><mrow><mo>&minus;</mo><mn>1</mn></mrow></msup>
  <mo>&minus;</mo>
  <msup><mi>H</mi><mrow><mo>&minus;</mo><mn>1</mn></mrow></msup><msup><mi>J</mi><mo>&top;</mo></msup>
  <msup><mrow><mo>(</mo><mi>J</mi><msup><mi>H</mi><mrow><mo>&minus;</mo><mn>1</mn></mrow></msup><msup><mi>J</mi><mo>&top;</mo></msup><mo>)</mo></mrow><mrow><mo>&minus;</mo><mn>1</mn></mrow></msup>
  <mi>J</mi><msup><mi>H</mi><mrow><mo>&minus;</mo><mn>1</mn></mrow></msup><mo>.</mo>
</math>

Define

<math display="block" aria-label="H orthogonal tangent projector">
  <msub><mi>&Pi;</mi><mi>H</mi></msub>
  <mo>=</mo><mi>I</mi>
  <mo>&minus;</mo><msup><mi>H</mi><mrow><mo>&minus;</mo><mn>1</mn></mrow></msup><msup><mi>J</mi><mo>&top;</mo></msup>
  <msup><mrow><mo>(</mo><mi>J</mi><msup><mi>H</mi><mrow><mo>&minus;</mo><mn>1</mn></mrow></msup><msup><mi>J</mi><mo>&top;</mo></msup><mo>)</mo></mrow><mrow><mo>&minus;</mo><mn>1</mn></mrow></msup><mi>J</mi><mo>.</mo>
</math>

Then <math><msub><mi>P</mi><mi>H</mi></msub><mo>=</mo><msub><mi>&Pi;</mi><mi>H</mi></msub><msup><mi>H</mi><mrow><mo>&minus;</mo><mn>1</mn></mrow></msup></math>. This distinction matters. <math><msub><mi>P</mi><mi>H</mi></msub></math> is not generally a Euclidean projector. It first applies inverse-curvature scaling, then an <math><mi>H</mi></math>-orthogonal projection onto <math><mi>ker</mi><mo>(</mo><mi>J</mi><mo>)</mo></math>. Only when <math><mi>H</mi><mo>=</mo><mi>&alpha;</mi><mi>I</mi></math> does the geometry essentially reduce to Euclidean projection.

## The regret gradient collapses to projected prediction error

Write the prediction error as <math><mi>e</mi><mo>=</mo><mover accent="true"><mi>c</mi><mo>^</mo></mover><mo>&minus;</mo><mi>c</mi></math>. Chain rule gives

<math display="block" aria-label="Regret gradient before KKT simplification">
  <msub><mo>&nabla;</mo><mover accent="true"><mi>c</mi><mo>^</mo></mover></msub><mi mathvariant="script">R</mi>
  <mo>=</mo><mo>&minus;</mo><msub><mi>P</mi><mi>H</mi></msub>
  <mrow><mo>[</mo><mo>&nabla;</mo><mi>&phi;</mi><mo>(</mo><msup><mi>z</mi><mo>*</mo></msup><mo>)</mo><mo>+</mo><mi>c</mi><mo>]</mo></mrow><mo>.</mo>
</math>

Stationarity implies

<math display="block" aria-label="KKT stationarity substitution">
  <mo>&nabla;</mo><mi>&phi;</mi><mo>(</mo><msup><mi>z</mi><mo>*</mo></msup><mo>)</mo><mo>+</mo><mi>c</mi>
  <mo>=</mo><mo>&minus;</mo><mi>e</mi><mo>&minus;</mo><msup><mi>J</mi><mo>&top;</mo></msup><msup><mi>y</mi><mo>*</mo></msup><mo>.</mo>
</math>

Because <math><msub><mi>P</mi><mi>H</mi></msub><msup><mi>J</mi><mo>&top;</mo></msup><mo>=</mo><mn>0</mn></math>, the dual term vanishes:

<math display="block" aria-label="PEAR exact local regret gradient">
  <msub><mo>&nabla;</mo><mover accent="true"><mi>c</mi><mo>^</mo></mover></msub><mi mathvariant="script">R</mi>
  <mo>=</mo><msub><mi>P</mi><mi>H</mi></msub>
  <mo>(</mo><mover accent="true"><mi>c</mi><mo>^</mo></mover><mo>&minus;</mo><mi>c</mi><mo>)</mo><mo>.</mo>
</math>

The MSE gradient is the raw error <math><mi>e</mi></math>. The PEAR gradient is that same error after removing directions that are locally invisible to the optimizer, with the curvature of the objective setting the metric. This is the paper's strongest conceptual contribution.

## PEAR is a custom backward rule, not a new scalar loss

The released implementation clarifies an easy point to miss from the mathematical presentation. The forward value of the QP projection loss is still

<math display="block" aria-label="PEAR forward value">
  <msub><mi>L</mi><mtext>forward</mtext></msub>
  <mo>=</mo><mfrac><mn>1</mn><mn>2</mn></mfrac>
  <msup><mrow><mo>&Vert;</mo><msub><mi>&mu;</mi><mtext>pred</mtext></msub><mo>&minus;</mo><msub><mi>&mu;</mi><mtext>true</mtext></msub><mo>&Vert;</mo></mrow><mn>2</mn></msup><mo>.</mo>
</math>

The backward method overrides the derivative and returns the projected error. PEAR is therefore better described as a gradient transformation than as a conventional scalar loss whose automatic derivative produces the update.

For each training sample, the method solves the forward optimization problem, identifies active constraints, and forms <math><mi>J</mi></math>. It does not need to materialize the full <math><mi>n</mi><mo>&times;</mo><mi>n</mi></math> matrix <math><msub><mi>P</mi><mi>H</mi></msub></math>. With <math><mi>k</mi></math> active constraints, it computes

<math display="block" aria-label="PEAR Schur complement solve">
  <msub><mi>x</mi><mi>H</mi></msub><mo>=</mo><msup><mi>H</mi><mrow><mo>&minus;</mo><mn>1</mn></mrow></msup><mi>e</mi><mo>,</mo>
  <mspace width="0.6em"/>
  <mo>(</mo><mi>J</mi><msup><mi>H</mi><mrow><mo>&minus;</mo><mn>1</mn></mrow></msup><msup><mi>J</mi><mo>&top;</mo></msup><mo>)</mo><mi>v</mi>
  <mo>=</mo><mi>J</mi><msup><mi>H</mi><mrow><mo>&minus;</mo><mn>1</mn></mrow></msup><mi>e</mi><mo>,</mo>
</math>

then returns

<math display="block" aria-label="PEAR gradient signal">
  <mi>g</mi><mo>=</mo><msup><mi>H</mi><mrow><mo>&minus;</mo><mn>1</mn></mrow></msup><mi>e</mi>
  <mo>&minus;</mo><msup><mi>H</mi><mrow><mo>&minus;</mo><mn>1</mn></mrow></msup><msup><mi>J</mi><mo>&top;</mo></msup><mi>v</mi><mo>.</mo>
</math>

The central solve is <math><mi>k</mi><mo>&times;</mo><mi>k</mi></math>, which can be attractive when <math><mi>k</mi><mo>&ll;</mo><mi>n</mi></math> and the Hessian has exploitable structure.

## The exact theorem is local and strictly convex

The derivation needs three strong conditions. The Hessian must be positive definite, the active constraint Jacobian must satisfy the linear independence constraint qualification, and active inequalities must satisfy strict complementarity. These conditions support a locally stable active set and differentiable solution map.

The result is therefore local. Crossing an active-set boundary changes <math><mi>J</mi></math>, and the solution map can become nonsmooth. Degenerate or weakly active constraints also weaken the argument. The theorem says something precise about a smooth neighborhood of a strictly convex problem; it is not a global differentiability result for arbitrary mathematical programs.

## The LP version is a modified problem, then a heuristic

For a linear program, <math><mi>&phi;</mi><mo>(</mo><mi>z</mi><mo>)</mo><mo>=</mo><mn>0</mn></math> and <math><mi>H</mi><mo>=</mo><mn>0</mn></math>, so the inverse Hessian in PEAR does not exist. More fundamentally, an LP optimizer is piecewise constant in the cost vector. Within one normal cone the optimal vertex does not move; at a boundary it may jump. The classical derivative is thus zero almost everywhere or undefined at the transition.

The paper adds quadratic smoothing,

<math display="block" aria-label="Quadratically smoothed LP objective">
  <mi>&phi;</mi><mo>(</mo><mi>z</mi><mo>)</mo>
  <mo>=</mo><mfrac><mi>&lambda;</mi><mn>2</mn></mfrac><msup><mrow><mo>&Vert;</mo><mi>z</mi><mo>&Vert;</mo></mrow><mn>2</mn></msup><mo>,</mo>
  <mspace width="0.7em"/><mi>H</mi><mo>=</mo><mi>&lambda;</mi><mi>I</mi><mo>.</mo>
</math>

This produces a useful gradient, but it is the gradient of the smoothed problem rather than the true regret gradient of the original LP.

The implementation goes further by injecting a normalized normal component:

<math display="block" aria-label="Normal space injection for LP training">
  <mi>n</mi><mo>=</mo><msup><mi>&lambda;</mi><mrow><mo>&minus;</mo><mn>1</mn></mrow></msup><msup><mi>J</mi><mo>&top;</mo></msup><mi>v</mi><mo>,</mo>
  <mspace width="0.7em"/>
  <msub><mi>g</mi><mtext>inj</mtext></msub>
  <mo>=</mo><mi>g</mi><mo>+</mo><mi>&beta;</mi>
  <mfrac><mrow><mo>&Vert;</mo><mi>g</mi><mo>&Vert;</mo></mrow><mrow><mo>&Vert;</mo><mi>n</mi><mo>&Vert;</mo></mrow></mfrac><mi>n</mi><mo>.</mo>
</math>

This is pragmatically understandable: a tangent signal can be too weak to escape an LP plateau. It is also conceptually ironic. The theorem removes the normal component as decision-irrelevant, while the LP training rule adds it back to obtain a useful update. Once injected, <math><msub><mi>g</mi><mtext>inj</mtext></msub></math> is not the regret gradient.

The method should therefore be described in three layers:

- Strictly convex QP: an exact local regret-gradient result under the stated regularity assumptions.
- Quadratically smoothed LP: a gradient for a modified optimization problem.
- Smoothed LP with normal injection: a heuristic training direction.

Those layers can all be useful. They should not share the same exact-gradient label.

## The portfolio experiment drops a predicted covariance path

The portfolio problem is

<math display="block" aria-label="Mean variance portfolio problem">
  <munder><mo>min</mo><mi>w</mi></munder>
  <mspace width="0.5em"/>
  <mfrac><mi>&lambda;</mi><mn>2</mn></mfrac><msup><mi>w</mi><mo>&top;</mo></msup><mi>&Sigma;</mi><mi>w</mi>
  <mo>&minus;</mo><msup><mi>&mu;</mi><mo>&top;</mo></msup><mi>w</mi>
  <mspace width="0.8em"/><mtext>subject to</mtext><mspace width="0.5em"/>
  <msup><mn>1</mn><mo>&top;</mo></msup><mi>w</mi><mo>=</mo><mn>1</mn><mo>,</mo>
  <mspace width="0.4em"/><mi>w</mi><mo>&ge;</mo><mn>0</mn><mo>.</mo>
</math>

The theorem treats <math><mi>&phi;</mi><mo>(</mo><mi>w</mi><mo>)</mo><mo>=</mo><mi>&lambda;</mi><msup><mi>w</mi><mo>&top;</mo></msup><mi>&Sigma;</mi><mi>w</mi><mo>/</mo><mn>2</mn></math> as known and prediction-independent, while the model predicts only the linear coefficient <math><mo>&minus;</mo><mi>&mu;</mi></math>. In the experiment, however, the network predicts a 21-day return path. Both its mean and a covariance matrix constructed from historical and predicted returns enter the optimizer. The actual decision is therefore <math><msup><mi>w</mi><mo>*</mo></msup><mo>(</mo><mover accent="true"><mi>&mu;</mi><mo>^</mo></mover><mo>,</mo><mover accent="true"><mi>&Sigma;</mi><mo>^</mo></mover><mo>)</mo></math>.

The full derivative with respect to predicted returns <math><mover accent="true"><mi>r</mi><mo>^</mo></mover></math> has two paths:

<math display="block" aria-label="Mean and covariance gradient paths">
  <mfrac>
    <mrow><mi>d</mi><mi mathvariant="script">R</mi></mrow>
    <mrow><mi>d</mi><mover accent="true"><mi>r</mi><mo>^</mo></mover></mrow>
  </mfrac>
  <mo>=</mo>
  <mfrac><mrow><mo>&part;</mo><mi mathvariant="script">R</mi></mrow><mrow><mo>&part;</mo><mover accent="true"><mi>&mu;</mi><mo>^</mo></mover></mrow></mfrac>
  <mfrac><mrow><mo>&part;</mo><mover accent="true"><mi>&mu;</mi><mo>^</mo></mover></mrow><mrow><mo>&part;</mo><mover accent="true"><mi>r</mi><mo>^</mo></mover></mrow></mfrac>
  <mo>+</mo>
  <mfrac><mrow><mo>&part;</mo><mi mathvariant="script">R</mi></mrow><mrow><mo>&part;</mo><mover accent="true"><mi>&Sigma;</mi><mo>^</mo></mover></mrow></mfrac>
  <mfrac><mrow><mo>&part;</mo><mover accent="true"><mi>&Sigma;</mi><mo>^</mo></mover></mrow><mrow><mo>&part;</mo><mover accent="true"><mi>r</mi><mo>^</mo></mover></mrow></mfrac><mo>.</mo>
</math>

In the released PEAR backward implementation, the projected gradient is returned for the predicted mean and `None` is returned for the predicted covariance. The covariance path is stopped. PEAR therefore computes a partial regret gradient with respect to the mean while treating the current predicted covariance as fixed. That is not the total derivative of the optimization problem used in the experiment.

This difference also complicates baseline comparisons. A differentiable QP layer receives both the predicted mean and a covariance factor and can propagate through both. PEAR uses less gradient information. Its performance may reflect the projection geometry, the covariance stop-gradient acting as regularization, or both. A direct ablation is needed to separate them.

## Active-set numerics and computational cost remain conditional

PEAR identifies binding inequalities from a finite-tolerance primal-dual solution. When <math><msub><mi>G</mi><mi>i</mi></msub><msup><mi>z</mi><mo>*</mo></msup><mo>&minus;</mo><msub><mi>h</mi><mi>i</mi></msub><mo>&approx;</mo><mn>0</mn></math>, membership in the active set can change with the numerical threshold. Near degeneracy, <math><mi>J</mi></math> may be unstable and <math><mi>J</mi><msup><mi>H</mi><mrow><mo>&minus;</mo><mn>1</mn></mrow></msup><msup><mi>J</mi><mo>&top;</mo></msup></math> may be ill-conditioned. The claim that this route is more numerically stable than differentiating a solver is empirical, not a consequence of the theorem.

The cost advantage is conditional as well. A small active set and structured Hessian favor PEAR. If many assets have zero weight, many nonnegativity constraints are active and <math><mi>k</mi></math> can approach <math><mi>n</mi></math>. A dense covariance matrix still requires a factorization or solves with <math><mi>H</mi></math>. PEAR does not become cheap merely by writing the sensitivity as a smaller Schur system.

## What the experiments establish

The LP benchmarks are a 5-by-5 shortest-path problem and a 100-item knapsack. The polynomial degree of the feature-to-cost mapping increases from 2 to 8. PEAR and LAVA train on an LP relaxation for knapsack and are evaluated on the original integer problem.

The decision results are strong. For degree-8 knapsack, normalized regret is 2.285% for MSE, 0.763% for SPO+, and 0.437% for PEAR. PEAR also gives the best reported result for degree-8 shortest path at 4.246%. It does not win every setting: at degree 4, SPO+ records 0.761% and PEAR 0.774%. The broad phrase “best decision quality among all baselines” is therefore slightly stronger than the table supports.

The same qualification applies to computational efficiency. At shortest-path degree 8, MSE takes 6.1 seconds and PEAR 38.4 seconds. In the portfolio task, MSE takes 33.0 seconds and PEAR 122.3 seconds. PEAR is faster than QPTH at 147.6 seconds and CVXPYLayers at 321.9 seconds in that portfolio comparison, making it one of the faster decision-focused methods rather than the fastest baseline without qualification.

For portfolio optimization, PEAR reports the lowest normalized regret at 85.38%, a Sharpe ratio of 1.44 versus 0.92 for MSE and 1.15 for QPTH/CVXPYLayers, and the lowest maximum drawdown. The uncertainty is large across five seeds. Cumulative return is <math><mn>184.19</mn><mo>&PlusMinus;</mo><mn>86.24</mn><mo>%</mo></math> for PEAR and <math><mn>139.77</mn><mo>&PlusMinus;</mo><mn>115.74</mn><mo>%</mo></math> for QPTH. These results are promising but too variable to settle economic superiority, especially without the covariance-gradient ablation.

The constraint-shift experiment may be more revealing. Training and testing use different optimization geometries: a changed source-target direction for shortest path, a changed knapsack capacity, and short selling at test time after long-only portfolio training. MSE remains strong. Under the shortest-path direction shift at degree 8, MSE scores 14.00, PEAR 21.42, and SPO+ 43.40. DFL deliberately shapes prediction error around the training-time feasible geometry. When that geometry changes, its inductive bias can become a liability. This is not a side result; it identifies a real boundary between in-distribution decision quality and transfer across constraints.

## Assessment

The exact result is worth keeping. For a prediction-independent, strictly convex objective with a regular and locally fixed active set, the regret gradient is a curvature-scaled tangent-space projection of ordinary prediction error. The proof follows cleanly from KKT sensitivity and stationarity, and the interpretation makes DFL easier to reason about.

The practical method occupies a wider territory. The LP variant optimizes a smoothed surrogate and then injects a heuristic normal component. The portfolio experiment differentiates only the mean-return path even though predicted returns also determine covariance. Active-set identification and runtime gains depend on numerical tolerances, sparsity, and Hessian structure.

The right conclusion is not that the theorem is wrong. It is that the theorem, the LP training rule, and the covariance-dependent QP experiment should be reported as three distinct objects. PEAR's geometry is most convincing when those boundaries are explicit.

## Reference

Junhyeong Lee, Sangjin Jin, and Yongjae Lee. *Decision-Focused Learning via Tangent-Space Projection of Prediction Error*. ICML, 2026. A source URL, DOI, and arXiv identifier were not provided with the reviewed material.

<!-- ko -->

## 정리는 method의 가장 넓은 주장보다 깔끔하다

*Decision-Focused Learning via Tangent-Space Projection of Prediction Error*가 흥미로운 이유는 새로운 neural architecture를 제안해서가 아니다. 이 논문은 decision-focused learning(DFL)의 gradient를 기하학적으로 다시 해석한다. Strictly convex optimization model과 locally fixed active set 아래에서 solver differentiation은 두 단계로 줄어든다. Prediction error를 objective curvature로 rescale한 뒤 active constraint의 tangent space에 project한다.

이 결과는 깔끔하다. DFL은 prediction error를 버리는 것이 아니라 downstream decision geometry를 통해 filtering하는 것으로 이해할 수 있다. 그러나 정확한 정리의 범위는 전체 method와 experiment보다 좁다. LP 버전은 quadratic smoothing과 normal-space injection을 추가하므로 update가 원래 LP regret의 true gradient가 아니다. Portfolio QP에서는 predicted return이 covariance matrix까지 결정하지만 공개된 PEAR backward는 covariance gradient를 끊는다. 정리 자체는 유효하다. 문제는 일부 experimental claim이 정리가 다루는 문제보다 넓다는 데 있다.

## Predict-then-optimize 문제

관측 feature를 <math><mi>x</mi></math>, 알 수 없는 objective coefficient를 <math><mi>c</mi><mo>&isin;</mo><msup><mi>&Ropf;</mi><mi>n</mi></msup></math>이라고 하자. Neural network는

<math display="block" aria-label="예측된 cost parameter">
  <mover accent="true"><mi>c</mi><mo>^</mo></mover>
  <mo>=</mo><msub><mi>f</mi><mi>&theta;</mi></msub><mo>(</mo><mi>x</mi><mo>)</mo>
</math>

를 예측하고, 그 coefficient를 optimization problem에 넣는다.

<math display="block" aria-label="Predict then optimize 문제">
  <msup><mi>z</mi><mo>*</mo></msup><mo>(</mo><mover accent="true"><mi>c</mi><mo>^</mo></mover><mo>)</mo>
  <mo>=</mo>
  <munder><mo>arg min</mo><mi>z</mi></munder>
  <mrow><mo>[</mo><mi>&phi;</mi><mo>(</mo><mi>z</mi><mo>)</mo><mo>+</mo><msup><mover accent="true"><mi>c</mi><mo>^</mo></mover><mo>&top;</mo></msup><mi>z</mi><mo>]</mo></mrow>
  <mspace width="0.8em"/><mtext>subject to</mtext><mspace width="0.5em"/>
  <mi>A</mi><mi>z</mi><mo>=</mo><mi>b</mi><mo>,</mo>
  <mspace width="0.4em"/><mi>G</mi><mi>z</mi><mo>&le;</mo><mi>h</mi><mo>.</mo>
</math>

일반적인 prediction learning은 다음과 같은 loss를 최소화한다.

<math display="block" aria-label="Mean squared prediction loss">
  <msub><mi>L</mi><mtext>MSE</mtext></msub>
  <mo>=</mo><mfrac><mn>1</mn><mn>2</mn></mfrac>
  <msup><mrow><mo>&Vert;</mo><mover accent="true"><mi>c</mi><mo>^</mo></mover><mo>&minus;</mo><mi>c</mi><mo>&Vert;</mo></mrow><mn>2</mn></msup><mo>.</mo>
</math>

DFL은 prediction으로 내린 decision을 true coefficient 아래에서 평가한다.

<math display="block" aria-label="의사결정 regret">
  <mi mathvariant="script">R</mi><mo>(</mo><mover accent="true"><mi>c</mi><mo>^</mo></mover><mo>;</mo><mi>c</mi><mo>)</mo>
  <mo>=</mo>
  <mi>&phi;</mi><mo>(</mo><msup><mi>z</mi><mo>*</mo></msup><mo>(</mo><mover accent="true"><mi>c</mi><mo>^</mo></mover><mo>)</mo><mo>)</mo>
  <mo>+</mo><msup><mi>c</mi><mo>&top;</mo></msup><msup><mi>z</mi><mo>*</mo></msup><mo>(</mo><mover accent="true"><mi>c</mi><mo>^</mo></mover><mo>)</mo>
  <mo>&minus;</mo>
  <mrow><mo>[</mo><mi>&phi;</mi><mo>(</mo><msup><mi>z</mi><mo>*</mo></msup><mo>(</mo><mi>c</mi><mo>)</mo><mo>)</mo>
  <mo>+</mo><msup><mi>c</mi><mo>&top;</mo></msup><msup><mi>z</mi><mo>*</mo></msup><mo>(</mo><mi>c</mi><mo>)</mo><mo>]</mo></mrow><mo>.</mo>
</math>

Backpropagation에서 어려운 항은 solution sensitivity <math><mo>&part;</mo><msup><mi>z</mi><mo>*</mo></msup><mo>/</mo><mo>&part;</mo><mover accent="true"><mi>c</mi><mo>^</mo></mover></math>다. Differentiable optimization layer는 KKT system에서 이를 구하고, surrogate method는 regret을 다른 loss로 대체하며, perturbation method는 주변 optimization problem을 여러 번 푼다. PEAR는 이 sensitivity term을 직접 공략한다.

## Tangent error만 decision을 바꾸는 이유

Constraint가 <math><msub><mi>z</mi><mn>1</mn></msub><mo>+</mo><msub><mi>z</mi><mn>2</mn></msub><mo>=</mo><mn>1</mn></math>이라고 하자. Feasible decision은 하나의 직선 위에 있다. Error direction <math><mo>(</mo><mn>1</mn><mo>,</mo><mo>&minus;</mo><mn>1</mn><mo>)</mo></math>은 그 직선을 따라가므로 optimizer를 바꿀 수 있다. 반면 <math><mo>(</mo><mn>1</mn><mo>,</mo><mn>1</mn><mo>)</mo></math>은 직선에 수직이다. 이 방향을 objective coefficient에 더하면 모든 feasible objective value에 같은 상수만 더해진다.

<math display="block" aria-label="Normal objective shift는 feasible set에서 상수다">
  <mo>(</mo><msub><mi>c</mi><mn>1</mn></msub><mo>+</mo><mn>1</mn><mo>)</mo><msub><mi>z</mi><mn>1</mn></msub>
  <mo>+</mo><mo>(</mo><msub><mi>c</mi><mn>2</mn></msub><mo>+</mo><mn>1</mn><mo>)</mo><msub><mi>z</mi><mn>2</mn></msub>
  <mo>=</mo><msub><mi>c</mi><mn>1</mn></msub><msub><mi>z</mi><mn>1</mn></msub>
  <mo>+</mo><msub><mi>c</mi><mn>2</mn></msub><msub><mi>z</mi><mn>2</mn></msub><mo>+</mo><mn>1</mn><mo>.</mo>
</math>

따라서 prediction error는 Euclidean norm으로 클 수 있지만 decision 관점에서는 아무 의미가 없을 수 있다.

현재 optimum에서 equality constraint와 active inequality를 모아 다음과 같이 쓴다.

<math display="block" aria-label="Active constraint Jacobian">
  <mi>J</mi><mo>=</mo>
  <mrow><mo>[</mo><mtable><mtr><mtd><mi>A</mi></mtd></mtr><mtr><mtd><msub><mi>G</mi><mi mathvariant="script">A</mi></msub></mtd></mtr></mtable><mo>]</mo></mrow><mo>.</mo>
</math>

Locally feasible displacement <math><mi>d</mi><mi>z</mi></math>는 <math><mi>J</mi><mi>d</mi><mi>z</mi><mo>=</mo><mn>0</mn></math>을 만족해야 한다. 따라서 tangent space와 normal space는

<math display="block" aria-label="Tangent space와 normal space">
  <mi mathvariant="script">T</mi><mo>=</mo><mi>ker</mi><mo>(</mo><mi>J</mi><mo>)</mo><mo>,</mo>
  <mspace width="1em"/>
  <mi mathvariant="script">N</mi><mo>=</mo><mi>range</mi><mo>(</mo><msup><mi>J</mi><mo>&top;</mo></msup><mo>)</mo><mo>.</mo>
</math>

PEAR는 prediction error 중 <math><mi mathvariant="script">T</mi></math>를 따라 decision을 실제로 움직일 수 있는 부분만 남긴다.

## KKT sensitivity는 curvature-aware projection이 된다

현재 solution 근방에서 active set이 유지된다고 하자. Local KKT condition은

<math display="block" aria-label="Local KKT condition">
  <mo>&nabla;</mo><mi>&phi;</mi><mo>(</mo><msup><mi>z</mi><mo>*</mo></msup><mo>)</mo>
  <mo>+</mo><mover accent="true"><mi>c</mi><mo>^</mo></mover>
  <mo>+</mo><msup><mi>J</mi><mo>&top;</mo></msup><msup><mi>y</mi><mo>*</mo></msup><mo>=</mo><mn>0</mn><mo>,</mo>
  <mspace width="0.8em"/>
  <mi>J</mi><msup><mi>z</mi><mo>*</mo></msup><mo>=</mo><mover><mi>b</mi><mo>~</mo></mover><mo>.</mo>
</math>

이다. <math><mi>H</mi><mo>=</mo><msup><mo>&nabla;</mo><mn>2</mn></msup><mi>&phi;</mi><mo>(</mo><msup><mi>z</mi><mo>*</mo></msup><mo>)</mo></math>라고 하고 KKT system을 미분하면

<math display="block" aria-label="미분한 KKT system">
  <mrow><mo>[</mo><mtable>
    <mtr><mtd><mi>H</mi></mtd><mtd><msup><mi>J</mi><mo>&top;</mo></msup></mtd></mtr>
    <mtr><mtd><mi>J</mi></mtd><mtd><mn>0</mn></mtd></mtr>
  </mtable><mo>]</mo></mrow>
  <mrow><mo>[</mo><mtable>
    <mtr><mtd><mi>d</mi><mi>z</mi></mtd></mtr>
    <mtr><mtd><mi>d</mi><mi>y</mi></mtd></mtr>
  </mtable><mo>]</mo></mrow>
  <mo>=</mo>
  <mrow><mo>[</mo><mtable>
    <mtr><mtd><mo>&minus;</mo><mi>d</mi><mover accent="true"><mi>c</mi><mo>^</mo></mover></mtd></mtr>
    <mtr><mtd><mn>0</mn></mtd></mtr>
  </mtable><mo>]</mo></mrow><mo>.</mo>
</math>

Schur complement로 dual displacement를 제거하면

<math display="block" aria-label="Curvature scaled tangent projection operator">
  <mi>d</mi><mi>z</mi><mo>=</mo><mo>&minus;</mo><msub><mi>P</mi><mi>H</mi></msub><mi>d</mi><mover accent="true"><mi>c</mi><mo>^</mo></mover><mo>,</mo>
  <mspace width="0.8em"/>
  <msub><mi>P</mi><mi>H</mi></msub>
  <mo>=</mo><msup><mi>H</mi><mrow><mo>&minus;</mo><mn>1</mn></mrow></msup>
  <mo>&minus;</mo>
  <msup><mi>H</mi><mrow><mo>&minus;</mo><mn>1</mn></mrow></msup><msup><mi>J</mi><mo>&top;</mo></msup>
  <msup><mrow><mo>(</mo><mi>J</mi><msup><mi>H</mi><mrow><mo>&minus;</mo><mn>1</mn></mrow></msup><msup><mi>J</mi><mo>&top;</mo></msup><mo>)</mo></mrow><mrow><mo>&minus;</mo><mn>1</mn></mrow></msup>
  <mi>J</mi><msup><mi>H</mi><mrow><mo>&minus;</mo><mn>1</mn></mrow></msup><mo>.</mo>
</math>

다음을 정의하자.

<math display="block" aria-label="H orthogonal tangent projector">
  <msub><mi>&Pi;</mi><mi>H</mi></msub>
  <mo>=</mo><mi>I</mi>
  <mo>&minus;</mo><msup><mi>H</mi><mrow><mo>&minus;</mo><mn>1</mn></mrow></msup><msup><mi>J</mi><mo>&top;</mo></msup>
  <msup><mrow><mo>(</mo><mi>J</mi><msup><mi>H</mi><mrow><mo>&minus;</mo><mn>1</mn></mrow></msup><msup><mi>J</mi><mo>&top;</mo></msup><mo>)</mo></mrow><mrow><mo>&minus;</mo><mn>1</mn></mrow></msup><mi>J</mi><mo>.</mo>
</math>

그러면 <math><msub><mi>P</mi><mi>H</mi></msub><mo>=</mo><msub><mi>&Pi;</mi><mi>H</mi></msub><msup><mi>H</mi><mrow><mo>&minus;</mo><mn>1</mn></mrow></msup></math>이다. 이 구분은 중요하다. <math><msub><mi>P</mi><mi>H</mi></msub></math> 자체는 일반적으로 Euclidean projector가 아니다. 먼저 inverse-curvature scaling을 하고, 그 뒤 <math><mi>ker</mi><mo>(</mo><mi>J</mi><mo>)</mo></math> 위로 <math><mi>H</mi></math>-orthogonal projection을 한다. <math><mi>H</mi><mo>=</mo><mi>&alpha;</mi><mi>I</mi></math>일 때만 geometry가 essentially Euclidean projection으로 줄어든다.

## Regret gradient는 projected prediction error로 줄어든다

Prediction error를 <math><mi>e</mi><mo>=</mo><mover accent="true"><mi>c</mi><mo>^</mo></mover><mo>&minus;</mo><mi>c</mi></math>라고 하자. Chain rule을 쓰면

<math display="block" aria-label="KKT 단순화 전 regret gradient">
  <msub><mo>&nabla;</mo><mover accent="true"><mi>c</mi><mo>^</mo></mover></msub><mi mathvariant="script">R</mi>
  <mo>=</mo><mo>&minus;</mo><msub><mi>P</mi><mi>H</mi></msub>
  <mrow><mo>[</mo><mo>&nabla;</mo><mi>&phi;</mi><mo>(</mo><msup><mi>z</mi><mo>*</mo></msup><mo>)</mo><mo>+</mo><mi>c</mi><mo>]</mo></mrow><mo>.</mo>
</math>

Stationarity에서

<math display="block" aria-label="KKT stationarity 대입">
  <mo>&nabla;</mo><mi>&phi;</mi><mo>(</mo><msup><mi>z</mi><mo>*</mo></msup><mo>)</mo><mo>+</mo><mi>c</mi>
  <mo>=</mo><mo>&minus;</mo><mi>e</mi><mo>&minus;</mo><msup><mi>J</mi><mo>&top;</mo></msup><msup><mi>y</mi><mo>*</mo></msup><mo>.</mo>
</math>

또 <math><msub><mi>P</mi><mi>H</mi></msub><msup><mi>J</mi><mo>&top;</mo></msup><mo>=</mo><mn>0</mn></math>이므로 dual term이 사라진다.

<math display="block" aria-label="PEAR의 정확한 local regret gradient">
  <msub><mo>&nabla;</mo><mover accent="true"><mi>c</mi><mo>^</mo></mover></msub><mi mathvariant="script">R</mi>
  <mo>=</mo><msub><mi>P</mi><mi>H</mi></msub>
  <mo>(</mo><mover accent="true"><mi>c</mi><mo>^</mo></mover><mo>&minus;</mo><mi>c</mi><mo>)</mo><mo>.</mo>
</math>

MSE gradient는 raw error <math><mi>e</mi></math>다. PEAR gradient는 같은 error에서 optimizer가 locally 볼 수 없는 방향을 제거하고 objective curvature로 metric을 조정한 것이다. 이것이 이 논문의 가장 강한 conceptual contribution이다.

## PEAR는 새로운 scalar loss보다 custom backward rule에 가깝다

공개된 implementation을 보면 수학적 설명에서 놓치기 쉬운 점이 드러난다. QP projection loss의 forward value는 여전히

<math display="block" aria-label="PEAR forward value">
  <msub><mi>L</mi><mtext>forward</mtext></msub>
  <mo>=</mo><mfrac><mn>1</mn><mn>2</mn></mfrac>
  <msup><mrow><mo>&Vert;</mo><msub><mi>&mu;</mi><mtext>pred</mtext></msub><mo>&minus;</mo><msub><mi>&mu;</mi><mtext>true</mtext></msub><mo>&Vert;</mo></mrow><mn>2</mn></msup><mo>.</mo>
</math>

이다. Backward method가 derivative를 override해 projected error를 반환한다. 따라서 PEAR는 automatic differentiation이 update를 만들어 내는 conventional scalar loss라기보다 gradient transformation이라고 부르는 편이 정확하다.

Training sample마다 forward optimization을 풀고 active constraint를 식별해 <math><mi>J</mi></math>를 만든다. Full <math><mi>n</mi><mo>&times;</mo><mi>n</mi></math> matrix <math><msub><mi>P</mi><mi>H</mi></msub></math>를 만들 필요는 없다. Active constraint가 <math><mi>k</mi></math>개라면

<math display="block" aria-label="PEAR Schur complement solve">
  <msub><mi>x</mi><mi>H</mi></msub><mo>=</mo><msup><mi>H</mi><mrow><mo>&minus;</mo><mn>1</mn></mrow></msup><mi>e</mi><mo>,</mo>
  <mspace width="0.6em"/>
  <mo>(</mo><mi>J</mi><msup><mi>H</mi><mrow><mo>&minus;</mo><mn>1</mn></mrow></msup><msup><mi>J</mi><mo>&top;</mo></msup><mo>)</mo><mi>v</mi>
  <mo>=</mo><mi>J</mi><msup><mi>H</mi><mrow><mo>&minus;</mo><mn>1</mn></mrow></msup><mi>e</mi>
</math>

를 계산한 뒤

<math display="block" aria-label="PEAR gradient signal">
  <mi>g</mi><mo>=</mo><msup><mi>H</mi><mrow><mo>&minus;</mo><mn>1</mn></mrow></msup><mi>e</mi>
  <mo>&minus;</mo><msup><mi>H</mi><mrow><mo>&minus;</mo><mn>1</mn></mrow></msup><msup><mi>J</mi><mo>&top;</mo></msup><mi>v</mi><mo>.</mo>
</math>

를 반환한다. 핵심 solve는 <math><mi>k</mi><mo>&times;</mo><mi>k</mi></math>다. <math><mi>k</mi><mo>&ll;</mo><mi>n</mi></math>이고 Hessian structure를 활용할 수 있다면 상당히 매력적이다.

## 정확한 정리는 local하고 strictly convex하다

유도에는 세 가지 강한 조건이 필요하다. Hessian이 positive definite여야 하고, active constraint Jacobian이 linear independence constraint qualification을 만족해야 하며, active inequality에 strict complementarity가 성립해야 한다. 이 조건들이 locally stable active set과 differentiable solution map을 뒷받침한다.

따라서 결과는 local이다. Active-set boundary를 넘으면 <math><mi>J</mi></math>가 바뀌고 solution map이 nonsmooth해질 수 있다. Degenerate하거나 weakly active한 constraint도 논리를 약하게 만든다. 정리는 strictly convex problem의 smooth neighborhood에 대해 정확한 결과를 준다. 임의의 mathematical program에 대한 global differentiability theorem은 아니다.

## LP 버전은 modified problem이고, 그다음에는 heuristic이다

LP에서는 <math><mi>&phi;</mi><mo>(</mo><mi>z</mi><mo>)</mo><mo>=</mo><mn>0</mn></math>이고 <math><mi>H</mi><mo>=</mo><mn>0</mn></math>이므로 PEAR의 inverse Hessian이 존재하지 않는다. 더 근본적으로 LP optimizer는 cost vector에 대해 piecewise constant다. 하나의 normal cone 안에서는 optimal vertex가 움직이지 않고 boundary에서는 jump할 수 있다. Classical derivative는 거의 모든 곳에서 zero이고 transition에서는 undefined다.

논문은 quadratic smoothing을 추가한다.

<math display="block" aria-label="Quadratically smoothed LP objective">
  <mi>&phi;</mi><mo>(</mo><mi>z</mi><mo>)</mo>
  <mo>=</mo><mfrac><mi>&lambda;</mi><mn>2</mn></mfrac><msup><mrow><mo>&Vert;</mo><mi>z</mi><mo>&Vert;</mo></mrow><mn>2</mn></msup><mo>,</mo>
  <mspace width="0.7em"/><mi>H</mi><mo>=</mo><mi>&lambda;</mi><mi>I</mi><mo>.</mo>
</math>

이렇게 하면 유용한 gradient가 생기지만, 그것은 원래 LP regret의 true gradient가 아니라 smoothed problem의 gradient다.

Implementation은 normalized normal component까지 주입한다.

<math display="block" aria-label="LP training을 위한 normal space injection">
  <mi>n</mi><mo>=</mo><msup><mi>&lambda;</mi><mrow><mo>&minus;</mo><mn>1</mn></mrow></msup><msup><mi>J</mi><mo>&top;</mo></msup><mi>v</mi><mo>,</mo>
  <mspace width="0.7em"/>
  <msub><mi>g</mi><mtext>inj</mtext></msub>
  <mo>=</mo><mi>g</mi><mo>+</mo><mi>&beta;</mi>
  <mfrac><mrow><mo>&Vert;</mo><mi>g</mi><mo>&Vert;</mo></mrow><mrow><mo>&Vert;</mo><mi>n</mi><mo>&Vert;</mo></mrow></mfrac><mi>n</mi><mo>.</mo>
</math>

Practical motivation은 이해할 수 있다. Tangent signal이 너무 약하면 LP plateau를 벗어나기 어렵다. 그러나 conceptually 역설적이다. 정리는 normal component를 decision-irrelevant하다고 제거하지만, LP training rule은 유용한 update를 얻기 위해 이를 다시 넣는다. Injection 이후의 <math><msub><mi>g</mi><mtext>inj</mtext></msub></math>는 regret gradient가 아니다.

따라서 method는 세 층으로 구분해야 한다.

- Strictly convex QP: 명시된 regularity assumption 아래의 exact local regret gradient.
- Quadratically smoothed LP: modified optimization problem의 gradient.
- Normal injection을 더한 smoothed LP: heuristic training direction.

세 층 모두 유용할 수 있다. 그러나 모두를 같은 exact-gradient label로 부르면 안 된다.

## Portfolio experiment는 predicted covariance 경로를 버린다

Portfolio problem은

<math display="block" aria-label="Mean variance portfolio problem">
  <munder><mo>min</mo><mi>w</mi></munder>
  <mspace width="0.5em"/>
  <mfrac><mi>&lambda;</mi><mn>2</mn></mfrac><msup><mi>w</mi><mo>&top;</mo></msup><mi>&Sigma;</mi><mi>w</mi>
  <mo>&minus;</mo><msup><mi>&mu;</mi><mo>&top;</mo></msup><mi>w</mi>
  <mspace width="0.8em"/><mtext>subject to</mtext><mspace width="0.5em"/>
  <msup><mn>1</mn><mo>&top;</mo></msup><mi>w</mi><mo>=</mo><mn>1</mn><mo>,</mo>
  <mspace width="0.4em"/><mi>w</mi><mo>&ge;</mo><mn>0</mn><mo>.</mo>
</math>

정리에서는 <math><mi>&phi;</mi><mo>(</mo><mi>w</mi><mo>)</mo><mo>=</mo><mi>&lambda;</mi><msup><mi>w</mi><mo>&top;</mo></msup><mi>&Sigma;</mi><mi>w</mi><mo>/</mo><mn>2</mn></math>가 known하고 prediction-independent이며 model은 linear coefficient <math><mo>&minus;</mo><mi>&mu;</mi></math>만 예측한다. 그러나 experiment에서 network는 21일 return path를 예측한다. 그 평균뿐 아니라 historical return과 predicted return에서 구성한 covariance matrix도 optimizer에 들어간다. 실제 decision은 <math><msup><mi>w</mi><mo>*</mo></msup><mo>(</mo><mover accent="true"><mi>&mu;</mi><mo>^</mo></mover><mo>,</mo><mover accent="true"><mi>&Sigma;</mi><mo>^</mo></mover><mo>)</mo></math>이다.

Predicted return <math><mover accent="true"><mi>r</mi><mo>^</mo></mover></math>에 대한 total derivative에는 두 경로가 있다.

<math display="block" aria-label="Mean과 covariance gradient 경로">
  <mfrac>
    <mrow><mi>d</mi><mi mathvariant="script">R</mi></mrow>
    <mrow><mi>d</mi><mover accent="true"><mi>r</mi><mo>^</mo></mover></mrow>
  </mfrac>
  <mo>=</mo>
  <mfrac><mrow><mo>&part;</mo><mi mathvariant="script">R</mi></mrow><mrow><mo>&part;</mo><mover accent="true"><mi>&mu;</mi><mo>^</mo></mover></mrow></mfrac>
  <mfrac><mrow><mo>&part;</mo><mover accent="true"><mi>&mu;</mi><mo>^</mo></mover></mrow><mrow><mo>&part;</mo><mover accent="true"><mi>r</mi><mo>^</mo></mover></mrow></mfrac>
  <mo>+</mo>
  <mfrac><mrow><mo>&part;</mo><mi mathvariant="script">R</mi></mrow><mrow><mo>&part;</mo><mover accent="true"><mi>&Sigma;</mi><mo>^</mo></mover></mrow></mfrac>
  <mfrac><mrow><mo>&part;</mo><mover accent="true"><mi>&Sigma;</mi><mo>^</mo></mover></mrow><mrow><mo>&part;</mo><mover accent="true"><mi>r</mi><mo>^</mo></mover></mrow></mfrac><mo>.</mo>
</math>

공개된 PEAR backward implementation은 predicted mean에 대해 projected gradient를 반환하고 predicted covariance에는 `None`을 반환한다. Covariance path가 stop-gradient 처리된다. 따라서 PEAR가 계산하는 것은 현재 predicted covariance를 fixed로 둔 채 mean에 대해서만 구한 partial regret gradient다. Experiment에서 사용한 optimization problem의 total derivative가 아니다.

이 차이는 baseline comparison도 복잡하게 만든다. Differentiable QP layer는 predicted mean과 covariance factor를 모두 받아 두 경로로 gradient를 보낼 수 있다. PEAR는 더 적은 gradient information을 사용한다. 성능 차이가 projection geometry 때문인지, covariance stop-gradient가 regularization처럼 작동했기 때문인지, 둘 다인지 알 수 없다. 이를 분리하는 direct ablation이 필요하다.

## Active-set numerics와 computational cost는 조건부다

PEAR는 finite-tolerance primal-dual solution에서 binding inequality를 식별한다. <math><msub><mi>G</mi><mi>i</mi></msub><msup><mi>z</mi><mo>*</mo></msup><mo>&minus;</mo><msub><mi>h</mi><mi>i</mi></msub><mo>&approx;</mo><mn>0</mn></math>이면 active-set membership이 numerical threshold에 따라 바뀔 수 있다. Degeneracy 근방에서는 <math><mi>J</mi></math>가 불안정해지고 <math><mi>J</mi><msup><mi>H</mi><mrow><mo>&minus;</mo><mn>1</mn></mrow></msup><msup><mi>J</mi><mo>&top;</mo></msup></math>가 ill-conditioned해질 수 있다. 이 방식이 solver differentiation보다 numerically stable하다는 주장은 theorem의 결과가 아니라 empirical claim이다.

Cost advantage도 조건부다. Active set이 작고 Hessian structure가 좋으면 PEAR가 유리하다. 그러나 많은 asset weight가 zero라면 nonnegativity constraint가 대량으로 active해져 <math><mi>k</mi></math>가 <math><mi>n</mi></math>에 가까워질 수 있다. Dense covariance matrix는 여전히 <math><mi>H</mi></math> factorization이나 solve를 요구한다. Sensitivity를 작은 Schur system으로 썼다는 이유만으로 PEAR가 자동으로 싸지는 것은 아니다.

## 실험이 실제로 보여 주는 것

LP benchmark는 5×5 shortest path와 100-item knapsack이다. Feature-to-cost mapping의 polynomial degree를 2에서 8까지 높인다. Knapsack에서 PEAR와 LAVA는 LP relaxation으로 training하고 original integer problem에서 evaluation한다.

Decision result는 강하다. Degree-8 knapsack의 normalized regret은 MSE 2.285%, SPO+ 0.763%, PEAR 0.437%다. Degree-8 shortest path에서도 PEAR가 4.246%로 가장 좋다. 그러나 모든 setting에서 이기지는 않는다. Degree 4에서는 SPO+가 0.761%, PEAR가 0.774%다. 따라서 “best decision quality among all baselines”라는 넓은 문구는 table이 지지하는 범위보다 약간 강하다.

Computational efficiency도 같은 식으로 한정해야 한다. Shortest-path degree 8에서 MSE는 6.1초, PEAR는 38.4초다. Portfolio에서는 MSE 33.0초, PEAR 122.3초다. 같은 portfolio comparison에서 QPTH는 147.6초, CVXPYLayers는 321.9초이므로 PEAR가 더 빠르다. 정확한 표현은 “가장 빠른 baseline”이 아니라 “빠른 decision-focused method 중 하나”다.

Portfolio optimization에서 PEAR는 가장 낮은 normalized regret 85.38%, MSE의 0.92와 QPTH/CVXPYLayers의 1.15보다 높은 Sharpe ratio 1.44, 가장 낮은 maximum drawdown을 보고한다. 하지만 5개 seed 사이의 uncertainty가 크다. Cumulative return은 PEAR가 <math><mn>184.19</mn><mo>&PlusMinus;</mo><mn>86.24</mn><mo>%</mo></math>, QPTH가 <math><mn>139.77</mn><mo>&PlusMinus;</mo><mn>115.74</mn><mo>%</mo></math>다. 결과는 유망하지만 economic superiority를 확정하기에는 variance가 크고 covariance-gradient ablation도 없다.

Constraint-shift experiment가 오히려 더 많은 것을 말해 준다. Training과 test에서 optimization geometry를 바꾼다. Shortest path의 source-target direction, knapsack capacity, portfolio의 long-only constraint가 달라진다. MSE는 상당히 강하다. Degree-8 shortest-path direction shift에서 MSE는 14.00, PEAR는 21.42, SPO+는 43.40이다. DFL은 training-time feasible geometry에 맞춰 prediction error를 의도적으로 변형한다. Geometry가 바뀌면 그 inductive bias가 약점이 될 수 있다. 이것은 부차적 결과가 아니라 in-distribution decision quality와 constraint transfer 사이의 실제 경계를 보여 준다.

## 판단

정확한 결과는 남길 가치가 있다. Prediction-independent한 strictly convex objective, regular하고 locally fixed된 active set 아래에서 regret gradient는 ordinary prediction error의 curvature-scaled tangent-space projection이다. Proof는 KKT sensitivity와 stationarity에서 깔끔하게 나오며, 이 해석은 DFL을 훨씬 이해하기 쉽게 만든다.

Practical method는 더 넓은 영역에 있다. LP variant는 smoothed surrogate를 최적화한 뒤 heuristic normal component를 넣는다. Portfolio experiment는 predicted return이 covariance도 결정하는데 mean-return path만 미분한다. Active-set identification과 runtime gain은 numerical tolerance, sparsity, Hessian structure에 의존한다.

올바른 결론은 theorem이 틀렸다는 것이 아니다. Theorem, LP training rule, covariance-dependent QP experiment를 서로 다른 세 개의 대상으로 구분해야 한다는 것이다. 이 경계를 명시할 때 PEAR의 geometry가 가장 설득력 있다.

## 참고문헌

Junhyeong Lee, Sangjin Jin, and Yongjae Lee. *Decision-Focused Learning via Tangent-Space Projection of Prediction Error*. ICML, 2026. 검토에 사용한 자료에는 source URL, DOI, arXiv identifier가 제공되지 않았다.
