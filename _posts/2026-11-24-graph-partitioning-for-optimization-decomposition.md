---
layout: post
title: "Finding Candidate Decompositions of Optimization Models with Graph Partitioning"
title_ko: "그래프 분할로 최적화 모형의 분해 후보 찾기"
date: 2026-11-24
category: graph-represented-methods
category_label: "Graph-Represented Methods"
research_group: algorithmic_reviews
research_category: graph-represented-methods
research_category_label: "Graph-Represented Methods"
application_category: ""
application_category_label: ""
method_category: "graph-represented-methods"
method_category_label: "Graph-Represented Methods"
paper_title: "A Graph-Theoretic Framework for Identifying Mathematical Programming Decompositions"
authors: "Nicholas N. Kalamaris, Christos T. Maravelias"
venue: "arXiv (preprint)"
year: "2026"
doi: "10.48550/arXiv.2611.23472"
arxiv: "2611.23472"
source_url: "https://arxiv.org/abs/2611.23472"
tags:
  - "graph partitioning"
  - "integer programming"
  - "decomposition"
  - "power planning"
excerpt: "A graph partition that splits only the second period by scenario cuts the number of fixed variables from 12 to 10 while keeping three nearly equal blocks."
excerpt_ko: "2기의 운전만 시나리오별로 나누면 세 블록의 크기를 거의 같게 유지하면서 고정할 변수를 12개에서 10개로 줄일 수 있다."
language: "en-ko"
has_korean_note: false
---

In power planning, a capacity decision ties together operations under several demand scenarios. Inventory links operations in one period to the next. A modeler usually decides up front whether to split the problem by scenario or by period. Kalamaris and Maravelias ask whether the equations themselves can tell us which variables to fix or which constraints to relax. Could that reveal a decomposition that mixes periods and scenarios?

## Finding a separator with integer programming

The authors build a graph with a vertex for each variable and each constraint. An edge joins a variable to each constraint in which it appears. After coarsening the graph, they use an integer program to choose a separator *R* and assign the remaining vertices to a specified number of blocks. **If both endpoints of an edge remain, they must belong to the same block.**

Three criteria guide the choice. How evenly sized are the blocks? How many variables or constraints must be selected? Will the subproblems still be nonlinear? Changing the weights on these criteria can yield a different decomposition of the same model.

## Two ways to split the same problem into three blocks

The table reconstructs Figure 11 of the paper. S1–S3 are demand scenarios. Each block groups the operations solved together in one subproblem.

| | By scenario | By period and scenario |
| --- | --- | --- |
| Block A | Periods 1–4 of S1 | All scenarios in period 1, plus S2 in period 2 |
| Block B | Periods 1–4 of S2 | All scenarios in period 3, plus S3 in period 2 |
| Block C | Periods 1–4 of S3 | All scenarios in period 4, plus S1 in period 2 |
| Variables fixed | **12** capacity variables | 3 capacity variables and 7 inventory variables at period boundaries, **10 in total** |
| Block sizes | All three equal | All three nearly equal |

The mixed decomposition splits only period 2 by scenario and assigns each of its scenarios to a different block. This brings the number of variables to fix down from 12 to 10 while keeping the three blocks nearly equal in size.

The contribution is a systematic way to find candidate decompositions for direct comparison. Fewer fixed variables and balanced blocks alone cannot tell us which candidate will solve faster. Both the time per subproblem solve and the number of master iterations matter. The paper reports the time spent finding candidate decompositions. To compare the candidates, we would need to measure how long each takes to solve the original power planning problem to completion.

## Reference

Kalamaris, N. N., & Maravelias, C. T. (2026). *A Graph-Theoretic Framework for Identifying Mathematical Programming Decompositions*. Preprint. [arXiv:2611.23472](https://arxiv.org/abs/2611.23472)

<!-- ko -->

전력계획에서 설비용량은 여러 수요 시나리오의 운전을 묶고, 재고는 한 기간의 운전을 다음 기간과 연결한다. 보통은 시나리오별로 풀지, 기간별로 풀지 먼저 정한다. Kalamaris와 Maravelias는 묻는다. **어떤 변수를 고정하거나 어떤 제약을 완화할지 수식에서 직접 찾으면, 기간과 시나리오를 섞는 분해도 발견할 수 있을까?**

## 분해 경계를 정수계획으로 찾는다

저자들은 각 변수와 각 제약식을 정점으로 놓고, 변수가 등장하는 제약식마다 둘 사이에 간선을 긋는다. 이 그래프를 축약한 뒤, 정수계획으로 분리집합 *R*을 고르고 남은 정점들을 주어진 수의 블록에 배정한다. **간선의 양 끝점이 모두 남으면 두 점은 같은 블록에 속해야 한다.**

각 후보는 세 가지 기준으로 평가한다. 블록 크기가 얼마나 고른가? 몇 개의 변수나 제약을 선택해야 하는가? 하위문제에 비선형성이 남는가? 이 기준들의 가중치를 바꾸면 같은 모형에서도 다른 분해를 얻을 수 있다.

## 같은 문제를 세 블록으로 나누는 두 가지 방법

아래 표는 논문의 그림 11을 재구성한 것이다. S1–S3는 수요 시나리오이고, 각 블록 행에는 하나의 하위문제로 함께 푸는 운전 범위를 표시했다.

| | 시나리오별 분해 | 기간·시나리오 혼합 분해 |
| --- | --- | --- |
| 블록 A | S1의 1–4기 | 1기의 모든 시나리오 + 2기의 S2 |
| 블록 B | S2의 1–4기 | 3기의 모든 시나리오 + 2기의 S3 |
| 블록 C | S3의 1–4기 | 4기의 모든 시나리오 + 2기의 S1 |
| 고정하는 변수 | 설비용량 **12개** | 설비용량 3개 + 기간 경계 재고 7개, **총 10개** |
| 블록 크기 | 세 블록이 동일 | 세 블록이 거의 동일 |

혼합 분해에서는 **2기의 운전만 시나리오별로 나누어 서로 다른 블록에 붙인다.** 이렇게 하면 고정할 변수를 12개에서 10개로 줄이면서도 세 블록의 크기를 거의 같게 유지할 수 있다.

이 연구의 기여는 직접 비교해 볼 분해 후보를 체계적으로 찾는 데 있다. 다만 고정할 변수가 적고 블록 크기가 고르다는 사실만으로 어느 후보가 더 빨리 풀릴지는 알 수 없다. 하위문제 한 번의 풀이시간과 마스터 문제의 반복 횟수가 모두 영향을 주기 때문이다. 논문이 보고한 시간은 **분해 후보를 찾는 시간**이다. 어느 후보가 더 빠른지 판단하려면 각 분해로 **원래 전력계획 문제를 끝까지 푸는 시간**을 비교해야 한다.

## 참고문헌

Kalamaris, N. N., & Maravelias, C. T. (2026). *A Graph-Theoretic Framework for Identifying Mathematical Programming Decompositions*. 프리프린트. [arXiv:2611.23472](https://arxiv.org/abs/2611.23472)
