---
layout: post
title: "Slow-Fast Degradation Inference for Chemical Plant Operation"
title_ko: "화학 플랜트 운전을 위한 slow-fast degradation inference"
date: 2026-07-02
category: chemical-plants
category_label: "Chemical Plants"
research_group: application_reviews
research_category: chemical-plants
research_category_label: "Chemical Plants"
application_category: "chemical-plants"
application_category_label: "Chemical Plants"
method_category: ""
method_category_label: ""
paper_title: "Disentangling slow and fast temporal dynamics in degradation inference with hierarchical differential models"
authors: "Zhao, M.; Fink, O."
venue: "Reliability Engineering & System Safety, 277, Article 112943"
year: "2027"
doi: "10.1016/j.ress.2026.112943"
arxiv: ""
source_url: "https://doi.org/10.1016/j.ress.2026.112943"
tags:
  - "chemical plants"
  - "degradation inference"
  - "process monitoring"
  - "neural CDE"
  - "slow-fast dynamics"
  - "predictive maintenance"
excerpt: "A note on Zhao and Fink's H-CDE model for separating slow latent degradation from fast operational dynamics, read from the viewpoint of chemical plant monitoring and operation."
excerpt_ko: "Zhao와 Fink의 H-CDE 모델을 chemical plant monitoring과 operation 관점에서 읽는다. 핵심은 느린 latent degradation과 빠른 operational dynamics를 분리해 추론하는 구조다."
language: "en-ko"
has_korean_note: false
---

This paper does not use a chemical plant as its case study, but it addresses a problem that chemical plants should care about: sensor signals move for two very different reasons. A plant can look different because the current feed, temperature, pressure, catalyst activity, recycle condition, or controller action is different. It can also look different because equipment has slowly degraded.

Those two causes are easily mixed. A heat exchanger may show a higher temperature approach because the fouling layer has grown, but it may also show the same symptom because the feed rate, utility condition, or upstream composition changed. A compressor vibration signal may increase because of bearing degradation, but also because the operating point moved closer to a difficult regime. A residual-based monitoring system can flag the deviation, but the deviation is not automatically a degradation coordinate.

That is the plant-facing reason this paper is interesting. Zhao and Fink frame degradation inference as a slow-fast disentanglement problem. The slow part is an unobserved latent degradation state. The fast part is the observable operational dynamics. The proposed model, Hierarchical Controlled Differential Equation, or H-CDE, forces these two parts into different modules.

## Why residual monitoring becomes ambiguous

A common monitoring logic is:

1. Learn or define a healthy-response model.
2. Compare the actual sensor value against the healthy prediction.
3. Treat a large residual as evidence of degradation or abnormality.

In notation, the residual is roughly `r(t) = x(t) - x_healthy_hat(t)`.

The problem is that `r(t)` is not only degradation. In a chemical plant, the residual can contain feed disturbance, load change, ambient condition, controller action, sensor noise, unmodeled recycle dynamics, catalyst aging, fouling, corrosion, or partial equipment damage. The residual is therefore a mixture of operation and degradation.

A minimal example makes the point. Suppose the measured response is `x = (1 + d)u`, where `u` is the operating input and `d` is degradation. If the healthy model predicts `x_hat = u`, then the residual is `r = du`. The same degradation level gives a small residual at low load and a large residual at high load. The residual size is not a clean health index.

This is exactly the difficulty that appears in plant monitoring. A fouled exchanger does not express itself independently of flow rate and temperature. A partially deactivated catalyst does not change conversion independently of inlet composition, residence time, and temperature. Degradation changes the fast process response, but it is not directly observed as a separate variable.

## The paper's modeling move

The paper starts from a slow-fast view of the system:

- `x(t)` is the fast observed or operational state.
- `u(t)` is the operating input or external condition.
- `d(t)` is the slow latent degradation state.
- `d(t)` evolves much more slowly than `x(t)`, but it changes the dynamics of `x(t)`.

The central phrase is:

degradation is not a residual; it is a slow latent state that conditions fast dynamics.

That distinction matters. If degradation is treated as a residual, the model asks, "What is left unexplained by the healthy model?" If degradation is treated as a slow latent state, the model asks, "What slowly accumulated state makes future sensor dynamics easier to predict?"

The H-CDE architecture uses this second question.

## H-CDE in one pass

The model has four important pieces.

First, a long and coarse history of observations is passed through a path transformation. The raw sensor and input history is not sent directly to the slow degradation module. A learned encoder `h_psi` transforms it into a latent path that is supposed to emphasize degradation-relevant temporal information.

Second, a slow CDE processes that transformed path and produces a latent degradation trajectory `d_hat(tau)`. This module uses a coarse time grid and long history. Its job is not to explain every short transient. Its job is to carry long-horizon information.

Third, the model uses an approximately monotone bounded activation inside the slow degradation dynamics. The intention is physically sensible: degradation usually does not jump up and down like a daily operating cycle, and its rate should not explode. The paper's activation does not give a strict monotonicity guarantee, but it acts as an inductive bias against encoding fast oscillations as degradation.

Fourth, the inferred degradation state is interpolated to the fast time grid and passed into a fast CDE. The fast CDE predicts the next sensor state using the current sensor state, current operating condition, time, and `d_hat`. This is important because `d_hat` must earn its role by helping predict future observable dynamics.

In plant language:

- the slow module asks what long-term condition the plant has accumulated;
- the fast module asks how the currently operated plant will respond next;
- the degradation representation is useful only if it changes the fast prediction in the right way.

## Why this is relevant to chemical plants

Chemical plants are full of slow-fast structure. Fouling, catalyst deactivation, corrosion, membrane aging, adsorbent capacity loss, valve stiction, sensor drift, and heat-transfer degradation can evolve over days, weeks, or months. The observable process variables move over seconds or minutes under disturbances, control actions, recycle dynamics, phase changes, and grade transitions.

That separation is exactly where the H-CDE idea becomes attractive. A plant historian may contain long operating histories, but the maintenance-relevant state is not a direct column in the data table. It has to be inferred from how the plant responds under different operating conditions.

For example, consider a distillation column with slow tray fouling or heat-exchanger fouling in the reboiler loop. The temperature profile and energy use fluctuate with feed rate, composition, pressure, and controller behavior. A residual can tell us that the current profile is unusual. It cannot by itself say whether the unusual profile is a temporary feed event or accumulated degradation. A slow-fast model tries to use long history to infer a slowly varying latent condition, then use that condition to explain the short-term response.

The same logic applies to reactor operation. Catalyst deactivation changes conversion and heat release, but the measured conversion also depends on inlet composition, temperature, flow rate, residence time, and control actions. A degradation-aware model should not confuse a difficult feed day with irreversible catalyst aging.

## What the path transformation is doing

The path transformation is one of the strongest parts of the architecture. It is not special because it is a large neural network. In the paper it is a small MLP. It is special because of where it is placed.

Raw plant signals contain too much fast operational variation. If the slow degradation module sees raw variables directly, it may learn operating regimes instead of degradation. The path transformation creates a learned control path for the slow module. It asks which aspects of the long history are useful for inferring a slow degradation-aligned state.

For chemical plants, this is a useful design principle. The slow module should not merely memorize current flow, pressure, or temperature. It should learn features closer to cumulative stress, repeated excursions, operation near limits, sustained fouling symptoms, or long-term response changes. The model does not guarantee that it has recovered true physical damage, but the architecture at least pushes the representation toward that role.

The ablation results in the paper support this point. Removing the path transformation is especially damaging in the N-CMAPSS turbofan case, where the degradation signal is not directly visible in raw sensor space. That is a warning for plant data too: if the degradation driver is hidden behind operating regimes, the encoder that feeds the slow module may be the critical part of the model.

## The monotonicity claim should be read carefully

The paper uses an activation of the form `sigma(a) = sigmoid(gamma a)tanh(a)` to bias degradation increments. The intent is clear: allow positive accumulation, suppress negative movement, keep increments bounded, and avoid drift when the driving input is zero.

But the activation is not strictly nonnegative. For negative `a`, `tanh(a)` is negative and `sigmoid(gamma a)` remains positive, so the product is still negative. With large `gamma`, that negative region is small, but it is not zero.

So the careful wording is not "strict monotonicity enforcement." It is "approximately monotone regularization." That is still useful. In a plant setting, it can reduce the chance that the latent degradation state simply follows load cycles or temperature cycles. But it should not be presented as a mathematical guarantee that the inferred health state can never decrease.

This distinction matters because chemical plants often have partial recovery, cleaning, regeneration, catalyst replacement, maintenance events, sensor recalibration, or regime changes. A model that assumes irreversible degradation too strongly can be wrong after intervention. A model that only regularizes monotonicity may be more flexible, but then its latent state must be interpreted with care.

## What the experiments show

The paper evaluates H-CDE on bridge and turbofan degradation settings. The bridge case is especially relevant conceptually because it has strong transient dynamics. The residual baseline has weak alignment with degradation, while the full H-CDE has much stronger alignment in both in-distribution and out-of-distribution tests.

In the turbofan case, residual representations contain some degradation information, but it is spread across latent directions and mixed with operational variation. H-CDE produces a more concentrated degradation-aligned latent space. The reported ablations also indicate that the path transformation is not decorative; without it, the latent alignment can collapse.

For chemical plant readers, the lesson is not that H-CDE can be deployed directly on every plant historian. The lesson is narrower: if the true plant condition evolves slowly and changes the fast process response, then the model structure should reflect that separation. A pure residual monitor may be too weak because it treats all unexplained variation as one object.

## What is not guaranteed

The most important limitation is identifiability. The latent state `d_hat(t)` is not automatically the true physical degradation `d_true(t)`. In an unsupervised setting, many latent variables can support the same prediction loss. The model might encode calendar time, operating regime, asset identity, or maintenance schedule rather than physical degradation.

This is particularly dangerous when age and degradation are strongly correlated in the data. If every asset becomes more degraded as time passes and the operating profile also changes with time, the model may learn a time coordinate rather than a usage-driven damage coordinate.

A stronger validation would need counterfactual structure: same age with different cumulative load, different age with similar cumulative damage, maintenance events that partially reset condition, or operating profiles shifted independently from degradation. Without such tests, "degradation-aligned latent representation" is safer than "identified physical degradation state."

The paper also does not prove a general stiffness-reduction theorem. Separating slow and fast CDEs can improve numerical conditioning, and the experiments report lower NFE in some settings. But that is empirical evidence under tested conditions, not a universal complexity guarantee.

## Plant-level takeaway

The valuable idea is a modeling discipline: do not ask one residual to carry every meaning. In chemical plant monitoring, fast operational variation and slow equipment degradation should often be represented by different objects.

H-CDE gives one way to impose that discipline:

- long history and coarse time grid for degradation;
- transformed path before the slow module;
- approximately monotone bounded latent dynamics;
- fast prediction conditioned on the inferred slow state.

Read this way, the paper is not only a PHM paper for bridges and engines. It is a useful reminder for process systems engineering: degradation-aware operation needs models where slowly changing equipment condition is allowed to change short-term process dynamics, rather than appearing only as a leftover residual.

## References

Zhao, M., & Fink, O. (2027). Disentangling slow and fast temporal dynamics in degradation inference with hierarchical differential models. *Reliability Engineering & System Safety, 277*, Article 112943. [https://doi.org/10.1016/j.ress.2026.112943](https://doi.org/10.1016/j.ress.2026.112943)

<!-- ko -->

이 논문은 chemical plant를 사례 문제로 적용한 것은 아니지만, chemical plant에서 매우 관심있어할 문제 상황을 다루고 있다. Sensor signal은 두 가지 전혀 다른 이유로 움직인다. 현재 feed, temperature, pressure, catalyst activity, recycle condition, controller action이 달라져서 plant가 다르게 보일 수 있다. 동시에 equipment가 천천히 degradation되었기 때문에 다르게 보일 수도 있다.

이 두 원인은 쉽게 섞인다. Heat exchanger의 temperature approach가 커졌다고 하자. 이것은 fouling layer가 두꺼워졌기 때문일 수 있지만, feed rate, utility condition, upstream composition이 바뀌었기 때문일 수도 있다. Compressor vibration이 커졌다고 하자. Bearing degradation 때문일 수 있지만, operating point가 더 어려운 regime으로 이동했기 때문일 수도 있다. Residual-based monitoring은 deviation을 잡아낼 수 있지만, 그 deviation이 곧바로 degradation coordinate가 되는 것은 아니다.

그래서 이 논문이 plant 관점에서 흥미롭다. Zhao와 Fink는 degradation inference를 slow-fast disentanglement 문제로 본다. 느린 부분은 관측되지 않는 latent degradation state이고, 빠른 부분은 관측 가능한 operational dynamics다. 제안 모델인 Hierarchical Controlled Differential Equation, 즉 H-CDE는 이 두 부분을 서로 다른 module로 나누도록 강제한다.

## Residual monitoring은 왜 애매해지는가

흔한 monitoring logic은 다음과 같다.

1. Healthy-response model을 학습하거나 정의한다.
2. 실제 sensor value와 healthy prediction을 비교한다.
3. 큰 residual을 degradation 또는 abnormality의 증거로 본다.

표기하면 residual은 대략 `r(t) = x(t) - x_healthy_hat(t)`다.

문제는 `r(t)`가 degradation만 담지 않는다는 점이다. Chemical plant에서 residual에는 feed disturbance, load change, ambient condition, controller action, sensor noise, unmodeled recycle dynamics, catalyst aging, fouling, corrosion, partial equipment damage가 함께 들어갈 수 있다. 따라서 residual은 operation과 degradation의 혼합물이다.

간단한 예로 보자. 측정 response가 `x = (1 + d)u`라고 하자. 여기서 `u`는 operating input이고 `d`는 degradation이다. Healthy model이 `x_hat = u`를 예측하면 residual은 `r = du`다. 같은 degradation level이라도 low load에서는 residual이 작고 high load에서는 residual이 크다. Residual 크기는 깨끗한 health index가 아니다.

Plant monitoring에서 바로 이런 문제가 나타난다. Fouled exchanger의 영향은 flow rate와 temperature에서 독립적으로 나타나지 않는다. Partially deactivated catalyst의 영향도 inlet composition, residence time, temperature, control action과 독립적으로 나타나지 않는다. Degradation은 fast process response를 바꾸지만, 별도의 변수로 직접 관측되지는 않는다.

## 논문의 modeling move

논문은 system을 slow-fast 구조로 본다.

- `x(t)`는 빠른 observed 또는 operational state다.
- `u(t)`는 operating input 또는 external condition이다.
- `d(t)`는 느린 latent degradation state다.
- `d(t)`는 `x(t)`보다 훨씬 느리게 변하지만, `x(t)`의 dynamics를 바꾼다.

핵심 문장은 다음에 가깝다.

Degradation은 residual이 아니라, fast dynamics를 condition하는 slow latent state다.

이 구분은 중요하다. Degradation을 residual로 보면 모델은 "healthy model이 설명하지 못하고 남은 것이 무엇인가?"를 묻는다. Degradation을 slow latent state로 보면 모델은 "어떤 느리게 누적된 상태가 future sensor dynamics를 더 잘 설명하는가?"를 묻는다.

H-CDE architecture는 두 번째 질문을 사용한다.

## H-CDE 구조

모델에는 중요한 네 가지 장치가 있다.

첫째, 길고 성긴 observation history를 path transformation에 통과시킨다. Raw sensor와 input history를 slow degradation module에 바로 넣지 않는다. Learned encoder `h_psi`가 이를 degradation-relevant temporal information을 강조하는 latent path로 바꾼다.

둘째, slow CDE가 그 transformed path를 처리해 latent degradation trajectory `d_hat(tau)`를 만든다. 이 module은 coarse time grid와 long history를 사용한다. 모든 short transient를 설명하는 것이 아니라 long-horizon information을 들고 가는 것이 역할이다.

셋째, slow degradation dynamics 안에 approximately monotone bounded activation을 사용한다. 의도는 물리적으로 타당하다. Degradation은 보통 daily operating cycle처럼 위아래로 튀지 않고, rate도 무한히 커지면 안 된다. 다만 논문의 activation은 strict monotonicity guarantee를 주지는 않는다. Fast oscillation을 degradation으로 encoding하지 못하게 하는 inductive bias로 보는 편이 정확하다.

넷째, inferred degradation state를 fast time grid로 보간한 뒤 fast CDE에 넣는다. Fast CDE는 현재 sensor state, operating condition, time, `d_hat`을 사용해 다음 sensor state를 예측한다. 여기서 중요점은 `d_hat`이 future observable dynamics를 예측하는 데 실제로 기여해야 한다는 것이다.

Plant 언어로 바꾸면 다음과 같다.

- slow module은 plant가 장기적으로 어떤 condition을 누적했는지 묻는다.
- fast module은 현재 운전되는 plant가 다음 순간 어떻게 반응할지 묻는다.
- degradation representation은 fast prediction을 올바른 방향으로 바꿀 때만 유용하다.

## Chemical plant에 왜 관련 있는가

Chemical plant에는 slow-fast structure가 많다. Fouling, catalyst deactivation, corrosion, membrane aging, adsorbent capacity loss, valve stiction, sensor drift, heat-transfer degradation은 days, weeks, months 단위로 움직일 수 있다. 반면 observable process variable은 disturbance, control action, recycle dynamics, phase change, grade transition 아래에서 seconds 또는 minutes 단위로 움직인다.

이 separation이 바로 H-CDE idea가 매력적인 지점이다. Plant historian에는 긴 operating history가 있을 수 있지만, maintenance-relevant state가 데이터 table의 직접 column으로 존재하는 것은 아니다. 그것은 서로 다른 operating condition 아래에서 plant가 어떻게 반응했는지를 통해 추론해야 한다.

예를 들어 distillation column에서 tray fouling이나 reboiler loop의 heat-exchanger fouling이 천천히 진행된다고 하자. Temperature profile과 energy use는 feed rate, composition, pressure, controller behavior에 따라 흔들린다. Residual은 현재 profile이 unusual하다는 사실을 말해 줄 수 있다. 하지만 그것만으로 이 unusual profile이 temporary feed event인지 accumulated degradation인지는 말하기 어렵다. Slow-fast model은 long history로 slowly varying latent condition을 추정하고, 그 condition으로 short-term response를 설명하려 한다.

Reactor operation도 비슷하다. Catalyst deactivation은 conversion과 heat release를 바꾸지만, measured conversion은 inlet composition, temperature, flow rate, residence time, control action에 의존한다. Degradation-aware model은 어려운 feed day와 irreversible catalyst aging을 혼동하지 않아야 한다.

## Path transformation의 역할

Path transformation은 이 architecture에서 가장 강한 부분 중 하나다. 이것이 큰 neural network라서 특별한 것은 아니다. 논문에서는 작은 MLP다. 특별한 점은 그 위치다.

Raw plant signal에는 fast operational variation이 너무 많이 들어 있다. Slow degradation module이 raw variable을 바로 보면, degradation 대신 operating regime을 배울 수 있다. Path transformation은 slow module을 위한 learned control path를 만든다. Long history 중 무엇이 slow degradation-aligned state를 추론하는 데 유용한지를 묻는 장치다.

Chemical plant 관점에서 이것은 좋은 설계 원칙이다. Slow module이 현재 flow, pressure, temperature를 그대로 외우면 안 된다. Cumulative stress, repeated excursion, operation near limits, sustained fouling symptom, long-term response change에 가까운 feature를 학습해야 한다. 모델이 true physical damage를 복원했다는 보장은 없지만, architecture는 적어도 representation을 그 역할 쪽으로 밀어준다.

논문의 ablation 결과도 이 점을 뒷받침한다. N-CMAPSS turbofan case에서 path transformation을 제거하면 성능이 크게 무너진다. Raw sensor space에서 degradation signal이 직접 보이지 않기 때문이다. Plant data에서도 같은 경고가 있다. Degradation driver가 operating regime 뒤에 숨어 있다면, slow module 앞의 encoder가 핵심이 될 수 있다.

## Monotonicity claim은 조심해서 읽어야 한다

논문은 degradation increment에 `sigma(a) = sigmoid(gamma a)tanh(a)` 형태의 activation을 사용한다. 의도는 명확하다. Positive accumulation은 허용하고, negative movement는 억제하며, increment는 bounded하게 만들고, driving input이 0이면 drift가 생기지 않게 하려는 것이다.

하지만 이 activation은 엄밀히 nonnegative가 아니다. `a`가 음수이면 `tanh(a)`는 음수이고 `sigmoid(gamma a)`는 양수이므로 곱도 음수다. `gamma`가 크면 그 negative region은 작지만 0은 아니다.

따라서 정확한 표현은 "strict monotonicity enforcement"가 아니라 "approximately monotone regularization"이다. 그래도 유용하다. Plant setting에서는 latent degradation state가 load cycle이나 temperature cycle을 그대로 따라가는 것을 줄일 수 있다. 하지만 inferred health state가 절대로 감소하지 않는다는 mathematical guarantee로 말해서는 안 된다.

이 구분은 중요하다. Chemical plant에는 partial recovery, cleaning, regeneration, catalyst replacement, maintenance event, sensor recalibration, regime change가 있다. Irreversible degradation assumption을 너무 강하게 두면 intervention 이후에 틀릴 수 있다. Monotonicity를 regularization으로만 쓰면 더 유연하지만, 그 latent state의 해석도 조심해야 한다.

## 실험 결과가 말하는 것

논문은 H-CDE를 bridge와 turbofan degradation setting에서 평가한다. Bridge case는 transient dynamics가 강하다는 점에서 conceptually relevant하다. Residual baseline은 degradation과 alignment가 약한 반면, full H-CDE는 in-distribution과 out-of-distribution test에서 훨씬 강한 alignment를 보인다.

Turbofan case에서는 residual representation도 어느 정도 degradation information을 담지만, 여러 latent direction에 퍼져 있고 operational variation과 섞인다. H-CDE는 더 concentrated degradation-aligned latent space를 만든다. Ablation 결과도 path transformation이 장식이 아니라는 점을 보인다. 이를 제거하면 latent alignment가 거의 무너질 수 있다.

Chemical plant 독자에게 중요한 메시지는 H-CDE를 모든 plant historian에 바로 배치할 수 있다는 것이 아니다. 더 좁은 lesson은 이것이다. 실제 plant condition이 느리게 변하고 fast process response를 바꾼다면, model structure도 그 separation을 반영해야 한다. Pure residual monitor는 모든 unexplained variation을 하나의 object로 보기 때문에 약할 수 있다.

## 무엇이 보장되지 않는가

가장 중요한 한계는 identifiability다. Latent state `d_hat(t)`가 자동으로 true physical degradation `d_true(t)`가 되는 것은 아니다. Unsupervised setting에서는 여러 latent variable이 같은 prediction loss를 달성할 수 있다. 모델은 physical degradation 대신 calendar time, operating regime, asset identity, maintenance schedule을 encoding할 수도 있다.

이 문제는 age와 degradation이 data에서 강하게 correlated되어 있을 때 특히 위험하다. 모든 asset이 시간이 지날수록 degraded되고, operating profile도 시간에 따라 함께 바뀐다면, 모델은 usage-driven damage coordinate가 아니라 time coordinate를 배울 수 있다.

더 강한 validation에는 counterfactual structure가 필요하다. Same age with different cumulative load, different age with similar cumulative damage, maintenance event that partially resets condition, degradation과 독립적으로 shift된 operating profile 같은 test가 있어야 한다. 이런 검증 없이 "identified physical degradation state"라고 말하기보다는 "degradation-aligned latent representation"이라고 말하는 편이 안전하다.

논문은 general stiffness-reduction theorem도 증명하지 않는다. Slow CDE와 fast CDE를 분리하면 numerical conditioning이 좋아질 수 있고, 실험에서 일부 setting의 NFE 감소도 보고된다. 하지만 이것은 tested condition 아래의 empirical evidence이지 universal complexity guarantee는 아니다.

## Plant-level takeaway

가장 가치 있는 아이디어는 modeling discipline이다. 하나의 residual에게 모든 의미를 맡기지 말자는 것이다. Chemical plant monitoring에서는 fast operational variation과 slow equipment degradation을 서로 다른 object로 표현해야 하는 경우가 많다.

H-CDE는 그 discipline을 강제하는 한 가지 방법이다.

- degradation에는 long history와 coarse time grid를 사용한다.
- slow module 앞에는 transformed path를 둔다.
- slow latent dynamics에는 approximately monotone bounded regularization을 둔다.
- fast prediction은 inferred slow state에 condition된다.

이렇게 읽으면 이 논문은 bridge와 engine을 위한 PHM 논문에만 머물지 않는다. Process systems engineering 관점에서도 유용한 reminder다. Degradation-aware operation을 하려면 slowly changing equipment condition이 short-term process dynamics를 바꿀 수 있어야 한다. 그것을 healthy model의 leftover residual로만 두면, plant가 실제로 늙어 가는 방식과 맞지 않을 수 있다.

## References

Zhao, M., & Fink, O. (2027). Disentangling slow and fast temporal dynamics in degradation inference with hierarchical differential models. *Reliability Engineering & System Safety, 277*, Article 112943. [https://doi.org/10.1016/j.ress.2026.112943](https://doi.org/10.1016/j.ress.2026.112943)
