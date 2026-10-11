---
layout: post
title: "Must an Optimum Satisfy KKT? Intuition and Proofs for LICQ, MFCQ, and Slater"
title_ko: "최적해는 반드시 KKT를 만족하는가? LICQ·MFCQ·Slater의 직관과 증명"
date: 2026-10-11
category: stochastic-nonlinear-optimization
category_label: "Mathematical Optimization"
research_group: algorithmic_reviews
research_category: stochastic-nonlinear-optimization
research_category_label: "Mathematical Optimization"
application_category: ""
application_category_label: ""
method_category: "stochastic-nonlinear-optimization"
method_category_label: "Mathematical Optimization"
paper_title: ""
authors: ""
venue: ""
year: ""
doi: ""
arxiv: ""
source_url: ""
tags:
  - "KKT"
  - "constraint qualification"
  - "LICQ"
  - "MFCQ"
  - "Slater"
  - "Fritz John"
  - "optimality conditions"
  - "solution sensitivity"
excerpt: "A constraint can block all feasible motion while its gradient says nothing. Ramp limits and short multiplier proofs separate KKT necessity, convex sufficiency, and optimizer differentiability."
excerpt_ko: "제약은 실제 움직임을 막는데 gradient는 이를 표현하지 못할 수 있다. Ramp 예제와 짧은 승수 증명으로 KKT의 필요성, convex 문제의 충분성, 최적해의 미분 가능성을 구분한다."
language: "en-ko"
has_korean_note: false
---

An optimum need not satisfy KKT. For a continuously differentiable problem, a local minimum admits KKT multipliers under a suitable constraint qualification (CQ). Convexity answers a different question: whether an existing KKT point is globally optimal.

The distinction becomes concrete through a ramp limit, a degenerate constraint, and short proofs for LICQ, MFCQ, and Slater.

## 1. A ramp limit: why the gradient need not vanish

Suppose increasing equipment output improves the objective, but this step's hard ramp limit allows only outputs between 0.4 and 0.6. Minimizing the negative output selects the upper bound:

<math display="block" aria-label="Linear reward with an upper ramp bound"><mtable columnalign="left"><mtr><mtd><munder><mo>min</mo><mrow><mn>.4</mn><mo>≤</mo><mi>a</mi><mo>≤</mo><mn>.6</mn></mrow></munder><mo>(</mo><mo>−</mo><mi>a</mi><mo>)</mo></mtd></mtr><mtr><mtd><msup><mi>a</mi><mo>*</mo></msup><mo>=</mo><mn>.6</mn><mo>,</mo><mi>λ</mi><mo>=</mo><mn>1</mn><mo>,</mo><mo>−</mo><mn>1</mn><mo>+</mo><mi>λ</mi><mo>=</mo><mn>0</mn></mtd></mtr></mtable></math>

The objective gradient is −1 even at the optimum. Increasing output would still improve the objective, but the active upper bound blocks that direction. Its gradient is +1. A multiplier of 1 balances the objective gradient in the stationarity equation. The lower bound has slack, so its multiplier is zero.

KKT expresses this balance with the gradients of the active constraints. It uses first-order information. That is also its limitation: a constraint may block actual motion without its gradient expressing the obstruction.

## 2. A global optimum that fails KKT

<math display="block" aria-label="A convex optimum without KKT multipliers"><munder><mo>min</mo><mi>x</mi></munder><mi>x</mi><mo>,</mo><mspace width="1em"/><mtext>subject to</mtext><mspace width=".5em"/><msup><mi>x</mi><mn>2</mn></msup><mo>≤</mo><mn>0</mn></math>

The only feasible point is <math><msup><mi>x</mi><mo>*</mo></msup></math> = 0. It is the unique global minimum, and both the objective and constraint function are convex. Yet stationarity cannot hold:

<math display="block" aria-label="Stationarity is impossible at zero"><mtable columnalign="left"><mtr><mtd><mi>L</mi><mo>(</mo><mi>x</mi><mo>,</mo><mi>λ</mi><mo>)</mo><mo>=</mo><mi>x</mi><mo>+</mo><mi>λ</mi><msup><mi>x</mi><mn>2</mn></msup></mtd></mtr><mtr><mtd><mn>1</mn><mo>+</mo><mn>2</mn><mi>λ</mi><mi>x</mi><mo>=</mo><mn>0</mn><mo>⇒</mo><mn>1</mn><mo>+</mo><mn>2</mn><mi>λ</mi><mo>·</mo><mn>0</mn><mo>=</mo><mn>0</mn></mtd></mtr></mtable></math>

At zero, every finite multiplier leaves the left side equal to 1. The actual constraint prevents any motion, whereas its first-order approximation admits every direction:

<math display="block" aria-label="The linearized constraint misses the obstruction"><mi>g</mi><mo>(</mo><mn>0</mn><mo>)</mo><mo>+</mo><msup><mi>g</mi><mo>′</mo></msup><mo>(</mo><mn>0</mn><mo>)</mo><mi>d</mi><mo>=</mo><mn>0</mn><mo>≤</mo><mn>0</mn></math>

Here the objective decreases by a first-order amount when moving left; infeasibility appears through the squared displacement. The derivative of the constraint at zero misses that second-order obstruction.

Write the same feasible set as the equality x = 0 instead. Its gradient is 1, and a multiplier of −1 gives stationarity:

<math display="block" aria-label="An equivalent equality has a nonzero gradient"><mi>L</mi><mo>(</mo><mi>x</mi><mo>,</mo><mi>ν</mi><mo>)</mo><mo>=</mo><mi>x</mi><mo>+</mo><mi>ν</mi><mi>x</mi><mo>,</mo><mn>1</mn><mo>+</mo><mi>ν</mi><mo>=</mo><mn>0</mn><mo>⇒</mo><mi>ν</mi><mo>=</mo><mo>−</mo><mn>1</mn></math>

Thus the existence of KKT multipliers can depend on the constraint representation, even when the objective and feasible set are unchanged.

## 3. What “the optimum satisfies KKT” means

Consider real continuous variables and functions that are <math><msup><mi>C</mi><mn>1</mn></msup></math> in a neighborhood of the candidate:

<math display="block" aria-label="Smooth constrained minimization problem"><mtable columnalign="left"><mtr><mtd><munder><mo>min</mo><mrow><mi>x</mi><mo>∈</mo><msup><mi>ℝ</mi><mi>n</mi></msup></mrow></munder><mi>f</mi><mo>(</mo><mi>x</mi><mo>)</mo></mtd></mtr><mtr><mtd><msub><mi>g</mi><mi>i</mi></msub><mo>(</mo><mi>x</mi><mo>)</mo><mo>≤</mo><mn>0</mn><mo>,</mo><mtext> i = 1, …, m</mtext></mtd></mtr><mtr><mtd><msub><mi>h</mi><mi>j</mi></msub><mo>(</mo><mi>x</mi><mo>)</mo><mo>=</mo><mn>0</mn><mo>,</mo><mtext> j = 1, …, p</mtext></mtd></mtr></mtable></math>

The statement means that there **exist** nonnegative inequality multipliers and unrestricted equality multipliers satisfying all four conditions. Stationarity is

<math display="block" aria-label="KKT stationarity"><mo>∇</mo><mi>f</mi><mo>(</mo><msup><mi>x</mi><mo>*</mo></msup><mo>)</mo><mo>+</mo><munder><mo>∑</mo><mrow><mi>i</mi></mrow></munder><msub><mi>λ</mi><mi>i</mi></msub><mo>∇</mo><msub><mi>g</mi><mi>i</mi></msub><mo>(</mo><msup><mi>x</mi><mo>*</mo></msup><mo>)</mo><mo>+</mo><munder><mo>∑</mo><mrow><mi>j</mi></mrow></munder><msub><mi>ν</mi><mi>j</mi></msub><mo>∇</mo><msub><mi>h</mi><mi>j</mi></msub><mo>(</mo><msup><mi>x</mi><mo>*</mo></msup><mo>)</mo><mo>=</mo><mn>0</mn></math>

The remaining conditions are primal feasibility, dual feasibility, and complementary slackness:

<math display="block" aria-label="Primal feasibility, dual feasibility, and complementarity"><mtable columnalign="left"><mtr><mtd><msub><mi>g</mi><mi>i</mi></msub><mo>(</mo><msup><mi>x</mi><mo>*</mo></msup><mo>)</mo><mo>≤</mo><mn>0</mn><mo>,</mo><msub><mi>h</mi><mi>j</mi></msub><mo>(</mo><msup><mi>x</mi><mo>*</mo></msup><mo>)</mo><mo>=</mo><mn>0</mn></mtd></mtr><mtr><mtd><mi>λ</mi><mo>≥</mo><mn>0</mn><mo>,</mo><msub><mi>λ</mi><mi>i</mi></msub><msub><mi>g</mi><mi>i</mi></msub><mo>(</mo><msup><mi>x</mi><mo>*</mo></msup><mo>)</mo><mo>=</mo><mn>0</mn><mspace width=".5em"/><mtext>for every i</mtext></mtd></mtr></mtable></math>

An inequality is active when it holds with equality. Define

<math display="block" aria-label="Active inequality indices"><mi>I</mi><mo>(</mo><msup><mi>x</mi><mo>*</mo></msup><mo>)</mo><mo>=</mo><mo>{</mo><mi>i</mi><mo>:</mo><msub><mi>g</mi><mi>i</mi></msub><mo>(</mo><msup><mi>x</mi><mo>*</mo></msup><mo>)</mo><mo>=</mo><mn>0</mn><mo>}</mo></math>

Complementary slackness sets the multiplier of every inactive inequality to zero. It does not require an active inequality to have a positive multiplier.

## 4. Linear independence: at least one nonzero coefficient

A family of vectors is linearly independent if the only combination yielding the zero vector uses zero for **every** coefficient:

<math display="block" aria-label="Definition of linear independence"><munder><mo>∑</mo><mrow><mi>k</mi></mrow></munder><msub><mi>c</mi><mi>k</mi></msub><msub><mi>v</mi><mi>k</mi></msub><mo>=</mo><mn>0</mn><mo>⇒</mo><mtext>every coefficient is zero</mtext></math>

Dependence means there is a coefficient vector with **at least one** nonzero component whose combination is zero. It does not require every coefficient to be nonzero. For example,

<math display="block" aria-label="A dependent family with one zero coefficient"><mtable columnalign="left"><mtr><mtd><msub><mi>v</mi><mi>1</mi></msub><mo>=</mo><mo>(</mo><mn>1</mn><mo>,</mo><mn>0</mn><mo>)</mo><mo>,</mo><msub><mi>v</mi><mi>2</mi></msub><mo>=</mo><mo>(</mo><mn>0</mn><mo>,</mo><mn>1</mn><mo>)</mo><mo>,</mo><msub><mi>v</mi><mi>3</mi></msub><mo>=</mo><mo>(</mo><mn>2</mn><mo>,</mo><mn>0</mn><mo>)</mo></mtd></mtr><mtr><mtd><mn>2</mn><msub><mi>v</mi><mi>1</mi></msub><mo>+</mo><mn>0</mn><msub><mi>v</mi><mi>2</mi></msub><mo>−</mo><msub><mi>v</mi><mi>3</mi></msub><mo>=</mo><mn>0</mn></mtd></mtr></mtable></math>

The coefficients (2, 0, −1) are a nonzero vector. The zero middle coefficient does not rescue independence. With vectors arranged as columns, independence is equivalent to full column rank.

## 5. The shared proof: exclude an abnormal Fritz John multiplier

For a smooth problem, a local minimum satisfies the Fritz John necessary conditions without a CQ. Evaluate the gradients below at <math><msup><mi>x</mi><mo>*</mo></msup></math>, restrict the inequality sum to the active set, and set inactive multipliers to zero:

<math display="block" aria-label="Fritz John necessary conditions"><mtable columnalign="left"><mtr><mtd><mi>α</mi><mo>∇</mo><mi>f</mi><mo>+</mo><munder><mo>∑</mo><mrow><mi>i</mi><mo>∈</mo><mi>I</mi></mrow></munder><msub><mi>λ</mi><mi>i</mi></msub><mo>∇</mo><msub><mi>g</mi><mi>i</mi></msub><mo>+</mo><munder><mo>∑</mo><mrow><mi>j</mi></mrow></munder><msub><mi>ν</mi><mi>j</mi></msub><mo>∇</mo><msub><mi>h</mi><mi>j</mi></msub><mo>=</mo><mn>0</mn></mtd></mtr><mtr><mtd><mi>α</mi><mo>≥</mo><mn>0</mn><mo>,</mo><mi>λ</mi><mo>≥</mo><mn>0</mn><mo>,</mo><mo>(</mo><mi>α</mi><mo>,</mo><mi>λ</mi><mo>,</mo><mi>ν</mi><mo>)</mo><mo>≠</mo><mn>0</mn></mtd></mtr></mtable></math>

Feasibility and complementary slackness also hold. The difference from KKT is the extra objective multiplier <math><mi>α</mi></math>. If it is positive, divide all multipliers by it:

<math display="block" aria-label="Normalize a positive objective multiplier"><mo>∇</mo><mi>f</mi><mo>+</mo><munder><mo>∑</mo><mrow><mi>i</mi><mo>∈</mo><mi>I</mi></mrow></munder><mfrac><mrow><msub><mi>λ</mi><mi>i</mi></msub></mrow><mrow><mi>α</mi></mrow></mfrac><mo>∇</mo><msub><mi>g</mi><mi>i</mi></msub><mo>+</mo><munder><mo>∑</mo><mrow><mi>j</mi></mrow></munder><mfrac><mrow><msub><mi>ν</mi><mi>j</mi></msub></mrow><mrow><mi>α</mi></mrow></mfrac><mo>∇</mo><msub><mi>h</mi><mi>j</mi></msub><mo>=</mo><mn>0</mn></math>

This is KKT. The difficulty is the abnormal case <math><mi>α</mi></math> = 0: the objective disappears and constraint gradients alone satisfy a nontrivial cancellation relation. LICQ and MFCQ rule out that case.

Why does Fritz John appear? With no equalities, a direction that strictly decreases the objective and every active constraint would contradict local minimality:

<math display="block" aria-label="A direction contradicting local minimality"><msup><mrow><mo>∇</mo><mi>f</mi></mrow><mo>⊤</mo></msup><mi>d</mi><mo>&lt;</mo><mn>0</mn><mo>,</mo><msup><mrow><mo>∇</mo><msub><mi>g</mi><mi>i</mi></msub></mrow><mo>⊤</mo></msup><mi>d</mi><mo>&lt;</mo><mn>0</mn><mspace width=".5em"/><mtext>for i ∈ I</mtext></math>

For a sufficiently small positive step, the active inequalities become strict, inactive inequalities keep their slack by continuity, and the objective decreases. A theorem of alternatives converts the absence of such a direction into a nonzero nonnegative combination of these gradients equal to zero. That combination is Fritz John.

For nonlinear equalities, satisfying their linearized equations alone does not make a straight step feasible. If their gradients are independent, the implicit function theorem supplies feasible curves with the required tangent. If the equality gradients are dependent, their dependence already supplies an abnormal Fritz John relation. The unrestricted equality multipliers reflect these equality directions.

### LICQ: independence prevents cancellation

LICQ requires the following entire family to be linearly independent:

<math display="block" aria-label="LICQ gradient family"><mo>{</mo><mo>∇</mo><msub><mi>g</mi><mi>i</mi></msub><mo>:</mo><mi>i</mi><mo>∈</mo><mi>I</mi><mo>}</mo><mo>∪</mo><mo>{</mo><mo>∇</mo><msub><mi>h</mi><mi>j</mi></msub><mo>:</mo><mtext>j = 1, …, p</mtext><mo>}</mo></math>

Suppose the Fritz John objective multiplier were zero. Then

<math display="block" aria-label="An abnormal Fritz John relation"><munder><mo>∑</mo><mrow><mi>i</mi><mo>∈</mo><mi>I</mi></mrow></munder><msub><mi>λ</mi><mi>i</mi></msub><mo>∇</mo><msub><mi>g</mi><mi>i</mi></msub><mo>+</mo><munder><mo>∑</mo><mrow><mi>j</mi></mrow></munder><msub><mi>ν</mi><mi>j</mi></msub><mo>∇</mo><msub><mi>h</mi><mi>j</mi></msub><mo>=</mo><mn>0</mn></math>

Independence forces every coefficient to be zero. Together with <math><mi>α</mi></math> = 0, that contradicts the nonzero-multiplier condition. Hence <math><mi>α</mi></math> is positive and normalization gives KKT.

LICQ also makes the KKT multipliers unique at this point: subtracting two stationarity equations would give another zero combination of the same independent gradients. Neither argument requires a convex objective or convex constraints.

### MFCQ: project the cancellation onto an inward direction

MFCQ requires independent equality gradients and a direction <math><mi>d</mi></math> such that

<math display="block" aria-label="MFCQ common inward direction"><mtable columnalign="left"><mtr><mtd><msup><mrow><mo>∇</mo><msub><mi>h</mi><mi>j</mi></msub></mrow><mo>⊤</mo></msup><mi>d</mi><mo>=</mo><mn>0</mn><mspace width=".5em"/><mtext>for every j</mtext></mtd></mtr><mtr><mtd><msup><mrow><mo>∇</mo><msub><mi>g</mi><mi>i</mi></msub></mrow><mo>⊤</mo></msup><mi>d</mi><mo>&lt;</mo><mn>0</mn><mspace width=".5em"/><mtext>for every i ∈ I</mtext></mtd></mtr></mtable></math>

The direction preserves the equalities to first order and moves strictly inward for every active inequality. It need not improve the objective.

Again suppose <math><mi>α</mi></math> = 0 in Fritz John. Take the inner product with <math><mi>d</mi></math>. The equality terms vanish, leaving

<math display="block" aria-label="Dotting the abnormal relation with the inward direction"><munder><mo>∑</mo><mrow><mi>i</mi><mo>∈</mo><mi>I</mi></mrow></munder><msub><mi>λ</mi><mi>i</mi></msub><msup><mrow><mo>∇</mo><msub><mi>g</mi><mi>i</mi></msub></mrow><mo>⊤</mo></msup><mi>d</mi><mo>=</mo><mn>0</mn></math>

Every inequality multiplier is nonnegative and every corresponding directional derivative is strictly negative. A positive multiplier would make the sum strictly negative. Therefore all inequality multipliers are zero. Independence of the equality gradients then forces all equality multipliers to zero. This contradicts nontriviality, so normalization gives KKT.

MFCQ permits some dependence among inequality gradients. For example,

<math display="block" aria-label="Dependent gradients that still satisfy MFCQ"><mtable columnalign="left"><mtr><mtd><munder><mo>min</mo><mi>x</mi></munder><mo>(</mo><mo>−</mo><mi>x</mi><mo>)</mo><mo>,</mo><mi>x</mi><mo>≤</mo><mn>0</mn><mo>,</mo><mn>2</mn><mi>x</mi><mo>≤</mo><mn>0</mn></mtd></mtr><mtr><mtd><mi>d</mi><mo>=</mo><mo>−</mo><mn>1</mn><mo>,</mo><mn>1</mn><mi>d</mi><mo>&lt;</mo><mn>0</mn><mo>,</mo><mn>2</mn><mi>d</mi><mo>&lt;</mo><mn>0</mn></mtd></mtr><mtr><mtd><mo>−</mo><mn>1</mn><mo>+</mo><msub><mi>λ</mi><mi>1</mi></msub><mo>+</mo><mn>2</mn><msub><mi>λ</mi><mi>2</mi></msub><mo>=</mo><mn>0</mn></mtd></mtr></mtable></math>

At the optimum zero, the active gradients 1 and 2 are dependent, so LICQ fails. The direction −1 still moves inward for both, so MFCQ holds. The KKT multipliers can be (1, 0) or (0, 1/2). Dependence need not destroy KKT; it can merely destroy multiplier uniqueness. LICQ implies MFCQ, but the reverse implication fails.

### Slater: convexity produces the inward direction

Assume the inequality functions are differentiable and convex, the equalities are affine, and a strict feasible point exists:

<math display="block" aria-label="A strict feasible point for convex inequalities"><mtable columnalign="left"><mtr><mtd><msub><mi>g</mi><mi>i</mi></msub><mo>(</mo><mover><mi>x</mi><mo>¯</mo></mover><mo>)</mo><mo>&lt;</mo><mn>0</mn><mspace width=".5em"/><mtext>for every i</mtext></mtd></mtr><mtr><mtd><mi>A</mi><mover><mi>x</mi><mo>¯</mo></mover><mo>=</mo><mi>b</mi></mtd></mtr></mtable></math>

For this MFCQ-based proof, remove redundant equality rows first. Feasibility ensures their right sides are consistent, so this does not change the feasible set. The remaining equality matrix has full row rank. Later, setting removed equality multipliers to zero lifts the obtained KKT relation back to the original representation.

From a candidate local minimum, choose

<math display="block" aria-label="Direction from the candidate to the strict feasible point"><mi>d</mi><mo>=</mo><mover><mi>x</mi><mo>¯</mo></mover><mo>−</mo><msup><mi>x</mi><mo>*</mo></msup><mo>,</mo><mi>A</mi><mi>d</mi><mo>=</mo><mn>0</mn></math>

The equality relation follows because both endpoints satisfy the same affine equations. A differentiable convex function lies above its tangent plane. For every active inequality this gives

<math display="block" aria-label="Convexity gives an inward first derivative"><mtable columnalign="left"><mtr><mtd><msup><mrow><mo>∇</mo><msub><mi>g</mi><mi>i</mi></msub><mo>(</mo><msup><mi>x</mi><mo>*</mo></msup><mo>)</mo></mrow><mo>⊤</mo></msup><mi>d</mi><mo>≤</mo><msub><mi>g</mi><mi>i</mi></msub><mo>(</mo><mover><mi>x</mi><mo>¯</mo></mover><mo>)</mo><mo>−</mo><msub><mi>g</mi><mi>i</mi></msub><mo>(</mo><msup><mi>x</mi><mo>*</mo></msup><mo>)</mo></mtd></mtr><mtr><mtd><msub><mi>g</mi><mi>i</mi></msub><mo>(</mo><msup><mi>x</mi><mo>*</mo></msup><mo>)</mo><mo>=</mo><mn>0</mn><mo>⇒</mo><msup><mrow><mo>∇</mo><msub><mi>g</mi><mi>i</mi></msub><mo>(</mo><msup><mi>x</mi><mo>*</mo></msup><mo>)</mo></mrow><mo>⊤</mo></msup><mi>d</mi><mo>≤</mo><msub><mi>g</mi><mi>i</mi></msub><mo>(</mo><mover><mi>x</mi><mo>¯</mo></mover><mo>)</mo><mo>&lt;</mo><mn>0</mn></mtd></mtr></mtable></math>

The direction to the strict feasible point therefore decreases every active constraint **already at first order**. Apply the MFCQ argument to obtain KKT.

This necessity proof uses convexity of the constraint functions, not of the objective. A nonconvex smooth objective can also have KKT multipliers at a local minimum under this constraint structure. Convexity of the objective is needed for the sufficiency result below.

Strict feasibility without that structure is insufficient:

<math display="block" aria-label="Strict feasibility alone does not suffice for a nonlinear representation"><mtable columnalign="left"><mtr><mtd><munder><mo>min</mo><mi>x</mi></munder><mo>(</mo><mo>−</mo><mi>x</mi><mo>)</mo><mo>,</mo><msup><mi>x</mi><mn>3</mn></msup><mo>≤</mo><mn>0</mn></mtd></mtr><mtr><mtd><msup><mi>x</mi><mo>*</mo></msup><mo>=</mo><mn>0</mn><mo>,</mo><mover><mi>x</mi><mo>¯</mo></mover><mo>=</mo><mo>−</mo><mn>1</mn><mo>,</mo><mo>−</mo><mn>1</mn><mo>+</mo><mi>λ</mi><mo>·</mo><mn>0</mn><mo>≠</mo><mn>0</mn></mtd></mtr></mtable></math>

The feasible set is the half-line x ≤ 0, the optimum is zero, and −1 is a strict feasible point. But the constraint derivative at zero vanishes, making stationarity impossible. The cubic constraint function is not convex on the real line. Even a convex feasible set does not repair this nonlinear representation.

## 6. Necessity and sufficiency are different directions

| Assumptions | Valid conclusion |
| --- | --- |
| Smooth functions, local minimum, suitable CQ | KKT multipliers exist; convexity is unnecessary. |
| Smooth convex objective and inequalities, affine equalities, a KKT pair | The primal point is a global minimum; Slater is unnecessary for this direction. |
| Smooth convex problem with Slater, and an attained optimum | Global optimality is equivalent to the existence of KKT multipliers. |
| Nonconvex problem, KKT alone | The point may be a local minimum, maximum, or saddle. |

For example, zero is a KKT point of the following problem, with both bound multipliers zero, but is a maximum:

<math display="block" aria-label="A KKT point that is a maximum"><munder><mo>min</mo><mrow><mo>−</mo><mn>1</mn><mo>≤</mo><mi>x</mi><mo>≤</mo><mn>1</mn></mrow></munder><mo>(</mo><mo>−</mo><msup><mi>x</mi><mn>2</mn></msup><mo>)</mo><mo>,</mo><msup><mi>f</mi><mo>′</mo></msup><mo>(</mo><mn>0</mn><mo>)</mo><mo>=</mo><mn>0</mn></math>

Convex sufficiency has a short proof. Fix a KKT multiplier pair. The Lagrangian is convex in x, so its stationary point minimizes it globally. For any feasible x,

<math display="block" aria-label="KKT sufficiency for a convex problem"><mtable columnalign="left"><mtr><mtd><mi>f</mi><mo>(</mo><mi>x</mi><mo>)</mo><mo>≥</mo><mi>L</mi><mo>(</mo><mi>x</mi><mo>,</mo><msup><mi>λ</mi><mo>*</mo></msup><mo>,</mo><msup><mi>ν</mi><mo>*</mo></msup><mo>)</mo></mtd></mtr><mtr><mtd><mi>L</mi><mo>(</mo><mi>x</mi><mo>,</mo><msup><mi>λ</mi><mo>*</mo></msup><mo>,</mo><msup><mi>ν</mi><mo>*</mo></msup><mo>)</mo><mo>≥</mo><mi>L</mi><mo>(</mo><msup><mi>x</mi><mo>*</mo></msup><mo>,</mo><msup><mi>λ</mi><mo>*</mo></msup><mo>,</mo><msup><mi>ν</mi><mo>*</mo></msup><mo>)</mo><mo>=</mo><mi>f</mi><mo>(</mo><msup><mi>x</mi><mo>*</mo></msup><mo>)</mo></mtd></mtr></mtable></math>

Feasibility and nonnegative multipliers give the first inequality. Convexity and stationarity give the second. Complementary slackness gives the equality at the candidate. This proves global optimality without invoking Slater.

Failure of LICQ, MFCQ, or the strict-feasibility version of Slater removes those sufficient guarantees of multiplier existence. It does not by itself prove that KKT fails.

## 7. Affine constraints: why LP and convex QP are a useful special case

With only affine constraints, any attained local minimum of a differentiable objective admits KKT multipliers:

<math display="block" aria-label="Affine constraints and stationarity"><mtable columnalign="left"><mtr><mtd><mi>A</mi><mi>x</mi><mo>=</mo><mi>b</mi><mo>,</mo><mi>G</mi><mi>x</mi><mo>≤</mo><mi>h</mi></mtd></mtr><mtr><mtd><mo>∇</mo><mi>f</mi><mo>(</mo><msup><mi>x</mi><mo>*</mo></msup><mo>)</mo><mo>+</mo><msup><mrow><mi>A</mi></mrow><mo>⊤</mo></msup><mi>ν</mi><mo>+</mo><msup><mrow><mi>G</mi></mrow><mo>⊤</mo></msup><mi>λ</mi><mo>=</mo><mn>0</mn></mtd></mtr></mtable></math>

To see the reason, linearized feasible directions satisfy the actual constraints for sufficiently small positive steps. There can be no feasible direction with a negative objective directional derivative at a local minimum. Farkas' lemma then represents the negative objective gradient as a nonnegative combination of active inequality normals plus an unrestricted combination of equality normals. This is stationarity; assigning zero multipliers to inactive inequalities gives complementarity.

This polyhedral argument needs neither LICQ nor a strictly feasible point. For example,

<math display="block" aria-label="Affine constraints can admit KKT even without LICQ or strict feasibility"><mtable columnalign="left"><mtr><mtd><munder><mo>min</mo><mi>x</mi></munder><mi>x</mi><mo>,</mo><mi>x</mi><mo>≤</mo><mn>0</mn><mo>,</mo><mo>−</mo><mi>x</mi><mo>≤</mo><mn>0</mn></mtd></mtr><mtr><mtd><msup><mi>x</mi><mo>*</mo></msup><mo>=</mo><mn>0</mn><mo>,</mo><msub><mi>λ</mi><mi>1</mi></msub><mo>=</mo><mn>0</mn><mo>,</mo><msub><mi>λ</mi><mi>2</mi></msub><mo>=</mo><mn>1</mn></mtd></mtr><mtr><mtd><mn>1</mn><mo>+</mo><msub><mi>λ</mi><mi>1</mi></msub><mo>−</mo><msub><mi>λ</mi><mi>2</mi></msub><mo>=</mo><mn>0</mn></mtd></mtr></mtable></math>

Both constraints are active and their gradients are dependent. No point satisfies both inequalities strictly. Nevertheless, the displayed multipliers satisfy KKT.

For a QP with a symmetric positive semidefinite Hessian and affine constraints, KKT is therefore necessary and sufficient for an attained optimum. A positive definite Hessian also makes the primal optimum unique whenever the feasible set is nonempty. Redundant constraints can still make the multipliers nonunique.

## 8. KKT does not guarantee that the optimizer is differentiable

Consider a parameterized ramp QP:

<math display="block" aria-label="A unique optimal solution with a kink"><mtable columnalign="left"><mtr><mtd><msup><mi>a</mi><mo>*</mo></msup><mo>(</mo><mi>η</mi><mo>)</mo><mo>=</mo><munder><mo>arg min</mo><mrow><mn>.4</mn><mo>≤</mo><mi>a</mi><mo>≤</mo><mn>.6</mn></mrow></munder><mo>(</mo><mfrac><mrow><mn>1</mn></mrow><mrow><mn>2</mn></mrow></mfrac><msup><mi>a</mi><mn>2</mn></msup><mo>−</mo><mi>η</mi><mi>a</mi><mo>)</mo></mtd></mtr><mtr><mtd><msup><mi>a</mi><mo>*</mo></msup><mo>(</mo><mi>η</mi><mo>)</mo><mo>=</mo><mo>min</mo><mo>{</mo><mn>.6</mn><mo>,</mo><mo>max</mo><mo>{</mo><mn>.4</mn><mo>,</mo><mi>η</mi><mo>}</mo><mo>}</mo></mtd></mtr></mtable></math>

For every <math><mi>η</mi></math>, the optimum is unique and admits KKT multipliers. Near <math><mi>η</mi></math> = 0.6, the action derivative is 1 on the left and 0 on the right. The ordinary derivative at the boundary does not exist. At that point, the upper bound is active but <math><msub><msup><mi>λ</mi><mo>*</mo></msup><mtext>upper</mtext></msub></math> = 0, so strict complementarity fails.

For implicit differentiation, collect the primal and dual variables in <math><msup><mi>y</mi><mo>*</mo></msup></math> and write the equality part of KKT as a residual:

<math display="block" aria-label="Implicit differentiation requires an invertible residual Jacobian"><mtable columnalign="left"><mtr><mtd><mi>F</mi><mo>(</mo><msup><mi>y</mi><mo>*</mo></msup><mo>(</mo><mi>η</mi><mo>)</mo><mo>,</mo><mi>η</mi><mo>)</mo><mo>=</mo><mn>0</mn></mtd></mtr><mtr><mtd><msub><mi>F</mi><mi>y</mi></msub><mfrac><mrow><mo>∂</mo><msup><mi>y</mi><mo>*</mo></msup></mrow><mrow><mo>∂</mo><mi>η</mi></mrow></mfrac><mo>=</mo><mo>−</mo><msub><mi>F</mi><mi>η</mi></msub></mtd></mtr></mtable></math>

Using the inverse formula requires a continuously differentiable residual and a nonsingular <math><msub><mi>F</mi><mi>y</mi></msub></math> at the solution. With sufficiently smooth problem data, LICQ, a second-order sufficient condition, and strict complementarity form a familiar sufficient set for a smooth local primal–dual solution branch. They are sufficient conditions, not an assertion that each is necessary for every differentiable primal solution map.

There are three separate checks: whether KKT multipliers exist, whether KKT certifies the intended optimum, and whether the chosen solution branch can be differentiated.

## References

- Boyd, S., and Vandenberghe, L. (2004). *Convex Optimization*, Chapter 5, especially §§5.2.3 and 5.5.3. [Authors' official book page](https://web.stanford.edu/~boyd/cvxbook/).
- Farina, G. (2025). *Lagrange multipliers and KKT conditions*, MIT 6.7220/15.084, Lecture 7. Affine normal cones, LICQ, and Slater. [Official lecture PDF](https://www.mit.edu/~gfarina/2025/67220s25_L07_kkt/L07.pdf).
- Sun, Y. (2024). *Notes on constraint qualifications*, STATS 606. Fritz John and MFCQ. [Official course note](https://websites.umich.edu/~yuekai/stats606/posts/constraint-qualifications.html).
- Amos, B., and Kolter, J. Z. (2017). *OptNet: Differentiable Optimization as a Layer in Neural Networks*. ICML, PMLR 70, 136–145. [Paper and metadata](https://proceedings.mlr.press/v70/amos17a.html).

<!-- ko -->

최적해가 반드시 KKT 조건을 만족하는 것은 아니다. 기억해야 할 명제는 **“연속적으로 미분 가능한 문제의 local minimum에서 적절한 제약 정규성 조건(CQ)이 성립하면 KKT 승수가 존재한다”**이다. Convexity는 다른 질문, 즉 이미 KKT를 만족하는 점이 global optimum인지에 답한다.

Ramp 제한, 퇴화된 제약 표현, LICQ·MFCQ·Slater의 짧은 증명을 순서대로 연결한다.

## 1. Ramp 제한: 최적점인데 왜 기울기가 0이 아닌가?

설비 출력을 높일수록 이익이 커지지만, 이번 시점에는 hard ramp 때문에 출력이 0.4와 0.6 사이여야 한다고 하자. 출력의 음수를 최소화하면 상한을 선택한다.

<math display="block" aria-label="Linear reward with an upper ramp bound"><mtable columnalign="left"><mtr><mtd><munder><mo>min</mo><mrow><mn>.4</mn><mo>≤</mo><mi>a</mi><mo>≤</mo><mn>.6</mn></mrow></munder><mo>(</mo><mo>−</mo><mi>a</mi><mo>)</mo></mtd></mtr><mtr><mtd><msup><mi>a</mi><mo>*</mo></msup><mo>=</mo><mn>.6</mn><mo>,</mo><mi>λ</mi><mo>=</mo><mn>1</mn><mo>,</mo><mo>−</mo><mn>1</mn><mo>+</mo><mi>λ</mi><mo>=</mo><mn>0</mn></mtd></mtr></mtable></math>

최적점에서도 목적함수의 기울기는 −1이다. 출력을 더 높이면 여전히 목적함수가 개선되지만, 활성 상한 제약 때문에 그 방향으로 갈 수 없다. 상한 제약의 기울기는 +1이므로 승수 1을 곱하면 목적함수 기울기와 합이 0이 된다. 하한은 여유가 있으므로 승수가 0이다.

KKT는 이처럼 **목적함수를 개선하려는 방향을 활성 제약이 막고 있는 관계**를 gradient와 승수로 표현한다. 이 설명은 일차 미분에 의존한다. 실제 움직임을 막는 제약이 그 사실을 gradient로 표현하지 못하면 문제가 생긴다.

## 2. Global optimum인데 KKT가 성립하지 않는 반례

<math display="block" aria-label="A convex optimum without KKT multipliers"><munder><mo>min</mo><mi>x</mi></munder><mi>x</mi><mo>,</mo><mspace width="1em"/><mtext>subject to</mtext><mspace width=".5em"/><msup><mi>x</mi><mn>2</mn></msup><mo>≤</mo><mn>0</mn></math>

가능한 점은 <math><msup><mi>x</mi><mo>*</mo></msup></math> = 0 하나뿐이다. 따라서 유일한 global minimum이며, 목적함수와 제약함수 모두 convex이다. 그런데 stationarity는 성립할 수 없다.

<math display="block" aria-label="Stationarity is impossible at zero"><mtable columnalign="left"><mtr><mtd><mi>L</mi><mo>(</mo><mi>x</mi><mo>,</mo><mi>λ</mi><mo>)</mo><mo>=</mo><mi>x</mi><mo>+</mo><mi>λ</mi><msup><mi>x</mi><mn>2</mn></msup></mtd></mtr><mtr><mtd><mn>1</mn><mo>+</mo><mn>2</mn><mi>λ</mi><mi>x</mi><mo>=</mo><mn>0</mn><mo>⇒</mo><mn>1</mn><mo>+</mo><mn>2</mn><mi>λ</mi><mo>·</mo><mn>0</mn><mo>=</mo><mn>0</mn></mtd></mtr></mtable></math>

어떤 유한한 승수를 넣어도 최적점에서 왼쪽은 1이다. 실제 제약은 모든 움직임을 막지만, 일차 선형화는 모든 방향을 허용하는 것처럼 보인다.

<math display="block" aria-label="The linearized constraint misses the obstruction"><mi>g</mi><mo>(</mo><mn>0</mn><mo>)</mo><mo>+</mo><msup><mi>g</mi><mo>′</mo></msup><mo>(</mo><mn>0</mn><mo>)</mo><mi>d</mi><mo>=</mo><mn>0</mn><mo>≤</mo><mn>0</mn></math>

왼쪽으로 움직이면 목적함수는 이동 크기에 비례해 감소한다. 반면 제약 위반은 이동 크기의 제곱으로 나타난다. 제약의 일차 미분이 이 이차적인 장애물을 놓치는 것이다.

같은 feasible set을 등식 x = 0으로 표현하면 제약 gradient는 1이다. 승수 −1로 stationarity가 성립한다.

<math display="block" aria-label="An equivalent equality has a nonzero gradient"><mi>L</mi><mo>(</mo><mi>x</mi><mo>,</mo><mi>ν</mi><mo>)</mo><mo>=</mo><mi>x</mi><mo>+</mo><mi>ν</mi><mi>x</mi><mo>,</mo><mn>1</mn><mo>+</mo><mi>ν</mi><mo>=</mo><mn>0</mn><mo>⇒</mo><mi>ν</mi><mo>=</mo><mo>−</mo><mn>1</mn></math>

목적함수와 feasible set이 같아도, **제약을 어떤 함수로 표현했는지**에 따라 KKT 승수의 존재 여부가 달라질 수 있다.

## 3. “최적해가 KKT를 만족한다”의 정확한 뜻

실수 연속변수의 다음 문제를 생각하자. 함수들은 후보점 주변에서 <math><msup><mi>C</mi><mn>1</mn></msup></math>, 즉 연속적으로 미분 가능하다고 가정한다.

<math display="block" aria-label="Smooth constrained minimization problem"><mtable columnalign="left"><mtr><mtd><munder><mo>min</mo><mrow><mi>x</mi><mo>∈</mo><msup><mi>ℝ</mi><mi>n</mi></msup></mrow></munder><mi>f</mi><mo>(</mo><mi>x</mi><mo>)</mo></mtd></mtr><mtr><mtd><msub><mi>g</mi><mi>i</mi></msub><mo>(</mo><mi>x</mi><mo>)</mo><mo>≤</mo><mn>0</mn><mo>,</mo><mtext> i = 1, …, m</mtext></mtd></mtr><mtr><mtd><msub><mi>h</mi><mi>j</mi></msub><mo>(</mo><mi>x</mi><mo>)</mo><mo>=</mo><mn>0</mn><mo>,</mo><mtext> j = 1, …, p</mtext></mtd></mtr></mtable></math>

“KKT를 만족한다”는 것은 비음수 부등식 승수와 부호 제한이 없는 등식 승수가 **존재하여** 네 조건을 동시에 만족한다는 뜻이다. Stationarity는 다음과 같다.

<math display="block" aria-label="KKT stationarity"><mo>∇</mo><mi>f</mi><mo>(</mo><msup><mi>x</mi><mo>*</mo></msup><mo>)</mo><mo>+</mo><munder><mo>∑</mo><mrow><mi>i</mi></mrow></munder><msub><mi>λ</mi><mi>i</mi></msub><mo>∇</mo><msub><mi>g</mi><mi>i</mi></msub><mo>(</mo><msup><mi>x</mi><mo>*</mo></msup><mo>)</mo><mo>+</mo><munder><mo>∑</mo><mrow><mi>j</mi></mrow></munder><msub><mi>ν</mi><mi>j</mi></msub><mo>∇</mo><msub><mi>h</mi><mi>j</mi></msub><mo>(</mo><msup><mi>x</mi><mo>*</mo></msup><mo>)</mo><mo>=</mo><mn>0</mn></math>

나머지는 primal feasibility, dual feasibility, complementary slackness이다.

<math display="block" aria-label="Primal feasibility, dual feasibility, and complementarity"><mtable columnalign="left"><mtr><mtd><msub><mi>g</mi><mi>i</mi></msub><mo>(</mo><msup><mi>x</mi><mo>*</mo></msup><mo>)</mo><mo>≤</mo><mn>0</mn><mo>,</mo><msub><mi>h</mi><mi>j</mi></msub><mo>(</mo><msup><mi>x</mi><mo>*</mo></msup><mo>)</mo><mo>=</mo><mn>0</mn></mtd></mtr><mtr><mtd><mi>λ</mi><mo>≥</mo><mn>0</mn><mo>,</mo><msub><mi>λ</mi><mi>i</mi></msub><msub><mi>g</mi><mi>i</mi></msub><mo>(</mo><msup><mi>x</mi><mo>*</mo></msup><mo>)</mo><mo>=</mo><mn>0</mn><mspace width=".5em"/><mtext>for every i</mtext></mtd></mtr></mtable></math>

등호로 만족되는 부등식이 활성 제약이다. 그 인덱스 집합을 다음과 같이 정의한다.

<math display="block" aria-label="Active inequality indices"><mi>I</mi><mo>(</mo><msup><mi>x</mi><mo>*</mo></msup><mo>)</mo><mo>=</mo><mo>{</mo><mi>i</mi><mo>:</mo><msub><mi>g</mi><mi>i</mi></msub><mo>(</mo><msup><mi>x</mi><mo>*</mo></msup><mo>)</mo><mo>=</mo><mn>0</mn><mo>}</mo></math>

Complementary slackness는 비활성 부등식의 승수를 0으로 만든다. 활성 부등식의 승수가 반드시 양수여야 한다는 뜻은 아니다.

## 4. 선형독립: 계수 중 하나라도 0이 아니면

벡터들이 선형독립이라는 것은, 그 선형결합으로 영벡터를 만들려면 **모든 계수가 0이어야 한다**는 뜻이다.

<math display="block" aria-label="Definition of linear independence"><munder><mo>∑</mo><mrow><mi>k</mi></mrow></munder><msub><mi>c</mi><mi>k</mi></msub><msub><mi>v</mi><mi>k</mi></msub><mo>=</mo><mn>0</mn><mo>⇒</mo><mtext>every coefficient is zero</mtext></math>

반대로 **계수 중 적어도 하나가 0이 아닌** 조합으로 영벡터를 만들 수 있으면 선형종속이다. 모든 계수가 각각 0이 아니어야 하는 것은 아니다. 다음 예를 보자.

<math display="block" aria-label="A dependent family with one zero coefficient"><mtable columnalign="left"><mtr><mtd><msub><mi>v</mi><mi>1</mi></msub><mo>=</mo><mo>(</mo><mn>1</mn><mo>,</mo><mn>0</mn><mo>)</mo><mo>,</mo><msub><mi>v</mi><mi>2</mi></msub><mo>=</mo><mo>(</mo><mn>0</mn><mo>,</mo><mn>1</mn><mo>)</mo><mo>,</mo><msub><mi>v</mi><mi>3</mi></msub><mo>=</mo><mo>(</mo><mn>2</mn><mo>,</mo><mn>0</mn><mo>)</mo></mtd></mtr><mtr><mtd><mn>2</mn><msub><mi>v</mi><mi>1</mi></msub><mo>+</mo><mn>0</mn><msub><mi>v</mi><mi>2</mi></msub><mo>−</mo><msub><mi>v</mi><mi>3</mi></msub><mo>=</mo><mn>0</mn></mtd></mtr></mtable></math>

계수벡터 (2, 0, −1)은 영벡터가 아니다. 가운데 계수가 0이어도 선형종속이다. 벡터들을 열로 모은 행렬에서는 선형독립이 full column rank와 같다.

## 5. 공통 증명: Fritz John에서 목적함수가 사라지는 경우를 배제한다

매끄러운 문제의 local minimum에서는 CQ 없이도 Fritz John 필요조건이 성립한다. 아래 gradient들은 모두 <math><msup><mi>x</mi><mo>*</mo></msup></math>에서 평가하고, 부등식은 활성 집합에 대해서만 합한다. 비활성 부등식 승수는 0으로 둔다.

<math display="block" aria-label="Fritz John necessary conditions"><mtable columnalign="left"><mtr><mtd><mi>α</mi><mo>∇</mo><mi>f</mi><mo>+</mo><munder><mo>∑</mo><mrow><mi>i</mi><mo>∈</mo><mi>I</mi></mrow></munder><msub><mi>λ</mi><mi>i</mi></msub><mo>∇</mo><msub><mi>g</mi><mi>i</mi></msub><mo>+</mo><munder><mo>∑</mo><mrow><mi>j</mi></mrow></munder><msub><mi>ν</mi><mi>j</mi></msub><mo>∇</mo><msub><mi>h</mi><mi>j</mi></msub><mo>=</mo><mn>0</mn></mtd></mtr><mtr><mtd><mi>α</mi><mo>≥</mo><mn>0</mn><mo>,</mo><mi>λ</mi><mo>≥</mo><mn>0</mn><mo>,</mo><mo>(</mo><mi>α</mi><mo>,</mo><mi>λ</mi><mo>,</mo><mi>ν</mi><mo>)</mo><mo>≠</mo><mn>0</mn></mtd></mtr></mtable></math>

Feasibility와 complementary slackness도 함께 성립한다. KKT와의 차이는 목적함수 앞의 추가 승수 <math><mi>α</mi></math>이다. 이것이 양수이면 식 전체를 나눈다.

<math display="block" aria-label="Normalize a positive objective multiplier"><mo>∇</mo><mi>f</mi><mo>+</mo><munder><mo>∑</mo><mrow><mi>i</mi><mo>∈</mo><mi>I</mi></mrow></munder><mfrac><mrow><msub><mi>λ</mi><mi>i</mi></msub></mrow><mrow><mi>α</mi></mrow></mfrac><mo>∇</mo><msub><mi>g</mi><mi>i</mi></msub><mo>+</mo><munder><mo>∑</mo><mrow><mi>j</mi></mrow></munder><mfrac><mrow><msub><mi>ν</mi><mi>j</mi></msub></mrow><mrow><mi>α</mi></mrow></mfrac><mo>∇</mo><msub><mi>h</mi><mi>j</mi></msub><mo>=</mo><mn>0</mn></math>

바로 KKT이다. 어려운 경우는 <math><mi>α</mi></math> = 0이다. 목적함수는 사라지고 제약 gradient들끼리만 비자명하게 상쇄된다. LICQ와 MFCQ는 이 비정상적인 경우를 배제한다.

Fritz John은 왜 나올까? 우선 등식제약이 없다면, 목적함수와 모든 활성 제약을 엄격하게 감소시키는 방향은 local minimum에서 존재할 수 없다.

<math display="block" aria-label="A direction contradicting local minimality"><msup><mrow><mo>∇</mo><mi>f</mi></mrow><mo>⊤</mo></msup><mi>d</mi><mo>&lt;</mo><mn>0</mn><mo>,</mo><msup><mrow><mo>∇</mo><msub><mi>g</mi><mi>i</mi></msub></mrow><mo>⊤</mo></msup><mi>d</mi><mo>&lt;</mo><mn>0</mn><mspace width=".5em"/><mtext>for i ∈ I</mtext></math>

그 방향으로 충분히 작은 양의 보폭을 이동하면 활성 제약은 엄격하게 만족되고, 비활성 제약의 기존 여유는 연속성 때문에 유지되며, 목적함수는 감소한다. Local minimum이라는 가정에 모순이다. 선형 대안정리는 이런 방향의 부재를 “gradient들의 비음수 가중합이 0인 비자명한 관계”로 바꾼다. 그 관계가 Fritz John이다.

비선형 등식에서는 선형화된 등식을 만족하는 직선 이동이 실제 등식을 만족한다고 단정하면 안 된다. 등식 gradient가 독립이면 implicit function theorem으로 같은 접선 방향의 실제 feasible curve를 다룰 수 있다. 등식 gradient가 종속이면 그 종속관계 자체가 비정상 Fritz John 관계를 준다. 등식 승수에 부호 제한이 없는 이유도 이 등식 방향과 연결된다.

### LICQ: 선형독립이면 제약들끼리 상쇄할 수 없다

LICQ는 다음 gradient들을 **전부 함께** 모았을 때 선형독립이라는 조건이다.

<math display="block" aria-label="LICQ gradient family"><mo>{</mo><mo>∇</mo><msub><mi>g</mi><mi>i</mi></msub><mo>:</mo><mi>i</mi><mo>∈</mo><mi>I</mi><mo>}</mo><mo>∪</mo><mo>{</mo><mo>∇</mo><msub><mi>h</mi><mi>j</mi></msub><mo>:</mo><mtext>j = 1, …, p</mtext><mo>}</mo></math>

Fritz John에서 <math><mi>α</mi></math> = 0이라고 가정하자. 그러면

<math display="block" aria-label="An abnormal Fritz John relation"><munder><mo>∑</mo><mrow><mi>i</mi><mo>∈</mo><mi>I</mi></mrow></munder><msub><mi>λ</mi><mi>i</mi></msub><mo>∇</mo><msub><mi>g</mi><mi>i</mi></msub><mo>+</mo><munder><mo>∑</mo><mrow><mi>j</mi></mrow></munder><msub><mi>ν</mi><mi>j</mi></msub><mo>∇</mo><msub><mi>h</mi><mi>j</mi></msub><mo>=</mo><mn>0</mn></math>

선형독립이므로 모든 계수가 0이어야 한다. <math><mi>α</mi></math>까지 0이면 승수 전체가 0인데, Fritz John은 이를 금지한다. 따라서 <math><mi>α</mi></math>는 양수이고, 나누면 KKT가 성립한다.

LICQ는 해당 점에서 KKT 승수의 유일성도 준다. 두 stationarity 식을 빼면 같은 독립 gradient들의 선형결합이 0이므로 두 승수가 같아야 한다. 이 증명에는 목적함수나 제약함수의 convexity가 필요하지 않다.

### MFCQ: 공통 내부 방향과 내적하면 상쇄가 불가능하다

MFCQ는 등식 gradient들이 독립이고 다음을 만족하는 방향 <math><mi>d</mi></math>가 있다는 조건이다.

<math display="block" aria-label="MFCQ common inward direction"><mtable columnalign="left"><mtr><mtd><msup><mrow><mo>∇</mo><msub><mi>h</mi><mi>j</mi></msub></mrow><mo>⊤</mo></msup><mi>d</mi><mo>=</mo><mn>0</mn><mspace width=".5em"/><mtext>for every j</mtext></mtd></mtr><mtr><mtd><msup><mrow><mo>∇</mo><msub><mi>g</mi><mi>i</mi></msub></mrow><mo>⊤</mo></msup><mi>d</mi><mo>&lt;</mo><mn>0</mn><mspace width=".5em"/><mtext>for every i ∈ I</mtext></mtd></mtr></mtable></math>

등식을 일차적으로 유지하면서 모든 활성 부등식의 안쪽으로 동시에 들어가는 방향이다. 목적함수를 개선하는 방향일 필요는 없다.

다시 Fritz John에서 <math><mi>α</mi></math> = 0이라고 가정하고 그 식을 <math><mi>d</mi></math>와 내적한다. 등식 항은 사라지고 다음만 남는다.

<math display="block" aria-label="Dotting the abnormal relation with the inward direction"><munder><mo>∑</mo><mrow><mi>i</mi><mo>∈</mo><mi>I</mi></mrow></munder><msub><mi>λ</mi><mi>i</mi></msub><msup><mrow><mo>∇</mo><msub><mi>g</mi><mi>i</mi></msub></mrow><mo>⊤</mo></msup><mi>d</mi><mo>=</mo><mn>0</mn></math>

각 항은 비음수 승수와 엄격히 음수인 방향미분의 곱이다. 승수 하나라도 양수이면 합은 음수다. 합이 0이려면 부등식 승수가 모두 0이어야 한다. 그러면 등식 gradient의 독립성에 의해 등식 승수도 모두 0이다. 비자명성에 모순이므로 <math><mi>α</mi></math>는 양수이고 KKT를 얻는다.

MFCQ는 부등식 gradient 사이의 일부 종속성을 허용한다.

<math display="block" aria-label="Dependent gradients that still satisfy MFCQ"><mtable columnalign="left"><mtr><mtd><munder><mo>min</mo><mi>x</mi></munder><mo>(</mo><mo>−</mo><mi>x</mi><mo>)</mo><mo>,</mo><mi>x</mi><mo>≤</mo><mn>0</mn><mo>,</mo><mn>2</mn><mi>x</mi><mo>≤</mo><mn>0</mn></mtd></mtr><mtr><mtd><mi>d</mi><mo>=</mo><mo>−</mo><mn>1</mn><mo>,</mo><mn>1</mn><mi>d</mi><mo>&lt;</mo><mn>0</mn><mo>,</mo><mn>2</mn><mi>d</mi><mo>&lt;</mo><mn>0</mn></mtd></mtr><mtr><mtd><mo>−</mo><mn>1</mn><mo>+</mo><msub><mi>λ</mi><mi>1</mi></msub><mo>+</mo><mn>2</mn><msub><mi>λ</mi><mi>2</mi></msub><mo>=</mo><mn>0</mn></mtd></mtr></mtable></math>

최적점 0에서 활성 gradient는 1과 2이므로 LICQ는 실패한다. 하지만 방향 −1은 두 제약의 안쪽으로 동시에 들어가므로 MFCQ는 성립한다. KKT 승수도 (1, 0) 또는 (0, 1/2)로 잡을 수 있다. 선형종속이 항상 KKT를 없애는 것은 아니다. 승수의 유일성만 없어질 수도 있다. LICQ는 MFCQ를 함의하지만 역은 성립하지 않는다.

### Slater: convexity가 공통 내부 방향을 만들어준다

부등식 함수는 미분 가능한 convex 함수, 등식은 affine이라고 하자. 다음과 같은 엄격한 feasible point가 존재한다.

<math display="block" aria-label="A strict feasible point for convex inequalities"><mtable columnalign="left"><mtr><mtd><msub><mi>g</mi><mi>i</mi></msub><mo>(</mo><mover><mi>x</mi><mo>¯</mo></mover><mo>)</mo><mo>&lt;</mo><mn>0</mn><mspace width=".5em"/><mtext>for every i</mtext></mtd></mtr><mtr><mtd><mi>A</mi><mover><mi>x</mi><mo>¯</mo></mover><mo>=</mo><mi>b</mi></mtd></mtr></mtable></math>

MFCQ를 경유하는 이 증명에서는 먼저 중복 등식 행을 제거한다. Feasible point가 있으므로 우변도 일관되어 있으며, 제거해도 feasible set은 같고 남은 행렬은 full row rank이다. 제거한 등식의 승수를 0으로 두면 나중에 얻은 KKT 관계를 원래 표현으로 되돌릴 수 있다.

후보 local minimum에서 엄격한 feasible point를 향하는 방향을 잡는다.

<math display="block" aria-label="Direction from the candidate to the strict feasible point"><mi>d</mi><mo>=</mo><mover><mi>x</mi><mo>¯</mo></mover><mo>−</mo><msup><mi>x</mi><mo>*</mo></msup><mo>,</mo><mi>A</mi><mi>d</mi><mo>=</mo><mn>0</mn></math>

두 점이 같은 affine 등식을 만족하므로 등식 방향 조건은 즉시 성립한다. 미분 가능한 convex 함수는 접평면보다 위에 있으므로 활성 부등식마다 다음이 성립한다.

<math display="block" aria-label="Convexity gives an inward first derivative"><mtable columnalign="left"><mtr><mtd><msup><mrow><mo>∇</mo><msub><mi>g</mi><mi>i</mi></msub><mo>(</mo><msup><mi>x</mi><mo>*</mo></msup><mo>)</mo></mrow><mo>⊤</mo></msup><mi>d</mi><mo>≤</mo><msub><mi>g</mi><mi>i</mi></msub><mo>(</mo><mover><mi>x</mi><mo>¯</mo></mover><mo>)</mo><mo>−</mo><msub><mi>g</mi><mi>i</mi></msub><mo>(</mo><msup><mi>x</mi><mo>*</mo></msup><mo>)</mo></mtd></mtr><mtr><mtd><msub><mi>g</mi><mi>i</mi></msub><mo>(</mo><msup><mi>x</mi><mo>*</mo></msup><mo>)</mo><mo>=</mo><mn>0</mn><mo>⇒</mo><msup><mrow><mo>∇</mo><msub><mi>g</mi><mi>i</mi></msub><mo>(</mo><msup><mi>x</mi><mo>*</mo></msup><mo>)</mo></mrow><mo>⊤</mo></msup><mi>d</mi><mo>≤</mo><msub><mi>g</mi><mi>i</mi></msub><mo>(</mo><mover><mi>x</mi><mo>¯</mo></mover><mo>)</mo><mo>&lt;</mo><mn>0</mn></mtd></mtr></mtable></math>

따라서 엄격한 feasible point를 향하는 방향은 모든 활성 제약을 **출발점의 일차 미분부터** 감소시킨다. 앞의 MFCQ 증명을 적용하면 KKT를 얻는다.

이 필요성 증명은 제약함수의 convexity만 사용했다. 목적함수가 매끄럽지만 nonconvex여도 이 제약 구조에서는 local minimum에 KKT 승수가 존재한다. 목적함수의 convexity는 아래의 충분성에 쓰인다.

이 구조 없이 엄격한 feasible point만 있다고 충분하지는 않다.

<math display="block" aria-label="Strict feasibility alone does not suffice for a nonlinear representation"><mtable columnalign="left"><mtr><mtd><munder><mo>min</mo><mi>x</mi></munder><mo>(</mo><mo>−</mo><mi>x</mi><mo>)</mo><mo>,</mo><msup><mi>x</mi><mn>3</mn></msup><mo>≤</mo><mn>0</mn></mtd></mtr><mtr><mtd><msup><mi>x</mi><mo>*</mo></msup><mo>=</mo><mn>0</mn><mo>,</mo><mover><mi>x</mi><mo>¯</mo></mover><mo>=</mo><mo>−</mo><mn>1</mn><mo>,</mo><mo>−</mo><mn>1</mn><mo>+</mo><mi>λ</mi><mo>·</mo><mn>0</mn><mo>≠</mo><mn>0</mn></mtd></mtr></mtable></math>

Feasible set은 x ≤ 0이고, 최적해는 0이며, −1은 엄격한 feasible point다. 그러나 최적점에서 제약 gradient가 0이므로 stationarity가 불가능하다. 세제곱 제약함수는 실수축 전체에서 convex하지 않다. Feasible set 자체가 convex여도 이런 비선형 표현의 퇴화를 해결해주지 못한다.

## 6. 필요조건과 충분조건은 방향이 다르다

| 가정 | 말할 수 있는 결론 |
| --- | --- |
| 매끄러운 함수, local minimum, 적절한 CQ | KKT 승수가 존재한다. Convexity는 필요하지 않다. |
| 매끄러운 convex 목적함수·부등식, affine 등식, KKT 충족 | 그 점은 global minimum이다. 이 방향에는 Slater가 필요하지 않다. |
| 매끄러운 convex 문제, Slater, 달성된 최적해 | Global optimality와 KKT 승수의 존재가 동치이다. |
| Nonconvex 문제에서 KKT만 충족 | Local minimum, maximum, saddle point일 수 있다. |

예를 들어 다음 문제에서 0은 두 bound 승수를 0으로 두면 KKT를 만족하지만 maximum이다.

<math display="block" aria-label="A KKT point that is a maximum"><munder><mo>min</mo><mrow><mo>−</mo><mn>1</mn><mo>≤</mo><mi>x</mi><mo>≤</mo><mn>1</mn></mrow></munder><mo>(</mo><mo>−</mo><msup><mi>x</mi><mn>2</mn></msup><mo>)</mo><mo>,</mo><msup><mi>f</mi><mo>′</mo></msup><mo>(</mo><mn>0</mn><mo>)</mo><mo>=</mo><mn>0</mn></math>

Convex 문제의 충분성 증명은 짧다. KKT 승수를 고정하면 Lagrangian은 x에 대해 convex이다. 따라서 stationary point가 그 Lagrangian의 global minimum이다. 임의의 feasible x에 대해

<math display="block" aria-label="KKT sufficiency for a convex problem"><mtable columnalign="left"><mtr><mtd><mi>f</mi><mo>(</mo><mi>x</mi><mo>)</mo><mo>≥</mo><mi>L</mi><mo>(</mo><mi>x</mi><mo>,</mo><msup><mi>λ</mi><mo>*</mo></msup><mo>,</mo><msup><mi>ν</mi><mo>*</mo></msup><mo>)</mo></mtd></mtr><mtr><mtd><mi>L</mi><mo>(</mo><mi>x</mi><mo>,</mo><msup><mi>λ</mi><mo>*</mo></msup><mo>,</mo><msup><mi>ν</mi><mo>*</mo></msup><mo>)</mo><mo>≥</mo><mi>L</mi><mo>(</mo><msup><mi>x</mi><mo>*</mo></msup><mo>,</mo><msup><mi>λ</mi><mo>*</mo></msup><mo>,</mo><msup><mi>ν</mi><mo>*</mo></msup><mo>)</mo><mo>=</mo><mi>f</mi><mo>(</mo><msup><mi>x</mi><mo>*</mo></msup><mo>)</mo></mtd></mtr></mtable></math>

Feasibility와 비음수 승수가 첫 부등식, convexity와 stationarity가 두 번째 부등식, complementary slackness가 마지막 등식을 준다. Slater 없이도 global optimality를 증명한다.

LICQ·MFCQ 또는 엄격한 feasibility 형태의 Slater가 실패했다는 사실은 그 충분조건으로 승수 존재를 보장할 수 없다는 뜻이다. KKT 자체가 반드시 실패한다는 뜻은 아니다.

## 7. Affine 제약: LP와 convex QP의 유용한 특수성

제약이 모두 affine이면, 미분 가능한 목적함수의 달성된 local minimum에서 KKT 승수가 존재한다.

<math display="block" aria-label="Affine constraints and stationarity"><mtable columnalign="left"><mtr><mtd><mi>A</mi><mi>x</mi><mo>=</mo><mi>b</mi><mo>,</mo><mi>G</mi><mi>x</mi><mo>≤</mo><mi>h</mi></mtd></mtr><mtr><mtd><mo>∇</mo><mi>f</mi><mo>(</mo><msup><mi>x</mi><mo>*</mo></msup><mo>)</mo><mo>+</mo><msup><mrow><mi>A</mi></mrow><mo>⊤</mo></msup><mi>ν</mi><mo>+</mo><msup><mrow><mi>G</mi></mrow><mo>⊤</mo></msup><mi>λ</mi><mo>=</mo><mn>0</mn></mtd></mtr></mtable></math>

이 경우 선형화된 feasible direction은 충분히 작은 양의 보폭에서 실제 제약도 만족한다. Local minimum에서는 그런 방향으로 목적함수의 방향미분이 음수일 수 없다. Farkas 보조정리는 이 방향의 부재를 “목적함수의 음의 gradient가 활성 부등식 법선의 비음수 결합과 등식 법선의 부호 제한 없는 결합으로 표현된다”로 바꾼다. 이것이 stationarity이고, 비활성 승수를 0으로 두면 complementarity도 성립한다.

이 polyhedral 논리는 LICQ나 엄격한 feasible point를 필요로 하지 않는다.

<math display="block" aria-label="Affine constraints can admit KKT even without LICQ or strict feasibility"><mtable columnalign="left"><mtr><mtd><munder><mo>min</mo><mi>x</mi></munder><mi>x</mi><mo>,</mo><mi>x</mi><mo>≤</mo><mn>0</mn><mo>,</mo><mo>−</mo><mi>x</mi><mo>≤</mo><mn>0</mn></mtd></mtr><mtr><mtd><msup><mi>x</mi><mo>*</mo></msup><mo>=</mo><mn>0</mn><mo>,</mo><msub><mi>λ</mi><mi>1</mi></msub><mo>=</mo><mn>0</mn><mo>,</mo><msub><mi>λ</mi><mi>2</mi></msub><mo>=</mo><mn>1</mn></mtd></mtr><mtr><mtd><mn>1</mn><mo>+</mo><msub><mi>λ</mi><mi>1</mi></msub><mo>−</mo><msub><mi>λ</mi><mi>2</mi></msub><mo>=</mo><mn>0</mn></mtd></mtr></mtable></math>

두 제약이 모두 활성이고 gradient는 종속이다. 둘을 동시에 엄격하게 만족하는 점도 없다. 그래도 위 승수는 KKT를 만족한다.

따라서 대칭 positive semidefinite Hessian과 affine 제약을 갖는 QP에서는 달성된 최적해에 대해 KKT가 필요충분조건이다. Hessian이 positive definite이면 feasible set이 비어 있지 않을 때 primal 최적해도 유일하다. 그래도 중복 제약 때문에 승수는 유일하지 않을 수 있다.

## 8. KKT가 성립해도 최적해를 미분할 수 있다는 뜻은 아니다

파라미터에 따라 목적함수가 달라지는 ramp QP를 보자.

<math display="block" aria-label="A unique optimal solution with a kink"><mtable columnalign="left"><mtr><mtd><msup><mi>a</mi><mo>*</mo></msup><mo>(</mo><mi>η</mi><mo>)</mo><mo>=</mo><munder><mo>arg min</mo><mrow><mn>.4</mn><mo>≤</mo><mi>a</mi><mo>≤</mo><mn>.6</mn></mrow></munder><mo>(</mo><mfrac><mrow><mn>1</mn></mrow><mrow><mn>2</mn></mrow></mfrac><msup><mi>a</mi><mn>2</mn></msup><mo>−</mo><mi>η</mi><mi>a</mi><mo>)</mo></mtd></mtr><mtr><mtd><msup><mi>a</mi><mo>*</mo></msup><mo>(</mo><mi>η</mi><mo>)</mo><mo>=</mo><mo>min</mo><mo>{</mo><mn>.6</mn><mo>,</mo><mo>max</mo><mo>{</mo><mn>.4</mn><mo>,</mo><mi>η</mi><mo>}</mo><mo>}</mo></mtd></mtr></mtable></math>

모든 <math><mi>η</mi></math>에서 최적해가 유일하고 KKT 승수가 존재한다. 하지만 <math><mi>η</mi></math> = 0.6 주변에서 action의 미분은 왼쪽에서 1, 오른쪽에서 0이다. 경계점의 일반적인 미분은 존재하지 않는다. 이 점에서는 상한이 활성인데 <math><msub><msup><mi>λ</mi><mo>*</mo></msup><mtext>upper</mtext></msub></math> = 0이므로 strict complementarity가 실패한다.

Implicit differentiation을 위해 primal·dual 변수를 <math><msup><mi>y</mi><mo>*</mo></msup></math>로 모아 KKT의 등식 부분을 residual로 쓰면

<math display="block" aria-label="Implicit differentiation requires an invertible residual Jacobian"><mtable columnalign="left"><mtr><mtd><mi>F</mi><mo>(</mo><msup><mi>y</mi><mo>*</mo></msup><mo>(</mo><mi>η</mi><mo>)</mo><mo>,</mo><mi>η</mi><mo>)</mo><mo>=</mo><mn>0</mn></mtd></mtr><mtr><mtd><msub><mi>F</mi><mi>y</mi></msub><mfrac><mrow><mo>∂</mo><msup><mi>y</mi><mo>*</mo></msup></mrow><mrow><mo>∂</mo><mi>η</mi></mrow></mfrac><mo>=</mo><mo>−</mo><msub><mi>F</mi><mi>η</mi></msub></mtd></mtr></mtable></math>

역행렬 공식을 적용하려면 residual이 연속적으로 미분 가능하고 해당 해에서 <math><msub><mi>F</mi><mi>y</mi></msub></math>가 nonsingular여야 한다. 충분히 매끄러운 문제 데이터와 LICQ, 이차 충분조건(SOSC), strict complementarity는 매끄러운 국소 primal–dual 해를 보장하는 대표적인 충분조건이다. 모든 미분 가능한 primal 해에 각각 필수라는 주장은 아니다.

확인할 것은 세 가지이다. KKT 승수가 존재하는가, KKT가 원하는 최적성을 보장하는가, 선택한 해의 파라미터 의존성을 미분할 수 있는가.

## 참고문헌

- Boyd, S., and Vandenberghe, L. (2004). *Convex Optimization*, Chapter 5, 특히 §§5.2.3, 5.5.3. [저자 공식 교재 페이지](https://web.stanford.edu/~boyd/cvxbook/).
- Farina, G. (2025). *Lagrange multipliers and KKT conditions*, MIT 6.7220/15.084, Lecture 7. Affine normal cone, LICQ, Slater. [공식 강의 PDF](https://www.mit.edu/~gfarina/2025/67220s25_L07_kkt/L07.pdf).
- Sun, Y. (2024). *Notes on constraint qualifications*, STATS 606. Fritz John과 MFCQ. [공식 강의 노트](https://websites.umich.edu/~yuekai/stats606/posts/constraint-qualifications.html).
- Amos, B., and Kolter, J. Z. (2017). *OptNet: Differentiable Optimization as a Layer in Neural Networks*. ICML, PMLR 70, 136–145. [논문과 서지정보](https://proceedings.mlr.press/v70/amos17a.html).
