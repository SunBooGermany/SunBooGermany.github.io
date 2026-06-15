---
layout: post
title: "Explainable Degradation-Aware Sizing for Off-Grid Green Hydrogen"
title_ko: "오프그리드 그린수소 sizing에서 degradation을 목적함수 안으로 넣기"
date: 2026-06-15
category: green-chemical-systems
category_label: "Green Chemical Systems"
research_group: application_reviews
research_category: green-chemical-systems
research_category_label: "Green Chemical Systems"
application_category: "green-chemical-systems"
application_category_label: "Green Chemical Systems"
method_category: ""
method_category_label: ""
paper_title: "Explainable degradation-aware techno-economic optimization of off-grid green hydrogen production"
authors: "Rinchi, B.; Al-Dahidi, S.; Ayadi, O.; Alrbai, M."
venue: "Energy Conversion and Management"
year: "2026"
doi: ""
arxiv: ""
source_url: ""
tags:
  - "green hydrogen"
  - "PEM electrolysis"
  - "techno-economic analysis"
  - "degradation"
  - "off-grid systems"
  - "LCOH"
  - "explainable AI"
excerpt: "A critical note on an off-grid PV-battery-PEM hydrogen TEA that folds PEM degradation, battery fade, replacement timing, and Sobol/XGBoost/SHAP interpretation into the sizing objective."
excerpt_ko: "PV-battery-PEM 오프그리드 그린수소 시스템에서 PEM degradation, battery fade, replacement timing, Sobol/XGBoost/SHAP 해석을 sizing objective에 함께 넣은 TEA 논문에 대한 비판적 정리."
language: "en-ko"
has_korean_note: false
---

## Why this paper matters

Off-grid solar hydrogen has a simple economic problem: the electrolyzer is expensive, but solar power is intermittent. A PEM stack cannot earn back its capital cost if it only operates during a limited part of the day. Rinchi et al. report PEM utilization around 32-33% in the solar-only off-grid cases they study, so the levelized cost of hydrogen is pushed up by low annual hydrogen output per unit of installed PEM capacity.

The second problem is more subtle. Many techno-economic analyses size the system on a representative year, repeat that production profile across the project lifetime, and then add replacements using coarse calendar assumptions. That misses the path dependence of the system. PEM stacks degrade under high load and start-stop cycling. Batteries lose effective capacity through cycle and calendar aging. Replacement timing is therefore not just an accounting line; it is a consequence of the dispatch trajectory.

This paper is useful because it puts those pieces into the objective evaluation itself. The main contribution is not a new optimizer. Differential Evolution, Sobol analysis, XGBoost, and SHAP are standard tools. The contribution is the engineering consistency of the pipeline:

```text
historical hourly weather
  -> PV generation
  -> rule-based PV-battery-PEM dispatch
  -> PEM degradation and battery fade
  -> physics-scheduled replacements
  -> discounted lifetime cost and hydrogen output
  -> LCOH-based sizing
  -> Sobol/XGBoost/SHAP interpretation
```

That is a useful TEA move: make the optimizer see the same degradation-aware lifecycle economics that the paper later reports.

## What is optimized

The design vector is small:

<math display="block" aria-label="Design vector">
  <mi>x</mi>
  <mo>=</mo>
  <mo>[</mo>
  <msub><mi>P</mi><mi>PV</mi></msub>
  <mo>,</mo>
  <msub><mi>E</mi><mi>bat</mi></msub>
  <mo>,</mo>
  <msub><mi>P</mi><mi>PEM</mi></msub>
  <mo>]</mo>
</math>

Here <math><msub><mi>P</mi><mi>PV</mi></msub></math> is PV capacity, <math><msub><mi>E</mi><mi>bat</mi></msub></math> is battery energy capacity, and <math><msub><mi>P</mi><mi>PEM</mi></msub></math> is PEM rated power. The objective is LCOH plus penalties for production shortfall and residual energy imbalance.

The dispatch policy itself is not optimized. Operation is rule-based: run the PEM at full load if PV and the battery can support it, run at partial load if PV is above the minimum stable PEM load, and turn the PEM off if the minimum load cannot be met. This matters. The paper is degradation-aware in the evaluation, but it is not a joint design-operation optimization paper. It is closer to optimized capacity sizing under a fixed dispatch heuristic.

That distinction is not a minor wording issue. Full-load operation improves utilization and capital recovery, but it can also accelerate degradation. If stack replacement is near a threshold, partial-load smoothing could be economically better than forcing full-load operation. This paper accounts for that degradation cost after the rule acts; it does not optimize the rule against that cost.

## Degradation is the important modeling step

The PEM degradation model links operation to efficiency loss. Operating degradation increases with load fraction through a power-law term, while start-up events add extra degradation. The accumulated degradation then increases the specific energy consumption:

<math display="block" aria-label="Degradation adjusted SEC">
  <msub><mi>SEC</mi><mi>deg</mi></msub>
  <mo>(</mo><mi>t</mi><mo>)</mo>
  <mo>=</mo>
  <mi>SEC</mi>
  <mo>(</mo><mi>t</mi><mo>)</mo>
  <mo>[</mo><mn>1</mn><mo>+</mo><mi>D</mi><mo>(</mo><mi>t</mi><mo>)</mo><mo>]</mo>
</math>

The economic mechanism is direct. High load and frequent start-stop events increase degradation; degradation raises SEC; higher SEC lowers hydrogen output for the same electrical input; lower lifetime production and stack replacement costs raise LCOH.

The battery model is simpler. Effective battery capacity declines according to the more severe of cycle fade and calendar fade, with a floor on remaining capacity. This is not a detailed electrochemical aging model, but the paper's results suggest that battery sizing is not the main economic driver in the studied cases.

## What the results say

The optimized systems are roughly half-megawatt PV systems with PEM capacities around 240-290 kW:

| Site | PV kW | Battery kWh | PEM kW | LCOH |
| --- | ---: | ---: | ---: | ---: |
| UAE | 536.7 | 99.9 | 286.9 | 7.83 $/kg |
| KSA | 532.0 | 149.5 | 285.6 | 8.06 $/kg |
| Qatar | 477.4 | 182.2 | 242.2 | 8.22 $/kg |

These are high values, but the reason is not mysterious. A solar-only off-grid system cannot keep the PEM stack highly utilized, so capital cost is spread over a smaller hydrogen output. Grid connection or wind-solar complementarity could change the utilization story, but that is outside this paper's system boundary.

The degradation effect is large enough to matter. Lifetime-averaged hydrogen yield is about 5-6% below year-one output. PEM stack replacement occurs around years 8, 16, and 24, while battery replacement occurs around year 15. The paper reports that stack replacement alone adds about 1.20 $/kg to LCOH. Ignoring degradation would therefore bias the economics downward in a structural way.

The cost hierarchy is also clear. CAPEX dominates the LCOH, stack replacement is the next important term, and battery replacement is small. The strongest improvement levers are PEM efficiency, PEM CAPEX, PV CAPEX, and discount rate. A 20% SEC reduction is reported to cut Abu Dhabi LCOH by about 1.62 $/kg, which is larger than the effect of a comparable PEM CAPEX reduction.

## Explainability is useful, but not causal proof

The paper adds Sobol sensitivity analysis, an XGBoost surrogate, and SHAP values to interpret the simulator. That is useful because the full model is a non-smooth black-box objective: dispatch regimes switch, replacement events are triggered by thresholds, and weather-year effects interact with sizing.

The Sobol results make intuitive sense. PV capacity has the largest total-effect index, followed by PEM capacity. Degradation rate and PEM CAPEX matter, while battery capacity has much weaker influence. XGBoost approximates the simulated LCOH mapping with high holdout accuracy, and SHAP then attributes surrogate predictions mostly to PV capacity and degradation-related variables.

The limitation is that this is explanation of a simulator, not validation of the physical plant. SHAP is not causal evidence. A careful interpretation is: given this simulator, this sampling range, and this surrogate model, degradation-related parameters receive high attribution in the learned LCOH mapping. That is still informative. It is just not a proof that the same ranking would hold under a different dispatch policy, degradation law, or downstream hydrogen boundary.

## The main weakness

The strongest limitation is the fixed dispatch policy. The paper is called degradation-aware, but the control policy does not appear to solve a degradation-aware dispatch problem. It follows a heuristic that prioritizes PEM utilization. A stronger formulation would optimize both capacity and dispatch policy:

<math display="block" aria-label="Joint sizing and dispatch objective">
  <munder><mi>min</mi><mrow><mi>x</mi><mo>,</mo><mi>π</mi></mrow></munder>
  <mspace width="0.5em"/>
  <mfrac>
    <mrow><msub><mi>C</mi><mi>disc</mi></msub><mo>(</mo><mi>x</mi><mo>,</mo><mi>π</mi><mo>)</mo></mrow>
    <mrow><msub><mi>M</mi><mi>disc</mi></msub><mo>(</mo><mi>x</mi><mo>,</mo><mi>π</mi><mo>)</mo></mrow>
  </mfrac>
</math>

where <math><mi>π</mi></math> controls whether to run at full load, smooth partial-load operation, charge the battery, or delay operation to avoid crossing a replacement threshold. That would turn the paper from degradation-accounting sizing into degradation-aware operation and design.

There are other limits too. The degradation law is an engineering surrogate. Real PEM degradation depends on temperature, pressure, water purity, current-density profile, shutdown protocol, and balance-of-plant behavior. Weather uncertainty is represented through historical records rather than a full climate-risk model. The LCOH boundary is closer to production-gate hydrogen because compression, storage, transport, and delivery are not the main focus.

## One-sentence evaluation

This is not a new optimization-theory paper. It is a practical process-systems TEA paper that makes off-grid PV-battery-PEM hydrogen sizing more internally consistent by carrying degradation, replacement, and lifetime economics through the objective, then using explainability tools to inspect the resulting cost drivers.

## Reference

Rinchi, B., Al-Dahidi, S., Ayadi, O., & Alrbai, M. (2026). Explainable degradation-aware techno-economic optimization of off-grid green hydrogen production. *Energy Conversion and Management, 364*, 121710.

<!-- ko -->

## 왜 이 논문이 중요한가

오프그리드 solar hydrogen의 경제성 문제는 단순하다. 전해조는 비싼데 태양광은 간헐적이다. PEM stack은 하루 중 제한된 시간에만 운전되면 설치비를 충분히 회수하기 어렵다. Rinchi et al.은 solar-only off-grid case에서 PEM utilization이 약 32-33% 수준이라고 보고한다. 따라서 설치된 PEM capacity 대비 연간 수소 생산량이 낮아지고, LCOH가 크게 올라간다.

두 번째 문제는 더 미묘하다. 많은 techno-economic analysis는 representative year에서 system을 sizing한 뒤 그 생산량을 project lifetime 동안 반복하고, replacement는 대략적인 calendar assumption으로 더한다. 이 방식은 system의 path dependence를 놓친다. PEM stack은 high load와 start-stop cycling에서 degradation되고, battery는 cycle aging과 calendar aging으로 effective capacity가 줄어든다. Replacement timing은 단순한 회계 항목이 아니라 dispatch trajectory의 결과다.

이 논문이 유용한 이유는 이 요소들을 objective evaluation 안으로 넣고, 다음 pipeline을 engineering 관점에서 일관되게 묶은 데 있다.

```text
historical hourly weather
  -> PV generation
  -> rule-based PV-battery-PEM dispatch
  -> PEM degradation and battery fade
  -> physics-scheduled replacements
  -> discounted lifetime cost and hydrogen output
  -> LCOH-based sizing
  -> Sobol/XGBoost/SHAP interpretation
```

## 무엇을 최적화하는가

<math display="block" aria-label="Design vector">
  <mi>x</mi>
  <mo>=</mo>
  <mo>[</mo>
  <msub><mi>P</mi><mi>PV</mi></msub>
  <mo>,</mo>
  <msub><mi>E</mi><mi>bat</mi></msub>
  <mo>,</mo>
  <msub><mi>P</mi><mi>PEM</mi></msub>
  <mo>]</mo>
</math>

여기서 <math><msub><mi>P</mi><mi>PV</mi></msub></math>는 PV capacity, <math><msub><mi>E</mi><mi>bat</mi></msub></math>는 battery energy capacity, <math><msub><mi>P</mi><mi>PEM</mi></msub></math>은 PEM rated power다. Objective는 LCOH에 production shortfall penalty와 residual energy imbalance penalty를 더한 형태다.

하지만 dispatch policy 자체는 최적화하지 않는다. 운전은 rule-based다. PV와 battery가 full-load PEM 운전을 지탱할 수 있으면 full load로 돌리고, PV가 minimum stable PEM load 이상이면 partial load로 돌리며, minimum load도 만족하지 못하면 PEM을 끈다. 이 점이 중요하다. 이 논문은 평가에서는 degradation-aware이지만, joint design-operation optimization 논문은 아니다. 더 정확히는 fixed dispatch heuristic 아래에서 capacity sizing을 최적화한 논문에 가깝다.

이 구분은 사소한 표현 문제가 아니다. Full-load operation은 utilization과 capital recovery에는 좋지만 degradation을 빠르게 만들 수 있다. Stack replacement가 threshold 근처라면 full-load 운전보다 partial-load smoothing이 경제적으로 더 나을 수도 있다. 이 논문은 rule이 작동한 뒤 degradation cost를 계산하지만, 그 cost를 기준으로 rule 자체를 최적화하지는 않는다.

## Degradation이 핵심 modeling step이다

PEM degradation model은 operation을 efficiency loss와 연결한다. Operating degradation은 load fraction에 대한 power-law term으로 증가하고, start-up event는 추가 degradation을 만든다. 누적 degradation은 specific energy consumption을 증가시킨다.

<math display="block" aria-label="Degradation adjusted SEC">
  <msub><mi>SEC</mi><mi>deg</mi></msub>
  <mo>(</mo><mi>t</mi><mo>)</mo>
  <mo>=</mo>
  <mi>SEC</mi>
  <mo>(</mo><mi>t</mi><mo>)</mo>
  <mo>[</mo><mn>1</mn><mo>+</mo><mi>D</mi><mo>(</mo><mi>t</mi><mo>)</mo><mo>]</mo>
</math>

경제적 mechanism은 직접적이다. High load와 잦은 start-stop event는 degradation을 증가시킨다. Degradation은 SEC를 높인다. SEC가 높아지면 같은 전력으로 생산되는 수소가 줄어든다. Lifetime production 감소와 stack replacement cost가 LCOH를 올린다.

Battery model은 더 단순하다. Effective battery capacity는 cycle fade와 calendar fade 중 더 severe한 쪽을 따라 감소하고, remaining capacity에는 하한을 둔다. 정교한 electrochemical aging model은 아니지만, 논문의 결과에서는 battery sizing이 주요 경제 driver가 아니므로 이 단순화가 핵심 결론을 크게 흔들지는 않는 것으로 보인다.

## 결과가 말하는 것

Optimized system은 대략 half-megawatt PV system이고, PEM capacity는 240-290 kW 정도다.

| Site | PV kW | Battery kWh | PEM kW | LCOH |
| --- | ---: | ---: | ---: | ---: |
| UAE | 536.7 | 99.9 | 286.9 | 7.83 $/kg |
| KSA | 532.0 | 149.5 | 285.6 | 8.06 $/kg |
| Qatar | 477.4 | 182.2 | 242.2 | 8.22 $/kg |

이 값은 높지만 이유는 명확하다. Solar-only off-grid system은 PEM stack을 높은 utilization으로 유지하기 어렵다. 따라서 capital cost가 더 작은 hydrogen output 위에 나뉜다. Grid connection이나 wind-solar complementarity가 있으면 utilization story가 달라질 수 있지만, 그건 이 논문의 system boundary 밖이다.

Degradation effect는 충분히 크다. Lifetime-averaged hydrogen yield는 year-one output보다 약 5-6% 낮다. PEM stack replacement는 대략 8, 16, 24년에 발생하고, battery replacement는 15년쯤 발생한다. 논문은 stack replacement alone이 LCOH에 약 1.20 $/kg를 더한다고 보고한다. 따라서 degradation을 무시하면 economics가 구조적으로 낮게 추정된다.

Cost hierarchy도 분명하다. CAPEX가 LCOH를 지배하고, stack replacement가 그 다음으로 중요하며, battery replacement는 작다. 가장 강한 개선 lever는 PEM efficiency, PEM CAPEX, PV CAPEX, discount rate다. 논문은 Abu Dhabi에서 SEC를 20% 줄이면 LCOH가 약 1.62 $/kg 낮아진다고 보고한다. 이는 유사한 비율의 PEM CAPEX reduction보다 큰 효과다.

## Explainability는 유용하지만 causal proof는 아니다

논문은 simulator를 해석하기 위해 Sobol sensitivity analysis, XGBoost surrogate, SHAP value를 붙인다. Full model은 non-smooth black-box objective이므로 이 접근은 유용하다. Dispatch regime이 바뀌고, replacement event는 threshold에서 발생하며, weather-year effect는 sizing과 상호작용한다.

Sobol 결과는 직관적이다. PV capacity가 가장 큰 total-effect index를 갖고, 그 다음이 PEM capacity다. Degradation rate와 PEM CAPEX도 영향을 주지만, battery capacity의 영향은 훨씬 약하다. XGBoost는 simulated LCOH mapping을 높은 holdout accuracy로 근사하고, SHAP은 surrogate prediction의 주요 attribution을 PV capacity와 degradation-related variables에 준다.

다만 이것은 physical plant validation이 아니라 simulator explanation이다. SHAP은 causal evidence가 아니다. 정확한 해석은 다음에 가깝다. 주어진 simulator, sampling range, surrogate model 안에서 degradation-related parameter는 learned LCOH mapping에 대해 높은 attribution을 갖는다. 이 사실은 유용하지만, dispatch policy, degradation law, downstream hydrogen boundary가 달라져도 같은 ranking이 유지된다는 증명은 아니다.

## 가장 큰 약점

가장 강한 limitation은 fixed dispatch policy다. 논문은 degradation-aware라고 부르지만, control policy가 degradation-aware dispatch problem을 푸는 것은 아니다. Policy는 PEM utilization을 우선하는 heuristic을 따른다. 더 강한 formulation은 capacity와 dispatch policy를 함께 최적화해야 한다.

<math display="block" aria-label="Joint sizing and dispatch objective">
  <munder><mi>min</mi><mrow><mi>x</mi><mo>,</mo><mi>π</mi></mrow></munder>
  <mspace width="0.5em"/>
  <mfrac>
    <mrow><msub><mi>C</mi><mi>disc</mi></msub><mo>(</mo><mi>x</mi><mo>,</mo><mi>π</mi><mo>)</mo></mrow>
    <mrow><msub><mi>M</mi><mi>disc</mi></msub><mo>(</mo><mi>x</mi><mo>,</mo><mi>π</mi><mo>)</mo></mrow>
  </mfrac>
</math>

여기서 <math><mi>π</mi></math>는 full load로 돌릴지, partial-load operation으로 smoothing할지, battery를 충전할지, replacement threshold를 피하기 위해 operation을 늦출지 결정한다. 이렇게 되어야 degradation-accounting sizing을 넘어 degradation-aware operation and design이 된다.

다른 한계도 있다. Degradation law는 engineering surrogate다. 실제 PEM degradation은 temperature, pressure, water purity, current-density profile, shutdown protocol, balance-of-plant behavior에 의존한다. Weather uncertainty는 full climate-risk model이 아니라 historical record를 통해 표현된다. Compression, storage, transport, delivery가 중심이 아니므로 LCOH boundary는 production-gate hydrogen에 가깝다.

## 한 문장 평가

Off-grid PV-battery-PEM hydrogen sizing에서 degradation, replacement, lifetime economics를 objective 안으로 끌고 들어와 내부 일관성을 높이고, 그 결과를 explainability tool로 해석한 practical process-systems TEA 논문이다.

## Reference

Rinchi, B., Al-Dahidi, S., Ayadi, O., & Alrbai, M. (2026). Explainable degradation-aware techno-economic optimization of off-grid green hydrogen production. *Energy Conversion and Management, 364*, 121710.
