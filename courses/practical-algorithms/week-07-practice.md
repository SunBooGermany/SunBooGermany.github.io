---
layout: "course-resource"
title: "Week 7 Student Exercises"
title_ko: "7주차 학생 실습"
permalink: "/courses/practical-algorithms/week-07-practice/"
course_id: "practical-algorithms"
---

## Set up and run

Extract the [lab code ZIP](/assets/courses/practical-algorithms/week-07-code.zip) and work in its code folder. Use Python 3.11+ and the standard library.

```text
python trace_lab.py --case rob
python verify.py
python verify.py --student
```

Predict the small example and its states on paper first. `trace_lab.py` traces the actual `solutions.py` implementation. `before L…` shows values immediately before that line executes: identify what the preceding executed line changed. Linked lists display a chain; tree nodes display their value and child values. Exclude tracing, copying, and printing overhead from the algorithm's complexity.

Implement the functions and methods in `student_week_07.py`, then run `verify.py --student`. An initial `NotImplementedError` identifies work still to implement. Without `--student`, the verifier checks the supplied solutions. Use `python trace_lab.py --case FUNCTION --student` to inspect your implementation.

For each task record the input/output meaning, state invariant, one state transition, final answer, time, auxiliary space, and output space. Passing one small example does not establish correctness for all inputs.

## This week’s problems

- [rob](#en-rob)
- [coin_change](#en-coin_change)
- [unique_paths](#en-unique_paths)
- [lcs](#en-lcs)

## Worked solutions

198 | 322 | 62 | 1143

What information is needed to maximize inspection value when adjacent items cannot both be selected? Grid paths and common order in two event logs can also be divided into smaller problems.

Store and reuse previously computed optima or counts. The meaning of the state determines whether to add, minimize, or maximize.

## DP state meaning and evaluation order

Dynamic programming stores and reuses answers to repeated subproblems. Define what one table entry means before choosing base cases and transitions.

![Dependency directions in path-count and common-subsequence tables](/assets/courses/practical-algorithms/curriculum/dp-dependencies.svg)

| Problem | Meaning of a state | Combination |
| --- | --- | --- |
| Maximum nonadjacent sum | Best value for a prefix | max(select,skip) |
| Coins | Minimum count for an amount | min over final coins |
| Grid paths | Number of paths reaching a cell | top+left |
| Common subsequence | Best length for two prefixes | diagonal+1 on match; otherwise max |

Time counts states times work per state. Space counts states retained simultaneously. The nonadjacent-sum problem needs only two prior states, but a table implementation is not automatically constant-space.

<a id="en-rob"></a>

## [LeetCode 198: House Robber](https://leetcode.com/problems/house-robber/) · Medium

Maximize selected value without selecting adjacent positions.

1 <= n <= 100; values 0..400.

### Predict before implementing

At each house compare skip=current_best with take=best_two_back+value. Compute the new best before shifting the two states. Prefix optima are 2,7,11,11,12; the last answer selects 2+9+1.

```python
rob([2, 7, 9, 3, 1],)
# 12
```

### Idea and state transitions

#### 198 · Idea and execution trace

[LeetCode 198: House Robber](https://leetcode.com/problems/house-robber/) · Medium

Maximize selected value without selecting adjacent positions.

Selecting the current value excludes its immediate predecessor. The best prefix value is therefore the larger of skipping the current value or adding it to the best prefix ending two positions earlier. Only those two prior results are needed for the next decision.

`nums=[3,1,4,2]`. Evaluate the entire right-hand side using old values before assignment.

| value | Old previous_two | Old previous_one | New previous_one |
| --- | --- | --- | --- |
| 3 | 0 | 0 | max(0,0+3)=3 |
| 1 | 0 | 3 | max(3,0+1)=3 |
| 4 | 3 | 3 | max(3,3+4)=7 |
| 2 | 3 | 7 | max(7,3+2)=7 |

#### A recurrence table and its two variables

Let D[i] be the maximum sum from the first i values. For [3,1,4,2], the empty prefix has D[0]=0.

| i and current value | Skip current | Take current | D[i] |
| --- | --- | --- | --- |
| 1, value 3 | 0 | 0+3 | 3 |
| 2, value 1 | D[1]=3 | D[0]+1=1 | 3 |
| 3, value 4 | D[2]=3 | D[1]+4=7 | 7 |
| 4, value 2 | D[3]=7 | D[2]+2=5 | 7 |

Before processing 4, previous_two=D[1] and previous_one=D[2]. After the update they become D[2] and D[3], preserving their roles for the next iteration. Taking the current value with D[i−1] could also take its neighbor, violating the constraint.

The branch taking 4 adds it to the already computed prefix optimum 3. Reusing that optimum rather than solving the prefix again is the DP step.

#### 198 · Why it works; time and memory

Every optimum either selects the current item or skips it. Each case leaves an optimal prefix, so the recurrence covers all optima.

For each of n values, perform one addition, one max comparison, and a fixed number of assignments. With constant-cost arithmetic for the input range, time is O(n). Prior prefix optima are already computed rather than searched again.

Only two optima and the current value are retained, independent of n, giving O(1) auxiliary space. A full prefix table would use O(n); this implementation retains only the two dependencies. Reconstructing selected positions requires additional information.

Summing only even or only odd positions misses optimum 4 for [2,1,1,2].

`nums=[3,1,4,2] → 7`

### Implement and execute

```python
from collections import deque
import heapq

def rob(nums):
    previous_two = previous_one = 0
    for value in nums:
        previous_two, previous_one = previous_one, max(previous_one, previous_two + value)
    return previous_one
```

```text
python trace_lab.py --case rob
```

Compare the trace return value with your prediction. Make the input change proposed above, find the first line where the state differs, and explain its effect on the answer.

<a id="en-coin_change"></a>

## [LeetCode 322: Coin Change](https://leetcode.com/problems/coin-change/) · Medium

Return the minimum coin count for amount, or -1 if impossible.

1..12 coins, values 1..<math xmlns="http://www.w3.org/1998/Math/MathML"><msup><mn>2</mn><mn>31</mn></msup></math>-1; amount 0..<math xmlns="http://www.w3.org/1998/Math/MathML"><msup><mn>10</mn><mn>4</mn></msup></math>; unlimited reuse.

### Predict before implementing

Let dp[a] be the minimum coins for amount a; set dp[0]=0 and other entries unreachable. Evaluate increasing amounts from smaller predecessors. The table is 0,1,2,1,1,2,2; 3+3 beats greedy 4+1+1.

```python
coin_change([1, 3, 4], 6)
# 2
```

### Idea and state transitions

#### 322 · Idea and execution trace

[LeetCode 322: Coin Change](https://leetcode.com/problems/coin-change/) · Medium

Return the minimum coin count for amount, or -1 if impossible.

If the last coin for amount a is c, the preceding coins must form an optimum for a-c. Compare every possible final coin. Choosing the largest coin first fails for amount 6 with `[1,3,4]`: 4+1+1 uses more coins than 3+3.

`coins=[1,3,4], amount=6`. Values are finalized after checking every coin for that total.

| total | Candidates dp[total-coin]+1 | Final dp[total] |
| --- | --- | --- |
| 0 | No coins needed | 0 |
| 1,2 | 0+1 / 1+1 | 1,2 |
| 3 | 2+1, 0+1 | 1 |
| 4 | 1+1, 1+1, 0+1 | 1 |
| 5 | 1+1, 2+1, 1+1 | 2 |
| 6 | 2+1, 1+1, 2+1 | 2 |

#### 322 · Why it works; time and memory

Removing the last coin c from an optimum leaves an optimum for a-c. Comparing all final coins finds the minimum; positive values ensure dependencies were filled earlier.

Each of A amount states checks m coins, giving at most A·m transitions. Each uses constant-time indexing, addition, and comparison, so time is O(Am). The outer bound is the numeric target A, not the number of coins.

The table has A+1 entries and other variables are constant-size, giving O(A) auxiliary space. Since A takes only O(log A) input bits, this is pseudopolynomial time in that bit length. The input coin list is not counted again as workspace.

Largest-first chooses 4+1+1 instead of 3+3 for [1,3,4],6. [2],3 gives -1; amount zero gives zero.

`coins=[1,3,4], amount=6 → 2`

### Implement and execute

```python
from collections import deque
import heapq

def coin_change(coins, amount):
    dp = [float("inf")] * (amount + 1)
    dp[0] = 0
    for total in range(1, amount + 1):
        for coin in coins:
            if coin <= total:
                dp[total] = min(dp[total], dp[total - coin] + 1)
    return -1 if dp[amount] == float("inf") else dp[amount]
```

```text
python trace_lab.py --case coin_change
```

Compare the trace return value with your prediction. Make the input change proposed above, find the first line where the state differs, and explain its effect on the answer.

<a id="en-unique_paths"></a>

## [LeetCode 62: Unique Paths](https://leetcode.com/problems/unique-paths/) · Medium

Count grid paths using only right and down moves.

1 <= R,C <= 100; supplied inputs have answer at most 2×<math xmlns="http://www.w3.org/1998/Math/MathML"><msup><mn>10</mn><mn>9</mn></msup></math>.

### Predict before implementing

A cell receives paths from above and left. In a one-row buffer, dp[col] still means above while dp[col-1] already means left. Rows become [1,1,1,1], [1,2,3,4], [1,3,6,10].

```python
unique_paths(3, 4)
# 10
```

### Idea and state transitions

#### 62 · Idea and execution trace

[LeetCode 62: Unique Paths](https://leetcode.com/problems/unique-paths/) · Medium

Count grid paths using only right and down moves.

With only right and down moves, the last move into a cell comes either from above or from the left. These cases have different last moves and are disjoint, so add their path counts rather than taking a maximum.

rows=3, cols=3. The first row and column have one possible route.

| Cell processed | Calculation | Current dp rows |
| --- | --- | --- |
| Initialize | Boundary values 1 | [1,1,1] / [1,1,1] / [1,1,1] |
| (1,1) | 1+1=2 | [1,1,1] / [1,2,1] / [1,1,1] |
| (1,2) | 1+2=3 | [1,1,1] / [1,2,3] / [1,1,1] |
| (2,1) | 2+1=3 | [1,1,1] / [1,2,3] / [1,3,1] |
| (2,2) | 3+3=6 | [1,1,1] / [1,2,3] / [1,3,6] |

#### 62 · Why it works; time and memory

Every path arrives from top or left. These disjoint classes cover all paths, so counts add; row order respects dependencies.

Initialization touches R·C cells; transitions fill (R-1)(C-1) cells. Two lookups and one addition per cell give O(RC) time. Paths are counted rather than enumerated, so runtime is not proportional to the number of paths.

Keeping the whole dp table uses O(RC) auxiliary space. This implementation is not the one-row O(C) optimization. Arithmetic is treated as constant within the official bounded-answer contract; unrestricted large grids would add large-integer bit costs.

`[[1]*C]*R` aliases rows; use a comprehension creating each row.

`rows=2, cols=4 → 4`

### Implement and execute

```python
from collections import deque
import heapq

def unique_paths(rows, cols):
    dp = [[1] * cols for _ in range(rows)]
    for r in range(1, rows):
        for c in range(1, cols):
            dp[r][c] = dp[r-1][c] + dp[r][c-1]
    return dp[-1][-1]
```

```text
python trace_lab.py --case unique_paths
```

Compare the trace return value with your prediction. Make the input change proposed above, find the first line where the state differs, and explain its effect on the answer.

<a id="en-lcs"></a>

## [LeetCode 1143: Longest Common Subsequence](https://leetcode.com/problems/longest-common-subsequence/) · Medium

Return the length of a longest common subsequence preserving order.

Each length 1..1000; lowercase English letters.

### Predict before implementing

Define dp[i][j] for the two prefixes. Equal final characters extend the diagonal by one; unequal characters take the larger value after dropping one final character. Highlight the a,c,e diagonal extensions.

```python
lcs('abcde', 'ace')
# 3
```

### Idea and state transitions

#### 1143 · Idea and execution trace

[LeetCode 1143: Longest Common Subsequence](https://leetcode.com/problems/longest-common-subsequence/) · Medium

Return the length of a longest common subsequence preserving order.

Store answers for pairs of prefixes. If their final characters match, pair them and add one to the shorter-prefix answer. Otherwise they cannot be paired with each other, so take the better result from omitting either final character.

`first="abc", second="ac"`. Rows and columns are prefixes of the two strings.

| Completed row | Empty prefix | a | ac |
| --- | --- | --- | --- |
| Empty prefix | 0 | 0 | 0 |
| a | 0 | 1 (=0+1) | 1 (=max(0,1)) |
| ab | 0 | 1 (=max(1,0)) | 1 (=max(1,1)) |
| abc | 0 | 1 (=max(1,0)) | 2 (=1+1) |

The answer 2 is the length of `ac`. Skipping b distinguishes a subsequence from a contiguous substring.

#### 1143 · Why it works; time and memory

Equal final characters can be paired in an optimum. Unequal ends cannot both be the final match, so at least one is skipped; maximize over both cases.

For lengths n and m, there are (n+1)(m+1) prefix pairs. Each interior cell uses one character comparison and an addition or max, giving O(nm) time. It becomes O(<math xmlns="http://www.w3.org/1998/Math/MathML"><msup><mi>n</mi><mn>2</mn></msup></math>) only when the two lengths have the same scale.

The full table uses O(nm) auxiliary space, while the returned length occupies O(1). Reconstructing an actual common subsequence would require traceback and output-character storage.

A subsequence preserves character order while allowing characters to be skipped. Skipping b in "abc" gives "ac", so their longest common subsequence has length 2.

`first="abca", second="aca" → 3`

When both final characters are c, an optimal subsequence can be chosen to match those final positions. A subsequence using neither final position can be extended by c; a match using an earlier c can move to the final c without changing order. This is why the matching case needs only the diagonal optimum plus one.

### Implement and execute

```python
from collections import deque
import heapq

def lcs(first, second):
    rows, cols = len(first), len(second)
    dp = [[0] * (cols + 1) for _ in range(rows + 1)]
    for r in range(1, rows + 1):
        for c in range(1, cols + 1):
            if first[r-1] == second[c-1]:
                dp[r][c] = dp[r-1][c-1] + 1
            else:
                dp[r][c] = max(dp[r-1][c], dp[r][c-1])
    return dp[rows][cols]
```

```text
python trace_lab.py --case lcs
```

Compare the trace return value with your prediction. Make the input change proposed above, find the first line where the state differs, and explain its effect on the answer.

## Lab report

Include the small-input state table, completed code, your own boundary input and expected result, and verification results. Explain time by total operation counts and space by simultaneously live state. Include any input copying or sorting costs.

<!-- ko -->

## 실행 준비

[실습 코드 ZIP](/assets/courses/practical-algorithms/week-07-code.zip)을 풀고 코드 폴더에서 실행합니다. Python 3.11 이상과 표준 라이브러리를 사용합니다.

```text
python trace_lab.py --case rob
python verify.py
python verify.py --student
```

먼저 작은 입력의 답과 상태 변화를 종이에 적고 실행 결과와 비교하세요. `trace_lab.py`는 `solutions.py`의 실제 실행을 추적합니다. `before L…`은 그 행을 실행하기 직전의 값이므로, 앞서 실행한 행이 무엇을 바꿨는지 읽습니다. 연결 리스트는 chain, 트리 노드는 값과 두 자식 값으로 표시합니다. 추적 출력의 복사·표시 비용은 알고리즘의 시간·공간 분석에 포함하지 않습니다.

`student_week_07.py`의 함수와 메서드를 구현한 뒤 `verify.py --student`로 검사합니다. 미구현 상태의 `NotImplementedError`는 해당 함수부터 채우라는 뜻입니다. `--student` 없이 실행하면 제공 풀이를 검사합니다. 특정 풀이의 동작은 `python trace_lab.py --case 함수명 --student`로 대조할 수 있습니다.

각 문제에서 입력·출력의 의미, 상태의 불변식, 한 단계의 변화, 최종 답, 시간·보조 공간·반환값 공간을 기록하세요. 아래 작은 예제 하나의 통과만으로 전체 정당성이 증명되지는 않습니다.

## 이 주의 문제

- [rob](#ko-rob)
- [coin_change](#ko-coin_change)
- [unique_paths](#ko-unique_paths)
- [lcs](#ko-lcs)

## 풀이와 실행 과정

198 | 322 | 62 | 1143

인접한 점검 항목을 함께 선택할 수 없을 때 최대 가치를 구하려면 어떤 정보를 남겨야 할까요? 격자 경로와 두 이벤트 기록의 공통 순서도 작은 부분 문제로 나눌 수 있습니다.

앞에서 계산한 최적값이나 개수를 저장하고 재사용합니다. 상태의 의미에 따라 합·최소·최대 중 연산을 결정합니다.

## DP 상태의 뜻과 계산 순서

동적 계획법은 같은 부분 문제의 답을 저장해 재사용합니다. 먼저 “표 한 칸이 무엇의 답인가”를 정해야 초기값과 전이를 결정할 수 있습니다.

![경로 수와 공통 부분수열 표의 의존 방향](/assets/courses/practical-algorithms/curriculum/dp-dependencies.svg)

| 문제 | 상태의 뜻 | 결합 연산 |
| --- | --- | --- |
| 인접하지 않은 최대 합 | 접두부에서 얻을 수 있는 최대 합 | 선택·건너뛰기의 max |
| 동전 | 금액을 만드는 최소 개수 | 마지막 동전별 min |
| 격자 경로 | 이 칸까지의 경로 수 | 위+왼쪽 |
| 공통 부분수열 | 두 접두부의 최대 공통 길이 | 일치 시 대각선+1, 아니면 max |

시간은 상태 수 × 상태 하나의 계산량으로 셉니다. 공간은 동시에 보관하는 상태 수입니다. 이전 두 상태만 필요한 최대 합은 표를 없앨 수 있지만, 모든 표 구현이 자동으로 O(1) 공간인 것은 아닙니다.

<a id="ko-rob"></a>

## [LeetCode 198: House Robber](https://leetcode.com/problems/house-robber/) · Medium

인접한 위치를 함께 고르지 않고 값의 합을 최대화합니다.

1 <= n <= 100; 값 0..400.

### 구현 전 예측

각 집에서 건너뛴 값 current_best와 선택한 값 best_two_back+value를 비교합니다. 새 최댓값을 구한 뒤 두 상태를 옮깁니다. 접두 구간의 답은 2,7,11,11,12이며 마지막 답은 2+9+1입니다.

```python
rob([2, 7, 9, 3, 1],)
# 12
```

### 풀이 아이디어와 상태 변화

#### 198 · 풀이의 출발점과 실행 추적

[LeetCode 198: House Robber](https://leetcode.com/problems/house-robber/) · Medium

인접한 위치를 함께 고르지 않고 값의 합을 최대화합니다.

현재 값을 고르면 바로 앞 값은 고를 수 없습니다. 따라서 현재 값까지의 최댓값은 “직전까지의 최댓값을 유지”하거나 “두 칸 전까지의 최댓값에 현재 값을 더함” 중 큰 값입니다. 다음 결정에는 이 두 과거 결과만 필요합니다.

`nums=[3,1,4,2]`. old 값으로 오른쪽 식을 모두 계산한 뒤 갱신합니다.

| value | old previous_two | old previous_one | 새 previous_one |
| --- | --- | --- | --- |
| 3 | 0 | 0 | max(0,0+3)=3 |
| 1 | 0 | 3 | max(3,0+1)=3 |
| 4 | 3 | 3 | max(3,3+4)=7 |
| 2 | 3 | 7 | max(7,3+2)=7 |

#### 점화식의 표와 두 변수의 대응

D[i]를 앞의 i개 값에서 얻는 최대 합으로 정의합니다. [3,1,4,2]에서 빈 접두부 D[0]=0입니다.

| i와 현재 값 | 현재 값 제외 | 현재 값 포함 | D[i] |
| --- | --- | --- | --- |
| 1, 값 3 | 0 | 0+3 | 3 |
| 2, 값 1 | D[1]=3 | D[0]+1=1 | 3 |
| 3, 값 4 | D[2]=3 | D[1]+4=7 | 7 |
| 4, 값 2 | D[3]=7 | D[2]+2=5 | 7 |

값 4를 처리하기 직전 previous_two=D[1], previous_one=D[2]입니다. 계산 후에는 각각 D[2],D[3]이 되어 다음 반복의 의미를 유지합니다. 포함 경로에서 D[i−1]을 더하면 바로 앞 값을 함께 고를 수 있어 인접 금지 조건을 깨뜨립니다.

4를 포함하는 경우 이미 고른 앞부분의 최적값 3에 4를 더합니다. 최적값 3을 매번 처음부터 다시 구하지 않는 것이 DP의 재사용입니다.

#### 198 · 정당성·시간·메모리의 근거

최적 선택은 현재 위치를 선택하거나 선택하지 않는 두 경우로 나뉩니다. 두 경우 모두 남은 접두부를 최적으로 풀어야 하므로 점화식이 모든 최적해를 포함합니다.

n개 값마다 덧셈 한 번, max 비교 한 번, 고정 개수 대입을 수행합니다. 숫자 연산을 O(1)로 보는 입력 범위에서 전체 시간은 O(n)입니다. 과거 최댓값은 이미 계산되어 있으므로 같은 접두부를 다시 탐색하지 않습니다.

입력이 커져도 두 최댓값과 현재 값만 보관하므로 보조 공간은 O(1)입니다. 모든 접두부 최댓값을 dp 리스트에 저장하면 O(n) 공간이지만 이 코드는 다음 단계에 필요한 두 값만 남깁니다. 실제 선택 위치 복원에는 추가 기록이 필요합니다.

[2,1,1,2]에서 짝수 위치만 또는 홀수 위치만 합하면 최적 4를 놓칩니다.

`nums=[3,1,4,2] → 7`

### 구현과 실행

```python
from collections import deque
import heapq

def rob(nums):
    previous_two = previous_one = 0
    for value in nums:
        previous_two, previous_one = previous_one, max(previous_one, previous_two + value)
    return previous_one
```

```text
python trace_lab.py --case rob
```

위 예측과 trace의 반환값을 대조하세요. 입력을 앞에서 제안한 대로 바꾸고, 처음으로 상태가 달라지는 행을 찾아 그 변화가 답에 미친 영향을 설명합니다.

<a id="ko-coin_change"></a>

## [LeetCode 322: Coin Change](https://leetcode.com/problems/coin-change/) · Medium

amount를 만드는 최소 동전 수를 반환하고 불가능하면 -1입니다.

1..12개 동전, 값 1..<math xmlns="http://www.w3.org/1998/Math/MathML"><msup><mn>2</mn><mn>31</mn></msup></math>-1; amount 0..<math xmlns="http://www.w3.org/1998/Math/MathML"><msup><mn>10</mn><mn>4</mn></msup></math>; 각 동전 무제한.

### 구현 전 예측

dp[a]를 금액 a의 최소 동전 수로 정의하고 dp[0]=0, 나머지는 도달 불가로 둡니다. 작은 금액부터 채웁니다. 표는 0,1,2,1,1,2,2이며 3+3이 greedy의 4+1+1보다 낫습니다.

```python
coin_change([1, 3, 4], 6)
# 2
```

### 풀이 아이디어와 상태 변화

#### 322 · 풀이의 출발점과 실행 추적

[LeetCode 322: Coin Change](https://leetcode.com/problems/coin-change/) · Medium

amount를 만드는 최소 동전 수를 반환하고 불가능하면 -1입니다.

금액 a를 만드는 마지막 동전이 c라고 정하면, 그 앞에는 a-c를 만드는 최선의 방법이 있어야 합니다. 각 동전을 마지막에 놓는 경우를 모두 비교합니다. 큰 동전부터 고르는 규칙은 `[1,3,4]`로 6을 만들 때 4+1+1을 골라 3+3을 놓칩니다.

`coins=[1,3,4], amount=6`. 표의 값은 해당 total의 모든 coin을 검사한 뒤입니다.

| total | 후보 dp[total-coin]+1 | 확정 dp[total] |
| --- | --- | --- |
| 0 | 동전 없이 가능 | 0 |
| 1,2 | 0+1 / 1+1 | 1,2 |
| 3 | 2+1, 0+1 | 1 |
| 4 | 1+1, 1+1, 0+1 | 1 |
| 5 | 1+1, 2+1, 1+1 | 2 |
| 6 | 2+1, 1+1, 2+1 | 2 |

#### 322 · 정당성·시간·메모리의 근거

최적해의 마지막 동전 c를 제거하면 a-c의 최적해가 남아야 합니다. 모든 가능한 마지막 동전을 비교하므로 최소를 놓치지 않습니다. 양수 동전이라 필요한 상태가 먼저 계산됩니다.

금액 상태 A개마다 동전 m개를 검사하므로 최대 A·m번의 전이가 있습니다. 각 전이는 리스트 접근·덧셈·비교이므로 O(1), 전체 시간은 O(Am)입니다. 바깥 범위가 동전 수가 아니라 목표 금액의 값 A라는 점에 주의합니다.

dp는 0부터 A까지 A+1칸이고 나머지 변수는 고정 개수라서 보조 공간 O(A)입니다. A를 입력에 쓰는 비트 수는 log A이므로 O(Am)은 그 비트 길이에 대해서는 의사다항 시간입니다. 입력 동전 목록은 보조 공간에 다시 세지 않습니다.

큰 동전 우선은 [1,3,4], 6에서 4+1+1을 골라 실패합니다. [2],3은 -1이고 amount=0은 0입니다.

`coins=[1,3,4], amount=6 → 2`

### 구현과 실행

```python
from collections import deque
import heapq

def coin_change(coins, amount):
    dp = [float("inf")] * (amount + 1)
    dp[0] = 0
    for total in range(1, amount + 1):
        for coin in coins:
            if coin <= total:
                dp[total] = min(dp[total], dp[total - coin] + 1)
    return -1 if dp[amount] == float("inf") else dp[amount]
```

```text
python trace_lab.py --case coin_change
```

위 예측과 trace의 반환값을 대조하세요. 입력을 앞에서 제안한 대로 바꾸고, 처음으로 상태가 달라지는 행을 찾아 그 변화가 답에 미친 영향을 설명합니다.

<a id="ko-unique_paths"></a>

## [LeetCode 62: Unique Paths](https://leetcode.com/problems/unique-paths/) · Medium

격자에서 오른쪽·아래로만 이동하는 경로 수를 반환합니다.

1 <= R,C <= 100; 답 <= 2×<math xmlns="http://www.w3.org/1998/Math/MathML"><msup><mn>10</mn><mn>9</mn></msup></math>인 입력.

### 구현 전 예측

한 칸으로는 위와 왼쪽에서 들어옵니다. 한 행 버퍼에서 dp[col]은 아직 위쪽 값이고 dp[col-1]은 갱신된 왼쪽 값입니다. 행은 [1,1,1,1], [1,2,3,4], [1,3,6,10]으로 바뀝니다.

```python
unique_paths(3, 4)
# 10
```

### 풀이 아이디어와 상태 변화

#### 62 · 풀이의 출발점과 실행 추적

[LeetCode 62: Unique Paths](https://leetcode.com/problems/unique-paths/) · Medium

격자에서 오른쪽·아래로만 이동하는 경로 수를 반환합니다.

오른쪽·아래로만 이동할 때 현재 칸에 도착하는 마지막 이동은 위에서 내려오거나 왼쪽에서 오는 경우뿐입니다. 두 경우는 마지막 이동이 달라 서로 겹치지 않으므로 경로 수를 더합니다. 최댓값을 고르는 문제가 아닙니다.

rows=3, cols=3. 첫 행·열은 한 방향으로만 올 수 있어 1입니다.

| 처리한 칸 | 계산 | 현재 dp의 행들 |
| --- | --- | --- |
| 초기화 | 경계값 1 | [1,1,1] / [1,1,1] / [1,1,1] |
| (1,1) | 1+1=2 | [1,1,1] / [1,2,1] / [1,1,1] |
| (1,2) | 1+2=3 | [1,1,1] / [1,2,3] / [1,1,1] |
| (2,1) | 2+1=3 | [1,1,1] / [1,2,3] / [1,3,1] |
| (2,2) | 3+3=6 | [1,1,1] / [1,2,3] / [1,3,6] |

#### 62 · 정당성·시간·메모리의 근거

각 경로의 마지막 이동은 아래 또는 오른쪽 하나입니다. 두 집합은 겹치지 않고 전체 경로를 덮으므로 수를 더합니다. 행 순서로 필요한 선행 상태가 준비됩니다.

초기화에 R·C칸, 전이에 (R-1)(C-1)칸을 처리합니다. 각 칸에서 두 값 조회와 덧셈 한 번을 수행하므로 시간 O(RC)입니다. 경로를 직접 하나씩 나열하지 않아 답의 개수만큼 반복하지 않습니다.

전체 dp 표를 보관하므로 보조 공간 O(RC)입니다. 이 구현의 공간을 한 행만 저장하는 최적화의 O(C)와 혼동하면 안 됩니다. 공식 입력의 답 범위에서는 정수 연산을 상수 비용으로 보며, 제한 없는 큰 격자에서는 큰 정수의 비트 비용도 증가합니다.

`[[1]*C]*R`은 같은 행을 공유합니다. `[[1]*C for _ in range(R)]`로 만듭니다.

`rows=2, cols=4 → 4`

### 구현과 실행

```python
from collections import deque
import heapq

def unique_paths(rows, cols):
    dp = [[1] * cols for _ in range(rows)]
    for r in range(1, rows):
        for c in range(1, cols):
            dp[r][c] = dp[r-1][c] + dp[r][c-1]
    return dp[-1][-1]
```

```text
python trace_lab.py --case unique_paths
```

위 예측과 trace의 반환값을 대조하세요. 입력을 앞에서 제안한 대로 바꾸고, 처음으로 상태가 달라지는 행을 찾아 그 변화가 답에 미친 영향을 설명합니다.

<a id="ko-lcs"></a>

## [LeetCode 1143: Longest Common Subsequence](https://leetcode.com/problems/longest-common-subsequence/) · Medium

두 문자열에서 순서를 보존하는 공통 부분수열의 최대 길이를 반환합니다.

각 문자열 길이 1..1000; 소문자 영문자.

### 구현 전 예측

두 접두 문자열의 답을 dp[i][j]로 정의합니다. 끝 문자가 같으면 대각선 값에 1을 더하고, 다르면 한쪽 끝 문자를 뺀 두 값 중 큰 것을 택합니다. a,c,e가 답을 늘리는 칸을 표시하세요.

```python
lcs('abcde', 'ace')
# 3
```

### 풀이 아이디어와 상태 변화

#### 1143 · 풀이의 출발점과 실행 추적

[LeetCode 1143: Longest Common Subsequence](https://leetcode.com/problems/longest-common-subsequence/) · Medium

두 문자열에서 순서를 보존하는 공통 부분수열의 최대 길이를 반환합니다.

두 문자열의 앞부분끼리 비교하는 답을 표에 저장합니다. 마지막 문자가 같으면 두 문자를 함께 사용하여 더 짧은 두 접두부의 답에 1을 더합니다. 다르면 둘을 서로 짝지을 수 없으므로 한쪽 끝을 제외하는 두 경우 중 큰 값을 택합니다.

`first="abc", second="ac"`. 행은 첫 문자열 접두부, 열은 두 번째 접두부입니다.

| 행 계산 완료 | 빈 접두부 | a | ac |
| --- | --- | --- | --- |
| 빈 접두부 | 0 | 0 | 0 |
| a | 0 | 1 (=0+1) | 1 (=max(0,1)) |
| ab | 0 | 1 (=max(1,0)) | 1 (=max(1,1)) |
| abc | 0 | 1 (=max(1,0)) | 2 (=1+1) |

답 2는 `ac`의 길이입니다. b를 건너뛰므로 연속 부분문자열과 다릅니다.

#### 1143 · 정당성·시간·메모리의 근거

끝 문자가 같으면 두 끝을 맞춘 최적 부분수열을 택할 수 있습니다. 다르면 둘을 동시에 마지막으로 맞출 수 없어 적어도 한쪽을 생략해야 합니다. 두 경우의 최댓값을 취합니다.

길이가 n, m인 문자열에는 (n+1)(m+1)개 접두부 쌍이 있습니다. 각 내부 칸은 문자 비교와 최대 한 번의 덧셈 또는 max로 계산하므로 O(nm) 시간입니다. n과 m이 같은 크기일 때만 이를 O(<math xmlns="http://www.w3.org/1998/Math/MathML"><msup><mi>n</mi><mn>2</mn></msup></math>)로 쓸 수 있습니다.

표 전체가 (n+1)(m+1)칸이므로 보조 공간 O(nm)입니다. 문자열 길이를 반환하는 한 정수는 O(1) 출력입니다. 실제 공통 부분수열을 복원하려면 표를 역추적하고 별도 출력 문자를 저장해야 합니다.

부분수열은 문자의 순서를 유지하면서 중간 문자를 건너뛸 수 있습니다. "abc"에서 b를 건너뛰면 "ac"가 되므로 공통 부분수열의 길이는 2입니다.

`first="abca", second="aca" → 3`

끝 문자가 모두 c라면 어떤 최적 부분수열도 마지막 c들을 짝지은 형태로 바꿀 수 있습니다. c를 사용하지 않는 더 짧은 양쪽 접두부의 해에는 c를 붙일 수 있고, 한쪽의 더 이른 c를 사용했다면 그 짝을 마지막 c로 옮겨도 순서가 유지됩니다. 그래서 일치할 때는 대각선 답+1만으로 충분합니다.

### 구현과 실행

```python
from collections import deque
import heapq

def lcs(first, second):
    rows, cols = len(first), len(second)
    dp = [[0] * (cols + 1) for _ in range(rows + 1)]
    for r in range(1, rows + 1):
        for c in range(1, cols + 1):
            if first[r-1] == second[c-1]:
                dp[r][c] = dp[r-1][c-1] + 1
            else:
                dp[r][c] = max(dp[r-1][c], dp[r][c-1])
    return dp[rows][cols]
```

```text
python trace_lab.py --case lcs
```

위 예측과 trace의 반환값을 대조하세요. 입력을 앞에서 제안한 대로 바꾸고, 처음으로 상태가 달라지는 행을 찾아 그 변화가 답에 미친 영향을 설명합니다.

## 실습 보고서

작은 입력의 상태표, 완성 코드, 직접 만든 경계 입력과 예상값, 검증 결과를 함께 기록합니다. 시간 복잡도는 총 연산 횟수로, 공간 복잡도는 동시에 살아 있는 상태로 설명하세요. 입력을 복사하거나 정렬한다면 그 비용도 포함합니다.
