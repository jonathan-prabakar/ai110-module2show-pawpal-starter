import streamlit as st
from pawpal_system import Owner, Pet, Task, Schedule

st.set_page_config(page_title="PawPal+", page_icon="🐾", layout="centered")

st.title("🐾 PawPal+")

st.markdown(
    """
Welcome to the PawPal+ starter app.

This file is intentionally thin. It gives you a working Streamlit app so you can start quickly,
but **it does not implement the project logic**. Your job is to design the system and build it.

Use this app as your interactive demo once your backend classes/functions exist.
"""
)

with st.expander("Scenario", expanded=True):
    st.markdown(
        """
**PawPal+** is a pet care planning assistant. It helps a pet owner plan care tasks
for their pet(s) based on constraints like time, priority, and preferences.

You will design and implement the scheduling logic and connect it to this Streamlit UI.
"""
    )

with st.expander("What you need to build", expanded=True):
    st.markdown(
        """
At minimum, your system should:
- Represent pet care tasks (what needs to happen, how long it takes, priority)
- Represent the pet and the owner (basic info and preferences)
- Build a plan/schedule for a day that chooses and orders tasks based on constraints
- Explain the plan (why each task was chosen and when it happens)
"""
    )

st.divider()

# --- Owner lives in the session "vault" so it persists across reruns ---
if "owner" not in st.session_state:
    st.session_state.owner = Owner(name="Jordan", available_minutes=120)
owner = st.session_state.owner

st.subheader("Owner")
owner.name = st.text_input("Owner name", value=owner.name)
owner.available_minutes = st.number_input(
    "Available minutes today", min_value=0, max_value=1440, value=owner.available_minutes
)

st.divider()

st.subheader("Add a Pet")
with st.form("add_pet"):
    pet_name = st.text_input("Pet name", value="Mochi")
    species = st.selectbox("Species", ["dog", "cat", "other"])
    if st.form_submit_button("Add pet"):
        owner.add_pet(Pet(name=pet_name, species=species))

if owner.pets:
    st.write("Pets:", ", ".join(f"{p.name} ({p.species})" for p in owner.pets))
else:
    st.info("No pets yet. Add one above.")

st.divider()

st.subheader("Schedule a Task")
if owner.pets:
    pet = st.selectbox("Pet", owner.pets, format_func=lambda p: p.name)
    with st.form("add_task"):
        col1, col2, col3 = st.columns(3)
        with col1:
            task_title = st.text_input("Task title", value="Morning walk")
        with col2:
            duration = st.number_input("Duration (minutes)", min_value=1, max_value=240, value=20)
        with col3:
            priority = st.selectbox("Priority", ["low", "medium", "high"], index=2)
        preferred_time = st.text_input("Preferred time (HH:MM)", value="08:00")
        if st.form_submit_button("Add task"):
            pet.add_task(
                Task(
                    task_id=f"t{len(pet.tasks) + 1}",
                    name=task_title,
                    duration_minutes=int(duration),
                    priority=priority,
                    preferred_time=preferred_time,
                )
            )

    if pet.tasks:
        st.write(f"Tasks for {pet.name}:")
        st.table(
            [
                {"time": t.preferred_time, "task": t.name,
                 "min": t.duration_minutes, "priority": t.priority}
                for t in pet.tasks
            ]
        )

    st.divider()
    st.subheader("Build Schedule")
    if st.button("Generate schedule"):
        schedule = Schedule(date="today", owner=owner, pet=pet, task_pool=list(pet.tasks))
        schedule.generate_plan()
        st.text(schedule.explain_plan())
        st.write(f"Within budget: {schedule.is_within_budget()}")
else:
    st.info("Add a pet before scheduling tasks.")
