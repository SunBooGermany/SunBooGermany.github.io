---
layout: post
title: "Do Transformers Need Three Projections?"
title_ko: "Transformer에 세 개의 projection이 필요할까?"
date: 2026-06-12
category: llm-probabilistic-approaches
category_label: "LLM & Probabilistic Approaches"
research_group: algorithmic_reviews
research_category: llm-probabilistic-approaches
research_category_label: "LLM & Probabilistic Approaches"
application_category: ""
application_category_label: ""
method_category: llm-probabilistic-approaches
method_category_label: "LLM & Probabilistic Approaches"
paper_title: "Do Transformers Need Three Projections? Systematic Study of QKV Variants"
authors: "Kayyam, A.; Gopal, A. M.; Lewis, M. A."
venue: "arXiv preprint"
year: "2026"
doi: ""
arxiv: "2606.04032"
source_url: "https://arxiv.org/abs/2606.04032"
tags:
  - "transformer"
  - "attention"
  - "kv-cache"
  - "projection-sharing"
  - "llm-inference"
excerpt: "A critical note on Q/K/V projection sharing in Transformer attention, where K=V preserves query-key directionality while cutting KV-cache memory in half."
excerpt_ko: "Transformer attention에서 Q/K/V projection을 모두 독립적으로 둘 필요가 있는지 검토하고, K=V sharing이 query-key 방향성을 유지하면서 KV cache를 절반으로 줄이는 압축 축임을 비판적으로 정리한다."
language: "en-ko"
has_korean_note: false
---

## The question is not whether attention can be made smaller

The useful question is more specific: which part of the Query, Key, Value split is actually doing work?

Standard self-attention takes an input sequence and forms three projected representations:

<math display="block" aria-label="Standard attention projections">
  <mi>Q</mi><mo>=</mo><mi>X</mi><msub><mi>W</mi><mi>q</mi></msub>
  <mo>,</mo>
  <mspace width="0.5em"></mspace>
  <mi>K</mi><mo>=</mo><mi>X</mi><msub><mi>W</mi><mi>k</mi></msub>
  <mo>,</mo>
  <mspace width="0.5em"></mspace>
  <mi>V</mi><mo>=</mo><mi>X</mi><msub><mi>W</mi><mi>v</mi></msub>
  <mo>.</mo>
</math>

The attention output is:

<math display="block" aria-label="Standard scaled dot product attention">
  <mi>Attn</mi><mo>(</mo><mi>X</mi><mo>)</mo>
  <mo>=</mo>
  <mi>Softmax</mi>
  <mo>(</mo>
  <mfrac>
    <mrow><mi>Q</mi><msup><mi>K</mi><mo>&top;</mo></msup></mrow>
    <msqrt><msub><mi>d</mi><mi>k</mi></msub></msqrt>
  </mfrac>
  <mo>)</mo>
  <mi>V</mi><mo>.</mo>
</math>

The usual story is that Q, K, and V play different roles. Query is the current token's retrieval request. Key is the address by which a past token can be found. Value is the payload that gets moved after attention weights are computed. The paper behind this note asks whether those roles really require three independent projection matrices.

The answer is not "all sharing is harmless." It is sharper than that. Sharing Q and K is costly for language modeling because it weakens directional lookup. Sharing K and V is much less damaging, and it directly cuts the KV cache.

The most interesting variant is therefore "Q-K=V."

This is not a new attention operator. It is a simple equality constraint on the projection axis. That simplicity is the point.

## Why KV cache is the right metric

For autoregressive LLM inference, the expensive object is not only the current attention computation. It is the stored history. Every generated token needs access to the keys and values of previous tokens across layers. As context windows grow, this KV cache becomes a central memory bottleneck.

If the batch size is <math><mi>B</mi></math>, the number of layers is <math><mi>L</mi></math>, the sequence length is <math><mi>T</mi></math>, the number of heads is <math><mi>H</mi></math>, the head dimension is <math><msub><mi>d</mi><mi>h</mi></msub></math>, and the dtype uses <math><mi>b</mi></math> bytes, the standard cache size is:

<math display="block" aria-label="Standard KV cache memory">
  <msub><mi>M</mi><mtext>QKV</mtext></msub>
  <mo>=</mo>
  <mi>B</mi><mi>L</mi><mi>T</mi>
  <mo>&middot;</mo>
  <mn>2</mn><mi>H</mi><msub><mi>d</mi><mi>h</mi></msub>
  <mo>&middot;</mo>
  <mi>b</mi><mo>.</mo>
</math>

The factor of two is there because both K and V are stored. If K and V are tied, only one representation has to be cached:

<math display="block" aria-label="K equals V cache memory">
  <msub><mi>M</mi><mtext>Q-K=V</mtext></msub>
  <mo>=</mo>
  <mi>B</mi><mi>L</mi><mi>T</mi>
  <mo>&middot;</mo>
  <mi>H</mi><msub><mi>d</mi><mi>h</mi></msub>
  <mo>&middot;</mo>
  <mi>b</mi><mo>.</mo>
</math>

So the cache reduction is exactly 50 percent. This part is arithmetic, not an empirical claim.

That matters because parameter savings alone would not be very exciting. Reducing three projection matrices to two saves some parameters and projection compute, but attention projections are only part of the full Transformer. The stronger deployment argument is that K=V attacks the stored inference state directly.

## Three sharing patterns

There are three natural variants.

First, Q=K-V ties query and key:

<math display="block" aria-label="Q equals K attention">
  <mi>Attn</mi><mo>(</mo><mi>X</mi><mo>)</mo>
  <mo>=</mo>
  <mi>Softmax</mi>
  <mo>(</mo><mi>&alpha;</mi><mi>K</mi><msup><mi>K</mi><mo>&top;</mo></msup><mo>)</mo>
  <mi>V</mi><mo>.</mo>
</math>

The problem is that the raw score matrix is symmetric before masking or positional corrections:

<math display="block" aria-label="Symmetric score from shared Q and K">
  <msub><mi>s</mi><mrow><mi>i</mi><mi>j</mi></mrow></msub>
  <mo>=</mo>
  <msubsup><mi>k</mi><mi>i</mi><mo>&top;</mo></msubsup><msub><mi>k</mi><mi>j</mi></msub>
  <mo>=</mo>
  <msubsup><mi>k</mi><mi>j</mi><mo>&top;</mo></msubsup><msub><mi>k</mi><mi>i</mi></msub>
  <mo>=</mo>
  <msub><mi>s</mi><mrow><mi>j</mi><mi>i</mi></mrow></msub>
  <mo>.</mo>
</math>

For non-causal vision or set-like tasks, this may not be fatal. For language modeling, it is a bad constraint. The current token asking for a past token is not the same relation as the past token asking for the current token. Q=K also does not reduce the KV cache because K and V still both exist.

Second, Q-K=V ties key and value:

<math display="block" aria-label="K equals V attention">
  <mi>Attn</mi><mo>(</mo><mi>X</mi><mo>)</mo>
  <mo>=</mo>
  <mi>Softmax</mi>
  <mo>(</mo><mi>&alpha;</mi><mi>Q</mi><msup><mi>K</mi><mo>&top;</mo></msup><mo>)</mo>
  <mi>K</mi><mo>.</mo>
</math>

This preserves the asymmetry of the attention score because Q and K remain separate:

<math display="block" aria-label="Asymmetric query key score">
  <msub><mi>s</mi><mrow><mi>i</mi><mi>j</mi></mrow></msub>
  <mo>=</mo>
  <msubsup><mi>q</mi><mi>i</mi><mo>&top;</mo></msubsup><msub><mi>k</mi><mi>j</mi></msub>
  <mo>,</mo>
  <mspace width="0.5em"></mspace>
  <msub><mi>s</mi><mrow><mi>j</mi><mi>i</mi></mrow></msub>
  <mo>=</mo>
  <msubsup><mi>q</mi><mi>j</mi><mo>&top;</mo></msubsup><msub><mi>k</mi><mi>i</mi></msub>
  <mo>.</mo>
</math>

In general these are not equal. The model still has one representation for "what I am looking for" and another representation for "how I can be found." It merely forces the searchable address and the delivered payload to share a representation.

Third, Q=K=V is the aggressive collapse. It saves parameters and halves the cache, but it combines both bottlenecks: symmetric score structure and no independent payload representation. Unsurprisingly, this is the variant that degrades most in language modeling.

## Why K=V is plausible, but not guaranteed

The best intuition is role separation. Q and K implement a directional lookup relation. K and V are both representations of past tokens. The address-payload distinction is real, but it may be less essential than the request-address distinction.

In retrieval language, Q is the current token's request, K is the past token's address, and V is the past token's payload.

Q=K says the request and the address must live in the same representation space. That is a strong constraint on directional attention. K=V says the address and the payload must share a representation. That is still a bottleneck, but it leaves directional lookup intact.

The paper's empirical analysis supports this story: in trained unconstrained QKV models, K and V projection matrices appear more similar to each other than Q is to either of them. This is useful evidence for redundancy. It is not a theorem.

The logical gap is important. Observing that trained matrices are similar does not prove that training under the equality constraint will find an equally good solution. The stronger claim would require a bound on the loss gap between unconstrained optimization and the constrained space where <math><msub><mi>W</mi><mi>k</mi></msub><mo>=</mo><msub><mi>W</mi><mi>v</mi></msub></math>. The paper does not provide that kind of guarantee.

So the correct interpretation is: "K=V gives a guaranteed memory reduction. Small perplexity loss is an empirical observation."

Both statements matter. Mixing them would overstate the result.

## Relationship to GQA and MQA

Q-K=V should not be read as a replacement for GQA or MQA. GQA and MQA reduce cache by sharing along the head axis. Projection sharing reduces cache along the projection axis. These are orthogonal design choices.

For a GQA variant with <math><mi>g</mi></math> KV groups, the cache is:

<math display="block" aria-label="GQA cache memory">
  <msub><mi>M</mi><mtext>GQA-g</mtext></msub>
  <mo>=</mo>
  <mi>B</mi><mi>L</mi><mi>T</mi>
  <mo>&middot;</mo>
  <mn>2</mn><mi>g</mi><msub><mi>d</mi><mi>h</mi></msub>
  <mo>&middot;</mo>
  <mi>b</mi><mo>.</mo>
</math>

Relative to standard multi-head attention, the reduction is <math><mn>1</mn><mo>-</mo><mi>g</mi><mo>/</mo><mi>H</mi></math>. If K=V is added on top of GQA, the cache becomes:

<math display="block" aria-label="Q-GQA cache memory">
  <msub><mi>M</mi><mtext>Q-GQA-g</mtext></msub>
  <mo>=</mo>
  <mi>B</mi><mi>L</mi><mi>T</mi>
  <mo>&middot;</mo>
  <mi>g</mi><msub><mi>d</mi><mi>h</mi></msub>
  <mo>&middot;</mo>
  <mi>b</mi><mo>,</mo>
</math>

with reduction <math><mn>1</mn><mo>-</mo><mi>g</mi><mo>/</mo><mo>(</mo><mn>2</mn><mi>H</mi><mo>)</mo></math>. For example, with <math><mi>H</mi><mo>=</mo><mn>16</mn></math> and <math><mi>g</mi><mo>=</mo><mn>4</mn></math>, Q-GQA reduces cache by 87.5 percent. With MQA, <math><mi>g</mi><mo>=</mo><mn>1</mn></math>, so the reduction is about 96.9 percent.

This is the practical reason the method is interesting even if standalone Q-K=V is not always better than GQA or MQA on perplexity-cache trade-off. Its claim is not "do not use GQA." Its claim is "there is another compression axis that can be stacked with GQA."

## What the experiments suggest

The reported language-modeling results are the main evidence. At roughly 300M parameters, Q-K=V gives a modest validation perplexity degradation while reducing cache by 50 percent. Q=K-V has similar or worse degradation but no cache saving. Q=K=V cuts cache but loses much more quality. That ranking is exactly what the role-separation argument predicts.

At a larger 1.2B scale, the relative ranking remains similar, and Q-K=V degradation becomes slightly smaller. That is suggestive. It does not settle the scaling question. A 1.2B model trained on 10B tokens is meaningful, but it is still far from proving the behavior at 7B, 13B, or 70B scale.

The downstream results are also encouraging but narrow. Maintaining average accuracy on benchmarks such as ARC, HellaSwag, PIQA, and WinoGrande is useful evidence that K=V does not immediately destroy general capability. It does not prove robustness for instruction following, coding, tool use, precise copying, or long-context retrieval. Those are exactly the places where the value representation may matter more.

The synthetic and vision tasks tell a different story: Q=K can work surprisingly well when directionality is less central, especially with positional mechanisms that break symmetry. That is a useful negative control. It shows that the harm of Q=K is not universal; it is task-structure dependent.

## Critical assessment

The strongest part of the paper is the framing. It does not introduce a complicated approximation to attention. It asks whether one accepted architectural degree of freedom is actually necessary. The resulting method is easy to implement, easy to combine with head sharing, and directly tied to a deployment bottleneck.

The weak part is theoretical support for quality retention. Cache reduction is exact. Parameter and projection-compute reductions are exact. The connection between full QKV collapse and recurrent-state updates in linear attention is algebraically interesting. But none of this proves that softmax LLMs with K=V should preserve perplexity, factual recall, or long-context behavior.

There is also a deployment question. If a serving stack already uses strong GQA or MQA, the incremental value of K=V depends on the acceptable quality loss at the target scale. A 3 to 5 percent perplexity degradation may be attractive for edge or on-device models. It may be unacceptable for a high-end model where quality is the product. The trade-off is not universal.

The most precise reading is therefore: "Q-K=V is not a better Transformer by default. It is a clean additional point on the memory-quality Pareto frontier."

That is enough to make the paper useful. In long-context serving, on-device LLMs, and high-throughput inference, a simple equality constraint that halves one part of the cache deserves attention, even if it remains an empirical design choice rather than a theorem-backed replacement for standard QKV.

## References

Kayyam, A., Gopal, A. M., & Lewis, M. A. (2026). Do Transformers Need Three Projections? Systematic Study of QKV Variants. arXiv preprint arXiv:2606.04032.

<!-- ko -->

## 질문은 attention을 작게 만들 수 있느냐가 아니다

표준 self-attention은 입력 sequence에서 세 개의 projection을 만든다.

<math display="block" aria-label="Standard attention projections">
  <mi>Q</mi><mo>=</mo><mi>X</mi><msub><mi>W</mi><mi>q</mi></msub>
  <mo>,</mo>
  <mspace width="0.5em"></mspace>
  <mi>K</mi><mo>=</mo><mi>X</mi><msub><mi>W</mi><mi>k</mi></msub>
  <mo>,</mo>
  <mspace width="0.5em"></mspace>
  <mi>V</mi><mo>=</mo><mi>X</mi><msub><mi>W</mi><mi>v</mi></msub>
  <mo>.</mo>
</math>

Attention output은 다음이다.

<math display="block" aria-label="Standard scaled dot product attention">
  <mi>Attn</mi><mo>(</mo><mi>X</mi><mo>)</mo>
  <mo>=</mo>
  <mi>Softmax</mi>
  <mo>(</mo>
  <mfrac>
    <mrow><mi>Q</mi><msup><mi>K</mi><mo>&top;</mo></msup></mrow>
    <msqrt><msub><mi>d</mi><mi>k</mi></msub></msqrt>
  </mfrac>
  <mo>)</mo>
  <mi>V</mi><mo>.</mo>
</math>

보통 Q, K, V는 서로 다른 역할을 한다고 설명된다. Query는 현재 token의 retrieval request다. Key는 과거 token이 검색될 수 있는 address다. Value는 attention weight가 계산된 뒤 실제로 전달되는 payload다. 이 글에서 다루는 논문은 이 세 역할이 정말 세 개의 독립 projection matrix를 요구하는지 묻는다.

답은 "공유해도 항상 괜찮다"가 아니다. 더 날카롭다. Q와 K를 공유하면 language modeling에서 비용이 크다. Directional lookup이 약해지기 때문이다. 반면 K와 V를 공유하는 것은 상대적으로 덜 해롭고, KV cache를 직접 줄인다.

따라서 가장 흥미로운 변형은 "Q-K=V"다.

이것은 새로운 attention operator가 아니다. Projection axis 위에 거는 단순한 equality constraint다. 오히려 그 단순함이 핵심이다.

## 왜 KV cache가 핵심 metric인가

Autoregressive LLM inference에서 비싼 것은 현재 token의 attention 계산만이 아니다. 저장된 history가 비싸다. 새 token을 생성할 때마다 모든 layer에서 과거 token의 key와 value에 접근해야 한다. Context window가 길어질수록 KV cache는 inference memory의 중심 병목이 된다.

Batch size가 <math><mi>B</mi></math>, layer 수가 <math><mi>L</mi></math>, sequence length가 <math><mi>T</mi></math>, head 수가 <math><mi>H</mi></math>, head dimension이 <math><msub><mi>d</mi><mi>h</mi></msub></math>, dtype byte 수가 <math><mi>b</mi></math>라면 표준 cache 크기는 다음이다.

<math display="block" aria-label="Standard KV cache memory">
  <msub><mi>M</mi><mtext>QKV</mtext></msub>
  <mo>=</mo>
  <mi>B</mi><mi>L</mi><mi>T</mi>
  <mo>&middot;</mo>
  <mn>2</mn><mi>H</mi><msub><mi>d</mi><mi>h</mi></msub>
  <mo>&middot;</mo>
  <mi>b</mi><mo>.</mo>
</math>

2라는 factor는 K와 V를 모두 저장하기 때문에 생긴다. K와 V를 묶으면 하나만 저장하면 된다.

<math display="block" aria-label="K equals V cache memory">
  <msub><mi>M</mi><mtext>Q-K=V</mtext></msub>
  <mo>=</mo>
  <mi>B</mi><mi>L</mi><mi>T</mi>
  <mo>&middot;</mo>
  <mi>H</mi><msub><mi>d</mi><mi>h</mi></msub>
  <mo>&middot;</mo>
  <mi>b</mi><mo>.</mo>
</math>

따라서 cache reduction은 정확히 50 percent다. 이 부분은 empirical claim이 아니라 산술이다.

이 점이 중요하다. Parameter saving만으로는 그렇게 흥미롭지 않다. 세 projection matrix를 두 개로 줄이면 parameter와 projection compute가 줄지만, attention projection은 전체 Transformer의 일부일 뿐이다. 더 강한 deployment argument는 K=V가 저장되는 inference state 자체를 직접 줄인다는 데 있다.

## 세 가지 sharing pattern

자연스러운 변형은 세 가지다.

첫째, Q=K-V는 query와 key를 묶는다.

<math display="block" aria-label="Q equals K attention">
  <mi>Attn</mi><mo>(</mo><mi>X</mi><mo>)</mo>
  <mo>=</mo>
  <mi>Softmax</mi>
  <mo>(</mo><mi>&alpha;</mi><mi>K</mi><msup><mi>K</mi><mo>&top;</mo></msup><mo>)</mo>
  <mi>V</mi><mo>.</mo>
</math>

문제는 raw score matrix가 mask나 positional correction 이전에 symmetric하다는 것이다.

<math display="block" aria-label="Symmetric score from shared Q and K">
  <msub><mi>s</mi><mrow><mi>i</mi><mi>j</mi></mrow></msub>
  <mo>=</mo>
  <msubsup><mi>k</mi><mi>i</mi><mo>&top;</mo></msubsup><msub><mi>k</mi><mi>j</mi></msub>
  <mo>=</mo>
  <msubsup><mi>k</mi><mi>j</mi><mo>&top;</mo></msubsup><msub><mi>k</mi><mi>i</mi></msub>
  <mo>=</mo>
  <msub><mi>s</mi><mrow><mi>j</mi><mi>i</mi></mrow></msub>
  <mo>.</mo>
</math>

Non-causal vision이나 set-like task에서는 치명적이지 않을 수 있다. 하지만 language modeling에서는 나쁜 제약이다. 현재 token이 과거 token을 찾는 관계와 과거 token이 현재 token을 찾는 관계는 같지 않다. 또한 Q=K는 KV cache를 줄이지 못한다. K와 V가 여전히 둘 다 존재하기 때문이다.

둘째, Q-K=V는 key와 value를 묶는다.

<math display="block" aria-label="K equals V attention">
  <mi>Attn</mi><mo>(</mo><mi>X</mi><mo>)</mo>
  <mo>=</mo>
  <mi>Softmax</mi>
  <mo>(</mo><mi>&alpha;</mi><mi>Q</mi><msup><mi>K</mi><mo>&top;</mo></msup><mo>)</mo>
  <mi>K</mi><mo>.</mo>
</math>

이 변형은 Q와 K를 분리하므로 attention score의 asymmetry를 보존한다.

<math display="block" aria-label="Asymmetric query key score">
  <msub><mi>s</mi><mrow><mi>i</mi><mi>j</mi></mrow></msub>
  <mo>=</mo>
  <msubsup><mi>q</mi><mi>i</mi><mo>&top;</mo></msubsup><msub><mi>k</mi><mi>j</mi></msub>
  <mo>,</mo>
  <mspace width="0.5em"></mspace>
  <msub><mi>s</mi><mrow><mi>j</mi><mi>i</mi></mrow></msub>
  <mo>=</mo>
  <msubsup><mi>q</mi><mi>j</mi><mo>&top;</mo></msubsup><msub><mi>k</mi><mi>i</mi></msub>
  <mo>.</mo>
</math>

일반적으로 이 둘은 같지 않다. 모델은 여전히 "내가 무엇을 찾고 있는가"와 "내가 어떻게 검색될 수 있는가"를 분리해서 갖는다. 다만 searchable address와 delivered payload를 같은 representation으로 강제할 뿐이다.

셋째, Q=K=V는 가장 강한 collapse다. Parameter를 줄이고 cache도 절반으로 줄이지만, 두 병목을 동시에 갖는다. Score structure가 symmetric해지고, payload representation도 독립적으로 가질 수 없다. Language modeling에서 이 변형의 손실이 가장 큰 것은 놀랍지 않다.

## K=V가 그럴듯한 이유와 보장되지 않는 이유

가장 좋은 직관은 role separation이다. Q와 K는 directional lookup relation을 구현한다. K와 V는 모두 과거 token의 representation이다. Address와 payload의 구분은 실제로 의미가 있지만, request와 address의 구분만큼 필수적이지 않을 수 있다.

Retrieval language로 쓰면, Q는 현재 token의 request, K는 과거 token의 address, V는 과거 token의 payload다.

Q=K는 request와 address가 같은 representation space에 살아야 한다고 말한다. 이것은 directional attention에 강한 제약이다. K=V는 address와 payload가 같은 representation을 공유해야 한다고 말한다. 이것도 bottleneck이지만, directional lookup은 보존된다.

논문의 empirical analysis는 이 해석을 뒷받침한다. Unconstrained QKV model을 학습한 뒤 보면, K와 V projection matrix가 Q와 K 또는 Q와 V보다 더 비슷하게 나타난다. 이것은 redundancy에 대한 좋은 근거다. 하지만 theorem은 아니다.

논리적 간격이 중요하다. 학습된 matrix들이 비슷하다는 관찰은 equality constraint를 걸고 처음부터 학습해도 비슷한 해에 도달한다는 것을 증명하지 않는다. 더 강한 주장을 하려면 unconstrained optimization과 <math><msub><mi>W</mi><mi>k</mi></msub><mo>=</mo><msub><mi>W</mi><mi>v</mi></msub></math> constrained space 사이의 loss gap을 bound해야 한다. 이 논문은 그런 보장을 제공하지 않는다.

그래서 정확한 해석은 다음이다. "K=V는 보장된 memory reduction을 준다. 작은 perplexity loss는 empirical observation이다."

두 문장 모두 중요하다. 둘을 섞으면 결과를 과장하게 된다.

## GQA, MQA와의 관계

Q-K=V는 GQA나 MQA의 대체물로 읽으면 안 된다. GQA와 MQA는 head axis를 공유해서 cache를 줄인다. Projection sharing은 projection axis를 줄인다. 두 선택은 orthogonal하다.

<math><mi>g</mi></math>개의 KV group을 쓰는 GQA variant의 cache는 다음이다.

<math display="block" aria-label="GQA cache memory">
  <msub><mi>M</mi><mtext>GQA-g</mtext></msub>
  <mo>=</mo>
  <mi>B</mi><mi>L</mi><mi>T</mi>
  <mo>&middot;</mo>
  <mn>2</mn><mi>g</mi><msub><mi>d</mi><mi>h</mi></msub>
  <mo>&middot;</mo>
  <mi>b</mi><mo>.</mo>
</math>

표준 multi-head attention 대비 reduction은 <math><mn>1</mn><mo>-</mo><mi>g</mi><mo>/</mo><mi>H</mi></math>다. 여기에 K=V를 추가하면 cache는 다음이 된다.

<math display="block" aria-label="Q-GQA cache memory">
  <msub><mi>M</mi><mtext>Q-GQA-g</mtext></msub>
  <mo>=</mo>
  <mi>B</mi><mi>L</mi><mi>T</mi>
  <mo>&middot;</mo>
  <mi>g</mi><msub><mi>d</mi><mi>h</mi></msub>
  <mo>&middot;</mo>
  <mi>b</mi><mo>,</mo>
</math>

reduction은 <math><mn>1</mn><mo>-</mo><mi>g</mi><mo>/</mo><mo>(</mo><mn>2</mn><mi>H</mi><mo>)</mo></math>다. 예를 들어 <math><mi>H</mi><mo>=</mo><mn>16</mn></math>, <math><mi>g</mi><mo>=</mo><mn>4</mn></math>이면 Q-GQA의 cache reduction은 87.5 percent다. MQA에서는 <math><mi>g</mi><mo>=</mo><mn>1</mn></math>이므로 reduction은 약 96.9 percent다.

이것이 standalone Q-K=V가 GQA나 MQA보다 항상 좋은 perplexity-cache trade-off를 보이지 않더라도 흥미로운 실용적 이유다. 주장은 "GQA를 쓰지 말라"가 아니다. 주장은 "GQA 위에 얹을 수 있는 다른 compression axis가 있다"에 가깝다.

## 실험이 시사하는 것

가장 중요한 근거는 language-modeling 결과다. 대략 300M parameter scale에서 Q-K=V는 validation perplexity를 조금 악화시키지만 cache를 50 percent 줄인다. Q=K-V는 비슷하거나 더 큰 손실을 보이면서 cache saving은 없다. Q=K=V는 cache는 줄이지만 품질 손실이 훨씬 크다. 이 ranking은 role-separation 직관과 잘 맞는다.

더 큰 1.2B scale에서도 상대적 ranking은 비슷하고, Q-K=V의 degradation은 약간 작아진다. 흥미로운 신호다. 하지만 scaling question을 끝내지는 않는다. 1.2B model과 10B token은 의미 있는 scale이지만, 7B, 13B, 70B에서도 같은 현상이 유지된다고 증명하기에는 부족하다.

Downstream 결과도 긍정적이지만 좁다. ARC, HellaSwag, PIQA, WinoGrande 같은 benchmark에서 평균 accuracy가 유지된다는 것은 K=V가 일반 능력을 즉시 무너뜨리지 않는다는 근거다. 그러나 instruction following, coding, tool use, precise copying, long-context retrieval까지 보장하지는 않는다. 오히려 그런 task들이 value representation의 독립성이 더 중요해질 수 있는 지점이다.

Synthetic과 vision task는 다른 이야기를 보여준다. Directionality가 덜 핵심인 경우 Q=K도 꽤 잘 작동할 수 있고, positional mechanism을 붙이면 symmetry 문제를 일부 완화할 수 있다. 이것은 유용한 negative control이다. Q=K의 손실이 보편적이지 않고 task structure에 의존한다는 것을 보여주기 때문이다.

## 비판적 평가

논문의 가장 강한 부분은 framing이다. 복잡한 attention approximation을 만들지 않는다. 너무 당연하게 받아들여졌던 architectural degree of freedom이 실제로 필요한지 묻는다. 결과적으로 방법은 구현하기 쉽고, head sharing과 결합하기 쉽고, deployment bottleneck과 직접 연결된다.

약한 부분은 quality retention에 대한 이론적 근거다. Cache reduction은 정확하다. Parameter와 projection-compute reduction도 정확하다. Linear attention에서 full QKV collapse가 recurrent-state update와 연결된다는 관찰도 algebraically 흥미롭다. 하지만 이런 결과들이 softmax LLM에서 K=V가 perplexity, factual recall, long-context behavior를 보존해야 한다는 증명은 아니다.

Deployment 관점의 질문도 남아 있다. Serving stack이 이미 강한 GQA나 MQA를 쓴다면, K=V의 incremental value는 target scale에서 허용 가능한 quality loss에 달려 있다. 3 to 5 percent 수준의 perplexity degradation은 edge나 on-device model에서는 매력적일 수 있다. 반대로 품질이 제품인 high-end model에서는 받아들이기 어려울 수 있다. 이 trade-off는 보편적이지 않다.

가장 정확한 독해는 다음이다. "Q-K=V는 기본적으로 더 좋은 Transformer가 아니다. Memory-quality Pareto frontier 위에 추가되는 깨끗한 한 점이다."

이 정도만으로도 논문은 유용하다. Long-context serving, on-device LLM, high-throughput inference에서는 cache의 한 부분을 절반으로 줄이는 단순한 equality constraint가 검토할 가치가 있다. 다만 그것은 theorem-backed replacement가 아니라 empirical design choice로 남아 있다.

## 참고문헌

Kayyam, A., Gopal, A. M., & Lewis, M. A. (2026). Do Transformers Need Three Projections? Systematic Study of QKV Variants. arXiv preprint arXiv:2606.04032.
