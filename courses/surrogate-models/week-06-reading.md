---
layout: "course-note"
title: "Week 6 Reading: Bounds, Relaxations, and Solver Results"
title_ko: "6주차 읽기자료: Bounds, 완화와 solver 결과"
description: "Bounds, scaling, OMLT, and solver interpretation with open-source HiGHS."
description_ko: "Bounds와 scaling을 조정하고 오픈소스 HiGHS로 신경망 기반 최적화를 풀어 결과를 해석합니다."
material_label: "Week 6 reading"
material_label_ko: "6주차 읽기자료"
updated: "2026-10-31"
permalink: "/courses/surrogate-models/week-06-reading/"
pdf_en: "/assets/courses/surrogate-models/week-06-reading-en.pdf"
pdf_ko: "/assets/courses/surrogate-models/week-06-reading-ko.pdf"
course_id: "surrogate-models"
notebook: "/assets/courses/surrogate-models/week-06/week06_lab.ipynb"
lab_script: "/assets/courses/surrogate-models/week-06/week06_lab.py"
lecture_note: "/courses/surrogate-models/week-06/"
---

## A sequence for reviewing the reactor calculation

After computing reactor conditions that meet product specifications, separately assess optimization progress and process prediction accuracy.

Derive the MILP and LP solutions of the two-neuron example, calculate bounds and scaling, then check the OMLT connections and CSTR results.

The [lab ZIP](/assets/courses/surrogate-models/week-06/week06-lab.zip) contains the network coefficients and recorded results. All LPs and MILPs use open-source HiGHS.

<!-- lecture-page -->

## Deriving the triangle relaxation from Big-M

Assume L < 0 < U and z ∈ [0, 1]. Rearrange h ≤ Uz and h ≤ a − L(1 − z) in terms of z.

<math display="block"><mtable columnalign="left"><mtr><mtd><mrow><mfrac><mrow><mi>h</mi></mrow><mrow><mi>U</mi></mrow></mfrac><mo>≤</mo><mi>z</mi><mo>≤</mo><mfrac><mrow><mi>h</mi><mo>−</mo><mi>a</mi><mo>+</mo><mi>L</mi></mrow><mrow><mi>L</mi></mrow></mfrac></mrow></mtd></mtr><mtr><mtd><mrow><mi>h</mi><mo>(</mo><mi>U</mi><mo>−</mo><mi>L</mi><mo>)</mo><mo>≤</mo><mi>U</mi><mo>(</mo><mi>a</mi><mo>−</mo><mi>L</mi><mo>)</mo></mrow></mtd></mtr></mtable></math>

Dividing by negative L reverses the inequality. Retaining h ≥ 0 and h ≥ a gives the lecture triangle relaxation. Keep the valid interval for a as well.

<!-- lecture-page -->

## Deriving the integer solution of the toy example

<math display="block"><mtable columnalign="left"><mtr><mtd><mrow><mn>0</mn><mo>≤</mo><msub><mrow><mi>x</mi></mrow><mrow><mn>1</mn></mrow></msub><mo>,</mo><msub><mrow><mi>x</mi></mrow><mrow><mn>2</mn></mrow></msub><mo>≤</mo><mn>1</mn><mo>,</mo><mtext>  </mtext><msub><mrow><mi>x</mi></mrow><mrow><mn>1</mn></mrow></msub><mo>+</mo><msub><mrow><mi>x</mi></mrow><mrow><mn>2</mn></mrow></msub><mo>=</mo><mn>1</mn></mrow></mtd></mtr><mtr><mtd><mrow><msub><mrow><mi>h</mi></mrow><mrow><mn>1</mn></mrow></msub><mo>=</mo><mi>max</mi><mo>(</mo><mn>0</mn><mo>,</mo><msub><mrow><mi>x</mi></mrow><mrow><mn>1</mn></mrow></msub><mo>+</mo><msub><mrow><mi>x</mi></mrow><mrow><mn>2</mn></mrow></msub><mo>−</mo><mn>1</mn><mo>)</mo><mo>,</mo><mtext>  </mtext><msub><mrow><mi>h</mi></mrow><mrow><mn>2</mn></mrow></msub><mo>=</mo><mi>max</mi><mo>(</mo><mn>0</mn><mo>,</mo><msub><mrow><mi>x</mi></mrow><mrow><mn>1</mn></mrow></msub><mo>−</mo><msub><mrow><mi>x</mi></mrow><mrow><mn>2</mn></mrow></msub><mo>)</mo></mrow></mtd></mtr><mtr><mtd><mrow><msub><mrow><mi>min</mi></mrow><mrow><msub><mrow><mi>x</mi></mrow><mrow><mn>1</mn></mrow></msub><mo>,</mo><msub><mrow><mi>x</mi></mrow><mrow><mn>2</mn></mrow></msub></mrow></msub><mtext>  </mtext><msub><mrow><mi>x</mi></mrow><mrow><mn>1</mn></mrow></msub><mtext>   subject to   </mtext><msub><mrow><mi>h</mi></mrow><mrow><mn>1</mn></mrow></msub><mo>+</mo><msub><mrow><mi>h</mi></mrow><mrow><mn>2</mn></mrow></msub><mo>≥</mo><mn>.4</mn></mrow></mtd></mtr></mtable></math>

The equality gives <math><msub><mrow><mi>x</mi></mrow><mrow><mn>2</mn></mrow></msub></math> = 1 − <math><msub><mrow><mi>x</mi></mrow><mrow><mn>1</mn></mrow></msub></math>, hence <math><msub><mrow><mi>h</mi></mrow><mrow><mn>1</mn></mrow></msub></math> = 0 and <math><msub><mrow><mi>h</mi></mrow><mrow><mn>2</mn></mrow></msub></math> = max(0, 2<math><msub><mrow><mi>x</mi></mrow><mrow><mn>1</mn></mrow></msub></math> − 1). Satisfying <math><msub><mrow><mi>h</mi></mrow><mrow><mn>2</mn></mrow></msub></math> ≥ 0.4 requires the active branch with 2<math><msub><mrow><mi>x</mi></mrow><mrow><mn>1</mn></mrow></msub></math> − 1 ≥ 0.4.

The optimum is (<math><msub><mrow><mi>x</mi></mrow><mrow><mn>1</mn></mrow></msub></math>, <math><msub><mrow><mi>x</mi></mrow><mrow><mn>2</mn></mrow></msub></math>) = (0.7, 0.3), with outputs (<math><msub><mrow><mi>h</mi></mrow><mrow><mn>1</mn></mrow></msub></math>, <math><msub><mrow><mi>h</mi></mrow><mrow><mn>2</mn></mrow></msub></math>) = (0, 0.4). Compare the objective 0.7 with both MILP implementations.

<!-- lecture-page -->

## Calculating the two LP relaxation values

With box bounds [−1, 1], the first triangle permits <math><msub><mrow><mi>h</mi></mrow><mrow><mn>1</mn></mrow></msub></math> ≤ 0.5 even when <math><msub><mrow><mi>a</mi></mrow><mrow><mn>1</mn></mrow></msub></math> = 0. Thus <math><msub><mrow><mi>x</mi></mrow><mrow><mn>1</mn></mrow></msub></math> = 0, <math><msub><mrow><mi>x</mi></mrow><mrow><mn>2</mn></mrow></msub></math> = 1, <math><msub><mrow><mi>h</mi></mrow><mrow><mn>1</mn></mrow></msub></math> = 0.4, <math><msub><mrow><mi>h</mi></mrow><mrow><mn>2</mn></mrow></msub></math> = 0 is feasible for the original LP. Since <math><msub><mrow><mi>x</mi></mrow><mrow><mn>1</mn></mrow></msub></math> is nonnegative, its minimum is zero.

Incorporating <math><msub><mrow><mi>a</mi></mrow><mrow><mn>1</mn></mrow></msub></math> = 0 into the bounds forces <math><msub><mrow><mi>h</mi></mrow><mrow><mn>1</mn></mrow></msub></math> = 0. The second triangle has upper bound <math><msub><mrow><mi>h</mi></mrow><mrow><mn>2</mn></mrow></msub></math> ≤ <math><msub><mrow><mi>x</mi></mrow><mrow><mn>1</mn></mrow></msub></math>, which requires <math><msub><mrow><mi>x</mi></mrow><mrow><mn>1</mn></mrow></msub></math> ≥ 0.4.

The point <math><msub><mrow><mi>x</mi></mrow><mrow><mn>1</mn></mrow></msub></math> = 0.4, <math><msub><mrow><mi>x</mi></mrow><mrow><mn>2</mn></mrow></msub></math> = 0.6, <math><msub><mrow><mi>h</mi></mrow><mrow><mn>2</mn></mrow></msub></math> = 0.4 is feasible for the tightened LP, proving its optimum is 0.4. Its actual second ReLU output is zero, so it is not an integer-graph solution.

<!-- lecture-page -->

## An interval-propagation calculation

Consider a = 2<math><msub><mrow><mi>x</mi></mrow><mrow><mn>1</mn></mrow></msub></math> − 3<math><msub><mrow><mi>x</mi></mrow><mrow><mn>2</mn></mrow></msub></math> + 0.5, <math><msub><mrow><mi>x</mi></mrow><mrow><mn>1</mn></mrow></msub></math> ∈ [0, 1], and <math><msub><mrow><mi>x</mi></mrow><mrow><mn>2</mn></mrow></msub></math> ∈ [−1, 2]. Positive coefficients use the matching extreme; negative coefficients use the opposite extreme.

<math display="block"><mtable columnalign="left"><mtr><mtd><mrow><mi>L</mi><mo>=</mo><mn>2</mn><mo>·</mo><mn>0</mn><mo>−</mo><mn>3</mn><mo>·</mo><mn>2</mn><mo>+</mo><mn>.5</mn><mo>=</mo><mn>−5.5</mn></mrow></mtd></mtr><mtr><mtd><mrow><mi>U</mi><mo>=</mo><mn>2</mn><mo>·</mo><mn>1</mn><mo>−</mo><mn>3</mn><mo>·</mo><mo>(</mo><mn>−1</mn><mo>)</mo><mo>+</mo><mn>.5</mn><mo>=</mo><mn>5.5</mn></mrow></mtd></mtr></mtable></math>

The ReLU output interval is [0, 5.5]. Both endpoints are attainable over this box, but the calculation can become loose when an equality couples the inputs.

<!-- lecture-page -->

## Validity of LP-OBBT bounds

Let S be the exact network feasible set and P an LP relaxation with S ⊆ P. Minimization over a larger set cannot increase the optimum; maximization cannot decrease it.

<math display="block"><mtable columnalign="left"><mtr><mtd><mrow><msub><mrow><mi>min</mi></mrow><mrow><mi>P</mi></mrow></msub><mtext> </mtext><msub><mrow><mi>a</mi></mrow><mrow><mi>j</mi></mrow></msub><mo>≤</mo><msub><mrow><mi>min</mi></mrow><mrow><mi>S</mi></mrow></msub><mtext> </mtext><msub><mrow><mi>a</mi></mrow><mrow><mi>j</mi></mrow></msub></mrow></mtd></mtr><mtr><mtd><mrow><msub><mrow><mi>max</mi></mrow><mrow><mi>S</mi></mrow></msub><mtext> </mtext><msub><mrow><mi>a</mi></mrow><mrow><mi>j</mi></mrow></msub><mo>≤</mo><msub><mrow><mi>max</mi></mrow><mrow><mi>P</mi></mrow></msub><mtext> </mtext><msub><mrow><mi>a</mi></mrow><mrow><mi>j</mi></mrow></msub></mrow></mtd></mtr></mtable></math>

The two values over P are valid outward bounds for S. Intersect them with the existing interval bounds. The lab P omits product specifications, so these bounds remain reusable after specification changes within the same input box.

<!-- lecture-page -->

## Bound directions in unfinished optimization

A feasible point found while minimizing a gives an upper bound on its minimum. Using that value as a lower bound on a can cut off valid network points, so use a valid lower bound on the minimum.

When maximizing a, a valid upper bound on the maximum is required. A maximization incumbent alone does not supply that upper bound.

The implementation requires optimal termination for every LP and uses `best_objective_bound`. It adds outward padding of 1e-7 × (1 + abs(bound)); this numerical margin does not replace an exact-arithmetic proof.

<!-- lecture-page -->

## Fixing neurons and changing the domain

The pre-activation a = <math><msub><mrow><mi>x</mi></mrow><mrow><mn>1</mn></mrow></msub></math> + <math><msub><mrow><mi>x</mi></mrow><mrow><mn>2</mn></mrow></msub></math> − 1 changes sign over [0, 1] × [0, 1]. With <math><msub><mrow><mi>x</mi></mrow><mrow><mn>1</mn></mrow></msub></math> + <math><msub><mrow><mi>x</mi></mrow><mrow><mn>2</mn></mrow></msub></math> = 1, it is identically zero and h can be fixed to zero.

Removing that equality while retaining h = 0 makes the formulation incorrect. At (1, 1), for example, the actual h is 1.

Store the input domain, additional constraints used, and frozen-weight version with the bounds. Recompute bounds after refitting the model or expanding its domain.

<!-- lecture-page -->

## Scaled inputs and product specifications

<math display="block"><mtable columnalign="left"><mtr><mtd><mrow><msub><mrow><mi>x</mi></mrow><mrow><mn>1</mn></mrow></msub><mo>=</mo><mfrac><mrow><mi>T</mi><mo>−</mo><mn>310</mn></mrow><mrow><mn>40</mn></mrow></mfrac><mo>,</mo><mtext>  </mtext><msub><mrow><mi>x</mi></mrow><mrow><mn>2</mn></mrow></msub><mo>=</mo><mfrac><mrow><mi>τ</mi><mo>−</mo><mn>2</mn></mrow><mrow><mn>8</mn></mrow></mfrac></mrow></mtd></mtr><mtr><mtd><mrow><mi>T</mi><mo>=</mo><mn>310</mn><mo>+</mo><mn>40</mn><msub><mrow><mi>x</mi></mrow><mrow><mn>1</mn></mrow></msub><mo>,</mo><mtext>  </mtext><mi>τ</mi><mo>=</mo><mn>2</mn><mo>+</mo><mn>8</mn><msub><mrow><mi>x</mi></mrow><mrow><mn>2</mn></mrow></msub></mrow></mtd></mtr></mtable></math>

At T = 330 K and τ = 6 min, (<math><msub><mrow><mi>x</mi></mrow><mrow><mn>1</mn></mrow></msub></math>, <math><msub><mrow><mi>x</mi></mrow><mrow><mn>2</mn></mrow></msub></math>) = (0.5, 0.5). Pass input offsets [310, 2] and factors [40, 8] to OMLT `OffsetScaling`.

If an output were standardized as s = (B − 0.3)/0.1, B ≥ 0.38 would become s ≥ 0.8. The lab uses output factors of 1 and offsets of 0, so physical concentrations equal the OMLT outputs.

<!-- lecture-page -->

## Objective transformations and gap calculations

<math display="block"><mtable columnalign="left"><mtr><mtd><mrow><mi>J</mi><mo>=</mo><mi>τ</mi><mo>+</mo><mi>α</mi><mo>(</mo><mi>T</mi><mo>−</mo><mn>310</mn><mo>)</mo><mo>,</mo><mtext>  </mtext><mi>α</mi><mo>=</mo><mn>.02</mn><mtext> min/K</mtext></mrow></mtd></mtr><mtr><mtd><mrow><mi>J</mi><mo>=</mo><mn>2</mn><mo>+</mo><mn>8</mn><msub><mrow><mi>x</mi></mrow><mrow><mn>2</mn></mrow></msub><mo>+</mo><mn>.8</mn><msub><mrow><mi>x</mi></mrow><mrow><mn>1</mn></mrow></msub></mrow></mtd></mtr></mtable></math>

An incumbent J of 3.2 and lower bound of 2.8 give an absolute gap of 0.4 and a relative gap of 12.5%. After dropping the constant 2, the same values become 1.2 and 0.8, giving about 33.3%.

The optimizer and absolute gap are unchanged, but the relative gap changes. State the reported objective, its constant term, and the solver gap convention.

<!-- lecture-page -->

## Constructing OMLT input metadata

Set the scaling and input bounds for the two-input model. Positive factors map both input intervals to [0, 1].

```python
scaling = OffsetScaling(
    offset_inputs=[310., 2.], factor_inputs=[40., 8.],
    offset_outputs=[0., 0., 0.],
    factor_outputs=[1., 1., 1.])
definition = NetworkDefinition(
    scaling_object=scaling,
    scaled_input_bounds={0: (0., 1.), 1: (0., 1.)})
```

Pass weights and biases to each `DenseLayer`, then connect layers with `add_edge`. The lab weight axes are [input, output], with input order [temperature, residence time].

<!-- lecture-page -->

## A fixed-input validation procedure

1. Select corners and interior points of the input domain.
2. Compute outputs from the original network forward pass.
3. Fix the same inputs in the MILP and remove product specifications.
4. Check termination and solution availability before reading outputs.
5. Compare output differences, constraint residuals, and integrality residuals.

Retaining product specifications makes checks infeasible at inputs whose outputs miss those specifications. Distinguish this from a network-encoding error. The lab requires a maximum output difference below 1e-5 mol/L.

<!-- lecture-page -->

## Reference CSTR balances and rate laws

Assume steady state, isothermal operation, constant density, and consecutive first-order reactions A → B → C, with feed A at 1.2 mol/L.

<math display="block"><mtable columnalign="left"><mtr><mtd><mrow><msub><mrow><mi>C</mi></mrow><mrow><mi>A</mi></mrow></msub><mo>=</mo><mfrac><mrow><mn>1.2</mn></mrow><mrow><mn>1</mn><mo>+</mo><msub><mrow><mi>k</mi></mrow><mrow><mn>1</mn></mrow></msub><mi>τ</mi></mrow></mfrac></mrow></mtd></mtr><mtr><mtd><mrow><msub><mrow><mi>C</mi></mrow><mrow><mi>B</mi></mrow></msub><mo>=</mo><mfrac><mrow><msub><mrow><mi>k</mi></mrow><mrow><mn>1</mn></mrow></msub><mi>τ</mi><msub><mrow><mi>C</mi></mrow><mrow><mi>A</mi></mrow></msub></mrow><mrow><mn>1</mn><mo>+</mo><msub><mrow><mi>k</mi></mrow><mrow><mn>2</mn></mrow></msub><mi>τ</mi></mrow></mfrac><mo>,</mo><mtext>  </mtext><msub><mrow><mi>C</mi></mrow><mrow><mi>C</mi></mrow></msub><mo>=</mo><msub><mrow><mi>k</mi></mrow><mrow><mn>2</mn></mrow></msub><mi>τ</mi><msub><mrow><mi>C</mi></mrow><mrow><mi>B</mi></mrow></msub></mrow></mtd></mtr></mtable></math>

At 330 K, <math><msub><mrow><mi>k</mi></mrow><mrow><mn>1</mn></mrow></msub></math> = 0.2 and <math><msub><mrow><mi>k</mi></mrow><mrow><mn>2</mn></mrow></msub></math> = 0.1 per minute. The next page defines temperature dependence with educational Arrhenius parameters. Evaluate these reference balances independently of the network approximation.

<!-- lecture-page -->

## Temperature dependence and data generation

<math display="block"><mtable columnalign="left"><mtr><mtd><mrow><msub><mrow><mi>k</mi></mrow><mrow><mi>i</mi></mrow></msub><mo>(</mo><mi>T</mi><mo>)</mo><mo>=</mo><msub><mrow><mi>k</mi></mrow><mrow><mi>i</mi></mrow></msub><mo>(</mo><mn>330</mn><mo>)</mo><mi>exp</mi><mo>(</mo><mfrac><mrow><msub><mrow><mi>E</mi></mrow><mrow><mi>i</mi></mrow></msub></mrow><mrow><mi>R</mi></mrow></mfrac><mo>(</mo><mfrac><mrow><mn>1</mn></mrow><mrow><mn>330</mn></mrow></mfrac><mo>−</mo><mfrac><mrow><mn>1</mn></mrow><mrow><mi>T</mi></mrow></mfrac><mo>)</mo><mo>)</mo></mrow></mtd></mtr></mtable></math>

Activation energies are <math><msub><mrow><mi>E</mi></mrow><mrow><mn>1</mn></mrow></msub></math> = 40,000 and <math><msub><mrow><mi>E</mi></mrow><mrow><mn>2</mn></mrow></msub></math> = 50,000 J/mol, with R = 8.314 J/(mol·K). These are specified example parameters rather than estimates for a real chemical system.

Generate 1,200 uniform training inputs over the box. The training seed is 61; independent checks and test generation use seed 87. Test data are not used to fit the coefficients.

<!-- lecture-page -->

## Training settings and frozen coefficients

The architecture is 2 → 12 → 12 → 3, with ReLU after the first two affine layers and a linear output layer. The loss is mean squared error across three concentration outputs in physical units.

Run 6,000 full-batch Adam updates: a learning rate of 0.006 for the first 3,999 updates, then 0.002, with <math><msub><mrow><mi>β</mi></mrow><mrow><mn>1</mn></mrow></msub></math> = 0.9, <math><msub><mrow><mi>β</mi></mrow><mrow><mn>2</mn></mrow></msub></math> = 0.999, and ε = 1e-8.

The default coefficients are in `frozen_cstr_network.json`. `--refit` saves a separate model in the specified output directory without overwriting the default. Keep comparison results with the coefficient file used.

<!-- lecture-page -->

## Reading results for the same optimization problem

| Formulation | LP lower bound | MILP optimum | Binaries |
| --- | --- | --- | --- |
| loose | 2.0000 | 3.1656 | 24 |
| interval | 2.0000 | 3.1656 | 22 |
| LP-OBBT | 2.5215 | 3.1656 | 19 |

OMLT returns the same MILP optimum. Inputs, weights, product specifications, and objective are identical across all four runs.

Each LP lower bound is the optimum of a separately solved continuous relaxation. It can differ from bounds reported after solver presolve and cuts.

<!-- lecture-page -->

## Timing scope and reuse of bounds

| Formulation | Bounds [s] | Build [s] | MILP [s] | Total [s] |
| --- | --- | --- | --- | --- |
| loose | 0.0001 | 0.0016 | 0.3107 | 0.3125 |
| interval | 0.0001 | 0.0016 | 0.1539 | 0.1556 |
| LP-OBBT | 0.1132 | 0.0016 | 0.0955 | 0.2104 |

Total is bounds plus model construction plus MILP solution. It excludes the separately solved LP relaxation, prediction checks, and training.

Reusing bounds for a fixed model and domain can spread preprocessing cost across solves. Repeated comparisons should use the same hardware, threads, and limits, reporting medians and variability.

<!-- lecture-page -->

## Exercise: scaling and gaps

Scale T = 340 K and τ = 4 min, then calculate J. Next calculate absolute and relative gaps for incumbent 5.0 and lower bound 4.5.

Check: (<math><msub><mrow><mi>x</mi></mrow><mrow><mn>1</mn></mrow></msub></math>, <math><msub><mrow><mi>x</mi></mrow><mrow><mn>2</mn></mrow></msub></math>) = (0.75, 0.25), and J = 4 + 0.02 × 30 = 4.6. The gaps are 0.5 and 10%.

What should be reported if only lower bound 4.5 is available? Check: report the valid lower bound and absence of an incumbent; leave the relative gap and selected inputs unavailable.

<!-- lecture-page -->

## Exercise: bounds and reference-process checks

After computing bounds over the input box, the temperature upper limit is raised from 350 K to 360 K. May the old bounds be retained? Check: recompute bounds or establish their validity over the expanded domain.

At the selected input, network B is 0.380000 and reference CSTR B is 0.371157 mol/L. Calculate the specification margin. Check: reference minus lower limit is -0.008843 mol/L, which is negative.

Reducing the solver gap alone cannot correct this violation. The predictor or selected conditions require reconsideration.

<!-- lecture-page -->

## Primary sources and lab files

[Ceccon et al., OMLT: Optimization & Machine Learning Toolkit, JMLR 23(349), 2022](https://jmlr.org/papers/v23/22-0277.html) · [Official quick-start](https://omlt.readthedocs.io/en/stable/quickstart.html)

[Anderson et al., Strong mixed-integer programming formulations for trained neural networks, Mathematical Programming, 2020](https://arxiv.org/abs/1811.01988)

[HiGHS and its MIT license](https://highs.dev/) · [Pyomo HiGHS interface](https://pyomo.readthedocs.io/en/stable/api/pyomo.contrib.appsi.solvers.highs.Highs.html)

`results.json` records termination and checks, `comparison.csv` contains the comparison table, and `frozen_network.json` stores the coefficients used. The verified environment is Python 3.12.14, NumPy 2.5.4, Pyomo 6.10.1, OMLT 1.2.2, HiGHS 1.15.1.

[Lecture](/courses/surrogate-models/week-06/) · [Lab ZIP](/assets/courses/surrogate-models/week-06/week06-lab.zip)

<!-- ko -->

## 반응기 계산을 검토하는 순서

제품 규격을 만족하는 반응기 조건을 계산했을 때, 최적화가 얼마나 진행됐는지와 공정 예측이 맞는지를 각각 확인합니다.

두 뉴런 예제의 MILP·LP 해를 직접 유도한 뒤 bounds와 scaling을 계산하고, OMLT 연결과 CSTR 결과를 확인합니다.

계산에 필요한 신경망 계수와 실행 결과는 [실습 ZIP](/assets/courses/surrogate-models/week-06/week06-lab.zip)에 있습니다. LP와 MILP는 모두 오픈소스 HiGHS로 풉니다.

<!-- lecture-page -->

## Big-M에서 삼각형 완화 유도

L < 0 < U이고 z ∈ [0, 1]이라고 놓습니다. h ≤ Uz와 h ≤ a − L(1 − z)를 z에 대해 정리합니다.

<math display="block"><mtable columnalign="left"><mtr><mtd><mrow><mfrac><mrow><mi>h</mi></mrow><mrow><mi>U</mi></mrow></mfrac><mo>≤</mo><mi>z</mi><mo>≤</mo><mfrac><mrow><mi>h</mi><mo>−</mo><mi>a</mi><mo>+</mo><mi>L</mi></mrow><mrow><mi>L</mi></mrow></mfrac></mrow></mtd></mtr><mtr><mtd><mrow><mi>h</mi><mo>(</mo><mi>U</mi><mo>−</mo><mi>L</mi><mo>)</mo><mo>≤</mo><mi>U</mi><mo>(</mo><mi>a</mi><mo>−</mo><mi>L</mi><mo>)</mo></mrow></mtd></mtr></mtable></math>

L이 음수이므로 나눌 때 부등호가 뒤집힙니다. 여기에 h ≥ 0과 h ≥ a를 유지하면 강의의 삼각형 완화가 됩니다. 유효한 a의 구간도 유지합니다.

<!-- lecture-page -->

## 두 뉴런 예제의 정수해 유도

<math display="block"><mtable columnalign="left"><mtr><mtd><mrow><mn>0</mn><mo>≤</mo><msub><mrow><mi>x</mi></mrow><mrow><mn>1</mn></mrow></msub><mo>,</mo><msub><mrow><mi>x</mi></mrow><mrow><mn>2</mn></mrow></msub><mo>≤</mo><mn>1</mn><mo>,</mo><mtext>  </mtext><msub><mrow><mi>x</mi></mrow><mrow><mn>1</mn></mrow></msub><mo>+</mo><msub><mrow><mi>x</mi></mrow><mrow><mn>2</mn></mrow></msub><mo>=</mo><mn>1</mn></mrow></mtd></mtr><mtr><mtd><mrow><msub><mrow><mi>h</mi></mrow><mrow><mn>1</mn></mrow></msub><mo>=</mo><mi>max</mi><mo>(</mo><mn>0</mn><mo>,</mo><msub><mrow><mi>x</mi></mrow><mrow><mn>1</mn></mrow></msub><mo>+</mo><msub><mrow><mi>x</mi></mrow><mrow><mn>2</mn></mrow></msub><mo>−</mo><mn>1</mn><mo>)</mo><mo>,</mo><mtext>  </mtext><msub><mrow><mi>h</mi></mrow><mrow><mn>2</mn></mrow></msub><mo>=</mo><mi>max</mi><mo>(</mo><mn>0</mn><mo>,</mo><msub><mrow><mi>x</mi></mrow><mrow><mn>1</mn></mrow></msub><mo>−</mo><msub><mrow><mi>x</mi></mrow><mrow><mn>2</mn></mrow></msub><mo>)</mo></mrow></mtd></mtr><mtr><mtd><mrow><msub><mrow><mi>min</mi></mrow><mrow><msub><mrow><mi>x</mi></mrow><mrow><mn>1</mn></mrow></msub><mo>,</mo><msub><mrow><mi>x</mi></mrow><mrow><mn>2</mn></mrow></msub></mrow></msub><mtext>  </mtext><msub><mrow><mi>x</mi></mrow><mrow><mn>1</mn></mrow></msub><mtext>   subject to   </mtext><msub><mrow><mi>h</mi></mrow><mrow><mn>1</mn></mrow></msub><mo>+</mo><msub><mrow><mi>h</mi></mrow><mrow><mn>2</mn></mrow></msub><mo>≥</mo><mn>.4</mn></mrow></mtd></mtr></mtable></math>

입력 등식에서 <math><msub><mrow><mi>x</mi></mrow><mrow><mn>2</mn></mrow></msub></math> = 1 − <math><msub><mrow><mi>x</mi></mrow><mrow><mn>1</mn></mrow></msub></math>이므로 <math><msub><mrow><mi>h</mi></mrow><mrow><mn>1</mn></mrow></msub></math> = 0이고 <math><msub><mrow><mi>h</mi></mrow><mrow><mn>2</mn></mrow></msub></math> = max(0, 2<math><msub><mrow><mi>x</mi></mrow><mrow><mn>1</mn></mrow></msub></math> − 1)입니다. <math><msub><mrow><mi>h</mi></mrow><mrow><mn>2</mn></mrow></msub></math> ≥ 0.4를 만족하려면 활성 분기에서 2<math><msub><mrow><mi>x</mi></mrow><mrow><mn>1</mn></mrow></msub></math> − 1 ≥ 0.4여야 합니다.

최적점은 (<math><msub><mrow><mi>x</mi></mrow><mrow><mn>1</mn></mrow></msub></math>, <math><msub><mrow><mi>x</mi></mrow><mrow><mn>2</mn></mrow></msub></math>) = (0.7, 0.3), 출력은 (<math><msub><mrow><mi>h</mi></mrow><mrow><mn>1</mn></mrow></msub></math>, <math><msub><mrow><mi>h</mi></mrow><mrow><mn>2</mn></mrow></msub></math>) = (0, 0.4)입니다. 목적값 0.7을 두 MILP 구현과 대조합니다.

<!-- lecture-page -->

## 두 LP 완화의 목적값 계산

구간 bounds [−1, 1]을 사용한 첫 뉴런의 삼각형은 <math><msub><mrow><mi>a</mi></mrow><mrow><mn>1</mn></mrow></msub></math> = 0에서도 <math><msub><mrow><mi>h</mi></mrow><mrow><mn>1</mn></mrow></msub></math> ≤ 0.5를 허용합니다. 따라서 <math><msub><mrow><mi>x</mi></mrow><mrow><mn>1</mn></mrow></msub></math> = 0, <math><msub><mrow><mi>x</mi></mrow><mrow><mn>2</mn></mrow></msub></math> = 1, <math><msub><mrow><mi>h</mi></mrow><mrow><mn>1</mn></mrow></msub></math> = 0.4, <math><msub><mrow><mi>h</mi></mrow><mrow><mn>2</mn></mrow></msub></math> = 0은 원래 LP의 가능점입니다. 비음수 <math><msub><mrow><mi>x</mi></mrow><mrow><mn>1</mn></mrow></msub></math>을 최소화하므로 최적값은 0입니다.

등식에서 얻은 <math><msub><mrow><mi>a</mi></mrow><mrow><mn>1</mn></mrow></msub></math> = 0을 bounds에 반영하면 <math><msub><mrow><mi>h</mi></mrow><mrow><mn>1</mn></mrow></msub></math> = 0입니다. 두 번째 뉴런의 삼각형 상한은 <math><msub><mrow><mi>h</mi></mrow><mrow><mn>2</mn></mrow></msub></math> ≤ <math><msub><mrow><mi>x</mi></mrow><mrow><mn>1</mn></mrow></msub></math>이므로 <math><msub><mrow><mi>x</mi></mrow><mrow><mn>1</mn></mrow></msub></math> ≥ 0.4가 필요합니다.

이때 <math><msub><mrow><mi>x</mi></mrow><mrow><mn>1</mn></mrow></msub></math> = 0.4, <math><msub><mrow><mi>x</mi></mrow><mrow><mn>2</mn></mrow></msub></math> = 0.6, <math><msub><mrow><mi>h</mi></mrow><mrow><mn>2</mn></mrow></msub></math> = 0.4인 점은 강화한 LP의 가능점이므로 최적값은 0.4입니다. 이 점의 실제 ReLU 출력 <math><msub><mrow><mi>h</mi></mrow><mrow><mn>2</mn></mrow></msub></math>는 0이라 정수해가 될 수 없습니다.

<!-- lecture-page -->

## 구간 전파 손계산

a = 2<math><msub><mrow><mi>x</mi></mrow><mrow><mn>1</mn></mrow></msub></math> − 3<math><msub><mrow><mi>x</mi></mrow><mrow><mn>2</mn></mrow></msub></math> + 0.5, <math><msub><mrow><mi>x</mi></mrow><mrow><mn>1</mn></mrow></msub></math> ∈ [0, 1], <math><msub><mrow><mi>x</mi></mrow><mrow><mn>2</mn></mrow></msub></math> ∈ [−1, 2]를 계산합니다. 양의 계수는 같은 방향의 극값을, 음의 계수는 반대쪽 극값을 선택합니다.

<math display="block"><mtable columnalign="left"><mtr><mtd><mrow><mi>L</mi><mo>=</mo><mn>2</mn><mo>·</mo><mn>0</mn><mo>−</mo><mn>3</mn><mo>·</mo><mn>2</mn><mo>+</mo><mn>.5</mn><mo>=</mo><mn>−5.5</mn></mrow></mtd></mtr><mtr><mtd><mrow><mi>U</mi><mo>=</mo><mn>2</mn><mo>·</mo><mn>1</mn><mo>−</mo><mn>3</mn><mo>·</mo><mo>(</mo><mn>−1</mn><mo>)</mo><mo>+</mo><mn>.5</mn><mo>=</mo><mn>5.5</mn></mrow></mtd></mtr></mtable></math>

ReLU 출력 범위는 [0, 5.5]입니다. 이 입력 상자에서는 양쪽 끝점이 실제로 가능하지만 입력 간 등식이 추가되면 같은 계산이 느슨해질 수 있습니다.

<!-- lecture-page -->

## LP-OBBT bounds의 유효성

S를 정확한 신경망의 가능집합, P를 S ⊆ P인 LP 완화라고 놓습니다. 더 큰 집합에서 최소화하면 값이 작아지거나 같고, 최대화하면 커지거나 같습니다.

<math display="block"><mtable columnalign="left"><mtr><mtd><mrow><msub><mrow><mi>min</mi></mrow><mrow><mi>P</mi></mrow></msub><mtext> </mtext><msub><mrow><mi>a</mi></mrow><mrow><mi>j</mi></mrow></msub><mo>≤</mo><msub><mrow><mi>min</mi></mrow><mrow><mi>S</mi></mrow></msub><mtext> </mtext><msub><mrow><mi>a</mi></mrow><mrow><mi>j</mi></mrow></msub></mrow></mtd></mtr><mtr><mtd><mrow><msub><mrow><mi>max</mi></mrow><mrow><mi>S</mi></mrow></msub><mtext> </mtext><msub><mrow><mi>a</mi></mrow><mrow><mi>j</mi></mrow></msub><mo>≤</mo><msub><mrow><mi>max</mi></mrow><mrow><mi>P</mi></mrow></msub><mtext> </mtext><msub><mrow><mi>a</mi></mrow><mrow><mi>j</mi></mrow></msub></mrow></mtd></mtr></mtable></math>

따라서 P에서 얻은 두 값은 S의 유효한 바깥 bounds입니다. 기존 구간 bounds와 교집합을 취해 적용합니다. 실습의 P에는 제품 규격이 들어 있지 않아 규격 변경에도 같은 입력 상자에서 사용할 수 있습니다.

<!-- lecture-page -->

## 미완료 bound 계산의 방향

a를 최소화하는 계산에서 찾은 가능점 값은 실제 최소값의 상한입니다. 이를 a의 하한으로 사용하면 유효한 신경망 점을 잘라낼 수 있으므로 최소값에 대한 유효한 하한을 사용해야 합니다.

a를 최대화할 때는 반대로 최대값의 유효한 상한이 필요합니다. 최대화 가능점 값만으로 상한을 만들면 안 됩니다.

제공 구현은 각 LP의 optimal 종료를 요구하고 `best_objective_bound`를 사용합니다. 바깥쪽으로 1e-7 × (1 + abs(bound))만큼 여유를 두지만, 이 수치 여유가 정확 산술의 증명을 대신하지는 않습니다.

<!-- lecture-page -->

## 뉴런 고정과 영역 변경

a = <math><msub><mrow><mi>x</mi></mrow><mrow><mn>1</mn></mrow></msub></math> + <math><msub><mrow><mi>x</mi></mrow><mrow><mn>2</mn></mrow></msub></math> − 1은 입력 상자 [0, 1] × [0, 1]에서 부호가 바뀝니다. 여기에 <math><msub><mrow><mi>x</mi></mrow><mrow><mn>1</mn></mrow></msub></math> + <math><msub><mrow><mi>x</mi></mrow><mrow><mn>2</mn></mrow></msub></math> = 1이 있으면 항상 0이므로 h = 0으로 고정합니다.

이 등식을 제거하면서 고정된 h = 0을 유지하면 정식화가 틀립니다. 예를 들어 (1, 1)에서 실제 h는 1입니다.

Bounds 파일에는 입력 범위, 적용한 추가 제약, 고정 가중치의 버전을 함께 보관합니다. 새 모델을 학습하거나 영역을 늘리면 bounds를 다시 계산합니다.

<!-- lecture-page -->

## Scaling된 입력과 제품 규격

<math display="block"><mtable columnalign="left"><mtr><mtd><mrow><msub><mrow><mi>x</mi></mrow><mrow><mn>1</mn></mrow></msub><mo>=</mo><mfrac><mrow><mi>T</mi><mo>−</mo><mn>310</mn></mrow><mrow><mn>40</mn></mrow></mfrac><mo>,</mo><mtext>  </mtext><msub><mrow><mi>x</mi></mrow><mrow><mn>2</mn></mrow></msub><mo>=</mo><mfrac><mrow><mi>τ</mi><mo>−</mo><mn>2</mn></mrow><mrow><mn>8</mn></mrow></mfrac></mrow></mtd></mtr><mtr><mtd><mrow><mi>T</mi><mo>=</mo><mn>310</mn><mo>+</mo><mn>40</mn><msub><mrow><mi>x</mi></mrow><mrow><mn>1</mn></mrow></msub><mo>,</mo><mtext>  </mtext><mi>τ</mi><mo>=</mo><mn>2</mn><mo>+</mo><mn>8</mn><msub><mrow><mi>x</mi></mrow><mrow><mn>2</mn></mrow></msub></mrow></mtd></mtr></mtable></math>

T = 330 K, τ = 6 min이면 (<math><msub><mrow><mi>x</mi></mrow><mrow><mn>1</mn></mrow></msub></math>, <math><msub><mrow><mi>x</mi></mrow><mrow><mn>2</mn></mrow></msub></math>) = (0.5, 0.5)입니다. OMLT의 `OffsetScaling`에 입력 offset [310, 2], factor [40, 8]을 전달합니다.

출력이 s = (B − 0.3)/0.1로 표준화되어 있다면 B ≥ 0.38은 s ≥ 0.8입니다. 실습은 출력 factor 1과 offset 0을 사용하므로 물리 농도와 OMLT 출력이 같습니다.

<!-- lecture-page -->

## 목적함수 변환과 gap 계산

<math display="block"><mtable columnalign="left"><mtr><mtd><mrow><mi>J</mi><mo>=</mo><mi>τ</mi><mo>+</mo><mi>α</mi><mo>(</mo><mi>T</mi><mo>−</mo><mn>310</mn><mo>)</mo><mo>,</mo><mtext>  </mtext><mi>α</mi><mo>=</mo><mn>.02</mn><mtext> min/K</mtext></mrow></mtd></mtr><mtr><mtd><mrow><mi>J</mi><mo>=</mo><mn>2</mn><mo>+</mo><mn>8</mn><msub><mrow><mi>x</mi></mrow><mrow><mn>2</mn></mrow></msub><mo>+</mo><mn>.8</mn><msub><mrow><mi>x</mi></mrow><mrow><mn>1</mn></mrow></msub></mrow></mtd></mtr></mtable></math>

J의 incumbent가 3.2, 하한이 2.8이면 절대 gap은 0.4이고 상대 gap은 12.5%입니다. 상수 2를 뺀 식에서는 같은 두 값이 1.2와 0.8이 되어 상대 gap은 약 33.3%입니다.

최적 입력과 절대 gap은 같지만 상대 gap은 달라집니다. 보고하는 목적함수, 상수항, solver의 gap 정의를 같이 적습니다.

<!-- lecture-page -->

## OMLT의 입력 정보 구성

2입력 모델의 scaling과 입력 bounds를 설정합니다. 양의 factor로 변환한 입력 구간은 둘 다 [0, 1]입니다.

```python
scaling = OffsetScaling(
    offset_inputs=[310., 2.], factor_inputs=[40., 8.],
    offset_outputs=[0., 0., 0.],
    factor_outputs=[1., 1., 1.])
definition = NetworkDefinition(
    scaling_object=scaling,
    scaled_input_bounds={0: (0., 1.), 1: (0., 1.)})
```

각 `DenseLayer`에 가중치와 bias를 넣고 `add_edge`로 연결합니다. 실습 배열의 가중치 축은 [입력, 출력]이며 입력 순서는 [온도, 체류시간]입니다.

<!-- lecture-page -->

## 고정 입력 검사 절차

1. 입력 영역의 모서리와 내부점을 선택합니다.
2. 원래 신경망의 forward 출력을 계산합니다.
3. 같은 입력을 MILP에 고정하고 제품 규격을 제외합니다.
4. 가능해 존재와 종료 상태를 확인한 뒤 출력을 읽습니다.
5. 출력 차이, 등식·부등식 잔차와 정수성 잔차를 비교합니다.

제품 규격을 남기면 출력이 규격을 벗어나는 입력에서 검사 문제가 infeasible이 됩니다. 이는 신경망 표현 오류와 구분해야 합니다. 실습은 최대 출력 차이 1e-5 mol/L 미만을 요구합니다.

<!-- lecture-page -->

## 기준 CSTR의 수지와 속도식

정상상태·등온·일정 밀도에서 A → B → C의 연속 1차 반응을 가정하고 유입 A 농도를 1.2 mol/L로 둡니다.

<math display="block"><mtable columnalign="left"><mtr><mtd><mrow><msub><mrow><mi>C</mi></mrow><mrow><mi>A</mi></mrow></msub><mo>=</mo><mfrac><mrow><mn>1.2</mn></mrow><mrow><mn>1</mn><mo>+</mo><msub><mrow><mi>k</mi></mrow><mrow><mn>1</mn></mrow></msub><mi>τ</mi></mrow></mfrac></mrow></mtd></mtr><mtr><mtd><mrow><msub><mrow><mi>C</mi></mrow><mrow><mi>B</mi></mrow></msub><mo>=</mo><mfrac><mrow><msub><mrow><mi>k</mi></mrow><mrow><mn>1</mn></mrow></msub><mi>τ</mi><msub><mrow><mi>C</mi></mrow><mrow><mi>A</mi></mrow></msub></mrow><mrow><mn>1</mn><mo>+</mo><msub><mrow><mi>k</mi></mrow><mrow><mn>2</mn></mrow></msub><mi>τ</mi></mrow></mfrac><mo>,</mo><mtext>  </mtext><msub><mrow><mi>C</mi></mrow><mrow><mi>C</mi></mrow></msub><mo>=</mo><msub><mrow><mi>k</mi></mrow><mrow><mn>2</mn></mrow></msub><mi>τ</mi><msub><mrow><mi>C</mi></mrow><mrow><mi>B</mi></mrow></msub></mrow></mtd></mtr></mtable></math>

330 K에서 <math><msub><mrow><mi>k</mi></mrow><mrow><mn>1</mn></mrow></msub></math> = 0.2, <math><msub><mrow><mi>k</mi></mrow><mrow><mn>2</mn></mrow></msub></math> = 0.1 /min입니다. 온도 의존성은 다음 페이지의 교육용 Arrhenius 계수로 정합니다. 이 수지는 기준 모델이며 신경망 근사와 별도로 계산합니다.

<!-- lecture-page -->

## 온도 의존성과 데이터 생성

<math display="block"><mtable columnalign="left"><mtr><mtd><mrow><msub><mrow><mi>k</mi></mrow><mrow><mi>i</mi></mrow></msub><mo>(</mo><mi>T</mi><mo>)</mo><mo>=</mo><msub><mrow><mi>k</mi></mrow><mrow><mi>i</mi></mrow></msub><mo>(</mo><mn>330</mn><mo>)</mo><mi>exp</mi><mo>(</mo><mfrac><mrow><msub><mrow><mi>E</mi></mrow><mrow><mi>i</mi></mrow></msub></mrow><mrow><mi>R</mi></mrow></mfrac><mo>(</mo><mfrac><mrow><mn>1</mn></mrow><mrow><mn>330</mn></mrow></mfrac><mo>−</mo><mfrac><mrow><mn>1</mn></mrow><mrow><mi>T</mi></mrow></mfrac><mo>)</mo><mo>)</mo></mrow></mtd></mtr></mtable></math>

활성화에너지는 <math><msub><mrow><mi>E</mi></mrow><mrow><mn>1</mn></mrow></msub></math> = 40,000, <math><msub><mrow><mi>E</mi></mrow><mrow><mn>2</mn></mrow></msub></math> = 50,000 J/mol, 기체상수 R = 8.314 J/(mol·K)입니다. 이 값은 예제에 지정한 매개변수로, 실제 물질에서 추정하지 않았습니다.

입력 상자에서 균일 난수로 학습점 1,200개를 생성합니다. 학습 seed는 61이고, 독립 검사·test 생성에는 seed 87을 사용합니다. 구현은 test 데이터를 계수 적합에 사용하지 않습니다.

<!-- lecture-page -->

## 학습 설정과 고정 계수 사용

2 → 12 → 12 → 3 구조에서 앞의 두 affine layer 뒤에 ReLU를 적용하고 마지막 층은 선형으로 둡니다. Loss는 물리 단위로 나타낸 세 농도 출력의 평균제곱오차입니다.

Full-batch Adam을 6,000회 적용하고 학습률은 처음 3,999회 0.006, 나머지는 0.002입니다. <math><msub><mrow><mi>β</mi></mrow><mrow><mn>1</mn></mrow></msub></math> = 0.9, <math><msub><mrow><mi>β</mi></mrow><mrow><mn>2</mn></mrow></msub></math> = 0.999, ε = 1e-8을 사용합니다.

기본 실행은 `frozen_cstr_network.json`의 계수를 사용합니다. `--refit` 결과는 지정한 출력 폴더의 별도 파일로 저장되며 기본 계수를 덮어쓰지 않습니다. 비교 결과는 사용한 계수 파일과 함께 보관합니다.

<!-- lecture-page -->

## 동일 문제의 계산 결과 읽기

| 정식화 | LP 하한 | MILP 최적값 | 이진변수 |
| --- | --- | --- | --- |
| loose | 2.0000 | 3.1656 | 24 |
| interval | 2.0000 | 3.1656 | 22 |
| LP-OBBT | 2.5215 | 3.1656 | 19 |

OMLT도 같은 MILP 최적값을 반환했습니다. 입력·가중치·제품 규격·목적함수는 네 실행에서 같습니다.

표의 LP 하한은 이진변수를 연속으로 바꾼 별도 문제의 최적값입니다. Solver가 presolve와 cut을 적용한 뒤 보고하는 bound와는 다를 수 있습니다.

<!-- lecture-page -->

## 계산 시간의 측정 범위와 bounds 재사용

| 정식화 | Bounds [s] | 구성 [s] | MILP [s] | 합계 [s] |
| --- | --- | --- | --- | --- |
| loose | 0.0001 | 0.0016 | 0.3107 | 0.3125 |
| interval | 0.0001 | 0.0016 | 0.1539 | 0.1556 |
| LP-OBBT | 0.1132 | 0.0016 | 0.0955 | 0.2104 |

합계는 bounds, 모델 구성과 MILP 풀이의 합입니다. 별도로 측정한 LP 완화, 예측 검증, 학습 시간은 포함하지 않습니다.

고정 모델과 영역에서 bounds를 재사용하면 여러 풀이에 전처리 비용을 나눌 수 있습니다. 반복 비교에서는 같은 장비·스레드·시간 제한을 사용하고 중앙값과 변동을 기록합니다.

<!-- lecture-page -->

## 연습: scaling과 gap

T = 340 K, τ = 4 min을 scaled 입력으로 바꾸고 목적함수 J를 계산합니다. 이어서 incumbent 5.0, 하한 4.5의 절대·상대 gap을 계산합니다.

확인: (<math><msub><mrow><mi>x</mi></mrow><mrow><mn>1</mn></mrow></msub></math>, <math><msub><mrow><mi>x</mi></mrow><mrow><mn>2</mn></mrow></msub></math>) = (0.75, 0.25), J = 4 + 0.02 × 30 = 4.6입니다. Gap은 0.5와 10%입니다.

Incumbent 없이 하한 4.5만 있으면 무엇을 보고할까요? 확인: 유효한 하한과 가능해 미확보를 보고하며, 상대 gap과 선택 입력은 비워둡니다.

<!-- lecture-page -->

## 연습: bounds와 기준 공정 검사

입력 상자에서 계산한 bounds를 사용하다가 온도 상한을 350 K에서 360 K로 늘렸습니다. 기존 bounds를 그대로 적용해도 될까요? 확인: 확장된 영역에서 bounds를 다시 계산하거나 유효성을 증명해야 합니다.

선택 입력의 신경망 B는 0.380000, 기준 CSTR B는 0.371157 mol/L입니다. 규격 여유를 계산합니다. 확인: 기준값에서 하한을 뺀 여유는 -0.008843 mol/L로 음수입니다.

이 경우 solver gap을 줄이는 것만으로 규격 위반을 고칠 수는 없습니다. 예측 모델 또는 선택 조건을 다시 검토해야 합니다.

<!-- lecture-page -->

## 원문과 실습 파일

[OMLT 논문: Ceccon 등, JMLR 23(349), 2022](https://jmlr.org/papers/v23/22-0277.html) · [공식 사용 예제](https://omlt.readthedocs.io/en/stable/quickstart.html)

[Anderson 등, Strong mixed-integer programming formulations for trained neural networks, Mathematical Programming, 2020](https://arxiv.org/abs/1811.01988)

[HiGHS 공식 사이트와 MIT 라이선스 안내](https://highs.dev/) · [Pyomo의 HiGHS 인터페이스](https://pyomo.readthedocs.io/en/stable/api/pyomo.contrib.appsi.solvers.highs.Highs.html)

`results.json`은 종료 상태와 검증값, `comparison.csv`는 비교표, `frozen_network.json`은 해당 실행의 계수를 담습니다. 검증 환경은 Python 3.12.14, NumPy 2.5.4, Pyomo 6.10.1, OMLT 1.2.2, HiGHS 1.15.1입니다.

[강의노트](/courses/surrogate-models/week-06/) · [실습 ZIP](/assets/courses/surrogate-models/week-06/week06-lab.zip)
