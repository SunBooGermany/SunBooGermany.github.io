---
layout: course-note
title: "Week 1 Reading: Process Prediction"
title_ko: "1주차 읽기자료: 공정 예측과 회귀 baseline"
description: "A worked guide to prediction contracts, reference balances, data splits, regression, and independent evaluation."
description_ko: "예측 문제 정의, 기준 수지, 데이터 분할, 회귀 학습과 독립 평가를 직접 계산하는 읽기자료입니다."
material_label: "Week 1 reading"
material_label_ko: "1주차 읽기자료"
updated: "2026-11-12"
permalink: /courses/surrogate-models/week-01-reading/
pdf_en: /assets/courses/surrogate-models/week-01-reading-en.pdf
pdf_ko: /assets/courses/surrogate-models/week-01-reading-ko.pdf
lecture_note: /courses/surrogate-models/week-01/
course_id: "surrogate-models"
---

## 1. Definition of the prediction map

A surrogate predicts outputs from specified inputs over a declared domain. A label is a reference output paired with one input row.

| Role | This prediction task |
| --- | --- |
| Inputs | T: 300–360 K; τ: 1–10 min; C_Af: 0.8–1.5 mol/L |
| Outputs | C_A in mol/L; conversion X, dimensionless |
| Fixed context | Ideal, constant-volume, isothermal CSTR; first-order A → B; fixed rate parameters |
| Reference | Steady-state material-balance solution |

Vary feed concentration within the declared domain while keeping reaction assumptions and units the same across rows.

A temperature name and numerical value need units and an operating range to define the prediction task.

<!-- lecture-page -->

## 2. Derive the steady-state map

The ideal CSTR is perfectly mixed, isothermal, and constant-volume, with first-order reaction A → B. The balance is accumulation = inlet − outlet − reaction:

<math display="block" aria-label="CSTR concentration balance"><mfrac><mrow><mi>d</mi><msub><mi>C</mi><mi>A</mi></msub></mrow><mrow><mi>d</mi><mi>t</mi></mrow></mfrac><mo>=</mo><mfrac><mrow><msub><mi>C</mi><mrow><mi>A</mi><mi>f</mi></mrow></msub><mo>−</mo><msub><mi>C</mi><mi>A</mi></msub></mrow><mi>τ</mi></mfrac><mo>−</mo><mi>k</mi><mo>(</mo><mi>T</mi><mo>)</mo><msub><mi>C</mi><mi>A</mi></msub></math>

At steady state, set the derivative to zero. Multiply by residence time, move the concentration terms to the same side, and factor out outlet concentration. Dividing by the positive factor gives:

<math display="block" aria-label="CSTR steady concentration and conversion"><msub><mi>C</mi><mi>A</mi></msub><mo>=</mo><mfrac><msub><mi>C</mi><mrow><mi>A</mi><mi>f</mi></mrow></msub><mrow><mn>1</mn><mo>+</mo><mi>k</mi><mo>(</mo><mi>T</mi><mo>)</mo><mi>τ</mi></mrow></mfrac><mo>,</mo><mspace width="1em"/><mi>X</mi><mo>=</mo><mn>1</mn><mo>−</mo><mfrac><msub><mi>C</mi><mi>A</mi></msub><msub><mi>C</mi><mrow><mi>A</mi><mi>f</mi></mrow></msub></mfrac><mo>=</mo><mfrac><mrow><mi>k</mi><mo>(</mo><mi>T</mi><mo>)</mo><mi>τ</mi></mrow><mrow><mn>1</mn><mo>+</mo><mi>k</mi><mo>(</mo><mi>T</mi><mo>)</mo><mi>τ</mi></mrow></mfrac></math>

At 330 K, the rate constant is 0.2/min. At 5 min residence time, the product of rate and residence time is 1, so conversion is 0.5. A 1.2 mol/L feed gives a 0.6 mol/L outlet.

Conversion is independent of feed concentration in this first-order model.

<!-- lecture-page -->

## A steady-state calculation, step by step

At 330 K, τ=5 min, and C_Af=1.2 mol/L, k=0.2/min. Treat concentration as the unknown and rearrange the balance.

| Step | Calculation | Interpretation |
| --- | --- | --- |
| Zero accumulation | 0=(1.2−C_A)/5−0.2C_A | Flow and reaction balance |
| Multiply by residence time | 0=1.2−C_A−1.0C_A | Every term now in mol/L |
| Collect concentration | 2C_A=1.2 | Add coefficients of the unknown |
| Concentration and conversion | C_A=0.6; X=1−0.6/1.2=0.5 | Half of A converted |

Substitution gives a net flow term (1.2−0.6)/5=0.12 mol/(L·min) and reaction consumption 0.2×0.6=0.12. Their equality explains why concentration no longer changes.

<!-- lecture-page -->

## 3. Build independent train, validation, and test data

Assume the following rate law, with T in K and k in 1/min:

<math display="block" aria-label="Numeric temperature-dependent teaching rate law"><mrow><mi>k</mi><mo>(</mo><mi>T</mi><mo>)</mo><mo>=</mo><mn>0.2</mn><mi>exp</mi><mo>[</mo><mn>6000</mn><mo>(</mo><mfrac><mn>1</mn><mn>330</mn></mfrac><mo>−</mo><mfrac><mn>1</mn><mi>T</mi></mfrac><mo>)</mo><mo>]</mo></mrow></math>

Sample inputs independently and uniformly inside the declared box; compute each label with the steady-state equations. Seed 42 fixes a reproducible sample.

| Split | Rows | Role |
| --- | --- | --- |
| Train | 400 | Fit coefficients |
| Validation | 120 | Compare model choices |
| Test | 160 | Final held-out evaluation |

The provided basis is fixed in advance. If comparing another basis or capacity, use validation and leave test untouched.

<!-- lecture-page -->

## 4. Scale inputs and fit ten features

<math display="block" aria-label="Input scaling using the declared domain"><msub><mi>x̃</mi><mi>j</mi></msub><mo>=</mo><mn>2</mn><mfrac><mrow><msub><mi>x</mi><mi>j</mi></msub><mo>−</mo><msub><mi>l</mi><mi>j</mi></msub></mrow><mrow><msub><mi>u</mi><mi>j</mi></msub><mo>−</mo><msub><mi>l</mi><mi>j</mi></msub></mrow></mfrac><mo>−</mo><mn>1</mn></math>

At [330 K, 5 min, 1.2 mol/L], the scaled input is approximately [0, −0.111111, 0.142857]. The scaling uses declared bounds, not statistics computed from test data.

The feature row contains 1 constant + 3 inputs + 3 squares + 3 pairwise products = 10 features. For 400 train rows, Φ has shape (400, 10), Y (400, 2), and B (10, 2).

<math display="block" aria-label="Least-squares training of the two-output baseline"><munder><mi>min</mi><mi mathvariant="bold">B</mi></munder><msubsup><mrow><mo>‖</mo><mi mathvariant="bold">Φ</mi><mi mathvariant="bold">B</mi><mo>−</mo><mi mathvariant="bold">Y</mi><mo>‖</mo></mrow><mi>F</mi><mn>2</mn></msubsup><mo>,</mo><mspace width="1em"/><mover><mi mathvariant="bold">y</mi><mo>^</mo></mover><mo>=</mo><mi>φ</mi><mo>(</mo><mi mathvariant="bold">x</mi><mo>)</mo><mi mathvariant="bold">B</mi></math>

`np.linalg.lstsq` fits B. Keep B fixed when predicting new input rows.

<!-- lecture-page -->

## From one input row to ten features

Scaling [330, 5, 1.2] with the declared bounds gives [a,b,c]=[0,−1/9,1/7]. Inputs with different units and magnitudes move to the same −1 to 1 interval.

| Feature group | Values for this row |
| --- | --- |
| Constant and inputs | 1, 0, −0.111111, 0.142857 |
| Squares a²,b²,c² | 0, 0.012346, 0.020408 |
| Products ab,ac,bc | 0, 0, −0.015873 |

```python
phi = features(np.array([[330., 5., 1.2]]))
phi_train = features(train_x)
coef = np.linalg.lstsq(phi_train, train_y, rcond=None)[0]
prediction = phi @ coef
```

Shapes are (1,10), (10,2), and (1,2) for phi, coef, and prediction. Matrix multiplication weights and sums feature columns separately for each output. Preserve the training feature order at new inputs.

<!-- lecture-page -->

## 5. Prediction accuracy and output consistency

<math display="block" aria-label="Root mean squared error for one output"><msub><mtext>RMSE</mtext><mi>j</mi></msub><mo>=</mo><msqrt><mrow><mfrac><mn>1</mn><mi>N</mi></mfrac><munderover><mo>∑</mo><mrow><mi>n</mi><mo>=</mo><mn>1</mn></mrow><mi>N</mi></munderover><msup><mrow><mo>(</mo><msub><mover><mi>y</mi><mo>^</mo></mover><mrow><mi>n</mi><mi>j</mi></mrow></msub><mo>−</mo><msub><mi>y</mi><mrow><mi>n</mi><mi>j</mi></mrow></msub><mo>)</mo></mrow><mn>2</mn></msup></mrow></msqrt></math>

For each output, subtract the reference from the prediction, square, average over the test rows, and take the square root. Concentration RMSE is in mol/L; conversion RMSE is dimensionless.

The seed-42 baseline gives concentration RMSE 0.032623 mol/L and conversion RMSE 0.025608. Inspect individual errors as well as the averages.

<math display="block" aria-label="Consistency residual of concentration and conversion"><mrow><mi>r</mi><mo>=</mo><mover><msub><mi>C</mi><mi>A</mi></msub><mo>^</mo></mover><mo>+</mo><msub><mi>C</mi><mi>Af</mi></msub><mover><mi>X</mi><mo>^</mo></mover><mo>−</mo><msub><mi>C</mi><mi>Af</mi></msub></mrow></math>

For feed 1.2, prediction C_A = 0.65 and X = 0.45 gives r = 0.65 + 1.2 × 0.45 − 1.2 = −0.01 mol/L. The predicted pair is not exactly consistent with the defined conversion relation.

<!-- lecture-page -->

## From residuals to RMSE and consistency

Compare reference concentrations [0.60,0.40] mol/L with predictions [0.65,0.38] mol/L.

| Calculation | Result |
| --- | --- |
| Prediction minus reference | [0.05,−0.02] mol/L |
| Square | [0.0025,0.0004] (mol/L)² |
| Average | 0.00145 (mol/L)² |
| Square root | RMSE≈0.038079 mol/L |

```python
error = prediction - truth
rmse = np.sqrt(np.mean(error**2, axis=0))
```

axis=0 averages input rows and retains output columns. Averaging both outputs together would mix concentration with dimensionless conversion. Separately, C_A=0.65, X=0.45, C_Af=1.2 gives 0.65+1.2×0.45−1.2=−0.01 mol/L. Accuracy and the relation between outputs need separate checks.

<!-- lecture-page -->

## 6. Answer checks and readings

Try first: at 330 K, 10 min, and feed 1.2 mol/L, what are C_A and X? How many regression coefficients are fitted for two outputs? Why can a low training error be misleading?

Answer check: kτ = 2, so C_A = 1.2/3 = 0.4 mol/L and X = 2/3. B contains 20 coefficients: ten features for each of two outputs. Training evaluates the same points used for fitting; independent errors can be larger.

Check your calculations in the [Week 1 lab]({{ page.lecture_note | relative_url }}). Optional background: affine maps and least-squares problems in Chapters 2 and 4 of Boyd and Vandenberghe, *Convex Optimization* ([official book PDF](https://web.stanford.edu/~boyd/cvxbook/bv_cvxbook.pdf)).

<!-- ko -->

## 1. 예측 mapping의 정의

Surrogate는 명시한 영역에서 입력에 대응하는 출력을 예측하는 모델이며, label은 입력 한 행에 짝지은 기준 출력입니다.

| 역할 | 이 예측 문제 |
| --- | --- |
| 입력 | T: 300–360 K; τ: 1–10 min; C_Af: 0.8–1.5 mol/L |
| 출력 | C_A: mol/L; 전환율 X: 무차원 |
| 고정 context | 이상적·일정 부피·등온 CSTR, 1차 반응 A → B, 고정된 속도식 파라미터 |
| 기준값 | 정상상태 물질수지의 해 |

유입 농도는 명시한 영역에서 변화시키며, 반응 가정과 단위는 모든 데이터 행에 동일하게 적용합니다.

“온도”라는 이름과 수치에 단위·운전 범위를 함께 적어야 예측 문제를 정의할 수 있습니다.

<!-- lecture-page -->

## 2. 정상상태 mapping 직접 유도하기

이상적인 완전혼합·등온·일정 부피 CSTR에서 1차 반응 A → B가 일어납니다. 축적 = 유입 − 유출 − 반응으로 수지를 작성합니다.

<math display="block" aria-label="CSTR concentration balance"><mfrac><mrow><mi>d</mi><msub><mi>C</mi><mi>A</mi></msub></mrow><mrow><mi>d</mi><mi>t</mi></mrow></mfrac><mo>=</mo><mfrac><mrow><msub><mi>C</mi><mrow><mi>A</mi><mi>f</mi></mrow></msub><mo>−</mo><msub><mi>C</mi><mi>A</mi></msub></mrow><mi>τ</mi></mfrac><mo>−</mo><mi>k</mi><mo>(</mo><mi>T</mi><mo>)</mo><msub><mi>C</mi><mi>A</mi></msub></math>

정상상태에서는 미분을 0으로 둡니다. 체류시간을 곱해 농도 항을 한쪽에 모으고 출구 농도를 묶은 뒤, 양수인 계수로 나눕니다.

<math display="block" aria-label="CSTR steady concentration and conversion"><msub><mi>C</mi><mi>A</mi></msub><mo>=</mo><mfrac><msub><mi>C</mi><mrow><mi>A</mi><mi>f</mi></mrow></msub><mrow><mn>1</mn><mo>+</mo><mi>k</mi><mo>(</mo><mi>T</mi><mo>)</mo><mi>τ</mi></mrow></mfrac><mo>,</mo><mspace width="1em"/><mi>X</mi><mo>=</mo><mn>1</mn><mo>−</mo><mfrac><msub><mi>C</mi><mi>A</mi></msub><msub><mi>C</mi><mrow><mi>A</mi><mi>f</mi></mrow></msub></mfrac><mo>=</mo><mfrac><mrow><mi>k</mi><mo>(</mo><mi>T</mi><mo>)</mo><mi>τ</mi></mrow><mrow><mn>1</mn><mo>+</mo><mi>k</mi><mo>(</mo><mi>T</mi><mo>)</mo><mi>τ</mi></mrow></mfrac></math>

330 K에서 속도상수는 0.2/min입니다. 체류시간 5 min에서는 속도상수와 체류시간의 곱이 1이므로 전환율은 0.5이고, 유입 농도 1.2 mol/L에 대한 출구 농도는 0.6 mol/L입니다.

이 1차 반응 모델에서는 전환율이 유입 농도에 무관합니다.

<!-- lecture-page -->

## 정상상태 농도의 계산 순서

330 K, τ=5 min, C_Af=1.2 mol/L에서 k=0.2/min입니다. 농도를 미지수로 두고 수지를 한 줄씩 정리합니다.

| 단계 | 계산 | 의미 |
| --- | --- | --- |
| 축적 0 | 0=(1.2−C_A)/5−0.2C_A | 유입·유출·반응의 상쇄 |
| 체류시간 곱하기 | 0=1.2−C_A−1.0C_A | 각 항의 단위 mol/L |
| 농도 묶기 | 2C_A=1.2 | 같은 미지수의 계수 합 |
| 농도와 전환율 | C_A=0.6; X=1−0.6/1.2=0.5 | A의 절반 전환 |

역대입하면 유입·유출 차이는 (1.2−0.6)/5=0.12 mol/(L·min), 반응 소모도 0.2×0.6=0.12입니다. 두 항이 같으므로 농도가 더 변하지 않습니다.

<!-- lecture-page -->

## 3. 독립 train·validation·test 데이터 만들기

교육용 속도식에서 T의 단위는 K, k는 1/min입니다.

<math display="block" aria-label="Numeric temperature-dependent teaching rate law"><mrow><mi>k</mi><mo>(</mo><mi>T</mi><mo>)</mo><mo>=</mo><mn>0.2</mn><mi>exp</mi><mo>[</mo><mn>6000</mn><mo>(</mo><mfrac><mn>1</mn><mn>330</mn></mfrac><mo>−</mo><mfrac><mn>1</mn><mi>T</mi></mfrac><mo>)</mo><mo>]</mo></mrow></math>

명시한 영역 안에서 입력을 독립·균등 표본추출하고 정상상태 식으로 각 기준값을 계산합니다. Seed 42를 사용하면 같은 표본을 재현할 수 있습니다.

| 분할 | 행 수 | 역할 |
| --- | --- | --- |
| Train | 400 | 계수 학습 |
| Validation | 120 | 모델 선택 비교 |
| Test | 160 | 최종 독립 평가 |

제공한 기저함수는 미리 고정되어 있습니다. 다른 기저함수나 모델 크기를 비교할 때는 validation을 사용하고 test는 최종 평가에 남겨둡니다.

<!-- lecture-page -->

## 4. 입력 scaling과 10개 feature 학습하기

<math display="block" aria-label="Input scaling using the declared domain"><msub><mi>x̃</mi><mi>j</mi></msub><mo>=</mo><mn>2</mn><mfrac><mrow><msub><mi>x</mi><mi>j</mi></msub><mo>−</mo><msub><mi>l</mi><mi>j</mi></msub></mrow><mrow><msub><mi>u</mi><mi>j</mi></msub><mo>−</mo><msub><mi>l</mi><mi>j</mi></msub></mrow></mfrac><mo>−</mo><mn>1</mn></math>

[330 K, 5 min, 1.2 mol/L]의 크기를 조정한 입력은 약 [0, −0.111111, 0.142857]입니다. 이 조정에는 명시한 bounds를 사용하며 test 통계량은 사용하지 않습니다.

특징량은 상수 1개 + 입력 3개 + 제곱 3개 + 두 입력의 곱 3개 = 10개입니다. Train 400행에서 Φ의 크기는 (400, 10), Y는 (400, 2), B는 (10, 2)입니다.

<math display="block" aria-label="Least-squares training of the two-output baseline"><munder><mi>min</mi><mi mathvariant="bold">B</mi></munder><msubsup><mrow><mo>‖</mo><mi mathvariant="bold">Φ</mi><mi mathvariant="bold">B</mi><mo>−</mo><mi mathvariant="bold">Y</mi><mo>‖</mo></mrow><mi>F</mi><mn>2</mn></msubsup><mo>,</mo><mspace width="1em"/><mover><mi mathvariant="bold">y</mi><mo>^</mo></mover><mo>=</mo><mi>φ</mi><mo>(</mo><mi mathvariant="bold">x</mi><mo>)</mo><mi mathvariant="bold">B</mi></math>

`np.linalg.lstsq`로 B를 학습한 뒤 새 입력을 예측할 때는 고정합니다.

<!-- lecture-page -->

## 입력 한 행에서 열 개의 특성으로

[330, 5, 1.2]를 정해진 범위로 변환하면 [a,b,c]=[0,−1/9,1/7]입니다. 단위와 크기가 다른 입력을 같은 −1~1 범위로 옮깁니다.

| 특성 묶음 | 해당 행의 값 |
| --- | --- |
| 상수와 입력 | 1, 0, −0.111111, 0.142857 |
| 제곱 a²,b²,c² | 0, 0.012346, 0.020408 |
| 곱 ab,ac,bc | 0, 0, −0.015873 |

```python
phi = features(np.array([[330., 5., 1.2]]))
phi_train = features(train_x)
coef = np.linalg.lstsq(phi_train, train_y, rcond=None)[0]
prediction = phi @ coef
```

phi는 (1,10), coef는 (10,2), prediction은 (1,2)입니다. 행렬곱은 특성 열마다 계수를 곱해 두 출력별로 합산합니다. 새 입력에서도 학습 때 사용한 특성 순서를 유지합니다.

<!-- lecture-page -->

## 5. 예측 정확도와 출력 일관성 평가

<math display="block" aria-label="Root mean squared error for one output"><msub><mtext>RMSE</mtext><mi>j</mi></msub><mo>=</mo><msqrt><mrow><mfrac><mn>1</mn><mi>N</mi></mfrac><munderover><mo>∑</mo><mrow><mi>n</mi><mo>=</mo><mn>1</mn></mrow><mi>N</mi></munderover><msup><mrow><mo>(</mo><msub><mover><mi>y</mi><mo>^</mo></mover><mrow><mi>n</mi><mi>j</mi></mrow></msub><mo>−</mo><msub><mi>y</mi><mrow><mi>n</mi><mi>j</mi></mrow></msub><mo>)</mo></mrow><mn>2</mn></msup></mrow></msqrt></math>

출력별로 예측에서 기준값을 빼고 제곱한 값을 test 행 전체에서 평균한 뒤 제곱근을 구합니다. 농도 RMSE는 mol/L, 전환율 RMSE는 무차원입니다.

Seed 42 기준 모델의 농도 RMSE는 0.032623 mol/L, 전환율 RMSE는 0.025608입니다. 평균 오차와 함께 개별 입력의 오차도 확인합니다.

<math display="block" aria-label="Consistency residual of concentration and conversion"><mrow><mi>r</mi><mo>=</mo><mover><msub><mi>C</mi><mi>A</mi></msub><mo>^</mo></mover><mo>+</mo><msub><mi>C</mi><mi>Af</mi></msub><mover><mi>X</mi><mo>^</mo></mover><mo>−</mo><msub><mi>C</mi><mi>Af</mi></msub></mrow></math>

유입 1.2에서 예측 C_A = 0.65, X = 0.45라면 r = 0.65 + 1.2 × 0.45 − 1.2 = −0.01 mol/L입니다. 이 예측 쌍은 전환율의 정의를 정확히 만족하지 않습니다.

<!-- lecture-page -->

## 잔차에서 RMSE와 일관성 검사로

농도 기준값 [0.60,0.40] mol/L와 예측 [0.65,0.38] mol/L를 비교합니다.

| 계산 | 결과 |
| --- | --- |
| 예측−기준 | [0.05,−0.02] mol/L |
| 제곱 | [0.0025,0.0004] (mol/L)² |
| 평균 | 0.00145 (mol/L)² |
| 제곱근 | RMSE≈0.038079 mol/L |

```python
error = prediction - truth
rmse = np.sqrt(np.mean(error**2, axis=0))
```

axis=0은 여러 입력 행을 평균하고 출력 열은 남깁니다. 두 출력을 모두 평균하면 농도와 무차원 전환율을 섞게 됩니다. 별도로 C_A=0.65, X=0.45, C_Af=1.2를 검사하면 0.65+1.2×0.45−1.2=−0.01 mol/L입니다. 정확도와 출력 간 관계를 각각 검사합니다.

<!-- lecture-page -->

## 6. 확인 문제·해설과 읽기자료

먼저 계산해봅니다. 330 K, 10 min, 유입 1.2 mol/L에서 C_A와 X는 얼마일까요? 두 출력을 학습하는 회귀 계수는 몇 개이며, 작은 train 오차만 보면 왜 잘못 판단할 수 있을까요?

kτ = 2이므로 C_A = 1.2/3 = 0.4 mol/L, X = 2/3입니다. B에는 출력별 10개씩 총 20개 계수가 있습니다. Train 평가는 학습에 사용한 점을 다시 평가하므로 독립 데이터의 오차는 더 클 수 있습니다.

계산한 내용을 [1주차 실습]({{ page.lecture_note | relative_url }})에서 확인합니다. 선택 배경자료는 Boyd·Vandenberghe의 *Convex Optimization* 2·4장에 나오는 affine map과 least-squares 문제입니다([공식 교재 PDF](https://web.stanford.edu/~boyd/cvxbook/bv_cvxbook.pdf)).
