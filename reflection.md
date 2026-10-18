# PawPal+ Project Reflection

## 1. System Design

**a. Initial design**

- Briefly describe your initial UML design.
    - My initial design had four classes: Task, Pet, Owner, and Scheduler. An Owner has many Pets, and each Pet has many Tasks. The Scheduler holds a reference to the Owner and gets every task through the Owner, so it can work across all pets instead of just one.
- What classes did you include, and what responsibilities did you assign to each?
    - Task: represents one care activity (like a walk or feeding). It stores the title, duration, priority, time, frequency, and whether it’s completed.
    - Pet: stores a pet’s name and species and holds that pet’s list of tasks.
    - Owner: stores the owner’s name and available time, manages multiple pets, and can return all tasks across every pet.
    - Scheduler: the “brain.” It sorts and filters tasks and builds the daily plan, using the Owner to get the data.
- The three core actions a user should be able to perform are: (1) add a pet, (2) schedule a care task for a pet, and (3) view today’s tasks in sorted order.

**b. Design changes**

- Did your design change during implementation?
- If yes, describe at least one change and why you made it.
    - Yes. After I built the class skeleton, I asked my AI assistant to review it for missing relationships and bottlenecks. It pointed out that a Task didn’t know which pet it belonged to, so the Scheduler and UI couldn’t show whose task was whose. I added a pet_name field to Task to fix this. I also added a due_date to Task, since recurring tasks need a date to calculate the next occurrence. I added detect_conflicts() and mark_task_complete() to the Scheduler because the project requires conflict warnings and recurring tasks. The AI also suggested adding remove_pet() and remove_task(), but I decided not to add them because they were not required and I wanted to keep the design simple.

---

## 2. Scheduling Logic and Tradeoffs

**a. Constraints and priorities**

- What constraints does your scheduler consider (for example: time, priority, preferences)?
    - It considers the owner's available minutes, each task's priority (high, medium, low), each task's duration, and whether the task is already completed. Tasks are shown in time order.
- How did you decide which constraints mattered most?
    - I decided that the owner's available time is a hard limit, and priority comes next, so important tasks like medicine are scheduled before optional ones like play time. Among tasks with equal priority, shorter ones go first so more tasks fit.

**b. Tradeoffs**

- Describe one tradeoff your scheduler makes.
- Why is that tradeoff reasonable for this scenario?

---

## 3. AI Collaboration

**a. How you used AI**

- How did you use AI tools during this project (for example: design brainstorming, debugging, refactoring)?
    - I used my AI assistant to draft the UML diagram, generate the class skeleton, and review that skeleton for missing relationships and bottlenecks. In Phase 2 I used it to help fill in the core methods and write the demo script and tests.

- What kinds of prompts or questions were most helpful?
    - The most helpful prompt was asking it to review my skeleton and list problems without changing the file. That gave me a list to decide on instead of code I hadn't asked for.

**b. Judgment and verification**

- Describe one moment where you did not accept an AI suggestion as-is.
    - The AI suggested adding `remove_pet()` and `remove_task()` and storing the generated schedule on the Scheduler. I rejected both because the required features don't need them, and I wanted to keep the design simple. I accepted its suggestions to link each task to its pet and to sort priority using numbers instead of text.

- How did you evaluate or verify what the AI suggested?
    - I ran `main.py` and checked that the schedule printed in the right order with the right totals. I also ran pytest, and both tests passed.
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
