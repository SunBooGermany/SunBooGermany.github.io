"""Explain bounds before comparing solvers.
Bounds의 의미를 확인하고 정식화 비교하기
Run beside the lab files: python guided_lab.py
"""

def main():
    # %% 1. Propagate signs through one affine bound / 1. Affine bound에서 부호 따라가기
    # For a=2x1−3x2+0.5 and x1,x2∈[0,1], the smallest value uses x1=0,x2=1; the largest uses x1=1,x2=0. Positive weights multiply lower bounds for a lower estimate; negative weights multiply upper bounds. This is the calculation performed layer by layer.
    # a=2x1−3x2+0.5, x1,x2∈[0,1]이면 최솟값은 x1=0,x2=1에서, 최댓값은 x1=1,x2=0에서 나옵니다. 하한을 구할 때 양의 가중치에는 입력 하한을, 음의 가중치에는 입력 상한을 곱합니다. 이 계산을 층마다 반복합니다.
    print("\n1. Propagate signs through one affine bound")
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

    # %% 2. Explain the two-neuron relaxation gap / 2. 두 뉴런의 완화 차이 설명하기
    # The toy model has x1+x2=1, so a0=x1+x2−1=0 exactly. The other activation is max(0,x1−x2)=max(0,2x1−1). Requiring total activation ≥0.4 gives the exact solution x1≥0.7. A loose LP can inflate activations; fixing the first activation to zero removes one source of inflation.
    # 작은 예제에서 x1+x2=1이므로 a0=x1+x2−1=0입니다. 다른 활성값은 max(0,x1−x2)=max(0,2x1−1)입니다. 활성값 합을 0.4 이상 요구하면 정확한 모델에서는 x1≥0.7입니다. 느슨한 LP는 활성값을 부풀릴 수 있고 첫 활성값을 0으로 고정하면 그 여지가 줄어듭니다.
    print("\n2. Explain the two-neuron relaxation gap")
    toy = {}
    for tight in [False,True]:
        for relax in [True,False]:
            result = lab.toy_case(tight,relax)
            toy[tight,relax] = result["objective"]
            print("tight, LP, objective:", tight,relax,result["objective"])
    np.testing.assert_allclose([toy[False,True],toy[True,True],toy[True,False]], [0,.4,.7], atol=1e-7)

    # %% 3. Follow physical scaling and layer outputs / 3. 물리 입력 scaling과 층별 출력 확인하기
    # At [330 K,6 min], subtract [310,2] and divide by [40,8] to obtain [0.5,0.5]. Each saved weight matrix maps a row of activations to the next layer. Apply ReLU only where the layer metadata says relu; the output layer stays linear.
    # [330 K,6분]에서 [310,2]를 빼고 [40,8]로 나누면 [0.5,0.5]입니다. 저장된 가중치 행렬은 활성값 한 행을 다음 층으로 옮깁니다. Metadata가 relu인 층에만 ReLU를 적용하고 출력층은 선형으로 둡니다.
    print("\n3. Follow physical scaling and layer outputs")
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

    # %% 4. Compare complete reports, including failures / 4. 실패 상태까지 포함해 보고서 비교하기
    # The full run compares loose, interval, LP-tightened, and OMLT formulations using identical coefficients. LP-OBBT solves auxiliary LPs to bound each preactivation over the declared input domain. Record bound computation, model construction, and solve time separately.
    # 전체 실행은 같은 계수로 느슨한 bounds, 구간 전파, LP 강화, OMLT를 비교합니다. LP-OBBT는 입력 영역에서 보조 LP를 풀어 각 preactivation의 범위를 구합니다. Bound 계산·모델 구성·solver 시간을 나눠 기록합니다.
    print("\n4. Compare complete reports, including failures")
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

if __name__ == "__main__":
    main()
