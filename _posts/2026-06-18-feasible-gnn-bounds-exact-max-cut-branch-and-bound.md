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

That qualification is the point. In branch-and-bound, a learned bound predictor is dangerous if it can be too optimistic. One wrong upper bound can prune the branch containing the optimum. Chen et al. avoid that failure mode by forcing the neural output to satisfy dual feasibility. The learned bound can be loose. It should not be invalid.

## The bottleneck

Max-Cut asks for a bipartition of a weighted graph that maximizes the weight of crossing edges. With binary signs `x_i in {-1, 1}`, a common quadratic form is to maximize `(1/4) x^T L x`, where `L` is the graph Laplacian.

The exact problem is NP-complete, so exact solvers rely on enumeration plus strong bounds. A common bound comes from the Goemans-Williamson SDP relaxation. The relaxation is useful because its dual solution gives a certificate: if the dual slack matrix is positive semidefinite, the dual objective is an upper bound on the best cut value.

The computational problem is repetition. Branch-and-bound needs this kind of upper bound at many nodes. Solving an SDP again and again can dominate runtime. This paper targets that repeated relaxation evaluation, not the branching rule itself.

## The certificate

The Max-Cut SDP introduces a matrix variable `X` with two basic primal conditions:

- `X` must be positive semidefinite.
- `diag(X) = e`.

The dual side can be written with a vector `y` and a slack matrix `S = Diag(y) - L`. If `S` is positive semidefinite, then `e^T y` is a valid upper bound on the SDP optimum, and therefore on the integer Max-Cut value below the current branch-and-bound node.

This is the object the neural network must preserve. A small prediction error is not the main issue. A violation of the certificate is.

## Why the GNN is pairwise

A node-level GNN is not a natural fit for this SDP. The main decision object is not a vertex label but a matrix entry `X_ij`. The paper therefore uses pairwise tokens `h_ij`.

The diagonal indicator is part of the input, because the SDP constraints are exactly diagonal constraints. This is a Max-Cut-specific design choice, not just a generic graph representation trick.

The message passing update refines each pair using information from related row and column entries. This resembles the way matrix powers mix entries through intermediate vertices. The sparse variant, delta-MC-MPNN, restricts aggregation to nonzero graph entries and is meant to reduce the cost relative to generic higher-order SDP architectures.

There is an important caveat. The paper notes that dense GPU operations can still be faster in practice. So the sparse complexity story should not be read as a guaranteed wall-clock advantage.

## How feasibility is preserved

The primal head predicts vectors `o_i`, normalizes them, and constructs `X_hat = O O^T`. Because each `o_i` is normalized, `diag(X_hat) = e`. Because `X_hat` is a Gram matrix, it is positive semidefinite. This gives primal SDP feasibility by construction.

The dual side is more important for exactness. The network first predicts a raw vector `y_hat`. The associated slack matrix `S_hat = Diag(y_hat) - L` may not be positive semidefinite. The paper fixes this with a uniform radial shift:

`y_feas = y_hat + max(0, -lambda_min(S_hat)) e`.

After this correction, the corrected slack matrix is positive semidefinite. Therefore `e^T y_feas` is a valid upper bound. This is the main reason the learned component can be placed inside an exact solver.

## Exactness and speed are different claims

For each branch-and-bound node `c`, the solver keeps a feasible incumbent lower bound `LB` and an upper bound `UB_c`. If a node cannot improve the incumbent, it can be pruned.

With the neural surrogate, the upper bound is `UB_c = e^T y_feas`. Because this value is dual feasible, it is safe. It may be weaker than the exact SDP bound, so it may prune fewer nodes. The solver remains exact because it has not used an invalid upper bound.

This distinction should stay sharp:

Feasibility projection supports correctness. It does not prove fast runtime.

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

The paper also compares MC-MPNN and delta-MC-MPNN on synthetic graph distributions. Their objective gaps are close in the reported settings. The sparse variant is theoretically appealing, but the dense variant can be competitive or better under dense GPU implementation.

## Limits

The strongest limitation is that this is not a state-of-the-art Max-Cut solver result. Full branch-and-cut solvers with cutting planes, such as BiqCrunch-style methods, remain much stronger on some instances. The paper is better read as a proof of concept for replacing a base SDP relaxation evaluation with a certified neural surrogate.

The second limitation is distribution dependence. Training instances and branch-and-bound subgraphs come from particular graph families. If graph size, sparsity, or weight distribution changes, the learned bound may become loose. Exactness would remain, but the speed-up could disappear.

The third limitation is the radial projection itself. A uniform shift is cheap and safe, but it can be conservative. It may increase every component of `y` even when a more selective diagonal correction would suffice. That makes the upper bound looser.

Finally, the method still needs an eigenvalue computation for `lambda_min(S_hat)`. At the reported scale this may not dominate, but it is not free. For larger graphs, this correction step and its numerical tolerance would become part of the solver engineering problem.

My reading is therefore: this paper is valuable because it identifies the right interface between learning and exact optimization. The learned model is useful only because it returns a certificate-compatible object. That is more disciplined than learning a cut value and hoping the solver remains safe.

## References

Chen, H., Qian, C., Morris, C., Lodi, A., & Li, C. (2026). Solving Max-Cut to Global Optimality via Feasibility-Preserving Graph Neural Networks. arXiv preprint arXiv:2605.07113.

<!-- ko -->

이 논문은 GNN이 Max-Cut 최적해를 직접 찾아낸다고 주장하는 논문이 아니다. 핵심은 더 좁다. Exact branch-and-bound solver 안에서 반복적으로 풀리는 SDP relaxation을 learned surrogate로 대체하되, 그 surrogate가 valid upper bound를 반환하도록 만드는 것이다.

이 조건이 중요하다. Branch-and-bound에서 learned bound predictor가 잘못 낙관적인 값을 내면 optimum이 들어 있는 branch를 지울 수 있다. Chen et al.은 neural output을 dual feasible하게 보정해서 이 failure mode를 피한다. Bound가 느슨할 수는 있다. 하지만 invalid하면 안 된다.

## 병목

Max-Cut은 weighted graph의 vertex를 두 partition으로 나누고, partition 사이를 가로지르는 edge weight 합을 최대화하는 문제다. Binary sign `x_i in {-1, 1}`을 쓰면 흔히 `(1/4) x^T L x`를 최대화하는 quadratic form으로 쓴다. 여기서 `L`은 graph Laplacian이다.

Exact Max-Cut은 NP-complete이므로 강한 bound와 enumeration을 결합해야 한다. Goemans-Williamson SDP relaxation은 여기서 중요한 bound를 제공한다. 특히 dual solution이 positive semidefinite slack을 가지면 dual objective가 valid upper bound가 된다.

문제는 이 upper bound를 branch-and-bound의 많은 node에서 반복적으로 계산해야 한다는 점이다. SDP를 반복해서 푸는 비용이 전체 runtime을 지배할 수 있다. 이 논문은 branching rule이 아니라 relaxation evaluation 자체를 겨냥한다.

## 필요한 certificate

Max-Cut SDP는 matrix variable `X`에 대해 두 가지 기본 primal condition을 둔다.

- `X`는 positive semidefinite이어야 한다.
- `diag(X) = e`이어야 한다.

Dual side는 vector `y`와 slack matrix `S = Diag(y) - L`로 볼 수 있다. 만약 `S`가 positive semidefinite이면 `e^T y`는 SDP optimum에 대한 valid upper bound이고, 따라서 현재 branch-and-bound node 아래의 integer Max-Cut value에 대한 upper bound가 된다.

Neural network가 보존해야 하는 것은 바로 이 certificate다. 작은 prediction error보다 certificate violation이 더 위험하다.

## 왜 pairwise GNN인가

일반 node-level GNN은 이 SDP에 잘 맞지 않는다. 중요한 decision object는 vertex label이 아니라 matrix entry `X_ij`다. 그래서 논문은 pairwise token `h_ij`를 사용한다.

Diagonal indicator도 input에 포함된다. Max-Cut SDP의 constraints가 diagonal constraints이기 때문이다. 이는 generic graph predictor가 아니라 Max-Cut SDP 구조에 맞춘 설계다.

Message passing은 각 pair를 row/column 관련 entry를 통해 refine한다. 이는 matrix powers가 intermediate vertex를 통해 entry 정보를 섞는 방식과 닮아 있다. Sparse variant인 delta-MC-MPNN은 nonzero graph entry만 사용해 generic higher-order SDP architecture보다 비용을 줄이려는 설계다.

다만 중요한 caveat가 있다. 논문은 실제 구현에서 dense GPU operation이 더 빠를 수 있다고 말한다. 따라서 sparse complexity가 곧 wall-clock advantage를 보장한다고 읽으면 안 된다.

## Feasibility를 보존하는 방식

Primal head는 vector `o_i`를 예측하고 normalize한 뒤 `X_hat = O O^T`를 만든다. 각 `o_i`가 normalized되어 있으므로 `diag(X_hat) = e`가 된다. 또 `X_hat`은 Gram matrix이므로 positive semidefinite이다. 따라서 primal SDP feasibility가 construction으로 보장된다.

Exactness에는 dual side가 더 중요하다. Network는 먼저 raw vector `y_hat`을 예측한다. 이때 slack matrix `S_hat = Diag(y_hat) - L`은 positive semidefinite가 아닐 수 있다. 논문은 uniform radial shift로 이를 보정한다.

`y_feas = y_hat + max(0, -lambda_min(S_hat)) e`.

이 correction 이후 corrected slack matrix는 positive semidefinite가 된다. 따라서 `e^T y_feas`는 valid upper bound다. 이 장치 때문에 learned component를 exact solver 안에 넣을 수 있다.

## Exactness와 speed는 다른 주장이다

Branch-and-bound는 각 node `c`에 대해 feasible incumbent lower bound `LB`와 upper bound `UB_c`를 유지한다. Node가 incumbent를 개선할 수 없으면 prune한다.

Neural surrogate를 쓰면 upper bound는 `UB_c = e^T y_feas`가 된다. Dual feasible이므로 안전하다. Exact SDP bound보다 약할 수 있고, 그러면 pruning은 줄어든다. 그래도 invalid upper bound를 쓴 것은 아니므로 solver의 exactness는 유지된다.

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

논문은 synthetic graph distribution에서 MC-MPNN과 delta-MC-MPNN도 비교한다. 보고된 설정에서는 objective gap이 비슷하다. Sparse variant는 이론적으로 매력적이지만, dense GPU implementation에서는 dense variant가 경쟁적이거나 더 안정적일 수 있다.

## 한계

가장 큰 한계는 이것이 state-of-the-art Max-Cut solver 결과는 아니라는 점이다. Cutting plane을 쓰는 BiqCrunch류 full branch-and-cut solver는 일부 instance에서 여전히 훨씬 강하다. 이 논문은 base SDP relaxation evaluation을 certified neural surrogate로 대체할 수 있음을 보이는 proof of concept에 가깝다.

두 번째 한계는 distribution dependence다. Training instance와 branch-and-bound subgraph는 특정 graph family에서 나온다. Graph size, sparsity, weight distribution이 바뀌면 learned bound가 느슨해질 수 있다. Exactness는 유지될 수 있지만 speed-up은 사라질 수 있다.

세 번째 한계는 radial projection이다. Uniform shift는 싸고 안전하지만 conservative할 수 있다. 특정 diagonal entry만 고쳐도 될 상황에서 모든 `y` component를 올리면 upper bound가 필요 이상으로 느슨해진다.

마지막으로 `lambda_min(S_hat)` 계산은 공짜가 아니다. 보고된 scale에서는 병목이 아닐 수 있지만, 더 큰 graph에서는 이 correction step과 numerical tolerance가 solver engineering의 일부가 된다.

내 해석은 이렇다. 이 논문은 learning과 exact optimization 사이의 interface를 잘 잡았다는 점에서 가치가 있다. Learned model이 유용한 이유는 cut value를 그럴듯하게 예측해서가 아니라, solver가 사용할 수 있는 certificate-compatible object를 반환하기 때문이다.

## References

Chen, H., Qian, C., Morris, C., Lodi, A., & Li, C. (2026). Solving Max-Cut to Global Optimality via Feasibility-Preserving Graph Neural Networks. arXiv preprint arXiv:2605.07113.
