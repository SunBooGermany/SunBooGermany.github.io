---
layout: post
title: "CAffNet: Hard Constraint-Affine Neural Networks"
title_ko: "CAffNet: 하드 제약을 구조적으로 만족시키는 신경망"
date: 2026-09-06
category: safe-constrained-rl
category_label: "Safe & Constrained RL"
research_group: algorithmic_reviews
research_category: safe-constrained-rl
research_category_label: "Safe & Constrained RL"
application_category: ""
application_category_label: ""
method_category: "safe-constrained-rl"
method_category_label: "Safe & Constrained RL"
paper_title: "CAffNet: Hard Constraint-Affine Neural Networks"
authors: "Yang Zhao, Jungeun Lee, Jeong Hwan Jeon, and Sze Zheng Yong"
venue: "ICML"
year: "2026"
doi: ""
arxiv: ""
source_url: ""
tags:
  - "safe-rl"
  - "safe-control"
  - "hard-constraints"
  - "control-barrier-functions"
  - "constrained-learning"
excerpt: "CAffNet embeds input-dependent affine constraints in a neural output layer. It guarantees feasibility for known nonempty constraint sets, but its combinatorial active-set cost and model-dependent safety assumptions remain central limitations."
excerpt_ko: "CAffNet은 입력 의존 affine 제약을 신경망 출력층에 삽입한다. 알려진 비공집합 제약집합에 대해서는 feasibility를 보장하지만, 조합적 active-set 비용과 모델 정확성에 의존하는 안전 가정은 여전히 핵심 한계다."
language: "en-ko"
has_korean_note: false
---

## A hard constraint layer is not the same as a safe system

Many control policies can be trained to reduce constraint violations. That is not enough when one violation is unacceptable. A robot action, a process-control input, or an RL policy may have to satisfy a state-dependent set of affine inequalities at every inference step:

<math display="block" aria-label="Input dependent affine constraint">
  <mi>A</mi><mo>(</mo><mi>x</mi><mo>)</mo><mi>y</mi><mo>&le;</mo><mi>b</mi><mo>(</mo><mi>x</mi><mo>)</mo><mo>,</mo>
  <mspace width="0.7em"/><mi>y</mi><mo>=</mo><msub><mi>f</mi><mi>&theta;</mi></msub><mo>(</mo><mi>x</mi><mo>)</mo><mo>.</mo>
</math>

Here the allowable output changes with the current state <math><mi>x</mi></math>. In obstacle avoidance, for example, the set of safe control actions changes as the robot moves. A penalty loss can make violations rare, but it cannot make them impossible. An optimization layer can correct a proposed output, but may require an iterative solve at every forward pass.

CAffNet takes a different route. It puts the affine constraints into the output architecture itself. Its central result is a feasibility guarantee for arbitrary numbers of input-dependent affine constraints, without requiring the constraint matrix to have full row rank. This is a useful distinction from earlier hard-constraint architectures. It is also a narrow guarantee: the architecture enforces the constraints supplied to it, not every condition required for a physically safe closed loop.

## Why a fixed hard projection was not enough

Hard feasibility is not new. One natural earlier design is to let a network propose an unconstrained output and linearly project it back to the constraint boundary or feasible set. This is attractive because the correction is explicit: an infeasible point is replaced by a valid one.

The limitation is that a fixed projection rule makes a task decision using geometry alone. Suppose a safety boundary fixes one component of a control action but leaves another component free. Orthogonal projection preserves or changes that free component according to its fixed formula; it does not ask whether the resulting action tracks the goal, saves energy, or gives the controller room for a future maneuver. The correction can therefore discard useful degrees of freedom even while it removes violation.

There is a second limitation when the constraints depend on the input. Earlier hard-constraint affine architectures such as HardNet-Aff handle this setting under structural conditions, including a full-row-rank requirement on the constraint matrix and a restriction tied to the number of constraints. Real feasible action sets can have redundant or dependent constraints, and a low-dimensional action can be enclosed by many inequalities. Those are ordinary cases for polytopes, not pathological edge cases.

CAffNet is motivated by both failures. It seeks a hard-feasible layer that does not require full row rank or a small constraint count, while preserving a learnable direction along each candidate constraint face. The next two-dimensional example makes the distinction concrete.

## The picture to keep in mind

Consider a network that outputs two numbers, <math><mi>y</mi><mo>=</mo><mo>(</mo><msub><mi>y</mi><mn>1</mn></msub><mo>,</mo><msub><mi>y</mi><mn>2</mn></msub><mo>)</mo></math>, subject to

<math display="block" aria-label="Simple triangular feasible region">
  <msub><mi>y</mi><mn>1</mn></msub><mo>+</mo><msub><mi>y</mi><mn>2</mn></msub><mo>&le;</mo><mn>10</mn><mo>,</mo>
  <mspace width="0.5em"/><msub><mi>y</mi><mn>1</mn></msub><mo>&ge;</mo><mn>0</mn><mo>,</mo>
  <mspace width="0.5em"/><msub><mi>y</mi><mn>2</mn></msub><mo>&ge;</mo><mn>0</mn><mo>.</mo>
</math>

The allowable outputs form a triangle. An ordinary network can still propose a point outside it. A soft constraint says, in effect, “leaving the triangle will cost you in the loss.” Even a large penalty does not make violation impossible at inference time.

CAffNet instead follows a simple sequence:

<math display="block" aria-label="CAffNet output flow">
  <mtext>unconstrained neural prediction</mtext><mo>&rarr;</mo>
  <mtext>constraint-aware correction</mtext><mo>&rarr;</mo>
  <mtext>feasible output</mtext><mo>.</mo>
</math>

The network first proposes <math><mover><mi>y</mi><mo>^</mo></mover><mo>=</mo><msub><mi>f</mi><mi>&theta;</mi></msub><mo>(</mo><mi>x</mi><mo>)</mo></math>. If that proposal is outside the allowable region, the CAffNet layer returns a point inside it. Under the nonempty-feasible-set assumption, the final output satisfies the supplied affine constraints by construction.

This is not merely “project to the closest point.” A boundary contains many feasible points. A fixed geometric projection may choose one point, while another point on the same boundary may be much better for the task: a robot can be safe at both points, but only one may also move efficiently toward its goal. CAffNet's trainable null-space term lets learning choose along directions that do not change the active equality constraints. In that limited but useful sense, it learns not only how to correct an infeasible proposal, but where on a feasible face to place the corrected output.

The same picture explains the active-set construction. With many inequalities, a point on a two-dimensional polygon is usually determined by one active edge or two active edges at a vertex, not all of its walls. CAffNet builds candidates from small constraint subsets, tests those candidates against the full constraint set, and selects among the feasible ones. It is this combination—input-dependent constraints, rank-tolerant active-set candidates, and a trainable feasible direction—that is more distinctive than projection alone.

## Parameterizing candidate faces of a polyhedron

For a constraint subset <math><mi>&gamma;</mi></math>, let <math><msub><mi>A</mi><mi>&gamma;</mi></msub></math> and <math><msub><mi>b</mi><mi>&gamma;</mi></msub></math> denote the corresponding rows. CAffNet forms one candidate per subset,

<math display="block" aria-label="CAffNet constraint affine candidate">
  <msub><mi mathvariant="script">P</mi><mi>&gamma;</mi></msub><mo>(</mo><mi>x</mi><mo>)</mo>
  <mo>=</mo><msub><mi>f</mi><mi>&theta;</mi></msub>
  <mo>-</mo><msubsup><mi>A</mi><mi>&gamma;</mi><mo>&dagger;</mo></msubsup>
  <mo>(</mo><msub><mi>A</mi><mi>&gamma;</mi></msub><msub><mi>f</mi><mi>&theta;</mi></msub><mo>-</mo><msub><mi>b</mi><mi>&gamma;</mi></msub><mo>)</mo>
  <mo>+</mo><mo>(</mo><mi>I</mi><mo>-</mo><msubsup><mi>A</mi><mi>&gamma;</mi><mo>&dagger;</mo></msubsup><msub><mi>A</mi><mi>&gamma;</mi></msub><mo>)</mo><msub><mi>w</mi><mi>&phi;</mi></msub><mo>.</mo>
</math>

The first two terms project the nominal network output <math><msub><mi>f</mi><mi>&theta;</mi></msub></math> onto the equality face <math><msub><mi>A</mi><mi>&gamma;</mi></msub><mi>y</mi><mo>=</mo><msub><mi>b</mi><mi>&gamma;</mi></msub></math>. The last term is the more interesting part. It lies in the null space of <math><msub><mi>A</mi><mi>&gamma;</mi></msub></math>, so it can move along that face without breaking its equality constraints. A second network <math><msub><mi>w</mi><mi>&phi;</mi></msub></math> learns this remaining freedom from the task loss.

This avoids a limitation of a fixed orthogonal projection. If the only equality is <math><msub><mi>y</mi><mn>2</mn></msub><mo>=</mo><mn>0</mn></math>, projecting <math><mo>(</mo><mn>3</mn><mo>,</mo><mn>2</mn><mo>)</mo></math> gives <math><mo>(</mo><mn>3</mn><mo>,</mo><mn>0</mn><mo>)</mo></math>. But every point <math><mo>(</mo><mi>z</mi><mo>,</mo><mn>0</mn><mo>)</mo></math> is feasible. CAffNet can learn a useful <math><mi>z</mi></math> while maintaining the equality.

The architecture checks each candidate against all inequalities and retains only feasible candidates. If the nominal output is feasible it is returned unchanged; otherwise the architecture selects a feasible candidate closest to it. It enumerates subsets of cardinality up to the output dimension. The number of candidates is

<math display="block" aria-label="Number of active constraint subsets">
  <mrow><mo>&sum;</mo><mrow><mi>k</mi><mo>=</mo><mn>1</mn></mrow><mrow><mi>min</mi><mo>(</mo><mi>m</mi><mo>,</mo><msub><mi>n</mi><mtext>out</mtext></msub><mo>)</mo></mrow></mrow>
  <mrow><mo>(</mo><mfrac><mi>m</mi><mi>k</mi></mfrac><mo>)</mo></mrow><mo>.</mo>
</math>

The geometry is natural: a projection onto a polyhedron lies on a face described by a linearly independent active set, and no more than <math><msub><mi>n</mi><mtext>out</mtext></msub></math> independent constraints are needed. The cost is also immediate. The method removes an iterative solver, but it replaces it with active-set enumeration.

## What the theorem actually establishes

Assume that the polyhedron

<math display="block" aria-label="Feasible set">
  <mi mathvariant="script">S</mi><mo>(</mo><mi>x</mi><mo>)</mo><mo>=</mo><mo>{</mo><mi>y</mi><mo>:</mo><mi>A</mi><mo>(</mo><mi>x</mi><mo>)</mo><mi>y</mi><mo>&le;</mo><mi>b</mi><mo>(</mo><mi>x</mi><mo>)</mo><mo>}</mo>
</math>

is nonempty for every input. CAffNet argues that at least one enumerated face candidate is feasible. Selecting only among feasible candidates then gives

<math display="block" aria-label="CAffNet hard feasibility">
  <mi>A</mi><mo>(</mo><mi>x</mi><mo>)</mo><msup><mi mathvariant="script">P</mi><mo>*</mo></msup><mo>(</mo><mi>x</mi><mo>)</mo><mo>&le;</mo><mi>b</mi><mo>(</mo><mi>x</mi><mo>)</mo><mo>.</mo>
</math>

This is the paper's strongest result. It is an inference-time feasibility statement, not an empirical tendency toward lower violation. The assumptions matter. If the controller uses estimated constraints <math><mover><mi>A</mi><mo>^</mo></mover></math> and <math><mover><mi>b</mi><mo>^</mo></mover></math>, it guarantees only <math><mover><mi>A</mi><mo>^</mo></mover><mi>y</mi><mo>&le;</mo><mover><mi>b</mi><mo>^</mo></mover></math>. It does not prove that the true plant constraint is satisfied when the model is wrong, a constraint is missing, or the deployment state lies outside the modeled regime.

The paper also claims universal approximation over feasible targets when the underlying unconstrained network class is universal. The claim is plausible, but the appendix proof needs care. Its comparison uses a selected boundary candidate as though it were already in the feasible-candidate set; equality on one chosen face alone does not ensure all other inequalities. The argument also moves from an <math><msup><mi>L</mi><mi>p</mi></msup></math> approximation statement to a pointwise inequality, which does not follow without additional conditions. These issues do not refute the feasibility theorem. They do mean the universal-approximation proof, as written, is less complete than the hard-feasibility result.

## Why this fits safe control, and where it stops

Control Barrier Functions often give a constraint affine in the control input <math><mi>u</mi></math>:

<math display="block" aria-label="Control barrier function inequality">
  <msub><mi>L</mi><mi>f</mi></msub><mi>h</mi><mo>(</mo><mi>x</mi><mo>)</mo><mo>+</mo><msub><mi>L</mi><mi>g</mi></msub><mi>h</mi><mo>(</mo><mi>x</mi><mo>)</mo><mi>u</mi>
  <mo>&ge;</mo><mo>-</mo><mi>&alpha;</mi><mo>(</mo><mi>h</mi><mo>(</mo><mi>x</mi><mo>)</mo><mo>)</mo><mo>.</mo>
</math>

After rearrangement, this is exactly the form CAffNet accepts. A learned policy can propose an action while the output layer returns an action satisfying the modeled CBF inequality. That is a clean interface between a learned policy and a constraint-defined safety filter.

It should not be called a complete physical safety guarantee. To convert CBF feasibility into closed-loop safety, the dynamics, barrier function, safe initial condition, and sampled-data implementation must all satisfy their own assumptions. Actuator limits can make the combined CBF and hardware constraints infeasible, especially near an obstacle. CAffNet assumes a nonempty action-feasible set precisely where a real controller may fail to have one.

## Solver-free does not mean inexpensive

The paper reports a large training-time gap in its small solver-learning experiment: CAffNet-FF takes roughly 1,325 ms per epoch, compared with 4.27 ms for an unconstrained neural network. CAffNet-Lite reduces the enumeration, but the full method's general feasibility proof does not automatically transfer to every restricted subset rule.

The experiments show that the architecture can produce zero reported constraint violation in toy regression, a feasible optimizer in a low-dimensional learning problem, and collision-free behavior in one unicycle-control demonstration. They do not show that CAffNet is generally more accurate, cheaper, or ready for high-dimensional real-time control. In the solver-learning experiment, the Transformer variant has much worse objective value than the feed-forward version. The control evaluation is also narrow relative to a safety-generalization benchmark.

The useful position is therefore precise. CAffNet is a hard-feasible neural output layer for known input-dependent affine constraints. Its active-face construction and trainable null-space term are genuinely useful ideas. Its safety claim ends at the correctness and feasibility of those modeled constraints; beyond that boundary, model uncertainty, discretization, missing hazards, and computational scaling remain separate problems.

## Reference

Yang Zhao, Jungeun Lee, Jeong Hwan Jeon, and Sze Zheng Yong. *CAffNet: Hard Constraint-Affine Neural Networks*. ICML, 2026. Source URL was not provided with the reviewed material.

<!-- ko -->

## 하드 제약층은 안전한 시스템 그 자체가 아니다

많은 제어 정책은 constraint violation을 줄이도록 학습할 수 있다. 하지만 한 번의 위반도 허용할 수 없는 문제에서는 그것으로 부족하다. 로봇의 action, 공정 제어 입력, RL policy는 매 inference step마다 상태 의존적인 affine inequality를 만족해야 할 수 있다.

<math display="block" aria-label="입력 의존 affine 제약">
  <mi>A</mi><mo>(</mo><mi>x</mi><mo>)</mo><mi>y</mi><mo>&le;</mo><mi>b</mi><mo>(</mo><mi>x</mi><mo>)</mo><mo>,</mo>
  <mspace width="0.7em"/><mi>y</mi><mo>=</mo><msub><mi>f</mi><mi>&theta;</mi></msub><mo>(</mo><mi>x</mi><mo>)</mo><mo>.</mo>
</math>

여기서 허용되는 출력은 현재 상태 <math><mi>x</mi></math>에 따라 달라진다. 예를 들어 obstacle avoidance에서는 로봇이 움직일수록 안전한 control action의 집합이 바뀐다. Penalty loss는 위반을 드물게 만들 수 있지만 불가능하게 만들지는 못한다. Optimization layer는 제안된 출력을 보정할 수 있지만 매 forward pass마다 반복 solve가 필요할 수 있다.

CAffNet은 다른 길을 택한다. Affine constraint를 output architecture 자체에 넣는다. 핵심 결과는 constraint matrix가 full row rank일 필요 없이, 임의 개수의 input-dependent affine constraint에 대해 feasibility를 보장한다는 것이다. 이는 기존 hard-constraint architecture와 구별되는 장점이다. 동시에 좁은 보장이다. Architecture는 주어진 constraint를 만족시킬 뿐, 실제 폐루프 시스템에 필요한 모든 물리적 안전 조건을 보장하지는 않는다.

## 고정된 hard projection만으로는 왜 부족했나

Hard feasibility 자체가 새로운 것은 아니다. 자연스러운 기존 설계는 network가 unconstrained output을 제안하면 이를 linear projection으로 constraint boundary 또는 feasible set 안으로 되돌리는 방식이다. Infeasible point를 valid point로 바꾸므로 correction이 명시적이라는 장점이 있다.

한계는 고정된 projection rule이 geometry만으로 task decision까지 내린다는 데 있다. Safety boundary가 control action의 한 component를 고정하지만 다른 component는 자유롭게 남긴다고 하자. Orthogonal projection은 고정된 수식에 따라 그 자유 component를 보존하거나 바꾼다. 그 결과가 goal tracking, energy use, 다음 maneuver의 여유에 좋은지 묻지 않는다. 따라서 violation은 제거해도 task에 유용한 degree of freedom을 버릴 수 있다.

Input-dependent constraint에서는 두 번째 한계가 있다. HardNet-Aff 같은 기존 hard-constraint affine architecture는 constraint matrix의 full-row-rank와 constraint 수에 연결된 구조적 조건 아래에서 이 문제를 다룬다. 그러나 실제 feasible action set에는 redundant하거나 dependent한 constraint가 있을 수 있고, 낮은 차원의 action도 많은 inequality로 둘러싸일 수 있다. 이는 polytope에서 예외적 상황이 아니라 흔한 경우다.

CAffNet은 이 두 한계에서 출발한다. Full row rank나 작은 constraint count를 요구하지 않는 hard-feasible layer를 만들면서, candidate constraint face를 따라 학습 가능한 방향을 남기려 한다. 다음 2차원 예시가 그 차이를 구체적으로 보여 준다.

## 머릿속에 남겨 둘 그림

두 숫자를 출력하는 network를 생각해 보자. 출력은 <math><mi>y</mi><mo>=</mo><mo>(</mo><msub><mi>y</mi><mn>1</mn></msub><mo>,</mo><msub><mi>y</mi><mn>2</mn></msub><mo>)</mo></math>이고, 다음을 만족해야 한다.

<math display="block" aria-label="간단한 삼각형 feasible region">
  <msub><mi>y</mi><mn>1</mn></msub><mo>+</mo><msub><mi>y</mi><mn>2</mn></msub><mo>&le;</mo><mn>10</mn><mo>,</mo>
  <mspace width="0.5em"/><msub><mi>y</mi><mn>1</mn></msub><mo>&ge;</mo><mn>0</mn><mo>,</mo>
  <mspace width="0.5em"/><msub><mi>y</mi><mn>2</mn></msub><mo>&ge;</mo><mn>0</mn><mo>.</mo>
</math>

허용되는 출력은 삼각형을 이룬다. 그렇다고 일반 network가 그 바깥의 점을 내지 않는 것은 아니다. Soft constraint는 사실상 “삼각형 밖으로 나가면 loss에서 대가를 치르게 하겠다”는 방식이다. Penalty가 아주 커도 inference-time violation을 불가능하게 만들지는 못한다.

CAffNet은 대신 다음 순서를 따른다.

<math display="block" aria-label="CAffNet 출력 흐름">
  <mtext>unconstrained neural prediction</mtext><mo>&rarr;</mo>
  <mtext>constraint-aware correction</mtext><mo>&rarr;</mo>
  <mtext>feasible output</mtext><mo>.</mo>
</math>

Network가 먼저 <math><mover><mi>y</mi><mo>^</mo></mover><mo>=</mo><msub><mi>f</mi><mi>&theta;</mi></msub><mo>(</mo><mi>x</mi><mo>)</mo></math>를 제안한다. 이 제안이 허용 영역 밖이면 CAffNet layer가 영역 안의 점을 반환한다. Feasible set이 nonempty라는 가정 아래, 최종 출력은 주어진 affine constraint를 구조적으로 만족한다.

이것은 단순히 “가장 가까운 점으로 projection한다”는 말보다 넓다. Boundary 위에는 feasible point가 많다. 고정된 geometric projection은 그중 하나를 선택하지만, 같은 boundary 위의 다른 점이 task에는 훨씬 나을 수 있다. 로봇은 두 점에서 모두 안전할 수 있지만 그중 하나에서만 목표로 효율적으로 갈 수 있다. CAffNet의 trainable null-space term은 active equality constraint를 바꾸지 않는 방향에서 학습하게 한다. 제한적이지만 유용한 의미에서, infeasible proposal을 보정하는 방법뿐 아니라 feasible face 위에서 어디에 보정된 출력을 놓을지도 학습한다.

이 그림은 active-set construction도 설명한다. Inequality가 많아도 2차원 polygon의 점은 보통 모든 벽이 아니라 active edge 하나, 또는 vertex에서 만나는 두 edge로 정해진다. CAffNet은 작은 constraint subset으로 candidate를 만들고, 전체 constraint set으로 다시 검사한 뒤 feasible candidate 중 하나를 선택한다. Input-dependent constraint, rank에 덜 민감한 active-set candidate, trainable feasible direction의 조합이 이 논문을 단순 projection보다 더 특징짓는다.

## Polyhedron의 candidate face를 parameterize한다

Constraint subset <math><mi>&gamma;</mi></math>에 대해 해당 행을 <math><msub><mi>A</mi><mi>&gamma;</mi></msub></math>, <math><msub><mi>b</mi><mi>&gamma;</mi></msub></math>라고 쓰자. CAffNet은 subset마다 다음 후보를 만든다.

<math display="block" aria-label="CAffNet 제약 affine 후보">
  <msub><mi mathvariant="script">P</mi><mi>&gamma;</mi></msub><mo>(</mo><mi>x</mi><mo>)</mo>
  <mo>=</mo><msub><mi>f</mi><mi>&theta;</mi></msub>
  <mo>-</mo><msubsup><mi>A</mi><mi>&gamma;</mi><mo>&dagger;</mo></msubsup>
  <mo>(</mo><msub><mi>A</mi><mi>&gamma;</mi></msub><msub><mi>f</mi><mi>&theta;</mi></msub><mo>-</mo><msub><mi>b</mi><mi>&gamma;</mi></msub><mo>)</mo>
  <mo>+</mo><mo>(</mo><mi>I</mi><mo>-</mo><msubsup><mi>A</mi><mi>&gamma;</mi><mo>&dagger;</mo></msubsup><msub><mi>A</mi><mi>&gamma;</mi></msub><mo>)</mo><msub><mi>w</mi><mi>&phi;</mi></msub><mo>.</mo>
</math>

앞의 두 항은 nominal network output <math><msub><mi>f</mi><mi>&theta;</mi></msub></math>를 equality face <math><msub><mi>A</mi><mi>&gamma;</mi></msub><mi>y</mi><mo>=</mo><msub><mi>b</mi><mi>&gamma;</mi></msub></math>로 projection한다. 더 흥미로운 것은 마지막 항이다. 이는 <math><msub><mi>A</mi><mi>&gamma;</mi></msub></math>의 null space에 있으므로 equality constraint를 깨지 않고 face 위에서 움직일 수 있다. 두 번째 network <math><msub><mi>w</mi><mi>&phi;</mi></msub></math>가 task loss를 통해 이 자유도를 학습한다.

이는 고정된 orthogonal projection의 한계를 피한다. Equality가 <math><msub><mi>y</mi><mn>2</mn></msub><mo>=</mo><mn>0</mn></math> 하나뿐이라면 <math><mo>(</mo><mn>3</mn><mo>,</mo><mn>2</mn><mo>)</mo></math>의 projection은 <math><mo>(</mo><mn>3</mn><mo>,</mo><mn>0</mn><mo>)</mo></math>이다. 그러나 <math><mo>(</mo><mi>z</mi><mo>,</mo><mn>0</mn><mo>)</mo></math>의 모든 점은 feasible하다. CAffNet은 constraint를 유지하면서 task에 유용한 <math><mi>z</mi></math>를 학습할 수 있다.

Architecture는 모든 inequality로 각 후보를 검사하고 feasible candidate만 남긴다. Nominal output이 feasible하면 그대로 반환하고, 그렇지 않으면 가장 가까운 feasible candidate를 고른다. Output dimension 이하의 cardinality를 가진 subset을 모두 열거한다. 후보 수는 다음과 같다.

<math display="block" aria-label="Active constraint subset 수">
  <mrow><mo>&sum;</mo><mrow><mi>k</mi><mo>=</mo><mn>1</mn></mrow><mrow><mi>min</mi><mo>(</mo><mi>m</mi><mo>,</mo><msub><mi>n</mi><mtext>out</mtext></msub><mo>)</mo></mrow></mrow>
  <mrow><mo>(</mo><mfrac><mi>m</mi><mi>k</mi></mfrac><mo>)</mo></mrow><mo>.</mo>
</math>

기하학적으로 자연스럽다. Polyhedron으로의 projection은 active set이 정의하는 face에 놓이고, 필요한 independent constraint 수는 output dimension을 넘지 않는다. 비용도 즉시 드러난다. 이 방법은 iterative solver를 없애지만 active-set enumeration으로 바꾼다.

## Theorem이 실제로 보이는 것

다음 polyhedron이 모든 입력에서 nonempty하다고 가정하자.

<math display="block" aria-label="Feasible set">
  <mi mathvariant="script">S</mi><mo>(</mo><mi>x</mi><mo>)</mo><mo>=</mo><mo>{</mo><mi>y</mi><mo>:</mo><mi>A</mi><mo>(</mo><mi>x</mi><mo>)</mo><mi>y</mi><mo>&le;</mo><mi>b</mi><mo>(</mo><mi>x</mi><mo>)</mo><mo>}</mo>
</math>

CAffNet은 열거된 face candidate 중 적어도 하나가 feasible함을 보인다. Feasible candidate에서만 최종 선택을 하므로 다음을 얻는다.

<math display="block" aria-label="CAffNet 하드 feasibility">
  <mi>A</mi><mo>(</mo><mi>x</mi><mo>)</mo><msup><mi mathvariant="script">P</mi><mo>*</mo></msup><mo>(</mo><mi>x</mi><mo>)</mo><mo>&le;</mo><mi>b</mi><mo>(</mo><mi>x</mi><mo>)</mo><mo>.</mo>
</math>

이것이 논문의 가장 강한 결과다. Penalty 때문에 violation이 줄어든다는 경험적 경향이 아니라 inference-time feasibility statement다. 가정이 중요하다. Controller가 estimate constraint <math><mover><mi>A</mi><mo>^</mo></mover></math>, <math><mover><mi>b</mi><mo>^</mo></mover></math>를 쓴다면 보장하는 것은 <math><mover><mi>A</mi><mo>^</mo></mover><mi>y</mi><mo>&le;</mo><mover><mi>b</mi><mo>^</mo></mover></math>뿐이다. 모델이 틀리거나 constraint가 빠졌거나 deployment state가 modeled regime 밖에 있을 때 true plant constraint까지 만족한다는 증명은 아니다.

논문은 underlying unconstrained network class가 universal하면 feasible target에 대해서도 universal approximation이 유지된다고 주장한다. Claim은 plausible하지만 appendix proof는 주의가 필요하다. 선택한 boundary candidate를 feasible-candidate set 안에 이미 들어 있는 것처럼 비교하는데, 하나의 face equality를 만족한다고 다른 inequality까지 만족하는 것은 아니다. 또 <math><msup><mi>L</mi><mi>p</mi></msup></math> approximation statement를 pointwise inequality로 옮기는 부분도 추가 조건 없이는 바로 따라오지 않는다. 이 문제들이 feasibility theorem을 반박하는 것은 아니다. 다만 universal-approximation proof는 hard-feasibility result보다 덜 완결적이다.

## Safe control에 맞는 이유와 멈추는 지점

Control Barrier Function은 control input <math><mi>u</mi></math>에 대해 흔히 affine constraint를 준다.

<math display="block" aria-label="Control Barrier Function 부등식">
  <msub><mi>L</mi><mi>f</mi></msub><mi>h</mi><mo>(</mo><mi>x</mi><mo>)</mo><mo>+</mo><msub><mi>L</mi><mi>g</mi></msub><mi>h</mi><mo>(</mo><mi>x</mi><mo>)</mo><mi>u</mi>
  <mo>&ge;</mo><mo>-</mo><mi>&alpha;</mi><mo>(</mo><mi>h</mi><mo>(</mo><mi>x</mi><mo>)</mo><mo>)</mo><mo>.</mo>
</math>

이를 정리하면 CAffNet이 받는 형태가 된다. Learned policy가 action을 제안하면 output layer가 modeled CBF inequality를 만족하는 action을 반환하는 구조다. Learned policy와 constraint-defined safety filter를 연결하는 깔끔한 interface다.

그러나 이를 complete physical safety guarantee라고 부르면 안 된다. CBF feasibility를 closed-loop safety로 연결하려면 dynamics, barrier function, safe initial condition, sampled-data implementation이 각각의 가정을 만족해야 한다. 특히 obstacle 근처에서는 actuator limit 때문에 CBF와 hardware constraint를 동시에 만족하는 입력이 없을 수 있다. 실제 controller가 action을 찾지 못할 수 있는 지점에서 CAffNet은 nonempty action-feasible set을 가정한다.

## Solver-free는 inexpensive가 아니다

논문은 작은 solver-learning experiment에서 큰 training-time 차이를 보고한다. CAffNet-FF는 epoch당 약 1,325 ms가 걸리고 unconstrained neural network는 4.27 ms다. CAffNet-Lite는 enumeration을 줄이지만, full method의 일반 feasibility proof가 모든 restricted subset rule에 자동으로 적용되지는 않는다.

실험은 toy regression에서 zero reported constraint violation, low-dimensional learning problem에서 feasible optimizer, unicycle-control demonstration에서 collision-free behavior를 보여 준다. 그러나 CAffNet이 일반적으로 더 정확하거나, 더 싸거나, high-dimensional real-time control에 준비됐다는 증거는 아니다. Solver-learning experiment에서는 Transformer variant의 objective value가 feed-forward version보다 훨씬 나쁘다. Control evaluation도 safety-generalization benchmark로 보기에는 좁다.

따라서 정확한 위치는 다음과 같다. CAffNet은 알려진 input-dependent affine constraint를 위한 hard-feasible neural output layer다. Active-face construction과 trainable null-space term은 유용한 아이디어다. 안전 주장은 modeled constraint의 정확성과 feasibility에서 끝난다. 그 경계 바깥의 model uncertainty, discretization, missing hazard, computational scaling은 별도의 문제로 남는다.

## 참고문헌

Yang Zhao, Jungeun Lee, Jeong Hwan Jeon, and Sze Zheng Yong. *CAffNet: Hard Constraint-Affine Neural Networks*. ICML, 2026. 검토에 사용한 자료에는 source URL이 제공되지 않았다.
