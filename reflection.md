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
    - My conflict detection only checks for exact matching start times. It doesn't check whether a 30-minute task starting at 08:00 overlaps with a task starting at 08:15.
- Why is that tradeoff reasonable for this scenario?
    - Exact matching is simple, easy to read, and easy to test, and it catches the most obvious mistake of double-booking a time. Overlap checking would need start and end times for every task. For a basic pet-care planner, a warning that never crashes is more useful than a perfect calendar.

---

## 3. AI Collaboration

**a. How you used AI**

- How did you use AI tools during this project (for example: design brainstorming, debugging, refactoring)?
    - I used AI at every phase. I used it to draft the UML diagram, generate the class skeleton, and review that skeleton for missing relationships and bottlenecks. Later I used it to help implement the scheduling logic (sorting, filtering, recurring tasks, conflict detection), draft the pytest suite, connect the Streamlit UI with `st.session_state`, and debug problems like pytest not being installed in my virtual environment. I used an AI coding assistant inside VS Code and a separate chat assistant for step-by-step guidance, since I'm new to Git, Python environments, and Streamlit.
- What kinds of prompts or questions were most helpful?
    - The most helpful prompts were specific and set a limit, like asking the AI to review my skeleton and list problems without changing the file, or asking for conflict detection that returns a warning instead of crashing. Those gave me options to judge instead of code I hadn't asked for. Pasting my actual error messages and terminal output also got much better answers than describing the problem in words.
- Which AI coding assistant features were most effective for building your scheduler?
    - Chat was the most useful, because I could ask questions about my code and get explanations before making changes. The assistant's ability to read my files and create or edit them directly was also helpful for the skeleton and diagram, as long as I reviewed each change before keeping it.
- How did using separate chat sessions for different phases help you stay organized?
    - I mostly stayed in one long chat, which made it harder to separate design decisions from implementation details. When I needed to revisit an earlier decision, I had to scroll back through a lot of unrelated conversation. If I did this again, I would start a fresh chat for each phase (design, algorithms, testing) so each conversation stays focused on one job.

**b. Judgment and verification**

- Describe one moment where you did not accept an AI suggestion as-is.
    - When I asked the AI to review my class skeleton, it suggested adding `remove_pet()` and `remove_task()` methods and storing the generated schedule inside the Scheduler. I rejected both because the required features don't need them, and I wanted to keep the design simple. I accepted its suggestions to link each task to its pet and to sort priority using numbers instead of text. I also made two simplifying choices of my own: I stored times as zero-padded "HH:MM" strings so they sort correctly as plain text, and I kept conflict detection to exact time matches instead of a more complex overlap check.
- How did you evaluate or verify what the AI suggested?
    - I ran `main.py` after each change and compared the output to what I expected. For example, two tasks at 08:00 produced a conflict warning, and completing a daily task created a new one due the next day. I wrote 14 pytest tests covering sorting, recurrence, conflicts, filtering, and edge cases, and they all pass. I also tested the Streamlit app by hand, adding pets and tasks, creating a conflict, and marking a recurring task complete.
- What did you learn about being the "lead architect" when working with powerful AI tools?
    - The AI can write code quickly, but it doesn't know what my project needs. I had to decide which suggestions to accept, keep the design small, and check every result myself. I also learned to read generated code before saving it, because copying a partial or wrong version caused real errors, like when an incomplete paste left my `app.py` with a syntax error. When I treated AI output as a draft to review instead of a final answer, I ended up with a system I can actually explain.
---

## 4. Testing and Verification

**a. What you tested**

- What behaviors did you test?
    - I tested sorting by time (including untimed tasks), daily and weekly recurring tasks, conflict detection, filtering by pet and status, and the schedule respecting available time and priority. I also tested edge cases like an owner with no pets.
- Why were these tests important?
    - These are the behaviors the app depends on. If sorting or conflict detection is wrong, the owner could miss a medication or double-book a time slot.

**b. Confidence**

- How confident are you that your scheduler works correctly?
    - Fairly confident (4 out of 5). All 14 tests pass, and the demo output matches what I expected.
- What edge cases would you test next if you had more time?
    - Tasks that overlap in duration instead of only matching start times, invalid input like zero-minute tasks, and tasks that cross midnight.

---

## 5. Reflection

**a. What went well**

- What part of this project are you most satisfied with?
    - I'm most satisfied with building the logic first and verifying it in the terminal before touching the UI. Because `pawpal_system.py` was already tested, connecting Streamlit only meant calling methods that worked.

**b. What you would improve**

- If you had another iteration, what would you improve or redesign?
    - I would make conflict detection check overlapping durations instead of only exact start times, validate input (like zero-minute tasks), let users edit or delete tasks, and save data to a file so it survives restarting the app.

**c. Key takeaway**

- What is one important thing you learned about designing systems or working with AI on this project?
    - Planning the classes before coding made everything easier, and AI works best when I give it clear limits and then verify the result. The design decisions were mine, even when the AI wrote the code.
