---
layout: post
title: "When No Violation Is Found: Probabilistic Certification and Benders Cuts"
title_ko: "위반을 못 찾았을 때: Soft separation의 확률적 인증과 Benders cut"
date: 2026-10-28
category: stochastic-nonlinear-optimization
category_label: "Mathematical Optimization"
research_group: algorithmic_reviews
research_category: stochastic-nonlinear-optimization
research_category_label: "Mathematical Optimization"
application_category: ""
application_category_label: ""
method_category: "stochastic-nonlinear-optimization"
method_category_label: "Mathematical Optimization"
paper_title: "Soft Separation for Adaptive Robust Optimization"
authors: "Qingyuan Xu; Ruiwei Jiang"
venue: "arXiv preprint"
year: "2026"
doi: "10.48550/arXiv.2609.36275"
arxiv: "2609.36275v1"
source_url: "https://arxiv.org/abs/2609.36275v1"
tags:
  - "soft separation"
  - "probabilistic certification"
  - "Benders decomposition"
  - "Markov chains"
  - "mixed-integer optimization"
  - "robust optimization"
excerpt: "What a conditional miss bound means, how certification costs grow, and how sampled scenario cuts support mixed-integer robust optimization."
excerpt_ko: "조건부 놓침 확률의 의미와 인증 검사량을 계산하고, 오류 예산 배분과 정수 설계별 Markov chain을 Benders cut에 연결합니다."
language: "en-ko"
has_korean_note: false
---

Many scenarios have been checked, and no violation has appeared. Can the current design be accepted? Low costs in the scenarios already inspected are insufficient. We need to know how readily the search would have found a violation if one remained.

The [previous mellowmax note]({% post_url 2026-10-23-markov-stationary-distributions-optimization-bias %}) examined how Markov-chain visit frequencies and sampling bias affect an optimization direction. Soft separation uses such probabilistic scenario searches to find violations. Certifying a fixed design requires a bound on the probability of missing a remaining violation. That bound determines the cost of certification and its role in mixed-integer Benders methods.

## 1. Valid cuts from sampled scenarios

Let f(x) be the investment cost of design x and <math><msub><mrow><mi>Q</mi></mrow><mrow><mi>i</mi></mrow></msub></math>(x) the optimal operating cost under scenario i. With m scenarios, the robust optimization problem is

<math display="block" aria-label="The finite-scenario robust objective"><mtable columnalign="left" displaystyle="true" rowspacing="0.45em"><mtr><mtd><msup><mrow><mi>F</mi></mrow><mrow><mo>⋆</mo></mrow></msup><mo>=</mo><munder><mrow><mi>min</mi></mrow><mrow><mi>x</mi><mo>∈</mo><mi>X</mi></mrow></munder><mi>F</mi><mrow><mo>(</mo><mi>x</mi><mo>)</mo></mrow></mtd></mtr><mtr><mtd><mi>F</mi><mrow><mo>(</mo><mi>x</mi><mo>)</mo></mrow><mo>:=</mo><mi>f</mi><mrow><mo>(</mo><mi>x</mi><mo>)</mo></mrow><mo>+</mo><msup><mrow><mi>Q</mi></mrow><mrow><mo>⋆</mo></mrow></msup><mrow><mo>(</mo><mi>x</mi><mo>)</mo></mrow></mtd></mtr><mtr><mtd><msup><mrow><mi>Q</mi></mrow><mrow><mo>⋆</mo></mrow></msup><mrow><mo>(</mo><mi>x</mi><mo>)</mo></mrow><mo>:=</mo><munder><mrow><mi>max</mi></mrow><mrow><mrow><mn>1</mn><mo>≤</mo><mi>i</mi><mo>≤</mo><mi>m</mi></mrow></mrow></munder><msub><mrow><mi>Q</mi></mrow><mrow><mi>i</mi></mrow></msub><mrow><mo>(</mo><mi>x</mi><mo>)</mo></mrow></mtd></mtr></mtable></math>

The set X may include integer variables such as facility-opening decisions. Introducing an auxiliary variable θ gives a constraint <math><mi>θ</mi><mo>≥</mo><msub><mrow><mi>Q</mi></mrow><mrow><mi>i</mi></mrow></msub><mrow><mo>(</mo><mi>x</mi><mo>)</mo></mrow></math> for each scenario. A master problem approximates these constraints with a subset of cuts and produces a candidate <math><mrow><mo>(</mo><mrow><mover><mi>x</mi><mo>¯</mo></mover><mo>,</mo><mover><mi>θ</mi><mo>¯</mo></mover></mrow><mo>)</mo></mrow></math>. Separation checks whether its θ is too small.

Assume linear recourse is feasible and finite for every design and scenario under consideration, with strong duality. Using a dual feasible region Π that does not depend on the design, write

<math display="block" aria-label="Linear recourse in dual form"><msub><mrow><mi>Q</mi></mrow><mrow><mi>i</mi></mrow></msub><mrow><mo>(</mo><mi>x</mi><mo>)</mo></mrow><mo>=</mo><munder><mrow><mi>max</mi></mrow><mrow><mi>π</mi><mo>∈</mo><mi>Π</mi></mrow></munder><msup><mrow><mi>π</mi></mrow><mrow><mtext>T</mtext></mrow></msup><mrow><mo>(</mo><mrow><mi>h</mi><mo>−</mo><mi>E</mi><mi>x</mi><mo>−</mo><mi>U</mi><msub><mrow><mi>ξ</mi></mrow><mrow><mi>i</mi></mrow></msub></mrow><mo>)</mo></mrow></math>

Here h is the right-hand-side vector, E and U describe how design and uncertainty enter that vector, and <math><msub><mrow><mi>ξ</mi></mrow><mrow><mi>i</mi></mrow></msub></math> contains the scenario data. Fix an optimal dual solution <math><msub><mrow><mover><mi>π</mi><mo>¯</mo></mover></mrow><mrow><mi>i</mi></mrow></msub></math> obtained by solving scenario i at the current design. Then

<math display="block" aria-label="A dual feasible solution gives a global lower cut"><mtable columnalign="left" displaystyle="true" rowspacing="0.45em"><mtr><mtd><msub><mrow><mi>a</mi></mrow><mrow><mi>i</mi></mrow></msub><mrow><mo>(</mo><mi>x</mi><mo>)</mo></mrow><mo>:=</mo><msup><mrow><msub><mrow><mover><mi>π</mi><mo>¯</mo></mover></mrow><mrow><mi>i</mi></mrow></msub></mrow><mrow><mtext>T</mtext></mrow></msup><mrow><mo>(</mo><mrow><mi>h</mi><mo>−</mo><mi>E</mi><mi>x</mi><mo>−</mo><mi>U</mi><msub><mrow><mi>ξ</mi></mrow><mrow><mi>i</mi></mrow></msub></mrow><mo>)</mo></mrow></mtd></mtr><mtr><mtd><msub><mrow><mi>a</mi></mrow><mrow><mi>i</mi></mrow></msub><mrow><mo>(</mo><mi>x</mi><mo>)</mo></mrow><mo>≤</mo><msub><mrow><mi>Q</mi></mrow><mrow><mi>i</mi></mrow></msub><mrow><mo>(</mo><mi>x</mi><mo>)</mo></mrow><mo>≤</mo><mrow><munder><mrow><mi>max</mi></mrow><mrow><mi>j</mi></mrow></munder><msub><mrow><mi>Q</mi></mrow><mrow><mi>j</mi></mrow></msub><mrow><mo>(</mo><mi>x</mi><mo>)</mo></mrow></mrow></mtd></mtr></mtable></math>

so <math><mi>θ</mi><mo>≥</mo><msub><mrow><mi>a</mi></mrow><mrow><mi>i</mi></mrow></msub><mrow><mo>(</mo><mi>x</mi><mo>)</mo></mrow></math> is a valid Benders cut for the robust problem. Scenario i need not be the worst one. If the current θ is 100 and the sampled scenario costs 120, that scenario can cut off the candidate even if the actual maximum cost is 150. The cut from an optimal dual solution equals 120 at the current point.

Dual feasibility makes the cut valid; dual optimality at the current point makes it tight there. The event requiring a probability bound is failure to discover a remaining violation.

## 2. The probability bounded by ρ

Fix a candidate <math><mrow><mo>(</mo><mrow><mover><mi>x</mi><mo>¯</mo></mover><mo>,</mo><mover><mi>θ</mi><mo>¯</mo></mover></mrow><mo>)</mo></mrow></math> and define its set of violating scenarios as

<math display="block" aria-label="Violating scenarios at a fixed candidate"><mi>V</mi><mo>:=</mo><mo>{</mo><mi>i</mi><mo>:</mo><msub><mrow><mi>Q</mi></mrow><mrow><mi>i</mi></mrow></msub><mrow><mo>(</mo><mover><mi>x</mi><mo>¯</mo></mover><mo>)</mo></mrow><mo>&gt;</mo><mover><mi>θ</mi><mo>¯</mo></mover><mo>}</mo></math>

Initially, use zero cost tolerance and count one check as selecting a scenario and evaluating its cost exactly.

Suppose V is nonempty. Let <math><msub><mrow><mi>ℋ</mi></mrow><mrow><mi>t</mi></mrow></msub></math> contain both the optimization history before certification and every check so far. For every possible history in which no violation has yet been found, require

<math display="block" aria-label="A conditional miss bound on every history without a detection"><mi>Pr</mi><mrow><mo>(</mo><msub><mrow><mi>I</mi></mrow><mrow><mrow><mi>t</mi><mo>+</mo><mn>1</mn></mrow></mrow></msub><mo>∉</mo><mi>V</mi><mo>∣</mo><msub><mrow><mi>ℋ</mi></mrow><mrow><mi>t</mi></mrow></msub><mo>)</mo></mrow><mo>≤</mo><mi>ρ</mi><mo>&lt;</mo><mn>1</mn></math>

With ρ = 0.9, the next check has at most a 90% probability of missing and at least a 10% probability of detecting a violation. The actual miss probability need not equal 90%.

Applying this conditional bound repeatedly gives, for a fixed violating candidate,

<math display="block" aria-label="Probability of K consecutive misses for a violating candidate"><mi>Pr</mi><mrow><mo>(</mo><munder><mrow><mo>⋂</mo></mrow><mrow><mrow><mi>t</mi><mo>=</mo><mn>1</mn><mo>,</mo><mo>…</mo><mo>,</mo><mi>K</mi></mrow></mrow></munder><mo>{</mo><msub><mrow><mi>I</mi></mrow><mrow><mi>t</mi></mrow></msub><mo>∉</mo><mi>V</mi><mo>}</mo><mo>∣</mo><msub><mrow><mi>ℋ</mi></mrow><mrow><mn>0</mn></mrow></msub><mo>)</mo></mrow><mo>≤</mo><msup><mrow><mi>ρ</mi></mrow><mrow><mi>K</mi></mrow></msup></math>

The checks need not be independent. The bound must instead remain valid conditional on what has already been observed. An average miss frequency of 90% over an entire run does not establish this condition.

For 0 < ρ < 1 and a per-candidate false-certification allowance <math><msub><mrow><mi>β</mi></mrow><mrow><mi>ℓ</mi></mrow></msub></math> between zero and one, choose

<math display="block" aria-label="Checks required for a per-attempt error allowance"><msub><mrow><mi>K</mi></mrow><mrow><mi>ℓ</mi></mrow></msub><mo>=</mo><mrow><mo>⌈</mo><mfrac><mrow><mi>log</mi><mrow><mo>(</mo><mfrac><mrow><mn>1</mn></mrow><mrow><msub><mrow><mi>β</mi></mrow><mrow><mi>ℓ</mi></mrow></msub></mrow></mfrac><mo>)</mo></mrow></mrow><mrow><mi>log</mi><mrow><mo>(</mo><mfrac><mrow><mn>1</mn></mrow><mrow><mi>ρ</mi></mrow></mfrac><mo>)</mo></mrow></mrow></mfrac><mo>⌉</mo></mrow></math>

and finish certification after that many consecutive checks without a violation. We choose <math><msub><mrow><mi>β</mi></mrow><mrow><mi>ℓ</mi></mrow></msub></math> as a target; we must justify ρ as a property of the search. This allowance controls the procedure's probability of accepting a violating candidate.

## 3. Stationary probabilities and reaching the violation set

Let P be the Markov transition matrix at the fixed design. From a current scenario i outside V, the probability of missing a violation on the next check is

<math display="block" aria-label="The miss probability is one minus the transition probability into V"><mtable columnalign="left" displaystyle="true" rowspacing="0.45em"><mtr><mtd><mi>Pr</mi><mrow><mo>(</mo><msub><mrow><mi>I</mi></mrow><mrow><mrow><mi>t</mi><mo>+</mo><mn>1</mn></mrow></mrow></msub><mo>∉</mo><mi>V</mi><mo>∣</mo><msub><mrow><mi>I</mi></mrow><mrow><mi>t</mi></mrow></msub><mo>=</mo><mi>i</mi><mo>)</mo></mrow></mtd></mtr><mtr><mtd><mo>=</mo><mn>1</mn><mo>−</mo><munder><mrow><mo>∑</mo></mrow><mrow><mi>j</mi><mo>∈</mo><mi>V</mi></mrow></munder><mi>P</mi><mrow><mo>(</mo><mrow><mi>i</mi><mo>,</mo><mi>j</mi></mrow><mo>)</mo></mrow></mtd></mtr></mtable></math>

Using ρ = 0.9 therefore requires at least a 0.1 probability of entering V from every reachable state in which no violation has been found. If some state cannot reach V in one transition, such a one-transition bound fails. Several transitions could form one checking unit, but both its probability bound and its cost would need to be recalculated.

Consider standard Metropolis-Hastings on 100 scenarios, with independent uniform proposals over the entire set. The target is <math><msub><mrow><mi>p</mi></mrow><mrow><mi>x</mi></mrow></msub><mrow><mo>(</mo><mi>i</mi><mo>)</mo></mrow><mo>∝</mo><mi>exp</mi><mrow><mo>(</mo><mfrac><mrow><msub><mrow><mi>Q</mi></mrow><mrow><mi>i</mi></mrow></msub><mrow><mo>(</mo><mi>x</mi><mo>)</mo></mrow></mrow><mrow><mi>w</mi></mrow></mfrac><mo>)</mo></mrow></math>, with w > 0. If the current scenario is nonviolating and the proposal violates, the proposed cost is higher, so acceptance has probability one.

| Number of violating scenarios | Detection probability per check | Miss probability per check |
|---:|---:|---:|
| 50 | 0.50 | 0.50 |
| 10 | 0.10 | 0.90 |
| 1 | 0.01 | 0.99 |
{: style="border-spacing: 0.5rem 0.35rem; width: 100%;" }

Applying ρ = 0.9 in the last case underestimates the certification error. Lowering the temperature can increase the violating scenario's stationary probability, but leaves its probability of first being proposed unchanged. Frequent visits in stationarity and rapid discovery from the current state are different properties.

Numerically, <math><msup><mrow><mn>0.9</mn></mrow><mrow><mn>50</mn></mrow></msup></math> is about 0.00515, whereas <math><msup><mrow><mn>0.99</mn></mrow><mrow><mn>50</mn></mrow></msup></math> is about 0.605. For the same 50 checks, the upper bound on consecutive misses changes sharply depending on whether the justified one-check bound is 0.9 or 0.99.

## 4. Do later candidates require an explosion in checks?

The number of certification attempts is usually unknown in advance. Giving every attempt the same error allowance makes it difficult to control the probability of any false certification over the entire run. Indexing actual certification attempts by ℓ, one allocation of a total error budget β is

<math display="block" aria-label="A summable error budget across certification attempts"><mtable columnalign="left" displaystyle="true" rowspacing="0.45em"><mtr><mtd><msub><mrow><mi>β</mi></mrow><mrow><mi>ℓ</mi></mrow></msub><mo>=</mo><mfrac><mrow><mi>β</mi></mrow><mrow><mi>ℓ</mi><mrow><mo>(</mo><mrow><mi>ℓ</mi><mo>+</mo><mn>1</mn></mrow><mo>)</mo></mrow></mrow></mfrac><mo>,</mo><mi>ℓ</mi><mo>=</mo><mn>1</mn><mo>,</mo><mn>2</mn><mo>,</mo><mo>…</mo></mtd></mtr><mtr><mtd><munderover><mo>∑</mo><mrow><mi>ℓ</mi><mo>=</mo><mn>1</mn></mrow><mrow><mo>∞</mo></mrow></munderover><msub><mrow><mi>β</mi></mrow><mrow><mi>ℓ</mi></mrow></msub><mo>=</mo><mi>β</mi></mtd></mtr></mtable></math>

The series telescopes to β. If each attempt's error probability is bounded by <math><msub><mrow><mi>β</mi></mrow><mrow><mi>ℓ</mi></mrow></msub></math> even conditional on its starting history, the union bound controls the overall error by β despite dependence between attempts. [Xu and Jiang, Section 4.2](https://arxiv.org/html/2609.36275v1)

Substituting this allocation into the checking rule gives

<math display="block" aria-label="Logarithmic growth in the attempt index for fixed beta and rho"><msub><mrow><mi>K</mi></mrow><mrow><mi>ℓ</mi></mrow></msub><mo>=</mo><mrow><mo>⌈</mo><mfrac><mrow><mi>log</mi><mrow><mo>(</mo><mfrac><mrow><mn>1</mn></mrow><mrow><mi>β</mi></mrow></mfrac><mo>)</mo></mrow><mo>+</mo><mi>log</mi><mrow><mo>(</mo><mi>ℓ</mi><mo>)</mo></mrow><mo>+</mo><mi>log</mi><mrow><mo>(</mo><mrow><mi>ℓ</mi><mo>+</mo><mn>1</mn></mrow><mo>)</mo></mrow></mrow><mrow><mi>log</mi><mrow><mo>(</mo><mfrac><mrow><mn>1</mn></mrow><mrow><mi>ρ</mi></mrow></mfrac><mo>)</mo></mrow></mrow></mfrac><mo>⌉</mo></mrow></math>

For fixed β and ρ, <math><msub><mrow><mi>K</mi></mrow><mrow><mi>ℓ</mi></mrow></msub></math> grows logarithmically in ℓ. Setting β = 0.01 and ρ = 0.9 gives the following checking limits.

| Certification attempt ℓ | Checks required with β = 0.01 and ρ = 0.9 |
|---:|---:|
| 1 | 51 |
| 10 | 89 |
| 100 | 132 |
| 1,000 | 175 |
| 10,000 | 219 |
{: style="border-spacing: 0.5rem 0.35rem; width: 100%;" }

A tenfold increase in the attempt index adds about 44 checks. If the first N attempts all use their full allowances, the total is <math><mi>O</mi><mrow><mo>(</mo><mi>N</mi><mi>log</mi><mrow><mo>(</mo><mi>N</mi><mo>)</mo></mrow><mo>)</mo></mrow></math>. Total runtime also depends on the time per LP solve and the number of candidates produced by branch-and-bound.

## 5. Allocating the error budget more evenly

Suppose there are exactly N attempts, all have the same ρ and checking cost, and every attempt runs to its limit without early stopping. Ignoring rounding, minimizing the total number of checks gives

<math display="block" aria-label="Equal-cost allocation problem before integer rounding"><mtable columnalign="left" displaystyle="true" rowspacing="0.45em"><mtr><mtd><munder><mrow><mi>min</mi></mrow><mrow><mrow><msub><mrow><mi>β</mi></mrow><mrow><mn>1</mn></mrow></msub><mo>,</mo><mo>…</mo><mo>,</mo><msub><mrow><mi>β</mi></mrow><mrow><mi>N</mi></mrow></msub><mo>&gt;</mo><mn>0</mn></mrow></mrow></munder><munderover><mo>∑</mo><mrow><mi>ℓ</mi><mo>=</mo><mn>1</mn></mrow><mrow><mi>N</mi></mrow></munderover><mfrac><mrow><mi>log</mi><mrow><mo>(</mo><mfrac><mrow><mn>1</mn></mrow><mrow><msub><mrow><mi>β</mi></mrow><mrow><mi>ℓ</mi></mrow></msub></mrow></mfrac><mo>)</mo></mrow></mrow><mrow><mi>log</mi><mrow><mo>(</mo><mfrac><mrow><mn>1</mn></mrow><mrow><mi>ρ</mi></mrow></mfrac><mo>)</mo></mrow></mrow></mfrac></mtd></mtr><mtr><mtd><munderover><mo>∑</mo><mrow><mi>ℓ</mi><mo>=</mo><mn>1</mn></mrow><mrow><mi>N</mi></mrow></munderover><msub><mrow><mi>β</mi></mrow><mrow><mi>ℓ</mi></mrow></msub><mo>≤</mo><mi>β</mi></mtd></mtr></mtable></math>

Convexity of the negative logarithm gives the optimal allocation <math><msub><mrow><mi>β</mi></mrow><mrow><mi>ℓ</mi></mrow></msub><mo>=</mo><mfrac><mrow><mi>β</mi></mrow><mrow><mi>N</mi></mrow></mfrac></math>. With N = 100, β = 0.01, and ρ = 0.9, equal allocation requires 88 checks each, or 8,800 in total. The earlier schedule requires 11,370 over its first 100 attempts, so equal allocation uses about 22.6% fewer checks in this comparison.

N must be an enforced limit. Expecting to finish after roughly 100 attempts, allocating the entire budget accordingly, and then certifying attempt 101 in the same way exceeds the budget. Further attempts require a reserve.

When the count is unknown, a possible alternative with a prespecified a ≥ 1 is

<math display="block" aria-label="A shifted telescoping allocation with a prespecified scale a"><mtable columnalign="left" displaystyle="true" rowspacing="0.45em"><mtr><mtd><msub><mrow><mi>β</mi></mrow><mrow><mi>ℓ</mi></mrow></msub><mo>=</mo><mfrac><mrow><mi>β</mi><mi>a</mi></mrow><mrow><mrow><mo>(</mo><mi>a</mi><mo>+</mo><mi>ℓ</mi><mo>−</mo><mn>1</mn><mo>)</mo></mrow><mrow><mo>(</mo><mi>a</mi><mo>+</mo><mi>ℓ</mi><mo>)</mo></mrow></mrow></mfrac></mtd></mtr><mtr><mtd><munderover><mo>∑</mo><mrow><mi>ℓ</mi><mo>=</mo><mn>1</mn></mrow><mrow><mo>∞</mo></mrow></munderover><msub><mrow><mi>β</mi></mrow><mrow><mi>ℓ</mi></mrow></msub><mo>=</mo><mi>β</mi><mo>,</mo><mi>a</mi><mo>≥</mo><mn>1</mn></mtd></mtr></mtable></math>

Its sum remains β, and a = 1 recovers the original schedule. When ℓ is much smaller than a, <math><msub><mrow><mi>β</mi></mrow><mrow><mi>ℓ</mi></mrow></msub><mo>≈</mo><mfrac><mrow><mi>β</mi></mrow><mrow><mi>a</mi></mrow></mfrac></math>, so early allocations are nearly uniform. A larger a reserves more budget for later attempts but permits less error initially, requiring more early checks. It can be costly when a run finishes quickly.

## 6. The checking limit versus actual checks

Once a violation is found, its cut can be added and certification stopped. For a fixed violating candidate, let T be the first detection time. Under the conditional miss bound,

<math display="block" aria-label="Early stopping bounds the expected checks for a violating candidate"><mtable columnalign="left" displaystyle="true" rowspacing="0.45em"><mtr><mtd><mi>𝔼</mi><mrow><mo>[</mo><mi>min</mi><mrow><mo>(</mo><mrow><mi>T</mi><mo>,</mo><msub><mrow><mi>K</mi></mrow><mrow><mi>ℓ</mi></mrow></msub></mrow><mo>)</mo></mrow><mo>]</mo></mrow><mo>=</mo><munderover><mo>∑</mo><mrow><mi>t</mi><mo>=</mo><mn>0</mn></mrow><mrow><msub><mrow><mi>K</mi></mrow><mrow><mi>ℓ</mi></mrow></msub><mo>−</mo><mn>1</mn></mrow></munderover><mi>Pr</mi><mrow><mo>(</mo><mi>T</mi><mo>&gt;</mo><mi>t</mi><mo>)</mo></mrow></mtd></mtr><mtr><mtd><mo>≤</mo><munderover><mo>∑</mo><mrow><mi>t</mi><mo>=</mo><mn>0</mn></mrow><mrow><msub><mrow><mi>K</mi></mrow><mrow><mi>ℓ</mi></mrow></msub><mo>−</mo><mn>1</mn></mrow></munderover><msup><mrow><mi>ρ</mi></mrow><mrow><mi>t</mi></mrow></msup><mo>≤</mo><mfrac><mrow><mn>1</mn></mrow><mrow><mn>1</mn><mo>−</mo><mi>ρ</mi></mrow></mfrac></mtd></mtr></mtable></math>

With ρ = 0.9, the expected number of checks is at most 10. This bound is unchanged whether the checking limit is 51 or 219. A candidate with no violation, however, has nothing to discover and must use its full checking allowance.

An allocation that minimizes runtime therefore also depends on which candidates are rejected quickly and which reach the end of certification. The arithmetic advantage of equal allocation need not transfer directly to actual runs.

The value of ρ has a particularly large effect. As ρ approaches one,

<math display="block" aria-label="Dependence on a miss bound close to one"><msub><mrow><mi>K</mi></mrow><mrow><mi>ℓ</mi></mrow></msub><mo>≈</mo><mfrac><mrow><mi>log</mi><mrow><mo>(</mo><mfrac><mrow><mn>1</mn></mrow><mrow><msub><mrow><mi>β</mi></mrow><mrow><mi>ℓ</mi></mrow></msub></mrow></mfrac><mo>)</mo></mrow></mrow><mrow><mn>1</mn><mo>−</mo><mi>ρ</mi></mrow></mfrac></math>

For <math><msub><mrow><mi>β</mi></mrow><mrow><mi>ℓ</mi></mrow></msub><mo>=</mo><msup><mrow><mn>10</mn></mrow><mrow><mrow><mo>−</mo><mn>4</mn></mrow></mrow></msup></math>, ρ = 0.9 requires 88 checks and ρ = 0.99 requires 917. Error-budget allocation should be examined together with the search's ability to discover rare violations.

## 7. Continuing a separate chain for each integer design

In continuous optimization, an analysis can let the chain track designs that move by small steps. Branch-and-bound candidates need not behave that way. A design that opens only facility A may be followed immediately by one that opens only B.

Split x into integer variables <math><msub><mrow><mi>x</mi></mrow><mrow><mi>z</mi></mrow></msub></math> and continuous variables <math><msub><mrow><mi>x</mi></mrow><mrow><mi>c</mi></mrow></msub></math>. Consider retaining, for each integer assignment, the last scenario, the last continuous design, and the number of oracle calls.

| Visit | Opening decisions (A, B) | Capacities (A, B) | Chain used |
|---:|---|---|---|
| 1 | (1, 0) | (50, 0) | Create the A-only chain |
| 2 | (0, 1) | (0, 70) | Create the B-only chain |
| 3 | (1, 0) | (52, 0) | Resume the A-only chain |
{: style="border-spacing: 0.5rem 0.35rem; width: 100%;" }

If the A-only chain ended its first visit at scenario 17, the third visit starts there. What is retained is the scenario index. Capacities have changed, so costs and acceptance probabilities must be evaluated at the new design.

Even with the same integer assignment, a capacity jump from 50 to 500 can make the old state poorly suited to the current design. One can use a single transition after a small continuous change and extra transitions at the fixed new design after a large change. [Xu and Jiang, Section 4.1](https://arxiv.org/html/2609.36275v1)

Although chain memory is maintained by assignment, the cuts derived earlier are valid over the entire design domain and can accumulate in a shared cut pool. Extra transitions help search for scenarios; failure to find a violation still requires certification.

## 8. Certified upper bounds and solver termination

The candidate-processing sequence is:

1. When branch-and-bound presents an integer-feasible candidate, select its assignment's chain and take transitions according to the design change.
2. If a violating scenario is found, add its valid Benders cut.
3. Otherwise, fix the candidate and certify it using its allocated error budget. Add a cut if a violation appears; accept the proposed upper bound if every check misses.
4. Use the difference between a certified upper bound and a valid global lower bound to decide when to stop.

Cost tolerance and error probability must be distinguished. If the certification target is relaxed to <math><msup><mrow><mi>Q</mi></mrow><mrow><mo>⋆</mo></mrow></msup><mrow><mo>(</mo><mover><mi>x</mi><mo>¯</mo></mover><mo>)</mo></mrow><mo>≤</mo><mover><mi>θ</mi><mo>¯</mo></mover><mo>+</mo><msub><mrow><mi>ε</mi></mrow><mrow><mtext>cert</mtext></mrow></msub></math>, the objective upper bound must be

<math display="block" aria-label="An upper bound must include the certification cost tolerance"><mi>U</mi><mo>=</mo><mi>f</mi><mrow><mo>(</mo><mover><mi>x</mi><mo>¯</mo></mover><mo>)</mo></mrow><mo>+</mo><mover><mi>θ</mi><mo>¯</mo></mover><mo>+</mo><msub><mrow><mi>ε</mi></mrow><mrow><mtext>cert</mtext></mrow></msub></math>

The tolerance <math><msub><mrow><mi>ε</mi></mrow><mrow><mtext>cert</mtext></mrow></msub></math> has cost units and must be added to the bound. The violation set must also be changed to scenarios exceeding the relaxed threshold, and ρ must be justified for missing that set. The dimensionless β is the budget for falsely certifying that condition.

If a valid global lower bound L and the certified candidate's U satisfy <math><mi>U</mi><mo>−</mo><mi>L</mi><mo>≤</mo><msub><mrow><mi>ε</mi></mrow><mrow><mtext>opt</mtext></mrow></msub></math>, then, on the event that every certificate used is correct,

<math display="block" aria-label="The objective gap on the event of correct certification"><mn>0</mn><mo>≤</mo><mi>F</mi><mrow><mo>(</mo><mover><mi>x</mi><mo>¯</mo></mover><mo>)</mo></mrow><mo>−</mo><msup><mrow><mi>F</mi></mrow><mrow><mo>⋆</mo></mrow></msup><mo>≤</mo><mi>U</mi><mo>−</mo><mi>L</mi><mo>≤</mo><msub><mrow><mi>ε</mi></mrow><mrow><mtext>opt</mtext></mrow></msub></math>

With the total error budget respected, that event has probability at least 1 − β. The guarantee depends on both the conditional certification bound and a valid lower bound. Implementation must account for cost tolerance in incumbent comparisons and pruning. Discarding promising nodes using uncertified sample values and adjusting the upper bound only at the end does not preserve this argument.

For practical certification, the paper describes using empirical quantiles from warm-start samples and reports ρ = 0.9 and <math><msub><mrow><mi>ε</mi></mrow><mrow><mtext>cert</mtext></mrow></msub><mo>=</mo><mn>100</mn></math> in its mixed-integer experiments. [Xu and Jiang, EC.9](https://arxiv.org/html/2609.36275v1)

That empirical choice does not automatically establish a conditional bound for every candidate and history without a detected violation. Estimates may be optimistic if the samples emphasize easy candidates or miss rare violations. Experiments comparing certification schedules should therefore check the final candidate against every scenario as well as report LP counts and runtime. This separates lower checking cost from the effect of incorrectly accepting candidates.

<!-- ko -->

많은 시나리오를 검사했는데 위반을 찾지 못했습니다. 이때 현재 설계를 받아들여도 될까요? 검사한 시나리오의 비용이 낮았다는 사실만으로는 부족합니다. 위반이 실제로 남아 있었다면, 지금 사용한 탐색 방법이 그것을 얼마나 쉽게 발견했을지를 알아야 합니다.

[앞선 mellowmax 글]({% post_url 2026-10-23-markov-stationary-distributions-optimization-bias %})에서는 Markov chain의 방문 비율과 표본 편향이 최적화 방향에 미치는 영향을 다뤘습니다. Soft separation은 이런 확률적 시나리오 탐색으로 위반을 찾는 방식입니다. 고정된 설계를 인증하려면 남아 있는 위반을 놓칠 확률의 상한이 필요합니다. 이 상한이 인증의 검사 비용과 혼합정수 Benders 방법에서의 역할을 결정합니다.

## 1. 표본 시나리오에서 얻는 유효한 cut

설계 x의 투자비를 f(x), 시나리오 i에서 최적으로 운영했을 때의 비용을 <math><msub><mrow><mi>Q</mi></mrow><mrow><mi>i</mi></mrow></msub></math>(x)라고 하겠습니다. 유한한 m개 시나리오를 고려하는 강건 최적화 문제는

<math display="block" aria-label="The finite-scenario robust objective"><mtable columnalign="left" displaystyle="true" rowspacing="0.45em"><mtr><mtd><msup><mrow><mi>F</mi></mrow><mrow><mo>⋆</mo></mrow></msup><mo>=</mo><munder><mrow><mi>min</mi></mrow><mrow><mi>x</mi><mo>∈</mo><mi>X</mi></mrow></munder><mi>F</mi><mrow><mo>(</mo><mi>x</mi><mo>)</mo></mrow></mtd></mtr><mtr><mtd><mi>F</mi><mrow><mo>(</mo><mi>x</mi><mo>)</mo></mrow><mo>:=</mo><mi>f</mi><mrow><mo>(</mo><mi>x</mi><mo>)</mo></mrow><mo>+</mo><msup><mrow><mi>Q</mi></mrow><mrow><mo>⋆</mo></mrow></msup><mrow><mo>(</mo><mi>x</mi><mo>)</mo></mrow></mtd></mtr><mtr><mtd><msup><mrow><mi>Q</mi></mrow><mrow><mo>⋆</mo></mrow></msup><mrow><mo>(</mo><mi>x</mi><mo>)</mo></mrow><mo>:=</mo><munder><mrow><mi>max</mi></mrow><mrow><mrow><mn>1</mn><mo>≤</mo><mi>i</mi><mo>≤</mo><mi>m</mi></mrow></mrow></munder><msub><mrow><mi>Q</mi></mrow><mrow><mi>i</mi></mrow></msub><mrow><mo>(</mo><mi>x</mi><mo>)</mo></mrow></mtd></mtr></mtable></math>

입니다. X에는 설비 건설 여부와 같은 정수변수도 포함될 수 있습니다. 보조변수 θ를 도입하면 각 시나리오에 대해 <math><mi>θ</mi><mo>≥</mo><msub><mrow><mi>Q</mi></mrow><mrow><mi>i</mi></mrow></msub><mrow><mo>(</mo><mi>x</mi><mo>)</mo></mrow></math>를 요구합니다. Master problem은 이 제약들을 일부 cut으로 근사하고, 후보 <math><mrow><mo>(</mo><mrow><mover><mi>x</mi><mo>¯</mo></mover><mo>,</mo><mover><mi>θ</mi><mo>¯</mo></mover></mrow><mo>)</mo></mrow></math>를 내놓습니다. Separation은 이 후보의 θ가 너무 작은지를 검사하는 절차입니다.

선형 recourse가 모든 고려 대상 설계와 시나리오에서 실행 가능하고 유한하며, 강한 쌍대성이 성립한다고 가정합시다. 설계에 의존하지 않는 쌍대 가능 영역 Π를 사용하면

<math display="block" aria-label="Linear recourse in dual form"><msub><mrow><mi>Q</mi></mrow><mrow><mi>i</mi></mrow></msub><mrow><mo>(</mo><mi>x</mi><mo>)</mo></mrow><mo>=</mo><munder><mrow><mi>max</mi></mrow><mrow><mi>π</mi><mo>∈</mo><mi>Π</mi></mrow></munder><msup><mrow><mi>π</mi></mrow><mrow><mtext>T</mtext></mrow></msup><mrow><mo>(</mo><mrow><mi>h</mi><mo>−</mo><mi>E</mi><mi>x</mi><mo>−</mo><mi>U</mi><msub><mrow><mi>ξ</mi></mrow><mrow><mi>i</mi></mrow></msub></mrow><mo>)</mo></mrow></math>

로 쓸 수 있습니다. 여기서 h는 우변 벡터, E와 U는 설계와 불확실성이 우변에 미치는 영향을 나타내는 행렬, <math><msub><mrow><mi>ξ</mi></mrow><mrow><mi>i</mi></mrow></msub></math>는 시나리오 데이터입니다. 현재 설계에서 시나리오 i를 풀어 얻은 최적 쌍대해 <math><msub><mrow><mover><mi>π</mi><mo>¯</mo></mover></mrow><mrow><mi>i</mi></mrow></msub></math>를 고정하면

<math display="block" aria-label="A dual feasible solution gives a global lower cut"><mtable columnalign="left" displaystyle="true" rowspacing="0.45em"><mtr><mtd><msub><mrow><mi>a</mi></mrow><mrow><mi>i</mi></mrow></msub><mrow><mo>(</mo><mi>x</mi><mo>)</mo></mrow><mo>:=</mo><msup><mrow><msub><mrow><mover><mi>π</mi><mo>¯</mo></mover></mrow><mrow><mi>i</mi></mrow></msub></mrow><mrow><mtext>T</mtext></mrow></msup><mrow><mo>(</mo><mrow><mi>h</mi><mo>−</mo><mi>E</mi><mi>x</mi><mo>−</mo><mi>U</mi><msub><mrow><mi>ξ</mi></mrow><mrow><mi>i</mi></mrow></msub></mrow><mo>)</mo></mrow></mtd></mtr><mtr><mtd><msub><mrow><mi>a</mi></mrow><mrow><mi>i</mi></mrow></msub><mrow><mo>(</mo><mi>x</mi><mo>)</mo></mrow><mo>≤</mo><msub><mrow><mi>Q</mi></mrow><mrow><mi>i</mi></mrow></msub><mrow><mo>(</mo><mi>x</mi><mo>)</mo></mrow><mo>≤</mo><mrow><munder><mrow><mi>max</mi></mrow><mrow><mi>j</mi></mrow></munder><msub><mrow><mi>Q</mi></mrow><mrow><mi>j</mi></mrow></msub><mrow><mo>(</mo><mi>x</mi><mo>)</mo></mrow></mrow></mtd></mtr></mtable></math>

이므로 <math><mi>θ</mi><mo>≥</mo><msub><mrow><mi>a</mi></mrow><mrow><mi>i</mi></mrow></msub><mrow><mo>(</mo><mi>x</mi><mo>)</mo></mrow></math>는 강건 문제에 유효한 Benders cut입니다. 시나리오 i가 최악일 필요는 없습니다. 예를 들어 현재 θ가 100이고 표본 시나리오의 비용이 120이라면, 실제 최대비용이 150이어도 비용 120의 시나리오만으로 현재 후보를 잘라낼 수 있습니다. 최적 쌍대해로 만든 cut은 현재점에서 비용 120과 정확히 일치하기 때문입니다.

쌍대 실행 가능성은 cut의 유효성을 주고, 현재점의 쌍대 최적성은 cut이 그 점에서 비용에 닿도록 합니다. 확률적 분석이 필요한 부분은 남아 있는 위반을 놓치는 사건입니다.

## 2. ρ가 제한하는 확률

후보 <math><mrow><mo>(</mo><mrow><mover><mi>x</mi><mo>¯</mo></mover><mo>,</mo><mover><mi>θ</mi><mo>¯</mo></mover></mrow><mo>)</mo></mrow></math>를 고정하고 위반 시나리오 집합을

<math display="block" aria-label="Violating scenarios at a fixed candidate"><mi>V</mi><mo>:=</mo><mo>{</mo><mi>i</mi><mo>:</mo><msub><mrow><mi>Q</mi></mrow><mrow><mi>i</mi></mrow></msub><mrow><mo>(</mo><mover><mi>x</mi><mo>¯</mo></mover><mo>)</mo></mrow><mo>&gt;</mo><mover><mi>θ</mi><mo>¯</mo></mover><mo>}</mo></math>

로 정의하겠습니다. 우선 허용오차 없이 검사하며, 한 번의 검사는 시나리오 하나를 선택해 그 비용을 정확히 평가하는 것으로 셉니다.

V가 비어 있지 않다고 합시다. 인증 시작 전의 최적화 이력과 지금까지의 모든 검사 결과를 <math><msub><mrow><mi>ℋ</mi></mrow><mrow><mi>t</mi></mrow></msub></math>에 포함시킵니다. 아직 위반을 찾지 못한 모든 가능한 이력에서

<math display="block" aria-label="A conditional miss bound on every history without a detection"><mi>Pr</mi><mrow><mo>(</mo><msub><mrow><mi>I</mi></mrow><mrow><mrow><mi>t</mi><mo>+</mo><mn>1</mn></mrow></mrow></msub><mo>∉</mo><mi>V</mi><mo>∣</mo><msub><mrow><mi>ℋ</mi></mrow><mrow><mi>t</mi></mrow></msub><mo>)</mo></mrow><mo>≤</mo><mi>ρ</mi><mo>&lt;</mo><mn>1</mn></math>

이 성립해야 합니다. ρ = 0.9라면 다음 검사에서도 놓칠 확률은 최대 90%, 발견할 확률은 최소 10%라는 뜻입니다. 실제 놓침 확률이 항상 90%라는 뜻은 아닙니다.

이 조건부 상한을 반복해서 적용하면, 위반이 있는 고정 후보에서

<math display="block" aria-label="Probability of K consecutive misses for a violating candidate"><mi>Pr</mi><mrow><mo>(</mo><munder><mrow><mo>⋂</mo></mrow><mrow><mrow><mi>t</mi><mo>=</mo><mn>1</mn><mo>,</mo><mo>…</mo><mo>,</mo><mi>K</mi></mrow></mrow></munder><mo>{</mo><msub><mrow><mi>I</mi></mrow><mrow><mi>t</mi></mrow></msub><mo>∉</mo><mi>V</mi><mo>}</mo><mo>∣</mo><msub><mrow><mi>ℋ</mi></mrow><mrow><mn>0</mn></mrow></msub><mo>)</mo></mrow><mo>≤</mo><msup><mrow><mi>ρ</mi></mrow><mrow><mi>K</mi></mrow></msup></math>

를 얻습니다. 검사들이 독립일 필요는 없습니다. 대신 이전에 무엇을 관찰했든 조건부 상한이 유지되어야 합니다. 전체 실행에서 평균적으로 90%를 놓쳤다는 관찰만으로 이 조건을 대신할 수는 없습니다.

0 < ρ < 1에서 한 후보를 잘못 인증할 확률의 허용치를 0과 1 사이의 <math><msub><mrow><mi>β</mi></mrow><mrow><mi>ℓ</mi></mrow></msub></math>로 정하면

<math display="block" aria-label="Checks required for a per-attempt error allowance"><msub><mrow><mi>K</mi></mrow><mrow><mi>ℓ</mi></mrow></msub><mo>=</mo><mrow><mo>⌈</mo><mfrac><mrow><mi>log</mi><mrow><mo>(</mo><mfrac><mrow><mn>1</mn></mrow><mrow><msub><mrow><mi>β</mi></mrow><mrow><mi>ℓ</mi></mrow></msub></mrow></mfrac><mo>)</mo></mrow></mrow><mrow><mi>log</mi><mrow><mo>(</mo><mfrac><mrow><mn>1</mn></mrow><mrow><mi>ρ</mi></mrow></mfrac><mo>)</mo></mrow></mrow></mfrac><mo>⌉</mo></mrow></math>

번 연속 위반을 발견하지 못했을 때 인증을 끝낼 수 있습니다. <math><msub><mrow><mi>β</mi></mrow><mrow><mi>ℓ</mi></mrow></msub></math>는 정하는 목표이고, ρ는 탐색 방법에 대해 입증해야 하는 상한입니다. 이 허용치는 위반이 있는 후보를 승인하는 절차의 오류확률을 제한합니다.

## 3. 정상분포와 위반 집합에 도달할 확률

고정 설계에서 Markov chain의 전이행렬을 P라고 합시다. 현재 시나리오 i가 V 밖에 있다면 다음 검사에서 위반을 놓칠 확률은

<math display="block" aria-label="The miss probability is one minus the transition probability into V"><mtable columnalign="left" displaystyle="true" rowspacing="0.45em"><mtr><mtd><mi>Pr</mi><mrow><mo>(</mo><msub><mrow><mi>I</mi></mrow><mrow><mrow><mi>t</mi><mo>+</mo><mn>1</mn></mrow></mrow></msub><mo>∉</mo><mi>V</mi><mo>∣</mo><msub><mrow><mi>I</mi></mrow><mrow><mi>t</mi></mrow></msub><mo>=</mo><mi>i</mi><mo>)</mo></mrow></mtd></mtr><mtr><mtd><mo>=</mo><mn>1</mn><mo>−</mo><munder><mrow><mo>∑</mo></mrow><mrow><mi>j</mi><mo>∈</mo><mi>V</mi></mrow></munder><mi>P</mi><mrow><mo>(</mo><mrow><mi>i</mi><mo>,</mo><mi>j</mi></mrow><mo>)</mo></mrow></mtd></mtr></mtable></math>

입니다. 따라서 ρ = 0.9를 쓰려면, 도달 가능한 모든 미발견 상태에서 V로 이동할 확률이 적어도 0.1이어야 합니다. 한 번에 V에 도달할 수 없는 상태가 있으면 한 전이에 대한 이런 상한은 성립하지 않습니다. 여러 전이를 한 검사 단위로 묶을 수도 있지만, 그 단위에 맞춰 상한과 비용을 다시 계산해야 합니다.

시나리오가 100개이고, 매번 전체 집합에서 균등하게 독립 제안하는 표준 Metropolis-Hastings를 생각해 봅시다. 목표분포는 <math><msub><mrow><mi>p</mi></mrow><mrow><mi>x</mi></mrow></msub><mrow><mo>(</mo><mi>i</mi><mo>)</mo></mrow><mo>∝</mo><mi>exp</mi><mrow><mo>(</mo><mfrac><mrow><msub><mrow><mi>Q</mi></mrow><mrow><mi>i</mi></mrow></msub><mrow><mo>(</mo><mi>x</mi><mo>)</mo></mrow></mrow><mrow><mi>w</mi></mrow></mfrac><mo>)</mo></mrow></math>이며 w > 0입니다. 현재 시나리오는 위반이 아니고 제안 시나리오는 위반이라면, 제안된 비용이 더 높으므로 수락확률은 1입니다.

| 위반 시나리오 수 | 한 번에 발견할 확률 | 한 번에 놓칠 확률 |
|---:|---:|---:|
| 50개 | 0.50 | 0.50 |
| 10개 | 0.10 | 0.90 |
| 1개 | 0.01 | 0.99 |
{: style="border-spacing: 0.5rem 0.35rem; width: 100%;" }

위반이 하나뿐인 마지막 경우에 ρ = 0.9를 적용하면 인증 오류를 과소평가합니다. 온도를 낮춰 그 시나리오의 정상확률을 높여도 균등 제안이 그 시나리오를 처음 뽑을 확률은 그대로입니다. 정상분포에서 많이 방문하는 것과, 현재 위치에서 빨리 발견하는 것은 구별해야 합니다.

수치 차이도 큽니다. <math><msup><mrow><mn>0.9</mn></mrow><mrow><mn>50</mn></mrow></msup></math>는 약 0.00515이지만 <math><msup><mrow><mn>0.99</mn></mrow><mrow><mn>50</mn></mrow></msup></math>는 약 0.605입니다. 같은 50번의 검사라도 유효한 놓침 상한이 0.9인지 0.99인지에 따라 연속 미발견 확률의 상계가 크게 달라집니다.

## 4. 뒤의 후보일수록 검사량이 폭증할까

최적화 중 인증을 몇 번 시도할지는 미리 알기 어렵습니다. 각 인증의 오류 허용치를 계속 같은 값으로 두면 전체 실행에서 한 번이라도 잘못 인증할 확률을 통제하기 어렵습니다. 전체 오류 예산 β를 실제 인증 시도 순서 ℓ에 따라

<math display="block" aria-label="A summable error budget across certification attempts"><mtable columnalign="left" displaystyle="true" rowspacing="0.45em"><mtr><mtd><msub><mrow><mi>β</mi></mrow><mrow><mi>ℓ</mi></mrow></msub><mo>=</mo><mfrac><mrow><mi>β</mi></mrow><mrow><mi>ℓ</mi><mrow><mo>(</mo><mrow><mi>ℓ</mi><mo>+</mo><mn>1</mn></mrow><mo>)</mo></mrow></mrow></mfrac><mo>,</mo><mi>ℓ</mi><mo>=</mo><mn>1</mn><mo>,</mo><mn>2</mn><mo>,</mo><mo>…</mo></mtd></mtr><mtr><mtd><munderover><mo>∑</mo><mrow><mi>ℓ</mi><mo>=</mo><mn>1</mn></mrow><mrow><mo>∞</mo></mrow></munderover><msub><mrow><mi>β</mi></mrow><mrow><mi>ℓ</mi></mrow></msub><mo>=</mo><mi>β</mi></mtd></mtr></mtable></math>

로 나누는 방법을 생각할 수 있습니다. 이 배분은 망원급수로 합이 β가 됩니다. 각 인증이 시작되기 전 이력에 조건부로도 오류확률이 <math><msub><mrow><mi>β</mi></mrow><mrow><mi>ℓ</mi></mrow></msub></math> 이하라면, 인증들이 서로 의존하더라도 합집합 부등식으로 전체 오류확률을 β 이하로 제한합니다. [Xu와 Jiang, 4.2절](https://arxiv.org/html/2609.36275v1)

검사 횟수에 이 배분을 대입하면

<math display="block" aria-label="Logarithmic growth in the attempt index for fixed beta and rho"><msub><mrow><mi>K</mi></mrow><mrow><mi>ℓ</mi></mrow></msub><mo>=</mo><mrow><mo>⌈</mo><mfrac><mrow><mi>log</mi><mrow><mo>(</mo><mfrac><mrow><mn>1</mn></mrow><mrow><mi>β</mi></mrow></mfrac><mo>)</mo></mrow><mo>+</mo><mi>log</mi><mrow><mo>(</mo><mi>ℓ</mi><mo>)</mo></mrow><mo>+</mo><mi>log</mi><mrow><mo>(</mo><mrow><mi>ℓ</mi><mo>+</mo><mn>1</mn></mrow><mo>)</mo></mrow></mrow><mrow><mi>log</mi><mrow><mo>(</mo><mfrac><mrow><mn>1</mn></mrow><mrow><mi>ρ</mi></mrow></mfrac><mo>)</mo></mrow></mrow></mfrac><mo>⌉</mo></mrow></math>

입니다. β와 ρ를 고정하면 <math><msub><mrow><mi>K</mi></mrow><mrow><mi>ℓ</mi></mrow></msub></math>은 ℓ에 대해 로그 수준으로 늘어납니다. β = 0.01, ρ = 0.9로 두고 검사 횟수를 계산하면 다음과 같습니다.

| 인증 순서 ℓ | β = 0.01, ρ = 0.9에서 필요한 검사 횟수 |
|---:|---:|
| 1 | 51 |
| 10 | 89 |
| 100 | 132 |
| 1,000 | 175 |
| 10,000 | 219 |
{: style="border-spacing: 0.5rem 0.35rem; width: 100%;" }

후보 번호가 열 배가 될 때 약 44회가 더 필요합니다. 첫 N회가 모두 끝까지 검사한다면 총량은 <math><mi>O</mi><mrow><mo>(</mo><mi>N</mi><mi>log</mi><mrow><mo>(</mo><mi>N</mi><mo>)</mo></mrow><mo>)</mo></mrow></math>입니다. 실제 총시간은 LP 한 번의 풀이 시간과 branch-and-bound가 만드는 후보 수에도 달려 있습니다.

## 5. 오류 예산을 더 고르게 배분하는 경우

인증을 정확히 N번 수행하고, 모든 인증의 ρ와 검사 비용이 같으며, 조기 종료 없이 정해진 검사를 모두 한다고 가정합시다. 올림을 제외한 총 검사량을 최소화하는 문제는

<math display="block" aria-label="Equal-cost allocation problem before integer rounding"><mtable columnalign="left" displaystyle="true" rowspacing="0.45em"><mtr><mtd><munder><mrow><mi>min</mi></mrow><mrow><mrow><msub><mrow><mi>β</mi></mrow><mrow><mn>1</mn></mrow></msub><mo>,</mo><mo>…</mo><mo>,</mo><msub><mrow><mi>β</mi></mrow><mrow><mi>N</mi></mrow></msub><mo>&gt;</mo><mn>0</mn></mrow></mrow></munder><munderover><mo>∑</mo><mrow><mi>ℓ</mi><mo>=</mo><mn>1</mn></mrow><mrow><mi>N</mi></mrow></munderover><mfrac><mrow><mi>log</mi><mrow><mo>(</mo><mfrac><mrow><mn>1</mn></mrow><mrow><msub><mrow><mi>β</mi></mrow><mrow><mi>ℓ</mi></mrow></msub></mrow></mfrac><mo>)</mo></mrow></mrow><mrow><mi>log</mi><mrow><mo>(</mo><mfrac><mrow><mn>1</mn></mrow><mrow><mi>ρ</mi></mrow></mfrac><mo>)</mo></mrow></mrow></mfrac></mtd></mtr><mtr><mtd><munderover><mo>∑</mo><mrow><mi>ℓ</mi><mo>=</mo><mn>1</mn></mrow><mrow><mi>N</mi></mrow></munderover><msub><mrow><mi>β</mi></mrow><mrow><mi>ℓ</mi></mrow></msub><mo>≤</mo><mi>β</mi></mtd></mtr></mtable></math>

입니다. 음의 로그함수의 볼록성으로 최적 배분은 <math><msub><mrow><mi>β</mi></mrow><mrow><mi>ℓ</mi></mrow></msub><mo>=</mo><mfrac><mrow><mi>β</mi></mrow><mrow><mi>N</mi></mrow></mfrac></math>입니다. N = 100, β = 0.01, ρ = 0.9라면 균등 배분은 매번 88회, 총 8,800회입니다. 앞의 배분은 첫 100회에 총 11,370회이므로 이 비교에서 균등 배분이 약 22.6% 적습니다.

N은 실제로 지키는 횟수 상한이어야 합니다. 100번쯤 끝날 것으로 예상하고 예산을 전부 나눈 뒤 101번째를 같은 방식으로 인증하면 전체 예산을 넘습니다. 계속할 가능성이 있다면 뒤에 쓸 예산을 남겨야 합니다.

횟수를 모를 때 쓸 대안으로, 미리 정한 a ≥ 1에 대해

<math display="block" aria-label="A shifted telescoping allocation with a prespecified scale a"><mtable columnalign="left" displaystyle="true" rowspacing="0.45em"><mtr><mtd><msub><mrow><mi>β</mi></mrow><mrow><mi>ℓ</mi></mrow></msub><mo>=</mo><mfrac><mrow><mi>β</mi><mi>a</mi></mrow><mrow><mrow><mo>(</mo><mi>a</mi><mo>+</mo><mi>ℓ</mi><mo>−</mo><mn>1</mn><mo>)</mo></mrow><mrow><mo>(</mo><mi>a</mi><mo>+</mo><mi>ℓ</mi><mo>)</mo></mrow></mrow></mfrac></mtd></mtr><mtr><mtd><munderover><mo>∑</mo><mrow><mi>ℓ</mi><mo>=</mo><mn>1</mn></mrow><mrow><mo>∞</mo></mrow></munderover><msub><mrow><mi>β</mi></mrow><mrow><mi>ℓ</mi></mrow></msub><mo>=</mo><mi>β</mi><mo>,</mo><mi>a</mi><mo>≥</mo><mn>1</mn></mtd></mtr></mtable></math>

를 고려할 수 있습니다. 합은 여전히 β이며 a = 1이면 앞의 배분과 같습니다. ℓ이 a보다 훨씬 작을 때는 <math><msub><mrow><mi>β</mi></mrow><mrow><mi>ℓ</mi></mrow></msub><mo>≈</mo><mfrac><mrow><mi>β</mi></mrow><mrow><mi>a</mi></mrow></mfrac></math>라서 초기 배분이 거의 균등합니다. a를 크게 잡으면 뒤의 인증에 예산을 더 남기는 대신, 초기에 허용하는 오류가 작아져 검사가 늘어납니다. 일찍 끝나는 실행에는 손해일 수 있습니다.

## 6. 검사 상한과 실제 검사 횟수

위반을 발견하면 그 즉시 cut을 추가하고 인증을 멈출 수 있습니다. 위반이 있는 고정 후보에서 최초 발견 시점을 T라고 하면, 앞의 조건부 상한 아래에서

<math display="block" aria-label="Early stopping bounds the expected checks for a violating candidate"><mtable columnalign="left" displaystyle="true" rowspacing="0.45em"><mtr><mtd><mi>𝔼</mi><mrow><mo>[</mo><mi>min</mi><mrow><mo>(</mo><mrow><mi>T</mi><mo>,</mo><msub><mrow><mi>K</mi></mrow><mrow><mi>ℓ</mi></mrow></msub></mrow><mo>)</mo></mrow><mo>]</mo></mrow><mo>=</mo><munderover><mo>∑</mo><mrow><mi>t</mi><mo>=</mo><mn>0</mn></mrow><mrow><msub><mrow><mi>K</mi></mrow><mrow><mi>ℓ</mi></mrow></msub><mo>−</mo><mn>1</mn></mrow></munderover><mi>Pr</mi><mrow><mo>(</mo><mi>T</mi><mo>&gt;</mo><mi>t</mi><mo>)</mo></mrow></mtd></mtr><mtr><mtd><mo>≤</mo><munderover><mo>∑</mo><mrow><mi>t</mi><mo>=</mo><mn>0</mn></mrow><mrow><msub><mrow><mi>K</mi></mrow><mrow><mi>ℓ</mi></mrow></msub><mo>−</mo><mn>1</mn></mrow></munderover><msup><mrow><mi>ρ</mi></mrow><mrow><mi>t</mi></mrow></msup><mo>≤</mo><mfrac><mrow><mn>1</mn></mrow><mrow><mn>1</mn><mo>−</mo><mi>ρ</mi></mrow></mfrac></mtd></mtr></mtable></math>

입니다. ρ = 0.9라면 기대 검사 횟수는 10회 이하입니다. 검사 상한이 51회인지 219회인지는 이 상한을 바꾸지 않습니다. 반면 위반이 전혀 없는 후보는 발견할 위반이 없으므로 정해진 검사를 끝까지 해야 합니다.

그래서 총시간을 줄이는 배분은 어떤 후보가 빨리 탈락하고 어떤 후보가 끝까지 인증되는지에도 영향을 받습니다. 균등 배분의 계산상 이점이 실제 실행에서도 그대로 나타난다고 단정할 수는 없습니다.

검사량에는 ρ가 특히 크게 작용합니다. ρ가 1에 가까우면

<math display="block" aria-label="Dependence on a miss bound close to one"><msub><mrow><mi>K</mi></mrow><mrow><mi>ℓ</mi></mrow></msub><mo>≈</mo><mfrac><mrow><mi>log</mi><mrow><mo>(</mo><mfrac><mrow><mn>1</mn></mrow><mrow><msub><mrow><mi>β</mi></mrow><mrow><mi>ℓ</mi></mrow></msub></mrow></mfrac><mo>)</mo></mrow></mrow><mrow><mn>1</mn><mo>−</mo><mi>ρ</mi></mrow></mfrac></math>

입니다. <math><msub><mrow><mi>β</mi></mrow><mrow><mi>ℓ</mi></mrow></msub><mo>=</mo><msup><mrow><mn>10</mn></mrow><mrow><mrow><mo>−</mo><mn>4</mn></mrow></mrow></msup></math>에서 ρ = 0.9이면 88회, ρ = 0.99이면 917회가 필요합니다. 오류 예산을 어떻게 나눌지와 함께, 드문 위반을 탐색기가 얼마나 잘 발견하는지도 살펴야 합니다.

## 7. 정수 설계별로 이어 쓰는 Markov chain

연속 최적화에서는 작은 보폭으로 움직이는 설계를 chain이 따라가도록 분석할 수 있습니다. Branch-and-bound가 제시하는 후보는 그렇게 움직이지 않습니다. 공장 A만 짓는 설계에서 B만 짓는 설계로 바로 넘어갈 수 있습니다.

정수 부분 <math><msub><mrow><mi>x</mi></mrow><mrow><mi>z</mi></mrow></msub></math>와 연속 부분 <math><msub><mrow><mi>x</mi></mrow><mrow><mi>c</mi></mrow></msub></math>로 설계를 나누고, 정수 배정마다 chain의 마지막 시나리오, 마지막 연속 설계, 호출 횟수를 저장하는 방식을 생각합시다.

| 방문 순서 | 건설 여부 (A, B) | 용량 (A, B) | 사용하는 chain |
|---:|---|---|---|
| 1 | (1, 0) | (50, 0) | A 전용 chain 생성 |
| 2 | (0, 1) | (0, 70) | B 전용 chain 생성 |
| 3 | (1, 0) | (52, 0) | A 전용 chain 재개 |
{: style="border-spacing: 0.5rem 0.35rem; width: 100%;" }

첫 방문의 A 전용 chain이 시나리오 17에서 끝났다면 세 번째 방문은 그 시나리오부터 이어갑니다. 기억하는 것은 시나리오 번호입니다. 용량이 바뀌었으므로 비용과 수락확률은 새 설계에서 다시 계산해야 합니다.

같은 정수 배정이어도 용량이 50에서 500으로 뛰면 이전 chain의 상태가 현재 설계에 잘 맞지 않을 수 있습니다. 연속 설계 변화가 작으면 한 번 전이하고, 크면 새 설계를 고정한 채 추가 전이를 수행하는 방식이 가능합니다. [Xu와 Jiang, 4.1절](https://arxiv.org/html/2609.36275v1)

Chain의 기억은 배정별로 관리해도, 앞서 유도한 cut은 전체 설계 영역에 유효하므로 공통 cut pool에 누적할 수 있습니다. 추가 전이는 시나리오를 찾는 데 쓰이고, 찾지 못했을 때의 판단에는 여전히 인증이 필요합니다.

## 8. 인증된 상한과 solver의 종료 조건

후보를 검토하는 흐름은 다음과 같이 연결됩니다.

1. Branch-and-bound가 정수 실행 가능 후보를 제시하면 해당 배정의 chain을 선택하고, 설계 변화에 맞춰 전이합니다.
2. 위반 시나리오를 찾으면 유효한 Benders cut을 추가합니다.
3. 위반을 못 찾으면 후보를 고정하고 배정된 오류 예산에 맞춰 인증합니다. 중간에 위반을 찾으면 cut을 추가하고, 끝까지 못 찾으면 상한 후보를 받아들입니다.
4. 인증된 상한과 유효한 전역 하한의 차이로 종료를 판단합니다.

여기서 비용 허용오차와 오류확률은 구분해야 합니다. 인증이 보장하려는 조건을 <math><msup><mrow><mi>Q</mi></mrow><mrow><mo>⋆</mo></mrow></msup><mrow><mo>(</mo><mover><mi>x</mi><mo>¯</mo></mover><mo>)</mo></mrow><mo>≤</mo><mover><mi>θ</mi><mo>¯</mo></mover><mo>+</mo><msub><mrow><mi>ε</mi></mrow><mrow><mtext>cert</mtext></mrow></msub></math>로 완화했다면, 사용해야 할 목적함수 상한은

<math display="block" aria-label="An upper bound must include the certification cost tolerance"><mi>U</mi><mo>=</mo><mi>f</mi><mrow><mo>(</mo><mover><mi>x</mi><mo>¯</mo></mover><mo>)</mo></mrow><mo>+</mo><mover><mi>θ</mi><mo>¯</mo></mover><mo>+</mo><msub><mrow><mi>ε</mi></mrow><mrow><mtext>cert</mtext></mrow></msub></math>

입니다. 비용 단위의 <math><msub><mrow><mi>ε</mi></mrow><mrow><mtext>cert</mtext></mrow></msub></math>를 상한에 더해야 합니다. 위반 집합도 완화된 기준을 넘는 시나리오들로 바꾸고, 그 집합을 놓칠 확률에 대해 ρ를 다시 정당화해야 합니다. β는 이 조건을 잘못 인증할 확률의 예산이며 단위가 없습니다.

유효한 전역 하한 L과 인증된 후보의 U가 <math><mi>U</mi><mo>−</mo><mi>L</mi><mo>≤</mo><msub><mrow><mi>ε</mi></mrow><mrow><mtext>opt</mtext></mrow></msub></math>를 만족하면, 모든 사용한 인증이 올바른 사건에서

<math display="block" aria-label="The objective gap on the event of correct certification"><mn>0</mn><mo>≤</mo><mi>F</mi><mrow><mo>(</mo><mover><mi>x</mi><mo>¯</mo></mover><mo>)</mo></mrow><mo>−</mo><msup><mrow><mi>F</mi></mrow><mrow><mo>⋆</mo></mrow></msup><mo>≤</mo><mi>U</mi><mo>−</mo><mi>L</mi><mo>≤</mo><msub><mrow><mi>ε</mi></mrow><mrow><mtext>opt</mtext></mrow></msub></math>

가 성립합니다. 전체 오류 예산을 지켰다면 그 사건의 확률은 적어도 1 − β입니다. 이 보장은 인증의 조건부 확률 상한과 하한의 유효성에 달려 있습니다. 구현에서는 비용 허용오차를 반영한 상한으로 incumbent 비교와 가지치기를 해야 하며, 미인증 표본값으로 유망한 노드를 버린 뒤 마지막에만 상한을 고쳐서는 이 논리를 유지할 수 없습니다.

논문은 실용적 인증에서 warm-start 표본의 경험적 분위수를 활용하는 방법을 설명하고, 혼합정수 실험에 ρ = 0.9와 <math><msub><mrow><mi>ε</mi></mrow><mrow><mtext>cert</mtext></mrow></msub><mo>=</mo><mn>100</mn></math>을 사용했다고 보고합니다. [Xu와 Jiang, EC.9](https://arxiv.org/html/2609.36275v1)

그 경험적 설정이 모든 후보와 미발견 이력에 대한 조건부 상한을 자동으로 입증하지는 않습니다. 표본이 쉬운 후보에 치우쳤거나 드문 위반을 놓쳤다면, 경험적 추정도 낙관적일 수 있습니다. 인증 배분을 비교하는 실험에서는 총 LP 풀이 수와 실행시간뿐 아니라 최종 후보의 전 시나리오 재검사 결과도 함께 확인해야 합니다. 그래야 검사 비용을 줄인 효과와 잘못 승인한 효과를 구별할 수 있습니다.
