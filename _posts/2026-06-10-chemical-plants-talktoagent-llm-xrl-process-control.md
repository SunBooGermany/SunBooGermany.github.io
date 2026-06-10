---
layout: post
title: "TalkToAgent: Using Existing LLMs to Explain RL Controllers in Chemical Plants"
title_ko: "TalkToAgent: 기존 LLM으로 화학 플랜트 RL 제어기를 설명하기"
date: 2026-06-10
category: chemical-plants
category_label: "Chemical Plants"
research_group: application_reviews
research_category: chemical-plants
research_category_label: "Chemical Plants"
application_category: "chemical-plants"
application_category_label: "Chemical Plants"
method_category: ""
method_category_label: ""
paper_title: "TalkToAgent: A multi-agent LLM Framework for natural language explanation of reinforcement learning policies"
authors: "Kim, H.; Chen, H.; Li, C.; Lee, J. M."
venue: "Computers & Chemical Engineering"
year: "2026"
doi: ""
arxiv: ""
source_url: ""
tags:
  - "process control"
  - "reinforcement learning"
  - "explainable AI"
  - "LLM agents"
  - "chemical plants"
  - "contrastive explanation"
excerpt: "A critical note on TalkToAgent, an LLM multi-agent framework that reuses existing LLMs to route natural-language questions to XRL tools for chemical process-control policies."
excerpt_ko: "기존 LLM을 화학 도메인에 맞게 fine-tuning하는 대신, 자연어 질문을 XRL 도구와 simulator에 연결해 chemical process-control RL policy를 설명하는 TalkToAgent에 대한 비판적 정리."
language: "en-ko"
has_korean_note: false
---

## How an LLM can help with controller explanations

The useful role of an LLM in this setting is not to replace process-control analysis. It is to make the analysis easier to ask for. A chemical engineer may not want to decide whether a question requires SHAP, Q-value decomposition, a rollout comparison, or a generated contrastive policy. The LLM can sit between the user's question and those tools: classify the intent, call the right computation, help assemble executable analysis code when needed, and summarize the resulting figures or numbers in ordinary language.

The LLM helps translate between engineering questions and XRL workflows. The plant-facing evidence still has to come from the controller, the simulator, the reward decomposition, and the contrastive trajectories.

## Still, this is not chemical-domain fine-tuning

The first thing to clarify is what this paper is not. This is not a study that fine-tunes an LLM to become a chemical-engineering or chemical-plant specialist. It does not claim that the language model has learned process dynamics, reaction kinetics, plant safety constraints, or controller design from domain-specific training.

The idea is narrower and more practical: take existing LLMs and use them as an interface layer around already defined explainable-RL tools. The LLM is not the source of truth. It routes a user's natural-language question to an XRL computation, helps generate small pieces of executable analysis code when needed, and turns plots or numerical outputs into a readable explanation. The explanation is grounded in DeepSHAP, Q-value decomposition, simulator rollouts, and contrastive policy comparisons, not in free-form LLM speculation.

That distinction matters for chemical plants. In a safety-critical process-control setting, a fluent explanation is not enough. If the LLM says "the controller increased coolant flow because the reactor temperature was rising," the useful question is: which attribution, rollout, reward component, or counterfactual simulation supports that sentence?

## Why this problem matters for process control

Deep reinforcement learning is attractive in process control because chemical plants are nonlinear, coupled, constrained, and often operated in continuous state-action spaces. A learned policy can sometimes handle dynamics that are awkward for a simple rule-based controller.

The problem is trust. A chemical engineer cannot simply deploy a black-box RL policy because its average simulation performance looks good. The operator needs to ask questions such as: "Why did the agent choose this control action?", "Which process variables drove the action?", "What future reward trade-off was the policy expecting?", "What would have happened under a more conservative behavior?", and "How would a simple on-off policy compare in this state region?"

Traditional XRL tools answer fragments of these questions. Feature attribution can show which state variables influenced the current action. Reward decomposition can show which future reward terms dominate. A contrastive rollout can compare one action with another. But those tools are scattered, technical, and often require the user to know which method to call.

TalkToAgent tries to reduce that interface burden. The contribution is not a new RL theorem. It is an engineering framework that connects natural-language questions to a structured set of XRL computations for process-control policies.

## System structure

The framework has three main roles:

```text
user query
  -> Coordinator: infer intent and select an XRL tool
  -> XRL tool: attribution, reward decomposition, or contrastive simulation
  -> Explainer: translate figures and numerical outputs into natural language

for generated code:
  Coder -> Evaluator -> Debugger -> refined code
```

The Coordinator maps a question to one of several explanation modes. If the user asks which variables mattered, the system can use a feature-importance tool such as DeepSHAP. If the user asks what the agent expected to gain, it can use Q-value or reward-component decomposition with rollout results. If the user asks "what if the controller behaved differently?", it can run a contrastive simulation.

The Coder-Evaluator-Debugger loop is used when the explanation requires generated code, especially for reward decomposition or policy-level contrastive explanations. This is a sensible use of LLMs: not to assert a plant explanation directly, but to help assemble executable analysis that can be checked against the simulator.

## The XRL tools being orchestrated

The first tool family is feature importance. The paper uses DeepSHAP to attribute an action output to input state variables. In a tank system, for example, the explanation might say that a lower-tank level error contributed strongly to a pump-voltage action. This is useful, but it is still local attribution. It does not prove dynamic causality inside the closed-loop plant.

The second family is expected-outcome explanation. Instead of asking only "which state variable changed the action?", it asks what future trajectory and reward trade-off the action is associated with. A policy in a quadruple-tank system may accept a short-term imbalance in one level to improve a later tracking objective or reduce control variation. This is closer to the logic of RL because the policy is trained against discounted future return, not only the current error.

In simplified notation, the value being explained is:

<math display="block" aria-label="Q value as expected discounted reward components">
  <msup><mi>Q</mi><mi>&pi;</mi></msup>
  <mo>(</mo><mi>s</mi><mo>,</mo><mi>a</mi><mo>)</mo>
  <mo>=</mo>
  <mi>E</mi>
  <mo>[</mo>
  <msubsup><mo>&sum;</mo><mrow><mi>t</mi><mo>=</mo><mn>0</mn></mrow><mi>&infin;</mi></msubsup>
  <msup><mi>&gamma;</mi><mi>t</mi></msup>
  <msub><mi>r</mi><mi>t</mi></msub>
  <mo>|</mo>
  <msub><mi>s</mi><mn>0</mn></msub><mo>=</mo><mi>s</mi><mo>,</mo>
  <msub><mi>a</mi><mn>0</mn></msub><mo>=</mo><mi>a</mi><mo>,</mo>
  <mi>&pi;</mi>
  <mo>]</mo>
  <mo>.</mo>
</math>

The caveat is that this "expectation" is only as good as the learned critic, the reward decomposition, and the simulator rollouts used to approximate it. In stochastic or model-mismatched plants, a representative rollout is not the same thing as a verified expectation over the real plant.

The third family is contrastive explanation. The paper separates this into three levels: "CE-A: action-level contrast", "CE-B: behavior-level contrast", and "CE-P: policy-level contrast".

CE-A changes a specific action and compares the resulting trajectory. This is direct, but it requires the user to specify a numerical alternative action. CE-B accepts qualitative control language such as "more conservative," "more aggressive," or "opposite," then maps that phrase into an action-trajectory transformation. CE-P generates a simple alternative policy, such as an on-off controller, and compares its rollout with the RL policy.

This is the most useful application-facing extension. A chemical engineer is more likely to ask about conservative operation, aggressive cooling, or an on-off fallback policy than to request a specific numerical action perturbation at one time step.

## Why the framework is useful

The useful part of TalkToAgent is the interaction design around XRL. It changes the user's job from "choose the correct explanation algorithm and its arguments" to "ask a process-control question." That is a real reduction in cognitive load.

It also avoids one obvious failure mode of LLM explanations. The language model is not asked to invent a reason from scratch. It is asked to interpret artifacts produced by predefined tools: SHAP values, reward-component plots, forward simulations, and contrastive trajectories. This does not eliminate hallucination, but it gives the explanation an external anchor.

For chemical plants, that matters because the explanation should be inspectable. A reasonable workflow is:

```text
natural-language question
  -> selected XRL tool
  -> simulator-grounded computation
  -> figure or numerical comparison
  -> natural-language explanation
  -> operator checks whether the explanation matches process intuition
```

The last step is important. This is not an autonomous safety-certification system. It is an interactive analysis layer for understanding a learned controller.

## Experimental setting

The paper evaluates the framework on three process-control benchmarks: a continuous stirred-tank reactor, a quadruple-tank system, and a photobioreactor. The RL controller is trained with SAC. The examples are well chosen because they cover different process-control structures: setpoint tracking, coupled liquid-level dynamics, and yield-oriented bioprocess operation.

The evaluation asks whether the system can map user queries to the correct XRL function and arguments, whether it can generate contrastive policy code reliably enough to run, and whether the resulting multimodal explanations contain domain-relevant information. The reported task-classification accuracy is high across the three benchmarks, with some errors in contrastive queries that are semantically ambiguous. The code-generation loop also reduces repeated failures compared with direct generation, although policy-level contrastive examples are still small in scale.

The cost profile is also worth noting. Simple feature-importance or rollout explanations are relatively cheap. CE-P can consume many more tokens because it involves code generation, evaluation, debugging, and another simulation. In a real deployment, that difference matters. A plant-facing explanation system would need latency, budget, and audit controls.

## Critical reading

The strongest limitation is explanation faithfulness. SHAP, reward decomposition, and contrastive rollout are post-hoc tools. They can make a controller more interpretable, but they do not prove that the neural policy internally "reasoned" in the way the explanation describes. A good phrasing is: this action is interpretable through these state attributions and simulated consequences. A bad phrasing is: the agent truly made the decision for this human-like reason.

The second limitation is simulator dependence. Expected-outcome and contrastive explanations depend on forward simulation. If the simulator misses actuator delays, measurement noise, unmodeled constraints, fouling, regime shifts, or plant-model mismatch, the contrastive explanation can be clean and still misleading.

The third limitation is the semantic gap in CE-B. Mapping "conservative" to a smoothing parameter or "aggressive" to an amplified action trajectory is intuitive, but it is a heuristic. In control terms, conservative behavior should ideally be defined through an optimization problem or explicit behavioral constraints, such as smaller action variation, bounded overshoot, or stricter safety margins. Without that, different users may mean different things by the same word.

The fourth limitation is CE-P. Comparing an RL policy against a generated on-off controller is useful, but it should not be oversold as general policy-level explanation. The current form is closer to local counterfactual policy simulation over a chosen interval or condition than to a global explanation of the learned policy.

Finally, the Evaluator is not a formal verifier. It may reduce code-generation errors, but it does not guarantee that a generated policy satisfies the intended process-control specification. For safety-facing use, the generated code should be checked by executable assertions or formal specifications, not only by another LLM agent.

## Takeaway

TalkToAgent is best read as a practical orchestration layer for explainable RL in chemical process control. Its value is not that an LLM becomes a chemical plant expert through fine-tuning. Its value is that an existing LLM can help route natural-language engineering questions to grounded XRL tools and then summarize their outputs in a way a process engineer can inspect.

## References

Kim, H., Chen, H., Li, C., & Lee, J. M. (2026). TalkToAgent: A multi-agent LLM Framework for natural language explanation of reinforcement learning policies. Computers & Chemical Engineering, 109672.

<!-- ko -->

## LLM이 controller explanation에서 도울 수 있는 일

이 setting에서 LLM의 유용한 역할은 process-control analysis를 대체하는 것이 아니다. 분석을 더 쉽게 요청할 수 있게 만드는 것이다. Chemical engineer가 어떤 질문에 SHAP이 필요한지, Q-value decomposition이 필요한지, rollout comparison이 필요한지, generated contrastive policy가 필요한지 매번 직접 고르고 싶지는 않을 수 있다. LLM은 사용자 질문과 이런 도구들 사이에 놓일 수 있다. Intent를 분류하고, 적절한 computation을 호출하고, 필요할 때 executable analysis code를 조립하도록 돕고, 결과 figure나 numerical output을 일반 언어로 요약한다.

LLM은 engineering question과 XRL workflow 사이를 번역한다. Plant-facing evidence는 여전히 controller, simulator, reward decomposition, contrastive trajectory에서 나와야 한다.

## 그래도 chemical-domain fine-tuning 연구는 아니다

먼저 이 논문이 무엇이 아닌지를 분명히 해야 한다. 이 연구는 LLM을 chemical engineering이나 chemical plant에 특화되도록 fine-tuning한 연구가 아니다. 언어모델이 도메인 특화 학습을 통해 공정 동역학, 반응속도론, plant safety constraint, controller design을 새로 배웠다고 주장하지 않는다.

핵심 아이디어는 더 좁고 실용적이다. 이미 개발된 LLM을 가져와서, 미리 정의된 explainable-RL 도구들 위에 인터페이스 계층으로 사용하는 것이다. LLM은 근거 자체가 아니다. 사용자의 자연어 질문을 적절한 XRL 계산으로 routing하고, 필요할 때 작은 분석 코드를 생성하며, plot이나 numerical output을 읽을 수 있는 설명으로 바꾼다. 설명의 근거는 LLM의 자유 추론이 아니라 DeepSHAP, Q-value decomposition, simulator rollout, contrastive policy comparison이다.

이 구분은 chemical plant에서 중요하다. Safety-critical process-control setting에서는 유창한 설명만으로는 충분하지 않다. LLM이 "reactor temperature가 올라가서 controller가 coolant flow를 늘렸다"고 말한다면, 실제로 중요한 질문은 그 문장을 어떤 attribution, rollout, reward component, counterfactual simulation이 뒷받침하느냐이다.

## 왜 process control에서 중요한 문제인가

Deep reinforcement learning은 chemical process control에서 매력적이다. Chemical plant는 nonlinear하고, 변수들이 강하게 coupled되어 있으며, constraint가 많고, continuous state-action space에서 운전되는 경우가 많다. Learned policy는 단순한 rule-based controller가 다루기 어려운 dynamics를 처리할 수 있다.

문제는 신뢰다. Chemical engineer는 평균적인 simulation performance가 좋다는 이유만으로 black-box RL policy를 그대로 배치할 수 없다. Operator는 다음과 같은 질문을 던질 수 있어야 한다. "왜 agent가 이 control action을 선택했는가?", "어떤 process variable이 action에 영향을 주었는가?", "policy는 어떤 future reward trade-off를 예상했는가?", "더 conservative하게 행동했다면 trajectory가 어떻게 달라졌는가?", "간단한 on-off policy와 비교하면 이 state region에서 무엇이 다른가?"

기존 XRL 도구들은 이 질문들의 일부만 답한다. Feature attribution은 현재 action에 영향을 준 state variable을 보여줄 수 있다. Reward decomposition은 어떤 future reward term이 지배적인지 보여줄 수 있다. Contrastive rollout은 한 action과 다른 action을 비교할 수 있다. 하지만 이런 도구들은 흩어져 있고, 기술적이며, 사용자가 어떤 method를 호출해야 하는지 알아야 하는 경우가 많다.

TalkToAgent는 이 interface burden을 줄이려는 시도다. 이 논문의 기여는 새로운 RL theorem이 아니다. 자연어 질문을 process-control policy를 설명하기 위한 구조화된 XRL computation으로 연결하는 engineering framework에 가깝다.

## 시스템 구조

프레임워크의 역할은 크게 세 가지다.

```text
user query
  -> Coordinator: intent를 파악하고 XRL tool 선택
  -> XRL tool: attribution, reward decomposition, contrastive simulation
  -> Explainer: figure와 numerical output을 자연어 설명으로 변환

generated code가 필요한 경우:
  Coder -> Evaluator -> Debugger -> refined code
```

Coordinator는 질문을 여러 explanation mode 중 하나로 mapping한다. 사용자가 어떤 변수가 중요했는지 물으면 DeepSHAP 같은 feature-importance tool을 쓴다. Agent가 무엇을 얻으려 했는지 물으면 rollout 결과와 함께 Q-value 또는 reward-component decomposition을 쓴다. "Controller가 다르게 행동했다면 어떻게 되는가?"라고 물으면 contrastive simulation을 실행한다.

Coder-Evaluator-Debugger loop는 reward decomposition이나 policy-level contrastive explanation처럼 generated code가 필요한 경우에 사용된다. 이것은 LLM을 비교적 타당하게 쓰는 방식이다. Plant explanation을 직접 단정하게 만드는 것이 아니라, simulator에서 확인할 수 있는 executable analysis를 조립하도록 쓰는 것이다.

## Orchestration되는 XRL 도구들

첫 번째 도구군은 feature importance다. 논문은 DeepSHAP을 사용해 action output을 input state variable에 attribution한다. Tank system이라면 lower-tank level error가 pump-voltage action에 크게 기여했다는 식의 설명을 만들 수 있다. 유용하지만, 여전히 local attribution이다. Closed-loop plant 안에서의 dynamic causality를 보장하지는 않는다.

두 번째는 expected-outcome explanation이다. 단순히 "어떤 state variable이 action을 바꾸었는가?"가 아니라, 그 action이 어떤 future trajectory와 reward trade-off에 연결되는지를 본다. Quadruple-tank system에서 policy는 나중의 tracking objective를 개선하거나 control variation을 줄이기 위해 단기적인 level imbalance를 받아들일 수 있다. 이것은 현재 error만이 아니라 discounted future return을 기준으로 학습되는 RL의 논리에 더 가깝다.

간단히 쓰면 설명하려는 값은 다음과 같다.

<math display="block" aria-label="Q value as expected discounted reward components">
  <msup><mi>Q</mi><mi>&pi;</mi></msup>
  <mo>(</mo><mi>s</mi><mo>,</mo><mi>a</mi><mo>)</mo>
  <mo>=</mo>
  <mi>E</mi>
  <mo>[</mo>
  <msubsup><mo>&sum;</mo><mrow><mi>t</mi><mo>=</mo><mn>0</mn></mrow><mi>&infin;</mi></msubsup>
  <msup><mi>&gamma;</mi><mi>t</mi></msup>
  <msub><mi>r</mi><mi>t</mi></msub>
  <mo>|</mo>
  <msub><mi>s</mi><mn>0</mn></msub><mo>=</mo><mi>s</mi><mo>,</mo>
  <msub><mi>a</mi><mn>0</mn></msub><mo>=</mo><mi>a</mi><mo>,</mo>
  <mi>&pi;</mi>
  <mo>]</mo>
  <mo>.</mo>
</math>

다만 이 "expectation"은 learned critic, reward decomposition, simulator rollout의 품질에 의존한다. Stochastic하거나 model-plant mismatch가 있는 plant에서는 representative rollout이 실제 plant에 대한 검증된 expectation과 같지 않다.

세 번째는 contrastive explanation이다. 논문은 이를 세 단계로 나눈다. "CE-A: action-level contrast", "CE-B: behavior-level contrast", "CE-P: policy-level contrast".

CE-A는 특정 action을 바꾸고 resulting trajectory를 비교한다. 직접적이지만 사용자가 numerical alternative action을 지정해야 한다. CE-B는 "more conservative," "more aggressive," "opposite" 같은 qualitative control language를 받아 action-trajectory transformation으로 바꾼다. CE-P는 on-off controller 같은 간단한 alternative policy를 생성하고, 그 rollout을 RL policy와 비교한다.

Application 관점에서 가장 유용한 확장은 이 부분이다. Chemical engineer는 특정 time step의 numerical action perturbation보다 conservative operation, aggressive cooling, on-off fallback policy 같은 말로 질문할 가능성이 높다.

## 왜 유용한가

TalkToAgent의 유용한 부분은 XRL을 둘러싼 interaction design이다. 사용자의 일을 "정확한 explanation algorithm과 argument를 고르는 것"에서 "process-control question을 던지는 것"으로 바꾼다. 이것은 실제로 cognitive load를 줄인다.

또 하나의 장점은 LLM explanation의 뻔한 실패 모드를 피하려 한다는 점이다. Language model은 이유를 처음부터 지어내도록 요구받지 않는다. SHAP value, reward-component plot, forward simulation, contrastive trajectory처럼 predefined tool이 만든 artifact를 해석하도록 요구받는다. 이것이 hallucination을 없애지는 않지만, 설명에 외부 anchor를 준다.

Chemical plant에서는 설명이 inspectable해야 한다. 합리적인 workflow는 다음과 같다.

```text
natural-language question
  -> selected XRL tool
  -> simulator-grounded computation
  -> figure or numerical comparison
  -> natural-language explanation
  -> operator checks whether the explanation matches process intuition
```

마지막 단계가 중요하다. 이것은 autonomous safety-certification system이 아니다. Learned controller를 이해하기 위한 interactive analysis layer다.

## 실험 설정

논문은 세 가지 process-control benchmark에서 프레임워크를 평가한다. Continuous stirred-tank reactor, quadruple-tank system, photobioreactor다. RL controller는 SAC로 학습된다. Setpoint tracking, coupled liquid-level dynamics, yield-oriented bioprocess operation을 모두 포함하므로 예제 선택은 적절하다.

평가는 system이 user query를 올바른 XRL function과 argument로 mapping할 수 있는지, contrastive policy code를 실행 가능하게 생성할 수 있는지, 그리고 multimodal explanation이 domain-relevant information을 포함하는지를 본다. 보고된 task-classification accuracy는 세 benchmark에서 높고, 일부 semantic ambiguity가 있는 contrastive query에서 오류가 나타난다. Code-generation loop도 direct generation에 비해 반복 실패를 줄이지만, policy-level contrastive example은 아직 작은 규모다.

비용 구조도 중요하다. Feature-importance나 rollout explanation은 비교적 싸다. CE-P는 code generation, evaluation, debugging, 추가 simulation이 들어가므로 token을 훨씬 많이 쓸 수 있다. 실제 deployment에서는 latency, budget, audit control이 필요하다.

## 비판적 읽기

가장 큰 한계는 explanation faithfulness다. SHAP, reward decomposition, contrastive rollout은 post-hoc tool이다. Controller를 더 해석 가능하게 만들 수는 있지만, neural policy가 실제로 설명된 방식으로 "reasoning"했다는 것을 증명하지 않는다. 좋은 표현은 "이 action은 이런 state attribution과 simulated consequence를 통해 해석할 수 있다"이다. 나쁜 표현은 "agent가 실제로 이 인간적인 이유 때문에 decision을 했다"이다.

두 번째 한계는 simulator dependence다. Expected-outcome과 contrastive explanation은 forward simulation에 의존한다. Simulator가 actuator delay, measurement noise, unmodeled constraint, fouling, regime shift, plant-model mismatch를 놓치면 contrastive explanation은 깨끗하지만 잘못된 설명이 될 수 있다.

세 번째 한계는 CE-B의 semantic gap이다. "Conservative"를 smoothing parameter로 바꾸거나 "aggressive"를 amplified action trajectory로 바꾸는 것은 직관적이지만 heuristic이다. Control 관점에서 conservative behavior는 action variation을 줄이거나 overshoot을 제한하거나 safety margin을 더 엄격하게 두는 explicit behavioral constraint나 optimization problem으로 정의되는 것이 더 낫다. 그렇지 않으면 같은 단어도 사용자마다 다른 의미가 된다.

네 번째 한계는 CE-P다. RL policy를 generated on-off controller와 비교하는 것은 유용하지만, 이를 general policy-level explanation으로 과장하면 안 된다. 현재 형태는 learned policy 전체에 대한 global explanation이라기보다, 선택된 interval이나 condition에서 alternative rule-based policy rollout을 비교하는 local counterfactual에 가깝다.

마지막으로 Evaluator는 formal verifier가 아니다. Code-generation error를 줄일 수는 있지만, generated policy가 의도한 process-control specification을 만족한다는 보장은 없다. Safety-facing use에서는 generated code를 또 다른 LLM agent만으로 확인할 것이 아니라 executable assertion이나 formal specification으로 점검해야 한다.

## Takeaway

TalkToAgent는 chemical process control을 위한 explainable RL orchestration layer로 읽는 것이 가장 정확하다. 가치는 LLM이 fine-tuning을 통해 chemical plant expert가 된다는 데 있지 않다. 이미 개발된 LLM이 자연어 engineering question을 grounded XRL tool로 routing하고, 그 output을 process engineer가 검토할 수 있는 설명으로 요약한다는 데 있다.

## References

Kim, H., Chen, H., Li, C., & Lee, J. M. (2026). TalkToAgent: A multi-agent LLM Framework for natural language explanation of reinforcement learning policies. Computers & Chemical Engineering, 109672.
