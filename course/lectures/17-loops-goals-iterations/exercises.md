# Exercises — Lecture 17: Loops, Goals, and Iterations

## Exercise 1 [B] — Turning a Vague Goal into a Control Object

[Placeholder] Give the student a vague goal (e.g., "make the credit memo better")
and ask them to rewrite it as a concrete, checkable, decomposable goal suitable
for an agentic loop. They must state (a) the success criterion a hook could
verify, (b) at least one stopping rule, and (c) where the goal would live as a
file (TASK.md, a rubric, or a validation script). The point is to practice goals
*as control objects*, not pure finance.

*Relates to Section 2: Goals as Control Objects.*

---

## Exercise 2 [I] — Build the Root-Finding Loop with a Tolerance Hook

[Placeholder] Using Claude Code (or pseudocode plus an evaluator script), build
the derivative-free loop that finds a zero of f(x)=x^3-x-2 starting from x=0. The
student must: write the goal file (tolerance |f(x)|<0.001), write a skill that
runs the evaluator, and write a hook that blocks a "success" declaration unless
the tolerance is met. Deliverable: the iteration trace and the final report. The
emphasis is the *loop mechanics and the hook*, not the numerical method.

*Relates to Section 7: Example 1 — A Naive Derivative-Free Root-Finding Loop.*

---

## Exercise 3 [A] — Design the Credit-Risk Agent Ensemble and Its Hooks

[Placeholder] Design (on paper, then optionally prototype) a multi-agent loop for
the credit-risk stress-testing memo. The student must specify: the agent ensemble
and their handoffs; at least four skills; at least four hooks (including a
target-leakage check and a skeptic sign-off gate); and the stopping criteria.
They must then explain *why* this task needs many feedback-driven iterations
rather than a single pass, and identify two failure modes (e.g., Goodhart
overfitting, premature success) their hooks defend against.

*Relates to Sections 8, 9, and 10: the credit-risk loop, governance, and failure modes.*
