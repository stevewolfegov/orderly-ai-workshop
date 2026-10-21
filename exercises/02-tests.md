# Test generation

**Time:** 15 minutes  
**Copilot features:** Ask mode, Agent mode, `/tests`, `#file`  
**Starting point:** your branch from the previous exercise, or `main`

Before anyone touches the pricing engine, you need tests that lock in how it
should behave. These tests are your safety net for the refactoring exercise.

## Plan before you generate (4 minutes)

In **Ask** mode:

```text
#file:app/pricing.py #file:docs/PRICING_RULES.md
List the edge cases I should test for calculate_order_total, based on the
pricing rules. Don't write any code yet. Group them by rule.
```

Review the list. Choose **six** cases to test. Include at least one boundary
case, such as an amount exactly at a threshold.

## Generate the tests (6 minutes)

Switch to **Agent** mode and ask for the tests you chose, with constraints:

```text
Create tests/test_pricing.py with tests for these cases: <your six cases>.
- Use pytest and the seeded_db fixture from tests/conftest.py. Don't mock the database.
- Call calculate_order_total directly.
- Use the demo customers and products from app/seed.py.
- Derive expected values from docs/PRICING_RULES.md, not from the current code.
- One behavior per test, with a descriptive test name.
```

Before you accept the change, read every test. For each one, ask yourself:
*Where did this expected value come from?*

Run the tests:

```sh
pytest -v
```

## Investigate the failures (5 minutes)

If your tests are good, at least one of them fails. For each failure, decide:

- **Is the test wrong?** Copilot calculated the expected value incorrectly.
- **Is the code wrong?** The code disagrees with `docs/PRICING_RULES.md`.

Work it out by hand from the rules document before you ask Copilot.

Don't fix the code yet. Mark each confirmed bug so the suite stays green while
you refactor:

```python
@pytest.mark.xfail(reason="Bug: <one-line description>", strict=True)
```

Commit your tests.

## Checkpoint questions

1. Which test did Copilot get wrong, and how did you know?
2. Which generated test, if any, was useless? For example, a test that can
   never fail, or one that only restates the code.
3. What bugs did your tests find? Quote the rule each one breaks.

## Stretch goal

Ask Copilot for tests of the `POST /orders` endpoint using the `client`
fixture. What happens if you send a quantity of `-2`? Is that covered by the
pricing rules?
