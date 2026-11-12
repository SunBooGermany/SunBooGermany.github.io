"""Decide only after reference revalidation.
기준식으로 재검증한 뒤 운전점 선택하기
Run beside the lab files: python guided_lab.py
"""

def main():
    # %% 1. Check the baseline by hand / 1. 기준 운전점 손계산하기
    # At 330 K and 6 min, k1=0.2 and k2=0.1 per minute. A=1.2/2.2; B=1.2·A/1.6; C=0.6·B. Test product shortfall max(0,0.38−B), byproduct excess max(0,C−0.25), negativity, and sum error. Cost is 72+4.8=76.8 dollars/hour under the stated teaching assumptions.
    # 330 K, 6분에서 k1=0.2/min, k2=0.1/min입니다. A=1.2/2.2, B=1.2·A/1.6, C=0.6·B입니다. 제품 부족량 max(0,0.38−B), 부산물 초과량 max(0,C−0.25), 음수 농도, 합 오차를 검사합니다. 가정한 교육용 비용은 72+4.8=76.8달러/시간입니다.
    print("\n1. Check the baseline by hand")
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

    # %% 2. Revalidate the optimizer at the same coordinates / 2. 최적점의 같은 좌표에서 재검증하기
    # Solve the surrogate model, then evaluate the reference at exactly the returned T and tau. Average held-out accuracy does not guarantee accuracy at a boundary selected by optimization. Keep prediction error signed so that overpredicted B can be linked directly to product shortfall.
    # Surrogate를 최적화한 뒤 반환된 T와 tau 그대로 기준식을 계산합니다. 독립 데이터의 평균 정확도가 최적화가 선택한 경계점의 정확도를 보장하지는 않습니다. B 과대 예측을 제품 부족과 연결해 읽을 수 있도록 오차 부호를 유지합니다.
    print("\n2. Revalidate the optimizer at the same coordinates")
    point, solver = lab.solve_candidate(net)
    candidate = lab.evaluate("unadjusted",point,net,solver)
    print("selected [T,tau]:",point)
    print("prediction:",candidate["prediction"],"reference:",candidate["reference"])
    print("signed error:",candidate["prediction_error"],"residuals:",candidate["reference_residuals"])
    assert solver["has_incumbent"] and solver["forward_error"] < 1e-6
    assert not candidate["reference_feasible"]
    assert candidate["savings_vs_baseline"] is None

    # %% 3. Calculate directional margins on calibration data / 3. Calibration 데이터로 방향별 margin 계산하기
    # B is dangerous when predicted too high; C is dangerous when predicted too low. On a separate 31×31 calibration grid, take max(predB−refB,0) and max(refC−predC,0). Add the first margin to the B lower bound and subtract the second from the C upper bound.
    # B는 높게 예측하면, C는 낮게 예측하면 규격 위반을 놓칩니다. 별도 31×31 calibration 격자에서 max(predB−refB,0), max(refC−predC,0)을 구합니다. 첫 margin을 B 하한에 더하고 두 번째를 C 상한에서 뺍니다.
    print("\n3. Calculate directional margins on calibration data")
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

    # %% 4. See what nine local evaluations fit / 4. 국소 기준값 아홉 개로 무엇을 맞추는지 보기
    # Center a 3×3 grid at the failed decision using scaled offsets −0.06,0,0.06 and clip to the input box. Fit reference minus prediction as an affine correction in [1,scaled T,scaled tau]. A 9×3 design and 9×3 residual matrix produce 3×3 correction coefficients. The correction is optimized only within that local box.
    # 실패한 선택점의 scaling 좌표에서 −0.06,0,0.06만큼 이동한 3×3 격자를 만들고 입력 영역으로 자릅니다. 기준값−예측을 [1,scaled T,scaled tau]의 affine 보정식으로 맞춥니다. 9×3 설계행렬과 9×3 residual에서 3×3 보정 계수를 얻습니다. 보정 모델은 그 국소 영역에서만 최적화합니다.
    print("\n4. See what nine local evaluations fit")
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

    # %% 5. Compare only accepted candidates on cost / 5. 받아들인 후보의 비용 비교하기
    # For each candidate read the reference residuals before cost savings. A residual tolerance of 1e−7 is used by evaluate. The reference benchmark uses a temperature scan and scalar refinement; it is a numerical comparison point without a certified global lower bound.
    # 후보마다 절감액보다 기준 residual을 먼저 읽습니다. evaluate의 residual 허용오차는 1e−7입니다. 기준 비교점은 온도 격자와 스칼라 정밀 탐색으로 구하며 전역 하한 인증을 가진 해는 아닙니다.
    print("\n5. Compare only accepted candidates on cost")
    for row in report["candidates"]:
        print(row["name"],"feasible",row["reference_feasible"],"cost",row["cost"],
              "residuals",row["reference_residuals"],"savings",row["savings_vs_baseline"])
    accepted = [r for r in report["candidates"] if r["reference_feasible"]]
    best = min(accepted,key=lambda r:r["cost"])
    print("lowest cost among revalidated candidates:",best["name"],best["cost"])
    assert all(r["savings_vs_baseline"] is None for r in report["candidates"] if not r["reference_feasible"])
    assert not report["benchmark"]["global_certificate"]

if __name__ == "__main__":
    main()
