# Prompt cheat sheet

## Principles

- **Give context.** Attach files with `#file:` or search the project with
  `#codebase`. Copilot can't use what it can't see.
- **State the goal and the constraints.** Say what you want, what you don't
  want, and what "done" looks like.
- **Ask for a plan before code.** Review the plan, then ask for one step at a
  time.
- **Ask for evidence.** "Cite file and line" makes errors easier to spot.
- **Name the source of truth.** For example, "Derive expected values from
  `docs/PRICING_RULES.md`, not from the code."

## Weak and strong prompts

| Task | Weak | Strong |
| --- | --- | --- |
| Understand code | `explain this` | `#file:app/pricing.py Walk through calculate_order_total for a gold customer in NY ordering one Docking Hub. Show the value of each variable as it changes.` |
| Set up a project | `how do I run this` | `#codebase How do I install, seed, and run this project? Cite the files you used, and flag anything in the README that disagrees with the code.` |
| Generate tests | `/tests` | `Write pytest tests for the bulk discount rule in docs/PRICING_RULES.md. Use the seeded_db fixture. Include the boundary at quantity 9 and 10. One behavior per test.` |
| Refactor | `clean up this function` | `Extract the shipping calculation from calculate_order_total into a function named shipping_cost. Don't change behavior or touch anything else.` |
| Review | `any bugs?` | `Review #file:app/main.py for OWASP Top 10 issues. For each finding, give the line, an example exploit, severity, and your confidence.` |
| Fix | `fix it` | `Fix the SQL injection in list_products using a parameterized query. Then write a test that sends a malicious q value and fails without the fix.` |

## Useful Copilot Chat features

| Feature | Use it to |
| --- | --- |
| **Ask** mode | Ask questions and get plans without changing files. |
| **Agent** mode | Let Copilot edit files and run commands. Review every change. |
| `#file:path` | Attach a specific file as context. |
| `#codebase` | Let Copilot search the whole repository. |
| `#selection` | Ask about the code you've highlighted. |
| `/explain` | Explain the selected code. |
| `/tests` | Generate tests for the selected code. |
| `/fix` | Propose a fix for a problem in the selected code. |
| `/explain-flow`, `/security-review` | Run this repository's reusable prompt files from `.github/prompts/`. |
| Inline chat (Ctrl+I or Cmd+I) | Make a small, local edit in the editor. |

## When Copilot goes off track

- **It changed too much:** Reject the change and ask again with "only" and
  "don't touch anything else."
- **It's confidently wrong:** Ask it to cite the file and line, then check them.
- **It's going in circles:** Start a new chat. Long conversations accumulate
  wrong assumptions.
- **It fixed something you didn't ask about:** Undo it. Unrequested changes are
  how bugs get into a refactor.
