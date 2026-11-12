---
layout: "course-resource"
title: "Week 7 Instructor Guide"
title_ko: "7주차 교사용 진행안"
permalink: "/courses/practical-algorithms/week-07-instructor/"
course_id: "practical-algorithms"
---
## Teaching sequence

Ask learners to predict the lecture traces before running demos. In session 13, focus on the first group of problems; in session 14, compare the later state definitions. Use the student file before opening solutions.

## Concept checks

The 1 in `dp[a-c]+1` counts the final added coin. Amount zero needs zero coins; unreachable amounts remain infinite.

Path counting adds the sizes of two disjoint sets distinguished by their final move. LCS maximizes possible lengths, so it cannot use the same addition rule.

## Checkpoint answers

1. 4, selecting the first and last values. Comparing only odd and even positions misses this choice.
2. 2, using 3+3 rather than the greedy 4+1+1.
3. 1 and 4. The second row contains 1,2,3,4.
4. `2`. A subsequence preserves order and may skip intermediate characters.

## Review criteria

Check contract, state meaning, correctness, time, auxiliary/output space, and boundary inputs separately. Accept alternative correct methods with their own cost analysis. Local tests do not replace a correctness argument.


<!-- ko -->

## 수업 순서

시연 실행 전에 강의 추적 표의 다음 상태를 예상하게 합니다. 13차시에서는 앞의 문제 묶음을 풀고, 14차시에서는 뒤의 상태 정의를 비교합니다. 학생 파일을 먼저 작성하고 해설을 엽니다.

## 개념 질문 해설

`dp[a-c]+1`의 1은 마지막으로 추가한 동전입니다. 금액이 0이면 동전 0개이고, 만들 수 없는 금액은 무한대로 유지합니다.

경로 수는 마지막 이동이 위·왼쪽인 두 집합의 크기를 더합니다. LCS는 가능한 길이 중 최댓값을 구하므로 같은 합 연산을 사용할 수 없습니다.

## 중간 점검 답

1. `4`. 첫 값과 마지막 값을 선택합니다. 홀수·짝수 위치의 합만 비교하면 놓칩니다.
2. `2`. 3+3이며 큰 동전부터 고른 4+1+1보다 적습니다.
3. 1과 4. 두 번째 행은 왼쪽부터 1,2,3,4입니다.
4. `2`. 부분수열은 순서를 보존하며 중간 문자를 건너뛸 수 있습니다.

## 검토 기준

입력 계약·상태 의미·정당성·시간·보조 공간·출력 공간·경계 입력을 나누어 확인합니다. 다른 올바른 풀이도 해당 비용 분석과 함께 인정합니다. 로컬 검사는 정당성 설명을 대신하지 않습니다.
