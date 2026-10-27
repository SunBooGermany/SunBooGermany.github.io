---
layout: course-note
title: "Syllabus: Surrogate Modeling for Process Prediction and Optimal Decision-Making"
title_ko: "강의계획서: 공정 예측과 최적 의사결정을 위한 서로게이트 모델링"
description: "Build validated process predictors, learn optimization formulations and model structures, then select and revalidate operating conditions."
description_ko: "공정 예측 모델을 학습·검증하고, 최적화 정식화와 모델 구조를 배운 뒤 운전 조건을 선택하고 재검증하는 8주 과정입니다."
material_label: "Syllabus"
material_label_ko: "강의 계획"
permalink: /courses/surrogate-models/syllabus/
pdf_en: /assets/courses/surrogate-models/syllabus-en.pdf
pdf_ko: /assets/courses/surrogate-models/syllabus-ko.pdf
course_id: "surrogate-models"
---

## Course purpose

Define inputs and outputs, fit a surrogate to process-response data, and validate its predictions under independent conditions. Then assess physical consistency, represent the learned function in an optimization problem, and select operating conditions for revalidation with the reference process model.

The course covers both formulating an already-trained model for optimization and designing a model structure for that use. Prediction error, physical consistency, formulation agreement, and decision quality are evaluated separately.

Sunwoo Kim designed this eight-week, self-paced course for chemical engineers entering graduate study. Original explanations, worked readings, and runnable examples accompany verified research sources.

## Audience and prerequisites

Basic Python, derivatives, matrix operations, linear algebra, and material balances are expected. LP/MILP, convexity, and KKT conditions are introduced when needed, so prior neural-network or mathematical-programming research experience is not required.

The recommended weekly workload is 90 minutes of theory, 60–90 minutes of guided coding, and 2–3 hours of reading or exercises.

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

## Reading assignments

| Week | Reading guidance |
| --- | --- |
{% for week in course.weeks %}| {{ week.number }} | {{ week.reading }} |
{% endfor %}

## Core sources

- Convex optimization background: S. Boyd and L. Vandenberghe, *Convex Optimization* (2004). Read selected parts of Chapters 2–4 for convex sets, convex functions, epigraphs, and optimization problems; return to Chapter 5 for duality and KKT. [Official book and downloads](https://web.stanford.edu/~boyd/cvxbook/) · [EE364a slides](https://web.stanford.edu/class/ee364a/lectures.html).
- Neural-network implementation: PyTorch tutorials on [model construction](https://docs.pytorch.org/tutorials/beginner/basics/buildmodel_tutorial.html), [autograd](https://docs.pytorch.org/tutorials/beginner/basics/autogradqs_tutorial.html), and [training](https://docs.pytorch.org/tutorials/beginner/basics/optimization_tutorial.html).
- ICNN/PICNN: B. Amos, L. Xu, and J. Z. Kolter, *Input Convex Neural Networks*, ICML (2017). Section 3 gives architecture conditions; Supplement B gives LP inference for ReLU/linear units. [Paper](https://proceedings.mlr.press/v70/amos17b.html) · [PDF](https://proceedings.mlr.press/v70/amos17b/amos17b.pdf) · [Supplement](https://proceedings.mlr.press/v70/amos17b/amos17b-supp.pdf).
- ReLU formulations: R. Anderson, J. Huchette, W. Ma, C. Tjandraatmadja, and J. P. Vielma, *Strong mixed-integer programming formulations for trained neural networks*, Mathematical Programming (2020). The public manuscript was first submitted in 2018 and revised in 2020. [Public manuscript](https://arxiv.org/abs/1811.01988).
- Embedding software: F. Ceccon, J. Jalving, J. Haddad, A. Thebelt, C. Tsay, C. D. Laird, and R. Misener, *OMLT: Optimization & Machine Learning Toolkit*, JMLR 23(349), 1–8 (2022). [Paper and PDF](https://jmlr.org/papers/v23/22-0277.html) · [Code](https://github.com/cog-imperial/OMLT) · [Documentation](https://omlt.readthedocs.io/en/stable/).
- PINN: M. Raissi, P. Perdikaris, and G. E. Karniadakis, *Physics-informed neural networks: A deep learning framework for solving forward and inverse problems involving nonlinear partial differential equations*, Journal of Computational Physics 378, 686–707 (2019). [Published paper](https://doi.org/10.1016/j.jcp.2018.10.045). The related 2017 Part I manuscript is a freely available introduction; it is not the identical final journal version. [2017 Part I](https://arxiv.org/abs/1711.10561).
- KKT-hPINN: H. Chen, G. E. Constante Flores, and C. Li, *Physics-informed neural networks with hard linear equality constraints*, Computers & Chemical Engineering 189, 108764 (2024). [Published paper](https://doi.org/10.1016/j.compchemeng.2024.108764) · [Public manuscript](https://arxiv.org/abs/2402.07251) · [Code and datasets](https://github.com/li-group/KKThPINN).
- Sequence-learning background: I. Sutskever, O. Vinyals, and Q. V. Le, *Sequence to Sequence Learning with Neural Networks*, NeurIPS (2014). Its application is translation; our process-trajectory exercises are separate educational examples. [Paper](https://proceedings.neurips.cc/paper_files/paper/2014/hash/5a18e133cbf9f257297f410bb7eca942-Abstract.html).

Optional extensions: [DeepONet, Nature Machine Intelligence (2021)](https://www.nature.com/articles/s42256-021-00302-5), for input-function to output-function mappings; [KKT-Hardnet public manuscript (2025), published in C&CE (2026)](https://arxiv.org/abs/2507.08124), for nonlinear equality and inequality projection.

<!-- ko -->

## 과목의 목적

입력과 출력을 정의하고 데이터로 공정 응답을 예측하는 surrogate를 학습한 뒤, 독립적인 조건에서 예측을 검증합니다. 이어서 물리적 일관성을 평가하고 학습된 함수를 최적화 문제에 넣어 운전 조건을 선택한 다음, 기준 공정 모델로 재검증합니다.

이미 학습된 모델을 최적화 문제로 정식화하는 방법과 최적화 활용에 맞춰 모델 구조를 설계하는 방법을 함께 다룹니다. 예측 오차, 물리적 일관성, 정식화의 일치성, 의사결정 품질은 구분해 평가합니다.

Sunwoo Kim이 화학공학 대학원 입문자를 위해 설계한 8주 자율 학습 과정입니다. 직접 작성한 설명과 계산을 포함한 읽기자료, 실행 예제를 검증된 연구 원문과 함께 제공합니다.

## 수강 대상과 선수 지식

Python 기초, 미분, 행렬 연산, 선형대수, 물질수지 지식을 전제로 합니다. LP/MILP, convexity, KKT 조건은 필요한 시점에 설명하므로 신경망이나 수리계획 연구 경험은 없어도 됩니다.

주당 이론 90분, 안내된 실습 60–90분, 읽기·연습문제 2–3시간을 권장합니다.

## 학습 목표

과정을 마치면 다음 작업을 수행할 수 있어야 합니다.

1. 공정 예측 문제의 입력·출력·고정 context·상태·단위·데이터 분할·유효한 영역을 정의합니다.
2. 정상상태·동적 surrogate를 학습하고, 독립 데이터와 정해진 미래 입력으로 성분별·궤적 예측 오차를 평가합니다.
3. 일반 모델, soft physics 모델, hard 선형 등식 모델을 비교하고 예측 정확도와 물리적 일관성을 구분합니다.
4. 조작변수·목적함수·제약을 정의하고, 고정된 ReLU 모델의 유효한 MILP 표현을 작성해 forward 출력과 대조합니다.
5. 활용 목적에 맞는 모델 구조와 정식화를 선택하고, ReLU ICNN/PICNN epigraph가 동치인 LP 문제를 허용하는 조건을 확인합니다.
6. Surrogate 기반 운전 최적화를 풀고 기준 공정 모델의 제약 만족·경제성·solver 종료 상태·gap·시간을 각각 보고합니다.

## 8주 구성

| 주차 | 주제와 범위 | 필수 결과물 |
| --- | --- | --- |
{% for week in course.weeks %}| {{ week.number }} | **{{ week.title_ko }}.** {{ week.topics_ko }} | {{ week.deliverable_ko }} |
{% endfor %}

## 주차별 읽기 안내

| 주차 | 읽기 범위 |
| --- | --- |
{% for week in course.weeks %}| {{ week.number }} | {{ week.reading_ko }} |
{% endfor %}

## 핵심 참고자료

- Convex optimization 기초: S. Boyd와 L. Vandenberghe, *Convex Optimization* (2004). 2–4장의 convex set, convex function, epigraph, 최적화 문제 관련 내용을 읽고 duality와 KKT는 5장을 참고합니다. [공식 교재·다운로드](https://web.stanford.edu/~boyd/cvxbook/) · [EE364a 슬라이드](https://web.stanford.edu/class/ee364a/lectures.html).
- 신경망 구현: PyTorch tutorial의 [모델 구성](https://docs.pytorch.org/tutorials/beginner/basics/buildmodel_tutorial.html), [autograd](https://docs.pytorch.org/tutorials/beginner/basics/autogradqs_tutorial.html), [학습](https://docs.pytorch.org/tutorials/beginner/basics/optimization_tutorial.html).
- ICNN/PICNN: B. Amos, L. Xu, J. Z. Kolter, *Input Convex Neural Networks*, ICML (2017). 3절은 구조 조건, Supplement B는 ReLU/linear unit의 LP inference를 설명합니다. [논문](https://proceedings.mlr.press/v70/amos17b.html) · [PDF](https://proceedings.mlr.press/v70/amos17b/amos17b.pdf) · [Supplement](https://proceedings.mlr.press/v70/amos17b/amos17b-supp.pdf).
- ReLU formulation: R. Anderson, J. Huchette, W. Ma, C. Tjandraatmadja, J. P. Vielma, *Strong mixed-integer programming formulations for trained neural networks*, Mathematical Programming (2020). 공개 원고는 2018년 처음 제출되었고 2020년 수정되었습니다. [공개 원고](https://arxiv.org/abs/1811.01988).
- Embedding 소프트웨어: F. Ceccon, J. Jalving, J. Haddad, A. Thebelt, C. Tsay, C. D. Laird, R. Misener, *OMLT: Optimization & Machine Learning Toolkit*, JMLR 23(349), 1–8 (2022). [논문·PDF](https://jmlr.org/papers/v23/22-0277.html) · [코드](https://github.com/cog-imperial/OMLT) · [문서](https://omlt.readthedocs.io/en/stable/).
- PINN: M. Raissi, P. Perdikaris, G. E. Karniadakis, *Physics-informed neural networks: A deep learning framework for solving forward and inverse problems involving nonlinear partial differential equations*, Journal of Computational Physics 378, 686–707 (2019). [정식 논문](https://doi.org/10.1016/j.jcp.2018.10.045). 관련 2017년 Part I 원고는 공개 입문 자료로 활용하며, 최종 학술지 논문과는 버전이 다릅니다. [2017 Part I](https://arxiv.org/abs/1711.10561).
- KKT-hPINN: H. Chen, G. E. Constante Flores, C. Li, *Physics-informed neural networks with hard linear equality constraints*, Computers & Chemical Engineering 189, 108764 (2024). [정식 논문](https://doi.org/10.1016/j.compchemeng.2024.108764) · [공개 원고](https://arxiv.org/abs/2402.07251) · [코드·데이터](https://github.com/li-group/KKThPINN).
- Sequence learning 기초: I. Sutskever, O. Vinyals, Q. V. Le, *Sequence to Sequence Learning with Neural Networks*, NeurIPS (2014). 원 논문은 번역을 다루며, 이 강의의 공정 궤적 실습은 별도로 만든 교육 예제입니다. [논문](https://proceedings.neurips.cc/paper_files/paper/2014/hash/5a18e133cbf9f257297f410bb7eca942-Abstract.html).

선택 확장: 입력 함수를 출력 함수로 매핑하는 [DeepONet, Nature Machine Intelligence (2021)](https://www.nature.com/articles/s42256-021-00302-5); 비선형 등식·부등식 projection을 다루는 [KKT-Hardnet 공개 원고(2025), C&CE 출판(2026)](https://arxiv.org/abs/2507.08124).
