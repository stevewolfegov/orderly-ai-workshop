# Refactoring

**Time:** 15 minutes  
**Copilot features:** Ask mode, Agent mode, inline chat, reviewing diffs  
**Starting point:** your branch, or `upstream/checkpoint-2-tests`

`calculate_order_total` does everything: it queries the database, applies five
kinds of discounts, calculates shipping, and hard-codes tax rates. Break it up
safely, one step at a time, with your tests running after each step.

## Get a plan, then push back (4 minutes)

In **Ask** mode:

```text
#file:app/pricing.py Propose a step-by-step plan to refactor
calculate_order_total into smaller functions. Each step must keep behavior
identical and be small enough to review in under a minute. Don't write code yet.
```

Before you accept the plan, challenge it:

- Does any step change behavior?
- Is any step too large?
- Copilot's plan probably doesn't mention the tax rates in `app/config.py`,
  `app/orders.py`, and `app/invoices.py`. Search for `0.0725` across the project.
  How many copies of the tax table are there? Do they agree?

## Refactor in small steps (8 minutes)

For each step in the plan:

1. Ask Copilot, in **Agent** mode, to do **only that step**.
2. Read the diff. Reject it if it's larger than you expected or touches
   anything else.
3. Run `pytest`. Every test that passed before must still pass.
4. Commit with your own message.

Good first steps:

- Replace the `if`/`elif` tax chain with a lookup in `config.TAX_RATES`.
- Extract the shipping calculation into its own function.
- Replace magic numbers such as `0.05`, `500`, and `75` with named constants.

> **Watch for:** Copilot "helpfully" fixing a bug in the middle of a refactor.
> That's a behavior change, and your `xfail` tests will report it as an
> unexpected pass. If it happens, undo the change and ask for the step again.

## Fix the bugs separately (3 minutes)

Now fix the bugs your tests found, in a **separate commit** from the refactor.
Remove each `xfail` marker as you fix its bug, and confirm the test passes.

## Checkpoint questions

1. Name one change Copilot proposed that you rejected or modified, and why.
2. How many copies of the tax table did you find? Which one was wrong, and what
   does that bug cost a New York customer?
3. Why keep the refactor and the bug fix in separate commits?

## Stretch goal

Make `app/invoices.py` follow the last rule in `docs/PRICING_RULES.md`: an
invoice shows the stored order amounts and never recalculates them.
