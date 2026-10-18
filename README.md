# PawPal+ 🐾

PawPal+ is a Streamlit app that helps a busy pet owner plan daily care for their pets. It tracks tasks like walks, feeding, and medicine for multiple pets, builds a daily plan that fits the owner's available time, warns about time conflicts, and automatically repeats daily and weekly tasks.

## Features

- **Multiple pets, one owner:** an `Owner` manages several `Pet`s, each with its own tasks.
- **Sorting by time:** tasks are shown in chronological order (`Scheduler.sort_by_time()`).
- **Filtering:** view tasks by pet or by pending/completed status (`filter_by_pet()`, `filter_by_status()`).
- **Priority-based daily plan:** pending tasks are chosen by priority, then shortest first, until the owner's available minutes run out (`generate_schedule()`), with a plain-language explanation (`explain_plan()`).
- **Conflict warnings:** tasks scheduled at the same date and time produce a warning instead of an error (`detect_conflicts()`).
- **Recurring tasks:** completing a daily or weekly task creates the next occurrence automatically (`mark_task_complete()`).

## Getting Started

```bash
python3 -m venv .venv
source .venv/bin/activate        # Windows: .\.venv\Scripts\Activate.ps1
pip install -r requirements.txt

streamlit run app.py             # launch the web app
python main.py                   # run the command-line demo
python -m pytest                 # run the tests
```

## Demo Walkthrough

1. **Set up the owner.** Enter your name and how many minutes you have available today.
2. **Add pets.** Enter a name and species and click *Add pet*. Each pet appears in the list and stays there while you use the app.
3. **Add tasks.** Choose a pet, then enter a title, duration, priority, time, and whether the task repeats (once, daily, weekly).
4. **Watch for conflicts.** If two pending tasks share the same time, a yellow warning names both tasks and suggests moving one.
5. **Complete a task.** Pick a pending task and click *Mark complete*. If it repeats, the app tells you the date of the next occurrence.
6. **Review your tasks.** The task table is sorted by time and can be filtered by pet and by status.
7. **Generate the schedule.** Click *Generate schedule* to see today's plan in time order, plus an explanation of how many tasks fit within your available time.

Key scheduler behaviors shown in the command-line demo (`python main.py`):

```
Conflict check:
  WARNING: Conflict at 08:00 on 2026-10-18: Rex: Give medicine, Luna: Feed breakfast

Completing 'Morning walk' (repeats daily)...
  New task created for 2026-10-19: Morning walk
```

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

## Implementation Summary

PawPal+ is built from four classes in `pawpal_system.py`. A `Task` is one care activity (title, duration, priority, time, frequency, completion status, due date, and the name of its pet). A `Pet` holds its own tasks, and an `Owner` holds multiple pets and exposes `get_all_tasks()`, which returns every pet's tasks together. The `Scheduler` reads all tasks through that Owner method, so it works across every pet. `main.py` is a command-line demo that verifies the logic, and `app.py` is the Streamlit interface that calls the same methods. The Owner is stored in `st.session_state` so data persists between clicks.

## 📐 Smarter Scheduling

| Feature | Method(s) | Notes |
|---------|-----------|-------|
| Task sorting | `Scheduler.sort_by_time()` | Sorts all tasks by zero-padded "HH:MM" time; untimed tasks go last |
| Filtering | `Scheduler.filter_by_status()`, `Scheduler.filter_by_pet()` | Filter by completed/pending, or by pet name |
| Conflict handling | `Scheduler.detect_conflicts()` | Returns warning messages when pending tasks share the same date and time; it never crashes |
| Recurring tasks | `Scheduler.mark_task_complete()` | Completing a daily or weekly task creates the next one (+1 day or +7 days) using `timedelta` |
| Schedule building | `Scheduler.generate_schedule()` | Picks pending tasks due today by priority, then shortest first, until available time runs out |

## 🧪 Testing PawPal+

Run the full test suite:

```bash
python -m pytest
```

The tests cover:

- **Task basics:** completing a task and adding a task to a pet
- **Sorting:** tasks come back in chronological order, with untimed tasks last
- **Recurrence:** completing a daily task creates one due tomorrow, a weekly task is due in 7 days, and a one-time task creates nothing
- **Conflict detection:** duplicate times are flagged, different times are not, and completed tasks are ignored
- **Filtering and edge cases:** filter by pet and by status, an owner with no pets, and a schedule that respects available time and priority

Sample test output:

```
============================================= test session starts ==============================================
platform darwin -- Python 3.13.2, pytest-9.1.1, pluggy-1.7.0
rootdir: /Volumes/G7XPHOTOS/Projects/AI 110/homeworks/ai110-module2show-pawpal-starter
collected 14 items

tests/test_pawpal.py ..............                                                                      [100%]

============================================== 14 passed in 0.15s ==============================================
```

**Confidence level:** ⭐⭐⭐⭐ (4/5). The core scheduling behaviors pass their tests. I'd test overlapping task durations and invalid input next.

## Project Structure

```
pawpal_system.py      # Task, Pet, Owner, Scheduler (logic layer)
main.py               # CLI demo
app.py                # Streamlit UI
tests/test_pawpal.py  # pytest suite
diagrams/uml_draft.mmd, uml_final.mmd   # Mermaid class diagrams
reflection.md         # design and AI collaboration reflection
```