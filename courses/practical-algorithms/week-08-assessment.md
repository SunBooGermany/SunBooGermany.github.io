---
layout: "course-resource"
title: "Mixed Assessment"
title_ko: "혼합 평가"
permalink: "/courses/practical-algorithms/week-08-assessment/"
course_id: "practical-algorithms"
---
## Independent task selection

Choose one of [200](https://leetcode.com/problems/number-of-islands/), [322](https://leetcode.com/problems/coin-change/), [56](https://leetcode.com/problems/merge-intervals/), or [207](https://leetcode.com/problems/course-schedule/). Read the linked contract. Record whether you have seen the problem before, then submit code, reasoning, complexity, and boundary checks.

## Job-selection problem

Input: 1..12 jobs [start,end,reward], with integer times 0..30, start<end, reward 0..20. Output: maximum reward obtainable without overlap. Touching endpoints are allowed; selecting no jobs is allowed. Example: [[0,2,3],[2,4,3],[0,4,10]] → 10. No input mutation is allowed.

Submit your function, an argument covering all possible selections, time/space costs, and a small independently checked input.

## Work through a smaller schedule

Use jobs A=[0,2,4], B=[2,3,3], C=[1,4,8]. A and B can both run because A ends when B starts. Their reward is 7; C overlaps each and gives 8. Draw the occupied half-open intervals [start,end) before choosing an algorithm.

Sorting by end time creates prefixes. Define dp[i] as the best reward using the first i sorted jobs; dp[0]=0 permits the empty choice. For the current job, either skip it and retain the preceding best, or take its reward plus the best prefix whose jobs end by its start. These two cases cover every valid selection.

| Job | Earlier compatible prefix length | Skip | Take | New best |
| --- | --- | --- | --- | --- |
| A: [0,2,4] | 0 | 0 | 4+0=4 | 4 |
| B: [2,3,3] | 1 | 4 | 3+4=7 | 7 |
| C: [1,4,8] | 0 | 7 | 8+0=8 | 8 |

Implement `weighted_jobs(jobs)` in `student_week_08.py`. Use sorted(jobs, key=...) to preserve the input. For each sorted job, scan earlier jobs to find the last compatible one and convert its zero-based index to a prefix length. Compute take before writing dp[i+1]. The answer is dp[n], not the reward of the last job.

```text
python trace_lab.py --case weighted_jobs
python trace_lab.py --case weighted_jobs --student
python verify.py --student
```

The trace executes the reference implementation or your implementation on the table's three jobs. Observe ordered, compatible, and dp. Sorting costs O(n log n); all predecessor scans total 0+1+...+(n−1), so this implementation takes O(n²) time. The sorted outer list and dp array occupy O(n) extra space; the returned number is O(1). No job record is changed.

For an independent check on n≤12, enumerate the <math xmlns="http://www.w3.org/1998/Math/MathML"><msup><mn>2</mn><mi>n</mi></msup></math> subsets, sort each selected subset by time, reject overlapping neighbors, and compare the best reward. This slower checker uses O(<math xmlns="http://www.w3.org/1998/Math/MathML"><msup><mn>2</mn><mi>n</mi></msup></math> n log n) time and O(n) working storage when subsets are processed one at a time. Test touching endpoints, identical intervals, zero rewards, and an example where the largest individual reward loses to two compatible jobs. Explain why selecting the earliest-finishing job alone is insufficient for weighted rewards.

Return to the original three-job assessment and write its own state table. For the selected LeetCode task, use the relevant [Week 5](/courses/practical-algorithms/week-05-practice/), [Week 6](/courses/practical-algorithms/week-06-practice/), or [Week 7](/courses/practical-algorithms/week-07-practice/) input contract and trace, then create a different test input.

<!-- ko -->

## 독립 문제 선택

[200](https://leetcode.com/problems/number-of-islands/), [322](https://leetcode.com/problems/coin-change/), [56](https://leetcode.com/problems/merge-intervals/), [207](https://leetcode.com/problems/course-schedule/) 중 하나를 선택합니다. 원문 조건을 읽고 이전에 본 문제인지 기록한 뒤 코드·정당성·복잡도·경계 검사를 제출합니다.

## 작업 선택 문제

입력은 [시작,끝,보상] 형태의 작업 1..12개입니다. 시간은 정수 0..30, 시작<끝, 보상 0..20입니다. 서로 겹치지 않게 선택한 최대 보상 합을 반환합니다. 끝점이 닿는 작업과 빈 선택은 허용하며 입력은 변경하지 않습니다. 예: [[0,2,3],[2,4,3],[0,4,10]] → 10.

함수, 모든 선택 경우를 포괄하는 근거, 시간·공간 비용, 독립적으로 확인한 작은 입력을 제출합니다.

## 작은 작업 일정부터 따라가기

A=[0,2,4], B=[2,3,3], C=[1,4,8]을 사용합니다. A가 끝날 때 B가 시작하므로 둘을 함께 수행하면 보상이 7입니다. C는 각각과 겹치며 보상은 8입니다. 알고리즘을 고르기 전에 작업이 차지하는 반열린 구간 [시작,끝)을 그려보세요.

끝 시각으로 정렬해 접두 구간을 만듭니다. dp[i]를 앞의 i개 작업만으로 얻는 최대 보상으로 정의하고 dp[0]=0으로 빈 선택을 허용합니다. 현재 작업을 건너뛰면 앞선 최댓값을 유지합니다. 선택하면 그 보상에 현재 시작 시각까지 끝나는 작업들의 최적 보상을 더합니다. 모든 유효한 선택은 이 두 경우 중 하나입니다.

| 작업 | 호환되는 앞쪽 구간 길이 | 건너뛰기 | 선택하기 | 새 최댓값 |
| --- | --- | --- | --- | --- |
| A: [0,2,4] | 0 | 0 | 4+0=4 | 4 |
| B: [2,3,3] | 1 | 4 | 3+4=7 | 7 |
| C: [1,4,8] | 0 | 7 | 8+0=8 | 8 |

`student_week_08.py`의 `weighted_jobs(jobs)`를 구현합니다. 입력을 보존하도록 sorted(jobs, key=...)를 사용합니다. 각 작업에서 앞선 작업을 훑어 마지막 호환 작업을 찾고, 0부터 센 인덱스를 접두 구간 길이로 바꿉니다. 선택한 경우의 보상을 계산한 뒤 dp[i+1]을 씁니다. 답은 마지막 작업 자체의 보상이 아니라 dp[n]입니다.

```text
python trace_lab.py --case weighted_jobs
python trace_lab.py --case weighted_jobs --student
python verify.py --student
```

위 표의 세 작업으로 제공 풀이 또는 본인 코드의 실행을 추적합니다. ordered, compatible, dp를 관찰하세요. 정렬은 O(n log n), 앞쪽 탐색은 총 0+1+...+(n−1)회이므로 이 구현의 시간은 O(n²)입니다. 정렬한 바깥 list와 dp 배열은 O(n) 추가 공간, 반환 숫자는 O(1) 공간을 씁니다. 작업 레코드는 수정하지 않습니다.

n≤12의 독립 검사는 <math xmlns="http://www.w3.org/1998/Math/MathML"><msup><mn>2</mn><mi>n</mi></msup></math>개 부분집합을 열거해 선택한 작업을 시간순으로 정렬하고, 이웃 구간이 겹치면 버린 뒤 최대 보상을 비교합니다. 이 느린 검사는 O(<math xmlns="http://www.w3.org/1998/Math/MathML"><msup><mn>2</mn><mi>n</mi></msup></math> n log n) 시간, 부분집합을 하나씩 처리하면 O(n) 작업 공간을 씁니다. 끝점 접촉, 같은 구간, 보상 0, 보상이 가장 큰 작업 하나보다 호환되는 두 작업이 유리한 경우를 확인하세요. 보상이 있을 때 가장 먼저 끝나는 작업만 고르면 충분하지 않은 이유도 설명합니다.

원래 평가의 세 작업으로 돌아가 별도 상태표를 작성하세요. 선택한 LeetCode 문제는 [5주차](/courses/practical-algorithms/week-05-practice/), [6주차](/courses/practical-algorithms/week-06-practice/), [7주차](/courses/practical-algorithms/week-07-practice/)의 입력 조건과 추적을 사용하고 다른 검사 입력을 직접 만듭니다.
