---
layout: post
title: "Why Stationary Distributions Matter in Markov-Chain Optimization"
title_ko: "Markov chain 최적화에서 정상분포가 중요한 이유"
date: 2026-10-23
category: stochastic-nonlinear-optimization
category_label: "Mathematical Optimization"
research_group: algorithmic_reviews
research_category: stochastic-nonlinear-optimization
research_category_label: "Mathematical Optimization"
application_category: ""
application_category_label: ""
method_category: "stochastic-nonlinear-optimization"
method_category_label: "Mathematical Optimization"
paper_title: ""
authors: ""
venue: ""
year: ""
doi: ""
arxiv: ""
source_url: ""
tags:
  - "Markov chains"
  - "stationary distribution"
  - "mellowmax"
  - "stochastic approximation"
  - "convex optimization"
  - "Markovian noise"
excerpt: "How scenario visit frequencies determine the optimization direction, why one-step Markov samples are biased, and which cumulative-error bound yields convergence."
excerpt_ko: "시나리오 방문 비율이 최적화 방향을 결정하는 이유를 살펴보고, 한 번의 Markov 전이로 생기는 편향과 수렴에 필요한 누적 오차 상계를 유도합니다."
language: "en-ko"
has_korean_note: false
---

When a Markov chain selects scenarios for optimization, its stationary distribution determines the average direction being computed. To give high-cost scenarios more weight, one can design the chain to visit them more often. Having the desired stationary distribution does not, by itself, guarantee that a short run produces that average. If the design changes at every iteration, the accumulated effect of sampling bias also needs analysis.

## 1. Scenario visit frequencies become gradient weights

Suppose a design <math><mi>x</mi></math> determines an investment cost f(x) and scenario operating costs <math><msub><mrow><mi>Q</mi></mrow><mrow><mi>i</mi></mrow></msub></math>(x). There are m scenarios. To emphasize expensive scenarios, use the mellowmax objective at a fixed temperature w > 0:

<math display="block" aria-label="The mellowmax objective at a fixed temperature"><mtable columnalign="left"><mtr><mtd><msub><mrow><mi>F</mi></mrow><mrow><mi>w</mi></mrow></msub><mrow><mo>(</mo><mi>x</mi><mo>)</mo></mrow><mo>=</mo><mi>f</mi><mrow><mo>(</mo><mi>x</mi><mo>)</mo></mrow><mo>+</mo><msub><mrow><mi>M</mi></mrow><mrow><mi>w</mi></mrow></msub><mrow><mo>(</mo><mi>x</mi><mo>)</mo></mrow></mtd></mtr><mtr><mtd><msub><mrow><mi>M</mi></mrow><mrow><mi>w</mi></mrow></msub><mrow><mo>(</mo><mi>x</mi><mo>)</mo></mrow><mo>=</mo><mi>w</mi><mi>log</mi><mrow><mo>(</mo><mfrac><mrow><mn>1</mn></mrow><mrow><mi>m</mi></mrow></mfrac><munderover><mo>∑</mo><mrow><mi>i</mi><mo>=</mo><mn>1</mn></mrow><mi>m</mi></munderover><mi>exp</mi><mrow><mo>(</mo><mfrac><mrow><msub><mrow><mi>Q</mi></mrow><mrow><mi>i</mi></mrow></msub><mrow><mo>(</mo><mi>x</mi><mo>)</mo></mrow></mrow><mrow><mi>w</mi></mrow></mfrac><mo>)</mo></mrow><mo>)</mo></mrow></mtd></mtr></mtable></math>

Here w is the temperature that divides cost; some references instead use an inverse-temperature convention. Assume the feasible design set <math><mi>X</mi></math> is nonempty, closed, and convex, and that f and each <math><msub><mrow><mi>Q</mi></mrow><mrow><mi>i</mi></mrow></msub></math> are finite convex functions on a neighborhood of <math><mi>X</mi></math>, with the subgradients used below well defined. Mellowmax approximates the maximum scenario cost. The optimization problem considered here keeps w fixed.

Let <math><msub><mrow><mi>g</mi></mrow><mrow><mi>f</mi></mrow></msub></math>(x) and <math><msub><mrow><mi>g</mi></mrow><mrow><mi>i</mi></mrow></msub></math>(x) be subgradients of investment and operating cost. Then

<math display="block" aria-label="Scenario weights and a subgradient of the objective"><mtable columnalign="left"><mtr><mtd><msub><mrow><mi>p</mi></mrow><mrow><mi>x</mi></mrow></msub><mrow><mo>(</mo><mi>i</mi><mo>)</mo></mrow><mo>=</mo><mfrac><mrow><mi>exp</mi><mrow><mo>(</mo><mfrac><mrow><msub><mrow><mi>Q</mi></mrow><mrow><mi>i</mi></mrow></msub><mrow><mo>(</mo><mi>x</mi><mo>)</mo></mrow></mrow><mrow><mi>w</mi></mrow></mfrac><mo>)</mo></mrow></mrow><mrow><munder><mo>∑</mo><mi>j</mi></munder><mi>exp</mi><mrow><mo>(</mo><mfrac><mrow><msub><mrow><mi>Q</mi></mrow><mrow><mi>j</mi></mrow></msub><mrow><mo>(</mo><mi>x</mi><mo>)</mo></mrow></mrow><mrow><mi>w</mi></mrow></mfrac><mo>)</mo></mrow></mrow></mfrac></mtd></mtr><mtr><mtd><msub><mrow><mi>g</mi></mrow><mrow><mi>w</mi></mrow></msub><mrow><mo>(</mo><mi>x</mi><mo>)</mo></mrow><mo>=</mo><msub><mrow><mi>g</mi></mrow><mrow><mi>f</mi></mrow></msub><mrow><mo>(</mo><mi>x</mi><mo>)</mo></mrow><mo>+</mo><munder><mo>∑</mo><mi>i</mi></munder><msub><mrow><mi>p</mi></mrow><mrow><mi>x</mi></mrow></msub><mrow><mo>(</mo><mi>i</mi><mo>)</mo></mrow><msub><mrow><mi>g</mi></mrow><mrow><mi>i</mi></mrow></msub><mrow><mo>(</mo><mi>x</mi><mo>)</mo></mrow><mo>∈</mo><mo>∂</mo><msub><mrow><mi>F</mi></mrow><mrow><mi>w</mi></mrow></msub><mrow><mo>(</mo><mi>x</mi><mo>)</mo></mrow></mtd></mtr></mtable></math>

Evaluating every scenario may be expensive, which motivates using only the subgradient of a visited scenario. The frequency of those visits then determines the average direction.

Consider two scenarios at the current design. In this example, x is scalar and the investment-cost gradient is omitted.

| Scenario | Operating cost | Gradient with respect to design |
|---|---:|---:|
| 1 | 30 | −10 |
| 2 | 10 | +10 |

With w = 10, the desired weights and average direction are

<math display="block" aria-label="Softmax weights for the two-scenario example"><mtable columnalign="left"><mtr><mtd><msub><mrow><mi>p</mi></mrow><mrow><mi>x</mi></mrow></msub><mrow><mo>(</mo><mn>1</mn><mo>)</mo></mrow><mo>=</mo><mfrac><mrow><mi>exp</mi><mrow><mo>(</mo><mn>3</mn><mo>)</mo></mrow></mrow><mrow><mrow><mi>exp</mi><mrow><mo>(</mo><mn>3</mn><mo>)</mo></mrow><mo>+</mo><mi>exp</mi><mrow><mo>(</mo><mn>1</mn><mo>)</mo></mrow></mrow></mrow></mfrac><mo>≈</mo><mn>0.881</mn><mo>,</mo><msub><mrow><mi>p</mi></mrow><mrow><mi>x</mi></mrow></msub><mrow><mo>(</mo><mn>2</mn><mo>)</mo></mrow><mo>≈</mo><mn>0.119</mn></mtd></mtr><mtr><mtd><msub><mrow><mi>g</mi></mrow><mrow><mi>w</mi></mrow></msub><mrow><mo>(</mo><mi>x</mi><mo>)</mo></mrow><mo>≈</mo><mn>0.881</mn><mrow><mo>(</mo><mo>−</mo><mn>10</mn><mo>)</mo></mrow><mo>+</mo><mn>0.119</mn><mrow><mo>(</mo><mn>10</mn><mo>)</mo></mrow><mo>≈</mo><mo>−</mo><mn>7.62</mn></mtd></mtr></mtable></math>

An update in the negative-gradient direction increases x, locally reducing the cost of scenario 1, which currently has the higher cost. An actual step must also account for its size and the design constraints.

Uniform sampling without reweighting gives

<math display="block" aria-label="Uniform sampling without reweighting cancels the two slopes"><mn>0.5</mn><mrow><mo>(</mo><mo>−</mo><mn>10</mn><mo>)</mo></mrow><mo>+</mo><mn>0.5</mn><mrow><mo>(</mo><mn>10</mn><mo>)</mo></mrow><mo>=</mo><mn>0</mn></math>

so the two gradients cancel. More iterations estimate this different average more accurately; they do not recover the desired weighted sum. This comparison concerns unweighted sample averages. Uniform sampling with suitable importance weights is a separate possibility.

At a fixed x, if the chain's long-run visit frequencies are about 88.1% for scenario 1 and 11.9% for scenario 2, the simple average of visited gradients approaches −7.62. Visit frequency implements the weighting. For a Metropolis chain, iterations that reject a proposed move and remain in the same scenario must also be counted.

## 2. Stationarity, convergence conditions, and mixing speed

Write <math><msub><mrow><mi>P</mi></mrow><mrow><mi>x</mi></mrow></msub></math> for the transition matrix at the current design. The stationarity condition is

<math display="block" aria-label="Stationarity is invariance under one transition"><msub><mrow><mi>p</mi></mrow><mrow><mi>x</mi></mrow></msub><msub><mrow><mi>P</mi></mrow><mrow><mi>x</mi></mrow></msub><mo>=</mo><msub><mrow><mi>p</mi></mrow><mrow><mi>x</mi></mrow></msub></math>

Starting with a scenario distributed according to <math><msub><mrow><mi>p</mi></mrow><mrow><mi>x</mi></mrow></msub></math>, one transition preserves that distribution. Whether a chain started from an arbitrary scenario approaches it is a separate question.

For example, if the transition matrix is the identity,

<math display="block" aria-label="An identity transition matrix never changes the scenario"><msub><mrow><mi>P</mi></mrow><mrow><mi>x</mi></mrow></msub><mo>=</mo><mi>I</mi></math>

the chain stays in its initial scenario forever. Every distribution is stationary, but a path trapped in one scenario cannot compute the desired weighted average.

| Property to check | What it establishes |
|---|---|
| <math><msub><mrow><mi>p</mi></mrow><mrow><mi>x</mi></mrow></msub></math> is stationary | The transition preserves the target weights. |
| Irreducibility and other convergence conditions | Long-run visit frequencies approach the target independently of the initial scenario. |
| Mixing rate | How close the current-state distribution gets to the target within a finite number of transitions. |

On a finite state space, irreducibility supports convergence of time averages along a sample path. Convergence of the state distribution at each time also requires aperiodicity. See Levin and Peres, [*Markov Chains and Mixing Times*, Theorem 4.9 and Appendix C](https://pages.uoregon.edu/dlevin/MARKOV/mcmt2e.pdf), for this distinction.

These statements hold with x fixed. Updating the design also moves the target distribution <math><msub><mrow><mi>p</mi></mrow><mrow><mi>x</mi></mrow></msub></math>.

## 3. Updating the design before the chain has mixed

A direct approach fixes x, runs the chain long enough to estimate the average subgradient, and then updates the design. Repeating this process after every design change can be expensive. An alternative alternates one scenario transition with one design update:

<math display="block" aria-label="One Markov transition followed by one projected design update"><mtable columnalign="left"><mtr><mtd><msub><mrow><mi>I</mi></mrow><mrow><mrow><mi>n</mi><mo>+</mo><mn>1</mn></mrow></mrow></msub><mo>∼</mo><msub><mrow><mi>P</mi></mrow><mrow><msub><mrow><mi>x</mi></mrow><mrow><mi>n</mi></mrow></msub></mrow></msub><mrow><mo>(</mo><mrow><msub><mrow><mi>I</mi></mrow><mrow><mi>n</mi></mrow></msub><mo>,</mo><mo>·</mo></mrow><mo>)</mo></mrow></mtd></mtr><mtr><mtd><msub><mrow><mi>x</mi></mrow><mrow><mrow><mi>n</mi><mo>+</mo><mn>1</mn></mrow></mrow></msub><mo>=</mo><msub><mrow><mi>Π</mi></mrow><mrow><mi>X</mi></mrow></msub><mrow><mo>[</mo><msub><mrow><mi>x</mi></mrow><mrow><mi>n</mi></mrow></msub><mo>−</mo><msub><mrow><mi>α</mi></mrow><mrow><mrow><mi>n</mi><mo>+</mo><mn>1</mn></mrow></mrow></msub><mrow><mo>(</mo><msub><mrow><mi>g</mi></mrow><mrow><mi>f</mi></mrow></msub><mrow><mo>(</mo><msub><mrow><mi>x</mi></mrow><mrow><mi>n</mi></mrow></msub><mo>)</mo></mrow><mo>+</mo><msub><mrow><mi>g</mi></mrow><mrow><msub><mrow><mi>I</mi></mrow><mrow><mrow><mi>n</mi><mo>+</mo><mn>1</mn></mrow></mrow></msub></mrow></msub><mrow><mo>(</mo><msub><mrow><mi>x</mi></mrow><mrow><mi>n</mi></mrow></msub><mo>)</mo></mrow><mo>)</mo></mrow><mo>]</mo></mrow></mtd></mtr></mtable></math>

The first line makes one transition from the current scenario. The second updates the design using the visited scenario's subgradient. The projection returns the result to <math><mi>X</mi></math> in Euclidean distance. The next iteration continues from the scenario just visited.

The scenario location is carried forward. Its old operating cost is not automatically valid: after the design changes, acceptance probabilities must use costs evaluated at the current design. One transition also need not mean one operating-problem solve. Evaluating both proposed and current scenario costs may be necessary.

Suppose the previous search was already close to its target distribution:

<math display="block" aria-label="A slowly changing target and a sharply changing target"><mtable columnalign="left"><mtr><mtd><msub><mrow><mi>p</mi></mrow><mrow><msub><mrow><mi>x</mi></mrow><mrow><mi>n</mi></mrow></msub></mrow></msub><mo>=</mo><mrow><mo>(</mo><mn>0.88</mn><mo>,</mo><mn>0.12</mn><mo>)</mo></mrow><mo>,</mo><msub><mrow><mi>p</mi></mrow><mrow><msub><mrow><mi>x</mi></mrow><mrow><mrow><mi>n</mi><mo>+</mo><mn>1</mn></mrow></mrow></msub></mrow></msub><mo>=</mo><mrow><mo>(</mo><mn>0.85</mn><mo>,</mo><mn>0.15</mn><mo>)</mo></mrow></mtd></mtr><mtr><mtd><msub><mrow><mi>p</mi></mrow><mrow><msub><mrow><mi>x</mi></mrow><mrow><mrow><mi>n</mi><mo>+</mo><mn>1</mn></mrow></mrow></msub></mrow></msub><mo>=</mo><mrow><mo>(</mo><mn>0.12</mn><mo>,</mo><mn>0.88</mn><mo>)</mo></mrow></mtd></mtr></mtable></math>

In the first line, a change from (0.88, 0.12) to (0.85, 0.15) leaves the previous search state a useful starting point. In the second line, the target flips to (0.12, 0.88), making the previously frequent scenario less important. Until the chain adapts, it may supply directions that poorly reflect the current design.

The chain's speed of adaptation must therefore be considered together with the speed at which design updates move the target. If sampled subgradients are bounded by B and <math><msub><mrow><mi>x</mi></mrow><mrow><mi>n</mi></mrow></msub></math> belongs to <math><mi>X</mi></math>, nonexpansiveness of projection gives

<math display="block" aria-label="A bounded sampled subgradient limits the design movement"><mtable columnalign="left"><mtr><mtd><msub><mrow><mi>Z</mi></mrow><mrow><mrow><mi>n</mi><mo>+</mo><mn>1</mn></mrow></mrow></msub><mo>:=</mo><msub><mrow><mi>g</mi></mrow><mrow><mi>f</mi></mrow></msub><mrow><mo>(</mo><msub><mrow><mi>x</mi></mrow><mrow><mi>n</mi></mrow></msub><mo>)</mo></mrow><mo>+</mo><msub><mrow><mi>g</mi></mrow><mrow><msub><mrow><mi>I</mi></mrow><mrow><mrow><mi>n</mi><mo>+</mo><mn>1</mn></mrow></mrow></msub></mrow></msub><mrow><mo>(</mo><msub><mrow><mi>x</mi></mrow><mrow><mi>n</mi></mrow></msub><mo>)</mo></mrow><mo>,</mo><mrow><mo>‖</mo><msub><mrow><mi>Z</mi></mrow><mrow><mrow><mi>n</mi><mo>+</mo><mn>1</mn></mrow></mrow></msub><mo>‖</mo></mrow><mo>≤</mo><mi>B</mi></mtd></mtr><mtr><mtd><mrow><mo>‖</mo><msub><mrow><mi>x</mi></mrow><mrow><mrow><mi>n</mi><mo>+</mo><mn>1</mn></mrow></mrow></msub><mo>−</mo><msub><mrow><mi>x</mi></mrow><mrow><mi>n</mi></mrow></msub><mo>‖</mo></mrow><mo>≤</mo><msub><mrow><mi>α</mi></mrow><mrow><mrow><mi>n</mi><mo>+</mo><mn>1</mn></mrow></mrow></msub><mi>B</mi></mtd></mtr></mtable></math>

Smaller stepsizes limit design movement. At fixed w, a common Lipschitz bound on the operating costs also lets us control changes in the softmax weights through changes in the design. A small stepsize alone does not guarantee adequate tracking; the transition's mixing properties must also be checked.

After a single transition, <math><msub><mrow><mi>I</mi></mrow><mrow><mrow><mi>n</mi><mo>+</mo><mn>1</mn></mrow></mrow></msub></math> is generally not an exact draw from <math><msub><mrow><mi>p</mi></mrow><mrow><msub><mrow><mi>x</mi></mrow><mrow><mi>n</mi></mrow></msub></mrow></msub></math>. Thus <math><msub><mrow><mi>Z</mi></mrow><mrow><mrow><mi>n</mi><mo>+</mo><mn>1</mn></mrow></mrow></msub></math> cannot be treated as a conditionally unbiased SGD estimator. Convergence analysis must control how this discrepancy affects the whole sequence of updates.

## 4. Isolating sampling error in the distance-to-optimum inequality

Assume a minimizer exists at the fixed w and choose a comparison point:

<math display="block" aria-label="A comparison optimizer for the fixed-temperature objective"><msup><mrow><mi>x</mi></mrow><mrow><mo>⋆</mo></mrow></msup><mo>∈</mo><mi>arg</mi><munder><mo>min</mo><mrow><mi>x</mi><mo>∈</mo><mi>X</mi></mrow></munder><msub><mrow><mi>F</mi></mrow><mrow><mi>w</mi></mrow></msub><mrow><mo>(</mo><mi>x</mi><mo>)</mo></mrow><mo>,</mo><msubsup><mi>F</mi><mi>w</mi><mo>⋆</mo></msubsup><mo>:=</mo><msub><mrow><mi>F</mi></mrow><mrow><mi>w</mi></mrow></msub><mrow><mo>(</mo><msup><mrow><mi>x</mi></mrow><mrow><mo>⋆</mo></mrow></msup><mo>)</mo></mrow></math>

The algorithm does not know <math><msup><mrow><mi>x</mi></mrow><mrow><mo>⋆</mo></mrow></msup></math> in advance; it is used in the proof. Euclidean projection gives the one-step inequality

<math display="block" aria-label="The one-step squared-distance inequality"><mtable columnalign="left"><mtr><mtd><msup><mrow><mrow><mo>‖</mo><msub><mrow><mi>x</mi></mrow><mrow><mrow><mi>n</mi><mo>+</mo><mn>1</mn></mrow></mrow></msub><mo>−</mo><msup><mrow><mi>x</mi></mrow><mrow><mo>⋆</mo></mrow></msup><mo>‖</mo></mrow></mrow><mrow><mn>2</mn></mrow></msup><mo>≤</mo><msup><mrow><mrow><mo>‖</mo><msub><mrow><mi>x</mi></mrow><mrow><mi>n</mi></mrow></msub><mo>−</mo><msub><mrow><mi>α</mi></mrow><mrow><mrow><mi>n</mi><mo>+</mo><mn>1</mn></mrow></mrow></msub><msub><mrow><mi>Z</mi></mrow><mrow><mrow><mi>n</mi><mo>+</mo><mn>1</mn></mrow></mrow></msub><mo>−</mo><msup><mrow><mi>x</mi></mrow><mrow><mo>⋆</mo></mrow></msup><mo>‖</mo></mrow></mrow><mrow><mn>2</mn></mrow></msup></mtd></mtr><mtr><mtd><mo>=</mo><msup><mrow><mrow><mo>‖</mo><mrow><msub><mrow><mi>x</mi></mrow><mrow><mi>n</mi></mrow></msub><mo>−</mo><msup><mrow><mi>x</mi></mrow><mrow><mo>⋆</mo></mrow></msup></mrow><mo>‖</mo></mrow></mrow><mrow><mn>2</mn></mrow></msup><mo>−</mo><mn>2</mn><msub><mrow><mi>α</mi></mrow><mrow><mrow><mi>n</mi><mo>+</mo><mn>1</mn></mrow></mrow></msub><msup><mrow><msub><mrow><mi>Z</mi></mrow><mrow><mrow><mi>n</mi><mo>+</mo><mn>1</mn></mrow></mrow></msub></mrow><mrow><mo>⊤</mo></mrow></msup><mrow><mo>(</mo><mrow><msub><mrow><mi>x</mi></mrow><mrow><mi>n</mi></mrow></msub><mo>−</mo><msup><mrow><mi>x</mi></mrow><mrow><mo>⋆</mo></mrow></msup></mrow><mo>)</mo></mrow><mo>+</mo><msup><mrow><msub><mrow><mi>α</mi></mrow><mrow><mrow><mi>n</mi><mo>+</mo><mn>1</mn></mrow></mrow></msub></mrow><mrow><mn>2</mn></mrow></msup><msup><mrow><mrow><mo>‖</mo><msub><mrow><mi>Z</mi></mrow><mrow><mrow><mi>n</mi><mo>+</mo><mn>1</mn></mrow></mrow></msub><mo>‖</mo></mrow></mrow><mrow><mn>2</mn></mrow></msup></mtd></mtr></mtable></math>

A sufficiently positive inner product in the middle term contributes to reducing squared distance. With an exact subgradient, convexity directly connects that inner product to the objective gap:

<math display="block" aria-label="An exact subgradient controls the objective gap"><mtable columnalign="left"><mtr><mtd><msub><mrow><mi>z</mi></mrow><mrow><mi>n</mi></mrow></msub><mo>∈</mo><mo>∂</mo><msub><mrow><mi>F</mi></mrow><mrow><mi>w</mi></mrow></msub><mrow><mo>(</mo><msub><mrow><mi>x</mi></mrow><mrow><mi>n</mi></mrow></msub><mo>)</mo></mrow></mtd></mtr><mtr><mtd><msup><mrow><msub><mrow><mi>z</mi></mrow><mrow><mi>n</mi></mrow></msub></mrow><mrow><mo>⊤</mo></mrow></msup><mrow><mo>(</mo><mrow><msub><mrow><mi>x</mi></mrow><mrow><mi>n</mi></mrow></msub><mo>−</mo><msup><mrow><mi>x</mi></mrow><mrow><mo>⋆</mo></mrow></msup></mrow><mo>)</mo></mrow><mo>≥</mo><mrow><msub><mrow><mi>F</mi></mrow><mrow><mi>w</mi></mrow></msub><mrow><mo>(</mo><msub><mrow><mi>x</mi></mrow><mrow><mi>n</mi></mrow></msub><mo>)</mo></mrow><mo>−</mo><msubsup><mi>F</mi><mi>w</mi><mo>⋆</mo></msubsup></mrow></mtd></mtr></mtable></math>

The actual <math><msub><mrow><mi>Z</mi></mrow><mrow><mrow><mi>n</mi><mo>+</mo><mn>1</mn></mrow></mrow></msub></math> contains information from only one scenario, so this inequality cannot be applied to it directly. Define a scenario-specific cost difference

<math display="block" aria-label="Scenario-specific cost differences relative to the comparison design"><msub><mrow><mi>r</mi></mrow><mrow><mi>i</mi></mrow></msub><mrow><mo>(</mo><mi>x</mi><mo>)</mo></mrow><mo>:=</mo><mrow><msub><mrow><mi>Q</mi></mrow><mrow><mi>i</mi></mrow></msub><mrow><mo>(</mo><mi>x</mi><mo>)</mo></mrow><mo>−</mo><msub><mrow><mi>Q</mi></mrow><mrow><mi>i</mi></mrow></msub><mrow><mo>(</mo><msup><mrow><mi>x</mi></mrow><mrow><mo>⋆</mo></mrow></msup><mo>)</mo></mrow></mrow></math>

An individual <math><msub><mrow><mi>r</mi></mrow><mrow><mi>i</mi></mrow></msub></math>(x) may be negative because <math><msup><mrow><mi>x</mi></mrow><mrow><mo>⋆</mo></mrow></msup></math> need not minimize every scenario separately. Define the sampling error as the visited scenario's cost difference minus its average under the target distribution:

<math display="block" aria-label="The sampled cost difference minus its target-distribution average"><msub><mrow><mi>e</mi></mrow><mrow><mrow><mi>n</mi><mo>+</mo><mn>1</mn></mrow></mrow></msub><mo>:=</mo><msub><mrow><mi>r</mi></mrow><mrow><msub><mrow><mi>I</mi></mrow><mrow><mrow><mi>n</mi><mo>+</mo><mn>1</mn></mrow></mrow></msub></mrow></msub><mrow><mo>(</mo><msub><mrow><mi>x</mi></mrow><mrow><mi>n</mi></mrow></msub><mo>)</mo></mrow><mo>−</mo><munder><mo>∑</mo><mi>i</mi></munder><msub><mrow><mi>p</mi></mrow><mrow><msub><mrow><mi>x</mi></mrow><mrow><mi>n</mi></mrow></msub></mrow></msub><mrow><mo>(</mo><mi>i</mi><mo>)</mo></mrow><msub><mrow><mi>r</mi></mrow><mrow><mi>i</mi></mrow></msub><mrow><mo>(</mo><msub><mrow><mi>x</mi></mrow><mrow><mi>n</mi></mrow></msub><mo>)</mo></mrow></math>

If <math><msub><mrow><mi>I</mi></mrow><mrow><mrow><mi>n</mi><mo>+</mo><mn>1</mn></mrow></mrow></msub></math> were drawn exactly from <math><msub><mrow><mi>p</mi></mrow><mrow><msub><mrow><mi>x</mi></mrow><mrow><mi>n</mi></mrow></msub></mrow></msub></math> conditional on the history, this error would have zero conditional mean. For one Markov transition, writing ℱ for the history gives, in general,

<math display="block" aria-label="One Markov transition need not give zero conditional mean error"><mi>𝔼</mi><mrow><mo>[</mo><msub><mrow><mi>e</mi></mrow><mrow><mrow><mi>n</mi><mo>+</mo><mn>1</mn></mrow></mrow></msub><mo>|</mo><msub><mrow><mi>ℱ</mi></mrow><mrow><mi>n</mi></mrow></msub><mo>]</mo></mrow><mo>=</mo><munder><mo>∑</mo><mi>i</mi></munder><mrow><mo>(</mo><msub><mrow><mi>P</mi></mrow><mrow><msub><mrow><mi>x</mi></mrow><mrow><mi>n</mi></mrow></msub></mrow></msub><mrow><mo>(</mo><mrow><msub><mrow><mi>I</mi></mrow><mrow><mi>n</mi></mrow></msub><mo>,</mo><mi>i</mi></mrow><mo>)</mo></mrow><mo>−</mo><msub><mrow><mi>p</mi></mrow><mrow><msub><mrow><mi>x</mi></mrow><mrow><mi>n</mi></mrow></msub></mrow></msub><mrow><mo>(</mo><mi>i</mi><mo>)</mo></mrow><mo>)</mo></mrow><msub><mrow><mi>r</mi></mrow><mrow><mi>i</mi></mrow></msub><mrow><mo>(</mo><msub><mrow><mi>x</mi></mrow><mrow><mi>n</mi></mrow></msub><mo>)</mo></mrow><mo>≠</mo><mn>0</mn></math>

The final ≠ 0 means the expression need not vanish; it can be zero for particular histories. This error is a scalar defined from cost differences, rather than a difference between gradient vectors.

Convexity of the investment and scenario costs gives

<math display="block" aria-label="Convexity lower-bounds the sampled inner product"><msup><mrow><msub><mrow><mi>Z</mi></mrow><mrow><mrow><mi>n</mi><mo>+</mo><mn>1</mn></mrow></mrow></msub></mrow><mrow><mo>⊤</mo></mrow></msup><mrow><mo>(</mo><mrow><msub><mrow><mi>x</mi></mrow><mrow><mi>n</mi></mrow></msub><mo>−</mo><msup><mrow><mi>x</mi></mrow><mrow><mo>⋆</mo></mrow></msup></mrow><mo>)</mo></mrow><mo>≥</mo><mi>f</mi><mrow><mo>(</mo><msub><mrow><mi>x</mi></mrow><mrow><mi>n</mi></mrow></msub><mo>)</mo></mrow><mo>−</mo><mi>f</mi><mrow><mo>(</mo><msup><mrow><mi>x</mi></mrow><mrow><mo>⋆</mo></mrow></msup><mo>)</mo></mrow><mo>+</mo><msub><mrow><mi>r</mi></mrow><mrow><msub><mrow><mi>I</mi></mrow><mrow><mrow><mi>n</mi><mo>+</mo><mn>1</mn></mrow></mrow></msub></mrow></msub><mrow><mo>(</mo><msub><mrow><mi>x</mi></mrow><mrow><mi>n</mi></mrow></msub><mo>)</mo></mrow></math>

Viewed as a convex function of the cost vector, mellowmax has gradient <math><msub><mrow><mi>p</mi></mrow><mrow><mi>x</mi></mrow></msub></math>. Its supporting-hyperplane inequality at the current cost vector yields

<math display="block" aria-label="Convexity of mellowmax as a function of the cost vector"><munder><mo>∑</mo><mi>i</mi></munder><msub><mrow><mi>p</mi></mrow><mrow><mi>x</mi></mrow></msub><mrow><mo>(</mo><mi>i</mi><mo>)</mo></mrow><mrow><mo>[</mo><mrow><msub><mrow><mi>Q</mi></mrow><mrow><mi>i</mi></mrow></msub><mrow><mo>(</mo><mi>x</mi><mo>)</mo></mrow><mo>−</mo><msub><mrow><mi>Q</mi></mrow><mrow><mi>i</mi></mrow></msub><mrow><mo>(</mo><msup><mrow><mi>x</mi></mrow><mrow><mo>⋆</mo></mrow></msup><mo>)</mo></mrow></mrow><mo>]</mo></mrow><mo>≥</mo><msub><mrow><mi>M</mi></mrow><mrow><mi>w</mi></mrow></msub><mrow><mo>(</mo><mi>x</mi><mo>)</mo></mrow><mo>−</mo><msub><mrow><mi>M</mi></mrow><mrow><mi>w</mi></mrow></msub><mrow><mo>(</mo><msup><mrow><mi>x</mi></mrow><mrow><mo>⋆</mo></mrow></msup><mo>)</mo></mrow></math>

The direction matters: the weighted cost difference upper-bounds the difference in mellowmax values, allowing it to be combined with the preceding scenario-wise lower bound. For log-sum-exp convexity and the supporting-hyperplane inequality, see Boyd and Vandenberghe, [*Convex Optimization*, Chapter 3](https://web.stanford.edu/~boyd/cvxbook/).

Substituting the definition of the sampling error gives

<math display="block" aria-label="The sampled direction controls the objective gap plus the error"><msup><mrow><msub><mrow><mi>Z</mi></mrow><mrow><mrow><mi>n</mi><mo>+</mo><mn>1</mn></mrow></mrow></msub></mrow><mrow><mo>⊤</mo></mrow></msup><mrow><mo>(</mo><mrow><msub><mrow><mi>x</mi></mrow><mrow><mi>n</mi></mrow></msub><mo>−</mo><msup><mrow><mi>x</mi></mrow><mrow><mo>⋆</mo></mrow></msup></mrow><mo>)</mo></mrow><mo>≥</mo><mrow><msub><mrow><mi>F</mi></mrow><mrow><mi>w</mi></mrow></msub><mrow><mo>(</mo><msub><mrow><mi>x</mi></mrow><mrow><mi>n</mi></mrow></msub><mo>)</mo></mrow><mo>−</mo><msubsup><mi>F</mi><mi>w</mi><mo>⋆</mo></msubsup></mrow><mo>+</mo><msub><mrow><mi>e</mi></mrow><mrow><mrow><mi>n</mi><mo>+</mo><mn>1</mn></mrow></mrow></msub></math>

A large negative <math><msub><mrow><mi>e</mi></mrow><mrow><mrow><mi>n</mi><mo>+</mo><mn>1</mn></mrow></mrow></msub></math> means the visited scenario reports a smaller cost difference than the target-weighted average. This weakens the lower bound supporting distance reduction.

## 5. The quantity to control is the stepsize-weighted cumulative error

Insert the inner-product lower bound and the bound B on <math><msub><mrow><mi>Z</mi></mrow><mrow><mrow><mi>n</mi><mo>+</mo><mn>1</mn></mrow></mrow></msub></math> into the distance inequality:

<math display="block" aria-label="Distance decrease, the quadratic term, and the signed sampling error"><mtable columnalign="left"><mtr><mtd><msub><mrow><mi>D</mi></mrow><mrow><mi>n</mi></mrow></msub><mo>:=</mo><msup><mrow><mrow><mo>‖</mo><mrow><msub><mrow><mi>x</mi></mrow><mrow><mi>n</mi></mrow></msub><mo>−</mo><msup><mrow><mi>x</mi></mrow><mrow><mo>⋆</mo></mrow></msup></mrow><mo>‖</mo></mrow></mrow><mrow><mn>2</mn></mrow></msup></mtd></mtr><mtr><mtd><mn>2</mn><msub><mrow><mi>α</mi></mrow><mrow><mrow><mi>n</mi><mo>+</mo><mn>1</mn></mrow></mrow></msub><mrow><mo>[</mo><mrow><msub><mrow><mi>F</mi></mrow><mrow><mi>w</mi></mrow></msub><mrow><mo>(</mo><msub><mrow><mi>x</mi></mrow><mrow><mi>n</mi></mrow></msub><mo>)</mo></mrow><mo>−</mo><msubsup><mi>F</mi><mi>w</mi><mo>⋆</mo></msubsup></mrow><mo>]</mo></mrow><mo>≤</mo><msub><mrow><mi>D</mi></mrow><mrow><mi>n</mi></mrow></msub><mo>−</mo><msub><mrow><mi>D</mi></mrow><mrow><mrow><mi>n</mi><mo>+</mo><mn>1</mn></mrow></mrow></msub><mo>+</mo><msup><mrow><msub><mrow><mi>α</mi></mrow><mrow><mrow><mi>n</mi><mo>+</mo><mn>1</mn></mrow></mrow></msub></mrow><mrow><mn>2</mn></mrow></msup><msup><mrow><mi>B</mi></mrow><mrow><mn>2</mn></mrow></msup><mo>−</mo><mn>2</mn><msub><mrow><mi>α</mi></mrow><mrow><mrow><mi>n</mi><mo>+</mo><mn>1</mn></mrow></mrow></msub><msub><mrow><mi>e</mi></mrow><mrow><mrow><mi>n</mi><mo>+</mo><mn>1</mn></mrow></mrow></msub></mtd></mtr></mtable></math>

The right side contains the reduction in squared distance, a quadratic term from taking a finite step, and the contribution of sampling error. Summing over iterations telescopes the distance terms:

<math display="block" aria-label="Squared-distance terms telescope"><munderover><mo>∑</mo><mrow><mi>n</mi><mo>=</mo><mn>0</mn></mrow><mrow><mi>N</mi><mo>−</mo><mn>1</mn></mrow></munderover><mrow><mo>(</mo><msub><mrow><mi>D</mi></mrow><mrow><mi>n</mi></mrow></msub><mo>−</mo><msub><mrow><mi>D</mi></mrow><mrow><mrow><mi>n</mi><mo>+</mo><mn>1</mn></mrow></mrow></msub><mo>)</mo></mrow><mo>=</mo><msub><mrow><mi>D</mi></mrow><mrow><mn>0</mn></mrow></msub><mo>−</mo><msub><mrow><mi>D</mi></mrow><mrow><mi>N</mi></mrow></msub><mo>≤</mo><msub><mrow><mi>D</mi></mrow><mrow><mn>0</mn></mrow></msub></math>

For a fixed initial design, taking expectations gives

<math display="block" aria-label="The cumulative error that the Markov-chain analysis must control"><mtable columnalign="left"><mtr><mtd><mn>2</mn><munderover><mo>∑</mo><mrow><mi>n</mi><mo>=</mo><mn>0</mn></mrow><mrow><mi>N</mi><mo>−</mo><mn>1</mn></mrow></munderover><msub><mrow><mi>α</mi></mrow><mrow><mrow><mi>n</mi><mo>+</mo><mn>1</mn></mrow></mrow></msub><mi>𝔼</mi><mrow><mo>[</mo><mrow><msub><mrow><mi>F</mi></mrow><mrow><mi>w</mi></mrow></msub><mrow><mo>(</mo><msub><mrow><mi>x</mi></mrow><mrow><mi>n</mi></mrow></msub><mo>)</mo></mrow><mo>−</mo><msubsup><mi>F</mi><mi>w</mi><mo>⋆</mo></msubsup></mrow><mo>]</mo></mrow></mtd></mtr><mtr><mtd><mo>≤</mo><msub><mrow><mi>D</mi></mrow><mrow><mn>0</mn></mrow></msub><mo>+</mo><msup><mrow><mi>B</mi></mrow><mrow><mn>2</mn></mrow></msup><munderover><mo>∑</mo><mrow><mi>n</mi><mo>=</mo><mn>0</mn></mrow><mrow><mi>N</mi><mo>−</mo><mn>1</mn></mrow></munderover><msup><mrow><msub><mrow><mi>α</mi></mrow><mrow><mrow><mi>n</mi><mo>+</mo><mn>1</mn></mrow></mrow></msub></mrow><mrow><mn>2</mn></mrow></msup><mo>+</mo><mi>𝔼</mi><mrow><mo>[</mo><mo>−</mo><mn>2</mn><munderover><mo>∑</mo><mrow><mi>n</mi><mo>=</mo><mn>0</mn></mrow><mrow><mi>N</mi><mo>−</mo><mn>1</mn></mrow></munderover><msub><mrow><mi>α</mi></mrow><mrow><mrow><mi>n</mi><mo>+</mo><mn>1</mn></mrow></mrow></msub><msub><mrow><mi>e</mi></mrow><mrow><mrow><mi>n</mi><mo>+</mo><mn>1</mn></mrow></mrow></msub><mo>]</mo></mrow></mtd></mtr></mtable></math>

Each <math><msub><mrow><mi>e</mi></mrow><mrow><mrow><mi>n</mi><mo>+</mo><mn>1</mn></mrow></mrow></msub></math> need not be zero. It is enough to bound the final cumulative-error term so that it grows sufficiently slowly relative to the sum of stepsizes.

For example, suppose one can prove that finite nonnegative constants <math><msub><mrow><mi>C</mi></mrow><mrow><mn>0</mn></mrow></msub></math> and <math><msub><mrow><mi>C</mi></mrow><mrow><mn>1</mn></mrow></msub></math>, independent of N, satisfy

<math display="block" aria-label="An additional cumulative-error bound, assumed for the rate derivation"><mi>𝔼</mi><mrow><mo>[</mo><mo>−</mo><mn>2</mn><munderover><mo>∑</mo><mrow><mi>n</mi><mo>=</mo><mn>0</mn></mrow><mrow><mi>N</mi><mo>−</mo><mn>1</mn></mrow></munderover><msub><mrow><mi>α</mi></mrow><mrow><mrow><mi>n</mi><mo>+</mo><mn>1</mn></mrow></mrow></msub><msub><mrow><mi>e</mi></mrow><mrow><mrow><mi>n</mi><mo>+</mo><mn>1</mn></mrow></mrow></msub><mo>]</mo></mrow><mo>≤</mo><msub><mrow><mi>C</mi></mrow><mrow><mn>0</mn></mrow></msub><mo>+</mo><msub><mrow><mi>C</mi></mrow><mrow><mn>1</mn></mrow></msub><munderover><mo>∑</mo><mrow><mi>n</mi><mo>=</mo><mn>0</mn></mrow><mrow><mi>N</mi><mo>−</mo><mn>1</mn></mrow></munderover><msup><mrow><msub><mrow><mi>α</mi></mrow><mrow><mrow><mi>n</mi><mo>+</mo><mn>1</mn></mrow></mrow></msub></mrow><mrow><mn>2</mn></mrow></msup></math>

This does not follow from the existence of a stationary distribution alone. It requires a separate argument using conditions on mixing of the design-dependent transitions, regularity with respect to design changes, and the stepsizes. The constants may depend on the fixed w, the problem, and the chain.

A Poisson-equation decomposition is one way to obtain such a bound. It expresses the centered cost differences through an equation involving the transition operator and uses that representation to analyze their accumulated contribution. Bounds and regularity for the equation's solution have not been proved here. The rate below is therefore conditional on establishing the stated cumulative-error bound.

## 6. Expected objective error of the averaged design

Define the stepsize-weighted average of the pre-update designs:

<math display="block" aria-label="The stepsize-weighted average of pre-update designs"><msub><mrow><mover><mi>x</mi><mo>¯</mo></mover></mrow><mrow><mi>N</mi></mrow></msub><mo>:=</mo><mfrac><mrow><munderover><mo>∑</mo><mrow><mi>n</mi><mo>=</mo><mn>0</mn></mrow><mrow><mi>N</mi><mo>−</mo><mn>1</mn></mrow></munderover><msub><mrow><mi>α</mi></mrow><mrow><mrow><mi>n</mi><mo>+</mo><mn>1</mn></mrow></mrow></msub><msub><mrow><mi>x</mi></mrow><mrow><mi>n</mi></mrow></msub></mrow><mrow><munderover><mo>∑</mo><mrow><mi>n</mi><mo>=</mo><mn>0</mn></mrow><mrow><mi>N</mi><mo>−</mo><mn>1</mn></mrow></munderover><msub><mrow><mi>α</mi></mrow><mrow><mrow><mi>n</mi><mo>+</mo><mn>1</mn></mrow></mrow></msub></mrow></mfrac></math>

Positive stepsizes and convexity of <math><mi>X</mi></math> keep this average feasible. Convexity of <math><msub><mrow><mi>F</mi></mrow><mrow><mi>w</mi></mrow></msub></math>, together with the cumulative-error bound, gives

<math display="block" aria-label="Expected objective error of the weighted average"><mtable columnalign="left"><mtr><mtd><mi>𝔼</mi><mrow><mo>[</mo><msub><mrow><mi>F</mi></mrow><mrow><mi>w</mi></mrow></msub><mrow><mo>(</mo><msub><mrow><mover><mi>x</mi><mo>¯</mo></mover></mrow><mrow><mi>N</mi></mrow></msub><mo>)</mo></mrow><mo>]</mo></mrow><mo>−</mo><msubsup><mi>F</mi><mi>w</mi><mo>⋆</mo></msubsup></mtd></mtr><mtr><mtd><mo>≤</mo><mfrac><mrow><mrow><msub><mrow><mi>D</mi></mrow><mrow><mn>0</mn></mrow></msub><mo>+</mo><msub><mrow><mi>C</mi></mrow><mrow><mn>0</mn></mrow></msub><mo>+</mo><mrow><mo>(</mo><msup><mrow><mi>B</mi></mrow><mrow><mn>2</mn></mrow></msup><mo>+</mo><msub><mrow><mi>C</mi></mrow><mrow><mn>1</mn></mrow></msub><mo>)</mo></mrow><munderover><mo>∑</mo><mrow><mi>n</mi><mo>=</mo><mn>0</mn></mrow><mrow><mi>N</mi><mo>−</mo><mn>1</mn></mrow></munderover><msup><mrow><msub><mrow><mi>α</mi></mrow><mrow><mrow><mi>n</mi><mo>+</mo><mn>1</mn></mrow></mrow></msub></mrow><mrow><mn>2</mn></mrow></msup></mrow></mrow><mrow><mrow><mn>2</mn><munderover><mo>∑</mo><mrow><mi>n</mi><mo>=</mo><mn>0</mn></mrow><mrow><mi>N</mi><mo>−</mo><mn>1</mn></mrow></munderover><msub><mrow><mi>α</mi></mrow><mrow><mrow><mi>n</mi><mo>+</mo><mn>1</mn></mrow></mrow></msub></mrow></mrow></mfrac></mtd></mtr></mtable></math>

We can now compare the growth of the numerator and denominator. For example,

<math display="block" aria-label="Inverse-square-root stepsizes and the growth of their sums"><mtable columnalign="left"><mtr><mtd><msub><mrow><mi>α</mi></mrow><mrow><mrow><mi>n</mi><mo>+</mo><mn>1</mn></mrow></mrow></msub><mo>=</mo><mfrac><mrow><mi>a</mi></mrow><mrow><msqrt><mrow><mi>n</mi><mo>+</mo><mn>1</mn></mrow></msqrt></mrow></mfrac><mo>,</mo><mi>a</mi><mo>&gt;</mo><mn>0</mn></mtd></mtr><mtr><mtd><munderover><mo>∑</mo><mrow><mi>n</mi><mo>=</mo><mn>0</mn></mrow><mrow><mi>N</mi><mo>−</mo><mn>1</mn></mrow></munderover><msub><mrow><mi>α</mi></mrow><mrow><mrow><mi>n</mi><mo>+</mo><mn>1</mn></mrow></mrow></msub><mo>≍</mo><msqrt><mi>N</mi></msqrt><mo>,</mo><munderover><mo>∑</mo><mrow><mi>n</mi><mo>=</mo><mn>0</mn></mrow><mrow><mi>N</mi><mo>−</mo><mn>1</mn></mrow></munderover><msup><mrow><msub><mrow><mi>α</mi></mrow><mrow><mrow><mi>n</mi><mo>+</mo><mn>1</mn></mrow></mrow></msub></mrow><mrow><mn>2</mn></mrow></msup><mo>≍</mo><mi>log</mi><mi>N</mi></mtd></mtr></mtable></math>

where ≍ denotes the same order of growth in N. Holding w and the associated constants fixed yields

<math display="block" aria-label="A conditional rate for the fixed-temperature averaged objective"><mi>𝔼</mi><mrow><mo>[</mo><msub><mrow><mi>F</mi></mrow><mrow><mi>w</mi></mrow></msub><mrow><mo>(</mo><msub><mrow><mover><mi>x</mi><mo>¯</mo></mover></mrow><mrow><mi>N</mi></mrow></msub><mo>)</mo></mrow><mo>]</mo></mrow><mo>−</mo><msubsup><mi>F</mi><mi>w</mi><mo>⋆</mo></msubsup><mo>=</mo><mi>O</mi><mrow><mo>(</mo><mfrac><mrow><mrow><mi>log</mi><mi>N</mi></mrow></mrow><mrow><msqrt><mi>N</mi></msqrt></mrow></mfrac><mo>)</mo></mrow><mo>→</mo><mn>0</mn></math>

This result concerns the expected objective error of the averaged design. It does not establish cost reduction at every iteration, unbiasedness of individual samples, or convergence of the last design itself. It also concerns the mellowmax problem at a fixed temperature. Approximation error relative to the original maximum-cost problem, and changes in mixing as w decreases, require separate analysis.

<!-- ko -->

Markov chain으로 시나리오를 골라 최적화할 때 정상분포는 어떤 평균 방향을 계산하는지 결정합니다. 비용이 큰 시나리오에 더 큰 가중치를 주고 싶다면, 그 비율만큼 자주 방문하도록 chain을 설계할 수 있습니다. 다만 원하는 분포가 정상분포라는 사실만으로는 짧은 탐색에서 그 평균을 얻는다고 보장할 수 없습니다. 설계까지 매번 바뀐다면 표본 편향이 최적화에 누적되는 효과도 살펴야 합니다.

## 1. 시나리오를 방문하는 비율이 기울기의 가중치가 됩니다

설계변수 <math><mi>x</mi></math>를 정하면 투자비 f(x)와 시나리오별 운영비용 <math><msub><mrow><mi>Q</mi></mrow><mrow><mi>i</mi></mrow></msub></math>(x)가 결정된다고 합시다. 시나리오는 m개이며, 비용이 큰 시나리오를 강조하기 위해 고정된 온도 w > 0에서 mellowmax 목적함수를 사용합니다.

<math display="block" aria-label="The mellowmax objective at a fixed temperature"><mtable columnalign="left"><mtr><mtd><msub><mrow><mi>F</mi></mrow><mrow><mi>w</mi></mrow></msub><mrow><mo>(</mo><mi>x</mi><mo>)</mo></mrow><mo>=</mo><mi>f</mi><mrow><mo>(</mo><mi>x</mi><mo>)</mo></mrow><mo>+</mo><msub><mrow><mi>M</mi></mrow><mrow><mi>w</mi></mrow></msub><mrow><mo>(</mo><mi>x</mi><mo>)</mo></mrow></mtd></mtr><mtr><mtd><msub><mrow><mi>M</mi></mrow><mrow><mi>w</mi></mrow></msub><mrow><mo>(</mo><mi>x</mi><mo>)</mo></mrow><mo>=</mo><mi>w</mi><mi>log</mi><mrow><mo>(</mo><mfrac><mrow><mn>1</mn></mrow><mrow><mi>m</mi></mrow></mfrac><munderover><mo>∑</mo><mrow><mi>i</mi><mo>=</mo><mn>1</mn></mrow><mi>m</mi></munderover><mi>exp</mi><mrow><mo>(</mo><mfrac><mrow><msub><mrow><mi>Q</mi></mrow><mrow><mi>i</mi></mrow></msub><mrow><mo>(</mo><mi>x</mi><mo>)</mo></mrow></mrow><mrow><mi>w</mi></mrow></mfrac><mo>)</mo></mrow><mo>)</mo></mrow></mtd></mtr></mtable></math>

여기서 w는 비용을 나누는 온도입니다. 문헌에 따라 역온도로 표기하기도 하므로 정의를 먼저 확인해야 합니다. 이 글에서는 설계 가능 영역 <math><mi>X</mi></math>가 비어 있지 않은 닫힌 볼록집합이고, f와 각 <math><msub><mrow><mi>Q</mi></mrow><mrow><mi>i</mi></mrow></msub></math>가 <math><mi>X</mi></math>를 포함하는 근방에서 유한한 볼록함수이며 필요한 부분기울기가 존재한다고 가정합니다. Mellowmax는 최대 시나리오 비용의 근사이며, w를 고정한 목적함수를 최적화하는 문제를 다룹니다.

투자비와 운영비용의 부분기울기(subgradient)를 각각 <math><msub><mrow><mi>g</mi></mrow><mrow><mi>f</mi></mrow></msub></math>(x), <math><msub><mrow><mi>g</mi></mrow><mrow><mi>i</mi></mrow></msub></math>(x)라고 하면,

<math display="block" aria-label="Scenario weights and a subgradient of the objective"><mtable columnalign="left"><mtr><mtd><msub><mrow><mi>p</mi></mrow><mrow><mi>x</mi></mrow></msub><mrow><mo>(</mo><mi>i</mi><mo>)</mo></mrow><mo>=</mo><mfrac><mrow><mi>exp</mi><mrow><mo>(</mo><mfrac><mrow><msub><mrow><mi>Q</mi></mrow><mrow><mi>i</mi></mrow></msub><mrow><mo>(</mo><mi>x</mi><mo>)</mo></mrow></mrow><mrow><mi>w</mi></mrow></mfrac><mo>)</mo></mrow></mrow><mrow><munder><mo>∑</mo><mi>j</mi></munder><mi>exp</mi><mrow><mo>(</mo><mfrac><mrow><msub><mrow><mi>Q</mi></mrow><mrow><mi>j</mi></mrow></msub><mrow><mo>(</mo><mi>x</mi><mo>)</mo></mrow></mrow><mrow><mi>w</mi></mrow></mfrac><mo>)</mo></mrow></mrow></mfrac></mtd></mtr><mtr><mtd><msub><mrow><mi>g</mi></mrow><mrow><mi>w</mi></mrow></msub><mrow><mo>(</mo><mi>x</mi><mo>)</mo></mrow><mo>=</mo><msub><mrow><mi>g</mi></mrow><mrow><mi>f</mi></mrow></msub><mrow><mo>(</mo><mi>x</mi><mo>)</mo></mrow><mo>+</mo><munder><mo>∑</mo><mi>i</mi></munder><msub><mrow><mi>p</mi></mrow><mrow><mi>x</mi></mrow></msub><mrow><mo>(</mo><mi>i</mi><mo>)</mo></mrow><msub><mrow><mi>g</mi></mrow><mrow><mi>i</mi></mrow></msub><mrow><mo>(</mo><mi>x</mi><mo>)</mo></mrow><mo>∈</mo><mo>∂</mo><msub><mrow><mi>F</mi></mrow><mrow><mi>w</mi></mrow></msub><mrow><mo>(</mo><mi>x</mi><mo>)</mo></mrow></mtd></mtr></mtable></math>

입니다. 모든 시나리오를 평가하기 어렵다면 방문한 시나리오의 부분기울기만 사용하고 싶어집니다. 이때 방문 비율이 달라지면 평균적으로 계산하는 방향도 달라집니다.

현재 설계에서 두 시나리오의 비용과 기울기가 아래와 같다고 합시다. 이 예제에서는 x가 스칼라이며 투자비 기울기는 생략합니다.

| 시나리오 | 운영비용 | 설계에 대한 기울기 |
|---|---:|---:|
| 1 | 30 | −10 |
| 2 | 10 | +10 |

w = 10이면 원하는 가중치와 평균 방향은

<math display="block" aria-label="Softmax weights for the two-scenario example"><mtable columnalign="left"><mtr><mtd><msub><mrow><mi>p</mi></mrow><mrow><mi>x</mi></mrow></msub><mrow><mo>(</mo><mn>1</mn><mo>)</mo></mrow><mo>=</mo><mfrac><mrow><mi>exp</mi><mrow><mo>(</mo><mn>3</mn><mo>)</mo></mrow></mrow><mrow><mrow><mi>exp</mi><mrow><mo>(</mo><mn>3</mn><mo>)</mo></mrow><mo>+</mo><mi>exp</mi><mrow><mo>(</mo><mn>1</mn><mo>)</mo></mrow></mrow></mrow></mfrac><mo>≈</mo><mn>0.881</mn><mo>,</mo><msub><mrow><mi>p</mi></mrow><mrow><mi>x</mi></mrow></msub><mrow><mo>(</mo><mn>2</mn><mo>)</mo></mrow><mo>≈</mo><mn>0.119</mn></mtd></mtr><mtr><mtd><msub><mrow><mi>g</mi></mrow><mrow><mi>w</mi></mrow></msub><mrow><mo>(</mo><mi>x</mi><mo>)</mo></mrow><mo>≈</mo><mn>0.881</mn><mrow><mo>(</mo><mo>−</mo><mn>10</mn><mo>)</mo></mrow><mo>+</mo><mn>0.119</mn><mrow><mo>(</mo><mn>10</mn><mo>)</mo></mrow><mo>≈</mo><mo>−</mo><mn>7.62</mn></mtd></mtr></mtable></math>

입니다. 기울기의 반대 방향으로 업데이트하므로 x를 증가시키게 됩니다. 현재 비용이 큰 시나리오 1의 비용을 국소적으로 줄이는 방향입니다. 실제 이동에서는 보폭과 설계 제약도 고려해야 합니다.

균등하게 뽑은 표본을 별도 가중치 없이 사용하면 평균 방향은

<math display="block" aria-label="Uniform sampling without reweighting cancels the two slopes"><mn>0.5</mn><mrow><mo>(</mo><mo>−</mo><mn>10</mn><mo>)</mo></mrow><mo>+</mo><mn>0.5</mn><mrow><mo>(</mo><mn>10</mn><mo>)</mo></mrow><mo>=</mo><mn>0</mn></math>

이 되어 두 기울기가 상쇄됩니다. 반복 횟수를 늘려도 원하는 가중합과 다른 평균을 더 정확하게 추정할 뿐입니다. 여기서 비교하는 것은 재가중하지 않은 표본 평균입니다. 균등 표본에 적절한 중요도 가중치를 곱하는 방법은 별도로 생각할 수 있습니다.

고정된 x에서 chain의 장기 방문 비율이 시나리오 1에 약 88.1%, 시나리오 2에 약 11.9%라면, 방문한 기울기의 단순 평균은 −7.62에 가까워집니다. 가중치를 매번 곱하는 계산을 방문 빈도로 구현하는 셈입니다. Metropolis 방식에서는 이동이 거절되어 같은 시나리오에 머문 반복도 평균에 포함해야 합니다.

## 2. 정상분포, 수렴 조건, 혼합 속도는 서로 다른 역할을 합니다

현재 설계에서의 전이행렬을 <math><msub><mrow><mi>P</mi></mrow><mrow><mi>x</mi></mrow></msub></math>라고 쓰면 정상분포 조건은

<math display="block" aria-label="Stationarity is invariance under one transition"><msub><mrow><mi>p</mi></mrow><mrow><mi>x</mi></mrow></msub><msub><mrow><mi>P</mi></mrow><mrow><mi>x</mi></mrow></msub><mo>=</mo><msub><mrow><mi>p</mi></mrow><mrow><mi>x</mi></mrow></msub></math>

입니다. 이미 <math><msub><mrow><mi>p</mi></mrow><mrow><mi>x</mi></mrow></msub></math>를 따르는 시나리오에서 한 번 전이했을 때도 같은 분포가 유지된다는 뜻입니다. 임의의 초기 시나리오에서 출발한 탐색이 그 분포에 도달하는지는 별도로 확인해야 합니다.

가령 전이행렬이 항등행렬이면,

<math display="block" aria-label="An identity transition matrix never changes the scenario"><msub><mrow><mi>P</mi></mrow><mrow><mi>x</mi></mrow></msub><mo>=</mo><mi>I</mi></math>

처음 선택한 시나리오에서 영원히 움직이지 않습니다. 모든 분포가 정상분포이지만 한 시나리오에 갇힌 경로로는 원하는 가중평균을 계산할 수 없습니다.

| 확인할 성질 | 확인하는 내용 |
|---|---|
| <math><msub><mrow><mi>p</mi></mrow><mrow><mi>x</mi></mrow></msub></math>가 정상분포인지 | 목표 가중치가 전이에 의해 보존되는지 |
| 기약성 등 수렴 조건 | 초기 시나리오와 무관하게 장기 방문 비율이 맞아지는지 |
| 혼합 속도(mixing rate) | 제한된 반복으로 현재 상태의 분포가 목표에 얼마나 가까워지는지 |

유한 상태공간에서 기약성은 하나의 경로를 따라 계산한 시간평균의 수렴을 뒷받침합니다. 각 시점의 상태 분포 자체가 정상분포로 수렴하려면 비주기성도 필요합니다. 두 수렴을 구분하는 설명은 Levin과 Peres의 [*Markov Chains and Mixing Times*, 정리 4.9와 부록 C](https://pages.uoregon.edu/dlevin/MARKOV/mcmt2e.pdf)에서 확인할 수 있습니다.

이 설명은 x를 고정했을 때의 이야기입니다. 설계를 업데이트하면 목표 분포 <math><msub><mrow><mi>p</mi></mrow><mrow><mi>x</mi></mrow></msub></math>도 움직입니다.

## 3. Chain이 충분히 섞이기 전에 설계를 바꾸면

직접적인 방법은 현재 x를 고정하고 chain을 충분히 돌린 뒤, 기울기의 평균으로 설계를 업데이트하는 것입니다. 설계가 바뀔 때마다 이 과정을 반복하면 계산량이 큽니다. 대신 한 번의 시나리오 전이와 한 번의 설계 업데이트를 번갈아 수행하는 방식을 생각할 수 있습니다.

<math display="block" aria-label="One Markov transition followed by one projected design update"><mtable columnalign="left"><mtr><mtd><msub><mrow><mi>I</mi></mrow><mrow><mrow><mi>n</mi><mo>+</mo><mn>1</mn></mrow></mrow></msub><mo>∼</mo><msub><mrow><mi>P</mi></mrow><mrow><msub><mrow><mi>x</mi></mrow><mrow><mi>n</mi></mrow></msub></mrow></msub><mrow><mo>(</mo><mrow><msub><mrow><mi>I</mi></mrow><mrow><mi>n</mi></mrow></msub><mo>,</mo><mo>·</mo></mrow><mo>)</mo></mrow></mtd></mtr><mtr><mtd><msub><mrow><mi>x</mi></mrow><mrow><mrow><mi>n</mi><mo>+</mo><mn>1</mn></mrow></mrow></msub><mo>=</mo><msub><mrow><mi>Π</mi></mrow><mrow><mi>X</mi></mrow></msub><mrow><mo>[</mo><msub><mrow><mi>x</mi></mrow><mrow><mi>n</mi></mrow></msub><mo>−</mo><msub><mrow><mi>α</mi></mrow><mrow><mrow><mi>n</mi><mo>+</mo><mn>1</mn></mrow></mrow></msub><mrow><mo>(</mo><msub><mrow><mi>g</mi></mrow><mrow><mi>f</mi></mrow></msub><mrow><mo>(</mo><msub><mrow><mi>x</mi></mrow><mrow><mi>n</mi></mrow></msub><mo>)</mo></mrow><mo>+</mo><msub><mrow><mi>g</mi></mrow><mrow><msub><mrow><mi>I</mi></mrow><mrow><mrow><mi>n</mi><mo>+</mo><mn>1</mn></mrow></mrow></msub></mrow></msub><mrow><mo>(</mo><msub><mrow><mi>x</mi></mrow><mrow><mi>n</mi></mrow></msub><mo>)</mo></mrow><mo>)</mo></mrow><mo>]</mo></mrow></mtd></mtr></mtable></math>

첫 줄은 현재 시나리오에서 한 번 전이하는 과정이고, 둘째 줄은 방문한 시나리오의 부분기울기로 설계를 바꾸는 과정입니다. Π는 결과를 <math><mi>X</mi></math>에 Euclidean projection하는 연산입니다. 다음 반복에서는 방금 방문한 시나리오에서 탐색을 이어갑니다.

이때 이어받는 것은 시나리오의 위치입니다. 설계가 바뀌면 같은 시나리오의 운영비용도 달라지므로, 수락확률은 현재 설계에서 평가한 비용으로 계산해야 합니다. 전이 한 번이 운영문제 풀이 한 번과 같다는 뜻도 아닙니다. 제안 시나리오와 현재 시나리오의 비용 평가 등이 필요할 수 있습니다.

이전 탐색이 첫 번째 목표 분포에 충분히 가까웠다고 합시다.

<math display="block" aria-label="A slowly changing target and a sharply changing target"><mtable columnalign="left"><mtr><mtd><msub><mrow><mi>p</mi></mrow><mrow><msub><mrow><mi>x</mi></mrow><mrow><mi>n</mi></mrow></msub></mrow></msub><mo>=</mo><mrow><mo>(</mo><mn>0.88</mn><mo>,</mo><mn>0.12</mn><mo>)</mo></mrow><mo>,</mo><msub><mrow><mi>p</mi></mrow><mrow><msub><mrow><mi>x</mi></mrow><mrow><mrow><mi>n</mi><mo>+</mo><mn>1</mn></mrow></mrow></msub></mrow></msub><mo>=</mo><mrow><mo>(</mo><mn>0.85</mn><mo>,</mo><mn>0.15</mn><mo>)</mo></mrow></mtd></mtr><mtr><mtd><msub><mrow><mi>p</mi></mrow><mrow><msub><mrow><mi>x</mi></mrow><mrow><mrow><mi>n</mi><mo>+</mo><mn>1</mn></mrow></mrow></msub></mrow></msub><mo>=</mo><mrow><mo>(</mo><mn>0.12</mn><mo>,</mo><mn>0.88</mn><mo>)</mo></mrow></mtd></mtr></mtable></math>

첫 줄처럼 (0.88, 0.12)에서 (0.85, 0.15)로 조금 바뀌었다면, 이전 탐색 상태는 새 목표에도 유용한 출발점입니다. 둘째 줄처럼 (0.12, 0.88)로 뒤집히면 이전에 자주 방문하던 시나리오가 덜 중요해집니다. Chain이 적응하는 동안 현재 설계에 맞지 않는 방향을 줄 수 있습니다.

따라서 chain이 현재 목표에 접근하는 속도와 설계 업데이트가 목표 분포를 바꾸는 속도를 함께 봐야 합니다. 표본 부분기울기의 크기에 상계 B가 있고 <math><msub><mrow><mi>x</mi></mrow><mrow><mi>n</mi></mrow></msub></math>이 <math><mi>X</mi></math> 안에 있다면, 투영의 비팽창성으로

<math display="block" aria-label="A bounded sampled subgradient limits the design movement"><mtable columnalign="left"><mtr><mtd><msub><mrow><mi>Z</mi></mrow><mrow><mrow><mi>n</mi><mo>+</mo><mn>1</mn></mrow></mrow></msub><mo>:=</mo><msub><mrow><mi>g</mi></mrow><mrow><mi>f</mi></mrow></msub><mrow><mo>(</mo><msub><mrow><mi>x</mi></mrow><mrow><mi>n</mi></mrow></msub><mo>)</mo></mrow><mo>+</mo><msub><mrow><mi>g</mi></mrow><mrow><msub><mrow><mi>I</mi></mrow><mrow><mrow><mi>n</mi><mo>+</mo><mn>1</mn></mrow></mrow></msub></mrow></msub><mrow><mo>(</mo><msub><mrow><mi>x</mi></mrow><mrow><mi>n</mi></mrow></msub><mo>)</mo></mrow><mo>,</mo><mrow><mo>‖</mo><msub><mrow><mi>Z</mi></mrow><mrow><mrow><mi>n</mi><mo>+</mo><mn>1</mn></mrow></mrow></msub><mo>‖</mo></mrow><mo>≤</mo><mi>B</mi></mtd></mtr><mtr><mtd><mrow><mo>‖</mo><msub><mrow><mi>x</mi></mrow><mrow><mrow><mi>n</mi><mo>+</mo><mn>1</mn></mrow></mrow></msub><mo>−</mo><msub><mrow><mi>x</mi></mrow><mrow><mi>n</mi></mrow></msub><mo>‖</mo></mrow><mo>≤</mo><msub><mrow><mi>α</mi></mrow><mrow><mrow><mi>n</mi><mo>+</mo><mn>1</mn></mrow></mrow></msub><mi>B</mi></mtd></mtr></mtable></math>

를 얻습니다. 보폭(step size)을 줄이면 설계 이동량도 제한됩니다. 고정된 w에서 운영비용이 설계에 대해 공통 Lipschitz 상계를 만족하면, softmax 가중치의 변화량도 설계 이동량으로 제어할 수 있습니다. 다만 작은 보폭만으로 충분한 추적을 보장하지는 않습니다. 전이의 혼합 특성도 함께 확인해야 합니다.

한 번 전이해 얻은 <math><msub><mrow><mi>I</mi></mrow><mrow><mrow><mi>n</mi><mo>+</mo><mn>1</mn></mrow></mrow></msub></math>는 일반적으로 <math><msub><mrow><mi>p</mi></mrow><mrow><msub><mrow><mi>x</mi></mrow><mrow><mi>n</mi></mrow></msub></mrow></msub></math>에서 정확히 뽑은 표본이 아닙니다. 따라서 <math><msub><mrow><mi>Z</mi></mrow><mrow><mrow><mi>n</mi><mo>+</mo><mn>1</mn></mrow></mrow></msub></math>를 조건부 불편향 SGD 추정량으로 취급할 수 없습니다. 수렴 분석에서는 이 오차가 반복 전체에 미치는 영향을 제어해야 합니다.

## 4. 최적해까지의 거리에서 표본 오차를 분리합니다

고정된 w에 대해 최소해가 존재한다고 가정하고 비교점을 잡습니다.

<math display="block" aria-label="A comparison optimizer for the fixed-temperature objective"><msup><mrow><mi>x</mi></mrow><mrow><mo>⋆</mo></mrow></msup><mo>∈</mo><mi>arg</mi><munder><mo>min</mo><mrow><mi>x</mi><mo>∈</mo><mi>X</mi></mrow></munder><msub><mrow><mi>F</mi></mrow><mrow><mi>w</mi></mrow></msub><mrow><mo>(</mo><mi>x</mi><mo>)</mo></mrow><mo>,</mo><msubsup><mi>F</mi><mi>w</mi><mo>⋆</mo></msubsup><mo>:=</mo><msub><mrow><mi>F</mi></mrow><mrow><mi>w</mi></mrow></msub><mrow><mo>(</mo><msup><mrow><mi>x</mi></mrow><mrow><mo>⋆</mo></mrow></msup><mo>)</mo></mrow></math>

<math><msup><mrow><mi>x</mi></mrow><mrow><mo>⋆</mo></mrow></msup></math>는 증명에 사용하는 값이며 알고리즘이 미리 알고 있는 설계는 아닙니다. Euclidean projection의 성질로 한 번의 업데이트 전후에

<math display="block" aria-label="The one-step squared-distance inequality"><mtable columnalign="left"><mtr><mtd><msup><mrow><mrow><mo>‖</mo><msub><mrow><mi>x</mi></mrow><mrow><mrow><mi>n</mi><mo>+</mo><mn>1</mn></mrow></mrow></msub><mo>−</mo><msup><mrow><mi>x</mi></mrow><mrow><mo>⋆</mo></mrow></msup><mo>‖</mo></mrow></mrow><mrow><mn>2</mn></mrow></msup><mo>≤</mo><msup><mrow><mrow><mo>‖</mo><msub><mrow><mi>x</mi></mrow><mrow><mi>n</mi></mrow></msub><mo>−</mo><msub><mrow><mi>α</mi></mrow><mrow><mrow><mi>n</mi><mo>+</mo><mn>1</mn></mrow></mrow></msub><msub><mrow><mi>Z</mi></mrow><mrow><mrow><mi>n</mi><mo>+</mo><mn>1</mn></mrow></mrow></msub><mo>−</mo><msup><mrow><mi>x</mi></mrow><mrow><mo>⋆</mo></mrow></msup><mo>‖</mo></mrow></mrow><mrow><mn>2</mn></mrow></msup></mtd></mtr><mtr><mtd><mo>=</mo><msup><mrow><mrow><mo>‖</mo><mrow><msub><mrow><mi>x</mi></mrow><mrow><mi>n</mi></mrow></msub><mo>−</mo><msup><mrow><mi>x</mi></mrow><mrow><mo>⋆</mo></mrow></msup></mrow><mo>‖</mo></mrow></mrow><mrow><mn>2</mn></mrow></msup><mo>−</mo><mn>2</mn><msub><mrow><mi>α</mi></mrow><mrow><mrow><mi>n</mi><mo>+</mo><mn>1</mn></mrow></mrow></msub><msup><mrow><msub><mrow><mi>Z</mi></mrow><mrow><mrow><mi>n</mi><mo>+</mo><mn>1</mn></mrow></mrow></msub></mrow><mrow><mo>⊤</mo></mrow></msup><mrow><mo>(</mo><mrow><msub><mrow><mi>x</mi></mrow><mrow><mi>n</mi></mrow></msub><mo>−</mo><msup><mrow><mi>x</mi></mrow><mrow><mo>⋆</mo></mrow></msup></mrow><mo>)</mo></mrow><mo>+</mo><msup><mrow><msub><mrow><mi>α</mi></mrow><mrow><mrow><mi>n</mi><mo>+</mo><mn>1</mn></mrow></mrow></msub></mrow><mrow><mn>2</mn></mrow></msup><msup><mrow><mrow><mo>‖</mo><msub><mrow><mi>Z</mi></mrow><mrow><mrow><mi>n</mi><mo>+</mo><mn>1</mn></mrow></mrow></msub><mo>‖</mo></mrow></mrow><mrow><mn>2</mn></mrow></msup></mtd></mtr></mtable></math>

가 성립합니다. 가운데 내적이 충분히 양수이면 거리 제곱을 줄이는 데 기여합니다. 정확한 부분기울기라면 볼록성으로 바로 목적함수 차이를 연결할 수 있습니다.

<math display="block" aria-label="An exact subgradient controls the objective gap"><mtable columnalign="left"><mtr><mtd><msub><mrow><mi>z</mi></mrow><mrow><mi>n</mi></mrow></msub><mo>∈</mo><mo>∂</mo><msub><mrow><mi>F</mi></mrow><mrow><mi>w</mi></mrow></msub><mrow><mo>(</mo><msub><mrow><mi>x</mi></mrow><mrow><mi>n</mi></mrow></msub><mo>)</mo></mrow></mtd></mtr><mtr><mtd><msup><mrow><msub><mrow><mi>z</mi></mrow><mrow><mi>n</mi></mrow></msub></mrow><mrow><mo>⊤</mo></mrow></msup><mrow><mo>(</mo><mrow><msub><mrow><mi>x</mi></mrow><mrow><mi>n</mi></mrow></msub><mo>−</mo><msup><mrow><mi>x</mi></mrow><mrow><mo>⋆</mo></mrow></msup></mrow><mo>)</mo></mrow><mo>≥</mo><mrow><msub><mrow><mi>F</mi></mrow><mrow><mi>w</mi></mrow></msub><mrow><mo>(</mo><msub><mrow><mi>x</mi></mrow><mrow><mi>n</mi></mrow></msub><mo>)</mo></mrow><mo>−</mo><msubsup><mi>F</mi><mi>w</mi><mo>⋆</mo></msubsup></mrow></mtd></mtr></mtable></math>

실제로 사용하는 <math><msub><mrow><mi>Z</mi></mrow><mrow><mrow><mi>n</mi><mo>+</mo><mn>1</mn></mrow></mrow></msub></math>에는 특정 시나리오의 정보만 들어 있으므로, 이 부등식을 그대로 적용할 수 없습니다. 시나리오별 비용 차이를

<math display="block" aria-label="Scenario-specific cost differences relative to the comparison design"><msub><mrow><mi>r</mi></mrow><mrow><mi>i</mi></mrow></msub><mrow><mo>(</mo><mi>x</mi><mo>)</mo></mrow><mo>:=</mo><mrow><msub><mrow><mi>Q</mi></mrow><mrow><mi>i</mi></mrow></msub><mrow><mo>(</mo><mi>x</mi><mo>)</mo></mrow><mo>−</mo><msub><mrow><mi>Q</mi></mrow><mrow><mi>i</mi></mrow></msub><mrow><mo>(</mo><msup><mrow><mi>x</mi></mrow><mrow><mo>⋆</mo></mrow></msup><mo>)</mo></mrow></mrow></math>

로 정의하겠습니다. <math><msup><mrow><mi>x</mi></mrow><mrow><mo>⋆</mo></mrow></msup></math>가 모든 시나리오를 각각 최적화하는 설계는 아니므로 개별 <math><msub><mrow><mi>r</mi></mrow><mrow><mi>i</mi></mrow></msub></math>(x)는 음수일 수도 있습니다. 이번에 방문한 시나리오의 비용 차이와 목표 분포에서 평균한 비용 차이의 차이를 표본 오차로 둡니다.

<math display="block" aria-label="The sampled cost difference minus its target-distribution average"><msub><mrow><mi>e</mi></mrow><mrow><mrow><mi>n</mi><mo>+</mo><mn>1</mn></mrow></mrow></msub><mo>:=</mo><msub><mrow><mi>r</mi></mrow><mrow><msub><mrow><mi>I</mi></mrow><mrow><mrow><mi>n</mi><mo>+</mo><mn>1</mn></mrow></mrow></msub></mrow></msub><mrow><mo>(</mo><msub><mrow><mi>x</mi></mrow><mrow><mi>n</mi></mrow></msub><mo>)</mo></mrow><mo>−</mo><munder><mo>∑</mo><mi>i</mi></munder><msub><mrow><mi>p</mi></mrow><mrow><msub><mrow><mi>x</mi></mrow><mrow><mi>n</mi></mrow></msub></mrow></msub><mrow><mo>(</mo><mi>i</mi><mo>)</mo></mrow><msub><mrow><mi>r</mi></mrow><mrow><mi>i</mi></mrow></msub><mrow><mo>(</mo><msub><mrow><mi>x</mi></mrow><mrow><mi>n</mi></mrow></msub><mo>)</mo></mrow></math>

현재까지의 이력을 조건으로 <math><msub><mrow><mi>I</mi></mrow><mrow><mrow><mi>n</mi><mo>+</mo><mn>1</mn></mrow></mrow></msub></math>를 정확히 <math><msub><mrow><mi>p</mi></mrow><mrow><msub><mrow><mi>x</mi></mrow><mrow><mi>n</mi></mrow></msub></mrow></msub></math>에서 뽑았다면 이 오차의 조건부 평균은 0입니다. 한 번의 Markov 전이에서는 이력을 ℱ로 표시할 때 일반적으로

<math display="block" aria-label="One Markov transition need not give zero conditional mean error"><mi>𝔼</mi><mrow><mo>[</mo><msub><mrow><mi>e</mi></mrow><mrow><mrow><mi>n</mi><mo>+</mo><mn>1</mn></mrow></mrow></msub><mo>|</mo><msub><mrow><mi>ℱ</mi></mrow><mrow><mi>n</mi></mrow></msub><mo>]</mo></mrow><mo>=</mo><munder><mo>∑</mo><mi>i</mi></munder><mrow><mo>(</mo><msub><mrow><mi>P</mi></mrow><mrow><msub><mrow><mi>x</mi></mrow><mrow><mi>n</mi></mrow></msub></mrow></msub><mrow><mo>(</mo><mrow><msub><mrow><mi>I</mi></mrow><mrow><mi>n</mi></mrow></msub><mo>,</mo><mi>i</mi></mrow><mo>)</mo></mrow><mo>−</mo><msub><mrow><mi>p</mi></mrow><mrow><msub><mrow><mi>x</mi></mrow><mrow><mi>n</mi></mrow></msub></mrow></msub><mrow><mo>(</mo><mi>i</mi><mo>)</mo></mrow><mo>)</mo></mrow><msub><mrow><mi>r</mi></mrow><mrow><mi>i</mi></mrow></msub><mrow><mo>(</mo><msub><mrow><mi>x</mi></mrow><mrow><mi>n</mi></mrow></msub><mo>)</mo></mrow><mo>≠</mo><mn>0</mn></math>

입니다. 마지막의 ≠ 0은 항상 0이 아니라는 뜻이며, 특정 이력에서는 0일 수도 있습니다. 이 오차는 기울기 벡터의 차이가 아니라 비용 차이로 정의한 스칼라입니다.

각 시나리오와 투자비의 볼록성은

<math display="block" aria-label="Convexity lower-bounds the sampled inner product"><msup><mrow><msub><mrow><mi>Z</mi></mrow><mrow><mrow><mi>n</mi><mo>+</mo><mn>1</mn></mrow></mrow></msub></mrow><mrow><mo>⊤</mo></mrow></msup><mrow><mo>(</mo><mrow><msub><mrow><mi>x</mi></mrow><mrow><mi>n</mi></mrow></msub><mo>−</mo><msup><mrow><mi>x</mi></mrow><mrow><mo>⋆</mo></mrow></msup></mrow><mo>)</mo></mrow><mo>≥</mo><mi>f</mi><mrow><mo>(</mo><msub><mrow><mi>x</mi></mrow><mrow><mi>n</mi></mrow></msub><mo>)</mo></mrow><mo>−</mo><mi>f</mi><mrow><mo>(</mo><msup><mrow><mi>x</mi></mrow><mrow><mo>⋆</mo></mrow></msup><mo>)</mo></mrow><mo>+</mo><msub><mrow><mi>r</mi></mrow><mrow><msub><mrow><mi>I</mi></mrow><mrow><mrow><mi>n</mi><mo>+</mo><mn>1</mn></mrow></mrow></msub></mrow></msub><mrow><mo>(</mo><msub><mrow><mi>x</mi></mrow><mrow><mi>n</mi></mrow></msub><mo>)</mo></mrow></math>

를 줍니다. 한편 mellowmax를 비용 벡터의 볼록함수로 보면 그 기울기는 <math><msub><mrow><mi>p</mi></mrow><mrow><mi>x</mi></mrow></msub></math>입니다. 현재 비용 벡터에서 지지 초평면 부등식을 적용하면

<math display="block" aria-label="Convexity of mellowmax as a function of the cost vector"><munder><mo>∑</mo><mi>i</mi></munder><msub><mrow><mi>p</mi></mrow><mrow><mi>x</mi></mrow></msub><mrow><mo>(</mo><mi>i</mi><mo>)</mo></mrow><mrow><mo>[</mo><mrow><msub><mrow><mi>Q</mi></mrow><mrow><mi>i</mi></mrow></msub><mrow><mo>(</mo><mi>x</mi><mo>)</mo></mrow><mo>−</mo><msub><mrow><mi>Q</mi></mrow><mrow><mi>i</mi></mrow></msub><mrow><mo>(</mo><msup><mrow><mi>x</mi></mrow><mrow><mo>⋆</mo></mrow></msup><mo>)</mo></mrow></mrow><mo>]</mo></mrow><mo>≥</mo><msub><mrow><mi>M</mi></mrow><mrow><mi>w</mi></mrow></msub><mrow><mo>(</mo><mi>x</mi><mo>)</mo></mrow><mo>−</mo><msub><mrow><mi>M</mi></mrow><mrow><mi>w</mi></mrow></msub><mrow><mo>(</mo><msup><mrow><mi>x</mi></mrow><mrow><mo>⋆</mo></mrow></msup><mo>)</mo></mrow></math>

가 성립합니다. 이 방향에 유의해야 합니다. 가중 비용 차이가 mellowmax 값의 차이를 위에서 감싸므로, 앞의 시나리오별 하한과 결합할 수 있습니다. Log-sum-exp의 볼록성과 지지 초평면 부등식은 Boyd와 Vandenberghe의 [*Convex Optimization*, 3장](https://web.stanford.edu/~boyd/cvxbook/)을 참고할 수 있습니다.

표본 오차의 정의를 대입하면

<math display="block" aria-label="The sampled direction controls the objective gap plus the error"><msup><mrow><msub><mrow><mi>Z</mi></mrow><mrow><mrow><mi>n</mi><mo>+</mo><mn>1</mn></mrow></mrow></msub></mrow><mrow><mo>⊤</mo></mrow></msup><mrow><mo>(</mo><mrow><msub><mrow><mi>x</mi></mrow><mrow><mi>n</mi></mrow></msub><mo>−</mo><msup><mrow><mi>x</mi></mrow><mrow><mo>⋆</mo></mrow></msup></mrow><mo>)</mo></mrow><mo>≥</mo><mrow><msub><mrow><mi>F</mi></mrow><mrow><mi>w</mi></mrow></msub><mrow><mo>(</mo><msub><mrow><mi>x</mi></mrow><mrow><mi>n</mi></mrow></msub><mo>)</mo></mrow><mo>−</mo><msubsup><mi>F</mi><mi>w</mi><mo>⋆</mo></msubsup></mrow><mo>+</mo><msub><mrow><mi>e</mi></mrow><mrow><mrow><mi>n</mi><mo>+</mo><mn>1</mn></mrow></mrow></msub></math>

를 얻습니다. <math><msub><mrow><mi>e</mi></mrow><mrow><mrow><mi>n</mi><mo>+</mo><mn>1</mn></mrow></mrow></msub></math>가 크게 음수이면 이번 시나리오는 목표 가중평균에 비해 현재 설계의 비용 차이를 작게 보여준 것입니다. 이 경우 거리 감소를 뒷받침하는 하한이 약해집니다.

## 5. 제어해야 하는 것은 보폭으로 가중한 누적 오차입니다

<math><msub><mrow><mi>Z</mi></mrow><mrow><mrow><mi>n</mi><mo>+</mo><mn>1</mn></mrow></mrow></msub></math>의 크기가 B 이하라는 가정과 앞의 내적 하한을 거리 변화식에 넣으면,

<math display="block" aria-label="Distance decrease, the quadratic term, and the signed sampling error"><mtable columnalign="left"><mtr><mtd><msub><mrow><mi>D</mi></mrow><mrow><mi>n</mi></mrow></msub><mo>:=</mo><msup><mrow><mrow><mo>‖</mo><mrow><msub><mrow><mi>x</mi></mrow><mrow><mi>n</mi></mrow></msub><mo>−</mo><msup><mrow><mi>x</mi></mrow><mrow><mo>⋆</mo></mrow></msup></mrow><mo>‖</mo></mrow></mrow><mrow><mn>2</mn></mrow></msup></mtd></mtr><mtr><mtd><mn>2</mn><msub><mrow><mi>α</mi></mrow><mrow><mrow><mi>n</mi><mo>+</mo><mn>1</mn></mrow></mrow></msub><mrow><mo>[</mo><mrow><msub><mrow><mi>F</mi></mrow><mrow><mi>w</mi></mrow></msub><mrow><mo>(</mo><msub><mrow><mi>x</mi></mrow><mrow><mi>n</mi></mrow></msub><mo>)</mo></mrow><mo>−</mo><msubsup><mi>F</mi><mi>w</mi><mo>⋆</mo></msubsup></mrow><mo>]</mo></mrow><mo>≤</mo><msub><mrow><mi>D</mi></mrow><mrow><mi>n</mi></mrow></msub><mo>−</mo><msub><mrow><mi>D</mi></mrow><mrow><mrow><mi>n</mi><mo>+</mo><mn>1</mn></mrow></mrow></msub><mo>+</mo><msup><mrow><msub><mrow><mi>α</mi></mrow><mrow><mrow><mi>n</mi><mo>+</mo><mn>1</mn></mrow></mrow></msub></mrow><mrow><mn>2</mn></mrow></msup><msup><mrow><mi>B</mi></mrow><mrow><mn>2</mn></mrow></msup><mo>−</mo><mn>2</mn><msub><mrow><mi>α</mi></mrow><mrow><mrow><mi>n</mi><mo>+</mo><mn>1</mn></mrow></mrow></msub><msub><mrow><mi>e</mi></mrow><mrow><mrow><mi>n</mi><mo>+</mo><mn>1</mn></mrow></mrow></msub></mtd></mtr></mtable></math>

입니다. 오른쪽에는 거리 제곱의 감소량, 유한한 보폭으로 움직이면서 생기는 이차항, 표본 오차의 영향이 남습니다. 여러 반복에 걸쳐 더하면 거리 항은 소거됩니다.

<math display="block" aria-label="Squared-distance terms telescope"><munderover><mo>∑</mo><mrow><mi>n</mi><mo>=</mo><mn>0</mn></mrow><mrow><mi>N</mi><mo>−</mo><mn>1</mn></mrow></munderover><mrow><mo>(</mo><msub><mrow><mi>D</mi></mrow><mrow><mi>n</mi></mrow></msub><mo>−</mo><msub><mrow><mi>D</mi></mrow><mrow><mrow><mi>n</mi><mo>+</mo><mn>1</mn></mrow></mrow></msub><mo>)</mo></mrow><mo>=</mo><msub><mrow><mi>D</mi></mrow><mrow><mn>0</mn></mrow></msub><mo>−</mo><msub><mrow><mi>D</mi></mrow><mrow><mi>N</mi></mrow></msub><mo>≤</mo><msub><mrow><mi>D</mi></mrow><mrow><mn>0</mn></mrow></msub></math>

초기 설계를 고정하고 기대값을 취하면

<math display="block" aria-label="The cumulative error that the Markov-chain analysis must control"><mtable columnalign="left"><mtr><mtd><mn>2</mn><munderover><mo>∑</mo><mrow><mi>n</mi><mo>=</mo><mn>0</mn></mrow><mrow><mi>N</mi><mo>−</mo><mn>1</mn></mrow></munderover><msub><mrow><mi>α</mi></mrow><mrow><mrow><mi>n</mi><mo>+</mo><mn>1</mn></mrow></mrow></msub><mi>𝔼</mi><mrow><mo>[</mo><mrow><msub><mrow><mi>F</mi></mrow><mrow><mi>w</mi></mrow></msub><mrow><mo>(</mo><msub><mrow><mi>x</mi></mrow><mrow><mi>n</mi></mrow></msub><mo>)</mo></mrow><mo>−</mo><msubsup><mi>F</mi><mi>w</mi><mo>⋆</mo></msubsup></mrow><mo>]</mo></mrow></mtd></mtr><mtr><mtd><mo>≤</mo><msub><mrow><mi>D</mi></mrow><mrow><mn>0</mn></mrow></msub><mo>+</mo><msup><mrow><mi>B</mi></mrow><mrow><mn>2</mn></mrow></msup><munderover><mo>∑</mo><mrow><mi>n</mi><mo>=</mo><mn>0</mn></mrow><mrow><mi>N</mi><mo>−</mo><mn>1</mn></mrow></munderover><msup><mrow><msub><mrow><mi>α</mi></mrow><mrow><mrow><mi>n</mi><mo>+</mo><mn>1</mn></mrow></mrow></msub></mrow><mrow><mn>2</mn></mrow></msup><mo>+</mo><mi>𝔼</mi><mrow><mo>[</mo><mo>−</mo><mn>2</mn><munderover><mo>∑</mo><mrow><mi>n</mi><mo>=</mo><mn>0</mn></mrow><mrow><mi>N</mi><mo>−</mo><mn>1</mn></mrow></munderover><msub><mrow><mi>α</mi></mrow><mrow><mrow><mi>n</mi><mo>+</mo><mn>1</mn></mrow></mrow></msub><msub><mrow><mi>e</mi></mrow><mrow><mrow><mi>n</mi><mo>+</mo><mn>1</mn></mrow></mrow></msub><mo>]</mo></mrow></mtd></mtr></mtable></math>

를 얻습니다. 각 <math><msub><mrow><mi>e</mi></mrow><mrow><mrow><mi>n</mi><mo>+</mo><mn>1</mn></mrow></mrow></msub></math>를 0으로 만들 필요는 없습니다. 마지막 누적 오차항이 보폭 합에 비해 충분히 느리게 커지도록 상계를 확보하면 됩니다.

예를 들어, N과 무관한 유한한 비음수 상수 <math><msub><mrow><mi>C</mi></mrow><mrow><mn>0</mn></mrow></msub></math>, <math><msub><mrow><mi>C</mi></mrow><mrow><mn>1</mn></mrow></msub></math>에 대해

<math display="block" aria-label="An additional cumulative-error bound, assumed for the rate derivation"><mi>𝔼</mi><mrow><mo>[</mo><mo>−</mo><mn>2</mn><munderover><mo>∑</mo><mrow><mi>n</mi><mo>=</mo><mn>0</mn></mrow><mrow><mi>N</mi><mo>−</mo><mn>1</mn></mrow></munderover><msub><mrow><mi>α</mi></mrow><mrow><mrow><mi>n</mi><mo>+</mo><mn>1</mn></mrow></mrow></msub><msub><mrow><mi>e</mi></mrow><mrow><mrow><mi>n</mi><mo>+</mo><mn>1</mn></mrow></mrow></msub><mo>]</mo></mrow><mo>≤</mo><msub><mrow><mi>C</mi></mrow><mrow><mn>0</mn></mrow></msub><mo>+</mo><msub><mrow><mi>C</mi></mrow><mrow><mn>1</mn></mrow></msub><munderover><mo>∑</mo><mrow><mi>n</mi><mo>=</mo><mn>0</mn></mrow><mrow><mi>N</mi><mo>−</mo><mn>1</mn></mrow></munderover><msup><mrow><msub><mrow><mi>α</mi></mrow><mrow><mrow><mi>n</mi><mo>+</mo><mn>1</mn></mrow></mrow></msub></mrow><mrow><mn>2</mn></mrow></msup></math>

를 증명할 수 있다고 가정하겠습니다. 이것은 정상분포의 존재만으로 따라오는 결과가 아닙니다. 설계에 따라 바뀌는 전이행렬의 혼합 성질, 설계 변화에 대한 정칙성, 보폭 조건 등을 사용해 별도로 증명해야 할 상계입니다. 상수는 고정된 w와 문제 및 chain의 특성에 의존할 수 있습니다.

Poisson 방정식을 이용한 오차 분해는 이 상계를 얻는 한 방법입니다. 중심화한 비용 차이를 전이 연산자에 대한 방정식으로 표현해 누적 오차를 다룹니다. 여기서는 그 방정식의 해에 필요한 상계와 정칙성을 증명하지 않았으므로, 아래 수렴률은 위 누적 오차 상계가 확보된다는 조건 아래에서 읽어야 합니다.

## 6. 가중평균 설계의 기대 목적함수 오차

업데이트 전 설계들의 보폭 가중평균을

<math display="block" aria-label="The stepsize-weighted average of pre-update designs"><msub><mrow><mover><mi>x</mi><mo>¯</mo></mover></mrow><mrow><mi>N</mi></mrow></msub><mo>:=</mo><mfrac><mrow><munderover><mo>∑</mo><mrow><mi>n</mi><mo>=</mo><mn>0</mn></mrow><mrow><mi>N</mi><mo>−</mo><mn>1</mn></mrow></munderover><msub><mrow><mi>α</mi></mrow><mrow><mrow><mi>n</mi><mo>+</mo><mn>1</mn></mrow></mrow></msub><msub><mrow><mi>x</mi></mrow><mrow><mi>n</mi></mrow></msub></mrow><mrow><munderover><mo>∑</mo><mrow><mi>n</mi><mo>=</mo><mn>0</mn></mrow><mrow><mi>N</mi><mo>−</mo><mn>1</mn></mrow></munderover><msub><mrow><mi>α</mi></mrow><mrow><mrow><mi>n</mi><mo>+</mo><mn>1</mn></mrow></mrow></msub></mrow></mfrac></math>

로 정의합니다. 보폭이 양수이고 <math><mi>X</mi></math>가 볼록하므로 이 평균도 <math><mi>X</mi></math>에 속합니다. <math><msub><mrow><mi>F</mi></mrow><mrow><mi>w</mi></mrow></msub></math>의 볼록성과 누적 오차 상계를 사용하면

<math display="block" aria-label="Expected objective error of the weighted average"><mtable columnalign="left"><mtr><mtd><mi>𝔼</mi><mrow><mo>[</mo><msub><mrow><mi>F</mi></mrow><mrow><mi>w</mi></mrow></msub><mrow><mo>(</mo><msub><mrow><mover><mi>x</mi><mo>¯</mo></mover></mrow><mrow><mi>N</mi></mrow></msub><mo>)</mo></mrow><mo>]</mo></mrow><mo>−</mo><msubsup><mi>F</mi><mi>w</mi><mo>⋆</mo></msubsup></mtd></mtr><mtr><mtd><mo>≤</mo><mfrac><mrow><mrow><msub><mrow><mi>D</mi></mrow><mrow><mn>0</mn></mrow></msub><mo>+</mo><msub><mrow><mi>C</mi></mrow><mrow><mn>0</mn></mrow></msub><mo>+</mo><mrow><mo>(</mo><msup><mrow><mi>B</mi></mrow><mrow><mn>2</mn></mrow></msup><mo>+</mo><msub><mrow><mi>C</mi></mrow><mrow><mn>1</mn></mrow></msub><mo>)</mo></mrow><munderover><mo>∑</mo><mrow><mi>n</mi><mo>=</mo><mn>0</mn></mrow><mrow><mi>N</mi><mo>−</mo><mn>1</mn></mrow></munderover><msup><mrow><msub><mrow><mi>α</mi></mrow><mrow><mrow><mi>n</mi><mo>+</mo><mn>1</mn></mrow></mrow></msub></mrow><mrow><mn>2</mn></mrow></msup></mrow></mrow><mrow><mrow><mn>2</mn><munderover><mo>∑</mo><mrow><mi>n</mi><mo>=</mo><mn>0</mn></mrow><mrow><mi>N</mi><mo>−</mo><mn>1</mn></mrow></munderover><msub><mrow><mi>α</mi></mrow><mrow><mrow><mi>n</mi><mo>+</mo><mn>1</mn></mrow></mrow></msub></mrow></mrow></mfrac></mtd></mtr></mtable></math>

를 얻습니다. 이제 분자와 분모의 성장 속도를 비교할 수 있습니다. 예를 들어

<math display="block" aria-label="Inverse-square-root stepsizes and the growth of their sums"><mtable columnalign="left"><mtr><mtd><msub><mrow><mi>α</mi></mrow><mrow><mrow><mi>n</mi><mo>+</mo><mn>1</mn></mrow></mrow></msub><mo>=</mo><mfrac><mrow><mi>a</mi></mrow><mrow><msqrt><mrow><mi>n</mi><mo>+</mo><mn>1</mn></mrow></msqrt></mrow></mfrac><mo>,</mo><mi>a</mi><mo>&gt;</mo><mn>0</mn></mtd></mtr><mtr><mtd><munderover><mo>∑</mo><mrow><mi>n</mi><mo>=</mo><mn>0</mn></mrow><mrow><mi>N</mi><mo>−</mo><mn>1</mn></mrow></munderover><msub><mrow><mi>α</mi></mrow><mrow><mrow><mi>n</mi><mo>+</mo><mn>1</mn></mrow></mrow></msub><mo>≍</mo><msqrt><mi>N</mi></msqrt><mo>,</mo><munderover><mo>∑</mo><mrow><mi>n</mi><mo>=</mo><mn>0</mn></mrow><mrow><mi>N</mi><mo>−</mo><mn>1</mn></mrow></munderover><msup><mrow><msub><mrow><mi>α</mi></mrow><mrow><mrow><mi>n</mi><mo>+</mo><mn>1</mn></mrow></mrow></msub></mrow><mrow><mn>2</mn></mrow></msup><mo>≍</mo><mi>log</mi><mi>N</mi></mtd></mtr></mtable></math>

입니다. 여기서 ≍는 N에 대한 성장 차수가 같다는 뜻입니다. w와 관련 상수들을 고정하면

<math display="block" aria-label="A conditional rate for the fixed-temperature averaged objective"><mi>𝔼</mi><mrow><mo>[</mo><msub><mrow><mi>F</mi></mrow><mrow><mi>w</mi></mrow></msub><mrow><mo>(</mo><msub><mrow><mover><mi>x</mi><mo>¯</mo></mover></mrow><mrow><mi>N</mi></mrow></msub><mo>)</mo></mrow><mo>]</mo></mrow><mo>−</mo><msubsup><mi>F</mi><mi>w</mi><mo>⋆</mo></msubsup><mo>=</mo><mi>O</mi><mrow><mo>(</mo><mfrac><mrow><mrow><mi>log</mi><mi>N</mi></mrow></mrow><mrow><msqrt><mi>N</mi></msqrt></mrow></mfrac><mo>)</mo></mrow><mo>→</mo><mn>0</mn></math>

가 됩니다. 이 결과는 가중평균 설계의 기대 목적함수 오차에 관한 것입니다. 매 반복의 비용 감소, 각 표본의 불편향성, 마지막 설계 자체의 수렴까지 보장하지는 않습니다. 또한 고정된 온도의 mellowmax 문제에 대한 결과이므로, 원래 최대비용 문제와의 근사 오차나 w를 줄일 때 달라지는 혼합 속도는 별도로 분석해야 합니다.
