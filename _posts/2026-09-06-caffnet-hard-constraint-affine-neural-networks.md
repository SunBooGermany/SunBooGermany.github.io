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
excerpt: "CAffNet builds input-dependent affine constraints into a neural output layer. It guarantees constraint satisfaction when the supplied feasible set is nonempty. Enumerating active constraint combinations can be costly, and physical safety still depends on the accuracy of the constraint model."
excerpt_ko: "CAffNet은 입력에 따라 달라지는 아핀 제약을 신경망 출력층에 넣는다. 주어진 제약을 만족하는 출력이 존재하면 제약 만족을 보장한다. 다만 활성 제약 조합을 열거하는 비용이 크고, 물리적 안전은 제약 모델의 정확성에 달려 있다."
language: "en-ko"
has_korean_note: false
---

## Hard constraints that change with the state

Control policies can be trained to violate constraints less often. Some problems require every output to satisfy them. A robot action, a process-control input, or the action returned by an RL policy may need to satisfy a set of affine inequalities that changes with the state at each inference step:

<math display="block" aria-label="Input dependent affine constraint">
  <mi>A</mi><mo>(</mo><mi>x</mi><mo>)</mo><mi>y</mi><mo>&le;</mo><mi>b</mi><mo>(</mo><mi>x</mi><mo>)</mo><mo>,</mo>
  <mspace width="0.7em"/><mi>y</mi><mo>=</mo><msub><mi>f</mi><mi>&theta;</mi></msub><mo>(</mo><mi>x</mi><mo>)</mo><mo>.</mo>
</math>

The allowable output depends on the current state <math><mi>x</mi></math>. During obstacle avoidance, the set of safe control actions changes as the robot moves. A penalty loss can reduce violations without ruling them out. An optimization layer can correct a proposed output, though it may need an iterative solve on every forward pass.

CAffNet builds the affine constraints into the output architecture. If a feasible output exists, it guarantees constraint satisfaction for an arbitrary number of input-dependent affine constraints. The constraint matrix need not have full row rank, a useful distinction from earlier hard-constraint architectures. The guarantee covers the supplied constraints; physical closed-loop safety requires further conditions.

## Limits of fixed projection

An earlier approach to hard constraints is to let a network propose an unconstrained output and then use linear projection to bring it to a constraint boundary or feasible set. The correction is explicit: an infeasible point is replaced with a feasible one.

A fixed projection rule makes a task decision from geometry alone. Suppose a safety boundary fixes one component of a control input while leaving another free. Orthogonal projection retains or changes the free component according to its fixed formula. It does not account for goal tracking, energy use, or room for a future maneuver. The correction can remove a violation while discarding freedom that would be useful for the task.

Input-dependent constraints bring another limitation. Earlier affine hard-constraint architectures such as HardNet-Aff require structural conditions, including full row rank of the constraint matrix and a condition on the number of constraints. Actual feasible action sets can contain redundant or dependent constraints, and a low-dimensional action can be enclosed by many inequalities. These are common configurations for polytopes.

CAffNet aims to enforce constraints without requiring full row rank or a small constraint count, while retaining a learnable direction along each candidate face.

## A triangular feasible set

Consider a network that outputs two values, <math><mi>y</mi><mo>=</mo><mo>(</mo><msub><mi>y</mi><mn>1</mn></msub><mo>,</mo><msub><mi>y</mi><mn>2</mn></msub><mo>)</mo></math>, subject to the following constraints:

<math display="block" aria-label="Simple triangular feasible region">
  <msub><mi>y</mi><mn>1</mn></msub><mo>+</mo><msub><mi>y</mi><mn>2</mn></msub><mo>&le;</mo><mn>10</mn><mo>,</mo>
  <mspace width="0.5em"/><msub><mi>y</mi><mn>1</mn></msub><mo>&ge;</mo><mn>0</mn><mo>,</mo>
  <mspace width="0.5em"/><msub><mi>y</mi><mn>2</mn></msub><mo>&ge;</mo><mn>0</mn><mo>.</mo>
</math>

The outputs satisfying these inequalities form a triangle. An ordinary network can propose a point outside it. A soft constraint penalizes such an output in the loss, but a large penalty still does not rule out violations at inference time.

CAffNet processes the output as follows:

<math display="block" aria-label="CAffNet output flow">
  <mtext>unconstrained neural prediction</mtext><mo>&rarr;</mo>
  <mtext>constraint-aware correction</mtext><mo>&rarr;</mo>
  <mtext>feasible output</mtext><mo>.</mo>
</math>

The network first proposes <math><mover><mi>y</mi><mo>^</mo></mover><mo>=</mo><msub><mi>f</mi><mi>&theta;</mi></msub><mo>(</mo><mi>x</mi><mo>)</mo></math>. If this output lies outside the allowable region, the CAffNet layer returns a point inside it. Assuming a nonempty feasible set, the final output satisfies the supplied affine constraints by construction.

A boundary can contain many feasible points. A different point on the same boundary may serve the task better than the one chosen by a fixed geometric projection. A robot might be safe at both points yet move efficiently toward its goal at only one of them. CAffNet's trainable null-space term learns along directions that preserve the active equality constraints. Within this freedom, it can learn both how to correct an infeasible proposal and where on a face to place the corrected output.

Many inequalities need not all be active at once. A point on the boundary of a two-dimensional polygon usually lies on one edge or at a vertex where two edges meet. CAffNet constructs candidates from small constraint subsets, tests them against the full constraint set, and selects a feasible candidate. Combining input-dependent constraints, active-set candidates with fewer rank restrictions, and a trainable null-space direction distinguishes this construction from fixed projection.

## Constructing candidates on polyhedral faces

Let <math><mi>&gamma;</mi></math> be a subset of constraints, with corresponding rows <math><msub><mi>A</mi><mi>&gamma;</mi></msub></math> and <math><msub><mi>b</mi><mi>&gamma;</mi></msub></math>. CAffNet constructs a candidate for each subset:

<math display="block" aria-label="CAffNet constraint affine candidate">
  <msub><mi mathvariant="script">P</mi><mi>&gamma;</mi></msub><mo>(</mo><mi>x</mi><mo>)</mo>
  <mo>=</mo><msub><mi>f</mi><mi>&theta;</mi></msub>
  <mo>-</mo><msubsup><mi>A</mi><mi>&gamma;</mi><mo>&dagger;</mo></msubsup>
  <mo>(</mo><msub><mi>A</mi><mi>&gamma;</mi></msub><msub><mi>f</mi><mi>&theta;</mi></msub><mo>-</mo><msub><mi>b</mi><mi>&gamma;</mi></msub><mo>)</mo>
  <mo>+</mo><mo>(</mo><mi>I</mi><mo>-</mo><msubsup><mi>A</mi><mi>&gamma;</mi><mo>&dagger;</mo></msubsup><msub><mi>A</mi><mi>&gamma;</mi></msub><mo>)</mo><msub><mi>w</mi><mi>&phi;</mi></msub><mo>.</mo>
</math>

The first two terms project the nominal network output <math><msub><mi>f</mi><mi>&theta;</mi></msub></math> onto the equality face <math><msub><mi>A</mi><mi>&gamma;</mi></msub><mi>y</mi><mo>=</mo><msub><mi>b</mi><mi>&gamma;</mi></msub></math>. The last term lies in the null space of <math><msub><mi>A</mi><mi>&gamma;</mi></msub></math>, allowing movement along the face while preserving its equality constraints. A second network <math><msub><mi>w</mi><mi>&phi;</mi></msub></math> learns how to use that freedom through the task loss.

Consider the equality <math><msub><mi>y</mi><mn>2</mn></msub><mo>=</mo><mn>0</mn></math>. A fixed orthogonal projection maps <math><mo>(</mo><mn>3</mn><mo>,</mo><mn>2</mn><mo>)</mo></math> to <math><mo>(</mo><mn>3</mn><mo>,</mo><mn>0</mn><mo>)</mo></math>, although every point <math><mo>(</mo><mi>z</mi><mo>,</mo><mn>0</mn><mo>)</mo></math> satisfies the equality. CAffNet can learn a value of <math><mi>z</mi></math> that serves the task while keeping the output feasible.

Each candidate is checked against all inequalities. If the nominal output is feasible, the architecture returns it unchanged. Otherwise, it selects the closest feasible candidate. All constraint subsets with cardinality up to the output dimension are enumerated, giving the following candidate count:

<math display="block" aria-label="Number of active constraint subsets">
  <mrow><mo>&sum;</mo><mrow><mi>k</mi><mo>=</mo><mn>1</mn></mrow><mrow><mi>min</mi><mo>(</mo><mi>m</mi><mo>,</mo><msub><mi>n</mi><mtext>out</mtext></msub><mo>)</mo></mrow></mrow>
  <mrow><mo>(</mo><mfrac><mi>m</mi><mi>k</mi></mfrac><mo>)</mo></mrow><mo>.</mo>
</math>

A projection onto a polyhedron lies on a face described by linearly independent active constraints. At most <math><msub><mi>n</mi><mtext>out</mtext></msub></math> such constraints are needed, which explains the subset size limit. Enumerating those active sets carries a computational cost even though inference requires no iterative solver.

## The feasibility theorem and its assumptions

Assume that the following polyhedron is nonempty for every input:

<math display="block" aria-label="Feasible set">
  <mi mathvariant="script">S</mi><mo>(</mo><mi>x</mi><mo>)</mo><mo>=</mo><mo>{</mo><mi>y</mi><mo>:</mo><mi>A</mi><mo>(</mo><mi>x</mi><mo>)</mo><mi>y</mi><mo>&le;</mo><mi>b</mi><mo>(</mo><mi>x</mi><mo>)</mo><mo>}</mo>
</math>

The paper establishes that at least one enumerated face candidate is feasible. Selecting from the feasible candidates gives

<math display="block" aria-label="CAffNet hard feasibility">
  <mi>A</mi><mo>(</mo><mi>x</mi><mo>)</mo><msup><mi mathvariant="script">P</mi><mo>*</mo></msup><mo>(</mo><mi>x</mi><mo>)</mo><mo>&le;</mo><mi>b</mi><mo>(</mo><mi>x</mi><mo>)</mo><mo>.</mo>
</math>

This theorem is the paper's strongest result: it guarantees constraint satisfaction at inference time, beyond the empirical reduction in violations obtained with a penalty. Its scope depends on the supplied model. A controller using estimated constraints <math><mover><mi>A</mi><mo>^</mo></mover></math> and <math><mover><mi>b</mi><mo>^</mo></mover></math> guarantees only <math><mover><mi>A</mi><mo>^</mo></mover><mi>y</mi><mo>&le;</mo><mover><mi>b</mi><mo>^</mo></mover></math>. The true plant constraints may still be violated if the model is wrong, a constraint is missing, or the deployment state falls outside the modeled regime.

The paper also claims that universal approximation is preserved for feasible targets when the underlying unconstrained network class is universal. The claim is plausible, though the appendix proof leaves gaps. It compares against a selected boundary candidate as if that candidate were already feasible. Satisfying one face's equality does not ensure that the remaining inequalities hold. The proof also moves from an <math><msup><mi>L</mi><mi>p</mi></msup></math> approximation statement to a pointwise inequality without establishing the additional conditions needed for that step. These gaps do not refute the feasibility theorem, but they leave the universal-approximation argument less complete than the hard-feasibility result.

## Applying the layer to control barrier constraints

Control Barrier Functions (CBFs) often produce constraints affine in the control input <math><mi>u</mi></math>:

<math display="block" aria-label="Control barrier function inequality">
  <msub><mi>L</mi><mi>f</mi></msub><mi>h</mi><mo>(</mo><mi>x</mi><mo>)</mo><mo>+</mo><msub><mi>L</mi><mi>g</mi></msub><mi>h</mi><mo>(</mo><mi>x</mi><mo>)</mo><mi>u</mi>
  <mo>&ge;</mo><mo>-</mo><mi>&alpha;</mi><mo>(</mo><mi>h</mi><mo>(</mo><mi>x</mi><mo>)</mo><mo>)</mo><mo>.</mo>
</math>

Rearranging this inequality puts it in the form accepted by CAffNet. The policy proposes an action, and the output layer returns one satisfying the modeled CBF inequality. This lets the constraint layer serve as a safety filter for the learned policy.

Physical closed-loop safety requires the dynamics, barrier function, safe initial condition, and sampled-data implementation to satisfy their respective assumptions. CBF feasibility alone is insufficient. Near an obstacle, actuator limits may leave no input satisfying both the CBF and hardware constraints. CAffNet assumes a nonempty feasible action set even at states where an actual controller may have no feasible action.

## The cost of active-set enumeration

In the paper's small solver-learning experiment, CAffNet-FF takes roughly 1,325 ms per epoch, compared with 4.27 ms for an unconstrained neural network. This is a substantial training-time gap. CAffNet-Lite reduces the enumeration, though the full method's general feasibility proof does not automatically extend to every rule that restricts the enumerated subsets.

The reported results include zero constraint violation in toy regression, a feasible optimizer in a low-dimensional learning problem, and collision-free behavior in one unicycle-control demonstration. Evidence for broader accuracy, efficiency, or suitability for high-dimensional real-time control remains limited. In the solver-learning experiment, the Transformer variant has a much worse objective value than the feed-forward model. The control evaluation is also too narrow to establish how safety generalizes.

CAffNet provides a neural output layer that enforces known input-dependent affine constraints. Constructing candidates on active faces and learning the null-space freedom are useful ideas. Its safety guarantee depends on a correct constraint model and a nonempty feasible set. Model uncertainty, discretization, missing hazards, and computational scaling remain separate problems.

## Reference

Yang Zhao, Jungeun Lee, Jeong Hwan Jeon, and Sze Zheng Yong. *CAffNet: Hard Constraint-Affine Neural Networks*. ICML, 2026.

<!-- ko -->

## 상태에 따라 달라지는 하드 제약

제어 정책을 학습해 제약 위반을 줄일 수는 있다. 한 번의 위반도 허용할 수 없는 문제라면 매번 제약을 만족해야 한다. 로봇의 행동이나 공정 제어 입력, RL 정책이 내놓는 행동이 추론할 때마다 현재 상태에 따라 달라지는 아핀(affine) 부등식을 만족해야 하는 문제가 여기에 해당한다.

<math display="block" aria-label="입력 의존 affine 제약">
  <mi>A</mi><mo>(</mo><mi>x</mi><mo>)</mo><mi>y</mi><mo>&le;</mo><mi>b</mi><mo>(</mo><mi>x</mi><mo>)</mo><mo>,</mo>
  <mspace width="0.7em"/><mi>y</mi><mo>=</mo><msub><mi>f</mi><mi>&theta;</mi></msub><mo>(</mo><mi>x</mi><mo>)</mo><mo>.</mo>
</math>

허용되는 출력은 현재 상태 <math><mi>x</mi></math>에 따라 달라진다. 장애물을 피하는 로봇이라면 이동하면서 안전한 제어 입력의 집합도 바뀐다. 손실 함수에 벌점을 넣어 제약 위반을 줄일 수는 있지만, 위반을 완전히 막지는 못한다. 최적화층으로 출력을 보정하는 방법도 있으나 순전파 때마다 최적화 문제를 반복해서 풀어야 할 수 있다.

CAffNet은 아핀 제약을 출력층 구조에 넣는다. 제약을 만족하는 출력이 존재하면, 입력에 따라 달라지는 제약이 몇 개든 제약 만족을 보장한다. 제약 행렬의 모든 행이 선형 독립일 필요도 없다. 기존 하드 제약 신경망과 구별되는 장점이지만 보장 범위는 주어진 제약까지다. 실제 폐루프 시스템의 물리적 안전에는 추가 조건이 필요하다.

## 고정된 투영이 남기는 문제

기존 하드 제약 설계에서는 신경망이 제약을 고려하지 않은 출력을 제안하면, 선형 투영으로 제약 경계나 가능 집합 안으로 옮기는 방식을 사용한다. 제약을 위반하는 점을 제약을 만족하는 점으로 바꾸므로 보정 과정이 명시적이라는 장점이 있다.

고정된 투영 규칙은 기하학적 조건만으로 과제에 필요한 결정까지 내린다. 안전 경계가 제어 입력의 한 성분을 고정하고 다른 성분은 자유롭게 둔다고 하자. 직교 투영은 정해진 수식에 따라 그 자유 성분을 유지하거나 바꾼다. 그 결과가 목표 추종이나 에너지 사용에 유리한지, 다음 동작에 여유를 남기는지는 고려하지 않는다. 제약 위반을 없애면서도 과제에 유용한 자유도를 버릴 수 있다.

입력에 따라 제약이 달라지면 제약 행렬의 조건도 문제가 된다. HardNet-Aff 같은 기존 아핀 하드 제약 신경망은 제약 행렬의 행들이 선형 독립이어야 한다는 조건(full row rank)과 제약 수에 관한 구조적 조건을 요구한다. 실제 행동의 가능 집합에는 중복되거나 선형 종속인 제약이 있을 수 있고, 저차원 행동도 많은 부등식으로 둘러싸일 수 있다. 다면체에서 흔히 나타나는 구성이다.

CAffNet은 제약 행렬의 행 독립성이나 적은 제약 수를 요구하지 않는 출력층을 구성하고, 각 제약면을 따라 학습할 수 있는 방향을 남긴다.

## 삼각형 예제로 보는 출력 보정

두 값을 출력하는 신경망을 생각해 보자. 출력은 <math><mi>y</mi><mo>=</mo><mo>(</mo><msub><mi>y</mi><mn>1</mn></msub><mo>,</mo><msub><mi>y</mi><mn>2</mn></msub><mo>)</mo></math>이고 다음 제약을 만족해야 한다.

<math display="block" aria-label="간단한 삼각형 feasible region">
  <msub><mi>y</mi><mn>1</mn></msub><mo>+</mo><msub><mi>y</mi><mn>2</mn></msub><mo>&le;</mo><mn>10</mn><mo>,</mo>
  <mspace width="0.5em"/><msub><mi>y</mi><mn>1</mn></msub><mo>&ge;</mo><mn>0</mn><mo>,</mo>
  <mspace width="0.5em"/><msub><mi>y</mi><mn>2</mn></msub><mo>&ge;</mo><mn>0</mn><mo>.</mo>
</math>

이 부등식들을 만족하는 출력은 삼각형을 이룬다. 일반 신경망은 삼각형 바깥의 점을 출력할 수 있다. 소프트 제약은 그런 출력에 손실 함수의 벌점을 부과한다. 벌점이 커도 추론 단계의 제약 위반을 완전히 막지는 못한다.

CAffNet의 출력은 다음 과정을 거친다.

<math display="block" aria-label="CAffNet 출력 흐름">
  <mtext>unconstrained neural prediction</mtext><mo>&rarr;</mo>
  <mtext>constraint-aware correction</mtext><mo>&rarr;</mo>
  <mtext>feasible output</mtext><mo>.</mo>
</math>

신경망이 먼저 <math><mover><mi>y</mi><mo>^</mo></mover><mo>=</mo><msub><mi>f</mi><mi>&theta;</mi></msub><mo>(</mo><mi>x</mi><mo>)</mo></math>를 제안한다. 이 출력이 허용 영역 밖에 있으면 CAffNet 출력층이 영역 안의 점을 반환한다. 가능 집합이 공집합이 아니라는 가정 아래, 최종 출력은 주어진 아핀 제약을 구조적으로 만족한다.

경계 위에도 제약을 만족하는 점은 여럿이다. 고정된 기하학적 투영이 택한 점보다 같은 경계 위의 다른 점이 과제에 더 유리할 수 있다. 로봇이 두 점에서 모두 안전하더라도, 그중 한 점에서만 목표를 향해 효율적으로 움직일 수 있는 경우다. CAffNet의 학습 가능한 영공간 항은 활성 등식 제약을 유지하는 방향에서 학습한다. 이 자유도 안에서 제약을 위반한 출력을 보정하는 방법과 면 위에 보정된 출력을 놓을 위치를 함께 학습할 수 있다.

부등식이 많아도 모든 제약을 동시에 활성화할 필요는 없다. 2차원 다각형의 경계에 있는 점은 보통 변 하나 위에 놓이거나 두 변이 만나는 꼭짓점에 놓인다. CAffNet은 작은 제약 부분집합으로 후보를 만들고 전체 제약으로 다시 검사한 뒤, 제약을 만족하는 후보 중 하나를 선택한다. 입력에 따라 달라지는 제약, 행렬의 계수 조건에 덜 묶이는 활성 제약 후보, 학습 가능한 영공간 방향을 함께 사용한다는 점이 단순 투영과 구별되는 특징이다.

## 다면체의 면 위에 출력 후보를 구성하는 방법

제약의 부분집합을 <math><mi>&gamma;</mi></math>, 해당 행들을 <math><msub><mi>A</mi><mi>&gamma;</mi></msub></math>, <math><msub><mi>b</mi><mi>&gamma;</mi></msub></math>라고 쓰자. CAffNet은 각 부분집합에 대해 다음과 같이 출력 후보를 만든다.

<math display="block" aria-label="CAffNet 제약 affine 후보">
  <msub><mi mathvariant="script">P</mi><mi>&gamma;</mi></msub><mo>(</mo><mi>x</mi><mo>)</mo>
  <mo>=</mo><msub><mi>f</mi><mi>&theta;</mi></msub>
  <mo>-</mo><msubsup><mi>A</mi><mi>&gamma;</mi><mo>&dagger;</mo></msubsup>
  <mo>(</mo><msub><mi>A</mi><mi>&gamma;</mi></msub><msub><mi>f</mi><mi>&theta;</mi></msub><mo>-</mo><msub><mi>b</mi><mi>&gamma;</mi></msub><mo>)</mo>
  <mo>+</mo><mo>(</mo><mi>I</mi><mo>-</mo><msubsup><mi>A</mi><mi>&gamma;</mi><mo>&dagger;</mo></msubsup><msub><mi>A</mi><mi>&gamma;</mi></msub><mo>)</mo><msub><mi>w</mi><mi>&phi;</mi></msub><mo>.</mo>
</math>

앞의 두 항은 보정 전 신경망 출력 <math><msub><mi>f</mi><mi>&theta;</mi></msub></math>를 등식면 <math><msub><mi>A</mi><mi>&gamma;</mi></msub><mi>y</mi><mo>=</mo><msub><mi>b</mi><mi>&gamma;</mi></msub></math>에 투영한다. 마지막 항은 <math><msub><mi>A</mi><mi>&gamma;</mi></msub></math>의 영공간(null space)에 놓인다. 따라서 등식 제약을 유지하면서 면 위에서 출력을 움직일 수 있다. 두 번째 신경망 <math><msub><mi>w</mi><mi>&phi;</mi></msub></math>는 과제의 손실 함수를 바탕으로 이 자유도를 어떻게 사용할지 학습한다.

등식 제약이 <math><msub><mi>y</mi><mn>2</mn></msub><mo>=</mo><mn>0</mn></math> 하나인 경우를 보자. 고정된 직교 투영은 <math><mo>(</mo><mn>3</mn><mo>,</mo><mn>2</mn><mo>)</mo></math>를 <math><mo>(</mo><mn>3</mn><mo>,</mo><mn>0</mn><mo>)</mo></math>으로 옮긴다. 하지만 <math><mo>(</mo><mi>z</mi><mo>,</mo><mn>0</mn><mo>)</mo></math>의 모든 점이 제약을 만족한다. CAffNet은 등식을 유지하면서 과제에 유용한 <math><mi>z</mi></math>를 학습할 수 있다.

각 후보가 모든 부등식을 만족하는지 검사한다. 보정 전 출력이 제약을 만족하면 그대로 반환하고, 그렇지 않으면 제약을 만족하는 후보 중 원래 출력에 가장 가까운 것을 고른다. 원소 수가 출력 차원 이하인 제약 부분집합을 모두 열거하므로 후보 수는 다음과 같이 계산된다.

<math display="block" aria-label="Active constraint subset 수">
  <mrow><mo>&sum;</mo><mrow><mi>k</mi><mo>=</mo><mn>1</mn></mrow><mrow><mi>min</mi><mo>(</mo><mi>m</mi><mo>,</mo><msub><mi>n</mi><mtext>out</mtext></msub><mo>)</mo></mrow></mrow>
  <mrow><mo>(</mo><mfrac><mi>m</mi><mi>k</mi></mfrac><mo>)</mo></mrow><mo>.</mo>
</math>

다면체에 투영한 점은 선형 독립인 활성 제약 집합(active set)이 정의하는 면에 놓인다. 필요한 독립 제약의 수는 출력 차원을 넘지 않으므로 열거할 부분집합의 크기도 제한된다. 다만 이 활성 제약 조합들을 열거하는 데 계산 비용이 든다. 추론 중 반복 최적화 솔버를 쓰지 않아도 이 비용은 남는다.

## 제약 만족 정리의 보장 범위와 가정

모든 입력에서 다음 다면체가 공집합이 아니라고 가정하자.

<math display="block" aria-label="Feasible set">
  <mi mathvariant="script">S</mi><mo>(</mo><mi>x</mi><mo>)</mo><mo>=</mo><mo>{</mo><mi>y</mi><mo>:</mo><mi>A</mi><mo>(</mo><mi>x</mi><mo>)</mo><mi>y</mi><mo>&le;</mo><mi>b</mi><mo>(</mo><mi>x</mi><mo>)</mo><mo>}</mo>
</math>

논문은 열거한 면 위의 후보 중 적어도 하나가 제약을 만족함을 보인다. 그 후보들 안에서 최종 출력을 선택하므로 다음 부등식이 성립한다.

<math display="block" aria-label="CAffNet 하드 feasibility">
  <mi>A</mi><mo>(</mo><mi>x</mi><mo>)</mo><msup><mi mathvariant="script">P</mi><mo>*</mo></msup><mo>(</mo><mi>x</mi><mo>)</mo><mo>&le;</mo><mi>b</mi><mo>(</mo><mi>x</mi><mo>)</mo><mo>.</mo>
</math>

이 정리는 벌점을 넣었을 때 위반이 줄어드는 경험적 경향을 넘어, 추론 단계에서 제약을 만족한다는 보장을 준다. 논문의 가장 강한 결과지만 어떤 제약 모델을 쓰는지에 따라 보장 범위가 달라진다. 제어기가 추정한 제약 <math><mover><mi>A</mi><mo>^</mo></mover></math>, <math><mover><mi>b</mi><mo>^</mo></mover></math>를 사용하면 보장하는 것은 <math><mover><mi>A</mi><mo>^</mo></mover><mi>y</mi><mo>&le;</mo><mover><mi>b</mi><mo>^</mo></mover></math>뿐이다. 모델이 틀리거나 제약을 빠뜨렸거나 실제 운전 상태가 모델의 적용 범위를 벗어나면 실제 공정의 제약은 위반할 수 있다.

논문은 기반이 되는 비제약 신경망 함수군에 보편 근사 성질이 있으면, 제약을 만족하는 목표 함수에도 그 성질이 유지된다고 주장한다. 주장 자체는 그럴듯하지만 부록의 증명에는 빠진 논리가 있다. 선택한 경계 후보를 이미 제약을 만족하는 후보 집합에 포함된 것처럼 비교한다. 한 면의 등식을 만족하는 것만으로 나머지 부등식까지 만족하지는 않는다. 또한 <math><msup><mi>L</mi><mi>p</mi></msup></math> 근사 성질에서 점별 부등식으로 넘어가는 단계에는 추가 조건이 필요하다. 이 문제들이 제약 만족 정리를 반박하지는 않지만, 보편 근사 증명은 하드 제약 만족 결과보다 덜 완결적이다.

## 제어 장벽 함수에 적용할 때 필요한 조건

제어 장벽 함수(Control Barrier Function, CBF)는 흔히 제어 입력 <math><mi>u</mi></math>에 대한 아핀 제약을 만든다.

<math display="block" aria-label="Control Barrier Function 부등식">
  <msub><mi>L</mi><mi>f</mi></msub><mi>h</mi><mo>(</mo><mi>x</mi><mo>)</mo><mo>+</mo><msub><mi>L</mi><mi>g</mi></msub><mi>h</mi><mo>(</mo><mi>x</mi><mo>)</mo><mi>u</mi>
  <mo>&ge;</mo><mo>-</mo><mi>&alpha;</mi><mo>(</mo><mi>h</mi><mo>(</mo><mi>x</mi><mo>)</mo><mo>)</mo><mo>.</mo>
</math>

이 부등식을 정리하면 CAffNet에 넣을 수 있는 형태가 된다. 학습된 정책이 행동을 제안하고, 출력층이 모델에 정의된 CBF 부등식을 만족하는 행동을 반환한다. 정책의 출력을 제약층에서 보정하는 안전 필터로 사용할 수 있는 구조다.

실제 폐루프 시스템의 물리적 안전까지 보장하려면 동역학, 장벽 함수, 안전한 초기 상태, 샘플링 기반 구현이 각각의 가정을 만족해야 한다. CBF 부등식의 만족만으로는 부족하다. 특히 장애물 근처에서는 구동기 한계 때문에 CBF와 하드웨어 제약을 동시에 만족하는 입력이 없을 수 있다. 실제 제어기가 가능한 행동을 찾지 못할 수 있는 상태에서도 CAffNet은 행동의 가능해 집합이 공집합이 아니라고 가정한다.

## 활성 제약 조합을 열거하는 계산 비용

논문의 작은 최적화 솔버 학습 실험에서 CAffNet-FF는 epoch당 약 1,325 ms가 걸렸고, 비제약 신경망은 4.27 ms가 걸렸다. 학습 시간 차이가 크다. CAffNet-Lite는 열거하는 조합 수를 줄인다. 다만 전체 방법의 일반적인 제약 만족 증명이 부분집합 열거를 제한하는 모든 규칙에 그대로 적용되지는 않는다.

실험에서 보고한 결과는 작은 회귀 예제의 제약 위반 0, 저차원 최적화 학습 문제의 가능해, 유니사이클 제어 시연 한 건의 충돌 회피다. 일반적인 정확도나 계산 효율, 고차원 실시간 제어에 대한 적용 가능성을 뒷받침하는 증거는 부족하다. 최적화 솔버 학습 실험에서는 Transformer 모델의 목적함수 값이 피드포워드 모델보다 훨씬 나빴다. 제어 실험의 범위도 안전성이 다른 상황까지 일반화되는지 평가하기에는 좁다.

CAffNet은 알려진 아핀 제약이 입력에 따라 달라질 때도 이를 만족하도록 출력을 구성하는 신경망 출력층이다. 활성 제약이 정의하는 면 위에 후보를 만들고 영공간 방향의 자유도를 학습하는 구성은 유용하다. 안전 보장은 제약 모델의 정확성과 가능해가 존재한다는 가정에 달려 있다. 모델 불확실성, 이산화, 누락된 위험 요인, 규모에 따른 계산 비용은 별도의 문제로 남는다.

## 참고문헌

Yang Zhao, Jungeun Lee, Jeong Hwan Jeon, and Sze Zheng Yong. *CAffNet: Hard Constraint-Affine Neural Networks*. ICML, 2026.
