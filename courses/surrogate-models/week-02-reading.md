---
layout: course-note
title: "Week 2 Reading: Steady-State MLPs"
title_ko: "2주차 읽기자료: 정상상태 MLP 학습과 평가"
description: "Worked steady-state balances, parameter counts, scaling, backpropagation, training, and independent evaluation."
description_ko: "정상상태 수지, 파라미터 수, scaling, backpropagation, 학습과 독립 평가를 직접 계산하는 자료입니다."
material_label: "Week 2 reading"
material_label_ko: "2주차 읽기자료"
updated: "2026-10-09"
permalink: /courses/surrogate-models/week-02-reading/
pdf_en: /assets/courses/surrogate-models/week-02-reading-en.pdf
pdf_ko: /assets/courses/surrogate-models/week-02-reading-ko.pdf
lecture_note: /courses/surrogate-models/week-02/
course_id: "surrogate-models"
---

## 1. One reactor, three steady-state outputs

For consecutive first-order reactions A → B → C, setting each derivative to zero lets us solve in the order A, B, then C:

<math display="block" aria-label="Three-component steady-state mapping"><mtable columnalign="left"><mtr><mtd><mrow><msub><mi>C</mi><mi>A</mi></msub><mo>=</mo><mfrac><msub><mi>C</mi><mi>Af</mi></msub><mrow><mn>1</mn><mo>+</mo><msub><mi>k</mi><mn>1</mn></msub><mi>τ</mi></mrow></mfrac></mrow></mtd></mtr><mtr><mtd><mrow><msub><mi>C</mi><mi>B</mi></msub><mo>=</mo><mfrac><mrow><msub><mi>k</mi><mn>1</mn></msub><mi>τ</mi><msub><mi>C</mi><mi>Af</mi></msub></mrow><mrow><mo>(</mo><mrow><mn>1</mn><mo>+</mo><msub><mi>k</mi><mn>1</mn></msub><mi>τ</mi></mrow><mo>)</mo><mo>(</mo><mrow><mn>1</mn><mo>+</mo><msub><mi>k</mi><mn>2</mn></msub><mi>τ</mi></mrow><mo>)</mo></mrow></mfrac></mrow></mtd></mtr><mtr><mtd><mrow><msub><mi>C</mi><mi>C</mi></msub><mo>=</mo><msub><mi>k</mi><mn>2</mn></msub><mi>τ</mi><msub><mi>C</mi><mi>B</mi></msub></mrow></mtd></mtr></mtable></math>

At 330 K, the first and second reaction rates are 0.2/min and 0.1/min. With 5 min residence time and 1.2 mol/L feed, the three concentrations are **[0.6, 0.4, 0.2] mol/L**. Their sum is 1.2. These are the labels for one steady-state training row.

The input is [T, τ, C_Af] and the output is [C_A, C_B, C_C]. Each row is one steady operating condition.

<!-- lecture-page -->

## 2. Count parameters before training

A dense layer has one weight for each input–output pair and one bias per output. The steady MLP is 3 → 32 → 32 → 3:

| Layer | Count |
| --- | --- |
| First hidden layer | 3 × 32 + 32 = 128 |
| Second hidden layer | 32 × 32 + 32 = 1056 |
| Output layer | 32 × 3 + 3 = 99 |
| Total | **1283** |

<math display="block" aria-label="MLP forward computation"><mtable columnalign="left"><mtr><mtd><mrow><msub><mi mathvariant="bold">h</mi><mn>1</mn></msub><mo>=</mo><mtext>ReLU</mtext><mo>(</mo><msub><mi mathvariant="bold">W</mi><mn>1</mn></msub><mi mathvariant="bold">x̃</mi><mo>+</mo><msub><mi mathvariant="bold">b</mi><mn>1</mn></msub><mo>)</mo></mrow></mtd></mtr><mtr><mtd><mrow><msub><mi mathvariant="bold">h</mi><mn>2</mn></msub><mo>=</mo><mtext>ReLU</mtext><mo>(</mo><msub><mi mathvariant="bold">W</mi><mn>2</mn></msub><msub><mi mathvariant="bold">h</mi><mn>1</mn></msub><mo>+</mo><msub><mi mathvariant="bold">b</mi><mn>2</mn></msub><mo>)</mo></mrow></mtd></mtr><mtr><mtd><mrow><mover><mi mathvariant="bold">z</mi><mo>^</mo></mover><mo>=</mo><msub><mi mathvariant="bold">W</mi><mn>3</mn></msub><msub><mi mathvariant="bold">h</mi><mn>2</mn></msub><mo>+</mo><msub><mi mathvariant="bold">b</mi><mn>3</mn></msub></mrow></mtd></mtr></mtable></math>

ReLU applies max(0, value) to each hidden pre-activation. A linear output can return negative concentrations; nonnegativity and concentration-sum consistency must therefore be evaluated.

<!-- lecture-page -->

## 3. Scaling changes what the loss emphasizes

Use the declared bounds for input scaling. For output standardization, compute the mean and standard deviation from training data only; restore physical units before reporting concentration errors.

<math display="block" aria-label="Input scaling, output standardization, and inverse transformation"><mtable columnalign="left"><mtr><mtd><mrow><msub><mi>x̃</mi><mi>j</mi></msub><mo>=</mo><mn>2</mn><mfrac><mrow><msub><mi>x</mi><mi>j</mi></msub><mo>−</mo><msub><mi>l</mi><mi>j</mi></msub></mrow><mrow><msub><mi>u</mi><mi>j</mi></msub><mo>−</mo><msub><mi>l</mi><mi>j</mi></msub></mrow></mfrac><mo>−</mo><mn>1</mn></mrow></mtd></mtr><mtr><mtd><mrow><msub><mi>z</mi><mi>j</mi></msub><mo>=</mo><mfrac><mrow><msub><mi>y</mi><mi>j</mi></msub><mo>−</mo><msub><mi>μ</mi><mi>j</mi></msub></mrow><msub><mi>s</mi><mi>j</mi></msub></mfrac><mo>,</mo><mspace width="1em"/><msub><mover><mi>y</mi><mo>^</mo></mover><mi>j</mi></msub><mo>=</mo><msub><mi>μ</mi><mi>j</mi></msub><mo>+</mo><msub><mi>s</mi><mi>j</mi></msub><msub><mover><mi>z</mi><mo>^</mo></mover><mi>j</mi></msub></mrow></mtd></mtr></mtable></math>

<math display="block" aria-label="Mean squared error over samples and standardized output components"><mrow><mi>L</mi><mo>=</mo><mfrac><mn>1</mn><mrow><mn>3</mn><mi>N</mi></mrow></mfrac><munderover><mo>∑</mo><mrow><mi>n</mi><mo>=</mo><mn>1</mn></mrow><mi>N</mi></munderover><munderover><mo>∑</mo><mrow><mi>j</mi><mo>=</mo><mn>1</mn></mrow><mn>3</mn></munderover><msup><mrow><mo>(</mo><msub><mover><mi>z</mi><mo>^</mo></mover><mrow><mi>n</mi><mo>,</mo><mi>j</mi></mrow></msub><mo>−</mo><msub><mi>z</mi><mrow><mi>n</mi><mo>,</mo><mi>j</mi></mrow></msub><mo>)</mo></mrow><mn>2</mn></msup></mrow></math>

A raw squared error is weighted by the inverse squared training standard deviation. With standard deviations approximately 0.283 for A and 0.110 for B, the same raw squared error receives about **6.62 times** the weight for B compared with A.

This explains a weighting choice, not a guarantee of better predictions. Compare each component's test RMSE and the concentration-sum residual. See the [official MSE definition](https://docs.pytorch.org/docs/stable/generated/torch.nn.MSELoss.html).

<!-- lecture-page -->

## 4. One backward pass, one parameter update

Use a 3 → 2 → 3 network with `W1 = [[1, 0, 0], [0, 0, 1]]`, `W2 = [[1, 0], [0, 1], [1, 1]]`, and zero biases. Input [1, 0, −1] gives hidden pre-activation [1, −1], ReLU output [1, 0], and prediction [1, 0, 1]. Against target [0, 1, 0], the error is [1, −1, 1].

<math display="block" aria-label="Backpropagation gradients for one example"><mtable columnalign="left"><mtr><mtd><mrow><msub><mi mathvariant="bold">δ</mi><mn>2</mn></msub><mo>=</mo><mi mathvariant="bold">e</mi><mo>,</mo><msub><mi>∇</mi><msub><mi mathvariant="bold">W</mi><mn>2</mn></msub></msub><mi>L</mi><mo>=</mo><mi mathvariant="bold">e</mi><msup><mi mathvariant="bold">h</mi><mi>T</mi></msup><mo>=</mo><mrow><mo>[</mo><mtable><mtr><mtd><mn>1</mn></mtd><mtd><mn>0</mn></mtd></mtr><mtr><mtd><mn>-1</mn></mtd><mtd><mn>0</mn></mtd></mtr><mtr><mtd><mn>1</mn></mtd><mtd><mn>0</mn></mtd></mtr></mtable><mo>]</mo></mrow></mrow></mtd></mtr><mtr><mtd><mrow><msub><mi mathvariant="bold">δ</mi><mn>1</mn></msub><mo>=</mo><mo>(</mo><msup><msub><mi mathvariant="bold">W</mi><mn>2</mn></msub><mi>T</mi></msup><mi mathvariant="bold">e</mi><mo>)</mo><mo>⊙</mo><mrow><mo>[</mo><mtable><mtr><mtd><mn>1</mn></mtd></mtr><mtr><mtd><mn>0</mn></mtd></mtr></mtable><mo>]</mo></mrow><mo>=</mo><mrow><mo>[</mo><mtable><mtr><mtd><mn>2</mn></mtd></mtr><mtr><mtd><mn>0</mn></mtd></mtr></mtable><mo>]</mo></mrow></mrow></mtd></mtr><mtr><mtd><mrow><msub><mi>∇</mi><msub><mi mathvariant="bold">W</mi><mn>1</mn></msub></msub><mi>L</mi><mo>=</mo><msub><mi mathvariant="bold">δ</mi><mn>1</mn></msub><msup><mi mathvariant="bold">x</mi><mi>T</mi></msup><mo>=</mo><mrow><mo>[</mo><mtable><mtr><mtd><mn>2</mn></mtd><mtd><mn>0</mn></mtd><mtd><mn>-2</mn></mtd></mtr><mtr><mtd><mn>0</mn></mtd><mtd><mn>0</mn></mtd><mtd><mn>0</mn></mtd></mtr></mtable><mo>]</mo></mrow></mrow></mtd></mtr></mtable></math>

The output-weight gradient is error × hidden activation transposed. The hidden error uses the output weights and then the ReLU derivative; a negative pre-activation blocks that component's gradient.

Bias gradients are the corresponding error vectors. Updating **both weights and biases** with learning rate 0.1 gives the next prediction **[0.26, 0.14, 0.26]**. The loss ½‖prediction − target‖² falls from **1.5 to 0.4374**.

[PyTorch autograd](https://docs.pytorch.org/tutorials/beginner/basics/autogradqs_tutorial.html) performs this chain-rule propagation automatically; the notebook checks the hand calculation.

<!-- lecture-page -->

## 5. Read the training loop as a calculation

Each batch computes predictions and a loss, clears previously accumulated parameter gradients, differentiates the current loss, and applies an optimizer update:

```python
prediction = model(inputs)
loss = loss_function(prediction, targets)
optimizer.zero_grad()
loss.backward()
optimizer.step()
```

`loss.backward()` computes gradients; `optimizer.step()` changes parameters. Without clearing gradients, successive backward passes accumulate them.

Evaluate validation loss after an epoch and retain the weights at its minimum. Keep the test set out of parameter fitting and model selection. Compute prediction metrics after undoing output standardization.

Original explanations: PyTorch [training loop](https://docs.pytorch.org/tutorials/beginner/basics/optimization_tutorial.html) and [model construction](https://docs.pytorch.org/tutorials/beginner/basics/buildmodel_tutorial.html).

<!-- lecture-page -->

## 6. Diagnose the held-out predictions

Suppose a reference row is [0.6, 0.4, 0.2] mol/L and the predictor returns [0.62, 0.39, 0.19] mol/L.

The component errors are **[0.02, −0.01, −0.01] mol/L**. Both sums equal 1.2, so the concentration-sum residual is **zero**. Correct total concentration does not make each component exact.

**Check:** which quantities should a test report include, and which data may be used to choose the model?

**Answer check:** report A/B/C RMSE in physical units, concentration-sum residual, and minimum predicted concentration. Fit on train, choose with validation, and leave test out of both steps.

Return to the [Week 2 core lab]({{ page.lecture_note | relative_url }}).

<!-- ko -->

## 1. 하나의 반응기, 세 정상상태 출력

1차 연속반응 A → B → C에서 각 시간 미분을 0으로 놓으면 A, B, C 순서로 정상 농도를 구할 수 있다.

<math display="block" aria-label="Three-component steady-state mapping"><mtable columnalign="left"><mtr><mtd><mrow><msub><mi>C</mi><mi>A</mi></msub><mo>=</mo><mfrac><msub><mi>C</mi><mi>Af</mi></msub><mrow><mn>1</mn><mo>+</mo><msub><mi>k</mi><mn>1</mn></msub><mi>τ</mi></mrow></mfrac></mrow></mtd></mtr><mtr><mtd><mrow><msub><mi>C</mi><mi>B</mi></msub><mo>=</mo><mfrac><mrow><msub><mi>k</mi><mn>1</mn></msub><mi>τ</mi><msub><mi>C</mi><mi>Af</mi></msub></mrow><mrow><mo>(</mo><mrow><mn>1</mn><mo>+</mo><msub><mi>k</mi><mn>1</mn></msub><mi>τ</mi></mrow><mo>)</mo><mo>(</mo><mrow><mn>1</mn><mo>+</mo><msub><mi>k</mi><mn>2</mn></msub><mi>τ</mi></mrow><mo>)</mo></mrow></mfrac></mrow></mtd></mtr><mtr><mtd><mrow><msub><mi>C</mi><mi>C</mi></msub><mo>=</mo><msub><mi>k</mi><mn>2</mn></msub><mi>τ</mi><msub><mi>C</mi><mi>B</mi></msub></mrow></mtd></mtr></mtable></math>

330 K에서 첫 번째와 두 번째 반응의 속도상수는 0.2/min, 0.1/min이다. 체류시간 5 min·유입 농도 1.2 mol/L이면 세 농도는 **[0.6, 0.4, 0.2] mol/L**다. 합은 1.2다. 정상상태 학습 행 하나의 label이 된다.

입력은 [T, τ, C_Af], 출력은 [C_A, C_B, C_C]다. 한 행은 하나의 정상상태 운전 조건이다.

<!-- lecture-page -->

## 2. 학습 전에 파라미터 수 계산하기

Dense layer는 입력–출력 쌍마다 weight 하나, 출력마다 bias 하나를 갖는다. 정상상태 MLP는 3 → 32 → 32 → 3이다.

| Layer | 개수 |
| --- | --- |
| 첫 hidden layer | 3 × 32 + 32 = 128 |
| 두 번째 hidden layer | 32 × 32 + 32 = 1056 |
| Output layer | 32 × 3 + 3 = 99 |
| 합계 | **1283** |

<math display="block" aria-label="MLP forward computation"><mtable columnalign="left"><mtr><mtd><mrow><msub><mi mathvariant="bold">h</mi><mn>1</mn></msub><mo>=</mo><mtext>ReLU</mtext><mo>(</mo><msub><mi mathvariant="bold">W</mi><mn>1</mn></msub><mi mathvariant="bold">x̃</mi><mo>+</mo><msub><mi mathvariant="bold">b</mi><mn>1</mn></msub><mo>)</mo></mrow></mtd></mtr><mtr><mtd><mrow><msub><mi mathvariant="bold">h</mi><mn>2</mn></msub><mo>=</mo><mtext>ReLU</mtext><mo>(</mo><msub><mi mathvariant="bold">W</mi><mn>2</mn></msub><msub><mi mathvariant="bold">h</mi><mn>1</mn></msub><mo>+</mo><msub><mi mathvariant="bold">b</mi><mn>2</mn></msub><mo>)</mo></mrow></mtd></mtr><mtr><mtd><mrow><mover><mi mathvariant="bold">z</mi><mo>^</mo></mover><mo>=</mo><msub><mi mathvariant="bold">W</mi><mn>3</mn></msub><msub><mi mathvariant="bold">h</mi><mn>2</mn></msub><mo>+</mo><msub><mi mathvariant="bold">b</mi><mn>3</mn></msub></mrow></mtd></mtr></mtable></math>

ReLU는 hidden pre-activation마다 max(0, 값)을 적용한다. Linear output은 음수 농도도 반환할 수 있으므로, 비음성과 농도 합의 일관성을 따로 평가해야 한다.

<!-- lecture-page -->

## 3. Scaling은 loss의 강조점을 바꾼다

입력 scaling에는 명시한 bounds를 사용한다. 출력 표준화의 평균·표준편차는 train 데이터에서만 계산한다. 농도 오차를 보고할 때는 물리 단위로 되돌린다.

<math display="block" aria-label="Input scaling, output standardization, and inverse transformation"><mtable columnalign="left"><mtr><mtd><mrow><msub><mi>x̃</mi><mi>j</mi></msub><mo>=</mo><mn>2</mn><mfrac><mrow><msub><mi>x</mi><mi>j</mi></msub><mo>−</mo><msub><mi>l</mi><mi>j</mi></msub></mrow><mrow><msub><mi>u</mi><mi>j</mi></msub><mo>−</mo><msub><mi>l</mi><mi>j</mi></msub></mrow></mfrac><mo>−</mo><mn>1</mn></mrow></mtd></mtr><mtr><mtd><mrow><msub><mi>z</mi><mi>j</mi></msub><mo>=</mo><mfrac><mrow><msub><mi>y</mi><mi>j</mi></msub><mo>−</mo><msub><mi>μ</mi><mi>j</mi></msub></mrow><msub><mi>s</mi><mi>j</mi></msub></mfrac><mo>,</mo><mspace width="1em"/><msub><mover><mi>y</mi><mo>^</mo></mover><mi>j</mi></msub><mo>=</mo><msub><mi>μ</mi><mi>j</mi></msub><mo>+</mo><msub><mi>s</mi><mi>j</mi></msub><msub><mover><mi>z</mi><mo>^</mo></mover><mi>j</mi></msub></mrow></mtd></mtr></mtable></math>

<math display="block" aria-label="Mean squared error over samples and standardized output components"><mrow><mi>L</mi><mo>=</mo><mfrac><mn>1</mn><mrow><mn>3</mn><mi>N</mi></mrow></mfrac><munderover><mo>∑</mo><mrow><mi>n</mi><mo>=</mo><mn>1</mn></mrow><mi>N</mi></munderover><munderover><mo>∑</mo><mrow><mi>j</mi><mo>=</mo><mn>1</mn></mrow><mn>3</mn></munderover><msup><mrow><mo>(</mo><msub><mover><mi>z</mi><mo>^</mo></mover><mrow><mi>n</mi><mo>,</mo><mi>j</mi></mrow></msub><mo>−</mo><msub><mi>z</mi><mrow><mi>n</mi><mo>,</mo><mi>j</mi></mrow></msub><mo>)</mo></mrow><mn>2</mn></msup></mrow></math>

Raw squared error에는 train 표준편차 제곱의 역수가 가중치로 붙는다. A의 표준편차가 약 0.283, B가 0.110이면, 같은 raw squared error에 B는 A보다 약 **6.62배**의 가중치를 받는다.

이는 가중치 선택의 의미이며 더 좋은 예측을 보장하지 않는다. 성분별 test RMSE와 농도 합 residual을 비교한다. [PyTorch 공식 MSE 정의](https://docs.pytorch.org/docs/stable/generated/torch.nn.MSELoss.html)도 확인할 수 있다.

<!-- lecture-page -->

## 4. Backward 한 번, 파라미터 갱신 한 번

3 → 2 → 3 network의 초기값을 `W1 = [[1, 0, 0], [0, 0, 1]]`, `W2 = [[1, 0], [0, 1], [1, 1]]`, bias는 모두 0으로 둔다. 입력 [1, 0, −1]에 대한 hidden pre-activation은 [1, −1], ReLU 출력은 [1, 0], 예측은 [1, 0, 1]이다. Target [0, 1, 0]에 대한 오차는 [1, −1, 1]이다.

<math display="block" aria-label="Backpropagation gradients for one example"><mtable columnalign="left"><mtr><mtd><mrow><msub><mi mathvariant="bold">δ</mi><mn>2</mn></msub><mo>=</mo><mi mathvariant="bold">e</mi><mo>,</mo><msub><mi>∇</mi><msub><mi mathvariant="bold">W</mi><mn>2</mn></msub></msub><mi>L</mi><mo>=</mo><mi mathvariant="bold">e</mi><msup><mi mathvariant="bold">h</mi><mi>T</mi></msup><mo>=</mo><mrow><mo>[</mo><mtable><mtr><mtd><mn>1</mn></mtd><mtd><mn>0</mn></mtd></mtr><mtr><mtd><mn>-1</mn></mtd><mtd><mn>0</mn></mtd></mtr><mtr><mtd><mn>1</mn></mtd><mtd><mn>0</mn></mtd></mtr></mtable><mo>]</mo></mrow></mrow></mtd></mtr><mtr><mtd><mrow><msub><mi mathvariant="bold">δ</mi><mn>1</mn></msub><mo>=</mo><mo>(</mo><msup><msub><mi mathvariant="bold">W</mi><mn>2</mn></msub><mi>T</mi></msup><mi mathvariant="bold">e</mi><mo>)</mo><mo>⊙</mo><mrow><mo>[</mo><mtable><mtr><mtd><mn>1</mn></mtd></mtr><mtr><mtd><mn>0</mn></mtd></mtr></mtable><mo>]</mo></mrow><mo>=</mo><mrow><mo>[</mo><mtable><mtr><mtd><mn>2</mn></mtd></mtr><mtr><mtd><mn>0</mn></mtd></mtr></mtable><mo>]</mo></mrow></mrow></mtd></mtr><mtr><mtd><mrow><msub><mi>∇</mi><msub><mi mathvariant="bold">W</mi><mn>1</mn></msub></msub><mi>L</mi><mo>=</mo><msub><mi mathvariant="bold">δ</mi><mn>1</mn></msub><msup><mi mathvariant="bold">x</mi><mi>T</mi></msup><mo>=</mo><mrow><mo>[</mo><mtable><mtr><mtd><mn>2</mn></mtd><mtd><mn>0</mn></mtd><mtd><mn>-2</mn></mtd></mtr><mtr><mtd><mn>0</mn></mtd><mtd><mn>0</mn></mtd><mtd><mn>0</mn></mtd></mtr></mtable><mo>]</mo></mrow></mrow></mtd></mtr></mtable></math>

Output weight의 gradient는 오차 × hidden activation의 전치다. Hidden 오차에는 output weight와 ReLU 미분이 들어간다. 음수 pre-activation에서는 그 성분의 gradient가 막힌다.

Bias gradient는 해당 오차 벡터다. 학습률 0.1로 **weight와 bias를 모두** 갱신하면 다음 예측은 **[0.26, 0.14, 0.26]**이다. Loss ½‖예측 − target‖²는 **1.5에서 0.4374로** 줄어든다.

[PyTorch autograd](https://docs.pytorch.org/tutorials/beginner/basics/autogradqs_tutorial.html)가 이 chain rule 계산을 자동 수행한다. Notebook에서 손 계산을 확인한다.

<!-- lecture-page -->

## 5. 학습 loop를 계산 순서로 읽기

한 batch에서는 예측과 loss를 계산하고, 이전에 누적된 parameter gradient를 지운 뒤, 현재 loss를 미분하고 optimizer 갱신을 적용한다.

```python
prediction = model(inputs)
loss = loss_function(prediction, targets)
optimizer.zero_grad()
loss.backward()
optimizer.step()
```

`loss.backward()`는 gradient를 계산하고 `optimizer.step()`은 파라미터를 바꾼다. Gradient를 지우지 않으면 다음 backward 계산이 기존 gradient에 누적된다.

Epoch 뒤 validation loss를 평가하고 최솟값의 weight를 보관한다. Test는 파라미터 학습과 모델 선택에 사용하지 않는다. 예측 지표는 출력 표준화를 되돌린 뒤 계산한다.

원문 해설: PyTorch [학습 loop](https://docs.pytorch.org/tutorials/beginner/basics/optimization_tutorial.html), [모델 구성](https://docs.pytorch.org/tutorials/beginner/basics/buildmodel_tutorial.html).

<!-- lecture-page -->

## 6. 독립 예측을 진단하기

기준값이 [0.6, 0.4, 0.2] mol/L이고 predictor가 [0.62, 0.39, 0.19] mol/L를 반환한다고 하자.

성분별 오차는 **[0.02, −0.01, −0.01] mol/L**다. 두 농도 합은 모두 1.2이므로 농도 합 residual은 **0**이다. 전체 농도가 맞아도 각 성분이 정확한 것은 아니다.

**확인:** Test 보고서에 어떤 지표가 필요한가? 모델을 선택할 때 어떤 데이터를 사용해야 하는가?

**확인 답:** 물리 단위의 A·B·C RMSE, 농도 합 residual, 최소 예측 농도를 보고한다. Train으로 학습하고 validation으로 선택하며, test는 두 단계에 사용하지 않는다.

[2주차 필수 실습]({{ page.lecture_note | relative_url }})으로 돌아간다.
