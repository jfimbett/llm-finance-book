# Lecture 17: Loops, Goals, and Iterations: Agents, Skills, and Hooks

## Learning Objectives

By the end of this lecture, students should be able to:

1. Explain why one-shot prompting is fragile and describe the goal-directed loop (observe, propose, act, evaluate, revise).
2. Write goals as concrete, checkable, decomposable control objects and encode them in project files.
3. Distinguish the roles of agents, skills, and hooks and assemble them into an iteration loop with explicit stopping criteria.
4. Trace a simple feedback loop (derivative-free root finding) and a complex multi-agent loop (credit-risk stress testing).
5. Diagnose failure modes of agentic iteration and apply hooks and stopping rules as remedies.
6. Select an appropriate design pattern for a given finance workflow.

---

## 1. From Linear Prompts to Iterative Systems

[Placeholder] Why one-shot prompting is fragile; the goal-directed loop; loops vs. ordinary repetition; Claude Code as the substrate; grounding in the agentic-AI literature (ReAct, Reflexion, Self-Refine); and when *not* to use an agentic loop.

## 2. Goals as Control Objects

[Placeholder] Concrete, checkable, decomposable goals; success criteria, stopping rules, and failure modes; representing goals in files (TASK.md, TOPIC.md, STATUS.md, rubrics, validation scripts); bad goals vs. good goals.

## 3. Agents as Specialized Iterators

[Placeholder] Agent roles (worker, critic, validator, planner, refactorer); single- vs. multi-agent loops; handoffs and shared state; agents should improve project *state*, not just emit output.

## 4. Skills as Reusable Procedures

[Placeholder] Skills as reusable operational knowledge; skills compared to functions (scoped, documented, repeatable, composable); skills encode project conventions; skills reduce entropy.

## 5. Hooks as Guardrails and Feedback Channels

[Placeholder] Hooks as automatic pre/post interventions; the hook catalogue; turning subjective improvement into measurable feedback; designing trustworthy validators; failure hooks.

## 6. Designing an Iteration Loop

[Placeholder] The seven-step loop template; pseudocode mapped onto a Claude Code workflow; state/memory/context across iterations; stopping criteria; the economics of iteration.

## 7. Example 1: A Naive Derivative-Free Root-Finding Loop

[Placeholder] Find a zero of f(x)=x^3-x-2 without derivatives; the goal file (tolerance |f(x)|<0.001), the evaluator skill, the success hook; a realistic iteration trace from x=0; the final report. Pedagogical point: a loop improves a state variable using feedback.

## 8. Example 2: A Credit-Risk Stress-Testing Agent Loop

[Placeholder] A mid-sized borrower seeking a revolving facility; the goal of a defensible credit-committee memo (PD, LGD, expected loss, drivers, recommendation); the combined macro shock; the agent ensemble; the skills; the hooks; the eleven-iteration narrative; the compact final result table.

## 9. Human Oversight, Accountability, and Audit Trails

[Placeholder] Human-in-the-loop and escalation; accountability and sign-off in regulated finance; reproducible audit trails (commits, logs, traces as evidence).

## 10. Failure Modes in Agentic Iteration

[Placeholder] Infinite loops and fake convergence; goal drift and premature success; Goodhart overfitting to validation checks; excessive agent delegation; warning signs and remedies.

## 11. Practical Design Patterns

[Placeholder] Planner-executor-critic; generate-test-revise; scaffold-draft-audit-repair; data-pipeline build-validate-document; credit-model build-stress-test-red-team-finalize; choosing a pattern.

## 12. Summary and Takeaways

[Placeholder] Iteration is useful only when feedback is informative; agents specialize, skills reuse, hooks enforce; complex finance workflows demand explicit goals, validation, stress testing, and skepticism.

---

## Further Reading

Companion book chapter: **Chapter 17 — Loops, Goals, and Iterations: Agents, Skills, and Hooks** (`book/chapters/17-loops-goals-iterations/chapter.tex`). The chapter goes deeper on the design of iterative agentic systems and the full credit-risk case study. See also Appendices A–F for the concrete tooling (Claude Code, Codex CLI, Hugging Face, the SDKs, Git/GitHub, and Cline).
