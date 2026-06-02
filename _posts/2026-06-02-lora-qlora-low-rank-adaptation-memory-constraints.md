---
layout: post
title: "LoRA and QLoRA: Low-Rank Adaptation Under Memory Constraints"
title_ko: "LoRA와 QLoRA: 메모리 제약 아래의 저랭크 적응"
date: 2026-06-02
category: llm-probabilistic-approaches
category_label: "LLM & Probabilistic Approaches"
research_group: algorithmic_reviews
research_category: llm-probabilistic-approaches
research_category_label: "LLM & Probabilistic Approaches"
application_category: ""
application_category_label: ""
method_category: llm-probabilistic-approaches
method_category_label: "LLM & Probabilistic Approaches"
paper_title: ""
authors: ""
venue: ""
year: ""
doi: ""
arxiv: ""
source_url: ""
tags:
  - lora
  - qlora
  - parameter-efficient-fine-tuning
  - quantization
  - llm
excerpt: "LoRA reduces fine-tuning cost by learning low-rank task-specific corrections on top of frozen pretrained weights, while QLoRA adds 4-bit quantization so larger base models can be adapted under tighter GPU memory constraints."
excerpt_ko: "LoRA는 고정된 pretrained weight 위에 저랭크 task-specific correction만 학습해 fine-tuning 비용을 줄이고, QLoRA는 여기에 4-bit quantization을 결합해 더 큰 base model을 제한된 GPU memory에서 적응시킬 수 있게 한다."
language: "en-ko"
has_korean_note: false
---

## Positioning

LoRA and QLoRA are best understood as adaptation methods for large pretrained models, not as new model architectures. Their shared premise is simple: when a pretrained language model already contains broad linguistic, representational, and reasoning capability, many downstream tasks may not require updating every weight in the model. Instead, the task can often be represented as a relatively small correction to the frozen base model.

LoRA makes this correction parameter-efficient by learning low-rank updates. QLoRA keeps the same adapter idea but makes the frozen base model memory-efficient by storing it in 4-bit quantized form during fine-tuning. The distinction is important: LoRA mainly reduces the number of trainable parameters, while QLoRA reduces both trainable parameters and the memory footprint of the base model.

This note treats LoRA and QLoRA as practical engineering tools for LLM adaptation. They are powerful, but their claims should stay precise: they can make adaptation cheaper and often surprisingly effective; they do not guarantee reliable new knowledge injection, remove the need for evaluation, or make a weak base model fundamentally capable of tasks it could not support.

## Problem setting

Full fine-tuning of a large language model is expensive for three linked reasons.

First, all model weights must be updated. For a 7B, 13B, or 65B parameter model, this means storing weights, gradients, and optimizer states. With optimizers such as Adam, optimizer states can dominate memory use because they store additional moment estimates for every trainable parameter.

Second, full fine-tuning is storage-inefficient when many tasks are needed. A separate fully fine-tuned copy for task A, task B, and task C means storing multiple versions of the entire model.

Third, small or narrow datasets can push full fine-tuning toward overfitting or catastrophic forgetting. The model may lose part of its pretrained general capability while chasing a limited downstream distribution.

The adaptation problem is therefore:

```text
Given a pretrained model,
adapt it to a task or style
without updating and storing a full copy of all model parameters.
```

LoRA answers this by freezing the pretrained model and learning only a low-rank task correction. QLoRA adds the additional constraint that the frozen pretrained model should fit into much smaller GPU memory.

## Prior Research Gap

The practical gap is not that pretrained models cannot be adapted. They can be adapted by full fine-tuning. The gap is that full fine-tuning becomes increasingly impractical as models grow.

A useful adaptation method should satisfy several constraints at once. It should keep most pretrained capability intact, require far fewer trainable parameters, allow multiple task-specific variants to be stored compactly, and remain feasible on limited GPU memory. LoRA focuses on the first three constraints. QLoRA pushes the fourth constraint further by combining adapter training with quantized storage of the base model.

This gap is especially relevant for instruction tuning, domain adaptation, preference tuning, and style adaptation, where the desired change is often a behavioral shift rather than learning a new language model from scratch.

## Core Idea

Consider a linear layer in a Transformer:

<math display="block" aria-label="Linear layer output">
  <mi>h</mi>
  <mo>=</mo>
  <mi>W</mi>
  <mi>x</mi><mo>.</mo>
</math>

Full fine-tuning changes the whole weight matrix:

<math display="block" aria-label="Full fine tuning weight update">
  <mi>W</mi>
  <mo>&larr;</mo>
  <mi>W</mi>
  <mo>+</mo>
  <mi>&Delta;</mi>
  <mi>W</mi><mo>.</mo>
</math>

LoRA does not learn a dense <math><mi>&Delta;</mi><mi>W</mi></math> directly. It represents the update as a product of two much smaller matrices:

<math display="block" aria-label="LoRA low rank update">
  <mi>&Delta;</mi>
  <mi>W</mi>
  <mo>=</mo>
  <mi>B</mi>
  <mi>A</mi><mo>,</mo>
</math>

where the rank <math><mi>r</mi></math> is much smaller than the input and output dimensions. The forward pass becomes:

<math display="block" aria-label="LoRA forward pass">
  <mi>h</mi>
  <mo>=</mo>
  <mi>W</mi>
  <mi>x</mi>
  <mo>+</mo>
  <mfrac>
    <mi>&alpha;</mi>
    <mi>r</mi>
  </mfrac>
  <mi>B</mi>
  <mi>A</mi>
  <mi>x</mi><mo>.</mo>
</math>

The pretrained weight <math><mi>W</mi></math> is frozen. Only <math><mi>A</mi></math> and <math><mi>B</mi></math> are trained. In practical Transformer implementations, LoRA adapters are often attached to attention projection matrices such as <math><msub><mi>W</mi><mi>Q</mi></msub></math>, <math><msub><mi>W</mi><mi>K</mi></msub></math>, <math><msub><mi>W</mi><mi>V</mi></msub></math>, and <math><msub><mi>W</mi><mi>O</mi></msub></math>, and sometimes to MLP projection layers as well.

QLoRA keeps this adapter structure but stores the frozen base model in quantized form:

<math display="block" aria-label="QLoRA quantized base and LoRA adapter">
  <mi>h</mi>
  <mo>=</mo>
  <msub><mi>Q</mi><mn>4</mn></msub>
  <mo>(</mo><mi>W</mi><mo>)</mo>
  <mi>x</mi>
  <mo>+</mo>
  <mfrac>
    <mi>&alpha;</mi>
    <mi>r</mi>
  </mfrac>
  <mi>B</mi>
  <mi>A</mi>
  <mi>x</mi><mo>.</mo>
</math>

Here <math><msub><mi>Q</mi><mn>4</mn></msub><mo>(</mo><mi>W</mi><mo>)</mo></math> denotes a 4-bit quantized representation of the base weights. During computation, the quantized weights are dequantized as needed, but the base weights remain frozen. The trainable learning signal still flows through the LoRA adapter.

## Mathematical Structure

Suppose <math><mi>W</mi><mo>&in;</mo><msup><mi>R</mi><mrow><msub><mi>d</mi><mtext>out</mtext></msub><mo>&times;</mo><msub><mi>d</mi><mtext>in</mtext></msub></mrow></msup></math>. LoRA chooses:

<math display="block" aria-label="LoRA factor dimensions">
  <mi>A</mi>
  <mo>&in;</mo>
  <msup><mi>R</mi><mrow><mi>r</mi><mo>&times;</mo><msub><mi>d</mi><mtext>in</mtext></msub></mrow></msup>
  <mo>,</mo>
  <mspace width="0.8em"></mspace>
  <mi>B</mi>
  <mo>&in;</mo>
  <msup><mi>R</mi><mrow><msub><mi>d</mi><mtext>out</mtext></msub><mo>&times;</mo><mi>r</mi></mrow></msup>
  <mo>,</mo>
  <mspace width="0.8em"></mspace>
  <mi>r</mi>
  <mo>&ll;</mo>
  <mi>min</mi>
  <mo>(</mo><msub><mi>d</mi><mtext>in</mtext></msub><mo>,</mo><msub><mi>d</mi><mtext>out</mtext></msub><mo>)</mo><mo>.</mo>
</math>

The dense update would contain <math><msub><mi>d</mi><mtext>out</mtext></msub><msub><mi>d</mi><mtext>in</mtext></msub></math> parameters. The LoRA update contains only:

<math display="block" aria-label="Number of LoRA trainable parameters">
  <mi>r</mi>
  <mo>(</mo>
  <msub><mi>d</mi><mtext>in</mtext></msub>
  <mo>+</mo>
  <msub><mi>d</mi><mtext>out</mtext></msub>
  <mo>)</mo>
</math>

parameters for that layer. When <math><mi>r</mi></math> is small, this is a large reduction.

The low-rank constraint is also a regularizer:

<math display="block" aria-label="LoRA rank constraint">
  <mi>&Delta;</mi>
  <mi>W</mi>
  <mo>&in;</mo>
  <mo>{</mo>
  <mi>B</mi>
  <mi>A</mi>
  <mo>:</mo>
  <mi>rank</mi>
  <mo>(</mo>
  <mi>&Delta;</mi>
  <mi>W</mi>
  <mo>)</mo>
  <mo>&le;</mo>
  <mi>r</mi>
  <mo>}</mo><mo>.</mo>
</math>

After training, the adapter can often be merged into the base weight for inference:

<math display="block" aria-label="Merged LoRA weight">
  <msub><mi>W</mi><mtext>merged</mtext></msub>
  <mo>=</mo>
  <mi>W</mi>
  <mo>+</mo>
  <mfrac>
    <mi>&alpha;</mi>
    <mi>r</mi>
  </mfrac>
  <mi>B</mi>
  <mi>A</mi><mo>.</mo>
</math>

QLoRA adds a quantization layer around the frozen base model. Its common ingredients include 4-bit NormalFloat quantization, double quantization of quantization constants, paged optimizers to reduce memory spikes, and higher-precision training of the LoRA adapter. The key design choice is asymmetric: the base model is compressed, but the task-specific adapter remains trainable with enough precision to carry the adaptation signal.

## Why It Can Work

The intuitive reason LoRA can work is that downstream adaptation often does not need to rebuild the model. The pretrained model already contains rich representations and many useful behaviors. Fine-tuning then becomes closer to steering those behaviors than learning the entire function again.

For example, instruction tuning, domain adaptation, and style adaptation often modify latent behavioral directions: follow instructions more reliably, answer in a domain-specific format, use a concise academic tone, or produce code-like outputs. Such changes may be expressible through a small number of structured directions in weight space, especially when applied to attention and MLP projections.

This does not prove that every useful task update is low-rank. Rather, LoRA imposes a bottleneck that is empirically useful in many settings and especially attractive when data are limited. The bottleneck can reduce overfitting and catastrophic forgetting by preventing the update from moving too freely.

QLoRA relies on an additional robustness assumption. Quantization introduces error into the base weights:

<math display="block" aria-label="Quantization error model">
  <msub><mi>Q</mi><mn>4</mn></msub>
  <mo>(</mo><mi>W</mi><mo>)</mo>
  <mo>&approx;</mo>
  <mi>W</mi>
  <mo>+</mo>
  <msub><mi>&epsilon;</mi><mi>q</mi></msub><mo>.</mo>
</math>

QLoRA works when useful pretrained behavior is sufficiently robust to this quantization error and when the LoRA adapter can compensate for the task-relevant residual differences. This is a practical empirical claim, not a universal guarantee.

## Assumptions and Limitations

LoRA assumes that a useful task update can be captured by a low-rank correction. This is plausible for many adaptation tasks, but it is not guaranteed. If the rank is too small, the adapter underfits. If the rank is too large, the memory advantage and regularization effect weaken.

QLoRA assumes that the base model can tolerate 4-bit quantization during adaptation. This can be less reliable for numerically sensitive tasks, smaller models, specialized domains, or long-context reasoning settings where small perturbations may matter.

Neither method is a reliable mechanism for inserting fresh factual knowledge. Fine-tuning can bias a model toward domain patterns, but if the goal is accurate access to new or changing facts, retrieval-augmented generation, tool use, or database grounding is often more appropriate.

Both methods are also bounded by the base model. A small or weak model does not become a strong reasoning model merely because a LoRA adapter is attached. LoRA adjusts existing capability more than it creates fundamentally new capability.

Finally, full fine-tuning can still be better when enough data, compute, and operational justification exist. LoRA and QLoRA trade update freedom for efficiency, modularity, and stability.

## Critical Assessment

LoRA is valuable because it turns fine-tuning into a modular correction problem. One base model can support multiple compact adapters for different tasks: medical response style, legal document analysis, code generation, bilingual technical writing, or process systems engineering literature assistance. This is operationally attractive because task-specific behavior can be swapped without storing a complete model copy for every task.

QLoRA is valuable because it moves the memory bottleneck. LoRA alone still requires the base model to reside in GPU memory at relatively high precision. QLoRA compresses that frozen base model, making larger-model adaptation feasible under tighter hardware budgets.

The main risk is over-interpreting the methods. A successful LoRA or QLoRA run does not mean the adaptation has become reliable, truthful, safe, or robust. Those properties must be measured directly. The right interpretation is narrower and stronger: LoRA and QLoRA are efficient ways to test and deploy task-specific changes to pretrained models while preserving a clear separation between the frozen base and the learned correction.

## References

- Edward J. Hu, Yelong Shen, Phillip Wallis, Zeyuan Allen-Zhu, Yuanzhi Li, Shean Wang, Lu Wang, and Weizhu Chen. "LoRA: Low-Rank Adaptation of Large Language Models." arXiv:2106.09685, 2021.
- Tim Dettmers, Artidoro Pagnoni, Ari Holtzman, and Luke Zettlemoyer. "QLoRA: Efficient Finetuning of Quantized LLMs." arXiv:2305.14314, 2023.
- Supplied Korean notes on LoRA and QLoRA.

<!-- ko -->

## 포지셔닝

LoRA와 QLoRA는 새로운 모델 아키텍처라기보다, 거대한 pretrained model을 현실적인 비용으로 특정 task에 적응시키기 위한 방법으로 이해하는 것이 적절하다. 두 방법의 공통 전제는 단순하다. pretrained language model이 이미 언어, representation, reasoning capability를 상당히 갖고 있다면, downstream task마다 모든 weight를 다시 학습할 필요는 없을 수 있다. 많은 경우 필요한 것은 frozen base model 위에 얹는 작은 task-specific correction이다.

LoRA는 이 correction을 low-rank update로 학습해 trainable parameter 수를 줄인다. QLoRA는 같은 adapter 아이디어를 유지하되, fine-tuning 중 frozen base model을 4-bit quantized form으로 저장해 memory footprint를 더 줄인다. 따라서 둘의 차이는 명확하다. LoRA는 주로 학습되는 parameter 수를 줄이고, QLoRA는 학습되는 parameter 수와 base model의 GPU memory 사용량을 함께 줄인다.

이 글에서는 LoRA와 QLoRA를 LLM adaptation을 위한 실용적인 engineering tool로 본다. 두 방법은 강력하지만, 주장은 정확해야 한다. adaptation을 더 저렴하고 자주 효과적으로 만들 수는 있지만, 새로운 factual knowledge의 안정적 주입을 보장하지도 않고, 평가의 필요성을 없애지도 않으며, 약한 base model을 근본적으로 강한 reasoning model로 바꾸지도 않는다.

## 문제 설정

거대 language model의 full fine-tuning은 세 가지 이유로 비싸다.

첫째, 모든 model weight를 업데이트해야 한다. 7B, 13B, 65B parameter model에서는 weight뿐 아니라 gradient와 optimizer state도 저장해야 한다. Adam 같은 optimizer를 쓰면 trainable parameter마다 추가 moment estimate가 필요하므로 optimizer state가 memory 사용량의 큰 부분을 차지할 수 있다.

둘째, task가 많아질수록 저장 비용이 커진다. task A, task B, task C마다 full fine-tuned model을 따로 저장하면 model 전체 copy가 여러 개 필요하다.

셋째, 작거나 좁은 dataset에서는 full fine-tuning이 overfitting이나 catastrophic forgetting을 유발하기 쉽다. 제한된 downstream distribution에 맞추는 과정에서 pretrained model이 가진 general capability 일부를 손상시킬 수 있다.

따라서 adaptation 문제는 다음처럼 요약할 수 있다.

```text
pretrained model이 주어졌을 때,
모든 parameter를 업데이트하고 저장하지 않으면서
특정 task나 style에 맞게 적응시키는 방법이 필요하다.
```

LoRA는 pretrained model을 freeze하고 low-rank task correction만 학습함으로써 이 문제에 답한다. QLoRA는 여기에 frozen pretrained model 자체도 훨씬 작은 GPU memory에 들어가야 한다는 제약을 추가로 다룬다.

## 선행 연구 공백

핵심 공백은 pretrained model을 adaptation할 수 없다는 것이 아니다. full fine-tuning을 하면 adaptation은 가능하다. 문제는 model size가 커질수록 full fine-tuning이 점점 비현실적이 된다는 데 있다.

유용한 adaptation method는 여러 제약을 동시에 만족해야 한다. pretrained capability를 대부분 보존해야 하고, 학습되는 parameter 수가 훨씬 적어야 하며, 여러 task-specific variant를 compact하게 저장할 수 있어야 하고, 제한된 GPU memory에서도 가능해야 한다. LoRA는 앞의 세 제약에 초점을 둔다. QLoRA는 adapter training과 base model quantization을 결합해 네 번째 제약을 더 강하게 다룬다.

이 공백은 instruction tuning, domain adaptation, preference tuning, style adaptation에서 특히 중요하다. 이런 setting에서는 완전히 새로운 language model을 학습한다기보다, 이미 존재하는 model behavior를 특정 방향으로 조정하는 경우가 많기 때문이다.

## 핵심 아이디어

Transformer의 한 linear layer를 생각하자.

<math display="block" aria-label="Linear layer output">
  <mi>h</mi>
  <mo>=</mo>
  <mi>W</mi>
  <mi>x</mi><mo>.</mo>
</math>

Full fine-tuning은 전체 weight matrix를 바꾼다.

<math display="block" aria-label="Full fine tuning weight update">
  <mi>W</mi>
  <mo>&larr;</mo>
  <mi>W</mi>
  <mo>+</mo>
  <mi>&Delta;</mi>
  <mi>W</mi><mo>.</mo>
</math>

LoRA는 dense한 <math><mi>&Delta;</mi><mi>W</mi></math>를 직접 학습하지 않는다. 대신 update를 두 개의 훨씬 작은 matrix 곱으로 표현한다.

<math display="block" aria-label="LoRA low rank update">
  <mi>&Delta;</mi>
  <mi>W</mi>
  <mo>=</mo>
  <mi>B</mi>
  <mi>A</mi><mo>.</mo>
</math>

여기서 rank <math><mi>r</mi></math>은 input dimension과 output dimension보다 훨씬 작다. Forward pass는 다음과 같이 바뀐다.

<math display="block" aria-label="LoRA forward pass">
  <mi>h</mi>
  <mo>=</mo>
  <mi>W</mi>
  <mi>x</mi>
  <mo>+</mo>
  <mfrac>
    <mi>&alpha;</mi>
    <mi>r</mi>
  </mfrac>
  <mi>B</mi>
  <mi>A</mi>
  <mi>x</mi><mo>.</mo>
</math>

Pretrained weight <math><mi>W</mi></math>는 freeze된다. 학습되는 것은 <math><mi>A</mi></math>와 <math><mi>B</mi></math>뿐이다. 실제 Transformer에서는 LoRA adapter가 <math><msub><mi>W</mi><mi>Q</mi></msub></math>, <math><msub><mi>W</mi><mi>K</mi></msub></math>, <math><msub><mi>W</mi><mi>V</mi></msub></math>, <math><msub><mi>W</mi><mi>O</mi></msub></math> 같은 attention projection matrix에 붙는 경우가 많고, task에 따라 MLP projection layer에도 붙는다.

QLoRA는 이 adapter 구조를 유지하면서 frozen base model을 quantized form으로 저장한다.

<math display="block" aria-label="QLoRA quantized base and LoRA adapter">
  <mi>h</mi>
  <mo>=</mo>
  <msub><mi>Q</mi><mn>4</mn></msub>
  <mo>(</mo><mi>W</mi><mo>)</mo>
  <mi>x</mi>
  <mo>+</mo>
  <mfrac>
    <mi>&alpha;</mi>
    <mi>r</mi>
  </mfrac>
  <mi>B</mi>
  <mi>A</mi>
  <mi>x</mi><mo>.</mo>
</math>

여기서 <math><msub><mi>Q</mi><mn>4</mn></msub><mo>(</mo><mi>W</mi><mo>)</mo></math>는 base weight의 4-bit quantized representation을 뜻한다. 계산할 때는 필요한 순간 dequantize해서 쓰지만, base weight 자체는 freeze되어 있다. Task-specific learning signal은 여전히 LoRA adapter를 통해 흐른다.

## 수학적 구조

<math><mi>W</mi><mo>&in;</mo><msup><mi>R</mi><mrow><msub><mi>d</mi><mtext>out</mtext></msub><mo>&times;</mo><msub><mi>d</mi><mtext>in</mtext></msub></mrow></msup></math>라고 하자. LoRA는 다음 matrix를 선택한다.

<math display="block" aria-label="LoRA factor dimensions">
  <mi>A</mi>
  <mo>&in;</mo>
  <msup><mi>R</mi><mrow><mi>r</mi><mo>&times;</mo><msub><mi>d</mi><mtext>in</mtext></msub></mrow></msup>
  <mo>,</mo>
  <mspace width="0.8em"></mspace>
  <mi>B</mi>
  <mo>&in;</mo>
  <msup><mi>R</mi><mrow><msub><mi>d</mi><mtext>out</mtext></msub><mo>&times;</mo><mi>r</mi></mrow></msup>
  <mo>,</mo>
  <mspace width="0.8em"></mspace>
  <mi>r</mi>
  <mo>&ll;</mo>
  <mi>min</mi>
  <mo>(</mo><msub><mi>d</mi><mtext>in</mtext></msub><mo>,</mo><msub><mi>d</mi><mtext>out</mtext></msub><mo>)</mo><mo>.</mo>
</math>

Dense update는 <math><msub><mi>d</mi><mtext>out</mtext></msub><msub><mi>d</mi><mtext>in</mtext></msub></math>개의 parameter를 갖는다. 반면 LoRA update는 해당 layer에서 다음 개수의 parameter만 학습한다.

<math display="block" aria-label="Number of LoRA trainable parameters">
  <mi>r</mi>
  <mo>(</mo>
  <msub><mi>d</mi><mtext>in</mtext></msub>
  <mo>+</mo>
  <msub><mi>d</mi><mtext>out</mtext></msub>
  <mo>)</mo>
</math>

<math><mi>r</mi></math>이 작으면 이는 큰 감소다.

Low-rank constraint는 regularization 역할도 한다.

<math display="block" aria-label="LoRA rank constraint">
  <mi>&Delta;</mi>
  <mi>W</mi>
  <mo>&in;</mo>
  <mo>{</mo>
  <mi>B</mi>
  <mi>A</mi>
  <mo>:</mo>
  <mi>rank</mi>
  <mo>(</mo>
  <mi>&Delta;</mi>
  <mi>W</mi>
  <mo>)</mo>
  <mo>&le;</mo>
  <mi>r</mi>
  <mo>}</mo><mo>.</mo>
</math>

학습 후에는 adapter를 base weight에 merge해서 inference에 사용할 수도 있다.

<math display="block" aria-label="Merged LoRA weight">
  <msub><mi>W</mi><mtext>merged</mtext></msub>
  <mo>=</mo>
  <mi>W</mi>
  <mo>+</mo>
  <mfrac>
    <mi>&alpha;</mi>
    <mi>r</mi>
  </mfrac>
  <mi>B</mi>
  <mi>A</mi><mo>.</mo>
</math>

QLoRA는 frozen base model 주변에 quantization layer를 추가한다. 보통 4-bit NormalFloat quantization, quantization constant에 대한 double quantization, memory spike를 줄이는 paged optimizer, 그리고 LoRA adapter의 higher-precision training이 함께 쓰인다. 핵심 설계는 비대칭적이다. base model은 압축하지만, task-specific adapter는 adaptation signal을 담을 만큼 충분한 precision으로 학습한다.

## 왜 작동할 수 있는가

LoRA가 작동할 수 있는 직관적 이유는 downstream adaptation이 model을 처음부터 다시 만들 필요가 없는 경우가 많기 때문이다. Pretrained model은 이미 풍부한 representation과 여러 유용한 behavior를 갖고 있다. 따라서 fine-tuning은 전체 함수를 다시 학습한다기보다, 이미 있는 behavior를 특정 방향으로 조정하는 일에 가깝다.

예를 들어 instruction tuning, domain adaptation, style adaptation은 latent behavioral direction을 바꾸는 경우가 많다. 지시를 더 잘 따르게 하기, 특정 domain format으로 답하게 하기, concise academic tone을 쓰게 하기, code-like output을 만들게 하기 같은 변화다. 이런 변화는 특히 attention projection이나 MLP projection에 적용되는 작은 수의 구조화된 방향으로 표현될 수 있다.

이것이 모든 유용한 task update가 low-rank라는 증명은 아니다. LoRA는 많은 setting에서 empirically useful한 bottleneck을 부여하는 방법이고, data가 제한될수록 매력적이다. 이 bottleneck은 update가 너무 자유롭게 움직이지 못하게 하므로 overfitting과 catastrophic forgetting을 줄이는 데 도움이 될 수 있다.

QLoRA는 추가적인 robustness assumption에 의존한다. Quantization은 base weight에 error를 넣는다.

<math display="block" aria-label="Quantization error model">
  <msub><mi>Q</mi><mn>4</mn></msub>
  <mo>(</mo><mi>W</mi><mo>)</mo>
  <mo>&approx;</mo>
  <mi>W</mi>
  <mo>+</mo>
  <msub><mi>&epsilon;</mi><mi>q</mi></msub><mo>.</mo>
</math>

QLoRA가 작동한다는 것은 useful pretrained behavior가 이 quantization error에 충분히 robust하고, LoRA adapter가 task-relevant residual difference를 어느 정도 보정할 수 있다는 뜻이다. 이는 practical empirical claim이지 universal guarantee는 아니다.

## 가정과 한계

LoRA는 유용한 task update가 low-rank correction으로 포착될 수 있다고 가정한다. 많은 adaptation task에서 그럴듯하지만 보장되지는 않는다. rank가 너무 작으면 adapter가 underfit한다. rank가 너무 크면 memory advantage와 regularization effect가 약해진다.

QLoRA는 base model이 adaptation 과정에서 4-bit quantization을 견딜 수 있다고 가정한다. 수치적으로 민감한 task, 작은 모델, 특수 domain, 긴 context reasoning에서는 작은 perturbation도 중요할 수 있으므로 항상 안전한 가정은 아니다.

두 방법 모두 새로운 factual knowledge를 안정적으로 주입하는 mechanism은 아니다. Fine-tuning이 domain pattern을 어느 정도 반영하게 만들 수는 있지만, 새롭거나 변하는 사실에 정확히 접근해야 한다면 retrieval-augmented generation, tool use, database grounding이 더 적절한 경우가 많다.

또한 두 방법은 base model의 한계 안에 있다. 작은 모델이나 약한 모델에 LoRA adapter를 붙인다고 갑자기 강한 reasoning model이 되지는 않는다. LoRA는 기존 capability를 조정하는 데 가깝지, 근본적으로 새로운 capability를 크게 창조하는 방법은 아니다.

마지막으로, data와 compute가 충분하고 operational justification이 있다면 full fine-tuning이 더 나을 수 있다. LoRA와 QLoRA는 update freedom을 줄이는 대신 efficiency, modularity, stability를 얻는 방법이다.

## 비판적 평가

LoRA의 가치는 fine-tuning을 modular correction 문제로 바꾼다는 데 있다. 하나의 base model 위에 medical response style, legal document analysis, code generation, bilingual technical writing, process systems engineering literature assistance 같은 여러 adapter를 붙일 수 있다. Task마다 model 전체 copy를 저장하지 않아도 된다는 점에서 operationally attractive하다.

QLoRA의 가치는 memory bottleneck을 옮긴다는 데 있다. LoRA만 사용해도 base model은 여전히 비교적 높은 precision으로 GPU memory에 올라가야 한다. QLoRA는 이 frozen base model을 압축해 더 제한된 hardware budget에서도 larger-model adaptation을 가능하게 한다.

가장 큰 위험은 두 방법을 과도하게 해석하는 것이다. LoRA나 QLoRA fine-tuning이 성공했다고 해서 adaptation이 reliable, truthful, safe, robust해진 것은 아니다. 그런 속성은 직접 평가해야 한다. 더 좁고 정확한 해석은 이것이다. LoRA와 QLoRA는 frozen base와 learned correction을 분리한 상태에서 pretrained model의 task-specific change를 효율적으로 실험하고 배포하는 방법이다.

## 참고문헌

- Edward J. Hu, Yelong Shen, Phillip Wallis, Zeyuan Allen-Zhu, Yuanzhi Li, Shean Wang, Lu Wang, and Weizhu Chen. "LoRA: Low-Rank Adaptation of Large Language Models." arXiv:2106.09685, 2021.
- Tim Dettmers, Artidoro Pagnoni, Ari Holtzman, and Luke Zettlemoyer. "QLoRA: Efficient Finetuning of Quantized LLMs." arXiv:2305.14314, 2023.
- 사용자가 제공한 LoRA/QLoRA 한국어 설명 노트.
