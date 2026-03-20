import pytest
from pawpal_system import Owner, Plan, Pet, Task


class TestTask:
    def test_mark_complete_changes_status(self):
        """Verify that calling mark_complete() changes the task's status from 'pending' to 'completed'."""
        pet = Pet("Mochi", "dog")
        task = Task(30, "high", "Morning walk", pet)

        # Initial status should be 'pending'
        assert task.status == "pending"

        # Mark as complete
        task.mark_complete()

        # Status should now be 'completed'
        assert task.status == "completed"

    def test_time_can_be_set_and_normalized(self):
        """Verify that task times are normalized into HH:MM format."""
        pet = Pet("Mochi", "dog")
        task = Task(10, "low", "Snack time", pet, time="8:00")

        assert task.time == "08:00"
        assert task.__str__().startswith("08:00 - ")


class TestPet:
    def test_add_task_increases_task_count(self):
        """Verify that adding a task to a pet increases the pet's task count."""
        pet = Pet("Mochi", "dog")

        # Initially, no tasks
        assert len(pet.tasks) == 0

        # Add a task
        task = Task(30, "high", "Morning walk", pet)
        pet.add_task(task)

        # Task count should increase to 1
        assert len(pet.tasks) == 1

        # Add another task
        task2 = Task(20, "medium", "Feed", pet)
        pet.add_task(task2)

        # Task count should increase to 2
        assert len(pet.tasks) == 2


class TestPlan:
    def test_sort_by_time_orders_tasks(self):
        """Verify that sort_by_time orders tasks by their HH:MM time."""
        pet = Pet("Mochi", "dog")

        task_a = Task(10, "medium", "Breakfast", pet, time="08:00")
        task_b = Task(20, "medium", "Walk", pet, time="07:30")

        owner = Owner("08:00-18:00", "none", [pet])
        plan = Plan(owner, [task_a, task_b])

        sorted_tasks = plan.sort_by_time()
        assert sorted_tasks[0] is task_b
        assert sorted_tasks[1] is task_a

    def test_filter_tasks_by_status_and_pet(self):
        """Verify that filter_tasks correctly filters by status and pet name."""
        pet_a = Pet("Mochi", "dog")
        pet_b = Pet("Buddy", "dog")

        task1 = Task(10, "high", "Walk", pet_a)
        task2 = Task(15, "medium", "Feed", pet_a)
        task3 = Task(20, "low", "Play", pet_b)

        task1.mark_complete()

        owner = Owner("08:00-18:00", "none", [pet_a, pet_b])
        plan = Plan(owner, [task1, task2, task3])

        completed = plan.filter_tasks(status="completed")
        assert completed == [task1]

        mochis_tasks = plan.filter_tasks(pet_name="mochi")
        assert {t.name for t in mochis_tasks} == {"Walk", "Feed"}

        combined = plan.filter_tasks(status="pending", pet_name="buddy")
        assert combined == [task3]

    def test_mark_task_complete_creates_next_recurrence(self):
        """Verify that marking a recurring task complete schedules the next occurrence."""
        pet = Pet("Mochi", "dog")
        task = Task(15, "medium", "Feed", pet, time="08:00", recurrence="daily")

        owner = Owner("08:00-18:00", "none", [pet])
        plan = Plan(owner, [task])

        next_task = plan.mark_task_complete(task)

        assert task.status == "completed"
        assert next_task is not None
        assert next_task.status == "pending"
        assert next_task.recurrence == "daily"
        assert next_task.name == task.name
        assert next_task.pet is task.pet
        assert next_task is not task

        # Ensure the plan now contains the new task
        assert next_task in plan.tasks

    def test_schedule_conflict_warning(self):
        """Verify that generate_schedule returns a warning when two tasks share the same start time."""
        pet = Pet("Mochi", "dog")
        task1 = Task(15, "medium", "Feed", pet, time="08:00")
        task2 = Task(20, "high", "Walk", pet, time="08:00")

        owner = Owner("08:00-18:00", "none", [pet])
        plan = Plan(owner, [task1, task2])

        schedule = plan.generate_schedule()
        assert "WARNINGS:" in schedule
        assert "Conflict" in schedule
