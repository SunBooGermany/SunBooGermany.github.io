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

The compute units that perform matrix operations live inside the GPU chip. SRAM, the small memory placed close to those compute units on the chip, can exchange information with them much more efficiently and quickly. HBM, by contrast, is a much larger memory system outside the compute core region, and its effective data exchange is substantially slower, often discussed at roughly an order-of-magnitude disadvantage in this kind of memory-hierarchy argument.

The core idea of FlashAttention is therefore not to naively store all matrix information in HBM and repeatedly send it back to the compute units. Instead, it uses SRAM to make the calculation faster and more efficient. The more important point is that this is not an approximation: FlashAttention computes softmax attention exactly, up to floating-point differences, by maintaining the right online normalization statistics.

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

## Takeaway

FlashAttention is an IO-aware reordering of exact attention computation. It keeps the same attention semantics, avoids materializing the full <math><mi>N</mi><mo>&times;</mo><mi>N</mi></math> intermediate matrices, and uses online softmax statistics to stream the computation through fast on-chip memory. The right claim is precise: less HBM traffic and exact softmax attention up to floating-point differences, not a removal of the quadratic interaction structure.

## References

- Stanford CME295 Transformers & LLMs | Autumn 2025 | Lecture 4 - LLM Training.

<!-- ko -->

## 포지셔닝

FlashAttention은 정확한 Transformer attention을 IO 관점에서 다시 구현한 방법으로 이해하는 것이 가장 적절하다. 어텐션의 정의를 바꾸지 않으며, 모든 query와 모든 key 사이의 상호작용을 제거하지도 않는다. 기여는 더 구체적이다. 큰 attention score 행렬과 probability 행렬을 high-bandwidth memory에 쓰고 다시 읽지 않도록 계산 순서를 재구성한다.

이 구분은 long-context language model에서 중요하다. 표준 attention은 많은 dot product를 수행하기 때문에 비싸지만, 그것만이 문제가 아니다. naive implementation은 큰 중간 행렬을 GPU global memory를 통해 반복적으로 이동시킨다. sequence length가 커질수록 산술 연산보다 memory traffic이 실제 병목이 될 수 있다.

행렬 연산 계산을 수행하는 compute unit은 GPU chip 내부에 존재한다. 마찬가지로 GPU chip 내부에 직접 장착된 작은 memory인 SRAM은 compute unit과의 정보 교환이 훨씬 효율적이고 빠르다. 반면에 GPU chip 외부에 장착된 큰 memory인 HBM은 그보다 정보 교환 속도가 대략 한 order 정도 느린 memory 계층으로 이해할 수 있다.

FlashAttention의 핵심 아이디어는 모든 행렬 정보를 naive하게 HBM에 저장한 뒤 compute unit에게 반복적으로 전달하는 방식이 아니다. SRAM을 활용하여 필요한 tile과 online softmax 통계만 가까운 memory에 두고, 그 상태에서 빠르고 효율적으로 계산을 수행하게 하는 것이다. 더 중요한 점은 이것이 approximation이 아니라는 점이다. FlashAttention은 softmax를 근사하지 않고, 올바른 online normalization statistics를 유지함으로써 floating-point 차이를 제외하면 exact하게 softmax attention을 계산한다.

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

## 결론

FlashAttention은 정확한 attention computation의 IO-aware reordering이다. attention semantics는 그대로 유지하고, full <math><mi>N</mi><mo>&times;</mo><mi>N</mi></math> intermediate matrix를 materialize하지 않으며, online softmax statistics를 사용해 빠른 on-chip memory를 통해 계산을 stream한다. 올바른 주장은 정밀해야 한다. HBM traffic을 줄이고 floating-point 차이를 제외하면 정확한 softmax attention을 계산한다는 것이지, quadratic interaction structure를 제거한다는 것이 아니다.

## 참고문헌

- Stanford CME295 Transformers & LLMs | Autumn 2025 | Lecture 4 - LLM Training.
