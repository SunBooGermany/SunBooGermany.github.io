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

## Core sources

- Stephen Boyd and Lieven Vandenberghe, [*Convex Optimization*](https://web.stanford.edu/~boyd/cvxbook/) (Cambridge University Press, 2004).
- Stephen Boyd, [EE364a: Convex Optimization I — Lecture Slides](https://web.stanford.edu/class/ee364a/lectures.html), Stanford University.
- [cog-imperial/OMLT](https://github.com/cog-imperial/OMLT): Optimization and Machine Learning Toolkit.
- [li-group/KKThPINN](https://github.com/li-group/KKThPINN): KKT-hPINN code and datasets.

<!-- ko -->

## 과목의 목적

입력과 출력을 정의하고 데이터로 공정 응답을 예측하는 surrogate를 학습한 뒤, 독립적인 조건에서 예측을 검증합니다. 이어서 물리적 일관성을 평가하고 학습된 함수를 최적화 문제에 넣어 운전 조건을 선택한 다음, 기준 공정 모델로 재검증합니다.

이미 학습된 모델을 최적화 문제로 정식화하는 방법과 최적화 활용에 맞춰 모델 구조를 설계하는 방법을 함께 다룹니다. 예측 오차, 물리적 일관성, 정식화의 일치성, 의사결정 품질은 구분해 평가합니다.

Sunwoo Kim이 화학공학 대학원 입문자를 위해 설계한 8주 자율 학습 과정입니다. 직접 작성한 설명과 계산을 포함한 읽기자료, 실행 예제를 검증된 연구 원문과 함께 제공합니다.

## 수강 대상과 선수 지식

Python 기초, 미분, 행렬 연산, 선형대수, 물질수지 지식을 전제로 합니다. LP/MILP, convexity, KKT 조건은 필요한 시점에 설명하므로 신경망이나 수리계획 연구 경험은 없어도 됩니다.

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

## 핵심 참고자료

- Stephen Boyd·Lieven Vandenberghe, [*Convex Optimization*](https://web.stanford.edu/~boyd/cvxbook/) (Cambridge University Press, 2004).
- Stephen Boyd, [EE364a: Convex Optimization I — Lecture Slides](https://web.stanford.edu/class/ee364a/lectures.html), Stanford University.
- [cog-imperial/OMLT](https://github.com/cog-imperial/OMLT): Optimization and Machine Learning Toolkit.
- [li-group/KKThPINN](https://github.com/li-group/KKThPINN): KKT-hPINN 코드와 데이터.
