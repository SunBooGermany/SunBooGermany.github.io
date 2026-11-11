---
layout: "course-resource"
title: "Week 3 Instructor Guide"
title_ko: "3주차 교사용 진행안"
permalink: "/courses/practical-algorithms/week-03-instructor/"
course_id: "practical-algorithms"
---

## Session 5: Candidate intervals

Ask learners to trace an absent target as well as a match. Check that the closed interval excludes the tested midpoint and that row boundaries satisfy the matrix contract. For rotated arrays, ask which half is ordered and whether the target lies within its inclusive/exclusive bounds.

The first-feasible variant has a different invariant and exit meaning: it can return an exclusive sentinel if no candidate is feasible. It requires a monotone predicate.

## Session 6: Node identity

Trace `previous`, `current`, and the saved next reference before changing a link. Ask learners to draw separate nodes with equal values. For merging, trace the dummy, tail, and remaining heads; check empty inputs and duplicate values.

Student exercises and completed implementations are separate. Ask for a correctness argument as well as test outputs.

<!-- ko -->

## 5차시: 후보 구간

목표값이 있는 경우와 없는 경우를 모두 추적합니다. 닫힌 구간에서 검사한 중간점을 제외하는지, 행렬의 행 사이 조건이 성립하는지 확인합니다. 회전 배열에서는 정렬된 절반과 목표값의 범위 포함 여부를 묻습니다.

최초 feasible 위치 탐색은 불변식과 종료 의미가 다릅니다. 가능한 후보가 없으면 구간 밖 sentinel을 반환할 수 있으며 단조 판정 함수가 필요합니다.

## 6차시: 노드 동일성

연결을 바꾸기 전에 `previous`, `current`, 보관한 다음 참조를 추적합니다. 같은 값을 가진 서로 다른 노드를 그려 보게 합니다. 병합에서는 dummy, tail, 남은 head를 따라가며 빈 입력과 중복 값을 확인합니다.

학생 실습과 완성 풀이는 분리되어 있습니다. 테스트 결과와 함께 정당성 설명을 요청합니다.
