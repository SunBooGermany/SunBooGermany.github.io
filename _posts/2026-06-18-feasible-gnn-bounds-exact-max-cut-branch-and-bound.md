---
layout: post
title: "Feasibility-Preserving GNN Bounds for Exact Max-Cut"
title_ko: "Exact Max-Cut을 위한 feasibility-preserving GNN bound"
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
excerpt: "A critical note on using feasibility-preserving graph neural networks as SDP bound surrogates inside exact Max-Cut branch-and-bound."
excerpt_ko: "Exact Max-Cut branch-and-bound 내부의 SDP bound 계산을 feasibility-preserving graph neural network surrogate로 대체하는 접근에 대한 비판적 정리."
language: "en-ko"
has_korean_note: false
---

This paper is easy to misread. It is not claiming that a graph neural network directly solves Max-Cut to optimality. The claim is narrower: inside an exact branch-and-bound solver, the repeated SDP relaxation solve can be replaced by a learned surrogate, provided that the surrogate returns a valid upper bound.

That qualification is the paper's core. In branch-and-bound, a learned bound predictor is dangerous if it can be too optimistic. One wrong upper bound can prune the branch containing the optimum. Chen et al. avoid that failure mode by forcing the neural output to satisfy dual feasibility. The learned bound can be loose. It should not be invalid.

## The bottleneck

For a weighted graph <math><mi>G</mi><mo>=</mo><mo>(</mo><mi>V</mi><mo>,</mo><mi>E</mi><mo>)</mo></math>, Max-Cut asks for a bipartition of the vertices that maximizes the weight of crossing edges. With binary signs <math><msub><mi>x</mi><mi>i</mi></msub><mo>&isin;</mo><mo>{</mo><mo>-</mo><mn>1</mn><mo>,</mo><mn>1</mn><mo>}</mo></math>, a standard form is:

<math display="block" aria-label="Max-Cut objective">
  <munder><mi>max</mi><mrow><mi>x</mi><mo>&isin;</mo><msup><mrow><mo>{</mo><mo>-</mo><mn>1</mn><mo>,</mo><mn>1</mn><mo>}</mrow><mi>n</mi></msup></mrow></munder>
  <mspace width="0.5em"></mspace>
  <mfrac><mn>1</mn><mn>4</mn></mfrac>
  <msup><mi>x</mi><mo>&top;</mo></msup><mi>L</mi><mi>x</mi><mo>.</mo>
</math>

The exact problem is NP-complete, so high-quality exact solvers rely on enumeration plus strong bounds. A common bound comes from the Goemans-Williamson SDP relaxation. The relaxation is useful because its dual solution gives a certificate: if the dual slack matrix is positive semidefinite, the dual objective is an upper bound on the best cut value.

The computational problem is that branch-and-bound needs this kind of upper bound at many nodes. Solving an SDP repeatedly can dominate runtime. The paper targets that repeated relaxation evaluation, not the branching rule itself.

## The certificate

The Max-Cut SDP introduces a matrix variable <math><mi>X</mi></math> that should be positive semidefinite with unit diagonal:

<math display="block" aria-label="Max-Cut SDP primal feasibility">
  <mi>X</mi><mo>&succeq;</mo><mn>0</mn>
  <mo>,</mo>
  <mspace width="0.5em"></mspace>
  <mi>diag</mi><mo>(</mo><mi>X</mi><mo>)</mo><mo>=</mo><mi>e</mi><mo>.</mo>
</math>

The dual side can be written in terms of a vector <math><mi>y</mi></math> and a slack matrix:

<math display="block" aria-label="Max-Cut SDP dual slack">
  <mi>S</mi><mo>=</mo><mi>Diag</mi><mo>(</mo><mi>y</mi><mo>)</mo><mo>-</mo><mi>L</mi>
  <mo>&succeq;</mo><mn>0</mn><mo>.</mo>
</math>

If this condition holds, weak duality gives:

<math display="block" aria-label="Dual upper bound">
  <msubsup><mi>f</mi><mtext>SDP</mtext><mo>*</mo></msubsup>
  <mo>&le;</mo>
  <msup><mi>e</mi><mo>&top;</mo></msup><mi>y</mi><mo>.</mo>
</math>

This is the object the neural network must preserve. A small prediction error is not the main issue. A violation of the certificate is.

## Why the GNN is pairwise

A node-level GNN is not a natural fit for this SDP. The main decision object is not a vertex label but a matrix entry <math><msub><mi>X</mi><mrow><mi>i</mi><mi>j</mi></mrow></msub></math>. The paper therefore uses pairwise tokens:

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

The diagonal indicator matters because the SDP constraints are exactly diagonal constraints. This is a Max-Cut-specific design choice, not just a generic graph representation trick.

The message passing update refines each pair using information from related row and column entries. This resembles the way matrix powers mix entries through intermediate vertices. The sparse variant, <math><mi>&delta;</mi></math>-MC-MPNN, restricts aggregation to nonzero graph entries and is intended to reduce the cost relative to generic higher-order SDP architectures. The paper notes, however, that dense GPU operations can still be faster in practice, so the sparse complexity story should not be read as a guaranteed wall-clock advantage.

## How feasibility is preserved

The primal head predicts vectors <math><msub><mi>o</mi><mi>i</mi></msub></math>, normalizes them, and constructs:

<math display="block" aria-label="Primal feasible construction">
  <mover><mi>X</mi><mo>^</mo></mover>
  <mo>=</mo>
  <mi>O</mi><msup><mi>O</mi><mo>&top;</mo></msup>
  <mo>,</mo>
  <mspace width="0.5em"></mspace>
  <msub><mover><mi>X</mi><mo>^</mo></mover><mrow><mi>i</mi><mi>i</mi></mrow></msub>
  <mo>=</mo><mn>1</mn><mo>.</mo>
</math>

This guarantees primal SDP feasibility by construction. It is a low-rank parameterization, so it may restrict the primal solution class. But for branch-and-bound correctness, the dual bound is the more critical part.

For the dual side, the network first predicts a raw vector <math><mover><mi>y</mi><mo>^</mo></mover></math>. The associated slack

<math display="block" aria-label="Raw dual slack">
  <mover><mi>S</mi><mo>^</mo></mover>
  <mo>=</mo>
  <mi>Diag</mi><mo>(</mo><mover><mi>y</mi><mo>^</mo></mover><mo>)</mo><mo>-</mo><mi>L</mi>
</math>

may not be PSD. The paper fixes this with a uniform radial shift:

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

After this correction, the new slack matrix is PSD. Therefore <math><msup><mi>e</mi><mo>&top;</mo></msup><msub><mover><mi>y</mi><mo>^</mo></mover><mtext>feas</mtext></msub></math> is a valid upper bound. This is the main reason the learned component can be placed inside an exact solver.

## Exactness and speed are different claims

The branch-and-bound logic is simple. For each node <math><mi>c</mi></math>, maintain a feasible incumbent lower bound <math><mi>LB</mi></math> and an upper bound <math><msub><mi>UB</mi><mi>c</mi></msub></math>. If a node cannot improve the incumbent, it can be pruned.

With the neural bound:

<math display="block" aria-label="Neural branch-and-bound upper bound">
  <msub><mi>UB</mi><mi>c</mi></msub>
  <mo>=</mo>
  <msup><mi>e</mi><mo>&top;</mo></msup>
  <msub><mover><mi>y</mi><mo>^</mo></mover><mtext>feas</mtext></msub><mo>.</mo>
</math>

Because this is dual feasible, it is safe. It can be weaker than the exact SDP bound, so it may prune fewer nodes. The solver remains exact because it has not used an invalid upper bound. The cost is potentially more enumeration.

This distinction should be kept sharp:

The feasibility projection supports correctness. It does not prove fast runtime.

Speed depends on an empirical trade-off: the GNN bound must be much cheaper than solving the SDP, while still tight enough that the branch-and-bound tree does not explode.

## What the experiments show

The reported results support that trade-off on the tested instance families. The neural solver evaluates more nodes than the vanilla SDP-based branch-and-bound solver, but each node is cheaper. The supplied notes report examples such as:

| Instance | Vanilla time | Neural time | Speed-up |
|---|---:|---:|---:|
| g05_60 | 53.1 s | 9.5 s | 5.6x |
| g05_80 | 1170.3 s | 155.7 s | 7.5x |
| g05_100 | 40930.1 s | 4509.3 s | 9.1x |
| pm1s_100 | 10382.5 s | 1058.2 s | 9.8x |
| w01_100 | 11348.6 s | 1073.9 s | 10.6x |

The paper also compares MC-MPNN and <math><mi>&delta;</mi></math>-MC-MPNN on synthetic graph distributions. Their objective gaps are close in the reported settings. The sparse variant is theoretically appealing, but the dense variant can be competitive or better under dense GPU implementation.

## Limits

The strongest limitation is that this is not a state-of-the-art Max-Cut solver result. Full branch-and-cut solvers with cutting planes, such as BiqCrunch-style methods, remain much stronger on some instances. The paper is better read as a proof of concept for replacing a base SDP relaxation evaluation with a certified neural surrogate.

The second limitation is distribution dependence. Training instances and branch-and-bound subgraphs come from particular graph families. If graph size, sparsity, or weight distribution changes, the learned bound may become loose. Exactness would remain, but the speed-up could disappear.

The third limitation is the radial projection itself. A uniform shift is cheap and safe, but it can be conservative. It may increase every component of <math><mi>y</mi></math> even when a more selective diagonal correction would suffice. That makes the upper bound looser.

Finally, the method still needs an eigenvalue computation for <math><msub><mi>&lambda;</mi><mi>min</mi></msub></math>. At the reported scale this may not dominate, but it is not free. For larger graphs, this correction step and its numerical tolerance would become part of the solver engineering problem.

My reading is therefore: this paper is valuable because it identifies the right interface between learning and exact optimization. The learned model is useful only because it returns a certificate-compatible object. That is more disciplined than learning a cut value and hoping the solver remains safe.

## References

Chen, H., Qian, C., Morris, C., Lodi, A., & Li, C. (2026). Solving Max-Cut to Global Optimality via Feasibility-Preserving Graph Neural Networks. arXiv preprint arXiv:2605.07113.

<!-- ko -->

이 논문은 GNN이 Max-Cut 최적해를 직접 찾아낸다는 주장을 하는 논문이 아니다. 핵심은 더 좁다. Exact branch-and-bound solver 안에서 반복적으로 풀리는 SDP relaxation을 learned surrogate로 대체하되, 그 surrogate가 valid upper bound를 반환하도록 만드는 것이다.

이 조건이 중요하다. Branch-and-bound에서 learned bound predictor가 잘못 낙관적인 값을 내면 optimum이 들어 있는 branch를 지울 수 있다. Chen et al.은 neural output을 dual feasible하게 보정해서 이 실패 모드를 피한다. Bound가 느슨할 수는 있다. 하지만 invalid하면 안 된다.

## 병목

Weighted graph <math><mi>G</mi><mo>=</mo><mo>(</mo><mi>V</mi><mo>,</mo><mi>E</mi><mo>)</mo></math>에서 Max-Cut은 vertex를 두 partition으로 나누어 crossing edge weight 합을 최대화하는 문제다. Binary sign <math><msub><mi>x</mi><mi>i</mi></msub><mo>&isin;</mo><mo>{</mo><mo>-</mo><mn>1</mn><mo>,</mo><mn>1</mn><mo>}</mo></math>를 쓰면 한 가지 표준 형태는 다음과 같다.

<math display="block" aria-label="Max-Cut objective Korean">
  <munder><mi>max</mi><mrow><mi>x</mi><mo>&isin;</mo><msup><mrow><mo>{</mo><mo>-</mo><mn>1</mn><mo>,</mo><mn>1</mn><mo>}</mrow><mi>n</mi></msup></mrow></munder>
  <mspace width="0.5em"></mspace>
  <mfrac><mn>1</mn><mn>4</mn></mfrac>
  <msup><mi>x</mi><mo>&top;</mo></msup><mi>L</mi><mi>x</mi><mo>.</mo>
</math>

Exact Max-Cut은 NP-complete이므로 강한 bound와 enumeration을 결합해야 한다. Goemans-Williamson SDP relaxation은 여기서 중요한 bound를 제공한다. 특히 dual solution이 positive semidefinite slack을 가지면 dual objective가 valid upper bound가 된다.

문제는 이 upper bound를 branch-and-bound의 많은 node에서 반복적으로 계산해야 한다는 점이다. SDP를 반복해서 푸는 비용이 전체 runtime을 지배할 수 있다. 이 논문은 branching rule이 아니라 relaxation evaluation 자체를 겨냥한다.

## 필요한 certificate

Max-Cut SDP는 positive semidefinite matrix <math><mi>X</mi></math>와 unit diagonal constraint를 사용한다.

<math display="block" aria-label="Max-Cut SDP primal feasibility Korean">
  <mi>X</mi><mo>&succeq;</mo><mn>0</mn>
  <mo>,</mo>
  <mspace width="0.5em"></mspace>
  <mi>diag</mi><mo>(</mo><mi>X</mi><mo>)</mo><mo>=</mo><mi>e</mi><mo>.</mo>
</math>

Dual은 vector <math><mi>y</mi></math>와 slack matrix로 볼 수 있다.

<math display="block" aria-label="Max-Cut SDP dual slack Korean">
  <mi>S</mi><mo>=</mo><mi>Diag</mi><mo>(</mo><mi>y</mi><mo>)</mo><mo>-</mo><mi>L</mi>
  <mo>&succeq;</mo><mn>0</mn><mo>.</mo>
</math>

이 조건이 성립하면 weak duality에 의해 다음 upper bound가 나온다.

<math display="block" aria-label="Dual upper bound Korean">
  <msubsup><mi>f</mi><mtext>SDP</mtext><mo>*</mo></msubsup>
  <mo>&le;</mo>
  <msup><mi>e</mi><mo>&top;</mo></msup><mi>y</mi><mo>.</mo>
</math>

Neural network가 보존해야 하는 것은 바로 이 certificate다. 작은 prediction error보다 certificate violation이 더 위험하다.

## 왜 pairwise GNN인가

일반 node-level GNN은 이 SDP에 잘 맞지 않는다. 중요한 decision object는 vertex label이 아니라 matrix entry <math><msub><mi>X</mi><mrow><mi>i</mi><mi>j</mi></mrow></msub></math>다. 그래서 논문은 pairwise token을 사용한다.

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

Diagonal indicator는 중요하다. Max-Cut SDP의 constraint가 diagonal constraint이기 때문이다. 이는 generic graph predictor가 아니라 Max-Cut SDP 구조에 맞춘 설계다.

Message passing은 각 pair를 row/column 관련 entry를 통해 refine한다. 이는 matrix powers가 intermediate vertex를 통해 entry 정보를 섞는 방식과 닮아 있다. Sparse variant인 <math><mi>&delta;</mi></math>-MC-MPNN은 nonzero graph entry만 사용해 generic higher-order SDP architecture보다 비용을 줄이려는 설계다. 다만 실제 구현에서는 dense GPU operation이 더 빠를 수 있으므로, sparse complexity가 곧 wall-clock advantage를 보장한다고 읽으면 안 된다.

## Feasibility를 보존하는 방식

Primal head는 vector <math><msub><mi>o</mi><mi>i</mi></msub></math>를 예측하고 normalize한 뒤 다음 matrix를 만든다.

<math display="block" aria-label="Primal feasible construction Korean">
  <mover><mi>X</mi><mo>^</mo></mover>
  <mo>=</mo>
  <mi>O</mi><msup><mi>O</mi><mo>&top;</mo></msup>
  <mo>,</mo>
  <mspace width="0.5em"></mspace>
  <msub><mover><mi>X</mi><mo>^</mo></mover><mrow><mi>i</mi><mi>i</mi></mrow></msub>
  <mo>=</mo><mn>1</mn><mo>.</mo>
</math>

이 construction은 primal SDP feasibility를 보장한다. Low-rank parameterization이므로 primal solution class를 제한할 수는 있다. 하지만 branch-and-bound correctness에는 dual bound가 더 중요하다.

Dual side에서는 먼저 raw vector <math><mover><mi>y</mi><mo>^</mo></mover></math>를 예측한다. 이때 slack matrix

<math display="block" aria-label="Raw dual slack Korean">
  <mover><mi>S</mi><mo>^</mo></mover>
  <mo>=</mo>
  <mi>Diag</mi><mo>(</mo><mover><mi>y</mi><mo>^</mo></mover><mo>)</mo><mo>-</mo><mi>L</mi>
</math>

는 PSD가 아닐 수 있다. 논문은 uniform radial shift로 이를 보정한다.

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

이 correction 이후 slack matrix는 PSD가 된다. 따라서 <math><msup><mi>e</mi><mo>&top;</mo></msup><msub><mover><mi>y</mi><mo>^</mo></mover><mtext>feas</mtext></msub></math>는 valid upper bound다. 이 장치 때문에 learned component를 exact solver 안에 넣을 수 있다.

## Exactness와 speed는 다른 주장이다

Branch-and-bound는 각 node <math><mi>c</mi></math>에 대해 feasible incumbent lower bound <math><mi>LB</mi></math>와 upper bound <math><msub><mi>UB</mi><mi>c</mi></msub></math>를 유지한다. Node가 incumbent를 개선할 수 없으면 prune한다.

Neural bound는 다음과 같다.

<math display="block" aria-label="Neural branch-and-bound upper bound Korean">
  <msub><mi>UB</mi><mi>c</mi></msub>
  <mo>=</mo>
  <msup><mi>e</mi><mo>&top;</mo></msup>
  <msub><mover><mi>y</mi><mo>^</mo></mover><mtext>feas</mtext></msub><mo>.</mo>
</math>

Dual feasible이므로 안전하다. Exact SDP bound보다 약할 수 있고, 그러면 pruning은 줄어든다. 그래도 invalid upper bound를 쓴 것은 아니므로 solver의 exactness는 유지된다. 대신 더 많은 node를 탐색할 수 있다.

따라서 두 주장을 분리해야 한다.

Feasibility projection은 correctness를 지지한다. 빠른 runtime을 증명하지는 않는다.

Speed는 empirical trade-off다. GNN bound가 SDP solve보다 훨씬 싸야 하고, 동시에 branch-and-bound tree가 폭발하지 않을 만큼 tight해야 한다.

## 실험이 보여주는 것

보고된 결과는 tested instance family에서 이 trade-off가 성립할 수 있음을 보여준다. Neural solver는 vanilla SDP-based branch-and-bound보다 더 많은 node를 평가하지만 node당 비용이 낮다. 첨부 노트의 대표 수치는 다음과 같다.

| Instance | Vanilla time | Neural time | Speed-up |
|---|---:|---:|---:|
| g05_60 | 53.1 s | 9.5 s | 5.6x |
| g05_80 | 1170.3 s | 155.7 s | 7.5x |
| g05_100 | 40930.1 s | 4509.3 s | 9.1x |
| pm1s_100 | 10382.5 s | 1058.2 s | 9.8x |
| w01_100 | 11348.6 s | 1073.9 s | 10.6x |

논문은 synthetic graph distribution에서 MC-MPNN과 <math><mi>&delta;</mi></math>-MC-MPNN도 비교한다. 보고된 설정에서는 objective gap이 비슷하다. Sparse variant는 이론적으로 매력적이지만, dense GPU implementation에서는 dense variant가 경쟁적이거나 더 안정적일 수 있다.

## 한계

가장 큰 한계는 이것이 state-of-the-art Max-Cut solver 결과는 아니라는 점이다. Cutting plane을 쓰는 BiqCrunch류 full branch-and-cut solver는 일부 instance에서 여전히 훨씬 강하다. 이 논문은 base SDP relaxation evaluation을 certified neural surrogate로 대체할 수 있음을 보이는 proof of concept에 가깝다.

두 번째 한계는 distribution dependence다. Training instance와 branch-and-bound subgraph는 특정 graph family에서 나온다. Graph size, sparsity, weight distribution이 바뀌면 learned bound가 느슨해질 수 있다. Exactness는 유지될 수 있지만 speed-up은 사라질 수 있다.

세 번째 한계는 radial projection이다. Uniform shift는 싸고 안전하지만 conservative할 수 있다. 특정 diagonal entry만 고쳐도 될 상황에서 모든 <math><mi>y</mi></math> component를 올리면 upper bound가 필요 이상으로 느슨해진다.

마지막으로 <math><msub><mi>&lambda;</mi><mi>min</mi></msub></math> 계산은 공짜가 아니다. 보고된 scale에서는 병목이 아닐 수 있지만, 더 큰 graph에서는 이 correction step과 numerical tolerance가 solver engineering의 일부가 된다.

내 해석은 이렇다. 이 논문은 learning과 exact optimization 사이의 interface를 잘 잡았다는 점에서 가치가 있다. Learned model이 유용한 이유는 cut value를 그럴듯하게 예측해서가 아니라, solver가 사용할 수 있는 certificate-compatible object를 반환하기 때문이다.

## References

Chen, H., Qian, C., Morris, C., Lodi, A., & Li, C. (2026). Solving Max-Cut to Global Optimality via Feasibility-Preserving Graph Neural Networks. arXiv preprint arXiv:2605.07113.
