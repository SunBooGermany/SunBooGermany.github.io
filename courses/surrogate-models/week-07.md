---
layout: "course-note"
title: "Week 7: Designing Model Structure for Optimization"
title_ko: "7주차: 최적화 활용을 위한 모델 구조 설계"
description: "Check ICNN/PICNN convexity conditions and build a ReLU epigraph LP, with counterexamples to equivalence."
description_ko: "ICNN·PICNN의 convexity 조건을 확인하고, ReLU epigraph로 유효한 LP와 동치성이 깨지는 반례를 계산합니다."
material_label: "Week 7"
material_label_ko: "7주차"
updated: "2026-11-12"
permalink: "/courses/surrogate-models/week-07/"
pdf_en: "/assets/courses/surrogate-models/week-07-en.pdf"
pdf_ko: "/assets/courses/surrogate-models/week-07-ko.pdf"
course_id: "surrogate-models"
notebook: "/assets/courses/surrogate-models/week-07/week07_lab.ipynb"
lab_script: "/assets/courses/surrogate-models/week-07/week07_lab.py"
lab_bundle: "/assets/courses/surrogate-models/week-07/week07-lab.zip"
reading_note: "/courses/surrogate-models/week-07-reading/"
reading_pdf_en: "/assets/courses/surrogate-models/week-07-reading-en.pdf"
reading_pdf_ko: "/assets/courses/surrogate-models/week-07-reading-ko.pdf"
practice_note: "/courses/surrogate-models/week-07-practice/"
---

## Utility cost models and repeated operating decisions

A changing supply condition requires a new heating-load decision. When a neural network predicts the cost curve, its structure also affects the optimization used to select the load.

<figure><img src="/assets/courses/surrogate-models/week-07/motivation-en.png" alt="Heating load, cost curve, and fixed supply context" /></figure>

Goal: load selection with preserved convex cost structure.

<!-- lecture-page -->

## Model choice and optimization formulations

Weeks 5 and 6 represented a fitted general ReLU network exactly as an MILP. This week imposes convexity in selected inputs during model design.

We begin with a known convex cost. Reactor concentrations and yields are not assumed convex.

Structural restrictions reduce the function class, so evaluate prediction error together with the resulting decisions.

### Learning objectives and deliverables

1. Decisions, fixed context, and ICNN sign conditions
2. Objective-value equivalence and conditions for a ReLU epigraph LP
3. Counterexamples: inequality direction, negative weights, and variable context
4. Fitted ICNN decision validation: forward evaluation and reference function

<!-- lecture-page -->

## Decision variables and fixed context

Choose a normalized heating load u, while fixing measured supply composition or ambient conditions c. Freeze model parameters θ before optimization.

<math display="block"><mtable columnalign="left"><mtr><mtd><mrow><msub><mi mathvariant="normal">min</mi><mrow><mi>u</mi><mo>∈</mo><mi>U</mi></mrow></msub><msub><mi>f</mi><mrow><mi>θ</mi></mrow></msub><mo>(</mo><mi>u</mi><mo>;</mo><mi>c</mi><mo>)</mo></mrow></mtd></mtr><mtr><mtd><mrow><mi>U</mi><mo>=</mo><mo>{</mo><mi>u</mi><mo>:</mo><mi>G</mi><mi>u</mi><mo>≤</mo><mi>r</mi><mo>}</mo><mo>,</mo><mi>c</mi><mo>=</mo><msub><mi>c</mi><mrow><mi>o</mi><mi>b</mi><mi>s</mi></mrow></msub></mrow></mtd></mtr></mtable></math>

Convexity here concerns u. It does not establish convexity in c or θ.

c is the observed supply condition; u is the load selected now. A changed supply condition may change the cost curve, so fix the new c and solve again. Distinguish training parameters θ from the operating decision u.

<!-- lecture-page -->

## Convex functions and sublevel sets

A convex function lies below the line segment joining two function values.

<math display="block"><mtable columnalign="left"><mtr><mtd><mrow><mi>f</mi><mo>(</mo><mi>λ</mi><mi>u</mi><mo>+</mo><mo>(</mo><mn>1</mn><mo>−</mo><mi>λ</mi><mo>)</mo><mi>v</mi><mo>)</mo><mo>≤</mo><mi>λ</mi><mi>f</mi><mo>(</mo><mi>u</mi><mo>)</mo><mo>+</mo><mo>(</mo><mn>1</mn><mo>−</mo><mi>λ</mi><mo>)</mo><mi>f</mi><mo>(</mo><mi>v</mi><mo>)</mo></mrow></mtd></mtr><mtr><mtd><mrow><mn>0</mn><mo>≤</mo><mi>λ</mi><mo>≤</mo><mn>1</mn></mrow></mtd></mtr></mtable></math>

For convex f, the constraint f(u) ≤ b defines a convex set. The reverse inequality generally does not. This distinction determines valid LP uses.

[Boyd and Vandenberghe, Convex Optimization, §§3.1-3.2 and 4.1-4.3](https://web.stanford.edu/~boyd/cvxbook/bv_cvxbook.pdf)

If two inputs each satisfy cost cap b, the cost at their mixture is at most their weighted average and hence at most b. This proves convexity of the sublevel set. The same inequality argument does not establish a lower-cost constraint.

<!-- lecture-page -->

## ICNN input connections and sign conditions

<math display="block"><mtable columnalign="left"><mtr><mtd><mrow><msub><mi>h</mi><mrow><mn>0</mn></mrow></msub><mo>=</mo><mn>0</mn></mrow></mtd></mtr><mtr><mtd><mrow><msub><mi>h</mi><mrow><mi>k</mi></mrow></msub><mo>=</mo><mi mathvariant="normal">ReLU</mi><mo>(</mo><msub><mi>W</mi><mrow><mi>k</mi></mrow></msub><msub><mi>h</mi><mrow><mi>k</mi><mo>−</mo><mn>1</mn></mrow></msub><mo>+</mo><msub><mi>A</mi><mrow><mi>k</mi></mrow></msub><mi>u</mi><mo>+</mo><msub><mi>b</mi><mrow><mi>k</mi></mrow></msub><mo>)</mo></mrow></mtd></mtr><mtr><mtd><mrow><mi>f</mi><mo>(</mo><mi>u</mi><mo>)</mo><mo>=</mo><msup><mi>a</mi><mrow><mi>T</mi></mrow></msup><mi>u</mi><mo>+</mo><mi>d</mi><mo>+</mo><msup><mi>w</mi><mrow><mi>T</mi></mrow></msup><msub><mi>h</mi><mrow><mi>K</mi></mrow></msub></mrow></mtd></mtr></mtable></math>

Constrain every entry of W and w to be nonnegative. Direct input weights A and a, and biases, may have either sign.

ReLU is convex and nondecreasing. These conditions preserve convexity in the inputs through the layers and output.

[Amos, Xu and Kolter, Input Convex Neural Networks, ICML 2017, pp. 146-155](https://proceedings.mlr.press/v70/amos17b.html)

Nonnegative sums preserve the convexity inequality of previous-layer functions. A negative multiplier reverses that inequality. Direct affine input terms have no curvature even with negative slopes, so their weights need no such restriction.

<!-- lecture-page -->

## Layerwise convexity derivation

The first layer is a maximum of an affine function and zero, so it is convex. Assume every component of the previous layer is convex.

With W ≥ 0, their weighted sum is convex; adding an affine input connection preserves this property. Applying convex, nondecreasing ReLU preserves it again.

The output condition w ≥ 0 serves the same purpose. Negative slopes in direct input connections remain affine and do not break the argument.

The induction hypothesis is componentwise convexity of the previous layer. Multiplying its inequalities by nonnegative W entries and adding preserves their direction. Applying nondecreasing ReLU then preserves the ordering needed for the composition argument.

<!-- lecture-page -->

## Negative weights and input convexity

Negative weights on hidden activations remove the sufficient condition.

<math display="block"><mtable columnalign="left"><mtr><mtd><mrow><mi>f</mi><mo>(</mo><mi>u</mi><mo>)</mo><mo>=</mo><mo>−</mo><mi mathvariant="normal">ReLU</mi><mo>(</mo><mi>u</mi><mo>)</mo><mo>,</mo><mo>−</mo><mn>1</mn><mo>≤</mo><mi>u</mi><mo>≤</mo><mn>1</mn></mrow></mtd></mtr><mtr><mtd><mrow><mi>f</mi><mo>(</mo><mn>0</mn><mo>)</mo><mo>=</mo><mn>0</mn><mo>&gt;</mo><mo>(</mo><mi>f</mi><mo>(</mo><mo>−</mo><mn>1</mn><mo>)</mo><mo>+</mo><mi>f</mi><mo>(</mo><mn>1</mn><mo>)</mo><mo>)</mo><mo>/</mo><mn>2</mn><mo>=</mo><mo>−</mo><mn>.5</mn></mrow></mtd></mtr></mtable></math>

Direct input weights need not be nonnegative: ReLU(−u + 0.4) is still convex. Identify which connection each restricted weight belongs to.

<!-- lecture-page -->

## Sign constraints during training

After a gradient update, project W to max(W, 0), or parameterize W = softplus(V) using free parameters V. Apply the same rule to output weights w.

Here softplus parameterizes positive weights. Hidden activations remain ReLU during inference.

Inspect the actual fitted weights. Training a general deep ICNN in its parameters is nonlinear and nonconvex.

If an updated constrained weight is −0.03, clipping replaces it by zero; a weight of 0.2 stays unchanged. These restrictions make the function convex in its input, without making the general weight-training problem convex.

<!-- lecture-page -->

## ReLU graphs and epigraphs

<math display="block"><mtable columnalign="left"><mtr><mtd><mrow><mi>h</mi><mo>=</mo><mi mathvariant="normal">ReLU</mi><mo>(</mo><mi>s</mi><mo>)</mo><mo>=</mo><mi mathvariant="normal">max</mi><mo>(</mo><mn>0</mn><mo>,</mo><mi>s</mi><mo>)</mo></mrow></mtd></mtr><mtr><mtd><mrow><mi>h</mi><mo>≥</mo><mn>0</mn><mo>,</mo><mi>h</mi><mo>≥</mo><mi>s</mi></mrow></mtd></mtr></mtable></math>

The two inequalities describe the region above ReLU. They allow h = 10 at s = 0, so they do not represent the graph equality itself.

To use these lower bounds in an LP, it must be possible to reduce the auxiliary activations to the actual outputs, and the objective and remaining constraints must permit that reduction.

At fixed input, values above the true ReLU still satisfy both lower inequalities. Reducing h to its forward value is harmless only when the objective favors reduction and other constraints permit it. These conditions justify using the epigraph instead of the graph equality.

<!-- lecture-page -->

## An extended LP for a ReLU ICNN

Constraint scope: a finite ReLU network with frozen weights

<math display="block"><mtable columnalign="left"><mtr><mtd><mrow><msub><mi>h</mi><mrow><mi>k</mi></mrow></msub><mo>≥</mo><mn>0</mn></mrow></mtd></mtr><mtr><mtd><mrow><msub><mi>h</mi><mrow><mi>k</mi></mrow></msub><mo>≥</mo><msub><mi>W</mi><mrow><mi>k</mi></mrow></msub><msub><mi>h</mi><mrow><mi>k</mi><mo>−</mo><mn>1</mn></mrow></msub><mo>+</mo><msub><mi>A</mi><mrow><mi>k</mi></mrow></msub><mi>u</mi><mo>+</mo><msub><mi>b</mi><mrow><mi>k</mi></mrow></msub></mrow></mtd></mtr><mtr><mtd><mrow><mi>t</mi><mo>≥</mo><msup><mi>a</mi><mrow><mi>T</mi></mrow></msup><mi>u</mi><mo>+</mo><mi>d</mi><mo>+</mo><msup><mi>w</mi><mrow><mi>T</mi></mrow></msup><msub><mi>h</mi><mrow><mi>K</mi></mrow></msub></mrow></mtd></mtr></mtable></math>

Add Gu ≤ r and minimize t. With W, w ≥ 0 and linear remaining expressions, this is an LP without binary variables.

Replacing the activation by softplus can preserve convexity, but not an exact representation by these finitely many linear constraints.

Auxiliary t is an upper value for cost. Every feasible point has t≥f(u), and the actual forward values permit t=f(u). Minimizing t therefore attains the same optimal value as minimizing the original cost.

<!-- lecture-page -->

## Forward recovery and objective-value equivalence

At fixed u, a feasible first-layer h dominates the actual ReLU output. Induction using W ≥ 0 gives the same result at every layer, hence t ≥ f(u).

Conversely, the true forward activations with t = f(u) satisfy every constraint. These two inclusions establish the exact epigraph.

The optimum of min t agrees with the objective at the selected u. Auxiliary variables that do not affect the output may remain slack even at an optimum.

<!-- lecture-page -->

## Restoring two auxiliary layers to forward values

Consider h₁=ReLU(u−0.4), h₂=ReLU(2h₁−0.1), and f=0.2−u+3h₂. Hidden weight 2 and output weight 3 are positive. Fix u=0.6.

| State | h₁ | h₂ | Output expression |
| --- | --- | --- | --- |
| Actual forward | 0.2 | 0.3 | 0.5 |
| Loose epigraph point | 0.4 | 0.7 | 1.7 |
| Restore first layer only | 0.2 | 0.7 | 1.7 |
| Restore second layer | 0.2 | 0.3 | 0.5 |

Lowering h₁ lowers 2h₁−0.1, so the existing h₂ still satisfies its lower bound. Lowering h₂ then decreases the objective because its output coefficient is positive. This is the layer-by-layer restoration argument.

With output coefficient −3, raising h₂ would improve the objective and the argument would fail. An external requirement h₂≥0.7 would also prevent restoration to 0.3. Both weight signs and external constraints matter.

<!-- lecture-page -->

## Applicability by output use

<table><thead><tr><th style="font-size:clamp(15px,1.7cqw,22px)">Output use</th><th style="font-size:clamp(15px,1.7cqw,22px)">Assessment</th></tr></thead><tbody><tr><td style="font-size:clamp(15px,1.7cqw,22px)">min f(u)</td><td style="font-size:clamp(15px,1.7cqw,22px)">Use an epigraph objective</td></tr><tr><td style="font-size:clamp(15px,1.7cqw,22px)">f(u) ≤ b</td><td style="font-size:clamp(15px,1.7cqw,22px)">Adding t ≤ b gives the exact input feasible set</td></tr><tr><td style="font-size:clamp(15px,1.7cqw,22px)">f(u) ≥ b</td><td style="font-size:clamp(15px,1.7cqw,22px)">Adding only t ≥ b does not enforce a lower bound on the true output</td></tr><tr><td style="font-size:clamp(15px,1.7cqw,22px)">y = f(u)</td><td style="font-size:clamp(15px,1.7cqw,22px)">The output graph equality is generally nonconvex</td></tr><tr><td style="font-size:clamp(15px,1.7cqw,22px)">max f(u)</td><td style="font-size:clamp(15px,1.7cqw,22px)">The same LP argument does not cover convex maximization</td></tr></tbody></table>

Also inspect any other constraints that favor larger h or t.

An upper cap gives f(u)≤t≤b and therefore enforces the original cap. A lower bound t≥b can be met by inflating t even when f(u) is small. The same predictor needs different formulations depending on whether its output is minimized, capped, or lower-bounded.

<!-- lecture-page -->

## A two-hinge cost model for hand calculation

<math display="block"><mtable columnalign="left"><mtr><mtd><mrow><mi>f</mi><mo>(</mo><mi>u</mi><mo>)</mo><mo>=</mo><mn>.4</mn><mo>−</mo><mn>.6</mn><mi>u</mi><mo>+</mo><msub><mi>h</mi><mrow><mn>1</mn></mrow></msub><mo>+</mo><mn>.5</mn><msub><mi>h</mi><mrow><mn>2</mn></mrow></msub></mrow></mtd></mtr><mtr><mtd><mrow><msub><mi>h</mi><mrow><mn>1</mn></mrow></msub><mo>=</mo><mi mathvariant="normal">ReLU</mi><mo>(</mo><mi>u</mi><mo>−</mo><mn>.4</mn><mo>)</mo><mo>,</mo><msub><mi>h</mi><mrow><mn>2</mn></mrow></msub><mo>=</mo><mi mathvariant="normal">ReLU</mi><mo>(</mo><mi>u</mi><mo>−</mo><mn>.7</mn><mo>)</mo></mrow></mtd></mtr><mtr><mtd><mrow><mn>0</mn><mo>≤</mo><mi>u</mi><mo>≤</mo><mn>1</mn></mrow></mtd></mtr></mtable></math>

Dimensionless cost example for direct numerical checks. Successive slopes: −0.6 → 0.4 → 0.9.

Minimum: first slope change at u = 0.4; f(0.4) = 0.16.

Before u=0.4 both ReLUs are zero and the slope is −0.6. Activating the first adds slope 1, giving 0.4; activating the second adds 0.5, giving 0.9. The first knot where cost switches from decreasing to increasing is the minimum.

<!-- lecture-page -->

## The hand model LP and a cost cap

<math display="block"><mtable columnalign="left"><mtr><mtd><mrow><msub><mi mathvariant="normal">min</mi><mrow><mi>u</mi><mo>,</mo><mi>h</mi></mrow></msub><mn>.4</mn><mo>−</mo><mn>.6</mn><mi>u</mi><mo>+</mo><msub><mi>h</mi><mrow><mn>1</mn></mrow></msub><mo>+</mo><mn>.5</mn><msub><mi>h</mi><mrow><mn>2</mn></mrow></msub></mrow></mtd></mtr><mtr><mtd><mrow><msub><mi>h</mi><mrow><mn>1</mn></mrow></msub><mo>≥</mo><mn>0</mn><mo>,</mo><msub><mi>h</mi><mrow><mn>1</mn></mrow></msub><mo>≥</mo><mi>u</mi><mo>−</mo><mn>.4</mn></mrow></mtd></mtr><mtr><mtd><mrow><msub><mi>h</mi><mrow><mn>2</mn></mrow></msub><mo>≥</mo><mn>0</mn><mo>,</mo><msub><mi>h</mi><mrow><mn>2</mn></mrow></msub><mo>≥</mo><mi>u</mi><mo>−</mo><mn>.7</mn><mo>,</mo><mn>0</mn><mo>≤</mo><mi>u</mi><mo>≤</mo><mn>1</mn></mrow></mtd></mtr></mtable></math>

A cost cap of 0.25 leaves the feasible input interval [0.25, 0.625]. Bound the affine output expression above to obtain this interval in the LP.

Lab checks: minimum value 0.16 and forward agreement.

<!-- lecture-page -->

## Cost and feasibility between two knots

Keep only active ReLUs in each interval to simplify the cost.

| u interval | Active terms | Cost | Condition for f(u)≤0.25 |
| --- | --- | --- | --- |
| 0–0.4 | None | 0.4−0.6u | u≥0.25 |
| 0.4–0.7 | u−0.4 | 0.4u | u≤0.625 |
| 0.7–1 | Both | 0.9u−0.35 | u≤2/3, outside this interval |

The feasible interval is [0.25,0.625]. At minimum u=0.4, both ReLUs are zero and f=0.4−0.6×0.4=0.16.

For example, u=0.6 gives h₁=0.2,h₂=0 and f=0.4−0.36+0.2=0.24. This matches 0.4u=0.24 in the middle interval, checking the piecewise expression against the original network.

<!-- lecture-page -->

## LP matrix columns and inequalities

Fix variable order [u,h₁,h₂]. Each row of linprog's A_ub is dotted with the variable vector and bounded above by the matching b_ub entry.

| Code value | Expression | Role |
| --- | --- | --- |
| Objective [−0.6,1,0.5] | −0.6u+h₁+0.5h₂ | Cost without constant 0.4 |
| Row [1,−1,0], rhs 0.4 | u−h₁≤0.4 | h₁≥u−0.4 |
| Row [1,0,−1], rhs 0.7 | u−h₂≤0.7 | h₂≥u−0.7 |
| h bounds (0,None) | h₁,h₂≥0 | Other ReLU lower bounds |

At solution [0.4,0,0], row values [0.4,0.4] satisfy their upper bounds. Add constant 0.4 to solver objective −0.24 to report 0.16. The original forward cost must also be 0.16.

Positive h coefficients make this objective minimize h. Changing their signs requires rechecking the recovery argument.

<!-- lecture-page -->

## A counterexample for an output lower bound

On 0 ≤ u ≤ 1, let f(u) = ReLU(u) and minimize u subject to f(u) ≥ 0.8. The true optimum is u = 0.8.

<math display="block"><mtable columnalign="left"><mtr><mtd><mrow><mi>h</mi><mo>≥</mo><mi>u</mi><mo>,</mo><mi>h</mi><mo>≥</mo><mn>0</mn><mo>,</mo><mi>h</mi><mo>≥</mo><mn>.8</mn></mrow></mtd></mtr></mtable></math>

The relaxation permits u = 0, h = 0.8. An inflated auxiliary variable lowers the cost. A small MIP gap or an LP optimal status cannot detect this modeling error.

At u=0,h=0.8, all three linear inequalities hold but f(0)=0. Solving a model with the wrong output lower-bound representation exactly still returns the wrong input. This is why forward validation follows status checking.

<!-- lecture-page -->

## Counterexamples for output rewards and graph equalities

Minimizing −h for the same ReLU makes the epigraph LP unbounded when h has no upper bound. The actual f(u) lies in [0, 1], and min −f(u) = −1.

For f(u) = &#124;u&#124;, graph points (−1, 1) and (1, 1) have midpoint (0, 1), which is not on the graph.

Transferring cost-epigraph equivalence directly to concentration equalities or output rewards changes the problem.

<!-- lecture-page -->

## PICNNs and fixed context

A PICNN imposes convexity on only part of its input. The path processing supply context c may be nonlinear, while the decision path in u must satisfy the required sign conditions after c is fixed.

The next page uses a sufficient form in which context determines layer coefficients. The paper’s gated construction can also be interpreted this way at fixed context.

[Amos, Xu and Kolter, Input Convex Neural Networks, ICML 2017, pp. 146-155](https://proceedings.mlr.press/v70/amos17b.html)

<!-- lecture-page -->

## Conditional coefficients and LP construction

<math display="block"><mtable columnalign="left"><mtr><mtd><mrow><msub><mi>h</mi><mrow><mi>k</mi></mrow></msub><mo>=</mo><mi mathvariant="normal">ReLU</mi><mo>(</mo><msub><mi>W</mi><mrow><mi>k</mi></mrow></msub><mo>(</mo><mi>c</mi><mo>)</mo><msub><mi>h</mi><mrow><mi>k</mi><mo>−</mo><mn>1</mn></mrow></msub><mo>+</mo><msub><mi>A</mi><mrow><mi>k</mi></mrow></msub><mo>(</mo><mi>c</mi><mo>)</mo><mi>u</mi><mo>+</mo><msub><mi>b</mi><mrow><mi>k</mi></mrow></msub><mo>(</mo><mi>c</mi><mo>)</mo><mo>)</mo></mrow></mtd></mtr><mtr><mtd><mrow><msub><mi>W</mi><mrow><mi>k</mi></mrow></msub><mo>(</mo><mi>c</mi><mo>)</mo><mo>≥</mo><mn>0</mn><mo>,</mo><mi>w</mi><mo>(</mo><mi>c</mi><mo>)</mo><mo>≥</mo><mn>0</mn></mrow></mtd></mtr></mtable></math>

Evaluate the context path once at observed c, then freeze its coefficients. With linear remaining decision expressions and constraints, construct the ReLU epigraph LP.

Optimizing c as well can introduce nonlinear products W(c)h or A(c)u. Fixed-context results do not imply joint convexity or an LP.

At observed c, W(c), A(c), and b(c) are numbers. Freezing them makes each expression affine in u and h. Leaving c variable turns a numerical coefficient times a variable into a function of a variable times another variable, which is no longer the same LP.

<!-- lecture-page -->

## Conditional versus joint convexity

<math display="block"><mtable columnalign="left"><mtr><mtd><mrow><mi>f</mi><mo>(</mo><mi>u</mi><mo>;</mo><mi>c</mi><mo>)</mo><mo>=</mo><mo>&#124;</mo><mi>u</mi><mo>−</mo><mi>c</mi><mo>&#124;</mo><mo>−</mo><mn>.1</mn><msup><mi>c</mi><mrow><mn>2</mn></mrow></msup></mrow></mtd></mtr><mtr><mtd><mrow><mn>0</mn><mo>≤</mo><mi>u</mi><mo>≤</mo><mn>1</mn><mo>,</mo><mn>0</mn><mo>≤</mo><mi>c</mi><mo>≤</mo><mn>1</mn></mrow></mtd></mtr></mtable></math>

At fixed c, the optimum is u = c. The lab solves separate LPs for c = 0.2, 0.5, and 0.8.

Along u = c, f = −0.1c². The endpoint average is −0.05 but the midpoint value is −0.025, violating joint convexity.

For fixed c=0.2, represent <math xmlns="http://www.w3.org/1998/Math/MathML"><mrow><mo stretchy="false">&#x7C;</mo><mi>u</mi><mo>−</mo><mn>0.2</mn><mo stretchy="false">&#x7C;</mo></mrow></math> with t≥u−0.2 and t≥0.2−u, and minimize t−0.004. The minimum is −0.004 at u=0.2,t=0. If c becomes a variable, −0.1c² is no longer a constant, so this LP no longer applies unchanged.

<!-- lecture-page -->

## Fitting a known convex reference function

<math display="block"><mtable columnalign="left"><mtr><mtd><mrow><mi>q</mi><mo>(</mo><mi>u</mi><mo>)</mo><mo>=</mo><mo>(</mo><mi>u</mi><mo>−</mo><mn>.6</mn><msup><mo>)</mo><mrow><mn>2</mn></mrow></msup><mo>+</mo><mn>.1</mn><mi>u</mi><mo>+</mo><mn>.2</mn></mrow></mtd></mtr><mtr><mtd><mrow><mi>f</mi><mo>(</mo><mi>u</mi><mo>)</mo><mo>=</mo><mi>b</mi><mo>+</mo><mi>a</mi><mi>u</mi><mo>+</mo><msup><msub><mo>∑</mo><mrow><mi>j</mi><mo>=</mo><mn>1</mn></mrow></msub><mrow><mn>9</mn></mrow></msup><msub><mi>w</mi><mrow><mi>j</mi></mrow></msub><mi mathvariant="normal">ReLU</mi><mo>(</mo><mi>u</mi><mo>−</mo><msub><mi>κ</mi><mrow><mi>j</mi></mrow></msub><mo>)</mo></mrow></mtd></mtr><mtr><mtd><mrow><msub><mi>κ</mi><mrow><mi>j</mi></mrow></msub><mo>=</mo><mn>.1</mn><mi>j</mi><mo>,</mo><msub><mi>w</mi><mrow><mi>j</mi></mrow></msub><mo>≥</mo><mn>0</mn></mrow></mtd></mtr></mtable></math>

Fit coefficients at 41 evenly spaced inputs and evaluate at 200 separate midpoint inputs. With fixed knots, this lab uses bounded linear least squares.

This shallow ICNN with fixed knots is a special case with convex training. The conclusion does not extend to general deep-ICNN training.

Fixed knots κ allow every ReLU feature to be computed before fitting. Only b,a,w remain unknown, giving bounded linear least squares. w≥0 prevents downward slope jumps at knots and preserves convexity of the fitted curve.

At u=0.25, the feature row is [1,0.25,0.15,0.05,0,0,0,0,0,0,0]. Only knots 0.1 and 0.2 have been crossed. Fit least squares with b and a unrestricted and lower bounds of zero on the remaining nine weights.

<!-- lecture-page -->

## Fitted curve and selected load

<figure><img src="/assets/courses/surrogate-models/week-07/fit-en.png" alt="Convex reference, fitted ICNN, and selected input" /></figure>

Independent-evaluation RMSE: 0.000760. LP choice: u = 0.50. Reference minimum: u = 0.55.

The reference cost difference is 0.0025. Close prediction curves can still have different minimizers.

A flat reference curve near its minimum allows a noticeable input shift with a small cost change. Input difference 0.05 and cost difference 0.0025 measure different things. Visually close prediction curves do not establish identical minimizing inputs.

<!-- lecture-page -->

## Prediction error and loss from the selected input

Complete the square in q(u)=(u−0.6)²+0.1u+0.2 to obtain q(u)=(u−0.55)²+0.2575. Squared distance from the minimizer equals the cost increase.

| Input | Reference calculation | Cost |
| --- | --- | --- |
| Reference minimum u=0.55 | 0²+0.2575 | 0.2575 |
| Model choice u=0.50 | (−0.05)²+0.2575 | 0.2600 |
| Difference | 0.2600−0.2575 | 0.0025 |

The difference 0.001563 between predicted cost 0.258437 and reference cost 0.260000 is prediction error at the selected point. Difference 0.0025 from the reference minimum is cost lost because of the selection.

These comparisons use different baselines. State the quantities subtracted in both accuracy reports and decision evaluations.

<!-- lecture-page -->

## Checks on an LP result

1. Save the input domain, context, scaling, and model weights.
2. Check W and w signs, objective direction, and every use of outputs.
3. Evaluate the original network at the chosen u and compare with the LP objective.
4. Separately evaluate the reference objective and constraints.

Fitted-model LP objective: 0.258437. Reference cost: 0.260000. Difference: surrogate error.

<!-- lecture-page -->

## Choosing a model structure

<table><thead><tr><th style="font-size:clamp(15px,1.7cqw,22px)">Target and conditions</th><th style="font-size:clamp(15px,1.7cqw,22px)">Approach to examine</th></tr></thead><tbody><tr><td style="font-size:clamp(15px,1.7cqw,22px)">Known convex cost minimization</td><td style="font-size:clamp(15px,1.7cqw,22px)">ICNN or fixed-context PICNN</td></tr><tr><td style="font-size:clamp(15px,1.7cqw,22px)">ReLU, linear output, linear outer constraints</td><td style="font-size:clamp(15px,1.7cqw,22px)">Epigraph LP after checking its conditions</td></tr><tr><td style="font-size:clamp(15px,1.7cqw,22px)">Concentration equalities or nonconvex response</td><td style="font-size:clamp(15px,1.7cqw,22px)">General surrogate with an appropriate NLP/MILP</td></tr><tr><td style="font-size:clamp(15px,1.7cqw,22px)">Weak evidence for convexity</td><td style="font-size:clamp(15px,1.7cqw,22px)">Compare structural prediction bias and decision errors</td></tr></tbody></table>

<!-- lecture-page -->

## Running the lab and checking outputs

```bash
python -m pip install -r requirements.txt
python week07_lab.py --output-dir my-results
```

Extract the code bundle before running. It writes results.json, fitted coefficients, training.csv, and heldout.csv.

Automatic checks cover the hand optimum 0.16, fitted sign conditions, LP/forward agreement, the output-lower-bound counterexample, and the unbounded example. The notebook runs the same functions in stages.

<!-- lecture-page -->

## Assignment: equivalence conditions and decision error

1. Add a cost cap of 0.25 to the two-hinge model and calculate both endpoints of its feasible interval.
2. Run the output-lower-bound counterexample and record the falsely allowed u and its true output.
3. Change fitted knot spacing from 0.1 to 0.05; compare prediction error and reference decision loss.
4. Explain why c is fixed and which output uses your formulation permits.

Companion: derivations and short answer checks.

<!-- lecture-page -->

## Companion and primary sources

[Week 7 companion](/courses/surrogate-models/week-07-reading/)

[Amos, Xu and Kolter, Input Convex Neural Networks, ICML 2017, pp. 146-155](https://proceedings.mlr.press/v70/amos17b.html)

[Boyd and Vandenberghe, Convex Optimization, §§3.1-3.2 and 4.1-4.3](https://web.stanford.edu/~boyd/cvxbook/bv_cvxbook.pdf)

[SciPy bounded least squares](https://docs.scipy.org/doc/scipy/reference/generated/scipy.optimize.lsq_linear.html) · [SciPy HiGHS LP interface](https://docs.scipy.org/doc/scipy/reference/generated/scipy.optimize.linprog.html)

<!-- ko -->

## 유틸리티 비용 모델과 반복 운전 선택

공급 조건이 바뀔 때마다 가열 부하를 다시 정해야 합니다. 비용 곡선을 신경망으로 학습하면 운전 조건을 찾는 계산도 모델 구조에 따라 달라집니다.

<figure><img src="/assets/courses/surrogate-models/week-07/motivation-ko.png" alt="가열 부하와 비용 곡선, 고정 공급 조건" /></figure>

비용의 convex 구조를 유지하면서 부하를 선택하는 방법을 다뤄봅니다.

<!-- lecture-page -->

## 모델 선택과 정식화의 연결

5·6주차에서는 학습된 일반 ReLU 네트워크를 MILP로 정확히 표현했습니다. 이번 주에는 학습 단계에서 입력에 대한 convexity를 부여합니다.

알려진 convex 비용을 먼저 다룹니다. 반응기 농도나 수율이 convex라는 가정은 하지 않습니다.

구조 제약을 추가하면 표현할 수 있는 함수가 줄어들므로, 예측 오차와 의사결정 결과를 함께 확인합니다.

### 학습 목표와 제출 항목

1. 결정변수와 고정 context를 구분하고 ICNN의 부호 조건을 확인합니다.
2. ReLU epigraph LP의 목적값 동치성과 적용 조건을 설명합니다.
3. 부등식 방향·음의 가중치·가변 context에 대한 반례를 계산
4. 학습한 작은 ICNN의 LP 해를 forward 계산과 기준 함수로 검증

<!-- lecture-page -->

## 결정변수와 고정 context

정규화한 가열 부하 u를 선택하고, 공급 조성·외기 조건 c는 측정한 값으로 고정합니다. 모델 매개변수 θ도 최적화 전에 고정합니다.

<math display="block"><mtable columnalign="left"><mtr><mtd><mrow><msub><mi mathvariant="normal">min</mi><mrow><mi>u</mi><mo>∈</mo><mi>U</mi></mrow></msub><msub><mi>f</mi><mrow><mi>θ</mi></mrow></msub><mo>(</mo><mi>u</mi><mo>;</mo><mi>c</mi><mo>)</mo></mrow></mtd></mtr><mtr><mtd><mrow><mi>U</mi><mo>=</mo><mo>{</mo><mi>u</mi><mo>:</mo><mi>G</mi><mi>u</mi><mo>≤</mo><mi>r</mi><mo>}</mo><mo>,</mo><mi>c</mi><mo>=</mo><msub><mi>c</mi><mrow><mi>o</mi><mi>b</mi><mi>s</mi></mrow></msub></mrow></mtd></mtr></mtable></math>

여기서 convexity는 u에 관한 성질입니다. c나 θ에 대해서도 convex라고 결론 내릴 수는 없습니다.

c는 현재 관측한 공급 조건이고 u는 지금 선택할 부하입니다. 공급 조건이 바뀌면 같은 u의 비용 곡선도 바뀔 수 있어 c를 다시 고정하고 풉니다. 학습에서 바꾸는 θ와 운전에서 선택하는 u를 구분합니다.

<!-- lecture-page -->

## Convex 함수와 sublevel set

두 입력 사이의 함수값이 두 함수값을 잇는 선분보다 높지 않으면 convex입니다.

<math display="block"><mtable columnalign="left"><mtr><mtd><mrow><mi>f</mi><mo>(</mo><mi>λ</mi><mi>u</mi><mo>+</mo><mo>(</mo><mn>1</mn><mo>−</mo><mi>λ</mi><mo>)</mo><mi>v</mi><mo>)</mo><mo>≤</mo><mi>λ</mi><mi>f</mi><mo>(</mo><mi>u</mi><mo>)</mo><mo>+</mo><mo>(</mo><mn>1</mn><mo>−</mo><mi>λ</mi><mo>)</mo><mi>f</mi><mo>(</mo><mi>v</mi><mo>)</mo></mrow></mtd></mtr><mtr><mtd><mrow><mn>0</mn><mo>≤</mo><mi>λ</mi><mo>≤</mo><mn>1</mn></mrow></mtd></mtr></mtable></math>

Convex f에 대한 f(u) ≤ b는 convex 영역을 만듭니다. f(u) ≥ b는 일반적으로 그렇지 않습니다. 이 방향 차이가 LP 사용 조건에 반영됩니다.

[Boyd and Vandenberghe, Convex Optimization, §§3.1-3.2 and 4.1-4.3](https://web.stanford.edu/~boyd/cvxbook/bv_cvxbook.pdf)

두 입력이 각각 비용 상한 b를 만족하면 그 사이 혼합 입력의 비용은 두 비용의 가중평균 이하이므로 b 이하입니다. 이 계산이 sublevel set의 convexity를 설명합니다. 비용 하한에는 같은 부등식 논리를 적용할 수 없습니다.

<!-- lecture-page -->

## ICNN의 입력 연결과 부호 조건

<math display="block"><mtable columnalign="left"><mtr><mtd><mrow><msub><mi>h</mi><mrow><mn>0</mn></mrow></msub><mo>=</mo><mn>0</mn></mrow></mtd></mtr><mtr><mtd><mrow><msub><mi>h</mi><mrow><mi>k</mi></mrow></msub><mo>=</mo><mi mathvariant="normal">ReLU</mi><mo>(</mo><msub><mi>W</mi><mrow><mi>k</mi></mrow></msub><msub><mi>h</mi><mrow><mi>k</mi><mo>−</mo><mn>1</mn></mrow></msub><mo>+</mo><msub><mi>A</mi><mrow><mi>k</mi></mrow></msub><mi>u</mi><mo>+</mo><msub><mi>b</mi><mrow><mi>k</mi></mrow></msub><mo>)</mo></mrow></mtd></mtr><mtr><mtd><mrow><mi>f</mi><mo>(</mo><mi>u</mi><mo>)</mo><mo>=</mo><msup><mi>a</mi><mrow><mi>T</mi></mrow></msup><mi>u</mi><mo>+</mo><mi>d</mi><mo>+</mo><msup><mi>w</mi><mrow><mi>T</mi></mrow></msup><msub><mi>h</mi><mrow><mi>K</mi></mrow></msub></mrow></mtd></mtr></mtable></math>

W와 w의 모든 원소를 0 이상으로 제한합니다. 입력에서 직접 들어오는 A와 a, bias의 부호는 제한하지 않습니다.

ReLU는 convex이고 비감소합니다. 이 조건으로 각 층과 출력의 입력 convexity를 유지합니다.

[Amos, Xu and Kolter, Input Convex Neural Networks, ICML 2017, pp. 146-155](https://proceedings.mlr.press/v70/amos17b.html)

이전 층의 convex 곡선을 양수 가중치로 더하면 아래로 굽는 부분이 새로 생기지 않습니다. 반면 그 곡선에 음수 가중치를 곱하면 위아래가 뒤집힙니다. 직접 입력의 affine 항은 기울기가 음수여도 굽음이 없어 별도 취급합니다.

<!-- lecture-page -->

## 층별 convexity 유도

첫 층은 affine 함수와 0의 최댓값이므로 convex입니다. 이전 층의 성분들이 convex라고 가정합니다.

W ≥ 0이면 그 성분의 가중합도 convex이고, affine 입력 연결을 더해도 유지됩니다. 여기에 convex·비감소 ReLU를 적용합니다.

출력의 w ≥ 0도 같은 역할을 합니다. 입력 연결의 음의 기울기는 affine 항이므로 이 논증을 깨지 않습니다.

귀납 단계에서 필요한 것은 이전 층의 각 성분이 convex라는 조건입니다. W의 각 원소가 비음수라면 성분별 convexity 부등식에 곱해 더해도 방향이 유지됩니다. 그 다음 비감소 함수 ReLU를 적용해도 대소관계를 뒤집지 않습니다.

<!-- lecture-page -->

## 음의 가중치와 입력 convexity

은닉 출력에 음의 가중치를 허용하면 위의 충분조건이 사라집니다.

<math display="block"><mtable columnalign="left"><mtr><mtd><mrow><mi>f</mi><mo>(</mo><mi>u</mi><mo>)</mo><mo>=</mo><mo>−</mo><mi mathvariant="normal">ReLU</mi><mo>(</mo><mi>u</mi><mo>)</mo><mo>,</mo><mo>−</mo><mn>1</mn><mo>≤</mo><mi>u</mi><mo>≤</mo><mn>1</mn></mrow></mtd></mtr><mtr><mtd><mrow><mi>f</mi><mo>(</mo><mn>0</mn><mo>)</mo><mo>=</mo><mn>0</mn><mo>&gt;</mo><mo>(</mo><mi>f</mi><mo>(</mo><mo>−</mo><mn>1</mn><mo>)</mo><mo>+</mo><mi>f</mi><mo>(</mo><mn>1</mn><mo>)</mo><mo>)</mo><mo>/</mo><mn>2</mn><mo>=</mo><mo>−</mo><mn>.5</mn></mrow></mtd></mtr></mtable></math>

음의 입력 연결을 금지할 필요는 없습니다. 예를 들어 ReLU(−u + 0.4)는 여전히 convex입니다. 제한하는 가중치가 어느 연결에 있는지 확인합니다.

<!-- lecture-page -->

## 학습 중 부호 제약

Gradient 갱신 뒤 W를 max(W, 0)으로 투영하거나, 자유 매개변수 V에서 W = softplus(V)를 계산할 수 있습니다. 출력 가중치 w에도 적용합니다.

여기서 softplus는 가중치를 양수로 만드는 매개화입니다. 추론할 때 은닉 활성화는 ReLU로 유지합니다.

학습 후 확인: 가중치의 부호. 일반적인 깊은 ICNN의 매개변수 학습: 비선형·비볼록 문제

가중치 하나가 갱신 뒤 −0.03이면 clipping은 0으로 바꿉니다. 다른 가중치가 0.2이면 그대로 둡니다. 이는 함수가 입력에 대해 convex하도록 제약하는 것이며, 가중치 전체를 찾는 학습 문제의 convexity를 보장하지는 않습니다.

<!-- lecture-page -->

## ReLU 그래프와 epigraph

<math display="block"><mtable columnalign="left"><mtr><mtd><mrow><mi>h</mi><mo>=</mo><mi mathvariant="normal">ReLU</mi><mo>(</mo><mi>s</mi><mo>)</mo><mo>=</mo><mi mathvariant="normal">max</mi><mo>(</mo><mn>0</mn><mo>,</mo><mi>s</mi><mo>)</mo></mrow></mtd></mtr><mtr><mtd><mrow><mi>h</mi><mo>≥</mo><mn>0</mn><mo>,</mo><mi>h</mi><mo>≥</mo><mi>s</mi></mrow></mtd></mtr></mtable></math>

두 부등식은 ReLU 위쪽 영역을 표현합니다. s = 0에서 h = 10도 허용하므로 그래프 등식 자체와 같지는 않습니다.

이 하한 제약을 LP에 사용하려면 보조변수를 실제 출력으로 줄일 수 있어야 하며, 목적함수와 나머지 제약도 그 방향을 허용해야 합니다.

고정 입력에서 h를 실제 ReLU값보다 크게 두어도 두 하한은 만족합니다. 최소화 목적이 h를 줄이는 방향이고 다른 제약도 그 감소를 허용할 때만 실제 순전파 값으로 내려도 손해가 없습니다. 이 조건이 등식 그래프 대신 epigraph를 사용하는 근거입니다.

<!-- lecture-page -->

## ReLU ICNN의 확장 LP

제약 적용 범위: 유한한 ReLU 네트워크, 고정된 가중치

<math display="block"><mtable columnalign="left"><mtr><mtd><mrow><msub><mi>h</mi><mrow><mi>k</mi></mrow></msub><mo>≥</mo><mn>0</mn></mrow></mtd></mtr><mtr><mtd><mrow><msub><mi>h</mi><mrow><mi>k</mi></mrow></msub><mo>≥</mo><msub><mi>W</mi><mrow><mi>k</mi></mrow></msub><msub><mi>h</mi><mrow><mi>k</mi><mo>−</mo><mn>1</mn></mrow></msub><mo>+</mo><msub><mi>A</mi><mrow><mi>k</mi></mrow></msub><mi>u</mi><mo>+</mo><msub><mi>b</mi><mrow><mi>k</mi></mrow></msub></mrow></mtd></mtr><mtr><mtd><mrow><mi>t</mi><mo>≥</mo><msup><mi>a</mi><mrow><mi>T</mi></mrow></msup><mi>u</mi><mo>+</mo><mi>d</mi><mo>+</mo><msup><mi>w</mi><mrow><mi>T</mi></mrow></msup><msub><mi>h</mi><mrow><mi>K</mi></mrow></msub></mrow></mtd></mtr></mtable></math>

입력 제약 Gu ≤ r를 추가하고 t를 최소화합니다. W, w ≥ 0이고 나머지 식도 선형이면 이진변수 없이 LP가 됩니다.

활성화를 softplus로 바꾸면 convexity는 유지할 수 있어도 이 유한한 선형 제약식으로 정확히 표현되지는 않습니다.

t는 비용의 상한을 나타내는 보조 변수입니다. 모든 허용된 점에서 t≥f(u)이고 실제 순전파 값을 넣으면 t=f(u)가 가능하므로, t 최소화는 원래 비용 최소화와 같은 최적값을 얻습니다.

<!-- lecture-page -->

## Forward 복원과 목적값 동치성

u를 고정하면 첫 층의 허용 h는 실제 ReLU 출력 이상입니다. W ≥ 0을 사용해 층별로 반복하면 모든 h가 실제 출력 이상이 됩니다. 따라서 t ≥ f(u)입니다.

반대로 실제 forward 값을 h에 넣고 t = f(u)로 두면 모든 제약을 만족합니다. 이 두 포함관계가 epigraph의 정확성을 보입니다.

min t의 최적값과 선택한 u의 목적값이 일치합니다. 출력에 영향을 주지 않는 보조변수는 최적해에서도 slack을 가질 수 있습니다.

<!-- lecture-page -->

## 두 층의 보조변수를 forward로 복원하기

h₁=ReLU(u−0.4), h₂=ReLU(2h₁−0.1), f=0.2−u+3h₂인 ICNN을 봅니다. 은닉 연결 2와 출력 연결 3이 양수입니다. 입력 u=0.6을 고정합니다.

| 상태 | h₁ | h₂ | 출력식의 값 |
| --- | --- | --- | --- |
| 실제 forward | 0.2 | 0.3 | 0.5 |
| 느슨한 epigraph 가능점 | 0.4 | 0.7 | 1.7 |
| 첫 층만 실제값으로 내림 | 0.2 | 0.7 | 1.7 |
| 둘째 층도 실제값으로 내림 | 0.2 | 0.3 | 0.5 |

h₁을 낮추면 2h₁−0.1도 낮아져 기존 h₂의 하한 제약을 깨뜨리지 않습니다. 이어 h₂를 낮추면 양의 출력 계수 때문에 목적값도 내려갑니다. 이 순서가 층별 복원 논증입니다.

출력 계수가 −3이면 h₂를 높일수록 목적값이 낮아져 이 논리가 성립하지 않습니다. 외부에서 h₂≥0.7을 요구해도 실제값 0.3으로 복원할 수 없으므로, 부호와 외부 제약을 함께 확인합니다.

<!-- lecture-page -->

## 출력 사용 방식에 따른 적용 범위

<table><thead><tr><th style="font-size:clamp(15px,1.7cqw,22px)">사용 방식</th><th style="font-size:clamp(15px,1.7cqw,22px)">판단</th></tr></thead><tbody><tr><td style="font-size:clamp(15px,1.7cqw,22px)">min f(u)</td><td style="font-size:clamp(15px,1.7cqw,22px)">epigraph 목적함수로 표현</td></tr><tr><td style="font-size:clamp(15px,1.7cqw,22px)">f(u) ≤ b</td><td style="font-size:clamp(15px,1.7cqw,22px)">t ≤ b를 추가하면 정확한 입력 feasible set</td></tr><tr><td style="font-size:clamp(15px,1.7cqw,22px)">f(u) ≥ b</td><td style="font-size:clamp(15px,1.7cqw,22px)">t ≥ b만으로는 실제 출력 하한을 강제하지 못함</td></tr><tr><td style="font-size:clamp(15px,1.7cqw,22px)">y = f(u)</td><td style="font-size:clamp(15px,1.7cqw,22px)">출력 그래프 등식은 일반적으로 비convex</td></tr><tr><td style="font-size:clamp(15px,1.7cqw,22px)">max f(u)</td><td style="font-size:clamp(15px,1.7cqw,22px)">convex 함수 최대화에 같은 LP 논증을 적용할 수 없음</td></tr></tbody></table>

다른 제약이 h나 t를 큰 쪽으로 밀어 올리는 경우도 다시 확인합니다.

비용 상한은 f(u)≤t≤b를 만들기 때문에 원래 상한도 만족합니다. 비용 하한 t≥b는 f(u)가 작아도 t만 키워 만족할 수 있습니다. 동일한 모델에서도 출력이 목적식인지 상한인지 하한인지에 따라 정식화가 달라집니다.

<!-- lecture-page -->

## 손 계산용 두 hinge 비용 모델

<math display="block"><mtable columnalign="left"><mtr><mtd><mrow><mi>f</mi><mo>(</mo><mi>u</mi><mo>)</mo><mo>=</mo><mn>.4</mn><mo>−</mo><mn>.6</mn><mi>u</mi><mo>+</mo><msub><mi>h</mi><mrow><mn>1</mn></mrow></msub><mo>+</mo><mn>.5</mn><msub><mi>h</mi><mrow><mn>2</mn></mrow></msub></mrow></mtd></mtr><mtr><mtd><mrow><msub><mi>h</mi><mrow><mn>1</mn></mrow></msub><mo>=</mo><mi mathvariant="normal">ReLU</mi><mo>(</mo><mi>u</mi><mo>−</mo><mn>.4</mn><mo>)</mo><mo>,</mo><msub><mi>h</mi><mrow><mn>2</mn></mrow></msub><mo>=</mo><mi mathvariant="normal">ReLU</mi><mo>(</mo><mi>u</mi><mo>−</mo><mn>.7</mn><mo>)</mo></mrow></mtd></mtr><mtr><mtd><mrow><mn>0</mn><mo>≤</mo><mi>u</mi><mo>≤</mo><mn>1</mn></mrow></mtd></mtr></mtable></math>

직접 수치 검증을 위한 무차원 비용 예제. 구간별 기울기: −0.6 → 0.4 → 0.9

최소점: 첫 번째 기울기 전환점 u = 0.4. 최솟값: f(0.4) = 0.16

u=0.4 전에는 두 ReLU가 모두 0이라 기울기는 −0.6입니다. 첫 ReLU가 켜지면 기울기 1이 더해져 0.4가 되고, 두 번째가 켜지면 0.5가 더해져 0.9가 됩니다. 부하를 늘릴 때 비용이 내려가다가 올라가는 첫 절점이 최소점입니다.

<!-- lecture-page -->

## 손 계산 모델의 LP와 비용 상한

<math display="block"><mtable columnalign="left"><mtr><mtd><mrow><msub><mi mathvariant="normal">min</mi><mrow><mi>u</mi><mo>,</mo><mi>h</mi></mrow></msub><mn>.4</mn><mo>−</mo><mn>.6</mn><mi>u</mi><mo>+</mo><msub><mi>h</mi><mrow><mn>1</mn></mrow></msub><mo>+</mo><mn>.5</mn><msub><mi>h</mi><mrow><mn>2</mn></mrow></msub></mrow></mtd></mtr><mtr><mtd><mrow><msub><mi>h</mi><mrow><mn>1</mn></mrow></msub><mo>≥</mo><mn>0</mn><mo>,</mo><msub><mi>h</mi><mrow><mn>1</mn></mrow></msub><mo>≥</mo><mi>u</mi><mo>−</mo><mn>.4</mn></mrow></mtd></mtr><mtr><mtd><mrow><msub><mi>h</mi><mrow><mn>2</mn></mrow></msub><mo>≥</mo><mn>0</mn><mo>,</mo><msub><mi>h</mi><mrow><mn>2</mn></mrow></msub><mo>≥</mo><mi>u</mi><mo>−</mo><mn>.7</mn><mo>,</mo><mn>0</mn><mo>≤</mo><mi>u</mi><mo>≤</mo><mn>1</mn></mrow></mtd></mtr></mtable></math>

비용 상한 0.25를 추가하면 feasible 입력은 [0.25, 0.625]입니다. 같은 LP의 출력 affine 식에 상한을 걸어 이 구간을 얻습니다.

실습 검증: 최소 목적값 0.16, forward 일치

<!-- lecture-page -->

## 두 절점 사이의 비용과 가능 구간

각 구간에서 켜진 ReLU만 남겨 비용식을 정리합니다.

| u 구간 | 켜진 항 | 비용식 | f(u)≤0.25의 조건 |
| --- | --- | --- | --- |
| 0~0.4 | 없음 | 0.4−0.6u | u≥0.25 |
| 0.4~0.7 | u−0.4 | 0.4u | u≤0.625 |
| 0.7~1 | 두 항 모두 | 0.9u−0.35 | u≤2/3, 해당 구간에 없음 |

가능 구간은 [0.25,0.625]입니다. 최소점 u=0.4에서 두 ReLU가 0이므로 f=0.4−0.6×0.4=0.16입니다.

예를 들어 u=0.6이면 h₁=0.2,h₂=0이고 f=0.4−0.36+0.2=0.24입니다. 중간 구간의 0.4u=0.24와 일치하므로 구간식과 원래 신경망을 서로 확인할 수 있습니다.

<!-- lecture-page -->

## LP 행렬의 열과 부등식

변수 순서를 [u,h₁,h₂]로 고정합니다. linprog의 A_ub는 각 행과 변수 벡터를 내적한 값이 b_ub 이하가 되도록 해석합니다.

| 코드의 값 | 해당 수식 | 역할 |
| --- | --- | --- |
| 목적 계수 [−0.6,1,0.5] | −0.6u+h₁+0.5h₂ | 상수 0.4를 뺀 비용 |
| 행 [1,−1,0], 우변 0.4 | u−h₁≤0.4 | h₁≥u−0.4 |
| 행 [1,0,−1], 우변 0.7 | u−h₂≤0.7 | h₂≥u−0.7 |
| h의 bounds (0,None) | h₁,h₂≥0 | ReLU의 다른 하한 |

해 [0.4,0,0]을 대입하면 행 값은 [0.4,0.4]로 우변 이하입니다. solver 목적값 −0.24에 상수 0.4를 더해 0.16을 보고합니다. 원래 forward에서 계산한 비용도 0.16이어야 합니다.

양의 h 계수 때문에 이 목적식은 h를 가능한 작게 만듭니다. 목적 계수의 부호를 바꾸면 이 복원 논리를 다시 검사해야 합니다.

<!-- lecture-page -->

## 출력 하한 제약의 반례

0 ≤ u ≤ 1에서 f(u) = ReLU(u)라 두고 f(u) ≥ 0.8을 만족하며 u를 최소화. 실제 최적점은 u = 0.8

<math display="block"><mtable columnalign="left"><mtr><mtd><mrow><mi>h</mi><mo>≥</mo><mi>u</mi><mo>,</mo><mi>h</mi><mo>≥</mo><mn>0</mn><mo>,</mo><mi>h</mi><mo>≥</mo><mn>.8</mn></mrow></mtd></mtr></mtable></math>

이 완화에서는 u = 0, h = 0.8이 허용됩니다. 비용을 줄이려고 보조변수를 부풀린 결과입니다. 작은 MIP gap이나 LP optimal 종료 상태로 이 모델링 오류를 발견할 수는 없습니다.

u=0,h=0.8을 두면 세 선형 부등식은 모두 만족하지만 실제 f(0)=0입니다. 출력 하한을 잘못 표현한 모델은 정확히 풀어도 잘못된 입력을 반환합니다. solver 상태 확인 뒤 순전파 검사가 필요한 이유입니다.

<!-- lecture-page -->

## 출력 보상과 그래프 등식의 반례

같은 ReLU에서 −h를 최소화하면 h의 상한이 없는 epigraph LP는 unbounded입니다. 실제 f(u)는 [0, 1]에 있어 min −f(u) = −1입니다.

또한 f(u) = &#124;u&#124;의 그래프 위에 있는 (−1, 1), (1, 1)의 중점 (0, 1)은 그래프에 없습니다.

비용 epigraph의 동치성을 농도 등식이나 출력 보상에 그대로 옮기면 문제가 달라집니다.

<!-- lecture-page -->

## PICNN과 고정 context

PICNN은 일부 입력에만 convexity를 부여합니다. 공급 조건 c를 처리하는 경로는 비선형이어도, c를 고정한 뒤 결정변수 u의 경로가 필요한 부호 조건을 만족해야 합니다.

다음 페이지는 context가 층의 계수를 결정하는 충분조건 형태를 사용합니다. 원 논문의 gate 구조도 고정 context에서 이 관점으로 해석할 수 있습니다.

[Amos, Xu and Kolter, Input Convex Neural Networks, ICML 2017, pp. 146-155](https://proceedings.mlr.press/v70/amos17b.html)

<!-- lecture-page -->

## 조건부 계수와 LP 구성

<math display="block"><mtable columnalign="left"><mtr><mtd><mrow><msub><mi>h</mi><mrow><mi>k</mi></mrow></msub><mo>=</mo><mi mathvariant="normal">ReLU</mi><mo>(</mo><msub><mi>W</mi><mrow><mi>k</mi></mrow></msub><mo>(</mo><mi>c</mi><mo>)</mo><msub><mi>h</mi><mrow><mi>k</mi><mo>−</mo><mn>1</mn></mrow></msub><mo>+</mo><msub><mi>A</mi><mrow><mi>k</mi></mrow></msub><mo>(</mo><mi>c</mi><mo>)</mo><mi>u</mi><mo>+</mo><msub><mi>b</mi><mrow><mi>k</mi></mrow></msub><mo>(</mo><mi>c</mi><mo>)</mo><mo>)</mo></mrow></mtd></mtr><mtr><mtd><mrow><msub><mi>W</mi><mrow><mi>k</mi></mrow></msub><mo>(</mo><mi>c</mi><mo>)</mo><mo>≥</mo><mn>0</mn><mo>,</mo><mi>w</mi><mo>(</mo><mi>c</mi><mo>)</mo><mo>≥</mo><mn>0</mn></mrow></mtd></mtr></mtable></math>

관측 c를 context 경로에 한 번 넣어 계수를 계산한 뒤 고정합니다. 나머지 결정변수와 제약이 선형이면 ReLU epigraph를 LP로 구성합니다.

c도 최적화하면 W(c)h나 A(c)u가 비선형 결합이 될 수 있습니다. 고정 context의 결론이 공동 최적화로 이어지지는 않습니다.

관측 c에서 계산된 W(c), A(c), b(c)는 숫자입니다. 이를 고정하면 최적화 변수 u와 h에 대해 모든 식이 affine입니다. c도 변수로 남기면 “숫자 계수×변수”가 “변수의 함수×변수”가 되어 같은 LP가 아닙니다.

<!-- lecture-page -->

## 조건부 convexity와 공동 convexity

<math display="block"><mtable columnalign="left"><mtr><mtd><mrow><mi>f</mi><mo>(</mo><mi>u</mi><mo>;</mo><mi>c</mi><mo>)</mo><mo>=</mo><mo>&#124;</mo><mi>u</mi><mo>−</mo><mi>c</mi><mo>&#124;</mo><mo>−</mo><mn>.1</mn><msup><mi>c</mi><mrow><mn>2</mn></mrow></msup></mrow></mtd></mtr><mtr><mtd><mrow><mn>0</mn><mo>≤</mo><mi>u</mi><mo>≤</mo><mn>1</mn><mo>,</mo><mn>0</mn><mo>≤</mo><mi>c</mi><mo>≤</mo><mn>1</mn></mrow></mtd></mtr></mtable></math>

고정 c에서 최적점은 u = c. 실습은 c = 0.2, 0.5, 0.8에 대한 LP를 각각 풉니다.

u = c인 선 위에서는 f = −0.1c²입니다. 끝점 함수값의 평균은 −0.05인데 중점 값은 −0.025이므로 공동 convexity 조건을 위반합니다.

고정 c=0.2에서는 <math xmlns="http://www.w3.org/1998/Math/MathML"><mrow><mo stretchy="false">&#x7C;</mo><mi>u</mi><mo>−</mo><mn>0.2</mn><mo stretchy="false">&#x7C;</mo></mrow></math>를 보조변수 t의 두 하한 t≥u−0.2, t≥0.2−u로 표현하고 t−0.004를 최소화합니다. u=0.2,t=0에서 최솟값 −0.004입니다. c가 변수가 되면 목적식의 −0.1c²가 상수가 아니므로 이 LP를 그대로 사용할 수 없습니다.

<!-- lecture-page -->

## 알려진 convex 함수를 이용한 학습

<math display="block"><mtable columnalign="left"><mtr><mtd><mrow><mi>q</mi><mo>(</mo><mi>u</mi><mo>)</mo><mo>=</mo><mo>(</mo><mi>u</mi><mo>−</mo><mn>.6</mn><msup><mo>)</mo><mrow><mn>2</mn></mrow></msup><mo>+</mo><mn>.1</mn><mi>u</mi><mo>+</mo><mn>.2</mn></mrow></mtd></mtr><mtr><mtd><mrow><mi>f</mi><mo>(</mo><mi>u</mi><mo>)</mo><mo>=</mo><mi>b</mi><mo>+</mo><mi>a</mi><mi>u</mi><mo>+</mo><msup><msub><mo>∑</mo><mrow><mi>j</mi><mo>=</mo><mn>1</mn></mrow></msub><mrow><mn>9</mn></mrow></msup><msub><mi>w</mi><mrow><mi>j</mi></mrow></msub><mi mathvariant="normal">ReLU</mi><mo>(</mo><mi>u</mi><mo>−</mo><msub><mi>κ</mi><mrow><mi>j</mi></mrow></msub><mo>)</mo></mrow></mtd></mtr><mtr><mtd><mrow><msub><mi>κ</mi><mrow><mi>j</mi></mrow></msub><mo>=</mo><mn>.1</mn><mi>j</mi><mo>,</mo><msub><mi>w</mi><mrow><mi>j</mi></mrow></msub><mo>≥</mo><mn>0</mn></mrow></mtd></mtr></mtable></math>

41개 균등 입력에서 계수를 학습하고 별도의 200개 중간 지점에서 평가합니다. Knot을 고정했으므로 이 실습의 학습은 bound가 있는 선형 least squares입니다.

고정 knot을 사용하는 이 얕은 ICNN은 convex 학습이 가능한 특수한 경우입니다. 깊은 ICNN의 일반적인 학습에는 이 결론을 적용할 수 없습니다.

절점 κ가 고정이면 각 입력의 ReLU 특성을 미리 계산할 수 있습니다. 계수 b,a,w만 미지수이므로 제한된 선형 최소제곱입니다. w≥0은 절점에서 기울기가 감소하지 않게 해 학습된 곡선의 convexity를 유지합니다.

예를 들어 u=0.25의 특성 행은 [1,0.25,0.15,0.05,0,0,0,0,0,0,0]입니다. 절점 0.1과 0.2만 지났으므로 두 hinge만 양수입니다. b,a 두 계수는 음수도 허용하고 나머지 9개에는 하한 0을 주어 최소제곱을 풉니다.

<!-- lecture-page -->

## 학습 곡선과 선택한 부하

<figure><img src="/assets/courses/surrogate-models/week-07/fit-ko.png" alt="Convex 기준 함수와 학습 ICNN 및 선택 입력" /></figure>

독립 평가 RMSE: 0.000760. LP 선택: u = 0.50. 기준 함수의 최소점: u = 0.55

두 점 사이의 기준 비용 차이는 0.0025입니다. 예측 곡선이 가까워도 최소점 위치는 달라질 수 있습니다.

최소점 근처에서 기준 곡선이 평평하면 입력이 조금 이동해도 비용 차이는 작습니다. 이 예의 입력 차이 0.05와 비용 차이 0.0025는 서로 다른 평가량입니다. 그래프가 겹쳐 보인다는 이유만으로 최적 입력까지 같다고 판단하지 않습니다.

<!-- lecture-page -->

## 예측 오차와 선택한 입력의 손실

기준 비용 q(u)=(u−0.6)²+0.1u+0.2를 완전제곱으로 정리하면 q(u)=(u−0.55)²+0.2575입니다. 최소점에서 벗어난 거리의 제곱이 비용 증가량입니다.

| 입력 | 기준 비용 계산 | 비용 |
| --- | --- | --- |
| 기준 최소 u=0.55 | 0²+0.2575 | 0.2575 |
| 모델 선택 u=0.50 | (−0.05)²+0.2575 | 0.2600 |
| 차이 | 0.2600−0.2575 | 0.0025 |

모델이 선택한 점의 예측 비용 0.258437과 기준 비용 0.260000의 차이 0.001563은 그 점의 예측 오차입니다. 기준 최소값과의 차이 0.0025는 선택 때문에 생긴 비용 손실입니다.

같은 숫자를 비교하는 기준이 다릅니다. 정확도 표와 의사결정 평가 표에서 각각 무엇을 빼는지 명시합니다.

<!-- lecture-page -->

## LP 결과의 검증 항목

1. 입력 domain, context, scaling, 모델 가중치를 저장
2. W와 w의 부호, 목적함수 방향, 모든 출력 사용 위치를 확인
3. 선택한 u를 원래 네트워크에 넣어 LP 목적값과 비교
4. 기준 함수의 목적값·제약을 따로 계산

학습 모델의 LP 목적값: 0.258437. 기준 비용: 0.260000. 두 값의 차이: 서로게이트 오차

<!-- lecture-page -->

## 모델 구조의 선택 기준

<table><thead><tr><th style="font-size:clamp(15px,1.7cqw,22px)">대상과 조건</th><th style="font-size:clamp(15px,1.7cqw,22px)">검토할 접근</th></tr></thead><tbody><tr><td style="font-size:clamp(15px,1.7cqw,22px)">알려진 convex 비용의 최소화</td><td style="font-size:clamp(15px,1.7cqw,22px)">ICNN 또는 고정-context PICNN</td></tr><tr><td style="font-size:clamp(15px,1.7cqw,22px)">ReLU·선형 출력·선형 외부 제약</td><td style="font-size:clamp(15px,1.7cqw,22px)">조건을 확인한 epigraph LP</td></tr><tr><td style="font-size:clamp(15px,1.7cqw,22px)">농도 등식·복잡한 비convex 응답</td><td style="font-size:clamp(15px,1.7cqw,22px)">일반 서로게이트와 적절한 NLP/MILP</td></tr><tr><td style="font-size:clamp(15px,1.7cqw,22px)">Convexity 근거가 약한 데이터</td><td style="font-size:clamp(15px,1.7cqw,22px)">구조 제약의 예측 편향과 결정 오차 비교</td></tr></tbody></table>

<!-- lecture-page -->

## 실습 실행과 확인 결과

```bash
python -m pip install -r requirements.txt
python week07_lab.py --output-dir my-results
```

코드 묶음을 풀어 실행합니다. results.json, 학습 계수, training.csv와 heldout.csv를 저장

손 계산 최적값 0.16, 학습 모델의 부호 조건, LP·forward 일치, 출력 하한 반례와 unbounded 반례를 자동 검사합니다. Notebook에는 같은 함수를 단계별로 실행하는 셀이 있습니다.

<!-- lecture-page -->

## 과제: 동치성 조건과 의사결정 오차

1. 두 hinge 모델에 비용 상한 0.25를 추가하고 feasible 구간의 양 끝을 계산
2. 출력 하한 반례를 실행하고 잘못 허용된 u와 실제 출력을 기록
3. 학습 모델의 knot 간격을 0.1에서 0.05로 바꿔 예측 오차와 기준 비용 손실을 비교
4. c를 고정해야 하는 이유와 현재 모델에 허용된 출력 사용 방식을 설명합니다.

<!-- lecture-page -->

## 해설 자료와 원문

[7주차 해설과 연습](/courses/surrogate-models/week-07-reading/)에서 epigraph 동치성 증명, LP 행렬, 부호 제약 학습과 반례를 계산

[Amos, Xu and Kolter, Input Convex Neural Networks, ICML 2017, pp. 146-155](https://proceedings.mlr.press/v70/amos17b.html)

[Boyd and Vandenberghe, Convex Optimization, §§3.1-3.2 and 4.1-4.3](https://web.stanford.edu/~boyd/cvxbook/bv_cvxbook.pdf)

[SciPy bounded least squares](https://docs.scipy.org/doc/scipy/reference/generated/scipy.optimize.lsq_linear.html) · [SciPy HiGHS LP interface](https://docs.scipy.org/doc/scipy/reference/generated/scipy.optimize.linprog.html)
