---
layout: "course-resource"
title: "Week 5 Guided Lab: Build and check a ReLU MILP"
title_ko: "5주차 실습: ReLU MILP를 만들고 대조하기"
course_id: "surrogate-models"
permalink: "/courses/surrogate-models/week-05-practice/"
---

## Problem and setup

At fixed T=330 K and feed=1.2 mol/L, choose residence time between 2 and 10 min. Require B≥0.40 and C≤0.25 mol/L and nonnegative outputs. With flow 1 L/min, minimizing residence time also minimizes reactor volume. Fit a piecewise-linear surrogate, then reproduce its exact ReLU mapping inside an MILP.

Extract the [lab ZIP](/assets/courses/surrogate-models/week-05/week05-lab.zip), keeping `requirements.txt`, the notebook, Python scripts, and supplied models together. These exercises were checked with Python 3.12. Use that folder as the working directory and run the commands below, or execute the [notebook](/assets/courses/surrogate-models/week-05/week05_lab.ipynb) cells in order. Downloading the notebook alone can omit required scripts or model files.

```text
python -m pip install -r requirements.txt
python guided_lab.py
```

`guided_lab.py` executes the calculations below in order and checks key values with assertions. Files in `guided-results/` belong to your new run; compare them with the supplied reference results. For Jupyter, select a kernel from the same Python environment. For `ModuleNotFoundError`, check that requirements were installed in that environment. For missing local files, check the working directory.


## 1. Follow scaling, hinges, and output contributions

Five reference knots at 2,4,6,8,10 min define linear interpolation. Scale tau by x=(tau−2)/8. Each hidden unit turns on after one threshold; its weight changes the output slope. At tau=5, only the first two hinges are active.

```python
from pathlib import Path
import numpy as np
from scipy.optimize import milp
import week05_lab as lab
net = lab.fit_network()
a,h,y = lab.forward(5., net)
contributions = h[:,None]*np.asarray(net["weights"])
print("scaled x:", (5-2)/8, "a:", a, "h:", h)
print("output bias:", net["bias"], "contributions by hidden unit:", contributions)
print("output:", y, "reference:", lab.reference(5.))
np.testing.assert_allclose(a, [.375,.125,-.125,-.375])
np.testing.assert_allclose(y, np.asarray(net["bias"])+contributions.sum(0))
np.testing.assert_allclose(y, (lab.reference(4.)+lab.reference(6.))/2)
```

The surrogate at 5 min is the midpoint of the 4- and 6-min outputs, about [0.606061,0.395022,0.198918]. The physical reference is [0.6,0.4,0.2]. This interpolation error remains even when an MILP represents the neural network exactly.

## 2. Read one matrix row as a constraint

Variables are [x,h0,h1,h2,h3,yA,yB,yC,z1,z2,z3]. The first row h0−x=0 encodes the always-active hinge. For threshold 0.25, preactivation a=x−0.25 lies in [−0.25,0.75]. Binary z selects inactive h=0 or active h=a through the two upper bounds and h≥a,h≥0.

```python
c, integrality, bounds, constraint = lab.formulate(net)
print("first row:", constraint.A[0], "row limits:", constraint.lb[0], constraint.ub[0])
print("binary positions:", np.flatnonzero(integrality))
fixed = lab.solve(net, fixed_tau=5., specifications=False)
v = fixed.x
print("fixed solution [x,h,y,z]:", v)
print("all row values:", constraint.A@v)
np.testing.assert_allclose(v[1:5], h, atol=1e-8)
np.testing.assert_allclose(v[5:8], y, atol=1e-8)
```

Binary positions are 8,9,10, and the fixed hidden values are [0.375,0.125,0,0]. Disable product specifications during a fixed-input equivalence test: tau=5 fails the surrogate B≥0.40 specification, but still has a valid forward evaluation.

## 3. Optimize, restore the objective constant, and recheck

The solver minimizes 8x; adding the omitted constant 2 gives residence time. Recompute outputs using forward at the returned tau and then the process reference. The first comparison checks implementation; the second checks the selected process condition.

```python
optimal = lab.solve(net)
tau = 2+8*optimal.x[0]
prediction = lab.forward(tau, net)[2]
truth = lab.reference(tau)
print("objective without constant:", optimal.fun, "tau:", tau)
print("surrogate:", prediction, "reference:", truth)
np.testing.assert_allclose(tau, 2+optimal.fun, atol=1e-8)
np.testing.assert_allclose(optimal.x[5:8], prediction, atol=1e-8)
np.testing.assert_allclose(tau, lab.enumerate_segments(net), atol=1e-8)
report = lab.run(Path("guided-results"))
```

The selected residence time is about 5.353846 min. B lies at the surrogate lower bound. Segment enumeration independently checks the one-dimensional optimum, and run also audits fixed inputs near activation boundaries. State whether the reference outputs meet every original specification.

## 4. Explain an infeasible result

Raise only the B lower bound to 0.41 and keep C≤0.25. B peaks at about 0.410256 at 8 min, but C there exceeds its limit. C increases across all knots and reaches 0.25 between 6 and 8 min. Interpolate that crossing first; then read the largest B allowed before it.

```python
values = lab.forward(lab.KNOTS, net)[2]
tau_cap = 6+2*(.25-values[2,2])/(values[3,2]-values[2,2])
max_allowed_b = lab.forward(tau_cap, net)[2][1]
print("B and C at knots:", values[:,1:])
print("C-limited maximum tau:",tau_cap,"maximum allowed B:",max_allowed_b)
assert np.all(np.diff(values[:,2]) > 0) and np.all(np.diff(values[:4,1]) > 0)
c, integer, bounds, con = lab.formulate(net)
bounds.lb[6] = .41
infeasible = milp(c, integrality=integer, bounds=bounds, constraints=con)
print("status:", infeasible.status, infeasible.message)
assert max_allowed_b < .41 and infeasible.status == 2
```

C restricts tau to at most 6.109859 min, where B is only 0.409155 mol/L. Thus both specifications cannot hold together for this frozen surrogate. Do not read result.x or report an operating point without a feasible solution. Submit the hand forward table, one decoded row, fixed-input comparison, selected point, reference check, and infeasibility argument.

## What to report

Record the inputs, outputs, units and fixed conditions; your hand prediction; intermediate computed values; and final metrics with interpretation. Before changing one setting, predict the direction of its effect, then revise that explanation after execution. Record the environment and seed.

[Lecture](/courses/surrogate-models/week-05/) · [Derivations and sources](/courses/surrogate-models/week-05-reading/)

<!-- ko -->

## 문제와 실행 준비

T=330 K, feed=1.2 mol/L에서 2~10분의 체류시간을 고릅니다. B≥0.40, C≤0.25 mol/L와 비음수 출력을 요구합니다. 유량이 1 L/min이므로 체류시간을 줄이면 반응기 부피도 줄어듭니다. 구간 선형 surrogate를 만들고 그 ReLU 계산을 MILP 안에 표현합니다.

[실습 ZIP](/assets/courses/surrogate-models/week-05/week05-lab.zip)을 풀고 `requirements.txt`, notebook, Python 파일과 제공 모델을 같은 폴더에 둡니다. Python 3.12에서 검증했습니다. 해당 폴더를 작업 디렉터리로 사용하며, 아래 명령 또는 [notebook](/assets/courses/surrogate-models/week-05/week05_lab.ipynb)의 셀을 위에서부터 실행합니다. Notebook만 따로 내려받으면 필요한 스크립트나 모델 파일이 빠질 수 있습니다.

```text
python -m pip install -r requirements.txt
python guided_lab.py
```

`guided_lab.py`는 아래 계산을 순서대로 실행하며 `assert`로 핵심 값을 검사합니다. `guided-results/`에 생성되는 결과는 이번 실행의 출력입니다. ZIP에 있던 기준 결과와 구별해서 비교하세요. Jupyter를 쓸 때는 같은 Python 환경의 kernel을 선택합니다. `ModuleNotFoundError`이면 그 환경에 requirements를 설치했는지, 파일을 찾지 못하면 작업 디렉터리가 압축을 푼 폴더인지 확인합니다.


## 1. Scaling·hinge·출력 기여량 따라가기

2,4,6,8,10분의 기준값 다섯 개 사이를 선형으로 잇습니다. x=(tau−2)/8로 scaling합니다. 각 은닉 뉴런은 문턱을 넘으면 켜지고 가중치만큼 출력 기울기를 바꿉니다. tau=5에서는 처음 두 hinge만 켜집니다.

```python
from pathlib import Path
import numpy as np
from scipy.optimize import milp
import week05_lab as lab
net = lab.fit_network()
a,h,y = lab.forward(5., net)
contributions = h[:,None]*np.asarray(net["weights"])
print("scaled x:", (5-2)/8, "a:", a, "h:", h)
print("output bias:", net["bias"], "contributions by hidden unit:", contributions)
print("output:", y, "reference:", lab.reference(5.))
np.testing.assert_allclose(a, [.375,.125,-.125,-.375])
np.testing.assert_allclose(y, np.asarray(net["bias"])+contributions.sum(0))
np.testing.assert_allclose(y, (lab.reference(4.)+lab.reference(6.))/2)
```

5분 예측은 4분과 6분 출력의 중간값인 약 [0.606061,0.395022,0.198918]입니다. 공정 기준값은 [0.6,0.4,0.2]입니다. MILP가 신경망을 정확히 표현해도 이 보간 오차는 남습니다.

## 2. 행렬 한 행을 제약으로 읽기

변수 순서는 [x,h0,h1,h2,h3,yA,yB,yC,z1,z2,z3]입니다. 첫 행 h0−x=0은 항상 활성인 hinge를 나타냅니다. 문턱 0.25인 뉴런의 a=x−0.25는 [−0.25,0.75] 안에 있습니다. 이진 z가 두 상한과 h≥a,h≥0을 이용해 비활성 h=0 또는 활성 h=a를 선택합니다.

```python
c, integrality, bounds, constraint = lab.formulate(net)
print("first row:", constraint.A[0], "row limits:", constraint.lb[0], constraint.ub[0])
print("binary positions:", np.flatnonzero(integrality))
fixed = lab.solve(net, fixed_tau=5., specifications=False)
v = fixed.x
print("fixed solution [x,h,y,z]:", v)
print("all row values:", constraint.A@v)
np.testing.assert_allclose(v[1:5], h, atol=1e-8)
np.testing.assert_allclose(v[5:8], y, atol=1e-8)
```

이진 변수 위치는 8,9,10이고 고정 hidden 값은 [0.375,0.125,0,0]입니다. 입력 고정 대조에서는 제품 규격을 끕니다. tau=5는 surrogate의 B≥0.40을 만족하지 않지만 forward 계산 자체는 유효합니다.

## 3. 최적화 후 목적함수 상수를 복원하고 재검증하기

Solver는 8x를 최소화하므로 생략한 상수 2를 더해야 체류시간이 됩니다. 반환된 tau에서 forward를 다시 계산하고 공정 기준식도 계산합니다. 첫 비교는 구현을, 두 번째는 선택한 공정 조건을 검사합니다.

```python
optimal = lab.solve(net)
tau = 2+8*optimal.x[0]
prediction = lab.forward(tau, net)[2]
truth = lab.reference(tau)
print("objective without constant:", optimal.fun, "tau:", tau)
print("surrogate:", prediction, "reference:", truth)
np.testing.assert_allclose(tau, 2+optimal.fun, atol=1e-8)
np.testing.assert_allclose(optimal.x[5:8], prediction, atol=1e-8)
np.testing.assert_allclose(tau, lab.enumerate_segments(net), atol=1e-8)
report = lab.run(Path("guided-results"))
```

선택한 체류시간은 약 5.353846분이며 surrogate B가 하한에 놓입니다. 구간별 계산이 1차원 최적해를 독립적으로 대조하고 run은 활성 경계 주변의 고정 입력도 검사합니다. 기준 출력이 원래 규격을 모두 만족하는지 적으세요.

## 4. Infeasible 결과 설명하기

B 하한만 0.41로 높이고 C≤0.25를 유지합니다. B는 8분에서 약 0.410256으로 최대이지만 그때 C가 상한을 넘습니다. C는 모든 knot에서 증가하고 6~8분 사이에 0.25가 됩니다. 먼저 이 교점을 보간한 뒤 그 이전에서 허용되는 최대 B를 읽습니다.

```python
values = lab.forward(lab.KNOTS, net)[2]
tau_cap = 6+2*(.25-values[2,2])/(values[3,2]-values[2,2])
max_allowed_b = lab.forward(tau_cap, net)[2][1]
print("B and C at knots:", values[:,1:])
print("C-limited maximum tau:",tau_cap,"maximum allowed B:",max_allowed_b)
assert np.all(np.diff(values[:,2]) > 0) and np.all(np.diff(values[:4,1]) > 0)
c, integer, bounds, con = lab.formulate(net)
bounds.lb[6] = .41
infeasible = milp(c, integrality=integer, bounds=bounds, constraints=con)
print("status:", infeasible.status, infeasible.message)
assert max_allowed_b < .41 and infeasible.status == 2
```

C 때문에 tau는 최대 6.109859분이고 그때 B는 0.409155 mol/L입니다. 따라서 이 고정 surrogate에서는 두 규격을 함께 만족할 수 없습니다. 가능해가 없으면 result.x를 읽거나 운전점을 보고하지 않습니다. 손계산 표, 해석한 행 하나, 고정 입력 비교, 선택점과 기준 재검증, infeasible 근거를 제출하세요.

## 제출할 내용

입력·출력·단위와 고정 조건, 손으로 예측한 값, 코드로 얻은 중간값, 최종 지표와 해석을 기록합니다. 설정 하나를 바꾸기 전에 결과가 어느 방향으로 달라질지 적고 실행 후 설명을 수정하세요. 실행 환경과 seed도 남깁니다.

[강의](/courses/surrogate-models/week-05/) · [풀이와 출처](/courses/surrogate-models/week-05-reading/)
