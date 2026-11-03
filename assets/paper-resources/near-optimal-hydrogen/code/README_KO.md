# 그린수소 준최적 설계영역 탐색 코드

Sunwoo Kim·Joungho Park의 논문 **Exploring near-optimal green hydrogen design
regions: Geometric error bounds and finite termination**을 재현하기 위한 코드입니다.
2026년 11월 3일 arXiv eess.SY에 제출했으며, 공개 식별자는 발표 후 추가합니다.

[English](README.md) · [홈페이지 코드 안내](https://sunboogermany.github.io/paper-resources/near-optimal-hydrogen/)

제안 방법은 외부 꼭짓점의 거리 LP와 축소된 최근접 설계 LP로 4차원 설계영역을 탐색합니다.
연간 생산 컷과 순환 저장 컷으로 최근접 설계 LP의 시간별 운전변수를 제거하고, 정수 풍력터빈
대수의 단면을 별도로 복원합니다. 제주·텍사스의 실제 입력, 기준 결과와 ORACLE·G-ORACLE
비교 구현을 포함합니다.

## 설치와 실행 확인

Python **3.12**를 사용하고 ZIP을 푼 폴더에서 실행합니다. Word·EndNote·MATLAB이나
상용 솔버는 필요하지 않습니다. requirements.txt는 검증한 수치 라이브러리 버전입니다.

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

demo는 짧은 합성 입력을 사용한 실행 확인입니다. 원고 결과가 아닙니다.
마지막 명령은 보존한 실측값으로 `outputs/performance/table4.csv`와 Fig. 7·8의
PNG/PDF/SVG를 만듭니다. 시간을 다시 측정하거나 보정하지 않습니다.

## 연간 사례 비교

```bash
python -m pem_planning benchmark --case jeju_1pct --method proposed --output outputs/jeju_1pct_proposed
python -m pem_planning benchmark --case jeju_1pct --method g-oracle --output outputs/jeju_1pct_g_oracle
python -m pem_planning benchmark --case jeju_1pct --method oracle --output outputs/jeju_1pct_oracle
```

사례는 `jeju_1pct`, `jeju_2pct`, `texas_1pct`, `texas_2pct`입니다. 각 지역의
2022–2024년 풍력·PV를 같은 연도끼리 사용하며, 실제 2월 29일을 제외한 연간 8,760시간을
모두 유지합니다. 솔버는 1스레드, 정규화 종료 허용오차는 0.01입니다. ORACLE 거리 MILP의
상대 최적성 갭은 0.1%입니다. G-ORACLE은 시간별 최근접 설계 LP를 유지하며 선택적인
비용 컷은 사용하지 않았습니다.

기본 실행은 보존한 공통 초기화와 그때 측정한 초기화 시간을 사용합니다.
`--fresh-initialization`을 추가하면 초기화부터 새로 계산하고 시간을 측정합니다.
새 결과는 지정한 출력 폴더에 저장합니다. ORACLE·G-ORACLE은 제안 방법보다 오래 걸릴 수
있으며, 다른 컴퓨터나 라이브러리 버전에서 같은 실행시간이 나올 것을 가정하지 않습니다.

G-ORACLE이 시간별 솔버의 누적 제한시간에 도달해 멈추면 같은 명령에 `--resume`을
추가하여 이어 계산할 수 있습니다. 저장된 상태와 이전 계산시간을 모두 유지합니다.
재개 후 캐시 카운터는 새 구간에 해당하며, 논문의 가속비에는 누적 전체 시간을 사용합니다.

## 기본 설계영역과 가격 민감도

```bash
python -m pem_planning.pwl_two_region_study --output outputs/case_study
python -m pem_planning.pwl_cost_sensitivity --output outputs/price_sensitivity
```

`restricted_design_choices.py`와 `sequential_project_decisions.py`는 4.4절의 부지·조달
제약 질의를 담고 있습니다. 보존된 입력과 결과는 `results/`에 있습니다. 이 두 스크립트를
다시 계산할 때는 새 출력 폴더를 지정하십시오. 독립적인 전체 시간별 모형은
`pwl_planning.py`에 있습니다.

## 선택 기능: 거리 재사용

```bash
python -m pem_planning benchmark --case jeju_1pct --method cached --output outputs/jeju_1pct_cached
```

기존 지지초평면 인증이 유효할 때만 꼭짓점의 이전 거리 값을 재사용합니다. 완전한 Qhull
꼭짓점 열거와 제안 방법의 축소된 최근접 설계 LP는 유지합니다. 시간 측정이 끝난 뒤 모든
저장 거리를 새 LP와 대조합니다. **제출 원고의 시간·그림·Table 4에는 이 후속 구현 실험을
사용하지 않았습니다.** 퇴화 LP와 거의 같은 최대거리 꼭짓점 때문에 탐색 경로가 조금 달라질
수 있습니다.

## 수치 결과와 모형 범위

`reference_results/performance/`에는 제출 원고에 사용한 기존 ORACLE·제안 방법 실측값과
보정 없는 G-ORACLE 실측값이 있습니다. 가속비는 공통 초기화와 탐색 단계를 포함한
**비교 방법의 전체 탐색시간 / 제안 방법의 전체 탐색시간**입니다. LP 한 번의 시간비가 아닙니다.
G-ORACLE은 독립적인 Python 구현이며 원저자의 수정 cddlib 배포본이 아닙니다.

선택한 생산곡선은 원점을 지나는 오목 PWL 계획 모형이며 비선형 전해조의 물리적 하한을
보장하는 곡선이 아닙니다. 구현은 부동소수점 LP/MIP 및 기하 허용오차를 사용합니다.
정확 연산 가정의 수학적 증명을 구간 연산으로 구현한 코드는 아닙니다.

## 라이선스와 출처

Copyright (c) 2026 Sunwoo Kim. PICNN 코드와 같은 비상업 연구용 조건을 적용합니다.
상업적 사용은 사전 서면 허가가 필요합니다. [라이선스 전문](LICENSE.md)을 확인하십시오.
ERA5 데이터는 제공기관의 자체 이용 조건을 따르며, 코드의 비상업 조건으로 제공기관이 부여한
권리를 제한하지 않습니다. [입력 설명](data/README.md)과
[외부 자료·방법 출처](THIRD_PARTY_NOTICES.md)를 함께 확인하십시오.

사용한 논문과 방법을 인용해 주십시오. ORACLE·G-ORACLE의 서지정보 및 파일별 설명은
[영문 README](README.md)에 있습니다.
