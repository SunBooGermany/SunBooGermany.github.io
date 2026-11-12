---
layout: "course-resource"
title: "Week 5 Student Exercises"
title_ko: "5주차 학생 실습"
permalink: "/courses/practical-algorithms/week-05-practice/"
course_id: "practical-algorithms"
---

## Set up and run

Extract the [lab code ZIP](/assets/courses/practical-algorithms/week-05-code.zip) and work in its code folder. Use Python 3.11+ and the standard library.

```text
python trace_lab.py --case kth_largest
python verify.py
python verify.py --student
```

Predict the small example and its states on paper first. `trace_lab.py` traces the actual `solutions.py` implementation. `before L…` shows values immediately before that line executes: identify what the preceding executed line changed. Linked lists display a chain; tree nodes display their value and child values. Exclude tracing, copying, and printing overhead from the algorithm's complexity.

Implement the functions and methods in `student_week_05.py`, then run `verify.py --student`. An initial `NotImplementedError` identifies work still to implement. Without `--student`, the verifier checks the supplied solutions. Use `python trace_lab.py --case FUNCTION --student` to inspect your implementation.

For each task record the input/output meaning, state invariant, one state transition, final answer, time, auxiliary space, and output space. Passing one small example does not establish correctness for all inputs.

## This week’s problems

- [kth_largest](#en-kth_largest)
- [merge_intervals](#en-merge_intervals)
- [islands](#en-islands)
- [rot_minutes](#en-rot_minutes)

## Worked solutions

215 | 56 | 200 | 994

Maintain the top k measurements as values arrive, and merge overlapping maintenance intervals. On a sensor map, identify separate failure regions and the time needed for failures to spread.

Full ordering, partial ranking, and connectivity need different state. Track a heap boundary, the end of a sorted interval, and traversal visits.

## What counts as one step on a grid?

Treat cells as vertices and four-directional adjacencies as edges. Islands ask for connected components; propagation asks for distance from the nearest source.

![Island connectivity and first arrival times during simultaneous spread](/assets/courses/practical-algorithms/curriculum/grid-traversal.svg)

Diagonal land cells on the left belong to separate islands. Numbers on the right are first infection times for `[[2,1,1],[0,1,1]]`; `-` marks an empty cell.

| Goal | Processing order | Retained information |
| --- | --- | --- |
| Find all connected land | Stack: depth first | Visited coordinates and pending neighbors |
| Spread simultaneously by minute | Queue: breadth first | Current sources and remaining fresh cells |

Mark cells when discovered so different neighbors cannot enqueue or push the same cell repeatedly.

<a id="en-kth_largest"></a>

## [LeetCode 215: Kth Largest Element in an Array](https://leetcode.com/problems/kth-largest-element-in-an-array/) · Medium

Return the kth value in descending order, counting duplicates.

1 <= k <= n <= <math xmlns="http://www.w3.org/1998/Math/MathML"><msup><mn>10</mn><mn>5</mn></msup></math>; values -<math xmlns="http://www.w3.org/1998/Math/MathML"><msup><mn>10</mn><mn>4</mn></msup></math>..<math xmlns="http://www.w3.org/1998/Math/MathML"><msup><mn>10</mn><mn>4</mn></msup></math>.

### Predict before implementing

Keep a min-heap of the largest k values seen so far. Replace its root only with a larger value. The root is the smallest retained value, hence the kth largest overall. Try k=1 and duplicates.

```python
kth_largest([3, 2, 1, 5, 6, 4], 2)
# 5
```

### Idea and state transitions

#### 215 · Idea and execution trace

[LeetCode 215: Kth Largest Element in an Array](https://leetcode.com/problems/kth-largest-element-in-an-array/) · Medium

Return the kth value in descending order, counting duplicates.

Sorting everything finds the kth value, but only the largest k values need to be retained. In a min-heap containing those values, the root is their minimum and hence the current kth largest. Replace it only when a larger value arrives.

`nums=[3,1,5,2,4], k=2`. The table shows the actual heap list, not a fully sorted sequence.

| Operation | heap | Current kth value |
| --- | --- | --- |
| Heapify first two | [1,3] | 1 |
| 5 > 1: replace | [3,5] | 3 |
| 2 <= 3: retain | [3,5] | 3 |
| 4 > 3: replace | [4,5] | 4 |

#### Heap positions and root replacement

In min-heap `[2,4,3,8,6,5,7]`, the children of position i are 2i+1 and 2i+2. Root 2 has children 4 and 3. Siblings need not be sorted; each parent must be no larger than its children.

Replace the root with 9 and trace a repair path that promotes the smaller child.

| Step | Array | Next comparison |
| --- | --- | --- |
| Replace root | [9,4,3,8,6,5,7] | choose 3 over 4 |
| Promote 3 | [3,4,9,8,6,5,7] | choose 5 over 7 |
| Promote 5 | [3,4,5,8,6,9,7] | 9 is a leaf; stop |

Reading root 3 takes O(1); repair follows a path of at most the tree height. heapify repairs parents from the bottom. With seven nodes, four leaves have height 0, two parents have height 1, and the root has height 2. This allows 2×1+1×2=4 downward levels in total. In general, the number of tall subtrees decreases geometrically, giving O(k) total work.

[Python heapq representation and operations](https://docs.python.org/3/library/heapq.html)

#### 215 · Why it works; time and memory

The heap retains the largest k values seen. A new value at most its minimum cannot improve that set; a larger one replaces the minimum. The final root is kth largest.

Copying and heapify cost O(k). Each of the remaining n-k values requires one root comparison and, only on replacement, a path of height O(log k). Time is O(k+(n-k)(1+log k)), commonly O(n log k) for k>=2. For k=1 it is O(n), like tracking a maximum.

The heap always has k entries, so auxiliary space is O(k); the result is one value. Heapify is linear because most nodes are near the bottom and have only short downward paths.

In a min-heap, each parent is no greater than its children, and the root holds a global minimum. Deduplicating changes the example’s answer.

`nums=[8,3,8,2,5], k=2 → 8`

### Implement and execute

```python
from collections import deque
import heapq

def kth_largest(nums, k):
    heap = nums[:k]
    heapq.heapify(heap)
    for index in range(k, len(nums)):
        value = nums[index]
        if value > heap[0]:
            heapq.heapreplace(heap, value)
    return heap[0]
```

```text
python trace_lab.py --case kth_largest
```

Compare the trace return value with your prediction. Make the input change proposed above, find the first line where the state differs, and explain its effect on the answer.

<a id="en-merge_intervals"></a>

## [LeetCode 56: Merge Intervals](https://leetcode.com/problems/merge-intervals/) · Medium

Return disjoint closed intervals covering the input union.

1 <= n <= <math xmlns="http://www.w3.org/1998/Math/MathML"><msup><mn>10</mn><mn>4</mn></msup></math>; 0 <= start <= end <= <math xmlns="http://www.w3.org/1998/Math/MathML"><msup><mn>10</mn><mn>4</mn></msup></math>; touching endpoints merge.

### Predict before implementing

Sort by start. Compare each interval with the last merged end; extend with max(end, next_end) on overlap. Test [1,6] with [2,3] so the end never shrinks.

```python
merge_intervals([[1, 3], [2, 6], [8, 10]],)
# [[1, 6], [8, 10]]
```

### Idea and state transitions

#### 56 · Idea and execution trace

[LeetCode 56: Merge Intervals](https://leetcode.com/problems/merge-intervals/) · Medium

Return disjoint closed intervals covering the input union.

After sorting by start, the next interval begins no earlier than processed intervals. It can therefore overlap only the last merged interval. Extend that interval’s end on overlap, or begin a new result interval when there is a gap.

Input: `[[1,4],[2,3],[4,6],[8,9]]`. Each row shows result after processing that interval.

| Interval | Test | result |
| --- | --- | --- |
| [1,4] | First interval | [[1,4]] |
| [2,3] | 2 <= 4 | [[1,4]] |
| [4,6] | 4 <= 4 | [[1,6]] |
| [8,9] | 8 > 6 | [[1,6],[8,9]] |

#### 56 · Why it works; time and memory

result equals the union of the processed prefix. Increasing starts mean a new interval can overlap only the last result; a gap makes a new disjoint component.

Sorting n intervals costs O(n log n). The subsequent scan runs n times and compares only one last result interval each time, so it costs O(n). Sorting dominates the total O(n log n).

`sorted` creates a list of n references and uses sorting workspace, giving O(n) auxiliary space. If z merged intervals remain, output space is O(z), with z<=n. Each output interval stores its own two endpoints.

Overwriting the end with 3 for [[1,8],[2,3]] loses coverage. Half-open time intervals may use a different touching rule.

`intervals=[[5,7],[1,3],[3,6]] → [[1,7]]`

### Implement and execute

```python
from collections import deque
import heapq

def merge_intervals(intervals):
    result = []
    for start, end in sorted(intervals, key=lambda item: item[0]):
        if result and start <= result[-1][1]:
            result[-1][1] = max(result[-1][1], end)
        else:
            result.append([start, end])
    return result
```

```text
python trace_lab.py --case merge_intervals
```

Compare the trace return value with your prediction. Make the input change proposed above, find the first line where the state differs, and explain its effect on the answer.

<a id="en-islands"></a>

## [LeetCode 200: Number of Islands](https://leetcode.com/problems/number-of-islands/) · Medium

Count land components connected horizontally or vertically in a character grid.

1 <= R,C <= 300; cells are strings "0" or "1".

### Predict before implementing

Scan cells. On unseen land, increment the component count and flood-fill its four-neighbor region. Mark when scheduling a cell to avoid duplicate work. Diagonally touching land remains separate.

```python
islands([list('110'), list('010'), list('001')],)
# 2
```

### Idea and state transitions

#### 200 · Idea and execution trace

[LeetCode 200: Number of Islands](https://leetcode.com/problems/number-of-islands/) · Medium

Count land components connected horizontally or vertically in a character grid.

Starting from one land cell and following all four-directional connections reaches its whole island. Start a traversal and increase the count only at unvisited land, preventing duplicate counting. Diagonals do not connect cells.

Grid: `[["1","1","0"],["0","1","0"],["1","0","1"]]`. Coordinates start at zero; stack top is on the right.

| Action | stack | Newly added to seen | count |
| --- | --- | --- | --- |
| Start (0,0) | [(0,0)] | (0,0) | 1 |
| Pop (0,0) | [(0,1)] | (0,1) | 1 |
| Pop (0,1) | [(1,1)] | (1,1) | 1 |
| Pop (1,1) | [] | None | 1 |
| Traverse (2,0), (2,2) separately | [] | (2,0), (2,2) | 3 |

#### 200 · Why it works; time and memory

A traversal reaches exactly its starting component. Marked components cannot restart; the number of starts equals the component count.

The outer scan reads R·C cells. Each land cell is pushed and popped once because of seen, and each pop checks four neighbors. Four is independent of input size, giving expected O(RC) time under expected hash-set costs. The inner traversal is not restarted fully for every cell.

Both seen and the pending stack can hold up to RC coordinates, so auxiliary space is O(RC). Marking the grid itself could replace seen, but would mutate the input and would not eliminate stack storage.

Use == for values; is tests identity. Diagonal land in a 2x2 grid forms two components.

`grid=[["1","0","1"],["1","0","0"]] → 2`

### Implement and execute

```python
from collections import deque
import heapq

def islands(grid):
    rows, cols = len(grid), len(grid[0])
    seen, count = set(), 0
    for row in range(rows):
        for col in range(cols):
            if grid[row][col] != "1" or (row, col) in seen:
                continue
            count += 1
            stack = [(row, col)]
            seen.add((row, col))
            while stack:
                r, c = stack.pop()
                for nr, nc in ((r-1,c),(r+1,c),(r,c-1),(r,c+1)):
                    if (0 <= nr < rows and 0 <= nc < cols
                            and grid[nr][nc] == "1" and (nr,nc) not in seen):
                        seen.add((nr,nc))
                        stack.append((nr,nc))
    return count
```

```text
python trace_lab.py --case islands
```

Compare the trace return value with your prediction. Make the input change proposed above, find the first line where the state differs, and explain its effect on the answer.

<a id="en-rot_minutes"></a>

## [LeetCode 994: Rotting Oranges](https://leetcode.com/problems/rotting-oranges/) · Medium

Return the minimum minutes for all fresh cells to change under simultaneous spread, or -1.

1 <= R,C <= 10; 0 empty,1 fresh,2 rotten; one orthogonal edge per minute.

### Predict before implementing

Put all initially rotten cells in one queue. Process a whole level per minute and decrease fresh on each newly rotten cell. The fresh counts are 6→4→2→1→0. Try an isolated fresh cell: return -1.

```python
rot_minutes([[2, 1, 1], [1, 1, 0], [0, 1, 1]],)
# 4
```

### Idea and state transitions

#### 994 · Idea and execution trace

[LeetCode 994: Rotting Oranges](https://leetcode.com/problems/rotting-oranges/) · Medium

Return the minimum minutes for all fresh cells to change under simultaneous spread, or -1.

All initially rotten cells are sources at time zero. Put them all in one queue and expand by levels. The first infection time of a cell is its distance from the nearest source. Processing sources sequentially would misrepresent simultaneous spread.

Input: `[[2,1,1],[0,1,1]]`. Each queue contains cells newly rotten at that time, awaiting processing.

| Time minutes | queue | fresh |
| --- | --- | --- |
| 0 | [(0,0)] | 4 |
| 1 | [(0,1)] | 3 |
| 2 | [(1,1),(0,2)] | 1 |
| 3 | [(1,2)] | 0 |

Once fresh is zero, return 3 without processing the final queue.

#### 994 · Why it works; time and memory

BFS levels are minimum edge distances from any source. Equal edge durations make first discovery earliest; remaining fresh cells after exhaustion are unreachable.

Copying and the initial scan each cost O(RC). Every cell enters the queue once and checks four neighbors when removed, so propagation also costs O(RC). Adding these stages gives O(RC); do not multiply by the number of minutes again.

The board copy stores RC cells to preserve the input. The queue may also hold O(RC) cells, giving O(RC) auxiliary space. Constant-size fresh and minutes counters do not make the whole algorithm constant-space.

[[2,0,1]] gives -1; [[0,2]] gives 0. Processing newly queued levels in the same minute undercounts time.

`grid=[[2,1,1],[0,1,0]] → 2`

`board=[row[:] for row in grid]` copies each row as well, preserving the original cell values. `fresh += board[r][c] == 1` adds 1 for True and 0 for False. Scanning [2,1,1] therefore makes fresh go 0→1→2.

An empty queue with fresh cells remaining means unreachable cells and returns -1. If fresh is initially zero, no time step is needed and the result is 0.

### Implement and execute

```python
from collections import deque
import heapq

def rot_minutes(grid):
    rows, cols = len(grid), len(grid[0])
    board = [row[:] for row in grid]
    queue, fresh, minutes = deque(), 0, 0
    for r in range(rows):
        for c in range(cols):
            if board[r][c] == 2:
                queue.append((r,c))
            fresh += board[r][c] == 1
    while queue and fresh:
        for _ in range(len(queue)):
            r, c = queue.popleft()
            for nr, nc in ((r-1,c),(r+1,c),(r,c-1),(r,c+1)):
                if 0 <= nr < rows and 0 <= nc < cols and board[nr][nc] == 1:
                    board[nr][nc] = 2
                    fresh -= 1
                    queue.append((nr,nc))
        minutes += 1
    return minutes if fresh == 0 else -1
```

```text
python trace_lab.py --case rot_minutes
```

Compare the trace return value with your prediction. Make the input change proposed above, find the first line where the state differs, and explain its effect on the answer.

## Lab report

Include the small-input state table, completed code, your own boundary input and expected result, and verification results. Explain time by total operation counts and space by simultaneously live state. Include any input copying or sorting costs.

<!-- ko -->

## 실행 준비

[실습 코드 ZIP](/assets/courses/practical-algorithms/week-05-code.zip)을 풀고 코드 폴더에서 실행합니다. Python 3.11 이상과 표준 라이브러리를 사용합니다.

```text
python trace_lab.py --case kth_largest
python verify.py
python verify.py --student
```

먼저 작은 입력의 답과 상태 변화를 종이에 적고 실행 결과와 비교하세요. `trace_lab.py`는 `solutions.py`의 실제 실행을 추적합니다. `before L…`은 그 행을 실행하기 직전의 값이므로, 앞서 실행한 행이 무엇을 바꿨는지 읽습니다. 연결 리스트는 chain, 트리 노드는 값과 두 자식 값으로 표시합니다. 추적 출력의 복사·표시 비용은 알고리즘의 시간·공간 분석에 포함하지 않습니다.

`student_week_05.py`의 함수와 메서드를 구현한 뒤 `verify.py --student`로 검사합니다. 미구현 상태의 `NotImplementedError`는 해당 함수부터 채우라는 뜻입니다. `--student` 없이 실행하면 제공 풀이를 검사합니다. 특정 풀이의 동작은 `python trace_lab.py --case 함수명 --student`로 대조할 수 있습니다.

각 문제에서 입력·출력의 의미, 상태의 불변식, 한 단계의 변화, 최종 답, 시간·보조 공간·반환값 공간을 기록하세요. 아래 작은 예제 하나의 통과만으로 전체 정당성이 증명되지는 않습니다.

## 이 주의 문제

- [kth_largest](#ko-kth_largest)
- [merge_intervals](#ko-merge_intervals)
- [islands](#ko-islands)
- [rot_minutes](#ko-rot_minutes)

## 풀이와 실행 과정

215 | 56 | 200 | 994

측정값이 계속 들어오는 동안 상위 k개를 유지하고, 겹치는 정비 시간을 합쳐야 합니다. 센서 지도에서는 떨어진 장애 영역과 장애가 퍼지는 시간을 구합니다.

전체 정렬·부분 순위·연결 관계는 서로 다른 상태가 필요합니다. 힙의 경계, 정렬된 구간의 끝, 탐색의 방문 기록을 추적합니다.

## 격자에서 무엇을 한 단계로 셀 것인가

격자 한 칸을 정점으로 보고 상하좌우 이웃 사이에 간선이 있다고 생각합니다. 섬 문제는 연결된 덩어리의 수를, 전파 문제는 가장 가까운 출발점에서의 거리를 묻습니다.

![섬의 연결과 동시 전파의 도착 시각](/assets/courses/practical-algorithms/curriculum/grid-traversal.svg)

왼쪽에서 대각선으로 닿은 육지는 별도 섬입니다. 오른쪽 숫자는 `[[2,1,1],[0,1,1]]`에서 처음 썩는 시각이며 `-`는 빈칸입니다.

| 목표 | 다음 처리 순서 | 보관할 정보 |
| --- | --- | --- |
| 연결된 육지 전부 찾기 | 스택으로 깊이 우선 | 방문한 좌표·미처리 이웃 |
| 한 분마다 동시에 확산 | 큐로 너비 우선 | 현재 시각의 전파원·남은 fresh |

둘 다 방문 표시를 넣는 시점이 중요합니다. 발견할 때 표시하면 여러 이웃이 같은 칸을 중복 삽입하지 않습니다.

<a id="ko-kth_largest"></a>

## [LeetCode 215: Kth Largest Element in an Array](https://leetcode.com/problems/kth-largest-element-in-an-array/) · Medium

정렬했을 때 큰 순서로 k번째 값을 반환합니다. 중복도 개수에 포함합니다.

1 <= k <= n <= <math xmlns="http://www.w3.org/1998/Math/MathML"><msup><mn>10</mn><mn>5</mn></msup></math>; 값 -<math xmlns="http://www.w3.org/1998/Math/MathML"><msup><mn>10</mn><mn>4</mn></msup></math>..<math xmlns="http://www.w3.org/1998/Math/MathML"><msup><mn>10</mn><mn>4</mn></msup></math>.

### 구현 전 예측

지금까지 본 큰 값 k개를 min-heap에 보관합니다. 루트보다 큰 값만 루트를 대체합니다. 루트는 보관한 값 중 가장 작으므로 전체에서 k번째 큰 값입니다. k=1과 중복 값도 확인하세요.

```python
kth_largest([3, 2, 1, 5, 6, 4], 2)
# 5
```

### 풀이 아이디어와 상태 변화

#### 215 · 풀이의 출발점과 실행 추적

[LeetCode 215: Kth Largest Element in an Array](https://leetcode.com/problems/kth-largest-element-in-an-array/) · Medium

정렬했을 때 큰 순서로 k번째 값을 반환합니다. 중복도 개수에 포함합니다.

전체를 정렬하면 k번째 값을 찾을 수 있지만, 필요한 것은 큰 값 k개뿐입니다. 지금까지 본 큰 값 k개를 최소 힙에 보관하면 그중 가장 작은 루트가 현재 k번째 값입니다. 새 값이 루트보다 클 때만 교체합니다.

`nums=[3,1,5,2,4], k=2`. 표는 실제 heap 리스트이며 전체 정렬 결과는 아닙니다.

| 처리 | heap | 현재 k번째 값 |
| --- | --- | --- |
| 첫 두 값 heapify | [1,3] | 1 |
| 5 > 1, 교체 | [3,5] | 3 |
| 2 <= 3, 유지 | [3,5] | 3 |
| 4 > 3, 교체 | [4,5] | 4 |

#### 힙의 배열 위치와 루트 교체

최소 힙 `[2,4,3,8,6,5,7]`의 부모 i와 자식은 2i+1,2i+2에 있습니다. 루트 2의 자식은 4와 3입니다. 형제끼리는 정렬되어 있지 않아도 부모≤자식 조건을 만족합니다.

루트에 새 값 9를 넣었을 때 작은 자식을 위로 올리며 조건을 복구하는 경로를 추적합니다.

| 단계 | 배열 | 다음 비교 |
| --- | --- | --- |
| 루트 교체 | [9,4,3,8,6,5,7] | 4와 3 중 작은 3 |
| 3을 위로 | [3,4,9,8,6,5,7] | 5와 7 중 작은 5 |
| 5를 위로 | [3,4,5,8,6,9,7] | 9는 잎, 종료 |

새 루트 3은 O(1)로 읽지만 복구는 높이만큼 작업합니다. heapify는 아래 부모부터 복구합니다. 노드가 7개인 트리에서는 잎 4개의 이동 높이는 0, 부모 2개는 최대 1, 루트는 최대 2입니다. 전체는 2×1+1×2=4단계 정도의 하향 이동이며, 일반적으로 높이가 큰 노드 수가 기하급수적으로 줄어 전체 O(k)입니다.

[Python heapq의 배열 규칙과 연산](https://docs.python.org/3/library/heapq.html)

#### 215 · 정당성·시간·메모리의 근거

힙은 지금까지 본 값 중 큰 k개입니다. root 이하의 새 값은 상위 k개를 바꾸지 못하고, 큰 새 값은 가장 작은 보관 값을 대체해야 합니다. 마지막 root가 k번째입니다.

복사와 heapify는 O(k)입니다. 나머지 n-k개는 루트를 한 번 비교하고, 교체할 때만 높이 O(log k)의 경로를 따라갑니다. 따라서 O(k+(n-k)(1+log k)), k>=2이면 보통 O(n log k)로 씁니다. k=1은 최댓값을 추적하는 O(n)입니다.

힙 크기는 항상 k라서 보조 공간은 O(k), 반환 값은 한 개입니다. heapify의 O(k)는 원소마다 O(log k)를 단순 곱한 비용보다 작습니다. 아래쪽에 있는 많은 노드는 내려갈 높이가 짧기 때문입니다.

최소 힙에서는 각 부모의 값이 자식 이하이고, root에 전체 최솟값이 놓입니다. 중복을 set으로 없애면 예시의 답이 달라집니다.

`nums=[8,3,8,2,5], k=2 → 8`

### 구현과 실행

```python
from collections import deque
import heapq

def kth_largest(nums, k):
    heap = nums[:k]
    heapq.heapify(heap)
    for index in range(k, len(nums)):
        value = nums[index]
        if value > heap[0]:
            heapq.heapreplace(heap, value)
    return heap[0]
```

```text
python trace_lab.py --case kth_largest
```

위 예측과 trace의 반환값을 대조하세요. 입력을 앞에서 제안한 대로 바꾸고, 처음으로 상태가 달라지는 행을 찾아 그 변화가 답에 미친 영향을 설명합니다.

<a id="ko-merge_intervals"></a>

## [LeetCode 56: Merge Intervals](https://leetcode.com/problems/merge-intervals/) · Medium

닫힌 구간들의 합집합을 겹치지 않는 구간으로 반환합니다.

1 <= n <= <math xmlns="http://www.w3.org/1998/Math/MathML"><msup><mn>10</mn><mn>4</mn></msup></math>; 0 <= start <= end <= <math xmlns="http://www.w3.org/1998/Math/MathML"><msup><mn>10</mn><mn>4</mn></msup></math>; 끝점이 닿아도 병합.

### 구현 전 예측

시작점으로 정렬합니다. 다음 구간을 마지막 병합 구간의 끝과 비교하고 겹치면 max(끝, 다음 끝)으로 늘립니다. [1,6]과 [2,3]으로 끝이 줄어들지 않는지 검사하세요.

```python
merge_intervals([[1, 3], [2, 6], [8, 10]],)
# [[1, 6], [8, 10]]
```

### 풀이 아이디어와 상태 변화

#### 56 · 풀이의 출발점과 실행 추적

[LeetCode 56: Merge Intervals](https://leetcode.com/problems/merge-intervals/) · Medium

닫힌 구간들의 합집합을 겹치지 않는 구간으로 반환합니다.

구간을 시작점순으로 정렬하면 다음 구간은 지금까지 처리한 구간보다 뒤에서 시작합니다. 따라서 결과의 마지막 구간과 겹치는지만 보면 됩니다. 겹치면 끝점을 더 멀리 늘리고, 떨어져 있으면 새 구간을 시작합니다.

입력 `[[1,4],[2,3],[4,6],[8,9]]`. 각 행은 현재 구간 처리 후의 result입니다.

| 구간 | 검사 | result |
| --- | --- | --- |
| [1,4] | 첫 구간 | [[1,4]] |
| [2,3] | 2 <= 4 | [[1,4]] |
| [4,6] | 4 <= 4 | [[1,6]] |
| [8,9] | 8 > 6 | [[1,6],[8,9]] |

#### 56 · 정당성·시간·메모리의 근거

처리한 접두부의 합집합은 result와 같습니다. 시작점이 증가하므로 새 구간은 마지막 결과와만 겹칠 수 있습니다. 분리되면 이후에도 앞 결과와 겹치지 않습니다.

n개 구간 정렬이 O(n log n), 정렬 뒤 스캔은 n번입니다. 각 스캔에서 마지막 구간 한 개만 비교하므로 O(n), 전체는 O(n log n)입니다. 앞의 모든 결과 구간을 매번 훑는 방식과 차이가 납니다.

`sorted`가 입력 참조 n개의 새 리스트를 만들고 정렬 작업 공간도 사용하므로 보조 공간은 O(n)입니다. 병합 결과가 z개라면 출력 공간은 O(z), z<=n입니다. 구간을 입력 그대로 공유하지 않는 비용도 결과의 두 끝점에 포함됩니다.

[[1,8],[2,3]]에서 end=3으로 덮으면 [3,8]을 잃습니다. 반열린 시간 구간은 닿음 규칙이 다를 수 있습니다.

`intervals=[[5,7],[1,3],[3,6]] → [[1,7]]`

### 구현과 실행

```python
from collections import deque
import heapq

def merge_intervals(intervals):
    result = []
    for start, end in sorted(intervals, key=lambda item: item[0]):
        if result and start <= result[-1][1]:
            result[-1][1] = max(result[-1][1], end)
        else:
            result.append([start, end])
    return result
```

```text
python trace_lab.py --case merge_intervals
```

위 예측과 trace의 반환값을 대조하세요. 입력을 앞에서 제안한 대로 바꾸고, 처음으로 상태가 달라지는 행을 찾아 그 변화가 답에 미친 영향을 설명합니다.

<a id="ko-islands"></a>

## [LeetCode 200: Number of Islands](https://leetcode.com/problems/number-of-islands/) · Medium

문자 격자의 상하좌우로 연결된 육지 덩어리 수를 반환합니다.

1 <= R,C <= 300; 셀은 문자열 "0" 또는 "1".

### 구현 전 예측

칸을 훑다가 방문하지 않은 땅이면 개수를 늘리고 상하좌우 연결 영역을 방문합니다. 탐색 대상으로 넣을 때 표시하면 중복 처리를 막습니다. 대각선으로 닿은 땅은 별개입니다.

```python
islands([list('110'), list('010'), list('001')],)
# 2
```

### 풀이 아이디어와 상태 변화

#### 200 · 풀이의 출발점과 실행 추적

[LeetCode 200: Number of Islands](https://leetcode.com/problems/number-of-islands/) · Medium

문자 격자의 상하좌우로 연결된 육지 덩어리 수를 반환합니다.

육지 한 칸에서 상하좌우 연결을 모두 따라가면 그 섬 전체를 찾습니다. 아직 방문하지 않은 육지를 만날 때만 섬 수를 늘리고 탐색을 시작하면 같은 섬을 여러 번 세지 않습니다. 대각선은 연결에 포함되지 않습니다.

격자 `[["1","1","0"],["0","1","0"],["1","0","1"]]`. 스택 오른쪽이 top이며 좌표는 0부터 셉니다.

| 동작 | stack | seen에 새로 추가 | count |
| --- | --- | --- | --- |
| (0,0) 시작 | [(0,0)] | (0,0) | 1 |
| (0,0) pop | [(0,1)] | (0,1) | 1 |
| (0,1) pop | [(1,1)] | (1,1) | 1 |
| (1,1) pop | [] | 없음 | 1 |
| (2,0), (2,2) 각각 탐색 | [] | (2,0), (2,2) | 3 |

#### 200 · 정당성·시간·메모리의 근거

한 번 시작한 탐색은 연결 경로를 따라 그 성분의 모든 노드와 그 노드만 방문합니다. 이미 표시한 성분은 다시 시작하지 않으므로 시작 횟수가 성분 수입니다.

R·C칸을 한 번 훑습니다. 육지 칸은 seen 때문에 한 번만 push·pop되고, 꺼낼 때 이웃 네 개만 검사합니다. 네 방향은 입력 크기와 무관한 상수라서 해시 연산의 기대 비용을 적용한 시간은 O(RC)입니다. 루프가 중첩되어 보여도 섬 탐색 전체가 매 칸에서 반복되는 것은 아닙니다.

seen에는 최대 RC개 좌표, stack에도 최대 RC개 좌표가 남을 수 있어 보조 공간은 O(RC)입니다. 격자를 직접 표시하면 seen을 없앨 수 있지만, 입력 변경과 탐색 스택의 비용은 여전히 따져야 합니다.

값 비교는 ==입니다. is는 객체 동일성입니다. [["1","0"],["0","1"]]은 대각선을 연결하지 않아 두 성분입니다.

`grid=[["1","0","1"],["1","0","0"]] → 2`

### 구현과 실행

```python
from collections import deque
import heapq

def islands(grid):
    rows, cols = len(grid), len(grid[0])
    seen, count = set(), 0
    for row in range(rows):
        for col in range(cols):
            if grid[row][col] != "1" or (row, col) in seen:
                continue
            count += 1
            stack = [(row, col)]
            seen.add((row, col))
            while stack:
                r, c = stack.pop()
                for nr, nc in ((r-1,c),(r+1,c),(r,c-1),(r,c+1)):
                    if (0 <= nr < rows and 0 <= nc < cols
                            and grid[nr][nc] == "1" and (nr,nc) not in seen):
                        seen.add((nr,nc))
                        stack.append((nr,nc))
    return count
```

```text
python trace_lab.py --case islands
```

위 예측과 trace의 반환값을 대조하세요. 입력을 앞에서 제안한 대로 바꾸고, 처음으로 상태가 달라지는 행을 찾아 그 변화가 답에 미친 영향을 설명합니다.

<a id="ko-rot_minutes"></a>

## [LeetCode 994: Rotting Oranges](https://leetcode.com/problems/rotting-oranges/) · Medium

동시에 퍼지는 변화를 적용해 모든 신선한 셀이 바뀌는 최소 분을 반환합니다. 불가능하면 -1입니다.

1 <= R,C <= 10; 0=빈 칸,1=신선,2=부패; 상하좌우로 분당 한 칸.

### 구현 전 예측

처음 썩은 칸을 모두 한 queue에 넣습니다. 한 깊이를 1분으로 처리하고 새로 썩을 때 fresh를 줄입니다. 남은 개수는 6→4→2→1→0입니다. 고립된 신선한 칸이 있으면 -1인지 확인하세요.

```python
rot_minutes([[2, 1, 1], [1, 1, 0], [0, 1, 1]],)
# 4
```

### 풀이 아이디어와 상태 변화

#### 994 · 풀이의 출발점과 실행 추적

[LeetCode 994: Rotting Oranges](https://leetcode.com/problems/rotting-oranges/) · Medium

동시에 퍼지는 변화를 적용해 모든 신선한 셀이 바뀌는 최소 분을 반환합니다. 불가능하면 -1입니다.

모든 썩은 칸은 같은 시각 0에서 출발하는 전파원입니다. 이들을 모두 큐에 넣고 한 층씩 확산하면 각 칸이 처음 썩는 시각이 가장 가까운 전파원까지의 거리입니다. 한 원점씩 따로 전파하면 동시에 일어나는 일을 잘못 셀 수 있습니다.

입력 `[[2,1,1],[0,1,1]]`. 아래 queue는 해당 시각에 새로 썩어 다음에 처리될 칸입니다.

| 시각 minutes | queue | fresh |
| --- | --- | --- |
| 0 | [(0,0)] | 4 |
| 1 | [(0,1)] | 3 |
| 2 | [(1,1),(0,2)] | 1 |
| 3 | [(1,2)] | 0 |

fresh가 0이므로 마지막 큐를 더 처리하지 않고 3을 반환합니다.

#### 994 · 정당성·시간·메모리의 근거

큐의 레벨은 어떤 시작점에서든 그 셀까지의 최소 간선 수입니다. 모든 간선의 전파 시간이 같으므로 먼저 발견한 시간이 최소입니다. 큐가 비어도 fresh가 남으면 경로가 없습니다.

격자 복사와 초기 스캔이 각각 O(RC)입니다. 각 칸은 한 번만 큐에 들어가고 나올 때 네 이웃을 검사하므로 전파도 O(RC)입니다. 세 단계의 합은 O(RC)이며 분 수를 RC에 다시 곱하지 않습니다.

board는 원본을 보존하려고 만든 RC칸 복사본입니다. 큐도 최대 RC칸을 담으므로 보조 공간은 O(RC)입니다. fresh와 minutes가 O(1) 변수여도 큰 board·queue가 존재하므로 전체 공간을 O(1)이라고 할 수 없습니다.

[[2,0,1]]은 -1, [[0,2]]는 0입니다. 다음 레벨까지 같은 분에 연쇄 처리하면 시간을 작게 계산합니다.

`grid=[[2,1,1],[0,1,0]] → 2`

`board=[row[:] for row in grid]`는 각 행도 복사해 원본의 값을 보존합니다. `fresh += board[r][c] == 1`은 비교 결과 True를 1, False를 0으로 더합니다. 예를 들어 [2,1,1]을 읽으면 fresh는 0→1→2가 됩니다.

큐가 비었는데 fresh가 남으면 도달 불가능하여 -1입니다. 처음부터 fresh가 0이면 시간이 흐를 필요 없이 0입니다.

### 구현과 실행

```python
from collections import deque
import heapq

def rot_minutes(grid):
    rows, cols = len(grid), len(grid[0])
    board = [row[:] for row in grid]
    queue, fresh, minutes = deque(), 0, 0
    for r in range(rows):
        for c in range(cols):
            if board[r][c] == 2:
                queue.append((r,c))
            fresh += board[r][c] == 1
    while queue and fresh:
        for _ in range(len(queue)):
            r, c = queue.popleft()
            for nr, nc in ((r-1,c),(r+1,c),(r,c-1),(r,c+1)):
                if 0 <= nr < rows and 0 <= nc < cols and board[nr][nc] == 1:
                    board[nr][nc] = 2
                    fresh -= 1
                    queue.append((nr,nc))
        minutes += 1
    return minutes if fresh == 0 else -1
```

```text
python trace_lab.py --case rot_minutes
```

위 예측과 trace의 반환값을 대조하세요. 입력을 앞에서 제안한 대로 바꾸고, 처음으로 상태가 달라지는 행을 찾아 그 변화가 답에 미친 영향을 설명합니다.

## 실습 보고서

작은 입력의 상태표, 완성 코드, 직접 만든 경계 입력과 예상값, 검증 결과를 함께 기록합니다. 시간 복잡도는 총 연산 횟수로, 공간 복잡도는 동시에 살아 있는 상태로 설명하세요. 입력을 복사하거나 정렬한다면 그 비용도 포함합니다.
