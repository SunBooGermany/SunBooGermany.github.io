---
layout: post
title: "PEAR: Which Prediction Errors Actually Change the Decision?"
title_ko: "PEAR: 어떤 예측 오차가 실제 의사결정을 바꾸는가?"
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
excerpt: "A constrained optimizer cannot react to every prediction error. PEAR keeps the directions that can move the decision, making it most natural when system dynamics and constraints stay fixed while objective coefficients change across instances."
excerpt_ko: "제약 최적화기는 모든 예측 오차에 반응하지 않는다. PEAR는 의사결정을 움직일 수 있는 오차만 남기며, 시스템의 동역학과 제약은 같고 목적함수 계수만 달라지는 문제에 특히 잘 맞는다."
language: "en-ko"
has_korean_note: false
---

This paper argues that a model need not predict every objective coefficient equally well. Some prediction errors may be large without changing the optimizer at all. A much smaller error in another direction can change the selected solution and sharply increase the realized cost. PEAR uses this difference: it trains the predictor on the part of its error that can move the downstream decision under the current constraints.

The approach is especially relevant when the system dynamics and constraints are reused while cost or reward coefficients change from one instance to the next. Examples include process operation with a fixed plant model but changing electricity prices, dispatch over the same network with changing marginal costs, and portfolio optimization with a fixed risk model but changing expected returns.

For a regular strictly convex problem, the paper shows that this intuition is exactly the local gradient of decision regret. The scope is narrower for the LP method and the portfolio experiment. The former adds smoothing and a heuristic normal component; the latter stops a covariance-gradient path that is present in the experimental optimization problem. The distinction between the theorem and these extensions is the main point to keep in view.

## 1. Repeated system, changing objective coefficients

Let <math><mi>x</mi></math> denote the information available before a decision and <math><mi>c</mi><mo>&isin;</mo><msup><mi>&Ropf;</mi><mi>n</mi></msup></math> an objective coefficient that is not yet known. A neural network predicts

<math display="block" aria-label="Predicted objective coefficient">
  <mover accent="true"><mi>c</mi><mo>^</mo></mover>
  <mo>=</mo><msub><mi>f</mi><mi>&theta;</mi></msub><mo>(</mo><mi>x</mi><mo>)</mo><mo>.</mo>
</math>

The prediction is not the final decision. It enters an optimization problem:

<math display="block" aria-label="Predict then optimize problem">
  <msup><mi>z</mi><mo>*</mo></msup><mo>(</mo><mover accent="true"><mi>c</mi><mo>^</mo></mover><mo>)</mo>
  <mo>=</mo>
  <munder><mo>arg min</mo><mi>z</mi></munder>
  <mrow><mo>[</mo><mi>&phi;</mi><mo>(</mo><mi>z</mi><mo>)</mo><mo>+</mo><msup><mover accent="true"><mi>c</mi><mo>^</mo></mover><mo>&top;</mo></msup><mi>z</mi><mo>]</mo></mrow>
  <mspace width="0.8em"/><mtext>subject to</mtext><mspace width="0.5em"/>
  <mi>A</mi><mi>z</mi><mo>=</mo><mi>b</mi><mo>,</mo>
  <mspace width="0.4em"/><mi>G</mi><mi>z</mi><mo>&le;</mo><mi>h</mi><mo>.</mo>
</math>

Here <math><mi>&phi;</mi></math> and the constraint system describe the part of the optimization model that is already known. PEAR's exact theorem treats the prediction as entering only through the linear coefficient <math><mover accent="true"><mi>c</mi><mo>^</mo></mover></math>. In a control problem, for example, the plant dynamics, input bounds, and quadratic control penalty may be fixed while a model predicts a linear cost term associated with the current operating condition. In a mean-variance portfolio, the same structure appears if covariance and portfolio constraints are fixed while expected returns are predicted.

Ordinary supervised learning minimizes the coefficient error,

<math display="block" aria-label="Mean squared prediction error">
  <msub><mi>L</mi><mtext>MSE</mtext></msub>
  <mo>=</mo><mfrac><mn>1</mn><mn>2</mn></mfrac>
  <msup><mrow><mo>&Vert;</mo><mover accent="true"><mi>c</mi><mo>^</mo></mover><mo>&minus;</mo><mi>c</mi><mo>&Vert;</mo></mrow><mn>2</mn></msup><mo>.</mo>
</math>

Decision-focused learning instead evaluates the decision made with the prediction under the true coefficient:

<math display="block" aria-label="Decision regret">
  <mi mathvariant="script">R</mi><mo>(</mo><mover accent="true"><mi>c</mi><mo>^</mo></mover><mo>;</mo><mi>c</mi><mo>)</mo>
  <mo>=</mo>
  <mi>&phi;</mi><mo>(</mo><msup><mi>z</mi><mo>*</mo></msup><mo>(</mo><mover accent="true"><mi>c</mi><mo>^</mo></mover><mo>)</mo><mo>)</mo>
  <mo>+</mo><msup><mi>c</mi><mo>&top;</mo></msup><msup><mi>z</mi><mo>*</mo></msup><mo>(</mo><mover accent="true"><mi>c</mi><mo>^</mo></mover><mo>)</mo>
  <mo>&minus;</mo>
  <mrow><mo>[</mo><mi>&phi;</mi><mo>(</mo><msup><mi>z</mi><mo>*</mo></msup><mo>(</mo><mi>c</mi><mo>)</mo><mo>)</mo>
  <mo>+</mo><msup><mi>c</mi><mo>&top;</mo></msup><msup><mi>z</mi><mo>*</mo></msup><mo>(</mo><mi>c</mi><mo>)</mo><mo>]</mo></mrow><mo>.</mo>
</math>

The first term is the realized cost of the decision induced by the prediction. The second is the perfect-information optimum. Training on this regret requires the sensitivity <math><mo>&part;</mo><msup><mi>z</mi><mo>*</mo></msup><mo>/</mo><mo>&part;</mo><mover accent="true"><mi>c</mi><mo>^</mo></mover></math>, which is usually the expensive part of differentiating through the optimizer.

## 2. Discard errors that cannot move the decision

Consider the constraint <math><msub><mi>z</mi><mn>1</mn></msub><mo>+</mo><msub><mi>z</mi><mn>2</mn></msub><mo>=</mo><mn>1</mn></math>. Feasible decisions lie on a line. Compare the prediction errors <math><mo>(</mo><mn>1</mn><mo>,</mo><mo>&minus;</mo><mn>1</mn><mo>)</mo></math> and <math><mo>(</mo><mn>1</mn><mo>,</mo><mn>1</mn><mo>)</mo></math>.

The first changes the relative costs of <math><msub><mi>z</mi><mn>1</mn></msub></math> and <math><msub><mi>z</mi><mn>2</mn></msub></math>, so it can move the solution along the feasible line. The second raises both costs equally. For every feasible decision,

<math display="block" aria-label="A normal objective shift is constant on the feasible set">
  <mo>(</mo><msub><mi>c</mi><mn>1</mn></msub><mo>+</mo><mn>1</mn><mo>)</mo><msub><mi>z</mi><mn>1</mn></msub>
  <mo>+</mo><mo>(</mo><msub><mi>c</mi><mn>2</mn></msub><mo>+</mo><mn>1</mn><mo>)</mo><msub><mi>z</mi><mn>2</mn></msub>
  <mo>=</mo><msub><mi>c</mi><mn>1</mn></msub><msub><mi>z</mi><mn>1</mn></msub>
  <mo>+</mo><msub><mi>c</mi><mn>2</mn></msub><msub><mi>z</mi><mn>2</mn></msub><mo>+</mo><mn>1</mn><mo>.</mo>
</math>

It adds the same constant to every feasible objective value, so the optimizer does not change. MSE tries to correct both errors. PEAR removes the second type before sending the learning signal back to the predictor.

This is a statement about directions, not individual coefficients. PEAR does not label one coefficient important and another irrelevant. A combination of coefficient errors can be invisible to the optimizer because it lies normal to the feasible set. Another combination of the same size can be tangent to that set and change the decision.

## 3. Active constraints define the relevant directions

At the current solution, collect the equality constraints and active inequalities in

<math display="block" aria-label="Active constraint Jacobian">
  <mi>J</mi><mo>=</mo>
  <mrow><mo>[</mo><mtable><mtr><mtd><mi>A</mi></mtd></mtr><mtr><mtd><msub><mi>G</mi><mi mathvariant="script">A</mi></msub></mtd></mtr></mtable><mo>]</mo></mrow><mo>.</mo>
</math>

A small feasible displacement must satisfy <math><mi>J</mi><mi>d</mi><mi>z</mi><mo>=</mo><mn>0</mn></math>. The local tangent and normal spaces are therefore

<math display="block" aria-label="Tangent and normal spaces">
  <mi mathvariant="script">T</mi><mo>=</mo><mi>ker</mi><mo>(</mo><mi>J</mi><mo>)</mo><mo>,</mo>
  <mspace width="1em"/>
  <mi mathvariant="script">N</mi><mo>=</mo><mi>range</mi><mo>(</mo><msup><mi>J</mi><mo>&top;</mo></msup><mo>)</mo><mo>.</mo>
</math>

The simple two-variable example used ordinary Euclidean geometry. A general strictly convex objective has its own local curvature. With

<math display="block" aria-label="Objective Hessian">
  <mi>H</mi><mo>=</mo><msup><mo>&nabla;</mo><mn>2</mn></msup><mi>&phi;</mi><mo>(</mo><msup><mi>z</mi><mo>*</mo></msup><mo>)</mo><mo>,</mo>
</math>

PEAR first scales the error by <math><msup><mi>H</mi><mrow><mo>&minus;</mo><mn>1</mn></mrow></msup></math> and then projects it onto <math><mi mathvariant="script">T</mi></math> in the metric defined by <math><mi>H</mi></math>. Calling the entire operation a Euclidean projection would be inaccurate unless <math><mi>H</mi><mo>=</mo><mi>&alpha;</mi><mi>I</mi></math>.

## 4. The projected error is the exact local regret gradient

Assume the active set does not change under a small perturbation. The local KKT conditions are

<math display="block" aria-label="Local KKT conditions">
  <mo>&nabla;</mo><mi>&phi;</mi><mo>(</mo><msup><mi>z</mi><mo>*</mo></msup><mo>)</mo>
  <mo>+</mo><mover accent="true"><mi>c</mi><mo>^</mo></mover>
  <mo>+</mo><msup><mi>J</mi><mo>&top;</mo></msup><msup><mi>y</mi><mo>*</mo></msup><mo>=</mo><mn>0</mn><mo>,</mo>
  <mspace width="0.8em"/>
  <mi>J</mi><msup><mi>z</mi><mo>*</mo></msup><mo>=</mo><mover><mi>b</mi><mo>~</mo></mover><mo>.</mo>
</math>

Differentiating them gives

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

Eliminating the dual displacement yields

<math display="block" aria-label="Projected sensitivity operator">
  <mi>d</mi><mi>z</mi><mo>=</mo><mo>&minus;</mo><msub><mi>P</mi><mi>H</mi></msub><mi>d</mi><mover accent="true"><mi>c</mi><mo>^</mo></mover><mo>,</mo>
  <mspace width="0.7em"/>
  <msub><mi>P</mi><mi>H</mi></msub>
  <mo>=</mo><msup><mi>H</mi><mrow><mo>&minus;</mo><mn>1</mn></mrow></msup>
  <mo>&minus;</mo>
  <msup><mi>H</mi><mrow><mo>&minus;</mo><mn>1</mn></mrow></msup><msup><mi>J</mi><mo>&top;</mo></msup>
  <msup><mrow><mo>(</mo><mi>J</mi><msup><mi>H</mi><mrow><mo>&minus;</mo><mn>1</mn></mrow></msup><msup><mi>J</mi><mo>&top;</mo></msup><mo>)</mo></mrow><mrow><mo>&minus;</mo><mn>1</mn></mrow></msup>
  <mi>J</mi><msup><mi>H</mi><mrow><mo>&minus;</mo><mn>1</mn></mrow></msup><mo>.</mo>
</math>

Let <math><mi>e</mi><mo>=</mo><mover accent="true"><mi>c</mi><mo>^</mo></mover><mo>&minus;</mo><mi>c</mi></math>. Stationarity gives <math><mo>&nabla;</mo><mi>&phi;</mi><mo>(</mo><msup><mi>z</mi><mo>*</mo></msup><mo>)</mo><mo>+</mo><mi>c</mi><mo>=</mo><mo>&minus;</mo><mi>e</mi><mo>&minus;</mo><msup><mi>J</mi><mo>&top;</mo></msup><msup><mi>y</mi><mo>*</mo></msup></math>. Since <math><msub><mi>P</mi><mi>H</mi></msub><msup><mi>J</mi><mo>&top;</mo></msup><mo>=</mo><mn>0</mn></math>, the dual term disappears from the chain rule, leaving

<math display="block" aria-label="Exact local regret gradient">
  <msub><mo>&nabla;</mo><mover accent="true"><mi>c</mi><mo>^</mo></mover></msub><mi mathvariant="script">R</mi>
  <mo>=</mo><msub><mi>P</mi><mi>H</mi></msub>
  <mo>(</mo><mover accent="true"><mi>c</mi><mo>^</mo></mover><mo>&minus;</mo><mi>c</mi><mo>)</mo><mo>.</mo>
</math>

This is the paper's main result. Under its assumptions, PEAR is not merely a plausible surrogate direction. It equals the local gradient of regret with respect to the predicted linear coefficient.

## 5. The implementation changes the backward signal

The released QP code returns an ordinary squared error as its forward value. Its backward method overrides the MSE derivative and returns <math><msub><mi>P</mi><mi>H</mi></msub><mi>e</mi></math>. PEAR is therefore better understood as a custom gradient rule than as a new scalar loss.

The full <math><mi>n</mi><mo>&times;</mo><mi>n</mi></math> matrix <math><msub><mi>P</mi><mi>H</mi></msub></math> need not be formed. If <math><mi>k</mi></math> constraints are active, the method solves

<math display="block" aria-label="Schur complement system used by PEAR">
  <mo>(</mo><mi>J</mi><msup><mi>H</mi><mrow><mo>&minus;</mo><mn>1</mn></mrow></msup><msup><mi>J</mi><mo>&top;</mo></msup><mo>)</mo><mi>v</mi>
  <mo>=</mo><mi>J</mi><msup><mi>H</mi><mrow><mo>&minus;</mo><mn>1</mn></mrow></msup><mi>e</mi>
</math>

and returns

<math display="block" aria-label="PEAR backward signal">
  <mi>g</mi><mo>=</mo><msup><mi>H</mi><mrow><mo>&minus;</mo><mn>1</mn></mrow></msup><mi>e</mi>
  <mo>&minus;</mo><msup><mi>H</mi><mrow><mo>&minus;</mo><mn>1</mn></mrow></msup><msup><mi>J</mi><mo>&top;</mo></msup><mi>v</mi><mo>.</mo>
</math>

The central solve is <math><mi>k</mi><mo>&times;</mo><mi>k</mi></math>. This is attractive when relatively few constraints are active and solves with <math><mi>H</mi></math> are cheap.

## 6. Where the exact theorem stops

The derivation requires <math><mi>H</mi><mo>&succ;</mo><mn>0</mn></math>, linearly independent active constraints, and strict complementarity. These assumptions keep the active set locally fixed and the solution map differentiable. The result is local. At an active-set boundary, <math><mi>J</mi></math> changes and the gradient can be nonsmooth.

A pure LP does not satisfy the curvature assumption because <math><mi>H</mi><mo>=</mo><mn>0</mn></math>. Its optimizer is piecewise constant in the cost vector: a small cost change usually leaves the optimal vertex unchanged, while crossing a normal-cone boundary can make the solution jump.

The paper handles this by adding quadratic smoothing,

<math display="block" aria-label="Quadratic smoothing for an LP">
  <mi>&phi;</mi><mo>(</mo><mi>z</mi><mo>)</mo>
  <mo>=</mo><mfrac><mi>&lambda;</mi><mn>2</mn></mfrac><msup><mrow><mo>&Vert;</mo><mi>z</mi><mo>&Vert;</mo></mrow><mn>2</mn></msup><mo>,</mo>
  <mspace width="0.7em"/><mi>H</mi><mo>=</mo><mi>&lambda;</mi><mi>I</mi><mo>.</mo>
</math>

The resulting gradient belongs to the smoothed problem, not the original LP. The implementation then adds a normalized normal component,

<math display="block" aria-label="Normal component injection">
  <mi>n</mi><mo>=</mo><msup><mi>&lambda;</mi><mrow><mo>&minus;</mo><mn>1</mn></mrow></msup><msup><mi>J</mi><mo>&top;</mo></msup><mi>v</mi><mo>,</mo>
  <mspace width="0.7em"/>
  <msub><mi>g</mi><mtext>inj</mtext></msub>
  <mo>=</mo><mi>g</mi><mo>+</mo><mi>&beta;</mi>
  <mfrac><mrow><mo>&Vert;</mo><mi>g</mi><mo>&Vert;</mo></mrow><mrow><mo>&Vert;</mo><mi>n</mi><mo>&Vert;</mo></mrow></mfrac><mi>n</mi><mo>.</mo>
</math>

This can help escape a flat LP region, but it is a heuristic. It also reintroduces the normal direction that the original geometric argument removed as locally decision-irrelevant. The strictly convex QP result, the smoothed LP gradient, and the LP gradient with normal injection are three different claims.

## 7. The portfolio experiment omits the covariance path

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

The theorem matches this problem when <math><mi>&Sigma;</mi></math> is fixed and only <math><mi>&mu;</mi></math> is predicted. In the experiment, the network predicts a 21-day return path. Both the sample mean and a covariance matrix constructed from historical and predicted returns enter the optimizer. The decision is therefore <math><msup><mi>w</mi><mo>*</mo></msup><mo>(</mo><mover accent="true"><mi>&mu;</mi><mo>^</mo></mover><mo>,</mo><mover accent="true"><mi>&Sigma;</mi><mo>^</mo></mover><mo>)</mo></math>, and the total derivative with respect to predicted returns has two paths:

<math display="block" aria-label="Mean and covariance derivative paths">
  <mfrac><mrow><mi>d</mi><mi mathvariant="script">R</mi></mrow><mrow><mi>d</mi><mover accent="true"><mi>r</mi><mo>^</mo></mover></mrow></mfrac>
  <mo>=</mo>
  <mfrac><mrow><mo>&part;</mo><mi mathvariant="script">R</mi></mrow><mrow><mo>&part;</mo><mover accent="true"><mi>&mu;</mi><mo>^</mo></mover></mrow></mfrac>
  <mfrac><mrow><mo>&part;</mo><mover accent="true"><mi>&mu;</mi><mo>^</mo></mover></mrow><mrow><mo>&part;</mo><mover accent="true"><mi>r</mi><mo>^</mo></mover></mrow></mfrac>
  <mo>+</mo>
  <mfrac><mrow><mo>&part;</mo><mi mathvariant="script">R</mi></mrow><mrow><mo>&part;</mo><mover accent="true"><mi>&Sigma;</mi><mo>^</mo></mover></mrow></mfrac>
  <mfrac><mrow><mo>&part;</mo><mover accent="true"><mi>&Sigma;</mi><mo>^</mo></mover></mrow><mrow><mo>&part;</mo><mover accent="true"><mi>r</mi><mo>^</mo></mover></mrow></mfrac><mo>.</mo>
</math>

The released PEAR backward pass returns the projected gradient for the predicted mean and `None` for the predicted covariance. It computes a partial derivative with respect to the mean while treating the current covariance as fixed. Differentiable QP baselines can receive gradients through both inputs. Without an ablation, it is unclear how much of PEAR's portfolio result comes from the projection and how much comes from stopping the covariance gradient.

## 8. The computational advantage is conditional

PEAR reads the active set from a finite-tolerance primal-dual solution. A nearly binding constraint can enter or leave the set when the numerical threshold changes. Near degeneracy, <math><mi>J</mi></math> may be unstable and <math><mi>J</mi><msup><mi>H</mi><mrow><mo>&minus;</mo><mn>1</mn></mrow></msup><msup><mi>J</mi><mo>&top;</mo></msup></math> may be ill-conditioned. Numerical stability relative to a differentiable solver is therefore an empirical question.

Runtime also depends on problem structure. PEAR is most favorable when <math><mi>k</mi><mo>&ll;</mo><mi>n</mi></math> and the Hessian is sparse, diagonal, or already factorized. If many nonnegativity constraints are active, as can happen in a sparse portfolio, <math><mi>k</mi></math> can approach <math><mi>n</mi></math>. A dense covariance matrix still requires expensive solves with <math><mi>H</mi></math>.

## 9. Strong results, but not a universal win

The LP benchmarks use a 5-by-5 shortest-path problem and a 100-item knapsack, with increasingly nonlinear feature-to-cost mappings. PEAR and LAVA train on an LP relaxation for knapsack and are evaluated on the original integer problem.

At polynomial degree 8, normalized regret on knapsack is 2.285% for MSE, 0.763% for SPO+, and 0.437% for PEAR. PEAR also records the best degree-8 shortest-path result at 4.246%. It does not win every setting: at degree 4, SPO+ obtains 0.761% and PEAR 0.774%. The phrase “best decision quality among all baselines” is slightly broader than the table supports.

PEAR is faster than the differentiable QP layers in the reported portfolio comparison: 122.3 seconds versus 147.6 for QPTH and 321.9 for CVXPYLayers. MSE takes only 33.0 seconds. The defensible claim is that PEAR is one of the faster decision-focused methods, not the fastest baseline without qualification.

The portfolio results are promising but variable. PEAR reports normalized regret of 85.38%, a Sharpe ratio of 1.44, and the lowest maximum drawdown. Across five seeds, cumulative return is <math><mn>184.19</mn><mo>&PlusMinus;</mo><mn>86.24</mn><mo>%</mo></math>, compared with <math><mn>139.77</mn><mo>&PlusMinus;</mo><mn>115.74</mn><mo>%</mo></math> for QPTH. That uncertainty is too large to establish clear economic superiority.

The constraint-shift experiment exposes a useful limitation. When the shortest-path source and target change, MSE is best at every tested degree. At degree 8, MSE scores 14.00, PEAR 21.42, and SPO+ 43.40. DFL deliberately concentrates accuracy on the training-time decision geometry. When that geometry changes, the same specialization can hurt transfer.

## 10. Assessment

The paper's main theorem is both simple and useful. When a regular strictly convex optimizer repeatedly solves the same system with changing linear objective coefficients, the regret gradient is ordinary prediction error after curvature scaling and tangent-space projection. This gives a clear answer to which prediction errors deserve learning capacity.

The qualifications are equally concrete. The LP version is a smoothed and then heuristically modified method. The portfolio implementation omits a covariance-gradient path. The speed advantage depends on a small, stable active set and cheap Hessian solves. None of these points invalidates the theorem; they mark the boundary between the theorem and the broader experimental method.

## Reference

Junhyeong Lee, Sangjin Jin, and Yongjae Lee. *Decision-Focused Learning via Tangent-Space Projection of Prediction Error*. ICML, 2026. A source URL, DOI, and arXiv identifier were not provided with the reviewed material.

<!-- ko -->

이 논문은 모든 목적함수 계수를 똑같이 정확하게 예측하기보다, 최종 의사결정의 질에 영향을 주는 예측 오차에 학습을 집중하자는 연구다. 제약 최적화에서는 어떤 예측 오차가 크더라도 최적해가 전혀 바뀌지 않을 수 있다. 반대로 특정 방향의 작은 오차가 선택되는 해와 실제 비용을 크게 바꿀 수도 있다. PEAR는 이러한 차이를 이용해, 예측 오차 중 현재 제약조건 아래에서 의사결정을 움직일 수 있는 방향만 학습에 사용한다.

이 접근법은 시스템의 동역학과 제약조건은 반복해서 동일하게 사용되지만, 비용이나 수익률과 같은 목적함수 계수가 문제마다 달라지는 경우에 특히 유용하다. 예를 들어 동일한 공정 모델을 사용하는 운전 최적화에서 전력가격이나 한계운전비용이 변하는 경우, 같은 전력망에서 발전비용 계수가 달라지는 경우, 또는 위험모형은 고정하고 기대수익률만 예측하는 포트폴리오 문제를 생각할 수 있다.

논문의 핵심 정리는 엄밀히 볼록한 최적화 문제에서 이 생각이 단순한 직관이 아니라 실제 후회값의 기울기와 일치한다는 것을 보인다. 다만 선형계획에 적용한 방법과 예측 공분산을 사용하는 포트폴리오 실험은 이 정리의 정확한 범위를 벗어난다. 이 글에서는 먼저 PEAR의 단순한 기하학적 아이디어를 설명하고, 그다음 정리가 성립하는 조건과 실제 구현 및 실험 사이의 차이를 살펴본다.

## 1. 동일한 시스템에서 목적함수 계수만 달라지는 문제

의사결정을 내리기 전에 알 수 있는 정보를 <math><mi>x</mi></math>, 아직 알 수 없는 목적함수 계수를 <math><mi>c</mi><mo>&isin;</mo><msup><mi>&Ropf;</mi><mi>n</mi></msup></math>이라고 하자. 신경망은 다음 값을 예측한다.

<math display="block" aria-label="예측 목적함수 계수">
  <mover accent="true"><mi>c</mi><mo>^</mo></mover>
  <mo>=</mo><msub><mi>f</mi><mi>&theta;</mi></msub><mo>(</mo><mi>x</mi><mo>)</mo><mo>.</mo>
</math>

이 예측값이 곧 최종 결정은 아니다. 예측값은 다음 최적화 문제의 목적함수에 들어간다.

<math display="block" aria-label="예측 후 최적화 문제">
  <msup><mi>z</mi><mo>*</mo></msup><mo>(</mo><mover accent="true"><mi>c</mi><mo>^</mo></mover><mo>)</mo>
  <mo>=</mo>
  <munder><mo>arg min</mo><mi>z</mi></munder>
  <mrow><mo>[</mo><mi>&phi;</mi><mo>(</mo><mi>z</mi><mo>)</mo><mo>+</mo><msup><mover accent="true"><mi>c</mi><mo>^</mo></mover><mo>&top;</mo></msup><mi>z</mi><mo>]</mo></mrow>
  <mspace width="0.8em"/><mtext>제약조건</mtext><mspace width="0.5em"/>
  <mi>A</mi><mi>z</mi><mo>=</mo><mi>b</mi><mo>,</mo>
  <mspace width="0.4em"/><mi>G</mi><mi>z</mi><mo>&le;</mo><mi>h</mi><mo>.</mo>
</math>

여기서 <math><mi>&phi;</mi></math>와 제약식은 이미 알고 있는 시스템 구조를 나타낸다. PEAR의 정확한 정리는 예측값이 선형 목적함수 계수 <math><mover accent="true"><mi>c</mi><mo>^</mo></mover></math>로만 들어가는 경우를 다룬다. 제어 문제라면 공정 동역학, 입력 한계, 이차 제어비용은 고정하고 현재 운전조건에 따른 선형 비용항만 예측하는 경우다. 평균–분산 포트폴리오에서는 공분산과 투자 제약은 고정하고 기대수익률만 예측할 때 같은 구조가 된다.

일반적인 지도학습은 계수의 평균제곱오차(MSE)를 최소화한다.

<math display="block" aria-label="평균제곱 예측오차">
  <msub><mi>L</mi><mtext>MSE</mtext></msub>
  <mo>=</mo><mfrac><mn>1</mn><mn>2</mn></mfrac>
  <msup><mrow><mo>&Vert;</mo><mover accent="true"><mi>c</mi><mo>^</mo></mover><mo>&minus;</mo><mi>c</mi><mo>&Vert;</mo></mrow><mn>2</mn></msup><mo>.</mo>
</math>

의사결정 중심 학습은 예측값으로 내린 결정을 실제 계수 아래에서 평가한다.

<math display="block" aria-label="의사결정 후회값">
  <mi mathvariant="script">R</mi><mo>(</mo><mover accent="true"><mi>c</mi><mo>^</mo></mover><mo>;</mo><mi>c</mi><mo>)</mo>
  <mo>=</mo>
  <mi>&phi;</mi><mo>(</mo><msup><mi>z</mi><mo>*</mo></msup><mo>(</mo><mover accent="true"><mi>c</mi><mo>^</mo></mover><mo>)</mo><mo>)</mo>
  <mo>+</mo><msup><mi>c</mi><mo>&top;</mo></msup><msup><mi>z</mi><mo>*</mo></msup><mo>(</mo><mover accent="true"><mi>c</mi><mo>^</mo></mover><mo>)</mo>
  <mo>&minus;</mo>
  <mrow><mo>[</mo><mi>&phi;</mi><mo>(</mo><msup><mi>z</mi><mo>*</mo></msup><mo>(</mo><mi>c</mi><mo>)</mo><mo>)</mo>
  <mo>+</mo><msup><mi>c</mi><mo>&top;</mo></msup><msup><mi>z</mi><mo>*</mo></msup><mo>(</mo><mi>c</mi><mo>)</mo><mo>]</mo></mrow><mo>.</mo>
</math>

첫 항은 예측값으로 선택한 결정을 실제 계수로 평가한 비용이다. 두 번째 항은 실제 계수를 미리 알았을 때 얻는 최적값이다. 이 후회값으로 신경망을 학습하려면 예측값이 바뀔 때 최적해가 어떻게 움직이는지, 즉 <math><mo>&part;</mo><msup><mi>z</mi><mo>*</mo></msup><mo>/</mo><mo>&part;</mo><mover accent="true"><mi>c</mi><mo>^</mo></mover></math>를 구해야 한다. 보통은 이 계산이 최적화기를 미분할 때 가장 부담스러운 부분이다.

## 2. 의사결정을 움직이지 않는 오차는 학습에서 제외한다

가능한 결정이 <math><msub><mi>z</mi><mn>1</mn></msub><mo>+</mo><msub><mi>z</mi><mn>2</mn></msub><mo>=</mo><mn>1</mn></math>을 만족해야 한다고 하자. 예측 오차 <math><mo>(</mo><mn>1</mn><mo>,</mo><mo>&minus;</mo><mn>1</mn><mo>)</mo></math>과 <math><mo>(</mo><mn>1</mn><mo>,</mo><mn>1</mn><mo>)</mo></math>을 비교해 보자.

첫 번째 오차는 <math><msub><mi>z</mi><mn>1</mn></msub></math>과 <math><msub><mi>z</mi><mn>2</mn></msub></math>의 상대적인 비용을 바꾼다. 따라서 최적해를 실행 가능한 직선을 따라 움직일 수 있다. 두 번째 오차는 두 비용을 같은 크기로 올린다. 모든 실행 가능한 결정에서

<math display="block" aria-label="법선방향 목적함수 변화는 실행가능집합에서 상수다">
  <mo>(</mo><msub><mi>c</mi><mn>1</mn></msub><mo>+</mo><mn>1</mn><mo>)</mo><msub><mi>z</mi><mn>1</mn></msub>
  <mo>+</mo><mo>(</mo><msub><mi>c</mi><mn>2</mn></msub><mo>+</mo><mn>1</mn><mo>)</mo><msub><mi>z</mi><mn>2</mn></msub>
  <mo>=</mo><msub><mi>c</mi><mn>1</mn></msub><msub><mi>z</mi><mn>1</mn></msub>
  <mo>+</mo><msub><mi>c</mi><mn>2</mn></msub><msub><mi>z</mi><mn>2</mn></msub><mo>+</mo><mn>1</mn><mo>.</mo>
</math>

목적함수에 같은 상수 1만 더해지므로 최적해는 변하지 않는다. 평균제곱오차는 두 오차를 모두 줄이려 하지만, PEAR는 두 번째와 같은 오차를 신경망에 되돌려 보낼 학습신호에서 제거한다.

여기서 구분하는 대상은 개별 계수가 아니라 오차의 방향이다. PEAR가 특정 계수 하나를 중요하거나 불필요하다고 판정하는 것은 아니다. 여러 계수의 오차가 결합된 방향이 실행가능집합에 수직이면 최적해가 보지 못한다. 같은 크기의 오차라도 실행가능집합을 따라가는 방향이면 의사결정을 바꿀 수 있다.

## 3. 활성 제약조건이 중요한 방향을 결정한다

현재 최적해에서 등식 제약과 활성화된 부등식 제약을 모아 다음 행렬을 만든다.

<math display="block" aria-label="활성 제약조건 행렬">
  <mi>J</mi><mo>=</mo>
  <mrow><mo>[</mo><mtable><mtr><mtd><mi>A</mi></mtd></mtr><mtr><mtd><msub><mi>G</mi><mi mathvariant="script">A</mi></msub></mtd></mtr></mtable><mo>]</mo></mrow><mo>.</mo>
</math>

제약을 깨지 않는 작은 이동은 <math><mi>J</mi><mi>d</mi><mi>z</mi><mo>=</mo><mn>0</mn></math>을 만족해야 한다. 따라서 국소 접공간과 법선공간은

<math display="block" aria-label="접공간과 법선공간">
  <mi mathvariant="script">T</mi><mo>=</mo><mi>ker</mi><mo>(</mo><mi>J</mi><mo>)</mo><mo>,</mo>
  <mspace width="1em"/>
  <mi mathvariant="script">N</mi><mo>=</mo><mi>range</mi><mo>(</mo><msup><mi>J</mi><mo>&top;</mo></msup><mo>)</mo><mo>.</mo>
</math>

이다. 앞의 두 변수 예에서는 평범한 유클리드 기하만 생각했다. 일반적인 엄밀히 볼록한 목적함수에는 고유한 국소 곡률이 있다.

<math display="block" aria-label="목적함수 헤시안">
  <mi>H</mi><mo>=</mo><msup><mo>&nabla;</mo><mn>2</mn></msup><mi>&phi;</mi><mo>(</mo><msup><mi>z</mi><mo>*</mo></msup><mo>)</mo><mo>.</mo>
</math>

PEAR는 먼저 <math><msup><mi>H</mi><mrow><mo>&minus;</mo><mn>1</mn></mrow></msup></math>로 오차의 크기를 조정하고, 그다음 <math><mi>H</mi></math>가 정하는 거리 아래에서 접공간으로 투영한다. 따라서 전체 연산을 단순한 유클리드 투영이라고 부르면 정확하지 않다. <math><mi>H</mi><mo>=</mo><mi>&alpha;</mi><mi>I</mi></math>일 때만 두 해석이 사실상 같아진다.

## 4. 투영된 오차가 실제 후회값의 기울기가 된다

작은 변화에 대해 활성 제약집합이 바뀌지 않는다고 하자. 국소 KKT 조건은

<math display="block" aria-label="국소 KKT 조건">
  <mo>&nabla;</mo><mi>&phi;</mi><mo>(</mo><msup><mi>z</mi><mo>*</mo></msup><mo>)</mo>
  <mo>+</mo><mover accent="true"><mi>c</mi><mo>^</mo></mover>
  <mo>+</mo><msup><mi>J</mi><mo>&top;</mo></msup><msup><mi>y</mi><mo>*</mo></msup><mo>=</mo><mn>0</mn><mo>,</mo>
  <mspace width="0.8em"/>
  <mi>J</mi><msup><mi>z</mi><mo>*</mo></msup><mo>=</mo><mover><mi>b</mi><mo>~</mo></mover><mo>.</mo>
</math>

이다. 이를 미분하면

<math display="block" aria-label="미분한 KKT 연립방정식">
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

쌍대변수의 변화를 슈어 여수로 제거하면 다음을 얻는다.

<math display="block" aria-label="투영된 민감도 연산자">
  <mi>d</mi><mi>z</mi><mo>=</mo><mo>&minus;</mo><msub><mi>P</mi><mi>H</mi></msub><mi>d</mi><mover accent="true"><mi>c</mi><mo>^</mo></mover><mo>,</mo>
  <mspace width="0.7em"/>
  <msub><mi>P</mi><mi>H</mi></msub>
  <mo>=</mo><msup><mi>H</mi><mrow><mo>&minus;</mo><mn>1</mn></mrow></msup>
  <mo>&minus;</mo>
  <msup><mi>H</mi><mrow><mo>&minus;</mo><mn>1</mn></mrow></msup><msup><mi>J</mi><mo>&top;</mo></msup>
  <msup><mrow><mo>(</mo><mi>J</mi><msup><mi>H</mi><mrow><mo>&minus;</mo><mn>1</mn></mrow></msup><msup><mi>J</mi><mo>&top;</mo></msup><mo>)</mo></mrow><mrow><mo>&minus;</mo><mn>1</mn></mrow></msup>
  <mi>J</mi><msup><mi>H</mi><mrow><mo>&minus;</mo><mn>1</mn></mrow></msup><mo>.</mo>
</math>

예측 오차를 <math><mi>e</mi><mo>=</mo><mover accent="true"><mi>c</mi><mo>^</mo></mover><mo>&minus;</mo><mi>c</mi></math>라고 하자. 정상성 조건을 이용하면 <math><mo>&nabla;</mo><mi>&phi;</mi><mo>(</mo><msup><mi>z</mi><mo>*</mo></msup><mo>)</mo><mo>+</mo><mi>c</mi><mo>=</mo><mo>&minus;</mo><mi>e</mi><mo>&minus;</mo><msup><mi>J</mi><mo>&top;</mo></msup><msup><mi>y</mi><mo>*</mo></msup></math>이다. 또 <math><msub><mi>P</mi><mi>H</mi></msub><msup><mi>J</mi><mo>&top;</mo></msup><mo>=</mo><mn>0</mn></math>이므로 연쇄법칙에서 쌍대변수 항이 사라진다.

<math display="block" aria-label="정확한 국소 후회값 기울기">
  <msub><mo>&nabla;</mo><mover accent="true"><mi>c</mi><mo>^</mo></mover></msub><mi mathvariant="script">R</mi>
  <mo>=</mo><msub><mi>P</mi><mi>H</mi></msub>
  <mo>(</mo><mover accent="true"><mi>c</mi><mo>^</mo></mover><mo>&minus;</mo><mi>c</mi><mo>)</mo><mo>.</mo>
</math>

이것이 논문의 핵심 정리다. 가정이 성립하는 범위에서는 PEAR가 그럴듯한 대체 방향을 만드는 것이 아니다. 예측된 선형 계수에 대한 실제 후회값의 국소 기울기와 정확히 일치한다.

## 5. 구현에서는 역전파 신호를 바꾼다

공개된 이차계획 코드는 순전파에서 평범한 제곱오차를 반환한다. 대신 역전파 함수를 직접 정의해 평균제곱오차의 기울기 대신 <math><msub><mi>P</mi><mi>H</mi></msub><mi>e</mi></math>를 신경망에 전달한다. 따라서 PEAR는 새로운 스칼라 손실함수라기보다 사용자 정의 기울기 규칙으로 이해하는 편이 정확하다.

<math><msub><mi>P</mi><mi>H</mi></msub></math>라는 <math><mi>n</mi><mo>&times;</mo><mi>n</mi></math> 행렬 전체를 만들 필요는 없다. 활성 제약조건이 <math><mi>k</mi></math>개라면 다음 연립방정식을 푼다.

<math display="block" aria-label="PEAR가 사용하는 슈어 여수 연립방정식">
  <mo>(</mo><mi>J</mi><msup><mi>H</mi><mrow><mo>&minus;</mo><mn>1</mn></mrow></msup><msup><mi>J</mi><mo>&top;</mo></msup><mo>)</mo><mi>v</mi>
  <mo>=</mo><mi>J</mi><msup><mi>H</mi><mrow><mo>&minus;</mo><mn>1</mn></mrow></msup><mi>e</mi>
</math>

그다음 아래 값을 역전파한다.

<math display="block" aria-label="PEAR 역전파 신호">
  <mi>g</mi><mo>=</mo><msup><mi>H</mi><mrow><mo>&minus;</mo><mn>1</mn></mrow></msup><mi>e</mi>
  <mo>&minus;</mo><msup><mi>H</mi><mrow><mo>&minus;</mo><mn>1</mn></mrow></msup><msup><mi>J</mi><mo>&top;</mo></msup><mi>v</mi><mo>.</mo>
</math>

핵심 연립방정식의 크기는 <math><mi>k</mi><mo>&times;</mo><mi>k</mi></math>다. 활성 제약조건이 적고 <math><mi>H</mi></math>에 대한 선형연립방정식을 싸게 풀 수 있을 때 계산상 이점이 생긴다.

## 6. 정확한 정리가 끝나는 지점

앞의 유도에는 <math><mi>H</mi><mo>&succ;</mo><mn>0</mn></math>, 활성 제약조건의 선형독립성, 엄격한 상보성이라는 조건이 필요하다. 이 조건들이 활성 제약집합을 국소적으로 고정하고 최적해 사상을 미분 가능하게 만든다. 따라서 정리는 국소 결과다. 활성 제약집합의 경계를 넘으면 <math><mi>J</mi></math>가 바뀌고 기울기가 매끄럽지 않을 수 있다.

순수 선형계획에서는 <math><mi>H</mi><mo>=</mo><mn>0</mn></math>이므로 곡률 조건이 성립하지 않는다. 선형계획의 최적해는 비용계수에 대해 구간별로 일정하다. 비용이 조금 변해도 같은 꼭짓점이 최적해로 남다가, 법선뿔의 경계를 넘으면 다른 꼭짓점으로 갑자기 이동한다.

논문은 다음과 같은 이차 평활화를 추가한다.

<math display="block" aria-label="선형계획을 위한 이차 평활화">
  <mi>&phi;</mi><mo>(</mo><mi>z</mi><mo>)</mo>
  <mo>=</mo><mfrac><mi>&lambda;</mi><mn>2</mn></mfrac><msup><mrow><mo>&Vert;</mo><mi>z</mi><mo>&Vert;</mo></mrow><mn>2</mn></msup><mo>,</mo>
  <mspace width="0.7em"/><mi>H</mi><mo>=</mo><mi>&lambda;</mi><mi>I</mi><mo>.</mo>
</math>

이때 얻는 기울기는 원래 선형계획이 아니라 평활화된 문제의 기울기다. 구현에서는 여기에 정규화된 법선성분도 더한다.

<math display="block" aria-label="법선성분 주입">
  <mi>n</mi><mo>=</mo><msup><mi>&lambda;</mi><mrow><mo>&minus;</mo><mn>1</mn></mrow></msup><msup><mi>J</mi><mo>&top;</mo></msup><mi>v</mi><mo>,</mo>
  <mspace width="0.7em"/>
  <msub><mi>g</mi><mtext>inj</mtext></msub>
  <mo>=</mo><mi>g</mi><mo>+</mo><mi>&beta;</mi>
  <mfrac><mrow><mo>&Vert;</mo><mi>g</mi><mo>&Vert;</mo></mrow><mrow><mo>&Vert;</mo><mi>n</mi><mo>&Vert;</mo></mrow></mfrac><mi>n</mi><mo>.</mo>
</math>

평평한 선형계획 영역을 벗어나기 위한 실용적 장치로는 이해할 수 있다. 그러나 이는 경험적 보정이다. 원래 기하학적 설명에서 의사결정과 무관하다고 제거한 법선방향을 다시 넣는 것이기도 하다. 엄밀히 볼록한 이차계획의 정확한 결과, 평활화된 선형계획의 기울기, 법선성분까지 넣은 선형계획의 학습방향은 서로 다른 주장이다.

## 7. 포트폴리오 실험에서는 공분산 경로가 빠진다

포트폴리오 문제는 다음과 같다.

<math display="block" aria-label="평균 분산 포트폴리오 문제">
  <munder><mo>min</mo><mi>w</mi></munder>
  <mspace width="0.5em"/>
  <mfrac><mi>&lambda;</mi><mn>2</mn></mfrac><msup><mi>w</mi><mo>&top;</mo></msup><mi>&Sigma;</mi><mi>w</mi>
  <mo>&minus;</mo><msup><mi>&mu;</mi><mo>&top;</mo></msup><mi>w</mi>
  <mspace width="0.8em"/><mtext>제약조건</mtext><mspace width="0.5em"/>
  <msup><mn>1</mn><mo>&top;</mo></msup><mi>w</mi><mo>=</mo><mn>1</mn><mo>,</mo>
  <mspace width="0.4em"/><mi>w</mi><mo>&ge;</mo><mn>0</mn><mo>.</mo>
</math>

공분산 <math><mi>&Sigma;</mi></math>가 고정되고 평균수익률 <math><mi>&mu;</mi></math>만 예측된다면 논문의 정리와 정확히 맞는다. 그러나 실험에서는 신경망이 21일 수익률 경로를 예측한다. 이 예측으로 평균수익률뿐 아니라 과거 및 예측 수익률을 결합한 공분산도 만든다. 따라서 실제 결정은 <math><msup><mi>w</mi><mo>*</mo></msup><mo>(</mo><mover accent="true"><mi>&mu;</mi><mo>^</mo></mover><mo>,</mo><mover accent="true"><mi>&Sigma;</mi><mo>^</mo></mover><mo>)</mo></math>이고, 예측 수익률에 대한 전체 미분에는 두 경로가 있어야 한다.

<math display="block" aria-label="평균과 공분산을 통한 미분 경로">
  <mfrac><mrow><mi>d</mi><mi mathvariant="script">R</mi></mrow><mrow><mi>d</mi><mover accent="true"><mi>r</mi><mo>^</mo></mover></mrow></mfrac>
  <mo>=</mo>
  <mfrac><mrow><mo>&part;</mo><mi mathvariant="script">R</mi></mrow><mrow><mo>&part;</mo><mover accent="true"><mi>&mu;</mi><mo>^</mo></mover></mrow></mfrac>
  <mfrac><mrow><mo>&part;</mo><mover accent="true"><mi>&mu;</mi><mo>^</mo></mover></mrow><mrow><mo>&part;</mo><mover accent="true"><mi>r</mi><mo>^</mo></mover></mrow></mfrac>
  <mo>+</mo>
  <mfrac><mrow><mo>&part;</mo><mi mathvariant="script">R</mi></mrow><mrow><mo>&part;</mo><mover accent="true"><mi>&Sigma;</mi><mo>^</mo></mover></mrow></mfrac>
  <mfrac><mrow><mo>&part;</mo><mover accent="true"><mi>&Sigma;</mi><mo>^</mo></mover></mrow><mrow><mo>&part;</mo><mover accent="true"><mi>r</mi><mo>^</mo></mover></mrow></mfrac><mo>.</mo>
</math>

공개 코드의 PEAR 역전파는 예측 평균에는 투영 기울기를 반환하지만 예측 공분산에는 `None`을 반환한다. 즉 현재 공분산을 고정한 채 평균에 대한 편미분만 계산한다. 반면 미분 가능한 이차계획 비교방법은 두 입력을 모두 통해 기울기를 전달할 수 있다. 별도의 제거실험이 없으므로 PEAR의 포트폴리오 성능이 투영에서 얼마나 왔고 공분산 기울기 차단에서 얼마나 왔는지 분리하기 어렵다.

## 8. 계산상 이점은 문제 구조에 달려 있다

PEAR는 유한한 허용오차로 계산된 원문제 및 쌍대문제의 해에서 활성 제약집합을 찾는다. 거의 활성화된 제약조건은 판정 기준이 조금만 바뀌어도 집합에 들어오거나 빠질 수 있다. 퇴화점 근처에서는 <math><mi>J</mi></math>가 불안정하고 <math><mi>J</mi><msup><mi>H</mi><mrow><mo>&minus;</mo><mn>1</mn></mrow></msup><msup><mi>J</mi><mo>&top;</mo></msup></math>의 조건수가 나빠질 수 있다. 미분 가능한 최적화기보다 수치적으로 안정적인지는 정리가 아니라 실험으로 확인해야 할 문제다.

계산시간도 구조에 좌우된다. <math><mi>k</mi><mo>&ll;</mo><mi>n</mi></math>이고 헤시안이 희소하거나 대각행렬이거나 이미 분해되어 있을 때 PEAR가 가장 유리하다. 희소 포트폴리오처럼 많은 비음수 제약이 활성화되면 <math><mi>k</mi></math>가 <math><mi>n</mi></math>에 가까워질 수 있다. 조밀한 공분산 행렬을 사용하면 <math><mi>H</mi></math>에 대한 연립방정식도 여전히 비싸다.

## 9. 결과는 강하지만 모든 조건에서 이기지는 않는다

선형계획 실험은 5×5 최단경로 문제와 100개 물품의 배낭문제를 사용한다. 입력에서 비용으로 가는 함수의 다항식 차수를 높여 예측 난도를 조절한다. 배낭문제에서 PEAR와 LAVA는 선형계획 완화문제로 학습하고, 평가는 원래 정수문제에서 수행한다.

다항식 차수 8인 배낭문제의 정규화 후회값은 MSE 2.285%, SPO+ 0.763%, PEAR 0.437%다. 차수 8 최단경로에서도 PEAR가 4.246%로 가장 좋다. 그러나 모든 조건에서 이기는 것은 아니다. 차수 4에서는 SPO+가 0.761%, PEAR가 0.774%다. 따라서 “모든 비교방법보다 가장 좋은 의사결정 품질”이라는 문구는 표가 보여 주는 범위보다 조금 넓다.

포트폴리오 비교에서 PEAR의 학습시간은 122.3초로 QPTH의 147.6초와 CVXPYLayers의 321.9초보다 짧다. MSE는 33.0초다. 따라서 PEAR를 아무 조건 없이 가장 빠른 방법이라고 하기보다는, 의사결정 중심 학습방법 중 비교적 빠른 방법이라고 하는 편이 정확하다.

포트폴리오 결과는 유망하지만 변동이 크다. PEAR는 정규화 후회값 85.38%, 샤프지수 1.44, 가장 낮은 최대낙폭을 기록했다. 다섯 개 초기값에서 누적수익률은 PEAR가 <math><mn>184.19</mn><mo>&PlusMinus;</mo><mn>86.24</mn><mo>%</mo></math>, QPTH가 <math><mn>139.77</mn><mo>&PlusMinus;</mo><mn>115.74</mn><mo>%</mo></math>다. 이 정도 불확실성으로 경제적 우위를 확정하기는 어렵다.

제약조건을 바꾼 실험은 방법의 한계를 더 분명하게 보여 준다. 학습 때와 다른 출발점 및 도착점을 사용하는 최단경로 문제에서는 모든 다항식 차수에서 MSE가 가장 좋다. 차수 8의 결과는 MSE 14.00, PEAR 21.42, SPO+ 43.40이다. 의사결정 중심 학습은 학습 당시의 최적화 구조에 맞춰 예측 정확도를 집중한다. 시험 시점의 제약구조가 달라지면 같은 특화가 전이성능을 떨어뜨릴 수 있다.

## 10. 판단

논문의 핵심 정리는 단순하면서 유용하다. 같은 시스템을 반복해서 풀되 선형 목적함수 계수만 달라지는 엄밀히 볼록한 문제에서는, 예측 오차에 곡률 조정과 접공간 투영을 적용하면 실제 후회값의 기울기가 된다. 어떤 예측 오차에 학습 능력을 집중해야 하는지 분명한 답을 준다.

한계도 구체적이다. 선형계획 버전은 평활화한 뒤 경험적 보정을 추가한 방법이다. 포트폴리오 구현은 공분산을 통한 기울기 경로를 빠뜨린다. 속도상 이점은 작고 안정적인 활성 제약집합과 계산하기 쉬운 헤시안에 의존한다. 이 문제들이 핵심 정리를 반박하는 것은 아니다. 정리와 더 넓은 실험방법 사이의 경계를 보여 줄 뿐이다.

## 참고문헌

Junhyeong Lee, Sangjin Jin, and Yongjae Lee. *Decision-Focused Learning via Tangent-Space Projection of Prediction Error*. ICML, 2026. 검토 자료에는 원문 링크, DOI, arXiv 식별자가 제공되지 않았다.
