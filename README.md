# PawPal+ (Module 2 Project)

You are building **PawPal+**, a Streamlit app that helps a pet owner plan care tasks for their pet.

## Scenario

A busy pet owner needs help staying consistent with pet care. They want an assistant that can:

- Track pet care tasks (walks, feeding, meds, enrichment, grooming, etc.)
- Consider constraints (time available, priority, owner preferences)
- Produce a daily plan and explain why it chose that plan

Your job is to design the system first (UML), then implement the logic in Python, then connect it to the Streamlit UI.

## What you will build

Your final app should:

- Let a user enter basic owner + pet info
- Let a user add/edit tasks (duration + priority at minimum)
- Generate a daily schedule/plan based on constraints and priorities
- Display the plan clearly (and ideally explain the reasoning)
- Include tests for the most important scheduling behaviors

## Getting started

### Setup

```bash
python -m venv .venv
source .venv/bin/activate  # Windows: .venv\Scripts\activate
pip install -r requirements.txt
```

### Suggested workflow

1. Read the scenario carefully and identify requirements and edge cases.
2. Draft a UML diagram (classes, attributes, methods, relationships).
3. Convert UML into Python class stubs (no logic yet).
4. Implement scheduling logic in small increments.
5. Add tests to verify key behaviors.
6. Connect your logic to the Streamlit UI in `app.py`.
7. Refine UML so it matches what you actually built.

## 🖥️ Sample Output

Output from running `python main.py`:

```
Today's Schedule
Time   Pet      Task                Min  Priority  Due
--------------------------------------------------------------
07:30  Rex      Morning walk        30   high      2026-10-18
08:00  Rex      Give medicine       5    high      2026-10-18
08:00  Luna     Feed breakfast      10   medium    2026-10-18
18:00  Rex      Play time           20   low       2026-10-18

Scheduled 4 of 4 pending tasks (65/90 minutes). Higher-priority tasks are chosen first, then shorter ones, until the owner's time runs out.

All tasks sorted by time
Time   Pet      Task                Min  Priority  Due
--------------------------------------------------------------
07:30  Rex      Morning walk        30   high      2026-10-18
08:00  Rex      Give medicine       5    high      2026-10-18
08:00  Luna     Feed breakfast      10   medium    2026-10-18
18:00  Rex      Play time           20   low       2026-10-18

Filter: Rex's tasks only
Time   Pet      Task                Min  Priority  Due
--------------------------------------------------------------
18:00  Rex      Play time           20   low       2026-10-18
07:30  Rex      Morning walk        30   high      2026-10-18
08:00  Rex      Give medicine       5    high      2026-10-18

Conflict check:
  WARNING: Conflict at 08:00 on 2026-10-18: Rex: Give medicine, Luna: Feed breakfast

Completing 'Morning walk' (repeats daily)...
  New task created for 2026-10-19: Morning walk

Filter: completed tasks
Time   Pet      Task                Min  Priority  Due
--------------------------------------------------------------
07:30  Rex      Morning walk        30   high      2026-10-18

Filter: pending tasks
Time   Pet      Task                Min  Priority  Due
--------------------------------------------------------------
18:00  Rex      Play time           20   low       2026-10-18
08:00  Rex      Give medicine       5    high      2026-10-18
07:30  Rex      Morning walk        30   high      2026-10-19
08:00  Luna     Feed breakfast      10   medium    2026-10-18
```

## 🧪 Testing PawPal+

```bash
# Run the full test suite:
python -m pytest


# Run with coverage:
pytest --cov
```
The tests cover:
- **Task basics:** completing a task and adding a task to a pet
- **Sorting:** tasks come back in chronological order, with untimed tasks last
- **Recurrence:** completing a daily task creates one due tomorrow, a weekly task is due in 7 days, and a one-time task creates nothing
- **Conflict detection:** duplicate times are flagged, different times are not, and completed tasks are ignored
- **Filtering and edge cases:** filter by pet and by status, an owner with no pets, and a schedule that respects available time and priority

```
# Paste your pytest output here
Sample test output:
============================================= test session starts ==============================================
platform darwin -- Python 3.13.2, pytest-9.1.1, pluggy-1.7.0
rootdir: /Volumes/G7XPHOTOS/Projects/AI 110/homeworks/ai110-module2show-pawpal-starter
collected 14 items                                                                                             

tests/test_pawpal.py ..............                                                                      [100%]

============================================== 14 passed in 0.15s ============================================
```
**Confidence level:** ⭐⭐⭐⭐ (4/5). The core scheduling behaviors pass their tests. I'd test overlapping task durations and invalid input next.

## 📐 Smarter Scheduling

> Fill in once you've implemented scheduling logic.

## 📐 Smarter Scheduling

| Feature | Method(s) | Notes |
|---------|-----------|-------|
| Task sorting | `Scheduler.sort_by_time()` | Sorts all tasks by zero-padded "HH:MM" time; untimed tasks go last |
| Filtering | `Scheduler.filter_by_status()`, `Scheduler.filter_by_pet()` | Filter by completed/pending, or by pet name |
| Conflict handling | `Scheduler.detect_conflicts()` | Returns warning messages when pending tasks share the same date and time; it never crashes |
| Recurring tasks | `Scheduler.mark_task_complete()` | Completing a daily or weekly task creates the next one (today + 1 day or + 7 days) using `timedelta` |
| Schedule building | `Scheduler.generate_schedule()` | Picks pending tasks due today by priority, then shortest first, until available time runs out |

## 📸 Demo Walkthrough

Describe your app in numbered steps so a reader can follow along without watching a video:

1. <!-- Describe this step -->
2. <!-- Describe this step -->
3. <!-- Describe this step -->
4. <!-- Describe this step -->
5. <!-- Add more steps as needed -->

**Screenshot or video** *(optional)*: <!-- Insert a screenshot or link to a demo video here -->
