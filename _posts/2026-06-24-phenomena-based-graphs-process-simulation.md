---
layout: post
title: "Phenomena-Based Graphs for Chemical Process Simulation"
title_ko: "화학공정 시뮬레이션을 위한 현상 기반 그래프"
date: 2026-06-24
category: graph-represented-methods
category_label: "Graph-Represented Methods"
research_group: algorithmic_reviews
research_category: graph-represented-methods
research_category_label: "Graph-Represented Methods"
application_category: ""
application_category_label: ""
method_category: graph-represented-methods
method_category_label: "Graph-Represented Methods"
paper_title: "Phenomena-based graph representations and applications to chemical process simulation"
authors: "Cortés-Peña, Y. R.; Zavala, V. M."
venue: "Computers & Chemical Engineering, 213, Article 109756"
year: "2026"
doi: "10.1016/j.compchemeng.2026.109756"
arxiv: ""
source_url: "https://doi.org/10.1016/j.compchemeng.2026.109756"
tags:
  - "chemical-process-simulation"
  - "graph-representations"
  - "phenomena-based-decomposition"
  - "flowsheet-simulation"
  - "process-systems-engineering"
excerpt: "A note on Cortés-Peña and Zavala's phenomena-based graph representation for flowsheet simulation, where nonlinear thermodynamic blocks are separated from process-wide linear material and energy balance solves."
excerpt_ko: "Cortés-Peña와 Zavala의 현상 기반 그래프 표현을 정리한다. 핵심은 비선형 열역학 블록과 전 공정 수준의 선형 물질수지 및 에너지수지 풀이를 분리하는 것이다."
language: "en-ko"
has_korean_note: false
---

## When Process Simulation Is Needed

Chemical process simulation is needed when we want to know how a process will behave before building it, changing it, or optimizing it. A simulator predicts stream flows, compositions, temperatures, phase splits, heat duties, recycle rates, reaction conversions, and equipment loads from a proposed flowsheet and operating condition.

This is useful in process design, retrofit studies, plant operation, control, safety analysis, techno-economic analysis, uncertainty analysis, and optimization. For example, one may need to compare alternative separation trains, estimate the energy demand of a solvent recovery system, check whether an ammonia synthesis loop closes under recycle, or evaluate thousands of operating points inside a design optimization.

In simple cases, simulation is almost routine. In realistic flowsheets, it becomes a numerical problem. Reaction, separation, phase equilibrium, recycle, and heat integration can make one part of the plant depend on another part several units away.

## Why Existing Simulation Methods Become Difficult

Sequential modular simulation handles a flowsheet by solving unit operations one by one and iterating on tear streams. This is robust and easy to implement, but information travels slowly around recycle loops. If a composition error appears in a downstream separator, it may need several passes through the process before the upstream units feel the correction.

Equation-oriented simulation puts all equations into one large nonlinear system and solves them together. This can be fast when the initialization, scaling, and sparsity structure are favorable. It can also be fragile. Strong nonideality, phase-regime switching, badly scaled equations, and poor initial guesses can make the nonlinear solve difficult.

Specialized decompositions such as MESH methods work well inside particular unit operations, especially distillation columns, because they separate material, equilibrium, summation, and enthalpy relations. But they are usually tied to a specific unit-operation structure. They do not automatically say how to coordinate material and energy balances across an entire flowsheet with recycle, reaction, separation, and phase splitting.

This is the gap that motivates the paper. Existing methods either respect equipment boundaries and may pass information slowly, or solve everything together and may become numerically delicate. Cortés-Peña and Zavala ask whether the equations can be reorganized by physical phenomena instead, so that process-wide material and energy balances are coordinated more directly.

## What Problem Is Being Solved?

Steady-state flowsheet simulation is often presented as a sequence of unit operations: mixer, reactor, column, settler, heat exchanger, recycle loop. That view is natural for engineers because it follows the process flow diagram. It is also convenient for software, because each unit operation can be treated as a module with a defined inlet and outlet interface.

Numerically, however, the unit-operation boundary is not always the most useful decomposition boundary. The nonlinear coupling in a chemical process is often created by physical phenomena that cut across units: material balances, energy balances, vapor-liquid equilibrium, liquid-liquid equilibrium, reaction generation, phase splitting, enthalpy relations, and separation factors. A recycle loop can make this coupling process-wide.

In equation form, the flowsheet simulator is trying to solve a large nonlinear system:

<math display="block" aria-label="Steady-state nonlinear flowsheet equations">
  <mi>F</mi><mo>(</mo><mi>x</mi><mo>)</mo><mo>=</mo><mn>0</mn><mo>,</mo>
</math>

where <math><mi>x</mi></math> includes stream flows, compositions, temperatures, phase fractions, heat duties, reaction extents, and other state variables. A small composition change can perturb activity coefficients, which perturb phase splits, which perturb flow rates, which perturb enthalpies, which perturb temperatures, which again perturb compositions.

The question in Cortés-Peña and Zavala (2026) is therefore not just how to draw a better graph. The question is sharper: can a MESH-like physical decomposition be lifted from specific unit operations, such as distillation columns, to the whole flowsheet?

That question is useful because the traditional sequential modular approach decomposes the process by equipment boundaries, while the numerical coupling is often determined by physical laws.

## The Graph Is Equation-Variable, Not Just Unit-Stream

A standard flowsheet graph uses units as nodes and streams as edges. That is a graph of equipment connectivity. The paper instead uses an equation-variable bipartite graph. Variable nodes represent objects such as component flow rates, temperatures, partition coefficients, phase ratios, reaction generation, and separation variables. Equation nodes represent material balances, energy balances, VLE relations, LLE relations, reaction relations, and shortcut separation equations.

The edge rule is simple: a variable is connected to an equation if the equation depends on that variable.

This matters because the graph is not mainly a visualization device. It is a way to expose which variables are coupled through which physical phenomena. Once that structure is explicit, the solver update order can be redesigned.

The resulting decomposition can be summarized as:

1. Evaluate local nonlinear phenomena: VLE, LLE, reaction, shortcut separation, thermodynamic sensitivities.
2. Hold those nonlinear coefficients fixed.
3. Solve a process-wide linear energy balance system.
4. Solve a process-wide linear material balance system.
5. Repeat until the outer fixed-point iteration converges.

This is closer to successive linearization or nonlinear block Gauss-Seidel than to a full Newton solve. The nonlinearities have not disappeared. They have been moved into an outer iteration.

## Why the Material Balance Becomes Linear

For a component <math><mi>c</mi></math>, a local material balance can be written schematically as:

<math display="block" aria-label="Component material balance">
  <munder><mo>&sum;</mo><mi>o</mi></munder>
  <msub><mi>x</mi><mrow><mi>F</mi><mo>,</mo><mi>c</mi><mo>,</mo><mi>o</mi></mrow></msub>
  <mo>-</mo>
  <munder><mo>&sum;</mo><mi>i</mi></munder>
  <msub><mi>x</mi><mrow><mi>F</mi><mo>,</mo><mi>c</mi><mo>,</mo><mi>i</mi></mrow></msub>
  <mo>=</mo>
  <msub><mi>x</mi><mrow><mi>R</mi><mo>,</mo><mi>c</mi></mrow></msub><mo>.</mo>
</math>

The reaction generation term <math><msub><mi>x</mi><mrow><mi>R</mi><mo>,</mo><mi>c</mi></mrow></msub></math> is generally nonlinear because it depends on local state. In a phase split, a separation relation may also depend on a separation factor:

<math display="block" aria-label="Separation factor relation">
  <msub><mi>x</mi><mrow><mi>S</mi><mo>,</mo><mi>c</mi></mrow></msub>
  <mo>=</mo>
  <msub><mi>x</mi><mrow><mi>K</mi><mo>,</mo><mi>c</mi></mrow></msub>
  <msub><mi>x</mi><mi>&Phi;</mi></msub><mo>.</mo>
</math>

The partition coefficient <math><msub><mi>x</mi><mrow><mi>K</mi><mo>,</mo><mi>c</mi></mrow></msub></math> and phase ratio <math><msub><mi>x</mi><mi>&Phi;</mi></msub></math> depend on composition and temperature, so the original model remains nonlinear.

The trick is conditional linearity. At outer iteration <math><mi>k</mi></math>, suppose the nonlinear quantities have already been evaluated:

<math display="block" aria-label="Fixed nonlinear coefficients">
  <msubsup><mi>x</mi><mi>K</mi><mrow><mo>(</mo><mi>k</mi><mo>)</mo></mrow></msubsup>
  <mo>,</mo>
  <msubsup><mi>x</mi><mi>&Phi;</mi><mrow><mo>(</mo><mi>k</mi><mo>)</mo></mrow></msubsup>
  <mo>,</mo>
  <msubsup><mi>x</mi><mi>R</mi><mrow><mo>(</mo><mi>k</mi><mo>)</mo></mrow></msubsup>
  <mtext> fixed</mtext><mo>.</mo>
</math>

Then the process-wide material balance can be assembled as a linear system:

<math display="block" aria-label="Linear material balance system">
  <msubsup><mi>A</mi><mi>F</mi><mrow><mo>(</mo><mi>k</mi><mo>)</mo></mrow></msubsup>
  <msubsup><mi>x</mi><mi>F</mi><mrow><mo>(</mo><mi>k</mi><mo>+</mo><mn>1</mn><mo>)</mo></mrow></msubsup>
  <mo>=</mo>
  <msubsup><mi>b</mi><mi>F</mi><mrow><mo>(</mo><mi>k</mi><mo>)</mo></mrow></msubsup><mo>.</mo>
</math>

This is the computational center of the paper. The method does not make thermodynamics linear. It temporarily freezes thermodynamic and reaction coefficients, then solves the global balance problem implied by those coefficients.

## The Energy Balance Has the Same Flavor

Energy balances are nonlinear because enthalpy depends on flow, temperature, composition, and phase. The paper chooses a key energy variable <math><msub><mi>x</mi><mi>E</mi></msub></math> for each stage. In a single-phase stream this may be temperature; in a VLE stage it may be a phase-ratio variable.

Near the current iterate, enthalpy can be locally linearized:

<math display="block" aria-label="Local enthalpy linearization">
  <mi>H</mi><mo>(</mo><msub><mi>x</mi><mi>E</mi></msub><mo>+</mo><mi>&Delta;</mi><msub><mi>x</mi><mi>E</mi></msub><mo>)</mo>
  <mo>&approx;</mo>
  <mi>H</mi><mo>(</mo><msub><mi>x</mi><mi>E</mi></msub><mo>)</mo>
  <mo>+</mo>
  <mfrac><mrow><mo>&part;</mo><mi>H</mi></mrow><mrow><mo>&part;</mo><msub><mi>x</mi><mi>E</mi></msub></mrow></mfrac>
  <mi>&Delta;</mi><msub><mi>x</mi><mi>E</mi></msub><mo>.</mo>
</math>

With the enthalpy sensitivities fixed, the energy balance also becomes a process-wide linear system:

<math display="block" aria-label="Linear energy balance system">
  <msubsup><mi>A</mi><mi>E</mi><mrow><mo>(</mo><mi>k</mi><mo>)</mo></mrow></msubsup>
  <msubsup><mi>x</mi><mi>E</mi><mrow><mo>(</mo><mi>k</mi><mo>+</mo><mn>1</mn><mo>)</mo></mrow></msubsup>
  <mo>=</mo>
  <msubsup><mi>b</mi><mi>E</mi><mrow><mo>(</mo><mi>k</mi><mo>)</mo></mrow></msubsup><mo>.</mo>
</math>

The intuition is concrete. Instead of letting temperature information crawl through unit operations around a recycle loop, the method computes local energy sensitivities and then adjusts the process-wide energy balance in one global solve.

## Why This Can Be Faster

Consider a minimal recycle relation:

<math display="block" aria-label="Two-stream recycle relation">
  <msub><mi>F</mi><mn>1</mn></msub>
  <mo>=</mo>
  <mi>q</mi><mo>+</mo><mi>&alpha;</mi><msub><mi>F</mi><mn>2</mn></msub>
  <mo>,</mo>
  <mspace width="1em"></mspace>
  <msub><mi>F</mi><mn>2</mn></msub>
  <mo>=</mo>
  <mi>&beta;</mi><msub><mi>F</mi><mn>1</mn></msub><mo>.</mo>
</math>

A sequential modular update propagates information around the loop. Its local convergence speed is governed by the recycle gain, roughly <math><mo>|</mo><mi>&alpha;</mi><mi>&beta;</mi><mo>|</mo></math>. If that product is close to one, convergence is slow.

If <math><mi>&alpha;</mi></math> and <math><mi>&beta;</mi></math> are fixed at the current outer iteration, the phenomena-based method instead solves the coupled linear system directly:

<math display="block" aria-label="Coupled recycle linear system">
  <mfenced open="[" close="]">
    <mtable>
      <mtr><mtd><mn>1</mn></mtd><mtd><mo>-</mo><mi>&alpha;</mi></mtd></mtr>
      <mtr><mtd><mo>-</mo><mi>&beta;</mi></mtd><mtd><mn>1</mn></mtd></mtr>
    </mtable>
  </mfenced>
  <mfenced open="[" close="]">
    <mtable>
      <mtr><mtd><msub><mi>F</mi><mn>1</mn></msub></mtd></mtr>
      <mtr><mtd><msub><mi>F</mi><mn>2</mn></msub></mtd></mtr>
    </mtable>
  </mfenced>
  <mo>=</mo>
  <mfenced open="[" close="]">
    <mtable>
      <mtr><mtd><mi>q</mi></mtd></mtr>
      <mtr><mtd><mn>0</mn></mtd></mtr>
    </mtable>
  </mfenced><mo>.</mo>
</math>

So, under fixed thermodynamic or separation coefficients, the recycle closure is handled at once. This explains why the approach can be fast for ideal or weakly coupled separation systems.

The important phrase is "under fixed coefficients." If the coefficients change violently when the flows change, the outer iteration can oscillate.

## Where It Fails

The paper is useful because it does not claim a universal convergence breakthrough. It reports cases where the phenomena-based method is faster, and cases where it is worse or fails.

The simplified acetic acid dewatering example under ideal-mixture assumptions is favorable. The thermodynamic coefficients and phase split relations vary smoothly enough that the global balance solve helps. The method can close recycle errors faster than sequential modular simulation.

The nonideal acetic acid system is different. With stronger liquid-liquid equilibrium effects, the settler can switch between one liquid phase and two liquid phases. That is a nonsmooth regime change, not a gentle coefficient update. The outer fixed-point map can become unstable, and the proposed method may fail to converge. Sequential modular simulation is slower, but more stable in this setting.

The butanol separation and Haber-Bosch examples also temper the story. If the flowsheet is small, if LLE-column coupling is strong, or if sequential modular simulation already converges in a few iterations, the overhead of global linear solves can exceed the benefit.

So the paper's message is not "phenomena-based is always better." It is closer to this: process-wide balance coordination is valuable when local nonlinear coefficients are not too sensitive to the global balance variables.

## What Is Guaranteed?

There is a limited but real structural guarantee. If the nonlinear coefficients are fixed at the current iteration, and if the assembled balance matrices are nonsingular, then the material and energy subproblems are linear systems:

<math display="block" aria-label="Linear subproblem guarantee">
  <msub><mi>A</mi><mi>F</mi></msub><msub><mi>x</mi><mi>F</mi></msub>
  <mo>=</mo>
  <msub><mi>b</mi><mi>F</mi></msub>
  <mo>,</mo>
  <mspace width="1em"></mspace>
  <msub><mi>A</mi><mi>E</mi></msub><msub><mi>x</mi><mi>E</mi></msub>
  <mo>=</mo>
  <msub><mi>b</mi><mi>E</mi></msub><mo>.</mo>
</math>

Those subproblems can be solved exactly up to numerical linear algebra error. Also, if the outer iteration reaches a fixed point and the local phenomenon equations are satisfied consistently, the decomposed model should correspond to a solution of the original steady-state equations.

But several stronger statements are not guaranteed. The paper does not prove convergence from arbitrary initial points. It does not prove that the method is always faster than sequential modular simulation. It does not prove a larger basin of attraction. It also does not benchmark directly against a full equation-oriented method.

The local convergence risk can be described by a fixed-point map:

<math display="block" aria-label="Outer fixed point map">
  <msup><mi>z</mi><mrow><mo>(</mo><mi>k</mi><mo>+</mo><mn>1</mn><mo>)</mo></mrow></msup>
  <mo>=</mo>
  <mi>T</mi><mo>(</mo><msup><mi>z</mi><mrow><mo>(</mo><mi>k</mi><mo>)</mo></mrow></msup><mo>)</mo><mo>.</mo>
</math>

Convergence usually requires the spectral radius of the local Jacobian to be less than one:

<math display="block" aria-label="Local fixed point convergence condition">
  <mi>&rho;</mi>
  <mo>(</mo>
  <msub>
    <mfrac><mrow><mo>&part;</mo><mi>T</mi></mrow><mrow><mo>&part;</mo><mi>z</mi></mrow></mfrac>
    <msup><mi>z</mi><mo>*</mo></msup>
  </msub>
  <mo>)</mo>
  <mo>&lt;</mo>
  <mn>1</mn><mo>.</mo>
</math>

That Jacobian is dangerous when thermodynamic coefficients are highly sensitive to composition or temperature, when phase regimes switch, or when the global balance matrices are ill-conditioned. The graph representation makes the coupling legible. It does not make the coupling benign.

## How To Read The Novelty

The strongest contribution is not a new graph-theoretic convergence result. It is an architecture for compiling a chemical process model into local nonlinear phenomenon blocks and process-wide linear balance blocks.

In that sense, the paper generalizes a familiar idea:

unit-level physical decomposition becomes process-wide balance coordination.

The graph is the language used to express and implement the decomposition, including the BioSTEAM implementation. It helps organize variables, equations, and update order. It is not yet an automatic algorithm for discovering the optimal decomposition. A process engineer still needs to decide which variables belong in local nonlinear blocks and which balances should be coordinated globally.

This is why the work belongs in graph-represented methods, but with a different flavor from graph neural networks. The graph is not used to learn a policy or predict a value. It is used to represent a solver structure.

## Final Assessment

Cortés-Peña and Zavala's paper is best read as a careful solver-architecture paper. It shows that unit-operation decomposition is not the only natural way to simulate chemical processes. By freezing local nonlinear phenomenon coefficients and solving material and energy balances over the whole flowsheet, the method can close weakly coupled recycle structures faster.

The limitation is equally important. The graph representation does not by itself create a convergence guarantee. Stability depends on how strongly flows, compositions, temperatures, thermodynamic coefficients, phase regimes, and global balance matrices feed back into one another.

So the fair summary is narrow and useful: this is a process-wide generalization of MESH-type physical decomposition, implemented through an equation-variable graph. It is promising when coupling is weak and smooth. It is fragile when phase-equilibrium coupling is strong or nonsmooth.

## Reference

Cortés-Peña, Y. R., & Zavala, V. M. (2026). Phenomena-based graph representations and applications to chemical process simulation. *Computers & Chemical Engineering, 213*, Article 109756. [https://doi.org/10.1016/j.compchemeng.2026.109756](https://doi.org/10.1016/j.compchemeng.2026.109756)

<!-- ko -->

## 공정 시뮬레이션은 언제 필요한가

화학공정 시뮬레이션은 공정을 실제로 만들거나, 바꾸거나, 최적화하기 전에 그 공정이 어떻게 거동할지 알고 싶을 때 필요하다. Simulator는 주어진 flowsheet와 operating condition에서 stream flow, composition, temperature, phase split, heat duty, recycle rate, reaction conversion, equipment load 등을 예측한다.

이것은 process design, retrofit study, plant operation, control, safety analysis, techno-economic analysis, uncertainty analysis, optimization에서 필요하다. 예를 들어 여러 separation train을 비교하거나, solvent recovery system의 energy demand를 추정하거나, ammonia synthesis loop가 recycle 아래에서 닫히는지 확인하거나, design optimization 안에서 수천 개 operating point를 평가해야 할 수 있다.

단순한 경우에는 시뮬레이션이 거의 routine하다. 하지만 실제 flowsheet에서는 이것이 수치해석 문제가 된다. 반응, 분리, phase equilibrium, recycle, heat integration 때문에 한 장치의 상태가 몇 개 장치 떨어진 다른 부분의 상태와 연결될 수 있다.

## 기존 시뮬레이션 방법은 왜 어려워지는가

Sequential modular simulation은 flowsheet를 unit operation 순서대로 풀고 tear stream을 반복한다. 이 방식은 robust하고 구현이 쉽다. 하지만 정보가 recycle loop를 따라 천천히 이동한다. Downstream separator에서 생긴 composition error가 upstream unit에 반영되려면 공정을 여러 번 돌아야 할 수 있다.

Equation-oriented simulation은 모든 방정식을 하나의 큰 nonlinear system으로 묶어 한꺼번에 푼다. 초기값, scaling, sparsity structure가 좋으면 빠를 수 있다. 하지만 강한 비이상성, phase-regime switching, 나쁜 scaling, poor initial guess가 있으면 nonlinear solve가 민감해진다.

MESH 같은 specialized decomposition은 특정 unit operation 안에서는 잘 작동한다. 특히 distillation column에서 material, equilibrium, summation, enthalpy relation을 나누는 것은 효과적이다. 그러나 이런 방법은 보통 특정 장치 구조에 묶여 있다. Recycle, reaction, separation, phase split이 섞인 전체 flowsheet에서 material balance와 energy balance를 어떻게 조정할지는 자동으로 말해주지 않는다.

이 지점이 논문의 출발점이다. 기존 방법은 장치 경계를 잘 존중하지만 정보 전달이 느릴 수 있고, 또는 모든 것을 한꺼번에 풀지만 수치적으로 민감해질 수 있다. Cortés-Peña and Zavala는 방정식을 장치가 아니라 물리 현상별로 재조직하면 전 공정 수준의 material balance와 energy balance를 더 직접적으로 조정할 수 있는지 묻는다.

## 어떤 문제를 풀려는가

정상상태 flowsheet simulation은 흔히 unit operation의 순서로 설명된다. Mixer, reactor, column, settler, heat exchanger, recycle loop를 따라가면 공정 흐름도가 된다. 이 관점은 공정 엔지니어에게 자연스럽고, 소프트웨어 구현에도 편하다. 각 장치를 하나의 module로 두고 inlet과 outlet interface만 맞추면 되기 때문이다.

하지만 수치해석 관점에서 unit-operation boundary가 항상 가장 좋은 분해 경계인 것은 아니다. 화학공정의 비선형 coupling은 장치 자체보다 물리 현상에서 생기는 경우가 많다. 물질수지, 에너지수지, VLE, LLE, 반응, phase split, enthalpy relation, separation factor가 서로 얽히고, recycle이 있으면 이 coupling이 공정 전체를 순환한다.

방정식으로 쓰면 flowsheet simulator는 큰 비선형 시스템을 푸는 문제다.

<math display="block" aria-label="Steady-state nonlinear flowsheet equations Korean">
  <mi>F</mi><mo>(</mo><mi>x</mi><mo>)</mo><mo>=</mo><mn>0</mn><mo>,</mo>
</math>

여기서 <math><mi>x</mi></math>에는 stream flow, composition, temperature, phase fraction, heat duty, reaction extent 등이 들어간다. 작은 조성 변화가 activity coefficient를 바꾸고, 이것이 phase split을 바꾸고, flow rate를 바꾸고, enthalpy를 바꾸고, temperature를 바꾸고, 다시 composition을 바꿀 수 있다.

Cortés-Peña and Zavala (2026)의 질문은 단순히 더 좋은 graph를 그리는 것이 아니다. 질문은 더 구체적이다. Distillation column 같은 특정 장치 내부에서 쓰이던 MESH식 물리 분해를 전체 flowsheet 수준으로 올릴 수 있는가?

이 질문은 의미가 있다. Traditional sequential modular approach는 장치 경계를 기준으로 공정을 나누지만, 실제 numerical coupling은 물리 법칙이 만드는 경우가 많기 때문이다.

## Graph는 Unit-Stream Graph가 아니라 Equation-Variable Graph다

일반적인 flowsheet graph에서는 unit이 node이고 stream이 edge다. 이것은 장치 연결성의 graph다. 이 논문은 대신 equation-variable bipartite graph를 쓴다. Variable node는 component flow rate, temperature, partition coefficient, phase ratio, reaction generation, separation variable 같은 항목을 나타낸다. Equation node는 material balance, energy balance, VLE, LLE, reaction relation, shortcut separation equation을 나타낸다.

Edge rule은 단순하다. 어떤 equation이 어떤 variable에 의존하면 둘 사이에 edge가 있다.

이 점이 중요하다. Graph의 목적은 주로 시각화가 아니다. 어떤 변수가 어떤 물리 현상을 통해 coupling되는지 드러내는 것이다. 그 구조가 명시되면 solver update order를 다시 설계할 수 있다.

전체 decomposition은 다음처럼 요약할 수 있다.

1. VLE, LLE, reaction, shortcut separation, thermodynamic sensitivity 같은 local nonlinear phenomena를 계산한다.
2. 이 nonlinear coefficient들을 고정한다.
3. 전 공정 수준의 linear energy balance system을 푼다.
4. 전 공정 수준의 linear material balance system을 푼다.
5. Outer fixed-point iteration이 수렴할 때까지 반복한다.

이것은 full Newton solve라기보다 successive linearization 또는 nonlinear block Gauss-Seidel에 가깝다. 비선형성이 사라진 것이 아니다. Outer iteration 바깥으로 밀려난 것이다.

## 왜 Material Balance가 Linear해지는가

Component <math><mi>c</mi></math>에 대한 local material balance는 개략적으로 다음처럼 쓸 수 있다.

<math display="block" aria-label="Component material balance Korean">
  <munder><mo>&sum;</mo><mi>o</mi></munder>
  <msub><mi>x</mi><mrow><mi>F</mi><mo>,</mo><mi>c</mi><mo>,</mo><mi>o</mi></mrow></msub>
  <mo>-</mo>
  <munder><mo>&sum;</mo><mi>i</mi></munder>
  <msub><mi>x</mi><mrow><mi>F</mi><mo>,</mo><mi>c</mi><mo>,</mo><mi>i</mi></mrow></msub>
  <mo>=</mo>
  <msub><mi>x</mi><mrow><mi>R</mi><mo>,</mo><mi>c</mi></mrow></msub><mo>.</mo>
</math>

Reaction generation term <math><msub><mi>x</mi><mrow><mi>R</mi><mo>,</mo><mi>c</mi></mrow></msub></math>는 local state에 의존하므로 일반적으로 비선형이다. Phase split이 있으면 separation factor도 들어간다.

<math display="block" aria-label="Separation factor relation Korean">
  <msub><mi>x</mi><mrow><mi>S</mi><mo>,</mo><mi>c</mi></mrow></msub>
  <mo>=</mo>
  <msub><mi>x</mi><mrow><mi>K</mi><mo>,</mo><mi>c</mi></mrow></msub>
  <msub><mi>x</mi><mi>&Phi;</mi></msub><mo>.</mo>
</math>

Partition coefficient <math><msub><mi>x</mi><mrow><mi>K</mi><mo>,</mo><mi>c</mi></mrow></msub></math>와 phase ratio <math><msub><mi>x</mi><mi>&Phi;</mi></msub></math>는 조성과 온도에 의존한다. 따라서 원래 모델은 여전히 비선형이다.

핵심은 conditional linearity다. Outer iteration <math><mi>k</mi></math>에서 nonlinear quantity들이 이미 계산되었다고 하자.

<math display="block" aria-label="Fixed nonlinear coefficients Korean">
  <msubsup><mi>x</mi><mi>K</mi><mrow><mo>(</mo><mi>k</mi><mo>)</mo></mrow></msubsup>
  <mo>,</mo>
  <msubsup><mi>x</mi><mi>&Phi;</mi><mrow><mo>(</mo><mi>k</mi><mo>)</mo></mrow></msubsup>
  <mo>,</mo>
  <msubsup><mi>x</mi><mi>R</mi><mrow><mo>(</mo><mi>k</mi><mo>)</mo></mrow></msubsup>
  <mtext> fixed</mtext><mo>.</mo>
</math>

그러면 전 공정 수준의 material balance는 다음 선형 시스템으로 조립된다.

<math display="block" aria-label="Linear material balance system Korean">
  <msubsup><mi>A</mi><mi>F</mi><mrow><mo>(</mo><mi>k</mi><mo>)</mo></mrow></msubsup>
  <msubsup><mi>x</mi><mi>F</mi><mrow><mo>(</mo><mi>k</mi><mo>+</mo><mn>1</mn><mo>)</mo></mrow></msubsup>
  <mo>=</mo>
  <msubsup><mi>b</mi><mi>F</mi><mrow><mo>(</mo><mi>k</mi><mo>)</mo></mrow></msubsup><mo>.</mo>
</math>

이것이 논문의 계산적 중심이다. 이 방법은 thermodynamics를 linear하게 만든 것이 아니다. Thermodynamic coefficient와 reaction coefficient를 잠시 고정한 뒤, 그 coefficient가 의미하는 global balance problem을 푼다.

## Energy Balance도 같은 구조다

Energy balance는 enthalpy가 flow, temperature, composition, phase에 의존하기 때문에 비선형이다. 논문은 각 stage마다 key energy variable <math><msub><mi>x</mi><mi>E</mi></msub></math>를 선택한다. Single-phase stream에서는 temperature일 수 있고, VLE stage에서는 phase-ratio variable일 수 있다.

현재 iterate 근방에서는 enthalpy를 local linearization할 수 있다.

<math display="block" aria-label="Local enthalpy linearization Korean">
  <mi>H</mi><mo>(</mo><msub><mi>x</mi><mi>E</mi></msub><mo>+</mo><mi>&Delta;</mi><msub><mi>x</mi><mi>E</mi></msub><mo>)</mo>
  <mo>&approx;</mo>
  <mi>H</mi><mo>(</mo><msub><mi>x</mi><mi>E</mi></msub><mo>)</mo>
  <mo>+</mo>
  <mfrac><mrow><mo>&part;</mo><mi>H</mi></mrow><mrow><mo>&part;</mo><msub><mi>x</mi><mi>E</mi></msub></mrow></mfrac>
  <mi>&Delta;</mi><msub><mi>x</mi><mi>E</mi></msub><mo>.</mo>
</math>

Enthalpy sensitivity를 고정하면 energy balance도 전 공정 수준의 선형 시스템이 된다.

<math display="block" aria-label="Linear energy balance system Korean">
  <msubsup><mi>A</mi><mi>E</mi><mrow><mo>(</mo><mi>k</mi><mo>)</mo></mrow></msubsup>
  <msubsup><mi>x</mi><mi>E</mi><mrow><mo>(</mo><mi>k</mi><mo>+</mo><mn>1</mn><mo>)</mo></mrow></msubsup>
  <mo>=</mo>
  <msubsup><mi>b</mi><mi>E</mi><mrow><mo>(</mo><mi>k</mi><mo>)</mo></mrow></msubsup><mo>.</mo>
</math>

직관은 분명하다. Temperature 정보가 unit operation을 따라 recycle loop를 한 바퀴 돌 때까지 기다리는 대신, local energy sensitivity를 계산한 뒤 전 공정 energy balance를 global solve로 한 번에 조정한다.

## 왜 빨라질 수 있는가

가장 단순한 recycle relation을 생각해 보자.

<math display="block" aria-label="Two-stream recycle relation Korean">
  <msub><mi>F</mi><mn>1</mn></msub>
  <mo>=</mo>
  <mi>q</mi><mo>+</mo><mi>&alpha;</mi><msub><mi>F</mi><mn>2</mn></msub>
  <mo>,</mo>
  <mspace width="1em"></mspace>
  <msub><mi>F</mi><mn>2</mn></msub>
  <mo>=</mo>
  <mi>&beta;</mi><msub><mi>F</mi><mn>1</mn></msub><mo>.</mo>
</math>

Sequential modular update는 정보를 loop를 따라 전달한다. Local convergence speed는 대략 recycle gain인 <math><mo>|</mo><mi>&alpha;</mi><mi>&beta;</mi><mo>|</mo></math>에 의해 좌우된다. 이 값이 1에 가까우면 수렴이 느리다.

반대로 <math><mi>&alpha;</mi></math>와 <math><mi>&beta;</mi></math>가 현재 outer iteration에서 고정되어 있다면, phenomena-based method는 coupled linear system을 직접 푼다.

<math display="block" aria-label="Coupled recycle linear system Korean">
  <mfenced open="[" close="]">
    <mtable>
      <mtr><mtd><mn>1</mn></mtd><mtd><mo>-</mo><mi>&alpha;</mi></mtd></mtr>
      <mtr><mtd><mo>-</mo><mi>&beta;</mi></mtd><mtd><mn>1</mn></mtd></mtr>
    </mtable>
  </mfenced>
  <mfenced open="[" close="]">
    <mtable>
      <mtr><mtd><msub><mi>F</mi><mn>1</mn></msub></mtd></mtr>
      <mtr><mtd><msub><mi>F</mi><mn>2</mn></msub></mtd></mtr>
    </mtable>
  </mfenced>
  <mo>=</mo>
  <mfenced open="[" close="]">
    <mtable>
      <mtr><mtd><mi>q</mi></mtd></mtr>
      <mtr><mtd><mn>0</mn></mtd></mtr>
    </mtable>
  </mfenced><mo>.</mo>
</math>

따라서 fixed thermodynamic 또는 separation coefficients 아래에서는 recycle closure를 한 번에 처리한다. 이것이 ideal 또는 weakly coupled separation system에서 이 접근이 빨라질 수 있는 이유다.

중요한 표현은 "fixed coefficients 아래에서"다. Flow가 바뀔 때 coefficient가 급격하게 변하면 outer iteration은 쉽게 진동할 수 있다.

## 어디서 실패하는가

이 논문이 유용한 이유는 보편적 convergence breakthrough를 주장하지 않는다는 데 있다. Phenomena-based method가 빠른 case도 보여주고, 더 나쁘거나 실패하는 case도 보여준다.

Ideal-mixture assumption을 둔 simplified acetic acid dewatering 예제는 유리하다. Thermodynamic coefficient와 phase split relation이 충분히 매끄럽게 변하므로 global balance solve의 이점이 살아난다. Sequential modular simulation보다 recycle error를 더 빨리 닫을 수 있다.

Nonideal acetic acid system은 다르다. Liquid-liquid equilibrium 효과가 강해지면 settler에서 one liquid phase와 two liquid phases가 나타났다 사라지는 switching이 생긴다. 이것은 부드러운 coefficient update가 아니라 nonsmooth regime change다. Outer fixed-point map이 불안정해질 수 있고, 제안법이 수렴하지 못할 수 있다. Sequential modular simulation은 느리지만 이 상황에서는 더 안정적이다.

Butanol separation과 Haber-Bosch 예제도 claim을 줄여 읽게 만든다. Flowsheet가 작거나, LLE-column coupling이 강하거나, sequential modular simulation이 이미 몇 iteration 안에 수렴한다면 global linear solve의 overhead가 이득보다 클 수 있다.

따라서 논문의 메시지는 "phenomena-based가 항상 더 좋다"가 아니다. 더 정확히는 local nonlinear coefficient가 global balance variable에 너무 민감하지 않을 때 process-wide balance coordination이 효과적이라는 것이다.

## 무엇이 보장되는가

제한적이지만 실제적인 구조적 보장은 있다. 현재 iteration에서 nonlinear coefficient가 고정되어 있고, 조립된 balance matrix가 nonsingular라면 material 및 energy subproblem은 선형 시스템이다.

<math display="block" aria-label="Linear subproblem guarantee Korean">
  <msub><mi>A</mi><mi>F</mi></msub><msub><mi>x</mi><mi>F</mi></msub>
  <mo>=</mo>
  <msub><mi>b</mi><mi>F</mi></msub>
  <mo>,</mo>
  <mspace width="1em"></mspace>
  <msub><mi>A</mi><mi>E</mi></msub><msub><mi>x</mi><mi>E</mi></msub>
  <mo>=</mo>
  <msub><mi>b</mi><mi>E</mi></msub><mo>.</mo>
</math>

이 subproblem들은 linear algebra error를 제외하면 정확하게 풀 수 있다. 또한 outer iteration이 fixed point에 도달하고 local phenomenon equations도 일관되게 만족된다면, 분해된 모델은 원래 steady-state equations의 해와 대응해야 한다.

하지만 더 강한 주장은 보장되지 않는다. 임의의 초기점에서 수렴한다는 증명은 없다. Sequential modular simulation보다 항상 빠르다는 증명도 없다. Basin of attraction이 더 넓다는 증명도 없다. Full equation-oriented method와의 직접 benchmark도 없다.

Local convergence risk는 fixed-point map으로 볼 수 있다.

<math display="block" aria-label="Outer fixed point map Korean">
  <msup><mi>z</mi><mrow><mo>(</mo><mi>k</mi><mo>+</mo><mn>1</mn><mo>)</mo></mrow></msup>
  <mo>=</mo>
  <mi>T</mi><mo>(</mo><msup><mi>z</mi><mrow><mo>(</mo><mi>k</mi><mo>)</mo></mrow></msup><mo>)</mo><mo>.</mo>
</math>

수렴하려면 보통 local Jacobian의 spectral radius가 1보다 작아야 한다.

<math display="block" aria-label="Local fixed point convergence condition Korean">
  <mi>&rho;</mi>
  <mo>(</mo>
  <msub>
    <mfrac><mrow><mo>&part;</mo><mi>T</mi></mrow><mrow><mo>&part;</mo><mi>z</mi></mrow></mfrac>
    <msup><mi>z</mi><mo>*</mo></msup>
  </msub>
  <mo>)</mo>
  <mo>&lt;</mo>
  <mn>1</mn><mo>.</mo>
</math>

Thermodynamic coefficient가 composition 또는 temperature에 매우 민감하거나, phase regime이 switching되거나, global balance matrix가 ill-conditioned이면 이 Jacobian은 위험해진다. Graph representation은 coupling을 읽기 쉽게 만든다. Coupling 자체를 benign하게 만들지는 않는다.

## 독창성을 어떻게 읽어야 하는가

가장 강한 기여는 새로운 graph-theoretic convergence result가 아니다. 화학공정 모델을 local nonlinear phenomenon block과 process-wide linear balance block으로 컴파일하는 architecture다.

이 의미에서 논문은 익숙한 아이디어를 일반화한다.

Unit-level physical decomposition이 process-wide balance coordination으로 확장된다.

Graph는 이 decomposition을 표현하고 구현하는 언어다. BioSTEAM 구현도 이 맥락에 있다. Graph는 variable, equation, update order를 정리하는 데 도움을 준다. 하지만 아직 최적 decomposition을 자동으로 발견하는 algorithm은 아니다. 어떤 variable을 local nonlinear block에 넣고 어떤 balance를 global하게 조정할지는 여전히 공정 지식이 필요하다.

그래서 이 연구는 graph-represented methods에 속하지만 graph neural networks와는 다른 결을 가진다. 여기서 graph는 policy를 학습하거나 value를 예측하는 데 쓰이지 않는다. Solver structure를 표현하는 데 쓰인다.

## 최종 평가

Cortés-Peña and Zavala의 논문은 조심스럽게 읽어야 하는 solver-architecture 논문이다. 이 논문은 unit-operation decomposition이 화학공정 시뮬레이션의 유일한 자연스러운 분해 방식이 아님을 보여준다. Local nonlinear phenomenon coefficient를 고정하고 material 및 energy balance를 전 flowsheet 수준에서 풀면, weakly coupled recycle structure를 더 빨리 닫을 수 있다.

한계도 똑같이 중요하다. Graph representation 자체가 convergence guarantee를 만들지는 않는다. 안정성은 flow, composition, temperature, thermodynamic coefficient, phase regime, global balance matrix가 서로 얼마나 강하게 feedback하는지에 달려 있다.

따라서 공정한 요약은 좁지만 유용하다. 이 논문은 MESH-type physical decomposition을 전체 flowsheet로 일반화한 equation-variable graph 기반 solver architecture다. Coupling이 약하고 매끄러울 때 유망하다. Phase-equilibrium coupling이 강하거나 nonsmooth할 때는 취약하다.

## Reference

Cortés-Peña, Y. R., & Zavala, V. M. (2026). Phenomena-based graph representations and applications to chemical process simulation. *Computers & Chemical Engineering, 213*, Article 109756. [https://doi.org/10.1016/j.compchemeng.2026.109756](https://doi.org/10.1016/j.compchemeng.2026.109756)
