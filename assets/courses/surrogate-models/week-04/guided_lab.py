"""Correct a prediction and differentiate through the correction.
예측을 보정하고 보정식으로 역전파하기
Run beside the lab files: python guided_lab.py
"""

def main():
    # %% 1. Spread the excess equally / 1. 초과량을 세 성분에 나누기
    # The raw sum is 0.70+0.45+0.25=1.40, exceeding feed by 0.20. In physical Euclidean distance, the smallest total squared correction subtracts 0.20/3 from every component. The sum then loses exactly 0.20.
    # 원래 합은 0.70+0.45+0.25=1.40으로 유입보다 0.20 큽니다. 물리 단위의 유클리드 거리에서 수정량 제곱합을 최소화하려면 각 성분에서 0.20/3을 뺍니다. 그러면 합이 정확히 0.20 줄어듭니다.
    print("\n1. Spread the excess equally")
    from pathlib import Path
    import numpy as np
    import torch
    import week04_lab as lab
    raw = torch.tensor([[.70,.45,.25]], dtype=torch.float64, requires_grad=True)
    feed = torch.tensor([[1.20]], dtype=torch.float64)
    excess = raw.sum(-1, keepdim=True)-feed
    corrected = lab.project(raw, feed)
    print("sum excess, correction per component:", excess.item(), excess.item()/3)
    print("projected:", corrected.detach().numpy())
    np.testing.assert_allclose(corrected.detach(), [[19/30,23/60,11/60]])
    np.testing.assert_allclose(corrected.detach().sum(1), [1.2])

    # %% 2. Trace one upstream gradient / 2. Upstream gradient 하나 따라가기
    # The first corrected output is rawA−(rawA+rawB+rawC−feed)/3. Its derivatives with respect to raw A/B/C are 2/3,−1/3,−1/3. Increasing B makes the common correction larger and therefore reduces the corrected A.
    # 첫 보정 출력은 rawA−(rawA+rawB+rawC−feed)/3입니다. raw A/B/C에 대한 미분은 2/3,−1/3,−1/3입니다. B가 커지면 공통으로 빼는 양이 커져 보정된 A가 줄어듭니다.
    print("\n2. Trace one upstream gradient")
    corrected[0,0].backward()
    print("raw gradient:", raw.grad.numpy())
    np.testing.assert_allclose(raw.grad, [[2/3,-1/3,-1/3]])
    checks = lab.mathematical_checks()
    print("projection checks:", checks)

    # %% 3. Find what equality does not control / 3. 합만으로 정해지지 않는 값 확인하기
    # Start from [0.02,0.90,0.50]. Its excess is 0.22, so subtracting 0.22/3 makes A negative. Clamping the negative component to zero adds mass without reducing another component. This is a concrete reason to inspect more than the sum residual.
    # [0.02,0.90,0.50]의 합 초과량은 0.22입니다. 각 성분에서 0.22/3을 빼면 A가 음수가 됩니다. 음수를 0으로 clamp하면 다른 성분을 줄이지 않은 채 총량만 늘어납니다. 그래서 합 residual 이외의 지표도 봅니다.
    print("\n3. Find what equality does not control")
    negative = lab.project(torch.tensor([[.02,.9,.5]], dtype=torch.float64), feed)
    clamped = negative.clamp(min=0)
    print("projected, minimum, clamped sum:", negative.tolist(), negative.min().item(), clamped.sum().item())
    assert negative.min() < 0 and clamped.sum() > feed.item()
    x = torch.tensor([[330.,5.,1.2]], dtype=torch.float64)
    truth = lab.reference(x)
    print("reference species balances:", lab.residuals(x, truth).tolist())
    print("projected species balances:", lab.residuals(x, corrected.detach()).tolist())

    # %% 4. Run the controlled comparison / 4. 같은 조건으로 네 방법 비교하기
    # Keep the 900/300/300 split, initialization, batch order, and minimum-validation-MSE selection fixed. The soft loss adds lambda times squared sum error; post-projection changes an already trained model, whereas hard training backpropagates through project. Test metrics use physical units.
    # 900/300/300 분할, 초기화, batch 순서, 최소 validation MSE 선택을 고정합니다. Soft loss는 합 오차 제곱에 lambda를 곱해 더합니다. 학습 후 투영은 완성 모델의 출력을 바꾸고 hard 학습은 project를 거쳐 역전파합니다. Test 지표는 물리 단위로 계산합니다.
    print("\n4. Run the controlled comparison")
    report = lab.run(Path("guided-results"), epochs=600, seed=404)
    for mode, metrics in report["test"].items():
        print(mode, "RMSE", metrics["rmse_all_mol_L"], "sum max", metrics["sum_max_mol_L"],
              "minimum", metrics["minimum_mol_L"], "species residual RMS", metrics["species_residual_rms_mol_L_min"])
    assert report["protocol"]["rows"] == [900,300,300]

if __name__ == "__main__":
    main()
