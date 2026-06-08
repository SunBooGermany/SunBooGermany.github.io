---
layout: post
title: "ORACLE: Near-Optimal Exploration as Certified Set Approximation"
title_ko: "ORACLE: near-optimal 탐색을 certified set approximation으로 바꾸기"
date: 2026-06-08
category: stochastic-nonlinear-optimization
category_label: "Stochastic & Nonlinear Optimization"
research_group: algorithmic_reviews
research_category: stochastic-nonlinear-optimization
research_category_label: "Stochastic & Nonlinear Optimization"
application_category: ""
application_category_label: ""
method_category: "stochastic-nonlinear-optimization"
method_category_label: "Stochastic & Nonlinear Optimization"
paper_title: ""
authors: ""
venue: ""
year: ""
doi: ""
arxiv: ""
source_url: ""
tags:
  - "near-optimality"
  - "MGA"
  - "set approximation"
  - "energy system optimization"
  - "convex optimization"
  - "outer approximation"
excerpt: "A note on ORACLE, which turns near-optimal energy-system exploration from point generation into an inner/outer approximation problem with a certified distance metric."
excerpt_ko: "near-optimal energy-system exploration을 단순한 point generation이 아니라 inner/outer approximation과 certified distance metric의 문제로 바꾸는 ORACLE에 대한 정리."
language: "en-ko"
has_korean_note: false
---

In fact, this paper is a very sophisticated method for finding the convex near-optimal solution space of a linear-programming energy system. It is therefore not a natural fit for Stochastic & Nonlinear Optimization. Still, I am writing this review because the paper contains ideas that are too original, precise, and frankly lovely not to record and share.

The main contribution is not a new energy-system optimization model. The model is still a large LP, and the near-optimal set is defined by the usual cost-budget constraint. The contribution is the reframing: near-optimal exploration is treated as a geometry problem.

Classical Modelling to Generate Alternatives (MGA) mostly follows this philosophy:

> Choose several directions and solve optimization problems to obtain diverse points.

ORACLE follows a different philosophy:

> Maintain inner and outer approximations of the near-optimal region, then reduce the largest approximation error.

That difference is not cosmetic. MGA is centered on solution generation. ORACLE is centered on set approximation and certified convergence.

## The Region Being Approximated

Start from a cost-optimal LP,

<math display="block" aria-label="Linear program cost optimum">
  <msup><mi>v</mi><mo>*</mo></msup>
  <mo>=</mo>
  <munder><mi>min</mi><mi>x</mi></munder>
  <mspace width="0.4em"></mspace>
  <msup><mi>c</mi><mo>&top;</mo></msup><mi>x</mi>
  <mspace width="1em"></mspace>
  <mtext>subject to</mtext>
  <mspace width="0.4em"></mspace>
  <mi>A</mi><mi>x</mi><mo>&le;</mo><mi>b</mi><mo>,</mo>
  <mspace width="0.4em"></mspace>
  <mi>F</mi><mi>x</mi><mo>=</mo><mi>d</mi><mo>.</mo>
</math>

The full vector <math><mi>x</mi></math> may contain capacity, dispatch, storage operation, import/export, and many other decisions. But the analyst usually wants to understand only a smaller set of design variables,

<math display="block" aria-label="Projection from full decision to design variables">
  <mi>z</mi><mo>=</mo><mi>S</mi><mi>x</mi><mo>.</mo>
</math>

The near-optimal region in this projected design space is

<math display="block" aria-label="Projected near optimal region">
  <msub><mi>Z</mi><mi>&epsilon;</mi></msub>
  <mo>=</mo>
  <mrow>
    <mo>{</mo>
    <mi>z</mi><mo>:</mo>
    <mo>&exist;</mo><mi>x</mi><mo>,</mo>
    <mspace width="0.3em"></mspace>
    <mi>S</mi><mi>x</mi><mo>=</mo><mi>z</mi><mo>,</mo>
    <mspace width="0.3em"></mspace>
    <mi>A</mi><mi>x</mi><mo>&le;</mo><mi>b</mi><mo>,</mo>
    <mspace width="0.3em"></mspace>
    <mi>F</mi><mi>x</mi><mo>=</mo><mi>d</mi><mo>,</mo>
    <mspace width="0.3em"></mspace>
    <msup><mi>c</mi><mo>&top;</mo></msup><mi>x</mi>
    <mo>&le;</mo>
    <msup><mi>v</mi><mo>*</mo></msup><mo>(</mo><mn>1</mn><mo>+</mo><mi>&epsilon;</mi><mo>)</mo>
    <mo>}</mo>
  </mrow>
  <mo>.</mo>
</math>

This set matters because a policy maker or system planner rarely cares only about the unique cheapest solution. A design that is 5% or 10% more expensive may be preferred because of political feasibility, social acceptance, supply-chain risk, regional fairness, or technology preference. These factors are often not explicit in the LP, but they matter after the optimization result leaves the model.

## Why Ordinary MGA Is Not Enough

Standard MGA repeatedly solves problems of the form

<math display="block" aria-label="MGA directional search">
  <munder><mi>min</mi><mrow><mi>x</mi><mo>,</mo><mi>z</mi></mrow></munder>
  <mspace width="0.4em"></mspace>
  <msubsup><mi>w</mi><mi>k</mi><mo>&top;</mo></msubsup><mi>z</mi>
  <mspace width="1em"></mspace>
  <mtext>subject to</mtext>
  <mspace width="0.4em"></mspace>
  <mi>S</mi><mi>x</mi><mo>=</mo><mi>z</mi><mo>,</mo>
  <mspace width="0.3em"></mspace>
  <mi>A</mi><mi>x</mi><mo>&le;</mo><mi>b</mi><mo>,</mo>
  <mspace width="0.3em"></mspace>
  <mi>F</mi><mi>x</mi><mo>=</mo><mi>d</mi><mo>,</mo>
  <mspace width="0.3em"></mspace>
  <msup><mi>c</mi><mo>&top;</mo></msup><mi>x</mi>
  <mo>&le;</mo>
  <msup><mi>v</mi><mo>*</mo></msup><mo>(</mo><mn>1</mn><mo>+</mo><mi>&epsilon;</mi><mo>)</mo><mo>.</mo>
</math>

Each iteration chooses a direction <math><msub><mi>w</mi><mi>k</mi></msub></math> and finds an extreme near-optimal design in that direction. Random MGA, VMM, HSJ, SPORES, ERG, and Manhattan-style variants differ in how they choose the directions or encourage diversity. But the common weakness remains: they generate points, not a certified approximation of the set.

A point cloud can look diverse and still miss a large part of <math><msub><mi>Z</mi><mi>&epsilon;</mi></msub></math>. Worse, the user does not know how much was missed.

MAA moves closer to a region-based method by using a convex hull, but explicit convex-hull facet computation becomes expensive in moderate dimension. ORACLE avoids this by using the convex hull in convex-combination form rather than explicit halfspace form.

## The Core ORACLE Invariant

ORACLE maintains a sandwich:

<math display="block" aria-label="Inner outer sandwich">
  <msub><mi>I</mi><mi>k</mi></msub>
  <mo>&subseteq;</mo>
  <msub><mi>Z</mi><mi>&epsilon;</mi></msub>
  <mo>&subseteq;</mo>
  <msub><mi>O</mi><mi>k</mi></msub>
  <mo>.</mo>
</math>

The inner approximation <math><msub><mi>I</mi><mi>k</mi></msub></math> is the convex hull of known near-optimal points:

<math display="block" aria-label="Inner approximation convex combination">
  <msub><mi>I</mi><mi>k</mi></msub>
  <mo>=</mo>
  <mrow>
    <mo>{</mo>
    <msub><mi>Z</mi><mi>k</mi></msub><mi>&lambda;</mi>
    <mo>:</mo>
    <msup><mn>1</mn><mo>&top;</mo></msup><mi>&lambda;</mi><mo>=</mo><mn>1</mn><mo>,</mo>
    <mspace width="0.3em"></mspace>
    <mi>&lambda;</mi><mo>&ge;</mo><mn>0</mn>
    <mo>}</mo>
  </mrow>
  <mo>,</mo>
</math>

where the columns of <math><msub><mi>Z</mi><mi>k</mi></msub></math> are the near-optimal points already found. The outer approximation <math><msub><mi>O</mi><mi>k</mi></msub></math> is an intersection of valid halfspaces that must contain the true region.

The distance between the two approximations is

<math display="block" aria-label="Max min distance between outer and inner approximations">
  <msub><mi>d</mi><mi>k</mi></msub>
  <mo>=</mo>
  <munder><mi>max</mi><mrow><msup><mi>z</mi><mi>O</mi></msup><mo>&isin;</mo><msub><mi>O</mi><mi>k</mi></msub></mrow></munder>
  <mspace width="0.3em"></mspace>
  <munder><mi>min</mi><mrow><msup><mi>z</mi><mi>I</mi></msup><mo>&isin;</mo><msub><mi>I</mi><mi>k</mi></msub></mrow></munder>
  <mspace width="0.3em"></mspace>
  <msub>
    <mrow><mo>&Vert;</mo><msup><mi>z</mi><mi>O</mi></msup><mo>-</mo><msup><mi>z</mi><mi>I</mi></msup><mo>&Vert;</mo></mrow>
    <mi>&infin;</mi>
  </msub>
  <mo>.</mo>
</math>

This is the clever convergence metric. If the exploratory variables are capacity variables measured in GW, then <math><msub><mi>d</mi><mi>k</mi></msub><mo>=</mo><mn>0.1</mn></math> GW means the worst remaining coordinate-wise approximation error is at most 0.1 GW. That is much more interpretable than a volume gap.

## Step 2: Find the Most Suspicious Outer Point

Step 2 asks:

> Where is the current outer approximation farthest from what we have already certified?

Using the convex-combination form of the inner hull, the abstract problem is

<math display="block" aria-label="Step 2 max min formulation">
  <msub><mi>d</mi><mi>k</mi></msub>
  <mo>=</mo>
  <munder><mi>max</mi><mrow><msup><mi>z</mi><mi>O</mi></msup><mo>&isin;</mo><msub><mi>O</mi><mi>k</mi></msub></mrow></munder>
  <mspace width="0.3em"></mspace>
  <munder><mi>min</mi><mrow><mi>&lambda;</mi><mo>&ge;</mo><mn>0</mn><mo>,</mo><msup><mn>1</mn><mo>&top;</mo></msup><mi>&lambda;</mi><mo>=</mo><mn>1</mn></mrow></munder>
  <mspace width="0.3em"></mspace>
  <msub>
    <mrow><mo>&Vert;</mo><msup><mi>z</mi><mi>O</mi></msup><mo>-</mo><msub><mi>Z</mi><mi>k</mi></msub><mi>&lambda;</mi><mo>&Vert;</mo></mrow>
    <mi>&infin;</mi>
  </msub>
  <mo>.</mo>
</math>

The order of max and min is essential. For each candidate outer point <math><msup><mi>z</mi><mi>O</mi></msup></math>, the lower problem computes its true shortest distance to the current inner hull. Then the upper problem chooses the outer point whose shortest distance is largest.

For a fixed <math><msup><mi>z</mi><mi>O</mi></msup></math>, the lower-level distance can be written as an LP:

<math display="block" aria-label="Infinity norm distance to inner hull">
  <munder><mi>min</mi><mrow><mi>&lambda;</mi><mo>,</mo><mi>&rho;</mi></mrow></munder>
  <mspace width="0.4em"></mspace>
  <mi>&rho;</mi>
  <mspace width="1em"></mspace>
  <mtext>subject to</mtext>
  <mspace width="0.4em"></mspace>
  <mo>-</mo><mi>&rho;</mi><mn>1</mn>
  <mo>&le;</mo>
  <msup><mi>z</mi><mi>O</mi></msup><mo>-</mo><msub><mi>Z</mi><mi>k</mi></msub><mi>&lambda;</mi>
  <mo>&le;</mo>
  <mi>&rho;</mi><mn>1</mn><mo>,</mo>
  <mspace width="0.3em"></mspace>
  <msup><mn>1</mn><mo>&top;</mo></msup><mi>&lambda;</mi><mo>=</mo><mn>1</mn><mo>,</mo>
  <mspace width="0.3em"></mspace>
  <mi>&lambda;</mi><mo>&ge;</mo><mn>0</mn><mo>.</mo>
</math>

Here <math><mi>&rho;</mi></math> is the largest coordinate-wise difference between the trial point and the closest convex combination of known feasible points. It is the maximum of the PV gap, wind gap, gas gap, and so on.

One must not simply maximize <math><mi>&rho;</mi></math> with these inequalities in a single flat problem, because then <math><mi>&rho;</mi></math> could be inflated artificially. It has to be the optimal value of the lower-level distance problem. The paper handles this by reformulating the bilevel LP with LP optimality conditions; with the <math><msub><mi>&ell;</mi><mi>&infin;</mi></msub></math> norm, the final Step 2 problem becomes a single-level MILP.

The output of Step 2 is <math><msup><mi>z</mi><mrow><mi>O</mi><mo>*</mo></mrow></msup></math>, the most suspicious point in the current outer approximation. It may be truly near-optimal. It may also be an artifact of an outer approximation that is too loose. Step 2 does not know which case holds.

## Step 3: Project the Trial Point Back to the True Model

Step 3 asks a different question:

> Is there an actual near-optimal energy-system design close to this aggressive trial point?

It solves the projection problem

<math display="block" aria-label="Step 3 projection to true near optimal region">
  <msup><mi>z</mi><mrow><mi>f</mi><mo>*</mo></mrow></msup>
  <mo>&isin;</mo>
  <munder><mi>argmin</mi><mrow><msup><mi>z</mi><mi>f</mi></msup><mo>&isin;</mo><msub><mi>Z</mi><mi>&epsilon;</mi></msub></mrow></munder>
  <mspace width="0.3em"></mspace>
  <msub>
    <mrow><mo>&Vert;</mo><msup><mi>z</mi><mrow><mi>O</mi><mo>*</mo></mrow></msup><mo>-</mo><msup><mi>z</mi><mi>f</mi></msup><mo>&Vert;</mo></mrow>
    <mi>&infin;</mi>
  </msub>
  <mo>.</mo>
</math>

Because membership in <math><msub><mi>Z</mi><mi>&epsilon;</mi></msub></math> is defined through the original system model, the projection is written with the full variable <math><mi>x</mi></math>:

<math display="block" aria-label="Step 3 full LP formulation">
  <munder><mi>min</mi><mrow><mi>x</mi><mo>,</mo><mi>&rho;</mi></mrow></munder>
  <mspace width="0.4em"></mspace>
  <mi>&rho;</mi>
  <mspace width="1em"></mspace>
  <mtext>subject to</mtext>
  <mspace width="0.4em"></mspace>
  <mo>-</mo><mi>&rho;</mi><mn>1</mn>
  <mo>&le;</mo>
  <msup><mi>z</mi><mrow><mi>O</mi><mo>*</mo></mrow></msup><mo>-</mo><mi>S</mi><mi>x</mi>
  <mo>&le;</mo>
  <mi>&rho;</mi><mn>1</mn><mo>,</mo>
  <mspace width="0.3em"></mspace>
  <mi>A</mi><mi>x</mi><mo>&le;</mo><mi>b</mi><mo>,</mo>
  <mspace width="0.3em"></mspace>
  <mi>F</mi><mi>x</mi><mo>=</mo><mi>d</mi><mo>,</mo>
  <mspace width="0.3em"></mspace>
  <msup><mi>c</mi><mo>&top;</mo></msup><mi>x</mi>
  <mo>&le;</mo>
  <msup><mi>v</mi><mo>*</mo></msup><mo>(</mo><mn>1</mn><mo>+</mo><mi>&epsilon;</mi><mo>)</mo><mo>.</mo>
</math>

This is much easier to interpret than Step 2. Step 2 says, "go to the place where the approximation is most empty." Step 3 says, "now ask the real model where the closest feasible point actually is."

If the optimal distance is zero, then <math><msup><mi>z</mi><mrow><mi>O</mi><mo>*</mo></mrow></msup></math> itself is a true near-optimal point and can be added to the inner approximation. If the distance is positive, the trial point is infeasible, but the projection <math><msup><mi>z</mi><mrow><mi>f</mi><mo>*</mo></mrow></msup></math> is still a valid near-optimal point and can be added to the inner approximation. In the infeasible case, the dual information from the projection can also generate a separating hyperplane that removes <math><msup><mi>z</mi><mrow><mi>O</mi><mo>*</mo></mrow></msup></math> from the outer approximation while preserving the true near-optimal region.

That is the loop:

1. Step 2 chooses the worst unexplored outer point.
2. Step 3 checks it against the original model.
3. The inner approximation grows by adding a real near-optimal point.
4. If the trial point was infeasible, the outer approximation shrinks by a valid cut.

The monotonic structure is the reason the method feels so clean:

<math display="block" aria-label="Monotone refinement">
  <msub><mi>I</mi><mi>k</mi></msub>
  <mo>&subseteq;</mo>
  <msub><mi>I</mi><mrow><mi>k</mi><mo>+</mo><mn>1</mn></mrow></msub>
  <mo>&subseteq;</mo>
  <msub><mi>Z</mi><mi>&epsilon;</mi></msub>
  <mo>&subseteq;</mo>
  <msub><mi>O</mi><mrow><mi>k</mi><mo>+</mo><mn>1</mn></mrow></msub>
  <mo>&subseteq;</mo>
  <msub><mi>O</mi><mi>k</mi></msub>
  <mo>.</mo>
</math>

## What Makes the Idea Original

The paper's originality is in combining three choices.

First, it uses the convex hull of known near-optimal points in convex-combination form, not explicit facet form. This is the difference between asking for a tractable LP membership check and asking a high-dimensional convex-hull algorithm to expose every face of the polytope.

Second, it defines the gap between inner and outer approximations as an interpretable max-min distance. The metric has the same unit as the design variables, so convergence can be stated in the language of capacity, not only in abstract polytope volume.

Third, it uses the original system model as an oracle. A trial point is projected back to the true near-optimal region; the projected feasible point grows the inner hull, and an infeasible trial point produces information for cutting the outer approximation.

This is why ORACLE is more than a smarter MGA heuristic. It is a certified set-approximation scheme for convex near-optimal regions.

## What Is Actually Guaranteed

The guarantees are strong, but only under the right assumptions.

If the near-optimal region is convex, then the convex hull of discovered near-optimal points is a valid inner approximation. If every outer cut is valid for the true region, then the outer approximation remains valid. If every point in the outer approximation is within tolerance of the inner approximation, then every point in the true region is also within that tolerance of the inner approximation.

This is the part that ordinary MGA does not provide. MGA can produce many interesting points, but it usually cannot say that the maximum unexplored error is below a specified threshold.

The limitation is just as important. The argument depends on convexity. Many realistic energy-system models include unit commitment, binary investment, modular technologies, minimum-load constraints, startup and shutdown costs, nonlinear efficiency, or degradation effects. In those settings, the near-optimal region may be nonconvex, and a convex combination of two feasible designs need not be feasible. ORACLE is therefore most naturally suited to continuous LP, convex, or quasiconvex planning models.

That is why I would not classify this paper as a core nonlinear-optimization paper. But as an algorithmic idea, it is unusually elegant: it turns "generate diverse alternatives" into "approximate the feasible alternative landscape with an error certificate."

<!-- ko -->

사실 이 논문은 LP 에너지 시스템의 convex near optimal solution space를 찾기 위한 매우 정교한 방법이다. 따라서 stochastic & nonlinear optimization에 들어가기에 적절한 논문은 아니다. 하지만 이 논문의 너무나 독창적이고 사랑스러운 아이디어들을 기록하고 공유하기 위해서 리뷰를 작성한다.

이 논문의 contribution은 새로운 에너지 시스템 최적화 모델 자체에 있지 않다. 모델은 여전히 대규모 LP이고, near-optimal set도 비용 상한 제약으로 정의된다. 핵심은 문제를 다시 정의하는 방식에 있다. Near-optimal exploration을 point generation 문제가 아니라 geometry problem으로 바꾼다.

기존 Modelling to Generate Alternatives, 즉 MGA는 대체로 다음 철학에 가깝다.

> 여러 방향으로 최적화해서 diverse points를 얻자.

ORACLE은 다른 철학을 따른다.

> 현재까지 아는 near-optimal region의 inner/outer approximation을 만들고, 가장 큰 approximation error가 있는 곳을 줄이자.

이 차이는 크다. 기존 MGA는 solution generation 중심이고, ORACLE은 set approximation과 certified convergence 중심이다.

## Approximation하려는 region

먼저 cost-optimal LP를 생각하자.

<math display="block" aria-label="Linear program cost optimum">
  <msup><mi>v</mi><mo>*</mo></msup>
  <mo>=</mo>
  <munder><mi>min</mi><mi>x</mi></munder>
  <mspace width="0.4em"></mspace>
  <msup><mi>c</mi><mo>&top;</mo></msup><mi>x</mi>
  <mspace width="1em"></mspace>
  <mtext>subject to</mtext>
  <mspace width="0.4em"></mspace>
  <mi>A</mi><mi>x</mi><mo>&le;</mo><mi>b</mi><mo>,</mo>
  <mspace width="0.4em"></mspace>
  <mi>F</mi><mi>x</mi><mo>=</mo><mi>d</mi><mo>.</mo>
</math>

전체 변수 <math><mi>x</mi></math>는 설비 용량, 운전량, 저장장치 운전, 수입/수출 등 매우 큰 decision vector다. 하지만 분석자가 실제로 보고 싶은 것은 보통 더 작은 설계 변수다.

<math display="block" aria-label="Projection from full decision to design variables">
  <mi>z</mi><mo>=</mo><mi>S</mi><mi>x</mi><mo>.</mo>
</math>

이 projected design space에서 near-optimal region은 다음처럼 정의된다.

<math display="block" aria-label="Projected near optimal region">
  <msub><mi>Z</mi><mi>&epsilon;</mi></msub>
  <mo>=</mo>
  <mrow>
    <mo>{</mo>
    <mi>z</mi><mo>:</mo>
    <mo>&exist;</mo><mi>x</mi><mo>,</mo>
    <mspace width="0.3em"></mspace>
    <mi>S</mi><mi>x</mi><mo>=</mo><mi>z</mi><mo>,</mo>
    <mspace width="0.3em"></mspace>
    <mi>A</mi><mi>x</mi><mo>&le;</mo><mi>b</mi><mo>,</mo>
    <mspace width="0.3em"></mspace>
    <mi>F</mi><mi>x</mi><mo>=</mo><mi>d</mi><mo>,</mo>
    <mspace width="0.3em"></mspace>
    <msup><mi>c</mi><mo>&top;</mo></msup><mi>x</mi>
    <mo>&le;</mo>
    <msup><mi>v</mi><mo>*</mo></msup><mo>(</mo><mn>1</mn><mo>+</mo><mi>&epsilon;</mi><mo>)</mo>
    <mo>}</mo>
  </mrow>
  <mo>.</mo>
</math>

정책결정자나 시스템 계획자는 단일 최저비용 해만 보지 않는다. 비용이 5% 또는 10% 더 들더라도 정치적 실행 가능성, 사회적 수용성, 공급망 리스크, 지역 형평성, 기술 선호 때문에 더 나은 선택지가 될 수 있다. 이런 요소들은 LP 안에 명시적으로 들어가지 않는 경우가 많지만, 최적화 결과가 실제 의사결정으로 넘어가는 순간 중요해진다.

## 왜 기존 MGA만으로는 부족한가

표준 MGA는 대체로 다음 문제를 반복해서 푼다.

<math display="block" aria-label="MGA directional search">
  <munder><mi>min</mi><mrow><mi>x</mi><mo>,</mo><mi>z</mi></mrow></munder>
  <mspace width="0.4em"></mspace>
  <msubsup><mi>w</mi><mi>k</mi><mo>&top;</mo></msubsup><mi>z</mi>
  <mspace width="1em"></mspace>
  <mtext>subject to</mtext>
  <mspace width="0.4em"></mspace>
  <mi>S</mi><mi>x</mi><mo>=</mo><mi>z</mi><mo>,</mo>
  <mspace width="0.3em"></mspace>
  <mi>A</mi><mi>x</mi><mo>&le;</mo><mi>b</mi><mo>,</mo>
  <mspace width="0.3em"></mspace>
  <mi>F</mi><mi>x</mi><mo>=</mo><mi>d</mi><mo>,</mo>
  <mspace width="0.3em"></mspace>
  <msup><mi>c</mi><mo>&top;</mo></msup><mi>x</mi>
  <mo>&le;</mo>
  <msup><mi>v</mi><mo>*</mo></msup><mo>(</mo><mn>1</mn><mo>+</mo><mi>&epsilon;</mi><mo>)</mo><mo>.</mo>
</math>

매 iteration마다 방향 <math><msub><mi>w</mi><mi>k</mi></msub></math>를 고르고, 그 방향으로 near-optimal feasible region 안에서 가장 극단적인 설계를 찾는다. Random MGA, VMM, HSJ, SPORES, ERG, Manhattan MGA 등은 방향을 고르거나 diversity를 유도하는 방식이 다를 뿐, 공통 약점은 그대로다. 점은 만든다. 하지만 set을 얼마나 잘 덮었는지는 보장하지 못한다.

Point cloud는 꽤 다양해 보여도 <math><msub><mi>Z</mi><mi>&epsilon;</mi></msub></math>의 큰 부분을 놓칠 수 있다. 더 나쁜 점은 사용자가 얼마나 놓쳤는지 알 수 없다는 것이다.

MAA는 convex hull을 사용하므로 region-based approach에 더 가깝다. 하지만 explicit convex hull의 facet을 계산하는 방식은 차원이 조금만 올라가도 부담이 커진다. ORACLE은 여기서 convex hull을 explicit halfspace form으로 만들지 않고 convex combination form으로 사용한다.

## ORACLE의 핵심 invariant

ORACLE은 다음 sandwich 구조를 유지한다.

<math display="block" aria-label="Inner outer sandwich">
  <msub><mi>I</mi><mi>k</mi></msub>
  <mo>&subseteq;</mo>
  <msub><mi>Z</mi><mi>&epsilon;</mi></msub>
  <mo>&subseteq;</mo>
  <msub><mi>O</mi><mi>k</mi></msub>
  <mo>.</mo>
</math>

Inner approximation <math><msub><mi>I</mi><mi>k</mi></msub></math>는 지금까지 찾은 near-optimal points의 convex hull이다.

<math display="block" aria-label="Inner approximation convex combination">
  <msub><mi>I</mi><mi>k</mi></msub>
  <mo>=</mo>
  <mrow>
    <mo>{</mo>
    <msub><mi>Z</mi><mi>k</mi></msub><mi>&lambda;</mi>
    <mo>:</mo>
    <msup><mn>1</mn><mo>&top;</mo></msup><mi>&lambda;</mi><mo>=</mo><mn>1</mn><mo>,</mo>
    <mspace width="0.3em"></mspace>
    <mi>&lambda;</mi><mo>&ge;</mo><mn>0</mn>
    <mo>}</mo>
  </mrow>
  <mo>,</mo>
</math>

여기서 <math><msub><mi>Z</mi><mi>k</mi></msub></math>의 column은 이미 발견한 near-optimal points다. Outer approximation <math><msub><mi>O</mi><mi>k</mi></msub></math>는 true region을 반드시 포함해야 하는 valid halfspaces의 intersection이다.

두 approximation 사이의 거리는 다음처럼 정의한다.

<math display="block" aria-label="Max min distance between outer and inner approximations">
  <msub><mi>d</mi><mi>k</mi></msub>
  <mo>=</mo>
  <munder><mi>max</mi><mrow><msup><mi>z</mi><mi>O</mi></msup><mo>&isin;</mo><msub><mi>O</mi><mi>k</mi></msub></mrow></munder>
  <mspace width="0.3em"></mspace>
  <munder><mi>min</mi><mrow><msup><mi>z</mi><mi>I</mi></msup><mo>&isin;</mo><msub><mi>I</mi><mi>k</mi></msub></mrow></munder>
  <mspace width="0.3em"></mspace>
  <msub>
    <mrow><mo>&Vert;</mo><msup><mi>z</mi><mi>O</mi></msup><mo>-</mo><msup><mi>z</mi><mi>I</mi></msup><mo>&Vert;</mo></mrow>
    <mi>&infin;</mi>
  </msub>
  <mo>.</mo>
</math>

이 수식이 이 논문의 매우 사랑스러운 부분이다. 탐색 변수가 GW 단위 설비용량이라면 <math><msub><mi>d</mi><mi>k</mi></msub><mo>=</mo><mn>0.1</mn></math> GW라는 말은 최악의 경우에도 design coordinate 하나에서 approximation error가 0.1 GW 이내라는 뜻이다. Volume gap보다 훨씬 직접적으로 해석된다.

## Step 2: 가장 의심스러운 outer point 찾기

Step 2는 다음 질문을 푼다.

> 현재 outer approximation 안에서, 지금까지 확실히 안다고 말할 수 있는 inner approximation과 가장 멀리 떨어진 곳은 어디인가?

Inner hull을 convex combination으로 쓰면 추상적인 formulation은 다음과 같다.

<math display="block" aria-label="Step 2 max min formulation">
  <msub><mi>d</mi><mi>k</mi></msub>
  <mo>=</mo>
  <munder><mi>max</mi><mrow><msup><mi>z</mi><mi>O</mi></msup><mo>&isin;</mo><msub><mi>O</mi><mi>k</mi></msub></mrow></munder>
  <mspace width="0.3em"></mspace>
  <munder><mi>min</mi><mrow><mi>&lambda;</mi><mo>&ge;</mo><mn>0</mn><mo>,</mo><msup><mn>1</mn><mo>&top;</mo></msup><mi>&lambda;</mi><mo>=</mo><mn>1</mn></mrow></munder>
  <mspace width="0.3em"></mspace>
  <msub>
    <mrow><mo>&Vert;</mo><msup><mi>z</mi><mi>O</mi></msup><mo>-</mo><msub><mi>Z</mi><mi>k</mi></msub><mi>&lambda;</mi><mo>&Vert;</mo></mrow>
    <mi>&infin;</mi>
  </msub>
  <mo>.</mo>
</math>

여기서 max-min 순서가 중요하다. 먼저 어떤 outer point <math><msup><mi>z</mi><mi>O</mi></msup></math>를 잡고, 그 점에서 현재 inner hull까지의 진짜 최단거리를 계산한다. 그 다음 이 최단거리가 가장 큰 outer point를 고른다.

고정된 <math><msup><mi>z</mi><mi>O</mi></msup></math>에 대해 inner hull까지의 거리는 다음 LP로 계산할 수 있다.

<math display="block" aria-label="Infinity norm distance to inner hull">
  <munder><mi>min</mi><mrow><mi>&lambda;</mi><mo>,</mo><mi>&rho;</mi></mrow></munder>
  <mspace width="0.4em"></mspace>
  <mi>&rho;</mi>
  <mspace width="1em"></mspace>
  <mtext>subject to</mtext>
  <mspace width="0.4em"></mspace>
  <mo>-</mo><mi>&rho;</mi><mn>1</mn>
  <mo>&le;</mo>
  <msup><mi>z</mi><mi>O</mi></msup><mo>-</mo><msub><mi>Z</mi><mi>k</mi></msub><mi>&lambda;</mi>
  <mo>&le;</mo>
  <mi>&rho;</mi><mn>1</mn><mo>,</mo>
  <mspace width="0.3em"></mspace>
  <msup><mn>1</mn><mo>&top;</mo></msup><mi>&lambda;</mi><mo>=</mo><mn>1</mn><mo>,</mo>
  <mspace width="0.3em"></mspace>
  <mi>&lambda;</mi><mo>&ge;</mo><mn>0</mn><mo>.</mo>
</math>

여기서 <math><mi>&rho;</mi></math>는 trial point와 가장 가까운 known feasible convex combination 사이의 coordinate-wise maximum difference다. PV는 몇 GW 차이, wind는 몇 GW 차이, gas는 몇 GW 차이인지 본 뒤 그중 가장 큰 값을 잡는 것이다.

주의할 점이 있다. 위 inequality를 두고 단순히 <math><mi>&rho;</mi></math>를 maximize하는 single-level problem을 만들면 안 된다. 그러면 <math><mi>&rho;</mi></math>를 일부러 크게 잡을 수 있기 때문이다. <math><mi>&rho;</mi></math>는 반드시 lower-level distance problem의 optimal value여야 한다. 논문은 이 bilevel LP를 LP optimality condition으로 reformulate하고, <math><msub><mi>&ell;</mi><mi>&infin;</mi></msub></math> norm 선택 덕분에 최종 Step 2를 single-level MILP로 푼다.

Step 2의 output은 <math><msup><mi>z</mi><mrow><mi>O</mi><mo>*</mo></mrow></msup></math>다. 이는 현재 outer approximation에서 가장 의심스러운 point다. 실제 near-optimal일 수도 있고, outer approximation이 너무 넓어서 생긴 가짜 후보일 수도 있다. Step 2만으로는 그 차이를 알 수 없다.

## Step 3: trial point를 true model로 projection하기

Step 3는 완전히 다른 질문을 푼다.

> 이 공격적인 trial point와 최대한 비슷한 실제 near-optimal energy-system design이 존재하는가?

즉 다음 projection problem을 푼다.

<math display="block" aria-label="Step 3 projection to true near optimal region">
  <msup><mi>z</mi><mrow><mi>f</mi><mo>*</mo></mrow></msup>
  <mo>&isin;</mo>
  <munder><mi>argmin</mi><mrow><msup><mi>z</mi><mi>f</mi></msup><mo>&isin;</mo><msub><mi>Z</mi><mi>&epsilon;</mi></msub></mrow></munder>
  <mspace width="0.3em"></mspace>
  <msub>
    <mrow><mo>&Vert;</mo><msup><mi>z</mi><mrow><mi>O</mi><mo>*</mo></mrow></msup><mo>-</mo><msup><mi>z</mi><mi>f</mi></msup><mo>&Vert;</mo></mrow>
    <mi>&infin;</mi>
  </msub>
  <mo>.</mo>
</math>

<math><msub><mi>Z</mi><mi>&epsilon;</mi></msub></math>에 속한다는 조건은 원래 system model을 통해 정의되므로, Step 3는 full variable <math><mi>x</mi></math>를 다시 사용한다.

<math display="block" aria-label="Step 3 full LP formulation">
  <munder><mi>min</mi><mrow><mi>x</mi><mo>,</mo><mi>&rho;</mi></mrow></munder>
  <mspace width="0.4em"></mspace>
  <mi>&rho;</mi>
  <mspace width="1em"></mspace>
  <mtext>subject to</mtext>
  <mspace width="0.4em"></mspace>
  <mo>-</mo><mi>&rho;</mi><mn>1</mn>
  <mo>&le;</mo>
  <msup><mi>z</mi><mrow><mi>O</mi><mo>*</mo></mrow></msup><mo>-</mo><mi>S</mi><mi>x</mi>
  <mo>&le;</mo>
  <mi>&rho;</mi><mn>1</mn><mo>,</mo>
  <mspace width="0.3em"></mspace>
  <mi>A</mi><mi>x</mi><mo>&le;</mo><mi>b</mi><mo>,</mo>
  <mspace width="0.3em"></mspace>
  <mi>F</mi><mi>x</mi><mo>=</mo><mi>d</mi><mo>,</mo>
  <mspace width="0.3em"></mspace>
  <msup><mi>c</mi><mo>&top;</mo></msup><mi>x</mi>
  <mo>&le;</mo>
  <msup><mi>v</mi><mo>*</mo></msup><mo>(</mo><mn>1</mn><mo>+</mo><mi>&epsilon;</mi><mo>)</mo><mo>.</mo>
</math>

이 formulation의 term은 직관적으로 읽힌다. <math><mi>x</mi></math>는 실제 energy system model의 전체 decision이고, <math><mi>S</mi><mi>x</mi></math>는 그중 우리가 보고 싶은 design variables다. <math><mi>A</mi><mi>x</mi><mo>&le;</mo><mi>b</mi></math>와 <math><mi>F</mi><mi>x</mi><mo>=</mo><mi>d</mi></math>는 기술적/운영상 제약과 balance equation이다. 비용 제약은 이 설계가 cost optimum에서 <math><mi>&epsilon;</mi></math>만큼만 벗어나는 near-optimal design이어야 한다는 뜻이다. 목적함수 <math><mi>&rho;</mi></math>는 trial point와 실제 feasible projected point 사이에서 가장 크게 어긋난 coordinate의 deviation이다.

한 문장으로 정리하면 Step 2는 "어디가 가장 비어 있나?"를 묻고, Step 3는 "그 방향에서 실제 feasible한 점은 어디인가?"를 묻는다.

Step 3의 optimal distance가 0이면 <math><msup><mi>z</mi><mrow><mi>O</mi><mo>*</mo></mrow></msup></math> 자체가 true near-optimal point이므로 inner approximation에 추가한다. Optimal distance가 양수이면 trial point는 infeasible이다. 하지만 projection point <math><msup><mi>z</mi><mrow><mi>f</mi><mo>*</mo></mrow></msup></math>는 실제 near-optimal point이므로 inner approximation에 추가할 수 있다. 또한 infeasible trial point의 경우 projection에서 얻은 dual information을 사용해 true near-optimal region은 보존하면서 <math><msup><mi>z</mi><mrow><mi>O</mi><mo>*</mo></mrow></msup></math>는 제거하는 separating hyperplane을 만들 수 있다.

따라서 loop는 다음과 같다.

1. Step 2가 worst unexplored outer point를 고른다.
2. Step 3가 그 점을 원래 모델로 검증한다.
3. 실제 near-optimal point를 추가하면서 inner approximation을 키운다.
4. Trial point가 infeasible이면 valid cut으로 outer approximation을 줄인다.

이 단조 구조가 ORACLE의 수학적 안정성이다.

<math display="block" aria-label="Monotone refinement">
  <msub><mi>I</mi><mi>k</mi></msub>
  <mo>&subseteq;</mo>
  <msub><mi>I</mi><mrow><mi>k</mi><mo>+</mo><mn>1</mn></mrow></msub>
  <mo>&subseteq;</mo>
  <msub><mi>Z</mi><mi>&epsilon;</mi></msub>
  <mo>&subseteq;</mo>
  <msub><mi>O</mi><mrow><mi>k</mi><mo>+</mo><mn>1</mn></mrow></msub>
  <mo>&subseteq;</mo>
  <msub><mi>O</mi><mi>k</mi></msub>
  <mo>.</mo>
</math>

## 무엇이 독창적인가

논문의 독창성은 세 요소의 결합에 있다.

첫째, convex hull을 explicit facet form이 아니라 convex combination form으로 사용한다. 이는 고차원 polytope의 모든 face를 계산하겠다는 접근이 아니라, membership과 distance 계산을 LP로 처리하겠다는 접근이다.

둘째, outer approximation과 inner approximation 사이의 max-min distance를 interpretable convergence metric으로 정의한다. 이 metric은 설계변수와 같은 단위를 가지므로, convergence를 abstract volume이 아니라 GW 단위 capacity error로 말할 수 있다.

셋째, 원래 system model을 oracle처럼 사용한다. Trial point를 true near-optimal region으로 projection하고, projected feasible point는 inner hull에 추가하며, infeasible trial point는 outer approximation을 자르는 정보를 준다.

그래서 ORACLE은 단순히 더 똑똑한 MGA heuristic이 아니다. Convex near-optimal region에 대한 certified set-approximation scheme에 가깝다.

## 무엇이 보장되고, 무엇이 약한가

보장은 강하지만, 조건도 강하다.

Near-optimal region이 convex라면, 발견한 near-optimal points의 convex hull은 valid inner approximation이다. 모든 outer cut이 true region에 대해 valid하다면, outer approximation은 계속 true region을 포함한다. Outer approximation의 모든 점이 inner approximation에서 tolerance 이내라면, true region의 모든 점도 inner approximation에서 tolerance 이내다.

이 부분이 기존 MGA에는 없다. MGA는 흥미로운 점을 많이 만들 수 있지만, maximum unexplored error가 특정 threshold보다 작다고 말하기 어렵다.

하지만 이 논리는 convexity에 기대고 있다. 실제 에너지 시스템 모델에는 unit commitment, binary investment, modular technology, minimum-load constraint, startup/shutdown cost, nonlinear efficiency, degradation effect가 들어갈 수 있다. 이런 경우 near-optimal region은 일반적으로 nonconvex이고, 두 feasible design의 convex combination이 실제 feasible design이 아닐 수 있다. 따라서 ORACLE은 continuous LP, convex, 또는 quasiconvex planning model에 가장 자연스럽게 맞는다.

이 때문에 이 논문을 핵심 nonlinear optimization 논문으로 분류하기는 어렵다. 그럼에도 algorithmic idea로서는 매우 우아하다. "다양한 대안을 많이 찍자"라는 문제를 "feasible alternative landscape를 error certificate와 함께 approximate하자"라는 문제로 바꾸기 때문이다.
