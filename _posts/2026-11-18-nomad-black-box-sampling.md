---
layout: post
title: "After 30 black-box evaluations, how does NOMAD choose point 31?"
title_ko: "블랙박스 함수를 30번 평가했다면, NOMAD는 31번째 점을 어떻게 고를까?"
date: 2026-11-18
category: llm-probabilistic-approaches
category_label: "LLM & Probabilistic Approaches"
research_group: algorithmic_reviews
research_category: llm-probabilistic-approaches
research_category_label: "LLM & Probabilistic Approaches"
application_category: ""
application_category_label: ""
method_category: "llm-probabilistic-approaches"
method_category_label: "LLM & Probabilistic Approaches"
paper_title: "Algorithm 1027: NOMAD Version 4: Nonlinear Optimization with the MADS Algorithm"
authors: "Charles Audet, Sébastien Le Digabel, Viviane Rochon Montplaisir, Christophe Tribes"
venue: "ACM Transactions on Mathematical Software"
year: "2022"
doi: "10.1145/3544489"
arxiv: "2104.11627"
source_url: "https://arxiv.org/abs/2104.11627"
tags:
  - "NOMAD"
  - "MADS"
  - "derivative-free optimization"
  - "quadratic models"
  - "black-box sampling"
excerpt: "With 30 samples in hand, NOMAD can fit a local model to propose the next evaluation. When does one Search call save work in Poll?"
excerpt_ko: "블랙박스 함수의 평가값 30개로 다음 점을 고르는 과정을 따라가며, Search에 쓴 평가 한 번이 어떤 조건에서 Poll 비용을 줄이는지 계산합니다."
language: "en-ko"
has_korean_note: false
---

Suppose we have sampled a black-box function *f* at 30 points. The smallest value we have seen is 8.0. We have no formula or gradient, only the input points and their function values. If each evaluation is expensive, where should we take sample 31?

NOMAD solves black-box optimization problems like this using Mesh Adaptive Direct Search (MADS). MADS places a mesh over the input space and chooses trial points on that mesh. During **Search**, it can use previous evaluations to propose a promising point. If Search is omitted or finds no improvement, **Poll** explores a set of directions around the best point so far. If neither step finds an improvement, the next iteration starts on a finer mesh. [Audet and Dennis on MADS](https://doi.org/10.1137/040603371)

## How does a quadratic model help choose a point?

Consider the samples among the first 30 that lie near the current best point. If the function falls and then rises along one direction, a quadratic model can approximate that curvature. With `QUAD_MODEL_SEARCH`, NOMAD fits a model to past evaluations, looks for coordinates where the predicted value is low, and projects them onto the current mesh to generate Search candidates. Comparing coordinates on the model costs no extra black-box calls. [NOMAD 4 implementation paper, Section 3.3](https://arxiv.org/abs/2104.11627)

Poll first generates nearby candidates using a set of directions and a step size. The model can help here too. Setting `EVAL_QUEUE_SORT` to `QUADRATIC_MODEL` lets the quadratic model order those candidates for evaluation. With `EVAL_OPPORTUNISTIC` enabled and points evaluated one at a time, an early improvement saves the calls for the remaining points. [NOMAD 4 user guide](https://nomad-4-user-guide.readthedocs.io/en/latest/AdvancedFunctionalities.html)

## Which of A, B, and C do we actually evaluate?

Suppose the best value so far is 8.0, all candidates are feasible, and A is the only Search candidate. The iteration ends at the first improvement.

| Step | Reason for choosing the point | Model prediction | Black-box value | Decision |
| --- | --- | ---: | ---: | --- |
| Search · A | New point proposed by the quadratic model | 7.3 | 8.2 | Keep 8.0 and proceed to Poll. |
| Poll · B | Lower predicted value than Poll candidate C, so B goes first | 7.6 | 7.9 | Adopt B as the new center. |
| Poll · C | Next in the evaluation queue | 7.8 | Unevaluated | End Poll because B improved the incumbent. |

The model predicted 7.3 at A, but the black box returned 8.2. Had it returned 7.3, NOMAD could have accepted A and skipped Poll for this iteration. Accepting B does not require knowing the value at C. The observed value of 7.9 at B already improves on 8.0.

## Is Search worth one evaluation?

Consider a separate cost comparison. Going straight to Poll takes four black-box calls. Trying Search first costs one call. Success ends the iteration, while failure adds four Poll calls. Let *p* be the probability that a single Search candidate improves the observed best value under comparable conditions. The 7.3 in the table predicts the function value at A. That number alone does not tell us *p*.

The expected count with Search first is *p* × 1 + (1 − *p*) × 5 = 5 − 4*p*. This equals the four calls for Poll alone at *p* = 0.25. One success in four attempts saves three calls, exactly covering the extra call spent on each of the three failures. Search reduces the average calls per iteration **when its success rate exceeds 25%**.

Early stopping in Poll changes the calculation. Suppose Poll averages two calls both when used directly and when reached after a failed Search. Search then saves calls if 1 + 2(1 − *p*) < 2, so its success rate must **exceed 50%**. To make this comparison from evaluation logs, count Poll calls separately in the two cases. If Poll takes more calls in iterations where Search fails, using the overall Poll average will understate the cost of failure.

<!-- ko -->

블랙박스 함수 *f*를 30개 점에서 평가했고, 지금까지 가장 작은 값은 8.0이라고 합시다. 함수식이나 기울기는 알 수 없습니다. 손에 있는 것은 각 입력점과 그 점에서 얻은 함수값뿐입니다. 평가 한 번에 비용이 많이 든다면 31번째 점은 어디에 찍는 게 좋을까요?

NOMAD는 이런 블랙박스 최적화 문제를 푸는 소프트웨어입니다. NOMAD가 구현한 MADS(Mesh Adaptive Direct Search)는 입력 공간에 격자를 두고, 그 위에서 다음 평가점을 고릅니다. **Search**에서는 과거 평가 결과를 이용해 유망한 점을 제안할 수 있습니다. Search를 생략하거나 개선점을 찾지 못하면 **Poll**에서 현재 최선점 주변을 정해진 방향으로 살핍니다. 두 단계 모두 개선점을 찾지 못하면 격자를 더 촘촘하게 만들어 다음 반복을 시작합니다. [Audet과 Dennis의 MADS 논문](https://doi.org/10.1137/040603371)

## 이차모델로 어느 점을 고를까?

30개 평가점 중 현재 최선점 주변에 있는 점들을 봅시다. 한 방향으로 움직일 때 함수값이 처음에는 내려가다가 다시 올라간다면, 이차모델로 그 곡률을 근사할 수 있습니다. NOMAD의 `QUAD_MODEL_SEARCH`는 과거 평가값에 맞춘 모델에서 작은 값이 예상되는 좌표를 찾고, 현재 격자에 맞춰 Search 후보를 만듭니다. 모델 위에서 여러 좌표를 비교해도 블랙박스 호출은 늘지 않습니다. [NOMAD 4 구현 논문, 3.3절](https://arxiv.org/abs/2104.11627)

Poll에서는 방향과 보폭으로 주변 후보를 먼저 만듭니다. 이때도 모델을 쓸 수 있습니다. `EVAL_QUEUE_SORT`를 `QUADRATIC_MODEL`로 설정하면 이미 만든 후보 중 어디부터 평가할지 이차모델로 정합니다. `EVAL_OPPORTUNISTIC`을 켜고 한 점씩 평가한다면, 앞쪽에서 개선점을 찾을수록 남은 후보를 평가하는 비용을 아낍니다. [NOMAD 4 사용자 안내서](https://nomad-4-user-guide.readthedocs.io/en/latest/AdvancedFunctionalities.html)

## A, B, C 중 실제로 평가하는 점은?

현재 최선값은 8.0이고 모든 후보가 제약을 만족한다고 합시다. Search 후보는 A 하나이며, 개선점을 찾으면 이번 반복을 끝냅니다.

| 단계 | 후보를 고른 이유 | 모델 예측값 | 블랙박스 함수값 | 결정 |
| --- | --- | ---: | ---: | --- |
| Search · A | 이차모델이 새로 제안한 점 | 7.3 | 8.2 | 8.0을 유지하고 Poll로 넘어갑니다. |
| Poll · B | Poll 후보 중 C보다 예측값이 낮아 먼저 평가 | 7.6 | 7.9 | B를 새 중심점으로 채택합니다. |
| Poll · C | B 다음에 평가할 점 | 7.8 | 미평가 | B에서 개선점을 찾았으므로 Poll을 끝냅니다. |

A의 예측값은 7.3이었지만 블랙박스가 돌려준 값은 8.2였습니다. 같은 점에서 실제로 7.3을 얻었다면 A를 채택하고 이번 Poll을 건너뛰었을 겁니다. B를 채택하는 데에는 C의 함수값까지 알 필요가 없습니다. B에서 얻은 7.9만으로도 현재 최선값 8.0을 개선했기 때문입니다.

## Search에 평가 한 번을 쓸 만한가?

이제 비용을 따로 계산해 봅시다. 바로 Poll을 하면 블랙박스를 4번 호출한다고 가정합니다. Search를 먼저 하면 1번 호출하고, 성공하면 그 자리에서 반복을 끝냅니다. 실패하면 Poll에 4번이 더 듭니다. 여기서 *p*는 비슷한 조건에서 Search 후보 하나가 실제 최선값을 개선할 확률입니다. 표의 7.3은 A에서 예상한 함수값이므로, 그 숫자만으로 *p*를 알 수는 없습니다.

Search를 먼저 할 때 평균 호출 수는 *p* × 1 + (1 − *p*) × 5 = 5 − 4*p*입니다. 바로 Poll을 하는 비용 4와 같아지는 지점은 *p* = 0.25입니다. 네 번 중 한 번 성공하면 그때 아낀 3회가 나머지 세 번에 한 회씩 더 쓴 비용을 메웁니다. 따라서 **성공률이 25%를 넘어야** 한 반복당 평균 호출 수가 줄어듭니다.

Poll도 일찍 끝난다면 기준은 달라집니다. 바로 Poll을 할 때와 Search 실패 후 Poll을 할 때 모두 평균 2회가 든다고 합시다. 그러면 1 + 2(1 − *p*) < 2를 만족해야 하므로 Search 성공률이 **50%를 넘어야** 합니다. 실제 평가 기록으로 비교할 때는 두 경우의 Poll 비용을 따로 집계해야 합니다. Search가 실패한 반복에서 Poll에도 호출이 더 많이 들었다면, 전체 Poll 평균을 그대로 대입하면 실패 비용을 낮게 잡게 됩니다.
