---
layout: post
title: "Tolerance Ball Acquisition for Specification-Driven Inverse Design"
title_ko: "Specification-Driven Inverse Design를 위한 Tolerance Ball Acquisition"
date: 2026-06-30
category: llm-probabilistic-approaches
category_label: "LLM & Probabilistic Approaches"
research_group: algorithmic_reviews
research_category: llm-probabilistic-approaches
research_category_label: "LLM & Probabilistic Approaches"
application_category: ""
application_category_label: ""
method_category: "llm-probabilistic-approaches"
method_category_label: "LLM & Probabilistic Approaches"
paper_title: "Range-aware Bayesian optimization for discovering diverse designs within target property windows"
authors: "Jiang, S.; Wu, J.; Schroeder, C. M.; Webb, M. A."
venue: "arXiv"
year: "2026"
doi: ""
arxiv: "2606.11574v1"
source_url: "https://arxiv.org/abs/2606.11574v1"
tags:
  - "Bayesian optimization"
  - "inverse design"
  - "probabilistic search"
  - "Gaussian process"
  - "materials design"
  - "diversity"
excerpt: "A critical note on Tolerance Ball acquisition: a clean probability-of-feasibility objective for specification-driven inverse design, but not a direct optimizer of diversity, boundary coverage, or global feasible-set recovery."
excerpt_ko: "Specification-driven inverse design에서 Tolerance Ball acquisition을 비판적으로 읽는다. TB는 valid hit probability에는 잘 정렬되어 있지만 diversity, boundary coverage, global feasible-set recovery를 직접 최적화하지는 않는다."
language: "en-ko"
has_korean_note: false
---

The problem is not the usual Bayesian optimization problem of finding one best design. In many materials and process-design settings, the useful question is closer to this:

Find many designs x such that f(x) lies inside a target property window.

The target may be a glass-transition-temperature interval, a bandgap range, a viscosity window, or a molecular-weight-distribution profile that only needs to be close enough. Exact matching is rarely necessary. Once several candidates satisfy the specification, the real choice often depends on cost, synthesis difficulty, robustness, toxicity, scale-up risk, or operational convenience.

That makes the objective different from ordinary extremum search. Standard EI, PI, and UCB are designed to locate a maximum or minimum. Multi-objective Bayesian optimization usually searches for a Pareto frontier. But a specification window can contain many useful points that are Pareto-dominated and still practically valuable. The paper behind this note reframes the task as specification-driven inverse design: instead of asking for the best point, ask for a set of valid points.

## Why Standard BO Is Misaligned

In standard Bayesian optimization, the next design is chosen by maximizing an acquisition function over the current posterior. Expected Improvement, for example, rewards points that may improve on the current incumbent. That is sensible when the objective is a single best value.

For target-window discovery, this incentive can be wrong. If one feasible point has already been found, EI may keep searching nearby for a slightly better discrepancy rather than looking for other disconnected feasible regions. The method becomes good at local refinement, but not necessarily good at collecting many practically different valid designs.

Constrained BO is closer. Constrained EI often multiplies an improvement term by a probability of feasibility. But in that setting feasibility is still a side condition attached to an optimization objective. The Tolerance Ball idea removes the separate objective and makes the probability of satisfying the target window the acquisition itself.

So the acquisition is best read as a target-centered probability of feasibility.

That is a useful shift. It is also narrower than the phrase "discovering diverse designs" might suggest.

## The Tolerance Ball Objective

Let x be a design variable and f(x) be a K-dimensional property vector. A target vector y_tgt is given, and a design is valid if the predicted property lies inside a ball of radius epsilon around the target:

<math display="block" aria-label="Tolerance ball validity condition">
  <msup>
    <mrow>
      <mo>||</mo><mi>f</mi><mo>(</mo><mi>x</mi><mo>)</mo><mo>-</mo><msub><mi>y</mi><mtext>tgt</mtext></msub><mo>||</mo>
    </mrow>
    <mn>2</mn>
  </msup>
  <mo>&le;</mo>
  <msup><mi>&epsilon;</mi><mn>2</mn></msup><mo>.</mo>
</math>

With multiple targets, each target defines its own valid set. The paper uses a shared Gaussian-process posterior for the property map and then computes a target-specific acquisition for each target.

The architecture is simple. Independent GPs are fitted for the output dimensions. Their posterior means and variances are combined into an approximate multi-output Gaussian. The acquisition at a candidate x is the posterior probability that f(x) falls inside the tolerance ball.

Under the isotropic approximation

<math display="block" aria-label="Isotropic Gaussian approximation for multi-output posterior">
  <mi>f</mi><mo>(</mo><mi>x</mi><mo>)</mo><mo>|</mo><mi>D</mi>
  <mo>&approx;</mo>
  <mi>N</mi><mo>(</mo>
  <mi>&mu;</mi><mo>(</mo><mi>x</mi><mo>)</mo><mo>,</mo>
  <msup><mi>&eta;</mi><mn>2</mn></msup><mo>(</mo><mi>x</mi><mo>)</mo><mi>I</mi>
  <mo>)</mo><mo>,</mo>
</math>

where eta squared is the average of the output-wise posterior variances, the tolerance-ball probability can be computed with a noncentral chi-square CDF. This is the clean mathematical part of the method. It avoids posterior sampling and directly scores the next point by its probability of being valid.

## What TB Actually Optimizes

The acquisition is exactly aligned with a one-step utility:

<math display="block" aria-label="One step valid hit utility">
  <mi>u</mi><mo>(</mo><mi>x</mi><mo>)</mo>
  <mo>=</mo>
  <mn>1</mn>
  <mo>{</mo>
  <msup>
    <mrow>
      <mo>||</mo><mi>f</mi><mo>(</mo><mi>x</mi><mo>)</mo><mo>-</mo><msub><mi>y</mi><mtext>tgt</mtext></msub><mo>||</mo>
    </mrow>
    <mn>2</mn>
  </msup>
  <mo>&le;</mo>
  <msup><mi>&epsilon;</mi><mn>2</mn></msup>
  <mo>}</mo><mo>.</mo>
</math>

The expected value of this utility is the probability that the next evaluated point is valid. Maximizing the TB acquisition therefore maximizes the posterior probability of getting a valid hit in the next experiment.

That is a precise and defensible objective. If the goal is to harvest valid candidates quickly near a known target region, TB is well matched to the task.

But it does not optimize a long-horizon portfolio objective. It does not directly maximize coverage of the feasible set. It does not directly maximize chemical diversity, process diversity, or the number of disconnected feasible components discovered. Those goals would require terms that depend on previously found valid designs, distances between candidates, feasible-region geometry, or an explicit exploration policy.

This is the central distinction: TB is a valid-hit acquisition, not a diversity acquisition.

## Where Exploration Comes From

The paper discusses exploration-exploitation behavior, but TB does not reward uncertainty in the usual optimistic sense. In a one-dimensional target interval [a,b], the acquisition is the posterior probability mass inside the interval. If the posterior mean is already inside [a,b], reducing variance usually increases that probability. Large uncertainty spreads probability mass outside the target window.

Uncertainty helps only in a particular case: when the posterior mean is near the target but outside it, some uncertainty can push probability mass into the valid region. That is not global exploration. It is target-adjacent uncertainty exploitation.

This matters because inverse design often contains disconnected feasible islands. Suppose the valid set has several components, but the initial data are concentrated near one component. TB can keep selecting points around the known component because that region has the largest posterior probability of validity. Preventing exact duplicate measurements is not enough. In a continuous space, many near-duplicate candidates can still live in the same local basin.

So the method may collect many valid points without discovering the full structure of the valid set.

## Diversity Is Evaluated, Not Optimized

The most important limitation is that diversity appears mainly as an evaluation metric. In continuous domains, the paper uses a distance-based uniqueness notion. In discrete libraries, it counts distinct valid candidates. These are reasonable reporting metrics, but the acquisition itself does not include a diversity penalty or reward.

That creates an objective-metric mismatch. The method is evaluated by asking whether it found many separated valid designs, but the actual decision rule asks which next point has the highest posterior probability of being valid.

A direct diversity-seeking acquisition would need a term such as distance from previously found valid candidates, coverage of underexplored feasible regions, novelty in a molecular graph kernel, scaffold diversity, synthesis-route diversity, or another task-specific notion of difference. Without such a term, any observed diversity is indirect. It may come from posterior geometry, target multiplicity, finite-library structure, or the duplicate-avoidance rule.

This does not make TB useless. It just narrows the claim.

## Boundary Learning Is a Different Problem

TB also should not be confused with level-set estimation or contour learning. If the valid set is defined by a tolerance ball, the boundary is where the distance from the target equals epsilon. Near that boundary, the probability of validity can be around one half. In the interior, it can be close to one.

TB prefers the high-confidence interior. A boundary-learning method would deliberately sample near uncertain boundaries to learn the shape, volume, and extent of the feasible set. TB is closer to high-confidence valid-point harvesting.

This distinction is important in safety-critical or regulation-constrained settings. If one needs to map the boundary of the safe operating envelope, TB is not the right objective by itself. If one only needs additional candidates that are likely to satisfy a known specification, TB can be appropriate.

## High-Dimensional Outputs

The high-dimensional output case is delicate. In the molecular-weight-distribution example, the output can be a 100-dimensional compositional vector. Treating this as an ordinary Euclidean vector with independent output GPs and an isotropic covariance approximation is strong.

There are two problems.

First, tolerance-ball probability in high dimension can collapse rapidly as posterior uncertainty increases. Even when the posterior mean is exactly at the target, the probability mass inside a small ball shrinks sharply with dimension. In a 100-dimensional output space, TB can become strongly biased against uncertain regions.

Second, a molecular-weight distribution is compositional. Its bins sum to one, and the bins are correlated: increasing one bin usually forces decreases elsewhere. Independent output GPs and an isotropic covariance approximation ignore this structure. The closed-form acquisition is computationally convenient, but the approximation may not respect the geometry of the output.

This is not a small modeling detail. In high-dimensional correlated outputs, the acquisition can be dominated by the covariance approximation rather than by the real design question.

## What Is Valuable

The contribution is not that TB creates a completely new principle for Bayesian optimization. It is the combination that is useful:

specification-driven inverse design, a tolerance-region utility, a sampling-free multi-output acquisition, shared posterior learning across targets, and materials-oriented case studies.

The strongest practical idea is to stop pretending that the best point is always the right target. In many design problems, the engineer wants several candidates that satisfy a specification, then chooses among them using external criteria. TB expresses that immediate objective more honestly than an extremum-seeking acquisition.

The closed-form acquisition is also attractive. Methods that estimate feasible sets by posterior sampling can be expensive. A noncentral chi-square CDF is much cleaner, provided the Gaussian and isotropic assumptions are acceptable.

## Reading the Experiments

The reported benchmarks are broad: synthetic functions, pool-based materials datasets, polymerization design with molecular-weight-distribution targets, and sequence-defined oligomer libraries. The compared methods include TB, HV, EI, LCB, BAX, and random sampling. In the reported results, TB obtains the best average rank overall and strong diversity scores in the polymerization case.

That is meaningful evidence that the acquisition works well in the tested settings. The polymerization result is particularly useful from a process-design viewpoint: finding different reaction conditions that lead to similar target MWDs can give a real operator more flexibility.

But the benchmark design should be read carefully. In pool-based datasets, targets selected from the observed output distribution are known to be feasible after the fact. Real inverse design often starts from an external requirement: a market target, a device-level specification, or a regulatory threshold. Such targets may be far from the training distribution, sparsely feasible, or infeasible.

The oligomer case also shows a weaker regime for TB. When a finite library already contains many valid candidates, random sampling can be competitive for some targets and the method gap shrinks. That does not refute TB. It shows that its value depends on scarcity, model calibration, and the geometry of the candidate set.

## Assessment

The clean guarantee is narrow. If the posterior approximation is correct, TB computes the probability that a candidate lies inside the tolerance ball. And because that probability is the expected value of a valid-hit indicator, TB is exactly aligned with one-step valid-hit maximization.

What is not guaranteed is just as important: global feasible-set recovery, boundary coverage, disconnected-component discovery, batch diversity optimality, long-horizon portfolio diversity, regret bounds, or global convergence.

So the right reading is modest. TB is a good acquisition when the feasible region is at least partly known, the model is reasonably calibrated, and the goal is to collect valid candidates efficiently near target specifications. It is less convincing when the design space is unknown, feasible islands are sparse and disconnected, outputs are high-dimensional and correlated, or the actual goal is useful diversity rather than valid-hit rate.

## References

Jiang, S., Wu, J., Schroeder, C. M., & Webb, M. A. (2026). Range-aware Bayesian optimization for discovering diverse designs within target property windows (arXiv:2606.11574v1). arXiv.

<!-- ko -->

이 문제는 보통의 Bayesian optimization처럼 가장 좋은 설계 하나를 찾는 문제가 아니다. 많은 materials/process design에서는 더 현실적인 질문이 다음에 가깝다.

목표 물성 범위 안에 들어오는 여러 설계 x를 찾는 것.

목표는 glass-transition-temperature 구간일 수도 있고, bandgap 범위, viscosity window, 또는 molecular-weight-distribution profile일 수도 있다. 정확히 한 점을 맞출 필요는 별로 없다. 일정 tolerance 안에 들어오면 후보는 유효하다. 이후 실제 선택은 cost, synthesis difficulty, robustness, toxicity, scale-up risk, operational convenience 같은 추가 기준으로 이루어진다.

따라서 목적은 일반적인 extremum search와 다르다. 표준 EI, PI, UCB는 maximum 또는 minimum을 찾도록 설계되어 있다. Multi-objective Bayesian optimization도 보통 Pareto frontier를 찾는다. 하지만 specification window 안에는 Pareto-dominated이지만 실용적으로 가치 있는 후보가 많을 수 있다. 이 글에서 다루는 논문은 이 문제를 specification-driven inverse design으로 다시 정의한다. 가장 좋은 한 점이 아니라 valid point들의 집합을 찾자는 것이다.

## 표준 BO와 맞지 않는 지점

표준 Bayesian optimization에서는 현재 posterior 아래에서 acquisition function을 최대화하는 다음 설계를 고른다. Expected Improvement는 현재 incumbent보다 더 좋은 값을 낼 가능성을 보상한다. 단일 최적값을 찾는 문제라면 합리적이다.

Target-window discovery에서는 이 유인이 어긋날 수 있다. 이미 feasible point 하나를 찾은 뒤에도 EI는 그 주변에서 discrepancy를 조금 더 줄이려 할 수 있다. 서로 떨어진 다른 feasible region을 찾는 것보다 local refinement에 집중할 수 있다는 뜻이다.

Constrained BO는 이 문제에 더 가깝다. Constrained EI는 보통 improvement term에 feasibility probability를 곱한다. 하지만 이때도 feasibility는 optimization objective에 붙는 보조 조건이다. Tolerance Ball 접근은 별도의 objective를 없애고 target window를 만족할 posterior probability 자체를 acquisition으로 둔다.

따라서 이 acquisition은 target-centered probability of feasibility로 읽는 것이 가장 정확하다.

이 전환은 유용하다. 동시에 "diverse designs discovery"라는 표현이 암시하는 것보다는 좁다.

## Tolerance Ball 목적

설계변수를 x, K-dimensional property vector를 f(x)라고 하자. Target vector y_tgt가 주어지고, 반지름 epsilon의 ball 안에 예측 물성이 들어오면 valid design으로 본다.

<math display="block" aria-label="Tolerance ball validity condition">
  <msup>
    <mrow>
      <mo>||</mo><mi>f</mi><mo>(</mo><mi>x</mi><mo>)</mo><mo>-</mo><msub><mi>y</mi><mtext>tgt</mtext></msub><mo>||</mo>
    </mrow>
    <mn>2</mn>
  </msup>
  <mo>&le;</mo>
  <msup><mi>&epsilon;</mi><mn>2</mn></msup><mo>.</mo>
</math>

Target이 여러 개라면 각 target은 자기 valid set을 정의한다. 논문은 property map에 대해 shared Gaussian-process posterior를 사용하고, target마다 별도의 acquisition을 계산한다.

구조는 단순하다. Output dimension별 independent GP를 학습한다. Posterior mean과 variance를 합쳐 approximate multi-output Gaussian을 만든다. Candidate x에서 acquisition은 f(x)가 tolerance ball 안에 들어갈 posterior probability다.

다음 isotropic approximation 아래에서

<math display="block" aria-label="Isotropic Gaussian approximation for multi-output posterior">
  <mi>f</mi><mo>(</mo><mi>x</mi><mo>)</mo><mo>|</mo><mi>D</mi>
  <mo>&approx;</mo>
  <mi>N</mi><mo>(</mo>
  <mi>&mu;</mi><mo>(</mo><mi>x</mi><mo>)</mo><mo>,</mo>
  <msup><mi>&eta;</mi><mn>2</mn></msup><mo>(</mo><mi>x</mi><mo>)</mo><mi>I</mi>
  <mo>)</mo><mo>,</mo>
</math>

여기서 eta squared는 output-wise posterior variance의 평균이다. 이때 tolerance-ball probability는 noncentral chi-square CDF로 계산된다. 이 부분이 방법의 수학적으로 깔끔한 지점이다. Posterior sampling 없이 다음 점이 valid일 확률을 직접 점수화한다.

## TB가 실제로 최적화하는 것

이 acquisition은 one-step utility와 정확히 정렬되어 있다.

<math display="block" aria-label="One step valid hit utility">
  <mi>u</mi><mo>(</mo><mi>x</mi><mo>)</mo>
  <mo>=</mo>
  <mn>1</mn>
  <mo>{</mo>
  <msup>
    <mrow>
      <mo>||</mo><mi>f</mi><mo>(</mo><mi>x</mi><mo>)</mo><mo>-</mo><msub><mi>y</mi><mtext>tgt</mtext></msub><mo>||</mo>
    </mrow>
    <mn>2</mn>
  </msup>
  <mo>&le;</mo>
  <msup><mi>&epsilon;</mi><mn>2</mn></msup>
  <mo>}</mo><mo>.</mo>
</math>

이 utility의 기대값은 다음 평가점이 valid일 확률이다. 따라서 TB acquisition을 최대화하는 것은 다음 실험에서 valid hit를 얻을 posterior probability를 최대화하는 것과 같다.

이는 정확하고 방어 가능한 목적이다. 목표 region 근처에서 valid candidate를 빠르게 수확하는 것이 목표라면 TB는 문제와 잘 맞는다.

하지만 이것은 long-horizon portfolio objective가 아니다. Feasible set의 coverage를 직접 최대화하지 않는다. Chemical diversity, process diversity, disconnected feasible component의 발견 수를 직접 최대화하지도 않는다. 그런 목표에는 이전에 찾은 valid design과의 거리, feasible-region geometry, 또는 명시적 exploration policy에 의존하는 항이 필요하다.

핵심 구분은 이것이다. TB는 valid-hit acquisition이지 diversity acquisition이 아니다.

## 탐험은 어디서 생기는가

논문은 exploration-exploitation behavior를 논의하지만, TB는 일반적인 optimistic acquisition처럼 uncertainty를 직접 보상하지 않는다. 1차원 target interval [a,b]를 생각하면 acquisition은 posterior probability mass가 interval 안에 들어갈 확률이다. Posterior mean이 이미 [a,b] 안에 있으면 variance가 줄어들수록 그 확률은 보통 커진다. Uncertainty가 크면 probability mass가 target window 밖으로 퍼진다.

Uncertainty가 도움이 되는 경우는 제한적이다. Posterior mean이 target 근처이지만 밖에 있을 때, 일부 uncertainty가 확률질량을 valid region 안으로 밀어 넣을 수 있다. 이것은 global exploration이라기보다 target-adjacent uncertainty exploitation에 가깝다.

이 점은 inverse design에서 중요하다. Valid set이 여러 disconnected island로 구성될 수 있기 때문이다. 초기 데이터가 한 component 주변에 몰려 있으면 TB는 그 이미 알려진 component 주변을 계속 선택할 수 있다. 그곳에서 posterior probability of validity가 가장 높기 때문이다. 정확히 같은 후보를 다시 측정하지 못하게 하는 것만으로는 충분하지 않다. Continuous space에서는 같은 local basin 안에 서로 매우 가까운 후보가 무한히 많을 수 있다.

따라서 이 방법은 많은 valid point를 모으면서도 valid set의 전체 구조는 발견하지 못할 수 있다.

## Diversity는 평가되지만 최적화되지는 않는다

가장 중요한 한계는 diversity가 주로 evaluation metric으로 등장한다는 점이다. Continuous domain에서는 distance-based uniqueness를 쓰고, discrete library에서는 distinct valid candidate 수를 센다. 보고 지표로는 합리적이다. 하지만 acquisition 자체에는 diversity penalty나 reward가 없다.

이 때문에 objective-metric mismatch가 생긴다. 평가는 서로 떨어진 valid design을 많이 찾았는지를 묻지만, 실제 의사결정 규칙은 현재 valid probability가 가장 높은 다음 점을 고른다.

진짜 diversity-seeking acquisition이 되려면 이전 valid candidate와의 거리, underexplored feasible region의 coverage, molecular graph kernel상의 novelty, scaffold diversity, synthesis-route diversity, 또는 과제별 차이 척도를 포함해야 한다. 이런 항이 없다면 관찰된 diversity는 간접적이다. Posterior geometry, 여러 target의 존재, finite-library structure, duplicate-avoidance rule에서 생길 수 있다.

이것이 TB를 무용하게 만들지는 않는다. 다만 주장을 좁힌다.

## Boundary learning은 다른 문제다

TB는 level-set estimation이나 contour learning과도 다르다. Valid set이 tolerance ball로 정의된다면 boundary는 target으로부터의 거리가 epsilon인 지점이다. Boundary 근처에서 probability of validity는 대략 0.5가 될 수 있다. Interior에서는 1에 가까워질 수 있다.

TB는 high-confidence interior를 선호한다. Boundary-learning method라면 feasible set의 shape, volume, extent를 학습하기 위해 uncertain boundary 근처를 의도적으로 샘플링한다. TB는 high-confidence valid-point harvesting에 더 가깝다.

이 구분은 safety-critical 또는 regulation-constrained setting에서 중요하다. Safe operating envelope의 boundary를 알아야 한다면 TB 하나만으로는 맞지 않는다. 이미 어느 정도 알려진 specification을 만족하는 후보를 추가로 모으는 것이 목표라면 TB는 적절할 수 있다.

## 고차원 output 문제

High-dimensional output에서는 문제가 더 민감해진다. Molecular-weight-distribution 예에서는 output이 100-dimensional compositional vector일 수 있다. 이를 ordinary Euclidean vector로 보고 independent output GP와 isotropic covariance approximation을 적용하는 것은 강한 가정이다.

문제는 두 가지다.

첫째, 고차원에서 tolerance-ball probability는 posterior uncertainty가 조금만 커져도 급격히 작아질 수 있다. Posterior mean이 target에 정확히 있어도 작은 ball 안에 들어가는 probability mass는 dimension이 커질수록 빠르게 줄어든다. 100-dimensional output space에서는 TB가 uncertain region을 강하게 회피할 수 있다.

둘째, molecular-weight distribution은 compositional output이다. Bin들의 합은 1이고, bin들은 서로 상관되어 있다. 어떤 bin이 증가하면 다른 bin은 감소해야 한다. Independent output GP와 isotropic covariance approximation은 이 구조를 무시한다. Closed-form acquisition은 계산상 편리하지만, output geometry를 제대로 반영하지 못할 수 있다.

이것은 작은 modeling detail이 아니다. High-dimensional correlated output에서는 acquisition이 실제 design question보다 covariance approximation에 의해 지배될 수 있다.

## 무엇이 가치 있는가

이 논문의 기여는 완전히 새로운 BO 원리를 만들었다는 데 있지 않다. 유용한 것은 다음 조합이다.

Specification-driven inverse design, tolerance-region utility, sampling-free multi-output acquisition, target들 사이의 shared posterior learning, materials-oriented case study.

가장 강한 실용적 아이디어는 "best point"가 항상 올바른 목표가 아니라는 점을 분명히 한 것이다. 많은 설계 문제에서 연구자는 specification을 만족하는 여러 후보를 얻은 뒤, 외부 기준으로 그중 하나를 고른다. TB는 extremum-seeking acquisition보다 이 즉각적인 목표를 더 솔직하게 표현한다.

Closed-form acquisition도 매력적이다. Posterior sampling으로 feasible set을 추정하는 방법은 비쌀 수 있다. Gaussian과 isotropic assumption이 받아들일 만하다면 noncentral chi-square CDF는 훨씬 깔끔하다.

## 실험을 읽는 법

보고된 benchmark는 넓다. Synthetic functions, pool-based materials datasets, molecular-weight-distribution target을 갖는 polymerization design, sequence-defined oligomer libraries가 포함된다. 비교 대상은 TB, HV, EI, LCB, BAX, random sampling이다. 보고된 결과에서 TB는 전체 average rank가 가장 좋고 polymerization case에서 강한 diversity score를 보인다.

이는 테스트된 설정에서 acquisition이 잘 작동했다는 의미 있는 근거다. Polymerization 결과는 공정 설계 관점에서 특히 유용하다. 서로 다른 reaction condition이 유사한 target MWD를 만들 수 있다면 실제 운영자는 더 많은 유연성을 갖는다.

하지만 benchmark design은 조심해서 읽어야 한다. Pool-based dataset에서 observed output distribution을 본 뒤 target을 고르면, 그 target은 사후적으로 feasible하다는 것을 이미 알고 있는 셈이다. 실제 inverse design은 보통 외부 요구에서 출발한다. Market target, device-level specification, regulatory threshold가 먼저 주어진다. 이런 target은 training distribution에서 멀거나, sparse하게 feasible하거나, 아예 infeasible할 수 있다.

Oligomer case는 TB의 약한 regime도 보여준다. Finite library에 valid candidate가 이미 충분히 많으면 일부 target에서는 random sampling도 경쟁력이 있고 method gap이 줄어든다. 이것은 TB를 반박하지 않는다. 다만 TB의 가치는 scarcity, model calibration, candidate set geometry에 의존한다는 뜻이다.

## 평가

깔끔하게 보장되는 것은 좁다. Posterior approximation이 맞다면 TB는 candidate가 tolerance ball 안에 들어갈 확률을 계산한다. 그리고 그 확률은 valid-hit indicator의 expected value이므로, TB는 one-step valid-hit maximization과 정확히 정렬되어 있다.

반대로 보장되지 않는 부분도 중요하다. Global feasible-set recovery, boundary coverage, disconnected-component discovery, batch diversity optimality, long-horizon portfolio diversity, regret bound, global convergence는 보장되지 않는다.

따라서 가장 정확한 독해는 겸손하다. TB는 feasible region이 어느 정도 알려져 있고, model이 reasonably calibrated되어 있으며, target specification 근처에서 valid candidate를 효율적으로 모으는 것이 목표일 때 좋은 acquisition이다. 반대로 design space가 알려져 있지 않고, feasible island가 sparse하고 disconnected되어 있으며, output이 high-dimensional correlated structure를 갖거나, 실제 목표가 valid-hit rate가 아니라 useful diversity라면 설득력이 약해진다.

## 참고문헌

Jiang, S., Wu, J., Schroeder, C. M., & Webb, M. A. (2026). Range-aware Bayesian optimization for discovering diverse designs within target property windows (arXiv:2606.11574v1). arXiv.
