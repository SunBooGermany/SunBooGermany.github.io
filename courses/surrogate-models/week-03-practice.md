---
layout: "course-resource"
title: "Week 3 Guided Lab: From one transition to a trajectory"
title_ko: "3주차 실습: 상태전이 하나에서 전체 궤적까지"
course_id: "surrogate-models"
permalink: "/courses/surrogate-models/week-03-practice/"
---

## Problem and setup

Predict 30 minutes of A/B/C concentrations under a prescribed temperature plan. The state is the three current concentrations; controls are temperature, residence time, and feed. Each interval is 0.2 min with constant controls. A transition MLP predicts concentration increments, which are added to the current state.

Extract the [lab ZIP](/assets/courses/surrogate-models/week-03/week03-lab.zip), keeping `requirements.txt`, the notebook, Python scripts, and supplied models together. These exercises were checked with Python 3.12. Use that folder as the working directory and run the commands below, or execute the [notebook](/assets/courses/surrogate-models/week-03/week03_lab.ipynb) cells in order. Downloading the notebook alone can omit required scripts or model files.

```text
python -m pip install -r requirements.txt
python guided_lab.py
```

`guided_lab.py` executes the calculations below in order and checks key values with assertions. Files in `guided-results/` belong to your new run; compare them with the supplied reference results. For Jupyter, select a kernel from the same Python environment. For `ModuleNotFoundError`, check that requirements were installed in that environment. For missing local files, check the working directory.


## 1. Compare a rate with a finite-time change

Start from [1.2,0,0] mol/L at 330 K and tau=5 min. The A rate is (1.2−1.2)/5−0.2×1.2=−0.24 mol/(L min); B gains 0.24 and C initially has rate zero. Euler multiplies these initial rates by 0.2 min. The reference integrates rates as concentrations change within the interval.

```python
from pathlib import Path
import numpy as np
import cstr_transition as cstr
from week03_lab import evaluate
initial = np.array([[1.2, 0., 0.]])
control = np.array([[330., 5., 1.2]])
rate = cstr.concentration_rate(initial, control)
euler = initial+.2*rate
exact = cstr.reference_step(initial, control)
print("initial rate:", rate[0], "Euler:", euler[0], "reference:", exact[0])
np.testing.assert_allclose(euler, [[1.152, .048, 0]])
np.testing.assert_allclose(exact[0,0], .6+.6*np.exp(-.4*.2))
np.testing.assert_allclose(exact.sum(1), [1.2])
```

The reference A concentration is about 1.153870 mol/L. Its equilibrium is 0.6 and its deviation decays by exp(−0.4×0.2). C becomes positive during the interval because B is produced before the interval ends. A rate has units per minute; an increment has units mol/L.

## 2. Inspect the first three transitions

Three input intervals require four state rows: the initial state and three successors. One-step evaluation repeatedly supplies the reference current state. Rollout supplies its own previous prediction after initialization. Keeping the weights and controls identical isolates this feedback difference.

```python
model, scaling = cstr.load_model(Path("."), "dynamic-model")
controls = np.tile(control[0], (3,1))
truth = cstr.simulate_trajectory(controls, initial[0])
one = cstr.dynamic_step(model, scaling, truth[:-1], controls)
roll = cstr.rollout(model, scaling, controls, initial[0])
for k in range(3):
    print("step", k+1, "reference input", truth[k], "rollout input", roll[k])
    print("next B: reference, one-step, rollout", truth[k+1,1], one[k,1], roll[k+1,1])
assert truth.shape == roll.shape == (4,3)
np.testing.assert_allclose(one[0], roll[1], atol=1e-7)
```

The first predicted step agrees within floating-point tolerance because the initial states match; batch and single-row matrix operations can round differently. Later predictions can differ because the input states differ even with identical weights. Do not replace roll[k] with truth[k] while claiming to measure rollout.

## 3. Evaluate complete held-out trajectories

Split entire trajectories, rather than adjacent rows from the same trajectory, to avoid sharing a process history between training and test. There are 60/15/20 trajectories with 150 intervals each. Exclude the supplied initial state from error averages: it was not predicted.

```python
metrics, trajectories, predictions = evaluate(Path("guided-results"))
truth_all = np.concatenate([item["states"][1:] for item in trajectories["test"]])
pred_all = np.concatenate([item[1:] for item in predictions])
manual = np.sqrt(np.mean((pred_all-truth_all)**2, axis=0))
np.testing.assert_allclose(manual, metrics["rollout"]["rmse_mol_L"])
print("one-step RMSE:", metrics["one_step"]["rmse_mol_L"])
print("rollout RMSE:", manual)
print("transition counts:", metrics["transition_counts"])
assert len(truth_all) == 3000
```

Read dynamic-rollout.png together with dynamic-errors.png. A small one-step error can feed into later states and accumulate during rollout. The two plots answer different questions: trajectory shape and error versus forecast distance. Also report sum residual and negative concentrations from the metrics.

## 4. Change the initial state, keep the future plan

Use [0.2,0.8,0.2] mol/L instead of pure A. This changes the transient while preserving total concentration. Keep the same 150-interval 330 K plan so that the effect comes from initial state, not a new control sequence.

```python
controls = np.tile([330.,5.,1.2], (150,1))
new_initial = np.array([.2,.8,.2])
changed_truth = cstr.simulate_trajectory(controls, new_initial)
changed_pred = cstr.rollout(model, scaling, controls, new_initial)
print("B at 0, 0.2, 30 min:", changed_truth[[0,1,-1],1])
print("changed-state metrics:", cstr.prediction_metrics(changed_truth[1:], changed_pred[1:], controls[:,2]))
np.testing.assert_allclose(changed_truth.sum(1), 1.2, atol=1e-12)
```

The reference initially has B above its 0.4 mol/L equilibrium, so B falls at first. Compare this with the original B=0 transient. Report states, controls, units, split rules, both protocols, and the changed-state result. RNN/LSTM comparisons are optional after this transition-model baseline.

## Result figure

After running, open `guided-results/dynamic-rollout.png` and relate it to the errors computed above.

## What to report

Record the inputs, outputs, units and fixed conditions; your hand prediction; intermediate computed values; and final metrics with interpretation. Before changing one setting, predict the direction of its effect, then revise that explanation after execution. Record the environment and seed.

[Lecture](/courses/surrogate-models/week-03/) · [Derivations and sources](/courses/surrogate-models/week-03-reading/)

<!-- ko -->

## 문제와 실행 준비

주어진 온도 계획에서 30분 동안의 A/B/C 농도를 예측합니다. 상태는 현재 농도 세 개이고 입력은 온도·체류시간·유입 농도입니다. 각 0.2분 구간에서는 입력이 일정합니다. 상태전이 MLP가 예측한 농도 변화량을 현재 상태에 더해 다음 상태를 만듭니다.

[실습 ZIP](/assets/courses/surrogate-models/week-03/week03-lab.zip)을 풀고 `requirements.txt`, notebook, Python 파일과 제공 모델을 같은 폴더에 둡니다. Python 3.12에서 검증했습니다. 해당 폴더를 작업 디렉터리로 사용하며, 아래 명령 또는 [notebook](/assets/courses/surrogate-models/week-03/week03_lab.ipynb)의 셀을 위에서부터 실행합니다. Notebook만 따로 내려받으면 필요한 스크립트나 모델 파일이 빠질 수 있습니다.

```text
python -m pip install -r requirements.txt
python guided_lab.py
```

`guided_lab.py`는 아래 계산을 순서대로 실행하며 `assert`로 핵심 값을 검사합니다. `guided-results/`에 생성되는 결과는 이번 실행의 출력입니다. ZIP에 있던 기준 결과와 구별해서 비교하세요. Jupyter를 쓸 때는 같은 Python 환경의 kernel을 선택합니다. `ModuleNotFoundError`이면 그 환경에 requirements를 설치했는지, 파일을 찾지 못하면 작업 디렉터리가 압축을 푼 폴더인지 확인합니다.


## 1. 변화율과 유한 시간 변화량 비교하기

330 K, tau=5분에서 [1.2,0,0] mol/L로 시작합니다. A 변화율은 (1.2−1.2)/5−0.2×1.2=−0.24 mol/(L min)이고 B는 0.24만큼 늘며 C의 초기 변화율은 0입니다. Euler는 이 초기 변화율에 0.2분을 곱합니다. 기준 계산은 구간 중 농도가 변하면서 변화율도 달라지는 과정을 반영합니다.

```python
from pathlib import Path
import numpy as np
import cstr_transition as cstr
from week03_lab import evaluate
initial = np.array([[1.2, 0., 0.]])
control = np.array([[330., 5., 1.2]])
rate = cstr.concentration_rate(initial, control)
euler = initial+.2*rate
exact = cstr.reference_step(initial, control)
print("initial rate:", rate[0], "Euler:", euler[0], "reference:", exact[0])
np.testing.assert_allclose(euler, [[1.152, .048, 0]])
np.testing.assert_allclose(exact[0,0], .6+.6*np.exp(-.4*.2))
np.testing.assert_allclose(exact.sum(1), [1.2])
```

기준 A 농도는 약 1.153870 mol/L입니다. 평형값 0.6에서의 편차가 exp(−0.4×0.2)배로 줄어듭니다. 구간이 끝나기 전에 B가 생성되므로 C도 양수가 됩니다. 변화율은 분당 값이고 변화량은 mol/L입니다.

## 2. 처음 세 상태전이 확인하기

입력 구간 세 개에는 초기 상태를 포함해 상태 네 행이 필요합니다. One-step에는 매번 기준 현재 상태를 넣습니다. Rollout에는 초기화 이후 직전 예측을 넣습니다. 가중치와 입력 계획을 같게 유지하면 이 되먹임 차이를 비교할 수 있습니다.

```python
model, scaling = cstr.load_model(Path("."), "dynamic-model")
controls = np.tile(control[0], (3,1))
truth = cstr.simulate_trajectory(controls, initial[0])
one = cstr.dynamic_step(model, scaling, truth[:-1], controls)
roll = cstr.rollout(model, scaling, controls, initial[0])
for k in range(3):
    print("step", k+1, "reference input", truth[k], "rollout input", roll[k])
    print("next B: reference, one-step, rollout", truth[k+1,1], one[k,1], roll[k+1,1])
assert truth.shape == roll.shape == (4,3)
np.testing.assert_allclose(one[0], roll[1], atol=1e-7)
```

첫 예측은 두 방식의 초기 상태가 같아 부동소수점 허용오차 안에서 일치합니다. Batch와 한 행의 행렬 연산은 반올림이 조금 다를 수 있습니다. 이후에는 입력 상태가 달라져 같은 가중치로도 다른 예측이 나옵니다. Rollout을 측정할 때 roll[k]를 truth[k]로 교체하면 안 됩니다.

## 3. 독립 궤적 전체 평가하기

인접 행을 나누는 대신 궤적 전체를 train·validation·test로 나눠 같은 공정 이력이 양쪽에 섞이지 않게 합니다. 궤적은 60/15/20개이고 각 150구간입니다. 주어진 초기 상태는 예측값이 아니므로 오차 평균에서 제외합니다.

```python
metrics, trajectories, predictions = evaluate(Path("guided-results"))
truth_all = np.concatenate([item["states"][1:] for item in trajectories["test"]])
pred_all = np.concatenate([item[1:] for item in predictions])
manual = np.sqrt(np.mean((pred_all-truth_all)**2, axis=0))
np.testing.assert_allclose(manual, metrics["rollout"]["rmse_mol_L"])
print("one-step RMSE:", metrics["one_step"]["rmse_mol_L"])
print("rollout RMSE:", manual)
print("transition counts:", metrics["transition_counts"])
assert len(truth_all) == 3000
```

dynamic-rollout.png와 dynamic-errors.png를 함께 읽습니다. 작은 한 단계 오차도 다음 상태에 들어가며 누적될 수 있습니다. 두 그림은 각각 궤적 모양과 예측 거리별 오차를 보여줍니다. 지표에서 농도 합 residual과 음수 농도도 확인하세요.

## 4. 미래 입력을 고정하고 초기 상태 바꾸기

순수 A 대신 [0.2,0.8,0.2] mol/L를 사용합니다. 농도 합은 같고 과도응답이 바뀝니다. 150구간의 330 K 계획은 그대로 두어 초기 상태의 영향만 비교합니다.

```python
controls = np.tile([330.,5.,1.2], (150,1))
new_initial = np.array([.2,.8,.2])
changed_truth = cstr.simulate_trajectory(controls, new_initial)
changed_pred = cstr.rollout(model, scaling, controls, new_initial)
print("B at 0, 0.2, 30 min:", changed_truth[[0,1,-1],1])
print("changed-state metrics:", cstr.prediction_metrics(changed_truth[1:], changed_pred[1:], controls[:,2]))
np.testing.assert_allclose(changed_truth.sum(1), 1.2, atol=1e-12)
```

기준 B의 초기 농도는 평형값 0.4 mol/L보다 높아 처음에는 감소합니다. B=0에서 시작한 경우와 비교하세요. 상태·입력·단위·분할 방식·두 평가 방식·초기 상태 변경 결과를 보고합니다. RNN/LSTM 비교는 이 상태전이 모델 이후의 선택 과제입니다.

## 결과 그림

실행 후 `guided-results/dynamic-rollout.png`을 열고 위에서 계산한 오차와 연결해 해석하세요.

## 제출할 내용

입력·출력·단위와 고정 조건, 손으로 예측한 값, 코드로 얻은 중간값, 최종 지표와 해석을 기록합니다. 설정 하나를 바꾸기 전에 결과가 어느 방향으로 달라질지 적고 실행 후 설명을 수정하세요. 실행 환경과 seed도 남깁니다.

[강의](/courses/surrogate-models/week-03/) · [풀이와 출처](/courses/surrogate-models/week-03-reading/)
