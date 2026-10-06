---
layout: course-note
title: "Syllabus: Surrogate Models for Process Decision-Making"
title_ko: "Syllabus: 공정 의사결정을 위한 서로게이트 모델"
description: "An eight-week graduate-entry course connecting process prediction, physics-informed learning, and optimization embedding."
description_ko: "공정 예측, physics-informed learning, 최적화 embedding을 연결하는 화학공학 대학원 입문 8주 과정입니다."
material_label: "Syllabus"
material_label_ko: "강의 계획"
updated: "2026-10-06"
permalink: /courses/surrogate-models/syllabus/
pdf_en: /assets/courses/surrogate-models/syllabus-en.pdf
pdf_ko: /assets/courses/surrogate-models/syllabus-ko.pdf
---

## Course purpose

A process surrogate approximates the response of a process model or measurements. A decision system also needs a choice of operating variables, an objective, constraints, and a way to check the selected operating point. This course connects these tasks without treating prediction accuracy as evidence of good decisions.

Designed by Sunwoo Kim as an independent, self-paced learning course for chemical engineers entering graduate study. The materials combine original explanations and exercises with cited research papers.

## Audience and prerequisites

Basic Python, derivatives, matrix operations, linear algebra, and material balances are expected. Prior neural-network or mathematical-programming research experience is not required. LP/MILP, convexity, and KKT conditions are introduced when they are needed.

Suggested weekly workload: 90 minutes of theory, 60–90 minutes of guided coding, and 2–3 hours of reading or exercises. These are study recommendations, not scheduled classes.

## Learning outcomes

By the end of the course, learners should be able to:

1. Define decision variables, fixed context, states, outputs, units, and a valid operating domain.
2. Build and evaluate steady-state vector-to-vector and dynamic sequence-to-sequence surrogates, including conditioning on future control inputs.
3. Compare data-driven, soft physics-informed, and hard linear-equality-constrained models using both prediction errors and constraint residuals.
4. Derive a valid MILP graph formulation for a frozen ReLU network and check its numerical agreement with a forward pass.
5. Explain when a ReLU ICNN/PICNN admits an LP epigraph formulation and when that formulation is not equivalent to the intended problem.
6. Report simulator revalidation, feasibility, decision quality, bounds, solver termination, and computation time separately.

## Eight-week sequence

{% assign course = site.data.courses | where: 'id', 'surrogate-models' | first %}

| Week | Topic and scope | Required output |
| --- | --- | --- |
{% for week in course.weeks %}| {{ week.number }} | **{{ week.title }}.** {{ week.topics }} | {{ week.deliverable }} |
{% endfor %}

Weeks 2–4 focus on building and evaluating models. Weeks 5–7 focus on optimization embedding. Week 8 joins the two parts. The syllabus and [Week 1]({{ '/courses/surrogate-models/week-01/' | relative_url }}) are available now; Weeks 2–8 describe planned content and do not yet have released lecture notes.

## Reading assignments

| Week | Reading guidance |
| --- | --- |
{% for week in course.weeks %}| {{ week.number }} | {{ week.reading }} |
{% endfor %}

The reading list is for selected sections, not six full-paper assignments each week. Advanced formulation proofs and operator-learning extensions are optional.

## Core sources

- **Convex optimization background:** S. Boyd and L. Vandenberghe, *Convex Optimization* (2004). Read selected parts of Chapters 2–4 for convex sets, convex functions, epigraphs, and optimization problems; return to Chapter 5 for duality and KKT. [Official book and downloads](https://web.stanford.edu/~boyd/cvxbook/) · [EE364a slides](https://web.stanford.edu/class/ee364a/lectures.html).
- **ICNN/PICNN:** B. Amos, L. Xu, and J. Z. Kolter, *Input Convex Neural Networks*, ICML (2017). Section 3 gives architecture conditions; Supplement B gives LP inference for ReLU/linear units. [Paper](https://proceedings.mlr.press/v70/amos17b.html) · [PDF](https://proceedings.mlr.press/v70/amos17b/amos17b.pdf) · [Supplement](https://proceedings.mlr.press/v70/amos17b/amos17b-supp.pdf).
- **ReLU formulations:** R. Anderson, J. Huchette, W. Ma, C. Tjandraatmadja, and J. P. Vielma, *Strong mixed-integer programming formulations for trained neural networks*, Mathematical Programming (2020). The public manuscript was first submitted in 2018 and revised in 2020. [Public manuscript](https://arxiv.org/abs/1811.01988).
- **Embedding software:** F. Ceccon, J. Jalving, J. Haddad, A. Thebelt, C. Tsay, C. D. Laird, and R. Misener, *OMLT: Optimization & Machine Learning Toolkit*, JMLR 23(349), 1–8 (2022). [Paper and PDF](https://jmlr.org/papers/v23/22-0277.html) · [Code](https://github.com/cog-imperial/OMLT) · [Documentation](https://omlt.readthedocs.io/en/stable/).
- **PINN:** M. Raissi, P. Perdikaris, and G. E. Karniadakis, *Physics-informed neural networks: A deep learning framework for solving forward and inverse problems involving nonlinear partial differential equations*, Journal of Computational Physics 378, 686–707 (2019). [Published paper](https://doi.org/10.1016/j.jcp.2018.10.045). The related 2017 Part I manuscript is a freely available introduction; it is not the identical final journal version. [2017 Part I](https://arxiv.org/abs/1711.10561).
- **KKT-hPINN:** H. Chen, G. E. Constante Flores, and C. Li, *Physics-informed neural networks with hard linear equality constraints*, Computers & Chemical Engineering 189, 108764 (2024). [Published paper](https://doi.org/10.1016/j.compchemeng.2024.108764) · [Public manuscript](https://arxiv.org/abs/2402.07251) · [Code and datasets](https://github.com/li-group/KKThPINN).
- **Sequence-learning background:** I. Sutskever, O. Vinyals, and Q. V. Le, *Sequence to Sequence Learning with Neural Networks*, NeurIPS (2014). Its application is translation; our process-trajectory exercises are separate educational examples. [Paper](https://proceedings.neurips.cc/paper_files/paper/2014/hash/5a18e133cbf9f257297f410bb7eca942-Abstract.html).

Optional extensions: [DeepONet, Nature Machine Intelligence (2021)](https://www.nature.com/articles/s42256-021-00302-5), for input-function to output-function mappings; [KKT-Hardnet public manuscript (2025), published in C&CE (2026)](https://arxiv.org/abs/2507.08124), for nonlinear equality and inequality projection.

## Process examples and software

The main educational example is a small isothermal CSTR with a first-order reaction. Week 1 supplies its equations, synthetic parameters, steady-state map, and dynamic simulation. It can be run without Aspen or a plant dataset. The public KKT-hPINN datasets provide a separate research-reproduction exercise; they are not generated by our teaching simulator.

Convexity and LP equivalence are first checked on a separate example with a known convex target. Convexity of an ICNN approximation does not establish convexity of an actual CSTR or of every output of a flowsheet.

Week 1 requires Python, NumPy, and Matplotlib. Later materials will introduce PyTorch and Pyomo/OMLT with a suitable solver. A notebook and a standalone Python script are both supplied so that Jupyter is optional for the first lab.

## What “exact” and “hard” mean here

- **Exact embedding:** a formulation represents the frozen learned function over the stated domain. It does not remove approximation error relative to the physical process. MILP status also depends on the rest of the objective and constraints.
- **LP reformulation:** ReLU/linear ICNN structure, fixed PICNN context, valid nonnegative propagation, and appropriate epigraph usage matter. Arbitrary output equalities, reversed inequalities, smooth activations, or additional nonlinear constraints can invalidate an LP claim.
- **Hard constraints:** KKT-hPINN enforces the specified consistent linear equalities under its matrix assumptions, up to numerical arithmetic. It does not automatically enforce positivity, nonlinear thermodynamics, stability, or every operating limit.
- **Optimization with physics-informed models:** training losses do not determine the algebraic class of the frozen predictor. A ReLU backbone followed by a fixed affine equality projection remains piecewise affine; a smooth or nonlinear projection can change the required formulation.

## Exercises and final project

Each week pairs a derivation or problem specification with an executable check. The final report should state the data domain, split method, model architecture, frozen weights, scaling, formulation assumptions, solver and termination status, and simulator used for revalidation.

Evaluate prediction error and constraint violations at held-out points and at selected decisions. Compare economic performance using the reference process model. If a grid or local solver is the benchmark, call it a grid or local benchmark; do not call it a certified global process optimum.

For self-study, assess the final project on four dimensions: correctness of the mathematical formulation, reproducibility, evidence about decision quality, and honesty about unresolved error or feasibility. An incomplete solve or a failed operating point is useful evidence when it is reported accurately.

<!-- ko -->

## 과목의 목적

공정 surrogate는 공정 모델이나 측정값의 입력–출력 관계를 근사한다. 의사결정 시스템에는 조작변수, 목적함수, 제약, 그리고 선택한 운전점을 검증하는 절차도 필요하다. 이 과목은 예측 정확도만으로 좋은 의사결정을 주장하지 않고, 이 과정을 연결해 공부한다.

Sunwoo Kim이 화학공학 대학원 입문자를 위해 직접 구성한 독립적인 자율 학습 과정이다. 직접 작성한 설명과 연습문제를 인용한 연구 논문에 연결한다.

## 수강 대상과 선수 지식

Python 기초, 미분, 행렬 연산, 선형대수, 물질수지를 알고 있다고 가정한다. 신경망이나 수리계획 연구 경험은 요구하지 않는다. LP/MILP, convexity, KKT 조건은 필요한 시점에 설명한다.

권장 주간 학습량은 이론 90분, 안내된 실습 60–90분, 읽기·연습문제 2–3시간이다. 실제 수업 시간표가 아니라 자율 학습을 위한 제안이다.

## 학습 목표

과정을 마친 뒤에는 다음을 할 수 있어야 한다.

1. 의사결정 변수, 고정 context, 상태, 출력, 단위, 유효한 운전 영역을 정의한다.
2. 미래 조작변수 계획을 입력으로 받는 모델을 포함해 정상상태 vector-to-vector와 동적 sequence-to-sequence surrogate를 구축하고 평가한다.
3. 데이터 기반, soft physics-informed, hard 선형 등식 제약 모델을 예측 오차와 제약 residual로 각각 비교한다.
4. 학습 후 고정된 ReLU 신경망의 유효한 MILP graph formulation을 유도하고 forward 출력과 수치적으로 대조한다.
5. ReLU ICNN/PICNN의 LP epigraph formulation이 가능한 조건과 원래 문제와 동치가 아닌 경우를 설명한다.
6. 공정 모델 재검증, feasibility, 의사결정 품질, bounds, solver 종료 상태, 계산 시간을 각각 보고한다.

## 8주 구성

| 주차 | 주제와 범위 | 결과물 |
| --- | --- | --- |
{% for week in course.weeks %}| {{ week.number }} | **{{ week.title_ko }}.** {{ week.topics_ko }} | {{ week.deliverable_ko }} |
{% endfor %}

2–4주차는 모델 구축과 평가, 5–7주차는 최적화 embedding에 집중한다. 8주차에서 두 부분을 연결한다. 현재 syllabus와 [1주차]({{ '/courses/surrogate-models/week-01/' | relative_url }})를 공개했다. 2–8주차는 강의 계획이며 해당 주차의 강의 노트는 아직 공개하지 않았다.

## 주차별 읽기 안내

| 주차 | 읽기 범위 |
| --- | --- |
{% for week in course.weeks %}| {{ week.number }} | {{ week.reading_ko }} |
{% endfor %}

지정된 절을 읽는 방식이다. 매주 여러 논문 전체를 읽도록 요구하지 않는다. 고급 formulation 증명과 operator learning 확장은 선택 내용이다.

## 핵심 참고자료

- **Convex optimization 기초:** S. Boyd와 L. Vandenberghe, *Convex Optimization* (2004). 2–4장의 convex set, convex function, epigraph, 최적화 문제 관련 내용을 읽고, duality와 KKT는 5장으로 돌아온다. [공식 교재·다운로드](https://web.stanford.edu/~boyd/cvxbook/) · [EE364a 슬라이드](https://web.stanford.edu/class/ee364a/lectures.html).
- **ICNN/PICNN:** B. Amos, L. Xu, J. Z. Kolter, *Input Convex Neural Networks*, ICML (2017). 3절은 구조 조건, Supplement B는 ReLU/linear unit의 LP inference를 설명한다. [논문](https://proceedings.mlr.press/v70/amos17b.html) · [PDF](https://proceedings.mlr.press/v70/amos17b/amos17b.pdf) · [Supplement](https://proceedings.mlr.press/v70/amos17b/amos17b-supp.pdf).
- **ReLU formulation:** R. Anderson, J. Huchette, W. Ma, C. Tjandraatmadja, J. P. Vielma, *Strong mixed-integer programming formulations for trained neural networks*, Mathematical Programming (2020). 공개 원고는 2018년 처음 제출되었고 2020년 수정되었다. [공개 원고](https://arxiv.org/abs/1811.01988).
- **Embedding 소프트웨어:** F. Ceccon, J. Jalving, J. Haddad, A. Thebelt, C. Tsay, C. D. Laird, R. Misener, *OMLT: Optimization & Machine Learning Toolkit*, JMLR 23(349), 1–8 (2022). [논문·PDF](https://jmlr.org/papers/v23/22-0277.html) · [코드](https://github.com/cog-imperial/OMLT) · [문서](https://omlt.readthedocs.io/en/stable/).
- **PINN:** M. Raissi, P. Perdikaris, G. E. Karniadakis, *Physics-informed neural networks: A deep learning framework for solving forward and inverse problems involving nonlinear partial differential equations*, Journal of Computational Physics 378, 686–707 (2019). [정식 논문](https://doi.org/10.1016/j.jcp.2018.10.045). 관련 2017년 Part I 원고는 공개 입문 자료로 활용한다. 최종 학술지 논문과 동일한 버전은 아니다. [2017 Part I](https://arxiv.org/abs/1711.10561).
- **KKT-hPINN:** H. Chen, G. E. Constante Flores, C. Li, *Physics-informed neural networks with hard linear equality constraints*, Computers & Chemical Engineering 189, 108764 (2024). [정식 논문](https://doi.org/10.1016/j.compchemeng.2024.108764) · [공개 원고](https://arxiv.org/abs/2402.07251) · [코드·데이터](https://github.com/li-group/KKThPINN).
- **Sequence learning 기초:** I. Sutskever, O. Vinyals, Q. V. Le, *Sequence to Sequence Learning with Neural Networks*, NeurIPS (2014). 원 논문의 응용은 번역이며, 이 강의의 공정 궤적 실습은 별도로 만든 교육 예제다. [논문](https://proceedings.neurips.cc/paper_files/paper/2014/hash/5a18e133cbf9f257297f410bb7eca942-Abstract.html).

선택 확장: 입력 함수에서 출력 함수로의 mapping을 다루는 [DeepONet, Nature Machine Intelligence (2021)](https://www.nature.com/articles/s42256-021-00302-5); 비선형 등식·부등식 projection을 다루는 [KKT-Hardnet 공개 원고(2025), C&CE 출판(2026)](https://arxiv.org/abs/2507.08124).

## 공정 예제와 소프트웨어

주요 교육 예제는 1차 반응을 갖는 작은 등온 CSTR이다. 1주차에 지배식, 교육용 가상 파라미터, 정상상태 mapping, 동적 시뮬레이션을 제공한다. Aspen이나 플랜트 데이터 없이 실행할 수 있다. 공개 KKT-hPINN 데이터는 별도의 연구 재현 실습에 활용하며, 이 강의의 교육용 simulator가 생성한 데이터와 구분한다.

Convexity와 LP 동치성은 convex target이 알려진 별도 예제에서 먼저 확인한다. ICNN 근사 함수가 convex라는 사실이 실제 CSTR나 flowsheet의 모든 출력이 convex라는 뜻은 아니다.

1주차에는 Python, NumPy, Matplotlib이 필요하다. 이후 PyTorch, Pyomo/OMLT와 적절한 solver를 소개한다. 첫 실습은 notebook과 독립 Python 스크립트를 함께 제공하므로 Jupyter가 필수는 아니다.

## 이 과목에서 exact와 hard가 뜻하는 것

- **Exact embedding:** 명시한 영역에서 학습 후 고정된 함수를 표현한다. 물리 공정에 대한 근사 오차를 없애지 않는다. 전체 문제가 MILP인지는 나머지 목적함수와 제약에도 달려 있다.
- **LP reformulation:** ReLU/linear ICNN 구조, 고정된 PICNN context, 유효한 비음수 전파, 적절한 epigraph 사용이 필요하다. 임의의 출력 등식, 반대 방향 부등식, smooth activation, 추가 비선형 제약은 LP라는 주장을 무효화할 수 있다.
- **Hard constraint:** KKT-hPINN은 행렬 가정하에서 명시된 일관된 선형 등식을 수치 연산 오차 범위에서 만족시킨다. 양수성, 비선형 열역학, 안정성, 모든 운전 한계를 자동으로 만족시키지는 않는다.
- **Physics-informed 모델의 최적화 활용:** 학습 loss가 고정된 predictor의 대수적 종류를 결정하지 않는다. ReLU backbone에 고정 affine 등식 projection을 붙이면 piecewise affine 구조를 유지한다. Smooth 또는 비선형 projection은 필요한 formulation을 바꿀 수 있다.

## 연습문제와 종합 프로젝트

매주 수식 유도 또는 문제 정의를 실행 가능한 확인 절차에 연결한다. 최종 보고서에는 데이터 영역, 분할 방법, 모델 구조, 고정된 가중치, scaling, formulation 가정, solver·종료 상태, 재검증용 simulator를 명시한다.

독립 평가점과 선택한 의사결정 지점 모두에서 예측 오차와 제약 위반을 평가한다. 경제성은 기준 공정 모델로 비교한다. Grid나 local solver를 기준으로 사용했다면 grid 또는 local benchmark라고 쓰며, 인증된 공정 전역 최적해라고 부르지 않는다.

자율 학습에서는 수리 formulation의 정확성, 재현성, 의사결정 품질의 근거, 남은 오차·feasibility 문제에 대한 정확한 보고로 프로젝트를 평가한다. 미완료 solve나 실패한 운전점도 정확하게 보고하면 유용한 근거가 된다.
