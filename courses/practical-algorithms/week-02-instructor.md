---
layout: "course-resource"
title: "Week 2 Instructor Guide"
title_ko: "2주차 교사용 진행안"
permalink: "/courses/practical-algorithms/week-02-instructor/"
course_id: "practical-algorithms"
---

## 3: Window state and aggregate movements

Opening prompt: Find a repeat-free log interval and a shortest interval reaching a total. Recopying windows repeats work; update only incoming and outgoing data.

Flow: ask the learner to restate inputs/outputs and compare a baseline with the improved state. Reveal the lecture trace one row at a time after predictions. Execute the companion implementation and compare with a simple baseline.

### [LeetCode 3: Longest Substring Without Repeating Characters](https://leetcode.com/problems/longest-substring-without-repeating-characters/) · Medium

Reasoning: After insertion, the set represents the unique-character window. Its left boundary is the earliest feasible one for that right endpoint. Each pointer advances at most n times.

Debugging activity: A single removal on "abba" leaves b duplicated. Empty text gives 0; one space gives 1.

### [LeetCode 209: Minimum Size Subarray Sum](https://leetcode.com/problems/minimum-size-subarray-sum/) · Medium

Reasoning: Positivity makes shrinking decrease the sum. Record each valid window before shrinking. A discarded left boundary can only produce longer later windows.

Debugging activity: Outside the positive-only contract, target=3, [1,-1,3] can make this rule miss length 1.

Concept check: Does a while inside a for always imply <math xmlns="http://www.w3.org/1998/Math/MathML"><mi>O</mi><mo>(</mo><msup><mi>n</mi><mn>2</mn></msup><mo>)</mo></math>?

Instructor answer: No. Each pointer advances at most n times, so total removals and insertions are O(n).

Independent activity: implement this session’s problems in the student workspace. For correct outputs, still ask for the invariant and elimination argument. For failures, find the earliest divergent state on a small counterexample.

## 4: Stacks and subexpressions

Opening prompt: Undo and postfix evaluation consume the most recent unresolved information first. Preserve per-depth state to restore the current minimum as well.

Flow: ask the learner to restate inputs/outputs and compare a baseline with the improved state. Reveal the lecture trace one row at a time after predictions. Execute the companion implementation and compare with a simple baseline.

### [LeetCode 155: Min Stack](https://leetcode.com/problems/min-stack/) · Medium

Reasoning: Induction on depth gives the correct prefix minimum; popping the last pair restores the previous prefix minimum.

Debugging activity: Calling min over the stack costs O(d). A single current minimum loses its predecessor after a pop.

### [LeetCode 150: Evaluate Reverse Polish Notation](https://leetcode.com/problems/evaluate-reverse-polish-notation/) · Medium

Reasoning: The stack preserves completed subexpression values in order. Each operator combines the final two; a valid complete expression leaves one value.

Debugging activity: 5//-2 is -3, but truncation toward zero gives -2. Reversing operands changes subtraction.

Concept check: Does popping a repeated minimum remove every minimum?

Instructor answer: No; the previous depth retains its own minimum.

Independent activity: implement this session’s problems in the student workspace. For correct outputs, still ask for the invariant and elimination argument. For failures, find the earliest divergent state on a small counterexample.

<!-- ko -->

## 3차시: 구간 상태와 누적 이동

도입 질문: 로그에서 반복 없는 연속 구간과 일정 합을 넘는 짧은 구간을 찾습니다. 구간을 매번 복사하면 같은 데이터를 반복 처리합니다. 들어오는 값과 나가는 값만 갱신합니다.

진행: 학생에게 입력·출력을 다시 말하게 한 뒤, 아래 문제의 단순 접근과 개선 상태를 비교합니다. 강의의 상태 표를 한 행씩 가리고 다음 행을 예측하게 합니다. 읽기자료의 구현을 실행한 뒤 단순 풀이와 결과를 비교합니다.

### [LeetCode 3: Longest Substring Without Repeating Characters](https://leetcode.com/problems/longest-substring-without-repeating-characters/) · Medium

설명 근거: 추가 직후 집합은 중복 없는 현재 구간과 같습니다. 오른쪽 끝을 고정할 때 가능한 가장 왼쪽 경계를 유지하므로 그 끝의 최장 구간을 검사합니다. 두 포인터는 각각 최대 n번 이동합니다.

디버깅 활동: "abba"에서 한 번만 제거하면 b가 남아 불변식이 깨집니다. 빈 문자열은 0, 공백 한 개는 1입니다.

### [LeetCode 209: Minimum Size Subarray Sum](https://leetcode.com/problems/minimum-size-subarray-sum/) · Medium

설명 근거: 양수이므로 왼쪽을 줄이면 합이 감소합니다. 유효한 구간을 버리기 전에 길이를 기록하고 더 짧은 후보를 검사합니다. 이미 버린 왼쪽 경계는 이후 더 긴 구간만 만들므로 개선 후보가 아닙니다.

디버깅 활동: 음수 확장 반례 target=3, [1,-1,3]: 일반 축소는 길이 1을 놓칩니다. 이는 공식 양수 조건 밖의 예입니다.

이해 확인: while이 for 안에 있으면 항상 <math xmlns="http://www.w3.org/1998/Math/MathML"><mi>O</mi><mo>(</mo><msup><mi>n</mi><mn>2</mn></msup><mo>)</mo></math>인가요?

교사용 답: 아닙니다. left와 right가 각각 최대 n번 이동하므로 총 제거·추가는 O(n)입니다.

독립 활동: 주차 학생 파일에서 이번 차시 문제를 풀게 합니다. 답이 맞아도 보존되는 상태와 제거 근거를 설명하게 하고, 틀리면 가장 작은 실패 입력에서 최초로 상태가 달라진 지점을 찾게 합니다.

## 4차시: 스택과 부분식

도입 질문: 계산기의 뒤로 가기와 후위 표기 계산은 가장 최근의 미해결 정보를 먼저 사용합니다. 현재 최솟값까지 복원할 수 있게 깊이별 정보를 보존합니다.

진행: 학생에게 입력·출력을 다시 말하게 한 뒤, 아래 문제의 단순 접근과 개선 상태를 비교합니다. 강의의 상태 표를 한 행씩 가리고 다음 행을 예측하게 합니다. 읽기자료의 구현을 실행한 뒤 단순 풀이와 결과를 비교합니다.

### [LeetCode 155: Min Stack](https://leetcode.com/problems/min-stack/) · Medium

설명 근거: 빈 상태에서 시작해 새 최소를 min(value, 이전 최소)로 저장하면 귀납적으로 각 깊이의 최소가 맞습니다. pop은 마지막 쌍만 없애므로 이전 최소가 복원됩니다.

디버깅 활동: min(entries)를 호출마다 계산하면 O(d)입니다. 최소값 하나만 저장하면 최소를 pop한 뒤 이전 값을 잃습니다.

### [LeetCode 150: Evaluate Reverse Polish Notation](https://leetcode.com/problems/evaluate-reverse-polish-notation/) · Medium

설명 근거: 스택은 지금까지 끝난 부분식의 값을 왼쪽부터 보존합니다. 연산자는 마지막 두 부분식을 하나로 줄입니다. 유효한 식이 끝나면 전체 식 값 하나가 남습니다.

디버깅 활동: 5//-2는 -3이지만 0 방향 절삭은 -2입니다. left-right를 right-left로 바꾸면 뺄셈이 달라집니다.

이해 확인: 중복 최소를 pop하면 최소가 사라지나요?

교사용 답: 각 깊이에 최소를 저장하므로 이전 최소가 그대로 남습니다.

독립 활동: 주차 학생 파일에서 이번 차시 문제를 풀게 합니다. 답이 맞아도 보존되는 상태와 제거 근거를 설명하게 하고, 틀리면 가장 작은 실패 입력에서 최초로 상태가 달라진 지점을 찾게 합니다.
