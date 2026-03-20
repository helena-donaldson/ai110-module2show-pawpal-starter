import streamlit as st
from pawpal_system import Pet, Owner, Task, Plan

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

# --------- Session state setup ---------
# Keep pets/tasks/schedule in memory across reruns.
if "pets" not in st.session_state:
    st.session_state.pets = []  # type: list[Pet]

if "tasks" not in st.session_state:
    st.session_state.tasks = []  # type: list[Task]

if "schedule" not in st.session_state:
    st.session_state.schedule = ""

if "plan" not in st.session_state:
    st.session_state.plan = None

# --------- Owner info ---------
st.subheader("Owner")
owner_name = st.text_input("Owner name", value="Jordan")
times_available = st.text_input("Available time window", value="08:00-18:00")
preferences = st.selectbox(
    "Preferences",
    ["none", "short tasks first", "long tasks first"],
    format_func=lambda v: v.capitalize(),
)

st.divider()

# --------- Pets ---------
st.subheader("Pets")
pet_name = st.text_input("Pet name", value="Mochi")
species = st.selectbox("Species", ["dog", "cat", "other"])

if st.button("Add pet"):
    if pet_name.strip():
        new_pet = Pet(pet_name.strip(), species)
        st.session_state.pets.append(new_pet)
        st.success(f"Added pet: {new_pet}")
    else:
        st.error("Please enter a pet name.")

if st.session_state.pets:
    pet_data = [{"Name": pet.name, "Species": pet.species.capitalize()} for pet in st.session_state.pets]
    st.dataframe(pet_data, use_container_width=True)
else:
    st.info("No pets yet. Add one above.")

st.divider()

# --------- Tasks ---------
st.subheader("Tasks")
st.caption("Add a task and assign it to one of your pets.")

if not st.session_state.pets:
    st.warning("Add a pet before creating tasks.")
else:
    col1, col2, col3 = st.columns(3)
    with col1:
        task_title = st.text_input("Task title", value="Morning walk")
    with col2:
        duration = st.number_input("Duration (minutes)", min_value=1, max_value=240, value=20)
    with col3:
        priority = st.selectbox("Priority", ["low", "medium", "high"], index=2)

    pet_options = {str(pet): pet for pet in st.session_state.pets}
    pet_choice = st.selectbox("Pet", list(pet_options.keys()))

    if st.button("Add task"):
        if task_title.strip():
            pet = pet_options[pet_choice]
            new_task = Task(int(duration), priority, task_title.strip(), pet)
            st.session_state.tasks.append(new_task)
            pet.add_task(new_task)
            st.success(f"Added task '{new_task.name}' for {pet.name}")
        else:
            st.error("Please enter a task title.")

if st.session_state.tasks:
    task_data = [
        {
            "Task": task.name,
            "Pet": task.pet.name,
            "Duration (min)": task.duration,
            "Priority": task.priority_label().capitalize(),
            "Status": task.status.capitalize()
        }
        for task in st.session_state.tasks
    ]
    st.dataframe(task_data, use_container_width=True)
else:
    st.info("No tasks yet. Add one above.")

st.divider()

# --------- Schedule generation ---------
st.subheader("Build Schedule")

if st.button("Generate schedule"):
    owner = Owner(times_available, preferences, st.session_state.pets)
    plan = Plan(owner, st.session_state.tasks)
    st.session_state.schedule = plan.generate_schedule()
    st.session_state.plan = plan

if st.session_state.schedule:
    st.markdown("### Generated schedule")
    
    plan = st.session_state.get("plan")
    if plan:
        sorted_tasks = plan.sort_by_time()
        
        # Display schedule summary metrics
        col1, col2, col3, col4 = st.columns(4)
        with col1:
            st.metric("Total Tasks", len(sorted_tasks))
        with col2:
            total_time = sum(t.duration for t in sorted_tasks)
            st.metric("Total Duration", f"{total_time} min")
        with col3:
            high_priority = len([t for t in sorted_tasks if t.priority == 3])
            st.metric("High Priority", high_priority)
        with col4:
            unique_pets = len(set(t.pet.name for t in sorted_tasks))
            st.metric("Pets Involved", unique_pets)
        
        st.divider()
        
        # Display sorted tasks in a professional table
        with st.expander("📋 Task Order & Details", expanded=True):
            task_order_data = [
                {
                    "Order": i,
                    "Task": task.name,
                    "Pet": task.pet.name,
                    "Duration (min)": task.duration,
                    "Priority": task.priority_label().capitalize(),
                    "Scheduled Time": task.time if task.time else "TBD"
                }
                for i, task in enumerate(sorted_tasks, 1)
            ]
            st.dataframe(task_order_data, use_container_width=True)
        
        st.divider()
        
        # Display the full schedule
        st.markdown("### ⏰ Full Schedule")
        st.code(st.session_state.schedule, language="text")
else:
    st.info("Generate a schedule to see the plan.")
