# 그린수소 준최적 설계영역 탐색 코드

Sunwoo Kim·Joungho Park의 논문 **Exploring near-optimal green hydrogen design
regions: Geometric error bounds and finite termination**을 재현하기 위한 코드입니다.
2026년 11월 3일 arXiv eess.SY에 제출했습니다.

[English](README.md) · [홈페이지 코드 안내](https://sunboogermany.github.io/paper-resources/near-optimal-hydrogen/)

제안 방법은 외부 꼭짓점의 거리 LP와 축소된 최근접 설계 LP로 4차원 설계영역을 탐색합니다.
연간 생산 컷과 순환 저장 컷으로 최근접 설계 LP의 시간별 운전변수를 제거하고, 정수 풍력터빈
대수의 단면을 별도로 복원합니다. 제주·텍사스의 실제 입력, 기준 결과와 ORACLE·G-ORACLE
비교 구현을 포함합니다.

## 설치와 실행

Python **3.12**에서 ZIP을 푼 폴더로 이동한 뒤 실행합니다.

```bash
python -m venv .venv
# Windows: .venv\Scripts\activate
# Linux/macOS: source .venv/bin/activate
python -m pip install -r requirements.txt
python -m pem_planning demo --output outputs/demo
python -m unittest pem_planning.test_pwl_capacity_oracle pem_planning.test_oracle_matched_benchmark pem_planning.test_g_oracle_benchmark
python scripts/check_release.py
python scripts/reproduce_performance.py
```

## 연간 사례 비교

```bash
python -m pem_planning benchmark --case jeju_1pct --method proposed --output outputs/jeju_1pct_proposed
python -m pem_planning benchmark --case jeju_1pct --method g-oracle --output outputs/jeju_1pct_g_oracle
python -m pem_planning benchmark --case jeju_1pct --method oracle --output outputs/jeju_1pct_oracle
```

사례는 `jeju_1pct`, `jeju_2pct`, `texas_1pct`, `texas_2pct`입니다. 각 지역의
2022–2024년 풍력·PV를 같은 연도끼리 사용하며, 2월 29일을 제외한 연간 8,760시간을
사용합니다. 솔버는 1스레드, 정규화 종료 허용오차는 0.01입니다. ORACLE 거리 MILP의
상대 최적성 갭은 0.1%입니다. G-ORACLE의 최근접 설계 LP는 시간별 운전변수를 포함하며,
비용 컷 옵션은 비활성화한 설정입니다.

기본 실행은 보존한 공통 초기화와 그때 측정한 초기화 시간을 사용합니다.
`--fresh-initialization`을 추가하면 초기화부터 새로 계산하고 시간을 측정합니다.

G-ORACLE이 시간별 솔버의 누적 제한시간에 도달해 멈추면 같은 명령에 `--resume`을
추가하여 이어 계산할 수 있습니다. 저장된 상태에서 계산을 이어가며 실행시간도 누적합니다.

## 기본 설계영역과 가격 민감도

```bash
python -m pem_planning.pwl_two_region_study --output outputs/case_study
python -m pem_planning.pwl_cost_sensitivity --output outputs/price_sensitivity
```

`restricted_design_choices.py`와 `sequential_project_decisions.py`는 4.4절의 부지·조달
제약 질의를 담고 있습니다. 입력과 결과는 `results/`에 있으며, 다시 계산할 때는 새 출력 폴더를 지정합니다.
전체 시간별 모형은
`pwl_planning.py`에 있습니다.

## 선택 기능: 거리 재사용

```bash
python -m pem_planning benchmark --case jeju_1pct --method cached --output outputs/jeju_1pct_cached
```

후속 실험용 옵션으로, 지지초평면 인증이 유효한 꼭짓점의 거리 값을 재사용합니다.
Qhull 꼭짓점 열거와 축소된 최근접 설계 LP를 사용하며, 실행 후 저장 거리를 새 LP와
대조합니다. 퇴화 LP나 최대거리가 거의 같은 꼭짓점에서는 탐색 경로가 달라질 수 있습니다.

## 수치 결과와 모형 범위

`reference_results/performance/`에는 제출 원고의 Table 4와 Fig. 7·8에 사용한
ORACLE·제안 방법·G-ORACLE의 측정 결과가 있습니다. 가속비는 공통 초기화와 탐색 단계를
포함한 **비교 방법의 전체 탐색시간 / 제안 방법의 전체 탐색시간**으로 계산합니다.
G-ORACLE은 Python으로 독립 구현했습니다.

생산곡선은 원점을 지나는 오목 PWL 계획 모형이며, 계산에는 부동소수점 LP/MIP와
기하 허용오차를 사용합니다.

## 라이선스와 출처

Copyright (c) 2026 Sunwoo Kim. 비상업적 연구 목적으로 이용할 수 있으며,
상업적 사용에는 사전 서면 허가가 필요합니다. [라이선스 전문](LICENSE.md)을 확인하십시오.
ERA5 데이터에는 제공기관의 이용 조건이 적용됩니다. [입력 설명](data/README.md)과
[외부 자료·방법 출처](THIRD_PARTY_NOTICES.md)를 함께 확인하십시오.

사용한 논문과 방법을 인용해 주십시오. ORACLE·G-ORACLE의 서지정보 및 파일별 설명은
[영문 README](README.md)에 있습니다.
