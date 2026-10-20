---
layout: course-note
title: "Week 1: Process Prediction and Surrogate Modeling Basics"
title_ko: "1주차: 공정 예측과 surrogate 모델의 기초"
description: "Define a prediction task, fit a steady-state CSTR regression baseline, and evaluate independent prediction errors."
description_ko: "예측 문제를 정의하고 정상상태 CSTR 회귀 baseline을 학습한 뒤 독립 데이터에서 예측 오차를 평가합니다."
material_label: "Week 1"
material_label_ko: "1주차"
updated: "2026-10-20"
permalink: /courses/surrogate-models/week-01/
pdf_en: /assets/courses/surrogate-models/week-01-en.pdf
pdf_ko: /assets/courses/surrogate-models/week-01-ko.pdf
notebook: /assets/courses/surrogate-models/week-01/week01_lab.ipynb
lab_script: /assets/courses/surrogate-models/week-01/week01_lab.py
reading_note: /courses/surrogate-models/week-01-reading/
reading_pdf_en: /assets/courses/surrogate-models/week-01-reading-en.pdf
reading_pdf_ko: /assets/courses/surrogate-models/week-01-reading-ko.pdf
course_id: "surrogate-models"
---

## The morning meeting needs a prediction

<div class="lecture-columns" markdown="1">

<div markdown="1">

An engineer wants to predict outlet concentration and conversion at new temperature and residence-time settings.

Experiments or detailed process calculations take time at each condition. Could existing data help predict the response?

What would you need to know before trusting that prediction?

</div>

<div markdown="1">

<figure><img src="{{ '/assets/courses/surrogate-models/week-01/motivation-engineer.png' | relative_url }}" alt="An engineer examines temperature, residence time, and reactor response." /></figure>

</div>

</div>

<!-- lecture-page -->

## A good fit must also work at new conditions

A model can reproduce its training data and still make large errors at new inputs. Units, operating range, and fixed assumptions also determine what its output means.

This week we define a prediction task and evaluate it on independent data. A small CSTR with a computable reference response lets us check each label.

If training error is small, what evidence is still missing?

<!-- lecture-page -->

## Build a predictor, then check it

1. Define inputs, outputs, context, units, and the domain.
2. Generate steady-state reference data and keep train, validation, and test separate.
3. Fit a quadratic regression baseline and report test errors in physical units.
4. Inspect concentration-conversion consistency and where the errors occur.

Course roadmap: Week 2 learns multicomponent MLPs; Week 3 adds time response; Week 4 examines physical consistency. Weeks 5-7 address optimization formulations and model structure. Week 8 selects and revalidates operating conditions.

Submit a predictor with an independent evaluation. Later weeks examine what else is needed before using it to select operating conditions.

<!-- lecture-page -->

## 1. Define the prediction contract

| Role | This example |
| --- | --- |
| Inputs | Temperature T [K], residence time τ [min], feed concentration C_Af [mol/L] |
| Outputs | Outlet concentration C_A [mol/L], conversion X [−] |
| Domain | 300–360 K; 1–10 min; 0.8–1.5 mol/L |
| Fixed context | Ideal mixing, constant volume/density, first-order A → B, declared rate parameters |
| Reference | Steady-state solution of the specified CSTR balance |

Feed concentration varies in this prediction task. Fixing it for a later operating comparison is a separate choice.

<!-- lecture-page -->

## 2. A reference process we can check

Use an ideal, perfectly mixed, constant-volume, isothermal CSTR with a first-order reaction A → B, constant density, and no B in the feed. Reactor temperature T is an operating input.

<math display="block" aria-label="CSTR concentration balance"><mfrac><mrow><mi>d</mi><msub><mi>C</mi><mi>A</mi></msub></mrow><mrow><mi>d</mi><mi>t</mi></mrow></mfrac><mo>=</mo><mfrac><mrow><msub><mi>C</mi><mrow><mi>A</mi><mi>f</mi></mrow></msub><mo>−</mo><msub><mi>C</mi><mi>A</mi></msub></mrow><mi>τ</mi></mfrac><mo>−</mo><mi>k</mi><mo>(</mo><mi>T</mi><mo>)</mo><msub><mi>C</mi><mi>A</mi></msub></math>

Here concentrations are in mol/L, time and residence time in minutes, T in kelvin, and k in inverse minutes. The flow-to-volume ratio is the reciprocal of residence time. The inlet-outlet term and the reaction term therefore both have units of mol/(L·min).

<!-- lecture-page -->

## Temperature dependence and operating domain

The rate constant depends on temperature as follows:

<math display="block" aria-label="Educational temperature-dependent rate law"><mi>k</mi><mo>(</mo><mi>T</mi><mo>)</mo><mo>=</mo><msub><mi>k</mi><mtext>ref</mtext></msub><mi>exp</mi><mo>[</mo><mi>β</mi><mo>(</mo><mfrac><mn>1</mn><msub><mi>T</mi><mtext>ref</mtext></msub></mfrac><mo>−</mo><mfrac><mn>1</mn><mi>T</mi></mfrac><mo>)</mo><mo>]</mo></math>

| Parameter or input | Value or range | Interpretation |
| --- | --- | --- |
| Reference rate constant | 0.2 per minute | Rate at the reference temperature |
| Reference temperature | 330 K | Rate-law reference |
| β = E/R | 6000 K | Synthetic temperature-sensitivity parameter |
| Temperature | 300–360 K | Sampling and evaluation domain |
| Residence time | 1–10 min | Sampling and evaluation domain |
| Feed A concentration | 0.8–1.5 mol/L | Sampling domain; reference map at 1.2 |

<!-- lecture-page -->

## 3. Derive the steady-state map

Set the time derivative to zero, multiply by residence time, and collect the terms containing outlet concentration. The resulting mapping and conversion are:

<math display="block" aria-label="CSTR steady concentration and conversion"><msub><mi>C</mi><mi>A</mi></msub><mo>=</mo><mfrac><msub><mi>C</mi><mrow><mi>A</mi><mi>f</mi></mrow></msub><mrow><mn>1</mn><mo>+</mo><mi>k</mi><mo>(</mo><mi>T</mi><mo>)</mo><mi>τ</mi></mrow></mfrac><mo>,</mo><mspace width="1em"/><mi>X</mi><mo>=</mo><mn>1</mn><mo>−</mo><mfrac><msub><mi>C</mi><mi>A</mi></msub><msub><mi>C</mi><mrow><mi>A</mi><mi>f</mi></mrow></msub></mfrac><mo>=</mo><mfrac><mrow><mi>k</mi><mo>(</mo><mi>T</mi><mo>)</mo><mi>τ</mi></mrow><mrow><mn>1</mn><mo>+</mo><mi>k</mi><mo>(</mo><mi>T</mi><mo>)</mo><mi>τ</mi></mrow></mfrac></math>

This gives a three-input, two-output map: temperature, residence time, and feed concentration map to outlet concentration and conversion. In this first-order model, conversion is independent of feed concentration.

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

<!-- lecture-page -->

## 4. Keep data roles separate

Generate 400 train, 120 validation, and 160 test points independently inside the declared box, with seed 42.

Fit coefficients with train data. Use validation for model choices. Reserve test for the final error report. The supplied baseline has a fixed quadratic basis.

<!-- lecture-page -->

## 5. Fit a small quadratic baseline

Scale each input using its declared lower and upper bounds:

<math display="block" aria-label="Input scaling using the declared domain"><msub><mi>x̃</mi><mi>j</mi></msub><mo>=</mo><mn>2</mn><mfrac><mrow><msub><mi>x</mi><mi>j</mi></msub><mo>−</mo><msub><mi>l</mi><mi>j</mi></msub></mrow><mrow><msub><mi>u</mi><mi>j</mi></msub><mo>−</mo><msub><mi>l</mi><mi>j</mi></msub></mrow></mfrac><mo>−</mo><mn>1</mn></math>

Use ten features: a constant, three scaled inputs, three squares, and three pairwise products. The feature matrix Φ is 400 × 10; Y is 400 × 2; B is 10 × 2.

Fit both outputs by least squares:

<math display="block" aria-label="Least-squares training of the two-output baseline"><munder><mi>min</mi><mi mathvariant="bold">B</mi></munder><msubsup><mrow><mo>‖</mo><mi mathvariant="bold">Φ</mi><mi mathvariant="bold">B</mi><mo>−</mo><mi mathvariant="bold">Y</mi><mo>‖</mo></mrow><mi>F</mi><mn>2</mn></msubsup><mo>,</mo><mspace width="1em"/><mover><mi mathvariant="bold">y</mi><mo>^</mo></mover><mo>=</mo><mi>φ</mi><mo>(</mo><mi mathvariant="bold">x</mi><mo>)</mo><mi mathvariant="bold">B</mi></math>

At prediction time, keep the fitted regression coefficients fixed and evaluate a new input. Week 2 introduces neural networks.

<!-- lecture-page -->

## 6. Evaluate errors and output consistency

Evaluate each output on the held-out test set:

<math display="block" aria-label="Root mean squared error for one output"><msub><mtext>RMSE</mtext><mi>j</mi></msub><mo>=</mo><msqrt><mrow><mfrac><mn>1</mn><mi>N</mi></mfrac><munderover><mo>∑</mo><mrow><mi>n</mi><mo>=</mo><mn>1</mn></mrow><mi>N</mi></munderover><msup><mrow><mo>(</mo><msub><mover><mi>y</mi><mo>^</mo></mover><mrow><mi>n</mi><mi>j</mi></mrow></msub><mo>−</mo><msub><mi>y</mi><mrow><mi>n</mi><mi>j</mi></mrow></msub><mo>)</mo></mrow><mn>2</mn></msup></mrow></msqrt></math>

Concentration RMSE is in mol/L. Conversion RMSE is dimensionless; 0.025608 corresponds to about 2.56 percentage points. Also check whether the predicted pair agrees with the definition of conversion.

<math display="block" aria-label="Consistency residual of concentration and conversion"><mrow><mi>r</mi><mo>=</mo><mover><msub><mi>C</mi><mi>A</mi></msub><mo>^</mo></mover><mo>+</mo><msub><mi>C</mi><mi>Af</mi></msub><mover><mi>X</mi><mo>^</mo></mover><mo>−</mo><msub><mi>C</mi><mi>Af</mi></msub></mrow></math>

The reference gives r = 0. An unconstrained two-output regression can disagree. A small average RMSE does not mean every condition has a small error.

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

<!-- lecture-page -->

## Where does the predictor miss?

The diagonal represents prediction equal to reference. Compare concentration and conversion separately, then relate the larger errors to the input conditions.

<figure><img src="{{ '/assets/courses/surrogate-models/week-01/prediction-check.png' | relative_url }}" alt="Held-out reference-versus-prediction plots for concentration and conversion." /></figure>

<!-- lecture-page -->

## 7. Run the prediction lab

Download the [notebook]({{ page.notebook | relative_url }}) or [script]({{ page.lab_script | relative_url }}), plus [requirements.txt]({{ '/assets/courses/surrogate-models/week-01/requirements.txt' | relative_url }}).

```bash
python -m pip install -r requirements.txt
python week01_lab.py --output-dir week01-results --seed 42
```

The default run saves the dataset, prediction metrics, the reference map, and test parity plots. Compare the [published dataset]({{ '/assets/courses/surrogate-models/week-01/week01_dataset.csv' | relative_url }}) and [recorded results]({{ '/assets/courses/surrogate-models/week-01/results.json' | relative_url }}).

Optional later-topic examples are retained in the script behind `--extensions`.

<!-- lecture-page -->

## 8. Exercises and required submission

1. Derive C_A and X from the steady-state balance, with units.
2. Calculate the response at 330 K, 10 min, and feed 1.2 mol/L.
3. Count the quadratic features and state the dimensions of Φ, B, and Y.
4. Re-run with another seed and compare held-out errors. Explain why train error alone is insufficient.
5. For predicted C_A = 0.65 mol/L and X = 0.45 at feed 1.2 mol/L, calculate the consistency residual.

Submit a prediction specification, the fitted baseline, and a test report with units, parity plots, and consistency diagnostics.

Answer checks: C_A = 0.4 mol/L and X = 2/3 in Question 2; ten features; residual −0.01 mol/L in Question 5.

<!-- lecture-page -->

## Reading and the next prediction task

Work through the data definition, CSTR derivation, input scaling, regression, and independent evaluation in the [Week 1 companion]({{ page.reading_note | relative_url }}) or [English PDF]({{ page.reading_pdf_en | relative_url }}), then check your answers.

Week 2 asks whether one neural network can predict A, B, and C together, and how to evaluate each component. Time response belongs to Week 3.

Using a predictor to select operating conditions requires objectives, operating constraints, and reference-model revalidation. Weeks 5-8 develop that process.

<!-- ko -->

## 아침 회의: 이 조건에서 농도는 얼마일까?

<div class="lecture-columns" markdown="1">

<div markdown="1">

공정 엔지니어가 새로운 온도와 체류시간에서 출구 농도와 전환율을 예측하려고 합니다.

조건마다 실험하거나 상세 공정 모델을 계산해야 한다면 시간이 걸립니다. 이미 확보한 데이터로 각 조건의 응답을 예측할 수 있을까요?

그 예측을 믿으려면 무엇을 확인해야 할까요?

</div>

<div markdown="1">

<figure><img src="{{ '/assets/courses/surrogate-models/week-01/motivation-engineer.png' | relative_url }}" alt="온도와 체류시간에 따른 반응기 응답을 살펴보는 공정 엔지니어." /></figure>

</div>

</div>

<!-- lecture-page -->

## 학습한 점 밖에서도 잘 맞을까?

학습 데이터를 잘 따라가는 모델도 새로운 입력에서는 큰 오차를 낼 수 있습니다. 단위나 운전 범위, 고정한 가정이 달라지면 출력의 의미부터 달라집니다.

이번 주에는 예측 문제를 정의하고 독립 데이터로 평가하는 과정을 다뤄봅니다. 기준 응답을 직접 계산할 수 있는 작은 CSTR를 사용해 각 기준값을 확인합니다.

Train 오차가 작다는 사실 외에 어떤 근거가 더 필요할까요?

<!-- lecture-page -->

## 예측 모델을 만들고 독립적으로 확인하기

1. 입력·출력·고정 조건(context)·단위·영역을 정의합니다.
2. 정상상태 기준 데이터를 만들고 train·validation·test의 역할을 구분합니다.
3. 이차 회귀 기준 모델(baseline)을 학습하고 test 오차를 물리 단위로 보고합니다.
4. 농도와 전환율의 일관성, 오차가 커지는 입력 조건을 살펴봅니다.

2주차는 다성분 MLP, 3주차는 시간 응답, 4주차는 물리적 일관성을 다룹니다. 5-7주차에서 최적화 정식화와 모델 구조를 배운 뒤, 8주차에는 운전 조건을 선택하고 기준 모델로 재검증합니다.

이번 주에는 독립 평가를 마친 예측 모델을 제출합니다. 이 모델로 운전 조건까지 선택하려면 무엇이 더 필요한지는 이후 주차에서 다룹니다.

<!-- lecture-page -->

## 1. 예측 문제의 입력과 출력 정의하기

| 역할 | 이 예제 |
| --- | --- |
| 입력 | 온도 T [K], 체류시간 τ [min], 유입 농도 C_Af [mol/L] |
| 출력 | 출구 농도 C_A [mol/L], 전환율 X [−] |
| 영역 | 300–360 K; 1–10 min; 0.8–1.5 mol/L |
| 고정 context | 이상적 혼합, 일정 부피·밀도, 1차 반응 A → B, 명시한 속도식 파라미터 |
| 기준값 | 정의한 CSTR 수지의 정상상태 해 |

유입 농도는 이 예측 문제에서 달라지는 입력입니다. 이후 운전 조건을 비교할 때 한 값으로 고정할지는 별도로 정합니다.

<!-- lecture-page -->

## 2. 직접 확인할 수 있는 기준 공정

1차 반응 A → B가 일어나는 이상적인 완전혼합·일정 부피·등온 CSTR를 사용합니다. 밀도는 일정하고 유입물에는 B가 없으며, 반응기 온도 T를 조작변수로 둡니다.

<math display="block" aria-label="CSTR 농도 수지"><mfrac><mrow><mi>d</mi><msub><mi>C</mi><mi>A</mi></msub></mrow><mrow><mi>d</mi><mi>t</mi></mrow></mfrac><mo>=</mo><mfrac><mrow><msub><mi>C</mi><mrow><mi>A</mi><mi>f</mi></mrow></msub><mo>−</mo><msub><mi>C</mi><mi>A</mi></msub></mrow><mi>τ</mi></mfrac><mo>−</mo><mi>k</mi><mo>(</mo><mi>T</mi><mo>)</mo><msub><mi>C</mi><mi>A</mi></msub></math>

농도 단위는 mol/L, 시간과 체류시간은 min, T는 K, k는 1/min입니다. 유량/부피가 체류시간의 역수이므로 유입·유출 항과 반응 항의 단위는 모두 mol/(L·min)입니다.

<!-- lecture-page -->

## 온도 의존성과 운전 영역

속도상수는 온도에 따라 아래 식으로 계산합니다.

<math display="block" aria-label="교육용 온도 의존 속도식"><mi>k</mi><mo>(</mo><mi>T</mi><mo>)</mo><mo>=</mo><msub><mi>k</mi><mtext>ref</mtext></msub><mi>exp</mi><mo>[</mo><mi>β</mi><mo>(</mo><mfrac><mn>1</mn><msub><mi>T</mi><mtext>ref</mtext></msub></mfrac><mo>−</mo><mfrac><mn>1</mn><mi>T</mi></mfrac><mo>)</mo><mo>]</mo></math>

| 파라미터·입력 | 값·범위 | 의미 |
| --- | --- | --- |
| 기준 속도상수 | 0.2 /min | 기준 온도에서의 속도 |
| 기준 온도 | 330 K | 속도식의 기준 |
| β = E/R | 6000 K | 교육용 온도 민감도 파라미터 |
| 온도 | 300–360 K | Sampling·평가 영역 |
| 체류시간 | 1–10 min | Sampling·평가 영역 |
| 유입 A 농도 | 0.8–1.5 mol/L | Sampling 영역; 기준 지도에서는 1.2 |

<!-- lecture-page -->

## 3. 정상상태 mapping 유도

시간 미분을 0으로 놓고 체류시간을 곱한 뒤 출구 농도가 포함된 항을 모으면 정상상태 관계식과 전환율을 얻습니다.

<math display="block" aria-label="CSTR 정상상태 농도와 전환율"><msub><mi>C</mi><mi>A</mi></msub><mo>=</mo><mfrac><msub><mi>C</mi><mrow><mi>A</mi><mi>f</mi></mrow></msub><mrow><mn>1</mn><mo>+</mo><mi>k</mi><mo>(</mo><mi>T</mi><mo>)</mo><mi>τ</mi></mrow></mfrac><mo>,</mo><mspace width="1em"/><mi>X</mi><mo>=</mo><mn>1</mn><mo>−</mo><mfrac><msub><mi>C</mi><mi>A</mi></msub><msub><mi>C</mi><mrow><mi>A</mi><mi>f</mi></mrow></msub></mfrac><mo>=</mo><mfrac><mrow><mi>k</mi><mo>(</mo><mi>T</mi><mo>)</mo><mi>τ</mi></mrow><mrow><mn>1</mn><mo>+</mo><mi>k</mi><mo>(</mo><mi>T</mi><mo>)</mo><mi>τ</mi></mrow></mfrac></math>

온도·체류시간·유입 농도라는 세 입력에서 출구 농도와 전환율을 계산합니다. 이 1차 반응 모델에서는 전환율이 유입 농도에 무관합니다.

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

<!-- lecture-page -->

## 4. Train·validation·test의 역할 나누기

Seed 42로 명시한 영역 안에서 train 400개, validation 120개, test 160개를 독립적으로 생성합니다.

Train으로 계수를 학습하고 validation으로 모델을 선택하며, test는 최종 오차 보고에 사용합니다. 제공하는 기준 모델의 이차 기저함수는 미리 정해져 있습니다.

<!-- lecture-page -->

## 5. 작은 quadratic baseline 학습하기

명시한 하한과 상한으로 각 입력의 크기를 조정합니다.

<math display="block" aria-label="Input scaling using the declared domain"><msub><mi>x̃</mi><mi>j</mi></msub><mo>=</mo><mn>2</mn><mfrac><mrow><msub><mi>x</mi><mi>j</mi></msub><mo>−</mo><msub><mi>l</mi><mi>j</mi></msub></mrow><mrow><msub><mi>u</mi><mi>j</mi></msub><mo>−</mo><msub><mi>l</mi><mi>j</mi></msub></mrow></mfrac><mo>−</mo><mn>1</mn></math>

상수 1개, 크기를 조정한 입력 3개, 제곱 3개, 두 입력의 곱 3개로 총 10개 특징량(feature)을 만듭니다. Φ는 400 × 10, Y는 400 × 2, B는 10 × 2 행렬입니다.

최소제곱법(least squares)으로 두 출력의 회귀 계수를 학습합니다.

<math display="block" aria-label="Least-squares training of the two-output baseline"><munder><mi>min</mi><mi mathvariant="bold">B</mi></munder><msubsup><mrow><mo>‖</mo><mi mathvariant="bold">Φ</mi><mi mathvariant="bold">B</mi><mo>−</mo><mi mathvariant="bold">Y</mi><mo>‖</mo></mrow><mi>F</mi><mn>2</mn></msubsup><mo>,</mo><mspace width="1em"/><mover><mi mathvariant="bold">y</mi><mo>^</mo></mover><mo>=</mo><mi>φ</mi><mo>(</mo><mi mathvariant="bold">x</mi><mo>)</mo><mi mathvariant="bold">B</mi></math>

예측할 때는 학습한 회귀 계수를 고정하고 새 입력의 출력을 계산합니다. 신경망은 2주차에서 다룹니다.

<!-- lecture-page -->

## 6. 예측 오차와 출력 일관성 확인하기

학습에 사용하지 않은 test 데이터에서 출력별 오차를 계산합니다.

<math display="block" aria-label="Root mean squared error for one output"><msub><mtext>RMSE</mtext><mi>j</mi></msub><mo>=</mo><msqrt><mrow><mfrac><mn>1</mn><mi>N</mi></mfrac><munderover><mo>∑</mo><mrow><mi>n</mi><mo>=</mo><mn>1</mn></mrow><mi>N</mi></munderover><msup><mrow><mo>(</mo><msub><mover><mi>y</mi><mo>^</mo></mover><mrow><mi>n</mi><mi>j</mi></mrow></msub><mo>−</mo><msub><mi>y</mi><mrow><mi>n</mi><mi>j</mi></mrow></msub><mo>)</mo></mrow><mn>2</mn></msup></mrow></msqrt></math>

농도 RMSE의 단위는 mol/L입니다. 전환율 RMSE는 무차원이며 0.025608은 약 2.56%p에 해당합니다. 두 예측 출력이 전환율의 정의와도 일치하는지 확인합니다.

<math display="block" aria-label="Consistency residual of concentration and conversion"><mrow><mi>r</mi><mo>=</mo><mover><msub><mi>C</mi><mi>A</mi></msub><mo>^</mo></mover><mo>+</mo><msub><mi>C</mi><mi>Af</mi></msub><mover><mi>X</mi><mo>^</mo></mover><mo>−</mo><msub><mi>C</mi><mi>Af</mi></msub></mrow></math>

기준 모델에서는 r = 0이지만, 제약 없는 두 출력 회귀는 이 관계를 위반할 수 있습니다. 평균 RMSE만으로 모든 입력 조건의 오차가 작다고 판단해서는 안 됩니다.

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

<!-- lecture-page -->

## 어떤 조건에서 예측이 빗나갈까?

대각선에서는 예측과 기준값이 같습니다. 농도와 전환율을 따로 비교한 뒤, 큰 오차가 나타난 점의 입력 조건을 살펴봅니다.

<figure><img src="{{ '/assets/courses/surrogate-models/week-01/prediction-check.png' | relative_url }}" alt="독립 test의 농도·전환율 기준값과 예측값 비교." /></figure>

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

1. 정상상태 수지에서 C_A와 X를 유도하고 단위를 확인합니다.
2. 330 K, 10 min, 유입 1.2 mol/L의 응답을 계산합니다.
3. 이차 특징량의 수와 Φ·B·Y의 차원을 적습니다.
4. 다른 seed로 다시 실행해 독립 평가 오차를 비교하고, train 오차만으로 충분하지 않은 이유를 설명합니다.
5. 유입 1.2 mol/L에서 예측 C_A = 0.65 mol/L, X = 0.45의 일관성 residual을 구합니다.

예측 문제 정의, 학습한 기준 모델, 단위·parity plot·일관성 진단을 포함한 test 보고서를 제출합니다.

답 확인: 2번은 C_A = 0.4 mol/L, X = 2/3입니다. 특징량은 10개이고, 5번 residual은 −0.01 mol/L입니다.

<!-- lecture-page -->

## 읽기자료와 다음 예측 문제

[1주차 읽기자료]({{ page.reading_note | relative_url }}) 또는 [국문 PDF]({{ page.reading_pdf_ko | relative_url }})에서 데이터 정의, CSTR 유도, 입력 크기 조정, 회귀와 독립 평가를 계산하고 답을 확인합니다.

2주차에는 한 신경망으로 A·B·C를 함께 예측하고 각 성분을 평가합니다. 시간 응답은 3주차에서 다룹니다.

예측 모델을 운전 조건 선택에 사용하려면 목적함수와 운전 제약을 정의하고 기준 공정 모델로 재검증해야 합니다. 이 과정은 5-8주차에서 다룹니다.
