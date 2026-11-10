# Week 2: Sliding windows and stacks

Use Python 3.11 or later; no third-party packages are required. Run commands from the extracted `code` directory.

```text
python demo_03.py
python demo_04.py
python verify.py
```

Implement `student_week_02.py` independently, then run `python verify.py --student`. The initial `NotImplementedError` exceptions mark the exercises to complete. `solutions.py` contains the separate worked solutions. The checks compare against exhaustive small-input baselines and test boundary inputs, independent stack objects, and operand order. They do not replace a correctness argument.

The fixed-width helper returns all window sums and rejects widths outside 1..n. Its initial slice uses O(w) temporary storage; its returned list uses O(n-w+1) storage. LeetCode 209 requires positive inputs. `MinStack.pop`, `top`, and `getMin` require a nonempty stack. RPN inputs must be valid expressions without division by zero; division truncates toward zero.

For LeetCode submission, adapt the function names to `lengthOfLongestSubstring(self, s)`, `minSubArrayLen(self, target, nums)`, and `evalRPN(self, tokens)` inside `class Solution`. `MinStack` already uses the required public methods.

Official problems: [3](https://leetcode.com/problems/longest-substring-without-repeating-characters/), [209](https://leetcode.com/problems/minimum-size-subarray-sum/), [155](https://leetcode.com/problems/min-stack/), [150](https://leetcode.com/problems/evaluate-reverse-polish-notation/).

## 2주차: 슬라이딩 윈도우와 스택

Python 3.11 이상과 표준 라이브러리만 사용합니다. 압축을 푼 `code` 폴더에서 위 명령을 실행합니다.

`student_week_02.py`에 직접 구현한 뒤 `python verify.py --student`로 검사합니다. 처음의 `NotImplementedError`는 채워야 할 실습 위치입니다. `solutions.py`에는 별도의 완성 풀이가 있습니다. 검증은 작은 입력의 완전 탐색 결과와 비교하고 경계 입력, 스택 객체의 독립성, 피연산자 순서를 검사합니다. 정당성 설명은 별도로 작성합니다.

고정 폭 함수는 모든 구간 합을 반환하며 1..n 범위 밖의 폭은 거부합니다. 초기 슬라이스는 O(w) 임시 공간, 반환 리스트는 O(n-w+1) 공간을 사용합니다. LeetCode 209의 입력은 양수여야 합니다. `MinStack`의 `pop`, `top`, `getMin`은 스택이 비어 있지 않을 때 호출합니다. RPN 입력은 0 나눗셈이 없는 유효한 식이며 나눗셈은 0 방향으로 절삭합니다.

LeetCode에 제출할 때는 `class Solution` 안에서 위의 공식 메서드 이름과 매개변수로 연결합니다. `MinStack`은 제공된 메서드 이름을 그대로 사용합니다.
