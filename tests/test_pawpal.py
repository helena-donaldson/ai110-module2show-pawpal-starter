import pytest
from pawpal_system import Pet, Task


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
