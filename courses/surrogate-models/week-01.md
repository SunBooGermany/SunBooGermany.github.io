---
layout: course-note
title: "Week 1: Process Prediction and Surrogate Modeling Basics"
title_ko: "1주차: 공정 예측과 surrogate 모델의 기초"
description: "Define a prediction task, fit a steady-state CSTR regression baseline, and evaluate independent prediction errors."
description_ko: "예측 문제를 정의하고 정상상태 CSTR 회귀 baseline을 학습한 뒤 독립 데이터에서 예측 오차를 평가합니다."
material_label: "Week 1"
material_label_ko: "1주차"
updated: "2026-11-12"
permalink: /courses/surrogate-models/week-01/
pdf_en: /assets/courses/surrogate-models/week-01-en.pdf
pdf_ko: /assets/courses/surrogate-models/week-01-ko.pdf
notebook: /assets/courses/surrogate-models/week-01/week01_lab.ipynb
lab_script: /assets/courses/surrogate-models/week-01/week01_lab.py
reading_note: /courses/surrogate-models/week-01-reading/
reading_pdf_en: /assets/courses/surrogate-models/week-01-reading-en.pdf
reading_pdf_ko: /assets/courses/surrogate-models/week-01-reading-ko.pdf
course_id: "surrogate-models"
practice_note: "/courses/surrogate-models/week-01-practice/"
lab_bundle: "/assets/courses/surrogate-models/week-01/week01-lab.zip"
---

## Outlet concentration prediction at specified operating conditions

<div class="lecture-columns" markdown="1">

<div markdown="1">

An engineer wants to predict outlet concentration and conversion at new temperature and residence-time settings.

Experiments or detailed process calculations take time at each condition. Could existing data help predict the response?

</div>

<div markdown="1">

<figure><img src="{{ '/assets/courses/surrogate-models/week-01/motivation-engineer.png' | relative_url }}" alt="An engineer examines temperature, residence time, and reactor response." /></figure>

</div>

</div>

<!-- lecture-page -->

## Prediction performance at new operating conditions

A model can reproduce its training data and still make large errors at new inputs. Units, operating range, and fixed assumptions also determine what its output means.

This week: prediction-task definition and independent evaluation. A small CSTR with a computable reference response lets us check each label.

### Predictor fitting and independent evaluation

1. Input, output, context, units, and domain definition
2. Steady-state reference data and separate train, validation, and test sets
3. Quadratic regression baseline and test errors in physical units
4. Concentration-conversion consistency and locations of large errors

Course roadmap: Week 2 learns multicomponent MLPs; Week 3 adds time response; Week 4 examines physical consistency. Weeks 5-7 address optimization formulations and model structure. Week 8 selects and revalidates operating conditions.

Deliverable: predictor with an independent evaluation.

<!-- lecture-page -->

## 1. Define the prediction contract

| Role | This example |
| --- | --- |
| Inputs | Temperature T [K], residence time τ [min], feed concentration C_Af [mol/L] |
| Outputs | Outlet concentration C_A [mol/L], conversion X [−] |
| Domain | 300–360 K; 1–10 min; 0.8–1.5 mol/L |
| Fixed context | Ideal mixing, constant volume/density, first-order A → B, declared rate parameters |
| Reference | Steady-state solution of the specified CSTR balance |

Feed concentration: a variable input in this prediction task.

One input row describes one operating condition. The same temperature with a different residence time or feed concentration asks a different question, so all three values travel together. The two outputs describe concentration and conversion after equilibration.

<!-- lecture-page -->

## 2. Reference CSTR model

Use an ideal, perfectly mixed, constant-volume, isothermal CSTR with a first-order reaction A → B, constant density, and no B in the feed. Reactor temperature T is an operating input.

<math display="block" aria-label="CSTR concentration balance"><mfrac><mrow><mi>d</mi><msub><mi>C</mi><mi>A</mi></msub></mrow><mrow><mi>d</mi><mi>t</mi></mrow></mfrac><mo>=</mo><mfrac><mrow><msub><mi>C</mi><mrow><mi>A</mi><mi>f</mi></mrow></msub><mo>−</mo><msub><mi>C</mi><mi>A</mi></msub></mrow><mi>τ</mi></mfrac><mo>−</mo><mi>k</mi><mo>(</mo><mi>T</mi><mo>)</mo><msub><mi>C</mi><mi>A</mi></msub></math>

Here concentrations are in mol/L, time and residence time in minutes, T in kelvin, and k in inverse minutes. The flow-to-volume ratio is the reciprocal of residence time. The inlet-outlet term and the reaction term therefore both have units of mol/(L·min).

The tank contains V·C_A of A. Inflow Q·C_Af minus outflow Q·C_A and reaction consumption V·k·C_A gives the rate of inventory change. Divide by V and substitute Q/V=1/τ to obtain the balance above.

<!-- lecture-page -->

## Temperature dependence and operating domain

Temperature-dependent rate constant:

<math display="block" aria-label="Educational temperature-dependent rate law"><mi>k</mi><mo>(</mo><mi>T</mi><mo>)</mo><mo>=</mo><msub><mi>k</mi><mtext>ref</mtext></msub><mi>exp</mi><mo>[</mo><mi>β</mi><mo>(</mo><mfrac><mn>1</mn><msub><mi>T</mi><mtext>ref</mtext></msub></mfrac><mo>−</mo><mfrac><mn>1</mn><mi>T</mi></mfrac><mo>)</mo><mo>]</mo></math>

| Parameter or input | Value or range | Interpretation |
| --- | --- | --- |
| Reference rate constant | 0.2 per minute | Rate at the reference temperature |
| Reference temperature | 330 K | Rate-law reference |
| β = E/R | 6000 K | Synthetic temperature-sensitivity parameter |
| Temperature | 300–360 K | Sampling and evaluation domain |
| Residence time | 1–10 min | Sampling and evaluation domain |
| Feed A concentration | 0.8–1.5 mol/L | Sampling domain; reference map at 1.2 |

At T=330 K the exponent is zero, so the exponential factor is one. Raising temperature decreases 1/T and increases the exponent and reaction rate. Use kelvin: inserting Celsius changes the reciprocal-temperature difference.

<!-- lecture-page -->

## 3. Derive the steady-state map

Set the time derivative to zero, multiply by residence time, and collect the terms containing outlet concentration. The resulting mapping and conversion are:

<math display="block" aria-label="CSTR steady concentration and conversion"><msub><mi>C</mi><mi>A</mi></msub><mo>=</mo><mfrac><msub><mi>C</mi><mrow><mi>A</mi><mi>f</mi></mrow></msub><mrow><mn>1</mn><mo>+</mo><mi>k</mi><mo>(</mo><mi>T</mi><mo>)</mo><mi>τ</mi></mrow></mfrac><mo>,</mo><mspace width="1em"/><mi>X</mi><mo>=</mo><mn>1</mn><mo>−</mo><mfrac><msub><mi>C</mi><mi>A</mi></msub><msub><mi>C</mi><mrow><mi>A</mi><mi>f</mi></mrow></msub></mfrac><mo>=</mo><mfrac><mrow><mi>k</mi><mo>(</mo><mi>T</mi><mo>)</mo><mi>τ</mi></mrow><mrow><mn>1</mn><mo>+</mo><mi>k</mi><mo>(</mo><mi>T</mi><mo>)</mo><mi>τ</mi></mrow></mfrac></math>

This gives a three-input, two-output map: temperature, residence time, and feed concentration map to outlet concentration and conversion. In this first-order model, conversion is independent of feed concentration.

Steady state does not stop the reaction. Inflow, outflow, and reaction continue, but their net effect is zero and tank concentration stays constant. The denominator combines outflow, represented by 1, with reaction over the residence time, represented by kτ.

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

## Read the reference response surface

<div class="lecture-columns" markdown="1">

<div markdown="1">

At 330 K and 5 min, conversion is 0.5; with feed 1.2 mol/L, outlet concentration is 0.6 mol/L.

</div>

<div markdown="1">

<figure><img src="{{ '/assets/courses/surrogate-models/week-01/conversion-map.png' | relative_url }}" alt="Reference CSTR conversion over the declared temperature and residence-time domain." /></figure>

</div>

</div>

At fixed feed, raising temperature or residence time increases kτ. The larger denominator lowers A concentration and raises conversion. Each point in the surface comes from evaluating these equations at another input.

<!-- lecture-page -->

## 4. Keep data roles separate

Independent samples within the declared box: 400 train, 120 validation, 160 test; seed 42.

Data roles: train for coefficient fitting; validation for model choices; test for the final error report. Supplied baseline: a fixed quadratic basis.

Error on points already used to choose coefficients does not measure error at new conditions. Repeated model selection also uses information from validation. A separate final test set therefore remains outside both fitting and selection.

<!-- lecture-page -->

## 5. Fit a small quadratic baseline

Scale each input using its declared lower and upper bounds:

<math display="block" aria-label="Input scaling using the declared domain"><msub><mi>x̃</mi><mi>j</mi></msub><mo>=</mo><mn>2</mn><mfrac><mrow><msub><mi>x</mi><mi>j</mi></msub><mo>−</mo><msub><mi>l</mi><mi>j</mi></msub></mrow><mrow><msub><mi>u</mi><mi>j</mi></msub><mo>−</mo><msub><mi>l</mi><mi>j</mi></msub></mrow></mfrac><mo>−</mo><mn>1</mn></math>

Ten features: a constant, three scaled inputs, three squares, and three pairwise products. Matrix dimensions: Φ 400 × 10; Y 400 × 2; B 10 × 2.

Coefficient fitting for both outputs: least squares

<math display="block" aria-label="Least-squares training of the two-output baseline"><munder><mi>min</mi><mi mathvariant="bold">B</mi></munder><msubsup><mrow><mo>‖</mo><mi mathvariant="bold">Φ</mi><mi mathvariant="bold">B</mi><mo>−</mo><mi mathvariant="bold">Y</mi><mo>‖</mo></mrow><mi>F</mi><mn>2</mn></msubsup><mo>,</mo><mspace width="1em"/><mover><mi mathvariant="bold">y</mi><mo>^</mo></mover><mo>=</mo><mi>φ</mi><mo>(</mo><mi mathvariant="bold">x</mi><mo>)</mo><mi mathvariant="bold">B</mi></math>

At prediction time, keep the fitted regression coefficients fixed and evaluate a new input.

Squares and cross-products represent curvature and interactions in the response surface. The predictor is quadratic in its inputs but linear in the unknown coefficients B, so fitting remains a linear least-squares problem.

<!-- lecture-page -->

## Fitting least-squares coefficients to three points

Use dimensionless data x=[−1,0,1], y=[1,2,2] and model b+ax. No line passes through all three points, so choose coefficients that minimize the sum of squared errors.

For errors eᵢ=b+axᵢ−yᵢ, differentiation gives 2∑eᵢ=0 for b and 2∑xᵢeᵢ=0 for a. Substituting ∑xᵢ=0, ∑xᵢ²=2, ∑yᵢ=5 and ∑xᵢyᵢ=1 gives 3b=5 and 2a=1.

| x | Target y | Prediction 5/3+x/2 | Error |
| --- | --- | --- | --- |
| −1 | 1 | 7/6 | 1/6 |
| 0 | 2 | 5/3 | −1/3 |
| 1 | 2 | 13/6 | 1/6 |

```python
import numpy as np
x = np.array([-1., 0., 1.])
phi = np.column_stack((np.ones(3), x))
coef = np.linalg.lstsq(phi, [1., 2., 2.], rcond=None)[0]
prediction = phi @ coef  # [7/6, 5/3, 13/6]
```

coef=[b,a] and the squared-error sum is 1/6. The CSTR fit extends the feature matrix to ten columns and applies the same calculation to each output column. `lstsq` solves the least-squares problem without explicitly forming an inverse.

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

The residence-time column is 2×(5−1)/(10−1)−1=−1/9; the feed column is 2×(1.2−0.8)/(1.5−0.8)−1=1/7. Squared features square these transformed values, not the physical values 5 and 1.2.

<!-- lecture-page -->

## 6. Evaluate errors and output consistency

Per-output error on the held-out test set:

<math display="block" aria-label="Root mean squared error for one output"><msub><mtext>RMSE</mtext><mi>j</mi></msub><mo>=</mo><msqrt><mrow><mfrac><mn>1</mn><mi>N</mi></mfrac><munderover><mo>∑</mo><mrow><mi>n</mi><mo>=</mo><mn>1</mn></mrow><mi>N</mi></munderover><msup><mrow><mo>(</mo><msub><mover><mi>y</mi><mo>^</mo></mover><mrow><mi>n</mi><mi>j</mi></mrow></msub><mo>−</mo><msub><mi>y</mi><mrow><mi>n</mi><mi>j</mi></mrow></msub><mo>)</mo></mrow><mn>2</mn></msup></mrow></msqrt></math>

Concentration RMSE is in mol/L. Conversion RMSE is dimensionless; 0.025608 corresponds to about 2.56 percentage points. Also check whether the predicted pair agrees with the definition of conversion.

<math display="block" aria-label="Consistency residual of concentration and conversion"><mrow><mi>r</mi><mo>=</mo><mover><msub><mi>C</mi><mi>A</mi></msub><mo>^</mo></mover><mo>+</mo><msub><mi>C</mi><mi>Af</mi></msub><mover><mi>X</mi><mo>^</mo></mover><mo>−</mo><msub><mi>C</mi><mi>Af</mi></msub></mrow></math>

The reference gives r = 0. An unconstrained two-output regression can disagree. A small average RMSE does not mean every condition has a small error.

Residual signs show overprediction and underprediction, but averaging signed residuals can cancel them. Squaring prevents that cancellation; the final square root restores the original output unit.

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

## Prediction results to reproduce

{% assign result = site.data.week01_results %}

| Check | Seed-42 baseline |
| --- | --- |
| Test concentration RMSE | {{ result.test_ca_rmse }} mol/L |
| Test conversion RMSE | {{ result.test_x_rmse }} |
| Test samples | 160 independent points |
| Model | Least squares on ten quadratic features |

Judge whether these errors are small enough for a particular use by inspecting parity plots and residuals together.

A conversion error of 0.025608 is about 2.56 percentage points on the 0–1 scale, not necessarily 2.56% relative error. Small average error can coexist with a large error at one condition; inspect the maximum and its input location as well.

<!-- lecture-page -->

## Prediction error across operating conditions

The diagonal represents prediction equal to reference. Compare concentration and conversion separately, then relate the larger errors to the input conditions.

<figure><img src="{{ '/assets/courses/surrogate-models/week-01/prediction-check.png' | relative_url }}" alt="Held-out reference-versus-prediction plots for concentration and conversion." /></figure>

Points above the diagonal are overpredictions; points below it are underpredictions. Systematic curvature differs from random scatter. Plot residuals against temperature and residence time to locate regions where the quadratic basis misses response curvature.

<!-- lecture-page -->

## 7. Run the prediction lab

Download the [notebook]({{ page.notebook | relative_url }}) or [script]({{ page.lab_script | relative_url }}), plus [requirements.txt]({{ '/assets/courses/surrogate-models/week-01/requirements.txt' | relative_url }}).

```bash
python -m pip install -r requirements.txt
python week01_lab.py --output-dir week01-results --seed 42
```

The default run saves the dataset, prediction metrics, the reference map, and test parity plots. Compare the [published dataset]({{ '/assets/courses/surrogate-models/week-01/week01_dataset.csv' | relative_url }}) and [recorded results]({{ '/assets/courses/surrogate-models/week-01/results.json' | relative_url }}).

Optional later-topic examples: retained in the script behind `--extensions`

<!-- lecture-page -->

## 8. Exercises and required submission

1. Derive C_A and X from the steady-state balance, with units.
2. Calculate the response at 330 K, 10 min, and feed 1.2 mol/L.
3. Count the quadratic features and state the dimensions of Φ, B, and Y.
4. Re-run with another seed and compare held-out errors. Explain why train error alone is insufficient.
5. For predicted C_A = 0.65 mol/L and X = 0.45 at feed 1.2 mol/L, calculate the consistency residual.

Submission: prediction specification, fitted baseline, and test report with units, parity plots, and consistency diagnostics.

Answer checks: C_A = 0.4 mol/L and X = 2/3 in Question 2; ten features; residual −0.01 mol/L in Question 5.

<!-- lecture-page -->

## Reading and the next prediction task

[Week 1 companion]({{ page.reading_note | relative_url }}) · [English PDF]({{ page.reading_pdf_en | relative_url }})

Using a predictor to select operating conditions requires objectives, operating constraints, and reference-model revalidation. Weeks 5-8 develop that process.

<!-- ko -->

## 운전 조건에 따른 출구 농도 예측

<div class="lecture-columns" markdown="1">

<div markdown="1">

공정 엔지니어가 새로운 온도와 체류시간에서 출구 농도와 전환율을 예측하려고 합니다.

조건마다 실험하거나 상세 공정 모델을 계산해야 한다면 시간이 걸립니다. 이미 확보한 데이터로 각 조건의 응답을 예측할 수 있을까요?

</div>

<div markdown="1">

<figure><img src="{{ '/assets/courses/surrogate-models/week-01/motivation-engineer.png' | relative_url }}" alt="온도와 체류시간에 따른 반응기 응답을 살펴보는 공정 엔지니어." /></figure>

</div>

</div>

<!-- lecture-page -->

## 새 운전 조건에서의 예측 성능

학습 데이터를 잘 따라가는 모델도 새로운 입력에서는 큰 오차를 낼 수 있습니다. 단위나 운전 범위, 고정한 가정이 달라지면 출력의 의미부터 달라집니다.

이번 주에는 예측 문제를 정의하고 독립 데이터로 평가하는 과정을 다뤄봅니다. 기준 응답을 직접 계산할 수 있는 작은 CSTR를 사용해 각 기준값을 확인합니다.

### 예측 모델의 학습과 독립 평가

1. 입력·출력·고정 조건(context)·단위·영역 정의
2. 정상상태 기준 데이터 생성과 train·validation·test 구분
3. 이차 회귀 기준 모델(baseline) 학습과 물리 단위의 test 오차
4. 농도·전환율의 일관성과 오차가 커지는 입력 조건

2주차는 다성분 MLP, 3주차는 시간 응답, 4주차는 물리적 일관성을 다룹니다. 5-7주차에서 최적화 정식화와 모델 구조를 배운 뒤, 8주차에는 운전 조건을 선택하고 기준 모델로 재검증합니다.

제출물: 독립 평가를 마친 예측 모델

<!-- lecture-page -->

## 1. 예측 문제의 입력과 출력 정의하기

| 역할 | 이 예제 |
| --- | --- |
| 입력 | 온도 T [K], 체류시간 τ [min], 유입 농도 C_Af [mol/L] |
| 출력 | 출구 농도 C_A [mol/L], 전환율 X [−] |
| 영역 | 300–360 K; 1–10 min; 0.8–1.5 mol/L |
| 고정 context | 이상적 혼합, 일정 부피·밀도, 1차 반응 A → B, 명시한 속도식 파라미터 |
| 기준값 | 정의한 CSTR 수지의 정상상태 해 |

유입 농도: 이 예측 문제의 가변 입력

입력 한 행은 운전 조건 하나입니다. 같은 온도라도 체류시간이나 유입 농도가 달라지면 다른 질문이 되므로 세 값을 함께 전달합니다. 출력 두 개는 그 조건에서 충분히 시간이 지난 뒤의 농도와 전환율입니다.

<!-- lecture-page -->

## 2. 기준 CSTR 모델

1차 반응 A → B가 일어나는 이상적인 완전혼합·일정 부피·등온 CSTR를 사용합니다. 밀도는 일정하고 유입물에는 B가 없으며, 반응기 온도 T를 조작변수로 둡니다.

<math display="block" aria-label="CSTR 농도 수지"><mfrac><mrow><mi>d</mi><msub><mi>C</mi><mi>A</mi></msub></mrow><mrow><mi>d</mi><mi>t</mi></mrow></mfrac><mo>=</mo><mfrac><mrow><msub><mi>C</mi><mrow><mi>A</mi><mi>f</mi></mrow></msub><mo>−</mo><msub><mi>C</mi><mi>A</mi></msub></mrow><mi>τ</mi></mfrac><mo>−</mo><mi>k</mi><mo>(</mo><mi>T</mi><mo>)</mo><msub><mi>C</mi><mi>A</mi></msub></math>

농도 단위는 mol/L, 시간과 체류시간은 min, T는 K, k는 1/min입니다. 유량/부피가 체류시간의 역수이므로 유입·유출 항과 반응 항의 단위는 모두 mol/(L·min)입니다.

탱크 안 A의 양은 V·C_A입니다. 유입량 Q·C_Af에서 유출량 Q·C_A와 반응 소모량 V·k·C_A를 빼면 축적량의 시간 변화가 됩니다. 부피 V로 나누고 Q/V=1/τ를 대입하면 위 식을 얻습니다.

<!-- lecture-page -->

## 온도 의존성과 운전 영역

온도에 따른 속도상수:

<math display="block" aria-label="교육용 온도 의존 속도식"><mi>k</mi><mo>(</mo><mi>T</mi><mo>)</mo><mo>=</mo><msub><mi>k</mi><mtext>ref</mtext></msub><mi>exp</mi><mo>[</mo><mi>β</mi><mo>(</mo><mfrac><mn>1</mn><msub><mi>T</mi><mtext>ref</mtext></msub></mfrac><mo>−</mo><mfrac><mn>1</mn><mi>T</mi></mfrac><mo>)</mo><mo>]</mo></math>

| 파라미터·입력 | 값·범위 | 의미 |
| --- | --- | --- |
| 기준 속도상수 | 0.2 /min | 기준 온도에서의 속도 |
| 기준 온도 | 330 K | 속도식의 기준 |
| β = E/R | 6000 K | 교육용 온도 민감도 파라미터 |
| 온도 | 300–360 K | Sampling·평가 영역 |
| 체류시간 | 1–10 min | Sampling·평가 영역 |
| 유입 A 농도 | 0.8–1.5 mol/L | Sampling 영역; 기준 지도에서는 1.2 |

T=330 K에서는 괄호가 0이므로 지수항이 1입니다. 온도가 올라가면 1/T가 작아져 지수항과 반응속도가 커집니다. 이 식에 섭씨 온도를 넣으면 역온도 차이가 바뀌므로 반드시 K로 계산합니다.

<!-- lecture-page -->

## 3. 정상상태 mapping 유도

시간 미분을 0으로 놓고 체류시간을 곱한 뒤 출구 농도가 포함된 항을 모으면 정상상태 관계식과 전환율을 얻습니다.

<math display="block" aria-label="CSTR 정상상태 농도와 전환율"><msub><mi>C</mi><mi>A</mi></msub><mo>=</mo><mfrac><msub><mi>C</mi><mrow><mi>A</mi><mi>f</mi></mrow></msub><mrow><mn>1</mn><mo>+</mo><mi>k</mi><mo>(</mo><mi>T</mi><mo>)</mo><mi>τ</mi></mrow></mfrac><mo>,</mo><mspace width="1em"/><mi>X</mi><mo>=</mo><mn>1</mn><mo>−</mo><mfrac><msub><mi>C</mi><mi>A</mi></msub><msub><mi>C</mi><mrow><mi>A</mi><mi>f</mi></mrow></msub></mfrac><mo>=</mo><mfrac><mrow><mi>k</mi><mo>(</mo><mi>T</mi><mo>)</mo><mi>τ</mi></mrow><mrow><mn>1</mn><mo>+</mo><mi>k</mi><mo>(</mo><mi>T</mi><mo>)</mo><mi>τ</mi></mrow></mfrac></math>

입력 3개: 온도·체류시간·유입 농도. 출력 2개: 출구 농도·전환율. 이 1차 반응 모델에서는 전환율이 유입 농도에 무관합니다.

정상상태는 반응이 멈춘 상태가 아닙니다. 유입·유출·반응이 계속되지만 그 합이 0이어서 탱크 농도가 일정합니다. 분모의 1은 유출, kτ는 체류시간 동안의 반응 소모에서 나옵니다.

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

## 기준 모델의 응답 곡면 읽기

<div class="lecture-columns" markdown="1">

<div markdown="1">

330 K·5 min에서 전환율은 0.5이고, 유입 농도가 1.2 mol/L이면 출구 농도는 0.6 mol/L입니다.

</div>

<div markdown="1">

<figure><img src="{{ '/assets/courses/surrogate-models/week-01/conversion-map.png' | relative_url }}" alt="명시한 온도·체류시간 영역에서 계산한 기준 CSTR 전환율." /></figure>

</div>

</div>

고정된 유입 농도에서 온도나 체류시간을 늘리면 kτ가 커집니다. 그러면 분모가 커져 A 농도는 내려가고 전환율은 올라갑니다. 그림의 각 점은 이 식을 다른 입력에 대입한 결과입니다.

<!-- lecture-page -->

## 4. Train·validation·test의 역할 나누기

Seed 42로 명시한 영역 안에서 train 400개, validation 120개, test 160개를 독립적으로 생성

데이터 역할: train은 계수 학습, validation은 모델 선택, test는 최종 오차 보고. 제공 기준 모델: 미리 정한 이차 기저함수

계수를 고를 때 이미 본 점의 오차는 새 조건의 오차를 대신하지 못합니다. 검증 오차로 모델을 여러 번 고른 뒤에는 검증 집합도 선택에 사용된 자료입니다. 마지막 시험 집합을 따로 남기는 이유입니다.

<!-- lecture-page -->

## 5. 작은 quadratic baseline 학습하기

명시한 하한과 상한으로 각 입력의 크기를 조정합니다.

<math display="block" aria-label="Input scaling using the declared domain"><msub><mi>x̃</mi><mi>j</mi></msub><mo>=</mo><mn>2</mn><mfrac><mrow><msub><mi>x</mi><mi>j</mi></msub><mo>−</mo><msub><mi>l</mi><mi>j</mi></msub></mrow><mrow><msub><mi>u</mi><mi>j</mi></msub><mo>−</mo><msub><mi>l</mi><mi>j</mi></msub></mrow></mfrac><mo>−</mo><mn>1</mn></math>

특징량(feature) 10개: 상수 1개, 크기를 조정한 입력 3개, 제곱 3개, 두 입력의 곱 3개. 행렬 크기: Φ 400 × 10, Y 400 × 2, B 10 × 2

학습: 최소제곱법(least squares)을 통한 두 출력의 회귀 계수 추정

<math display="block" aria-label="Least-squares training of the two-output baseline"><munder><mi>min</mi><mi mathvariant="bold">B</mi></munder><msubsup><mrow><mo>‖</mo><mi mathvariant="bold">Φ</mi><mi mathvariant="bold">B</mi><mo>−</mo><mi mathvariant="bold">Y</mi><mo>‖</mo></mrow><mi>F</mi><mn>2</mn></msubsup><mo>,</mo><mspace width="1em"/><mover><mi mathvariant="bold">y</mi><mo>^</mo></mover><mo>=</mo><mi>φ</mi><mo>(</mo><mi mathvariant="bold">x</mi><mo>)</mo><mi mathvariant="bold">B</mi></math>

예측할 때는 학습한 회귀 계수를 고정하고 새 입력의 출력을 계산합니다.

입력의 제곱과 곱은 반응 곡면의 굽음과 변수 간 관계를 표현합니다. 입력에 대해서는 이차식이지만 미지 계수 B에 대해서는 선형이므로 선형 최소제곱으로 계산할 수 있습니다.

<!-- lecture-page -->

## 세 데이터에서 최소제곱 계수 구하기

계수 학습을 작은 무차원 데이터 x=[−1,0,1], y=[1,2,2]로 계산합니다. 모델은 b+ax이며, 세 점을 모두 지나는 직선이 없으므로 오차 제곱합을 가장 작게 만듭니다.

오차 eᵢ=b+axᵢ−yᵢ에 대해 b로 미분하면 2∑eᵢ=0, a로 미분하면 2∑xᵢeᵢ=0입니다. ∑xᵢ=0, ∑xᵢ²=2, ∑yᵢ=5, ∑xᵢyᵢ=1을 넣으면 3b=5, 2a=1입니다.

| x | 기준 y | 예측 5/3+x/2 | 오차 |
| --- | --- | --- | --- |
| −1 | 1 | 7/6 | 1/6 |
| 0 | 2 | 5/3 | −1/3 |
| 1 | 2 | 13/6 | 1/6 |

```python
import numpy as np
x = np.array([-1., 0., 1.])
phi = np.column_stack((np.ones(3), x))
coef = np.linalg.lstsq(phi, [1., 2., 2.], rcond=None)[0]
prediction = phi @ coef  # [7/6, 5/3, 13/6]
```

coef=[b,a]이고 오차 제곱합은 1/6입니다. CSTR에서는 특성 열을 10개로 늘리고 출력 두 열에 같은 계산을 적용합니다. `lstsq`는 역행렬을 직접 만들지 않고 최소제곱 문제를 풉니다.

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

체류시간 열은 2×(5−1)/(10−1)−1=−1/9, 유입 농도 열은 2×(1.2−0.8)/(1.5−0.8)−1=1/7입니다. 제곱 열은 이 변환값을 제곱하며 원래 단위의 5나 1.2를 제곱하지 않습니다.

<!-- lecture-page -->

## 6. 예측 오차와 출력 일관성 확인하기

학습에 사용하지 않은 test 데이터의 출력별 오차:

<math display="block" aria-label="Root mean squared error for one output"><msub><mtext>RMSE</mtext><mi>j</mi></msub><mo>=</mo><msqrt><mrow><mfrac><mn>1</mn><mi>N</mi></mfrac><munderover><mo>∑</mo><mrow><mi>n</mi><mo>=</mo><mn>1</mn></mrow><mi>N</mi></munderover><msup><mrow><mo>(</mo><msub><mover><mi>y</mi><mo>^</mo></mover><mrow><mi>n</mi><mi>j</mi></mrow></msub><mo>−</mo><msub><mi>y</mi><mrow><mi>n</mi><mi>j</mi></mrow></msub><mo>)</mo></mrow><mn>2</mn></msup></mrow></msqrt></math>

농도 RMSE 단위: mol/L. 전환율 RMSE는 무차원이며 0.025608은 약 2.56%p에 해당합니다. 두 예측 출력이 전환율의 정의와도 일치하는지 확인

<math display="block" aria-label="Consistency residual of concentration and conversion"><mrow><mi>r</mi><mo>=</mo><mover><msub><mi>C</mi><mi>A</mi></msub><mo>^</mo></mover><mo>+</mo><msub><mi>C</mi><mi>Af</mi></msub><mover><mi>X</mi><mo>^</mo></mover><mo>−</mo><msub><mi>C</mi><mi>Af</mi></msub></mrow></math>

기준 모델에서는 r = 0이지만, 제약 없는 두 출력 회귀는 이 관계를 위반할 수 있습니다. 평균 RMSE만으로 모든 입력 조건의 오차가 작다고 판단해서는 안 됩니다.

잔차의 부호는 과대·과소 예측 방향을 나타내지만 평균하면 서로 상쇄될 수 있습니다. 제곱한 뒤 평균하면 그 상쇄를 막고, 마지막 제곱근으로 원래 출력 단위를 회복합니다.

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

## 재현할 예측 평가 결과

{% assign result = site.data.week01_results %}

| 확인 항목 | Seed 42 baseline |
| --- | --- |
| Test 농도 RMSE | {{ result.test_ca_rmse }} mol/L |
| Test 전환율 RMSE | {{ result.test_x_rmse }} |
| Test 표본 | 독립된 160개 점 |
| 모델 | 10개 quadratic feature의 least squares |

이 오차가 특정 용도에 충분히 작은지는 예측값과 기준값을 비교한 parity plot, 잔차(residual)를 함께 보고 판단합니다.

전환율 오차 0.025608은 전환율 자체의 약 2.56%라는 뜻이 아니라 0~1 척도에서 약 2.56 퍼센트포인트입니다. 작은 평균 오차와 특정 조건의 큰 오차가 함께 나타날 수 있어 최대 오차와 입력 위치도 확인합니다.

<!-- lecture-page -->

## 운전 조건별 예측 오차

대각선에서는 예측과 기준값이 같습니다. 농도와 전환율을 따로 비교한 뒤, 큰 오차가 나타난 점의 입력 조건을 살펴봅니다.

<figure><img src="{{ '/assets/courses/surrogate-models/week-01/prediction-check.png' | relative_url }}" alt="독립 test의 농도·전환율 기준값과 예측값 비교." /></figure>

대각선 위의 점은 과대 예측, 아래의 점은 과소 예측입니다. 한쪽으로 휘는 패턴은 단순한 무작위 산포와 다릅니다. 잔차를 온도·체류시간별로 다시 그리면 이차식이 놓친 곡률이 어느 구간에 모이는지 볼 수 있습니다.

<!-- lecture-page -->

## 7. 예측 실습 실행하기

[Notebook]({{ page.notebook | relative_url }}) 또는 [스크립트]({{ page.lab_script | relative_url }})와 [requirements.txt]({{ '/assets/courses/surrogate-models/week-01/requirements.txt' | relative_url }})를 받습니다.

```bash
python -m pip install -r requirements.txt
python week01_lab.py --output-dir week01-results --seed 42
```

실행하면 데이터, 예측 지표, 기준 응답 지도와 test parity plot이 저장됩니다. [공개 데이터]({{ '/assets/courses/surrogate-models/week-01/week01_dataset.csv' | relative_url }})와 [기록된 결과]({{ '/assets/courses/surrogate-models/week-01/results.json' | relative_url }})를 대조합니다.

후반부의 선택 예제는 스크립트의 `--extensions` 옵션으로 실행합니다.

<!-- lecture-page -->

## 8. 연습문제와 필수 제출물

1. 정상상태 수지에서 C_A와 X를 유도하고 단위를 확인
2. 330 K, 10 min, 유입 1.2 mol/L의 응답을 계산
3. 이차 특징량의 수와 Φ·B·Y의 차원을 적습니다.
4. 다른 seed로 다시 실행해 독립 평가 오차를 비교하고, train 오차만으로 충분하지 않은 이유를 설명합니다.
5. 유입 1.2 mol/L에서 예측 C_A = 0.65 mol/L, X = 0.45의 일관성 residual을 구합니다.

제출물: 예측 문제 정의, 학습한 기준 모델, 단위·parity plot·일관성 진단을 포함한 test 보고서

답 확인: 2번은 C_A = 0.4 mol/L, X = 2/3. 특징량은 10개이고, 5번 residual은 −0.01 mol/L

<!-- lecture-page -->

## 읽기자료와 다음 예측 문제

[1주차 읽기자료]({{ page.reading_note | relative_url }}) · [국문 PDF]({{ page.reading_pdf_ko | relative_url }})

예측 모델을 운전 조건 선택에 사용하려면 목적함수와 운전 제약을 정의하고 기준 공정 모델로 재검증해야 합니다. 이 과정은 5-8주차에서 다룹니다.
