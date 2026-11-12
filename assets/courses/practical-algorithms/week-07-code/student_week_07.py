"""Week 7 implementation workspace.

Run python verify.py --student after completing the tasks.
Use python trace_lab.py --case FUNCTION --student to inspect states.
실습: 문제별 작은 예제를 예측한 뒤 구현하고 상태 변화를 비교합니다.
"""
from collections import deque
import heapq

def rob(nums):
    """At each house compare skip=current_best with take=best_two_back+value. Compute the new best before shifting the two states. Prefix optima are 2,7,11,11,12; the last answer selects 2+9+1.

    각 집에서 건너뛴 값 current_best와 선택한 값 best_two_back+value를 비교합니다. 새 최댓값을 구한 뒤 두 상태를 옮깁니다. 접두 구간의 답은 2,7,11,11,12이며 마지막 답은 2+9+1입니다.
    Example: rob([2, 7, 9, 3, 1],) => 12
    """
    raise NotImplementedError("Implement the exercise")

def coin_change(coins, amount):
    """Let dp[a] be the minimum coins for amount a; set dp[0]=0 and other entries unreachable. Evaluate increasing amounts from smaller predecessors. The table is 0,1,2,1,1,2,2; 3+3 beats greedy 4+1+1.

    dp[a]를 금액 a의 최소 동전 수로 정의하고 dp[0]=0, 나머지는 도달 불가로 둡니다. 작은 금액부터 채웁니다. 표는 0,1,2,1,1,2,2이며 3+3이 greedy의 4+1+1보다 낫습니다.
    Example: coin_change([1, 3, 4], 6) => 2
    """
    raise NotImplementedError("Implement the exercise")

def unique_paths(rows, cols):
    """A cell receives paths from above and left. In a one-row buffer, dp[col] still means above while dp[col-1] already means left. Rows become [1,1,1,1], [1,2,3,4], [1,3,6,10].

    한 칸으로는 위와 왼쪽에서 들어옵니다. 한 행 버퍼에서 dp[col]은 아직 위쪽 값이고 dp[col-1]은 갱신된 왼쪽 값입니다. 행은 [1,1,1,1], [1,2,3,4], [1,3,6,10]으로 바뀝니다.
    Example: unique_paths(3, 4) => 10
    """
    raise NotImplementedError("Implement the exercise")

def lcs(first, second):
    """Define dp[i][j] for the two prefixes. Equal final characters extend the diagonal by one; unequal characters take the larger value after dropping one final character. Highlight the a,c,e diagonal extensions.

    두 접두 문자열의 답을 dp[i][j]로 정의합니다. 끝 문자가 같으면 대각선 값에 1을 더하고, 다르면 한쪽 끝 문자를 뺀 두 값 중 큰 것을 택합니다. a,c,e가 답을 늘리는 칸을 표시하세요.
    Example: lcs('abcde', 'ace') => 3
    """
    raise NotImplementedError("Implement the exercise")
