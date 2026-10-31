---
layout: "course-note"
title: "Week 6: Solve Time and Results in Neural-Network Optimization"
title_ko: "6주차: 신경망 기반 최적화의 풀이 속도와 결과 해석"
description: "Bounds, scaling, OMLT, and solver interpretation with open-source HiGHS."
description_ko: "Bounds와 scaling을 조정하고 오픈소스 HiGHS로 신경망 기반 최적화를 풀어 결과를 해석합니다."
material_label: "Week 6"
material_label_ko: "6주차"
updated: "2026-10-31"
permalink: "/courses/surrogate-models/week-06/"
pdf_en: "/assets/courses/surrogate-models/week-06-en.pdf"
pdf_ko: "/assets/courses/surrogate-models/week-06-ko.pdf"
course_id: "surrogate-models"
notebook: "/assets/courses/surrogate-models/week-06/week06_lab.ipynb"
lab_script: "/assets/courses/surrogate-models/week-06/week06_lab.py"
reading_note: "/courses/surrogate-models/week-06-reading/"
reading_pdf_en: "/assets/courses/surrogate-models/week-06-reading-en.pdf"
reading_pdf_ko: "/assets/courses/surrogate-models/week-06-reading-ko.pdf"
---

## Reactor conditions that meet product specifications

A reactor design review requires repeated searches over temperature and residence time. After finding conditions that meet the product specifications, we still need to assess how much improvement may remain.

<figure><img src="/assets/courses/surrogate-models/week-06/motivation-en.svg" alt="Reactor input domain and concentration specifications" /></figure>

This week develops ways to assess unfinished solves and adjust bounds and formulations.

<!-- lecture-page -->

## The problem and the comparison conditions

Add temperature as an input to the Week 5 reactor setting. At a fixed flow of 1 L/min, residence time also selects reactor volume and is therefore a design variable.

Hold the fitted ReLU model, input domain, objective, and product specifications fixed while comparing formulations. Arbitrarily shrinking the temperature interval changes the design problem.

All LPs and MILPs use the open-source HiGHS solver.

<!-- lecture-page -->

## Learning objectives for formulations and solver results

1. Distinguish an incumbent objective from an objective bound and calculate a gap.
2. Compare interval propagation with LP-based bound tightening.
3. Connect a frozen network and its scaling through Pyomo and OMLT.
4. Report termination, time, forward agreement, and constraint residuals.

Review the Week 5 Big-M equivalence and input-bound calculations first.

<!-- lecture-page -->

## The frozen network and its MILP representation

For a ReLU input a with valid bounds L ≤ a ≤ U and L < 0 < U, use these inequalities with binary z.

<math display="block"><mtable columnalign="left"><mtr><mtd><mrow><mi>h</mi><mo>≥</mo><mn>0</mn><mo>,</mo><mtext>  </mtext><mi>h</mi><mo>≥</mo><mi>a</mi></mrow></mtd></mtr><mtr><mtd><mrow><mi>h</mi><mo>≤</mo><mi>U</mi><mi>z</mi><mo>,</mo><mtext>  </mtext><mi>h</mi><mo>≤</mo><mi>a</mi><mo>−</mo><mi>L</mi><mo>(</mo><mn>1</mn><mo>−</mo><mi>z</mi><mo>)</mo></mrow></mtd></mtr></mtable></math>

Weights, biases, and scaling remain fixed. The full problem is an MILP when the other constraints and objective are linear. Exact network representation is separate from process prediction error.

<!-- lecture-page -->

## Incumbents, objective bounds, and gaps

For minimization, the incumbent is the best integer-feasible solution found so far. Its objective value supplies an upper bound that, together with a valid lower bound, brackets the optimum.

<math display="block"><mtable columnalign="left"><mtr><mtd><mrow><msub><mrow><mi>J</mi></mrow><mrow><mi>bound</mi></mrow></msub><mo>≤</mo><msub><mrow><mi>J</mi></mrow><mrow><mi>opt</mi></mrow></msub><mo>≤</mo><msub><mrow><mi>J</mi></mrow><mrow><mi>inc</mi></mrow></msub></mrow></mtd></mtr><mtr><mtd><mrow><msub><mrow><mi>g</mi></mrow><mrow><mi>abs</mi></mrow></msub><mo>=</mo><msub><mrow><mi>J</mi></mrow><mrow><mi>inc</mi></mrow></msub><mo>−</mo><msub><mrow><mi>J</mi></mrow><mrow><mi>bound</mi></mrow></msub><mo>,</mo><mtext>  </mtext><msub><mrow><mi>g</mi></mrow><mrow><mi>rel</mi></mrow></msub><mo>=</mo><mfrac><mrow><msub><mrow><mi>J</mi></mrow><mrow><mi>inc</mi></mrow></msub><mo>−</mo><msub><mrow><mi>J</mi></mrow><mrow><mi>bound</mi></mrow></msub></mrow><mrow><mo>|</mo><msub><mrow><mi>J</mi></mrow><mrow><mi>inc</mi></mrow></msub><mo>|</mo></mrow></mfrac></mrow></mtd></mtr></mtable></math>

An upper bound of 100 and lower bound of 80 give an absolute gap of 20 and a relative gap of 20% under this definition. Without an incumbent this gap is unavailable; near a zero objective, also report the absolute gap.

<!-- lecture-page -->

## How branch-and-bound progresses

Relaxing binaries to continuous intervals gives an LP lower bound for minimization. A fractional binary can be branched into subproblems with z = 0 and z = 1.

An integer-feasible solution updates the incumbent. Infeasible nodes and nodes whose lower bounds cannot improve the incumbent need no further search.

Valid bounds from open nodes form the global lower bound. HiGHS also uses presolve, cuts, and heuristics, so the original LP relaxation value can differ from the final solver bound.

<!-- lecture-page -->

## The continuous relaxation of a ReLU

Relaxing z to [0, 1] and eliminating it gives this triangle for L < 0 < U.

<math display="block"><mtable columnalign="left"><mtr><mtd><mrow><mi>h</mi><mo>≥</mo><mn>0</mn><mo>,</mo><mtext>  </mtext><mi>h</mi><mo>≥</mo><mi>a</mi><mo>,</mo><mtext>  </mtext><mi>h</mi><mo>≤</mo><mfrac><mrow><mi>U</mi></mrow><mrow><mi>U</mi><mo>−</mo><mi>L</mi></mrow></mfrac><mo>(</mo><mi>a</mi><mo>−</mo><mi>L</mi><mo>)</mo></mrow></mtd></mtr></mtable></math>

At a = 0, the largest allowed h is −UL/(U − L). It is 0.5 when L = −1 and U = 1, although the ReLU output is zero.

This triangle is the convex hull of the scalar (a, h) graph. Correlations across inputs and neurons may require additional constraints.

<!-- lecture-page -->

## Two neurons coupled by an equality

Use this dimensionless example to calculate a dependence that box bounds miss.

<math display="block"><mtable columnalign="left"><mtr><mtd><mrow><mn>0</mn><mo>≤</mo><msub><mrow><mi>x</mi></mrow><mrow><mn>1</mn></mrow></msub><mo>,</mo><msub><mrow><mi>x</mi></mrow><mrow><mn>2</mn></mrow></msub><mo>≤</mo><mn>1</mn><mo>,</mo><mtext>  </mtext><msub><mrow><mi>x</mi></mrow><mrow><mn>1</mn></mrow></msub><mo>+</mo><msub><mrow><mi>x</mi></mrow><mrow><mn>2</mn></mrow></msub><mo>=</mo><mn>1</mn></mrow></mtd></mtr><mtr><mtd><mrow><msub><mrow><mi>h</mi></mrow><mrow><mn>1</mn></mrow></msub><mo>=</mo><mi>max</mi><mo>(</mo><mn>0</mn><mo>,</mo><msub><mrow><mi>x</mi></mrow><mrow><mn>1</mn></mrow></msub><mo>+</mo><msub><mrow><mi>x</mi></mrow><mrow><mn>2</mn></mrow></msub><mo>−</mo><mn>1</mn><mo>)</mo><mo>,</mo><mtext>  </mtext><msub><mrow><mi>h</mi></mrow><mrow><mn>2</mn></mrow></msub><mo>=</mo><mi>max</mi><mo>(</mo><mn>0</mn><mo>,</mo><msub><mrow><mi>x</mi></mrow><mrow><mn>1</mn></mrow></msub><mo>−</mo><msub><mrow><mi>x</mi></mrow><mrow><mn>2</mn></mrow></msub><mo>)</mo></mrow></mtd></mtr><mtr><mtd><mrow><msub><mrow><mi>min</mi></mrow><mrow><msub><mrow><mi>x</mi></mrow><mrow><mn>1</mn></mrow></msub><mo>,</mo><msub><mrow><mi>x</mi></mrow><mrow><mn>2</mn></mrow></msub></mrow></msub><mtext>  </mtext><msub><mrow><mi>x</mi></mrow><mrow><mn>1</mn></mrow></msub><mtext>   subject to   </mtext><msub><mrow><mi>h</mi></mrow><mrow><mn>1</mn></mrow></msub><mo>+</mo><msub><mrow><mi>h</mi></mrow><mrow><mn>2</mn></mrow></msub><mo>≥</mo><mn>.4</mn></mrow></mtd></mtr></mtable></math>

Using only the input box gives [−1, 1] for both pre-activations. The input equality, however, makes the first pre-activation identically zero.

<!-- lecture-page -->

## The exact solution of the two-neuron example

<math display="block"><mtable columnalign="left"><mtr><mtd><mrow><msub><mrow><mi>h</mi></mrow><mrow><mn>1</mn></mrow></msub><mo>=</mo><mn>0</mn><mo>,</mo><mtext>  </mtext><msub><mrow><mi>h</mi></mrow><mrow><mn>2</mn></mrow></msub><mo>=</mo><mi>max</mi><mo>(</mo><mn>0</mn><mo>,</mo><mn>2</mn><msub><mrow><mi>x</mi></mrow><mrow><mn>1</mn></mrow></msub><mo>−</mo><mn>1</mn><mo>)</mo></mrow></mtd></mtr><mtr><mtd><mrow><msub><mrow><mi>h</mi></mrow><mrow><mn>2</mn></mrow></msub><mo>≥</mo><mn>.4</mn><mo>⇒</mo><msub><mrow><mi>x</mi></mrow><mrow><mn>1</mn></mrow></msub><mo>≥</mo><mn>.7</mn></mrow></mtd></mtr></mtable></math>

The minimum <math><msub><mrow><mi>x</mi></mrow><mrow><mn>1</mn></mrow></msub></math> is therefore 0.7. The MILP with box bounds and the MILP using the equality both attain this optimum.

The LP relaxation can place h above the network output, so this conclusion does not immediately apply to its solution.

<!-- lecture-page -->

## LP relaxations before and after tightening

<figure><img src="/assets/courses/surrogate-models/week-06/toy-relaxation-en.png" alt="Box-bound and equality-aware LP envelopes compared with the network" /></figure>

The original LP allows <math><msub><mrow><mi>h</mi></mrow><mrow><mn>1</mn></mrow></msub></math> = 0.4 even at <math><msub><mrow><mi>x</mi></mrow><mrow><mn>1</mn></mrow></msub></math> = 0. Enforcing <math><msub><mrow><mi>h</mi></mrow><mrow><mn>1</mn></mrow></msub></math> = 0 raises the LP optimum to 0.4, still below the MILP optimum of 0.7.

<!-- lecture-page -->

## The domain over which bounds are valid

Bounds must hold at every allowed input. Training-sample extrema alone do not guarantee coverage of the full input domain.

Overly narrow bounds can cut off valid network points. Wider valid bounds preserve the integer graph but can weaken its relaxation.

Bounds computed using product specifications are valid only over that constrained feasible set. Recheck them when specifications or the input domain change.

<!-- lecture-page -->

## Interval propagation with weight signs

Suppose the previous layer satisfies ℓ ≤ h ≤ u, with <math><msup><mrow><mi>w</mi></mrow><mrow><mo>+</mo></mrow></msup></math> = max(w, 0) and <math><msup><mrow><mi>w</mi></mrow><mrow><mo>−</mo></mrow></msup></math> = min(w, 0).

<math display="block"><mtable columnalign="left"><mtr><mtd><mrow><msub><mrow><mi>L</mi></mrow><mrow><mi>j</mi></mrow></msub><mo>=</mo><msub><mrow><mi>b</mi></mrow><mrow><mi>j</mi></mrow></msub><mo>+</mo><msub><mrow><mo>∑</mo></mrow><mrow><mi>i</mi></mrow></msub><mo>(</mo><msup><mrow><msub><mrow><mi>w</mi></mrow><mrow><mi>ij</mi></mrow></msub></mrow><mrow><mo>+</mo></mrow></msup><msub><mrow><mi>ℓ</mi></mrow><mrow><mi>i</mi></mrow></msub><mo>+</mo><msup><mrow><msub><mrow><mi>w</mi></mrow><mrow><mi>ij</mi></mrow></msub></mrow><mrow><mo>−</mo></mrow></msup><msub><mrow><mi>u</mi></mrow><mrow><mi>i</mi></mrow></msub><mo>)</mo></mrow></mtd></mtr><mtr><mtd><mrow><msub><mrow><mi>U</mi></mrow><mrow><mi>j</mi></mrow></msub><mo>=</mo><msub><mrow><mi>b</mi></mrow><mrow><mi>j</mi></mrow></msub><mo>+</mo><msub><mrow><mo>∑</mo></mrow><mrow><mi>i</mi></mrow></msub><mo>(</mo><msup><mrow><msub><mrow><mi>w</mi></mrow><mrow><mi>ij</mi></mrow></msub></mrow><mrow><mo>+</mo></mrow></msup><msub><mrow><mi>u</mi></mrow><mrow><mi>i</mi></mrow></msub><mo>+</mo><msup><mrow><msub><mrow><mi>w</mi></mrow><mrow><mi>ij</mi></mrow></msub></mrow><mrow><mo>−</mo></mrow></msup><msub><mrow><mi>ℓ</mi></mrow><mrow><mi>i</mi></mrow></msub><mo>)</mo></mrow></mtd></mtr></mtable></math>

After a ReLU, pass [max(0, L), max(0, U)] to the next layer. This is inexpensive but does not check whether different variable extremes can occur simultaneously.

<!-- lecture-page -->

## LP-based bound tightening

Let P be an LP relaxation containing the network MILP feasible set. Minimize and maximize each pre-activation over P.

<math display="block"><mtable columnalign="left"><mtr><mtd><mrow><msub><mrow><mi>L</mi></mrow><mrow><mi>j</mi></mrow></msub><mo>=</mo><msub><mrow><mi>min</mi></mrow><mrow><mi>v</mi><mo>∈</mo><mi>P</mi></mrow></msub><mtext>  </mtext><msub><mrow><mi>a</mi></mrow><mrow><mi>j</mi></mrow></msub><mo>(</mo><mi>v</mi><mo>)</mo></mrow></mtd></mtr><mtr><mtd><mrow><msub><mrow><mi>U</mi></mrow><mrow><mi>j</mi></mrow></msub><mo>=</mo><msub><mrow><mi>max</mi></mrow><mrow><mi>v</mi><mo>∈</mo><mi>P</mi></mrow></msub><mtext>  </mtext><msub><mrow><mi>a</mi></mrow><mrow><mi>j</mi></mrow></msub><mo>(</mo><mi>v</mi><mo>)</mo></mrow></mtd></mtr></mtable></math>

This is optimization-based bound tightening, or OBBT. The lab solves 54 LPs over the full input domain without product specifications, then rebuilds the MILP with the resulting bounds.

<!-- lecture-page -->

## Handling neurons with fixed activation states

<math display="block"><mtable columnalign="left"><mtr><mtd><mrow><mi>U</mi><mo>≤</mo><mn>0</mn><mo>⇒</mo><mi>h</mi><mo>=</mo><mn>0</mn></mrow></mtd></mtr><mtr><mtd><mrow><mi>L</mi><mo>≥</mo><mn>0</mn><mo>⇒</mo><mi>h</mi><mo>=</mo><mi>a</mi></mrow></mtd></mtr></mtable></math>

These cases need no binary variable. Only neurons whose intervals cross zero remain candidates for branching.

The hand-built MILP uses 24 binaries with loose bounds, 22 with interval propagation, and 19 with LP-OBBT. These are binary-variable counts before solver presolve.

<!-- lecture-page -->

## Input scaling and physical units

<math display="block"><mtable columnalign="left"><mtr><mtd><mrow><msub><mrow><mi>x</mi></mrow><mrow><mn>1</mn></mrow></msub><mo>=</mo><mfrac><mrow><mi>T</mi><mo>−</mo><mn>310</mn></mrow><mrow><mn>40</mn></mrow></mfrac><mo>,</mo><mtext>  </mtext><msub><mrow><mi>x</mi></mrow><mrow><mn>2</mn></mrow></msub><mo>=</mo><mfrac><mrow><mi>τ</mi><mo>−</mo><mn>2</mn></mrow><mrow><mn>8</mn></mrow></mfrac></mrow></mtd></mtr><mtr><mtd><mrow><mi>T</mi><mo>=</mo><mn>310</mn><mo>+</mo><mn>40</mn><msub><mrow><mi>x</mi></mrow><mrow><mn>1</mn></mrow></msub><mo>,</mo><mtext>  </mtext><mi>τ</mi><mo>=</mo><mn>2</mn><mo>+</mo><mn>8</mn><msub><mrow><mi>x</mi></mrow><mrow><mn>2</mn></mrow></msub></mrow></mtd></mtr></mtable></math>

Reuse exactly the offsets and scales used during fitting. Supplying physical-input bounds as scaled-input bounds changes the domain evaluated by the network.

Outputs in this lab already use mol/L. If outputs were standardized, include the fixed inverse transform before connecting product specifications.

<!-- lecture-page -->

## Objective constants and relative gaps

<math display="block"><mtable columnalign="left"><mtr><mtd><mrow><mi>J</mi><mo>=</mo><mi>τ</mi><mo>+</mo><mi>α</mi><mo>(</mo><mi>T</mi><mo>−</mo><mn>310</mn><mo>)</mo><mo>,</mo><mtext>  </mtext><mi>α</mi><mo>=</mo><mn>.02</mn><mtext> min/K</mtext></mrow></mtd></mtr><mtr><mtd><mrow><mi>J</mi><mo>=</mo><mn>2</mn><mo>+</mo><mn>8</mn><msub><mrow><mi>x</mi></mrow><mrow><mn>2</mn></mrow></msub><mo>+</mo><mn>.8</mn><msub><mrow><mi>x</mi></mrow><mrow><mn>1</mn></mrow></msub></mrow></mtd></mtr></mtable></math>

The educational weight α trades residence time against increased temperature. The objective is a min-equivalent score rather than a calibrated process cost.

Dropping the constant 2 preserves the optimizer but changes the denominator of a relative gap. The lab reports objectives and bounds with the constant included.

<!-- lecture-page -->

## Roles of the open-source tools

| Tool | Role |
| --- | --- |
| NumPy | Network forward pass and optional refitting |
| Pyomo | Variables, objective, and process constraints |
| OMLT | Frozen-network constraints in Pyomo |
| HiGHS / highspy | LP and MILP solution |

All LPs and MILPs use open-source HiGHS under the MIT license.

Check the input ordering, scaling, and bounds of the constraints generated by OMLT. [HiGHS official site](https://highs.dev/)

<!-- lecture-page -->

## Connecting OMLT to process constraints

Build `definition` from the weights and scaling, then connect the process constraints. `nn.inputs` uses physical units; `scaled_inputs` holds transformed inputs.

```python
model.nn = OmltBlock()
model.nn.build_formulation(ReluBigMFormulation(definition))
model.product = pyo.Constraint(expr=model.nn.outputs[1] >= .38)
model.byproduct = pyo.Constraint(expr=model.nn.outputs[2] <= .25)
model.obj = pyo.Objective(
    expr=model.nn.inputs[1] + .02*(model.nn.inputs[0]-310))
```

The lab function `make_omlt` contains the complete construction.

<!-- lecture-page -->

## Reproducing Week 5 with OMLT

First check the existing interpolant with residence time as its sole decision, at 330 K and a feed A concentration of 1.2 mol/L. Apply B ≥ 0.40 and C ≤ 0.25 mol/L.

| Formulation | Minimum residence time [min] | Generated binaries |
| --- | --- | --- |
| Hand-built | 5.353846 | 3 |
| OMLT | 5.353846 | 4 |

This OMLT version creates a binary for each ReLU. The hand-built model represents one always-active neuron linearly, using one fewer binary while giving the same outputs.

<!-- lecture-page -->

## Choosing temperature and residence time

<math display="block"><mtable columnalign="left"><mtr><mtd><mrow><msub><mrow><mi>min</mi></mrow><mrow><mi>T</mi><mo>,</mo><mi>τ</mi></mrow></msub><mtext>  </mtext><mi>J</mi><mo>=</mo><mi>τ</mi><mo>+</mo><mn>.02</mn><mo>(</mo><mi>T</mi><mo>−</mo><mn>310</mn><mo>)</mo></mrow></mtd></mtr><mtr><mtd><mrow><mn>310</mn><mo>≤</mo><mi>T</mi><mo>≤</mo><mn>350</mn><mo>,</mo><mtext>  </mtext><mn>2</mn><mo>≤</mo><mi>τ</mi><mo>≤</mo><mn>10</mn></mrow></mtd></mtr><mtr><mtd><mrow><mi>y</mi><mo>=</mo><msub><mrow><mi>f</mi></mrow><mrow><mi>θ</mi></mrow></msub><mo>(</mo><mi>T</mi><mo>,</mo><mi>τ</mi><mo>)</mo><mo>,</mo><mtext>  </mtext><msub><mrow><mi>y</mi></mrow><mrow><mi>B</mi></mrow></msub><mo>≥</mo><mn>.38</mn><mo>,</mo><mtext>  </mtext><msub><mrow><mi>y</mi></mrow><mrow><mi>C</mi></mrow></msub><mo>≤</mo><mn>.25</mn></mrow></mtd></mtr></mtable></math>

Concentrations use mol/L, temperature uses K, and residence time uses min. Predicted concentrations are also constrained to be nonnegative.

The network has two inputs, two hidden layers of 12 ReLUs each, and three linear outputs. Every comparison uses the same frozen coefficients.

<!-- lecture-page -->

## Fitting and independently evaluating the frozen model

Generate concentrations at 1,200 training inputs from ideal isothermal A → B → C CSTR balances and fit with 6,000 NumPy Adam updates. Evaluate physical-unit errors at 500 independent random inputs.

| Component | Test RMSE [mol/L] |
| --- | --- |
| A | 0.00546 |
| B | 0.00440 |
| C | 0.00564 |

The default lab loads the supplied coefficients. `--refit` optionally refits them; weights never change during optimization.

<!-- lecture-page -->

## Comparing relaxation values across bounds

<figure><img src="/assets/courses/surrogate-models/week-06/objective-bounds-en.png" alt="LP objectives for three bound settings and their common MILP optimum" /></figure>

LP-OBBT raises the original LP lower bound from 2.0000 to 2.5215. All three MILPs attain 3.1656. All three comparisons use the same predictor.

<!-- lecture-page -->

## Timing including bound computation

<figure><img src="/assets/courses/surrogate-models/week-06/timing-en.png" alt="Time for bounds, model construction, and the MILP solve" /></figure>

In the supplied run, LP-OBBT reduces MILP solve time, but its total time including bounds exceeds interval propagation. These single-run measurements include interface overhead and do not establish a general speed ranking.

<!-- lecture-page -->

## Selected conditions and solver conclusions

| Item | Supplied run |
| --- | --- |
| Temperature [K] | 342.059300 |
| Residence time [min] | 2.524440 |
| Objective [min-equivalent] | 3.165626 |
| Predicted B [mol/L] | 0.380000 |
| Termination / relative gap | optimal / 0 |

HiGHS establishes optimality for this surrogate MILP within the configured numerical tolerances. The B lower bound is active; the C upper bound has slack.

<!-- lecture-page -->

## Checking forward agreement and residuals

Remove product specifications, fix the input, and solve only the network representation. Evaluate the four domain corners and 12 independent interior points with both the hand-built and OMLT models.

Across 32 checks, the maximum absolute output difference is 7.77e-16 mol/L. Recompute the forward pass at the selected optimum too.

Check constraint and integrality residuals. Finite samples help detect implementation errors; equivalence over the entire domain follows from the formulation conditions developed in Week 5.

<!-- lecture-page -->

## Termination and incumbent availability

| Termination | Interpretation |
| --- | --- |
| optimal | Completed within gap and numerical tolerances |
| Time limit, incumbent found | Report the feasible solution and remaining gap |
| Time limit, no incumbent | No usable solution has been obtained |
| infeasible | The formulated feasible set is empty |
| unbounded / error | Inspect bounds, objective, logs, and model |

A time limit alone does not establish infeasibility. The lab returns `maxTimeLimit` with no incumbent at a zero-second limit, and `infeasible` when B ≥ 2.

<!-- lecture-page -->

## Checking solution availability and loading results

```python
opt = Highs()
opt.config.load_solution = False
opt.config.time_limit = 30.0
result = opt.solve(model)
inc = result.best_feasible_objective
print(result.termination_condition)
if inc is not None and np.isfinite(inc):
    result.solution_loader.load_vars()
    print(inc, result.best_objective_bound)
```

Reading variables after termination without a solution can mistake initial or stale values for results. The complete lab function also returns gaps and constraint residuals.

<!-- lecture-page -->

## Solver gaps and process prediction error

| At the same selected input | B concentration [mol/L] |
| --- | --- |
| Network and MILP | 0.380000 |
| Reference CSTR | 0.371157 |
| Required minimum | 0.380000 |

The reference CSTR misses the B specification. Forward agreement and a zero solver gap still require a separate process-model feasibility check.

Week 8 uses errors at selected points to reconsider decisions and identify additional data.

<!-- lecture-page -->

## Running the lab and reporting comparisons

Extract the lab bundle and run these commands in its directory.

```bash
python -m pip install -r requirements.txt
python week06_lab.py --output-dir my-results
```

1. Verify the toy LP values 0 and 0.4 and MILP value 0.7 by hand.
2. Compare bounds, binary counts, LP lower bounds, and total times for the same frozen model.
3. Report termination, gap, forward differences, and the reference CSTR B-specification violation.

[Reading companion](/courses/surrogate-models/week-06-reading/) · [Lab ZIP](/assets/courses/surrogate-models/week-06/week06-lab.zip)

<!-- lecture-page -->

## Sources and assigned reading

[Ceccon et al., OMLT: Optimization & Machine Learning Toolkit, JMLR 23(349), 2022](https://jmlr.org/papers/v23/22-0277.html) · [Official quick-start](https://omlt.readthedocs.io/en/stable/quickstart.html)

[Anderson et al., Strong mixed-integer programming formulations for trained neural networks, Mathematical Programming, 2020](https://arxiv.org/abs/1811.01988)

[HiGHS and its MIT license](https://highs.dev/) · [Pyomo HiGHS interface](https://pyomo.readthedocs.io/en/stable/api/pyomo.contrib.appsi.solvers.highs.Highs.html)

Work through the companion derivations of the triangle relaxation, OBBT bound directions, scaling, and gaps. Strong multivariate and partition formulations are optional extensions.

<!-- ko -->

## 제품 규격을 만족하는 반응기 조건

반응기 설계 검토에서 온도와 체류시간 후보를 반복해서 계산합니다. 제품 규격을 만족하는 조건을 찾았어도 더 나은 조건이 남아 있는지 판단해야 합니다.

<figure><img src="/assets/courses/surrogate-models/week-06/motivation-ko.svg" alt="반응기 입력 범위와 제품 농도 규격" /></figure>

이번 주에는 계산을 마치기 전에도 해의 품질을 평가하고 bounds와 정식화를 조정하는 방법을 다뤄봅니다.

<!-- lecture-page -->

## 비교할 문제와 계산 조건

5주차 반응기 모델에 온도를 입력으로 추가합니다. 유량을 1 L/min로 고정하므로 체류시간은 반응기 부피도 결정하는 설계변수입니다.

학습을 마친 ReLU 모델, 입력 영역, 목적함수와 제품 규격을 고정하고 정식화만 비교합니다. 온도 범위를 임의로 줄이면 원래 설계 문제와 달라집니다.

모든 LP와 MILP는 오픈소스 HiGHS로 풉니다.

<!-- lecture-page -->

## 정식화와 solver 결과의 학습 목표

1. 가능해의 목적값과 최적값에 대한 bound를 구분하고 gap을 계산합니다.
2. 구간 전파와 LP 기반 bound tightening을 비교합니다.
3. Pyomo·OMLT에 고정 신경망과 scaling을 연결합니다.
4. 종료 상태, 계산 시간, forward 일치와 제약 잔차를 보고합니다.

5주차의 Big-M 동치성과 입력 bounds 계산을 복습한 뒤 시작합니다.

<!-- lecture-page -->

## 고정 신경망과 MILP 표현

각 ReLU의 입력 a에 유효한 L ≤ a ≤ U가 있고 L < 0 < U이면 다음 식에 이진변수 z를 사용합니다.

<math display="block"><mtable columnalign="left"><mtr><mtd><mrow><mi>h</mi><mo>≥</mo><mn>0</mn><mo>,</mo><mtext>  </mtext><mi>h</mi><mo>≥</mo><mi>a</mi></mrow></mtd></mtr><mtr><mtd><mrow><mi>h</mi><mo>≤</mo><mi>U</mi><mi>z</mi><mo>,</mo><mtext>  </mtext><mi>h</mi><mo>≤</mo><mi>a</mi><mo>−</mo><mi>L</mi><mo>(</mo><mn>1</mn><mo>−</mo><mi>z</mi><mo>)</mo></mrow></mtd></mtr></mtable></math>

가중치·bias·scaling은 고정합니다. 다른 제약과 목적함수까지 선형이면 전체 문제가 MILP입니다. 정확한 신경망 표현은 공정 예측 오차와 별개입니다.

<!-- lecture-page -->

## 가능해, bound와 gap

최소화에서 incumbent는 지금까지 찾은 가장 좋은 정수 가능해입니다. 이 가능해의 목적값을 상한으로 사용하면 유효한 하한과 함께 최적값의 범위를 정할 수 있습니다.

<math display="block"><mtable columnalign="left"><mtr><mtd><mrow><msub><mrow><mi>J</mi></mrow><mrow><mi>bound</mi></mrow></msub><mo>≤</mo><msub><mrow><mi>J</mi></mrow><mrow><mi>opt</mi></mrow></msub><mo>≤</mo><msub><mrow><mi>J</mi></mrow><mrow><mi>inc</mi></mrow></msub></mrow></mtd></mtr><mtr><mtd><mrow><msub><mrow><mi>g</mi></mrow><mrow><mi>abs</mi></mrow></msub><mo>=</mo><msub><mrow><mi>J</mi></mrow><mrow><mi>inc</mi></mrow></msub><mo>−</mo><msub><mrow><mi>J</mi></mrow><mrow><mi>bound</mi></mrow></msub><mo>,</mo><mtext>  </mtext><msub><mrow><mi>g</mi></mrow><mrow><mi>rel</mi></mrow></msub><mo>=</mo><mfrac><mrow><msub><mrow><mi>J</mi></mrow><mrow><mi>inc</mi></mrow></msub><mo>−</mo><msub><mrow><mi>J</mi></mrow><mrow><mi>bound</mi></mrow></msub></mrow><mrow><mo>|</mo><msub><mrow><mi>J</mi></mrow><mrow><mi>inc</mi></mrow></msub><mo>|</mo></mrow></mfrac></mrow></mtd></mtr></mtable></math>

상한 100, 하한 80이면 절대 gap은 20이고 이 정의의 상대 gap은 20%입니다. Incumbent가 없으면 이 gap을 계산할 수 없으며, 목적값이 0에 가까우면 절대 gap을 함께 보고합니다.

<!-- lecture-page -->

## Branch-and-bound의 진행

이진변수를 연속 구간으로 완화한 LP를 풀면 최소화 문제의 하한을 얻습니다. LP 해에서 분수값인 이진변수 하나를 선택해 z = 0과 z = 1인 하위 문제로 나눕니다.

정수 가능해를 찾으면 incumbent를 갱신합니다. 불가능한 노드나 하한이 incumbent보다 나쁘거나 같은 노드는 더 탐색할 필요가 없습니다.

열린 노드들의 유효한 하한을 모아 전체 하한을 계산합니다. 실제 HiGHS는 presolve, cutting plane과 heuristic도 사용하므로 원래 LP 완화값과 solver의 최종 bound는 다를 수 있습니다.

<!-- lecture-page -->

## ReLU의 연속 완화

z를 [0, 1]로 완화하고 제거하면 L < 0 < U에서 다음 삼각형을 얻습니다.

<math display="block"><mtable columnalign="left"><mtr><mtd><mrow><mi>h</mi><mo>≥</mo><mn>0</mn><mo>,</mo><mtext>  </mtext><mi>h</mi><mo>≥</mo><mi>a</mi><mo>,</mo><mtext>  </mtext><mi>h</mi><mo>≤</mo><mfrac><mrow><mi>U</mi></mrow><mrow><mi>U</mi><mo>−</mo><mi>L</mi></mrow></mfrac><mo>(</mo><mi>a</mi><mo>−</mo><mi>L</mi><mo>)</mo></mrow></mtd></mtr></mtable></math>

a = 0에서 허용하는 최대 h는 −UL/(U − L)입니다. L = −1, U = 1이면 0.5지만 실제 ReLU 출력은 0입니다.

이 삼각형은 스칼라 (a, h) 그래프의 convex hull입니다. 여러 뉴런과 입력 간 상관관계를 함께 표현하는 데에는 추가 제약이 필요할 수 있습니다.

<!-- lecture-page -->

## 등식 제약이 있는 두 뉴런 예제

다음 무차원 예제로 bounds가 놓치는 관계를 직접 계산합니다.

<math display="block"><mtable columnalign="left"><mtr><mtd><mrow><mn>0</mn><mo>≤</mo><msub><mrow><mi>x</mi></mrow><mrow><mn>1</mn></mrow></msub><mo>,</mo><msub><mrow><mi>x</mi></mrow><mrow><mn>2</mn></mrow></msub><mo>≤</mo><mn>1</mn><mo>,</mo><mtext>  </mtext><msub><mrow><mi>x</mi></mrow><mrow><mn>1</mn></mrow></msub><mo>+</mo><msub><mrow><mi>x</mi></mrow><mrow><mn>2</mn></mrow></msub><mo>=</mo><mn>1</mn></mrow></mtd></mtr><mtr><mtd><mrow><msub><mrow><mi>h</mi></mrow><mrow><mn>1</mn></mrow></msub><mo>=</mo><mi>max</mi><mo>(</mo><mn>0</mn><mo>,</mo><msub><mrow><mi>x</mi></mrow><mrow><mn>1</mn></mrow></msub><mo>+</mo><msub><mrow><mi>x</mi></mrow><mrow><mn>2</mn></mrow></msub><mo>−</mo><mn>1</mn><mo>)</mo><mo>,</mo><mtext>  </mtext><msub><mrow><mi>h</mi></mrow><mrow><mn>2</mn></mrow></msub><mo>=</mo><mi>max</mi><mo>(</mo><mn>0</mn><mo>,</mo><msub><mrow><mi>x</mi></mrow><mrow><mn>1</mn></mrow></msub><mo>−</mo><msub><mrow><mi>x</mi></mrow><mrow><mn>2</mn></mrow></msub><mo>)</mo></mrow></mtd></mtr><mtr><mtd><mrow><msub><mrow><mi>min</mi></mrow><mrow><msub><mrow><mi>x</mi></mrow><mrow><mn>1</mn></mrow></msub><mo>,</mo><msub><mrow><mi>x</mi></mrow><mrow><mn>2</mn></mrow></msub></mrow></msub><mtext>  </mtext><msub><mrow><mi>x</mi></mrow><mrow><mn>1</mn></mrow></msub><mtext>   subject to   </mtext><msub><mrow><mi>h</mi></mrow><mrow><mn>1</mn></mrow></msub><mo>+</mo><msub><mrow><mi>h</mi></mrow><mrow><mn>2</mn></mrow></msub><mo>≥</mo><mn>.4</mn></mrow></mtd></mtr></mtable></math>

입력 구간만 사용하면 두 pre-activation의 bounds는 모두 [−1, 1]입니다. 하지만 첫 번째 pre-activation은 입력 등식 때문에 항상 0입니다.

<!-- lecture-page -->

## 두 뉴런 예제의 정확한 해

<math display="block"><mtable columnalign="left"><mtr><mtd><mrow><msub><mrow><mi>h</mi></mrow><mrow><mn>1</mn></mrow></msub><mo>=</mo><mn>0</mn><mo>,</mo><mtext>  </mtext><msub><mrow><mi>h</mi></mrow><mrow><mn>2</mn></mrow></msub><mo>=</mo><mi>max</mi><mo>(</mo><mn>0</mn><mo>,</mo><mn>2</mn><msub><mrow><mi>x</mi></mrow><mrow><mn>1</mn></mrow></msub><mo>−</mo><mn>1</mn><mo>)</mo></mrow></mtd></mtr><mtr><mtd><mrow><msub><mrow><mi>h</mi></mrow><mrow><mn>2</mn></mrow></msub><mo>≥</mo><mn>.4</mn><mo>⇒</mo><msub><mrow><mi>x</mi></mrow><mrow><mn>1</mn></mrow></msub><mo>≥</mo><mn>.7</mn></mrow></mtd></mtr></mtable></math>

따라서 최소 <math><msub><mrow><mi>x</mi></mrow><mrow><mn>1</mn></mrow></msub></math>은 0.7입니다. 구간 bounds를 사용하는 MILP와 등식을 반영한 MILP 모두 같은 최적값을 냅니다.

LP 완화에서는 h가 실제 신경망 출력보다 커질 수 있으므로 같은 결론이 바로 성립하지 않습니다.

<!-- lecture-page -->

## Bounds 강화 전후의 LP 완화

<figure><img src="/assets/courses/surrogate-models/week-06/toy-relaxation-ko.png" alt="구간 bounds, 등식 반영 bounds와 실제 신경망 출력의 비교" /></figure>

원래 LP는 <math><msub><mrow><mi>x</mi></mrow><mrow><mn>1</mn></mrow></msub></math> = 0에서도 첫 뉴런의 <math><msub><mrow><mi>h</mi></mrow><mrow><mn>1</mn></mrow></msub></math> = 0.4를 허용합니다. <math><msub><mrow><mi>h</mi></mrow><mrow><mn>1</mn></mrow></msub></math> = 0을 반영하면 LP 최적값은 0.4로 올라가지만 MILP 최적값 0.7에는 아직 못 미칩니다.

<!-- lecture-page -->

## Bounds의 유효한 범위

Bounds는 허용한 모든 입력에서 성립해야 합니다. 학습 데이터의 최솟값·최댓값만으로는 입력 영역 전체를 덮는다고 보장할 수 없습니다.

너무 좁은 bounds는 유효한 신경망 점을 잘라내고, 넓은 bounds는 정수해의 그래프를 유지하면서 완화를 약하게 만들 수 있습니다.

제품 규격까지 사용해 계산한 bounds는 해당 규격의 가능집합에만 유효합니다. 규격이나 입력 영역을 바꿀 때는 bounds를 다시 확인합니다.

<!-- lecture-page -->

## 가중치 부호를 반영한 구간 전파

이전 층의 각 출력이 ℓ ≤ h ≤ u에 있고 <math><msup><mrow><mi>w</mi></mrow><mrow><mo>+</mo></mrow></msup></math> = max(w, 0), <math><msup><mrow><mi>w</mi></mrow><mrow><mo>−</mo></mrow></msup></math> = min(w, 0)라고 놓습니다.

<math display="block"><mtable columnalign="left"><mtr><mtd><mrow><msub><mrow><mi>L</mi></mrow><mrow><mi>j</mi></mrow></msub><mo>=</mo><msub><mrow><mi>b</mi></mrow><mrow><mi>j</mi></mrow></msub><mo>+</mo><msub><mrow><mo>∑</mo></mrow><mrow><mi>i</mi></mrow></msub><mo>(</mo><msup><mrow><msub><mrow><mi>w</mi></mrow><mrow><mi>ij</mi></mrow></msub></mrow><mrow><mo>+</mo></mrow></msup><msub><mrow><mi>ℓ</mi></mrow><mrow><mi>i</mi></mrow></msub><mo>+</mo><msup><mrow><msub><mrow><mi>w</mi></mrow><mrow><mi>ij</mi></mrow></msub></mrow><mrow><mo>−</mo></mrow></msup><msub><mrow><mi>u</mi></mrow><mrow><mi>i</mi></mrow></msub><mo>)</mo></mrow></mtd></mtr><mtr><mtd><mrow><msub><mrow><mi>U</mi></mrow><mrow><mi>j</mi></mrow></msub><mo>=</mo><msub><mrow><mi>b</mi></mrow><mrow><mi>j</mi></mrow></msub><mo>+</mo><msub><mrow><mo>∑</mo></mrow><mrow><mi>i</mi></mrow></msub><mo>(</mo><msup><mrow><msub><mrow><mi>w</mi></mrow><mrow><mi>ij</mi></mrow></msub></mrow><mrow><mo>+</mo></mrow></msup><msub><mrow><mi>u</mi></mrow><mrow><mi>i</mi></mrow></msub><mo>+</mo><msup><mrow><msub><mrow><mi>w</mi></mrow><mrow><mi>ij</mi></mrow></msub></mrow><mrow><mo>−</mo></mrow></msup><msub><mrow><mi>ℓ</mi></mrow><mrow><mi>i</mi></mrow></msub><mo>)</mo></mrow></mtd></mtr></mtable></math>

ReLU 뒤에는 [max(0, L), max(0, U)]를 다음 층에 전달합니다. 계산 비용은 작지만 각 변수의 극값을 동시에 달성할 수 있는지는 반영하지 않습니다.

<!-- lecture-page -->

## LP 기반 bound tightening

P를 신경망 MILP 가능집합을 포함하는 LP 완화라고 놓습니다. 각 pre-activation을 목적함수로 바꾸어 최소화·최대화합니다.

<math display="block"><mtable columnalign="left"><mtr><mtd><mrow><msub><mrow><mi>L</mi></mrow><mrow><mi>j</mi></mrow></msub><mo>=</mo><msub><mrow><mi>min</mi></mrow><mrow><mi>v</mi><mo>∈</mo><mi>P</mi></mrow></msub><mtext>  </mtext><msub><mrow><mi>a</mi></mrow><mrow><mi>j</mi></mrow></msub><mo>(</mo><mi>v</mi><mo>)</mo></mrow></mtd></mtr><mtr><mtd><mrow><msub><mrow><mi>U</mi></mrow><mrow><mi>j</mi></mrow></msub><mo>=</mo><msub><mrow><mi>max</mi></mrow><mrow><mi>v</mi><mo>∈</mo><mi>P</mi></mrow></msub><mtext>  </mtext><msub><mrow><mi>a</mi></mrow><mrow><mi>j</mi></mrow></msub><mo>(</mo><mi>v</mi><mo>)</mo></mrow></mtd></mtr></mtable></math>

이 방식은 optimization-based bound tightening(OBBT)입니다. 실습은 제품 규격을 제외한 입력 영역 전체에서 LP 54개를 풀고, bounds를 적용한 MILP를 새로 만듭니다.

<!-- lecture-page -->

## 활성이 고정된 뉴런의 처리

<math display="block"><mtable columnalign="left"><mtr><mtd><mrow><mi>U</mi><mo>≤</mo><mn>0</mn><mo>⇒</mo><mi>h</mi><mo>=</mo><mn>0</mn></mrow></mtd></mtr><mtr><mtd><mrow><mi>L</mi><mo>≥</mo><mn>0</mn><mo>⇒</mo><mi>h</mi><mo>=</mo><mi>a</mi></mrow></mtd></mtr></mtable></math>

이 두 경우에는 이진변수가 필요하지 않습니다. 0을 가로지르는 뉴런만 분기 대상으로 남깁니다.

실습에서 직접 작성한 MILP는 넓은 bounds에서 이진변수 24개, 구간 전파에서 22개, LP-OBBT에서 19개를 사용합니다. 이 개수는 solver presolve를 적용하기 전의 이진변수 수입니다.

<!-- lecture-page -->

## 입력 scaling과 물리 단위

<math display="block"><mtable columnalign="left"><mtr><mtd><mrow><msub><mrow><mi>x</mi></mrow><mrow><mn>1</mn></mrow></msub><mo>=</mo><mfrac><mrow><mi>T</mi><mo>−</mo><mn>310</mn></mrow><mrow><mn>40</mn></mrow></mfrac><mo>,</mo><mtext>  </mtext><msub><mrow><mi>x</mi></mrow><mrow><mn>2</mn></mrow></msub><mo>=</mo><mfrac><mrow><mi>τ</mi><mo>−</mo><mn>2</mn></mrow><mrow><mn>8</mn></mrow></mfrac></mrow></mtd></mtr><mtr><mtd><mrow><mi>T</mi><mo>=</mo><mn>310</mn><mo>+</mo><mn>40</mn><msub><mrow><mi>x</mi></mrow><mrow><mn>1</mn></mrow></msub><mo>,</mo><mtext>  </mtext><mi>τ</mi><mo>=</mo><mn>2</mn><mo>+</mo><mn>8</mn><msub><mrow><mi>x</mi></mrow><mrow><mn>2</mn></mrow></msub></mrow></mtd></mtr></mtable></math>

학습 때 사용한 offset과 scale을 그대로 가져옵니다. 물리 입력의 bounds를 scaled 입력에 잘못 전달하면 신경망을 평가하는 영역이 바뀝니다.

이 실습의 출력 단위는 mol/L입니다. 표준화된 출력을 사용한다면 제품 규격에 연결하기 전에 고정된 역변환도 넣어야 합니다.

<!-- lecture-page -->

## 목적함수의 상수와 상대 gap

<math display="block"><mtable columnalign="left"><mtr><mtd><mrow><mi>J</mi><mo>=</mo><mi>τ</mi><mo>+</mo><mi>α</mi><mo>(</mo><mi>T</mi><mo>−</mo><mn>310</mn><mo>)</mo><mo>,</mo><mtext>  </mtext><mi>α</mi><mo>=</mo><mn>.02</mn><mtext> min/K</mtext></mrow></mtd></mtr><mtr><mtd><mrow><mi>J</mi><mo>=</mo><mn>2</mn><mo>+</mo><mn>8</mn><msub><mrow><mi>x</mi></mrow><mrow><mn>2</mn></mrow></msub><mo>+</mo><mn>.8</mn><msub><mrow><mi>x</mi></mrow><mrow><mn>1</mn></mrow></msub></mrow></mtd></mtr></mtable></math>

α는 체류시간과 온도 증가를 함께 비교하기 위한 교육용 가중치입니다. 이 목적함수의 단위는 min 등가 점수이며 공정의 실제 비용식은 아닙니다.

상수 2를 빼도 최적 입력은 같지만 상대 gap의 분모는 바뀝니다. 실습은 상수를 포함한 목적값과 bound를 그대로 보고합니다.

<!-- lecture-page -->

## 오픈소스 계산 도구의 역할

| 도구 | 역할 |
| --- | --- |
| NumPy | 신경망 forward 계산과 선택 재학습 |
| Pyomo | 변수·목적함수·공정 제약 작성 |
| OMLT | 고정 신경망을 Pyomo 제약으로 변환 |
| HiGHS / highspy | LP와 MILP 풀이 |

모든 LP와 MILP는 MIT 라이선스의 오픈소스 HiGHS로 풉니다.

OMLT가 만든 제약도 입력 순서, scaling, bounds와 함께 확인합니다. [HiGHS 공식 안내](https://highs.dev/)

<!-- lecture-page -->

## OMLT와 공정 제약 연결

가중치와 scaling을 담은 `definition`을 만든 뒤 다음과 같이 연결합니다. `nn.inputs`는 물리 단위이고 `scaled_inputs`는 변환된 입력입니다.

```python
model.nn = OmltBlock()
model.nn.build_formulation(ReluBigMFormulation(definition))
model.product = pyo.Constraint(expr=model.nn.outputs[1] >= .38)
model.byproduct = pyo.Constraint(expr=model.nn.outputs[2] <= .25)
model.obj = pyo.Objective(
    expr=model.nn.inputs[1] + .02*(model.nn.inputs[0]-310))
```

완전한 구성 코드는 실습의 `make_omlt` 함수에 있습니다.

<!-- lecture-page -->

## 5주차 예제의 OMLT 재현

온도 330 K, 유입 A 농도 1.2 mol/L에서 체류시간만 선택하는 기존 보간 모델을 먼저 확인합니다. B ≥ 0.40, C ≤ 0.25 mol/L를 적용합니다.

| 정식화 | 최소 체류시간 [min] | 생성된 이진변수 |
| --- | --- | --- |
| 직접 작성 | 5.353846 | 3 |
| OMLT | 5.353846 | 4 |

OMLT는 이 버전에서 ReLU마다 이진변수를 생성합니다. 직접 작성한 모델은 항상 활성인 뉴런 하나를 선형으로 표현하므로 이진변수가 하나 적고 출력은 같습니다.

<!-- lecture-page -->

## 온도와 체류시간을 선택하는 문제

<math display="block"><mtable columnalign="left"><mtr><mtd><mrow><msub><mrow><mi>min</mi></mrow><mrow><mi>T</mi><mo>,</mo><mi>τ</mi></mrow></msub><mtext>  </mtext><mi>J</mi><mo>=</mo><mi>τ</mi><mo>+</mo><mn>.02</mn><mo>(</mo><mi>T</mi><mo>−</mo><mn>310</mn><mo>)</mo></mrow></mtd></mtr><mtr><mtd><mrow><mn>310</mn><mo>≤</mo><mi>T</mi><mo>≤</mo><mn>350</mn><mo>,</mo><mtext>  </mtext><mn>2</mn><mo>≤</mo><mi>τ</mi><mo>≤</mo><mn>10</mn></mrow></mtd></mtr><mtr><mtd><mrow><mi>y</mi><mo>=</mo><msub><mrow><mi>f</mi></mrow><mrow><mi>θ</mi></mrow></msub><mo>(</mo><mi>T</mi><mo>,</mo><mi>τ</mi><mo>)</mo><mo>,</mo><mtext>  </mtext><msub><mrow><mi>y</mi></mrow><mrow><mi>B</mi></mrow></msub><mo>≥</mo><mn>.38</mn><mo>,</mo><mtext>  </mtext><msub><mrow><mi>y</mi></mrow><mrow><mi>C</mi></mrow></msub><mo>≤</mo><mn>.25</mn></mrow></mtd></mtr></mtable></math>

농도는 mol/L, 온도는 K, 체류시간은 min입니다. 각 예측 농도에는 비음수 제약도 적용합니다.

신경망은 입력 2개, 뉴런이 12개씩인 ReLU 은닉층 두 개, 선형 출력 3개로 구성됩니다. 모든 비교에 같은 고정 계수를 사용합니다.

<!-- lecture-page -->

## 고정 모델의 학습과 독립 예측 평가

이상적 등온 A → B → C CSTR 수지에서 학습 입력 1,200개의 농도를 생성하고 NumPy Adam으로 6,000회 갱신했습니다. 독립 난수 입력 500개에서 물리 단위 오차를 평가합니다.

| 성분 | Test RMSE [mol/L] |
| --- | --- |
| A | 0.00546 |
| B | 0.00440 |
| C | 0.00564 |

기본 실습은 제공된 계수를 읽습니다. `--refit`은 선택 재학습이며 최적화 도중 가중치를 바꾸지 않습니다.

<!-- lecture-page -->

## Bounds에 따른 완화값 비교

<figure><img src="/assets/courses/surrogate-models/week-06/objective-bounds-ko.png" alt="세 bounds 설정의 LP 목적값과 공통 MILP 최적값" /></figure>

LP-OBBT는 원래 LP 하한을 2.0000에서 2.5215로 올렸습니다. 세 MILP의 최적값은 모두 3.1656으로 일치합니다. 세 비교에는 같은 예측 모델을 사용했습니다.

<!-- lecture-page -->

## Bounds 계산 비용을 포함한 시간

<figure><img src="/assets/courses/surrogate-models/week-06/timing-ko.png" alt="Bounds 계산, 모델 구성과 MILP 풀이 시간" /></figure>

제공 실행에서 LP-OBBT의 MILP 풀이 시간은 줄었지만 bounds 계산을 더한 총시간은 구간 전파보다 길었습니다. 인터페이스 비용을 포함해 한 번 측정한 결과이므로 이 속도 순위가 일반적으로 성립하는지는 알 수 없습니다.

<!-- lecture-page -->

## 선택된 조건과 solver의 결론

| 항목 | 제공 실행 |
| --- | --- |
| 온도 [K] | 342.059300 |
| 체류시간 [min] | 2.524440 |
| 목적값 [min 등가] | 3.165626 |
| 예측 B [mol/L] | 0.380000 |
| 종료 상태 / 상대 gap | optimal / 0 |

HiGHS는 설정한 수치 허용오차 안에서 이 surrogate MILP의 최적성을 확인했습니다. B 하한은 활성이고 C 상한에는 여유가 있습니다.

<!-- lecture-page -->

## Forward 일치와 제약 잔차 검사

제품 규격을 뺀 상태에서 입력을 고정하고 신경망 표현만 풉니다. 입력 영역의 네 모서리와 독립 내부점 12개를 직접 작성한 모델과 OMLT에 각각 넣습니다.

32회 검사에서 출력의 최대 절대 차이는 7.77e-16 mol/L였습니다. 선택된 최적 조건에서도 forward 출력을 다시 계산합니다.

제약 잔차와 이진변수의 정수성 잔차도 확인합니다. 표본 검사는 구현 오류를 찾는 데 사용합니다. 영역 전체의 수학적 동치는 5주차의 정식화 조건이 성립해야 보장됩니다.

<!-- lecture-page -->

## 종료 상태와 가능해 존재 여부

| 종료 상태 | 해석 |
| --- | --- |
| optimal | 설정한 gap·수치 허용오차 안에서 완료 |
| 시간 제한, incumbent 있음 | 가능해와 남은 gap을 보고 |
| 시간 제한, incumbent 없음 | 사용할 해를 아직 확보하지 못함 |
| infeasible | 작성한 문제의 가능집합이 비어 있음 |
| unbounded / error | Bounds·목적식·로그와 모델 확인 |

시간 제한만으로 infeasible을 결론 내리지 않습니다. 실습의 0초 제한은 `maxTimeLimit`과 incumbent 없음, B ≥ 2인 경우는 `infeasible`을 반환했습니다.

<!-- lecture-page -->

## 가능해 확인과 결과 불러오기

```python
opt = Highs()
opt.config.load_solution = False
opt.config.time_limit = 30.0
result = opt.solve(model)
inc = result.best_feasible_objective
print(result.termination_condition)
if inc is not None and np.isfinite(inc):
    result.solution_loader.load_vars()
    print(inc, result.best_objective_bound)
```

가능해가 없는 종료에서 변수 값을 읽으면 초기값이나 이전 계산값을 결과로 오해할 수 있습니다. 실습 함수는 gap과 제약 잔차도 반환합니다.

<!-- lecture-page -->

## Solver gap과 공정 예측 오차

| 선택한 같은 입력 | B 농도 [mol/L] |
| --- | --- |
| 신경망 및 MILP | 0.380000 |
| 기준 CSTR | 0.371157 |
| 요구 하한 | 0.380000 |

기준 CSTR의 B 농도는 규격보다 낮습니다. 정식화가 forward와 일치하고 solver gap이 0이어도 공정 모델의 제약 만족은 따로 확인해야 합니다.

8주차에서는 이런 선택 지점의 오차를 바탕으로 조건을 재검토하고 추가 데이터를 정합니다.

<!-- lecture-page -->

## 실습 실행과 비교 보고서

실습 묶음을 풀고 같은 폴더에서 실행합니다.

```bash
python -m pip install -r requirements.txt
python week06_lab.py --output-dir my-results
```

1. 두 뉴런 예제의 LP 값 0, 0.4와 MILP 값 0.7을 손으로 확인합니다.
2. 동일한 고정 모델에서 bounds·이진변수 수·LP 하한·총시간을 비교합니다.
3. 종료 상태·gap·forward 차이와 기준 CSTR의 B 규격 위반을 보고합니다.

[읽기자료](/courses/surrogate-models/week-06-reading/) · [실습 ZIP](/assets/courses/surrogate-models/week-06/week06-lab.zip)

<!-- lecture-page -->

## 출처와 지정 읽기

[OMLT 논문: Ceccon 등, JMLR 23(349), 2022](https://jmlr.org/papers/v23/22-0277.html) · [공식 사용 예제](https://omlt.readthedocs.io/en/stable/quickstart.html)

[Anderson 등, Strong mixed-integer programming formulations for trained neural networks, Mathematical Programming, 2020](https://arxiv.org/abs/1811.01988)

[HiGHS 공식 사이트와 MIT 라이선스 안내](https://highs.dev/) · [Pyomo의 HiGHS 인터페이스](https://pyomo.readthedocs.io/en/stable/api/pyomo.contrib.appsi.solvers.highs.Highs.html)

읽기자료에서 삼각형 완화 유도, OBBT의 bound 방향, scaling과 gap 계산을 따라갑니다. Anderson 등의 다변수 강한 정식화와 partition formulation은 선택 심화입니다.
