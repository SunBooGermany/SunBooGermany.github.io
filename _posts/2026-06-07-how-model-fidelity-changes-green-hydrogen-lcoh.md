---
layout: post
title: "How Model Fidelity Changes Green Hydrogen LCOH"
title_ko: "모델 충실도가 그린수소 LCOH를 바꾸는 방식"
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
paper_title: "Impact of electrolyzer-model fidelity and renewable-data resolution on techno-economic assessments of green hydrogen systems"
authors: "Kang, B.; Kim, H.; Park, J."
venue: "Energy Conversion and Management"
year: "2026"
doi: ""
arxiv: ""
source_url: ""
tags:
  - "green hydrogen"
  - "techno-economic analysis"
  - "electrolyzer modeling"
  - "renewable intermittency"
  - "PEM electrolysis"
  - "LCOH"
excerpt: "A critical note on how fixed-efficiency electrolyzer models and low-resolution renewable data can bias green-hydrogen LCOH estimates."
excerpt_ko: "고정 효율 전해조 모델과 낮은 해상도의 재생에너지 데이터가 그린수소 LCOH 추정에 어떤 bias를 만드는지 비판적으로 정리한다."
language: "en-ko"
has_korean_note: false
---

## Problem: TEA can hide the operating physics between renewable power and LCOH

Green-hydrogen techno-economic analysis often has a simple computational chain:

```text
renewable power time series
  -> electrolyzer model
  -> hydrogen production
  -> LCOH
```

The weak point is the middle of the chain. Many TEA studies use a fixed electrolyzer efficiency, so hydrogen production is treated as nearly proportional to input power:

<math display="block" aria-label="Fixed efficiency hydrogen production">
  <msub><mover><mi>m</mi><mo>&#x02D9;</mo></mover><mrow><msub><mi>H</mi><mn>2</mn></msub><mo>,</mo><mi>t</mi></mrow></msub>
  <mo>&#x2248;</mo>
  <mfrac>
    <mrow><msub><mi>&eta;</mi><mtext>fixed</mtext></msub><msub><mi>P</mi><mi>t</mi></msub></mrow>
    <msub><mi>HHV</mi><msub><mi>H</mi><mn>2</mn></msub></msub>
  </mfrac>
  <mo>.</mo>
</math>

That is convenient, but it hides load-dependent behavior. A PEM electrolyzer does not have one efficiency number. Its cell voltage and efficiency change with current density, part-load operation, overload, activation loss, ohmic loss, and diffusion loss. If a renewable-powered electrolyzer spends much of its time away from the design point, a fixed-efficiency TEA is not a harmless simplification.

The second simplification is temporal aggregation. Hourly wind and solar output contain zero-output periods, curtailment, short peaks, and overload opportunities. If the same resource profile is replaced by daily or monthly averages, the electrolyzer can appear to run more smoothly than it actually would. Hydrogen output and LCOH then become artifacts of the data resolution.

The paper asks a useful practical question: how much fidelity is needed in the electrolyzer model and renewable-data resolution before a green-hydrogen LCOH estimate becomes credible?

## Where this paper sits

The contribution is a systematic comparison of TEA modeling choices:

```text
fixed-efficiency PEMEL
  vs variable-efficiency I-V PEMEL

hourly renewable data
  vs daily averages
  vs monthly averages

WT, PV, and hybrid WT+PV systems
  under overload and minimum part-load assumptions

multi-year weather
  across Korea, China, Australia, and Germany
```

That makes the paper valuable as a bias study. It does not prove that one model is universally correct. It shows how seemingly modest modeling choices can move the economics by several percent, and in temporal-resolution cases by much more.

## Modeling architecture

The framework is straightforward:

```text
meteorological data
  -> wind speed, solar irradiance, ambient temperature
  -> WT and PV generation models
  -> fixed-efficiency or variable-efficiency PEMEL model
  -> hydrogen production
  -> CAPEX and OPEX
  -> LCOH
  -> scenario comparison
```

Wind generation is computed through a piecewise turbine power curve with cut-in, rated, and cut-out speeds. PV output uses irradiance and ambient-temperature-dependent module efficiency. The electrolyzer is then represented in two ways.

The fixed-efficiency model uses the efficiency at the design current density, <math><mi>i</mi><mo>=</mo><mn>2</mn><mtext> A </mtext><msup><mtext>cm</mtext><mrow><mo>-</mo><mn>2</mn></mrow></msup></math>, for all operating points:

<math display="block" aria-label="Fixed electrolyzer efficiency">
  <msub><mi>&eta;</mi><mtext>EL</mtext></msub>
  <mo>(</mo><mi>i</mi><mo>)</mo>
  <mo>=</mo>
  <msub><mi>&eta;</mi><mtext>design</mtext></msub>
  <mo>.</mo>
</math>

The variable-efficiency model uses a steady-state I-V approximation:

<math display="block" aria-label="PEM electrolyzer cell voltage">
  <msub><mi>V</mi><mtext>cell</mtext></msub>
  <mo>=</mo>
  <msub><mi>E</mi><mtext>rev</mtext></msub>
  <mo>+</mo>
  <msub><mi>&eta;</mi><mtext>act</mtext></msub>
  <mo>+</mo>
  <msub><mi>&eta;</mi><mtext>ohm</mtext></msub>
  <mo>+</mo>
  <msub><mi>&eta;</mi><mtext>diff</mtext></msub>
  <mo>.</mo>
</math>

This is still not a full dynamic electrolyzer model. Thermal dynamics, start-up and shut-down behavior, pressure dynamics, ramp-rate constraints, and cycling-driven degradation are outside the model. The improvement is narrower: efficiency changes with operating current instead of being pinned to one design-point value.

The economic metric is LCOH. The paper assumes a 25-year lifetime, 7% discount rate, and 8000 h annual operating time. Those choices matter for absolute values, but the paper's main point is the relative bias caused by model fidelity and time resolution.

## Why fixed efficiency creates bias

A fixed-efficiency model is close to replacing an entire efficiency curve with one point. The accumulated hydrogen-production error can be read as:

<math display="block" aria-label="Hydrogen production bias from fixed efficiency">
  <mi>&Delta;</mi><mi>H</mi>
  <mo>=</mo>
  <munder><mo>&sum;</mo><mi>t</mi></munder>
  <msub><mi>P</mi><mi>t</mi></msub>
  <mo>[</mo>
  <msub><mi>&eta;</mi><mtext>var</mtext></msub>
  <mo>(</mo><msub><mi>i</mi><mi>t</mi></msub><mo>)</mo>
  <mo>-</mo>
  <msub><mi>&eta;</mi><mtext>design</mtext></msub>
  <mo>]</mo>
  <mo>.</mo>
</math>

The sign is not predetermined. If the electrolyzer often operates at moderate part-load where the variable-efficiency model is better than the design-point efficiency, the fixed model underestimates hydrogen production. If the electrolyzer often operates in overload where ohmic and diffusion losses become larger, the fixed model can overestimate production by ignoring the efficiency penalty.

This is the most important nuance in the paper. The claim is not "variable efficiency always gives a more optimistic TEA." In the baseline Korean cases, the variable-efficiency model gives higher hydrogen production and lower LCOH. WT falls from USD 6.02/kg to USD 5.73/kg, PV from USD 4.12/kg to USD 4.01/kg, and hybrid from USD 4.57/kg to USD 4.35/kg. But as overload increases, the advantage of the variable model shrinks because high-current operation carries an efficiency cost that the fixed model cannot see.

So the better statement is: fixed-efficiency bias is controlled by the distribution of current density, not by a universal direction of error.

## Why temporal aggregation is dangerous

With hourly data, hydrogen production is computed as:

<math display="block" aria-label="Hourly hydrogen production">
  <msub><mi>H</mi><mtext>hourly</mtext></msub>
  <mo>=</mo>
  <munder><mo>&sum;</mo><mi>t</mi></munder>
  <mi>f</mi>
  <mo>(</mo><msub><mi>P</mi><mi>t</mi></msub><mo>)</mo>
  <mo>.</mo>
</math>

If the same interval is replaced by a daily or monthly average, the calculation becomes closer to:

<math display="block" aria-label="Aggregated hydrogen production">
  <msub><mi>H</mi><mtext>agg</mtext></msub>
  <mo>=</mo>
  <mo>|</mo><mi>T</mi><mo>|</mo>
  <mi>f</mi>
  <mo>(</mo>
  <mfrac>
    <mn>1</mn>
    <mrow><mo>|</mo><mi>T</mi><mo>|</mo></mrow>
  </mfrac>
  <munder><mo>&sum;</mo><mrow><mi>t</mi><mo>&#x2208;</mo><mi>T</mi></mrow></munder>
  <msub><mi>P</mi><mi>t</mi></msub>
  <mo>)</mo>
  <mo>.</mo>
</math>

These are equal only under restrictive conditions. The function <math><mi>f</mi></math> is not linear; it contains renewable power conversion, current mapping, electrolyzer efficiency, capacity limits, overload rules, curtailment, and zero-output periods. Therefore <math><mi>f</mi><mo>(</mo><mi>E</mi><mo>[</mo><mi>P</mi><mo>]</mo><mo>)</mo></math> is not generally equal to <math><mi>E</mi><mo>[</mo><mi>f</mi><mo>(</mo><mi>P</mi><mo>)</mo><mo>]</mo></math>.

The Korea hybrid case shows the scale of the problem:

| Temporal resolution | LCOH | Hydrogen production |
| --- | ---: | ---: |
| Hourly | USD 4.35/kg | 940 kg/h |
| Daily | USD 3.79/kg | 1066 kg/h |
| Monthly | USD 3.57/kg | 1125 kg/h |

Daily and monthly aggregation make the system look smoother, more continuously operated, and cheaper. In this case they raise estimated hydrogen production by roughly 13% and 20%.

But again, the direction is not a theorem. The paper notes cases where the relationship between daily and monthly data is not monotone. Wind power is strongly nonlinear in wind speed, and averaging wind speed before applying a turbine power curve is not equivalent to averaging power. Temporal aggregation bias includes both renewable-generation nonlinearity and electrolyzer-operation nonlinearity. The paper would be stronger if it decomposed those two effects explicitly.

## Hybrid WT+PV and variability

The hybrid result is intuitive. If wind and solar do not peak at the same times, the variance of combined renewable power can be lower than either single source after normalization:

<math display="block" aria-label="Hybrid renewable variance">
  <mi>Var</mi>
  <mo>(</mo><msub><mi>P</mi><mtext>WT</mtext></msub><mo>+</mo><msub><mi>P</mi><mtext>PV</mtext></msub><mo>)</mo>
  <mo>=</mo>
  <mi>Var</mi><mo>(</mo><msub><mi>P</mi><mtext>WT</mtext></msub><mo>)</mo>
  <mo>+</mo>
  <mi>Var</mi><mo>(</mo><msub><mi>P</mi><mtext>PV</mtext></msub><mo>)</mo>
  <mo>+</mo>
  <mn>2</mn><mi>Cov</mi><mo>(</mo><msub><mi>P</mi><mtext>WT</mtext></msub><mo>,</mo><msub><mi>P</mi><mtext>PV</mtext></msub><mo>)</mo>
  <mo>.</mo>
</math>

The multi-year results are consistent with this. Hybrid systems have smaller year-to-year LCOH variation than WT-only or PV-only systems. For the hybrid case, the LCOH standard deviation is about USD 0.082/kg under the fixed model and USD 0.072/kg under the variable model.

This is useful, but not universal. Hybrid advantage depends on the local covariance structure. If wind and solar are simultaneously weak in a region or season, the smoothing effect can be much weaker.

## What is reliable, and what is still weak

Several conclusions are structurally reliable:

1. A fixed-efficiency model is a point approximation of a load-dependent electrolyzer curve.
2. Temporal aggregation of a nonlinear operating model generally creates bias.
3. WT+PV hybridization can reduce variability when wind and solar profiles are complementary.

The weaker part is the operational realism. The variable PEMEL model is steady-state. It does not model transient dynamics, cycling degradation, pressure dynamics, start-up and shut-down costs, thermal constraints, or warranty-limited overload behavior. The overload rule is also stylized, closer to a sensitivity assumption than a dispatch policy.

The sizing structure is another limitation. The electrolyzer capacity is fixed at 100 MW while renewable capacity is adjusted for LCOH. That is useful for isolating fidelity and resolution effects, but a real project would jointly size electrolyzer, PV, wind, storage, and possibly grid interaction. Once storage, PPA structure, curtailment compensation, hydrogen storage, and transport enter the problem, the value of hourly resolution may become even more coupled to system design.

The cross-country comparison should also be read carefully. A representative site in Korea, China, Australia, or Germany is not the same as a national resource assessment. The absolute ranking is less important than the repeated pattern: model fidelity and temporal resolution can move LCOH enough to change early project-screening decisions.

## Critical take

The strongest part of this paper is its refusal to treat TEA inputs as neutral bookkeeping. Electrolyzer efficiency fidelity and renewable-data resolution are modeling choices, and those choices can become economic claims. In the baseline scenarios, variable-efficiency PEMEL modeling lowers LCOH by a few percent. In the temporal-resolution comparison, daily and monthly aggregation can overstate hydrogen output by much more.

The paper should not be read as proving that hourly data plus a variable-efficiency PEMEL model is always "correct." It shows something narrower and more useful: when renewable intermittency and nonlinear electrolyzer physics are present, fixed efficiency and low-resolution data create structural bias. The size and direction of that bias depend on current-density distribution, renewable-resource distribution, capacity ratio, and overload rule.

For green-hydrogen screening, that is already enough. If a project is economically marginal, a few percent from electrolyzer fidelity and a 10-20% production shift from temporal aggregation are not details. They can change whether the project looks viable.

## References

- Kang, B., Kim, H., & Park, J. (2026). Impact of electrolyzer-model fidelity and renewable-data resolution on techno-economic assessments of green hydrogen systems. *Energy Conversion and Management*, 364, 121676.

<!-- ko -->

## 문제: TEA는 재생에너지 출력과 LCOH 사이의 운전 물리를 숨길 수 있다

그린수소 techno-economic analysis는 보통 다음과 같은 계산 사슬로 구성된다.

```text
renewable power time series
  -> electrolyzer model
  -> hydrogen production
  -> LCOH
```

취약한 지점은 중간 단계다. 많은 TEA 연구는 전해조 효율을 고정값으로 두고, 수소 생산량을 입력 전력에 거의 비례하는 형태로 계산한다.

<math display="block" aria-label="Fixed efficiency hydrogen production">
  <msub><mover><mi>m</mi><mo>&#x02D9;</mo></mover><mrow><msub><mi>H</mi><mn>2</mn></msub><mo>,</mo><mi>t</mi></mrow></msub>
  <mo>&#x2248;</mo>
  <mfrac>
    <mrow><msub><mi>&eta;</mi><mtext>fixed</mtext></msub><msub><mi>P</mi><mi>t</mi></msub></mrow>
    <msub><mi>HHV</mi><msub><mi>H</mi><mn>2</mn></msub></msub>
  </mfrac>
  <mo>.</mo>
</math>

이 가정은 편하지만 load-dependent behavior를 지운다. PEM electrolyzer의 효율은 하나의 숫자가 아니다. current density, part-load 운전, overload, activation loss, ohmic loss, diffusion loss에 따라 cell voltage와 효율이 달라진다. 재생에너지 기반 전해조가 design point에서 벗어난 시간에 많이 머문다면, fixed-efficiency TEA는 무해한 단순화가 아니다.

두 번째 단순화는 temporal aggregation이다. hourly 풍력과 태양광 출력에는 zero-output period, curtailment, 짧은 peak, overload opportunity가 있다. 그런데 같은 resource profile을 daily 또는 monthly average로 바꾸면, 전해조가 실제보다 훨씬 부드럽게 운전되는 것처럼 보일 수 있다. 그러면 hydrogen output과 LCOH는 데이터 해상도의 산물이 된다.

이 논문이 묻는 질문은 실용적이다. 그린수소 LCOH 추정이 신뢰 가능하려면 electrolyzer model fidelity와 renewable-data resolution을 어느 정도까지 반영해야 하는가?

## 이 논문의 위치

이 논문의 기여는 TEA modeling choice를 체계적으로 비교한 bias study에 가깝다.

```text
fixed-efficiency PEMEL
  vs variable-efficiency I-V PEMEL

hourly renewable data
  vs daily averages
  vs monthly averages

WT, PV, hybrid WT+PV systems
  under overload and minimum part-load assumptions

multi-year weather
  across Korea, China, Australia, and Germany
```

따라서 이 논문은 어떤 모델이 보편적으로 옳다는 것을 증명하기보다, 사소해 보이는 모델링 선택이 economics를 수 % 이상, temporal-resolution case에서는 훨씬 더 크게 움직일 수 있음을 보여준다.

## 모델링 구조

전체 framework는 단순하다.

```text
meteorological data
  -> wind speed, solar irradiance, ambient temperature
  -> WT and PV generation models
  -> fixed-efficiency or variable-efficiency PEMEL model
  -> hydrogen production
  -> CAPEX and OPEX
  -> LCOH
  -> scenario comparison
```

풍력은 cut-in, rated, cut-out speed를 갖는 piecewise turbine power curve로 계산한다. PV 출력은 irradiance와 ambient temperature에 따른 module efficiency를 사용한다. 전해조는 두 방식으로 표현된다.

Fixed-efficiency model은 design current density인 <math><mi>i</mi><mo>=</mo><mn>2</mn><mtext> A </mtext><msup><mtext>cm</mtext><mrow><mo>-</mo><mn>2</mn></mrow></msup></math>에서의 효율을 모든 operating point에 적용한다.

<math display="block" aria-label="Fixed electrolyzer efficiency">
  <msub><mi>&eta;</mi><mtext>EL</mtext></msub>
  <mo>(</mo><mi>i</mi><mo>)</mo>
  <mo>=</mo>
  <msub><mi>&eta;</mi><mtext>design</mtext></msub>
  <mo>.</mo>
</math>

Variable-efficiency model은 steady-state I-V approximation을 사용한다.

<math display="block" aria-label="PEM electrolyzer cell voltage">
  <msub><mi>V</mi><mtext>cell</mtext></msub>
  <mo>=</mo>
  <msub><mi>E</mi><mtext>rev</mtext></msub>
  <mo>+</mo>
  <msub><mi>&eta;</mi><mtext>act</mtext></msub>
  <mo>+</mo>
  <msub><mi>&eta;</mi><mtext>ohm</mtext></msub>
  <mo>+</mo>
  <msub><mi>&eta;</mi><mtext>diff</mtext></msub>
  <mo>.</mo>
</math>

이 모델도 완전한 dynamic electrolyzer model은 아니다. Thermal dynamics, start-up and shut-down behavior, pressure dynamics, ramp-rate constraint, cycling-driven degradation은 들어가지 않는다. 개선은 더 좁다. 효율을 design point에 고정하지 않고 operating current에 따라 바뀌게 둔 것이다.

경제성 지표는 LCOH다. 논문은 25년 lifetime, 7% discount rate, 8000 h annual operating time을 가정한다. 이런 값은 absolute LCOH에 중요하지만, 논문의 핵심은 model fidelity와 time resolution이 만드는 상대적 bias다.

## Fixed efficiency가 bias를 만드는 이유

Fixed-efficiency model은 효율 곡선 전체를 한 점으로 대체하는 것에 가깝다. 누적 hydrogen-production error는 다음처럼 읽을 수 있다.

<math display="block" aria-label="Hydrogen production bias from fixed efficiency">
  <mi>&Delta;</mi><mi>H</mi>
  <mo>=</mo>
  <munder><mo>&sum;</mo><mi>t</mi></munder>
  <msub><mi>P</mi><mi>t</mi></msub>
  <mo>[</mo>
  <msub><mi>&eta;</mi><mtext>var</mtext></msub>
  <mo>(</mo><msub><mi>i</mi><mi>t</mi></msub><mo>)</mo>
  <mo>-</mo>
  <msub><mi>&eta;</mi><mtext>design</mtext></msub>
  <mo>]</mo>
  <mo>.</mo>
</math>

부호는 미리 정해져 있지 않다. 전해조가 variable-efficiency model에서 design efficiency보다 유리한 moderate part-load 구간에 오래 머물면 fixed model은 hydrogen production을 과소평가한다. 반대로 overload 구간에 오래 머물고 ohmic/diffusion loss가 커지면 fixed model은 efficiency penalty를 보지 못해 production을 과대평가할 수 있다.

이 논문의 중요한 nuance가 여기에 있다. 주장은 "variable efficiency가 항상 더 낙관적이다"가 아니다. Korean baseline case에서는 variable-efficiency model이 더 높은 hydrogen production과 낮은 LCOH를 준다. WT는 USD 6.02/kg에서 USD 5.73/kg으로, PV는 USD 4.12/kg에서 USD 4.01/kg으로, hybrid는 USD 4.57/kg에서 USD 4.35/kg으로 낮아진다. 하지만 overload가 커지면 high-current operation의 efficiency cost 때문에 variable model의 advantage가 줄어든다.

따라서 더 정확한 표현은 이렇다. Fixed-efficiency bias는 보편적인 오차 방향이 아니라 current-density distribution에 의해 결정된다.

## Temporal aggregation이 위험한 이유

Hourly data를 쓰면 hydrogen production은 다음처럼 계산된다.

<math display="block" aria-label="Hourly hydrogen production">
  <msub><mi>H</mi><mtext>hourly</mtext></msub>
  <mo>=</mo>
  <munder><mo>&sum;</mo><mi>t</mi></munder>
  <mi>f</mi>
  <mo>(</mo><msub><mi>P</mi><mi>t</mi></msub><mo>)</mo>
  <mo>.</mo>
</math>

같은 기간을 daily 또는 monthly average로 바꾸면 계산은 다음에 가까워진다.

<math display="block" aria-label="Aggregated hydrogen production">
  <msub><mi>H</mi><mtext>agg</mtext></msub>
  <mo>=</mo>
  <mo>|</mo><mi>T</mi><mo>|</mo>
  <mi>f</mi>
  <mo>(</mo>
  <mfrac>
    <mn>1</mn>
    <mrow><mo>|</mo><mi>T</mi><mo>|</mo></mrow>
  </mfrac>
  <munder><mo>&sum;</mo><mrow><mi>t</mi><mo>&#x2208;</mo><mi>T</mi></mrow></munder>
  <msub><mi>P</mi><mi>t</mi></msub>
  <mo>)</mo>
  <mo>.</mo>
</math>

이 둘이 같으려면 매우 제한적인 조건이 필요하다. <math><mi>f</mi></math>는 선형함수가 아니다. Renewable power conversion, current mapping, electrolyzer efficiency, capacity limit, overload rule, curtailment, zero-output period가 모두 들어간다. 따라서 <math><mi>f</mi><mo>(</mo><mi>E</mi><mo>[</mo><mi>P</mi><mo>]</mo><mo>)</mo></math>는 일반적으로 <math><mi>E</mi><mo>[</mo><mi>f</mi><mo>(</mo><mi>P</mi><mo>)</mo><mo>]</mo></math>와 같지 않다.

Korea hybrid case는 이 문제가 얼마나 큰지 보여준다.

| Temporal resolution | LCOH | Hydrogen production |
| --- | ---: | ---: |
| Hourly | USD 4.35/kg | 940 kg/h |
| Daily | USD 3.79/kg | 1066 kg/h |
| Monthly | USD 3.57/kg | 1125 kg/h |

Daily와 monthly aggregation은 시스템을 더 부드럽고 연속적으로 운전되는 것처럼 만든다. 이 경우 estimated hydrogen production은 각각 약 13%, 20% 높아진다.

다만 이것도 항상 같은 방향의 theorem은 아니다. 논문에서도 daily와 monthly의 관계가 단조롭지 않은 case가 나온다. 풍력 출력은 wind speed에 대해 강하게 비선형이고, wind speed를 평균낸 뒤 turbine power curve에 넣는 것은 power를 평균내는 것과 다르다. Temporal aggregation bias에는 renewable-generation nonlinearity와 electrolyzer-operation nonlinearity가 함께 섞여 있다. 이 두 효과를 명시적으로 분해했다면 논문의 주장은 더 강해졌을 것이다.

## Hybrid WT+PV와 variability

Hybrid result의 직관은 분명하다. Wind와 solar가 같은 시간에 peak를 찍지 않는다면, 결합된 renewable power의 normalized variability는 단일 자원보다 낮아질 수 있다.

<math display="block" aria-label="Hybrid renewable variance">
  <mi>Var</mi>
  <mo>(</mo><msub><mi>P</mi><mtext>WT</mtext></msub><mo>+</mo><msub><mi>P</mi><mtext>PV</mtext></msub><mo>)</mo>
  <mo>=</mo>
  <mi>Var</mi><mo>(</mo><msub><mi>P</mi><mtext>WT</mtext></msub><mo>)</mo>
  <mo>+</mo>
  <mi>Var</mi><mo>(</mo><msub><mi>P</mi><mtext>PV</mtext></msub><mo>)</mo>
  <mo>+</mo>
  <mn>2</mn><mi>Cov</mi><mo>(</mo><msub><mi>P</mi><mtext>WT</mtext></msub><mo>,</mo><msub><mi>P</mi><mtext>PV</mtext></msub><mo>)</mo>
  <mo>.</mo>
</math>

Multi-year result도 이 직관과 맞는다. Hybrid system은 WT-only나 PV-only보다 year-to-year LCOH variation이 작다. Hybrid의 LCOH standard deviation은 fixed model에서 약 USD 0.082/kg, variable model에서 약 USD 0.072/kg 수준이다.

하지만 이것도 보편 법칙은 아니다. Hybrid advantage는 local covariance structure에 의존한다. 특정 지역이나 계절에서 wind와 solar가 동시에 약하면 smoothing effect는 훨씬 약해질 수 있다.

## 믿을 수 있는 부분과 약한 부분

구조적으로 믿을 수 있는 결론은 세 가지다.

1. Fixed-efficiency model은 load-dependent electrolyzer curve의 point approximation이다.
2. 비선형 operating model에 대한 temporal aggregation은 일반적으로 bias를 만든다.
3. Wind와 solar profile이 보완적이면 WT+PV hybridization은 variability를 줄일 수 있다.

약한 부분은 operational realism이다. Variable PEMEL model은 steady-state다. Transient dynamics, cycling degradation, pressure dynamics, start-up and shut-down cost, thermal constraint, warranty-limited overload behavior가 없다. Overload rule도 실제 dispatch policy라기보다 sensitivity assumption에 가깝다.

Sizing structure도 한계다. 논문은 electrolyzer capacity를 100 MW로 고정하고 renewable capacity를 LCOH 관점에서 조정한다. Model fidelity와 resolution effect를 분리하기에는 좋은 설계지만, 실제 프로젝트에서는 electrolyzer, PV, wind, storage, grid interaction을 함께 size해야 한다. Storage, PPA, curtailment compensation, hydrogen storage, transport가 들어가면 hourly resolution의 가치는 system design과 더 강하게 결합된다.

Cross-country comparison도 조심해서 읽어야 한다. Korea, China, Australia, Germany의 representative site 하나가 국가 전체의 renewable potential을 대표하지는 않는다. Absolute ranking보다 중요한 것은 반복되는 패턴이다. Model fidelity와 temporal resolution은 early project-screening decision을 바꿀 만큼 LCOH를 움직일 수 있다.

## 비판적 총평

이 논문의 가장 강한 부분은 TEA input을 중립적인 bookkeeping으로 보지 않는다는 점이다. Electrolyzer efficiency fidelity와 renewable-data resolution은 modeling choice이고, 그 선택은 economic claim이 된다. Baseline scenario에서 variable-efficiency PEMEL modeling은 LCOH를 몇 % 낮춘다. Temporal-resolution comparison에서는 daily/monthly aggregation이 hydrogen output을 훨씬 크게 과대평가할 수 있다.

그렇다고 이 논문이 "hourly data와 variable-efficiency PEMEL model을 쓰면 항상 정확하다"를 증명하는 것은 아니다. 더 좁고 더 유용한 결론은 이것이다. Renewable intermittency와 nonlinear electrolyzer physics가 존재할 때, fixed efficiency와 low-resolution data는 구조적으로 bias를 만든다. 그 bias의 크기와 방향은 current-density distribution, renewable-resource distribution, capacity ratio, overload rule에 의해 결정된다.

Green-hydrogen screening에서는 이 정도로도 충분히 중요하다. Project economics가 marginal하다면 electrolyzer fidelity에서 오는 몇 % 차이와 temporal aggregation에서 오는 10-20% production shift는 세부사항이 아니다. 프로젝트가 viable해 보이는지 자체를 바꿀 수 있다.

## References

- Kang, B., Kim, H., & Park, J. (2026). Impact of electrolyzer-model fidelity and renewable-data resolution on techno-economic assessments of green hydrogen systems. *Energy Conversion and Management*, 364, 121676.
