from pawpal_system import Pet, Owner, Task, Plan

Pet1 = Pet(name="Buddy", species="Dog")
Pet2 = Pet(name="Whiskers", species="Cat")

# Create an owner with a clear time window (the plan will use defaults if parsing fails)
Owner1 = Owner(times_available="08:00-18:00", preferences="short", pets=[Pet1, Pet2])

# Create tasks out of chronological order (time is HH:MM)
Task1 = Task(name="Walk", priority=1, duration=30, pet=Pet1, time="12:00")
Task2 = Task(name="Feed", priority=2, duration=15, pet=Pet2, time="08:00")
Task3 = Task(name="Play", priority=3, duration=20, pet=Pet2, time="10:30")
Task4 = Task(name="Walk", priority=1, duration=30, pet=Pet1, time="12:00")

plan = Plan(owner=Owner1, tasks=[Task1, Task2, Task3, Task4])

print("Tasks (original order):")
for t in plan.tasks:
    print(f"  {t}")

print("\nTasks sorted by time:")
for t in plan.sort_by_time():
    print(f"  {t}")

# Demonstrate filtering
Task1.mark_complete()
print("\nCompleted tasks:")
for t in plan.filter_tasks(status="completed"):
    print(f"  {t}")

print("\nTasks for Whiskers:")
for t in plan.filter_tasks(pet_name="whiskers"):
    print(f"  {t}")

print(f"\nToday's Schedule: {plan.generate_schedule()}")