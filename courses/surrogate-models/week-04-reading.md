---
layout: "course-note"
title: "Week 4 Reading: Physical Constraints and Projection"
title_ko: "4주차 읽기자료: 물리 제약과 투영"
description: "Residual losses, KKT projection, scaling, and differentiable physical equalities."
description_ko: "Residual loss, KKT 투영, scaling과 미분 가능한 물리 등식을 다룹니다."
material_label: "Week 4 reading"
material_label_ko: "4주차 읽기자료"
updated: "2026-10-20"
permalink: "/courses/surrogate-models/week-04-reading/"
pdf_en: "/assets/courses/surrogate-models/week-04-reading-en.pdf"
pdf_ko: "/assets/courses/surrogate-models/week-04-reading-ko.pdf"
course_id: "surrogate-models"
lecture_note: "/courses/surrogate-models/week-04/"
---

## 1. Derive the sum equality from steady balances

For first-order consecutive reactions A → B → C, steady state requires r_A = r_B = r_C = 0. Solve A first, then substitute into B and C:

<math display="block"><mtable columnalign="left"><mtr><mtd><mrow><msub><mrow><mi>C</mi></mrow><mrow><mi>A</mi></mrow></msub><mo>=</mo><mfrac><mrow><msub><mrow><mi>C</mi></mrow><mrow><mi>Af</mi></mrow></msub></mrow><mrow><mn>1</mn><mo>+</mo><msub><mrow><mi>k</mi></mrow><mrow><mn>1</mn></mrow></msub><mi>τ</mi></mrow></mfrac></mrow></mtd></mtr><mtr><mtd><mrow><msub><mrow><mi>C</mi></mrow><mrow><mi>B</mi></mrow></msub><mo>=</mo><mfrac><mrow><msub><mrow><mi>k</mi></mrow><mrow><mn>1</mn></mrow></msub><mi>τ</mi><msub><mrow><mi>C</mi></mrow><mrow><mi>A</mi></mrow></msub></mrow><mrow><mn>1</mn><mo>+</mo><msub><mrow><mi>k</mi></mrow><mrow><mn>2</mn></mrow></msub><mi>τ</mi></mrow></mfrac><mo>,</mo><mtext>  </mtext><msub><mrow><mi>C</mi></mrow><mrow><mi>C</mi></mrow></msub><mo>=</mo><msub><mrow><mi>k</mi></mrow><mrow><mn>2</mn></mrow></msub><mi>τ</mi><msub><mrow><mi>C</mi></mrow><mrow><mi>B</mi></mrow></msub></mrow></mtd></mtr></mtable></math>

The B balance gives k₁τC_A = (1 + k₂τ)C_B, hence C_B + C_C = k₁τC_A. Combine with C_Af = (1 + k₁τ)C_A from the A balance to obtain the concentration-sum equality.

Check: 330 K, τ = 5 min, and C_Af = 1.2 mol/L give [0.6, 0.4, 0.2].

<!-- lecture-page -->

## 2. The stationary point of a soft penalty

For J(z) = ½(z − a)² + ½λ(z − b)² with λ ≥ 0, dJ/dz = (z − a) + λ(z − b). The second derivative is 1 + λ > 0, so the stationary point is the unique minimizer.

<math display="block"><mtable columnalign="left"><mtr><mtd><mrow><msub><mrow><mi>z</mi></mrow><mrow><mo>∗</mo></mrow></msub><mo>=</mo><mfrac><mrow><mi>a</mi><mo>+</mo><mi>λ</mi><mi>b</mi></mrow><mrow><mn>1</mn><mo>+</mo><mi>λ</mi></mrow></mfrac></mrow></mtd></mtr><mtr><mtd><mrow><msub><mrow><mi>z</mi></mrow><mrow><mo>∗</mo></mrow></msub><mo>−</mo><mi>b</mi><mo>=</mo><mfrac><mrow><mi>a</mi><mo>−</mo><mi>b</mi></mrow><mrow><mn>1</mn><mo>+</mo><mi>λ</mi></mrow></mfrac></mrow></mtd></mtr></mtable></math>

Exercise: set a = 1.4 and b = 1.2; compute the solution and residual for λ = 1 and 9.

Answer check: solutions are 1.30 and 1.22; residuals are 0.10 and 0.02. A finite penalty can leave a residual even at its exact minimizer.

<!-- lecture-page -->

## 3. Equality QP and its KKT derivation

Let B ∈ ℝᵐˣⁿ have rank m and let d ∈ ℝᵐ. Hold the input and raw prediction fixed and solve:

<math display="block"><mtable columnalign="left"><mtr><mtd><mrow><msub><mrow><mi>y</mi></mrow><mrow><mi>p</mi></mrow></msub><mo>=</mo><msub><mrow><mi>argmin</mi></mrow><mrow><mi>z</mi></mrow></msub><mtext>  </mtext><mfrac><mrow><mn>1</mn></mrow><mrow><mn>2</mn></mrow></mfrac><msup><mrow><mo>‖</mo><mi>z</mi><mo>−</mo><mover><mi>y</mi><mo>^</mo></mover><mo>‖</mo></mrow><mrow><mn>2</mn></mrow></msup><mtext>   subject to   </mtext><mi>B</mi><mi>z</mi><mo>=</mo><mi>d</mi><mrow><mo>(</mo><mi>x</mi><mo>)</mo></mrow></mrow></mtd></mtr></mtable></math>

<math display="block"><mtable columnalign="left"><mtr><mtd><mrow><mi>z</mi><mo>−</mo><mover><mi>y</mi><mo>^</mo></mover><mo>+</mo><msup><mrow><mi>B</mi></mrow><mrow><mi>T</mi></mrow></msup><mi>λ</mi><mo>=</mo><mn>0</mn><mo>,</mo><mtext>  </mtext><mi>B</mi><mi>z</mi><mo>=</mo><mi>d</mi></mrow></mtd></mtr></mtable></math>

Stationarity gives z = ŷ − Bᵀλ. Substitution into feasibility gives BBᵀλ = Bŷ − d. Invertibility makes λ and z unique. The equality set is convex and the objective Hessian is I.

<!-- lecture-page -->

## 4. Equality guarantee and projector identities

<math display="block"><mtable columnalign="left"><mtr><mtd><mrow><mi>G</mi><mo>=</mo><mi>B</mi><msup><mrow><mi>B</mi></mrow><mrow><mi>T</mi></mrow></msup><mo>,</mo><mtext>  </mtext><mi>G</mi><mi>λ</mi><mo>=</mo><mi>B</mi><mover><mi>y</mi><mo>^</mo></mover><mo>−</mo><mi>d</mi></mrow></mtd></mtr><mtr><mtd><mrow><msub><mrow><mi>y</mi></mrow><mrow><mi>p</mi></mrow></msub><mo>=</mo><mover><mi>y</mi><mo>^</mo></mover><mo>−</mo><msup><mrow><mi>B</mi></mrow><mrow><mi>T</mi></mrow></msup><msup><mrow><mi>G</mi></mrow><mrow><mo>−</mo><mn>1</mn></mrow></msup><mrow><mo>(</mo><mi>B</mi><mover><mi>y</mi><mo>^</mo></mover><mo>−</mo><mi>d</mi><mo>)</mo></mrow></mrow></mtd></mtr></mtable></math>

Multiplying by B shows that correction cancels the original residual.

<math display="block"><mtable columnalign="left"><mtr><mtd><mrow><mi>B</mi><msub><mrow><mi>y</mi></mrow><mrow><mi>p</mi></mrow></msub><mo>=</mo><mi>B</mi><mover><mi>y</mi><mo>^</mo></mover><mo>−</mo><mi>G</mi><msup><mrow><mi>G</mi></mrow><mrow><mo>−</mo><mn>1</mn></mrow></msup><mrow><mo>(</mo><mi>B</mi><mover><mi>y</mi><mo>^</mo></mover><mo>−</mo><mi>d</mi><mo>)</mo></mrow><mo>=</mo><mi>d</mi></mrow></mtd></mtr></mtable></math>

P = I − Bᵀ(BBᵀ)⁻¹B satisfies Pᵀ = P, P² = P, and BP = 0. It projects onto the null space of B. Feasible raw outputs receive zero correction, and projecting an already projected output changes nothing.

<!-- lecture-page -->

## 5. Hand calculation: correction and error

<math display="block"><mtable columnalign="left"><mtr><mtd><mrow><mi>B</mi><mo>=</mo><mrow><mo>[</mo><mtable><mtr><mtd><mrow><mn>1</mn></mrow></mtd><mtd><mrow><mn>1</mn></mrow></mtd><mtd><mrow><mn>1</mn></mrow></mtd></mtr></mtable><mo>]</mo></mrow><mo>,</mo><mtext>  </mtext><mi>d</mi><mo>=</mo><mn>1.2</mn></mrow></mtd></mtr><mtr><mtd><mrow><msub><mrow><mi>y</mi></mrow><mrow><mi>p</mi></mrow></msub><mo>=</mo><mrow><mo>[</mo><mtable><mtr><mtd><mrow><mn>.70</mn></mrow></mtd></mtr><mtr><mtd><mrow><mn>.45</mn></mrow></mtd></mtr><mtr><mtd><mrow><mn>.25</mn></mrow></mtd></mtr></mtable><mo>]</mo></mrow><mo>−</mo><mfrac><mrow><mn>.20</mn></mrow><mrow><mn>3</mn></mrow></mfrac><mrow><mo>[</mo><mtable><mtr><mtd><mrow><mn>1</mn></mrow></mtd></mtr><mtr><mtd><mrow><mn>1</mn></mrow></mtd></mtr><mtr><mtd><mrow><mn>1</mn></mrow></mtd></mtr></mtable><mo>]</mo></mrow><mo>=</mo><mrow><mo>[</mo><mtable><mtr><mtd><mrow><mn>.633333</mn></mrow></mtd></mtr><mtr><mtd><mrow><mn>.383333</mn></mrow></mtd></mtr><mtr><mtd><mrow><mn>.183333</mn></mrow></mtd></mtr></mtable><mo>]</mo></mrow></mrow></mtd></mtr></mtable></math>

Against reference [0.6, 0.4, 0.2], the raw sum of squared errors is 0.015 (mol/L)². Squared correction norm is 0.04/3 and projected squared error is 1/600 ≈ 0.001667.

The A error changes from +0.10 to +0.033333. B and C change from +0.05 to −0.016667. Calculate aggregate and individual errors separately.

<!-- lecture-page -->

## 6. Chain rule for parameters and inputs

Let J_f,θ be the raw-output parameter Jacobian. For fixed A, B, b:

<math display="block"><mtable columnalign="left"><mtr><mtd><mrow><msub><mrow><mi>∇</mi></mrow><mrow><mi>θ</mi></mrow></msub><mi>L</mi><mo>=</mo><msup><mrow><msub><mrow><mi>J</mi></mrow><mrow><mi>f</mi><mo>,</mo><mi>θ</mi></mrow></msub></mrow><mrow><mi>T</mi></mrow></msup><msup><mrow><mi>P</mi></mrow><mrow><mi>T</mi></mrow></msup><msub><mrow><mi>∇</mi></mrow><mrow><msub><mrow><mi>y</mi></mrow><mrow><mi>p</mi></mrow></msub></mrow></msub><mi>L</mi></mrow></mtd></mtr><mtr><mtd><mrow><mfrac><mrow><mi>∂</mi><msub><mrow><mi>y</mi></mrow><mrow><mi>p</mi></mrow></msub></mrow><mrow><mi>∂</mi><mi>x</mi></mrow></mfrac><mo>=</mo><mi>P</mi><mfrac><mrow><mi>∂</mi><msub><mrow><mi>f</mi></mrow><mrow><mi>θ</mi></mrow></msub></mrow><mrow><mi>∂</mi><mi>x</mi></mrow></mfrac><mo>−</mo><msup><mrow><mi>B</mi></mrow><mrow><mi>T</mi></mrow></msup><msup><mrow><mi>G</mi></mrow><mrow><mo>−</mo><mn>1</mn></mrow></msup><mi>A</mi></mrow></mtd></mtr></mtable></math>

Input gradients include the direct path through d(x) = b − Ax. If B depends on inputs, P does too and additional derivative terms are required; the fixed-projector formula is insufficient.

Check: upstream [1, 0, 0] and B = [1, 1, 1] yield [2/3, −1/3, −1/3].

<!-- lecture-page -->

## 7. Equality and distance in standardized coordinates

<math display="block"><mtable columnalign="left"><mtr><mtd><mrow><mi>y</mi><mo>=</mo><mi>μ</mi><mo>+</mo><mi>D</mi><mi>z</mi><mo>,</mo><mtext>  </mtext><mi>B</mi><mi>D</mi><mi>z</mi><mo>=</mo><mi>d</mi><mo>−</mo><mi>B</mi><mi>μ</mi></mrow></mtd></mtr><mtr><mtd><mrow><mi>D</mi><mo>=</mo><mi>diag</mi><mrow><mo>(</mo><msub><mrow><mi>s</mi></mrow><mrow><mn>1</mn></mrow></msub><mo>,</mo><mi>…</mi><mo>,</mo><msub><mrow><mi>s</mi></mrow><mrow><mi>n</mi></mrow></msub><mo>)</mo></mrow></mrow></mtd></mtr></mtable></math>

Euclidean projection in z minimizes ‖D⁻¹(y − ŷ)‖² in physical coordinates. Its metric differs from physical Euclidean projection.

Example: raw [0.70, 0.45, 0.25], total 1.20, and s = [0.2, 0.5, 0.1] give restored standardized-projection output [0.673333, 0.283333, 0.243333]. Corrections are proportional to s_j².

Both methods satisfy the sum. For outputs with different units, even a physical Euclidean distance depends on unit choices; design the metric explicitly.

<!-- lecture-page -->

## 8. Redundant equalities and inconsistent right sides

<math display="block"><mtable columnalign="left"><mtr><mtd><mrow><mi>B</mi><mo>=</mo><mrow><mo>[</mo><mtable><mtr><mtd><mrow><mn>1</mn></mrow></mtd><mtd><mrow><mn>1</mn></mrow></mtd><mtd><mrow><mn>1</mn></mrow></mtd></mtr><mtr><mtd><mrow><mn>2</mn></mrow></mtd><mtd><mrow><mn>2</mn></mrow></mtd><mtd><mrow><mn>2</mn></mrow></mtd></mtr></mtable><mo>]</mo></mrow></mrow></mtd></mtr></mtable></math>

The second row is twice the first, so rank is 1. With d = [1.2, 2.4], both equations define the same set; retaining one independent row is sufficient.

With d = [1.2, 2.5], twice the first equation contradicts the second. No feasible output exists. A pseudoinverse can return a least-squares result, but cannot make every residual zero.

When discarding small singular values, recheck residuals of removed equations in their original units.

<!-- lecture-page -->

## 9. Nondimensionalization of residuals with different units

The sum residual has units mol/L; species-balance residuals have units mol/(L·min). Adding their squares without scales makes the meaning of λ depend on the unit convention.

For example, choose reference concentration <math><msub><mrow><mi>c</mi></mrow><mrow><mo>∗</mo></mrow></msub></math> and time <math><msub><mrow><mi>t</mi></mrow><mrow><mo>∗</mo></mrow></msub></math>; divide the sum residual by <math><msub><mrow><mi>c</mi></mrow><mrow><mo>∗</mo></mrow></msub></math> and species residuals by <math><msub><mrow><mi>c</mi></mrow><mrow><mo>∗</mo></mrow></msub></math>/<math><msub><mrow><mi>t</mi></mrow><mrow><mo>∗</mo></mrow></msub></math>. Still specify loss averaging and λ after nondimensionalization.

The lab penalizes the sum residual; known kinetics can also define species-balance residuals.

<!-- lecture-page -->

## 10. Accuracy conditions and incorrect physics

<math display="block"><mtable columnalign="left"><mtr><mtd><mrow><msup><mrow><mo>‖</mo><mover><mi>y</mi><mo>^</mo></mover><mo>−</mo><msup><mrow><mi>y</mi></mrow><mrow><mo>∗</mo></mrow></msup><mo>‖</mo></mrow><mrow><mn>2</mn></mrow></msup><mo>=</mo><msup><mrow><mo>‖</mo><mover><mi>y</mi><mo>^</mo></mover><mo>−</mo><msub><mrow><mi>y</mi></mrow><mrow><mi>p</mi></mrow></msub><mo>‖</mo></mrow><mrow><mn>2</mn></mrow></msup><mo>+</mo><msup><mrow><mo>‖</mo><msub><mrow><mi>y</mi></mrow><mrow><mi>p</mi></mrow></msub><mo>−</mo><msup><mrow><mi>y</mi></mrow><mrow><mo>∗</mo></mrow></msup><mo>‖</mo></mrow><mrow><mn>2</mn></mrow></msup></mrow></mtd></mtr></mtable></math>

This decomposition requires <math><msup><mrow><mi>y</mi></mrow><mrow><mo>∗</mo></mrow></msup></math> in the same affine set. The correction is normal to the set while y_p − <math><msup><mrow><mi>y</mi></mrow><mrow><mo>∗</mo></mrow></msup></math> is tangent, so their inner product vanishes.

If the true total is 1.2 but an incorrect equality enforces 1.1, the true output lies outside the set. The minimum Euclidean distance from truth is already 0.1/√3 ≈ 0.057735 mol/L.

Check sensor bias, omitted species, and stoichiometric errors first. Projection enforces an incorrectly specified equality too.

<!-- lecture-page -->

## 11. Joint nonnegativity and concentration-sum constraints

Clamping negative values after equality projection changes the sum. Requiring both the sum and nonnegativity gives:

<math display="block"><mtable columnalign="left"><mtr><mtd><mrow><msub><mrow><mi>min</mi></mrow><mrow><mi>z</mi></mrow></msub><mtext>  </mtext><mfrac><mrow><mn>1</mn></mrow><mrow><mn>2</mn></mrow></mfrac><msup><mrow><mo>‖</mo><mi>z</mi><mo>−</mo><mover><mi>y</mi><mo>^</mo></mover><mo>‖</mo></mrow><mrow><mn>2</mn></mrow></msup><mtext>   s.t.   </mtext><msup><mrow><mi>1</mi></mrow><mrow><mi>T</mi></mrow></msup><mi>z</mi><mo>=</mo><msub><mrow><mi>C</mi></mrow><mrow><mi>Af</mi></mrow></msub><mo>,</mo><mtext>  </mtext><mi>z</mi><mo>≥</mo><mn>0</mn></mrow></mtd></mtr></mtable></math>

For C_Af ≥ 0 the feasible set is a simplex. The solution is affine within a fixed active-set region; derivatives need care where a component reaches zero.

The required lab stops at linear equalities. Report results and gradient checks separately if implementing this inequality extension.

<!-- lecture-page -->

## 12. Derive the dynamic total-concentration transition

Adding dynamic species balances gives dS/dt = (C_Af − S)/τ. With constant C_Af and τ within an interval, the derivative of S − C_Af is −(S − C_Af)/τ, hence:

<math display="block"><mtable columnalign="left"><mtr><mtd><mrow><msub><mrow><mi>S</mi></mrow><mrow><mi>k</mi><mo>+</mo><mn>1</mn></mrow></msub><mo>=</mo><msub><mrow><mi>C</mi></mrow><mrow><mi>Af</mi></mrow></msub><mo>+</mo><mrow><mo>(</mo><msub><mrow><mi>S</mi></mrow><mrow><mi>k</mi></mrow></msub><mo>−</mo><msub><mrow><mi>C</mi></mrow><mrow><mi>Af</mi></mrow></msub><mo>)</mo></mrow><msup><mrow><mi>e</mi></mrow><mrow><mo>−</mo><mfrac><mrow><mi>Δt</mi></mrow><mrow><mi>τ</mi></mrow></mfrac></mrow></msup></mrow></mtd></mtr></mtable></math>

Exercise: use S_k = 1.0, C_Af = 1.2 mol/L, τ = 5 min, and Δt = 0.2 min. Compute the next total.

Answer check: 1.2 − 0.2 exp(−0.04) ≈ 1.007842 mol/L. Forcing the steady-state total immediately would change this transition. Project the raw next state onto this right side instead.

<!-- lecture-page -->

## 13. General-B implementation and gradient check

raw has shape (batch, n), rhs (batch, m), and B (m, n). B is fixed and must have independent rows.

```python
def linear_project(raw, rhs, B):
    residual = raw @ B.T - rhs
    lam = torch.linalg.solve(B @ B.T, residual.T).T
    return raw - lam @ B

# Use float64 and independent inputs for finite differences.
assert torch.autograd.gradcheck(
    lambda a, d: linear_project(a, d, B), (raw, rhs)
)
```

Create checked raw and rhs tensors with requires_grad=True. The lab’s --check-only checks feasibility, idempotence, Jacobians, scaling, and counterexamples.

<!-- lecture-page -->

## 14. Define the comparison metrics

Component-j RMSE is the square root of mean squared prediction error over test rows. Pooled RMSE averages over rows and components. Sum MAE and maximum use the absolute sum residual.

Count equality violations when the absolute sum residual exceeds 10⁻⁶ mol/L and negative entries when a predicted concentration is below −10⁻⁸ mol/L. Also report the minimum predicted concentration.

Species-balance RMS averages r_j² over all three species and test rows, then takes the square root; units are mol/(L·min). Do not select settings using test. Assess variation across seeds in a separate repeated experiment.

<!-- lecture-page -->

## 15. Exercises with short answer checks

1. How many output directions remain trainable for B = I₃? Answer: P = 0 fixes the output to d; there are no free directions.
2. How many remain for B = [1, 1, 1]? Answer: null-space dimension is 3 − 1 = 2.
3. What happens to a raw output whose sum is already 1.2? Answer: zero residual means no change.
4. Does zero test sum-violation count make the hard model fully physically feasible? Answer: inspect negative concentrations and species balances separately.
5. Does post-projection reduce every component error? Answer: no. Nonincrease applies to total squared error in the same metric with a feasible reference.

<!-- lecture-page -->

## 16. Primary-source reading guide

Chen, H., Constante Flores, G. E., & Li, C. (2024). *Physics-informed neural networks with hard linear equality constraints*. C&CE 189, 108764. [DOI](https://doi.org/10.1016/j.compchemeng.2024.108764) · [Manuscript](https://arxiv.org/abs/2402.07251) · [Author repository](https://github.com/li-group/KKThPINN). Compare Section 3’s fixed projection and assumptions; read one Section 4 process case.

Raissi, M., Perdikaris, P., & Karniadakis, G. E. (2019). *Physics-informed neural networks: A deep learning framework for solving forward and inverse problems involving nonlinear partial differential equations*. JCP 378, 686-707. [DOI](https://doi.org/10.1016/j.jcp.2018.10.045) · [2017 Part I](https://arxiv.org/abs/1711.10561). Read Part I’s continuous-time residual and coordinate differentiation.

<!-- lecture-page -->

## 17. Sources for mathematics and implementation

Boyd, S., & Vandenberghe, L. (2004). *Convex Optimization*. [Official book](https://web.stanford.edu/~boyd/cvxbook/). Use Section 5.5.3 on KKT conditions and Section 10.1 on equality-constrained minimization to rederive companion pages 3-4.

PyTorch: [torch.linalg.solve](https://docs.pytorch.org/docs/2.14/generated/torch.linalg.solve.html) solves a linear system without explicitly forming an inverse. [gradcheck](https://docs.pytorch.org/docs/2.9/generated/torch.autograd.gradcheck.gradcheck.html) compares automatic differentiation with finite differences; default tolerances assume double precision.

[Return to the lecture]({{ page.lecture_note | relative_url }}).

<!-- ko -->

## 1. 정상상태 수지에서 합 등식 유도하기

A → B → C의 1차 연속반응에서 정상상태는 r_A = r_B = r_C = 0입니다. A 수지를 먼저 풀고 그 결과를 B, C 순서로 대입하면:

<math display="block"><mtable columnalign="left"><mtr><mtd><mrow><msub><mrow><mi>C</mi></mrow><mrow><mi>A</mi></mrow></msub><mo>=</mo><mfrac><mrow><msub><mrow><mi>C</mi></mrow><mrow><mi>Af</mi></mrow></msub></mrow><mrow><mn>1</mn><mo>+</mo><msub><mrow><mi>k</mi></mrow><mrow><mn>1</mn></mrow></msub><mi>τ</mi></mrow></mfrac></mrow></mtd></mtr><mtr><mtd><mrow><msub><mrow><mi>C</mi></mrow><mrow><mi>B</mi></mrow></msub><mo>=</mo><mfrac><mrow><msub><mrow><mi>k</mi></mrow><mrow><mn>1</mn></mrow></msub><mi>τ</mi><msub><mrow><mi>C</mi></mrow><mrow><mi>A</mi></mrow></msub></mrow><mrow><mn>1</mn><mo>+</mo><msub><mrow><mi>k</mi></mrow><mrow><mn>2</mn></mrow></msub><mi>τ</mi></mrow></mfrac><mo>,</mo><mtext>  </mtext><msub><mrow><mi>C</mi></mrow><mrow><mi>C</mi></mrow></msub><mo>=</mo><msub><mrow><mi>k</mi></mrow><mrow><mn>2</mn></mrow></msub><mi>τ</mi><msub><mrow><mi>C</mi></mrow><mrow><mi>B</mi></mrow></msub></mrow></mtd></mtr></mtable></math>

B 수지에서 k₁τC_A = (1 + k₂τ)C_B이므로 C_B + C_C = k₁τC_A입니다. A 수지의 C_Af = (1 + k₁τ)C_A와 결합하면 세 농도의 합이 C_Af가 됩니다.

확인: 330 K, τ = 5 min, C_Af = 1.2 mol/L이면 [0.6, 0.4, 0.2]입니다.

<!-- lecture-page -->

## 2. Soft penalty의 정지점

J(z) = ½(z − a)² + ½λ(z − b)², λ ≥ 0에서 dJ/dz = (z − a) + λ(z − b)입니다. 2차 미분은 1 + λ > 0이므로 정지점이 유일한 최소점입니다.

<math display="block"><mtable columnalign="left"><mtr><mtd><mrow><msub><mrow><mi>z</mi></mrow><mrow><mo>∗</mo></mrow></msub><mo>=</mo><mfrac><mrow><mi>a</mi><mo>+</mo><mi>λ</mi><mi>b</mi></mrow><mrow><mn>1</mn><mo>+</mo><mi>λ</mi></mrow></mfrac></mrow></mtd></mtr><mtr><mtd><mrow><msub><mrow><mi>z</mi></mrow><mrow><mo>∗</mo></mrow></msub><mo>−</mo><mi>b</mi><mo>=</mo><mfrac><mrow><mi>a</mi><mo>−</mo><mi>b</mi></mrow><mrow><mn>1</mn><mo>+</mo><mi>λ</mi></mrow></mfrac></mrow></mtd></mtr></mtable></math>

연습: a = 1.4, b = 1.2에서 λ = 1, 9의 해와 residual을 구합니다.

답 확인: 해는 1.30, 1.22이고 residual은 0.10, 0.02입니다. 학습이 정확히 최소점에 도달해도 유한한 penalty가 등식을 정확히 맞추지 않는 예입니다.

<!-- lecture-page -->

## 3. Equality QP와 KKT 유도

B ∈ ℝᵐˣⁿ, rank(B) = m, d ∈ ℝᵐ로 둡니다. 입력과 raw 예측을 고정하고 다음 QP를 풉니다.

<math display="block"><mtable columnalign="left"><mtr><mtd><mrow><msub><mrow><mi>y</mi></mrow><mrow><mi>p</mi></mrow></msub><mo>=</mo><msub><mrow><mi>argmin</mi></mrow><mrow><mi>z</mi></mrow></msub><mtext>  </mtext><mfrac><mrow><mn>1</mn></mrow><mrow><mn>2</mn></mrow></mfrac><msup><mrow><mo>‖</mo><mi>z</mi><mo>−</mo><mover><mi>y</mi><mo>^</mo></mover><mo>‖</mo></mrow><mrow><mn>2</mn></mrow></msup><mtext>   subject to   </mtext><mi>B</mi><mi>z</mi><mo>=</mo><mi>d</mi><mrow><mo>(</mo><mi>x</mi><mo>)</mo></mrow></mrow></mtd></mtr></mtable></math>

<math display="block"><mtable columnalign="left"><mtr><mtd><mrow><mi>z</mi><mo>−</mo><mover><mi>y</mi><mo>^</mo></mover><mo>+</mo><msup><mrow><mi>B</mi></mrow><mrow><mi>T</mi></mrow></msup><mi>λ</mi><mo>=</mo><mn>0</mn><mo>,</mo><mtext>  </mtext><mi>B</mi><mi>z</mi><mo>=</mo><mi>d</mi></mrow></mtd></mtr></mtable></math>

첫 식에서 z = ŷ − Bᵀλ입니다. 두 번째 식에 대입하면 BBᵀλ = Bŷ − d입니다. BBᵀ가 가역이므로 λ가 유일하고, z도 유일하게 정해집니다. 등식은 convex 집합이며 목적함수의 Hessian은 I입니다.

<!-- lecture-page -->

## 4. 등식 보장과 projector의 성질

<math display="block"><mtable columnalign="left"><mtr><mtd><mrow><mi>G</mi><mo>=</mo><mi>B</mi><msup><mrow><mi>B</mi></mrow><mrow><mi>T</mi></mrow></msup><mo>,</mo><mtext>  </mtext><mi>G</mi><mi>λ</mi><mo>=</mo><mi>B</mi><mover><mi>y</mi><mo>^</mo></mover><mo>−</mo><mi>d</mi></mrow></mtd></mtr><mtr><mtd><mrow><msub><mrow><mi>y</mi></mrow><mrow><mi>p</mi></mrow></msub><mo>=</mo><mover><mi>y</mi><mo>^</mo></mover><mo>−</mo><msup><mrow><mi>B</mi></mrow><mrow><mi>T</mi></mrow></msup><msup><mrow><mi>G</mi></mrow><mrow><mo>−</mo><mn>1</mn></mrow></msup><mrow><mo>(</mo><mi>B</mi><mover><mi>y</mi><mo>^</mo></mover><mo>−</mo><mi>d</mi><mo>)</mo></mrow></mrow></mtd></mtr></mtable></math>

B를 곱하면 보정항이 정확히 원래 residual을 제거합니다.

<math display="block"><mtable columnalign="left"><mtr><mtd><mrow><mi>B</mi><msub><mrow><mi>y</mi></mrow><mrow><mi>p</mi></mrow></msub><mo>=</mo><mi>B</mi><mover><mi>y</mi><mo>^</mo></mover><mo>−</mo><mi>G</mi><msup><mrow><mi>G</mi></mrow><mrow><mo>−</mo><mn>1</mn></mrow></msup><mrow><mo>(</mo><mi>B</mi><mover><mi>y</mi><mo>^</mo></mover><mo>−</mo><mi>d</mi><mo>)</mo></mrow><mo>=</mo><mi>d</mi></mrow></mtd></mtr></mtable></math>

P = I − Bᵀ(BBᵀ)⁻¹B는 Pᵀ = P, P² = P, BP = 0을 만족합니다. P는 B의 null space로 투영합니다. 이미 가능한 ŷ는 보정량이 0이고, 한 번 투영한 값을 다시 투영해도 바뀌지 않습니다.

<!-- lecture-page -->

## 5. 손계산: 보정량과 오차 변화

<math display="block"><mtable columnalign="left"><mtr><mtd><mrow><mi>B</mi><mo>=</mo><mrow><mo>[</mo><mtable><mtr><mtd><mrow><mn>1</mn></mrow></mtd><mtd><mrow><mn>1</mn></mrow></mtd><mtd><mrow><mn>1</mn></mrow></mtd></mtr></mtable><mo>]</mo></mrow><mo>,</mo><mtext>  </mtext><mi>d</mi><mo>=</mo><mn>1.2</mn></mrow></mtd></mtr><mtr><mtd><mrow><msub><mrow><mi>y</mi></mrow><mrow><mi>p</mi></mrow></msub><mo>=</mo><mrow><mo>[</mo><mtable><mtr><mtd><mrow><mn>.70</mn></mrow></mtd></mtr><mtr><mtd><mrow><mn>.45</mn></mrow></mtd></mtr><mtr><mtd><mrow><mn>.25</mn></mrow></mtd></mtr></mtable><mo>]</mo></mrow><mo>−</mo><mfrac><mrow><mn>.20</mn></mrow><mrow><mn>3</mn></mrow></mfrac><mrow><mo>[</mo><mtable><mtr><mtd><mrow><mn>1</mn></mrow></mtd></mtr><mtr><mtd><mrow><mn>1</mn></mrow></mtd></mtr><mtr><mtd><mrow><mn>1</mn></mrow></mtd></mtr></mtable><mo>]</mo></mrow><mo>=</mo><mrow><mo>[</mo><mtable><mtr><mtd><mrow><mn>.633333</mn></mrow></mtd></mtr><mtr><mtd><mrow><mn>.383333</mn></mrow></mtd></mtr><mtr><mtd><mrow><mn>.183333</mn></mrow></mtd></mtr></mtable><mo>]</mo></mrow></mrow></mtd></mtr></mtable></math>

기준 [0.6, 0.4, 0.2]에 대한 raw 제곱오차 합은 0.015 (mol/L)²입니다. 보정량의 제곱 norm은 0.04/3, 투영 후 제곱오차 합은 1/600 ≈ 0.001667입니다.

성분별로는 A 오차가 +0.10에서 +0.033333으로 바뀝니다. B와 C는 +0.05에서 −0.016667로 바뀝니다. 전체 오차와 개별 오차를 각각 계산하는 연습입니다.

<!-- lecture-page -->

## 6. 파라미터와 입력에 대한 chain rule

J_f,θ는 raw 출력의 파라미터 Jacobian입니다. A·B·b가 고정이면:

<math display="block"><mtable columnalign="left"><mtr><mtd><mrow><msub><mrow><mi>∇</mi></mrow><mrow><mi>θ</mi></mrow></msub><mi>L</mi><mo>=</mo><msup><mrow><msub><mrow><mi>J</mi></mrow><mrow><mi>f</mi><mo>,</mo><mi>θ</mi></mrow></msub></mrow><mrow><mi>T</mi></mrow></msup><msup><mrow><mi>P</mi></mrow><mrow><mi>T</mi></mrow></msup><msub><mrow><mi>∇</mi></mrow><mrow><msub><mrow><mi>y</mi></mrow><mrow><mi>p</mi></mrow></msub></mrow></msub><mi>L</mi></mrow></mtd></mtr><mtr><mtd><mrow><mfrac><mrow><mi>∂</mi><msub><mrow><mi>y</mi></mrow><mrow><mi>p</mi></mrow></msub></mrow><mrow><mi>∂</mi><mi>x</mi></mrow></mfrac><mo>=</mo><mi>P</mi><mfrac><mrow><mi>∂</mi><msub><mrow><mi>f</mi></mrow><mrow><mi>θ</mi></mrow></msub></mrow><mrow><mi>∂</mi><mi>x</mi></mrow></mfrac><mo>−</mo><msup><mrow><mi>B</mi></mrow><mrow><mi>T</mi></mrow></msup><msup><mrow><mi>G</mi></mrow><mrow><mo>−</mo><mn>1</mn></mrow></msup><mi>A</mi></mrow></mtd></mtr></mtable></math>

입력 gradient에는 d(x) = b − Ax의 직접 경로도 포함됩니다. B가 입력에 따라 달라지면 P도 입력에 의존하므로 추가 미분항이 필요합니다. 고정 projector 식을 그대로 사용하면 안 됩니다.

확인: upstream [1, 0, 0]에 B = [1, 1, 1]을 사용하면 [2/3, −1/3, −1/3]이 전달됩니다.

<!-- lecture-page -->

## 7. 표준화 좌표의 등식과 거리

<math display="block"><mtable columnalign="left"><mtr><mtd><mrow><mi>y</mi><mo>=</mo><mi>μ</mi><mo>+</mo><mi>D</mi><mi>z</mi><mo>,</mo><mtext>  </mtext><mi>B</mi><mi>D</mi><mi>z</mi><mo>=</mo><mi>d</mi><mo>−</mo><mi>B</mi><mi>μ</mi></mrow></mtd></mtr><mtr><mtd><mrow><mi>D</mi><mo>=</mo><mi>diag</mi><mrow><mo>(</mo><msub><mrow><mi>s</mi></mrow><mrow><mn>1</mn></mrow></msub><mo>,</mo><mi>…</mi><mo>,</mo><msub><mrow><mi>s</mi></mrow><mrow><mi>n</mi></mrow></msub><mo>)</mo></mrow></mrow></mtd></mtr></mtable></math>

z 공간의 Euclidean 투영은 y 공간에서 ‖D⁻¹(y − ŷ)‖²를 최소화합니다. 물리 Euclidean 투영과는 metric이 다릅니다.

예: raw [0.70, 0.45, 0.25], 합 1.20, s = [0.2, 0.5, 0.1]이면 z 공간 투영을 복원한 결과는 [0.673333, 0.283333, 0.243333]입니다. 보정량은 s_j²에 비례합니다.

두 방법 모두 합을 맞춥니다. 서로 다른 단위의 출력을 함께 투영할 때에는 물리 Euclidean 거리 자체에도 단위 선택이 영향을 주므로 metric을 설계해야 합니다.

<!-- lecture-page -->

## 8. 중복 등식과 모순된 우변

<math display="block"><mtable columnalign="left"><mtr><mtd><mrow><mi>B</mi><mo>=</mo><mrow><mo>[</mo><mtable><mtr><mtd><mrow><mn>1</mn></mrow></mtd><mtd><mrow><mn>1</mn></mrow></mtd><mtd><mrow><mn>1</mn></mrow></mtd></mtr><mtr><mtd><mrow><mn>2</mn></mrow></mtd><mtd><mrow><mn>2</mn></mrow></mtd><mtd><mrow><mn>2</mn></mrow></mtd></mtr></mtable><mo>]</mo></mrow></mrow></mtd></mtr></mtable></math>

두 번째 행은 첫 행의 두 배라 rank는 1입니다. d = [1.2, 2.4]이면 두 등식은 같은 집합을 나타냅니다. 독립 행 하나만 사용해도 됩니다.

d = [1.2, 2.5]이면 첫 식의 두 배와 두 번째 식이 모순됩니다. 가능한 출력이 없습니다. Pseudoinverse는 least-squares 결과를 반환할 수 있지만 모든 residual을 0으로 만들지는 못합니다.

작은 singular value를 버릴 때에는 제거된 식의 residual도 원래 단위로 다시 확인합니다.

<!-- lecture-page -->

## 9. 단위가 다른 residual의 무차원화

농도 합 residual의 단위는 mol/L이고 성분수지 residual의 단위는 mol/(L·min)입니다. 두 제곱값을 scale 없이 더하면 λ의 의미가 단위 선택에 따라 달라집니다.

예를 들어 기준 농도 <math><msub><mrow><mi>c</mi></mrow><mrow><mo>∗</mo></mrow></msub></math>와 기준 시간 <math><msub><mrow><mi>t</mi></mrow><mrow><mo>∗</mo></mrow></msub></math>를 정해 합 residual은 <math><msub><mrow><mi>c</mi></mrow><mrow><mo>∗</mo></mrow></msub></math>로, 성분수지는 <math><msub><mrow><mi>c</mi></mrow><mrow><mo>∗</mo></mrow></msub></math>/<math><msub><mrow><mi>t</mi></mrow><mrow><mo>∗</mo></mrow></msub></math>로 나눕니다. 무차원화 후에도 loss 평균 방식과 λ는 명시해야 합니다.

실습은 합 penalty를 사용하며, 알려진 속도식을 성분수지 residual로 추가할 수 있습니다.

<!-- lecture-page -->

## 10. 정확도 보장의 조건과 잘못된 물리식

<math display="block"><mtable columnalign="left"><mtr><mtd><mrow><msup><mrow><mo>‖</mo><mover><mi>y</mi><mo>^</mo></mover><mo>−</mo><msup><mrow><mi>y</mi></mrow><mrow><mo>∗</mo></mrow></msup><mo>‖</mo></mrow><mrow><mn>2</mn></mrow></msup><mo>=</mo><msup><mrow><mo>‖</mo><mover><mi>y</mi><mo>^</mo></mover><mo>−</mo><msub><mrow><mi>y</mi></mrow><mrow><mi>p</mi></mrow></msub><mo>‖</mo></mrow><mrow><mn>2</mn></mrow></msup><mo>+</mo><msup><mrow><mo>‖</mo><msub><mrow><mi>y</mi></mrow><mrow><mi>p</mi></mrow></msub><mo>−</mo><msup><mrow><mi>y</mi></mrow><mrow><mo>∗</mo></mrow></msup><mo>‖</mo></mrow><mrow><mn>2</mn></mrow></msup></mrow></mtd></mtr></mtable></math>

이 분해는 <math><msup><mrow><mi>y</mi></mrow><mrow><mo>∗</mo></mrow></msup></math>가 같은 affine 집합에 있을 때 성립합니다. 보정 벡터는 집합의 normal 방향이고 y_p − <math><msup><mrow><mi>y</mi></mrow><mrow><mo>∗</mo></mrow></msup></math>는 tangent 방향이라 내적이 0입니다.

참 합이 1.2인데 잘못된 등식이 합 1.1을 강제하면 참 출력은 집합 밖입니다. 세 성분의 보정 때문에 참 출력과의 최소 거리부터 0.1/√3 ≈ 0.057735 mol/L가 됩니다.

센서 편향·누락 성분·반응 화학양론 오류를 먼저 확인합니다. 잘못 지정한 등식도 투영은 그대로 강제합니다.

<!-- lecture-page -->

## 11. 비음수성과 농도 합의 동시 제약

등식 투영 후 음수를 clamp하면 합이 달라집니다. 합과 비음수성을 함께 요구하는 문제는:

<math display="block"><mtable columnalign="left"><mtr><mtd><mrow><msub><mrow><mi>min</mi></mrow><mrow><mi>z</mi></mrow></msub><mtext>  </mtext><mfrac><mrow><mn>1</mn></mrow><mrow><mn>2</mn></mrow></mfrac><msup><mrow><mo>‖</mo><mi>z</mi><mo>−</mo><mover><mi>y</mi><mo>^</mo></mover><mo>‖</mo></mrow><mrow><mn>2</mn></mrow></msup><mtext>   s.t.   </mtext><msup><mrow><mi>1</mi></mrow><mrow><mi>T</mi></mrow></msup><mi>z</mi><mo>=</mo><msub><mrow><mi>C</mi></mrow><mrow><mi>Af</mi></mrow></msub><mo>,</mo><mtext>  </mtext><mi>z</mi><mo>≥</mo><mn>0</mn></mrow></mtd></mtr></mtable></math>

C_Af ≥ 0이면 가능한 simplex입니다. 활성집합이 고정된 구간에서는 affine 식으로 풀 수 있지만, 성분이 0이 되는 경계에서 미분을 주의해야 합니다.

필수 실습은 선형 등식 투영까지입니다. 이 부등식 확장을 적용했다면 결과와 gradient 확인을 별도로 보고합니다.

<!-- lecture-page -->

## 12. 동적 총 농도 전이의 유도

동적 성분수지를 합하면 dS/dt = (C_Af − S)/τ입니다. 구간 안에서 C_Af와 τ가 일정하면 S − C_Af의 미분은 −(S − C_Af)/τ이므로:

<math display="block"><mtable columnalign="left"><mtr><mtd><mrow><msub><mrow><mi>S</mi></mrow><mrow><mi>k</mi><mo>+</mo><mn>1</mn></mrow></msub><mo>=</mo><msub><mrow><mi>C</mi></mrow><mrow><mi>Af</mi></mrow></msub><mo>+</mo><mrow><mo>(</mo><msub><mrow><mi>S</mi></mrow><mrow><mi>k</mi></mrow></msub><mo>−</mo><msub><mrow><mi>C</mi></mrow><mrow><mi>Af</mi></mrow></msub><mo>)</mo></mrow><msup><mrow><mi>e</mi></mrow><mrow><mo>−</mo><mfrac><mrow><mi>Δt</mi></mrow><mrow><mi>τ</mi></mrow></mfrac></mrow></msup></mrow></mtd></mtr></mtable></math>

연습: S_k = 1.0, C_Af = 1.2 mol/L, τ = 5 min, Δt = 0.2 min의 다음 합을 구합니다.

답 확인: 1.2 − 0.2 exp(−0.04) ≈ 1.007842 mol/L입니다. 정상상태 합을 즉시 강제하면 이 전이를 바꿔버립니다. Raw 다음 상태의 합을 이 우변으로 투영할 수 있습니다.

<!-- lecture-page -->

## 13. 일반 B의 구현과 gradient 확인

raw는 (batch, n), rhs는 (batch, m), B는 (m, n)입니다. B는 고정이며 행이 독립이어야 합니다.

```python
def linear_project(raw, rhs, B):
    residual = raw @ B.T - rhs
    lam = torch.linalg.solve(B @ B.T, residual.T).T
    return raw - lam @ B

# Use float64 and independent inputs for finite differences.
assert torch.autograd.gradcheck(
    lambda a, d: linear_project(a, d, B), (raw, rhs)
)
```

검사할 raw와 rhs는 requires_grad=True로 만듭니다. 실습의 --check-only가 가능성·멱등성·Jacobian·표준화·반례까지 확인합니다.

<!-- lecture-page -->

## 14. 공정 비교 보고서의 계산 정의

성분 j의 RMSE는 test 행에서 (예측 − 기준)²의 평균에 제곱근을 취합니다. 전체 RMSE는 행과 성분을 모두 평균합니다. 합 MAE와 최대값은 합 residual의 절댓값에서 계산합니다.

합 residual의 절댓값이 10⁻⁶ mol/L보다 크면 위반으로, 예측 농도가 −10⁻⁸ mol/L보다 작으면 음수 항목으로 셉니다. 최소 예측 농도도 함께 보고합니다.

성분수지 RMS는 세 성분과 test 행 전체의 r_j²를 평균한 제곱근입니다. 단위는 mol/(L·min)입니다. Test는 설정 선택에 사용하지 않고, 여러 seed의 분포는 별도 반복 실험으로 확인합니다.

<!-- lecture-page -->

## 15. 연습문제와 짧은 답 확인

1. B = I₃이면 학습할 수 있는 출력 방향이 몇 개일까요? 답: P = 0이므로 지정한 d로 출력이 고정되고 자유 방향은 0개입니다.
2. B = [1, 1, 1]이면 자유 방향은 몇 개일까요? 답: null space 차원은 3 − 1 = 2입니다.
3. 이미 합이 1.2인 raw 출력은 어떻게 바뀔까요? 답: residual이 0이므로 바뀌지 않습니다.
4. Hard 모델이 test에서 합 위반 0개이면 물리적으로 모두 가능한가요? 답: 음수 농도와 성분수지 위반을 따로 검사해야 합니다.
5. 후처리 투영이 모든 성분의 오차를 줄이나요? 답: 아닙니다. 가능한 기준값에 대한 동일 metric의 전체 제곱오차에만 비증가 성질이 있습니다.

<!-- lecture-page -->

## 16. 원문 읽기와 출처

Chen, H., Constante Flores, G. E., & Li, C. (2024). *Physics-informed neural networks with hard linear equality constraints*. C&CE 189, 108764. [DOI](https://doi.org/10.1016/j.compchemeng.2024.108764) · [공개 원고](https://arxiv.org/abs/2402.07251) · [저자 저장소](https://github.com/li-group/KKThPINN). 3절의 고정 투영층과 가정을 대조하고 4절의 공정 사례 중 하나를 읽습니다.

Raissi, M., Perdikaris, P., & Karniadakis, G. E. (2019). *Physics-informed neural networks: A deep learning framework for solving forward and inverse problems involving nonlinear partial differential equations*. JCP 378, 686-707. [DOI](https://doi.org/10.1016/j.jcp.2018.10.045) · [2017 Part I](https://arxiv.org/abs/1711.10561). 공개 Part I의 연속시간 residual과 좌표 자동미분을 읽습니다.

<!-- lecture-page -->

## 17. 수학과 구현을 확인할 원문

Boyd, S., & Vandenberghe, L. (2004). *Convex Optimization*. [공식 교재](https://web.stanford.edu/~boyd/cvxbook/). 5.5.3절의 KKT 조건과 10.1절의 등식 제약 최소화를 사용해 읽기자료 3-4쪽을 다시 유도합니다.

PyTorch: [torch.linalg.solve](https://docs.pytorch.org/docs/2.14/generated/torch.linalg.solve.html)는 역행렬을 명시적으로 만들지 않고 선형계를 풉니다. [gradcheck](https://docs.pytorch.org/docs/2.9/generated/torch.autograd.gradcheck.gradcheck.html)는 자동미분과 유한차분을 대조하며 기본 tolerance는 double precision을 전제로 합니다.

[강의노트로 돌아가기]({{ page.lecture_note | relative_url }}).
