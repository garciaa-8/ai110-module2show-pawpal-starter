# PawPal+ Project Reflection

## 1. System Design

**a. Initial design**

My initial UML included six classes. `Owner` stores the owner's name and pets and provides the entry point for scheduling and event history. `Pet` stores its basic details and care tasks. `Task` describes care work through its name, duration, frequency, and priority. `Scheduler` manages event creation and retrieval. `CareEvent` represents one scheduled occurrence of a task for a pet, with a time and status. `EventStatus` defines scheduled, completed, and skipped states. During implementation I added task completion state to `Task`; the skipped status remains defined, but there is not yet a skip operation.


**b. Design changes**

I made the ownership path explicit during implementation: each `Owner` has a `Scheduler`, and the scheduler's upcoming-event and history methods accept an `Owner` so they can select events associated with that owner's pets. `Owner` delegates event completion to `Scheduler`, which owns the event collection and recurrence logic. I also added `Task.is_completed`; when a recurring event is completed, the scheduler creates a fresh task rather than reusing the completed one. This preserves the completed occurrence while leaving the next task pending.

---

## 2. Scheduling Logic and Tradeoffs

**a. Constraints and priorities**

The scheduler sorts tasks by priority, then duration, then name. It filters tasks by completion state and exact, case-insensitive pet name, and returns upcoming events chronologically. Conflict detection compares event intervals using task durations. Completing a daily or weekly event schedules a new task at the same time on the next day or week. The scheduler does not yet consider an owner's available time or preferences.

**b. Tradeoffs**

Conflict detection currently compares every pair of scheduled events, so its work grows quadratically with the number of events. That approach is simple to explain and test for this small app; for larger schedules, I could sort by start time and avoid checking pairs that cannot overlap. The app warns about conflicts instead of blocking them, since separate people might handle overlapping tasks. This keeps scheduling flexible but leaves the owner responsible for reviewing warnings.

---

## 3. AI Collaboration

**a. How you used AI**

I used the AI coding assistant to compare the UML with the Python classes, draft focused edge-case tests, explain which scheduler method controlled a behavior, and update project documentation. The most effective prompts named a concrete behavior and nearby file, such as asking for tests around events that touch at an end time, or asking how the app could display scheduler conflict warnings. Keeping requests specific made the changes easier to review and verify.

I separated work into design, implementation/testing, and documentation chats. That kept each conversation focused and made it easier to find decisions from a particular phase. I carried forward the relevant files and verified details in the code instead of assuming an earlier chat's summary was still current.

**b. Judgment and verification**

One suggestion I modified was the first UML relationship that implied each task belonged to exactly one pet. The implementation stores tasks in a pet's list and does not give `Task` a pet reference, so the same task object can be added to more than one pet. I adjusted the final UML relationship to match that behavior instead of letting the diagram claim a stricter rule than the code enforces. I checked `Pet.add_task()` and `Scheduler.schedule()` before deciding how to represent it.

I treated AI output as a draft: I checked method names and behavior against the source, ran the focused tests after code changes, and used the CLI output to verify the documented example. Tests and diagnostics caught mismatches more reliably than accepting a plausible explanation on its own.

---

## 4. Testing and Verification

**a. What you tested**

The tests cover task completion and duplicate addition, task filtering, chronological ordering of upcoming events, daily and weekly recurrence, overlapping intervals and non-conflicting touching intervals, conflict warnings, invalid task ownership during scheduling, and attempts to repeat operations on completed or missing events. These tests protect the scheduler's ownership rules and its most important time-boundary behaviors. The CLI example demonstrates task priority sorting, but I still need a direct unit test for the full priority-duration-name ordering.

**b. Confidence**

I am reasonably confident in the behaviors covered by the unit tests, especially recurrence and overlap boundaries. I have less confidence in the full interactive workflow because the Streamlit interface does not yet have end-to-end tests. Next I would add direct tests for `get_tasks()` tie-breaking, event-history ordering and owner isolation, one-time tasks not recurring, and timezone-aware event comparisons. I would also test the UI flow for adding, scheduling, filtering, and displaying a conflict.

---

## 5. Reflection

**a. What went well**

I am most satisfied that the scheduling rules live in `Scheduler` rather than being duplicated across the UI. That gives the rules a clear home and makes them testable without running Streamlit. The tests around recurrence and interval boundaries also helped turn design assumptions into explicit behavior.

**b. What you would improve**

I would add UI actions for completing and rescheduling events, plus a view for event history. I would also add the missing direct task-sort test and broaden validation for time zones and larger event collections. If schedule size became significant, I would revisit the pairwise conflict algorithm.

**c. Key takeaway**

I learned that being the lead architect means setting clear responsibilities and deciding which tradeoffs fit the project, not simply accepting the fastest AI-generated implementation. The assistant can accelerate exploration and drafting, but I remain responsible for checking that the UML, code, tests, and UI describe the same system.
