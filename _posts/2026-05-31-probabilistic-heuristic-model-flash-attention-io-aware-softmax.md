---
layout: post
title: "FlashAttention: Exact Attention as an IO-Aware Streaming Computation"
title_ko: "FlashAttention: IO 인식 스트리밍 계산으로서의 정확한 어텐션"
date: 2026-05-31
category: probabilistic-heuristic-model
category_label: "Probabilistic Heuristics & Bayesian Search"
research_group: algorithmic_reviews
research_category: probabilistic-heuristic-model
research_category_label: "Probabilistic Heuristics & Bayesian Search"
application_category: ""
application_category_label: ""
method_category: llm-probabilistic-approaches
method_category_label: "LLM & Probabilistic Approaches"
paper_title: "Stanford CME295 Transformers & LLMs | Autumn 2025 | Lecture 4 - LLM Training"
authors: ""
venue: "Stanford CME295 Transformers & LLMs"
year: "2025"
doi: ""
arxiv: ""
source_url: ""
tags:
  - flash-attention
  - transformer
  - attention
  - memory-hierarchy
  - online-softmax
  - gpu
excerpt: "FlashAttention is not an approximation to attention. Its core idea is to avoid materializing the N by N attention matrix in HBM by computing tiled attention in SRAM and maintaining online softmax statistics."
excerpt_ko: "FlashAttention은 어텐션의 근사가 아니다. 핵심은 SRAM에서 타일 단위 어텐션을 계산하고 online softmax 통계를 유지함으로써 HBM에 N by N 어텐션 행렬을 만들지 않는 것이다."
language: "en-ko"
has_korean_note: false
---

## Positioning

FlashAttention is best understood as an IO-aware implementation of exact Transformer attention. It does not change the attention definition, and it does not remove the pairwise interaction between every query and every key. Its contribution is more specific: it reorganizes the computation so that the large attention score and probability matrices do not have to be written to and read from high-bandwidth memory.

This distinction matters for long-context language models. Standard attention is expensive not only because it performs many dot products, but also because a naive implementation moves large intermediate matrices through global GPU memory. When sequence length grows, memory traffic can become a practical bottleneck even when the arithmetic units are powerful.

The useful mental model is therefore not "approximate attention." It is "stream exact attention through fast on-chip memory while keeping only the statistics needed to normalize softmax correctly."

## Problem setting

For a sequence of length <math><mi>N</mi></math> and head dimension <math><mi>d</mi></math>, scaled dot-product attention is

<math display="block" aria-label="Scaled dot product attention">
  <mi>O</mi>
  <mo>=</mo>
  <mtext>softmax</mtext>
  <mo>(</mo>
  <mfrac>
    <mrow><mi>Q</mi><msup><mi>K</mi><mi>T</mi></msup></mrow>
    <msqrt><mi>d</mi></msqrt>
  </mfrac>
  <mo>)</mo>
  <mi>V</mi><mo>.</mo>
</math>

The naive implementation follows the formula too literally:

```text
Q, K, V
  |
  v
S = QK^T          full N by N score matrix written to HBM
  |
  v
P = softmax(S)   full N by N probability matrix written to HBM
  |
  v
O = PV
```

Here <math><mi>S</mi></math> and <math><mi>P</mi></math> are both <math><mi>N</mi><mo>&times;</mo><mi>N</mi></math> matrices. For <math><mi>N</mi><mo>=</mo><mn>4096</mn></math>, this means more than sixteen million entries per attention matrix per head before considering batch size, precision, layers, or backward-pass storage. The mathematical object is attention, but the implementation has materialized large intermediate objects that are not needed as final outputs.

## Prior research gap

The gap is not that ordinary attention is mathematically wrong. The gap is between the algebraic formula and an efficient memory-access pattern on modern GPUs.

HBM is large enough to store model activations and intermediate tensors, but it is far from the compute units relative to on-chip SRAM, shared memory, and registers. A naive attention kernel repeatedly writes and reads the full <math><mi>N</mi><mo>&times;</mo><mi>N</mi></math> score and probability matrices. This creates heavy HBM traffic. As sequence length increases, the cost of moving these matrices can dominate the wall-clock behavior of the kernel.

The prior implementation pattern therefore wastes memory bandwidth by storing an object whose entries are immediately consumed by the following softmax and value multiplication. FlashAttention asks whether the same final output can be produced without ever materializing that object in HBM.

## Core idea

FlashAttention computes attention in tiles. It loads a block of queries into on-chip memory, streams blocks of keys and values through it, computes temporary score tiles, updates row-wise softmax statistics, accumulates the output numerator, and discards the temporary scores.

```text
Q_tile, K_tile, V_tile
  |
  v
S_tile = Q_tile K_tile^T
  |
  v
update running max, denominator, and output accumulator
  |
  v
discard S_tile
  |
  v
write final O_tile only
```

The important point is that FlashAttention does not merely split the attention matrix into smaller matrices and store them. Its stronger idea is to avoid storing the full score matrix <math><mi>S</mi></math> and softmax probability matrix <math><mi>P</mi></math> in HBM at all. Temporary score tiles live only long enough to update the online softmax state and output accumulator.

## Mathematical structure

For one query row <math><msub><mi>q</mi><mi>i</mi></msub></math>, define scores

<math display="block" aria-label="Attention score for one query and key">
  <msub><mi>s</mi><mrow><mi>i</mi><mi>j</mi></mrow></msub>
  <mo>=</mo>
  <msubsup><mi>q</mi><mi>i</mi><mi>T</mi></msubsup>
  <msub><mi>k</mi><mi>j</mi></msub><mo>.</mo>
</math>

The attention output for that query is

<math display="block" aria-label="Attention output as normalized weighted sum">
  <msub><mi>o</mi><mi>i</mi></msub>
  <mo>=</mo>
  <mfrac>
    <mrow>
      <msub><mo>&sum;</mo><mi>j</mi></msub>
      <mi>exp</mi><mo>(</mo><msub><mi>s</mi><mrow><mi>i</mi><mi>j</mi></mrow></msub><mo>)</mo>
      <msub><mi>v</mi><mi>j</mi></msub>
    </mrow>
    <mrow>
      <msub><mo>&sum;</mo><mi>j</mi></msub>
      <mi>exp</mi><mo>(</mo><msub><mi>s</mi><mrow><mi>i</mi><mi>j</mi></mrow></msub><mo>)</mo>
    </mrow>
  </mfrac><mo>.</mo>
</math>

Naively, this looks as if all scores <math><msub><mi>s</mi><mrow><mi>i</mi><mi>j</mi></mrow></msub></math> must be stored before normalization. The online softmax identity shows that this is not necessary. For keys processed so far, maintain a running maximum

<math display="block" aria-label="Running softmax maximum">
  <msub><mi>m</mi><mi>i</mi></msub>
  <mo>=</mo>
  <munder><mi>max</mi><mrow><mi>j</mi><mo>&in;</mo><mtext>processed</mtext></mrow></munder>
  <msub><mi>s</mi><mrow><mi>i</mi><mi>j</mi></mrow></msub><mo>,</mo>
</math>

a running denominator

<math display="block" aria-label="Running softmax denominator">
  <msub><mi>&ell;</mi><mi>i</mi></msub>
  <mo>=</mo>
  <msub><mo>&sum;</mo><mrow><mi>j</mi><mo>&in;</mo><mtext>processed</mtext></mrow></msub>
  <mi>exp</mi><mo>(</mo>
  <msub><mi>s</mi><mrow><mi>i</mi><mi>j</mi></mrow></msub>
  <mo>-</mo><msub><mi>m</mi><mi>i</mi></msub>
  <mo>)</mo><mo>,</mo>
</math>

and an unnormalized output accumulator

<math display="block" aria-label="Running unnormalized output accumulator">
  <msub><mi>a</mi><mi>i</mi></msub>
  <mo>=</mo>
  <msub><mo>&sum;</mo><mrow><mi>j</mi><mo>&in;</mo><mtext>processed</mtext></mrow></msub>
  <mi>exp</mi><mo>(</mo>
  <msub><mi>s</mi><mrow><mi>i</mi><mi>j</mi></mrow></msub>
  <mo>-</mo><msub><mi>m</mi><mi>i</mi></msub>
  <mo>)</mo>
  <msub><mi>v</mi><mi>j</mi></msub><mo>.</mo>
</math>

The term <math><msub><mi>m</mi><mi>i</mi></msub></math> is the row-wise maximum used for numerical stability. The term <math><msub><mi>&ell;</mi><mi>i</mi></msub></math> is the softmax denominator after subtracting that maximum. The term <math><msub><mi>a</mi><mi>i</mi></msub></math> is the numerator before final division.

When a new key-value block arrives, define its local maximum and the updated maximum:

<math display="block" aria-label="Updated softmax maximum after a new block">
  <msubsup><mi>m</mi><mi>i</mi><mtext>block</mtext></msubsup>
  <mo>=</mo>
  <munder><mi>max</mi><mrow><mi>j</mi><mo>&in;</mo><mtext>block</mtext></mrow></munder>
  <msub><mi>s</mi><mrow><mi>i</mi><mi>j</mi></mrow></msub><mo>,</mo>
  <mspace width="0.8em"></mspace>
  <msubsup><mi>m</mi><mi>i</mi><mtext>new</mtext></msubsup>
  <mo>=</mo>
  <mi>max</mi><mo>(</mo>
  <msubsup><mi>m</mi><mi>i</mi><mtext>old</mtext></msubsup>
  <mo>,</mo>
  <msubsup><mi>m</mi><mi>i</mi><mtext>block</mtext></msubsup>
  <mo>)</mo><mo>.</mo>
</math>

Then update the denominator and accumulator:

<math display="block" aria-label="Online softmax denominator update">
  <msubsup><mi>&ell;</mi><mi>i</mi><mtext>new</mtext></msubsup>
  <mo>=</mo>
  <mi>exp</mi><mo>(</mo>
  <msubsup><mi>m</mi><mi>i</mi><mtext>old</mtext></msubsup>
  <mo>-</mo>
  <msubsup><mi>m</mi><mi>i</mi><mtext>new</mtext></msubsup>
  <mo>)</mo>
  <msubsup><mi>&ell;</mi><mi>i</mi><mtext>old</mtext></msubsup>
  <mo>+</mo>
  <msub><mo>&sum;</mo><mrow><mi>j</mi><mo>&in;</mo><mtext>block</mtext></mrow></msub>
  <mi>exp</mi><mo>(</mo>
  <msub><mi>s</mi><mrow><mi>i</mi><mi>j</mi></mrow></msub>
  <mo>-</mo>
  <msubsup><mi>m</mi><mi>i</mi><mtext>new</mtext></msubsup>
  <mo>)</mo><mo>,</mo>
</math>

<math display="block" aria-label="Online softmax accumulator update">
  <msubsup><mi>a</mi><mi>i</mi><mtext>new</mtext></msubsup>
  <mo>=</mo>
  <mi>exp</mi><mo>(</mo>
  <msubsup><mi>m</mi><mi>i</mi><mtext>old</mtext></msubsup>
  <mo>-</mo>
  <msubsup><mi>m</mi><mi>i</mi><mtext>new</mtext></msubsup>
  <mo>)</mo>
  <msubsup><mi>a</mi><mi>i</mi><mtext>old</mtext></msubsup>
  <mo>+</mo>
  <msub><mo>&sum;</mo><mrow><mi>j</mi><mo>&in;</mo><mtext>block</mtext></mrow></msub>
  <mi>exp</mi><mo>(</mo>
  <msub><mi>s</mi><mrow><mi>i</mi><mi>j</mi></mrow></msub>
  <mo>-</mo>
  <msubsup><mi>m</mi><mi>i</mi><mtext>new</mtext></msubsup>
  <mo>)</mo>
  <msub><mi>v</mi><mi>j</mi></msub><mo>.</mo>
</math>

The exponential rescaling term adjusts all previously accumulated quantities when a larger maximum is discovered in the new block. At the end,

<math display="block" aria-label="Final online softmax output">
  <msub><mi>o</mi><mi>i</mi></msub>
  <mo>=</mo>
  <mfrac><msub><mi>a</mi><mi>i</mi></msub><msub><mi>&ell;</mi><mi>i</mi></msub></mfrac><mo>.</mo>
</math>

This is the mathematical reason FlashAttention can stream over key-value blocks without storing the full score vector for each query.

## Why it can work

FlashAttention works because softmax normalization can be decomposed into row-wise running statistics. The algorithm only needs the current query tile, the current key-value tile, a temporary score tile, and row-wise statistics. It does not need the full attention row in memory at once.

For query and key block sizes <math><msub><mi>B</mi><mi>q</mi></msub></math> and <math><msub><mi>B</mi><mi>k</mi></msub></math>, SRAM stores objects such as

<math display="block" aria-label="Objects stored during tiled attention">
  <msub><mi>Q</mi><mtext>tile</mtext></msub>
  <mo>&in;</mo><msup><mi>R</mi><mrow><msub><mi>B</mi><mi>q</mi></msub><mo>&times;</mo><mi>d</mi></mrow></msup>
  <mo>,</mo>
  <mspace width="0.5em"></mspace>
  <msub><mi>K</mi><mtext>tile</mtext></msub>
  <mo>&in;</mo><msup><mi>R</mi><mrow><msub><mi>B</mi><mi>k</mi></msub><mo>&times;</mo><mi>d</mi></mrow></msup>
  <mo>,</mo>
  <mspace width="0.5em"></mspace>
  <msub><mi>V</mi><mtext>tile</mtext></msub>
  <mo>&in;</mo><msup><mi>R</mi><mrow><msub><mi>B</mi><mi>k</mi></msub><mo>&times;</mo><mi>d</mi></mrow></msup><mo>.</mo>
</math>

It also stores the temporary score tile and row-wise statistics:

<math display="block" aria-label="Temporary score tile and row-wise statistics">
  <msub><mi>S</mi><mtext>tile</mtext></msub>
  <mo>=</mo>
  <msub><mi>Q</mi><mtext>tile</mtext></msub>
  <msubsup><mi>K</mi><mtext>tile</mtext><mi>T</mi></msubsup>
  <mo>&in;</mo>
  <msup><mi>R</mi><mrow><msub><mi>B</mi><mi>q</mi></msub><mo>&times;</mo><msub><mi>B</mi><mi>k</mi></msub></mrow></msup>
  <mo>,</mo>
  <mspace width="0.5em"></mspace>
  <mi>m</mi><mo>&in;</mo><msup><mi>R</mi><msub><mi>B</mi><mi>q</mi></msub></msup>
  <mo>,</mo>
  <mspace width="0.5em"></mspace>
  <mi>&ell;</mi><mo>&in;</mo><msup><mi>R</mi><msub><mi>B</mi><mi>q</mi></msub></msup>
  <mo>,</mo>
  <mspace width="0.5em"></mspace>
  <mi>A</mi><mo>&in;</mo><msup><mi>R</mi><mrow><msub><mi>B</mi><mi>q</mi></msub><mo>&times;</mo><mi>d</mi></mrow></msup><mo>.</mo>
</math>

If <math><mi>N</mi><mo>=</mo><mn>4096</mn></math>, the full score matrix has <math><mn>4096</mn><mo>&times;</mo><mn>4096</mn></math> entries. But if <math><msub><mi>B</mi><mi>q</mi></msub><mo>=</mo><mn>128</mn></math> and <math><msub><mi>B</mi><mi>k</mi></msub><mo>=</mo><mn>64</mn></math>, the temporary score tile has only <math><mn>8192</mn></math> entries. SRAM cannot hold the full attention matrix, but it can hold a carefully chosen tile and the running statistics needed to make the streamed computation exact.

## Assumptions and limitations

The performance benefit comes from memory movement, not magical arithmetic. FLOPs are executed by Tensor Cores, CUDA cores, or similar compute units. SRAM does not make a floating-point multiply-add intrinsically different. Its advantage is that on-chip memory is physically closer to the compute units and can provide lower latency, higher effective bandwidth, lower energy per access, and better data reuse than HBM.

Several limitations should be stated clearly.

- FlashAttention still computes pairwise query-key interactions. The arithmetic complexity remains quadratic in sequence length for standard dense attention.
- It does not make attention theoretically linear in <math><mi>N</mi></math>.
- It does not solve the semantic or modeling limitations of attention.
- Actual speedup depends on GPU architecture, tile size, precision, kernel implementation, sequence length, causal masking, and memory bandwidth.
- Numerical results can differ slightly from a naive implementation because floating-point operations occur in a different order and precision regime.

The exact claim is therefore narrow but important: FlashAttention computes mathematically equivalent softmax attention up to floating-point differences while avoiding the materialization of full <math><mi>N</mi><mo>&times;</mo><mi>N</mi></math> score and probability matrices in HBM.

## Critical assessment

The strongest part of FlashAttention is that it identifies the real implementation bottleneck. A simple reading of the attention formula focuses on <math><mi>Q</mi><msup><mi>K</mi><mi>T</mi></msup></math> and <math><mi>P</mi><mi>V</mi></math> as matrix multiplications. A systems reading asks where the intermediate tensors live, how often they cross the HBM boundary, and whether they can be consumed before being stored.

The online softmax update is also conceptually clean. It is not a heuristic normalization trick. It preserves the correct numerator and denominator by rescaling previously accumulated terms whenever the running maximum changes. This is why FlashAttention can be exact rather than approximate.

The risk is rhetorical overstatement. FlashAttention should not be described as solving quadratic attention. It reduces memory traffic and improves practical GPU utilization for an important attention workload. That is a major systems contribution, but it is not a new attention model, not a proof of better language modeling, and not a universal speed guarantee.

## Takeaway

FlashAttention is an IO-aware reordering of exact attention computation. It keeps the same attention semantics, avoids materializing the full <math><mi>N</mi><mo>&times;</mo><mi>N</mi></math> intermediate matrices, and uses online softmax statistics to stream the computation through fast on-chip memory. The right claim is precise: less HBM traffic and exact softmax attention up to floating-point differences, not a removal of the quadratic interaction structure.

## References

- Stanford CME295 Transformers & LLMs | Autumn 2025 | Lecture 4 - LLM Training. Bibliographic details beyond the lecture title, course identifier, and year were not provided in the supplied material.

<!-- ko -->

## 포지셔닝

FlashAttention은 정확한 Transformer attention을 IO 관점에서 다시 구현한 방법으로 이해하는 것이 가장 적절하다. 어텐션의 정의를 바꾸지 않으며, 모든 query와 모든 key 사이의 상호작용을 제거하지도 않는다. 기여는 더 구체적이다. 큰 attention score 행렬과 probability 행렬을 high-bandwidth memory에 쓰고 다시 읽지 않도록 계산 순서를 재구성한다.

이 구분은 long-context language model에서 중요하다. 표준 attention은 많은 dot product를 수행하기 때문에 비싸지만, 그것만이 문제가 아니다. naive implementation은 큰 중간 행렬을 GPU global memory를 통해 반복적으로 이동시킨다. sequence length가 커질수록 산술 연산보다 memory traffic이 실제 병목이 될 수 있다.

따라서 유용한 관점은 "근사 attention"이 아니다. 더 정확한 관점은 "softmax를 정확히 정규화하는 데 필요한 통계만 유지하면서, 빠른 on-chip memory를 통해 정확한 attention을 stream한다"는 것이다.

## 문제 설정

sequence length가 <math><mi>N</mi></math>이고 head dimension이 <math><mi>d</mi></math>일 때 scaled dot-product attention은 다음과 같다.

<math display="block" aria-label="Scaled dot product attention">
  <mi>O</mi>
  <mo>=</mo>
  <mtext>softmax</mtext>
  <mo>(</mo>
  <mfrac>
    <mrow><mi>Q</mi><msup><mi>K</mi><mi>T</mi></msup></mrow>
    <msqrt><mi>d</mi></msqrt>
  </mfrac>
  <mo>)</mo>
  <mi>V</mi><mo>.</mo>
</math>

naive implementation은 이 식을 너무 직접적으로 따른다.

```text
Q, K, V
  |
  v
S = QK^T          full N by N score matrix written to HBM
  |
  v
P = softmax(S)   full N by N probability matrix written to HBM
  |
  v
O = PV
```

여기서 <math><mi>S</mi></math>와 <math><mi>P</mi></math>는 모두 <math><mi>N</mi><mo>&times;</mo><mi>N</mi></math> 행렬이다. <math><mi>N</mi><mo>=</mo><mn>4096</mn></math>이면 batch size, precision, layer 수, backward-pass 저장량을 고려하기 전에도 한 head의 attention 행렬 하나에 1,600만 개가 넘는 entry가 필요하다. 수학적 대상은 attention이지만, 구현은 최종 출력으로 필요하지 않은 거대한 중간 객체를 materialize하고 있다.

## 선행 접근의 간극

문제는 보통의 attention이 수학적으로 틀렸다는 것이 아니다. 간극은 대수적 공식과 현대 GPU에서 효율적인 memory-access pattern 사이에 있다.

HBM은 model activation과 intermediate tensor를 저장할 만큼 크지만, on-chip SRAM, shared memory, register에 비해 compute unit에서 멀리 있다. naive attention kernel은 전체 <math><mi>N</mi><mo>&times;</mo><mi>N</mi></math> score 행렬과 probability 행렬을 반복적으로 쓰고 읽는다. 이것이 큰 HBM traffic을 만든다. sequence length가 증가하면 이러한 행렬 이동 비용이 kernel의 실제 실행 시간을 지배할 수 있다.

따라서 기존 구현 패턴의 낭비는 다음과 같다. 바로 다음 softmax와 value multiplication에서 소비될 객체를 memory bandwidth를 써가며 저장한다. FlashAttention은 같은 최종 출력을 만들면서 그 객체를 HBM에 만들지 않을 수 있는지를 묻는다.

## 핵심 아이디어

FlashAttention은 attention을 tile 단위로 계산한다. query block을 on-chip memory에 올리고, key와 value block을 순차적으로 stream하며, temporary score tile을 계산하고, row-wise softmax statistics를 업데이트하고, output numerator를 누적한 뒤 temporary score를 버린다.

```text
Q_tile, K_tile, V_tile
  |
  v
S_tile = Q_tile K_tile^T
  |
  v
update running max, denominator, and output accumulator
  |
  v
discard S_tile
  |
  v
write final O_tile only
```

중요한 점은 FlashAttention이 attention matrix를 작은 조각으로 나누어 저장하는 방법이 아니라는 것이다. 더 강한 아이디어는 score matrix <math><mi>S</mi></math>와 softmax probability matrix <math><mi>P</mi></math> 전체를 HBM에 저장하지 않는 것이다. temporary score tile은 online softmax state와 output accumulator를 업데이트하는 동안만 존재한다.

## 수학적 구조

하나의 query row <math><msub><mi>q</mi><mi>i</mi></msub></math>에 대해 score를 다음과 같이 정의한다.

<math display="block" aria-label="Attention score for one query and key">
  <msub><mi>s</mi><mrow><mi>i</mi><mi>j</mi></mrow></msub>
  <mo>=</mo>
  <msubsup><mi>q</mi><mi>i</mi><mi>T</mi></msubsup>
  <msub><mi>k</mi><mi>j</mi></msub><mo>.</mo>
</math>

그 query의 attention output은 다음의 normalized weighted sum이다.

<math display="block" aria-label="Attention output as normalized weighted sum">
  <msub><mi>o</mi><mi>i</mi></msub>
  <mo>=</mo>
  <mfrac>
    <mrow>
      <msub><mo>&sum;</mo><mi>j</mi></msub>
      <mi>exp</mi><mo>(</mo><msub><mi>s</mi><mrow><mi>i</mi><mi>j</mi></mrow></msub><mo>)</mo>
      <msub><mi>v</mi><mi>j</mi></msub>
    </mrow>
    <mrow>
      <msub><mo>&sum;</mo><mi>j</mi></msub>
      <mi>exp</mi><mo>(</mo><msub><mi>s</mi><mrow><mi>i</mi><mi>j</mi></mrow></msub><mo>)</mo>
    </mrow>
  </mfrac><mo>.</mo>
</math>

겉으로 보면 모든 score <math><msub><mi>s</mi><mrow><mi>i</mi><mi>j</mi></mrow></msub></math>를 저장한 뒤 정규화해야 할 것처럼 보인다. 그러나 online softmax identity는 이것이 필요하지 않음을 보여준다. 지금까지 처리한 key들에 대해 running maximum을 유지한다.

<math display="block" aria-label="Running softmax maximum">
  <msub><mi>m</mi><mi>i</mi></msub>
  <mo>=</mo>
  <munder><mi>max</mi><mrow><mi>j</mi><mo>&in;</mo><mtext>processed</mtext></mrow></munder>
  <msub><mi>s</mi><mrow><mi>i</mi><mi>j</mi></mrow></msub><mo>.</mo>
</math>

또한 running denominator와 unnormalized output accumulator를 유지한다.

<math display="block" aria-label="Running softmax denominator">
  <msub><mi>&ell;</mi><mi>i</mi></msub>
  <mo>=</mo>
  <msub><mo>&sum;</mo><mrow><mi>j</mi><mo>&in;</mo><mtext>processed</mtext></mrow></msub>
  <mi>exp</mi><mo>(</mo>
  <msub><mi>s</mi><mrow><mi>i</mi><mi>j</mi></mrow></msub>
  <mo>-</mo><msub><mi>m</mi><mi>i</mi></msub>
  <mo>)</mo><mo>,</mo>
</math>

<math display="block" aria-label="Running unnormalized output accumulator">
  <msub><mi>a</mi><mi>i</mi></msub>
  <mo>=</mo>
  <msub><mo>&sum;</mo><mrow><mi>j</mi><mo>&in;</mo><mtext>processed</mtext></mrow></msub>
  <mi>exp</mi><mo>(</mo>
  <msub><mi>s</mi><mrow><mi>i</mi><mi>j</mi></mrow></msub>
  <mo>-</mo><msub><mi>m</mi><mi>i</mi></msub>
  <mo>)</mo>
  <msub><mi>v</mi><mi>j</mi></msub><mo>.</mo>
</math>

<math><msub><mi>m</mi><mi>i</mi></msub></math>는 numerical stability를 위한 row-wise maximum이다. <math><msub><mi>&ell;</mi><mi>i</mi></msub></math>는 그 maximum을 뺀 뒤의 softmax denominator이다. <math><msub><mi>a</mi><mi>i</mi></msub></math>는 마지막 나눗셈 전의 numerator이다.

새로운 key-value block이 들어오면 block maximum과 updated maximum을 계산한다.

<math display="block" aria-label="Updated softmax maximum after a new block">
  <msubsup><mi>m</mi><mi>i</mi><mtext>block</mtext></msubsup>
  <mo>=</mo>
  <munder><mi>max</mi><mrow><mi>j</mi><mo>&in;</mo><mtext>block</mtext></mrow></munder>
  <msub><mi>s</mi><mrow><mi>i</mi><mi>j</mi></mrow></msub><mo>,</mo>
  <mspace width="0.8em"></mspace>
  <msubsup><mi>m</mi><mi>i</mi><mtext>new</mtext></msubsup>
  <mo>=</mo>
  <mi>max</mi><mo>(</mo>
  <msubsup><mi>m</mi><mi>i</mi><mtext>old</mtext></msubsup>
  <mo>,</mo>
  <msubsup><mi>m</mi><mi>i</mi><mtext>block</mtext></msubsup>
  <mo>)</mo><mo>.</mo>
</math>

그 다음 denominator와 accumulator를 업데이트한다.

<math display="block" aria-label="Online softmax denominator update">
  <msubsup><mi>&ell;</mi><mi>i</mi><mtext>new</mtext></msubsup>
  <mo>=</mo>
  <mi>exp</mi><mo>(</mo>
  <msubsup><mi>m</mi><mi>i</mi><mtext>old</mtext></msubsup>
  <mo>-</mo>
  <msubsup><mi>m</mi><mi>i</mi><mtext>new</mtext></msubsup>
  <mo>)</mo>
  <msubsup><mi>&ell;</mi><mi>i</mi><mtext>old</mtext></msubsup>
  <mo>+</mo>
  <msub><mo>&sum;</mo><mrow><mi>j</mi><mo>&in;</mo><mtext>block</mtext></mrow></msub>
  <mi>exp</mi><mo>(</mo>
  <msub><mi>s</mi><mrow><mi>i</mi><mi>j</mi></mrow></msub>
  <mo>-</mo>
  <msubsup><mi>m</mi><mi>i</mi><mtext>new</mtext></msubsup>
  <mo>)</mo><mo>,</mo>
</math>

<math display="block" aria-label="Online softmax accumulator update">
  <msubsup><mi>a</mi><mi>i</mi><mtext>new</mtext></msubsup>
  <mo>=</mo>
  <mi>exp</mi><mo>(</mo>
  <msubsup><mi>m</mi><mi>i</mi><mtext>old</mtext></msubsup>
  <mo>-</mo>
  <msubsup><mi>m</mi><mi>i</mi><mtext>new</mtext></msubsup>
  <mo>)</mo>
  <msubsup><mi>a</mi><mi>i</mi><mtext>old</mtext></msubsup>
  <mo>+</mo>
  <msub><mo>&sum;</mo><mrow><mi>j</mi><mo>&in;</mo><mtext>block</mtext></mrow></msub>
  <mi>exp</mi><mo>(</mo>
  <msub><mi>s</mi><mrow><mi>i</mi><mi>j</mi></mrow></msub>
  <mo>-</mo>
  <msubsup><mi>m</mi><mi>i</mi><mtext>new</mtext></msubsup>
  <mo>)</mo>
  <msub><mi>v</mi><mi>j</mi></msub><mo>.</mo>
</math>

여기서 exponential rescaling term은 새로운 block에서 더 큰 maximum이 발견되었을 때 이전에 누적된 값들을 새 기준에 맞추어 조정한다. 마지막에는 다음과 같이 출력한다.

<math display="block" aria-label="Final online softmax output">
  <msub><mi>o</mi><mi>i</mi></msub>
  <mo>=</mo>
  <mfrac><msub><mi>a</mi><mi>i</mi></msub><msub><mi>&ell;</mi><mi>i</mi></msub></mfrac><mo>.</mo>
</math>

이것이 FlashAttention이 각 query에 대한 전체 score vector를 저장하지 않고도 key-value block을 stream할 수 있는 수학적 이유다.

## 왜 작동할 수 있는가

FlashAttention이 작동하는 이유는 softmax normalization을 row-wise running statistics로 분해할 수 있기 때문이다. 알고리즘은 현재 query tile, 현재 key-value tile, temporary score tile, row-wise statistics만 필요로 한다. 전체 attention row를 한 번에 memory에 둘 필요가 없다.

query와 key block size를 <math><msub><mi>B</mi><mi>q</mi></msub></math>, <math><msub><mi>B</mi><mi>k</mi></msub></math>라고 하면 SRAM에는 다음과 같은 객체가 올라간다.

<math display="block" aria-label="Objects stored during tiled attention">
  <msub><mi>Q</mi><mtext>tile</mtext></msub>
  <mo>&in;</mo><msup><mi>R</mi><mrow><msub><mi>B</mi><mi>q</mi></msub><mo>&times;</mo><mi>d</mi></mrow></msup>
  <mo>,</mo>
  <mspace width="0.5em"></mspace>
  <msub><mi>K</mi><mtext>tile</mtext></msub>
  <mo>&in;</mo><msup><mi>R</mi><mrow><msub><mi>B</mi><mi>k</mi></msub><mo>&times;</mo><mi>d</mi></mrow></msup>
  <mo>,</mo>
  <mspace width="0.5em"></mspace>
  <msub><mi>V</mi><mtext>tile</mtext></msub>
  <mo>&in;</mo><msup><mi>R</mi><mrow><msub><mi>B</mi><mi>k</mi></msub><mo>&times;</mo><mi>d</mi></mrow></msup><mo>.</mo>
</math>

또한 temporary score tile과 row-wise statistics가 저장된다.

<math display="block" aria-label="Temporary score tile and row-wise statistics">
  <msub><mi>S</mi><mtext>tile</mtext></msub>
  <mo>=</mo>
  <msub><mi>Q</mi><mtext>tile</mtext></msub>
  <msubsup><mi>K</mi><mtext>tile</mtext><mi>T</mi></msubsup>
  <mo>&in;</mo>
  <msup><mi>R</mi><mrow><msub><mi>B</mi><mi>q</mi></msub><mo>&times;</mo><msub><mi>B</mi><mi>k</mi></msub></mrow></msup>
  <mo>,</mo>
  <mspace width="0.5em"></mspace>
  <mi>m</mi><mo>&in;</mo><msup><mi>R</mi><msub><mi>B</mi><mi>q</mi></msub></msup>
  <mo>,</mo>
  <mspace width="0.5em"></mspace>
  <mi>&ell;</mi><mo>&in;</mo><msup><mi>R</mi><msub><mi>B</mi><mi>q</mi></msub></msup>
  <mo>,</mo>
  <mspace width="0.5em"></mspace>
  <mi>A</mi><mo>&in;</mo><msup><mi>R</mi><mrow><msub><mi>B</mi><mi>q</mi></msub><mo>&times;</mo><mi>d</mi></mrow></msup><mo>.</mo>
</math>

<math><mi>N</mi><mo>=</mo><mn>4096</mn></math>이면 full score matrix는 <math><mn>4096</mn><mo>&times;</mo><mn>4096</mn></math> entry를 가진다. 그러나 <math><msub><mi>B</mi><mi>q</mi></msub><mo>=</mo><mn>128</mn></math>, <math><msub><mi>B</mi><mi>k</mi></msub><mo>=</mo><mn>64</mn></math>이면 temporary score tile은 <math><mn>8192</mn></math> entry만 가진다. SRAM은 전체 attention matrix를 담을 수 없지만, 적절히 선택된 tile과 정확한 streamed computation에 필요한 running statistics는 담을 수 있다.

## 가정과 한계

성능 이득은 memory movement에서 온다. 산술 연산 자체가 마법처럼 빨라지는 것이 아니다. FLOP은 Tensor Core, CUDA core 또는 유사한 compute unit에서 실행된다. SRAM의 장점은 on-chip memory가 compute unit에 물리적으로 더 가깝고, HBM보다 낮은 latency, 높은 effective bandwidth, 낮은 access energy, 더 나은 data reuse를 제공할 수 있다는 데 있다.

명확히 말해야 할 한계도 있다.

- FlashAttention은 여전히 pairwise query-key interaction을 계산한다. 표준 dense attention의 arithmetic complexity는 sequence length에 대해 여전히 quadratic이다.
- attention을 이론적으로 <math><mi>N</mi></math>에 대해 linear하게 만들지 않는다.
- attention의 semantic 또는 modeling limitation을 해결하지 않는다.
- 실제 speedup은 GPU architecture, tile size, precision, kernel implementation, sequence length, causal masking, memory bandwidth에 의존한다.
- floating-point operation의 순서와 precision regime이 달라지기 때문에 naive implementation과 수치적으로 약간 다를 수 있다.

따라서 정확한 주장은 좁지만 중요하다. FlashAttention은 full <math><mi>N</mi><mo>&times;</mo><mi>N</mi></math> score/probability matrix를 HBM에 materialize하지 않으면서, floating-point 차이를 제외하면 수학적으로 동등한 softmax attention을 계산한다.

## 비판적 평가

FlashAttention의 가장 강한 지점은 실제 구현 병목을 정확히 짚는다는 데 있다. attention 공식을 단순히 읽으면 <math><mi>Q</mi><msup><mi>K</mi><mi>T</mi></msup></math>와 <math><mi>P</mi><mi>V</mi></math>라는 matrix multiplication에 초점이 간다. 그러나 systems 관점에서는 intermediate tensor가 어디에 저장되는지, HBM boundary를 몇 번 건너는지, 저장되기 전에 소비될 수 있는지가 핵심이다.

online softmax update도 개념적으로 깔끔하다. 이는 heuristic normalization trick이 아니다. running maximum이 바뀔 때마다 이전 누적 항들을 rescale함으로써 올바른 numerator와 denominator를 보존한다. 그래서 FlashAttention은 approximate attention이 아니라 exact attention으로 이해될 수 있다.

위험은 수사적 과장이다. FlashAttention을 quadratic attention problem의 해결로 설명해서는 안 된다. 이 방법은 중요한 attention workload에서 memory traffic을 줄이고 GPU utilization을 개선한다. 이는 큰 systems contribution이지만, 새로운 attention model도 아니고, 더 좋은 language modeling을 증명하는 것도 아니며, 모든 환경에서의 속도 향상을 보장하는 것도 아니다.

## 결론

FlashAttention은 정확한 attention computation의 IO-aware reordering이다. attention semantics는 그대로 유지하고, full <math><mi>N</mi><mo>&times;</mo><mi>N</mi></math> intermediate matrix를 materialize하지 않으며, online softmax statistics를 사용해 빠른 on-chip memory를 통해 계산을 stream한다. 올바른 주장은 정밀해야 한다. HBM traffic을 줄이고 floating-point 차이를 제외하면 정확한 softmax attention을 계산한다는 것이지, quadratic interaction structure를 제거한다는 것이 아니다.

## 참고문헌

- Stanford CME295 Transformers & LLMs | Autumn 2025 | Lecture 4 - LLM Training. 제공된 자료에는 lecture title, course identifier, year 외의 세부 서지 정보가 포함되어 있지 않았다.
