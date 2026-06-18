---
layout: post
title: "Feasible GNN Bounds for Exact Max-Cut Branch-and-Bound"
title_ko: "Exact Max-Cut branch-and-bound를 위한 feasible GNN bound"
date: 2026-06-18
category: graph-represented-methods
category_label: "Graph-Represented Methods"
research_group: algorithmic_reviews
research_category: graph-represented-methods
research_category_label: "Graph-Represented Methods"
application_category: ""
application_category_label: ""
method_category: "graph-represented-methods"
method_category_label: "Graph-Represented Methods"
paper_title: "Solving Max-Cut to Global Optimality via Feasibility-Preserving Graph Neural Networks"
authors: "Chen, H.; Qian, C.; Morris, C.; Lodi, A.; Li, C."
venue: "arXiv preprint"
year: "2026"
doi: ""
arxiv: "2605.07113"
source_url: "https://arxiv.org/abs/2605.07113"
tags:
  - "max-cut"
  - "branch-and-bound"
  - "semidefinite-programming"
  - "graph-neural-networks"
  - "exact-optimization"
excerpt: "A note on replacing repeated Max-Cut SDP bound computations inside exact branch-and-bound with a GNN surrogate that preserves dual feasibility and valid upper bounds."
excerpt_ko: "Exact Max-Cut branch-and-bound 안의 반복적인 SDP bound 계산을 dual feasibility와 valid upper bound를 보존하는 GNN surrogate로 대체하는 연구에 대한 정리."
language: "en-ko"
has_korean_note: false
---

This paper is not mainly about using a GNN to find a good Max-Cut heuristic. Its more interesting move is narrower and more structural: it replaces the repeated SDP relaxation solve inside exact branch-and-bound with a neural surrogate that still returns a valid upper bound. The point is not that the neural network proves optimality by itself. The point is that its output is projected into a dual-feasible SDP solution, so the branch-and-bound algorithm can use it without losing the global optimality guarantee.

That distinction matters. In exact combinatorial optimization, a learned predictor is usually dangerous when it sits inside a pruning rule. If the predictor is optimistic in the wrong direction, it can remove the branch containing the optimum. This paper avoids that failure mode by making the learned bound conservative by construction.

## The Bottleneck

Max-Cut partitions the vertices of a weighted graph <math><mi>G</mi><mo>=</mo><mo>(</mo><mi>V</mi><mo>,</mo><mi>E</mi><mo>)</mo></math> into two sides and maximizes the total edge weight crossing the partition. With <math><msub><mi>x</mi><mi>i</mi></msub><mo>&isin;</mo><mo>{</mo><mo>-</mo><mn>1</mn><mo>,</mo><mn>1</mn><mo>}</mo></math>, one common form is:

<math display="block" aria-label="Max-Cut quadratic form">
  <munder><mi>max</mi><mrow><mi>x</mi><mo>&isin;</mo><msup><mrow><mo>{</mo><mo>-</mo><mn>1</mn><mo>,</mo><mn>1</mn><mo>}</mrow><mi>n</mi></msup></mrow></munder>
  <mspace width="0.5em"></mspace>
  <mfrac><mn>1</mn><mn>2</mn></mfrac>
  <munder><mo>&sum;</mo><mrow><mo>{</mo><mi>i</mi><mo>,</mo><mi>j</mi><mo>}</mo><mo>&isin;</mo><mi>E</mi></mrow></munder>
  <msub><mi>w</mi><mrow><mi>i</mi><mi>j</mi></mrow></msub>
  <mo>(</mo><mn>1</mn><mo>-</mo><msub><mi>x</mi><mi>i</mi></msub><msub><mi>x</mi><mi>j</mi></msub><mo>)</mo>
  <mo>=</mo>
  <mfrac><mn>1</mn><mn>4</mn></mfrac>
  <msup><mi>x</mi><mo>&top;</mo></msup><mi>L</mi><mi>x</mi><mo>.</mo>
</math>

The problem is NP-complete, so exact solving typically needs branch-and-bound. At each node, the solver needs an upper bound on the best cut that can still appear below that node. SDP relaxations are strong bounds, but repeatedly solving an SDP at many branch-and-bound nodes is expensive.

The paper targets precisely this repeated bounding step. Existing machine-learning work for branch-and-bound often learns branching decisions, cut selection, or primal heuristics while leaving the relaxation solver unchanged. Here the relaxation evaluation itself is replaced.

## The SDP Object

The standard Max-Cut SDP relaxation replaces binary signs by unit vectors and introduces the Gram matrix:

<math display="block" aria-label="Max-Cut SDP matrix variable">
  <msub><mi>X</mi><mrow><mi>i</mi><mi>j</mi></mrow></msub>
  <mo>=</mo>
  <msubsup><mi>v</mi><mi>i</mi><mo>&top;</mo></msubsup>
  <msub><mi>v</mi><mi>j</mi></msub>
  <mo>,</mo>
  <mspace width="0.5em"></mspace>
  <mi>X</mi><mo>&succeq;</mo><mn>0</mn><mo>,</mo>
  <mspace width="0.5em"></mspace>
  <mi>diag</mi><mo>(</mo><mi>X</mi><mo>)</mo><mo>=</mo><mi>e</mi><mo>.</mo>
</math>

The primal relaxation has the form:

<math display="block" aria-label="Primal SDP relaxation">
  <munder><mi>max</mi><mrow><mi>X</mi><mo>&isin;</mo><msubsup><mi>S</mi><mo>+</mo><mi>n</mi></msubsup></mrow></munder>
  <mspace width="0.5em"></mspace>
  <mo>&lang;</mo><mi>L</mi><mo>,</mo><mi>X</mi><mo>&rang;</mo>
  <mspace width="1em"></mspace>
  <mtext>subject to</mtext>
  <mspace width="0.5em"></mspace>
  <mi>diag</mi><mo>(</mo><mi>X</mi><mo>)</mo><mo>=</mo><mi>e</mi><mo>.</mo>
</math>

The corresponding dual can be written around a vector <math><mi>y</mi></math> and a positive semidefinite slack matrix:

<math display="block" aria-label="Dual SDP feasibility">
  <mi>S</mi><mo>=</mo><mi>Diag</mi><mo>(</mo><mi>y</mi><mo>)</mo><mo>-</mo><mi>L</mi>
  <mo>&succeq;</mo><mn>0</mn><mo>.</mo>
</math>

If <math><mi>y</mi></math> is dual feasible, then <math><msup><mi>e</mi><mo>&top;</mo></msup><mi>y</mi></math> is a valid upper bound. This is the mathematical door through which the neural network enters the exact algorithm.

## Why Pairwise Tokens Are Natural

A standard node-level GNN maintains embeddings <math><msub><mi>h</mi><mi>i</mi></msub></math>. That is a poor match to the SDP variable, because the decision object is not a vertex vector but a matrix entry <math><msub><mi>X</mi><mrow><mi>i</mi><mi>j</mi></mrow></msub></math>. The architecture therefore keeps a representation for each pair:

<math display="block" aria-label="Pairwise token">
  <msubsup><mi>h</mi><mrow><mi>i</mi><mi>j</mi></mrow><mn>0</mn></msubsup>
  <mo>=</mo>
  <mi>INIT</mi>
  <mo>(</mo>
  <msub><mi>C</mi><mrow><mi>i</mi><mi>j</mi></mrow></msub>
  <mo>,</mo>
  <msub><mi>I</mi><mrow><mi>i</mi><mo>=</mo><mi>j</mi></mrow></msub>
  <mo>)</mo><mo>.</mo>
</math>

The diagonal indicator is not a cosmetic feature. The Max-Cut SDP constraints are exactly the diagonal equalities <math><msub><mi>X</mi><mrow><mi>i</mi><mi>i</mi></mrow></msub><mo>=</mo><mn>1</mn></math>. By marking diagonal entries directly, the model can exploit the special structure of this SDP instead of using a heavier generic SDP architecture.

The MC-MPNN update resembles matrix-style information flow: an entry <math><msub><mi>h</mi><mrow><mi>i</mi><mi>j</mi></mrow></msub></math> is refined using row-direction and column-direction messages through intermediate vertices. This is closer to the behavior of matrix powers than ordinary vertex message passing. A sparsity-aware variant, <math><mi>&delta;</mi></math>-MC-MPNN, restricts aggregation to nonzero graph entries and has an idealized update cost of <math><mi>O</mi><mo>(</mo><msup><mi>n</mi><mn>2</mn></msup><mo>+</mo><mi>n</mi><mi>e</mi><mo>)</mo></math>.

There is a caveat. The notes indicate that the sparse variant is still implemented with dense GPU operations because those are faster in practice. So the theoretical sparsity story and wall-clock behavior do not perfectly coincide. Empirically, the sparse variant saves some memory but is not clearly dominant over the dense MC-MPNN.

## Preserving Feasibility

The main engineering idea is to make infeasible neural outputs impossible, or at least correct them into feasible objects before branch-and-bound sees them.

For the primal SDP, the model predicts vectors <math><msub><mi>o</mi><mi>i</mi></msub><mo>&isin;</mo><msup><mi>R</mi><mi>r</mi></msup></math> and normalizes them:

<math display="block" aria-label="Primal normalization">
  <msub><mrow><mo>||</mo><msub><mi>o</mi><mi>i</mi></msub><mo>||</mo></mrow><mn>2</mn></msub>
  <mo>=</mo><mn>1</mn><mo>.</mo>
</math>

Then it defines:

<math display="block" aria-label="Primal factorization">
  <mover><mi>X</mi><mo>^</mo></mover>
  <mo>=</mo>
  <mi>O</mi><msup><mi>O</mi><mo>&top;</mo></msup>
  <mo>,</mo>
  <mspace width="0.5em"></mspace>
  <msub><mover><mi>X</mi><mo>^</mo></mover><mrow><mi>i</mi><mi>j</mi></mrow></msub>
  <mo>=</mo>
  <msubsup><mi>o</mi><mi>i</mi><mo>&top;</mo></msubsup><msub><mi>o</mi><mi>j</mi></msub><mo>.</mo>
</math>

This guarantees <math><mover><mi>X</mi><mo>^</mo></mover><mo>&succeq;</mo><mn>0</mn></math> and <math><mi>diag</mi><mo>(</mo><mover><mi>X</mi><mo>^</mo></mover><mo>)</mo><mo>=</mo><mi>e</mi></math>. It is similar in spirit to a low-rank Burer-Monteiro parameterization, though here it is used as a feasibility-preserving output layer rather than as an exact SDP solver.

The dual side is more important for exactness. The network predicts a raw vector <math><mover><mi>y</mi><mo>^</mo></mover></math>. Its slack matrix may fail to be PSD:

<math display="block" aria-label="Raw dual slack">
  <mover><mi>S</mi><mo>^</mo></mover>
  <mo>=</mo>
  <mi>Diag</mi><mo>(</mo><mover><mi>y</mi><mo>^</mo></mover><mo>)</mo><mo>-</mo><mi>L</mi><mo>.</mo>
</math>

The paper fixes this with a radial shift:

<math display="block" aria-label="Dual radial projection">
  <msub><mover><mi>y</mi><mo>^</mo></mover><mtext>feas</mtext></msub>
  <mo>=</mo>
  <mover><mi>y</mi><mo>^</mo></mover>
  <mo>+</mo>
  <mi>max</mi>
  <mo>{</mo>
  <mn>0</mn><mo>,</mo>
  <mo>-</mo><msub><mi>&lambda;</mi><mi>min</mi></msub>
  <mo>(</mo><mover><mi>S</mi><mo>^</mo></mover><mo>)</mo>
  <mo>}</mo>
  <mi>e</mi><mo>.</mo>
</math>

The corrected slack is:

<math display="block" aria-label="Corrected slack matrix">
  <msub><mover><mi>S</mi><mo>^</mo></mover><mtext>feas</mtext></msub>
  <mo>=</mo>
  <mover><mi>S</mi><mo>^</mo></mover>
  <mo>+</mo>
  <mi>max</mi>
  <mo>{</mo>
  <mn>0</mn><mo>,</mo>
  <mo>-</mo><msub><mi>&lambda;</mi><mi>min</mi></msub>
  <mo>(</mo><mover><mi>S</mi><mo>^</mo></mover><mo>)</mo>
  <mo>}</mo>
  <mi>I</mi>
  <mo>&succeq;</mo><mn>0</mn><mo>.</mo>
</math>

This is the key safety device. The bound may become loose, but it remains valid.

## Exactness Inside Branch-and-Bound

For a maximization problem, branch-and-bound keeps a feasible incumbent value <math><mi>LB</mi></math> and an upper bound <math><mi>UB</mi><mo>(</mo><mi>c</mi><mo>)</mo></math> for each node <math><mi>c</mi></math>. A node can be pruned when its upper bound cannot beat the incumbent. In integer-weight settings, the notes describe the rule roughly as:

<math display="block" aria-label="Branch and bound pruning">
  <msub><mi>UB</mi><mi>c</mi></msub>
  <mo>&lt;</mo>
  <mi>LB</mi><mo>+</mo><mn>1</mn><mo>.</mo>
</math>

The vanilla solver obtains <math><msub><mi>UB</mi><mi>c</mi></msub></math> by solving the SDP relaxation, often with Mosek. The neural solver instead uses:

<math display="block" aria-label="Neural upper bound">
  <msub><mi>UB</mi><mi>c</mi></msub>
  <mo>=</mo>
  <msup><mi>e</mi><mo>&top;</mo></msup>
  <msub><mover><mi>y</mi><mo>^</mo></mover><mtext>feas</mtext></msub><mo>.</mo>
</math>

By dual feasibility,

<math display="block" aria-label="Upper-bound relation">
  <msubsup><mi>f</mi><mtext>SDP</mtext><mo>*</mo></msubsup>
  <mo>&le;</mo>
  <msup><mi>e</mi><mo>&top;</mo></msup>
  <msub><mover><mi>y</mi><mo>^</mo></mover><mtext>feas</mtext></msub><mo>.</mo>
</math>

So the learned bound is at least as conservative as the exact SDP bound. It may prune fewer nodes, but it should not prune incorrectly. That is the precise sense in which global optimality is preserved.

This also explains the performance trade-off. The neural method can visit more nodes because the bounds are looser. It wins only if the cost per node drops enough. In the reported examples, that happens: for instance, the notes report g05_100 going from about 40,930 seconds with vanilla Mosek B&B to about 4,509 seconds with the neural version, despite evaluating more nodes. The important mechanism is "more nodes, much cheaper bounds."

## What The Theory Actually Says

There are three different guarantees, and they should not be conflated.

First, feasibility is guaranteed by construction. The primal output is PSD with unit diagonal because of factorization and normalization. The dual output is PSD after the radial projection. This part does not depend on successful training.

Second, the expressivity theorem is about symmetry consistency. If the stable coloring of the <math><mi>&delta;</mi></math>-MC-WL procedure cannot distinguish two pairs <math><mo>(</mo><mi>i</mi><mo>,</mo><mi>j</mi><mo>)</mo></math> and <math><mo>(</mo><mi>p</mi><mo>,</mo><mi>q</mi><mo>)</mo></math>, then the corresponding entries in an optimal primal SDP solution need not be distinguished either. Similarly, equal diagonal colors imply equal dual variables in an optimal dual solution. The proof idea links the WL refinement to matrix powers, spectral projectors, and a convergent PDHG view of the SDP.

That is a useful expressivity statement. It is not a finite-depth neural approximation guarantee. It does not say that the trained network will always predict a tight SDP solution.

Third, branch-and-bound correctness follows from using valid upper bounds and feasible lower bounds. If the learned dual bound is weak, the algorithm may become slow. But it should still be exact as long as enumeration and pruning are implemented correctly.

## Strengths

The strongest contribution is the placement of the neural network. The paper does not merely add a learned heuristic around the solver. It replaces the relaxation oracle while preserving the one property the exact solver needs: a valid bound.

The second strength is the clean dual-feasibility mechanism. Penalty-based constrained learning can still produce infeasible predictions. Here feasibility is forced after prediction, so the branch-and-bound pruning rule sees a certified upper bound rather than a hopeful estimate.

The third strength is that the architecture uses the Max-Cut SDP structure instead of treating the problem as a generic graph prediction task. Pairwise tokens match the matrix decision variable. The diagonal indicator matches the diagonal equality constraints. That is the right kind of inductive bias.

The self-supervised training setup is also attractive. The model can optimize the dual objective without requiring solved SDP labels for every training instance, even though comparison to Mosek remains necessary for evaluation.

## Limitations

The main limitation is that this is not yet a state-of-the-art Max-Cut solver story. Classical branch-and-cut solvers with cutting planes, such as BiqCrunch-style methods, remain much stronger on some instances. The paper's more defensible claim is that base SDP relaxation evaluation can be replaced by a feasibility-preserving GNN surrogate, not that the full Max-Cut solver ecosystem has been surpassed.

The second limitation is distribution dependence. Training subgraphs are generated from random branch-and-bound trajectories and related graph families. If the graph size, sparsity pattern, or weight distribution changes, bound quality can degrade. Exactness survives, but speed may disappear.

The third limitation is that dual feasibility does not imply tightness. The guarantee is:

<math display="block" aria-label="Dual feasibility without approximation guarantee">
  <msubsup><mi>f</mi><mtext>SDP</mtext><mo>*</mo></msubsup>
  <mo>&le;</mo>
  <msup><mi>e</mi><mo>&top;</mo></msup>
  <msub><mover><mi>y</mi><mo>^</mo></mover><mtext>feas</mtext></msub><mo>.</mo>
</math>

It is not:

<math display="block" aria-label="No tightness guarantee">
  <msup><mi>e</mi><mo>&top;</mo></msup>
  <msub><mover><mi>y</mi><mo>^</mo></mover><mtext>feas</mtext></msub>
  <mo>-</mo>
  <msubsup><mi>f</mi><mtext>SDP</mtext><mo>*</mo></msubsup>
  <mo>&le;</mo>
  <mi>&epsilon;</mi><mo>.</mo>
</math>

In a bad case, the bound can be so loose that branch-and-bound explores a very large tree.

The radial projection is also conservative. Adding the same shift to every component of <math><mi>y</mi></math> is cheap and safe, but it may increase the objective much more than necessary. A more refined correction layer could search for a smaller diagonal adjustment, but then the method starts to reintroduce an optimization problem inside the bound oracle.

Finally, the eigenvalue computation for <math><msub><mi>&lambda;</mi><mi>min</mi></msub></math> has not disappeared. It may be acceptable at the reported scale, but for much larger graphs, approximate eigensolvers and feasibility tolerances would become part of the story.

## References

Chen, H., Qian, C., Morris, C., Lodi, A., & Li, C. (2026). Solving Max-Cut to Global Optimality via Feasibility-Preserving Graph Neural Networks. arXiv preprint arXiv:2605.07113.

<!-- ko -->

이 논문은 좋은 Max-Cut heuristic을 찾는 GNN 연구라기보다, exact branch-and-bound 안에서 반복적으로 풀리는 SDP relaxation을 neural surrogate로 대체하려는 연구에 가깝다. 중요한 점은 neural network가 최적성을 직접 증명한다는 것이 아니다. GNN이 만든 dual solution을 feasible하게 보정해서 valid upper bound로 만들고, 그 bound를 branch-and-bound pruning에 넣어도 global optimality guarantee가 깨지지 않게 만든다는 점이 핵심이다.

이 차이는 꽤 중요하다. Exact combinatorial optimization에서 learned predictor가 pruning rule 안에 들어가면 위험하다. 잘못 낙관적인 예측이 나오면 optimum이 들어 있는 branch를 지울 수 있기 때문이다. 이 논문은 그 failure mode를 dual feasibility로 막는다. Bound가 느슨할 수는 있지만, 안전한 방향으로 느슨하다.

## 병목은 어디에 있는가

Max-Cut은 weighted graph <math><mi>G</mi><mo>=</mo><mo>(</mo><mi>V</mi><mo>,</mo><mi>E</mi><mo>)</mo></math>의 vertex를 두 partition으로 나누고, partition 사이를 가로지르는 edge weight 합을 최대화하는 문제다. <math><msub><mi>x</mi><mi>i</mi></msub><mo>&isin;</mo><mo>{</mo><mo>-</mo><mn>1</mn><mo>,</mo><mn>1</mn><mo>}</mo></math>라고 하면 보통 다음처럼 쓴다.

<math display="block" aria-label="Max-Cut quadratic form Korean">
  <munder><mi>max</mi><mrow><mi>x</mi><mo>&isin;</mo><msup><mrow><mo>{</mo><mo>-</mo><mn>1</mn><mo>,</mo><mn>1</mn><mo>}</mrow><mi>n</mi></msup></mrow></munder>
  <mspace width="0.5em"></mspace>
  <mfrac><mn>1</mn><mn>2</mn></mfrac>
  <munder><mo>&sum;</mo><mrow><mo>{</mo><mi>i</mi><mo>,</mo><mi>j</mi><mo>}</mo><mo>&isin;</mo><mi>E</mi></mrow></munder>
  <msub><mi>w</mi><mrow><mi>i</mi><mi>j</mi></mrow></msub>
  <mo>(</mo><mn>1</mn><mo>-</mo><msub><mi>x</mi><mi>i</mi></msub><msub><mi>x</mi><mi>j</mi></msub><mo>)</mo>
  <mo>=</mo>
  <mfrac><mn>1</mn><mn>4</mn></mfrac>
  <msup><mi>x</mi><mo>&top;</mo></msup><mi>L</mi><mi>x</mi><mo>.</mo>
</math>

Max-Cut은 NP-complete이므로 exact solution을 위해서는 보통 branch-and-bound가 필요하다. 각 node에서는 그 node 아래에서 나올 수 있는 best cut에 대한 upper bound가 필요하다. SDP relaxation은 강한 bound를 주지만, branch-and-bound tree가 커질수록 node마다 SDP를 푸는 비용이 병목이 된다.

이 논문은 바로 이 bounding step을 겨냥한다. 기존 ML-for-B&B 연구가 branching decision, cut selection, primal heuristic을 주로 학습했다면, 여기서는 relaxation evaluation 자체를 neural network가 대신한다.

## SDP에서 필요한 것

Max-Cut SDP relaxation은 binary sign을 unit vector로 relax하고 Gram matrix를 도입한다.

<math display="block" aria-label="Max-Cut SDP matrix variable Korean">
  <msub><mi>X</mi><mrow><mi>i</mi><mi>j</mi></mrow></msub>
  <mo>=</mo>
  <msubsup><mi>v</mi><mi>i</mi><mo>&top;</mo></msubsup>
  <msub><mi>v</mi><mi>j</mi></msub>
  <mo>,</mo>
  <mspace width="0.5em"></mspace>
  <mi>X</mi><mo>&succeq;</mo><mn>0</mn><mo>,</mo>
  <mspace width="0.5em"></mspace>
  <mi>diag</mi><mo>(</mo><mi>X</mi><mo>)</mo><mo>=</mo><mi>e</mi><mo>.</mo>
</math>

Primal relaxation은 대략 다음 형태다.

<math display="block" aria-label="Primal SDP relaxation Korean">
  <munder><mi>max</mi><mrow><mi>X</mi><mo>&isin;</mo><msubsup><mi>S</mi><mo>+</mo><mi>n</mi></msubsup></mrow></munder>
  <mspace width="0.5em"></mspace>
  <mo>&lang;</mo><mi>L</mi><mo>,</mo><mi>X</mi><mo>&rang;</mo>
  <mspace width="1em"></mspace>
  <mtext>subject to</mtext>
  <mspace width="0.5em"></mspace>
  <mi>diag</mi><mo>(</mo><mi>X</mi><mo>)</mo><mo>=</mo><mi>e</mi><mo>.</mo>
</math>

Dual은 vector <math><mi>y</mi></math>와 PSD slack matrix로 볼 수 있다.

<math display="block" aria-label="Dual SDP feasibility Korean">
  <mi>S</mi><mo>=</mo><mi>Diag</mi><mo>(</mo><mi>y</mi><mo>)</mo><mo>-</mo><mi>L</mi>
  <mo>&succeq;</mo><mn>0</mn><mo>.</mo>
</math>

만약 <math><mi>y</mi></math>가 dual feasible이면 <math><msup><mi>e</mi><mo>&top;</mo></msup><mi>y</mi></math>는 valid upper bound다. 이 사실이 neural network를 exact algorithm 안으로 넣는 수학적 통로가 된다.

## 왜 pairwise token이 필요한가

일반적인 GNN은 node embedding <math><msub><mi>h</mi><mi>i</mi></msub></math>를 둔다. 하지만 SDP의 decision object는 vertex vector가 아니라 matrix entry <math><msub><mi>X</mi><mrow><mi>i</mi><mi>j</mi></mrow></msub></math>다. 그래서 이 논문은 각 pair마다 representation을 둔다.

<math display="block" aria-label="Pairwise token Korean">
  <msubsup><mi>h</mi><mrow><mi>i</mi><mi>j</mi></mrow><mn>0</mn></msubsup>
  <mo>=</mo>
  <mi>INIT</mi>
  <mo>(</mo>
  <msub><mi>C</mi><mrow><mi>i</mi><mi>j</mi></mrow></msub>
  <mo>,</mo>
  <msub><mi>I</mi><mrow><mi>i</mi><mo>=</mo><mi>j</mi></mrow></msub>
  <mo>)</mo><mo>.</mo>
</math>

Diagonal indicator는 단순한 feature가 아니다. Max-Cut SDP의 constraint는 <math><msub><mi>X</mi><mrow><mi>i</mi><mi>i</mi></mrow></msub><mo>=</mo><mn>1</mn></math>이라는 diagonal equality이므로, diagonal 여부를 직접 표시하면 generic SDP architecture보다 훨씬 문제 구조에 맞는 inductive bias를 줄 수 있다.

MC-MPNN update는 matrix multiplication과 비슷한 정보 흐름을 가진다. <math><msub><mi>h</mi><mrow><mi>i</mi><mi>j</mi></mrow></msub></math>를 update할 때 intermediate vertex를 통해 row 방향과 column 방향 정보를 같이 본다. 그래서 ordinary node-level message passing보다 SDP matrix structure를 더 직접적으로 표현한다.

논문은 sparsity-aware variant인 <math><mi>&delta;</mi></math>-MC-MPNN도 제안한다. Nonzero graph entry만 aggregate하면 이론적 update cost는 <math><mi>O</mi><mo>(</mo><msup><mi>n</mi><mn>2</mn></msup><mo>+</mo><mi>n</mi><mi>e</mi><mo>)</mo></math>가 된다. 다만 실제 구현에서는 dense GPU operation이 더 빠르기 때문에 sparse variant도 dense matrix multiplication으로 구현했다고 한다. 그래서 theoretical sparsity advantage와 실제 wall-clock advantage는 완전히 일치하지 않는다.

## Feasibility를 어떻게 보존하는가

이 논문의 가장 중요한 부분은 infeasible neural output을 branch-and-bound에 그대로 넣지 않는다는 점이다.

Primal SDP 쪽에서는 model이 vector <math><msub><mi>o</mi><mi>i</mi></msub><mo>&isin;</mo><msup><mi>R</mi><mi>r</mi></msup></math>를 예측하고 normalize한다.

<math display="block" aria-label="Primal normalization Korean">
  <msub><mrow><mo>||</mo><msub><mi>o</mi><mi>i</mi></msub><mo>||</mo></mrow><mn>2</mn></msub>
  <mo>=</mo><mn>1</mn><mo>.</mo>
</math>

그 다음 다음처럼 matrix를 만든다.

<math display="block" aria-label="Primal factorization Korean">
  <mover><mi>X</mi><mo>^</mo></mover>
  <mo>=</mo>
  <mi>O</mi><msup><mi>O</mi><mo>&top;</mo></msup>
  <mo>,</mo>
  <mspace width="0.5em"></mspace>
  <msub><mover><mi>X</mi><mo>^</mo></mover><mrow><mi>i</mi><mi>j</mi></mrow></msub>
  <mo>=</mo>
  <msubsup><mi>o</mi><mi>i</mi><mo>&top;</mo></msubsup><msub><mi>o</mi><mi>j</mi></msub><mo>.</mo>
</math>

그러면 <math><mover><mi>X</mi><mo>^</mo></mover><mo>&succeq;</mo><mn>0</mn></math>이고 <math><mi>diag</mi><mo>(</mo><mover><mi>X</mi><mo>^</mo></mover><mo>)</mo><mo>=</mo><mi>e</mi></math>가 자동으로 성립한다. Burer-Monteiro low-rank factorization과 비슷하지만, 여기서는 exact SDP solver가 아니라 feasible neural output layer로 쓰인다는 점이 다르다.

Exactness에는 dual side가 더 중요하다. Network가 raw vector <math><mover><mi>y</mi><mo>^</mo></mover></math>를 예측하면 slack matrix

<math display="block" aria-label="Raw dual slack Korean">
  <mover><mi>S</mi><mo>^</mo></mover>
  <mo>=</mo>
  <mi>Diag</mi><mo>(</mo><mover><mi>y</mi><mo>^</mo></mover><mo>)</mo><mo>-</mo><mi>L</mi>
</math>

가 PSD가 아닐 수 있다. 논문은 이를 radial shift로 보정한다.

<math display="block" aria-label="Dual radial projection Korean">
  <msub><mover><mi>y</mi><mo>^</mo></mover><mtext>feas</mtext></msub>
  <mo>=</mo>
  <mover><mi>y</mi><mo>^</mo></mover>
  <mo>+</mo>
  <mi>max</mi>
  <mo>{</mo>
  <mn>0</mn><mo>,</mo>
  <mo>-</mo><msub><mi>&lambda;</mi><mi>min</mi></msub>
  <mo>(</mo><mover><mi>S</mi><mo>^</mo></mover><mo>)</mo>
  <mo>}</mo>
  <mi>e</mi><mo>.</mo>
</math>

그러면 corrected slack은 다음처럼 PSD가 된다.

<math display="block" aria-label="Corrected slack matrix Korean">
  <msub><mover><mi>S</mi><mo>^</mo></mover><mtext>feas</mtext></msub>
  <mo>=</mo>
  <mover><mi>S</mi><mo>^</mo></mover>
  <mo>+</mo>
  <mi>max</mi>
  <mo>{</mo>
  <mn>0</mn><mo>,</mo>
  <mo>-</mo><msub><mi>&lambda;</mi><mi>min</mi></msub>
  <mo>(</mo><mover><mi>S</mi><mo>^</mo></mover><mo>)</mo>
  <mo>}</mo>
  <mi>I</mi>
  <mo>&succeq;</mo><mn>0</mn><mo>.</mo>
</math>

이 장치가 branch-and-bound correctness의 핵심이다. Bound가 느슨해질 수는 있지만, valid upper bound라는 성질은 남는다.

## Branch-and-bound에서 exactness가 유지되는 이유

Maximization problem의 branch-and-bound는 feasible incumbent value <math><mi>LB</mi></math>와 각 node의 upper bound <math><mi>UB</mi><mo>(</mo><mi>c</mi><mo>)</mo></math>를 유지한다. Integer-weight setting에서는 대략 다음 조건이면 node를 prune할 수 있다.

<math display="block" aria-label="Branch and bound pruning Korean">
  <msub><mi>UB</mi><mi>c</mi></msub>
  <mo>&lt;</mo>
  <mi>LB</mi><mo>+</mo><mn>1</mn><mo>.</mo>
</math>

Vanilla solver는 Mosek 등으로 SDP relaxation을 풀어서 <math><msub><mi>UB</mi><mi>c</mi></msub></math>를 얻는다. Neural solver는 대신 다음 bound를 쓴다.

<math display="block" aria-label="Neural upper bound Korean">
  <msub><mi>UB</mi><mi>c</mi></msub>
  <mo>=</mo>
  <msup><mi>e</mi><mo>&top;</mo></msup>
  <msub><mover><mi>y</mi><mo>^</mo></mover><mtext>feas</mtext></msub><mo>.</mo>
</math>

Dual feasibility 때문에 다음이 성립한다.

<math display="block" aria-label="Upper-bound relation Korean">
  <msubsup><mi>f</mi><mtext>SDP</mtext><mo>*</mo></msubsup>
  <mo>&le;</mo>
  <msup><mi>e</mi><mo>&top;</mo></msup>
  <msub><mover><mi>y</mi><mo>^</mo></mover><mtext>feas</mtext></msub><mo>.</mo>
</math>

즉 learned bound는 exact SDP bound보다 같거나 더 conservative하다. 더 많은 node를 보게 만들 수는 있지만, 잘못 prune하지는 않는다. 이것이 이 논문에서 말하는 global optimality preservation의 정확한 의미다.

성능 trade-off도 여기서 나온다. Neural bound는 느슨해서 node 수를 늘릴 수 있다. 대신 node당 계산 비용이 훨씬 낮다. 첨부 노트에 따르면 g05_100에서는 vanilla Mosek B&B가 약 40,930초 걸렸고 neural version은 약 4,509초 걸렸다. Node 수는 늘었지만 bound computation이 훨씬 싸서 전체 시간이 줄어든 것이다.

## 이론이 실제로 보장하는 것

보장에는 세 층위가 있고, 서로 섞으면 안 된다.

첫째, feasibility는 construction으로 보장된다. Primal은 factorization과 normalization 때문에 PSD와 unit diagonal을 만족한다. Dual은 radial projection 이후 PSD slack을 가진다. 이 부분은 training success와 무관하다.

둘째, expressivity theorem은 symmetry consistency에 관한 것이다. <math><mi>&delta;</mi></math>-MC-WL의 stable coloring이 두 pair <math><mo>(</mo><mi>i</mi><mo>,</mo><mi>j</mi><mo>)</mo></math>와 <math><mo>(</mo><mi>p</mi><mo>,</mo><mi>q</mi><mo>)</mo></math>를 구분하지 못하면, optimal primal SDP solution에서도 해당 entries를 구분할 필요가 없다는 식의 주장이다. Diagonal colors가 같으면 optimal dual variable도 같아진다. 증명 직관은 WL refinement, matrix powers, spectral projectors, PDHG limit을 연결한다.

좋은 이론적 연결이지만, 이것은 finite-depth finite-width neural network가 항상 tight SDP bound를 예측한다는 보장이 아니다. Architecture가 Max-Cut SDP의 structural symmetry를 표현하기에 맞다는 보장에 가깝다.

셋째, branch-and-bound correctness는 valid upper bound와 feasible lower bound를 유지하기 때문에 나온다. Learned dual bound가 약하면 느려질 수 있다. 그래도 enumeration과 pruning이 제대로 구현되어 있으면 exactness는 유지된다.

## 강점

가장 큰 강점은 neural network가 들어간 위치다. Solver 주변에 heuristic을 하나 더 붙인 것이 아니라, relaxation oracle 자체를 대체하면서 exact solver가 필요로 하는 valid bound 성질을 보존했다.

두 번째 강점은 dual feasibility mechanism이 명확하다는 점이다. Penalty-based constrained learning은 infeasible prediction 가능성을 남긴다. 반면 여기서는 prediction 이후 PSD slack을 강제로 만든다. 그래서 branch-and-bound pruning rule이 보는 것은 hopeful estimate가 아니라 certified upper bound다.

세 번째 강점은 Max-Cut SDP의 구조를 잘 썼다는 점이다. Pairwise token은 matrix decision variable에 맞고, diagonal indicator는 diagonal equality constraint에 맞다. 단순히 graph-level predictor를 만든 것이 아니라 SDP 구조에 맞춘 architecture다.

Self-supervised training도 흥미롭다. 모든 training instance에 대해 solved SDP label을 만들지 않고 dual objective를 직접 optimize한다. 물론 evaluation과 baseline 비교에는 Mosek optimum이 필요하다.

## 약점과 조심할 점

가장 큰 약점은 이 논문이 아직 state-of-the-art Max-Cut solver 논문은 아니라는 점이다. Cutting plane을 쓰는 BiqCrunch류 full branch-and-cut solver는 일부 instance에서 여전히 훨씬 강하다. 따라서 이 연구의 claim은 "Max-Cut solver를 갈아엎었다"가 아니라 "base SDP relaxation evaluation을 feasibility-preserving GNN surrogate로 대체할 수 있다"에 가깝다.

두 번째 약점은 distribution dependence다. Training subgraph는 random branch-and-bound trajectory와 특정 graph family에서 만들어진다. Graph size, sparsity pattern, edge-weight distribution이 달라지면 bound quality가 나빠질 수 있다. Exactness는 남지만 speed-up은 사라질 수 있다.

세 번째로, dual feasibility는 tightness를 보장하지 않는다. 보장되는 것은 다음이다.

<math display="block" aria-label="Dual feasibility without approximation guarantee Korean">
  <msubsup><mi>f</mi><mtext>SDP</mtext><mo>*</mo></msubsup>
  <mo>&le;</mo>
  <msup><mi>e</mi><mo>&top;</mo></msup>
  <msub><mover><mi>y</mi><mo>^</mo></mover><mtext>feas</mtext></msub><mo>.</mo>
</math>

하지만 다음은 아니다.

<math display="block" aria-label="No tightness guarantee Korean">
  <msup><mi>e</mi><mo>&top;</mo></msup>
  <msub><mover><mi>y</mi><mo>^</mo></mover><mtext>feas</mtext></msub>
  <mo>-</mo>
  <msubsup><mi>f</mi><mtext>SDP</mtext><mo>*</mo></msubsup>
  <mo>&le;</mo>
  <mi>&epsilon;</mi><mo>.</mo>
</math>

Worst case에서는 bound가 너무 느슨해져 branch-and-bound tree가 크게 폭발할 수 있다.

Radial projection도 conservative하다. 모든 <math><msub><mi>y</mi><mi>i</mi></msub></math>에 같은 shift를 더하는 것은 싸고 안전하지만, objective를 필요 이상으로 키울 수 있다. 더 작은 diagonal correction을 찾는 layer를 만들 수도 있겠지만, 그러면 다시 optimization problem이 bound oracle 안에 들어간다. 이 논문은 tightest correction보다 cheap and safe correction을 선택한 것이다.

마지막으로 <math><msub><mi>&lambda;</mi><mi>min</mi></msub></math> 계산 비용이 완전히 사라지는 것은 아니다. 보고된 scale에서는 괜찮을 수 있지만, 훨씬 큰 graph에서는 approximate eigensolver와 feasibility tolerance가 중요한 implementation issue가 될 수 있다.

## References

Chen, H., Qian, C., Morris, C., Lodi, A., & Li, C. (2026). Solving Max-Cut to Global Optimality via Feasibility-Preserving Graph Neural Networks. arXiv preprint arXiv:2605.07113.
