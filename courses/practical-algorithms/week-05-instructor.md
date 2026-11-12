---
layout: "course-resource"
title: "Week 5 Instructor Guide"
title_ko: "5주차 교사용 진행안"
permalink: "/courses/practical-algorithms/week-05-instructor/"
course_id: "practical-algorithms"
---
## Teaching sequence

Ask learners to predict the lecture traces before running demos. In session 9, focus on the first group of problems; in session 10, compare the later state definitions. Use the student file before opening solutions.

## Concept checks

Insertion into a sorted list takes O(n) because elements shift, even if binary search finds the position. A min-heap is not fully sorted; its root is a global minimum.

BFS first discovery gives minimum cost when every edge has the same cost. With unequal costs, a path with fewer edges can cost more.

## Checkpoint answers

1. 8 and 2. Both copies of 8 count.
2. `[[1,8]]` and `[[1,6]]`. A nested interval cannot shorten the union; closed intervals touching at an endpoint merge.
3. `2`. Diagonals are not connected.
4. -1 and 0. The first has unreachable fresh cells; the second starts with no fresh cells.

## Review criteria

Check contract, state meaning, correctness, time, auxiliary/output space, and boundary inputs separately. Accept alternative correct methods with their own cost analysis. Local tests do not replace a correctness argument.


<!-- ko -->

## 수업 순서

시연 실행 전에 강의 추적 표의 다음 상태를 예상하게 합니다. 9차시에서는 앞의 문제 묶음을 풀고, 10차시에서는 뒤의 상태 정의를 비교합니다. 학생 파일을 먼저 작성하고 해설을 엽니다.

## 개념 질문 해설

정렬된 리스트의 삽입은 위치를 이진 탐색해도 원소 이동 때문에 O(n)입니다. 최소 힙은 전체 정렬이 아니며 루트만 전역 최솟값입니다.

BFS의 첫 발견이 최소 비용이 되는 조건은 모든 간선 비용이 같다는 것입니다. 비용이 다르면 간선 수가 적은 경로가 더 비쌀 수 있습니다.

## 중간 점검 답

1. 8과 2. 중복 8을 두 번 셉니다.
2. `[[1,8]]`과 `[[1,6]]`. 포함 구간의 끝으로 기존 끝을 줄이지 않으며, 닫힌 구간은 끝점이 닿으면 합칩니다.
3. `2`. 대각선은 연결하지 않습니다.
4. -1과 0. 첫 지도는 신선한 셀에 경로가 없고, 둘째는 처음부터 신선한 셀이 없습니다.

## 검토 기준

입력 계약·상태 의미·정당성·시간·보조 공간·출력 공간·경계 입력을 나누어 확인합니다. 다른 올바른 풀이도 해당 비용 분석과 함께 인정합니다. 로컬 검사는 정당성 설명을 대신하지 않습니다.
