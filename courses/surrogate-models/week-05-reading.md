---
layout: "course-note"
title: "Week 5 Reading: ReLU Graphs and MILP Derivations"
title_ko: "5주차 읽기자료: ReLU 그래프와 MILP 유도"
description: "Frozen ReLU models, valid bounds, and verified optimization formulations."
description_ko: "고정 ReLU 모델, 유효한 bounds와 최적화 정식화를 다룹니다."
material_label: "Week 5 reading"
material_label_ko: "5주차 읽기자료"
updated: "2026-10-25"
permalink: "/courses/surrogate-models/week-05-reading/"
pdf_en: "/assets/courses/surrogate-models/week-05-reading-en.pdf"
pdf_ko: "/assets/courses/surrogate-models/week-05-reading-ko.pdf"
course_id: "surrogate-models"
notebook: "/assets/courses/surrogate-models/week-05/week05_lab.ipynb"
lab_script: "/assets/courses/surrogate-models/week-05/week05_lab.py"
lecture_note: "/courses/surrogate-models/week-05/"
---

## Optimization formulation for reactor design

At a fixed flow of 1 L/min, find the minimum volume satisfying the product specifications. Since V = Qτ, residence time τ expresses the design choice.

The fixed context is 330 K and an A feed concentration of 1.2 mol/L. Outputs are A, B, and C concentrations; require B ≥ 0.40 and C ≤ 0.25 mol/L.

We first define the process problem, translate the predictor into constraints, and then verify the computed solution.

<!-- lecture-page -->

## Feasible set of the CSTR design problem

<math display="block"><mtable columnalign="left"><mtr><mtd><mrow><msub><mrow><mi>min</mi></mrow><mrow><mi>τ</mi><mo>,</mo><mi>y</mi></mrow></msub><mtext>  </mtext><mi>V</mi><mo>=</mo><mi>Q</mi><mi>τ</mi></mrow></mtd></mtr><mtr><mtd><mrow><mn>2</mn><mo>≤</mo><mi>τ</mi><mo>≤</mo><mn>10</mn><mo>,</mo><mtext>  </mtext><mi>y</mi><mo>=</mo><msub><mrow><mi>f</mi></mrow><mrow><mi>θ</mi></mrow></msub><mrow><mo>(</mo><mi>τ</mi><mo>)</mo></mrow></mrow></mtd></mtr><mtr><mtd><mrow><msub><mrow><mi>y</mi></mrow><mrow><mi>B</mi></mrow></msub><mo>≥</mo><mn>.40</mn><mo>,</mo><mtext>  </mtext><msub><mrow><mi>y</mi></mrow><mrow><mi>C</mi></mrow></msub><mo>≤</mo><mn>.25</mn><mo>,</mo><mtext>  </mtext><mi>y</mi><mo>≥</mo><mn>0</mn></mrow></mtd></mtr></mtable></math>

The τ range defines both the model domain and the starting point for bound calculation. Concentration inequalities encode product requirements, while y = fθ(τ) encodes the predictor.

The objective V is in L; y is in mol/L. τ and V have the same numerical value only because Q = 1 L/min.

<!-- lecture-page -->

## Interpolation data and model construction

| τ [min] | A [mol/L] | B [mol/L] | C [mol/L] |
| --- | --- | --- | --- |
| 2 | 0.857143 | 0.285714 | 0.057143 |
| 4 | 0.666667 | 0.380952 | 0.152381 |
| 6 | 0.545455 | 0.409091 | 0.245455 |
| 8 | 0.461538 | 0.410256 | 0.328205 |
| 10 | 0.400000 | 0.400000 | 0.400000 |

Interpolate linearly between adjacent rows. Each segment is a convex combination of its endpoint concentrations, preserving nonnegativity and the total 1.2 within the domain.

The table displays six decimals; computations use full-precision coefficients.

<!-- lecture-page -->

## Derivation of a ReLU representation of linear interpolation

Let cᵢ be the concentration vector at knot i and compute each segment slope sᵢ. Start with the first slope and add its change at each breakpoint.

<math display="block"><mtable columnalign="left"><mtr><mtd><mrow><msub><mrow><mi>s</mi></mrow><mrow><mi>i</mi></mrow></msub><mo>=</mo><mfrac><mrow><msub><mrow><mi>c</mi></mrow><mrow><mi>i</mi><mo>+</mo><mn>1</mn></mrow></msub><mo>−</mo><msub><mrow><mi>c</mi></mrow><mrow><mi>i</mi></mrow></msub></mrow><mrow><msub><mrow><mi>τ</mi></mrow><mrow><mi>i</mi><mo>+</mo><mn>1</mn></mrow></msub><mo>−</mo><msub><mrow><mi>τ</mi></mrow><mrow><mi>i</mi></mrow></msub></mrow></mfrac></mrow></mtd></mtr><mtr><mtd><mrow><mi>y</mi><mrow><mo>(</mo><mi>τ</mi><mo>)</mo></mrow><mo>=</mo><msub><mrow><mi>c</mi></mrow><mrow><mn>0</mn></mrow></msub><mo>+</mo><msub><mrow><mi>s</mi></mrow><mrow><mn>0</mn></mrow></msub><mrow><mo>(</mo><mi>τ</mi><mo>−</mo><msub><mrow><mi>τ</mi></mrow><mrow><mn>0</mn></mrow></msub><mo>)</mo></mrow></mrow></mtd></mtr><mtr><mtd><mrow><mtext>          </mtext><mo>+</mo><munderover><mo>∑</mo><mrow><mi>i</mi><mo>=</mo><mn>1</mn></mrow><mn>3</mn></munderover><mrow><mo>(</mo><msub><mrow><mi>s</mi></mrow><mrow><mi>i</mi></mrow></msub><mo>−</mo><msub><mrow><mi>s</mi></mrow><mrow><mi>i</mi><mo>−</mo><mn>1</mn></mrow></msub><mo>)</mo></mrow><mi>max</mi><mrow><mo>(</mo><mn>0</mn><mo>,</mo><mi>τ</mi><mo>−</mo><msub><mrow><mi>τ</mi></mrow><mrow><mi>i</mi></mrow></msub><mo>)</mo></mrow></mrow></mtd></mtr></mtable></math>

Within segment i, active hinge slopes telescope to s₀ + (s₁ − s₀) + ··· + (sᵢ − sᵢ₋₁) = sᵢ. Continuity at the knots and the correct initial value identify the desired interpolant.

<!-- lecture-page -->

## All weights after input scaling

Use x = (τ − 2)/8, hⱼ = max(0, x − tⱼ), and t = [0, 0.25, 0.50, 0.75]. In y = b + Wᵀh, rows of W index neurons and columns index components.

| j | WⱼA | WⱼB | WⱼC |
| --- | --- | --- | --- |
| 0 | -0.761904762 | 0.380952381 | 0.380952381 |
| 1 | 0.277056277 | -0.268398268 | -0.008658009 |
| 2 | 0.149184149 | -0.107892108 | -0.041292041 |
| 3 | 0.089510490 | -0.045687646 | -0.043822844 |

b = [0.857142857, 0.285714286, 0.057142857] mol/L. W is also in mol/L, while h is dimensionless.

Full-precision coefficients are stored in `frozen_network.json`. Reconstructing them from the rounded table can introduce small output differences.

<!-- lecture-page -->

## From interpolation slopes to ReLU weights

The first three B knot values at τ=2,4,6 are 0.285714286,0.380952381,0.409090909. Since x=(τ−2)/8, adjacent knots are 2/8=0.25 apart in x.

| Calculation | Result |
| --- | --- |
| First slope in x | (0.380952381−0.285714286)/0.25=0.380952381 |
| Second slope in x | (0.409090909−0.380952381)/0.25=0.112554113 |
| First ReLU weight W₀B | first slope: 0.380952381 |
| Weight W₁B at knot 0.25 | new minus previous slope: −0.268398268 |

For 0.25<x<0.5, only the first two ReLUs have derivative 1, so the total slope is 0.380952381 − 0.268398268 = 0.112554113. The new hinge is zero at its knot, preserving continuity.

Slopes computed with respect to τ must be multiplied by 8 to obtain weights for x: the same concentration change occurs over an x interval eight times shorter. Construct the A and C columns in the same way.

<!-- lecture-page -->

## Hidden values and B concentration at τ=5 min

Subtract thresholds [0,0.25,0.50,0.75] from x=(5−2)/8=0.375.

| j | aⱼ=x−tⱼ | hⱼ | Contribution WⱼB·hⱼ |
| --- | --- | --- | --- |
| 0 | 0.375 | 0.375 | 0.380952381×0.375=0.142857143 |
| 1 | 0.125 | 0.125 | −0.268398268×0.125=−0.033549784 |
| 2 | −0.125 | 0 | 0 |
| 3 | −0.375 | 0 | 0 |

Adding bias 0.285714286 gives B≈0.395021645 mol/L. Taking the midpoint of the 4-min and 6-min values also gives (0.380952381+0.409090909)/2=0.395021645.

The ReLU sum and segment interpolation express the same calculation. They differ from reference-process B=0.4 at 5 min, so this prediction falls slightly below the B≥0.40 specification.

<!-- lecture-page -->

## Both directions of Big-M equivalence

<math display="block"><mtable columnalign="left"><mtr><mtd><mrow><mi>h</mi><mo>≥</mo><mn>0</mn><mo>,</mo><mtext>  </mtext><mi>h</mi><mo>≥</mo><mi>a</mi></mrow></mtd></mtr><mtr><mtd><mrow><mi>h</mi><mo>≤</mo><mi>a</mi><mo>−</mo><mi>L</mi><mrow><mo>(</mo><mn>1</mn><mo>−</mo><mi>z</mi><mo>)</mo></mrow></mrow></mtd></mtr><mtr><mtd><mrow><mi>h</mi><mo>≤</mo><mi>U</mi><mi>z</mi><mo>,</mo><mtext>  </mtext><mi>z</mi><mo>∈</mo><mo>{</mo><mn>0</mn><mo>,</mo><mn>1</mn><mo>}</mo></mrow></mtd></mtr></mtable></math>

A feasible formulation point with z = 0 has h = 0 and a ≤ 0; with z = 1 it has h = a ≥ 0. Either branch gives h = max(0, a).

Conversely, choose any point on the ReLU graph. Set z = 0 if a ≤ 0 and z = 1 if a ≥ 0; all four inequalities hold. Valid bounds L ≤ a ≤ U are needed in this direction too.

<!-- lecture-page -->

## Substituting numbers into one ReLU formulation

For a=2x−1 and x∈[0,1], L=−1,U=1. The inequalities are h≥0, h≥a, h≤a+1−z, and h≤z.

| Input and branch | Lower bound | Upper bound | Output |
| --- | --- | --- | --- |
| x=0.2, a=−0.6, z=0 | h≥0 | h≤0; h≤0.4 | h=0 |
| x=0.8, a=0.6, z=1 | h≥0.6 | h≤0.6; h≤1 | h=0.6 |
| Wrong z=0 at x=0.8 | h≥0.6 | h≤0 | Impossible |

```python
a = 2 * x - 1
h = max(0., a)
z = int(a >= 0.)
assert h >= 0 and h >= a
assert h <= a + 1 - z and h <= z
```

The binary selects a branch compatible with a; it does not create an arbitrary output. At a=0, either z is possible but both give h=0.

<!-- lecture-page -->

## Equivalence of multilayer ReLU formulations

Fix input x. The first affine layer uniquely determines a¹, and its ReLU constraints determine h¹ exactly.

Once h¹ is fixed, the next affine layer determines a². Repeating this argument through the final layer shows that the MILP output equals the forward output.

Conversely, insert all forward intermediate values and choose each z from its neuron’s sign to obtain an MILP-feasible point. Bounds must be valid at every layer; nonunique z values at zero do not change the output.

<!-- lecture-page -->

## Layerwise propagation of interval bounds

<math display="block"><mtable columnalign="left"><mtr><mtd><mrow><mi>a</mi><mo>=</mo><msub><mrow><mo>∑</mo></mrow><mrow><mi>i</mi></mrow></msub><msub><mrow><mi>w</mi></mrow><mrow><mi>i</mi></mrow></msub><msub><mrow><mi>h</mi></mrow><mrow><mi>i</mi></mrow></msub><mo>+</mo><mi>b</mi></mrow></mtd></mtr><mtr><mtd><mrow><mi>L</mi><mo>=</mo><mi>b</mi><mo>+</mo><msub><mrow><mo>∑</mo></mrow><mrow><mi>i</mi></mrow></msub><mi>min</mi><mrow><mo>(</mo><msub><mrow><mi>w</mi></mrow><mrow><mi>i</mi></mrow></msub><msub><mrow><mi>l</mi></mrow><mrow><mi>i</mi></mrow></msub><mo>,</mo><msub><mrow><mi>w</mi></mrow><mrow><mi>i</mi></mrow></msub><msub><mrow><mi>u</mi></mrow><mrow><mi>i</mi></mrow></msub><mo>)</mo></mrow></mrow></mtd></mtr><mtr><mtd><mrow><mi>U</mi><mo>=</mo><mi>b</mi><mo>+</mo><msub><mrow><mo>∑</mo></mrow><mrow><mi>i</mi></mrow></msub><mi>max</mi><mrow><mo>(</mo><msub><mrow><mi>w</mi></mrow><mrow><mi>i</mi></mrow></msub><msub><mrow><mi>l</mi></mrow><mrow><mi>i</mi></mrow></msub><mo>,</mo><msub><mrow><mi>w</mi></mrow><mrow><mi>i</mi></mrow></msub><msub><mrow><mi>u</mi></mrow><mrow><mi>i</mi></mrow></msub><mo>)</mo></mrow></mrow></mtd></mtr></mtable></math>

After ReLU, the interval is [max(0, L), max(0, U)]. Pass it to the next affine layer as its input bounds.

For example, if h₁ = x and h₂ = x, then h₁ − h₂ is always zero. Using only the separate intervals [0, 1] gives [−1, 1]. This remains valid but loses their correlation.

<!-- lecture-page -->

## Variable ordering in the objective and constraint matrix

The variable order is [x, h₀, h₁, h₂, h₃, y_A, y_B, y_C, z₁, z₂, z₃]. Each matrix row is stored as row_lower ≤ Av ≤ row_upper.

For V = 2 + 8x, the constant 2 does not change the optimizer, so the solver minimizes 8x. Add 2 back when reporting V and its dual bound.

An integer variable becomes binary only when its bounds are [0, 1]. If pre-activations are explicit variables, assign lower bounds that permit negative values.

<!-- lecture-page -->

## Storing one constraint as a solver row

Use variable order [x,h₀,h₁,h₂,h₃,y_A,y_B,y_C,z₁,z₂,z₃]. Only three columns are nonzero for h₁−x+0.25z₁≤0.

```python
import numpy as np
row = [-1, 0, 1, 0, 0, 0, 0, 0, 0.25, 0, 0]
row_lower = -np.inf
row_upper = 0.0
```

| Substitution | Row dot product | Check |
| --- | --- | --- |
| x=0.5,h₁=0.25,z₁=1 | −0.5+0.25+0.25=0 | satisfies upper bound 0 |
| x=0.5,h₁=0.30,z₁=1 | −0.5+0.30+0.25=0.05 | violates upper bound |

For output equality y_B−∑WⱼB hⱼ=b_B, set both row bounds to b_B. Mark the z₁ column as integer and also give it bounds [0,1]. A coefficient row alone does not make a variable binary.

[SciPy LinearConstraint](https://docs.scipy.org/doc/scipy/reference/generated/scipy.optimize.LinearConstraint.html) interprets each row as `lb <= A @ v <= ub`. Check variable order and coefficient signs against the same equation.

<!-- lecture-page -->

## Compute the optimal residence time by hand

B stays below 0.40 throughout 2-4 min. It increases over 4-6 min, so compute the first point reaching 0.40.

<math display="block"><mtable columnalign="left"><mtr><mtd><mrow><mi>τ</mi><mo>=</mo><mn>4</mn><mo>+</mo><mn>2</mn><mfrac><mrow><mn>.40</mn><mo>−</mo><mn>.380952380952</mn></mrow><mrow><mn>.409090909091</mn><mo>−</mo><mn>.380952380952</mn></mrow></mfrac></mrow></mtd></mtr><mtr><mtd><mrow><mi>τ</mi><mo>≈</mo><mn>5.353846</mn><mtext> min</mtext></mrow></mtd></mtr></mtable></math>

The same interpolation fraction gives [A, B, C] = [0.584615, 0.400000, 0.215385] mol/L. This satisfies C ≤ 0.25 and nonnegativity, so it is the minimum feasible residence time.

<!-- lecture-page -->

## Interpolation fraction at the product lower bound

Across 4–6 min, B increases from 0.380952381 to 0.409090909. Divide the required increase by the full segment increase.

| Calculation | Value |
| --- | --- |
| Required B increase | 0.40−0.380952381=0.019047619 |
| Full segment increase | 0.409090909−0.380952381=0.028138528 |
| Segment fraction α | 0.019047619/0.028138528≈0.676923077 |
| Residence time | 4+2α≈5.353846154 min |
| C at the same α | 0.152380952+α(0.245454545−0.152380952)≈0.215384615 |

B is below 0.40 on all earlier segments. At this first crossing, C≤0.25 and nonnegativity also hold, giving the minimum volume. Comparing interpolated B with C at a different τ would not check specifications for the same design.

<!-- lecture-page -->

## The continuous relaxation of a scalar ReLU

For L < 0 < U, relax z to [0, 1] and eliminate it to obtain a triangle.

<math display="block"><mtable columnalign="left"><mtr><mtd><mrow><mi>h</mi><mo>≥</mo><mn>0</mn><mo>,</mo><mtext>  </mtext><mi>h</mi><mo>≥</mo><mi>a</mi></mrow></mtd></mtr><mtr><mtd><mrow><mi>h</mi><mo>≤</mo><mfrac><mrow><mi>U</mi></mrow><mrow><mi>U</mi><mo>−</mo><mi>L</mi></mrow></mfrac><mrow><mo>(</mo><mi>a</mi><mo>−</mo><mi>L</mi><mo>)</mo></mrow></mrow></mtd></mtr></mtable></math>

The upper inequalities give h/U ≤ z ≤ (h − a + L)/L. Combining them, taking care with the negative sign of L, yields the last inequality.

This is the convex hull of the scalar (a, h) graph. When a is an affine function of several inputs, it need not be the strongest relaxation in the original input space.

<!-- lecture-page -->

## MILP representation of affine equality projection

<math display="block"><mtable columnalign="left"><mtr><mtd><mrow><mi>y</mi><mo>=</mo><mi>P</mi><msub><mrow><mi>y</mi></mrow><mrow><mi>raw</mi></mrow></msub><mo>+</mo><mi>R</mi><mi>u</mi><mo>+</mo><mi>q</mi></mrow></mtd></mtr></mtable></math>

If the Week 4 projection has this affine form with fixed P, R, and q, append it directly as output equalities. No additional binaries are required.

If the constraint matrices depend on the decisions, inverses or products of variables may appear, so the same conclusion does not automatically apply.

When adding a separate conservation equality, check compatibility with existing outputs. A new equality imposed on an approximate predictor can shrink or empty its feasible set.

<!-- lecture-page -->

## Exercise 1: signs and branches

For a = 2x − 1 and x ∈ [0, 1], find L and U and write the Big-M inequalities. Calculate (a, h, z) at x = 0.2 and 0.8.

Check: L = −1, U = 1, with h ≥ 0, h ≥ 2x − 1, h ≤ 2x − z, and h ≤ z.

At x = 0.2 the tuple is (−0.6, 0, 0); at x = 0.8 it is (0.6, 0.6, 1). At x = 0.5, h = 0 and either binary value is possible.

<!-- lecture-page -->

## Exercise 2: product specifications and feasibility

Does feasibility remain if B ≥ 0.41 replaces B ≥ 0.40 while C ≤ 0.25 stays unchanged? Use the knot table and segmentwise interpolation.

Check: C is 0.245455 at 6 min and 0.328205 at 8 min. The C bound limits residence time to about 6.109859 min.

B there is about 0.409155 mol/L, and its values in earlier segments are smaller. The modified surrogate problem is therefore infeasible. This calculation helps distinguish an infeasible solver result from an implementation error.

<!-- lecture-page -->

## Exercise 3: inputs for formulation verification

Random checks can miss errors at breakpoints or domain endpoints. Include τ = 2, 4, 6, 8, 10 and points on both sides of interior knots.

At each fixed input, measure the maximum absolute difference in h and y. At a = 0, require output agreement rather than identical binary values.

Check: the supplied run had a maximum difference of about 1.25 × 10⁻⁸ across 41 inputs. Solver tolerances can leave small differences very close to a breakpoint. Distinguish mathematical equivalence of a valid formulation from finite-precision computation.

<!-- lecture-page -->

## Lab files and sources

`week05_lab.py` includes coefficient construction, MILP matrix assembly, fixed-input checks, and independent segment calculations. Use `frozen_network.json` and `fit_knots.csv` to inspect the model; use `results.json` and `milp_matrix.csv` to inspect the solve.

[Boyd & Vandenberghe, Convex Optimization](https://stanford.edu/~boyd/cvxbook/), §4.1: variables, objectives, and feasible sets.

[Anderson et al., Strong mixed-integer programming formulations for trained neural networks](https://arxiv.org/abs/1811.08359), §2.1: the ReLU Big-M formulation.

[SciPy milp documentation](https://docs.scipy.org/doc/scipy/reference/generated/scipy.optimize.milp.html): bounds, integrality, LinearConstraint, and return status.

[Lecture](/courses/surrogate-models/week-05/) · [Lab bundle](/assets/courses/surrogate-models/week-05/week05-lab.zip)

<!-- ko -->

## 반응기 설계의 최적화 정식화

유량이 1 L/min으로 정해졌을 때 제품 규격을 만족하는 최소 부피를 찾습니다. 체류시간과 부피가 V = Qτ로 연결되므로 τ 하나로 설계 선택을 표현합니다.

고정 조건은 330 K와 유입 A 농도 1.2 mol/L입니다. 모델 출력은 A·B·C의 농도이며 B ≥ 0.40, C ≤ 0.25 mol/L를 요구합니다.

먼저 공정 문제를 적고, 예측 계산을 제약식으로 바꾼 뒤, 계산된 해를 검증하는 순서로 풀어봅니다.

<!-- lecture-page -->

## CSTR 설계 문제의 가능집합

<math display="block"><mtable columnalign="left"><mtr><mtd><mrow><msub><mrow><mi>min</mi></mrow><mrow><mi>τ</mi><mo>,</mo><mi>y</mi></mrow></msub><mtext>  </mtext><mi>V</mi><mo>=</mo><mi>Q</mi><mi>τ</mi></mrow></mtd></mtr><mtr><mtd><mrow><mn>2</mn><mo>≤</mo><mi>τ</mi><mo>≤</mo><mn>10</mn><mo>,</mo><mtext>  </mtext><mi>y</mi><mo>=</mo><msub><mrow><mi>f</mi></mrow><mrow><mi>θ</mi></mrow></msub><mrow><mo>(</mo><mi>τ</mi><mo>)</mo></mrow></mrow></mtd></mtr><mtr><mtd><mrow><msub><mrow><mi>y</mi></mrow><mrow><mi>B</mi></mrow></msub><mo>≥</mo><mn>.40</mn><mo>,</mo><mtext>  </mtext><msub><mrow><mi>y</mi></mrow><mrow><mi>C</mi></mrow></msub><mo>≤</mo><mn>.25</mn><mo>,</mo><mtext>  </mtext><mi>y</mi><mo>≥</mo><mn>0</mn></mrow></mtd></mtr></mtable></math>

τ의 범위는 모델을 사용할 영역이자 bounds 계산의 출발점입니다. 농도 부등식은 제품 요구사항을, y = fθ(τ)는 예측 모델의 계산을 나타냅니다.

목적함수의 V는 L 단위이고 제약의 y는 mol/L 단위입니다. τ와 V의 수치가 같은 이유는 Q = 1 L/min이기 때문입니다.

<!-- lecture-page -->

## 보간 자료와 모델 구성

| τ [min] | A [mol/L] | B [mol/L] | C [mol/L] |
| --- | --- | --- | --- |
| 2 | 0.857143 | 0.285714 | 0.057143 |
| 4 | 0.666667 | 0.380952 | 0.152381 |
| 6 | 0.545455 | 0.409091 | 0.245455 |
| 8 | 0.461538 | 0.410256 | 0.328205 |
| 10 | 0.400000 | 0.400000 | 0.400000 |

인접한 두 행 사이를 선형 보간합니다. 구간 안에서는 양 끝 농도의 convex combination이므로 비음수성과 농도 합 1.2가 유지됩니다.

표는 소수 여섯 자리로 표시했으며, 계산에는 원래 정밀도의 계수를 사용합니다.

<!-- lecture-page -->

## 선형 보간의 ReLU 표현 유도

각 knot의 농도 벡터를 cᵢ라고 두고 구간 기울기 sᵢ를 계산합니다. 첫 구간 기울기에서 출발해, knot를 지날 때 기울기 차이를 더합니다.

<math display="block"><mtable columnalign="left"><mtr><mtd><mrow><msub><mrow><mi>s</mi></mrow><mrow><mi>i</mi></mrow></msub><mo>=</mo><mfrac><mrow><msub><mrow><mi>c</mi></mrow><mrow><mi>i</mi><mo>+</mo><mn>1</mn></mrow></msub><mo>−</mo><msub><mrow><mi>c</mi></mrow><mrow><mi>i</mi></mrow></msub></mrow><mrow><msub><mrow><mi>τ</mi></mrow><mrow><mi>i</mi><mo>+</mo><mn>1</mn></mrow></msub><mo>−</mo><msub><mrow><mi>τ</mi></mrow><mrow><mi>i</mi></mrow></msub></mrow></mfrac></mrow></mtd></mtr><mtr><mtd><mrow><mi>y</mi><mrow><mo>(</mo><mi>τ</mi><mo>)</mo></mrow><mo>=</mo><msub><mrow><mi>c</mi></mrow><mrow><mn>0</mn></mrow></msub><mo>+</mo><msub><mrow><mi>s</mi></mrow><mrow><mn>0</mn></mrow></msub><mrow><mo>(</mo><mi>τ</mi><mo>−</mo><msub><mrow><mi>τ</mi></mrow><mrow><mn>0</mn></mrow></msub><mo>)</mo></mrow></mrow></mtd></mtr><mtr><mtd><mrow><mtext>          </mtext><mo>+</mo><munderover><mo>∑</mo><mrow><mi>i</mi><mo>=</mo><mn>1</mn></mrow><mn>3</mn></munderover><mrow><mo>(</mo><msub><mrow><mi>s</mi></mrow><mrow><mi>i</mi></mrow></msub><mo>−</mo><msub><mrow><mi>s</mi></mrow><mrow><mi>i</mi><mo>−</mo><mn>1</mn></mrow></msub><mo>)</mo></mrow><mi>max</mi><mrow><mo>(</mo><mn>0</mn><mo>,</mo><mi>τ</mi><mo>−</mo><msub><mrow><mi>τ</mi></mrow><mrow><mi>i</mi></mrow></msub><mo>)</mo></mrow></mrow></mtd></mtr></mtable></math>

구간 i 안에서 활성 hinge의 기울기를 합하면 s₀ + (s₁ − s₀) + ··· + (sᵢ − sᵢ₋₁) = sᵢ가 됩니다. knot에서 연속이고 첫 값을 맞추므로 원하는 보간식입니다.

<!-- lecture-page -->

## Scaling을 반영한 전체 가중치

x = (τ − 2)/8, hⱼ = max(0, x − tⱼ), t = [0, 0.25, 0.50, 0.75]입니다. y = b + Wᵀh에서 W의 행은 뉴런, 열은 성분입니다.

| j | WⱼA | WⱼB | WⱼC |
| --- | --- | --- | --- |
| 0 | -0.761904762 | 0.380952381 | 0.380952381 |
| 1 | 0.277056277 | -0.268398268 | -0.008658009 |
| 2 | 0.149184149 | -0.107892108 | -0.041292041 |
| 3 | 0.089510490 | -0.045687646 | -0.043822844 |

b = [0.857142857, 0.285714286, 0.057142857] mol/L입니다. W의 단위도 mol/L이며 h는 무차원입니다.

정확한 계수는 `frozen_network.json`에 저장됩니다. 표의 반올림값으로 다시 구성하면 작은 출력 차이가 생길 수 있습니다.

<!-- lecture-page -->

## 보간 기울기에서 ReLU 가중치로

B의 첫 세 절점 값은 τ=2,4,6에서 0.285714286,0.380952381,0.409090909입니다. x=(τ−2)/8이므로 절점의 x 간격은 2/8=0.25입니다.

| 계산 | 결과 |
| --- | --- |
| 첫 구간의 x 기울기 | (0.380952381−0.285714286)/0.25=0.380952381 |
| 두 번째 구간의 x 기울기 | (0.409090909−0.380952381)/0.25=0.112554113 |
| 첫 ReLU 가중치 W₀B | 첫 기울기 0.380952381 |
| 절점 0.25의 가중치 W₁B | 새 기울기−이전 기울기=−0.268398268 |

0.25<x<0.5에서는 첫 두 ReLU만 미분이 1이므로 전체 기울기는 0.380952381 − 0.268398268 = 0.112554113입니다. 새 항은 절점에서 0이므로 값의 연속성도 유지됩니다.

τ 기준 기울기를 사용했다면 x 기준 가중치로 옮길 때 8을 곱해야 합니다. 같은 농도 변화가 x에서는 8배 짧은 간격에 걸쳐 일어나기 때문입니다. A와 C 열도 같은 방법으로 구합니다.

<!-- lecture-page -->

## τ=5 min에서 은닉값과 B 농도

x=(5−2)/8=0.375를 네 절점 [0,0.25,0.50,0.75]에서 뺍니다.

| j | aⱼ=x−tⱼ | hⱼ | B에 더해지는 값 WⱼB·hⱼ |
| --- | --- | --- | --- |
| 0 | 0.375 | 0.375 | 0.380952381×0.375=0.142857143 |
| 1 | 0.125 | 0.125 | −0.268398268×0.125=−0.033549784 |
| 2 | −0.125 | 0 | 0 |
| 3 | −0.375 | 0 | 0 |

편향 0.285714286을 더하면 B≈0.395021645 mol/L입니다. 4분과 6분의 농도를 반씩 섞어도 (0.380952381+0.409090909)/2=0.395021645가 됩니다.

ReLU 가중합과 구간 보간이 같은 계산을 다른 표현으로 수행합니다. 기준 공정의 5분 B=0.4와는 차이가 있어, 이 예측은 B≥0.40 규격에 조금 못 미칩니다.

<!-- lecture-page -->

## Big-M의 양방향 동치

<math display="block"><mtable columnalign="left"><mtr><mtd><mrow><mi>h</mi><mo>≥</mo><mn>0</mn><mo>,</mo><mtext>  </mtext><mi>h</mi><mo>≥</mo><mi>a</mi></mrow></mtd></mtr><mtr><mtd><mrow><mi>h</mi><mo>≤</mo><mi>a</mi><mo>−</mo><mi>L</mi><mrow><mo>(</mo><mn>1</mn><mo>−</mo><mi>z</mi><mo>)</mo></mrow></mrow></mtd></mtr><mtr><mtd><mrow><mi>h</mi><mo>≤</mo><mi>U</mi><mi>z</mi><mo>,</mo><mtext>  </mtext><mi>z</mi><mo>∈</mo><mo>{</mo><mn>0</mn><mo>,</mo><mn>1</mn><mo>}</mo></mrow></mtd></mtr></mtable></math>

정식화의 가능점에서 z = 0이면 h = 0, a ≤ 0이고, z = 1이면 h = a ≥ 0입니다. 어느 분기에서도 h = max(0, a)입니다.

역으로 ReLU 그래프의 점을 택합니다. a ≤ 0이면 z = 0, a ≥ 0이면 z = 1로 두면 네 부등식이 모두 성립합니다. L ≤ a ≤ U의 유효성이 이 역방향에도 필요합니다.

<!-- lecture-page -->

## 하나의 ReLU 제약에 수치 대입

a=2x−1, x∈[0,1]이면 L=−1,U=1입니다. 네 식은 h≥0, h≥a, h≤a+1−z, h≤z입니다.

| 입력과 가지 | 하한 | 상한 | 결정된 출력 |
| --- | --- | --- | --- |
| x=0.2, a=−0.6, z=0 | h≥0 | h≤0; h≤0.4 | h=0 |
| x=0.8, a=0.6, z=1 | h≥0.6 | h≤0.6; h≤1 | h=0.6 |
| x=0.8에서 잘못된 z=0 | h≥0.6 | h≤0 | 불가능 |

```python
a = 2 * x - 1
h = max(0., a)
z = int(a >= 0.)
assert h >= 0 and h >= a
assert h <= a + 1 - z and h <= z
```

이진변수가 임의의 출력을 만드는 것이 아니라, 주어진 a와 양립하는 가지를 선택합니다. a=0에서는 두 z가 가능하지만 h는 모두 0입니다.

<!-- lecture-page -->

## 다층 ReLU 정식화의 동치성

입력 x를 고정합니다. 첫 affine layer는 a¹을 유일하게 정하고, 각 ReLU 제약은 h¹을 정확히 정합니다.

h¹이 정해지면 다음 affine layer의 a²도 정해집니다. 같은 논리를 마지막 layer까지 반복하면 MILP의 출력은 forward 출력과 같습니다.

반대로 forward 계산의 모든 중간값을 넣고 각 뉴런의 부호로 z를 고르면 MILP 가능점이 됩니다. 전 layer에서 bounds가 유효해야 하며, 0인 뉴런에서 z가 여러 값이어도 출력은 같습니다.

<!-- lecture-page -->

## Layer별 interval bounds의 전파

<math display="block"><mtable columnalign="left"><mtr><mtd><mrow><mi>a</mi><mo>=</mo><msub><mrow><mo>∑</mo></mrow><mrow><mi>i</mi></mrow></msub><msub><mrow><mi>w</mi></mrow><mrow><mi>i</mi></mrow></msub><msub><mrow><mi>h</mi></mrow><mrow><mi>i</mi></mrow></msub><mo>+</mo><mi>b</mi></mrow></mtd></mtr><mtr><mtd><mrow><mi>L</mi><mo>=</mo><mi>b</mi><mo>+</mo><msub><mrow><mo>∑</mo></mrow><mrow><mi>i</mi></mrow></msub><mi>min</mi><mrow><mo>(</mo><msub><mrow><mi>w</mi></mrow><mrow><mi>i</mi></mrow></msub><msub><mrow><mi>l</mi></mrow><mrow><mi>i</mi></mrow></msub><mo>,</mo><msub><mrow><mi>w</mi></mrow><mrow><mi>i</mi></mrow></msub><msub><mrow><mi>u</mi></mrow><mrow><mi>i</mi></mrow></msub><mo>)</mo></mrow></mrow></mtd></mtr><mtr><mtd><mrow><mi>U</mi><mo>=</mo><mi>b</mi><mo>+</mo><msub><mrow><mo>∑</mo></mrow><mrow><mi>i</mi></mrow></msub><mi>max</mi><mrow><mo>(</mo><msub><mrow><mi>w</mi></mrow><mrow><mi>i</mi></mrow></msub><msub><mrow><mi>l</mi></mrow><mrow><mi>i</mi></mrow></msub><mo>,</mo><msub><mrow><mi>w</mi></mrow><mrow><mi>i</mi></mrow></msub><msub><mrow><mi>u</mi></mrow><mrow><mi>i</mi></mrow></msub><mo>)</mo></mrow></mrow></mtd></mtr></mtable></math>

ReLU를 통과한 다음 구간은 [max(0, L), max(0, U)]입니다. 이 구간을 다음 affine layer의 입력 bounds로 전달합니다.

예를 들어 h₁ = x, h₂ = x이면 h₁ − h₂는 항상 0입니다. 각 h가 [0, 1]이라는 정보만 사용하면 [−1, 1]을 얻습니다. 이 범위도 유효하지만 상관관계를 놓쳤습니다.

<!-- lecture-page -->

## 목적함수와 제약 행렬의 변수 순서

변수 순서는 [x, h₀, h₁, h₂, h₃, y_A, y_B, y_C, z₁, z₂, z₃]입니다. 각 행은 row_lower ≤ Av ≤ row_upper 형태로 저장합니다.

V = 2 + 8x에서 상수 2는 최적해에 영향을 주지 않으므로 solver에는 8x만 전달합니다. 보고하는 V와 dual bound에는 2를 다시 더합니다.

정수변수의 bounds를 [0, 1]로 지정해야 이진변수가 됩니다. pre-activation을 별도 변수로 만들면 음수도 허용하도록 하한을 직접 지정합니다.

<!-- lecture-page -->

## 제약식 한 줄을 solver 행으로 저장하기

전체 변수 순서는 [x,h₀,h₁,h₂,h₃,y_A,y_B,y_C,z₁,z₂,z₃]입니다. h₁−x+0.25z₁≤0의 계수는 해당 세 열에만 들어갑니다.

```python
import numpy as np
row = [-1, 0, 1, 0, 0, 0, 0, 0, 0.25, 0, 0]
row_lower = -np.inf
row_upper = 0.0
```

| 대입 | 행 내적 | 판정 |
| --- | --- | --- |
| x=0.5,h₁=0.25,z₁=1 | −0.5+0.25+0.25=0 | 상한 0 만족 |
| x=0.5,h₁=0.30,z₁=1 | −0.5+0.30+0.25=0.05 | 상한 위반 |

출력 등식 y_B−∑WⱼB hⱼ=b_B는 해당 행의 하한과 상한을 모두 b_B로 둡니다. z₁ 열은 정수 표시와 [0,1] bounds를 함께 설정합니다. 계수 배열만 만들고 이 두 설정을 빼면 이진변수가 되지 않습니다.

[SciPy LinearConstraint](https://docs.scipy.org/doc/scipy/reference/generated/scipy.optimize.LinearConstraint.html)는 각 행을 `lb <= A @ v <= ub`로 해석합니다. 따라서 변수 순서와 계수의 부호를 같은 행에서 대조합니다.

<!-- lecture-page -->

## 최적 체류시간 손계산

2-4 min 구간에서 B는 0.40에 못 미칩니다. 4-6 min 구간에서는 B가 증가하므로 최초로 0.40을 만족하는 점을 구합니다.

<math display="block"><mtable columnalign="left"><mtr><mtd><mrow><mi>τ</mi><mo>=</mo><mn>4</mn><mo>+</mo><mn>2</mn><mfrac><mrow><mn>.40</mn><mo>−</mo><mn>.380952380952</mn></mrow><mrow><mn>.409090909091</mn><mo>−</mo><mn>.380952380952</mn></mrow></mfrac></mrow></mtd></mtr><mtr><mtd><mrow><mi>τ</mi><mo>≈</mo><mn>5.353846</mn><mtext> min</mtext></mrow></mtd></mtr></mtable></math>

같은 보간 비율로 [A, B, C] = [0.584615, 0.400000, 0.215385] mol/L를 얻습니다. C ≤ 0.25와 비음수성을 만족하므로 이 점이 최소 체류시간입니다.

<!-- lecture-page -->

## 제품 하한에 도달하는 보간 비율

4~6분 구간에서 B는 0.380952381에서 0.409090909로 증가합니다. 필요한 증가량을 구간 전체 증가량으로 나눕니다.

| 계산 | 값 |
| --- | --- |
| 필요한 B 증가량 | 0.40−0.380952381=0.019047619 |
| 구간 전체 증가량 | 0.409090909−0.380952381=0.028138528 |
| 구간 비율 α | 0.019047619/0.028138528≈0.676923077 |
| 체류시간 | 4+2α≈5.353846154 min |
| 같은 α의 C | 0.152380952+α(0.245454545−0.152380952)≈0.215384615 |

이전 구간의 B는 모두 0.40보다 작습니다. 이 첫 교점에서 C≤0.25와 비음수 조건도 만족하므로 최소 부피를 얻습니다. B만 따로 보간한 뒤 다른 τ의 C와 비교하면 같은 설계의 규격 검사가 되지 않습니다.

<!-- lecture-page -->

## 스칼라 ReLU의 연속 완화

L < 0 < U에서 z ∈ [0, 1]로 풀고 z를 제거하면 다음 삼각형을 얻습니다.

<math display="block"><mtable columnalign="left"><mtr><mtd><mrow><mi>h</mi><mo>≥</mo><mn>0</mn><mo>,</mo><mtext>  </mtext><mi>h</mi><mo>≥</mo><mi>a</mi></mrow></mtd></mtr><mtr><mtd><mrow><mi>h</mi><mo>≤</mo><mfrac><mrow><mi>U</mi></mrow><mrow><mi>U</mi><mo>−</mo><mi>L</mi></mrow></mfrac><mrow><mo>(</mo><mi>a</mi><mo>−</mo><mi>L</mi><mo>)</mo></mrow></mrow></mtd></mtr></mtable></math>

두 상한에서 h/U ≤ z ≤ (h − a + L)/L을 얻습니다. L < 0의 부호 반전에 주의해 결합하면 마지막 부등식이 나옵니다.

이는 스칼라 (a, h) 그래프의 convex hull입니다. a가 여러 입력의 affine 함수일 때 원래 입력 공간의 가장 강한 완화라는 뜻은 아닙니다.

<!-- lecture-page -->

## Affine 등식 투영의 MILP 표현

<math display="block"><mtable columnalign="left"><mtr><mtd><mrow><mi>y</mi><mo>=</mo><mi>P</mi><msub><mrow><mi>y</mi></mrow><mrow><mi>raw</mi></mrow></msub><mo>+</mo><mi>R</mi><mi>u</mi><mo>+</mo><mi>q</mi></mrow></mtd></mtr></mtable></math>

4주차의 투영이 위 affine 형태이고 P, R, q가 고정이면 출력 등식으로 그대로 추가할 수 있습니다. 추가 이진변수는 필요하지 않습니다.

제약 행렬이 조작변수에 따라 달라지면 역행렬이나 변수 곱이 생길 수 있으므로 같은 결론을 바로 적용할 수 없습니다.

보존식을 별도 제약으로 추가할 때는 기존 출력과 일치하는지도 확인합니다. 근사 예측에 새 등식을 추가하면 가능집합이 줄거나 사라질 수 있습니다.

<!-- lecture-page -->

## 연습 1: 부호와 분기 확인

a = 2x − 1, x ∈ [0, 1]에서 L과 U를 구하고 Big-M 식을 적으세요. x = 0.2와 0.8에서 (a, h, z)를 계산합니다.

확인: L = −1, U = 1이고 h ≥ 0, h ≥ 2x − 1, h ≤ 2x − z, h ≤ z입니다.

x = 0.2에서는 (−0.6, 0, 0), x = 0.8에서는 (0.6, 0.6, 1)입니다. x = 0.5에서는 h = 0이고 z는 0 또는 1입니다.

<!-- lecture-page -->

## 연습 2: 제품 규격과 가능집합

C ≤ 0.25를 유지하면서 B ≥ 0.41로 바꾸면 가능해가 남을까요? 표의 knot 값과 구간별 보간으로 판단하세요.

확인: 6 min에서 C = 0.245455이고 8 min에서 0.328205입니다. C 상한은 체류시간을 약 6.109859 min 이하로 제한합니다.

그 점의 B는 약 0.409155 mol/L이며 이전 구간의 B도 더 작습니다. 따라서 변경한 surrogate 문제는 불가능합니다. Solver의 infeasible 종료와 구현 오류는 이 계산으로 구별할 수 있습니다.

<!-- lecture-page -->

## 연습 3: 정식화 검증용 입력

난수 입력만 확인하면 꺾임점이나 영역 끝점의 오류를 놓칠 수 있습니다. τ = 2, 4, 6, 8, 10과 내부 knot 양쪽의 점을 포함하세요.

같은 입력에서 h와 y의 최대 절대 차이를 계산합니다. a = 0에서 이진변수의 일치를 요구하지 말고 출력의 일치를 확인합니다.

확인: 제공 실습은 41개 입력의 최대 차이가 약 1.25 × 10⁻⁸이었습니다. Solver 허용오차 때문에 knot에 매우 가까운 점에서 작은 차이가 남을 수 있습니다. 유효한 정식화의 수학적 동치와 유한 정밀도의 계산 결과를 구분합니다.

<!-- lecture-page -->

## 실습 파일과 출처

`week05_lab.py`는 계수 구성, MILP 행렬 조립, 고정 입력 검사와 구간별 독립 계산을 포함합니다. `frozen_network.json`과 `fit_knots.csv`는 모델을, `results.json`과 `milp_matrix.csv`는 계산을 확인할 때 사용합니다.

[Boyd & Vandenberghe, Convex Optimization](https://stanford.edu/~boyd/cvxbook/), 4.1절: 변수·목적함수·가능집합.

[Anderson et al., Strong mixed-integer programming formulations for trained neural networks](https://arxiv.org/abs/1811.08359), 2.1절: ReLU Big-M 표현.

[SciPy milp 공식 문서](https://docs.scipy.org/doc/scipy/reference/generated/scipy.optimize.milp.html): bounds, integrality, LinearConstraint와 반환 상태.

[강의노트](/courses/surrogate-models/week-05/) · [실습 묶음](/assets/courses/surrogate-models/week-05/week05-lab.zip)
