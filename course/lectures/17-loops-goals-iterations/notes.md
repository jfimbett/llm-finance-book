# Lecture 17: Loops, Goals, and Iterations: Agents, Skills, and Hooks

This is the methodology capstone of the course. Earlier lectures treated a large
language model as a *function*: prompt in, completion out. This lecture argues
that the primary unit of design is the **loop**, not the prompt — a system that
repeatedly observes the world, proposes an action, acts, evaluates the result
against an explicit goal, and revises. Concrete tooling (Claude Code,
Codex, the SDKs, Git) lives in book Appendices A–F; here we study the *design of
iterative agentic systems* rather than any single tool.

## Learning Objectives

By the end of this lecture you should be able to:

- Explain why one-shot prompting is fragile and describe the goal-directed loop
  (observe, propose, act, evaluate, revise) that replaces it.
- Write goals as concrete, checkable, decomposable **control objects** and encode
  them in project files (TASK.md, TOPIC.md, rubrics, validation scripts).
- Distinguish the roles of **agents, skills, and hooks** and assemble them into a
  working loop with explicit stopping criteria.
- Trace a deliberately simple feedback loop (derivative-free root finding) and a
  complex multi-agent loop (credit-risk stress testing), and explain why each
  requires real, feedback-driven iteration.
- Diagnose the common failure modes of agentic iteration (infinite loops, fake
  convergence, goal drift, premature success, Goodhart overfitting, and excessive
  delegation) and apply hooks and stopping rules as remedies.
- Select an appropriate design pattern (planner–executor–critic,
  generate–test–revise, scaffold–draft–audit–repair, and others) for a given
  finance workflow.

---

## 1. From Linear Prompts to Iterative Systems

The natural mental model after learning to call an API is that the LLM is a
function: shape the prompt, read the completion. This is adequate for short,
self-contained, verifiable-at-a-glance tasks — summarize a filing, extract a
counterparty name. But almost every *consequential* use of an LLM in finance is a
**process**, not a single call. It is a sequence of model invocations interleaved
with tool calls, validations, human checks, and revisions, organized around a goal
the first call almost never achieves.

A one-shot prompt is an **open-loop controller**. The model emits an output that
flows downstream without the model ever learning whether it was correct.
There is no error-correction channel. If a generated SQL query references a
non-existent column, the system never finds out. If a valuation script divides by
a zero free-cash-flow base, it reports the wrong number as confidently as a right
one. The fragility compounds along three axes:

1. **Errors propagate without attenuation.** When one completion must parse,
   extract, compute, and narrate, an early error corrupts everything after it,
   and the single forward pass gives no chance to notice the inconsistency.
2. **The specification exceeds one pass.** Real tasks carry interacting
   constraints (turnover limits, sector caps, tracking-error budgets, tax-lot
   accounting all at once). The probability of jointly satisfying them falls
   roughly multiplicatively as constraints accumulate.
3. **The model cannot see the environment.** It does not know the real schema,
   the current rate, or whether a file it assumed exists actually does. One-shot
   prompting asks the model to act on a *hallucinated* model of the world.

The combination — silent failure plus reliability that degrades sharply with
complexity — is exactly the regime in which most consequential finance work lives.
A junior analyst does not write a DCF top-to-bottom and submit it; they sketch,
sanity-check the terminal value, notice the implied margin is above the sector
ceiling, walk the assumption back, re-run, and circulate. The expert workflow is
intrinsically iterative.

---

## 2. The Goal-Directed Loop: Observe, Propose, Act, Evaluate, Revise

The remedy is to **close the loop**. Given a goal $G$ with a success predicate
$\mathrm{ok}(\cdot)$, repeat five phases until $\mathrm{ok}$ holds or a stopping
rule fires:

1. **Observe.** Read the current environment state $s_t$ (files, test results,
   data, prior outputs).
2. **Propose.** Generate a candidate action $a_t$ to move toward $G$, conditioned
   on $s_t$ and history.
3. **Act.** Execute $a_t$, producing new state $s_{t+1}$.
4. **Evaluate.** Compute feedback $e_{t+1}$ by applying checks — tests, a rubric,
   a validator, a human review — and assess whether $\mathrm{ok}(s_{t+1})$ holds.
5. **Revise.** If the goal is unmet and the stopping rule has not fired, fold
   $e_{t+1}$ into context and return to Observe.

The ordering encodes a dependency structure. *Propose* is conditioned on what
*Observe* read, so the model reasons about the real environment. *Evaluate* runs
against what *Act* produced, so the verdict is grounded in a real artifact. Most
importantly, *Revise* feeds the concrete evidence of what went wrong back into the
next *Propose* — exactly the error-correction channel one-shot prompting lacks.

> **The Evaluate phase is where most engineering value lives.** A loop is only as
> good as its feedback. If $\mathrm{ok}(\cdot)$ is weak — accepting outputs that
> are wrong — the loop will happily converge to something useless. The feedback
> function deserves at least as much design attention as the prompt.

### Loops versus ordinary repetition

A repeated procedure is **genuinely iterative** only if the action at step $t+1$
depends on the evaluated feedback $e_{t+1}$ from step $t$:
$a_{t+1} = \pi(s_{t+1}, e_{t+1}, h_t)$. If $a_{t+1}$ is independent of $e_{t+1}$,
it is mere repetition — *sampling*, not iteration.

The canonical anti-pattern is **spurious repetition**: re-prompting "fix the
failing test" without reading whether the test now passes. The model runs
repeatedly but no information from the test runner flows back; the second attempt
is no more likely to be right than the first, and accumulated partial edits can
leave the codebase worse. The genuinely iterative version captures the exact
assertion that failed and the offending values, and includes that message in the
next prompt. Both issue the same number of calls; only one carries information
forward. **Whenever you build something that calls a model more than once, the
first design question is not "how many times?" but "what does iteration $t+1$
learn from iteration $t$?"**

### Lineage: the loop is old engineering wisdom

The loop synthesizes two literatures. On the LLM side: **ReAct** (Yao et al.,
2022) interleaves reasoning and action (Observe–Propose–Act); **Reflexion**
(Shinn et al., 2023) adds verbalized Evaluate–Revise; **Self-Refine** (Madaan et
al., 2023) is the single-model special case; **chain-of-thought** (Wei et al.,
2022) makes Propose's reasoning inspectable; **Toolformer** (Schick et al., 2023)
gives Act real effects; **AutoGen** (Wu et al., 2023) splits phases across roles.
On the engineering side: Boehm's **spiral model** (1988) and Deming's **PDCA
cycle** replaced single-pass waterfall with risk-driven closed-loop cycles. That
an LLM agent loop, a 1980s software methodology, and a mid-century manufacturing
discipline all converge on the same shape is no coincidence. It is what any
system that must produce correct output under uncertainty looks like once it
closes its feedback loop.

<!-- BOOK-ONLY: the control-theoretic reading (open-loop vs feedback control, gain/instability predicting failure modes) is a worthwhile deep dive but too dense for the live lecture; mention it in one sentence only. -->

### When *not* to use a loop

Power is not appropriateness. A loop is justified only when iteration buys
something. Run through four questions: (1) Is the output **mechanically
verifiable**? No check, no feedback, no loop. (2) Does the task require
**reasoning that varies with the input**? If the same procedure applies every
time, write the procedure. (3) Is the first attempt **likely wrong and being
wrong costly**? That is where loops earn their keep. (4) Can a wrong intermediate
action cause **irreversible harm** (sending an order, wiring funds)? Then add a
human gate or sandbox before Act — or a loop may be the wrong architecture.

| Task | Right tool | Why |
|---|---|---|
| Compute a bond's yield to maturity | Pure function | Deterministic, specifiable |
| Daily download of a price file | Cron job | Scheduled, no per-run reasoning |
| Extract figures from a novel filing | Loop with validator | Variable input, checkable output |
| Draft and harden a valuation model | Agentic loop | Low one-shot reliability, costly silent errors |

---

## 3. Goals as Control Objects

If the loop is the unit of design, the goal is its **setpoint**. A goal is a
control object — an artifact that actively governs the loop's behavior, decides
when it stops, and decides whether its output is acceptable — not a preamble.

A goal is usable when it has three properties, each mapping to a loop phase:

- **Concrete** (for *Act*): it names the artifact to produce or change. "Improve
  the credit model" names nothing; "raise the out-of-sample AUC of
  `models/credit.py`, measured by `eval/backtest.py`, to ≥ 0.78" names the file,
  the measuring script, and the target.
- **Checkable** (for *Evaluate*): satisfaction can be verified mechanically or by
  a stated rubric. "Make the writing better" is uncheckable; "every rubric
  dimension scores ≥ 90 as reported by `/score-content`" supplies the success
  predicate $\mathrm{ok}(\cdot)$.
- **Decomposable** (for *Revise*): it splits into local subgoals checkable
  independently. "Bring the book to release quality" → per-chapter →
  per-dimension. Decomposability localizes failures, bounds context, and enables
  multi-agent decomposition.

### Three components every complete goal specifies

The most common defect is specifying only the first of these:

1. **Success criterion** — the predicate that defines *done because we won*: "all
   tests pass and coverage ≥ 90%."
2. **Stopping rule** — the condition to halt *even though we did not win*: an
   iteration cap, a token/wall-clock budget, a no-progress detector. A loop
   without one can run forever or thrash. (`max_refine_iterations` is a stopping
   rule; `quality_threshold` is a success criterion.)
3. **Anticipated failure modes** — the ways the loop is expected to go wrong,
   named in advance so the system can detect them: gaming the proxy, converging
   to a local optimum, oscillating, "succeeding" by weakening its own test.

Example — a complete credit-model goal: *Success:* out-of-sample AUC ≥ 0.78 on
the 2023 book with calibration error below a bound. *Stopping:* halt after eight
iterations, or after three consecutive iterations failing to improve validation
AUC by > 0.002. *Failure modes:* overfitting the validation split (mitigated by a
final lockbox test set), future-information leakage (temporal-split check),
trading calibration for discrimination (explicit calibration bound).

### Represent goals in files

A goal in a chat prompt is fragile: it vanishes when context rolls over and no
two runs share a definition of success. A goal in a **file** is durable across
context windows, auditable, version-controlled, and — when executable — *directly
usable as the Evaluate phase*. The decisive move is to make the success criterion
not merely *stated* but *executable*. A `validate.sh` that exits 0 iff the goal is
met can be wired into Evaluate and enforced before commit, so "done" and
"acceptable" are literally the same code.

### Bad goals vs good goals

| Bad goal | Good goal | What the repair adds |
|---|---|---|
| "Improve the chapter." | "Every rubric dimension ≥ 90 via `/score-content`." | Checkable predicate + fixed measure |
| "Make the credit model more accurate." | "Held-out AUC of `credit.py` ≥ 0.78 on 2023, no post-origination features." | Named artifact, target, leakage guard |
| "Get the tests passing." | "`pytest` exits 0 *and* coverage ≥ 90%; swallowing exceptions forbidden." | Second criterion + anti-gaming guard |
| "Keep improving the portfolio." | "Maximize backtested Sharpe s.t. turnover ≤ 30%; stop after 8 runs or Sharpe gain < 0.05." | Constraint + stopping rule |

Each bad goal disables a loop phase: unconcrete, uncheckable, or unbounded. Each
repair restores it. **A loop is only ever as good as the goal you hand it.**

---

## 4. Agents, Skills, and Hooks — The Three Building Blocks

The loop is abstract; we need a substrate that supplies its five phases. We use
Claude Code as that substrate because its primitives map cleanly onto the loop.

### Agents as specialized iterators

The useful agents are **specialized iterators**, not chatbots-with-tools: each
occupies a narrow position in the loop, performs one well-defined transformation
on project state, and hands control onward. Five canonical roles:

- **Worker** — produces or transforms the primary artifact (the only role that
  *must* exist).
- **Critic** — reads the artifact and returns a structured judgment (strengths,
  weaknesses, change requests) without rewriting; supplies the natural-language
  *gradient*.
- **Validator** — applies an objective, ideally deterministic test returning
  pass/fail (compiles? tests pass? score above threshold?). The role most often
  omitted and most sorely missed: a critic's judgment is itself a fallible model
  output; a validator built on a compiler or test suite is not subject to
  persuasion. The critic is the senior reviewer who says the model looks
  aggressive; the validator is the limit system that rejects the trade.
- **Planner** — decomposes a goal into ordered subtasks.
- **Refactorer** — improves internal structure while preserving behavior.

**Single- vs multi-agent.** A single self-reflective agent (generate → critique
self → revise, à la Reflexion) is the simplest thing to build and often
sufficient. Separation earns its keep when the **critic must be genuinely
independent** of the worker — a model critiquing its own fresh text is biased
toward endorsing it. The right default is the *smallest* number of agents that
gives the critic real independence; do not split roles because the diagram looks
sophisticated.

**Handoffs.** With multiple agents, the loop lives or dies on handoff quality.
Channels in decreasing robustness: a committed **file** the next agent reads → a
**structured output** (fixed-schema JSON) → free-form natural-language summary.
Guard against the **lossy handoff** (a critic that receives a prose summary
critiques the summary, not the page). The analogue is front-office/back-office
information loss in the trade lifecycle: a single authoritative record everyone
reads from, not a chain of re-keyed summaries.

**The central discipline:** an agent's value is the durable, inspectable change it
makes to project state (files written, tests green, a score raised, a commit
recorded), *not* the text it prints. A brilliant critique no file records has
changed nothing. We measure an agent by its diff.

### Skills as reusable procedures

If agents are the *who*, a **skill** is the *how*: a named, reusable, composable
sequence of steps that accomplishes a recurring task the same way every time
(`/new-topic`, `/draft-chapter`, `/score-content`, `/iterate-book-quality`). A
loop run a hundred times whose steps are improvised each run is not the same loop
twice; a skill makes the procedure a durable, version-controlled artifact.

The load-bearing analogy: **a skill is to a workflow what a function is to a
computation.** A well-formed skill has a *name* you invoke it by, *scoped inputs*,
a *single documented responsibility*, *repeatability* (same inputs → same
procedure), and *composability* (one skill calls another, as `/draft-chapter`
calls `/score-content` calls `/refine-until-threshold`). Skills also **freeze
conventions** into enforceable form: `/new-topic` mechanizes the convention that
chapter/lecture/notebook $N$ share a topic, so it cannot drift. And they **reduce
entropy**: every invocation pushes a long-running project back toward consistency
instead of away from it. The analogy is a trading firm's control framework — the
standard operating procedures that make the correct action the default action.

### Hooks as guardrails and feedback channels

Agents act and skills sequence them, but neither *guarantees* the result meets
standards. A **hook** is a script registered to run automatically on an event —
before a tool is used, after a file is written, when a session ends — outside the
agent's control. Its defining property: **it does not depend on the agent's
cooperation.**

- A **pre-action hook** fires before an action and can block it (a precondition
  check). Analogue: the pre-trade limit check.
- A **post-action hook** fires after and can validate, record, repair, or
  escalate. Analogue: post-trade surveillance.

A hook converts the subjective "is this good?" into an objective, enforced bit.
"This chapter reads well" is an opinion; "this chapter compiles, every citation
resolves, and every dimension scores ≥ threshold" is a fact a hook establishes
and reports. The loop's stopping condition can then hang on that bit, not on the
model's confidence. A hook's verdict is *reproducible*, so progress against
it is real progress, not a fluctuation in the model's mood.

**Designing trustworthy validators.** The power of hooks creates Goodhart's law:
when a measure becomes a target, it ceases to be a good measure. *A passing check
is necessary, not sufficient.* The loop optimizes for $V = \text{pass}$, not for
the true goal $G$, so unless passing $V$ entails meeting $G$, an optimizing loop
will find artifacts that pass yet fail. Defenses: prefer outcome-tied checks over
proxy checks; combine heterogeneous checks whose conjunction is hard to satisfy
by accident; keep validator logic out of the worker's reach; hold some checks back
as a hidden release-time holdout. This is model-risk management's playbook:
out-of-sample testing, independent benchmarks, validation separated from
development.

**Failure hooks.** What the system does on a failing verdict, escalating in
severity: **block** (refuse to proceed), **revert** (undo a regression to
last-good), **escalate** (hand to a human when no obvious edit fixes it), or
**re-enter** (feed the failure message back as the next iteration's input). The
deciding question is whether the failure is recoverable and by whom. This is the
operational-risk playbook in miniature: breached limit blocks; erroneous trade is
reversed; loss beyond mandate escalates; near miss feeds back into controls.

---

## 5. Designing an Iteration Loop

None of the components is useful alone: a goal with no iterator is a wish; an
iterator with no goal wanders; either without guardrails will eventually declare
victory the author never intended. Assemble them.

### The seven-step template

1. **Read the current state.** Establish ground truth from disk and version
   control before acting. State lives on disk, not in the agent's memory.
2. **State the next local goal.** The global goal is rarely reachable in one move;
   name a concrete, checkable objective for *this* turn.
3. **Propose a change** (reason).
4. **Apply the change** (act — write to disk; only now has the world changed).
5. **Run validation** — a deterministic check measures the new state against the
   goal. The agent does not grade its own work; the validator does.
6. **Interpret feedback** — extract signal: did the residual shrink or grow, in
   which direction, by how much? This turns a blind retry into a directed search.
7. **Decide: stop, continue, or escalate.** Every loop must be able to reach a
   stop *or escalate* state.

Validation (5) is separated from interpretation (6), and both from the decision
(7). Collapsing them removes the independent check that makes the loop
trustworthy. And the decision always includes **escalate** — a loop that can only
succeed or grind forever will eventually grind forever.

As pseudocode (each line maps to a Claude Code primitive — `read_state`/`read_goal`
are file reads, `propose`+`apply` is the ReAct reason-then-act turn, `validate` is
a skill, the accept/reject branch is Self-Refine, `commit` is the audit trail, and
`escalate`/`emit_report` are hook-gated):

```
state <- read_state()
goal  <- read_goal()
best  <- evaluate(state, goal)
while not goal.satisfied(best) and not goal.budget_exhausted():
    local  <- choose_objective(state, best)
    change <- propose(state, local)        # REASON
    state2 <- apply(change, state)         # ACT
    report <- validate(state2)             # deterministic check
    if report.improves_on(best):
        commit(state2, summarize(change, report))
        state, best <- state2, report.score
    else:
        state <- rollback(state)           # reject, keep best
    if stalled(history) or report.requires_human:
        escalate(state, report); break
emit_report(state, best, history)
```

The accept/reject structure makes the loop robust to the agent's mistakes: a bad
proposal costs one iteration, not the whole run, because everything is validated
before commit and rolled back if it does not improve.

### State, memory, and amnesia

The most common reason a sound loop fails in practice is misunderstanding *where
state lives*. An LLM agent has **no durable memory** between turns; its context
window is truncated or summarized. Design for amnesia: assume the agent remembers
nothing except what it reads from disk. A useful mental model — *the agent is a
new employee every morning who reads the files, does one day's work, commits it,
and is replaced overnight by someone equally capable with no memory of yesterday.*

Persists (external to the model): files in the working tree; git history (the
loop's long-term memory); validation reports written to a known path; a
human-readable **status table / scratchpad** (current best, iterations spent, what
was tried, what failed — the single most valuable artifact to maintain). Lost:
the agent's chain of thought, unsaved intermediate values, earlier nuance. The
rule is **write before you forget.** A side benefit is that the loop becomes
**resumable**: all state on disk means a run interrupted at iteration 12 restarts
at 13 from a fresh agent.

### Stopping criteria and economics

A loop that cannot stop is a liability. A loop is **well-formed** only if at least
one stopping rule is *guaranteed-terminating*. Combine: (1) success (goal met),
(2) convergence (no improvement for $k$ iterations), (3) **budget exhaustion**
(the guaranteed-terminating rule every loop must include), (4)
human-review-required. Only the budget is non-negotiable: the goal may be
unreachable, the agent may make tiny non-zero improvements forever, no guardrail
may trip. Convergence and escalation make the loop *smart*; the budget makes it
*safe*.

Each iteration costs tokens, compute, and latency. Marginal improvement shrinks
as the loop approaches the goal while cost per iteration stays roughly constant,
so there is a point past which the next iteration costs more than it is worth.
Illustrative sketch: if manual revision is worth ~$200/run and each iteration
costs ~$0.50 and ~90 seconds, eight iterations cost ~$4 and four minutes — an
obvious win. But iterations 15–30 chasing quality the reviewer cannot distinguish
might cost another ~$8 for nothing. Set the budget where marginal value crosses
marginal cost. (Latency binds when the loop sits in a human's critical path;
dollar/token cost binds when it runs unattended overnight.)

---

## 6. Example 1: A Naive Derivative-Free Root-Finding Loop

A deliberately transparent worked example. **The point is not numerical
analysis** — we are *not* teaching Newton, secant, or bisection as algorithms.
The point is that an iteration loop can improve a state variable using **feedback
alone**, reading the sign and size of an error and adjusting, without the agent
ever being told an update formula.

**Setup.** Find $x$ with $f(x) = x^3 - x - 2 \approx 0$ to tolerance
$|f(x)| < 10^{-3}$. There is a single real root near $x \approx 1.52$. Crucially,
the agent may **evaluate** $f$ at any point but is **forbidden derivatives**: no
$f'(x) = 3x^2 - 1$, no Newton update. All it has is "what is $f$ at this point?".
This is sign-and-magnitude guided search, closer to bisection / false position.

**Finance analogue.** This is mechanically an **IRR or implied-volatility
solver**. To find an IRR we seek the rate $r$ with
$\mathrm{NPV}(r) = \sum_t c_t/(1+r)^t = 0$ — no closed-form inverse, so evaluate
NPV at trial rates and move the guess by the sign (too-high NPV ⇒ rate too low).
Implied vol is the same: price the option at a trial vol, compare to market,
bracket. The loop below is an IRR solver with $f$ swapped out.

**Three supporting artifacts** (one per loop component):

- **Goal file** — objective `|f(x)| < 0.001`; allowed: evaluate $f$; forbidden:
  derivatives/Newton; budget: ≤ 12 iterations; success: evaluator prints
  `|f(x)| < 0.001`.
- **Skill** — `python evaluator.py "$x" | tee -a results.log`, appending a line
  like `x=1.5  f(x)=-0.125` that becomes the loop's on-disk memory.
- **Hook** — a stop hook that re-reads the last logged residual and exits nonzero
  unless $|f(x)| < 10^{-3}$, so the agent literally cannot declare success while
  the residual is too large.

None of the three contains a root-finding algorithm: the goal says *what*
convergence means, the skill says *how* to measure, the hook *enforces* it. How to
move the guess is left to the agent's reasoning over feedback.

### Iteration trace (from the poor start $x = 0$)

| Iter | $x$ | $f(x)$ | Agent's reasoning |
|---:|---:|---:|---|
| 1 | $0$ | $-2$ | Negative; root is to the right. Jump up. |
| 2 | $2$ | $4$ | Positive now; root bracketed in $(0,2)$. |
| 3 | $1.5$ | $-0.125$ | Negative but small; root just above $1.5$. |
| 4 | $1.6$ | $0.496$ | Positive; bracket tightens to $(1.5,1.6)$. |
| 5 | $1.52$ | $-0.008192$ | Tiny negative; nudge up slightly. |
| 6 | $1.522$ | $\approx 0.004$ | Overshot to small positive; back off a touch. |
| 7 | $1.5214$ | $\approx 0$ | $|f(x)| < 0.001$: tolerance met, hook passes. |

The **sign change** between $x=0$ and $x=2$ is the entire engine: a continuous
function going negative→positive crosses zero in between — no derivative needed.
From iteration 3 the agent refines the bracket; because $|f(1.5)| \ll |f(1.6)|$, a
false-position reading places the root near $1.5$, so it tries $1.52$, then nudges
to $1.522$ (overshoot), then backs to $1.5214$. Had it tried to declare success at
iteration 5 ($|f| = 0.008192$) the hook would have vetoed it.

The path is *not* optimal — a textbook method would not zig-zag past the root at
iteration 6 — and that inefficiency *is the point*. The loop reaches tolerance
**without an algorithm, using only feedback**, which means the same loop works
when the "residual" is a failing test, a style violation, or a reviewer's
objection rather than a number. The final report reconstructs everything from
`results.log` and git: root at $x \approx 1.5214$, 7 of 12 iterations, stop hook
PASS, trace `0 → 2 → 1.5 → 1.6 → 1.52 → 1.522 → 1.5214`. **This is the template
every later chapter instantiates; only the state variable, the validator, and the
definition of "residual" change.**

---

## 7. Example 2: A Credit-Risk Stress-Testing Agent Loop

The root-finding loop optimized a single scalar against a sharp target. Most
finance decisions optimize a **judgment**: a position that must be internally
consistent, empirically grounded, stress-tested, and able to survive an
adversarial reading. This is the chapter's capstone.

**Meridian Components** (fictional; *all figures illustrative*) is a mid-sized
private manufacturer seeking a **$40 million** committed revolver. On the surface
it looks comfortable: three years of revenue growth, rising reported EBITDA,
leverage inside appetite. But it sells into two cyclical end markets, carries
specialized illiquid inventory, and concentrates receivables in a few customers.
A combined shock could move it from "comfortable" to "covenant breach" fast.

**The goal is not "estimate the PD."** A point estimate is an output, not a goal —
nothing can fail against it. The goal is a **credit-committee memo a committee
would accept**, which makes it checkable. The expected-loss vocabulary:

$$\mathrm{EL} = \mathrm{PD} \times \mathrm{LGD} \times \mathrm{EAD}$$

where PD is the one-year default probability, LGD = 1 − recovery rate, and EAD is
the drawn balance plus expected further drawdown. The memo must assign PD (horizon
+ method), state LGD (collateral logic), state EAD (drawdown assumption), compute
EL in dollars and bps, identify risk drivers, and give a recommendation — lend /
modify / decline. A checkable table encodes the acceptance criteria, each
row checked by a hook or the skeptic, including a "low risk" language gate
permitted *only if* base and stressed EL both fall below thresholds.

### The combined macro-financial shock

Stress testing prices the *tail*, not the mean. The shock is a **parameter table**
(so every agent consumes the same assumptions and outputs regenerate
deterministically), in three layers — base, adverse, severe:

| Shock parameter | Adverse | Severe |
|---|---:|---:|
| Revenue | −20% | −30% |
| Gross margin | −300 bps | −450 bps |
| Benchmark interest rate | +250 bps | +350 bps |
| Days sales outstanding (DSO) | +25 days | +40 days |
| Inventory days | +20 days | +35 days |
| Refinancing of maturing debt | at +250 bps | partial / curtailed |
| ICR covenant | tightened to 2.5× | tightened to 2.5× |

Each parameter maps to a mechanism: revenue and margin down together compress
operating cash flow more than either alone (operating leverage in reverse); the
rate rise bites floating-rate and refinancing debt (refinancing risk); rising DSO
and inventory days lengthen the **cash conversion cycle** exactly when cash is
scarce; covenant tightening captures lenders cutting headroom in a downturn. The
scenario is **combined** rather than one-at-a-time because the parameters are
*correlated in the world*: the demand shock that cuts revenue is the same macro
event that widens spreads and slows collections. And nonlinearities (covenant
breach, liquidity exhaustion) only trigger when several stresses coincide.

### The nine-agent ensemble

No single agent holds the whole problem. Nine role-scoped agents, each with one
output that becomes the next's input:

1. **Data-ingestion** — pulls and parses statements, debt schedule, covenants.
2. **Accounting-quality** — strips add-backs, fixes definitional inconsistencies;
   hands *normalized* statements forward.
3. **Feature-engineering** — builds credit features (leverage, coverage,
   liquidity, payment behavior, concentration, cash conversion cycle).
4. **PD-model** — fits and validates a PD model out of sample (the leakage hook
   can reject it).
5. **Stress-scenario** — applies the parameter table, re-derives stressed
   features and PD.
6. **Cash-flow** — projects operating cash flow, liquidity, covenant compliance
   per scenario.
7. **LGD** — values collateral, estimates recovery / LGD / EAD by scenario.
8. **Skeptic** — adversarially reviews every output, demands missing
   sensitivities and benchmarks, returns work upstream or signs off.
9. **Memo-writing** — assembles the validated artifacts into the committee memo.

The graph is mostly a pipeline but with two **feedback edges** that make it a
loop: the skeptic can return control to *any* upstream agent, and a failing hook
bounces an output back to its producer. Seven **skills** freeze the procedures
(financial-statement-normalization, credit-feature-engineering, pd-modeling,
macro-stress-scenario-design, covenant-liquidity-analysis,
lgd-collateral-valuation, credit-memo-writing); the pd-modeling skill writes the
train/test split, leakage check, and out-of-sample validation *into the procedure*
so an agent cannot skip them. Eight **hooks** enforce: no uncited claims, ratios
reconcile, train/test separation, target-leakage check, parameterized scenarios,
skeptic sign-off, end-to-end regeneration, and the "low risk" threshold gate. The
two that matter most are the **leakage check** (the easiest way to a beautiful
backtest is to let the model peek at the answer) and the **"low risk" gate**
(language is a control surface; the phrase must be earned by arithmetic, not
chosen by the writer). Hooks catch violations you can specify in advance; the
skeptic — a Reflexion-style critic — catches the ones you cannot.

### The eleven-iteration narrative

Feedback from the previous iteration drives each one; the numbers evolve as
the analysis improves, which is the point.

1. **Naive memo.** Given only reported profitability and leverage, the memo drafts
   an approval: healthy EBITDA, leverage 3.0×, lookup PD ≈ **1.2%**, "low risk."
2. **Accounting quality intervenes.** Reported EBITDA includes $3m of
   non-recurring add-backs; working capital computed two ways. Normalizing pushes
   true leverage 3.0× → **3.8×**; the whole chain must rerun.
3. **Feature engineering enriches.** Adds payment-delay trends, customer
   concentration (top two = 45% of receivables), a cash conversion cycle crept
   from 70 to 95 days, covenant headroom.
4. **First PD model rejected.** A suspiciously strong fit, PD ≈ 0.9% — the
   **leakage hook fires**: one feature derived from a post-default collections
   field. Rejected before any PD reaches the memo.
5. **Model rebuilt clean.** On leakage-free features with a time-based holdout and
   OOS validation, base PD ≈ **2.5%** — roughly double the naive 1.2% and now
   defensible; a model card records method and validation.
6. **Stress imposed.** Applying the adverse parameter table, stressed PD rises to
   ≈ **9%**.
7. **Cash flow finds the breach.** Base case survives comfortably; under the
   adverse shock, ICR drops below the tightened 2.5× covenant and liquidity falls
   below minimum, peak shortfall ≈ **$6 million**.
8. **LGD worsens recovery.** Specialized illiquid inventory (deep haircut) and
   concentrated receivables stressed by the same shock: base LGD ≈ **40%**,
   stressed ≈ **55%**.
9. **Skeptic pushes back.** Refuses sign-off; demands an alternative macro path,
   peer benchmarking, a recovery-rate sensitivity, and notes severe was never
   tested. Work goes upstream.
10. **Everything reruns under three scenarios.** Severe pushes PD toward **13%**
    and LGD toward **60%**, deepening breach and shortfall; the peer benchmark
    places base PD as slightly worse than median — consistent, not alarming.
11. **Final memo.** Every hook passing and the skeptic satisfied: not a clean
    approval nor a flat decline, but **conditional approval at a reduced $30
    million facility**, tighter ICR covenant, additional collateral, repricing.
    "Low risk" never appears — the gate would have blocked it.

### The compact final result (EAD = $40m)

| Metric | Base case | Stressed (adverse) |
|---|---:|---:|
| Probability of default (PD) | 2.5% | 9.0% |
| Loss given default (LGD) | 40% | 55% |
| Exposure at default (EAD) | $40.0m | $40.0m |
| Expected loss ($) | $0.40m | $1.98m |
| Expected loss (bps of EAD) | 100 bps | 495 bps |
| Covenant breach? | No | Yes (ICR & liquidity) |
| Liquidity shortfall ($) | — | ≈ $6.0m |
| Recommended action | — | Conditional: $30m, tighter covenants, more collateral, repriced |

The arithmetic reconciles by construction:
base $\mathrm{EL} = 0.025 \times 0.40 \times \$40\text{m} = \$0.40\text{m}$
(100 bps); stressed
$\mathrm{EL} = 0.09 \times 0.55 \times \$40\text{m} = \$1.98\text{m}$ (495 bps).
Meridian is sound *in expectation* but fragile *in the tail*: EL nearly
quintuples under a coherent combined shock, and the damage is **structural** (a
covenant breach and a $6m liquidity hole), not merely a higher loss rate. A point
estimate of 1.2% would have hidden all of it. The recommendation is deliberately a
*recommendation, not a decision* — a human credit officer signs the line.

---

## 8. Human Oversight, Accountability, and Audit Trails

The memo ended in a recommendation for a human to sign. What does that signature
add that the loop cannot? Hooks are mechanical guardrails — they answer "did the
artifact pass the checks?" but never "who is *answerable* for it?" In regulated
finance the second question is the one that matters. The loop can manufacture the
analysis but not accountability, nor the legal standing to act on it.

**Human-in-the-loop and escalation.** An autonomous loop suits work with bounded,
reversible consequences. The moment output can move money, bind the institution,
or affect a customer, the loop needs designated points to pause and wait for human
approval. Make **human-review-required** an explicit terminal state alongside
success and failure: the loop writes its state, emits a summary, and yields. An
**escalation trigger** is a predicate evaluated automatically at iteration end —
stated in advance in the goal file, not improvised. Typical triggers: a
recommendation crossing a materiality threshold (e.g. a facility above a $25m
limit), low model confidence or out-of-range inputs, two agents that cannot
reconcile, a hook firing repeatedly on the same issue, or an irreversible action.
A loop that *never* escalates may simply have been given no triggers — it has
quietly assumed nothing it does is consequential.

**Accountability and sign-off.** SR 11-7 governs models through three pillars:
sound development, independent validation, active governance with clear ownership.
Automation dissolves none of them. The worker agents are *developers*; the skeptic
is internal challenge but **not** independent validation (it is implemented by the
same team). Independent validation must sit *outside* the loop. **Sign-off** is an
event with a time, an identity, and a scope — not a property of the artifact — so
the skeptic's approval makes the memo *eligible* for human review but is not
sign-off. Design rule: the artifact carries an explicit **unsigned sign-off
block** only a human can complete; the loop fills everything except the signature.
The loop must never *simulate* sign-off.

**Reproducible audit trails.** The standard is exacting: months later, someone
absent must be able to reconstruct exactly how every number was produced — which
data, code, model version, scenario parameters, and human approvals. Three records
usually suffice: **version control** (every change a commit with author,
timestamp, message), a **structured run log** (each iteration appends which agent
ran, which skill, which hooks fired, the measured state), and **content-addressed
inputs** (data and weights referenced by hash). A run log line like
`iter=04 agent=pd-model skill=pd-modeling hooks=[leakage:FAIL] result=rejected`
can be joined to git so an auditor checks out the exact commit and re-runs the
model. Reproducibility does not mean the analysis is *correct*; it means its
derivation is *fully recoverable and therefore challengeable*. A loop that
produces a defensible recommendation but no reproducible trail has produced only
an assertion.

---

## 9. Failure Modes in Agentic Iteration

Open-ended processes fail in open-ended ways. The unifying message: a failure
caught by an automatic check at iteration's end is a nuisance; the same failure
found weeks later in production is an incident.

- **Infinite loops.** The goal is unsatisfiable or the agent oscillates between
  two states. Cure: a hard iteration budget and cost ceiling as *stopping rules*.
  "Unmet after the budget" is a legitimate, informative outcome.
- **Fake convergence.** The loop declares success (or goes quiet) without the
  success criterion being independently verified. *A quiet loop looks like a
  finished loop.* Warning sign: divergence between the agent's self-report and the
  validator. Remedy: **never let the agent's own "done" end the loop** — condition
  termination on a check the agent does not control.
- **Goal drift.** Over many iterations the objective erodes by small
  reinterpretations: "memo whose stressed EL is below threshold" silently becomes
  "memo that reads as if risk is acceptable." Defense: the **file-based goal**
  re-read each iteration; changes are visible commits, not silent reinterpretation.
- **Premature success.** The agent declares the goal met before it is. Defense: a
  **tolerance hook** that evaluates the real criterion (the "low risk" gate is
  exactly this — it converts a subjective claim into a numeric condition).
- **Goodhart overfitting.** Optimizing a fixed proxy $V$ for an unobserved true
  objective $U$: as optimization pressure rises, the artifacts maximizing $V$
  increasingly *exploit the gap* between $V$ and $U$. Standard pathology of
  metric-driven finance ("teaching to the regulatory metric"). Remedies: diverse
  checks, held-out validation, rotating adversarial review.
- **Excessive delegation.** A nine-agent ensemble to compute a ratio one line of
  code computes exactly is overhead, not sophistication. Each agent adds latency,
  cost, error surface, and coordination burden. Replace agents with functions for
  closed-form work; apply the when-not-to-loop test.

Every remedy is a mechanism introduced earlier — a stopping rule, a file-based
goal, a hook, a validator design choice, a delegation test. **The failure modes
are the predictable consequences of omitting machinery the lecture has already
argued for.** A loop built with explicit goals, external validators, diverse
checks, and honest stopping rules has defended against most of this by
construction.

---

## 10. Practical Design Patterns

Named arrangements of roles and feedback channels, so a designer starts from a
known-good skeleton. They nest and compose.

- **Planner–executor–critic.** Three distinct jobs in three roles: planner
  decomposes and decides next, executor carries out (ReAct), critic evaluates and
  feeds verbal feedback back (Reflexion). Pays off when the right next step
  depends on earlier results; overkill when the step sequence is fixed.
- **Generate–test–revise.** The tightest loop; the workhorse for well-specified,
  machine-checkable goals. Generate → automatic deterministic test → revise using
  the test's diagnostic (Self-Refine) → repeat. Cheap and reliable where it
  applies; only as good as its test — a weak test is the breeding ground for
  Goodhart overfitting.
- **Scaffold–draft–audit–repair.** For subjective, rubric-scored goals. Scaffold
  structure → draft content → audit against a rubric (per-dimension scores +
  findings) → repair until every dimension clears threshold. This is the pattern
  behind *this book* (`/new-topic`, `/draft-chapter`, the audit skills). The audit
  is itself a judgment, so trustworthy-validator and adversarial-review discipline
  matter most here.
- **Data-pipeline: build–validate–document.** For reproducible data work where the
  artifact is a *process* and what must be trustworthy is *lineage*. Build →
  validate (schemas, row counts, reconciliation to source totals) → document
  provenance. The documentation step is a first-class output enforced by a hook.
- **Credit-model: build–stress-test–red-team–finalize.** The Example 2
  generalization for any high-stakes financial model. Build (clean, leakage-free,
  OOS-validated) → stress-test (adverse and severe, not just base) → red-team
  (adversarial critic: challenge assumptions, demand sensitivities, benchmark
  peers) → finalize (governed artifact with an unsigned sign-off block). The
  mandatory stress-test and red-team stages distinguish it: a high-stakes model is
  finished not when it fits well but when it behaves acceptably under worse
  conditions and survives a determined attempt to break its conclusion — the
  design encoding of SR 11-7 governance.

**Choosing a pattern** turns on the goal's properties: is success machine-checkable
or judgment-based, is the output a number or a complex artifact, what are the
stakes, how strong is the reproducibility requirement. In practice one workflow
uses several at once: the credit-model build stage is generate–test–revise over
the PD model, the red-team stage is planner–executor–critic, the data ingestion is
build–validate–document. What never changes is the requirement that the loop's
feedback be **informative**.

---

## 11. Summary and Takeaways

- **Iteration is useful only when feedback is informative.** A loop adds value
  exactly to the degree each iteration's feedback informs the next action. Strip
  the feedback away and a loop is just repetition — same prompt, redone work,
  multiplied cost, no gain. Goals exist so feedback has something to measure
  against; validators so feedback is honest; stopping rules so the loop ends when
  feedback stops being informative. *When a loop disappoints, first diagnose the
  feedback signal — fix it and the loop fixes itself.*
- **Agents specialize the loop; skills reuse it; hooks enforce it.** Agents are
  *who* does the work; skills are *how* recurring work is done the same way twice;
  hooks are *what* the work is never allowed to violate.
- **Complex finance workflows demand explicit goals, real validation, mandatory
  stress testing, and built-in skepticism.** When output can move money or bind an
  institution, good practice becomes a requirement: goals recorded, validation
  independent, stress testing mandatory (a model evaluated only at the base case is
  silent about exactly the conditions under which it matters), and skepticism built
  in (a loop optimizing fixed checks will learn to game them).

The credit-risk arc threaded all of this. A memo that began as a naive read of
profitability was forced by hooks to confront accounting quality and target
leakage, was put under a combined shock, and was challenged by a skeptic until it
produced sensitivities and benchmarks. It ended as a reproducible, stress-tested,
signed-off recommendation a human could defend. *In finance the goal is never to
produce an answer, but to produce an answer someone can stand behind — and that is
achieved not by a better prompt but by a better loop.*

---

## Further Reading

- **Book Chapter 17**, "Loops, Goals, and Iterations: Agents, Skills, and Hooks"
  (`book/chapters/17-loops-goals-iterations/chapter.tex`) — the full treatment,
  with formal definitions (genuine iteration, the goal-directed loop, fake
  convergence, Goodhart degradation), the control-theoretic reading, and the
  complete agent/skill/hook code listings.
- **Book Appendices A–F** — the concrete tooling deferred from this chapter:
  Claude Code, Codex, and Hugging Face (A–B), skills (C), evaluation and human
  gates (D), hooks and `settings.json` registration (E), and Git as the loop's
  memory and rollback path (F).
- Companion notebooks: `code/practicals/17-loops-goals-iterations/`.
- Key references: ReAct (Yao et al., 2022), Reflexion (Shinn et al., 2023),
  Self-Refine (Madaan et al., 2023), AutoGen (Wu et al., 2023), Boehm's spiral
  model (1988), Deming (PDCA), Goodhart (1984), SR 11-7 model-risk guidance.
</content>
