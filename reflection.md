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

- What constraints does your scheduler consider (for example: time, priority, preferences)?
- How did you decide which constraints mattered most?

**b. Tradeoffs**

- Describe one tradeoff your scheduler makes.
- Why is that tradeoff reasonable for this scenario?

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
