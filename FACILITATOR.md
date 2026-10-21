# Facilitator guide

This guide covers running the workshop as a 90-minute Microsoft Teams call with
breakout rooms. The answer key is kept in a separate private repository, so
participants can't see it in their forks.

## Before the workshop

Send this to participants at least two days ahead:

- Confirm you have a GitHub Copilot license, and that you can open Copilot Chat
  in VS Code or in a Codespace.
- Fork the workshop repository and confirm that you can open it in a Codespace,
  or clone it and run `pip install -r requirements.txt` with Python 3.10+.
- Don't read the code ahead of time. The onboarding exercise works best on
  unfamiliar code.

Prepare these yourself:

- [ ] Create the checkpoint branches (see the answer key's
      `make-checkpoints.sh`) and push them to the workshop repository.
- [ ] Pre-assign breakout rooms in pairs. Pair people who don't usually work
      together. If the count is odd, make one group of three.
- [ ] Set breakout rooms to close automatically with a 1-minute warning, or set
      your own timer.
- [ ] Do a dry run of every exercise in a fresh Codespace. Copilot's behavior
      changes between versions.
- [ ] Decide whether Copilot code review is enabled for your organization. If
      not, tell people to skip that step in the review exercise.

## Run of show

| Time | Where | What you do |
| --- | --- | --- |
| 0:00–0:10 | Main room | Kickoff: goals, the predict, prompt, verify loop, and a 3-minute live demo |
| 0:10–0:40 | Breakout 1 | Onboarding (15 min), then test generation (15 min) |
| 0:40–0:50 | Main room | Debrief 1 |
| 0:50–1:20 | Breakout 2 | Refactoring (15 min), then review and PR (15 min) |
| 1:20–1:30 | Main room | Debrief 2 and wrap-up |

### Kickoff (10 minutes)

1. **Frame the goal (2 min).** Copilot writes code fast. Your job today is to
   stay in control: understand the code, check Copilot's work, and own what you
   commit.
2. **Explain the loop (2 min).** Predict, prompt, verify. Show the rules in
   `exercises/00-start-here.md`.
3. **Live demo (3 min).** Share your screen. In Ask mode, ask Copilot a vague
   question about `app/pricing.py`, then a specific one with `#file` and a
   concrete scenario. Point out the difference. Switch to Agent mode and show a
   diff being reviewed before you accept it.
4. **Logistics (3 min).** Pairs, driver and navigator, switch roles per
   exercise. Show where the checkpoint branches are. Open breakout rooms.

### During breakouts

- Visit each room briefly. Ask "What has Copilot gotten wrong so far?" rather
  than "How's it going?"
- Post time warnings in the main chat: halfway through each breakout, and at
  the 15-minute mark when pairs move to the next exercise.
- If a pair is stuck on setup for more than 5 minutes, point them to a
  Codespace.

### Debrief 1 (10 minutes)

Ask two or three pairs to share:

- What was wrong in the README, and did Copilot spot it or repeat it?
- What does Ada pay for 10 Widgets with `SAVE10`? Did predictions match?
- Which test did Copilot get wrong? Which bugs did your tests find?

**Teaching point:** Copilot often derives expected values from the code instead
of the spec, which produces tests that pass on buggy code. Telling it the
source of truth matters.

### Debrief 2 and wrap-up (10 minutes)

Ask:

- What did you reject during the refactor, and why?
- Who found the duplicated tax table? What did it cost New York customers?
- How many of Copilot's security findings were real? What did it miss?

Close with three takeaways:

1. Give Copilot context and a source of truth.
2. Plan first, then make small, reviewable changes.
3. You're accountable for every line you commit, whoever wrote it.

Ask everyone to share a link to their PR in the meeting chat.

## If you're running short on time

- Make the stretch goals optional and skip them in debriefs.
- Run the review exercise as a live demo during debrief 2 instead of in a
  breakout.
- Point pairs to the checkpoint branches early, so everyone starts each
  exercise from the same place.
