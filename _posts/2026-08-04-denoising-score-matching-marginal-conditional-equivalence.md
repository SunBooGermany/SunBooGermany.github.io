---
layout: post
title: "Denoising Score Matching: Why a Conditional Target Learns the Marginal Score"
title_ko: "Denoising Score Matching: 조건부 타깃이 주변부 Score를 학습하는 이유"
date: 2026-08-04
category: llm-probabilistic-approaches
category_label: "LLM & Probabilistic Approaches"
research_group: algorithmic_reviews
research_category: llm-probabilistic-approaches
research_category_label: "LLM & Probabilistic Approaches"
application_category: ""
application_category_label: ""
method_category: "llm-probabilistic-approaches"
method_category_label: "LLM & Probabilistic Approaches"
paper_title: "Stanford CME296 Diffusion & Large Vision Models | Spring 2026 | Lecture 2 - Score matching"
authors: ""
venue: ""
year: "2026"
doi: ""
arxiv: ""
source_url: ""
tags:
  - "denoising score matching"
  - "score-based models"
  - "diffusion models"
  - "Gaussian corruption"
  - "probabilistic modeling"
excerpt: "Diffusion models need the marginal score to reverse a noising process. This note explains why a tractable conditional Gaussian target learns that score and in what sense the two losses are equivalent."
excerpt_ko: "Diffusion model이 noising process를 역전할 때 필요한 marginal score를 조건부 Gaussian target으로 학습할 수 있는 이유와 두 손실함수의 정확한 등가성을 정리한다."
language: "en-ko"
has_korean_note: false
---

## Where Denoising Score Matching Enters a Diffusion Model

A diffusion model first defines a forward process that gradually adds Gaussian noise to data. At a noise level <math><mi>t</mi></math>, a common parameterization is

<math display="block" aria-label="Forward Gaussian noising process at time t">
  <msub><mi>x</mi><mi>t</mi></msub>
  <mo>=</mo><msub><mi>&alpha;</mi><mi>t</mi></msub><msub><mi>x</mi><mn>0</mn></msub>
  <mo>+</mo><msub><mi>&sigma;</mi><mi>t</mi></msub><mi>&epsilon;</mi><mo>,</mo>
  <mspace width="0.5em"></mspace>
  <mi>&epsilon;</mi><mo>&sim;</mo><mi mathvariant="normal">N</mi><mo>(</mo><mn>0</mn><mo>,</mo><mi>I</mi><mo>)</mo><mo>.</mo>
</math>

For sufficiently large noise, the distribution of <math><msub><mi>x</mi><mi>t</mi></msub></math> becomes close to a simple Gaussian. Generation starts from that noisy distribution and moves in the reverse direction. The reverse transition—expressed as a reverse-time SDE, an ODE, or a discrete denoising update—requires the score of the marginal distribution at the current noise level:

<math display="block" aria-label="Time dependent marginal score required by a diffusion model">
  <msub><mi>s</mi><mi>&theta;</mi></msub><mo>(</mo><msub><mi>x</mi><mi>t</mi></msub><mo>,</mo><mi>t</mi><mo>)</mo>
  <mo>&approx;</mo><msub><mo>&nabla;</mo><msub><mi>x</mi><mi>t</mi></msub></msub>
  <mi>log</mi><msub><mi>q</mi><mi>t</mi></msub><mo>(</mo><msub><mi>x</mi><mi>t</mi></msub><mo>)</mo><mo>.</mo>
</math>

This vector tells the sampler how the noisy state should be corrected at that level. Without it, the forward noising process is easy to run, but its reverse dynamics are unavailable.

The difficulty is that <math><msub><mi>q</mi><mi>t</mi></msub><mo>(</mo><msub><mi>x</mi><mi>t</mi></msub><mo>)</mo></math> is the result of averaging the forward kernel over the unknown data distribution. Its score cannot normally be evaluated for a training sample. What can be evaluated is the conditional score given the clean datum:

<math display="block" aria-label="Conditional score target used in diffusion training">
  <msub><mo>&nabla;</mo><msub><mi>x</mi><mi>t</mi></msub></msub>
  <mi>log</mi><mi>q</mi><mo>(</mo><msub><mi>x</mi><mi>t</mi></msub><mo>|</mo><msub><mi>x</mi><mn>0</mn></msub><mo>)</mo>
  <mo>=</mo><mfrac><mrow><msub><mi>&alpha;</mi><mi>t</mi></msub><msub><mi>x</mi><mn>0</mn></msub><mo>&minus;</mo><msub><mi>x</mi><mi>t</mi></msub></mrow><msup><msub><mi>&sigma;</mi><mi>t</mi></msub><mn>2</mn></msup></mfrac>
  <mo>=</mo><mo>&minus;</mo><mfrac><mi>&epsilon;</mi><msub><mi>&sigma;</mi><mi>t</mi></msub></mfrac><mo>.</mo>
</math>

Training can sample <math><msub><mi>x</mi><mn>0</mn></msub></math>, <math><mi>t</mi></math>, and <math><mi>&epsilon;</mi></math>, construct <math><msub><mi>x</mi><mi>t</mi></msub></math>, and regress against this known target. Implementations may predict the score, the added noise <math><mi>&epsilon;</mi></math>, or a denoised quantity; under Gaussian parameterizations these are related by known rescalings. Denoising score matching is the argument that makes this trainable target legitimate: its population optimum is the marginal score required by the reverse process.

The rest of this note fixes one noise level <math><mi>&sigma;</mi></math> to isolate that argument. A diffusion model applies the same reasoning across many levels and conditions the network on <math><mi>t</mi></math>, usually with a level-dependent loss weight.

Denoising score matching replaces an inaccessible marginal target with an accessible conditional one. The score of the full noisy-data distribution is usually unknown because that distribution is a mixture over the unknown data distribution. The score of a Gaussian corruption kernel, however, is available in closed form for every clean-noisy training pair.

The replacement looks suspicious at first. A conditional score points from one noisy sample toward the particular clean sample that generated it. The marginal score cannot depend on that hidden clean sample. It must describe the geometry of the entire noisy-data distribution. Why should regression against the first target recover the second?

The answer is an exact conditional-expectation identity. The two squared-error objectives are not numerically identical, but they differ only by a term independent of the model parameters. Their minimizers and parameter gradients are therefore the same.

## Clean Samples, Noisy Samples, and Two Distributions

Let a clean sample be drawn from the data distribution,

<math display="block" aria-label="A clean sample is drawn from the data distribution">
  <mi>x</mi><mo>&sim;</mo><msub><mi>p</mi><mtext>data</mtext></msub><mo>(</mo><mi>x</mi><mo>)</mo><mo>.</mo>
</math>

We corrupt it with isotropic Gaussian noise,

<math display="block" aria-label="Gaussian corruption of a clean sample">
  <mover><mi>x</mi><mo>~</mo></mover><mo>=</mo><mi>x</mi><mo>+</mo><mi>&sigma;</mi><mi>&epsilon;</mi><mo>,</mo>
  <mspace width="0.5em"></mspace>
  <mi>&epsilon;</mi><mo>&sim;</mo><mi mathvariant="normal">N</mi><mo>(</mo><mn>0</mn><mo>,</mo><mi>I</mi><mo>)</mo><mo>.</mo>
</math>

This defines the conditional corruption kernel

<math display="block" aria-label="Conditional Gaussian corruption kernel">
  <msub><mi>q</mi><mi>&sigma;</mi></msub><mo>(</mo><mover><mi>x</mi><mo>~</mo></mover><mo>|</mo><mi>x</mi><mo>)</mo>
  <mo>=</mo><mi mathvariant="normal">N</mi><mo>(</mo><mi>x</mi><mo>,</mo><msup><mi>&sigma;</mi><mn>2</mn></msup><mi>I</mi><mo>)</mo><mo>.</mo>
</math>

This distribution is known. We chose it. For a fixed clean point <math><mi>x</mi></math>, it says where the perturbed point <math><mover><mi>x</mi><mo>~</mo></mover></math> can land.

The marginal noisy-data distribution is different:

<math display="block" aria-label="Marginal noisy data distribution">
  <msub><mi>q</mi><mi>&sigma;</mi></msub><mo>(</mo><mover><mi>x</mi><mo>~</mo></mover><mo>)</mo>
  <mo>=</mo><mo>&int;</mo><msub><mi>p</mi><mtext>data</mtext></msub><mo>(</mo><mi>x</mi><mo>)</mo>
  <msub><mi>q</mi><mi>&sigma;</mi></msub><mo>(</mo><mover><mi>x</mi><mo>~</mo></mover><mo>|</mo><mi>x</mi><mo>)</mo><mi>d</mi><mi>x</mi><mo>.</mo>
</math>

It is the mixture obtained after corrupting every possible clean sample. Even though the Gaussian kernel is explicit, the mixture generally is not: the data distribution is available through samples, not as a tractable density.

This distinction is the whole problem. The conditional density is easy to evaluate, while the marginal density is the distribution whose score the model must ultimately learn.

## The Direct Objective Is Inaccessible

Let <math><msub><mi>s</mi><mi>&theta;</mi></msub><mo>(</mo><mover><mi>x</mi><mo>~</mo></mover><mo>)</mo></math> be a neural network that predicts a vector. The desired target is the marginal score,

<math display="block" aria-label="The marginal score learning target">
  <msub><mi>s</mi><mi>&theta;</mi></msub><mo>(</mo><mover><mi>x</mi><mo>~</mo></mover><mo>)</mo>
  <mo>&approx;</mo><msub><mo>&nabla;</mo><mover><mi>x</mi><mo>~</mo></mover></msub>
  <mi>log</mi><msub><mi>q</mi><mi>&sigma;</mi></msub><mo>(</mo><mover><mi>x</mi><mo>~</mo></mover><mo>)</mo><mo>.</mo>
</math>

The score is the gradient of log density, not the density itself. At a noisy point, it indicates the local direction in which log density increases fastest. For a smoothed data distribution, this often points toward a region containing more probability mass. Calling it a “direction back to the data manifold” is useful intuition, but it is only approximate: at an ambiguous point, the score combines several possible clean explanations.

The most direct squared-error objective would be

<math display="block" aria-label="Explicit score matching objective">
  <msub><mi>J</mi><mtext>explicit</mtext></msub><mo>(</mo><mi>&theta;</mi><mo>)</mo>
  <mo>=</mo><msub><mi mathvariant="double-struck">E</mi><mover><mi>x</mi><mo>~</mo></mover></msub>
  <mrow><mo>[</mo><msup><mrow><mo>&Vert;</mo>
  <msub><mi>s</mi><mi>&theta;</mi></msub><mo>(</mo><mover><mi>x</mi><mo>~</mo></mover><mo>)</mo>
  <mo>&minus;</mo><msub><mo>&nabla;</mo><mover><mi>x</mi><mo>~</mo></mover></msub>
  <mi>log</mi><msub><mi>q</mi><mi>&sigma;</mi></msub><mo>(</mo><mover><mi>x</mi><mo>~</mo></mover><mo>)</mo>
  <mo>&Vert;</mo></mrow><mn>2</mn></msup><mo>]</mo></mrow><mo>.</mo>
</math>

The target in this expression requires the intractable marginal mixture. This objective states the right problem but does not yet give a usable training rule.

## The Conditional Gaussian Score Is Available

Denoising score matching instead uses the score of the conditional corruption kernel:

<math display="block" aria-label="Denoising score matching objective">
  <msub><mi>J</mi><mtext>DSM</mtext></msub><mo>(</mo><mi>&theta;</mi><mo>)</mo>
  <mo>=</mo><msub><mi mathvariant="double-struck">E</mi><mrow><mi>x</mi><mo>,</mo><mover><mi>x</mi><mo>~</mo></mover></mrow></msub>
  <mrow><mo>[</mo><msup><mrow><mo>&Vert;</mo>
  <msub><mi>s</mi><mi>&theta;</mi></msub><mo>(</mo><mover><mi>x</mi><mo>~</mo></mover><mo>)</mo>
  <mo>&minus;</mo><msub><mo>&nabla;</mo><mover><mi>x</mi><mo>~</mo></mover></msub>
  <mi>log</mi><msub><mi>q</mi><mi>&sigma;</mi></msub><mo>(</mo><mover><mi>x</mi><mo>~</mo></mover><mo>|</mo><mi>x</mi><mo>)</mo>
  <mo>&Vert;</mo></mrow><mn>2</mn></msup><mo>]</mo></mrow><mo>.</mo>
</math>

For Gaussian corruption, the target is explicit:

<math display="block" aria-label="Conditional Gaussian score">
  <msub><mo>&nabla;</mo><mover><mi>x</mi><mo>~</mo></mover></msub>
  <mi>log</mi><msub><mi>q</mi><mi>&sigma;</mi></msub><mo>(</mo><mover><mi>x</mi><mo>~</mo></mover><mo>|</mo><mi>x</mi><mo>)</mo>
  <mo>=</mo><mfrac><mrow><mi>x</mi><mo>&minus;</mo><mover><mi>x</mi><mo>~</mo></mover></mrow><msup><mi>&sigma;</mi><mn>2</mn></msup></mfrac><mo>.</mo>
</math>

Every clean-noisy pair therefore supplies a supervised regression target. For that pair, the vector points from the noisy sample toward its generating clean sample, scaled by inverse noise variance.

This target is noisy in a statistical sense. The same noisy location can be compatible with multiple clean samples, and those clean samples imply different regression targets. The network cannot identify which hidden clean point generated a location from the noisy location alone. Under squared loss, it learns their conditional mean.

## The Identity That Connects the Two Scores

The marginal score is exactly that conditional mean:

<math display="block" aria-label="Marginal score as conditional expectation of conditional score">
  <msub><mo>&nabla;</mo><mover><mi>x</mi><mo>~</mo></mover></msub>
  <mi>log</mi><msub><mi>q</mi><mi>&sigma;</mi></msub><mo>(</mo><mover><mi>x</mi><mo>~</mo></mover><mo>)</mo>
  <mo>=</mo><msub><mi mathvariant="double-struck">E</mi><mrow><mi>x</mi><mo>|</mo><mover><mi>x</mi><mo>~</mo></mover></mrow></msub>
  <mrow><mo>[</mo><msub><mo>&nabla;</mo><mover><mi>x</mi><mo>~</mo></mover></msub>
  <mi>log</mi><msub><mi>q</mi><mi>&sigma;</mi></msub><mo>(</mo><mover><mi>x</mi><mo>~</mo></mover><mo>|</mo><mi>x</mi><mo>)</mo><mo>]</mo></mrow><mo>.</mo>
</math>

The derivation is short. Differentiate the marginal density under the integral sign:

<math display="block" aria-label="Differentiate the marginal density">
  <msub><mo>&nabla;</mo><mover><mi>x</mi><mo>~</mo></mover></msub>
  <msub><mi>q</mi><mi>&sigma;</mi></msub><mo>(</mo><mover><mi>x</mi><mo>~</mo></mover><mo>)</mo>
  <mo>=</mo><mo>&int;</mo><msub><mi>p</mi><mtext>data</mtext></msub><mo>(</mo><mi>x</mi><mo>)</mo>
  <msub><mo>&nabla;</mo><mover><mi>x</mi><mo>~</mo></mover></msub>
  <msub><mi>q</mi><mi>&sigma;</mi></msub><mo>(</mo><mover><mi>x</mi><mo>~</mo></mover><mo>|</mo><mi>x</mi><mo>)</mo><mi>d</mi><mi>x</mi><mo>.</mo>
</math>

Using <math><mo>&nabla;</mo><mi>q</mi><mo>=</mo><mi>q</mi><mo>&nabla;</mo><mi>log</mi><mi>q</mi></math>, divide by the marginal density. The ratio inside the integral becomes the posterior density over clean samples,

<math display="block" aria-label="Bayes rule produces the clean sample posterior">
  <mfrac><mrow><msub><mi>p</mi><mtext>data</mtext></msub><mo>(</mo><mi>x</mi><mo>)</mo>
  <msub><mi>q</mi><mi>&sigma;</mi></msub><mo>(</mo><mover><mi>x</mi><mo>~</mo></mover><mo>|</mo><mi>x</mi><mo>)</mo></mrow>
  <mrow><msub><mi>q</mi><mi>&sigma;</mi></msub><mo>(</mo><mover><mi>x</mi><mo>~</mo></mover><mo>)</mo></mrow></mfrac>
  <mo>=</mo><msub><mi>q</mi><mi>&sigma;</mi></msub><mo>(</mo><mi>x</mi><mo>|</mo><mover><mi>x</mi><mo>~</mo></mover><mo>)</mo><mo>.</mo>
</math>

Substitution gives the conditional-expectation identity above. The usual regularity conditions are doing real work here: differentiation must be allowed to pass through the integral, the relevant expectations must exist, and the marginal density must be positive where its log score is evaluated. Gaussian smoothing makes these conditions mild in many standard settings, but the algebra should not be read as assumption-free.

## Exact Equivalence of the Objectives

Define

<math display="block" aria-label="Definitions of marginal and conditional score targets">
  <mi>a</mi><mo>(</mo><mover><mi>x</mi><mo>~</mo></mover><mo>)</mo>
  <mo>=</mo><msub><mo>&nabla;</mo><mover><mi>x</mi><mo>~</mo></mover></msub><mi>log</mi><msub><mi>q</mi><mi>&sigma;</mi></msub><mo>(</mo><mover><mi>x</mi><mo>~</mo></mover><mo>)</mo><mo>,</mo>
  <mspace width="1em"></mspace>
  <mi>b</mi><mo>(</mo><mi>x</mi><mo>,</mo><mover><mi>x</mi><mo>~</mo></mover><mo>)</mo>
  <mo>=</mo><msub><mo>&nabla;</mo><mover><mi>x</mi><mo>~</mo></mover></msub><mi>log</mi><msub><mi>q</mi><mi>&sigma;</mi></msub><mo>(</mo><mover><mi>x</mi><mo>~</mo></mover><mo>|</mo><mi>x</mi><mo>)</mo><mo>.</mo>
</math>

Then <math><mi>a</mi><mo>(</mo><mover><mi>x</mi><mo>~</mo></mover><mo>)</mo><mo>=</mo><mi mathvariant="double-struck">E</mi><mo>[</mo><mi>b</mi><mo>|</mo><mover><mi>x</mi><mo>~</mo></mover><mo>]</mo></math>. Conditional bias-variance decomposition gives

<math display="block" aria-label="Loss decomposition for denoising score matching">
  <msub><mi>J</mi><mtext>DSM</mtext></msub><mo>(</mo><mi>&theta;</mi><mo>)</mo>
  <mo>=</mo><msub><mi>J</mi><mtext>explicit</mtext></msub><mo>(</mo><mi>&theta;</mi><mo>)</mo>
  <mo>+</mo><msub><mi mathvariant="double-struck">E</mi><mover><mi>x</mi><mo>~</mo></mover></msub>
  <mrow><mo>[</mo><msub><mi mathvariant="double-struck">E</mi><mrow><mi>x</mi><mo>|</mo><mover><mi>x</mi><mo>~</mo></mover></mrow></msub>
  <mrow><mo>[</mo><msup><mrow><mo>&Vert;</mo><mi>b</mi><mo>&minus;</mo><mi>a</mi><mo>&Vert;</mo></mrow><mn>2</mn></msup><mo>]</mo></mrow><mo>]</mo></mrow><mo>.</mo>
</math>

The last term is the conditional variance of the vector target, more precisely its expected squared deviation from the conditional mean. It contains no <math><mi>&theta;</mi></math>. Hence

<math display="block" aria-label="Same minimizers and gradients">
  <munder><mi>arg min</mi><mi>&theta;</mi></munder><msub><mi>J</mi><mtext>DSM</mtext></msub><mo>(</mo><mi>&theta;</mi><mo>)</mo>
  <mo>=</mo><munder><mi>arg min</mi><mi>&theta;</mi></munder><msub><mi>J</mi><mtext>explicit</mtext></msub><mo>(</mo><mi>&theta;</mi><mo>)</mo><mo>,</mo>
  <mspace width="1em"></mspace>
  <msub><mo>&nabla;</mo><mi>&theta;</mi></msub><msub><mi>J</mi><mtext>DSM</mtext></msub>
  <mo>=</mo><msub><mo>&nabla;</mo><mi>&theta;</mi></msub><msub><mi>J</mi><mtext>explicit</mtext></msub><mo>.</mo>
</math>

This is the precise meaning of “the two losses are equivalent.” Their numerical values need not match. The denoising objective includes irreducible target variance, so it is generally larger by a constant. What matches is the optimization problem with respect to <math><mi>&theta;</mi></math>.

## Why the Learned Vector Is a Denoising Direction

For Gaussian corruption, insert the conditional score into the expectation identity:

<math display="block" aria-label="Marginal score under Gaussian corruption">
  <msup><mi>s</mi><mo>*</mo></msup><mo>(</mo><mover><mi>x</mi><mo>~</mo></mover><mo>)</mo>
  <mo>=</mo><msub><mi mathvariant="double-struck">E</mi><mrow><mi>x</mi><mo>|</mo><mover><mi>x</mi><mo>~</mo></mover></mrow></msub>
  <mrow><mo>[</mo><mfrac><mrow><mi>x</mi><mo>&minus;</mo><mover><mi>x</mi><mo>~</mo></mover></mrow><msup><mi>&sigma;</mi><mn>2</mn></msup></mfrac><mo>]</mo></mrow><mo>.</mo>
</math>

Rearranging yields

<math display="block" aria-label="Posterior mean denoising identity">
  <mi mathvariant="double-struck">E</mi><mo>[</mo><mi>x</mi><mo>|</mo><mover><mi>x</mi><mo>~</mo></mover><mo>]</mo>
  <mo>=</mo><mover><mi>x</mi><mo>~</mo></mover><mo>+</mo><msup><mi>&sigma;</mi><mn>2</mn></msup>
  <msup><mi>s</mi><mo>*</mo></msup><mo>(</mo><mover><mi>x</mi><mo>~</mo></mover><mo>)</mo><mo>.</mo>
</math>

The score correction moves a noisy point toward the posterior mean of the clean sample. This is stronger and more precise than saying that every score vector points back to one original datum. When several clean explanations are plausible, the learned vector averages them according to the posterior induced by the corruption process.

That averaging is also the reason sample-wise training works. Each training pair provides a target aimed at one clean sample. Across many pairs, squared-error regression estimates the conditional mean of those targets. The conditional mean is the marginal score. Denoising supervision is therefore not a heuristic substitute for score learning; under the stated conditions, it is a tractable regression formulation of the same parameter optimization problem.

The scope of the claim should remain narrow. It does not say that a finite neural network reaches the population optimum, that finite-sample training is unbiased in every implementation, or that optimization finds the global minimizer. It says that at the population-objective level, replacing the marginal score with the conditional corruption score changes the loss only by a parameter-independent constant. That is the core equivalence.

## Reference

**Stanford CME296 Diffusion & Large Vision Models | Spring 2026 | Lecture 2 - Score matching**

<!-- ko -->

## Diffusion Model에서 Denoising Score Matching이 필요한 지점

Diffusion model은 먼저 데이터에 Gaussian noise를 점진적으로 더하는 forward process를 정의한다. Noise level <math><mi>t</mi></math>에서 흔히 사용하는 parameterization은 다음과 같다.

<math display="block" aria-label="Forward Gaussian noising process at time t">
  <msub><mi>x</mi><mi>t</mi></msub>
  <mo>=</mo><msub><mi>&alpha;</mi><mi>t</mi></msub><msub><mi>x</mi><mn>0</mn></msub>
  <mo>+</mo><msub><mi>&sigma;</mi><mi>t</mi></msub><mi>&epsilon;</mi><mo>,</mo>
  <mspace width="0.5em"></mspace>
  <mi>&epsilon;</mi><mo>&sim;</mo><mi mathvariant="normal">N</mi><mo>(</mo><mn>0</mn><mo>,</mo><mi>I</mi><mo>)</mo><mo>.</mo>
</math>

Noise가 충분히 커지면 <math><msub><mi>x</mi><mi>t</mi></msub></math>의 분포는 단순한 Gaussian에 가까워진다. 생성은 이 noisy distribution에서 출발해 반대 방향으로 진행한다. Reverse-time SDE, ODE, 또는 discrete denoising update로 표현되는 reverse transition에는 현재 noise level에서의 marginal distribution score가 필요하다.

<math display="block" aria-label="Time dependent marginal score required by a diffusion model">
  <msub><mi>s</mi><mi>&theta;</mi></msub><mo>(</mo><msub><mi>x</mi><mi>t</mi></msub><mo>,</mo><mi>t</mi><mo>)</mo>
  <mo>&approx;</mo><msub><mo>&nabla;</mo><msub><mi>x</mi><mi>t</mi></msub></msub>
  <mi>log</mi><msub><mi>q</mi><mi>t</mi></msub><mo>(</mo><msub><mi>x</mi><mi>t</mi></msub><mo>)</mo><mo>.</mo>
</math>

이 벡터는 해당 noise level에서 noisy state를 어느 방향으로 보정해야 하는지를 알려준다. 이 score가 없으면 forward noising은 쉽게 실행할 수 있지만 그 reverse dynamics를 구성할 수 없다.

문제는 <math><msub><mi>q</mi><mi>t</mi></msub><mo>(</mo><msub><mi>x</mi><mi>t</mi></msub><mo>)</mo></math>가 forward kernel을 미지의 data distribution에 대해 평균한 결과라는 점이다. 따라서 training sample에서 그 score를 직접 계산할 수 없다. 대신 clean datum이 주어진 conditional score는 계산할 수 있다.

<math display="block" aria-label="Conditional score target used in diffusion training">
  <msub><mo>&nabla;</mo><msub><mi>x</mi><mi>t</mi></msub></msub>
  <mi>log</mi><mi>q</mi><mo>(</mo><msub><mi>x</mi><mi>t</mi></msub><mo>|</mo><msub><mi>x</mi><mn>0</mn></msub><mo>)</mo>
  <mo>=</mo><mfrac><mrow><msub><mi>&alpha;</mi><mi>t</mi></msub><msub><mi>x</mi><mn>0</mn></msub><mo>&minus;</mo><msub><mi>x</mi><mi>t</mi></msub></mrow><msup><msub><mi>&sigma;</mi><mi>t</mi></msub><mn>2</mn></msup></mfrac>
  <mo>=</mo><mo>&minus;</mo><mfrac><mi>&epsilon;</mi><msub><mi>&sigma;</mi><mi>t</mi></msub></mfrac><mo>.</mo>
</math>

학습할 때는 <math><msub><mi>x</mi><mn>0</mn></msub></math>, <math><mi>t</mi></math>, <math><mi>&epsilon;</mi></math>을 sampling하여 <math><msub><mi>x</mi><mi>t</mi></msub></math>를 만들고, 이 계산 가능한 target에 대해 regression하면 된다. 구현에 따라 score, 추가한 noise <math><mi>&epsilon;</mi></math>, 또는 denoised quantity를 예측하지만 Gaussian parameterization에서는 이들이 알려진 scaling으로 연결된다. Denoising score matching은 이 계산 가능한 target을 정당화한다. 그 population optimum이 reverse process에 필요한 marginal score이기 때문이다.

이하에서는 핵심 논리를 분리해 보기 위해 하나의 noise level <math><mi>&sigma;</mi></math>를 고정한다. 실제 diffusion model은 여러 noise level에서 같은 논리를 적용하며, network가 <math><mi>t</mi></math>에도 의존하도록 학습한다. 보통 noise level별 loss weight도 함께 사용한다.

Denoising score matching은 계산하기 어려운 marginal target을 계산 가능한 conditional target으로 바꾼다. 전체 noisy-data distribution의 score는 일반적으로 알기 어렵다. 이 분포가 미지의 데이터 분포 위에서 정의된 mixture이기 때문이다. 반면 Gaussian corruption kernel의 score는 각 clean-noisy training pair에 대해 닫힌 형태로 계산할 수 있다.

처음 보면 이 대체는 의심스럽다. Conditional score는 하나의 noisy sample을 그 sample을 생성한 특정 clean sample 쪽으로 향하게 한다. Marginal score는 숨겨진 clean sample에 의존할 수 없다. 전체 noisy-data distribution의 기하를 나타내야 한다. 그런데 왜 첫 번째 타깃에 대한 회귀가 두 번째 타깃을 복원하는가?

답은 정확한 conditional-expectation identity에 있다. 두 squared-error objective의 수치가 같은 것은 아니다. 그러나 두 목적함수는 모델 매개변수와 무관한 항만큼만 차이 난다. 따라서 minimizer와 parameter gradient는 같다.

## Clean Sample, Noisy Sample, 그리고 두 분포

먼저 clean sample을 데이터 분포에서 뽑는다.

<math display="block" aria-label="A clean sample is drawn from the data distribution">
  <mi>x</mi><mo>&sim;</mo><msub><mi>p</mi><mtext>data</mtext></msub><mo>(</mo><mi>x</mi><mo>)</mo><mo>.</mo>
</math>

여기에 isotropic Gaussian noise를 더한다.

<math display="block" aria-label="Gaussian corruption of a clean sample">
  <mover><mi>x</mi><mo>~</mo></mover><mo>=</mo><mi>x</mi><mo>+</mo><mi>&sigma;</mi><mi>&epsilon;</mi><mo>,</mo>
  <mspace width="0.5em"></mspace>
  <mi>&epsilon;</mi><mo>&sim;</mo><mi mathvariant="normal">N</mi><mo>(</mo><mn>0</mn><mo>,</mo><mi>I</mi><mo>)</mo><mo>.</mo>
</math>

이 과정은 다음 conditional corruption kernel을 정의한다.

<math display="block" aria-label="Conditional Gaussian corruption kernel">
  <msub><mi>q</mi><mi>&sigma;</mi></msub><mo>(</mo><mover><mi>x</mi><mo>~</mo></mover><mo>|</mo><mi>x</mi><mo>)</mo>
  <mo>=</mo><mi mathvariant="normal">N</mi><mo>(</mo><mi>x</mi><mo>,</mo><msup><mi>&sigma;</mi><mn>2</mn></msup><mi>I</mi><mo>)</mo><mo>.</mo>
</math>

이 분포는 알고 있다. 우리가 직접 선택했기 때문이다. Clean point <math><mi>x</mi></math>가 고정되었을 때 perturbed point <math><mover><mi>x</mi><mo>~</mo></mover></math>가 어디에 위치할 수 있는지를 나타낸다.

Marginal noisy-data distribution은 다르다.

<math display="block" aria-label="Marginal noisy data distribution">
  <msub><mi>q</mi><mi>&sigma;</mi></msub><mo>(</mo><mover><mi>x</mi><mo>~</mo></mover><mo>)</mo>
  <mo>=</mo><mo>&int;</mo><msub><mi>p</mi><mtext>data</mtext></msub><mo>(</mo><mi>x</mi><mo>)</mo>
  <msub><mi>q</mi><mi>&sigma;</mi></msub><mo>(</mo><mover><mi>x</mi><mo>~</mo></mover><mo>|</mo><mi>x</mi><mo>)</mo><mi>d</mi><mi>x</mi><mo>.</mo>
</math>

이 분포는 가능한 모든 clean sample을 오염시킨 뒤 얻는 mixture이다. Gaussian kernel 자체는 명시적이지만 이 mixture는 보통 명시적이지 않다. 데이터 분포를 계산 가능한 density가 아니라 sample을 통해서만 알고 있기 때문이다.

두 분포의 구분이 문제의 핵심이다. Conditional density는 쉽게 계산할 수 있지만, 모델이 최종적으로 배워야 할 score는 marginal density의 score이다.

## 직접적인 목적함수는 계산하기 어렵다

벡터를 출력하는 neural network를 <math><msub><mi>s</mi><mi>&theta;</mi></msub><mo>(</mo><mover><mi>x</mi><mo>~</mo></mover><mo>)</mo></math>라고 하자. 원하는 타깃은 marginal score이다.

<math display="block" aria-label="The marginal score learning target">
  <msub><mi>s</mi><mi>&theta;</mi></msub><mo>(</mo><mover><mi>x</mi><mo>~</mo></mover><mo>)</mo>
  <mo>&approx;</mo><msub><mo>&nabla;</mo><mover><mi>x</mi><mo>~</mo></mover></msub>
  <mi>log</mi><msub><mi>q</mi><mi>&sigma;</mi></msub><mo>(</mo><mover><mi>x</mi><mo>~</mo></mover><mo>)</mo><mo>.</mo>
</math>

Score는 density 자체가 아니라 log density의 gradient이다. 한 noisy point에서 log density가 가장 빠르게 증가하는 국소 방향을 가리킨다. Smoothed data distribution에서는 대체로 probability mass가 더 많은 영역 쪽을 향한다. 이를 “data manifold로 돌아가는 방향”이라고 해석하면 직관적이지만, 이 표현은 근사적인 설명이다. 여러 clean sample이 가능한 모호한 지점에서는 score가 여러 설명을 결합하기 때문이다.

가장 직접적인 squared-error objective는 다음과 같다.

<math display="block" aria-label="Explicit score matching objective">
  <msub><mi>J</mi><mtext>explicit</mtext></msub><mo>(</mo><mi>&theta;</mi><mo>)</mo>
  <mo>=</mo><msub><mi mathvariant="double-struck">E</mi><mover><mi>x</mi><mo>~</mo></mover></msub>
  <mrow><mo>[</mo><msup><mrow><mo>&Vert;</mo>
  <msub><mi>s</mi><mi>&theta;</mi></msub><mo>(</mo><mover><mi>x</mi><mo>~</mo></mover><mo>)</mo>
  <mo>&minus;</mo><msub><mo>&nabla;</mo><mover><mi>x</mi><mo>~</mo></mover></msub>
  <mi>log</mi><msub><mi>q</mi><mi>&sigma;</mi></msub><mo>(</mo><mover><mi>x</mi><mo>~</mo></mover><mo>)</mo>
  <mo>&Vert;</mo></mrow><mn>2</mn></msup><mo>]</mo></mrow><mo>.</mo>
</math>

하지만 이 식의 target을 구하려면 계산하기 어려운 marginal mixture가 필요하다. 목적함수는 올바른 문제를 표현하지만, 아직 사용할 수 있는 학습 규칙은 아니다.

## Conditional Gaussian Score는 계산할 수 있다

Denoising score matching은 대신 conditional corruption kernel의 score를 사용한다.

<math display="block" aria-label="Denoising score matching objective">
  <msub><mi>J</mi><mtext>DSM</mtext></msub><mo>(</mo><mi>&theta;</mi><mo>)</mo>
  <mo>=</mo><msub><mi mathvariant="double-struck">E</mi><mrow><mi>x</mi><mo>,</mo><mover><mi>x</mi><mo>~</mo></mover></mrow></msub>
  <mrow><mo>[</mo><msup><mrow><mo>&Vert;</mo>
  <msub><mi>s</mi><mi>&theta;</mi></msub><mo>(</mo><mover><mi>x</mi><mo>~</mo></mover><mo>)</mo>
  <mo>&minus;</mo><msub><mo>&nabla;</mo><mover><mi>x</mi><mo>~</mo></mover></msub>
  <mi>log</mi><msub><mi>q</mi><mi>&sigma;</mi></msub><mo>(</mo><mover><mi>x</mi><mo>~</mo></mover><mo>|</mo><mi>x</mi><mo>)</mo>
  <mo>&Vert;</mo></mrow><mn>2</mn></msup><mo>]</mo></mrow><mo>.</mo>
</math>

Gaussian corruption에서는 이 target을 명시적으로 계산할 수 있다.

<math display="block" aria-label="Conditional Gaussian score">
  <msub><mo>&nabla;</mo><mover><mi>x</mi><mo>~</mo></mover></msub>
  <mi>log</mi><msub><mi>q</mi><mi>&sigma;</mi></msub><mo>(</mo><mover><mi>x</mi><mo>~</mo></mover><mo>|</mo><mi>x</mi><mo>)</mo>
  <mo>=</mo><mfrac><mrow><mi>x</mi><mo>&minus;</mo><mover><mi>x</mi><mo>~</mo></mover></mrow><msup><mi>&sigma;</mi><mn>2</mn></msup></mfrac><mo>.</mo>
</math>

따라서 모든 clean-noisy pair가 supervised regression target을 제공한다. 각 pair의 target은 noisy sample에서 그 sample을 생성한 clean sample 쪽을 가리키며, inverse noise variance로 scaling된다.

이 target은 통계적인 의미에서 noisy하다. 같은 noisy location이 여러 clean sample과 양립할 수 있고, 각 clean sample은 서로 다른 회귀 타깃을 만든다. Network는 noisy location만 보고 어느 clean point가 숨어 있었는지 식별할 수 없다. Squared loss 아래에서는 그 타깃들의 conditional mean을 학습한다.

## 두 Score를 연결하는 항등식

Marginal score는 바로 그 conditional mean이다.

<math display="block" aria-label="Marginal score as conditional expectation of conditional score">
  <msub><mo>&nabla;</mo><mover><mi>x</mi><mo>~</mo></mover></msub>
  <mi>log</mi><msub><mi>q</mi><mi>&sigma;</mi></msub><mo>(</mo><mover><mi>x</mi><mo>~</mo></mover><mo>)</mo>
  <mo>=</mo><msub><mi mathvariant="double-struck">E</mi><mrow><mi>x</mi><mo>|</mo><mover><mi>x</mi><mo>~</mo></mover></mrow></msub>
  <mrow><mo>[</mo><msub><mo>&nabla;</mo><mover><mi>x</mi><mo>~</mo></mover></msub>
  <mi>log</mi><msub><mi>q</mi><mi>&sigma;</mi></msub><mo>(</mo><mover><mi>x</mi><mo>~</mo></mover><mo>|</mo><mi>x</mi><mo>)</mo><mo>]</mo></mrow><mo>.</mo>
</math>

유도는 짧다. Marginal density를 적분 기호 안에서 미분한다.

<math display="block" aria-label="Differentiate the marginal density">
  <msub><mo>&nabla;</mo><mover><mi>x</mi><mo>~</mo></mover></msub>
  <msub><mi>q</mi><mi>&sigma;</mi></msub><mo>(</mo><mover><mi>x</mi><mo>~</mo></mover><mo>)</mo>
  <mo>=</mo><mo>&int;</mo><msub><mi>p</mi><mtext>data</mtext></msub><mo>(</mo><mi>x</mi><mo>)</mo>
  <msub><mo>&nabla;</mo><mover><mi>x</mi><mo>~</mo></mover></msub>
  <msub><mi>q</mi><mi>&sigma;</mi></msub><mo>(</mo><mover><mi>x</mi><mo>~</mo></mover><mo>|</mo><mi>x</mi><mo>)</mo><mi>d</mi><mi>x</mi><mo>.</mo>
</math>

<math><mo>&nabla;</mo><mi>q</mi><mo>=</mo><mi>q</mi><mo>&nabla;</mo><mi>log</mi><mi>q</mi></math>를 적용하고 marginal density로 나누면 적분 안의 비율이 clean sample에 대한 posterior density가 된다.

<math display="block" aria-label="Bayes rule produces the clean sample posterior">
  <mfrac><mrow><msub><mi>p</mi><mtext>data</mtext></msub><mo>(</mo><mi>x</mi><mo>)</mo>
  <msub><mi>q</mi><mi>&sigma;</mi></msub><mo>(</mo><mover><mi>x</mi><mo>~</mo></mover><mo>|</mo><mi>x</mi><mo>)</mo></mrow>
  <mrow><msub><mi>q</mi><mi>&sigma;</mi></msub><mo>(</mo><mover><mi>x</mi><mo>~</mo></mover><mo>)</mo></mrow></mfrac>
  <mo>=</mo><msub><mi>q</mi><mi>&sigma;</mi></msub><mo>(</mo><mi>x</mi><mo>|</mo><mover><mi>x</mi><mo>~</mo></mover><mo>)</mo><mo>.</mo>
</math>

이를 대입하면 위의 conditional-expectation identity를 얻는다. 여기에는 통상적인 regularity condition이 필요하다. 미분을 적분 안으로 옮길 수 있어야 하고, 관련 기대값이 존재해야 하며, log score를 계산하는 곳에서 marginal density가 양수여야 한다. Gaussian smoothing은 많은 표준적인 상황에서 이 조건들을 완화하지만, 유도 자체가 무가정인 것은 아니다.

## 목적함수의 정확한 등가성

다음과 같이 정의하자.

<math display="block" aria-label="Definitions of marginal and conditional score targets">
  <mi>a</mi><mo>(</mo><mover><mi>x</mi><mo>~</mo></mover><mo>)</mo>
  <mo>=</mo><msub><mo>&nabla;</mo><mover><mi>x</mi><mo>~</mo></mover></msub><mi>log</mi><msub><mi>q</mi><mi>&sigma;</mi></msub><mo>(</mo><mover><mi>x</mi><mo>~</mo></mover><mo>)</mo><mo>,</mo>
  <mspace width="1em"></mspace>
  <mi>b</mi><mo>(</mo><mi>x</mi><mo>,</mo><mover><mi>x</mi><mo>~</mo></mover><mo>)</mo>
  <mo>=</mo><msub><mo>&nabla;</mo><mover><mi>x</mi><mo>~</mo></mover></msub><mi>log</mi><msub><mi>q</mi><mi>&sigma;</mi></msub><mo>(</mo><mover><mi>x</mi><mo>~</mo></mover><mo>|</mo><mi>x</mi><mo>)</mo><mo>.</mo>
</math>

그러면 <math><mi>a</mi><mo>(</mo><mover><mi>x</mi><mo>~</mo></mover><mo>)</mo><mo>=</mo><mi mathvariant="double-struck">E</mi><mo>[</mo><mi>b</mi><mo>|</mo><mover><mi>x</mi><mo>~</mo></mover><mo>]</mo></math>이다. Conditional bias-variance decomposition을 적용하면 다음 관계를 얻는다.

<math display="block" aria-label="Loss decomposition for denoising score matching">
  <msub><mi>J</mi><mtext>DSM</mtext></msub><mo>(</mo><mi>&theta;</mi><mo>)</mo>
  <mo>=</mo><msub><mi>J</mi><mtext>explicit</mtext></msub><mo>(</mo><mi>&theta;</mi><mo>)</mo>
  <mo>+</mo><msub><mi mathvariant="double-struck">E</mi><mover><mi>x</mi><mo>~</mo></mover></msub>
  <mrow><mo>[</mo><msub><mi mathvariant="double-struck">E</mi><mrow><mi>x</mi><mo>|</mo><mover><mi>x</mi><mo>~</mo></mover></mrow></msub>
  <mrow><mo>[</mo><msup><mrow><mo>&Vert;</mo><mi>b</mi><mo>&minus;</mo><mi>a</mi><mo>&Vert;</mo></mrow><mn>2</mn></msup><mo>]</mo></mrow><mo>]</mo></mrow><mo>.</mo>
</math>

마지막 항은 vector target의 conditional variance, 더 정확히는 conditional mean으로부터의 squared deviation의 기대값이다. 이 항에는 <math><mi>&theta;</mi></math>가 없다. 따라서

<math display="block" aria-label="Same minimizers and gradients">
  <munder><mi>arg min</mi><mi>&theta;</mi></munder><msub><mi>J</mi><mtext>DSM</mtext></msub><mo>(</mo><mi>&theta;</mi><mo>)</mo>
  <mo>=</mo><munder><mi>arg min</mi><mi>&theta;</mi></munder><msub><mi>J</mi><mtext>explicit</mtext></msub><mo>(</mo><mi>&theta;</mi><mo>)</mo><mo>,</mo>
  <mspace width="1em"></mspace>
  <msub><mo>&nabla;</mo><mi>&theta;</mi></msub><msub><mi>J</mi><mtext>DSM</mtext></msub>
  <mo>=</mo><msub><mo>&nabla;</mo><mi>&theta;</mi></msub><msub><mi>J</mi><mtext>explicit</mtext></msub><mo>.</mo>
</math>

이것이 “두 loss가 equivalent하다”는 말의 정확한 의미다. 두 loss의 수치가 같을 필요는 없다. Denoising objective에는 제거할 수 없는 target variance가 포함되므로 일반적으로 상수만큼 더 크다. 같은 것은 <math><mi>&theta;</mi></math>에 대한 optimization problem이다.

## 학습된 벡터가 Denoising Direction인 이유

Gaussian corruption의 conditional score를 기대값 항등식에 대입하면 다음과 같다.

<math display="block" aria-label="Marginal score under Gaussian corruption">
  <msup><mi>s</mi><mo>*</mo></msup><mo>(</mo><mover><mi>x</mi><mo>~</mo></mover><mo>)</mo>
  <mo>=</mo><msub><mi mathvariant="double-struck">E</mi><mrow><mi>x</mi><mo>|</mo><mover><mi>x</mi><mo>~</mo></mover></mrow></msub>
  <mrow><mo>[</mo><mfrac><mrow><mi>x</mi><mo>&minus;</mo><mover><mi>x</mi><mo>~</mo></mover></mrow><msup><mi>&sigma;</mi><mn>2</mn></msup></mfrac><mo>]</mo></mrow><mo>.</mo>
</math>

이를 정리하면

<math display="block" aria-label="Posterior mean denoising identity">
  <mi mathvariant="double-struck">E</mi><mo>[</mo><mi>x</mi><mo>|</mo><mover><mi>x</mi><mo>~</mo></mover><mo>]</mo>
  <mo>=</mo><mover><mi>x</mi><mo>~</mo></mover><mo>+</mo><msup><mi>&sigma;</mi><mn>2</mn></msup>
  <msup><mi>s</mi><mo>*</mo></msup><mo>(</mo><mover><mi>x</mi><mo>~</mo></mover><mo>)</mo><mo>.</mo>
</math>

즉 score correction은 noisy point를 clean sample의 posterior mean 쪽으로 이동시킨다. 이는 모든 score vector가 하나의 원본 데이터로 돌아간다는 설명보다 정확하다. 여러 clean explanation이 가능하면 학습된 벡터는 corruption process가 만드는 posterior probability에 따라 그 방향들을 평균한다.

이 평균화가 sample-wise training이 작동하는 이유이기도 하다. 각 training pair는 하나의 clean sample을 향하는 target을 제공한다. 많은 pair에 대한 squared-error regression은 그 target들의 conditional mean을 추정한다. 그리고 그 conditional mean이 marginal score이다. 따라서 denoising supervision은 score learning을 대신하는 heuristic이 아니다. 명시한 조건 아래에서 같은 parameter optimization problem을 계산 가능한 회귀 문제로 바꾼 것이다.

주장의 범위는 좁게 유지해야 한다. 이 등가성은 유한한 neural network가 population optimum에 도달한다는 뜻이 아니다. 모든 구현에서 finite-sample training이 unbiased라는 뜻도 아니며, optimization이 global minimizer를 찾는다는 보장도 아니다. Population objective 수준에서 marginal score를 conditional corruption score로 바꾸면 loss가 parameter-independent constant만큼 변한다는 뜻이다. 이것이 핵심 등가성이다.

## Reference

**Stanford CME296 Diffusion & Large Vision Models | Spring 2026 | Lecture 2 - Score matching**
