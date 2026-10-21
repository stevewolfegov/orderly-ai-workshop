# Start here

In this workshop, you use GitHub Copilot to learn, test, refactor, and review a
codebase you've never seen. The goal isn't to get Copilot to do the work. The
goal is to stay in control of it: understand what it changes, catch what it gets
wrong, and be able to defend every line you commit.

## The codebase

Orderly is a small order and invoicing API built with FastAPI and SQLite. It
works, mostly. It also has the problems real codebases have: an out-of-date
README, a function that does too much, no real tests, duplicated logic, and
security issues.

## How each exercise works

Every exercise uses the same loop:

1. **Predict.** Read the code and write down what you expect before you ask.
2. **Prompt.** Ask Copilot to explain, plan, or change something.
3. **Verify.** Compare Copilot's answer with your prediction. Read every diff
   before you accept it.

Each exercise ends with **checkpoint questions**. Answer them yourself, in your
own words, in `exercises/NOTES.md`. Bring your answers to the debrief.

## Rules for working with Copilot

- **Use Ask mode before Agent mode.** Understand and plan in Ask mode. Switch to
  Agent mode only when you know what change you want.
- **Keep diffs small.** If Copilot proposes more than about 40 changed lines,
  reject it and ask for a smaller step.
- **Run the tests after every accepted change.**
- **Commit often**, with messages you write yourself.

The file `.github/copilot-instructions.md` tells Copilot to follow these rules
too. You read it in the first exercise.

## Set up

1. Fork this repository to your own GitHub account.
2. In your fork, click the **Actions** tab and enable workflows. GitHub
   disables them on forks by default.
3. Open your fork in one of these ways:
   - **Codespaces (recommended):** Click **Code** > **Codespaces** > **Create
     codespace on main**. Dependencies install automatically.
   - **Locally:** Clone your fork, open it in VS Code, and make sure the GitHub
     Copilot Chat extension is installed and signed in.
4. Open Copilot Chat and confirm that you can switch between **Ask** and
   **Agent** modes.

Don't follow the README's setup steps yet. That's the first exercise.

## Breakout format

You work in pairs. Each of you has your own fork, but you share one screen:

- The **driver** shares their screen and types prompts.
- The **navigator** challenges Copilot's output: "How do we know that's true?",
  "What else did that change touch?"

Switch roles at each new exercise.

## Agenda

| Time | Where | What |
| --- | --- | --- |
| 0:00–0:10 | Main room | Kickoff |
| 0:10–0:40 | Breakout 1 | [Onboarding](01-onboarding.md), then [Test generation](02-tests.md) |
| 0:40–0:50 | Main room | Debrief |
| 0:50–1:20 | Breakout 2 | [Refactoring](03-refactor.md), then [Review and PR](04-review-and-pr.md) |
| 1:20–1:30 | Main room | Debrief and wrap-up |

## If you fall behind

Each exercise starts from a checkpoint branch, so you can catch up at any time:

```sh
git fetch upstream
git checkout -b my-work upstream/checkpoint-2-tests
```

To add the original repository as `upstream`, run
`git remote add upstream <URL of the workshop repository>` once.

See also: [Prompt cheat sheet](prompt-cheatsheet.md).
