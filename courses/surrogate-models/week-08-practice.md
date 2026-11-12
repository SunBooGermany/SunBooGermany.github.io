---
layout: "course-resource"
title: "Week 8 Guided Lab: Decide only after reference revalidation"
title_ko: "8주차 실습: 기준식으로 재검증한 뒤 운전점 선택하기"
course_id: "surrogate-models"
permalink: "/courses/surrogate-models/week-08-practice/"
---

## Problem and setup

Use the Week 6 frozen reactor network on T∈[310,350] K and tau∈[2,10] min. Keep feed=1.2 mol/L and specifications B≥0.38, C≤0.25, and nonnegative concentrations. The assumed hourly cost is 12·tau+0.24·(T−310). Compare a feasible baseline, an unadjusted optimizer, calibration margins, local correction, and reference repair.

Extract the [lab ZIP](/assets/courses/surrogate-models/week-08/week08-lab.zip), keeping `requirements.txt`, the notebook, Python scripts, and supplied models together. These exercises were checked with Python 3.12. Use that folder as the working directory and run the commands below, or execute the [notebook](/assets/courses/surrogate-models/week-08/week08_lab.ipynb) cells in order. Downloading the notebook alone can omit required scripts or model files.

```text
python -m pip install -r requirements.txt
python guided_lab.py
```

`guided_lab.py` executes the calculations below in order and checks key values with assertions. Files in `guided-results/` belong to your new run; compare them with the supplied reference results. For Jupyter, select a kernel from the same Python environment. For `ModuleNotFoundError`, check that requirements were installed in that environment. For missing local files, check the working directory.


## 1. Check the baseline by hand

At 330 K and 6 min, k1=0.2 and k2=0.1 per minute. A=1.2/2.2; B=1.2·A/1.6; C=0.6·B. Test product shortfall max(0,0.38−B), byproduct excess max(0,C−0.25), negativity, and sum error. Cost is 72+4.8=76.8 dollars/hour under the stated teaching assumptions.

```python
from pathlib import Path
import json
import numpy as np
import week08_lab as lab
net = json.loads(Path("frozen_cstr_network.json").read_text())
baseline = lab.evaluate("baseline",[330.,6.],net)
print("baseline reference:",baseline["reference"])
print("residuals:",baseline["reference_residuals"],"cost:",baseline["cost"])
np.testing.assert_allclose(baseline["reference"],[.5454545454545,.4090909090909,.2454545454545])
np.testing.assert_allclose(baseline["cost"],76.8)
assert baseline["reference_feasible"]
```

All baseline residuals are zero up to floating-point tolerance. Retain this feasible comparison while assessing cheaper candidates; a low reported cost alone is not an acceptable operating decision.

## 2. Revalidate the optimizer at the same coordinates

Solve the surrogate model, then evaluate the reference at exactly the returned T and tau. Average held-out accuracy does not guarantee accuracy at a boundary selected by optimization. Keep prediction error signed so that overpredicted B can be linked directly to product shortfall.

```python
point, solver = lab.solve_candidate(net)
candidate = lab.evaluate("unadjusted",point,net,solver)
print("selected [T,tau]:",point)
print("prediction:",candidate["prediction"],"reference:",candidate["reference"])
print("signed error:",candidate["prediction_error"],"residuals:",candidate["reference_residuals"])
assert solver["has_incumbent"] and solver["forward_error"] < 1e-6
assert not candidate["reference_feasible"]
assert candidate["savings_vs_baseline"] is None
```

The unadjusted network meets its own product specification, while the reference B is about 0.371 mol/L and therefore below 0.38. Forward agreement verifies the formulation; the reference check rejects this operating candidate. Savings are left undefined for an infeasible candidate.

## 3. Calculate directional margins on calibration data

B is dangerous when predicted too high; C is dangerous when predicted too low. On a separate 31×31 calibration grid, take max(predB−refB,0) and max(refC−predC,0). Add the first margin to the B lower bound and subtract the second from the C upper bound.

```python
axis = np.linspace(0,1,31)
scaled = np.array(np.meshgrid(axis,axis)).reshape(2,-1).T
calibration = lab.OFFSET+lab.SCALE*scaled
error = lab.forward(calibration,net)-lab.reference(calibration)
b_margin = max(0.,float(error[:,1].max()))
c_margin = max(0.,float((-error[:,2]).max()))
print("calibration rows:",len(calibration),"B margin:",b_margin,"C margin:",c_margin)
print("new surrogate limits:",.38+b_margin,.25-c_margin)
np.testing.assert_allclose([b_margin,c_margin],[.02130093477436318,.01304798025717252],atol=1e-8)
margin_point, margin_solver = lab.solve_candidate(net,b_margin,c_margin)
margin_candidate = lab.evaluate("margin",margin_point,net,margin_solver)
print("margin reference residuals:",margin_candidate["reference_residuals"])
```

The adjusted surrogate limits are about B≥0.401301 and C≤0.236952 mol/L. These are sample maxima on 961 points, not uniform error guarantees between points. Revalidate the resulting candidate against the original 0.38/0.25 specifications.

## 4. See what nine local evaluations fit

Center a 3×3 grid at the failed decision using scaled offsets −0.06,0,0.06 and clip to the input box. Fit reference minus prediction as an affine correction in [1,scaled T,scaled tau]. A 9×3 design and 9×3 residual matrix produce 3×3 correction coefficients. The correction is optimized only within that local box.

```python
center = (point-lab.OFFSET)/lab.SCALE
axes = [np.clip(center[j]+np.array([-.06,0,.06]),0,1) for j in range(2)]
local_scaled = np.array(np.meshgrid(*axes)).reshape(2,-1).T
local = lab.OFFSET+lab.SCALE*local_scaled
design = np.column_stack([np.ones(len(local)),local_scaled])
residual = lab.reference(local)-lab.forward(local,net)
correction, _, rank, _ = np.linalg.lstsq(design,residual,rcond=None)
print("first three physical inputs:",local[:3])
print("first residual and fitted correction:",residual[0],design[0]@correction)
print("design shape, rank, coefficient shape:",design.shape,rank,correction.shape)
assert design.shape == (9,3) and correction.shape == (3,3) and rank == 3
report = lab.run(Path("guided-results"))
np.testing.assert_allclose(correction,report["local_update"]["coefficients"],atol=1e-8)
```

The affine fit minimizes local squared residuals; it does not force every residual to zero or certify feasibility. The full run keeps the failed local candidate, then performs a separate reference-model repair. Read targeted_data.csv to see which nine reference calls supported the update.

## 5. Compare only accepted candidates on cost

For each candidate read the reference residuals before cost savings. A residual tolerance of 1e−7 is used by evaluate. The reference benchmark uses a temperature scan and scalar refinement; it is a numerical comparison point without a certified global lower bound.

```python
for row in report["candidates"]:
    print(row["name"],"feasible",row["reference_feasible"],"cost",row["cost"],
          "residuals",row["reference_residuals"],"savings",row["savings_vs_baseline"])
accepted = [r for r in report["candidates"] if r["reference_feasible"]]
best = min(accepted,key=lambda r:r["cost"])
print("lowest cost among revalidated candidates:",best["name"],best["cost"])
assert all(r["savings_vs_baseline"] is None for r in report["candidates"] if not r["reference_feasible"])
assert not report["benchmark"]["global_certificate"]
```

Report feasibility, reference cost, and savings separately. The 997 held-out points estimate prediction accuracy; the 961 calibration points set margins; the nine targeted points fit the correction. Keep those roles separate when changing a margin or local width. Revalidate every new decision and explain a rejected candidate as carefully as an accepted one.

## What to report

Record the inputs, outputs, units and fixed conditions; your hand prediction; intermediate computed values; and final metrics with interpretation. Before changing one setting, predict the direction of its effect, then revise that explanation after execution. Record the environment and seed.

[Lecture](/courses/surrogate-models/week-08/) · [Derivations and sources](/courses/surrogate-models/week-08-reading/)

<!-- ko -->

## 문제와 실행 준비

6주차 고정 반응기 모델을 T∈[310,350] K, tau∈[2,10]분에서 사용합니다. Feed=1.2 mol/L와 B≥0.38, C≤0.25, 비음수 농도 규격을 유지합니다. 가정한 시간당 비용은 12·tau+0.24·(T−310)입니다. 기준 운전점, 보정 전 최적점, calibration margin, 국소 보정, 기준식 수정을 비교합니다.

[실습 ZIP](/assets/courses/surrogate-models/week-08/week08-lab.zip)을 풀고 `requirements.txt`, notebook, Python 파일과 제공 모델을 같은 폴더에 둡니다. Python 3.12에서 검증했습니다. 해당 폴더를 작업 디렉터리로 사용하며, 아래 명령 또는 [notebook](/assets/courses/surrogate-models/week-08/week08_lab.ipynb)의 셀을 위에서부터 실행합니다. Notebook만 따로 내려받으면 필요한 스크립트나 모델 파일이 빠질 수 있습니다.

```text
python -m pip install -r requirements.txt
python guided_lab.py
```

`guided_lab.py`는 아래 계산을 순서대로 실행하며 `assert`로 핵심 값을 검사합니다. `guided-results/`에 생성되는 결과는 이번 실행의 출력입니다. ZIP에 있던 기준 결과와 구별해서 비교하세요. Jupyter를 쓸 때는 같은 Python 환경의 kernel을 선택합니다. `ModuleNotFoundError`이면 그 환경에 requirements를 설치했는지, 파일을 찾지 못하면 작업 디렉터리가 압축을 푼 폴더인지 확인합니다.


## 1. 기준 운전점 손계산하기

330 K, 6분에서 k1=0.2/min, k2=0.1/min입니다. A=1.2/2.2, B=1.2·A/1.6, C=0.6·B입니다. 제품 부족량 max(0,0.38−B), 부산물 초과량 max(0,C−0.25), 음수 농도, 합 오차를 검사합니다. 가정한 교육용 비용은 72+4.8=76.8달러/시간입니다.

```python
from pathlib import Path
import json
import numpy as np
import week08_lab as lab
net = json.loads(Path("frozen_cstr_network.json").read_text())
baseline = lab.evaluate("baseline",[330.,6.],net)
print("baseline reference:",baseline["reference"])
print("residuals:",baseline["reference_residuals"],"cost:",baseline["cost"])
np.testing.assert_allclose(baseline["reference"],[.5454545454545,.4090909090909,.2454545454545])
np.testing.assert_allclose(baseline["cost"],76.8)
assert baseline["reference_feasible"]
```

기준 운전점 residual은 부동소수점 허용오차 안에서 0입니다. 더 싼 후보를 평가할 때 이 가능한 비교점을 유지합니다. 비용만 작다고 운전 조건으로 채택할 수는 없습니다.

## 2. 최적점의 같은 좌표에서 재검증하기

Surrogate를 최적화한 뒤 반환된 T와 tau 그대로 기준식을 계산합니다. 독립 데이터의 평균 정확도가 최적화가 선택한 경계점의 정확도를 보장하지는 않습니다. B 과대 예측을 제품 부족과 연결해 읽을 수 있도록 오차 부호를 유지합니다.

```python
point, solver = lab.solve_candidate(net)
candidate = lab.evaluate("unadjusted",point,net,solver)
print("selected [T,tau]:",point)
print("prediction:",candidate["prediction"],"reference:",candidate["reference"])
print("signed error:",candidate["prediction_error"],"residuals:",candidate["reference_residuals"])
assert solver["has_incumbent"] and solver["forward_error"] < 1e-6
assert not candidate["reference_feasible"]
assert candidate["savings_vs_baseline"] is None
```

보정 전 신경망은 자체 제품 규격을 만족하지만 기준 B는 약 0.371 mol/L로 0.38보다 작습니다. Forward 일치는 정식화를 확인하고 기준 재검증은 이 운전 후보를 기각합니다. 불가능한 후보의 절감액은 정의하지 않습니다.

## 3. Calibration 데이터로 방향별 margin 계산하기

B는 높게 예측하면, C는 낮게 예측하면 규격 위반을 놓칩니다. 별도 31×31 calibration 격자에서 max(predB−refB,0), max(refC−predC,0)을 구합니다. 첫 margin을 B 하한에 더하고 두 번째를 C 상한에서 뺍니다.

```python
axis = np.linspace(0,1,31)
scaled = np.array(np.meshgrid(axis,axis)).reshape(2,-1).T
calibration = lab.OFFSET+lab.SCALE*scaled
error = lab.forward(calibration,net)-lab.reference(calibration)
b_margin = max(0.,float(error[:,1].max()))
c_margin = max(0.,float((-error[:,2]).max()))
print("calibration rows:",len(calibration),"B margin:",b_margin,"C margin:",c_margin)
print("new surrogate limits:",.38+b_margin,.25-c_margin)
np.testing.assert_allclose([b_margin,c_margin],[.02130093477436318,.01304798025717252],atol=1e-8)
margin_point, margin_solver = lab.solve_candidate(net,b_margin,c_margin)
margin_candidate = lab.evaluate("margin",margin_point,net,margin_solver)
print("margin reference residuals:",margin_candidate["reference_residuals"])
```

조정한 surrogate 규격은 약 B≥0.401301, C≤0.236952 mol/L입니다. 이 값은 961점에서 본 최대 오차이며 점 사이의 균일 보장은 아닙니다. 새 후보도 원래 0.38/0.25 규격으로 재검증합니다.

## 4. 국소 기준값 아홉 개로 무엇을 맞추는지 보기

실패한 선택점의 scaling 좌표에서 −0.06,0,0.06만큼 이동한 3×3 격자를 만들고 입력 영역으로 자릅니다. 기준값−예측을 [1,scaled T,scaled tau]의 affine 보정식으로 맞춥니다. 9×3 설계행렬과 9×3 residual에서 3×3 보정 계수를 얻습니다. 보정 모델은 그 국소 영역에서만 최적화합니다.

```python
center = (point-lab.OFFSET)/lab.SCALE
axes = [np.clip(center[j]+np.array([-.06,0,.06]),0,1) for j in range(2)]
local_scaled = np.array(np.meshgrid(*axes)).reshape(2,-1).T
local = lab.OFFSET+lab.SCALE*local_scaled
design = np.column_stack([np.ones(len(local)),local_scaled])
residual = lab.reference(local)-lab.forward(local,net)
correction, _, rank, _ = np.linalg.lstsq(design,residual,rcond=None)
print("first three physical inputs:",local[:3])
print("first residual and fitted correction:",residual[0],design[0]@correction)
print("design shape, rank, coefficient shape:",design.shape,rank,correction.shape)
assert design.shape == (9,3) and correction.shape == (3,3) and rank == 3
report = lab.run(Path("guided-results"))
np.testing.assert_allclose(correction,report["local_update"]["coefficients"],atol=1e-8)
```

Affine 적합은 국소 residual 제곱합을 줄이며 모든 오차를 0으로 만들거나 가능성을 보장하지 않습니다. 전체 실행은 실패한 국소 후보도 남기고 별도로 기준식 수정을 수행합니다. targeted_data.csv에서 어떤 기준값 아홉 개가 보정에 쓰였는지 확인하세요.

## 5. 받아들인 후보의 비용 비교하기

후보마다 절감액보다 기준 residual을 먼저 읽습니다. evaluate의 residual 허용오차는 1e−7입니다. 기준 비교점은 온도 격자와 스칼라 정밀 탐색으로 구하며 전역 하한 인증을 가진 해는 아닙니다.

```python
for row in report["candidates"]:
    print(row["name"],"feasible",row["reference_feasible"],"cost",row["cost"],
          "residuals",row["reference_residuals"],"savings",row["savings_vs_baseline"])
accepted = [r for r in report["candidates"] if r["reference_feasible"]]
best = min(accepted,key=lambda r:r["cost"])
print("lowest cost among revalidated candidates:",best["name"],best["cost"])
assert all(r["savings_vs_baseline"] is None for r in report["candidates"] if not r["reference_feasible"])
assert not report["benchmark"]["global_certificate"]
```

가능성·기준 비용·절감액을 따로 보고합니다. 독립 997점은 예측 정확도를 평가하고 calibration 961점은 margin을 정하며 국소 아홉 점은 보정식을 맞춥니다. Margin이나 국소 폭을 바꿔도 데이터 역할을 섞지 마세요. 새 선택점을 모두 재검증하고 기각한 후보의 이유도 설명합니다.

## 제출할 내용

입력·출력·단위와 고정 조건, 손으로 예측한 값, 코드로 얻은 중간값, 최종 지표와 해석을 기록합니다. 설정 하나를 바꾸기 전에 결과가 어느 방향으로 달라질지 적고 실행 후 설명을 수정하세요. 실행 환경과 seed도 남깁니다.

[강의](/courses/surrogate-models/week-08/) · [풀이와 출처](/courses/surrogate-models/week-08-reading/)
