---
layout: course-note
title: "Syllabus: Surrogate Modeling for Process Prediction and Optimization"
title_ko: "Syllabus: 공정 예측과 최적화를 위한 서로게이트 모델링"
description: "Build validated process predictors, learn optimization formulations and model structures, then select and revalidate operating conditions."
description_ko: "공정 예측 모델을 학습·검증하고, 최적화 정식화와 모델 구조를 배운 뒤 운전 조건을 선택하고 재검증하는 8주 과정입니다."
material_label: "Syllabus"
material_label_ko: "강의 계획"
updated: "2026-10-09"
permalink: /courses/surrogate-models/syllabus/
pdf_en: /assets/courses/surrogate-models/syllabus-en.pdf
pdf_ko: /assets/courses/surrogate-models/syllabus-ko.pdf
course_id: "surrogate-models"
---

## Course purpose

Start by learning a process response from data: define inputs and outputs, fit a surrogate, and check its predictions on independent conditions. Then examine physical consistency and learn how a trained function can be represented inside an optimization problem. Finally, choose operating conditions and revalidate them with the reference process.

The course follows **prediction → physical consistency → optimization formulations and model structure → operating decisions**. It covers both formulating an already-trained model and designing a model structure for an intended optimization use. Prediction error, physical consistency, formulation agreement, and decision quality are evaluated separately.

Designed by Sunwoo Kim as an independent, self-paced course for chemical engineers entering graduate study. Original explanations, worked readings, and runnable examples accompany verified research sources.

## Audience and prerequisites

Basic Python, derivatives, matrix operations, linear algebra, and material balances are expected. Prior neural-network or mathematical-programming research experience is not required. LP/MILP, convexity, and KKT conditions are introduced when needed.

Suggested weekly workload: 90 minutes of theory, 60–90 minutes of guided coding, and 2–3 hours of reading or exercises. These are study recommendations, not scheduled classes.

## Learning outcomes

By the end of the course, learners should be able to:

1. Define a process prediction task: inputs, outputs, fixed context, states, units, data splits, and valid domain.
2. Fit steady-state and dynamic surrogates, and evaluate component errors and trajectory errors using independent data and prescribed future inputs.
3. Compare unconstrained, soft-physics, and hard linear-equality models, separating prediction accuracy from physical consistency.
4. Define operating variables, an objective, and constraints; formulate a frozen ReLU model as a valid MILP and check agreement with its forward pass.
5. Select model structure and formulation for the intended use, including the conditions under which ReLU ICNN/PICNN epigraphs permit an equivalent LP problem.
6. Solve a surrogate-based operating problem and report reference-model feasibility, economic performance, solver termination, gaps, and time separately.

## Eight-week sequence

{% assign course = site.data.courses | where: 'id', 'surrogate-models' | first %}

| Week | Topic and scope | Required output |
| --- | --- | --- |
{% for week in course.weeks %}| {{ week.number }} | **{{ week.title }}.** {{ week.topics }} | {{ week.deliverable }} |
{% endfor %}

Weeks 1–3 establish prediction. Week 4 examines physical consistency. Weeks 5–6 formulate and solve problems with trained models; Week 7 designs model structure for optimization. Week 8 integrates the full workflow. Operating decisions are introduced briefly as the course destination in Week 1.

The syllabus and [Week 1]({{ '/courses/surrogate-models/week-01/' | relative_url }})–[Week 3]({{ '/courses/surrogate-models/week-03/' | relative_url }}) materials are available. Weeks 4–8 remain planned.

## Reading assignments

| Week | Reading guidance |
| --- | --- |
{% for week in course.weeks %}| {{ week.number }} | {{ week.reading }} |
{% endfor %}

Start with the supplied [Week 1]({{ '/courses/surrogate-models/week-01-reading/' | relative_url }}), [Week 2]({{ '/courses/surrogate-models/week-02-reading/' | relative_url }}), and [Week 3 reading companions]({{ '/courses/surrogate-models/week-03-reading/' | relative_url }}), each available as English/Korean PDFs. External readings use selected sections. RNN/LSTM, encoder–decoder, DeepONet, advanced formulation proofs, and longer-horizon examples are optional extensions.

## Core sources

- **Convex optimization background:** S. Boyd and L. Vandenberghe, *Convex Optimization* (2004). Read selected parts of Chapters 2–4 for convex sets, convex functions, epigraphs, and optimization problems; return to Chapter 5 for duality and KKT. [Official book and downloads](https://web.stanford.edu/~boyd/cvxbook/) · [EE364a slides](https://web.stanford.edu/class/ee364a/lectures.html).
- **Neural-network implementation:** PyTorch tutorials on [model construction](https://docs.pytorch.org/tutorials/beginner/basics/buildmodel_tutorial.html), [autograd](https://docs.pytorch.org/tutorials/beginner/basics/autogradqs_tutorial.html), and [training](https://docs.pytorch.org/tutorials/beginner/basics/optimization_tutorial.html).
- **ICNN/PICNN:** B. Amos, L. Xu, and J. Z. Kolter, *Input Convex Neural Networks*, ICML (2017). Section 3 gives architecture conditions; Supplement B gives LP inference for ReLU/linear units. [Paper](https://proceedings.mlr.press/v70/amos17b.html) · [PDF](https://proceedings.mlr.press/v70/amos17b/amos17b.pdf) · [Supplement](https://proceedings.mlr.press/v70/amos17b/amos17b-supp.pdf).
- **ReLU formulations:** R. Anderson, J. Huchette, W. Ma, C. Tjandraatmadja, and J. P. Vielma, *Strong mixed-integer programming formulations for trained neural networks*, Mathematical Programming (2020). The public manuscript was first submitted in 2018 and revised in 2020. [Public manuscript](https://arxiv.org/abs/1811.01988).
- **Embedding software:** F. Ceccon, J. Jalving, J. Haddad, A. Thebelt, C. Tsay, C. D. Laird, and R. Misener, *OMLT: Optimization & Machine Learning Toolkit*, JMLR 23(349), 1–8 (2022). [Paper and PDF](https://jmlr.org/papers/v23/22-0277.html) · [Code](https://github.com/cog-imperial/OMLT) · [Documentation](https://omlt.readthedocs.io/en/stable/).
- **PINN:** M. Raissi, P. Perdikaris, and G. E. Karniadakis, *Physics-informed neural networks: A deep learning framework for solving forward and inverse problems involving nonlinear partial differential equations*, Journal of Computational Physics 378, 686–707 (2019). [Published paper](https://doi.org/10.1016/j.jcp.2018.10.045). The related 2017 Part I manuscript is a freely available introduction; it is not the identical final journal version. [2017 Part I](https://arxiv.org/abs/1711.10561).
- **KKT-hPINN:** H. Chen, G. E. Constante Flores, and C. Li, *Physics-informed neural networks with hard linear equality constraints*, Computers & Chemical Engineering 189, 108764 (2024). [Published paper](https://doi.org/10.1016/j.compchemeng.2024.108764) · [Public manuscript](https://arxiv.org/abs/2402.07251) · [Code and datasets](https://github.com/li-group/KKThPINN).
- **Sequence-learning background:** I. Sutskever, O. Vinyals, and Q. V. Le, *Sequence to Sequence Learning with Neural Networks*, NeurIPS (2014). Its application is translation; our process-trajectory exercises are separate educational examples. [Paper](https://proceedings.neurips.cc/paper_files/paper/2014/hash/5a18e133cbf9f257297f410bb7eca942-Abstract.html).

Optional extensions: [DeepONet, Nature Machine Intelligence (2021)](https://www.nature.com/articles/s42256-021-00302-5), for input-function to output-function mappings; [KKT-Hardnet public manuscript (2025), published in C&CE (2026)](https://arxiv.org/abs/2507.08124), for nonlinear equality and inequality projection.

## Process examples and software

Week 1 uses a small ideal isothermal CSTR, reference-generated data, and a quadratic regression baseline. Week 2 extends to A → B → C and a steady-state MLP. Week 3 uses state transitions and rollout as the common dynamic example. These teaching models run without Aspen or plant data; they do not establish the computational cost or fidelity of an industrial simulator.

Week 4 uses residual losses and consistent linear equalities; public KKT-hPINN datasets are a separate reproduction exercise. Weeks 5–6 reuse a frozen ReLU predictor for optimization. Week 7 first checks convexity and LP equivalence on a separate known convex target; an ICNN approximation does not prove that a CSTR or every flowsheet output is convex.

Week 1 requires Python, NumPy, and Matplotlib. Week 2 adds PyTorch. Later weeks introduce Pyomo/OMLT and a suitable solver. The Week 1 script runs prediction by default; `--extensions` retains the earlier operating-selection and dynamic examples for later study.

## What “exact” and “hard” mean here

- **Exact embedding:** a formulation represents the frozen learned function over the stated domain. It does not remove approximation error relative to the physical process. MILP status also depends on the rest of the objective and constraints.
- **LP reformulation:** ReLU/linear ICNN structure, fixed PICNN context, valid nonnegative propagation, and appropriate epigraph usage matter. Arbitrary output equalities, reversed inequalities, smooth activations, or additional nonlinear constraints can invalidate an LP claim.
- **Hard constraints:** KKT-hPINN enforces the specified consistent linear equalities under its matrix assumptions, up to numerical arithmetic. It does not automatically enforce positivity, nonlinear thermodynamics, stability, or every operating limit.
- **Optimization with physics-informed models:** training losses do not determine the algebraic class of the frozen predictor. A ReLU backbone followed by a fixed affine equality projection remains piecewise affine; a smooth or nonlinear projection can change the required formulation.

## Exercises and final project

Week 1 submits a prediction specification, fitted baseline, and held-out evaluation. Week 2 submits a steady-state MLP, checked gradient update, and component/consistency diagnostics. Later weeks add verified elements.

Document the domain, data split, model structure, frozen weights, scaling, formulation assumptions, solver termination, and reference process. Report prediction error, physical consistency, formulation agreement, and decision quality separately. Compare economics with the reference model. Identify grid or local-solver benchmarks without claiming certified global process optimality.

Assessment covers mathematical correctness, reproducibility, decision evidence, and accurate reporting of unresolved error or feasibility. Include failed operating points and incomplete solves.

<!-- ko -->

## 과목의 목적

먼저 공정 응답을 데이터로 예측하는 모델을 만든다. 입력과 출력을 정의하고 surrogate를 학습한 뒤, 독립적인 조건에서 예측을 확인한다. 이어서 물리적 일관성을 평가하고, 학습된 함수를 최적화 문제 안에 표현하는 방법을 배운다. 마지막으로 운전 조건을 선택하고 기준 공정 모델로 재검증한다.

전체 흐름은 **공정 예측 → 물리적 일관성 → 최적화 정식화와 모델 구조 설계 → 운전 의사결정**이다. 이미 학습된 모델을 정식화하는 접근과 최적화 활용을 고려해 모델 구조를 설계하는 접근을 함께 다룬다. 예측 오차, 물리적 일관성, 정식화의 일치성, 의사결정 품질은 구분해 평가한다.

Sunwoo Kim이 화학공학 대학원 입문자를 위해 구성한 독립적인 자율 학습 과정이다. 직접 작성한 설명·계산 읽기자료·실행 예제를 검증된 연구 원문에 연결한다.

## 수강 대상과 선수 지식

Python 기초, 미분, 행렬 연산, 선형대수, 물질수지를 알고 있다고 가정한다. 신경망이나 수리계획 연구 경험은 요구하지 않는다. LP/MILP, convexity, KKT 조건은 필요한 시점에 설명한다.

권장 주간 학습량은 이론 90분, 안내된 실습 60–90분, 읽기·연습문제 2–3시간이다. 실제 수업 시간표가 아니라 자율 학습을 위한 제안이다.

## 학습 목표

과정을 마친 뒤에는 다음을 할 수 있어야 한다.

1. 공정 예측 문제의 입력·출력·고정 context·상태·단위·데이터 분할·유효한 영역을 정의한다.
2. 정상상태·동적 surrogate를 학습하고, 독립 데이터와 정해진 미래 입력에서 성분별·궤적 예측 오차를 평가한다.
3. 일반 모델, soft physics 모델, hard 선형 등식 모델을 비교하고 예측 정확도와 물리적 일관성을 구분한다.
4. 조작변수·목적함수·제약을 정의하고, 고정된 ReLU 모델의 유효한 MILP 표현을 작성해 forward 출력과 대조한다.
5. 활용 목적에 맞는 모델 구조와 정식화를 선택하고, ReLU ICNN/PICNN epigraph가 동치인 LP 문제를 허용하는 조건을 확인한다.
6. Surrogate 기반 운전 최적화를 풀고 기준 공정 모델의 제약 만족·경제성·solver 종료 상태·gap·시간을 각각 보고한다.

## 8주 구성

| 주차 | 주제와 범위 | 필수 결과물 |
| --- | --- | --- |
{% for week in course.weeks %}| {{ week.number }} | **{{ week.title_ko }}.** {{ week.topics_ko }} | {{ week.deliverable_ko }} |
{% endfor %}

1–3주차는 예측 모델을 구축한다. 4주차는 물리적 일관성, 5–6주차는 학습된 모델의 정식화와 풀이, 7주차는 최적화 활용을 위한 모델 구조 설계를 다룬다. 8주차에서 전체 과정을 연결한다. 1주차의 운전 의사결정은 과목의 도착점을 짧게 보여주는 예고다.

현재 syllabus와 [1주차]({{ '/courses/surrogate-models/week-01/' | relative_url }})–[3주차]({{ '/courses/surrogate-models/week-03/' | relative_url }}) 자료를 제공한다. 4–8주차는 강의 계획이다.

## 주차별 읽기 안내

| 주차 | 읽기 범위 |
| --- | --- |
{% for week in course.weeks %}| {{ week.number }} | {{ week.reading_ko }} |
{% endfor %}

직접 제공하는 [1주차]({{ '/courses/surrogate-models/week-01-reading/' | relative_url }}), [2주차]({{ '/courses/surrogate-models/week-02-reading/' | relative_url }}), [3주차 읽기자료]({{ '/courses/surrogate-models/week-03-reading/' | relative_url }})부터 읽는다. 각 자료는 국문·영문 PDF를 제공한다. 외부 원문은 지정된 절을 읽는다. RNN/LSTM·encoder–decoder·DeepONet, 고급 formulation 증명과 긴 horizon 예제는 선택 확장이다.

## 핵심 참고자료

- **Convex optimization 기초:** S. Boyd와 L. Vandenberghe, *Convex Optimization* (2004). 2–4장의 convex set, convex function, epigraph, 최적화 문제 관련 내용을 읽고, duality와 KKT는 5장으로 돌아온다. [공식 교재·다운로드](https://web.stanford.edu/~boyd/cvxbook/) · [EE364a 슬라이드](https://web.stanford.edu/class/ee364a/lectures.html).
- **신경망 구현:** PyTorch tutorial의 [모델 구성](https://docs.pytorch.org/tutorials/beginner/basics/buildmodel_tutorial.html), [autograd](https://docs.pytorch.org/tutorials/beginner/basics/autogradqs_tutorial.html), [학습](https://docs.pytorch.org/tutorials/beginner/basics/optimization_tutorial.html).
- **ICNN/PICNN:** B. Amos, L. Xu, J. Z. Kolter, *Input Convex Neural Networks*, ICML (2017). 3절은 구조 조건, Supplement B는 ReLU/linear unit의 LP inference를 설명한다. [논문](https://proceedings.mlr.press/v70/amos17b.html) · [PDF](https://proceedings.mlr.press/v70/amos17b/amos17b.pdf) · [Supplement](https://proceedings.mlr.press/v70/amos17b/amos17b-supp.pdf).
- **ReLU formulation:** R. Anderson, J. Huchette, W. Ma, C. Tjandraatmadja, J. P. Vielma, *Strong mixed-integer programming formulations for trained neural networks*, Mathematical Programming (2020). 공개 원고는 2018년 처음 제출되었고 2020년 수정되었다. [공개 원고](https://arxiv.org/abs/1811.01988).
- **Embedding 소프트웨어:** F. Ceccon, J. Jalving, J. Haddad, A. Thebelt, C. Tsay, C. D. Laird, R. Misener, *OMLT: Optimization & Machine Learning Toolkit*, JMLR 23(349), 1–8 (2022). [논문·PDF](https://jmlr.org/papers/v23/22-0277.html) · [코드](https://github.com/cog-imperial/OMLT) · [문서](https://omlt.readthedocs.io/en/stable/).
- **PINN:** M. Raissi, P. Perdikaris, G. E. Karniadakis, *Physics-informed neural networks: A deep learning framework for solving forward and inverse problems involving nonlinear partial differential equations*, Journal of Computational Physics 378, 686–707 (2019). [정식 논문](https://doi.org/10.1016/j.jcp.2018.10.045). 관련 2017년 Part I 원고는 공개 입문 자료로 활용한다. 최종 학술지 논문과 동일한 버전은 아니다. [2017 Part I](https://arxiv.org/abs/1711.10561).
- **KKT-hPINN:** H. Chen, G. E. Constante Flores, C. Li, *Physics-informed neural networks with hard linear equality constraints*, Computers & Chemical Engineering 189, 108764 (2024). [정식 논문](https://doi.org/10.1016/j.compchemeng.2024.108764) · [공개 원고](https://arxiv.org/abs/2402.07251) · [코드·데이터](https://github.com/li-group/KKThPINN).
- **Sequence learning 기초:** I. Sutskever, O. Vinyals, Q. V. Le, *Sequence to Sequence Learning with Neural Networks*, NeurIPS (2014). 원 논문의 응용은 번역이며, 이 강의의 공정 궤적 실습은 별도로 만든 교육 예제다. [논문](https://proceedings.neurips.cc/paper_files/paper/2014/hash/5a18e133cbf9f257297f410bb7eca942-Abstract.html).

선택 확장: 입력 함수에서 출력 함수로의 mapping을 다루는 [DeepONet, Nature Machine Intelligence (2021)](https://www.nature.com/articles/s42256-021-00302-5); 비선형 등식·부등식 projection을 다루는 [KKT-Hardnet 공개 원고(2025), C&CE 출판(2026)](https://arxiv.org/abs/2507.08124).

## 공정 예제와 소프트웨어

1주차는 작은 이상적 등온 CSTR, 기준 모델로 생성한 데이터, quadratic 회귀 baseline을 사용한다. 2주차는 A → B → C와 정상상태 MLP로 확장한다. 3주차의 공통 동적 예제는 상태전이와 rollout이다. Aspen이나 플랜트 데이터 없이 실행할 수 있는 교육 모델이며, 산업용 simulator의 계산 비용이나 fidelity를 입증하지 않는다.

4주차는 residual loss와 일관된 선형 등식을 다룬다. 공개 KKT-hPINN 데이터는 별도의 연구 재현 실습이다. 5–6주차는 고정된 ReLU predictor를 최적화에 재사용한다. 7주차는 알려진 convex target의 별도 예제에서 convexity와 LP 동치성을 먼저 확인한다. ICNN 근사 함수가 convex라는 사실이 실제 CSTR나 flowsheet의 모든 출력이 convex라는 뜻은 아니다.

1주차에는 Python·NumPy·Matplotlib, 2주차에는 PyTorch가 필요하다. 이후 Pyomo/OMLT와 적절한 solver를 소개한다. 1주차 스크립트의 기본 실행은 예측 실습이며, `--extensions`로 기존 운전점 선택·동적 예제를 후반부 학습용으로 실행할 수 있다.

## 이 과목에서 exact와 hard가 뜻하는 것

- **Exact embedding:** 명시한 영역에서 학습 후 고정된 함수를 표현한다. 물리 공정에 대한 근사 오차를 없애지 않는다. 전체 문제가 MILP인지는 나머지 목적함수와 제약에도 달려 있다.
- **LP reformulation:** ReLU/linear ICNN 구조, 고정된 PICNN context, 유효한 비음수 전파, 적절한 epigraph 사용이 필요하다. 임의의 출력 등식, 반대 방향 부등식, smooth activation, 추가 비선형 제약은 LP라는 주장을 무효화할 수 있다.
- **Hard constraint:** KKT-hPINN은 행렬 가정하에서 명시된 일관된 선형 등식을 수치 연산 오차 범위에서 만족시킨다. 양수성, 비선형 열역학, 안정성, 모든 운전 한계를 자동으로 만족시키지는 않는다.
- **Physics-informed 모델의 최적화 활용:** 학습 loss가 고정된 predictor의 대수적 종류를 결정하지 않는다. ReLU backbone에 고정 affine 등식 projection을 붙이면 piecewise affine 구조를 유지한다. Smooth 또는 비선형 projection은 필요한 formulation을 바꿀 수 있다.

## 연습문제와 종합 프로젝트

1주차는 예측 문제 정의·학습한 baseline·독립 test 평가를 제출한다. 2주차는 정상상태 MLP·손 계산으로 확인한 gradient 갱신·성분별 오차와 일관성 진단을 제출한다. 이후 주차마다 확인된 요소 하나씩을 연결한다.

최종 프로젝트에는 영역·데이터 분할·모델 구조·고정 가중치·scaling·정식화 가정·solver 종료 상태·기준 공정을 명시한다. 독립 데이터의 예측 오차, 물리적 일관성, 정식화의 일치성, 선택한 운전 조건의 품질을 구분해 평가한다. 경제성은 기준 모델로 비교한다. Grid나 local solver를 기준으로 사용했다면 그 이름을 정확히 쓰며 인증된 공정 전역 최적해라고 부르지 않는다.

수리적 정확성, 재현성, 의사결정 품질의 근거, 남은 오차·feasibility에 대한 정확한 보고를 평가한다. 실패한 운전점이나 미완료 solve도 보고할 수 있는 결과다.
