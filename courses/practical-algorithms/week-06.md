---
layout: "course-note"
title: "Week 6: Dependencies and backtracking"
title_ko: "6주차: 의존관계와 백트래킹"
course_id: "practical-algorithms"
permalink: "/courses/practical-algorithms/week-06/"
updated: "2026-11-12"
material_label: "Week 6 lecture"
material_label_ko: "6주차 강의"
pdf_en: "/assets/courses/practical-algorithms/week-06-en.pdf"
pdf_ko: "/assets/courses/practical-algorithms/week-06-ko.pdf"
reading_note: "/courses/practical-algorithms/week-06-reading/"
lab_bundle: "/assets/courses/practical-algorithms/week-06-code.zip"
practice_note: "/courses/practical-algorithms/week-06-practice/"
reading_pdf_en: "/assets/courses/practical-algorithms/week-06-reading-en.pdf"
reading_pdf_ko: "/assets/courses/practical-algorithms/week-06-reading-ko.pdf"
---

## Prerequisites and possible choices

A pipeline stops when its jobs wait on each other. Find a feasible execution order, then enumerate the choices that can be made from a given set of items.

Use remaining prerequisites to schedule jobs. Choose, recurse, and restore to keep one search branch from changing the next.

### Learning outcomes

Sessions 11 and 12: Indegree, cycles, choice paths, and restoration

- Check contracts and boundary conditions.
- Trace state and implement in Python.
- Explain correctness, time, auxiliary space, and output space.

<!-- lecture-page -->

## Edge direction and adjacency lists

`[after,before]` means before must finish before after can begin. Store the edge before → after. indegree counts unfinished prerequisites.

![Tasks 1 and 2 follow 0, and both precede task 3](/assets/courses/practical-algorithms/curriculum/dependency-dag.svg)

| Stored item | Value in this graph | Meaning |
| --- | --- | --- |
| graph | [[1,2],[3],[3],[]] | Tasks affected when each task finishes |
| indegree | [0,1,1,2] | Remaining prerequisite counts |
| Initial queue | [0] | Tasks ready now |

The graph stores E edge entries. Unlike a V-by-V matrix, an adjacency list uses storage proportional to V+E.

<!-- lecture-page -->

## 207 · Idea and execution trace

[LeetCode 207: Course Schedule](https://leetcode.com/problems/course-schedule/) · Medium

Decide whether all courses can be completed under prerequisite constraints.

If no remaining course can start, look for circular waiting. Repeatedly remove zero-prerequisite courses and check whether all courses were removed. Any nonempty remainder contains a directed cycle.

`n=3, prerequisites=[[1,0],[2,1],[1,2]]`: 0 → 1, 1 → 2, 2 → 1

| Stage | indegree | queue | Processed |
| --- | --- | --- | --- |
| Initial | [0,2,1] | [0] | [] |
| Complete 0 | [0,1,1] | [] | [0] |
| Stop | 1 and 2 wait on each other | [] | 1 course < 3 |

`course_order` returns [] rather than a partial order; `can_finish` returns False.

<!-- lecture-page -->

## 207 · Turning the idea into code

```python
def can_finish(n, prerequisites):
    return len(course_order(n, prerequisites)) == n
```

The one-line call in `can_finish` executes the entire `course_order` traversal below. A function call written on one line does not imply one unit of work.

On a cycle, every course retains an unfinished prerequisite. Every nonempty finite acyclic directed graph has a zero-indegree vertex, so removal can continue until nothing remains.

The called routine processes V vertices and E edges at most once, taking O(V+E) time. Only len and the final comparison are O(1); the earlier traversal still counts.

Adjacency storage costs O(V+E), while indegrees, queue, and order cost O(V). The returned bool occupies O(1), but peak auxiliary space during execution is O(V+E). Output size alone does not determine workspace.

<!-- lecture-page -->

## 210 · Idea and execution trace

[LeetCode 210: Course Schedule II](https://leetcode.com/problems/course-schedule-ii/) · Medium

Return any prerequisite-respecting order, or an empty list if impossible.

Instead of rechecking every prerequisite repeatedly, store each task’s remaining prerequisite count. A count of zero means it can run now. Completing a task decrements only the counts of tasks that depend on it.

`n=4, prerequisites=[[1,0],[2,0],[3,1],[3,2]]`. Edges point before → after.

| Completed node | indegree (0,1,2,3) | queue | order |
| --- | --- | --- | --- |
| Initial | [0,1,1,2] | [0] | [] |
| 0 | [0,0,0,2] | [1,2] | [0] |
| 1 | [0,0,0,1] | [2] | [0,1] |
| 2 | [0,0,0,0] | [3] | [0,1,2] |
| 3 | [0,0,0,0] | [] | [0,1,2,3] |

<!-- lecture-page -->

## 210 · Turning the idea into code

```python
from collections import deque

def course_order(n, prerequisites):
    graph, indegree = [[] for _ in range(n)], [0] * n
    for after, before in prerequisites:
        graph[before].append(after)
        indegree[after] += 1
    queue = deque(v for v in range(n) if indegree[v] == 0)
    order = []
    while queue:
        node = queue.popleft()
        order.append(node)
        for neighbor in graph[node]:
            indegree[neighbor] -= 1
            if indegree[neighbor] == 0:
                queue.append(neighbor)
    return order if len(order) == n else []
```

For `[after,before]`, append after to `graph[before]`. When removing a node, decrement its neighbors’ indegrees and enqueue a neighbor exactly when its count reaches zero.

Problem 207 asks whether all tasks can be included; problem 210 returns the order itself. Choosing any currently available task preserves prerequisite validity.

<!-- lecture-page -->

## 210 · Why it works; time and memory

A course enters only after all prerequisites were removed, so every before precedes after in the result. A short result cannot be a complete order.

Initialization stores V vertices and E edges in O(V+E) work. Each vertex enters the queue once; each edge is read once when its source is processed. Degrees vary, but their sum is E, giving total O(V+E) time.

There are V adjacency lists with E entries, plus up to V entries in indegree, queue, and order. Total extra space is O(V+E), including O(V) output order. Although 207 returns only a bool, this implementation calls the same order routine and uses O(V+E) space.

<!-- lecture-page -->

## 78 · Idea and execution trace

[LeetCode 78: Subsets](https://leetcode.com/problems/subsets/) · Medium

Return every subset of an array of distinct values.

Restrict each next selection to a later index. This generates [2,5] once rather than also generating [5,2]. Every current path is itself a subset, so record it starting with the empty path.

`nums=[2,5]`. A snapshot is stored immediately on entering visit.

| Execution | path | Snapshot stored |
| --- | --- | --- |
| visit(0) | [] | [] |
| append(2), visit(1) | [2] | [2] |
| append(5), visit(2) | [2,5] | [2,5] |
| pop(), pop() | [] | None |
| append(5), visit(2) | [5] | [5] |

Output order: `[[],[2],[2,5],[5]]`.

<!-- lecture-page -->

## 78 · Turning the idea into code

```python
def subsets(nums):
    result, path = [], []

    def visit(start):
        result.append(path.copy())
        for index in range(start, len(nums)):
            path.append(nums[index])
            visit(index + 1)
            path.pop()

    visit(0)
    return result
```

Append one choice, then explore from `index+1`. On return, pop that choice so another branch starts from the same parent path.

`path.copy()` stores an independent snapshot. Appending path itself would make outputs refer to one mutable list and change together after later pops. Input elements are distinct.

<!-- lecture-page -->

## 78 · Why it works; time and memory

Every subset has one increasing index sequence. start permits exactly that sequence, and restoration returns the parent path to its prior state.

Each element can be included or excluded, giving <math xmlns="http://www.w3.org/1998/Math/MathML"><msup><mn>2</mn><mi>n</mi></msup></math> subsets. For n>=1, each element occurs in half of them, so snapshots copy n·<math xmlns="http://www.w3.org/1998/Math/MathML"><msup><mn>2</mn><mrow><mi>n</mi><mo>−</mo><mn>1</mn></mrow></msup></math> elements in total. Materializing the output takes O(n·<math xmlns="http://www.w3.org/1998/Math/MathML"><msup><mn>2</mn><mi>n</mi></msup></math>) time and output space.

The current path and recursion depth are each at most n, so auxiliary space excluding output is O(n). Time counts all work; space counts paths and calls alive at the same moment, not every call ever made.

<!-- lecture-page -->

## 39 · Idea and execution trace

[LeetCode 39: Combination Sum](https://leetcode.com/problems/combination-sum/) · Medium

Return unique combinations reaching target with unlimited candidate reuse.

Choose positive candidates to decrease the remaining sum. Reuse is allowed, so recurse from the selected index again. Never return to earlier indices; this avoids permutation duplicates such as [2,3] and [3,2].

`candidates=[2,3], target=5`. remaining is the sum still required.

| path | remaining | Next action |
| --- | --- | --- |
| [] | 5 | Choose 2 |
| [2] | 3 | Reuse 2 |
| [2,2] | 1 | 2 > 1 → return |
| [2,3] | 0 | Save snapshot; return |
| [3] | 2 | 3 > 2 → stop |

Output: `[[2,3]]`.

<!-- lecture-page -->

## 39 · Turning the idea into code

```python
def combinations(candidates, target):
    values, result, path = sorted(candidates), [], []

    def visit(start, remaining):
        if remaining == 0:
            result.append(path.copy())
            return
        for index in range(start, len(values)):
            value = values[index]
            if value > remaining:
                break
            path.append(value)
            visit(index, remaining - value)
            path.pop()

    visit(0, target)
    return result
```

After sorting, if `value > remaining`, every later candidate is also too large. This permits break rather than continue. Save a snapshot only when remaining becomes zero.

`visit(index, ...)` allows reuse; the subsets routine uses `index+1` to forbid it. Positivity ensures remaining decreases and recursion terminates.

<!-- lecture-page -->

## 39 · Why it works; time and memory

Positive choices decrease remaining and ensure termination. Nondecreasing indices avoid permutations while representing every combination.

With m candidates, target T, and smallest candidate c, path length is at most L=floor(T/c). Let B be visited calls and S the total output elements. Sorting costs O(m log m), each call checks at most m choices, and copying costs O(S): total O(m log m+mB+S). B depends strongly on the input; this is not a linear scan.

A conservative bound is B=O(<math xmlns="http://www.w3.org/1998/Math/MathML"><msup><mrow><mo>(</mo><mi>m</mi><mo>+</mo><mn>1</mn><mo>)</mo></mrow><mrow><mi>L</mi><mo>+</mo><mn>1</mn></mrow></msup></math>). The sorted candidates plus the path and call stack use O(m+L) auxiliary space. Output uses O(S); the full search tree is not stored simultaneously.

<!-- lecture-page -->

## Checkpoint questions

1. Find an execution order for `[[1,0],[0,1]]`.
2. Is `[1,0,2]` valid for `[[2,0],[2,1]]`?
3. How many subsets does `[2,5]` have, including the empty subset?
4. For candidates `[2]` and target 4, which index should the recursive call reuse?

### Exercises and sources

[LeetCode · 207, 210, 78, 39](/courses/practical-algorithms/week-06-practice/) · [Worked solutions](/courses/practical-algorithms/week-06-reading/) · [Python ZIP](/assets/courses/practical-algorithms/week-06-code.zip)

```text
python demo_11.py
python demo_12.py
python verify.py
```

After implementing the student file, check it with `python verify.py --student`.

Erik Demaine, Srini Devadas. [MIT 6.006, Introduction to Algorithms](https://ocw.mit.edu/courses/6-006-introduction-to-algorithms-fall-2011/) (2011).

<!-- ko -->

## 선행 작업과 가능한 선택

분석 파이프라인의 작업이 서로를 기다리면 실행이 멈춥니다. 실행 가능한 순서를 찾은 뒤에는 주어진 항목으로 만들 수 있는 선택을 빠짐없이 생성해야 합니다.

남은 선행 조건으로 실행 순서를 정하고, 선택·재귀·복원으로 분기 간 상태를 분리합니다.

### 학습 목표

11·12차시: 진입차수·사이클·선택 경로·복원

- 입력 계약과 경계 조건 확인
- 상태 추적과 Python 구현
- 정당성·시간·보조 공간·출력 공간 설명

<!-- lecture-page -->

## 의존관계의 방향과 인접 리스트

`[after,before]`는 before가 끝나야 after를 시작할 수 있다는 뜻입니다. before → after 방향으로 간선을 저장합니다. 진입차수 indegree는 아직 끝나지 않은 선행 작업의 수입니다.

![작업 0 뒤에 1과 2, 두 작업 뒤에 3을 수행하는 그래프](/assets/courses/practical-algorithms/curriculum/dependency-dag.svg)

| 저장 항목 | 이 그림의 값 | 의미 |
| --- | --- | --- |
| graph | [[1,2],[3],[3],[]] | 각 작업 완료 시 영향을 받는 작업 |
| indegree | [0,1,1,2] | 남은 선행 작업 수 |
| 초기 queue | [0] | 지금 바로 할 수 있는 작업 |

graph는 간선 E개를 저장합니다. 정점마다 전체 V개를 넣는 행렬과 달리 인접 리스트의 전체 항목 수는 V+E에 비례합니다.

<!-- lecture-page -->

## 207 · 풀이의 출발점과 실행 추적

[LeetCode 207: Course Schedule](https://leetcode.com/problems/course-schedule/) · Medium

선수 과목 조건을 모두 만족하며 전체 과목을 끝낼 수 있는지 반환합니다.

어떤 과목도 시작할 수 없다면 서로 기다리는 고리가 있는지 의심해야 합니다. 선행 과목 수가 0인 과목을 반복해서 제거한 뒤 모든 과목을 제거했는지가 판정 기준입니다. 남은 과목이 있다면 그 안에 유향 사이클이 있습니다.

`n=3, prerequisites=[[1,0],[2,1],[1,2]]`: 0 → 1, 1 → 2, 2 → 1

| 단계 | indegree | queue | 처리한 과목 |
| --- | --- | --- | --- |
| 시작 | [0,2,1] | [0] | [] |
| 0 완료 | [0,1,1] | [] | [0] |
| 종료 | 1과 2가 서로 대기 | [] | 1개 < 3개 |

`course_order`는 미완료 순서 대신 []를 반환하고, `can_finish`는 False입니다.

<!-- lecture-page -->

## 207 · 아이디어를 코드로 옮기기

```python
def can_finish(n, prerequisites):
    return len(course_order(n, prerequisites)) == n
```

`can_finish`의 한 줄은 뒤의 `course_order` 전체 탐색을 실행합니다. 함수 호출을 한 줄로 썼다고 계산이 한 번으로 끝나는 것은 아닙니다.

사이클이 있으면 그 위의 모든 과목이 적어도 하나의 미완료 선행 과목을 유지합니다. 사이클이 없는 유한 유향 그래프에는 진입차수 0인 정점이 하나 이상 있으므로 계속 제거할 수 있습니다.

호출한 `course_order`가 모든 정점 V개와 간선 E개를 최대 한 번씩 처리하므로 O(V+E) 시간입니다. 반환된 리스트의 len 조회와 n 비교만 O(1)이며, 그 전에 수행한 탐색 비용을 빼면 안 됩니다.

인접 리스트 O(V+E), 진입차수·큐·순서 O(V)를 생성합니다. 반환값 False나 True는 O(1)이어도 실행 중 최대 보조 공간은 O(V+E)입니다. 공간은 최종 출력 크기만으로 정하지 않습니다.

<!-- lecture-page -->

## 210 · 풀이의 출발점과 실행 추적

[LeetCode 210: Course Schedule II](https://leetcode.com/problems/course-schedule-ii/) · Medium

선수 조건을 만족하는 순서 하나를 반환합니다. 불가능하면 빈 목록입니다.

의존관계를 매번 전부 확인하는 대신 아직 끝나지 않은 선행 작업 수를 각 작업에 저장합니다. 이 수가 0이면 지금 실행할 수 있습니다. 하나를 끝낼 때 그 작업을 기다리던 이웃들의 수만 1씩 줄입니다.

`n=4, prerequisites=[[1,0],[2,0],[3,1],[3,2]]`. 간선은 before → after입니다.

| 완료한 node | indegree (0,1,2,3) | queue | order |
| --- | --- | --- | --- |
| 시작 | [0,1,1,2] | [0] | [] |
| 0 | [0,0,0,2] | [1,2] | [0] |
| 1 | [0,0,0,1] | [2] | [0,1] |
| 2 | [0,0,0,0] | [3] | [0,1,2] |
| 3 | [0,0,0,0] | [] | [0,1,2,3] |

<!-- lecture-page -->

## 210 · 아이디어를 코드로 옮기기

```python
from collections import deque

def course_order(n, prerequisites):
    graph, indegree = [[] for _ in range(n)], [0] * n
    for after, before in prerequisites:
        graph[before].append(after)
        indegree[after] += 1
    queue = deque(v for v in range(n) if indegree[v] == 0)
    order = []
    while queue:
        node = queue.popleft()
        order.append(node)
        for neighbor in graph[node]:
            indegree[neighbor] -= 1
            if indegree[neighbor] == 0:
                queue.append(neighbor)
    return order if len(order) == n else []
```

`[after,before]`를 읽어 `graph[before]`에 after를 추가합니다. node를 꺼내면 그 이웃의 indegree를 줄이고, 정확히 0이 되는 순간에만 넣습니다.

207번은 이 순서에 모든 작업이 포함되는지만 반환합니다. 210번은 순서 자체를 반환합니다. 큐에서 가능한 작업 중 어느 것을 먼저 택해도 선행 조건을 지킨 순서가 됩니다.

<!-- lecture-page -->

## 210 · 정당성·시간·메모리의 근거

각 과목은 모든 선수가 제거된 뒤에만 큐에 들어갑니다. 따라서 반환 순서에서 모든 before의 위치가 after보다 앞섭니다. 수가 부족하면 전체 순서가 아닙니다.

정점 V개와 간선 E개를 저장하는 초기 작업이 O(V+E)입니다. 각 정점은 한 번 큐에 들어가고 각 간선은 출발 정점 처리 때 한 번만 읽습니다. 이웃 수가 정점마다 달라도 그 합은 E이므로 전체 시간은 O(V+E)입니다.

인접 리스트의 빈 목록 V개와 간선 항목 E개, indegree·queue·order의 최대 V개 항목이 필요합니다. 총 추가 공간은 O(V+E), 그중 반환 순서는 O(V)입니다. 207번의 반환값은 bool이지만 이 구현은 같은 순서 함수를 호출하므로 공간도 O(V+E)입니다.

<!-- lecture-page -->

## 78 · 풀이의 출발점과 실행 추적

[LeetCode 78: Subsets](https://leetcode.com/problems/subsets/) · Medium

서로 다른 값으로 이루어진 배열의 모든 부분집합을 반환합니다.

부분집합을 만들 때는 다음에 고를 위치를 현재 위치보다 뒤로 제한합니다. 그러면 [2,5]와 [5,2]를 따로 만들지 않습니다. 현재 경로 자체도 하나의 부분집합이므로 빈 경로부터 결과에 넣습니다.

`nums=[2,5]`. 결과 저장은 visit에 들어간 직후입니다.

| 실행 | path | 저장되는 복사본 |
| --- | --- | --- |
| visit(0) | [] | [] |
| append(2), visit(1) | [2] | [2] |
| append(5), visit(2) | [2,5] | [2,5] |
| pop(), pop() | [] | 없음 |
| append(5), visit(2) | [5] | [5] |

결과 순서는 `[[],[2],[2,5],[5]]`입니다.

<!-- lecture-page -->

## 78 · 아이디어를 코드로 옮기기

```python
def subsets(nums):
    result, path = [], []

    def visit(start):
        result.append(path.copy())
        for index in range(start, len(nums)):
            path.append(nums[index])
            visit(index + 1)
            path.pop()

    visit(0)
    return result
```

append로 한 선택을 한 뒤 `visit(index+1)`로 다음 위치부터 탐색합니다. 재귀가 돌아오면 pop으로 그 선택만 취소해야 같은 부모에서 다른 선택을 시험할 수 있습니다.

`path.copy()`는 현재 내용을 따로 저장합니다. path 자체를 넣으면 모든 결과가 같은 리스트를 가리켜 나중의 pop에 함께 바뀝니다. 입력 원소는 서로 다릅니다.

<!-- lecture-page -->

## 78 · 정당성·시간·메모리의 근거

부분집합마다 오름차순 인덱스 열이 하나 있습니다. start가 그 열만 허용하므로 모든 부분집합을 정확히 한 번 만듭니다. 복원 후 부모의 path는 호출 전과 같습니다.

원소마다 포함·제외 두 가능성이 있어 부분집합은 <math xmlns="http://www.w3.org/1998/Math/MathML"><msup><mn>2</mn><mi>n</mi></msup></math>개입니다. n>=1일 때 각 원소는 정확히 절반의 부분집합에 들어가므로 복사하는 원소 수의 합은 n·<math xmlns="http://www.w3.org/1998/Math/MathML"><msup><mn>2</mn><mrow><mi>n</mi><mo>−</mo><mn>1</mn></mrow></msup></math>입니다. 결과를 실제 리스트로 만드는 시간과 출력 공간은 O(n·<math xmlns="http://www.w3.org/1998/Math/MathML"><msup><mn>2</mn><mi>n</mi></msup></math>)입니다.

현재 path 길이와 재귀 깊이는 각각 최대 n이므로 출력을 제외한 보조 공간은 O(n)입니다. 시간은 전체 탐색량, 공간은 동시에 살아 있는 경로와 호출을 셉니다. 호출 총수를 전부 동시에 저장한다고 계산하지 않습니다.

<!-- lecture-page -->

## 39 · 풀이의 출발점과 실행 추적

[LeetCode 39: Combination Sum](https://leetcode.com/problems/combination-sum/) · Medium

후보를 반복 사용해 target 합을 만드는 중복 없는 조합을 반환합니다.

양수 후보를 골라 남은 합을 줄입니다. 같은 후보를 여러 번 사용할 수 있으므로 고른 위치부터 다시 탐색합니다. 대신 앞 위치로 돌아가지 않아 [2,3]과 [3,2] 같은 순열 중복을 만들지 않습니다.

`candidates=[2,3], target=5`. remaining은 아직 채워야 할 합입니다.

| path | remaining | 다음 동작 |
| --- | --- | --- |
| [] | 5 | 2 선택 |
| [2] | 3 | 2 재사용 |
| [2,2] | 1 | 2 > 1 → 복귀 |
| [2,3] | 0 | 복사 저장 후 복귀 |
| [3] | 2 | 3 > 2 → 종료 |

결과는 `[[2,3]]`입니다.

<!-- lecture-page -->

## 39 · 아이디어를 코드로 옮기기

```python
def combinations(candidates, target):
    values, result, path = sorted(candidates), [], []

    def visit(start, remaining):
        if remaining == 0:
            result.append(path.copy())
            return
        for index in range(start, len(values)):
            value = values[index]
            if value > remaining:
                break
            path.append(value)
            visit(index, remaining - value)
            path.pop()

    visit(0, target)
    return result
```

정렬했기 때문에 `value > remaining`이면 뒤 후보도 전부 너무 큽니다. 그래서 continue가 아니라 break할 수 있습니다. remaining이 0일 때만 복사본을 저장합니다.

`visit(index, ...)`는 재사용, 부분집합의 `visit(index+1)`은 해당 원소 재사용 금지입니다. 양수 조건이 있어야 매 호출에서 remaining이 줄고 탐색이 종료합니다.

<!-- lecture-page -->

## 39 · 정당성·시간·메모리의 근거

양수 선택마다 remaining이 감소해 종료합니다. 비내림차순 인덱스만 선택하므로 순서만 다른 중복을 피하고 모든 가능한 조합을 표현합니다.

후보 수 m, 목표 T, 최소 후보 c라 하면 경로 길이는 L=floor(T/c) 이하입니다. 방문 호출 수 B, 출력 원소 수의 합 S를 쓰면 정렬 O(m log m), 호출당 최대 m개 검사, 복사 O(S)이므로 O(m log m+mB+S) 시간입니다. B는 입력에 따라 크게 달라져 이를 단순 O(n)이라 할 수 없습니다.

보수적으로 B=O(<math xmlns="http://www.w3.org/1998/Math/MathML"><msup><mrow><mo>(</mo><mi>m</mi><mo>+</mo><mn>1</mn><mo>)</mo></mrow><mrow><mi>L</mi><mo>+</mo><mn>1</mn></mrow></msup></math>)입니다. 정렬한 후보 m개와 길이 L의 path·호출 스택이 있어 보조 공간 O(m+L), 출력은 O(S)입니다. 전체 탐색 트리를 한 번에 저장하지는 않습니다.

<!-- lecture-page -->

## 중간 점검

1. 조건 `[[1,0],[0,1]]`을 만족하는 실행 순서는?
2. 조건 `[[2,0],[2,1]]`에서 `[1,0,2]`도 정답인가요?
3. `[2,5]`의 부분집합 수와 빈 부분집합은?
4. 후보 `[2]`, 목표 4에서 다음 재귀 인덱스는?

### 실습과 참고자료

[LeetCode · 207, 210, 78, 39](/courses/practical-algorithms/week-06-practice/) · [풀이](/courses/practical-algorithms/week-06-reading/) · [Python ZIP](/assets/courses/practical-algorithms/week-06-code.zip)

```text
python demo_11.py
python demo_12.py
python verify.py
```

학생 파일을 구현한 뒤 `python verify.py --student`로 검사합니다.

Erik Demaine, Srini Devadas. [MIT 6.006, Introduction to Algorithms](https://ocw.mit.edu/courses/6-006-introduction-to-algorithms-fall-2011/) (2011).
