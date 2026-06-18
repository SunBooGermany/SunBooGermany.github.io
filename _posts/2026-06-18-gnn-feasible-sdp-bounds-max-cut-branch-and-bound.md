---
layout: post
title: "Feasible GNN Bounds for Exact Max-Cut Branch-and-Bound"
title_ko: "Exact Max-Cut Branch-and-Bound를 위한 Feasible GNN Bound"
date: 2026-06-18
category: graph-represented-methods
category_label: "Graph-Represented Methods"
research_group: algorithmic_reviews
research_category: graph-represented-methods
research_category_label: "Graph-Represented Methods"
application_category: ""
application_category_label: ""
method_category: graph-represented-methods
method_category_label: "Graph-Represented Methods"
paper_title: ""
authors: ""
venue: ""
year: ""
doi: ""
arxiv: ""
source_url: ""
tags:
  - "max-cut"
  - "graph-neural-networks"
  - "semidefinite-programming"
  - "branch-and-bound"
  - "valid-bounds"
excerpt: "A note on a Max-Cut solver that replaces repeated SDP relaxation solves with a feasibility-preserving GNN surrogate, keeping branch-and-bound correctness by constructing dual-feasible upper bounds."
excerpt_ko: "Max-Cut branch-and-bound에서 반복되는 SDP relaxation solve를 feasibility-preserving GNN surrogate로 대체하되, dual-feasible upper bound를 만들어 exactness를 유지하는 접근을 정리한다."
language: "en-ko"
has_korean_note: false
---

## What Max-Cut Asks

For a weighted graph <math><mi>G</mi><mo>=</mo><mo>(</mo><mi>V</mi><mo>,</mo><mi>E</mi><mo>)</mo></math>, Max-Cut assigns each vertex to one of two partitions and maximizes the total weight of edges crossing the partition. With <math><msub><mi>x</mi><mi>i</mi></msub><mo>&isin;</mo><mo>{</mo><mo>-</mo><mn>1</mn><mo>,</mo><mn>1</mn><mo>}</mo></math>, one common Laplacian form is:

<math display="block" aria-label="Max-Cut quadratic objective">
  <munder><mo>max</mo><mrow><mi>x</mi><mo>&isin;</mo><msup><mrow><mo>{</mo><mo>-</mo><mn>1</mn><mo>,</mo><mn>1</mn><mo>}</mo></mrow><mi>n</mi></msup></mrow></munder>
  <mspace width="0.5em"></mspace>
  <mfrac><mn>1</mn><mn>4</mn></mfrac>
  <msup><mi>x</mi><mo>&top;</mo></msup>
  <mi>L</mi>
  <mi>x</mi><mo>.</mo>
</math>

The plain-language question is simple: which binary assignment makes as many important edges as possible disagree? This appears whenever the graph edge means "these two items prefer to be separated" or "separating this pair creates value." Typical examples include two-way clustering with dissimilarity rewards, graph partitioning subroutines, anti-ferromagnetic Ising or spin-glass energy minimization, certain VLSI and circuit-layout abstractions, and approximation subproblems inside combinatorial optimization.

The important detail is that Max-Cut is not asking for a good-looking partition in a vague sense. It is optimizing a precise discrete objective. Every vertex must choose one of two sides, and each edge contributes only when its endpoints land on opposite sides.

## Why It Is Hard

The difficulty is combinatorial. With <math><mi>n</mi></math> vertices, there are <math><msup><mn>2</mn><mi>n</mi></msup></math> binary assignments, up to a global sign flip. Local changes are misleading: moving one vertex may improve the cut for some incident edges while worsening it for others. Dense graphs, frustrated cycles, and mixed edge weights make the search landscape especially awkward.

Max-Cut is NP-hard, so exact solvers usually rely on branch-and-bound or branch-and-cut. At each node, the solver needs a lower bound from a feasible cut and an upper bound proving that a subtree cannot contain a better cut. SDP relaxations are attractive because they give strong upper bounds. They are also expensive when thousands or millions of branch-and-bound nodes must be evaluated.

This creates the bottleneck behind the paper: exact branch-and-bound may spend most of its time repeatedly solving similar SDP relaxations just to decide whether a node can be pruned.

## How GNNs Have Usually Been Used

Graphs are the native input object, so GNNs are a natural candidate for Max-Cut. Prior learning-based approaches usually use GNNs in one of three ways.

First, a GNN can predict a primal cut directly. This is useful as a heuristic: it may produce a good feasible solution quickly, and that feasible solution gives a lower bound for the maximization problem. But a good cut alone does not certify that no better cut exists.

Second, a GNN can guide a solver. It can suggest branching variables, rank candidate cuts, or choose which local search move to try. This can improve runtime, but the classical relaxation solver still supplies the certifying bounds.

Third, a GNN can approximate scores used inside a heuristic search. This can be fast, but if the score is not tied to feasibility or dual validity, it is hard to use safely inside an exact pruning rule.

So the usual GNN role is advisory or heuristic. That is useful, but it is not the same as replacing the relaxation evaluation itself.

## What Is Different Here

The interesting point in this paper is narrower: replace the repeated SDP relaxation solve inside branch-and-bound with a neural surrogate that still returns a valid bound.

That distinction matters. In exact branch-and-bound, a learned value predictor is dangerous if it can underestimate an upper bound. A fast but invalid bound can prune the optimal branch and destroy correctness. This work avoids that failure mode by making the GNN output dual-feasible SDP solutions after a projection step. The global optimality claim should therefore be read carefully. The neural network does not prove that it has found the optimal cut. It supplies a safe upper bound, and complete branch-and-bound keeps the exactness.

The computational bet is that evaluating more nodes with a cheap valid bound can be faster than evaluating fewer nodes with an expensive SDP solve. That bet only works if the learned bound remains valid. This paper is best understood as a feasibility-preserving neural bounding oracle for Max-Cut SDP relaxations.

## SDP Relaxation and the Role of the Dual

The Max-Cut SDP relaxation replaces binary variables with a positive semidefinite matrix <math><mi>X</mi></math> whose diagonal entries are one:

<math display="block" aria-label="Max-Cut SDP primal">
  <munder><mo>max</mo><mrow><mi>X</mi></mrow></munder>
  <mspace width="0.5em"></mspace>
  <mo>&lang;</mo><mi>L</mi><mo>,</mo><mi>X</mi><mo>&rang;</mo>
  <mspace width="0.5em"></mspace>
  <mtext>subject to</mtext>
  <mspace width="0.5em"></mspace>
  <mi>diag</mi><mo>(</mo><mi>X</mi><mo>)</mo><mo>=</mo><mi>e</mi><mo>,</mo>
  <mspace width="0.5em"></mspace>
  <mi>X</mi><mo>&succeq;</mo><mn>0</mn><mo>.</mo>
</math>

The corresponding dual can be written as:

<math display="block" aria-label="Max-Cut SDP dual">
  <munder><mo>min</mo><mrow><mi>y</mi><mo>,</mo><mi>S</mi></mrow></munder>
  <mspace width="0.5em"></mspace>
  <msup><mi>e</mi><mo>&top;</mo></msup><mi>y</mi>
  <mspace width="0.5em"></mspace>
  <mtext>subject to</mtext>
  <mspace width="0.5em"></mspace>
  <mi>L</mi><mo>-</mo><mi>Diag</mi><mo>(</mo><mi>y</mi><mo>)</mo><mo>+</mo><mi>S</mi><mo>=</mo><mn>0</mn><mo>,</mo>
  <mspace width="0.5em"></mspace>
  <mi>S</mi><mo>&succeq;</mo><mn>0</mn><mo>.</mo>
</math>

Equivalently, dual feasibility is:

<math display="block" aria-label="Dual feasibility condition">
  <mi>Diag</mi><mo>(</mo><mi>y</mi><mo>)</mo><mo>-</mo><mi>L</mi><mo>&succeq;</mo><mn>0</mn><mo>.</mo>
</math>

This is the key constraint. If <math><mi>y</mi></math> satisfies it, then <math><msup><mi>e</mi><mo>&top;</mo></msup><mi>y</mi></math> is a valid upper bound on the SDP optimum, hence also on the integer Max-Cut optimum inside the current branch-and-bound node. The GNN does not need to output the optimal dual solution. It needs to output a feasible one that is tight enough to be useful.

## What the GNN Is Asked to Predict

A standard node-level GNN is not an obvious fit for the SDP variable <math><mi>X</mi></math>, because <math><mi>X</mi></math> is not a vector of node labels. It is a matrix whose entries correspond to vertex pairs. The architecture therefore uses pairwise embeddings <math><msub><mi>h</mi><mrow><mi>i</mi><mi>j</mi></mrow></msub></math>.

The initial pairwise token contains information such as the objective matrix entry and whether the pair is diagonal:

<math display="block" aria-label="Pairwise token initialization">
  <msubsup><mi>h</mi><mrow><mi>i</mi><mi>j</mi></mrow><mn>0</mn></msubsup>
  <mo>=</mo>
  <mi>INIT</mi>
  <mo>(</mo>
  <msub><mi>C</mi><mrow><mi>i</mi><mi>j</mi></mrow></msub>
  <mo>,</mo>
  <msub><mi>I</mi><mrow><mi>i</mi><mo>=</mo><mi>j</mi></mrow></msub>
  <mo>)</mo><mo>.</mo>
</math>

This is more natural than a purely node-level representation. The SDP relaxation is built from pairwise correlations. If the network only stores <math><msub><mi>h</mi><mi>i</mi></msub></math>, it must reconstruct matrix-level structure indirectly. Pairwise tokens put the decision object closer to the representation.

The MC-MPNN update then lets an entry <math><mo>(</mo><mi>i</mi><mo>,</mo><mi>j</mi><mo>)</mo></math> aggregate information through intermediate indices <math><mi>u</mi></math>. The intuition is close to matrix multiplication: entry <math><mo>(</mo><mi>i</mi><mo>,</mo><mi>j</mi><mo>)</mo></math> is refined using information from entries <math><mo>(</mo><mi>i</mi><mo>,</mo><mi>u</mi><mo>)</mo></math> and <math><mo>(</mo><mi>u</mi><mo>,</mo><mi>j</mi><mo>)</mo></math>. The sparse variant, <math><mi>&delta;</mi></math>-MC-MPNN, restricts part of this aggregation to nonzero graph edges.

The architecture is therefore graph-represented in a precise sense: it does not only pass messages over vertices; it passes messages over pairwise objects that match the SDP matrix.

## Feasibility-Preserving Heads

The most important design choice is not the message passing layer by itself. It is the output parameterization.

For the primal SDP, the network predicts vectors <math><msub><mi>o</mi><mi>i</mi></msub></math> and normalizes them:

<math display="block" aria-label="Primal vector normalization">
  <msub><mi>o</mi><mi>i</mi></msub>
  <mo>&leftarrow;</mo>
  <mfrac>
    <msub><mover><mi>o</mi><mo>~</mo></mover><mi>i</mi></msub>
    <mrow><mo>||</mo><msub><mover><mi>o</mi><mo>~</mo></mover><mi>i</mi></msub><msub><mo>||</mo><mn>2</mn></msub></mrow>
  </mfrac><mo>.</mo>
</math>

Then it constructs:

<math display="block" aria-label="Primal Gram matrix construction">
  <msub><mover><mi>X</mi><mo>^</mo></mover><mrow><mi>i</mi><mi>j</mi></mrow></msub>
  <mo>=</mo>
  <msubsup><mi>o</mi><mi>i</mi><mo>&top;</mo></msubsup>
  <msub><mi>o</mi><mi>j</mi></msub><mo>.</mo>
</math>

This gives <math><mover><mi>X</mi><mo>^</mo></mover><mo>=</mo><mi>O</mi><msup><mi>O</mi><mo>&top;</mo></msup><mo>&succeq;</mo><mn>0</mn></math> and <math><msub><mover><mi>X</mi><mo>^</mo></mover><mrow><mi>i</mi><mi>i</mi></mrow></msub><mo>=</mo><mn>1</mn></math>. Primal feasibility follows from the construction, not from a penalty term in the loss.

For the dual, the network first predicts an unconstrained vector <math><mover><mi>y</mi><mo>^</mo></mover></math>. The raw slack matrix is:

<math display="block" aria-label="Raw dual slack matrix">
  <mover><mi>S</mi><mo>^</mo></mover>
  <mo>=</mo>
  <mi>Diag</mi><mo>(</mo><mover><mi>y</mi><mo>^</mo></mover><mo>)</mo>
  <mo>-</mo><mi>L</mi><mo>.</mo>
</math>

This raw matrix may not be positive semidefinite. The paper fixes that with a uniform eigenvalue shift:

<math display="block" aria-label="Radial dual projection">
  <mi>&delta;</mi>
  <mo>=</mo>
  <mi>max</mi>
  <mo>{</mo>
  <mn>0</mn><mo>,</mo>
  <mo>-</mo><msub><mi>&lambda;</mi><mi>min</mi></msub>
  <mo>(</mo><mover><mi>S</mi><mo>^</mo></mover><mo>)</mo>
  <mo>}</mo><mo>,</mo>
  <mspace width="0.5em"></mspace>
  <msub><mover><mi>y</mi><mo>^</mo></mover><mi>feas</mi></msub>
  <mo>=</mo>
  <mover><mi>y</mi><mo>^</mo></mover>
  <mo>+</mo>
  <mi>&delta;</mi><mi>e</mi><mo>.</mo>
</math>

The corrected slack is:

<math display="block" aria-label="Corrected slack matrix">
  <msub><mover><mi>S</mi><mo>^</mo></mover><mi>feas</mi></msub>
  <mo>=</mo>
  <mi>Diag</mi><mo>(</mo><msub><mover><mi>y</mi><mo>^</mo></mover><mi>feas</mi></msub><mo>)</mo>
  <mo>-</mo><mi>L</mi>
  <mo>=</mo>
  <mover><mi>S</mi><mo>^</mo></mover>
  <mo>+</mo><mi>&delta;</mi><mi>I</mi>
  <mo>&succeq;</mo><mn>0</mn><mo>.</mo>
</math>

The shift raises every eigenvalue by <math><mi>&delta;</mi></math>. If the smallest eigenvalue was negative, it is moved to zero. If the raw matrix was already PSD, nothing changes.

This is the mechanism that makes the bound safe.

## Why This Does Not Change the Dual Problem

A tempting objection is that shifting the dual variable might be solving a different problem. It does not. The original dual feasible set is still:

<math display="block" aria-label="Original dual feasible set">
  <mo>{</mo>
  <mi>y</mi>
  <mo>:</mo>
  <mi>Diag</mi><mo>(</mo><mi>y</mi><mo>)</mo><mo>-</mo><mi>L</mi><mo>&succeq;</mo><mn>0</mn>
  <mo>}</mo><mo>.</mo>
</math>

The raw GNN output may lie outside this set. The projection constructs a new candidate inside the same set. Once <math><msub><mover><mi>y</mi><mo>^</mo></mover><mi>feas</mi></msub></math> is feasible, its objective cannot be smaller than the dual optimum, because the dual is a minimization problem. By weak duality:

<math display="block" aria-label="Weak duality chain">
  <msubsup><mi>z</mi><mi>MaxCut</mi><mo>*</mo></msubsup>
  <mo>&le;</mo>
  <msubsup><mi>p</mi><mi>SDP</mi><mo>*</mo></msubsup>
  <mo>&le;</mo>
  <msubsup><mi>d</mi><mi>SDP</mi><mo>*</mo></msubsup>
  <mo>&le;</mo>
  <msup><mi>e</mi><mo>&top;</mo></msup>
  <msub><mover><mi>y</mi><mo>^</mo></mover><mi>feas</mi></msub><mo>.</mo>
</math>

So the corrected dual value is a valid upper bound for the original Max-Cut node. It may be loose, but it is safe. That is exactly the trade-off branch-and-bound can tolerate.

## How Exactness Is Preserved in Branch-and-Bound

For a maximization problem, branch-and-bound tracks an incumbent lower bound from the best feasible cut and an upper bound for each unresolved node. A node can be pruned only when its upper bound proves that it cannot beat the incumbent.

The classical solver obtains this upper bound by solving the SDP relaxation at the node. The neural solver instead evaluates:

<math display="block" aria-label="Neural branch and bound upper bound">
  <mi>UB</mi><mo>(</mo><mi>node</mi><mo>)</mo>
  <mo>=</mo>
  <msup><mi>e</mi><mo>&top;</mo></msup>
  <msub><mover><mi>y</mi><mo>^</mo></mover><mi>feas</mi></msub><mo>.</mo>
</math>

Because the value is dual feasible, a wrong low upper bound is not introduced. The worst case is different: if the bound is too conservative, fewer nodes are pruned, and the search may become slower. Correctness is protected; performance is empirical.

This is the cleanest lesson of the paper. A neural component can sit inside an exact optimization algorithm if the interface exposes the right certificate. Here the certificate is dual feasibility.

## Empirical Trade-Off

The reported results fit the expected pattern. The neural branch-and-bound evaluates more nodes than the vanilla SDP-based solver, because the learned upper bounds are typically looser than exact SDP optima. But each node is much cheaper to evaluate. On the reported Max-Cut instances, this gives speed-ups such as 5.6x on g05_60, 9.1x on g05_100, and 10.6x on w01_100 against the vanilla Mosek branch-and-bound baseline.

The GNN variant comparison is also informative. The sparse <math><mi>&delta;</mi></math>-MC-MPNN has a better asymptotic story, but the implementation still uses dense GPU operations. In the reported experiments, MC-MPNN and <math><mi>&delta;</mi></math>-MC-MPNN have similar objective gaps, and the dense MC-MPNN can be more stable in practice. The theoretical sparsity advantage does not automatically become wall-clock dominance.

This should temper the claim. The method is not presented as a full replacement for mature Max-Cut branch-and-cut solvers with cutting planes. Against solvers such as BiqCrunch with strong cuts, the neural method is not necessarily competitive. Its value is more specific: it shows that the SDP bounding step itself can be replaced by a learned surrogate without giving up validity.

## Limitations

The first limitation is bound tightness. Dual feasibility guarantees:

<math display="block" aria-label="GNN upper bound is above SDP optimum">
  <msubsup><mi>p</mi><mi>SDP</mi><mo>*</mo></msubsup>
  <mo>&le;</mo>
  <msub><mi>f</mi><mi>GNN</mi></msub><mo>,</mo>
</math>

but it does not guarantee:

<math display="block" aria-label="No approximation error guarantee">
  <msub><mi>f</mi><mi>GNN</mi></msub>
  <mo>-</mo>
  <msubsup><mi>p</mi><mi>SDP</mi><mo>*</mo></msubsup>
  <mo>&le;</mo>
  <mi>&epsilon;</mi><mo>.</mo>
</math>

If the GNN is poorly calibrated or out of distribution, the branch-and-bound tree may grow dramatically.

The second limitation is the projection itself. A uniform shift is cheap and safe, but it can be conservative. It increases the dual objective by <math><mi>n</mi><mi>&delta;</mi></math>. A more selective correction could be tighter, but computing it may reintroduce the optimization cost that the surrogate was meant to avoid.

The third limitation is distribution dependence. The training data are generated from graph families and branch-and-bound trajectories similar to those used in testing. For a practical solver, one would need to understand how the bound behaves across graph sizes, weight distributions, and structures not seen during training.

The fourth limitation is numerical. The certificate relies on the sign convention and on computing the smallest eigenvalue accurately enough. In implementation, a small positive tolerance is usually needed. A nearly feasible matrix with a slightly negative eigenvalue is harmless if corrected; an incorrectly accepted infeasible matrix is not.

## Why This Matters Beyond Max-Cut

The broader message is useful for optimization with learned components. If a neural network is inserted into a solver only as a value predictor, it can be fast and still unsafe. If it is inserted as a certificate-producing module, it can accelerate part of the algorithm while preserving the logic of the solver.

That idea transfers beyond Max-Cut. In decomposition, Benders-type methods, SDDP, robust optimization, stochastic programming, and mixed-integer nonlinear workflows, repeated relaxation or recourse evaluation is often the bottleneck. A black-box surrogate for those values is risky. A surrogate that preserves feasibility, dual validity, or certified bounds is much more interesting.

For graph-represented optimization, this paper gives a concrete pattern: match the representation to the structured decision variable, then force the output to satisfy the certificate required by the solver.

The GNN is not trusted because it is neural. It is trusted only after its output has been turned into a valid SDP dual point. That is the right level of skepticism.

<!-- ko -->

## Max-Cut은 무엇을 묻는가

가중 그래프 <math><mi>G</mi><mo>=</mo><mo>(</mo><mi>V</mi><mo>,</mo><mi>E</mi><mo>)</mo></math>에서 Max-Cut은 vertex를 두 partition으로 나누고, partition을 가로지르는 edge weight의 합을 최대화한다. <math><msub><mi>x</mi><mi>i</mi></msub><mo>&isin;</mo><mo>{</mo><mo>-</mo><mn>1</mn><mo>,</mo><mn>1</mn><mo>}</mo></math>를 쓰면 Laplacian 형태는 보통 다음처럼 쓸 수 있다.

<math display="block" aria-label="Max-Cut quadratic objective Korean">
  <munder><mo>max</mo><mrow><mi>x</mi><mo>&isin;</mo><msup><mrow><mo>{</mo><mo>-</mo><mn>1</mn><mo>,</mo><mn>1</mn><mo>}</mo></mrow><mi>n</mi></msup></mrow></munder>
  <mspace width="0.5em"></mspace>
  <mfrac><mn>1</mn><mn>4</mn></mfrac>
  <msup><mi>x</mi><mo>&top;</mo></msup>
  <mi>L</mi>
  <mi>x</mi><mo>.</mo>
</math>

말로 풀면 질문은 단순하다. 어떤 binary assignment가 중요한 edge들을 최대한 많이 갈라놓는가? 이 문제는 edge가 "두 항목은 분리되는 것이 좋다" 또는 "이 pair를 분리하면 가치가 생긴다"는 의미를 가질 때 등장한다. 대표적으로 dissimilarity reward가 있는 two-way clustering, graph partitioning subroutine, anti-ferromagnetic Ising 또는 spin-glass energy minimization, 일부 VLSI 및 circuit-layout abstraction, combinatorial optimization 내부의 approximation subproblem을 들 수 있다.

중요한 점은 Max-Cut이 막연히 좋아 보이는 partition을 찾는 문제가 아니라는 것이다. 정확한 discrete objective가 있다. 모든 vertex는 둘 중 한 side를 골라야 하고, edge는 양 끝 vertex가 서로 다른 side에 놓일 때만 objective에 기여한다.

## 왜 어려운가

어려움은 combinatorial하다. <math><mi>n</mi></math>개 vertex가 있으면 global sign flip을 제외하더라도 가능한 binary assignment 수가 <math><msup><mn>2</mn><mi>n</mi></msup></math> 규모로 커진다. Local change도 단순하지 않다. Vertex 하나를 옮기면 어떤 incident edge에서는 cut value가 좋아지지만 다른 edge에서는 나빠질 수 있다. Dense graph, frustrated cycle, mixed edge weight가 있으면 search landscape는 더 까다로워진다.

Max-Cut은 NP-hard이므로 exact solver는 보통 branch-and-bound 또는 branch-and-cut에 의존한다. 각 node에서는 feasible cut에서 나오는 lower bound와, 그 subtree가 더 좋은 해를 포함할 수 없음을 보이는 upper bound가 필요하다. SDP relaxation은 강한 upper bound를 제공하지만, branch-and-bound tree의 수많은 node마다 SDP를 풀어야 하면 비용이 커진다.

이 논문의 병목은 여기서 나온다. Exact branch-and-bound가 node를 prune할 수 있는지 판단하기 위해 비슷한 SDP relaxation을 반복해서 푸는 데 많은 시간을 쓴다.

## GNN은 기존에 어떻게 쓰였는가

Graph가 원래 input object이기 때문에 Max-Cut에 GNN을 쓰는 것은 자연스럽다. 기존 learning-based 접근은 보통 세 가지 방식으로 GNN을 사용한다.

첫째, GNN이 primal cut을 직접 예측할 수 있다. 이는 heuristic으로 유용하다. 빠르게 좋은 feasible solution을 만들 수 있고, 그 feasible solution은 maximization problem의 lower bound가 된다. 하지만 좋은 cut을 찾았다는 사실만으로 더 좋은 cut이 없다는 것을 증명할 수는 없다.

둘째, GNN이 solver를 guide할 수 있다. Branching variable을 추천하거나, candidate cut을 rank하거나, local search move를 고를 수 있다. Runtime을 줄일 수는 있지만, certifying bound는 여전히 classical relaxation solver가 제공한다.

셋째, GNN이 heuristic search 내부의 score를 근사할 수 있다. 빠를 수는 있지만, 그 score가 feasibility나 dual validity와 연결되어 있지 않으면 exact pruning rule 안에서 안전하게 쓰기 어렵다.

따라서 일반적인 GNN의 역할은 advisory 또는 heuristic에 가깝다. 유용하지만 relaxation evaluation 자체를 대체하는 것과는 다르다.

## 이 논문의 차이

이 논문에서 흥미로운 점은 더 좁다. Branch-and-bound 내부에서 반복적으로 풀어야 하는 SDP relaxation을 neural surrogate로 대체하되, 여전히 valid bound를 반환하게 만든다.

이 차이가 중요하다. Exact branch-and-bound에서는 learned value predictor가 upper bound를 과소평가할 수 있으면 위험하다. 빠르지만 invalid한 bound는 optimal branch를 잘못 prune할 수 있고, 그러면 exactness가 깨진다. 이 논문은 projection을 거친 dual-feasible SDP solution을 만들도록 해서 이 실패 모드를 피한다. 따라서 여기서 말하는 global optimality는 신경망이 최적 cut을 직접 증명한다는 뜻이 아니다. 신경망은 안전한 upper bound를 제공하고, complete branch-and-bound가 exactness를 유지한다.

계산적 가설은 조금 더 많은 node를 보더라도 cheap valid bound로 평가하면, 더 적은 node를 expensive SDP solve로 평가하는 것보다 빠를 수 있다는 것이다. 단, 이 가설은 learned bound가 valid할 때만 의미가 있다. 그래서 이 논문은 Max-Cut SDP relaxation을 위한 feasibility-preserving neural bounding oracle로 읽는 것이 가장 정확하다.

## SDP Relaxation과 Dual의 역할

Max-Cut SDP relaxation은 binary variable을 diagonal이 1인 positive semidefinite matrix <math><mi>X</mi></math>로 바꾼다.

<math display="block" aria-label="Max-Cut SDP primal Korean">
  <munder><mo>max</mo><mrow><mi>X</mi></mrow></munder>
  <mspace width="0.5em"></mspace>
  <mo>&lang;</mo><mi>L</mi><mo>,</mo><mi>X</mi><mo>&rang;</mo>
  <mspace width="0.5em"></mspace>
  <mtext>subject to</mtext>
  <mspace width="0.5em"></mspace>
  <mi>diag</mi><mo>(</mo><mi>X</mi><mo>)</mo><mo>=</mo><mi>e</mi><mo>,</mo>
  <mspace width="0.5em"></mspace>
  <mi>X</mi><mo>&succeq;</mo><mn>0</mn><mo>.</mo>
</math>

그 dual은 다음처럼 쓸 수 있다.

<math display="block" aria-label="Max-Cut SDP dual Korean">
  <munder><mo>min</mo><mrow><mi>y</mi><mo>,</mo><mi>S</mi></mrow></munder>
  <mspace width="0.5em"></mspace>
  <msup><mi>e</mi><mo>&top;</mo></msup><mi>y</mi>
  <mspace width="0.5em"></mspace>
  <mtext>subject to</mtext>
  <mspace width="0.5em"></mspace>
  <mi>L</mi><mo>-</mo><mi>Diag</mi><mo>(</mo><mi>y</mi><mo>)</mo><mo>+</mo><mi>S</mi><mo>=</mo><mn>0</mn><mo>,</mo>
  <mspace width="0.5em"></mspace>
  <mi>S</mi><mo>&succeq;</mo><mn>0</mn><mo>.</mo>
</math>

동치로 dual feasibility는 다음 조건이다.

<math display="block" aria-label="Dual feasibility condition Korean">
  <mi>Diag</mi><mo>(</mo><mi>y</mi><mo>)</mo><mo>-</mo><mi>L</mi><mo>&succeq;</mo><mn>0</mn><mo>.</mo>
</math>

이 제약이 핵심이다. <math><mi>y</mi></math>가 이 조건을 만족하면 <math><msup><mi>e</mi><mo>&top;</mo></msup><mi>y</mi></math>는 SDP optimum에 대한 valid upper bound이고, 따라서 해당 branch-and-bound node 안의 integer Max-Cut optimum에 대해서도 upper bound다. GNN이 optimal dual solution을 출력할 필요는 없다. Feasible하면서 충분히 tight한 dual solution을 만들면 된다.

## GNN이 예측하는 대상

일반 node-level GNN은 SDP variable <math><mi>X</mi></math>와 잘 맞지 않는다. <math><mi>X</mi></math>는 node label vector가 아니라 vertex pair에 대응하는 matrix이기 때문이다. 그래서 이 architecture는 pairwise embedding <math><msub><mi>h</mi><mrow><mi>i</mi><mi>j</mi></mrow></msub></math>를 쓴다.

초기 pairwise token은 objective matrix entry와 diagonal 여부 같은 정보를 포함한다.

<math display="block" aria-label="Pairwise token initialization Korean">
  <msubsup><mi>h</mi><mrow><mi>i</mi><mi>j</mi></mrow><mn>0</mn></msubsup>
  <mo>=</mo>
  <mi>INIT</mi>
  <mo>(</mo>
  <msub><mi>C</mi><mrow><mi>i</mi><mi>j</mi></mrow></msub>
  <mo>,</mo>
  <msub><mi>I</mi><mrow><mi>i</mi><mo>=</mo><mi>j</mi></mrow></msub>
  <mo>)</mo><mo>.</mo>
</math>

이는 순수 node-level representation보다 자연스럽다. SDP relaxation은 pairwise correlation으로 이루어져 있다. 네트워크가 <math><msub><mi>h</mi><mi>i</mi></msub></math>만 저장하면 matrix-level structure를 간접적으로 복원해야 한다. Pairwise token은 decision object와 representation을 더 가깝게 맞춘다.

MC-MPNN update는 entry <math><mo>(</mo><mi>i</mi><mo>,</mo><mi>j</mi><mo>)</mo></math>가 intermediate index <math><mi>u</mi></math>를 통해 정보를 aggregate하게 한다. 직관은 matrix multiplication과 가깝다. Entry <math><mo>(</mo><mi>i</mi><mo>,</mo><mi>j</mi><mo>)</mo></math>가 <math><mo>(</mo><mi>i</mi><mo>,</mo><mi>u</mi><mo>)</mo></math>와 <math><mo>(</mo><mi>u</mi><mo>,</mo><mi>j</mi><mo>)</mo></math>의 정보를 통해 refined된다. Sparse variant인 <math><mi>&delta;</mi></math>-MC-MPNN은 이 aggregation의 일부를 nonzero graph edge로 제한한다.

따라서 이 architecture는 정확한 의미에서 graph-represented method다. Vertex 위에서만 message passing을 하는 것이 아니라, SDP matrix와 맞는 pairwise object 위에서 message passing을 한다.

## Feasibility-Preserving Head

가장 중요한 설계는 message passing layer 자체보다 output parameterization이다.

Primal SDP에 대해서는 network가 vector <math><msub><mi>o</mi><mi>i</mi></msub></math>를 예측하고 normalize한다.

<math display="block" aria-label="Primal vector normalization Korean">
  <msub><mi>o</mi><mi>i</mi></msub>
  <mo>&leftarrow;</mo>
  <mfrac>
    <msub><mover><mi>o</mi><mo>~</mo></mover><mi>i</mi></msub>
    <mrow><mo>||</mo><msub><mover><mi>o</mi><mo>~</mo></mover><mi>i</mi></msub><msub><mo>||</mo><mn>2</mn></msub></mrow>
  </mfrac><mo>.</mo>
</math>

그다음 다음 matrix를 만든다.

<math display="block" aria-label="Primal Gram matrix construction Korean">
  <msub><mover><mi>X</mi><mo>^</mo></mover><mrow><mi>i</mi><mi>j</mi></mrow></msub>
  <mo>=</mo>
  <msubsup><mi>o</mi><mi>i</mi><mo>&top;</mo></msubsup>
  <msub><mi>o</mi><mi>j</mi></msub><mo>.</mo>
</math>

그러면 <math><mover><mi>X</mi><mo>^</mo></mover><mo>=</mo><mi>O</mi><msup><mi>O</mi><mo>&top;</mo></msup><mo>&succeq;</mo><mn>0</mn></math>이고 <math><msub><mover><mi>X</mi><mo>^</mo></mover><mrow><mi>i</mi><mi>i</mi></mrow></msub><mo>=</mo><mn>1</mn></math>이다. Primal feasibility는 loss penalty에서 나오는 것이 아니라 construction에서 나온다.

Dual에 대해서는 network가 먼저 unconstrained vector <math><mover><mi>y</mi><mo>^</mo></mover></math>를 예측한다. Raw slack matrix는 다음이다.

<math display="block" aria-label="Raw dual slack matrix Korean">
  <mover><mi>S</mi><mo>^</mo></mover>
  <mo>=</mo>
  <mi>Diag</mi><mo>(</mo><mover><mi>y</mi><mo>^</mo></mover><mo>)</mo>
  <mo>-</mo><mi>L</mi><mo>.</mo>
</math>

이 raw matrix는 PSD가 아닐 수 있다. 논문은 uniform eigenvalue shift로 이를 고친다.

<math display="block" aria-label="Radial dual projection Korean">
  <mi>&delta;</mi>
  <mo>=</mo>
  <mi>max</mi>
  <mo>{</mo>
  <mn>0</mn><mo>,</mo>
  <mo>-</mo><msub><mi>&lambda;</mi><mi>min</mi></msub>
  <mo>(</mo><mover><mi>S</mi><mo>^</mo></mover><mo>)</mo>
  <mo>}</mo><mo>,</mo>
  <mspace width="0.5em"></mspace>
  <msub><mover><mi>y</mi><mo>^</mo></mover><mi>feas</mi></msub>
  <mo>=</mo>
  <mover><mi>y</mi><mo>^</mo></mover>
  <mo>+</mo>
  <mi>&delta;</mi><mi>e</mi><mo>.</mo>
</math>

Corrected slack은 다음이다.

<math display="block" aria-label="Corrected slack matrix Korean">
  <msub><mover><mi>S</mi><mo>^</mo></mover><mi>feas</mi></msub>
  <mo>=</mo>
  <mi>Diag</mi><mo>(</mo><msub><mover><mi>y</mi><mo>^</mo></mover><mi>feas</mi></msub><mo>)</mo>
  <mo>-</mo><mi>L</mi>
  <mo>=</mo>
  <mover><mi>S</mi><mo>^</mo></mover>
  <mo>+</mo><mi>&delta;</mi><mi>I</mi>
  <mo>&succeq;</mo><mn>0</mn><mo>.</mo>
</math>

Shift는 모든 eigenvalue를 <math><mi>&delta;</mi></math>만큼 올린다. 최소 eigenvalue가 음수였다면 0까지 올라간다. 이미 PSD였다면 아무 변화도 없다.

이 mechanism이 bound를 안전하게 만든다.

## 이것은 Dual Problem을 바꾸는 것이 아니다

한 가지 자연스러운 의문은 dual variable을 shift하면 다른 문제를 푸는 것이 아닌가 하는 것이다. 그렇지 않다. 원래 dual feasible set은 그대로 다음이다.

<math display="block" aria-label="Original dual feasible set Korean">
  <mo>{</mo>
  <mi>y</mi>
  <mo>:</mo>
  <mi>Diag</mi><mo>(</mo><mi>y</mi><mo>)</mo><mo>-</mo><mi>L</mi><mo>&succeq;</mo><mn>0</mn>
  <mo>}</mo><mo>.</mo>
</math>

Raw GNN output이 이 set 밖에 있을 수 있다. Projection은 같은 feasible set 안에 들어가는 새 candidate를 만드는 것이다. <math><msub><mover><mi>y</mi><mo>^</mo></mover><mi>feas</mi></msub></math>가 feasible이면, dual은 minimization problem이므로 그 objective는 dual optimum보다 작을 수 없다. Weak duality에 의해 다음이 성립한다.

<math display="block" aria-label="Weak duality chain Korean">
  <msubsup><mi>z</mi><mi>MaxCut</mi><mo>*</mo></msubsup>
  <mo>&le;</mo>
  <msubsup><mi>p</mi><mi>SDP</mi><mo>*</mo></msubsup>
  <mo>&le;</mo>
  <msubsup><mi>d</mi><mi>SDP</mi><mo>*</mo></msubsup>
  <mo>&le;</mo>
  <msup><mi>e</mi><mo>&top;</mo></msup>
  <msub><mover><mi>y</mi><mo>^</mo></mover><mi>feas</mi></msub><mo>.</mo>
</math>

따라서 corrected dual value는 원래 Max-Cut node에 대한 valid upper bound다. 느슨할 수는 있지만 안전하다. Branch-and-bound가 받아들일 수 있는 trade-off는 바로 이것이다.

## Branch-and-Bound에서 Exactness가 유지되는 이유

Maximization problem에서 branch-and-bound는 best feasible cut에서 나온 incumbent lower bound와, 각 unresolved node의 upper bound를 추적한다. 어떤 node의 upper bound가 incumbent를 이길 수 없다는 것을 보일 때만 prune할 수 있다.

Classical solver는 해당 node의 SDP relaxation을 풀어서 이 upper bound를 얻는다. Neural solver는 대신 다음 값을 쓴다.

<math display="block" aria-label="Neural branch and bound upper bound Korean">
  <mi>UB</mi><mo>(</mo><mi>node</mi><mo>)</mo>
  <mo>=</mo>
  <msup><mi>e</mi><mo>&top;</mo></msup>
  <msub><mover><mi>y</mi><mo>^</mo></mover><mi>feas</mi></msub><mo>.</mo>
</math>

이 값은 dual feasible이므로 잘못 낮은 upper bound가 들어오지 않는다. 최악의 경우는 다르다. Bound가 너무 보수적이면 pruning이 덜 되고 search가 느려진다. Correctness는 보호되고, performance는 empirical 문제로 남는다.

이 논문의 가장 깨끗한 교훈은 여기에 있다. Neural component가 exact optimization algorithm 안에 들어가려면, solver가 요구하는 certificate를 interface로 내놓아야 한다. 여기서는 그 certificate가 dual feasibility다.

## 실험적 Trade-Off

보고된 결과는 예상한 패턴과 맞다. Neural branch-and-bound는 vanilla SDP-based solver보다 더 많은 node를 평가한다. Learned upper bound가 exact SDP optimum보다 보통 느슨하기 때문이다. 하지만 각 node evaluation이 훨씬 싸다. 보고된 Max-Cut instance에서는 vanilla Mosek branch-and-bound baseline 대비 g05_60에서 5.6x, g05_100에서 9.1x, w01_100에서 10.6x 같은 speed-up이 나온다.

GNN variant 비교도 흥미롭다. Sparse <math><mi>&delta;</mi></math>-MC-MPNN은 asymptotic 관점에서 더 좋은 이야기를 갖지만, 실제 구현은 dense GPU operation을 사용한다. 실험에서는 MC-MPNN과 <math><mi>&delta;</mi></math>-MC-MPNN의 objective gap이 비슷하고, dense MC-MPNN이 더 안정적일 수 있다. 이론적 sparsity advantage가 곧바로 wall-clock dominance가 되는 것은 아니다.

따라서 claim은 조심해야 한다. 이 방법은 strong cutting plane을 가진 성숙한 Max-Cut branch-and-cut solver를 완전히 대체한다고 보기 어렵다. BiqCrunch 같은 solver와 비교하면 neural method가 반드시 경쟁적이지 않다. 이 논문의 가치는 더 구체적이다. SDP bounding step 자체를 learned surrogate로 대체하되 validity를 포기하지 않을 수 있음을 보인 것이다.

## 한계

첫 번째 한계는 bound tightness다. Dual feasibility는 다음을 보장한다.

<math display="block" aria-label="GNN upper bound is above SDP optimum Korean">
  <msubsup><mi>p</mi><mi>SDP</mi><mo>*</mo></msubsup>
  <mo>&le;</mo>
  <msub><mi>f</mi><mi>GNN</mi></msub><mo>,</mo>
</math>

하지만 다음을 보장하지는 않는다.

<math display="block" aria-label="No approximation error guarantee Korean">
  <msub><mi>f</mi><mi>GNN</mi></msub>
  <mo>-</mo>
  <msubsup><mi>p</mi><mi>SDP</mi><mo>*</mo></msubsup>
  <mo>&le;</mo>
  <mi>&epsilon;</mi><mo>.</mo>
</math>

GNN이 잘 calibration되지 않았거나 out-of-distribution graph를 만나면 branch-and-bound tree가 크게 커질 수 있다.

두 번째 한계는 projection 자체다. Uniform shift는 싸고 안전하지만 보수적일 수 있다. Dual objective를 <math><mi>n</mi><mi>&delta;</mi></math>만큼 증가시킨다. 더 선택적인 correction은 tighter할 수 있지만, 그것을 계산하려면 surrogate가 피하려던 optimization cost가 다시 들어올 수 있다.

세 번째 한계는 distribution dependence다. Training data는 test와 유사한 graph family 및 branch-and-bound trajectory에서 생성된다. 실제 solver로 쓰려면 graph size, weight distribution, unseen structure가 바뀌었을 때 bound가 어떻게 변하는지 이해해야 한다.

네 번째 한계는 numerical issue다. Certificate는 sign convention과 minimum eigenvalue 계산에 의존한다. 구현에서는 작은 positive tolerance가 필요할 가능성이 높다. 거의 feasible한 matrix를 조금 보정하는 것은 괜찮지만, infeasible matrix를 feasible하다고 잘못 받아들이면 위험하다.

## Max-Cut 밖에서의 의미

더 넓은 메시지는 learned component를 optimization에 넣을 때 유용하다. Neural network가 단순 value predictor로 solver 안에 들어가면 빠르더라도 안전하지 않을 수 있다. 반대로 certificate를 만들어내는 module로 들어가면, solver logic을 유지하면서 일부 병목을 가속할 수 있다.

이 생각은 Max-Cut 밖으로도 옮겨갈 수 있다. Decomposition, Benders-type method, SDDP, robust optimization, stochastic programming, mixed-integer nonlinear workflow에서는 반복적인 relaxation 또는 recourse evaluation이 병목인 경우가 많다. 이런 값을 black-box surrogate로 대체하는 것은 위험하다. Feasibility, dual validity, certified bound를 보존하는 surrogate가 훨씬 흥미롭다.

Graph-represented optimization 관점에서 이 논문은 구체적인 pattern을 준다. Structured decision variable에 맞춰 representation을 설계하고, solver가 요구하는 certificate를 output에서 강제로 만족시킨다.

GNN은 neural이기 때문에 신뢰되는 것이 아니다. 그 output이 원래 SDP dual feasible point로 변환된 뒤에야 신뢰된다. 이 정도의 회의성이 맞다.
