# Week 6 lab / 6주차 실습

## Set up and run

Extract the [lab code ZIP](https://sunboogermany.github.io/assets/courses/practical-algorithms/week-06-code.zip) and work in its code folder. Use Python 3.11+ and the standard library.

```text
python trace_lab.py --case can_finish
python verify.py
python verify.py --student
```

Predict the small example and its states on paper first. `trace_lab.py` traces the actual `solutions.py` implementation. `before L…` shows values immediately before that line executes: identify what the preceding executed line changed. Linked lists display a chain; tree nodes display their value and child values. Exclude tracing, copying, and printing overhead from the algorithm's complexity.

Implement the functions and methods in `student_week_06.py`, then run `verify.py --student`. An initial `NotImplementedError` identifies work still to implement. Without `--student`, the verifier checks the supplied solutions. Use `python trace_lab.py --case FUNCTION --student` to inspect your implementation.

For each task record the input/output meaning, state invariant, one state transition, final answer, time, auxiliary space, and output space. Passing one small example does not establish correctness for all inputs.

## This week’s problems

- [can_finish](#en-can_finish)
- [course_order](#en-course_order)
- [subsets](#en-subsets)
- [combinations](#en-combinations)

## Worked solutions

207 | 210 | 78 | 39

A pipeline stops when its jobs wait on each other. Find a feasible execution order, then enumerate the choices that can be made from a given set of items.

Use remaining prerequisites to schedule jobs. Choose, recurse, and restore to keep one search branch from changing the next.

## Edge direction and adjacency lists

`[after,before]` means before must finish before after can begin. Store the edge before → after. indegree counts unfinished prerequisites.

![Tasks 1 and 2 follow 0, and both precede task 3](figures/dependency-dag.svg)

| Stored item | Value in this graph | Meaning |
| --- | --- | --- |
| graph | [[1,2],[3],[3],[]] | Tasks affected when each task finishes |
| indegree | [0,1,1,2] | Remaining prerequisite counts |
| Initial queue | [0] | Tasks ready now |

The graph stores E edge entries. Unlike a V-by-V matrix, an adjacency list uses storage proportional to V+E.

<a id="en-can_finish"></a>

## [LeetCode 207: Course Schedule](https://leetcode.com/problems/course-schedule/) · Medium

Decide whether all courses can be completed under prerequisite constraints.

1 <= V <= 2000; 0 <= E <= 5000; pairs [after,before], no duplicate pairs.

### Predict before implementing

Build prerequisite→course edges and incoming counts. Only zero-indegree vertices enter the queue. This cycle has no initial ready course; processed count stays zero. Remove [0,2] to make all three processable.

```python
can_finish(3, [[1, 0], [2, 1], [0, 2]])
# False
```

### Idea and state transitions

#### 207 · Idea and execution trace

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

### Implement and execute

```python
from collections import deque
import heapq

def can_finish(n, prerequisites):
    return len(course_order(n, prerequisites)) == n
```

```text
python trace_lab.py --case can_finish
```

Compare the trace return value with your prediction. Make the input change proposed above, find the first line where the state differs, and explain its effect on the answer.

<a id="en-course_order"></a>

## [LeetCode 210: Course Schedule II](https://leetcode.com/problems/course-schedule-ii/) · Medium

Return any prerequisite-respecting order, or an empty list if impossible.

1 <= V <= 2000; 0 <= E <= V(V-1); distinct endpoints and unique [after,before] pairs.

### Predict before implementing

Append each ready course to the order before reducing its successors’ indegrees. Course 3 becomes ready only after both 1 and 2. Validate every edge using positions; [0,2,1,3] is also valid.

```python
course_order(4, [[1, 0], [2, 0], [3, 1], [3, 2]])
# [0, 1, 2, 3]
```

### Idea and state transitions

#### 210 · Idea and execution trace

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

#### 210 · Why it works; time and memory

A course enters only after all prerequisites were removed, so every before precedes after in the result. A short result cannot be a complete order.

Initialization stores V vertices and E edges in O(V+E) work. Each vertex enters the queue once; each edge is read once when its source is processed. Degrees vary, but their sum is E, giving total O(V+E) time.

There are V adjacency lists with E entries, plus up to V entries in indegree, queue, and order. Total extra space is O(V+E), including O(V) output order. Although 207 returns only a bool, this implementation calls the same order routine and uses O(V+E) space.

Reading [[1,0]] as 1→0 reverses the dependency. Validate edges instead of comparing with one chosen valid order.

`n=4, prerequisites=[[2,0],[2,1],[3,2]] → [0,1,2,3]`

`[[] for _ in range(n)]` creates a separate neighbor list per vertex. `[[]]*n` shares one list, so `graph[0].append(1)` would add 1 to every vertex's neighbors. An indegree reaches zero only once, which prevents duplicate queue insertion on valid inputs.

### Implement and execute

```python
from collections import deque
import heapq

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

```text
python trace_lab.py --case course_order
```

Compare the trace return value with your prediction. Make the input change proposed above, find the first line where the state differs, and explain its effect on the answer.

<a id="en-subsets"></a>

## [LeetCode 78: Subsets](https://leetcode.com/problems/subsets/) · Medium

Return every subset of an array of distinct values.

1 <= n <= 10; values -10..10; all distinct.

### Predict before implementing

At each search node, save a copy of path. Choose an element, recurse on later positions, then pop it. Saving path itself aliases one changing list. With n=2, there are four outputs including the empty subset.

```python
subsets([1, 2],)
# [[], [1], [1, 2], [2]]
```

### Idea and state transitions

#### 78 · Idea and execution trace

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

#### 78 · Why it works; time and memory

Every subset has one increasing index sequence. start permits exactly that sequence, and restoration returns the parent path to its prior state.

Each element can be included or excluded, giving <math xmlns="http://www.w3.org/1998/Math/MathML"><msup><mn>2</mn><mi>n</mi></msup></math> subsets. For n>=1, each element occurs in half of them, so snapshots copy n·<math xmlns="http://www.w3.org/1998/Math/MathML"><msup><mn>2</mn><mrow><mi>n</mi><mo>−</mo><mn>1</mn></mrow></msup></math> elements in total. Materializing the output takes O(n·<math xmlns="http://www.w3.org/1998/Math/MathML"><msup><mn>2</mn><mi>n</mi></msup></math>) time and output space.

The current path and recursion depth are each at most n, so auxiliary space excluding output is O(n). Time counts all work; space counts paths and calls alive at the same moment, not every call ever made.

result.append(path) stores one shared object; later pops can turn multiple results into empty lists.

`nums=[2,5] → [[],[2],[2,5],[5]]`

### Implement and execute

```python
from collections import deque
import heapq

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

```text
python trace_lab.py --case subsets
```

Compare the trace return value with your prediction. Make the input change proposed above, find the first line where the state differs, and explain its effect on the answer.

<a id="en-combinations"></a>

## [LeetCode 39: Combination Sum](https://leetcode.com/problems/combination-sum/) · Medium

Return unique combinations reaching target with unlimited candidate reuse.

1..30 distinct candidates, each 2..40; target 1..40; fewer than 150 answer combinations.

### Predict before implementing

Track remaining target and the first allowed candidate index. Reuse the chosen index to permit repeats, but never return to smaller indices. Stop at remaining=0. Explain why [3,2,2] is not a second answer.

```python
combinations([2, 3, 6, 7], 7)
# [[2, 2, 3], [7]]
```

### Idea and state transitions

#### 39 · Idea and execution trace

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

#### Returning to the parent's next choice

For candidates [2,3] and target 5, each call owns its start and remaining variables; only path is shared. Returning from a child resumes the parent's loop at the next statement.

| Execution point | Shared path | This call's remaining |
| --- | --- | --- |
| Parent visit(0,3), append 2 | [2,2] | 3 |
| Child visit(0,1), stop because 2>1 | [2,2] | 1 |
| Resume parent, path.pop() | [2] | still 3 |
| Parent's next index=1, append 3 | [2,3] | 3 |
| Child visit(1,0), save a copy and return | [2,3] | 0 |
| Resume parent, path.pop() | [2] | 3 |

The parent in the first row has already selected the first 2. pop undoes the last shared path choice. The parent's remaining was never changed, so it needs no addition to restore it. An implementation that mutates a global remaining would have to restore that value too.

#### 39 · Why it works; time and memory

Positive choices decrease remaining and ensure termination. Nondecreasing indices avoid permutations while representing every combination.

With m candidates, target T, and smallest candidate c, path length is at most L=floor(T/c). Let B be visited calls and S the total output elements. Sorting costs O(m log m), each call checks at most m choices, and copying costs O(S): total O(m log m+mB+S). B depends strongly on the input; this is not a linear scan.

A conservative bound is B=O(<math xmlns="http://www.w3.org/1998/Math/MathML"><msup><mrow><mo>(</mo><mi>m</mi><mo>+</mo><mn>1</mn><mo>)</mo></mrow><mrow><mi>L</mi><mo>+</mo><mn>1</mn></mrow></msup></math>). The sorted candidates plus the path and call stack use O(m+L) auxiliary space. Output uses O(S); the full search tree is not stored simultaneously.

Recursing at index+1 misses [2,2] for [2], target=4. Zero is outside the contract and breaks termination.

`candidates=[2,5], target=7 → [[2,5]]`

For m=2,T=5,c=2, depth is at most L=2. The loose bound of at most m children per call gives at most 1+m+m²=7 calls. Ordering and sum pruning reduce the actual count; copying the S output elements is counted separately.

### Implement and execute

```python
from collections import deque
import heapq

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

```text
python trace_lab.py --case combinations
```

Compare the trace return value with your prediction. Make the input change proposed above, find the first line where the state differs, and explain its effect on the answer.

## Lab report

Include the small-input state table, completed code, your own boundary input and expected result, and verification results. Explain time by total operation counts and space by simultaneously live state. Include any input copying or sorting costs.

---

## 실행 준비

[실습 코드 ZIP](https://sunboogermany.github.io/assets/courses/practical-algorithms/week-06-code.zip)을 풀고 코드 폴더에서 실행합니다. Python 3.11 이상과 표준 라이브러리를 사용합니다.

```text
python trace_lab.py --case can_finish
python verify.py
python verify.py --student
```

먼저 작은 입력의 답과 상태 변화를 종이에 적고 실행 결과와 비교하세요. `trace_lab.py`는 `solutions.py`의 실제 실행을 추적합니다. `before L…`은 그 행을 실행하기 직전의 값이므로, 앞서 실행한 행이 무엇을 바꿨는지 읽습니다. 연결 리스트는 chain, 트리 노드는 값과 두 자식 값으로 표시합니다. 추적 출력의 복사·표시 비용은 알고리즘의 시간·공간 분석에 포함하지 않습니다.

`student_week_06.py`의 함수와 메서드를 구현한 뒤 `verify.py --student`로 검사합니다. 미구현 상태의 `NotImplementedError`는 해당 함수부터 채우라는 뜻입니다. `--student` 없이 실행하면 제공 풀이를 검사합니다. 특정 풀이의 동작은 `python trace_lab.py --case 함수명 --student`로 대조할 수 있습니다.

각 문제에서 입력·출력의 의미, 상태의 불변식, 한 단계의 변화, 최종 답, 시간·보조 공간·반환값 공간을 기록하세요. 아래 작은 예제 하나의 통과만으로 전체 정당성이 증명되지는 않습니다.

## 이 주의 문제

- [can_finish](#ko-can_finish)
- [course_order](#ko-course_order)
- [subsets](#ko-subsets)
- [combinations](#ko-combinations)

## 풀이와 실행 과정

207 | 210 | 78 | 39

분석 파이프라인의 작업이 서로를 기다리면 실행이 멈춥니다. 실행 가능한 순서를 찾은 뒤에는 주어진 항목으로 만들 수 있는 선택을 빠짐없이 생성해야 합니다.

남은 선행 조건으로 실행 순서를 정하고, 선택·재귀·복원으로 분기 간 상태를 분리합니다.

## 의존관계의 방향과 인접 리스트

`[after,before]`는 before가 끝나야 after를 시작할 수 있다는 뜻입니다. before → after 방향으로 간선을 저장합니다. 진입차수 indegree는 아직 끝나지 않은 선행 작업의 수입니다.

![작업 0 뒤에 1과 2, 두 작업 뒤에 3을 수행하는 그래프](figures/dependency-dag.svg)

| 저장 항목 | 이 그림의 값 | 의미 |
| --- | --- | --- |
| graph | [[1,2],[3],[3],[]] | 각 작업 완료 시 영향을 받는 작업 |
| indegree | [0,1,1,2] | 남은 선행 작업 수 |
| 초기 queue | [0] | 지금 바로 할 수 있는 작업 |

graph는 간선 E개를 저장합니다. 정점마다 전체 V개를 넣는 행렬과 달리 인접 리스트의 전체 항목 수는 V+E에 비례합니다.

<a id="ko-can_finish"></a>

## [LeetCode 207: Course Schedule](https://leetcode.com/problems/course-schedule/) · Medium

선수 과목 조건을 모두 만족하며 전체 과목을 끝낼 수 있는지 반환합니다.

1 <= V <= 2000; 0 <= E <= 5000; 쌍 [after,before], 중복 쌍 없음.

### 구현 전 예측

선수과목→다음 과목 방향으로 간선과 진입차수를 만듭니다. 진입차수가 0인 정점만 queue에 넣습니다. 이 순환은 처음부터 준비된 과목이 없어 처리 개수가 0입니다. [0,2]를 빼면 세 과목을 모두 처리할 수 있습니다.

```python
can_finish(3, [[1, 0], [2, 1], [0, 2]])
# False
```

### 풀이 아이디어와 상태 변화

#### 207 · 풀이의 출발점과 실행 추적

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

### 구현과 실행

```python
from collections import deque
import heapq

def can_finish(n, prerequisites):
    return len(course_order(n, prerequisites)) == n
```

```text
python trace_lab.py --case can_finish
```

위 예측과 trace의 반환값을 대조하세요. 입력을 앞에서 제안한 대로 바꾸고, 처음으로 상태가 달라지는 행을 찾아 그 변화가 답에 미친 영향을 설명합니다.

<a id="ko-course_order"></a>

## [LeetCode 210: Course Schedule II](https://leetcode.com/problems/course-schedule-ii/) · Medium

선수 조건을 만족하는 순서 하나를 반환합니다. 불가능하면 빈 목록입니다.

1 <= V <= 2000; 0 <= E <= V(V-1); 서로 다른 정점의 중복 없는 [after,before].

### 구현 전 예측

준비된 과목을 순서에 넣고 다음 과목들의 진입차수를 줄입니다. 3은 1과 2를 모두 끝낸 뒤 준비됩니다. 각 간선의 앞뒤 위치를 검사하세요. [0,2,1,3]도 유효합니다.

```python
course_order(4, [[1, 0], [2, 0], [3, 1], [3, 2]])
# [0, 1, 2, 3]
```

### 풀이 아이디어와 상태 변화

#### 210 · 풀이의 출발점과 실행 추적

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

#### 210 · 정당성·시간·메모리의 근거

각 과목은 모든 선수가 제거된 뒤에만 큐에 들어갑니다. 따라서 반환 순서에서 모든 before의 위치가 after보다 앞섭니다. 수가 부족하면 전체 순서가 아닙니다.

정점 V개와 간선 E개를 저장하는 초기 작업이 O(V+E)입니다. 각 정점은 한 번 큐에 들어가고 각 간선은 출발 정점 처리 때 한 번만 읽습니다. 이웃 수가 정점마다 달라도 그 합은 E이므로 전체 시간은 O(V+E)입니다.

인접 리스트의 빈 목록 V개와 간선 항목 E개, indegree·queue·order의 최대 V개 항목이 필요합니다. 총 추가 공간은 O(V+E), 그중 반환 순서는 O(V)입니다. 207번의 반환값은 bool이지만 이 구현은 같은 순서 함수를 호출하므로 공간도 O(V+E)입니다.

[[1,0]]을 1→0으로 읽으면 역순을 만듭니다. 정답 하나와 목록을 직접 비교하지 말고 모든 간선을 검증합니다.

`n=4, prerequisites=[[2,0],[2,1],[3,2]] → [0,1,2,3]`

`[[] for _ in range(n)]`는 정점마다 새 이웃 목록을 만듭니다. `[[]]*n`은 같은 목록을 공유하므로 `graph[0].append(1)`이 모든 정점의 이웃에 1을 넣는 오류가 됩니다. 진입차수가 0이 되는 순간은 한 번뿐이라 정상 입력에서는 한 정점을 큐에 중복 삽입하지 않습니다.

### 구현과 실행

```python
from collections import deque
import heapq

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

```text
python trace_lab.py --case course_order
```

위 예측과 trace의 반환값을 대조하세요. 입력을 앞에서 제안한 대로 바꾸고, 처음으로 상태가 달라지는 행을 찾아 그 변화가 답에 미친 영향을 설명합니다.

<a id="ko-subsets"></a>

## [LeetCode 78: Subsets](https://leetcode.com/problems/subsets/) · Medium

서로 다른 값으로 이루어진 배열의 모든 부분집합을 반환합니다.

1 <= n <= 10; 값 -10..10; 모두 다름.

### 구현 전 예측

탐색 노드마다 path의 복사본을 저장합니다. 원소 선택, 뒤쪽 위치 재귀, pop 순서로 진행합니다. path 자체를 저장하면 하나의 변하는 list를 공유합니다. n=2의 출력은 빈 부분집합을 포함해 네 개입니다.

```python
subsets([1, 2],)
# [[], [1], [1, 2], [2]]
```

### 풀이 아이디어와 상태 변화

#### 78 · 풀이의 출발점과 실행 추적

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

#### 78 · 정당성·시간·메모리의 근거

부분집합마다 오름차순 인덱스 열이 하나 있습니다. start가 그 열만 허용하므로 모든 부분집합을 정확히 한 번 만듭니다. 복원 후 부모의 path는 호출 전과 같습니다.

원소마다 포함·제외 두 가능성이 있어 부분집합은 <math xmlns="http://www.w3.org/1998/Math/MathML"><msup><mn>2</mn><mi>n</mi></msup></math>개입니다. n>=1일 때 각 원소는 정확히 절반의 부분집합에 들어가므로 복사하는 원소 수의 합은 n·<math xmlns="http://www.w3.org/1998/Math/MathML"><msup><mn>2</mn><mrow><mi>n</mi><mo>−</mo><mn>1</mn></mrow></msup></math>입니다. 결과를 실제 리스트로 만드는 시간과 출력 공간은 O(n·<math xmlns="http://www.w3.org/1998/Math/MathML"><msup><mn>2</mn><mi>n</mi></msup></math>)입니다.

현재 path 길이와 재귀 깊이는 각각 최대 n이므로 출력을 제외한 보조 공간은 O(n)입니다. 시간은 전체 탐색량, 공간은 동시에 살아 있는 경로와 호출을 셉니다. 호출 총수를 전부 동시에 저장한다고 계산하지 않습니다.

result.append(path)는 같은 객체를 보관합니다. 마지막 pop 뒤 여러 결과가 빈 목록으로 바뀔 수 있습니다.

`nums=[2,5] → [[],[2],[2,5],[5]]`

### 구현과 실행

```python
from collections import deque
import heapq

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

```text
python trace_lab.py --case subsets
```

위 예측과 trace의 반환값을 대조하세요. 입력을 앞에서 제안한 대로 바꾸고, 처음으로 상태가 달라지는 행을 찾아 그 변화가 답에 미친 영향을 설명합니다.

<a id="ko-combinations"></a>

## [LeetCode 39: Combination Sum](https://leetcode.com/problems/combination-sum/) · Medium

후보를 반복 사용해 target 합을 만드는 중복 없는 조합을 반환합니다.

1..30개 서로 다른 후보, 각 2..40; target 1..40; 답 조합 150개 미만.

### 구현 전 예측

남은 target과 선택 가능한 첫 인덱스를 둡니다. 반복 사용을 위해 같은 인덱스로 재귀하되 더 작은 인덱스로 돌아가지 않습니다. 나머지가 0이면 저장합니다. [3,2,2]가 별도 답이 아닌 이유를 설명하세요.

```python
combinations([2, 3, 6, 7], 7)
# [[2, 2, 3], [7]]
```

### 풀이 아이디어와 상태 변화

#### 39 · 풀이의 출발점과 실행 추적

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

#### 재귀 복귀와 부모의 다음 선택

후보 [2,3], 목표 5에서 각 호출의 start와 remaining은 독립된 지역 변수이고 path만 공유합니다. 자식이 return해도 부모의 for는 그 다음 줄부터 계속됩니다.

| 실행 위치 | 공유 path | 해당 호출의 remaining |
| --- | --- | --- |
| 부모 visit(0,3), 2 추가 | [2,2] | 3 |
| 자식 visit(0,1), 2>1로 종료 | [2,2] | 1 |
| 부모로 복귀, path.pop() | [2] | 여전히 3 |
| 부모의 다음 index=1, 3 추가 | [2,3] | 3 |
| 자식 visit(1,0), 복사 저장 후 return | [2,3] | 0 |
| 부모로 복귀, path.pop() | [2] | 3 |

첫 행의 부모는 이미 첫 2를 고른 호출입니다. pop은 공유 경로의 마지막 선택을 취소합니다. remaining은 부모 값이 바뀐 적이 없어 별도로 더해 복원하지 않습니다. 반대로 전역 remaining을 직접 줄이는 구현이라면 그 값도 복원해야 합니다.

#### 39 · 정당성·시간·메모리의 근거

양수 선택마다 remaining이 감소해 종료합니다. 비내림차순 인덱스만 선택하므로 순서만 다른 중복을 피하고 모든 가능한 조합을 표현합니다.

후보 수 m, 목표 T, 최소 후보 c라 하면 경로 길이는 L=floor(T/c) 이하입니다. 방문 호출 수 B, 출력 원소 수의 합 S를 쓰면 정렬 O(m log m), 호출당 최대 m개 검사, 복사 O(S)이므로 O(m log m+mB+S) 시간입니다. B는 입력에 따라 크게 달라져 이를 단순 O(n)이라 할 수 없습니다.

보수적으로 B=O(<math xmlns="http://www.w3.org/1998/Math/MathML"><msup><mrow><mo>(</mo><mi>m</mi><mo>+</mo><mn>1</mn><mo>)</mo></mrow><mrow><mi>L</mi><mo>+</mo><mn>1</mn></mrow></msup></math>)입니다. 정렬한 후보 m개와 길이 L의 path·호출 스택이 있어 보조 공간 O(m+L), 출력은 O(S)입니다. 전체 탐색 트리를 한 번에 저장하지는 않습니다.

index+1로 재귀하면 [2], target=4의 [2,2]를 놓칩니다. 후보 0은 공식 범위 밖이며 종료 논리를 깨뜨립니다.

`candidates=[2,5], target=7 → [[2,5]]`

예를 들어 m=2,T=5,c=2이면 깊이는 L=2 이하입니다. 모든 호출이 최대 m개 자식을 가진다는 느슨한 계산으로 호출 수는 1+m+m²=7 이하입니다. 실제로는 순서 제한과 합 초과 가지치기로 더 적으며, 저장된 답을 복사하는 S의 비용은 별도로 더합니다.

### 구현과 실행

```python
from collections import deque
import heapq

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

```text
python trace_lab.py --case combinations
```

위 예측과 trace의 반환값을 대조하세요. 입력을 앞에서 제안한 대로 바꾸고, 처음으로 상태가 달라지는 행을 찾아 그 변화가 답에 미친 영향을 설명합니다.

## 실습 보고서

작은 입력의 상태표, 완성 코드, 직접 만든 경계 입력과 예상값, 검증 결과를 함께 기록합니다. 시간 복잡도는 총 연산 횟수로, 공간 복잡도는 동시에 살아 있는 상태로 설명하세요. 입력을 복사하거나 정렬한다면 그 비용도 포함합니다.
