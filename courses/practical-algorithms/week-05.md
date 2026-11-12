---
layout: "course-note"
title: "Week 5: Heaps, intervals, and graph traversal"
title_ko: "5주차: 힙·구간·그래프 탐색"
course_id: "practical-algorithms"
permalink: "/courses/practical-algorithms/week-05/"
updated: "2026-11-12"
material_label: "Week 5 lecture"
material_label_ko: "5주차 강의"
pdf_en: "/assets/courses/practical-algorithms/week-05-en.pdf"
pdf_ko: "/assets/courses/practical-algorithms/week-05-ko.pdf"
reading_note: "/courses/practical-algorithms/week-05-reading/"
lab_bundle: "/assets/courses/practical-algorithms/week-05-code.zip"
practice_note: "/courses/practical-algorithms/week-05-practice/"
reading_pdf_en: "/assets/courses/practical-algorithms/week-05-reading-en.pdf"
reading_pdf_ko: "/assets/courses/practical-algorithms/week-05-reading-ko.pdf"
---

## Priorities and spreading failures

Maintain the top k measurements as values arrive, and merge overlapping maintenance intervals. On a sensor map, identify separate failure regions and the time needed for failures to spread.

Full ordering, partial ranking, and connectivity need different state. Track a heap boundary, the end of a sorted interval, and traversal visits.

<!-- lecture-page -->

## Week 5 learning outcomes

Sessions 9 and 10: Heap boundaries, interval unions, visited sets, and BFS levels

- Check contracts and boundary conditions.
- Trace state and implement in Python.
- Explain correctness, time, auxiliary space, and output space.

Opening scenarios, traces, and checks are additional teaching examples.

<!-- lecture-page -->

## Session 9 · Sorting, heaps, and intervals

Maintain top-k measurements and merge maintenance intervals. Separate questions requiring a full order from those requiring one priority boundary.

<!-- lecture-page -->

## Prerequisites and Python semantics

sorted(...,key=lambda item:item[0]) sorts by first coordinate. heapq is a min-heap: heapify O(n), push/pop O(log n). Equal tuple priorities compare later fields; add a counter before nonorderable payloads.

<!-- lecture-page -->

## Full sorting and partial ranking

- Full sort: O(n log n) time, all ranks available
- Size-k min-heap: retain only the top k
- New value ≤ root: keep the existing top k
- New value > root: replace the root and restore the heap

Import `heapq`. Heapify costs O(k), replacement O(log(k+1)); k=1 is supported.

<!-- lecture-page -->

## 215 · Problem and state

[LeetCode 215: Kth Largest Element in an Array](https://leetcode.com/problems/kth-largest-element-in-an-array/) · Medium

Return the kth value in descending order, counting duplicates.

`nums=[8,3,8,2,5], k=2 → 8`

Heapify the first k values; replace the root only when a later value is larger.

<!-- lecture-page -->

## 215 · Implementation

```python
def kth_largest(nums, k):
    heap = nums[:k]
    heapq.heapify(heap)
    for index in range(k, len(nums)):
        value = nums[index]
        if value > heap[0]:
            heapq.heapreplace(heap, value)
    return heap[0]
```

<!-- lecture-page -->

## 215 · Correctness and cost

The heap retains the largest k values seen. A new value at most its minimum cannot improve that set; a larger one replaces the minimum. The final root is kth largest.

n is length. O(n log(k+1)) time, O(k) space; heapify O(k). A full negated heap takes O(n+k log n) time and O(n) space.

<!-- lecture-page -->

## 56 · Problem and state

[LeetCode 56: Merge Intervals](https://leetcode.com/problems/merge-intervals/) · Medium

Return disjoint closed intervals covering the input union.

`intervals=[[5,7],[1,3],[3,6]] → [[1,7]]`

Sort by start; extend the last result end by max when intervals overlap.

<!-- lecture-page -->

## 56 · Implementation

```python
def merge_intervals(intervals):
    result = []
    for start, end in sorted(intervals, key=lambda item: item[0]):
        if result and start <= result[-1][1]:
            result[-1][1] = max(result[-1][1], end)
        else:
            result.append([start, end])
    return result
```

<!-- lecture-page -->

## 56 · Correctness and cost

result equals the union of the processed prefix. Increasing starts mean a new interval can overlap only the last result; a gap makes a new disjoint component.

n is interval count. O(n log n) sorting plus O(n) scan; O(n) sorting workspace and output. Input order is preserved.

<!-- lecture-page -->

## State trace

| incoming value(k=2) | retained multiset | root |
| --- | --- | --- |
| 8,3 | {3,8} | 3 |
| 8 | {8,8} | 8 |
| 2 | {8,8} | 8 |
| 5 | {8,8} | 8 |

Each row retains the largest two values seen, including duplicates.

<!-- lecture-page -->

## Failure inputs and concept checks

In a min-heap, each parent is no greater than its children, and the root holds a global minimum. Deduplicating changes the example’s answer.

Does insertion into a sorted list also cost log n?

The instructor answer is in the separate guide. Compare the reasoning line by line with the companion implementation.

<!-- lecture-page -->

## Session 10 · Graph representations and simultaneous spread

Count connected sensor regions and propagation time from multiple failures. Use DFS or BFS to find connected regions, and use BFS levels to compute earliest arrival when all edges have equal propagation time.

<!-- lecture-page -->

## Prerequisites and Python semantics

Represent a grid by coordinates, an adjacency list by vertex-to-neighbors, or an object graph by node.neighbors. Coordinate tuples are hashable; copy grid rows independently.

<!-- lecture-page -->

## 200 · Problem and state

[LeetCode 200: Number of Islands](https://leetcode.com/problems/number-of-islands/) · Medium

Count land components connected horizontally or vertically in a character grid.

`grid=[["1","0","1"],["1","0","0"]] → 2`

Start a stack traversal at each unseen land cell and mark its whole component.

<!-- lecture-page -->

## 200 · Implementation

```python
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

<!-- lecture-page -->

## 200 · Correctness and cost

A traversal reaches exactly its starting component. Marked components cannot restart; the number of starts equals the component count.

R,C are dimensions. O(RC) time and space; general adjacency lists take O(V+E) time.

<!-- lecture-page -->

## 994 · Problem and state

[LeetCode 994: Rotting Oranges](https://leetcode.com/problems/rotting-oranges/) · Medium

Return the minimum minutes for all fresh cells to change under simultaneous spread, or -1.

`grid=[[2,1,1],[0,1,0]] → 2`

Enqueue all sources together, process levels, and mark a discovered cell as 2 immediately.

<!-- lecture-page -->

## 994 · Implementation

```python
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

<!-- lecture-page -->

## 994 · Correctness and cost

BFS levels are minimum edge distances from any source. Equal edge durations make first discovery earliest; remaining fresh cells after exhaustion are unreachable.

R,C are dimensions. O(RC) time and O(RC) board-copy/queue space.

<!-- lecture-page -->

## State trace

| minute | current frontier | newly marked |
| --- | --- | --- |
| 0 | (0,0) | (0,1) |
| 1 | (0,1) | (0,2),(1,1) |
| 2 | (0,2),(1,1) | none |

The newly marked cells belong to time t+1, not time t.

<!-- lecture-page -->

## Failure inputs and concept checks

Use == for values; is tests identity. Diagonal land in a 2x2 grid forms two components.

Does BFS guarantee minimum cost with weighted edges?

The instructor answer is in the separate guide. Compare the reasoning line by line with the companion implementation.

<!-- lecture-page -->

## Time boundaries in simultaneous spread

| Time | Newly rotten at that time | Fresh cells left |
| --- | --- | --- |
| 0 | (0,0), initial source | 3 |
| 1 | (0,1) | 2 |
| 2 | (0,2), (1,1) | 0 |

Grid: `[[2,1,1],[0,1,0]]`. One iteration over a fixed queue length advances one minute. Mark cells when enqueuing them.

<!-- lecture-page -->

## Checkpoint questions

1. Find the answers for k=2 and k=5 in `[8,3,8,2,5]`.
2. Merge `[[1,8],[2,3]]` and, separately, `[[1,3],[3,6]]`.
3. Count components in `[["1","0"],["0","1"]]`.
4. Find spread times for `[[2,0,1]]` and `[[0,2]]`.

<!-- lecture-page -->

## Independent practice and connections

[Student exercises](/courses/practical-algorithms/week-05-practice/)

[Hints and solutions](/courses/practical-algorithms/week-05-reading/)

[Instructor guide](/courses/practical-algorithms/week-05-instructor/)

[Download Week 5 code](/assets/courses/practical-algorithms/week-05-code.zip)

Submit code, state definition, correctness argument, complexity, and boundary inputs. Week 8 includes a mixed assessment without pattern labels.

<!-- lecture-page -->

## Execution and sources

Run in the `code` folder of the [weekly code archive](/assets/courses/practical-algorithms/week-05-code.zip).

```text
python demo_09.py
python demo_10.py
python verify.py
python verify.py --student
```

Use the last command after implementing the student file.

Erik Demaine and Srini Devadas, [MIT 6.006: Introduction to Algorithms](https://ocw.mit.edu/courses/6-006-introduction-to-algorithms-fall-2011/) (2011).

<!-- ko -->

## 측정값의 우선순위와 장애 확산

측정값이 계속 들어오는 동안 상위 k개를 유지하고, 겹치는 정비 시간을 합쳐야 합니다. 센서 지도에서는 떨어진 장애 영역과 장애가 퍼지는 시간을 구합니다.

전체 정렬·부분 순위·연결 관계는 서로 다른 상태가 필요합니다. 힙의 경계, 정렬된 구간의 끝, 탐색의 방문 기록을 추적합니다.

<!-- lecture-page -->

## 5주차 학습 목표

9·10차시: 힙 경계·구간 합집합·방문 집합·BFS 레벨

- 입력 계약과 경계 조건 확인
- 상태 추적과 Python 구현
- 정당성·시간·보조 공간·출력 공간 설명

도입 상황, 표와 점검 문제는 강의용 추가 예시입니다.

<!-- lecture-page -->

## 9차시 · 정렬·힙·구간

계속 들어오는 수치의 상위 k개와 겹치는 정비 구간을 관리합니다. 모든 값을 완전 정렬해야 하는 질문과 최소 경계 하나만 필요한 질문을 구분합니다.

<!-- lecture-page -->

## 선수 지식과 Python 문법

sorted(items,key=lambda item:item[0])는 첫 좌표로 정렬합니다. heapq는 최소 힙입니다. heapify는 O(n), push/pop은 O(log n)입니다. tuple 우선순위가 같으면 다음 원소도 비교하므로 비교 불가 객체 앞에 고유 카운터를 둡니다.

<!-- lecture-page -->

## 완전 정렬과 부분 순위

- 전체 정렬: O(n log n) 시간, 모든 순위 확인
- 크기 k 최소 힙: 상위 k개만 저장
- 새 값 ≤ 루트: 기존 상위 k개 유지
- 새 값 > 루트: 루트 교체 후 힙 복구

`heapq`를 가져옵니다. heapify는 O(k), 교체는 O(log(k+1))이며 k=1도 처리합니다.

<!-- lecture-page -->

## 215 · 문제와 상태

[LeetCode 215: Kth Largest Element in an Array](https://leetcode.com/problems/kth-largest-element-in-an-array/) · Medium

정렬했을 때 큰 순서로 k번째 값을 반환합니다. 중복도 개수에 포함합니다.

`nums=[8,3,8,2,5], k=2 → 8`

처음 k개를 heapify하고 이후 값이 root보다 크면 heapreplace합니다.

<!-- lecture-page -->

## 215 · 구현

```python
def kth_largest(nums, k):
    heap = nums[:k]
    heapq.heapify(heap)
    for index in range(k, len(nums)):
        value = nums[index]
        if value > heap[0]:
            heapq.heapreplace(heap, value)
    return heap[0]
```

<!-- lecture-page -->

## 215 · 정당성과 비용

힙은 지금까지 본 값 중 큰 k개입니다. root 이하의 새 값은 상위 k개를 바꾸지 못하고, 큰 새 값은 가장 작은 보관 값을 대체해야 합니다. 마지막 root가 k번째입니다.

n=길이. O(n log(k+1)) 시간, O(k) 보조 공간. 초기 heapify O(k). 전체 음수 힙 대안은 O(n+k log n) 시간·O(n) 공간.

<!-- lecture-page -->

## 56 · 문제와 상태

[LeetCode 56: Merge Intervals](https://leetcode.com/problems/merge-intervals/) · Medium

닫힌 구간들의 합집합을 겹치지 않는 구간으로 반환합니다.

`intervals=[[5,7],[1,3],[3,6]] → [[1,7]]`

시작점으로 정렬하고 마지막 결과 구간과 겹치면 끝을 max로 늘립니다.

<!-- lecture-page -->

## 56 · 구현

```python
def merge_intervals(intervals):
    result = []
    for start, end in sorted(intervals, key=lambda item: item[0]):
        if result and start <= result[-1][1]:
            result[-1][1] = max(result[-1][1], end)
        else:
            result.append([start, end])
    return result
```

<!-- lecture-page -->

## 56 · 정당성과 비용

처리한 접두부의 합집합은 result와 같습니다. 시작점이 증가하므로 새 구간은 마지막 결과와만 겹칠 수 있습니다. 분리되면 이후에도 앞 결과와 겹치지 않습니다.

n=구간 수. 정렬 O(n log n), 스캔 O(n); 정렬 보조 O(n), 출력 O(n). 입력을 복사 정렬합니다.

<!-- lecture-page -->

## 상태 추적

| 입력 값(k=2) | 보관 값(중복 포함) | root |
| --- | --- | --- |
| 8,3 | {3,8} | 3 |
| 8 | {8,8} | 8 |
| 2 | {8,8} | 8 |
| 5 | {8,8} | 8 |

각 행은 지금까지 본 값 중 큰 두 개를 중복 포함해 유지합니다.

<!-- lecture-page -->

## 실패 입력과 이해 확인

최소 힙에서는 각 부모의 값이 자식 이하이고, root에 전체 최솟값이 놓입니다. 중복을 set으로 없애면 예시의 답이 달라집니다.

정렬된 배열에 반복 삽입하는 비용도 log n인가요?

교사용 답은 별도 진행안에 있습니다. 코드 설명은 읽기자료의 구현과 줄별로 대조합니다.

<!-- lecture-page -->

## 10차시 · 그래프 표현과 동시 전파

센서 격자의 연결된 영역을 세고 여러 시작점에서 번지는 장애 시간을 구합니다. 연결된 영역은 DFS나 BFS로 찾고, 간선별 전파 시간이 같을 때의 최소 도착 시간은 BFS의 레벨로 계산합니다.

<!-- lecture-page -->

## 선수 지식과 Python 문법

격자는 (row,col), 인접 리스트는 정점→이웃 목록, 객체 그래프는 node.neighbors로 표현합니다. 좌표 tuple은 set에 넣을 수 있습니다. 복사 지도는 [row[:] for row in grid]로 만듭니다.

<!-- lecture-page -->

## 200 · 문제와 상태

[LeetCode 200: Number of Islands](https://leetcode.com/problems/number-of-islands/) · Medium

문자 격자의 상하좌우로 연결된 육지 덩어리 수를 반환합니다.

`grid=[["1","0","1"],["1","0","0"]] → 2`

미방문 육지에서 count를 늘리고 연결된 육지를 스택으로 모두 표시합니다.

<!-- lecture-page -->

## 200 · 구현

```python
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

<!-- lecture-page -->

## 200 · 정당성과 비용

한 번 시작한 탐색은 연결 경로를 따라 그 성분의 모든 노드와 그 노드만 방문합니다. 이미 표시한 성분은 다시 시작하지 않으므로 시작 횟수가 성분 수입니다.

R,C=행·열 수. O(RC) 시간·O(RC) 보조 공간. 일반 인접 리스트에서는 O(V+E) 시간입니다.

<!-- lecture-page -->

## 994 · 문제와 상태

[LeetCode 994: Rotting Oranges](https://leetcode.com/problems/rotting-oranges/) · Medium

동시에 퍼지는 변화를 적용해 모든 신선한 셀이 바뀌는 최소 분을 반환합니다. 불가능하면 -1입니다.

`grid=[[2,1,1],[0,1,0]] → 2`

모든 시작점을 같은 큐에 넣고 레벨별로 처리합니다. 새 셀은 enqueue할 때 즉시 2로 바꿉니다.

<!-- lecture-page -->

## 994 · 구현

```python
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

<!-- lecture-page -->

## 994 · 정당성과 비용

큐의 레벨은 어떤 시작점에서든 그 셀까지의 최소 간선 수입니다. 모든 간선의 전파 시간이 같으므로 먼저 발견한 시간이 최소입니다. 큐가 비어도 fresh가 남으면 경로가 없습니다.

R,C=행·열 수. O(RC) 시간, 복사 board와 큐 O(RC) 보조 공간.

<!-- lecture-page -->

## 상태 추적

| 분 | 처리 frontier | 새로 표시 |
| --- | --- | --- |
| 0 | (0,0) | (0,1) |
| 1 | (0,1) | (0,2),(1,1) |
| 2 | (0,2),(1,1) | 없음 |

새로 표시한 셀의 시점은 t가 아니라 t+1입니다.

<!-- lecture-page -->

## 실패 입력과 이해 확인

값 비교는 ==입니다. is는 객체 동일성입니다. [["1","0"],["0","1"]]은 대각선을 연결하지 않아 두 성분입니다.

BFS가 가중 간선에서도 최소 비용을 보장하나요?

교사용 답은 별도 진행안에 있습니다. 코드 설명은 읽기자료의 구현과 줄별로 대조합니다.

<!-- lecture-page -->

## 동시 전파의 시간 경계

| 시간 | 그 시점에 새로 썩은 셀 | 남은 신선한 셀 |
| --- | --- | --- |
| 0 | (0,0), 초기 시작점 | 3 |
| 1 | (0,1) | 2 |
| 2 | (0,2), (1,1) | 0 |

격자 `[[2,1,1],[0,1,0]]`. 큐 길이를 고정한 한 번의 반복이 1분입니다. 새 셀은 큐에 넣을 때 표시합니다.

<!-- lecture-page -->

## 중간 점검

1. `[8,3,8,2,5]`에서 k=2와 k=5의 답은?
2. `[[1,8],[2,3]]`과 `[[1,3],[3,6]]`의 합집합은?
3. `[["1","0"],["0","1"]]`의 연결 성분 수는?
4. `[[2,0,1]]`과 `[[0,2]]`의 전파 시간은?

<!-- lecture-page -->

## 독립 실습과 다음 연결

[학생 실습](/courses/practical-algorithms/week-05-practice/)

[힌트·해설](/courses/practical-algorithms/week-05-reading/)

[교사용 진행안](/courses/practical-algorithms/week-05-instructor/)

[5주차 코드 내려받기](/assets/courses/practical-algorithms/week-05-code.zip)

코드·상태 정의·정당성·복잡도·경계 입력을 함께 제출합니다. 8주차에는 주제를 숨긴 혼합 평가가 있습니다.

<!-- lecture-page -->

## 실행과 참고자료

[주차별 코드](/assets/courses/practical-algorithms/week-05-code.zip)의 `code` 폴더에서 실행합니다.

```text
python demo_09.py
python demo_10.py
python verify.py
python verify.py --student
```

마지막 명령은 학생 파일을 구현한 뒤 실행합니다.

Erik Demaine·Srini Devadas, [MIT 6.006: Introduction to Algorithms](https://ocw.mit.edu/courses/6-006-introduction-to-algorithms-fall-2011/) (2011).
