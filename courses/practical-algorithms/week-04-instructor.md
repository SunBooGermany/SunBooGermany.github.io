---
layout: "course-resource"
title: "Week 4 Instructor Guide"
title_ko: "4주차 교사용 진행안"
permalink: "/courses/practical-algorithms/week-04-instructor/"
course_id: "practical-algorithms"
---

## Session 7: Returned heights

Draw the teaching tree before running either demo. Ask what each child returns and why the empty tree returns 0. Require both branches to be checked; an `elif` can skip a deeper right subtree. Compare recursive and iterative outputs on small trees, then use the iterative version for a 10,000-node chain.

## Session 8: Levels and bounds

Freeze the queue size at the start of each level. Trace inherited bounds down the root-to-6 path in the invalid-BST example. In recursive validation, every child result must contribute to the parent's result; ignoring a `False` can hide a descendant violation. Distinguish the 1-indexed kth visit from Python list index k-1.

## Midpoint review

Use the three questions at the end of the lecture before opening the companion answers. Check output, stored state, correctness, time, and auxiliary/output space separately. Ask learners to add an empty tree, duplicate-key tree, and skew tree. No learner performance is assumed.

<!-- ko -->

## 7차시: 높이 반환값

시연 실행 전에 강의의 트리를 그립니다. 각 자식의 반환값과 빈 트리에서 0을 반환하는 이유를 묻습니다. `elif`는 더 깊은 오른쪽 부분 트리를 건너뛸 수 있으므로 양쪽 분기를 확인합니다. 작은 트리에서 재귀·반복 결과를 비교한 뒤 10,000노드 연결 모양 트리는 반복 구현으로 처리합니다.

## 8차시: 레벨과 범위

각 레벨 시작 시 큐 길이를 고정합니다. 잘못된 BST 예시의 루트에서 6으로 이어지는 경로에 조상 범위를 표시합니다. 재귀 검증에서는 모든 자식의 결과를 부모 결과에 반영해야 합니다. `False`를 무시하면 후손의 위반을 놓칩니다. 1부터 세는 k번째 방문과 Python 리스트의 k-1 인덱스를 구별합니다.

## 중간 점검

해설을 열기 전에 강의 끝의 세 문제를 풉니다. 출력·상태·정당성·시간·보조 공간·출력 공간을 나누어 확인합니다. 빈 트리·중복 키·편향 트리를 추가로 만들게 합니다. 실제 학습자의 수행 결과를 가정하지 않습니다.
