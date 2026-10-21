# Onboarding and code understanding

**Time:** 15 minutes  
**Copilot features:** Ask mode, `#codebase`, `#file`, `/explain`, prompt files  
**Starting point:** `main`

You've joined the Orderly team. Get the app running, then build a mental model
of how it prices an order.

## Read the guardrails (1 minute)

Open `.github/copilot-instructions.md`. Copilot reads this file with every
request in this repository.

- What does it tell Copilot to do before editing a file?
- Why might a team want these rules outside a workshop?

## Get the app running (5 minutes)

1. In **Ask** mode, send this prompt:

   ```text
   #codebase How do I install, seed, and run this project locally? Cite the
   files you used.
   ```

2. Compare Copilot's answer with the **Getting started** section of
   `README.md`. Did Copilot repeat the README, or did it read the code?
3. Follow the steps until you can open http://localhost:8000/docs and get a
   successful response from `GET /products`.
4. Place an order with `POST /orders`. You need a valid API token.

> **Tip:** The README is wrong in at least three places. When something fails,
> paste the error into Copilot Chat and ask why. Then check its answer against
> the code.

When it's working, fix the README's **Getting started** section and commit:

```sh
git commit -am "Fix README setup instructions"
```

## Understand the pricing engine (7 minutes)

Open `app/pricing.py`. Before you ask Copilot anything, spend two minutes
reading `calculate_order_total` and write down your answer to this question:

> Ada (standard tier, California) quotes 10 Widgets with promo code `SAVE10`.
> What are the subtotal, discount, shipping, tax, and total?

Now check your answer:

1. Run the prompt file: type `/explain-flow` in Copilot Chat and describe the
   order above.
2. Compare Copilot's trace with your prediction. Where did you differ? Who was
   right?
3. Confirm with a real request to `POST /quote`.

Try a weaker prompt and compare the result:

```text
explain pricing.py
```

What did the specific prompt get you that the vague one didn't?

## Write it down (2 minutes)

Ask Copilot to draft a short `docs/ARCHITECTURE.md`: modules, request flow, and
where the data lives. Read it critically. Correct at least one statement that's
wrong, vague, or missing, then commit it.

## Checkpoint questions

Answer these in `exercises/NOTES.md`:

1. What were the three problems in the README's setup steps?
2. What does Ada pay for 10 Widgets with `SAVE10`? Did your prediction match?
3. Name one thing Copilot told you that turned out to be wrong or incomplete.

## Stretch goal

Ask Copilot which parts of the codebase disagree with `docs/PRICING_RULES.md`.
Don't fix anything. Keep the list for the next exercise.
