# Review and pull request

**Time:** 15 minutes  
**Copilot features:** prompt files, Ask mode, Copilot code review on GitHub  
**Starting point:** your branch, or `upstream/checkpoint-3-refactor`

Use Copilot as a security reviewer, then judge its findings like a senior
engineer would: what's real, what's noise, and what did it miss?

## Run a security review (5 minutes)

1. Open `app/main.py`.
2. In Copilot Chat, type `/security-review` and attach `#file:app/main.py`.
3. Run it again for `app/auth.py` and `app/invoices.py`.
4. Sort every finding into a table in `exercises/NOTES.md`:

   | Finding | Real or false positive? | How I confirmed it |
   | --- | --- | --- |

Confirm at least one finding yourself with a real request, for example from
http://localhost:8000/docs or with `curl`. Don't take Copilot's word for it.

## Look for what it missed (2 minutes)

Without Copilot, answer these questions by reading the code:

- Can Ada read Grace's orders? Try it: place an order as Grace, then call
  `GET /orders/{id}` with Ada's token.
- Can you place an order for a negative quantity? What's the total?
- What does `GET /admin/customers` return that it shouldn't?

Did Copilot's review catch these?

## Fix one issue (5 minutes)

Choose one confirmed issue. Good choices for the time available:

- The SQL injection in `GET /products`.
- Missing ownership checks on `GET /orders/{id}`.
- Missing quantity validation on `OrderItem`.

1. In **Ask** mode, ask Copilot to explain the fix and its trade-offs.
2. In **Agent** mode, ask for the fix **and** a test that fails before the fix
   and passes after it.
3. Prove it: temporarily undo the fix and confirm that the test fails.

## Open a pull request (3 minutes)

1. Push your branch to your fork.
2. On GitHub, open a pull request. Set the **base repository** to **your
   fork**, not the original workshop repository.
3. Ask Copilot to draft the description, then edit it. Fill in every section of
   the template yourself, especially **Working with Copilot**.
4. If your organization has Copilot code review enabled, click **Reviewers** and
   request a review from **Copilot**. Compare its comments with your own review.
5. Check that CI passes.

## Checkpoint questions

1. How many of Copilot's findings were real? How many were false positives?
2. What did Copilot miss that you found by reading the code?
3. Would you merge your own PR? What would a reviewer ask you?
