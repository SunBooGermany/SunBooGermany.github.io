"""Week 1 implementation workspace.

Run python verify.py --student after completing the tasks.
Use python trace_lab.py --case FUNCTION --student to inspect states.
실습: 문제별 작은 예제를 예측한 뒤 구현하고 상태 변화를 비교합니다.
"""

def two_sum(nums, target):
    """For each value, compute target minus value. Look up that complement in a dictionary of earlier indices, then store the current index. Test [3,3] with target 6 to check that the two indices differ.

    현재 값마다 target에서 그 값을 뺍니다. 이전 인덱스를 담은 dictionary에서 필요한 값을 찾은 뒤 현재 인덱스를 저장합니다. [3,3], target=6으로 두 인덱스가 서로 다른지 확인하세요.
    Example: two_sum([4, 8, 3], 7) => [0, 2]
    """
    raise NotImplementedError("Implement the exercise")

def nearby_duplicate(nums, k):
    """Store the most recent index for each value. Compare the index distance before replacing it. At index 3, the preceding 4 is at index 2, not index 0. Change k to 0 and explain False.

    값마다 가장 최근 인덱스를 저장합니다. 인덱스 차이를 비교한 뒤 기록을 갱신합니다. 인덱스 3에서 직전 4의 위치는 0이 아니라 2입니다. k를 0으로 바꾸고 False인 이유를 설명하세요.
    Example: nearby_duplicate([4, 7, 4, 4], 1) => True
    """
    raise NotImplementedError("Implement the exercise")

def two_sum_sorted(numbers, target):
    """Start at both ends. If the sum is too large, move the right pointer left; if too small, move the left pointer right. Track sums 10 then 7. Convert zero-based positions to the required one-based answer.

    양 끝에서 시작합니다. 합이 크면 오른쪽 포인터를 왼쪽으로, 작으면 왼쪽 포인터를 오른쪽으로 옮깁니다. 합이 10에서 7로 바뀌는 과정을 적고, 0부터 센 위치를 문제에서 요구하는 1부터 센 인덱스로 바꾸세요.
    Example: two_sum_sorted([1, 4, 6, 9], 7) => [1, 3]
    """
    raise NotImplementedError("Implement the exercise")

def three_sum(nums):
    """Sort, fix one value, and find its opposite using two pointers. Skip equal fixed values and equal pointer values after a match. Try [0,0,0,0]: four indices produce only one distinct value triple.

    정렬한 뒤 값 하나를 고정하고 나머지 두 값의 합을 포인터로 찾습니다. 고정 값이 반복되거나 답을 찾은 뒤 포인터 값이 반복되면 건너뜁니다. [0,0,0,0]에서 서로 다른 값의 조합이 하나만 나와야 하는 이유를 설명하세요.
    Example: three_sum([-2, 0, 1, 1, 2],) => [[-2, 0, 2], [-2, 1, 1]]
    """
    raise NotImplementedError("Implement the exercise")
