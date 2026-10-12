# PawPal+ Project Reflection

## 1. System Design
-schedule events
-check off events 
-see event history 

**a. Initial design**
- Briefly describe your initial UML design.
- What classes did you include, and what responsibilities did you assign to each?

-Owner represents the person using PawPal+. An owner can have multiple pets and can request scheduling, completion, or event history.
Pet belongs to an owner and has care tasks, such as feeding or medication.
-Task defines the reusable care activity, including its name, duration, frequency, and priority.
-Scheduler manages care events and provides operations for scheduling, rescheduling, and retrieving upcoming events or history.
-CareEvent is one dated occurrence of a task for a specific pet. Its status and timestamps let the app record whether it was scheduled, completed, or skipped.
-EventStatus enumerates those three event states.


**b. Design changes**

- Did your design change during implementation?
- If yes, describe at least one change and why you made it.

During implementation, I clarified how event history is linked to an owner. I added a Scheduler reference to Owner and changed the Scheduler's upcoming-event and history methods to accept an Owner, so they can use that owner's pets to identify the right events. I also added a Scheduler completion method so Owner can delegate event completion to the same class that manages scheduled events. This makes the ownership and responsibility links explicit while keeping individual event records connected to their pet and task.

---

## 2. Scheduling Logic and Tradeoffs

**a. Constraints and priorities**

The scheduler sorts tasks by priority first, then by duration and name, so high-priority care appears first. It also compares scheduled event time intervals using each task's duration to find overlaps, and creates the next occurrence for daily and weekly tasks when an event is completed. It does not yet account for an owner's available time or preferences. The conflict check currently compares every pair of scheduled events, which is easy to understand but takes quadratic time as the schedule grows. For better performance on larger schedules, I could sort events by start time and skip later events once they start after the current event ends; this avoids many unnecessary comparisons when events rarely overlap, while keeping the current simple approach for a small schedule.

**b. Tradeoffs**

The scheduler warns about overlapping events but does not block them. This keeps scheduling flexible, especially when overlapping care tasks can be handled by different people, but it means the owner must review and resolve the warning. For this small app, a clear warning is less disruptive than rejecting a schedule automatically.

---

## 3. AI Collaboration

**a. How you used AI**

- How did you use AI tools during this project (for example: design brainstorming, debugging, refactoring)?
- What kinds of prompts or questions were most helpful?

**b. Judgment and verification**

- Describe one moment where you did not accept an AI suggestion as-is.
- How did you evaluate or verify what the AI suggested?

---

## 4. Testing and Verification

**a. What you tested**

- What behaviors did you test?
- Why were these tests important?

**b. Confidence**

- How confident are you that your scheduler works correctly?
- What edge cases would you test next if you had more time?

---

## 5. Reflection

**a. What went well**

- What part of this project are you most satisfied with?

**b. What you would improve**

- If you had another iteration, what would you improve or redesign?

**c. Key takeaway**

- What is one important thing you learned about designing systems or working with AI on this project?
