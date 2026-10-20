---
layout: course-note
title: "Week 3: Predicting Dynamic Responses and Rollout"
title_ko: "3주차: 동적 응답 예측과 rollout"
description: "Learn a state transition and evaluate one-step and trajectory predictions under prescribed future inputs."
description_ko: "상태전이를 학습하고 주어진 미래 입력에서 one-step·전체 궤적 예측을 평가합니다."
material_label: "Week 3"
material_label_ko: "3주차"
updated: "2026-10-20"
permalink: /courses/surrogate-models/week-03/
pdf_en: /assets/courses/surrogate-models/week-03-en.pdf
pdf_ko: /assets/courses/surrogate-models/week-03-ko.pdf
course_id: surrogate-models
reading_note: /courses/surrogate-models/week-03-reading/
reading_pdf_en: /assets/courses/surrogate-models/week-03-reading-en.pdf
reading_pdf_ko: /assets/courses/surrogate-models/week-03-reading-ko.pdf
notebook: /assets/courses/surrogate-models/week-03/week03_lab.ipynb
lab_script: /assets/courses/surrogate-models/week-03/week03_lab.py
---

## The temperature changed. Is the product ready?

A process engineer changes reactor temperature at 10 min. If the outlet flows directly into a product tank, how will B concentration change over the next 20 min?

<figure><img src="/assets/courses/surrogate-models/week-03/motivation-en.svg" alt="Engineer, reactor and lagging product response" /></figure>

<!-- lecture-page -->

## The journey to a new steady state matters

During a grade change or startup, material produced before the target composition is reached can require separation or reprocessing. The endpoint alone does not describe that transient.

At the same temperature, different current tank compositions can lead to different next responses. Learn a short state transition and apply it repeatedly to predict the full trajectory.

<figure><img src="/assets/courses/surrogate-models/week-03/initial-state-response.png" alt="Different B trajectories under identical controls" /><figcaption>T = 330 K, τ = 5 min, C_Af = 1.2 mol/L; only the initial state differs.</figcaption></figure>

<!-- lecture-page -->

## What we will build

1. Define the current state, prescribed future inputs, fixed context, and sampling interval.
2. Train a state-transition MLP on concentration increments.
3. Compare one-step predictions and 30 min rollout on held-out trajectories.

Submit the same model’s component errors in both evaluations, error versus horizon, and two temperature-plan trajectories. RNN/LSTM and encoder-decoder are optional extensions.

<!-- lecture-page -->

## A steady-state map becomes a transition map

Week 2: [T, τ, C_Af] → the composition after equilibration.

Week 3: current composition + interval input + context → composition one interval later.

<math display="block"><mtable columnalign="left"><mtr><mtd><mrow><msub><mi>c</mi><mrow><mi>k</mi><mo>+</mo><mn>1</mn></mrow></msub><mo>=</mo><msub><mi>F</mi><mrow><mi>Δt</mi></mrow></msub><mrow><mo>(</mo><msub><mi>c</mi><mrow><mi>k</mi></mrow></msub><mo>,</mo><msub><mi>u</mi><mrow><mi>k</mi></mrow></msub><mo>;</mo><mi>q</mi><mo>)</mo></mrow></mrow></mtd></mtr></mtable></math>

Repeatedly applying this map produces a trajectory. A feedforward MLP can model a dynamic transition when its inputs contain the state needed for that transition.

<!-- lecture-page -->

## State, future input, and fixed context

| Quantity | Meaning | Unit / role |
| --- | --- | --- |
| c_k = [C_A,k, C_B,k, C_C,k] | Current reactor composition | mol/L; state |
| u_k = T_k | Temperature over interval k | K; prescribed input |
| q = [τ, C_Af] | Residence time and feed concentration | min, mol/L; fixed per trajectory |
| Δt = 0.2 | Sampling interval | min; fixed for this model |

Specify c_0 and the complete temperature sequence before rollout. The temperature plan is supplied by the exercise.

<!-- lecture-page -->

## The reference CSTR

An ideal, perfectly mixed reactor has constant volume and equal inlet/outlet flow. Its consecutive first-order reactions are A → B → C with 1:1 stoichiometry. Feed contains A only. Temperature is prescribed; an energy balance is not included.

<math display="block"><mtable columnalign="left"><mtr><mtd><mrow><mfrac><mrow><mi>d</mi><msub><mi>C</mi><mrow><mi>A</mi></mrow></msub></mrow><mrow><mi>d</mi><mi>t</mi></mrow></mfrac><mo>=</mo><mfrac><mrow><msub><mi>C</mi><mrow><mi>Af</mi></mrow></msub><mo>−</mo><msub><mi>C</mi><mrow><mi>A</mi></mrow></msub></mrow><mrow><mi>τ</mi></mrow></mfrac><mo>−</mo><msub><mi>k</mi><mrow><mn>1</mn></mrow></msub><msub><mi>C</mi><mrow><mi>A</mi></mrow></msub></mrow></mtd></mtr><mtr><mtd><mrow><mfrac><mrow><mi>d</mi><msub><mi>C</mi><mrow><mi>B</mi></mrow></msub></mrow><mrow><mi>d</mi><mi>t</mi></mrow></mfrac><mo>=</mo><msub><mi>k</mi><mrow><mn>1</mn></mrow></msub><msub><mi>C</mi><mrow><mi>A</mi></mrow></msub><mo>−</mo><mfrac><mrow><msub><mi>C</mi><mrow><mi>B</mi></mrow></msub></mrow><mrow><mi>τ</mi></mrow></mfrac><mo>−</mo><msub><mi>k</mi><mrow><mn>2</mn></mrow></msub><msub><mi>C</mi><mrow><mi>B</mi></mrow></msub></mrow></mtd></mtr><mtr><mtd><mrow><mfrac><mrow><mi>d</mi><msub><mi>C</mi><mrow><mi>C</mi></mrow></msub></mrow><mrow><mi>d</mi><mi>t</mi></mrow></mfrac><mo>=</mo><msub><mi>k</mi><mrow><mn>2</mn></mrow></msub><msub><mi>C</mi><mrow><mi>B</mi></mrow></msub><mo>−</mo><mfrac><mrow><msub><mi>C</mi><mrow><mi>C</mi></mrow></msub></mrow><mrow><mi>τ</mi></mrow></mfrac></mrow></mtd></mtr></mtable></math>

k₁(T) = 0.2 exp[6000(1/330 − 1/T)], k₂(T) = 0.1 exp[5000(1/330 − 1/T)] in min⁻¹. At 330 K, k₁ = 0.2 and k₂ = 0.1 min⁻¹.

<!-- lecture-page -->

## A continuous process, sampled at fixed times

For each interval [t_k, t_k + Δt), hold T_k constant. Integrate the balances over that interval to obtain c_k+1. The state stays continuous when the input switches.

30 min / 0.2 min = 150 transitions, with 151 sampled states. The temperature step at 10 min starts at interval index 50.

The learned map predicts a 0.2 min transition. Increasing the number of applications extends the horizon; it does not change the sampling interval.

<!-- lecture-page -->

## An exact interval response for this teaching model

With constant interval inputs, the balances are affine in the state. Write dc/dt = Mc + b. The steady state c∗ satisfies Mc∗ + b = 0.

<math display="block"><mtable columnalign="left"><mtr><mtd><mrow><msub><mi>F</mi><mrow><mi>Δt</mi></mrow></msub><mrow><mo>(</mo><mi>c</mi><mo>,</mo><mi>u</mi><mo>;</mo><mi>q</mi><mo>)</mo></mrow><mo>=</mo><msup><mi>c</mi><mrow><mo>∗</mo></mrow></msup><mo>+</mo><msup><mi>e</mi><mrow><mi>M</mi><mi>Δt</mi></mrow></msup><mrow><mo>(</mo><mi>c</mi><mo>−</mo><msup><mi>c</mi><mrow><mo>∗</mo></mrow></msup><mo>)</mo></mrow></mrow></mtd></mtr></mtable></math>

The lab generates labels at the selected Δt from this analytic solution. Work through the derivations of M and the component formulas in the reading companion.

At c₀ = [1.2, 0, 0], T = 330 K, τ = 5 min, feed = 1.2 mol/L: c₁ ≈ [1.153870, 0.045672, 0.000458] mol/L.

<!-- lecture-page -->

## Build trajectories before building transition rows

Use 300-360 K, τ = 1-10 min, and feed = 0.8-1.5 mol/L. Random temperature plans contain six 5 min blocks. Each trajectory has its own initial composition, with nonnegative components summing to feed.

| Split | Trajectories | Transition rows |
| --- | --- | --- |
| Train | 60 | 9000 |
| Validation | 15 | 2250 |
| Test | 20 | 3000 |

<!-- lecture-page -->

## What does one training row contain?

| Fields | Construction |
| --- | --- |
| Input v_k | [C_A,k, C_B,k, C_C,k, T_k, τ, C_Af] |
| Next-state label | c_k+1 from the reference interval response |
| Increment target | Δc_k = c_k+1 − c_k |
| Identification | split, trajectory ID, t_k |

<math display="block"><mtable columnalign="left"><mtr><mtd><mrow><msub><mi>Δc</mi><mrow><mi>k</mi></mrow></msub><mo>=</mo><msub><mi>c</mi><mrow><mi>k</mi><mo>+</mo><mn>1</mn></mrow></msub><mo>−</mo><msub><mi>c</mi><mrow><mi>k</mi></mrow></msub></mrow></mtd></mtr><mtr><mtd><mrow><msub><mover><mi>c</mi><mo>^</mo></mover><mrow><mi>k</mi><mo>+</mo><mn>1</mn></mrow></msub><mo>=</mo><msub><mi>c</mi><mrow><mi>k</mi></mrow></msub><mo>+</mo><msub><mi>μ</mi><mrow><mi>Δ</mi></mrow></msub><mo>+</mo><msub><mi>s</mi><mrow><mi>Δ</mi></mrow></msub><mo>⊙</mo><msub><mi>g</mi><mrow><mi>θ</mi></mrow></msub><mrow><mo>(</mo><msub><mi>ṽ</mi><mrow><mi>k</mi></mrow></msub><mo>)</mo></mrow></mrow></mtd></mtr></mtable></math>

The target is a change in mol/L.

<!-- lecture-page -->

## The transition MLP and its scaling

Use 6 → 32 → 32 → 3, ReLU hidden layers, and a linear output. The parameter count is (6×32 + 32) + (32×32 + 32) + (32×3 + 3) = 1379.

Compute input and increment means/standard deviations from train rows. Apply those same statistics to validation, test, and rollout states.

The MLP predicts standardized increments. Restore each increment to mol/L before adding it to the current state. An increment model can represent a zero change, but its architecture alone does not guarantee accuracy or physical consistency.

<!-- lecture-page -->

## Train on reference current states

Each train input contains the reference current state. Minimize the mean squared standardized increment error.

<math display="block"><mtable columnalign="left"><mtr><mtd><mrow><msub><mi>L</mi><mrow><mn>1</mn></mrow></msub><mo>=</mo><mfrac><mrow><mn>1</mn></mrow><mrow><mn>3</mn><mi>N</mi></mrow></mfrac><msub><mo>∑</mo><mrow><mi>n</mi></mrow></msub><msub><mo>∑</mo><mrow><mi>j</mi></mrow></msub><msup><mrow><mo>(</mo><msub><msub><mi>g</mi><mrow><mi>θ</mi></mrow></msub><mrow><mo>(</mo><msub><mi>ṽ</mi><mrow><mi>n</mi></mrow></msub><mo>)</mo></mrow><mrow><mi>j</mi></mrow></msub><mo>−</mo><msub><mi>Δc̃</mi><mrow><mi>n</mi><mo>,</mo><mi>j</mi></mrow></msub><mo>)</mo></mrow><mrow><mn>2</mn></mrow></msup></mrow></mtd></mtr></mtable></math>

Adam: learning rate 0.001, batch size 512, up to 800 epochs. Retain the weights with minimum validation loss. Test trajectories are used after this selection.

<!-- lecture-page -->

## Training history

<figure><img src="/assets/courses/surrogate-models/week-03/dynamic-training.png" alt="Train and validation scaled increment loss" /></figure>

<!-- lecture-page -->

## Two ways to evaluate the same model

<math display="block"><mtable columnalign="left"><mtr><mtd><mrow><mtext>one-step:  </mtext><msub><mover><mi>c</mi><mo>^</mo></mover><mrow><mi>k</mi><mo>+</mo><mn>1</mn></mrow></msub><mo>=</mo><msub><mi>f</mi><mrow><mi>θ</mi></mrow></msub><mrow><mo>(</mo><msub><mi>c</mi><mrow><mi>k</mi></mrow></msub><mo>,</mo><msub><mi>u</mi><mrow><mi>k</mi></mrow></msub><mo>;</mo><mi>q</mi><mo>)</mo></mrow></mrow></mtd></mtr><mtr><mtd><mrow><mtext>rollout:  </mtext><msub><mover><mi>c</mi><mo>^</mo></mover><mrow><mi>k</mi><mo>+</mo><mn>1</mn></mrow></msub><mo>=</mo><msub><mi>f</mi><mrow><mi>θ</mi></mrow></msub><mrow><mo>(</mo><msub><mover><mi>c</mi><mo>^</mo></mover><mrow><mi>k</mi></mrow></msub><mo>,</mo><msub><mi>u</mi><mrow><mi>k</mi></mrow></msub><mo>;</mo><mi>q</mi><mo>)</mo></mrow><mo>,</mo><mtext>  </mtext><msub><mover><mi>c</mi><mo>^</mo></mover><mrow><mn>0</mn></mrow></msub><mo>=</mo><msub><mi>c</mi><mrow><mn>0</mn></mrow></msub></mrow></mtd></mtr></mtable></math>

One-step: reset the input to the reference state at every time.

Rollout: start at c₀, then feed each predicted state into the next transition. Keep all future inputs and the context identical in both evaluations.

One-step evaluation receives a new reference state at every time, so it uses more state information than a forecast initialized only once.

<!-- lecture-page -->

## Where the next state comes from

<figure><img src="/assets/courses/surrogate-models/week-03/evaluation-flow-en.svg" alt="One-step uses reference states; rollout feeds predictions back" /></figure>

Both diagrams use the same frozen transition model.

<!-- lecture-page -->

## A rollout is a short, explicit loop

Given an initial state and 150 future input intervals:

```python
pred = np.empty((len(controls) + 1, 3))
pred[0] = initial_state
for k, control in enumerate(controls):
    pred[k + 1] = dynamic_step(
        model, scaling, pred[k:k+1], control[None, :]
    )[0]
```

No reference state enters this loop after initialization. Evaluate all 150 predicted states.

<!-- lecture-page -->

## How local error propagates

Let e_k = ĉ_k − c_k. Add and subtract the prediction at the reference state:

<math display="block"><mtable columnalign="left"><mtr><mtd><mrow><msub><mi>e</mi><mrow><mi>k</mi><mo>+</mo><mn>1</mn></mrow></msub><mo>=</mo><msub><mi>f</mi><mrow><mi>θ</mi></mrow></msub><mrow><mo>(</mo><msub><mover><mi>c</mi><mo>^</mo></mover><mrow><mi>k</mi></mrow></msub><mo>,</mo><msub><mi>u</mi><mrow><mi>k</mi></mrow></msub><mo>)</mo></mrow><mo>−</mo><msub><mi>f</mi><mrow><mi>θ</mi></mrow></msub><mrow><mo>(</mo><msub><mi>c</mi><mrow><mi>k</mi></mrow></msub><mo>,</mo><msub><mi>u</mi><mrow><mi>k</mi></mrow></msub><mo>)</mo></mrow><mo>+</mo><msub><mi>δ</mi><mrow><mi>k</mi></mrow></msub></mrow></mtd></mtr><mtr><mtd><mrow><msub><mi>δ</mi><mrow><mi>k</mi></mrow></msub><mo>=</mo><msub><mi>f</mi><mrow><mi>θ</mi></mrow></msub><mrow><mo>(</mo><msub><mi>c</mi><mrow><mi>k</mi></mrow></msub><mo>,</mo><msub><mi>u</mi><mrow><mi>k</mi></mrow></msub><mo>)</mo></mrow><mo>−</mo><msub><mi>F</mi><mrow><mi>Δt</mi></mrow></msub><mrow><mo>(</mo><msub><mi>c</mi><mrow><mi>k</mi></mrow></msub><mo>,</mo><msub><mi>u</mi><mrow><mi>k</mi></mrow></msub><mo>)</mo></mrow></mrow></mtd></mtr></mtable></math>

The first difference transports the existing state error through the learned map. δ_k is the local prediction error at the reference state. Even a small δ_k enters each successive prediction.

<!-- lecture-page -->

## Small one-step error can accumulate

For a scalar illustration, let the reference be F(c) = 0.9c and the learned map be f(c) = 0.9c + 0.001. Start with e₀ = 0.

<math display="block"><mtable columnalign="left"><mtr><mtd><mrow><msub><mi>e</mi><mrow><mi>h</mi><mo>+</mo><mn>1</mn></mrow></msub><mo>=</mo><mn>0.9</mn><msub><mi>e</mi><mrow><mi>h</mi></mrow></msub><mo>+</mo><mn>0.001</mn></mrow></mtd></mtr><mtr><mtd><mrow><msub><mi>e</mi><mrow><mi>h</mi></mrow></msub><mo>=</mo><mn>0.001</mn><mfrac><mrow><mn>1</mn><mo>−</mo><msup><mn>0.9</mn><mrow><mi>h</mi></mrow></msup></mrow><mrow><mn>1</mn><mo>−</mo><mn>0.9</mn></mrow></mfrac></mrow></mtd></mtr></mtable></math>

One-step bias is 0.001; at 10 recursive steps the error is about 0.00651. A contracting map limits the accumulation. A different state sensitivity can produce a different horizon pattern.

<!-- lecture-page -->

## The state sensitivity matters too

<figure><img src="/assets/courses/surrogate-models/week-03/error-recurrence.png" alt="Error recurrence for sensitivities 0.9, 1 and 1.02" /></figure>

These are scalar examples, not fitted CSTR results. Actual rollout errors can increase, level off, or change sign.

<!-- lecture-page -->

## Two prescribed temperature plans

| Setting | Constant plan | Step plan |
| --- | --- | --- |
| Initial composition, mol/L | [1.2, 0, 0] | [1.2, 0, 0] |
| τ; C_Af | 5 min; 1.2 mol/L | 5 min; 1.2 mol/L |
| 0 ≤ t < 10 min | 330 K | 330 K |
| 10 ≤ t ≤ 30 min | 330 K | 345 K |

Compare reference trajectories and the MLP rollout under exactly the same plans. Check when the curves separate and how they approach their new steady response.

<!-- lecture-page -->

## A, B, and C over the full trajectory

<figure class="tall-figure"><img src="/assets/courses/surrogate-models/week-03/dynamic-rollout.png" alt="Temperature plans and concentration trajectories" /></figure>

<!-- lecture-page -->

## Compare error in physical units

| RMSE, mol/L | A | B | C |
| --- | --- | --- | --- |
| One-step | 0.001170 | 0.001288 | 0.001163 |
| Rollout | 0.009465 | 0.009629 | 0.010425 |

Results from 20 held-out trajectories, 150 predicted times each. Rollout errors are larger in this stored run. Compute per-component RMSE across the 3000 predictions, then also inspect each horizon separately.

<math display="block"><mtable columnalign="left"><mtr><mtd><mrow><msub><mi>RMSE</mi><mrow><mi>j</mi><mo>,</mo><mi>h</mi></mrow></msub><mo>=</mo><msqrt><mfrac><mrow><mn>1</mn></mrow><mrow><mi>N</mi></mrow></mfrac><msub><mo>∑</mo><mrow><mi>n</mi></mrow></msub><msup><mrow><mo>(</mo><msub><mover><mi>C</mi><mo>^</mo></mover><mrow><mi>n</mi><mo>,</mo><mi>h</mi><mo>,</mo><mi>j</mi></mrow></msub><mo>−</mo><msub><mi>C</mi><mrow><mi>n</mi><mo>,</mo><mi>h</mi><mo>,</mo><mi>j</mi></mrow></msub><mo>)</mo></mrow><mrow><mn>2</mn></mrow></msup></msqrt></mrow></mtd></mtr></mtable></math>

Here n indexes test trajectories, h the number of transitions, and j the component.

<!-- lecture-page -->

## Read the error versus horizon

<figure><img src="/assets/courses/surrogate-models/week-03/dynamic-errors.png" alt="Component RMSE and sum residual over the horizon" /></figure>

<!-- lecture-page -->

## Physical checks along the trajectory

<math display="block"><mtable columnalign="left"><mtr><mtd><mrow><mi>S</mi><mo>=</mo><msub><mi>C</mi><mrow><mi>A</mi></mrow></msub><mo>+</mo><msub><mi>C</mi><mrow><mi>B</mi></mrow></msub><mo>+</mo><msub><mi>C</mi><mrow><mi>C</mi></mrow></msub><mo>,</mo><mtext>  </mtext><mfrac><mrow><mi>d</mi><mi>S</mi></mrow><mrow><mi>d</mi><mi>t</mi></mrow></mfrac><mo>=</mo><mfrac><mrow><msub><mi>C</mi><mrow><mi>Af</mi></mrow></msub><mo>−</mo><mi>S</mi></mrow><mrow><mi>τ</mi></mrow></mfrac></mrow></mtd></mtr><mtr><mtd><mrow><msub><mi>S</mi><mrow><mi>k</mi><mo>+</mo><mn>1</mn></mrow></msub><mo>=</mo><msub><mi>C</mi><mrow><mi>Af</mi></mrow></msub><mo>+</mo><mrow><mo>(</mo><msub><mi>S</mi><mrow><mi>k</mi></mrow></msub><mo>−</mo><msub><mi>C</mi><mrow><mi>Af</mi></mrow></msub><mo>)</mo></mrow><msup><mi>e</mi><mrow><mo>−</mo><mi>Δt</mi><mo>/</mo><mi>τ</mi></mrow></msup></mrow></mtd></mtr></mtable></math>

With S₀ = C_Af and fixed feed, the reference sum stays equal to feed. The learned outputs need not satisfy this relation.

| Check, mol/L | One-step | Rollout |
| --- | --- | --- |
| Sum-residual RMSE | 0.000051 | 0.002014 |
| Minimum prediction | -0.001152 | -0.005166 |

<!-- lecture-page -->

## Return to the engineer’s question

| B at 30 min, mol/L | Reference | MLP rollout |
| --- | --- | --- |
| Constant 330 K | 0.400091 | 0.399819 |
| 330 → 345 K at 10 min | 0.420021 | 0.411526 |

Both calculations give more B at 30 min under the step plan. The MLP underestimates that endpoint by about 0.00850 mol/L. The full trajectory reveals the transient that a final steady-state value cannot describe.

A time-dependent product specification would require checking the relevant interval, not just this final sample.

<!-- lecture-page -->

## Run the local lab and submit the comparison

The supplied [lab bundle](/assets/courses/surrogate-models/week-03/week03-lab.zip) includes the reference, stored model, scaling, plots, and [notebook](/assets/courses/surrogate-models/week-03/week03_lab.ipynb).

```bash
python -m pip install -r requirements.txt
python week03_lab.py --output-dir week03-results
# Optional: train again with the same data construction
python week03_lab.py --train --output-dir week03-retrained
```

Submit state/input definitions, split/scaling details, one-step and rollout RMSE, horizon plots, and the two temperature-plan trajectories.

<!-- lecture-page -->

## Exercises and direct reading

1. Derive dS/dt and state the condition for S to remain equal to feed.
2. Compute the first 0.2 min transition and compare it with forward Euler.
3. Explain why the same MLP receives different state inputs in the two evaluations.
4. Change an initial state while keeping the input plan fixed. Compare both reference and predicted trajectories.

Work through the derivations, examples, code, and answer checks in the [reading companion](/courses/surrogate-models/week-03-reading/). It develops the error recurrence and treats multi-step training as an optional extension.

<!-- lecture-page -->

## Optional: when a hidden state helps

The core example supplies all three concentration states and prescribed temperature. If measurements omit relevant states, a history of observations and inputs can help reconstruct them.

<math display="block"><mtable columnalign="left"><mtr><mtd><mrow><msub><mi>h</mi><mrow><mi>k</mi></mrow></msub><mo>=</mo><mi>φ</mi><mrow><mo>(</mo><msub><mi>W</mi><mrow><mi>x</mi></mrow></msub><msub><mi>x</mi><mrow><mi>k</mi></mrow></msub><mo>+</mo><msub><mi>W</mi><mrow><mi>h</mi></mrow></msub><msub><mi>h</mi><mrow><mi>k</mi><mo>−</mo><mn>1</mn></mrow></msub><mo>+</mo><mi>b</mi><mo>)</mo></mrow></mrow></mtd></mtr><mtr><mtd><mrow><msub><mover><mi>y</mi><mo>^</mo></mover><mrow><mi>k</mi></mrow></msub><mo>=</mo><msub><mi>W</mi><mrow><mi>y</mi></mrow></msub><msub><mi>h</mi><mrow><mi>k</mi></mrow></msub><mo>+</mo><msub><mi>b</mi><mrow><mi>y</mi></mrow></msub></mrow></mtd></mtr></mtable></math>

An RNN updates a learned hidden state. An LSTM adds gated memory updates. Compare these models with the same trajectory split and forecast information.

Implementation: PyTorch [RNN](https://docs.pytorch.org/docs/stable/generated/torch.nn.RNN.html) and [LSTM](https://docs.pytorch.org/docs/stable/generated/torch.nn.LSTM.html).

<!-- lecture-page -->

## Optional: an encoder and a trajectory decoder

Encoder: summarize past observations and inputs into a state representation.

Decoder: predict the future concentration sequence using that representation and the prescribed future input plan. Ensure each future input reaches the corresponding prediction step.

Read Sutskever, Vinyals & Le (2014), Sections 1-2, for the sequence-to-sequence idea.

Use the [original paper](https://proceedings.neurips.cc/paper_files/paper/2014/hash/5a18e133cbf9f257297f410bb7eca942-Abstract.html) for reference and work through the additional derivations in the companion.

<!-- ko -->

## 온도를 바꿨다. 제품도 바로 바뀔까?

공정 엔지니어가 10분에 반응기 온도를 바꿉니다. 출구 유체가 곧바로 제품 탱크에 들어간다면 앞으로 20분 동안 B 농도는 어떻게 변할까요?

<figure><img src="/assets/courses/surrogate-models/week-03/motivation-ko.svg" alt="엔지니어와 반응기, 온도 변경 후 천천히 달라지는 제품 농도" /></figure>

<!-- lecture-page -->

## 새 정상상태로 가는 과정이 중요하다

제품 전환이나 기동 중 목표 조성에 도달하기 전에 나온 유체는 따로 모으거나 다시 처리해야 할 수 있습니다. 최종 농도만으로는 이 과도 구간을 설명할 수 없습니다.

온도가 같아도 탱크 안의 현재 조성이 다르면 다음 응답이 달라질 수 있습니다. 짧은 상태전이를 학습하고 반복 적용해 전체 궤적을 예측해봅니다.

<figure><img src="/assets/courses/surrogate-models/week-03/initial-state-response.png" alt="같은 운전 입력에서도 초기 상태에 따라 달라지는 B 농도" /><figcaption>T = 330 K, τ = 5 min, C_Af = 1.2 mol/L. 초기 상태만 다르다.</figcaption></figure>

<!-- lecture-page -->

## 이번 주에 만들 것

1. 현재 상태, 주어진 미래 입력, 고정 조건(context)과 표본 간격을 정의합니다.
2. 농도 변화량을 학습하는 상태전이 MLP를 만듭니다.
3. 독립 test 궤적에서 one-step 예측과 30분 rollout을 비교합니다.

같은 모델의 두 평가에서 성분별 오차, 예측 거리(horizon)에 따른 오차와 두 온도 계획의 궤적을 제출합니다. RNN/LSTM과 encoder-decoder는 선택 확장입니다.

<!-- lecture-page -->

## 정상상태 mapping에서 상태전이 mapping으로

2주차: [T, τ, C_Af] → 정상상태에 도달한 뒤의 조성.

3주차: 현재 조성 + 해당 구간 입력 + context → 한 구간 뒤의 조성.

<math display="block"><mtable columnalign="left"><mtr><mtd><mrow><msub><mi>c</mi><mrow><mi>k</mi><mo>+</mo><mn>1</mn></mrow></msub><mo>=</mo><msub><mi>F</mi><mrow><mi>Δt</mi></mrow></msub><mrow><mo>(</mo><msub><mi>c</mi><mrow><mi>k</mi></mrow></msub><mo>,</mo><msub><mi>u</mi><mrow><mi>k</mi></mrow></msub><mo>;</mo><mi>q</mi><mo>)</mo></mrow></mrow></mtd></mtr></mtable></math>

이 관계식을 반복 적용하면 궤적을 얻습니다. 전이에 필요한 상태를 입력에 포함하면 feedforward MLP로도 동적 상태전이를 학습할 수 있습니다.

<!-- lecture-page -->

## 상태·미래 입력·고정 context

| 기호 | 의미 | 단위·역할 |
| --- | --- | --- |
| c_k = [C_A,k, C_B,k, C_C,k] | 현재 반응기 조성 | mol/L; 상태 |
| u_k = T_k | k번째 구간의 온도 | K; 주어진 입력 |
| q = [τ, C_Af] | 체류시간·유입 농도 | min, mol/L; 궤적별 고정 |
| Δt = 0.2 | Sampling interval | min; 이 모델에서 고정 |

Rollout 전에 c_0와 전체 온도 입력열을 정합니다. 실습에서는 온도 계획이 주어집니다.

<!-- lecture-page -->

## 기준 CSTR

완전 혼합·일정 부피·동일한 유입 및 유출 유량을 가정하는 이상적 반응기입니다. 1:1 화학양론의 1차 연속반응 A → B → C를 사용하며 유입에는 A만 포함됩니다. 온도는 주어지고 에너지수지는 포함하지 않습니다.

<math display="block"><mtable columnalign="left"><mtr><mtd><mrow><mfrac><mrow><mi>d</mi><msub><mi>C</mi><mrow><mi>A</mi></mrow></msub></mrow><mrow><mi>d</mi><mi>t</mi></mrow></mfrac><mo>=</mo><mfrac><mrow><msub><mi>C</mi><mrow><mi>Af</mi></mrow></msub><mo>−</mo><msub><mi>C</mi><mrow><mi>A</mi></mrow></msub></mrow><mrow><mi>τ</mi></mrow></mfrac><mo>−</mo><msub><mi>k</mi><mrow><mn>1</mn></mrow></msub><msub><mi>C</mi><mrow><mi>A</mi></mrow></msub></mrow></mtd></mtr><mtr><mtd><mrow><mfrac><mrow><mi>d</mi><msub><mi>C</mi><mrow><mi>B</mi></mrow></msub></mrow><mrow><mi>d</mi><mi>t</mi></mrow></mfrac><mo>=</mo><msub><mi>k</mi><mrow><mn>1</mn></mrow></msub><msub><mi>C</mi><mrow><mi>A</mi></mrow></msub><mo>−</mo><mfrac><mrow><msub><mi>C</mi><mrow><mi>B</mi></mrow></msub></mrow><mrow><mi>τ</mi></mrow></mfrac><mo>−</mo><msub><mi>k</mi><mrow><mn>2</mn></mrow></msub><msub><mi>C</mi><mrow><mi>B</mi></mrow></msub></mrow></mtd></mtr><mtr><mtd><mrow><mfrac><mrow><mi>d</mi><msub><mi>C</mi><mrow><mi>C</mi></mrow></msub></mrow><mrow><mi>d</mi><mi>t</mi></mrow></mfrac><mo>=</mo><msub><mi>k</mi><mrow><mn>2</mn></mrow></msub><msub><mi>C</mi><mrow><mi>B</mi></mrow></msub><mo>−</mo><mfrac><mrow><msub><mi>C</mi><mrow><mi>C</mi></mrow></msub></mrow><mrow><mi>τ</mi></mrow></mfrac></mrow></mtd></mtr></mtable></math>

k₁(T) = 0.2 exp[6000(1/330 − 1/T)], k₂(T) = 0.1 exp[5000(1/330 − 1/T)]이며 단위는 min⁻¹입니다. 330 K에서 k₁ = 0.2, k₂ = 0.1 min⁻¹입니다.

<!-- lecture-page -->

## 연속 공정을 일정 간격으로 관찰하기

각 구간 [t_k, t_k + Δt)에서 T_k를 일정하게 유지하고 수지를 적분해 c_k+1을 구합니다. 입력이 바뀌는 순간에도 상태는 연속입니다.

30 min / 0.2 min = 상태전이 150개이며, 초기값을 포함한 관찰 상태는 151개입니다. 10분 온도 변경은 index 50 구간에서 시작합니다.

학습한 관계식은 0.2분 전이를 예측합니다. 반복 횟수를 늘리면 예측 거리가 길어지고 표본 간격은 그대로 유지됩니다.

<!-- lecture-page -->

## 이 교육 모델의 구간 응답 계산

구간 입력이 일정하면 수지는 상태에 대해 affine합니다. dc/dt = Mc + b로 나타낼 때 정상상태 c∗는 Mc∗ + b = 0을 만족합니다.

<math display="block"><mtable columnalign="left"><mtr><mtd><mrow><msub><mi>F</mi><mrow><mi>Δt</mi></mrow></msub><mrow><mo>(</mo><mi>c</mi><mo>,</mo><mi>u</mi><mo>;</mo><mi>q</mi><mo>)</mo></mrow><mo>=</mo><msup><mi>c</mi><mrow><mo>∗</mo></mrow></msup><mo>+</mo><msup><mi>e</mi><mrow><mi>M</mi><mi>Δt</mi></mrow></msup><mrow><mo>(</mo><mi>c</mi><mo>−</mo><msup><mi>c</mi><mrow><mo>∗</mo></mrow></msup><mo>)</mo></mrow></mrow></mtd></mtr></mtable></math>

실습은 이 식의 해석해로 정한 Δt의 기준값을 생성합니다. M과 성분별 식의 유도는 읽기자료에서 확인합니다.

c₀ = [1.2, 0, 0], T = 330 K, τ = 5 min, feed = 1.2 mol/L이면 c₁ ≈ [1.153870, 0.045672, 0.000458] mol/L입니다.

<!-- lecture-page -->

## 궤적을 만든 뒤 상태전이 행을 만든다

300-360 K, τ = 1-10 min, feed = 0.8-1.5 mol/L를 사용합니다. 무작위 온도 계획은 5분 구간 6개로 구성하며, 각 궤적의 초기 조성은 비음수이고 합은 유입 농도입니다.

| 분할 | 궤적 수 | 상태전이 행 수 |
| --- | --- | --- |
| Train | 60 | 9000 |
| Validation | 15 | 2250 |
| Test | 20 | 3000 |

<!-- lecture-page -->

## 학습 데이터 한 행에는 무엇이 들어갈까?

| 항목 | 구성 |
| --- | --- |
| 입력 v_k | [C_A,k, C_B,k, C_C,k, T_k, τ, C_Af] |
| 다음 상태 label | 기준 구간 응답으로 계산한 c_k+1 |
| 변화량 target | Δc_k = c_k+1 − c_k |
| 식별 정보 | split, 궤적 ID, t_k |

<math display="block"><mtable columnalign="left"><mtr><mtd><mrow><msub><mi>Δc</mi><mrow><mi>k</mi></mrow></msub><mo>=</mo><msub><mi>c</mi><mrow><mi>k</mi><mo>+</mo><mn>1</mn></mrow></msub><mo>−</mo><msub><mi>c</mi><mrow><mi>k</mi></mrow></msub></mrow></mtd></mtr><mtr><mtd><mrow><msub><mover><mi>c</mi><mo>^</mo></mover><mrow><mi>k</mi><mo>+</mo><mn>1</mn></mrow></msub><mo>=</mo><msub><mi>c</mi><mrow><mi>k</mi></mrow></msub><mo>+</mo><msub><mi>μ</mi><mrow><mi>Δ</mi></mrow></msub><mo>+</mo><msub><mi>s</mi><mrow><mi>Δ</mi></mrow></msub><mo>⊙</mo><msub><mi>g</mi><mrow><mi>θ</mi></mrow></msub><mrow><mo>(</mo><msub><mi>ṽ</mi><mrow><mi>k</mi></mrow></msub><mo>)</mo></mrow></mrow></mtd></mtr></mtable></math>

학습 대상은 mol/L 단위의 농도 변화량입니다.

<!-- lecture-page -->

## 상태전이 MLP와 scaling

6 → 32 → 32 → 3 MLP에 ReLU 은닉층과 선형 출력층을 사용합니다. 파라미터 수는 (6×32 + 32) + (32×32 + 32) + (32×3 + 3) = 1379개입니다.

입력과 변화량의 평균·표준편차는 train 행으로 계산하며, 같은 통계량을 validation·test·rollout 상태에 적용합니다.

MLP가 예측한 표준화 변화량을 mol/L로 복원해 현재 상태에 더합니다. 변화량 모델은 변화가 0인 응답도 표현할 수 있지만 정확도나 물리적 일관성을 구조만으로 보장하지는 않습니다.

<!-- lecture-page -->

## 기준 현재 상태에서 학습하기

각 train 입력에는 기준 현재 상태를 넣고, 표준화 변화량의 평균제곱 오차를 최소화합니다.

<math display="block"><mtable columnalign="left"><mtr><mtd><mrow><msub><mi>L</mi><mrow><mn>1</mn></mrow></msub><mo>=</mo><mfrac><mrow><mn>1</mn></mrow><mrow><mn>3</mn><mi>N</mi></mrow></mfrac><msub><mo>∑</mo><mrow><mi>n</mi></mrow></msub><msub><mo>∑</mo><mrow><mi>j</mi></mrow></msub><msup><mrow><mo>(</mo><msub><msub><mi>g</mi><mrow><mi>θ</mi></mrow></msub><mrow><mo>(</mo><msub><mi>ṽ</mi><mrow><mi>n</mi></mrow></msub><mo>)</mo></mrow><mrow><mi>j</mi></mrow></msub><mo>−</mo><msub><mi>Δc̃</mi><mrow><mi>n</mi><mo>,</mo><mi>j</mi></mrow></msub><mo>)</mo></mrow><mrow><mn>2</mn></mrow></msup></mrow></mtd></mtr></mtable></math>

Adam을 학습률 0.001, batch size 512, 최대 800 epoch로 실행합니다. Validation loss가 가장 작은 가중치를 보관한 뒤 test 궤적을 평가합니다.

<!-- lecture-page -->

## 학습 곡선

<figure><img src="/assets/courses/surrogate-models/week-03/dynamic-training.png" alt="Train·validation의 표준화된 변화량 loss" /></figure>

<!-- lecture-page -->

## 같은 모델을 평가하는 두 방법

<math display="block"><mtable columnalign="left"><mtr><mtd><mrow><mtext>one-step:  </mtext><msub><mover><mi>c</mi><mo>^</mo></mover><mrow><mi>k</mi><mo>+</mo><mn>1</mn></mrow></msub><mo>=</mo><msub><mi>f</mi><mrow><mi>θ</mi></mrow></msub><mrow><mo>(</mo><msub><mi>c</mi><mrow><mi>k</mi></mrow></msub><mo>,</mo><msub><mi>u</mi><mrow><mi>k</mi></mrow></msub><mo>;</mo><mi>q</mi><mo>)</mo></mrow></mrow></mtd></mtr><mtr><mtd><mrow><mtext>rollout:  </mtext><msub><mover><mi>c</mi><mo>^</mo></mover><mrow><mi>k</mi><mo>+</mo><mn>1</mn></mrow></msub><mo>=</mo><msub><mi>f</mi><mrow><mi>θ</mi></mrow></msub><mrow><mo>(</mo><msub><mover><mi>c</mi><mo>^</mo></mover><mrow><mi>k</mi></mrow></msub><mo>,</mo><msub><mi>u</mi><mrow><mi>k</mi></mrow></msub><mo>;</mo><mi>q</mi><mo>)</mo></mrow><mo>,</mo><mtext>  </mtext><msub><mover><mi>c</mi><mo>^</mo></mover><mrow><mn>0</mn></mrow></msub><mo>=</mo><msub><mi>c</mi><mrow><mn>0</mn></mrow></msub></mrow></mtd></mtr></mtable></math>

One-step에서는 매 시각 기준 상태를 입력으로 새로 넣습니다.

Rollout에서는 c₀에서 시작해 예측 상태를 다음 전이에 계속 넣습니다. 두 평가의 미래 입력과 context는 동일하게 유지합니다.

One-step은 매 시각 기준 상태를 다시 받으므로, 초기 상태에서 한 번만 시작하는 예측보다 더 많은 상태 정보를 사용합니다.

<!-- lecture-page -->

## 다음 입력 상태가 어디서 오는가

<figure><img src="/assets/courses/surrogate-models/week-03/evaluation-flow-ko.svg" alt="One-step은 기준 상태를, rollout은 앞선 예측 상태를 입력으로 쓴다" /></figure>

두 그림은 같은 고정된 상태전이 모델을 사용합니다.

<!-- lecture-page -->

## Rollout은 짧고 명확한 반복문이다

초기 상태와 미래 입력 구간 150개가 주어졌을 때 아래 반복문으로 예측합니다.

```python
pred = np.empty((len(controls) + 1, 3))
pred[0] = initial_state
for k, control in enumerate(controls):
    pred[k + 1] = dynamic_step(
        model, scaling, pred[k:k+1], control[None, :]
    )[0]
```

초기화 후에는 기준 상태를 반복문에 넣지 않고 예측 상태 150개를 평가합니다.

<!-- lecture-page -->

## 한 단계의 오차는 어떻게 이어질까?

e_k = ĉ_k − c_k로 정의하고, 기준 상태에서 계산한 예측값을 더했다 빼봅니다.

<math display="block"><mtable columnalign="left"><mtr><mtd><mrow><msub><mi>e</mi><mrow><mi>k</mi><mo>+</mo><mn>1</mn></mrow></msub><mo>=</mo><msub><mi>f</mi><mrow><mi>θ</mi></mrow></msub><mrow><mo>(</mo><msub><mover><mi>c</mi><mo>^</mo></mover><mrow><mi>k</mi></mrow></msub><mo>,</mo><msub><mi>u</mi><mrow><mi>k</mi></mrow></msub><mo>)</mo></mrow><mo>−</mo><msub><mi>f</mi><mrow><mi>θ</mi></mrow></msub><mrow><mo>(</mo><msub><mi>c</mi><mrow><mi>k</mi></mrow></msub><mo>,</mo><msub><mi>u</mi><mrow><mi>k</mi></mrow></msub><mo>)</mo></mrow><mo>+</mo><msub><mi>δ</mi><mrow><mi>k</mi></mrow></msub></mrow></mtd></mtr><mtr><mtd><mrow><msub><mi>δ</mi><mrow><mi>k</mi></mrow></msub><mo>=</mo><msub><mi>f</mi><mrow><mi>θ</mi></mrow></msub><mrow><mo>(</mo><msub><mi>c</mi><mrow><mi>k</mi></mrow></msub><mo>,</mo><msub><mi>u</mi><mrow><mi>k</mi></mrow></msub><mo>)</mo></mrow><mo>−</mo><msub><mi>F</mi><mrow><mi>Δt</mi></mrow></msub><mrow><mo>(</mo><msub><mi>c</mi><mrow><mi>k</mi></mrow></msub><mo>,</mo><msub><mi>u</mi><mrow><mi>k</mi></mrow></msub><mo>)</mo></mrow></mrow></mtd></mtr></mtable></math>

첫 번째 차이는 기존 상태 오차가 학습된 관계식을 거쳐 전달되는 부분입니다. δ_k는 기준 상태에서의 한 단계 예측 오차로, 작더라도 매번 다음 예측에 더해집니다.

<!-- lecture-page -->

## 작은 one-step 오차도 쌓일 수 있다

한 변수 예제에서 기준 관계식을 F(c) = 0.9c, 학습 모델을 f(c) = 0.9c + 0.001로 두고 e₀ = 0에서 시작합니다.

<math display="block"><mtable columnalign="left"><mtr><mtd><mrow><msub><mi>e</mi><mrow><mi>h</mi><mo>+</mo><mn>1</mn></mrow></msub><mo>=</mo><mn>0.9</mn><msub><mi>e</mi><mrow><mi>h</mi></mrow></msub><mo>+</mo><mn>0.001</mn></mrow></mtd></mtr><mtr><mtd><mrow><msub><mi>e</mi><mrow><mi>h</mi></mrow></msub><mo>=</mo><mn>0.001</mn><mfrac><mrow><mn>1</mn><mo>−</mo><msup><mn>0.9</mn><mrow><mi>h</mi></mrow></msup></mrow><mrow><mn>1</mn><mo>−</mo><mn>0.9</mn></mrow></mfrac></mrow></mtd></mtr></mtable></math>

One-step bias는 0.001이지만 10번 반복한 오차는 약 0.00651입니다. 수축하는 관계식에서는 누적이 제한되며, 상태 민감도가 달라지면 예측 거리에 따른 오차도 달라집니다.

<!-- lecture-page -->

## 상태에 대한 민감도도 중요하다

<figure><img src="/assets/courses/surrogate-models/week-03/error-recurrence.png" alt="민감도 0.9, 1, 1.02에서의 오차 전달" /></figure>

그림은 한 변수 예제의 계산 결과입니다. 실제 rollout 오차는 증가하거나 완만해지거나 부호가 바뀔 수 있습니다.

<!-- lecture-page -->

## 주어진 두 온도 계획

| 조건 | 일정 온도 계획 | 온도 변경 계획 |
| --- | --- | --- |
| 초기 조성, mol/L | [1.2, 0, 0] | [1.2, 0, 0] |
| τ; C_Af | 5 min; 1.2 mol/L | 5 min; 1.2 mol/L |
| 0 ≤ t < 10 min | 330 K | 330 K |
| 10 ≤ t ≤ 30 min | 330 K | 345 K |

동일한 온도 계획에서 기준 궤적과 MLP rollout을 비교합니다. 두 곡선이 달라지기 시작하는 시점과 새 정상상태 응답에 접근하는 과정을 살펴봅니다.

<!-- lecture-page -->

## 전체 시간에 걸친 A·B·C 농도

<figure class="tall-figure"><img src="/assets/courses/surrogate-models/week-03/dynamic-rollout.png" alt="온도 계획과 세 성분 농도 궤적" /></figure>

<!-- lecture-page -->

## 물리 단위에서 오차 비교하기

| RMSE, mol/L | A | B | C |
| --- | --- | --- | --- |
| One-step | 0.001170 | 0.001288 | 0.001163 |
| Rollout | 0.009465 | 0.009629 | 0.010425 |

독립 test 궤적 20개에서 궤적당 예측 시각 150개를 평가한 결과입니다. 이번 실행에서는 rollout 오차가 더 큽니다. 예측 3000개의 성분별 RMSE를 계산하고 각 예측 거리의 오차도 따로 확인합니다.

<math display="block"><mtable columnalign="left"><mtr><mtd><mrow><msub><mi>RMSE</mi><mrow><mi>j</mi><mo>,</mo><mi>h</mi></mrow></msub><mo>=</mo><msqrt><mfrac><mrow><mn>1</mn></mrow><mrow><mi>N</mi></mrow></mfrac><msub><mo>∑</mo><mrow><mi>n</mi></mrow></msub><msup><mrow><mo>(</mo><msub><mover><mi>C</mi><mo>^</mo></mover><mrow><mi>n</mi><mo>,</mo><mi>h</mi><mo>,</mo><mi>j</mi></mrow></msub><mo>−</mo><msub><mi>C</mi><mrow><mi>n</mi><mo>,</mo><mi>h</mi><mo>,</mo><mi>j</mi></mrow></msub><mo>)</mo></mrow><mrow><mn>2</mn></mrow></msup></msqrt></mrow></mtd></mtr></mtable></math>

n은 test 궤적, h는 상태전이 횟수, j는 성분을 뜻합니다.

<!-- lecture-page -->

## Horizon에 따른 오차 읽기

<figure><img src="/assets/courses/surrogate-models/week-03/dynamic-errors.png" alt="Horizon별 성분 RMSE와 농도 합 residual" /></figure>

<!-- lecture-page -->

## 궤적을 따라 물리적 일관성 확인하기

<math display="block"><mtable columnalign="left"><mtr><mtd><mrow><mi>S</mi><mo>=</mo><msub><mi>C</mi><mrow><mi>A</mi></mrow></msub><mo>+</mo><msub><mi>C</mi><mrow><mi>B</mi></mrow></msub><mo>+</mo><msub><mi>C</mi><mrow><mi>C</mi></mrow></msub><mo>,</mo><mtext>  </mtext><mfrac><mrow><mi>d</mi><mi>S</mi></mrow><mrow><mi>d</mi><mi>t</mi></mrow></mfrac><mo>=</mo><mfrac><mrow><msub><mi>C</mi><mrow><mi>Af</mi></mrow></msub><mo>−</mo><mi>S</mi></mrow><mrow><mi>τ</mi></mrow></mfrac></mrow></mtd></mtr><mtr><mtd><mrow><msub><mi>S</mi><mrow><mi>k</mi><mo>+</mo><mn>1</mn></mrow></msub><mo>=</mo><msub><mi>C</mi><mrow><mi>Af</mi></mrow></msub><mo>+</mo><mrow><mo>(</mo><msub><mi>S</mi><mrow><mi>k</mi></mrow></msub><mo>−</mo><msub><mi>C</mi><mrow><mi>Af</mi></mrow></msub><mo>)</mo></mrow><msup><mi>e</mi><mrow><mo>−</mo><mi>Δt</mi><mo>/</mo><mi>τ</mi></mrow></msup></mrow></mtd></mtr></mtable></math>

S₀ = C_Af이고 유입 농도가 고정이면 기준 농도 합은 유입 농도와 같습니다. 학습 모델의 출력에는 이 관계가 자동으로 강제되지 않습니다.

| 진단, mol/L | One-step | Rollout |
| --- | --- | --- |
| 농도 합 residual RMSE | 0.000051 | 0.002014 |
| 최소 예측 농도 | -0.001152 | -0.005166 |

<!-- lecture-page -->

## 처음의 엔지니어 질문으로 돌아가기

| 30분 B 농도, mol/L | 기준 모델 | MLP rollout |
| --- | --- | --- |
| 일정 330 K | 0.400091 | 0.399819 |
| 10분에 330 → 345 K | 0.420021 | 0.411526 |

두 계산 모두 온도 변경 계획의 30분 B 농도가 더 높습니다. MLP는 그 최종 농도를 약 0.00850 mol/L 낮게 예측합니다. 전체 궤적에서는 정상상태 최종값만으로 알 수 없는 과도 구간을 확인합니다.

시간에 따라 적용되는 제품 규격을 확인할 때는 마지막 표본과 함께 해당 구간 전체를 살펴야 합니다.

<!-- lecture-page -->

## 실습 실행과 제출

[실습 묶음](/assets/courses/surrogate-models/week-03/week03-lab.zip)에서 기준 모델, 저장된 학습 모델, scaling, 그림과 [Notebook](/assets/courses/surrogate-models/week-03/week03_lab.ipynb)을 받습니다.

```bash
python -m pip install -r requirements.txt
python week03_lab.py --output-dir week03-results
# 선택: 같은 데이터 구성으로 다시 학습하기
python week03_lab.py --train --output-dir week03-retrained
```

상태·입력 정의, 데이터 분할·scaling, one-step·rollout RMSE, 예측 거리에 따른 오차 그림과 두 온도 계획의 궤적을 제출합니다.

<!-- lecture-page -->

## 연습문제와 직접 제공 읽기자료

1. dS/dt를 유도하고 S가 유입 농도와 같게 유지되는 조건을 적습니다.
2. 첫 0.2분 전이를 계산해 forward Euler와 비교합니다.
3. 두 평가에서 같은 MLP에 서로 다른 상태를 입력하는 이유를 설명합니다.
4. 입력 계획은 유지한 채 초기 상태를 바꿔 기준 궤적과 예측 궤적을 비교합니다.

[읽기자료](/courses/surrogate-models/week-03-reading/)에서 유도·계산 예·코드와 답을 확인합니다. 오차 전달식을 계산하고 multi-step 학습 목적함수는 선택 내용으로 다룹니다.

<!-- lecture-page -->

## 선택 확장: hidden state가 도움이 될 때

필수 예제는 세 농도 상태와 주어진 온도를 모두 입력으로 받습니다. 필요한 상태가 측정에서 빠져 있다면 과거 관측과 입력으로 그 상태를 추정하는 방법이 도움이 될 수 있습니다.

<math display="block"><mtable columnalign="left"><mtr><mtd><mrow><msub><mi>h</mi><mrow><mi>k</mi></mrow></msub><mo>=</mo><mi>φ</mi><mrow><mo>(</mo><msub><mi>W</mi><mrow><mi>x</mi></mrow></msub><msub><mi>x</mi><mrow><mi>k</mi></mrow></msub><mo>+</mo><msub><mi>W</mi><mrow><mi>h</mi></mrow></msub><msub><mi>h</mi><mrow><mi>k</mi><mo>−</mo><mn>1</mn></mrow></msub><mo>+</mo><mi>b</mi><mo>)</mo></mrow></mrow></mtd></mtr><mtr><mtd><mrow><msub><mover><mi>y</mi><mo>^</mo></mover><mrow><mi>k</mi></mrow></msub><mo>=</mo><msub><mi>W</mi><mrow><mi>y</mi></mrow></msub><msub><mi>h</mi><mrow><mi>k</mi></mrow></msub><mo>+</mo><msub><mi>b</mi><mrow><mi>y</mi></mrow></msub></mrow></mtd></mtr></mtable></math>

RNN은 학습된 은닉 상태를 갱신하고 LSTM은 gate를 사용한 메모리 갱신을 추가합니다. 비교할 때는 궤적 분할과 예측에 제공하는 미래 정보를 같게 둡니다.

구현은 PyTorch [RNN](https://docs.pytorch.org/docs/stable/generated/torch.nn.RNN.html)·[LSTM](https://docs.pytorch.org/docs/stable/generated/torch.nn.LSTM.html)을 참고합니다.

<!-- lecture-page -->

## 선택 확장: encoder와 궤적 decoder

Encoder는 과거 관측과 입력열을 상태 표현으로 요약합니다.

Decoder는 그 표현과 주어진 미래 입력 계획으로 미래 농도열을 예측합니다. 각 미래 입력이 해당 예측 단계에 전달되도록 구성합니다.

Sutskever·Vinyals·Le (2014)의 1-2절에서 sequence-to-sequence 아이디어를 읽습니다.

[논문 원문](https://proceedings.neurips.cc/paper_files/paper/2014/hash/5a18e133cbf9f257297f410bb7eca942-Abstract.html)을 참고하고, 추가 유도는 읽기자료에서 계산합니다.
