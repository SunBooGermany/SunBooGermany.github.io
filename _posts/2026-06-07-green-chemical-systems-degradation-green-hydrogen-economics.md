---
layout: post
title: "Degradation-Aware Economics for Renewable Green Hydrogen"
title_ko: "재생에너지 기반 그린수소 경제성에서 전해조 degradation을 반영하기"
date: 2026-06-07
category: green-chemical-systems
category_label: "Green Chemical Systems"
research_group: application_reviews
research_category: green-chemical-systems
research_category_label: "Green Chemical Systems"
application_category: "green-chemical-systems"
application_category_label: "Green Chemical Systems"
method_category: ""
method_category_label: ""
paper_title: "The impact of degradation on the economics of green hydrogen"
authors: "Park, J.; Kang, S.; Kim, S.; Kim, H.; Cho, H. S.; Lee, C.; ...; Lee, J. H."
venue: "Renewable and Sustainable Energy Reviews"
year: "2025"
doi: ""
arxiv: ""
source_url: ""
tags:
  - "green hydrogen"
  - "alkaline electrolysis"
  - "techno-economic analysis"
  - "degradation"
  - "renewable intermittency"
  - "LCOH"
excerpt: "A critical note on why renewable green-hydrogen TEA should treat electrolyzer degradation, replacement, and on/off operation as endogenous economic effects rather than fixed lifetime parameters."
excerpt_ko: "재생에너지 기반 그린수소 경제성 분석에서 전해조 degradation, 교체주기, on/off 운전을 고정 수명 파라미터가 아니라 경제성을 바꾸는 내생적 효과로 보아야 하는 이유를 정리한다."
language: "en-ko"
has_korean_note: false
---

## Problem: degradation is not a small correction to green hydrogen TEA

The paper's central point is simple but important: if techno-economic analysis of renewable-powered green hydrogen ignores electrolyzer degradation, it can structurally underestimate the levelized cost of hydrogen. This is especially relevant for alkaline water electrolysis. Alkaline electrolyzers are attractive for large-scale deployment because of cost and maturity, but renewable power profiles are not smooth. Wind and photovoltaic generation can force frequent start-up and shutdown events, and those on/off operations can accelerate stack degradation.

The paper therefore treats degradation as part of actual operation: renewable variability is connected to on/off cycles, on/off cycles to degradation, degradation to efficiency loss and stack replacement, and replacement to LCOH. The causal path is:

```text
renewable variability
  -> on/off operation
  -> stack degradation
  -> efficiency loss and shorter replacement interval
  -> lower productivity and higher replacement cost
  -> higher LCOH
```

This changes the interpretation of green-hydrogen economics. The question is not only whether renewable electricity is cheap enough. It is also whether the temporal pattern of that electricity damages the electrolyzer often enough to change the economic optimum.

## Architecture: experiment-calibrated process-system TEA

The modeling flow is:

```text
meteorological data
  -> WT and PV generation models
  -> hourly renewable electricity profile
  -> electrolyzer on/off decision under minimum part-load
  -> alkaline electrolyzer I-V and hydrogen production model
  -> normal degradation plus on/off degradation
  -> efficiency trajectory and stack replacement schedule
  -> CAPEX, OPEX, replacement cost, hydrogen production
  -> LCOH
```

The key modeling move is that the degradation trajectory is generated from the operation profile rather than assigned as a fixed lifetime number. Wind and solar generation are first converted into hourly power availability. If renewable power is above the minimum part-load, the electrolyzer operates; if not, it shuts down. An ESS can smooth part of this fluctuation, but it also adds cost and round-trip losses.

The alkaline electrolyzer model maps power input to current, voltage, Faraday efficiency, and hydrogen production. Degradation then modifies the efficiency trajectory over time. Once the efficiency reaches a replacement threshold, the stack is replaced and efficiency is reset.

## Degradation model and economic mechanism

The paper separates degradation into normal operating degradation and on/off degradation:

<math display="block" aria-label="Degradation accumulation">
  <msub><mi>D</mi><mi>t</mi></msub>
  <mo>=</mo>
  <msub><mi>D</mi><mrow><mi>t</mi><mo>-</mo><mn>1</mn></mrow></msub>
  <mo>+</mo>
  <msub><mi>&gamma;</mi><mi>normal</mi></msub>
  <msub><mi>h</mi><mi>t</mi></msub>
  <mo>+</mo>
  <msub><mi>&gamma;</mi><mrow><mi>on</mi><mo>/</mo><mi>off</mi></mrow></msub>
  <msubsup><mi>N</mi><mi>t</mi><mrow><mi>on</mi><mo>/</mo><mi>off</mi></mrow></msubsup>
  <mo>.</mo>
</math>

In the paper's experimental setting, the normal degradation rate is 0.00013% per hour and the on/off degradation rate is 0.00109% per operation. The normal component is based on a target lifetime assumption, while the on/off component is calibrated from a single-cell accelerated stress test with 500 cycles between 0.6 A/cm2 and 0 A/cm2 at one-minute intervals.

This is valuable because it links a materials-level degradation experiment to a system-level cost metric. The model does not merely say that lower efficiency reduces hydrogen output. It also captures the second economic channel: faster degradation shortens the replacement interval, and replacement cost can dominate the economic penalty.

The LCOH mechanism can be summarized as:

<math display="block" aria-label="LCOH degradation channels">
  <msub><mi>D</mi><mi>t</mi></msub>
  <mo>&uarr;</mo>
  <mo>&rArr;</mo>
  <msub><mi>&eta;</mi><mrow><mi>EL</mi><mo>,</mo><mi>t</mi></mrow></msub>
  <mo>&darr;</mo>
  <mo>&rArr;</mo>
  <msub><mi>M</mi><msub><mi>H</mi><mn>2</mn></msub></msub>
  <mo>&darr;</mo>
  <mo>&rArr;</mo>
  <mi>LCOH</mi>
  <mo>&uarr;</mo>
  <mspace width="1em"></mspace>
  <mtext>and</mtext>
  <mspace width="1em"></mspace>
  <msub><mi>D</mi><mi>t</mi></msub>
  <mo>&uarr;</mo>
  <mo>&rArr;</mo>
  <msub><mi>&tau;</mi><mi>replace</mi></msub>
  <mo>&darr;</mo>
  <mo>&rArr;</mo>
  <msub><mi>C</mi><mi>replace</mi></msub>
  <mo>&uarr;</mo>
  <mo>&rArr;</mo>
  <mi>LCOH</mi>
  <mo>&uarr;</mo>
</math>

## Main results: replacement cost matters more than the obvious efficiency loss

For the base design used in the paper's experiment, the paper compares a 100 MW alkaline electrolyzer with 200 MW wind and 100 MW photovoltaic capacity. The reported cases are:

```text
No degradation:              LCOH 7.6 USD/kg, hydrogen production 1404 kg/h
Normal degradation:          LCOH 8.8 USD/kg, hydrogen production 1342 kg/h
Normal + on/off degradation: LCOH 9.8 USD/kg, hydrogen production 1342 kg/h
```

The interesting part is that adding on/off degradation does not mainly change average hydrogen production relative to the normal-degradation case. Its larger effect is to shorten the stack replacement interval, from the supplied-note figure of about 6.5 years under normal degradation to about 4.9 years when on/off degradation is included.

That makes the economic message sharper. In renewable electrolysis TEA, degradation is not only an efficiency-loss issue. It is also a maintenance and replacement scheduling issue. A model that only updates the production denominator can miss the cost-side effect that actually drives LCOH.

## Renewable mix: PV, wind, and hybrid profiles do not degrade stacks the same way

The paper's application insight is strongest when it compares renewable profiles. PV-only systems can experience frequent daily shutdowns because solar generation follows a deterministic day-night pattern. The paper reports that PV-only operation can exceed 700 on/off operations per year. That makes PV-only designs particularly exposed to on/off degradation.

Wind-only operation is not automatically smooth, but its variability is different. Wind may continue at night and does not necessarily impose the same daily zero-generation structure. Hybrid wind-PV systems can therefore reduce low-power gaps by temporal complementarity:

```text
PV-only:
  daily zero-generation pattern
  -> frequent shutdown
  -> high on/off degradation exposure

WT-only:
  stochastic variability
  -> possible night-time generation
  -> different on/off structure

Hybrid WT/PV:
  temporal complementarity
  -> fewer low-power gaps
  -> reduced degradation cost
```

This is more subtle than saying "hybrid renewables have a higher capacity factor." The degradation-aware view asks how the shape of the power profile changes electrolyzer switching frequency and stack life.

## ESS and replacement threshold: design variables, not afterthoughts

The battery result is also a useful warning. ESS can reduce fluctuations and on/off cycles, but the economic benefit is not automatic. A battery helps only when the avoided degradation cost plus additional utilization benefit exceeds battery CAPEX, OPEX, and round-trip loss:

<math display="block" aria-label="Battery economic condition">
  <mi>&Delta;</mi><msub><mi>C</mi><mi>degradation</mi></msub>
  <mo>+</mo>
  <mi>&Delta;</mi><msub><mi>C</mi><mi>utilization</mi></msub>
  <mo>&gt;</mo>
  <msub><mi>C</mi><mi>ESS</mi></msub>
  <mo>.</mo>
</math>

The paper indicates that larger batteries often do not improve LCOH, especially when renewable capacity is not large enough to create useful surplus energy. In large PV-heavy cases, such as the cited 700 MW PV-only setting, battery integration can become more defensible because it both increases utilization and reduces on/off cycling.

The replacement threshold creates another trade-off. Replacing the stack too early raises replacement cost. Replacing it too late keeps a degraded stack in service and reduces productivity. The paper reports an interior optimum around an efficiency threshold of roughly 0.60 for normal degradation and about 0.55-0.60 when on/off degradation is included. This is not a universal threshold for all plants. It is a scenario result that shows replacement policy is part of the design problem.

## Limitations

The first limitation is that degradation is simplified into normal degradation and on/off degradation. Normal degradation is treated as proportional to operating time, and on/off degradation is treated as proportional to the number of on/off events. This is useful for system-level TEA, but real degradation can be much more complex because it depends on current, temperature, pressure, ramping, off duration, stack state, and balance-of-plant operation.

The second limitation is that the operation rule is deliberately simple. Capacity choices and replacement thresholds are explored through scenario tables rather than solved as an optimization problem. As the system becomes more complex, this table-based approach may not scale directly to realistic design and control decisions.

## Takeaway

The paper is most useful because it makes electrolyzer lifetime endogenous to renewable operation. It shows that green hydrogen economics can be distorted if efficiency and lifetime are treated as fixed parameters, especially when PV-driven daily shutdowns or renewable intermittency create frequent stack stress.

Its contribution is not that degradation always makes one technology or design universally worse. The contribution is the modeling connection: renewable profile -> on/off operation -> degradation trajectory -> replacement schedule -> LCOH. That connection makes hybrid renewable design, ESS sizing, and replacement threshold part of the same economic question.

For follow-up research, the natural next step is degradation-aware optimal operation and design under uncertainty. The present paper provides a strong motivation for that direction, while also leaving open the harder questions of stack-scale degradation validity, nonlinear degradation laws, and stochastic operational control.

## References

Park, J., Kang, S., Kim, S., Kim, H., Cho, H. S., Lee, C., ... & Lee, J. H. (2025). The impact of degradation on the economics of green hydrogen. Renewable and Sustainable Energy Reviews, 213, 115472.

<!-- ko -->

## 문제: degradation은 그린수소 TEA의 작은 보정항이 아니다

이 논문의 핵심 문제의식은 단순하지만 중요하다. 재생에너지 기반 그린수소의 techno-economic analysis에서 전해조 degradation을 무시하면 LCOH가 구조적으로 과소평가될 수 있다. 특히 알칼라인 수전해는 대규모화와 비용 측면에서 매력적이지만, 재생에너지 전력 profile은 매끄럽지 않다. WT와 PV의 변동성은 잦은 start-up과 shutdown을 만들 수 있고, 이러한 on/off operation은 stack degradation을 가속할 수 있다.

따라서 이 논문은 degradation을 실제 운영 과정에서 재생에너지 변동성을 on/off cycle과 연결하고, on/off cycle을 degradation과 연결하며, degradation을 효율 저하와 stack 교체주기 단축, 그리고 LCOH 변화와 연결한다. 핵심 경로는 다음과 같다.

```text
renewable variability
  -> on/off operation
  -> stack degradation
  -> efficiency loss and shorter replacement interval
  -> lower productivity and higher replacement cost
  -> higher LCOH
```

이 관점은 그린수소 경제성의 질문을 바꾼다. 단순히 재생에너지 전기가 충분히 싼가를 묻는 것이 아니라, 그 전기의 시간적 pattern이 전해조를 얼마나 자주 손상시키고 그 손상이 경제적 최적점을 얼마나 바꾸는지를 묻는다.

## Architecture: 실험으로 보정된 process-system TEA

모델 흐름은 다음과 같다.

```text
meteorological data
  -> WT and PV generation models
  -> hourly renewable electricity profile
  -> electrolyzer on/off decision under minimum part-load
  -> alkaline electrolyzer I-V and hydrogen production model
  -> normal degradation plus on/off degradation
  -> efficiency trajectory and stack replacement schedule
  -> CAPEX, OPEX, replacement cost, hydrogen production
  -> LCOH
```

핵심 modeling move는 degradation trajectory를 고정 수명 숫자로 두지 않고 operation profile에서 생성한다는 점이다. 풍력과 태양광 발전량을 먼저 시간별 전력 availability로 변환한다. 재생에너지 전력이 minimum part-load 이상이면 전해조가 운전되고, 부족하면 꺼진다. ESS는 이 변동성을 일부 완화할 수 있지만, 동시에 비용과 round-trip loss를 추가한다.

Alkaline electrolyzer model은 power input을 current, voltage, Faraday efficiency, hydrogen production으로 변환한다. 이후 degradation이 시간에 따른 efficiency trajectory를 바꾼다. 효율이 replacement threshold에 도달하면 stack을 교체하고 efficiency를 reset한다.

## Degradation model과 경제적 mechanism

논문은 degradation을 normal operating degradation과 on/off degradation으로 나눈다.

<math display="block" aria-label="Degradation accumulation">
  <msub><mi>D</mi><mi>t</mi></msub>
  <mo>=</mo>
  <msub><mi>D</mi><mrow><mi>t</mi><mo>-</mo><mn>1</mn></mrow></msub>
  <mo>+</mo>
  <msub><mi>&gamma;</mi><mi>normal</mi></msub>
  <msub><mi>h</mi><mi>t</mi></msub>
  <mo>+</mo>
  <msub><mi>&gamma;</mi><mrow><mi>on</mi><mo>/</mo><mi>off</mi></mrow></msub>
  <msubsup><mi>N</mi><mi>t</mi><mrow><mi>on</mi><mo>/</mo><mi>off</mi></mrow></msubsup>
  <mo>.</mo>
</math>

논문에서 진행된 실험 기준으로 normal degradation rate는 시간당 0.00013%, on/off degradation rate는 operation당 0.00109%다. Normal component는 target lifetime assumption에 기반하고, on/off component는 0.6 A/cm2와 0 A/cm2를 1분 간격으로 500회 반복하는 single-cell accelerated stress test에서 보정된다.

이 점이 중요한 이유는 materials-level degradation 실험을 system-level cost metric과 연결하기 때문이다. 모델은 단지 효율이 낮아져 수소 생산량이 줄어든다고만 말하지 않는다. 더 중요한 두 번째 경제적 channel, 즉 faster degradation이 replacement interval을 줄이고 replacement cost를 키운다는 점을 함께 잡는다.

LCOH mechanism은 다음처럼 요약할 수 있다.

<math display="block" aria-label="LCOH degradation channels">
  <msub><mi>D</mi><mi>t</mi></msub>
  <mo>&uarr;</mo>
  <mo>&rArr;</mo>
  <msub><mi>&eta;</mi><mrow><mi>EL</mi><mo>,</mo><mi>t</mi></mrow></msub>
  <mo>&darr;</mo>
  <mo>&rArr;</mo>
  <msub><mi>M</mi><msub><mi>H</mi><mn>2</mn></msub></msub>
  <mo>&darr;</mo>
  <mo>&rArr;</mo>
  <mi>LCOH</mi>
  <mo>&uarr;</mo>
  <mspace width="1em"></mspace>
  <mtext>and</mtext>
  <mspace width="1em"></mspace>
  <msub><mi>D</mi><mi>t</mi></msub>
  <mo>&uarr;</mo>
  <mo>&rArr;</mo>
  <msub><mi>&tau;</mi><mi>replace</mi></msub>
  <mo>&darr;</mo>
  <mo>&rArr;</mo>
  <msub><mi>C</mi><mi>replace</mi></msub>
  <mo>&uarr;</mo>
  <mo>&rArr;</mo>
  <mi>LCOH</mi>
  <mo>&uarr;</mo>
</math>

## 주요 결과: obvious한 efficiency loss보다 replacement cost가 중요하다

논문에서 진행된 실험 기준으로 base design은 100 MW alkaline electrolyzer, 200 MW WT, 100 MW PV다. 논문은 다음 세 경우를 비교한다.

```text
No degradation:              LCOH 7.6 USD/kg, hydrogen production 1404 kg/h
Normal degradation:          LCOH 8.8 USD/kg, hydrogen production 1342 kg/h
Normal + on/off degradation: LCOH 9.8 USD/kg, hydrogen production 1342 kg/h
```

흥미로운 점은 on/off degradation을 추가해도 normal degradation case 대비 평균 hydrogen production이 크게 바뀌지 않는다는 것이다. 더 큰 효과는 stack replacement interval이 짧아지는 데서 온다. 제공된 노트에 따르면 normal degradation에서는 약 6.5년, on/off degradation까지 고려하면 약 4.9년으로 줄어든다.

따라서 경제적 메시지는 더 날카롭다. Renewable electrolysis TEA에서 degradation은 단순한 efficiency-loss 문제가 아니다. 유지보수와 replacement scheduling 문제이기도 하다. 생산량 denominator만 업데이트하는 모델은 실제 LCOH를 지배하는 cost-side effect를 놓칠 수 있다.

## Renewable mix: PV, wind, hybrid profile은 stack을 다르게 손상시킨다

이 논문의 application insight는 renewable profile 비교에서 가장 잘 드러난다. PV-only system은 낮과 밤의 deterministic pattern 때문에 거의 매일 shutdown을 겪을 수 있다. 제공된 노트는 PV-only operation에서 연간 700회 이상의 on/off operation이 발생할 수 있다고 정리한다. 이 때문에 PV-only design은 on/off degradation에 특히 취약하다.

Wind-only operation은 자동으로 smooth한 것은 아니지만 variability의 구조가 다르다. Wind는 야간에도 발전할 수 있고, PV처럼 매일 zero-generation pattern을 강제하지 않는다. Hybrid wind-PV system은 temporal complementarity를 통해 low-power gap을 줄일 수 있다.

```text
PV-only:
  daily zero-generation pattern
  -> frequent shutdown
  -> high on/off degradation exposure

WT-only:
  stochastic variability
  -> possible night-time generation
  -> different on/off structure

Hybrid WT/PV:
  temporal complementarity
  -> fewer low-power gaps
  -> reduced degradation cost
```

이는 단순히 hybrid renewable의 capacity factor가 높다는 말보다 더 미묘하다. Degradation-aware view는 power profile의 모양이 electrolyzer switching frequency와 stack life를 어떻게 바꾸는지를 묻는다.

## ESS와 replacement threshold: 사후 보정이 아니라 design variable

Battery result도 유용한 경고를 준다. ESS는 fluctuation과 on/off cycle을 줄일 수 있지만, 경제적 이득이 자동으로 생기지는 않는다. Battery가 유리하려면 avoided degradation cost와 utilization benefit이 battery CAPEX, OPEX, round-trip loss를 넘어야 한다.

<math display="block" aria-label="Battery economic condition">
  <mi>&Delta;</mi><msub><mi>C</mi><mi>degradation</mi></msub>
  <mo>+</mo>
  <mi>&Delta;</mi><msub><mi>C</mi><mi>utilization</mi></msub>
  <mo>&gt;</mo>
  <msub><mi>C</mi><mi>ESS</mi></msub>
  <mo>.</mo>
</math>

제공된 노트에 따르면 battery size 증가는 많은 경우 LCOH를 개선하지 않는다. 특히 renewable capacity가 충분하지 않아 useful surplus energy가 생기지 않으면 비용만 커질 수 있다. 반면 700 MW PV-only setting처럼 PV capacity가 매우 큰 경우에는 battery integration이 utilization 증가와 on/off cycle 감소 측면에서 더 설득력을 가질 수 있다.

Replacement threshold도 또 하나의 trade-off다. Stack을 너무 빨리 교체하면 replacement cost가 커진다. 너무 늦게 교체하면 degraded stack으로 운전하므로 productivity가 낮아진다. 논문은 normal degradation에서는 efficiency threshold 약 0.60, normal + on/off degradation에서는 약 0.55-0.60 부근의 interior optimum을 보고한다. 이 값은 모든 plant에 적용되는 보편 threshold가 아니라, replacement policy가 design problem의 일부임을 보여주는 scenario result다.

## 한계점

첫 번째 한계는 degradation을 normal degradation과 on/off degradation으로 단순화했다는 점이다. Normal degradation은 운영 시간에 정비례하고, on/off degradation은 on/off 횟수에 정비례한다고 둔다. 이는 system-level TEA에는 유용하지만, 실제 degradation은 current, temperature, pressure, ramping, off duration, stack state, balance-of-plant operation 등에 따라 훨씬 더 복잡할 수 있다.

두 번째 한계는 operation rule이 의도적으로 단순하다는 점이다. Capacity를 정하거나 replacement threshold를 정하는 과정도 최적화 문제를 푼 것이 아니라 scenario table 형태로 탐색한 것에 가깝다. 따라서 시스템이 더 복잡해지면 현재 접근법을 그대로 realistic design/control decision에 적용하기는 어렵다.

## Takeaway

이 논문이 유용한 이유는 electrolyzer lifetime을 renewable operation의 내생적 결과로 만든다는 데 있다. Efficiency와 lifetime을 고정 parameter로 두면 green hydrogen economics가 왜곡될 수 있음을 보여주며, 특히 PV-driven daily shutdown이나 renewable intermittency가 잦은 stack stress를 만드는 경우 그 문제가 커진다.

논문의 contribution은 degradation이 모든 기술이나 설계를 보편적으로 나쁘게 만든다는 말이 아니다. 핵심은 modeling connection이다. Renewable profile -> on/off operation -> degradation trajectory -> replacement schedule -> LCOH. 이 연결을 넣으면 hybrid renewable design, ESS sizing, replacement threshold가 같은 경제성 질문 안으로 들어온다.

후속 연구로는 degradation-aware optimal operation and design under uncertainty가 자연스럽다. 현재 논문은 그 방향의 필요성을 강하게 보여주지만, stack-scale degradation validity, nonlinear degradation law, stochastic operational control이라는 더 어려운 문제는 아직 열어 둔다.

## References

Park, J., Kang, S., Kim, S., Kim, H., Cho, H. S., Lee, C., ... & Lee, J. H. (2025). The impact of degradation on the economics of green hydrogen. Renewable and Sustainable Energy Reviews, 213, 115472.
