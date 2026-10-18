---
layout: post
title: "Benders Decomposition and C&CG: Cuts, Scenarios, and Certified Bounds"
title_ko: "Benders 분해와 C&CG: 컷, 시나리오, 그리고 상하한"
date: 2026-10-18
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
  - "Benders decomposition"
  - "C&CG"
  - "two-stage robust optimization"
  - "recourse"
  - "duality"
  - "decomposition methods"
excerpt: "Derive Benders cuts and C&CG scenario blocks, trace two capacity-planning examples, and check which solver bounds certify convergence."
excerpt_ko: "Benders 컷과 C&CG 시나리오 블록을 유도하고 설비 용량 예제로 반복 계산을 따라가며 수렴을 인증하는 상하한을 확인한다."
language: "en-ko"
has_korean_note: false
---

A plant designer chooses equipment capacity before production starts. Once that capacity is fixed, an operating problem decides how to meet demand. Solving both decisions together may be expensive, especially with integer design choices or many possible demand realizations.

Benders decomposition passes information from the operating problem to the design problem as cuts. Column-and-constraint generation (C&CG), in two-stage robust optimization, adds the operating variables and constraints of selected uncertainty scenarios. Both alternate between a master problem and a subproblem, but they retain different information between iterations.

## 1. Benders decomposition: learning the operating-cost function

### Separate the design decision from recourse

Let x denote design decisions and y denote operating, or recourse, decisions. Consider

<math display="block" aria-label="A separable optimization problem and its recourse value"><mtable columnalign="left"><mtr><mtd><munder><mo>min</mo><mrow><mi>x</mi><mo>∈</mo><mi>X</mi></mrow></munder><msup><mi>c</mi><mi>T</mi></msup><mi>x</mi><mo>+</mo><mi>Q</mi><mo>(</mo><mi>x</mi><mo>)</mo></mtd></mtr><mtr><mtd><mi>Q</mi><mo>(</mo><mi>x</mi><mo>)</mo><mo>=</mo><munder><mo>min</mo><mrow><mi>y</mi><mo>≥</mo><mn>0</mn></mrow></munder><mo>{</mo><msup><mi>q</mi><mi>T</mi></msup><mi>y</mi><mo>:</mo><mi>W</mi><mi>y</mi><mo>≥</mo><mi>h</mi><mo>−</mo><mi>T</mi><mi>x</mi><mo>}</mo></mtd></mtr></mtable></math>

X contains the first-stage constraints and may include integer variables. The fixed data c and q are cost vectors; W and T are constraint matrices, and h is a right-hand-side vector. Fixing x leaves a linear program in continuous y. Its optimal value Q(x) is the least operating cost compatible with that design.

The classical method introduced by [Benders (1962)](https://doi.org/10.1007/BF01386316) exploits this separation. The master chooses x and a cost estimate θ. The subproblem evaluates Q(x) and supplies a constraint that improves the master.

Assume operating cost is bounded below wherever recourse is feasible and an optimum is attained. For a feasible subproblem, LP strong duality gives

<math display="block" aria-label="The dual of the continuous recourse problem"><mtable columnalign="left"><mtr><mtd><mi>Π</mi><mo>=</mo><mo>{</mo><mi>π</mi><mo>≥</mo><mn>0</mn><mo>:</mo><msup><mi>W</mi><mi>T</mi></msup><mi>π</mi><mo>≤</mo><mi>q</mi><mo>}</mo></mtd></mtr><mtr><mtd><mi>Q</mi><mo>(</mo><mi>x</mi><mo>)</mo><mo>=</mo><munder><mo>max</mo><mrow><mi>π</mi><mo>∈</mo><mi>Π</mi></mrow></munder><msup><mi>π</mi><mi>T</mi></msup><mo>(</mo><mi>h</mi><mo>−</mo><mi>T</mi><mi>x</mi><mo>)</mo></mtd></mtr></mtable></math>

The dual feasible set Π is independent of x because W and q are fixed. Every dual-feasible π supplies an affine lower bound on operating cost. For any feasible y,

<math display="block" aria-label="Weak duality gives a global lower bound"><msup><mi>q</mi><mi>T</mi></msup><mi>y</mi><mo>≥</mo><msup><mi>π</mi><mi>T</mi></msup><mi>W</mi><mi>y</mi><mo>≥</mo><msup><mi>π</mi><mi>T</mi></msup><mo>(</mo><mi>h</mi><mo>−</mo><mi>T</mi><mi>x</mi><mo>)</mo></math>

Taking the minimum over y preserves this bound. If the subproblem at the current design returns an optimal dual solution <math><msup><mi>π</mi><mi>k</mi></msup></math>, add

<math display="block" aria-label="A Benders optimality cut"><mi>θ</mi><mo>≥</mo><mo>(</mo><msup><mi>π</mi><mi>k</mi></msup><msup><mo>)</mo><mi>T</mi></msup><mo>(</mo><mi>h</mi><mo>−</mo><mi>T</mi><mi>x</mi><mo>)</mo></math>

This is an optimality cut. It is valid for every feasible design, including designs with integer components, and is tight at the design where it was generated. Accumulating such cuts builds a piecewise linear lower approximation to Q.

### An infeasible operating problem needs a different cut

Some designs cannot meet the operating constraints. An infeasible subproblem has no finite operating cost to insert into an optimality cut. A Farkas certificate r can instead satisfy the first line below and generate the second:

<math display="block" aria-label="A Farkas certificate and the resulting feasibility cut"><mtable columnalign="left"><mtr><mtd><mi>r</mi><mo>≥</mo><mn>0</mn><mo>,</mo><mspace width=".5em"/><msup><mi>W</mi><mi>T</mi></msup><mi>r</mi><mo>≤</mo><mn>0</mn><mo>,</mo><mspace width=".5em"/><msup><mi>r</mi><mi>T</mi></msup><mo>(</mo><mi>h</mi><mo>−</mo><mi>T</mi><msup><mi>x</mi><mi>k</mi></msup><mo>)</mo><mo>&gt;</mo><mn>0</mn></mtd></mtr><mtr><mtd><msup><mi>r</mi><mi>T</mi></msup><mo>(</mo><mi>h</mi><mo>−</mo><mi>T</mi><mi>x</mi><mo>)</mo><mo>≤</mo><mn>0</mn></mtd></mtr></mtable></math>

To check the sign, any feasible y satisfies <math><msup><mi>r</mi><mi>T</mi></msup><mi>W</mi><mi>y</mi><mo>≤</mo><mn>0</mn></math> because <math><msup><mi>W</mi><mi>T</mi></msup><mi>r</mi><mo>≤</mo><mn>0</mn></math> and y ≥ 0. It also satisfies <math><msup><mi>r</mi><mi>T</mi></msup><mi>W</mi><mi>y</mi><mo>≥</mo><msup><mi>r</mi><mi>T</mi></msup><mo>(</mo><mi>h</mi><mo>−</mo><mi>T</mi><mi>x</mi><mo>)</mo></math>. Therefore every design admitting feasible recourse must satisfy the generated inequality. The current design violates it. This is a feasibility cut.

The certificate is often obtained as a dual ray or from a phase-I feasibility problem. Solver conventions differ; the inequality should be checked against the original constraint directions.

### The master, bounds, and stopping rule

Let E index stored optimality cuts and R stored feasibility cuts. The restricted master is

<math display="block" aria-label="A restricted Benders master problem"><mtable columnalign="left"><mtr><mtd><munder><mo>min</mo><mrow><mi>x</mi><mo>,</mo><mi>θ</mi></mrow></munder><msup><mi>c</mi><mi>T</mi></msup><mi>x</mi><mo>+</mo><mi>θ</mi></mtd></mtr><mtr><mtd><mi>x</mi><mo>∈</mo><mi>X</mi><mo>,</mo><mspace width=".5em"/><mi>θ</mi><mo>≥</mo><munder><mi>θ</mi><mo>_</mo></munder></mtd></mtr><mtr><mtd><mi>θ</mi><mo>≥</mo><mo>(</mo><msup><mi>π</mi><mi>j</mi></msup><msup><mo>)</mo><mi>T</mi></msup><mo>(</mo><mi>h</mi><mo>−</mo><mi>T</mi><mi>x</mi><mo>)</mo><mo>,</mo><mspace width=".5em"/><mi>j</mi><mo>∈</mo><mi>E</mi></mtd></mtr><mtr><mtd><mo>(</mo><msup><mi>r</mi><mi>j</mi></msup><msup><mo>)</mo><mi>T</mi></msup><mo>(</mo><mi>h</mi><mo>−</mo><mi>T</mi><mi>x</mi><mo>)</mo><mo>≤</mo><mn>0</mn><mo>,</mo><mspace width=".5em"/><mi>j</mi><mo>∈</mo><mi>R</mi></mtd></mtr></mtable></math>

The underlined θ is a known global lower bound on recourse cost. Zero is valid when all operating costs are nonnegative. Without a valid initial bound or suitable initial cuts, the first master may be unbounded.

For minimization, the master relaxes the full problem, so its globally optimal objective is a lower bound, LB. A design with feasible recourse supplies an upper bound, UB, through its actual total cost. With exact solves,

<math display="block" aria-label="Bounds for minimization with an exactly solved master and recourse"><mtable columnalign="left"><mtr><mtd><msub><mi>LB</mi><mi>k</mi></msub><mo>=</mo><msup><mi>c</mi><mi>T</mi></msup><msup><mi>x</mi><mi>k</mi></msup><mo>+</mo><msup><mi>θ</mi><mi>k</mi></msup></mtd></mtr><mtr><mtd><msub><mi>UB</mi><mi>k</mi></msub><mo>=</mo><mo>min</mo><mo>{</mo><msub><mi>UB</mi><mrow><mi>k</mi><mo>−</mo><mn>1</mn></mrow></msub><mo>,</mo><msup><mi>c</mi><mi>T</mi></msup><msup><mi>x</mi><mi>k</mi></msup><mo>+</mo><mi>Q</mi><mo>(</mo><msup><mi>x</mi><mi>k</mi></msup><mo>)</mo><mo>}</mo></mtd></mtr></mtable></math>

Only a feasible subproblem updates UB. Store the design that achieved the best UB; this is the incumbent to return.

```text
Initialize a valid recourse lower bound, empty cut sets, and UB = +infinity.
Repeat:
    Solve the restricted master; obtain x, theta, and LB.
    If the master is certified infeasible, return infeasible.
    Solve the operating LP at x.
    If infeasible:
        Add a certified feasibility cut.
    Otherwise:
        Update UB and its incumbent using the evaluated total cost.
        If the certified gap is within tolerance, return the incumbent.
        Add an optimality cut from an optimal dual solution.
```

A practical absolute-plus-relative stopping test is

<math display="block" aria-label="An absolute and relative optimality gap criterion"><mi>UB</mi><mo>−</mo><mi>LB</mi><mo>≤</mo><msub><mi>ε</mi><mtext>abs</mtext></msub><mo>+</mo><msub><mi>ε</mi><mtext>rel</mtext></msub><mo>max</mo><mo>{</mo><mn>1</mn><mo>,</mo><mo>|</mo><mi>UB</mi><mo>|</mo><mo>}</mo></math>

If a mixed-integer master stops early, its incumbent objective is an upper bound on that restricted master. Use the solver's best bound for the original problem's LB. A dual-feasible, suboptimal subproblem solution still gives a valid cut, but the cut need not be tight. A feasible operating solution gives a valid UB even if its operating cost has not been minimized exactly.

### A numerical example: capacity versus emergency purchases

Use normalized capacity, production, and cost units over one planning period. Capacity x costs 2 per unit, in-house production y costs 3, and emergency purchases z cost 9. Demand is 8. Purchases have no upper limit, so every allowed capacity admits recourse:

<math display="block" aria-label="A capacity and production example with demand eight"><mtable columnalign="left"><mtr><mtd><munder><mo>min</mo><mrow><mn>0</mn><mo>≤</mo><mi>x</mi><mo>≤</mo><mn>12</mn></mrow></munder><mn>2</mn><mi>x</mi><mo>+</mo><mi>Q</mi><mo>(</mo><mi>x</mi><mo>)</mo></mtd></mtr><mtr><mtd><mi>Q</mi><mo>(</mo><mi>x</mi><mo>)</mo><mo>=</mo><munder><mo>min</mo><mrow><mi>y</mi><mo>,</mo><mi>z</mi><mo>≥</mo><mn>0</mn></mrow></munder><mo>{</mo><mn>3</mn><mi>y</mi><mo>+</mo><mn>9</mn><mi>z</mi><mo>:</mo><mi>y</mi><mo>+</mo><mi>z</mi><mo>≥</mo><mn>8</mn><mo>,</mo><mi>y</mi><mo>≤</mo><mi>x</mi><mo>}</mo></mtd></mtr></mtable></math>

In-house production is cheaper than purchases. It therefore supplies the smaller of capacity and demand, with purchases covering the remainder. Direct substitution gives

<math display="block" aria-label="The exact piecewise linear recourse value"><mi>Q</mi><mo>(</mo><mi>x</mi><mo>)</mo><mo>=</mo><mn>24</mn><mo>+</mo><mn>6</mn><mo>max</mo><mo>{</mo><mn>8</mn><mo>−</mo><mi>x</mi><mo>,</mo><mn>0</mn><mo>}</mo><mo>=</mo><mo>max</mo><mo>{</mo><mn>72</mn><mo>−</mo><mn>6</mn><mi>x</mi><mo>,</mo><mn>24</mn><mo>}</mo></math>

The subproblem dual makes the two affine pieces explicit:

<math display="block" aria-label="The production subproblem dual"><munder><mo>max</mo><mrow><mi>α</mi><mo>,</mo><mi>β</mi><mo>≥</mo><mn>0</mn></mrow></munder><mo>{</mo><mn>8</mn><mi>α</mi><mo>−</mo><mi>β</mi><mi>x</mi><mo>:</mo><mi>α</mi><mo>−</mo><mi>β</mi><mo>≤</mo><mn>3</mn><mo>,</mo><mi>α</mi><mo>≤</mo><mn>9</mn><mo>}</mo></math>

Here α multiplies the demand constraint and β multiplies −y ≥ −x. Two dual optima encountered during the iterations generate

<math display="block" aria-label="The two cuts found in the example"><mtable columnalign="left"><mtr><mtd><mo>(</mo><mi>α</mi><mo>,</mo><mi>β</mi><mo>)</mo><mo>=</mo><mo>(</mo><mn>9</mn><mo>,</mo><mn>6</mn><mo>)</mo><mo>:</mo><mspace width=".5em"/><mi>θ</mi><mo>≥</mo><mn>72</mn><mo>−</mo><mn>6</mn><mi>x</mi></mtd></mtr><mtr><mtd><mo>(</mo><mi>α</mi><mo>,</mo><mi>β</mi><mo>)</mo><mo>=</mo><mo>(</mo><mn>3</mn><mo>,</mo><mn>0</mn><mo>)</mo><mo>:</mo><mspace width=".5em"/><mi>θ</mi><mo>≥</mo><mn>24</mn></mtd></mtr></mtable></math>

Starting with θ ≥ 0, the iterations are

| Quantity | Iteration 1 | Iteration 2 | Iteration 3 |
|---|---:|---:|---:|
| Master x | 0 | 12 | 8 |
| Master θ | 0 | 0 | 24 |
| LB | 0 | 24 | 40 |
| Evaluated Q(x) | 72 | 24 | 24 |
| Best UB | 72 | 48 | 40 |

After one cut, the master selects x = 12 and predicts zero operating cost. Evaluation reveals a cost of 24, producing the second cut. With both cuts present, the master represents the entire value function in this example and selects x = 8. The total cost is 40.

Removing emergency purchases changes feasibility: any x &lt; 8 then makes the operating problem infeasible. A feasibility cut is x ≥ 8. In models where every allowed first-stage decision has feasible recourse, this property is called relatively complete recourse.

## 2. C&CG: adding scenarios with their recourse decisions

### First choose a design, then observe uncertainty, then operate

Suppose demand or renewable supply is uncertain. In two-stage robust optimization, x is chosen before uncertainty u is observed; y can adjust after observation. The objective minimizes first-stage cost plus worst-case optimal operating cost:

<math display="block" aria-label="Two-stage robust optimization with continuous recourse"><mtable columnalign="left"><mtr><mtd><munder><mo>min</mo><mrow><mi>x</mi><mo>∈</mo><mi>X</mi></mrow></munder><msup><mi>c</mi><mi>T</mi></msup><mi>x</mi><mo>+</mo><mi>Ψ</mi><mo>(</mo><mi>x</mi><mo>)</mo></mtd></mtr><mtr><mtd><mi>Ψ</mi><mo>(</mo><mi>x</mi><mo>)</mo><mo>=</mo><munder><mo>max</mo><mrow><mi>u</mi><mo>∈</mo><mi>U</mi></mrow></munder><mi>Q</mi><mo>(</mo><mi>x</mi><mo>,</mo><mi>u</mi><mo>)</mo></mtd></mtr><mtr><mtd><mi>Q</mi><mo>(</mo><mi>x</mi><mo>,</mo><mi>u</mi><mo>)</mo><mo>=</mo><munder><mo>min</mo><mrow><mi>y</mi><mo>≥</mo><mn>0</mn></mrow></munder><mo>{</mo><msup><mi>q</mi><mi>T</mi></msup><mi>y</mi><mo>:</mo><mi>W</mi><mi>y</mi><mo>≥</mo><mi>h</mi><mo>−</mo><mi>T</mi><mi>x</mi><mo>−</mo><mi>M</mi><mi>u</mi><mo>}</mo></mtd></mtr></mtable></math>

U is the specified uncertainty set, and M maps uncertainty into the operating constraints. This exposition uses fixed W and q and uncertainty in the right-hand side. The feasibility condition follows the same decision order: choose x, observe u, then adjust y.

<math display="block" aria-label="The information structure of robust recourse"><mo>∃</mo><mi>x</mi><mo>∈</mo><mi>X</mi><mspace width=".5em"/><mo>∀</mo><mi>u</mi><mo>∈</mo><mi>U</mi><mspace width=".5em"/><mo>∃</mo><mi>y</mi><mo>(</mo><mi>u</mi><mo>)</mo><mo>≥</mo><mn>0</mn><mo>:</mo><mi>W</mi><mi>y</mi><mo>(</mo><mi>u</mi><mo>)</mo><mo>≥</mo><mi>h</mi><mo>−</mo><mi>T</mi><mi>x</mi><mo>−</mo><mi>M</mi><mi>u</mi></math>

The same x must work for every u, while the operating decision may differ by scenario. This assumes that the uncertainty relevant to y has been revealed before y is chosen. Partial or sequential observation requires additional information constraints.

[Zeng and Zhao (2013)](https://doi.org/10.1016/j.orl.2013.05.003) formulate C&CG by generating scenario-specific recourse variables together with their constraints. The [2011 precursor by Zeng](https://optimization-online.org/wp-content/uploads/2011/06/3065.pdf) provides an openly accessible derivation.

### Keep a restricted set of scenarios

Let S index the scenarios identified so far, with fixed realizations <math><msup><mi>u</mi><mi>s</mi></msup></math>. For each scenario, introduce an independent recourse vector <math><msup><mi>y</mi><mi>s</mi></msup></math>:

<math display="block" aria-label="The restricted column-and-constraint generation master"><mtable columnalign="left"><mtr><mtd><munder><mo>min</mo><mrow><mi>x</mi><mo>,</mo><mi>η</mi><mo>,</mo><mo>{</mo><msup><mi>y</mi><mi>s</mi></msup><mo>}</mo></mrow></munder><msup><mi>c</mi><mi>T</mi></msup><mi>x</mi><mo>+</mo><mi>η</mi></mtd></mtr><mtr><mtd><mi>x</mi><mo>∈</mo><mi>X</mi><mo>,</mo><mspace width=".5em"/><mi>η</mi><mo>≥</mo><munder><mi>η</mi><mo>_</mo></munder></mtd></mtr><mtr><mtd><mi>η</mi><mo>≥</mo><msup><mi>q</mi><mi>T</mi></msup><msup><mi>y</mi><mi>s</mi></msup><mo>,</mo><mspace width=".5em"/><mi>s</mi><mo>∈</mo><mi>S</mi></mtd></mtr><mtr><mtd><mi>W</mi><msup><mi>y</mi><mi>s</mi></msup><mo>≥</mo><mi>h</mi><mo>−</mo><mi>T</mi><mi>x</mi><mo>−</mo><mi>M</mi><msup><mi>u</mi><mi>s</mi></msup><mo>,</mo><mspace width=".5em"/><msup><mi>y</mi><mi>s</mi></msup><mo>≥</mo><mn>0</mn><mo>,</mo><mspace width=".5em"/><mi>s</mi><mo>∈</mo><mi>S</mi></mtd></mtr></mtable></math>

The underlined η is a valid lower bound on worst-case recourse cost. All scenario blocks share x. Their operating variables are separate, and η bounds every scenario's cost from above. Minimizing η therefore represents a maximum over the stored scenarios. An expected-cost model would instead use probability-weighted scenario costs.

Here “columns” means the new recourse-variable block <math><msup><mi>y</mi><mi>s</mi></msup></math>; “constraints” means its operating constraints and cost inequality. The master grows in both variables and constraints.

### Search outside the current scenario set

After solving the master, fix its design and solve the adversarial subproblem: maximize Q over all of U. If continuous recourse is feasible and finite for every scenario, strong duality yields

<math display="block" aria-label="The worst-case oracle after dualizing continuous recourse"><mi>Ψ</mi><mo>(</mo><msup><mi>x</mi><mi>k</mi></msup><mo>)</mo><mo>=</mo><munder><mo>max</mo><mrow><mi>u</mi><mo>∈</mo><mi>U</mi><mo>,</mo><mi>π</mi><mo>∈</mo><mi>Π</mi></mrow></munder><msup><mi>π</mi><mi>T</mi></msup><mo>(</mo><mi>h</mi><mo>−</mo><mi>T</mi><msup><mi>x</mi><mi>k</mi></msup><mo>−</mo><mi>M</mi><mi>u</mi><mo>)</mo></math>

The product between u and π generally makes this a bilinear optimization problem. Dualizing the inner LP leaves a potentially difficult global maximization. An exact MILP reformulation needs suitable uncertainty structure and justified bounds; a local NLP solution alone does not certify the maximum.

An exact oracle returns a worst-case scenario and its cost. Add that scenario's recourse-variable and constraint block. The restricted master gives LB; a finite, certified full-set evaluation of the design gives UB:

<math display="block" aria-label="Bounds for column-and-constraint generation with exact solves"><mtable columnalign="left"><mtr><mtd><msub><mi>LB</mi><mi>k</mi></msub><mo>=</mo><msup><mi>c</mi><mi>T</mi></msup><msup><mi>x</mi><mi>k</mi></msup><mo>+</mo><msup><mi>η</mi><mi>k</mi></msup></mtd></mtr><mtr><mtd><msub><mi>UB</mi><mi>k</mi></msub><mo>=</mo><mo>min</mo><mo>{</mo><msub><mi>UB</mi><mrow><mi>k</mi><mo>−</mo><mn>1</mn></mrow></msub><mo>,</mo><msup><mi>c</mi><mi>T</mi></msup><msup><mi>x</mi><mi>k</mi></msup><mo>+</mo><mi>Ψ</mi><mo>(</mo><msup><mi>x</mi><mi>k</mi></msup><mo>)</mo><mo>}</mo></mtd></mtr></mtable></math>

If some scenario admits no feasible recourse, define its Q as +infinity. A feasibility oracle must find such a scenario or certify its absence. Add the violating scenario's block and re-solve; do not update UB from that design. The shared x must then change enough to make that block feasible. The same scenario-block construction can address both operating-cost underestimation and infeasibility.

```text
Initialize a valid recourse lower bound and a small scenario set S.
Set UB = +infinity.
Repeat:
    Solve the restricted master; obtain x, eta, and LB.
    If the master is certified infeasible, return infeasible.
    Check recourse feasibility over the full uncertainty set.
    If a violating scenario is found:
        Add its recourse variables and constraints; continue.
    Solve the worst-case operating-cost problem over the full set.
    Update UB and its incumbent using the certified worst-case cost.
    If the certified gap is within tolerance, return the incumbent.
    Add the worst-case scenario's recourse variables and constraints.
```

The feasibility and cost searches may be implemented by a combined oracle. A finite UB requires both recourse feasibility for every scenario and a certified upper bound on the worst-case operating cost.

The cost of a single adversarial scenario alone does not certify that it is worst-case. For this maximization, a feasible scenario supplies a lower bound on the maximum. A certified global upper bound on the oracle value, together with robust recourse feasibility, can support an outer UB even before the oracle is solved exactly.

### The same plant with uncertain demand

Keep the costs and capacity range from the Benders example, but let demand vary between 6 and 10:

<math display="block" aria-label="The uncertain-demand production example"><mi>Q</mi><mo>(</mo><mi>x</mi><mo>,</mo><mi>d</mi><mo>)</mo><mo>=</mo><munder><mo>min</mo><mrow><mi>y</mi><mo>,</mo><mi>z</mi><mo>≥</mo><mn>0</mn></mrow></munder><mo>{</mo><mn>3</mn><mi>y</mi><mo>+</mo><mn>9</mn><mi>z</mi><mo>:</mo><mi>y</mi><mo>+</mo><mi>z</mi><mo>≥</mo><mi>d</mi><mo>,</mo><mi>y</mi><mo>≤</mo><mi>x</mi><mo>}</mo><mo>,</mo><mspace width=".5em"/><mi>d</mi><mo>∈</mo><mo>[</mo><mn>6</mn><mo>,</mo><mn>10</mn><mo>]</mo></math>

The robust objective is 2x plus the maximum of this operating cost over the demand interval. Start with only d = 6 in the restricted master. It chooses x = 6, with operating cost 18 and total cost 30. At that design, d = 10 requires in-house production 6 and purchases 4. The evaluated total cost is 12 + 18 + 36 = 66.

Adding d = 10 introduces the following block, alongside the existing d = 6 block:

<math display="block" aria-label="The newly generated scenario-ten variable and constraint block"><mtable columnalign="left"><mtr><mtd><msup><mi>y</mi><mn>10</mn></msup><mo>≥</mo><mn>0</mn><mo>,</mo><mspace width=".5em"/><msup><mi>z</mi><mn>10</mn></msup><mo>≥</mo><mn>0</mn></mtd></mtr><mtr><mtd><msup><mi>y</mi><mn>10</mn></msup><mo>+</mo><msup><mi>z</mi><mn>10</mn></msup><mo>≥</mo><mn>10</mn><mo>,</mo><mspace width=".5em"/><msup><mi>y</mi><mn>10</mn></msup><mo>≤</mo><mi>x</mi></mtd></mtr><mtr><mtd><mi>η</mi><mo>≥</mo><mn>3</mn><msup><mi>y</mi><mn>10</mn></msup><mo>+</mo><mn>9</mn><msup><mi>z</mi><mn>10</mn></msup></mtd></mtr></mtable></math>

The superscript 10 labels the demand scenario; it is not a power. Both demand blocks use the same capacity x, and each has its own production and purchase decisions.

| Quantity | Iteration 1 | Iteration 2 |
|---|---:|---:|
| Stored demands | {6} | {6, 10} |
| Master x | 6 | 10 |
| Master η | 18 | 30 |
| LB | 30 | 50 |
| Worst demand | 10 | 10 |
| Worst operating cost | 54 | 30 |
| Best UB | 66 | 50 |

Operating cost is nondecreasing in demand here, so the exact worst case is always d = 10. The algorithm stops at x = 10 and total cost 50. Finding the worst scenario can be much harder with interacting demands, network constraints, or budgeted uncertainty.

## 3. What each iteration retains

| Aspect | Benders | C&CG |
|---|---|---|
| Information added | A dual cost cut or feasibility cut | A scenario's recourse variables and constraints |
| Recourse variables | Eliminated from the basic master | Kept for stored scenarios |
| Subproblem | Fixed-design recourse | Worst-case cost or feasibility search over U |
| Master growth | Inequalities | Variables and inequalities |
| Main cost | Cut quality and repeated solves | Growing masters and adversarial search |

Benders decomposition also applies to stochastic programs and can form the basis of robust cutting-plane methods. C&CG is one way to organize a two-stage robust problem; the presence of uncertainty alone does not select an algorithm.

For continuous LP recourse, the connection is precise. Eliminating the operating variables from the d = 10 block gives

<math display="block" aria-label="Projecting one complete scenario block into the first-stage space"><mi>η</mi><mo>≥</mo><mi>Q</mi><mo>(</mo><mi>x</mi><mo>,</mo><mn>10</mn><mo>)</mo><mo>=</mo><mo>max</mo><mo>{</mo><mn>90</mn><mo>−</mo><mn>6</mn><mi>x</mi><mo>,</mo><mn>30</mn><mo>}</mo></math>

That one block represents both affine pieces of this scenario's value function. A Benders cost cut supplies one dual-based affine bound at a time. C&CG keeps an extended formulation of the selected scenario's epigraph, which can strengthen the master at the cost of extra variables. This tradeoff does not establish a universal runtime ranking.

For a finite uncertainty set, exact C&CG has only finitely many distinct scenario blocks to add, provided feasibility and worst-case separation are certified. With continuous LP recourse, fixed W and q, and a compact polyhedral right-hand-side uncertainty set, feasible finite Q is convex in u. A maximum is attained at a vertex. An exact oracle that returns vertices then reduces the relevant scenarios to a finite set. These conditions should be checked before claiming finite termination.

Classical Benders likewise has finitely many relevant dual extreme points and feasibility rays in its polyhedral LP setting. Finite termination relies on the usual solvability assumptions, exact solves, and appropriate extreme-point or ray selection. Integer variables in x are compatible with the cuts, but each mixed-integer master may still be expensive.

If recourse contains integer variables, the continuous LP dual no longer represents its exact value. Classical Benders cuts alone may be insufficient, and the displayed dualized C&CG oracle is no longer an exact reformulation. Scenario blocks can still retain integer recourse variables, but require a suitable exact oracle. Logic-based or integer Benders methods and nested C&CG are possible extensions, each requiring its own assumptions. For nonconvex continuous recourse, global solution guarantees also need separate justification.

For a process model, the first checks are concrete: which decisions are fixed before uncertainty is observed, which can adjust afterward, whether recourse is continuous and feasible, and which solver bounds certify the final gap.

## References

- J. F. Benders (1962). “Partitioning procedures for solving mixed-variables programming problems.” *Numerische Mathematik*, 4, 238–252. [DOI](https://doi.org/10.1007/BF01386316).
- Bo Zeng and Long Zhao (2013). “Solving two-stage robust optimization problems using a column-and-constraint generation method.” *Operations Research Letters*, 41(5), 457–461. [DOI](https://doi.org/10.1016/j.orl.2013.05.003).
- Bo Zeng (2011). “Solving Two-stage Robust Optimization Problems by A Constraint-and-Column Generation Method.” Technical report, June 2011. [Open manuscript](https://optimization-online.org/wp-content/uploads/2011/06/3065.pdf).

<!-- ko -->

공장을 설계할 때는 설비 용량을 먼저 정하고 그 용량 안에서 수요를 충족하는 운전 계획을 세운다. 설비 선택에 정수변수가 들어가거나 고려할 수요가 많아지면 두 결정을 한꺼번에 풀기 부담스러워진다.

Benders 분해는 운전 문제에서 얻은 정보를 컷(cut)으로 만들어 설계 문제에 전달한다. 2단계 강건 최적화의 column-and-constraint generation(C&CG)은 선택한 불확실성 시나리오의 운전변수와 제약을 함께 추가한다. 두 방법 모두 주문제(master problem)와 부문제(subproblem)를 번갈아 풀지만 다음 반복에 남기는 정보가 다르다.

## 1. Benders 분해: 운전비 함수를 컷으로 알아가기

### 설계 결정과 후속 운전 결정을 나눈다

설계변수를 x, 설계 이후 조정하는 운전변수를 y라고 하자. 후속 조정 결정을 recourse라고 부른다.

<math display="block" aria-label="A separable optimization problem and its recourse value"><mtable columnalign="left"><mtr><mtd><munder><mo>min</mo><mrow><mi>x</mi><mo>∈</mo><mi>X</mi></mrow></munder><msup><mi>c</mi><mi>T</mi></msup><mi>x</mi><mo>+</mo><mi>Q</mi><mo>(</mo><mi>x</mi><mo>)</mo></mtd></mtr><mtr><mtd><mi>Q</mi><mo>(</mo><mi>x</mi><mo>)</mo><mo>=</mo><munder><mo>min</mo><mrow><mi>y</mi><mo>≥</mo><mn>0</mn></mrow></munder><mo>{</mo><msup><mi>q</mi><mi>T</mi></msup><mi>y</mi><mo>:</mo><mi>W</mi><mi>y</mi><mo>≥</mo><mi>h</mi><mo>−</mo><mi>T</mi><mi>x</mi><mo>}</mo></mtd></mtr></mtable></math>

X는 1단계 제약을 모은 집합이며 정수변수를 포함해도 된다. c와 q는 비용벡터, W와 T는 제약행렬, h는 우변벡터이고 모두 고정된 데이터다. x를 고정하면 연속변수 y에 관한 선형계획법(LP) 문제가 남는다. 그 최적값 Q(x)는 주어진 설계에서 가능한 최소 운전비다.

[Benders(1962)](https://doi.org/10.1007/BF01386316)의 고전적 분해법은 이 구조를 이용한다. 주문제는 x와 운전비 추정값 θ를 정한다. 부문제는 Q(x)를 계산하고 주문제를 보강할 제약을 돌려준다.

운전 문제가 실행 가능할 때 비용의 하한이 유한하고 최적해가 존재한다고 가정하자. 그러면 LP의 강한 쌍대성으로 Q(x)를 쌍대 문제의 최적값으로 표현할 수 있다.

<math display="block" aria-label="The dual of the continuous recourse problem"><mtable columnalign="left"><mtr><mtd><mi>Π</mi><mo>=</mo><mo>{</mo><mi>π</mi><mo>≥</mo><mn>0</mn><mo>:</mo><msup><mi>W</mi><mi>T</mi></msup><mi>π</mi><mo>≤</mo><mi>q</mi><mo>}</mo></mtd></mtr><mtr><mtd><mi>Q</mi><mo>(</mo><mi>x</mi><mo>)</mo><mo>=</mo><munder><mo>max</mo><mrow><mi>π</mi><mo>∈</mo><mi>Π</mi></mrow></munder><msup><mi>π</mi><mi>T</mi></msup><mo>(</mo><mi>h</mi><mo>−</mo><mi>T</mi><mi>x</mi><mo>)</mo></mtd></mtr></mtable></math>

W와 q가 고정되어 있으므로 쌍대 실행 가능 집합 Π는 x에 의존하지 않는다. Π에 속하는 π 하나마다 운전비의 아핀 하계함수를 얻는다. 실행 가능한 y는 아래 부등식을 만족한다.

<math display="block" aria-label="Weak duality gives a global lower bound"><msup><mi>q</mi><mi>T</mi></msup><mi>y</mi><mo>≥</mo><msup><mi>π</mi><mi>T</mi></msup><mi>W</mi><mi>y</mi><mo>≥</mo><msup><mi>π</mi><mi>T</mi></msup><mo>(</mo><mi>h</mi><mo>−</mo><mi>T</mi><mi>x</mi><mo>)</mo></math>

y에 관한 최솟값을 취해도 이 하한은 유지된다. 현재 설계에서 부문제를 풀어 최적 쌍대해 <math><msup><mi>π</mi><mi>k</mi></msup></math>를 얻었다면 아래 부등식을 주문제에 추가한다.

<math display="block" aria-label="A Benders optimality cut"><mi>θ</mi><mo>≥</mo><mo>(</mo><msup><mi>π</mi><mi>k</mi></msup><msup><mo>)</mo><mi>T</mi></msup><mo>(</mo><mi>h</mi><mo>−</mo><mi>T</mi><mi>x</mi><mo>)</mo></math>

이 부등식이 최적성 컷(optimality cut)이다. 컷을 만든 설계에서는 실제 운전비와 같고, 다른 실행 가능한 설계에서도 유효한 하한이다. x에 정수 성분이 있어도 이 성질은 유지된다. 컷을 쌓을수록 Q의 구간별 선형 하한 근사가 보강된다.

### 운전 자체가 불가능하면 실행 가능성 컷이 필요하다

어떤 설계에서는 운전 제약을 만족하는 y가 존재하지 않는다. 이 경우 최적성 컷에 넣을 유한한 운전비를 구할 수 없다. 대신 Farkas 인증서 r로 첫째 줄을 확인하고 둘째 줄을 주문제에 추가한다.

<math display="block" aria-label="A Farkas certificate and the resulting feasibility cut"><mtable columnalign="left"><mtr><mtd><mi>r</mi><mo>≥</mo><mn>0</mn><mo>,</mo><mspace width=".5em"/><msup><mi>W</mi><mi>T</mi></msup><mi>r</mi><mo>≤</mo><mn>0</mn><mo>,</mo><mspace width=".5em"/><msup><mi>r</mi><mi>T</mi></msup><mo>(</mo><mi>h</mi><mo>−</mo><mi>T</mi><msup><mi>x</mi><mi>k</mi></msup><mo>)</mo><mo>&gt;</mo><mn>0</mn></mtd></mtr><mtr><mtd><msup><mi>r</mi><mi>T</mi></msup><mo>(</mo><mi>h</mi><mo>−</mo><mi>T</mi><mi>x</mi><mo>)</mo><mo>≤</mo><mn>0</mn></mtd></mtr></mtable></math>

부호를 직접 확인해보자. 실행 가능한 y는 <math><msup><mi>W</mi><mi>T</mi></msup><mi>r</mi><mo>≤</mo><mn>0</mn></math>, y ≥ 0 때문에 <math><msup><mi>r</mi><mi>T</mi></msup><mi>W</mi><mi>y</mi><mo>≤</mo><mn>0</mn></math>을 만족한다. 원래 제약에서는 <math><msup><mi>r</mi><mi>T</mi></msup><mi>W</mi><mi>y</mi><mo>≥</mo><msup><mi>r</mi><mi>T</mi></msup><mo>(</mo><mi>h</mi><mo>−</mo><mi>T</mi><mi>x</mi><mo>)</mo></math>를 얻는다. 따라서 운전이 가능한 모든 설계는 추가한 부등식을 만족해야 한다. 현재 설계는 이를 위반한다. 이것이 실행 가능성 컷(feasibility cut)다.

인증서는 쌍대 ray나 인공변수를 둔 실행 가능성 검사 문제(phase I)에서 구하는 경우가 많다. 솔버마다 부호 관례가 다를 수 있으므로 원래 제약 방향에 대입해 확인해야 한다.

### 주문제와 상하한

E는 모아둔 최적성 컷의 인덱스, R은 실행 가능성 컷의 인덱스 집합이다.

<math display="block" aria-label="A restricted Benders master problem"><mtable columnalign="left"><mtr><mtd><munder><mo>min</mo><mrow><mi>x</mi><mo>,</mo><mi>θ</mi></mrow></munder><msup><mi>c</mi><mi>T</mi></msup><mi>x</mi><mo>+</mo><mi>θ</mi></mtd></mtr><mtr><mtd><mi>x</mi><mo>∈</mo><mi>X</mi><mo>,</mo><mspace width=".5em"/><mi>θ</mi><mo>≥</mo><munder><mi>θ</mi><mo>_</mo></munder></mtd></mtr><mtr><mtd><mi>θ</mi><mo>≥</mo><mo>(</mo><msup><mi>π</mi><mi>j</mi></msup><msup><mo>)</mo><mi>T</mi></msup><mo>(</mo><mi>h</mi><mo>−</mo><mi>T</mi><mi>x</mi><mo>)</mo><mo>,</mo><mspace width=".5em"/><mi>j</mi><mo>∈</mo><mi>E</mi></mtd></mtr><mtr><mtd><mo>(</mo><msup><mi>r</mi><mi>j</mi></msup><msup><mo>)</mo><mi>T</mi></msup><mo>(</mo><mi>h</mi><mo>−</mo><mi>T</mi><mi>x</mi><mo>)</mo><mo>≤</mo><mn>0</mn><mo>,</mo><mspace width=".5em"/><mi>j</mi><mo>∈</mo><mi>R</mi></mtd></mtr></mtable></math>

밑줄 친 θ는 전체 설계 범위에서 유효한 운전비 하한이다. 운전비가 항상 음이 아니면 0을 써도 된다. 초기 하한이나 적절한 초기 컷이 없으면 첫 주문제가 비유계가 될 수 있다.

최소화 문제에서 주문제는 원문제의 완화 문제이므로 주문제의 전역 최적값은 하한 LB다. 운전이 가능한 설계를 실제로 평가한 총비용은 상한 UB를 준다. 두 문제를 정확히 풀었을 때는 아래 식으로 상하한을 갱신한다.

<math display="block" aria-label="Bounds for minimization with an exactly solved master and recourse"><mtable columnalign="left"><mtr><mtd><msub><mi>LB</mi><mi>k</mi></msub><mo>=</mo><msup><mi>c</mi><mi>T</mi></msup><msup><mi>x</mi><mi>k</mi></msup><mo>+</mo><msup><mi>θ</mi><mi>k</mi></msup></mtd></mtr><mtr><mtd><msub><mi>UB</mi><mi>k</mi></msub><mo>=</mo><mo>min</mo><mo>{</mo><msub><mi>UB</mi><mrow><mi>k</mi><mo>−</mo><mn>1</mn></mrow></msub><mo>,</mo><msup><mi>c</mi><mi>T</mi></msup><msup><mi>x</mi><mi>k</mi></msup><mo>+</mo><mi>Q</mi><mo>(</mo><msup><mi>x</mi><mi>k</mi></msup><mo>)</mo><mo>}</mo></mtd></mtr></mtable></math>

부문제가 실행 가능할 때만 UB를 갱신하며 가장 좋은 UB를 얻은 설계도 함께 저장한다. 종료할 때 반환할 해는 이 설계다.

```text
유효한 운전비 하한을 정하고, 컷 집합을 비우고, UB = +무한대로 둔다.
반복:
    주문제를 풀어 x, theta, LB를 얻는다.
    주문제의 실행 불가능성이 인증되면 원문제도 실행 불가능하다고 반환한다.
    x를 고정한 운전 LP를 푼다.
    실행 불가능하면:
        인증된 실행 가능성 컷을 추가한다.
    실행 가능하면:
        평가한 총비용으로 UB와 저장된 최선 설계를 갱신한다.
        인증된 상하한 차이가 허용오차 이내면 최선 설계를 반환한다.
        최적 쌍대해로 최적성 컷을 추가한다.
```

절대오차와 상대오차를 함께 쓰려면 아래 기준으로 종료 여부를 판단한다.

<math display="block" aria-label="An absolute and relative optimality gap criterion"><mi>UB</mi><mo>−</mo><mi>LB</mi><mo>≤</mo><msub><mi>ε</mi><mtext>abs</mtext></msub><mo>+</mo><msub><mi>ε</mi><mtext>rel</mtext></msub><mo>max</mo><mo>{</mo><mn>1</mn><mo>,</mo><mo>|</mo><mi>UB</mi><mo>|</mo><mo>}</mo></math>

혼합정수 주문제를 시간제한으로 중단했다면 솔버가 찾은 실행 가능 해의 목적값은 그 주문제의 상한이다. 원문제의 LB에는 솔버의 best bound를 써야 한다. 부문제의 쌍대 실행 가능 해는 최적이 아니어도 유효한 컷을 주지만 현재 점에서 운전비와 일치할 필요는 없다. 운전비를 정확히 최소화하지 못했더라도 실행 가능한 운전해를 구했다면 그 총비용으로 유효한 UB를 얻는다.

### 수치 예제: 설비 용량과 긴급 구매

한 계획기간의 용량·생산량·비용을 정규화한 단위로 계산하자. 설비 용량 x의 단위비용은 2, 자체 생산 y의 단위비용은 3, 긴급 구매 z의 단위비용은 9다. 수요는 8이고 긴급 구매에는 상한이 없어 모든 허용 용량에서 운전이 가능하다.

<math display="block" aria-label="A capacity and production example with demand eight"><mtable columnalign="left"><mtr><mtd><munder><mo>min</mo><mrow><mn>0</mn><mo>≤</mo><mi>x</mi><mo>≤</mo><mn>12</mn></mrow></munder><mn>2</mn><mi>x</mi><mo>+</mo><mi>Q</mi><mo>(</mo><mi>x</mi><mo>)</mo></mtd></mtr><mtr><mtd><mi>Q</mi><mo>(</mo><mi>x</mi><mo>)</mo><mo>=</mo><munder><mo>min</mo><mrow><mi>y</mi><mo>,</mo><mi>z</mi><mo>≥</mo><mn>0</mn></mrow></munder><mo>{</mo><mn>3</mn><mi>y</mi><mo>+</mo><mn>9</mn><mi>z</mi><mo>:</mo><mi>y</mi><mo>+</mo><mi>z</mi><mo>≥</mo><mn>8</mn><mo>,</mo><mi>y</mi><mo>≤</mo><mi>x</mi><mo>}</mo></mtd></mtr></mtable></math>

자체 생산이 구매보다 싸므로 용량과 수요 중 작은 양만큼 생산하고 부족분을 구매한다. 이 운전 계획의 비용을 계산하면 Q(x)는 두 아핀 함수의 최댓값이 된다.

<math display="block" aria-label="The exact piecewise linear recourse value"><mi>Q</mi><mo>(</mo><mi>x</mi><mo>)</mo><mo>=</mo><mn>24</mn><mo>+</mo><mn>6</mn><mo>max</mo><mo>{</mo><mn>8</mn><mo>−</mo><mi>x</mi><mo>,</mo><mn>0</mn><mo>}</mo><mo>=</mo><mo>max</mo><mo>{</mo><mn>72</mn><mo>−</mo><mn>6</mn><mi>x</mi><mo>,</mo><mn>24</mn><mo>}</mo></math>

부문제의 쌍대 문제에서도 두 아핀 함수를 확인할 수 있다.

<math display="block" aria-label="The production subproblem dual"><munder><mo>max</mo><mrow><mi>α</mi><mo>,</mo><mi>β</mi><mo>≥</mo><mn>0</mn></mrow></munder><mo>{</mo><mn>8</mn><mi>α</mi><mo>−</mo><mi>β</mi><mi>x</mi><mo>:</mo><mi>α</mi><mo>−</mo><mi>β</mi><mo>≤</mo><mn>3</mn><mo>,</mo><mi>α</mi><mo>≤</mo><mn>9</mn><mo>}</mo></math>

α는 수요 제약, β는 −y ≥ −x에 대응한다. 반복 중 만나는 두 최적 쌍대해에서 아래 컷을 얻는다.

<math display="block" aria-label="The two cuts found in the example"><mtable columnalign="left"><mtr><mtd><mo>(</mo><mi>α</mi><mo>,</mo><mi>β</mi><mo>)</mo><mo>=</mo><mo>(</mo><mn>9</mn><mo>,</mo><mn>6</mn><mo>)</mo><mo>:</mo><mspace width=".5em"/><mi>θ</mi><mo>≥</mo><mn>72</mn><mo>−</mo><mn>6</mn><mi>x</mi></mtd></mtr><mtr><mtd><mo>(</mo><mi>α</mi><mo>,</mo><mi>β</mi><mo>)</mo><mo>=</mo><mo>(</mo><mn>3</mn><mo>,</mo><mn>0</mn><mo>)</mo><mo>:</mo><mspace width=".5em"/><mi>θ</mi><mo>≥</mo><mn>24</mn></mtd></mtr></mtable></math>

θ ≥ 0만 둔 상태에서 시작하면 계산은 이렇게 진행된다.

| 항목 | 반복 1 | 반복 2 | 반복 3 |
|---|---:|---:|---:|
| 주문제 x | 0 | 12 | 8 |
| 주문제 θ | 0 | 0 | 24 |
| LB | 0 | 24 | 40 |
| 평가한 Q(x) | 72 | 24 | 24 |
| 최선 UB | 72 | 48 | 40 |

첫 컷만 넣으면 주문제는 용량 12에서 운전비가 0이라고 추정한다. 실제 운전비는 24이므로 둘째 컷이 필요하다. 두 컷이 모이면 이 예제의 운전비 함수 전체를 표현하고 용량 8과 총비용 40을 얻는다.

긴급 구매를 없애면 실행 가능성도 달라진다. x &lt; 8에서는 운전 부문제가 실행 불가능하며 x ≥ 8이 실행 가능성 컷이 된다. 모든 허용 1단계 결정에서 후속 운전이 가능한 성질을 relatively complete recourse라고 부른다.

## 2. C&CG: 시나리오와 후속 운전 결정을 함께 추가하기

### 설계를 정하고 불확실성을 관측한 뒤 운전한다

수요나 재생에너지 공급이 불확실하다고 하자. 2단계 강건 최적화에서는 불확실성 u를 관측하기 전에 x를 정하고 관측한 뒤 y를 조정한다. 목적함수는 1단계 비용과 최악의 경우에 필요한 최소 운전비의 합을 최소화한다.

<math display="block" aria-label="Two-stage robust optimization with continuous recourse"><mtable columnalign="left"><mtr><mtd><munder><mo>min</mo><mrow><mi>x</mi><mo>∈</mo><mi>X</mi></mrow></munder><msup><mi>c</mi><mi>T</mi></msup><mi>x</mi><mo>+</mo><mi>Ψ</mi><mo>(</mo><mi>x</mi><mo>)</mo></mtd></mtr><mtr><mtd><mi>Ψ</mi><mo>(</mo><mi>x</mi><mo>)</mo><mo>=</mo><munder><mo>max</mo><mrow><mi>u</mi><mo>∈</mo><mi>U</mi></mrow></munder><mi>Q</mi><mo>(</mo><mi>x</mi><mo>,</mo><mi>u</mi><mo>)</mo></mtd></mtr><mtr><mtd><mi>Q</mi><mo>(</mo><mi>x</mi><mo>,</mo><mi>u</mi><mo>)</mo><mo>=</mo><munder><mo>min</mo><mrow><mi>y</mi><mo>≥</mo><mn>0</mn></mrow></munder><mo>{</mo><msup><mi>q</mi><mi>T</mi></msup><mi>y</mi><mo>:</mo><mi>W</mi><mi>y</mi><mo>≥</mo><mi>h</mi><mo>−</mo><mi>T</mi><mi>x</mi><mo>−</mo><mi>M</mi><mi>u</mi><mo>}</mo></mtd></mtr></mtable></math>

U는 정해둔 불확실성 집합이고 M은 불확실성을 운전 제약의 우변에 반영하는 행렬이다. 여기서는 W와 q가 고정되고 불확실성이 우변에 들어가는 형태를 다룬다. 실행 가능성 조건에도 x를 먼저 정하고 u를 관측한 뒤 y를 조정하는 순서를 반영한다.

<math display="block" aria-label="The information structure of robust recourse"><mo>∃</mo><mi>x</mi><mo>∈</mo><mi>X</mi><mspace width=".5em"/><mo>∀</mo><mi>u</mi><mo>∈</mo><mi>U</mi><mspace width=".5em"/><mo>∃</mo><mi>y</mi><mo>(</mo><mi>u</mi><mo>)</mo><mo>≥</mo><mn>0</mn><mo>:</mo><mi>W</mi><mi>y</mi><mo>(</mo><mi>u</mi><mo>)</mo><mo>≥</mo><mi>h</mi><mo>−</mo><mi>T</mi><mi>x</mi><mo>−</mo><mi>M</mi><mi>u</mi></math>

모든 u에 같은 x를 사용하되 운전 결정은 시나리오별로 달라도 된다. y를 정할 때 필요한 불확실성이 이미 관측되었다는 가정이다. 정보를 일부만 관측하거나 순차적으로 관측한다면 그에 맞는 정보 제약을 더 넣어야 한다.

[Zeng과 Zhao(2013)](https://doi.org/10.1016/j.orl.2013.05.003)의 C&CG는 시나리오별 운전변수와 제약을 함께 생성한다. 공개된 [Zeng의 2011년 선행 원고](https://optimization-online.org/wp-content/uploads/2011/06/3065.pdf)에서도 유도를 확인할 수 있다.

### 일부 시나리오로 주문제를 구성한다

지금까지 찾은 시나리오의 인덱스를 S, 각 시나리오의 고정된 불확실성 값을 <math><msup><mi>u</mi><mi>s</mi></msup></math>라고 하자. 시나리오마다 독립된 운전변수 <math><msup><mi>y</mi><mi>s</mi></msup></math>를 둔다.

<math display="block" aria-label="The restricted column-and-constraint generation master"><mtable columnalign="left"><mtr><mtd><munder><mo>min</mo><mrow><mi>x</mi><mo>,</mo><mi>η</mi><mo>,</mo><mo>{</mo><msup><mi>y</mi><mi>s</mi></msup><mo>}</mo></mrow></munder><msup><mi>c</mi><mi>T</mi></msup><mi>x</mi><mo>+</mo><mi>η</mi></mtd></mtr><mtr><mtd><mi>x</mi><mo>∈</mo><mi>X</mi><mo>,</mo><mspace width=".5em"/><mi>η</mi><mo>≥</mo><munder><mi>η</mi><mo>_</mo></munder></mtd></mtr><mtr><mtd><mi>η</mi><mo>≥</mo><msup><mi>q</mi><mi>T</mi></msup><msup><mi>y</mi><mi>s</mi></msup><mo>,</mo><mspace width=".5em"/><mi>s</mi><mo>∈</mo><mi>S</mi></mtd></mtr><mtr><mtd><mi>W</mi><msup><mi>y</mi><mi>s</mi></msup><mo>≥</mo><mi>h</mi><mo>−</mo><mi>T</mi><mi>x</mi><mo>−</mo><mi>M</mi><msup><mi>u</mi><mi>s</mi></msup><mo>,</mo><mspace width=".5em"/><msup><mi>y</mi><mi>s</mi></msup><mo>≥</mo><mn>0</mn><mo>,</mo><mspace width=".5em"/><mi>s</mi><mo>∈</mo><mi>S</mi></mtd></mtr></mtable></math>

밑줄 친 η는 최악 운전비의 유효한 하한이다. 각 시나리오 블록은 설계변수 x를 공유하지만 운전변수는 따로 둔다. η는 저장된 모든 시나리오의 비용 이상이어야 하므로, 이를 최소화하면 저장된 시나리오 사이의 최대 비용을 표현한다. 기대비용을 다루는 모형에서는 시나리오 비용에 확률을 곱해 더한다.

이름의 column은 새로 넣는 운전변수 블록 <math><msup><mi>y</mi><mi>s</mi></msup></math>를 뜻한다. constraint는 그 변수에 대응하는 운전 제약과 비용 부등식이다. 반복할수록 주문제의 변수와 제약이 함께 늘어난다.

### 현재 시나리오 집합 밖을 검사한다

주문제를 푼 뒤 설계를 고정하고 U 전체에서 Q를 최대화하는 적대적 부문제를 푼다. 모든 시나리오에서 연속 운전 문제가 실행 가능하고 최적값이 유한하다면 강한 쌍대성을 적용해 내부 최소화를 쌍대 최대화로 바꾼다.

<math display="block" aria-label="The worst-case oracle after dualizing continuous recourse"><mi>Ψ</mi><mo>(</mo><msup><mi>x</mi><mi>k</mi></msup><mo>)</mo><mo>=</mo><munder><mo>max</mo><mrow><mi>u</mi><mo>∈</mo><mi>U</mi><mo>,</mo><mi>π</mi><mo>∈</mo><mi>Π</mi></mrow></munder><msup><mi>π</mi><mi>T</mi></msup><mo>(</mo><mi>h</mi><mo>−</mo><mi>T</mi><msup><mi>x</mi><mi>k</mi></msup><mo>−</mo><mi>M</mi><mi>u</mi><mo>)</mo></math>

u와 π의 곱이 들어가므로 일반적으로 쌍선형 최적화 문제다. 내부 LP를 쌍대화한 뒤에도 전역 최대화가 어려울 수 있다. 정확한 MILP 재정식화에는 적절한 불확실성 구조와 근거 있는 변수 경계가 필요하며 국소 NLP 해만으로 최댓값을 인증할 수는 없다.

정확한 oracle은 최악 시나리오와 그 비용을 반환한다. 그 시나리오의 운전변수·제약 블록을 주문제에 추가한다. 제한된 시나리오로 푼 주문제는 LB를 주고, U 전체에서 인증한 유한한 최악 비용은 UB를 준다.

<math display="block" aria-label="Bounds for column-and-constraint generation with exact solves"><mtable columnalign="left"><mtr><mtd><msub><mi>LB</mi><mi>k</mi></msub><mo>=</mo><msup><mi>c</mi><mi>T</mi></msup><msup><mi>x</mi><mi>k</mi></msup><mo>+</mo><msup><mi>η</mi><mi>k</mi></msup></mtd></mtr><mtr><mtd><msub><mi>UB</mi><mi>k</mi></msub><mo>=</mo><mo>min</mo><mo>{</mo><msub><mi>UB</mi><mrow><mi>k</mi><mo>−</mo><mn>1</mn></mrow></msub><mo>,</mo><msup><mi>c</mi><mi>T</mi></msup><msup><mi>x</mi><mi>k</mi></msup><mo>+</mo><mi>Ψ</mi><mo>(</mo><msup><mi>x</mi><mi>k</mi></msup><mo>)</mo><mo>}</mo></mtd></mtr></mtable></math>

운전이 불가능한 시나리오가 있으면 그 Q를 +무한대로 정의한다. 실행 가능성 oracle은 그런 시나리오를 찾거나 존재하지 않음을 인증해야 한다. 위반 시나리오의 블록을 넣고 주문제를 다시 풀되, 이 설계로 UB를 갱신하지는 않는다. 추가한 블록에서 운전이 가능해지도록 공유 설계 x가 바뀌어야 한다. 시나리오 블록을 추가하는 같은 방식으로 비용 과소평가와 실행 불가능성을 다룬다.

```text
유효한 운전비 하한과 작은 시나리오 집합 S를 정한다.
UB = +무한대로 둔다.
반복:
    주문제를 풀어 x, eta, LB를 얻는다.
    주문제의 실행 불가능성이 인증되면 원문제도 실행 불가능하다고 반환한다.
    전체 불확실성 집합에서 후속 운전의 실행 가능성을 검사한다.
    위반 시나리오를 찾으면:
        그 시나리오의 운전변수와 제약을 추가하고 반복한다.
    전체 집합에서 최악 운전비 문제를 푼다.
    인증한 최악 비용으로 UB와 저장된 최선 설계를 갱신한다.
    인증된 상하한 차이가 허용오차 이내면 최선 설계를 반환한다.
    최악 시나리오의 운전변수와 제약을 추가한다.
```

실행 가능성 검사와 비용 탐색을 하나의 oracle로 구현해도 된다. 유한한 UB를 계산하려면 모든 시나리오의 운전 가능성을 확인하고 최악 운전비의 상한을 인증해야 한다.

적대적 부문제에서 찾은 시나리오 하나의 비용만으로 최악 비용을 인증할 수는 없다. 최대화 문제에서 실행 가능한 시나리오 하나는 최댓값의 하한을 준다. 반면 oracle 최적값의 인증된 전역 상한을 얻고 모든 시나리오의 운전 가능성도 확인했다면 oracle을 정확히 풀기 전이라도 바깥 최소화 문제의 UB를 구성할 수 있다.

### 같은 공장에서 수요가 불확실해지면

Benders 예제의 비용과 용량 범위를 유지하되 수요를 6에서 10 사이로 바꾸자.

<math display="block" aria-label="The uncertain-demand production example"><mi>Q</mi><mo>(</mo><mi>x</mi><mo>,</mo><mi>d</mi><mo>)</mo><mo>=</mo><munder><mo>min</mo><mrow><mi>y</mi><mo>,</mo><mi>z</mi><mo>≥</mo><mn>0</mn></mrow></munder><mo>{</mo><mn>3</mn><mi>y</mi><mo>+</mo><mn>9</mn><mi>z</mi><mo>:</mo><mi>y</mi><mo>+</mo><mi>z</mi><mo>≥</mo><mi>d</mi><mo>,</mo><mi>y</mi><mo>≤</mo><mi>x</mi><mo>}</mo><mo>,</mo><mspace width=".5em"/><mi>d</mi><mo>∈</mo><mo>[</mo><mn>6</mn><mo>,</mo><mn>10</mn><mo>]</mo></math>

강건 목적함수는 2x와 이 구간의 최악 운전비를 더한 값이다. 처음에는 d = 6만 넣는다. 주문제는 용량 6, 운전비 18, 총비용 30을 선택한다. 그런데 이 설계에서 d = 10이면 자체 생산 6과 구매 4가 필요하다. 평가한 총비용은 12 + 18 + 36 = 66이다.

d = 10을 추가하면 기존 d = 6 블록 옆에 다음 블록이 생긴다.

<math display="block" aria-label="The newly generated scenario-ten variable and constraint block"><mtable columnalign="left"><mtr><mtd><msup><mi>y</mi><mn>10</mn></msup><mo>≥</mo><mn>0</mn><mo>,</mo><mspace width=".5em"/><msup><mi>z</mi><mn>10</mn></msup><mo>≥</mo><mn>0</mn></mtd></mtr><mtr><mtd><msup><mi>y</mi><mn>10</mn></msup><mo>+</mo><msup><mi>z</mi><mn>10</mn></msup><mo>≥</mo><mn>10</mn><mo>,</mo><mspace width=".5em"/><msup><mi>y</mi><mn>10</mn></msup><mo>≤</mo><mi>x</mi></mtd></mtr><mtr><mtd><mi>η</mi><mo>≥</mo><mn>3</mn><msup><mi>y</mi><mn>10</mn></msup><mo>+</mo><mn>9</mn><msup><mi>z</mi><mn>10</mn></msup></mtd></mtr></mtable></math>

위첨자 10은 수요 시나리오를 구분하는 표기이며 거듭제곱이 아니다. 두 수요 블록은 같은 용량 x를 쓰고, 생산량과 구매량은 각각 정한다.

| 항목 | 반복 1 | 반복 2 |
|---|---:|---:|
| 저장한 수요 | {6} | {6, 10} |
| 주문제 x | 6 | 10 |
| 주문제 η | 18 | 30 |
| LB | 30 | 50 |
| 최악 수요 | 10 | 10 |
| 최악 운전비 | 54 | 30 |
| 최선 UB | 66 | 50 |

이 예제에서는 수요가 늘수록 운전비가 줄지 않으므로 최악 수요가 항상 10이다. 용량 10, 총비용 50에서 종료한다. 여러 수요가 얽히거나 네트워크 제약, 예산형 불확실성이 들어가면 최악 시나리오 탐색은 훨씬 어려워질 수 있다.

## 3. 반복마다 남기는 정보의 차이

| 항목 | Benders | C&CG |
|---|---|---|
| 추가하는 정보 | 쌍대 비용 컷 또는 실행 가능성 컷 | 시나리오의 운전변수와 제약 |
| 운전변수 | 기본 주문제에서 소거 | 저장한 시나리오의 변수 유지 |
| 부문제 | 고정 설계의 후속 운전 | U 전체의 최악 비용 또는 실행 가능성 검사 |
| 주문제의 증가 | 부등식 | 변수와 부등식 |
| 주된 계산 부담 | 컷의 품질과 반복 풀이 | 커지는 주문제와 적대적 탐색 |

Benders 분해는 확률계획법에도 쓰이고 강건 최적화의 컷 생성법을 구성하는 데도 쓰인다. C&CG는 2단계 강건 문제를 푸는 한 가지 구성 방식이다. 불확실성이 있다는 사실만으로 알고리즘이 정해지지는 않는다.

연속 LP recourse에서는 두 방식의 연결을 수식으로 확인할 수 있다. d = 10 블록에서 운전변수를 소거하면 해당 시나리오의 비용함수 부등식이 남는다.

<math display="block" aria-label="Projecting one complete scenario block into the first-stage space"><mi>η</mi><mo>≥</mo><mi>Q</mi><mo>(</mo><mi>x</mi><mo>,</mo><mn>10</mn><mo>)</mo><mo>=</mo><mo>max</mo><mo>{</mo><mn>90</mn><mo>−</mo><mn>6</mn><mi>x</mi><mo>,</mo><mn>30</mn><mo>}</mo></math>

시나리오 블록 하나가 해당 운전비 함수의 두 아핀 조각을 모두 표현한다. Benders의 비용 컷은 쌍대해 하나에 대응하는 아핀 하한을 한 번에 하나씩 제공한다. C&CG는 선택한 시나리오의 비용함수 에피그래프를 확장 정식화로 유지하므로 주문제를 더 강하게 만들 수 있지만 변수도 늘어난다. 이 차이만으로 어느 방법이 항상 빠르다고 판단할 수는 없다.

불확실성 집합이 유한하면 실행 가능성과 최악 비용 탐색을 정확히 인증하는 C&CG에서 추가할 서로 다른 시나리오 블록도 유한하다. 연속 LP recourse에 W와 q가 고정되고 우변 불확실성 집합이 콤팩트한 다면체라면 실행 가능하고 유한한 Q는 u에 대해 볼록하다. 최댓값은 꼭짓점에서 달성되므로 꼭짓점을 반환하는 정확한 oracle을 쓰면 고려할 시나리오를 유한하게 줄일 수 있다. 유한 종료를 주장하려면 이 조건부터 확인해야 한다.

고전적 Benders도 다면체 LP 구조에서 필요한 쌍대 극점과 실행 가능성 ray가 유한하다. 통상적인 해 존재 조건과 정확한 풀이, 적절한 극점·ray 선택 아래 유한 종료를 논할 수 있다. x에 정수변수가 있어도 컷은 유효하지만 매 반복의 혼합정수 주문제 자체가 어려울 수 있다.

후속 운전에 정수변수가 들어가면 연속 LP 쌍대가 정확한 운전비를 표현하지 못한다. 고전적 Benders 컷만으로는 부족할 수 있고, 앞서 쓴 쌍대화 C&CG oracle도 더 이상 정확한 재정식화가 아니다. 시나리오 블록에는 정수 운전변수를 유지할 수 있지만 그에 맞는 정확한 oracle이 필요하다. Logic-based 또는 integer Benders, nested C&CG 같은 확장을 고려하되 각 방법의 조건을 따로 확인해야 한다. 비볼록 연속 운전 문제에서도 전역해 보장은 별도 근거가 필요하다.

공정 모형에서는 불확실성 관측 전에 고정할 결정과 관측 후 조정할 결정을 먼저 구분해야 한다. 이어 후속 운전변수의 연속성, 실행 가능성, 최종 상하한을 인증할 솔버 경계를 확인한다.

## 참고문헌

- J. F. Benders (1962). “Partitioning procedures for solving mixed-variables programming problems.” *Numerische Mathematik*, 4, 238–252. [DOI](https://doi.org/10.1007/BF01386316).
- Bo Zeng and Long Zhao (2013). “Solving two-stage robust optimization problems using a column-and-constraint generation method.” *Operations Research Letters*, 41(5), 457–461. [DOI](https://doi.org/10.1016/j.orl.2013.05.003).
- Bo Zeng (2011). “Solving Two-stage Robust Optimization Problems by A Constraint-and-Column Generation Method.” 기술보고서, 2011년 6월. [공개 원고](https://optimization-online.org/wp-content/uploads/2011/06/3065.pdf).
