from datetime import date, datetime, timedelta

import streamlit as st

from pawpal_system import Owner, Pet, Scheduler, Task

st.set_page_config(page_title="PawPal+", page_icon="🐾", layout="centered")

if "owner" not in st.session_state:
    st.session_state.owner = Owner(name="Jordan", scheduler=Scheduler())

owner = st.session_state.owner

st.title("PawPal+")
st.caption("Plan and track care for your pets.")
owner.name = st.text_input("Owner name", value=owner.name)

st.divider()
st.subheader("Pets")

with st.form("add_pet_form"):
    pet_name = st.text_input("Pet name")
    species = st.selectbox("Species", ["Dog", "Cat", "Other"])
    birth_date = st.date_input(
        "Birth date",
        value=date.today() - timedelta(days=365),
        max_value=date.today(),
    )
    add_pet_submitted = st.form_submit_button("Add pet")

if add_pet_submitted:
    if not pet_name.strip():
        st.error("Enter a pet name before adding the pet.")
    else:
        owner.add_pet(
            Pet(
                name=pet_name.strip(),
                species=species,
                birth_date=birth_date,
            )
        )
        st.success(f"Added {pet_name.strip()} to {owner.name}'s pets.")

if owner.pets:
    st.table(
        [
            {
                "Pet": pet.name,
                "Species": pet.species,
                "Tasks": len(pet.get_tasks()),
            }
            for pet in owner.pets
        ]
    )
else:
    st.info("Add a pet to start scheduling care.")

st.divider()
st.subheader("Care tasks")

if owner.pets:
    filter_col, status_col = st.columns(2)
    with filter_col:
        selected_task_pet = st.selectbox(
            "Filter by pet",
            ["All pets", *(pet.name for pet in owner.pets)],
            key="task_pet_filter",
        )
    with status_col:
        selected_task_status = st.selectbox(
            "Filter by status",
            ["All", "Pending", "Completed"],
            key="task_status_filter",
        )

    completed_filter = {"Pending": False, "Completed": True}.get(
        selected_task_status
    )
    filtered_tasks = owner.scheduler.filter_tasks(
        owner,
        completed=completed_filter,
        pet_name=(
            None if selected_task_pet == "All pets" else selected_task_pet
        ),
    )
    filtered_task_ids = {id(task) for task in filtered_tasks}
    display_tasks = [
        task
        for task in owner.scheduler.get_tasks(owner)
        if id(task) in filtered_task_ids
    ]

    if display_tasks:
        st.table(
            [
                {
                    "Task": task.name,
                    "Description": task.description,
                    "Duration": f"{task.duration_minutes} min",
                    "Frequency": task.frequency.title(),
                    "Priority": task.priority.title(),
                    "Status": "Completed" if task.is_completed else "Pending",
                }
                for task in display_tasks
            ]
        )
    else:
        st.info("No tasks match these filters.")
else:
    st.info("Add a pet to view care tasks.")

st.divider()
st.subheader("Schedule a task")

if owner.pets:
    suggested_time = datetime.now() + timedelta(minutes=15)
    with st.form("schedule_task_form"):
        selected_pet_index = st.selectbox(
            "Pet",
            options=range(len(owner.pets)),
            format_func=lambda index: (
                f"{owner.pets[index].name} ({owner.pets[index].species})"
            ),
        )
        task_name = st.text_input("Task name")
        description = st.text_input("Description")
        duration_minutes = st.number_input(
            "Duration (minutes)", min_value=1, max_value=240, value=20
        )
        frequency = st.selectbox("Frequency", ["Once", "Daily", "Weekly"])
        priority = st.selectbox("Priority", ["low", "medium", "high"], index=2)
        schedule_date = st.date_input(
            "Date", value=suggested_time.date(), min_value=date.today()
        )
        schedule_time = st.time_input(
            "Time",
            value=suggested_time.time().replace(second=0, microsecond=0),
        )
        schedule_submitted = st.form_submit_button("Schedule task")

    if schedule_submitted:
        selected_pet = owner.pets[selected_pet_index]
        scheduled_at = datetime.combine(schedule_date, schedule_time)
        if not task_name.strip():
            st.error("Enter a task name before scheduling.")
        elif scheduled_at < datetime.now():
            st.error("Choose a future date and time for this task.")
        else:
            task = Task(
                name=task_name.strip(),
                description=description.strip(),
                duration_minutes=int(duration_minutes),
                frequency=frequency,
                priority=priority,
            )
            selected_pet.add_task(task)
            event = owner.schedule_event(selected_pet, task, scheduled_at)
            conflict_warning = owner.scheduler.get_conflict_warning(event)
            if conflict_warning:
                st.warning(conflict_warning)
            else:
                st.success(f"Scheduled {task.name} for {selected_pet.name}.")
else:
    st.info("Add a pet before scheduling a task.")

st.divider()
st.subheader("Upcoming schedule")
upcoming_events = owner.scheduler.get_upcoming_events(owner)
if upcoming_events:
    st.table(
        [
            {
                "Date": event.scheduled_at.strftime("%b %d, %Y"),
                "Time": event.scheduled_at.strftime("%I:%M %p"),
                "Pet": event.pet.name,
                "Task": event.task.name,
                "Duration": f"{event.task.duration_minutes} min",
                "Priority": event.task.priority.title(),
                "Conflict warning": (
                    owner.scheduler.get_conflict_warning(event) or "None"
                ),
            }
            for event in upcoming_events
        ]
    )
else:
    st.info("No upcoming tasks scheduled.")
