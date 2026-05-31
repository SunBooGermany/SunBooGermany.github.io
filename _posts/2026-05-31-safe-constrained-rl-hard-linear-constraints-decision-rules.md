---
layout: post
title: "Hard Linear Constraints in Neural Decisions: Feasibility by Decision-Rule Anchoring"
title_ko: "신경망 의사결정의 하드 선형 제약: 결정규칙 앵커를 통한 실행가능성"
date: 2026-05-31
category: safe-constrained-rl
category_label: "Safe & Constrained RL"
research_group: algorithmic_reviews
research_category: safe-constrained-rl
research_category_label: "Safe & Constrained RL"
application_category: ""
application_category_label: ""
method_category: safe-constrained-rl
method_category_label: "Safe & Constrained RL"
paper_title: "Enforcing hard linear constraints in deep learning models with decision rules"
authors: "Constante-Flores, G. E., Chen, H., & Li, C."
venue: "arXiv preprint"
year: "2025"
doi: ""
arxiv: "2505.13858"
source_url: ""
tags:
  - hard-constraints
  - robust-optimization
  - decision-rules
  - feasible-neural-networks
  - constrained-learning
excerpt: "A critical note on enforcing input-dependent linear equality and inequality constraints in neural network outputs using a robustly feasible decision-rule anchor and minimal interpolation."
excerpt_ko: "강건하게 실행가능한 결정규칙 앵커와 최소 보간을 이용해 신경망 출력의 입력 의존 선형 등식 및 부등식 제약을 강제하는 방법에 대한 비판적 연구 노트."
language: "en-ko"
has_korean_note: false
---

## Positioning: why hard feasibility matters

Many neural decision systems are not allowed to be merely accurate on average. A dispatch model for DC optimal power flow must balance supply and demand. A portfolio model must respect budget and exposure limits. A process-control surrogate may need to output actions that remain inside actuator, safety, or material-balance constraints. In these settings, a small average violation can still be operationally unacceptable.

The paper studies neural network outputs that must satisfy an input-dependent linear feasible set:

<math display="block" aria-label="Input-dependent linear feasible set">
  <mi>C</mi><mo>(</mo><mi>x</mi><mo>)</mo>
  <mo>=</mo>
  <mo>{</mo>
  <mi>y</mi><mo>&isin;</mo><msup><mi mathvariant="double-struck">R</mi><mi>n</mi></msup>
  <mo>&mid;</mo>
  <mi>G</mi><mo>(</mo><mi>x</mi><mo>)</mo><mi>y</mi><mo>=</mo><mi>g</mi><mo>(</mo><mi>x</mi><mo>)</mo>
  <mo>,</mo>
  <mi>H</mi><mo>(</mo><mi>x</mi><mo>)</mo><mi>y</mi><mo>&le;</mo><mi>h</mi><mo>(</mo><mi>x</mi><mo>)</mo>
  <mo>}</mo><mo>.</mo>
</math>

Here, <math><mi>x</mi></math> is the input or uncertain parameter, such as demand, load, market condition, or system state. The vector <math><mi>y</mi></math> is the neural network decision output, such as generation dispatch, portfolio allocation, or control action. The equality constraints <math><mi>G</mi><mo>(</mo><mi>x</mi><mo>)</mo><mi>y</mi><mo>=</mo><mi>g</mi><mo>(</mo><mi>x</mi><mo>)</mo></math> represent balance equations or conservation laws. The inequalities <math><mi>H</mi><mo>(</mo><mi>x</mi><mo>)</mo><mi>y</mi><mo>&le;</mo><mi>h</mi><mo>(</mo><mi>x</mi><mo>)</mo></math> represent capacity, safety, line-flow, allocation, or actuator limits.

The practical issue is not just whether violations are rare. In feasibility-critical settings, a learned model can be useless if it needs a separate repair step every time it is deployed. The question is therefore precise: can a neural decision model preserve much of the accuracy of a task-trained network while enforcing hard linear constraints without solving an optimization problem at inference time?

## Problem setting

The model receives an input <math><mi>x</mi></math> from a specified domain <math><mi>X</mi></math> and returns a decision vector <math><mi>y</mi></math>. The constraints are linear in <math><mi>y</mi></math>, but their coefficients and right-hand sides may depend on <math><mi>x</mi></math>. This captures a useful class of engineering problems: the feasible dispatch region changes with load, the feasible portfolio region changes with market features, and the feasible control set changes with state or operating condition.

The paper's goal is not to learn constraints from data. The constraints are assumed to be known. The learning problem is to produce useful predictions while respecting those constraints by construction. This distinction matters: feasibility is not delegated to statistical generalization alone.

## Prior research gap

Several existing strategies can encourage or enforce constraints in neural outputs.

Activation-based designs, such as softmax, sigmoid, or normalization layers, are simple and fast. They work well for special structures such as simplex, box, or positivity constraints. Their limitation is expressiveness: general input-dependent equality and inequality systems cannot usually be encoded by a fixed activation function.

Penalty and regularization methods add violation terms to the loss. They are easy to train and often improve empirical feasibility, but they do not guarantee zero violation unless additional assumptions and limiting arguments hold. A small penalty loss is not the same as hard feasibility.

Projection methods and differentiable optimization layers can map an unconstrained prediction back into the feasible set. These methods can give feasibility when the projection problem is solved correctly, but they require solving an optimization problem at inference time. That cost can be significant when decisions must be made repeatedly or under tight latency.

Other approaches, including gauge mappings, homeomorphic transformations, and feasible-region sampling, can be powerful for particular geometries. The difficulty is that they may require nontrivial characterization of the feasible region or may not scale cleanly to input-dependent linear systems.

The paper targets the middle ground: avoid pure penalties, avoid per-query projection, and still obtain hard feasibility for linear constraints under stated assumptions.

## Core idea: safe anchor plus minimal interpolation

The architecture combines two outputs:

<math display="block" aria-label="Decision-rule interpolation architecture">
  <msub><mi>f</mi><mi>&psi;</mi></msub><mo>(</mo><mi>x</mi><mo>)</mo>
  <mo>=</mo>
  <mo>(</mo><mn>1</mn><mo>-</mo><msub><mi>&alpha;</mi><mi>&psi;</mi></msub><mo>(</mo><mi>x</mi><mo>)</mo><mo>)</mo>
  <msubsup><mi>f</mi><mi>&theta;</mi><mi>TN</mi></msubsup><mo>(</mo><mi>x</mi><mo>)</mo>
  <mo>+</mo>
  <msub><mi>&alpha;</mi><mi>&psi;</mi></msub><mo>(</mo><mi>x</mi><mo>)</mo>
  <msubsup><mi>f</mi><mi>&phi;</mi><mi>SN</mi></msubsup><mo>(</mo><mi>x</mi><mo>)</mo><mo>.</mo>
</math>

The task network <math><msubsup><mi>f</mi><mi>&theta;</mi><mi>TN</mi></msubsup><mo>(</mo><mi>x</mi><mo>)</mo></math> is trained for prediction quality and may violate inequalities. The safe network <math><msubsup><mi>f</mi><mi>&phi;</mi><mi>SN</mi></msubsup><mo>(</mo><mi>x</mi><mo>)</mo></math> is constructed to be feasible for all <math><mi>x</mi><mo>&isin;</mo><mi>X</mi></math>. The scalar <math><msub><mi>&alpha;</mi><mi>&psi;</mi></msub><mo>(</mo><mi>x</mi><mo>)</mo></math> is the smallest correction amount needed to remove constraint violation along the line segment from the task output to the safe output.

```text
task output, possibly infeasible
        f_TN(x)
          \
           \  move only as much as needed
            \
             f_psi(x)
              \
               \
                f_SN(x), always feasible
```

This is best understood as a line-segment correction toward a robustly feasible anchor. The method does not ask a neural network to discover feasibility from examples. It constructs one endpoint that is feasible by robust optimization logic, then uses only as much interpolation toward that endpoint as the violated constraints require.

## Mathematical structure: equality and inequality handling

Equality constraints can be handled separately by a closed-form equality projection or adjustment of the task output. After that step, the remaining question is inequality feasibility.

Define the slack of constraint <math><mi>i</mi></math> for the task network and safe network:

<math display="block" aria-label="Task and safe network slacks">
  <msubsup><mi>s</mi><mi>i</mi><mi>TN</mi></msubsup><mo>(</mo><mi>x</mi><mo>)</mo>
  <mo>=</mo>
  <msub><mi>h</mi><mi>i</mi></msub><mo>(</mo><mi>x</mi><mo>)</mo>
  <mo>-</mo>
  <msub><mi>H</mi><mi>i</mi></msub><mo>(</mo><mi>x</mi><mo>)</mo>
  <msubsup><mi>f</mi><mi>&theta;</mi><mi>TN</mi></msubsup><mo>(</mo><mi>x</mi><mo>)</mo>
  <mo>,</mo>
  <mspace width="1em"></mspace>
  <msubsup><mi>s</mi><mi>i</mi><mi>SN</mi></msubsup><mo>(</mo><mi>x</mi><mo>)</mo>
  <mo>=</mo>
  <msub><mi>h</mi><mi>i</mi></msub><mo>(</mo><mi>x</mi><mo>)</mo>
  <mo>-</mo>
  <msub><mi>H</mi><mi>i</mi></msub><mo>(</mo><mi>x</mi><mo>)</mo>
  <msubsup><mi>f</mi><mi>&phi;</mi><mi>SN</mi></msubsup><mo>(</mo><mi>x</mi><mo>)</mo><mo>.</mo>
</math>

A nonnegative slack means the constraint is satisfied. A negative slack means it is violated. For the final interpolated output, linearity gives

<math display="block" aria-label="Interpolated slack">
  <msubsup><mi>s</mi><mi>i</mi><mi>&psi;</mi></msubsup><mo>(</mo><mi>x</mi><mo>)</mo>
  <mo>=</mo>
  <mo>(</mo><mn>1</mn><mo>-</mo><mi>&alpha;</mi><mo>)</mo>
  <msubsup><mi>s</mi><mi>i</mi><mi>TN</mi></msubsup><mo>(</mo><mi>x</mi><mo>)</mo>
  <mo>+</mo>
  <mi>&alpha;</mi>
  <msubsup><mi>s</mi><mi>i</mi><mi>SN</mi></msubsup><mo>(</mo><mi>x</mi><mo>)</mo><mo>.</mo>
</math>

If a task output already satisfies all inequalities, then <math><mi>&alpha;</mi><mo>=</mo><mn>0</mn></math> is enough. If a constraint is violated, then the interpolation coefficient must be large enough to make its slack nonnegative. The final coefficient is the maximum required correction over the violated constraints.

The intuition is simple. If the safe point has positive or nonnegative slack and the task point violates a constraint, the line segment from the task point to the safe point eventually crosses back into the feasible halfspace. Taking the largest required crossing fraction across constraints enforces all inequalities simultaneously.

## Why the safe network is a decision rule

The safe network is not a normal task-trained neural network. It is closer to a robust optimization decision rule. In its basic form,

<math display="block" aria-label="Linear decision rule safe network">
  <msubsup><mi>f</mi><mi>&phi;</mi><mi>SN</mi></msubsup><mo>(</mo><mi>x</mi><mo>)</mo>
  <mo>=</mo>
  <mi>F</mi><mi>x</mi><mo>.</mo>
</math>

The matrix <math><mi>F</mi></math> is chosen offline so that <math><mi>F</mi><mi>x</mi></math> satisfies the constraints for every <math><mi>x</mi><mo>&isin;</mo><mi>X</mi></math>. This is analogous to adjustable robust optimization: the decision may depend on the uncertain input, but it must remain feasible over the whole uncertainty set.

The safe output should ideally lie inside the feasible region with useful slack rather than exactly on the boundary. A deeper feasible anchor can reduce the amount of interpolation needed. If the safe point is barely feasible, many task outputs may need large corrections, which can damage prediction quality.

## Tractable formulations

The supplied material distinguishes two cases.

In the more general input-dependent left-hand-side case, the constraint matrix depends on <math><mi>x</mi></math>. Robust feasibility of a linear decision rule can then lead to quadratic constraints. The paper uses an SDP-type inner approximation for tractability. This can be conservative: failure to find such a decision rule does not necessarily mean no feasible rule exists.

In the jointly linear case, the left-hand side is fixed while the right-hand side depends linearly on <math><mi>x</mi></math>. Robust linear constraints can then be reformulated using LP duality. This is cleaner and more directly useful for problems such as DC-OPF, where linear physics and uncertain loads naturally produce structured linear constraints.

The distinction is important. The hard-feasibility architecture is conceptually simple, but the offline construction of the safe anchor may still be the difficult part.

## What is mathematically guaranteed

The core feasibility guarantee is conditional and structural. Under the stated assumptions, if the task output satisfies the equality constraints, if the safe output is feasible for all <math><mi>x</mi><mo>&isin;</mo><mi>X</mi></math>, if the feasible set is defined by linear equality and inequality constraints, and if <math><msub><mi>&alpha;</mi><mi>&psi;</mi></msub><mo>(</mo><mi>x</mi><mo>)</mo></math> is computed exactly as the minimum required interpolation amount, then the final output satisfies the hard linear constraints.

This guarantee is independent of neural network prediction accuracy. The task network may generalize poorly, but feasibility still follows from the safe anchor and interpolation rule as long as the input lies in the assumed domain and the safe decision rule is valid.

For the robust reformulation, the LP formulation in the jointly linear case is relatively clean because it follows from robust linear constraint duality. The SDP formulation for more general input dependence is an inner approximation, so it may be conservative.

The supplied material also points to a universal approximation result. That result should be read cautiously. It depends on strong expressiveness assumptions and should not be interpreted as saying that a practical linear decision-rule implementation is universally expressive in finite data, finite width, or numerically constrained settings.

## Distinctive contribution

The distinctive contribution is the way the paper separates feasibility certification from task prediction. A standard task network is allowed to focus on predictive quality. A separate decision-rule anchor is constructed offline to be feasible over the uncertainty set. The final output is then obtained by an explicit interpolation rule whose only job is to restore hard linear feasibility.

This is more specific than adding a penalty to the loss and less computationally heavy than solving a projection problem at every inference call. The paper's original design choice is to make the safe endpoint a robust decision rule, then compute the minimum line-segment movement needed to satisfy the violated linear inequalities. Feasibility comes from the geometry of linear constraints and the validity of the safe anchor, not from the task network learning the feasible set.

This contribution is especially relevant to safe and constrained learning because many safety filters repair a learned action by solving an online optimization problem. Here, after the safe rule has been built, the repair is algebraic: check slacks, identify the most restrictive violated constraint, and interpolate only as much as required. The result is a fast feasibility layer with a clear certificate, while still leaving objective optimality and nonlinear constraint handling outside the guarantee.

## Assumptions and limitations

First, the method is mainly suited to linear equality and inequality constraints. It does not directly handle nonlinear process constraints, complementarity constraints, binary decisions, or strongly nonconvex feasible regions.

Second, the method may become harder to use when the number of constraints is very large. The interpolation coefficient depends on constraint-wise slacks, and the most restrictive violated constraints dominate the correction.

Third, the method may be sensitive when constraint scales differ substantially. Poorly scaled constraints can make the interpolation correction numerically unbalanced, so constraint normalization or scaling may be necessary.

Fourth, the correction is feasibility-oriented rather than objective-oriented. The interpolation coefficient is chosen to remove linear constraint violations, not to minimize the original cost, reward loss, economic objective, or downstream control objective over the feasible region. Therefore, the corrected output can be hard-feasible without being the best feasible decision for the task objective.

These limitations do not undermine the main idea. They specify where the guarantee lives: linear constraints, a valid uncertainty set, and a tractable safe decision rule.

## Critical assessment

The paper's strongest point is the clean separation between accuracy and feasibility. The task network carries predictive power. The safe decision rule carries robust feasibility. The interpolation coefficient links them through a transparent algebraic correction.

The main caveat is that the burden has not disappeared. It has moved offline into the construction of a robustly feasible decision-rule anchor and into the assumption that the deployment input belongs to the specified uncertainty set. If that set is misspecified, if the safe rule is too conservative, or if the constraint representation omits important nonlinear physics, the practical value can weaken even though the linear feasibility statement remains true within its scope.

This is a useful contribution precisely because it avoids a common overclaim. It does not make a neural network magically learn feasibility. It uses robust optimization to construct a feasible anchor, then corrects a task-trained output toward that anchor by the minimum amount required to satisfy hard linear constraints. The main strength is the combination of hard feasibility and fast inference. The main restriction is that the guarantee is tied to linear constraints, a valid uncertainty set, and a tractable safe decision rule.

## References

- Constante-Flores, G. E., Chen, H., & Li, C. (2025). Enforcing hard linear constraints in deep learning models with decision rules. arXiv preprint arXiv:2505.13858.

<!-- ko -->

## 포지셔닝: 왜 하드 실행가능성이 중요한가

많은 신경망 기반 의사결정 시스템에서는 평균적으로 정확한 것만으로 충분하지 않다. DC 최적전력흐름의 dispatch 모델은 수요와 공급의 균형을 맞추어야 한다. 포트폴리오 모델은 예산과 노출 한도를 지켜야 한다. 공정 제어 surrogate는 actuator, 안전, 물질수지 제약 안에 머무르는 제어 입력을 출력해야 할 수 있다. 이런 시스템에서는 작은 평균 위반도 실제 운영에서는 받아들이기 어렵다.

이 논문은 신경망 출력이 다음과 같은 입력 의존 선형 실행가능 집합을 만족해야 하는 문제를 다룬다.

<math display="block" aria-label="Input-dependent linear feasible set">
  <mi>C</mi><mo>(</mo><mi>x</mi><mo>)</mo>
  <mo>=</mo>
  <mo>{</mo>
  <mi>y</mi><mo>&isin;</mo><msup><mi mathvariant="double-struck">R</mi><mi>n</mi></msup>
  <mo>&mid;</mo>
  <mi>G</mi><mo>(</mo><mi>x</mi><mo>)</mo><mi>y</mi><mo>=</mo><mi>g</mi><mo>(</mo><mi>x</mi><mo>)</mo>
  <mo>,</mo>
  <mi>H</mi><mo>(</mo><mi>x</mi><mo>)</mo><mi>y</mi><mo>&le;</mo><mi>h</mi><mo>(</mo><mi>x</mi><mo>)</mo>
  <mo>}</mo><mo>.</mo>
</math>

여기서 <math><mi>x</mi></math>는 입력 또는 불확실한 파라미터이며, 수요, 부하, 시장 조건, 시스템 상태일 수 있다. <math><mi>y</mi></math>는 신경망이 출력하는 의사결정 벡터로, 발전량 dispatch, 포트폴리오 배분, 제어 입력 같은 값을 뜻한다. 등식 제약 <math><mi>G</mi><mo>(</mo><mi>x</mi><mo>)</mo><mi>y</mi><mo>=</mo><mi>g</mi><mo>(</mo><mi>x</mi><mo>)</mo></math>는 균형식이나 보존 법칙을 나타낸다. 부등식 제약 <math><mi>H</mi><mo>(</mo><mi>x</mi><mo>)</mo><mi>y</mi><mo>&le;</mo><mi>h</mi><mo>(</mo><mi>x</mi><mo>)</mo></math>는 용량, 안전, 선로 흐름, 배분, actuator 한계를 나타낸다.

실용적 문제는 위반이 드문지 여부만이 아니다. 실행가능성이 중요한 시스템에서는 배포할 때마다 별도의 repair 단계가 필요하다면 학습 모델의 가치가 크게 줄어든다. 따라서 핵심 질문은 명확하다. task-trained network의 정확도를 상당 부분 유지하면서, 추론 시점에 최적화 문제를 풀지 않고도 하드 선형 제약을 강제할 수 있는가?

## 문제 설정

모델은 지정된 영역 <math><mi>X</mi></math>에서 입력 <math><mi>x</mi></math>를 받고 의사결정 벡터 <math><mi>y</mi></math>를 반환한다. 제약은 <math><mi>y</mi></math>에 대해서는 선형이지만, 계수와 우변은 <math><mi>x</mi></math>에 의존할 수 있다. 이는 여러 공학 문제를 포착한다. 부하가 달라지면 dispatch의 실행가능 영역이 달라지고, 시장 특징이 달라지면 포트폴리오 제약이 달라지며, 상태나 운전 조건이 달라지면 제어 입력의 실행가능 집합도 달라진다.

논문의 목표는 데이터로부터 제약을 학습하는 것이 아니다. 제약은 알려져 있다고 가정한다. 학습 문제는 유용한 예측을 만들면서도 그 제약을 구조적으로 만족시키는 것이다. 이 구분이 중요하다. 실행가능성을 통계적 일반화에만 맡기지 않기 때문이다.

## 선행 접근과 한계

신경망 출력의 제약을 유도하거나 강제하는 방법은 여러 가지가 있다.

softmax, sigmoid, normalization layer 같은 activation 기반 설계는 단순하고 빠르다. simplex, box, positivity 제약처럼 특수한 구조에는 잘 맞는다. 그러나 일반적인 입력 의존 등식 및 부등식 시스템을 고정된 activation 함수로 표현하기는 어렵다.

penalty나 regularization 방법은 손실함수에 제약 위반 항을 추가한다. 학습하기 쉽고 경험적으로 실행가능성을 개선할 수 있지만, 추가 가정이나 극한 논리 없이는 위반이 정확히 0임을 보장하지 않는다. 작은 penalty loss는 하드 실행가능성과 같지 않다.

projection 방법과 differentiable optimization layer는 unconstrained prediction을 실행가능 집합으로 다시 사상할 수 있다. projection 문제가 정확히 풀리면 실행가능성을 줄 수 있지만, 추론 시점마다 최적화 문제를 풀어야 한다. 반복적 의사결정이나 낮은 latency가 필요한 환경에서는 이 비용이 중요해질 수 있다.

gauge mapping, homeomorphic transformation, feasible-region sampling 같은 다른 접근도 특정 기하 구조에서는 강력할 수 있다. 다만 feasible region의 비자명한 특성화가 필요하거나, 입력 의존 선형 시스템으로 깔끔하게 확장되지 않을 수 있다.

이 논문은 중간 지점을 겨냥한다. 순수 penalty를 피하고, 매 query마다 projection을 푸는 것도 피하면서, 명시된 가정 아래 선형 제약에 대한 하드 실행가능성을 얻으려 한다.

## 핵심 아이디어: 안전 앵커와 최소 보간

아키텍처는 두 출력을 결합한다.

<math display="block" aria-label="Decision-rule interpolation architecture">
  <msub><mi>f</mi><mi>&psi;</mi></msub><mo>(</mo><mi>x</mi><mo>)</mo>
  <mo>=</mo>
  <mo>(</mo><mn>1</mn><mo>-</mo><msub><mi>&alpha;</mi><mi>&psi;</mi></msub><mo>(</mo><mi>x</mi><mo>)</mo><mo>)</mo>
  <msubsup><mi>f</mi><mi>&theta;</mi><mi>TN</mi></msubsup><mo>(</mo><mi>x</mi><mo>)</mo>
  <mo>+</mo>
  <msub><mi>&alpha;</mi><mi>&psi;</mi></msub><mo>(</mo><mi>x</mi><mo>)</mo>
  <msubsup><mi>f</mi><mi>&phi;</mi><mi>SN</mi></msubsup><mo>(</mo><mi>x</mi><mo>)</mo><mo>.</mo>
</math>

task network <math><msubsup><mi>f</mi><mi>&theta;</mi><mi>TN</mi></msubsup><mo>(</mo><mi>x</mi><mo>)</mo></math>는 예측 품질을 위해 학습되며 부등식 제약을 위반할 수 있다. safe network <math><msubsup><mi>f</mi><mi>&phi;</mi><mi>SN</mi></msubsup><mo>(</mo><mi>x</mi><mo>)</mo></math>는 모든 <math><mi>x</mi><mo>&isin;</mo><mi>X</mi></math>에 대해 실행가능하도록 구성된다. 스칼라 <math><msub><mi>&alpha;</mi><mi>&psi;</mi></msub><mo>(</mo><mi>x</mi><mo>)</mo></math>는 task output에서 safe output으로 가는 선분 위에서 제약 위반을 제거하기 위해 필요한 최소 보정량이다.

```text
task output, possibly infeasible
        f_TN(x)
          \
           \  move only as much as needed
            \
             f_psi(x)
              \
               \
                f_SN(x), always feasible
```

이 방법은 강건하게 실행가능한 앵커를 향한 선분 보정으로 이해하는 것이 가장 정확하다. 신경망이 예시로부터 실행가능성을 직접 발견하도록 맡기는 것이 아니다. 한쪽 끝점을 robust optimization 논리로 실행가능하게 만들고, 위반된 제약이 요구하는 만큼만 그 끝점 쪽으로 보간한다.

## 수학적 구조: 등식 처리와 부등식 보정

등식 제약은 closed-form equality projection 또는 task output의 조정을 통해 별도로 처리할 수 있다. 그 이후 남는 문제는 부등식 실행가능성이다.

제약 <math><mi>i</mi></math>에 대한 task network와 safe network의 slack을 다음과 같이 정의한다.

<math display="block" aria-label="Task and safe network slacks">
  <msubsup><mi>s</mi><mi>i</mi><mi>TN</mi></msubsup><mo>(</mo><mi>x</mi><mo>)</mo>
  <mo>=</mo>
  <msub><mi>h</mi><mi>i</mi></msub><mo>(</mo><mi>x</mi><mo>)</mo>
  <mo>-</mo>
  <msub><mi>H</mi><mi>i</mi></msub><mo>(</mo><mi>x</mi><mo>)</mo>
  <msubsup><mi>f</mi><mi>&theta;</mi><mi>TN</mi></msubsup><mo>(</mo><mi>x</mi><mo>)</mo>
  <mo>,</mo>
  <mspace width="1em"></mspace>
  <msubsup><mi>s</mi><mi>i</mi><mi>SN</mi></msubsup><mo>(</mo><mi>x</mi><mo>)</mo>
  <mo>=</mo>
  <msub><mi>h</mi><mi>i</mi></msub><mo>(</mo><mi>x</mi><mo>)</mo>
  <mo>-</mo>
  <msub><mi>H</mi><mi>i</mi></msub><mo>(</mo><mi>x</mi><mo>)</mo>
  <msubsup><mi>f</mi><mi>&phi;</mi><mi>SN</mi></msubsup><mo>(</mo><mi>x</mi><mo>)</mo><mo>.</mo>
</math>

slack이 0 이상이면 해당 제약은 만족된다. slack이 음수이면 제약을 위반한 것이다. 최종 보간 출력의 slack은 선형성 때문에 다음과 같다.

<math display="block" aria-label="Interpolated slack">
  <msubsup><mi>s</mi><mi>i</mi><mi>&psi;</mi></msubsup><mo>(</mo><mi>x</mi><mo>)</mo>
  <mo>=</mo>
  <mo>(</mo><mn>1</mn><mo>-</mo><mi>&alpha;</mi><mo>)</mo>
  <msubsup><mi>s</mi><mi>i</mi><mi>TN</mi></msubsup><mo>(</mo><mi>x</mi><mo>)</mo>
  <mo>+</mo>
  <mi>&alpha;</mi>
  <msubsup><mi>s</mi><mi>i</mi><mi>SN</mi></msubsup><mo>(</mo><mi>x</mi><mo>)</mo><mo>.</mo>
</math>

task output이 이미 모든 부등식을 만족하면 <math><mi>&alpha;</mi><mo>=</mo><mn>0</mn></math>이면 충분하다. 어떤 제약을 위반했다면, 그 slack을 0 이상으로 만들 만큼 보간 계수가 커져야 한다. 최종 계수는 위반된 제약들이 요구하는 보정량 중 최대값이다.

직관은 단순하다. safe point가 양의 slack 또는 비음수 slack을 가지고 있고 task point가 어떤 제약을 위반한다면, task point에서 safe point로 가는 선분은 결국 해당 feasible halfspace 안으로 다시 들어온다. 모든 제약에 대해 필요한 crossing fraction 중 가장 큰 값을 취하면 모든 부등식을 동시에 만족시킬 수 있다.

## safe network는 왜 결정규칙인가

safe network는 일반적인 task-trained neural network가 아니다. robust optimization의 decision rule에 더 가깝다. 기본 형태는 다음과 같다.

<math display="block" aria-label="Linear decision rule safe network">
  <msubsup><mi>f</mi><mi>&phi;</mi><mi>SN</mi></msubsup><mo>(</mo><mi>x</mi><mo>)</mo>
  <mo>=</mo>
  <mi>F</mi><mi>x</mi><mo>.</mo>
</math>

행렬 <math><mi>F</mi></math>는 모든 <math><mi>x</mi><mo>&isin;</mo><mi>X</mi></math>에 대해 <math><mi>F</mi><mi>x</mi></math>가 제약을 만족하도록 오프라인에서 선택된다. 이는 adjustable robust optimization과 유사하다. 결정은 불확실 입력에 의존할 수 있지만, 전체 uncertainty set 위에서 실행가능해야 한다.

safe output은 가능하면 feasible region의 경계가 아니라 충분한 slack을 가진 내부에 위치하는 것이 좋다. 더 깊은 feasible anchor는 필요한 보간량을 줄일 수 있다. safe point가 간신히 feasible하면 많은 task output이 큰 보정을 필요로 하며, 이는 예측 품질을 손상시킬 수 있다.

## 계산 가능한 정식화

제공된 자료는 두 경우를 구분한다.

더 일반적인 input-dependent left-hand-side 경우에는 제약 행렬이 <math><mi>x</mi></math>에 의존한다. 이때 선형 decision rule의 robust feasibility는 quadratic constraints로 이어질 수 있다. 논문은 계산 가능성을 위해 SDP-type inner approximation을 사용한다. 이는 보수적일 수 있다. 그런 decision rule을 찾지 못했다는 사실이 실행가능한 rule이 전혀 없다는 뜻은 아니다.

jointly linear 경우에는 좌변 행렬이 고정되어 있고 우변이 <math><mi>x</mi></math>에 선형으로 의존한다. 이 경우 robust linear constraints는 LP duality를 통해 재정식화될 수 있다. 이는 더 깔끔하며, 선형 물리식과 불확실 부하가 구조적 선형 제약을 만드는 DC-OPF 같은 문제에 특히 직접적으로 유용하다.

이 구분은 중요하다. 하드 실행가능성 아키텍처 자체는 개념적으로 단순하지만, safe anchor를 오프라인에서 구성하는 일이 여전히 어려운 부분일 수 있기 때문이다.

## 무엇이 수학적으로 보장되는가

핵심 실행가능성 보장은 조건부이며 구조적이다. 명시된 가정 아래, task output이 등식 제약을 만족하고, safe output이 모든 <math><mi>x</mi><mo>&isin;</mo><mi>X</mi></math>에 대해 실행가능하며, feasible set이 선형 등식 및 부등식 제약으로 정의되고, <math><msub><mi>&alpha;</mi><mi>&psi;</mi></msub><mo>(</mo><mi>x</mi><mo>)</mo></math>가 필요한 최소 보간량으로 정확히 계산된다면, 최종 출력은 하드 선형 제약을 만족한다.

이 보장은 신경망 예측 정확도와 독립적이다. task network가 일반화를 잘 못하더라도, 입력이 가정된 영역 안에 있고 safe decision rule이 유효하다면 실행가능성은 safe anchor와 보간 규칙으로부터 따라온다.

robust reformulation에 대해서는, jointly linear 경우의 LP 정식화가 robust linear constraint duality에서 나오므로 비교적 깔끔하다. 더 일반적인 입력 의존성에 대한 SDP 정식화는 inner approximation이므로 보수적일 수 있다.

제공된 자료는 universal approximation 결과도 언급한다. 이 결과는 조심스럽게 읽어야 한다. 강한 표현력 가정에 의존하며, 실제 선형 decision-rule 구현이 유한 데이터, 유한 width, 수치적 제약 아래에서 보편적으로 expressive하다는 뜻으로 해석해서는 안 된다.

## 이 연구의 독창적인 부분

이 연구의 독창적인 부분은 실행가능성 인증과 task prediction을 분리하는 방식에 있다. 일반적인 task network는 예측 품질에 집중하게 둔다. 별도의 decision-rule anchor는 uncertainty set 전체에서 실행가능하도록 오프라인에서 구성한다. 최종 출력은 하드 선형 실행가능성을 회복하기 위한 명시적 보간 규칙으로 얻는다.

이는 단순히 loss에 penalty를 더하는 것보다 구체적이고, 매 inference마다 projection 문제를 푸는 방식보다 계산적으로 가볍다. 논문의 독창적인 설계 선택은 safe endpoint를 robust decision rule로 만들고, 위반된 선형 부등식을 만족하기 위해 필요한 최소한의 선분 이동량을 계산한다는 점이다. 실행가능성은 task network가 feasible set을 학습했기 때문에 생기는 것이 아니라, 선형 제약의 기하와 safe anchor의 유효성에서 나온다.

이 점은 safe and constrained learning 관점에서 특히 중요하다. 많은 safety filter는 학습된 action을 고치기 위해 온라인 최적화 문제를 푼다. 반면 이 방법은 safe rule이 한 번 구성되고 나면 repair가 대수적으로 이루어진다. slack을 확인하고, 가장 제한적인 위반 제약을 찾고, 필요한 만큼만 보간한다. 그 결과 빠른 feasibility layer와 명확한 인증 논리를 얻지만, objective optimality와 비선형 제약 처리는 여전히 보장 밖에 남는다.

## 가정과 한계

첫째, 이 방법은 주로 선형 등식 및 부등식 제약에 적합하다. 비선형 공정 제약, complementarity constraints, binary decisions, 강한 nonconvex feasible region을 직접 다루지는 않는다.

둘째, 제약 수가 매우 많아지면 사용이 어려워질 수 있다. 보간 계수는 constraint-wise slack에 의존하고, 가장 제한적인 위반 제약들이 보정을 지배한다.

셋째, 제약들의 scale이 크게 다르면 민감해질 수 있다. poorly scaled constraints는 보간 보정을 수치적으로 불균형하게 만들 수 있으므로 constraint normalization 또는 scaling이 필요할 수 있다.

넷째, 보정은 objective-oriented라기보다 feasibility-oriented이다. 보간 계수는 선형 제약 위반을 제거하기 위해 선택되는 것이지, feasible region 위에서 원래의 비용함수, reward loss, 경제적 목적함수, 또는 downstream control objective를 최소화하도록 선택되는 것은 아니다. 따라서 최종 출력은 하드 실행가능할 수 있지만, task objective 관점에서 가장 좋은 feasible decision이라고 보장되지는 않는다.

이 한계들은 핵심 아이디어를 무너뜨리지 않는다. 오히려 보장이 존재하는 영역을 분명히 한다. 그 영역은 선형 제약, 유효한 uncertainty set, 계산 가능한 safe decision rule이다.

## 비판적 평가

이 논문의 가장 강한 점은 정확도와 실행가능성을 깔끔하게 분리한다는 것이다. task network는 예측력을 담당한다. safe decision rule은 robust feasibility를 담당한다. interpolation coefficient는 투명한 대수적 보정으로 둘을 연결한다.

핵심 caveat는 부담이 사라진 것이 아니라는 점이다. 부담은 robustly feasible decision-rule anchor의 오프라인 구성과, 배포 입력이 지정된 uncertainty set에 속한다는 가정으로 이동했다. 그 집합이 잘못 지정되거나, safe rule이 지나치게 보수적이거나, 제약 표현이 중요한 비선형 물리를 빠뜨린다면, 선형 실행가능성 명제는 그 범위 안에서 참이더라도 실제 가치는 약해질 수 있다.

이 기여가 유용한 이유는 흔한 과장을 피하기 때문이다. 이 방법은 신경망이 마술처럼 실행가능성을 학습하게 만들지 않는다. robust optimization으로 feasible anchor를 구성하고, hard linear constraints를 만족하기 위해 필요한 최소량만큼 task-trained output을 그 anchor 쪽으로 보정한다. 주된 장점은 하드 실행가능성과 빠른 추론의 결합이다. 주된 제한은 보장이 선형 제약, 유효한 uncertainty set, 계산 가능한 safe decision rule에 묶여 있다는 점이다.

## References

- Constante-Flores, G. E., Chen, H., & Li, C. (2025). Enforcing hard linear constraints in deep learning models with decision rules. arXiv preprint arXiv:2505.13858.
