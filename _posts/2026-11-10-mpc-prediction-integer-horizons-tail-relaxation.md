---
layout: post
title: "Predict Far Ahead, Keep Integer Decisions Near Term"
title_ko: "멀리 예측하되, 정수 결정은 가까운 미래에 집중하기"
date: 2026-11-10
category: stochastic-nonlinear-optimization
category_label: "Mathematical Optimization"
research_group: algorithmic_reviews
research_category: stochastic-nonlinear-optimization
research_category_label: "Mathematical Optimization"
application_category: ""
application_category_label: ""
method_category: "stochastic-nonlinear-optimization"
method_category_label: "Mathematical Optimization"
paper_title: "Real-Time Nonlinear Mixed-Integer Model Predictive Control With Horizon-Tail Relaxations"
authors: "Armin Nurkanović"
venue: "arXiv preprint"
year: "2026"
doi: "10.48550/arXiv.2611.09187"
arxiv: "2611.09187v1"
source_url: "https://arxiv.org/abs/2611.09187v1"
tags:
  - "model predictive control"
  - "mixed-integer optimization"
  - "horizon-tail relaxation"
  - "energy systems"
excerpt: "Separate the prediction horizon from the integer horizon: retain a long look ahead while relaxing distant on/off decisions to reduce computation."
excerpt_ko: "예측기간은 길게 유지하면서 가까운 미래의 on/off만 정수로 결정하고, 먼 미래에는 연속 완화를 허용해 계산 부담을 줄이는 아이디어."
language: "en-ko"
has_korean_note: false
---

Operating chillers or electrolyzers requires looking far enough ahead to account for future demand and storage levels. Yet choosing every on/off decision as an integer over that entire horizon can make optimization expensive. Can we retain the long view while shortening the interval over which we search for on/off combinations?

Nurkanović’s [study of horizon-tail relaxations](https://arxiv.org/abs/2611.09187v1) offers an intuitive approach: **predict far ahead, but concentrate integer decisions on the near future.** Allow continuous relaxations of distant on/off decisions, then recompute the plan when the next measurement arrives.

## 1. Separate the prediction horizon from the integer horizon

Call the full look-ahead length the prediction horizon N, and the initial interval that retains integrality the integer horizon M. Within M, each on/off input must be either 0 or 1.

Consider three chillers controlled at three-minute intervals with a 90-minute prediction horizon. Here N is 30. Keeping every on/off decision binary requires 30 decisions per chiller, giving 90 binary variables in total.

With M set to 5, each chiller must be either on or off during the first 15 minutes. Over the remaining 75 minutes, its input may take any value between 0 and 1.

| Formulation | First 15 minutes | Remaining 75 minutes |
|---|---|---|
| Integrality over the full horizon | On/off decisions are 0 or 1 | On/off decisions are 0 or 1 |
| Relaxed tail integrality | On/off decisions are 0 or 1 | Continuous values between 0 and 1 are allowed |

The controller still looks 90 minutes ahead, but the number of freely optimized binary variables falls from 90 to 15. Continuous variables and constraints remain over the full horizon, so runtime need not fall in the same proportion. The reduction targets the combinatorial search.

## 2. Keep the distant future in the calculation

Shortening the prediction horizon itself to 15 minutes would make it harder to account for demand or temperature changes beyond that point. Tail relaxation keeps the distant costs, dynamics, and constraints in the approximate problem while relaxing integrality there. The distant future still influences the current decision.

A future chiller input might therefore be 0.4. This is a relaxed value allowed for computational purposes; it is not automatically equivalent to running the equipment for 40% of that interval. The first input actually applied comes from the initial integer interval, so it is on or off.

MPC does not execute the entire plan at once. It applies the first input and optimizes again using the next measurement. As time advances, a previously relaxed interval enters the near-term integer horizon. This repeated planning structure reduces the need to search over every distant on/off combination at every update.

The appealing idea is to treat N and M as separate design choices. How far ahead should the controller look? How far ahead should it retain binary on/off decisions? Those lengths can be chosen independently. The paper also studies fixing the tail to a previously obtained binary plan; the focus here is on relaxing integrality while leaving future operating choices open.

## 3. Reduce computation after the measurement arrives

The paper combines this idea with advance computation. Before a measurement arrives, the controller solves a continuous relaxation at a predicted state and prepares a mixed-integer quadratic program (MIQP). After the measurement, it updates the initial state and solves the MIQP to choose near-term on/off decisions together with continuous inputs.

In a three-chiller simulation with N = 30 and M = 5, the continuous-tail variant computed feedback 15.56 times faster on average than full AS-MINMPC, which retains integrality over the entire horizon. Closed-loop cost increased by 0.27%. This comparison illustrates the effect of combining long predictions with a short integer horizon within the same experiment. The reported time is the feedback computation after the measurement arrives. [Paper, §V](https://arxiv.org/html/2611.09187v1#S5)

## Reference

Nurkanović, A. (2026). *Real-time nonlinear mixed-integer model predictive control with horizon-tail relaxations*. arXiv, 2611.09187v1. [Paper](https://arxiv.org/abs/2611.09187v1) · [DOI](https://doi.org/10.48550/arXiv.2611.09187) · [Code](https://github.com/nosnoc/advanced-minmpc)

<!-- ko -->

냉동기나 전해조를 운전할 때는 앞으로의 수요와 저장량을 충분히 멀리 내다봐야 합니다. 그런데 예측기간 전체에서 설비를 언제 켜고 끌지까지 정수변수로 결정하면 계산 부담이 빠르게 커집니다. 멀리 보는 능력을 유지하면서 on/off 조합을 탐색하는 구간만 줄일 수 있을까요?

Nurkanović의 [horizon-tail relaxation 연구](https://arxiv.org/abs/2611.09187v1)는 이 질문에 직관적인 접근을 제시합니다. **예측은 멀리까지 하되, 정수 결정은 가까운 미래에 집중합니다.** 먼 미래의 on/off에는 연속 완화를 허용하고, 새 측정값이 들어오면 계획을 다시 계산하는 방식입니다.

## 1. 예측기간과 정수 결정 구간을 따로 정하기

여기서는 전체를 내다보는 길이를 prediction horizon N, 앞부분에서 정수성을 유지하는 길이를 integer horizon M이라고 부르겠습니다. M은 on/off를 실제 0 또는 1로 선택하는 구간입니다.

냉동기 3대의 운전을 3분 간격으로 결정하고, 앞으로 90분을 예측한다고 해봅시다. N은 30입니다. 전체 구간에서 정수성을 유지하면 냉동기마다 30개의 on/off 결정이 필요하므로 이진변수는 총 90개가 됩니다.

이때 M을 5로 정하면 가까운 15분에는 각 냉동기를 켤지 끌지 0 또는 1로 결정하고, 나머지 75분에는 0과 1 사이의 값을 허용합니다.

| 구분 | 가까운 15분 | 이후 75분 |
|---|---|---|
| 전체 구간의 정수성을 유지 | on/off를 0 또는 1로 결정 | on/off를 0 또는 1로 결정 |
| Tail의 정수성을 완화 | on/off를 0 또는 1로 결정 | 0과 1 사이의 연속값 허용 |

예측은 여전히 90분 앞까지 이어지지만, 자유롭게 탐색하는 이진변수는 90개에서 15개로 줄어듭니다. 전체 기간의 연속변수와 제약은 남아 있으므로 계산시간이 같은 비율로 줄어드는 것은 아니어도, 정수 조합 탐색의 부담을 줄일 수 있습니다.

## 2. 먼 미래를 지우지 않고 계산하기 쉽게 만들기

예측기간 자체를 15분으로 줄이면 그 이후의 수요나 온도 변화를 고려하기 어렵습니다. Tail relaxation은 먼 구간의 비용과 동역학·제약을 근사문제에 계속 포함하면서, 그 구간의 정수성만 풉니다. 먼 미래가 현재 결정에 미치는 영향은 남겨두는 셈입니다.

예를 들어 미래의 냉동기 입력이 0.4로 계산될 수 있습니다. 이는 계산을 쉽게 하려고 허용한 완화값이며, 실제 설비를 그 시간의 40%만 가동하는 것과 자동으로 같아지는 것은 아닙니다. 당장 적용하는 첫 입력은 앞쪽 정수 구간에서 선택하므로 on 또는 off입니다.

MPC는 계획 전체를 한 번에 실행하지 않습니다. 첫 입력을 적용한 뒤 다음 측정값으로 다시 최적화합니다. 시간이 흐르면 이전에 완화했던 먼 구간도 가까운 정수 결정 구간으로 들어옵니다. 이 반복 구조 덕분에 아직 먼 시점의 on/off를 매번 모두 정수로 탐색해야 하는 부담을 줄일 수 있습니다.

이 연구에서 흥미로운 점은 N과 M을 별개의 설계변수로 본다는 데 있습니다. “얼마나 멀리 볼 것인가”와 “어디까지 on/off를 정수로 결정할 것인가”를 각각 정할 수 있습니다. 논문은 tail을 미리 구한 이진 계획으로 고정하는 방식도 다루지만, 여기서는 미래 운전의 선택지를 열어둔 채 정수성을 완화하는 접근에 주목합니다.

## 3. 측정 후 계산을 줄이는 구성

논문은 이 아이디어를 사전 계산과 결합합니다. 측정값이 도착하기 전에 예측 상태에서 연속 완화 문제를 풀고, 이를 바탕으로 혼합정수 이차계획(MIQP)을 준비합니다. 측정 후에는 초기 상태를 갱신한 MIQP에서 가까운 미래의 on/off와 연속 입력을 함께 결정합니다.

냉동기 3대의 시뮬레이션에서 N = 30, M = 5인 tail 연속 완화 방식은 전체 구간의 정수성을 유지한 AS-MINMPC보다 평균 피드백 계산이 15.56배 빨랐고, 폐루프 비용은 0.27% 증가했습니다. 같은 실험 안에서 긴 예측과 짧은 정수 탐색을 결합한 효과를 보여주는 비교입니다. 이 시간은 측정 후 입력을 계산하는 피드백 시간입니다. [논문 §V](https://arxiv.org/html/2611.09187v1#S5)

## 참고문헌

Nurkanović, A. (2026). *Real-time nonlinear mixed-integer model predictive control with horizon-tail relaxations*. arXiv, 2611.09187v1. [논문](https://arxiv.org/abs/2611.09187v1) · [DOI](https://doi.org/10.48550/arXiv.2611.09187) · [공개 코드](https://github.com/nosnoc/advanced-minmpc)
