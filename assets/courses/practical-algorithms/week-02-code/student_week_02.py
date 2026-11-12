"""Week 2 implementation workspace.

Run python verify.py --student after completing the tasks.
Use python trace_lab.py --case FUNCTION --student to inspect states.
실습: 문제별 작은 예제를 예측한 뒤 구현하고 상태 변화를 비교합니다.
"""

def longest_unique(text):
    """Keep a left boundary and last-seen indices. A repeated character moves left to max(left, previous+1). The last a must not move left backward. Compare abba with abca.

    왼쪽 경계와 문자별 마지막 위치를 둡니다. 중복 문자를 만나면 left를 max(left, 이전 위치+1)로 바꿉니다. 마지막 a에서 경계가 뒤로 돌아가면 안 됩니다. abba와 abca를 비교하세요.
    Example: longest_unique('abba',) => 2
    """
    raise NotImplementedError("Implement the exercise")

def min_subarray(target, nums):
    """Extend the right end and add its value. While sum meets the target, record the length and remove the left value. At the final 3, the valid window [4,3] has length 2. Explain why positive inputs make shrinking safe.

    오른쪽 값을 합에 더합니다. 합이 target 이상인 동안 길이를 기록하고 왼쪽 값을 뺍니다. 마지막 3을 읽으면 [4,3]의 길이 2를 얻습니다. 양수 조건 덕분에 줄이기가 가능한 이유를 설명하세요.
    Example: min_subarray(7, [2, 3, 1, 2, 4, 3]) => 2
    """
    raise NotImplementedError("Implement the exercise")

class MinStack:
    """Push 2,1,1; query the minimum, pop, query, pop, query. Store the minimum so far with each value. Both copies of 1 need their own minimum record; the three queried minima are 1,1,2.

    2,1,1을 push한 뒤 최솟값 조회, pop, 조회, pop, 조회를 실행합니다. 각 값과 그때까지의 최솟값을 함께 저장합니다. 두 1 모두 최솟값 기록을 가져야 하며 조회 결과는 1,1,2입니다.
    Example: MinStack() => [1, 1, 2]
    """
    def __init__(self):
        raise NotImplementedError("Implement the exercise")
    def push(self, val):
        raise NotImplementedError("Implement the exercise")
    def pop(self):
        raise NotImplementedError("Implement the exercise")
    def top(self):
        raise NotImplementedError("Implement the exercise")
    def getMin(self):
        raise NotImplementedError("Implement the exercise")

def rpn(tokens):
    """Read tokens left to right. For an operator, pop the right operand before the left operand. Division truncates toward zero: 7 / -3 becomes -2. Compare Python floor division, which gives -3.

    토큰을 왼쪽부터 읽습니다. 연산자를 만나면 오른쪽 피연산자를 먼저 pop하고 왼쪽을 다음에 꺼냅니다. 7 / -3은 0 방향으로 잘라 -2입니다. -3이 나오는 Python 내림 나눗셈과 비교하세요.
    Example: rpn(['7', '-3', '/'],) => -2
    """
    raise NotImplementedError("Implement the exercise")
