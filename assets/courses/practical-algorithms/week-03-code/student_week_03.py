"""Week 3 implementation workspace.

Run python verify.py --student after completing the tasks.
Use python trace_lab.py --case FUNCTION --student to inspect states.
실습: 문제별 작은 예제를 예측한 뒤 구현하고 상태 변화를 비교합니다.
"""
from structures import ListNode

def search_matrix(matrix, target):
    """Treat the ordered matrix as six virtual positions. Convert midpoint with divmod(mid, column_count), without flattening a new list. Search 8 next and record when the inclusive interval becomes empty.

    정렬된 행렬을 여섯 개의 가상 위치로 봅니다. 새 list를 만들지 않고 divmod(mid, 열 수)로 행·열을 구합니다. 8도 탐색해 양 끝을 포함한 구간이 언제 비는지 기록하세요.
    Example: search_matrix([[1, 3, 5], [7, 9, 11]], 9) => True
    """
    raise NotImplementedError("Implement the exercise")

def search_rotated(nums, target):
    """Check which half is ordered, then whether target lies within that half. Update one boundary beyond mid. Repeat for missing target 3 and explain the -1 result. Distinct values make the ordered-half test decisive.

    어느 절반이 정렬됐는지 확인한 뒤 그 구간에 target이 있는지 검사합니다. 한쪽 경계를 mid 너머로 옮깁니다. 없는 값 3을 탐색하고 -1을 설명하세요. 값이 서로 다르다는 조건이 절반 판정을 가능하게 합니다.
    Example: search_rotated([4, 5, 6, 7, 0, 1, 2], 0) => 4
    """
    raise NotImplementedError("Implement the exercise")

def reverse_list(head):
    """Save current.next before rewriting it to previous. Then advance previous and current. Draw 2→5→8, then 2→None with current at 5. Check that the reversed chain ends at None.

    current.next를 저장한 뒤 previous를 향하도록 바꿉니다. 그다음 previous와 current를 전진시킵니다. 2→5→8에서 2→None, current=5가 되는 모습을 그리세요. 뒤집은 연결의 끝이 None인지 확인합니다.
    Example: reverse_list(linked([2, 5, 8]),) => [8, 5, 2]
    """
    raise NotImplementedError("Implement the exercise")

def merge_lists(first, second):
    """Use a dummy node and a tail. Attach the smaller head and advance only that input. Once one list ends, attach the remaining chain. Compare duplicate values and an empty input.

    dummy 노드와 tail을 둡니다. 두 head 중 작은 노드를 붙이고 해당 입력만 전진시킵니다. 한 list가 끝나면 남은 연결을 통째로 붙입니다. 같은 값과 빈 입력도 비교하세요.
    Example: merge_lists(linked([1, 3]), linked([2, 4])) => [1, 2, 3, 4]
    """
    raise NotImplementedError("Implement the exercise")
