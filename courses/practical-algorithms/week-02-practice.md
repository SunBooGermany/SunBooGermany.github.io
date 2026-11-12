---
layout: "course-resource"
title: "Week 2 Student Exercises"
title_ko: "2주차 학생 실습"
permalink: "/courses/practical-algorithms/week-02-practice/"
course_id: "practical-algorithms"
---

## [LeetCode 3: Longest Substring Without Repeating Characters](https://leetcode.com/problems/longest-substring-without-repeating-characters/) · Medium

Return the maximum length of a contiguous substring without repeated characters.

0 <= n <= 10^5; letters, digits, symbols, and spaces.

## [LeetCode 209: Minimum Size Subarray Sum](https://leetcode.com/problems/minimum-size-subarray-sum/) · Medium

Return the shortest contiguous interval reaching target, or zero if none exists.

1 <= n <= 10^5; 1 <= nums[i] <= 10^4; 1 <= target <= 10^9.

## [LeetCode 155: Min Stack](https://leetcode.com/problems/min-stack/) · Medium

Implement push, pop, top, and current minimum with constant-time stack operations; explain the amortized cost of Python list updates.

Signed 32-bit values; at most 30000 calls; pop/top/getMin on nonempty stacks.

## [LeetCode 150: Evaluate Reverse Polish Notation](https://leetcode.com/problems/evaluate-reverse-polish-notation/) · Medium

Evaluate an integer expression in postfix notation, truncating division toward zero.

1..10^4 tokens; operands -200..200; +,-,*,/; valid expression, no zero divisor, signed 32-bit intermediate results.

## Submission and execution

[Download Week 2 code](/assets/courses/practical-algorithms/week-02-code.zip). Run `python verify.py --student` from the extracted code directory to check your implementation.

For each problem submit code, state meaning, correctness, complexity, and your own boundary input. Implement `student_week_02.py`. Its explicit unimplemented exceptions mark learner work and are separate from completed solutions.

When a hint is needed, open [Hints and solutions](/courses/practical-algorithms/week-02-reading/).

<!-- ko -->

## [LeetCode 3: Longest Substring Without Repeating Characters](https://leetcode.com/problems/longest-substring-without-repeating-characters/) · Medium

중복 문자가 없는 연속 부분문자열의 최대 길이를 반환합니다.

0 <= n <= 10^5; 영문자·숫자·기호·공백.

## [LeetCode 209: Minimum Size Subarray Sum](https://leetcode.com/problems/minimum-size-subarray-sum/) · Medium

합이 target 이상인 연속 구간의 최소 길이를 반환하고, 없으면 0을 반환합니다.

1 <= n <= 10^5; 1 <= nums[i] <= 10^4; 1 <= target <= 10^9.

## [LeetCode 155: Min Stack](https://leetcode.com/problems/min-stack/) · Medium

삽입·제거·맨 위 값·현재 최솟값을 상수 시간 스택 연산으로 지원합니다. Python 리스트 갱신의 상각 비용도 설명합니다.

값은 signed 32-bit; 최대 30000회 호출; pop/top/getMin은 비어 있지 않을 때만 호출.

## [LeetCode 150: Evaluate Reverse Polish Notation](https://leetcode.com/problems/evaluate-reverse-polish-notation/) · Medium

후위 표기 정수 식을 계산하며 나눗셈은 0 방향으로 절삭합니다.

1 <= 토큰 수 <= 10^4; 피연산자 -200..200; +,-,*,/; 유효한 식·0 나눗셈 없음·중간 결과 signed 32-bit.

## 제출과 실행

[2주차 코드](/assets/courses/practical-algorithms/week-02-code.zip)를 내려받습니다. 압축을 푼 code 폴더에서 `python verify.py --student`를 실행하면 작성한 풀이를 검사합니다.

각 문제에 코드, 상태의 의미, 정당성, 시간·공간 분석, 직접 만든 경계 입력을 제출합니다. `student_week_02.py`에 풀이를 작성합니다. 실습 파일의 미구현 예외는 학생이 채우는 자리이며 완성 해설과 분리되어 있습니다.

힌트가 필요할 때만 [힌트·해설](/courses/practical-algorithms/week-02-reading/)을 확인합니다.