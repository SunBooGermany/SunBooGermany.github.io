---
layout: "course-resource"
title: "Week 4 Guided Lab: Correct a prediction and differentiate through the correction"
title_ko: "4주차 실습: 예측을 보정하고 보정식으로 역전파하기"
course_id: "surrogate-models"
permalink: "/courses/surrogate-models/week-04-practice/"
---

## Problem and setup

An MLP predicts three concentrations whose sum differs from the known feed. Compare ordinary training, a soft sum penalty, post-training projection, and training through a projection layer. The conserved sum is 1.2 mol/L in the hand example. Equality, nonnegativity, and individual steady-state balances are separate checks.

Extract the [lab ZIP](/assets/courses/surrogate-models/week-04/week04-lab.zip), keeping `requirements.txt`, the notebook, Python scripts, and supplied models together. These exercises were checked with Python 3.12. Use that folder as the working directory and run the commands below, or execute the [notebook](/assets/courses/surrogate-models/week-04/week04_lab.ipynb) cells in order. Downloading the notebook alone can omit required scripts or model files.

```text
python -m pip install -r requirements.txt
python guided_lab.py
```

`guided_lab.py` executes the calculations below in order and checks key values with assertions. Files in `guided-results/` belong to your new run; compare them with the supplied reference results. For Jupyter, select a kernel from the same Python environment. For `ModuleNotFoundError`, check that requirements were installed in that environment. For missing local files, check the working directory.


## 1. Spread the excess equally

The raw sum is 0.70+0.45+0.25=1.40, exceeding feed by 0.20. In physical Euclidean distance, the smallest total squared correction subtracts 0.20/3 from every component. The sum then loses exactly 0.20.

```python
from pathlib import Path
import numpy as np
import torch
import week04_lab as lab
raw = torch.tensor([[.70,.45,.25]], dtype=torch.float64, requires_grad=True)
feed = torch.tensor([[1.20]], dtype=torch.float64)
excess = raw.sum(-1, keepdim=True)-feed
corrected = lab.project(raw, feed)
print("sum excess, correction per component:", excess.item(), excess.item()/3)
print("projected:", corrected.detach().numpy())
np.testing.assert_allclose(corrected.detach(), [[19/30,23/60,11/60]])
np.testing.assert_allclose(corrected.detach().sum(1), [1.2])
```

The corrected vector is about [0.633333,0.383333,0.183333]. Equal physical corrections are generally unequal after dividing by different output scales, which is why project operates after conversion back to mol/L.

## 2. Trace one upstream gradient

The first corrected output is rawA−(rawA+rawB+rawC−feed)/3. Its derivatives with respect to raw A/B/C are 2/3,−1/3,−1/3. Increasing B makes the common correction larger and therefore reduces the corrected A.

```python
corrected[0,0].backward()
print("raw gradient:", raw.grad.numpy())
np.testing.assert_allclose(raw.grad, [[2/3,-1/3,-1/3]])
checks = lab.mathematical_checks()
print("projection checks:", checks)
```

The gradient sums to zero: a common increase in all raw components is removed by projection. mathematical_checks also tests multiple independent equality rows, the analytic Jacobian, scaling, and inconsistent constraints.

## 3. Find what equality does not control

Start from [0.02,0.90,0.50]. Its excess is 0.22, so subtracting 0.22/3 makes A negative. Clamping the negative component to zero adds mass without reducing another component. This is a concrete reason to inspect more than the sum residual.

```python
negative = lab.project(torch.tensor([[.02,.9,.5]], dtype=torch.float64), feed)
clamped = negative.clamp(min=0)
print("projected, minimum, clamped sum:", negative.tolist(), negative.min().item(), clamped.sum().item())
assert negative.min() < 0 and clamped.sum() > feed.item()
x = torch.tensor([[330.,5.,1.2]], dtype=torch.float64)
truth = lab.reference(x)
print("reference species balances:", lab.residuals(x, truth).tolist())
print("projected species balances:", lab.residuals(x, corrected.detach()).tolist())
```

A becomes −0.053333 mol/L and the clamped sum becomes 1.253333 mol/L. An exact sum alone also leaves individual reaction balances unconstrained. Compare all three residuals with the reference residuals near zero.

## 4. Run the controlled comparison

Keep the 900/300/300 split, initialization, batch order, and minimum-validation-MSE selection fixed. The soft loss adds lambda times squared sum error; post-projection changes an already trained model, whereas hard training backpropagates through project. Test metrics use physical units.

```python
report = lab.run(Path("guided-results"), epochs=600, seed=404)
for mode, metrics in report["test"].items():
    print(mode, "RMSE", metrics["rmse_all_mol_L"], "sum max", metrics["sum_max_mol_L"],
          "minimum", metrics["minimum_mol_L"], "species residual RMS", metrics["species_residual_rms_mol_L_min"])
assert report["protocol"]["rows"] == [900,300,300]
```

A method can improve the sum while leaving concentration error or species residuals. Explain each column before ranking methods; this single seed does not establish a general ranking. For a new lambda comparison use run(..., soft_lambda=value, evaluate_test=False), compare training["soft"]["validation_mse"], then evaluate test once after selection. Reconstruct one reported RMSE from saved rows as a follow-up.

## Result figure

After running, open `guided-results/comparison.png` and relate it to the errors computed above.

## What to report

Record the inputs, outputs, units and fixed conditions; your hand prediction; intermediate computed values; and final metrics with interpretation. Before changing one setting, predict the direction of its effect, then revise that explanation after execution. Record the environment and seed.

[Lecture](/courses/surrogate-models/week-04/) · [Derivations and sources](/courses/surrogate-models/week-04-reading/)

<!-- ko -->

## 문제와 실행 준비

MLP가 예측한 세 농도의 합이 알려진 유입 농도와 다릅니다. 일반 학습, 합 오차 penalty, 학습 후 투영, 투영층을 포함한 학습을 비교합니다. 손계산의 보존량은 1.2 mol/L입니다. 합 등식, 비음수성, 개별 정상상태 물질수지를 각각 확인합니다.

[실습 ZIP](/assets/courses/surrogate-models/week-04/week04-lab.zip)을 풀고 `requirements.txt`, notebook, Python 파일과 제공 모델을 같은 폴더에 둡니다. Python 3.12에서 검증했습니다. 해당 폴더를 작업 디렉터리로 사용하며, 아래 명령 또는 [notebook](/assets/courses/surrogate-models/week-04/week04_lab.ipynb)의 셀을 위에서부터 실행합니다. Notebook만 따로 내려받으면 필요한 스크립트나 모델 파일이 빠질 수 있습니다.

```text
python -m pip install -r requirements.txt
python guided_lab.py
```

`guided_lab.py`는 아래 계산을 순서대로 실행하며 `assert`로 핵심 값을 검사합니다. `guided-results/`에 생성되는 결과는 이번 실행의 출력입니다. ZIP에 있던 기준 결과와 구별해서 비교하세요. Jupyter를 쓸 때는 같은 Python 환경의 kernel을 선택합니다. `ModuleNotFoundError`이면 그 환경에 requirements를 설치했는지, 파일을 찾지 못하면 작업 디렉터리가 압축을 푼 폴더인지 확인합니다.


## 1. 초과량을 세 성분에 나누기

원래 합은 0.70+0.45+0.25=1.40으로 유입보다 0.20 큽니다. 물리 단위의 유클리드 거리에서 수정량 제곱합을 최소화하려면 각 성분에서 0.20/3을 뺍니다. 그러면 합이 정확히 0.20 줄어듭니다.

```python
from pathlib import Path
import numpy as np
import torch
import week04_lab as lab
raw = torch.tensor([[.70,.45,.25]], dtype=torch.float64, requires_grad=True)
feed = torch.tensor([[1.20]], dtype=torch.float64)
excess = raw.sum(-1, keepdim=True)-feed
corrected = lab.project(raw, feed)
print("sum excess, correction per component:", excess.item(), excess.item()/3)
print("projected:", corrected.detach().numpy())
np.testing.assert_allclose(corrected.detach(), [[19/30,23/60,11/60]])
np.testing.assert_allclose(corrected.detach().sum(1), [1.2])
```

보정값은 약 [0.633333,0.383333,0.183333]입니다. 같은 물리 수정량도 성분별 scale로 나누면 달라지므로 project는 mol/L로 되돌린 뒤 적용합니다.

## 2. Upstream gradient 하나 따라가기

첫 보정 출력은 rawA−(rawA+rawB+rawC−feed)/3입니다. raw A/B/C에 대한 미분은 2/3,−1/3,−1/3입니다. B가 커지면 공통으로 빼는 양이 커져 보정된 A가 줄어듭니다.

```python
corrected[0,0].backward()
print("raw gradient:", raw.grad.numpy())
np.testing.assert_allclose(raw.grad, [[2/3,-1/3,-1/3]])
checks = lab.mathematical_checks()
print("projection checks:", checks)
```

Gradient 합은 0입니다. 세 raw 성분을 함께 늘리는 변화는 투영에서 제거됩니다. mathematical_checks는 여러 독립 등식, 해석 Jacobian, scaling, 서로 모순인 제약도 검사합니다.

## 3. 합만으로 정해지지 않는 값 확인하기

[0.02,0.90,0.50]의 합 초과량은 0.22입니다. 각 성분에서 0.22/3을 빼면 A가 음수가 됩니다. 음수를 0으로 clamp하면 다른 성분을 줄이지 않은 채 총량만 늘어납니다. 그래서 합 residual 이외의 지표도 봅니다.

```python
negative = lab.project(torch.tensor([[.02,.9,.5]], dtype=torch.float64), feed)
clamped = negative.clamp(min=0)
print("projected, minimum, clamped sum:", negative.tolist(), negative.min().item(), clamped.sum().item())
assert negative.min() < 0 and clamped.sum() > feed.item()
x = torch.tensor([[330.,5.,1.2]], dtype=torch.float64)
truth = lab.reference(x)
print("reference species balances:", lab.residuals(x, truth).tolist())
print("projected species balances:", lab.residuals(x, corrected.detach()).tolist())
```

A는 −0.053333 mol/L이고 clamp한 합은 1.253333 mol/L입니다. 합이 정확해도 개별 반응 물질수지가 정해지지는 않습니다. 성분 residual 세 개를 0에 가까운 기준 residual과 비교하세요.

## 4. 같은 조건으로 네 방법 비교하기

900/300/300 분할, 초기화, batch 순서, 최소 validation MSE 선택을 고정합니다. Soft loss는 합 오차 제곱에 lambda를 곱해 더합니다. 학습 후 투영은 완성 모델의 출력을 바꾸고 hard 학습은 project를 거쳐 역전파합니다. Test 지표는 물리 단위로 계산합니다.

```python
report = lab.run(Path("guided-results"), epochs=600, seed=404)
for mode, metrics in report["test"].items():
    print(mode, "RMSE", metrics["rmse_all_mol_L"], "sum max", metrics["sum_max_mol_L"],
          "minimum", metrics["minimum_mol_L"], "species residual RMS", metrics["species_residual_rms_mol_L_min"])
assert report["protocol"]["rows"] == [900,300,300]
```

합이 개선돼도 농도 오차나 성분 residual이 남을 수 있습니다. 각 열의 뜻부터 설명하고 방법을 비교하세요. Seed 하나로 일반적인 순위를 정하지 않습니다. Lambda를 새로 비교할 때 run(..., soft_lambda=value, evaluate_test=False)를 쓰고 training["soft"]["validation_mse"]로 고른 뒤 test를 한 번 평가합니다. 추가로 저장 행에서 보고된 RMSE 하나를 직접 재계산하세요.

## 결과 그림

실행 후 `guided-results/comparison.png`을 열고 위에서 계산한 오차와 연결해 해석하세요.

## 제출할 내용

입력·출력·단위와 고정 조건, 손으로 예측한 값, 코드로 얻은 중간값, 최종 지표와 해석을 기록합니다. 설정 하나를 바꾸기 전에 결과가 어느 방향으로 달라질지 적고 실행 후 설명을 수정하세요. 실행 환경과 seed도 남깁니다.

[강의](/courses/surrogate-models/week-04/) · [풀이와 출처](/courses/surrogate-models/week-04-reading/)
