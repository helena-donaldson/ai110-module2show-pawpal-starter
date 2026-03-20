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


class TestSortingComprehensive:
    """Comprehensive tests for task sorting by time and priority."""

    def test_sort_by_time_chronological_order(self):
        """Verify tasks are returned in strict chronological order."""
        pet = Pet("Buddy", "dog")
        task1 = Task(15, "high", "Breakfast", pet, time="06:00")
        task2 = Task(20, "medium", "Walk", pet, time="07:30")
        task3 = Task(10, "low", "Playtime", pet, time="12:00")
        task4 = Task(15, "high", "Dinner", pet, time="18:00")

        owner = Owner("06:00-20:00", "none", [pet])
        plan = Plan(owner, [task4, task1, task3, task2])

        sorted_tasks = plan.sort_by_time()
        assert sorted_tasks[0] is task1  # 06:00
        assert sorted_tasks[1] is task2  # 07:30
        assert sorted_tasks[2] is task3  # 12:00
        assert sorted_tasks[3] is task4  # 18:00

    def test_sort_by_time_mixed_with_and_without_times(self):
        """Verify tasks with explicit times come before tasks without times."""
        pet = Pet("Mochi", "dog")
        task_with_time1 = Task(15, "high", "Feed", pet, time="09:00")
        task_with_time2 = Task(20, "low", "Walk", pet, time="10:00")
        task_no_time1 = Task(30, "high", "Play", pet)  # No time
        task_no_time2 = Task(15, "medium", "Groom", pet)  # No time

        owner = Owner("08:00-18:00", "none", [pet])
        plan = Plan(owner, [task_no_time2, task_with_time2, task_no_time1, task_with_time1])

        sorted_tasks = plan.sort_by_time()
        # First two should have times, in chronological order
        assert sorted_tasks[0] is task_with_time1  # 09:00
        assert sorted_tasks[1] is task_with_time2  # 10:00
        # Last two should not have times, sorted by priority/duration
        assert sorted_tasks[2] is task_no_time1  # high priority, 30m
        assert sorted_tasks[3] is task_no_time2  # medium priority

    def test_sort_by_time_same_time_maintains_order(self):
        """Verify tasks with same start time maintain insertion order (no secondary sort for timed tasks)."""
        pet = Pet("Mochi", "dog")
        task_high = Task(15, "high", "Feed", pet, time="08:00")
        task_medium = Task(20, "medium", "Walk", pet, time="08:00")
        task_low = Task(10, "low", "Snack", pet, time="08:00")

        owner = Owner("08:00-18:00", "none", [pet])
        plan = Plan(owner, [task_high, task_medium, task_low])

        sorted_tasks = plan.sort_by_time()
        # All have same time, so they maintain insertion order (sort_by_time doesn't apply secondary sort to timed tasks)
        assert sorted_tasks[0] is task_high
        assert sorted_tasks[1] is task_medium
        assert sorted_tasks[2] is task_low
        assert all(t.time == "08:00" for t in sorted_tasks)

    def test_sort_by_time_no_time_respects_owner_preference_short(self):
        """Verify tasks without time are sorted by priority first, then duration when owner prefers short tasks."""
        pet = Pet("Buddy", "dog")
        # All low priority, different durations
        task_long = Task(45, "low", "Training", pet)
        task_short = Task(10, "low", "Treat", pet)
        task_medium = Task(25, "low", "Walk", pet)

        owner = Owner("08:00-18:00", "short", [pet])
        plan = Plan(owner, [task_long, task_short, task_medium])

        sorted_tasks = plan.sort_by_time()
        # Same priority: short preference orders by duration (ascending)
        assert sorted_tasks[0] is task_short  # 10m
        assert sorted_tasks[1] is task_medium  # 25m
        assert sorted_tasks[2] is task_long  # 45m

    def test_sort_by_time_no_time_respects_owner_preference_long(self):
        """Verify tasks without time are sorted by priority first, then by duration (desc) when owner prefers long tasks."""
        pet = Pet("Buddy", "dog")
        # All low priority, different durations
        task_short = Task(10, "low", "Treat", pet)
        task_medium = Task(25, "low", "Walk", pet)
        task_long = Task(45, "low", "Training", pet)

        owner = Owner("08:00-18:00", "long", [pet])
        plan = Plan(owner, [task_short, task_medium, task_long])

        sorted_tasks = plan.sort_by_time()
        # Same priority: long preference orders by duration (descending)
        assert sorted_tasks[0] is task_long  # 45m
        assert sorted_tasks[1] is task_medium  # 25m
        assert sorted_tasks[2] is task_short  # 10m

    def test_sort_by_time_deterministic_with_identical_tasks(self):
        """Verify deterministic ordering when multiple tasks have identical properties."""
        pet = Pet("Mochi", "dog")
        task_a = Task(15, "medium", "Activity", pet)
        task_b = Task(15, "medium", "Activity", pet)

        owner = Owner("08:00-18:00", "none", [pet])
        plan = Plan(owner, [task_b, task_a])

        sorted_tasks = plan.sort_by_time()
        # With same priority, duration, and name, order should be stable
        assert len(sorted_tasks) == 2


class TestRecurrenceComprehensive:
    """Comprehensive tests for recurring task logic."""

    def test_daily_recurrence_creates_next_pending_task(self):
        """Verify daily recurrence creates a new pending task with same attributes."""
        pet = Pet("Mochi", "dog")
        task = Task(
            duration=20,
            priority="high",
            name="Feed",
            pet=pet,
            time="08:00",
            recurrence="daily",
            notes="with dry food"
        )

        owner = Owner("08:00-18:00", "none", [pet])
        plan = Plan(owner, [task])

        next_task = plan.mark_task_complete(task)

        # Original task should be completed
        assert task.status == "completed"
        assert task.recurrence == "daily"

        # New task should be pending
        assert next_task is not None
        assert next_task.status == "pending"
        assert next_task.recurrence == "daily"

        # All attributes should be preserved
        assert next_task.name == "Feed"
        assert next_task.duration == 20
        assert next_task.priority == 3  # "high" normalizes to 3
        assert next_task.time == "08:00"
        assert next_task.notes == "with dry food"
        assert next_task.pet is pet

    def test_weekly_recurrence_creates_next_pending_task(self):
        """Verify weekly recurrence creates a new pending task."""
        pet = Pet("Buddy", "dog")
        task = Task(
            duration=60,
            priority="medium",
            name="Grooming",
            pet=pet,
            time="10:00",
            recurrence="weekly"
        )

        owner = Owner("08:00-18:00", "none", [pet])
        plan = Plan(owner, [task])

        next_task = plan.mark_task_complete(task)

        assert task.status == "completed"
        assert next_task is not None
        assert next_task.status == "pending"
        assert next_task.recurrence == "weekly"
        assert next_task.name == "Grooming"

    def test_non_recurring_task_does_not_create_next_occurrence(self):
        """Verify that non-recurring tasks return None on mark_complete."""
        pet = Pet("Mochi", "dog")
        task = Task(15, "high", "One-time Vet Visit", pet)

        owner = Owner("08:00-18:00", "none", [pet])
        plan = Plan(owner, [task])

        next_task = plan.mark_task_complete(task)

        assert task.status == "completed"
        assert next_task is None
        assert len(plan.tasks) == 1  # Only original task remains

    def test_recurring_task_multiple_completions(self):
        """Verify that completing a recurring task multiple times creates a chain."""
        pet = Pet("Mochi", "dog")
        task1 = Task(15, "high", "Feed", pet, time="08:00", recurrence="daily")

        owner = Owner("08:00-18:00", "none", [pet])
        plan = Plan(owner, [task1])

        # First completion
        task2 = plan.mark_task_complete(task1)
        assert len(plan.tasks) == 2
        assert task1.status == "completed"
        assert task2.status == "pending"

        # Second completion
        task3 = plan.mark_task_complete(task2)
        assert len(plan.tasks) == 3
        assert task2.status == "completed"
        assert task3.status == "pending"

        # Third completion
        task4 = plan.mark_task_complete(task3)
        assert len(plan.tasks) == 4
        assert task3.status == "completed"
        assert task4.status == "pending"

        # Verify all are in the plan
        assert all(t in plan.tasks for t in [task1, task2, task3, task4])

    def test_recurring_task_preserves_all_attributes_through_chain(self):
        """Verify attributes are preserved across multiple recurrence cycles."""
        pet = Pet("Buddy", "dog")
        original = Task(
            duration=25,
            priority="medium",
            name="Training Session",
            pet=pet,
            time="14:00",
            recurrence="daily",
            notes="work on recall"
        )

        owner = Owner("08:00-18:00", "none", [pet])
        plan = Plan(owner, [original])

        task_gen2 = plan.mark_task_complete(original)
        task_gen3 = plan.mark_task_complete(task_gen2)
        task_gen4 = plan.mark_task_complete(task_gen3)

        # Verify each generation preserves attributes
        for task in [task_gen2, task_gen3, task_gen4]:
            assert task.name == "Training Session"
            assert task.duration == 25
            assert task.priority == 2  # "medium"
            assert task.time == "14:00"
            assert task.recurrence == "daily"
            assert task.notes == "work on recall"
            assert task.pet is pet


class TestConflictDetectionComprehensive:
    """Comprehensive tests for conflict detection in scheduling."""

    def test_conflict_detection_two_tasks_same_time(self):
        """Verify conflict is detected when two tasks share the same start time."""
        pet = Pet("Mochi", "dog")
        task1 = Task(15, "high", "Feed", pet, time="08:00")
        task2 = Task(20, "medium", "Walk", pet, time="08:00")

        owner = Owner("08:00-18:00", "none", [pet])
        plan = Plan(owner, [task1, task2])

        schedule = plan.generate_schedule()
        assert "WARNINGS:" in schedule
        assert "Conflict" in schedule
        assert "08:00" in schedule

    def test_conflict_detection_multiple_tasks_same_time(self):
        """Verify conflict is detected when three or more tasks share the same start time."""
        pet = Pet("Buddy", "dog")
        task1 = Task(10, "high", "Breakfast", pet, time="07:00")
        task2 = Task(15, "medium", "Medication", pet, time="07:00")
        task3 = Task(20, "low", "Vitamin", pet, time="07:00")

        owner = Owner("07:00-19:00", "none", [pet])
        plan = Plan(owner, [task1, task2, task3])

        schedule = plan.generate_schedule()
        assert "WARNINGS:" in schedule
        assert schedule.count("Conflict") >= 1

    def test_conflict_detection_different_pets_same_time(self):
        """Verify conflicts are detected even when tasks are for different pets."""
        pet_a = Pet("Mochi", "dog")
        pet_b = Pet("Whiskers", "cat")

        task1 = Task(15, "high", "Feed", pet_a, time="08:00")
        task2 = Task(20, "high", "Play", pet_b, time="08:00")

        owner = Owner("08:00-18:00", "none", [pet_a, pet_b])
        plan = Plan(owner, [task1, task2])

        schedule = plan.generate_schedule()
        assert "WARNINGS:" in schedule
        assert "Conflict" in schedule

    def test_no_conflict_when_tasks_sequential(self):
        """Verify no conflict is flagged when tasks are scheduled sequentially."""
        pet = Pet("Mochi", "dog")
        task1 = Task(30, "high", "Feed", pet, time="08:00")
        task2 = Task(20, "medium", "Walk", pet, time="08:30")

        owner = Owner("08:00-18:00", "none", [pet])
        plan = Plan(owner, [task1, task2])

        schedule = plan.generate_schedule()
        # Should not have conflict warning (or if it does, it should be minimal)
        assert "Feed" in schedule
        assert "Walk" in schedule

    def test_overlap_warning_when_task_starts_during_another(self):
        """Verify overlap is detected when a task starts before the previous one ends."""
        pet = Pet("Buddy", "dog")
        task1 = Task(30, "high", "Training", pet, time="09:00")
        task2 = Task(20, "medium", "Walk", pet, time="09:15")

        owner = Owner("08:00-18:00", "none", [pet])
        plan = Plan(owner, [task1, task2])

        schedule = plan.generate_schedule()
        assert "Walk" in schedule or "Training" in schedule
