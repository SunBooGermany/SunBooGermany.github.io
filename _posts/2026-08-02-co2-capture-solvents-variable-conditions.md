---
layout: post
title: "Beyond Minimum Reboiler Duty: Evaluating CO₂ Capture Solvents under Variable Conditions"
title_ko: "최소 regeneration energy를 넘어: 변동 조건에서 CO₂ 포집 흡수제 평가하기"
date: 2026-08-02
category: chemical-plants
category_label: "Chemical Plants"
research_group: application_reviews
research_category: chemical-plants
research_category_label: "Chemical Plants"
application_category: "chemical-plants"
application_category_label: "Chemical Plants"
method_category: ""
method_category_label: ""
paper_title: "Robust process design and operation for efficient CO₂ capture under variable supply-and-demand conditions"
authors: "Lim, S.; Yun, S. H.; Oh, J.; Yoon, Y. I.; Jang, J. T.; Park, J."
venue: "Journal of Environmental Chemical Engineering, 14, Article 124308"
year: "2026"
doi: "10.1016/j.jece.2026.124308"
arxiv: ""
source_url: "https://doi.org/10.1016/j.jece.2026.124308"
tags:
  - "chemical plants"
  - "CO₂ capture"
  - "amine solvents"
  - "MDEA/PZ"
  - "off-design operation"
  - "reboiler duty"
  - "process sensitivity"
excerpt: "A solvent with the lowest nominal reboiler duty may still require the tightest circulation control. This note separates energy efficiency, disturbance sensitivity, and ease of operation in an Aspen Plus comparison of MEA and MDEA/PZ solvents."
excerpt_ko: "정상 설계점에서 regeneration energy가 가장 낮은 흡수제가 반드시 운전하기 쉬운 것은 아니다. Aspen Plus 기반 MEA 및 MDEA/PZ 비교를 통해 에너지 효율, 외생조건 민감도, 운전 오차 민감도를 구분한다."
language: "en-ko"
has_korean_note: false
---

An industrial CO₂-capture unit rarely receives a fixed feed. The CO₂ concentration and flow rate of flue gas change with plant load, fuel composition, upstream operation, and combustion conditions. The required capture rate or CO₂ production target can also change. The absorber–stripper system must therefore operate while both the supply of CO₂ and the demand for captured CO₂ are moving.

Most solvent-screening and process-design studies simplify this problem to one steady-state condition. They select an inlet CO₂ concentration, gas flow rate, and capture target, then determine the absorber and stripper design and the operating point that minimize reboiler duty. The resulting solvent ranking is often treated as fixed. This is useful for establishing a nominal design, but it does not show whether the same solvent remains efficient when the feed and production target move away from that point.

That gap is the problem examined by this paper. A CO₂-capture solvent should not be ranked only by its minimum reboiler duty at one nominal design point. The location of that minimum can move as flue-gas composition, throughput, and capture rate change. Even when the external condition is fixed, a plant rarely holds the solvent circulation rate exactly at its calculated optimum.

The economic scale is already visible from the paper's regeneration-energy calculation. Using its steam price of 6 USD/GJ, the nominal duties correspond to about 22.93 USD/tCO₂ for MEA and 19.97 USD/tCO₂ for MDEA/PZ 20/20. The nominal difference is therefore about 2.96 USD per tonne of captured CO₂. At 100 tCO₂/day, continuous operation for 365 days would make the difference about 108,000 USD/year in regeneration steam alone. Yet a ±10% L/G deviation raises the duty of MDEA/PZ 20/20 by roughly 8–12%. Under the same simplifying assumptions, that penalty is about 58,000–87,000 USD/year.

Three quantities therefore need to be separated:

- the minimum specific reboiler duty at the nominal condition;
- the change in the best attainable duty when the external condition changes;
- the energy penalty caused by operating away from the best liquid-to-gas ratio, or L/G.

Lim et al. compare 40 wt% MEA, 20/20 wt% MDEA/PZ, and 30/10 wt% MDEA/PZ with a rate-based Aspen Plus absorber–stripper model. MDEA/PZ 20/20 performs best on the first two measures. It has the lowest nominal duty and generally the smallest response to the tested changes in CO₂ concentration and production rate. Yet its L/G–duty curve is the sharpest near the optimum. A small circulation set-point error can erase part of its energy advantage.

That apparent contradiction is the useful engineering result: the solvent that is least sensitive to external load changes can still be the most sensitive to an internal operating decision.

## The nominal ranking

The reference condition is 13 mol% CO₂, 100 tonnes per day of captured CO₂, and a 90% capture rate. The reported optima are:

| Solvent | Optimal L/G | Minimum reboiler duty |
|---|---:|---:|
| MEA 40 wt% | 3.695 | 3.821 GJ/tCO₂ |
| MDEA/PZ 20/20 wt% | 2.352 | 3.328 GJ/tCO₂ |
| MDEA/PZ 30/10 wt% | 2.942 | 3.591 GJ/tCO₂ |

At this point, MDEA/PZ 20/20 uses about 12.9% less regeneration energy than MEA. Its lower optimal L/G also means that the target capture rate is reached with less solvent circulation.

The result is chemically plausible. MDEA offers favorable regeneration through a bicarbonate-dominated pathway, while PZ accelerates CO₂ absorption. Raising the PZ fraction from the 30/10 blend to the 20/20 blend helps when gas-phase driving force or contact time is limited. The faster reaction and higher effective cyclic capacity reduce the solvent flow required for the same capture target, which in turn reduces the sensible heat needed to warm the circulating liquid.

This explanation has a boundary. The model does not directly include PZ precipitation, volatilization, aerosol emissions, long-term degradation, or every viscosity-related hydraulic penalty. The result establishes an energy ranking inside the modeled process, not a complete solvent-life or environmental ranking.

## Why the L/G curve has a minimum

The U-shaped relation between L/G and reboiler duty is the physical core of the comparison.

At very low L/G, a small amount of solvent must carry a large CO₂ load. To maintain the specified capture rate, more CO₂ must be removed from each unit of solvent in the stripper so that the returning lean solvent has a lower CO₂ loading. This requires additional reboiler heat and stripping steam, although it does not necessarily require a higher stripper-bottom temperature.

As L/G increases, each unit of solvent carries less CO₂. Deep regeneration is no longer necessary, so reboiler duty initially falls. Beyond the optimum, however, the plant is heating and pumping more liquid than it needs. Sensible heat becomes dominant and duty rises again.

The minimum alone does not describe this curve. Its local curvature matters. The paper measures this by perturbing L/G by ±10% around the optimum. The approximate duty increases are 2–3% for MEA, 8–12% for MDEA/PZ 20/20, and 6–9% for MDEA/PZ 30/10.

MEA therefore has the highest minimum duty but the flattest neighborhood. MDEA/PZ 20/20 has the lowest minimum but the narrowest neighborhood. MDEA/PZ 30/10 lies between them. In operational terms:

- MDEA/PZ 20/20 rewards accurate L/G control;
- MEA sacrifices energy efficiency but tolerates more circulation error;
- MDEA/PZ 30/10 offers an intermediate compromise.

This is a local, one-factor sensitivity metric. Stripper pressure, lean loading, and other operating variables are held fixed rather than reoptimized together. A multivariable controller could recover some of the apparent penalty. The ±10% result should not be read as a closed-loop control test.

## External variability is a different axis

The study also varies three supply-and-demand conditions: inlet CO₂ concentration, CO₂ production rate, and capture rate. These scenarios ask a different question from the L/G perturbation. They ask how the process response changes when the plant is given a different task.

For CO₂ concentrations of 11, 13, and 15 mol%, the gas flow is adjusted to maintain 100 tonnes per day of CO₂ production. MDEA/PZ 20/20 shows an approximate duty variation of 3–4%, compared with roughly 8–10% for MEA; MDEA/PZ 30/10 responds non-monotonically. The higher PZ content is helpful at low CO₂ partial pressure because fast reaction kinetics compensate for weaker gas-phase driving force.

This scenario is not a clean concentration-only experiment. Lowering CO₂ concentration while holding CO₂ production fixed requires more flue gas. The result combines a partial-pressure effect with changes in gas velocity, contact time, and column hydraulics. “Concentration–throughput coupled sensitivity” is the more exact description.

The size of this coupling is not small. Relative to 13 mol%, maintaining the same captured-CO₂ product and capture rate at 11 mol% requires about 18.2% more molar flue-gas flow; at 15 mol%, it requires about 13.3% less. This is a meaningful demand-following scenario if a downstream process requires a fixed CO₂ product rate and the capture unit can adjust the fraction of flue gas it treats. It is not, however, a generic representation of a power plant disturbance. In a single plant, load, fuel composition, excess air, and air leakage jointly determine both flue-gas flow and CO₂ concentration. A load decrease will often reduce total flue-gas flow while concentration changes less, although the exact correlation is plant-specific.

A more discriminating study would separate three cases: fixed gas flow with concentration varied, fixed concentration with gas flow varied, and joint concentration–flow trajectories taken from plant data. It would then evaluate a factorial grid or realistic joint scenarios with capture rate, inlet temperature, and production target varied together. The paper tests several parameters, but mainly one at a time or through the constant-product coupling above. That is useful steady-state scenario mapping, but it cannot identify nonlinear interactions among simultaneous disturbances or establish performance over the actual joint operating distribution.

When CO₂ production changes from 90 to 110 tonnes per day, MDEA/PZ 20/20 again has the smallest reported duty change, about 1–2%, compared with 8–10% for MEA and 3–4% for MDEA/PZ 30/10. This supports a limited claim: the 20/20 blend is relatively insensitive within the tested ±10% throughput range. It does not establish performance over the full load-following range of a power plant, and the steady-state model contains neither solvent inventory dynamics nor thermal transients.

Raising capture rate is more punishing. The duties at 80% and 90% capture are relatively close, whereas all three solvents become much more energy-intensive at 99%. The reported curves place the 99% duties at roughly 5.6 GJ/tCO₂ for MEA and 4.5 GJ/tCO₂ for both MDEA/PZ blends. Near the absorber top, the remaining gas-phase CO₂ partial pressure becomes very small. Achieving the last percentage points requires a much lower lean loading, which means removing more CO₂ from the solvent with additional reboiler heat and stripping steam.

The 99% case uses equipment designed around the 90% reference condition. It therefore estimates the penalty of pushing that equipment to 99%, not the minimum energy of a new process designed specifically for 99% capture. Packing height, heat-exchanger area, circulation capacity, pressure level, intercooling, or split-flow design could change that result.

## What “robust” means here

The word “robust” in the title should be interpreted empirically, not as a mathematical guarantee. The paper maps steady-state Aspen Plus responses across selected off-design scenarios. It does not define an uncertainty set or probability distribution, solve a min–max or chance-constrained problem, examine simultaneous worst cases, or simulate a feedback controller under temporal disturbances.

A low steady-state energy sensitivity does not imply short settling time, low overshoot, freedom from actuator saturation, or closed-loop stability. Likewise, identifying the lowest point on a sampled response curve does not prove a joint global optimum over L/G, stripper pressure, column design, and every disturbance.

The most defensible reading is narrower: within the modeled equipment, tested operating ranges, and converged sensitivity cases, MDEA/PZ 20/20 maintains a low reboiler duty across several external scenarios. Near its own L/G optimum, however, its energy performance deteriorates faster than MEA's when the circulation ratio is displaced.

## Model and comparison boundaries

The Aspen Plus model uses an electrolyte thermodynamic description and rate-based columns to represent reaction-enhanced gas–liquid mass transfer. That level of detail is needed to distinguish the kinetic effect of PZ from the slower MDEA response. The model is based on Aspen examples and parameter sets validated in prior literature, but the paper does not report independent pilot-scale validation for every solvent composition, column size, and 99% off-design case studied here. It is better described as a literature- and database-based rate process model than as a plant-validated digital twin.

The equipment also differs by solvent. The reported absorber heights are 15 m for MEA, 20 m for MDEA/PZ 20/20, and 25 m for MDEA/PZ 30/10, with differences in stripper geometry as well. This is a comparison of separately sized solvent–process systems, not a same-column solvent swap. That is reasonable for comparing operating energy in new designs, but insufficient for a retrofit decision.

These equipment dimensions are fixed during the sensitivity studies. The columns are sized separately for each solvent around the nominal basis of 13 mol% CO₂, 100 tonnes per day of captured CO₂, and 90% capture, after which diameter, height, packing, and associated equipment parameters are carried into the off-design cases. L/G and stripper pressure are the main operating variables that are swept; the equipment design is not resized or co-optimized for each disturbance.

It is therefore too strong to describe the equipment as a mathematically optimal design. The paper does not formulate a joint design problem in which column dimensions, packing, heat-exchanger area, and operating policy are decision variables optimized over all scenarios or total annual cost. “Solvent-specific nominal sizing followed by off-design operating analysis” is the more accurate description. The reported solvent ranking is conditional on those fixed designs. A different column geometry or a design chosen explicitly for 99% capture or wide load-following could produce a different energy ranking and operating window.

The economic calculation mainly converts steam duty at 6 USD/GJ. It excludes column and packing capital, pump and blower electricity, solvent makeup, corrosion, emissions control, precipitation management, instrumentation, maintenance, and downtime. “Lowest regeneration-steam cost” is supported; “lowest total cost” is not.

## Design implication

The practical lesson is to replace a single solvent-ranking number with a response surface. At minimum, a screening study should report the minimum duty, the optimal L/G, the local curvature around that optimum, and performance under coupled concentration and throughput changes. It should then check whether the low-energy region remains feasible under hydraulic, thermal, degradation, and control constraints.

For MDEA/PZ 20/20, that suggests pairing the solvent choice with accurate solvent-flow measurement, sufficient pump turndown, and an L/G control or real-time optimization strategy that tracks a moving optimum. For MEA, the control requirement is less sharp, but the baseline steam penalty remains. The plant decision is therefore not “which solvent has the lowest point?” It is “which solvent–equipment–control combination keeps an acceptably low duty over the conditions the plant will actually visit?”

The most efficient solvent is not necessarily the easiest solvent to operate.

## Reference

Lim, S., Yun, S. H., Oh, J., Yoon, Y. I., Jang, J. T., & Park, J. (2026). Robust process design and operation for efficient CO₂ capture under variable supply-and-demand conditions. *Journal of Environmental Chemical Engineering, 14*, 124308. [https://doi.org/10.1016/j.jece.2026.124308](https://doi.org/10.1016/j.jece.2026.124308)

<!-- ko -->

산업용 CO₂ 포집설비에 일정한 조건의 배가스만 들어오는 경우는 드물다. 발전소나 공정의 부하, 연료 조성, 상류공정 운전, 연소조건이 달라지면 배가스의 CO₂ 농도와 유량도 계속 변한다. 요구되는 포집률이나 CO₂ 생산목표도 고정되어 있지 않을 수 있다. Absorber–stripper 공정은 CO₂ 공급조건과 포집 수요가 함께 움직이는 상황에서 운전되어야 한다.

그러나 대부분의 solvent screening과 process design 연구는 이 문제를 하나의 steady-state condition으로 단순화한다. 특정 inlet CO₂ concentration, gas flow rate, capture target을 정한 뒤 reboiler duty가 최소가 되도록 absorber와 stripper를 설계하고 운전점을 결정한다. 이렇게 얻은 solvent ranking도 고정된 결과처럼 사용되는 경우가 많다. Nominal design을 정하는 데는 유용하지만, feed와 생산목표가 기준점에서 벗어났을 때도 같은 흡수제가 효율적인지는 보여 주지 못한다.

이 논문이 다루는 문제가 바로 이 간극이다. CO₂ 포집용 흡수제를 하나의 정상 설계점에서 계산한 최소 reboiler duty만으로 평가해서는 안 된다. 배가스 조성, 처리량, 포집률이 바뀌면 최소점의 위치도 이동할 수 있다. 외생조건이 고정되어 있어도 실제 플랜트가 solvent circulation을 계산된 최적값에 정확히 유지하기는 어렵다.

논문의 regeneration energy 계산만으로도 이 문제의 경제적 규모를 볼 수 있다. 논문이 사용한 steam price 6 USD/GJ를 적용하면 기준조건의 재생증기 비용은 MEA가 약 22.93 USD/tCO₂, MDEA/PZ 20/20이 약 19.97 USD/tCO₂다. 따라서 기준조건에서 MDEA/PZ 20/20의 재생증기 비용은 MEA보다 포집 CO₂ 1톤당 약 2.96 USD 낮다. 하루 100 tCO₂를 365일 연속 포집한다고 가정하면 재생증기 비용 차이는 연간 약 108,000 USD다. 그러나 MDEA/PZ 20/20은 L/G가 최적점에서 ±10% 벗어날 때 duty가 약 8–12% 증가한다. 같은 단순 가정으로 환산하면 연간 약 58,000–87,000 USD의 penalty다.

따라서 세 가지를 구분해야 한다.

- 기준조건에서의 최소 specific reboiler duty
- 외생조건이 변했을 때 달성 가능한 최소 duty의 변화
- 최적 liquid-to-gas ratio, 즉 L/G에서 벗어날 때 발생하는 energy penalty

Lim 등은 rate-based Aspen Plus absorber–stripper model로 MEA 40 wt%, MDEA/PZ 20/20 wt%, MDEA/PZ 30/10 wt%를 비교한다. MDEA/PZ 20/20은 앞의 두 기준에서 가장 좋다. 기준 duty가 가장 낮고, 시험한 CO₂ 농도와 생산량 변화에 대한 민감도도 대체로 가장 작다. 그러나 최적점 부근의 L/G–duty 곡선은 가장 뾰족하다. 작은 circulation set-point 오차가 에너지 이점의 일부를 지울 수 있다.

이 모순처럼 보이는 결과가 중요한 공학적 메시지다. 외부 부하변화에 가장 둔감한 흡수제가 내부 운전변수에는 가장 민감할 수 있다.

## 기준조건에서의 순위

기준조건은 CO₂ 13 mol%, CO₂ 포집량 100 tonnes/day, 포집률 90%다. 보고된 최적값은 다음과 같다.

| 흡수제 | 최적 L/G | 최소 reboiler duty |
|---|---:|---:|
| MEA 40 wt% | 3.695 | 3.821 GJ/tCO₂ |
| MDEA/PZ 20/20 wt% | 2.352 | 3.328 GJ/tCO₂ |
| MDEA/PZ 30/10 wt% | 2.942 | 3.591 GJ/tCO₂ |

이 조건에서 MDEA/PZ 20/20의 regeneration energy는 MEA보다 약 12.9% 낮다. 최적 L/G도 더 낮으므로 더 적은 solvent circulation으로 목표 포집률을 달성한다.

화학적으로 설명 가능한 결과다. MDEA는 bicarbonate 중심의 경로를 통해 비교적 유리한 regeneration 특성을 제공하고, PZ는 CO₂ absorption을 빠르게 한다. 30/10 혼합물보다 20/20 혼합물의 PZ 비율이 높기 때문에 gas-phase driving force나 contact time이 부족할 때 유리하다. 빠른 반응과 높은 effective cyclic capacity는 같은 포집목표에 필요한 solvent flow를 줄이고, 순환액을 가열하는 sensible heat도 낮춘다.

이 해석에는 경계가 있다. 모델은 PZ precipitation, volatilization, aerosol emission, 장기 degradation, viscosity와 관련된 모든 hydraulic penalty를 직접 포함하지 않는다. 이 결과는 모델에 포함된 공정의 energy ranking이지 solvent lifetime과 환경영향까지 포함한 종합순위가 아니다.

## L/G 곡선에 최소점이 생기는 이유

L/G와 reboiler duty 사이의 U자형 관계가 이 비교의 물리적 핵심이다.

L/G가 지나치게 낮으면 적은 용매가 많은 CO₂를 운반해야 한다. 정해진 포집률을 유지하려면 stripper에서 용매 단위량당 더 많은 CO₂를 떼어내 lean solvent에 남는 CO₂ loading을 더 낮춰야 한다. 이를 위해 추가 reboiler heat와 stripping steam이 필요하다. 운전조건에 따라 온도가 상승할 수 있지만, stripper bottom temperature를 일정하게 유지하면서 열과 steam 투입량을 늘리는 경우도 있으므로 반드시 더 높은 온도까지 가열한다는 뜻은 아니다.

L/G가 증가하면 용매 단위질량당 CO₂ 부하가 낮아진다. 극단적으로 깊은 재생이 필요하지 않으므로 처음에는 reboiler duty가 감소한다. 그러나 최적점을 지나면 필요 이상으로 많은 액체를 가열하고 펌핑하게 된다. Sensible heat가 지배적이 되면서 duty가 다시 증가한다.

최소값 하나만으로는 이 곡선을 설명할 수 없다. 최적점 주변의 local curvature가 중요하다. 논문은 최적 L/G에서 ±10% 벗어났을 때 duty 증가를 계산한다. 대략 MEA는 2–3%, MDEA/PZ 20/20은 8–12%, MDEA/PZ 30/10은 6–9%다.

MEA는 최소 duty가 가장 높지만 최적점 주변이 가장 평평하다. MDEA/PZ 20/20은 최소 duty가 가장 낮지만 최적점 주변이 가장 좁다. MDEA/PZ 30/10은 그 사이다. 운전 관점에서는 다음처럼 읽을 수 있다.

- MDEA/PZ 20/20은 정확한 L/G control의 보상이 크다.
- MEA는 energy efficiency를 희생하지만 circulation 오차에 더 관대하다.
- MDEA/PZ 30/10은 두 특성 사이의 절충안이다.

다만 이것은 one-factor local sensitivity다. Stripper pressure, lean loading, 다른 운전변수를 고정하고 L/G만 바꾸며, 모든 변수를 함께 재최적화하지 않는다. Multivariable controller는 계산된 penalty의 일부를 줄일 수 있다. ±10% 결과는 closed-loop control test가 아니다.

## 외생조건 변동은 별개의 축이다

연구는 CO₂ inlet concentration, CO₂ production rate, capture rate도 변화시킨다. 이 시나리오는 L/G perturbation과 다른 질문을 다룬다. 플랜트에 주어진 처리목표가 바뀌었을 때 공정 응답이 어떻게 달라지는지를 본다.

CO₂ 농도는 11, 13, 15 mol%로 바꾸고 CO₂ 생산량 100 tonnes/day를 유지하도록 gas flow를 조정한다. MDEA/PZ 20/20의 duty 변화는 약 3–4%로, MEA의 약 8–10%보다 작다. MDEA/PZ 30/10은 비단조적인 응답을 보인다. 낮은 CO₂ partial pressure에서는 gas-phase driving force가 약해지므로 높은 PZ 농도의 빠른 kinetics가 도움이 된다.

그러나 이것은 concentration만 분리해 변화시킨 실험이 아니다. CO₂ 생산량을 고정한 채 농도를 낮추려면 더 많은 flue gas를 처리해야 한다. 따라서 결과에는 partial-pressure effect뿐 아니라 gas velocity, contact time, column hydraulics의 변화가 함께 들어 있다. 엄밀히는 “concentration–throughput coupled sensitivity”에 가깝다.

두 변수의 coupling은 작지 않다. 13 mol%를 기준으로 동일한 captured-CO₂ product와 capture rate를 유지한다면 11 mol%에서는 molar flue-gas flow가 약 18.2% 증가하고, 15 mol%에서는 약 13.3% 감소한다. Downstream 공정이 일정한 CO₂ product rate를 요구하고 capture unit이 처리할 flue-gas fraction을 조절할 수 있다면 의미 있는 demand-following scenario다. 그러나 일반적인 발전소 disturbance를 그대로 나타내지는 않는다. 하나의 발전소에서는 load, fuel composition, excess air, air leakage가 flue-gas flow와 CO₂ concentration을 함께 결정한다. Load가 감소하면 total flue-gas flow가 크게 감소하고 concentration은 상대적으로 작게 변하는 경우가 많지만, 정확한 상관관계는 plant마다 다르다.

원인을 더 명확히 구분하려면 세 실험이 필요하다. Gas flow를 고정하고 concentration만 바꾸는 경우, concentration을 고정하고 gas flow만 바꾸는 경우, 실제 plant data에서 얻은 concentration–flow joint trajectory를 적용하는 경우다. 그다음 capture rate, inlet temperature, production target까지 함께 바꾸는 factorial grid 또는 realistic joint scenario를 평가해야 한다. 논문은 여러 parameter를 시험하지만 대부분 하나씩 바꾸거나 위의 constant-product coupling을 사용한다. 이는 steady-state scenario mapping으로는 유용하지만 simultaneous disturbance 사이의 nonlinear interaction이나 실제 joint operating distribution에서의 성능을 보여 주지는 못한다.

CO₂ 생산량을 90–110 tonnes/day로 바꾸었을 때도 MDEA/PZ 20/20의 duty 변화가 약 1–2%로 가장 작았다. MEA는 약 8–10%, MDEA/PZ 30/10은 약 3–4%다. 20/20 혼합물이 시험한 ±10% throughput 범위에서 상대적으로 둔감하다는 제한된 결론은 가능하다. 그러나 발전소의 전체 load-following 범위를 검증한 것은 아니며, 정상상태 모델에는 solvent inventory dynamics와 thermal transient가 없다.

포집률을 높이는 것은 훨씬 어렵다. 80%와 90%의 duty는 비교적 가깝지만 99%에서는 세 흡수제 모두 급격히 증가한다. 보고된 곡선에서 99% duty는 대략 MEA 5.6 GJ/tCO₂, 두 MDEA/PZ 혼합물은 각각 4.5 GJ/tCO₂ 수준이다. Absorber top으로 갈수록 남은 gas-phase CO₂ partial pressure가 매우 낮아진다. 마지막 몇 %p를 더 포집하려면 lean solvent의 CO₂ loading을 훨씬 낮춰야 하며, 이를 위해 stripper에서 더 많은 CO₂를 떼어낼 수 있도록 reboiler heat와 stripping steam 투입을 늘려야 한다.

99% case는 90% 기준조건에 맞춰 설계한 장치를 그대로 사용한다. 따라서 99%를 목적으로 새로 설계한 공정의 최소에너지가 아니라 기존 장치를 99%까지 밀어붙일 때의 penalty에 가깝다. Packing height, heat-exchanger area, circulation capacity, pressure level, intercooling, split-flow design을 다시 선택하면 결과가 달라질 수 있다.

## 여기서 “robust”가 의미하는 것

제목의 “robust”는 수학적 보장이 아니라 경험적 의미로 읽어야 한다. 논문은 선택한 off-design scenario에서 정상상태 Aspen Plus response를 mapping한다. Uncertainty set이나 probability distribution을 정의하지 않고, min–max 또는 chance-constrained problem을 풀지 않으며, simultaneous worst case나 temporal disturbance 아래에서 feedback controller를 시험하지 않는다.

Steady-state energy sensitivity가 작다고 settling time이 짧거나 overshoot가 작고, actuator saturation이 없으며, closed-loop stability가 보장되는 것은 아니다. Sampled response curve의 최저점을 찾았다고 L/G, stripper pressure, column design, 모든 disturbance에 대한 joint global optimum이 증명되는 것도 아니다.

가장 방어 가능한 해석은 좁다. 모델링된 설비, 시험한 운전범위, 수렴한 sensitivity case 안에서 MDEA/PZ 20/20은 여러 외생조건에 걸쳐 낮은 reboiler duty를 유지한다. 그러나 자체 L/G 최적점 주변에서는 circulation ratio가 벗어날 때 MEA보다 energy performance가 빠르게 나빠진다.

## 모델과 비교의 경계

Aspen Plus model은 electrolyte thermodynamics와 rate-based column을 사용하여 reaction-enhanced gas–liquid mass transfer를 표현한다. PZ kinetics와 느린 MDEA response를 구분하려면 이 정도의 모델 상세도가 필요하다. 모델은 Aspen example과 기존 문헌에서 검증된 parameter set을 기반으로 하지만, 이 연구에서 다룬 모든 solvent composition, column size, 99% off-design case를 독립적으로 pilot-scale validation하지는 않았다. Plant-validated digital twin보다는 literature- and database-based rate process model이라고 부르는 편이 정확하다.

장치 크기도 흡수제마다 다르다. 보고된 absorber height는 MEA 15 m, MDEA/PZ 20/20 20 m, MDEA/PZ 30/10 25 m이며 stripper geometry도 서로 다르다. 동일 column에서 solvent만 교체한 비교가 아니라 흡수제별로 sizing한 solvent–process system의 비교다. 신규설비의 operating energy 비교에는 합리적이지만 retrofit decision에는 부족하다.

Sensitivity analysis 동안 이 equipment dimension은 고정된다. 각 흡수제의 column은 CO₂ 13 mol%, captured CO₂ 100 tonnes/day, capture rate 90%인 nominal basis를 중심으로 별도로 sizing한 뒤, diameter, height, packing과 관련 equipment parameter를 off-design case에서도 그대로 사용한다. L/G와 stripper pressure는 sweep하는 주요 operating variable이지만 disturbance마다 equipment design을 다시 sizing하거나 operating variable과 함께 co-optimization하지 않는다.

따라서 이 장치를 수학적으로 optimal design이라고 부르는 것은 과하다. Column dimension, packing, heat-exchanger area, operating policy를 decision variable로 두고 모든 scenario 또는 total annual cost에 대해 동시에 최적화한 design problem은 제시되지 않는다. “흡수제별 nominal sizing 후 off-design operating analysis”라고 표현하는 편이 정확하다. 보고된 solvent ranking도 이 fixed design에 조건부다. 99% capture나 넓은 load-following range를 목적으로 column geometry를 다시 선택하면 energy ranking과 operating window가 달라질 수 있다.

경제성 계산도 주로 steam duty를 6 USD/GJ로 환산한다. Column과 packing의 CAPEX, pump와 blower electricity, solvent makeup, corrosion, emission control, precipitation management, instrumentation, maintenance, downtime은 제외된다. “재생증기 비용이 가장 낮다”는 결론은 지지되지만 “총비용이 가장 낮다”는 결론은 지지되지 않는다.

## 설계에 남는 의미

실무적 교훈은 하나의 solvent-ranking number를 response surface로 바꾸는 것이다. 최소한 screening 단계에서 minimum duty, optimal L/G, 최적점 주변의 local curvature, concentration과 throughput이 결합된 변동조건에서의 성능을 함께 보고해야 한다. 그 뒤 낮은 에너지 영역이 hydraulic, thermal, degradation, control constraint 아래에서도 feasible한지 확인해야 한다.

MDEA/PZ 20/20을 선택한다면 정확한 solvent-flow measurement, 충분한 pump turndown, 이동하는 최적점을 추적하는 L/G control 또는 real-time optimization strategy가 함께 필요하다. MEA의 control requirement는 덜 날카롭지만 baseline steam penalty는 남는다. 따라서 플랜트가 답해야 할 질문은 “어떤 흡수제의 최소점이 가장 낮은가?”가 아니다. “플랜트가 실제로 방문할 조건에서 어떤 solvent–equipment–control 조합이 충분히 낮은 duty를 유지하는가?”다.

가장 에너지 효율적인 흡수제가 반드시 가장 운전하기 쉬운 흡수제는 아니다.

## 참고문헌

Lim, S., Yun, S. H., Oh, J., Yoon, Y. I., Jang, J. T., & Park, J. (2026). Robust process design and operation for efficient CO₂ capture under variable supply-and-demand conditions. *Journal of Environmental Chemical Engineering, 14*, 124308. [https://doi.org/10.1016/j.jece.2026.124308](https://doi.org/10.1016/j.jece.2026.124308)
