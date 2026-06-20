---
layout: post
title: "BOHB and MILP for Multi-Timescale LH2 Supply Chain Design"
title_ko: "BOHB와 MILP로 보는 국제 LH2 공급망의 다시간척도 설계"
date: 2026-06-20
category: llm-probabilistic-approaches
category_label: "LLM & Probabilistic Approaches"
research_group: algorithmic_reviews
research_category: llm-probabilistic-approaches
research_category_label: "LLM & Probabilistic Approaches"
application_category: ""
application_category_label: ""
method_category: "llm-probabilistic-approaches"
method_category_label: "LLM & Probabilistic Approaches"
paper_title: "Techno-economic analysis for design and management of international green hydrogen supply chain under uncertainty: An integrated temporal planning approach"
authors: "Kim, S.; Park, J.; Chung, W.; Adams, D.; Lee, J. H."
venue: "Energy Conversion and Management"
year: "2024"
doi: ""
arxiv: ""
source_url: ""
tags:
  - "Bayesian optimization"
  - "BOHB"
  - "MILP"
  - "liquid hydrogen"
  - "stochastic scenarios"
  - "supply chain design"
excerpt: "A critical note on a BOHB-MILP framework for international liquid hydrogen supply-chain design under hourly renewable variability, weekly shipping, lead time, and sampled demand-weather scenarios."
excerpt_ko: "시간별 재생에너지 변동, 주별 선박운항, 운송 lead time, 수요-기상 시나리오를 결합한 국제 액화수소 공급망 BOHB-MILP 프레임워크에 대한 비판적 노트."
language: "en-ko"
has_korean_note: false
---

This note is about an international liquid-hydrogen supply-chain model that combines investment decisions, hourly renewable operation, weekly ship scheduling, long-distance transport lead time, boil-off, and demand-weather uncertainty. The interesting part is not that each component is new. The interesting part is the coupling. A hydrogen exporter is not cheap just because its annual solar or wind resource looks good. It is cheap only if production, storage, liquefaction, fleet size, and import-side inventory survive the timing problem.

The paper can be read as a BOHB-MILP architecture. BOHB searches over a small set of capacity decisions. For each proposed design, scenario-wise MILPs check whether hourly and weekly operation can meet demand. This is why the paper belongs naturally in LLM & Probabilistic Approaches rather than only in green hydrogen techno-economics: the upper layer is a probabilistic black-box search procedure, while the lower layer preserves exact operational constraints.

## The Design Problem

The high-level design vector is roughly

<math display="block" aria-label="Design vector for liquid hydrogen supply chain">
  <mi>x</mi>
  <mo>=</mo>
  <mo>(</mo>
  <msup><mi>X</mi><mi>T</mi></msup><mo>,</mo>
  <msup><mi>X</mi><mi>P</mi></msup><mo>,</mo>
  <msup><mi>X</mi><mi>B</mi></msup><mo>,</mo>
  <msup><mi>X</mi><mi>W</mi></msup><mo>,</mo>
  <msup><mi>X</mi><mi>L</mi></msup><mo>,</mo>
  <msup><mi>X</mi><mi>HE</mi></msup><mo>,</mo>
  <msup><mi>X</mi><mi>HI</mi></msup><mo>,</mo>
  <msup><mi>X</mi><mi>S</mi></msup>
  <mo>)</mo><mo>.</mo>
</math>

These terms represent wind, PV, battery, PEM electrolyzer, liquefaction plant, export-side LH2 storage, import-side LH2 storage, and LH2 ship count. The vector is chosen before the demand-weather scenario is known.

Given a scenario, the lower-level operating variables include battery state of charge, charge and discharge, electrolyzer power, liquefaction power, export and import inventory, and weekly shipping decisions. Structurally, the problem is closer to

<math display="block" aria-label="Scenario robust feasibility constrained design problem">
  <munder><mi>min</mi><mi>x</mi></munder>
  <mspace width="0.4em"></mspace>
  <mi>C</mi><mo>(</mo><mi>x</mi><mo>)</mo>
  <mspace width="1em"></mspace>
  <mtext>subject to</mtext>
  <mspace width="0.4em"></mspace>
  <mo>&forall;</mo><mi>s</mi><mo>&isin;</mo><mi>S</mi><mo>,</mo>
  <mspace width="0.3em"></mspace>
  <mo>&exist;</mo><msub><mi>y</mi><mi>s</mi></msub>
  <mo>&isin;</mo>
  <msub><mi>Y</mi><mi>s</mi></msub><mo>(</mo><mi>x</mi><mo>)</mo>
  <mo>.</mo>
</math>

That is, the model is not mainly minimizing expected operating cost across recourse decisions. It is searching for a capital design whose operation is feasible for every sampled scenario. The objective is dominated by annualized CAPEX and fixed O&M. Since annual hydrogen demand is fixed, minimizing annual cost is equivalent to minimizing LCOH, but the denominator should be kept explicit when interpreting units.

## Why Time Scales Matter

The model combines three clocks.

The annual clock chooses capacity: wind, PV, battery, electrolyzer, liquefaction, tanks, and ships. The weekly clock moves LH2 across the ocean with lead time. The hourly clock balances renewable generation, battery operation, electrolyzer loading, liquefaction, storage, and curtailment.

This matters because the assets are not interchangeable. Batteries absorb hourly power volatility. Electrolyzers convert electricity into hydrogen but are constrained by minimum-load logic. LH2 tanks absorb daily, weekly, and seasonal mismatch in hydrogen inventory. Ships are not just transport vehicles; they are moving storage whose cycle time depends on distance, boil-off, and onboard fuel consumption.

The minimum-load constraint is a good example. If the PEM electrolyzer must operate above a fraction <math><mi>&rho;</mi></math> of installed capacity whenever it is on, then a simplified form is

<math display="block" aria-label="Electrolyzer minimum load">
  <msub><mi>p</mi><mrow><mi>s</mi><mo>,</mo><mi>t</mi></mrow></msub>
  <mo>&le;</mo>
  <msup><mi>X</mi><mi>W</mi></msup>
  <msub><mi>z</mi><mrow><mi>s</mi><mo>,</mo><mi>t</mi></mrow></msub>
  <mo>,</mo>
  <mspace width="1em"></mspace>
  <msub><mi>p</mi><mrow><mi>s</mi><mo>,</mo><mi>t</mi></mrow></msub>
  <mo>&ge;</mo>
  <mi>&rho;</mi>
  <msup><mi>X</mi><mi>W</mi></msup>
  <msub><mi>z</mi><mrow><mi>s</mi><mo>,</mo><mi>t</mi></mrow></msub>
  <mo>,</mo>
  <mspace width="1em"></mspace>
  <msub><mi>z</mi><mrow><mi>s</mi><mo>,</mo><mi>t</mi></mrow></msub>
  <mo>&isin;</mo><mo>{</mo><mn>0</mn><mo>,</mo><mn>1</mn><mo>}</mo><mo>.</mo>
</math>

This single binary switch changes the lower-level problem from an LP-like dispatch model into a MILP. It also explains a reported sensitivity: reducing the minimum load from 5% to 3% lowers required battery capacity and improves LCOH. That conclusion is conditional. It assumes the better low-load capability does not bring extra CAPEX, degradation, balance-of-plant cost, or safety cost.

## What BOHB Is Doing

The outer BOHB layer proposes candidate capacity vectors. The lower MILP then checks each candidate against demand-weather scenarios. Feasible candidates receive an LCOH score; infeasible candidates are removed or penalized; BOHB uses the history to propose the next candidate.

Bayesian optimization is useful here because the design dimension is modest. The operating model is huge, but the outer variables are only a handful of capacities and ship count. The paper uses TPE rather than a Gaussian process. TPE separates past candidates into good and bad groups and samples where the candidate looks more like the good group than the bad group.

Hyperband adds early stopping. Many candidates are evaluated cheaply, weak candidates are discarded, and only a smaller set receives expensive evaluation. This is sensible only if the cheap evaluation ranks designs similarly to the full evaluation. In a robustness problem, that assumption is delicate. A design can look cheap under ordinary scenarios and fail under a rare low-wind, high-demand, long-lead-time case. The paper would be easier to reproduce and judge if the Hyperband resource budget were described more concretely: scenario count, solver time, horizon length, iteration count, or some other fidelity level.

## The Main Strength

The main strength is that the lower-level operation is not replaced by a learned surrogate. A black-box neural or regression surrogate might badly approximate the feasibility boundary created by inventory nonnegativity, vessel integer decisions, lead time, boil-off, battery dynamics, and electrolyzer on/off constraints. Here, for a fixed design and sampled scenario, the MILP performs an explicit operational feasibility check.

This gives the framework a clear division of labor:

BOHB explores a nonconvex, discontinuous design landscape.

MILP verifies scenario-wise physical and operational feasibility.

That is a defensible architecture. The paper does not prove global optimality of the BOHB result, and it should not be read as doing so. But it avoids the weaker mistake of replacing hard logistics and storage constraints with a smooth surrogate and then trusting the surrogate near feasibility cliffs.

## What Is Guaranteed

The guarantees are local to the modeling choices.

If the lower problem is correctly formulated as a MILP and solved to the claimed tolerance, then for a fixed design and fixed scenario the operational feasibility judgment is exact at the MILP level. If every sampled scenario is feasible, then the design is feasible for the sampled scenario set.

That does not imply global optimality of the full design problem. BOHB is a heuristic global search method, not a certificate-producing optimizer. The design landscape is discontinuous because ship count is integer, electrolyzer operation contains binary variables, feasibility appears through thresholds, and lead time changes fleet circulation.

It also does not imply robustness to unobserved futures. The sampled scenarios are not the same as a chance constraint over the true distribution, and they are not the same as robust feasibility over an uncertainty set. A more formal version would need something like

<math display="block" aria-label="Chance feasibility target">
  <mi>P</mi><mo>(</mo>
  <mi>Y</mi><mo>(</mo><mi>x</mi><mo>,</mo><mi>&xi;</mi><mo>)</mo>
  <mo>&ne;</mo><mi>&empty;</mi>
  <mo>)</mo>
  <mo>&ge;</mo>
  <mn>1</mn><mo>-</mo><mi>&epsilon;</mi>
  <mo>,</mo>
</math>

or a robust counterpart over an uncertainty set. The supplied analysis notes that the statistical construction of demand-weather scenarios is not fully clear from the paper text alone.

## The Perfect-Foresight Issue

The most important modeling weakness is perfect foresight in operation. The lower MILP appears to optimize each scenario with the full year of future weather and demand already known. That is useful for planning, but it is not an online operating policy.

A real operator at time <math><mi>t</mi></math> does not know the full future path. A realistic operational layer would be nonanticipative, or it would use rolling-horizon MPC with forecasts. In general, perfect-information operation gives a lower cost than nonanticipative operation. The gap may be large during long low-wind periods, port delays, demand spikes, ship outages, degradation events, or seasonal transitions with poor forecasts.

So the LCOH should be read carefully: it is closer to the design cost under sampled scenarios with future-informed operation than to the cost achievable by a deployable real-time policy.

## Reading the Results

The contrast between the average case and the variability case is the useful message. Under constant demand and renewable availability, LCOH is reported around 2.3-2.9 USD/kg H2, batteries are not needed, and electrolyzers and liquefaction plants can operate close to full load. In that simplified world, lead time dominates because transport distance and losses are the main remaining differences.

When demand and weather variability are included, LCOH rises to about 3.6-5.0 USD/kg H2. The design shifts toward mixed wind-PV portfolios, larger electrolyzers, battery and LH2 storage, and lower average electrolyzer utilization. This is the core systems lesson:

Average renewable resource is not enough. The supply chain must survive the timing of bad renewable periods, demand peaks, inventory depletion, and ship lead time.

The reported cost increase should not be called pure uncertainty cost. It mixes temporal variability, seasonal structure, scenario robustness, storage value, and flexibility value. An ablation separating these effects would make the interpretation stronger.

## Assessment

The contribution is not a fundamentally new decomposition method. At its core, the architecture is outer black-box design search plus inner exact operational optimization. A stronger optimization paper might use scenario-wise infeasibility certificates, logic-based Benders cuts, adaptive scenario generation, chance-constrained design, distributionally robust optimization, or joint design with a nonanticipative MPC/RL policy.

Still, the integrated model is valuable. International LH2 supply chains are easy to underestimate when the analysis collapses renewable supply, shipping, and demand into annual averages. This paper keeps the timing problem visible: hourly power, weekly vessels, lead time, inventory, boil-off, and scenario feasibility all interact.

The strongest conclusion is therefore modest but useful. A country with a good average renewable resource is not automatically the lowest-cost hydrogen exporter under uncertainty. Once variability enters, complementarity between wind and PV, electrolyzer flexibility, storage sizing, and fleet circulation can matter as much as, or more than, simple distance.

The open question is operational realism. The next step should not only be a better BOHB tuning strategy. It should be a design model linked to nonanticipative operation: rolling-horizon MPC, adaptive scenario generation, distributional robustness, or an explicit learned policy whose mistakes are accounted for inside the capacity decision.

## Reference

Kim, S., Park, J., Chung, W., Adams, D., & Lee, J. H. (2024). Techno-economic analysis for design and management of international green hydrogen supply chain under uncertainty: An integrated temporal planning approach. Energy Conversion and Management, 301, 118010.

<!-- ko -->

이 글은 국제 액화수소(LH2) 공급망에서 설비 투자, 시간별 재생에너지 운영, 주별 선박 스케줄, 장거리 운송 lead time, boil-off, 수요-기상 불확실성을 하나로 묶는 논문에 대한 노트다. 흥미로운 지점은 각 요소가 완전히 새롭다는 데 있지 않다. 핵심은 결합이다. 어떤 국가의 연평균 태양광 또는 풍력 자원이 좋다고 해서 그 국가가 곧 저비용 수소 수출국이 되는 것은 아니다. 생산, 저장, 액화, 선박 수, 수입국 재고가 모두 시간 문제를 견뎌야 한다.

이 논문은 BOHB-MILP 구조로 읽을 수 있다. BOHB는 비교적 작은 설비용량 설계공간을 탐색한다. 각 설계 후보에 대해 시나리오별 MILP가 시간별·주별 운영으로 수요를 충족할 수 있는지 확인한다. 그래서 이 글은 단순히 그린수소 techno-economics가 아니라 LLM 및 확률론적 접근법 섹션에 두는 것이 자연스럽다. 상위층은 확률적 black-box search이고, 하위층은 물리적 운영 제약을 정확한 최적화 문제로 남겨 둔다.

## 설계 문제

상위 설계변수는 대략 다음과 같다.

<math display="block" aria-label="Design vector for liquid hydrogen supply chain">
  <mi>x</mi>
  <mo>=</mo>
  <mo>(</mo>
  <msup><mi>X</mi><mi>T</mi></msup><mo>,</mo>
  <msup><mi>X</mi><mi>P</mi></msup><mo>,</mo>
  <msup><mi>X</mi><mi>B</mi></msup><mo>,</mo>
  <msup><mi>X</mi><mi>W</mi></msup><mo>,</mo>
  <msup><mi>X</mi><mi>L</mi></msup><mo>,</mo>
  <msup><mi>X</mi><mi>HE</mi></msup><mo>,</mo>
  <msup><mi>X</mi><mi>HI</mi></msup><mo>,</mo>
  <msup><mi>X</mi><mi>S</mi></msup>
  <mo>)</mo><mo>.</mo>
</math>

각 항은 풍력, PV, 배터리, PEM 전해조, 액화 플랜트, 수출국 LH2 저장탱크, 수입국 LH2 저장탱크, LH2 선박 수를 뜻한다. 이 벡터는 수요-기상 시나리오가 실현되기 전에 결정된다.

시나리오가 주어지면 하위 운영변수는 배터리 SOC, 충방전량, 전해조 전력, 액화 전력, 수출국·수입국 재고, 주별 선박 운항 결정을 포함한다. 구조적으로 이 문제는 다음에 가깝다.

<math display="block" aria-label="Scenario robust feasibility constrained design problem">
  <munder><mi>min</mi><mi>x</mi></munder>
  <mspace width="0.4em"></mspace>
  <mi>C</mi><mo>(</mo><mi>x</mi><mo>)</mo>
  <mspace width="1em"></mspace>
  <mtext>subject to</mtext>
  <mspace width="0.4em"></mspace>
  <mo>&forall;</mo><mi>s</mi><mo>&isin;</mo><mi>S</mi><mo>,</mo>
  <mspace width="0.3em"></mspace>
  <mo>&exist;</mo><msub><mi>y</mi><mi>s</mi></msub>
  <mo>&isin;</mo>
  <msub><mi>Y</mi><mi>s</mi></msub><mo>(</mo><mi>x</mi><mo>)</mo>
  <mo>.</mo>
</math>

즉, 기대 운영비를 recourse로 최소화하는 전형적 2-stage stochastic program이라기보다, 표본 시나리오 전체에서 운영 가능한 설비 설계를 찾는 feasibility-constrained design problem에 더 가깝다. 목적함수는 연간화 CAPEX와 고정 O&M이 중심이다. 연간 수소 수요가 고정되어 있으므로 총연간비용 최소화와 LCOH 최소화는 최적화 관점에서 동치지만, 단위 해석에서는 분모를 명시하는 편이 더 정확하다.

## 왜 시간척도가 중요한가

모델은 세 개의 시계를 결합한다.

연간 시계는 풍력, PV, 배터리, 전해조, 액화기, 저장탱크, 선박 수를 정한다. 주간 시계는 LH2를 선박 lead time과 함께 바다 건너 이동시킨다. 시간별 시계는 재생에너지 발전, 배터리 운전, 전해조 부하, 액화, 저장, 출력제한을 맞춘다.

이 구분이 중요한 이유는 자산들이 서로 단순 대체재가 아니기 때문이다. 배터리는 시간 단위 전력 변동성을 흡수한다. 전해조는 전기를 수소로 바꾸지만 최소부하 논리에 묶인다. LH2 탱크는 일·주·계절 단위의 수소 재고 불일치를 흡수한다. 선박은 단순한 운송수단이 아니라 거리, boil-off, 선박 연료 소비에 따라 회전율이 달라지는 이동형 저장설비다.

전해조 minimum-load 제약이 좋은 예다. PEM 전해조가 켜져 있을 때 설치용량의 일정 비율 <math><mi>&rho;</mi></math> 이상으로 운전해야 한다면, 단순화된 제약은 다음과 같다.

<math display="block" aria-label="Electrolyzer minimum load">
  <msub><mi>p</mi><mrow><mi>s</mi><mo>,</mo><mi>t</mi></mrow></msub>
  <mo>&le;</mo>
  <msup><mi>X</mi><mi>W</mi></msup>
  <msub><mi>z</mi><mrow><mi>s</mi><mo>,</mo><mi>t</mi></mrow></msub>
  <mo>,</mo>
  <mspace width="1em"></mspace>
  <msub><mi>p</mi><mrow><mi>s</mi><mo>,</mo><mi>t</mi></mrow></msub>
  <mo>&ge;</mo>
  <mi>&rho;</mi>
  <msup><mi>X</mi><mi>W</mi></msup>
  <msub><mi>z</mi><mrow><mi>s</mi><mo>,</mo><mi>t</mi></mrow></msub>
  <mo>,</mo>
  <mspace width="1em"></mspace>
  <msub><mi>z</mi><mrow><mi>s</mi><mo>,</mo><mi>t</mi></mrow></msub>
  <mo>&isin;</mo><mo>{</mo><mn>0</mn><mo>,</mo><mn>1</mn><mo>}</mo><mo>.</mo>
</math>

이 binary switch 하나 때문에 하위 운영문제는 LP에 가까운 dispatch가 아니라 MILP가 된다. 또한 minimum load를 5%에서 3%로 낮추면 배터리 용량이 줄고 LCOH가 개선된다는 민감도 결과도 설명된다. 다만 이 결론은 조건부다. 낮은 minimum load가 추가 CAPEX, degradation, balance-of-plant 비용, 안전비용 없이 가능하다고 가정하기 때문이다.

## BOHB가 하는 일

상위 BOHB는 설비용량 후보를 제안한다. 하위 MILP는 각 후보를 수요-기상 시나리오에 대해 검사한다. feasible 후보에는 LCOH 점수가 붙고, infeasible 후보는 제거되거나 벌점을 받는다. BOHB는 그 평가 이력을 사용해 다음 후보를 제안한다.

Bayesian optimization이 유용한 이유는 설계 차원이 비교적 작기 때문이다. 운영모델은 크지만 상위 변수는 몇 개의 용량과 선박 수다. 논문은 Gaussian process 대신 TPE를 사용한다. TPE는 과거 후보를 좋은 집단과 나쁜 집단으로 나누고, 좋은 집단과 닮았지만 나쁜 집단과는 덜 닮은 영역에서 다음 후보를 뽑는다.

Hyperband는 조기 제거를 더한다. 많은 후보를 싸게 평가하고, 약한 후보를 버린 뒤, 적은 수의 후보만 비싼 평가로 보낸다. 이 방식이 타당하려면 저비용 평가의 순위와 전체 평가의 순위가 충분히 비슷해야 한다. 그러나 robustness 문제에서는 이 가정이 약하다. 어떤 설계는 보통 시나리오에서는 싸지만 저풍속, 고수요, 긴 lead time이 겹친 rare event에서 실패할 수 있다. 논문에서 Hyperband의 resource budget이 시나리오 수인지, solver time인지, horizon length인지, 반복횟수인지 더 구체적으로 설명되었다면 재현성과 해석이 더 쉬웠을 것이다.

## 가장 강한 부분

가장 큰 장점은 하위 운영을 학습 surrogate로 대체하지 않는다는 점이다. black-box neural surrogate나 regression surrogate는 재고 비음수 제약, 선박 정수 결정, lead time, boil-off, 배터리 동역학, 전해조 on/off 제약이 만드는 feasibility boundary를 잘못 근사할 수 있다. 이 논문은 고정 설계와 표본 시나리오에 대해 MILP로 운영 가능성을 직접 확인한다.

역할 분담은 분명하다.

BOHB는 비볼록·불연속 설계공간을 탐색한다.

MILP는 시나리오별 물리·운영 feasibility를 검증한다.

이는 방어 가능한 구조다. 논문이 BOHB 결과의 전역 최적성을 증명하는 것은 아니고, 그렇게 읽어서도 안 된다. 하지만 hard logistics와 storage 제약을 매끄러운 surrogate로 바꾸고 feasibility cliff 근처에서 그 surrogate를 믿는 약한 접근은 피한다.

## 무엇이 보장되는가

보장은 모델링 선택 안에서만 성립한다.

하위문제가 정확히 MILP로 구성되었고 solver가 주장한 tolerance까지 풀렸다면, 고정 설계와 고정 시나리오에 대한 운영 가능성 판단은 MILP 수준에서 정확하다. 모든 표본 시나리오가 feasible이면 그 설계는 표본 시나리오 집합에 대해 feasible이다.

하지만 이것은 전체 설계문제의 global optimum을 뜻하지 않는다. BOHB는 certificate를 주는 전역최적화 알고리즘이 아니라 heuristic global search다. 선박 수는 정수이고, 전해조 운전에는 binary 변수가 있으며, feasibility는 threshold를 통해 나타나고, lead time은 선박 회전율을 불연속적으로 바꿀 수 있다.

또한 관측되지 않은 미래에 대한 robustness도 보장하지 않는다. 표본 시나리오 feasibility는 참분포에 대한 chance constraint도 아니고, uncertainty set 전체에 대한 robust feasibility도 아니다. 더 형식적인 목표라면 다음과 같은 조건이 필요하다.

<math display="block" aria-label="Chance feasibility target">
  <mi>P</mi><mo>(</mo>
  <mi>Y</mi><mo>(</mo><mi>x</mi><mo>,</mo><mi>&xi;</mi><mo>)</mo>
  <mo>&ne;</mo><mi>&empty;</mi>
  <mo>)</mo>
  <mo>&ge;</mo>
  <mn>1</mn><mo>-</mo><mi>&epsilon;</mi>
  <mo>,</mo>
</math>

또는 uncertainty set에 대한 robust counterpart가 필요하다. 첨부 분석에서도 demand-weather scenario의 통계적 생성 구조가 본문만으로 충분히 명확하지 않다는 점을 지적한다.

## Perfect Foresight 문제

가장 중요한 약점은 운영 단계의 perfect foresight다. 하위 MILP는 각 시나리오에서 1년치 미래 기상과 수요를 이미 알고 운전계획을 최적화하는 것으로 보인다. 이는 계획 문제로는 유용하지만 온라인 운영정책은 아니다.

실제 운영자는 시점 <math><mi>t</mi></math>에서 미래 경로 전체를 모른다. 더 현실적인 운영층은 nonanticipative policy이거나 예측을 사용하는 rolling-horizon MPC여야 한다. 일반적으로 perfect-information operation은 nonanticipative operation보다 낮은 비용을 준다. 장기 저풍속 기간, 항만 지연, 수요 급증, 선박 고장, degradation, 예측오차가 큰 계절 전환기에서는 그 차이가 커질 수 있다.

따라서 LCOH는 조심해서 읽어야 한다. 이는 실제 배포 가능한 실시간 정책의 비용이라기보다, 표본 시나리오에서 미래를 알고 운전할 수 있다고 가정했을 때의 설계비용에 더 가깝다.

## 결과를 읽는 법

평균조건 case와 variability case의 대비가 이 논문의 유용한 메시지다. 수요와 재생에너지 availability를 일정하게 두면 LCOH는 약 2.3-2.9 USD/kg H2로 보고되고, 배터리는 필요 없으며, 전해조와 액화기는 거의 full-load에 가깝게 운전된다. 이 단순화된 세계에서는 lead time이 지배적이다. 운송거리와 운송 중 손실이 주요 차이로 남기 때문이다.

수요와 기상 변동성을 넣으면 LCOH는 약 3.6-5.0 USD/kg H2로 상승한다. 설계는 풍력-PV 혼합, 더 큰 전해조, 배터리와 LH2 저장, 낮은 평균 전해조 utilization 쪽으로 이동한다. 시스템 관점의 핵심은 이 문장이다.

평균 재생에너지 자원량이 충분한 것과 모든 불리한 시점에 공급망이 버티는 것은 다르다.

저풍속·저일사 구간, 수요 peak, 재고 depletion, 선박 lead time이 겹칠 때도 공급망은 작동해야 한다.

이 비용 상승분을 순수한 uncertainty cost라고 부르면 안 된다. 여기에는 시간변동성, 계절 구조, scenario robustness, storage value, flexibility value가 섞여 있다. 이 효과들을 분리하는 ablation이 있었다면 해석력이 더 강했을 것이다.

## 평가

이 논문의 기여는 근본적으로 새로운 decomposition 방법은 아니다. 구조의 핵심은 outer black-box design search와 inner exact operational optimization이다. 더 강한 최적화 논문이 되려면 scenario-wise infeasibility certificate, logic-based Benders cut, adaptive scenario generation, chance-constrained design, distributionally robust optimization, 또는 nonanticipative MPC/RL 정책과 설계의 결합이 필요했을 것이다.

그럼에도 통합 모델로서의 가치는 있다. 국제 LH2 공급망은 재생에너지 공급, 선박 운송, 수요를 연평균으로 압축하면 너무 쉽게 과소평가된다. 이 논문은 시간 문제를 계속 보이게 둔다. 시간별 전력, 주별 선박, lead time, 재고, boil-off, 시나리오 feasibility가 서로 물린다.

따라서 가장 강한 결론은 겸손하지만 유용하다. 평균 재생에너지 자원이 좋은 국가가 불확실성 하에서 자동으로 가장 싼 수소 수출국이 되는 것은 아니다. 변동성이 들어오면 풍력과 PV의 상호보완성, 전해조 유연성, 저장 용량, 선박 회전율이 단순 거리만큼 또는 그보다 더 중요해질 수 있다.

남는 질문은 운영 현실성이다. 다음 단계는 BOHB tuning을 조금 더 잘하는 데서 끝나면 안 된다. 설계 모델이 nonanticipative operation과 연결되어야 한다. rolling-horizon MPC, adaptive scenario generation, distributional robustness, 또는 명시적 learned policy를 설계 결정 안에서 함께 다루는 방향이 더 중요하다.

## Reference

Kim, S., Park, J., Chung, W., Adams, D., & Lee, J. H. (2024). Techno-economic analysis for design and management of international green hydrogen supply chain under uncertainty: An integrated temporal planning approach. Energy Conversion and Management, 301, 118010.
