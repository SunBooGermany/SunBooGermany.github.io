---
layout: "course-note"
title: "Week 4: Learning with Physical Constraints"
title_ko: "4주차: 물리 제약을 반영한 학습"
description: "Residual losses, KKT projection, scaling, and differentiable physical equalities."
description_ko: "Residual loss, KKT 투영, scaling과 미분 가능한 물리 등식을 다룹니다."
material_label: "Week 4"
material_label_ko: "4주차"
updated: "2026-10-20"
permalink: "/courses/surrogate-models/week-04/"
pdf_en: "/assets/courses/surrogate-models/week-04-en.pdf"
pdf_ko: "/assets/courses/surrogate-models/week-04-ko.pdf"
course_id: "surrogate-models"
reading_note: "/courses/surrogate-models/week-04-reading/"
reading_pdf_en: "/assets/courses/surrogate-models/week-04-reading-en.pdf"
reading_pdf_ko: "/assets/courses/surrogate-models/week-04-reading-ko.pdf"
notebook: "/assets/courses/surrogate-models/week-04/week04_lab.ipynb"
lab_script: "/assets/courses/surrogate-models/week-04/week04_lab.py"
---

## The predicted outlet contains too much material

An MLP predicts [0.70, 0.45, 0.25] mol/L for A, B, and C with a 1.20 mol/L feed. The total is 1.40. Can an engineer pass this outlet to the next process unit?

<figure><img src="/assets/courses/surrogate-models/week-04/motivation-en.svg" alt="Reactor with feed 1.20 and predicted total 1.40 mol/L" /></figure>

<!-- lecture-page -->

## A balance error passes to the next unit

The next separator calculates its load from incoming component amounts. A total-concentration error in the reactor surrogate enters that calculation directly, so prediction error and balance violation need separate checks.

This week we penalize residuals in the loss and project outputs onto specified linear equalities. We also measure component errors before and after correction.

<!-- lecture-page -->

## What we will calculate

1. Compare an MLP, a soft sum penalty, and a hard sum projection on the same data.
2. Derive the nearest-point projection from KKT conditions and check rank assumptions.
3. Compare hand gradients with automatic differentiation through a fixed layer.
4. Report component errors, equality violations, negative concentrations, and unenforced balances separately.

The lab uses the Week 2 steady-state CSTR. We return to dynamic constraints near the end.

<!-- lecture-page -->

## Reference process and units

Assume perfect mixing, constant volume, and equal inlet/outlet flow. The feed contains only A; consecutive reactions A → B → C have 1:1 stoichiometry. Temperature T is prescribed and the model has no energy balance.

<math display="block"><mtable columnalign="left"><mtr><mtd><mrow><msub><mrow><mi>C</mi></mrow><mrow><mi>A</mi></mrow></msub><mo>=</mo><mfrac><mrow><msub><mrow><mi>C</mi></mrow><mrow><mi>Af</mi></mrow></msub></mrow><mrow><mn>1</mn><mo>+</mo><msub><mrow><mi>k</mi></mrow><mrow><mn>1</mn></mrow></msub><mi>τ</mi></mrow></mfrac></mrow></mtd></mtr><mtr><mtd><mrow><msub><mrow><mi>C</mi></mrow><mrow><mi>B</mi></mrow></msub><mo>=</mo><mfrac><mrow><msub><mrow><mi>k</mi></mrow><mrow><mn>1</mn></mrow></msub><mi>τ</mi><msub><mrow><mi>C</mi></mrow><mrow><mi>A</mi></mrow></msub></mrow><mrow><mn>1</mn><mo>+</mo><msub><mrow><mi>k</mi></mrow><mrow><mn>2</mn></mrow></msub><mi>τ</mi></mrow></mfrac><mo>,</mo><mtext>  </mtext><msub><mrow><mi>C</mi></mrow><mrow><mi>C</mi></mrow></msub><mo>=</mo><msub><mrow><mi>k</mi></mrow><mrow><mn>2</mn></mrow></msub><mi>τ</mi><msub><mrow><mi>C</mi></mrow><mrow><mi>B</mi></mrow></msub></mrow></mtd></mtr></mtable></math>

At 330 K, k₁ = 0.2 min⁻¹ and k₂ = 0.1 min⁻¹. With τ = 5 min and C_Af = 1.2 mol/L, [C_A, C_B, C_C] = [0.6, 0.4, 0.2] mol/L.

<!-- lecture-page -->

## Where the concentration-sum equality comes from

Let r_A, r_B, and r_C denote the right sides of the steady-state species balances. Adding them cancels the reaction terms.

<math display="block"><mtable columnalign="left"><mtr><mtd><mrow><msub><mrow><mi>r</mi></mrow><mrow><mi>A</mi></mrow></msub><mo>+</mo><msub><mrow><mi>r</mi></mrow><mrow><mi>B</mi></mrow></msub><mo>+</mo><msub><mrow><mi>r</mi></mrow><mrow><mi>C</mi></mrow></msub><mo>=</mo><mfrac><mrow><msub><mrow><mi>C</mi></mrow><mrow><mi>Af</mi></mrow></msub><mo>−</mo><mrow><mo>(</mo><msub><mrow><mi>C</mi></mrow><mrow><mi>A</mi></mrow></msub><mo>+</mo><msub><mrow><mi>C</mi></mrow><mrow><mi>B</mi></mrow></msub><mo>+</mo><msub><mrow><mi>C</mi></mrow><mrow><mi>C</mi></mrow></msub><mo>)</mo></mrow></mrow><mrow><mi>τ</mi></mrow></mfrac></mrow></mtd></mtr></mtable></math>

At steady state each residual is zero, giving S = C_A + C_B + C_C = C_Af. This concentration-sum equality depends on the stated stoichiometry and flow assumptions. Other reactions require the appropriate elemental or mass balance and units.

<!-- lecture-page -->

## Component error and sum error are different

| Prediction [mol/L] | Component error [mol/L] | Sum residual [mol/L] |
| --- | --- | --- |
| [0.70, 0.45, 0.25] | [+0.10, +0.05, +0.05] | +0.20 |
| [0.70, 0.30, 0.20] | [+0.10, −0.10, 0.00] | 0.00 |

The reference is [0.60, 0.40, 0.20] mol/L. The second prediction has the right sum but incorrect A and B. An equality-only evaluation would miss those errors.

<!-- lecture-page -->

## Define the residual before choosing a loss

The sum residual is r_sum = C_A + C_B + C_C − C_Af, in mol/L. Known kinetics also allow species-level steady-state residuals.

<math display="block"><mtable columnalign="left"><mtr><mtd><mrow><msub><mrow><mi>r</mi></mrow><mrow><mi>A</mi></mrow></msub><mo>=</mo><mfrac><mrow><msub><mrow><mi>C</mi></mrow><mrow><mi>Af</mi></mrow></msub><mo>−</mo><msub><mrow><mi>C</mi></mrow><mrow><mi>A</mi></mrow></msub></mrow><mrow><mi>τ</mi></mrow></mfrac><mo>−</mo><msub><mrow><mi>k</mi></mrow><mrow><mn>1</mn></mrow></msub><msub><mrow><mi>C</mi></mrow><mrow><mi>A</mi></mrow></msub></mrow></mtd></mtr><mtr><mtd><mrow><msub><mrow><mi>r</mi></mrow><mrow><mi>B</mi></mrow></msub><mo>=</mo><msub><mrow><mi>k</mi></mrow><mrow><mn>1</mn></mrow></msub><msub><mrow><mi>C</mi></mrow><mrow><mi>A</mi></mrow></msub><mo>−</mo><mfrac><mrow><msub><mrow><mi>C</mi></mrow><mrow><mi>B</mi></mrow></msub></mrow><mrow><mi>τ</mi></mrow></mfrac><mo>−</mo><msub><mrow><mi>k</mi></mrow><mrow><mn>2</mn></mrow></msub><msub><mrow><mi>C</mi></mrow><mrow><mi>B</mi></mrow></msub></mrow></mtd></mtr><mtr><mtd><mrow><msub><mrow><mi>r</mi></mrow><mrow><mi>C</mi></mrow></msub><mo>=</mo><msub><mrow><mi>k</mi></mrow><mrow><mn>2</mn></mrow></msub><msub><mrow><mi>C</mi></mrow><mrow><mi>B</mi></mrow></msub><mo>−</mo><mfrac><mrow><msub><mrow><mi>C</mi></mrow><mrow><mi>C</mi></mrow></msub></mrow><mrow><mi>τ</mi></mrow></mfrac></mrow></mtd></mtr></mtable></math>

These three residuals have units mol/(L·min). The lab trains with the sum residual only and uses the species residuals as a separate evaluation.

<!-- lecture-page -->

## Soft penalty: fit data and penalize violations

<math display="block"><mtable columnalign="left"><mtr><mtd><mrow><msub><mrow><mi>L</mi></mrow><mrow><mi>soft</mi></mrow></msub><mo>=</mo><mfrac><mrow><mn>1</mn></mrow><mrow><mn>3</mn><mi>N</mi></mrow></mfrac><msub><mrow><mo>∑</mo></mrow><mrow><mi>i</mi></mrow></msub><msup><mrow><mo>‖</mo><mfrac><mrow><msub><mrow><mover><mi>y</mi><mo>^</mo></mover></mrow><mrow><mi>i</mi></mrow></msub><mo>−</mo><msub><mrow><mi>y</mi></mrow><mrow><mi>i</mi></mrow></msub></mrow><mrow><msub><mrow><mi>c</mi></mrow><mrow><mo>∗</mo></mrow></msub></mrow></mfrac><mo>‖</mo></mrow><mrow><mn>2</mn></mrow></msup><mo>+</mo><mi>λ</mi><mfrac><mrow><mn>1</mn></mrow><mrow><mi>N</mi></mrow></mfrac><msub><mrow><mo>∑</mo></mrow><mrow><mi>i</mi></mrow></msub><msup><mrow><mrow><mo>(</mo><mfrac><mrow><msub><mrow><mi>r</mi></mrow><mrow><mi>sum</mi><mo>,</mo><mi>i</mi></mrow></msub></mrow><mrow><msub><mrow><mi>c</mi></mrow><mrow><mo>∗</mo></mrow></msub></mrow></mfrac><mo>)</mo></mrow></mrow><mrow><mn>2</mn></mrow></msup></mrow></mtd></mtr></mtable></math>

Both terms are dimensionless with <math><msub><mrow><mi>c</mi></mrow><mrow><mo>∗</mo></mrow></msub></math> = 1 mol/L. The lab uses λ = 10; its meaning includes the averaging conventions for one sum residual and three component errors.

Changing λ changes the objective and gradient magnitudes. A finite penalty and a completed training run do not guarantee zero residual at every input.

<!-- lecture-page -->

## Solve a finite-penalty problem by hand

Minimize the scalar objective ½(z − a)² + ½λ(z − b)², where data favor a, the equality requires z = b, and λ ≥ 0. Setting the derivative to zero gives:

<math display="block"><mtable columnalign="left"><mtr><mtd><mrow><msub><mrow><mi>z</mi></mrow><mrow><mo>∗</mo></mrow></msub><mo>=</mo><mfrac><mrow><mi>a</mi><mo>+</mo><mi>λ</mi><mi>b</mi></mrow><mrow><mn>1</mn><mo>+</mo><mi>λ</mi></mrow></mfrac></mrow></mtd></mtr><mtr><mtd><mrow><msub><mrow><mi>z</mi></mrow><mrow><mo>∗</mo></mrow></msub><mo>−</mo><mi>b</mi><mo>=</mo><mfrac><mrow><mi>a</mi><mo>−</mo><mi>b</mi></mrow><mrow><mn>1</mn><mo>+</mo><mi>λ</mi></mrow></mfrac></mrow></mtd></mtr></mtable></math>

If a ≠ b, a residual remains for finite λ. Very large penalties also require attention to loss magnitudes and numerical conditioning. This is a counterexample to automatic exact equality enforcement by a penalty.

<!-- lecture-page -->

## What automatic differentiation differentiates

Our MLP maps [T, τ, C_Af] to steady concentrations. Training differentiates the loss with respect to parameters θ. The sum residual and steady-state species balances need no time derivative.

A continuous-time PINN using y_θ(t) may have a residual ∂y_θ/∂t − F(y_θ, u), which also differentiates with respect to a coordinate. Distinguish this from the parameter gradient used for training.

If t̃ = (t − μ_t)/s_t, then ∂y/∂t = (1/s_t)∂y/∂t̃.

<!-- lecture-page -->

## Hard equality: each input defines an output set

<math display="block"><mtable columnalign="left"><mtr><mtd><mrow><mi>A</mi><mi>x</mi><mo>+</mo><mi>B</mi><mi>y</mi><mo>=</mo><mi>b</mi><mo>,</mo></mrow></mtd></mtr><mtr><mtd><mrow><mi>B</mi><mi>y</mi><mo>=</mo><mi>d</mi><mrow><mo>(</mo><mi>x</mi><mo>)</mo></mrow><mo>,</mo><mtext>  </mtext><mi>d</mi><mrow><mo>(</mo><mi>x</mi><mo>)</mo></mrow><mo>=</mo><mi>b</mi><mo>−</mo><mi>A</mi><mi>x</mi></mrow></mtd></mtr></mtable></math>

x ∈ ℝᵖ, y ∈ ℝⁿ, A ∈ ℝᵐˣᵖ, B ∈ ℝᵐˣⁿ, and b ∈ ℝᵐ. Coefficients A, B, b are fixed; the raw output is ŷ = f_θ(x).

For the CSTR, x = [T, τ, C_Af], A = [0, 0, −1], B = [1, 1, 1], and b = 0. Thus d(x) = C_Af.

<!-- lecture-page -->

## The nearest output satisfying the equality

<math display="block"><mtable columnalign="left"><mtr><mtd><mrow><msub><mrow><mi>y</mi></mrow><mrow><mi>p</mi></mrow></msub><mo>=</mo><msub><mrow><mi>argmin</mi></mrow><mrow><mi>z</mi></mrow></msub><mtext>  </mtext><mfrac><mrow><mn>1</mn></mrow><mrow><mn>2</mn></mrow></mfrac><msup><mrow><mo>‖</mo><mi>z</mi><mo>−</mo><mover><mi>y</mi><mo>^</mo></mover><mo>‖</mo></mrow><mrow><mn>2</mn></mrow></msup><mtext>   subject to   </mtext><mi>B</mi><mi>z</mi><mo>=</mo><mi>d</mi><mrow><mo>(</mo><mi>x</mi><mo>)</mo></mrow></mrow></mtd></mtr></mtable></math>

Hold x and the raw prediction ŷ fixed and adjust only output z. Distance here is Euclidean distance in physical concentration coordinates.

The objective is strictly convex, so a nonempty feasible set has a unique projected output. KKT conditions give a closed form for this equality-only QP.

<!-- lecture-page -->

## Lagrangian and KKT conditions

<math display="block"><mtable columnalign="left"><mtr><mtd><mrow><mi>ℒ</mi><mrow><mo>(</mo><mi>z</mi><mo>,</mo><mi>λ</mi><mo>)</mo></mrow><mo>=</mo><mfrac><mrow><mn>1</mn></mrow><mrow><mn>2</mn></mrow></mfrac><msup><mrow><mo>‖</mo><mi>z</mi><mo>−</mo><mover><mi>y</mi><mo>^</mo></mover><mo>‖</mo></mrow><mrow><mn>2</mn></mrow></msup><mo>+</mo><msup><mrow><mi>λ</mi></mrow><mrow><mi>T</mi></mrow></msup><mrow><mo>(</mo><mi>B</mi><mi>z</mi><mo>−</mo><mi>d</mi><mo>)</mo></mrow></mrow></mtd></mtr></mtable></math>

Enforce stationarity and primal feasibility together.

<math display="block"><mtable columnalign="left"><mtr><mtd><mrow><mi>z</mi><mo>−</mo><mover><mi>y</mi><mo>^</mo></mover><mo>+</mo><msup><mrow><mi>B</mi></mrow><mrow><mi>T</mi></mrow></msup><mi>λ</mi><mo>=</mo><mn>0</mn><mo>,</mo><mtext>  </mtext><mi>B</mi><mi>z</mi><mo>=</mo><mi>d</mi></mrow></mtd></mtr></mtable></math>

There are no inequalities, hence no complementary slackness or multiplier sign restriction. For a strictly convex objective with affine equalities, an output satisfying these conditions is the global minimizer.

<!-- lecture-page -->

## Eliminate the multiplier to obtain the projection

Stationarity gives z = ŷ − Bᵀλ. Substitute into Bz = d.

<math display="block"><mtable columnalign="left"><mtr><mtd><mrow><mi>G</mi><mo>=</mo><mi>B</mi><msup><mrow><mi>B</mi></mrow><mrow><mi>T</mi></mrow></msup><mo>,</mo><mtext>  </mtext><mi>G</mi><mi>λ</mi><mo>=</mo><mi>B</mi><mover><mi>y</mi><mo>^</mo></mover><mo>−</mo><mi>d</mi></mrow></mtd></mtr><mtr><mtd><mrow><msub><mrow><mi>y</mi></mrow><mrow><mi>p</mi></mrow></msub><mo>=</mo><mover><mi>y</mi><mo>^</mo></mover><mo>−</mo><msup><mrow><mi>B</mi></mrow><mrow><mi>T</mi></mrow></msup><msup><mrow><mi>G</mi></mrow><mrow><mo>−</mo><mn>1</mn></mrow></msup><mrow><mo>(</mo><mi>B</mi><mover><mi>y</mi><mo>^</mo></mover><mo>−</mo><mi>d</mi><mo>)</mo></mrow></mrow></mtd></mtr></mtable></math>

If rank(B) = m, then G = BBᵀ is positive definite. The formula uses an inverse for notation; implementation solves Gλ = Bŷ − d. A fixed B allows reuse of a factorization or fixed projection coefficients.

<!-- lecture-page -->

## The fixed affine output layer in KKT-hPINN

<math display="block"><mtable columnalign="left"><mtr><mtd><mrow><mi>P</mi><mo>=</mo><mi>I</mi><mo>−</mo><msup><mrow><mi>B</mi></mrow><mrow><mi>T</mi></mrow></msup><msup><mrow><mi>G</mi></mrow><mrow><mo>−</mo><mn>1</mn></mrow></msup><mi>B</mi></mrow></mtd></mtr><mtr><mtd><mrow><msub><mrow><mi>y</mi></mrow><mrow><mi>p</mi></mrow></msub><mo>=</mo><mi>P</mi><msub><mrow><mi>f</mi></mrow><mrow><mi>θ</mi></mrow></msub><mrow><mo>(</mo><mi>x</mi><mo>)</mo></mrow><mo>+</mo><msup><mrow><mi>B</mi></mrow><mrow><mi>T</mi></mrow></msup><msup><mrow><mi>G</mi></mrow><mrow><mo>−</mo><mn>1</mn></mrow></msup><mrow><mo>(</mo><mi>b</mi><mo>−</mo><mi>A</mi><mi>x</mi><mo>)</mo></mrow></mrow></mtd></mtr></mtable></math>

Physical equalities determine this layer’s coefficients; they are not trained. MLP weights θ are trained using the projected output in the loss.

<math display="block"><mtable columnalign="left"><mtr><mtd><mrow><mi>B</mi><msub><mrow><mi>y</mi></mrow><mrow><mi>p</mi></mrow></msub><mo>=</mo><mi>B</mi><mover><mi>y</mi><mo>^</mo></mover><mo>−</mo><mi>G</mi><msup><mrow><mi>G</mi></mrow><mrow><mo>−</mo><mn>1</mn></mrow></msup><mrow><mo>(</mo><mi>B</mi><mover><mi>y</mi><mo>^</mo></mover><mo>−</mo><mi>d</mi><mo>)</mo></mrow><mo>=</mo><mi>d</mi></mrow></mtd></mtr></mtable></math>

The specified equalities hold during training and inference, subject in implementation to floating-point error and linear-system conditioning. Source: Chen et al. (2024).

<!-- lecture-page -->

## Check rank and consistency separately

| Case | Consequence |
| --- | --- |
| rank(B) = m ≤ n | Every d is attainable; BBᵀ is invertible. |
| Redundant rows, consistent d | Feasible outputs exist but BBᵀ is singular. Use independent rows or an SVD. |
| Redundant rows, inconsistent d | No feasible output exists. A pseudoinverse cannot satisfy all equations. |

For nearly dependent rows, inspect rank tolerance and conditioning. Scaling entire equality rows consistently changes numerical scales without changing the feasible set.

<!-- lecture-page -->

## Project the concentration sum by hand

<math display="block"><mtable columnalign="left"><mtr><mtd><mrow><mi>B</mi><mo>=</mo><mrow><mo>[</mo><mtable><mtr><mtd><mrow><mn>1</mn></mrow></mtd><mtd><mrow><mn>1</mn></mrow></mtd><mtd><mrow><mn>1</mn></mrow></mtd></mtr></mtable><mo>]</mo></mrow><mo>,</mo><mtext>  </mtext><mi>d</mi><mo>=</mo><mn>1.2</mn></mrow></mtd></mtr><mtr><mtd><mrow><msub><mrow><mi>y</mi></mrow><mrow><mi>p</mi></mrow></msub><mo>=</mo><mrow><mo>[</mo><mtable><mtr><mtd><mrow><mn>.70</mn></mrow></mtd></mtr><mtr><mtd><mrow><mn>.45</mn></mrow></mtd></mtr><mtr><mtd><mrow><mn>.25</mn></mrow></mtd></mtr></mtable><mo>]</mo></mrow><mo>−</mo><mfrac><mrow><mn>.20</mn></mrow><mrow><mn>3</mn></mrow></mfrac><mrow><mo>[</mo><mtable><mtr><mtd><mrow><mn>1</mn></mrow></mtd></mtr><mtr><mtd><mrow><mn>1</mn></mrow></mtd></mtr><mtr><mtd><mrow><mn>1</mn></mrow></mtd></mtr></mtable><mo>]</mo></mrow><mo>=</mo><mrow><mo>[</mo><mtable><mtr><mtd><mrow><mn>.633333</mn></mrow></mtd></mtr><mtr><mtd><mrow><mn>.383333</mn></mrow></mtd></mtr><mtr><mtd><mrow><mn>.183333</mn></mrow></mtd></mtr></mtable><mo>]</mo></mrow></mrow></mtd></mtr></mtable></math>

Subtract the same 0.066667 mol/L from each component. The total is 1.20, but the output still differs from the reference [0.60, 0.40, 0.20].

Displayed values are rounded. Keep full precision during calculation and check the final sum residual.

<!-- lecture-page -->

## Post-projection and training through projection

| Method | Output used in the training loss |
| --- | --- |
| MLP + post-projection | Train on raw outputs; project at test time. |
| KKT-hPINN approach | Use projected outputs throughout training. |

<figure><img src="/assets/courses/surrogate-models/week-04/flow-en.svg" alt="MLP output, fixed projection, data loss, and backward path" /></figure>
Both can satisfy the same equality, but their training gradients differ and generally produce different parameters.

<!-- lecture-page -->

## A fixed layer still transmits gradients

<math display="block"><mtable columnalign="left"><mtr><mtd><mrow><mfrac><mrow><mi>∂</mi><msub><mrow><mi>y</mi></mrow><mrow><mi>p</mi></mrow></msub></mrow><mrow><mi>∂</mi><mover><mi>y</mi><mo>^</mo></mover></mrow></mfrac><mo>=</mo><mi>P</mi></mrow></mtd></mtr><mtr><mtd><mrow><msub><mrow><mi>∇</mi></mrow><mrow><mover><mi>y</mi><mo>^</mo></mover></mrow></msub><mi>L</mi><mo>=</mo><msup><mrow><mi>P</mi></mrow><mrow><mi>T</mi></mrow></msup><msub><mrow><mi>∇</mi></mrow><mrow><msub><mrow><mi>y</mi></mrow><mrow><mi>p</mi></mrow></msub></mrow></msub><mi>L</mi></mrow></mtd></mtr></mtable></math>

P is a symmetric orthogonal projector, so Pᵀ = P. Fixed coefficients do not remove the derivative path.

Detaching the output or wrapping projection in no_grad cuts the required path. The parameter gradient continues through the MLP Jacobian by the chain rule.

<!-- lecture-page -->

## Check the backward pass with three components

<math display="block"><mtable columnalign="left"><mtr><mtd><mrow><mi>P</mi><mo>=</mo><mi>I</mi><mo>−</mo><mfrac><mrow><mn>1</mn></mrow><mrow><mn>3</mn></mrow></mfrac><mrow><mo>[</mo><mtable><mtr><mtd><mrow><mn>1</mn></mrow></mtd><mtd><mrow><mn>1</mn></mrow></mtd><mtd><mrow><mn>1</mn></mrow></mtd></mtr><mtr><mtd><mrow><mn>1</mn></mrow></mtd><mtd><mrow><mn>1</mn></mrow></mtd><mtd><mrow><mn>1</mn></mrow></mtd></mtr><mtr><mtd><mrow><mn>1</mn></mrow></mtd><mtd><mrow><mn>1</mn></mrow></mtd><mtd><mrow><mn>1</mn></mrow></mtd></mtr></mtable><mo>]</mo></mrow></mrow></mtd></mtr><mtr><mtd><mrow><msup><mrow><mi>P</mi></mrow><mrow><mi>T</mi></mrow></msup><mrow><mo>[</mo><mtable><mtr><mtd><mrow><mn>1</mn></mrow></mtd></mtr><mtr><mtd><mrow><mn>0</mn></mrow></mtd></mtr><mtr><mtd><mrow><mn>0</mn></mrow></mtd></mtr></mtable><mo>]</mo></mrow><mo>=</mo><mrow><mo>[</mo><mtable><mtr><mtd><mrow><mfrac><mrow><mn>2</mn></mrow><mrow><mn>3</mn></mrow></mfrac></mrow></mtd></mtr><mtr><mtd><mrow><mfrac><mrow><mo>−</mo><mn>1</mn></mrow><mrow><mn>3</mn></mrow></mfrac></mrow></mtd></mtr><mtr><mtd><mrow><mfrac><mrow><mo>−</mo><mn>1</mn></mrow><mrow><mn>3</mn></mrow></mfrac></mrow></mtd></mtr></mtable><mo>]</mo></mrow></mrow></mtd></mtr></mtable></math>

An upstream gradient [1, 0, 0] at the projected output becomes [2/3, −1/3, −1/3] at the raw output. Its sum is zero, so it lies in the equality’s tangent space.

The lab also checks an analytic Jacobian and double-precision gradcheck for two independent equalities.

<!-- lecture-page -->

## Output standardization also changes B

<math display="block"><mtable columnalign="left"><mtr><mtd><mrow><mi>y</mi><mo>=</mo><mi>μ</mi><mo>+</mo><mi>D</mi><mi>z</mi><mo>,</mo><mtext>  </mtext><mi>B</mi><mi>D</mi><mi>z</mi><mo>=</mo><mi>d</mi><mo>−</mo><mi>B</mi><mi>μ</mi></mrow></mtd></mtr><mtr><mtd><mrow><mi>D</mi><mo>=</mo><mi>diag</mi><mrow><mo>(</mo><msub><mrow><mi>s</mi></mrow><mrow><mn>1</mn></mrow></msub><mo>,</mo><mi>…</mi><mo>,</mo><msub><mrow><mi>s</mi></mrow><mrow><mi>n</mi></mrow></msub><mo>)</mo></mrow></mrow></mtd></mtr></mtable></math>

Compute μ and positive scales s_j from training data only. A projection in standardized coordinates z must use BD and right side d − Bμ.

Nearest points in standardized and physical coordinates differ when component scales differ. State both the equality being enforced and the correction metric.

<!-- lecture-page -->

## Lab choice: restore physical units, then project

The MLP returns standardized outputs z. Restore mol/L with μ + Dz, then project in physical coordinates. Divide data errors by the common scale <math><msub><mrow><mi>c</mi></mrow><mrow><mo>∗</mo></mrow></msub></math> = 1 mol/L.

<math display="block"><mtable columnalign="left"><mtr><mtd><mrow><msub><mrow><mi>∇</mi></mrow><mrow><mi>z</mi></mrow></msub><mi>L</mi><mo>=</mo><msup><mrow><mi>D</mi></mrow><mrow><mi>T</mi></mrow></msup><msup><mrow><mi>P</mi></mrow><mrow><mi>T</mi></mrow></msup><msub><mrow><mi>∇</mi></mrow><mrow><msub><mrow><mi>y</mi></mrow><mrow><mi>p</mi></mrow></msub></mrow></msub><mi>L</mi></mrow></mtd></mtr></mtable></math>

D is diagonal, hence Dᵀ = D. A loss divided by component-specific standard deviations adds weights that must also enter gradient and error interpretations.

<!-- lecture-page -->

## A minimal PyTorch implementation

raw is already in mol/L; feed has shape (batch, 1).

```python
raw = y_mean + y_scale * net(x_scaled)
residual = raw.sum(dim=-1, keepdim=True) - feed
y_projected = raw - residual / 3.0
loss = ((y_projected - y_true) / c_scale).square().mean()
optimizer.zero_grad()
loss.backward()
optimizer.step()
```

Projection adds no trainable parameters. The companion and lab script include the general B implementation and gradient checks.

<!-- lecture-page -->

## A correct sum can still contain negative concentrations

Raw [0.02, 0.90, 0.50] mol/L sums to 1.42. Projection to 1.20 gives [−0.053333, 0.826667, 0.426667] mol/L.

The sum is correct and A is negative. Clamping just the negative value to zero changes the sum to about 1.253333.

To require both nonnegativity and the sum, use a method including those inequalities, such as simplex projection. Its gradient changes by region as active inequalities change.

<!-- lecture-page -->

## Accuracy statements require a metric and assumptions

If reference <math><msup><mrow><mi>y</mi></mrow><mrow><mo>∗</mo></mrow></msup></math> lies in the same affine set, orthogonality gives:

<math display="block"><mtable columnalign="left"><mtr><mtd><mrow><msup><mrow><mo>‖</mo><mover><mi>y</mi><mo>^</mo></mover><mo>−</mo><msup><mrow><mi>y</mi></mrow><mrow><mo>∗</mo></mrow></msup><mo>‖</mo></mrow><mrow><mn>2</mn></mrow></msup><mo>=</mo><msup><mrow><mo>‖</mo><mover><mi>y</mi><mo>^</mo></mover><mo>−</mo><msub><mrow><mi>y</mi></mrow><mrow><mi>p</mi></mrow></msub><mo>‖</mo></mrow><mrow><mn>2</mn></mrow></msup><mo>+</mo><msup><mrow><mo>‖</mo><msub><mrow><mi>y</mi></mrow><mrow><mi>p</mi></mrow></msub><mo>−</mo><msup><mrow><mi>y</mi></mrow><mrow><mo>∗</mo></mrow></msup><mo>‖</mo></mrow><mrow><mn>2</mn></mrow></msup></mrow></mtd></mtr></mtable></math>

Thus physical-space projection of the same raw prediction cannot increase total squared Euclidean error. An individual component error can increase.

If noisy labels lie outside the set, or projection uses another weighted metric, this physical Euclidean comparison does not directly apply. The identity also does not rank two separately trained models.

<!-- lecture-page -->

## Fix the comparison protocol

Use T = 305-355 K, τ = 1-8 min, C_Af = 0.8-1.5 mol/L. Rates are k₁ = 0.2 exp[6000(1/330 − 1/T)] and k₂ = 0.1 exp[5000(1/330 − 1/T)] min⁻¹.

Train/validation/test have 900/300/300 rows, seed 404, and noise-free analytic labels. All models are 3 → 32 → 32 → 3 ReLU MLPs with 1283 parameters.

They share initial weights, batch order, and training statistics. Use Adam 0.001, batches of 128, and the minimum validation physical MSE among 600 epochs; then evaluate test.

<!-- lecture-page -->

## Run results: accuracy and equality violations

| Model | Pooled RMSE | Max sum violation | Negative entries |
| --- | --- | --- | --- |
| MLP | 0.003657 | 1.17e-02 | 1 |
| Soft (λ = 10) | 0.008161 | 6.30e-03 | 5 |
| MLP + post | 0.003426 | 2.22e-16 | 1 |
| Hard | 0.003036 | 3.33e-16 | 1 |

Concentrations and errors are in mol/L. Negative entries count values below −10⁻⁸ among 900 test component values.

In this run, the soft penalty reduced sum violations but increased RMSE. Hard and post satisfied the sum while retaining negative concentrations. One seed does not establish a general accuracy ranking.

<!-- lecture-page -->

## Component RMSE and minimum concentration

| Model | A RMSE | B RMSE | C RMSE | Minimum |
| --- | --- | --- | --- | --- |
| MLP | 0.003866 | 0.003383 | 0.003704 | -0.003451 |
| Soft (λ = 10) | 0.008753 | 0.008742 | 0.006840 | -0.010393 |
| MLP + post | 0.003724 | 0.003015 | 0.003500 | -0.004176 |
| Hard | 0.003728 | 0.002540 | 0.002703 | -0.002822 |

All quantities are in mol/L. Pooled RMSE can hide differences between components.

The minimum covers every component and test row. The hard model also returns a negative value, so nonnegativity cannot be claimed. Record the evaluation tolerance and the actual minimum together.

<!-- lecture-page -->

## Inspect balances that were not enforced

<figure><img src="/assets/courses/surrogate-models/week-04/comparison.png" alt="Pooled RMSE and maximum concentration-sum violation by model" /></figure>
The hard model has species-balance residual RMS 0.002225 mol/(L·min). Satisfying the sum does not make every reaction/outlet relation exact.

Report accuracy, sum violations, nonnegativity, and species balances separately.

<!-- lecture-page -->

## Run the lab and retain the evidence

Download the [lab ZIP](/assets/courses/surrogate-models/week-04/week04-lab.zip), [notebook]({{ page.notebook | relative_url }}), or [Python script]({{ page.lab_script | relative_url }}). Extract the ZIP and run in that folder.

```bash
python -m pip install -r requirements.txt
python week04_lab.py --check-only
python week04_lab.py --output-dir week04-results
```

Outputs retain the split dataset, test predictions, weights, training statistics, validation history, and evaluation JSON. The supplied run used CPU, float64, and PyTorch 2.14.1+cpu.

<!-- lecture-page -->

## Connect the equality to the Week 3 dynamic model

With constant feed and τ within an interval, the exact total-concentration transition is:

<math display="block"><mtable columnalign="left"><mtr><mtd><mrow><msub><mrow><mi>S</mi></mrow><mrow><mi>k</mi><mo>+</mo><mn>1</mn></mrow></msub><mo>=</mo><msub><mrow><mi>C</mi></mrow><mrow><mi>Af</mi></mrow></msub><mo>+</mo><mrow><mo>(</mo><msub><mrow><mi>S</mi></mrow><mrow><mi>k</mi></mrow></msub><mo>−</mo><msub><mrow><mi>C</mi></mrow><mrow><mi>Af</mi></mrow></msub><mo>)</mo></mrow><msup><mrow><mi>e</mi></mrow><mrow><mo>−</mo><mfrac><mrow><mi>Δt</mi></mrow><mrow><mi>τ</mi></mrow></mfrac></mrow></msup></mrow></mtd></mtr></mtable></math>

If S_k differs from C_Af, do not immediately force the next total to C_Af. B = [1, 1, 1] still acts on the next state, but the right side is the transition above.

When τ varies as an input, the right side is nonlinear in inputs. A fixed-B projection remains possible, but the fixed-A affine input layer derived earlier no longer represents it.

<!-- lecture-page -->

## Exercises and submission

1. Project [0.70, 0.45, 0.25] onto total 1.20; backpropagate an upstream gradient [1, 0, 0].
2. Explain feasibility for B rows [1, 1, 1], [2, 2, 2] and d = [1.2, 2.5].
3. Compare λ = 0.1, 1, 10 using validation; evaluate only the selected setting on test.
4. Submit A/B/C RMSE, sum MAE/max, minimum concentration, and species-balance residuals for each model.

The companion supplies derivations and short answer checks. Next week, freeze a trained ReLU predictor and define an optimization problem.

<!-- lecture-page -->

## Reading companion and papers

[Week 4 companion]({{ page.reading_note | relative_url }}) · [English reading PDF]({{ page.reading_pdf_en | relative_url }})

Chen, H., Constante Flores, G. E., & Li, C. (2024). *Physics-informed neural networks with hard linear equality constraints*. Computers & Chemical Engineering, 189, 108764. [DOI](https://doi.org/10.1016/j.compchemeng.2024.108764) · [Public manuscript](https://arxiv.org/abs/2402.07251) · [Author code/data](https://github.com/li-group/KKThPINN).

Raissi, M., Perdikaris, P., & Karniadakis, G. E. (2019). *Physics-informed neural networks: A deep learning framework for solving forward and inverse problems involving nonlinear partial differential equations*. Journal of Computational Physics, 378, 686-707. [DOI](https://doi.org/10.1016/j.jcp.2018.10.045).

<!-- lecture-page -->

## Mathematics, implementation sources, and scope

Boyd, S., & Vandenberghe, L. (2004). *Convex Optimization*. Section 5.5.3 on KKT conditions and Section 10.1 on equality-constrained minimization. [Official book](https://web.stanford.edu/~boyd/cvxbook/).

Official PyTorch documentation: [linear solves](https://docs.pytorch.org/docs/2.14/generated/torch.linalg.solve.html), [numerical gradient checks](https://docs.pytorch.org/docs/2.9/generated/torch.autograd.gradcheck.gradcheck.html). Raissi et al.’s [2017 Part I manuscript](https://arxiv.org/abs/1711.10561) is a separate version from the 2019 journal paper.

The lab is an original analytic CSTR example, not a reproduction of Chen et al.’s Aspen cases. The sum-equality guarantee does not cover extrapolation accuracy, nonlinear thermodynamics, stability, or operating safety.

<!-- ko -->

## 예측 농도의 합이 유입보다 크다

유입 농도가 1.20 mol/L인 반응기에서 MLP가 A·B·C를 [0.70, 0.45, 0.25] mol/L로 예측했습니다. 합은 1.40입니다. 이 출력을 다음 공정의 입력으로 보내도 될까요?

<figure><img src="/assets/courses/surrogate-models/week-04/motivation-ko.svg" alt="유입 1.20과 예측 합 1.40 mol/L가 일치하지 않는 반응기" /></figure>

<!-- lecture-page -->

## 연결된 공정에서는 작은 위반도 전달된다

다음 분리기는 각 성분의 유입량으로 부하를 계산합니다. 반응기 surrogate의 합 오차가 그 계산에 그대로 들어가므로, 예측 오차와 물질수지 위반을 따로 확인해야 합니다.

이번 주에는 loss에 위반을 벌점으로 넣는 방법과, 출력이 지정한 선형 등식을 만족하도록 투영하는 방법을 다뤄봅니다. 보정 전후의 성분 오차도 함께 계산합니다.

<!-- lecture-page -->

## 이번 주에 계산할 것

1. 같은 데이터로 MLP·soft sum penalty·hard sum projection을 비교합니다.
2. 최소 거리 투영을 KKT 조건으로 유도하고 rank 가정을 확인합니다.
3. 고정 투영층의 역전파를 손계산과 자동미분으로 대조합니다.
4. 성분별 오차·등식 위반·음수 농도·미반영 수지를 따로 보고합니다.

실습은 2주차의 정상상태 CSTR를 사용하며, 동적 응답에서 달라지는 제약식은 마지막에 연결합니다.

<!-- lecture-page -->

## 기준 공정과 단위

완전 혼합·일정 부피·같은 유입 및 유출 유량을 가정합니다. A만 유입되며 1:1 연속반응 A → B → C가 일어납니다. 온도 T는 주어지고 에너지수지는 모델에 포함하지 않습니다.

<math display="block"><mtable columnalign="left"><mtr><mtd><mrow><msub><mrow><mi>C</mi></mrow><mrow><mi>A</mi></mrow></msub><mo>=</mo><mfrac><mrow><msub><mrow><mi>C</mi></mrow><mrow><mi>Af</mi></mrow></msub></mrow><mrow><mn>1</mn><mo>+</mo><msub><mrow><mi>k</mi></mrow><mrow><mn>1</mn></mrow></msub><mi>τ</mi></mrow></mfrac></mrow></mtd></mtr><mtr><mtd><mrow><msub><mrow><mi>C</mi></mrow><mrow><mi>B</mi></mrow></msub><mo>=</mo><mfrac><mrow><msub><mrow><mi>k</mi></mrow><mrow><mn>1</mn></mrow></msub><mi>τ</mi><msub><mrow><mi>C</mi></mrow><mrow><mi>A</mi></mrow></msub></mrow><mrow><mn>1</mn><mo>+</mo><msub><mrow><mi>k</mi></mrow><mrow><mn>2</mn></mrow></msub><mi>τ</mi></mrow></mfrac><mo>,</mo><mtext>  </mtext><msub><mrow><mi>C</mi></mrow><mrow><mi>C</mi></mrow></msub><mo>=</mo><msub><mrow><mi>k</mi></mrow><mrow><mn>2</mn></mrow></msub><mi>τ</mi><msub><mrow><mi>C</mi></mrow><mrow><mi>B</mi></mrow></msub></mrow></mtd></mtr></mtable></math>

330 K에서 k₁ = 0.2 min⁻¹, k₂ = 0.1 min⁻¹입니다. τ = 5 min, C_Af = 1.2 mol/L이면 [C_A, C_B, C_C] = [0.6, 0.4, 0.2] mol/L입니다.

<!-- lecture-page -->

## 농도 합 등식은 어디서 나오는가

각 정상상태 성분수지의 우변을 r_A, r_B, r_C라고 놓고 더하면 반응항이 상쇄됩니다.

<math display="block"><mtable columnalign="left"><mtr><mtd><mrow><msub><mrow><mi>r</mi></mrow><mrow><mi>A</mi></mrow></msub><mo>+</mo><msub><mrow><mi>r</mi></mrow><mrow><mi>B</mi></mrow></msub><mo>+</mo><msub><mrow><mi>r</mi></mrow><mrow><mi>C</mi></mrow></msub><mo>=</mo><mfrac><mrow><msub><mrow><mi>C</mi></mrow><mrow><mi>Af</mi></mrow></msub><mo>−</mo><mrow><mo>(</mo><msub><mrow><mi>C</mi></mrow><mrow><mi>A</mi></mrow></msub><mo>+</mo><msub><mrow><mi>C</mi></mrow><mrow><mi>B</mi></mrow></msub><mo>+</mo><msub><mrow><mi>C</mi></mrow><mrow><mi>C</mi></mrow></msub><mo>)</mo></mrow></mrow><mrow><mi>τ</mi></mrow></mfrac></mrow></mtd></mtr></mtable></math>

정상상태에서는 각 residual이 0이므로 S = C_A + C_B + C_C = C_Af입니다. 이 농도 합 보존은 위 화학양론과 유량 가정에 의존합니다. 일반 반응에서는 원소수지나 질량수지를 해당 단위로 다시 구성해야 합니다.

<!-- lecture-page -->

## 성분 오차와 합 오차를 구분하기

| 예측 [mol/L] | 성분 오차 [mol/L] | 합 residual [mol/L] |
| --- | --- | --- |
| [0.70, 0.45, 0.25] | [+0.10, +0.05, +0.05] | +0.20 |
| [0.70, 0.30, 0.20] | [+0.10, −0.10, 0.00] | 0.00 |

기준값은 [0.60, 0.40, 0.20] mol/L입니다. 두 번째 예측은 합을 맞추지만 A와 B가 틀립니다. 등식 만족만으로 예측 품질을 판단하면 이 오차를 놓칩니다.

<!-- lecture-page -->

## Residual을 먼저 정의하기

농도 합 residual은 r_sum = C_A + C_B + C_C − C_Af이며 단위는 mol/L입니다. 알려진 속도식을 사용하면 성분별 정상상태 residual도 계산할 수 있습니다.

<math display="block"><mtable columnalign="left"><mtr><mtd><mrow><msub><mrow><mi>r</mi></mrow><mrow><mi>A</mi></mrow></msub><mo>=</mo><mfrac><mrow><msub><mrow><mi>C</mi></mrow><mrow><mi>Af</mi></mrow></msub><mo>−</mo><msub><mrow><mi>C</mi></mrow><mrow><mi>A</mi></mrow></msub></mrow><mrow><mi>τ</mi></mrow></mfrac><mo>−</mo><msub><mrow><mi>k</mi></mrow><mrow><mn>1</mn></mrow></msub><msub><mrow><mi>C</mi></mrow><mrow><mi>A</mi></mrow></msub></mrow></mtd></mtr><mtr><mtd><mrow><msub><mrow><mi>r</mi></mrow><mrow><mi>B</mi></mrow></msub><mo>=</mo><msub><mrow><mi>k</mi></mrow><mrow><mn>1</mn></mrow></msub><msub><mrow><mi>C</mi></mrow><mrow><mi>A</mi></mrow></msub><mo>−</mo><mfrac><mrow><msub><mrow><mi>C</mi></mrow><mrow><mi>B</mi></mrow></msub></mrow><mrow><mi>τ</mi></mrow></mfrac><mo>−</mo><msub><mrow><mi>k</mi></mrow><mrow><mn>2</mn></mrow></msub><msub><mrow><mi>C</mi></mrow><mrow><mi>B</mi></mrow></msub></mrow></mtd></mtr><mtr><mtd><mrow><msub><mrow><mi>r</mi></mrow><mrow><mi>C</mi></mrow></msub><mo>=</mo><msub><mrow><mi>k</mi></mrow><mrow><mn>2</mn></mrow></msub><msub><mrow><mi>C</mi></mrow><mrow><mi>B</mi></mrow></msub><mo>−</mo><mfrac><mrow><msub><mrow><mi>C</mi></mrow><mrow><mi>C</mi></mrow></msub></mrow><mrow><mi>τ</mi></mrow></mfrac></mrow></mtd></mtr></mtable></math>

이 세 residual의 단위는 mol/(L·min)입니다. 실습은 합 residual만 학습에 사용하고, 성분수지 residual은 별도 평가로 남깁니다.

<!-- lecture-page -->

## Soft penalty: 데이터와 등식 위반을 함께 줄이기

<math display="block"><mtable columnalign="left"><mtr><mtd><mrow><msub><mrow><mi>L</mi></mrow><mrow><mi>soft</mi></mrow></msub><mo>=</mo><mfrac><mrow><mn>1</mn></mrow><mrow><mn>3</mn><mi>N</mi></mrow></mfrac><msub><mrow><mo>∑</mo></mrow><mrow><mi>i</mi></mrow></msub><msup><mrow><mo>‖</mo><mfrac><mrow><msub><mrow><mover><mi>y</mi><mo>^</mo></mover></mrow><mrow><mi>i</mi></mrow></msub><mo>−</mo><msub><mrow><mi>y</mi></mrow><mrow><mi>i</mi></mrow></msub></mrow><mrow><msub><mrow><mi>c</mi></mrow><mrow><mo>∗</mo></mrow></msub></mrow></mfrac><mo>‖</mo></mrow><mrow><mn>2</mn></mrow></msup><mo>+</mo><mi>λ</mi><mfrac><mrow><mn>1</mn></mrow><mrow><mi>N</mi></mrow></mfrac><msub><mrow><mo>∑</mo></mrow><mrow><mi>i</mi></mrow></msub><msup><mrow><mrow><mo>(</mo><mfrac><mrow><msub><mrow><mi>r</mi></mrow><mrow><mi>sum</mi><mo>,</mo><mi>i</mi></mrow></msub></mrow><mrow><msub><mrow><mi>c</mi></mrow><mrow><mo>∗</mo></mrow></msub></mrow></mfrac><mo>)</mo></mrow></mrow><mrow><mn>2</mn></mrow></msup></mrow></mtd></mtr></mtable></math>

두 항은 <math><msub><mrow><mi>c</mi></mrow><mrow><mo>∗</mo></mrow></msub></math> = 1 mol/L로 무차원화합니다. 실습의 λ = 10은 합 residual 한 개와 성분 오차 세 개의 평균 정의까지 포함한 선택입니다.

λ를 바꾸면 학습 목표와 gradient 크기가 달라집니다. 유한한 λ와 학습 종료만으로 모든 입력의 residual이 0이라고 보장할 수는 없습니다.

<!-- lecture-page -->

## 유한한 벌점의 해를 직접 구하기

스칼라 예제로 ½(z − a)² + ½λ(z − b)²를 최소화합니다. 데이터는 a를, 등식은 z = b를 요구하며 λ ≥ 0입니다. 미분을 0으로 놓으면:

<math display="block"><mtable columnalign="left"><mtr><mtd><mrow><msub><mrow><mi>z</mi></mrow><mrow><mo>∗</mo></mrow></msub><mo>=</mo><mfrac><mrow><mi>a</mi><mo>+</mo><mi>λ</mi><mi>b</mi></mrow><mrow><mn>1</mn><mo>+</mo><mi>λ</mi></mrow></mfrac></mrow></mtd></mtr><mtr><mtd><mrow><msub><mrow><mi>z</mi></mrow><mrow><mo>∗</mo></mrow></msub><mo>−</mo><mi>b</mi><mo>=</mo><mfrac><mrow><mi>a</mi><mo>−</mo><mi>b</mi></mrow><mrow><mn>1</mn><mo>+</mo><mi>λ</mi></mrow></mfrac></mrow></mtd></mtr></mtable></math>

a ≠ b일 때 residual은 유한한 λ에서 남습니다. λ를 매우 크게 잡으면 손실항의 크기 차이와 수치 조건도 확인해야 합니다. 이 계산은 penalty가 항상 정확한 등식을 주지는 않는다는 반례입니다.

<!-- lecture-page -->

## 자동미분에서 무엇을 미분하는가

현재 실습의 MLP는 [T, τ, C_Af]에서 정상 농도로 가는 mapping입니다. Loss를 파라미터 θ로 미분하며, 합 residual과 정상상태 성분수지에는 시간 미분이 필요하지 않습니다.

연속시간 PINN에서 y_θ(t)를 사용한다면 residual은 ∂y_θ/∂t − F(y_θ, u)처럼 좌표 미분도 포함합니다. 이는 θ에 대한 학습 gradient와 구분해야 합니다.

시간을 t̃ = (t − μ_t)/s_t로 표준화했다면 ∂y/∂t = (1/s_t)∂y/∂t̃입니다.

<!-- lecture-page -->

## Hard 등식: 입력이 정해지면 가능한 출력 집합이 정해진다

<math display="block"><mtable columnalign="left"><mtr><mtd><mrow><mi>A</mi><mi>x</mi><mo>+</mo><mi>B</mi><mi>y</mi><mo>=</mo><mi>b</mi><mo>,</mo></mrow></mtd></mtr><mtr><mtd><mrow><mi>B</mi><mi>y</mi><mo>=</mo><mi>d</mi><mrow><mo>(</mo><mi>x</mi><mo>)</mo></mrow><mo>,</mo><mtext>  </mtext><mi>d</mi><mrow><mo>(</mo><mi>x</mi><mo>)</mo></mrow><mo>=</mo><mi>b</mi><mo>−</mo><mi>A</mi><mi>x</mi></mrow></mtd></mtr></mtable></math>

x ∈ ℝᵖ, y ∈ ℝⁿ, A ∈ ℝᵐˣᵖ, B ∈ ℝᵐˣⁿ, b ∈ ℝᵐ입니다. A·B·b는 고정 계수이고, raw 출력은 ŷ = f_θ(x)입니다.

CSTR에서는 x = [T, τ, C_Af], A = [0, 0, −1], B = [1, 1, 1], b = 0입니다. 따라서 d(x) = C_Af입니다.

<!-- lecture-page -->

## 가장 가까운 등식 만족 출력

<math display="block"><mtable columnalign="left"><mtr><mtd><mrow><msub><mrow><mi>y</mi></mrow><mrow><mi>p</mi></mrow></msub><mo>=</mo><msub><mrow><mi>argmin</mi></mrow><mrow><mi>z</mi></mrow></msub><mtext>  </mtext><mfrac><mrow><mn>1</mn></mrow><mrow><mn>2</mn></mrow></mfrac><msup><mrow><mo>‖</mo><mi>z</mi><mo>−</mo><mover><mi>y</mi><mo>^</mo></mover><mo>‖</mo></mrow><mrow><mn>2</mn></mrow></msup><mtext>   subject to   </mtext><mi>B</mi><mi>z</mi><mo>=</mo><mi>d</mi><mrow><mo>(</mo><mi>x</mi><mo>)</mo></mrow></mrow></mtd></mtr></mtable></math>

입력 x와 raw 예측 ŷ를 고정한 뒤 출력 z만 조정합니다. 여기서 거리는 물리 농도 좌표의 Euclidean 거리입니다.

목적함수는 strictly convex입니다. 가능한 집합이 비어 있지 않으면 투영 출력은 유일합니다. 등식만 있는 이 작은 QP는 KKT 조건으로 닫힌 형태를 구할 수 있습니다.

<!-- lecture-page -->

## Lagrangian과 KKT 조건

<math display="block"><mtable columnalign="left"><mtr><mtd><mrow><mi>ℒ</mi><mrow><mo>(</mo><mi>z</mi><mo>,</mo><mi>λ</mi><mo>)</mo></mrow><mo>=</mo><mfrac><mrow><mn>1</mn></mrow><mrow><mn>2</mn></mrow></mfrac><msup><mrow><mo>‖</mo><mi>z</mi><mo>−</mo><mover><mi>y</mi><mo>^</mo></mover><mo>‖</mo></mrow><mrow><mn>2</mn></mrow></msup><mo>+</mo><msup><mrow><mi>λ</mi></mrow><mrow><mi>T</mi></mrow></msup><mrow><mo>(</mo><mi>B</mi><mi>z</mi><mo>−</mo><mi>d</mi><mo>)</mo></mrow></mrow></mtd></mtr></mtable></math>

정지조건과 primal feasibility를 함께 만족시킵니다.

<math display="block"><mtable columnalign="left"><mtr><mtd><mrow><mi>z</mi><mo>−</mo><mover><mi>y</mi><mo>^</mo></mover><mo>+</mo><msup><mrow><mi>B</mi></mrow><mrow><mi>T</mi></mrow></msup><mi>λ</mi><mo>=</mo><mn>0</mn><mo>,</mo><mtext>  </mtext><mi>B</mi><mi>z</mi><mo>=</mo><mi>d</mi></mrow></mtd></mtr></mtable></math>

부등식이 없으므로 complementary slackness나 multiplier의 부호 제약은 없습니다. Strictly convex 목적함수와 affine 등식에서는 이 조건을 만족하는 출력이 전역 최소점입니다.

<!-- lecture-page -->

## Multiplier를 제거해 투영식 얻기

정지조건에서 z = ŷ − Bᵀλ를 얻고 Bz = d에 대입합니다.

<math display="block"><mtable columnalign="left"><mtr><mtd><mrow><mi>G</mi><mo>=</mo><mi>B</mi><msup><mrow><mi>B</mi></mrow><mrow><mi>T</mi></mrow></msup><mo>,</mo><mtext>  </mtext><mi>G</mi><mi>λ</mi><mo>=</mo><mi>B</mi><mover><mi>y</mi><mo>^</mo></mover><mo>−</mo><mi>d</mi></mrow></mtd></mtr><mtr><mtd><mrow><msub><mrow><mi>y</mi></mrow><mrow><mi>p</mi></mrow></msub><mo>=</mo><mover><mi>y</mi><mo>^</mo></mover><mo>−</mo><msup><mrow><mi>B</mi></mrow><mrow><mi>T</mi></mrow></msup><msup><mrow><mi>G</mi></mrow><mrow><mo>−</mo><mn>1</mn></mrow></msup><mrow><mo>(</mo><mi>B</mi><mover><mi>y</mi><mo>^</mo></mover><mo>−</mo><mi>d</mi><mo>)</mo></mrow></mrow></mtd></mtr></mtable></math>

rank(B) = m이면 G = BBᵀ는 양의 정부호입니다. 식에서는 역행렬로 표현하지만 구현은 Gλ = Bŷ − d를 풉니다. 고정 B라면 분해나 고정 투영 계수를 재사용할 수 있습니다.

<!-- lecture-page -->

## KKT-hPINN의 고정 affine 출력층

<math display="block"><mtable columnalign="left"><mtr><mtd><mrow><mi>P</mi><mo>=</mo><mi>I</mi><mo>−</mo><msup><mrow><mi>B</mi></mrow><mrow><mi>T</mi></mrow></msup><msup><mrow><mi>G</mi></mrow><mrow><mo>−</mo><mn>1</mn></mrow></msup><mi>B</mi></mrow></mtd></mtr><mtr><mtd><mrow><msub><mrow><mi>y</mi></mrow><mrow><mi>p</mi></mrow></msub><mo>=</mo><mi>P</mi><msub><mrow><mi>f</mi></mrow><mrow><mi>θ</mi></mrow></msub><mrow><mo>(</mo><mi>x</mi><mo>)</mo></mrow><mo>+</mo><msup><mrow><mi>B</mi></mrow><mrow><mi>T</mi></mrow></msup><msup><mrow><mi>G</mi></mrow><mrow><mo>−</mo><mn>1</mn></mrow></msup><mrow><mo>(</mo><mi>b</mi><mo>−</mo><mi>A</mi><mi>x</mi><mo>)</mo></mrow></mrow></mtd></mtr></mtable></math>

이 층의 계수는 물리 등식으로 정하고 학습하지 않습니다. MLP 가중치 θ는 투영된 출력의 loss로 학습합니다.

<math display="block"><mtable columnalign="left"><mtr><mtd><mrow><mi>B</mi><msub><mrow><mi>y</mi></mrow><mrow><mi>p</mi></mrow></msub><mo>=</mo><mi>B</mi><mover><mi>y</mi><mo>^</mo></mover><mo>−</mo><mi>G</mi><msup><mrow><mi>G</mi></mrow><mrow><mo>−</mo><mn>1</mn></mrow></msup><mrow><mo>(</mo><mi>B</mi><mover><mi>y</mi><mo>^</mo></mover><mo>−</mo><mi>d</mi><mo>)</mo></mrow><mo>=</mo><mi>d</mi></mrow></mtd></mtr></mtable></math>

지정한 등식은 학습 중과 추론 시 모두 만족합니다. 실제 구현에서는 floating-point 오차와 선형계의 수치 조건을 확인합니다. 출처: Chen et al. (2024).

<!-- lecture-page -->

## Rank와 일관성은 별도로 확인한다

| 경우 | 판단 |
| --- | --- |
| rank(B) = m ≤ n | 모든 d에 출력 해가 존재하며 BBᵀ가 가역입니다. |
| 중복 행, 일관된 d | 가능한 출력은 존재해도 BBᵀ는 특이합니다. 독립 행이나 SVD를 사용합니다. |
| 중복 행, 모순된 d | 가능한 출력이 없습니다. Pseudoinverse로도 모든 등식을 맞출 수 없습니다. |

거의 종속인 행은 rank 판정 tolerance와 condition number도 살펴봅니다. 등식의 단위와 크기를 맞추는 row scaling은 가능한 집합을 바꾸지 않습니다.

<!-- lecture-page -->

## 농도 합 투영을 손으로 계산하기

<math display="block"><mtable columnalign="left"><mtr><mtd><mrow><mi>B</mi><mo>=</mo><mrow><mo>[</mo><mtable><mtr><mtd><mrow><mn>1</mn></mrow></mtd><mtd><mrow><mn>1</mn></mrow></mtd><mtd><mrow><mn>1</mn></mrow></mtd></mtr></mtable><mo>]</mo></mrow><mo>,</mo><mtext>  </mtext><mi>d</mi><mo>=</mo><mn>1.2</mn></mrow></mtd></mtr><mtr><mtd><mrow><msub><mrow><mi>y</mi></mrow><mrow><mi>p</mi></mrow></msub><mo>=</mo><mrow><mo>[</mo><mtable><mtr><mtd><mrow><mn>.70</mn></mrow></mtd></mtr><mtr><mtd><mrow><mn>.45</mn></mrow></mtd></mtr><mtr><mtd><mrow><mn>.25</mn></mrow></mtd></mtr></mtable><mo>]</mo></mrow><mo>−</mo><mfrac><mrow><mn>.20</mn></mrow><mrow><mn>3</mn></mrow></mfrac><mrow><mo>[</mo><mtable><mtr><mtd><mrow><mn>1</mn></mrow></mtd></mtr><mtr><mtd><mrow><mn>1</mn></mrow></mtd></mtr><mtr><mtd><mrow><mn>1</mn></mrow></mtd></mtr></mtable><mo>]</mo></mrow><mo>=</mo><mrow><mo>[</mo><mtable><mtr><mtd><mrow><mn>.633333</mn></mrow></mtd></mtr><mtr><mtd><mrow><mn>.383333</mn></mrow></mtd></mtr><mtr><mtd><mrow><mn>.183333</mn></mrow></mtd></mtr></mtable><mo>]</mo></mrow></mrow></mtd></mtr></mtable></math>

세 성분에서 같은 0.066667 mol/L를 뺍니다. 합은 1.20이지만 기준 [0.60, 0.40, 0.20]과는 다릅니다.

값은 표시 자릿수로 반올림했습니다. 계산에서는 중간값을 반올림하지 않고, 최종 합 residual을 확인합니다.

<!-- lecture-page -->

## 학습 후 보정과 투영층을 포함한 학습

| 방법 | 학습 loss에 들어가는 출력 |
| --- | --- |
| MLP + 학습 후 투영 | Raw 예측으로 학습하고 test에서 투영합니다. |
| KKT-hPINN 방식 | 학습할 때부터 투영 출력을 loss에 넣습니다. |

<figure><img src="/assets/courses/surrogate-models/week-04/flow-ko.svg" alt="MLP 출력, 고정 투영, 데이터 loss와 역전파 경로" /></figure>
두 방법은 같은 등식을 만족시킬 수 있지만, gradient가 달라 학습된 파라미터는 일반적으로 다릅니다.

<!-- lecture-page -->

## 고정된 층도 gradient를 전달한다

<math display="block"><mtable columnalign="left"><mtr><mtd><mrow><mfrac><mrow><mi>∂</mi><msub><mrow><mi>y</mi></mrow><mrow><mi>p</mi></mrow></msub></mrow><mrow><mi>∂</mi><mover><mi>y</mi><mo>^</mo></mover></mrow></mfrac><mo>=</mo><mi>P</mi></mrow></mtd></mtr><mtr><mtd><mrow><msub><mrow><mi>∇</mi></mrow><mrow><mover><mi>y</mi><mo>^</mo></mover></mrow></msub><mi>L</mi><mo>=</mo><msup><mrow><mi>P</mi></mrow><mrow><mi>T</mi></mrow></msup><msub><mrow><mi>∇</mi></mrow><mrow><msub><mrow><mi>y</mi></mrow><mrow><mi>p</mi></mrow></msub></mrow></msub><mi>L</mi></mrow></mtd></mtr></mtable></math>

P는 대칭인 orthogonal projector이므로 Pᵀ = P입니다. 학습하지 않는 계수라는 사실과 미분 경로가 없다는 주장은 다릅니다.

출력을 detach하거나 투영 계산을 no_grad로 감싸면 필요한 경로가 끊깁니다. θ에 대한 gradient는 MLP Jacobian까지 chain rule로 이어집니다.

<!-- lecture-page -->

## 역전파를 세 성분으로 확인하기

<math display="block"><mtable columnalign="left"><mtr><mtd><mrow><mi>P</mi><mo>=</mo><mi>I</mi><mo>−</mo><mfrac><mrow><mn>1</mn></mrow><mrow><mn>3</mn></mrow></mfrac><mrow><mo>[</mo><mtable><mtr><mtd><mrow><mn>1</mn></mrow></mtd><mtd><mrow><mn>1</mn></mrow></mtd><mtd><mrow><mn>1</mn></mrow></mtd></mtr><mtr><mtd><mrow><mn>1</mn></mrow></mtd><mtd><mrow><mn>1</mn></mrow></mtd><mtd><mrow><mn>1</mn></mrow></mtd></mtr><mtr><mtd><mrow><mn>1</mn></mrow></mtd><mtd><mrow><mn>1</mn></mrow></mtd><mtd><mrow><mn>1</mn></mrow></mtd></mtr></mtable><mo>]</mo></mrow></mrow></mtd></mtr><mtr><mtd><mrow><msup><mrow><mi>P</mi></mrow><mrow><mi>T</mi></mrow></msup><mrow><mo>[</mo><mtable><mtr><mtd><mrow><mn>1</mn></mrow></mtd></mtr><mtr><mtd><mrow><mn>0</mn></mrow></mtd></mtr><mtr><mtd><mrow><mn>0</mn></mrow></mtd></mtr></mtable><mo>]</mo></mrow><mo>=</mo><mrow><mo>[</mo><mtable><mtr><mtd><mrow><mfrac><mrow><mn>2</mn></mrow><mrow><mn>3</mn></mrow></mfrac></mrow></mtd></mtr><mtr><mtd><mrow><mfrac><mrow><mo>−</mo><mn>1</mn></mrow><mrow><mn>3</mn></mrow></mfrac></mrow></mtd></mtr><mtr><mtd><mrow><mfrac><mrow><mo>−</mo><mn>1</mn></mrow><mrow><mn>3</mn></mrow></mfrac></mrow></mtd></mtr></mtable><mo>]</mo></mrow></mrow></mtd></mtr></mtable></math>

투영 출력에서 올라온 gradient가 [1, 0, 0]이면 raw 출력에 전달되는 값은 [2/3, −1/3, −1/3]입니다. 합이 0이므로 등식의 접공간 방향입니다.

실습은 두 개의 독립 등식에서도 analytic Jacobian과 double-precision gradcheck를 확인합니다.

<!-- lecture-page -->

## 출력 표준화를 하면 B도 변한다

<math display="block"><mtable columnalign="left"><mtr><mtd><mrow><mi>y</mi><mo>=</mo><mi>μ</mi><mo>+</mo><mi>D</mi><mi>z</mi><mo>,</mo><mtext>  </mtext><mi>B</mi><mi>D</mi><mi>z</mi><mo>=</mo><mi>d</mi><mo>−</mo><mi>B</mi><mi>μ</mi></mrow></mtd></mtr><mtr><mtd><mrow><mi>D</mi><mo>=</mo><mi>diag</mi><mrow><mo>(</mo><msub><mrow><mi>s</mi></mrow><mrow><mn>1</mn></mrow></msub><mo>,</mo><mi>…</mi><mo>,</mo><msub><mrow><mi>s</mi></mrow><mrow><mi>n</mi></mrow></msub><mo>)</mo></mrow></mrow></mtd></mtr></mtable></math>

μ와 양의 scale s_j는 train 데이터로만 계산합니다. 표준화 좌표 z에서 투영하려면 B 대신 BD, 우변 대신 d − Bμ를 사용해야 합니다.

표준화 공간의 최소 거리와 물리 공간의 최소 거리는 s_j가 서로 다르면 다릅니다. 등식의 만족과 어떤 거리로 보정하는지를 각각 명시합니다.

<!-- lecture-page -->

## 실습의 선택: 물리 단위로 복원한 뒤 투영

MLP는 표준화 출력 z를 만들고, μ + Dz로 mol/L를 복원한 뒤 물리 공간에서 투영합니다. 데이터 loss는 모든 성분에 공통인 <math><msub><mrow><mi>c</mi></mrow><mrow><mo>∗</mo></mrow></msub></math> = 1 mol/L로 나눕니다.

<math display="block"><mtable columnalign="left"><mtr><mtd><mrow><msub><mrow><mi>∇</mi></mrow><mrow><mi>z</mi></mrow></msub><mi>L</mi><mo>=</mo><msup><mrow><mi>D</mi></mrow><mrow><mi>T</mi></mrow></msup><msup><mrow><mi>P</mi></mrow><mrow><mi>T</mi></mrow></msup><msub><mrow><mi>∇</mi></mrow><mrow><msub><mrow><mi>y</mi></mrow><mrow><mi>p</mi></mrow></msub></mrow></msub><mi>L</mi></mrow></mtd></mtr></mtable></math>

D는 대각행렬이라 Dᵀ = D입니다. 성분별 표준편차로 loss까지 나누는 경우에는 그 가중치도 gradient와 오차 해석에 반영해야 합니다.

<!-- lecture-page -->

## PyTorch의 최소 구현

raw는 이미 mol/L 단위이고 feed의 shape은 (batch, 1)입니다.

```python
raw = y_mean + y_scale * net(x_scaled)
residual = raw.sum(dim=-1, keepdim=True) - feed
y_projected = raw - residual / 3.0
loss = ((y_projected - y_true) / c_scale).square().mean()
optimizer.zero_grad()
loss.backward()
optimizer.step()
```

투영에는 학습 파라미터가 추가되지 않습니다. 일반 B의 구현과 gradient 확인은 읽기자료와 실습 스크립트에 있습니다.

<!-- lecture-page -->

## 합을 맞춰도 음수 농도는 남을 수 있다

Raw [0.02, 0.90, 0.50] mol/L의 합은 1.42입니다. 1.20으로 투영하면 [−0.053333, 0.826667, 0.426667] mol/L가 됩니다.

합은 맞고 A는 음수입니다. 음수만 0으로 자르면 합이 약 1.253333으로 바뀝니다.

비음수성과 합을 함께 요구하려면 simplex 투영처럼 해당 부등식까지 포함한 방법이 필요합니다. 활성 부등식이 바뀌면 gradient도 구간별로 달라집니다.

<!-- lecture-page -->

## 투영과 정확도의 관계에는 조건이 있다

기준 <math><msup><mrow><mi>y</mi></mrow><mrow><mo>∗</mo></mrow></msup></math>가 같은 affine 집합에 있으면 Euclidean 투영의 직교성으로:

<math display="block"><mtable columnalign="left"><mtr><mtd><mrow><msup><mrow><mo>‖</mo><mover><mi>y</mi><mo>^</mo></mover><mo>−</mo><msup><mrow><mi>y</mi></mrow><mrow><mo>∗</mo></mrow></msup><mo>‖</mo></mrow><mrow><mn>2</mn></mrow></msup><mo>=</mo><msup><mrow><mo>‖</mo><mover><mi>y</mi><mo>^</mo></mover><mo>−</mo><msub><mrow><mi>y</mi></mrow><mrow><mi>p</mi></mrow></msub><mo>‖</mo></mrow><mrow><mn>2</mn></mrow></msup><mo>+</mo><msup><mrow><mo>‖</mo><msub><mrow><mi>y</mi></mrow><mrow><mi>p</mi></mrow></msub><mo>−</mo><msup><mrow><mi>y</mi></mrow><mrow><mo>∗</mo></mrow></msup><mo>‖</mo></mrow><mrow><mn>2</mn></mrow></msup></mrow></mtd></mtr></mtable></math>

따라서 같은 raw 예측을 물리 공간에서 투영하면 전체 제곱오차는 증가하지 않습니다. 성분 하나의 오차는 커질 수 있습니다.

측정 잡음으로 기준값이 집합 밖에 있거나 다른 가중 metric을 사용하면 이 물리 Euclidean 비교를 그대로 적용할 수 없습니다. 별도로 학습한 두 모델의 우열도 이 식에서 나오지 않습니다.

<!-- lecture-page -->

## 비교 실험의 조건을 고정하기

입력 영역은 T = 305-355 K, τ = 1-8 min, C_Af = 0.8-1.5 mol/L입니다. 속도식은 k₁ = 0.2 exp[6000(1/330 − 1/T)], k₂ = 0.1 exp[5000(1/330 − 1/T)] min⁻¹입니다.

Train/validation/test = 900/300/300행, seed = 404, 잡음 없는 analytic label을 사용합니다. 모델은 모두 3 → 32 → 32 → 3 ReLU MLP(1283개 파라미터)입니다.

초기 가중치·batch 순서·train 통계량을 공유합니다. Adam 0.001, batch 128, 600 epoch 중 validation 물리 MSE가 최소인 가중치를 선택하고 test를 평가합니다.

<!-- lecture-page -->

## 실행 결과: 정확도와 등식 위반

| 모델 | 전체 RMSE | 최대 합 위반 | 음수 항목 수 |
| --- | --- | --- | --- |
| MLP | 0.003657 | 1.17e-02 | 1 |
| Soft (λ = 10) | 0.008161 | 6.30e-03 | 5 |
| MLP + post | 0.003426 | 2.22e-16 | 1 |
| Hard | 0.003036 | 3.33e-16 | 1 |

농도와 오차 단위는 mol/L입니다. 음수 항목은 900개 test 성분값 중 −10⁻⁸ 미만인 값입니다.

이번 실행에서 soft penalty는 합 위반을 줄였지만 RMSE가 커졌습니다. Hard와 post는 합을 맞췄고 음수 농도는 남았습니다. 한 seed의 결과이므로 일반적인 정확도 순위를 뜻하지 않습니다.

<!-- lecture-page -->

## 성분별 RMSE와 최소 농도

| 모델 | A RMSE | B RMSE | C RMSE | 최소 농도 |
| --- | --- | --- | --- | --- |
| MLP | 0.003866 | 0.003383 | 0.003704 | -0.003451 |
| Soft (λ = 10) | 0.008753 | 0.008742 | 0.006840 | -0.010393 |
| MLP + post | 0.003724 | 0.003015 | 0.003500 | -0.004176 |
| Hard | 0.003728 | 0.002540 | 0.002703 | -0.002822 |

단위는 모두 mol/L입니다. 전체 RMSE만 보면 성분별 차이를 놓칠 수 있습니다.

최소 농도는 세 성분과 test 행 전체에서 구합니다. Hard 모델도 음수 값을 출력했으므로 비음수성을 주장할 수 없습니다. 평가 tolerance와 실제 최소값을 함께 기록합니다.

<!-- lecture-page -->

## 전체 수지를 만족하는지는 별도로 검사하기

<figure><img src="/assets/courses/surrogate-models/week-04/comparison.png" alt="모델별 pooled RMSE와 최대 농도 합 위반 비교" /></figure>
Hard 모델의 성분수지 residual RMS는 0.002225 mol/(L·min)입니다. 합 등식을 만족해도 각 성분의 반응·유출 관계가 모두 정확하지는 않습니다.

정확도·합 위반·비음수성·성분수지를 각각 보고합니다.

<!-- lecture-page -->

## 실습 실행과 재현 기록

[실습 ZIP](/assets/courses/surrogate-models/week-04/week04-lab.zip), [Notebook]({{ page.notebook | relative_url }}), [Python 스크립트]({{ page.lab_script | relative_url }})를 제공합니다. ZIP을 풀고 같은 폴더에서 실행합니다.

```bash
python -m pip install -r requirements.txt
python week04_lab.py --check-only
python week04_lab.py --output-dir week04-results
```

결과에는 분할된 dataset, test 예측, 모델 가중치, train 통계량, validation 이력과 평가 JSON이 저장됩니다. 제공 수치는 CPU·float64·PyTorch 2.14.1+cpu에서 실행했습니다.

<!-- lecture-page -->

## 3주차 동적 모델에 연결하기

구간 안에서 유입 농도와 τ가 일정하면 총 농도의 정확한 전이는:

<math display="block"><mtable columnalign="left"><mtr><mtd><mrow><msub><mrow><mi>S</mi></mrow><mrow><mi>k</mi><mo>+</mo><mn>1</mn></mrow></msub><mo>=</mo><msub><mrow><mi>C</mi></mrow><mrow><mi>Af</mi></mrow></msub><mo>+</mo><mrow><mo>(</mo><msub><mrow><mi>S</mi></mrow><mrow><mi>k</mi></mrow></msub><mo>−</mo><msub><mrow><mi>C</mi></mrow><mrow><mi>Af</mi></mrow></msub><mo>)</mo></mrow><msup><mrow><mi>e</mi></mrow><mrow><mo>−</mo><mfrac><mrow><mi>Δt</mi></mrow><mrow><mi>τ</mi></mrow></mfrac></mrow></msup></mrow></mtd></mtr></mtable></math>

초기 합 S_k가 C_Af와 다르면 다음 합을 곧바로 C_Af로 강제하면 안 됩니다. 다음 상태의 B = [1, 1, 1]은 같지만 우변은 위 전이식입니다.

τ를 입력으로 바꾸면 우변은 입력의 비선형 함수입니다. 고정 B의 투영은 가능하나 앞서 쓴 고정 A의 affine 입력층으로 표현되지는 않습니다.

<!-- lecture-page -->

## 연습문제와 제출물

1. [0.70, 0.45, 0.25]를 합 1.20에 투영하고 gradient [1, 0, 0]의 역전파를 계산합니다.
2. B의 두 행이 [1, 1, 1], [2, 2, 2]일 때 d = [1.2, 2.5]의 가능 여부를 설명합니다.
3. λ = 0.1, 1, 10을 validation으로 비교하고, 선택한 설정만 test에서 평가합니다.
4. 각 모델의 A/B/C RMSE·합 MAE/최대값·최소 농도·성분수지 residual을 제출합니다.

읽기자료에는 유도와 짧은 답 확인이 있습니다. 다음 주에는 학습을 끝낸 ReLU predictor를 고정하고 최적화 문제를 정의합니다.

<!-- lecture-page -->

## 읽기자료와 논문

[4주차 읽기자료]({{ page.reading_note | relative_url }}) · [국문 읽기 PDF]({{ page.reading_pdf_ko | relative_url }})

Chen, H., Constante Flores, G. E., & Li, C. (2024). *Physics-informed neural networks with hard linear equality constraints*. Computers & Chemical Engineering, 189, 108764. [DOI](https://doi.org/10.1016/j.compchemeng.2024.108764) · [공개 원고](https://arxiv.org/abs/2402.07251) · [저자 코드·데이터](https://github.com/li-group/KKThPINN).

Raissi, M., Perdikaris, P., & Karniadakis, G. E. (2019). *Physics-informed neural networks: A deep learning framework for solving forward and inverse problems involving nonlinear partial differential equations*. Journal of Computational Physics, 378, 686-707. [DOI](https://doi.org/10.1016/j.jcp.2018.10.045).

<!-- lecture-page -->

## 수학·구현 원문과 학습 범위

Boyd, S., & Vandenberghe, L. (2004). *Convex Optimization*. 5.5.3절의 KKT 조건, 10.1절의 등식 제약 최소화. [공식 교재](https://web.stanford.edu/~boyd/cvxbook/).

PyTorch 공식 문서: [선형계 풀이](https://docs.pytorch.org/docs/2.14/generated/torch.linalg.solve.html), [수치 gradient 확인](https://docs.pytorch.org/docs/2.9/generated/torch.autograd.gradcheck.gradcheck.html). Raissi et al.의 [2017 Part I 공개 원고](https://arxiv.org/abs/1711.10561)는 2019 학술지 논문과 별도 버전입니다.

실습은 직접 구성한 analytic CSTR 예제입니다. Chen et al.의 Aspen 공정 사례 재현 결과가 아닙니다. 외삽 정확도·비선형 열역학·안정성·운전 안전성은 지정한 합 등식의 보장 범위 밖입니다.
