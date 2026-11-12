"""From a material balance to an evaluated predictor.
물질수지에서 예측 모델 평가까지
Run beside the lab files: python guided_lab.py
"""

def main():
    # %% 1. Calculate one reference point / 1. 기준 운전점 하나 계산하기
    # At steady state, inflow minus outflow minus reaction is zero: (feed−CA)/tau−k·CA=0. Moving the CA terms together gives CA=feed/(1+k·tau). At 330 K, k=0.2/min; k·tau=1 at five minutes. Half the feed remains, so conversion is one half. A sample is one row with three input columns.
    # 정상상태에서는 유입−유출−반응이 0이므로 (feed−CA)/tau−k·CA=0입니다. CA가 든 항을 모으면 CA=feed/(1+k·tau)입니다. 330 K에서 k=0.2/min이고 5분이면 k·tau=1입니다. 유입 농도의 절반이 남으므로 전환율도 절반입니다. 입력 한 행에 온도·체류시간·유입 농도 세 열을 넣습니다.
    print("\n1. Calculate one reference point")
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

    # %% 2. Turn physical inputs into features / 2. 물리 입력을 feature로 바꾸기
    # The three inputs have different scales. Map the declared operating box [300,360] K × [1,10] min × [0.8,1.5] mol/L to [−1,1] in each coordinate. Add a constant, three linear terms, three squares, and three cross terms. Ten features allow curvature without a neural network.
    # 입력 세 개의 크기가 다릅니다. 선언한 영역 [300,360] K × [1,10] min × [0.8,1.5] mol/L을 각 좌표의 [−1,1]로 옮깁니다. 상수 하나, 일차항 세 개, 제곱항 세 개, 교차항 세 개를 만들면 신경망 없이도 곡률을 표현할 수 있습니다.
    print("\n2. Turn physical inputs into features")
    scaled = 2*(x-lab.LOWER)/(lab.UPPER-lab.LOWER)-1
    phi = lab.features(x)
    print("scaled inputs:", scaled)
    print("first feature row:", phi[0])
    assert phi.shape == (2, 10)
    np.testing.assert_allclose(scaled[0], [0, -1/9, 1/7])

    # %% 3. Fit using training rows only / 3. Train 행만으로 계수 구하기
    # Least squares chooses coefficients that minimize the sum of squared training errors. The matrix product (400×10) @ (10×2) produces 400 two-output predictions. Validation and test rows do not enter this solve.
    # 최소제곱법은 train 오차 제곱합을 줄이는 계수를 찾습니다. (400×10) @ (10×2)의 결과는 400개의 두 출력 예측입니다. Validation과 test 행은 이 계산에 넣지 않습니다.
    print("\n3. Fit using training rows only")
    splits = lab.generate_splits(seed=42)
    train_x, train_y = splits["train"]
    weights, _, rank, _ = np.linalg.lstsq(lab.features(train_x), train_y, rcond=None)
    print("split sizes:", {name: len(pair[0]) for name, pair in splits.items()})
    print("design, weights, rank:", lab.features(train_x).shape, weights.shape, rank)
    assert rank == 10 and weights.shape == (10, 2)
    test_x, test_y = splits["test"]
    prediction = lab.features(test_x) @ weights
    print("first test reference, prediction, error:", test_y[0], prediction[0], prediction[0]-test_y[0])

    # %% 4. Reconstruct error metrics and interpret / 4. 오차 지표를 직접 계산하고 해석하기
    # Square each residual, average over the 160 test rows, then take the square root separately for each output. Also check CA+feed·X−feed. The latter measures consistency between the two predicted outputs, so a small value alone cannot establish agreement with the reference.
    # 각 오차를 제곱하고 test 160행에 대해 평균한 뒤 출력별로 제곱근을 구합니다. CA+feed·X−feed도 확인합니다. 이 값은 두 예측 출력 사이의 일관성이므로 작다고 기준값과도 가깝다는 뜻은 아닙니다.
    print("\n4. Reconstruct error metrics and interpret")
    error = prediction-test_y
    rmse = np.sqrt(np.mean(error**2, axis=0))
    consistency = prediction[:, 0]+test_x[:, 2]*prediction[:, 1]-test_x[:, 2]
    metrics = lab.evaluate_predictions(test_x, test_y, prediction)
    np.testing.assert_allclose(rmse, [metrics["ca_rmse_mol_per_l"], metrics["conversion_rmse"]])
    print("RMSE [CA, X]:", rmse)
    print("first three consistency residuals:", consistency[:3])
    report = lab.run_lab(Path("guided-results"), seed=42)
    assert report["prediction_metrics"]["test"] == metrics

if __name__ == "__main__":
    main()
