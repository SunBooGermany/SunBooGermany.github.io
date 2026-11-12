"""Follow an MLP update before training.
MLP 학습 한 번을 따라가기
Run beside the lab files: python guided_lab.py
"""

def main():
    # %% 1. Build three reference labels / 1. 기준 농도 세 개 만들기
    # At 330 K, k1=0.2/min and k2=0.1/min. Solve A first, then B using the A production term, then C using B. This triangular dependency explains the order of the three assignment statements.
    # 330 K에서 k1=0.2/min, k2=0.1/min입니다. A를 먼저 구하고, 그 A로 B 생성량을 구한 뒤 B로 C를 구합니다. 이 의존 관계 때문에 대입문도 A, B, C 순서입니다.
    print("\n1. Build three reference labels")
    from pathlib import Path
    import numpy as np
    import torch
    import week02_lab as lab
    xphysical = np.array([[330., 5., 1.2]])
    ca = 1.2/(1+.2*5)
    cb = .2*5*ca/(1+.1*5)
    cc = .1*5*cb
    print("CA, CB, CC:", ca, cb, cc)
    np.testing.assert_allclose(lab.steady_state(xphysical), [[ca, cb, cc]])
    np.testing.assert_allclose([ca, cb, cc], [.6, .4, .2])

    # %% 2. Inspect a tiny forward calculation / 2. 작은 신경망의 forward 확인하기
    # Use a two-neuron hidden layer to make each operation visible. The example input and target are dimensionless. Multiply the input by W1, apply ReLU, and combine hidden outputs with W2. ReLU sets negative preactivations to zero.
    # 계산이 보이도록 은닉 뉴런 두 개를 사용합니다. 이 예제의 입력과 target은 무차원입니다. W1을 곱하고 ReLU를 적용한 뒤 W2로 결합합니다. ReLU는 음수인 preactivation을 0으로 바꿉니다.
    print("\n2. Inspect a tiny forward calculation")
    x = torch.tensor([1., 0., -1.], dtype=torch.float64)
    target = torch.tensor([0., 1., 0.], dtype=torch.float64)
    w1 = torch.tensor([[1.,0.,0.],[0.,0.,1.]], dtype=torch.float64, requires_grad=True)
    b1 = torch.zeros(2, dtype=torch.float64, requires_grad=True)
    w2 = torch.tensor([[1.,0.],[0.,1.],[1.,1.]], dtype=torch.float64, requires_grad=True)
    b2 = torch.zeros(3, dtype=torch.float64, requires_grad=True)
    a = w1@x+b1
    h = torch.relu(a)
    prediction = w2@h+b2
    error = prediction-target
    loss = .5*(error**2).sum()
    print("a, h, prediction, error, loss:", a.tolist(), h.tolist(), prediction.tolist(), error.tolist(), loss.item())
    assert loss.item() == 1.5

    # %% 3. Trace the gradient and parameter update / 3. Gradient와 파라미터 갱신 추적하기
    # For half squared error, the output derivative is the residual. Multiplying by W2 transpose gives the hidden derivative; the ReLU gate then removes the second component. The first hidden derivative is 2, so its weight gradient is 2 times x. Move opposite to the gradient with learning rate 0.1.
    # 제곱 오차의 절반을 쓰면 출력 미분은 오차 벡터입니다. W2의 전치를 곱해 은닉층으로 전달한 뒤 ReLU의 비활성 성분을 0으로 만듭니다. 첫 은닉 미분이 2이므로 첫 가중치 행의 gradient는 2x입니다. 학습률 0.1로 gradient의 반대 방향으로 이동합니다.
    print("\n3. Trace the gradient and parameter update")
    loss.backward()
    print("dW1:", w1.grad.tolist(), "db1:", b1.grad.tolist())
    print("dW2:", w2.grad.tolist(), "db2:", b2.grad.tolist())
    np.testing.assert_allclose(w1.grad, [[2,0,-2],[0,0,0]])
    with torch.no_grad():
        for parameter in (w1,b1,w2,b2):
            parameter -= .1*parameter.grad
        after = w2@torch.relu(w1@x+b1)+b2
        after_loss = .5*((after-target)**2).sum()
    print("updated prediction and loss:", after.tolist(), after_loss.item())
    check = lab.backprop_example()
    np.testing.assert_allclose(after.tolist(), check["prediction_after"])
    assert after_loss.item() < loss.item()

    # %% 4. Scale, train, and read the physical errors / 4. Scaling·학습·물리 단위 오차 읽기
    # The actual network is 3→32→32→3: (3×32+32)+(32×32+32)+(32×3+3)=1283 parameters. Inputs use declared bounds; output means and standard deviations come only from training rows. Validation chooses the saved epoch; test rows assess that fixed model.
    # 실제 신경망은 3→32→32→3으로 파라미터가 (3×32+32)+(32×32+32)+(32×3+3)=1283개입니다. 입력은 선언한 영역으로, 출력은 train 평균·표준편차로 scaling합니다. Validation으로 저장할 epoch를 고른 뒤 고정 모델을 test로 평가합니다.
    print("\n4. Scale, train, and read the physical errors")
    splits = lab.generate_steady_splits(seed=42)
    tx, ty = splits["train"]
    print("input scaled first row:", (tx[0]-(lab.LOWER+lab.UPPER)/2)/((lab.UPPER-lab.LOWER)/2))
    print("output mean, scale:", ty.mean(0), ty.std(0))
    assert sum(p.numel() for p in lab.make_model(3).parameters()) == 1283
    report = lab.run_steady(Path("guided-results"), seed=42, epochs=1400)
    model, scaling = lab.load_model(Path("guided-results"), "steady-model")
    vx, truth = splits["test"]
    pred = lab.predict(model, scaling, vx)
    print("first three reference / prediction rows:", np.column_stack([truth[:3], pred[:3]]))
    manual_rmse = np.sqrt(np.mean((pred-truth)**2, axis=0))
    print("physical RMSE:", manual_rmse)
    np.testing.assert_allclose(manual_rmse, report["scaled_output_model"]["rmse_mol_L"])

if __name__ == "__main__":
    main()
