# 다단계 설비계획을 위한 PICNN 코드

논문과 보충자료(SI)의 PICNN을 학습하고 myopic, omniscient,
2-period rolling horizon(RH), 8·27노드 Markov-chain SDDP와 비교합니다. 최적화에는 SciPy의
HiGHS dual simplex solver를 사용하며, 6일치(144시간) 태양광·수요 데이터는
`data/renewables_demand_6days.csv`에 포함되어 있습니다.

[English](README.md)

## 이용 조건

Copyright (c) 2026 Sunwoo Kim. 비상업적 연구 목적으로만 사용·복제·수정·공유할 수
있습니다. 기업 내부 연구개발, 유료 자문, 상용 제품·서비스 개발을 포함한 상업적
이용에는 Sunwoo Kim의 사전 서면 허가가 필요합니다. 재배포할 때는 저작권 고지와
동일한 이용 조건을 유지해야 하며, 외부 라이브러리·데이터에는 각 권리자의 조건이
적용됩니다. 전체 조건은 [라이선스](LICENSE.md)에 명시되어 있습니다.

## 설치와 평가

Python 3.10 이상에서 이 폴더를 기준으로 실행합니다.

```bash
python -m venv .venv
# Windows: .venv\Scripts\activate
# Linux/macOS: source .venv/bin/activate
python -m pip install -r requirements.txt

python -m capacity_planning evaluate --stages 6 --uncertainty 0.1 --test-count 10 --methods proposed myopic omniscient rh --policy reference_policies/T6_std10_PICNN4_seed0 --out outputs/example
python scripts/reproduce_table10.py
```

평가 결과는 경로별 순현재비용(NPC)과 평균·표준편차·최대값을 담은 CSV/JSON으로
저장합니다. 비용 단위는 논문과 같습니다. `reproduce_table10.py`는 저장된 경로별
결과로 SI Table 10을 재구성합니다.

## PICNN 학습

```bash
# 짧은 실행 확인
python -m capacity_planning train --stages 6 --uncertainty 0.1 --successors 4 --epochs 6 --validation-rounds 1 1 1 --out outputs/short_training

# 10,000 epoch 학습 및 고정 정책 평가
python -m capacity_planning train --stages 6 --uncertainty 0.1 --successors 4 --seed 0 --out outputs/training
python -m capacity_planning evaluate --stages 6 --uncertainty 0.1 --methods proposed --policy outputs/training/selected_policy --out outputs/evaluation
```

`--stages`는 6·12·18·24단계, `--successors`는 후속 표본 1·4·16개를 지원합니다.
짧은 실행 예시는 동작 확인용이며, 논문의 학습은 10,000 epoch 동안 epoch마다
한 경로를 사용합니다. 손실함수는 MSE입니다.

PICNN은 256개 노드의 볼록 은닉층, 64개 노드의 conditioning network,
비음수 출력 가중치를 사용합니다. 학습에는 replay, 실행 가능한 의사결정 탐색,
후속 비용 가중치의 점진적 증가, target network 갱신을 적용하며, 마지막 단계의
학습 목표도 후속 표본들의 평균으로 계산합니다.

기본 검증은 seed 400-799를 50/50/300경로로 나누어 정책을 선택하고,
기본 평가는 seed 0-399를 사용합니다. 선택한 정책을 추가 경로에서 평가하려면
`--test-start 10000 --test-count 2000`을 지정합니다.

## SDDP와 비교 정책

```bash
python -m capacity_planning benchmark --stages 6 --uncertainty 0.1 --nodes 8 27 --seeds 17 23 29 --iterations 100 --out outputs/benchmarks
python -m capacity_planning benchmark --stages 24 --uncertainty 0.3 --nodes 8 27 --seeds 17 23 29 --iterations 100 --out outputs/benchmarks_24
```

SDDP의 8노드 격자는 각 배율의 평균 ±1 표준편차로 만든 누적 경로를 조합하며,
27노드 격자는 단계별 주변분포 중앙값을 추가합니다. 노드별 cut과 현재 관측에
조건부인 전이확률로 Markov 의존성을 반영합니다. 현재 의사결정에는 실현된
후속 관측을 사용하지 않습니다.

전이확률 추정에는 2,048개, 중앙값 추정에는 65,536개의 독립 표본을 사용합니다.
SI의 네 가지 경우는 격자와 조건부 표본을 함께 제공하며, 그 밖의 지원 조건은
독립적으로 생성합니다. SDDP는 지정한 반복 횟수만큼 학습하고 각 학습 seed의
결과를 저장합니다.

RH는 다음 단계의 조건부 평균을 사용해 현재와 다음 단계를 함께 최적화하고,
현재 의사결정만 실행한 뒤 다음 관측에서 다시 풉니다. 두 단계 이후의 후속
비용은 0으로 둡니다. Myopic은 현재 단계만 최적화합니다. Omniscient는 전체
실현 경로를 미리 알고 푸는 비교 기준이므로 실제 운영 정책으로 사용할 수 없습니다.

## 모델 조건

총 계획기간은 단계 수와 관계없이 30년입니다. 5년 기준 불확실성 모멘트를
단계 간격에 맞게 변환한 뒤 배율의 상·하한을 적용하고, 144시간 운영자료는
8760/144의 가중치로 연간 환산합니다. 당기 투자 설비는 당기 운영에 사용할 수
있으며, 설비 수명 구간은 다음 단계로 넘어갈 때 이동합니다.

## 저장된 정책과 결과

`reference_results/`에는 SI 네 가지 경우의 SDDP·PICNN 비용과 표의 출처가,
`reference_policies/`에는 PICNN의 NumPy 체크포인트와 설정별 SDDP cut이 있습니다.
6단계·10% SI 정책은 seed 0, 추가 경로 분석의 검증 선택 정책은 seed 4입니다.
24단계·30% 정책도 포함되어 있습니다.

저장된 비용은 당시 solver와 학습 설정에서 얻은 결과입니다. HiGHS는 퇴화 LP에서
다른 의사결정이나 쌍대해를 선택할 수 있고, 재학습한 정책도 저장된 정책과 달라질
수 있습니다. 고정 정책 재평가와 짧은 학습의 검증 범위는 [검증 기록](verification/README.md)에
정리되어 있습니다. 전체 10,000 epoch 재학습은 이 검증에 포함되지 않았습니다.

```bash
python -m unittest discover -s tests -v
python scripts/check_release.py --full-picnn
```

## 파일 구성

| 경로 | 내용 |
|---|---|
| `capacity_planning/config.py`, `data/` | 모델 파라미터, 6일 데이터, SDDP 격자 |
| `capacity_planning/lp.py`, `model.py` | HiGHS LP와 설비계획 모델 |
| `capacity_planning/picnn.py`, `training.py` | PICNN 학습과 체크포인트 선택 |
| `capacity_planning/nodes.py`, `sddp.py` | Markov 격자와 SDDP |
| `capacity_planning/policies.py` | 동일 경로에서의 정책 평가 |
| `scripts/reproduce_table10.py` | SI Table 10 재구성 |
| `scripts/check_release.py`, `tests/` | 고정 정책 재평가와 수치 검증 |
| `verification/` | 검증 설정과 결과 |

Solver 문서: [SciPy HiGHS](https://docs.scipy.org/doc/scipy/reference/optimize.linprog-highs.html).
