---
layout: post
title: "OptNet: Differentiating Optimal Actions Through a QP Layer"
title_ko: "OptNet: QP layer의 최적 action을 거쳐 미분하기"
date: 2026-10-11
category: stochastic-nonlinear-optimization
category_label: "Mathematical Optimization"
research_group: algorithmic_reviews
research_category: stochastic-nonlinear-optimization
research_category_label: "Mathematical Optimization"
application_category: ""
application_category_label: ""
method_category: "stochastic-nonlinear-optimization"
method_category_label: "Mathematical Optimization"
paper_title: "OptNet: Differentiable Optimization as a Layer in Neural Networks"
authors: "Brandon Amos and J. Zico Kolter"
venue: "ICML, PMLR 70, pp. 136–145"
year: "2017"
doi: ""
arxiv: "1703.00443"
source_url: "https://proceedings.mlr.press/v70/amos17a.html"
tags:
  - "OptNet"
  - "differentiable optimization"
  - "quadratic programming"
  - "implicit differentiation"
  - "KKT"
  - "hard ramp"
  - "optimal actions"
  - "neural networks"
excerpt: "A hard ramp example separates function-value gradients from action sensitivity, then derives forward and backward passes through the KKT equations of a quadratic program."
excerpt_ko: "Hard ramp 예제로 함수값의 미분과 action 민감도를 구분하고, QP의 KKT 조건을 통해 forward·backward pass를 유도한다."
language: "en-ko"
has_korean_note: false
---

Amos and Kolter's ICML 2017 paper, *OptNet: Differentiable Optimization as a Layer in Neural Networks*, uses a QP's **optimal solution as a neural-network layer output** and differentiates through that solution.

The motivating question is concrete: “If an action chosen by optimization performs poorly, how should the parameters that produced that action change?” The derivative of a function value at a fixed action and the derivative of the selected action are different objects:

<math display="block" aria-label="Value derivative at a fixed action versus optimal action derivative"><mtable columnalign="left"><mtr><mtd><mfrac><mrow><mo>∂</mo><msub><mover><mi>V</mi><mo>^</mo></mover><mi>θ</mi></msub><mo>(</mo><mi>x</mi><mo>,</mo><mi>a</mi><mo>)</mo></mrow><mrow><mo>∂</mo><mi>θ</mi></mrow></mfrac></mtd></mtr><mtr><mtd><mfrac><mrow><mo>∂</mo><msub><msup><mi>a</mi><mo>*</mo></msup><mi>θ</mi></msub><mo>(</mo><mi>x</mi><mo>)</mo></mrow><mrow><mo>∂</mo><mi>θ</mi></mrow></mfrac></mtd></mtr></mtable></math>

The first asks how a predicted value changes while holding the action fixed. The second asks how the optimizer's chosen action changes when the parameters change. OptNet provides a way to compute the latter and train a model containing the optimization operation.

## 1. Forward pass: choose an action under a hard ramp limit

The following is an educational example for equipment operation, not an experiment from the paper. Let a be normalized equipment output, with a previous output of 0.5 and a hard ramp limit of 0.1:

<math display="block" aria-label="Normalized output and hard ramp constraint"><mtable columnalign="left"><mtr><mtd><mn>0</mn><mo>≤</mo><mi>a</mi><mo>≤</mo><mn>1</mn><mo>,</mo><msub><mi>a</mi><mtext>prev</mtext></msub><mo>=</mo><mn>.5</mn></mtd></mtr><mtr><mtd><mo>|</mo><mi>a</mi><mo>−</mo><msub><mi>a</mi><mtext>prev</mtext></msub><mo>|</mo><mo>≤</mo><mn>.1</mn><mo>⇒</mo><mn>.4</mn><mo>≤</mo><mi>a</mi><mo>≤</mo><mn>.6</mn></mtd></mtr></mtable></math>

A neural network takes observations x and predicts one number, <math><msub><mi>η</mi><mi>θ</mi></msub><mo>(</mo><mi>x</mi><mo>)</mo></math>. Do not use it directly as the action. Pass it to this QP:

<math display="block" aria-label="A unique optimal solution with a kink"><mtable columnalign="left"><mtr><mtd><msup><mi>a</mi><mo>*</mo></msup><mo>(</mo><mi>η</mi><mo>)</mo><mo>=</mo><munder><mo>arg min</mo><mrow><mn>.4</mn><mo>≤</mo><mi>a</mi><mo>≤</mo><mn>.6</mn></mrow></munder><mo>(</mo><mfrac><mrow><mn>1</mn></mrow><mrow><mn>2</mn></mrow></mfrac><msup><mi>a</mi><mn>2</mn></msup><mo>−</mo><mi>η</mi><mi>a</mi><mo>)</mo></mtd></mtr><mtr><mtd><msup><mi>a</mi><mo>*</mo></msup><mo>(</mo><mi>η</mi><mo>)</mo><mo>=</mo><mo>min</mo><mo>{</mo><mn>.6</mn><mo>,</mo><mo>max</mo><mo>{</mo><mn>.4</mn><mo>,</mo><mi>η</mi><mo>}</mo><mo>}</mo></mtd></mtr></mtable></math>

Here <math><mi>η</mi></math> is an incentive to increase output. A larger incentive favors higher output, but the modeled hard ramp constraint must still hold. Completing the square explains what the optimizer does:

<math display="block" aria-label="Complete the square to interpret the QP as projection"><mfrac><mrow><mn>1</mn></mrow><mrow><mn>2</mn></mrow></mfrac><msup><mi>a</mi><mn>2</mn></msup><mo>−</mo><mi>η</mi><mi>a</mi><mo>=</mo><mfrac><mrow><mn>1</mn></mrow><mrow><mn>2</mn></mrow></mfrac><msup><mo>(</mo><mi>a</mi><mo>−</mo><mi>η</mi><mo>)</mo><mn>2</mn></msup><mo>−</mo><mfrac><mrow><mn>1</mn></mrow><mrow><mn>2</mn></mrow></mfrac><msup><mi>η</mi><mn>2</mn></msup></math>

The final term is independent of a. Therefore the optimizer selects the feasible action closest to <math><mi>η</mi></math>:

<math display="block" aria-label="Piecewise optimal action"><msup><mi>a</mi><mo>*</mo></msup><mo>(</mo><mi>η</mi><mo>)</mo><mo>=</mo><mo>{</mo><mtable columnalign="left left"><mtr><mtd><mn>.4</mn></mtd><mtd><mi>η</mi><mo>&lt;</mo><mn>.4</mn></mtd></mtr><mtr><mtd><mi>η</mi></mtd><mtd><mn>.4</mn><mo>≤</mo><mi>η</mi><mo>≤</mo><mn>.6</mn></mtd></mtr><mtr><mtd><mn>.6</mn></mtd><mtd><mi>η</mi><mo>&gt;</mo><mn>.6</mn></mtd></mtr></mtable></math>

When <math><mi>η</mi></math> = 0.45, the action is 0.45. When <math><mi>η</mi></math> = 0.8, the action is 0.6. The network can prefer a higher output, but the QP returns the upper feasible output.

<math display="block" aria-label="Forward pass returns an optimal action"><mi>x</mi><mo>→</mo><msub><mi>η</mi><mi>θ</mi></msub><mo>(</mo><mi>x</mi><mo>)</mo><mo>→</mo><mtext>QP solve</mtext><mo>→</mo><msub><msup><mi>a</mi><mo>*</mo></msup><mi>θ</mi></msub><mo>(</mo><mi>x</mi><mo>)</mo></math>

The layer output is the optimal decision, **not the minimum objective value**. In numerical implementation, satisfaction of modeled constraints is subject to solver tolerances; the exact mathematical example satisfies them exactly.

## 2. Backward pass: what can a poor action teach the network?

For one input, suppose a reference action of 0.55 is given. This is a hypothetical training label to demonstrate differentiation. It does not assume that optimal-action labels are available in the real operating problem.

<math display="block" aria-label="Illustrative supervised action loss"><mi>ℓ</mi><mo>(</mo><mi>θ</mi><mo>)</mo><mo>=</mo><mfrac><mrow><mn>1</mn></mrow><mrow><mn>2</mn></mrow></mfrac><msup><mo>(</mo><msub><msup><mi>a</mi><mo>*</mo></msup><mi>θ</mi></msub><mo>(</mo><mi>x</mi><mo>)</mo><mo>−</mo><mn>.55</mn><mo>)</mo><mn>2</mn></msup></math>

The chain rule is

<math display="block" aria-label="Chain rule through the optimal action"><mfrac><mrow><mo>∂</mo><mi>ℓ</mi></mrow><mrow><mo>∂</mo><mi>θ</mi></mrow></mfrac><mo>=</mo><mfrac><mrow><mo>∂</mo><mi>ℓ</mi></mrow><mrow><mo>∂</mo><msup><mi>a</mi><mo>*</mo></msup></mrow></mfrac><mfrac><mrow><mo>∂</mo><msup><mi>a</mi><mo>*</mo></msup></mrow><mrow><mo>∂</mo><mi>η</mi></mrow></mfrac><mfrac><mrow><mo>∂</mo><msub><mi>η</mi><mi>θ</mi></msub><mo>(</mo><mi>x</mi><mo>)</mo></mrow><mrow><mo>∂</mo><mi>θ</mi></mrow></mfrac></math>

The first factor says which way the loss wants to move the action. The last factor propagates through the network. The middle factor <math><mfrac><mrow><mo>∂</mo><msup><mi>a</mi><mo>*</mo></msup></mrow><mrow><mo>∂</mo><mi>η</mi></mrow></mfrac></math> says whether changing the QP parameter actually moves the selected action.

### When no bound is active

<math display="block" aria-label="Gradient when no bound is active"><mtable columnalign="left"><mtr><mtd><mi>η</mi><mo>=</mo><mn>.45</mn><mo>⇒</mo><msup><mi>a</mi><mo>*</mo></msup><mo>=</mo><mn>.45</mn><mo>,</mo><mfrac><mrow><mo>∂</mo><msup><mi>a</mi><mo>*</mo></msup></mrow><mrow><mo>∂</mo><mi>η</mi></mrow></mfrac><mo>=</mo><mn>1</mn></mtd></mtr><mtr><mtd><mfrac><mrow><mo>∂</mo><mi>ℓ</mi></mrow><mrow><mo>∂</mo><mi>η</mi></mrow></mfrac><mo>=</mo><mo>(</mo><mn>.45</mn><mo>−</mo><mn>.55</mn><mo>)</mo><mo>·</mo><mn>1</mn><mo>=</mo><mo>−</mo><mn>.1</mn></mtd></mtr></mtable></math>

Gradient descent increases <math><mi>η</mi></math>, which increases the action toward 0.55. The optimizer lets the network's changed preference reach the decision.

### When the upper ramp bound is active

<math display="block" aria-label="The upper bound gives a locally zero action gradient"><mtable columnalign="left"><mtr><mtd><mi>η</mi><mo>=</mo><mn>.8</mn><mo>⇒</mo><msup><mi>a</mi><mo>*</mo></msup><mo>=</mo><mn>.6</mn></mtd></mtr><mtr><mtd><mfrac><mrow><mo>∂</mo><msup><mi>a</mi><mo>*</mo></msup></mrow><mrow><mo>∂</mo><mi>η</mi></mrow></mfrac><mo>=</mo><mn>0</mn><mo>,</mo><mfrac><mrow><mo>∂</mo><mi>ℓ</mi></mrow><mrow><mo>∂</mo><mi>η</mi></mrow></mfrac><mo>=</mo><mn>0</mn></mtd></mtr></mtable></math>

Reducing the incentive from 0.8 to 0.79 still returns action 0.6. The action is locally constant. Its loss is positive, but the gradient through this parameter path is zero.

**Being able to differentiate an optimization layer does not mean that its gradient is always informative for training.** In this example the constrained optimum is correct for the current objective, yet this local gradient cannot tell the network how far its incentive must move to leave saturation. Other parameter paths, losses, or a deliberate smoothing choice can change the learning behavior, but this calculation gives no automatic remedy.

At incentives 0.4 and 0.6 the action map has kinks. The QP is strongly convex and its optimum is unique, but ordinary differentiability still fails at those two points. Any derivative convention or generalized derivative used there must be distinguished from an ordinary derivative.

## 3. How can we differentiate a solution without a closed-form formula?

Clipping made the scalar example easy. With many variables and constraints, we usually do not have an explicit formula for the optimizer. OptNet differentiates the **KKT conditions satisfied at the solution**, rather than backpropagating through every iteration used by the solver to reach it.

### 3.1 Use the equations satisfied by the optimum

Consider the parameterized QP

<math display="block" aria-label="Parameterized positive definite quadratic program"><mtable columnalign="left"><mtr><mtd><msup><mi>a</mi><mo>*</mo></msup><mo>(</mo><mi>η</mi><mo>)</mo><mo>=</mo><munder><mo>arg min</mo><mi>a</mi></munder><mo>(</mo><mfrac><mrow><mn>1</mn></mrow><mrow><mn>2</mn></mrow></mfrac><msup><mrow><mi>a</mi></mrow><mo>⊤</mo></msup><mi>H</mi><mo>(</mo><mi>η</mi><mo>)</mo><mi>a</mi><mo>+</mo><msup><mrow><mi>c</mi><mo>(</mo><mi>η</mi><mo>)</mo></mrow><mo>⊤</mo></msup><mi>a</mi><mo>)</mo></mtd></mtr><mtr><mtd><mi>A</mi><mo>(</mo><mi>η</mi><mo>)</mo><mi>a</mi><mo>=</mo><mi>b</mi><mo>(</mo><mi>η</mi><mo>)</mo></mtd></mtr><mtr><mtd><mi>G</mi><mo>(</mo><mi>η</mi><mo>)</mo><mi>a</mi><mo>≤</mo><mi>h</mi><mo>(</mo><mi>η</mi><mo>)</mo></mtd></mtr></mtable></math>

Here <math><mi>η</mi></math> collects the parameters determining the objective and constraints. Assume the feasible set is nonempty and the symmetric Hessian satisfies <math><mi>H</mi><mo>≻</mo><mn>0</mn></math>. At each such parameter value the primal optimum exists and is unique. The affine constraints ensure KKT multipliers exist, although redundant constraints can make those multipliers nonunique.

Using equality multipliers ν and nonnegative inequality multipliers λ, and suppressing the parameter arguments, the KKT conditions are

<math display="block" aria-label="QP KKT equations and inequalities"><mtable columnalign="left"><mtr><mtd><mi>H</mi><msup><mi>a</mi><mo>*</mo></msup><mo>+</mo><mi>c</mi><mo>+</mo><msup><mrow><mi>A</mi></mrow><mo>⊤</mo></msup><msup><mi>ν</mi><mo>*</mo></msup><mo>+</mo><msup><mrow><mi>G</mi></mrow><mo>⊤</mo></msup><msup><mi>λ</mi><mo>*</mo></msup><mo>=</mo><mn>0</mn></mtd></mtr><mtr><mtd><mi>A</mi><msup><mi>a</mi><mo>*</mo></msup><mo>−</mo><mi>b</mi><mo>=</mo><mn>0</mn></mtd></mtr><mtr><mtd><msub><msup><mi>λ</mi><mo>*</mo></msup><mi>i</mi></msub><msub><mo>(</mo><mi>G</mi><msup><mi>a</mi><mo>*</mo></msup><mo>−</mo><mi>h</mi><mo>)</mo><mi>i</mi></msub><mo>=</mo><mn>0</mn></mtd></mtr><mtr><mtd><mi>G</mi><msup><mi>a</mi><mo>*</mo></msup><mo>−</mo><mi>h</mi><mo>≤</mo><mn>0</mn><mo>,</mo><msup><mi>λ</mi><mo>*</mo></msup><mo>≥</mo><mn>0</mn></mtd></mtr></mtable></math>

Collect the primal and dual solution variables:

<math display="block" aria-label="Primal and dual solution variables"><msup><mi>y</mi><mo>*</mo></msup><mo>=</mo><mo>[</mo><mtable><mtr><mtd><msup><mi>a</mi><mo>*</mo></msup></mtd></mtr><mtr><mtd><msup><mi>λ</mi><mo>*</mo></msup></mtd></mtr><mtr><mtd><msup><mi>ν</mi><mo>*</mo></msup></mtd></mtr></mtable><mo>]</mo></math>

Write the **equality part** of KKT as the following residual, with all QP data evaluated at <math><mi>η</mi></math>:

<math display="block" aria-label="Equality part of the KKT residual"><mi>F</mi><mo>(</mo><mi>y</mi><mo>,</mo><mi>η</mi><mo>)</mo><mo>=</mo><mo>[</mo><mtable><mtr><mtd><mi>H</mi><mi>a</mi><mo>+</mo><mi>c</mi><mo>+</mo><msup><mrow><mi>G</mi></mrow><mo>⊤</mo></msup><mi>λ</mi><mo>+</mo><msup><mrow><mi>A</mi></mrow><mo>⊤</mo></msup><mi>ν</mi></mtd></mtr><mtr><mtd><mo>diag</mo><mo>(</mo><mi>λ</mi><mo>)</mo><mo>(</mo><mi>G</mi><mi>a</mi><mo>−</mo><mi>h</mi><mo>)</mo></mtd></mtr><mtr><mtd><mi>A</mi><mi>a</mi><mo>−</mo><mi>b</mi></mtd></mtr></mtable><mo>]</mo></math>

At the primal–dual optimum the residual is zero. Primal inequality feasibility and nonnegative inequality multipliers are still required. A zero equality residual alone does not certify an arbitrary point.

### 3.2 Differentiate the residual equation

Ask: “After a small parameter change, how must the solution move so that the KKT equations remain true?” Differentiating the zero-residual relation gives

<math display="block" aria-label="Differentiate a zero KKT residual"><msub><mi>F</mi><mi>y</mi></msub><mfrac><mrow><mo>∂</mo><msup><mi>y</mi><mo>*</mo></msup></mrow><mrow><mo>∂</mo><mi>η</mi></mrow></mfrac><mo>+</mo><msub><mi>F</mi><mi>η</mi></msub><mo>=</mo><mn>0</mn></math>

The first term is the residual change caused by motion of the primal–dual solution. The second is the direct parameter effect, evaluated while holding those variables fixed. When the residual is continuously differentiable and <math><msub><mi>F</mi><mi>y</mi></msub></math> is nonsingular, the implicit function theorem yields

<math display="block" aria-label="Implicit solution derivative when the Jacobian is nonsingular"><mfrac><mrow><mo>∂</mo><msup><mi>y</mi><mo>*</mo></msup></mrow><mrow><mo>∂</mo><mi>η</mi></mrow></mfrac><mo>=</mo><mo>−</mo><msup><msub><mi>F</mi><mi>y</mi></msub><mrow><mo>−</mo><mn>1</mn></mrow></msup><msub><mi>F</mi><mi>η</mi></msub></math>

The useful computational statement is a linear system:

<math display="block" aria-label="Implicit differentiation requires an invertible residual Jacobian"><mtable columnalign="left"><mtr><mtd><mi>F</mi><mo>(</mo><msup><mi>y</mi><mo>*</mo></msup><mo>(</mo><mi>η</mi><mo>)</mo><mo>,</mo><mi>η</mi><mo>)</mo><mo>=</mo><mn>0</mn></mtd></mtr><mtr><mtd><msub><mi>F</mi><mi>y</mi></msub><mfrac><mrow><mo>∂</mo><msup><mi>y</mi><mo>*</mo></msup></mrow><mrow><mo>∂</mo><mi>η</mi></mrow></mfrac><mo>=</mo><mo>−</mo><msub><mi>F</mi><mi>η</mi></msub></mtd></mtr></mtable></math>

An implementation solves the system instead of forming an explicit inverse.

For this QP residual, the Jacobian has the block structure

<math display="block" aria-label="Jacobian of the equality residual at a KKT solution"><msub><mi>F</mi><mi>y</mi></msub><mo>=</mo><mo>[</mo><mtable><mtr><mtd><mi>H</mi></mtd><mtd><msup><mrow><mi>G</mi></mrow><mo>⊤</mo></msup></mtd><mtd><msup><mrow><mi>A</mi></mrow><mo>⊤</mo></msup></mtd></mtr><mtr><mtd><mo>diag</mo><mo>(</mo><msup><mi>λ</mi><mo>*</mo></msup><mo>)</mo><mi>G</mi></mtd><mtd><mo>diag</mo><mo>(</mo><mi>G</mi><msup><mi>a</mi><mo>*</mo></msup><mo>−</mo><mi>h</mi><mo>)</mo></mtd><mtd><mn>0</mn></mtd></mtr><mtr><mtd><mi>A</mi></mtd><mtd><mn>0</mn></mtd><mtd><mn>0</mn></mtd></mtr></mtable><mo>]</mo></math>

The positive definiteness of H alone does not ensure this whole matrix is invertible. Redundant active constraints or an active inequality with zero multiplier can cause singularity. Independent equality and active-inequality gradients, together with strict complementarity, are a familiar sufficient regularity set for a positive definite QP with smooth local data. An unchanged active set then permits a smooth local solution branch.

### 3.3 Recover the ramp derivative directly from KKT

Use lower-bound constraint 0.4 − a ≤ 0 and upper-bound constraint a − 0.6 ≤ 0. Their KKT equations include

<math display="block" aria-label="Scalar ramp KKT equations"><mtable columnalign="left"><mtr><mtd><mi>a</mi><mo>−</mo><mi>η</mi><mo>−</mo><msub><mi>λ</mi><mtext>lower</mtext></msub><mo>+</mo><msub><mi>λ</mi><mtext>upper</mtext></msub><mo>=</mo><mn>0</mn></mtd></mtr><mtr><mtd><msub><mi>λ</mi><mtext>lower</mtext></msub><mo>(</mo><mn>.4</mn><mo>−</mo><mi>a</mi><mo>)</mo><mo>=</mo><mn>0</mn></mtd></mtr><mtr><mtd><msub><mi>λ</mi><mtext>upper</mtext></msub><mo>(</mo><mi>a</mi><mo>−</mo><mn>.6</mn><mo>)</mo><mo>=</mo><mn>0</mn></mtd></mtr></mtable></math>

At incentive 0.45 both multipliers are zero and remain so locally. Differentiating stationarity gives da = dη, hence <math><mfrac><mrow><mo>∂</mo><msup><mi>a</mi><mo>*</mo></msup></mrow><mrow><mo>∂</mo><mi>η</mi></mrow></mfrac></math> = 1.

At incentive 0.8 the upper multiplier is positive. Differentiate its complementarity equation:

<math display="block" aria-label="Differentiating complementarity at a strictly active upper bound"><mtable columnalign="left"><mtr><mtd><msub><msup><mi>λ</mi><mo>*</mo></msup><mtext>upper</mtext></msub><mo>=</mo><mi>η</mi><mo>−</mo><mn>.6</mn><mo>=</mo><mn>.2</mn></mtd></mtr><mtr><mtd><msub><msup><mi>λ</mi><mo>*</mo></msup><mtext>upper</mtext></msub><mi>d</mi><mi>a</mi><mo>+</mo><mo>(</mo><msup><mi>a</mi><mo>*</mo></msup><mo>−</mo><mn>.6</mn><mo>)</mo><mi>d</mi><msub><mi>λ</mi><mtext>upper</mtext></msub><mo>=</mo><mn>0</mn></mtd></mtr><mtr><mtd><mn>.2</mn><mi>d</mi><mi>a</mi><mo>=</mo><mn>0</mn><mo>⇒</mo><mfrac><mrow><mo>∂</mo><msup><mi>a</mi><mo>*</mo></msup></mrow><mrow><mo>∂</mo><mi>η</mi></mrow></mfrac><mo>=</mo><mn>0</mn></mtd></mtr></mtable></math>

The action cannot move to first order; the upper multiplier absorbs the changed incentive. At incentive 0.6, both the upper slack and multiplier are zero. The corresponding complementarity row has zero first derivative, the residual Jacobian is singular, and the inverse formula does not apply. This matches the kink in the explicit clipping solution.

## 4. Backpropagation needs a product, not the whole Jacobian

For a scalar loss that depends on <math><mi>η</mi></math> through the solution, solve an adjoint system:

<math display="block" aria-label="Adjoint solve for a scalar loss"><mtable columnalign="left"><mtr><mtd><msup><mrow><msub><mi>F</mi><mi>y</mi></msub></mrow><mo>⊤</mo></msup><mi>v</mi><mo>=</mo><msub><mo>∇</mo><mi>y</mi></msub><mi>ℓ</mi></mtd></mtr><mtr><mtd><msub><mo>∇</mo><mi>η</mi></msub><mi>ℓ</mi><mo>=</mo><mo>−</mo><msup><mrow><msub><mi>F</mi><mi>η</mi></msub></mrow><mo>⊤</mo></msup><mi>v</mi></mtd></mtr></mtable></math>

If the loss also depends directly on the QP parameter, add that direct partial derivative to the final gradient. The adjoint computes the needed Jacobian product without constructing a sensitivity matrix for every parameter.

OptNet's solver uses a primal–dual interior-point method and reuses matrix-factorization work from the forward solve in the backward calculation. This reduces extra backward work in that implementation. It is not a general claim that solving and differentiating any constrained optimization problem costs nothing.

The calculation rests on the zero KKT residual and its local regularity. Feasibility, solution uniqueness, ordinary differentiability, and a useful training gradient each require their own check. The hard ramp example makes those distinctions visible even with a single decision variable.

## References

- Amos, B., and Kolter, J. Z. (2017). *OptNet: Differentiable Optimization as a Layer in Neural Networks*. In *Proceedings of the 34th International Conference on Machine Learning*, PMLR 70, 136–145. [Official metadata](https://proceedings.mlr.press/v70/amos17a.html), [ICML paper PDF](https://proceedings.mlr.press/v70/amos17a/amos17a.pdf), [arXiv:1703.00443](https://arxiv.org/abs/1703.00443).
- *Implicit Layers Tutorial*, Chapter 5, “Differentiable optimization.” KKT residuals and implicit differentiation. [Tutorial chapter](https://implicit-layers-tutorial.org/differentiable_optimization/).

<!-- ko -->

Amos와 Kolter의 ICML 2017 논문 *OptNet: Differentiable Optimization as a Layer in Neural Networks*는 QP의 **최적해를 신경망 layer의 출력으로 사용하고, 그 최적해를 거쳐 역전파하는 방법**을 다룬다.

질문은 구체적이다. “최적화로 선택된 action이 좋지 않았다면, 그 action을 만들어낸 모델의 파라미터를 어떻게 수정할 것인가?” 고정된 action에서 함수값을 미분하는 것과 선택된 action 자체를 미분하는 것은 다르다.

<math display="block" aria-label="Value derivative at a fixed action versus optimal action derivative"><mtable columnalign="left"><mtr><mtd><mfrac><mrow><mo>∂</mo><msub><mover><mi>V</mi><mo>^</mo></mover><mi>θ</mi></msub><mo>(</mo><mi>x</mi><mo>,</mo><mi>a</mi><mo>)</mo></mrow><mrow><mo>∂</mo><mi>θ</mi></mrow></mfrac></mtd></mtr><mtr><mtd><mfrac><mrow><mo>∂</mo><msub><msup><mi>a</mi><mo>*</mo></msup><mi>θ</mi></msub><mo>(</mo><mi>x</mi><mo>)</mo></mrow><mrow><mo>∂</mo><mi>θ</mi></mrow></mfrac></mtd></mtr></mtable></math>

첫 번째는 action을 고정했을 때 예측값이 어떻게 달라지는지를 묻는다. 두 번째는 파라미터를 바꾸면 최적화가 선택하는 action이 어떻게 움직이는지를 묻는다. OptNet은 두 번째 미분을 계산하여 최적화 연산을 포함한 전체 모델을 학습할 수 있게 한다.

## 1. Forward pass: hard ramp를 지키는 action 선택

다음은 원 논문의 실험이 아니라 설비 운영을 이해하기 위한 **교육용 예제**이다. 정규화된 출력을 a라고 하고, 이전 출력은 0.5, hard ramp 제한은 0.1이라고 하자.

<math display="block" aria-label="Normalized output and hard ramp constraint"><mtable columnalign="left"><mtr><mtd><mn>0</mn><mo>≤</mo><mi>a</mi><mo>≤</mo><mn>1</mn><mo>,</mo><msub><mi>a</mi><mtext>prev</mtext></msub><mo>=</mo><mn>.5</mn></mtd></mtr><mtr><mtd><mo>|</mo><mi>a</mi><mo>−</mo><msub><mi>a</mi><mtext>prev</mtext></msub><mo>|</mo><mo>≤</mo><mn>.1</mn><mo>⇒</mo><mn>.4</mn><mo>≤</mo><mi>a</mi><mo>≤</mo><mn>.6</mn></mtd></mtr></mtable></math>

신경망은 관측정보 x를 받아 하나의 숫자 <math><msub><mi>η</mi><mi>θ</mi></msub><mo>(</mo><mi>x</mi><mo>)</mo></math>를 출력한다. 이 숫자를 바로 action으로 사용하지 않고 다음 QP에 넣는다.

<math display="block" aria-label="A unique optimal solution with a kink"><mtable columnalign="left"><mtr><mtd><msup><mi>a</mi><mo>*</mo></msup><mo>(</mo><mi>η</mi><mo>)</mo><mo>=</mo><munder><mo>arg min</mo><mrow><mn>.4</mn><mo>≤</mo><mi>a</mi><mo>≤</mo><mn>.6</mn></mrow></munder><mo>(</mo><mfrac><mrow><mn>1</mn></mrow><mrow><mn>2</mn></mrow></mfrac><msup><mi>a</mi><mn>2</mn></msup><mo>−</mo><mi>η</mi><mi>a</mi><mo>)</mo></mtd></mtr><mtr><mtd><msup><mi>a</mi><mo>*</mo></msup><mo>(</mo><mi>η</mi><mo>)</mo><mo>=</mo><mo>min</mo><mo>{</mo><mn>.6</mn><mo>,</mo><mo>max</mo><mo>{</mo><mn>.4</mn><mo>,</mo><mi>η</mi><mo>}</mo><mo>}</mo></mtd></mtr></mtable></math>

<math><mi>η</mi></math>는 출력을 증가시키려는 유인의 크기이다. 커질수록 높은 출력을 선호하지만, 모델에 넣은 hard ramp는 지켜야 한다. 목적함수를 완전제곱으로 바꾸면 동작이 분명해진다.

<math display="block" aria-label="Complete the square to interpret the QP as projection"><mfrac><mrow><mn>1</mn></mrow><mrow><mn>2</mn></mrow></mfrac><msup><mi>a</mi><mn>2</mn></msup><mo>−</mo><mi>η</mi><mi>a</mi><mo>=</mo><mfrac><mrow><mn>1</mn></mrow><mrow><mn>2</mn></mrow></mfrac><msup><mo>(</mo><mi>a</mi><mo>−</mo><mi>η</mi><mo>)</mo><mn>2</mn></msup><mo>−</mo><mfrac><mrow><mn>1</mn></mrow><mrow><mn>2</mn></mrow></mfrac><msup><mi>η</mi><mn>2</mn></msup></math>

마지막 항은 a와 무관하다. 따라서 <math><mi>η</mi></math>에 가장 가까운 feasible action을 선택하는 문제이다.

<math display="block" aria-label="Piecewise optimal action"><msup><mi>a</mi><mo>*</mo></msup><mo>(</mo><mi>η</mi><mo>)</mo><mo>=</mo><mo>{</mo><mtable columnalign="left left"><mtr><mtd><mn>.4</mn></mtd><mtd><mi>η</mi><mo>&lt;</mo><mn>.4</mn></mtd></mtr><mtr><mtd><mi>η</mi></mtd><mtd><mn>.4</mn><mo>≤</mo><mi>η</mi><mo>≤</mo><mn>.6</mn></mtd></mtr><mtr><mtd><mn>.6</mn></mtd><mtd><mi>η</mi><mo>&gt;</mo><mn>.6</mn></mtd></mtr></mtable></math>

<math><mi>η</mi></math> = 0.45이면 action은 0.45이다. <math><mi>η</mi></math> = 0.8을 출력해도 action은 0.6이다. 신경망이 더 높은 출력을 선호하더라도 QP는 feasible 상한을 반환한다.

<math display="block" aria-label="Forward pass returns an optimal action"><mi>x</mi><mo>→</mo><msub><mi>η</mi><mi>θ</mi></msub><mo>(</mo><mi>x</mi><mo>)</mo><mo>→</mo><mtext>QP solve</mtext><mo>→</mo><msub><msup><mi>a</mi><mo>*</mo></msup><mi>θ</mi></msub><mo>(</mo><mi>x</mi><mo>)</mo></math>

Layer의 출력은 **목적함수의 최솟값이 아니라 최적 의사결정**이다. 실제 수치 구현에서 모델 제약의 만족 정도는 solver tolerance의 영향을 받는다. 이 예제의 정확한 수학적 해는 제약을 정확히 만족한다.

## 2. Backward pass: 좋지 않은 action에서 무엇을 학습하는가?

어떤 입력에서 목표 action 0.55가 주어졌다고 하자. 미분을 보여주기 위한 가상의 학습 label이며, 실제 운영 문제에서 optimal-action label을 안다고 가정하는 것은 아니다.

<math display="block" aria-label="Illustrative supervised action loss"><mi>ℓ</mi><mo>(</mo><mi>θ</mi><mo>)</mo><mo>=</mo><mfrac><mrow><mn>1</mn></mrow><mrow><mn>2</mn></mrow></mfrac><msup><mo>(</mo><msub><msup><mi>a</mi><mo>*</mo></msup><mi>θ</mi></msub><mo>(</mo><mi>x</mi><mo>)</mo><mo>−</mo><mn>.55</mn><mo>)</mo><mn>2</mn></msup></math>

Chain rule은 다음과 같다.

<math display="block" aria-label="Chain rule through the optimal action"><mfrac><mrow><mo>∂</mo><mi>ℓ</mi></mrow><mrow><mo>∂</mo><mi>θ</mi></mrow></mfrac><mo>=</mo><mfrac><mrow><mo>∂</mo><mi>ℓ</mi></mrow><mrow><mo>∂</mo><msup><mi>a</mi><mo>*</mo></msup></mrow></mfrac><mfrac><mrow><mo>∂</mo><msup><mi>a</mi><mo>*</mo></msup></mrow><mrow><mo>∂</mo><mi>η</mi></mrow></mfrac><mfrac><mrow><mo>∂</mo><msub><mi>η</mi><mi>θ</mi></msub><mo>(</mo><mi>x</mi><mo>)</mo></mrow><mrow><mo>∂</mo><mi>θ</mi></mrow></mfrac></math>

첫 번째 인자는 loss를 줄이려면 action을 어느 방향으로 바꾸고 싶은지를 말한다. 마지막 인자는 신경망을 통해 파라미터로 역전파한다. 가운데 <math><mfrac><mrow><mo>∂</mo><msup><mi>a</mi><mo>*</mo></msup></mrow><mrow><mo>∂</mo><mi>η</mi></mrow></mfrac></math>는 QP 파라미터를 바꾸면 **선택된 action이 실제로 움직이는지**를 말한다.

### 제약에 걸리지 않는 경우

<math display="block" aria-label="Gradient when no bound is active"><mtable columnalign="left"><mtr><mtd><mi>η</mi><mo>=</mo><mn>.45</mn><mo>⇒</mo><msup><mi>a</mi><mo>*</mo></msup><mo>=</mo><mn>.45</mn><mo>,</mo><mfrac><mrow><mo>∂</mo><msup><mi>a</mi><mo>*</mo></msup></mrow><mrow><mo>∂</mo><mi>η</mi></mrow></mfrac><mo>=</mo><mn>1</mn></mtd></mtr><mtr><mtd><mfrac><mrow><mo>∂</mo><mi>ℓ</mi></mrow><mrow><mo>∂</mo><mi>η</mi></mrow></mfrac><mo>=</mo><mo>(</mo><mn>.45</mn><mo>−</mo><mn>.55</mn><mo>)</mo><mo>·</mo><mn>1</mn><mo>=</mo><mo>−</mo><mn>.1</mn></mtd></mtr></mtable></math>

Gradient descent는 <math><mi>η</mi></math>를 증가시킨다. Action도 증가해 목표 0.55에 가까워진다. 신경망의 선호 변화가 최적화기를 지나 의사결정에 도달한다.

### Ramp 상한에 걸린 경우

<math display="block" aria-label="The upper bound gives a locally zero action gradient"><mtable columnalign="left"><mtr><mtd><mi>η</mi><mo>=</mo><mn>.8</mn><mo>⇒</mo><msup><mi>a</mi><mo>*</mo></msup><mo>=</mo><mn>.6</mn></mtd></mtr><mtr><mtd><mfrac><mrow><mo>∂</mo><msup><mi>a</mi><mo>*</mo></msup></mrow><mrow><mo>∂</mo><mi>η</mi></mrow></mfrac><mo>=</mo><mn>0</mn><mo>,</mo><mfrac><mrow><mo>∂</mo><mi>ℓ</mi></mrow><mrow><mo>∂</mo><mi>η</mi></mrow></mfrac><mo>=</mo><mn>0</mn></mtd></mtr></mtable></math>

유인을 0.8에서 0.79로 줄여도 action은 여전히 0.6이다. Action이 국소적으로 상수이므로, loss가 양수인데도 이 파라미터 경로의 gradient는 0이다.

**최적화 layer를 미분할 수 있다는 것과 학습에 유용한 gradient가 항상 나온다는 것은 다르다.** 현재 목적함수에 대해 제약 최적해는 올바르지만, 이 국소 gradient는 포화를 벗어나려면 유인을 얼마나 바꿔야 하는지 알려주지 못한다. 다른 파라미터 경로, loss, 의도적인 smoothing에 따라 학습 동작은 달라질 수 있으나 이 계산만으로 해결책이 보장되지는 않는다.

유인 0.4와 0.6에서는 action map에 꺾임이 있다. 목적함수가 strongly convex하고 최적해가 유일한데도 두 점의 일반적인 미분은 존재하지 않는다. 그 지점에서 사용하는 미분 convention이나 generalized derivative는 일반적인 미분과 구분해야 한다.

## 3. 최적해의 명시적인 수식을 모르는데 어떻게 미분하는가?

일차원 예제는 clipping 해를 직접 쓸 수 있었다. 변수가 많아지면 보통 명시적인 해를 모른다. OptNet은 solver가 수행한 모든 반복을 역전파하는 대신, **찾아낸 해에서 성립하는 KKT 조건을 미분**한다.

### 3.1 최적해가 만족하는 방정식을 이용한다

다음 파라미터화된 QP를 생각하자.

<math display="block" aria-label="Parameterized positive definite quadratic program"><mtable columnalign="left"><mtr><mtd><msup><mi>a</mi><mo>*</mo></msup><mo>(</mo><mi>η</mi><mo>)</mo><mo>=</mo><munder><mo>arg min</mo><mi>a</mi></munder><mo>(</mo><mfrac><mrow><mn>1</mn></mrow><mrow><mn>2</mn></mrow></mfrac><msup><mrow><mi>a</mi></mrow><mo>⊤</mo></msup><mi>H</mi><mo>(</mo><mi>η</mi><mo>)</mo><mi>a</mi><mo>+</mo><msup><mrow><mi>c</mi><mo>(</mo><mi>η</mi><mo>)</mo></mrow><mo>⊤</mo></msup><mi>a</mi><mo>)</mo></mtd></mtr><mtr><mtd><mi>A</mi><mo>(</mo><mi>η</mi><mo>)</mo><mi>a</mi><mo>=</mo><mi>b</mi><mo>(</mo><mi>η</mi><mo>)</mo></mtd></mtr><mtr><mtd><mi>G</mi><mo>(</mo><mi>η</mi><mo>)</mo><mi>a</mi><mo>≤</mo><mi>h</mi><mo>(</mo><mi>η</mi><mo>)</mo></mtd></mtr></mtable></math>

<math><mi>η</mi></math>는 목적함수와 제약을 결정하는 파라미터들을 모은 것이다. Feasible set은 비어 있지 않고 대칭 Hessian이 <math><mi>H</mi><mo>≻</mo><mn>0</mn></math>라고 가정한다. 이런 각 파라미터 값에서는 primal 최적해가 존재하고 유일하다. Affine 제약이므로 KKT 승수도 존재하지만, 중복 제약 때문에 승수는 유일하지 않을 수 있다.

등식 승수를 ν, 비음수 부등식 승수를 λ라고 하고 파라미터 인수를 생략하면 KKT 조건은 다음과 같다.

<math display="block" aria-label="QP KKT equations and inequalities"><mtable columnalign="left"><mtr><mtd><mi>H</mi><msup><mi>a</mi><mo>*</mo></msup><mo>+</mo><mi>c</mi><mo>+</mo><msup><mrow><mi>A</mi></mrow><mo>⊤</mo></msup><msup><mi>ν</mi><mo>*</mo></msup><mo>+</mo><msup><mrow><mi>G</mi></mrow><mo>⊤</mo></msup><msup><mi>λ</mi><mo>*</mo></msup><mo>=</mo><mn>0</mn></mtd></mtr><mtr><mtd><mi>A</mi><msup><mi>a</mi><mo>*</mo></msup><mo>−</mo><mi>b</mi><mo>=</mo><mn>0</mn></mtd></mtr><mtr><mtd><msub><msup><mi>λ</mi><mo>*</mo></msup><mi>i</mi></msub><msub><mo>(</mo><mi>G</mi><msup><mi>a</mi><mo>*</mo></msup><mo>−</mo><mi>h</mi><mo>)</mo><mi>i</mi></msub><mo>=</mo><mn>0</mn></mtd></mtr><mtr><mtd><mi>G</mi><msup><mi>a</mi><mo>*</mo></msup><mo>−</mo><mi>h</mi><mo>≤</mo><mn>0</mn><mo>,</mo><msup><mi>λ</mi><mo>*</mo></msup><mo>≥</mo><mn>0</mn></mtd></mtr></mtable></math>

Primal·dual 해를 하나로 모으자.

<math display="block" aria-label="Primal and dual solution variables"><msup><mi>y</mi><mo>*</mo></msup><mo>=</mo><mo>[</mo><mtable><mtr><mtd><msup><mi>a</mi><mo>*</mo></msup></mtd></mtr><mtr><mtd><msup><mi>λ</mi><mo>*</mo></msup></mtd></mtr><mtr><mtd><msup><mi>ν</mi><mo>*</mo></msup></mtd></mtr></mtable><mo>]</mo></math>

KKT의 **등식 부분**을 다음 residual로 쓴다. QP 데이터는 모두 <math><mi>η</mi></math>에서 평가한다.

<math display="block" aria-label="Equality part of the KKT residual"><mi>F</mi><mo>(</mo><mi>y</mi><mo>,</mo><mi>η</mi><mo>)</mo><mo>=</mo><mo>[</mo><mtable><mtr><mtd><mi>H</mi><mi>a</mi><mo>+</mo><mi>c</mi><mo>+</mo><msup><mrow><mi>G</mi></mrow><mo>⊤</mo></msup><mi>λ</mi><mo>+</mo><msup><mrow><mi>A</mi></mrow><mo>⊤</mo></msup><mi>ν</mi></mtd></mtr><mtr><mtd><mo>diag</mo><mo>(</mo><mi>λ</mi><mo>)</mo><mo>(</mo><mi>G</mi><mi>a</mi><mo>−</mo><mi>h</mi><mo>)</mo></mtd></mtr><mtr><mtd><mi>A</mi><mi>a</mi><mo>−</mo><mi>b</mi></mtd></mtr></mtable><mo>]</mo></math>

Primal–dual 최적해에서는 residual이 0이다. 그러나 부등식 feasibility와 부등식 승수의 비음수 조건도 여전히 필요하다. 등식 residual만 0이라고 임의의 점이 최적해가 되는 것은 아니다.

### 3.2 Residual 방정식을 미분한다

“파라미터를 조금 바꿨을 때 KKT 조건이 계속 성립하려면 해가 얼마나 움직여야 하는가?” Residual이 0이라는 관계를 미분하면

<math display="block" aria-label="Differentiate a zero KKT residual"><msub><mi>F</mi><mi>y</mi></msub><mfrac><mrow><mo>∂</mo><msup><mi>y</mi><mo>*</mo></msup></mrow><mrow><mo>∂</mo><mi>η</mi></mrow></mfrac><mo>+</mo><msub><mi>F</mi><mi>η</mi></msub><mo>=</mo><mn>0</mn></math>

첫 항은 primal·dual 해의 움직임 때문에 생기는 residual 변화이다. 두 번째는 해 변수를 고정했을 때 파라미터의 직접적인 영향이다. Residual이 연속적으로 미분 가능하고 <math><msub><mi>F</mi><mi>y</mi></msub></math>가 nonsingular이면 implicit function theorem으로 다음을 얻는다.

<math display="block" aria-label="Implicit solution derivative when the Jacobian is nonsingular"><mfrac><mrow><mo>∂</mo><msup><mi>y</mi><mo>*</mo></msup></mrow><mrow><mo>∂</mo><mi>η</mi></mrow></mfrac><mo>=</mo><mo>−</mo><msup><msub><mi>F</mi><mi>y</mi></msub><mrow><mo>−</mo><mn>1</mn></mrow></msup><msub><mi>F</mi><mi>η</mi></msub></math>

계산에 쓰는 핵심은 다음 선형시스템이다.

<math display="block" aria-label="Implicit differentiation requires an invertible residual Jacobian"><mtable columnalign="left"><mtr><mtd><mi>F</mi><mo>(</mo><msup><mi>y</mi><mo>*</mo></msup><mo>(</mo><mi>η</mi><mo>)</mo><mo>,</mo><mi>η</mi><mo>)</mo><mo>=</mo><mn>0</mn></mtd></mtr><mtr><mtd><msub><mi>F</mi><mi>y</mi></msub><mfrac><mrow><mo>∂</mo><msup><mi>y</mi><mo>*</mo></msup></mrow><mrow><mo>∂</mo><mi>η</mi></mrow></mfrac><mo>=</mo><mo>−</mo><msub><mi>F</mi><mi>η</mi></msub></mtd></mtr></mtable></math>

구현에서는 역행렬을 직접 만들기보다 이 시스템을 푼다.

이 QP residual의 Jacobian은 다음 블록 구조를 갖는다.

<math display="block" aria-label="Jacobian of the equality residual at a KKT solution"><msub><mi>F</mi><mi>y</mi></msub><mo>=</mo><mo>[</mo><mtable><mtr><mtd><mi>H</mi></mtd><mtd><msup><mrow><mi>G</mi></mrow><mo>⊤</mo></msup></mtd><mtd><msup><mrow><mi>A</mi></mrow><mo>⊤</mo></msup></mtd></mtr><mtr><mtd><mo>diag</mo><mo>(</mo><msup><mi>λ</mi><mo>*</mo></msup><mo>)</mo><mi>G</mi></mtd><mtd><mo>diag</mo><mo>(</mo><mi>G</mi><msup><mi>a</mi><mo>*</mo></msup><mo>−</mo><mi>h</mi><mo>)</mo></mtd><mtd><mn>0</mn></mtd></mtr><mtr><mtd><mi>A</mi></mtd><mtd><mn>0</mn></mtd><mtd><mn>0</mn></mtd></mtr></mtable><mo>]</mo></math>

H의 positive definiteness만으로 전체 행렬의 가역성이 보장되지는 않는다. 중복된 활성 제약이나 승수가 0인 활성 부등식 때문에 singular해질 수 있다. 매끄러운 국소 데이터와 positive definite QP에서 등식·활성 부등식 gradient의 독립성과 strict complementarity는 대표적인 충분 정규성 조건이다. 이때 활성 집합이 국소적으로 유지되면 매끄러운 해를 추적할 수 있다.

### 3.3 Ramp 미분을 KKT에서 직접 다시 구한다

하한 제약을 0.4 − a ≤ 0, 상한 제약을 a − 0.6 ≤ 0으로 쓰면 KKT 등식에 다음이 포함된다.

<math display="block" aria-label="Scalar ramp KKT equations"><mtable columnalign="left"><mtr><mtd><mi>a</mi><mo>−</mo><mi>η</mi><mo>−</mo><msub><mi>λ</mi><mtext>lower</mtext></msub><mo>+</mo><msub><mi>λ</mi><mtext>upper</mtext></msub><mo>=</mo><mn>0</mn></mtd></mtr><mtr><mtd><msub><mi>λ</mi><mtext>lower</mtext></msub><mo>(</mo><mn>.4</mn><mo>−</mo><mi>a</mi><mo>)</mo><mo>=</mo><mn>0</mn></mtd></mtr><mtr><mtd><msub><mi>λ</mi><mtext>upper</mtext></msub><mo>(</mo><mi>a</mi><mo>−</mo><mn>.6</mn><mo>)</mo><mo>=</mo><mn>0</mn></mtd></mtr></mtable></math>

유인 0.45에서는 두 승수가 0이고 국소적으로 그대로 유지된다. Stationarity를 미분하면 da = dη이므로 <math><mfrac><mrow><mo>∂</mo><msup><mi>a</mi><mo>*</mo></msup></mrow><mrow><mo>∂</mo><mi>η</mi></mrow></mfrac></math> = 1이다.

유인 0.8에서는 상한 승수가 양수다. 그 complementarity 식을 미분한다.

<math display="block" aria-label="Differentiating complementarity at a strictly active upper bound"><mtable columnalign="left"><mtr><mtd><msub><msup><mi>λ</mi><mo>*</mo></msup><mtext>upper</mtext></msub><mo>=</mo><mi>η</mi><mo>−</mo><mn>.6</mn><mo>=</mo><mn>.2</mn></mtd></mtr><mtr><mtd><msub><msup><mi>λ</mi><mo>*</mo></msup><mtext>upper</mtext></msub><mi>d</mi><mi>a</mi><mo>+</mo><mo>(</mo><msup><mi>a</mi><mo>*</mo></msup><mo>−</mo><mn>.6</mn><mo>)</mo><mi>d</mi><msub><mi>λ</mi><mtext>upper</mtext></msub><mo>=</mo><mn>0</mn></mtd></mtr><mtr><mtd><mn>.2</mn><mi>d</mi><mi>a</mi><mo>=</mo><mn>0</mn><mo>⇒</mo><mfrac><mrow><mo>∂</mo><msup><mi>a</mi><mo>*</mo></msup></mrow><mrow><mo>∂</mo><mi>η</mi></mrow></mfrac><mo>=</mo><mn>0</mn></mtd></mtr></mtable></math>

Action은 일차적으로 움직이지 못하고 상한 승수가 유인의 변화를 흡수한다. 유인 0.6에서는 상한의 slack과 승수가 둘 다 0이다. 해당 complementarity 행의 일차 미분이 0이 되어 residual Jacobian이 singular하고, 역행렬 공식을 적용할 수 없다. 명시적인 clipping 해의 꺾임과 같은 현상이다.

## 4. 역전파에는 전체 Jacobian 대신 필요한 곱을 계산한다

Scalar loss가 해를 통해 <math><mi>η</mi></math>에 의존한다면 다음 adjoint 시스템을 푼다.

<math display="block" aria-label="Adjoint solve for a scalar loss"><mtable columnalign="left"><mtr><mtd><msup><mrow><msub><mi>F</mi><mi>y</mi></msub></mrow><mo>⊤</mo></msup><mi>v</mi><mo>=</mo><msub><mo>∇</mo><mi>y</mi></msub><mi>ℓ</mi></mtd></mtr><mtr><mtd><msub><mo>∇</mo><mi>η</mi></msub><mi>ℓ</mi><mo>=</mo><mo>−</mo><msup><mrow><msub><mi>F</mi><mi>η</mi></msub></mrow><mo>⊤</mo></msup><mi>v</mi></mtd></mtr></mtable></math>

Loss가 QP 파라미터에 직접 의존하는 항도 있으면 마지막 gradient에 그 직접 편미분을 더한다. 모든 파라미터의 민감도 행렬을 만들지 않고 필요한 Jacobian 곱을 얻는 방법이다.

OptNet solver는 primal–dual interior-point 방법을 사용하며, forward solve의 행렬 분해 작업을 backward 계산에 재사용한다. 그 구현의 추가 역전파 비용을 줄이는 방식이다. 임의의 제약 최적화 문제를 풀고 미분하는 비용이 항상 없다는 뜻은 아니다.

이 계산의 출발점은 0인 KKT residual과 그 국소 정규성이다. Feasibility, 해의 유일성, 일반적인 미분 가능성, 유용한 학습 gradient는 각각 확인해야 한다. 의사결정 변수가 하나인 hard ramp 예제에서도 이 차이가 드러난다.

## 참고문헌

- Amos, B., and Kolter, J. Z. (2017). *OptNet: Differentiable Optimization as a Layer in Neural Networks*. In *Proceedings of the 34th International Conference on Machine Learning*, PMLR 70, 136–145. [공식 서지정보](https://proceedings.mlr.press/v70/amos17a.html), [ICML 논문 PDF](https://proceedings.mlr.press/v70/amos17a/amos17a.pdf), [arXiv:1703.00443](https://arxiv.org/abs/1703.00443).
- *Implicit Layers Tutorial*, Chapter 5, “Differentiable optimization.” KKT residual과 implicit differentiation. [튜토리얼 장](https://implicit-layers-tutorial.org/differentiable_optimization/).
