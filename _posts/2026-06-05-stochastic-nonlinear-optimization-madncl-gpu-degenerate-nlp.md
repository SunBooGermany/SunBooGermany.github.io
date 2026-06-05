---
layout: post
title: "MadNCL: GPU-Friendly NCL for Degenerate Nonlinear Programs"
title_ko: "MadNCL: 퇴화된 비선형계획을 위한 GPU 친화적 NCL"
date: 2026-06-05
category: stochastic-nonlinear-optimization
category_label: "Stochastic & Nonlinear Optimization"
research_group: algorithmic_reviews
research_category: stochastic-nonlinear-optimization
research_category_label: "Stochastic & Nonlinear Optimization"
application_category: ""
application_category_label: ""
method_category: "stochastic-nonlinear-optimization"
method_category_label: "Stochastic & Nonlinear Optimization"
paper_title: "MADNCL: a GPU implementation of algorithm NCL for large-scale, degenerate nonlinear programs"
authors: "Montoison, A.; Pacaud, F.; Saunders, M.; Shin, S.; Orban, D."
venue: "arXiv preprint"
year: "2025"
doi: ""
arxiv: "2510.05885"
source_url: "https://arxiv.org/abs/2510.05885"
tags:
  - "nonlinear programming"
  - "augmented Lagrangian"
  - "Algorithm NCL"
  - "GPU optimization"
  - "KKT systems"
  - "degeneracy"
excerpt: "A critical note on MadNCL, which combines Algorithm NCL, MadNLP, and GPU-friendly KKT reformulations to improve robustness on large-scale degenerate nonlinear programs."
excerpt_ko: "Algorithm NCL, MadNLP, GPU 친화적 KKT 재구성을 결합해 대규모 퇴화 비선형계획에서 강건성을 높이려는 MadNCL 논문에 대한 비판적 정리."
language: "en-ko"
has_korean_note: false
---

## Problem: GPU speed is not enough when the NLP is degenerate

The paper studies large-scale nonlinear programs of the form

<math display="block" aria-label="Bound constrained nonlinear program">
  <munder><mi>min</mi><mrow><mi>x</mi><mo>&isin;</mo><msup><mi>R</mi><mi>n</mi></msup></mrow></munder>
  <mspace width="0.4em"></mspace>
  <mi>&phi;</mi><mo>(</mo><mi>x</mi><mo>)</mo>
  <mspace width="1em"></mspace>
  <mtext>subject to</mtext>
  <mspace width="0.4em"></mspace>
  <mi>c</mi><mo>(</mo><mi>x</mi><mo>)</mo><mo>=</mo><mn>0</mn><mo>,</mo>
  <mspace width="0.4em"></mspace>
  <mi>&ell;</mi><mo>&le;</mo><mi>x</mi><mo>&le;</mo><mi>u</mi><mo>.</mo>
</math>

The central difficulty is not only scale. It is constraint degeneracy: cases where standard constraint qualifications such as LICQ or MFCQ fail. In these instances, an interior-point method or SQP method can run into singular KKT systems, restoration failure, or excessive regularization. The paper is motivated by large OPF instances, COPS benchmarks, and SCOPF-MPCC problems where complementarity constraints make degeneracy structural rather than accidental.

This matters because GPU acceleration does not automatically solve the numerical problem. GPUs are excellent for massive parallel linear algebra, but sparse indefinite factorization often depends on dynamic numerical pivoting, and dynamic pivoting does not fit GPU execution cleanly. Many GPU-oriented IPM formulations therefore change the KKT system into lifted or condensed forms. That can improve throughput, but it can also worsen conditioning. The question MadNCL asks is narrower and more practical: can an older augmented-Lagrangian idea be reformulated so that it is both robust to degeneracy and compatible with GPU sparse direct solvers?

MadNCL tries to retain GPU-level speed while recovering robustness in degenerate NLPs where conventional IPM formulations can fail.

## From ALM to NCL

The method sits in the augmented Lagrangian family. A classical bound-constrained augmented Lagrangian subproblem can be written as

<math display="block" aria-label="Classical bound constrained augmented Lagrangian">
  <munder><mi>min</mi><mrow><mi>&ell;</mi><mo>&le;</mo><mi>x</mi><mo>&le;</mo><mi>u</mi></mrow></munder>
  <mspace width="0.4em"></mspace>
  <mi>&phi;</mi><mo>(</mo><mi>x</mi><mo>)</mo>
  <mo>-</mo>
  <msubsup><mi>y</mi><mi>k</mi><mi>T</mi></msubsup>
  <mi>c</mi><mo>(</mo><mi>x</mi><mo>)</mo>
  <mo>+</mo>
  <mfrac><msub><mi>&rho;</mi><mi>k</mi></msub><mn>2</mn></mfrac>
  <msup><mrow><mo>&Vert;</mo><mi>c</mi><mo>(</mo><mi>x</mi><mo>)</mo><mo>&Vert;</mo></mrow><mn>2</mn></msup>
  <mo>.</mo>
</math>

Algorithm NCL rewrites this subproblem by adding a free variable <math><mi>r</mi></math>:

<math display="block" aria-label="NCL formulation">
  <munder><mi>min</mi><mrow><mi>x</mi><mo>,</mo><mi>r</mi></mrow></munder>
  <mspace width="0.4em"></mspace>
  <mi>&phi;</mi><mo>(</mo><mi>x</mi><mo>)</mo>
  <mo>+</mo>
  <msubsup><mi>y</mi><mi>k</mi><mi>T</mi></msubsup><mi>r</mi>
  <mo>+</mo>
  <mfrac><msub><mi>&rho;</mi><mi>k</mi></msub><mn>2</mn></mfrac>
  <msup><mrow><mo>&Vert;</mo><mi>r</mi><mo>&Vert;</mo></mrow><mn>2</mn></msup>
  <mspace width="1em"></mspace>
  <mtext>subject to</mtext>
  <mspace width="0.4em"></mspace>
  <mi>c</mi><mo>(</mo><mi>x</mi><mo>)</mo><mo>+</mo><mi>r</mi><mo>=</mo><mn>0</mn><mo>,</mo>
  <mspace width="0.4em"></mspace>
  <mi>&ell;</mi><mo>&le;</mo><mi>x</mi><mo>&le;</mo><mi>u</mi><mo>.</mo>
</math>

Mathematically, the two subproblems are equivalent after substituting <math><mi>r</mi><mo>=</mo><mo>-</mo><mi>c</mi><mo>(</mo><mi>x</mi><mo>)</mo></math>. Numerically, they are very different. The NCL constraint Jacobian is

<math display="block" aria-label="NCL constraint Jacobian">
  <mo>[</mo><mi>J</mi><mo>(</mo><mi>x</mi><mo>)</mo><mspace width="0.5em"></mspace><mi>I</mi><mo>]</mo><mo>.</mo>
</math>

Even if <math><mi>J</mi><mo>(</mo><mi>x</mi><mo>)</mo></math> is rank deficient, this augmented Jacobian has full row rank. If <math><msup><mi>&lambda;</mi><mi>T</mi></msup><mo>[</mo><mi>J</mi><mspace width="0.3em"></mspace><mi>I</mi><mo>]</mo><mo>=</mo><mn>0</mn></math>, then the identity block implies <math><mi>&lambda;</mi><mo>=</mo><mn>0</mn></math>. This is the cleanest reason NCL can handle LICQ failure more gracefully than a direct IPM formulation.

The variable <math><mi>r</mi></math> is not a free permission to violate constraints. It temporarily absorbs infeasibility, but the term <math><msubsup><mi>y</mi><mi>k</mi><mi>T</mi></msubsup><mi>r</mi><mo>+</mo><msub><mi>&rho;</mi><mi>k</mi></msub><msup><mrow><mo>&Vert;</mo><mi>r</mi><mo>&Vert;</mo></mrow><mn>2</mn></msup><mo>/</mo><mn>2</mn></math> penalizes it. As the penalty is increased, the method pushes <math><mi>r</mi></math> back toward zero. In this sense, NCL separates two tasks that are entangled in a direct KKT system: keep the subproblem regular enough to solve, and then use the augmented-Lagrangian mechanism to recover feasibility.

## Solver architecture

MadNCL is best understood as a solver architecture rather than a new optimization principle:

```text
NLP model
  -> ExaModels derivative evaluation on GPU
  -> MadNCL augmented-Lagrangian outer layer
  -> MadNLP interior-point subproblem solve
  -> K2r or K1s KKT reformulation
  -> NVIDIA cuDSS sparse factorization
```

The key implementation point is that MadNCL does not treat MadNLP as a black-box inner solver. It uses the KKT structure induced by the NCL subproblem and exposes formulations that are more suitable for GPU sparse factorization. That is where most of the paper's engineering value lies.

The outer-loop update can be read in the classical augmented-Lagrangian form:

<math display="block" aria-label="Multiplier update">
  <msub><mi>y</mi><mrow><mi>k</mi><mo>+</mo><mn>1</mn></mrow></msub>
  <mo>=</mo>
  <msub><mi>y</mi><mi>k</mi></msub>
  <mo>-</mo>
  <msub><mi>&rho;</mi><mi>k</mi></msub>
  <mi>c</mi><mo>(</mo><msub><mi>x</mi><mrow><mi>k</mi><mo>+</mo><mn>1</mn></mrow></msub><mo>)</mo>
  <mo>.</mo>
</math>

In NCL variables, because <math><msub><mi>r</mi><mrow><mi>k</mi><mo>+</mo><mn>1</mn></mrow></msub><mo>=</mo><mo>-</mo><mi>c</mi><mo>(</mo><msub><mi>x</mi><mrow><mi>k</mi><mo>+</mo><mn>1</mn></mrow></msub><mo>)</mo></math>, the same update becomes <math><msub><mi>y</mi><mrow><mi>k</mi><mo>+</mo><mn>1</mn></mrow></msub><mo>=</mo><msub><mi>y</mi><mi>k</mi></msub><mo>+</mo><msub><mi>&rho;</mi><mi>k</mi></msub><msub><mi>r</mi><mrow><mi>k</mi><mo>+</mo><mn>1</mn></mrow></msub></math>. If infeasibility is sufficiently reduced, the multiplier is updated. Otherwise, the penalty is increased and the next subproblem presses harder on feasibility.

## KKT reformulations: K2, K2r, and K1s

The original NCL Newton system contains the primal variables, the free variables <math><mi>r</mi></math>, and the constraint multipliers. In simplified block form, the augmented KKT matrix is

<math display="block" aria-label="Augmented KKT matrix K2">
  <msub><mi>K</mi><mn>2</mn></msub>
  <mo>=</mo>
  <mfenced open="[" close="]">
    <mtable>
      <mtr><mtd><mover><mi>H</mi><mo>^</mo></mover><mo>+</mo><msub><mi>&delta;</mi><mi>k</mi></msub><mi>I</mi></mtd><mtd><mn>0</mn></mtd><mtd><mi>J</mi></mtd></mtr>
      <mtr><mtd><mn>0</mn></mtd><mtd><msub><mover><mi>&rho;</mi><mo>^</mo></mover><mi>k</mi></msub><mi>I</mi></mtd><mtd><mi>I</mi></mtd></mtr>
      <mtr><mtd><msup><mi>J</mi><mi>T</mi></msup></mtd><mtd><mi>I</mi></mtd><mtd><mn>0</mn></mtd></mtr>
    </mtable>
  </mfenced>
  <mo>.</mo>
</math>

The regularization parameter <math><msub><mi>&delta;</mi><mi>k</mi></msub></math> is used to obtain the correct inertia for an IPM descent direction. The paper then derives two GPU-oriented reductions.

First, eliminating the <math><mi>r</mi></math> direction gives the stabilized KKT system

<math display="block" aria-label="Stabilized KKT system K2r">
  <msub><mi>K</mi><mrow><mn>2</mn><mi>r</mi></mrow></msub>
  <mo>=</mo>
  <mfenced open="[" close="]">
    <mtable>
      <mtr><mtd><mover><mi>H</mi><mo>^</mo></mover><mo>+</mo><msub><mi>&delta;</mi><mi>k</mi></msub><mi>I</mi></mtd><mtd><mi>J</mi></mtd></mtr>
      <mtr><mtd><msup><mi>J</mi><mi>T</mi></msup></mtd><mtd><mo>-</mo><msub><mi>&theta;</mi><mi>k</mi></msub><mi>I</mi></mtd></mtr>
    </mtable>
  </mfenced>
  <mo>,</mo>
  <mspace width="0.6em"></mspace>
  <msub><mi>&theta;</mi><mi>k</mi></msub>
  <mo>=</mo>
  <msup><msub><mover><mi>&rho;</mi><mo>^</mo></mover><mi>k</mi></msub><mrow><mo>-</mo><mn>1</mn></mrow></msup>
  <mo>.</mo>
</math>

The important feature is the negative definite lower-right block. It leaves a stabilizing trace of the eliminated <math><mi>r</mi></math> variable and produces a structure that is friendlier to static LDL factorization.

Second, further condensation leads to K1s, whose core has the flavor

<math display="block" aria-label="Condensed K1s matrix intuition">
  <mover><mi>H</mi><mo>^</mo></mover>
  <mo>+</mo>
  <msub><mi>&delta;</mi><mi>k</mi></msub><mi>I</mi>
  <mo>+</mo>
  <mover><mi>&rho;</mi><mo>^</mo></mover>
  <msup><mi>J</mi><mi>T</mi></msup><mi>J</mi>
  <mo>.</mo>
</math>

K1s is smaller and can be attractive for Cholesky-like GPU solvers. But the same condensation that makes it compact can also amplify ill-conditioning. The empirical story in the paper is therefore not that K1s is uniformly superior. K2r is the more robust default; K1s is a problem-dependent fast option.

One theoretical contribution is the inertia equivalence:

<math display="block" aria-label="Inertia equivalence">
  <mi>In</mi><mo>(</mo><msub><mi>K</mi><mn>2</mn></msub><mo>)</mo>
  <mo>=</mo><mo>(</mo><mi>n</mi><mo>+</mo><mi>m</mi><mo>,</mo><mi>m</mi><mo>,</mo><mn>0</mn><mo>)</mo>
  <mo>&iff;</mo>
  <mi>In</mi><mo>(</mo><msub><mi>K</mi><mrow><mn>2</mn><mi>r</mi></mrow></msub><mo>)</mo>
  <mo>=</mo><mo>(</mo><mi>n</mi><mo>,</mo><mi>m</mi><mo>,</mo><mn>0</mn><mo>)</mo>
  <mo>&iff;</mo>
  <mi>In</mi><mo>(</mo><msub><mi>K</mi><mrow><mn>1</mn><mi>s</mi></mrow></msub><mo>)</mo>
  <mo>=</mo><mo>(</mo><mi>n</mi><mo>,</mo><mn>0</mn><mo>,</mo><mn>0</mn><mo>)</mo>.
</math>

This matters because the GPU-friendly systems are not arbitrary numerical hacks. Under the stated conditions, they preserve the descent-direction validity of the original NCL/IPM system.

## What is actually guaranteed?

The strongest guarantee is structural: the NCL formulation repairs constraint-Jacobian rank deficiency by replacing <math><mi>J</mi></math> with <math><mo>[</mo><mi>J</mi><mspace width="0.3em"></mspace><mi>I</mi><mo>]</mo></math>. This does not prove global convergence to a global optimum, and it is not a guarantee for every degeneracy mechanism. It specifically addresses a first-order constraint degeneracy mechanism.

The paper also connects the KKT reductions to inertia conditions, so solving K2r or K1s can be justified in relation to the original augmented system. That is stronger than saying "condensation seems to work." It explains why the reformulated linear systems can still produce valid IPM directions when the assumptions are met.

The extrapolation step is a local acceleration device. Once the inner and outer iterations are close enough, a Newton-style extrapolation step can allow the method to skip an inner solve and still move toward the next outer iterate. The relevant point is local superlinear behavior near the solution, not a claim that every instance becomes fast from the start.

## Experimental reading

The experiments should be read by regime.

On CUTEst CPU benchmarks, MadNCL is not always faster than Ipopt or MadNLP. Its value is that it solves some instances where IPM methods fail because of insufficient degrees of freedom, restoration failure, or excessive primal-dual regularization. This supports the robustness story rather than a speed-dominance story.

On GPU OPF and COPS benchmarks, the picture is mixed but informative. In a large OPF case with hundreds of thousands of variables and over a million constraints, MadNCL-K2r with cuDSS reports a large speed-up over a CPU MA27-based MadNCL variant. At the same time, K1s can fail on that OPF instance because condensation worsens conditioning. In COPS-type problems, K1s can be stable and fast. The practical conclusion is that KKT form selection is problem dependent.

The SCOPF-MPCC results are the closest match to the paper's main argument. MPCC formulations violate MFCQ at every feasible point, so degeneracy is unavoidable. The paper reports that Ipopt and MadNLP can end in restoration failure or infeasible solutions, while MadNCL-K2r solves the tested instances to the reported tolerance on both CPU and GPU. This is the clearest evidence that NCL regularization plus a stabilized KKT system can matter in genuinely degenerate large-scale models.

## Limitations

First, MadNCL is not a universal speed improvement over GPU-IPM. On regular OPF instances, other GPU IPM formulations can be faster. The distinctive strength is robustness under degeneracy while retaining useful GPU throughput.

Second, NCL does not solve every degeneracy. The mechanism is strongest for constraint-Jacobian degeneracy and LICQ failure. If the reduced Hessian is nearly singular or the problem has deeper second-order degeneracy, the augmented-Lagrangian story may not provide the same protection.

Finally, some of the most degenerate MPCC experiments use a looser tolerance than the standard NLP benchmarks. That may be practically reasonable, but it means the evidence is about robust progress to a useful tolerance, not necessarily high-precision resolution of every degenerate case.

## Assessment

This paper is best understood as an implementation-theory hybrid. It does not discover a new optimization principle from scratch. Instead, it shows that the old robustness advantages of ALM/NCL become newly relevant when second-order NLP solvers are moved onto GPUs.

The core chain is:

```text
degenerate NLP
  -> NCL regularization
  -> better structured KKT systems
  -> GPU-compatible sparse factorization
  -> robust large-scale solver behavior
```

A formulation-level regularization can be carried all the way down to GPU-friendly KKT linear algebra, and this combination is useful on large-scale degenerate NLPs such as SCOPF-MPCC.

## References

Montoison, A., Pacaud, F., Saunders, M., Shin, S., & Orban, D. (2025). MADNCL: a GPU implementation of algorithm NCL for large-scale, degenerate nonlinear programs. arXiv preprint arXiv:2510.05885.

<!-- ko -->

## 문제: GPU 속도만으로는 퇴화된 NLP를 해결할 수 없다

이 논문이 다루는 문제는 다음 형태의 대규모 비선형계획이다.

<math display="block" aria-label="Bound constrained nonlinear program">
  <munder><mi>min</mi><mrow><mi>x</mi><mo>&isin;</mo><msup><mi>R</mi><mi>n</mi></msup></mrow></munder>
  <mspace width="0.4em"></mspace>
  <mi>&phi;</mi><mo>(</mo><mi>x</mi><mo>)</mo>
  <mspace width="1em"></mspace>
  <mtext>subject to</mtext>
  <mspace width="0.4em"></mspace>
  <mi>c</mi><mo>(</mo><mi>x</mi><mo>)</mo><mo>=</mo><mn>0</mn><mo>,</mo>
  <mspace width="0.4em"></mspace>
  <mi>&ell;</mi><mo>&le;</mo><mi>x</mi><mo>&le;</mo><mi>u</mi><mo>.</mo>
</math>

핵심 난점은 단순히 규모가 크다는 것이 아니다. 문제는 constraint degeneracy, 즉 LICQ나 MFCQ 같은 표준 constraint qualification이 깨지는 경우다. 이런 경우 interior-point method나 SQP는 singular KKT system, restoration failure, excessive regularization에 부딪힐 수 있다. 논문은 특히 large-scale OPF, COPS benchmark, SCOPF-MPCC처럼 complementarity constraint 때문에 퇴화가 우연이 아니라 구조적으로 생기는 문제를 염두에 둔다.

이 지점이 중요한 이유는 GPU acceleration이 수치적 안정성을 자동으로 해결하지 않기 때문이다. GPU는 대규모 병렬 선형대수에는 강하지만, sparse indefinite factorization은 흔히 dynamic numerical pivoting에 의존한다. 그런데 dynamic pivoting은 GPU 병렬 구조와 잘 맞지 않는다. 그래서 많은 GPU 기반 IPM은 KKT system을 lifted form이나 condensed form으로 바꾸는데, 이 과정은 처리량을 높이는 대신 conditioning을 악화시킬 수 있다. MadNCL이 던지는 질문은 더 구체적이다. 오래된 augmented Lagrangian/NCL 아이디어를 GPU sparse direct solver와 잘 맞는 형태로 바꾸면, 퇴화된 NLP에서도 강건성을 유지할 수 있는가?

MadNCL은 기존 IPM formulation이 실패할 수 있는 degenerate NLP에서 robustness를 회복하면서도 GPU 수준의 속도를 어느 정도 유지하려는 solver design이다.

## ALM에서 NCL로

이 방법은 augmented Lagrangian 계열에 있다. 고전적인 bound-constrained augmented Lagrangian subproblem은 다음처럼 쓸 수 있다.

<math display="block" aria-label="Classical bound constrained augmented Lagrangian">
  <munder><mi>min</mi><mrow><mi>&ell;</mi><mo>&le;</mo><mi>x</mi><mo>&le;</mo><mi>u</mi></mrow></munder>
  <mspace width="0.4em"></mspace>
  <mi>&phi;</mi><mo>(</mo><mi>x</mi><mo>)</mo>
  <mo>-</mo>
  <msubsup><mi>y</mi><mi>k</mi><mi>T</mi></msubsup>
  <mi>c</mi><mo>(</mo><mi>x</mi><mo>)</mo>
  <mo>+</mo>
  <mfrac><msub><mi>&rho;</mi><mi>k</mi></msub><mn>2</mn></mfrac>
  <msup><mrow><mo>&Vert;</mo><mi>c</mi><mo>(</mo><mi>x</mi><mo>)</mo><mo>&Vert;</mo></mrow><mn>2</mn></msup>
  <mo>.</mo>
</math>

Algorithm NCL은 여기에 free variable <math><mi>r</mi></math>을 추가해 subproblem을 다시 쓴다.

<math display="block" aria-label="NCL formulation">
  <munder><mi>min</mi><mrow><mi>x</mi><mo>,</mo><mi>r</mi></mrow></munder>
  <mspace width="0.4em"></mspace>
  <mi>&phi;</mi><mo>(</mo><mi>x</mi><mo>)</mo>
  <mo>+</mo>
  <msubsup><mi>y</mi><mi>k</mi><mi>T</mi></msubsup><mi>r</mi>
  <mo>+</mo>
  <mfrac><msub><mi>&rho;</mi><mi>k</mi></msub><mn>2</mn></mfrac>
  <msup><mrow><mo>&Vert;</mo><mi>r</mi><mo>&Vert;</mo></mrow><mn>2</mn></msup>
  <mspace width="1em"></mspace>
  <mtext>subject to</mtext>
  <mspace width="0.4em"></mspace>
  <mi>c</mi><mo>(</mo><mi>x</mi><mo>)</mo><mo>+</mo><mi>r</mi><mo>=</mo><mn>0</mn><mo>,</mo>
  <mspace width="0.4em"></mspace>
  <mi>&ell;</mi><mo>&le;</mo><mi>x</mi><mo>&le;</mo><mi>u</mi><mo>.</mo>
</math>

수학적으로는 <math><mi>r</mi><mo>=</mo><mo>-</mo><mi>c</mi><mo>(</mo><mi>x</mi><mo>)</mo></math>를 대입하면 두 subproblem이 같다. 하지만 numerical structure는 다르다. NCL의 constraint Jacobian은

<math display="block" aria-label="NCL constraint Jacobian">
  <mo>[</mo><mi>J</mi><mo>(</mo><mi>x</mi><mo>)</mo><mspace width="0.5em"></mspace><mi>I</mi><mo>]</mo><mo>.</mo>
</math>

원래 <math><mi>J</mi><mo>(</mo><mi>x</mi><mo>)</mo></math>가 rank deficient여도 이 augmented Jacobian은 full row rank다. 만약 <math><msup><mi>&lambda;</mi><mi>T</mi></msup><mo>[</mo><mi>J</mi><mspace width="0.3em"></mspace><mi>I</mi><mo>]</mo><mo>=</mo><mn>0</mn></math>이면 identity block 때문에 <math><mi>&lambda;</mi><mo>=</mo><mn>0</mn></math>이어야 한다. 이 한 줄이 NCL이 LICQ failure를 직접 IPM formulation보다 더 안정적으로 다룰 수 있는 가장 깔끔한 이유다.

물론 <math><mi>r</mi></math>은 constraint violation을 마음대로 허용하는 변수가 아니다. <math><mi>r</mi></math>은 infeasibility를 임시로 흡수하지만, objective의 <math><msubsup><mi>y</mi><mi>k</mi><mi>T</mi></msubsup><mi>r</mi><mo>+</mo><msub><mi>&rho;</mi><mi>k</mi></msub><msup><mrow><mo>&Vert;</mo><mi>r</mi><mo>&Vert;</mo></mrow><mn>2</mn></msup><mo>/</mo><mn>2</mn></math> 항이 이를 강하게 penalize한다. penalty가 커질수록 method는 <math><mi>r</mi></math>을 0으로 밀어 넣는다. 즉 NCL은 직접 KKT system 안에서 뒤엉켜 있던 두 일을 분리한다. 먼저 subproblem을 풀 수 있을 만큼 regular하게 만들고, 그다음 augmented-Lagrangian mechanism으로 feasibility를 회복한다.

## Solver architecture

MadNCL은 새로운 최적화 원리라기보다 solver architecture로 읽는 것이 좋다.

```text
NLP model
  -> ExaModels derivative evaluation on GPU
  -> MadNCL augmented-Lagrangian outer layer
  -> MadNLP interior-point subproblem solve
  -> K2r or K1s KKT reformulation
  -> NVIDIA cuDSS sparse factorization
```

중요한 구현 포인트는 MadNCL이 MadNLP를 black-box inner solver처럼만 쓰지 않는다는 점이다. NCL subproblem에서 생기는 KKT structure를 이용해 GPU sparse factorization에 더 적합한 formulation을 노출한다. 논문의 engineering value는 대부분 이 지점에서 나온다.

Outer-loop update는 고전적인 augmented-Lagrangian multiplier update로 읽을 수 있다.

<math display="block" aria-label="Multiplier update">
  <msub><mi>y</mi><mrow><mi>k</mi><mo>+</mo><mn>1</mn></mrow></msub>
  <mo>=</mo>
  <msub><mi>y</mi><mi>k</mi></msub>
  <mo>-</mo>
  <msub><mi>&rho;</mi><mi>k</mi></msub>
  <mi>c</mi><mo>(</mo><msub><mi>x</mi><mrow><mi>k</mi><mo>+</mo><mn>1</mn></mrow></msub><mo>)</mo>
  <mo>.</mo>
</math>

NCL 변수로 보면 <math><msub><mi>r</mi><mrow><mi>k</mi><mo>+</mo><mn>1</mn></mrow></msub><mo>=</mo><mo>-</mo><mi>c</mi><mo>(</mo><msub><mi>x</mi><mrow><mi>k</mi><mo>+</mo><mn>1</mn></mrow></msub><mo>)</mo></math>이므로 같은 식은 <math><msub><mi>y</mi><mrow><mi>k</mi><mo>+</mo><mn>1</mn></mrow></msub><mo>=</mo><msub><mi>y</mi><mi>k</mi></msub><mo>+</mo><msub><mi>&rho;</mi><mi>k</mi></msub><msub><mi>r</mi><mrow><mi>k</mi><mo>+</mo><mn>1</mn></mrow></msub></math>가 된다. Infeasibility가 충분히 줄면 multiplier를 갱신하고, 그렇지 않으면 penalty를 키워 다음 subproblem에서 feasibility를 더 강하게 압박한다.

## KKT reformulation: K2, K2r, K1s

원래 NCL Newton system은 primal variable, free variable <math><mi>r</mi></math>, constraint multiplier를 모두 포함한다. 단순화한 block form으로 augmented KKT matrix는 다음과 같다.

<math display="block" aria-label="Augmented KKT matrix K2">
  <msub><mi>K</mi><mn>2</mn></msub>
  <mo>=</mo>
  <mfenced open="[" close="]">
    <mtable>
      <mtr><mtd><mover><mi>H</mi><mo>^</mo></mover><mo>+</mo><msub><mi>&delta;</mi><mi>k</mi></msub><mi>I</mi></mtd><mtd><mn>0</mn></mtd><mtd><mi>J</mi></mtd></mtr>
      <mtr><mtd><mn>0</mn></mtd><mtd><msub><mover><mi>&rho;</mi><mo>^</mo></mover><mi>k</mi></msub><mi>I</mi></mtd><mtd><mi>I</mi></mtd></mtr>
      <mtr><mtd><msup><mi>J</mi><mi>T</mi></msup></mtd><mtd><mi>I</mi></mtd><mtd><mn>0</mn></mtd></mtr>
    </mtable>
  </mfenced>
  <mo>.</mo>
</math>

여기서 <math><msub><mi>&delta;</mi><mi>k</mi></msub></math>는 IPM descent direction에 필요한 올바른 inertia를 맞추기 위한 regularization이다. 논문은 이 system에서 GPU에 더 맞는 두 가지 reduction을 유도한다.

첫째, <math><mi>r</mi></math> direction을 제거하면 stabilized KKT system인 K2r가 나온다.

<math display="block" aria-label="Stabilized KKT system K2r">
  <msub><mi>K</mi><mrow><mn>2</mn><mi>r</mi></mrow></msub>
  <mo>=</mo>
  <mfenced open="[" close="]">
    <mtable>
      <mtr><mtd><mover><mi>H</mi><mo>^</mo></mover><mo>+</mo><msub><mi>&delta;</mi><mi>k</mi></msub><mi>I</mi></mtd><mtd><mi>J</mi></mtd></mtr>
      <mtr><mtd><msup><mi>J</mi><mi>T</mi></msup></mtd><mtd><mo>-</mo><msub><mi>&theta;</mi><mi>k</mi></msub><mi>I</mi></mtd></mtr>
    </mtable>
  </mfenced>
  <mo>,</mo>
  <mspace width="0.6em"></mspace>
  <msub><mi>&theta;</mi><mi>k</mi></msub>
  <mo>=</mo>
  <msup><msub><mover><mi>&rho;</mi><mo>^</mo></mover><mi>k</mi></msub><mrow><mo>-</mo><mn>1</mn></mrow></msup>
  <mo>.</mo>
</math>

핵심은 lower-right block이 negative definite라는 점이다. 제거된 <math><mi>r</mi></math> 변수의 안정화 효과가 dual block에 남고, 이 구조는 static LDL factorization에 더 친화적이다.

둘째, dual direction까지 더 제거하면 K1s가 나온다. 핵심 matrix는 대략 다음 형태를 갖는다.

<math display="block" aria-label="Condensed K1s matrix intuition">
  <mover><mi>H</mi><mo>^</mo></mover>
  <mo>+</mo>
  <msub><mi>&delta;</mi><mi>k</mi></msub><mi>I</mi>
  <mo>+</mo>
  <mover><mi>&rho;</mi><mo>^</mo></mover>
  <msup><mi>J</mi><mi>T</mi></msup><mi>J</mi>
  <mo>.</mo>
</math>

K1s는 더 작고 Cholesky-like GPU solver에 매력적이다. 하지만 compact하게 만드는 condensation 자체가 ill-conditioning을 키울 수 있다. 따라서 논문의 empirical message는 K1s가 항상 우월하다는 것이 아니다. K2r가 더 robust한 default이고, K1s는 problem-dependent fast option에 가깝다.

이론적으로 중요한 기여 중 하나는 inertia equivalence다.

<math display="block" aria-label="Inertia equivalence">
  <mi>In</mi><mo>(</mo><msub><mi>K</mi><mn>2</mn></msub><mo>)</mo>
  <mo>=</mo><mo>(</mo><mi>n</mi><mo>+</mo><mi>m</mi><mo>,</mo><mi>m</mi><mo>,</mo><mn>0</mn><mo>)</mo>
  <mo>&iff;</mo>
  <mi>In</mi><mo>(</mo><msub><mi>K</mi><mrow><mn>2</mn><mi>r</mi></mrow></msub><mo>)</mo>
  <mo>=</mo><mo>(</mo><mi>n</mi><mo>,</mo><mi>m</mi><mo>,</mo><mn>0</mn><mo>)</mo>
  <mo>&iff;</mo>
  <mi>In</mi><mo>(</mo><msub><mi>K</mi><mrow><mn>1</mn><mi>s</mi></mrow></msub><mo>)</mo>
  <mo>=</mo><mo>(</mo><mi>n</mi><mo>,</mo><mn>0</mn><mo>,</mo><mn>0</mn><mo>)</mo>.
</math>

이 점이 중요한 이유는 GPU-friendly system들이 임의의 numerical trick이 아니기 때문이다. 명시된 조건 아래에서는 원래 NCL/IPM system의 descent-direction validity와 연결된다.

## 실제로 무엇이 보장되는가?

가장 강한 보장은 구조적이다. NCL formulation은 <math><mi>J</mi></math>를 <math><mo>[</mo><mi>J</mi><mspace width="0.3em"></mspace><mi>I</mi><mo>]</mo></math>로 바꾸어 constraint-Jacobian rank deficiency를 완화한다. 이것이 global optimum으로의 global convergence를 뜻하지는 않는다. 또한 모든 degeneracy mechanism에 대한 보장도 아니다. 주로 first-order constraint degeneracy를 다루는 장치다.

또한 논문은 KKT reduction을 inertia condition과 연결한다. 그래서 K2r나 K1s를 푸는 것이 원래 augmented system과 어떤 관계를 갖는지 설명할 수 있다. 이는 단순히 "condensation이 경험적으로 잘 된다"는 주장보다 강하다. 가정이 맞을 때 reformulated linear system이 유효한 IPM direction을 줄 수 있는 이유를 제공하기 때문이다.

Extrapolation step은 local acceleration 장치다. Inner/outer iteration이 충분히 가까워졌을 때 Newton-style extrapolation으로 inner solve를 생략하고 다음 outer iterate로 이동할 수 있다. 여기서 핵심은 solution 근처에서의 local superlinear behavior이지, 모든 instance가 처음부터 빨라진다는 주장이 아니다.

## 실험 결과 읽기

실험은 regime별로 읽어야 한다.

CUTEst CPU benchmark에서 MadNCL은 항상 Ipopt나 MadNLP보다 빠르지 않다. 가치가 있는 부분은 degrees of freedom 부족, restoration failure, excessive primal-dual regularization 때문에 IPM 계열이 실패하는 일부 문제를 해결한다는 점이다. 이는 speed dominance보다 robustness claim을 뒷받침한다.

GPU OPF와 COPS benchmark에서는 그림이 섞여 있지만 유익하다. 수십만 개 변수와 백만 개 이상의 제약을 가진 큰 OPF instance에서 MadNCL-K2r-cuDSS는 CPU MA27 기반 MadNCL-K2r보다 큰 speed-up을 보고한다. 동시에 K1s는 해당 OPF instance에서 실패할 수 있다. Condensation이 conditioning을 악화시키기 때문이다. 반면 COPS-type problem에서는 K1s가 안정적이고 빠를 수 있다. 실용적 결론은 KKT form selection이 problem dependent라는 것이다.

SCOPF-MPCC 결과는 논문의 핵심 주장과 가장 잘 맞는다. MPCC formulation은 모든 feasible point에서 MFCQ를 위반하므로 degeneracy가 피할 수 없다. 논문은 Ipopt와 MadNLP가 restoration failure나 infeasible solution으로 끝날 수 있는 반면, MadNCL-K2r는 CPU/GPU 모두에서 테스트한 instance를 보고된 tolerance까지 해결한다고 말한다. 이것이 NCL regularization과 stabilized KKT system의 결합이 실제 degenerate large-scale model에서 의미 있음을 보여주는 가장 선명한 증거다.

## 한계

첫째, MadNCL은 모든 GPU-IPM보다 빠른 보편적 개선이 아니다. Regular OPF instance에서는 다른 GPU IPM formulation이 더 빠를 수 있다. MadNCL의 차별점은 GPU throughput을 유지하면서 degeneracy 아래의 robustness를 높이는 데 있다.

둘째, NCL이 모든 degeneracy를 해결하는 것은 아니다. 이 mechanism은 constraint-Jacobian degeneracy와 LICQ failure에 가장 강하다. Reduced Hessian이 nearly singular하거나 더 깊은 second-order degeneracy가 있으면 augmented-Lagrangian story가 같은 보호를 제공한다고 볼 수 없다.

마지막으로, 가장 퇴화가 강한 MPCC 실험 일부는 표준 NLP benchmark보다 완화된 tolerance를 사용한다. 이것은 실용적으로 타당할 수 있지만, 모든 degenerate case를 high precision으로 해결했다는 의미는 아니다.

## 평가

이 논문은 implementation-theory hybrid paper로 읽는 것이 가장 정확하다. 완전히 새로운 최적화 원리를 발견했다기보다, ALM/NCL의 오래된 robustness advantage가 second-order NLP solver를 GPU로 옮기는 시대에 다시 중요해질 수 있음을 보여준다.

핵심 흐름은 다음과 같다.

```text
degenerate NLP
  -> NCL regularization
  -> better structured KKT systems
  -> GPU-compatible sparse factorization
  -> robust large-scale solver behavior
```

Formulation-level regularization을 GPU-friendly KKT linear algebra까지 일관되게 밀어붙였고, 그 조합이 SCOPF-MPCC 같은 large-scale degenerate NLP에서 실제로 유용하다는 점을 보였다는 데 있다.

## References

Montoison, A., Pacaud, F., Saunders, M., Shin, S., & Orban, D. (2025). MADNCL: a GPU implementation of algorithm NCL for large-scale, degenerate nonlinear programs. arXiv preprint arXiv:2510.05885.
