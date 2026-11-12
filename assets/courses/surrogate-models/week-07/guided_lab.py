"""Why a convex hinge model can use an LP.
Convex hinge 모델을 LP로 푸는 이유
Run beside the lab files: python guided_lab.py
"""

def main():
    # %% 1. Calculate values and slopes by interval / 1. 구간별 값과 기울기 계산하기
    # Use f(u)=0.4−0.6u+ReLU(u−0.4)+0.5ReLU(u−0.7). Before 0.4, both hinges are zero and the slope is −0.6. After the first knot, add 1 to the slope; after the second, add 0.5. Nonnegative additions make slopes nondecreasing.
    # f(u)=0.4−0.6u+ReLU(u−0.4)+0.5ReLU(u−0.7)을 사용합니다. 0.4 이전에는 두 hinge가 0이고 기울기가 −0.6입니다. 첫 knot 뒤에서 기울기에 1, 두 번째 뒤에서 0.5를 더합니다. 비음수 값을 더하므로 기울기가 감소하지 않습니다.
    print("\n1. Calculate values and slopes by interval")
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

    # %% 2. Let minimization tighten the lifted activations / 2. 최소화가 보조 활성값을 낮추는 과정 보기
    # Replace each hinge by h≥u−knot and h≥0. With positive objective weights, increasing h raises cost, so minimization chooses the smallest feasible h. The resulting optimal objective matches the forward network without binaries.
    # 각 hinge를 h≥u−knot, h≥0으로 바꿉니다. 목적함수 가중치가 양수이면 h를 키울수록 비용이 늘어 최소화가 가능한 가장 작은 h를 고릅니다. 이때 이진 변수 없이 forward 신경망과 같은 최적값을 얻습니다.
    print("\n2. Let minimization tighten the lifted activations")
    solution = lab.solve_lp(hand)
    print("LP result:",solution)
    u = solution["u"]
    hidden = np.maximum(u-np.array(hand["knots"]),0)
    print("minimal hidden values:",hidden)
    np.testing.assert_allclose([u,solution["objective"]],[.4,.16])
    assert solution["binaries"] == 0

    # %% 3. Construct the misleading lower-bound example / 3. 잘못된 하한 제약의 반례 만들기
    # For h=ReLU(u) with u≥0, requiring h≥0.8 means u≥0.8. But the epigraph inequalities h≥u,h≥0,h≥0.8 allow u=0,h=0.8. Minimizing u chooses that false candidate because the objective no longer penalizes h.
    # u≥0에서 h=ReLU(u)에 h≥0.8을 요구하면 u≥0.8이어야 합니다. 하지만 h≥u,h≥0,h≥0.8만 두면 u=0,h=0.8도 가능합니다. 목적함수에서 h를 벌주지 않고 u만 줄이면 이 잘못된 후보를 선택합니다.
    print("\n3. Construct the misleading lower-bound example")
    relaxed = linprog([1.,0.],A_ub=[[1.,-1.],[0.,-1.]],b_ub=[0.,-.8],
                      bounds=[(0,1),(0,None)],method="highs")
    print("lifted [u,h]:",relaxed.x,"true ReLU at u:",max(0,relaxed.x[0]))
    assert relaxed.success and abs(relaxed.x[0]) < 1e-9
    assert max(0,relaxed.x[0]) < .8
    unbounded = linprog([0.,-1.],A_ub=[[1.,-1.]],b_ub=[0.],bounds=[(0,1),(0,None)],method="highs")
    assert unbounded.status == 3

    # %% 4. Fit, then distinguish prediction and decision error / 4. 학습 후 예측 오차와 선택 손실 구별하기
    # The reference q(u)=(u−0.6)^2+0.1u+0.2 has derivative 2u−1.1, so its minimum is at u=0.55 with cost 0.2575. For 41 training points, build columns [1,u,hinges] and fit 11 coefficients. The first two coefficient bounds are unrestricted; the remaining nine lower bounds are zero to preserve convexity. Evaluate 200 separate midpoint samples. The fitted LP selects an operating point; q at that point measures the real decision cost.
    # 기준식 q(u)=(u−0.6)^2+0.1u+0.2의 미분은 2u−1.1이므로 u=0.55, 비용 0.2575에서 최소입니다. Train 41점에서 [1,u,hinge들] 열을 만들고 계수 11개를 학습합니다. 처음 두 계수는 부호 제한이 없고 나머지 아홉 계수의 하한은 0으로 두어 convexity를 유지합니다. 별도 중간점 200개로 평가합니다. 학습 모델의 LP가 고른 u를 q에 넣어 실제 선택 비용을 구합니다.
    print("\n4. Fit, then distinguish prediction and decision error")
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

if __name__ == "__main__":
    main()
