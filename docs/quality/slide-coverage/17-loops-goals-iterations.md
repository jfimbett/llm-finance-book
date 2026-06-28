# Slide Coverage — Chapter 17: Loops, Goals, and Iterations

Source: `book/chapters/17-loops-goals-iterations/chapter.tex`

## Checklist

### Sections and Subsections
- [x] §1 From Linear Prompts to Iterative Systems
- [x] §1.1 Why One-Shot Prompting Is Fragile
- [x] §1.2 The Goal-Directed Loop: Observe, Propose, Act, Evaluate, Revise (def:goal-directed-loop)
- [x] §1.3 Loops Versus Ordinary Repetition (def:genuine-iteration; spurious repetition anti-pattern)
- [x] §1.4 Claude Code as the Concrete Substrate (Observe→file reads; Propose/Act→agents; Evaluate→skills/hooks; version control as memory)
- [x] §1.5 Situating the Loop in the Agentic-AI Literature (ReAct, Reflexion, Self-Refine, CoT, Toolformer, AutoGen, Generative Agents, spiral model, PDCA)
- [x] §1.6 When Not to Use an Agentic Loop (four questions; Table: task→right tool)
- [x] §2 Goals as Control Objects
- [x] §2.1 Concrete, Checkable, Decomposable Goals (one property per loop phase)
- [x] §2.2 Success Criteria, Stopping Rules, and Anticipated Failure Modes (three-component goal; Example: credit model)
- [x] §2.3 Representing Goals in Files (TASK.md template; validate.sh as executable predicate)
- [x] §2.4 Bad Goals Versus Good Goals (Table: bad→good; each repair re-enables a loop phase)
- [x] §3 Agents as Specialized Iterators
- [x] §3.1 Roles: Worker, Critic, Validator, Planner, Refactorer (def:agent-roles)
- [x] §3.2 Single-Agent Versus Multi-Agent Loops (Reflexion self-reflection; adversarial independence; AutoGen)
- [x] §3.3 Handoffs and Shared State Between Agents (lossy handoff; file-based vs JSON vs prose; trade-lifecycle analogy)
- [x] §3.4 Agents Should Improve Project State, Not Merely Emit Output (durable change = diff/commit)
- [x] §4 Skills as Reusable Procedures
- [x] §4.1 Skills as Reusable Operational Knowledge
- [x] §4.2 Skills Compared to Functions (def:skill-function; composability; Example: /draft-chapter calls /score-content)
- [x] §4.3 Skills Encode Project-Specific Conventions (/new-topic enforces numbering)
- [x] §4.4 Skills Reduce Entropy in Long-Running Projects (financial-controls analogy; SOPs)
- [x] §5 Hooks as Guardrails and Feedback Channels
- [x] §5.1 Hooks as Automatic Interventions (def:hook-types; pre-action = pre-trade limit; post-action = post-trade surveillance)
- [x] §5.2 The Hook Catalogue (pre-run checks; post-write validation; linting/tests; safety checks; commit checks)
- [x] §5.3 Turning Subjective Improvement into Measurable Feedback (opinion→reproducible bit)
- [x] §5.4 Designing Trustworthy Validators (thm:check-not-goal; Goodhart's law; outcome-tied; diverse; holdout; validator logic out of reach)
- [x] §5.5 Failure Hooks (block; revert; escalate; re-enter; failure-policy taxonomy)
- [x] §6 Designing an Iteration Loop
- [x] §6.1 The General Loop Template (seven steps)
- [x] §6.2 Pseudocode and Its Mapping onto a Claude Code Workflow
- [x] §6.3 State, Memory, and Context Management Across Iterations (design for amnesia; what persists vs. what is lost)
- [x] §6.4 Stopping Criteria (def:stopping-rule; success / convergence / budget / human-review)
- [x] §6.5 The Economics of Iteration (marginal-value sketch; latency vs. dollar cost)
- [x] §7 Example 1: Derivative-Free Root-Finding Loop
- [x] §7.1 Problem Setup: f(x) = x³ − x − 2, tolerance |f(x)| < 10⁻³, forbidden derivatives (finance analogue: IRR, implied vol)
- [x] §7.2 Supporting Artifacts: Goal File, Skill, and Hook
- [x] §7.3 Iteration Trace from Poor Start (x = 0): 7 iterations, bracketing, false-position reasoning
- [x] §7.4 Final Report (ROOT-FINDING LOOP — FINAL REPORT; 7 of 12 budgeted; x ≈ 1.5214)
- [x] §8 Example 2: Credit-Risk Stress-Testing Agent Loop
- [x] §8.1 The Goal: A Defensible Credit-Committee Memo (def:el-decomposition; EL = PD × LGD × EAD)
- [x] §8.2 The Combined Macro-Financial Shock (def:scenario-layering; Table: adverse/severe parameters)
- [x] §8.3 The Agent Ensemble (nine agents; two feedback edges: skeptic + failing hooks)
- [x] §8.4 The Skills (seven named skills: financial-statement-normalization, credit-feature-engineering, pd-modeling, macro-stress-scenario-design, covenant-liquidity-analysis, lgd-collateral-valuation, credit-memo-writing)
- [x] §8.5 The Hooks (eight checklist items; leakage check; "low risk" gate; Goodhart + skeptic as defense)
- [x] §8.6 The Eleven-Iteration Narrative (naive PD 1.2% → clean 2.5% → stressed 9%; leakage hook fires on iter 4; skeptic pushes back on iter 9)
- [x] §8.7 The Compact Final Result Table (base vs stressed; EL reconciles; conditional $30m, tighter covenants)
- [x] §9 Human Oversight, Accountability, and Audit Trails
- [x] §9.1 Human-in-the-Loop and Escalation Points (def:escalation-trigger; trigger list; unsigned sign-off block)
- [x] §9.2 Accountability and Sign-Off in Regulated Finance (SR 11-7; three pillars; def:model-ownership; skeptic ≠ sign-off)
- [x] §9.3 Reproducible Audit Trails (version control; structured run log; content-addressed inputs; Example: audit-ready run log)
- [x] §10 Failure Modes in Agentic Iteration
- [x] §10.1 Infinite Loops and Fake Convergence (def:fake-convergence; hard budget; external validator)
- [x] §10.2 Goal Drift and Premature Success (file-based goal defense; tolerance hook)
- [x] §10.3 Overfitting to Validation Checks (thm:goodhart degradation; diverse checks; holdout; adversarial review)
- [x] §10.4 Excessive Agent Delegation (deterministic subtasks → functions; when-not-to-loop diagnostic)
- [x] §10.5 Warning Signs and Remedies (Table: failure mode → warning sign → control)
- [x] §11 Practical Design Patterns
- [x] §11.1 Planner–Executor–Critic (ReAct + Reflexion; multi-step tasks)
- [x] §11.2 Generate–Test–Revise (machine-checkable; Self-Refine; Goodhart risk)
- [x] §11.3 Scaffold–Draft–Audit–Repair (rubric-scored; this book's own pattern)
- [x] §11.4 Data-Pipeline: Build–Validate–Document (lineage; provenance; rebuild-on-fail)
- [x] §11.5 Credit-Model: Build–Stress-Test–Red-Team–Finalize (mandatory stress + red-team; SR 11-7 encoded)
- [x] §11.6 Choosing a Pattern (Table: goal properties → pattern; patterns nest)
- [x] §12 Summary and Takeaways
- [x] §12.1 Feedback must be informative (central thesis)
- [x] §12.2 Agents specialize / skills reuse / hooks enforce
- [x] §12.3 Finance demands: explicit goals, validation, stress testing, skepticism

### Named Methods / Results / Systems
- [x] ReAct (Yao, 2022)
- [x] Reflexion (Shinn, 2023)
- [x] Self-Refine (Madaan, 2023)
- [x] Chain-of-thought (Wei, 2022)
- [x] Toolformer (Schick, 2023)
- [x] AutoGen (Wu, 2023)
- [x] Generative Agents (Park, 2023)
- [x] Spiral model (Boehm, 1988)
- [x] PDCA cycle (Deming, 1986)
- [x] Goodhart's law (Goodhart, 1984)
- [x] SR 11-7 (model risk management guidance)
- [x] BCBS 2018 stress testing principles
- [x] thomas2002credit (credit scoring tradition)
- [x] def:goal-directed-loop
- [x] def:genuine-iteration
- [x] def:agent-roles (worker/critic/validator/planner/refactorer)
- [x] def:skill-function (the correspondence)
- [x] def:hook-types (pre-action / post-action)
- [x] def:stopping-rule
- [x] def:escalation-trigger
- [x] def:model-ownership (sign-off)
- [x] def:el-decomposition (EL = PD × LGD × EAD)
- [x] def:scenario-layering (base / adverse / severe)
- [x] def:fake-convergence
- [x] thm:check-not-goal (Goodhart, formally)
- [x] thm:goodhart (degradation, informal)

### Key Numbers
- [x] AUC target 0.78 (credit model goal)
- [x] f(x) = x³ − x − 2, single root ≈ 1.52
- [x] tolerance |f(x)| < 10⁻³
- [x] Iteration trace: 7 of 12 budgeted; final x ≈ 1.5214
- [x] Meridian: \$40m revolver
- [x] naive PD ≈ 1.2%; leverage 3.0× → 3.8× after add-backs
- [x] customer concentration: top 2 customers = 45% of receivables
- [x] cash conversion cycle: crept 70 → 95 days
- [x] base PD = 2.5%, adverse PD = 9%, severe PD = 13%
- [x] base LGD = 40%, adverse LGD = 55%, severe LGD = 60%
- [x] EAD = \$40m (both scenarios)
- [x] base EL = \$0.40m (100 bps); stressed EL = \$1.98m (495 bps)
- [x] liquidity shortfall ≈ \$6m under stress
- [x] Revenue shock: −20% adverse, −30% severe
- [x] Gross margin: −300 bps adverse, −450 bps severe
- [x] Rate: +250 bps adverse, +350 bps severe
- [x] DSO: +25 days adverse, +40 days severe
- [x] Inventory days: +20 adverse, +35 severe
- [x] ICR covenant: tightened to 2.5×
- [x] conditional approval: \$30m facility, tighter covenants, more collateral
- [x] economics sketch: \$0.50/iteration, 8 iterations ≈ \$4 (illustrative)
- [x] nine agents in credit loop
- [x] eleven iterations in credit loop

## Omissions

All items initially identified as missing are now covered in the updated deck. No unchecked items remain under this section.
