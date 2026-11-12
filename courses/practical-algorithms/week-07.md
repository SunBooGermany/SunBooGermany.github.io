---
layout: "course-note"
title: "Week 7: One- and two-dimensional DP"
title_ko: "7주차: 1차원·2차원 동적 계획법"
course_id: "practical-algorithms"
permalink: "/courses/practical-algorithms/week-07/"
updated: "2026-11-12"
material_label: "Week 7 lecture"
material_label_ko: "7주차 강의"
pdf_en: "/assets/courses/practical-algorithms/week-07-en.pdf"
pdf_ko: "/assets/courses/practical-algorithms/week-07-ko.pdf"
reading_note: "/courses/practical-algorithms/week-07-reading/"
lab_bundle: "/assets/courses/practical-algorithms/week-07-code.zip"
practice_note: "/courses/practical-algorithms/week-07-practice/"
reading_pdf_en: "/assets/courses/practical-algorithms/week-07-reading-en.pdf"
reading_pdf_ko: "/assets/courses/practical-algorithms/week-07-reading-ko.pdf"
---

## Repeated subproblem calculations

What information is needed to maximize inspection value when adjacent items cannot both be selected? Grid paths and common order in two event logs can also be divided into smaller problems.

Store and reuse previously computed optima or counts. The meaning of the state determines whether to add, minimize, or maximize.

<!-- lecture-page -->

## Week 7 learning outcomes

Sessions 13 and 14: State meaning, base cases, recurrences, and evaluation order

- Check contracts and boundary conditions.
- Trace state and implement in Python.
- Explain correctness, time, auxiliary space, and output space.

Opening scenarios, traces, and checks are additional teaching examples.

<!-- lecture-page -->

## Session 13 · Optimal subproblems and one-dimensional DP

Replace repeated prefix or amount computations with states. Define the optimization objective before assigning meanings to table entries.

<!-- lecture-page -->

## Prerequisites and Python semantics

`float("inf")` represents unreachable minimization states. Tuple assignment evaluates the right side using old values; preserve both predecessor states.

<!-- lecture-page -->

## Before allocating a DP table

- State: which answer for which part of the input?
- Base cases: empty input, amount zero, first row/column
- Recurrence: split cases by the final choice
- Evaluation order: compute dependencies first

Filling coin amounts downward reads smaller states before computing them. Positive coins permit increasing-amount evaluation.

<!-- lecture-page -->

## 198 · Problem and state

[LeetCode 198: House Robber](https://leetcode.com/problems/house-robber/) · Medium

Maximize selected value without selecting adjacent positions.

`nums=[3,1,4,2] → 7`

D[i] is the best prefix of length i. D[0]=0, D[1]=nums[0]; for i>=2, D[i]=max(D[i-1],D[i-2]+nums[i-1]). The code starts both rolling states at zero and applies the update from the first value.

<!-- lecture-page -->

## 198 · Implementation

```python
def rob(nums):
    previous_two = previous_one = 0
    for value in nums:
        previous_two, previous_one = previous_one, max(previous_one, previous_two + value)
    return previous_one
```

<!-- lecture-page -->

## 198 · Correctness and cost

Every optimum either selects the current item or skips it. Each case leaves an optimal prefix, so the recurrence covers all optima.

n is length. O(n) time, O(1) auxiliary space. Reconstructing selected indices needs additional state.

<!-- lecture-page -->

## 322 · Problem and state

[LeetCode 322: Coin Change](https://leetcode.com/problems/coin-change/) · Medium

Return the minimum coin count for amount, or -1 if impossible.

`coins=[1,3,4], amount=6 → 2`

Set dp[0]=0 and other states to infinity; fill increasing amounts using min(dp[a-c]+1).

<!-- lecture-page -->

## 322 · Implementation

```python
def coin_change(coins, amount):
    dp = [float("inf")] * (amount + 1)
    dp[0] = 0
    for total in range(1, amount + 1):
        for coin in coins:
            if coin <= total:
                dp[total] = min(dp[total], dp[total - coin] + 1)
    return -1 if dp[amount] == float("inf") else dp[amount]
```

<!-- lecture-page -->

## 322 · Correctness and cost

Removing the last coin c from an optimum leaves an optimum for a-c. Comparing all final coins finds the minimum; positive values ensure dependencies were filled earlier.

A is amount,m coin types. O(Am) time,O(A) space; pseudopolynomial in the bit length of A.

<!-- lecture-page -->

## State trace

| a | 0 | 1 | 2 | 3 | 4 | 5 | 6 |
| --- | --- | --- | --- | --- | --- | --- | --- |
| dp[a],coins=1,3,4 | 0 | 1 | 2 | 1 | 1 | 2 | 2 |

Each amount uses already-computed smaller amounts.

<!-- lecture-page -->

## Failure inputs and concept checks

Summing only even or only odd positions misses optimum 4 for [2,1,1,2].

Why add one to dp[a-c]?

The instructor answer is in the separate guide. Compare the reasoning line by line with the companion implementation.

<!-- lecture-page -->

## Session 14 · Grid and prefix-string DP

Count grid paths and compare event sequences. A table shape does not determine whether transitions should sum or maximize.

<!-- lecture-page -->

## Prerequisites and Python semantics

Allocate independent rows with a comprehension. A prefix of length i ends at first[i-1]; reserve row/column zero for empty prefixes.

<!-- lecture-page -->

## 62 · Problem and state

[LeetCode 62: Unique Paths](https://leetcode.com/problems/unique-paths/) · Medium

Count grid paths using only right and down moves.

`rows=2, cols=4 → 4`

Initialize first row/column to 1, add top and left counts, and allocate each row independently.

<!-- lecture-page -->

## 62 · Implementation

```python
def unique_paths(rows, cols):
    dp = [[1] * cols for _ in range(rows)]
    for r in range(1, rows):
        for c in range(1, cols):
            dp[r][c] = dp[r-1][c] + dp[r][c-1]
    return dp[-1][-1]
```

<!-- lecture-page -->

## 62 · Correctness and cost

Every path arrives from top or left. These disjoint classes cover all paths, so counts add; row order respects dependencies.

R,C are dimensions. O(RC) time/space under the bounded-answer model; arbitrary-size integer bit costs are separate.

<!-- lecture-page -->

## 1143 · Problem and state

[LeetCode 1143: Longest Common Subsequence](https://leetcode.com/problems/longest-common-subsequence/) · Medium

Return the length of a longest common subsequence preserving order.

`first="abca", second="aca" → 3`

Equal final characters give diagonal+1; otherwise take max(top,left); empty prefixes give zero.

<!-- lecture-page -->

## 1143 · Implementation

```python
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

<!-- lecture-page -->

## 1143 · Correctness and cost

Equal final characters can be paired in an optimum. Unequal ends cannot both be the final match, so at least one is skipped; maximize over both cases.

n,m are string lengths. O(nm) time/space; this returns length, not a reconstructed sequence.

<!-- lecture-page -->

## State trace

| LCS("ab","ac") | empty prefix | a | c |
| --- | --- | --- | --- |
| empty prefix | 0 | 0 | 0 |
| a | 0 | 1 | 1 |
| ab | 0 | 1 | 1 |

Rows and columns denote prefix lengths, including zero.

<!-- lecture-page -->

## Failure inputs and concept checks

`[[1]*C]*R` aliases rows; use a comprehension creating each row.

Why add rather than maximize when counting paths?

The instructor answer is in the separate guide. Compare the reasoning line by line with the companion implementation.

<!-- lecture-page -->

## Preserving two previous optima

| Current value | Old prev_two | Old prev_one | New optimum |
| --- | --- | --- | --- |
| 3 | 0 | 0 | 3 |
| 1 | 0 | 3 | 3 |
| 4 | 3 | 3 | 7 |
| 2 | 3 | 7 | 7 |

Every right-hand expression uses the old state. Selecting the current value skips the immediately preceding position.

<!-- lecture-page -->

## Checkpoint questions

1. Find the maximum nonadjacent sum for `[2,1,1,2]`.
2. Find the minimum coins for amount 6 using `[1,3,4]`.
3. Count paths in 1×4 and 2×4 grids.
4. Find the LCS length of `abc` and `ac`. Must the characters be contiguous?

<!-- lecture-page -->

## Independent practice and connections

[Student exercises](/courses/practical-algorithms/week-07-practice/)

[Hints and solutions](/courses/practical-algorithms/week-07-reading/)

[Instructor guide](/courses/practical-algorithms/week-07-instructor/)

[Download Week 7 code](/assets/courses/practical-algorithms/week-07-code.zip)

Submit code, state definition, correctness argument, complexity, and boundary inputs. Week 8 includes a mixed assessment without pattern labels.

<!-- lecture-page -->

## Execution and sources

Run in the `code` folder of the [weekly code archive](/assets/courses/practical-algorithms/week-07-code.zip).

```text
python demo_13.py
python demo_14.py
python verify.py
python verify.py --student
```

Use the last command after implementing the student file.

Erik Demaine and Srini Devadas, [MIT 6.006: Introduction to Algorithms](https://ocw.mit.edu/courses/6-006-introduction-to-algorithms-fall-2011/) (2011).

<!-- ko -->

## 같은 부분 문제의 반복 계산

인접한 점검 항목을 함께 선택할 수 없을 때 최대 가치를 구하려면 어떤 정보를 남겨야 할까요? 격자 경로와 두 이벤트 기록의 공통 순서도 작은 부분 문제로 나눌 수 있습니다.

앞에서 계산한 최적값이나 개수를 저장하고 재사용합니다. 상태의 의미에 따라 합·최소·최대 중 연산을 결정합니다.

<!-- lecture-page -->

## 7주차 학습 목표

13·14차시: 상태 의미·초기값·점화식·계산 순서

- 입력 계약과 경계 조건 확인
- 상태 추적과 Python 구현
- 정당성·시간·보조 공간·출력 공간 설명

도입 상황, 표와 점검 문제는 강의용 추가 예시입니다.

<!-- lecture-page -->

## 13차시 · 최적 부분 문제와 1차원 DP

같은 접두부·금액을 반복 계산하는 탐색을 상태 표로 바꿉니다. 무엇을 최대화하거나 최소화하는지 먼저 적어 값의 의미를 고정합니다.

<!-- lecture-page -->

## 선수 지식과 Python 문법

`float("inf")`는 불가능한 최소화 상태를 나타냅니다. tuple 동시 대입은 오른쪽을 이전 값으로 계산합니다. 덮어쓰기 전에 필요한 이전 두 상태를 보존합니다.

<!-- lecture-page -->

## DP 표를 만들기 전의 정의

- 상태: 어떤 입력 범위의 어떤 답인가?
- 초기값: 빈 입력·금액 0·첫 행과 열
- 점화식: 마지막 선택으로 경우 분할
- 계산 순서: 필요한 이전 상태부터

동전 금액을 큰 값부터 계산하면 아직 구하지 않은 작은 금액을 읽게 됩니다. 양수 동전은 작은 금액부터의 계산을 가능하게 합니다.

<!-- lecture-page -->

## 198 · 문제와 상태

[LeetCode 198: House Robber](https://leetcode.com/problems/house-robber/) · Medium

인접한 위치를 함께 고르지 않고 값의 합을 최대화합니다.

`nums=[3,1,4,2] → 7`

D[i]는 앞 i개 최댓값입니다. D[0]=0, D[1]=nums[0]이며 i>=2에서 D[i]=max(D[i-1],D[i-2]+nums[i-1])입니다. 코드에서는 이전 두 상태를 0으로 시작해 첫 값부터 같은 갱신을 적용합니다.

<!-- lecture-page -->

## 198 · 구현

```python
def rob(nums):
    previous_two = previous_one = 0
    for value in nums:
        previous_two, previous_one = previous_one, max(previous_one, previous_two + value)
    return previous_one
```

<!-- lecture-page -->

## 198 · 정당성과 비용

최적 선택은 현재 위치를 선택하거나 선택하지 않는 두 경우로 나뉩니다. 두 경우 모두 남은 접두부를 최적으로 풀어야 하므로 점화식이 모든 최적해를 포함합니다.

n=길이. O(n) 시간, O(1) 보조 공간. 선택 위치 복원은 별도 상태가 필요합니다.

<!-- lecture-page -->

## 322 · 문제와 상태

[LeetCode 322: Coin Change](https://leetcode.com/problems/coin-change/) · Medium

amount를 만드는 최소 동전 수를 반환하고 불가능하면 -1입니다.

`coins=[1,3,4], amount=6 → 2`

dp[0]=0, 나머지는 inf입니다. 작은 금액부터 dp[a-c]+1 중 최소를 취합니다.

<!-- lecture-page -->

## 322 · 구현

```python
def coin_change(coins, amount):
    dp = [float("inf")] * (amount + 1)
    dp[0] = 0
    for total in range(1, amount + 1):
        for coin in coins:
            if coin <= total:
                dp[total] = min(dp[total], dp[total - coin] + 1)
    return -1 if dp[amount] == float("inf") else dp[amount]
```

<!-- lecture-page -->

## 322 · 정당성과 비용

최적해의 마지막 동전 c를 제거하면 a-c의 최적해가 남아야 합니다. 모든 가능한 마지막 동전을 비교하므로 최소를 놓치지 않습니다. 양수 동전이라 필요한 상태가 먼저 계산됩니다.

A=amount,m=종류 수. O(Am) 시간·O(A) 보조 공간. A의 비트 길이에 대해서는 의사다항 시간입니다.

<!-- lecture-page -->

## 상태 추적

| a | 0 | 1 | 2 | 3 | 4 | 5 | 6 |
| --- | --- | --- | --- | --- | --- | --- | --- |
| dp[a],coins=1,3,4 | 0 | 1 | 2 | 1 | 1 | 2 | 2 |

각 금액은 먼저 계산한 작은 금액의 상태를 사용합니다.

<!-- lecture-page -->

## 실패 입력과 이해 확인

[2,1,1,2]에서 짝수 위치만 또는 홀수 위치만 합하면 최적 4를 놓칩니다.

dp[a-c]에 왜 1을 더하나요?

교사용 답은 별도 진행안에 있습니다. 코드 설명은 읽기자료의 구현과 줄별로 대조합니다.

<!-- lecture-page -->

## 14차시 · 격자와 접두 문자열 DP

격자 경로의 개수와 두 이벤트 문자열의 공통 순서를 구합니다. 같은 표 형태라도 합산과 최댓값의 의미를 구분해 점화식을 설계합니다.

<!-- lecture-page -->

## 선수 지식과 Python 문법

[[0]*(m+1) for _ in range(n+1)]는 독립 행입니다. 길이 i인 접두부의 마지막 문자는 first[i-1]입니다. 빈 접두부를 위한 0행·0열을 둡니다.

<!-- lecture-page -->

## 62 · 문제와 상태

[LeetCode 62: Unique Paths](https://leetcode.com/problems/unique-paths/) · Medium

격자에서 오른쪽·아래로만 이동하는 경로 수를 반환합니다.

`rows=2, cols=4 → 4`

첫 행·열은 1이고 내부는 위쪽 수+왼쪽 수입니다. 행마다 새 list를 만듭니다.

<!-- lecture-page -->

## 62 · 구현

```python
def unique_paths(rows, cols):
    dp = [[1] * cols for _ in range(rows)]
    for r in range(1, rows):
        for c in range(1, cols):
            dp[r][c] = dp[r-1][c] + dp[r][c-1]
    return dp[-1][-1]
```

<!-- lecture-page -->

## 62 · 정당성과 비용

각 경로의 마지막 이동은 아래 또는 오른쪽 하나입니다. 두 집합은 겹치지 않고 전체 경로를 덮으므로 수를 더합니다. 행 순서로 필요한 선행 상태가 준비됩니다.

R,C=행·열 수. O(RC) 시간·O(RC) 보조 공간. 큰 정수의 비트 비용은 별도이며 공식 답 범위에서는 작습니다.

<!-- lecture-page -->

## 1143 · 문제와 상태

[LeetCode 1143: Longest Common Subsequence](https://leetcode.com/problems/longest-common-subsequence/) · Medium

두 문자열에서 순서를 보존하는 공통 부분수열의 최대 길이를 반환합니다.

`first="abca", second="aca" → 3`

같으면 대각선+1, 다르면 위·왼쪽 중 최대입니다. 길이 0 접두부의 행·열은 0입니다.

<!-- lecture-page -->

## 1143 · 구현

```python
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

<!-- lecture-page -->

## 1143 · 정당성과 비용

끝 문자가 같으면 두 끝을 맞춘 최적 부분수열을 택할 수 있습니다. 다르면 둘을 동시에 마지막으로 맞출 수 없어 적어도 한쪽을 생략해야 합니다. 두 경우의 최댓값을 취합니다.

n,m=문자열 길이. O(nm) 시간·O(nm) 보조 공간. 길이만 반환하며 문자열 복원은 별도입니다.

<!-- lecture-page -->

## 상태 추적

| LCS("ab","ac") | 빈 접두부 | a | c |
| --- | --- | --- | --- |
| 빈 접두부 | 0 | 0 | 0 |
| a | 0 | 1 | 1 |
| ab | 0 | 1 | 1 |

행과 열은 0을 포함한 접두부 길이입니다.

<!-- lecture-page -->

## 실패 입력과 이해 확인

`[[1]*C]*R`은 같은 행을 공유합니다. `[[1]*C for _ in range(R)]`로 만듭니다.

경로 수에서는 왜 max가 아니라 +인가요?

교사용 답은 별도 진행안에 있습니다. 코드 설명은 읽기자료의 구현과 줄별로 대조합니다.

<!-- lecture-page -->

## 이전 두 최적값의 보존

| 현재 값 | 갱신 전 prev_two | 갱신 전 prev_one | 새 최적값 |
| --- | --- | --- | --- |
| 3 | 0 | 0 | 3 |
| 1 | 0 | 3 | 3 |
| 4 | 3 | 3 | 7 |
| 2 | 3 | 7 | 7 |

오른쪽 식은 모두 갱신 전 값을 사용합니다. 현재 값을 선택하면 바로 앞 위치는 건너뜁니다.

<!-- lecture-page -->

## 중간 점검

1. `[2,1,1,2]`의 인접하지 않은 최대 합은?
2. 동전 `[1,3,4]`로 6을 만드는 최소 개수는?
3. 1×4와 2×4 격자의 경로 수는?
4. `abc`, `ac`의 LCS 길이는? 연속해야 하나요?

<!-- lecture-page -->

## 독립 실습과 다음 연결

[학생 실습](/courses/practical-algorithms/week-07-practice/)

[힌트·해설](/courses/practical-algorithms/week-07-reading/)

[교사용 진행안](/courses/practical-algorithms/week-07-instructor/)

[7주차 코드 내려받기](/assets/courses/practical-algorithms/week-07-code.zip)

코드·상태 정의·정당성·복잡도·경계 입력을 함께 제출합니다. 8주차에는 주제를 숨긴 혼합 평가가 있습니다.

<!-- lecture-page -->

## 실행과 참고자료

[주차별 코드](/assets/courses/practical-algorithms/week-07-code.zip)의 `code` 폴더에서 실행합니다.

```text
python demo_13.py
python demo_14.py
python verify.py
python verify.py --student
```

마지막 명령은 학생 파일을 구현한 뒤 실행합니다.

Erik Demaine·Srini Devadas, [MIT 6.006: Introduction to Algorithms](https://ocw.mit.edu/courses/6-006-introduction-to-algorithms-fall-2011/) (2011).
