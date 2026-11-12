---
layout: "course-note"
title: "Week 1 Worked Companion"
title_ko: "1주차 풀이 읽기자료"
course_id: "practical-algorithms"
permalink: "/courses/practical-algorithms/week-01-reading/"
updated: "2026-11-12"
material_label: "Week 1 reading"
material_label_ko: "1주차 읽기자료"
pdf_en: "/assets/courses/practical-algorithms/week-01-reading-en.pdf"
pdf_ko: "/assets/courses/practical-algorithms/week-01-reading-ko.pdf"
lecture_note: "/courses/practical-algorithms/week-01/"
practice_note: "/courses/practical-algorithms/week-01-practice/"
---

## Operation costs and worked solutions

Removing every element can have different total costs depending on the operation. Repeated removal from the front of a list shifts n-1, n-2, …, 0 references.

| Repeated operation | One operation | Count or total shifts | Total |
| --- | --- | --- | --- |
| list pop from end | Amortized O(1) | n calls | O(n) |
| list pop(0) | Current length | n(n-1)/2 shifts | O(<math xmlns="http://www.w3.org/1998/Math/MathML"><msup><mi>n</mi><mn>2</mn></msup></math>) |
| deque popleft | O(1) | n calls | O(n) |
| Search earlier list per value | Up to O(n) | n calls | O(<math xmlns="http://www.w3.org/1998/Math/MathML"><msup><mi>n</mi><mn>2</mn></msup></math>) |
| dict key lookup per value | Expected O(1) | n calls | Expected O(n) |

Summing n values while retaining only a running sum takes O(n) time and O(1) auxiliary space. Count iterations and retained storage separately.

<!-- lecture-page -->

## 1 · Staged hints

[LeetCode 1: Two Sum](https://leetcode.com/problems/two-sum/) · Easy

H1. Which value would complete the current value?

H2. When should an index be recorded to avoid using it twice?

H3. Store earlier value-to-index pairs; look up target-value before recording the current value.

`nums=[4,8,3], target=7`

| index | value | Needed | seen before lookup | Result |
| --- | --- | --- | --- | --- |
| 0 | 4 | 3 | {} | Absent → record 4:0 |
| 1 | 8 | -1 | {4:0} | Absent → record 8:1 |
| 2 | 3 | 4 | {4:0,8:1} | Found → [0,2] |

<!-- lecture-page -->

## 1 · Correctness and cost

At loop entry, the map contains only earlier positions. At the later position of the unique answer, its partner is present. This reuses information instead of checking all O(<math xmlns="http://www.w3.org/1998/Math/MathML"><msup><mi>n</mi><mn>2</mn></msup></math>) pairs.

Each element performs a fixed number of dictionary operations. Expected O(1) operations repeated n times give expected O(n) time. Up to n distinct value-position entries use O(n) auxiliary space; two returned indices use O(1). Severe hash collisions give an O(<math xmlns="http://www.w3.org/1998/Math/MathML"><msup><mi>n</mi><mn>2</mn></msup></math>) worst-case upper bound.

### 1 · Counterexamples and checks

Recording first can reuse one index on [3,3], target=6.

`nums=[4,8,3], target=7 → [0,2]`

<!-- lecture-page -->

## 1 · Implementation 1/1



```python
def two_sum(nums, target):
    seen = {}
    for index, value in enumerate(nums):
        if target - value in seen:
            return [seen[target - value], index]
        seen[value] = index
    return []  # Defensive extension: official inputs have one answer.
```

Each iteration looks up the complement `target-value`. Store the current value only after an unsuccessful lookup, preventing reuse of the current position. With `[4,8,3]`, reading 3 finds 4:0 and recovers index 0.

<!-- lecture-page -->

## 219 · Staged hints

[LeetCode 219: Contains Duplicate II](https://leetcode.com/problems/contains-duplicate-ii/) · Easy

H1. Which occurrence of a value should be retained?

H2. Can an older occurrence be closer than the latest one?

H3. Retain the latest index per value; compare distance, then update.

`nums=[4,7,4,4], k=1`

| index | value | Prior latest[value] | Distance | Action |
| --- | --- | --- | --- | --- |
| 0 | 4 | Absent | - | Store 4:0 |
| 1 | 7 | Absent | - | Store 7:1 |
| 2 | 4 | 0 | 2 > 1 | Fail, update to 4:2 |
| 3 | 4 | 2 | 1 <= 1 | Return True |

<!-- lecture-page -->

## 219 · Correctness and cost

The latest occurrence minimizes distance to the current index. If it is too far, all older occurrences are too far. Updating preserves this property.

One lookup, distance comparison, and update per value give expected O(n) time. There are d entries for d distinct values, so auxiliary space is O(d), d<=n. Even with k=1, all-distinct input leaves n keys; this implementation is not O(k)-space.

### 219 · Counterexamples and checks

Keeping only the first position misses the last pair in [4,7,4,4], k=1. No distinct-index pair qualifies when k=0.

`nums=[4,7,4,4], k=1 → True`

<!-- lecture-page -->

## 219 · Implementation 1/1



```python
def nearby_duplicate(nums, k):
    latest = {}
    for index, value in enumerate(nums):
        if value in latest and index - latest[value] <= k:
            return True
        latest[value] = index
    return False
```

latest stores the most recent position for each value. Update it even after a failed distance check so the next occurrence uses its nearest predecessor. Only one position per distinct value is stored, although old keys are never deleted.

<!-- lecture-page -->

## 167 · Staged hints

[LeetCode 167: Two Sum II - Input Array Is Sorted](https://leetcode.com/problems/two-sum-ii-input-array-is-sorted/) · Medium

H1. If the endpoint sum is too small, which candidates are all too small?

H2. Does the elimination remain valid without sorting?

H3. While left<right, move left inward for a small sum and right inward for a large sum.

`nums=[1,4,6,9], target=7`

| Current pair | Sum | Decision for target=7 | Removed candidates |
| --- | --- | --- | --- |
| 1,9 | 10 | Too large | 9 paired with 1,4,6 |
| 1,6 | 7 | Answer | No further elimination |

<!-- lecture-page -->

## 167 · Correctness and cost

If the sum is small, no partner at or below right works with left. If large, no partner at or above left works with right. Each elimination preserves any answer.

The initial gap right-left is n-1 and decreases by at least one per iteration, giving O(n) comparisons. Two pointers and a sum use O(1) auxiliary space; the two returned positions use O(1). No copy or sorting step is present.

### 167 · Counterexamples and checks

Outside the sorted contract, [3,1,4], target=5 defeats this rule. left==right reuses one element.

`numbers=[1,4,6,9], target=10 → [1,4]`

<!-- lecture-page -->

## 167 · Implementation 1/1



```python
def two_sum_sorted(numbers, target):
    left, right = 0, len(numbers) - 1
    while left < right:
        total = numbers[left] + numbers[right]
        if total == target:
            return [left + 1, right + 1]
        if total < target:
            left += 1
        else:
            right -= 1
    return []
```

When the sum is too small, every pair using the current left value is too small; advance left. When it is too large, discard the right value. Each move narrows the remaining candidates without revisiting discarded pairs.

<!-- lecture-page -->

## 15 · Staged hints

[LeetCode 15: 3Sum](https://leetcode.com/problems/3sum/) · Medium

H1. What remains after fixing one value?

H2. Does fixing the same value again create a new triplet?

H3. Sort a copy, fix the first value, and use two pointers on the suffix; skip repeated fixed values and matched pair values.

`nums=[-2,0,1,1,2]`

| index,left,right | Values | Sum | Action |
| --- | --- | --- | --- |
| 0,1,4 | -2,0,2 | 0 | Store [-2,0,2]; move both |
| 0,2,3 | -2,1,1 | 0 | Store [-2,1,1]; move both |
| 0,3,2 | Interval ended | - | Finish fixed value -2 |

<!-- lecture-page -->

## 15 · Correctness and cost

Every ordered triplet is examined when its smallest value is fixed. Sorted elimination is valid; skipping duplicates removes repeated value combinations only.

There are at most n fixed positions, each with O(n) total pointer movement: O(<math xmlns="http://www.w3.org/1998/Math/MathML"><msup><mi>n</mi><mn>2</mn></msup></math>) time. Duplicate-skipping loops are part of those same movements, not another factor of n. O(n log n) sorting is dominated. Copy/sort workspace is O(n), separate from O(z) space for z output triplets.

### 15 · Counterexamples and checks

[0,0,0,0] yields one triplet. Equal values at distinct positions remain allowed.

`nums=[-2,0,1,1,2] → [[-2,0,2],[-2,1,1]]`

<!-- lecture-page -->

## 15 · Implementation 1/2



```python
def three_sum(nums):
    values = sorted(nums)
    result = []
    for index in range(len(values) - 2):
        if index and values[index] == values[index - 1]:
            continue
        left, right = index + 1, len(values) - 1
        while left < right:
            total = values[index] + values[left] + values[right]
            if total < 0:
                left += 1
```

For each fixed value, restart two pointers in the suffix. Skip repeated fixed values and, after recording a match, repeated values at both ends to avoid duplicate value combinations. Equal values at distinct positions may still be used together.

<!-- lecture-page -->

## 15 · Implementation 2/2



```python
            elif total > 0:
                right -= 1
            else:
                result.append([values[index], values[left], values[right]])
                left += 1
                right -= 1
                while left < right and values[left] == values[left - 1]:
                    left += 1
                while left < right and values[right] == values[right + 1]:
                    right -= 1
    return result
```

When the sum is zero, record the triplet and move both ends inward. The following while loops skip repeated values so the same value combination is not emitted again. Both pointers keep moving inward, so these skips are part of the same linear scan.

<!-- lecture-page -->

## Execution and sources

```text
cd code
python demo_01.py
python demo_02.py
python verify.py
```

Completed implementations are in solutions.py; independent work is in student_week_01.py. On LeetCode, adapt each function to the official method signature.

Erik Demaine and Srini Devadas, [Introduction to Algorithms, MIT 6.006](https://ocw.mit.edu/courses/6-006-introduction-to-algorithms-fall-2011/) (Fall 2011).

<!-- ko -->

## 연산 비용과 풀이

같은 데이터를 전부 제거해도 선택한 연산에 따라 총 비용이 달라집니다. n개 리스트의 앞을 계속 제거하면 이동하는 참조 수는 n-1, n-2, …, 0개입니다.

| 코드의 반복 작업 | 한 번 | 횟수 또는 총 이동량 | 전체 |
| --- | --- | --- | --- |
| list의 맨 뒤 pop | 분할상환 O(1) | n번 | O(n) |
| list의 맨 앞 pop(0) | 현재 길이에 비례 | n(n-1)/2회 이동 | O(<math xmlns="http://www.w3.org/1998/Math/MathML"><msup><mi>n</mi><mn>2</mn></msup></math>) |
| deque의 popleft | O(1) | n번 | O(n) |
| 매 값마다 이전 list에서 검색 | 최대 O(n) | n번 | O(<math xmlns="http://www.w3.org/1998/Math/MathML"><msup><mi>n</mi><mn>2</mn></msup></math>) |
| 매 값마다 dict 키 조회 | 기대 O(1) | n번 | 기대 O(n) |

합을 구하며 누적 값 하나만 유지하는 코드는 n번 더하므로 시간 O(n), 보조 공간 O(1)입니다. 반복 횟수와 저장량은 따로 셉니다.

<!-- lecture-page -->

## 1 · 단계별 힌트

[LeetCode 1: Two Sum](https://leetcode.com/problems/two-sum/) · Easy

신규 연습

H1. 현재 값과 짝이 되는 값은 무엇인가요?

H2. 같은 위치를 두 번 사용하지 않으려면 언제 기록하나요?

H3. 이전 값→인덱스를 저장하고 target-value를 조회한 뒤 현재 값을 기록합니다.

`nums=[4,8,3], target=7`

| index | value | 필요한 값 | 조회 전 seen | 결과 |
| --- | --- | --- | --- | --- |
| 0 | 4 | 3 | {} | 없음 → 4:0 저장 |
| 1 | 8 | -1 | {4:0} | 없음 → 8:1 저장 |
| 2 | 3 | 4 | {4:0,8:1} | 발견 → [0,2] |

<!-- lecture-page -->

## 1 · 정당성과 비용

반복 시작 때 사전에는 앞서 본 위치만 있습니다. 답의 두 번째 위치에 도착하면 첫 위치가 기록되어 있으므로 답을 찾습니다. 모든 쌍을 검사하는 O(<math xmlns="http://www.w3.org/1998/Math/MathML"><msup><mi>n</mi><mn>2</mn></msup></math>) 방법에서 이전 정보를 재사용한 것입니다.

각 원소에서 사전 조회·저장 횟수는 고정입니다. 기대 O(1)인 이 작업을 n번 하므로 기대 시간 O(n)입니다. 보조 사전은 최악에 n개의 서로 다른 값과 위치를 담아 O(n), 반환 인덱스 두 개는 O(1)입니다. 심한 해시 충돌까지 포함한 시간 상한은 O(<math xmlns="http://www.w3.org/1998/Math/MathML"><msup><mi>n</mi><mn>2</mn></msup></math>)입니다.

### 1 · 반례와 검증

[3,3], target=6에서 현재 값을 먼저 저장하면 같은 인덱스를 두 번 반환할 수 있습니다.

`nums=[4,8,3], target=7 → [0,2]`

<!-- lecture-page -->

## 1 · 구현 1/1



```python
def two_sum(nums, target):
    seen = {}
    for index, value in enumerate(nums):
        if target - value in seen:
            return [seen[target - value], index]
        seen[value] = index
    return []  # Defensive extension: official inputs have one answer.
```

각 반복은 현재 값의 짝 `target-value`를 사전에서 조회합니다. 찾지 못했을 때만 현재 값을 저장하므로 같은 위치를 두 번 쓰지 않습니다. `nums=[4,8,3]`에서 3을 읽을 때 사전의 4:0이 인덱스 0을 알려줍니다.

<!-- lecture-page -->

## 219 · 단계별 힌트

[LeetCode 219: Contains Duplicate II](https://leetcode.com/problems/contains-duplicate-ii/) · Easy

신규 연습

H1. 같은 값의 어떤 위치를 남길까요?

H2. 가장 가까운 과거 위치보다 오래된 위치가 더 유리할까요?

H3. 값마다 최근 인덱스를 남기고 거리를 비교한 뒤 갱신합니다.

`nums=[4,7,4,4], k=1`

| index | value | 이전 latest[value] | 거리 | 처리 |
| --- | --- | --- | --- | --- |
| 0 | 4 | 없음 | - | 4:0 저장 |
| 1 | 7 | 없음 | - | 7:1 저장 |
| 2 | 4 | 0 | 2 > 1 | 실패 후 4:2로 갱신 |
| 3 | 4 | 2 | 1 <= 1 | True 반환 |

<!-- lecture-page -->

## 219 · 정당성과 비용

최근 위치는 모든 이전 위치 중 현재 위치와 가장 가깝습니다. 이 거리도 k보다 크면 다른 과거 위치도 실패합니다. 갱신으로 다음 반복에도 같은 성질이 유지됩니다.

각 값마다 조회·거리 비교·저장을 한 번씩 하므로 기대 O(n) 시간입니다. 서로 다른 값 수 d만큼 사전 항목이 생겨 보조 공간 O(d), d<=n입니다. k=1이어도 입력이 모두 다르면 이 코드는 n개 키를 유지하므로 공간을 O(k)라고 할 수 없습니다.

### 219 · 반례와 검증

최초 위치만 저장하면 [4,7,4,4], k=1에서 마지막 두 위치를 놓칩니다. k=0에서는 서로 다른 위치의 답이 없습니다.

`nums=[4,7,4,4], k=1 → True`

<!-- lecture-page -->

## 219 · 구현 1/1



```python
def nearby_duplicate(nums, k):
    latest = {}
    for index, value in enumerate(nums):
        if value in latest and index - latest[value] <= k:
            return True
        latest[value] = index
    return False
```

latest의 값은 해당 숫자를 가장 최근에 본 위치입니다. 멀리 떨어져 실패한 경우에도 갱신해야 다음에 더 가까운 쌍을 찾습니다. k가 커져도 값마다 최근 위치 하나만 저장하며, 오래된 키를 지우는 구현은 아닙니다.

<!-- lecture-page -->

## 167 · 단계별 힌트

[LeetCode 167: Two Sum II - Input Array Is Sorted](https://leetcode.com/problems/two-sum-ii-input-array-is-sorted/) · Medium

신규 연습

H1. 양 끝 합이 작으면 어느 후보들이 모두 작나요?

H2. 정렬 조건을 지우면 이 제거가 가능한가요?

H3. left<right인 동안 합이 작으면 left, 크면 right를 안쪽으로 이동합니다.

`nums=[1,4,6,9], target=7`

| 현재 쌍 | 합 | target=7의 판정 | 제거되는 후보 |
| --- | --- | --- | --- |
| 1,9 | 10 | 너무 큼 | 9와 1·4·6의 쌍 |
| 1,6 | 7 | 정답 | 더 제거하지 않음 |

<!-- lecture-page -->

## 167 · 정당성과 비용

합이 작으면 현재 left와 right 이하의 어떤 값도 답을 만들지 못합니다. 합이 크면 현재 right와 left 이상의 어떤 값도 실패합니다. 제거된 쌍에는 답이 없으므로 남은 범위가 답을 보존합니다.

간격 right-left는 처음 n-1이며 반복마다 적어도 1 줄어듭니다. 따라서 비교는 최대 O(n)번입니다. 포인터 두 개와 합만 저장하여 보조 공간 O(1), 반환 위치 두 개도 O(1)입니다. 원소들을 복사하거나 정렬하는 코드는 포함되어 있지 않습니다.

### 167 · 반례와 검증

정렬 전제 밖 [3,1,4], target=5에는 같은 이동 규칙을 적용할 수 없습니다. left==right는 같은 원소 재사용입니다.

`numbers=[1,4,6,9], target=10 → [1,4]`

<!-- lecture-page -->

## 167 · 구현 1/1



```python
def two_sum_sorted(numbers, target):
    left, right = 0, len(numbers) - 1
    while left < right:
        total = numbers[left] + numbers[right]
        if total == target:
            return [left + 1, right + 1]
        if total < target:
            left += 1
        else:
            right -= 1
    return []
```

작은 합에서 left를 늘리는 것은 현재 왼쪽 값으로 만들 수 있는 모든 쌍이 너무 작기 때문입니다. 큰 합에서는 오른쪽 값을 제외합니다. 이동 뒤 두 포인터 사이 후보만 남으므로 이미 탈락한 쌍을 다시 읽지 않습니다.

<!-- lecture-page -->

## 15 · 단계별 힌트

[LeetCode 15: 3Sum](https://leetcode.com/problems/3sum/) · Medium

신규 연습

H1. 한 값을 고정하면 남는 문제는 무엇인가요?

H2. 같은 값을 다시 고정하면 새 조합이 생기나요?

H3. 복사 정렬 후 첫 값을 고정하고 뒤쪽에서 두 포인터를 사용합니다. 고정 값과 발견한 쌍의 중복을 건너뜁니다.

`nums=[-2,0,1,1,2]`

| index,left,right | 세 값 | 합 | 동작 |
| --- | --- | --- | --- |
| 0,1,4 | -2,0,2 | 0 | [-2,0,2] 저장; 양쪽 이동 |
| 0,2,3 | -2,1,1 | 0 | [-2,1,1] 저장; 양쪽 이동 |
| 0,3,2 | 범위 끝 | - | 고정 값 -2의 탐색 종료 |

<!-- lecture-page -->

## 15 · 정당성과 비용

각 정렬된 세 값은 가장 작은 값의 차례에서 검사됩니다. 두 포인터 제거는 정렬로 정당화됩니다. 같은 값을 건너뛰는 것은 위치가 다른 동일한 값 조합만 제거합니다.

고정 인덱스가 최대 n개이고 각 인덱스에서 두 포인터의 총 이동이 O(n)이므로 O(<math xmlns="http://www.w3.org/1998/Math/MathML"><msup><mi>n</mi><mn>2</mn></msup></math>)입니다. 중복을 넘기는 while도 같은 방향 이동의 일부라 별도 n을 다시 곱하지 않습니다. 정렬 O(n log n)은 이보다 작습니다. 복사·정렬 작업 공간 O(n)과 정답 z개의 출력 공간 O(z)를 구분합니다.

### 15 · 반례와 검증

[0,0,0,0]은 한 조합만 반환합니다. 값이 같다는 이유로 서로 다른 위치를 금지하면 이 답을 잃습니다.

`nums=[-2,0,1,1,2] → [[-2,0,2],[-2,1,1]]`

<!-- lecture-page -->

## 15 · 구현 1/2



```python
def three_sum(nums):
    values = sorted(nums)
    result = []
    for index in range(len(values) - 2):
        if index and values[index] == values[index - 1]:
            continue
        left, right = index + 1, len(values) - 1
        while left < right:
            total = values[index] + values[left] + values[right]
            if total < 0:
                left += 1
```

고정 값 하나마다 뒤쪽에서 두 포인터를 새로 시작합니다. 같은 고정 값을 건너뛰고, 정답을 저장한 뒤 양쪽의 같은 값을 건너뛰어 값 조합의 중복을 제거합니다. 서로 다른 위치의 같은 값 두 개를 사용하는 것은 허용됩니다.

<!-- lecture-page -->

## 15 · 구현 2/2



```python
            elif total > 0:
                right -= 1
            else:
                result.append([values[index], values[left], values[right]])
                left += 1
                right -= 1
                while left < right and values[left] == values[left - 1]:
                    left += 1
                while left < right and values[right] == values[right + 1]:
                    right -= 1
    return result
```

합이 0이면 세 값을 저장한 뒤 양 끝을 한 칸씩 옮깁니다. 이후 같은 값을 넘기는 while은 이미 저장한 값 조합을 반복하지 않기 위한 것입니다. 포인터는 계속 안쪽으로만 이동하므로 이 중복 제거도 같은 선형 탐색 비용에 포함됩니다.

<!-- lecture-page -->

## 실행과 참고자료

```text
cd code
python demo_01.py
python demo_02.py
python verify.py
```

완성 코드는 `solutions.py`, 독립 실습은 `student_week_01.py`에 있습니다. LeetCode에서는 공식 메서드 서명에 맞춰 함수를 연결합니다.

Erik Demaine and Srini Devadas, [Introduction to Algorithms, MIT 6.006](https://ocw.mit.edu/courses/6-006-introduction-to-algorithms-fall-2011/) (Fall 2011).
