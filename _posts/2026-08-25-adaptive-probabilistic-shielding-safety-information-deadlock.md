---
layout: post
title: "The Safety–Information Deadlock in Adaptive Probabilistic Shielding"
title_ko: "적응형 확률적 실딩의 안전–정보 교착: 안전을 배우려면 언제 위험을 감수해야 하는가"
date: 2026-08-25
category: safe-constrained-rl
category_label: "Safe & Constrained RL"
research_group: algorithmic_reviews
research_category: safe-constrained-rl
research_category_label: "Safe & Constrained RL"
application_category: ""
application_category_label: ""
method_category: "safe-constrained-rl"
method_category_label: "Safe & Constrained RL"
paper_title: ""
authors: ""
venue: ""
year: ""
doi: ""
arxiv: ""
source_url: ""
tags:
  - "safe-rl"
  - "probabilistic-shielding"
  - "interval-mdp"
  - "model-uncertainty"
  - "safe-exploration"
excerpt: "How online MDP estimation, interval uncertainty, and probabilistic shielding form a coupled loop in which blocking risky actions can also block the evidence needed to learn safety."
excerpt_ko: "온라인 MDP 추정, 구간 불확실성, 확률적 실딩이 결합될 때 위험한 행동의 차단이 안전을 학습하는 데 필요한 증거까지 막는 교착을 분석한다."
language: "en-ko"
has_korean_note: false
---

## The trap: safety needs data, but data collection can be unsafe

Imagine an aircraft-avoidance agent that knows every physically possible next state but does not know how likely each transition is. A maneuver may lead to clear air, a near miss, or a collision state. The topology is known; the probabilities are not.

Three apparently reasonable responses all fail in a different way.

First, the agent can explore freely until it has enough data to estimate the transition model, then construct a safety shield. The final policy may be protected, but the data-collection phase—the period in which the model is least reliable—has no protection.

Second, the agent can build a conservative shield immediately. Yet an action with little data receives a wide uncertainty interval and looks dangerous under a worst-case calculation. The shield blocks it, the agent never collects evidence about it, and the interval never contracts. A genuinely safe route can remain permanently classified as unsafe.

Third, the agent can use a short look-ahead horizon to make shielding computationally manageable. That works until risk is delayed. If a choice made now causes a failure one hundred steps later, a shield looking only six or fifty steps ahead sees no danger at all.

These are not isolated implementation bugs. They expose the central conflict in online safe reinforcement learning:

**Safety assessment requires transition data, while acquiring transition data may require risky exploration.**

The study considered here addresses this conflict by repeatedly learning an MDP or interval MDP from new transitions, recomputing a probabilistic shield, and continuing Q-learning under the updated shield. Its main contribution is the online adaptive closed loop. It does not introduce a new RL algorithm, a new interval estimator, or a new shield-synthesis theory. The interesting question is what happens when existing components are coupled and each one changes the data seen by the others.

## What is known, and what remains unknown?

Let the environment be an MDP

<math display="block" aria-label="Unknown Markov decision process">
  <mi>M</mi><mo>=</mo><mo>(</mo><mi>S</mi><mo>,</mo><mi>A</mi><mo>,</mo><msub><mi>s</mi><mn>0</mn></msub><mo>,</mo><mi>T</mi><mo>)</mo><mo>,</mo>
</math>

where the transition probabilities <math><mi>T</mi><mo>(</mo><mi>s</mi><mo>,</mo><mi>a</mi><mo>,</mo><msup><mi>s</mi><mo>&prime;</mo></msup><mo>)</mo></math> are unknown. The agent is nevertheless assumed to know the transition support

<math display="block" aria-label="Known transition support">
  <msub><mi>T</mi><mi>U</mi></msub><mo>(</mo><mi>s</mi><mo>,</mo><mi>a</mi><mo>)</mo>
  <mo>=</mo><mo>{</mo><msup><mi>s</mi><mo>&prime;</mo></msup><mo>:</mo>
  <mi>T</mi><mo>(</mo><mi>s</mi><mo>,</mo><mi>a</mi><mo>,</mo><msup><mi>s</mi><mo>&prime;</mo></msup><mo>)</mo><mo>&gt;</mo><mn>0</mn><mo>}</mo><mo>.</mo>
</math>

Thus the agent may know that an action can lead to states <math><msub><mi>s</mi><mn>2</mn></msub></math>, <math><msub><mi>s</mi><mn>3</mn></msub></math>, and <math><msub><mi>s</mi><mn>4</mn></msub></math>, while not knowing whether their probabilities are <math><mo>(</mo><mn>0.7</mn><mo>,</mo><mn>0.2</mn><mo>,</mo><mn>0.1</mn><mo>)</mo></math> or <math><mo>(</mo><mn>0.4</mn><mo>,</mo><mn>0.4</mn><mo>,</mo><mn>0.2</mn><mo>)</mo></math>. Discovering previously unknown successor states is outside the problem formulation.

This assumption makes the problem tractable, but it is strong. A rare accident transition omitted from the known support is treated as impossible. No confidence interval over the listed transitions can repair a missing edge.

## Finite-horizon probabilistic shielding

Let <math><mi>&phi;</mi><mo>&sube;</mo><mi>S</mi></math> be the set of safe states. Rather than requiring safety forever, the shield evaluates the probability of remaining in <math><mi>&phi;</mi></math> for the next <math><mi>h</mi></math> steps. The best achievable safety probability from state <math><mi>s</mi></math> is

<math display="block" aria-label="Maximum finite horizon safety probability">
  <msubsup><mi>P</mi><mrow><mi>M</mi><mo>,</mo><mi>&phi;</mi><mo>|</mo><mi>h</mi></mrow><mi>max</mi></msubsup><mo>(</mo><mi>s</mi><mo>)</mo>
  <mo>=</mo><munder><mo>max</mo><mi>&pi;</mi></munder>
  <msubsup><mi>P</mi><mi>M</mi><mi>&pi;</mi></msubsup>
  <mo>(</mo><msub><mi>s</mi><mn>0</mn></msub><mo>,</mo><mo>&hellip;</mo><mo>,</mo><msub><mi>s</mi><mi>h</mi></msub><mo>&isin;</mo><mi>&phi;</mi>
  <mo>|</mo><msub><mi>s</mi><mn>0</mn></msub><mo>=</mo><mi>s</mi><mo>)</mo><mo>.</mo>
</math>

If action <math><mi>a</mi></math> must be taken first, the recursion is

<math display="block" aria-label="Action-conditioned safety recursion">
  <msubsup><mi>P</mi><mrow><mi>M</mi><mo>,</mo><mi>&phi;</mi><mo>|</mo><mi>h</mi></mrow><mi>max</mi></msubsup><mo>(</mo><mi>s</mi><mo>,</mo><mi>a</mi><mo>)</mo>
  <mo>=</mo><munder><mo>&sum;</mo><msup><mi>s</mi><mo>&prime;</mo></msup></munder>
  <mi>T</mi><mo>(</mo><mi>s</mi><mo>,</mo><mi>a</mi><mo>,</mo><msup><mi>s</mi><mo>&prime;</mo></msup><mo>)</mo>
  <msubsup><mi>P</mi><mrow><mi>M</mi><mo>,</mo><mi>&phi;</mi><mo>|</mo><mi>h</mi><mo>-</mo><mn>1</mn></mrow><mi>max</mi></msubsup><mo>(</mo><msup><mi>s</mi><mo>&prime;</mo></msup><mo>)</mo><mo>.</mo>
</math>

With a risk tolerance <math><mi>&theta;</mi></math>, the primary shield admits

<math display="block" aria-label="Risk threshold shield">
  <msub><mi>&nabla;</mi><mi>&theta;</mi></msub><mo>(</mo><mi>s</mi><mo>)</mo>
  <mo>=</mo><mo>{</mo><mi>a</mi><mo>:</mo>
  <msubsup><mi>P</mi><mrow><mi>M</mi><mo>,</mo><mi>&phi;</mi><mo>|</mo><mi>h</mi></mrow><mi>max</mi></msubsup><mo>(</mo><mi>s</mi><mo>,</mo><mi>a</mi><mo>)</mo>
  <mo>&ge;</mo><mn>1</mn><mo>-</mo><mi>&theta;</mi><mo>}</mo><mo>.</mo>
</math>

The reported default <math><mi>&theta;</mi><mo>=</mo><mn>0.05</mn></math> therefore asks for at least 95% safety over the chosen horizon. But this admissible set can be empty. The implementation then uses a fallback set containing actions whose safety value is within <math><mi>&kappa;</mi></math> of the best available action. If the best action has only 70% predicted safety, a fallback with <math><mi>&kappa;</mi><mo>=</mo><mn>0.01</mn></math> may admit actions at or above 69%.

That detail changes the interpretation. The shield does not always guarantee 95% finite-horizon safety. When the threshold set is empty, it selects actions close to the least unsafe option currently available.

## Why an interval MDP changes the decision

A point estimate might state that a collision transition has probability 0.10. An interval MDP instead records

<math display="block" aria-label="Interval transition probability">
  <mi>T</mi><mo>(</mo><mi>s</mi><mo>,</mo><mi>a</mi><mo>,</mo><msup><mi>s</mi><mo>&prime;</mo></msup><mo>)</mo>
  <mo>&isin;</mo><mo>[</mo><mn>0.06</mn><mo>,</mo><mn>0.15</mn><mo>]</mo><mo>.</mo>
</math>

A robust shield evaluates the MDP inside those intervals that gives the worst safety value. An optimistic shield evaluates the best one. If the probability of falling into a hole is estimated as <math><mo>[</mo><mn>0.02</mn><mo>,</mo><mn>0.20</mn><mo>]</mo></math>, the robust interpretation acts as if it might be 20%; the optimistic interpretation acts as if it might be 2%. As observations accumulate and the interval contracts toward, say, <math><mo>[</mo><mn>0.075</mn><mo>,</mo><mn>0.085</mn><mo>]</mo></math>, the two decisions should become closer.

The study compares three estimators:

| Estimator | Model output | Explicit uncertainty | Finite-data coverage claim |
|---|---|---:|---:|
| MAP | Point MDP | No | No |
| PAC | Interval MDP | Yes | Yes, subject to its stated assumptions |
| LUI | Interval MDP | Yes | No |

MAP uses a symmetric prior and smoothed transition counts. It avoids assigning exact zero probability from sparse data, but it provides no direct measure of confidence.

The PAC estimator places concentration-based intervals around the estimated transitions. More samples narrow the intervals, and the intended coverage level controls the probability that the true model lies outside them. One technical point deserves verification: the supplied account reports that the displayed Hoeffding half-width in the paper appears without the square root found in the standard form. If that reflects the printed equation rather than a transcription issue, the finite-data derivation and the implementation need to be checked separately.

Linearly Updating Intervals (LUI) blend prior interval information with empirical frequencies. The prior dominates early; observations dominate as counts grow. LUI is less conservative in the experiments and is used as a default, but it is not a finite-sample confidence set.

## One loop learns both policy and safety model

The architecture repeatedly executes the following sequence:

1. Collect transition counts from interaction.
2. Update a point MDP or interval MDP.
3. Recompute the probabilistic shield by model checking.
4. Continue Q-learning with the newly admissible action sets.

Both the policy and the safety filter therefore move over time. This is the central architectural contribution. A shield is not a passive guard placed after a fixed policy. It changes which actions generate data, which changes the estimated model, which changes the next shield.

The most revealing design choice appears in exploration. With probability <math><mi>&epsilon;</mi></math>, the algorithm samples uniformly from the full action space <math><mi>A</mi></math>, not only from the currently shielded set <math><mi>&nabla;</mi><mo>(</mo><mi>s</mi><mo>)</mo></math>. The shield is deliberately bypassed during those exploration steps.

Why accept this? If early robust intervals are wide, strict shield-only exploration creates a self-reinforcing loop:

<math display="block" aria-label="Uncertainty blocking feedback loop">
  <mtext>wide uncertainty</mtext><mo>&rarr;</mo><mtext>action blocked</mtext><mo>&rarr;</mo>
  <mtext>no data</mtext><mo>&rarr;</mo><mtext>wide uncertainty</mtext><mo>.</mo>
</math>

Bypassing the shield with a small probability can break the deadlock. It also means that this should not be described as formal zero-violation training. The stated objective is a low number of safety violations during learning, not their complete elimination.

## What the experiments reveal

The evaluation uses five finite discrete environments: Aircraft, Antlion, Sinkholes, Crossroads, and Gravity. They range from 202 to 2,000 states and cover collisions, predator or hole avoidance, delayed risk, and gravity-well hazards. Each configuration is reported over 100 runs. The default settings include Q-learning with <math><mi>&alpha;</mi><mo>=</mo><mn>0.1</mn></math>, <math><mi>&gamma;</mi><mo>=</mo><mn>0.9</mn></math>, and <math><mi>&epsilon;</mi><mo>=</mo><mn>0.05</mn></math>, and shielding with <math><mi>&theta;</mi><mo>=</mo><mn>0.05</mn></math>, <math><mi>&kappa;</mi><mo>=</mo><mn>0.01</mn></math>, and <math><mi>h</mi><mo>=</mo><mn>100</mn></math>.

### Safety improves, but reward can collapse

In Gravity, unshielded Q-learning obtains reward 30.35 but an unsafe probability of 99.2%. Robust LUI reduces the unsafe probability to 3.9%, while reward falls to 8.27. Robust PAC reaches 0.0% unsafe in the reported trials, but its reward is -2.56. The result is clear: the shield can change the safety profile dramatically, but safety is not free.

### Robustness can lock onto the wrong route

Robust shielding is not uniformly safer in every benchmark. In Aircraft, Robust LUI reports 8.3% unsafe, compared with 4.0% for MAP and 4.1% for an oracle shield. A plausible mechanism is sampling bias. An initially visited route gets narrower intervals and therefore looks safer under worst-case evaluation. A less visited route may be truly safer but remains blocked because its interval is wide. Conservatism can preserve an early mistake.

### Shield bypass buys information with risk

In Gravity, exploration over the full action space yields reward 8.27 and 3.9% unsafe, whereas exploration restricted to the shield yields reward 1.58 and 0.6% unsafe. The latter is safer but discovers less. This is the empirical form of the safety-information trade-off, not a minor tuning effect.

### A shield cannot see beyond its horizon

Crossroads contains danger that accumulates roughly one hundred steps after the relevant choice. Horizons of 6, 25, 50, and 75 all produce reward 9.57 and 40.1% unsafe. At horizons 100 and 200, unsafe falls to 0.0% while reward falls to 5.12. The horizon is therefore part of the safety specification. If it is shorter than the hazard delay, the shield can classify a dangerous action as locally harmless.

## What is and is not guaranteed

The individual estimators are asymptotically consistent when every relevant state-action transition is observed sufficiently often. If an interval MDP contains the true MDP, its robust safety value is conservative within the modeled finite horizon. These facts support the intuition that the adaptive shield can approach an oracle shield as uncertainty vanishes.

They do not prove convergence of the entire closed loop. The shield changes the visitation distribution required for estimator convergence. The study does not establish that the shield converges to the oracle shield, that the policy converges to a constrained optimum, or that training avoids all violations.

Nor does a local condition such as “95% safe for the next <math><mi>h</mi></math> steps” imply “95% safe over the entire lifetime.” Risk can accumulate across repeated horizons, and the fallback shield may discard the 95% threshold altogether.

The PAC interpretation also needs care across repeated adaptive updates. A coverage statement for one estimate does not automatically become a simultaneous guarantee for every estimate in a sequence. An anytime claim would require a confidence budget across updates or a confidence-sequence argument. The lower clipping value <math><mi>&xi;</mi><mo>=</mo><msup><mn>10</mn><mrow><mo>-</mo><mn>8</mn></mrow></msup></math> similarly implies a lower-bound assumption for every nonzero transition if strict model containment is claimed.

Finally, the experiments use finite tabular MDPs, stationary Markov dynamics, known unsafe states, and known transition support. Continuous physical systems need an abstraction; nonstationary dynamics need forgetting or change detection; unknown hazards need support discovery or a different uncertainty model. None of these extensions follows automatically from the reported framework.

## The real contribution: a coupled data-generating system

The most useful result is not a new Q-learning update or a new model-checking operator. It is the recognition that an online shield participates in the data-generating process:

<math display="block" aria-label="Adaptive shielding coupled system">
  <mtext>safety filter</mtext><mo>&rarr;</mo><mtext>exploration distribution</mtext><mo>&rarr;</mo>
  <mtext>model uncertainty</mtext><mo>&rarr;</mo><mtext>safety filter</mtext><mo>.</mo>
</math>

This coupling creates two opposing errors. An optimistic shield may gather informative data by accepting excessive risk. A robust shield may suppress risk while preventing the evidence needed to discover a better safe policy. The framework makes that tension observable and tunable, but it does not solve it once and for all.

That is the right way to position the study: an integration of probabilistic shielding, online MDP/iMDP estimation, model checking, and Q-learning that exposes a neglected feedback problem in safe exploration. Its strongest lesson is also its most uncomfortable one. Sometimes the only way to learn that an action is safe is to try it before safety is known.

<!-- ko -->

## 함정: 안전을 판단하려면 데이터가 필요하지만, 데이터 수집은 위험할 수 있다

어떤 항공기 회피 에이전트가 물리적으로 가능한 모든 다음 상태는 알지만 각 전이의 확률은 모른다고 하자. 한 기동은 안전한 공역, 근접 조우, 충돌 상태로 이어질 수 있다. 전이 구조는 알지만 확률은 모른다.

얼핏 합리적으로 보이는 세 가지 대응은 서로 다른 방식으로 실패한다.

첫째, 충분한 데이터를 자유롭게 수집해 전이 모델을 추정한 뒤 safety shield를 만들 수 있다. 최종 정책은 보호받을 수 있지만, 모델이 가장 부정확한 데이터 수집 기간은 아무 보호도 받지 못한다.

둘째, 처음부터 보수적인 shield를 만들 수 있다. 그러나 데이터가 적은 action은 불확실성 구간이 넓고 최악의 경우 계산에서 위험해 보인다. Shield가 그 action을 막으면 에이전트는 실제 데이터를 얻지 못하고 구간도 줄어들지 않는다. 실제로 안전한 경로가 영원히 위험한 경로로 분류될 수 있다.

셋째, 계산량을 줄이기 위해 짧은 look-ahead horizon을 사용할 수 있다. 위험이 지연되기 전까지는 잘 작동한다. 지금의 선택이 100 step 뒤의 실패를 만든다면 6 step이나 50 step만 보는 shield는 아무 위험도 발견하지 못한다.

이들은 단순한 구현 오류가 아니다. Online safe reinforcement learning의 중심 모순을 드러낸다.

**안전을 판단하려면 transition data가 필요하지만, transition data를 얻으려면 위험한 exploration이 필요할 수 있다.**

여기서 다루는 연구는 새로운 transition을 얻을 때마다 MDP 또는 interval MDP를 학습하고, probabilistic shield를 다시 계산하고, 갱신된 shield 아래에서 Q-learning을 계속하는 방식으로 이 모순을 다룬다. 주된 기여는 online adaptive closed loop다. 새로운 RL 알고리즘, 새로운 interval estimator, 새로운 shield synthesis 이론을 제안한 연구는 아니다. 흥미로운 질문은 기존 구성요소들을 결합했을 때 각 요소가 다른 요소가 보게 되는 데이터를 어떻게 바꾸는가에 있다.

## 무엇을 알고 있고, 무엇을 모르는가?

환경을 다음 MDP로 두자.

<math display="block" aria-label="미지의 마르코프 결정 과정">
  <mi>M</mi><mo>=</mo><mo>(</mo><mi>S</mi><mo>,</mo><mi>A</mi><mo>,</mo><msub><mi>s</mi><mn>0</mn></msub><mo>,</mo><mi>T</mi><mo>)</mo><mo>.</mo>
</math>

Transition probability <math><mi>T</mi><mo>(</mo><mi>s</mi><mo>,</mo><mi>a</mi><mo>,</mo><msup><mi>s</mi><mo>&prime;</mo></msup><mo>)</mo></math>는 알 수 없다. 다만 agent는 transition support를 알고 있다고 가정한다.

<math display="block" aria-label="알려진 전이 support">
  <msub><mi>T</mi><mi>U</mi></msub><mo>(</mo><mi>s</mi><mo>,</mo><mi>a</mi><mo>)</mo>
  <mo>=</mo><mo>{</mo><msup><mi>s</mi><mo>&prime;</mo></msup><mo>:</mo>
  <mi>T</mi><mo>(</mo><mi>s</mi><mo>,</mo><mi>a</mi><mo>,</mo><msup><mi>s</mi><mo>&prime;</mo></msup><mo>)</mo><mo>&gt;</mo><mn>0</mn><mo>}</mo><mo>.</mo>
</math>

즉 하나의 action이 <math><msub><mi>s</mi><mn>2</mn></msub></math>, <math><msub><mi>s</mi><mn>3</mn></msub></math>, <math><msub><mi>s</mi><mn>4</mn></msub></math>로 이어질 수 있다는 사실은 알지만, 그 확률이 <math><mo>(</mo><mn>0.7</mn><mo>,</mo><mn>0.2</mn><mo>,</mo><mn>0.1</mn><mo>)</mo></math>인지 <math><mo>(</mo><mn>0.4</mn><mo>,</mo><mn>0.4</mn><mo>,</mo><mn>0.2</mn><mo>)</mo></math>인지는 모를 수 있다. 이전에 몰랐던 successor state를 새로 발견하는 문제는 범위 밖이다.

이 가정은 문제를 다룰 수 있게 만들지만 상당히 강하다. 알려진 support에서 빠진 희귀 사고 transition은 불가능한 사건으로 처리된다. 등록된 transition들의 confidence interval을 아무리 정교하게 만들어도 누락된 edge는 복구할 수 없다.

## Finite-horizon probabilistic shielding

<math><mi>&phi;</mi><mo>&sube;</mo><mi>S</mi></math>를 안전한 state의 집합이라고 하자. Shield는 영원한 안전을 요구하는 대신 앞으로 <math><mi>h</mi></math> step 동안 <math><mi>&phi;</mi></math> 안에 머물 확률을 계산한다. State <math><mi>s</mi></math>에서 달성할 수 있는 최대 안전 확률은 다음과 같다.

<math display="block" aria-label="유한 horizon 최대 안전 확률">
  <msubsup><mi>P</mi><mrow><mi>M</mi><mo>,</mo><mi>&phi;</mi><mo>|</mo><mi>h</mi></mrow><mi>max</mi></msubsup><mo>(</mo><mi>s</mi><mo>)</mo>
  <mo>=</mo><munder><mo>max</mo><mi>&pi;</mi></munder>
  <msubsup><mi>P</mi><mi>M</mi><mi>&pi;</mi></msubsup>
  <mo>(</mo><msub><mi>s</mi><mn>0</mn></msub><mo>,</mo><mo>&hellip;</mo><mo>,</mo><msub><mi>s</mi><mi>h</mi></msub><mo>&isin;</mo><mi>&phi;</mi>
  <mo>|</mo><msub><mi>s</mi><mn>0</mn></msub><mo>=</mo><mi>s</mi><mo>)</mo><mo>.</mo>
</math>

먼저 action <math><mi>a</mi></math>를 실행해야 한다면 recursion은 다음과 같다.

<math display="block" aria-label="Action 조건부 안전 재귀식">
  <msubsup><mi>P</mi><mrow><mi>M</mi><mo>,</mo><mi>&phi;</mi><mo>|</mo><mi>h</mi></mrow><mi>max</mi></msubsup><mo>(</mo><mi>s</mi><mo>,</mo><mi>a</mi><mo>)</mo>
  <mo>=</mo><munder><mo>&sum;</mo><msup><mi>s</mi><mo>&prime;</mo></msup></munder>
  <mi>T</mi><mo>(</mo><mi>s</mi><mo>,</mo><mi>a</mi><mo>,</mo><msup><mi>s</mi><mo>&prime;</mo></msup><mo>)</mo>
  <msubsup><mi>P</mi><mrow><mi>M</mi><mo>,</mo><mi>&phi;</mi><mo>|</mo><mi>h</mi><mo>-</mo><mn>1</mn></mrow><mi>max</mi></msubsup><mo>(</mo><msup><mi>s</mi><mo>&prime;</mo></msup><mo>)</mo><mo>.</mo>
</math>

Risk tolerance <math><mi>&theta;</mi></math>가 주어지면 기본 shield는 다음 action을 허용한다.

<math display="block" aria-label="위험 임계값 shield">
  <msub><mi>&nabla;</mi><mi>&theta;</mi></msub><mo>(</mo><mi>s</mi><mo>)</mo>
  <mo>=</mo><mo>{</mo><mi>a</mi><mo>:</mo>
  <msubsup><mi>P</mi><mrow><mi>M</mi><mo>,</mo><mi>&phi;</mi><mo>|</mo><mi>h</mi></mrow><mi>max</mi></msubsup><mo>(</mo><mi>s</mi><mo>,</mo><mi>a</mi><mo>)</mo>
  <mo>&ge;</mo><mn>1</mn><mo>-</mo><mi>&theta;</mi><mo>}</mo><mo>.</mo>
</math>

보고된 기본값 <math><mi>&theta;</mi><mo>=</mo><mn>0.05</mn></math>는 선택한 horizon 동안 적어도 95%의 안전 확률을 요구한다. 그러나 admissible set이 비어 있을 수 있다. 구현은 이때 최선 action의 안전 값에서 <math><mi>&kappa;</mi></math> 이내에 있는 action들을 담은 fallback set을 사용한다. 최선 action의 예측 안전 확률이 70%에 불과하다면 <math><mi>&kappa;</mi><mo>=</mo><mn>0.01</mn></math>인 fallback은 69% 이상의 action을 허용할 수 있다.

이 세부사항은 해석을 바꾼다. 이 shield는 항상 95%의 finite-horizon safety를 보장하지 않는다. Threshold set이 비어 있으면 현재 선택 가능한 것 가운데 가장 덜 위험한 action과 가까운 것들을 고른다.

## Interval MDP가 판단을 바꾸는 이유

Point estimate는 collision transition의 확률이 0.10이라고 말할 수 있다. Interval MDP는 대신 다음과 같이 기록한다.

<math display="block" aria-label="구간 전이 확률">
  <mi>T</mi><mo>(</mo><mi>s</mi><mo>,</mo><mi>a</mi><mo>,</mo><msup><mi>s</mi><mo>&prime;</mo></msup><mo>)</mo>
  <mo>&isin;</mo><mo>[</mo><mn>0.06</mn><mo>,</mo><mn>0.15</mn><mo>]</mo><mo>.</mo>
</math>

Robust shield는 이 구간 안의 MDP 중 안전 값이 가장 나쁜 모델을 평가한다. Optimistic shield는 가장 좋은 모델을 평가한다. 구덩이에 빠질 확률이 <math><mo>[</mo><mn>0.02</mn><mo>,</mo><mn>0.20</mn><mo>]</mo></math>으로 추정됐다면 robust 해석은 20%일 수 있다고 판단하고, optimistic 해석은 2%일 수 있다고 판단한다. 관측이 쌓여 구간이 <math><mo>[</mo><mn>0.075</mn><mo>,</mo><mn>0.085</mn><mo>]</mo></math>처럼 줄어들면 두 판단도 가까워져야 한다.

연구는 세 가지 estimator를 비교한다.

| Estimator | Model output | 불확실성 명시 | Finite-data coverage 주장 |
|---|---|---:|---:|
| MAP | Point MDP | 아니요 | 아니요 |
| PAC | Interval MDP | 예 | 가정이 맞을 때 예 |
| LUI | Interval MDP | 예 | 아니요 |

MAP은 symmetric prior와 smoothed transition count를 사용한다. 적은 데이터 때문에 확률을 정확히 0으로 만드는 것은 피하지만, confidence를 직접 표현하지 않는다.

PAC estimator는 transition estimate 주변에 concentration-based interval을 둔다. 표본이 많아질수록 구간이 좁아지고, 설정한 coverage level은 true model이 구간 밖에 있을 확률을 통제하려 한다. 한 가지 기술적 사항은 확인이 필요하다. 제공된 정리에 따르면 논문의 Hoeffding half-width 표기에는 통상적인 식에 있는 square root가 보이지 않는다. 이것이 단순한 전사 문제가 아니라 실제 인쇄된 식이라면 finite-data derivation과 구현을 각각 확인해야 한다.

Linearly Updating Intervals(LUI)는 prior interval 정보와 empirical frequency를 결합한다. 초기에는 prior가 지배하고 count가 커지면 관측이 지배한다. 실험에서 LUI는 덜 보수적이며 기본 estimator로 사용되지만 finite-sample confidence set은 아니다.

## 하나의 loop에서 policy와 safety model을 함께 학습한다

전체 architecture는 다음 순서를 반복한다.

1. 환경과 상호작용해 transition count를 수집한다.
2. Point MDP 또는 interval MDP를 갱신한다.
3. Model checking으로 probabilistic shield를 다시 계산한다.
4. 새 admissible action set 아래에서 Q-learning을 계속한다.

Policy와 safety filter가 모두 시간에 따라 바뀐다. 이것이 핵심 architecture contribution이다. Shield는 고정된 policy 뒤에 놓인 수동적인 guard가 아니다. Shield는 어떤 action이 데이터를 생성하는지를 바꾸고, 이는 estimate model을 바꾸며, 다시 다음 shield를 바꾼다.

가장 드러나는 설계 선택은 exploration에서 나온다. 확률 <math><mi>&epsilon;</mi></math>로 알고리즘은 현재 shield set <math><mi>&nabla;</mi><mo>(</mo><mi>s</mi><mo>)</mo></math>가 아니라 전체 action space <math><mi>A</mi></math>에서 균등하게 action을 뽑는다. 해당 exploration step에서는 shield를 의도적으로 우회한다.

왜 이런 위험을 받아들이는가? 초기 robust interval이 넓을 때 shield 안에서만 탐색하면 다음 self-reinforcing loop가 생기기 때문이다.

<math display="block" aria-label="불확실성 차단 피드백 루프">
  <mtext>넓은 불확실성</mtext><mo>&rarr;</mo><mtext>action 차단</mtext><mo>&rarr;</mo>
  <mtext>데이터 없음</mtext><mo>&rarr;</mo><mtext>넓은 불확실성</mtext><mo>.</mo>
</math>

작은 확률로 shield를 우회하면 deadlock을 깨뜨릴 수 있다. 동시에 이 방법을 formal zero-violation training이라고 부를 수 없게 된다. 목표는 학습 중 safety violation을 완전히 제거하는 것이 아니라 그 수를 낮게 유지하는 것이다.

## 실험이 보여주는 것

평가는 Aircraft, Antlion, Sinkholes, Crossroads, Gravity의 유한 discrete environment 다섯 개를 사용한다. 202개에서 2,000개의 state를 가지며 collision, predator 또는 hole 회피, delayed risk, gravity-well hazard를 포함한다. 각 configuration은 100회 실행 결과로 보고된다. 기본 설정은 Q-learning에서 <math><mi>&alpha;</mi><mo>=</mo><mn>0.1</mn></math>, <math><mi>&gamma;</mi><mo>=</mo><mn>0.9</mn></math>, <math><mi>&epsilon;</mi><mo>=</mo><mn>0.05</mn></math>이며, shield는 <math><mi>&theta;</mi><mo>=</mo><mn>0.05</mn></math>, <math><mi>&kappa;</mi><mo>=</mo><mn>0.01</mn></math>, <math><mi>h</mi><mo>=</mo><mn>100</mn></math>을 사용한다.

### 안전은 좋아지지만 reward가 무너질 수 있다

Gravity에서 unshielded Q-learning은 reward 30.35를 얻지만 unsafe probability는 99.2%다. Robust LUI는 unsafe probability를 3.9%로 낮추는 대신 reward가 8.27로 떨어진다. Robust PAC는 보고된 trial에서 0.0% unsafe에 도달하지만 reward는 -2.56이다. Shield가 safety profile을 크게 바꿀 수 있지만 안전은 공짜가 아니다.

### Robustness가 잘못된 경로를 고착시킬 수 있다

Robust shielding이 모든 benchmark에서 항상 더 안전하지는 않다. Aircraft에서 Robust LUI는 8.3% unsafe를 보인 반면 MAP은 4.0%, oracle shield는 4.1%다. 가능한 메커니즘은 sampling bias다. 초기에 방문한 경로는 interval이 좁아져 worst-case 평가에서 더 안전해 보인다. 방문이 적은 경로는 실제로 더 안전해도 interval이 넓어 차단된다. 보수성이 초기의 실수를 보존할 수 있다.

### Shield 우회는 위험과 정보를 교환한다

Gravity에서 전체 action space를 탐색하면 reward 8.27과 3.9% unsafe를 얻지만, shield 안에서만 탐색하면 reward 1.58과 0.6% unsafe를 얻는다. 후자가 더 안전하지만 덜 발견한다. 이는 단순한 tuning 문제가 아니라 safety-information trade-off의 실험적 형태다.

### Shield는 horizon 바깥을 볼 수 없다

Crossroads의 위험은 관련 선택 이후 약 100 step에 걸쳐 누적된다. Horizon 6, 25, 50, 75는 모두 reward 9.57과 40.1% unsafe를 보인다. Horizon 100과 200에서 unsafe는 0.0%로 내려가고 reward는 5.12로 낮아진다. 따라서 horizon은 safety specification의 일부다. Hazard delay보다 짧으면 shield는 위험한 action을 국소적으로 안전하다고 분류할 수 있다.

## 무엇이 보장되고 무엇이 보장되지 않는가

각 estimator는 관련 state-action transition을 충분히 자주 관측하면 asymptotically consistent하다. Interval MDP가 true MDP를 포함할 때 robust safety value는 모델링된 finite horizon 안에서 conservative하다. 이는 불확실성이 사라질수록 adaptive shield가 oracle shield에 가까워질 수 있다는 직관을 뒷받침한다.

그러나 전체 closed loop의 convergence를 증명하지는 않는다. Shield 자체가 estimator convergence에 필요한 visitation distribution을 바꾸기 때문이다. 이 연구는 shield가 oracle shield로 수렴하거나, policy가 constrained optimum으로 수렴하거나, training 중 모든 violation을 피한다는 것을 보이지 않는다.

또한 “앞으로 <math><mi>h</mi></math> step 동안 95% 안전”이라는 국소 조건은 “전체 lifetime 동안 95% 안전”을 의미하지 않는다. 반복되는 horizon 사이에서 risk가 누적될 수 있고, fallback shield는 95% threshold 자체를 버릴 수 있다.

반복되는 adaptive update에 PAC 해석을 적용할 때도 주의해야 한다. 한 번의 estimate에 대한 coverage statement가 sequence 전체의 simultaneous guarantee로 자동 변환되지는 않는다. Anytime claim을 하려면 update 사이에 confidence budget을 배분하거나 confidence sequence 논증이 필요하다. Lower clipping 값 <math><mi>&xi;</mi><mo>=</mo><msup><mn>10</mn><mrow><mo>-</mo><mn>8</mn></mrow></msup></math>도 strict model containment를 주장하려면 모든 nonzero transition에 대한 lower-bound assumption을 사실상 요구한다.

마지막으로 실험은 finite tabular MDP, stationary Markov dynamics, 알려진 unsafe state, 알려진 transition support를 사용한다. Continuous physical system에는 abstraction이 필요하고, nonstationary dynamics에는 forgetting 또는 change detection이 필요하며, 알려지지 않은 hazard에는 support discovery나 다른 uncertainty model이 필요하다. 이러한 확장은 보고된 framework에서 자동으로 따라오지 않는다.

## 실제 기여: 결합된 data-generating system

가장 유용한 결과는 새로운 Q-learning update나 새로운 model-checking operator가 아니다. Online shield가 data-generating process에 참여한다는 사실이다.

<math display="block" aria-label="Adaptive shielding 결합 시스템">
  <mtext>safety filter</mtext><mo>&rarr;</mo><mtext>exploration distribution</mtext><mo>&rarr;</mo>
  <mtext>model uncertainty</mtext><mo>&rarr;</mo><mtext>safety filter</mtext><mo>.</mo>
</math>

이 coupling은 반대 방향의 두 오류를 만든다. Optimistic shield는 과도한 위험을 받아들이며 유용한 데이터를 모을 수 있다. Robust shield는 위험을 억제하면서 더 나은 safe policy를 발견하는 데 필요한 evidence까지 막을 수 있다. 이 framework는 그 긴장을 관찰하고 조정할 수 있게 하지만, 이를 완전히 해결하지는 않는다.

따라서 이 연구는 probabilistic shielding, online MDP/iMDP estimation, model checking, Q-learning을 통합해 safe exploration에서 간과되기 쉬운 feedback 문제를 드러낸 연구로 평가하는 것이 정확하다. 가장 강한 교훈은 동시에 가장 불편한 교훈이다. 어떤 action이 안전하다는 사실을 배우는 유일한 방법이, 안전을 알기 전에 그 action을 시도하는 것일 때가 있다.
