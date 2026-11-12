# From a material balance to an evaluated predictor / 물질수지에서 예측 모델 평가까지

## Problem and setup

A reactor operator needs outlet concentration and conversion for a proposed temperature, residence time, and feed. Start with an ideal isothermal, first-order A → B CSTR. Generate labels with its steady balance, fit a cheap quadratic predictor, and measure errors on independent inputs.

Extract the [lab ZIP](https://sunboogermany.github.io/assets/courses/surrogate-models/week-01/week01-lab.zip), keeping `requirements.txt`, the notebook, Python scripts, and supplied models together. These exercises were checked with Python 3.12. Use that folder as the working directory and run the commands below, or execute the [notebook](https://sunboogermany.github.io/assets/courses/surrogate-models/week-01/week01_lab.ipynb) cells in order. Downloading the notebook alone can omit required scripts or model files.

```text
python -m pip install -r requirements.txt
python guided_lab.py
```

`guided_lab.py` executes the calculations below in order and checks key values with assertions. Files in `guided-results/` belong to your new run; compare them with the supplied reference results. For Jupyter, select a kernel from the same Python environment. For `ModuleNotFoundError`, check that requirements were installed in that environment. For missing local files, check the working directory.


## 1. Calculate one reference point

At steady state, inflow minus outflow minus reaction is zero: (feed−CA)/tau−k·CA=0. Moving the CA terms together gives CA=feed/(1+k·tau). At 330 K, k=0.2/min; k·tau=1 at five minutes. Half the feed remains, so conversion is one half. A sample is one row with three input columns.

```python
from pathlib import Path
import numpy as np
import week01_lab as lab
x = np.array([[330., 5., 1.2], [330., 10., 1.2]])
k = lab.rate_constant(x[:, 0])
denominator = 1 + k*x[:, 1]
ca = x[:, 2]/denominator
conversion = 1-ca/x[:, 2]
print("k, denominator, CA, X:", np.column_stack([k, denominator, ca, conversion]))
np.testing.assert_allclose(lab.steady_state(x), np.column_stack([ca, conversion]))
np.testing.assert_allclose(ca, [.6, .4])
```

The rows are [0.2,2,0.6,0.5] and [0.2,3,0.4,0.666667]. CA is in mol/L; conversion is dimensionless. Longer residence leaves less A at this fixed temperature and feed.

## 2. Turn physical inputs into features

The three inputs have different scales. Map the declared operating box [300,360] K × [1,10] min × [0.8,1.5] mol/L to [−1,1] in each coordinate. Add a constant, three linear terms, three squares, and three cross terms. Ten features allow curvature without a neural network.

```python
scaled = 2*(x-lab.LOWER)/(lab.UPPER-lab.LOWER)-1
phi = lab.features(x)
print("scaled inputs:", scaled)
print("first feature row:", phi[0])
assert phi.shape == (2, 10)
np.testing.assert_allclose(scaled[0], [0, -1/9, 1/7])
```

For the first point the scaled coordinates are [0,−1/9,1/7]. The feature row begins [1,0,−1/9,1/7]. Two output columns need 10×2=20 fitted coefficients; units are recovered in the output predictions.

## 3. Fit using training rows only

Least squares chooses coefficients that minimize the sum of squared training errors. The matrix product (400×10) @ (10×2) produces 400 two-output predictions. Validation and test rows do not enter this solve.

```python
splits = lab.generate_splits(seed=42)
train_x, train_y = splits["train"]
weights, _, rank, _ = np.linalg.lstsq(lab.features(train_x), train_y, rcond=None)
print("split sizes:", {name: len(pair[0]) for name, pair in splits.items()})
print("design, weights, rank:", lab.features(train_x).shape, weights.shape, rank)
assert rank == 10 and weights.shape == (10, 2)
test_x, test_y = splits["test"]
prediction = lab.features(test_x) @ weights
print("first test reference, prediction, error:", test_y[0], prediction[0], prediction[0]-test_y[0])
```

The split sizes are 400,120,160 and rank is 10. The first test residual is prediction minus reference; its sign tells whether the predictor overestimates that output. A full-rank solve identifies the coefficients, not perfect physical predictions.

## 4. Reconstruct error metrics and interpret

Square each residual, average over the 160 test rows, then take the square root separately for each output. Also check CA+feed·X−feed. The latter measures consistency between the two predicted outputs, so a small value alone cannot establish agreement with the reference.

```python
error = prediction-test_y
rmse = np.sqrt(np.mean(error**2, axis=0))
consistency = prediction[:, 0]+test_x[:, 2]*prediction[:, 1]-test_x[:, 2]
metrics = lab.evaluate_predictions(test_x, test_y, prediction)
np.testing.assert_allclose(rmse, [metrics["ca_rmse_mol_per_l"], metrics["conversion_rmse"]])
print("RMSE [CA, X]:", rmse)
print("first three consistency residuals:", consistency[:3])
report = lab.run_lab(Path("guided-results"), seed=42)
assert report["prediction_metrics"]["test"] == metrics
```

Read guided-results/results.json and prediction-check.png together. On a parity plot, the diagonal is exact agreement; points above it are overpredictions. Repeat with another seed, keeping the feature basis fixed, and explain which errors change. Retain the test set for final evaluation when selecting a different basis.

## Result figure

After running, open `guided-results/prediction-check.png` and relate it to the errors computed above.

## What to report

Record the inputs, outputs, units and fixed conditions; your hand prediction; intermediate computed values; and final metrics with interpretation. Before changing one setting, predict the direction of its effect, then revise that explanation after execution. Record the environment and seed.

[Lecture](https://sunboogermany.github.io/courses/surrogate-models/week-01/) · [Derivations and sources](https://sunboogermany.github.io/courses/surrogate-models/week-01-reading/)

---

## 문제와 실행 준비

반응기 운전자가 온도·체류시간·유입 농도를 정했을 때 출구 농도와 전환율을 알고 싶어 합니다. 이상적 등온 CSTR의 1차 반응 A → B를 가정합니다. 정상상태 물질수지로 기준값을 만든 뒤 이차 예측식을 학습하고 독립 입력에서 오차를 확인합니다.

[실습 ZIP](https://sunboogermany.github.io/assets/courses/surrogate-models/week-01/week01-lab.zip)을 풀고 `requirements.txt`, notebook, Python 파일과 제공 모델을 같은 폴더에 둡니다. Python 3.12에서 검증했습니다. 해당 폴더를 작업 디렉터리로 사용하며, 아래 명령 또는 [notebook](https://sunboogermany.github.io/assets/courses/surrogate-models/week-01/week01_lab.ipynb)의 셀을 위에서부터 실행합니다. Notebook만 따로 내려받으면 필요한 스크립트나 모델 파일이 빠질 수 있습니다.

```text
python -m pip install -r requirements.txt
python guided_lab.py
```

`guided_lab.py`는 아래 계산을 순서대로 실행하며 `assert`로 핵심 값을 검사합니다. `guided-results/`에 생성되는 결과는 이번 실행의 출력입니다. ZIP에 있던 기준 결과와 구별해서 비교하세요. Jupyter를 쓸 때는 같은 Python 환경의 kernel을 선택합니다. `ModuleNotFoundError`이면 그 환경에 requirements를 설치했는지, 파일을 찾지 못하면 작업 디렉터리가 압축을 푼 폴더인지 확인합니다.


## 1. 기준 운전점 하나 계산하기

정상상태에서는 유입−유출−반응이 0이므로 (feed−CA)/tau−k·CA=0입니다. CA가 든 항을 모으면 CA=feed/(1+k·tau)입니다. 330 K에서 k=0.2/min이고 5분이면 k·tau=1입니다. 유입 농도의 절반이 남으므로 전환율도 절반입니다. 입력 한 행에 온도·체류시간·유입 농도 세 열을 넣습니다.

```python
from pathlib import Path
import numpy as np
import week01_lab as lab
x = np.array([[330., 5., 1.2], [330., 10., 1.2]])
k = lab.rate_constant(x[:, 0])
denominator = 1 + k*x[:, 1]
ca = x[:, 2]/denominator
conversion = 1-ca/x[:, 2]
print("k, denominator, CA, X:", np.column_stack([k, denominator, ca, conversion]))
np.testing.assert_allclose(lab.steady_state(x), np.column_stack([ca, conversion]))
np.testing.assert_allclose(ca, [.6, .4])
```

각 행은 [0.2,2,0.6,0.5], [0.2,3,0.4,0.666667]입니다. CA의 단위는 mol/L이고 전환율은 무차원입니다. 온도와 유입 농도를 고정하면 체류시간이 길수록 A가 적게 남습니다.

## 2. 물리 입력을 feature로 바꾸기

입력 세 개의 크기가 다릅니다. 선언한 영역 [300,360] K × [1,10] min × [0.8,1.5] mol/L을 각 좌표의 [−1,1]로 옮깁니다. 상수 하나, 일차항 세 개, 제곱항 세 개, 교차항 세 개를 만들면 신경망 없이도 곡률을 표현할 수 있습니다.

```python
scaled = 2*(x-lab.LOWER)/(lab.UPPER-lab.LOWER)-1
phi = lab.features(x)
print("scaled inputs:", scaled)
print("first feature row:", phi[0])
assert phi.shape == (2, 10)
np.testing.assert_allclose(scaled[0], [0, -1/9, 1/7])
```

첫 운전점의 좌표는 [0,−1/9,1/7]이고 feature 행은 [1,0,−1/9,1/7]로 시작합니다. 출력 두 열에 10×2=20개의 계수를 학습합니다. 예측 결과는 원래 출력 단위를 가집니다.

## 3. Train 행만으로 계수 구하기

최소제곱법은 train 오차 제곱합을 줄이는 계수를 찾습니다. (400×10) @ (10×2)의 결과는 400개의 두 출력 예측입니다. Validation과 test 행은 이 계산에 넣지 않습니다.

```python
splits = lab.generate_splits(seed=42)
train_x, train_y = splits["train"]
weights, _, rank, _ = np.linalg.lstsq(lab.features(train_x), train_y, rcond=None)
print("split sizes:", {name: len(pair[0]) for name, pair in splits.items()})
print("design, weights, rank:", lab.features(train_x).shape, weights.shape, rank)
assert rank == 10 and weights.shape == (10, 2)
test_x, test_y = splits["test"]
prediction = lab.features(test_x) @ weights
print("first test reference, prediction, error:", test_y[0], prediction[0], prediction[0]-test_y[0])
```

분할 크기는 400,120,160이고 rank는 10입니다. 첫 test 오차는 예측−기준값이며 부호로 과대·과소 예측을 읽습니다. Full rank는 계수를 식별한다는 뜻이며 공정 예측이 정확하다는 뜻은 아닙니다.

## 4. 오차 지표를 직접 계산하고 해석하기

각 오차를 제곱하고 test 160행에 대해 평균한 뒤 출력별로 제곱근을 구합니다. CA+feed·X−feed도 확인합니다. 이 값은 두 예측 출력 사이의 일관성이므로 작다고 기준값과도 가깝다는 뜻은 아닙니다.

```python
error = prediction-test_y
rmse = np.sqrt(np.mean(error**2, axis=0))
consistency = prediction[:, 0]+test_x[:, 2]*prediction[:, 1]-test_x[:, 2]
metrics = lab.evaluate_predictions(test_x, test_y, prediction)
np.testing.assert_allclose(rmse, [metrics["ca_rmse_mol_per_l"], metrics["conversion_rmse"]])
print("RMSE [CA, X]:", rmse)
print("first three consistency residuals:", consistency[:3])
report = lab.run_lab(Path("guided-results"), seed=42)
assert report["prediction_metrics"]["test"] == metrics
```

guided-results/results.json과 prediction-check.png를 함께 읽습니다. Parity plot의 대각선은 정확한 예측이고 위쪽 점은 과대 예측입니다. Feature를 고정한 채 seed를 바꾸고 오차가 어떻게 달라지는지 설명하세요. 다른 feature를 선택한다면 test는 최종 평가에 남겨둡니다.

## 결과 그림

실행 후 `guided-results/prediction-check.png`을 열고 위에서 계산한 오차와 연결해 해석하세요.

## 제출할 내용

입력·출력·단위와 고정 조건, 손으로 예측한 값, 코드로 얻은 중간값, 최종 지표와 해석을 기록합니다. 설정 하나를 바꾸기 전에 결과가 어느 방향으로 달라질지 적고 실행 후 설명을 수정하세요. 실행 환경과 seed도 남깁니다.

[강의](https://sunboogermany.github.io/courses/surrogate-models/week-01/) · [풀이와 출처](https://sunboogermany.github.io/courses/surrogate-models/week-01-reading/)
