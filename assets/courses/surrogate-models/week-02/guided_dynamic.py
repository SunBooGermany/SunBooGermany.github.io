"""Optional dynamic preview: follow the state transitions.
선택 동적 미리보기: 상태전이 따라가기
Run beside the lab files: python guided_dynamic.py
"""

def main():
    # %% 1. Compare a rate with a finite-time change / 1. 변화율과 유한 시간 변화량 비교하기
    # Start from [1.2,0,0] mol/L at 330 K and tau=5 min. The A rate is (1.2−1.2)/5−0.2×1.2=−0.24 mol/(L min); B gains 0.24 and C initially has rate zero. Euler multiplies these initial rates by 0.2 min. The reference integrates rates as concentrations change within the interval.
    # 330 K, tau=5분에서 [1.2,0,0] mol/L로 시작합니다. A 변화율은 (1.2−1.2)/5−0.2×1.2=−0.24 mol/(L min)이고 B는 0.24만큼 늘며 C의 초기 변화율은 0입니다. Euler는 이 초기 변화율에 0.2분을 곱합니다. 기준 계산은 구간 중 농도가 변하면서 변화율도 달라지는 과정을 반영합니다.
    print("\n1. Compare a rate with a finite-time change")
    from pathlib import Path
    import numpy as np
    import week02_lab as cstr
    initial = np.array([[1.2, 0., 0.]])
    control = np.array([[330., 5., 1.2]])
    rate = cstr.concentration_rate(initial, control)
    euler = initial+.2*rate
    exact = cstr.reference_step(initial, control)
    print("initial rate:", rate[0], "Euler:", euler[0], "reference:", exact[0])
    np.testing.assert_allclose(euler, [[1.152, .048, 0]])
    np.testing.assert_allclose(exact[0,0], .6+.6*np.exp(-.4*.2))
    np.testing.assert_allclose(exact.sum(1), [1.2])

    # %% 2. Inspect the first three transitions / 2. 처음 세 상태전이 확인하기
    # Three input intervals require four state rows: the initial state and three successors. One-step evaluation repeatedly supplies the reference current state. Rollout supplies its own previous prediction after initialization. Keeping the weights and controls identical isolates this feedback difference.
    # 입력 구간 세 개에는 초기 상태를 포함해 상태 네 행이 필요합니다. One-step에는 매번 기준 현재 상태를 넣습니다. Rollout에는 초기화 이후 직전 예측을 넣습니다. 가중치와 입력 계획을 같게 유지하면 이 되먹임 차이를 비교할 수 있습니다.
    print("\n2. Inspect the first three transitions")
    model, scaling = cstr.load_model(Path("."), "dynamic-model")
    controls = np.tile(control[0], (3,1))
    truth = cstr.simulate_trajectory(controls, initial[0])
    one = cstr.dynamic_step(model, scaling, truth[:-1], controls)
    roll = cstr.rollout(model, scaling, controls, initial[0])
    for k in range(3):
        print("step", k+1, "reference input", truth[k], "rollout input", roll[k])
        print("next B: reference, one-step, rollout", truth[k+1,1], one[k,1], roll[k+1,1])
    assert truth.shape == roll.shape == (4,3)
    np.testing.assert_allclose(one[0], roll[1], atol=1e-7)

    # %% 3. Evaluate complete held-out trajectories / 3. 독립 궤적 전체 평가하기
    # Split entire trajectories, rather than adjacent rows from the same trajectory, to avoid sharing a process history between training and test. There are 60/15/20 trajectories with 150 intervals each. Exclude the supplied initial state from error averages: it was not predicted.
    # 인접 행을 나누는 대신 궤적 전체를 train·validation·test로 나눠 같은 공정 이력이 양쪽에 섞이지 않게 합니다. 궤적은 60/15/20개이고 각 150구간입니다. 주어진 초기 상태는 예측값이 아니므로 오차 평균에서 제외합니다.
    print("\n3. Evaluate complete held-out trajectories")
    trajectories = cstr.generate_trajectories(seed=42)
    inputs, increments = cstr.transition_data(trajectories["test"])
    one = cstr.dynamic_step(model,scaling,inputs[:,:3],inputs[:,3:])
    predictions = [cstr.rollout(model,scaling,t["controls"],t["states"][0]) for t in trajectories["test"]]
    truth_all = np.concatenate([t["states"][1:] for t in trajectories["test"]])
    pred_all = np.concatenate([t[1:] for t in predictions])
    feed = np.concatenate([t["controls"][:,2] for t in trajectories["test"]])
    metrics = {"one_step":cstr.prediction_metrics(inputs[:,:3]+increments,one,inputs[:,-1]),
               "rollout":cstr.prediction_metrics(truth_all,pred_all,feed)}
    manual = np.sqrt(np.mean((pred_all-truth_all)**2,axis=0))
    np.testing.assert_allclose(manual,metrics["rollout"]["rmse_mol_L"])
    assert len(truth_all)==3000
    print("one-step and rollout metrics:",metrics)
    out = Path("guided-results");out.mkdir(exist_ok=True)
    cstr.write_json(out/"dynamic-preview-results.json",metrics)
    cstr.dynamic_figures(out,trajectories["test"],predictions,metrics["one_step"]["rmse_mol_L"])

    # %% 4. Change the initial state, keep the future plan / 4. 미래 입력을 고정하고 초기 상태 바꾸기
    # Use [0.2,0.8,0.2] mol/L instead of pure A. This changes the transient while preserving total concentration. Keep the same 150-interval 330 K plan so that the effect comes from initial state, not a new control sequence.
    # 순수 A 대신 [0.2,0.8,0.2] mol/L를 사용합니다. 농도 합은 같고 과도응답이 바뀝니다. 150구간의 330 K 계획은 그대로 두어 초기 상태의 영향만 비교합니다.
    print("\n4. Change the initial state, keep the future plan")
    controls = np.tile([330.,5.,1.2], (150,1))
    new_initial = np.array([.2,.8,.2])
    changed_truth = cstr.simulate_trajectory(controls, new_initial)
    changed_pred = cstr.rollout(model, scaling, controls, new_initial)
    print("B at 0, 0.2, 30 min:", changed_truth[[0,1,-1],1])
    print("changed-state metrics:", cstr.prediction_metrics(changed_truth[1:], changed_pred[1:], controls[:,2]))
    np.testing.assert_allclose(changed_truth.sum(1), 1.2, atol=1e-12)

if __name__ == "__main__":
    main()
