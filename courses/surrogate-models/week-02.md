---
layout: course-note
title: "Week 2: Learning Multicomponent Steady-State Responses with MLPs"
title_ko: "2주차: MLP로 다성분 정상상태 응답 학습하기"
description: "Train and evaluate a steady-state three-output MLP; follow one gradient update and check concentration consistency."
description_ko: "정상상태 세 출력 MLP를 학습·평가하고, gradient 갱신 한 번과 농도 합의 일관성을 확인합니다."
material_label: "Week 2"
material_label_ko: "2주차"
updated: "2026-11-12"
permalink: /courses/surrogate-models/week-02/
pdf_en: /assets/courses/surrogate-models/week-02-en.pdf
pdf_ko: /assets/courses/surrogate-models/week-02-ko.pdf
notebook: /assets/courses/surrogate-models/week-02/week02_steady.ipynb
lab_script: /assets/courses/surrogate-models/week-02/week02_lab.py
reading_note: /courses/surrogate-models/week-02-reading/
reading_pdf_en: /assets/courses/surrogate-models/week-02-reading-en.pdf
reading_pdf_ko: /assets/courses/surrogate-models/week-02-reading-ko.pdf
course_id: "surrogate-models"
---

## Conversion and product composition in consecutive reactions

{% assign result = site.data.week02_results %}

<div class="lecture-columns" markdown="1">

<div markdown="1">

The desired intermediate is B in A → B → C. At short residence time little B forms; at long residence time more B reacts onward to C.

An engineer must predict all three outlet concentrations at each condition because conversion alone does not determine product composition.

Can one model predict A, B, and C consistently?

</div>

<div markdown="1">

<figure><img src="{{ '/assets/courses/surrogate-models/week-02/motivation-engineer.png' | relative_url }}" alt="A process engineer examines the three reactor products A, B, and C." /></figure>

</div>

</div>

<!-- lecture-page -->

## Componentwise prediction errors

All three concentrations have the same units, but their variation differs. An unscaled loss can emphasize one component.

This week: MLP outputs, one gradient update, and component-wise evaluation.

### Learn and check the steady-state MLP

1. Steady-state label derivation for A, B, and C
2. Data scaling, forward pass, backpropagation, and one parameter update
3. MLP training; comparison of component RMSE and concentration-sum residuals

<!-- lecture-page -->

## 1. A → B → C in a CSTR

Consider a perfectly mixed, constant-volume, constant-density, isothermal CSTR with consecutive first-order reactions A → B → C. The feed contains A; its B and C concentrations are zero. Temperature is an operating input. With concentrations in mol/L, temperature in K, and time in min, the balances are:

<math display="block" aria-label="Concentration balances for consecutive CSTR reactions"><mtable columnalign="left"><mtr><mtd><mrow><mfrac><mrow><mi>d</mi><msub><mi>C</mi><mi>A</mi></msub></mrow><mrow><mi>d</mi><mi>t</mi></mrow></mfrac><mo>=</mo><mfrac><mrow><msub><mi>C</mi><mi>Af</mi></msub><mo>−</mo><msub><mi>C</mi><mi>A</mi></msub></mrow><mi>τ</mi></mfrac><mo>−</mo><msub><mi>k</mi><mn>1</mn></msub><msub><mi>C</mi><mi>A</mi></msub></mrow></mtd></mtr><mtr><mtd><mrow><mfrac><mrow><mi>d</mi><msub><mi>C</mi><mi>B</mi></msub></mrow><mrow><mi>d</mi><mi>t</mi></mrow></mfrac><mo>=</mo><mo>−</mo><mfrac><msub><mi>C</mi><mi>B</mi></msub><mi>τ</mi></mfrac><mo>+</mo><msub><mi>k</mi><mn>1</mn></msub><msub><mi>C</mi><mi>A</mi></msub><mo>−</mo><msub><mi>k</mi><mn>2</mn></msub><msub><mi>C</mi><mi>B</mi></msub></mrow></mtd></mtr><mtr><mtd><mrow><mfrac><mrow><mi>d</mi><msub><mi>C</mi><mi>C</mi></msub></mrow><mrow><mi>d</mi><mi>t</mi></mrow></mfrac><mo>=</mo><mo>−</mo><mfrac><msub><mi>C</mi><mi>C</mi></msub><mi>τ</mi></mfrac><mo>+</mo><msub><mi>k</mi><mn>2</mn></msub><msub><mi>C</mi><mi>B</mi></msub></mrow></mtd></mtr></mtable></math>

The B balance contains both formation and consumption. Formation from A contributes +k₁C_A; onward reaction and outflow contribute −k₂C_B and −C_B/τ. Their competition creates the maximum in B.

<!-- lecture-page -->

## Rate constants and operating domain

Both rate constants have units of 1/min. Use the following temperature dependence:

<math display="block" aria-label="Temperature-dependent first-order rate constants"><mtable columnalign="left"><mtr><mtd><mrow><msub><mi>k</mi><mn>1</mn></msub><mo>(</mo><mi>T</mi><mo>)</mo><mo>=</mo><mn>0.2</mn><mi>exp</mi><mo>[</mo><mn>6000</mn><mo>(</mo><mfrac><mn>1</mn><mn>330</mn></mfrac><mo>−</mo><mfrac><mn>1</mn><mi>T</mi></mfrac><mo>)</mo><mo>]</mo></mrow></mtd></mtr><mtr><mtd><mrow><msub><mi>k</mi><mn>2</mn></msub><mo>(</mo><mi>T</mi><mo>)</mo><mo>=</mo><mn>0.1</mn><mi>exp</mi><mo>[</mo><mn>5000</mn><mo>(</mo><mfrac><mn>1</mn><mn>330</mn></mfrac><mo>−</mo><mfrac><mn>1</mn><mi>T</mi></mfrac><mo>)</mo><mo>]</mo></mrow></mtd></mtr></mtable></math>

| Quantity | Value or range |
| --- | --- |
| Reference temperature | 330 K |
| Reference k₁; k₂ | 0.2; 0.1 per minute |
| Temperature-sensitivity parameters | 6000 K; 5000 K |
| Temperature T | 300–360 K |
| Residence time τ | 1–10 min |
| Feed A concentration | 0.8–1.5 mol/L |

The three balances describe A consumption, B formation and consumption, and C formation. Adding them cancels the reaction terms.

<!-- lecture-page -->

## 2. Derive the three-output steady-state map

Set the time derivatives to zero and multiply each balance by τ. Collect the concentration terms:

<math display="block" aria-label="Steady-state balance equations"><mtable columnalign="left"><mtr><mtd><mrow><mo>(</mo><mrow><mn>1</mn><mo>+</mo><msub><mi>k</mi><mn>1</mn></msub><mi>τ</mi></mrow><mo>)</mo><msub><mi>C</mi><mi>A</mi></msub><mo>=</mo><msub><mi>C</mi><mi>Af</mi></msub></mrow></mtd></mtr><mtr><mtd><mrow><mo>(</mo><mrow><mn>1</mn><mo>+</mo><msub><mi>k</mi><mn>2</mn></msub><mi>τ</mi></mrow><mo>)</mo><msub><mi>C</mi><mi>B</mi></msub><mo>=</mo><msub><mi>k</mi><mn>1</mn></msub><mi>τ</mi><msub><mi>C</mi><mi>A</mi></msub></mrow></mtd></mtr><mtr><mtd><mrow><msub><mi>C</mi><mi>C</mi></msub><mo>=</mo><msub><mi>k</mi><mn>2</mn></msub><mi>τ</mi><msub><mi>C</mi><mi>B</mi></msub></mrow></mtd></mtr></mtable></math>

The first equation contains only A, so solve it directly. Substitute A into the second equation for B, then B into the last equation for C. This ordering avoids an iterative simultaneous solve for all three unknowns.

<!-- lecture-page -->

## Solve for A, B, and C

Solve in the order A, B, C:

<math display="block" aria-label="Three-component steady-state mapping"><mtable columnalign="left"><mtr><mtd><mrow><msub><mi>C</mi><mi>A</mi></msub><mo>=</mo><mfrac><msub><mi>C</mi><mi>Af</mi></msub><mrow><mn>1</mn><mo>+</mo><msub><mi>k</mi><mn>1</mn></msub><mi>τ</mi></mrow></mfrac></mrow></mtd></mtr><mtr><mtd><mrow><msub><mi>C</mi><mi>B</mi></msub><mo>=</mo><mfrac><mrow><msub><mi>k</mi><mn>1</mn></msub><mi>τ</mi><msub><mi>C</mi><mi>Af</mi></msub></mrow><mrow><mo>(</mo><mrow><mn>1</mn><mo>+</mo><msub><mi>k</mi><mn>1</mn></msub><mi>τ</mi></mrow><mo>)</mo><mo>(</mo><mrow><mn>1</mn><mo>+</mo><msub><mi>k</mi><mn>2</mn></msub><mi>τ</mi></mrow><mo>)</mo></mrow></mfrac></mrow></mtd></mtr><mtr><mtd><mrow><msub><mi>C</mi><mi>C</mi></msub><mo>=</mo><msub><mi>k</mi><mn>2</mn></msub><mi>τ</mi><msub><mi>C</mi><mi>B</mi></msub></mrow></mtd></mtr></mtable></math>

At 330 K, τ = 5 min, and feed = 1.2 mol/L, the concentrations are [0.6, 0.4, 0.2] mol/L. Their sum equals the feed concentration. These three outputs are the labels for the steady-state MLP.

Numerically, A=1.2/2=0.6, B=(0.2×5×0.6)/1.5=0.4, then C=0.1×5×0.4=0.2. The B denominator must retain both the outflow term 1 and the onward-reaction term 0.5.

<!-- lecture-page -->

## Nonmonotone response of intermediate B

At a fixed temperature, the B yield and its maximizing residence time follow from the expression for C_B:

<math display="block" aria-label="B yield and maximizing residence time at fixed temperature"><mrow><msub><mi>Y</mi><mi>B</mi></msub><mo>=</mo><mfrac><msub><mi>C</mi><mi>B</mi></msub><msub><mi>C</mi><mi>Af</mi></msub></mfrac><mo>=</mo><mfrac><mrow><msub><mi>k</mi><mn>1</mn></msub><mi>τ</mi></mrow><mrow><mo>(</mo><mrow><mn>1</mn><mo>+</mo><msub><mi>k</mi><mn>1</mn></msub><mi>τ</mi></mrow><mo>)</mo><mo>(</mo><mrow><mn>1</mn><mo>+</mo><msub><mi>k</mi><mn>2</mn></msub><mi>τ</mi></mrow><mo>)</mo></mrow></mfrac><mo>,</mo><mspace width="1em"/><msup><mi>τ</mi><mo>*</mo></msup><mo>=</mo><mfrac><mn>1</mn><msqrt><mrow><msub><mi>k</mi><mn>1</mn></msub><msub><mi>k</mi><mn>2</mn></msub></mrow></msqrt></mfrac></mrow></math>

Write the denominator as D=1+(k₁+k₂)τ+k₁k₂τ². Differentiation gives numerator k₁(D−τD′)=k₁(1−k₁k₂τ²). The positive denominator D² does not change its sign: yield increases before τ=1/√(k₁k₂) and decreases afterward.

<!-- lecture-page -->

## Compare the three concentration profiles

<div class="lecture-columns" markdown="1">

<div markdown="1">

At 330 K, τ* is about 7.07 min. Short residence times limit B formation; long residence times allow more B to react to C.

</div>

<div markdown="1">

<figure><img src="{{ '/assets/courses/surrogate-models/week-02/steady-profiles.png' | relative_url }}" alt="A, B, and C concentration responses to residence time at 330 kelvin, comparing the reference process and MLP." /><figcaption>Three-component response at 330 K. The B concentration has an interior maximum.</figcaption></figure>

</div>

</div>

<!-- lecture-page -->

## 3. Prepare the supervised dataset

Each row contains inputs [T, τ, C_Af] and outputs [C_A, C_B, C_C]. Input and output arrays both have shape (N, 3). Generate 400 train, 120 validation, and 160 test operating points within the table's bounds, then calculate their labels with the steady-state map.

The three concentrations have the same units but different variations. In the training data, their standard deviations are approximately [0.283, 0.110, 0.217] mol/L.

A, B, and C in one row belong to the same input. Shuffling components independently breaks input-label alignment. Apply splitting and shuffling to paired input and output rows.

<!-- lecture-page -->

## 4. Forward calculation and scaling

MLP architecture: 3 → 32 → 32 → 3; ReLU hidden layers and a linear output layer.

Hidden-layer calculation: weighted sum + bias → ReLU(a) = max(0, a). Positive values retained; negative values set to zero. Parameters fitted to concentration data: weights and biases.

<math display="block" aria-label="MLP forward computation"><mtable columnalign="left"><mtr><mtd><mrow><msub><mi mathvariant="bold">h</mi><mn>1</mn></msub><mo>=</mo><mtext>ReLU</mtext><mo>(</mo><msub><mi mathvariant="bold">W</mi><mn>1</mn></msub><mi mathvariant="bold">x̃</mi><mo>+</mo><msub><mi mathvariant="bold">b</mi><mn>1</mn></msub><mo>)</mo></mrow></mtd></mtr><mtr><mtd><mrow><msub><mi mathvariant="bold">h</mi><mn>2</mn></msub><mo>=</mo><mtext>ReLU</mtext><mo>(</mo><msub><mi mathvariant="bold">W</mi><mn>2</mn></msub><msub><mi mathvariant="bold">h</mi><mn>1</mn></msub><mo>+</mo><msub><mi mathvariant="bold">b</mi><mn>2</mn></msub><mo>)</mo></mrow></mtd></mtr><mtr><mtd><mrow><mover><mi mathvariant="bold">z</mi><mo>^</mo></mover><mo>=</mo><msub><mi mathvariant="bold">W</mi><mn>3</mn></msub><msub><mi mathvariant="bold">h</mi><mn>2</mn></msub><mo>+</mo><msub><mi mathvariant="bold">b</mi><mn>3</mn></msub></mrow></mtd></mtr></mtable></math>

| Layer | Weight shape | Bias shape | Parameters |
| --- | --- | --- | --- |
| Input → hidden 1 | 32 × 3 | 32 | 128 |
| Hidden 1 → hidden 2 | 32 × 32 | 32 | 1056 |
| Hidden 2 → output | 3 × 32 | 3 | 99 |
| Total | | | **1283** |

One neuron combines all input columns into one number. Each of 32 first-layer neurons has three weights and one bias, giving 32×(3+1)=128 parameters. Hidden layers repeat this computation for several learned features.

<!-- lecture-page -->

## Computing column equations as a batch matrix

The equations use column inputs. If batch code stores X as (N,3) rows, the first layer is `X @ W1.T + b1`, producing (N,32). Transposing the weights implements the same weighted sums with row storage; the 32 biases are applied to every data row.

| Array | Shape | Axis meanings |
| --- | --- | --- |
| X | N×3 | data rows, input variables |
| W1.T | 3×32 | input variables, hidden neurons |
| X @ W1.T | N×32 | data rows, hidden neurons |
| b1 | 32 | one bias per neuron |

Take input rows [1,0,−1] and [0,1,1], first-neuron weights [1,0,0], and bias 0.2. The first output column contains 1×1+0×0−1×0+0.2=1.2 and 0×1+1×0+1×0+0.2=0.2. The other 31 columns repeat this calculation with their own neuron weights.

ReLU then acts on each matrix entry separately. This operation does not mix different data rows.

<!-- lecture-page -->

## Scaling and the training loss

Scale the inputs with the declared lower and upper bounds. Standardize each output with its training mean μ and standard deviation s, and restore physical units after prediction:

<math display="block" aria-label="Input scaling, output standardization, and inverse transformation"><mtable columnalign="left"><mtr><mtd><mrow><msub><mi>x̃</mi><mi>j</mi></msub><mo>=</mo><mn>2</mn><mfrac><mrow><msub><mi>x</mi><mi>j</mi></msub><mo>−</mo><msub><mi>l</mi><mi>j</mi></msub></mrow><mrow><msub><mi>u</mi><mi>j</mi></msub><mo>−</mo><msub><mi>l</mi><mi>j</mi></msub></mrow></mfrac><mo>−</mo><mn>1</mn></mrow></mtd></mtr><mtr><mtd><mrow><msub><mi>z</mi><mi>j</mi></msub><mo>=</mo><mfrac><mrow><msub><mi>y</mi><mi>j</mi></msub><mo>−</mo><msub><mi>μ</mi><mi>j</mi></msub></mrow><msub><mi>s</mi><mi>j</mi></msub></mfrac><mo>,</mo><mspace width="1em"/><msub><mover><mi>y</mi><mo>^</mo></mover><mi>j</mi></msub><mo>=</mo><msub><mi>μ</mi><mi>j</mi></msub><mo>+</mo><msub><mi>s</mi><mi>j</mi></msub><msub><mover><mi>z</mi><mo>^</mo></mover><mi>j</mi></msub></mrow></mtd></mtr></mtable></math>

Loss: mean squared error across samples and standardized output components.

<math display="block" aria-label="Mean squared error over samples and standardized output components"><mrow><mi>L</mi><mo>=</mo><mfrac><mn>1</mn><mrow><mn>3</mn><mi>N</mi></mrow></mfrac><munderover><mo>∑</mo><mrow><mi>n</mi><mo>=</mo><mn>1</mn></mrow><mi>N</mi></munderover><munderover><mo>∑</mo><mrow><mi>j</mi><mo>=</mo><mn>1</mn></mrow><mn>3</mn></munderover><msup><mrow><mo>(</mo><msub><mover><mi>z</mi><mo>^</mo></mover><mrow><mi>n</mi><mo>,</mo><mi>j</mi></mrow></msub><mo>−</mo><msub><mi>z</mi><mrow><mi>n</mi><mo>,</mo><mi>j</mi></mrow></msub><mo>)</mo></mrow><mn>2</mn></msup></mrow></math>

Thus a concentration error is measured relative to that component's training variation. For example, the smaller B standard deviation gives its raw squared error a larger weight in this loss.

The same 0.01 mol/L error becomes about 0.0353 for A and 0.0909 for B after division by 0.283 and 0.110. Squaring makes B contribute about 6.62 times as much. Output scaling changes the relative emphasis in training as well as the numerical scale.

<!-- lecture-page -->

## 5. Backpropagation: one calculation

Calculation example: a 3 → 2 → 3 network with zero biases and the values below. Loss: L = ½‖ŷ − y‖². Learning rate: 0.1.

<math display="block" aria-label="Weights and data for one backpropagation example"><mtable columnalign="left"><mtr><mtd><mrow><mi mathvariant="bold">x</mi><mo>=</mo><mrow><mo>[</mo><mtable><mtr><mtd><mn>1</mn></mtd></mtr><mtr><mtd><mn>0</mn></mtd></mtr><mtr><mtd><mn>-1</mn></mtd></mtr></mtable><mo>]</mo></mrow><mo>,</mo><mi mathvariant="bold">y</mi><mo>=</mo><mrow><mo>[</mo><mtable><mtr><mtd><mn>0</mn></mtd></mtr><mtr><mtd><mn>1</mn></mtd></mtr><mtr><mtd><mn>0</mn></mtd></mtr></mtable><mo>]</mo></mrow></mrow></mtd></mtr><mtr><mtd><mrow><msub><mi mathvariant="bold">W</mi><mn>1</mn></msub><mo>=</mo><mrow><mo>[</mo><mtable><mtr><mtd><mn>1</mn></mtd><mtd><mn>0</mn></mtd><mtd><mn>0</mn></mtd></mtr><mtr><mtd><mn>0</mn></mtd><mtd><mn>0</mn></mtd><mtd><mn>1</mn></mtd></mtr></mtable><mo>]</mo></mrow><mo>,</mo><msub><mi mathvariant="bold">W</mi><mn>2</mn></msub><mo>=</mo><mrow><mo>[</mo><mtable><mtr><mtd><mn>1</mn></mtd><mtd><mn>0</mn></mtd></mtr><mtr><mtd><mn>0</mn></mtd><mtd><mn>1</mn></mtd></mtr><mtr><mtd><mn>1</mn></mtd><mtd><mn>1</mn></mtd></mtr></mtable><mo>]</mo></mrow></mrow></mtd></mtr></mtable></math>

Hidden pre-activation a, activation h, prediction, and error:

<math display="block" aria-label="Forward computation in the small network"><mrow><mi mathvariant="bold">a</mi><mo>=</mo><mrow><mo>[</mo><mtable><mtr><mtd><mn>1</mn></mtd></mtr><mtr><mtd><mn>-1</mn></mtd></mtr></mtable><mo>]</mo></mrow><mo>,</mo><mi mathvariant="bold">h</mi><mo>=</mo><mrow><mo>[</mo><mtable><mtr><mtd><mn>1</mn></mtd></mtr><mtr><mtd><mn>0</mn></mtd></mtr></mtable><mo>]</mo></mrow><mo>,</mo><mover><mi mathvariant="bold">y</mi><mo>^</mo></mover><mo>=</mo><mrow><mo>[</mo><mtable><mtr><mtd><mn>1</mn></mtd></mtr><mtr><mtd><mn>0</mn></mtd></mtr><mtr><mtd><mn>1</mn></mtd></mtr></mtable><mo>]</mo></mrow><mo>,</mo><mi mathvariant="bold">e</mi><mo>=</mo><mrow><mo>[</mo><mtable><mtr><mtd><mn>1</mn></mtd></mtr><mtr><mtd><mn>-1</mn></mtd></mtr><mtr><mtd><mn>1</mn></mtd></mtr></mtable><mo>]</mo></mrow></mrow></math>

The first hidden neuron reads input component 1 and the second reads component −1. ReLU leaves [1,0]. The output layer forms [first, second, their sum], yielding [1,0,1].

<!-- lecture-page -->

## The chain rule for one weight

The hand calculation uses L=½∑eⱼ² with eⱼ=ŷⱼ−yⱼ. Its derivative with respect to prediction ŷⱼ is eⱼ. Increasing output weight W₂,ji changes ŷⱼ at rate hᵢ.

| Derivative path | Factors | Value in the example |
| --- | --- | --- |
| W₂,A1 → ŷ_A → L | e_A×h₁ | 1×1=1 |
| W₂,B1 → ŷ_B → L | e_B×h₁ | −1×1=−1 |
| h₁ → three outputs → L | sum of weight×error | 1×1+0×(−1)+1×1=2 |
| W₁,13 → a₁ → h₁ → L | x₃×ReLU′(a₁)×2 | (−1)×1×2=−2 |

ReLU has derivative 1 for a>0 and 0 for a<0; this example avoids a=0. A bias enters the weighted sum with coefficient 1, so its derivative uses 1 instead of an input value.

δ denotes the loss derivative with respect to a layer's pre-activation; ⊙ multiplies matching components. For the actual mean-squared loss, the output derivative is 2e/(3N), with a different factor from the hand calculation's half squared sum.

<!-- lecture-page -->

## Gradients and the parameter update

The output error propagates through the output weights and the ReLU derivative:

<math display="block" aria-label="Backpropagation gradients for one example"><mtable columnalign="left"><mtr><mtd><mrow><msub><mi mathvariant="bold">δ</mi><mn>2</mn></msub><mo>=</mo><mi mathvariant="bold">e</mi><mo>,</mo><msub><mi>∇</mi><msub><mi mathvariant="bold">W</mi><mn>2</mn></msub></msub><mi>L</mi><mo>=</mo><mi mathvariant="bold">e</mi><msup><mi mathvariant="bold">h</mi><mi>T</mi></msup><mo>=</mo><mrow><mo>[</mo><mtable><mtr><mtd><mn>1</mn></mtd><mtd><mn>0</mn></mtd></mtr><mtr><mtd><mn>-1</mn></mtd><mtd><mn>0</mn></mtd></mtr><mtr><mtd><mn>1</mn></mtd><mtd><mn>0</mn></mtd></mtr></mtable><mo>]</mo></mrow></mrow></mtd></mtr><mtr><mtd><mrow><msub><mi mathvariant="bold">δ</mi><mn>1</mn></msub><mo>=</mo><mo>(</mo><msup><msub><mi mathvariant="bold">W</mi><mn>2</mn></msub><mi>T</mi></msup><mi mathvariant="bold">e</mi><mo>)</mo><mo>⊙</mo><mrow><mo>[</mo><mtable><mtr><mtd><mn>1</mn></mtd></mtr><mtr><mtd><mn>0</mn></mtd></mtr></mtable><mo>]</mo></mrow><mo>=</mo><mrow><mo>[</mo><mtable><mtr><mtd><mn>2</mn></mtd></mtr><mtr><mtd><mn>0</mn></mtd></mtr></mtable><mo>]</mo></mrow></mrow></mtd></mtr><mtr><mtd><mrow><msub><mi>∇</mi><msub><mi mathvariant="bold">W</mi><mn>1</mn></msub></msub><mi>L</mi><mo>=</mo><msub><mi mathvariant="bold">δ</mi><mn>1</mn></msub><msup><mi mathvariant="bold">x</mi><mi>T</mi></msup><mo>=</mo><mrow><mo>[</mo><mtable><mtr><mtd><mn>2</mn></mtd><mtd><mn>0</mn></mtd><mtd><mn>-2</mn></mtd></mtr><mtr><mtd><mn>0</mn></mtd><mtd><mn>0</mn></mtd><mtd><mn>0</mn></mtd></mtr></mtable><mo>]</mo></mrow></mrow></mtd></mtr></mtable></math>

The bias gradients are δ₁ and δ₂. Update every weight and bias with parameter ← parameter − 0.1 × gradient. The next forward calculation gives [0.26, 0.14, 0.26], and the loss decreases from 1.5 to 0.4374. The notebook checks these gradients using autograd.

The first hidden value connects to outputs A and C with unit weights, receiving their combined error 1+1=2. The second pre-activation is negative, so its ReLU derivative is zero. Its input weights and bias therefore do not move in this update.

<!-- lecture-page -->

## The second forward pass after updating parameters

Update both weights and biases with learning rate 0.1. Subtracting 0.1×[2,0,−2] from the first hidden weight [1,0,0] gives [0.8,0,0.2]; its bias becomes −0.2.

| Intermediate value | Updated calculation |
| --- | --- |
| First hidden pre-activation | 0.8×1+0×0+0.2×(−1)−0.2=0.4 |
| Second hidden pre-activation | −1 |
| ReLU output | [0.4,0] |
| Outputs A and C | 0.9×0.4−0.1=0.26 |
| Output B | 0.1×0.4+0.1=0.14 |

The new error is [0.26,−0.86,0.26]. Loss falls to (0.0676+0.7396+0.0676)/2=0.4374, but B remains below its target 1. One decrease does not complete training.

<!-- lecture-page -->

## 6. Train and evaluate the steady-state model

<div class="lecture-columns" markdown="1">

<div markdown="1">

Training: Adam, learning rate 0.001, batch size 64, up to 1400 epochs. Weight selection: minimum validation loss across epochs.

```python
prediction = model(inputs)
loss = loss_function(prediction, targets)
optimizer.zero_grad()
loss.backward()
optimizer.step()
```

</div>

<div markdown="1">

<figure><img src="{{ '/assets/courses/surrogate-models/week-02/steady-training.png' | relative_url }}" alt="Training and validation scaled mean squared errors for the steady-state MLP." /><figcaption>Training and validation loss. Prediction metrics below are computed after restoring mol/L units.</figcaption></figure>

</div>

</div>

<!-- lecture-page -->

## Values and changes inside the training loop

```python
prediction = model(inputs)
loss = loss_function(prediction, targets)
optimizer.zero_grad()
loss.backward()
optimizer.step()
```

| Line | Value produced or changed |
| --- | --- |
| model(inputs) | Batch predictions with current weights |
| loss_function | Prediction errors reduced to a scalar loss |
| zero_grad | Previous batch gradients cleared |
| backward | Current loss gradients for weights and biases |
| step | Parameters updated using gradients and optimizer state |

The hand calculation uses gradient descent; the lab uses Adam. Adam also uses gradient history, so its numerical update is not the same subtraction by 0.1 times the gradient. To assess the updated parameters, run a new forward pass after step.

<!-- lecture-page -->

## Adam's first update and the meaning of a batch

A batch is a group of rows used for one loss and gradient calculation. Splitting 400 rows into batches of 64 gives six full batches and a final batch of 16, hence seven updates per epoch. An epoch is one pass through the training data.

Adam accumulates a gradient average m and a squared-gradient average v. Start with m=v=0 and consider one weight with g=2, β₁=0.9 and β₂=0.999.

| Calculation | First-step value |
| --- | --- |
| m=0.9m+0.1g | 0.2 |
| v=0.999v+0.001g² | 0.004 |
| Correction for initialization at zero | m̂=0.2/(1−0.9)=2; v̂=0.004/(1−0.999)=4 |
| Update magnitude at learning rate 0.001 | 0.001×2/(√4+10⁻⁸)≈0.001 |

Plain gradient descent would subtract 0.001×2=0.002. Adam scales the step using accumulated gradient magnitudes, so equal learning rates need not give equal updates. Here ε=10⁻⁸ prevents a zero denominator.

[PyTorch Adam update definition](https://docs.pytorch.org/docs/stable/generated/torch.optim.Adam.html)

<!-- lecture-page -->

## Evaluate each output component

| Test RMSE, mol/L | A | B | C |
| --- | --- | --- | --- |
| Output scaling | {{ result.steady_a_rmse }} | {{ result.steady_b_rmse }} | {{ result.steady_c_rmse }} |
| Unscaled outputs | {{ result.unscaled_a_rmse }} | {{ result.unscaled_b_rmse }} | {{ result.unscaled_c_rmse }} |

In this comparison, output scaling reduces A and B RMSE; C RMSE is slightly higher. Evaluate each component rather than combining all three into one error number.

<figure><img src="{{ '/assets/courses/surrogate-models/week-02/steady-parity.png' | relative_url }}" alt="Reference-versus-predicted parity plots for the three concentrations on the test set." /><figcaption>Separate parity plots reveal each component's errors.</figcaption></figure>

<!-- lecture-page -->

## From standardized outputs to concentrations and errors

For a one-component calculation, take training mean μ=0.4 mol/L and standard deviation s=0.1 mol/L. Target concentration 0.45 becomes z=(0.45−0.4)/0.1=0.5.

| Quantity | Calculation |
| --- | --- |
| Standardized network prediction | ẑ=0.3 |
| Restore concentration | 0.4+0.1×0.3=0.43 mol/L |
| Standardized error | 0.3−0.5=−0.2 |
| Concentration error | 0.43−0.45=−0.02 mol/L |

```python
prediction = y_mean + y_scale * standardized_prediction
component_rmse = np.sqrt(((prediction - truth)**2).mean(axis=0))
sum_residual = prediction.sum(axis=1) - feed
```

The first line applies each column's mean and scale. axis=0 measures accuracy by component; axis=1 sums the three components at one condition. Swapping these axes computes a different quantity.

<!-- lecture-page -->

## Check the concentration sum

<math display="block" aria-label="Concentration-sum residual"><mrow><mi>r</mi><mo>=</mo><mover><msub><mi>C</mi><mi>A</mi></msub><mo>^</mo></mover><mo>+</mo><mover><msub><mi>C</mi><mi>B</mi></msub><mo>^</mo></mover><mo>+</mo><mover><msub><mi>C</mi><mi>C</mi></msub><mo>^</mo></mover><mo>−</mo><msub><mi>C</mi><mi>Af</mi></msub></mrow></math>

Its test RMSE is {{ result.steady_balance }} mol/L. Component prediction errors and the residual describe different aspects of the model.

Balance-consistent training labels do not force the sum of the three linear outputs to match the feed concentration.

For feed 1.2 mol/L, predictions [0.62, 0.41, 0.20] mol/L sum to 1.23 mol/L, giving r = 0.03 mol/L. A model predicting mole fractions can likewise return a sum different from one.

The sum residual equals the sum of component errors. Errors [0.02,−0.01,−0.01] sum to zero despite incorrect components. Small positive errors in all three components instead accumulate into a larger total-concentration error.

<!-- lecture-page -->

## Week 4 preview: concentration-sum constraints in the model

We can correct a prediction after training, or include a constraint-respecting transformation in the training calculation.

| Approach | Where the correction enters |
| --- | --- |
| Post-training mapping/projection | Train the raw predictor, then correct its outputs. |
| KKT-hPINN | Apply a fixed affine projection using the input and raw prediction before the loss, and at inference. |

<math display="block" aria-label="Constraint-aware training flow"><mrow><mi mathvariant="bold">x</mi><mo>→</mo><msub><mi>f</mi><mi>θ</mi></msub><mo>→</mo><mover><mi mathvariant="bold">y</mi><mo>^</mo></mover><mo>→</mo><msub><mi>Π</mi><mi mathvariant="bold">x</mi></msub><mo>→</mo><mover><mi mathvariant="bold">y</mi><mo>~</mo></mover><mo>→</mo><mtext>loss</mtext></mrow></math>

KKT-hPINN computes the loss on projected outputs and backpropagates through the projection layer. Projection coefficients stay fixed while the MLP weights learn with the transformation in place.

The projection layer satisfies the specified linear equalities up to numerical arithmetic; nonnegativity needs an additional constraint.

Source: Chen et al. (2024), [DOI: 10.1016/j.compchemeng.2024.108764](https://doi.org/10.1016/j.compchemeng.2024.108764).

<!-- lecture-page -->

## 7. Run the required steady-state lab

Download the [steady-state notebook]({{ page.notebook | relative_url }}).

```bash
python -m pip install -r requirements.txt
python week02_lab.py --mode steady --output-dir week02-results
```

Evaluate the trained predictor by component RMSE and concentration-sum residual.

<!-- lecture-page -->

## 8. Core exercises and submission

1. Derive C_A, C_B, and C_C and verify their sum. Explain the nonmonotone B curve.
2. Count the 1283 steady-state MLP parameters and verify the hand-calculated gradient update.
3. Compare scaled and unscaled outputs by each component’s RMSE.
4. Inspect concentration-sum residual and minimum predicted concentration on held-out inputs.

Submission: steady-state model, split/scaling details, checked gradient update, and component/consistency evaluation.

Original explanations: PyTorch [model construction](https://docs.pytorch.org/tutorials/beginner/basics/buildmodel_tutorial.html), [autograd](https://docs.pytorch.org/tutorials/beginner/basics/autogradqs_tutorial.html), and [training](https://docs.pytorch.org/tutorials/beginner/basics/optimization_tutorial.html).

<!-- lecture-page -->

## Reading companion

[Week 2 companion]({{ page.reading_note | relative_url }}) · [English PDF]({{ page.reading_pdf_en | relative_url }})

KKT-hPINN reference: Chen, H., Constante Flores, G. E., & Li, C. (2024). [Physics-informed neural networks with hard linear equality constraints](https://doi.org/10.1016/j.compchemeng.2024.108764). *Computers & Chemical Engineering*, 189, 108764.

<!-- ko -->

## 연속반응의 전환율과 생성물 조성

{% assign result = site.data.week02_results %}

<div class="lecture-columns" markdown="1">

<div markdown="1">

A → B → C에서 원하는 중간 생성물은 B입니다. 체류시간이 짧으면 B가 충분히 만들어지지 않고, 길면 더 많은 B가 C로 반응합니다.

전환율 하나로는 제품 조성을 알 수 없으므로 엔지니어는 각 조건의 세 출구 농도를 모두 예측해야 합니다.

한 모델로 A·B·C를 일관되게 예측할 수 있을까요?

</div>

<div markdown="1">

<figure><img src="{{ '/assets/courses/surrogate-models/week-02/motivation-engineer.png' | relative_url }}" alt="반응기의 A·B·C 생성물을 살펴보는 공정 엔지니어." /></figure>

</div>

</div>

<!-- lecture-page -->

## 성분별 예측 오차

세 농도의 단위는 같아도 변화 폭은 다르므로, 크기를 조정하지 않은 손실함수는 한 성분의 오차를 더 크게 반영할 수 있습니다.

이번 주에는 MLP의 출력 계산, gradient 한 번으로 파라미터가 바뀌는 과정과 성분별 평가를 다뤄봅니다.

### 정상상태 MLP를 학습하고 확인하기

1. A·B·C의 정상상태 기준값을 유도합니다.
2. 데이터 크기를 조정하고 순전파·역전파·파라미터 갱신을 한 번씩 계산
3. MLP를 학습해 성분별 RMSE와 농도 합 residual을 비교

<!-- lecture-page -->

## 1. CSTR의 연속반응 A → B → C

기준 공정: 완전혼합·일정 부피·일정 밀도·등온 CSTR의 1차 연속반응 A → B → C. 유입: A 포함, B·C 농도 0. 운전 입력: 온도. 단위: 농도 mol/L, 온도 K, 시간 min

<math display="block" aria-label="Concentration balances for consecutive CSTR reactions"><mtable columnalign="left"><mtr><mtd><mrow><mfrac><mrow><mi>d</mi><msub><mi>C</mi><mi>A</mi></msub></mrow><mrow><mi>d</mi><mi>t</mi></mrow></mfrac><mo>=</mo><mfrac><mrow><msub><mi>C</mi><mi>Af</mi></msub><mo>−</mo><msub><mi>C</mi><mi>A</mi></msub></mrow><mi>τ</mi></mfrac><mo>−</mo><msub><mi>k</mi><mn>1</mn></msub><msub><mi>C</mi><mi>A</mi></msub></mrow></mtd></mtr><mtr><mtd><mrow><mfrac><mrow><mi>d</mi><msub><mi>C</mi><mi>B</mi></msub></mrow><mrow><mi>d</mi><mi>t</mi></mrow></mfrac><mo>=</mo><mo>−</mo><mfrac><msub><mi>C</mi><mi>B</mi></msub><mi>τ</mi></mfrac><mo>+</mo><msub><mi>k</mi><mn>1</mn></msub><msub><mi>C</mi><mi>A</mi></msub><mo>−</mo><msub><mi>k</mi><mn>2</mn></msub><msub><mi>C</mi><mi>B</mi></msub></mrow></mtd></mtr><mtr><mtd><mrow><mfrac><mrow><mi>d</mi><msub><mi>C</mi><mi>C</mi></msub></mrow><mrow><mi>d</mi><mi>t</mi></mrow></mfrac><mo>=</mo><mo>−</mo><mfrac><msub><mi>C</mi><mi>C</mi></msub><mi>τ</mi></mfrac><mo>+</mo><msub><mi>k</mi><mn>2</mn></msub><msub><mi>C</mi><mi>B</mi></msub></mrow></mtd></mtr></mtable></math>

B 수지에는 생성과 소모가 모두 들어갑니다. A에서 생기는 k₁C_A는 양수, 다음 반응으로 사라지는 k₂C_B와 탱크 밖으로 나가는 C_B/τ는 음수입니다. B의 최대점은 이 경쟁에서 생깁니다.

<!-- lecture-page -->

## 속도상수와 운전 영역

두 속도상수의 단위는 1/min이며, 온도에 따라 아래 식으로 계산

<math display="block" aria-label="Temperature-dependent first-order rate constants"><mtable columnalign="left"><mtr><mtd><mrow><msub><mi>k</mi><mn>1</mn></msub><mo>(</mo><mi>T</mi><mo>)</mo><mo>=</mo><mn>0.2</mn><mi>exp</mi><mo>[</mo><mn>6000</mn><mo>(</mo><mfrac><mn>1</mn><mn>330</mn></mfrac><mo>−</mo><mfrac><mn>1</mn><mi>T</mi></mfrac><mo>)</mo><mo>]</mo></mrow></mtd></mtr><mtr><mtd><mrow><msub><mi>k</mi><mn>2</mn></msub><mo>(</mo><mi>T</mi><mo>)</mo><mo>=</mo><mn>0.1</mn><mi>exp</mi><mo>[</mo><mn>5000</mn><mo>(</mo><mfrac><mn>1</mn><mn>330</mn></mfrac><mo>−</mo><mfrac><mn>1</mn><mi>T</mi></mfrac><mo>)</mo><mo>]</mo></mrow></mtd></mtr></mtable></math>

| 항목 | 값·범위 |
| --- | --- |
| 기준 온도 | 330 K |
| 기준 k₁; k₂ | 0.2; 0.1 /min |
| 온도 민감도 파라미터 | 6000 K; 5000 K |
| 온도 T | 300–360 K |
| 체류시간 τ | 1–10 min |
| 유입 A 농도 | 0.8–1.5 mol/L |

세 수지는 각각 A의 소모, B의 생성·소모, C의 생성을 나타냅니다. 세 식을 더하면 반응 항이 상쇄됩니다.

<!-- lecture-page -->

## 2. 세 출력을 갖는 정상상태 mapping 유도

시간 미분을 0으로 놓고 각 식에 τ를 곱한 뒤 농도 항을 모읍니다.

<math display="block" aria-label="Steady-state balance equations"><mtable columnalign="left"><mtr><mtd><mrow><mo>(</mo><mrow><mn>1</mn><mo>+</mo><msub><mi>k</mi><mn>1</mn></msub><mi>τ</mi></mrow><mo>)</mo><msub><mi>C</mi><mi>A</mi></msub><mo>=</mo><msub><mi>C</mi><mi>Af</mi></msub></mrow></mtd></mtr><mtr><mtd><mrow><mo>(</mo><mrow><mn>1</mn><mo>+</mo><msub><mi>k</mi><mn>2</mn></msub><mi>τ</mi></mrow><mo>)</mo><msub><mi>C</mi><mi>B</mi></msub><mo>=</mo><msub><mi>k</mi><mn>1</mn></msub><mi>τ</mi><msub><mi>C</mi><mi>A</mi></msub></mrow></mtd></mtr><mtr><mtd><mrow><msub><mi>C</mi><mi>C</mi></msub><mo>=</mo><msub><mi>k</mi><mn>2</mn></msub><mi>τ</mi><msub><mi>C</mi><mi>B</mi></msub></mrow></mtd></mtr></mtable></math>

첫 식은 A만 포함하므로 바로 풀 수 있습니다. 그 A를 두 번째 식에 넣어 B를 구하고, B를 마지막 식에 넣어 C를 구합니다. 이 순서 때문에 세 미지수를 동시에 반복 계산할 필요가 없습니다.

<!-- lecture-page -->

## A·B·C 농도 계산

A를 먼저 구하고 B, C에 차례로 대입합니다.

<math display="block" aria-label="Three-component steady-state mapping"><mtable columnalign="left"><mtr><mtd><mrow><msub><mi>C</mi><mi>A</mi></msub><mo>=</mo><mfrac><msub><mi>C</mi><mi>Af</mi></msub><mrow><mn>1</mn><mo>+</mo><msub><mi>k</mi><mn>1</mn></msub><mi>τ</mi></mrow></mfrac></mrow></mtd></mtr><mtr><mtd><mrow><msub><mi>C</mi><mi>B</mi></msub><mo>=</mo><mfrac><mrow><msub><mi>k</mi><mn>1</mn></msub><mi>τ</mi><msub><mi>C</mi><mi>Af</mi></msub></mrow><mrow><mo>(</mo><mrow><mn>1</mn><mo>+</mo><msub><mi>k</mi><mn>1</mn></msub><mi>τ</mi></mrow><mo>)</mo><mo>(</mo><mrow><mn>1</mn><mo>+</mo><msub><mi>k</mi><mn>2</mn></msub><mi>τ</mi></mrow><mo>)</mo></mrow></mfrac></mrow></mtd></mtr><mtr><mtd><mrow><msub><mi>C</mi><mi>C</mi></msub><mo>=</mo><msub><mi>k</mi><mn>2</mn></msub><mi>τ</mi><msub><mi>C</mi><mi>B</mi></msub></mrow></mtd></mtr></mtable></math>

330 K, τ = 5 min, 유입 농도 1.2 mol/L에서 농도는 [0.6, 0.4, 0.2] mol/L. 합은 유입 농도와 같으며, 이 세 농도를 정상상태 MLP의 기준값으로 사용

수치 대입은 A=1.2/2=0.6, B=(0.2×5×0.6)/1.5=0.4, C=0.1×5×0.4=0.2 순서입니다. B 계산에서는 분모의 유출 항 1과 다음 반응 항 0.5를 모두 남겨야 합니다.

<!-- lecture-page -->

## 중간 생성물 B의 비단조 응답

온도가 고정되면 C_B 식에서 B의 수율과 그 수율을 최대화하는 체류시간을 구할 수 있습니다.

<math display="block" aria-label="B yield and maximizing residence time at fixed temperature"><mrow><msub><mi>Y</mi><mi>B</mi></msub><mo>=</mo><mfrac><msub><mi>C</mi><mi>B</mi></msub><msub><mi>C</mi><mi>Af</mi></msub></mfrac><mo>=</mo><mfrac><mrow><msub><mi>k</mi><mn>1</mn></msub><mi>τ</mi></mrow><mrow><mo>(</mo><mrow><mn>1</mn><mo>+</mo><msub><mi>k</mi><mn>1</mn></msub><mi>τ</mi></mrow><mo>)</mo><mo>(</mo><mrow><mn>1</mn><mo>+</mo><msub><mi>k</mi><mn>2</mn></msub><mi>τ</mi></mrow><mo>)</mo></mrow></mfrac><mo>,</mo><mspace width="1em"/><msup><mi>τ</mi><mo>*</mo></msup><mo>=</mo><mfrac><mn>1</mn><msqrt><mrow><msub><mi>k</mi><mn>1</mn></msub><msub><mi>k</mi><mn>2</mn></msub></mrow></msqrt></mfrac></mrow></math>

분모를 D=1+(k₁+k₂)τ+k₁k₂τ²로 두면 미분의 분자는 k₁(D−τD′)=k₁(1−k₁k₂τ²)입니다. 양의 분모 D²는 부호를 바꾸지 않습니다. 따라서 τ=1/√(k₁k₂) 전에는 증가하고 이후에는 감소합니다.

<!-- lecture-page -->

## 세 성분의 농도 profile 비교

<div class="lecture-columns" markdown="1">

<div markdown="1">

330 K에서 τ*는 약 7.07 min. 짧은 체류시간에서는 B 생성이 부족하고, 체류시간이 길어지면 더 많은 B가 C로 반응합니다.

</div>

<div markdown="1">

<figure><img src="{{ '/assets/courses/surrogate-models/week-02/steady-profiles.png' | relative_url }}" alt="330 K에서 체류시간에 따른 A·B·C 농도와 기준 모델·MLP 비교." /><figcaption>330 K에서의 다성분 응답. B 농도는 중간 체류시간에서 최대가 된다.</figcaption></figure>

</div>

</div>

<!-- lecture-page -->

## 3. 학습 데이터 구성

한 행의 입력은 [T, τ, C_Af], 출력은 [C_A, C_B, C_C]이며 두 배열의 크기는 모두 (N, 3). 표의 운전 영역에서 train 400개, validation 120개, test 160개를 생성하고 정상상태 식으로 기준값을 계산

Train 데이터에서 세 농도의 표준편차는 약 [0.283, 0.110, 0.217] mol/L로, 단위가 같아도 변화 폭은 다릅니다.

한 행의 A·B·C는 같은 입력에서 계산한 하나의 묶음입니다. 성분별로 행을 따로 섞으면 입력과 정답의 대응이 깨집니다. 분할과 순서 섞기는 입력 행과 출력 행에 함께 적용합니다.

<!-- lecture-page -->

## 4. Forward 계산과 scaling

MLP 구조: 3 → 32 → 32 → 3. ReLU 은닉층과 선형 출력층

은닉층 계산: 가중합 + bias → ReLU(a) = max(0, a). 양수는 통과, 음수는 0. 농도 데이터로 학습하는 파라미터: 가중치와 bias

<math display="block" aria-label="MLP forward computation"><mtable columnalign="left"><mtr><mtd><mrow><msub><mi mathvariant="bold">h</mi><mn>1</mn></msub><mo>=</mo><mtext>ReLU</mtext><mo>(</mo><msub><mi mathvariant="bold">W</mi><mn>1</mn></msub><mi mathvariant="bold">x̃</mi><mo>+</mo><msub><mi mathvariant="bold">b</mi><mn>1</mn></msub><mo>)</mo></mrow></mtd></mtr><mtr><mtd><mrow><msub><mi mathvariant="bold">h</mi><mn>2</mn></msub><mo>=</mo><mtext>ReLU</mtext><mo>(</mo><msub><mi mathvariant="bold">W</mi><mn>2</mn></msub><msub><mi mathvariant="bold">h</mi><mn>1</mn></msub><mo>+</mo><msub><mi mathvariant="bold">b</mi><mn>2</mn></msub><mo>)</mo></mrow></mtd></mtr><mtr><mtd><mrow><mover><mi mathvariant="bold">z</mi><mo>^</mo></mover><mo>=</mo><msub><mi mathvariant="bold">W</mi><mn>3</mn></msub><msub><mi mathvariant="bold">h</mi><mn>2</mn></msub><mo>+</mo><msub><mi mathvariant="bold">b</mi><mn>3</mn></msub></mrow></mtd></mtr></mtable></math>

| 층 | Weight shape | Bias shape | Parameter 수 |
| --- | --- | --- | --- |
| 입력 → hidden 1 | 32 × 3 | 32 | 128 |
| Hidden 1 → hidden 2 | 32 × 32 | 32 | 1056 |
| Hidden 2 → 출력 | 3 × 32 | 3 | 99 |
| 합계 | | | **1283** |

한 뉴런은 입력 열 전체를 가중합해 숫자 하나를 만듭니다. 첫 층의 뉴런 32개가 각각 입력 3개의 가중치와 편향 하나를 가져 32×(3+1)=128개입니다. 은닉층은 이 계산을 여러 특징에 반복합니다.

<!-- lecture-page -->

## 열벡터 수식을 batch 행렬로 계산하기

수식은 입력을 열벡터로 씁니다. Batch 코드가 입력을 (N,3)의 행으로 저장하면 첫 층은 `X @ W1.T + b1`이고 결과는 (N,32)입니다. 전치는 같은 가중합을 행 단위 저장 방식에 맞추며, bias 32개는 각 데이터 행에 반복 적용됩니다.

| 배열 | 크기 | 각 축의 의미 |
| --- | --- | --- |
| X | N×3 | 데이터 행, 입력 변수 |
| W1.T | 3×32 | 입력 변수, 은닉 뉴런 |
| X @ W1.T | N×32 | 데이터 행, 은닉 뉴런 |
| b1 | 32 | 각 뉴런의 bias |

두 입력 행 [1,0,−1], [0,1,1]과 첫 뉴런 가중치 [1,0,0], bias 0.2를 생각합니다. 첫 출력 열은 각각 1×1+0×0−1×0+0.2=1.2와 0×1+1×0+1×0+0.2=0.2입니다. 나머지 31개 열도 해당 뉴런의 가중치로 같은 계산을 합니다.

행렬곱 뒤 ReLU는 각 원소에 따로 적용합니다. 행 하나가 다른 데이터 행과 섞이는 연산은 아닙니다.

<!-- lecture-page -->

## Scaling과 학습 loss

입력은 명시한 하한·상한으로 크기를 조정합니다. 출력은 train 평균 μ와 표준편차 s로 표준화하고, 예측한 뒤 원래 단위로 복원

<math display="block" aria-label="Input scaling, output standardization, and inverse transformation"><mtable columnalign="left"><mtr><mtd><mrow><msub><mi>x̃</mi><mi>j</mi></msub><mo>=</mo><mn>2</mn><mfrac><mrow><msub><mi>x</mi><mi>j</mi></msub><mo>−</mo><msub><mi>l</mi><mi>j</mi></msub></mrow><mrow><msub><mi>u</mi><mi>j</mi></msub><mo>−</mo><msub><mi>l</mi><mi>j</mi></msub></mrow></mfrac><mo>−</mo><mn>1</mn></mrow></mtd></mtr><mtr><mtd><mrow><msub><mi>z</mi><mi>j</mi></msub><mo>=</mo><mfrac><mrow><msub><mi>y</mi><mi>j</mi></msub><mo>−</mo><msub><mi>μ</mi><mi>j</mi></msub></mrow><msub><mi>s</mi><mi>j</mi></msub></mfrac><mo>,</mo><mspace width="1em"/><msub><mover><mi>y</mi><mo>^</mo></mover><mi>j</mi></msub><mo>=</mo><msub><mi>μ</mi><mi>j</mi></msub><mo>+</mo><msub><mi>s</mi><mi>j</mi></msub><msub><mover><mi>z</mi><mo>^</mo></mover><mi>j</mi></msub></mrow></mtd></mtr></mtable></math>

손실함수는 표본과 표준화된 출력 성분 전체의 제곱 오차를 평균합니다.

<math display="block" aria-label="Mean squared error over samples and standardized output components"><mrow><mi>L</mi><mo>=</mo><mfrac><mn>1</mn><mrow><mn>3</mn><mi>N</mi></mrow></mfrac><munderover><mo>∑</mo><mrow><mi>n</mi><mo>=</mo><mn>1</mn></mrow><mi>N</mi></munderover><munderover><mo>∑</mo><mrow><mi>j</mi><mo>=</mo><mn>1</mn></mrow><mn>3</mn></munderover><msup><mrow><mo>(</mo><msub><mover><mi>z</mi><mo>^</mo></mover><mrow><mi>n</mi><mo>,</mo><mi>j</mi></mrow></msub><mo>−</mo><msub><mi>z</mi><mrow><mi>n</mi><mo>,</mo><mi>j</mi></mrow></msub><mo>)</mo></mrow><mn>2</mn></msup></mrow></math>

각 농도 오차를 해당 성분의 train 변화 폭에 상대적으로 평가하므로, 표준편차가 작은 B의 원래 단위 제곱 오차에는 더 큰 가중치가 붙습니다.

같은 0.01 mol/L 오차라도 A의 표준화 오차는 0.01/0.283≈0.0353, B는 0.01/0.110≈0.0909입니다. 제곱하면 B의 손실 기여가 약 6.62배입니다. 출력 scaling은 단위 변환과 함께 학습에서 강조하는 성분도 바꿉니다.

<!-- lecture-page -->

## 5. Backpropagation 한 번 계산하기

계산 예제: bias가 모두 0인 3 → 2 → 3 신경망. 손실함수: L = ½‖ŷ − y‖². 학습률: 0.1

<math display="block" aria-label="Weights and data for one backpropagation example"><mtable columnalign="left"><mtr><mtd><mrow><mi mathvariant="bold">x</mi><mo>=</mo><mrow><mo>[</mo><mtable><mtr><mtd><mn>1</mn></mtd></mtr><mtr><mtd><mn>0</mn></mtd></mtr><mtr><mtd><mn>-1</mn></mtd></mtr></mtable><mo>]</mo></mrow><mo>,</mo><mi mathvariant="bold">y</mi><mo>=</mo><mrow><mo>[</mo><mtable><mtr><mtd><mn>0</mn></mtd></mtr><mtr><mtd><mn>1</mn></mtd></mtr><mtr><mtd><mn>0</mn></mtd></mtr></mtable><mo>]</mo></mrow></mrow></mtd></mtr><mtr><mtd><mrow><msub><mi mathvariant="bold">W</mi><mn>1</mn></msub><mo>=</mo><mrow><mo>[</mo><mtable><mtr><mtd><mn>1</mn></mtd><mtd><mn>0</mn></mtd><mtd><mn>0</mn></mtd></mtr><mtr><mtd><mn>0</mn></mtd><mtd><mn>0</mn></mtd><mtd><mn>1</mn></mtd></mtr></mtable><mo>]</mo></mrow><mo>,</mo><msub><mi mathvariant="bold">W</mi><mn>2</mn></msub><mo>=</mo><mrow><mo>[</mo><mtable><mtr><mtd><mn>1</mn></mtd><mtd><mn>0</mn></mtd></mtr><mtr><mtd><mn>0</mn></mtd><mtd><mn>1</mn></mtd></mtr><mtr><mtd><mn>1</mn></mtd><mtd><mn>1</mn></mtd></mtr></mtable><mo>]</mo></mrow></mrow></mtd></mtr></mtable></math>

은닉층의 활성화 전 값 a와 활성화 값 h, 예측값과 오차를 구합니다.

<math display="block" aria-label="Forward computation in the small network"><mrow><mi mathvariant="bold">a</mi><mo>=</mo><mrow><mo>[</mo><mtable><mtr><mtd><mn>1</mn></mtd></mtr><mtr><mtd><mn>-1</mn></mtd></mtr></mtable><mo>]</mo></mrow><mo>,</mo><mi mathvariant="bold">h</mi><mo>=</mo><mrow><mo>[</mo><mtable><mtr><mtd><mn>1</mn></mtd></mtr><mtr><mtd><mn>0</mn></mtd></mtr></mtable><mo>]</mo></mrow><mo>,</mo><mover><mi mathvariant="bold">y</mi><mo>^</mo></mover><mo>=</mo><mrow><mo>[</mo><mtable><mtr><mtd><mn>1</mn></mtd></mtr><mtr><mtd><mn>0</mn></mtd></mtr><mtr><mtd><mn>1</mn></mtd></mtr></mtable><mo>]</mo></mrow><mo>,</mo><mi mathvariant="bold">e</mi><mo>=</mo><mrow><mo>[</mo><mtable><mtr><mtd><mn>1</mn></mtd></mtr><mtr><mtd><mn>-1</mn></mtd></mtr><mtr><mtd><mn>1</mn></mtd></mtr></mtable><mo>]</mo></mrow></mrow></math>

첫 은닉 뉴런은 입력 첫 성분 1을 읽고, 두 번째는 셋째 성분 −1을 읽습니다. ReLU 뒤에는 [1,0]만 남습니다. 출력층은 이 두 숫자를 각각 [첫째,둘째,두 값의 합]으로 조합하므로 [1,0,1]이 됩니다.

<!-- lecture-page -->

## 가중치 하나의 연쇄법칙

손계산 손실은 L=½∑eⱼ²이고 eⱼ=ŷⱼ−yⱼ입니다. 따라서 출력 ŷⱼ를 조금 늘렸을 때의 손실 변화율은 eⱼ입니다. 출력 가중치 W₂,ji를 늘리면 ŷⱼ는 은닉값 hᵢ만큼 변합니다.

| 미분 경로 | 곱하는 값 | 앞 예제의 결과 |
| --- | --- | --- |
| W₂,A1 → ŷ_A → L | e_A×h₁ | 1×1=1 |
| W₂,B1 → ŷ_B → L | e_B×h₁ | −1×1=−1 |
| h₁ → 세 출력 → L | 연결 가중치×오차의 합 | 1×1+0×(−1)+1×1=2 |
| W₁,13 → a₁ → h₁ → L | x₃×ReLU′(a₁)×2 | (−1)×1×2=−2 |

ReLU 미분은 a>0에서 1, a<0에서 0입니다. 이 예는 a=0을 피합니다. Bias는 가중합에 1배로 더해지므로 그 미분에는 입력값 대신 1을 곱합니다.

δ는 해당 층의 활성화 전 값에 대한 손실 미분, ⊙는 같은 위치끼리의 곱입니다. 실제 평균제곱 손실에서는 출력 미분이 2e/(3N)이므로 손계산의 ½ 제곱합과 계수가 다릅니다.

<!-- lecture-page -->

## Gradient와 파라미터 갱신

출력 오차를 출력층 가중치와 ReLU 미분을 거쳐 전달합니다.

<math display="block" aria-label="Backpropagation gradients for one example"><mtable columnalign="left"><mtr><mtd><mrow><msub><mi mathvariant="bold">δ</mi><mn>2</mn></msub><mo>=</mo><mi mathvariant="bold">e</mi><mo>,</mo><msub><mi>∇</mi><msub><mi mathvariant="bold">W</mi><mn>2</mn></msub></msub><mi>L</mi><mo>=</mo><mi mathvariant="bold">e</mi><msup><mi mathvariant="bold">h</mi><mi>T</mi></msup><mo>=</mo><mrow><mo>[</mo><mtable><mtr><mtd><mn>1</mn></mtd><mtd><mn>0</mn></mtd></mtr><mtr><mtd><mn>-1</mn></mtd><mtd><mn>0</mn></mtd></mtr><mtr><mtd><mn>1</mn></mtd><mtd><mn>0</mn></mtd></mtr></mtable><mo>]</mo></mrow></mrow></mtd></mtr><mtr><mtd><mrow><msub><mi mathvariant="bold">δ</mi><mn>1</mn></msub><mo>=</mo><mo>(</mo><msup><msub><mi mathvariant="bold">W</mi><mn>2</mn></msub><mi>T</mi></msup><mi mathvariant="bold">e</mi><mo>)</mo><mo>⊙</mo><mrow><mo>[</mo><mtable><mtr><mtd><mn>1</mn></mtd></mtr><mtr><mtd><mn>0</mn></mtd></mtr></mtable><mo>]</mo></mrow><mo>=</mo><mrow><mo>[</mo><mtable><mtr><mtd><mn>2</mn></mtd></mtr><mtr><mtd><mn>0</mn></mtd></mtr></mtable><mo>]</mo></mrow></mrow></mtd></mtr><mtr><mtd><mrow><msub><mi>∇</mi><msub><mi mathvariant="bold">W</mi><mn>1</mn></msub></msub><mi>L</mi><mo>=</mo><msub><mi mathvariant="bold">δ</mi><mn>1</mn></msub><msup><mi mathvariant="bold">x</mi><mi>T</mi></msup><mo>=</mo><mrow><mo>[</mo><mtable><mtr><mtd><mn>2</mn></mtd><mtd><mn>0</mn></mtd><mtd><mn>-2</mn></mtd></mtr><mtr><mtd><mn>0</mn></mtd><mtd><mn>0</mn></mtd><mtd><mn>0</mn></mtd></mtr></mtable><mo>]</mo></mrow></mrow></mtd></mtr></mtable></math>

Bias gradient는 각각 δ₁, δ₂입니다. 모든 가중치와 bias를 parameter ← parameter − 0.1 × gradient로 갱신하면 다음 순전파 출력은 [0.26, 0.14, 0.26]이고, loss는 1.5에서 0.4374로 줄어듭니다. Notebook의 autograd 결과와 손계산을 대조합니다.

첫 은닉값은 A와 C 출력에 각각 가중치 1로 연결되어 있어 두 오차 1+1=2를 받습니다. 두 번째 은닉값의 pre-activation은 음수라 ReLU 미분이 0입니다. 따라서 그 뉴런의 입력 가중치와 편향은 이번 단계에서 움직이지 않습니다.

<!-- lecture-page -->

## 가중치 갱신 뒤의 두 번째 순전파

학습률 0.1로 가중치와 편향을 모두 갱신합니다. 첫 은닉 가중치 [1,0,0]에서 0.1×[2,0,−2]를 빼면 [0.8,0,0.2], 편향은 −0.2가 됩니다.

| 중간값 | 갱신 뒤 계산 |
| --- | --- |
| 첫 은닉 pre-activation | 0.8×1+0×0+0.2×(−1)−0.2=0.4 |
| 두 번째 은닉 pre-activation | −1 |
| ReLU 출력 | [0.4,0] |
| 출력 A, C | 0.9×0.4−0.1=0.26 |
| 출력 B | 0.1×0.4+0.1=0.14 |

새 오차는 [0.26,−0.86,0.26]입니다. 손실은 (0.0676+0.7396+0.0676)/2=0.4374로 줄지만 B는 여전히 목표 1보다 작습니다. 한 번의 감소가 학습 완료를 뜻하지는 않습니다.

<!-- lecture-page -->

## 6. 정상상태 모델 학습과 평가

<div class="lecture-columns" markdown="1">

<div markdown="1">

학습 설정: Adam, 학습률 0.001, batch 64, 최대 1400 epoch. 가중치 선택: 매 epoch의 validation loss 중 최솟값

```python
prediction = model(inputs)
loss = loss_function(prediction, targets)
optimizer.zero_grad()
loss.backward()
optimizer.step()
```

</div>

<div markdown="1">

<figure><img src="{{ '/assets/courses/surrogate-models/week-02/steady-training.png' | relative_url }}" alt="정상상태 MLP의 train·validation 표준화 MSE 곡선." /><figcaption>Train·validation loss. 아래 예측 지표는 mol/L 단위로 되돌린 뒤 계산한다.</figcaption></figure>

</div>

</div>

<!-- lecture-page -->

## 학습 루프의 값과 변경 시점

```python
prediction = model(inputs)
loss = loss_function(prediction, targets)
optimizer.zero_grad()
loss.backward()
optimizer.step()
```

| 줄 | 만들어지거나 바뀌는 값 |
| --- | --- |
| model(inputs) | 현재 가중치로 batch의 출력 계산 |
| loss_function | 출력과 정답 차이를 스칼라 손실로 축약 |
| zero_grad | 이전 batch의 기울기 제거 |
| backward | 현재 손실의 가중치·편향별 기울기 |
| step | 기울기와 optimizer 상태로 파라미터 갱신 |

손 계산은 단순 gradient descent였고 실제 학습은 Adam입니다. Adam은 과거 기울기 정보도 사용하므로 같은 0.1배 빼기와 수치가 같지 않습니다. step 뒤의 성능을 보려면 갱신된 가중치로 순전파를 다시 수행합니다.

<!-- lecture-page -->

## Adam의 첫 갱신과 batch의 의미

Batch는 한 번에 손실과 기울기를 계산하는 데이터 묶음입니다. 400개 행을 batch 64로 나누면 한 epoch에 64개짜리 6묶음과 16개짜리 마지막 묶음, 총 7번 갱신합니다. Epoch는 학습 데이터 한 바퀴입니다.

Adam은 기울기 평균 m과 제곱 평균 v를 누적합니다. 처음 m=v=0, 기울기 g=2, β₁=0.9, β₂=0.999인 가중치 하나를 계산합니다.

| 계산 | 첫 단계 값 |
| --- | --- |
| m=0.9m+0.1g | 0.2 |
| v=0.999v+0.001g² | 0.004 |
| 초기 0의 편향 보정 | m̂=0.2/(1−0.9)=2; v̂=0.004/(1−0.999)=4 |
| 학습률 0.001의 이동 크기 | 0.001×2/(√4+10⁻⁸)≈0.001 |

단순 경사하강이라면 0.001×2=0.002를 뺍니다. Adam은 누적된 기울기 크기로 이동을 조정하므로 같은 학습률이어도 갱신량이 다릅니다. 이 계산의 ε=10⁻⁸은 분모가 0이 되는 것을 막습니다.

[PyTorch Adam의 갱신 정의](https://docs.pytorch.org/docs/stable/generated/torch.optim.Adam.html)

<!-- lecture-page -->

## 출력 성분별 평가

| Test RMSE, mol/L | A | B | C |
| --- | --- | --- | --- |
| 출력 scaling 적용 | {{ result.steady_a_rmse }} | {{ result.steady_b_rmse }} | {{ result.steady_c_rmse }} |
| 출력 scaling 미적용 | {{ result.unscaled_a_rmse }} | {{ result.unscaled_b_rmse }} | {{ result.unscaled_c_rmse }} |

이번 실행에서는 출력 scaling으로 A·B RMSE가 줄었고 C RMSE는 조금 커졌습니다. 각 성분의 변화를 따로 확인해야 전체 오차 하나에 가려진 차이를 볼 수 있습니다.

<figure><img src="{{ '/assets/courses/surrogate-models/week-02/steady-parity.png' | relative_url }}" alt="Test 데이터의 A·B·C 농도에 대한 기준값·예측값 parity plot." /><figcaption>성분별 parity plot에서 각 출력의 오차를 확인한다.</figcaption></figure>

<!-- lecture-page -->

## 표준화 출력에서 농도와 오차로

계산용 한 성분의 학습 평균 μ=0.4 mol/L, 표준편차 s=0.1 mol/L를 둡니다. 정답 농도 0.45는 z=(0.45−0.4)/0.1=0.5입니다.

| 항목 | 계산 |
| --- | --- |
| 신경망의 표준화 예측 | ẑ=0.3 |
| 농도 복원 | 0.4+0.1×0.3=0.43 mol/L |
| 표준화 오차 | 0.3−0.5=−0.2 |
| 농도 오차 | 0.43−0.45=−0.02 mol/L |

```python
prediction = y_mean + y_scale * standardized_prediction
component_rmse = np.sqrt(((prediction - truth)**2).mean(axis=0))
sum_residual = prediction.sum(axis=1) - feed
```

첫 줄은 각 출력 열에 해당 평균과 표준편차를 적용합니다. axis=0은 성분별 정확도, axis=1은 같은 조건의 세 성분 합을 계산합니다. 두 축을 바꾸면 다른 질문을 계산하게 됩니다.

<!-- lecture-page -->

## 농도 합 확인

<math display="block" aria-label="Concentration-sum residual"><mrow><mi>r</mi><mo>=</mo><mover><msub><mi>C</mi><mi>A</mi></msub><mo>^</mo></mover><mo>+</mo><mover><msub><mi>C</mi><mi>B</mi></msub><mo>^</mo></mover><mo>+</mo><mover><msub><mi>C</mi><mi>C</mi></msub><mo>^</mo></mover><mo>−</mo><msub><mi>C</mi><mi>Af</mi></msub></mrow></math>

Test residual RMSE는 {{ result.steady_balance }} mol/L. 성분별 오차로 예측 정확도를, 농도 합 residual로 해당 수지의 일관성을 평가

수지를 만족하는 기준값으로 학습해도 세 선형 출력의 합이 유입 농도와 같도록 강제되지는 않습니다.

유입 1.2 mol/L에서 예측이 [0.62, 0.41, 0.20] mol/L이면 합은 1.23 mol/L이고 r = 0.03 mol/L입니다. 몰분율을 예측할 때도 합이 1을 벗어날 수 있습니다.

성분 오차의 합이 합 잔차입니다. 오차 [0.02,−0.01,−0.01]은 합이 0이지만 성분은 틀립니다. 반대로 작은 양의 오차가 세 성분에 누적되면 총농도 오차가 커집니다.

<!-- lecture-page -->

## 4주차 예고: 농도 합 제약의 모델 반영

학습 후 출력을 보정하거나, 제약을 만족하는 변환을 학습 과정에 포함할 수 있습니다.

| 접근 | 보정이 들어가는 위치 |
| --- | --- |
| 학습 후 외부 mapping/projection | Raw predictor를 학습한 뒤 출력을 보정한다. |
| KKT-hPINN | 입력과 raw 예측을 받는 고정 affine projection을 loss 전에 적용하며, 예측할 때도 적용한다. |

<math display="block" aria-label="Constraint-aware training flow"><mrow><mi mathvariant="bold">x</mi><mo>→</mo><msub><mi>f</mi><mi>θ</mi></msub><mo>→</mo><mover><mi mathvariant="bold">y</mi><mo>^</mo></mover><mo>→</mo><msub><mi>Π</mi><mi mathvariant="bold">x</mi></msub><mo>→</mo><mover><mi mathvariant="bold">y</mi><mo>~</mo></mover><mo>→</mo><mtext>loss</mtext></mrow></math>

KKT-hPINN은 투영한 출력으로 loss를 계산하고 투영층을 거쳐 역전파합니다. 투영 계수는 고정하지만 MLP 가중치는 이 변환을 반영해 학습합니다.

투영층은 지정한 선형 등식을 수치 연산 오차 범위에서 만족시키며, 비음수성에는 별도 제약이 필요합니다.

출처: Chen et al. (2024), [DOI: 10.1016/j.compchemeng.2024.108764](https://doi.org/10.1016/j.compchemeng.2024.108764).

<!-- lecture-page -->

## 7. 필수 정상상태 실습 실행

[정상상태 Notebook]({{ page.notebook | relative_url }})을 받습니다.

```bash
python -m pip install -r requirements.txt
python week02_lab.py --mode steady --output-dir week02-results
```

학습한 예측 모델의 성분별 RMSE와 농도 합 residual을 평가

<!-- lecture-page -->

## 8. 필수 연습문제와 제출물

1. C_A·C_B·C_C를 유도해 합을 확인하고, B 곡선이 단조롭지 않은 이유를 설명합니다.
2. 정상상태 MLP의 파라미터 1283개와 손으로 계산한 gradient 갱신을 확인
3. 출력 scaling 전후의 성분별 RMSE를 비교
4. 독립 입력에서 농도 합 residual과 최소 예측 농도를 살펴봅니다.

제출물: 정상상태 모델, 데이터 분할·scaling 정보, 확인한 gradient 갱신, 성분별 오차·일관성 평가

구현 설명은 PyTorch의 [모델 구성](https://docs.pytorch.org/tutorials/beginner/basics/buildmodel_tutorial.html), [autograd](https://docs.pytorch.org/tutorials/beginner/basics/autogradqs_tutorial.html), [학습](https://docs.pytorch.org/tutorials/beginner/basics/optimization_tutorial.html)을 참고합니다.

<!-- lecture-page -->

## 읽기자료

[2주차 읽기자료]({{ page.reading_note | relative_url }}) · [국문 PDF]({{ page.reading_pdf_ko | relative_url }})

KKT-hPINN 참고문헌: Chen, H., Constante Flores, G. E., & Li, C. (2024). [Physics-informed neural networks with hard linear equality constraints](https://doi.org/10.1016/j.compchemeng.2024.108764). *Computers & Chemical Engineering*, 189, 108764.
