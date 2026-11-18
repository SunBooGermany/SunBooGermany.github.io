---
layout: post
title: "How NOMAD chooses the next Aspen run"
title_ko: "Aspen을 30번 돌린 뒤, NOMAD는 다음 운전점을 어떻게 고를까?"
date: 2026-11-18
category: stochastic-nonlinear-optimization
category_label: "Mathematical Optimization"
research_group: algorithmic_reviews
research_category: stochastic-nonlinear-optimization
research_category_label: "Mathematical Optimization"
application_category: ""
application_category_label: ""
method_category: "stochastic-nonlinear-optimization"
method_category_label: "Mathematical Optimization"
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
  - "Aspen"
excerpt: "A carbon capture example traces a quadratic Search proposal, an early stop in Poll, and the success rate needed to save simulator calls."
excerpt_ko: "탄소 포집 공정에서 이차모델이 제안한 운전점을 Aspen으로 평가하고, Search를 먼저 하면 몇 번의 호출을 아낄 수 있는지 계산합니다."
language: "en-ko"
has_korean_note: false
---

Suppose Aspen has evaluated 30 operating points for a carbon capture process. Among the points that met the capture target, the lowest regenerator heat duty was 8.0. For run 31, should we adjust the solvent circulation rate slightly from that point? Or do the heat duties from the first 30 runs suggest a more promising set of operating conditions?

NOMAD solves problems like this without derivatives of the objective or constraints. It sends operating conditions to Aspen and receives a heat duty and a capture rate. NOMAD implements Mesh Adaptive Direct Search (MADS), which chooses trial points on a mesh. If an iteration finds no improvement, MADS refines the mesh so it can explore the neighborhood at a smaller scale. [Audet and Dennis on MADS](https://doi.org/10.1137/040603371)

## Using a model to choose a point or order evaluations

During Search, previous evaluations can provide a local approximation to heat duty. Suppose duty falls as circulation increases, then starts rising again. A quadratic model can represent that curvature. With `QUAD_MODEL_SEARCH`, NOMAD looks for promising coordinates on the model and projects them onto the current mesh to generate trial points. Comparing coordinates on the model costs no additional Aspen runs. [NOMAD 4 implementation paper, Section 3.3](https://arxiv.org/abs/2104.11627)

If Search is omitted or finds no improvement, the iteration proceeds to Poll. Poll generates nearby mesh points using a set of directions and a step size around the current point. Setting `EVAL_QUEUE_SORT` to `QUADRATIC_MODEL` allows model predictions to determine which of these candidates gets evaluated first. With `EVAL_OPPORTUNISTIC` enabled and evaluations run one at a time, an improvement can save the calls for the remaining candidates. [NOMAD 4 user guide](https://nomad-4-user-guide.readthedocs.io/en/latest/AdvancedFunctionalities.html)

## Why reject A when its predicted heat duty is 7.3?

Consider one hypothetical iteration. The best heat duty so far is 8.0, all candidates satisfy the capture constraint, and A is the only Search candidate.

| Step | Reason for choosing the point | Predicted duty | Aspen duty | Decision |
| --- | --- | ---: | ---: | --- |
| Search · A | Operating point proposed by the quadratic model | 7.3 | 8.2 | Keep 8.0 and proceed to Poll. |
| Poll · B | Lower predicted duty among the Poll candidates, so B goes first | 7.6 | 7.9 | Duty falls by 0.1. Adopt B as the new center. |
| Poll · C | Next in the evaluation queue | 7.8 | Unevaluated | Poll ended at B. |

The model predicted a reduction of 0.7 at A. Aspen returned an increase of 0.2. Had Aspen returned 7.3 as predicted, NOMAD could have accepted A and skipped Poll for this iteration. C raises a different question. Could its heat duty have been even lower than B’s? We never evaluated C, so its duty is unknown. Under this stopping rule, one verified improvement over 8.0 is enough to end the iteration.

## Is Search worth one Aspen call?

Consider a separate cost comparison. Going straight to Poll takes four Aspen calls. Trying Search first costs one call. Let *p* be the probability that this call finds an improvement. Success ends the iteration after one call. Failure adds four Poll calls, bringing the total to five.

The expected count with Search first is *p* × 1 + (1 − *p*) × 5 = 5 − 4*p*. This equals the four calls for Poll alone at *p* = 0.25. One success in four attempts saves three calls, exactly covering the extra call spent on each of the three failures. Search reduces the average calls per iteration **when its success rate exceeds 25%**.

Early stopping in Poll changes the calculation. Suppose Poll averages two calls both when used directly and when reached after a failed Search. Search then saves calls if 1 + 2(1 − *p*) < 2, so its success rate must **exceed 50%**. To make this comparison from run logs, count Poll calls separately in the two cases. If Poll takes longer under the conditions where Search fails, its overall average cannot stand in for the cost after failure.

<!-- ko -->

Aspen으로 탄소 포집 공정의 운전점 30개를 평가했다고 합시다. 목표 포집률을 달성한 점 가운데 재생기 열부하가 가장 낮은 값은 8.0입니다. 31번째 계산에서는 이 운전점의 용매 순환량을 조금 바꿔 볼까요? 아니면 지금까지 얻은 열부하 데이터에서 더 유망한 운전조건을 찾아볼까요?

NOMAD는 목적함수와 제약조건의 미분값 없이 이런 문제를 푸는 소프트웨어입니다. 운전조건을 넘기면 Aspen이 열부하와 포집률을 돌려줍니다. NOMAD가 구현한 MADS(Mesh Adaptive Direct Search)는 후보를 격자(mesh) 위에서 고릅니다. 한 반복에서 개선점을 찾지 못하면 다음에는 격자를 더 촘촘하게 만들어 현재점 주변을 더 작은 간격으로 살핍니다. [Audet과 Dennis의 MADS 논문](https://doi.org/10.1137/040603371)

## 모델로 후보를 고를 때와 평가 순서를 정할 때

Search에서는 이전에 평가한 운전점으로 현재점 근처의 열부하를 근사할 수 있습니다. 가령 순환량을 늘릴 때 처음에는 열부하가 내려가다가 다시 올라간다면, 이차모델은 그 굽은 모양을 표현할 수 있습니다. NOMAD의 `QUAD_MODEL_SEARCH`는 이런 모델로 유망한 좌표를 찾고 현재 격자에 맞춰 평가 후보를 만듭니다. 모델 위에서 여러 좌표를 비교하는 동안에는 Aspen을 다시 호출할 필요가 없습니다. [NOMAD 4 구현 논문, 3.3절](https://arxiv.org/abs/2104.11627)

Search를 생략하거나 Search에서 개선점을 찾지 못하면 Poll로 넘어갑니다. Poll은 현재점을 중심으로 방향과 보폭을 정해 주변 격자점을 후보로 만듭니다. 이때 `EVAL_QUEUE_SORT`를 `QUADRATIC_MODEL`로 설정하면 이차모델의 예측값으로 후보의 평가 순서를 정할 수 있습니다. `EVAL_OPPORTUNISTIC`을 켜고 한 점씩 평가하면 개선점이 나온 순간 나머지 후보의 호출을 아낄 수 있습니다. [NOMAD 4 사용자 안내서](https://nomad-4-user-guide.readthedocs.io/en/latest/AdvancedFunctionalities.html)

## 열부하 7.3을 예측한 A는 왜 탈락했을까?

아래는 한 번의 반복을 따라가는 가상 예입니다. 현재 최선값은 8.0이고, 모든 후보가 포집률 제약을 만족한다고 가정합니다. Search 후보는 A 하나입니다.

| 단계 | 후보를 고른 이유 | 예측 열부하 | Aspen 열부하 | 결정 |
| --- | --- | ---: | ---: | --- |
| Search · A | 이차모델이 제안한 운전점 | 7.3 | 8.2 | 8.0을 유지하고 Poll로 넘어갑니다. |
| Poll · B | Poll 후보 중 예측 열부하가 낮아 먼저 평가 | 7.6 | 7.9 | 열부하가 0.1 줄었으므로 B를 새 중심점으로 채택합니다. |
| Poll · C | B 다음에 평가할 후보 | 7.8 | 미평가 | B에서 Poll이 끝났습니다. |

A에서는 모델이 열부하를 0.7 줄일 수 있다고 봤지만, Aspen으로 계산하니 오히려 0.2 늘었습니다. A에서 Aspen 결과가 예측대로 7.3이었다면 그 자리에서 A를 채택하고 이번 Poll을 건너뛰었을 겁니다. C에서는 반대 질문이 남습니다. C가 실제로 B보다 좋았을까요? C를 계산하지 않았으니 알 수 없습니다. 이 설정에서는 현재의 8.0을 개선하는 점 하나를 찾으면 이번 반복을 마칩니다.

## Search에 Aspen 호출 한 번을 쓸 만한가?

이제 한 반복에 드는 호출 수를 비교해 봅시다. 비용 계산에서는 바로 Poll을 하면 Aspen을 4번 호출한다고 가정합니다. Search를 앞에 두면 먼저 1번을 씁니다. 이 호출에서 개선점을 찾을 확률을 *p*라고 하면 성공할 때는 그 1번으로 끝나고, 실패할 때는 Poll의 4번을 더해 총 5번을 씁니다.

따라서 Search를 먼저 할 때의 평균 호출 수는 *p* × 1 + (1 − *p*) × 5 = 5 − 4*p*입니다. 바로 Poll을 하는 비용 4와 같아지는 지점은 *p* = 0.25입니다. 네 번 시도해서 한 번 성공하면 그 한 번에 아낀 3회가 나머지 세 번에 한 회씩 더 쓴 비용을 메웁니다. **성공률이 25%를 넘어야** 한 반복당 평균 호출 수가 줄어듭니다.

Poll도 일찍 끝난다면 기준은 달라집니다. 바로 Poll을 할 때와 Search 실패 후 Poll을 할 때 모두 평균 2회가 든다고 합시다. 그러면 1 + 2(1 − *p*) < 2를 만족해야 하므로 Search 성공률이 **50%를 넘어야** 합니다. 실제 실행 기록으로 이 계산을 하려면 두 경우의 Poll 비용을 따로 집계해야 합니다. Search가 실패한 운전조건에서 Poll도 오래 걸린다면, 전체 Poll 평균을 그대로 대입할 수 없습니다.
