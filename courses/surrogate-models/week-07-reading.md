---
layout: "course-note"
title: "Week 7: Designing Model Structure for Optimization | Worked Companion"
title_ko: "7주차: 최적화 활용을 위한 모델 구조 설계 | 해설과 연습"
description: "Check ICNN/PICNN convexity conditions and build a ReLU epigraph LP, with counterexamples to equivalence."
description_ko: "ICNN·PICNN의 convexity 조건을 확인하고, ReLU epigraph로 유효한 LP와 동치성이 깨지는 반례를 계산합니다."
material_label: "Week 7 Reading"
material_label_ko: "7주차 읽기자료"
updated: "2026-11-01"
permalink: "/courses/surrogate-models/week-07-reading/"
pdf_en: "/assets/courses/surrogate-models/week-07-reading-en.pdf"
pdf_ko: "/assets/courses/surrogate-models/week-07-reading-ko.pdf"
course_id: "surrogate-models"
notebook: "/assets/courses/surrogate-models/week-07/week07_lab.ipynb"
lab_script: "/assets/courses/surrogate-models/week-07/week07_lab.py"
lab_bundle: "/assets/courses/surrogate-models/week-07/week07-lab.zip"
lecture_note: "/courses/surrogate-models/week-07/"
---

## Mathematical scope of the heating-load decision

The cost used to choose u in [0, 1] is a dimensionless calculation example. It is not a cost law derived from the thermodynamics of a real process.

Consider structural restrictions when there is evidence that the fixed-context cost is convex. Do not transfer this assumption automatically to concentration, yield, or recovery.

Check network convexity, formulation equivalence, and decision quality on the reference function separately.

<!-- lecture-page -->

## The induction step in the convexity proof

Assume each component of h is convex and W ≥ 0. Multiplying the componentwise convexity inequality by W preserves its direction for 0 ≤ λ ≤ 1.

<math display="block"><mtable columnalign="left"><mtr><mtd><mrow><mi>W</mi><mi>h</mi><mo>(</mo><mi>λ</mi><mi>u</mi><mo>+</mo><mo>(</mo><mn>1</mn><mo>−</mo><mi>λ</mi><mo>)</mo><mi>v</mi><mo>)</mo><mo>≤</mo><mi>λ</mi><mi>W</mi><mi>h</mi><mo>(</mo><mi>u</mi><mo>)</mo><mo>+</mo><mo>(</mo><mn>1</mn><mo>−</mo><mi>λ</mi><mo>)</mo><mi>W</mi><mi>h</mi><mo>(</mo><mi>v</mi><mo>)</mo></mrow></mtd></mtr></mtable></math>

The affine term Au + b satisfies equality. Add it, then compose with convex, nondecreasing ReLU to obtain a convex next layer. Apply the same reasoning to the nonnegative output sum.

<!-- lecture-page -->

## Two inclusions for the extended epigraph

Let <math><msup><mi>h</mi><mrow><mo>*</mo></mrow></msup></math> denote actual forward activations. A feasible lifted h satisfies h ≥ <math><msup><mi>h</mi><mrow><mo>*</mo></mrow></msup></math> at the first layer. Substituting this relation and W ≥ 0 into the next-layer constraints propagates the inequality.

Thus every lifted feasible point has t ≥ f(u). Conversely, for any (u, t) with t ≥ f(u), choosing h = <math><msup><mi>h</mi><mrow><mo>*</mo></mrow></msup></math> satisfies the extended constraints.

Projection onto (u, t) is exactly the epigraph. This proof does not require every optimal auxiliary variable to be tight.

<!-- lecture-page -->

## Objective monotonicity and auxiliary recovery

If the objective is nondecreasing in t and all other constraints permit reducing t and h to forward values, recovery preserves the optimal value.

This condition holds directly for min t. An upper bound t ≤ b also permits reduction. Lower bounds h ≥ b, output rewards, and state constraints coupled through output equalities require separate inspection.

An activation with zero weight along all output paths can remain slack without affecting the objective. Interpret predictions by reevaluating the network at u.

<!-- lecture-page -->

## Piecewise calculation of the two-hinge model

<table><thead><tr><th style="font-size:clamp(15px,1.7cqw,22px)">u interval</th><th style="font-size:clamp(15px,1.7cqw,22px)">f(u)</th><th style="font-size:clamp(15px,1.7cqw,22px)">Slope</th></tr></thead><tbody><tr><td style="font-size:clamp(15px,1.7cqw,22px)">[0, 0.4]</td><td style="font-size:clamp(15px,1.7cqw,22px)">0.4 − 0.6u</td><td style="font-size:clamp(15px,1.7cqw,22px)">−0.6</td></tr><tr><td style="font-size:clamp(15px,1.7cqw,22px)">[0.4, 0.7]</td><td style="font-size:clamp(15px,1.7cqw,22px)">0.4u</td><td style="font-size:clamp(15px,1.7cqw,22px)">0.4</td></tr><tr><td style="font-size:clamp(15px,1.7cqw,22px)">[0.7, 1]</td><td style="font-size:clamp(15px,1.7cqw,22px)">0.9u − 0.35</td><td style="font-size:clamp(15px,1.7cqw,22px)">0.9</td></tr></tbody></table>

Continuity gives f(0.4) = 0.16 and f(0.7) = 0.28. The slope switches from negative to positive at the unique minimum 0.4.

Solving f ≤ 0.25 on each interval leaves u ≥ 0.25 and u ≤ 0.625. The third interval contributes no feasible points.

<!-- lecture-page -->

## Cost and feasibility between two knots

Keep only active ReLUs in each interval to simplify the cost.

| u interval | Active terms | Cost | Condition for f(u)≤0.25 |
| --- | --- | --- | --- |
| 0–0.4 | None | 0.4−0.6u | u≥0.25 |
| 0.4–0.7 | u−0.4 | 0.4u | u≤0.625 |
| 0.7–1 | Both | 0.9u−0.35 | u≤2/3, outside this interval |

The feasible interval is [0.25,0.625]. At minimum u=0.4, both ReLUs are zero and f=0.4−0.6×0.4=0.16.

For example, u=0.6 gives h₁=0.2,h₂=0 and f=0.4−0.36+0.2=0.24. This matches 0.4u=0.24 in the middle interval, checking the piecewise expression against the original network.

<!-- lecture-page -->

## LP matrices passed to SciPy

The variable order is [u, h₁, h₂]. Add the objective constant 0.4 after solving.

```python
result = linprog(
    [-0.6, 1.0, 0.5],
    A_ub=[[1, -1, 0], [1, 0, -1]],
    b_ub=[0.4, 0.7],
    bounds=[(0, 1), (0, None), (0, None)],
    method='highs')
value = result.fun + 0.4
```

The first matrix row is u − h₁ ≤ 0.4. Check the returned status before using result.x.

<!-- lecture-page -->

## LP matrix columns and inequalities

Fix variable order [u,h₁,h₂]. Each row of linprog's A_ub is dotted with the variable vector and bounded above by the matching b_ub entry.

| Code value | Expression | Role |
| --- | --- | --- |
| Objective [−0.6,1,0.5] | −0.6u+h₁+0.5h₂ | Cost without constant 0.4 |
| Row [1,−1,0], rhs 0.4 | u−h₁≤0.4 | h₁≥u−0.4 |
| Row [1,0,−1], rhs 0.7 | u−h₂≤0.7 | h₂≥u−0.7 |
| h bounds (0,None) | h₁,h₂≥0 | Other ReLU lower bounds |

At solution [0.4,0,0], row values [0.4,0.4] satisfy their upper bounds. Add constant 0.4 to solver objective −0.24 to report 0.16. The original forward cost must also be 0.16.

Positive h coefficients make this objective minimize h. Changing their signs requires rechecking the recovery argument.

<!-- lecture-page -->

## Complete solution of the inequality-direction counterexample

The true problem is min u with 0 ≤ u ≤ 1 and ReLU(u) ≥ 0.8. ReLU(u) = u on this interval, so the optimum is 0.8.

The relaxation uses h ≥ u, h ≥ 0, h ≥ 0.8. Every u ∈ [0, 1] can be paired with h = max(u, 0.8), expanding the projected feasible set to the full interval.

The optimum is 0. The solver correctly solves the revised problem but does not recover the original answer.

<!-- lecture-page -->

## The fixed-knot ICNN fitting matrix

<math display="block"><mtable columnalign="left"><mtr><mtd><mrow><msub><mi>Φ</mi><mrow><mi>i</mi></mrow></msub><mo>=</mo><mo>[</mo><mn>1</mn><mo>,</mo><msub><mi>u</mi><mrow><mi>i</mi></mrow></msub><mo>,</mo><mi mathvariant="normal">ReLU</mi><mo>(</mo><msub><mi>u</mi><mrow><mi>i</mi></mrow></msub><mo>−</mo><msub><mi>κ</mi><mrow><mn>1</mn></mrow></msub><mo>)</mo><mo>,</mo><mo>…</mo><mo>,</mo><mi mathvariant="normal">ReLU</mi><mo>(</mo><msub><mi>u</mi><mrow><mi>i</mi></mrow></msub><mo>−</mo><msub><mi>κ</mi><mrow><mn>9</mn></mrow></msub><mo>)</mo><mo>]</mo></mrow></mtd></mtr><mtr><mtd><mrow><mi>β</mi><mo>=</mo><mo>[</mo><mi>b</mi><mo>,</mo><mi>a</mi><mo>,</mo><msub><mi>w</mi><mrow><mn>1</mn></mrow></msub><mo>,</mo><mo>…</mo><mo>,</mo><msub><mi>w</mi><mrow><mn>9</mn></mrow></msub><msup><mo>]</mo><mrow><mi>T</mi></mrow></msup></mrow></mtd></mtr><mtr><mtd><mrow><msub><mi mathvariant="normal">min</mi><mrow><mi>β</mi></mrow></msub><mo>‖</mo><mi>Φ</mi><mi>β</mi><mo>−</mo><mi>q</mi><msup><msub><mo>‖</mo><mrow><mn>2</mn></mrow></msub><mrow><mn>2</mn></mrow></msup><mo>,</mo><mi>w</mi><mo>≥</mo><mn>0</mn></mrow></mtd></mtr></mtable></math>

b and a are free; only w is nonnegative. At fixed Φ, the Hessian 2ΦᵀΦ is positive semidefinite, so this is a convex quadratic fit.

If knots or deep-layer weights are also learned, Φ depends on the parameters and this argument no longer applies directly.

<!-- lecture-page -->

## Reference minimizer and decision loss

<math display="block"><mtable columnalign="left"><mtr><mtd><mrow><mi>q</mi><mo>(</mo><mi>u</mi><mo>)</mo><mo>=</mo><mo>(</mo><mi>u</mi><mo>−</mo><mn>.6</mn><msup><mo>)</mo><mrow><mn>2</mn></mrow></msup><mo>+</mo><mn>.1</mn><mi>u</mi><mo>+</mo><mn>.2</mn></mrow></mtd></mtr><mtr><mtd><mrow><mi>q</mi><mo>′</mo><mo>(</mo><mi>u</mi><mo>)</mo><mo>=</mo><mn>2</mn><mo>(</mo><mi>u</mi><mo>−</mo><mn>.6</mn><mo>)</mo><mo>+</mo><mn>.1</mn><mo>=</mo><mn>0</mn><mo>⇒</mo><msup><mi>u</mi><mrow><mo>*</mo></mrow></msup><mo>=</mo><mn>.55</mn></mrow></mtd></mtr><mtr><mtd><mrow><mi>q</mi><mo>(</mo><mn>.5</mn><mo>)</mo><mo>−</mo><mi>q</mi><mo>(</mo><mn>.55</mn><mo>)</mo><mo>=</mo><mn>.2600</mn><mo>−</mo><mn>.2575</mn><mo>=</mo><mn>.0025</mn></mrow></mtd></mtr></mtable></math>

Near a flat minimum, a small prediction error can shift the selected input. Input error 0.05 and cost loss 0.0025 are distinct metrics.

The fitted slope on [0.5, 0.6] is approximately 0.0000233, nearly flat. Check solver tolerances alongside the selected point.

<!-- lecture-page -->

## Prediction error and loss from the selected input

Complete the square in q(u)=(u−0.6)²+0.1u+0.2 to obtain q(u)=(u−0.55)²+0.2575. Squared distance from the minimizer equals the cost increase.

| Input | Reference calculation | Cost |
| --- | --- | --- |
| Reference minimum u=0.55 | 0²+0.2575 | 0.2575 |
| Model choice u=0.50 | (−0.05)²+0.2575 | 0.2600 |
| Difference | 0.2600−0.2575 | 0.0025 |

The difference 0.001563 between predicted cost 0.258437 and reference cost 0.260000 is prediction error at the selected point. Difference 0.0025 from the reference minimum is cost lost because of the selection.

These comparisons use different baselines. State the quantities subtracted in both accuracy reports and decision evaluations.

<!-- lecture-page -->

## Freezing PICNN coefficients and context gates

Suppose a context path r(c) produces a gate s(c) ≥ 0. At fixed c, nonnegative W diag(s(c)) preserves a nonnegative weighted sum of previous convex activations.

A gate multiplying u is a fixed number and can be absorbed into an affine input connection with unrestricted sign.

The lab uses &#124;u − c&#124; − 0.1c² to check the fixed-context LP and a counterexample to joint convexity. It does not train the paper’s full PICNN architecture.

<!-- lecture-page -->

## Scaling and physical constraints

Composing convex f with a fixed affine input map u = Sx + r preserves convexity in x. Bounds, units, and context must still agree between the formulation and forward code.

A positive output scale preserves convexity. A negative scale makes a convex function concave, requiring corresponding changes in objective and inequality interpretation.

A concentration-balance projection can mix components with negative coefficients. The Week 4 equality guarantee alone establishes neither componentwise convexity nor this LP representation.

<!-- lecture-page -->

## Exercises

1. Determine whether f(u) = ReLU(−2u + 1) is input-convex and justify it.
2. Find the feasible interval for f ≤ 0.20 in the two-hinge model.
3. Does adding h ≤ 1 to the linear inequalities for h ≥ ReLU(u) impose equality? Find a counterexample.
4. Test joint convexity of f(u;c) = &#124;u − c&#124; − 0.1c² using a midpoint.
5. Does a lower independent RMSE necessarily reduce the error in the selected input? Explain.

<!-- lecture-page -->

## Short answer checks

1. Convex: it is the maximum of the affine function −2u + 1 and zero.
2. [1/3, 1/2]. Solve 0.4 − 0.6u ≤ 0.2 on the left and 0.4u ≤ 0.2 in the middle.
3. u = 0, h = 0.8 is a counterexample. An upper bound alone does not recover the graph.
4. Endpoint values at (u, c) = (0, 0) and (1, 1) average −0.05; the midpoint value is −0.025.
5. No guarantee: local shape, gradients, and constraint-boundary errors influence the decision.

<!-- lecture-page -->

## Reproduction record and review criteria

The lab was run with NumPy 2.5.4 and SciPy 1.18.1. Timing depends on the execution environment.

Include fitted coefficients, data splits, sign checks, LP status and forward error, and reference decision loss. With multiple minimizers, distinguish objective-value equivalence from input nonuniqueness.

[Amos, Xu and Kolter, Input Convex Neural Networks, ICML 2017, pp. 146-155](https://proceedings.mlr.press/v70/amos17b.html)

[Boyd and Vandenberghe, Convex Optimization, §§3.1-3.2 and 4.1-4.3](https://web.stanford.edu/~boyd/cvxbook/bv_cvxbook.pdf)

<!-- ko -->

## 가열 부하 선택의 수학적 범위

가열 부하 u를 [0, 1]에서 선택할 때 사용한 비용은 무차원 계산 예제입니다. 실제 공정의 열역학 모델에서 convexity를 유도한 비용식은 아닙니다.

공급 조건을 고정한 비용의 형상이 convex라는 근거가 있을 때 구조 제약을 검토합니다. 농도·수율·회수율에는 이 가정을 자동으로 적용하지 않습니다.

네트워크의 convexity, 정식화의 동치성, 기준 함수에서의 의사결정 품질을 각각 확인합니다.

<!-- lecture-page -->

## Convexity 증명의 귀납 단계

h의 각 성분이 convex이고 W ≥ 0이라고 가정합니다. 0 ≤ λ ≤ 1에서 성분별 convexity 부등식에 W를 곱해도 부등식 방향이 유지됩니다.

<math display="block"><mtable columnalign="left"><mtr><mtd><mrow><mi>W</mi><mi>h</mi><mo>(</mo><mi>λ</mi><mi>u</mi><mo>+</mo><mo>(</mo><mn>1</mn><mo>−</mo><mi>λ</mi><mo>)</mo><mi>v</mi><mo>)</mo><mo>≤</mo><mi>λ</mi><mi>W</mi><mi>h</mi><mo>(</mo><mi>u</mi><mo>)</mo><mo>+</mo><mo>(</mo><mn>1</mn><mo>−</mo><mi>λ</mi><mo>)</mo><mi>W</mi><mi>h</mi><mo>(</mo><mi>v</mi><mo>)</mo></mrow></mtd></mtr></mtable></math>

Affine 항 Au + b에는 등식이 성립합니다. 두 항을 더한 뒤 convex·비감소 ReLU를 합성하면 다음 층도 convex입니다. 같은 논증을 출력의 비음수 가중합에 적용합니다.

<!-- lecture-page -->

## 확장 epigraph의 두 포함관계

실제 forward 출력을 <math><msup><mi>h</mi><mrow><mo>*</mo></mrow></msup></math>라 둡니다. 확장 제약의 h는 첫 층에서 h ≥ <math><msup><mi>h</mi><mrow><mo>*</mo></mrow></msup></math>입니다. 이전 층의 이 관계와 W ≥ 0을 다음 층 제약에 대입하면 같은 부등식이 이어집니다.

따라서 모든 확장 feasible point에서 t ≥ f(u)입니다. 반대로 t ≥ f(u)인 임의의 (u, t)에 h = <math><msup><mi>h</mi><mrow><mo>*</mo></mrow></msup></math>를 붙이면 확장 제약을 만족합니다.

즉, 보조변수를 제거한 (u, t) 집합은 정확히 epigraph입니다. 이 증명은 모든 최적 보조변수가 반드시 tight하다고 요구하지 않습니다.

<!-- lecture-page -->

## 목적함수 단조성과 보조변수 복원

목적함수가 t에 대해 비감소이고, 나머지 제약도 t와 h를 forward 값까지 줄이는 것을 허용하면 최적값을 보존하며 복원할 수 있습니다.

min t에서는 이 조건이 직접 성립합니다. t ≤ b인 상한도 줄이는 방향을 허용합니다. 반면 h ≥ b, 출력 보상, 출력 등식과 결합된 다른 상태 제약은 따로 검사해야 합니다.

출력에 연결되지 않은 뉴런의 w가 0이라면 h에 slack이 남아도 목적값은 바뀌지 않습니다. 해석에는 u를 다시 forward 계산한 출력을 사용합니다.

<!-- lecture-page -->

## 두 hinge 모델의 구간별 계산

<table><thead><tr><th style="font-size:clamp(15px,1.7cqw,22px)">u 구간</th><th style="font-size:clamp(15px,1.7cqw,22px)">f(u)</th><th style="font-size:clamp(15px,1.7cqw,22px)">기울기</th></tr></thead><tbody><tr><td style="font-size:clamp(15px,1.7cqw,22px)">[0, 0.4]</td><td style="font-size:clamp(15px,1.7cqw,22px)">0.4 − 0.6u</td><td style="font-size:clamp(15px,1.7cqw,22px)">−0.6</td></tr><tr><td style="font-size:clamp(15px,1.7cqw,22px)">[0.4, 0.7]</td><td style="font-size:clamp(15px,1.7cqw,22px)">0.4u</td><td style="font-size:clamp(15px,1.7cqw,22px)">0.4</td></tr><tr><td style="font-size:clamp(15px,1.7cqw,22px)">[0.7, 1]</td><td style="font-size:clamp(15px,1.7cqw,22px)">0.9u − 0.35</td><td style="font-size:clamp(15px,1.7cqw,22px)">0.9</td></tr></tbody></table>

연속성을 확인하면 f(0.4) = 0.16, f(0.7) = 0.28입니다. 기울기가 음수에서 양수로 바뀌는 0.4가 유일한 최소점입니다.

f ≤ 0.25를 각 구간에서 풀면 u ≥ 0.25와 u ≤ 0.625가 남습니다. 세 번째 구간에는 해가 없습니다.

<!-- lecture-page -->

## 두 절점 사이의 비용과 가능 구간

각 구간에서 켜진 ReLU만 남겨 비용식을 정리합니다.

| u 구간 | 켜진 항 | 비용식 | f(u)≤0.25의 조건 |
| --- | --- | --- | --- |
| 0~0.4 | 없음 | 0.4−0.6u | u≥0.25 |
| 0.4~0.7 | u−0.4 | 0.4u | u≤0.625 |
| 0.7~1 | 두 항 모두 | 0.9u−0.35 | u≤2/3, 해당 구간에 없음 |

가능 구간은 [0.25,0.625]입니다. 최소점 u=0.4에서 두 ReLU가 0이므로 f=0.4−0.6×0.4=0.16입니다.

예를 들어 u=0.6이면 h₁=0.2,h₂=0이고 f=0.4−0.36+0.2=0.24입니다. 중간 구간의 0.4u=0.24와 일치하므로 구간식과 원래 신경망을 서로 확인할 수 있습니다.

<!-- lecture-page -->

## SciPy에 전달하는 LP 행렬

변수 순서는 [u, h₁, h₂]이고 목적함수 상수 0.4는 풀이 뒤 더합니다.

```python
result = linprog(
    [-0.6, 1.0, 0.5],
    A_ub=[[1, -1, 0], [1, 0, -1]],
    b_ub=[0.4, 0.7],
    bounds=[(0, 1), (0, None), (0, None)],
    method='highs')
value = result.fun + 0.4
```

행렬의 첫 행은 u − h₁ ≤ 0.4입니다. 반환된 status를 확인한 뒤 result.x를 사용합니다.

<!-- lecture-page -->

## LP 행렬의 열과 부등식

변수 순서를 [u,h₁,h₂]로 고정합니다. linprog의 A_ub는 각 행과 변수 벡터를 내적한 값이 b_ub 이하가 되도록 해석합니다.

| 코드의 값 | 해당 수식 | 역할 |
| --- | --- | --- |
| 목적 계수 [−0.6,1,0.5] | −0.6u+h₁+0.5h₂ | 상수 0.4를 뺀 비용 |
| 행 [1,−1,0], 우변 0.4 | u−h₁≤0.4 | h₁≥u−0.4 |
| 행 [1,0,−1], 우변 0.7 | u−h₂≤0.7 | h₂≥u−0.7 |
| h의 bounds (0,None) | h₁,h₂≥0 | ReLU의 다른 하한 |

해 [0.4,0,0]을 대입하면 행 값은 [0.4,0.4]로 우변 이하입니다. solver 목적값 −0.24에 상수 0.4를 더해 0.16을 보고합니다. 원래 forward에서 계산한 비용도 0.16이어야 합니다.

양의 h 계수 때문에 이 목적식은 h를 가능한 작게 만듭니다. 목적 계수의 부호를 바꾸면 이 복원 논리를 다시 검사해야 합니다.

<!-- lecture-page -->

## 부등식 방향 반례의 완전한 해

실제 문제는 min u, 0 ≤ u ≤ 1, ReLU(u) ≥ 0.8입니다. 이 입력 구간에서 ReLU(u) = u이므로 최적값은 0.8입니다.

완화에서는 h ≥ u, h ≥ 0, h ≥ 0.8을 사용합니다. 모든 u ∈ [0, 1]에 h = max(u, 0.8)를 붙일 수 있어 feasible 입력이 전체 구간으로 늘어납니다.

최적값은 0입니다. Solver는 변경된 문제를 정확히 풀었지만 원래 문제의 답은 얻지 못했습니다.

<!-- lecture-page -->

## 고정 knot ICNN의 학습 행렬

<math display="block"><mtable columnalign="left"><mtr><mtd><mrow><msub><mi>Φ</mi><mrow><mi>i</mi></mrow></msub><mo>=</mo><mo>[</mo><mn>1</mn><mo>,</mo><msub><mi>u</mi><mrow><mi>i</mi></mrow></msub><mo>,</mo><mi mathvariant="normal">ReLU</mi><mo>(</mo><msub><mi>u</mi><mrow><mi>i</mi></mrow></msub><mo>−</mo><msub><mi>κ</mi><mrow><mn>1</mn></mrow></msub><mo>)</mo><mo>,</mo><mo>…</mo><mo>,</mo><mi mathvariant="normal">ReLU</mi><mo>(</mo><msub><mi>u</mi><mrow><mi>i</mi></mrow></msub><mo>−</mo><msub><mi>κ</mi><mrow><mn>9</mn></mrow></msub><mo>)</mo><mo>]</mo></mrow></mtd></mtr><mtr><mtd><mrow><mi>β</mi><mo>=</mo><mo>[</mo><mi>b</mi><mo>,</mo><mi>a</mi><mo>,</mo><msub><mi>w</mi><mrow><mn>1</mn></mrow></msub><mo>,</mo><mo>…</mo><mo>,</mo><msub><mi>w</mi><mrow><mn>9</mn></mrow></msub><msup><mo>]</mo><mrow><mi>T</mi></mrow></msup></mrow></mtd></mtr><mtr><mtd><mrow><msub><mi mathvariant="normal">min</mi><mrow><mi>β</mi></mrow></msub><mo>‖</mo><mi>Φ</mi><mi>β</mi><mo>−</mo><mi>q</mi><msup><msub><mo>‖</mo><mrow><mn>2</mn></mrow></msub><mrow><mn>2</mn></mrow></msup><mo>,</mo><mi>w</mi><mo>≥</mo><mn>0</mn></mrow></mtd></mtr></mtable></math>

b와 a는 자유롭고 w만 비음수입니다. Φ를 고정하면 목적함수의 Hessian은 2ΦᵀΦ로 positive semidefinite이므로 convex quadratic fit입니다.

Knot 위치나 깊은 층의 가중치도 함께 학습하면 Φ가 매개변수에 의존해 이 논증을 그대로 적용할 수 없습니다.

<!-- lecture-page -->

## 기준 최소점과 결정 손실

<math display="block"><mtable columnalign="left"><mtr><mtd><mrow><mi>q</mi><mo>(</mo><mi>u</mi><mo>)</mo><mo>=</mo><mo>(</mo><mi>u</mi><mo>−</mo><mn>.6</mn><msup><mo>)</mo><mrow><mn>2</mn></mrow></msup><mo>+</mo><mn>.1</mn><mi>u</mi><mo>+</mo><mn>.2</mn></mrow></mtd></mtr><mtr><mtd><mrow><mi>q</mi><mo>′</mo><mo>(</mo><mi>u</mi><mo>)</mo><mo>=</mo><mn>2</mn><mo>(</mo><mi>u</mi><mo>−</mo><mn>.6</mn><mo>)</mo><mo>+</mo><mn>.1</mn><mo>=</mo><mn>0</mn><mo>⇒</mo><msup><mi>u</mi><mrow><mo>*</mo></mrow></msup><mo>=</mo><mn>.55</mn></mrow></mtd></mtr><mtr><mtd><mrow><mi>q</mi><mo>(</mo><mn>.5</mn><mo>)</mo><mo>−</mo><mi>q</mi><mo>(</mo><mn>.55</mn><mo>)</mo><mo>=</mo><mn>.2600</mn><mo>−</mo><mn>.2575</mn><mo>=</mo><mn>.0025</mn></mrow></mtd></mtr></mtable></math>

최소점 부근에서 비용 곡선이 완만하면 작은 예측 오차가 입력 위치를 바꿀 수 있습니다. 입력 오차 0.05와 비용 손실 0.0025는 서로 다른 평가량입니다.

학습한 기울기 중 [0.5, 0.6] 구간은 약 0.0000233으로 거의 평평합니다. solver 허용오차를 함께 확인합니다.

<!-- lecture-page -->

## 예측 오차와 선택한 입력의 손실

기준 비용 q(u)=(u−0.6)²+0.1u+0.2를 완전제곱으로 정리하면 q(u)=(u−0.55)²+0.2575입니다. 최소점에서 벗어난 거리의 제곱이 비용 증가량입니다.

| 입력 | 기준 비용 계산 | 비용 |
| --- | --- | --- |
| 기준 최소 u=0.55 | 0²+0.2575 | 0.2575 |
| 모델 선택 u=0.50 | (−0.05)²+0.2575 | 0.2600 |
| 차이 | 0.2600−0.2575 | 0.0025 |

모델이 선택한 점의 예측 비용 0.258437과 기준 비용 0.260000의 차이 0.001563은 그 점의 예측 오차입니다. 기준 최소값과의 차이 0.0025는 선택 때문에 생긴 비용 손실입니다.

같은 숫자를 비교하는 기준이 다릅니다. 정확도 표와 의사결정 평가 표에서 각각 무엇을 빼는지 명시합니다.

<!-- lecture-page -->

## PICNN 계수 고정과 context gate

Context 경로 r(c)가 gate s(c) ≥ 0을 계산한다고 합시다. 고정된 c에서 W diag(s(c))가 비음수이면 이전 convex 활성화의 비음수 가중합을 유지합니다.

u에 곱하는 gate는 고정된 수이므로 부호가 자유로운 affine 입력 연결에 포함할 수 있습니다.

실습에서는 &#124;u − c&#124; − 0.1c²로 고정 context에서의 LP와 공동 convexity 반례를 확인합니다. 원 논문의 전체 PICNN 구조를 학습하는 실험은 포함하지 않습니다.

<!-- lecture-page -->

## Scaling과 물리 제약의 관계

고정된 affine 입력 변환 u = Sx + r에 convex f를 합성하면 x에 대해서도 convex입니다. 하지만 bounds, 단위와 고정 context는 정식화와 forward 코드에서 같아야 합니다.

양의 출력 scale은 convexity를 보존합니다. 음의 scale은 convex 함수를 concave로 바꾸므로 목적함수·부등식 방향을 함께 바꿔 해석해야 합니다.

농도 합을 맞추는 projection은 성분을 음의 계수로 섞을 수 있습니다. Week 4의 등식 보장만으로 각 출력의 convexity나 이 LP 표현을 보장하지는 않습니다.

<!-- lecture-page -->

## 연습 문제

1. f(u) = ReLU(−2u + 1)의 입력 convexity를 판정하고 근거를 적습니다.
2. 두 hinge 모델에서 f ≤ 0.20의 feasible 구간을 구합니다.
3. h ≥ ReLU(u)를 나타내는 선형 부등식에 h ≤ 1을 추가하면 h = ReLU(u)가 되는지 반례를 찾습니다.
4. f(u;c) = &#124;u − c&#124; − 0.1c²의 공동 convexity를 중점으로 검사합니다.
5. 비용 모델의 독립 RMSE가 줄어들 때 최적 입력 오차도 반드시 줄어드는지 설명합니다.

<!-- lecture-page -->

## 연습 문제의 짧은 답

1. Convex입니다. Affine 함수 −2u + 1과 0의 최댓값입니다.
2. [1/3, 1/2]입니다. 왼쪽에서는 0.4 − 0.6u ≤ 0.2, 가운데에서는 0.4u ≤ 0.2를 풉니다.
3. u = 0, h = 0.8이 반례입니다. 상한만으로 그래프 등식을 얻지 못합니다.
4. (u, c) = (0, 0), (1, 1)의 평균 함수값은 −0.05, 중점 값은 −0.025입니다.
5. 보장되지 않습니다. 최적점 주변의 국소 형상·기울기와 제약 경계의 오차가 결정에 영향을 줍니다.

<!-- lecture-page -->

## 재현 기록과 검토 기준

실습은 NumPy 2.5.4, SciPy 1.18.1에서 실행했습니다. 계산시간은 실행 환경에 따라 달라집니다.

제출물에는 학습 계수, 데이터 구분, 부호 검사, LP status와 forward 오차, 기준 비용 손실을 포함합니다. 최소점이 여러 개이면 목적값 동치성과 입력의 비유일성을 구분합니다.

[Amos, Xu and Kolter, Input Convex Neural Networks, ICML 2017, pp. 146-155](https://proceedings.mlr.press/v70/amos17b.html)

[Boyd and Vandenberghe, Convex Optimization, §§3.1-3.2 and 4.1-4.3](https://web.stanford.edu/~boyd/cvxbook/bv_cvxbook.pdf)
