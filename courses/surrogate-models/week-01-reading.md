---
layout: course-note
title: "Week 1 Reading: Process Prediction"
title_ko: "1주차 읽기자료: 공정 예측과 회귀 baseline"
description: "A worked guide to prediction contracts, reference balances, data splits, regression, and independent evaluation."
description_ko: "예측 문제 정의, 기준 수지, 데이터 분할, 회귀 학습과 독립 평가를 직접 계산하는 읽기자료입니다."
material_label: "Week 1 reading"
material_label_ko: "1주차 읽기자료"
updated: "2026-10-09"
permalink: /courses/surrogate-models/week-01-reading/
pdf_en: /assets/courses/surrogate-models/week-01-reading-en.pdf
pdf_ko: /assets/courses/surrogate-models/week-01-reading-ko.pdf
lecture_note: /courses/surrogate-models/week-01/
course_id: "surrogate-models"
---

## 1. Define the map before collecting data

A surrogate predicts outputs from specified inputs over a declared domain. A label is a reference output paired with one input row.

| Role | This prediction task |
| --- | --- |
| Inputs | T: 300–360 K; τ: 1–10 min; C_Af: 0.8–1.5 mol/L |
| Outputs | C_A in mol/L; conversion X, dimensionless |
| Fixed context | Ideal, constant-volume, isothermal CSTR; first-order A → B; fixed rate parameters |
| Reference | Steady-state material-balance solution |

Feed concentration is an input here. It is not fixed to 1.2 mol/L for all data. Reaction assumptions and units must stay the same across the rows.

**Check:** a number called “temperature” is insufficient unless its units and operating range are known.

<!-- lecture-page -->

## 2. Derive the steady-state map

The ideal CSTR is perfectly mixed, isothermal, and constant-volume, with first-order reaction A → B. The balance is accumulation = inlet − outlet − reaction:

<math display="block" aria-label="CSTR concentration balance"><mfrac><mrow><mi>d</mi><msub><mi>C</mi><mi>A</mi></msub></mrow><mrow><mi>d</mi><mi>t</mi></mrow></mfrac><mo>=</mo><mfrac><mrow><msub><mi>C</mi><mrow><mi>A</mi><mi>f</mi></mrow></msub><mo>−</mo><msub><mi>C</mi><mi>A</mi></msub></mrow><mi>τ</mi></mfrac><mo>−</mo><mi>k</mi><mo>(</mo><mi>T</mi><mo>)</mo><msub><mi>C</mi><mi>A</mi></msub></math>

At steady state, set the derivative to zero. Multiply by residence time, move the concentration terms to the same side, and factor out outlet concentration. Dividing by the positive factor gives:

<math display="block" aria-label="CSTR steady concentration and conversion"><msub><mi>C</mi><mi>A</mi></msub><mo>=</mo><mfrac><msub><mi>C</mi><mrow><mi>A</mi><mi>f</mi></mrow></msub><mrow><mn>1</mn><mo>+</mo><mi>k</mi><mo>(</mo><mi>T</mi><mo>)</mo><mi>τ</mi></mrow></mfrac><mo>,</mo><mspace width="1em"/><mi>X</mi><mo>=</mo><mn>1</mn><mo>−</mo><mfrac><msub><mi>C</mi><mi>A</mi></msub><msub><mi>C</mi><mrow><mi>A</mi><mi>f</mi></mrow></msub></mfrac><mo>=</mo><mfrac><mrow><mi>k</mi><mo>(</mo><mi>T</mi><mo>)</mo><mi>τ</mi></mrow><mrow><mn>1</mn><mo>+</mo><mi>k</mi><mo>(</mo><mi>T</mi><mo>)</mo><mi>τ</mi></mrow></mfrac></math>

At 330 K, the rate constant is 0.2/min. At 5 min residence time, the product of rate and residence time is 1, so conversion is 0.5. A 1.2 mol/L feed gives a 0.6 mol/L outlet.

The conversion is independent of feed concentration in this particular first-order model. That property is not a general rule for all reactors.

<!-- lecture-page -->

## 3. Build independent train, validation, and test data

Use this teaching rate law, with T in K and k in 1/min:

<math display="block" aria-label="Numeric temperature-dependent teaching rate law"><mrow><mi>k</mi><mo>(</mo><mi>T</mi><mo>)</mo><mo>=</mo><mn>0.2</mn><mi>exp</mi><mo>[</mo><mn>6000</mn><mo>(</mo><mfrac><mn>1</mn><mn>330</mn></mfrac><mo>−</mo><mfrac><mn>1</mn><mi>T</mi></mfrac><mo>)</mo><mo>]</mo></mrow></math>

Sample inputs independently and uniformly inside the declared box; compute each label with the steady-state equations. Seed 42 fixes a reproducible sample.

| Split | Rows | Role |
| --- | --- | --- |
| Train | 400 | Fit coefficients |
| Validation | 120 | Compare model choices |
| Test | 160 | Final held-out evaluation |

The provided basis is fixed in advance. If comparing another basis or capacity, use validation and leave test untouched. A new simulator sample is not automatically a new experimental campaign.

<!-- lecture-page -->

## 4. Scale inputs and fit ten features

<math display="block" aria-label="Input scaling using the declared domain"><msub><mi>x̃</mi><mi>j</mi></msub><mo>=</mo><mn>2</mn><mfrac><mrow><msub><mi>x</mi><mi>j</mi></msub><mo>−</mo><msub><mi>l</mi><mi>j</mi></msub></mrow><mrow><msub><mi>u</mi><mi>j</mi></msub><mo>−</mo><msub><mi>l</mi><mi>j</mi></msub></mrow></mfrac><mo>−</mo><mn>1</mn></math>

At [330 K, 5 min, 1.2 mol/L], the scaled input is approximately [0, −0.111111, 0.142857]. The scaling uses declared bounds, not statistics computed from test data.

The feature row contains 1 constant + 3 inputs + 3 squares + 3 pairwise products = **10 features**. For 400 train rows, Φ has shape (400, 10), Y (400, 2), and B (10, 2).

<math display="block" aria-label="Least-squares training of the two-output baseline"><munder><mi>min</mi><mi mathvariant="bold">B</mi></munder><msubsup><mrow><mo>‖</mo><mi mathvariant="bold">Φ</mi><mi mathvariant="bold">B</mi><mo>−</mo><mi mathvariant="bold">Y</mi><mo>‖</mo></mrow><mi>F</mi><mn>2</mn></msubsup><mo>,</mo><mspace width="1em"/><mover><mi mathvariant="bold">y</mi><mo>^</mo></mover><mo>=</mo><mi>φ</mi><mo>(</mo><mi mathvariant="bold">x</mi><mo>)</mo><mi mathvariant="bold">B</mi></math>

`np.linalg.lstsq` fits B. Keep B fixed when predicting new input rows. Fitting parameters is an optimization calculation; selecting plant operating conditions is a later, separate problem.

<!-- lecture-page -->

## 5. Read accuracy and consistency separately

<math display="block" aria-label="Root mean squared error for one output"><msub><mtext>RMSE</mtext><mi>j</mi></msub><mo>=</mo><msqrt><mrow><mfrac><mn>1</mn><mi>N</mi></mfrac><munderover><mo>∑</mo><mrow><mi>n</mi><mo>=</mo><mn>1</mn></mrow><mi>N</mi></munderover><msup><mrow><mo>(</mo><msub><mover><mi>y</mi><mo>^</mo></mover><mrow><mi>n</mi><mi>j</mi></mrow></msub><mo>−</mo><msub><mi>y</mi><mrow><mi>n</mi><mi>j</mi></mrow></msub><mo>)</mo></mrow><mn>2</mn></msup></mrow></msqrt></math>

For each output, subtract the reference from the prediction, square, average over the test rows, and take the square root. Concentration RMSE is in mol/L; conversion RMSE is dimensionless.

The seed-42 baseline gives concentration RMSE **0.032623 mol/L** and conversion RMSE **0.025608**. Inspect individual errors as well as the averages.

<math display="block" aria-label="Consistency residual of concentration and conversion"><mrow><mi>r</mi><mo>=</mo><mover><msub><mi>C</mi><mi>A</mi></msub><mo>^</mo></mover><mo>+</mo><msub><mi>C</mi><mi>Af</mi></msub><mover><mi>X</mi><mo>^</mo></mover><mo>−</mo><msub><mi>C</mi><mi>Af</mi></msub></mrow></math>

For feed 1.2, prediction C_A = 0.65 and X = 0.45 gives r = 0.65 + 1.2 × 0.45 − 1.2 = **−0.01 mol/L**. The predicted pair is not exactly consistent with the defined conversion relation. Physical-consistency methods are studied in Week 4.

<!-- lecture-page -->

## 6. Answer checks and readings

**Try first:** at 330 K, 10 min, and feed 1.2 mol/L, what are C_A and X? How many regression coefficients are fitted for two outputs? Why can a low training error be misleading?

**Answer check:** kτ = 2, so C_A = 1.2/3 = **0.4 mol/L** and X = **2/3**. B contains **20 coefficients**: ten features for each of two outputs. Training evaluates the same points used for fitting; independent errors can be larger.

Work through this course-specific companion and the [Week 1 lab]({{ page.lecture_note | relative_url }}). Optional background: Boyd and Vandenberghe, *Convex Optimization*, affine maps and least-squares problems in Chapters 2 and 4 ([official book PDF](https://web.stanford.edu/~boyd/cvxbook/bv_cvxbook.pdf)).

Week 2 introduces MLPs; Week 3 adds dynamic prediction. Operating objectives and constraints return in Weeks 5–8.

<!-- ko -->

## 1. 데이터를 만들기 전에 mapping 정의하기

Surrogate는 명시한 영역에서 입력으로부터 출력을 예측한다. Label은 입력 한 행에 짝지은 기준 출력이다.

| 역할 | 이 예측 문제 |
| --- | --- |
| 입력 | T: 300–360 K; τ: 1–10 min; C_Af: 0.8–1.5 mol/L |
| 출력 | C_A: mol/L; 전환율 X: 무차원 |
| 고정 context | 이상적·일정 부피·등온 CSTR, 1차 반응 A → B, 고정된 속도식 파라미터 |
| 기준값 | 정상상태 물질수지의 해 |

여기에서 유입 농도는 입력이다. 모든 데이터를 1.2 mol/L로 고정하지 않는다. 반응 가정과 단위는 데이터 행들 사이에서 같아야 한다.

**확인:** “온도”라는 수만으로는 부족하다. 단위와 운전 범위를 함께 알아야 한다.

<!-- lecture-page -->

## 2. 정상상태 mapping 직접 유도하기

이상적인 완전혼합·등온·일정 부피 CSTR에서 1차 반응 A → B가 일어난다. 축적 = 유입 − 유출 − 반응으로 수지를 작성한다.

<math display="block" aria-label="CSTR concentration balance"><mfrac><mrow><mi>d</mi><msub><mi>C</mi><mi>A</mi></msub></mrow><mrow><mi>d</mi><mi>t</mi></mrow></mfrac><mo>=</mo><mfrac><mrow><msub><mi>C</mi><mrow><mi>A</mi><mi>f</mi></mrow></msub><mo>−</mo><msub><mi>C</mi><mi>A</mi></msub></mrow><mi>τ</mi></mfrac><mo>−</mo><mi>k</mi><mo>(</mo><mi>T</mi><mo>)</mo><msub><mi>C</mi><mi>A</mi></msub></math>

정상상태에서는 미분을 0으로 둔다. 체류시간을 곱하고 농도가 있는 항을 한쪽에 모은 뒤 출구 농도를 묶는다. 양수인 계수로 나누면 다음 결과를 얻는다.

<math display="block" aria-label="CSTR steady concentration and conversion"><msub><mi>C</mi><mi>A</mi></msub><mo>=</mo><mfrac><msub><mi>C</mi><mrow><mi>A</mi><mi>f</mi></mrow></msub><mrow><mn>1</mn><mo>+</mo><mi>k</mi><mo>(</mo><mi>T</mi><mo>)</mo><mi>τ</mi></mrow></mfrac><mo>,</mo><mspace width="1em"/><mi>X</mi><mo>=</mo><mn>1</mn><mo>−</mo><mfrac><msub><mi>C</mi><mi>A</mi></msub><msub><mi>C</mi><mrow><mi>A</mi><mi>f</mi></mrow></msub></mfrac><mo>=</mo><mfrac><mrow><mi>k</mi><mo>(</mo><mi>T</mi><mo>)</mo><mi>τ</mi></mrow><mrow><mn>1</mn><mo>+</mo><mi>k</mi><mo>(</mo><mi>T</mi><mo>)</mo><mi>τ</mi></mrow></mfrac></math>

330 K에서 속도상수는 0.2/min이다. 체류시간이 5 min이면 속도상수와 체류시간의 곱이 1이므로 전환율은 0.5다. 유입 농도가 1.2 mol/L이면 출구는 0.6 mol/L이다.

이 1차 반응 모델에서는 전환율이 유입 농도에 무관하다. 모든 반응기에 적용되는 일반 성질은 아니다.

<!-- lecture-page -->

## 3. 독립 train·validation·test 데이터 만들기

다음 교육용 속도식을 사용한다. T의 단위는 K, k는 1/min이다:

<math display="block" aria-label="Numeric temperature-dependent teaching rate law"><mrow><mi>k</mi><mo>(</mo><mi>T</mi><mo>)</mo><mo>=</mo><mn>0.2</mn><mi>exp</mi><mo>[</mo><mn>6000</mn><mo>(</mo><mfrac><mn>1</mn><mn>330</mn></mfrac><mo>−</mo><mfrac><mn>1</mn><mi>T</mi></mfrac><mo>)</mo><mo>]</mo></mrow></math>

명시한 box 안에서 입력을 독립·균등 표본추출하고 정상상태 식으로 각 label을 계산한다. Seed 42로 재현 가능한 표본을 만든다.

| 분할 | 행 수 | 역할 |
| --- | --- | --- |
| Train | 400 | 계수 학습 |
| Validation | 120 | 모델 선택 비교 |
| Test | 160 | 최종 독립 평가 |

제공한 basis는 미리 고정되어 있다. 다른 basis나 capacity를 비교하면 validation을 쓰고 test는 남겨둔다. 새 simulator 표본이 새 실험 campaign과 같은 것은 아니다.

<!-- lecture-page -->

## 4. 입력 scaling과 10개 feature 학습하기

<math display="block" aria-label="Input scaling using the declared domain"><msub><mi>x̃</mi><mi>j</mi></msub><mo>=</mo><mn>2</mn><mfrac><mrow><msub><mi>x</mi><mi>j</mi></msub><mo>−</mo><msub><mi>l</mi><mi>j</mi></msub></mrow><mrow><msub><mi>u</mi><mi>j</mi></msub><mo>−</mo><msub><mi>l</mi><mi>j</mi></msub></mrow></mfrac><mo>−</mo><mn>1</mn></math>

[330 K, 5 min, 1.2 mol/L]의 scaled 입력은 약 [0, −0.111111, 0.142857]이다. Scaling에는 명시한 bounds를 쓰며 test 통계량을 사용하지 않는다.

Feature는 상수 1개 + 입력 3개 + 제곱 3개 + 두 입력의 곱 3개 = **10개**다. Train 400행에서 Φ의 shape는 (400, 10), Y는 (400, 2), B는 (10, 2)다.

<math display="block" aria-label="Least-squares training of the two-output baseline"><munder><mi>min</mi><mi mathvariant="bold">B</mi></munder><msubsup><mrow><mo>‖</mo><mi mathvariant="bold">Φ</mi><mi mathvariant="bold">B</mi><mo>−</mo><mi mathvariant="bold">Y</mi><mo>‖</mo></mrow><mi>F</mi><mn>2</mn></msubsup><mo>,</mo><mspace width="1em"/><mover><mi mathvariant="bold">y</mi><mo>^</mo></mover><mo>=</mo><mi>φ</mi><mo>(</mo><mi mathvariant="bold">x</mi><mo>)</mo><mi mathvariant="bold">B</mi></math>

`np.linalg.lstsq`로 B를 학습한다. 새 입력을 예측할 때 B는 고정한다. 파라미터 학습은 최적화 계산이며, 공정의 운전 조건을 선택하는 문제는 후반부에서 별도로 다룬다.

<!-- lecture-page -->

## 5. 정확도와 일관성을 따로 읽기

<math display="block" aria-label="Root mean squared error for one output"><msub><mtext>RMSE</mtext><mi>j</mi></msub><mo>=</mo><msqrt><mrow><mfrac><mn>1</mn><mi>N</mi></mfrac><munderover><mo>∑</mo><mrow><mi>n</mi><mo>=</mo><mn>1</mn></mrow><mi>N</mi></munderover><msup><mrow><mo>(</mo><msub><mover><mi>y</mi><mo>^</mo></mover><mrow><mi>n</mi><mi>j</mi></mrow></msub><mo>−</mo><msub><mi>y</mi><mrow><mi>n</mi><mi>j</mi></mrow></msub><mo>)</mo></mrow><mn>2</mn></msup></mrow></msqrt></math>

출력별로 예측에서 기준값을 빼고, 제곱하여 test 행들에서 평균한 뒤 제곱근을 구한다. 농도 RMSE는 mol/L, 전환율 RMSE는 무차원이다.

Seed 42 baseline의 농도 RMSE는 **0.032623 mol/L**, 전환율 RMSE는 **0.025608**이다. 평균과 함께 개별 오차도 확인한다.

<math display="block" aria-label="Consistency residual of concentration and conversion"><mrow><mi>r</mi><mo>=</mo><mover><msub><mi>C</mi><mi>A</mi></msub><mo>^</mo></mover><mo>+</mo><msub><mi>C</mi><mi>Af</mi></msub><mover><mi>X</mi><mo>^</mo></mover><mo>−</mo><msub><mi>C</mi><mi>Af</mi></msub></mrow></math>

유입 1.2에서 예측 C_A = 0.65, X = 0.45라면 r = 0.65 + 1.2 × 0.45 − 1.2 = **−0.01 mol/L**다. 예측 쌍은 정의한 전환율 관계를 정확히 만족하지 않는다. 물리적 일관성을 반영하는 방법은 4주차에서 공부한다.

<!-- lecture-page -->

## 6. 확인 문제·해설과 읽기자료

**먼저 계산:** 330 K, 10 min, 유입 1.2 mol/L에서 C_A와 X는 얼마인가? 두 출력을 학습하는 회귀 계수는 몇 개인가? 작은 train 오차만 보면 왜 오해할 수 있는가?

**확인 답:** kτ = 2이므로 C_A = 1.2/3 = **0.4 mol/L**, X = **2/3**다. B에는 출력별 10개, 총 **20개 계수**가 있다. Train 평가는 학습에 사용한 점을 다시 확인하므로 독립 오차가 더 클 수 있다.

직접 작성한 이 해설과 [1주차 실습]({{ page.lecture_note | relative_url }})을 따라간다. 선택 배경자료: Boyd·Vandenberghe, *Convex Optimization*, 2·4장의 affine map과 least-squares 문제([공식 교재 PDF](https://web.stanford.edu/~boyd/cvxbook/bv_cvxbook.pdf)).

2주차는 MLP, 3주차는 동적 예측으로 이어진다. 운전 목적함수·제약은 5–8주차에서 다시 다룬다.
