"""Week 4 implementation workspace.

Run python verify.py --student after completing the tasks.
Use python trace_lab.py --case FUNCTION --student to inspect states.
실습: 문제별 작은 예제를 예측한 뒤 구현하고 상태 변화를 비교합니다.
"""
from structures import TreeNode

def max_depth(root):
    """Store (node, depth) on a stack, starting at depth 1. Update best on every pop and push children at depth+1. A three-node chain and a three-node balanced tree have different depths; draw both.

    stack에 (노드, 깊이)를 넣고 깊이 1에서 시작합니다. pop할 때 best를 갱신하고 자식을 깊이+1로 넣습니다. 노드 세 개의 사슬과 균형 트리를 그려 깊이가 다른 이유를 설명하세요.
    Example: max_depth(tree([4, 2, 7, None, 3]),) => 3
    """
    raise NotImplementedError("Implement the exercise")

def level_order(root):
    """Use deque and freeze the queue length at the start of each level. Newly appended children belong to the next level. Predict queues [4], [2,7], [3] before execution.

    deque를 사용하고 각 깊이를 시작할 때 queue 길이를 고정합니다. 새로 넣는 자식은 다음 깊이에 속합니다. 실행 전에 queue가 [4], [2,7], [3]이 되는 과정을 예측하세요.
    Example: level_order(tree([4, 2, 7, None, 3]),) => [[4], [2, 7], [3]]
    """
    raise NotImplementedError("Implement the exercise")

def valid_bst(root):
    """Carry strict lower and upper bounds from ancestors. Node 6 is less than parent 10 but lies in the right subtree of 8, so it violates (8,10). Replace 6 by 9 and predict True.

    조상에서 내려온 엄격한 하한·상한을 함께 전달합니다. 6은 부모 10보다 작지만 8의 오른쪽 후손이라 (8,10)을 위반합니다. 6을 9로 바꾸고 True가 되는 이유를 적으세요.
    Example: valid_bst(tree([8, 3, 10, None, None, 6, 12]),) => False
    """
    raise NotImplementedError("Implement the exercise")

def kth_smallest(root, k):
    """Follow left links while stacking nodes. Pop to visit the next smallest value, decrease k, then enter the right subtree. Record visits 1,2,3,4. Compare k=1 with k=7.

    왼쪽 연결을 따라 노드를 stack에 넣습니다. pop으로 다음 작은 값을 방문하고 k를 줄인 뒤 오른쪽으로 갑니다. 방문 값 1,2,3,4를 기록하고 k=1과 k=7을 비교하세요.
    Example: kth_smallest(tree([4, 2, 6, 1, 3, 5, 7]), 4) => 4
    """
    raise NotImplementedError("Implement the exercise")
