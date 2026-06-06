---
layout: post
title: "Learning Data-Center Flexibility for Grid Demand Response with RMABs"
title_ko: "RMAB로 데이터센터 전력 유연성을 학습하는 grid demand response"
date: 2026-06-06
category: energy-grids
category_label: "Energy Grids"
research_group: application_reviews
research_category: energy-grids
research_category_label: "Energy Grids"
application_category: "energy-grids"
application_category_label: "Energy Grids"
method_category: ""
method_category_label: ""
paper_title: "Robust Restless Multi-Armed Bandit for Data Center Flexibility Services Through Virtual Machine Scheduling"
authors: "Ding, Y.; Chen, Z.; Magnanti, T."
venue: "arXiv preprint"
year: "2026"
doi: ""
arxiv: "2605.19116"
source_url: "https://arxiv.org/abs/2605.19116"
tags:
  - "demand response"
  - "data centers"
  - "restless bandits"
  - "Whittle index"
  - "Thompson sampling"
  - "flexibility procurement"
excerpt: "A critical note on modeling data centers as restless bandit arms for grid demand response, and on where the finite-state RMAB abstraction is useful or fragile."
excerpt_ko: "데이터센터를 전력망 demand response를 위한 restless bandit arm으로 모델링하는 접근을 정리하고, finite-state RMAB 추상화가 유용한 지점과 취약한 지점을 비판적으로 검토한다."
language: "en-ko"
has_korean_note: false
---

## Problem: data centers as flexible but private grid resources

The paper studies a grid-demand-response setting in which data centers can reduce short-term electricity consumption by delaying or reshuffling virtual-machine jobs. From the grid operator's perspective, this is attractive: data centers are large, controllable loads, and even a modest temporary reduction can be valuable during a peak or congestion event.

The hard part is that the grid operator does not see the internal scheduling state of each data center. It does not know the full job queue, delay sensitivity, QoS cost, thermal condition, or server-level availability. The operator only sees an aggregate or batch-level context and must decide which data centers should receive a flexibility request in each round.

The simplified decision problem is:

<math display="block" aria-label="RMAB activation budget">
  <munder><mi>max</mi><mi>&pi;</mi></munder>
  <mspace width="0.4em"></mspace>
  <msub><mi>E</mi><mi>&pi;</mi></msub>
  <mo>[</mo>
  <msubsup><mo>&sum;</mo><mrow><mi>t</mi><mo>=</mo><mn>0</mn></mrow><mi>&infin;</mi></msubsup>
  <msup><mi>&beta;</mi><mi>t</mi></msup>
  <msubsup><mo>&sum;</mo><mrow><mi>i</mi><mo>=</mo><mn>1</mn></mrow><mi>N</mi></msubsup>
  <msub><mi>r</mi><mrow><mi>i</mi><mo>,</mo><mi>t</mi></mrow></msub>
  <msub><mi>a</mi><mrow><mi>i</mi><mo>,</mo><mi>t</mi></mrow></msub>
  <mo>]</mo>
  <mspace width="1em"></mspace>
  <mtext>subject to</mtext>
  <mspace width="0.4em"></mspace>
  <msubsup><mo>&sum;</mo><mrow><mi>i</mi><mo>=</mo><mn>1</mn></mrow><mi>N</mi></msubsup>
  <msub><mi>a</mi><mrow><mi>i</mi><mo>,</mo><mi>t</mi></mrow></msub>
  <mo>&le;</mo>
  <msub><mi>N</mi><mi>t</mi></msub>
  <mo>,</mo>
  <mspace width="0.4em"></mspace>
  <msub><mi>a</mi><mrow><mi>i</mi><mo>,</mo><mi>t</mi></mrow></msub>
  <mo>&in;</mo>
  <mo>{</mo><mn>0</mn><mo>,</mo><mn>1</mn><mo>}</mo>
  <mo>.</mo>
</math>

Here each data center is an arm. Activating arm <math><mi>i</mi></math> means sending a flexibility request to that data center. The reward is the electricity-saving benefit minus the QoS or delay penalty caused by the rescheduling action.

This is a natural restless multi-armed bandit formulation because inactive data centers do not freeze. Their internal queues keep evolving even when the grid operator does not request flexibility.

## State and reward abstraction

The paper makes the data-center state finite by representing it as the current position in a circular VM-job queue. A state is not the full physical or operational state of the data center; it is the current batch position:

```text
s = 1: [job 1, job 2, ..., job Nj]
s = 2: [job 2, job 3, ..., job Nj+1]
...
```

When the operator activates a data center, the data center can choose lower-power jobs from a lookahead window and thereby reduce instantaneous power. The reward is roughly:

<math display="block" aria-label="Reward as energy saving minus delay penalty">
  <mi>r</mi><mo>(</mo><mi>s</mi><mo>)</mo>
  <mo>=</mo>
  <mi>max</mi>
  <mo>{</mo>
  <mn>0</mn>
  <mo>,</mo>
  <mspace width="0.4em"></mspace>
  <mi>LMP</mi>
  <mo>&middot;</mo>
  <mo>(</mo>
  <msub><mi>P</mi><mi>def</mi></msub><mo>(</mo><mi>s</mi><mo>)</mo>
  <mo>-</mo>
  <msub><mi>P</mi><mi>sel</mi></msub><mo>(</mo><mi>s</mi><mo>)</mo>
  <mo>)</mo>
  <mo>-</mo>
  <msub><mi>C</mi><mi>delay</mi></msub><mo>(</mo><mi>s</mi><mo>)</mo>
  <mo>}</mo>
  <mo>.</mo>
</math>

The important modeling choice is that the reward and transition dynamics are attached to this finite queue state. This makes the RMAB solvable and learnable, but it also compresses a very rich operational system into a small discrete representation.

## Whittle index view

Solving the full dynamic program over all data centers is intractable because the joint state space grows exponentially with the number of arms. The Whittle-index relaxation turns the global allocation problem into many single-arm subsidy problems.

The intuition is:

```text
Original problem:
  choose the best subset of data centers jointly

Whittle relaxation:
  ask each data center-state independently:
  how much passive subsidy would make passivity as attractive as activation?
```

For one arm, the active and passive values under a passive subsidy <math><mi>&lambda;</mi></math> can be written schematically as:

<math display="block" aria-label="Active and passive value comparison">
  <msup><mi>Q</mi><mn>1</mn></msup><mo>(</mo><mi>s</mi><mo>)</mo>
  <mo>=</mo>
  <mi>R</mi><mo>(</mo><mi>s</mi><mo>,</mo><mn>1</mn><mo>)</mo>
  <mo>+</mo>
  <mi>&beta;</mi>
  <msub><mo>&sum;</mo><msup><mi>s</mi><mo>&prime;</mo></msup></msub>
  <msup><mi>P</mi><mn>1</mn></msup><mo>(</mo><mi>s</mi><mo>,</mo><msup><mi>s</mi><mo>&prime;</mo></msup><mo>)</mo>
  <mi>V</mi><mo>(</mo><msup><mi>s</mi><mo>&prime;</mo></msup><mo>)</mo>
  <mo>,</mo>
  <mspace width="1em"></mspace>
  <msup><mi>Q</mi><mn>0</mn></msup><mo>(</mo><mi>s</mi><mo>)</mo>
  <mo>=</mo>
  <mi>R</mi><mo>(</mo><mi>s</mi><mo>,</mo><mn>0</mn><mo>)</mo>
  <mo>+</mo>
  <mi>&lambda;</mi>
  <mo>+</mo>
  <mi>&beta;</mi>
  <msub><mo>&sum;</mo><msup><mi>s</mi><mo>&prime;</mo></msup></msub>
  <msup><mi>P</mi><mn>0</mn></msup><mo>(</mo><mi>s</mi><mo>,</mo><msup><mi>s</mi><mo>&prime;</mo></msup><mo>)</mo>
  <mi>V</mi><mo>(</mo><msup><mi>s</mi><mo>&prime;</mo></msup><mo>)</mo>
  <mo>.</mo>
</math>

The Whittle index is the smallest passive subsidy that makes passive action preferable. A large index means that the operator would need to pay a large subsidy to justify not activating that data center-state; equivalently, activation is valuable.

## Learning: Thompson-Whittle with a trust-mixed exploration stage

Classical Whittle-index policies assume that rewards and transition probabilities are known. In the data-center setting, the operator does not know them. The paper therefore uses a Thompson-sampling style model-learning approach.

For each arm, the unknown model is treated as a stationary parameter:

<math display="block" aria-label="Stationary reward and transition model">
  <msub><mi>r</mi><mrow><mi>i</mi><mo>,</mo><mi>t</mi></mrow></msub>
  <mo>=</mo>
  <msub><mi>R</mi><mi>i</mi></msub>
  <mo>(</mo>
  <msub><mi>s</mi><mrow><mi>i</mi><mo>,</mo><mi>t</mi></mrow></msub>
  <mo>,</mo>
  <msub><mi>a</mi><mrow><mi>i</mi><mo>,</mo><mi>t</mi></mrow></msub>
  <mo>)</mo>
  <mo>+</mo>
  <msub><mi>&epsilon;</mi><mrow><mi>i</mi><mo>,</mo><mi>t</mi></mrow></msub>
  <mo>,</mo>
  <mspace width="1em"></mspace>
  <msub><mi>s</mi><mrow><mi>i</mi><mo>,</mo><mi>t</mi><mo>+</mo><mn>1</mn></mrow></msub>
  <mo>&sim;</mo>
  <msub><mi>P</mi><mi>i</mi></msub>
  <mo>(</mo>
  <mo>&middot;</mo>
  <mo>|</mo>
  <msub><mi>s</mi><mrow><mi>i</mi><mo>,</mo><mi>t</mi></mrow></msub>
  <mo>,</mo>
  <msub><mi>a</mi><mrow><mi>i</mi><mo>,</mo><mi>t</mi></mrow></msub>
  <mo>)</mo>
  <mo>.</mo>
</math>

The transition model uses Dirichlet-Categorical uncertainty, and the reward model uses Gaussian uncertainty. Each round samples a plausible model from the posterior, computes Whittle indices under that sampled model, and activates the top-ranked arms.

Pure Thompson-Whittle has a clear failure mode. Early in learning, many state-action transitions have barely been observed. The sampled transition model can be unstable, and the resulting Whittle-index ranking can be wrong. The paper's proposed Trust-Mixed Thompson-Whittle approach adds a decaying UCB-based greedy score:

```text
early rounds:   global/local UCB dominates
middle rounds:  state-level UCB and Whittle both matter
late rounds:    Whittle index dominates
```

This is best read as a practical mixed strategy: short-term robust exploration first, transition-aware RMAB control later.

## Experimental reading

The experiments use Microsoft Azure VM traces. The paper filters low-usage or low-utilization jobs and estimates power consumption and QoS cost, with GPU power modeled using hardware specifications such as NVIDIA A100 static and maximum power.

The main comparisons are Oracle Whittle, pure Thompson-Whittle, the proposed trust-mixed method, a state-only Thompson-style baseline, and EXP4-style expert mixing. The strongest empirical message is not that the proposed method changes the long-run RMAB theory. It is that pure Thompson-Whittle can be fragile in the early learning stage, and a scheduled UCB mixture can reduce that transient regret.

The reported improvement over pure Thompson-Whittle is positive but not overwhelming in every table. The supplied summary notes a roughly 0.17-2.14% improvement over TW in some settings. That should be interpreted as an early-learning robustness gain, not as a broad theoretical dominance result.

The noisy-context experiment is also subtle. When observation noise is high, the proposed method can outperform an "Oracle Whittle" baseline. This does not mean it beats an oracle with access to the true hidden state. It means the oracle baseline still performs a state-indexed Whittle lookup using corrupted observed state, while the UCB mixture can exploit aggregated statistics that are less brittle under noisy state labels.

## Where the abstraction is useful

The application idea is clean: if a grid operator cannot directly observe or query all internal data-center costs, it may learn which data centers tend to be useful in which coarse states. The RMAB formulation also captures an important feature that a myopic contextual bandit misses: activation affects future state distributions, not only immediate reward.

This makes the paper a useful computational proof-of-concept for grid-data-center coordination under limited observability. It gives a plausible algorithmic template:

```text
aggregate batch context
  -> posterior over reward and transition models
  -> sampled single-arm MDPs
  -> Whittle-index ranking
  -> activate a limited number of data centers
  -> observe feedback and update
```

For an application review, the most valuable contribution is this mapping from privacy-constrained data-center flexibility to a learning RMAB structure.

## Limitations: state abstraction, reward stationarity, and incentives

The weakest part of the application story is the gap between the real data-center state and the finite circular-queue state. A real operational state would include CPU and GPU utilization, memory pressure, VM queue composition, job deadlines, QoS sensitivity, thermal state, server availability, network constraints, electricity price, and perhaps carbon or local congestion signals. That is continuous, hybrid, high-dimensional, and partly private.

The paper's finite state is therefore a coarse abstraction:

<math display="block" aria-label="Coarse state abstraction">
  <msubsup><mi>s</mi><mrow><mi>i</mi><mo>,</mo><mi>t</mi></mrow><mi>real</mi></msubsup>
  <mo>&mapsto;</mo>
  <msub><mover accent="true"><mi>s</mi><mo>^</mo></mover><mrow><mi>i</mi><mo>,</mo><mi>t</mi></mrow></msub>
  <mo>=</mo>
  <mi>&psi;</mi>
  <mo>(</mo><msub><mi>x</mi><mrow><mi>i</mi><mo>,</mo><mi>t</mi></mrow></msub><mo>)</mo>
  <mo>.</mo>
</math>

This abstraction is valid only if the current batch position is sufficient to explain reward and transition behavior. Nonstationary workload arrivals, hidden QoS sensitivity, changing electricity prices, thermal constraints, or regime shifts can break that Markov abstraction.

The same issue appears in the reward model. Thompson sampling is not a magic solution for a reward that changes arbitrarily over time. In the paper, Thompson sampling learns a stationary unknown reward and transition model. If the true reward is instead driven by an external regime variable,

<math display="block" aria-label="Context-dependent nonstationary reward">
  <msub><mi>r</mi><mrow><mi>i</mi><mo>,</mo><mi>t</mi></mrow></msub>
  <mo>=</mo>
  <msub><mi>R</mi><mi>i</mi></msub>
  <mo>(</mo>
  <msub><mi>s</mi><mrow><mi>i</mi><mo>,</mo><mi>t</mi></mrow></msub>
  <mo>,</mo>
  <msub><mi>a</mi><mrow><mi>i</mi><mo>,</mo><mi>t</mi></mrow></msub>
  <mo>;</mo>
  <msub><mi>&eta;</mi><mi>t</mi></msub>
  <mo>)</mo>
  <mo>+</mo>
  <msub><mi>&epsilon;</mi><mrow><mi>i</mi><mo>,</mo><mi>t</mi></mrow></msub>
  <mo>,</mo>
</math>

then electricity price, workload regime, SLA condition, carbon intensity, or local grid congestion must either be included in the state/context or treated as stationary noise. Otherwise the posterior simply learns an averaged stationary model over a misspecified process.

There is also a procurement question. If each data center can truthfully report real-time flexibility, cost, and reliability, the grid operator could solve a direct flexibility procurement problem instead of learning an RMAB policy:

<math display="block" aria-label="Direct flexibility procurement">
  <munder><mi>min</mi><mi>a</mi></munder>
  <mspace width="0.4em"></mspace>
  <msub><mo>&sum;</mo><mi>i</mi></msub>
  <msub><mi>c</mi><mrow><mi>i</mi><mo>,</mo><mi>t</mi></mrow></msub>
  <msub><mi>a</mi><mrow><mi>i</mi><mo>,</mo><mi>t</mi></mrow></msub>
  <mspace width="1em"></mspace>
  <mtext>subject to</mtext>
  <mspace width="0.4em"></mspace>
  <msub><mo>&sum;</mo><mi>i</mi></msub>
  <mi>&Delta;</mi>
  <msub><mi>P</mi><mrow><mi>i</mi><mo>,</mo><mi>t</mi></mrow></msub>
  <msub><mi>a</mi><mrow><mi>i</mi><mo>,</mo><mi>t</mi></mrow></msub>
  <mo>&ge;</mo>
  <msubsup><mi>D</mi><mi>t</mi><mi>DR</mi></msubsup>
  <mo>,</mo>
  <mspace width="0.4em"></mspace>
  <msub><mi>a</mi><mrow><mi>i</mi><mo>,</mo><mi>t</mi></mrow></msub>
  <mo>&in;</mo>
  <mo>{</mo><mn>0</mn><mo>,</mo><mn>1</mn><mo>}</mo>
  <mo>.</mo>
</math>

That market-based formulation may be more natural when truthful real-time bids are available. The RMAB approach becomes more compelling when bids are unavailable, delayed, strategically filtered, or too privacy-sensitive to expose directly.

Finally, reward observability is under-specified. If the operator does not see internal QoS cost, how does it observe the net reward "power saving minus delay penalty"? If the data center reports the QoS penalty, incentive compatibility becomes central. If it does not, the operator may only learn grid-side power response, not true social reward. This creates tension with the privacy-preserving claim.

## Takeaway

This paper is best read as an application-oriented RMAB learning proof-of-concept, not yet as a complete grid-data-center coordination architecture. The finite circular-queue model makes the problem tractable and allows Thompson-Whittle learning, while the trust-mixed UCB stage addresses a real early-learning instability.

The application claim would be stronger with three additional pieces: a richer state or context model for continuous data-center operation, a clear settlement mechanism for observing net reward without violating privacy, and an incentive-compatible reason why the grid operator should learn activations instead of receiving real-time flexibility bids.

## References

Ding, Y., Chen, Z., & Magnanti, T. (2026). Robust Restless Multi-Armed Bandit for Data Center Flexibility Services Through Virtual Machine Scheduling. arXiv preprint arXiv:2605.19116.

<!-- ko -->

## 문제: 데이터센터를 flexible하지만 private한 전력망 자원으로 보기

이 논문은 데이터센터가 VM job을 조금 지연하거나 재배치해서 단기 전력 소비를 줄일 수 있다는 점에 주목한다. 전력망 입장에서는 데이터센터가 큰 controllable load이기 때문에, 피크나 congestion 상황에서 잠깐의 전력 절감도 demand response 자원으로 가치가 있다.

문제는 grid operator가 각 데이터센터의 내부 scheduling state를 직접 볼 수 없다는 점이다. job queue 전체, delay sensitivity, QoS cost, thermal condition, server availability 같은 정보는 데이터센터 내부의 private한 운영 정보에 가깝다. 따라서 operator는 aggregate 또는 batch-level context만 보고, 매 round 어느 데이터센터에 flexibility request를 보낼지 결정해야 한다.

논문이 단순화한 의사결정 문제는 다음과 같다.

<math display="block" aria-label="RMAB activation budget">
  <munder><mi>max</mi><mi>&pi;</mi></munder>
  <mspace width="0.4em"></mspace>
  <msub><mi>E</mi><mi>&pi;</mi></msub>
  <mo>[</mo>
  <msubsup><mo>&sum;</mo><mrow><mi>t</mi><mo>=</mo><mn>0</mn></mrow><mi>&infin;</mi></msubsup>
  <msup><mi>&beta;</mi><mi>t</mi></msup>
  <msubsup><mo>&sum;</mo><mrow><mi>i</mi><mo>=</mo><mn>1</mn></mrow><mi>N</mi></msubsup>
  <msub><mi>r</mi><mrow><mi>i</mi><mo>,</mo><mi>t</mi></mrow></msub>
  <msub><mi>a</mi><mrow><mi>i</mi><mo>,</mo><mi>t</mi></mrow></msub>
  <mo>]</mo>
  <mspace width="1em"></mspace>
  <mtext>subject to</mtext>
  <mspace width="0.4em"></mspace>
  <msubsup><mo>&sum;</mo><mrow><mi>i</mi><mo>=</mo><mn>1</mn></mrow><mi>N</mi></msubsup>
  <msub><mi>a</mi><mrow><mi>i</mi><mo>,</mo><mi>t</mi></mrow></msub>
  <mo>&le;</mo>
  <msub><mi>N</mi><mi>t</mi></msub>
  <mo>,</mo>
  <mspace width="0.4em"></mspace>
  <msub><mi>a</mi><mrow><mi>i</mi><mo>,</mo><mi>t</mi></mrow></msub>
  <mo>&in;</mo>
  <mo>{</mo><mn>0</mn><mo>,</mo><mn>1</mn><mo>}</mo>
  <mo>.</mo>
</math>

여기서 각 데이터센터는 하나의 arm이다. <math><mi>a</mi></math>가 1이면 해당 데이터센터에 flexibility request를 보내는 것이고, reward는 전력 절감 benefit에서 QoS 또는 delay penalty를 뺀 값이다.

이 문제는 restless multi-armed bandit으로 보기 자연스럽다. 요청을 보내지 않은 데이터센터도 멈춰 있는 것이 아니라, 내부 job queue가 계속 시간에 따라 변하기 때문이다.

## State와 reward의 추상화

논문은 데이터센터 state를 finite하게 만들기 위해 circular VM job queue에서 현재 batch 위치를 state로 둔다. 즉 state는 데이터센터의 전체 물리적, 운영적 상태가 아니라 현재 batch position이다.

```text
s = 1: [job 1, job 2, ..., job Nj]
s = 2: [job 2, job 3, ..., job Nj+1]
...
```

operator가 데이터센터를 activate하면, 데이터센터는 lookahead window 안에서 더 낮은 power를 쓰는 job을 선택해 instantaneous power를 낮출 수 있다. reward는 대략 다음 구조다.

<math display="block" aria-label="Reward as energy saving minus delay penalty">
  <mi>r</mi><mo>(</mo><mi>s</mi><mo>)</mo>
  <mo>=</mo>
  <mi>max</mi>
  <mo>{</mo>
  <mn>0</mn>
  <mo>,</mo>
  <mspace width="0.4em"></mspace>
  <mi>LMP</mi>
  <mo>&middot;</mo>
  <mo>(</mo>
  <msub><mi>P</mi><mi>def</mi></msub><mo>(</mo><mi>s</mi><mo>)</mo>
  <mo>-</mo>
  <msub><mi>P</mi><mi>sel</mi></msub><mo>(</mo><mi>s</mi><mo>)</mo>
  <mo>)</mo>
  <mo>-</mo>
  <msub><mi>C</mi><mi>delay</mi></msub><mo>(</mo><mi>s</mi><mo>)</mo>
  <mo>}</mo>
  <mo>.</mo>
</math>

핵심 modeling choice는 reward와 transition dynamics를 이 finite queue state에 붙인다는 점이다. 이 선택 덕분에 RMAB를 풀고 학습할 수 있지만, 동시에 매우 복잡한 운영 시스템을 작은 discrete representation으로 압축한다.

## Whittle index 관점

모든 데이터센터의 joint state를 놓고 full dynamic programming을 풀기는 어렵다. arm 수가 늘수록 joint state space가 지수적으로 커지기 때문이다. Whittle-index relaxation은 global allocation 문제를 여러 single-arm subsidy problem으로 바꾼다.

직관은 다음과 같다.

```text
Original problem:
  choose the best subset of data centers jointly

Whittle relaxation:
  ask each data center-state independently:
  how much passive subsidy would make passivity as attractive as activation?
```

하나의 arm에 대해 passive subsidy <math><mi>&lambda;</mi></math>를 두면 active value와 passive value는 다음처럼 쓸 수 있다.

<math display="block" aria-label="Active and passive value comparison">
  <msup><mi>Q</mi><mn>1</mn></msup><mo>(</mo><mi>s</mi><mo>)</mo>
  <mo>=</mo>
  <mi>R</mi><mo>(</mo><mi>s</mi><mo>,</mo><mn>1</mn><mo>)</mo>
  <mo>+</mo>
  <mi>&beta;</mi>
  <msub><mo>&sum;</mo><msup><mi>s</mi><mo>&prime;</mo></msup></msub>
  <msup><mi>P</mi><mn>1</mn></msup><mo>(</mo><mi>s</mi><mo>,</mo><msup><mi>s</mi><mo>&prime;</mo></msup><mo>)</mo>
  <mi>V</mi><mo>(</mo><msup><mi>s</mi><mo>&prime;</mo></msup><mo>)</mo>
  <mo>,</mo>
  <mspace width="1em"></mspace>
  <msup><mi>Q</mi><mn>0</mn></msup><mo>(</mo><mi>s</mi><mo>)</mo>
  <mo>=</mo>
  <mi>R</mi><mo>(</mo><mi>s</mi><mo>,</mo><mn>0</mn><mo>)</mo>
  <mo>+</mo>
  <mi>&lambda;</mi>
  <mo>+</mo>
  <mi>&beta;</mi>
  <msub><mo>&sum;</mo><msup><mi>s</mi><mo>&prime;</mo></msup></msub>
  <msup><mi>P</mi><mn>0</mn></msup><mo>(</mo><mi>s</mi><mo>,</mo><msup><mi>s</mi><mo>&prime;</mo></msup><mo>)</mo>
  <mi>V</mi><mo>(</mo><msup><mi>s</mi><mo>&prime;</mo></msup><mo>)</mo>
  <mo>.</mo>
</math>

Whittle index는 passive action이 active action보다 좋아지게 만드는 최소 subsidy다. index가 크다는 것은 그 state의 arm을 activate하지 않으려면 큰 subsidy가 필요하다는 뜻이고, 따라서 activate할 가치가 크다는 의미로 읽을 수 있다.

## Learning: Thompson-Whittle과 trust-mixed exploration

기존 Whittle-index policy는 reward와 transition probability를 알고 있다고 가정한다. 하지만 데이터센터 setting에서는 operator가 이를 모른다. 그래서 논문은 Thompson sampling 스타일의 model learning을 사용한다.

각 arm의 unknown model은 stationary parameter로 취급된다.

<math display="block" aria-label="Stationary reward and transition model">
  <msub><mi>r</mi><mrow><mi>i</mi><mo>,</mo><mi>t</mi></mrow></msub>
  <mo>=</mo>
  <msub><mi>R</mi><mi>i</mi></msub>
  <mo>(</mo>
  <msub><mi>s</mi><mrow><mi>i</mi><mo>,</mo><mi>t</mi></mrow></msub>
  <mo>,</mo>
  <msub><mi>a</mi><mrow><mi>i</mi><mo>,</mo><mi>t</mi></mrow></msub>
  <mo>)</mo>
  <mo>+</mo>
  <msub><mi>&epsilon;</mi><mrow><mi>i</mi><mo>,</mo><mi>t</mi></mrow></msub>
  <mo>,</mo>
  <mspace width="1em"></mspace>
  <msub><mi>s</mi><mrow><mi>i</mi><mo>,</mo><mi>t</mi><mo>+</mo><mn>1</mn></mrow></msub>
  <mo>&sim;</mo>
  <msub><mi>P</mi><mi>i</mi></msub>
  <mo>(</mo>
  <mo>&middot;</mo>
  <mo>|</mo>
  <msub><mi>s</mi><mrow><mi>i</mi><mo>,</mo><mi>t</mi></mrow></msub>
  <mo>,</mo>
  <msub><mi>a</mi><mrow><mi>i</mi><mo>,</mo><mi>t</mi></mrow></msub>
  <mo>)</mo>
  <mo>.</mo>
</math>

transition에는 Dirichlet-Categorical uncertainty를, reward에는 Gaussian uncertainty를 둔다. 매 round posterior에서 plausible model을 sample하고, 그 sampled model에서 Whittle index를 계산한 뒤 top-ranked arm들을 activate한다.

Pure Thompson-Whittle의 failure mode는 분명하다. learning 초기에는 많은 state-action transition을 거의 관측하지 못한다. 그러면 sampled transition model이 흔들리고, Whittle-index ranking도 잘못될 수 있다. 논문의 Trust-Mixed Thompson-Whittle은 여기에 decaying UCB-based greedy score를 섞는다.

```text
early rounds:   global/local UCB dominates
middle rounds:  state-level UCB and Whittle both matter
late rounds:    Whittle index dominates
```

따라서 이 방법은 short-term robust exploration을 먼저 하고, 시간이 지나 transition posterior가 안정되면 transition-aware RMAB control로 넘어가는 practical mixed strategy로 읽는 것이 좋다.

## 실험 결과 해석

논문은 Microsoft Azure VM trace를 사용한다. low-usage 또는 low-utilization job을 filtering하고, power consumption과 QoS cost를 추정한다. GPU power는 NVIDIA A100 같은 hardware specification을 참고해 static power와 maximum power를 두는 방식으로 모델링한다.

주요 비교 대상은 Oracle Whittle, pure Thompson-Whittle, 제안한 trust-mixed method, state-only Thompson-style baseline, EXP4-style expert mixing이다. 가장 강한 메시지는 long-run RMAB theory가 바뀌었다는 것이 아니다. Pure Thompson-Whittle이 early learning stage에서 취약할 수 있고, scheduled UCB mixture가 그 transient regret을 줄일 수 있다는 점이다.

첨부 요약 기준으로 TM-TW는 일부 setting에서 pure TW 대비 약 0.17-2.14% 개선을 보인다. 이는 긍정적인 결과지만 압도적인 차이는 아니다. 따라서 broad theoretical dominance라기보다는 early-learning robustness gain으로 해석하는 편이 정확하다.

Noisy-context 실험도 조심해서 읽어야 한다. observation noise가 클 때 제안 method가 "Oracle Whittle"보다 높게 나오는 경우가 있는데, 이것은 true hidden state까지 아는 완전한 oracle을 이겼다는 뜻이 아니다. 해당 oracle baseline도 corrupted observed state로 state-indexed Whittle lookup을 하기 때문에, aggregated statistics를 쓰는 UCB mixture가 noisy state label 아래에서 덜 brittle했음을 보여주는 결과에 가깝다.

## 이 추상화가 유용한 지점

application idea 자체는 명확하다. Grid operator가 데이터센터 내부 비용을 직접 관측하거나 질의할 수 없다면, coarse state에서 어떤 데이터센터가 가치 있는지 학습하는 접근이 의미를 가질 수 있다. 또한 RMAB formulation은 myopic contextual bandit이 놓치기 쉬운 점, 즉 activation이 immediate reward뿐 아니라 future state distribution에도 영향을 준다는 점을 반영한다.

이 점에서 논문은 limited observability 아래의 grid-data center coordination에 대한 computational proof-of-concept로 유용하다. 전체 구조는 다음처럼 볼 수 있다.

```text
aggregate batch context
  -> posterior over reward and transition models
  -> sampled single-arm MDPs
  -> Whittle-index ranking
  -> activate a limited number of data centers
  -> observe feedback and update
```

Application review 관점에서 가장 중요한 contribution은 privacy-constrained data-center flexibility 문제를 learning RMAB structure로 mapping한 것이다.

## 한계: state abstraction, reward stationarity, incentive

가장 약한 부분은 실제 데이터센터 state와 finite circular-queue state 사이의 간극이다. 실제 operational state는 CPU/GPU utilization, memory pressure, VM queue composition, job deadlines, QoS sensitivity, thermal state, server availability, network constraints, electricity price, carbon signal, local congestion 등을 포함한다. 이는 continuous, hybrid, high-dimensional, partially private state다.

따라서 논문의 finite state는 다음과 같은 coarse abstraction이다.

<math display="block" aria-label="Coarse state abstraction">
  <msubsup><mi>s</mi><mrow><mi>i</mi><mo>,</mo><mi>t</mi></mrow><mi>real</mi></msubsup>
  <mo>&mapsto;</mo>
  <msub><mover accent="true"><mi>s</mi><mo>^</mo></mover><mrow><mi>i</mi><mo>,</mo><mi>t</mi></mrow></msub>
  <mo>=</mo>
  <mi>&psi;</mi>
  <mo>(</mo><msub><mi>x</mi><mrow><mi>i</mi><mo>,</mo><mi>t</mi></mrow></msub><mo>)</mo>
  <mo>.</mo>
</math>

이 abstraction이 성립하려면 현재 batch position만으로 reward와 transition behavior를 충분히 설명할 수 있어야 한다. 하지만 workload arrival이 nonstationary하거나, QoS sensitivity가 hidden variable이거나, electricity price와 thermal constraint가 변하면 Markov abstraction은 쉽게 깨질 수 있다.

Reward model도 마찬가지다. Thompson sampling은 시간이 따라 임의로 바뀌는 reward를 자동으로 맞히는 magic이 아니다. 이 논문에서 Thompson sampling은 stationary unknown reward/transition model을 학습한다. 만약 실제 reward가 외생 regime variable에 의해 다음처럼 바뀐다면,

<math display="block" aria-label="Context-dependent nonstationary reward">
  <msub><mi>r</mi><mrow><mi>i</mi><mo>,</mo><mi>t</mi></mrow></msub>
  <mo>=</mo>
  <msub><mi>R</mi><mi>i</mi></msub>
  <mo>(</mo>
  <msub><mi>s</mi><mrow><mi>i</mi><mo>,</mo><mi>t</mi></mrow></msub>
  <mo>,</mo>
  <msub><mi>a</mi><mrow><mi>i</mi><mo>,</mo><mi>t</mi></mrow></msub>
  <mo>;</mo>
  <msub><mi>&eta;</mi><mi>t</mi></msub>
  <mo>)</mo>
  <mo>+</mo>
  <msub><mi>&epsilon;</mi><mrow><mi>i</mi><mo>,</mo><mi>t</mi></mrow></msub>
  <mo>,</mo>
</math>

electricity price, workload regime, SLA condition, carbon intensity, local grid congestion 같은 변수가 state/context에 들어가야 한다. 그렇지 않으면 posterior는 misspecified process 위에서 stationary average를 학습할 뿐이다.

또 하나는 procurement 관점의 질문이다. 각 데이터센터가 real-time flexibility, cost, reliability를 정직하게 report할 수 있다면, grid operator는 RMAB를 학습하기보다 직접 flexibility procurement problem을 풀 수 있다.

<math display="block" aria-label="Direct flexibility procurement">
  <munder><mi>min</mi><mi>a</mi></munder>
  <mspace width="0.4em"></mspace>
  <msub><mo>&sum;</mo><mi>i</mi></msub>
  <msub><mi>c</mi><mrow><mi>i</mi><mo>,</mo><mi>t</mi></mrow></msub>
  <msub><mi>a</mi><mrow><mi>i</mi><mo>,</mo><mi>t</mi></mrow></msub>
  <mspace width="1em"></mspace>
  <mtext>subject to</mtext>
  <mspace width="0.4em"></mspace>
  <msub><mo>&sum;</mo><mi>i</mi></msub>
  <mi>&Delta;</mi>
  <msub><mi>P</mi><mrow><mi>i</mi><mo>,</mo><mi>t</mi></mrow></msub>
  <msub><mi>a</mi><mrow><mi>i</mi><mo>,</mo><mi>t</mi></mrow></msub>
  <mo>&ge;</mo>
  <msubsup><mi>D</mi><mi>t</mi><mi>DR</mi></msubsup>
  <mo>,</mo>
  <mspace width="0.4em"></mspace>
  <msub><mi>a</mi><mrow><mi>i</mi><mo>,</mo><mi>t</mi></mrow></msub>
  <mo>&in;</mo>
  <mo>{</mo><mn>0</mn><mo>,</mo><mn>1</mn><mo>}</mo>
  <mo>.</mo>
</math>

Truthful real-time bid가 가능하다면 market-based formulation이 더 자연스러울 수 있다. RMAB approach는 bid가 불가능하거나, 늦거나, strategic하게 filtered되거나, privacy 때문에 직접 공개하기 어려울 때 더 설득력을 가진다.

마지막으로 reward observability가 충분히 명확하지 않다. Operator가 내부 QoS cost를 볼 수 없다면, "power saving minus delay penalty"라는 net reward를 어떻게 관측하는가? 데이터센터가 QoS penalty를 report한다면 incentive compatibility가 핵심 문제가 된다. report하지 않는다면 operator는 grid-side power response만 학습할 수 있고 true social reward는 학습하지 못할 수 있다. 이 지점은 privacy-preserving claim과 긴장 관계에 있다.

## Takeaway

이 논문은 완성된 grid-data center coordination architecture라기보다는 application-oriented RMAB learning proof-of-concept로 읽는 것이 적절하다. Finite circular-queue model은 문제를 tractable하게 만들고 Thompson-Whittle learning을 가능하게 한다. Trust-mixed UCB stage도 early learning instability를 줄이는 practical한 장치다.

다만 application claim이 강해지려면 세 가지가 더 필요하다. 실제 데이터센터 운영을 반영하는 richer state/context model, privacy를 크게 침해하지 않으면서 net reward를 관측할 수 있는 settlement mechanism, 그리고 grid operator가 real-time flexibility bid를 받는 대신 activation policy를 학습해야 하는 incentive-compatible operational reason이다.

## References

Ding, Y., Chen, Z., & Magnanti, T. (2026). Robust Restless Multi-Armed Bandit for Data Center Flexibility Services Through Virtual Machine Scheduling. arXiv preprint arXiv:2605.19116.
