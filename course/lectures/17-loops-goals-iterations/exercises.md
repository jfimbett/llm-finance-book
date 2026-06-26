# Lecture 17 Exercises — Loops, Goals, and Iterations

These written exercises test the *methodology* of agentic iteration — goals as
control objects, the observe–propose–act–evaluate–revise loop, agents/skills/hooks,
stopping rules, and the characteristic failure modes (spurious repetition, fake
convergence, goal drift, Goodhart overfitting). Finance tasks (IRR solving, credit
PD/LGD/EL) appear only as vehicles; what is being assessed is your command of the
loop/goal/hook design discipline, not the finance arithmetic. (Coding versions of
these ideas live in the companion `exercises.ipynb`.)

---

### Exercise 1 [B]

A junior quant hands you the following one-line instruction for an agentic loop
that is supposed to harden an implied-volatility solver:

> "Keep improving the vol solver until it's good enough."

**(a)** Explain why this is not a usable *goal* in the control-object sense, by
naming which of the three goal properties (concrete, checkable, decomposable) it
violates.

**(b)** Rewrite it as a complete goal that specifies all three required
components: a **success criterion**, a **stopping rule**, and one **anticipated
failure mode**. Use the option-pricing vehicle: the solver inverts the
Black–Scholes price for the implied vol of a given quoted option, and a reference
script `eval/check_iv.py` reports the absolute pricing residual at the returned
vol.

**(c)** State, for your rewritten goal, which single loop phase (observe, propose,
act, evaluate, revise) each of the three components primarily serves.

---

### Exercise 2 [I]

You must design an iteration loop for the following task:

> Extract the five headline figures (revenue, EBITDA, net debt, interest expense,
> capex) from an arbitrary, never-before-seen PDF credit filing, and emit them as a
> validated JSON record. Filings vary wildly in layout; a wrong figure that slips
> through is costly because it feeds a downstream covenant calculation.

**(a)** Specify the loop using the five phases (observe, propose, act, evaluate,
revise). For each phase say concretely *what happens* in this task.

**(b)** Name the **goal file**, the **success-gate hook**, and the **stopping
criteria** you would attach. The success gate must be more than "the JSON parses" —
state at least two independent checks it enforces.

**(c)** Identify which single component of your loop is what actually *prevents
premature success* (the agent declaring victory before the figures are right), and
explain why that component, and not the others, is the one doing that job.

> **Hint for (a):** the non-obvious first phase is *observe*. Ask what ground truth
> the loop should read from disk before the model proposes anything — remember the
> agent has no durable memory and the filing's true totals must be reconcilable.

---

### Exercise 3 [A]

Recall the nine-agent credit-risk stress-testing loop from the lecture, which
produced this reconciled result for Meridian Components (EAD = \$40m,
EL = PD × LGD × EAD):

| Metric | Base | Stressed (adverse) |
|---|---:|---:|
| PD | 2.5% | 9.0% |
| LGD | 40% | 55% |
| Expected loss | \$0.40m | \$1.98m |
| Expected loss (bps) | 100 bps | 495 bps |

A new team wants to run this loop *unsupervised overnight* to pre-screen a pipeline
of fifty borrowers, keeping only those whose memo concludes "low risk."

**(a)** For each of the three named failure modes below, describe one concrete,
plausible way it could corrupt *this specific loop* under unsupervised operation,
and design the defending mechanism (a hook, a skill constraint, or a skeptic-agent
check). Be specific about what the defense measures and when it fires.
  - **Goodhart overfitting** (optimizing the "low risk" proxy rather than true
    creditworthiness),
  - **Target leakage** in the PD model,
  - **Goal drift** across the fifty-borrower batch.

**(b)** The team proposes deleting the skeptic agent to cut cost, arguing "the
eight hooks already enforce everything that matters." Argue for or against, using
the lecture's distinction between what hooks can guarantee and what they cannot.

**(c)** Give a decision rule the team can apply *per borrower* to decide whether
the loop may auto-finalize a memo or must instead halt in the
`human-review-required` terminal state. Express it as an explicit escalation
predicate over quantities the loop already computes, and justify each clause.
