---
layout: "course-note"
title: "Week 3 Worked Companion"
title_ko: "3주차 풀이 읽기자료"
course_id: "practical-algorithms"
permalink: "/courses/practical-algorithms/week-03-reading/"
updated: "2026-11-12"
material_label: "Week 3 reading"
material_label_ko: "3주차 읽기자료"
pdf_en: "/assets/courses/practical-algorithms/week-03-reading-en.pdf"
pdf_ko: "/assets/courses/practical-algorithms/week-03-reading-ko.pdf"
lecture_note: "/courses/practical-algorithms/week-03/"
practice_note: "/courses/practical-algorithms/week-03-practice/"
---

## Worked solutions

74 | 33 | 206 | 21

A device stores sorted measurements in rows. When a new reading arrives, can we find it without inspecting every record? Then a queue of records must be reordered while preserving the same node objects.

This week uses candidate intervals for search and changes links to reverse or merge lists.

<!-- lecture-page -->

## Positions and node references

An array directly accesses position i by index. A linked list follows next references from its head. Two nodes with the same value 2 can still be distinct objects.

```python
class ListNode:
    def __init__(self, val=0, next=None):
        self.val, self.next = val, next
```

![Save the successor before reversing the current link](/assets/courses/practical-algorithms/curriculum/reverse-links.svg)

The diagram processes node 2. Preserve node 3 as following before changing 2’s next to node 1. A node’s value and its links are different data. `node = node.next` moves a local reference; `node.next = other` changes the structure.

<!-- lecture-page -->

## 74 · Idea and execution trace

[LeetCode 74: Search a 2D Matrix](https://leetcode.com/problems/search-a-2d-matrix/) · Medium

Return whether target occurs in the matrix.

Each row is sorted and its first value exceeds the previous row’s last value. Reading rows consecutively therefore gives one sorted sequence. Search that virtual sequence without copying it; translate each position into a row and column.

`matrix=[[1,3,5],[7,9,11]], target=9`. Bounds are shown before each comparison.

| left,right | mid | row,col | Value | Next action |
| --- | --- | --- | --- | --- |
| 0,5 | 2 | 0,2 | 5 | 5 < 9 → left=3 |
| 3,5 | 4 | 1,1 | 9 | Return True |

<!-- lecture-page -->

## 74 · Turning the idea into code

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

`mid // cols` counts complete rows before the position; `mid % cols` locates it within a row. Position 4 with three columns is row 1, column 1.

If the value is too small, discard through mid; if too large, discard from mid onward. Excluding the tested position guarantees progress even with one candidate left.

<!-- lecture-page -->

## 74 · Why it works; time and memory

The cross-row property makes the flattened order sorted. Comparisons eliminate an impossible half; every update shrinks the interval, and an empty interval means absence.

For N=R·C elements, comparisons reduce the candidates roughly to N/2, N/4, and so on. N=8 needs at most four comparisons; time is O(log(N+1)). Index arithmetic and each list lookup cost O(1).

No flattened list is built. Only a fixed number of indices and values are retained, so auxiliary space is O(1). Copying the matrix into a new sequence would change this space bound.

left=mid can stall on two candidates. [[1,9],[2,10]] has sorted rows but violates this contract.

`matrix=[[1,4,7],[9,12,18]], target=12 → True`

<!-- lecture-page -->

## Termination when the target is absent

Search for target=8 in `[[1,3,5],[7,9,11]]`. The interval `[left,right]` includes both remaining endpoints.

| Interval before comparison | mid and value | Reason for removal | Next interval |
| --- | --- | --- | --- |
| [0,5] | 2, value 5 | All positions at or below 2 have values below 8 | [3,5] |
| [3,5] | 4, value 9 | All positions at or above 4 have values above 8 | [3,3] |
| [3,3] | 3, value 7 | The last candidate also fails | [4,3] |

left>right means no candidate remains, so return False. left==right still requires one comparison. Updating left=mid can repeat mid=3 forever on `[3,4]`.

Halving N candidates takes about log₂N reductions to reach one. Including its comparison, the worst count is floor(log₂N)+1 for N≥1.

<!-- lecture-page -->

## 33 · Idea and execution trace

[LeetCode 33: Search in Rotated Sorted Array](https://leetcode.com/problems/search-in-rotated-sorted-array/) · Medium

Return target’s index in a rotated sorted array, or -1.

Although a rotated array is not globally sorted, with distinct values at least one half around mid is sorted. Identify that half, then test whether target lies within its value range to decide which half to discard.

`nums=[4,5,6,7,0,1,2], target=0`

| left,mid,right | Sorted half | Target test | Update |
| --- | --- | --- | --- |
| 0,3,6 | Left: 4..7 | 0 is outside | left=4 |
| 4,5,6 | Left: 0..1 | 0 is inside | right=4 |
| 4,4,4 | nums[4]=0 | Match | Return 4 |

<!-- lecture-page -->

## 33 · Turning the idea into code

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

`nums[left] <= nums[mid]` identifies a sorted left half. Keep it only when `nums[left] <= target < nums[mid]`. Equality at mid was already tested, hence the strict inequality at that end.

The sorted-right case is symmetric. Sorting again would change the original positions that the function must return.

<!-- lecture-page -->

## 33 · Why it works; time and memory

Distinct values and one rotation ensure a sorted half. Range tests discard only an impossible half; mid±1 guarantees progress.

Each iteration retains only one half, excluding mid. There are O(log(n+1)) iterations, each with a fixed number of comparisons and lookups.

No new array or recursive call stack is created, so auxiliary space is O(1). With duplicates, an input such as `[1,1,1,0,1]` can have equal endpoints and midpoint, hiding which half is sorted. This code and bound depend on distinct values.

With duplicates, [1,0,1,1,1] makes the sorted-side test ambiguous; duplicates are outside this contract.

`nums=[6,8,1,3,5], target=3 → 3`

<!-- lecture-page -->

## 206 · Idea and execution trace

[LeetCode 206: Reverse Linked List](https://leetcode.com/problems/reverse-linked-list/) · Easy

Reverse a singly linked list and return its new head.

A linked list’s order is determined by next links. Reverse each link without allocating replacement nodes. Save the original successor before changing the link, or the unprocessed remainder becomes unreachable.

Input: `1 → 2 → 3 → None`. Each row is the state after one loop body.

| Node processed | Chain at previous | Chain at current |
| --- | --- | --- |
| None yet | None | 1 → 2 → 3 |
| 1 | 1 → None | 2 → 3 |
| 2 | 2 → 1 → None | 3 |
| 3 | 3 → 2 → 1 → None | None |

<!-- lecture-page -->

## 206 · Turning the idea into code

```python
def reverse_list(head):
    previous, current = None, head
    while current:
        following = current.next
        current.next = previous
        previous, current = current, following
    return previous
```

`following = current.next` preserves the successor. `current.next = previous` reverses one link. The final simultaneous assignment advances previous to the processed node and current to the saved successor.

When current is None, no node remains to process and previous is the new head. An empty input skips the loop and returns None.

While processing node 2, previous points to 1, current to 2, and following to 3. After reversing next, the simultaneous assignment first evaluates its right side `(current,following)` as `(2,3)`. previous therefore becomes 2 and current becomes 3. Advancing through `current.next` would follow the reversed edge back to 1, which is why the saved following is used.

<!-- lecture-page -->

## 206 · Why it works; time and memory

previous holds the reversed prefix and current the untouched suffix. Moving one node preserves all nodes; when current is None, previous is the full reversed list.

Each of n nodes is visited once, with a fixed number of reference assignments per visit, giving O(n) time. Reversing the first link does not reverse later links; every node must be processed.

Only previous, current, and following are added. Existing nodes are reused, so auxiliary space is O(1) and no output nodes are allocated. The O(n) input structure is distinct from extra workspace. A recursive implementation would need O(n) call-stack space.

Overwriting without saving next loses the suffix. Two nodes with equal values are still different objects.

`head=[4,6,9] → [9,6,4]`

<!-- lecture-page -->

## 21 · Idea and execution trace

[LeetCode 21: Merge Two Sorted Lists](https://leetcode.com/problems/merge-two-sorted-lists/) · Easy

Splice two sorted linked lists into one sorted list.

The smallest remaining value must be at one of the two sorted-list heads. Attach the smaller head to the result tail and advance only that input. There is no need to search farther down either list.

A=`1 → 4`, B=`2 → 3`. Links beyond tail may still point into an input until the next assignment replaces them.

| Choice | Finalized result prefix | A head | B head |
| --- | --- | --- | --- |
| Initial | Empty | 1 | 2 |
| A: 1 | 1 | 4 | 2 |
| B: 2 | 1 → 2 | 4 | 3 |
| B: 3 | 1 → 2 → 3 | 4 | None |
| Attach remaining A | 1 → 2 → 3 → 4 | 4 | None |

<!-- lecture-page -->

## 21 · Turning the idea into code

```python
from structures import ListNode

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

The dummy node makes the first attachment use the same operation as later attachments. Simultaneous assignment attaches the old first node and advances first to its original successor.

Once either list is empty, the other remainder is already sorted. `tail.next = first or second` attaches that chain in one operation. The returned head excludes dummy.

<!-- lecture-page -->

## 21 · Why it works; time and memory

The prefix through tail is sorted. The smaller head is minimal among all remaining nodes; the leftover suffix is already sorted.

For lengths n and m, each iteration finalizes one node. Alternating choices can require O(n+m) work. The final remainder attachment itself costs O(1).

One dummy node and a fixed number of references give O(1) auxiliary space. The result has n+m nodes, but these are reused input nodes. Preserving both input chains would require a copying implementation with O(n+m) new-node space.

Returning dummy includes a fake node. This implementation assumes acyclic input lists with no shared nodes.

`first=[1,5], second=[2,3] → [1,2,3,5]`

<!-- lecture-page -->

## Exercises and sources

[LeetCode · 74, 33, 206, 21](/courses/practical-algorithms/week-03-practice/) · [Worked solutions](/courses/practical-algorithms/week-03-reading/) · [Python ZIP](/assets/courses/practical-algorithms/week-03-code.zip)

```text
python demo_05.py
python demo_06.py
python verify.py
```

After implementing the student file, check it with `python verify.py --student`.

Erik Demaine, Srini Devadas. [MIT 6.006, Introduction to Algorithms](https://ocw.mit.edu/courses/6-006-introduction-to-algorithms-fall-2011/) (2011).

<!-- ko -->

## 풀이와 실행 과정

74 | 33 | 206 | 21

장치가 측정값을 정렬된 행에 저장합니다. 새 측정값을 찾을 때 모든 기록을 확인하지 않을 수 있을까요? 이어서 대기열의 노드 객체를 유지한 채 순서를 바꿉니다.

이번 주에는 후보 구간으로 값을 탐색하고 노드의 연결을 바꿔 리스트를 뒤집거나 병합합니다.

<!-- lecture-page -->

## 위치와 노드 참조

배열의 i번째 원소는 인덱스로 직접 읽습니다. 연결 리스트는 노드가 다음 노드를 가리키므로 머리에서 next를 따라 이동합니다. 같은 값 2를 가진 노드 두 개도 서로 다른 객체일 수 있습니다.

```python
class ListNode:
    def __init__(self, val=0, next=None):
        self.val, self.next = val, next
```

![연결을 뒤집기 전에 다음 노드를 보존하는 과정](/assets/courses/practical-algorithms/curriculum/reverse-links.svg)

그림은 2를 처리할 때입니다. following으로 3을 보존한 뒤 2의 next를 1로 바꿉니다. 노드의 값과 노드 사이 연결은 서로 다른 데이터입니다. `node = node.next`는 지역 참조만 옮기고 `node.next = other`는 연결을 바꿉니다.

<!-- lecture-page -->

## 74 · 풀이의 출발점과 실행 추적

[LeetCode 74: Search a 2D Matrix](https://leetcode.com/problems/search-a-2d-matrix/) · Medium

행렬에서 target의 존재 여부를 반환합니다.

각 행이 정렬되어 있고 다음 행의 첫 값이 앞 행의 마지막 값보다 큽니다. 따라서 행을 이어 붙였다고 생각하면 하나의 정렬된 배열입니다. 실제로 복사할 필요 없이 가상의 위치를 행·열 번호로 바꿉니다.

`matrix=[[1,3,5],[7,9,11]], target=9`. 비교 직전의 범위와 갱신 결과입니다.

| left,right | mid | 행,열 | 값 | 다음 동작 |
| --- | --- | --- | --- | --- |
| 0,5 | 2 | 0,2 | 5 | 5 < 9 → left=3 |
| 3,5 | 4 | 1,1 | 9 | True 반환 |

<!-- lecture-page -->

## 74 · 아이디어를 코드로 옮기기

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

`mid // cols`는 앞에서 완전히 지난 행 수, `mid % cols`는 현재 행 안의 위치입니다. 예를 들어 4를 3으로 나누면 행 1, 열 1입니다.

값이 작으면 mid까지, 크면 mid부터 제거합니다. 이미 비교한 mid를 다시 남기지 않으므로 원소 하나가 남아도 탐색이 끝납니다.

<!-- lecture-page -->

## 74 · 정당성·시간·메모리의 근거

행 사이 조건까지 있으므로 평탄 배열은 정렬되어 있습니다. mid가 target보다 작으면 mid 이하를 제거합니다. 매 반복 구간이 줄고, 종료하면 후보가 없습니다.

원소 수를 N=R·C라 하면 비교 후 후보가 대략 N/2, N/4, …로 줄어듭니다. N=8이면 최대 4번 비교하며, 일반적으로 시간은 O(log(N+1))입니다. 각 비교의 행·열 계산과 리스트 접근은 O(1)입니다.

행렬을 평탄화한 새 리스트를 만들지 않습니다. left, right, mid 등 고정 개수의 값만 추가하므로 보조 공간은 O(1)입니다. `sum(matrix, [])` 같은 복사는 이 공간 분석에 포함되지 않는 다른 구현입니다.

left=mid는 길이 2 구간에서 정체할 수 있습니다. [[1,9],[2,10]]은 행만 정렬된 다른 문제입니다.

`matrix=[[1,4,7],[9,12,18]], target=12 → True`

<!-- lecture-page -->

## 없는 값을 찾을 때의 종료

같은 행렬 `[[1,3,5],[7,9,11]]`에서 target=8을 찾습니다. `[left,right]`는 양 끝을 포함한 아직 남은 위치입니다.

| 비교 전 범위 | mid와 값 | 제거 근거 | 다음 범위 |
| --- | --- | --- | --- |
| [0,5] | 2, 값 5 | 2 이하 값은 모두 8보다 작음 | [3,5] |
| [3,5] | 4, 값 9 | 4 이상 값은 모두 8보다 큼 | [3,3] |
| [3,3] | 3, 값 7 | 마지막 후보도 불일치 | [4,3] |

left>right이면 후보가 0개라 False입니다. left==right는 후보가 한 개 남은 상태이므로 검사해야 합니다. 첫 행의 갱신을 left=mid로 쓰면 `[3,4]`에서 mid=3을 반복할 수 있습니다.

범위 크기를 반씩 줄여 1개가 되려면 약 log₂N번이 필요하고, 마지막 한 개의 검사까지 더해 최악 비교 횟수는 floor(log₂N)+1입니다(N≥1).

<!-- lecture-page -->

## 33 · 풀이의 출발점과 실행 추적

[LeetCode 33: Search in Rotated Sorted Array](https://leetcode.com/problems/search-in-rotated-sorted-array/) · Medium

회전된 정렬 배열에서 target의 위치를 반환하고 없으면 -1입니다.

회전된 배열 전체는 정렬되어 있지 않아도, 서로 다른 값이라는 조건에서는 mid를 기준으로 적어도 한쪽 절반이 정렬되어 있습니다. 먼저 정렬된 쪽을 찾고, target이 그 값 범위에 들어가는지 확인하면 버릴 절반을 결정할 수 있습니다.

`nums=[4,5,6,7,0,1,2], target=0`

| left,mid,right | 정렬된 쪽 | target 검사 | 갱신 |
| --- | --- | --- | --- |
| 0,3,6 | 왼쪽: 4..7 | 0은 범위 밖 | left=4 |
| 4,5,6 | 왼쪽: 0..1 | 0은 범위 안 | right=4 |
| 4,4,4 | nums[4]=0 | 일치 | 4 반환 |

<!-- lecture-page -->

## 33 · 아이디어를 코드로 옮기기

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

`nums[left] <= nums[mid]`이면 왼쪽이 정렬되어 있습니다. `nums[left] <= target < nums[mid]`일 때만 그쪽을 남깁니다. mid는 앞의 일치 검사에서 처리했으므로 target 범위의 mid 쪽 끝은 엄격한 부등식입니다.

오른쪽이 정렬된 경우도 같은 논리입니다. 위치를 반환하므로 정렬을 새로 하면 원래 위치 정보와 회전 구조가 바뀝니다.

<!-- lecture-page -->

## 33 · 정당성·시간·메모리의 근거

서로 다른 값의 한 번 회전 배열에서는 적어도 한 절반이 정렬되어 있습니다. 그 범위 안/밖 검사는 target을 포함할 수 없는 절반만 제거하며 mid±1로 진전합니다.

각 반복에서 mid를 제외한 한쪽 절반만 남깁니다. 비교 횟수는 입력을 몇 번 반으로 줄일 수 있는지에 따라 O(log(n+1))이고, 반복 안의 고정 개수 비교·접근은 O(1)입니다.

새 배열이나 재귀 호출을 만들지 않아 보조 공간은 O(1)입니다. 중복을 허용하면 `[1,1,1,0,1]`처럼 양 끝과 mid가 같아 정렬된 쪽을 판별할 수 없는 경우가 생깁니다. 이 복잡도와 코드는 서로 다른 값 조건에 의존합니다.

중복을 허용한 [1,0,1,1,1]에서는 양 끝과 mid가 같아 정렬 방향 판정이 모호합니다. 공식 제약 밖 확장입니다.

`nums=[6,8,1,3,5], target=3 → 3`

<!-- lecture-page -->

## 206 · 풀이의 출발점과 실행 추적

[LeetCode 206: Reverse Linked List](https://leetcode.com/problems/reverse-linked-list/) · Easy

단일 연결 리스트를 뒤집고 새 head를 반환합니다.

리스트의 순서는 값이 저장된 위치가 아니라 next 연결로 정해집니다. 새 노드를 만들지 않고 현재 노드의 next를 앞쪽으로 돌립니다. 다만 연결을 바꾸기 전에 원래 다음 노드를 저장해야 아직 처리하지 않은 부분을 잃지 않습니다.

입력 `1 → 2 → 3 → None`. 각 행은 while 본문을 한 번 끝낸 상태입니다.

| 처리한 노드 | previous가 가리키는 부분 | current가 가리키는 부분 |
| --- | --- | --- |
| 없음 | None | 1 → 2 → 3 |
| 1 | 1 → None | 2 → 3 |
| 2 | 2 → 1 → None | 3 |
| 3 | 3 → 2 → 1 → None | None |

<!-- lecture-page -->

## 206 · 아이디어를 코드로 옮기기

```python
def reverse_list(head):
    previous, current = None, head
    while current:
        following = current.next
        current.next = previous
        previous, current = current, following
    return previous
```

`following = current.next`: 원래 다음 노드를 보존합니다. `current.next = previous`: 현재 연결 하나를 뒤집습니다. 마지막 동시 대입은 previous를 방금 처리한 노드로, current를 보존한 다음 노드로 옮깁니다.

current가 None이면 미처리 노드가 없습니다. 새 머리는 previous입니다. 빈 입력에서는 반복을 한 번도 실행하지 않고 None을 반환합니다.

2를 처리하는 순간 previous는 1, current는 2, following은 3을 가리킵니다. next 변경 뒤 동시 대입의 오른쪽 `(current,following)`은 먼저 `(2,3)`으로 평가됩니다. 그러므로 previous는 2, current는 3이 됩니다. `current=current.next`로 전진하면 이미 뒤집힌 연결을 따라 1로 되돌아가므로 저장한 following을 사용합니다.

<!-- lecture-page -->

## 206 · 정당성·시간·메모리의 근거

반복 시작 때 previous는 처리한 접두부의 역순, current는 미처리 접미부입니다. 한 노드를 옮겨도 둘의 합은 원래 노드 전체입니다. current가 None이면 previous가 완성된 역순입니다.

노드 n개를 각각 한 번 방문하고, 방문마다 고정 개수의 참조 대입을 하므로 시간은 O(n)입니다. 첫 노드를 바꾸었다고 뒤 노드의 연결까지 자동으로 바뀌지는 않아 모든 노드를 처리해야 합니다.

previous, current, following의 세 참조만 추가합니다. 입력 노드를 재사용하므로 보조 공간은 O(1), 새 출력 노드 수는 0입니다. 노드의 개수 O(n)과 추가로 사용한 공간 O(1)을 구분합니다. 재귀 구현은 호출 스택 O(n)이 필요합니다.

다음 참조를 먼저 저장하지 않으면 나머지 연결을 잃습니다. 같은 값의 두 노드도 서로 다른 객체입니다.

`head=[4,6,9] → [9,6,4]`

<!-- lecture-page -->

## 21 · 풀이의 출발점과 실행 추적

[LeetCode 21: Merge Two Sorted Lists](https://leetcode.com/problems/merge-two-sorted-lists/) · Easy

정렬된 두 연결 리스트의 노드를 이어 하나의 정렬 리스트로 반환합니다.

두 정렬된 리스트에서 가장 작은 남은 값은 두 머리 중 하나입니다. 작은 머리를 결과의 꼬리에 연결한 뒤 그 리스트만 한 칸 전진합니다. 뒤쪽 노드를 매번 다시 검색할 필요가 없습니다.

입력 A=`1 → 4`, B=`2 → 3`. tail 뒤에 아직 붙어 있는 입력 연결은 다음 대입에서 바뀔 수 있습니다.

| 선택 | 확정된 결과 접두부 | A 머리 | B 머리 |
| --- | --- | --- | --- |
| 시작 | 없음 | 1 | 2 |
| A의 1 | 1 | 4 | 2 |
| B의 2 | 1 → 2 | 4 | 3 |
| B의 3 | 1 → 2 → 3 | 4 | None |
| 남은 A 연결 | 1 → 2 → 3 → 4 | 4 | None |

<!-- lecture-page -->

## 21 · 아이디어를 코드로 옮기기

```python
from structures import ListNode

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

dummy는 첫 삽입도 나머지 삽입과 같게 처리하는 임시 머리입니다. `tail.next, first = first, first.next`는 갱신 전 first를 연결하고 원래 다음 노드로 first를 옮깁니다.

한쪽이 비면 다른 쪽은 이미 정렬되어 있으므로 `tail.next = first or second`로 나머지 사슬 전체를 연결합니다. 반환할 때 dummy는 제외합니다.

<!-- lecture-page -->

## 21 · 정당성·시간·메모리의 근거

tail까지는 정렬된 병합 접두부입니다. 두 head 중 작은 것은 남은 모든 값 중 최소이므로 다음 노드로 안전합니다. 남은 접미부도 정렬되어 있습니다.

길이가 n, m이면 반복 한 번마다 한 노드가 확정됩니다. 두 리스트가 번갈아 선택되는 경우 O(n+m)번의 작업이 필요합니다. 남은 사슬을 연결하는 마지막 대입은 O(1)입니다.

dummy 한 개와 고정 개수의 참조만 추가하므로 보조 공간은 O(1)입니다. 결과에 n+m개 노드가 있어도 기존 입력 노드를 다시 연결한 것이므로 새 노드 n+m개를 저장하지 않습니다. 입력 연결을 보존해야 한다면 복사 구현과 O(n+m) 공간이 필요합니다.

head 대신 dummy를 반환하면 가짜 값이 포함됩니다. 이 구현은 서로 겹치지 않고 사이클 없는 입력 리스트를 전제로 합니다.

`first=[1,5], second=[2,3] → [1,2,3,5]`

<!-- lecture-page -->

## 실습과 참고자료

[LeetCode · 74, 33, 206, 21](/courses/practical-algorithms/week-03-practice/) · [풀이](/courses/practical-algorithms/week-03-reading/) · [Python ZIP](/assets/courses/practical-algorithms/week-03-code.zip)

```text
python demo_05.py
python demo_06.py
python verify.py
```

학생 파일을 구현한 뒤 `python verify.py --student`로 검사합니다.

Erik Demaine, Srini Devadas. [MIT 6.006, Introduction to Algorithms](https://ocw.mit.edu/courses/6-006-introduction-to-algorithms-fall-2011/) (2011).
