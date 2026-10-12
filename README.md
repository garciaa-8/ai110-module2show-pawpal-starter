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
# Run the full test suite:
pytest

# Run with coverage:
pytest --cov
```

Sample test output:

```
# Paste your pytest output here
```

## 📐 Smarter Scheduling

| Feature | Method(s) | Notes |
|---------|-----------|-------|
| Task sorting | `Scheduler.get_tasks(owner)` | Sorts by priority (high to low), then duration and task name. |
| Event time sorting | `Scheduler.get_upcoming_events(owner)` | Returns future scheduled events in chronological order. |
| Filtering | `Scheduler.filter_tasks(owner, completed, pet_name)` | Optional completion and exact, case-insensitive pet-name filters; when both are provided, both must match. `Scheduler.get_tasks(owner, include_completed=False)` can also exclude completed tasks. |
| Conflict detection | `Scheduler.find_conflicts()`, `Scheduler.get_conflict_warning(event)` | Checks overlapping scheduled-event intervals using task durations. Touching end/start times are not conflicts. The app warns but does not block scheduling. |
| Recurring tasks | `Scheduler.complete_event(event_id)` | Completing a daily or weekly event creates a fresh task and schedules its next event one day or one week later at the same time. Other frequencies do not repeat. |

## 📸 Demo Walkthrough

Describe your app in numbered steps so a reader can follow along without watching a video:

1. <!-- Describe this step -->
2. <!-- Describe this step -->
3. <!-- Describe this step -->
4. <!-- Describe this step -->
5. <!-- Add more steps as needed -->

**Screenshot or video** *(optional)*: <!-- Insert a screenshot or link to a demo video here -->
