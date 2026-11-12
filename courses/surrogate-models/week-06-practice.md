---
layout: "course-resource"
title: "Week 6 Guided Lab: Explain bounds before comparing solvers"
title_ko: "6주차 실습: Bounds의 의미를 확인하고 정식화 비교하기"
course_id: "surrogate-models"
permalink: "/courses/surrogate-models/week-06-practice/"
---

## Problem and setup

Embed the same frozen 2→12→12→3 reactor network using manual constraints and OMLT. Inputs are T∈[310,350] K and tau∈[2,10] min; feed is fixed at 1.2 mol/L. Require B≥0.38, C≤0.25, and nonnegative outputs. Minimize tau+0.02(T−310). Investigate how valid bounds change the LP relaxation while preserving the network.

Extract the [lab ZIP](/assets/courses/surrogate-models/week-06/week06-lab.zip), keeping `requirements.txt`, the notebook, Python scripts, and supplied models together. These exercises were checked with Python 3.12. Use that folder as the working directory and run the commands below, or execute the [notebook](/assets/courses/surrogate-models/week-06/week06_lab.ipynb) cells in order. Downloading the notebook alone can omit required scripts or model files.

```text
python -m pip install -r requirements.txt
python guided_lab.py
```

`guided_lab.py` executes the calculations below in order and checks key values with assertions. Files in `guided-results/` belong to your new run; compare them with the supplied reference results. For Jupyter, select a kernel from the same Python environment. For `ModuleNotFoundError`, check that requirements were installed in that environment. For missing local files, check the working directory.


## 1. Propagate signs through one affine bound

For a=2x1−3x2+0.5 and x1,x2∈[0,1], the smallest value uses x1=0,x2=1; the largest uses x1=1,x2=0. Positive weights multiply lower bounds for a lower estimate; negative weights multiply upper bounds. This is the calculation performed layer by layer.

```python
from pathlib import Path
import json
import numpy as np
import week06_lab as lab
lo, hi = np.zeros(2), np.ones(2)
w = np.array([2., -3.]); b = .5
lower = lo@np.maximum(w,0)+hi@np.minimum(w,0)+b
upper = hi@np.maximum(w,0)+lo@np.minimum(w,0)+b
print("affine bounds:", lower, upper, "ReLU bounds:", max(0,lower), max(0,upper))
np.testing.assert_allclose([lower,upper], [-2.5,2.5])
net = json.loads(Path("frozen_cstr_network.json").read_text())
bounds = lab.interval_bounds(net)
print("first three neuron bounds:", list(zip(bounds[0][0][:3],bounds[0][1][:3])))
```

After ReLU the interval is [0,2.5]. A preactivation upper bound ≤0 fixes a neuron off; a lower bound ≥0 makes it linear. Only intervals crossing zero need binaries. Broad independent intervals may miss correlations between neurons.

## 2. Explain the two-neuron relaxation gap

The toy model has x1+x2=1, so a0=x1+x2−1=0 exactly. The other activation is max(0,x1−x2)=max(0,2x1−1). Requiring total activation ≥0.4 gives the exact solution x1≥0.7. A loose LP can inflate activations; fixing the first activation to zero removes one source of inflation.

```python
toy = {}
for tight in [False,True]:
    for relax in [True,False]:
        result = lab.toy_case(tight,relax)
        toy[tight,relax] = result["objective"]
        print("tight, LP, objective:", tight,relax,result["objective"])
np.testing.assert_allclose([toy[False,True],toy[True,True],toy[True,False]], [0,.4,.7], atol=1e-7)
```

LP lower bounds improve from 0 to 0.4; the MILP optimum remains 0.7. The tightened LP is still a relaxation, not an exact forward graph. A stronger lower bound can reduce search, but preprocessing also takes time.

## 3. Follow physical scaling and layer outputs

At [330 K,6 min], subtract [310,2] and divide by [40,8] to obtain [0.5,0.5]. Each saved weight matrix maps a row of activations to the next layer. Apply ReLU only where the layer metadata says relu; the output layer stays linear.

```python
physical = np.array([330.,6.])
state = (physical-net["offset"])/net["scale"]
print("scaled input:", state)
for index, layer in enumerate(net["layers"]):
    pre = state@np.asarray(layer["weights"])+np.asarray(layer["bias"])
    state = np.maximum(pre,0) if layer["activation"] == "relu" else pre
    print("layer",index,"first preactivations",pre[:3],"first outputs",state[:3])
np.testing.assert_allclose(state,lab.forward(physical,net))
fixed = lab.solve_report(lab.make_omlt(net,fixed=[.5,.5],specifications=False))
assert fixed["has_incumbent"]
np.testing.assert_allclose(fixed["outputs"],state,atol=1e-6)
```

The direct forward output and fixed-input OMLT output should agree within tolerance. This checks scaling, matrix orientation, and activation encoding without mixing in product feasibility. The fixed argument uses scaled coordinates [0.5,0.5].

## 4. Compare complete reports, including failures

The full run compares loose, interval, LP-tightened, and OMLT formulations using identical coefficients. LP-OBBT solves auxiliary LPs to bound each preactivation over the declared input domain. Record bound computation, model construction, and solve time separately.

```python
import subprocess, sys
subprocess.run([sys.executable,"week06_lab.py","--output-dir","guided-results"],check=True)
report = json.loads(Path("guided-results/results.json").read_text())
for row in report["comparisons"]:
    print(row["formulation"],"LP bound",row.get("lp_objective"),"incumbent",row["objective"],
          "binaries",row["binary_variables"],"total seconds",row["total_seconds"])
print("infeasible:",report["infeasible_case"])
print("zero time limit:",report["zero_time_limit_case"])
assert report["max_forward_error"] < 1e-5
assert not report["infeasible_case"]["has_incumbent"]
```

The feasible optimal objectives should agree while relaxation bounds and binary counts can differ. Compare total time, including OBBT, and avoid drawing a speed ranking from one run. An absent incumbent means no selected inputs or gap can be reported. Submit a decoded bound, toy calculation, layer trace, equivalence error, solver status, and reference outputs at the selected point.

## What to report

Record the inputs, outputs, units and fixed conditions; your hand prediction; intermediate computed values; and final metrics with interpretation. Before changing one setting, predict the direction of its effect, then revise that explanation after execution. Record the environment and seed.

[Lecture](/courses/surrogate-models/week-06/) · [Derivations and sources](/courses/surrogate-models/week-06-reading/)

<!-- ko -->

## 문제와 실행 준비

같은 고정 2→12→12→3 반응기 신경망을 수동 제약과 OMLT로 표현합니다. 입력은 T∈[310,350] K, tau∈[2,10]분이고 feed=1.2 mol/L입니다. B≥0.38, C≤0.25와 비음수 출력을 요구하며 tau+0.02(T−310)을 최소화합니다. 유효한 bounds가 신경망을 유지하면서 LP 완화를 어떻게 바꾸는지 확인합니다.

[실습 ZIP](/assets/courses/surrogate-models/week-06/week06-lab.zip)을 풀고 `requirements.txt`, notebook, Python 파일과 제공 모델을 같은 폴더에 둡니다. Python 3.12에서 검증했습니다. 해당 폴더를 작업 디렉터리로 사용하며, 아래 명령 또는 [notebook](/assets/courses/surrogate-models/week-06/week06_lab.ipynb)의 셀을 위에서부터 실행합니다. Notebook만 따로 내려받으면 필요한 스크립트나 모델 파일이 빠질 수 있습니다.

```text
python -m pip install -r requirements.txt
python guided_lab.py
```

`guided_lab.py`는 아래 계산을 순서대로 실행하며 `assert`로 핵심 값을 검사합니다. `guided-results/`에 생성되는 결과는 이번 실행의 출력입니다. ZIP에 있던 기준 결과와 구별해서 비교하세요. Jupyter를 쓸 때는 같은 Python 환경의 kernel을 선택합니다. `ModuleNotFoundError`이면 그 환경에 requirements를 설치했는지, 파일을 찾지 못하면 작업 디렉터리가 압축을 푼 폴더인지 확인합니다.


## 1. Affine bound에서 부호 따라가기

a=2x1−3x2+0.5, x1,x2∈[0,1]이면 최솟값은 x1=0,x2=1에서, 최댓값은 x1=1,x2=0에서 나옵니다. 하한을 구할 때 양의 가중치에는 입력 하한을, 음의 가중치에는 입력 상한을 곱합니다. 이 계산을 층마다 반복합니다.

```python
from pathlib import Path
import json
import numpy as np
import week06_lab as lab
lo, hi = np.zeros(2), np.ones(2)
w = np.array([2., -3.]); b = .5
lower = lo@np.maximum(w,0)+hi@np.minimum(w,0)+b
upper = hi@np.maximum(w,0)+lo@np.minimum(w,0)+b
print("affine bounds:", lower, upper, "ReLU bounds:", max(0,lower), max(0,upper))
np.testing.assert_allclose([lower,upper], [-2.5,2.5])
net = json.loads(Path("frozen_cstr_network.json").read_text())
bounds = lab.interval_bounds(net)
print("first three neuron bounds:", list(zip(bounds[0][0][:3],bounds[0][1][:3])))
```

ReLU를 거치면 [0,2.5]입니다. Preactivation 상한이 0 이하면 꺼진 뉴런이고 하한이 0 이상이면 선형입니다. 0을 가로지르는 뉴런에만 이진 변수가 필요합니다. 독립 구간은 뉴런 사이의 상관관계를 놓칠 수 있습니다.

## 2. 두 뉴런의 완화 차이 설명하기

작은 예제에서 x1+x2=1이므로 a0=x1+x2−1=0입니다. 다른 활성값은 max(0,x1−x2)=max(0,2x1−1)입니다. 활성값 합을 0.4 이상 요구하면 정확한 모델에서는 x1≥0.7입니다. 느슨한 LP는 활성값을 부풀릴 수 있고 첫 활성값을 0으로 고정하면 그 여지가 줄어듭니다.

```python
toy = {}
for tight in [False,True]:
    for relax in [True,False]:
        result = lab.toy_case(tight,relax)
        toy[tight,relax] = result["objective"]
        print("tight, LP, objective:", tight,relax,result["objective"])
np.testing.assert_allclose([toy[False,True],toy[True,True],toy[True,False]], [0,.4,.7], atol=1e-7)
```

LP 하한은 0에서 0.4로 좋아지고 MILP 최적값은 0.7로 유지됩니다. 강화한 LP도 여전히 완화식입니다. 하한이 좋아지면 탐색을 줄일 수 있지만 전처리 시간도 듭니다.

## 3. 물리 입력 scaling과 층별 출력 확인하기

[330 K,6분]에서 [310,2]를 빼고 [40,8]로 나누면 [0.5,0.5]입니다. 저장된 가중치 행렬은 활성값 한 행을 다음 층으로 옮깁니다. Metadata가 relu인 층에만 ReLU를 적용하고 출력층은 선형으로 둡니다.

```python
physical = np.array([330.,6.])
state = (physical-net["offset"])/net["scale"]
print("scaled input:", state)
for index, layer in enumerate(net["layers"]):
    pre = state@np.asarray(layer["weights"])+np.asarray(layer["bias"])
    state = np.maximum(pre,0) if layer["activation"] == "relu" else pre
    print("layer",index,"first preactivations",pre[:3],"first outputs",state[:3])
np.testing.assert_allclose(state,lab.forward(physical,net))
fixed = lab.solve_report(lab.make_omlt(net,fixed=[.5,.5],specifications=False))
assert fixed["has_incumbent"]
np.testing.assert_allclose(fixed["outputs"],state,atol=1e-6)
```

직접 forward와 입력 고정 OMLT 출력이 허용오차 안에서 같아야 합니다. 제품 규격 가능성과 분리해 scaling·행렬 방향·활성식 구현을 확인합니다. fixed 인수에는 scaling된 [0.5,0.5]를 넣습니다.

## 4. 실패 상태까지 포함해 보고서 비교하기

전체 실행은 같은 계수로 느슨한 bounds, 구간 전파, LP 강화, OMLT를 비교합니다. LP-OBBT는 입력 영역에서 보조 LP를 풀어 각 preactivation의 범위를 구합니다. Bound 계산·모델 구성·solver 시간을 나눠 기록합니다.

```python
import subprocess, sys
subprocess.run([sys.executable,"week06_lab.py","--output-dir","guided-results"],check=True)
report = json.loads(Path("guided-results/results.json").read_text())
for row in report["comparisons"]:
    print(row["formulation"],"LP bound",row.get("lp_objective"),"incumbent",row["objective"],
          "binaries",row["binary_variables"],"total seconds",row["total_seconds"])
print("infeasible:",report["infeasible_case"])
print("zero time limit:",report["zero_time_limit_case"])
assert report["max_forward_error"] < 1e-5
assert not report["infeasible_case"]["has_incumbent"]
```

가능한 최적값은 일치해야 하지만 완화 하한과 이진 변수 수는 다를 수 있습니다. OBBT를 포함한 총 시간을 비교하고 한 번의 실행으로 속도 순위를 정하지 않습니다. Incumbent가 없으면 선택 입력이나 gap을 보고할 수 없습니다. Bound 계산, 작은 예제, 층별 추적, 일치 오차, 종료 상태, 선택점의 기준 출력을 제출하세요.

## 제출할 내용

입력·출력·단위와 고정 조건, 손으로 예측한 값, 코드로 얻은 중간값, 최종 지표와 해석을 기록합니다. 설정 하나를 바꾸기 전에 결과가 어느 방향으로 달라질지 적고 실행 후 설명을 수정하세요. 실행 환경과 seed도 남깁니다.

[강의](/courses/surrogate-models/week-06/) · [풀이와 출처](/courses/surrogate-models/week-06-reading/)
