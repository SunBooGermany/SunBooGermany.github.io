---
layout: "course-resource"
title: "Week 2 Guided Lab: Follow an MLP update before training"
title_ko: "2주차 실습: MLP 학습 한 번을 따라가기"
course_id: "surrogate-models"
permalink: "/courses/surrogate-models/week-02-practice/"
---

## Problem and setup

Extend the reactor to consecutive first-order reactions A → B → C. Predict all three outlet concentrations from T, tau, and feed. Understand how the network generates a prediction, how an error becomes a gradient, and how scaling affects a full training run.

Extract the [lab ZIP](/assets/courses/surrogate-models/week-02/week02-labs.zip), keeping `requirements.txt`, the notebook, Python scripts, and supplied models together. These exercises were checked with Python 3.12. Use that folder as the working directory and run the commands below, or execute the [notebook](/assets/courses/surrogate-models/week-02/week02_steady.ipynb) cells in order. Downloading the notebook alone can omit required scripts or model files.

```text
python -m pip install -r requirements.txt
python guided_lab.py
```

`guided_lab.py` executes the calculations below in order and checks key values with assertions. Files in `guided-results/` belong to your new run; compare them with the supplied reference results. For Jupyter, select a kernel from the same Python environment. For `ModuleNotFoundError`, check that requirements were installed in that environment. For missing local files, check the working directory.


## 1. Build three reference labels

At 330 K, k1=0.2/min and k2=0.1/min. Solve A first, then B using the A production term, then C using B. This triangular dependency explains the order of the three assignment statements.

```python
from pathlib import Path
import numpy as np
import torch
import week02_lab as lab
xphysical = np.array([[330., 5., 1.2]])
ca = 1.2/(1+.2*5)
cb = .2*5*ca/(1+.1*5)
cc = .1*5*cb
print("CA, CB, CC:", ca, cb, cc)
np.testing.assert_allclose(lab.steady_state(xphysical), [[ca, cb, cc]])
np.testing.assert_allclose([ca, cb, cc], [.6, .4, .2])
```

The concentrations sum to 1.2 mol/L. The later output layer predicts all three together, so this equality is not automatically enforced by an ordinary MLP.

## 2. Inspect a tiny forward calculation

Use a two-neuron hidden layer to make each operation visible. The example input and target are dimensionless. Multiply the input by W1, apply ReLU, and combine hidden outputs with W2. ReLU sets negative preactivations to zero.

```python
x = torch.tensor([1., 0., -1.], dtype=torch.float64)
target = torch.tensor([0., 1., 0.], dtype=torch.float64)
w1 = torch.tensor([[1.,0.,0.],[0.,0.,1.]], dtype=torch.float64, requires_grad=True)
b1 = torch.zeros(2, dtype=torch.float64, requires_grad=True)
w2 = torch.tensor([[1.,0.],[0.,1.],[1.,1.]], dtype=torch.float64, requires_grad=True)
b2 = torch.zeros(3, dtype=torch.float64, requires_grad=True)
a = w1@x+b1
h = torch.relu(a)
prediction = w2@h+b2
error = prediction-target
loss = .5*(error**2).sum()
print("a, h, prediction, error, loss:", a.tolist(), h.tolist(), prediction.tolist(), error.tolist(), loss.item())
assert loss.item() == 1.5
```

a=[1,−1] becomes h=[1,0]. The prediction [1,0,1] minus target [0,1,0] gives [1,−1,1]. Half of 1+1+1 is loss 1.5. The second hidden unit contributes nothing on this input.

## 3. Trace the gradient and parameter update

For half squared error, the output derivative is the residual. Multiplying by W2 transpose gives the hidden derivative; the ReLU gate then removes the second component. The first hidden derivative is 2, so its weight gradient is 2 times x. Move opposite to the gradient with learning rate 0.1.

```python
loss.backward()
print("dW1:", w1.grad.tolist(), "db1:", b1.grad.tolist())
print("dW2:", w2.grad.tolist(), "db2:", b2.grad.tolist())
np.testing.assert_allclose(w1.grad, [[2,0,-2],[0,0,0]])
with torch.no_grad():
    for parameter in (w1,b1,w2,b2):
        parameter -= .1*parameter.grad
    after = w2@torch.relu(w1@x+b1)+b2
    after_loss = .5*((after-target)**2).sum()
print("updated prediction and loss:", after.tolist(), after_loss.item())
check = lab.backprop_example()
np.testing.assert_allclose(after.tolist(), check["prediction_after"])
assert after_loss.item() < loss.item()
```

The updated prediction is [0.26,0.14,0.26] and loss is 0.4374. This one-sample decrease checks the update direction; it does not establish test performance. In repeated training, gradients must be cleared before the next backward call, as fit_mlp does with optimizer.zero_grad().

## 4. Scale, train, and read the physical errors

The actual network is 3→32→32→3: (3×32+32)+(32×32+32)+(32×3+3)=1283 parameters. Inputs use declared bounds; output means and standard deviations come only from training rows. Validation chooses the saved epoch; test rows assess that fixed model.

```python
splits = lab.generate_steady_splits(seed=42)
tx, ty = splits["train"]
print("input scaled first row:", (tx[0]-(lab.LOWER+lab.UPPER)/2)/((lab.UPPER-lab.LOWER)/2))
print("output mean, scale:", ty.mean(0), ty.std(0))
assert sum(p.numel() for p in lab.make_model(3).parameters()) == 1283
report = lab.run_steady(Path("guided-results"), seed=42, epochs=1400)
model, scaling = lab.load_model(Path("guided-results"), "steady-model")
vx, truth = splits["test"]
pred = lab.predict(model, scaling, vx)
print("first three reference / prediction rows:", np.column_stack([truth[:3], pred[:3]]))
manual_rmse = np.sqrt(np.mean((pred-truth)**2, axis=0))
print("physical RMSE:", manual_rmse)
np.testing.assert_allclose(manual_rmse, report["scaled_output_model"]["rmse_mol_L"])
```

Compare A/B/C errors in mol/L, concentration-sum residual, and minimum concentration for scaled and unscaled outputs. The stored seed-42 run has scaled-model RMSE about [0.00528,0.00294,0.00442] mol/L; environment changes may change the last digits. Inspect steady-training.png: validation, rather than the last epoch, chooses the saved weights. Change one setting using validation and then perform a final independent evaluation. The script also saves an optional operating-point preview for later weeks.

## Result figure

After running, open `guided-results/steady-training.png` and relate it to the errors computed above.

## What to report

Record the inputs, outputs, units and fixed conditions; your hand prediction; intermediate computed values; and final metrics with interpretation. Before changing one setting, predict the direction of its effect, then revise that explanation after execution. Record the environment and seed.

[Lecture](/courses/surrogate-models/week-02/) · [Derivations and sources](/courses/surrogate-models/week-02-reading/)

## Optional dynamic preview

The bundle also includes `week02_dynamic.ipynb`, `guided_dynamic.py`, and `README-dynamic.md`. They follow the first transition, three-step feedback, full held-out trajectories, and a changed initial state using the supplied frozen dynamic model. This preview is separate from the Week 2 steady-state exercise.

<!-- ko -->

## 문제와 실행 준비

반응을 A → B → C의 1차 연속반응으로 늘립니다. T·tau·feed에서 세 출구 농도를 예측합니다. 신경망이 예측을 만드는 과정, 오차가 gradient로 전달되는 과정, scaling이 전체 학습에 미치는 영향을 확인합니다.

[실습 ZIP](/assets/courses/surrogate-models/week-02/week02-labs.zip)을 풀고 `requirements.txt`, notebook, Python 파일과 제공 모델을 같은 폴더에 둡니다. Python 3.12에서 검증했습니다. 해당 폴더를 작업 디렉터리로 사용하며, 아래 명령 또는 [notebook](/assets/courses/surrogate-models/week-02/week02_steady.ipynb)의 셀을 위에서부터 실행합니다. Notebook만 따로 내려받으면 필요한 스크립트나 모델 파일이 빠질 수 있습니다.

```text
python -m pip install -r requirements.txt
python guided_lab.py
```

`guided_lab.py`는 아래 계산을 순서대로 실행하며 `assert`로 핵심 값을 검사합니다. `guided-results/`에 생성되는 결과는 이번 실행의 출력입니다. ZIP에 있던 기준 결과와 구별해서 비교하세요. Jupyter를 쓸 때는 같은 Python 환경의 kernel을 선택합니다. `ModuleNotFoundError`이면 그 환경에 requirements를 설치했는지, 파일을 찾지 못하면 작업 디렉터리가 압축을 푼 폴더인지 확인합니다.


## 1. 기준 농도 세 개 만들기

330 K에서 k1=0.2/min, k2=0.1/min입니다. A를 먼저 구하고, 그 A로 B 생성량을 구한 뒤 B로 C를 구합니다. 이 의존 관계 때문에 대입문도 A, B, C 순서입니다.

```python
from pathlib import Path
import numpy as np
import torch
import week02_lab as lab
xphysical = np.array([[330., 5., 1.2]])
ca = 1.2/(1+.2*5)
cb = .2*5*ca/(1+.1*5)
cc = .1*5*cb
print("CA, CB, CC:", ca, cb, cc)
np.testing.assert_allclose(lab.steady_state(xphysical), [[ca, cb, cc]])
np.testing.assert_allclose([ca, cb, cc], [.6, .4, .2])
```

세 농도의 합은 1.2 mol/L입니다. 이후 출력층은 세 농도를 함께 예측하므로 일반 MLP가 이 등식을 자동으로 만족하지는 않습니다.

## 2. 작은 신경망의 forward 확인하기

계산이 보이도록 은닉 뉴런 두 개를 사용합니다. 이 예제의 입력과 target은 무차원입니다. W1을 곱하고 ReLU를 적용한 뒤 W2로 결합합니다. ReLU는 음수인 preactivation을 0으로 바꿉니다.

```python
x = torch.tensor([1., 0., -1.], dtype=torch.float64)
target = torch.tensor([0., 1., 0.], dtype=torch.float64)
w1 = torch.tensor([[1.,0.,0.],[0.,0.,1.]], dtype=torch.float64, requires_grad=True)
b1 = torch.zeros(2, dtype=torch.float64, requires_grad=True)
w2 = torch.tensor([[1.,0.],[0.,1.],[1.,1.]], dtype=torch.float64, requires_grad=True)
b2 = torch.zeros(3, dtype=torch.float64, requires_grad=True)
a = w1@x+b1
h = torch.relu(a)
prediction = w2@h+b2
error = prediction-target
loss = .5*(error**2).sum()
print("a, h, prediction, error, loss:", a.tolist(), h.tolist(), prediction.tolist(), error.tolist(), loss.item())
assert loss.item() == 1.5
```

a=[1,−1]은 h=[1,0]이 됩니다. 예측 [1,0,1]에서 target [0,1,0]을 빼면 [1,−1,1]입니다. 1+1+1의 절반이 loss 1.5입니다. 이 입력에서는 두 번째 은닉 뉴런이 출력에 기여하지 않습니다.

## 3. Gradient와 파라미터 갱신 추적하기

제곱 오차의 절반을 쓰면 출력 미분은 오차 벡터입니다. W2의 전치를 곱해 은닉층으로 전달한 뒤 ReLU의 비활성 성분을 0으로 만듭니다. 첫 은닉 미분이 2이므로 첫 가중치 행의 gradient는 2x입니다. 학습률 0.1로 gradient의 반대 방향으로 이동합니다.

```python
loss.backward()
print("dW1:", w1.grad.tolist(), "db1:", b1.grad.tolist())
print("dW2:", w2.grad.tolist(), "db2:", b2.grad.tolist())
np.testing.assert_allclose(w1.grad, [[2,0,-2],[0,0,0]])
with torch.no_grad():
    for parameter in (w1,b1,w2,b2):
        parameter -= .1*parameter.grad
    after = w2@torch.relu(w1@x+b1)+b2
    after_loss = .5*((after-target)**2).sum()
print("updated prediction and loss:", after.tolist(), after_loss.item())
check = lab.backprop_example()
np.testing.assert_allclose(after.tolist(), check["prediction_after"])
assert after_loss.item() < loss.item()
```

갱신 후 예측은 [0.26,0.14,0.26], loss는 0.4374입니다. 한 표본의 loss 감소로 갱신 방향을 확인할 수 있지만 test 성능은 따로 평가합니다. 반복 학습에서는 fit_mlp의 optimizer.zero_grad()처럼 다음 backward 전에 gradient를 지웁니다.

## 4. Scaling·학습·물리 단위 오차 읽기

실제 신경망은 3→32→32→3으로 파라미터가 (3×32+32)+(32×32+32)+(32×3+3)=1283개입니다. 입력은 선언한 영역으로, 출력은 train 평균·표준편차로 scaling합니다. Validation으로 저장할 epoch를 고른 뒤 고정 모델을 test로 평가합니다.

```python
splits = lab.generate_steady_splits(seed=42)
tx, ty = splits["train"]
print("input scaled first row:", (tx[0]-(lab.LOWER+lab.UPPER)/2)/((lab.UPPER-lab.LOWER)/2))
print("output mean, scale:", ty.mean(0), ty.std(0))
assert sum(p.numel() for p in lab.make_model(3).parameters()) == 1283
report = lab.run_steady(Path("guided-results"), seed=42, epochs=1400)
model, scaling = lab.load_model(Path("guided-results"), "steady-model")
vx, truth = splits["test"]
pred = lab.predict(model, scaling, vx)
print("first three reference / prediction rows:", np.column_stack([truth[:3], pred[:3]]))
manual_rmse = np.sqrt(np.mean((pred-truth)**2, axis=0))
print("physical RMSE:", manual_rmse)
np.testing.assert_allclose(manual_rmse, report["scaled_output_model"]["rmse_mol_L"])
```

출력 scaling 유무에 따라 성분별 mol/L 오차, 농도 합 residual, 최소 농도를 비교합니다. 저장된 seed=42 실행의 scaled RMSE는 약 [0.00528,0.00294,0.00442] mol/L이며 환경에 따라 마지막 자릿수는 달라질 수 있습니다. steady-training.png에서 마지막 epoch 대신 validation으로 저장 가중치를 고르는 과정을 읽으세요. 설정 하나를 validation으로 비교한 뒤 독립 평가를 합니다. 스크립트는 후반 주차에서 다룰 운전점 선택 그림도 저장합니다.

## 결과 그림

실행 후 `guided-results/steady-training.png`을 열고 위에서 계산한 오차와 연결해 해석하세요.

## 제출할 내용

입력·출력·단위와 고정 조건, 손으로 예측한 값, 코드로 얻은 중간값, 최종 지표와 해석을 기록합니다. 설정 하나를 바꾸기 전에 결과가 어느 방향으로 달라질지 적고 실행 후 설명을 수정하세요. 실행 환경과 seed도 남깁니다.

[강의](/courses/surrogate-models/week-02/) · [풀이와 출처](/courses/surrogate-models/week-02-reading/)

## 선택 동적 미리보기

같은 묶음의 `week02_dynamic.ipynb`, `guided_dynamic.py`, `README-dynamic.md`는 제공된 고정 동적 모델로 첫 상태전이, 세 단계 되먹임, 독립 궤적 전체, 초기 상태 변경을 따라갑니다. 2주차 정상상태 실습과 별개인 선택 미리보기입니다.
