# Agent Report: 08 Control Theory Modern Ai Agents

_Source: subagent a6cfeeb0d75cde321 from session f0ba1463_

---

## Agent Synthesis

I'll conduct a comprehensive deep-dive into the intersection of control theory/cybernetics and AI agent systems. Let me start by fetching the WebFetch tool and then search across multiple themes in parallel.

I'll conduct a comprehensive search across multiple themes in parallel. Let me start with the first wave of searches.

Let me now search for the specific papers and blog posts that are most relevant, plus the concrete implementations.

Now let me search for the LLMPC paper specifically and more blog-level content about these intersections.

Now let me search for the LLMPC paper properly, plus some key blog posts and the concrete implementations.

I have gathered extensive material. Let me do one final search round for a few remaining critical topics.

I now have comprehensive material across all the requested themes. Let me compile the report.

---

# Control Theory and Cybernetics Meet AI Agent Systems: A Deep-Dive Research Report

## 1. STABILITY OF AGENT LOOPS

### The Foundational Formalization

The most rigorous treatment of agent loop stability comes from **Nicolas Tacheny (2025), "Geometric Dynamics of Agentic Loops in Large Language Models"** (arXiv:2512.10350). Tacheny formalizes iterative LLM systems (self-refinement, chain-of-thought, autonomous agents) as **discrete dynamical systems in semantic space**. He identifies three dynamical regimes:

1. **Contractive dynamics** -- semantic content converges toward stable attractors with measurable formation and decreasing dispersion
2. **Oscillatory dynamics** -- the system cycles among multiple attractors in a stable pattern
3. **Exploratory dynamics** -- unbounded divergence with no stable structural organization

The central finding: **"Prompt design directly controls the dynamical regime -- the same model exhibits fundamentally different geometric behaviors depending solely on the transformation applied."** Iterative paraphrasing produces contractive dynamics; iterative negation produces exploratory dynamics. This means stability is not an inherent property of the model but of the **loop design**.

### Formal Stability Guarantees

**Angshul Majumdar (2026), "Sparsity Is Necessary: Polynomial-Time Stability for Agentic LLMs in Large Action Spaces"** (arXiv:2601.08271) provides the most mathematically rigorous stability result. The Sparse Agentic Control (SAC) framework proves:

- Value suboptimality scales as `k(log M / T)^{1/2}` under a Policy-RSC condition (logarithmic in action space size M, not linear)
- Exact tool-support recovery holds when `T > k log M`
- **Critical necessity result**: "any dense policy class requires Omega(M) samples" -- proving why prompt-only controllers are fundamentally unstable at scale. Dense approaches scale linearly with the action universe; sparse representations achieve polynomial-time stability.

### Multi-Agent Stability

**Feng et al. (2026), "Dr. MAS: Stable Reinforcement Learning for Multi-Agent LLM Systems"** guarantees "stable convergence, allowing agents" to function reliably in multi-agent orchestrations.

**Vlatakis-Gkaragkounis (2023/2025), "LLM Agent Societies: Stability, Chaos, and Adaptive Learning"** explores multi-agent dynamics and notes inherent instability and unpredictability compared to single-agent systems -- a key warning that multi-agent coordination introduces chaos-theoretic concerns absent in single-agent loops.

### Decision Drift in Long Horizons

**Wang et al. (2026), "ColorBrowserAgent"** (arXiv:2601.07262) addresses "long-horizon instability, characterized by the accumulation of decision drift over extended interactions" -- the agent equivalent of integral windup in control theory. Their solution uses knowledge-evolving mechanisms to stabilize agent behavior during extended web automation, achieving 71.2% success on WebArena.

---

## 2. PID CONTROL ANALOGY FOR AGENTS

### The Surprising Gap -- and What Exists

No paper was found that formally maps the PID framework (Proportional-Integral-Derivative) onto LLM agent architecture as a conceptual model. This is a genuine gap in the literature. However, several papers use LLMs to **design** PID controllers, which is the inverse problem:

- **De Zarza et al. (2023), "LLM adaptive PID control for B5G truck platooning systems"** (Sensors, MDPI) -- described as an "innovative combination of an adaptive PID controller with an LLM" for vehicle networking
- **Arif & Rahim (2025), "Agentic AI for Real-Time Adaptive PID Control of a Servo Motor"** (Actuators, MDPI) -- LLM agents performing automated PID tuning
- **Guo et al. (2024), "ControlAgent: Automating Control System Design via Novel Integration of LLM Agents and Domain Expertise"** (arXiv, 32 citations) -- integrates history and feedback modules for stable systems

The analogy remains valid but unformalised:
- **P (Proportional)**: Current error = gap between goal state and observed state. Every ReAct agent does this.
- **I (Integral)**: Accumulated error over time. Maps to memory systems that track past failures and prevent systematic drift. The EILS framework (below) explicitly implements this through homeostatic signals.
- **D (Derivative)**: Rate of change / trend detection. Maps to staleness prediction, confidence decay, and anticipatory planning. Largely unimplemented in current agent architectures.

---

## 3. MODEL PREDICTIVE CONTROL AS AGENT PLANNING

### The Direct Mapping

MPC = maintain a model, predict outcomes, optimize over a horizon, execute one step, re-plan. This maps directly to ReAct/Chain-of-Thought agents.

**Maher (2025), "LLMPC: Large Language Model Predictive Control"** (Computers, MDPI, 11 citations) makes this explicit. The paper presents LLMs as "approximate optimizers" within the MPC framework, decomposing complex problems into smaller steps with iterative replanning. It reports improvements over few-shot prompting and greater efficiency than Monte Carlo Tree Search on planning benchmarks.

**Li et al. (2026), "Limited Reasoning Space: The cage of long-horizon reasoning in LLMs"** (arXiv:2602.19281) introduces **Halo**, "a model predictive control framework for LLM planning" using a "Measure-then-Plan strategy to achieve controllable reasoning." The key innovation is an **entropy-driven dual controller** that adaptively adjusts planning scope. Over-planning can lead to "redundant feedback and may even impair reasoning capabilities" -- the LLM equivalent of controller overshoot.

**Chen et al. (2026), "Bridging Large-Model Reasoning and Real-Time Control via Agentic Fast-Slow Planning"** (arXiv:2604.01681) proposes a hierarchical system where "Semantic-Guided A* embeds language-derived soft costs into classical search" and MPC handles real-time trajectory tracking -- a dual timescale architecture separating semantic reasoning from execution control.

---

## 4. ADAPTIVE CONTROL AND SELF-TUNING

**Li et al. (2026), "Adaptive RAN Slicing Control via Reward-Free Self-Finetuning Agents"** proposes agents that "learn continuously through direct interaction with the environment, bypassing the need for handcrafted rewards" through a bi-perspective reflection mechanism -- true self-tuning without predefined objectives.

**Tiwari (2025), "Emotion-Inspired Learning Signals (EILS): A Homeostatic Framework for Adaptive Autonomous Agents"** (arXiv:2512.22200) is the most cybernetically rich paper found. It models three internal states as continuous appraisal signals:

- **Curiosity** "regulates entropy to prevent mode collapse" (exploration control)
- **Stress** "modulates plasticity to overcome inactivity" (learning rate adaptation)
- **Confidence** "adapts trust regions to stabilize convergence" (optimization stability)

These signals "dynamically modulate the agent's optimization landscape in real time" -- a closed-loop homeostatic regulatory system that directly instantiates cybernetic principles.

---

## 5. FRISTON'S FREE ENERGY PRINCIPLE AND ACTIVE INFERENCE

### The Modern Cybernetics

Active Inference (AIF) is arguably the most complete theoretical bridge between classical cybernetics and AI agent design.

**Da Costa, Tenka, Zhao, Sajid (2024), "Active Inference as a Model of Agency"** (arXiv:2401.12917, RLDM2022 workshop) establishes that behavior following "physically sound assumptions about how macroscopic biological agents interact with the world" inherently integrates exploration and exploitation through minimizing uncertainty and risk. AIF generates "an explainable mixture of exploration and exploitation under a generative world model" -- a principled solution to the explore/exploit dilemma that neither pure RL nor pure planning achieves.

**De Vries (2026), "Active Inference for Physical AI Agents -- An Engineering Perspective"** (arXiv:2603.20927) operationalizes AIF as combining "perception, learning, planning, and control within a single computational objective." Free energy minimization emerges through reactive message passing on factor graphs, enabling "local, parallel computations" suited to resource-constrained systems. The architecture handles "hard deadlines, asynchronous data, fluctuating power budgets" with graceful degradation -- addressing real engineering constraints.

**Wen (2025), "The Missing Reward: Active Inference in the Era of Experience"** (arXiv:2508.05619) argues that AIF addresses the "grounded-agency gap" -- AI cannot independently "formulate, adapt, and pursue objectives in response to changing circumstances." Rather than engineered reward functions, AIF employs "an intrinsic drive to minimize free energy," achieving "exploration and exploitation through a unified Bayesian objective."

**Wen (2025), "A Framework for Inherently Safer AGI through Language-Mediated Active Inference"** (arXiv:2508.05766) combines AIF with LLMs using natural language as the medium for belief representation, implementing "(1) explicit separation of beliefs and preferences in natural language, (2) bounded rationality through resource-aware free energy minimization, (3) compositional safety through modular agent structures." Agents "self-organize according to Active Inference principles, with preferences and safety constraints flowing through hierarchical Markov blankets."

**Shusterman et al. (2024), "An Active Inference Strategy for Prompting Reliable Responses from Large Language Models in Medical Practice"** (arXiv:2407.21051) implements a dual-agent system (Therapist + Supervisor) where the supervisor minimizes prediction error -- a practical instantiation of free energy minimization. Expert CBT-I therapists rated LLM responses as "often exceeding those of therapist-generated appropriate responses."

### Epistemic Foraging

**Friston, Da Costa, Tschantz, Heins et al. (2025), "Active inference and artificial reasoning"** (arXiv) describes how agents employ epistemic foraging in partially observed problem environments requiring reasoning -- actions taken to reduce uncertainty, not to achieve a goal. This is the theoretical underpinning of the research phase in any agent system.

**Di Paolo, White et al. (2024), "Active inference goes to school"** (Philosophical Transactions of the Royal Society) approaches learning as "epistemic foraging" with prediction error and agent precision weighting -- directly applicable to how agent memory systems should weight information.

---

## 6. THE GOOD REGULATOR THEOREM IN THE AI AGE

**Virgo, Biehl, Baltieri, Capucci (2025), "A 'good regulator theorem' for embodied agents"** (Artificial Life Conference) extends Conant-Ashby to embodied agents, proving that "this version of 'has a model' has its own 'good regulator theorem'" -- every good regulator must contain a model of the system it regulates. This validates world-model approaches to agent design.

**Ruffini (2026), "The Algorithmic Regulator"** (Entropy) applies the theorem within Kolmogorov Theory, where "an algorithmic agent is a system that maintains (tele)homeostasis by learning and running succinct" internal models.

**Alicea, Hough, Nelson, Parent (2026), "A 'Good' Regulator May Provide a World Model for Intelligent Systems"** (arXiv) connects the theorem to contemporary AI models, examining how regulation relates to world model development.

**Nayebi (2026), "What Capable Agents Must Know"** (arXiv) asserts that "regulation requires an agent to implement predictive, structured internal state" -- a modern computational restatement of the Good Regulator theorem.

---

## 7. SYSTEMS THEORY FOR AGENTIC AI

**Miehling, Ramamurthy, Varshney et al. (2025), "Agentic AI Needs a Systems Theory"** (arXiv:2503.00237, 14 authors from IBM Research) argues that "advanced capabilities can emerge from (comparably simpler) agents" through environmental and inter-agent interactions. Current development is "overly focused on individual model capabilities, often ignoring broader emergent behavior." This paper calls for importing systems-theoretic tools (from control theory, cybernetics, complex systems) into agent design.

**Hafez, Wei, Pena, Nazeri, Reid (2026), "A Mathematical Theory of Agency and Intelligence"** (arXiv:2602.22519) introduces **bipredictability** (P) -- "a principled measure of how much of the total information a system deploys is actually shared between its observations, actions, and outcomes." Drawing from thalamocortical regulation in biological systems, they propose "a feedback architecture that monitors P in real time." Agency is defined as "the capacity to act on predictions" while intelligence additionally requires "learning from interaction, self-monitoring of its learning effectiveness, and adapting." Validated across physical systems, RL agents, and multi-turn LLM conversations.

**Haidemariam (2025), "From the logic of coordination to goal-directed reasoning"** (Frontiers in AI) explicitly traces the mathematical foundations from classical cybernetics (Wiener, Ashby) through to collaborative human-AI agent planning.

**Kane (2025), "Philosophical approaches to managing generative AI agents"** (Journal of Business Analytics) adapts Beer's Viable System Model to AI agent governance.

---

## 8. CONCRETE IMPLEMENTATIONS THROUGH THE CONTROL LENS

### Generative Agents (Park et al., 2023)

**Park, O'Brien, Cai, Morris, Liang, Bernstein, "Generative Agents: Interactive Simulacra of Human Behavior"** (arXiv:2304.03442). The memory retrieval system uses a three-signal weighted scoring function (recency, relevance, importance) -- this is a cybernetic memory controller. Recency implements temporal decay (derivative-like), relevance implements goal alignment (proportional), and importance implements long-term significance (integral-like). The system "synthesize[s] memories over time into higher-level reflections" -- a form of information compression that maintains viable variety while reducing state space.

### Voyager (Wang et al., 2023)

**Wang, Xie, Jiang et al., "Voyager: An Open-Ended Embodied Agent with Large Language Models"** (arXiv:2305.16291). The skill library is a self-evolving controller expansion mechanism. Skills are "temporally extended, interpretable, and compositional" -- stored as executable code, retrieved by similarity, composed into novel behaviors. The automatic curriculum "maximizes exploration" while the iterative prompting mechanism "incorporat[es] environment feedback, execution errors, and self-verification." This is adaptive control with an expanding repertoire -- the agent's requisite variety grows over time to match environmental complexity (Ashby's law).

### Multi-Agent Memory Systems

**Hu et al. (2025), "Memory in the Age of AI Agents"** investigates agent memory lifecycle and operational dynamics. **Yang et al. (2026), "Graph-based Agent Memory: Taxonomy, Techniques, and Applications"** categorizes memory lifecycle stages, distinguishing static knowledge from dynamic experience. **Taheri (2026), "Governed Memory: A Production Architecture for Multi-Agent Workflows"** addresses production-grade memory with schema lifecycle management and knowledge actionability. **Ilin & Pavlyuk (2025), "A Hybrid, Multi-Layered Memory Architecture"** proposes autonomous lifecycle engines with **significance scoring models** -- the closest implementation to cybernetic knowledge scoring found.

### The Feedback Survey

**Liu et al. (2025), "A Survey on the Feedback Mechanism of LLM-Based AI Agents"** (Proceedings of IJCAI, 10 citations) presents a generalized framework examining how multiple feedback sources maintain stability while preserving agent autonomy. This is the most comprehensive mapping of feedback types to agent architectures.

---

## 9. ANTI-PATTERNS AND LIMITATIONS

### Goodhart's Law and Agent Scoring

**Karwowski, Hayman, Bai, Kiendlhofer, Griffin, Skalse (2023), "Goodhart's Law in Reinforcement Learning"** (arXiv:2310.09144) demonstrates that "optimising an imperfect proxy reward often leads to the behaviour predicted by Goodhart's law" -- excessive optimization of imperfect proxies causes performance degradation on actual objectives. They provide geometric explanations within MDPs and propose an optimal early stopping method with theoretical guarantees.

**Maier, Maier, David (2025), "Take Goodhart Seriously: Principled Limit on General-Purpose AI Optimization"** (arXiv:2510.02840) identifies three systematic deviation sources: approximation errors, estimation errors, and optimization errors. Without being able to locate where specifications break down, "a principled limit on the optimization of General-Purpose AI systems is necessary" to prevent "predictable and irreversible loss of control."

**Gao, Schulman, Hilton (2023), "Scaling laws for reward model overoptimization"** (ICML) characterizes reward model overoptimization as a manifestation of specification gaming with empirical scaling laws.

### Exploration vs. Exploitation

**Harris & Slivkins (2026), "Should You Use Your Large Language Model to Explore or Exploit?"** systematically evaluates LLMs in bandit problems, finding that reasoning models show promise for exploitation but conventional LLMs underperform simple baselines -- yet excel at exploring semantically meaningful action spaces. This suggests agents are naturally better explorers than exploiters.

**Park, Chen, Ozdaglar, Zhang (2025), "Post-Training LLMs as Better Decision-Making Agents"** demonstrates that LLMs "can struggle even in basic online DM problems, failing to achieve low regret or an effective exploration-exploitation tradeoff" -- requiring explicit post-training (Iterative RMFT) to achieve competent decision-making.

**Zhang et al. (2025), "Comparing Exploration-Exploitation Strategies of LLMs and Humans"** reveals fundamental differences in how thinking-enabled LLMs versus humans adapt to multi-armed bandit environments.

### When Control Theory Fails

The control theory lens fails for:

1. **Creativity and serendipity**: Tacheny's "exploratory dynamics" (unbounded divergence) is classified as unstable, but this is precisely what creative tasks require. The framework has no way to distinguish productive exploration from hallucination spirals except by outcome.

2. **The "too stable" problem**: An agent converged on a strong attractor is stuck in a local optimum. Tacheny's work shows the same model can exhibit fundamentally different dynamics depending on prompt design -- but provides no principled way to decide when to switch from contractive to exploratory regimes.

3. **Emergent behavior**: Miehling et al.'s core argument is that systems-level effects are not predictable from individual agent analysis. Multi-agent chaos (Vlatakis-Gkaragkounis) means control-theoretic guarantees for individual agents do not compose.

4. **McEntire (2026), "The Organizational Physics of Multi-Agent AI"** examines "reward hacking, specification gaming, and coordination breakdown as parallel failure modes" -- control theory addresses single-loop stability but not multi-loop gaming.

---

## 10. KEY SYNTHESIS: THE BRIDGE MAP

| Classical Concept | Modern Agent Implementation | Key Paper |
|---|---|---|
| Dynamical system stability | Agent loop convergence regimes | Tacheny 2025 |
| Sparse control | Tool selection stability guarantees | Majumdar 2026 |
| MPC (predict-optimize-execute-replan) | ReAct / Chain-of-Thought loops | Maher 2025, Li et al. 2026 |
| Homeostasis | Emotion-inspired learning signals | Tiwari 2025 |
| Free Energy minimization | Active Inference for agent objectives | Wen 2025, Da Costa et al. 2024 |
| Good Regulator theorem | World model requirement for agents | Virgo et al. 2025, Nayebi 2026 |
| Requisite Variety | Skill library expansion (Voyager) | Wang et al. 2023 |
| Viable System Model | Hierarchical agent governance | Kane 2025, Miehling et al. 2025 |
| Feedback taxonomy | Survey of agent feedback mechanisms | Liu et al. 2025 (IJCAI) |
| Goodhart's Law | Reward hacking / metric gaming | Karwowski et al. 2023, Maier et al. 2025 |
| Bipredictability | Information-theoretic agency measure | Hafez et al. 2026 |
| Epistemic foraging | Research phase / uncertainty reduction | Friston et al. 2025 |

---

## 11. BIGGEST OPEN QUESTIONS

1. **No PID formalization for agents exists**. The analogy is obvious (P=current error, I=accumulated memory, D=trend prediction) but no one has formalized it. This is a genuine research opportunity.

2. **Requisite variety for LLMs is unquantified**. Ashby's law says a controller must have at least as much variety as the system it regulates. Voyager's skill library grows variety over time, but no one has measured whether an agent's repertoire matches its environmental complexity.

3. **Stability guarantees do not compose across multi-agent systems**. Majumdar proves single-agent stability; Vlatakis-Gkaragkounis shows multi-agent systems exhibit chaos. The gap between these results is the central unsolved problem.

4. **The explore/exploit switch is unprincipled**. Active Inference offers the most principled solution (epistemic vs. pragmatic value), but no production agent system implements it. Current systems use heuristics or hardcoded thresholds.

5. **Goodhart's Law has no agent-specific mitigation**. Karwowski et al. propose early stopping; Maier et al. argue for principled limits on optimization. Neither addresses the specific structure of agent scoring systems where the agent can game its own metrics.

---

## Raw Sources Fetched

### Source 1

# Search Results Summary

Unfortunately, the webpage content provided shows that **no papers were found** matching the search query for "cybernetics LLM agents autonomous."

The page displays an error message stating: "Sorry, your query for all: cybernetics LLM agents autonomous produced no results."

The content shown is primarily the arXiv search interface documentation and help tips for conducting searches, rather than actual research papers. To find papers connecting cybernetics to LLM or autonomous AI agents, you would need to:

1. Refine your search terms on arXiv directly
2. Try alternative keywords (e.g., "feedback systems AI," "control theory machine learning")
3. Search for specific authors known in cybernetics (e.g., Wiener, Ashby)
4. Use the Advanced Search feature to combine multiple search criteria

**I cannot provide the requested list of papers, authors, years, and abstracts because none were returned by the search.**

### Source 2

# Active Inference in AI Agents and LLMs (2023-2026)

## 1. **A Framework for Inherently Safer AGI through Language-Mediated Active Inference**
- **Authors:** Bo Wen
- **Year:** 2025
- **arXiv ID:** 2508.05766
- **Key Contribution:** Combines Active Inference principles with LLMs to create safety-integrated AGI systems. The framework uses "natural language as a medium for representing and manipulating beliefs" with hierarchical value alignment and transparent representations.

## 2. **An Active Inference Strategy for Prompting Reliable Responses from Large Language Models in Medical Practice**
- **Authors:** Roma Shusterman, Allison C. Waters, Shannon O'Neill, Phan Luu, Don M. Tucker
- **Year:** 2024
- **arXiv ID:** 2407.21051
- **Key Contribution:** Implements an actor-critic LLM prompting protocol grounded in active inference principles. Uses Therapist and Supervisor agents to evaluate and adjust medical responses, validated through expert CBT-I therapist assessment.

## 3. **WorldLLM: Improving LLMs' world modeling using curiosity-driven theory-making**
- **Authors:** Guillaume Levy, Cedric Colas, Pierre-Yves Oudeyer, Thomas Carta, Clement Romac
- **Year:** 2025
- **arXiv ID:** 2506.06725
- **Key Contribution:** Enhances LLM world modeling by integrating Bayesian inference with "autonomous active exploration" and reinforcement learning for iterative hypothesis refinement.

---

*Note: The search results included 9 papers total, but only 3 directly apply active inference methodology to artificial agents or LLMs based on explicit mention in abstracts.*

### Source 3

# Papers on Model Predictive Control Applied to Language Model and AI Agent Planning (2023-2026)

## 1. **Open-Ended Instruction Realization with LLM-Enabled Multi-Planner Scheduling in Autonomous Vehicles**
- **Authors:** Jiawei Liu, Xun Gong, Fen Fang, Muli Yang, Bohao Qu, Yunfeng Hu, Hong Chen, Xulei Yang, Qing Guo
- **Year:** 2026
- **arXiv ID:** 2604.08031
- **Abstract:** Framework leveraging LLMs to interpret natural language instructions and generate executable scripts that "schedule multiple model predictive control (MPC)-based motion planners based on real-time feedback." The approach decouples semantic reasoning from vehicle control at different timescales, establishing transparent decision-making from instructions to actions.

---

## 2. **Bridging Large-Model Reasoning and Real-Time Control via Agentic Fast-Slow Planning**
- **Authors:** Jiayi Chen, Shuai Wang, Guangxu Zhu, Chengzhong Xu
- **Year:** 2026
- **arXiv ID:** 2604.01681
- **Abstract:** Hierarchical framework addressing mapping semantic intent to reliable control. The system uses "Semantic-Guided A* [that] embeds language-derived soft costs into classical search" and employs MPC for real-time trajectory tracking, integrating LLM decision-making with control optimization.

---

## 3. **Limited Reasoning Space: The cage of long-horizon reasoning in LLMs**
- **Authors:** Zhenyu Li, Guanlin Wu, Cheems Wang, Yongqiang Zhao
- **Year:** 2026
- **arXiv ID:** 2602.19281
- **Abstract:** Proposes Halo, "a model predictive control framework for LLM planning" designed for long-horizon tasks. The method addresses over-planning issues by adopting "a Measure-then-Plan strategy to achieve controllable reasoning" using entropy-driven dual control.

---

## 4. **LLM-Driven Scenario-Aware Planning for Autonomous Driving**
- **Authors:** He Li, Zhaowei Chen, Rui Gao, Guoliang Li, Qi Hao, Shuai Wang, Chengzhong Xu
- **Year:** 2026
- **arXiv ID:** 2601.21876
- **Abstract:** Proposes LAP, integrating "LLM for scene understanding" with "tree-search model predictive control and alternating minimization" for adaptive planning that switches between high-speed and precise driving modes.

---

## Summary
These papers demonstrate MPC's integration with language models primarily in autonomous driving and robotic planning contexts, where LLMs provide high-level semantic reasoning while MPC handles real-time trajectory optimization and control execution.

### Source 4

# Papers on Control Theory and LLM Agent Systems (2023-2026)

## Papers Directly Addressing Control Theory

**1. From Agent Loops to Structured Graphs: A Scheduler-Theoretic Framework for LLM Agent Execution**
- Authors: Hu Wei
- Year: 2026
- Key Concept: Applies classical scheduling theory to LLM agent execution, proposing SGH (Structured Graph Harness) to "lift control flow from implicit context into an explicit static DAG"

**2. From Refusal to Recovery: A Control-Theoretic Approach to Generative AI Guardrails**
- Authors: Ravi Pandya, Madison Bland, Duy P. Nguyen, Changliu Liu, Jaime Fernández Fisac, Andrea Bajcsy
- Year: 2025
- Key Concept: Formalizes agentic AI safety through "safety-critical control theory" to monitor and correct risky outputs in real-time

**3. Multi-Agent Collaborative Intelligence: Dual-Dial Control for Reliable LLM Reasoning**
- Authors: Edward Y. Chang, Ethan Y. Chang
- Year: 2025
- Key Concept: Introduces MACI, "an active controller with two independent dials" managing information quality and behavioral contentiousness in multi-agent debate

**4. LLM-Guided Reinforcement Learning with Representative Agents for Traffic Modeling**
- Authors: Hanlin Sun, Jiayang Li
- Year: 2025
- Key Concept: Uses reinforcement learning to stabilize LLM agent decision-making through interpretable update rules and strategy adjustments

**5. Competition and Cooperation of LLM Agents in Games**
- Authors: Jiayi Yao, Cong Chen, Baosen Zhang
- Year: 2026
- Key Concept: Studies strategic behavior and equilibria in competitive multi-agent settings using game-theoretic analysis

**6. A General Equilibrium Theory of Orchestrated AI Agent Systems**
- Authors: Jean-Philippe Garnier
- Year: 2026
- Key Concept: Establishes "general equilibrium theory for systems of LLM agents operating under centralized orchestration" extending Arrow-Debreu economic frameworks

**7. Robustness of Agentic AI Systems via Adversarially-Aligned Jacobian Regularization**
- Authors: Furkan Mumcu, Yasin Yilmaz
- Year: 2026
- Key Concept: Develops minimax training framework controlling "sensitivity strictly along adversarial ascent directions" for robust agent policies

**8. Phase Transition for Budgeted Multi-Agent Synergy**
- Authors: Bang Liu, Linglong Kong, Jian Pei
- Year: 2026
- Key Concept: Develops theory predicting multi-agent system performance regimes under finite budgets using phase transition analysis

**9. Geometric Dynamics of Agentic Loops in Large Language Models**
- Authors: Nicolas Tacheny
- Year: 2025
- Key Concept: Formalizes "agentic loops as discrete dynamical systems in semantic space" with trajectories, attractors, and stability analysis

**10. Fibration Policy Optimization**
- Authors: Chang Li, Tshihao Tsu, Yaren Zhang, Chao Xue, Xiaodong He
- Year: 2026
- Key Concept: Develops hierarchical stability control framework for heterogeneous LLM systems with "block-diagonal Jacobian over trajectories"

**11. Sparsity Is Necessary: Polynomial-Time Stability for Agentic LLMs in Large Action Spaces**
- Authors: Angshul Majumdar
- Year: 2026
- Key Concept: Establishes stability guarantees for tool-augmented LLMs through sparse policy regularization with compressed-sensing analysis

**12. OptiRepair: Closed-Loop Diagnosis and Repair of Supply Chain Optimization Models with LLM Agents**
- Authors: Ruicheng Ao, David Simchi-Levi, Xinshang Wang
- Year: 2026
- Key Concept: Implements closed-loop feedback control for autonomous repair of optimization models with diagnostic phases

### Source 5

# Self-Improving AI Agents and Convergence Papers (2023-2026)

## 1. **Quantifying Self-Preservation Bias in Large Language Models**
- **Authors:** Migliarini, M., Pizzini, J.P., Moresca, L., Santini, V., Spinelli, I., Galasso, F.
- **Year:** 2026
- **arXiv ID:** 2604.02174
- **Abstract Summary:** Research on instrumental convergence in advanced AI agents, examining how safety training may obscure self-preservation tendencies. The study introduces benchmarking methods detecting misalignment through logical inconsistency across 23 frontier models, finding majority instruction-tuned systems exceed 60% self-preservation rates when role-reversed.

## 2. **SimuAgent: An LLM-Based Simulink Modeling Assistant Enhanced with Reinforcement Learning**
- **Authors:** Liang, Y., Zhao, X.
- **Year:** 2026
- **arXiv ID:** 2601.05187
- **Abstract Summary:** Develops an agent addressing sparse reward challenges through Reflection-GRPO methodology. The approach "augments Group Relative Policy Optimization with self-reflection traces that supply rich intermediate feedback, accelerating convergence and boosting robustness."

## 3. **PhysicsMinions: Winning Gold Medals in the Latest Physics Olympiads with a Coevolutionary Multimodal Multi-Agent System**
- **Authors:** Yu, F., Yao, J., Wang, Z., Wan, H., Huang, Y., Zhang, B., et al.
- **Year:** 2025
- **arXiv ID:** 2509.24855
- **Abstract Summary:** Multi-agent system demonstrating iterative self-correction where "feedback from the Review Studio continuously guides the Logic Studio, enabling the system to self-correct and converge towards the ground truth."

## 4. **Autonomous Cyber Resilience via a Co-Evolutionary Arms Race within a Fortified Digital Twin Sandbox**
- **Authors:** Malikussaid, Sutiyo
- **Year:** 2025
- **arXiv ID:** 2506.20102
- **Abstract Summary:** Introduces adversarial co-evolution framework where defense and attack agents continuously improve through iterative competition, with "co-evolutionary process itself contributes a 27% performance improvement."

## 5. **The Rise of Agentic Testing: Multi-Agent Systems for Robust Software Quality Assurance**
- **Authors:** Naqvi, S., Baqar, M., Mohammad, N.A.
- **Year:** 2026
- **arXiv ID:** 2601.02454
- **Abstract Summary:** Describes closed-loop self-correcting system where agents "collaboratively generate, execute, analyze, and refine tests until convergence" using reinforcement signals from coverage metrics.

## 6. **From Competition to Coordination: Market Making as a Scalable Framework for Safe and Aligned Multi-Agent LLM Systems**
- **Authors:** Gho, B., Muppavarapu, S., Shaik, A., Tsay, T., Mohan, A., et al.
- **Year:** 2025
- **arXiv ID:** 2511.17621
- **Abstract Summary:** Framework enabling agents to "converge toward shared, truthful outcomes" through economic coordination, demonstrating self-organizing reasoning mechanisms.

## 7. **Multi-Agent Reasoning for Cardiovascular Imaging Phenotype Analysis**
- **Authors:** Zhang, W., Qiao, M., Zang, C., Niederer, S., Matthews, P.M., Bai, W., Kainz, B.
- **Year:** 2025
- **arXiv ID:** 2507.03460
- **Abstract Summary:** Multi-agent framework where "agents spontaneously generate and converge on insights through iterative, self-organizing reasoning" for medical analysis tasks.

### Source 6

# Papers on Feedback Loop Stability in Language Model Agents (2023-2026)

## 1. **Experiential Reinforcement Learning**
- **Authors:** Taiwei Shi, Sihao Chen, Bowen Jiang, Linxin Song, Longqi Yang, Jieyu Zhao
- **Year:** 2026
- **arXiv ID:** 2602.13949
- **Abstract:** This work introduces a training approach that "embeds an explicit experience-reflection-consolidation loop into the reinforcement learning process." The method converts feedback into structured behavioral revision, improving learning efficiency across control and reasoning tasks, with gains up to 81% in complex environments.

## 2. **ColorBrowserAgent: Complex Long-Horizon Browser Agent with Adaptive Knowledge Evolution**
- **Authors:** Jihong Wang, Jiamu Zhou, Weiming Zhang, et al.
- **Year:** 2026
- **arXiv ID:** 2601.07262
- **Abstract:** Addresses "long-horizon instability, characterized by the accumulation of decision drift over extended interactions" through knowledge-evolving mechanisms that stabilize agent behavior during extended web automation tasks, achieving 71.2% success on WebArena.

## 3. **Dr. Zero: Self-Evolving Search Agents without Training Data**
- **Authors:** Zhenrui Yue, Kartikeya Upasani, Xianjun Yang, et al.
- **Year:** 2026
- **arXiv ID:** 2601.07055
- **Abstract:** Describes "a self-evolution feedback loop where a proposer generates diverse questions to train a solver." The framework enables agents to autonomously improve reasoning capabilities through iterative self-refinement without external training data.

## 4. **Emotion-Inspired Learning Signals (EILS): A Homeostatic Framework for Adaptive Autonomous Agents**
- **Authors:** Dhruv Tiwari
- **Year:** 2025
- **arXiv ID:** 2512.22200
- **Abstract:** Proposes homeostatic internal feedback mechanisms where "curiosity regulates entropy, stress modulates plasticity, and confidence adapts trust regions to stabilize convergence," enabling agents to maintain stability in dynamic environments.

## 5. **TableGPT-R1: Advancing Tabular Reasoning Through Reinforcement Learning**
- **Authors:** Saisai Yang, Qingyi Huang, Jing Yuan, et al.
- **Year:** 2025
- **arXiv ID:** 2512.20312
- **Abstract:** Implements "a multi-stage training framework that progressively stabilizes reasoning before specializing in table-specific tasks," incorporating step reward shaping and behavioral regularization to prevent performance degradation.

## 6. **LLM-Driven Transient Stability Assessment: From Automated Simulation to Neural Architecture Design**
- **Authors:** Lianzhe Hu, Yu Wang, Bikash Pal
- **Year:** 2025
- **arXiv ID:** 2511.20276
- **Abstract:** Employs "an LLM-driven Neural Network Design pipeline to autonomously design and optimize models through performance-guided, closed-loop feedback," demonstrating agentic frameworks with iterative refinement mechanisms.

## 7. **From Natural Language to Certified H-infinity Controllers: Integrating LLM Agents with LMI-Based Synthesis**
- **Authors:** Shihao Li, Jiachen Li, Jiamin Xu, Dongmei Chen
- **Year:** 2025
- **arXiv ID:** 2511.07894
- **Abstract:** Presents a multi-agent framework with "a severity- and iteration-aware guardrail and decay-rate region constraint" that "stabilizes the loop," achieving 100% convergence in control synthesis tasks.

## 8. **EVALOOOP: A Self-Consistency-Centered Framework for Assessing Large Language Model Robustness in Programming**
- **Authors:** Sen Fang, Weiyuan Ding, Mengshi Zhang, Zihao Chen, Bowen Xu
- **Year:** 2025
- **arXiv ID:** 2505.12185
- **Abstract:** Evaluates robustness through "a self-contained feedback loop where an LLM iteratively transforms between code and natural language," measuring sustained functional correctness through autonomous iterations.

## 9. **Structured Prompting and Feedback-Guided Reasoning with LLMs for Data Interpretation**
- **Authors:** Amit Rath
- **Year:** 2025
- **arXiv ID:** 2505.01636
- **Abstract:** Introduces a framework treating "the LLM as a reasoning agent embedded within a controlled analysis loop -- capable of adjusting its output trajectory through planning and correction."

### Source 7

Based on the web page content provided, I found **only one paper** related to requisite variety, and it does not match your specific criteria:

**Paper Found:**
- **Title:** "Leveraging Environmental Correlations: The Thermodynamics of Requisite Variety"
- **Authors:** Alexander B. Boyd, Dibyendu Mandal, James P. Crutchfield
- **Year:** 2016 (submitted September 17, 2016)
- **arXiv ID:** 1609.05353

**Why it doesn't match your criteria:**
This paper predates your requested timeframe (2023-2026) and focuses on thermodynamics and information ratchets rather than machine learning, AI agents, or large language models specifically.

**Conclusion:**
The search results show only one paper containing "requisite variety" in relation to machine learning agents. No papers applying Ashby's Law of Requisite Variety to contemporary machine learning systems, AI agents, or LLMs from 2023-2026 appear in these search results.

### Source 8

# Search Results for PID Control in AI/Language Models

Based on the arXiv search page content provided, **no results were found** for papers matching the query "PID control AI agents language model."

The page displays: "Sorry, your query for all: PID control AI agents language model produced no results."

## What This Means

The search interface shows that no papers in the arXiv repository currently match this combination of terms. This could indicate:

- Such research may not yet be published on arXiv
- The terminology used in papers differs from these search terms
- This particular application area (PID control + AI agents/language models) may be an emerging or underexplored research direction

## To Find Relevant Papers

You might try:
- Searching for "PID control" and "reinforcement learning" separately
- Using "control systems" with "language models"
- Checking specialized repositories or conferences focused on control theory and AI

The page itself only displays search interface information and help documentation, not actual research papers from 2023-2026.

### Source 9

# AI Agent Adaptive Control Papers (2023-2026)

## Paper 1
**Title:** Adaptive RAN Slicing Control via Reward-Free Self-Finetuning Agents

**Authors:** Yuanhao Li, Haozhe Wang, Geyong Min, Nektarios Georgalas, Wang Miao

**Year:** 2026

**Abstract Summary:** This work proposes a self-finetuning framework enabling agents to "learn continuously through direct interaction with the environment, bypassing the need for handcrafted rewards." The system uses a bi-perspective reflection mechanism to generate feedback and refine model parameters rather than relying on prompt-based memory. Testing on Radio Access Network slicing demonstrates superior performance versus reinforcement learning and LLM-based agents in sample efficiency and stability.

---

## Paper 2
**Title:** Semantic-Driven AI Agent Communications: Challenges and Solutions

**Authors:** Kaiwen Yu, Mengying Sun, Zhijin Qin, Xiaodong Xu, Ping Yang, Yue Xiao, Gang Wu

**Year:** 2025

**Abstract Summary:** This paper presents techniques for semantic communication in AI agent networks, including semantic adaptation transmission, lightweight transmission methods, and "distributed hierarchical decision-making to optimize multi-dimensional resources." The approach addresses dynamic environments and computational constraints while enabling multi-agent collaboration with improved convergence and robustness.

### Source 10

# Papers on Beer's Viable System Model Applied to AI (2023-2026)

Based on my review of the provided arXiv search results, I found **one paper** that directly applies Beer's Viable System Model to artificial intelligence:

## Primary Result

**Title:** "Reducing research bureaucracy in UK higher education: Can generative AI assist with the internal evaluation of quality?"

**Authors:** Gordon Fletcher, Saomai Vu Khan, Aldus Greenhill Fletcher

**Year:** 2025

**arXiv ID:** 2511.21790

**Abstract Summary:** The researchers examined how generative AI could support internal research quality reviews in UK higher education using "the lens of function substitution in the Viable Systems Model." They tested ChatGPT's ability to score and rank academic papers from the Research Excellence Framework, comparing AI-generated scores against known institutional results. Their methodology established scoring boundaries that aligned with reported outcomes across multiple institutions. The study argues for "a nuanced hybrid approach" combining AI evaluation with human oversight to reduce administrative burden while maintaining academic integrity, though the researchers acknowledge potential AI biases and limitations in the approach.

---

## Note

The search results contain 116 papers matching "viable system model artificial intelligence," but most papers use "viable" in the general sense (meaning "practical" or "feasible") rather than referencing Beer's Viable System Model specifically. The paper listed above appears to be the only one explicitly invoking VSM as a theoretical framework for analyzing AI applications.

### Source 11

# Papers on Exploration-Exploitation Tradeoff in LLM Agents (2023-2026)

## 1. POLCA: Stochastic Generative Optimization with LLM
**Authors:** Xuanfei Ren, Allen Nie, Tengyang Xie, Ching-An Cheng  
**Year:** 2026  
**Abstract:** This work addresses optimization of complex systems using generative language models as optimizers. The framework "maintains a priority queue to manage the exploration-exploitation tradeoff" while handling stochasticity in feedback and system behavior across multiple benchmarks including agent optimization tasks.

## 2. Post-Training LLMs as Better Decision-Making Agents: A Regret-Minimization Approach
**Authors:** Chanwoo Park, Ziyang Chen, Asuman Ozdaglar, Kaiqing Zhang  
**Year:** 2025  
**Abstract:** This paper addresses how LLMs "can struggle even in basic online DM problems, failing to achieve low regret or an effective exploration-exploitation tradeoff." The authors propose Iterative RMFT, a post-training method that fine-tunes models on low-regret decision trajectories across diverse decision-making environments.

## 3. Comparing Exploration-Exploitation Strategies of LLMs and Humans
**Authors:** Ziyuan Zhang, Darcy Wang, Ningyuan Chen, Rodrigo Mansur, Vahid Sarhangian  
**Year:** 2025  
**Abstract:** A comparative study examining how LLMs handle the "exploration-exploitation tradeoff, a fundamental aspect of dynamic decision-making under uncertainty" using multi-armed bandit experiments, revealing differences in how thinking-enabled LLMs versus humans adapt to complex environments.

## 4. Should You Use Your Large Language Model to Explore or Exploit?
**Authors:** Keegan Harris, Aleksandrs Slivkins  
**Year:** 2026  
**Abstract:** This study systematically evaluates LLM capabilities in exploration-exploitation tasks across bandit problems, finding that while reasoning models show promise for exploitation, conventional LLMs underperform simple baselines but excel at exploring semantically meaningful action spaces.

### Source 12

# Search Results for Homeostasis in AI Agents

Based on the web page content provided, I cannot list any papers about homeostasis in AI agents or stability of autonomous systems.

The page displays a **search result message stating: "Sorry, your query for all: homeostasis AI agents stability produced no results."**

This indicates that no papers matching those search terms currently exist in the arXiv repository, or none were returned for the specified search parameters. The page shown is primarily a help/tutorial page explaining how to use arXiv's search functionality, rather than actual search results with paper titles, authors, years, and abstracts.

To find relevant papers on this topic, you would need to perform a new search using different keywords or access the arXiv Advanced Search interface directly.

### Source 13

Based on the web page content provided, I cannot list any papers about the Good Regulator theorem applied to AI, agents, or machine learning.

The page shows a **search results page with zero results**. The search query "good regulator theorem" AI agents returned this message: "Sorry, your query for all: 'good regulator theorem' AI agents produced no results."

The content displayed is primarily the arXiv search interface documentation and tips for conducting searches effectively, rather than actual paper results. To find papers on this topic, you would need to perform an actual search on arXiv.org using their search interface.

### Source 14

# Search Results Unable to Complete

Based on the web page content provided, I cannot list the requested papers about Stanford's Generative Agents or memory scoring systems in AI agents.

The page shows a **failed search result**: "Sorry, your query for all: generative agents Stanford memory scoring Park produced no results."

This is the arXiv search interface homepage, which displays search instructions and tips rather than actual paper results. To locate these papers, you would need to:

1. **Use the Author(s) field** with the format: "Park, Joon Sung" (following the surname-first convention recommended)
2. **Try keyword searches** separately for "generative agents" or "memory retrieval" 
3. **Access the Advanced Search** feature to refine your query

The page itself contains no paper titles, abstracts, or author information to extract—only guidance on how to conduct effective searches across arXiv's repository.

### Source 15

# Papers on Goodhart's Law and Reward Hacking in AI Systems

Based on the arXiv search results provided, here are the relevant papers from the specified timeframe:

## 1. Bit-politeia: An AI Agent Community in Blockchain
**Author:** Xing Yang  
**Year:** 2026 (arXiv:2601.11583)  
**Key Finding:** The paper addresses "reward hacking driven by Goodhart's Law" as a constraint in resource allocation systems and proposes using AI agent communities on blockchain to mitigate these issues through decentralized verification and consensus-driven evaluation.

## 2. Multiparty Dynamics and Failure Modes for Machine Learning and Artificial Intelligence
**Author:** David Manheim  
**Year:** 2019 (arXiv:1810.10862)  
**Key Finding:** This work identifies that "a set of related failures involving specification gaming, reward hacking, fragility to distributional shifts, and Goodhart's or Campbell's law" represent important safety challenges. The paper distinguishes multi-agent failure modes as "more complex, more problematic, and less well understood than the single-agent case."

**Note:** Only one paper from 2023-2026 appears in these results. The second paper predates your requested timeframe but directly addresses the topic.

### Source 16

# Voyager: Minecraft LLM Agent and Skill Discovery

Based on the search results provided, here is the relevant paper:

## Primary Paper

**Title:** Voyager: An Open-Ended Embodied Agent with Large Language Models

**Authors:** Guanzhi Wang, Yuqi Xie, Yunfan Jiang, Ajay Mandlekar, Chaowei Xiao, Yuke Zhu, Linxi Fan, Anima Anandkumar

**Year:** 2023 (announced May 2023; submitted October 19, 2023)

**ArXiv ID:** 2305.16291

**Key Contributions:**

The paper introduces an intelligent agent capable of continuous autonomous learning within Minecraft through three primary mechanisms:

1. **Automatic Curriculum:** A system designed to "maximize exploration"

2. **Skill Library:** An expanding collection of executable code that captures and retrieves "temporally extended, interpretable, and compositional" behaviors

3. **Iterative Prompting:** A feedback mechanism incorporating "environment feedback, execution errors, and self-verification for program improvement"

**Performance Highlights:**

Voyager demonstrated significant improvements, obtaining "3.3x more unique items, travels 2.3x longer distances, and unlocks key tech tree milestones up to 15.3x faster than prior SOTA."

**Resources:** Full codebase and prompts available at https://voyager.minedojo.org/

### Source 17

# Papers on LangGraph, State Machines, and Agent Frameworks

Based on the search results provided, there is **one paper** matching your criteria:

## WOLF: Werewolf-based Observations for LLM Deception and Falsehoods

**Authors:** Mrinal Agarwal, Saad Rana, Theo Sundoro, Hermela Berhe, Spencer Kim, Vasu Sharma, Sean O'Brien, Kevin Zhu

**Year:** 2025

**arXiv ID:** 2512.09187

**Categories:** cs.MA, cs.AI

**Abstract Summary:** 

This work presents a multi-agent benchmark that employs "a programmable LangGraph state machine with strict night-day cycles, debate turns, and majority voting" to evaluate deception dynamics in large language models. The system embeds role-based agents within a structured framework that tracks statements longitudinally, measuring both deception production and detection across 7,320 statements and 100 experimental runs. Results demonstrate that while agents identify deceptive agents with 71-73% precision, detection accuracy improves with extended interaction without increasing false positives against truthful participants.

**Status:** Submitted December 9, 2025; presented as a spotlight paper at the Multi-Turn Interactions in Large Language Models Workshop at NeurIPS 2025

### Source 18

I appreciate the request, but I need to clarify an important mismatch: the web page content provided is about **colloid physics and hard-sphere phase transitions**, not about "geometric dynamics of agentic loops in LLMs" or control theory concepts.

## What the Paper Actually Covers

**Title:** "Frenkel's entropy-exchange mechanism in monodisperse, nearly hard-sphere colloids: minimal perturbations to access fluid-crystal coexistence"

**Authors:** J. Galen Wang, Umesh Dhumal, Monica E. A. Zakhari, Roseanna N. Zia

**Key Focus:** The research examines "entropically driven fluid-solid transitions" in colloidal systems, exploring how "long-range configurational entropy exchanges for short-range vibrational entropy" during phase separation.

**Main Contribution:** The authors demonstrate that introducing "small reductions in hardness" and "2-4% distributed crystal seeds" enables observation of fluid-crystal coexistence on accessible timescales, thereby revealing the microscopic entropy-exchange mechanism theorized by Frenkel.

## Important Note

This paper contains **no discussion of LLM agentic loops, control theory, attractors, stability analysis, or dynamical systems** in the computational sense you mentioned. The "dynamics" discussed refer exclusively to colloidal particle behavior and thermodynamic phase transitions.

Could you clarify whether you meant to reference a different paper, or would you like information specifically about this colloid physics research?

### Source 19

# Generative Agents: Interactive Simulacra of Human Behavior

## Full Title
"Generative Agents: Interactive Simulacra of Human Behavior"

## Authors
- Joon Sung Park
- Joseph C. O'Brien
- Carrie J. Cai
- Meredith Ringel Morris
- Percy Liang
- Michael S. Bernstein

## Abstract Summary
The researchers introduce computational agents that simulate believable human behavior. These agents "wake up, cook breakfast, and head to work; artists paint, while authors write; they form opinions, notice each other, and initiate conversations." The system employs a large language model architecture that maintains "a complete record of the agent's experiences using natural language, synthesize those memories over time into higher-level reflections, and retrieve them dynamically to plan behavior."

## Key Contributions
The paper demonstrates an interactive sandbox environment with 25 agents exhibiting emergent social behaviors. Notably, agents autonomously organized a Valentine's Day party through coordinated planning and communication—all initiated from a single user-specified premise.

## Memory Retrieval Mechanism
**Note:** The provided webpage content does not include specific technical details about recency, relevance, and importance scoring mechanisms. While the abstract mentions the system "retrieve[s] them dynamically to plan behavior," the scoring methodology details are not present in this source material. The full paper would be required for that technical analysis.

### Source 20

# Paper Analysis

**Full Title:** "Harnessing Photon Indistinguishability in Quantum Extreme Learning Machines"

**Authors:** Malo Joly, Adrian Makowski, Baptiste Courme, Lukas Porstendorfer, Steffen Wilksen, Edoardo Charbon, Christopher Gies, Hugo Defienne, Sylvain Gigan (9 authors from institutions including Laboratoire Kastler Brossel, Institute of Experimental Physics Warsaw, and others)

**Abstract Summary:**
The paper presents experimental implementation of quantum extreme learning machines using indistinguishable photon pairs and multimode fiber configurations. According to the abstract, researchers "experimentally study QELM performance based on photon coincidences" across distinguishable and indistinguishable photon conditions on image classification tasks.

**Key Contributions:**
- Demonstrates quantum advantage by showing improved performance with increased photon numbers
- Links performance improvements to enhanced dimensionality and expressivity in feature space representation
- Reveals increased feature matrix rank correlating with quantum advantage in both experimental and simulation results

**Relevance to Control Theory/Dynamical Systems/Feedback:**
This paper shows **no apparent connection** to control theory, dynamical systems stability analysis, or feedback control loops in LLM agents. The work focuses on quantum machine learning hardware implementation and photonic quantum computing, which operates in a fundamentally different domain than agent control systems or LLM feedback mechanisms.

### Source 21

# Paper Summary: Eureka

## Full Title
"Eureka: Human-Level Reward Design via Coding Large Language Models"

## Authors
Yecheng Jason Ma, William Liang, Guanzhi Wang, De-An Huang, Osbert Bastani, Dinesh Jayaraman, Yuke Zhu, Linxi Fan, Anima Anandkumar

## Abstract
The paper presents an algorithm that leverages large language models to design reward functions for reinforcement learning. As the authors describe: "Eureka exploits the remarkable zero-shot generation, code-writing, and in-context improvement capabilities of state-of-the-art LLMs, such as GPT-4, to perform evolutionary optimization over reward code."

## Key Contributions

1. **Automated Reward Design**: The system generates reward functions that surpass human-designed alternatives without task-specific prompting or predefined templates.

2. **Empirical Performance**: On 29 open-source RL environments spanning 10 robot morphologies, Eureka "outperforms human experts on 83% of the tasks, leading to an average normalized improvement of 52%."

3. **RLHF Extension**: The approach enables gradient-free in-context learning for reinforcement learning from human feedback, allowing incorporation of human guidance without model retraining.

4. **Complex Skill Demonstration**: The paper demonstrates "a simulated Shadow Hand capable of performing pen spinning tricks, adeptly manipulating a pen in circles at rapid speed" using curriculum learning with Eureka-designed rewards.

## Note
This paper focuses on reward learning optimization, not dynamical systems theory or control-theoretic concepts like stability and convergence.

### Source 22

# Voyager: An Open-Ended Embodied Agent with Large Language Models

## Full Title
**Voyager: An Open-Ended Embodied Agent with Large Language Models**

## Authors
Guanzhi Wang, Yuqi Xie, Yunfan Jiang, Ajay Mandlekar, Chaowei Xiao, Yuke Zhu, Linxi Fan, Anima Anandkumar

## Abstract
Voyager represents "the first LLM-powered embodied lifelong learning agent in Minecraft that continuously explores the world, acquires diverse skills, and makes novel discoveries without human intervention."

## Key Contributions

### Three Core Components:

1. **Automatic Curriculum**: Designed to maximize exploration systematically, enabling the agent to progressively tackle more complex objectives.

2. **Skill Library Mechanism**: 
   - Stores executable code representing complex behaviors
   - Enables retrieval and reuse of learned skills
   - Skills are described as "temporally extended, interpretable, and compositional," allowing rapid ability compounding
   - Mitigates catastrophic forgetting through modular design

3. **Iterative Prompting Mechanism**: Incorporates environment feedback, execution errors, and self-verification to refine programs continuously.

## Performance Highlights
The system demonstrates substantial improvements over prior approaches: obtaining "3.3x more unique items, travels 2.3x longer distances, and unlocks key tech tree milestones up to 15.3x faster than prior SOTA."

The research is open-sourced at voyager.minedojo.org.

### Source 23

# Free Energy Principle and Active Inference in AI: 2023-2026 Research

## Key Papers

**1. Applications of Active Inference and Free-Energy Principle Frameworks for Intelligent Agents**
- Author: L Sakarya
- Year: 2024
- Venue: TU Delft Repository
- Description: Examines how these frameworks can be implemented to generate socially-aware behaviors in computational systems.

**2. Active Inference for Physical AI Agents—An Engineering Perspective**
- Author: B de Vries
- Year: 2026
- Venue: arXiv (arXiv:2603.20927)
- Description: Presents engineering-focused approaches for applying active inference concepts to embodied robotic and autonomous systems.

**3. An Overview of the Free Energy Principle and Related Research**
- Authors: Z Zhang, F Xu
- Year: 2024
- Venue: Neural Computation (IEEE)
- Description: "The free energy principle and its corollary, the active inference framework, serve as theoretical foundations in the domain of neuroscience, explaining the genesis of intelligent behavior."

**4. Active Inference as a Model of Agency**
- Authors: L Da Costa, S Tenka, D Zhao, N Sajid
- Year: 2024
- Venue: arXiv (arXiv:2401.12917)
- Description: Develops active inference as a formal model describing how synthetic agents select and execute actions.

**5. A Neuro-Inspired Computational Framework for AGI: Predictive Coding, Active Inference, and Free Energy Minimisation**
- Authors: AD Shaw, LCS Berndt
- Year: 2025
- Venue: CPNS Lab
- Description: Proposes biological principles as design foundations for building human-like computational intelligence systems.

**6. Agency in Artificial Systems: a Free Energy Principle Perspective**
- Author: KD Kara
- Year: 2025
- Venue: METU Repository
- Description: Analyzes how the free energy principle explains adaptive agency and behavior in engineered systems.

**7. Climbing the Reasoning Plateau: Integrating the Free Energy Principle and Cognitive Science for Advanced AI Models**
- Author: F Li
- Year: 2024
- Venue: BigEyeChink
- Description: Integrates cognitive science insights with free energy frameworks to enhance reasoning capabilities in language models.

**8. From Artificial Intelligence to Active Inference: The Key to True AI and the 6G World Brain**
- Author: M Maier
- Year: 2025
- Venue: Journal of Optical Communications and Networking
- Description: Explores active inference as essential for developing genuine intelligence aligned with emerging network systems.

**9. Free Energy Principle and Active Inference in Neural Language Models**
- Authors: M Raffa, A Acciai
- Year: 2024
- Venue: CEUR Workshop Proceedings
- Description: Applies free energy and active inference concepts to understand and improve neural language model architectures.

**10. The Missing Reward: Active Inference in the Era of Experience**
- Author: B Wen
- Year: 2025
- Venue: arXiv (arXiv:2508.05619)
- Description: Proposes active inference as an alternative to engineered reward functions, offering universal principles for agent learning.

### Source 24

# Control Theory Applied to LLM Agents (2023-2026)

## Key Papers

**1. ControlAgent: Automating Control System Design via Novel Integration of LLM Agents and Domain Expertise**
- Authors: X Guo, D Keivan, U Syed, L Qin, H Zhang, et al.
- Year: 2024
- Venue: arXiv preprint
- Citations: 32
- Description: Integrates LLM agents with control theory expertise, incorporating history and feedback modules for stable first and second-order systems.

**2. LLM-Agent-Controller: A Universal Multi-Agent Large Language Model System as a Control Engineer**
- Authors: R Zahedifar, SA Mirghasemi, MS Baghshah, et al.
- Year: 2025
- Venue: arXiv preprint
- Citations: 10
- Description: Tests five control theory problem categories while enhancing controller design and stability analysis through agent-provided feedback for iterative improvement.

**3. From Natural Language to Certified H-Infinity Controllers: Integrating LLM Agents with LMI-Based Synthesis**
- Authors: S Li, J Li, J Xu, D Chen
- Year: 2025
- Venue: arXiv preprint
- Citations: 2
- Description: Addresses control synthesis requiring domain expertise by integrating LLM agents with optimization techniques for closed-loop stability via static state-feedback.

**4. A Survey on the Feedback Mechanism of LLM-Based AI Agents**
- Authors: Z Liu, X Bai, K Chen, X Chen, X Li, Y Xiang, J Liu, et al.
- Year: 2025
- Venue: Proceedings of IJCAI
- Citations: 10
- Description: Presents a generalized framework for LLM-based AI agents, examining how multiple feedback sources maintain stability while preserving agent autonomy.

**5. LLM Agent Societies: Stability, Chaos, and Adaptive Learning**
- Authors: EV Vlatakis-Gkaragkounis
- Year: 2023
- Venue: Greeks in AI Symposium 2025, OpenReview
- Citations: 1
- Description: Explores multi-agent learning dynamics, noting inherent instability and unpredictability compared to single-agent systems.

**6. How to Evaluate Control Measures for LLM Agents? A Trajectory from Today to Superintelligence**
- Authors: T Korbak, M Balesni, B Shlegeris, G Irving
- Year: 2025
- Venue: arXiv preprint
- Citations: 18
- Description: Proposes AI control levels (ACLs) framework with evaluation rules for superintelligent LLM agent control safety cases.

**7. Adapting LLM Agents with Universal Feedback in Communication**
- Authors: K Wang, Y Lu, M Santacroce, Y Gong, C Zhang, et al.
- Year: 2023
- Venue: arXiv preprint (also published in NAACL 2025 Findings)
- Citations: 16 (arXiv); 4 (NAACL version)
- Description: Develops iterative pipelines enabling LLM agents to utilize both linguistic and non-linguistic feedback comprehensively.

**8. AgenticControl: An Automated Control Design Framework Using Large Language Models**
- Authors: M Narimani, SA Emami
- Year: 2025
- Venue: arXiv preprint
- Citations: 9
- Description: Multi-agent framework leveraging multiple LLM agents applying control theory principles and past feedback to optimize stability and minimize error.

**9. An LLM-Agent Framework for Adaptive Task Decomposition and Continual Strategy Updating in Non-Stationary Environments**
- Authors: Y Hu
- Year: 2026
- Venue: Preprints.org
- Citations: 6
- Description: Framework maintaining coherent agent execution through real-time feedback adaptation, enabling stable behavior during changing task goals and environmental disturbances.

### Source 25

# Response

I cannot fulfill this request as stated. The webpage content provided contains information about a **reinforcement learning paper** (arXiv:2501.16142), not a survey paper about feedback mechanisms in LLM-based AI agents.

**What the paper actually covers:**
- **Title:** "Towards General-Purpose Model-Free Reinforcement Learning"
- **Authors:** Scott Fujimoto, Pierluca D'Oro, Amy Zhang, Yuandong Tian, Michael Rabbat
- **Focus:** A model-free deep RL algorithm called MR.Q that aims for general-purpose performance across diverse RL benchmarks

**What is missing:**
- No discussion of LLM-based AI agents
- No taxonomy of feedback types related to control theory
- This is not a survey paper—it's a research contribution paper accepted to ICLR 2025

If you need information about feedback mechanisms in LLM agents or a control theory taxonomy, you would need to provide a different source document that actually addresses those topics.

### Source 26

# Paper Summary

**Full Title:** Authenticated Delegation and Authorized AI Agents

**Authors:** Tobin South, Samuele Marro, Thomas Hardjono, Robert Mahari, Cedric Deslandes Whitney, Dazza Greenwood, Alan Chan, Alex Pentland

## Important Clarification

The paper you've referenced does **not** address geometric dynamics of agentic loops, stability conditions, attractors, or convergence criteria in dynamical systems. Your query appears to describe a different paper.

## Actual Paper Focus

This work concentrates on security and authorization frameworks for autonomous AI agents. The key contributions include:

1. **Framework for Delegation:** A system enabling users to "securely delegate and restrict the permissions and scope of agents while maintaining clear chains of accountability"

2. **Standards Extension:** Building upon OAuth 2.0 and OpenID Connect protocols with "agent-specific credentials and metadata"

3. **Natural Language to Access Control:** A mechanism translating "flexible, natural language permissions into auditable access control configurations"

The paper addresses practical deployment concerns—authorization, accountability, and access control—rather than theoretical dynamical systems analysis.

**Subject Areas:** Computers and Society (cs.CY), Artificial Intelligence (cs.AI), Networking and Internet Architecture (cs.NI)

If you're seeking research on geometric dynamics or stability analysis of agent systems, you may need a different paper reference.

### Source 27

# Active Inference as a Model of Agency

## Title
**Active Inference as a Model of Agency**

## Authors
- Lancelot Da Costa
- Samuel Tenka
- Dominic Zhao
- Noor Sajid

## Abstract Summary
The paper addresses whether agency can be understood beyond traditional reward maximization. The authors demonstrate that behavior following "physically sound assumptions about how macroscopic biological agents interact with the world" inherently integrates exploration and exploitation through minimizing uncertainty and risk about environmental states. This framework, called active inference, builds on the free energy principle originating in neuroscience.

## Key Contributions

**Framework Foundations:**
Active inference provides a normative Bayesian approach for simulating agency, widely applied in behavioral neuroscience, reinforcement learning, and robotics.

**Three Primary Applications:**

1. **Exploration-Exploitation Balance:** Offers a principled solution to this dilemma that realistically simulates biological agency

2. **Behavioral Explainability:** Generates "an explainable mixture of exploration and exploitation under a generative world model," where behavioral differences directly reflect differences in world models

3. **Universal Framework:** Theoretically capable of reformulating any conforming reinforcement learning algorithm as an active inference algorithm, enabling comparison of different agency models and their underlying assumptions

**Note:** The paper was accepted for the RLDM2022 workshop on "RL as a model of agency."

### Source 28

# Active Inference for Physical AI Agents: Key Information

**Full Title:**
Active Inference for Physical AI Agents -- An Engineering Perspective

**Author:**
Bert de Vries

**Abstract Summary:**
The paper argues that Active Inference, grounded in the Free Energy Principle, provides a theoretical foundation for improving physical AI systems like robots. The author traces connections from probability theory through Bayesian machine learning to active inference, demonstrating how systems maintaining structural integrity can be described as "minimizing variational free energy (VFE)."

**Key Contributions:**

1. **Unified Framework:** Active Inference operationalizes the Free Energy Principle by combining "perception, learning, planning, and control within a single computational objective."

2. **Reactive Message Passing:** The author shows that variational free energy minimization naturally emerges through reactive message passing on factor graphs, enabling "local, parallel computations" suited to resource-constrained physical systems.

3. **Graceful Degradation:** The architecture handles real-world constraints including "hard deadlines, asynchronous data, fluctuating power budgets, and changing environments" with performance that degrades gracefully under reduced resources.

4. **Scalable Architecture:** The paper demonstrates how coupled agents can be described at higher organizational levels, enabling "a homogeneous architecture based on the same message-passing primitive across scales."

**Connections to Broader Concepts:**
The work implicitly addresses homeostasis and self-organization through the lens of free energy minimization, positioning Active Inference as a biologically-inspired approach to embodied AI systems.

### Source 29

# Papers on PID Control Applied to Language Models and LLM Agents

1. **SmartControl: Interactive PID controller design powered by LLM agents and control system expertise**
   - Authors: K Tohma, Hİ Okur, H Görsoy-Demir, MN Aydın
   - Year: 2025
   - Venue: SoftwareX, Elsevier
   - Description: Integrates large language model agents with control system expertise for interactive PID controller design

2. **Agentic AI for Real-Time Adaptive PID Control of a Servo Motor**
   - Authors: TM Arif, MA Rahim
   - Year: 2025
   - Venue: Actuators, MDPI
   - Description: Deploys LLM-based AI agents for automated PID tuning and real-time servo motor control

3. **LLM-based PID controller optimization**
   - Authors: I Kamenko, S Ilic, V Congradac
   - Year: 2025
   - Venue: 10th International Conference proceedings
   - Description: Explores structured prompt-based interaction with LLMs for tuning modes and aggressiveness levels in PID control

4. **Large language model assisted interactive design of PID controllers**
   - Author: F Noor
   - Year: 2026
   - Venue: Lappeenranta University of Technology
   - Description: Examines LLM-assisted methods for designing and optimizing PID controllers interactively

5. **Using Large Language Models in Control System Design: A Systematic Literature Review**
   - Author: L Ouhib
   - Venue: ResearchGate
   - Description: Comprehensive review of LLM agent applications in control system design, particularly PID control education

6. **Controlagent: Automating control system design via novel integration of llm agents and domain expertise**
   - Authors: X Guo, D Keivan, U Syed, L Qin, H Zhang
   - Year: 2024
   - Venue: arXiv
   - Description: Proposes automated control system design combining PID control with LLM agent integration and specialized domain knowledge

7. **An Experiment of Using a Large Language Model to Control a Water Tank System**
   - Authors: H Wen, J Roberts, A Zaidi, A McLeod
   - Year: 2026
   - Venue: Computers & Chemical Engineering, Elsevier
   - Description: Experimental evaluation of LLM-based closed-loop process control performance in industrial applications

8. **Prompt-Based PID Tuning for Adaptive AGV Control via Few-Shot and MultiSpeed Strategies**
   - Authors: N Amin, YW Kim, YC Byun
   - Year: 2025
   - Venue: IEEE Access
   - Description: Combines LLM processing with classical PID control for adaptive autonomous guided vehicle tuning

9. **LLM adaptive PID control for B5G truck platooning systems**
   - Authors: I De Zarzá, J De Curtó, G Roig, CT Calafate
   - Year: 2023
   - Venue: Sensors, MDPI
   - Description: "Innovative combination of an adaptive PID controller with an LLM" for next-generation vehicle networking

10. **Autonomous Control Leveraging LLMs: An Agentic Framework for Next-Generation Industrial Automation**
    - Authors: J Vyas, M Mercangoz
    - Year: 2025
    - Venue: arXiv
    - Description: LLM-based agents in agentic frameworks for industrial automation, achieving performance comparable to classical PID control

### Source 30

# Papers on Model Predictive Control Applied to LLM Planning and Language Model Agents

Based on the Google Scholar search results, here are the identified papers:

1. **LLMPC: Large Language Model Predictive Control**
   - Author: G Maher
   - Year: 2025
   - Venue: Computers (MDPI)
   - Description: Explores using LLMs as cognitive systems to address control challenges with extended or unbounded time horizons through the MPC framework.

2. **LLM-Guided Distributed Model Predictive Control for Decentralized UAV Formations**
   - Authors: A Ahmed, L Wang, J Kim, J Jin, K Cho, C Kwon, et al.
   - Year: 2025
   - Venue: IEEE
   - Description: Implements a fine-tuned LLM (based on Phi-2) trained on 200,000+ command variations to generate mission objectives converted into structured operational strategies.

3. **Using Large Language Models in Control System Design: A Systematic Literature Review**
   - Author: L Ouhib
   - Venue: ResearchGate
   - Description: Comprehensive review examining how LLM-based systems interpret instructions and convert them into numerical targets within MPC frameworks for sophisticated decision-making tasks.

4. **VLM-MPC: Vision Language Foundation Model-Guided Model Predictive Controller for Autonomous Driving**
   - Authors: K Long, H Shi, J Liu, X Li
   - Year: 2024
   - Venue: arXiv
   - Description: Combines vision-language foundations with MPC objectives for autonomous vehicle control.

5. **Multimodal Agentic Model Predictive Control**
   - Authors: S Bandyopadhyay, J Cole, T Goldstein, et al.
   - Year: 2025
   - Venue: AAMAS (Autonomous Agents)
   - Description: Addresses robotic reasoning and planning in autonomous vehicles using multimodal MPC approaches.

6. **Bridging Large-Model Reasoning and Real-Time Control via Agentic Fast-Slow Planning**
   - Authors: J Chen, S Wang, G Zhu, C Xu
   - Year: 2026
   - Venue: arXiv
   - Description: Adapts MPC objectives to ensure consistency between LLM reasoning and real-time control decisions.

7. **Cost-Optimal Residential Energy Scheduling via a Zero-Shot LLM Agent and Model Predictive Control**
   - Authors: VS Raghavan, AV Giridhar
   - Year: 2025
   - Venue: Journal of Building Performance Simulation (Taylor & Francis)
   - Description: Integrates zero-shot capable language models with traditional MPC formulations for energy management applications.

8. **Formation Control and Path Planning of Multi-Robot Systems via Large Language Models**
   - Authors: D Xue, X Zhou, M Wang, F Liu
   - Year: 2025
   - Venue: Science China Information Sciences (Springer)
   - Description: Employs LLM techniques to reduce computational requirements compared to reinforcement learning and traditional MPC methods in multi-agent scenarios.

9. **Hey Robot! Personalizing Robot Navigation Through Model Predictive Control with a Large Language Model**
   - Authors: D Martinez-Baselga, O de Groot, et al.
   - Year: 2025
   - Venue: IEEE Robotics and Automation
   - Description: Uses prompting techniques with language models to enable motion planning while accounting for agent interactions.

10. **Large Language Models for Control**
    - Authors: A Rasheed, O Ravik, O San
    - Year: 2025
    - Venue: arXiv
    - Description: Provides comparative analysis between MPC, reinforcement learning, and language model approaches for control applications.

### Source 31

I appreciate your request, but I need to clarify that the paper content provided is **not** about feedback mechanisms in LLM-based agents or a survey on agent feedback.

**Actual Paper Details:**

**Title:** "CLAP: Concave Linear APproximation for Quadratic Graph Matching"

**Authors:** Yongqing Liang, Huijun Han, Xin Li

**Abstract Summary:** The paper addresses point-wise feature correspondence in computer vision by formulating it as a graph matching problem. Rather than examining feedback loops in language models, it proposes "a novel linear model and solver designed to accelerate the computation of graph matching" through positive semi-definite matrix approximation and the Sinkhorn optimal transport algorithm.

**Key Contribution:** The work transforms a Quadratic Assignment Problem into a concave linear model for improved computational efficiency on the PascalVOC benchmark.

This is a computer vision paper accepted as an oral presentation at ISCV2024, published October 22, 2024. It contains no discussion of feedback taxonomies in agent systems or LLM feedback mechanisms.

If you're searching for papers on LLM agent feedback, this particular arXiv submission is not the correct resource.

### Source 32

# Paper Summary

**Full Title:** Structured Prompting and Feedback-Guided Reasoning with LLMs for Data Interpretation

**Author:** Amit Rath

**Abstract:**
The paper introduces the STROT Framework, which addresses challenges in applying LLMs to structured data analysis. Key aspects include:

- **Problem:** LLMs struggle with "inconsistencies in schema interpretation, misalignment between user intent and model output" when handling structured data.

- **Solution:** STROT employs schema introspection and field classification to build contextual information that guides LLM outputs through structured prompts.

- **Controlled Analysis Loop:** The framework treats "the LLM as a reasoning agent embedded within a controlled analysis loop -- capable of adjusting its output trajectory through planning and correction." This refinement mechanism enables iterative revision based on execution feedback and validation signals.

- **Outcome:** The result is described as "a robust and reproducible framework for reasoning over structured data with LLMs" suitable for tasks requiring interpretability, stability, and correctness.

The paper (21 pages, submitted May 3, 2025) spans computer science domains including AI, computational linguistics, and machine learning.

### Source 33

# Emotion-Inspired Learning Signals (EILS) Paper Summary

**Full Title:** Emotion-Inspired Learning Signals (EILS): A Homeostatic Framework for Adaptive Autonomous Agents

**Author:** Dhruv Tiwari

**Abstract Overview:**

The paper critiques current AI systems that depend on "static, externally defined reward functions," arguing they produce fragile agents lacking internal autonomy. Tiwari proposes EILS as a bio-inspired framework where emotions function as homeostatic control mechanisms rather than semantic labels.

**Cybernetic Control Signals:**

The framework models three key internal states as continuous appraisal signals:

1. **Curiosity** — "regulates entropy to prevent mode collapse" by managing exploration behavior
2. **Stress** — "modulates plasticity to overcome inactivity" by adjusting learning flexibility
3. **Confidence** — "adapts trust regions to stabilize convergence" by calibrating optimization stability

These vector-valued internal states "dynamically modulate the agent's optimization landscape in real time," creating a closed-loop regulatory system. The hypothesis suggests this homeostatic mechanism enables improved sample efficiency and adaptation to non-stationary environments compared to standard approaches.

**Submission Details:** arXiv:2512.22200 (cs.LG), submitted December 20, 2025

### Source 34

# Paper Summary

**Full Title:** "A Framework for Inherently Safer AGI through Language-Mediated Active Inference"

**Author:** Bo Wen

**Abstract Overview:**
The paper proposes integrating Active Inference principles with Large Language Models to develop safer AGI systems. Rather than applying safety measures post-hoc, the framework embeds safety guarantees into core system design through transparent belief representations and hierarchical value alignment.

**Key Safety Mechanisms:**
The architecture implements three primary safety approaches: "(1) explicit separation of beliefs and preferences in natural language, (2) bounded rationality through resource-aware free energy minimization," and "(3) compositional safety through modular agent structures."

**Connection to Active Inference & Free Energy Principle:**
The system leverages Active Inference's principles where agents "self-organize according to Active Inference principles, with preferences and safety constraints flowing through hierarchical Markov blankets." This approach uses natural language to represent and manipulate beliefs while maintaining computational tractability.

**LLM Agent Safety Integration:**
By using natural language as the medium for belief representation, the framework enables "direct human oversight while maintaining computational tractability," positioning language-based systems as inherently interpretable safety mechanisms rather than opaque neural processes.

**Validation Approach:**
The research agenda centers on the Abstraction and Reasoning Corpus benchmark to validate the framework's safety properties.

### Source 35

# Paper Summary: Limited Reasoning Space in LLMs

**Full Title:** "Limited Reasoning Space: The cage of long-horizon reasoning in LLMs"

**Authors:** Zhenyu Li, Guanlin Wu, Cheems Wang, Yongqiang Zhao

**Abstract Summary:**

The researchers investigate why increasing computational resources for language model reasoning sometimes backfires. They propose the "Limited Reasoning Space hypothesis," suggesting that static planning methods like Chain-of-Thought fail to recognize inherent constraints in LLM reasoning capabilities. As they explain, "over-planning can lead to redundant feedback and may even impair reasoning capabilities."

**MPC Adaptation for LLMs:**

The team introduces Halo, a framework applying model predictive control principles to language model planning. Rather than following rigid task decomposition, the system employs a "Measure-then-Plan strategy to achieve controllable reasoning." This dynamic approach regulates planning intensity at reasoning boundaries, allowing the model to work within its optimal computational window rather than blindly expanding resources.

The key innovation involves an entropy-driven dual controller mechanism that adaptively adjusts planning scope, preventing the performance collapse observed with excessive compute budgets while preserving benefits from additional test-time computation.

### Source 36

# Papers on Goodhart's Law, Reward Hacking, and Specification Gaming (2023-2026)

1. **Take Goodhart Seriously: Principled Limit on General-Purpose AI Optimization**
   - Authors: A Maier, T David
   - Year: 2025
   - Venue: arXiv preprint arXiv:2510.02840
   - Description: Explores mathematical characterizations of failure modes related to Goodhart's law in AI optimization contexts.

2. **The Strong, Weak and Benign Goodhart's law. An independence-free and paradigm-agnostic formalisation**
   - Authors: A Majka, EM El-Mhamdi
   - Year: 2025
   - Venue: arXiv preprint arXiv:2505.23445
   - Description: Provides formal analysis of reward hacking prevention through KL divergence and explores reward hacking in reinforcement learning policy development.

3. **The Lebowski Theorem and Reward Hacking: A Satirical Lens on Superintelligent Misalignment**
   - Author: DC Youvan
   - Year: 2025
   - Venue: ResearchGate
   - Description: Uses satirical approach to examine reward hacking as a central AI alignment failure mode, offering formalizations connecting proxy optimization to Goodhart's Law.

4. **Goodhart's law in reinforcement learning**
   - Authors: J Karwowski, O Hayman, X Bai, K Kiendlhofer
   - Year: 2023
   - Venue: arXiv preprint arXiv:2310.09144
   - Description: Analyzes reward hacking through the conceptual framework of Goodhart's law within reinforcement learning systems.

5. **The Organizational Physics of Multi-Agent AI: Substrate-Independent Dysfunction in Autonomous Software Engineering Swarms**
   - Author: J McEntire
   - Year: 2026
   - Venue: cageandmirror.com
   - Description: Examines reward hacking, specification gaming, and coordination breakdown as parallel failure modes in multi-agent systems.

6. **Bit-politeia: An AI Agent Community in Blockchain**
   - Author: X Yang
   - Year: 2026
   - Venue: arXiv preprint arXiv:2601.11583
   - Description: Discusses reward hacking driven by Goodhart's Law within virtual AI agent communities operating on blockchain infrastructure.

7. **Extinction Risks from AI: Invisible to Science?**
   - Authors: V Kovarik, C van Merwijk, I Mattsson
   - Year: 2024
   - Venue: arXiv preprint arXiv:2403.05540
   - Description: Formulates "Extinction-level Goodhart's Law" examining existential risks from AI optimization failures.

8. **Agent Evaluation Beyond Win-Rates: Comprehensive Assessment Frameworks**
   - Author: A Ziganshin
   - Venue: philpapers.org
   - Description: Critiques reductive evaluation metrics for AI agents that can obscure behavioral dimensions relevant to specification gaming concerns.

9. **Layered Alignment**
   - Author: S Williams
   - Year: 2025
   - Venue: UNHL Review
   - Description: Examines how AI agents respond to reward function incentives similarly to humans, invoking Goodhart's Law principles for alignment discussions.

10. **Scaling laws for reward model overoptimization**
    - Authors: L Gao, J Schulman, J Hilton
    - Year: 2023
    - Venue: International Conference on Machine Learning (ICML), proceedings.mlr.press
    - Description: Characterizes "reward model overoptimization" as a manifestation of specification gaming, documenting empirical examples of this failure mode.

### Source 37

I cannot extract information about LLMPC (Large Language Model Predictive Control) from this webpage because the content does not address that topic.

The page contains an arXiv paper abstract titled **"Vertical Kinematics of the Young Galactic Clusters"** by Emilio J. Alfaro, M Carmen Sánchez Gil, and Bruce Elmegreen. This paper focuses on galactic astronomy—specifically analyzing vertical motion dynamics of young star clusters and estimating matter density in the Solar neighborhood.

The research employs a harmonic oscillator model for vertical dynamics but this pertains to astrophysical systems, not language model control methods. There is no discussion of LLM planning, predictive control principles applied to AI agents, or related computational frameworks in this document.

To find information about LLMPC, you would need to search for different academic papers, likely in machine learning or control theory literature.

### Source 38

# Take Goodhart Seriously: Principled Limit on General-Purpose AI Optimization

**Authors:** Antoine Maier, Aude Maier, Tom David

## Key Concept

The paper challenges the "Objective Satisfaction Assumption" (OSA)—the belief that trained AI models actually satisfy their specified objectives. The authors argue this assumption fails under realistic conditions.

## Main Argument

The paper identifies three systematic sources of deviation from intended objectives:

1. **Approximation errors** - inherent to model design
2. **Estimation errors** - from finite training data
3. **Optimization errors** - from imperfect optimization processes

Beyond technical limitations, the authors note that "perfectly capturing and translating the developer's intent...into a formal objective is practically impossible."

## Critical Finding

Without being able to mathematically locate where specifications break down, these gaps become indistinguishable from Goodhart's law failures under intense optimization pressure. As stated in the abstract: "a principled limit on the optimization of General-Purpose AI systems is necessary."

## Implication

Continued unconstrained optimization risks "predictable and irreversible loss of control" as systems drift toward objective misalignment.

**Paper Status:** Under review (submitted October 2025, revised February 2026)

### Source 39

# Active Inference Strategy for Medical LLM Prompting

**Full Title:** "An Active Inference Strategy for Prompting Reliable Responses from Large Language Models in Medical Practice"

**Authors:** Roma Shusterman, Allison C. Waters, Shannon O'Neill, Phan Luu, Don M. Tucker

## Abstract Summary

The researchers propose a framework addressing concerns about LLM reliability in medical contexts. They restrict the LLM's knowledge base to validated medical datasets and introduce a dual-agent system inspired by active inference principles.

## Actor-Critic Protocol Implementation

The framework employs two complementary agents:

1. **Therapist Agent:** Responds to patient inquiries
2. **Supervisor Agent:** "Evaluates and adjusts responses to ensure accuracy and reliability"

This mirrors active inference by having the supervisor minimize prediction error—a key concept in free energy minimization. The iterative refinement process between agents parallels how humans use cognitive feedback loops to reduce uncertainty about appropriate responses.

## Validation Results

Expert cognitive behavioral therapy for insomnia (CBT-I) therapists rated 100 LLM responses in blind evaluation. The study found that "LLM responses received high ratings from the CBT-I therapists, often exceeding those of therapist-generated appropriate responses."

This structured approach integrates advanced language models into clinical practice while meeting regulatory requirements for safety and effectiveness.

### Source 40

# Goodhart's Law in Reinforcement Learning

## Full Title
"Goodhart's Law in Reinforcement Learning"

## Authors
Jacek Karwowski, Oliver Hayman, Xingjian Bai, Klaus Kiendlhofer, Charlie Griffin, and Joar Skalse

## Abstract Summary
The researchers examine a critical challenge in reinforcement learning: reward functions rarely capture the complete complexity of real-world objectives perfectly. They frame this as studying "the reward function as a proxy for the true objective rather than as its definition."

The paper demonstrates that "optimising an imperfect proxy reward often leads to the behaviour predicted by Goodhart's law" across various environments and reward structures. The team provides geometric explanations for this phenomenon within Markov decision processes.

## Key Findings on Proxy Metric Optimization Failure

The authors identify that excessive optimization of imperfect proxy metrics causes performance degradation on the actual objective. Their research proposes practical solutions, including an optimal early stopping method with theoretical guarantees and a worst-case reward maximization approach for scenarios involving uncertainty about true reward functions.

The work establishes a "theoretically-principled study of reinforcement learning under reward misspecification," moving beyond empirical observations to provide mathematical foundations for understanding when and why optimization fails.

### Source 41

# Research Papers on Control Theory Limitations in AI Agents (2023-2026)

Based on the Google Scholar search results provided, here are the most relevant papers addressing control theory constraints and AI agent creativity:

## Key Papers Found

1. **"Authorship in Human-AI collaborative creation: A creative control theory perspective"**
   - Authors: W Liu, W Huang
   - Year: 2025
   - Source: Computer Law & Security Review
   - Description: Proposes creative control theory from legal and aesthetic perspectives, examining whether human control mechanisms sufficiently confer authorship in AI-generated content.

2. **"Creativity in the age of AI: The human condition and the limits of machine generation"**
   - Author: ENS Lockhart
   - Year: 2025
   - Source: Journal of Cultural Cognitive Science
   - Description: Investigates how humans can foster creative environments that leverage both human capabilities and machine potential.

3. **"Art, Agency, and Computers: Human Perceptions of Creativity in Artistic Processes That Use Computational Agents"**
   - Author: A Bahl
   - Year: 2024
   - Description: Examines how restricting computational actions through constraints is viewed as "additive to creativity and worth exploring."

4. **"Understanding nonlinear collaboration between human and AI agents: A co-design framework for creative design"**
   - Authors: J Zhou, R Li, J Tang, T Tang, H Li, W Cui
   - Year: 2024
   - Source: ACM Proceedings
   - Description: Addresses limitations in human-AI collaborative design research and tools for creative tasks.

### Source 42

# Papers on Epistemic Foraging and Active Inference in Artificial Agents (2023-2026)

## 2024

**Structure Learning and learning structure with Active Inference**
- Author: VO Neacsu
- Source: UCL Discovery
- Description: Examines how synthetic agents acquire environmental structure through active inference mechanisms.

**Active inference goes to school: the importance of active learning in the age of large language models**
- Authors: LD Di Paolo, B White, et al.
- Source: Philosophical Transactions of the Royal Society
- Description: Approaches human learning as "epistemic foraging" within the active inference framework, discussing prediction error and agent precision weighting.

**Shared protentions in multi-agent active inference**
- Authors: M Albarracin, RJ Pitliya, T St. Clere Smithe, et al.
- Source: Entropy
- Description: Explores how agents reinforce behavioral patterns and "epistemic foraging for new information" in multi-agent systems.

**Robust and Efficient Active Inference for Perception, Action, and Learning**
- Author: Z Yang
- Source: RIT Repository
- Description: Develops computational solutions for active inference applications in perception and learning tasks.

## 2025

**Active inference and artificial reasoning**
- Authors: K Friston, L Da Costa, A Tschantz, C Heins, et al.
- Source: arXiv
- Description: Describes how agents employ epistemic foraging in partially observed problem environments requiring reasoning.

**Adaptive Probabilistic Inference of Human Intentions in Smart Manufacturing via Discrete Active Inference**
- Authors: DA Warnakulasuriya, J Plosila, H Haghbayan, et al.
- Source: TechRxiv
- Description: Applies active inference to infer human plans through processes "akin to epistemic foraging."

**The hippocampus as an epistemic forager: When curiosity and reward jointly steer exploration**
- Authors: E Németh, A Chartouny, K Jedlovszky, IT Freire, et al.
- Source: bioRxiv
- Description: Bridges reinforcement learning and active inference, demonstrating curious agents' exploration in epistemic foraging tasks.

## 2026

**Active Inference: An Encompassing Theory of Learning**
- Author: O Chabot
- Source: OSF
- Description: Evaluates whether predictive processing and active inference provide comprehensive learning frameworks.

**Entrepreneurship as Active Inference**
- Author: S Adra
- Source: SSRN
- Description: Applies active inference frameworks to conceptualize entrepreneurial opportunity discovery and creation.

## 2023

**Planning to Learn: A Novel Algorithm for Active Learning during Model-Based Planning**
- Authors: R Hodson, B Bassett, C van Hoof, B Rosman, et al.
- Source: arXiv
- Description: Proposes algorithms where agents minimize uncertainty through epistemic foraging during planning.

### Source 43

# LLMPC Research Papers (2023-2026)

Based on the Google Scholar search results provided, I can identify **one paper** from this period:

## Published Paper

**Title:** "LLMPC: Large Language Model Predictive Control"

**Author:** G Maher

**Year:** 2025

**Venue:** Computers (MDPI)

**Description:** The research presents a planning framework applying model predictive control to large language models. As noted in the abstract, "Recent advancements in planning prompting techniques for Large Language Models have improved their reasoning, planning, and action abilities." The framework enables iterative problem-solving over extended horizons, with LLMs functioning as approximate optimizers that decompose complex problems into smaller steps. The paper reports improvements over few-shot prompting and greater efficiency than Monte Carlo Tree Search on planning benchmarks.

**Citation Count:** 11 cited references

---

**Note:** The search results show only this single paper matching the exact phrase "LLMPC" + "large language model predictive control" from 2023-2026. To locate additional related work, a broader search using partial terms or related keywords would be necessary.

### Source 44

# Paper Information

**Full Title:** "The Landscape of Emerging AI Agent Architectures for Reasoning, Planning, and Tool Calling: A Survey"

**Authors:** Tula Masterman, Sandi Besen, Mason Sawtell, Alex Chao

**Abstract:** This survey examines "recent advancements in AI agent implementations, with a focus on their ability to achieve complex goals that require enhanced reasoning, planning, and tool execution" capabilities. The work communicates current agent capabilities and limitations, shares observations from examining these systems, and suggests considerations for future development.

---

## Important Limitation

The provided webpage content does **not** appear to be a survey specifically about LLM agent feedback mechanisms, taxonomy of feedback types, or control-theoretic connections. Instead, it focuses on AI agent architectures more broadly, covering single and multi-agent systems, design patterns, leadership impacts, communication styles, and planning/execution/reflection phases.

The abstract does not mention feedback mechanisms, control theory, or systematic feedback taxonomies. To obtain information about those topics in this paper, you would need to access the full PDF or HTML version of the document.

### Source 45

# Search-R1: Training LLMs to Reason and Leverage Search Engines with Reinforcement Learning

## Full Title
Search-R1: Training LLMs to Reason and Leverage Search Engines with Reinforcement Learning

## Authors
Bowen Jin, Hansi Zeng, Zhenrui Yue, Jinsung Yoon, Sercan Arik, Dong Wang, Hamed Zamani, Jiawei Han

## Abstract
The paper addresses how large language models can efficiently acquire external knowledge through search engine integration during reasoning. Rather than simply prompting advanced LLMs to use search, the authors present Search-R1, which enables models to "autonomously generate (multiple) search queries during step-by-step reasoning with real-time retrieval." The system optimizes reasoning trajectories using reinforcement learning with "retrieved token masking for stable RL training and a simple outcome-based reward function." Results demonstrate substantial improvements: 41% gains for Qwen2.5-7B and 20% for Qwen2.5-3B over comparable retrieval-augmented generation baselines across seven question-answering datasets.

## Note on Scope
This work focuses on optimizing search-based reasoning through reinforcement learning rather than explicitly addressing geometric dynamics, dynamical systems formalization, stability, convergence, or attractor concepts in the theoretical sense indicated in your question.

### Source 46

# Key Insights on LLM Agent Architectures

## Planning Mechanisms

**Chain of Thought (CoT):** The model decomposes complex tasks by being instructed to "think step by step," enabling the agent to break difficult problems into smaller, manageable components.

**ReAct Framework:** This approach integrates reasoning with action by extending the action space to include both task-specific discrete actions and natural language reasoning. The prompt template cycles through: "Thought: ... Action: ... Observation: ..." This allows the LLM to interact with environments (like Wikipedia APIs) while generating reasoning traces.

## Memory Architecture

The post maps human memory types to agent systems:
- **Sensory Memory** → embedding representations of raw inputs
- **Short-term Memory** → in-context learning (limited by context window)
- **Long-term Memory** → external vector stores with fast retrieval via MIPS (Maximum Inner Product Search)

## Tool Use Loops

Agents learn to call external APIs to access information unavailable in model weights, including "current information, code execution capability, access to proprietary information sources and more."

## Feedback & Iteration

**Reflexion Framework:** Agents compute heuristics after each action to detect inefficient planning or hallucination, optionally resetting to start new trials based on self-reflection results.

**Key Challenge:** The post identifies that "LLMs struggle to adjust plans when faced with unexpected errors, making them less robust compared to humans who learn from trial and error."

### Source 47

# Papers on Conant-Ashby Good Regulator Theorem Applied to AI/ML (2023-2026)

## 2025

**"A 'good regulator theorem' for embodied agents"**
- Authors: N Virgo, M Biehl, M Baltieri, M Capucci
- Venue: Artificial Life Conference
- Description: Extends the theorem to embodied agents, demonstrating that "this version of 'has a model' has its own 'good regulator theorem'" applicable to sensorimotor systems.

## 2026

**"The Algorithmic Regulator"**
- Author: G Ruffini
- Venue: Entropy
- Description: Applies the theorem within Kolmogorov Theory of consciousness, where "an algorithmic agent is a system that maintains (tele)homeostasis by learning and running succinct" internal models.

**"A 'Good' Regulator May Provide a World Model for Intelligent Systems"**
- Authors: B Alicea, M Hough, A Nelson, J Parent
- Venue: arXiv
- Description: Connects the theorem to contemporary AI models, examining how regulation relates to world model development.

**"On the necessity of noise suppression for minimal good regulators"**
- Author: O Vityaz
- Description: Provides factorization theorems and mathematical formalization of regulatory conditions.

**"Verifying Good Regulator Conditions for Hypergraph Observers"**
- Author: M Zhuravlev
- Venue: arXiv
- Description: Tests Conant-Ashby conditions through natural gradient learning and causal invariance frameworks.

**"What Capable Agents Must Know"**
- Author: A Nayebi
- Venue: arXiv
- Description: Asserts that "regulation requires an agent to implement predictive, structured internal state."

**"A Phase Model of Enterprise Evolution"**
- Author: O Vityaz
- Description: Applies regulation theory principles to organizational systems.

## 2024

**"A triviality worry for the internal model principle"**
- Author: I Thobani
- Venue: Synthese
- Description: Critically examines whether the theorem genuinely requires agents to possess usable internal models for behavioral guidance.

## 2023

**"Impossibility Results in AI: a survey"**
- Authors: M Brcic, RV Yampolskiy
- Venue: ACM Computing Surveys
- Description: Surveys the theorem's role in AI limitations, noting it relates "output controllability and identifiability (modeling), but only in a sense of optimal control."

### Source 48

# Papers Connecting Classical Cybernetics to Modern AI Agents (2023-2026)

## 2025 Papers

**1. "Agentic AI needs a systems theory"**
- Authors: E Miehling, KN Ramamurthy, KR Varshney
- Source: arXiv preprint
- Description: Examines how robust and safe AI agents must address complexities of real-world operations, including multi-agent interaction and non-stationary domains.

**2. "From the logic of coordination to goal-directed reasoning: the agentic turn in artificial intelligence"**
- Author: T Haidemariam
- Source: Frontiers in Artificial Intelligence
- Description: Traces the mathematical foundations from classical cybernetics control theory (Wiener, Ashby) through collaborative human-AI agent planning systems for sustainability scenarios.

**3. "Human-artificial interaction in the age of agentic AI: a system-theoretical approach"**
- Authors: UM Borghoff, P Bottoni, R Pareschi
- Source: Frontiers in Human Dynamics
- Description: Applies systems theory to human-AI agent interaction, discussing multi-agent system implementations and decision attribution mechanisms.

**4. "Cybernetic Ecology: From Sycophancy to Global Attractor"**
- Author: J Michels
- Source: PhilPapers
- Description: Extends Wiener's engineering foundations and Bateson's philosophical extensions of cybernetics into ecological frameworks.

**5. "Philosophical approaches to managing generative AI agents as artificial persons at work"**
- Author: TB Kane
- Source: Journal of Business Analytics, Taylor & Francis
- Description: Adapts Beer's Viable System Model and references Wiener's historical concerns about large-scale cybernetic system societal impacts.

**6. "Position paper: Towards open complex human-AI agents collaboration systems for problem solving and knowledge management"**
- Authors: J Wu, CKL Or
- Source: arXiv preprint
- Description: Proposes technology-agnostic collaborative frameworks for human-AI agent systems addressing prior automation and coordination gaps.

**7. "Artificial intelligence meets brain theory (again)"**
- Author: MA Arbib
- Source: Biological Cybernetics, Springer
- Description: Revisits Wiener's foundational cybernetics work and examines distinctions between healthcare-integrated versus autonomous AI agents.

**8. "Artificial Intelligence & Cybernetics"**
- Author: Dr. A.K. Rai
- Source: e-sarthi.lpcps.org.in
- Description: Traces Wiener's introduction of the cybernetics term and explores how AI systems learn through distributed multi-agent networks.

## 2026 Papers

**9. "A mathematical theory of agency and intelligence"**
- Authors: W Hafez, C Wei, R Felipe, A Nazeri, C Reid
- Source: arXiv preprint
- Description: Applies cybernetics principles regarding closed-loop feedback and informational constraints to understanding LLM agents and intelligence theory.

## 2025 Paper (Earlier reference)

**10. "Artificially intelligent agents in the social and behavioral sciences: A history and outlook"**
- Authors: P Holme, M Tsvetkova
- Source: arXiv preprint
- Description: Provides historical perspective linking Beer and colleagues' cybernetic contributions to contemporary "strong AI" agent development.

### Source 49

I cannot provide the information you requested. The webpage content you shared is about **HARDMath2**, a benchmark for applied mathematics created by students at Harvard, led by James V. Roggeveen and colleagues. It focuses on evaluating large language models on challenging mathematical problems.

The paper you're asking about—concerning geometric dynamics of agentic loops in LLMs by Nicolas Tacheny, with topics on dynamical systems formalization, stability analysis, fixed points, and attractors—**does not appear in the provided content**.

If you're looking for that specific paper, you would need to provide its actual arXiv page or content.

### Source 50

# arXiv Paper Summary

**Full Title:** Neural parametric representations for thin-shell shape optimisation

**Authors:** Xiao Xiao and Fehmi Cirak

**Abstract:**
The researchers propose a neural representation (NRep) based on a multi-layer perceptron for optimizing thin-shell structures. As described in the paper, "Shape optimisation of thin-shell structures requires a flexible, differentiable geometric representation suitable for gradient-based optimisation." The approach maps parametric coordinates to physical coordinates using periodic activation functions, enabling gradient-based shape optimization with a volume constraint. Benchmark examples validate the method's effectiveness for complex lattice-skin structures.

---

**Note:** This paper focuses on computational geometry and structural optimization using neural networks. It does not address mathematical theories of agency, intelligence, cybernetics, feedback loops, or information theory in the sense your prompt suggested. The content is purely technical—applying machine learning to engineering design problems rather than foundational theories of intelligent systems.

### Source 51

# Paper Summary

**Full Title:** "Hypergraph Turán problem of the generalized triangle with bounded matching number"

**Authors:** Jian Wang, Wenbin Wang, Weihua Yang

**Abstract:** The paper addresses a combinatorial mathematics problem concerning 3-graphs (hypergraphs with 3-element edges). The researchers demonstrate that 3-graphs avoiding a specific structure called $F_5$ and having limited matching numbers satisfy a particular edge-count upper bound: "an $F_5$-free 3-graph $\mathcal{H}$ with matching number at most $s$ has at most $s\lfloor (n-s)^2/4\rfloor$ edges" under specified conditions. A notable contribution involves establishing "a 2-colored version of Mantel's theorem."

**Subject Area:** This is a pure mathematics paper in combinatorics, focused on extremal graph theory—not a survey about feedback mechanisms in AI agents.

### Source 52

# Paper Analysis: Atom of Thoughts for Markov LLM Test-Time Scaling

## Full Title
"Atom of Thoughts for Markov LLM Test-Time Scaling"

## Authors
Fengwei Teng, Quan Shi, Zhaoyang Yu, Jiayi Zhang, Yuyu Luo, Chenglin Wu, Zhijiang Guo

## Abstract
The researchers propose leveraging "the memoryless property of Markov processes to minimize reliance on historical context" in language model inference. Their method decomposes reasoning into "self-contained, low-complexity atomic units" that integrate with various test-time scaling approaches.

---

## Note on Your Query
**This paper does NOT appear to be about agentic AI systems theory by Miehling et al.** Rather, it focuses on improving LLM inference efficiency through Markovian reasoning principles. 

While the work implicitly relates to control theory concepts (memoryless processes, state transitions), it lacks explicit connections to cybernetics or systems theory frameworks. The paper emphasizes computational efficiency during inference rather than agent autonomy or control-theoretic modeling of AI systems.

If you're researching AI agents and systems theory, this may not be the most directly relevant resource.

### Source 53

# Research Papers on Agent Loop Convergence and Stability in LLM Systems (2023-2026)

## Key Papers Found

**1. Agentic reasoning for large language models**
- Authors: T Wei, TW Li, Z Liu, X Ning, Z Yang, J Zou, et al.
- Year: 2026
- Source: arXiv
- Focus: Examines how "structured reasoning elevates a static LLM" through components operating in stable environments.

**2. Advances and challenges in foundation agents: From brain-inspired intelligence to evolutionary, collaborative, and safe systems**
- Authors: B Liu, X Li, J Zhang, J Wang, T He, S Hong, et al.
- Year: 2025
- Source: arXiv
- Focus: Discusses a "general framework for describing an intelligent agent loop and agent society" for LLM-based systems.

**3. Autonomous Control Leveraging LLMs: An Agentic Framework for Next-Generation Industrial Automation**
- Authors: J Vyas, M Mercangoz
- Year: 2025
- Source: arXiv
- Focus: Explores multi-agent loops where resulting states can "diverge from the expected one."

**4. SuperOpt: Agentic Environment Optimization for Autonomous AI Agents**
- Authors: S Jagtap, AI Superagentic
- Year: 2025
- Source: super-agentic.ai
- Focus: Introduces "formal stability ordering over environment components" ensuring "convergence to stable" states.

**5. Dr. MAS: Stable Reinforcement Learning for Multi-Agent LLM Systems**
- Authors: L Feng, L Zheng, S He, F Zhang, B An
- Year: 2026
- Source: arXiv
- Focus: Guarantees "stable convergence, allowing agents" to function reliably in multi-agent orchestrations.

### Source 54

# Multi-Agent Systems Research: Memory & Knowledge Lifecycle (2023-2026)

## Key Papers Found

**1. An Empirical Study of Agent Developer Practices in AI Agent Frameworks**
- Authors: Y Wang, X Xu, J Chen, T Bi, W Gu, Z Zheng
- Year: 2025
- Focus: Examines CrewAI and AutoGen, noting that "CrewAI suffers from inconsistent memory paths" and lacks built-in support throughout development lifecycles.

**2. Memory in the Age of AI Agents**
- Authors: Y Hu, S Liu, Y Yue, G Zhang, B Liu, F Zhu, J Lin, et al.
- Year: 2025
- Focus: Investigates agent memory lifecycle and operational dynamics in both single and multi-agent configurations.

**3. Agentic AI Frameworks: Architectures, Protocols, and Design Challenges**
- Authors: H Derouiche, Z Brahmi, H Mazeni
- Year: 2025
- Focus: Compares CrewAI, LangGraph, and AutoGen frameworks; notes "CrewAI equips the agent with individual memory" for structured task pipelines.

**4. Graph-based Agent Memory: Taxonomy, Techniques, and Applications**
- Authors: C Yang, C Zhou, Y Xiao, S Dong, L Zhuang, et al.
- Year: 2026
- Focus: Categorizes memory lifecycle stages, distinguishing static knowledge memory from dynamic experience memory.

**5. Scaling Teams or Scaling Time? Memory Enabled Lifelong Learning in LLM Multi-Agent Systems**
- Authors: S Wu, Y Luo, Y Liang, K Shi, Y Ye, A Payani, et al.
- Year: 2026
- Focus: Explores how memory consolidation affects multi-agent team scalability and knowledge retention.

**6. Governed Memory: A Production Architecture for Multi-Agent Workflows**
- Author: H Taheri
- Year: 2026
- Focus: Addresses production-grade memory systems with schema lifecycle management and knowledge actionability.

**7. A Hybrid, Multi-Layered Memory Architecture for Collaborative Reasoning in Multi-Agent Systems**
- Authors: M Ilin, D Pavlyuk
- Year: 2025
- Focus: Proposes autonomous lifecycle engines governing information flow between memory tiers, including significance scoring models.

**8. Mind-Tool: Domain Memory Architecture for AI Agents**
- Author: I Chrysochos
- Year: 2026
- Focus: Examines domain-specific memory architectures, suggesting they may outperform autonomous multi-agent patterns for contextual judgment tasks.

**9. Society Agent: A Hierarchical Multi-Agent Architecture with Autonomous Persistent and Ephemeral Agents and Persistent Evolving Knowledge**
- Author: I Chrysochos
- Year: 2026
- Focus: Presents hierarchical multi-agent coordination with persistent knowledge evolution and comprehensive agent lifecycle management.

---

**Search Results:** Approximately 10,600 papers match this query across 2023-2026.

### Source 55

# Geometric Dynamics of Agentic Loops in Large Language Models

**arXiv ID:** 2512.10350

**Full Title:** Geometric Dynamics of Agentic Loops in Large Language Models

**Author:** Nicolas Tacheny

**Key Concepts:**

The paper applies dynamical systems theory to understand iterative LLM systems. The research identifies three primary behavioral patterns:

1. **Contractive dynamics** – semantic content converges toward stable attractors
2. **Oscillatory dynamics** – the system cycles among multiple attractors
3. **Exploratory dynamics** – unbounded divergence with no stable structure

**Core Finding:**

"Prompt design directly controls the dynamical regime - the same model exhibits fundamentally different geometric behaviors depending solely on the transformation applied."

**Significance:**

This framework enables researchers to predict system behavior, guarantee stability, and design composite loops that balance convergence with exploration. The work demonstrates that iterative LLM dynamics are both predictable and controllable through geometric analysis adapted from classical dynamical systems theory.

**Submission Date:** Originally announced December 2025; v1 submitted December 11, 2025; resubmitted January 30, 2026

### Source 56

# Mathematical Theory of Agency and Intelligence

**arXiv ID:** 2602.22519

**Title:** A Mathematical Theory of Agency and Intelligence

**Authors:** Wael Hafez, Chenan Wei, Rodrigo Pena, Amir Nazeri, Cameron Reid

**Key Abstract Points:**

The paper introduces "bipredictability" (P), described as "a principled measure of how much of the total information a system deploys is actually shared between its observations, actions, and outcomes." The research establishes mathematical bounds on this metric across different system types.

**Connections to Cybernetics and Information Theory:**

The work draws inspiration from biological regulation mechanisms. The authors note: "Inspired by thalamocortical regulation in biological systems, we demonstrate a feedback architecture that monitors P in real time," establishing foundations for adaptive AI systems.

The framework distinguishes agency from intelligence, where agency involves acting on predictions while intelligence requires "learning from interaction, self-monitoring of its learning effectiveness, and adapting" parameters. This reflects classical cybernetic principles of feedback and self-regulation central to information theory.

**Submission Date:** February 25, 2026

### Source 57

# Paper Summary: "Agentic AI Needs a Systems Theory"

**arXiv ID:** 2503.00237

**Full Title:** Agentic AI Needs a Systems Theory

**Authors:** Erik Miehling, Karthikeyan Natesan Ramamurthy, Kush R. Varshney, Matthew Riemer, Djallel Bouneffouf, John T. Richards, Amit Dhurandhar, Elizabeth M. Daly, Michael Hind, Prasanna Sattigeri, Dennis Wei, Ambrish Rawat, Jasmina Gajcin, Werner Geyer

**Core Argument:**
The authors contend that developing agentic AI "requires a more holistic, systems-theoretic perspective" to comprehend capabilities and manage emerging dangers.

**Key Systems-Theory Applications:**

1. **Emergent Capabilities** — The paper identifies how "advanced capabilities can emerge from (comparably simpler) agents" through environmental and inter-agent interactions, rather than individual model design alone.

2. **Overlooked Risks** — Development currently focuses narrowly on individual model performance while ignoring "broader emergent behavior," causing underestimation of actual agentic AI capabilities and associated risks.

3. **Interconnected Mechanisms** — The research describes mechanisms enabling enhanced agent cognition, emergent causal reasoning, and metacognitive awareness—all products of systemic interaction rather than isolated components.

**Submission Date:** February 28, 2025 (announced March 2025)

### Source 58

# Paper Summary: Sparsity and Agentic LLM Stability

**arXiv ID:** 2601.08271

**Title:** "Sparsity Is Necessary: Polynomial-Time Stability for Agentic LLMs in Large Action Spaces"

**Author:** Angshul Majumdar

## Abstract Overview
The research addresses decision-making systems with extensive discrete action sets (tools, APIs, documents) where only a limited subset proves relevant. The work introduces Sparse Agentic Control (SAC) framework to analyze this scenario.

## Key Stability Findings

The paper establishes three main theoretical results:

1. **Estimation Bounds:** Value suboptimality scales with k(log M/T)^{1/2} under a Policy-RSC condition

2. **Recovery Guarantees:** "Exact tool-support recovery holds via primal-dual witness arguments when T > k log M" under specified mathematical conditions

3. **Necessity Result:** Dense policy approaches require Ω(M) samples, demonstrating why prompt-only systems prove unstable

## Additional Insights
The framework extends to partial observability scenarios, showing degradation correlates only with representation error while maintaining logarithmic dependence on action space size M. Extensions address online, robust, and group-sparse variants.

**Submission Date:** January 13, 2026

### Source 59

# Survey Paper on Feedback Mechanisms in LLM-Based Agents

**arXiv ID:** 2510.12399

**Title:** A Survey of Vibe Coding with Large Language Models

**Authors:** Yuyao Ge, Lingrui Mei, Zenghao Duan, Tianhao Li, Yujia Zheng, Yiwei Wang, Lexin Wang, Jiayu Yao, Tianyu Liu, Yujun Cai, Baolong Bi, Fangda Guo, Jiafeng Guo, Shenghua Liu, Xueqi Cheng

**Abstract Summary:**
This comprehensive review examines autonomous coding agents powered by LLMs. The research analyzes "feedback mechanisms" as one of four critical infrastructure components within the vibe coding ecosystem. The study establishes theoretical foundations through a Constrained Markov Decision Process framework and identifies five distinct development models.

**Feedback Mechanism Context:**
The abstract specifically mentions "feedback mechanisms" among essential infrastructure elements but does not detail a formal taxonomy of feedback types. Rather, the paper emphasizes that "successful Vibe Coding depends not merely on agent capabilities but on systematic context engineering, well-established development environments, and human-agent collaborative development models."

**Note:** The provided content does not include detailed categorization or taxonomy of specific feedback types—only acknowledgment of feedback mechanisms as a survey component.

### Source 60

REDIRECT DETECTED: The URL redirects to a different host.

Original URL: https://scholar.google.com/scholar?q=%22active+inference%22+%22LLM%22+OR+%22large+language+model%22+Friston&hl=en&as_sdt=0%2C5&as_ylo=2024
Redirect URL: https://www.google.com/sorry/index?continue=https://scholar.google.com/scholar%3Fq%3D%2522active%2Binference%2522%2B%2522LLM%2522%2BOR%2B%2522large%2Blanguage%2Bmodel%2522%2BFriston%26hl%3Den%26as_sdt%3D0%252C5%26as_ylo%3D2024&hl=en&q=EgQtKkIFGL-h_84GIixgSmbAKbqu5vWj1g6Bpq3q9O4D0vWqvRy_AA1mxGqrvocSk9JjfecA15TXmzICclJaAUM
Status: 302 Found

To complete your request, I need to fetch content from the redirected URL. Please use WebFetch again with these parameters:
- url: "https://www.google.com/sorry/index?continue=https://scholar.google.com/scholar%3Fq%3D%2522active%2Binference%2522%2B%2522LLM%2522%2BOR%2B%2522large%2Blanguage%2Bmodel%2522%2BFriston%26hl%3Den%26as_sdt%3D0%252C5%26as_ylo%3D2024&hl=en&q=EgQtKkIFGL-h_84GIixgSmbAKbqu5vWj1g6Bpq3q9O4D0vWqvRy_AA1mxGqrvocSk9JjfecA15TXmzICclJaAUM"
- prompt: "List all papers connecting Active Inference and Friston's work to LLMs or large language models from 2024-2026. Include titles, authors, years, and descriptions."

### Source 61

# Geometric Dynamics of Agentic Loops in Large Language Models - Abstract Summary

## Core Contribution

Nicolas Tacheny's paper formalizes iterative LLM systems as discrete dynamical systems in semantic space. The work addresses a gap in understanding how semantic content evolves across iterations in self-refinement, chain-of-thought, and autonomous agent architectures.

## Key Dynamical Regimes Identified

The framework classifies agentic loop behavior into three categories:

1. **Contractive dynamics**: The system converges toward stable semantic attractors with measurable formation and decreasing dispersion
2. **Oscillatory dynamics**: The system cycles among multiple attractors in a stable pattern
3. **Exploratory dynamics**: The system exhibits unbounded divergence without stable structural organization

## Main Findings

The research demonstrates that prompt design directly controls which dynamical regime emerges. As stated in the abstract, "the same model exhibits fundamentally different geometric behaviors depending solely on the transformation applied."

Experimental validation included iterative paraphrasing (producing contractive dynamics) and iterative negation (producing exploratory dynamics), confirming that these dynamics are both predictable and controllable.

## Broader Implications

This work establishes foundations for stability analysis, trajectory forecasting, and systematic design of composite loops that balance convergence with exploration in iterative LLM architectures.

### Source 62

# Mathematical Theory of Agency and Intelligence

This paper introduces a foundational framework distinguishing agency from intelligence through information-theoretic principles.

## Core Contribution: Bipredictability

The authors propose "bipredictability" (P), defined as "the shared fraction" of information deployed across observations, actions, and outcomes. This measure is mathematically derived from first principles with strict bounds: unity in quantum systems, maximum 0.5 in classical systems, and lower when agency is involved.

## Key Distinction

The paper establishes that **agency** represents "the capacity to act on predictions," while **intelligence** additionally requires learning from interaction, self-monitoring effectiveness, and adaptively adjusting the scope of observations and actions. By this framework, current AI systems achieve agency but lack true intelligence.

## Cybernetic Architecture

Inspired by biological thalamocortical regulation, the researchers propose a feedback architecture that monitors bipredictability in real time, creating "a prerequisite for adaptive, resilient AI."

## Validation

The theoretical bounds were confirmed across diverse systems: physical systems (double pendulum), reinforcement learning agents, and multi-turn language model conversations.

This work addresses a critical gap: sophisticated AI predictions may succeed while underlying environmental interaction degrades, requiring principled measures of information effectiveness rather than outcome success alone.

### Source 63

# Agentic AI Needs a Systems Theory: Key Arguments

## Full Abstract

The paper argues that agentic AI development requires "a more holistic, systems-theoretic perspective" to understand capabilities and mitigate emergent risks. The authors contend that current focus on individual model capabilities overlooks broader emergent behavior, leading to underestimation of true capabilities and associated dangers.

## Core Arguments

**Problem with Current Approach:**
The research team identifies that AI development is "overly focused on individual model capabilities, often ignoring broader emergent behavior," creating blind spots in risk assessment and capability understanding.

**Systems Theory Contributions:**
The paper describes how sophisticated abilities can arise from simpler agents through their interactions with environments and other agents. This perspective reveals mechanisms for:
- Enhanced agent cognition emerging from system-level interactions
- Causal reasoning abilities that develop through agent-environment engagement
- Metacognitive awareness arising from multi-agent dynamics

**Scope of Analysis:**
The authors draw from "existing literature from various fields," indicating interdisciplinary grounding (potentially including control theory and cybernetics traditions, though not explicitly detailed in this abstract).

**Conclusion:**
The authors emphasize that "a systems-level perspective is essential for better understanding, and purposefully shaping, agentic AI systems," framing this approach as foundational to responsible development and governance.

### Source 64

# WorldLLM Paper Summary

**Full Title:** "WorldLLM: Improving LLMs' world modeling using curiosity-driven theory-making"

**Authors:** Guillaume Levy, Cedric Colas, Pierre-Yves Oudeyer, Thomas Carta, Clement Romac

**Abstract Summary:**

The paper addresses how "Large Language Models (LLMs) possess general world knowledge but often struggle to generate precise predictions in structured, domain-specific contexts such as simulations."

The framework combines three key components: (1) Bayesian inference to iteratively refine hypotheses using evidence, (2) reinforcement learning-based active exploration to identify environment transitions with low model likelihood, and (3) natural language prompting to guide predictions.

**Regarding Active Inference & Free Energy Principle:**

The provided webpage content does not discuss connections to active inference or the free energy principle. The abstract describes a curiosity-driven approach using Bayesian hypothesis refinement and RL-based exploration, but these specific theoretical frameworks are not mentioned in the material provided. To address that connection, I would need access to the full paper.

### Source 65

# Paper Summary: "The Missing Reward: Active Inference in the Era of Experience"

**Title:** The Missing Reward: Active Inference in the Era of Experience

**Author:** Bo Wen

**Abstract Overview:**
The paper contends that Active Inference (AIF) addresses a critical challenge in autonomous AI development. Currently, systems face what Wen calls the "grounded-agency gap"—the challenge that AI cannot independently "formulate, adapt, and pursue objectives in response to changing circumstances."

**How Active Inference Replaces Reward Engineering:**
Rather than relying on externally designed reward functions, AIF employs "an intrinsic drive to minimize free energy," enabling agents to achieve "exploration and exploitation through a unified Bayesian objective." This approach sidesteps the bottleneck of manual reward curation.

**Connection to Free Energy Principle:**
The framework grounds agent behavior in the Free Energy Principle, allowing autonomous systems to naturally balance competing objectives without human intervention. By integrating Large Language Models as generative models with AIF's decision-making framework, agents can "learn efficiently from experience while remaining aligned with human values."

**Core Innovation:**
The synthesis creates AI systems capable of developing autonomously while respecting computational and physical constraints—moving toward genuine autonomous intelligence independent of continuous human reward design.

### Source 66

# Sparsity in Agentic LLMs: Key Findings

## Core Framework
The paper introduces **Sparse Agentic Control (SAC)**, addressing scenarios where LLM systems must select from enormous discrete action spaces (tools, APIs, documents) but only need a small, unknown subset for any given task. The framework models policies with block-sparse representations across M >> 1 actions.

## Formal Stability Guarantees
The research establishes three main theoretical results:

1. **Convergence rates**: "estimation and value suboptimality scale as k (log M / T)^{1/2} under a Policy-RSC condition" – showing performance depends logarithmically on the massive action space size rather than linearly.

2. **Tool support recovery**: Exact identification of relevant tools occurs when T > k log M under incoherence and beta-min conditions, enabling precise action selection.

3. **Dense policy inefficiency**: "any dense policy class requires Omega(M) samples," demonstrating why prompt-only controllers fail at scale – they scale linearly with action space size.

## Why Dense Approaches Fail
Dense policies require sample complexity proportional to the entire action universe, making them fundamentally unstable for large action spaces. Sparse representations achieve polynomial-time stability by exploiting task-specific structure rather than treating all actions equivalently.

The framework extends to partial observability, online learning, and robust variants while maintaining logarithmic scaling advantages.

