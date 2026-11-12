# Week 8 code / 8주차 코드

Python 3.11+; standard library only. Extract the archive and run in `code`:

```text
python demo_15.py
python demo_16.py
python verify.py
python verify.py --student
```

Implement `student_week_08.py` before using `--student`. Completed solutions are in `solutions.py`. The verifier compares small cases against independent exhaustive methods and checks large boundary inputs. Tests support debugging; the worked companion explains correctness.

Python 3.11 이상과 표준 라이브러리를 사용합니다. 압축을 푼 `code` 폴더에서 실행합니다. `--student`는 `student_week_08.py`를 구현한 뒤 사용합니다. 완성 풀이는 `solutions.py`에 분리되어 있습니다. 검사는 작은 입력의 완전 탐색 결과와 큰 경계 입력을 대조하며, 정당성은 읽기자료에서 설명합니다.

`assessment_reference.py` is the separate instructor key. Gas-station differential tests also check multiple valid starts, an extension beyond the official uniqueness guarantee. `min_jumps` requires a reachable last index.

`assessment_reference.py`는 교사용 답입니다. 주유소 검사는 공식 유일해 조건을 넘어 여러 출발점이 가능한 경우도 대조합니다. `min_jumps`는 마지막 위치 도달 가능을 전제로 합니다.
