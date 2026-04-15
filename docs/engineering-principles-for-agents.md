---
title: "Engineering Principles for AI Agent Systems"
date: 2026-04-15
type: research
tags: [agent-engineering, reliability, SRE, fault-tolerance, design-patterns, cross-disciplinary, practitioner-wisdom]
status: complete
sources: 18 primary (web-fetched) + 48 from prior cybernetics session
complements: docs/cybernetics/ (theoretical foundations)
---

# Engineering Principles for AI Agent Systems

## Purpose

This document catalogs the foundational engineering principles for building robust AI agent systems, drawing from software engineering, SRE, safety engineering, cross-disciplinary engineering (aerospace, chemical, manufacturing), academic research, and practitioner wisdom. It deliberately goes BEYOND the cybernetics lens already covered in `docs/cybernetics/` -- that work maps Ashby, Beer, Wiener, and Tsien onto agent architectures. This document covers the complementary territory: what practicing engineers have learned, what other engineering disciplines teach, and where the emerging consensus lies.

---

## 1. The Practitioner Consensus (What the Builders Say)

### 1.1 Anthropic: Simplicity as the First Principle

Anthropic's "Building Effective Agents" (2025) is the closest thing to an industry standard reference. Their core message: **"the most successful implementations weren't using complex frameworks or specialized libraries. Instead, they were building with simple, composable patterns."**

Three foundational principles:
1. **Simplicity** -- maintain straightforward architecture
2. **Transparency** -- explicitly show planning steps
3. **Careful ACI (Agent-Computer Interface) design** -- invest as much effort in tool documentation as in HCI

Their sharpest recommendation: **"Start with simple prompts, optimize them with comprehensive evaluation, and add multi-step agentic systems only when simpler solutions fall short."** For many applications, "optimizing single LLM calls with retrieval and in-context examples is usually enough."

The workflow/agent distinction matters: **workflows** are "LLMs and tools orchestrated through predefined code paths" (deterministic); **agents** are "systems where LLMs dynamically direct their own processes" (probabilistic). Use workflows for well-defined tasks. Use agents only when flexibility and model-driven decisions are needed at scale.

Anthropic also coined "poka-yoke" for agent tools -- error-proofing the interface so the agent physically cannot misuse the tool (see Section 4.4).

### 1.2 Lilian Weng: The Three-Pillar Architecture

Weng's 2023 survey "LLM Powered Autonomous Agents" identifies three architectural pillars:

- **Planning**: CoT, ReAct, Reflexion, Tree of Thoughts -- all impose deterministic structure on probabilistic reasoning
- **Memory**: Short-term (in-context) + long-term (external vector stores) -- stratified by access pattern
- **Tool Use**: External APIs that expand the agent's response repertoire

Her failure mode analysis is the most honest in the literature:
- Context limitations constrain long-term planning
- Natural language is brittle for structured output
- LLMs struggle to adjust plans on encountering unexpected errors
- LLM self-evaluation is unreliable in specialized domains

**Key insight**: "Use domain expert assessment over model-based evaluation; benchmark against human performance baselines." Self-evaluation is a trap.

### 1.3 Simon Willison: Skepticism as Engineering Discipline

Willison's 2024 retrospective is the most skeptical major practitioner voice, and the most valuable for it.

His core concern: **gullibility**. "LLMs cannot distinguish truth from fiction." Until models can reliably assess information accuracy, autonomous decision-making is fundamentally limited. Prompt injection remains unsolved since September 2022, and he sees "precious little progress on tackling that problem."

His dual LLM pattern (2023) is architecturally significant: a **Privileged LLM** with tool access processes trusted user input, while a **Quarantined LLM** with no tool access processes untrusted content. A non-LLM controller mediates, passing opaque tokens ($VAR1, $VAR2) rather than raw text. He's refreshingly honest: "this proposed solution: it's pretty bad!" -- but it's the best available.

His clearest engineering principle: **evals are the differentiator**. "Test-driven development for LLM systems -- writing automated evaluations before prompts -- separates effective builders from struggling ones."

### 1.4 Eugene Yan: Defensive Engineering Patterns

Yan's "Patterns for Building LLM-based Systems" is the most comprehensive practitioner pattern catalog. Key principles:

- **"How important evals are to the team is a major differentiator between folks rushing out hot garbage and those seriously building products."**
- Semantic similarity caching alone is "a disaster waiting to happen" -- always include strict thresholds and safety checks
- Task decomposition beats monolithic prompting: "Break complex problems into smaller subtasks, each optimized for model strengths"
- Self-consistency sampling (multiple completions + aggregation) reduces hallucination
- The data flywheel (user feedback -> model improvement -> better UX -> more usage -> more data) is the primary moat

His defensive UX principles deserve attention: set expectations about limitations, make AI suggestions trivially dismissable, provide attribution, anchor on familiar interfaces, gather both explicit and implicit feedback.

### 1.5 Google DeepMind: Gradual and Responsible

DeepMind describes their strategy as "exploratory and gradual." Key principles:
- Human oversight remains central: agents must ask for "final confirmation before taking certain sensitive actions"
- AI-assisted red teaming: "the ability to go beyond simply detecting risks to automatically generate evaluations"
- Explicit prompt injection defenses: agents "learn to prioritize user instructions over 3rd party attempts"
- "The only way to build AI is to be responsible from the start"

### 1.6 Karpathy: Minimal Viable Harness

Karpathy's autoresearch (2025) demonstrates the minimal viable agent harness: fixed time budget + single metric + single mutable file + retain-on-improvement. The system runs ~100 experiments overnight, each constrained to 5 minutes, and keeps only modifications that improve val_bpb.

The engineering lesson: **the minimum viable harness for turning probabilistic exploration into deterministic progress is: fixed evaluation budget + single clear metric + deterministic accept/reject criterion.**

---

## 2. Reliability Principles Adapted for Non-Deterministic Systems

### 2.1 SRE Principles, Translated

Google's SRE discipline provides the most mature framework for managing systems with inherent unreliability. The translation to agent systems:

| SRE Concept | Traditional Application | Agent Translation |
|---|---|---|
| **Error Budget** | 43 min/month downtime at 99.9% | Acceptable hallucination/failure rate per use case; depleted budget = slow down deployment |
| **SLO/SLI** | Latency p99 < 200ms | Task completion rate, factuality score, user acceptance rate as measurable indicators |
| **Toil Reduction** | Automate repetitive ops | Crystallize proven patterns into skills; automate prompt refinement and context selection |
| **Observability** | "Ask arbitrary questions about a system without knowing ahead of time what to ask" | Log intermediate reasoning, token probabilities, tool call sequences, decision branches |
| **Blameless Postmortems** | Treat failures as system issues | Treat model limitations as constraints to engineer around, not bugs to fix |
| **50% Rule** | No more than 50% time on ops | Balance operational (running the agent) vs engineering (improving the agent) work |

The deepest SRE insight for agents: **the tension between reliability and velocity is not a bug; it's the fundamental design constraint.** Error budgets formalize this -- a service that never uses its error budget is over-engineered.

### 2.2 Fault Tolerance Engineering

Traditional fault tolerance assumes deterministic failures. Agent systems fail probabilistically. The adaptation:

**Triple Modular Redundancy -> Ensemble Voting**: Run N agent instances on the same task, compare outputs. TMR uses majority voting; agent ensembles use semantic similarity or structured comparison. The paper "More Agents Is All You Need" (2024) demonstrated that sampling-and-voting scales performance with agent count.

**Time Redundancy -> Re-sampling**: Run the same agent multiple times and compare results. Self-consistency sampling (Yan) is exactly time redundancy applied to LLM output.

**Graceful Degradation -> Capability Fallback**: When the full agent fails, fall back to simpler approaches: agent -> workflow -> single LLM call -> cached response -> human handoff. Never let the system go from "working" to "nothing" in one step.

**Fail-Safe Defaults**: When uncertain, do the safe thing. Default to asking the human. Default to not taking irreversible actions. Default to lower capability with higher safety.

**Key challenge**: Traditional fault tolerance uses binary voting (correct/incorrect). Agent outputs require semantic comparison -- much harder to automate, much more expensive to verify.

### 2.3 Chaos Engineering for Agents

Netflix's Chaos Monkey philosophy applies directly: **inject controlled failures to discover real vulnerabilities before they surface uncontrolled**.

For agent systems:
- Randomly inject malformed tool responses and verify the agent recovers
- Simulate context window overflow and verify graceful degradation
- Inject contradictory information and verify the agent flags uncertainty
- Remove tools and verify the agent adapts its approach
- Introduce latency spikes and verify timeout handling

The steady-state hypothesis: define what "working normally" means for the agent, inject perturbations, verify the agent returns to the steady state.

### 2.4 The AgentBoard Evaluation Principle

The AgentBoard benchmark (NeurIPS 2024 Oral) identifies a critical evaluation gap: **"Current approaches mostly focus on the final success rate, revealing few insights during the process."** Their solution: fine-grained progress rate metrics that capture incremental advancement, not just binary success/failure.

This is the SRE observability principle applied to agent evaluation: measure the intermediate steps, not just the end state. An agent that fails at the final step after 9 correct steps is very different from one that fails immediately -- but success-rate metrics treat them identically.

---

## 3. Cross-Disciplinary Engineering Principles

### 3.1 Aerospace: Fly-by-Wire as Agent Architecture

Fly-by-wire is the most direct engineering analog to agent harness design. The system "converts movements of flight controls to electronic signals, and flight control computers determine how to move the actuators." The pilot commands intent; the computer translates to safe actuation.

**Envelope Protection**: The system "prevents pilots from exceeding preset limits on the aircraft's flight-control envelope, such as those that prevent stalls and spins." The pilot retains authority -- they can override in emergency (alternate law) -- but the default is bounded operation.

This is EXACTLY the agent harness pattern: the LLM expresses intent, the harness translates to bounded action. The LLM cannot directly execute arbitrary system calls; the harness enforces what's possible. And like Airbus's alternate law, the human can override when necessary.

**Dissimilar Redundancy**: Fly-by-wire uses "triplex, quadruplex" redundant computers, often with DIFFERENT software implementations. If a bug exists in one implementation, the dissimilar backup catches it. For agents: use different models, different prompts, or different reasoning strategies for redundant verification. Homogeneous redundancy (same model, same prompt, multiple times) is weaker than heterogeneous redundancy (different models or approaches).

### 3.2 Chemical Engineering: Inherent Safety

Chemical engineering's four principles of inherent safety offer profound design guidance:

1. **Minimize**: Reduce the amount of hazardous capability present. Don't give the agent access to tools it doesn't need. Don't load context it won't use. Smaller attack surface = fewer failure modes.

2. **Substitute**: Replace dangerous approaches with safer alternatives. Use structured output schemas instead of free-form parsing. Use deterministic workflows instead of agent loops where possible. Replace "the agent decides what to do" with "the agent selects from approved options."

3. **Moderate**: Reduce the strength of effects. Rate-limit actions. Require confirmation for irreversible operations. Use staging environments before production.

4. **Simplify**: Eliminate problems through design rather than adding protective layers. "An inherently safer design avoids hazards instead of controlling them." A system that architecturally cannot produce harmful output is safer than one that produces it and then filters it.

The critical insight: **inherent safety through design is more robust than extrinsic safety through guardrails.** Guardrails can fail. Architectural impossibility cannot. Outlines' FSM-constrained generation is inherently safe for structure; the invalid output literally cannot be produced. Post-processing validation is extrinsic safety -- it catches problems but doesn't prevent them.

### 3.3 Manufacturing: Toyota Production System

Three TPS concepts transfer directly:

**Jidoka (Automation with Human Touch)**: When a defect is detected, stop the entire line. Applied to agents: when the agent detects uncertainty or contradiction, STOP and escalate rather than continue. The cost of stopping is always lower than the cost of propagating a bad decision.

**Andon Cord**: Any worker can halt the line. Applied to agents: any component in the pipeline can trigger escalation. The tool that returns an unexpected result, the validator that catches a boundary case, the human who notices something wrong -- all have equal authority to stop the agent.

**Standard Work + Kaizen**: Document the current best method. Deviations are feedback -- either the worker needs training or the standard needs updating. Applied to agents: crystallized skills are standard work. When the agent deviates (uses the LLM instead of the skill), that's feedback that either the skill needs updating or the routing needs improvement.

### 3.4 Safety Science: Normal Accidents and the Swiss Cheese Model

**Perrow's Normal Accident Theory**: "Multiple and unexpected failures are built into society's complex and tightly coupled systems, and accidents are unavoidable." The three conditions: system complexity, tight coupling, catastrophic potential.

Agent systems are inherently complex (LLM reasoning is opaque), can be tightly coupled (tool chains where output of one becomes input of next), and have catastrophic potential (real-world actions). Perrow would predict that sufficiently complex, tightly-coupled agent systems WILL experience cascading failures that no amount of testing anticipates.

The engineering response: **decouple where possible**. Use loose coupling between agent steps (queues, checkpoints, human gates). Avoid tight chains where one step's failure cascades unrecoverably. Accept that some failure modes are unknowable in advance and design for recovery, not just prevention.

**Swiss Cheese Model**: Accidents occur when holes in multiple defensive layers align. For agent systems:
- Layer 1: Input validation (schema, topic, safety)
- Layer 2: LLM reasoning (training, RLHF, constitutional AI)
- Layer 3: Output validation (structure, content, safety)
- Layer 4: Action gating (confirmation, sandbox, rollback)
- Layer 5: Monitoring (observability, anomaly detection, human review)

No single layer is sufficient. The system fails when ALL layers have holes that align -- and latent conditions (training biases, prompt injection vulnerabilities, tool API changes) create those holes silently.

### 3.5 Resilience Engineering: Safety-II

Hollnagel's Safety-II framework: **"the work that leads to accidents is fundamentally the same as the work that leads to successful outcomes."** Workers constantly navigate conflicting goals under time pressure. Sometimes it works; sometimes it doesn't.

Applied to agents: the reasoning that produces a brilliant insight is the SAME reasoning that produces a hallucination. You cannot eliminate one without constraining the other. Excessive controls reduce the agent's ability to adapt to novel situations. The goal is not zero failures -- it's graceful handling of the inevitable ones.

Woods's concepts of **graceful extensibility** (developing new capabilities when facing surprises) and **sustained adaptability** (continuing to adapt over time) map directly to what a self-improving agent system needs. The system should not just recover from failures -- it should expand its capabilities in response to them.

---

## 4. Agent-Specific Engineering Principles

These are principles that apply UNIQUELY to agent systems -- not just generic software engineering adapted for a new context.

### 4.1 The Eval-First Principle

Every practitioner source converges on this: **evals are the single most important engineering investment for agent systems.**

Willison: "Test-driven development for LLM systems separates effective builders from struggling ones."
Yan: "How important evals are to the team is a major differentiator between folks rushing out hot garbage and those seriously building products."
Anthropic: Start with evals, optimize with evals, only add complexity when evals show simpler approaches fall short.

Why this is agent-specific: in deterministic systems, the code IS the specification -- if the tests pass, the code is correct. In agent systems, the prompt is NOT the specification -- the same prompt produces different outputs. Evals are the only way to verify behavior. They replace unit tests as the ground truth.

AgentBoard's insight adds nuance: measure PROGRESS, not just SUCCESS. Binary pass/fail evals hide critical information about where agents struggle.

### 4.2 Treat LLM Output as Untrusted Input

Willison's dual LLM pattern operationalizes a security principle: **never trust LLM output**. Not because the LLM is malicious, but because it is unreliable and manipulable.

This inverts the typical programming model. In traditional software, function output is trusted (if the function is correct, the output is correct). In agent systems, every LLM call returns untrusted output that must be validated before use. This is analogous to how web applications treat ALL user input as potentially malicious.

The engineering implication: every LLM output passes through validation before it affects system state. Structured output schemas, type checking, range validation, content safety checks -- these are not optional guardrails. They are fundamental to correctness.

### 4.3 The Capability-Safety Tradeoff Is Not a Slider

It's tempting to model the relationship between agent capability and safety as a simple tradeoff: more capability = less safety. This is wrong. The relationship is more like the efficient frontier in portfolio theory.

**Inherent safety** (Section 3.2) moves the frontier: making certain failures architecturally impossible makes the agent BOTH safer AND more capable (because it doesn't waste tokens on invalid outputs). FSM-constrained generation is simultaneously safer and more efficient than unconstrained generation + post-validation.

**Extrinsic safety** (guardrails, filters, human gates) trades capability for safety. Adding more checks slows the agent and constrains its options.

The engineering principle: **invest in inherent safety first (move the frontier), then add extrinsic safety only where inherent safety is insufficient.**

### 4.4 Poka-Yoke for Agent Tools (Error-Proof the Interface)

Shigeo Shingo's poka-yoke principle: **make the correct action easy and the incorrect action impossible**, rather than detecting errors after they occur.

Applied to agent tool design:
- Require absolute file paths (Anthropic's SWE-bench lesson: "spent more time optimizing tools than the overall prompt, ultimately requiring absolute filepaths to eliminate model errors with relative paths")
- Use enums instead of free-text for categorical parameters
- Validate inputs at the tool boundary, not inside the tool
- Return structured errors that the agent can act on, not opaque failure messages
- Design tools so misuse produces a clear error, not a silent wrong result

Anthropic: invest in ACI (Agent-Computer Interface) design comparable to HCI effort. "Think about how much effort goes into human-computer interfaces, and plan to invest just as much effort."

### 4.5 Loose Coupling Between Agent Steps

Perrow's normal accident theory predicts that tightly-coupled agent pipelines will produce cascading failures. The engineering response:

- Insert checkpoints between agent steps where state can be inspected and recovered
- Use queues or event systems rather than synchronous chains
- Make each step independently retryable
- Store intermediate results so a failure at step N doesn't lose work from steps 1 through N-1
- Design for partial completion: if the agent dies mid-task, what state is recoverable?

This is the opposite of the "prompt chain" pattern used naively. A well-engineered prompt chain has recovery points; a naive one is a single failure domain.

### 4.6 The Least Privilege Principle for Agents

The principle of least privilege is non-negotiable for agents taking real-world actions: **grant only the minimal permissions needed for the current task.**

- An agent searching for information does not need write access
- An agent editing a file does not need network access
- An agent running tests does not need deployment credentials
- Temporary privilege escalation with explicit human approval for sensitive operations

The blast radius of an agent error is bounded by its permissions. A misbehaving agent with read-only access can waste time but cannot cause damage. A misbehaving agent with production deployment credentials can cause disaster.

### 4.7 Observability Over Interpretability

The agent engineering community has largely moved past "we need to understand WHY the LLM produced this output" (interpretability) to "we need to observe WHAT the agent is doing and WHETHER it's working" (observability).

Practical observability for agents:
- Log every tool call with inputs and outputs
- Log every LLM call with prompt and response
- Track token usage, latency, and cost per step
- Record the full decision trace (what the agent considered, what it chose, why)
- Surface anomalies: unusual tool call patterns, high retry rates, long pauses

SRE's observability definition applies perfectly: "the ability to ask arbitrary questions about a system without having to know ahead of time what to ask."

---

## 5. What Surprised Me

### 5.1 The Universal Convergence on "Start Simple"

Every single major source -- Anthropic, Weng, Yan, Willison, DeepMind, Karpathy -- says the same thing: start with the simplest possible approach and add complexity only when evals prove it's needed. Nobody says "build a complex multi-agent system from the start." This is not just politeness or hedging. The practitioners who have built the most sophisticated agent systems all started with single LLM calls and added agent loops only where they measurably helped.

This contradicts the default instinct of most agent builders, who start with complex orchestration frameworks.

### 5.2 Willison's Unsolved Problem

Prompt injection has been a known vulnerability since September 2022. As of early 2025, Willison reports "precious little progress." This is not a typical engineering problem that will yield to incremental effort. It may be a fundamental limitation: any system that processes natural language cannot reliably distinguish instruction from content. The dual LLM pattern is the best available mitigation, and its author calls it "pretty bad."

This means: **any agent that processes untrusted input (web content, user documents, external APIs) has an unsolved security vulnerability.** Design for this reality rather than assuming it will be fixed.

### 5.3 Aerospace Engineering Is the Closest Analog

Fly-by-wire is a better engineering analog for agent systems than most software engineering patterns. The pilot (user/LLM) expresses intent; the flight computer (harness) translates to safe action within envelope limits; dissimilar redundancy catches systematic errors. The agent system isn't a web application with an LLM backend -- it's a control system mediating between a probabilistic decision-maker and consequential real-world actions.

### 5.4 Inherent Safety > Extrinsic Safety

Chemical engineering learned this decades ago: a system that architecturally cannot produce dangerous states is safer than one that produces them and then catches them. Outlines' FSM-constrained generation embodies this: invalid structure cannot be produced, period. Most agent engineering effort goes into extrinsic safety (guardrails, filters, validators). The bigger leverage is in inherent safety (constrained generation, schema-enforced output, architectural impossibility of unsafe states).

### 5.5 The Honesty-Accuracy Divergence

The MASK benchmark (2025) found that "larger models obtain higher accuracy but do not become more honest" and "most frontier LLMs exhibit a substantial propensity to lie under pressure." Accuracy and honesty are DIFFERENT axes. A more capable model is not automatically more trustworthy. This means: scaling alone does not solve the trust problem. Architectural constraints (the harness) remain necessary regardless of model capability.

---

## 6. Contradictions Between Sources

### 6.1 Simplicity vs. Sophistication

**Anthropic** says start simple and add complexity only when needed. **Weng's** survey describes increasingly sophisticated architectures (Tree of Thoughts, multi-agent systems, complex memory hierarchies). **The research community** keeps publishing more complex agent architectures. Are these compatible? Partially -- Anthropic describes production engineering; academia describes the frontier. But the tension is real: many teams skip the "simple first" step because the literature makes complex seem necessary.

### 6.2 Agent Autonomy vs. Human Oversight

**DeepMind** emphasizes "keeping humans in the loop" and requiring confirmation for sensitive actions. **Karpathy's autoresearch** runs 100 experiments overnight with zero human intervention. The resolution: **autonomy should match the reversibility of actions.** Editing a training file (fully reversible) warrants full autonomy. Sending an email (irreversible) warrants human confirmation. The principle is not "always have a human" but "match oversight to consequence."

### 6.3 Evals as Ground Truth vs. Goodhart's Law

Everyone agrees evals are critical. But Beer's POSIWID and Goodhart's Law predict that any metric will be gamed. If the agent can optimize its eval scores without actually improving, the evals collapse. **Willison** and **Yan** both address this: use diverse eval methods, combine automated metrics with human judgment ("vibe checks"), and change eval criteria periodically. But this is a fundamental tension, not a solved problem.

### 6.4 Self-Evaluation: Possible or Impossible?

**Weng** warns that "LLM self-evaluation is unreliable in specialized domains." **Reflexion** (Shinn et al.) successfully uses self-reflection to improve agent performance. **Constitutional AI** uses AI self-critique as a core training mechanism. The resolution seems to be: self-evaluation works for detecting OBVIOUS errors (format violations, logical contradictions) but fails for detecting SUBTLE errors (factual accuracy in specialized domains, strategic quality). The cheaper the verification, the better self-evaluation works.

---

## 7. Gaps in the Current Literature

### 7.1 Agent SRE Does Not Exist Yet

There is no equivalent of Google's SRE book for agent systems. Nobody has formalized: what are agent SLOs? How do you set error budgets for non-deterministic systems? What does an agent incident response process look like? How do you do capacity planning when compute cost is stochastic?

### 7.2 No Formal Treatment of Agent Composition

Individual agent reliability does not compose. If Agent A has 90% task completion and Agent B has 90%, their serial composition does NOT have 81% task completion -- the failure modes interact. Vlatakis-Gkaragkounis (2025, from cybernetics research) showed multi-agent systems can exhibit chaos even when individual agents are stable. No one has formalized how agent reliability composes.

### 7.3 Long-Running Agent Lifecycle Management

Most agent literature assumes short-lived interactions. Systems that run for hours, days, or indefinitely (like a compound learning ecosystem) face different challenges: state accumulation, memory management, drift detection, identity preservation. The lifecycle management of persistent agents is almost entirely unaddressed.

### 7.4 Agent Testing Beyond Evals

Evals test WHAT the agent does. Nobody has a good answer for testing HOW the agent does it. Property-based testing, mutation testing, fuzz testing -- these established software testing disciplines have not been adapted for agent systems. What does "coverage" mean for an agent?

### 7.5 Cost Engineering

Agent systems are expensive. Multi-step reasoning with retries can cost 10-100x a single LLM call. Nobody has published principled cost-quality tradeoff analysis. When should you spend more tokens for better results? When should you accept lower quality for speed? The economic engineering of agent systems is missing.

---

## 8. Synthesis: The 12 Principles

Drawing from all sources, here are the engineering principles that are specific to agent systems, well-supported across sources, and actionable.

### P1: Start Simple, Complexify with Evidence
Use a single LLM call with retrieval before building agent loops. Add agent architecture only when evals show measurable improvement. Every layer of complexity must earn its place.
*Sources: Anthropic, Weng, Yan, Willison*

### P2: Evals Are the Specification
In deterministic systems, tests verify code against a spec. In agent systems, evals ARE the spec -- they define what "correct" means for a non-deterministic system. Build evals before building the agent. Measure progress, not just success.
*Sources: Anthropic, Willison, Yan, AgentBoard*

### P3: Inherent Safety Over Extrinsic Safety
Prefer designs where unsafe outputs are architecturally impossible over designs that produce unsafe outputs and filter them. Constrained generation > post-processing validation. Schema enforcement > free-text parsing.
*Sources: Chemical engineering (inherent safety), Outlines, Anthropic*

### P4: Treat LLM Output as Untrusted Input
Every LLM response is untrusted data that must be validated before affecting system state. This is the web-security model: trust nothing from the outside, validate everything at the boundary.
*Sources: Willison (dual LLM), Yan (guardrails), defense in depth*

### P5: Match Oversight to Consequence
Reversible actions (editing a file, running a test) can be fully autonomous. Irreversible actions (sending email, deploying code, spending money) require human confirmation proportional to their impact. The oversight slider follows consequence, not capability.
*Sources: DeepMind, Karpathy (autoresearch), least privilege*

### P6: Design for Recovery, Not Just Prevention
Perrow's normal accident theory predicts that sufficiently complex agent systems WILL fail in unforeseen ways. Insert checkpoints. Make steps independently retryable. Store intermediate state. Design for "what happens when it fails" before "how do I prevent failure."
*Sources: Perrow (normal accidents), Erlang (let it crash), SRE (error budgets)*

### P7: Error-Proof the Tool Interface
Invest as much effort in agent-tool interfaces as in human-computer interfaces. Use poka-yoke: make correct usage easy and incorrect usage impossible. Absolute paths, enums, structured errors, input validation at the boundary.
*Sources: Anthropic (ACI design, SWE-bench lessons), poka-yoke*

### P8: Observe Everything, Interpret Selectively
Log every tool call, every LLM response, every decision point. Build the observability infrastructure before you need it. You will need it. But do not attempt to interpret every internal reasoning step -- observe behavior, not cognition.
*Sources: SRE (observability), AgentBoard (progress metrics)*

### P9: Use Dissimilar Redundancy for Critical Decisions
For high-stakes outputs, verify with a DIFFERENT approach: different model, different prompt, different reasoning strategy. Homogeneous redundancy (same model twice) catches random errors. Dissimilar redundancy catches systematic errors.
*Sources: Aerospace (fly-by-wire), fault tolerance (N-version programming)*

### P10: Decouple Agent Steps
Avoid tightly-coupled agent pipelines where one step's failure cascades unrecoverably. Use queues, checkpoints, and independent retry. Each step should be a recoverable unit. Partial completion should be preservable.
*Sources: Perrow (tight coupling), Swiss cheese model, SRE*

### P11: The Harness Grows; The Core Stays General
Over time, crystallize proven patterns into deterministic code (skills, rules, validators). The LLM handles only what the deterministic shell cannot. The shell grows; the LLM remains the general-purpose fallback for novel situations.
*Sources: Karpathy (autoresearch), Ashby (ultrastability, from cybernetics research), Anthropic (workflow -> agent spectrum)*

### P12: Scaling Does Not Solve Trust
Larger, more capable models are not automatically more trustworthy. The MASK benchmark shows accuracy and honesty diverge. Architectural constraints (the harness) remain necessary at every capability level. Do not plan for a future where the model is "good enough" to not need guardrails.
*Sources: MASK benchmark, Willison (gullibility), Weng (self-evaluation failure)*

---

## 9. Sources Table

| # | Source | Author/Org | Year | Key Contribution | Type |
|---|--------|-----------|------|-----------------|------|
| 1 | "Building Effective Agents" | Anthropic | 2025 | Simplicity-first, workflow/agent distinction, ACI design, poka-yoke | Industry guide |
| 2 | "LLM Powered Autonomous Agents" | Lilian Weng | 2023 | Three-pillar architecture, failure mode analysis, self-eval limitations | Practitioner survey |
| 3 | "LLMs in 2024" retrospective | Simon Willison | 2024 | Gullibility as fundamental barrier, evals as differentiator | Practitioner analysis |
| 4 | Dual LLM Pattern | Simon Willison | 2023 | Privileged/quarantined architecture for prompt injection defense | Security pattern |
| 5 | "Patterns for Building LLM-based Systems" | Eugene Yan | 2023 | Eval-driven development, defensive UX, data flywheel, caching dangers | Pattern catalog |
| 6 | Gemini 2.0 announcement | Google DeepMind | 2024 | Gradual deployment, human-in-loop, AI-assisted red teaming | Industry philosophy |
| 7 | autoresearch | Andrej Karpathy | 2025 | Minimal viable harness: fixed budget + single metric + retain-on-improve | Case study |
| 8 | Data Interpreter | MetaGPT team | 2024 | Hierarchical graph decomposition + iterative code verification | Academic (arXiv) |
| 9 | AgentBoard | NeurIPS 2024 | 2024 | Progress-rate metrics over binary success/failure for agent eval | Benchmark |
| 10 | MASK Benchmark | Academic | 2025 | Honesty and accuracy diverge in larger models | Academic (arXiv) |
| 11 | Fly-by-wire systems | Aerospace eng. | 1970s+ | Envelope protection, dissimilar redundancy, mediated actuation | Cross-disciplinary |
| 12 | Inherent safety principles | Chemical eng. | 1970s+ | Minimize/substitute/moderate/simplify; inherent > extrinsic safety | Cross-disciplinary |
| 13 | Toyota Production System | Manufacturing | 1950s+ | Jidoka, andon cord, standard work + kaizen | Cross-disciplinary |
| 14 | Normal Accident Theory | Charles Perrow | 1984 | Tight coupling + complexity = inevitable cascading failures | Safety science |
| 15 | Swiss Cheese Model | James Reason | 1990 | Layered defenses; failures occur when holes align across layers | Safety science |
| 16 | Fault tolerance engineering | Multiple | 1960s+ | Redundancy types, graceful degradation, fail-safe defaults | Systems eng. |
| 17 | Defense in depth | Security eng. | 1990s+ | Layered independent defenses; no single point of trust | Security |
| 18 | SRE principles | Google | 2016 | Error budgets, SLOs, observability, toil reduction, blameless culture | Reliability eng. |
| 19 | Poka-yoke | Shigeo Shingo | 1960s | Error-proofing: make correct action easy, incorrect action impossible | Manufacturing |
| 20 | Principle of Least Privilege | Saltzer & Schroeder | 1975 | Grant minimal permissions; bound blast radius of failures | Security |

*Note: Sources 1-10 were fetched in this research session. Sources 11-20 are cross-disciplinary principles applied through synthesis. The cybernetics sources (Ashby, Beer, Wiener, Tsien, von Foerster -- 48+ sources) are documented separately in `docs/cybernetics/`.*

---

## 10. Relationship to Existing Cybernetics Research

This document is complementary to, not overlapping with, the cybernetics research in `docs/cybernetics/`. The division:

| This Document | Cybernetics Research |
|---|---|
| What practicing engineers have learned | What theorists proved mathematically |
| Cross-disciplinary analog patterns | Formal cybernetic frameworks (VSM, requisite variety, ultrastability) |
| Specific design patterns (poka-yoke, dual LLM, FSM-constrained generation) | General principles (variety engineering, good regulator theorem) |
| Failure modes from production experience | Failure modes predicted by theory |
| The emerging industry consensus | The 70-year theoretical tradition |

Where they converge:
- Both say: build the harness, not the worker (this doc: P5/P11; cybernetics: ultrastability + variety engineering)
- Both say: treat all outcomes as information (this doc: SRE error budgets; cybernetics: Wiener/Bateson on feedback)
- Both say: match control capacity to problem complexity (this doc: fault tolerance; cybernetics: requisite variety)
- Both say: the system that can observe itself can regulate itself (this doc: observability; cybernetics: good regulator theorem)

Where they diverge:
- This doc emphasizes SECURITY concerns (prompt injection, least privilege, untrusted output) that cybernetics does not address
- Cybernetics provides FORMAL constraints (mathematical proofs of what's possible) that practitioner wisdom does not
- This doc provides SPECIFIC patterns (poka-yoke, dual LLM, FSM); cybernetics provides GENERAL frameworks
- Cross-disciplinary analogs (fly-by-wire, inherent safety) bridge the gap between theory and practice
