---
layout: "course-resource"
title: "Week 1 Student Exercises"
title_ko: "1주차 학생 실습"
permalink: "/courses/practical-algorithms/week-01-practice/"
course_id: "practical-algorithms"
---

## Set up and run

Extract the [lab code ZIP](/assets/courses/practical-algorithms/practical-algorithms-code.zip) and work in its code folder. Use Python 3.11+ and the standard library.

```text
python trace_lab.py --case two_sum
python verify.py
python verify.py --student
```

Predict the small example and its states on paper first. `trace_lab.py` traces the actual `solutions.py` implementation. `before L…` shows values immediately before that line executes: identify what the preceding executed line changed. Linked lists display a chain; tree nodes display their value and child values. Exclude tracing, copying, and printing overhead from the algorithm's complexity.

Implement the functions and methods in `student_week_01.py`, then run `verify.py --student`. An initial `NotImplementedError` identifies work still to implement. Without `--student`, the verifier checks the supplied solutions. Use `python trace_lab.py --case FUNCTION --student` to inspect your implementation.

For each task record the input/output meaning, state invariant, one state transition, final answer, time, auxiliary space, and output space. Passing one small example does not establish correctness for all inputs.

## This week’s problems

- [two_sum](#en-two_sum)
- [nearby_duplicate](#en-nearby_duplicate)
- [two_sum_sorted](#en-two_sum_sorted)
- [three_sum](#en-three_sum)

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

## Sharing resize costs across calls

Count eight appends to an array whose capacity doubles through 1,2,4,8. This is a calculation for geometric growth, not CPython's exact allocation schedule.

| Length after append | New capacity needed | Existing references moved |
| --- | --- | --- |
| 1 | 1 | 0 |
| 2 | 2 | 1 |
| 3 | 4 | 2 |
| 4 | unchanged | 0 |
| 5 | 8 | 4 |
| 6–8 | unchanged | 0 |

Eight new writes plus 1+2+4=7 copies give 15 operations. When N is a power of two, copies total N−1 and all writes total 2N−1. Between powers of two, copies remain below 2N, so total cost is O(N). Growing by just one slot would instead copy 1+2+…+(N−1) references, giving O(N²).

Dividing O(N) total work by N calls gives amortized O(1) per append.

<a id="en-two_sum"></a>

## [LeetCode 1: Two Sum](https://leetcode.com/problems/two-sum/) · Easy

Return two distinct indices whose values sum to target.

2 <= n <= 10^4; values and target: -10^9..10^9; exactly one answer.

### Predict before implementing

For each value, compute target minus value. Look up that complement in a dictionary of earlier indices, then store the current index. Test [3,3] with target 6 to check that the two indices differ.

```python
two_sum([4, 8, 3], 7)
# [0, 2]
```

### Idea and state transitions

#### 1 · Staged hints

Return two distinct indices whose values sum to target. An element cannot be reused; official inputs have one answer.

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

#### 1 · Correctness and cost

At loop entry, the map contains only earlier positions. At the later position of the unique answer, its partner is present. This reuses information instead of checking all O(<math xmlns="http://www.w3.org/1998/Math/MathML"><msup><mi>n</mi><mn>2</mn></msup></math>) pairs.

Each element performs a fixed number of dictionary operations. Expected O(1) operations repeated n times give expected O(n) time. Up to n distinct value-position entries use O(n) auxiliary space; two returned indices use O(1). Severe hash collisions give an O(<math xmlns="http://www.w3.org/1998/Math/MathML"><msup><mi>n</mi><mn>2</mn></msup></math>) worst-case upper bound.

### 1 · Counterexamples and checks

Recording first can reuse one index on [3,3], target=6.

`nums=[4,8,3], target=7 → [0,2]`

### Implement and execute

```python
def two_sum(nums, target):
    seen = {}
    for index, value in enumerate(nums):
        if target - value in seen:
            return [seen[target - value], index]
        seen[value] = index
    return []
```

```text
python trace_lab.py --case two_sum
```

Compare the trace return value with your prediction. Make the input change proposed above, find the first line where the state differs, and explain its effect on the answer.

<a id="en-nearby_duplicate"></a>

## [LeetCode 219: Contains Duplicate II](https://leetcode.com/problems/contains-duplicate-ii/) · Easy

Decide whether equal values occur at distinct indices at distance at most k.

1 <= n <= 10^5; values -10^9..10^9; 0 <= k <= 10^5.

### Predict before implementing

Store the most recent index for each value. Compare the index distance before replacing it. At index 3, the preceding 4 is at index 2, not index 0. Change k to 0 and explain False.

```python
nearby_duplicate([4, 7, 4, 4], 1)
# True
```

### Idea and state transitions

#### 219 · Staged hints

Return True exactly when equal values occur at distinct positions i,j with distance <math xmlns="http://www.w3.org/1998/Math/MathML"><mrow><mo stretchy="false">&#x7C;</mo><mi>i</mi><mo>−</mo><mi>j</mi><mo stretchy="false">&#x7C;</mo></mrow></math> at most k.

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

#### 219 · Correctness and cost

The latest occurrence minimizes distance to the current index. If it is too far, all older occurrences are too far. Updating preserves this property.

One lookup, distance comparison, and update per value give expected O(n) time. There are d entries for d distinct values, so auxiliary space is O(d), d<=n. Even with k=1, all-distinct input leaves n keys; this implementation is not O(k)-space.

### 219 · Counterexamples and checks

Keeping only the first position misses the last pair in [4,7,4,4], k=1. No distinct-index pair qualifies when k=0.

`nums=[4,7,4,4], k=1 → True`

### Implement and execute

```python
def nearby_duplicate(nums, k):
    latest = {}
    for index, value in enumerate(nums):
        if value in latest and index - latest[value] <= k:
            return True
        latest[value] = index
    return False
```

```text
python trace_lab.py --case nearby_duplicate
```

Compare the trace return value with your prediction. Make the input change proposed above, find the first line where the state differs, and explain its effect on the answer.

<a id="en-two_sum_sorted"></a>

## [LeetCode 167: Two Sum II - Input Array Is Sorted](https://leetcode.com/problems/two-sum-ii-input-array-is-sorted/) · Medium

Return 1-based positions of a target-sum pair in a sorted array.

2 <= n <= 30000; values/target -1000..1000; nondecreasing; one answer; constant extra space.

### Predict before implementing

Start at both ends. If the sum is too large, move the right pointer left; if too small, move the left pointer right. Track sums 10 then 7. Convert zero-based positions to the required one-based answer.

```python
two_sum_sorted([1, 4, 6, 9], 7)
# [1, 3]
```

### Idea and state transitions

#### 167 · Staged hints

Find two distinct positions summing to target in a nondecreasing array. Return 1-based indices using O(1) auxiliary space.

[LeetCode 167: Two Sum II - Input Array Is Sorted](https://leetcode.com/problems/two-sum-ii-input-array-is-sorted/) · Medium

H1. If the endpoint sum is too small, which candidates are all too small?

H2. Does the elimination remain valid without sorting?

H3. While left<right, move left inward for a small sum and right inward for a large sum.

`nums=[1,4,6,9], target=7`

| Current pair | Sum | Decision for target=7 | Removed candidates |
| --- | --- | --- | --- |
| 1,9 | 10 | Too large | 9 paired with 1,4,6 |
| 1,6 | 7 | Answer | No further elimination |

#### 167 · Correctness and cost

If the sum is small, no partner at or below right works with left. If large, no partner at or above left works with right. Each elimination preserves any answer.

The initial gap right-left is n-1 and decreases by at least one per iteration, giving O(n) comparisons. Two pointers and a sum use O(1) auxiliary space; the two returned positions use O(1). No copy or sorting step is present.

### 167 · Counterexamples and checks

Outside the sorted contract, [3,1,4], target=5 defeats this rule. left==right reuses one element.

`numbers=[1,4,6,9], target=10 → [1,4]`

### Implement and execute

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

```text
python trace_lab.py --case two_sum_sorted
```

Compare the trace return value with your prediction. Make the input change proposed above, find the first line where the state differs, and explain its effect on the answer.

<a id="en-three_sum"></a>

## [LeetCode 15: 3Sum](https://leetcode.com/problems/3sum/) · Medium

Return distinct value triplets summing to zero at three distinct positions.

3 <= n <= 3000; values -10^5..10^5.

### Predict before implementing

Sort, fix one value, and find its opposite using two pointers. Skip equal fixed values and equal pointer values after a match. Try [0,0,0,0]: four indices produce only one distinct value triple.

```python
three_sum([-2, 0, 1, 1, 2],)
# [[-2, 0, 2], [-2, 1, 1]]
```

### Idea and state transitions

#### 15 · Staged hints

Return all distinct value triples from three distinct positions whose sum is zero. Results contain values rather than indices, with no repeated value combination.

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

#### 15 · Correctness and cost

Every ordered triplet is examined when its smallest value is fixed. Sorted elimination is valid; skipping duplicates removes repeated value combinations only.

There are at most n fixed positions, each with O(n) total pointer movement: O(<math xmlns="http://www.w3.org/1998/Math/MathML"><msup><mi>n</mi><mn>2</mn></msup></math>) time. Duplicate-skipping loops are part of those same movements, not another factor of n. O(n log n) sorting is dominated. Copy/sort workspace is O(n), separate from O(z) space for z output triplets.

### 15 · Counterexamples and checks

[0,0,0,0] yields one triplet. Equal values at distinct positions remain allowed.

`nums=[-2,0,1,1,2] → [[-2,0,2],[-2,1,1]]`

### Implement and execute

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

```text
python trace_lab.py --case three_sum
```

Compare the trace return value with your prediction. Make the input change proposed above, find the first line where the state differs, and explain its effect on the answer.

## Lab report

Include the small-input state table, completed code, your own boundary input and expected result, and verification results. Explain time by total operation counts and space by simultaneously live state. Include any input copying or sorting costs.

<!-- ko -->

## 실행 준비

[실습 코드 ZIP](/assets/courses/practical-algorithms/practical-algorithms-code.zip)을 풀고 코드 폴더에서 실행합니다. Python 3.11 이상과 표준 라이브러리를 사용합니다.

```text
python trace_lab.py --case two_sum
python verify.py
python verify.py --student
```

먼저 작은 입력의 답과 상태 변화를 종이에 적고 실행 결과와 비교하세요. `trace_lab.py`는 `solutions.py`의 실제 실행을 추적합니다. `before L…`은 그 행을 실행하기 직전의 값이므로, 앞서 실행한 행이 무엇을 바꿨는지 읽습니다. 연결 리스트는 chain, 트리 노드는 값과 두 자식 값으로 표시합니다. 추적 출력의 복사·표시 비용은 알고리즘의 시간·공간 분석에 포함하지 않습니다.

`student_week_01.py`의 함수와 메서드를 구현한 뒤 `verify.py --student`로 검사합니다. 미구현 상태의 `NotImplementedError`는 해당 함수부터 채우라는 뜻입니다. `--student` 없이 실행하면 제공 풀이를 검사합니다. 특정 풀이의 동작은 `python trace_lab.py --case 함수명 --student`로 대조할 수 있습니다.

각 문제에서 입력·출력의 의미, 상태의 불변식, 한 단계의 변화, 최종 답, 시간·보조 공간·반환값 공간을 기록하세요. 아래 작은 예제 하나의 통과만으로 전체 정당성이 증명되지는 않습니다.

## 이 주의 문제

- [two_sum](#ko-two_sum)
- [nearby_duplicate](#ko-nearby_duplicate)
- [two_sum_sorted](#ko-two_sum_sorted)
- [three_sum](#ko-three_sum)

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

## 확장 비용을 여러 호출에 나누기

용량을 1,2,4,8칸으로 두 배씩 늘리는 배열에서 append 8회를 세어봅니다. CPython의 실제 증설 비율을 재현한 표는 아니며, 비율을 정해 확장할 때 총 이동량이 어떻게 제한되는지 계산합니다.

| 추가 후 길이 | 필요한 새 용량 | 옮기는 기존 참조 수 |
| --- | --- | --- |
| 1 | 1 | 0 |
| 2 | 2 | 1 |
| 3 | 4 | 2 |
| 4 | 유지 | 0 |
| 5 | 8 | 4 |
| 6~8 | 유지 | 0 |

새 값 기록 8회와 복사 1+2+4=7회를 합하면 15회입니다. N이 2의 거듭제곱이면 복사 합은 N−1, 총 기록은 2N−1입니다. N이 그 사이에 있어도 복사 합은 2N보다 작아 총비용은 O(N)입니다. 반면 용량을 한 칸씩만 늘리면 1+2+…+(N−1)을 복사하므로 O(N²)이 됩니다.

전체 O(N)을 호출 N회로 나누면 append의 분할상환 비용은 O(1)입니다.

<a id="ko-two_sum"></a>

## [LeetCode 1: Two Sum](https://leetcode.com/problems/two-sum/) · Easy

서로 다른 두 위치의 합이 target인 인덱스 쌍을 반환합니다.

2 <= n <= 10^4; 값과 target은 -10^9..10^9; 답은 하나.

### 구현 전 예측

현재 값마다 target에서 그 값을 뺍니다. 이전 인덱스를 담은 dictionary에서 필요한 값을 찾은 뒤 현재 인덱스를 저장합니다. [3,3], target=6으로 두 인덱스가 서로 다른지 확인하세요.

```python
two_sum([4, 8, 3], 7)
# [0, 2]
```

### 풀이 아이디어와 상태 변화

#### 1 · 단계별 힌트

서로 다른 두 인덱스의 값 합이 target인 인덱스 두 개를 반환합니다. 같은 원소를 재사용하지 않으며, 공식 입력에는 답 하나가 있습니다.

[LeetCode 1: Two Sum](https://leetcode.com/problems/two-sum/) · Easy

H1. 현재 값과 짝이 되는 값은 무엇인가요?

H2. 같은 위치를 두 번 사용하지 않으려면 언제 기록하나요?

H3. 이전 값→인덱스를 저장하고 target-value를 조회한 뒤 현재 값을 기록합니다.

`nums=[4,8,3], target=7`

| index | value | 필요한 값 | 조회 전 seen | 결과 |
| --- | --- | --- | --- | --- |
| 0 | 4 | 3 | {} | 없음 → 4:0 저장 |
| 1 | 8 | -1 | {4:0} | 없음 → 8:1 저장 |
| 2 | 3 | 4 | {4:0,8:1} | 발견 → [0,2] |

#### 1 · 정당성과 비용

반복 시작 때 사전에는 앞서 본 위치만 있습니다. 답의 두 번째 위치에 도착하면 첫 위치가 기록되어 있으므로 답을 찾습니다. 모든 쌍을 검사하는 O(<math xmlns="http://www.w3.org/1998/Math/MathML"><msup><mi>n</mi><mn>2</mn></msup></math>) 방법에서 이전 정보를 재사용한 것입니다.

각 원소에서 사전 조회·저장 횟수는 고정입니다. 기대 O(1)인 이 작업을 n번 하므로 기대 시간 O(n)입니다. 보조 사전은 최악에 n개의 서로 다른 값과 위치를 담아 O(n), 반환 인덱스 두 개는 O(1)입니다. 심한 해시 충돌까지 포함한 시간 상한은 O(<math xmlns="http://www.w3.org/1998/Math/MathML"><msup><mi>n</mi><mn>2</mn></msup></math>)입니다.

### 1 · 반례와 검증

[3,3], target=6에서 현재 값을 먼저 저장하면 같은 인덱스를 두 번 반환할 수 있습니다.

`nums=[4,8,3], target=7 → [0,2]`

### 구현과 실행

```python
def two_sum(nums, target):
    seen = {}
    for index, value in enumerate(nums):
        if target - value in seen:
            return [seen[target - value], index]
        seen[value] = index
    return []
```

```text
python trace_lab.py --case two_sum
```

위 예측과 trace의 반환값을 대조하세요. 입력을 앞에서 제안한 대로 바꾸고, 처음으로 상태가 달라지는 행을 찾아 그 변화가 답에 미친 영향을 설명합니다.

<a id="ko-nearby_duplicate"></a>

## [LeetCode 219: Contains Duplicate II](https://leetcode.com/problems/contains-duplicate-ii/) · Easy

같은 값의 서로 다른 두 위치가 거리 k 이내인지 반환합니다.

1 <= n <= 10^5; 값 -10^9..10^9; 0 <= k <= 10^5.

### 구현 전 예측

값마다 가장 최근 인덱스를 저장합니다. 인덱스 차이를 비교한 뒤 기록을 갱신합니다. 인덱스 3에서 직전 4의 위치는 0이 아니라 2입니다. k를 0으로 바꾸고 False인 이유를 설명하세요.

```python
nearby_duplicate([4, 7, 4, 4], 1)
# True
```

### 풀이 아이디어와 상태 변화

#### 219 · 단계별 힌트

서로 다른 위치 i,j에서 값이 같고 거리 <math xmlns="http://www.w3.org/1998/Math/MathML"><mrow><mo stretchy="false">&#x7C;</mo><mi>i</mi><mo>−</mo><mi>j</mi><mo stretchy="false">&#x7C;</mo></mrow></math>가 k 이하이면 True, 아니면 False입니다.

[LeetCode 219: Contains Duplicate II](https://leetcode.com/problems/contains-duplicate-ii/) · Easy

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

#### 219 · 정당성과 비용

최근 위치는 모든 이전 위치 중 현재 위치와 가장 가깝습니다. 이 거리도 k보다 크면 다른 과거 위치도 실패합니다. 갱신으로 다음 반복에도 같은 성질이 유지됩니다.

각 값마다 조회·거리 비교·저장을 한 번씩 하므로 기대 O(n) 시간입니다. 서로 다른 값 수 d만큼 사전 항목이 생겨 보조 공간 O(d), d<=n입니다. k=1이어도 입력이 모두 다르면 이 코드는 n개 키를 유지하므로 공간을 O(k)라고 할 수 없습니다.

### 219 · 반례와 검증

최초 위치만 저장하면 [4,7,4,4], k=1에서 마지막 두 위치를 놓칩니다. k=0에서는 서로 다른 위치의 답이 없습니다.

`nums=[4,7,4,4], k=1 → True`

### 구현과 실행

```python
def nearby_duplicate(nums, k):
    latest = {}
    for index, value in enumerate(nums):
        if value in latest and index - latest[value] <= k:
            return True
        latest[value] = index
    return False
```

```text
python trace_lab.py --case nearby_duplicate
```

위 예측과 trace의 반환값을 대조하세요. 입력을 앞에서 제안한 대로 바꾸고, 처음으로 상태가 달라지는 행을 찾아 그 변화가 답에 미친 영향을 설명합니다.

<a id="ko-two_sum_sorted"></a>

## [LeetCode 167: Two Sum II - Input Array Is Sorted](https://leetcode.com/problems/two-sum-ii-input-array-is-sorted/) · Medium

정렬된 배열에서 합이 target인 두 위치를 1-based로 반환합니다.

2 <= n <= 30000; 값·target -1000..1000; 비내림차순; 답 하나; 상수 보조 공간.

### 구현 전 예측

양 끝에서 시작합니다. 합이 크면 오른쪽 포인터를 왼쪽으로, 작으면 왼쪽 포인터를 오른쪽으로 옮깁니다. 합이 10에서 7로 바뀌는 과정을 적고, 0부터 센 위치를 문제에서 요구하는 1부터 센 인덱스로 바꾸세요.

```python
two_sum_sorted([1, 4, 6, 9], 7)
# [1, 3]
```

### 풀이 아이디어와 상태 변화

#### 167 · 단계별 힌트

비내림차순 배열에서 합이 target인 서로 다른 두 위치를 찾습니다. 답은 1-based 인덱스이며 보조 공간 O(1)이 요구됩니다.

[LeetCode 167: Two Sum II - Input Array Is Sorted](https://leetcode.com/problems/two-sum-ii-input-array-is-sorted/) · Medium

H1. 양 끝 합이 작으면 어느 후보들이 모두 작나요?

H2. 정렬 조건을 지우면 이 제거가 가능한가요?

H3. left<right인 동안 합이 작으면 left, 크면 right를 안쪽으로 이동합니다.

`nums=[1,4,6,9], target=7`

| 현재 쌍 | 합 | target=7의 판정 | 제거되는 후보 |
| --- | --- | --- | --- |
| 1,9 | 10 | 너무 큼 | 9와 1·4·6의 쌍 |
| 1,6 | 7 | 정답 | 더 제거하지 않음 |

#### 167 · 정당성과 비용

합이 작으면 현재 left와 right 이하의 어떤 값도 답을 만들지 못합니다. 합이 크면 현재 right와 left 이상의 어떤 값도 실패합니다. 제거된 쌍에는 답이 없으므로 남은 범위가 답을 보존합니다.

간격 right-left는 처음 n-1이며 반복마다 적어도 1 줄어듭니다. 따라서 비교는 최대 O(n)번입니다. 포인터 두 개와 합만 저장하여 보조 공간 O(1), 반환 위치 두 개도 O(1)입니다. 원소들을 복사하거나 정렬하는 코드는 포함되어 있지 않습니다.

### 167 · 반례와 검증

정렬 전제 밖 [3,1,4], target=5에는 같은 이동 규칙을 적용할 수 없습니다. left==right는 같은 원소 재사용입니다.

`numbers=[1,4,6,9], target=10 → [1,4]`

### 구현과 실행

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

```text
python trace_lab.py --case two_sum_sorted
```

위 예측과 trace의 반환값을 대조하세요. 입력을 앞에서 제안한 대로 바꾸고, 처음으로 상태가 달라지는 행을 찾아 그 변화가 답에 미친 영향을 설명합니다.

<a id="ko-three_sum"></a>

## [LeetCode 15: 3Sum](https://leetcode.com/problems/3sum/) · Medium

서로 다른 세 위치의 합이 0인 값의 조합을 중복 없이 반환합니다.

3 <= n <= 3000; 값 -10^5..10^5.

### 구현 전 예측

정렬한 뒤 값 하나를 고정하고 나머지 두 값의 합을 포인터로 찾습니다. 고정 값이 반복되거나 답을 찾은 뒤 포인터 값이 반복되면 건너뜁니다. [0,0,0,0]에서 서로 다른 값의 조합이 하나만 나와야 하는 이유를 설명하세요.

```python
three_sum([-2, 0, 1, 1, 2],)
# [[-2, 0, 2], [-2, 1, 1]]
```

### 풀이 아이디어와 상태 변화

#### 15 · 단계별 힌트

합이 0인 서로 다른 세 위치의 값 조합을 모두 반환합니다. 결과는 인덱스가 아닌 값이며, 같은 값 조합을 중복 반환하지 않습니다.

[LeetCode 15: 3Sum](https://leetcode.com/problems/3sum/) · Medium

H1. 한 값을 고정하면 남는 문제는 무엇인가요?

H2. 같은 값을 다시 고정하면 새 조합이 생기나요?

H3. 복사 정렬 후 첫 값을 고정하고 뒤쪽에서 두 포인터를 사용합니다. 고정 값과 발견한 쌍의 중복을 건너뜁니다.

`nums=[-2,0,1,1,2]`

| index,left,right | 세 값 | 합 | 동작 |
| --- | --- | --- | --- |
| 0,1,4 | -2,0,2 | 0 | [-2,0,2] 저장; 양쪽 이동 |
| 0,2,3 | -2,1,1 | 0 | [-2,1,1] 저장; 양쪽 이동 |
| 0,3,2 | 범위 끝 | - | 고정 값 -2의 탐색 종료 |

#### 15 · 정당성과 비용

각 정렬된 세 값은 가장 작은 값의 차례에서 검사됩니다. 두 포인터 제거는 정렬로 정당화됩니다. 같은 값을 건너뛰는 것은 위치가 다른 동일한 값 조합만 제거합니다.

고정 인덱스가 최대 n개이고 각 인덱스에서 두 포인터의 총 이동이 O(n)이므로 O(<math xmlns="http://www.w3.org/1998/Math/MathML"><msup><mi>n</mi><mn>2</mn></msup></math>)입니다. 중복을 넘기는 while도 같은 방향 이동의 일부라 별도 n을 다시 곱하지 않습니다. 정렬 O(n log n)은 이보다 작습니다. 복사·정렬 작업 공간 O(n)과 정답 z개의 출력 공간 O(z)를 구분합니다.

### 15 · 반례와 검증

[0,0,0,0]은 한 조합만 반환합니다. 값이 같다는 이유로 서로 다른 위치를 금지하면 이 답을 잃습니다.

`nums=[-2,0,1,1,2] → [[-2,0,2],[-2,1,1]]`

### 구현과 실행

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

```text
python trace_lab.py --case three_sum
```

위 예측과 trace의 반환값을 대조하세요. 입력을 앞에서 제안한 대로 바꾸고, 처음으로 상태가 달라지는 행을 찾아 그 변화가 답에 미친 영향을 설명합니다.

## 실습 보고서

작은 입력의 상태표, 완성 코드, 직접 만든 경계 입력과 예상값, 검증 결과를 함께 기록합니다. 시간 복잡도는 총 연산 횟수로, 공간 복잡도는 동시에 살아 있는 상태로 설명하세요. 입력을 복사하거나 정렬한다면 그 비용도 포함합니다.
