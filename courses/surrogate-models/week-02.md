---
layout: course-note
title: "Week 2: Learning Multicomponent Steady-State Responses with MLPs"
title_ko: "2주차: MLP로 다성분 정상상태 응답 학습하기"
description: "Train and evaluate a steady-state three-output MLP; follow one gradient update and check concentration consistency."
description_ko: "정상상태 세 출력 MLP를 학습·평가하고, gradient 갱신 한 번과 농도 합의 일관성을 확인합니다."
material_label: "Week 2"
material_label_ko: "2주차"
updated: "2026-10-20"
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

This week we calculate MLP outputs, follow one gradient update, and evaluate each component.

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

At 330 K, τ = 5 min, and feed = 1.2 mol/L, the concentrations are [0.6, 0.4, 0.2] mol/L. Their sum equals the feed concentration. These three outputs are the labels for the steady-state MLP.

<!-- lecture-page -->

## Nonmonotone response of intermediate B

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

Each row contains inputs [T, τ, C_Af] and outputs [C_A, C_B, C_C]. Input and output arrays both have shape (N, 3). Generate 400 train, 120 validation, and 160 test operating points within the table's bounds, then calculate their labels with the steady-state map.

The three concentrations have the same units but different variations. In the training data, their standard deviations are approximately [0.283, 0.110, 0.217] mol/L.

<!-- lecture-page -->

## 4. Forward calculation and scaling

Use a 3 → 32 → 32 → 3 MLP, with ReLU hidden layers and a linear output layer:

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

Take a 3 → 2 → 3 network with zero biases and the following values. For this calculation, use L = ½‖ŷ − y‖² and learning rate 0.1.

<math display="block" aria-label="Weights and data for one backpropagation example"><mtable columnalign="left"><mtr><mtd><mrow><mi mathvariant="bold">x</mi><mo>=</mo><mrow><mo>[</mo><mtable><mtr><mtd><mn>1</mn></mtd></mtr><mtr><mtd><mn>0</mn></mtd></mtr><mtr><mtd><mn>-1</mn></mtd></mtr></mtable><mo>]</mo></mrow><mo>,</mo><mi mathvariant="bold">y</mi><mo>=</mo><mrow><mo>[</mo><mtable><mtr><mtd><mn>0</mn></mtd></mtr><mtr><mtd><mn>1</mn></mtd></mtr><mtr><mtd><mn>0</mn></mtd></mtr></mtable><mo>]</mo></mrow></mrow></mtd></mtr><mtr><mtd><mrow><msub><mi mathvariant="bold">W</mi><mn>1</mn></msub><mo>=</mo><mrow><mo>[</mo><mtable><mtr><mtd><mn>1</mn></mtd><mtd><mn>0</mn></mtd><mtd><mn>0</mn></mtd></mtr><mtr><mtd><mn>0</mn></mtd><mtd><mn>0</mn></mtd><mtd><mn>1</mn></mtd></mtr></mtable><mo>]</mo></mrow><mo>,</mo><msub><mi mathvariant="bold">W</mi><mn>2</mn></msub><mo>=</mo><mrow><mo>[</mo><mtable><mtr><mtd><mn>1</mn></mtd><mtd><mn>0</mn></mtd></mtr><mtr><mtd><mn>0</mn></mtd><mtd><mn>1</mn></mtd></mtr><mtr><mtd><mn>1</mn></mtd><mtd><mn>1</mn></mtd></mtr></mtable><mo>]</mo></mrow></mrow></mtd></mtr></mtable></math>

The hidden pre-activation a, hidden activation h, prediction, and error are:

<math display="block" aria-label="Forward computation in the small network"><mrow><mi mathvariant="bold">a</mi><mo>=</mo><mrow><mo>[</mo><mtable><mtr><mtd><mn>1</mn></mtd></mtr><mtr><mtd><mn>-1</mn></mtd></mtr></mtable><mo>]</mo></mrow><mo>,</mo><mi mathvariant="bold">h</mi><mo>=</mo><mrow><mo>[</mo><mtable><mtr><mtd><mn>1</mn></mtd></mtr><mtr><mtd><mn>0</mn></mtd></mtr></mtable><mo>]</mo></mrow><mo>,</mo><mover><mi mathvariant="bold">y</mi><mo>^</mo></mover><mo>=</mo><mrow><mo>[</mo><mtable><mtr><mtd><mn>1</mn></mtd></mtr><mtr><mtd><mn>0</mn></mtd></mtr><mtr><mtd><mn>1</mn></mtd></mtr></mtable><mo>]</mo></mrow><mo>,</mo><mi mathvariant="bold">e</mi><mo>=</mo><mrow><mo>[</mo><mtable><mtr><mtd><mn>1</mn></mtd></mtr><mtr><mtd><mn>-1</mn></mtd></mtr><mtr><mtd><mn>1</mn></mtd></mtr></mtable><mo>]</mo></mrow></mrow></math>

<!-- lecture-page -->

## Gradients and the parameter update

The output error propagates through the output weights and the ReLU derivative:

<math display="block" aria-label="Backpropagation gradients for one example"><mtable columnalign="left"><mtr><mtd><mrow><msub><mi mathvariant="bold">δ</mi><mn>2</mn></msub><mo>=</mo><mi mathvariant="bold">e</mi><mo>,</mo><msub><mi>∇</mi><msub><mi mathvariant="bold">W</mi><mn>2</mn></msub></msub><mi>L</mi><mo>=</mo><mi mathvariant="bold">e</mi><msup><mi mathvariant="bold">h</mi><mi>T</mi></msup><mo>=</mo><mrow><mo>[</mo><mtable><mtr><mtd><mn>1</mn></mtd><mtd><mn>0</mn></mtd></mtr><mtr><mtd><mn>-1</mn></mtd><mtd><mn>0</mn></mtd></mtr><mtr><mtd><mn>1</mn></mtd><mtd><mn>0</mn></mtd></mtr></mtable><mo>]</mo></mrow></mrow></mtd></mtr><mtr><mtd><mrow><msub><mi mathvariant="bold">δ</mi><mn>1</mn></msub><mo>=</mo><mo>(</mo><msup><msub><mi mathvariant="bold">W</mi><mn>2</mn></msub><mi>T</mi></msup><mi mathvariant="bold">e</mi><mo>)</mo><mo>⊙</mo><mrow><mo>[</mo><mtable><mtr><mtd><mn>1</mn></mtd></mtr><mtr><mtd><mn>0</mn></mtd></mtr></mtable><mo>]</mo></mrow><mo>=</mo><mrow><mo>[</mo><mtable><mtr><mtd><mn>2</mn></mtd></mtr><mtr><mtd><mn>0</mn></mtd></mtr></mtable><mo>]</mo></mrow></mrow></mtd></mtr><mtr><mtd><mrow><msub><mi>∇</mi><msub><mi mathvariant="bold">W</mi><mn>1</mn></msub></msub><mi>L</mi><mo>=</mo><msub><mi mathvariant="bold">δ</mi><mn>1</mn></msub><msup><mi mathvariant="bold">x</mi><mi>T</mi></msup><mo>=</mo><mrow><mo>[</mo><mtable><mtr><mtd><mn>2</mn></mtd><mtd><mn>0</mn></mtd><mtd><mn>-2</mn></mtd></mtr><mtr><mtd><mn>0</mn></mtd><mtd><mn>0</mn></mtd><mtd><mn>0</mn></mtd></mtr></mtable><mo>]</mo></mrow></mrow></mtd></mtr></mtable></math>

The bias gradients are δ₁ and δ₂. Update every weight and bias with parameter ← parameter − 0.1 × gradient. The next forward calculation gives [0.26, 0.14, 0.26], and the loss decreases from 1.5 to 0.4374. The notebook checks these gradients using autograd.

<!-- lecture-page -->

## 6. Train and evaluate the steady-state model

<div class="lecture-columns" markdown="1">

<div markdown="1">

Use Adam with learning rate 0.001, batches of 64, and up to 1400 epochs. After each epoch, evaluate validation loss and retain the weights at its minimum.

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

<math display="block" aria-label="Concentration-sum residual"><mrow><mi>r</mi><mo>=</mo><mover><msub><mi>C</mi><mi>A</mi></msub><mo>^</mo></mover><mo>+</mo><mover><msub><mi>C</mi><mi>B</mi></msub><mo>^</mo></mover><mo>+</mo><mover><msub><mi>C</mi><mi>C</mi></msub><mo>^</mo></mover><mo>−</mo><msub><mi>C</mi><mi>Af</mi></msub></mrow></math>

Its test RMSE is {{ result.steady_balance }} mol/L. Component prediction errors and the residual describe different aspects of the model.

Balance-consistent training labels do not force the sum of the three linear outputs to match the feed concentration.

For feed 1.2 mol/L, predictions [0.62, 0.41, 0.20] mol/L sum to 1.23 mol/L, giving r = 0.03 mol/L. A model predicting mole fractions can likewise return a sum different from one.



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

Submit the steady-state model, split/scaling details, checked gradient update, and component/consistency evaluation.

Original explanations: PyTorch [model construction](https://docs.pytorch.org/tutorials/beginner/basics/buildmodel_tutorial.html), [autograd](https://docs.pytorch.org/tutorials/beginner/basics/autogradqs_tutorial.html), and [training](https://docs.pytorch.org/tutorials/beginner/basics/optimization_tutorial.html).

<!-- lecture-page -->

## Reading companion

The [Week 2 companion]({{ page.reading_note | relative_url }}) and [English PDF]({{ page.reading_pdf_en | relative_url }}) work through the three-output map, parameter count, scaling, gradient update, training, and independent evaluation.

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

<!-- lecture-page -->

## 정상상태 MLP를 학습하고 확인하기

1. A·B·C의 정상상태 기준값을 유도합니다.
2. 데이터 크기를 조정하고 순전파·역전파·파라미터 갱신을 한 번씩 계산합니다.
3. MLP를 학습해 성분별 RMSE와 농도 합 residual을 비교합니다.

<!-- lecture-page -->

## 1. CSTR의 연속반응 A → B → C

완전혼합·일정 부피·일정 밀도·등온 CSTR에서 1차 연속반응 A → B → C를 다룹니다. 유입물에는 A가 포함되고 B·C의 유입 농도는 0이며, 온도는 운전 입력입니다. 농도 단위는 mol/L, 온도는 K, 시간은 min입니다.

<math display="block" aria-label="Concentration balances for consecutive CSTR reactions"><mtable columnalign="left"><mtr><mtd><mrow><mfrac><mrow><mi>d</mi><msub><mi>C</mi><mi>A</mi></msub></mrow><mrow><mi>d</mi><mi>t</mi></mrow></mfrac><mo>=</mo><mfrac><mrow><msub><mi>C</mi><mi>Af</mi></msub><mo>−</mo><msub><mi>C</mi><mi>A</mi></msub></mrow><mi>τ</mi></mfrac><mo>−</mo><msub><mi>k</mi><mn>1</mn></msub><msub><mi>C</mi><mi>A</mi></msub></mrow></mtd></mtr><mtr><mtd><mrow><mfrac><mrow><mi>d</mi><msub><mi>C</mi><mi>B</mi></msub></mrow><mrow><mi>d</mi><mi>t</mi></mrow></mfrac><mo>=</mo><mo>−</mo><mfrac><msub><mi>C</mi><mi>B</mi></msub><mi>τ</mi></mfrac><mo>+</mo><msub><mi>k</mi><mn>1</mn></msub><msub><mi>C</mi><mi>A</mi></msub><mo>−</mo><msub><mi>k</mi><mn>2</mn></msub><msub><mi>C</mi><mi>B</mi></msub></mrow></mtd></mtr><mtr><mtd><mrow><mfrac><mrow><mi>d</mi><msub><mi>C</mi><mi>C</mi></msub></mrow><mrow><mi>d</mi><mi>t</mi></mrow></mfrac><mo>=</mo><mo>−</mo><mfrac><msub><mi>C</mi><mi>C</mi></msub><mi>τ</mi></mfrac><mo>+</mo><msub><mi>k</mi><mn>2</mn></msub><msub><mi>C</mi><mi>B</mi></msub></mrow></mtd></mtr></mtable></math>

<!-- lecture-page -->

## 속도상수와 운전 영역

두 속도상수의 단위는 1/min이며, 온도에 따라 아래 식으로 계산합니다.

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

<!-- lecture-page -->

## A·B·C 농도 계산

A를 먼저 구하고 B, C에 차례로 대입합니다.

<math display="block" aria-label="Three-component steady-state mapping"><mtable columnalign="left"><mtr><mtd><mrow><msub><mi>C</mi><mi>A</mi></msub><mo>=</mo><mfrac><msub><mi>C</mi><mi>Af</mi></msub><mrow><mn>1</mn><mo>+</mo><msub><mi>k</mi><mn>1</mn></msub><mi>τ</mi></mrow></mfrac></mrow></mtd></mtr><mtr><mtd><mrow><msub><mi>C</mi><mi>B</mi></msub><mo>=</mo><mfrac><mrow><msub><mi>k</mi><mn>1</mn></msub><mi>τ</mi><msub><mi>C</mi><mi>Af</mi></msub></mrow><mrow><mo>(</mo><mrow><mn>1</mn><mo>+</mo><msub><mi>k</mi><mn>1</mn></msub><mi>τ</mi></mrow><mo>)</mo><mo>(</mo><mrow><mn>1</mn><mo>+</mo><msub><mi>k</mi><mn>2</mn></msub><mi>τ</mi></mrow><mo>)</mo></mrow></mfrac></mrow></mtd></mtr><mtr><mtd><mrow><msub><mi>C</mi><mi>C</mi></msub><mo>=</mo><msub><mi>k</mi><mn>2</mn></msub><mi>τ</mi><msub><mi>C</mi><mi>B</mi></msub></mrow></mtd></mtr></mtable></math>

330 K, τ = 5 min, 유입 농도 1.2 mol/L에서 농도는 [0.6, 0.4, 0.2] mol/L입니다. 합은 유입 농도와 같으며, 이 세 농도를 정상상태 MLP의 기준값으로 사용합니다.

<!-- lecture-page -->

## 중간 생성물 B의 비단조 응답

온도가 고정되면 C_B 식에서 B의 수율과 그 수율을 최대화하는 체류시간을 구할 수 있습니다.

<math display="block" aria-label="B yield and maximizing residence time at fixed temperature"><mrow><msub><mi>Y</mi><mi>B</mi></msub><mo>=</mo><mfrac><msub><mi>C</mi><mi>B</mi></msub><msub><mi>C</mi><mi>Af</mi></msub></mfrac><mo>=</mo><mfrac><mrow><msub><mi>k</mi><mn>1</mn></msub><mi>τ</mi></mrow><mrow><mo>(</mo><mrow><mn>1</mn><mo>+</mo><msub><mi>k</mi><mn>1</mn></msub><mi>τ</mi></mrow><mo>)</mo><mo>(</mo><mrow><mn>1</mn><mo>+</mo><msub><mi>k</mi><mn>2</mn></msub><mi>τ</mi></mrow><mo>)</mo></mrow></mfrac><mo>,</mo><mspace width="1em"/><msup><mi>τ</mi><mo>*</mo></msup><mo>=</mo><mfrac><mn>1</mn><msqrt><mrow><msub><mi>k</mi><mn>1</mn></msub><msub><mi>k</mi><mn>2</mn></msub></mrow></msqrt></mfrac></mrow></math>

<!-- lecture-page -->

## 세 성분의 농도 profile 비교

<div class="lecture-columns" markdown="1">

<div markdown="1">

330 K에서 τ*는 약 7.07 min입니다. 짧은 체류시간에서는 B 생성이 부족하고, 체류시간이 길어지면 더 많은 B가 C로 반응합니다.

</div>

<div markdown="1">

<figure><img src="{{ '/assets/courses/surrogate-models/week-02/steady-profiles.png' | relative_url }}" alt="330 K에서 체류시간에 따른 A·B·C 농도와 기준 모델·MLP 비교." /><figcaption>330 K에서의 다성분 응답. B 농도는 중간 체류시간에서 최대가 된다.</figcaption></figure>

</div>

</div>

<!-- lecture-page -->

## 3. 학습 데이터 구성

한 행의 입력은 [T, τ, C_Af], 출력은 [C_A, C_B, C_C]이며 두 배열의 크기는 모두 (N, 3)입니다. 표의 운전 영역에서 train 400개, validation 120개, test 160개를 생성하고 정상상태 식으로 기준값을 계산합니다.

Train 데이터에서 세 농도의 표준편차는 약 [0.283, 0.110, 0.217] mol/L로, 단위가 같아도 변화 폭은 다릅니다.

<!-- lecture-page -->

## 4. Forward 계산과 scaling

3 → 32 → 32 → 3 MLP를 사용합니다. 은닉층에는 ReLU를 적용하고 출력층은 선형으로 둡니다.

각 은닉층은 입력의 가중합에 bias를 더한 뒤 ReLU(a) = max(0, a)를 적용합니다. 양수는 그대로 통과하고 음수는 0이 되며, 농도 데이터로 학습하는 파라미터는 가중치와 bias입니다.

<math display="block" aria-label="MLP forward computation"><mtable columnalign="left"><mtr><mtd><mrow><msub><mi mathvariant="bold">h</mi><mn>1</mn></msub><mo>=</mo><mtext>ReLU</mtext><mo>(</mo><msub><mi mathvariant="bold">W</mi><mn>1</mn></msub><mi mathvariant="bold">x̃</mi><mo>+</mo><msub><mi mathvariant="bold">b</mi><mn>1</mn></msub><mo>)</mo></mrow></mtd></mtr><mtr><mtd><mrow><msub><mi mathvariant="bold">h</mi><mn>2</mn></msub><mo>=</mo><mtext>ReLU</mtext><mo>(</mo><msub><mi mathvariant="bold">W</mi><mn>2</mn></msub><msub><mi mathvariant="bold">h</mi><mn>1</mn></msub><mo>+</mo><msub><mi mathvariant="bold">b</mi><mn>2</mn></msub><mo>)</mo></mrow></mtd></mtr><mtr><mtd><mrow><mover><mi mathvariant="bold">z</mi><mo>^</mo></mover><mo>=</mo><msub><mi mathvariant="bold">W</mi><mn>3</mn></msub><msub><mi mathvariant="bold">h</mi><mn>2</mn></msub><mo>+</mo><msub><mi mathvariant="bold">b</mi><mn>3</mn></msub></mrow></mtd></mtr></mtable></math>

| 층 | Weight shape | Bias shape | Parameter 수 |
| --- | --- | --- | --- |
| 입력 → hidden 1 | 32 × 3 | 32 | 128 |
| Hidden 1 → hidden 2 | 32 × 32 | 32 | 1056 |
| Hidden 2 → 출력 | 3 × 32 | 3 | 99 |
| 합계 | | | **1283** |

<!-- lecture-page -->

## Scaling과 학습 loss

입력은 명시한 하한·상한으로 크기를 조정합니다. 출력은 train 평균 μ와 표준편차 s로 표준화하고, 예측한 뒤 원래 단위로 복원합니다.

<math display="block" aria-label="Input scaling, output standardization, and inverse transformation"><mtable columnalign="left"><mtr><mtd><mrow><msub><mi>x̃</mi><mi>j</mi></msub><mo>=</mo><mn>2</mn><mfrac><mrow><msub><mi>x</mi><mi>j</mi></msub><mo>−</mo><msub><mi>l</mi><mi>j</mi></msub></mrow><mrow><msub><mi>u</mi><mi>j</mi></msub><mo>−</mo><msub><mi>l</mi><mi>j</mi></msub></mrow></mfrac><mo>−</mo><mn>1</mn></mrow></mtd></mtr><mtr><mtd><mrow><msub><mi>z</mi><mi>j</mi></msub><mo>=</mo><mfrac><mrow><msub><mi>y</mi><mi>j</mi></msub><mo>−</mo><msub><mi>μ</mi><mi>j</mi></msub></mrow><msub><mi>s</mi><mi>j</mi></msub></mfrac><mo>,</mo><mspace width="1em"/><msub><mover><mi>y</mi><mo>^</mo></mover><mi>j</mi></msub><mo>=</mo><msub><mi>μ</mi><mi>j</mi></msub><mo>+</mo><msub><mi>s</mi><mi>j</mi></msub><msub><mover><mi>z</mi><mo>^</mo></mover><mi>j</mi></msub></mrow></mtd></mtr></mtable></math>

손실함수는 표본과 표준화된 출력 성분 전체의 제곱 오차를 평균합니다.

<math display="block" aria-label="Mean squared error over samples and standardized output components"><mrow><mi>L</mi><mo>=</mo><mfrac><mn>1</mn><mrow><mn>3</mn><mi>N</mi></mrow></mfrac><munderover><mo>∑</mo><mrow><mi>n</mi><mo>=</mo><mn>1</mn></mrow><mi>N</mi></munderover><munderover><mo>∑</mo><mrow><mi>j</mi><mo>=</mo><mn>1</mn></mrow><mn>3</mn></munderover><msup><mrow><mo>(</mo><msub><mover><mi>z</mi><mo>^</mo></mover><mrow><mi>n</mi><mo>,</mo><mi>j</mi></mrow></msub><mo>−</mo><msub><mi>z</mi><mrow><mi>n</mi><mo>,</mo><mi>j</mi></mrow></msub><mo>)</mo></mrow><mn>2</mn></msup></mrow></math>

각 농도 오차를 해당 성분의 train 변화 폭에 상대적으로 평가하므로, 표준편차가 작은 B의 원래 단위 제곱 오차에는 더 큰 가중치가 붙습니다.

<!-- lecture-page -->

## 5. Backpropagation 한 번 계산하기

Bias가 모두 0인 3 → 2 → 3 신경망으로 계산합니다. 손실함수는 L = ½‖ŷ − y‖², 학습률은 0.1입니다.

<math display="block" aria-label="Weights and data for one backpropagation example"><mtable columnalign="left"><mtr><mtd><mrow><mi mathvariant="bold">x</mi><mo>=</mo><mrow><mo>[</mo><mtable><mtr><mtd><mn>1</mn></mtd></mtr><mtr><mtd><mn>0</mn></mtd></mtr><mtr><mtd><mn>-1</mn></mtd></mtr></mtable><mo>]</mo></mrow><mo>,</mo><mi mathvariant="bold">y</mi><mo>=</mo><mrow><mo>[</mo><mtable><mtr><mtd><mn>0</mn></mtd></mtr><mtr><mtd><mn>1</mn></mtd></mtr><mtr><mtd><mn>0</mn></mtd></mtr></mtable><mo>]</mo></mrow></mrow></mtd></mtr><mtr><mtd><mrow><msub><mi mathvariant="bold">W</mi><mn>1</mn></msub><mo>=</mo><mrow><mo>[</mo><mtable><mtr><mtd><mn>1</mn></mtd><mtd><mn>0</mn></mtd><mtd><mn>0</mn></mtd></mtr><mtr><mtd><mn>0</mn></mtd><mtd><mn>0</mn></mtd><mtd><mn>1</mn></mtd></mtr></mtable><mo>]</mo></mrow><mo>,</mo><msub><mi mathvariant="bold">W</mi><mn>2</mn></msub><mo>=</mo><mrow><mo>[</mo><mtable><mtr><mtd><mn>1</mn></mtd><mtd><mn>0</mn></mtd></mtr><mtr><mtd><mn>0</mn></mtd><mtd><mn>1</mn></mtd></mtr><mtr><mtd><mn>1</mn></mtd><mtd><mn>1</mn></mtd></mtr></mtable><mo>]</mo></mrow></mrow></mtd></mtr></mtable></math>

은닉층의 활성화 전 값 a와 활성화 값 h, 예측값과 오차를 구합니다.

<math display="block" aria-label="Forward computation in the small network"><mrow><mi mathvariant="bold">a</mi><mo>=</mo><mrow><mo>[</mo><mtable><mtr><mtd><mn>1</mn></mtd></mtr><mtr><mtd><mn>-1</mn></mtd></mtr></mtable><mo>]</mo></mrow><mo>,</mo><mi mathvariant="bold">h</mi><mo>=</mo><mrow><mo>[</mo><mtable><mtr><mtd><mn>1</mn></mtd></mtr><mtr><mtd><mn>0</mn></mtd></mtr></mtable><mo>]</mo></mrow><mo>,</mo><mover><mi mathvariant="bold">y</mi><mo>^</mo></mover><mo>=</mo><mrow><mo>[</mo><mtable><mtr><mtd><mn>1</mn></mtd></mtr><mtr><mtd><mn>0</mn></mtd></mtr><mtr><mtd><mn>1</mn></mtd></mtr></mtable><mo>]</mo></mrow><mo>,</mo><mi mathvariant="bold">e</mi><mo>=</mo><mrow><mo>[</mo><mtable><mtr><mtd><mn>1</mn></mtd></mtr><mtr><mtd><mn>-1</mn></mtd></mtr><mtr><mtd><mn>1</mn></mtd></mtr></mtable><mo>]</mo></mrow></mrow></math>

<!-- lecture-page -->

## Gradient와 파라미터 갱신

출력 오차를 출력층 가중치와 ReLU 미분을 거쳐 전달합니다.

<math display="block" aria-label="Backpropagation gradients for one example"><mtable columnalign="left"><mtr><mtd><mrow><msub><mi mathvariant="bold">δ</mi><mn>2</mn></msub><mo>=</mo><mi mathvariant="bold">e</mi><mo>,</mo><msub><mi>∇</mi><msub><mi mathvariant="bold">W</mi><mn>2</mn></msub></msub><mi>L</mi><mo>=</mo><mi mathvariant="bold">e</mi><msup><mi mathvariant="bold">h</mi><mi>T</mi></msup><mo>=</mo><mrow><mo>[</mo><mtable><mtr><mtd><mn>1</mn></mtd><mtd><mn>0</mn></mtd></mtr><mtr><mtd><mn>-1</mn></mtd><mtd><mn>0</mn></mtd></mtr><mtr><mtd><mn>1</mn></mtd><mtd><mn>0</mn></mtd></mtr></mtable><mo>]</mo></mrow></mrow></mtd></mtr><mtr><mtd><mrow><msub><mi mathvariant="bold">δ</mi><mn>1</mn></msub><mo>=</mo><mo>(</mo><msup><msub><mi mathvariant="bold">W</mi><mn>2</mn></msub><mi>T</mi></msup><mi mathvariant="bold">e</mi><mo>)</mo><mo>⊙</mo><mrow><mo>[</mo><mtable><mtr><mtd><mn>1</mn></mtd></mtr><mtr><mtd><mn>0</mn></mtd></mtr></mtable><mo>]</mo></mrow><mo>=</mo><mrow><mo>[</mo><mtable><mtr><mtd><mn>2</mn></mtd></mtr><mtr><mtd><mn>0</mn></mtd></mtr></mtable><mo>]</mo></mrow></mrow></mtd></mtr><mtr><mtd><mrow><msub><mi>∇</mi><msub><mi mathvariant="bold">W</mi><mn>1</mn></msub></msub><mi>L</mi><mo>=</mo><msub><mi mathvariant="bold">δ</mi><mn>1</mn></msub><msup><mi mathvariant="bold">x</mi><mi>T</mi></msup><mo>=</mo><mrow><mo>[</mo><mtable><mtr><mtd><mn>2</mn></mtd><mtd><mn>0</mn></mtd><mtd><mn>-2</mn></mtd></mtr><mtr><mtd><mn>0</mn></mtd><mtd><mn>0</mn></mtd><mtd><mn>0</mn></mtd></mtr></mtable><mo>]</mo></mrow></mrow></mtd></mtr></mtable></math>

Bias gradient는 각각 δ₁, δ₂입니다. 모든 가중치와 bias를 parameter ← parameter − 0.1 × gradient로 갱신하면 다음 순전파 출력은 [0.26, 0.14, 0.26]이고, loss는 1.5에서 0.4374로 줄어듭니다. Notebook의 autograd 결과와 손계산을 대조합니다.

<!-- lecture-page -->

## 6. 정상상태 모델 학습과 평가

<div class="lecture-columns" markdown="1">

<div markdown="1">

Adam을 학습률 0.001, batch 64, 최대 1400 epoch로 실행합니다. 매 epoch 뒤 validation loss를 계산해 가장 작은 값의 가중치를 저장합니다.

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

이번 실행에서는 출력 scaling으로 A·B RMSE가 줄었고 C RMSE는 조금 커졌습니다. 각 성분의 변화를 따로 확인해야 전체 오차 하나에 가려진 차이를 볼 수 있습니다.

<figure><img src="{{ '/assets/courses/surrogate-models/week-02/steady-parity.png' | relative_url }}" alt="Test 데이터의 A·B·C 농도에 대한 기준값·예측값 parity plot." /><figcaption>성분별 parity plot에서 각 출력의 오차를 확인한다.</figcaption></figure>

<!-- lecture-page -->

## 농도 합 확인

<math display="block" aria-label="Concentration-sum residual"><mrow><mi>r</mi><mo>=</mo><mover><msub><mi>C</mi><mi>A</mi></msub><mo>^</mo></mover><mo>+</mo><mover><msub><mi>C</mi><mi>B</mi></msub><mo>^</mo></mover><mo>+</mo><mover><msub><mi>C</mi><mi>C</mi></msub><mo>^</mo></mover><mo>−</mo><msub><mi>C</mi><mi>Af</mi></msub></mrow></math>

Test residual RMSE는 {{ result.steady_balance }} mol/L입니다. 성분별 오차로 예측 정확도를, 농도 합 residual로 해당 수지의 일관성을 평가합니다.

수지를 만족하는 기준값으로 학습해도 세 선형 출력의 합이 유입 농도와 같도록 강제되지는 않습니다.

유입 1.2 mol/L에서 예측이 [0.62, 0.41, 0.20] mol/L이면 합은 1.23 mol/L이고 r = 0.03 mol/L입니다. 몰분율을 예측할 때도 합이 1을 벗어날 수 있습니다.



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

학습한 예측 모델의 성분별 RMSE와 농도 합 residual을 평가합니다.

<!-- lecture-page -->

## 8. 필수 연습문제와 제출물

1. C_A·C_B·C_C를 유도해 합을 확인하고, B 곡선이 단조롭지 않은 이유를 설명합니다.
2. 정상상태 MLP의 파라미터 1283개와 손으로 계산한 gradient 갱신을 확인합니다.
3. 출력 scaling 전후의 성분별 RMSE를 비교합니다.
4. 독립 입력에서 농도 합 residual과 최소 예측 농도를 살펴봅니다.

정상상태 모델, 데이터 분할·scaling 정보, 확인한 gradient 갱신과 성분별 오차·일관성 평가를 제출합니다.

구현 설명은 PyTorch의 [모델 구성](https://docs.pytorch.org/tutorials/beginner/basics/buildmodel_tutorial.html), [autograd](https://docs.pytorch.org/tutorials/beginner/basics/autogradqs_tutorial.html), [학습](https://docs.pytorch.org/tutorials/beginner/basics/optimization_tutorial.html)을 참고합니다.

<!-- lecture-page -->

## 읽기자료

[2주차 읽기자료]({{ page.reading_note | relative_url }})와 [국문 PDF]({{ page.reading_pdf_ko | relative_url }})에서 세 출력의 관계식, 파라미터 수, scaling, gradient 갱신과 학습 과정을 계산하고 독립 평가를 확인합니다.

KKT-hPINN 참고문헌: Chen, H., Constante Flores, G. E., & Li, C. (2024). [Physics-informed neural networks with hard linear equality constraints](https://doi.org/10.1016/j.compchemeng.2024.108764). *Computers & Chemical Engineering*, 189, 108764.
