---
layout: post
title: "Learning the Objective, Not the Schedule: Inverse Optimization for Expert Production Planning"
title_ko: "계획이 아니라 목적함수를 학습하기: 전문가 생산계획을 위한 역최적화"
date: 2026-08-14
category: stochastic-nonlinear-optimization
category_label: "Mathematical Optimization"
research_group: algorithmic_reviews
research_category: stochastic-nonlinear-optimization
research_category_label: "Mathematical Optimization"
application_category: ""
application_category_label: ""
method_category: "stochastic-nonlinear-optimization"
method_category_label: "Mathematical Optimization"
paper_title: "Uncovering expert objectives in production planning via inverse optimization: An industrial case study"
authors: "Dixit, S.; Gupta, R.; Kelloway, A.; Wassick, J.; Zhang, Q."
venue: "Chemical Engineering Research and Design"
year: "2026"
doi: "10.1016/j.cherd.2026.07.065"
arxiv: "2608.07398"
source_url: "https://arxiv.org/abs/2608.07398"
tags:
  - "inverse optimization"
  - "inverse MILP"
  - "production planning"
  - "cutting planes"
  - "suboptimality loss"
  - "human-in-the-loop"
excerpt: "A critical note on learning interpretable objective weights from expert production plans while preserving a known industrial MILP."
excerpt_ko: "알려진 산업 MILP를 유지하면서 전문가 생산계획으로부터 해석 가능한 목적함수 가중치를 학습하는 inverse optimization에 대한 비판적 정리."
language: "en-ko"
has_korean_note: false
---

When trying to uncover tacit knowledge behind complex supply-chain decisions, the obvious data-driven approach is to learn a mapping from situation to decision. Give a black-box model the demand forecast, current inventory, and production conditions, then train it to reproduce the schedule chosen by an experienced planner. Such a model may predict well, but it still leaves the central question unanswered: why did the planner prefer this decision over the other feasible alternatives?

The more interesting approach is to model the objective behind the decision. Perhaps the planner cares far more about avoiding shortages than reducing inventory cost. Perhaps a regular production cycle matters because it protects the plant against uncertain future demand. If these priorities can be inferred from historical decisions, the resulting model does more than imitate an expert. It expresses the expert's decision logic as an interpretable objective function and generates a decision by solving an optimization problem under known operational constraints. The process becomes inspectable: we can see which trade-offs drive a plan, challenge their interpretation, and identify where the model fails to explain actual practice.

This is why I wanted to introduce the study by Dixit et al. Their Dow production-planning case is specific, but the underlying idea has room to extend to many supply-chain decisions in which constraints are reasonably well understood while preferences remain implicit. Procurement, inventory positioning, production allocation, network operation, and rolling-horizon planning all contain versions of the same problem. The paper does not complete those extensions, but it provides a useful starting architecture: preserve the known mixed-integer model, infer a small set of objective weights from expert plans, and put the learned objective back inside the optimizer.

## The forward problem is known; the objective is not

For planning instance <math><mi>u</mi></math>, the forward problem is written compactly as

<math display="block" aria-label="Forward mixed integer optimization problem">
  <mrow>
    <munder><mi>min</mi><mi>x</mi></munder>
    <mspace width="0.5em"></mspace>
    <msup><mi>c</mi><mo>⊤</mo></msup><mi>x</mi>
  </mrow>
  <mspace width="1em"></mspace>
  <mtext>subject to</mtext>
  <mspace width="0.5em"></mspace>
  <mi>A</mi><mo>(</mo><mi>u</mi><mo>)</mo><mi>x</mi><mo>≤</mo><mi>b</mi><mo>(</mo><mi>u</mi><mo>)</mo><mo>,</mo>
  <mspace width="0.5em"></mspace>
  <mi>x</mi><mo>∈</mo><msup><mi>ℝ</mi><mi>p</mi></msup><mo>×</mo><msup><mi>ℤ</mi><mi>q</mi></msup><mo>.</mo>
</math>

The variables describe production, inventory, campaign starts and ends, cycle lengths, and production gaps. The Dow plant produces eight products on one unit over a 200-period horizon. Product order is fixed by a higher-level planning problem; this MILP chooses campaign lengths while enforcing inventory and scheduling constraints.

The unknown objective is not treated as an unrestricted vector. It is assembled from seven hypothesized cost terms elicited through domain knowledge:

- positive-inventory holding cost;
- lower and upper deviations from desired inventory at campaign starts;
- lower and upper deviations from desired inventory at campaign ends;
- violations of a preferred cycle-length range;
- gaps between production campaigns.

The objective is

<math display="block" aria-label="Weighted sum of hypothesized objective terms">
  <munder><mi>min</mi><mi>x</mi></munder>
  <mspace width="0.5em"></mspace>
  <munder><mo>∑</mo><mrow><mi>k</mi><mo>∈</mo><mi>𝒦</mi></mrow></munder>
  <msub><mi>α</mi><mi>k</mi></msub>
  <msub><mi>ρ</mi><mi>k</mi></msub>
  <msub><mi>C</mi><mi>k</mi></msub><mo>(</mo><mi>x</mi><mo>)</mo><mo>.</mo>
</math>

Here <math><msub><mi>ρ</mi><mi>k</mi></msub></math> normalizes the terms and <math><msub><mi>α</mi><mi>k</mi></msub></math> represents the planner's relative preference. This is already a strong modeling decision. The method does not discover arbitrary human motives; it estimates weights within a basis chosen in advance.

## Why direct inverse MILP is awkward

Suppose the historical data contain pairs <math><mo>(</mo><msub><mi>u</mi><mi>i</mi></msub><mo>,</mo><msub><mi>x</mi><mi>i</mi></msub><mo>)</mo></math>: the demand and inventory conditions, followed by the plan made by an expert. A direct formulation would choose a cost vector and require each predicted plan to be optimal for a lower-level MILP. It would then minimize the distance between predicted and observed decisions.

This creates a bilevel problem with one mixed-integer lower level per observation. KKT conditions or strong-duality reformulations are not available in the usual way because the lower problems are MILPs. Keeping every predicted schedule and all of its mixed-integer constraints in the inverse master also makes the formulation grow quickly with the number of observations.

The paper instead uses a suboptimality loss. For instance <math><mi>i</mi></math>, let

<math display="block" aria-label="Feasible set for training instance i">
  <msub><mi>𝒮</mi><mi>i</mi></msub>
  <mo>=</mo>
  <mo>{</mo>
  <mi>x</mi><mo>:</mo><mi>A</mi><mo>(</mo><msub><mi>u</mi><mi>i</mi></msub><mo>)</mo><mi>x</mi>
  <mo>≤</mo><mi>b</mi><mo>(</mo><msub><mi>u</mi><mi>i</mi></msub><mo>)</mo>
  <mo>}</mo><mo>.</mo>
</math>

The loss asks how much worse the observed expert plan is than the best feasible plan under the estimated objective:

<math display="block" aria-label="Suboptimality gap for an observed expert decision">
  <msub><mi>ε</mi><mi>i</mi></msub>
  <mo>≥</mo>
  <msup><mover><mi>c</mi><mo>^</mo></mover><mo>⊤</mo></msup><msub><mi>x</mi><mi>i</mi></msub>
  <mo>−</mo>
  <munder><mi>min</mi><mrow><mi>x</mi><mo>∈</mo><msub><mi>𝒮</mi><mi>i</mi></msub></mrow></munder>
  <msup><mover><mi>c</mi><mo>^</mo></mover><mo>⊤</mo></msup><mi>x</mi><mo>.</mo>
</math>

If <math><msub><mi>ε</mi><mi>i</mi></msub><mo>=</mo><mn>0</mn></math>, the observed plan is optimal under the estimated objective. A positive value permits a noisy or merely near-optimal expert. The inverse problem minimizes the sum of these gaps plus an <math><msub><mi>ℓ</mi><mn>1</mn></msub></math> penalty that favors a sparse objective. The admissible set for <math><mover><mi>c</mi><mo>^</mo></mover></math> must also rule out the meaningless all-zero objective and fix the otherwise unidentified scale.

This substitution changes what the model tries to reproduce. Decision loss asks for the same schedule. Suboptimality loss asks for an objective under which the expert schedule is hard to beat. Multiple schedules can have similar costs, so the second criterion is weaker. It is also the reason the inverse master no longer needs a predicted mixed-integer schedule for every observation.

## Cutting planes turn the universal comparison into a solvable loop

The suboptimality constraint must hold against every feasible alternative:

<math display="block" aria-label="Universal suboptimality constraint">
  <msup><mover><mi>c</mi><mo>^</mo></mover><mo>⊤</mo></msup>
  <mo>(</mo><msub><mi>x</mi><mi>i</mi></msub><mo>−</mo><mover><mi>x</mi><mo>~</mo></mover><mo>)</mo>
  <mo>≤</mo><msub><mi>ε</mi><mi>i</mi></msub>
  <mspace width="0.6em"></mspace>
  <mtext>for every</mtext>
  <mspace width="0.4em"></mspace>
  <mover><mi>x</mi><mo>~</mo></mover><mo>∈</mo><msub><mi>𝒮</mi><mi>i</mi></msub><mo>.</mo>
</math>

Enumerating all alternatives is impossible. The algorithm begins with a finite subset of schedules for each training instance. With those schedules fixed, the master problem for the objective weights and suboptimality variables is an LP. It then solves a forward MILP for each observation under the current estimated cost:

<math display="block" aria-label="Cut generating forward MILP">
  <msubsup><mi>x</mi><mi>i</mi><mo>*</mo></msubsup>
  <mo>∈</mo>
  <munder><mi>arg min</mi><mrow><mi>x</mi><mo>∈</mo><msub><mi>𝒮</mi><mi>i</mi></msub></mrow></munder>
  <msup><mover><mi>c</mi><mo>^</mo></mover><mo>⊤</mo></msup><mi>x</mi><mo>.</mo>
</math>

If this schedule beats the expert by more than the current <math><msub><mi>ε</mi><mi>i</mi></msub></math>, it exposes a violated constraint and is added to the master. The loop alternates between a small LP and independent forward MILPs. It keeps only schedules that currently challenge the inferred objective.

The convergence statement needs a qualifier. To certify that no violated constraint remains, the final cut-generating MILPs must be solved to global optimality. The authors use limited solve times for faster cuts in early iterations and require optimality toward the end. A time-limited separation problem that fails to find a better schedule is not, by itself, a proof that no such schedule exists.

## What the Dow case reveals

The dataset contains 70 historical plans: 50 for training and 20 for testing, evaluated over five random splits. A model using inventory holding cost alone predicts inventory levels that are systematically too low. Adding penalties for desired inventory ranges improves the match, and the full seven-term objective improves it further.

The learned seven-term model assigns essentially zero weight to explicit inventory holding cost. Avoiding low inventory, maintaining acceptable cycle lengths, and avoiding production gaps matter more. Interviews with an expert planner support much of this interpretation. This is the paper's most persuasive result: costs that are easy to measure need not be the costs that govern decisions.

The disagreements are equally informative. Some weight rankings suggested an explanation that the expert rejected. Short production gaps in the historical plans also weakened the inferred gap penalty, even though the planner said intentional idling is normally unacceptable. Unmodeled disruptions may have produced those gaps. Inverse optimization then absorbed a missing constraint or external event into the objective weights.

The authors also let the weights vary across four time buckets and across products. Predictive error decreases. The time-dependent model suggests that shortage avoidance is stronger near the start of the rolling horizon, while regular cycle lengths matter more farther out when demand is uncertain. Product-dependent weights are consistent with different margins and customer priorities, but they can also reflect demand bias or omitted operating conditions. Better fit does not identify which explanation is correct.

## What is guaranteed, and what is inferred

The cleanest guarantee is feasibility with respect to the modeled forward problem. A new schedule is still obtained by solving the MILP, so it satisfies the constraints encoded in <math><mi>𝒮</mi><mo>(</mo><mi>u</mi><mo>)</mo></math>. A direct neural predictor would need additional machinery to make the same statement. This guarantee is only as good as the constraint model. Maintenance, operator availability, quality events, or customer-specific rules that are missing from the MILP are not covered.

The method does not guarantee recovery of a planner's true psychological objective. At least five issues remain.

First, the weighted-sum basis is prespecified. A planner may use lexicographic rules—avoid shortages first, then minimize gaps, then reduce inventory—rather than a compensatory weighted sum.

Second, inverse objectives are identifiable only up to positive scale, and highly correlated cost features may admit many nearly equivalent weight vectors. Normalization makes relative weights readable; it does not prove uniqueness.

Third, the study pools plans from multiple planners under one objective. The estimated vector may be a population compromise rather than any individual's preference.

Fourth, the records are rolling-horizon plans, not fully implemented trajectories. Decisions late in the horizon may be provisional. Time-varying weights may capture this planning convention rather than a genuine change in preference.

Fifth, allowing weights to vary by time and product adds substantial flexibility. The lower test RMSE is useful evidence, but it does not by itself separate real preference heterogeneity from additional fitting capacity.

The right interpretation is therefore modest: the method finds an objective within a chosen feature space that makes historical expert plans approximately optimal under a chosen constraint model. That is weaker than discovering the true objective. It is still valuable. The result is an interpretable, optimization-compatible hypothesis about tacit planning logic, and disagreements with experts become diagnostics for missing objectives, missing constraints, or bad data.

## Reference

Dixit, S., Gupta, R., Kelloway, A., Wassick, J., & Zhang, Q. (2026). Uncovering expert objectives in production planning via inverse optimization: An industrial case study. *Chemical Engineering Research and Design*. [https://doi.org/10.1016/j.cherd.2026.07.065](https://doi.org/10.1016/j.cherd.2026.07.065). [arXiv:2608.07398](https://arxiv.org/abs/2608.07398).

<!-- ko -->

복잡한 공급망 의사결정에 숨어 있는 암묵지를 찾아내려 할 때, 가장 먼저 떠올릴 수 있는 data-driven 접근은 상황에서 의사결정으로 가는 mapping을 학습하는 것이다. 수요 예측, 현재 재고, 생산 조건을 black-box model에 넣고 숙련된 planner가 선택한 schedule을 재현하도록 학습한다. 이런 모델은 예측을 잘할 수 있다. 그러나 가장 중요한 질문은 여전히 남는다. Planner는 왜 수많은 feasible alternative 가운데 이 결정을 더 선호했는가?

더 흥미로운 접근은 의사결정 뒤에 있는 목적함수 자체를 모델링하는 것이다. Planner는 재고 비용을 줄이는 것보다 shortage를 피하는 일을 훨씬 중요하게 생각할 수 있다. 일정한 production cycle은 미래 수요의 불확실성에 대응하기 위한 수단일 수 있다. Historical decision에서 이런 priority를 추정할 수 있다면, 모델은 단순히 전문가의 행동을 모방하는 데서 멈추지 않는다. 전문가의 의사결정 논리를 해석 가능한 목적함수로 표현하고, 알려진 운영 제약 아래에서 optimization을 풀어 결정을 생성한다. 어떤 trade-off가 계획을 움직였는지 확인하고, 그 해석에 이의를 제기하고, 실제 관행을 설명하지 못하는 지점을 찾을 수 있으므로 의사결정 과정도 더 투명해진다.

내가 Dixit et al.의 연구를 소개하고 싶은 이유가 여기에 있다. 논문이 다루는 Dow 생산계획 사례는 구체적이지만, 그 핵심 아이디어는 제약조건은 비교적 잘 알려져 있고 preference는 암묵적인 여러 공급망 문제로 확장될 여지가 크다. 조달, 재고 배치, 생산 할당, network operation, rolling-horizon planning에서도 같은 문제가 반복된다. 이 논문이 그런 확장을 완성한 것은 아니다. 대신 알려진 mixed-integer model을 보존하고, 전문가 계획에서 소수의 목적함수 가중치를 추정한 뒤, 학습된 목적함수를 다시 optimizer 안에 넣는 유용한 출발 구조를 제시한다.

## Forward problem은 알고 있고 objective만 모른다

Planning instance <math><mi>u</mi></math>에 대한 forward problem은 다음처럼 쓸 수 있다.

<math display="block" aria-label="Forward mixed integer optimization problem">
  <mrow>
    <munder><mi>min</mi><mi>x</mi></munder>
    <mspace width="0.5em"></mspace>
    <msup><mi>c</mi><mo>⊤</mo></msup><mi>x</mi>
  </mrow>
  <mspace width="1em"></mspace>
  <mtext>subject to</mtext>
  <mspace width="0.5em"></mspace>
  <mi>A</mi><mo>(</mo><mi>u</mi><mo>)</mo><mi>x</mi><mo>≤</mo><mi>b</mi><mo>(</mo><mi>u</mi><mo>)</mo><mo>,</mo>
  <mspace width="0.5em"></mspace>
  <mi>x</mi><mo>∈</mo><msup><mi>ℝ</mi><mi>p</mi></msup><mo>×</mo><msup><mi>ℤ</mi><mi>q</mi></msup><mo>.</mo>
</math>

변수는 생산, 재고, campaign 시작과 종료, cycle 길이, 생산 gap을 나타낸다. Dow plant는 하나의 생산 unit에서 8개 제품을 200개 기간에 걸쳐 생산한다. 제품 순서는 상위 planning problem에서 고정되며, 이 MILP는 재고와 scheduling 제약을 만족하면서 campaign 길이를 결정한다.

알 수 없는 목적함수를 제한 없는 vector로 두지는 않는다. Domain knowledge와 전문가 인터뷰를 이용해 다음 7개 후보 cost term을 정한다.

- 양의 재고에 대한 holding cost;
- campaign 시작 시점의 목표 재고 범위보다 낮거나 높은 deviation;
- campaign 종료 시점의 목표 재고 범위보다 낮거나 높은 deviation;
- 선호하는 cycle-length 범위의 위반;
- 생산 campaign 사이의 gap.

목적함수는 다음과 같다.

<math display="block" aria-label="Weighted sum of hypothesized objective terms">
  <munder><mi>min</mi><mi>x</mi></munder>
  <mspace width="0.5em"></mspace>
  <munder><mo>∑</mo><mrow><mi>k</mi><mo>∈</mo><mi>𝒦</mi></mrow></munder>
  <msub><mi>α</mi><mi>k</mi></msub>
  <msub><mi>ρ</mi><mi>k</mi></msub>
  <msub><mi>C</mi><mi>k</mi></msub><mo>(</mo><mi>x</mi><mo>)</mo><mo>.</mo>
</math>

<math><msub><mi>ρ</mi><mi>k</mi></msub></math>는 항들의 scale을 정규화하고, <math><msub><mi>α</mi><mi>k</mi></msub></math>는 planner의 상대적 선호를 나타낸다. 이 단계부터 강한 modeling choice가 들어간다. 이 방법은 인간의 임의의 동기를 발견하지 않는다. 미리 선택한 basis 안에서 가중치를 추정한다.

## Direct inverse MILP가 어려운 이유

Historical data가 <math><mo>(</mo><msub><mi>u</mi><mi>i</mi></msub><mo>,</mo><msub><mi>x</mi><mi>i</mi></msub><mo>)</mo></math> 쌍을 포함한다고 하자. 이는 당시의 수요·재고 조건과 전문가가 만든 계획이다. 가장 직접적인 formulation은 cost vector를 선택하고, 각 predicted plan이 lower-level MILP의 최적해가 되도록 강제한 뒤 predicted decision과 observed decision 사이의 거리를 최소화하는 것이다.

그러면 observation마다 mixed-integer lower level을 갖는 bilevel problem이 된다. Lower problem이 MILP이므로 보통의 KKT condition이나 strong duality를 이용한 reformulation을 적용할 수 없다. 각 observation의 predicted schedule과 mixed-integer constraint를 inverse master에 모두 유지하면 데이터 수에 따라 문제도 빠르게 커진다.

논문은 대신 suboptimality loss를 사용한다. Instance <math><mi>i</mi></math>의 feasible set을

<math display="block" aria-label="Feasible set for training instance i">
  <msub><mi>𝒮</mi><mi>i</mi></msub>
  <mo>=</mo>
  <mo>{</mo>
  <mi>x</mi><mo>:</mo><mi>A</mi><mo>(</mo><msub><mi>u</mi><mi>i</mi></msub><mo>)</mo><mi>x</mi>
  <mo>≤</mo><mi>b</mi><mo>(</mo><msub><mi>u</mi><mi>i</mi></msub><mo>)</mo>
  <mo>}</mo><mo>.</mo>
</math>

라고 하자. Loss는 추정한 objective 아래에서 observed expert plan이 최적 feasible plan보다 얼마나 나쁜지를 묻는다.

<math display="block" aria-label="Suboptimality gap for an observed expert decision">
  <msub><mi>ε</mi><mi>i</mi></msub>
  <mo>≥</mo>
  <msup><mover><mi>c</mi><mo>^</mo></mover><mo>⊤</mo></msup><msub><mi>x</mi><mi>i</mi></msub>
  <mo>−</mo>
  <munder><mi>min</mi><mrow><mi>x</mi><mo>∈</mo><msub><mi>𝒮</mi><mi>i</mi></msub></mrow></munder>
  <msup><mover><mi>c</mi><mo>^</mo></mover><mo>⊤</mo></msup><mi>x</mi><mo>.</mo>
</math>

<math><msub><mi>ε</mi><mi>i</mi></msub><mo>=</mo><mn>0</mn></math>이면 observed plan은 추정 objective 아래에서 optimal하다. 양의 값은 expert가 noisy하거나 near-optimal할 수 있게 허용한다. Inverse problem은 이 gap들의 합과 sparse objective를 유도하는 <math><msub><mi>ℓ</mi><mn>1</mn></msub></math> penalty를 최소화한다. 또한 <math><mover><mi>c</mi><mo>^</mo></mover></math>의 admissible set은 의미 없는 all-zero objective를 금지하고 본질적으로 식별되지 않는 scale을 고정해야 한다.

이 대체는 model이 재현하려는 대상을 바꾼다. Decision loss는 같은 schedule을 요구한다. Suboptimality loss는 expert schedule보다 훨씬 좋은 대안을 찾기 어려운 objective를 요구한다. 서로 다른 schedule이 비슷한 cost를 가질 수 있으므로 두 번째 기준이 더 약하다. 동시에 inverse master가 observation마다 predicted mixed-integer schedule을 가질 필요가 없어지는 이유이기도 하다.

## Cutting plane으로 모든 feasible alternative와의 비교를 처리한다

Suboptimality constraint는 모든 feasible alternative에 대해 성립해야 한다.

<math display="block" aria-label="Universal suboptimality constraint">
  <msup><mover><mi>c</mi><mo>^</mo></mover><mo>⊤</mo></msup>
  <mo>(</mo><msub><mi>x</mi><mi>i</mi></msub><mo>−</mo><mover><mi>x</mi><mo>~</mo></mover><mo>)</mo>
  <mo>≤</mo><msub><mi>ε</mi><mi>i</mi></msub>
  <mspace width="0.6em"></mspace>
  <mtext>for every</mtext>
  <mspace width="0.4em"></mspace>
  <mover><mi>x</mi><mo>~</mo></mover><mo>∈</mo><msub><mi>𝒮</mi><mi>i</mi></msub><mo>.</mo>
</math>

모든 대안을 열거할 수는 없다. 알고리즘은 각 training instance에 대해 소수의 schedule만 포함한 finite subset으로 시작한다. Schedule이 고정되면 objective weight와 suboptimality variable을 찾는 master problem은 LP가 된다. 그 뒤 현재 추정 cost로 각 observation의 forward MILP를 푼다.

<math display="block" aria-label="Cut generating forward MILP">
  <msubsup><mi>x</mi><mi>i</mi><mo>*</mo></msubsup>
  <mo>∈</mo>
  <munder><mi>arg min</mi><mrow><mi>x</mi><mo>∈</mo><msub><mi>𝒮</mi><mi>i</mi></msub></mrow></munder>
  <msup><mover><mi>c</mi><mo>^</mo></mover><mo>⊤</mo></msup><mi>x</mi><mo>.</mo>
</math>

이 schedule이 현재 <math><msub><mi>ε</mi><mi>i</mi></msub></math>보다 더 큰 차이로 expert를 이기면 violated constraint를 찾은 것이므로 master에 추가한다. 알고리즘은 작은 LP와 서로 독립적인 forward MILP들을 반복한다. 현재 objective를 실제로 반박하는 schedule만 유지한다.

Convergence에는 조건이 붙는다. 더 이상의 violated constraint가 없다고 보이려면 마지막 cut-generating MILP를 global optimality까지 풀어야 한다. 저자들은 초기 iteration에서는 빠른 cut을 얻기 위해 solve time을 제한하고, 마지막에는 optimality를 요구한다. Time limit 안에 더 좋은 schedule을 찾지 못했다는 사실만으로 그런 schedule이 존재하지 않는다고 증명할 수는 없다.

## Dow case가 보여준 것

Dataset은 70개의 historical plan으로 구성되며, 50개를 training에, 20개를 test에 사용하고 5개의 random split으로 평가한다. Inventory holding cost만 쓰는 model은 재고 수준을 일관되게 너무 낮게 예측한다. 목표 재고 범위에 대한 penalty를 추가하면 planner의 계획에 가까워지고, 7개 term을 모두 사용하면 더 개선된다.

학습된 7-term model에서 명시적 inventory holding cost의 weight는 사실상 0이다. 낮은 재고를 피하는 것, 적절한 cycle length를 유지하는 것, production gap을 피하는 것이 더 중요하다. Expert interview는 이 해석의 상당 부분을 지지했다. 측정하기 쉬운 비용이 실제 의사결정을 지배하는 비용과 같지 않다는 점이 이 논문의 가장 설득력 있는 결과다.

불일치도 중요하다. 일부 weight ranking에서 도출한 설명을 expert는 부정했다. Historical plan에 있던 짧은 production gap은 추정된 gap penalty를 낮췄지만, planner는 정상 상황에서 의도적 idling이 허용되기 어렵다고 설명했다. 모델에 없는 disruption이 gap을 만들었을 수 있다. 그 경우 inverse optimization은 missing constraint나 external event를 objective weight에 흡수한다.

저자들은 weight를 4개 time bucket과 제품별로도 다르게 두었다. Predictive error는 감소했다. Time-dependent model은 rolling horizon 앞부분에서 shortage 회피가 더 강하고, demand가 불확실한 뒤쪽에서는 regular cycle length가 더 중요하다고 해석할 수 있다. Product-dependent weight는 margin이나 customer priority 차이와 일치할 수 있지만, demand bias나 omitted operating condition도 같은 현상을 만들 수 있다. Better fit만으로 어느 설명이 옳은지는 식별되지 않는다.

## 무엇이 보장되고 무엇이 추론되는가

가장 명확한 보장은 modeled forward problem에 대한 feasibility다. 새 schedule도 MILP를 풀어 얻으므로 <math><mi>𝒮</mi><mo>(</mo><mi>u</mi><mo>)</mo></math>에 포함된 제약을 만족한다. Direct neural predictor가 같은 주장을 하려면 별도의 장치가 필요하다. 그러나 이 보장은 constraint model만큼만 유효하다. MILP에 없는 maintenance, operator availability, quality event, customer-specific rule은 보장 범위 밖이다.

이 방법은 planner의 true psychological objective를 복원한다고 보장하지 않는다. 최소한 다섯 가지 문제가 남는다.

첫째, weighted-sum basis는 미리 정해진다. Planner가 shortage 회피를 먼저 만족하고, 그 안에서 gap을 줄인 뒤, 마지막으로 inventory를 줄이는 lexicographic rule을 사용할 수도 있다. 이는 compensatory weighted sum과 같지 않다.

둘째, inverse objective는 positive scale까지밖에 식별되지 않는다. Cost feature들이 강하게 correlated되어 있으면 여러 weight vector가 거의 같은 결정을 설명할 수도 있다. Normalization은 relative weight를 읽을 수 있게 하지만 uniqueness를 증명하지는 않는다.

셋째, 이 연구는 여러 planner의 계획을 하나의 objective 아래에 묶는다. 추정 vector는 특정 개인의 preference가 아니라 population compromise일 수 있다.

넷째, 기록은 실제로 끝까지 실행된 trajectory가 아니라 rolling-horizon plan이다. Horizon 뒤쪽의 decision은 provisional할 수 있다. Time-varying weight가 genuine preference change보다 planning convention을 반영할 가능성이 있다.

다섯째, time과 product별로 weight를 다르게 두면 model flexibility가 크게 증가한다. 낮아진 test RMSE는 유용한 근거이지만, true preference heterogeneity와 추가된 fitting capacity를 그 자체로 구분하지는 못한다.

따라서 적절한 해석은 제한적이다. 이 방법은 선택한 feature space 안에서, 선택한 constraint model 아래에서, historical expert plan을 approximately optimal하게 만드는 objective를 찾는다. True objective의 발견보다는 약한 주장이다. 그래도 가치가 있다. 결과는 암묵적 planning logic에 대한 해석 가능하고 optimization-compatible한 가설이다. Expert와의 불일치는 missing objective, missing constraint, 또는 나쁜 데이터를 찾는 진단 신호가 된다.

## 참고문헌

Dixit, S., Gupta, R., Kelloway, A., Wassick, J., & Zhang, Q. (2026). Uncovering expert objectives in production planning via inverse optimization: An industrial case study. *Chemical Engineering Research and Design*. [https://doi.org/10.1016/j.cherd.2026.07.065](https://doi.org/10.1016/j.cherd.2026.07.065). [arXiv:2608.07398](https://arxiv.org/abs/2608.07398).
