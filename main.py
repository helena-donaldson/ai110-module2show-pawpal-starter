from pawpal_system import Pet, Owner, Task, Plan

Pet1 = Pet(name="Buddy", species="Dog")
Pet2 = Pet(name="Whiskers", species="Cat")

Owner1 = Owner(
    times_available="Morning, Afternoon", preferences="short", pets=[Pet1, Pet2])

Task1 = Task(name="Walk", priority=1, duration=30, pet=Pet(name="Buddy", species="Dog"))
Task2 = Task(name="Feed", priority=2, duration=15, pet=Pet(name="Whiskers", species="Cat"))
Task3 = Task(name="Feed", priority=3, duration=20, pet=Pet(name="Whiskers", species="Cat"))

plan = Plan(owner=Owner1, tasks=[Task1, Task2, Task3])
print(f"Today's Schedule: {plan.generate_schedule()}")