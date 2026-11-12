---
layout: "course-note"
title: "Week 6 Worked Companion"
title_ko: "6주차 풀이 읽기자료"
course_id: "practical-algorithms"
permalink: "/courses/practical-algorithms/week-06-reading/"
updated: "2026-11-12"
material_label: "Week 6 reading"
material_label_ko: "6주차 읽기자료"
pdf_en: "/assets/courses/practical-algorithms/week-06-reading-en.pdf"
pdf_ko: "/assets/courses/practical-algorithms/week-06-reading-ko.pdf"
lecture_note: "/courses/practical-algorithms/week-06/"
practice_note: "/courses/practical-algorithms/week-06-practice/"
---

## Using the worked companion

Attempt the student exercises independently first. This companion contains hints and complete solutions. Read only as far as needed, then return to your attempt.

Examples are original teaching examples. Follow each official link for the source problem and its complete contract.

[Student exercises](/courses/practical-algorithms/week-06-practice/)

[Instructor guide](/courses/practical-algorithms/week-06-instructor/)

[Download Week 6 code](/assets/courses/practical-algorithms/week-06-code.zip)

<!-- lecture-page -->

## 207 · Staged hints

[LeetCode 207: Course Schedule](https://leetcode.com/problems/course-schedule/) · Medium

H1. Which courses have no remaining prerequisites?

H2. Can checking one component detect all cycles?

H3. Direct edges before→after, remove zero-indegree nodes, and compare the removed count with V.

<!-- lecture-page -->

## 207 · Correctness and cost

Each removed node has no remaining prerequisite. Every nonempty DAG has a zero-indegree node, so an unprocessed remainder must contain a cycle.

V is courses, E constraints. O(V+E) time and auxiliary space including the graph.

<!-- lecture-page -->

## 207 · Counterexamples and checks

[[1,0],[0,1]] is cyclic. A vertex in state 1 lies on the current search path. An edge back to it identifies a cycle. A vertex in state 2 has completed its search, so its result can be reused.

`n=3, prerequisites=[[1,0],[2,1]] → True`

Predict the state and return value before running this example. Then check the boundary cases above.

<!-- lecture-page -->

## 207 · Implementation

```python
def can_finish(n, prerequisites):
    return len(course_order(n, prerequisites)) == n
```

<!-- lecture-page -->

## 210 · Staged hints

[LeetCode 210: Course Schedule II](https://leetcode.com/problems/course-schedule-ii/) · Medium

H1. Must the valid order be unique?

H2. How can the returned order be checked independently?

H3. Record Kahn queue removals and require V nodes at the end.

<!-- lecture-page -->

## 210 · Correctness and cost

A course enters only after all prerequisites were removed, so every before precedes after in the result. A short result cannot be a complete order.

V is courses, E edges. O(V+E) time and total graph/queue/indegree/output space.

<!-- lecture-page -->

## 210 · Counterexamples and checks

Reading [[1,0]] as 1→0 reverses the dependency. Validate edges instead of comparing with one chosen valid order.

`n=4, prerequisites=[[2,0],[2,1],[3,2]] → [0,1,2,3]`

Predict the state and return value before running this example. Then check the boundary cases above.

<!-- lecture-page -->

## 210 · Implementation

```python
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

<!-- lecture-page -->

## 78 · Staged hints

[LeetCode 78: Subsets](https://leetcode.com/problems/subsets/) · Medium

H1. Will later pops change a stored path?

H2. Must later choices return to earlier indices?

H3. Choose an index at least start, recurse from the next index, pop, and store path.copy() at each call.

<!-- lecture-page -->

## 78 · Correctness and cost

Every subset has one increasing index sequence. start permits exactly that sequence, and restoration returns the parent path to its prior state.

n is length. O(n·<math xmlns="http://www.w3.org/1998/Math/MathML"><msup><mn>2</mn><mi>n</mi></msup></math>) time/output including snapshots; O(n) path and call stack.

<!-- lecture-page -->

## 78 · Counterexamples and checks

result.append(path) stores one shared object; later pops can turn multiple results into empty lists.

`nums=[2,5] → [[],[2],[2,5],[5]]`

Predict the state and return value before running this example. Then check the boundary cases above.

<!-- lecture-page -->

## 78 · Implementation

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

<!-- lecture-page -->

## 39 · Staged hints

[LeetCode 39: Combination Sum](https://leetcode.com/problems/combination-sum/) · Medium

H1. Which next start permits reusing the same candidate?

H2. Would remaining keep decreasing with nonpositive candidates?

H3. Sort candidates, recurse from the same index to permit reuse, and stop at values exceeding remaining.

<!-- lecture-page -->

## 39 · Correctness and cost

Positive choices decrease remaining and ensure termination. Nondecreasing indices avoid permutations while representing every combination.

m candidates,T target,c minimum,L=floor(T/c),B visited calls,S output elements. Time O(m log m+mB+S), auxiliary O(m+L), output O(S); conservatively B=O(<math xmlns="http://www.w3.org/1998/Math/MathML"><msup><mrow><mo>(</mo><mi>m</mi><mo>+</mo><mn>1</mn><mo>)</mo></mrow><mrow><mi>L</mi><mo>+</mo><mn>1</mn></mrow></msup></math>).

<!-- lecture-page -->

## 39 · Counterexamples and checks

Recursing at index+1 misses [2,2] for [2], target=4. Zero is outside the contract and breaks termination.

`candidates=[2,5], target=7 → [[2,5]]`

Predict the state and return value before running this example. Then check the boundary cases above.

<!-- lecture-page -->

## 39 · Implementation

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

<!-- lecture-page -->

## Execution and sources

```text
cd code
python demo_11.py
python demo_12.py
python verify.py
```

Standard-library imports are in `solutions.py`. On LeetCode, adapt the function to the official method signature.

Erik Demaine and Srini Devadas, [Introduction to Algorithms, MIT 6.006](https://ocw.mit.edu/courses/6-006-introduction-to-algorithms-fall-2011/) (Fall 2011).

<!-- lecture-page -->

## Checkpoint answers and reasoning

1. None exists: each course waits for the other, so return `[]`.
2. Yes. Both 0 and 1 only need to precede 2.
3. Four subsets, including `[]`. Copy the path so later pops do not alter saved results.
4. Reuse index 0. Advancing to the next index misses `[2,2]`.

<!-- lecture-page -->

## Concept-check explanations

DFS state 1 is on the active path, so an edge back to it identifies a cycle. State 2 has left that path. In `0→1`, `0→2`, `2→1`, revisiting completed node 1 is not a cycle.

A recursive return ends only that call. The parent resumes with pop and the next loop choice. Use Kahn’s algorithm for long graphs to avoid recursion-depth limits.

<!-- ko -->

## 해설 사용 순서

먼저 학생 실습에서 문제를 독립적으로 풉니다. 이 자료는 힌트와 완전 해설을 포함합니다. 필요한 단계까지만 읽고 다시 풀이합니다.

표시된 예시는 강의에서 만든 예시입니다. 원문과 전체 제약은 각 공식 링크에서 확인합니다.

[학생 실습](/courses/practical-algorithms/week-06-practice/)

[교사용 진행안](/courses/practical-algorithms/week-06-instructor/)

[6주차 코드 내려받기](/assets/courses/practical-algorithms/week-06-code.zip)

<!-- lecture-page -->

## 207 · 단계별 힌트

[LeetCode 207: Course Schedule](https://leetcode.com/problems/course-schedule/) · Medium

H1. 아직 남은 선수 조건이 없는 과목은 무엇인가요?

H2. 일부 성분만 검사하면 전체 사이클을 알 수 있나요?

H3. before→after로 간선을 만들고 진입차수 0부터 제거합니다. 제거 수가 V이면 True입니다.

<!-- lecture-page -->

## 207 · 정당성과 비용

제거 시 남은 선수 조건이 없으므로 선택은 안전합니다. 남은 유향 비순환 그래프에는 진입차수 0 노드가 있어야 합니다. V개를 제거하지 못하면 남은 부분에 사이클이 있습니다.

V=과목 수,E=조건 수. O(V+E) 시간, 인접 리스트 포함 O(V+E) 보조 공간.

<!-- lecture-page -->

## 207 · 반례와 검증

[[1,0],[0,1]]은 사이클입니다. 상태 1인 정점은 현재 탐색 경로에 있습니다. 그 정점으로 돌아가는 간선을 만나면 사이클입니다. 상태 2인 정점은 탐색이 끝났으므로 결과를 재사용합니다.

`n=3, prerequisites=[[1,0],[2,1]] → True`

실행 전에 상태와 반환값을 적고 위의 경계 사례도 확인합니다.

<!-- lecture-page -->

## 207 · 구현

```python
def can_finish(n, prerequisites):
    return len(course_order(n, prerequisites)) == n
```

<!-- lecture-page -->

## 210 · 단계별 힌트

[LeetCode 210: Course Schedule II](https://leetcode.com/problems/course-schedule-ii/) · Medium

H1. 정답 순서는 유일해야 하나요?

H2. 반환한 순서를 어떻게 알고리즘과 독립적으로 검사하나요?

H3. 진입차수 0 큐에서 꺼낸 순서를 저장하고 마지막에 V개인지 확인합니다.

<!-- lecture-page -->

## 210 · 정당성과 비용

각 과목은 모든 선수가 제거된 뒤에만 큐에 들어갑니다. 따라서 반환 순서에서 모든 before의 위치가 after보다 앞섭니다. 수가 부족하면 전체 순서가 아닙니다.

V=과목 수,E=간선 수. O(V+E) 시간, graph·indegree·queue·출력 합 O(V+E).

<!-- lecture-page -->

## 210 · 반례와 검증

[[1,0]]을 1→0으로 읽으면 역순을 만듭니다. 정답 하나와 목록을 직접 비교하지 말고 모든 간선을 검증합니다.

`n=4, prerequisites=[[2,0],[2,1],[3,2]] → [0,1,2,3]`

실행 전에 상태와 반환값을 적고 위의 경계 사례도 확인합니다.

<!-- lecture-page -->

## 210 · 구현

```python
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

<!-- lecture-page -->

## 78 · 단계별 힌트

[LeetCode 78: Subsets](https://leetcode.com/problems/subsets/) · Medium

H1. 현재 path를 결과에 넣으면 이후 pop의 영향이 있나요?

H2. 선택한 인덱스보다 앞쪽으로 돌아갈 필요가 있나요?

H3. start 이상에서 하나를 선택하고 다음 인덱스부터 재귀한 뒤 pop합니다. 매 호출에서 path.copy()를 저장합니다.

<!-- lecture-page -->

## 78 · 정당성과 비용

부분집합마다 오름차순 인덱스 열이 하나 있습니다. start가 그 열만 허용하므로 모든 부분집합을 정확히 한 번 만듭니다. 복원 후 부모의 path는 호출 전과 같습니다.

n=길이. snapshot 포함 O(n·<math xmlns="http://www.w3.org/1998/Math/MathML"><msup><mn>2</mn><mi>n</mi></msup></math>) 시간·출력 공간, path와 호출 스택 O(n).

<!-- lecture-page -->

## 78 · 반례와 검증

result.append(path)는 같은 객체를 보관합니다. 마지막 pop 뒤 여러 결과가 빈 목록으로 바뀔 수 있습니다.

`nums=[2,5] → [[],[2],[2,5],[5]]`

실행 전에 상태와 반환값을 적고 위의 경계 사례도 확인합니다.

<!-- lecture-page -->

## 78 · 구현

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

<!-- lecture-page -->

## 39 · 단계별 힌트

[LeetCode 39: Combination Sum](https://leetcode.com/problems/combination-sum/) · Medium

H1. 같은 후보를 다시 쓰려면 다음 start는 무엇인가요?

H2. 양수가 아니면 remaining이 계속 감소하나요?

H3. 정렬한 후보에서 같은 index로 재귀해 재사용을 허용하고, remaining보다 큰 후보부터는 중단합니다.

<!-- lecture-page -->

## 39 · 정당성과 비용

양수 선택마다 remaining이 감소해 종료합니다. 비내림차순 인덱스만 선택하므로 순서만 다른 중복을 피하고 모든 가능한 조합을 표현합니다.

m=후보 수,T=target,c=최소 후보,L=floor(T/c),B=방문 호출 수,S=출력 원소 합. 시간 O(m log m + mB + S), 보조 O(m+L), 출력 O(S). B는 보수적으로 O(<math xmlns="http://www.w3.org/1998/Math/MathML"><msup><mrow><mo>(</mo><mi>m</mi><mo>+</mo><mn>1</mn><mo>)</mo></mrow><mrow><mi>L</mi><mo>+</mo><mn>1</mn></mrow></msup></math>).

<!-- lecture-page -->

## 39 · 반례와 검증

index+1로 재귀하면 [2], target=4의 [2,2]를 놓칩니다. 후보 0은 공식 범위 밖이며 종료 논리를 깨뜨립니다.

`candidates=[2,5], target=7 → [[2,5]]`

실행 전에 상태와 반환값을 적고 위의 경계 사례도 확인합니다.

<!-- lecture-page -->

## 39 · 구현

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

<!-- lecture-page -->

## 실행과 참고자료

```text
cd code
python demo_11.py
python demo_12.py
python verify.py
```

표준 라이브러리 import는 `solutions.py`에 있습니다. LeetCode에서는 공식 메서드 서명에 맞춰 함수를 연결합니다.

Erik Demaine and Srini Devadas, [Introduction to Algorithms, MIT 6.006](https://ocw.mit.edu/courses/6-006-introduction-to-algorithms-fall-2011/) (Fall 2011).

<!-- lecture-page -->

## 중간 점검의 답과 근거

1. 없습니다. 두 과목이 서로를 기다리므로 빈 목록을 반환합니다.
2. 정답입니다. 0과 1이 모두 2보다 먼저 나오면 됩니다.
3. 4개이며 `[]`도 하나입니다. 경로를 복사해야 이후 pop이 저장된 답을 바꾸지 않습니다.
4. 같은 인덱스 0. 다음 인덱스로 이동하면 필요한 `[2,2]`를 놓칩니다.

<!-- lecture-page -->

## 개념 질문 해설

DFS의 진행 중 상태 1은 현재 경로에 있으므로 그곳으로 돌아가는 간선은 사이클입니다. 완료 상태 2는 경로에서 빠진 정점입니다. `0→1`, `0→2`, `2→1`에서 완료된 1의 재방문은 사이클이 아닙니다.

재귀의 return은 그 호출만 끝냅니다. 부모는 호출 다음 줄의 pop을 수행하고 for의 다음 선택을 처리합니다. 긴 그래프는 재귀 제한을 피하는 Kahn 구현으로 풉니다.
