---
layout: "course-resource"
title: "Week 1 Instructor Guide"
title_ko: "1주차 교사용 진행안"
permalink: "/courses/practical-algorithms/instructor/"
course_id: "practical-algorithms"
---

## Teaching flow

Use problem definition, manual tracing, implementation, independent work, and explanation/debugging in each session. Adjust pacing to learner responses. Open student exercises before hints.



## 1: Arrays and hashed state

Opening prompt: A sensor retransmits events at short intervals. Can recent duplicates be detected without comparing every past pair? Store values and latest positions to retain only relevant history.

Flow: ask the learner to restate inputs/outputs and compare a baseline with the improved state. Reveal the lecture trace one row at a time after predictions. Execute the companion implementation and compare with a simple baseline.

### [LeetCode 1: Two Sum](https://leetcode.com/problems/two-sum/) · Easy

Reasoning: At loop entry, the map contains only earlier positions. At the later position of the unique answer, its partner is present. This reuses information instead of checking all O(n²) pairs.

Debugging activity: Recording first can reuse one index on [3,3], target=6.

### [LeetCode 219: Contains Duplicate II](https://leetcode.com/problems/contains-duplicate-ii/) · Easy

Reasoning: The latest occurrence minimizes distance to the current index. If it is too far, all older occurrences are too far. Updating preserves this property.

Debugging activity: Keeping only the first position misses the last pair in [4,7,4,4], k=1. No distinct-index pair qualifies when k=0.

Concept check: Is the first occurrence enough?

Instructor answer: No. Updating at index 2 exposes its distance 1 from index 3.

Independent activity: implement this session’s problems in the student workspace. For correct outputs, still ask for the invariant and elimination argument. For failures, find the earliest divergent state on a small counterexample.

## 2: Sorted order and two pointers

Opening prompt: Choose two sorted part lengths totaling a target. Explain why a too-small left candidate can be discarded, then extend to three values.

Flow: ask the learner to restate inputs/outputs and compare a baseline with the improved state. Reveal the lecture trace one row at a time after predictions. Execute the companion implementation and compare with a simple baseline.

### [LeetCode 167: Two Sum II - Input Array Is Sorted](https://leetcode.com/problems/two-sum-ii-input-array-is-sorted/) · Medium

Reasoning: If the sum is small, no partner at or below right works with left. If large, no partner at or above left works with right. Each elimination preserves any answer.

Debugging activity: Outside the sorted contract, [3,1,4], target=5 defeats this rule. left==right reuses one element.

### [LeetCode 15: 3Sum](https://leetcode.com/problems/3sum/) · Medium

Reasoning: Every ordered triplet is examined when its smallest value is fixed. Sorted elimination is valid; skipping duplicates removes repeated value combinations only.

Debugging activity: [0,0,0,0] yields one triplet. Equal values at distinct positions remain allowed.

Concept check: If original indices are required, is sorting values alone enough?

Instructor answer: No; retain original indices with values. Problem 167 asks for positions in its already sorted input.

Independent activity: implement this session’s problems in the student workspace. For correct outputs, still ask for the invariant and elimination argument. For failures, find the earliest divergent state on a small counterexample.

<h2 id="en-week-1-checks">Week 1 answer checks</h2>

1. List membership searches values; dictionary membership tests keys.
2. Recording the first 3 at index 0 before lookup finds that same index. Lookup must precede recording so the next 3 finds earlier index 0.
3. Without updating latest[4] at index 2, index 3 compares with index 0 and misses the distance-one pair.
4. Copying a growing dictionary every iteration takes O(n²) total time. Discarding each snapshot gives O(n) peak additional space; retaining all gives O(n²) space.

<!-- ko -->

## 수업 운영

각 차시는 문제 정의와 손 추적, 구현, 독립 풀이, 설명·디버깅 순서로 진행합니다. 진행 시간은 수강생 반응에 맞춥니다. 학생 실습을 먼저 열고 힌트·해설은 필요할 때만 엽니다.



## 1차시: 배열과 해시 상태

도입 질문: 같은 센서 이벤트가 짧은 간격으로 재전송됩니다. 모든 과거 쌍을 비교하지 않고 최근 중복을 찾을 수 있을까요? 값과 최근 위치를 저장해 질문에 필요한 과거만 남깁니다.

진행: 학생에게 입력·출력을 다시 말하게 한 뒤, 아래 문제의 단순 접근과 개선 상태를 비교합니다. 강의의 상태 표를 한 행씩 가리고 다음 행을 예측하게 합니다. 읽기자료의 구현을 실행한 뒤 단순 풀이와 결과를 비교합니다.

### [LeetCode 1: Two Sum](https://leetcode.com/problems/two-sum/) · Easy

설명 근거: 반복 시작 때 사전에는 앞서 본 위치만 있습니다. 답의 두 번째 위치에 도착하면 첫 위치가 기록되어 있으므로 답을 찾습니다. 모든 쌍을 검사하는 O(n²) 방법에서 이전 정보를 재사용한 것입니다.

디버깅 활동: [3,3], target=6에서 현재 값을 먼저 저장하면 같은 인덱스를 두 번 반환할 수 있습니다.

### [LeetCode 219: Contains Duplicate II](https://leetcode.com/problems/contains-duplicate-ii/) · Easy

설명 근거: 최근 위치는 모든 이전 위치 중 현재 위치와 가장 가깝습니다. 이 거리도 k보다 크면 다른 과거 위치도 실패합니다. 갱신으로 다음 반복에도 같은 성질이 유지됩니다.

디버깅 활동: 최초 위치만 저장하면 [4,7,4,4], k=1에서 마지막 두 위치를 놓칩니다. k=0에서는 서로 다른 위치의 답이 없습니다.

이해 확인: 사전에 최초 위치만 남겨도 되나요?

교사용 답: 아닙니다. 2에서 최근 위치를 갱신해야 3과의 거리가 1입니다.

독립 활동: 주차 학생 파일에서 이번 차시 문제를 풀게 합니다. 답이 맞아도 보존되는 상태와 제거 근거를 설명하게 하고, 틀리면 가장 작은 실패 입력에서 최초로 상태가 달라진 지점을 찾게 합니다.

## 2차시: 정렬과 두 포인터

도입 질문: 정렬된 부품 길이에서 목표 길이를 만드는 두 개를 고릅니다. 작은 합을 만든 왼쪽 후보를 버려도 답이 남는 이유를 설명한 뒤 세 값으로 확장합니다.

진행: 학생에게 입력·출력을 다시 말하게 한 뒤, 아래 문제의 단순 접근과 개선 상태를 비교합니다. 강의의 상태 표를 한 행씩 가리고 다음 행을 예측하게 합니다. 읽기자료의 구현을 실행한 뒤 단순 풀이와 결과를 비교합니다.

### [LeetCode 167: Two Sum II - Input Array Is Sorted](https://leetcode.com/problems/two-sum-ii-input-array-is-sorted/) · Medium

설명 근거: 합이 작으면 현재 left와 right 이하의 어떤 값도 답을 만들지 못합니다. 합이 크면 현재 right와 left 이상의 어떤 값도 실패합니다. 제거된 쌍에는 답이 없으므로 남은 범위가 답을 보존합니다.

디버깅 활동: 정렬 전제 밖 [3,1,4], target=5에는 같은 이동 규칙을 적용할 수 없습니다. left==right는 같은 원소 재사용입니다.

### [LeetCode 15: 3Sum](https://leetcode.com/problems/3sum/) · Medium

설명 근거: 각 정렬된 세 값은 가장 작은 값의 차례에서 검사됩니다. 두 포인터 제거는 정렬로 정당화됩니다. 같은 값을 건너뛰는 것은 위치가 다른 동일한 값 조합만 제거합니다.

디버깅 활동: [0,0,0,0]은 한 조합만 반환합니다. 값이 같다는 이유로 서로 다른 위치를 금지하면 이 답을 잃습니다.

이해 확인: 정렬된 값이 아니라 원래 위치가 필요하면 정렬만 해도 되나요?

교사용 답: 아닙니다. 값과 원래 인덱스를 함께 보존해야 합니다. 167은 이미 정렬된 입력의 위치를 요구합니다.

독립 활동: 주차 학생 파일에서 이번 차시 문제를 풀게 합니다. 답이 맞아도 보존되는 상태와 제거 근거를 설명하게 하고, 틀리면 가장 작은 실패 입력에서 최초로 상태가 달라진 지점을 찾게 합니다.

<h2 id="ko-week-1-checks">1주차 확인 답</h2>

1. 리스트 membership은 값을 순서대로 찾고, 사전 membership은 키의 존재를 검사합니다.
2. 첫 3을 index=0으로 저장한 뒤 조회하면 그 위치 자신을 찾습니다. 조회 후 저장해야 다음 3이 이전 0을 찾습니다.
3. index=2에서 latest[4]=2로 갱신하지 않으면 index=3에서 0과 비교해 거리 3으로 실패하고, 실제 거리 1의 쌍을 놓칩니다.
4. 서로 다른 키가 계속 늘면 반복별 전체 사전 복사의 시간 합은 O(n²)입니다. snapshot을 매번 버리면 추가 메모리의 최대치는 O(n), 모두 보관하면 O(n²)입니다.
