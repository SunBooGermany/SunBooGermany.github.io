# 그린수소 준최적 설계영역 탐색 코드

그린수소 시스템의 4차원 준최적 설계영역을 탐색하고 제안 방법을 ORACLE·G-ORACLE과
비교합니다. 최적화에는 HiGHS LP/MIP 솔버를 사용하며, 제주·텍사스의 2022–2024년
시간별 입력은 `data/era5/`에 포함되어 있습니다.

[English](README.md)

## 이용 조건

Copyright (c) 2026 Sunwoo Kim. 비상업적 연구 목적으로만 사용·복제·수정·공유할 수
있습니다. 기업 내부 연구개발, 유료 자문, 상용 제품·서비스 개발을 포함한 상업적
이용에는 Sunwoo Kim의 사전 서면 허가가 필요합니다. 재배포할 때는 저작권 고지와
동일한 이용 조건을 유지해야 하며, 외부 라이브러리·데이터에는 각 권리자의 조건이
적용됩니다. 전체 조건은 [라이선스](LICENSE.md)에 명시되어 있습니다.

## 설치와 평가

Python 3.12에서 이 폴더를 기준으로 실행합니다.

```bash
python -m venv .venv
# Windows: .venv\Scripts\activate
# Linux/macOS: source .venv/bin/activate
python -m pip install -r requirements.txt

# 합성 입력으로 짧은 실행 확인
python -m pem_planning demo --output outputs/demo

# 저장된 결과로 Table 4와 Fig. 7·8 재구성
python scripts/reproduce_performance.py
```

## 설계영역 탐색

```bash
# 제주 1% 사례에 제안 방법 적용
python -m pem_planning benchmark --case jeju_1pct --method proposed --output outputs/jeju_1pct_proposed

# 기본 설계, 설계영역과 가격 민감도 계산
python -m pem_planning.pwl_two_region_study --output outputs/case_study
python -m pem_planning.pwl_cost_sensitivity --output outputs/price_sensitivity
```

`--case`는 `jeju_1pct`, `jeju_2pct`, `texas_1pct`, `texas_2pct`를 지원합니다.
비교 실험은 저장된 공통 초기화와 당시 측정한 초기화 시간을 사용하며,
`--fresh-initialization`을 추가하면 초기화부터 새로 계산하고 시간을 측정합니다.

`restricted_design_choices.py`와 `sequential_project_decisions.py`는 4.4절의
부지·조달 제약 질의를 계산합니다. 입력과 결과는 `results/`에 있으며, 다시 계산할
때는 새 출력 폴더를 지정합니다.

거리 재사용 옵션은 후속 실험용입니다. 지지초평면 인증이 유효한 꼭짓점의 거리 값을
재사용하며, 실행 후 저장 거리를 새 LP와 대조합니다.

```bash
python -m pem_planning benchmark --case jeju_1pct --method cached --output outputs/jeju_1pct_cached
```

## ORACLE·G-ORACLE 비교

```bash
python -m pem_planning benchmark --case jeju_1pct --method g-oracle --output outputs/jeju_1pct_g_oracle
python -m pem_planning benchmark --case jeju_1pct --method oracle --output outputs/jeju_1pct_oracle
```

ORACLE은 KKT 기반 MILP로 거리를 평가합니다. G-ORACLE은 꼭짓점 LP와 시간별
운전변수를 포함한 최근접 설계 LP를 사용하며, 비용 컷 옵션은 비활성화한 설정입니다.
두 방법 모두 비교 실험을 위해 Python으로 독립 구현했습니다.

G-ORACLE이 시간별 솔버의 누적 제한시간에 도달해 멈추면 같은 명령에 `--resume`을
추가하여 이어 계산합니다. 저장된 상태에서 재개하며 실행시간도 누적합니다.

## 모델 조건

각 지역의 2022–2024년 기상자료에서 풍력·PV를 같은 연도끼리 사용합니다.
2월 29일을 제외한 연간 시간 수는 8,760시간이며, 생산곡선은 원점을 지나는
오목 PWL 계획 모형입니다.

제안 방법은 꼭짓점의 거리 LP와 축소된 최근접 설계 LP를 결합합니다. 연간 생산 컷과
순환 저장 컷으로 최근접 설계 LP의 시간별 운전변수를 제거하고, 정수 풍력터빈 대수의
단면을 별도로 복원합니다. 전체 시간별 모형은 `pwl_planning.py`에 있습니다.

솔버는 1스레드, 정규화 종료 허용오차는 0.01이며, ORACLE 거리 MILP의 상대 최적성
갭은 0.1%입니다. 계산에는 부동소수점 LP/MIP와 기하 허용오차를 사용합니다.

## 저장된 결과

`reference_results/performance/`에는 Table 4와 Fig. 7·8에 사용한 ORACLE·제안 방법·
G-ORACLE의 측정 결과가, `results/`에는 사례 분석 결과가 있습니다. 가속비는 공통
초기화와 탐색 단계를 포함한 비교 방법의 전체 탐색시간을 제안 방법의 전체 탐색시간으로
나누어 계산합니다.

수치 테스트, 제안 방법의 연간 네 사례 재현, 표·그림 재구성 결과는
[검증 기록](verification/README.md)에 정리되어 있습니다. 입력 데이터와 출처는
[입력 설명](data/README.md)과 [외부 자료·방법 출처](THIRD_PARTY_NOTICES.md)에서
확인하실 수 있습니다.

```bash
python -m unittest pem_planning.test_pwl_capacity_oracle pem_planning.test_oracle_matched_benchmark pem_planning.test_g_oracle_benchmark
python scripts/check_release.py
```

## 파일 구성

| 경로 | 내용 |
|---|---|
| `pem_planning/physics/`, `data/` | 물리·경제 파라미터와 연간 입력 |
| `pem_planning/pwl_capacity_oracle.py`, `model.py` | 연간 생산·순환 저장 분리와 운전 복원 |
| `pem_planning/continuous_oracle.py`, `fixed_wind_slices.py` | 설계영역 탐색과 정수 단면 |
| `pem_planning/oracle_matched_benchmark.py`, `g_oracle_benchmark.py` | ORACLE·G-ORACLE 비교 |
| `pem_planning/cached_distance.py` | 거리 재사용 옵션 |
| `results/`, `reference_results/` | 사례 분석과 성능 비교 결과 |
| `scripts/reproduce_performance.py` | Table 4와 Fig. 7·8 재구성 |
| `scripts/check_release.py`, `verification/` | 수치 검증과 검증 기록 |

Solver 문서: [SciPy HiGHS](https://docs.scipy.org/doc/scipy/reference/optimize.linprog-highs.html).

방법 출처: ORACLE, Turan·Moert·Bardow (2026),
[10.1016/j.compchemeng.2026.109630](https://doi.org/10.1016/j.compchemeng.2026.109630);
G-ORACLE, Hajikazemi·Steinke (2026),
[arXiv:2610.32759v1](https://arxiv.org/abs/2610.32759v1).
