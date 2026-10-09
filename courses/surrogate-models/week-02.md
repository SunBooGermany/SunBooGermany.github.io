---
layout: course-note
title: "Week 2: Learning Multicomponent Steady-State Responses with MLPs"
title_ko: "2주차: MLP로 다성분 정상상태 응답 학습하기"
description: "Train and evaluate a steady-state three-output MLP; follow one gradient update and check concentration consistency."
description_ko: "정상상태 세 출력 MLP를 학습·평가하고, gradient 갱신 한 번과 농도 합의 일관성을 확인합니다."
material_label: "Week 2"
material_label_ko: "2주차"
updated: "2026-10-09"
permalink: /courses/surrogate-models/week-02/
pdf_en: /assets/courses/surrogate-models/week-02-en.pdf
pdf_ko: /assets/courses/surrogate-models/week-02-ko.pdf
notebook: /assets/courses/surrogate-models/week-02/week02_steady.ipynb
notebook_2: /assets/courses/surrogate-models/week-02/week02_dynamic.ipynb
lab_script: /assets/courses/surrogate-models/week-02/week02_lab.py
reading_note: /courses/surrogate-models/week-02-reading/
reading_pdf_en: /assets/courses/surrogate-models/week-02-reading-en.pdf
reading_pdf_ko: /assets/courses/surrogate-models/week-02-reading-ko.pdf
course_id: "surrogate-models"
---

## More conversion does not tell the whole composition

{% assign result = site.data.week02_results %}

<div class="lecture-columns" markdown="1">

<div markdown="1">

The desired intermediate is **B** in **A → B → C**. At short residence time little B forms; at long residence time more B reacts onward to C.

An engineer needs all three outlet concentrations at each condition. One conversion number does not describe the product composition.

**Can one model predict A, B, and C consistently?**

</div>

<div markdown="1">

<figure><img src="{{ '/assets/courses/surrogate-models/week-02/motivation-engineer.png' | relative_url }}" alt="A process engineer examines the three reactor products A, B, and C." /></figure>

</div>

</div>

<!-- lecture-page -->

## Three outputs, different errors

All three concentrations have the same units, but their variation differs. An unscaled loss can emphasize one component.

This week learns how an MLP computes these outputs, how one gradient update changes its parameters, and how to evaluate each component.

<!-- lecture-page -->

## Learn and check the steady-state MLP

1. Derive steady-state labels for A, B, and C.
2. Scale the data and follow a forward pass, backpropagation, and one parameter update.
3. Train the MLP and compare component RMSE and concentration-sum residuals.

<!-- lecture-page -->

## 1. A → B → C in a CSTR

Consider a perfectly mixed, constant-volume, constant-density, isothermal CSTR with consecutive first-order reactions A → B → C. The feed contains A; its B and C concentrations are zero. Temperature is an operating input. With concentrations in mol/L, temperature in K, and time in min, the balances are:

<math display="block" aria-label="Concentration balances for consecutive CSTR reactions"><mtable columnalign="left"><mtr><mtd><mrow><mfrac><mrow><mi>d</mi><msub><mi>C</mi><mi>A</mi></msub></mrow><mrow><mi>d</mi><mi>t</mi></mrow></mfrac><mo>=</mo><mfrac><mrow><msub><mi>C</mi><mi>Af</mi></msub><mo>−</mo><msub><mi>C</mi><mi>A</mi></msub></mrow><mi>τ</mi></mfrac><mo>−</mo><msub><mi>k</mi><mn>1</mn></msub><msub><mi>C</mi><mi>A</mi></msub></mrow></mtd></mtr><mtr><mtd><mrow><mfrac><mrow><mi>d</mi><msub><mi>C</mi><mi>B</mi></msub></mrow><mrow><mi>d</mi><mi>t</mi></mrow></mfrac><mo>=</mo><mo>−</mo><mfrac><msub><mi>C</mi><mi>B</mi></msub><mi>τ</mi></mfrac><mo>+</mo><msub><mi>k</mi><mn>1</mn></msub><msub><mi>C</mi><mi>A</mi></msub><mo>−</mo><msub><mi>k</mi><mn>2</mn></msub><msub><mi>C</mi><mi>B</mi></msub></mrow></mtd></mtr><mtr><mtd><mrow><mfrac><mrow><mi>d</mi><msub><mi>C</mi><mi>C</mi></msub></mrow><mrow><mi>d</mi><mi>t</mi></mrow></mfrac><mo>=</mo><mo>−</mo><mfrac><msub><mi>C</mi><mi>C</mi></msub><mi>τ</mi></mfrac><mo>+</mo><msub><mi>k</mi><mn>2</mn></msub><msub><mi>C</mi><mi>B</mi></msub></mrow></mtd></mtr></mtable></math>

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

<!-- lecture-page -->

## Solve for A, B, and C

Solve in the order A, B, C:

<math display="block" aria-label="Three-component steady-state mapping"><mtable columnalign="left"><mtr><mtd><mrow><msub><mi>C</mi><mi>A</mi></msub><mo>=</mo><mfrac><msub><mi>C</mi><mi>Af</mi></msub><mrow><mn>1</mn><mo>+</mo><msub><mi>k</mi><mn>1</mn></msub><mi>τ</mi></mrow></mfrac></mrow></mtd></mtr><mtr><mtd><mrow><msub><mi>C</mi><mi>B</mi></msub><mo>=</mo><mfrac><mrow><msub><mi>k</mi><mn>1</mn></msub><mi>τ</mi><msub><mi>C</mi><mi>Af</mi></msub></mrow><mrow><mo>(</mo><mrow><mn>1</mn><mo>+</mo><msub><mi>k</mi><mn>1</mn></msub><mi>τ</mi></mrow><mo>)</mo><mo>(</mo><mrow><mn>1</mn><mo>+</mo><msub><mi>k</mi><mn>2</mn></msub><mi>τ</mi></mrow><mo>)</mo></mrow></mfrac></mrow></mtd></mtr><mtr><mtd><mrow><msub><mi>C</mi><mi>C</mi></msub><mo>=</mo><msub><mi>k</mi><mn>2</mn></msub><mi>τ</mi><msub><mi>C</mi><mi>B</mi></msub></mrow></mtd></mtr></mtable></math>

At 330 K, τ = 5 min, and feed = 1.2 mol/L, the concentrations are **[0.6, 0.4, 0.2] mol/L**. Their sum equals the feed concentration. These three outputs are the labels for the steady-state MLP.

<!-- lecture-page -->

## Why the B response is nonmonotone

At a fixed temperature, the B yield and its maximizing residence time follow from the expression for C_B:

<math display="block" aria-label="B yield and maximizing residence time at fixed temperature"><mrow><msub><mi>Y</mi><mi>B</mi></msub><mo>=</mo><mfrac><msub><mi>C</mi><mi>B</mi></msub><msub><mi>C</mi><mi>Af</mi></msub></mfrac><mo>=</mo><mfrac><mrow><msub><mi>k</mi><mn>1</mn></msub><mi>τ</mi></mrow><mrow><mo>(</mo><mrow><mn>1</mn><mo>+</mo><msub><mi>k</mi><mn>1</mn></msub><mi>τ</mi></mrow><mo>)</mo><mo>(</mo><mrow><mn>1</mn><mo>+</mo><msub><mi>k</mi><mn>2</mn></msub><mi>τ</mi></mrow><mo>)</mo></mrow></mfrac><mo>,</mo><mspace width="1em"/><msup><mi>τ</mi><mo>*</mo></msup><mo>=</mo><mfrac><mn>1</mn><msqrt><mrow><msub><mi>k</mi><mn>1</mn></msub><msub><mi>k</mi><mn>2</mn></msub></mrow></msqrt></mfrac></mrow></math>

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

Each row contains inputs [T, τ, C_Af] and outputs [C_A, C_B, C_C]. Input and output arrays both have shape **(N, 3)**. Generate 400 train, 120 validation, and 160 test operating points within the table's bounds, then calculate their labels with the steady-state map.

The three concentrations have the same units but different variations. In the training data, their standard deviations are approximately **[0.283, 0.110, 0.217] mol/L**.

<!-- lecture-page -->

## 4. Forward calculation and scaling

Use a **3 → 32 → 32 → 3** MLP, with ReLU hidden layers and a linear output layer:

Each hidden layer first computes a weighted sum and bias. ReLU(a) = max(0, a) retains positive values and sets negative values to zero. The weights and biases are the parameters fitted to the concentration data.

<math display="block" aria-label="MLP forward computation"><mtable columnalign="left"><mtr><mtd><mrow><msub><mi mathvariant="bold">h</mi><mn>1</mn></msub><mo>=</mo><mtext>ReLU</mtext><mo>(</mo><msub><mi mathvariant="bold">W</mi><mn>1</mn></msub><mi mathvariant="bold">x̃</mi><mo>+</mo><msub><mi mathvariant="bold">b</mi><mn>1</mn></msub><mo>)</mo></mrow></mtd></mtr><mtr><mtd><mrow><msub><mi mathvariant="bold">h</mi><mn>2</mn></msub><mo>=</mo><mtext>ReLU</mtext><mo>(</mo><msub><mi mathvariant="bold">W</mi><mn>2</mn></msub><msub><mi mathvariant="bold">h</mi><mn>1</mn></msub><mo>+</mo><msub><mi mathvariant="bold">b</mi><mn>2</mn></msub><mo>)</mo></mrow></mtd></mtr><mtr><mtd><mrow><mover><mi mathvariant="bold">z</mi><mo>^</mo></mover><mo>=</mo><msub><mi mathvariant="bold">W</mi><mn>3</mn></msub><msub><mi mathvariant="bold">h</mi><mn>2</mn></msub><mo>+</mo><msub><mi mathvariant="bold">b</mi><mn>3</mn></msub></mrow></mtd></mtr></mtable></math>

| Layer | Weight shape | Bias shape | Parameters |
| --- | --- | --- | --- |
| Input → hidden 1 | 32 × 3 | 32 | 128 |
| Hidden 1 → hidden 2 | 32 × 32 | 32 | 1056 |
| Hidden 2 → output | 3 × 32 | 3 | 99 |
| Total | | | **1283** |

<!-- lecture-page -->

## Scaling and the training loss

Scale the inputs with the declared lower and upper bounds. Standardize each output with its training mean μ and standard deviation s, and restore physical units after prediction:

<math display="block" aria-label="Input scaling, output standardization, and inverse transformation"><mtable columnalign="left"><mtr><mtd><mrow><msub><mi>x̃</mi><mi>j</mi></msub><mo>=</mo><mn>2</mn><mfrac><mrow><msub><mi>x</mi><mi>j</mi></msub><mo>−</mo><msub><mi>l</mi><mi>j</mi></msub></mrow><mrow><msub><mi>u</mi><mi>j</mi></msub><mo>−</mo><msub><mi>l</mi><mi>j</mi></msub></mrow></mfrac><mo>−</mo><mn>1</mn></mrow></mtd></mtr><mtr><mtd><mrow><msub><mi>z</mi><mi>j</mi></msub><mo>=</mo><mfrac><mrow><msub><mi>y</mi><mi>j</mi></msub><mo>−</mo><msub><mi>μ</mi><mi>j</mi></msub></mrow><msub><mi>s</mi><mi>j</mi></msub></mfrac><mo>,</mo><mspace width="1em"/><msub><mover><mi>y</mi><mo>^</mo></mover><mi>j</mi></msub><mo>=</mo><msub><mi>μ</mi><mi>j</mi></msub><mo>+</mo><msub><mi>s</mi><mi>j</mi></msub><msub><mover><mi>z</mi><mo>^</mo></mover><mi>j</mi></msub></mrow></mtd></mtr></mtable></math>

The loss averages squared errors across samples and standardized output components:

<math display="block" aria-label="Mean squared error over samples and standardized output components"><mrow><mi>L</mi><mo>=</mo><mfrac><mn>1</mn><mrow><mn>3</mn><mi>N</mi></mrow></mfrac><munderover><mo>∑</mo><mrow><mi>n</mi><mo>=</mo><mn>1</mn></mrow><mi>N</mi></munderover><munderover><mo>∑</mo><mrow><mi>j</mi><mo>=</mo><mn>1</mn></mrow><mn>3</mn></munderover><msup><mrow><mo>(</mo><msub><mover><mi>z</mi><mo>^</mo></mover><mrow><mi>n</mi><mo>,</mo><mi>j</mi></mrow></msub><mo>−</mo><msub><mi>z</mi><mrow><mi>n</mi><mo>,</mo><mi>j</mi></mrow></msub><mo>)</mo></mrow><mn>2</mn></msup></mrow></math>

Thus a concentration error is measured relative to that component's training variation. For example, the smaller B standard deviation gives its raw squared error a larger weight in this loss.

<!-- lecture-page -->

## 5. Backpropagation: one calculation

Take a **3 → 2 → 3** network with zero biases and the following values. For this calculation, use L = ½‖ŷ − y‖² and learning rate 0.1.

<math display="block" aria-label="Weights and data for one backpropagation example"><mtable columnalign="left"><mtr><mtd><mrow><mi mathvariant="bold">x</mi><mo>=</mo><mrow><mo>[</mo><mtable><mtr><mtd><mn>1</mn></mtd></mtr><mtr><mtd><mn>0</mn></mtd></mtr><mtr><mtd><mn>-1</mn></mtd></mtr></mtable><mo>]</mo></mrow><mo>,</mo><mi mathvariant="bold">y</mi><mo>=</mo><mrow><mo>[</mo><mtable><mtr><mtd><mn>0</mn></mtd></mtr><mtr><mtd><mn>1</mn></mtd></mtr><mtr><mtd><mn>0</mn></mtd></mtr></mtable><mo>]</mo></mrow></mrow></mtd></mtr><mtr><mtd><mrow><msub><mi mathvariant="bold">W</mi><mn>1</mn></msub><mo>=</mo><mrow><mo>[</mo><mtable><mtr><mtd><mn>1</mn></mtd><mtd><mn>0</mn></mtd><mtd><mn>0</mn></mtd></mtr><mtr><mtd><mn>0</mn></mtd><mtd><mn>0</mn></mtd><mtd><mn>1</mn></mtd></mtr></mtable><mo>]</mo></mrow><mo>,</mo><msub><mi mathvariant="bold">W</mi><mn>2</mn></msub><mo>=</mo><mrow><mo>[</mo><mtable><mtr><mtd><mn>1</mn></mtd><mtd><mn>0</mn></mtd></mtr><mtr><mtd><mn>0</mn></mtd><mtd><mn>1</mn></mtd></mtr><mtr><mtd><mn>1</mn></mtd><mtd><mn>1</mn></mtd></mtr></mtable><mo>]</mo></mrow></mrow></mtd></mtr></mtable></math>

The hidden pre-activation a, hidden activation h, prediction, and error are:

<math display="block" aria-label="Forward computation in the small network"><mrow><mi mathvariant="bold">a</mi><mo>=</mo><mrow><mo>[</mo><mtable><mtr><mtd><mn>1</mn></mtd></mtr><mtr><mtd><mn>-1</mn></mtd></mtr></mtable><mo>]</mo></mrow><mo>,</mo><mi mathvariant="bold">h</mi><mo>=</mo><mrow><mo>[</mo><mtable><mtr><mtd><mn>1</mn></mtd></mtr><mtr><mtd><mn>0</mn></mtd></mtr></mtable><mo>]</mo></mrow><mo>,</mo><mover><mi mathvariant="bold">y</mi><mo>^</mo></mover><mo>=</mo><mrow><mo>[</mo><mtable><mtr><mtd><mn>1</mn></mtd></mtr><mtr><mtd><mn>0</mn></mtd></mtr><mtr><mtd><mn>1</mn></mtd></mtr></mtable><mo>]</mo></mrow><mo>,</mo><mi mathvariant="bold">e</mi><mo>=</mo><mrow><mo>[</mo><mtable><mtr><mtd><mn>1</mn></mtd></mtr><mtr><mtd><mn>-1</mn></mtd></mtr><mtr><mtd><mn>1</mn></mtd></mtr></mtable><mo>]</mo></mrow></mrow></math>

<!-- lecture-page -->

## Gradients and the parameter update

The output error propagates through the output weights and the ReLU derivative:

<math display="block" aria-label="Backpropagation gradients for one example"><mtable columnalign="left"><mtr><mtd><mrow><msub><mi mathvariant="bold">δ</mi><mn>2</mn></msub><mo>=</mo><mi mathvariant="bold">e</mi><mo>,</mo><msub><mi>∇</mi><msub><mi mathvariant="bold">W</mi><mn>2</mn></msub></msub><mi>L</mi><mo>=</mo><mi mathvariant="bold">e</mi><msup><mi mathvariant="bold">h</mi><mi>T</mi></msup><mo>=</mo><mrow><mo>[</mo><mtable><mtr><mtd><mn>1</mn></mtd><mtd><mn>0</mn></mtd></mtr><mtr><mtd><mn>-1</mn></mtd><mtd><mn>0</mn></mtd></mtr><mtr><mtd><mn>1</mn></mtd><mtd><mn>0</mn></mtd></mtr></mtable><mo>]</mo></mrow></mrow></mtd></mtr><mtr><mtd><mrow><msub><mi mathvariant="bold">δ</mi><mn>1</mn></msub><mo>=</mo><mo>(</mo><msup><msub><mi mathvariant="bold">W</mi><mn>2</mn></msub><mi>T</mi></msup><mi mathvariant="bold">e</mi><mo>)</mo><mo>⊙</mo><mrow><mo>[</mo><mtable><mtr><mtd><mn>1</mn></mtd></mtr><mtr><mtd><mn>0</mn></mtd></mtr></mtable><mo>]</mo></mrow><mo>=</mo><mrow><mo>[</mo><mtable><mtr><mtd><mn>2</mn></mtd></mtr><mtr><mtd><mn>0</mn></mtd></mtr></mtable><mo>]</mo></mrow></mrow></mtd></mtr><mtr><mtd><mrow><msub><mi>∇</mi><msub><mi mathvariant="bold">W</mi><mn>1</mn></msub></msub><mi>L</mi><mo>=</mo><msub><mi mathvariant="bold">δ</mi><mn>1</mn></msub><msup><mi mathvariant="bold">x</mi><mi>T</mi></msup><mo>=</mo><mrow><mo>[</mo><mtable><mtr><mtd><mn>2</mn></mtd><mtd><mn>0</mn></mtd><mtd><mn>-2</mn></mtd></mtr><mtr><mtd><mn>0</mn></mtd><mtd><mn>0</mn></mtd><mtd><mn>0</mn></mtd></mtr></mtable><mo>]</mo></mrow></mrow></mtd></mtr></mtable></math>

The bias gradients are δ₁ and δ₂. Update every weight and bias with parameter ← parameter − 0.1 × gradient. The next forward calculation gives **[0.26, 0.14, 0.26]**, and the loss decreases from **1.5 to 0.4374**. The notebook checks these gradients using autograd.

<!-- lecture-page -->

## 6. Train and evaluate the steady-state model

<div class="lecture-columns" markdown="1">

<div markdown="1">

Use Adam with learning rate 0.001, batches of 64, and up to 1400 epochs. After each epoch, evaluate validation loss and retain the weights at its minimum. One batch follows these operations:

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

## Evaluate each output component

| Test RMSE, mol/L | A | B | C |
| --- | --- | --- | --- |
| Output scaling | {{ result.steady_a_rmse }} | {{ result.steady_b_rmse }} | {{ result.steady_c_rmse }} |
| Unscaled outputs | {{ result.unscaled_a_rmse }} | {{ result.unscaled_b_rmse }} | {{ result.unscaled_c_rmse }} |

In this comparison, output scaling reduces A and B RMSE; C RMSE is slightly higher. Evaluate each component rather than combining all three into one error number.

<figure><img src="{{ '/assets/courses/surrogate-models/week-02/steady-parity.png' | relative_url }}" alt="Reference-versus-predicted parity plots for the three concentrations on the test set." /><figcaption>Separate parity plots reveal each component's errors.</figcaption></figure>

<!-- lecture-page -->

## Check the concentration sum

Also calculate the concentration-sum residual:

<math display="block" aria-label="Concentration-sum residual"><mrow><mi>r</mi><mo>=</mo><mover><msub><mi>C</mi><mi>A</mi></msub><mo>^</mo></mover><mo>+</mo><mover><msub><mi>C</mi><mi>B</mi></msub><mo>^</mo></mover><mo>+</mo><mover><msub><mi>C</mi><mi>C</mi></msub><mo>^</mo></mover><mo>−</mo><msub><mi>C</mi><mi>Af</mi></msub></mrow></math>

Its test RMSE is **{{ result.steady_balance }} mol/L**. Component prediction errors and the residual describe different aspects of the model.

The three linear outputs are free predictions. Balance-consistent training labels do not force their sum to match the feed concentration.

For feed **1.2 mol/L**, predictions **[0.62, 0.41, 0.20] mol/L** sum to **1.23 mol/L**, giving **r = 0.03 mol/L**. A model predicting mole fractions can likewise return a sum different from one.

**A small prediction error does not enforce a required equality.**

<!-- lecture-page -->

## Week 4 preview: put the constraint into the model

We can correct a prediction after training, or include a constraint-respecting transformation in the training calculation.

| Approach | Where the correction enters |
| --- | --- |
| Post-training mapping/projection | Train the raw predictor, then correct its outputs. |
| KKT-hPINN | Apply a fixed affine projection using the input and raw prediction before the loss, and at inference. |

<math display="block" aria-label="Constraint-aware training flow"><mrow><mi mathvariant="bold">x</mi><mo>→</mo><msub><mi>f</mi><mi>θ</mi></msub><mo>→</mo><mover><mi mathvariant="bold">y</mi><mo>^</mo></mover><mo>→</mo><msub><mi>Π</mi><mi mathvariant="bold">x</mi></msub><mo>→</mo><mover><mi mathvariant="bold">y</mi><mo>~</mo></mover><mo>→</mo><mtext>loss</mtext></mrow></math>

KKT-hPINN computes loss on the projected output and backpropagates through the projection. Its coefficients are fixed; the MLP weights learn with that transformation in place.

**Week 4** derives the projection and KKT conditions, checks rank assumptions, and follows the gradient. The guarantee concerns the specified linear equalities, up to numerical arithmetic; nonnegativity needs an additional constraint.

Source: Chen et al., [Section 3 and Remark 3](https://arxiv.org/html/2402.07251v1#S3).

<!-- lecture-page -->

## 7. Run the required steady-state lab

Download the [steady-state notebook]({{ page.notebook | relative_url }}) or [lab bundle]({{ '/assets/courses/surrogate-models/week-02/week02-labs.zip' | relative_url }}). The bundle also preserves optional later-topic materials.

```bash
python -m pip install -r requirements.txt
python week02_lab.py --mode steady --output-dir week02-results
```

Evaluate the trained predictor by component RMSE and concentration-sum residual. The stored operating-selection results belong to the later optimization part.

<!-- lecture-page -->

## 8. Core exercises and submission

1. Derive C_A, C_B, and C_C and verify their sum. Explain the nonmonotone B curve.
2. Count the **1283** steady-state MLP parameters and verify the hand-calculated gradient update.
3. Compare scaled and unscaled outputs by each component’s RMSE.
4. Inspect concentration-sum residual and minimum predicted concentration on held-out inputs.

Submit the steady-state model, split/scaling details, checked gradient update, and component/consistency evaluation.

Original explanations: PyTorch [model construction](https://docs.pytorch.org/tutorials/beginner/basics/buildmodel_tutorial.html), [autograd](https://docs.pytorch.org/tutorials/beginner/basics/autogradqs_tutorial.html), and [training](https://docs.pytorch.org/tutorials/beginner/basics/optimization_tutorial.html).

<!-- lecture-page -->

## Reading companion

The [Week 2 companion]({{ page.reading_note | relative_url }}) and [English PDF]({{ page.reading_pdf_en | relative_url }}) explain the three-output map, parameter count, scaling, gradient update, training loop, and independent diagnostics.

<!-- lecture-page -->

## Generate dynamic concentration data

Use the same balances to generate 30 min trajectories at **Δt = 0.2 min**. There are 150 input intervals and 151 concentration times. Feed concentration and residence time are fixed within each trajectory; temperature can change between intervals. Each initial concentration vector sums to the feed concentration.

Adding the balances gives the evolution of total concentration:

<math display="block" aria-label="Dynamics of total concentration"><mrow><mfrac><mrow><mi>d</mi><mrow><mo>(</mo><msub><mi>C</mi><mi>A</mi></msub><mo>+</mo><msub><mi>C</mi><mi>B</mi></msub><mo>+</mo><msub><mi>C</mi><mi>C</mi></msub><mo>)</mo></mrow></mrow><mrow><mi>d</mi><mi>t</mi></mrow></mfrac><mo>=</mo><mfrac><mrow><msub><mi>C</mi><mi>Af</mi></msub><mo>−</mo><mo>(</mo><msub><mi>C</mi><mi>A</mi></msub><mo>+</mo><msub><mi>C</mi><mi>B</mi></msub><mo>+</mo><msub><mi>C</mi><mi>C</mi></msub><mo>)</mo></mrow><mi>τ</mi></mfrac></mrow></math>

With this initial condition and fixed feed concentration, the reference concentration sum stays equal to C_Af throughout the trajectory.

Generate **60 train, 15 validation, and 20 test trajectories**. Their transition counts are 9000, 2250, and 3000. Assign whole trajectories to the three sets. Each transition row contains the current concentrations, operating inputs, and the next concentrations.

<!-- lecture-page -->

## Learn a dynamic MLP

The network receives six values: three current concentrations and [T, τ, C_Af]. Use a **6 → 32 → 32 → 3** architecture, containing **1379 parameters**. Train its three outputs on concentration increments Δc = c_next − c_current. Standardize both inputs and increments with training statistics.

<math display="block" aria-label="Dynamic MLP inputs and concentration-increment update"><mtable columnalign="left"><mtr><mtd><mrow><msub><mi mathvariant="bold">v</mi><mi>k</mi></msub><mo>=</mo><mrow><mo>[</mo><mtable><mtr><mtd><msub><msub><mi>C</mi><mi>A</mi></msub><mi>k</mi></msub></mtd></mtr><mtr><mtd><msub><msub><mi>C</mi><mi>B</mi></msub><mi>k</mi></msub></mtd></mtr><mtr><mtd><msub><msub><mi>C</mi><mi>C</mi></msub><mi>k</mi></msub></mtd></mtr><mtr><mtd><msub><mi>T</mi><mi>k</mi></msub></mtd></mtr><mtr><mtd><msub><mi>τ</mi><mi>k</mi></msub></mtd></mtr><mtr><mtd><msub><mi>C</mi><mi>Af</mi></msub></mtd></mtr></mtable><mo>]</mo></mrow></mrow></mtd></mtr><mtr><mtd><mrow><msub><mover><mi mathvariant="bold">c</mi><mo>^</mo></mover><mrow><mi>k</mi><mo>+</mo><mn>1</mn></mrow></msub><mo>=</mo><msub><mi mathvariant="bold">c</mi><mi>k</mi></msub><mo>+</mo><msub><mi mathvariant="bold">μ</mi><mi>Δ</mi></msub><mo>+</mo><msub><mi mathvariant="bold">s</mi><mi>Δ</mi></msub><mo>⊙</mo><msub><mi>g</mi><mi>θ</mi></msub><mo>(</mo><msub><mi mathvariant="bold">ṽ</mi><mi>k</mi></msub><mo>)</mo></mrow></mtd></mtr></mtable></math>

Here μ_Δ and s_Δ restore the increment to mol/L units. Adding it to the current concentration produces the next state. Train with Adam, learning rate 0.001, batches of 512, and up to 800 epochs; retain the validation-minimum weights.

<!-- lecture-page -->

## Dynamic model training history

<figure><img src="{{ '/assets/courses/surrogate-models/week-02/dynamic-training.png' | relative_url }}" alt="Training and validation losses for standardized concentration increments." /><figcaption>The dynamic loss is measured on standardized increments.</figcaption></figure>

<!-- lecture-page -->

## One-step prediction and time-series rollout

For one-step evaluation, supply the reference concentration at each time. For rollout, begin with the specified initial concentration and then supply the model's previous prediction:

<math display="block" aria-label="One-step prediction versus autoregressive rollout"><mtable columnalign="left"><mtr><mtd><mrow><mtext>one-step:</mtext><mspace width="1em"/><msub><mover><mi mathvariant="bold">c</mi><mo>^</mo></mover><mrow><mi>k</mi><mo>+</mo><mn>1</mn></mrow></msub><mo>=</mo><msub><mi>f</mi><mi>θ</mi></msub><mo>(</mo><msub><mi mathvariant="bold">c</mi><mi>k</mi></msub><mo>,</mo><msub><mi mathvariant="bold">u</mi><mi>k</mi></msub><mo>)</mo></mrow></mtd></mtr><mtr><mtd><mrow><mtext>rollout:</mtext><mspace width="1em"/><msub><mover><mi mathvariant="bold">c</mi><mo>^</mo></mover><mrow><mi>k</mi><mo>+</mo><mn>1</mn></mrow></msub><mo>=</mo><msub><mi>f</mi><mi>θ</mi></msub><mo>(</mo><msub><mover><mi mathvariant="bold">c</mi><mo>^</mo></mover><mi>k</mi></msub><mo>,</mo><msub><mi mathvariant="bold">u</mi><mi>k</mi></msub><mo>)</mo></mrow></mtd></mtr></mtable></math>

The future input sequence remains prescribed in both evaluations. Compare a constant 330 K plan with a plan that changes from 330 to 345 K at 10 min. Both use τ = 5 min, feed = 1.2 mol/L, and initial concentrations [1.2, 0, 0] mol/L.

<!-- lecture-page -->

## Two temperature plans: full time series

<figure class="tall-figure"><img src="{{ '/assets/courses/surrogate-models/week-02/dynamic-rollout.png' | relative_url }}" alt="Two prescribed temperature plans and reference-versus-MLP time series for A, B, and C." /><figcaption>Solid curves are reference concentrations; dashed curves are MLP rollout. The temperature plan changes all three concentration histories.</figcaption></figure>

<!-- lecture-page -->

## One-step and rollout errors

| Test RMSE, mol/L | A | B | C |
| --- | --- | --- | --- |
| One-step | {{ result.one_step_a_rmse }} | {{ result.one_step_b_rmse }} | {{ result.one_step_c_rmse }} |
| 30 min rollout | {{ result.rollout_a_rmse }} | {{ result.rollout_b_rmse }} | {{ result.rollout_c_rmse }} |

| Physical check | One-step | Rollout |
| --- | --- | --- |
| Concentration-sum RMSE, mol/L | {{ result.one_step_balance }} | {{ result.rollout_balance }} |
| Minimum predicted concentration, mol/L | {{ result.one_step_min }} | {{ result.rollout_min }} |

The rollout errors are larger because the next prediction uses an already predicted state. The minimum concentration also reveals small negative predictions. Follow the component errors and concentration sum along the full trajectory.

<!-- lecture-page -->

## Follow errors over the prediction horizon

<figure><img src="{{ '/assets/courses/surrogate-models/week-02/dynamic-errors.png' | relative_url }}" alt="Component rollout RMSE and concentration-sum residual over the prediction horizon." /><figcaption>Errors over 20 test trajectories. Dotted lines show the corresponding one-step RMSE.</figcaption></figure>

<!-- lecture-page -->

## Compare the final B concentration

| Final B concentration at 30 min, mol/L | Reference | MLP rollout |
| --- | --- | --- |
| Constant 330 K | {{ result.constant_reference_b }} | {{ result.constant_predicted_b }} |
| Step from 330 to 345 K | {{ result.step_reference_b }} | {{ result.step_predicted_b }} |

The temperature-step plan gives a higher final B concentration in both calculations. The MLP underestimates the step plan's final concentration; the time-series comparison shows where the discrepancy develops.

<!-- lecture-page -->

## Later preview: Select an operating point for B production

Fix the feed at 1.2 mol/L and maximize predicted B concentration. Enumerate temperature in 0.5 K steps and residence time in 0.1 min steps, retaining candidates whose predicted component concentrations lie between zero and the feed concentration. Evaluate the selected point with the reference map.

| Quantity | Result |
| --- | --- |
| MLP-selected temperature; residence time | {{ result.selected_temperature_K }} K; {{ result.selected_tau_min }} min |
| Predicted B concentration | {{ result.predicted_C_B_mol_L }} mol/L |
| Reference B concentration at this point | {{ result.reference_C_B_mol_L }} mol/L |
| Reference-grid maximizing temperature; residence time | {{ result.reference_temperature_K }} K; {{ result.reference_tau_min }} min |
| Reference-grid maximum B concentration | {{ result.reference_grid_C_B_mol_L }} mol/L |
| Reference B yield at the MLP-selected point | {{ result.reference_yield_B }} |

<!-- lecture-page -->

## Later preview: Compare the selected operating points

<figure><img src="{{ '/assets/courses/surrogate-models/week-02/steady-decision.png' | relative_url }}" alt="Reference B concentration over temperature and residence time, with MLP-selected and reference-grid maximizing points." /><figcaption>The selected residence time is 1.7 min; the reference grid selects 1.8 min. Compare their reference B concentrations.</figcaption></figure>

<!-- ko -->

## A가 줄어들면 B는 얼마나 만들어질까?

{% assign result = site.data.week02_results %}

<div class="lecture-columns" markdown="1">

<div markdown="1">

**A → B → C**에서 원하는 중간 생성물은 **B**다. 체류시간이 짧으면 B가 충분히 만들어지지 않고, 길면 더 많은 B가 C로 반응한다.

엔지니어는 각 조건에서 세 출구 농도를 알아야 한다. 전환율 하나로는 제품 조성을 설명할 수 없다.

**한 모델이 A·B·C를 일관되게 예측할 수 있을까?**

</div>

<div markdown="1">

<figure><img src="{{ '/assets/courses/surrogate-models/week-02/motivation-engineer.png' | relative_url }}" alt="반응기의 A·B·C 생성물을 살펴보는 공정 엔지니어." /></figure>

</div>

</div>

<!-- lecture-page -->

## 출력은 세 개, 오차의 크기도 다르다

세 농도의 단위는 같아도 변화 폭은 다르다. Scaling 없는 loss는 한 성분을 더 강조할 수 있다.

이번 주는 MLP가 출력을 계산하는 방법, 한 번의 gradient 갱신으로 파라미터가 바뀌는 과정, 성분별 평가를 배운다.

<!-- lecture-page -->

## 정상상태 MLP를 학습하고 확인하기

1. A·B·C의 정상상태 label을 유도한다.
2. 데이터를 scaling하고 forward·backpropagation·파라미터 갱신 한 번을 따라간다.
3. MLP를 학습하고 성분별 RMSE와 농도 합 residual을 비교한다.

<!-- lecture-page -->

## 1. CSTR의 연속반응 A → B → C

완전혼합·일정 부피·일정 밀도·등온 CSTR에서 1차 연속반응 A → B → C를 다룬다. 유입물은 A를 포함하며 B·C의 유입 농도는 0이다. 온도는 운전 입력이다. 농도 단위는 mol/L, 온도는 K, 시간은 min이며 물질수지는 다음과 같다.

<math display="block" aria-label="Concentration balances for consecutive CSTR reactions"><mtable columnalign="left"><mtr><mtd><mrow><mfrac><mrow><mi>d</mi><msub><mi>C</mi><mi>A</mi></msub></mrow><mrow><mi>d</mi><mi>t</mi></mrow></mfrac><mo>=</mo><mfrac><mrow><msub><mi>C</mi><mi>Af</mi></msub><mo>−</mo><msub><mi>C</mi><mi>A</mi></msub></mrow><mi>τ</mi></mfrac><mo>−</mo><msub><mi>k</mi><mn>1</mn></msub><msub><mi>C</mi><mi>A</mi></msub></mrow></mtd></mtr><mtr><mtd><mrow><mfrac><mrow><mi>d</mi><msub><mi>C</mi><mi>B</mi></msub></mrow><mrow><mi>d</mi><mi>t</mi></mrow></mfrac><mo>=</mo><mo>−</mo><mfrac><msub><mi>C</mi><mi>B</mi></msub><mi>τ</mi></mfrac><mo>+</mo><msub><mi>k</mi><mn>1</mn></msub><msub><mi>C</mi><mi>A</mi></msub><mo>−</mo><msub><mi>k</mi><mn>2</mn></msub><msub><mi>C</mi><mi>B</mi></msub></mrow></mtd></mtr><mtr><mtd><mrow><mfrac><mrow><mi>d</mi><msub><mi>C</mi><mi>C</mi></msub></mrow><mrow><mi>d</mi><mi>t</mi></mrow></mfrac><mo>=</mo><mo>−</mo><mfrac><msub><mi>C</mi><mi>C</mi></msub><mi>τ</mi></mfrac><mo>+</mo><msub><mi>k</mi><mn>2</mn></msub><msub><mi>C</mi><mi>B</mi></msub></mrow></mtd></mtr></mtable></math>

<!-- lecture-page -->

## 속도상수와 운전 영역

두 속도상수의 단위는 1/min이다. 온도 의존성은 다음 식을 사용한다.

<math display="block" aria-label="Temperature-dependent first-order rate constants"><mtable columnalign="left"><mtr><mtd><mrow><msub><mi>k</mi><mn>1</mn></msub><mo>(</mo><mi>T</mi><mo>)</mo><mo>=</mo><mn>0.2</mn><mi>exp</mi><mo>[</mo><mn>6000</mn><mo>(</mo><mfrac><mn>1</mn><mn>330</mn></mfrac><mo>−</mo><mfrac><mn>1</mn><mi>T</mi></mfrac><mo>)</mo><mo>]</mo></mrow></mtd></mtr><mtr><mtd><mrow><msub><mi>k</mi><mn>2</mn></msub><mo>(</mo><mi>T</mi><mo>)</mo><mo>=</mo><mn>0.1</mn><mi>exp</mi><mo>[</mo><mn>5000</mn><mo>(</mo><mfrac><mn>1</mn><mn>330</mn></mfrac><mo>−</mo><mfrac><mn>1</mn><mi>T</mi></mfrac><mo>)</mo><mo>]</mo></mrow></mtd></mtr></mtable></math>

| 항목 | 값·범위 |
| --- | --- |
| 기준 온도 | 330 K |
| 기준 k₁; k₂ | 0.2; 0.1 /min |
| 온도 민감도 파라미터 | 6000 K; 5000 K |
| 온도 T | 300–360 K |
| 체류시간 τ | 1–10 min |
| 유입 A 농도 | 0.8–1.5 mol/L |

세 수지는 A의 소모, B의 생성·소모, C의 생성을 나타낸다. 세 식을 더하면 반응 항이 상쇄된다.

<!-- lecture-page -->

## 2. 세 출력을 갖는 정상상태 mapping 유도

시간 미분을 0으로 놓고 각 식에 τ를 곱한다. 농도 항을 모으면 다음 관계를 얻는다.

<math display="block" aria-label="Steady-state balance equations"><mtable columnalign="left"><mtr><mtd><mrow><mo>(</mo><mrow><mn>1</mn><mo>+</mo><msub><mi>k</mi><mn>1</mn></msub><mi>τ</mi></mrow><mo>)</mo><msub><mi>C</mi><mi>A</mi></msub><mo>=</mo><msub><mi>C</mi><mi>Af</mi></msub></mrow></mtd></mtr><mtr><mtd><mrow><mo>(</mo><mrow><mn>1</mn><mo>+</mo><msub><mi>k</mi><mn>2</mn></msub><mi>τ</mi></mrow><mo>)</mo><msub><mi>C</mi><mi>B</mi></msub><mo>=</mo><msub><mi>k</mi><mn>1</mn></msub><mi>τ</mi><msub><mi>C</mi><mi>A</mi></msub></mrow></mtd></mtr><mtr><mtd><mrow><msub><mi>C</mi><mi>C</mi></msub><mo>=</mo><msub><mi>k</mi><mn>2</mn></msub><mi>τ</mi><msub><mi>C</mi><mi>B</mi></msub></mrow></mtd></mtr></mtable></math>

<!-- lecture-page -->

## A·B·C 농도 계산

A, B, C 순서로 풀면 다음과 같다.

<math display="block" aria-label="Three-component steady-state mapping"><mtable columnalign="left"><mtr><mtd><mrow><msub><mi>C</mi><mi>A</mi></msub><mo>=</mo><mfrac><msub><mi>C</mi><mi>Af</mi></msub><mrow><mn>1</mn><mo>+</mo><msub><mi>k</mi><mn>1</mn></msub><mi>τ</mi></mrow></mfrac></mrow></mtd></mtr><mtr><mtd><mrow><msub><mi>C</mi><mi>B</mi></msub><mo>=</mo><mfrac><mrow><msub><mi>k</mi><mn>1</mn></msub><mi>τ</mi><msub><mi>C</mi><mi>Af</mi></msub></mrow><mrow><mo>(</mo><mrow><mn>1</mn><mo>+</mo><msub><mi>k</mi><mn>1</mn></msub><mi>τ</mi></mrow><mo>)</mo><mo>(</mo><mrow><mn>1</mn><mo>+</mo><msub><mi>k</mi><mn>2</mn></msub><mi>τ</mi></mrow><mo>)</mo></mrow></mfrac></mrow></mtd></mtr><mtr><mtd><mrow><msub><mi>C</mi><mi>C</mi></msub><mo>=</mo><msub><mi>k</mi><mn>2</mn></msub><mi>τ</mi><msub><mi>C</mi><mi>B</mi></msub></mrow></mtd></mtr></mtable></math>

330 K, τ = 5 min, 유입 농도 1.2 mol/L에서는 **[0.6, 0.4, 0.2] mol/L**이다. 세 농도의 합은 유입 농도와 같다. 이 세 출력을 정상상태 MLP의 label로 사용한다.

<!-- lecture-page -->

## B 응답이 단조롭지 않은 이유

고정 온도에서 B의 수율과 이를 최대화하는 체류시간은 C_B 식에서 얻는다.

<math display="block" aria-label="B yield and maximizing residence time at fixed temperature"><mrow><msub><mi>Y</mi><mi>B</mi></msub><mo>=</mo><mfrac><msub><mi>C</mi><mi>B</mi></msub><msub><mi>C</mi><mi>Af</mi></msub></mfrac><mo>=</mo><mfrac><mrow><msub><mi>k</mi><mn>1</mn></msub><mi>τ</mi></mrow><mrow><mo>(</mo><mrow><mn>1</mn><mo>+</mo><msub><mi>k</mi><mn>1</mn></msub><mi>τ</mi></mrow><mo>)</mo><mo>(</mo><mrow><mn>1</mn><mo>+</mo><msub><mi>k</mi><mn>2</mn></msub><mi>τ</mi></mrow><mo>)</mo></mrow></mfrac><mo>,</mo><mspace width="1em"/><msup><mi>τ</mi><mo>*</mo></msup><mo>=</mo><mfrac><mn>1</mn><msqrt><mrow><msub><mi>k</mi><mn>1</mn></msub><msub><mi>k</mi><mn>2</mn></msub></mrow></msqrt></mfrac></mrow></math>

<!-- lecture-page -->

## 세 성분의 농도 profile 비교

<div class="lecture-columns" markdown="1">

<div markdown="1">

330 K에서 τ*는 약 7.07 min이다. 체류시간이 짧으면 B가 충분히 생성되지 않고, 길면 더 많은 B가 C로 반응한다.

</div>

<div markdown="1">

<figure><img src="{{ '/assets/courses/surrogate-models/week-02/steady-profiles.png' | relative_url }}" alt="330 K에서 체류시간에 따른 A·B·C 농도와 기준 모델·MLP 비교." /><figcaption>330 K에서의 다성분 응답. B 농도는 중간 체류시간에서 최대가 된다.</figcaption></figure>

</div>

</div>

<!-- lecture-page -->

## 3. 학습 데이터 구성

한 행의 입력은 [T, τ, C_Af], 출력은 [C_A, C_B, C_C]다. 입력·출력 배열의 shape은 모두 **(N, 3)**이다. 표의 운전 영역에서 train 400개, validation 120개, test 160개를 생성하고 정상상태 식으로 label을 계산한다.

세 농도는 단위가 같지만 변화 폭이 다르다. Train 데이터의 표준편차는 약 **[0.283, 0.110, 0.217] mol/L**이다.

<!-- lecture-page -->

## 4. Forward 계산과 scaling

**3 → 32 → 32 → 3** MLP를 사용한다. Hidden layer에는 ReLU, 출력층에는 linear 연산을 둔다.

각 hidden layer는 입력의 가중합에 bias를 더한다. ReLU(a) = max(0, a)는 양수 값을 그대로 두고 음수 값을 0으로 만든다. 농도 데이터에 맞춰 학습하는 parameter는 weight와 bias다.

<math display="block" aria-label="MLP forward computation"><mtable columnalign="left"><mtr><mtd><mrow><msub><mi mathvariant="bold">h</mi><mn>1</mn></msub><mo>=</mo><mtext>ReLU</mtext><mo>(</mo><msub><mi mathvariant="bold">W</mi><mn>1</mn></msub><mi mathvariant="bold">x̃</mi><mo>+</mo><msub><mi mathvariant="bold">b</mi><mn>1</mn></msub><mo>)</mo></mrow></mtd></mtr><mtr><mtd><mrow><msub><mi mathvariant="bold">h</mi><mn>2</mn></msub><mo>=</mo><mtext>ReLU</mtext><mo>(</mo><msub><mi mathvariant="bold">W</mi><mn>2</mn></msub><msub><mi mathvariant="bold">h</mi><mn>1</mn></msub><mo>+</mo><msub><mi mathvariant="bold">b</mi><mn>2</mn></msub><mo>)</mo></mrow></mtd></mtr><mtr><mtd><mrow><mover><mi mathvariant="bold">z</mi><mo>^</mo></mover><mo>=</mo><msub><mi mathvariant="bold">W</mi><mn>3</mn></msub><msub><mi mathvariant="bold">h</mi><mn>2</mn></msub><mo>+</mo><msub><mi mathvariant="bold">b</mi><mn>3</mn></msub></mrow></mtd></mtr></mtable></math>

| 층 | Weight shape | Bias shape | Parameter 수 |
| --- | --- | --- | --- |
| 입력 → hidden 1 | 32 × 3 | 32 | 128 |
| Hidden 1 → hidden 2 | 32 × 32 | 32 | 1056 |
| Hidden 2 → 출력 | 3 × 32 | 3 | 99 |
| 합계 | | | **1283** |

<!-- lecture-page -->

## Scaling과 학습 loss

입력은 명시한 하한·상한으로 scaling한다. 각 출력은 train 평균 μ와 표준편차 s로 표준화하고, 예측 뒤 원래 단위로 되돌린다.

<math display="block" aria-label="Input scaling, output standardization, and inverse transformation"><mtable columnalign="left"><mtr><mtd><mrow><msub><mi>x̃</mi><mi>j</mi></msub><mo>=</mo><mn>2</mn><mfrac><mrow><msub><mi>x</mi><mi>j</mi></msub><mo>−</mo><msub><mi>l</mi><mi>j</mi></msub></mrow><mrow><msub><mi>u</mi><mi>j</mi></msub><mo>−</mo><msub><mi>l</mi><mi>j</mi></msub></mrow></mfrac><mo>−</mo><mn>1</mn></mrow></mtd></mtr><mtr><mtd><mrow><msub><mi>z</mi><mi>j</mi></msub><mo>=</mo><mfrac><mrow><msub><mi>y</mi><mi>j</mi></msub><mo>−</mo><msub><mi>μ</mi><mi>j</mi></msub></mrow><msub><mi>s</mi><mi>j</mi></msub></mfrac><mo>,</mo><mspace width="1em"/><msub><mover><mi>y</mi><mo>^</mo></mover><mi>j</mi></msub><mo>=</mo><msub><mi>μ</mi><mi>j</mi></msub><mo>+</mo><msub><mi>s</mi><mi>j</mi></msub><msub><mover><mi>z</mi><mo>^</mo></mover><mi>j</mi></msub></mrow></mtd></mtr></mtable></math>

Loss는 표본과 표준화된 출력 성분에 걸쳐 제곱 오차를 평균한다.

<math display="block" aria-label="Mean squared error over samples and standardized output components"><mrow><mi>L</mi><mo>=</mo><mfrac><mn>1</mn><mrow><mn>3</mn><mi>N</mi></mrow></mfrac><munderover><mo>∑</mo><mrow><mi>n</mi><mo>=</mo><mn>1</mn></mrow><mi>N</mi></munderover><munderover><mo>∑</mo><mrow><mi>j</mi><mo>=</mo><mn>1</mn></mrow><mn>3</mn></munderover><msup><mrow><mo>(</mo><msub><mover><mi>z</mi><mo>^</mo></mover><mrow><mi>n</mi><mo>,</mo><mi>j</mi></mrow></msub><mo>−</mo><msub><mi>z</mi><mrow><mi>n</mi><mo>,</mo><mi>j</mi></mrow></msub><mo>)</mo></mrow><mn>2</mn></msup></mrow></math>

농도 오차를 해당 성분의 train 변화 폭에 상대적으로 평가하는 셈이다. 표준편차가 작은 B의 원래 단위 제곱 오차에는 더 큰 가중치가 붙는다.

<!-- lecture-page -->

## 5. Backpropagation 한 번 계산하기

Bias가 모두 0인 **3 → 2 → 3** 신경망에서 다음 값을 사용한다. 이번 계산의 loss는 L = ½‖ŷ − y‖², learning rate는 0.1이다.

<math display="block" aria-label="Weights and data for one backpropagation example"><mtable columnalign="left"><mtr><mtd><mrow><mi mathvariant="bold">x</mi><mo>=</mo><mrow><mo>[</mo><mtable><mtr><mtd><mn>1</mn></mtd></mtr><mtr><mtd><mn>0</mn></mtd></mtr><mtr><mtd><mn>-1</mn></mtd></mtr></mtable><mo>]</mo></mrow><mo>,</mo><mi mathvariant="bold">y</mi><mo>=</mo><mrow><mo>[</mo><mtable><mtr><mtd><mn>0</mn></mtd></mtr><mtr><mtd><mn>1</mn></mtd></mtr><mtr><mtd><mn>0</mn></mtd></mtr></mtable><mo>]</mo></mrow></mrow></mtd></mtr><mtr><mtd><mrow><msub><mi mathvariant="bold">W</mi><mn>1</mn></msub><mo>=</mo><mrow><mo>[</mo><mtable><mtr><mtd><mn>1</mn></mtd><mtd><mn>0</mn></mtd><mtd><mn>0</mn></mtd></mtr><mtr><mtd><mn>0</mn></mtd><mtd><mn>0</mn></mtd><mtd><mn>1</mn></mtd></mtr></mtable><mo>]</mo></mrow><mo>,</mo><msub><mi mathvariant="bold">W</mi><mn>2</mn></msub><mo>=</mo><mrow><mo>[</mo><mtable><mtr><mtd><mn>1</mn></mtd><mtd><mn>0</mn></mtd></mtr><mtr><mtd><mn>0</mn></mtd><mtd><mn>1</mn></mtd></mtr><mtr><mtd><mn>1</mn></mtd><mtd><mn>1</mn></mtd></mtr></mtable><mo>]</mo></mrow></mrow></mtd></mtr></mtable></math>

Hidden pre-activation a, activation h, 예측값, 오차는 다음과 같다.

<math display="block" aria-label="Forward computation in the small network"><mrow><mi mathvariant="bold">a</mi><mo>=</mo><mrow><mo>[</mo><mtable><mtr><mtd><mn>1</mn></mtd></mtr><mtr><mtd><mn>-1</mn></mtd></mtr></mtable><mo>]</mo></mrow><mo>,</mo><mi mathvariant="bold">h</mi><mo>=</mo><mrow><mo>[</mo><mtable><mtr><mtd><mn>1</mn></mtd></mtr><mtr><mtd><mn>0</mn></mtd></mtr></mtable><mo>]</mo></mrow><mo>,</mo><mover><mi mathvariant="bold">y</mi><mo>^</mo></mover><mo>=</mo><mrow><mo>[</mo><mtable><mtr><mtd><mn>1</mn></mtd></mtr><mtr><mtd><mn>0</mn></mtd></mtr><mtr><mtd><mn>1</mn></mtd></mtr></mtable><mo>]</mo></mrow><mo>,</mo><mi mathvariant="bold">e</mi><mo>=</mo><mrow><mo>[</mo><mtable><mtr><mtd><mn>1</mn></mtd></mtr><mtr><mtd><mn>-1</mn></mtd></mtr><mtr><mtd><mn>1</mn></mtd></mtr></mtable><mo>]</mo></mrow></mrow></math>

<!-- lecture-page -->

## Gradient와 파라미터 갱신

출력 오차를 출력층 가중치와 ReLU 미분을 거쳐 전달한다.

<math display="block" aria-label="Backpropagation gradients for one example"><mtable columnalign="left"><mtr><mtd><mrow><msub><mi mathvariant="bold">δ</mi><mn>2</mn></msub><mo>=</mo><mi mathvariant="bold">e</mi><mo>,</mo><msub><mi>∇</mi><msub><mi mathvariant="bold">W</mi><mn>2</mn></msub></msub><mi>L</mi><mo>=</mo><mi mathvariant="bold">e</mi><msup><mi mathvariant="bold">h</mi><mi>T</mi></msup><mo>=</mo><mrow><mo>[</mo><mtable><mtr><mtd><mn>1</mn></mtd><mtd><mn>0</mn></mtd></mtr><mtr><mtd><mn>-1</mn></mtd><mtd><mn>0</mn></mtd></mtr><mtr><mtd><mn>1</mn></mtd><mtd><mn>0</mn></mtd></mtr></mtable><mo>]</mo></mrow></mrow></mtd></mtr><mtr><mtd><mrow><msub><mi mathvariant="bold">δ</mi><mn>1</mn></msub><mo>=</mo><mo>(</mo><msup><msub><mi mathvariant="bold">W</mi><mn>2</mn></msub><mi>T</mi></msup><mi mathvariant="bold">e</mi><mo>)</mo><mo>⊙</mo><mrow><mo>[</mo><mtable><mtr><mtd><mn>1</mn></mtd></mtr><mtr><mtd><mn>0</mn></mtd></mtr></mtable><mo>]</mo></mrow><mo>=</mo><mrow><mo>[</mo><mtable><mtr><mtd><mn>2</mn></mtd></mtr><mtr><mtd><mn>0</mn></mtd></mtr></mtable><mo>]</mo></mrow></mrow></mtd></mtr><mtr><mtd><mrow><msub><mi>∇</mi><msub><mi mathvariant="bold">W</mi><mn>1</mn></msub></msub><mi>L</mi><mo>=</mo><msub><mi mathvariant="bold">δ</mi><mn>1</mn></msub><msup><mi mathvariant="bold">x</mi><mi>T</mi></msup><mo>=</mo><mrow><mo>[</mo><mtable><mtr><mtd><mn>2</mn></mtd><mtd><mn>0</mn></mtd><mtd><mn>-2</mn></mtd></mtr><mtr><mtd><mn>0</mn></mtd><mtd><mn>0</mn></mtd><mtd><mn>0</mn></mtd></mtr></mtable><mo>]</mo></mrow></mrow></mtd></mtr></mtable></math>

Bias gradient는 각각 δ₁, δ₂다. 모든 weight·bias를 parameter ← parameter − 0.1 × gradient로 갱신한다. 다음 forward의 출력은 **[0.26, 0.14, 0.26]**, loss는 **1.5에서 0.4374**로 감소한다. Notebook에서 autograd로 이 gradient를 확인한다.

<!-- lecture-page -->

## 6. 정상상태 모델 학습과 평가

<div class="lecture-columns" markdown="1">

<div markdown="1">

Adam, learning rate 0.001, batch 64, 최대 1400 epoch를 사용한다. 매 epoch 뒤 validation loss를 계산하고 최소값의 가중치를 저장한다. 한 batch의 학습은 다음 연산으로 구성된다.

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

## 출력 성분별 평가

| Test RMSE, mol/L | A | B | C |
| --- | --- | --- | --- |
| 출력 scaling 적용 | {{ result.steady_a_rmse }} | {{ result.steady_b_rmse }} | {{ result.steady_c_rmse }} |
| 출력 scaling 미적용 | {{ result.unscaled_a_rmse }} | {{ result.unscaled_b_rmse }} | {{ result.unscaled_c_rmse }} |

이 비교에서는 출력 scaling으로 A·B RMSE가 감소하고, C RMSE는 조금 증가했다. 세 오차를 하나로 합치기보다 성분별로 확인한다.

<figure><img src="{{ '/assets/courses/surrogate-models/week-02/steady-parity.png' | relative_url }}" alt="Test 데이터의 A·B·C 농도에 대한 기준값·예측값 parity plot." /><figcaption>성분별 parity plot에서 각 출력의 오차를 확인한다.</figcaption></figure>

<!-- lecture-page -->

## 농도 합 확인

농도 합 residual도 계산한다.

<math display="block" aria-label="Concentration-sum residual"><mrow><mi>r</mi><mo>=</mo><mover><msub><mi>C</mi><mi>A</mi></msub><mo>^</mo></mover><mo>+</mo><mover><msub><mi>C</mi><mi>B</mi></msub><mo>^</mo></mover><mo>+</mo><mover><msub><mi>C</mi><mi>C</mi></msub><mo>^</mo></mover><mo>−</mo><msub><mi>C</mi><mi>Af</mi></msub></mrow></math>

Test residual RMSE는 **{{ result.steady_balance }} mol/L**이다. 성분별 예측 오차와 농도 합 residual은 모델의 서로 다른 성질을 보여준다.

세 linear output은 자유롭게 예측된다. 수지를 만족하는 label로 학습해도 예측 농도 합이 유입 농도와 같도록 강제되지는 않는다.

유입 **1.2 mol/L**에서 예측이 **[0.62, 0.41, 0.20] mol/L**이면 합은 **1.23 mol/L**, **r = 0.03 mol/L**이다. 몰분율을 예측하는 모델에서도 합이 1과 다른 값이 나올 수 있다.

**예측 오차가 작다는 것과 반드시 지켜야 할 등식을 만족한다는 것은 다르다.**

<!-- lecture-page -->

## 4주차 예고: 제약을 모델 안에 넣으면?

학습 후 예측을 보정할 수도 있고, 제약을 지키는 변환을 학습 계산 안에 넣을 수도 있다.

| 접근 | 보정이 들어가는 위치 |
| --- | --- |
| 학습 후 외부 mapping/projection | Raw predictor를 학습한 뒤 출력을 보정한다. |
| KKT-hPINN | 입력과 raw 예측을 받는 고정 affine projection을 loss 전에 적용하며, 예측할 때도 적용한다. |

<math display="block" aria-label="Constraint-aware training flow"><mrow><mi mathvariant="bold">x</mi><mo>→</mo><msub><mi>f</mi><mi>θ</mi></msub><mo>→</mo><mover><mi mathvariant="bold">y</mi><mo>^</mo></mover><mo>→</mo><msub><mi>Π</mi><mi mathvariant="bold">x</mi></msub><mo>→</mo><mover><mi mathvariant="bold">y</mi><mo>~</mo></mover><mo>→</mo><mtext>loss</mtext></mrow></math>

KKT-hPINN은 projection을 거친 출력으로 loss를 계산하고, projection을 통해 역전파한다. Layer의 계수는 고정되어 있고, MLP의 weight는 이 변환을 반영하여 학습한다.

**4주차**에서 projection·KKT 조건을 유도하고 rank 가정과 gradient를 확인한다. 보장 범위는 명시한 선형 등식의 만족(수치 연산 오차 범위)이며, 비음수성은 별도 제약이 필요하다.

원문: Chen et al., [3절과 Remark 3](https://arxiv.org/html/2402.07251v1#S3).

<!-- lecture-page -->

## 7. 필수 정상상태 실습 실행

[정상상태 Notebook]({{ page.notebook | relative_url }}) 또는 [실습 묶음]({{ '/assets/courses/surrogate-models/week-02/week02-labs.zip' | relative_url }})을 받는다. 묶음에는 후반부의 선택 자료도 보존했다.

```bash
python -m pip install -r requirements.txt
python week02_lab.py --mode steady --output-dir week02-results
```

학습한 predictor의 성분별 RMSE와 농도 합 residual을 평가한다. 기록된 운전점 선택 결과는 후반부 최적화 내용이다.

<!-- lecture-page -->

## 8. 필수 연습문제와 제출물

1. C_A·C_B·C_C를 유도하고 합을 확인한다. B 곡선이 단조롭지 않은 이유를 설명한다.
2. 정상상태 MLP의 **1283개** 파라미터와 손 계산한 gradient 갱신을 확인한다.
3. 출력 scaling 적용 전후의 성분별 RMSE를 비교한다.
4. 독립 입력에서 농도 합 residual과 최소 예측 농도를 살펴본다.

정상상태 모델, 분할·scaling 정보, 확인한 gradient 갱신, 성분별 오차·일관성 평가를 제출한다.

원문 해설: PyTorch [모델 구성](https://docs.pytorch.org/tutorials/beginner/basics/buildmodel_tutorial.html), [autograd](https://docs.pytorch.org/tutorials/beginner/basics/autogradqs_tutorial.html), [학습](https://docs.pytorch.org/tutorials/beginner/basics/optimization_tutorial.html).

<!-- lecture-page -->

## 읽기자료

[2주차 읽기자료]({{ page.reading_note | relative_url }})와 [국문 PDF]({{ page.reading_pdf_ko | relative_url }})에서 세 출력 mapping, 파라미터 수, scaling, gradient 갱신, 학습 loop와 독립 진단을 읽는다.

<!-- lecture-page -->

## 동적 농도 데이터 생성

같은 수지식으로 **Δt = 0.2 min**, 30 min 길이의 궤적을 생성한다. 입력 구간은 150개, 농도 시점은 151개다. 한 궤적 안에서 유입 농도·체류시간은 고정하고 온도를 구간 사이에서 바꾼다. 각 초기 농도 벡터의 합은 유입 농도와 같다.

세 수지를 더하면 전체 농도의 시간 변화를 얻는다.

<math display="block" aria-label="Dynamics of total concentration"><mrow><mfrac><mrow><mi>d</mi><mrow><mo>(</mo><msub><mi>C</mi><mi>A</mi></msub><mo>+</mo><msub><mi>C</mi><mi>B</mi></msub><mo>+</mo><msub><mi>C</mi><mi>C</mi></msub><mo>)</mo></mrow></mrow><mrow><mi>d</mi><mi>t</mi></mrow></mfrac><mo>=</mo><mfrac><mrow><msub><mi>C</mi><mi>Af</mi></msub><mo>−</mo><mo>(</mo><msub><mi>C</mi><mi>A</mi></msub><mo>+</mo><msub><mi>C</mi><mi>B</mi></msub><mo>+</mo><msub><mi>C</mi><mi>C</mi></msub><mo>)</mo></mrow><mi>τ</mi></mfrac></mrow></math>

이 초기 조건과 고정 유입 농도에서 기준 농도의 합은 궤적 전체에 걸쳐 C_Af를 유지한다.

**Train 60개, validation 15개, test 20개 궤적**을 생성한다. 상태전이 표본 수는 각각 9000, 2250, 3000개다. 궤적 전체를 세 집합에 배정한다. 각 행은 현재 농도, 운전 입력, 다음 농도를 포함한다.

<!-- lecture-page -->

## 동적 MLP 학습

현재 세 농도와 [T, τ, C_Af]를 합친 여섯 값을 입력한다. **6 → 32 → 32 → 3** 구조이며 parameter는 **1379개**다. 세 출력의 학습 target은 농도 변화량 Δc = c_next − c_current다. 입력과 변화량 모두 train 통계량으로 표준화한다.

<math display="block" aria-label="Dynamic MLP inputs and concentration-increment update"><mtable columnalign="left"><mtr><mtd><mrow><msub><mi mathvariant="bold">v</mi><mi>k</mi></msub><mo>=</mo><mrow><mo>[</mo><mtable><mtr><mtd><msub><msub><mi>C</mi><mi>A</mi></msub><mi>k</mi></msub></mtd></mtr><mtr><mtd><msub><msub><mi>C</mi><mi>B</mi></msub><mi>k</mi></msub></mtd></mtr><mtr><mtd><msub><msub><mi>C</mi><mi>C</mi></msub><mi>k</mi></msub></mtd></mtr><mtr><mtd><msub><mi>T</mi><mi>k</mi></msub></mtd></mtr><mtr><mtd><msub><mi>τ</mi><mi>k</mi></msub></mtd></mtr><mtr><mtd><msub><mi>C</mi><mi>Af</mi></msub></mtd></mtr></mtable><mo>]</mo></mrow></mrow></mtd></mtr><mtr><mtd><mrow><msub><mover><mi mathvariant="bold">c</mi><mo>^</mo></mover><mrow><mi>k</mi><mo>+</mo><mn>1</mn></mrow></msub><mo>=</mo><msub><mi mathvariant="bold">c</mi><mi>k</mi></msub><mo>+</mo><msub><mi mathvariant="bold">μ</mi><mi>Δ</mi></msub><mo>+</mo><msub><mi mathvariant="bold">s</mi><mi>Δ</mi></msub><mo>⊙</mo><msub><mi>g</mi><mi>θ</mi></msub><mo>(</mo><msub><mi mathvariant="bold">ṽ</mi><mi>k</mi></msub><mo>)</mo></mrow></mtd></mtr></mtable></math>

μ_Δ와 s_Δ로 변화량을 mol/L 단위로 복원한다. 이를 현재 농도에 더하면 다음 상태를 얻는다. Adam, learning rate 0.001, batch 512, 최대 800 epoch로 학습하고 validation 최소값의 가중치를 저장한다.

<!-- lecture-page -->

## 동적 모델 학습 곡선

<figure><img src="{{ '/assets/courses/surrogate-models/week-02/dynamic-training.png' | relative_url }}" alt="표준화한 농도 변화량을 학습하는 동적 MLP의 train·validation loss." /><figcaption>동적 loss는 표준화된 농도 변화량에서 계산한다.</figcaption></figure>

<!-- lecture-page -->

## One-step 예측과 시계열 rollout

One-step 평가에서는 각 시점의 기준 농도를 입력한다. Rollout에서는 지정한 초기 농도로 시작한 뒤 직전 예측값을 다음 입력으로 사용한다.

<math display="block" aria-label="One-step prediction versus autoregressive rollout"><mtable columnalign="left"><mtr><mtd><mrow><mtext>one-step:</mtext><mspace width="1em"/><msub><mover><mi mathvariant="bold">c</mi><mo>^</mo></mover><mrow><mi>k</mi><mo>+</mo><mn>1</mn></mrow></msub><mo>=</mo><msub><mi>f</mi><mi>θ</mi></msub><mo>(</mo><msub><mi mathvariant="bold">c</mi><mi>k</mi></msub><mo>,</mo><msub><mi mathvariant="bold">u</mi><mi>k</mi></msub><mo>)</mo></mrow></mtd></mtr><mtr><mtd><mrow><mtext>rollout:</mtext><mspace width="1em"/><msub><mover><mi mathvariant="bold">c</mi><mo>^</mo></mover><mrow><mi>k</mi><mo>+</mo><mn>1</mn></mrow></msub><mo>=</mo><msub><mi>f</mi><mi>θ</mi></msub><mo>(</mo><msub><mover><mi mathvariant="bold">c</mi><mo>^</mo></mover><mi>k</mi></msub><mo>,</mo><msub><mi mathvariant="bold">u</mi><mi>k</mi></msub><mo>)</mo></mrow></mtd></mtr></mtable></math>

두 평가 모두 미래 운전 입력은 주어진 계획을 사용한다. 온도 330 K 유지와 10 min에 330 → 345 K로 바꾸는 계획을 비교한다. 두 계획의 τ는 5 min, 유입 농도는 1.2 mol/L, 초기 농도는 [1.2, 0, 0] mol/L다.

<!-- lecture-page -->

## 두 온도 계획의 전체 시계열

<figure class="tall-figure"><img src="{{ '/assets/courses/surrogate-models/week-02/dynamic-rollout.png' | relative_url }}" alt="두 온도 계획과 A·B·C의 기준 농도·MLP rollout 시계열." /><figcaption>실선은 기준 농도, 점선은 MLP rollout이다. 온도 계획에 따라 세 성분의 시간 응답이 달라진다.</figcaption></figure>

<!-- lecture-page -->

## One-step과 rollout 오차

| Test RMSE, mol/L | A | B | C |
| --- | --- | --- | --- |
| One-step | {{ result.one_step_a_rmse }} | {{ result.one_step_b_rmse }} | {{ result.one_step_c_rmse }} |
| 30 min rollout | {{ result.rollout_a_rmse }} | {{ result.rollout_b_rmse }} | {{ result.rollout_c_rmse }} |

| 물리적 확인 | One-step | Rollout |
| --- | --- | --- |
| 농도 합 RMSE, mol/L | {{ result.one_step_balance }} | {{ result.rollout_balance }} |
| 최소 예측 농도, mol/L | {{ result.one_step_min }} | {{ result.rollout_min }} |

Rollout은 이미 예측한 상태에서 다음 값을 계산하므로 오차가 더 크다. 최소 농도에서는 작은 음수 예측도 확인된다. 전체 궤적에서 성분별 오차와 농도 합을 함께 살핀다.

<!-- lecture-page -->

## 예측 horizon에 따른 오차

<figure><img src="{{ '/assets/courses/surrogate-models/week-02/dynamic-errors.png' | relative_url }}" alt="예측 horizon에 따른 성분별 rollout RMSE와 농도 합 residual." /><figcaption>Test 궤적 20개의 시간별 오차. 점선은 성분별 one-step RMSE다.</figcaption></figure>

<!-- lecture-page -->

## 최종 B 농도 비교

| 30 min의 B 농도, mol/L | 기준 모델 | MLP rollout |
| --- | --- | --- |
| 330 K 유지 | {{ result.constant_reference_b }} | {{ result.constant_predicted_b }} |
| 330 → 345 K step | {{ result.step_reference_b }} | {{ result.step_predicted_b }} |

두 계산 모두 온도 step 계획의 마지막 B 농도가 더 높다. MLP는 step 계획의 마지막 농도를 작게 예측하며, 시계열 비교에서 차이가 생기는 구간을 확인할 수 있다.

<!-- lecture-page -->

## 후반부 미리보기: B 생산을 위한 운전점 선택

유입 농도를 1.2 mol/L로 고정하고 예측 B 농도를 최대화한다. 온도 간격 0.5 K, 체류시간 간격 0.1 min의 grid를 평가한다. 예측한 각 성분 농도가 0과 유입 농도 사이인 후보를 사용하고, 선택한 운전점을 기준 mapping으로 확인한다.

| 항목 | 결과 |
| --- | --- |
| MLP가 선택한 온도·체류시간 | {{ result.selected_temperature_K }} K; {{ result.selected_tau_min }} min |
| 예측 B 농도 | {{ result.predicted_C_B_mol_L }} mol/L |
| 선택한 지점의 기준 B 농도 | {{ result.reference_C_B_mol_L }} mol/L |
| 기준 grid 최대점의 온도·체류시간 | {{ result.reference_temperature_K }} K; {{ result.reference_tau_min }} min |
| 기준 grid의 최대 B 농도 | {{ result.reference_grid_C_B_mol_L }} mol/L |
| MLP 선택점의 기준 B 수율 | {{ result.reference_yield_B }} |

<!-- lecture-page -->

## 후반부 미리보기: 선택한 운전점 비교

<figure><img src="{{ '/assets/courses/surrogate-models/week-02/steady-decision.png' | relative_url }}" alt="온도·체류시간에 따른 기준 B 농도와 MLP 선택점·기준 grid 최대점." /><figcaption>MLP가 선택한 체류시간은 1.7 min, 기준 grid는 1.8 min이다. 두 지점의 기준 B 농도를 비교한다.</figcaption></figure>
