"""PawPal+ Streamlit app: the UI layer on top of pawpal_system.py."""

import streamlit as st

from pawpal_system import Owner, Pet, Scheduler, Task

st.set_page_config(page_title="PawPal+", page_icon="🐾", layout="centered")

# Streamlit re-runs this file on every click, so keep the Owner in session_state.
# It is only created the first time the page loads.
if "owner" not in st.session_state:
    st.session_state.owner = Owner("Jordan", available_minutes=120)

owner: Owner = st.session_state.owner
scheduler = Scheduler(owner)

st.title("🐾 PawPal+")
st.caption("A pet care planner that organizes your pets' daily tasks.")

# ---------------------------------------------------------------- Owner
st.header("Owner")
col1, col2 = st.columns(2)
with col1:
    owner.name = st.text_input("Your name", value=owner.name)
with col2:
    owner.available_minutes = int(
        st.number_input(
            "Time available today (minutes)",
            min_value=10,
            max_value=1440,
            value=owner.available_minutes,
            step=10,
        )
    )

st.divider()

# ----------------------------------------------------------------- Pets
st.header("Pets")
with st.form("add_pet_form", clear_on_submit=True):
    pcol1, pcol2 = st.columns(2)
    with pcol1:
        new_pet_name = st.text_input("Pet name")
    with pcol2:
        new_pet_species = st.selectbox("Species", ["dog", "cat", "bird", "other"])
    add_pet_clicked = st.form_submit_button("Add pet")

if add_pet_clicked:
    name = new_pet_name.strip()
    if not name:
        st.warning("Please enter a pet name.")
    elif any(p.name.lower() == name.lower() for p in owner.pets):
        st.warning(f"You already have a pet named {name}.")
    else:
        owner.add_pet(Pet(name, new_pet_species))
        st.success(f"Added {name} the {new_pet_species}!")

if owner.pets:
    st.write("Your pets: " + ", ".join(f"{p.name} ({p.species})" for p in owner.pets))
else:
    st.info("No pets yet. Add one above to get started.")

st.divider()

# ---------------------------------------------------------------- Tasks
st.header("Tasks")
if not owner.pets:
    st.caption("Add a pet first, then you can schedule tasks for it.")
else:
    # ---- Add a task
    with st.form("add_task_form", clear_on_submit=True):
        selected_pet = st.selectbox("Which pet?", [p.name for p in owner.pets])
        task_title = st.text_input("Task title", placeholder="e.g. Morning walk")
        tcol1, tcol2, tcol3 = st.columns(3)
        with tcol1:
            duration = st.number_input(
                "Duration (minutes)", min_value=1, max_value=240, value=20
            )
        with tcol2:
            priority = st.selectbox("Priority", ["high", "medium", "low"], index=1)
        with tcol3:
            task_time = st.time_input("Time")
        frequency = st.selectbox("Repeats", ["once", "daily", "weekly"])
        add_task_clicked = st.form_submit_button("Add task")

    if add_task_clicked:
        if not task_title.strip():
            st.warning("Please enter a task title.")
        else:
            pet = next(p for p in owner.pets if p.name == selected_pet)
            pet.add_task(
                Task(
                    title=task_title.strip(),
                    duration_minutes=int(duration),
                    priority=priority,
                    time=task_time.strftime("%H:%M"),  # zero-padded "HH:MM"
                    frequency=frequency,
                )
            )
            st.success(f"Added '{task_title.strip()}' for {pet.name}.")

    # ---- Mark a task complete (recurring tasks create their next occurrence)
    st.subheader("Mark a task complete")
    pending = [t for t in scheduler.sort_by_time() if not t.completed]
    if pending:
        choice = st.selectbox(
            "Pending task",
            options=range(len(pending)),
            format_func=lambda i: (
                f"{pending[i].pet_name}: {pending[i].title} "
                f"({pending[i].time or 'no time'}, due {pending[i].due_date})"
            ),
        )
        if st.button("Mark complete"):
            done_task = pending[choice]
            next_task = scheduler.mark_task_complete(done_task)
            st.success(f"Completed '{done_task.title}' for {done_task.pet_name}.")
            if next_task:
                st.info(
                    f"This task repeats {next_task.frequency}. "
                    f"Next one is scheduled for {next_task.due_date}."
                )
    else:
        st.caption("No pending tasks.")

    # ---- Conflict warnings (from Scheduler.detect_conflicts)
    for message in scheduler.detect_conflicts():
        st.warning(
            f"⚠️ {message}. Consider moving one of these tasks to a different "
            "time so you aren't doing two things at once."
        )

    # ---- Task list: sorted by time, with optional filters
    st.subheader("Your tasks")
    fcol1, fcol2 = st.columns(2)
    with fcol1:
        pet_filter = st.selectbox("Show pet", ["All pets"] + [p.name for p in owner.pets])
    with fcol2:
        status_filter = st.selectbox("Show status", ["All", "Pending", "Completed"])

    tasks = scheduler.sort_by_time()  # chronological order
    # Narrow the sorted list using the Scheduler's filter methods.
    if pet_filter != "All pets":
        keep = {id(t) for t in scheduler.filter_by_pet(pet_filter)}
        tasks = [t for t in tasks if id(t) in keep]
    if status_filter != "All":
        keep = {id(t) for t in scheduler.filter_by_status(status_filter == "Completed")}
        tasks = [t for t in tasks if id(t) in keep]

    if tasks:
        st.table(
            [
                {
                    "Time": t.time or "--:--",
                    "Pet": t.pet_name,
                    "Task": t.title,
                    "Min": t.duration_minutes,
                    "Priority": t.priority,
                    "Repeats": t.frequency,
                    "Due": str(t.due_date),
                    "Status": "✅ Done" if t.completed else "⏳ Pending",
                }
                for t in tasks
            ]
        )
    else:
        st.info("No tasks match this view.")

st.divider()

# ------------------------------------------------------------- Schedule
st.header("Today's Schedule")
st.caption("Builds a plan from pending tasks, highest priority first, within your available time.")

if st.button("Generate schedule"):
    schedule = scheduler.generate_schedule()
    if schedule:
        st.success(f"Here's today's plan for {owner.name}.")
        st.table(
            [
                {
                    "Time": t.time or "--:--",
                    "Pet": t.pet_name,
                    "Task": t.title,
                    "Min": t.duration_minutes,
                    "Priority": t.priority,
                }
                for t in schedule
            ]
        )
        st.info(scheduler.explain_plan())
        if scheduler.detect_conflicts():
            st.warning("Some tasks share a time slot. See the warnings above.")
    else:
        st.warning("Nothing to schedule yet. Add a pet and some tasks first.")