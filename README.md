# PawPal+ (Module 2 Project)

You are building **PawPal+**, a Streamlit app that helps a pet owner plan care tasks for their pet.

## Scenario

A busy pet owner needs help staying consistent with pet care. They want an assistant that can:

- Track pet care tasks (walks, feeding, meds, enrichment, grooming, etc.)
- Consider constraints (time available, priority, owner preferences)
- Produce a daily plan and explain why it chose that plan

Your job is to design the system first (UML), then implement the logic in Python, then connect it to the Streamlit UI.

## Testing PawPal+

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
source .venv/bin/activate  
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

Paste a sample of your app's CLI or Streamlit output here so a reader can see what a generated plan looks like:

```
# e.g.:
# Daily plan for Biscuit (Golden Retriever):
#   08:00 — Morning walk (30 min) [priority: high]
#   09:00 — Feeding (10 min) [priority: high]
#   ...
```
Today's Schedule - Sunday, October 11, 2026
08:00 AM - Morning walk for Bailey (30 min)
12:00 PM - Breakfast for Miso (10 min)
06:00 PM - Medication for Bailey (5 min)
## 🧪 Testing PawPal+

```bash
python -m pytest
```

The tests cover task completion and addition, task filtering and sorting, chronological event ordering, daily and weekly recurrence, schedule conflicts, and edge cases such as invalid scheduling and repeated event completion.

Sample test output:

```
platform darwin -- Python 3.9.6, pytest-8.4.2, pluggy-1.6.0
rootdir: /Users/albert_garcia7/ai110-module2show-pawpal-starter
collected 13 items                                                                                                                               

tests/test_pawpal.py .............                                                                                                         [100%]

=============================================================== 13 passed in 0.01s ===============================================================   
```
Confidence LEvel of Reliabilty: 4 Stars 

## Features

- **Priority-based task sorting:** `Scheduler.get_tasks()` orders tasks by priority (high, medium, then low), then shorter duration, then task name. Unrecognized priorities sort after the known levels.
- **Task filters:** Filter by completion status, pet name, or both. Pet-name matching is exact and case-insensitive; when both filters are set, a task must match both. The app displays matching tasks in scheduler sort order.
- **Chronological upcoming schedule:** `Scheduler.get_upcoming_events()` returns only future, scheduled events belonging to the owner, sorted by date and time.
- **Schedule conflict warnings:** `Scheduler.find_conflicts()` detects overlapping event intervals using task durations. Events that touch at an end time do not conflict. The app displays warnings without blocking scheduling.
- **Daily and weekly recurrence:** Completing a daily or weekly event creates a fresh, incomplete task for the same pet and schedules it at the same time the next day or week. Other frequencies do not repeat.
- **Scheduling and event validation:** A task must belong to the selected pet, and that pet must belong to the owner. Completed events cannot be completed or rescheduled again.

## Demo Walkthrough

Run the interface with `streamlit run app.py`, or run the CLI example with `python main.py`.

1. Enter an owner name, then add a pet with its name, species, and birth date. The Pets table shows each pet and its task count.
2. Schedule care by selecting a pet and entering the task name, description, duration, frequency, priority, and a future date and time. The app confirms a successful schedule or displays a conflict warning.
3. Use the Care tasks filters to view tasks for one pet or all pets, and to show pending, completed, or all tasks. Results follow the Scheduler's priority, duration, and name ordering.
4. Review the Upcoming schedule, which lists future events chronologically and includes conflict warnings. Overlapping event durations trigger warnings; events that only touch at an end time do not.

The Scheduler also supports daily and weekly recurrence when an event is completed, creating a fresh task and scheduling it for the next interval. Event completion is currently available through the Python API, not as a control in the Streamlit interface.

Sample output from `main.py` (the date is calculated at runtime):

```text
$ python main.py
Tasks sorted by priority, duration, and name:
- High: Medication (5 min)
- High: Breakfast (10 min)
- Medium: Morning walk (30 min)

Upcoming schedule for Monday, October 12, 2026:
- 08:00 AM: Morning walk for Bailey
- 08:00 AM: Breakfast for Miso
- 06:00 PM: Medication for Bailey
WARNING: Schedule conflict: Breakfast for Miso overlaps with Morning walk for Bailey.

Completed tasks:
- Medication

Tasks for Bailey:
- Medication (high)
- Morning walk (medium)
- Medication (high)
```
