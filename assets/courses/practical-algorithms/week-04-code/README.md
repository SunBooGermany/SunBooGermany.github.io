# Week 4: Tree recursion, BFS, and BSTs

Python 3.11+; standard library only. From the extracted `code` directory:

```text
python demo_07.py
python demo_08.py
python verify.py
python verify.py --student
```

Implement `student_week_04.py` before the last command. Completed solutions are separate in `solutions.py`. `depth_recursive` is for small trees; use the iterative `max_depth` on long chains. Inputs are acyclic binary trees with no shared child objects. BST ordering is strict; `kth_smallest` requires a valid BST and 1 <= k <= n. The input adapter uses level-order values and `None` for absent children. Algorithms preserve input links.

## 4주차: 트리 재귀·BFS·BST

Python 3.11 이상과 표준 라이브러리를 사용합니다. 압축을 푼 `code` 폴더에서 위 명령을 실행합니다. 마지막 명령은 `student_week_04.py`를 구현한 뒤 실행합니다. 완성 풀이는 `solutions.py`에 분리되어 있습니다.

`depth_recursive`는 작은 트리의 설명용이며 긴 연결 모양 트리에는 반복형 `max_depth`를 사용합니다. 입력은 사이클이나 공유 자식이 없는 이진 트리입니다. BST는 엄격한 순서를 따르며 `kth_smallest`는 유효한 BST와 1 <= k <= n을 전제로 합니다. 입력 변환은 레벨 순서와 없는 자식을 나타내는 `None`을 사용합니다. 알고리즘은 입력 연결을 보존합니다.
