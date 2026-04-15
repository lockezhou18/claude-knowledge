---
title: "Harness Engineering for Probabilistic Agents: A Comprehensive Research Report"
date: 2026-04-15
session: continuation of f0ba1463 (agent 10, killed mid-research)
type: research-report
tags: [harness-engineering, probabilistic-agents, cybernetics, crystallization, feedback, variety-engineering, deterministic-shell]
sources: 60+ (48 from killed agent + 15 fresh fetches)
---

# Harness Engineering for Probabilistic Agents

## The Founding Insight

> "We live in a probabilistic world, agents are probabilistic. The way would be like agents exploration, where patterns that keep working keep crystallizing into deterministic structures (software, skills, hooks, rules). Everything is feedback, not failure. The deterministic harness around the probabilistic agent is the engineering."

This insight articulates a design philosophy that, once examined through the right lenses, turns out to have deep roots in cybernetics, statistical physics, control theory, and systems engineering. The claim is not merely aesthetic. It is a precise engineering statement that maps onto formal mathematical structures -- structures that constrain what is possible, predict what will fail, and prescribe what to build.

This report examines five facets of that statement in depth.

---

## 1. The Deterministic Shell Pattern

### The Universal Architecture

Across every field that handles uncertainty computationally, one pattern recurs: a **deterministic outer structure wraps a stochastic inner process**, channeling randomness toward useful ends while guaranteeing properties the stochastic core alone cannot provide. This is not a design preference. It is a mathematical necessity: stochastic processes produce distributions, not answers. Something deterministic must extract the answer.

### Monte Carlo Methods: The Canonical Example

Monte Carlo methods are the purest expression of this pattern. The core idea -- "use randomness to solve deterministic problems" (Metropolis & Ulam, 1949) -- inverts the expected relationship between randomness and precision.

The architecture has four fixed layers:

1. **Domain definition** (deterministic): Establish the space of possible inputs
2. **Random sampling** (stochastic): Generate inputs from a probability distribution
3. **Computation** (deterministic): Apply a fixed function to each sample
4. **Aggregation** (deterministic): Compile results with statistical guarantees

The deterministic shell provides what the stochastic core cannot: convergence guarantees. The law of large numbers ensures the sample mean converges to the population mean. The convergence rate follows 1/sqrt(N) -- quadrupling samples halves the error, regardless of dimensionality. The minimum sample size for a desired error margin epsilon and confidence level z satisfies:

    n >= s^2 * z^2 / epsilon^2

where s^2 is the estimated variance. This formula is entirely deterministic. The randomness lives inside; the guarantees wrap around it.

**Variance reduction techniques** add further deterministic structure inside the stochastic layer. Importance sampling biases random selection toward high-value regions. Stratified sampling partitions the domain deterministically, then samples within each stratum. Quasi-Monte Carlo replaces random sequences with low-discrepancy sequences that fill the space more uniformly. Each technique imposes deterministic scaffolding on the random process, trading pure randomness for faster convergence while preserving the stochastic core's advantage over analytical methods in high dimensions.

### The Kalman Filter: Deterministic Estimation from Noisy Observations

The Kalman filter wraps noisy sensor measurements in a deterministic estimation framework through a predict-update cycle:

**Predict** (deterministic model):
- Project state forward: x_hat(k|k-1) = F_k * x_hat(k-1|k-1) + B_k * u_k
- Project covariance: P(k|k-1) = F_k * P(k-1|k-1) * F_k^T + Q_k

**Update** (fuse with stochastic measurement):
- Innovation: y_tilde_k = z_k - H_k * x_hat(k|k-1)
- Kalman gain: K_k = P(k|k-1) * H_k^T * S_k^(-1)
- State update: x_hat(k|k) = x_hat(k|k-1) + K_k * y_tilde_k

The Kalman gain K_k is the critical mechanism -- it dynamically weights trust between the deterministic model and the noisy measurement. High measurement noise (large R) reduces K, favoring model predictions. Low measurement noise increases K, favoring observations. The gain is computed deterministically from the covariance matrices; the stochasticity enters only through the measurements.

The deep insight: **despite stochastic inputs, the algorithm runs entirely with deterministic matrix operations.** Covariance matrices encode uncertainty quantitatively, but the recursion itself involves no random sampling. Probabilistic observations enter; deterministic estimates exit. This encapsulation is the Kalman filter's engineering genius.

### Stochastic Gradient Descent Inside Training Pipelines

SGD injects noise through random mini-batch sampling. The basic update rule:

    w := w - eta * gradient(Q_i(w))

where i is randomly selected, introduces stochasticity at every step. Yet the training pipeline wrapping SGD is thoroughly deterministic:

- **Epoch structure**: Fixed number of passes over the data
- **Learning rate schedule**: Deterministic decay (step, cosine, warmup-then-decay)
- **Checkpointing**: Save model state at deterministic intervals
- **Early stopping**: Halt when validation loss hasn't improved for N deterministic epochs
- **Gradient clipping**: Deterministic bounds on update magnitude

The learning rate eta functions as a temperature parameter. The connection to simulated annealing is made rigorous through the SDE formulation:

    dW_t = -gradient(Q(W_t) + (1/4)*eta*|gradient(Q(W_t))|^2) dt + sqrt(eta) * Sigma(W_t)^(1/2) * dB_t

The noise term sqrt(eta) scales exploration magnitude -- higher eta maintains greater stochasticity, paralleling temperature decay in annealing. The entire deep learning revolution operates on this pattern: stochastic optimization inside deterministic infrastructure.

### Compiler Optimization: Heuristic Core in a Deterministic Pipeline

Compilers present a less obvious but equally instructive example. The compilation pipeline is deterministic: lexing, parsing, semantic analysis, optimization, code generation. But within the optimization phase, many subproblems are NP-hard and solved with heuristics:

- **Register allocation**: Equivalent to graph coloring (NP-complete). Chaitin's algorithm builds an interference graph deterministically, then applies heuristic coloring. If coloring fails, variables are spilled to memory and the algorithm retries -- a deterministic fallback loop around a heuristic search.
- **Instruction scheduling**: Reorder instructions to minimize pipeline stalls, preserving semantics deterministically while making heuristic ordering decisions.

The compiler guarantees correctness (deterministic) while optimizing performance (heuristic). The user never sees the heuristic choices; they see only correct, optimized output.

### Las Vegas Algorithms: The Pattern Distilled

Las Vegas algorithms make the shell pattern explicit in algorithm theory. They wrap deterministic verification around probabilistic search: the algorithm may take unpredictable paths through solution space, but every answer is verified correct before returning. Randomness affects *when* a solution appears, not *whether* it is valid. The expected runtime is finite (ZPP complexity class), but correctness is certain.

This contrasts with Monte Carlo algorithms, which bound runtime but accept probabilistic correctness. The choice between Las Vegas and Monte Carlo is the choice between which guarantee the deterministic shell provides: correctness or timeliness.

### The Pattern Applied to LLM Agents

Every successful LLM agent framework implements the deterministic shell pattern:

| Framework | Deterministic Shell | Stochastic Core |
|-----------|-------------------|-----------------|
| **Outlines** | Finite state machine constraining valid tokens | LLM probability distribution |
| **Instructor** | Pydantic schema + retry-on-validation-failure | LLM generation |
| **NeMo Guardrails** | Colang flow engine + input/output rails | LLM reasoning |
| **Constitutional AI** | Principled self-critique + RLAIF | LLM generation |
| **ReAct** | Thought-Action-Observation template | LLM reasoning |
| **DSPy** | Compiler optimizing prompt pipelines | LLM module calls |

The Outlines library is particularly elegant: it converts structured specifications (JSON schemas, Pydantic models, grammars) into finite state machines that constrain token sampling at each generation step. The LLM generates probability scores for all possible next tokens (stochastic), but only tokens consistent with the required structure pass through the FSM filter (deterministic). Invalid structures cannot be produced. The shell does not post-process the output; it prevents invalid output from existing.

Anthropic's own architectural guidance (2025) formalizes this distinction: **workflows** are "LLMs and tools orchestrated through predefined code paths" (deterministic orchestration), while **agents** are "systems where LLMs dynamically direct their own processes and tool usage" (probabilistic reasoning). Their recommendation: start with workflows, add agency only where needed. This is engineering advice about how thick the deterministic shell should be.

---

## 2. Crystallization Dynamics: When Exploration Becomes Structure

### The Physics of Phase Transitions

Phase transitions are changes between states of matter governed by a control parameter -- typically temperature. At high temperature, systems exhibit disorder and high symmetry: molecules move freely, all configurations are accessible, the system explores widely. At low temperature, **spontaneous symmetry breaking** occurs: the system selects a specific ordered configuration. The high-temperature phase contains more symmetries than the low-temperature phase.

The order parameter quantifies organizational degree, transitioning from zero (disordered phase) to nonzero (ordered phase). The critical temperature marks where the transition occurs, and near this point, microscopic fluctuations dramatically influence macroscopic properties.

This is not merely a metaphor for agent systems. The LLM temperature parameter literally implements the Boltzmann distribution:

    p_i proportional to exp(-epsilon_i / (k_B * T))

At high T, energy differences between states matter less -- the system explores uniformly. At low T, the distribution concentrates on the lowest-energy state -- the system exploits. The ratio between two states depends only on energy *differences*:

    p_i / p_j = exp((epsilon_j - epsilon_i) / (k_B * T))

Higher-energy states become exponentially less probable as temperature drops. At T=0, only the ground state is occupied. This is crystallization.

### Simulated Annealing: The Cooling Schedule Problem

Simulated annealing makes the crystallization question explicit: **how fast should the system cool?**

The acceptance probability mirrors the Metropolis-Hastings algorithm: downhill moves are always accepted; uphill moves are accepted with probability exp(-(E_new - E) / T). At high T, nearly all moves are accepted (exploration). At low T, only improvements pass (exploitation). At T=0, the algorithm reduces to greedy search.

The cooling schedule T(k) = temperature(1 - (k+1)/k_max) determines crystallization dynamics:

- **Fast cooling** (high cooling rate): Produces amorphous structures -- the system freezes before finding good configurations. Analogous to premature optimization.
- **Slow cooling** (low cooling rate): Produces crystalline structures -- the system finds the global minimum. But may take longer than exhaustive search.
- **Adaptive cooling**: Connects the schedule to search progress. Thermodynamic simulated annealing adjusts temperature based on energy differences at each step.

The theoretical guarantee: "the probability that simulated annealing terminates with a global optimal solution approaches 1 as the annealing schedule is extended." But the caveat is severe: achieving practical confidence may require schedules longer than exhaustive search. Engineering is choosing the cooling schedule that produces acceptable solutions in acceptable time.

### Multi-Armed Bandits: Formalizing the Tradeoff

The exploration-exploitation tradeoff is formalized in the multi-armed bandit problem, where an agent must decide between exploiting the current best-known option and exploring alternatives.

**Epsilon-greedy**: Exploit the best arm with probability (1 - epsilon), explore randomly with probability epsilon. Simple but wastes exploration budget -- it does not direct exploration toward uncertain options.

**Upper Confidence Bound (UCB)**: Select the arm maximizing:

    UCB_i = x_bar_i + c * sqrt(ln(n) / n_i)

where x_bar_i is the empirical mean, n is total pulls, n_i is pulls of arm i, and c controls exploration. This directs exploration toward *uncertain* options, not random ones. The confidence bonus shrinks as an arm is explored, naturally transitioning from exploration to exploitation.

**Thompson Sampling**: Maintain a posterior distribution over each arm's reward probability. At each step, sample from each posterior and select the arm with the highest sample. This is "probability matching" -- the number of pulls matches the probability of being optimal. Naturally balances exploration (high uncertainty = high variance in samples) with exploitation (high mean = likely selected).

The **regret** formulation quantifies suboptimality:

    rho = T * mu_star - sum(r_hat_t)

where mu_star is the optimal mean reward. A zero-regret strategy achieves average regret approaching zero as rounds approach infinity. UCB achieves O(sqrt(T * K * ln(T))) regret; Thompson sampling achieves O(sqrt(K * T * ln(T))).

### Bayesian Optimization: Principled Acquisition

Bayesian optimization adds a surrogate model (typically a Gaussian process) that provides uncertainty estimates at unexplored points. The acquisition function decides where to sample next:

- **Expected Improvement (EI)**: Maximize the expected improvement over the current best
- **Probability of Improvement (PI)**: Maximize the probability of exceeding the current best
- **UCB**: Maximize mean + c * standard_deviation

The Gaussian process posterior gives both a mean prediction (what we think the value is) and uncertainty (how confident we are). The acquisition function uses both to balance exploration (high uncertainty) with exploitation (high predicted value). As more points are evaluated, uncertainty decreases everywhere, naturally cooling the exploration.

### Ashby's Ultrastability: The Cybernetic Answer

Ashby's homeostat provided the cybernetic answer to "when should exploration stop": **when Level 1 feedback achieves homeostasis.**

The two-level architecture:

- **Level 1**: Normal negative feedback loop. Continuous, fast, deterministic. The thermostat adjusting temperature. The skill executing a proven pattern.
- **Level 2**: When essential variables leave their viable range (Level 1 has failed), **random reorganization** of internal connections. Slow, exploratory, stochastic. The system tries random configurations until it finds one where Level 1 can maintain homeostasis again.

The crystallization criterion is homeostasis of essential variables. The system does not cool on a schedule. It cools **when the environment permits** -- when a configuration works. If the environment changes and the crystallized configuration fails, the system reheats (Level 2 activates) and explores again.

This is more adaptive than a cooling schedule because it is **environment-driven, not time-driven**. Simulated annealing cools regardless of whether the current solution is adequate. Ultrastability only reorganizes when the current solution fails. The compound learning ecosystem's graduation criterion -- use_count >= 3 AND outcome_score >= 2.0 -- is an ultrastability threshold: the insight crystallizes into permanent memory when it has demonstrated repeated homeostatic success.

### The Adjacent Possible: Where New Crystals Nucleate

Stuart Kauffman's theory of the adjacent possible describes how systems expand their potential through exploration. The adjacent possible is the boundary of what becomes newly accessible when current possibilities are explored. As systems interact with their environment, they open pathways into previously unreachable states.

In crystallization terms: nucleation occurs when isolated insights coalesce at the boundary of the known. The first successful application of a new pattern is the nucleus. Repeated success grows the crystal. The system does not explore uniformly; it explores at the edges of what it already knows.

### Synthesis: What Determines the Crystallization Temperature?

Across all these frameworks, the crystallization criterion converges:

| Framework | Crystallization Signal |
|-----------|----------------------|
| Simulated annealing | Energy below threshold at current temperature |
| Multi-armed bandits | Regret rate below acceptable level |
| Bayesian optimization | Expected improvement below acquisition threshold |
| Ultrastability | Essential variables within viable range |
| Evolutionary algorithms | Fitness above selection pressure |
| Phase transitions | Order parameter exceeds critical value |

The common structure: **crystallization occurs when the cost of continued exploration exceeds the expected value of undiscovered alternatives.** In a multi-armed bandit, this is when the UCB bonus is smaller than the exploitation gap. In ultrastability, this is when Level 1 maintains homeostasis. In simulated annealing, this is when T is low enough that the acceptance probability for uphill moves is negligible.

For agent systems, the practical answer: **crystallize a pattern into a skill/hook/rule when it has been validated N times with positive outcomes, and the variance of its outcomes is low enough to trust.** The graduation threshold (use_count >= 3 AND outcome_score >= 2.0) is a reasonable heuristic for this -- it requires both repeated use and consistent positive results.

---

## 3. Everything-as-Feedback Engineering

### The Cybernetic Foundation

Wiener's formalization of negative feedback as the stabilizing signal -- not the punitive one -- is the foundation. He wrote: "The information fed back to the control center tends to oppose the departure of the controlled from the controlling quantity." The thermostat does not "fail" when the room is cold. It receives a signal (temperature deviation) and acts (heat on). Bateson extended this: "Information is a difference which makes a difference." Not success or failure -- just a difference that changes the receiving system.

In information-theoretic terms: every observation reduces uncertainty. A "failed" tool call tells you something about the state space. A "wrong" approach eliminates a hypothesis. The system that treats non-working outcomes as information has **higher regulatory capacity** (higher variety) than one that discards them as errors.

The PID controller expresses feedback control mathematically:

    MV(t) = K_p * [e(t) + (1/T_i) * integral(e(tau) d_tau) + T_d * de/dt]

- **Proportional**: Current error -- how far from the setpoint
- **Integral**: Accumulated error -- systematic drift that must be corrected
- **Derivative**: Rate of change -- anticipatory correction

All three terms treat deviation as information. The P term says "you are this far off." The I term says "you have been systematically drifting." The D term says "you are moving away faster." None of these is "failure." All are feedback.

### Chaos Engineering: Netflix's Operationalization

Netflix's Chaos Monkey (2011) operationalized "everything is feedback" for distributed systems. The approach: randomly disable production servers during business hours, forcing engineers to build redundancy.

The Simian Army expanded this:
- **Chaos Monkey**: Disable individual instances
- **Chaos Gorilla**: Drop entire Availability Zones
- **Chaos Kong**: Eliminate entire AWS regions

The steady-state hypothesis: define normal operating conditions, inject failure, verify the system recovers. If it does not, that is not a "failure of the chaos experiment" -- it is **information about a real vulnerability** that would have surfaced eventually, uncontrolled.

Netflix's insight: "Knowing that this would happen frequently has created a strong alignment among engineers to build redundancy and process automation." The chaos is not the enemy. The chaos is the teacher. The deterministic harness (monitoring, alerting, automated recovery) wraps the stochastic perturbation (random instance termination) to extract learning.

Amazon's "Game Day" (2003) and Google's "DiRT" (Disaster Recovery Testing) implement the same principle: inject controlled failures to verify that backup, restore, failover, and security mechanisms actually function. Every failure teaches.

### SRE Error Budgets: Quantifying Acceptable Failure

Google's SRE practice quantifies the everything-as-feedback principle through error budgets. If a service targets 99.9% availability, the error budget is 0.1% -- approximately 43 minutes of downtime per month.

The feedback loop: when the error budget is full (few errors), the team can deploy more aggressively -- the budget permits risk. When the error budget is depleted (many errors), deployment slows until reliability improves. Errors are not "bad" -- they are **budget consumption** that informs the velocity/reliability tradeoff. A service that never uses its error budget is over-engineered; one that always exceeds it is under-engineered.

The engineering insight: **the error budget transforms the binary "is it reliable?" into a continuous signal** that dynamically adjusts development velocity. The system learns from both successes (budget preserved) and failures (budget consumed).

### Toyota Production System: Andon and Jidoka

The Toyota Production System (TPS) institutionalized everything-as-feedback in manufacturing.

**Jidoka** ("automation with a human touch"): When a machine detects a defect, it stops the entire production line. This seems wasteful -- stopping a factory is expensive. But the alternative (continuing to produce defective units) is more expensive. The stopped line creates a feedback signal: something is wrong, and it must be fixed before production resumes.

**The Andon cord**: Any worker can pull a cord to stop the line when they detect a problem. A large lighted board alerts supervisors to the problem location. This inverts the traditional authority structure -- the lowest-level worker has the power to halt the entire operation because **they are closest to the information**.

**Kaizen** (continuous improvement): Toyota commits to "improving our business operations continuously, always driving for innovation and evolution." The key mechanism is **standard work** -- documented procedures that represent the current best known method. Deviations from standard work are feedback: either the worker needs training, or the standard needs updating. Both are information.

**The crystallization cycle in TPS**: A worker discovers a better method (exploration). It is tested (validation). If it works, it becomes the new standard work procedure (crystallization). Future deviations from this new standard become feedback. This is ultrastability in manufacturing: Level 1 is standard work; Level 2 is the kaizen process that reorganizes standard work when it proves inadequate.

### Deming's System of Profound Knowledge

W. Edwards Deming formalized the feedback-not-failure philosophy through his System of Profound Knowledge:

1. **Appreciation of a system**: Understanding how feedback between organizational elements creates inherent constraints
2. **Knowledge of variation**: Recognizing "common cause" variation (system-inherent) versus "special cause" variation (addressable anomalies)
3. **Theory of knowledge**: Understanding what can and cannot be known
4. **Psychology**: Human nature's complexity

Deming's critical insight about variation: **responding to common-cause variation actually worsens performance.** If a metric fluctuates within its normal range and management reacts to each fluctuation, they introduce oscillation. Only special-cause variation (signals, not noise) warrants intervention. This is the control-theoretic principle that a regulator must model the system it regulates -- without understanding which variation is signal and which is noise, the regulator makes things worse.

His PDSA cycle (Plan-Do-Study-Act) embeds feedback into every iteration. Deming insisted on "Study" rather than "Check" because studying implies learning, while checking implies pass/fail. Every cycle produces information that informs the next cycle. There is no terminal state.

### Safety-II and Resilience Engineering

Erik Hollnagel's Safety-II framework takes everything-as-feedback to its logical conclusion in high-reliability systems. The core insight: **the work that leads to accidents is fundamentally the same as the work that leads to successful outcomes.** Workers constantly navigate conflicting goals under time pressure and limited resources. Sometimes this navigation succeeds; sometimes it fails. Studying only failures (Safety-I) introduces selection bias.

Safety-II demands studying ordinary operations comprehensively. Failures represent information about system boundaries rather than aberrations requiring elimination. Performance variability is not a bug -- it is the mechanism by which humans adapt to novel circumstances. Excessive controls can paradoxically reduce safety by constraining beneficial adaptive responses.

David Woods introduces two concepts: **graceful extensibility** (developing new capabilities when facing surprises) and **sustained adaptability** (continuing to adapt over time). These are antifragility operationalized for safety-critical systems.

### Taleb's Antifragility: Systems That Need Disorder

Nassim Taleb's triad completes the picture:

- **Fragile**: Deteriorates under stress (negative sensitivity to volatility)
- **Robust**: Resists shocks and maintains status quo
- **Antifragile**: Gains capability from stressors and disorder

"The resilient resists shocks and stays the same; the antifragile gets better."

Mathematically, antifragility is characterized by **convexity**: the response function to stressors is convex, meaning benefits increase disproportionately with volatility. A system that treats all outcomes as feedback and learns from them has a convex response to disorder -- it improves with each stressor. A system that discards failure information has a concave response -- it deteriorates under stress.

The **barbell strategy** is directly applicable to agent design: combine extremely safe, deterministic components (skills, validated patterns) with extremely exploratory, high-risk components (LLM free-form reasoning). Avoid the middle -- moderately structured, moderately risky approaches that provide neither safety nor learning. The deterministic shell is one end of the barbell; the probabilistic core is the other.

### Boyd's OODA Loop: Speed of Feedback Integration

John Boyd's OODA loop (Observe-Orient-Decide-Act) adds a temporal dimension to feedback engineering. The competitive advantage comes not from better individual decisions but from **faster feedback integration** -- getting inside the opponent's decision cycle.

The Orient phase is the differentiator: it incorporates mental models, prior experience, and cultural context. Two agents observing identical data but with different orientation frameworks will make different decisions. Boyd's insight: the Orient phase is where learning crystallizes. Superior orientation -- built from accumulated feedback -- enables faster, better decisions from the same observations.

The OODA loop enables **late commitment**: continuous feedback allows decision-makers to adapt as conditions unfold rather than rigidly executing predetermined plans. This is the opposite of waterfall planning; it is the cybernetic principle of circular causality applied to decision-making.

---

## 4. The Harness Architecture: Wrapping LLM Agents

### Variety Engineering as the Design Framework

Stafford Beer's Viable System Model provides the architectural framework for understanding harness design. The core mechanism is **variety engineering** -- managing complexity through two complementary operations:

**Variety attenuation** (filter complexity DOWN before it reaches the LLM):
- Input validation and schema enforcement
- Topic control and off-topic rejection
- Context window management and relevance filtering
- Pre-compiled briefings and knowledge scoring
- Search indexes that pre-select relevant information

**Variety amplification** (expand the deterministic shell's capacity UP):
- More tools and skills increase the agent's response repertoire
- Multi-agent coordination enables parallel exploration
- Memory systems accumulate proven patterns
- Hook systems automate recurring responses

Ashby's Law of Requisite Variety provides the hard constraint:

    V(Outcomes) >= V(Disturbances) - V(Regulator)

An agent with 5 tools handling an environment with 1000 distinguishable problem states will fail -- not because of bad prompts or wrong architecture, but because of mathematical impossibility. The harness must either attenuate environmental variety (filter before the LLM) or amplify the agent's variety (more tools, skills, patterns).

### NeMo Guardrails: Colang as Deterministic Control

NeMo Guardrails implements a flow engine that controls when and how the LLM engages. The architecture:

1. **Input rails**: Applied to user input before LLM processing. Can reject, modify, or mask sensitive data.
2. **Dialog rails**: Determine whether to invoke the LLM, use predefined responses, or execute custom actions.
3. **Output rails**: Validate or modify bot responses before returning them.
4. **Retrieval rails**: Control RAG operations.

The Colang language defines conversation flows as Python-like patterns:

```
define user express greeting
  "Hello!"
  "Good afternoon!"

define flow greeting
  user express greeting
  bot express greeting
```

This is variety attenuation: the flow engine restricts the conversation space to defined patterns. The LLM is invoked only within these patterns, never in unconstrained free-form. The deterministic flow engine is the shell; the LLM is the core.

Safety guardrails provide additional attenuation: jailbreak detection, topic safety models, content moderation, hallucination detection, and fact-checking. Each rail is a variety attenuator that reduces the space of possible outputs before the probabilistic generation selects from what remains.

### Outlines: FSM-Constrained Generation

Outlines enforces structured generation by converting schemas into finite state machines that constrain token sampling at each step. The architecture:

1. Convert structured specification (JSON schema, Pydantic model, regex, grammar) into an FSM
2. At each generation step, the FSM determines which tokens keep the output valid
3. The LLM generates probability scores for all tokens (stochastic)
4. Only valid tokens pass through the FSM filter (deterministic)
5. Sample from the filtered distribution

This eliminates post-generation parsing failures entirely: invalid structures cannot be produced. The deterministic FSM does not post-process -- it constrains generation in real-time. This is the tightest possible deterministic shell: it operates at the token level, every single step.

### Constitutional AI: Internalized Harness

Constitutional AI takes a different approach: rather than external constraints, it internalizes the harness into the model's weights through training.

**Phase 1 (Supervised Learning)**: The model generates responses, then critiques them against constitutional principles, then revises. The revised responses become training data. The constitution -- a fixed set of principles -- is the deterministic specification. The self-critique cycle is the feedback loop.

**Phase 2 (RLAIF)**: An AI evaluator compares responses against the constitution, generating preference data. A preference model trains on these AI-generated judgments. The model learns to generate constitutionally-compliant outputs without external filtering.

This is crystallization: the constitution starts as an external harness (external rules applied post-generation) and becomes an internal constraint (learned behavioral boundaries). The probabilistic core has been shaped to produce outputs that satisfy deterministic principles, internalizing the shell.

### Anthropic's Workflow Patterns as Harness Taxonomy

Anthropic's 2025 guidance identifies five deterministic workflow patterns, each representing a different harness topology:

1. **Prompt Chaining**: Sequential LLM calls with programmatic gates for validation. The gates are deterministic checkpoints; the LLM calls are probabilistic steps. This is a pipeline harness.

2. **Routing**: Classification-driven task direction to specialized handlers. The router is deterministic (if class=A, go to handler_A); the classification may be LLM-assisted but feeds into a deterministic dispatch.

3. **Parallelization**: Multiple LLM calls (stochastic) aggregated by a deterministic combiner. Sectioning runs parallel subtasks; voting runs parallel perspectives and takes the majority.

4. **Orchestrator-Workers**: A central LLM dynamically breaks tasks into subtasks, then deterministic dispatch sends each to a worker. The orchestrator is probabilistic; the dispatch and aggregation are deterministic.

5. **Evaluator-Optimizer**: Iterative refinement through feedback loops. The evaluator applies deterministic criteria; the optimizer (LLM) generates improvements. This is the closest to ultrastability: the evaluator is Level 1 feedback, and the LLM optimizer is Level 2 exploration.

### The Agent Framework Landscape

Lilian Weng's 2023 survey identifies three pillars of LLM agent architecture, all of which are harness components:

**Planning** (deterministic scaffolding):
- Chain-of-thought: "think step by step" imposes sequential structure on generation
- ReAct: Thought-Action-Observation template forces the LLM into a rigid cycle
- Reflexion: adds self-reflection and retry -- deterministic feedback loops around probabilistic reasoning

**Memory** (persistent harness state):
- Short-term: in-context examples (variety attenuation -- selecting relevant context)
- Long-term: external vector stores (variety amplification -- expanding available knowledge)

**Tool Use** (variety amplification):
- Each tool expands the agent's response repertoire
- Tool specifications are deterministic contracts; tool selection is probabilistic

The ReAct pattern deserves special attention. It forces the LLM into a repeating deterministic cycle: "Thought: ... Action: ... Observation: ..." This is a deterministic harness at the prompt level -- the structure is fixed, only the content is probabilistic. The observations (from tool calls or environment) ground the reasoning in external reality, preventing the LLM from drifting into unsupported generation.

Reflexion adds another layer: after each action, the agent computes heuristics to detect inefficient planning or hallucinations. If detected, it resets and retries with learned insights from previous failures. This is explicit everything-as-feedback: the failure is stored in working memory and informs the next attempt.

### Erlang's "Let It Crash": The Supervisor Pattern

Erlang's OTP framework provides an overlooked model for agent harness design. Rather than preventing errors through defensive programming, Erlang **assumes components will crash** and wraps them in deterministic supervisor trees.

Supervisor trees organize processes hierarchically:
- Top-level supervisors oversee child processes
- Child processes are either workers or subordinate supervisors
- When a worker crashes, the supervisor receives a message and restarts it

Joe Armstrong: "If Java is 'write once, run anywhere', then Erlang is 'write once, run forever.'" System-level reliability emerges from accepting component-level unreliability. Processes either succeed or fail completely -- they do not limp along in corrupted states. The supervisor restarts them cleanly.

This maps directly to agent architecture: LLM calls are workers that may produce invalid output (crash). The harness is the supervisor that detects the crash (validation failure) and restarts (retry with modified prompt). The system achieves reliability not by preventing LLM failures but by deterministically handling them.

### The VSM Mapping for Agent Systems

Beer's Viable System Model maps comprehensively onto agent architecture:

| VSM System | Agent Equivalent | Harness Function |
|------------|-----------------|------------------|
| **S1 (Operations)** | Individual skills, tool calls, LLM invocations | Do the actual work |
| **S2 (Coordination)** | Task scheduling, resource allocation, anti-conflict | Prevent operational units from interfering |
| **S3 (Control)** | Evaluation loops, behavioral gates, quality checks | Manage internal performance |
| **S3* (Audit)** | Integration tests, ground-truth checks, random sampling | Bypass normal reporting for truth |
| **S4 (Intelligence)** | Research capability, environment scanning, new tool discovery | Identify adaptation needs |
| **S5 (Identity)** | Constitutional principles, persistent goals, user preferences | Maintain coherent purpose across sessions |
| **Algedonic** | Critical error alerts, breakthrough discoveries | Bypass hierarchy for urgent signals |

Beer's organizational pathologies predict agent failures:
- **Missing S2**: Concurrent agents/skills interfere with each other (no coordination layer)
- **Missing S3***: Trusting self-reports instead of measuring ground truth (no audit)
- **S3 dominating S4**: Optimizing current metrics but unable to adapt (ossification -- exploring too little)
- **S4 dominating S3**: Constantly changing without stabilizing (chaos -- crystallizing too little)
- **Missing S5**: No persistent identity across sessions (drift)

The S3/S4 homeostat -- the tension between "optimize what we have" (S3) and "explore what we might need" (S4) -- IS the exploration-exploitation tradeoff, formalized as organizational structure decades before reinforcement learning named it.

---

## 5. Karpathy's autoresearch: A Concrete Case Study

### Architecture

Karpathy's autoresearch (2025) implements a deliberately minimal harness around an LLM agent that optimizes neural network architectures. The system consists of three files:

- **`prepare.py`**: Immutable. Fixed constants and one-time data preparation. This is the ground truth -- it never changes.
- **`train.py`**: The single mutable file containing the full GPT model, optimizer, and training loop. This is what the agent modifies.
- **`program.md`**: Baseline instructions for the agent. Human-edited directives.

### The Deterministic Shell

The harness enforces determinism through four mechanisms:

1. **Fixed time budget**: Every experiment runs for exactly 5 minutes of wall-clock training time. This creates comparable metrics across architectural variations -- the constraint is deterministic regardless of what the agent tries.

2. **Single metric**: Validation bits-per-byte (val_bpb) provides standardized evaluation independent of vocabulary size. There is one number, and it is computed deterministically from the model's output.

3. **Single modification surface**: The agent can only edit `train.py`. The data preparation, tokenizer, and evaluation code are immutable. This is variety attenuation -- reducing the space the agent can explore to a manageable surface.

4. **Immutable evaluation**: `prepare.py` guarantees consistent data and evaluation utilities across all experiments. The agent cannot game the metric by changing how it is computed.

### The Exploration Loop

The implicit pipeline:

1. Agent reads `program.md` for context (deterministic input)
2. Agent modifies `train.py` (probabilistic exploration)
3. 5-minute training execution (deterministic time bound)
4. Validation metric evaluation (deterministic measurement)
5. Agent decides to keep or discard changes (probabilistic decision informed by deterministic metric)
6. Loop repeats

This is ultrastability in miniature. Level 1 is the current `train.py` -- a deterministic configuration that produces a known val_bpb. Level 2 is the LLM agent exploring modifications. When a modification improves val_bpb, it becomes the new Level 1. When it does not, the system reverts.

### What autoresearch Gets Right

**Variety attenuation**: The single-file constraint, fixed time budget, and immutable evaluation code dramatically reduce the space the agent explores. It cannot change the data, the metric, or the evaluation procedure. It can only change the model architecture and training procedure within one file.

**Everything as feedback**: Every experiment produces a val_bpb number. There are no "failed" experiments -- only experiments that produced information about what works and what does not. The 5-minute budget ensures every experiment completes and produces a signal.

**Crystallization**: Successful modifications persist in `train.py`. Unsuccessful ones are discarded. Over time, the file accumulates proven patterns -- it crystallizes.

### What autoresearch Does Not Do

**No explicit memory**: The agent does not maintain a record of what it tried and what happened. Each decision is based on the current state of `train.py` and the instructions in `program.md`, not accumulated experience. This limits its ability to avoid repeating failed experiments.

**No retry/fallback logic**: If an experiment produces invalid output (e.g., the model fails to train), there is no automatic recovery. The system assumes successful execution.

**No multi-agent coordination**: A single agent operates on a single file. There is no parallelism, no specialization, no variety amplification through multiple agents.

**No adaptive crystallization threshold**: The agent decides to keep or discard changes, but there is no formal criterion (like use_count >= 3 AND outcome_score >= 2.0) for when a modification should be considered permanently crystallized versus still under evaluation.

### autoresearch as Harness Pattern Exemplar

Despite its deliberate simplicity, autoresearch cleanly demonstrates the core harness pattern:

| Component | autoresearch Implementation | General Pattern |
|-----------|---------------------------|-----------------|
| Deterministic shell | Fixed time budget, single metric, immutable eval | Constraints that bound the stochastic core |
| Stochastic core | LLM agent modifying train.py | Probabilistic exploration of the solution space |
| Feedback signal | val_bpb after each experiment | Metric that converts outcomes into information |
| Crystallization | Keeping improvements, discarding regressions | Hardening successful patterns into structure |
| Variety attenuation | Single-file constraint, immutable data | Reducing the space the agent explores |

The system's power comes from the interaction between these components, not from the sophistication of any individual component. The LLM agent is general-purpose; the harness makes it specialized.

---

## 6. Synthesis: The Unified Framework

### The Five Themes as One Structure

The five themes of this report are not parallel investigations. They are facets of a single structure:

**The deterministic shell pattern** (Theme 1) defines WHAT the harness IS -- a deterministic outer structure wrapping a stochastic inner process.

**Crystallization dynamics** (Theme 2) defines WHEN exploration becomes structure -- the cooling schedule, the UCB threshold, the ultrastability criterion that determines when a pattern has earned its place in the shell.

**Everything-as-feedback engineering** (Theme 3) defines HOW the system learns -- by treating all outcomes as information, not sorting them into success and failure categories.

**The harness architecture** (Theme 4) defines WHERE the engineering happens -- the specific components (guardrails, validators, supervisors, evaluators) that constitute the shell for LLM agents.

**autoresearch** (Theme 5) demonstrates the pattern IN PRACTICE -- a working system where these principles operate visibly.

### The Mathematical Core

The user's insight can be formalized through three equations:

**1. Ashby's Law (What the harness must provide):**

    V(Outcomes) >= V(Disturbances) - V(Regulator)

The harness must have enough variety (through attenuation of inputs and amplification of responses) to regulate the combined variety of the environment and the LLM.

**2. The Boltzmann Distribution (How exploration and crystallization relate):**

    p_i proportional to exp(-E_i / T)

At high temperature (high LLM temperature, early exploration), all configurations are accessible. At low temperature (deterministic skills, crystallized patterns), only the lowest-energy (best-performing) configurations persist. The engineering is choosing and adapting T.

**3. The Good Regulator Theorem (What the harness must contain):**

    "Every good regulator of a system must be a model of that system."

The evaluation loop must contain a model of the agent it evaluates. The improvement process must model the behavior it improves. This is not optional -- Conant and Ashby proved it in 1970.

### The Ultrastability Diagram

The user's insight maps onto Ashby's ultrastability with precision:

```
                    ENVIRONMENT
                        |
                        v
           +------------------------+
           |   DETERMINISTIC SHELL  |  <-- Skills, hooks, rules, validators
           |   (Level 1 Feedback)   |      Fast, proven, crystallized
           |                        |
           |   Essential Variables  |---> Monitored: Are outcomes acceptable?
           |   within viable range? |
           +------------------------+
                   |           |
                  YES          NO (essential variables out of range)
                   |           |
                   v           v
              [Continue    +------------------------+
               with        |   PROBABILISTIC CORE   |  <-- LLM exploration
               current     |   (Level 2 Reorganize) |     Slow, random, creative
               shell]      |                        |
                           |   Try random configs   |
                           |   until Level 1 works  |
                           +------------------------+
                                    |
                                    v
                           [New configuration found]
                                    |
                                    v
                           [Crystallize into shell]
                           (new skill, hook, or rule)
```

When the deterministic shell handles the problem (Level 1 succeeds), the probabilistic core never activates. When the shell fails (essential variables leave viable range), the LLM explores until something works, and if that pattern proves repeatable, it crystallizes into a new piece of the shell. The shell grows. The system learns.

### Connection to Existing Cybernetics Research

The previous research agents (agents 1-9 in the cybernetics session) established that this framework connects to:

- **Tsien's meta-synthesis**: Human-machine structured partnership for open complex giant systems. The user choosing what to build and when to change course (qualitative judgment) combined with the agent searching, analyzing, and executing (quantitative computation) is literally meta-synthesis.

- **Beer's POSIWID**: "The purpose of a system is what it does." If the agent claims to learn but its behavior does not measurably change, its purpose is not learning.

- **Bateson's Learning Levels**: Learning 0 = hardcoded prompts. Learning I = specific corrections (RLHF). Learning II = learning the pattern of what makes improvements stick (compound learning). Learning III = changing the principles that govern Learning II (rare, deliberate).

- **Von Foerster's eigenforms**: The engineering principles and persistent identity must survive recursive self-application. If the improvement process applied to itself does not regenerate itself, the system is unstable.

- **Friston's free energy**: Active inference -- agents minimize surprise by both updating their models (perception) and acting on the environment (action). Free energy minimization provides a unified mathematical framework: F = Expected Energy - Entropy. The harness minimizes free energy by attenuating surprise through prediction and structure.

### The Literature Gap

The broad survey agent confirmed: **zero papers apply classical cybernetics directly to LLM agent design.** The compound learning ecosystem independently rediscovered Ashby's ultrastability, Beer's variety engineering, and Tsien's meta-synthesis from engineering intuition. This convergence -- between a 70-year theoretical tradition and a 2-year-old field -- suggests the cybernetic lens is not merely applicable but natural.

---

## 7. Design Principles: Actionable Engineering Guidance

### Principle 1: Attenuate Before You Generate

**Rule**: Reduce the variety of inputs to the LLM before invocation, not after.

**Rationale**: Ashby's Law (V_O >= V_D - V_R) means the LLM must handle whatever variety reaches it. Every bit of irrelevant context, every off-topic input, every ambiguous instruction consumes the LLM's limited regulatory capacity. Attenuate first: validate inputs, select relevant context, filter noise, enforce schemas on inputs.

**Implementation**: Input rails (NeMo Guardrails), context window management (relevance scoring), pre-compiled briefings (knowledge filtering), structured prompts (ReAct templates).

### Principle 2: Constrain Generation, Don't Post-Process

**Rule**: Where possible, constrain what the LLM can generate rather than filtering invalid output after generation.

**Rationale**: Post-processing discards tokens already generated (wasted compute) and may require retry (wasted time). Constrained generation (Outlines FSM, structured decoding) prevents invalid output from existing. The deterministic shell is tighter and more efficient when it operates at the generation boundary rather than the output boundary.

**Implementation**: Outlines for structured output, Instructor for Pydantic-validated generation, grammar-constrained decoding, tool-call schemas that define valid invocations.

### Principle 3: Use Ultrastability, Not Cooling Schedules

**Rule**: Crystallize patterns based on demonstrated success, not on a timer.

**Rationale**: Simulated annealing cooling schedules are time-driven -- they cool regardless of whether the current solution is adequate. Ultrastability is environment-driven -- it crystallizes only when Level 1 feedback achieves homeostasis. For agent systems where the environment changes unpredictably, environment-driven crystallization is strictly superior.

**Implementation**: Graduation thresholds (use_count >= N AND outcome_score >= threshold). If an insight has been used 3+ times with positive outcomes, crystallize it into a skill or rule. If the environment changes and the crystallized pattern fails, de-crystallize (degrade the insight back to probabilistic exploration).

### Principle 4: Treat Every Outcome as a Bit

**Rule**: All outcomes -- success, failure, timeout, partial result, unexpected behavior -- are information that reduces uncertainty about the system and environment.

**Rationale**: In information theory, a "failed" outcome has positive Shannon information. Discarding it is literally throwing away bits. The system that processes all outcomes has higher requisite variety than one that only processes successes. This is the foundation of antifragility: convex response to stressors.

**Implementation**: Log all outcomes with structured metadata. When a tool call fails, record the input, the error, and the context. When an approach does not work, record it as a negative result that informs future attempts. Implement Reflexion-style retry that uses failure information to improve the next attempt.

### Principle 5: Build the Supervisor, Not the Worker

**Rule**: Invest engineering effort in the harness (supervisor), not in making the LLM more reliable (worker).

**Rationale**: Erlang's insight: system-level reliability emerges from accepting component-level unreliability. The LLM will sometimes produce invalid output. The engineering is in how the harness detects and recovers from this. The supervisor pattern (detect crash, restart cleanly) is more reliable and maintainable than defensive programming inside the worker.

**Implementation**: Validation layers that check LLM output against schemas. Retry logic with exponential backoff and prompt modification. Fallback chains that try simpler approaches when complex ones fail. Circuit breakers that prevent cascading failures.

### Principle 6: Match Variety to Variety

**Rule**: The agent's response repertoire must match the variety of problems it faces.

**Rationale**: Ashby's Law is not a guideline -- it is a mathematical constraint. An agent with 5 tools facing 1000 problem types will fail. Either attenuate the problem space (route only certain problems to this agent) or amplify the response space (add tools, skills, multi-agent coordination).

**Implementation**: Monitor the distribution of problems the agent encounters. When the agent fails repeatedly on a class of problems, either add a tool/skill to handle that class (variety amplification) or route that class to a different system (variety attenuation). The VSM's S4 (intelligence) system should scan for unmatched variety.

### Principle 7: Audit Independently of the Scoring System

**Rule**: The mechanism that evaluates agent performance must be independent of the mechanism the agent can influence.

**Rationale**: Goodhart's Law: when a measure becomes a target, it ceases to be a good measure. If the agent can optimize its own scores without actually improving, the scoring system collapses. Beer's S3* (audit channel) provides ground truth that bypasses normal reporting.

**Implementation**: Integration tests that check actual system behavior, not self-reported metrics. Random output sampling by an independent evaluator. External benchmarks that the agent cannot anticipate or optimize for. The audit mechanism must be uncorrelated with the scoring mechanism.

### Principle 8: Maintain the S3/S4 Balance

**Rule**: Balance optimization of current performance (S3) with exploration of new capabilities (S4). Neither should dominate.

**Rationale**: S3 dominating S4 produces ossification -- the system optimizes current metrics but cannot adapt. S4 dominating S3 produces chaos -- the system constantly changes without stabilizing. S5 (identity/purpose) exists to balance them.

**Implementation**: Allocate explicit time/compute budgets for both consolidation (compound learning, skill optimization) and exploration (research, new tool discovery, architectural experiments). Monitor the ratio and adjust. If the system has not discovered a new pattern in N sessions, increase S4 allocation. If the system has not stabilized a pattern in N sessions, increase S3 allocation.

### Principle 9: Design for Learning III (But Gate It)

**Rule**: The system should be capable of changing its own learning process (Bateson's Learning III), but this capability must be gated by S5 (identity/purpose).

**Rationale**: Learning II (learning to learn) is the target operating mode. But sometimes the learning process itself is inadequate -- the scoring function is wrong, the graduation threshold is miscalibrated, the evaluation criteria are outdated. Learning III changes these. But Learning III is dangerous: changing the principles that govern improvement can destabilize the entire system.

**Implementation**: Learning III should be rare, deliberate, and require explicit human approval. The system can propose changes to its own improvement process (S4 function), but a human must approve them (S5 gate). Eigenform test: if the proposed change is applied to itself, does the system converge to a stable state? If not, reject it.

### Principle 10: The Harness Grows; the Core Stays Probabilistic

**Rule**: Over time, the deterministic shell should grow (more skills, rules, patterns) while the probabilistic core remains general-purpose.

**Rationale**: This is the fundamental asymmetry of the system. The shell crystallizes -- it accumulates proven patterns that handle known situations deterministically. The core explores -- it handles novel situations probabilistically. As the shell grows, more situations are handled deterministically, and the core is invoked less often. But the core must remain general-purpose because novel situations are unbounded.

**Implementation**: Do not fine-tune the LLM for specific use cases (this bakes exploration into the core). Instead, crystallize patterns into the shell (skills, hooks, rules, validators). The LLM remains the general-purpose explorer; the shell is the specialized, proven structure. The harness IS the engineering.

---

## Sources

### Primary Cybernetics Sources
- Wiener, N. (1948). *Cybernetics: Or Control and Communication in the Animal and the Machine*
- Ashby, W.R. (1952). *Design for a Brain*
- Ashby, W.R. (1956). *An Introduction to Cybernetics*
- Conant, R.C. & Ashby, W.R. (1970). "Every Good Regulator of a System Must Be a Model of That System"
- Beer, S. (1972). *Brain of the Firm*
- Maturana, H. & Varela, F. (1972). *Autopoiesis and Cognition*
- Bateson, G. (1972). *Steps to an Ecology of Mind*
- Tsien, H.S. (1954). *Engineering Cybernetics*
- Von Foerster, H. (1979). "Cybernetics of Cybernetics"
- Qian, X., Yu, J., & Dai, R. (1993). "Open Complex Giant Systems"

### Control Theory and Optimization
- Metropolis, N. & Ulam, S. (1949). "The Monte Carlo Method"
- Kirkpatrick, S., Gelatt, C.D., & Vecchi, M.P. (1983). "Optimization by Simulated Annealing"
- Kalman, R.E. (1960). "A New Approach to Linear Filtering and Prediction Problems"
- Mockus, J. (1978). "The Application of Bayesian Methods for Seeking the Extremum"
- Friston, K. (2006-2022). Free Energy Principle and Active Inference papers
- Tacheny (2025). "Geometric Dynamics of Agentic Loops"

### Systems Engineering and Feedback
- Taleb, N.N. (2012). *Antifragile: Things That Gain from Disorder*
- Boyd, J. (1976). "Destruction and Creation" / OODA Loop
- Deming, W.E. (1993). *The New Economics*
- Hollnagel, E. (2014). *Safety-I and Safety-II*
- Kauffman, S. (2000). *Investigations* (Adjacent Possible)
- Alexander, C. (1977). *A Pattern Language*

### Modern AI Agent Architecture
- Bai, Y. et al. (2022). "Constitutional AI: Harmlessness from AI Feedback" (arXiv:2212.08073)
- Yao, S. et al. (2022). "ReAct: Synergizing Reasoning and Acting in Language Models"
- Shinn, N. et al. (2023). "Reflexion: Language Agents with Verbal Reinforcement Learning"
- Khattab, O. et al. (2023). "DSPy: Compiling Declarative Language Model Calls"
- Weng, L. (2023). "LLM Powered Autonomous Agents" (lilianweng.github.io)
- Anthropic (2025). "Building Effective Agents"
- Wang, Li, He, Fan et al. (2025). "AI Agent in Hall for Workshop of Metasynthetic Engineering"

### Framework Documentation
- NeMo Guardrails (NVIDIA, 2023-2025). GitHub repository and documentation
- Outlines (outlines-dev, 2023-2025). Structured generation library
- Instructor (jxnl, 2023-2025). Pydantic-validated LLM output
- Karpathy, A. (2025). autoresearch. GitHub repository

### Reliability and Feedback Engineering
- Netflix (2011). Chaos Monkey and the Simian Army
- Google SRE (2016). Error budget framework
- Toyota Production System. Jidoka, Andon, Kaizen, Standard Work
- Armstrong, J. (2003). *Programming Erlang* (Let It Crash philosophy)
