# Why a convex hinge model can use an LP / Convex hinge 모델을 LP로 푸는 이유

## Problem and setup

Choose a dimensionless operating variable u∈[0,1] that minimizes a convex cost surrogate. A one-dimensional hinge network is a simple input-convex model: an affine term plus nonnegative multiples of ReLU(u−knot). First solve a hand model, then fit a convex quadratic reference and compare prediction error with decision loss.

Extract the [lab ZIP](https://sunboogermany.github.io/assets/courses/surrogate-models/week-07/week07-lab.zip), keeping `requirements.txt`, the notebook, Python scripts, and supplied models together. These exercises were checked with Python 3.12. Use that folder as the working directory and run the commands below, or execute the [notebook](https://sunboogermany.github.io/assets/courses/surrogate-models/week-07/week07_lab.ipynb) cells in order. Downloading the notebook alone can omit required scripts or model files.

```text
python -m pip install -r requirements.txt
python guided_lab.py
```

`guided_lab.py` executes the calculations below in order and checks key values with assertions. Files in `guided-results/` belong to your new run; compare them with the supplied reference results. For Jupyter, select a kernel from the same Python environment. For `ModuleNotFoundError`, check that requirements were installed in that environment. For missing local files, check the working directory.


## 1. Calculate values and slopes by interval

Use f(u)=0.4−0.6u+ReLU(u−0.4)+0.5ReLU(u−0.7). Before 0.4, both hinges are zero and the slope is −0.6. After the first knot, add 1 to the slope; after the second, add 0.5. Nonnegative additions make slopes nondecreasing.

```python
from pathlib import Path
import json
import numpy as np
from scipy.optimize import linprog, lsq_linear
import week07_lab as lab
hand = {"knots":[.4,.7],"coefficients":[.4,-.6,1.,.5]}
points = np.array([0.,.4,.7,1.])
design = lab.features(points,np.array(hand["knots"]))
values = lab.forward(points,hand)
print("columns [1,u,hinge1,hinge2]:",design)
print("values:",values,"slopes:",[-.6,.4,.9])
np.testing.assert_allclose(values,[.4,.16,.28,.55])
```

The cost falls until u=0.4 and then rises, so the minimum is f(0.4)=0.16. The convexity argument depends on the nonnegative hinge weights, not on ReLU alone.

## 2. Let minimization tighten the lifted activations

Replace each hinge by h≥u−knot and h≥0. With positive objective weights, increasing h raises cost, so minimization chooses the smallest feasible h. The resulting optimal objective matches the forward network without binaries.

```python
solution = lab.solve_lp(hand)
print("LP result:",solution)
u = solution["u"]
hidden = np.maximum(u-np.array(hand["knots"]),0)
print("minimal hidden values:",hidden)
np.testing.assert_allclose([u,solution["objective"]],[.4,.16])
assert solution["binaries"] == 0
```

At u=0.4, hidden values are [0,0]. Tightness is induced by the minimization direction and weights. A constraint that rewards inflated h can break this equivalence.

## 3. Construct the misleading lower-bound example

For h=ReLU(u) with u≥0, requiring h≥0.8 means u≥0.8. But the epigraph inequalities h≥u,h≥0,h≥0.8 allow u=0,h=0.8. Minimizing u chooses that false candidate because the objective no longer penalizes h.

```python
relaxed = linprog([1.,0.],A_ub=[[1.,-1.],[0.,-1.]],b_ub=[0.,-.8],
                  bounds=[(0,1),(0,None)],method="highs")
print("lifted [u,h]:",relaxed.x,"true ReLU at u:",max(0,relaxed.x[0]))
assert relaxed.success and abs(relaxed.x[0]) < 1e-9
assert max(0,relaxed.x[0]) < .8
unbounded = linprog([0.,-1.],A_ub=[[1.,-1.]],b_ub=[0.],bounds=[(0,1),(0,None)],method="highs")
assert unbounded.status == 3
```

The lower-bound model is falsely feasible; a negative coefficient rewarding unbounded h makes the second LP unbounded. Always check the direction in which the objective and constraints use a lifted network output.

## 4. Fit, then distinguish prediction and decision error

The reference q(u)=<math xmlns="http://www.w3.org/1998/Math/MathML"><msup><mrow><mo>(</mo><mi>u</mi><mo>−</mo><mn>0.6</mn><mo>)</mo></mrow><mn>2</mn></msup></math>+0.1u+0.2 has derivative 2u−1.1, so its minimum is at u=0.55 with cost 0.2575. For 41 training points, build columns [1,u,hinges] and fit 11 coefficients. The first two coefficient bounds are unrestricted; the remaining nine lower bounds are zero to preserve convexity. Evaluate 200 separate midpoint samples. The fitted LP selects an operating point; q at that point measures the real decision cost.

```python
reference = lambda z: (np.asarray(z)-.6)**2+.1*np.asarray(z)+.2
knots = np.arange(.1,1.,.1)
train = np.linspace(0,1,41)
design = lab.features(train,knots)
lower = np.r_[[-np.inf,-np.inf],np.zeros(len(knots))]
fit = lsq_linear(design,reference(train),bounds=(lower,np.full(len(lower),np.inf)),tol=1e-12)
assert fit.success
print("training matrix:",design.shape,"first feature row:",design[0])
print("coefficients [b,a,hinge weights]:",fit.x)
report = lab.run(Path("guided-results"))
model = json.loads(Path("guided-results/fitted_icnn.json").read_text())
np.testing.assert_allclose(fit.x,model["coefficients"])
u = report["fitted"]["u"]
decision_loss = float(reference(u)-reference(.55))
print("selected u:",u,"surrogate cost:",lab.forward([u],model)[0])
print("reference cost:",reference(u),"decision loss:",decision_loss)
np.testing.assert_allclose(reference(.55),.2575)
np.testing.assert_allclose(decision_loss,report["reference"]["decision_loss"])
print("held-out prediction errors:",report["heldout"])
print("fixed-context solutions:",report["conditional"])
```

RMSE averages prediction errors over independent points; decision loss compares reference costs at two selected points. They answer different questions. In the conditional examples, context is fixed while u is optimized; convexity in u does not imply joint convexity in context and u. Change knot spacing using training/validation data, then report held-out error and reference decision loss separately.

## What to report

Record the inputs, outputs, units and fixed conditions; your hand prediction; intermediate computed values; and final metrics with interpretation. Before changing one setting, predict the direction of its effect, then revise that explanation after execution. Record the environment and seed.

[Lecture](https://sunboogermany.github.io/courses/surrogate-models/week-07/) · [Derivations and sources](https://sunboogermany.github.io/courses/surrogate-models/week-07-reading/)

---

## 문제와 실행 준비

무차원 운전 변수 u∈[0,1]에서 convex 비용 surrogate를 최소화합니다. Affine 항에 ReLU(u−knot)의 비음수 가중합을 더한 1차원 hinge 신경망은 간단한 input-convex 모델입니다. 손계산 모델을 푼 뒤 convex 이차 기준식에 모델을 맞추고 예측 오차와 의사결정 손실을 비교합니다.

[실습 ZIP](https://sunboogermany.github.io/assets/courses/surrogate-models/week-07/week07-lab.zip)을 풀고 `requirements.txt`, notebook, Python 파일과 제공 모델을 같은 폴더에 둡니다. Python 3.12에서 검증했습니다. 해당 폴더를 작업 디렉터리로 사용하며, 아래 명령 또는 [notebook](https://sunboogermany.github.io/assets/courses/surrogate-models/week-07/week07_lab.ipynb)의 셀을 위에서부터 실행합니다. Notebook만 따로 내려받으면 필요한 스크립트나 모델 파일이 빠질 수 있습니다.

```text
python -m pip install -r requirements.txt
python guided_lab.py
```

`guided_lab.py`는 아래 계산을 순서대로 실행하며 `assert`로 핵심 값을 검사합니다. `guided-results/`에 생성되는 결과는 이번 실행의 출력입니다. ZIP에 있던 기준 결과와 구별해서 비교하세요. Jupyter를 쓸 때는 같은 Python 환경의 kernel을 선택합니다. `ModuleNotFoundError`이면 그 환경에 requirements를 설치했는지, 파일을 찾지 못하면 작업 디렉터리가 압축을 푼 폴더인지 확인합니다.


## 1. 구간별 값과 기울기 계산하기

f(u)=0.4−0.6u+ReLU(u−0.4)+0.5ReLU(u−0.7)을 사용합니다. 0.4 이전에는 두 hinge가 0이고 기울기가 −0.6입니다. 첫 knot 뒤에서 기울기에 1, 두 번째 뒤에서 0.5를 더합니다. 비음수 값을 더하므로 기울기가 감소하지 않습니다.

```python
from pathlib import Path
import json
import numpy as np
from scipy.optimize import linprog, lsq_linear
import week07_lab as lab
hand = {"knots":[.4,.7],"coefficients":[.4,-.6,1.,.5]}
points = np.array([0.,.4,.7,1.])
design = lab.features(points,np.array(hand["knots"]))
values = lab.forward(points,hand)
print("columns [1,u,hinge1,hinge2]:",design)
print("values:",values,"slopes:",[-.6,.4,.9])
np.testing.assert_allclose(values,[.4,.16,.28,.55])
```

비용은 u=0.4까지 줄고 이후 늘므로 최솟값은 f(0.4)=0.16입니다. Convexity는 ReLU를 썼다는 사실만으로 얻는 것이 아니라 hinge 가중치가 비음수라는 조건에서 나옵니다.

## 2. 최소화가 보조 활성값을 낮추는 과정 보기

각 hinge를 h≥u−knot, h≥0으로 바꿉니다. 목적함수 가중치가 양수이면 h를 키울수록 비용이 늘어 최소화가 가능한 가장 작은 h를 고릅니다. 이때 이진 변수 없이 forward 신경망과 같은 최적값을 얻습니다.

```python
solution = lab.solve_lp(hand)
print("LP result:",solution)
u = solution["u"]
hidden = np.maximum(u-np.array(hand["knots"]),0)
print("minimal hidden values:",hidden)
np.testing.assert_allclose([u,solution["objective"]],[.4,.16])
assert solution["binaries"] == 0
```

u=0.4에서 hidden 값은 [0,0]입니다. 등호가 성립하는 이유는 최소화 방향과 가중치입니다. h를 부풀리면 유리해지는 제약에서는 이 대조가 깨질 수 있습니다.

## 3. 잘못된 하한 제약의 반례 만들기

u≥0에서 h=ReLU(u)에 h≥0.8을 요구하면 u≥0.8이어야 합니다. 하지만 h≥u,h≥0,h≥0.8만 두면 u=0,h=0.8도 가능합니다. 목적함수에서 h를 벌주지 않고 u만 줄이면 이 잘못된 후보를 선택합니다.

```python
relaxed = linprog([1.,0.],A_ub=[[1.,-1.],[0.,-1.]],b_ub=[0.,-.8],
                  bounds=[(0,1),(0,None)],method="highs")
print("lifted [u,h]:",relaxed.x,"true ReLU at u:",max(0,relaxed.x[0]))
assert relaxed.success and abs(relaxed.x[0]) < 1e-9
assert max(0,relaxed.x[0]) < .8
unbounded = linprog([0.,-1.],A_ub=[[1.,-1.]],b_ub=[0.],bounds=[(0,1),(0,None)],method="highs")
assert unbounded.status == 3
```

하한 모델은 실제보다 넓은 가능영역을 만들고, 상한 없는 h에 음수 목적계수를 붙인 두 번째 LP는 unbounded가 됩니다. 목적함수와 제약이 보조 출력을 어느 방향으로 사용하는지 확인하세요.

## 4. 학습 후 예측 오차와 선택 손실 구별하기

기준식 q(u)=<math xmlns="http://www.w3.org/1998/Math/MathML"><msup><mrow><mo>(</mo><mi>u</mi><mo>−</mo><mn>0.6</mn><mo>)</mo></mrow><mn>2</mn></msup></math>+0.1u+0.2의 미분은 2u−1.1이므로 u=0.55, 비용 0.2575에서 최소입니다. Train 41점에서 [1,u,hinge들] 열을 만들고 계수 11개를 학습합니다. 처음 두 계수는 부호 제한이 없고 나머지 아홉 계수의 하한은 0으로 두어 convexity를 유지합니다. 별도 중간점 200개로 평가합니다. 학습 모델의 LP가 고른 u를 q에 넣어 실제 선택 비용을 구합니다.

```python
reference = lambda z: (np.asarray(z)-.6)**2+.1*np.asarray(z)+.2
knots = np.arange(.1,1.,.1)
train = np.linspace(0,1,41)
design = lab.features(train,knots)
lower = np.r_[[-np.inf,-np.inf],np.zeros(len(knots))]
fit = lsq_linear(design,reference(train),bounds=(lower,np.full(len(lower),np.inf)),tol=1e-12)
assert fit.success
print("training matrix:",design.shape,"first feature row:",design[0])
print("coefficients [b,a,hinge weights]:",fit.x)
report = lab.run(Path("guided-results"))
model = json.loads(Path("guided-results/fitted_icnn.json").read_text())
np.testing.assert_allclose(fit.x,model["coefficients"])
u = report["fitted"]["u"]
decision_loss = float(reference(u)-reference(.55))
print("selected u:",u,"surrogate cost:",lab.forward([u],model)[0])
print("reference cost:",reference(u),"decision loss:",decision_loss)
np.testing.assert_allclose(reference(.55),.2575)
np.testing.assert_allclose(decision_loss,report["reference"]["decision_loss"])
print("held-out prediction errors:",report["heldout"])
print("fixed-context solutions:",report["conditional"])
```

RMSE는 독립 점의 예측 오차를 평균하고 의사결정 손실은 선택점과 기준 최적점의 기준 비용을 비교합니다. 두 값의 질문이 다릅니다. 조건부 예제에서는 context를 고정한 채 u를 최적화합니다. u에 대한 convexity가 context와 u의 결합 convexity를 뜻하지는 않습니다. Train·validation으로 knot 간격을 바꾼 뒤 독립 오차와 기준 선택 손실을 따로 보고하세요.

## 제출할 내용

입력·출력·단위와 고정 조건, 손으로 예측한 값, 코드로 얻은 중간값, 최종 지표와 해석을 기록합니다. 설정 하나를 바꾸기 전에 결과가 어느 방향으로 달라질지 적고 실행 후 설명을 수정하세요. 실행 환경과 seed도 남깁니다.

[강의](https://sunboogermany.github.io/courses/surrogate-models/week-07/) · [풀이와 출처](https://sunboogermany.github.io/courses/surrogate-models/week-07-reading/)
