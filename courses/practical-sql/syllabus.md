---
layout: "course-note"
title: "Syllabus: Practical SQL for Data Analysis and Applications"
title_ko: "강의계획서: 데이터 분석과 업무 활용을 위한 실무 SQL"
description: "Define the meaning of each row, write queries across related tables, and verify results before using SQL in an application."
description_ko: "각 행의 의미를 정의하고 여러 테이블을 다루는 SQL을 작성한 뒤 결과를 검증해 업무에 적용하는 8주 과정입니다."
material_label: "Syllabus"
material_label_ko: "강의 계획"
syllabus_style: "monochrome"
permalink: "/courses/practical-sql/syllabus/"
pdf_en: "/assets/courses/practical-sql/syllabus-en.pdf"
pdf_ko: "/assets/courses/practical-sql/syllabus-ko.pdf"
course_id: "practical-sql"
---

## Course purpose

Define a data question and the meaning of each result row, write a query, and check the output against manually verified examples. Progress from filtering and aggregation to joins, staged queries, and window functions, then examine data changes, query plans, and application use.

The course emphasizes matching the grains of related tables and checking intermediate results. Query correctness, duplicate or missing records, execution cost, and transaction behavior are evaluated separately.

Sunwoo Kim designed this eight-week, self-paced course for learners without a computer science background. Original explanations and worked readings present the schema, example data, query, and expected result together, alongside official documentation.

## Audience and prerequisites

The course is for researchers, engineers, and analysts who need to retrieve and summarize table-based data. Familiarity with spreadsheet rows and columns is expected. Schema, keys, and relationships are introduced before multi-table queries. Prior programming and database coursework are not required; the Python examples used to connect SQL to an application are explained when introduced.

## Learning outcomes

By the end of the course, learners should be able to:

1. Read a schema and identify each table's grain, keys, and relationships.
2. Write filtering, aggregation, and conditional-summary queries with a defined treatment of missing values.
3. Join tables at compatible grains and check row counts, totals, and unmatched records.
4. Structure composite conditions with subqueries, CTEs, and existence checks; inspect the result of each stage.
5. Use window functions with explicit partitions, event order, tie handling, and relevant frame boundaries.
6. Check data changes and rollback behavior, compare query plans, and call parameterized SQL from a program.

## Eight-week sequence

{% assign course = site.data.courses | where: 'id', page.course_id | first %}

| Week | Topic and scope | Required output |
| --- | --- | --- |
{% for week in course.weeks %}| {{ week.number }} | **{{ week.title }}.** {{ week.topics }} | {{ week.deliverable }} |
{% endfor %}

## Core sources

- Carter Zenke and David J. Malan, [CS50’s Introduction to Databases with SQL](https://cs50.harvard.edu/sql/), Harvard University.

<!-- ko -->

## 과목의 목적

데이터로 답할 질문과 결과의 한 행이 뜻하는 대상을 정의하고 쿼리를 작성한 뒤, 손으로 확인한 예제와 결과를 대조합니다. 조회와 집계에서 JOIN·단계별 쿼리·윈도 함수로 진행하고, 데이터 변경·실행 계획·프로그램 활용을 다룹니다.

여러 테이블의 행 단위(grain)를 맞추고 중간 결과를 검증하는 데 중점을 둡니다. 쿼리의 정확성, 중복·누락 기록, 실행 비용, 트랜잭션 동작은 구분해 평가합니다.

Sunwoo Kim이 컴퓨터공학 비전공자를 위해 설계한 8주 자율 학습 과정입니다. 직접 작성한 설명과 풀이 읽기자료에 스키마·예제 데이터·쿼리·기대 결과를 함께 담고 공식 문서를 참고합니다.

## 수강 대상과 선수 지식

표 데이터를 조회하고 요약해야 하는 연구자·엔지니어·분석가를 대상으로 합니다. 스프레드시트의 행과 열을 이해한다고 가정합니다. 스키마·키·관계는 다중 테이블 쿼리에 앞서 설명합니다. 프로그래밍이나 데이터베이스 수강 경험은 요구하지 않으며, SQL을 프로그램에 연결하는 Python 예제는 필요한 시점에 설명합니다.

## 학습 목표

과정을 마치면 다음 작업을 수행할 수 있어야 합니다.

1. 스키마를 읽고 테이블의 행 단위·키·관계를 설명합니다.
2. 누락 값의 처리 방식을 정해 조회·집계·조건별 요약 쿼리를 작성합니다.
3. 서로 맞는 행 단위로 테이블을 JOIN하고 행 수·합계·미매칭 기록을 확인합니다.
4. 서브쿼리·CTE·존재 여부 검사로 복합 조건을 구성하고 각 단계의 결과를 검증합니다.
5. 파티션·이벤트 순서·동률 처리·필요한 프레임 경계를 명시해 윈도 함수를 사용합니다.
6. 데이터 변경과 롤백 동작을 확인하고 실행 계획을 비교하며 프로그램에서 매개변수 SQL을 호출합니다.

## 8주 구성

| 주차 | 주제와 범위 | 필수 결과물 |
| --- | --- | --- |
{% for week in course.weeks %}| {{ week.number }} | **{{ week.title_ko }}.** {{ week.topics_ko }} | {{ week.deliverable_ko }} |
{% endfor %}

## 핵심 참고자료

- Carter Zenke·David J. Malan, [CS50’s Introduction to Databases with SQL](https://cs50.harvard.edu/sql/), Harvard University.
