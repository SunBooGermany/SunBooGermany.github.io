---
layout: "course-note"
title: "Week 5: From a Predictor to an Optimization Formulation"
title_ko: "5주차: 예측 모델을 최적화 문제에 넣기"
description: "Frozen ReLU models, valid bounds, and verified optimization formulations."
description_ko: "고정 ReLU 모델, 유효한 bounds와 최적화 정식화를 다룹니다."
material_label: "Week 5"
material_label_ko: "5주차"
updated: "2026-10-25"
permalink: "/courses/surrogate-models/week-05/"
pdf_en: "/assets/courses/surrogate-models/week-05-en.pdf"
pdf_ko: "/assets/courses/surrogate-models/week-05-ko.pdf"
course_id: "surrogate-models"
notebook: "/assets/courses/surrogate-models/week-05/week05_lab.ipynb"
lab_script: "/assets/courses/surrogate-models/week-05/week05_lab.py"
reading_note: "/courses/surrogate-models/week-05-reading/"
reading_pdf_en: "/assets/courses/surrogate-models/week-05-reading-en.pdf"
reading_pdf_ko: "/assets/courses/surrogate-models/week-05-reading-ko.pdf"
---

## The smallest reactor that meets product specifications

Product B must reach 0.40 mol/L while byproduct C stays below 0.25 mol/L. At fixed flow, how small can the reactor be?

<figure><img src="/assets/courses/surrogate-models/week-05/motivation-en.svg" alt="Reactor volume and product specifications at fixed flow" /></figure>

<!-- lecture-page -->

## Product specifications and reactor volume minimization

Given a residence time, the network predicts outlet concentrations. Design asks for a residence time that satisfies those concentration requirements.

Longer residence converts A to B, but also converts B to C. Maximizing B and minimizing volume are different objectives.

This week we formulate that choice and express a frozen ReLU computation using linear constraints and binary variables.

<!-- lecture-page -->

## Learning objectives for optimization formulation

1. Separate decisions, fixed context, and predicted outputs; write the objective and constraints.
2. Prove the Big-M representation of one ReLU by examining both branches.
3. Derive valid pre-activation bounds from the input domain.
4. Compare a hand-built MILP with the forward pass at identical inputs.

Submit the formulation, verification results, and interpretation of the solution.

<!-- lecture-page -->

## Decision variables and fixed context

| Role | Value or range in the lab |
| --- | --- |
| Decision | Residence time τ ∈ [2, 10] min |
| Fixed context | T = 330 K, C_Af = 1.2 mol/L |
| Fixed flow | Q = 1 L/min |
| Predicted output | A, B, C concentrations y [mol/L] |
| Objective | Minimize volume V = Qτ [L] |

Here τ is a design variable selecting volume at fixed flow. Choosing temperature as well requires a model with temperature as an input and bounds over that domain.

<!-- lecture-page -->

## An optimization problem in symbols

<math display="block"><mtable columnalign="left"><mtr><mtd><mrow><msub><mrow><mi>min</mi></mrow><mrow><mi>u</mi><mo>,</mo><mi>y</mi></mrow></msub><mtext>  </mtext><mi>J</mi><mrow><mo>(</mo><mi>u</mi><mo>,</mo><mi>y</mi><mo>;</mo><mi>d</mi><mo>)</mo></mrow></mrow></mtd></mtr><mtr><mtd><mrow><mi>y</mi><mo>=</mo><msub><mrow><mi>f</mi></mrow><mrow><mi>θ</mi></mrow></msub><mrow><mo>(</mo><mi>u</mi><mo>;</mo><mi>d</mi><mo>)</mo></mrow><mo>,</mo><mtext>  </mtext><mi>g</mi><mrow><mo>(</mo><mi>u</mi><mo>,</mo><mi>y</mi><mo>;</mo><mi>d</mi><mo>)</mo></mrow><mo>≤</mo><mn>0</mn></mrow></mtd></mtr></mtable></math>

u denotes decisions, d fixed context, and y model outputs. The fitted weights θ are also fixed.

A feasible point satisfies both the network equations and the process constraints. We seek the feasible point with the smallest objective.

<!-- lecture-page -->

## CSTR design optimization problem

<math display="block"><mtable columnalign="left"><mtr><mtd><mrow><msub><mrow><mi>min</mi></mrow><mrow><mi>τ</mi><mo>,</mo><mi>y</mi></mrow></msub><mtext>  </mtext><mi>V</mi><mo>=</mo><mi>Q</mi><mi>τ</mi></mrow></mtd></mtr><mtr><mtd><mrow><mn>2</mn><mo>≤</mo><mi>τ</mi><mo>≤</mo><mn>10</mn><mo>,</mo><mtext>  </mtext><mi>y</mi><mo>=</mo><msub><mrow><mi>f</mi></mrow><mrow><mi>θ</mi></mrow></msub><mrow><mo>(</mo><mi>τ</mi><mo>)</mo></mrow></mrow></mtd></mtr><mtr><mtd><mrow><msub><mrow><mi>y</mi></mrow><mrow><mi>B</mi></mrow></msub><mo>≥</mo><mn>.40</mn><mo>,</mo><mtext>  </mtext><msub><mrow><mi>y</mi></mrow><mrow><mi>C</mi></mrow></msub><mo>≤</mo><mn>.25</mn><mo>,</mo><mtext>  </mtext><mi>y</mi><mo>≥</mo><mn>0</mn></mrow></mtd></mtr></mtable></math>

With Q = 1 L/min, minimizing τ also minimizes V. Outputs are in mol/L and must be converted to those units before checking specifications.

B ≥ 0.40 is a concentration specification. Purity or production-rate requirements need constraints written from their own definitions.

<!-- lecture-page -->

## Reference concentrations for the lab

Assume perfect mixing, constant volume, equal inlet and outlet flow, and consecutive 1:1 reactions A → B → C. At 330 K, k₁ = 0.2 min⁻¹ and k₂ = 0.1 min⁻¹.

<math display="block"><mtable columnalign="left"><mtr><mtd><mrow><msub><mrow><mi>C</mi></mrow><mrow><mi>A</mi></mrow></msub><mo>=</mo><mfrac><mrow><mn>1.2</mn></mrow><mrow><mn>1</mn><mo>+</mo><mn>.2</mn><mi>τ</mi></mrow></mfrac></mrow></mtd></mtr><mtr><mtd><mrow><msub><mrow><mi>C</mi></mrow><mrow><mi>B</mi></mrow></msub><mo>=</mo><mfrac><mrow><mn>.2</mn><mi>τ</mi><msub><mrow><mi>C</mi></mrow><mrow><mi>A</mi></mrow></msub></mrow><mrow><mn>1</mn><mo>+</mo><mn>.1</mn><mi>τ</mi></mrow></mfrac><mo>,</mo><mtext>  </mtext><msub><mrow><mi>C</mi></mrow><mrow><mi>C</mi></mrow></msub><mo>=</mo><mn>.1</mn><mi>τ</mi><msub><mrow><mi>C</mi></mrow><mrow><mi>B</mi></mrow></msub></mrow></mtd></mtr></mtable></math>

We evaluate these equations at five residence times to construct a small ReLU model.

<!-- lecture-page -->

## The frozen computational graph

<math display="block"><mtable columnalign="left"><mtr><mtd><mrow><msup><mrow><mi>h</mi></mrow><mrow><mn>0</mn></mrow></msup><mo>=</mo><mi>x</mi></mrow></mtd></mtr><mtr><mtd><mrow><msup><mrow><mi>a</mi></mrow><mrow><mi>ℓ</mi></mrow></msup><mo>=</mo><msup><mrow><mi>W</mi></mrow><mrow><mi>ℓ</mi></mrow></msup><msup><mrow><mi>h</mi></mrow><mrow><mi>ℓ</mi><mo>−</mo><mn>1</mn></mrow></msup><mo>+</mo><msup><mrow><mi>b</mi></mrow><mrow><mi>ℓ</mi></mrow></msup></mrow></mtd></mtr><mtr><mtd><mrow><msup><mrow><mi>h</mi></mrow><mrow><mi>ℓ</mi></mrow></msup><mo>=</mo><mi>max</mi><mrow><mo>(</mo><mn>0</mn><mo>,</mo><msup><mrow><mi>a</mi></mrow><mrow><mi>ℓ</mi></mrow></msup><mo>)</mo></mrow></mrow></mtd></mtr><mtr><mtd><mrow><mi>y</mi><mo>=</mo><msub><mrow><mi>W</mi></mrow><mrow><mi>out</mi></mrow></msub><msup><mrow><mi>h</mi></mrow><mrow><mi>K</mi></mrow></msup><mo>+</mo><msub><mrow><mi>b</mi></mrow><mrow><mi>out</mi></mrow></msub></mrow></mtd></mtr></mtable></math>

ReLU acts componentwise in each hidden layer. Inputs, intermediate values, and outputs are optimization variables; W and b are numeric constants.

Making weights variable introduces products of W and h, so the MILP derived here would no longer apply.

<!-- lecture-page -->

## Equality representation of input scaling

<math display="block"><mtable columnalign="left"><mtr><mtd><mrow><mi>x</mi><mo>=</mo><mfrac><mrow><mi>τ</mi><mo>−</mo><mn>2</mn></mrow><mrow><mn>8</mn></mrow></mfrac><mo>,</mo><mtext>  </mtext><mn>0</mn><mo>≤</mo><mi>x</mi><mo>≤</mo><mn>1</mn></mrow></mtd></mtr><mtr><mtd><mrow><mi>τ</mi><mo>=</mo><mn>2</mn><mo>+</mo><mn>8</mn><mi>x</mi></mrow></mtd></mtr></mtable></math>

The lab maps τ to dimensionless input x. Optimization uses exactly the offset and scale used to construct the predictor.

If outputs were standardized as well, include y = μ + Ds. This inverse transformation is linear when μ and D are fixed.

<!-- lecture-page -->

## Piecewise-linear structure of ReLU

<math display="block"><mtable columnalign="left"><mtr><mtd><mrow><mi>h</mi><mo>=</mo><mi>max</mi><mrow><mo>(</mo><mn>0</mn><mo>,</mo><mi>a</mi><mo>)</mo></mrow></mrow></mtd></mtr></mtable></math>

<figure><img src="/assets/courses/surrogate-models/week-05/relu-en.svg" alt="ReLU graph and the region admitted by the binary relaxation" /></figure>
The blue line is the exact graph. The shaded region includes points admitted when the binary variable is relaxed.

<!-- lecture-page -->

## The ReLU graph and its lower inequalities

<math display="block"><mtable columnalign="left"><mtr><mtd><mrow><mi>h</mi><mo>≥</mo><mn>0</mn><mo>,</mo><mtext>  </mtext><mi>h</mi><mo>≥</mo><mi>a</mi></mrow></mtd></mtr></mtable></math>

At a = −0.2, h = 0.4 satisfies both inequalities, although ReLU returns 0.

The objective or a later layer may favor larger h. For an arbitrary network, these lower inequalities alone are insufficient; exact graph modeling also needs branch-specific upper inequalities.

<!-- lecture-page -->

## Big-M formulation of one ReLU

Assume valid finite bounds L ≤ a ≤ U with L < 0 < U.

<math display="block"><mtable columnalign="left"><mtr><mtd><mrow><mi>h</mi><mo>≥</mo><mn>0</mn><mo>,</mo><mtext>  </mtext><mi>h</mi><mo>≥</mo><mi>a</mi></mrow></mtd></mtr><mtr><mtd><mrow><mi>h</mi><mo>≤</mo><mi>a</mi><mo>−</mo><mi>L</mi><mrow><mo>(</mo><mn>1</mn><mo>−</mo><mi>z</mi><mo>)</mo></mrow></mrow></mtd></mtr><mtr><mtd><mrow><mi>h</mi><mo>≤</mo><mi>U</mi><mi>z</mi><mo>,</mo><mtext>  </mtext><mi>z</mi><mo>∈</mo><mo>{</mo><mn>0</mn><mo>,</mo><mn>1</mn><mo>}</mo></mrow></mtd></mtr></mtable></math>

z = 0 selects the inactive branch; z = 1 selects the active branch. L and U bound this neuron’s pre-activation.

<!-- lecture-page -->

## Equivalence of the inactive branch (z = 0)

<math display="block"><mtable columnalign="left"><mtr><mtd><mrow><mi>h</mi><mo>≤</mo><mi>U</mi><mn>0</mn><mo>=</mo><mn>0</mn><mo>,</mo><mtext>  </mtext><mi>h</mi><mo>≥</mo><mn>0</mn></mrow></mtd></mtr><mtr><mtd><mrow><mi>h</mi><mo>=</mo><mn>0</mn><mo>,</mo><mtext>  </mtext><mi>a</mi><mo>≤</mo><mi>h</mi><mo>=</mo><mn>0</mn></mrow></mtd></mtr></mtable></math>

The remaining upper inequality, 0 ≤ a − L, holds because a ≥ L. This branch therefore represents exactly L ≤ a ≤ 0 and h = 0.

<!-- lecture-page -->

## Equivalence of the active branch (z = 1)

<math display="block"><mtable columnalign="left"><mtr><mtd><mrow><mi>h</mi><mo>≤</mo><mi>a</mi><mo>−</mo><mi>L</mi><mn>0</mn><mo>=</mo><mi>a</mi><mo>,</mo><mtext>  </mtext><mi>h</mi><mo>≥</mo><mi>a</mi></mrow></mtd></mtr><mtr><mtd><mrow><mi>h</mi><mo>=</mo><mi>a</mi><mo>≥</mo><mn>0</mn></mrow></mtd></mtr></mtable></math>

The remaining upper inequality h ≤ U is equivalent to a ≤ U. Thus 0 ≤ a ≤ U and h = a.

At a = 0, z can be either 0 or 1, and the output h is fixed at 0.

<!-- lecture-page -->

## Linear representations of stable active and inactive neurons

| Valid range | Replacement | Binary variable |
| --- | --- | --- |
| U ≤ 0 | h = 0 | None |
| L ≥ 0 | h = a | None |
| L < 0 < U | Four Big-M inequalities | One |

Allowing inputs outside the bounded domain invalidates this simplification. Recheck bounds and classifications when changing the domain.

<!-- lecture-page -->

## Interval bounds accounting for weight signs

<math display="block"><mtable columnalign="left"><mtr><mtd><mrow><mi>a</mi><mo>=</mo><msub><mrow><mo>∑</mo></mrow><mrow><mi>i</mi></mrow></msub><msub><mrow><mi>w</mi></mrow><mrow><mi>i</mi></mrow></msub><msub><mrow><mi>h</mi></mrow><mrow><mi>i</mi></mrow></msub><mo>+</mo><mi>b</mi></mrow></mtd></mtr><mtr><mtd><mrow><mi>L</mi><mo>=</mo><mi>b</mi><mo>+</mo><msub><mrow><mo>∑</mo></mrow><mrow><mi>i</mi></mrow></msub><mi>min</mi><mrow><mo>(</mo><msub><mrow><mi>w</mi></mrow><mrow><mi>i</mi></mrow></msub><msub><mrow><mi>l</mi></mrow><mrow><mi>i</mi></mrow></msub><mo>,</mo><msub><mrow><mi>w</mi></mrow><mrow><mi>i</mi></mrow></msub><msub><mrow><mi>u</mi></mrow><mrow><mi>i</mi></mrow></msub><mo>)</mo></mrow></mrow></mtd></mtr><mtr><mtd><mrow><mi>U</mi><mo>=</mo><mi>b</mi><mo>+</mo><msub><mrow><mo>∑</mo></mrow><mrow><mi>i</mi></mrow></msub><mi>max</mi><mrow><mo>(</mo><msub><mrow><mi>w</mi></mrow><mrow><mi>i</mi></mrow></msub><msub><mrow><mi>l</mi></mrow><mrow><mi>i</mi></mrow></msub><mo>,</mo><msub><mrow><mi>w</mi></mrow><mrow><mi>i</mi></mrow></msub><msub><mrow><mi>u</mi></mrow><mrow><mi>i</mi></mrow></msub><mo>)</mo></mrow></mrow></mtd></mtr></mtable></math>

Assume lᵢ ≤ hᵢ ≤ uᵢ for every input. Negative weights reverse which input endpoint gives the minimum or maximum.

Interval arithmetic gives valid bounds, but ignoring correlations between inputs can make them wider than the attainable range.

<!-- lecture-page -->

## A bound calculation by hand

<math display="block"><mtable columnalign="left"><mtr><mtd><mrow><mi>a</mi><mo>=</mo><mn>2</mn><msub><mrow><mi>x</mi></mrow><mrow><mn>1</mn></mrow></msub><mo>−</mo><mn>3</mn><msub><mrow><mi>x</mi></mrow><mrow><mn>2</mn></mrow></msub><mo>+</mo><mn>.5</mn></mrow></mtd></mtr><mtr><mtd><mrow><mn>0</mn><mo>≤</mo><msub><mrow><mi>x</mi></mrow><mrow><mn>1</mn></mrow></msub><mo>≤</mo><mn>1</mn><mo>,</mo><mtext>  </mtext><mo>−</mo><mn>1</mn><mo>≤</mo><msub><mrow><mi>x</mi></mrow><mrow><mn>2</mn></mrow></msub><mo>≤</mo><mn>2</mn></mrow></mtd></mtr><mtr><mtd><mrow><mi>L</mi><mo>=</mo><mo>−</mo><mn>5.5</mn><mo>,</mo><mtext>  </mtext><mi>U</mi><mo>=</mo><mn>5.5</mn></mrow></mtd></mtr></mtable></math>

The minimum occurs at (x₁, x₂) = (0, 2), and the maximum at (1, −1). Do this calculation before choosing an arbitrary large constant.

<!-- lecture-page -->

## Bound validity and formulation correctness

Using U = 0.5 at a point whose true pre-activation is a = 0.7 excludes h = 0.7: even z = 1 imposes h ≤ 0.5.

Wider valid bounds preserve the graph at integer solutions, but can weaken the continuous relaxation.

Observed extrema in the training samples do not automatically bound the entire input domain.

<!-- lecture-page -->

## Frozen coefficients of the ReLU interpolant

Linearly interpolate reference concentrations at τ = 2, 4, 6, 8, 10 min. Fix the hidden hinges at those breakpoints and compute output weights from interpolation slopes.

<math display="block"><mtable columnalign="left"><mtr><mtd><mrow><msub><mrow><mi>a</mi></mrow><mrow><mi>j</mi></mrow></msub><mo>=</mo><mi>x</mi><mo>−</mo><msub><mrow><mi>t</mi></mrow><mrow><mi>j</mi></mrow></msub><mo>,</mo><mtext>  </mtext><msub><mrow><mi>h</mi></mrow><mrow><mi>j</mi></mrow></msub><mo>=</mo><mi>max</mi><mrow><mo>(</mo><mn>0</mn><mo>,</mo><msub><mrow><mi>a</mi></mrow><mrow><mi>j</mi></mrow></msub><mo>)</mo></mrow></mrow></mtd></mtr><mtr><mtd><mrow><mi>t</mi><mo>=</mo><mrow><mo>[</mo><mtable><mtr><mtd><mrow><mn>0</mn></mrow></mtd><mtd><mrow><mn>.25</mn></mrow></mtd><mtd><mrow><mn>.50</mn></mrow></mtd><mtd><mrow><mn>.75</mn></mrow></mtd></mtr></mtable><mo>]</mo></mrow></mrow></mtd></mtr><mtr><mtd><mrow><msub><mrow><mi>y</mi></mrow><mrow><mi>k</mi></mrow></msub><mo>=</mo><msub><mrow><mi>b</mi></mrow><mrow><mi>k</mi></mrow></msub><mo>+</mo><munderover><mo>∑</mo><mrow><mi>j</mi><mo>=</mo><mn>0</mn></mrow><mn>3</mn></munderover><msub><mrow><mi>W</mi></mrow><mrow><mi>jk</mi></mrow></msub><msub><mrow><mi>h</mi></mrow><mrow><mi>j</mi></mrow></msub></mrow></mtd></mtr></mtable></math>

j = 0, 1, 2, 3 and output k is A, B, or C. This lab constructs the model by interpolation rather than gradient training.

<!-- lecture-page -->

## Neuron bounds in the lab model

| Neuron | aⱼ | Lⱼ | Uⱼ | Treatment |
| --- | --- | --- | --- | --- |
| 0 | x | 0 | 1 | h₀ = x |
| 1 | x − 0.25 | −0.25 | 0.75 | Binary |
| 2 | x − 0.50 | −0.50 | 0.50 | Binary |
| 3 | x − 0.75 | −0.75 | 0.25 | Binary |

There are three binary variables. Substituting the affine pre-activations leaves eight continuous variables: one x, four h values, and three outputs.

<!-- lecture-page -->

## Matrix representation of Big-M constraints

For neuron 1, a₁ = x − 0.25, L₁ = −0.25, and U₁ = 0.75.

<math display="block"><mtable columnalign="left"><mtr><mtd><mrow><msub><mrow><mi>h</mi></mrow><mrow><mn>1</mn></mrow></msub><mo>−</mo><mi>x</mi><mo>≥</mo><mo>−</mo><mn>.25</mn></mrow></mtd></mtr><mtr><mtd><mrow><msub><mrow><mi>h</mi></mrow><mrow><mn>1</mn></mrow></msub><mo>−</mo><mi>x</mi><mo>+</mo><mn>.25</mn><msub><mrow><mi>z</mi></mrow><mrow><mn>1</mn></mrow></msub><mo>≤</mo><mn>0</mn></mrow></mtd></mtr><mtr><mtd><mrow><msub><mrow><mi>h</mi></mrow><mrow><mn>1</mn></mrow></msub><mo>−</mo><mn>.75</mn><msub><mrow><mi>z</mi></mrow><mrow><mn>1</mn></mrow></msub><mo>≤</mo><mn>0</mn></mrow></mtd></mtr></mtable></math>

Set h₁ ≥ 0 and 0 ≤ z₁ ≤ 1 as variable bounds, and declare z₁ integer. The lab assembles the full matrix in the same way.

<!-- lecture-page -->

## Conditions for MILP representability

A graph of fixed affine layers, ReLUs, and affine scaling can be expressed by an MILP. The objective and all remaining constraints must also be linear for the entire problem to be an MILP.

Products Qy with both flow and concentration variable, nonlinear kinetics, or sigmoid/tanh operations fall outside this formulation.

The Week 4 projection can also be appended as affine equalities when its coefficient matrices are fixed and its input dependence is affine.

<!-- lecture-page -->

## MILP and forward-pass consistency at fixed inputs

Fix one residence time, remove product specifications, and solve the network equations. Compare every h and y with the forward pass.

We checked 41 inputs covering domain endpoints, all breakpoints, both sides of interior breakpoints, and random inputs. The maximum difference was 1.25e-08.

This tests the formulation implementation. Process prediction error requires comparison with separate reference values.

<!-- lecture-page -->

## CSTR design optimization results

| Quantity | This run |
| --- | --- |
| Minimum τ [min] | 5.353846 |
| Minimum V [L] | 5.353846 |
| Predicted [A, B, C] [mol/L] | [0.584615, 0.400000, 0.215385] |
| Binary [z₁, z₂, z₃] | [1, 0, 0] |
| Termination | optimal, status = 0 |

The B lower bound is active, while the C upper bound has slack. Independent segmentwise linear calculations give the same residence time.

<!-- lecture-page -->

## Formulation equivalence and process prediction error

The MILP exactly represents the frozen interpolant. This property does not remove its process approximation error.

At the selected τ = 5.353846 min, the reference concentrations are [0.579495, 0.404137, 0.216369] mol/L, which differ from the predictor.

The solution is optimal for the specified surrogate problem. A process design decision also requires checking reference-process specifications and comparing objective values.

<!-- lecture-page -->

## LP relaxation and objective lower bounds

Relaxing z to [0, 1] gives a lower bound on the MILP optimum for minimization. Intermediate values and outputs may nevertheless leave the network graph.

With L = −1, U = 2, a = 0, the relaxed point z = 1/3, h = 2/3 is feasible, although the ReLU output is 0.

The LP and MILP objective values coincide in this CSTR example. Equality of objectives in one instance does not establish general graph equivalence.

<!-- lecture-page -->

## Run the lab and prepare the submission

```bash
python -m pip install -r requirements.txt
python week05_lab.py --output-dir my-results
```

1. Check one neuron’s bounds and matrix signs by hand.
2. Inspect forward error and termination status in `results.json`.
3. Translate one row of `milp_matrix.csv` back into an equation.
4. Change the B lower bound from 0.40 to 0.41 and explain whether feasibility remains.

The [reading companion](/courses/surrogate-models/week-05-reading/) contains derivations, the weight table, and exercise checks. Download and run the [lab bundle](/assets/courses/surrogate-models/week-05/week05-lab.zip).

<!-- lecture-page -->

## Sources and assigned reading

[Boyd & Vandenberghe, Convex Optimization](https://stanford.edu/~boyd/cvxbook/), §4.1: variables, objectives, and feasible sets.

[Anderson et al., Strong mixed-integer programming formulations for trained neural networks](https://arxiv.org/abs/1811.08359), §2.1: the ReLU Big-M formulation.

[SciPy milp documentation](https://docs.scipy.org/doc/scipy/reference/generated/scipy.optimize.milp.html): bounds, integrality, LinearConstraint, and return status.

<!-- ko -->

## 제품 규격을 맞추는 최소 반응기

제품 B는 0.40 mol/L 이상, 부산물 C는 0.25 mol/L 이하가 필요합니다. 유량이 일정할 때 반응기 부피를 얼마나 줄일 수 있을까요?

<figure><img src="/assets/courses/surrogate-models/week-05/motivation-ko.svg" alt="유량이 고정된 반응기의 부피와 제품 규격" /></figure>

<!-- lecture-page -->

## 제품 규격과 반응기 부피 최소화

체류시간을 주면 신경망이 출구 농도를 계산합니다. 설계에서는 반대로, 농도 조건을 만족하는 체류시간을 찾아야 합니다.

체류시간을 늘리면 A가 B로 전환되지만 B도 C로 반응합니다. B만 크게 만드는 선택과 부피를 줄이는 선택은 같지 않습니다.

이번 주에는 이 선택을 최적화 문제로 적고, 고정된 ReLU 모델의 계산을 선형식과 이진변수로 표현해봅니다.

<!-- lecture-page -->

## 최적화 정식화의 학습 목표

1. 조작변수·고정 조건·예측 출력을 구분하고 목적함수와 제약을 적습니다.
2. ReLU 한 개의 Big-M 식을 두 분기로 증명합니다.
3. 입력 범위에서 유효한 pre-activation bounds를 계산합니다.
4. 직접 작성한 MILP와 forward 계산을 같은 입력에서 대조합니다.

실습의 최종 제출물은 정식화, 검증 결과와 해의 해석입니다.

<!-- lecture-page -->

## 결정변수와 고정 조건

| 역할 | 실습의 값 또는 범위 |
| --- | --- |
| 결정변수 | 체류시간 τ ∈ [2, 10] min |
| 고정 조건 | T = 330 K, C_Af = 1.2 mol/L |
| 고정 유량 | Q = 1 L/min |
| 예측 출력 | A·B·C 농도 y [mol/L] |
| 목적 | 부피 V = Qτ [L] 최소화 |

여기서 τ는 고정 유량에서 부피를 선택하는 설계변수입니다. 온도까지 선택하려면 온도를 입력으로 받는 모델과 그 영역의 bounds가 필요합니다.

<!-- lecture-page -->

## 최적화 문제의 기본 구성

<math display="block"><mtable columnalign="left"><mtr><mtd><mrow><msub><mrow><mi>min</mi></mrow><mrow><mi>u</mi><mo>,</mo><mi>y</mi></mrow></msub><mtext>  </mtext><mi>J</mi><mrow><mo>(</mo><mi>u</mi><mo>,</mo><mi>y</mi><mo>;</mo><mi>d</mi><mo>)</mo></mrow></mrow></mtd></mtr><mtr><mtd><mrow><mi>y</mi><mo>=</mo><msub><mrow><mi>f</mi></mrow><mrow><mi>θ</mi></mrow></msub><mrow><mo>(</mo><mi>u</mi><mo>;</mo><mi>d</mi><mo>)</mo></mrow><mo>,</mo><mtext>  </mtext><mi>g</mi><mrow><mo>(</mo><mi>u</mi><mo>,</mo><mi>y</mi><mo>;</mo><mi>d</mi><mo>)</mo></mrow><mo>≤</mo><mn>0</mn></mrow></mtd></mtr></mtable></math>

u는 설계·운전 변수, d는 고정 조건, y는 모델 출력입니다. 학습을 마친 가중치 θ도 고정합니다.

신경망 등식과 공정 제약을 모두 만족하는 점이 가능해입니다. 그중 목적함수가 가장 작은 점을 찾습니다.

<!-- lecture-page -->

## CSTR 설계 최적화 문제

<math display="block"><mtable columnalign="left"><mtr><mtd><mrow><msub><mrow><mi>min</mi></mrow><mrow><mi>τ</mi><mo>,</mo><mi>y</mi></mrow></msub><mtext>  </mtext><mi>V</mi><mo>=</mo><mi>Q</mi><mi>τ</mi></mrow></mtd></mtr><mtr><mtd><mrow><mn>2</mn><mo>≤</mo><mi>τ</mi><mo>≤</mo><mn>10</mn><mo>,</mo><mtext>  </mtext><mi>y</mi><mo>=</mo><msub><mrow><mi>f</mi></mrow><mrow><mi>θ</mi></mrow></msub><mrow><mo>(</mo><mi>τ</mi><mo>)</mo></mrow></mrow></mtd></mtr><mtr><mtd><mrow><msub><mrow><mi>y</mi></mrow><mrow><mi>B</mi></mrow></msub><mo>≥</mo><mn>.40</mn><mo>,</mo><mtext>  </mtext><msub><mrow><mi>y</mi></mrow><mrow><mi>C</mi></mrow></msub><mo>≤</mo><mn>.25</mn><mo>,</mo><mtext>  </mtext><mi>y</mi><mo>≥</mo><mn>0</mn></mrow></mtd></mtr></mtable></math>

Q = 1 L/min이므로 τ를 줄이면 V도 줄어듭니다. y의 농도 단위는 mol/L이며, 모델의 출력은 이 단위로 복원한 뒤 규격과 비교합니다.

B ≥ 0.40은 농도 규격입니다. 순도나 생산량을 요구한다면 해당 정의로 제약을 다시 적어야 합니다.

<!-- lecture-page -->

## 실습의 기준 농도

완전 혼합·일정 부피·동일한 유입 및 유출 유량을 가정하고, 1:1 연속반응 A → B → C를 사용합니다. 330 K에서 k₁ = 0.2 min⁻¹, k₂ = 0.1 min⁻¹입니다.

<math display="block"><mtable columnalign="left"><mtr><mtd><mrow><msub><mrow><mi>C</mi></mrow><mrow><mi>A</mi></mrow></msub><mo>=</mo><mfrac><mrow><mn>1.2</mn></mrow><mrow><mn>1</mn><mo>+</mo><mn>.2</mn><mi>τ</mi></mrow></mfrac></mrow></mtd></mtr><mtr><mtd><mrow><msub><mrow><mi>C</mi></mrow><mrow><mi>B</mi></mrow></msub><mo>=</mo><mfrac><mrow><mn>.2</mn><mi>τ</mi><msub><mrow><mi>C</mi></mrow><mrow><mi>A</mi></mrow></msub></mrow><mrow><mn>1</mn><mo>+</mo><mn>.1</mn><mi>τ</mi></mrow></mfrac><mo>,</mo><mtext>  </mtext><msub><mrow><mi>C</mi></mrow><mrow><mi>C</mi></mrow></msub><mo>=</mo><mn>.1</mn><mi>τ</mi><msub><mrow><mi>C</mi></mrow><mrow><mi>B</mi></mrow></msub></mrow></mtd></mtr></mtable></math>

다섯 체류시간에서 이 식을 계산해 작은 ReLU 모델을 구성합니다.

<!-- lecture-page -->

## 가중치를 고정한 계산 그래프

<math display="block"><mtable columnalign="left"><mtr><mtd><mrow><msup><mrow><mi>h</mi></mrow><mrow><mn>0</mn></mrow></msup><mo>=</mo><mi>x</mi></mrow></mtd></mtr><mtr><mtd><mrow><msup><mrow><mi>a</mi></mrow><mrow><mi>ℓ</mi></mrow></msup><mo>=</mo><msup><mrow><mi>W</mi></mrow><mrow><mi>ℓ</mi></mrow></msup><msup><mrow><mi>h</mi></mrow><mrow><mi>ℓ</mi><mo>−</mo><mn>1</mn></mrow></msup><mo>+</mo><msup><mrow><mi>b</mi></mrow><mrow><mi>ℓ</mi></mrow></msup></mrow></mtd></mtr><mtr><mtd><mrow><msup><mrow><mi>h</mi></mrow><mrow><mi>ℓ</mi></mrow></msup><mo>=</mo><mi>max</mi><mrow><mo>(</mo><mn>0</mn><mo>,</mo><msup><mrow><mi>a</mi></mrow><mrow><mi>ℓ</mi></mrow></msup><mo>)</mo></mrow></mrow></mtd></mtr><mtr><mtd><mrow><mi>y</mi><mo>=</mo><msub><mrow><mi>W</mi></mrow><mrow><mi>out</mi></mrow></msub><msup><mrow><mi>h</mi></mrow><mrow><mi>K</mi></mrow></msup><mo>+</mo><msub><mrow><mi>b</mi></mrow><mrow><mi>out</mi></mrow></msub></mrow></mtd></mtr></mtable></math>

각 hidden layer의 ReLU는 성분별로 적용합니다. 입력·중간값·출력은 최적화 변수이고 W와 b는 수치 상수입니다.

가중치까지 변수로 두면 W와 h의 곱이 생기므로 여기서 유도하는 MILP가 성립하지 않습니다.

<!-- lecture-page -->

## 입력 scaling의 등식 표현

<math display="block"><mtable columnalign="left"><mtr><mtd><mrow><mi>x</mi><mo>=</mo><mfrac><mrow><mi>τ</mi><mo>−</mo><mn>2</mn></mrow><mrow><mn>8</mn></mrow></mfrac><mo>,</mo><mtext>  </mtext><mn>0</mn><mo>≤</mo><mi>x</mi><mo>≤</mo><mn>1</mn></mrow></mtd></mtr><mtr><mtd><mrow><mi>τ</mi><mo>=</mo><mn>2</mn><mo>+</mo><mn>8</mn><mi>x</mi></mrow></mtd></mtr></mtable></math>

실습은 τ를 무차원 입력 x로 바꿉니다. 학습 때 사용한 offset과 scale을 최적화에서도 그대로 사용합니다.

출력까지 표준화했다면 y = μ + Ds를 추가합니다. μ와 D가 고정이면 이 복원식은 선형입니다.

<!-- lecture-page -->

## ReLU 함수의 구간별 선형 구조

<math display="block"><mtable columnalign="left"><mtr><mtd><mrow><mi>h</mi><mo>=</mo><mi>max</mi><mrow><mo>(</mo><mn>0</mn><mo>,</mo><mi>a</mi><mo>)</mo></mrow></mrow></mtd></mtr></mtable></math>

<figure><img src="/assets/courses/surrogate-models/week-05/relu-ko.svg" alt="ReLU 그래프와 이진변수를 완화했을 때 허용되는 영역" /></figure>
파란 선이 정확한 그래프입니다. 색칠한 영역은 이진변수를 연속으로 풀었을 때 허용되는 점을 포함합니다.

<!-- lecture-page -->

## ReLU 그래프와 하한 제약

<math display="block"><mtable columnalign="left"><mtr><mtd><mrow><mi>h</mi><mo>≥</mo><mn>0</mn><mo>,</mo><mtext>  </mtext><mi>h</mi><mo>≥</mo><mi>a</mi></mrow></mtd></mtr></mtable></math>

a = −0.2일 때 h = 0.4도 이 두 식을 만족하지만 ReLU 출력은 0입니다.

목적함수나 후속 layer가 큰 h를 선호할 수 있으므로, 임의의 신경망에서는 이 두 하한만 넣어서는 안 됩니다. 정확한 그래프에는 두 분기에 맞는 상한도 필요합니다.

<!-- lecture-page -->

## 한 개 ReLU의 Big-M 정식화

유효한 유한 bounds L ≤ a ≤ U를 알고 있고 L < 0 < U라고 놓습니다.

<math display="block"><mtable columnalign="left"><mtr><mtd><mrow><mi>h</mi><mo>≥</mo><mn>0</mn><mo>,</mo><mtext>  </mtext><mi>h</mi><mo>≥</mo><mi>a</mi></mrow></mtd></mtr><mtr><mtd><mrow><mi>h</mi><mo>≤</mo><mi>a</mi><mo>−</mo><mi>L</mi><mrow><mo>(</mo><mn>1</mn><mo>−</mo><mi>z</mi><mo>)</mo></mrow></mrow></mtd></mtr><mtr><mtd><mrow><mi>h</mi><mo>≤</mo><mi>U</mi><mi>z</mi><mo>,</mo><mtext>  </mtext><mi>z</mi><mo>∈</mo><mo>{</mo><mn>0</mn><mo>,</mo><mn>1</mn><mo>}</mo></mrow></mtd></mtr></mtable></math>

z = 0은 비활성 분기, z = 1은 활성 분기를 선택합니다. L과 U는 해당 뉴런의 pre-activation 범위입니다.

<!-- lecture-page -->

## 비활성 분기(z = 0)의 동치성

<math display="block"><mtable columnalign="left"><mtr><mtd><mrow><mi>h</mi><mo>≤</mo><mi>U</mi><mn>0</mn><mo>=</mo><mn>0</mn><mo>,</mo><mtext>  </mtext><mi>h</mi><mo>≥</mo><mn>0</mn></mrow></mtd></mtr><mtr><mtd><mrow><mi>h</mi><mo>=</mo><mn>0</mn><mo>,</mo><mtext>  </mtext><mi>a</mi><mo>≤</mo><mi>h</mi><mo>=</mo><mn>0</mn></mrow></mtd></mtr></mtable></math>

나머지 상한 0 ≤ a − L은 a ≥ L이므로 만족합니다. 따라서 이 분기는 L ≤ a ≤ 0, h = 0을 정확히 나타냅니다.

<!-- lecture-page -->

## 활성 분기(z = 1)의 동치성

<math display="block"><mtable columnalign="left"><mtr><mtd><mrow><mi>h</mi><mo>≤</mo><mi>a</mi><mo>−</mo><mi>L</mi><mn>0</mn><mo>=</mo><mi>a</mi><mo>,</mo><mtext>  </mtext><mi>h</mi><mo>≥</mo><mi>a</mi></mrow></mtd></mtr><mtr><mtd><mrow><mi>h</mi><mo>=</mo><mi>a</mi><mo>≥</mo><mn>0</mn></mrow></mtd></mtr></mtable></math>

나머지 상한 h ≤ U는 a ≤ U와 같습니다. 따라서 0 ≤ a ≤ U, h = a를 얻습니다.

a = 0에서는 z가 0 또는 1이어도 출력 h는 0으로 정해집니다.

<!-- lecture-page -->

## 활성·비활성 뉴런의 선형 표현

| 유효한 범위 | 대체 식 | 이진변수 |
| --- | --- | --- |
| U ≤ 0 | h = 0 | 불필요 |
| L ≥ 0 | h = a | 불필요 |
| L < 0 < U | Big-M 네 부등식 | 1개 |

범위를 벗어나는 입력까지 허용하면 이 단순화의 근거가 사라집니다. 입력 영역을 바꾸면 bounds와 분류도 다시 확인합니다.

<!-- lecture-page -->

## 가중치 부호를 반영한 구간 bounds

<math display="block"><mtable columnalign="left"><mtr><mtd><mrow><mi>a</mi><mo>=</mo><msub><mrow><mo>∑</mo></mrow><mrow><mi>i</mi></mrow></msub><msub><mrow><mi>w</mi></mrow><mrow><mi>i</mi></mrow></msub><msub><mrow><mi>h</mi></mrow><mrow><mi>i</mi></mrow></msub><mo>+</mo><mi>b</mi></mrow></mtd></mtr><mtr><mtd><mrow><mi>L</mi><mo>=</mo><mi>b</mi><mo>+</mo><msub><mrow><mo>∑</mo></mrow><mrow><mi>i</mi></mrow></msub><mi>min</mi><mrow><mo>(</mo><msub><mrow><mi>w</mi></mrow><mrow><mi>i</mi></mrow></msub><msub><mrow><mi>l</mi></mrow><mrow><mi>i</mi></mrow></msub><mo>,</mo><msub><mrow><mi>w</mi></mrow><mrow><mi>i</mi></mrow></msub><msub><mrow><mi>u</mi></mrow><mrow><mi>i</mi></mrow></msub><mo>)</mo></mrow></mrow></mtd></mtr><mtr><mtd><mrow><mi>U</mi><mo>=</mo><mi>b</mi><mo>+</mo><msub><mrow><mo>∑</mo></mrow><mrow><mi>i</mi></mrow></msub><mi>max</mi><mrow><mo>(</mo><msub><mrow><mi>w</mi></mrow><mrow><mi>i</mi></mrow></msub><msub><mrow><mi>l</mi></mrow><mrow><mi>i</mi></mrow></msub><mo>,</mo><msub><mrow><mi>w</mi></mrow><mrow><mi>i</mi></mrow></msub><msub><mrow><mi>u</mi></mrow><mrow><mi>i</mi></mrow></msub><mo>)</mo></mrow></mrow></mtd></mtr></mtable></math>

각 입력이 lᵢ ≤ hᵢ ≤ uᵢ를 만족한다고 가정합니다. 음의 가중치는 입력의 위아래 끝점을 뒤집습니다.

이 구간 계산은 유효한 범위를 주지만, 입력 간 상관관계를 무시하므로 가능한 실제 범위보다 넓을 수 있습니다.

<!-- lecture-page -->

## Bounds 손계산 예제

<math display="block"><mtable columnalign="left"><mtr><mtd><mrow><mi>a</mi><mo>=</mo><mn>2</mn><msub><mrow><mi>x</mi></mrow><mrow><mn>1</mn></mrow></msub><mo>−</mo><mn>3</mn><msub><mrow><mi>x</mi></mrow><mrow><mn>2</mn></mrow></msub><mo>+</mo><mn>.5</mn></mrow></mtd></mtr><mtr><mtd><mrow><mn>0</mn><mo>≤</mo><msub><mrow><mi>x</mi></mrow><mrow><mn>1</mn></mrow></msub><mo>≤</mo><mn>1</mn><mo>,</mo><mtext>  </mtext><mo>−</mo><mn>1</mn><mo>≤</mo><msub><mrow><mi>x</mi></mrow><mrow><mn>2</mn></mrow></msub><mo>≤</mo><mn>2</mn></mrow></mtd></mtr><mtr><mtd><mrow><mi>L</mi><mo>=</mo><mo>−</mo><mn>5.5</mn><mo>,</mo><mtext>  </mtext><mi>U</mi><mo>=</mo><mn>5.5</mn></mrow></mtd></mtr></mtable></math>

최솟값은 (x₁, x₂) = (0, 2), 최댓값은 (1, −1)에서 나옵니다. 임의의 큰 숫자를 고르기 전에 이 계산부터 합니다.

<!-- lecture-page -->

## Bounds의 유효성과 정식화의 정확성

실제 pre-activation이 a = 0.7인 점에 U = 0.5를 사용하면 h = 0.7을 표현할 수 없습니다. z = 1에서도 h ≤ 0.5이기 때문입니다.

반대로 충분히 넓은 유효 bounds는 정수해의 그래프를 유지하지만, 연속 완화를 느슨하게 만들 수 있습니다.

학습 샘플에서 관측한 최솟값·최댓값은 전체 입력 영역의 bounds를 자동으로 보장하지 않습니다.

<!-- lecture-page -->

## ReLU 보간 모델의 고정 계수

τ = 2, 4, 6, 8, 10 min의 기준 농도를 선형 보간합니다. 꺾이는 위치를 hidden layer에 고정하고, 보간 기울기에서 출력 가중치를 계산합니다.

<math display="block"><mtable columnalign="left"><mtr><mtd><mrow><msub><mrow><mi>a</mi></mrow><mrow><mi>j</mi></mrow></msub><mo>=</mo><mi>x</mi><mo>−</mo><msub><mrow><mi>t</mi></mrow><mrow><mi>j</mi></mrow></msub><mo>,</mo><mtext>  </mtext><msub><mrow><mi>h</mi></mrow><mrow><mi>j</mi></mrow></msub><mo>=</mo><mi>max</mi><mrow><mo>(</mo><mn>0</mn><mo>,</mo><msub><mrow><mi>a</mi></mrow><mrow><mi>j</mi></mrow></msub><mo>)</mo></mrow></mrow></mtd></mtr><mtr><mtd><mrow><mi>t</mi><mo>=</mo><mrow><mo>[</mo><mtable><mtr><mtd><mrow><mn>0</mn></mrow></mtd><mtd><mrow><mn>.25</mn></mrow></mtd><mtd><mrow><mn>.50</mn></mrow></mtd><mtd><mrow><mn>.75</mn></mrow></mtd></mtr></mtable><mo>]</mo></mrow></mrow></mtd></mtr><mtr><mtd><mrow><msub><mrow><mi>y</mi></mrow><mrow><mi>k</mi></mrow></msub><mo>=</mo><msub><mrow><mi>b</mi></mrow><mrow><mi>k</mi></mrow></msub><mo>+</mo><munderover><mo>∑</mo><mrow><mi>j</mi><mo>=</mo><mn>0</mn></mrow><mn>3</mn></munderover><msub><mrow><mi>W</mi></mrow><mrow><mi>jk</mi></mrow></msub><msub><mrow><mi>h</mi></mrow><mrow><mi>j</mi></mrow></msub></mrow></mtd></mtr></mtable></math>

j = 0, 1, 2, 3이며 출력 k는 A, B, C입니다. 이 실습의 모델 구성은 보간이고, 경사하강 학습은 사용하지 않습니다.

<!-- lecture-page -->

## 실습 모델의 뉴런별 bounds

| 뉴런 | aⱼ | Lⱼ | Uⱼ | 처리 |
| --- | --- | --- | --- | --- |
| 0 | x | 0 | 1 | h₀ = x |
| 1 | x − 0.25 | −0.25 | 0.75 | 이진변수 |
| 2 | x − 0.50 | −0.50 | 0.50 | 이진변수 |
| 3 | x − 0.75 | −0.75 | 0.25 | 이진변수 |

총 이진변수는 3개입니다. a를 식에 대입해 없애면 연속변수는 x 1개, h 4개, y 3개로 8개입니다.

<!-- lecture-page -->

## Big-M 제약의 행렬 표현

뉴런 1에서 a₁ = x − 0.25, L₁ = −0.25, U₁ = 0.75입니다.

<math display="block"><mtable columnalign="left"><mtr><mtd><mrow><msub><mrow><mi>h</mi></mrow><mrow><mn>1</mn></mrow></msub><mo>−</mo><mi>x</mi><mo>≥</mo><mo>−</mo><mn>.25</mn></mrow></mtd></mtr><mtr><mtd><mrow><msub><mrow><mi>h</mi></mrow><mrow><mn>1</mn></mrow></msub><mo>−</mo><mi>x</mi><mo>+</mo><mn>.25</mn><msub><mrow><mi>z</mi></mrow><mrow><mn>1</mn></mrow></msub><mo>≤</mo><mn>0</mn></mrow></mtd></mtr><mtr><mtd><mrow><msub><mrow><mi>h</mi></mrow><mrow><mn>1</mn></mrow></msub><mo>−</mo><mn>.75</mn><msub><mrow><mi>z</mi></mrow><mrow><mn>1</mn></mrow></msub><mo>≤</mo><mn>0</mn></mrow></mtd></mtr></mtable></math>

h₁ ≥ 0과 0 ≤ z₁ ≤ 1은 변수 bounds에 적고, z₁을 정수로 지정합니다. 실습은 같은 방식으로 전체 행렬을 직접 조립합니다.

<!-- lecture-page -->

## MILP 표현의 성립 조건

고정 계수의 affine layer, ReLU, affine scaling을 위 식으로 연결하면 신경망 그래프를 MILP로 표현할 수 있습니다. 전체 문제의 목적함수와 나머지 제약도 선형이어야 합니다.

가변 유량 Q와 가변 농도의 곱 Qy, 비선형 속도식, sigmoid·tanh를 그대로 추가하면 현재 MILP 구조를 벗어납니다.

4주차의 투영도 계수 행렬이 고정이고 입력에 affine이면 마지막 선형 등식으로 연결할 수 있습니다.

<!-- lecture-page -->

## 고정 입력의 MILP·forward 일치 검사

체류시간 하나를 고정하고 제품 규격 제약을 뺀 뒤 신경망 등식만 풉니다. 계산된 모든 h와 y를 forward 결과와 비교합니다.

끝점, 모든 꺾임점, 꺾임점 양쪽과 난수 입력을 포함해 41개 입력을 확인했습니다. 최대 차이는 1.25e-08입니다.

이 대조는 정식화 구현을 검사합니다. 공정 예측 오차는 별도의 기준값과 비교해야 합니다.

<!-- lecture-page -->

## CSTR 설계 최적화 결과

| 항목 | 이번 실행 |
| --- | --- |
| 최소 τ [min] | 5.353846 |
| 최소 V [L] | 5.353846 |
| 예측 [A, B, C] [mol/L] | [0.584615, 0.400000, 0.215385] |
| 이진변수 [z₁, z₂, z₃] | [1, 0, 0] |
| 종료 상태 | optimal, status = 0 |

B의 하한이 활성이고 C의 상한에는 여유가 있습니다. 독립적인 구간별 선형 계산에서도 같은 체류시간을 얻었습니다.

<!-- lecture-page -->

## 정식화의 동치성과 공정 예측 오차

MILP는 고정한 보간 모델을 정확히 표현합니다. 이 성질이 보간 모델의 공정 오차를 없애지는 않습니다.

선택된 τ = 5.353846 min에서 기준 농도는 [0.579495, 0.404137, 0.216369] mol/L이고, 모델 예측과 차이가 있습니다.

이 해는 주어진 surrogate 문제의 최적해입니다. 실제 공정에 대한 설계 판단에는 기준 공정의 규격 확인과 목적값 비교가 더 필요합니다.

<!-- lecture-page -->

## LP 완화와 목적값 하한

z ∈ [0, 1]로 완화하면 최소화 문제의 목적값은 MILP 최적값의 하한입니다. 그러나 중간값과 출력이 원래 신경망 그래프를 벗어날 수 있습니다.

L = −1, U = 2, a = 0에서 z = 1/3, h = 2/3은 완화식을 만족하지만 실제 ReLU 출력은 0입니다.

이번 CSTR 예제에서는 LP와 MILP의 목적값이 같았습니다. 한 사례의 목적값 일치로 일반적인 그래프 동치가 성립하지는 않습니다.

<!-- lecture-page -->

## 실습 실행과 제출

```bash
python -m pip install -r requirements.txt
python week05_lab.py --output-dir my-results
```

1. 한 뉴런의 bounds와 행렬 부호를 손으로 확인합니다.
2. `results.json`의 forward 오차와 종료 상태를 확인합니다.
3. `milp_matrix.csv`의 행 하나를 수식으로 되돌려 적습니다.
4. B 하한을 0.40에서 0.41로 바꾸고 가능해가 남는지 설명합니다.

[읽기자료](/courses/surrogate-models/week-05-reading/)에는 유도, 가중치 표와 연습문제 풀이가 있습니다. [실습 묶음](/assets/courses/surrogate-models/week-05/week05-lab.zip)을 내려받아 실행합니다.

<!-- lecture-page -->

## 출처와 지정 읽기

[Boyd & Vandenberghe, Convex Optimization](https://stanford.edu/~boyd/cvxbook/), 4.1절: 변수·목적함수·가능집합.

[Anderson et al., Strong mixed-integer programming formulations for trained neural networks](https://arxiv.org/abs/1811.08359), 2.1절: ReLU Big-M 표현.

[SciPy milp 공식 문서](https://docs.scipy.org/doc/scipy/reference/generated/scipy.optimize.milp.html): bounds, integrality, LinearConstraint와 반환 상태.
