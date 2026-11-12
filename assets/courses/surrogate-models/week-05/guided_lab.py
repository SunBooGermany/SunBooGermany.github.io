"""Build and check a ReLU MILP.
ReLU MILP를 만들고 대조하기
Run beside the lab files: python guided_lab.py
"""

def main():
    # %% 1. Follow scaling, hinges, and output contributions / 1. Scaling·hinge·출력 기여량 따라가기
    # Five reference knots at 2,4,6,8,10 min define linear interpolation. Scale tau by x=(tau−2)/8. Each hidden unit turns on after one threshold; its weight changes the output slope. At tau=5, only the first two hinges are active.
    # 2,4,6,8,10분의 기준값 다섯 개 사이를 선형으로 잇습니다. x=(tau−2)/8로 scaling합니다. 각 은닉 뉴런은 문턱을 넘으면 켜지고 가중치만큼 출력 기울기를 바꿉니다. tau=5에서는 처음 두 hinge만 켜집니다.
    print("\n1. Follow scaling, hinges, and output contributions")
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

    # %% 2. Read one matrix row as a constraint / 2. 행렬 한 행을 제약으로 읽기
    # Variables are [x,h0,h1,h2,h3,yA,yB,yC,z1,z2,z3]. The first row h0−x=0 encodes the always-active hinge. For threshold 0.25, preactivation a=x−0.25 lies in [−0.25,0.75]. Binary z selects inactive h=0 or active h=a through the two upper bounds and h≥a,h≥0.
    # 변수 순서는 [x,h0,h1,h2,h3,yA,yB,yC,z1,z2,z3]입니다. 첫 행 h0−x=0은 항상 활성인 hinge를 나타냅니다. 문턱 0.25인 뉴런의 a=x−0.25는 [−0.25,0.75] 안에 있습니다. 이진 z가 두 상한과 h≥a,h≥0을 이용해 비활성 h=0 또는 활성 h=a를 선택합니다.
    print("\n2. Read one matrix row as a constraint")
    c, integrality, bounds, constraint = lab.formulate(net)
    print("first row:", constraint.A[0], "row limits:", constraint.lb[0], constraint.ub[0])
    print("binary positions:", np.flatnonzero(integrality))
    fixed = lab.solve(net, fixed_tau=5., specifications=False)
    v = fixed.x
    print("fixed solution [x,h,y,z]:", v)
    print("all row values:", constraint.A@v)
    np.testing.assert_allclose(v[1:5], h, atol=1e-8)
    np.testing.assert_allclose(v[5:8], y, atol=1e-8)

    # %% 3. Optimize, restore the objective constant, and recheck / 3. 최적화 후 목적함수 상수를 복원하고 재검증하기
    # The solver minimizes 8x; adding the omitted constant 2 gives residence time. Recompute outputs using forward at the returned tau and then the process reference. The first comparison checks implementation; the second checks the selected process condition.
    # Solver는 8x를 최소화하므로 생략한 상수 2를 더해야 체류시간이 됩니다. 반환된 tau에서 forward를 다시 계산하고 공정 기준식도 계산합니다. 첫 비교는 구현을, 두 번째는 선택한 공정 조건을 검사합니다.
    print("\n3. Optimize, restore the objective constant, and recheck")
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

    # %% 4. Explain an infeasible result / 4. Infeasible 결과 설명하기
    # Raise only the B lower bound to 0.41 and keep C≤0.25. B peaks at about 0.410256 at 8 min, but C there exceeds its limit. C increases across all knots and reaches 0.25 between 6 and 8 min. Interpolate that crossing first; then read the largest B allowed before it.
    # B 하한만 0.41로 높이고 C≤0.25를 유지합니다. B는 8분에서 약 0.410256으로 최대이지만 그때 C가 상한을 넘습니다. C는 모든 knot에서 증가하고 6~8분 사이에 0.25가 됩니다. 먼저 이 교점을 보간한 뒤 그 이전에서 허용되는 최대 B를 읽습니다.
    print("\n4. Explain an infeasible result")
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

if __name__ == "__main__":
    main()
