---
layout: course-note
title: "Week 3 Reading: State Transitions and Trajectories"
title_ko: "3주차 읽기자료: 상태전이와 궤적 예측"
description: "Balance derivations, interval solutions, evaluation code, error propagation, and worked exercises."
description_ko: "수지 유도, 구간 해, 평가 코드, 오차 전달식과 계산 연습을 제공합니다."
material_label: "Week 3 Reading"
material_label_ko: "3주차 읽기자료"
updated: "2026-10-09"
permalink: /courses/surrogate-models/week-03-reading/
pdf_en: /assets/courses/surrogate-models/week-03-reading-en.pdf
pdf_ko: /assets/courses/surrogate-models/week-03-reading-ko.pdf
course_id: surrogate-models
lecture_note: /courses/surrogate-models/week-03/
---

## Predict a trajectory from one starting point

The core task is to approximate F_Δt: current concentration and a held interval input → next concentration. Given c₀ and T₀,…,T₁₄₉, recursively compute 150 future states.

<math display="block"><mtable columnalign="left"><mtr><mtd><mrow><msub><mi>c</mi><mrow><mi>k</mi><mo>+</mo><mn>1</mn></mrow></msub><mo>=</mo><msub><mi>F</mi><mrow><mi>Δt</mi></mrow></msub><mrow><mo>(</mo><msub><mi>c</mi><mrow><mi>k</mi></mrow></msub><mo>,</mo><msub><mi>u</mi><mrow><mi>k</mi></mrow></msub><mo>;</mo><mi>q</mi><mo>)</mo></mrow></mrow></mtd></mtr></mtable></math>

Fix Δt = 0.2 min, τ and C_Af within each trajectory. T changes between intervals. The ideal mixed state contains all three species; thermal dynamics are omitted.

Work through the balances, interval solution, data construction, and two evaluation loops before the optional sequence models.

<!-- lecture-page -->

## Derive the concentration balances

For constant volume V and flow Q, τ = V/Q. Divide each species inventory balance by V. A enters at concentration C_Af and reacts into B; B reacts into C.

<math display="block"><mtable columnalign="left"><mtr><mtd><mrow><mfrac><mrow><mi>d</mi><msub><mi>C</mi><mrow><mi>A</mi></mrow></msub></mrow><mrow><mi>d</mi><mi>t</mi></mrow></mfrac><mo>=</mo><mfrac><mrow><msub><mi>C</mi><mrow><mi>Af</mi></mrow></msub><mo>−</mo><msub><mi>C</mi><mrow><mi>A</mi></mrow></msub></mrow><mrow><mi>τ</mi></mrow></mfrac><mo>−</mo><msub><mi>k</mi><mrow><mn>1</mn></mrow></msub><msub><mi>C</mi><mrow><mi>A</mi></mrow></msub></mrow></mtd></mtr><mtr><mtd><mrow><mfrac><mrow><mi>d</mi><msub><mi>C</mi><mrow><mi>B</mi></mrow></msub></mrow><mrow><mi>d</mi><mi>t</mi></mrow></mfrac><mo>=</mo><msub><mi>k</mi><mrow><mn>1</mn></mrow></msub><msub><mi>C</mi><mrow><mi>A</mi></mrow></msub><mo>−</mo><mfrac><mrow><msub><mi>C</mi><mrow><mi>B</mi></mrow></msub></mrow><mrow><mi>τ</mi></mrow></mfrac><mo>−</mo><msub><mi>k</mi><mrow><mn>2</mn></mrow></msub><msub><mi>C</mi><mrow><mi>B</mi></mrow></msub></mrow></mtd></mtr><mtr><mtd><mrow><mfrac><mrow><mi>d</mi><msub><mi>C</mi><mrow><mi>C</mi></mrow></msub></mrow><mrow><mi>d</mi><mi>t</mi></mrow></mfrac><mo>=</mo><msub><mi>k</mi><mrow><mn>2</mn></mrow></msub><msub><mi>C</mi><mrow><mi>B</mi></mrow></msub><mo>−</mo><mfrac><mrow><msub><mi>C</mi><mrow><mi>C</mi></mrow></msub></mrow><mrow><mi>τ</mi></mrow></mfrac></mrow></mtd></mtr></mtable></math>

Adding the three equations cancels both reaction terms, giving dS/dt = (C_Af − S)/τ. Therefore S(t) = C_Af + [S(0) − C_Af] exp(−t/τ) under fixed feed.

S(0) = C_Af gives a constant sum. An arbitrary initial sum instead relaxes toward feed.

<!-- lecture-page -->

## Derive the interval solution

<math display="block"><mtable columnalign="left"><mtr><mtd><mrow><mfrac><mrow><mi>d</mi><mi>c</mi></mrow><mrow><mi>d</mi><mi>t</mi></mrow></mfrac><mo>=</mo><mi>M</mi><mi>c</mi><mo>+</mo><mi>b</mi></mrow></mtd></mtr><mtr><mtd><mrow><mi>M</mi><mo>=</mo><mrow><mo>[</mo><mtable><mtr><mtd><mrow><mo>−</mo><mn>1</mn><mo>/</mo><mi>τ</mi><mo>−</mo><msub><mi>k</mi><mrow><mn>1</mn></mrow></msub></mrow></mtd><mtd><mrow><mn>0</mn></mrow></mtd><mtd><mrow><mn>0</mn></mrow></mtd></mtr><mtr><mtd><mrow><msub><mi>k</mi><mrow><mn>1</mn></mrow></msub></mrow></mtd><mtd><mrow><mo>−</mo><mn>1</mn><mo>/</mo><mi>τ</mi><mo>−</mo><msub><mi>k</mi><mrow><mn>2</mn></mrow></msub></mrow></mtd><mtd><mrow><mn>0</mn></mrow></mtd></mtr><mtr><mtd><mrow><mn>0</mn></mrow></mtd><mtd><mrow><msub><mi>k</mi><mrow><mn>2</mn></mrow></msub></mrow></mtd><mtd><mrow><mo>−</mo><mn>1</mn><mo>/</mo><mi>τ</mi></mrow></mtd></mtr></mtable><mo>]</mo></mrow><mo>,</mo><mtext>  </mtext><mi>b</mi><mo>=</mo><mrow><mo>[</mo><mtable><mtr><mtd><mrow><msub><mi>C</mi><mrow><mi>Af</mi></mrow></msub><mo>/</mo><mi>τ</mi></mrow></mtd></mtr><mtr><mtd><mrow><mn>0</mn></mrow></mtd></mtr><mtr><mtd><mrow><mn>0</mn></mrow></mtd></mtr></mtable><mo>]</mo></mrow></mrow></mtd></mtr></mtable></math>

Set z = c − c∗, where Mc∗ + b = 0. Then dz/dt = Mz. For fixed inputs within the interval, z(t+Δt) = exp(MΔt)z(t).

<math display="block"><mtable columnalign="left"><mtr><mtd><mrow><msub><mi>F</mi><mrow><mi>Δt</mi></mrow></msub><mrow><mo>(</mo><mi>c</mi><mo>,</mo><mi>u</mi><mo>;</mo><mi>q</mi><mo>)</mo></mrow><mo>=</mo><msup><mi>c</mi><mrow><mo>∗</mo></mrow></msup><mo>+</mo><msup><mi>e</mi><mrow><mi>M</mi><mi>Δt</mi></mrow></msup><mrow><mo>(</mo><mi>c</mi><mo>−</mo><msup><mi>c</mi><mrow><mo>∗</mo></mrow></msup><mo>)</mo></mrow></mrow></mtd></mtr></mtable></math>

This formula remains valid when T changes at a boundary: compute a new M and c∗ for the next interval, retaining the boundary state.

<!-- lecture-page -->

## A worked first transition

At 330 K, τ = 5 min and feed = 1.2 mol/L, a = 1/τ + k₁ = 0.4 and b = 1/τ + k₂ = 0.3 min⁻¹. The steady composition is c∗ = [0.6, 0.4, 0.2] mol/L. With Δt = 0.2 min and c₀ = [1.2, 0, 0]:

<math display="block"><mtable columnalign="left"><mtr><mtd><mrow><msub><msub><mi>C</mi><mrow><mi>A</mi></mrow></msub><mrow><mn>1</mn></mrow></msub><mo>=</mo><msup><msub><mi>C</mi><mrow><mi>A</mi></mrow></msub><mrow><mo>∗</mo></mrow></msup><mo>+</mo><mrow><mo>(</mo><msub><msub><mi>C</mi><mrow><mi>A</mi></mrow></msub><mrow><mn>0</mn></mrow></msub><mo>−</mo><msup><msub><mi>C</mi><mrow><mi>A</mi></mrow></msub><mrow><mo>∗</mo></mrow></msup><mo>)</mo></mrow><msup><mi>e</mi><mrow><mo>−</mo><mi>a</mi><mi>Δt</mi></mrow></msup></mrow></mtd></mtr><mtr><mtd><mrow><msub><msub><mi>C</mi><mrow><mi>B</mi></mrow></msub><mrow><mn>1</mn></mrow></msub><mo>=</mo><msup><msub><mi>C</mi><mrow><mi>B</mi></mrow></msub><mrow><mo>∗</mo></mrow></msup><mo>+</mo><mrow><mo>(</mo><msub><msub><mi>C</mi><mrow><mi>B</mi></mrow></msub><mrow><mn>0</mn></mrow></msub><mo>−</mo><msup><msub><mi>C</mi><mrow><mi>B</mi></mrow></msub><mrow><mo>∗</mo></mrow></msup><mo>)</mo></mrow><msup><mi>e</mi><mrow><mo>−</mo><mi>b</mi><mi>Δt</mi></mrow></msup><mo>+</mo><msub><mi>k</mi><mrow><mn>1</mn></mrow></msub><mrow><mo>(</mo><msub><msub><mi>C</mi><mrow><mi>A</mi></mrow></msub><mrow><mn>0</mn></mrow></msub><mo>−</mo><msup><msub><mi>C</mi><mrow><mi>A</mi></mrow></msub><mrow><mo>∗</mo></mrow></msup><mo>)</mo></mrow><mfrac><mrow><msup><mi>e</mi><mrow><mo>−</mo><mi>a</mi><mi>Δt</mi></mrow></msup><mo>−</mo><msup><mi>e</mi><mrow><mo>−</mo><mi>b</mi><mi>Δt</mi></mrow></msup></mrow><mrow><mi>b</mi><mo>−</mo><mi>a</mi></mrow></mfrac></mrow></mtd></mtr></mtable></math>

C_C,1 = S₁ − C_A,1 − C_B,1. This gives **[1.153870, 0.045672, 0.000458] mol/L**.

Forward Euler gives [1.152, 0.048, 0]. It differs because the rates change during the interval. When a = b, the fraction’s limit is Δt exp(−aΔt).

<!-- lecture-page -->

## Turn a trajectory into learning pairs

One trajectory has states of shape (151, 3) and controls of shape (150, 3). Split by trajectory, then stack its rows:

```python
inputs = np.column_stack((states[:-1], controls))
increments = states[1:] - states[:-1]
# inputs: (150, 6); increments: (150, 3)
x_mean = train_inputs.mean(axis=0)
x_scale = np.maximum(train_inputs.std(axis=0), 1e-8)
d_mean = train_increments.mean(axis=0)
d_scale = np.maximum(train_increments.std(axis=0), 1e-8)
```

The first input row contains c₀ and the first interval control. The last contains c₁₄₉ and the last control; its label is c₁₅₀. Test statistics do not enter scaling.

<!-- lecture-page -->

## Restore the increment and evaluate both loops

<math display="block"><mtable columnalign="left"><mtr><mtd><mrow><msub><mi>Δc</mi><mrow><mi>k</mi></mrow></msub><mo>=</mo><msub><mi>c</mi><mrow><mi>k</mi><mo>+</mo><mn>1</mn></mrow></msub><mo>−</mo><msub><mi>c</mi><mrow><mi>k</mi></mrow></msub></mrow></mtd></mtr><mtr><mtd><mrow><msub><mover><mi>c</mi><mo>^</mo></mover><mrow><mi>k</mi><mo>+</mo><mn>1</mn></mrow></msub><mo>=</mo><msub><mi>c</mi><mrow><mi>k</mi></mrow></msub><mo>+</mo><msub><mi>μ</mi><mrow><mi>Δ</mi></mrow></msub><mo>+</mo><msub><mi>s</mi><mrow><mi>Δ</mi></mrow></msub><mo>⊙</mo><msub><mi>g</mi><mrow><mi>θ</mi></mrow></msub><mrow><mo>(</mo><msub><mi>ṽ</mi><mrow><mi>k</mi></mrow></msub><mo>)</mo></mrow></mrow></mtd></mtr></mtable></math>

```python
# Reference current states at every step
one_step = dynamic_step(model, scaling,
                        states[:-1], controls)
# Only the initial state is supplied
recursive = rollout(model, scaling, controls, states[0])
err_one = one_step - states[1:]
err_roll = recursive[1:] - states[1:]
```

Restore Δc before adding it to c. Flatten all noninitial times across test trajectories for overall component RMSE; keep the horizon axis for RMSE_j,h. Both loops use the same future inputs.

<!-- lecture-page -->

## Derive the error recurrence

<math display="block"><mtable columnalign="left"><mtr><mtd><mrow><msub><mi>e</mi><mrow><mi>k</mi><mo>+</mo><mn>1</mn></mrow></msub><mo>=</mo><msub><mi>f</mi><mrow><mi>θ</mi></mrow></msub><mrow><mo>(</mo><msub><mover><mi>c</mi><mo>^</mo></mover><mrow><mi>k</mi></mrow></msub><mo>,</mo><msub><mi>u</mi><mrow><mi>k</mi></mrow></msub><mo>)</mo></mrow><mo>−</mo><msub><mi>f</mi><mrow><mi>θ</mi></mrow></msub><mrow><mo>(</mo><msub><mi>c</mi><mrow><mi>k</mi></mrow></msub><mo>,</mo><msub><mi>u</mi><mrow><mi>k</mi></mrow></msub><mo>)</mo></mrow><mo>+</mo><msub><mi>δ</mi><mrow><mi>k</mi></mrow></msub></mrow></mtd></mtr><mtr><mtd><mrow><msub><mi>δ</mi><mrow><mi>k</mi></mrow></msub><mo>=</mo><msub><mi>f</mi><mrow><mi>θ</mi></mrow></msub><mrow><mo>(</mo><msub><mi>c</mi><mrow><mi>k</mi></mrow></msub><mo>,</mo><msub><mi>u</mi><mrow><mi>k</mi></mrow></msub><mo>)</mo></mrow><mo>−</mo><msub><mi>F</mi><mrow><mi>Δt</mi></mrow></msub><mrow><mo>(</mo><msub><mi>c</mi><mrow><mi>k</mi></mrow></msub><mo>,</mo><msub><mi>u</mi><mrow><mi>k</mi></mrow></msub><mo>)</mo></mrow></mrow></mtd></mtr></mtable></math>

If the learned map is L_k-Lipschitz between c_k and ĉ_k, then:

<math display="block"><mtable columnalign="left"><mtr><mtd><mrow><mo>‖</mo><msub><mi>e</mi><mrow><mi>k</mi><mo>+</mo><mn>1</mn></mrow></msub><mo>‖</mo><mo>≤</mo><msub><mi>L</mi><mrow><mi>k</mi></mrow></msub><mo>‖</mo><msub><mi>e</mi><mrow><mi>k</mi></mrow></msub><mo>‖</mo><mo>+</mo><mo>‖</mo><msub><mi>δ</mi><mrow><mi>k</mi></mrow></msub><mo>‖</mo></mrow></mtd></mtr></mtable></math>

For constant L and local error bound ε, repeated substitution gives:

<math display="block"><mtable columnalign="left"><mtr><mtd><mrow><mo>‖</mo><msub><mi>e</mi><mrow><mi>h</mi></mrow></msub><mo>‖</mo><mo>≤</mo><msup><mi>L</mi><mrow><mi>h</mi></mrow></msup><mo>‖</mo><msub><mi>e</mi><mrow><mn>0</mn></mrow></msub><mo>‖</mo><mo>+</mo><mi>ε</mi><munderover><mo>∑</mo><mrow><mi>r</mi><mo>=</mo><mn>0</mn></mrow><mrow><mi>h</mi><mo>−</mo><mn>1</mn></mrow></munderover><msup><mi>L</mi><mrow><mi>r</mi></mrow></msup></mrow></mtd></mtr></mtable></math>

L < 1 limits this bound to ε/(1−L) when e₀ = 0; L = 1 gives hε. The sensitivity and error bounds must hold along the relevant states. Test RMSE alone is not that bound.

<!-- lecture-page -->

## Optional: train through several transitions

A multi-step loss begins at a reference state, then feeds predicted states forward for H steps and penalizes their trajectory error. Use component scaling consistently.

<math display="block"><mtable columnalign="left"><mtr><mtd><mrow><msub><mi>L</mi><mrow><mi>H</mi></mrow></msub><mo>=</mo><mfrac><mrow><mn>1</mn></mrow><mrow><mi>N</mi><mi>H</mi></mrow></mfrac><msub><mo>∑</mo><mrow><mi>n</mi></mrow></msub><msub><mo>∑</mo><mrow><mi>h</mi></mrow></msub><msup><mo>‖</mo><msub><mover><mi>c</mi><mo>^</mo></mover><mrow><mi>n</mi><mo>,</mo><mi>h</mi></mrow></msub><mo>−</mo><msub><mi>c</mi><mrow><mi>n</mi><mo>,</mo><mi>h</mi></mrow></msub><mo>‖</mo><mrow><mn>2</mn></mrow></msup></mrow></mtd></mtr></mtable></math>

Gradients pass through every unrolled transition. This can expose the model to its own states during training, but increases memory and may make training harder. Construct windows inside train trajectories only; choose H with validation trajectories.

The stored core experiment uses one-step training. A multi-step comparison is an extension to run, not an extra reported result.

<!-- lecture-page -->

## Exercises with short answer checks

1. **Why 151 states?** A 30 min horizon has 150 intervals of 0.2 min, plus its initial state.
2. **How many parameters?** 224 + 1056 + 99 = 1379.
3. **What if S₀ ≠ feed?** The reference sum evolves as feed + (S₀−feed)exp(−t/τ); a constant-sum check would be wrong.
4. **Error at h = 10 in the scalar example?** 0.001(1−0.9¹⁰)/0.1 ≈ 0.006513.
5. **Can we run the model at Δt = 1 min by changing a variable?** Its learned output still represents 0.2 min. Apply five steps or train a map for the new interval.
6. **What if a reference state is injected halfway through rollout?** That is a forecast reset; report the reset times and evaluate the resulting protocol separately.

<!-- lecture-page -->

## Optional sequence models and original sources

With incomplete observations, an RNN/LSTM hidden state can summarize available history. An encoder–decoder can convert observed history into a future sequence conditioned on the prescribed controls. Keep future measurements out of the encoder.

- Sutskever, Vinyals & Le (2014), [Sections 1–2](https://proceedings.neurips.cc/paper_files/paper/2014/hash/5a18e133cbf9f257297f410bb7eca942-Abstract.html): sequence encoding and decoding. Their model is for translation.
- PyTorch [RNN](https://docs.pytorch.org/docs/stable/generated/torch.nn.RNN.html) and [LSTM](https://docs.pytorch.org/docs/stable/generated/torch.nn.LSTM.html): recurrent updates, inputs, hidden states, and outputs.
- SciPy [matrix exponential](https://docs.scipy.org/doc/scipy/reference/generated/scipy.linalg.expm.html): an alternative implementation of exp(MΔt).

The CSTR derivations and worked exercises here are original course materials.

<!-- ko -->

## 한 시작점에서 궤적 예측하기

핵심 과제는 F_Δt를 근사하는 것이다. 현재 농도와 구간 동안 일정한 입력에서 다음 농도를 예측한다. c₀와 T₀,…,T₁₄₉가 주어지면 미래 상태 150개를 반복 계산한다.

<math display="block"><mtable columnalign="left"><mtr><mtd><mrow><msub><mi>c</mi><mrow><mi>k</mi><mo>+</mo><mn>1</mn></mrow></msub><mo>=</mo><msub><mi>F</mi><mrow><mi>Δt</mi></mrow></msub><mrow><mo>(</mo><msub><mi>c</mi><mrow><mi>k</mi></mrow></msub><mo>,</mo><msub><mi>u</mi><mrow><mi>k</mi></mrow></msub><mo>;</mo><mi>q</mi><mo>)</mo></mrow></mrow></mtd></mtr></mtable></math>

Δt = 0.2 min, 궤적 내 τ·C_Af는 고정한다. T는 구간 사이에서 바뀐다. 이상적 혼합 상태는 세 성분 농도를 모두 포함하며 열적 동특성은 생략한다.

수지·구간 해·데이터 구성·두 평가 반복문을 먼저 계산하고, sequence 모델은 선택 내용으로 읽는다.

<!-- lecture-page -->

## 농도 수지 유도

부피 V와 유량 Q가 일정하면 τ = V/Q다. 각 성분의 보유량 수지를 V로 나눈다. A가 C_Af로 들어오고 B로 반응하며, B는 C로 반응한다.

<math display="block"><mtable columnalign="left"><mtr><mtd><mrow><mfrac><mrow><mi>d</mi><msub><mi>C</mi><mrow><mi>A</mi></mrow></msub></mrow><mrow><mi>d</mi><mi>t</mi></mrow></mfrac><mo>=</mo><mfrac><mrow><msub><mi>C</mi><mrow><mi>Af</mi></mrow></msub><mo>−</mo><msub><mi>C</mi><mrow><mi>A</mi></mrow></msub></mrow><mrow><mi>τ</mi></mrow></mfrac><mo>−</mo><msub><mi>k</mi><mrow><mn>1</mn></mrow></msub><msub><mi>C</mi><mrow><mi>A</mi></mrow></msub></mrow></mtd></mtr><mtr><mtd><mrow><mfrac><mrow><mi>d</mi><msub><mi>C</mi><mrow><mi>B</mi></mrow></msub></mrow><mrow><mi>d</mi><mi>t</mi></mrow></mfrac><mo>=</mo><msub><mi>k</mi><mrow><mn>1</mn></mrow></msub><msub><mi>C</mi><mrow><mi>A</mi></mrow></msub><mo>−</mo><mfrac><mrow><msub><mi>C</mi><mrow><mi>B</mi></mrow></msub></mrow><mrow><mi>τ</mi></mrow></mfrac><mo>−</mo><msub><mi>k</mi><mrow><mn>2</mn></mrow></msub><msub><mi>C</mi><mrow><mi>B</mi></mrow></msub></mrow></mtd></mtr><mtr><mtd><mrow><mfrac><mrow><mi>d</mi><msub><mi>C</mi><mrow><mi>C</mi></mrow></msub></mrow><mrow><mi>d</mi><mi>t</mi></mrow></mfrac><mo>=</mo><msub><mi>k</mi><mrow><mn>2</mn></mrow></msub><msub><mi>C</mi><mrow><mi>B</mi></mrow></msub><mo>−</mo><mfrac><mrow><msub><mi>C</mi><mrow><mi>C</mi></mrow></msub></mrow><mrow><mi>τ</mi></mrow></mfrac></mrow></mtd></mtr></mtable></math>

세 식을 더하면 반응 항이 상쇄되어 dS/dt = (C_Af − S)/τ다. 유입 농도가 고정이면 S(t) = C_Af + [S(0) − C_Af] exp(−t/τ)다.

S(0) = C_Af이면 합이 일정하다. 초기 합이 다르면 유입 농도로 점차 다가간다.

<!-- lecture-page -->

## 구간 해 유도

<math display="block"><mtable columnalign="left"><mtr><mtd><mrow><mfrac><mrow><mi>d</mi><mi>c</mi></mrow><mrow><mi>d</mi><mi>t</mi></mrow></mfrac><mo>=</mo><mi>M</mi><mi>c</mi><mo>+</mo><mi>b</mi></mrow></mtd></mtr><mtr><mtd><mrow><mi>M</mi><mo>=</mo><mrow><mo>[</mo><mtable><mtr><mtd><mrow><mo>−</mo><mn>1</mn><mo>/</mo><mi>τ</mi><mo>−</mo><msub><mi>k</mi><mrow><mn>1</mn></mrow></msub></mrow></mtd><mtd><mrow><mn>0</mn></mrow></mtd><mtd><mrow><mn>0</mn></mrow></mtd></mtr><mtr><mtd><mrow><msub><mi>k</mi><mrow><mn>1</mn></mrow></msub></mrow></mtd><mtd><mrow><mo>−</mo><mn>1</mn><mo>/</mo><mi>τ</mi><mo>−</mo><msub><mi>k</mi><mrow><mn>2</mn></mrow></msub></mrow></mtd><mtd><mrow><mn>0</mn></mrow></mtd></mtr><mtr><mtd><mrow><mn>0</mn></mrow></mtd><mtd><mrow><msub><mi>k</mi><mrow><mn>2</mn></mrow></msub></mrow></mtd><mtd><mrow><mo>−</mo><mn>1</mn><mo>/</mo><mi>τ</mi></mrow></mtd></mtr></mtable><mo>]</mo></mrow><mo>,</mo><mtext>  </mtext><mi>b</mi><mo>=</mo><mrow><mo>[</mo><mtable><mtr><mtd><mrow><msub><mi>C</mi><mrow><mi>Af</mi></mrow></msub><mo>/</mo><mi>τ</mi></mrow></mtd></mtr><mtr><mtd><mrow><mn>0</mn></mrow></mtd></mtr><mtr><mtd><mrow><mn>0</mn></mrow></mtd></mtr></mtable><mo>]</mo></mrow></mrow></mtd></mtr></mtable></math>

Mc∗ + b = 0인 c∗를 이용해 z = c − c∗로 두면 dz/dt = Mz다. 구간 입력이 고정이면 z(t+Δt) = exp(MΔt)z(t)다.

<math display="block"><mtable columnalign="left"><mtr><mtd><mrow><msub><mi>F</mi><mrow><mi>Δt</mi></mrow></msub><mrow><mo>(</mo><mi>c</mi><mo>,</mo><mi>u</mi><mo>;</mo><mi>q</mi><mo>)</mo></mrow><mo>=</mo><msup><mi>c</mi><mrow><mo>∗</mo></mrow></msup><mo>+</mo><msup><mi>e</mi><mrow><mi>M</mi><mi>Δt</mi></mrow></msup><mrow><mo>(</mo><mi>c</mi><mo>−</mo><msup><mi>c</mi><mrow><mo>∗</mo></mrow></msup><mo>)</mo></mrow></mrow></mtd></mtr></mtable></math>

경계에서 T가 바뀌어도 같은 식을 쓸 수 있다. 경계 상태는 유지하고 다음 구간의 M과 c∗를 새로 계산한다.

<!-- lecture-page -->

## 첫 전이 손 계산

330 K, τ = 5 min, feed = 1.2 mol/L이면 a = 1/τ + k₁ = 0.4, b = 1/τ + k₂ = 0.3 min⁻¹다. 정상 조성은 c∗ = [0.6, 0.4, 0.2] mol/L다. Δt = 0.2 min, c₀ = [1.2, 0, 0]이면:

<math display="block"><mtable columnalign="left"><mtr><mtd><mrow><msub><msub><mi>C</mi><mrow><mi>A</mi></mrow></msub><mrow><mn>1</mn></mrow></msub><mo>=</mo><msup><msub><mi>C</mi><mrow><mi>A</mi></mrow></msub><mrow><mo>∗</mo></mrow></msup><mo>+</mo><mrow><mo>(</mo><msub><msub><mi>C</mi><mrow><mi>A</mi></mrow></msub><mrow><mn>0</mn></mrow></msub><mo>−</mo><msup><msub><mi>C</mi><mrow><mi>A</mi></mrow></msub><mrow><mo>∗</mo></mrow></msup><mo>)</mo></mrow><msup><mi>e</mi><mrow><mo>−</mo><mi>a</mi><mi>Δt</mi></mrow></msup></mrow></mtd></mtr><mtr><mtd><mrow><msub><msub><mi>C</mi><mrow><mi>B</mi></mrow></msub><mrow><mn>1</mn></mrow></msub><mo>=</mo><msup><msub><mi>C</mi><mrow><mi>B</mi></mrow></msub><mrow><mo>∗</mo></mrow></msup><mo>+</mo><mrow><mo>(</mo><msub><msub><mi>C</mi><mrow><mi>B</mi></mrow></msub><mrow><mn>0</mn></mrow></msub><mo>−</mo><msup><msub><mi>C</mi><mrow><mi>B</mi></mrow></msub><mrow><mo>∗</mo></mrow></msup><mo>)</mo></mrow><msup><mi>e</mi><mrow><mo>−</mo><mi>b</mi><mi>Δt</mi></mrow></msup><mo>+</mo><msub><mi>k</mi><mrow><mn>1</mn></mrow></msub><mrow><mo>(</mo><msub><msub><mi>C</mi><mrow><mi>A</mi></mrow></msub><mrow><mn>0</mn></mrow></msub><mo>−</mo><msup><msub><mi>C</mi><mrow><mi>A</mi></mrow></msub><mrow><mo>∗</mo></mrow></msup><mo>)</mo></mrow><mfrac><mrow><msup><mi>e</mi><mrow><mo>−</mo><mi>a</mi><mi>Δt</mi></mrow></msup><mo>−</mo><msup><mi>e</mi><mrow><mo>−</mo><mi>b</mi><mi>Δt</mi></mrow></msup></mrow><mrow><mi>b</mi><mo>−</mo><mi>a</mi></mrow></mfrac></mrow></mtd></mtr></mtable></math>

C_C,1 = S₁ − C_A,1 − C_B,1이므로 **[1.153870, 0.045672, 0.000458] mol/L**다.

Forward Euler는 [1.152, 0.048, 0]이다. 구간 안에서 반응속도가 바뀌므로 값이 다르다. a = b이면 분수의 극한은 Δt exp(−aΔt)다.

<!-- lecture-page -->

## 궤적을 학습 쌍으로 바꾸기

한 궤적의 states shape는 (151, 3), controls shape는 (150, 3)이다. 궤적별로 분할한 뒤 행을 쌓는다.

```python
inputs = np.column_stack((states[:-1], controls))
increments = states[1:] - states[:-1]
# inputs: (150, 6); increments: (150, 3)
x_mean = train_inputs.mean(axis=0)
x_scale = np.maximum(train_inputs.std(axis=0), 1e-8)
d_mean = train_increments.mean(axis=0)
d_scale = np.maximum(train_increments.std(axis=0), 1e-8)
```

첫 입력 행은 c₀와 첫 구간 입력이다. 마지막은 c₁₄₉와 마지막 입력이고 label은 c₁₅₀다. Scaling에 test 통계량은 들어가지 않는다.

<!-- lecture-page -->

## 변화량 복원과 두 평가 반복문

<math display="block"><mtable columnalign="left"><mtr><mtd><mrow><msub><mi>Δc</mi><mrow><mi>k</mi></mrow></msub><mo>=</mo><msub><mi>c</mi><mrow><mi>k</mi><mo>+</mo><mn>1</mn></mrow></msub><mo>−</mo><msub><mi>c</mi><mrow><mi>k</mi></mrow></msub></mrow></mtd></mtr><mtr><mtd><mrow><msub><mover><mi>c</mi><mo>^</mo></mover><mrow><mi>k</mi><mo>+</mo><mn>1</mn></mrow></msub><mo>=</mo><msub><mi>c</mi><mrow><mi>k</mi></mrow></msub><mo>+</mo><msub><mi>μ</mi><mrow><mi>Δ</mi></mrow></msub><mo>+</mo><msub><mi>s</mi><mrow><mi>Δ</mi></mrow></msub><mo>⊙</mo><msub><mi>g</mi><mrow><mi>θ</mi></mrow></msub><mrow><mo>(</mo><msub><mi>ṽ</mi><mrow><mi>k</mi></mrow></msub><mo>)</mo></mrow></mrow></mtd></mtr></mtable></math>

```python
# 매 단계 기준 현재 상태를 제공
one_step = dynamic_step(model, scaling,
                        states[:-1], controls)
# 초기 상태만 제공
recursive = rollout(model, scaling, controls, states[0])
err_one = one_step - states[1:]
err_roll = recursive[1:] - states[1:]
```

Δc를 복원한 뒤 c에 더한다. 전체 성분별 RMSE는 초기 상태를 뺀 모든 test 시각을 모아 계산한다. RMSE_j,h는 horizon 축을 유지해 계산한다. 두 반복문은 같은 미래 입력을 쓴다.

<!-- lecture-page -->

## 오차 전달식 유도

<math display="block"><mtable columnalign="left"><mtr><mtd><mrow><msub><mi>e</mi><mrow><mi>k</mi><mo>+</mo><mn>1</mn></mrow></msub><mo>=</mo><msub><mi>f</mi><mrow><mi>θ</mi></mrow></msub><mrow><mo>(</mo><msub><mover><mi>c</mi><mo>^</mo></mover><mrow><mi>k</mi></mrow></msub><mo>,</mo><msub><mi>u</mi><mrow><mi>k</mi></mrow></msub><mo>)</mo></mrow><mo>−</mo><msub><mi>f</mi><mrow><mi>θ</mi></mrow></msub><mrow><mo>(</mo><msub><mi>c</mi><mrow><mi>k</mi></mrow></msub><mo>,</mo><msub><mi>u</mi><mrow><mi>k</mi></mrow></msub><mo>)</mo></mrow><mo>+</mo><msub><mi>δ</mi><mrow><mi>k</mi></mrow></msub></mrow></mtd></mtr><mtr><mtd><mrow><msub><mi>δ</mi><mrow><mi>k</mi></mrow></msub><mo>=</mo><msub><mi>f</mi><mrow><mi>θ</mi></mrow></msub><mrow><mo>(</mo><msub><mi>c</mi><mrow><mi>k</mi></mrow></msub><mo>,</mo><msub><mi>u</mi><mrow><mi>k</mi></mrow></msub><mo>)</mo></mrow><mo>−</mo><msub><mi>F</mi><mrow><mi>Δt</mi></mrow></msub><mrow><mo>(</mo><msub><mi>c</mi><mrow><mi>k</mi></mrow></msub><mo>,</mo><msub><mi>u</mi><mrow><mi>k</mi></mrow></msub><mo>)</mo></mrow></mrow></mtd></mtr></mtable></math>

학습 mapping이 c_k와 ĉ_k 사이에서 L_k-Lipschitz이면:

<math display="block"><mtable columnalign="left"><mtr><mtd><mrow><mo>‖</mo><msub><mi>e</mi><mrow><mi>k</mi><mo>+</mo><mn>1</mn></mrow></msub><mo>‖</mo><mo>≤</mo><msub><mi>L</mi><mrow><mi>k</mi></mrow></msub><mo>‖</mo><msub><mi>e</mi><mrow><mi>k</mi></mrow></msub><mo>‖</mo><mo>+</mo><mo>‖</mo><msub><mi>δ</mi><mrow><mi>k</mi></mrow></msub><mo>‖</mo></mrow></mtd></mtr></mtable></math>

L과 한 단계 오차 상한 ε이 일정하면 반복 대입으로:

<math display="block"><mtable columnalign="left"><mtr><mtd><mrow><mo>‖</mo><msub><mi>e</mi><mrow><mi>h</mi></mrow></msub><mo>‖</mo><mo>≤</mo><msup><mi>L</mi><mrow><mi>h</mi></mrow></msup><mo>‖</mo><msub><mi>e</mi><mrow><mn>0</mn></mrow></msub><mo>‖</mo><mo>+</mo><mi>ε</mi><munderover><mo>∑</mo><mrow><mi>r</mi><mo>=</mo><mn>0</mn></mrow><mrow><mi>h</mi><mo>−</mo><mn>1</mn></mrow></munderover><msup><mi>L</mi><mrow><mi>r</mi></mrow></msup></mrow></mtd></mtr></mtable></math>

e₀ = 0일 때 L < 1이면 상한은 ε/(1−L) 이하이고, L = 1이면 hε다. 실제로 거치는 상태에서 유효한 민감도와 오차 상한이 필요하다. Test RMSE 자체가 그 상한은 아니다.

<!-- lecture-page -->

## 선택: 여러 전이를 거쳐 학습하기

Multi-step loss는 기준 상태에서 시작해 예측 상태를 H단계 반복 입력하고 궤적 오차를 벌점으로 준다. 성분 scaling을 일관되게 적용한다.

<math display="block"><mtable columnalign="left"><mtr><mtd><mrow><msub><mi>L</mi><mrow><mi>H</mi></mrow></msub><mo>=</mo><mfrac><mrow><mn>1</mn></mrow><mrow><mi>N</mi><mi>H</mi></mrow></mfrac><msub><mo>∑</mo><mrow><mi>n</mi></mrow></msub><msub><mo>∑</mo><mrow><mi>h</mi></mrow></msub><msup><mo>‖</mo><msub><mover><mi>c</mi><mo>^</mo></mover><mrow><mi>n</mi><mo>,</mo><mi>h</mi></mrow></msub><mo>−</mo><msub><mi>c</mi><mrow><mi>n</mi><mo>,</mo><mi>h</mi></mrow></msub><mo>‖</mo><mrow><mn>2</mn></mrow></msup></mrow></mtd></mtr></mtable></math>

Gradient는 펼친 각 전이를 거쳐 전달된다. 학습 중 모델 자신의 상태를 경험하게 할 수 있지만 메모리가 늘고 학습이 어려워질 수 있다. Train 궤적 안에서만 window를 만들고 H는 validation 궤적으로 선택한다.

저장된 핵심 실험은 one-step 학습이다. Multi-step 비교는 직접 실행할 확장 과제이며, 이미 얻은 실험 결과로 제시하지 않는다.

<!-- lecture-page -->

## 연습문제와 짧은 답 확인

1. **왜 상태가 151개인가?** 30분에는 0.2분 구간 150개와 초기 상태가 있다.
2. **파라미터 수는?** 224 + 1056 + 99 = 1379다.
3. **S₀가 feed와 다르면?** 기준 합은 feed + (S₀−feed)exp(−t/τ)로 변한다. 일정한 합을 검사하면 잘못된 진단이다.
4. **한 변수 예의 h = 10 오차는?** 0.001(1−0.9¹⁰)/0.1 ≈ 0.006513이다.
5. **변수만 바꾸어 Δt = 1분으로 실행할 수 있나?** 학습된 출력은 여전히 0.2분 변화량이다. 다섯 번 적용하거나 새 간격의 mapping을 학습한다.
6. **Rollout 중간에 기준 상태를 넣으면?** 예측을 다시 시작한 것이다. Reset 시각을 적고 그 평가 방식을 따로 보고한다.

<!-- lecture-page -->

## 선택 sequence 모델과 원문

관측이 불완전하면 RNN/LSTM hidden state로 가용한 과거 정보를 요약할 수 있다. Encoder–decoder는 관측 이력에서 미래 sequence를 만들되 주어진 미래 입력을 조건으로 사용한다. 미래 측정값을 encoder에 넣지 않는다.

- Sutskever·Vinyals·Le (2014), [1–2절](https://proceedings.neurips.cc/paper_files/paper/2014/hash/5a18e133cbf9f257297f410bb7eca942-Abstract.html): sequence encoding·decoding. 원 모델의 응용은 번역이다.
- PyTorch [RNN](https://docs.pytorch.org/docs/stable/generated/torch.nn.RNN.html)·[LSTM](https://docs.pytorch.org/docs/stable/generated/torch.nn.LSTM.html): 반복 갱신, 입력, hidden state와 출력.
- SciPy [matrix exponential](https://docs.scipy.org/doc/scipy/reference/generated/scipy.linalg.expm.html): exp(MΔt)의 다른 구현 방법.

CSTR 유도와 계산 연습은 이 과목을 위해 직접 작성했다.
