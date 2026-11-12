---
layout: "course-note"
title: "Week 8: Selecting and Revalidating Operating Conditions | Worked Companion"
title_ko: "8주차: 운전 조건 선택과 공정 모델 재검증 | 해설과 연습"
description: "Revalidate Week 6 reactor decisions with reference process equations and compare violations, costs, and targeted data updates."
description_ko: "6주차 반응기 모델의 후보를 기준 공정식으로 재검증하고, 제약 위반·비용·추가 데이터의 효과를 비교합니다."
material_label: "Week 8 Reading"
material_label_ko: "8주차 읽기자료"
updated: "2026-11-01"
permalink: "/courses/surrogate-models/week-08-reading/"
pdf_en: "/assets/courses/surrogate-models/week-08-reading-en.pdf"
pdf_ko: "/assets/courses/surrogate-models/week-08-reading-ko.pdf"
course_id: "surrogate-models"
notebook: "/assets/courses/surrogate-models/week-08/week08_lab.ipynb"
lab_script: "/assets/courses/surrogate-models/week-08/week08_lab.py"
lab_bundle: "/assets/courses/surrogate-models/week-08/week08-lab.zip"
lecture_note: "/courses/surrogate-models/week-08/"
---

## Cost reduction subject to specifications

Reject candidates that violate product specifications even when their cost is low. Recalculate candidates under identical reactor equations and specifications to compare acceptance and cost.

The baseline is 330 K and 6 min, giving B = 0.409091 and C = 0.245455 mol/L. It is reference-feasible and costs 76.80 $/h.

Retaining it during comparison preserves a checked option when a new model or solve fails.

<!-- lecture-page -->

## Deriving the steady-state material balances

<math display="block"><mtable columnalign="left"><mtr><mtd><mrow><mn>0</mn><mo>=</mo><mfrac><mrow><msub><mi>C</mi><mrow><mi>A</mi><mn>0</mn></mrow></msub><mo>−</mo><msub><mi>C</mi><mrow><mi>A</mi></mrow></msub></mrow><mrow><mi>τ</mi></mrow></mfrac><mo>−</mo><msub><mi>k</mi><mrow><mn>1</mn></mrow></msub><msub><mi>C</mi><mrow><mi>A</mi></mrow></msub></mrow></mtd></mtr><mtr><mtd><mrow><mn>0</mn><mo>=</mo><mo>−</mo><mfrac><mrow><msub><mi>C</mi><mrow><mi>B</mi></mrow></msub></mrow><mrow><mi>τ</mi></mrow></mfrac><mo>+</mo><msub><mi>k</mi><mrow><mn>1</mn></mrow></msub><msub><mi>C</mi><mrow><mi>A</mi></mrow></msub><mo>−</mo><msub><mi>k</mi><mrow><mn>2</mn></mrow></msub><msub><mi>C</mi><mrow><mi>B</mi></mrow></msub></mrow></mtd></mtr><mtr><mtd><mrow><mn>0</mn><mo>=</mo><mo>−</mo><mfrac><mrow><msub><mi>C</mi><mrow><mi>C</mi></mrow></msub></mrow><mrow><mi>τ</mi></mrow></mfrac><mo>+</mo><msub><mi>k</mi><mrow><mn>2</mn></mrow></msub><msub><mi>C</mi><mrow><mi>B</mi></mrow></msub></mrow></mtd></mtr></mtable></math>

These are per-volume balances using τ = V/F. Solve the first for A, the second for B, and the third for C to obtain the lecture’s reference equations.

Summing the equations gives <math><msub><mi>C</mi><mrow><mi>A</mi></mrow></msub></math> + <math><msub><mi>C</mi><mrow><mi>B</mi></mrow></msub></math> + <math><msub><mi>C</mi><mrow><mi>C</mi></mrow></msub></math> = <math><msub><mi>C</mi><mrow><mi>A</mi><mn>0</mn></mrow></msub></math>, under the equal-mole consecutive-reaction and constant-density assumptions.

<!-- lecture-page -->

## Hand calculation of the baseline

At 330 K, k₁ = 0.2 and k₂ = 0.1 min⁻¹. Substitute τ = 6 min.

<math display="block"><mtable columnalign="left"><mtr><mtd><mrow><msub><mi>C</mi><mrow><mi>A</mi></mrow></msub><mo>=</mo><mn>1.2</mn><mo>/</mo><mo>(</mo><mn>1</mn><mo>+</mo><mn>.2</mn><mo>×</mo><mn>6</mn><mo>)</mo><mo>=</mo><mn>.545455</mn></mrow></mtd></mtr><mtr><mtd><mrow><msub><mi>C</mi><mrow><mi>B</mi></mrow></msub><mo>=</mo><mn>.2</mn><mo>×</mo><mn>6</mn><mo>×</mo><mn>.545455</mn><mo>/</mo><mo>(</mo><mn>1</mn><mo>+</mo><mn>.1</mn><mo>×</mo><mn>6</mn><mo>)</mo><mo>=</mo><mn>.409091</mn></mrow></mtd></mtr><mtr><mtd><mrow><msub><mi>C</mi><mrow><mi>C</mi></mrow></msub><mo>=</mo><mn>.1</mn><mo>×</mo><mn>6</mn><mo>×</mo><mn>.409091</mn><mo>=</mo><mn>.245455</mn></mrow></mtd></mtr></mtable></math>

This satisfies B ≥ 0.38 and C ≤ 0.25. Cost is 12 × 6 + 0.24 × 20 = 76.80 $/h.

<!-- lecture-page -->

## Deriving one-sided margins

Define error as e = prediction − reference. If overprediction <math><msub><mi>e</mi><mrow><mi>B</mi></mrow></msub></math> is bounded by <math><msub><mi>δ</mi><mrow><mi>B</mi></mrow></msub></math> everywhere in the domain, then

<math display="block"><mtable columnalign="left"><mtr><mtd><mrow><msub><mi>C</mi><mrow><mi>B</mi></mrow></msub><mo>=</mo><msub><mi>Ĉ</mi><mrow><mi>B</mi></mrow></msub><mo>−</mo><msub><mi>e</mi><mrow><mi>B</mi></mrow></msub><mo>≥</mo><mn>.38</mn><mo>+</mo><msub><mi>δ</mi><mrow><mi>B</mi></mrow></msub><mo>−</mo><msub><mi>δ</mi><mrow><mi>B</mi></mrow></msub><mo>=</mo><mn>.38</mn></mrow></mtd></mtr></mtable></math>

For C, the required bound is on underprediction, −<math><msub><mi>e</mi><mrow><mi>C</mi></mrow></msub></math> ≤ <math><msub><mi>δ</mi><mrow><mi>C</mi></mrow></msub></math>. Then <math><msub><mi>Ĉ</mi><mrow><mi>C</mi></mrow></msub></math> ≤ 0.25 − <math><msub><mi>δ</mi><mrow><mi>C</mi></mrow></msub></math> gives <math><msub><mi>C</mi><mrow><mi>C</mi></mrow></msub></math> = <math><msub><mi>Ĉ</mi><mrow><mi>C</mi></mrow></msub></math> − <math><msub><mi>e</mi><mrow><mi>C</mi></mrow></msub></math> ≤ 0.25.

This argument assumes uniform bounds. Maxima on a finite calibration sample do not prove that assumption.

<!-- lecture-page -->

## Calculating one-sided margins

Define e=prediction−reference. Positive e is adverse for B; negative e is adverse for C.

| Quantity | B lower limit | C upper limit |
| --- | --- | --- |
| Original specification | Reference B≥0.38 | Reference C≤0.25 |
| Applied margin | δ_B=0.02130 | δ_C=0.01305 |
| Required prediction | B̂≥0.40130 | Ĉ≤0.23695 |
| At the assumed error limit | 0.40130−0.02130=0.38 | 0.23695+0.01305=0.25 |

The last row applies when the error limit holds at that input. The maximum over 961 calibration points does not prove a bound at every unseen point. Reevaluate the next candidate with the reference process even after adding margins.

Sample margins are δ_B=max(0,maxᵢ e_B,i) and δ_C=max(0,maxᵢ(−e_C,i)). B errors [−0.003,0.008,0.002] give 0.008; C errors [0.004,−0.006,−0.001] give 0.006. Unlike an absolute-error maximum, these select only the direction that can violate the specification.

<!-- lecture-page -->

## Data partitions and reference-evaluation cost

<table><thead><tr><th style="font-size:clamp(15px,1.7cqw,22px)">Data</th><th style="font-size:clamp(15px,1.7cqw,22px)">Size and role</th></tr></thead><tbody><tr><td style="font-size:clamp(15px,1.7cqw,22px)">Existing training</td><td style="font-size:clamp(15px,1.7cqw,22px)">Week 6 network, 1,200 training points</td></tr><tr><td style="font-size:clamp(15px,1.7cqw,22px)">Independent evaluation</td><td style="font-size:clamp(15px,1.7cqw,22px)">997 inputs, seed 808, full-box prediction error</td></tr><tr><td style="font-size:clamp(15px,1.7cqw,22px)">Calibration</td><td style="font-size:clamp(15px,1.7cqw,22px)">31 × 31 = 961, margin calculation</td></tr><tr><td style="font-size:clamp(15px,1.7cqw,22px)">Local update</td><td style="font-size:clamp(15px,1.7cqw,22px)">3 × 3 = 9, affine residual fitting</td></tr><tr><td style="font-size:clamp(15px,1.7cqw,22px)">Candidate revalidation</td><td style="font-size:clamp(15px,1.7cqw,22px)">Fresh reference evaluation at each selected input</td></tr><tr><td style="font-size:clamp(15px,1.7cqw,22px)">Comparison search</td><td style="font-size:clamp(15px,1.7cqw,22px)">4,001 T values and local scalar refinement</td></tr></tbody></table>

Do not mix post-fit candidate revalidation data into independent test results. With expensive process models, calibration and benchmark costs also belong in the evaluation budget.

<!-- lecture-page -->

## Error signs at a selected point

At the unadjusted candidate, predicted B is 0.380000 and reference B is 0.371157 mol/L. Thus <math><msub><mi>e</mi><mrow><mi>B</mi></mrow></msub></math> = +0.008843, the adverse overprediction direction.

Predicted C is 0.171228 and reference C is 0.178136 mol/L. Although <math><msub><mi>e</mi><mrow><mi>C</mi></mrow></msub></math> = −0.006908 is adverse underprediction, reference C remains below 0.25.

Error signs alone do not determine acceptance. Compare error magnitudes with the remaining margin to each constraint.

<!-- lecture-page -->

## Local update coordinates and residual regression

The unadjusted candidate has scaled coordinates approximately (0.80148, 0.06556). Offsets ±0.06 correspond to ±2.4 K and ±0.48 min.

<math display="block"><mtable columnalign="left"><mtr><mtd><mrow><msub><mi>r</mi><mrow><mi>i</mi></mrow></msub><mo>=</mo><msup><mi>C</mi><mrow><mi>r</mi><mi>e</mi><mi>f</mi></mrow></msup><mo>(</mo><msub><mi>x</mi><mrow><mi>i</mi></mrow></msub><mo>)</mo><mo>−</mo><msub><mi>f</mi><mrow><mi>θ</mi></mrow></msub><mo>(</mo><msub><mi>x</mi><mrow><mi>i</mi></mrow></msub><mo>)</mo></mrow></mtd></mtr><mtr><mtd><mrow><msub><mi mathvariant="normal">min</mi><mrow><mi>β</mi></mrow></msub><msup><msub><mo>∑</mo><mrow><mi>i</mi><mo>=</mo><mn>1</mn></mrow></msub><mrow><mn>9</mn></mrow></msup><mo>‖</mo><msub><mi>r</mi><mrow><mi>i</mi></mrow></msub><mo>−</mo><mo>[</mo><mn>1</mn><mo>,</mo><msub><mi>x</mi><mrow><mi>i</mi><mn>1</mn></mrow></msub><mo>,</mo><msub><mi>x</mi><mrow><mi>i</mi><mn>2</mn></mrow></msub><mo>]</mo><mi>β</mi><msup><msub><mo>‖</mo><mrow><mn>2</mn></mrow></msub><mrow><mn>2</mn></mrow></msup></mrow></mtd></mtr></mtable></math>

Use the same input matrix for every output component. Adding an affine output term preserves the ReLU binary structure. Optimize the corrected model only inside the update-data box.

<!-- lecture-page -->

## Local-data coordinates and the regression matrix

Candidate (342.0593 K,2.52444 min) has scaled coordinates [(342.0593−310)/40,(2.52444−2)/8]≈[0.80148,0.06556].

| Axis | Scaled offset | Physical offset |
| --- | --- | --- |
| Temperature | ±0.06 | ±2.4 K |
| Residence time | ±0.06 | ±0.48 min |

```python
design = np.column_stack((np.ones(len(x_local)), x_local))
residual = reference_y - network_y
beta = np.linalg.lstsq(design, residual, rcond=None)[0]
corrected_y = network_y + design @ beta
```

For nine inputs, design is (9,3), the three-component residual is (9,3), and beta is (3,3). Multiplying a row [1,x₁,x₂] by beta gives three corrections. Restrict the next optimization to the fitted region and check remaining error at the new candidate.

<!-- lecture-page -->

## Substituting the fitted correction coefficients

The recorded B correction coefficients are [−0.0160962605,0.0074357617,0.0823403944]. At local candidate (339.815193 K,2.870934 min), x₁=0.745379824 and x₂=0.108866748.

| B correction term | Value [mol/L] |
| --- | --- |
| Intercept | −0.0160962605 |
| Temperature-coordinate term | 0.0074357617×0.745379824=0.0055424667 |
| Residence-time-coordinate term | 0.0823403944×0.108866748=0.0089641309 |
| Sum | −0.0015896628 |

Adding this to the original network prediction B≈0.3835896628 gives corrected prediction 0.382000. The reference value at the same input is 0.3768201356, leaving error 0.0051798644.

Least squares reduces the summed squared errors of nine points. It does not require interpolation of every point or exact prediction at a new candidate. Correctly computed regression coefficients still require candidate revalidation.

<!-- lecture-page -->

## Follow-up data from a failed correction

B error at the local-correction candidate is 0.005180 mol/L, exceeding the applied 0.002 margin. Although its prediction is 0.002 above the specification, its reference output falls short by 0.003180.

Add the failed point’s reference output to the update data and examine residual changes with temperature and residence time. A smaller region or larger margin are other candidate revisions.

Each revision defines a new model or problem. Revalidate against the same original specifications and retain a checked feasible candidate until a revision succeeds.

<!-- lecture-page -->

## Calculating residence time from the product specification

At fixed T, setting <math><msub><mi>C</mi><mrow><mi>B</mi></mrow></msub></math> to target b gives a quadratic equation in τ.

<math display="block"><mtable columnalign="left"><mtr><mtd><mrow><msub><mi>C</mi><mrow><mi>B</mi></mrow></msub><mo>=</mo><mfrac><mrow><mn>1.2</mn><msub><mi>k</mi><mrow><mn>1</mn></mrow></msub><mi>τ</mi></mrow><mrow><mo>(</mo><mn>1</mn><mo>+</mo><msub><mi>k</mi><mrow><mn>1</mn></mrow></msub><mi>τ</mi><mo>)</mo><mo>(</mo><mn>1</mn><mo>+</mo><msub><mi>k</mi><mrow><mn>2</mn></mrow></msub><mi>τ</mi><mo>)</mo></mrow></mfrac></mrow></mtd></mtr><mtr><mtd><mrow><mi>b</mi><msub><mi>k</mi><mrow><mn>1</mn></mrow></msub><msub><mi>k</mi><mrow><mn>2</mn></mrow></msub><msup><mi>τ</mi><mrow><mn>2</mn></mrow></msup><mo>+</mo><mo>[</mo><mi>b</mi><mo>(</mo><msub><mi>k</mi><mrow><mn>1</mn></mrow></msub><mo>+</mo><msub><mi>k</mi><mrow><mn>2</mn></mrow></msub><mo>)</mo><mo>−</mo><mn>1.2</mn><msub><mi>k</mi><mrow><mn>1</mn></mrow></msub><mo>]</mo><mi>τ</mi><mo>+</mo><mi>b</mi><mo>=</mo><mn>0</mn></mrow></mtd></mtr></mtable></math>

With a nonnegative discriminant and two positive roots, B ≥ b between the roots. The τ bounds and C upper limit must also hold.

The smaller root is preferred because cost increases with τ at fixed T.

<!-- lecture-page -->

## From the B specification to a quadratic in residence time

At fixed temperature, k₁ and k₂ are numbers. Set B to target b and multiply by the positive concentration denominator.

| Step | Relation |
| --- | --- |
| Set B=b | 1.2k₁τ=b(1+k₁τ)(1+k₂τ) |
| Expand denominator | 1.2k₁τ=b[1+(k₁+k₂)τ+k₁k₂τ²] |
| Collect terms | bk₁k₂τ²+[b(k₁+k₂)−1.2k₁]τ+b=0 |

At 330 K and b=0.4, this is 0.008τ²−0.12τ+0.4=0. Dividing by 0.008 gives (τ−5)(τ−10)=0. B≥0.4 holds between the roots, [5,10].

At fixed temperature, cost increases with τ, so check 5 min first. It gives C=0.1×5×0.4=0.2≤0.25. At 10 min, C=0.4 violates the cap; the B condition alone is insufficient.

<!-- lecture-page -->

## The smaller root and a stable numerical formula

<math display="block"><mtable columnalign="left"><mtr><mtd><mrow><mi>a</mi><mo>=</mo><mi>b</mi><msub><mi>k</mi><mrow><mn>1</mn></mrow></msub><msub><mi>k</mi><mrow><mn>2</mn></mrow></msub><mo>,</mo><mi>d</mi><mo>=</mo><mi>b</mi><mo>(</mo><msub><mi>k</mi><mrow><mn>1</mn></mrow></msub><mo>+</mo><msub><mi>k</mi><mrow><mn>2</mn></mrow></msub><mo>)</mo><mo>−</mo><mn>1.2</mn><msub><mi>k</mi><mrow><mn>1</mn></mrow></msub></mrow></mtd></mtr><mtr><mtd><mrow><mi>D</mi><mo>=</mo><msup><mi>d</mi><mrow><mn>2</mn></mrow></msup><mo>−</mo><mn>4</mn><mi>a</mi><mi>b</mi></mrow></mtd></mtr><mtr><mtd><mrow><msub><mi>τ</mi><mrow><mi>l</mi><mi>o</mi><mi>w</mi></mrow></msub><mo>=</mo><mfrac><mrow><mn>2</mn><mi>b</mi></mrow><mrow><mo>−</mo><mi>d</mi><mo>+</mo><msqrt><mi>D</mi></msqrt></mrow></mfrac></mrow></mtd></mtr></mtable></math>

For a > 0, d < 0, D ≥ 0, this computes the smaller positive root while avoiding subtraction of similar positive quantities in the standard formula.

Take max(2, <math><msub><mi>τ</mi><mrow><mi>l</mi><mi>o</mi><mi>w</mi></mrow></msub></math>), then check the larger root, the 10 min upper bound, and the C specification. No roots or an exceeded upper bound means no feasible candidate at that T.

<!-- lecture-page -->

## Rationalizing the smaller-root formula

For aτ²+dτ+b=0, define D=d²−4ab. With a>0,d<0,D≥0, the smaller root is (−d−√D)/(2a). Multiply numerator and denominator by −d+√D.

<div class="equation"><math xmlns="http://www.w3.org/1998/Math/MathML" display="block"><mrow><mfrac><mrow><mo>−</mo><mi>d</mi><mo>−</mo><msqrt><mi>D</mi></msqrt></mrow><mrow><mn>2</mn><mi>a</mi></mrow></mfrac><mo>=</mo><mfrac><mrow><msup><mi>d</mi><mn>2</mn></msup><mo>−</mo><mi>D</mi></mrow><mrow><mn>2</mn><mi>a</mi><mo stretchy="false">(</mo><mo>−</mo><mi>d</mi><mo>+</mo><msqrt><mi>D</mi></msqrt><mo stretchy="false">)</mo></mrow></mfrac><mo>=</mo><mfrac><mrow><mn>2</mn><mi>b</mi></mrow><mrow><mo>−</mo><mi>d</mi><mo>+</mo><msqrt><mi>D</mi></msqrt></mrow></mfrac></mrow></math></div>

Since d²−D=4ab, cancellation gives the last expression. Replacing subtraction of similar positive values −d and √D with addition reduces loss of significant digits.

At 330 K,b=0.4, a=0.008,d=−0.12,D=0.0016 and √D=0.04. The smaller root is 0.8/(0.12+0.04)=5; the larger is (0.12+0.04)/0.016=10 min. Substitute roots back into the original B equation and C specification before accepting a candidate.

<!-- lecture-page -->

## Calculating the reference-repaired candidate

Fix the local-correction candidate’s temperature at 339.8152 K and use b = 0.382. The smaller root is τ = 3.08559 min.

Reference outputs are A = 0.618470, B = 0.382000, and C = 0.199530 mol/L. They sum to 1.2 and satisfy the C upper bound.

Cost is 44.1828 $/h, which is 32.6172 $/h below the initial baseline. This point leaves the local optimization box, so report it separately as a repair checked directly with the reference equations.

<!-- lecture-page -->

## Computing the smaller root and revalidating the candidate

At T=339.8152 K and b=0.382, calculate a=bk₁k₂ and d=b(k₁+k₂)−1.2k₁. A negative discriminant means there is no real residence time with B=b at this temperature.

```python
k1 = 0.2 * np.exp(40000 / 8.314 * (1/330 - 1/T))
k2 = 0.1 * np.exp(50000 / 8.314 * (1/330 - 1/T))
a = b * k1 * k2
d = b * (k1 + k2) - 1.2 * k1
disc = d*d - 4*a*b
tau = 2*b / (-d + np.sqrt(disc))
```

Here k₁≈0.3047, k₂≈0.1693/min and τ≈3.08559 min. This smaller-root formula uses a>0,d<0,disc≥0. Check the original τ bounds and reference B,C for each candidate.

Reference C≈0.199530<0.25 and cost is 12×3.08559+0.24×(339.8152−310)≈44.1828 $/h. Savings from the original baseline are 76.8−44.1828=32.6172 $/h.

<!-- lecture-page -->

## Benchmark differences and conditions for regret

<math display="block"><mtable columnalign="left"><mtr><mtd><mrow><mi>Δ</mi><msub><mi>J</mi><mrow><mi>b</mi><mi>e</mi><mi>n</mi><mi>c</mi><mi>h</mi></mrow></msub><mo>=</mo><mi>J</mi><mo>(</mo><msub><mi>u</mi><mrow><mi>c</mi><mi>a</mi><mi>n</mi><mi>d</mi><mi>i</mi><mi>d</mi><mi>a</mi><mi>t</mi><mi>e</mi></mrow></msub><mo>)</mo><mo>−</mo><mi>J</mi><mo>(</mo><msub><mi>u</mi><mrow><mi>b</mi><mi>e</mi><mi>n</mi><mi>c</mi><mi>h</mi></mrow></msub><mo>)</mo></mrow></mtd></mtr></mtable></math>

Compute this when both points satisfy the original specifications. If the benchmark is only a found feasible solution, the difference does not certify regret relative to the global optimum. It could become negative for a better candidate.

The repaired candidate has difference 44.1828 − 41.3920 = 2.7908 $/h. Leave savings and benchmark differences blank for the infeasible unadjusted and local-correction candidates.

<!-- lecture-page -->

## Predicted versus actual improvement

For minimization using an objective model m on a common feasible input domain, compare predicted and actual improvement between the current point and a candidate.

<math display="block"><mtable columnalign="left"><mtr><mtd><mrow><mi>ρ</mi><mo>=</mo><mfrac><mrow><mi>J</mi><mo>(</mo><msub><mi>u</mi><mrow><mi>o</mi><mi>l</mi><mi>d</mi></mrow></msub><mo>)</mo><mo>−</mo><mi>J</mi><mo>(</mo><msub><mi>u</mi><mrow><mi>n</mi><mi>e</mi><mi>w</mi></mrow></msub><mo>)</mo></mrow><mrow><mi>m</mi><mo>(</mo><msub><mi>u</mi><mrow><mi>o</mi><mi>l</mi><mi>d</mi></mrow></msub><mo>)</mo><mo>−</mo><mi>m</mi><mo>(</mo><msub><mi>u</mi><mrow><mi>n</mi><mi>e</mi><mi>w</mi></mrow></msub><mo>)</mo></mrow></mfrac></mrow></mtd></mtr></mtable></math>

Use this ratio only with a positive denominator. Here the cost is an exact input function, so feasibility error is the issue rather than objective-model error. Do not use this ratio to accept infeasible candidates.

[Alexandrov, Dennis, Lewis and Torczon, A trust-region framework for managing the use of approximation models in optimization (1998), author manuscript](https://www.cs.wm.edu/~va/research/adlt.pdf)

If the true objective drops from 100 to 92 while the model predicts 100 to 90, actual improvement is 8, predicted improvement is 10, and ρ=0.8. If the model also predicts 100 at the new point, the denominator is zero and the ratio is not evaluated. Both candidates must first satisfy the original constraints.

<!-- lecture-page -->

## Exercises

1. Calculate B violation at the unadjusted candidate and C slack at the baseline.
2. If the uniform overprediction bound for B is 0.01, what lower bound is needed on predicted B?
3. Does the maximum error on 961 calibration points guarantee the entire box? Explain.
4. State the acceptance rule when comparing an infeasible cost of 37.9875 with a feasible cost of 44.1828.
5. Propose a point after local-correction failure and explain why it should not be added to the independent test set.

<!-- lecture-page -->

## Short answer checks

1. B shortfall is 0.008843 mol/L. Baseline C slack is 0.25 − 0.245455 = 0.004545 mol/L.
2. Require predicted B ≥ 0.39 mol/L. The implication holds only where the uniform bound is valid.
3. Larger errors between sampled points remain possible. Reevaluate the new candidate.
4. Compare costs among specification-feasible candidates. The cost 37.9875 is not accepted savings.
5. The failed point (339.8152 K, 2.87093 min) and nearby boundary points are useful. If used for improvement, they become adaptively collected training data.

<!-- lecture-page -->

## Final submission and supporting sources

Submit the candidate table, rejection reasons, feasible-cost comparison, model/data revision plan, and execution record. State the reference assumptions used in evaluation.

Use the weight hash recorded in the result file to check that the same fitted model was used. A solver’s optimal status applies to its formulation, not global optimality of the actual process.

[Week 6 frozen model](/assets/courses/surrogate-models/week-06/frozen_cstr_network.json)

[Alexandrov, Dennis, Lewis and Torczon, A trust-region framework for managing the use of approximation models in optimization (1998), author manuscript](https://www.cs.wm.edu/~va/research/adlt.pdf)

<!-- ko -->

## 규격을 지키는 비용 절감

제품 규격을 어긴 후보는 비용이 낮아도 채택할 수 없습니다. 같은 반응기 식과 규격으로 후보를 다시 계산해 채택 여부와 비용을 비교합니다.

기준 후보는 330 K, 6 min이며 B = 0.409091, C = 0.245455 mol/L입니다. 기준 공정식에서 feasible하고 비용은 76.80 $/h입니다.

비교 과정에서 이 후보를 유지하면 새 모델이나 풀이가 실패해도 이미 확인한 선택지를 잃지 않습니다.

<!-- lecture-page -->

## 정상상태 물질수지 유도

<math display="block"><mtable columnalign="left"><mtr><mtd><mrow><mn>0</mn><mo>=</mo><mfrac><mrow><msub><mi>C</mi><mrow><mi>A</mi><mn>0</mn></mrow></msub><mo>−</mo><msub><mi>C</mi><mrow><mi>A</mi></mrow></msub></mrow><mrow><mi>τ</mi></mrow></mfrac><mo>−</mo><msub><mi>k</mi><mrow><mn>1</mn></mrow></msub><msub><mi>C</mi><mrow><mi>A</mi></mrow></msub></mrow></mtd></mtr><mtr><mtd><mrow><mn>0</mn><mo>=</mo><mo>−</mo><mfrac><mrow><msub><mi>C</mi><mrow><mi>B</mi></mrow></msub></mrow><mrow><mi>τ</mi></mrow></mfrac><mo>+</mo><msub><mi>k</mi><mrow><mn>1</mn></mrow></msub><msub><mi>C</mi><mrow><mi>A</mi></mrow></msub><mo>−</mo><msub><mi>k</mi><mrow><mn>2</mn></mrow></msub><msub><mi>C</mi><mrow><mi>B</mi></mrow></msub></mrow></mtd></mtr><mtr><mtd><mrow><mn>0</mn><mo>=</mo><mo>−</mo><mfrac><mrow><msub><mi>C</mi><mrow><mi>C</mi></mrow></msub></mrow><mrow><mi>τ</mi></mrow></mfrac><mo>+</mo><msub><mi>k</mi><mrow><mn>2</mn></mrow></msub><msub><mi>C</mi><mrow><mi>B</mi></mrow></msub></mrow></mtd></mtr></mtable></math>

τ = V/F로 나눈 단위 부피당 수지입니다. 첫 식에서 A, 두 번째 식에서 B, 세 번째 식에서 C를 순서대로 구하면 강의의 기준식을 얻습니다.

세 식을 더하면 <math><msub><mi>C</mi><mrow><mi>A</mi></mrow></msub></math> + <math><msub><mi>C</mi><mrow><mi>B</mi></mrow></msub></math> + <math><msub><mi>C</mi><mrow><mi>C</mi></mrow></msub></math> = C_A0입니다. 이 관계는 동일 몰수의 연속 반응과 일정 밀도라는 가정 아래 성립합니다.

<!-- lecture-page -->

## 기준 후보의 손 계산

330 K에서는 k₁ = 0.2, k₂ = 0.1 min⁻¹입니다. τ = 6 min를 대입합니다.

<math display="block"><mtable columnalign="left"><mtr><mtd><mrow><msub><mi>C</mi><mrow><mi>A</mi></mrow></msub><mo>=</mo><mn>1.2</mn><mo>/</mo><mo>(</mo><mn>1</mn><mo>+</mo><mn>.2</mn><mo>×</mo><mn>6</mn><mo>)</mo><mo>=</mo><mn>.545455</mn></mrow></mtd></mtr><mtr><mtd><mrow><msub><mi>C</mi><mrow><mi>B</mi></mrow></msub><mo>=</mo><mn>.2</mn><mo>×</mo><mn>6</mn><mo>×</mo><mn>.545455</mn><mo>/</mo><mo>(</mo><mn>1</mn><mo>+</mo><mn>.1</mn><mo>×</mo><mn>6</mn><mo>)</mo><mo>=</mo><mn>.409091</mn></mrow></mtd></mtr><mtr><mtd><mrow><msub><mi>C</mi><mrow><mi>C</mi></mrow></msub><mo>=</mo><mn>.1</mn><mo>×</mo><mn>6</mn><mo>×</mo><mn>.409091</mn><mo>=</mo><mn>.245455</mn></mrow></mtd></mtr></mtable></math>

B ≥ 0.38, C ≤ 0.25를 만족합니다. 비용은 12 × 6 + 0.24 × 20 = 76.80 $/h입니다.

<!-- lecture-page -->

## 한쪽 오차와 margin의 유도

오차를 e = 예측 − 기준 출력으로 정의합니다. B의 과대예측 e_B가 <math><msub><mi>δ</mi><mrow><mi>B</mi></mrow></msub></math> 이하라는 영역 전체의 bound가 있다면 다음이 성립합니다.

<math display="block"><mtable columnalign="left"><mtr><mtd><mrow><msub><mi>C</mi><mrow><mi>B</mi></mrow></msub><mo>=</mo><msub><mi>Ĉ</mi><mrow><mi>B</mi></mrow></msub><mo>−</mo><msub><mi>e</mi><mrow><mi>B</mi></mrow></msub><mo>≥</mo><mn>.38</mn><mo>+</mo><msub><mi>δ</mi><mrow><mi>B</mi></mrow></msub><mo>−</mo><msub><mi>δ</mi><mrow><mi>B</mi></mrow></msub><mo>=</mo><mn>.38</mn></mrow></mtd></mtr></mtable></math>

C에서는 과소예측 −<math><msub><mi>e</mi><mrow><mi>C</mi></mrow></msub></math> ≤ δ_C가 필요한 bound입니다. <math><msub><mi>Ĉ</mi><mrow><mi>C</mi></mrow></msub></math> ≤ 0.25 − δ_C이면 <math><msub><mi>C</mi><mrow><mi>C</mi></mrow></msub></math> = <math><msub><mi>Ĉ</mi><mrow><mi>C</mi></mrow></msub></math> − <math><msub><mi>e</mi><mrow><mi>C</mi></mrow></msub></math> ≤ 0.25입니다.

이 논증은 uniform bound를 가정합니다. 유한 calibration 표본의 최대값만으로 그 가정을 입증하지는 못합니다.

<!-- lecture-page -->

## 한쪽 방향 margin의 계산

오차를 e=예측−기준으로 정의합니다. B에서는 e가 양수일 때, C에서는 e가 음수일 때 위험한 방향입니다.

| 항목 | B 하한 | C 상한 |
| --- | --- | --- |
| 원래 규격 | 기준 B≥0.38 | 기준 C≤0.25 |
| 적용 margin | δ_B=0.02130 | δ_C=0.01305 |
| 예측에 요구할 값 | B̂≥0.40130 | Ĉ≤0.23695 |
| 오차가 가정한 한계일 때 | 0.40130−0.02130=0.38 | 0.23695+0.01305=0.25 |

이 마지막 행은 오차 한계가 그 입력에서 성립할 때의 계산입니다. calibration 961점의 최대값은 보지 않은 모든 점의 한계를 증명하지 않습니다. 그래서 margin을 넣은 다음 후보도 기준 공정으로 다시 계산합니다.

표본에서 margin을 구하는 연산은 δ_B=max(0,maxᵢ e_B,i), δ_C=max(0,maxᵢ(−e_C,i))입니다. B 오차 [−0.003,0.008,0.002]라면 0.008, C 오차 [0.004,−0.006,−0.001]라면 0.006을 사용합니다. 절댓값 최대와 달리 규격을 위반시키는 쪽만 선택합니다.

<!-- lecture-page -->

## 데이터 분할과 참조 계산의 비용

<table><thead><tr><th style="font-size:clamp(15px,1.7cqw,22px)">데이터</th><th style="font-size:clamp(15px,1.7cqw,22px)">크기·역할</th></tr></thead><tbody><tr><td style="font-size:clamp(15px,1.7cqw,22px)">기존 학습</td><td style="font-size:clamp(15px,1.7cqw,22px)">6주차 네트워크, 1,200개 학습점</td></tr><tr><td style="font-size:clamp(15px,1.7cqw,22px)">독립 평가</td><td style="font-size:clamp(15px,1.7cqw,22px)">997개, seed 808, 전체 box의 예측 오차</td></tr><tr><td style="font-size:clamp(15px,1.7cqw,22px)">Calibration</td><td style="font-size:clamp(15px,1.7cqw,22px)">31 × 31 = 961개, margin 계산</td></tr><tr><td style="font-size:clamp(15px,1.7cqw,22px)">국소 보완</td><td style="font-size:clamp(15px,1.7cqw,22px)">3 × 3 = 9개, affine 잔차 학습</td></tr><tr><td style="font-size:clamp(15px,1.7cqw,22px)">후보 재검증</td><td style="font-size:clamp(15px,1.7cqw,22px)">선택한 각 입력의 새로운 기준 계산</td></tr><tr><td style="font-size:clamp(15px,1.7cqw,22px)">비교용 탐색</td><td style="font-size:clamp(15px,1.7cqw,22px)">4,001개 T와 국소 1차원 refinement</td></tr></tbody></table>

서로게이트 학습 뒤 후보 재검증에 쓴 데이터를 독립 test 결과에 섞지 않습니다. 공정식의 계산 비용이 크면 calibration과 benchmark에 드는 비용도 예산에 포함합니다.

<!-- lecture-page -->

## 최적점에서의 오차 부호

무보정 후보에서 B 예측은 0.380000, 기준값은 0.371157 mol/L입니다. <math><msub><mi>e</mi><mrow><mi>B</mi></mrow></msub></math> = +0.008843이므로 위험한 과대예측입니다.

C 예측은 0.171228, 기준값은 0.178136 mol/L입니다. <math><msub><mi>e</mi><mrow><mi>C</mi></mrow></msub></math> = −0.006908로 과소예측하지만 기준값도 상한 0.25 아래입니다.

두 성분의 오차 부호만으로 후보를 판정하지 않습니다. 오차의 크기와 각 제약까지의 여유를 함께 봅니다.

<!-- lecture-page -->

## 국소 보완 좌표와 잔차 회귀

무보정 후보의 정규화 좌표는 약 (0.80148, 0.06556)입니다. 각 축에서 ±0.06을 이동하면 온도 ±2.4 K, 체류시간 ±0.48 min에 해당합니다.

<math display="block"><mtable columnalign="left"><mtr><mtd><mrow><msub><mi>r</mi><mrow><mi>i</mi></mrow></msub><mo>=</mo><msup><mi>C</mi><mrow><mi>r</mi><mi>e</mi><mi>f</mi></mrow></msup><mo>(</mo><msub><mi>x</mi><mrow><mi>i</mi></mrow></msub><mo>)</mo><mo>−</mo><msub><mi>f</mi><mrow><mi>θ</mi></mrow></msub><mo>(</mo><msub><mi>x</mi><mrow><mi>i</mi></mrow></msub><mo>)</mo></mrow></mtd></mtr><mtr><mtd><mrow><msub><mi mathvariant="normal">min</mi><mrow><mi>β</mi></mrow></msub><msup><msub><mo>∑</mo><mrow><mi>i</mi><mo>=</mo><mn>1</mn></mrow></msub><mrow><mn>9</mn></mrow></msup><mo>‖</mo><msub><mi>r</mi><mrow><mi>i</mi></mrow></msub><mo>−</mo><mo>[</mo><mn>1</mn><mo>,</mo><msub><mi>x</mi><mrow><mi>i</mi><mn>1</mn></mrow></msub><mo>,</mo><msub><mi>x</mi><mrow><mi>i</mi><mn>2</mn></mrow></msub><mo>]</mo><mi>β</mi><msup><msub><mo>‖</mo><mrow><mn>2</mn></mrow></msub><mrow><mn>2</mn></mrow></msup></mrow></mtd></mtr></mtable></math>

각 성분에 같은 입력 행렬을 사용합니다. 출력에 affine 항을 더해도 ReLU의 binary 구조는 유지됩니다. 보정 모델은 데이터 box 안에서만 최적화에 사용합니다.

<!-- lecture-page -->

## 국소 데이터의 좌표와 회귀 행렬

후보 (342.0593 K,2.52444 min)의 scaled 좌표는 [(342.0593−310)/40,(2.52444−2)/8]≈[0.80148,0.06556]입니다.

| 축 | scaled offset | 물리 단위 offset |
| --- | --- | --- |
| 온도 | ±0.06 | ±2.4 K |
| 체류시간 | ±0.06 | ±0.48 min |

```python
design = np.column_stack((np.ones(len(x_local)), x_local))
residual = reference_y - network_y
beta = np.linalg.lstsq(design, residual, rcond=None)[0]
corrected_y = network_y + design @ beta
```

9개 입력의 design은 (9,3), 세 성분 residual도 (9,3), beta는 (3,3)입니다. design의 한 행 [1,x₁,x₂]와 beta를 곱하면 세 성분의 보정값이 나옵니다. 이 회귀가 본 범위 안으로 다음 최적화 영역을 제한하되, 남은 오차는 새 후보에서 확인합니다.

<!-- lecture-page -->

## 학습된 보정 계수의 수치 대입

제공 실행의 B 보정 계수는 [−0.0160962605,0.0074357617,0.0823403944]입니다. 국소 후보 (339.815193 K,2.870934 min)의 좌표는 x₁=0.745379824,x₂=0.108866748입니다.

| B 보정의 항 | 계산값 [mol/L] |
| --- | --- |
| 절편 | −0.0160962605 |
| 온도 좌표 항 | 0.0074357617×0.745379824=0.0055424667 |
| 체류시간 좌표 항 | 0.0823403944×0.108866748=0.0089641309 |
| 합 | −0.0015896628 |

원래 신경망 B≈0.3835896628에 이 합을 더하면 보정 예측은 0.382000입니다. 같은 입력의 기준값 0.3768201356과 비교하면 오차 0.0051798644가 남습니다.

최소제곱은 아홉 점의 제곱오차 합을 줄입니다. 모든 점을 통과하는 보간 조건이나 새 후보에서 정확해야 한다는 제약은 없습니다. 회귀 계수의 계산이 맞아도 후보 재검증이 필요한 이유입니다.

<!-- lecture-page -->

## 보정 실패에서 얻는 다음 데이터

국소 보정 후보의 B 예측 오차는 0.005180 mol/L로 적용한 margin 0.002보다 큽니다. 모델은 원래 규격보다 0.002 높은 값을 예측하지만 기준 출력은 0.003180 부족합니다.

실패 지점의 기준 출력을 보완 데이터에 추가하고, 주변의 온도·체류시간 변화에 따른 잔차를 확인합니다. 좁은 영역이나 더 큰 margin도 후보 방법입니다.

각 변경은 새로운 모델 또는 문제입니다. 같은 원래 규격으로 재검증하고, 성공 전까지 확인된 feasible 후보를 유지합니다.

<!-- lecture-page -->

## 제품 규격에서 체류시간 계산

T를 고정하고 목표 농도를 b라고 하면 <math><msub><mi>C</mi><mrow><mi>B</mi></mrow></msub></math> = b는 τ에 대한 이차방정식입니다.

<math display="block"><mtable columnalign="left"><mtr><mtd><mrow><msub><mi>C</mi><mrow><mi>B</mi></mrow></msub><mo>=</mo><mfrac><mrow><mn>1.2</mn><msub><mi>k</mi><mrow><mn>1</mn></mrow></msub><mi>τ</mi></mrow><mrow><mo>(</mo><mn>1</mn><mo>+</mo><msub><mi>k</mi><mrow><mn>1</mn></mrow></msub><mi>τ</mi><mo>)</mo><mo>(</mo><mn>1</mn><mo>+</mo><msub><mi>k</mi><mrow><mn>2</mn></mrow></msub><mi>τ</mi><mo>)</mo></mrow></mfrac></mrow></mtd></mtr><mtr><mtd><mrow><mi>b</mi><msub><mi>k</mi><mrow><mn>1</mn></mrow></msub><msub><mi>k</mi><mrow><mn>2</mn></mrow></msub><msup><mi>τ</mi><mrow><mn>2</mn></mrow></msup><mo>+</mo><mo>[</mo><mi>b</mi><mo>(</mo><msub><mi>k</mi><mrow><mn>1</mn></mrow></msub><mo>+</mo><msub><mi>k</mi><mrow><mn>2</mn></mrow></msub><mo>)</mo><mo>−</mo><mn>1.2</mn><msub><mi>k</mi><mrow><mn>1</mn></mrow></msub><mo>]</mo><mi>τ</mi><mo>+</mo><mi>b</mi><mo>=</mo><mn>0</mn></mrow></mtd></mtr></mtable></math>

판별식이 0 이상이고 양의 두 근이 있으면 그 사이에서 B ≥ b입니다. τ의 box와 C 상한도 만족해야 합니다.

작은 쪽 근을 선택하는 이유는 같은 T에서 비용이 τ에 대해 증가하기 때문입니다.

<!-- lecture-page -->

## B 규격에서 체류시간 이차식으로

온도를 고정하면 k₁,k₂가 숫자로 정해집니다. 목표 B 농도를 b라 두고 농도식의 양의 분모를 곱합니다.

| 순서 | 관계식 |
| --- | --- |
| B=b | 1.2k₁τ=b(1+k₁τ)(1+k₂τ) |
| 분모 전개 | 1.2k₁τ=b[1+(k₁+k₂)τ+k₁k₂τ²] |
| 한쪽으로 모으기 | bk₁k₂τ²+[b(k₁+k₂)−1.2k₁]τ+b=0 |

330 K에서 b=0.4이면 0.008τ²−0.12τ+0.4=0이고, 0.008로 나누면 (τ−5)(τ−10)=0입니다. B≥0.4는 두 근 사이 [5,10]에서 성립합니다.

비용은 같은 온도에서 τ가 작을수록 낮으므로 5분을 먼저 확인합니다. 이때 C=0.1×5×0.4=0.2≤0.25입니다. 10분에서는 C=0.4로 상한을 위반하므로 B 조건만으로는 부족합니다.

<!-- lecture-page -->

## 작은 근과 안정적인 계산식

<math display="block"><mtable columnalign="left"><mtr><mtd><mrow><mi>a</mi><mo>=</mo><mi>b</mi><msub><mi>k</mi><mrow><mn>1</mn></mrow></msub><msub><mi>k</mi><mrow><mn>2</mn></mrow></msub><mo>,</mo><mi>d</mi><mo>=</mo><mi>b</mi><mo>(</mo><msub><mi>k</mi><mrow><mn>1</mn></mrow></msub><mo>+</mo><msub><mi>k</mi><mrow><mn>2</mn></mrow></msub><mo>)</mo><mo>−</mo><mn>1.2</mn><msub><mi>k</mi><mrow><mn>1</mn></mrow></msub></mrow></mtd></mtr><mtr><mtd><mrow><mi>D</mi><mo>=</mo><msup><mi>d</mi><mrow><mn>2</mn></mrow></msup><mo>−</mo><mn>4</mn><mi>a</mi><mi>b</mi></mrow></mtd></mtr><mtr><mtd><mrow><msub><mi>τ</mi><mrow><mi>l</mi><mi>o</mi><mi>w</mi></mrow></msub><mo>=</mo><mfrac><mrow><mn>2</mn><mi>b</mi></mrow><mrow><mo>−</mo><mi>d</mi><mo>+</mo><msqrt><mi>D</mi></msqrt></mrow></mfrac></mrow></mtd></mtr></mtable></math>

위 식은 a > 0, d < 0, D ≥ 0에서 작은 양의 근을 계산합니다. 표준 근의 공식에서 비슷한 양수를 빼는 계산을 피합니다.

먼저 max(2, <math><msub><mi>τ</mi><mrow><mi>l</mi><mi>o</mi><mi>w</mi></mrow></msub></math>)를 취하고 큰 근, 10 min, C 규격을 검사합니다. 근이 없거나 상한을 넘으면 그 온도는 feasible 후보를 주지 않습니다.

<!-- lecture-page -->

## 작은 근 공식의 유리화

이차식 aτ²+dτ+b=0에서 D=d²−4ab입니다. a>0,d<0,D≥0이면 작은 근은 (−d−√D)/(2a)입니다. 분자·분모에 −d+√D를 곱합니다.

<div class="equation"><math xmlns="http://www.w3.org/1998/Math/MathML" display="block"><mrow><mfrac><mrow><mo>−</mo><mi>d</mi><mo>−</mo><msqrt><mi>D</mi></msqrt></mrow><mrow><mn>2</mn><mi>a</mi></mrow></mfrac><mo>=</mo><mfrac><mrow><msup><mi>d</mi><mn>2</mn></msup><mo>−</mo><mi>D</mi></mrow><mrow><mn>2</mn><mi>a</mi><mo stretchy="false">(</mo><mo>−</mo><mi>d</mi><mo>+</mo><msqrt><mi>D</mi></msqrt><mo stretchy="false">)</mo></mrow></mfrac><mo>=</mo><mfrac><mrow><mn>2</mn><mi>b</mi></mrow><mrow><mo>−</mo><mi>d</mi><mo>+</mo><msqrt><mi>D</mi></msqrt></mrow></mfrac></mrow></math></div>

d²−D=4ab를 약분한 결과입니다. 비슷한 두 양수 −d와 √D의 뺄셈을 합으로 바꿔 유효 숫자의 손실을 줄입니다.

330 K,b=0.4 예에서는 a=0.008,d=−0.12,D=0.0016,√D=0.04입니다. 작은 근은 0.8/(0.12+0.04)=5, 큰 근은 (0.12+0.04)/0.016=10 min입니다. 계산한 근을 다시 원래 B 식과 C 규격에 대입해야 후보 판정이 끝납니다.

<!-- lecture-page -->

## 기준식 보완 후보의 계산

국소 보정 후보의 온도 339.8152 K를 고정하고 b = 0.382를 사용합니다. 작은 쪽 근은 τ = 3.08559 min입니다.

기준 출력은 A = 0.618470, B = 0.382000, C = 0.199530 mol/L입니다. 농도 합은 1.2이며 C 상한도 만족합니다.

비용은 44.1828 $/h이고 초기 기준 후보 대비 32.6172 $/h 낮습니다. 최적화에 사용한 국소 box를 벗어나므로 기준식으로 직접 확인한 보완 단계로 따로 보고합니다.

<!-- lecture-page -->

## 작은 근의 계산과 후보 재검증

T=339.8152 K, b=0.382에서 a=bk₁k₂, d=b(k₁+k₂)−1.2k₁을 계산합니다. 판별식이 음수이면 이 온도에서 B=b인 실수 체류시간이 없습니다.

```python
k1 = 0.2 * np.exp(40000 / 8.314 * (1/330 - 1/T))
k2 = 0.1 * np.exp(50000 / 8.314 * (1/330 - 1/T))
a = b * k1 * k2
d = b * (k1 + k2) - 1.2 * k1
disc = d*d - 4*a*b
tau = 2*b / (-d + np.sqrt(disc))
```

이 경우 k₁≈0.3047, k₂≈0.1693/min이고 τ≈3.08559 min입니다. 작은 근 식은 a>0,d<0,disc≥0인 경우를 사용합니다. 후보마다 원래 τ 범위와 기준 B,C를 다시 검사합니다.

기준 C≈0.199530<0.25이며 비용은 12×3.08559+0.24×(339.8152−310)≈44.1828 $/h입니다. 초기 기준안 대비 절감은 76.8−44.1828=32.6172 $/h입니다.

<!-- lecture-page -->

## Benchmark 차이와 regret의 조건

<math display="block"><mtable columnalign="left"><mtr><mtd><mrow><mi>Δ</mi><msub><mi>J</mi><mrow><mi>b</mi><mi>e</mi><mi>n</mi><mi>c</mi><mi>h</mi></mrow></msub><mo>=</mo><mi>J</mi><mo>(</mo><msub><mi>u</mi><mrow><mi>c</mi><mi>a</mi><mi>n</mi><mi>d</mi><mi>i</mi><mi>d</mi><mi>a</mi><mi>t</mi><mi>e</mi></mrow></msub><mo>)</mo><mo>−</mo><mi>J</mi><mo>(</mo><msub><mi>u</mi><mrow><mi>b</mi><mi>e</mi><mi>n</mi><mi>c</mi><mi>h</mi></mrow></msub><mo>)</mo></mrow></mtd></mtr></mtable></math>

둘 다 원래 규격에서 feasible할 때 계산합니다. Benchmark가 단지 발견한 feasible 해라면 이 차이는 전역 최적값 대비 regret를 인증하지 않습니다. 더 좋은 후보를 찾으면 음수가 될 수도 있습니다.

이번 기준식 보완 후보의 차이는 44.1828 − 41.3920 = 2.7908 $/h입니다. 무보정·국소 보정 후보는 infeasible이므로 이 비교 표에서 절감액과 차이를 비워 둡니다.

<!-- lecture-page -->

## 예측 개선과 실제 개선의 비율

공통 feasible 입력 영역에서 목적함수 모델 m을 사용하는 최소화라면 현재점과 후보 사이의 개선을 비교할 수 있습니다.

<math display="block"><mtable columnalign="left"><mtr><mtd><mrow><mi>ρ</mi><mo>=</mo><mfrac><mrow><mi>J</mi><mo>(</mo><msub><mi>u</mi><mrow><mi>o</mi><mi>l</mi><mi>d</mi></mrow></msub><mo>)</mo><mo>−</mo><mi>J</mi><mo>(</mo><msub><mi>u</mi><mrow><mi>n</mi><mi>e</mi><mi>w</mi></mrow></msub><mo>)</mo></mrow><mrow><mi>m</mi><mo>(</mo><msub><mi>u</mi><mrow><mi>o</mi><mi>l</mi><mi>d</mi></mrow></msub><mo>)</mo><mo>−</mo><mi>m</mi><mo>(</mo><msub><mi>u</mi><mrow><mi>n</mi><mi>e</mi><mi>w</mi></mrow></msub><mo>)</mo></mrow></mfrac></mrow></mtd></mtr></mtable></math>

분모가 양수일 때만 이 비율로 예측 개선을 평가합니다. 이번 예제의 비용식은 정확한 입력 함수라 비용 오차보다 feasibility 오차가 문제입니다. Infeasible 후보에는 이 비율을 수락 근거로 쓰지 않습니다.

[Alexandrov, Dennis, Lewis and Torczon, A trust-region framework for managing the use of approximation models in optimization (1998), author manuscript](https://www.cs.wm.edu/~va/research/adlt.pdf)

예를 들어 목적값이 100→92로 줄고 모델은 100→90을 예측했다면 실제 개선 8, 예측 개선 10으로 ρ=0.8입니다. 모델의 새 예측도 100이라면 분모가 0이므로 나누지 않습니다. 이 비율은 두 후보의 원래 제약 만족을 확인한 뒤에만 의미가 있습니다.

<!-- lecture-page -->

## 연습 문제

1. 무보정 후보의 B 위반량과 기준 후보의 C 여유를 계산합니다.
2. B 과대예측의 uniform bound가 0.01이면 예측 B에 어떤 하한을 걸어야 합니까?
3. 961개 calibration 점의 최대 오차가 전체 box에서의 보장을 주는지 설명합니다.
4. Infeasible 후보의 비용 37.9875와 feasible 후보의 비용 44.1828을 비교해 채택 기준을 적습니다.
5. 국소 보정 실패 뒤 추가할 점과, 그 점을 test set에 넣으면 안 되는 이유를 설명합니다.

<!-- lecture-page -->

## 연습 문제의 짧은 답

1. B 부족량은 0.008843 mol/L, 기준 후보의 C 여유는 0.25 − 0.245455 = 0.004545 mol/L입니다.
2. 예측 B ≥ 0.39 mol/L입니다. 보장은 uniform bound가 유효한 영역에서만 성립합니다.
3. 표본 밖의 더 큰 오차를 배제하지 못합니다. 새 후보의 기준 계산이 필요합니다.
4. 규격을 만족하는 후보끼리 비용을 비교합니다. 37.9875는 채택된 절감 성과가 아닙니다.
5. 실패 지점 (339.8152 K, 2.87093 min)과 주변 경계점이 유용합니다. 모델 개선에 사용하면 적응적으로 수집한 학습 데이터가 됩니다.

<!-- lecture-page -->

## 최종 제출과 근거 자료

제출물은 후보 비교표, 기각 이유, feasible 후보의 비용 비교, 수정할 모델·데이터 계획과 실행 기록으로 구성합니다. 평가에 사용한 기준식의 가정도 명시합니다.

결과 파일에 기록한 가중치 hash로 같은 학습 모델을 사용했는지 확인합니다. Solver의 optimal은 각 정식화에 대한 종료 상태이며 실제 공정의 전역 최적성을 뜻하지 않습니다.

[6주차 고정 모델](/assets/courses/surrogate-models/week-06/frozen_cstr_network.json)

[Alexandrov, Dennis, Lewis and Torczon, A trust-region framework for managing the use of approximation models in optimization (1998), author manuscript](https://www.cs.wm.edu/~va/research/adlt.pdf)
