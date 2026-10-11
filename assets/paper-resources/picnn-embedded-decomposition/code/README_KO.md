# PICNN 논문 공개용 코드

논문과 SI에서 사용한 PICNN, myopic, omniscient, 2-period RH, 고정 8·27노드
Markov-chain SDDP를 실행하는 코드입니다. CPLEX 대신 SciPy에 포함된
오픈소스 HiGHS solver를 사용합니다. 실제 사용한 6일치(144시간) solar·수요
데이터를 `data/renewables_demand_6days.csv`에 저장하여 Excel 경로가 필요 없습니다.

## 설치 및 간단한 실행

Python 3.10 이상을 사용하고 이 폴더에서 실행하십시오.

```bash
python -m venv .venv
# Windows: .venv\Scripts\activate
# Linux/macOS: source .venv/bin/activate
python -m pip install -r requirements.txt

python -m capacity_planning evaluate --stages 6 --uncertainty 0.1 --test-count 10 --methods proposed myopic omniscient rh --policy reference_policies/T6_std10_PICNN4_seed0 --out outputs/example
python scripts/reproduce_table10.py
```

결과는 각 경로의 NPC와 평균·표준편차·최대값을 담은 CSV/JSON으로 저장합니다.
실험 결과와 원고 수치는 별도로 보존하며, 공개 코드로 다시 학습한 결과를
기존 논문의 결과로 덮어쓰지 않습니다.

## PICNN 학습

```bash
# 짧은 실행 확인
python -m capacity_planning train --stages 6 --uncertainty 0.1 --successors 4 --epochs 6 --validation-rounds 1 1 1 --out outputs/short_training

# 10,000 epoch 학습 및 고정 정책 평가
python -m capacity_planning train --stages 6 --uncertainty 0.1 --successors 4 --seed 0 --out outputs/training
python -m capacity_planning evaluate --stages 6 --uncertainty 0.1 --methods proposed --policy outputs/training/selected_policy --out outputs/evaluation
```

stage는 6·12·18·24개, successor는 1·4·16개를 지원합니다. 새 PICNN 학습은
MSE 손실만 사용하며 Huber 학습 옵션은 제거했습니다. 구조는 은닉층
256개 노드, conditioning network 64개 노드입니다. replay, target network,
feasible exploration, continuation 비중 증가, 마지막 단계까지 적용하는
multi-successor 평균을 유지했습니다. validation은 seed 400–799, 기본 test는
seed 0–399입니다. 추가 test는 예를 들어 `--test-start 10000 --test-count 2000`으로
실행할 수 있습니다.

## Benchmark 실행

```bash
python -m capacity_planning benchmark --stages 6 --uncertainty 0.1 --nodes 8 27 --seeds 17 23 29 --iterations 100 --out outputs/benchmarks
python -m capacity_planning benchmark --stages 24 --uncertainty 0.3 --nodes 8 27 --seeds 17 23 29 --iterations 100 --out outputs/benchmarks_24
```

SDDP의 8노드는 각 배율의 평균 ±1 표준편차를 누적한 값들의 조합이고,
27노드는 단계별 주변분포 중앙값을 추가한 조합입니다. 현재 관측 상태에 따른
조건부 전이확률을 사용합니다. SI 네 가지 경우의 노드와 조건부 표본 기반
전이확률은 cache로 제공합니다. RH는 현재와 다음 단계의 조건부 평균을 사용하여
두 단계를 함께 최적화하고, 현재 의사결정만 실행한 뒤 다시 최적화합니다.

모든 stage 수에서 총 계획기간은 30년입니다. 비용·할인·설비 수명·bucket 이동·
144시간 운영자료의 연간 환산은 기존 0510 모델을 유지했습니다. 당기 투자
설비는 당기 운영에 사용할 수 있습니다.

## 포함된 정책과 재현 범위

기존 정책을 `.npz`로 변환해 함께 제공했습니다. SI의 6-stage/10% Proposed는
seed 0이며, 추가 경로 분석에 사용한 validation 선택 정책 seed 4도 별도로
포함했습니다. SI Proposed 값의 successor 수는 행 순서대로 4·16·1·4입니다.
SDDP는 세 training seed의 평균입니다. 24-stage/10% Proposed는 원고 그림에서
얻은 근삿값이며, 해당 원래 checkpoint는 이 컴퓨터에 없어 포함하지 않았습니다.

저장된 6-stage 추가 실험 정책 일부는 과거 Huber 손실로 학습되었습니다.
그 정책과 결과의 학습 이력은 그대로 보존했습니다. 현재 메인 코드로 새로
학습하는 정책은 모두 MSE를 사용합니다.

기존 결과는 기존 solver에서 얻은 값으로 보존했습니다. 공개 코드의 새 학습은
PyTorch seed를 명시하고 진단 연산을 제거하므로, 기존 best run과 완전히 같은
학습 경로를 보장하지 않습니다. solver 변경 검증은 저장된 정책을 고정한 상태에서
수행했습니다. 확인한 범위는 `verification/`에 기록했습니다.

```bash
python -m unittest discover -s tests -v
python scripts/check_release.py --full-picnn
```

GitHub에는 전체 전달물 중 `github_code/`의 내용만 올리면 됩니다. 수정 원고·SI·
답변서는 상위 `revision_documents/`에 별도로 묶었습니다. ensemble, 학습 진단,
Excel 입출력, CPLEX 서버, 컴퓨터별 경로는 실행 코드에서 제거했습니다.
상세 설명은 영문 `README.md`를 참조하십시오.
