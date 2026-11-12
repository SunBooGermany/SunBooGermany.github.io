---
layout: "course-resource"
title: "Week 8 Instructor Guide"
title_ko: "8주차 교사용 진행안"
permalink: "/courses/practical-algorithms/week-08-instructor/"
course_id: "practical-algorithms"
---
## Teaching sequence

Ask learners to predict the lecture traces before running demos. In session 15, focus on the first group of problems; in session 16, compare the later state definitions. Use the student file before opening solutions.

## Concept checks

A successful example does not prove a greedy rule. Every position in the current reachable range must be considered before fixing the next level’s boundary.



## Checkpoint answers

1. No. The reachable boundary remains 2.
2. 2, following 0→1→4.
3. Zero-based index 1. The tank after each leg is 3,2,0.
4. `0`. The start is already the last position, so no jump is counted.

## Review criteria

Check contract, state meaning, correctness, time, auxiliary/output space, and boundary inputs separately. Accept alternative correct methods with their own cost analysis. Local tests do not replace a correctness argument.

## Job-selection problem: instructor key

Sort jobs by end time. Let dp[i] be the best reward using the first i jobs. An optimum either skips job i or takes it after the compatible prefix. Earlier jobs ending no later than the current start form a prefix, so these cases cover every valid selection. Empty selection gives dp[0]=0. The linear predecessor scan gives O(n²) time and O(n) space, including the sorted copy; input rows are unchanged.

```python
def weighted_jobs(jobs):
    ordered = sorted(jobs, key=lambda job: job[1])
    dp = [0] * (len(ordered) + 1)
    for i, (start, end, reward) in enumerate(ordered):
        compatible = 0
        for j in range(i):
            if ordered[j][1] <= start:
                compatible = j + 1
        dp[i + 1] = max(dp[i], reward + dp[compatible])
    return dp[-1]
```

For `[[0,2,3],[2,4,3],[0,4,10]]`, the best reward is 10, rather than 6 from the two shorter jobs. Exhaustive subset enumeration is also valid under the 12-job limit; assess its O(n·<math xmlns="http://www.w3.org/1998/Math/MathML"><msup><mn>2</mn><mi>n</mi></msup></math>+n log n) time with presorting and O(n) auxiliary space separately.


<!-- ko -->

## 수업 순서

시연 실행 전에 강의 추적 표의 다음 상태를 예상하게 합니다. 15차시에서는 앞의 문제 묶음을 풀고, 16차시에서는 뒤의 상태 정의를 비교합니다. 학생 파일을 먼저 작성하고 해설을 엽니다.

## 개념 질문 해설

예제 성공은 그리디 규칙의 증명이 아닙니다. 현재 도달 범위의 모든 위치를 확인해야 다음 레벨의 최대 범위를 확정할 수 있습니다.



## 중간 점검 답

1. 불가능합니다. 도달 범위의 끝이 2에 머뭅니다.
2. `2`. 0→1→4로 이동합니다.
3. 0부터 센 인덱스 1. 순환하며 탱크는 3,2,0입니다.
4. `0`. 이미 마지막 위치에 있으므로 추가 점프를 세지 않습니다.

## 검토 기준

입력 계약·상태 의미·정당성·시간·보조 공간·출력 공간·경계 입력을 나누어 확인합니다. 다른 올바른 풀이도 해당 비용 분석과 함께 인정합니다. 로컬 검사는 정당성 설명을 대신하지 않습니다.

## 작업 선택 문제: 교사용 답

끝 시간으로 정렬하고 dp[i]를 앞 i개 작업에서 얻을 수 있는 최대 보상으로 정의합니다. 최적해는 현재 작업을 건너뛰거나, 호환되는 접두부의 최적해 뒤에 현재 작업을 선택합니다. 현재 시작 시간 이하에 끝나는 이전 작업은 접두부를 이루므로 두 경우가 모든 선택을 포함합니다. 빈 선택의 초기값은 dp[0]=0입니다. 호환 작업을 선형 탐색하므로 O(n²) 시간이며, 정렬 복사를 포함해 O(n) 공간입니다. 입력 행은 바꾸지 않습니다.

```python
def weighted_jobs(jobs):
    ordered = sorted(jobs, key=lambda job: job[1])
    dp = [0] * (len(ordered) + 1)
    for i, (start, end, reward) in enumerate(ordered):
        compatible = 0
        for j in range(i):
            if ordered[j][1] <= start:
                compatible = j + 1
        dp[i + 1] = max(dp[i], reward + dp[compatible])
    return dp[-1]
```

`[[0,2,3],[2,4,3],[0,4,10]]`의 최댓값은 10입니다. 짧은 두 작업의 합 6보다 큽니다. 최대 12개 조건에서는 부분집합 완전 탐색도 정답으로 인정합니다. 미리 정렬하면 O(n·<math xmlns="http://www.w3.org/1998/Math/MathML"><msup><mn>2</mn><mi>n</mi></msup></math>+n log n) 시간과 O(n) 보조 공간이 드는 점을 따로 평가합니다.
