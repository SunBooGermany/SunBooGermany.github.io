---
layout: "course-note"
title: "Week 3 Worked Companion"
title_ko: "3주차 풀이 읽기자료"
course_id: "practical-algorithms"
permalink: "/courses/practical-algorithms/week-03-reading/"
updated: "2026-11-11"
material_label: "Week 3 reading"
material_label_ko: "3주차 읽기자료"
pdf_en: "/assets/courses/practical-algorithms/week-03-reading-en.pdf"
pdf_ko: "/assets/courses/practical-algorithms/week-03-reading-ko.pdf"
lecture_note: "/courses/practical-algorithms/week-03/"
practice_note: "/courses/practical-algorithms/week-03-practice/"
---

## Using the worked companion

Attempt the student exercises independently first. This companion contains hints and complete solutions. Read only as far as needed, then return to your attempt.

Examples are original teaching examples. Follow each official link for the source problem and its complete contract.

[Student exercises](/courses/practical-algorithms/week-03-practice/)

[Instructor guide](/courses/practical-algorithms/week-03-instructor/)

[Download all code](/assets/courses/practical-algorithms/week-03-code.zip)

<!-- lecture-page -->

## 74 · Staged hints

[LeetCode 74: Search a 2D Matrix](https://leetcode.com/problems/search-a-2d-matrix/) · Medium

New exercise

H1. Which row and column correspond to flat index 4?

H2. Is the flattened order sorted without the cross-row condition?

H3. Keep a closed candidate interval [left,right]; read mid at row mid//C and column mid%C.

<!-- lecture-page -->

## 74 · Correctness and cost

The cross-row property makes the flattened order sorted. Comparisons eliminate an impossible half; every update shrinks the interval, and an empty interval means absence.

R,C are row/column counts. O(log(RC)) time, O(1) auxiliary space; no flattened copy.

<!-- lecture-page -->

## 74 · Counterexamples and checks

left=mid can stall on two candidates. [[1,9],[2,10]] has sorted rows but violates this contract.

`matrix=[[1,4,7],[9,12,18]], target=12 → True`

Trace before execution: write down each state and the return value, then compare with the code. Follow-up: what changes if mutation is forbidden, a different output is requested, or structure costs change?

<!-- lecture-page -->

## 74 · Implementation 1/1

The complete implementation is also in the code bundle.

```python
def search_matrix(matrix, target):
    rows, cols = len(matrix), len(matrix[0])
    left, right = 0, rows * cols - 1
    while left <= right:
        mid = (left + right) // 2
        value = matrix[mid // cols][mid % cols]
        if value == target:
            return True
        if value < target:
            left = mid + 1
        else:
            right = mid - 1
    return False
```

<!-- lecture-page -->

## 33 · Staged hints

[LeetCode 33: Search in Rotated Sorted Array](https://leetcode.com/problems/search-in-rotated-sorted-array/) · Medium

Extension

H1. Which side of mid must be sorted?

H2. Does target lie inside that sorted value range?

H3. Identify a sorted half and retain it only when its value range contains target.

<!-- lecture-page -->

## 33 · Correctness and cost

Distinct values and one rotation ensure a sorted half. Range tests discard only an impossible half; mid±1 guarantees progress.

n is length. O(log n) time, O(1) auxiliary space.

<!-- lecture-page -->

## 33 · Counterexamples and checks

With duplicates, [1,0,1,1,1] makes the sorted-side test ambiguous; duplicates are outside this contract.

`nums=[6,8,1,3,5], target=3 → 3`

Trace before execution: write down each state and the return value, then compare with the code. Follow-up: what changes if mutation is forbidden, a different output is requested, or structure costs change?

<!-- lecture-page -->

## 33 · Implementation 1/1

The complete implementation is also in the code bundle.

```python
def search_rotated(nums, target):
    left, right = 0, len(nums) - 1
    while left <= right:
        mid = (left + right) // 2
        if nums[mid] == target:
            return mid
        if nums[left] <= nums[mid]:
            if nums[left] <= target < nums[mid]:
                right = mid - 1
            else:
                left = mid + 1
        else:
            if nums[mid] < target <= nums[right]:
                left = mid + 1
            else:
                right = mid - 1
    return -1
```

<!-- lecture-page -->

## 206 · Staged hints

[LeetCode 206: Reverse Linked List](https://leetcode.com/problems/reverse-linked-list/) · Easy

New exercise

H1. How will the remaining chain be found after next is overwritten?

H2. What are the heads of the processed and unprocessed parts?

H3. Save following, redirect current.next to previous, then advance both references.

<!-- lecture-page -->

## 206 · Correctness and cost

previous holds the reversed prefix and current the untouched suffix. Moving one node preserves all nodes; when current is None, previous is the full reversed list.

n is node count. O(n) time, O(1) auxiliary space; nodes are reused.

<!-- lecture-page -->

## 206 · Counterexamples and checks

Overwriting without saving next loses the suffix. Two nodes with equal values are still different objects.

`head=[4,6,9] → [9,6,4]`

Trace before execution: write down each state and the return value, then compare with the code. Follow-up: what changes if mutation is forbidden, a different output is requested, or structure costs change?

<!-- lecture-page -->

## 206 · Implementation 1/1

The complete implementation is also in the code bundle.

```python
def reverse_list(head):
    previous, current = None, head
    while current:
        following = current.next
        current.next = previous
        previous, current = current, following
    return previous
```

<!-- lecture-page -->

## 21 · Staged hints

[LeetCode 21: Merge Two Sorted Lists](https://leetcode.com/problems/merge-two-sorted-lists/) · Easy

New exercise

H1. Can any unprocessed value precede the smaller head?

H2. Must the first result node need special handling?

H3. Maintain tail after a dummy node; link the smaller head, then attach the remaining suffix.

<!-- lecture-page -->

## 21 · Correctness and cost

The prefix through tail is sorted. The smaller head is minimal among all remaining nodes; the leftover suffix is already sorted.

n,m are node counts. O(n+m) time, O(1) auxiliary space; input links change.

<!-- lecture-page -->

## 21 · Counterexamples and checks

Returning dummy includes a fake node. This implementation assumes acyclic input lists with no shared nodes.

`first=[1,5], second=[2,3] → [1,2,3,5]`

Trace before execution: write down each state and the return value, then compare with the code. Follow-up: what changes if mutation is forbidden, a different output is requested, or structure costs change?

<!-- lecture-page -->

## 21 · Implementation 1/1

The complete implementation is also in the code bundle.

```python
def merge_lists(first, second):
    dummy = tail = ListNode()
    while first and second:
        if first.val <= second.val:
            tail.next, first = first, first.next
        else:
            tail.next, second = second, second.next
        tail = tail.next
    tail.next = first or second
    return dummy.next
```

<!-- lecture-page -->

## Execution and sources

```text
cd code
python verify.py
```

Common objects and imports are in structures.py and solutions.py. On LeetCode, adapt the function to the official method signature.

Erik Demaine and Srini Devadas, [Introduction to Algorithms, MIT 6.006](https://ocw.mit.edu/courses/6-006-introduction-to-algorithms-fall-2011/) (Fall 2011).

<!-- lecture-page -->

## Short checks

1. In a four-column matrix, which cell has flat index 6?
2. Why must the next node be saved before reversing a link?
3. What does `dummy.next` return when both input lists are empty?

Answers: (1) row 1, column 2; (2) otherwise the unprocessed suffix is no longer reachable from the current node; (3) `None`.

<!-- ko -->

## 해설 사용 순서

먼저 학생 실습에서 문제를 독립적으로 풉니다. 이 자료는 힌트와 완전 해설을 포함합니다. 필요한 단계까지만 읽고 다시 풀이합니다.

표시된 예시는 강의에서 만든 예시입니다. 원문과 전체 제약은 각 공식 링크에서 확인합니다.

[학생 실습](/courses/practical-algorithms/week-03-practice/)

[교사용 진행안](/courses/practical-algorithms/week-03-instructor/)

[코드 전체 내려받기](/assets/courses/practical-algorithms/week-03-code.zip)

<!-- lecture-page -->

## 74 · 단계별 힌트

[LeetCode 74: Search a 2D Matrix](https://leetcode.com/problems/search-a-2d-matrix/) · Medium

신규 연습

H1. 평탄 인덱스 4는 어느 행·열인가요?

H2. 행끼리의 순서가 없으면 전체 정렬인가요?

H3. [left,right]를 닫힌 후보 구간으로 두고 mid//C, mid%C로 값을 읽습니다.

<!-- lecture-page -->

## 74 · 정당성과 비용

행 사이 조건까지 있으므로 평탄 배열은 정렬되어 있습니다. mid가 target보다 작으면 mid 이하를 제거합니다. 매 반복 구간이 줄고, 종료하면 후보가 없습니다.

R,C=행·열 수. O(log(RC)) 시간, O(1) 보조 공간. 평탄 복사하지 않습니다.

<!-- lecture-page -->

## 74 · 반례와 검증

left=mid는 길이 2 구간에서 정체할 수 있습니다. [[1,9],[2,10]]은 행만 정렬된 다른 문제입니다.

`matrix=[[1,4,7],[9,12,18]], target=12 → True`

직접 추적: 실행 전에 각 상태와 반환값을 적고 코드와 비교합니다. 후속 질문: 입력을 바꾸지 않는 조건, 다른 출력 요구 또는 자료구조의 비용이 달라지면 무엇을 수정해야 하나요?

<!-- lecture-page -->

## 74 · 구현 1/1

아래 구현은 코드 묶음에서도 확인할 수 있습니다.

```python
def search_matrix(matrix, target):
    rows, cols = len(matrix), len(matrix[0])
    left, right = 0, rows * cols - 1
    while left <= right:
        mid = (left + right) // 2
        value = matrix[mid // cols][mid % cols]
        if value == target:
            return True
        if value < target:
            left = mid + 1
        else:
            right = mid - 1
    return False
```

<!-- lecture-page -->

## 33 · 단계별 힌트

[LeetCode 33: Search in Rotated Sorted Array](https://leetcode.com/problems/search-in-rotated-sorted-array/) · Medium

보강

H1. 중간을 기준으로 어느 쪽은 반드시 정렬되어 있나요?

H2. target이 그 값 범위 안에 있나요?

H3. 정렬된 절반을 식별하고 target이 그 범위에 있는지로 남길 절반을 정합니다.

<!-- lecture-page -->

## 33 · 정당성과 비용

서로 다른 값의 한 번 회전 배열에서는 적어도 한 절반이 정렬되어 있습니다. 그 범위 안/밖 검사는 target을 포함할 수 없는 절반만 제거하며 mid±1로 진전합니다.

n=길이. O(log n) 시간, O(1) 보조 공간.

<!-- lecture-page -->

## 33 · 반례와 검증

중복을 허용한 [1,0,1,1,1]에서는 양 끝과 mid가 같아 정렬 방향 판정이 모호합니다. 공식 제약 밖 확장입니다.

`nums=[6,8,1,3,5], target=3 → 3`

직접 추적: 실행 전에 각 상태와 반환값을 적고 코드와 비교합니다. 후속 질문: 입력을 바꾸지 않는 조건, 다른 출력 요구 또는 자료구조의 비용이 달라지면 무엇을 수정해야 하나요?

<!-- lecture-page -->

## 33 · 구현 1/1

아래 구현은 코드 묶음에서도 확인할 수 있습니다.

```python
def search_rotated(nums, target):
    left, right = 0, len(nums) - 1
    while left <= right:
        mid = (left + right) // 2
        if nums[mid] == target:
            return mid
        if nums[left] <= nums[mid]:
            if nums[left] <= target < nums[mid]:
                right = mid - 1
            else:
                left = mid + 1
        else:
            if nums[mid] < target <= nums[right]:
                left = mid + 1
            else:
                right = mid - 1
    return -1
```

<!-- lecture-page -->

## 206 · 단계별 힌트

[LeetCode 206: Reverse Linked List](https://leetcode.com/problems/reverse-linked-list/) · Easy

신규 연습

H1. next를 덮어쓴 뒤 나머지 노드를 어떻게 찾나요?

H2. 처리한 부분과 남은 부분의 head는 무엇인가요?

H3. following에 다음 참조를 보존하고 current.next=previous로 뒤집은 뒤 두 참조를 전진합니다.

<!-- lecture-page -->

## 206 · 정당성과 비용

반복 시작 때 previous는 처리한 접두부의 역순, current는 미처리 접미부입니다. 한 노드를 옮겨도 둘의 합은 원래 노드 전체입니다. current가 None이면 previous가 완성된 역순입니다.

n=노드 수. O(n) 시간, O(1) 보조 공간. 노드를 재사용합니다.

<!-- lecture-page -->

## 206 · 반례와 검증

다음 참조를 먼저 저장하지 않으면 나머지 연결을 잃습니다. 같은 값의 두 노드도 서로 다른 객체입니다.

`head=[4,6,9] → [9,6,4]`

직접 추적: 실행 전에 각 상태와 반환값을 적고 코드와 비교합니다. 후속 질문: 입력을 바꾸지 않는 조건, 다른 출력 요구 또는 자료구조의 비용이 달라지면 무엇을 수정해야 하나요?

<!-- lecture-page -->

## 206 · 구현 1/1

아래 구현은 코드 묶음에서도 확인할 수 있습니다.

```python
def reverse_list(head):
    previous, current = None, head
    while current:
        following = current.next
        current.next = previous
        previous, current = current, following
    return previous
```

<!-- lecture-page -->

## 21 · 단계별 힌트

[LeetCode 21: Merge Two Sorted Lists](https://leetcode.com/problems/merge-two-sorted-lists/) · Easy

신규 연습

H1. 두 head 중 작은 값보다 먼저 올 미처리 값이 있나요?

H2. 결과의 첫 노드를 매번 특별 취급해야 하나요?

H3. dummy 뒤 tail을 유지하고 작은 head를 연결합니다. 한 리스트가 끝나면 나머지를 붙입니다.

<!-- lecture-page -->

## 21 · 정당성과 비용

tail까지는 정렬된 병합 접두부입니다. 두 head 중 작은 것은 남은 모든 값 중 최소이므로 다음 노드로 안전합니다. 남은 접미부도 정렬되어 있습니다.

n,m=두 노드 수. O(n+m) 시간, O(1) 보조 공간. 입력 연결을 변경합니다.

<!-- lecture-page -->

## 21 · 반례와 검증

head 대신 dummy를 반환하면 가짜 값이 포함됩니다. 이 구현은 서로 겹치지 않고 사이클 없는 입력 리스트를 전제로 합니다.

`first=[1,5], second=[2,3] → [1,2,3,5]`

직접 추적: 실행 전에 각 상태와 반환값을 적고 코드와 비교합니다. 후속 질문: 입력을 바꾸지 않는 조건, 다른 출력 요구 또는 자료구조의 비용이 달라지면 무엇을 수정해야 하나요?

<!-- lecture-page -->

## 21 · 구현 1/1

아래 구현은 코드 묶음에서도 확인할 수 있습니다.

```python
def merge_lists(first, second):
    dummy = tail = ListNode()
    while first and second:
        if first.val <= second.val:
            tail.next, first = first, first.next
        else:
            tail.next, second = second, second.next
        tail = tail.next
    tail.next = first or second
    return dummy.next
```

<!-- lecture-page -->

## 실행과 참고자료

```text
cd code
python verify.py
```

공통 객체와 표준 라이브러리 import는 `structures.py`, `solutions.py`에 있습니다. LeetCode에서는 공식 메서드 서명에 맞춰 함수를 연결합니다.

Erik Demaine and Srini Devadas, [Introduction to Algorithms, MIT 6.006](https://ocw.mit.edu/courses/6-006-introduction-to-algorithms-fall-2011/) (Fall 2011).

<!-- lecture-page -->

## 짧은 확인 문제

1. 열이 네 개인 행렬에서 평탄 인덱스 6은 어느 칸인가요?
2. 연결을 뒤집기 전에 다음 노드를 저장하는 이유는 무엇인가요?
3. 두 입력 리스트가 비어 있으면 `dummy.next`는 무엇인가요?

답: (1) 1행 2열입니다. (2) 저장하지 않으면 현재 노드에서 미처리 부분으로 가는 연결을 잃습니다. (3) `None`입니다.
