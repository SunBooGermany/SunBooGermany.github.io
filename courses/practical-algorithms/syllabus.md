---
layout: "course-note"
title: "Syllabus: Practical Data Structures and Algorithms"
title_ko: "강의계획서: 실무 자료구조와 알고리즘"
description: "Choose data structures, write Python solutions to LeetCode problems, and evaluate correctness and computational cost."
description_ko: "자료구조를 선택하고 LeetCode 문제의 Python 풀이를 작성하며 정확성과 계산 비용을 평가하는 8주 과정입니다."
material_label: "Syllabus"
material_label_ko: "강의 계획"
syllabus_style: "monochrome"
permalink: "/courses/practical-algorithms/syllabus/"
pdf_en: "/assets/courses/practical-algorithms/syllabus-en.pdf"
pdf_ko: "/assets/courses/practical-algorithms/syllabus-ko.pdf"
course_id: "practical-algorithms"
---

## Course purpose

Define the inputs and required operations of a problem, choose a data structure, and write a Python solution. Trace the execution on small examples, check boundary cases, and evaluate how time and memory use change with input size.

LeetCode problems provide practice in searching, grouping, processing sequences, and following dependencies. Correctness, computational cost, and the conditions required to reuse a method in a work task are assessed separately.

Sunwoo Kim designed this eight-week, self-paced course for learners without a computer science background. Original explanations, worked readings, and Python solutions accompany official problem statements and documentation.

## Audience and prerequisites

The course is for researchers, engineers, and analysts who need to process data or automate tasks. Basic Python variables, conditionals, loops, and functions are expected. Node references, recursion, and complexity notation are introduced when needed; prior algorithms study and advanced mathematics are not required.

## Learning outcomes

By the end of the course, learners should be able to:

1. Define a problem's inputs, outputs, allowed operations, and constraints.
2. Choose lists, dictionaries, sets, stacks, queues, or heaps for the required operations.
3. Write and trace Python solutions using search, traversal, greedy rules, and one- and two-dimensional dynamic programming.
4. Explain time and space costs, accounting for sorting, copying, and recursive calls where relevant.
5. Check boundary cases and compare results with a simple reference solution on small inputs.
6. Identify the assumptions of a solution and revise its input handling and tests before applying it to work data.

## Eight-week sequence

{% assign course = site.data.courses | where: 'id', page.course_id | first %}

| Week | Topic and scope | Required output |
| --- | --- | --- |
{% for week in course.weeks %}| {{ week.number }} | **{{ week.title }}.** {{ week.topics }} | {{ week.deliverable }} |
{% endfor %}

## Core sources

- Erik Demaine and Srini Devadas, [Introduction to Algorithms, MIT 6.006](https://ocw.mit.edu/courses/6-006-introduction-to-algorithms-fall-2011/) (Fall 2011).

<!-- ko -->

## 과목의 목적

문제의 입력과 필요한 연산을 정의하고 자료구조를 선택한 뒤 Python 풀이를 작성합니다. 작은 예제로 실행 과정을 추적하고 경계 조건을 확인하며, 입력 크기에 따라 시간과 메모리 사용량이 어떻게 달라지는지 평가합니다.

LeetCode 문제로 탐색·그룹화·순차 데이터 처리·의존관계 분석을 연습합니다. 풀이의 정확성, 계산 비용, 업무에 같은 방법을 적용하기 위한 조건은 구분해 평가합니다.

Sunwoo Kim이 컴퓨터공학 비전공자를 위해 설계한 8주 자율 학습 과정입니다. 직접 작성한 설명과 풀이 읽기자료, Python 풀이를 공식 문제 원문·문서와 함께 제공합니다.

## 수강 대상과 선수 지식

데이터 처리와 업무 자동화가 필요한 연구자·엔지니어·분석가를 대상으로 합니다. Python 변수·조건문·반복문·함수의 기초를 전제로 합니다. 노드 참조·재귀·복잡도 표기는 필요한 시점에 설명하므로 알고리즘 수강 경험이나 고급 수학 지식은 없어도 됩니다.

## 학습 목표

과정을 마치면 다음 작업을 수행할 수 있어야 합니다.

1. 문제의 입력·출력·허용 연산·제약 조건을 정의합니다.
2. 필요한 연산에 맞춰 리스트·딕셔너리·집합·스택·큐·힙을 선택합니다.
3. 탐색·순회·탐욕법·1차원·2차원 동적 계획법을 사용한 Python 풀이를 작성하고 실행 과정을 설명합니다.
4. 정렬·복사·재귀 호출을 포함해 시간과 공간 비용을 설명합니다.
5. 경계 조건을 검사하고 작은 입력에서 단순한 기준 풀이와 결과를 비교합니다.
6. 풀이가 전제하는 조건을 확인하고 업무 데이터에 적용하기 전에 입력 처리와 검사를 조정합니다.

## 8주 구성

| 주차 | 주제와 범위 | 필수 결과물 |
| --- | --- | --- |
{% for week in course.weeks %}| {{ week.number }} | **{{ week.title_ko }}.** {{ week.topics_ko }} | {{ week.deliverable_ko }} |
{% endfor %}

## 핵심 참고자료

- Erik Demaine·Srini Devadas, [Introduction to Algorithms, MIT 6.006](https://ocw.mit.edu/courses/6-006-introduction-to-algorithms-fall-2011/) (2011년 가을 학기).
