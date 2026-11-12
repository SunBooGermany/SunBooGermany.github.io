---
layout: "course-resource"
title: "Week 6 Instructor Guide"
title_ko: "6주차 교사용 진행안"
permalink: "/courses/practical-algorithms/week-06-instructor/"
course_id: "practical-algorithms"
---
## Teaching sequence

Ask learners to predict the lecture traces before running demos. In session 11, focus on the first group of problems; in session 12, compare the later state definitions. Use the student file before opening solutions.

## Concept checks

DFS state 1 is on the active path, so an edge back to it identifies a cycle. State 2 has left that path. In `0→1`, `0→2`, `2→1`, revisiting completed node 1 is not a cycle.

A recursive return ends only that call. The parent resumes with pop and the next loop choice. Use Kahn’s algorithm for long graphs to avoid recursion-depth limits.

## Checkpoint answers

1. None exists: each course waits for the other, so return `[]`.
2. Yes. Both 0 and 1 only need to precede 2.
3. Four subsets, including `[]`. Copy the path so later pops do not alter saved results.
4. Reuse index 0. Advancing to the next index misses `[2,2]`.

## Review criteria

Check contract, state meaning, correctness, time, auxiliary/output space, and boundary inputs separately. Accept alternative correct methods with their own cost analysis. Local tests do not replace a correctness argument.


<!-- ko -->

## 수업 순서

시연 실행 전에 강의 추적 표의 다음 상태를 예상하게 합니다. 11차시에서는 앞의 문제 묶음을 풀고, 12차시에서는 뒤의 상태 정의를 비교합니다. 학생 파일을 먼저 작성하고 해설을 엽니다.

## 개념 질문 해설

DFS의 진행 중 상태 1은 현재 경로에 있으므로 그곳으로 돌아가는 간선은 사이클입니다. 완료 상태 2는 경로에서 빠진 정점입니다. `0→1`, `0→2`, `2→1`에서 완료된 1의 재방문은 사이클이 아닙니다.

재귀의 return은 그 호출만 끝냅니다. 부모는 호출 다음 줄의 pop을 수행하고 for의 다음 선택을 처리합니다. 긴 그래프는 재귀 제한을 피하는 Kahn 구현으로 풉니다.

## 중간 점검 답

1. 없습니다. 두 과목이 서로를 기다리므로 빈 목록을 반환합니다.
2. 정답입니다. 0과 1이 모두 2보다 먼저 나오면 됩니다.
3. 4개이며 `[]`도 하나입니다. 경로를 복사해야 이후 pop이 저장된 답을 바꾸지 않습니다.
4. 같은 인덱스 0. 다음 인덱스로 이동하면 필요한 `[2,2]`를 놓칩니다.

## 검토 기준

입력 계약·상태 의미·정당성·시간·보조 공간·출력 공간·경계 입력을 나누어 확인합니다. 다른 올바른 풀이도 해당 비용 분석과 함께 인정합니다. 로컬 검사는 정당성 설명을 대신하지 않습니다.
