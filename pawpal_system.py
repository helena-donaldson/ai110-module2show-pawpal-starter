from __future__ import annotations

from dataclasses import dataclass, field
from datetime import datetime, timedelta
from typing import List, Optional, Union


@dataclass
class Pet:
    """A simple representation of a pet."""

    name: str
    species: str = "unknown"
    tasks: List[Task] = field(default_factory=list)

    def __post_init__(self):
        """Initialize and validate pet attributes after dataclass creation."""
        self.name = str(self.name).strip()
        self.species = str(self.species).strip().lower() if self.species else "unknown"

    def add_task(self, task: Task):
        """Add a task to this pet's task list."""
        if not isinstance(task, Task):
            raise TypeError("add_task expects a Task instance")
        self.tasks.append(task)

    def __str__(self):
        """Return a string representation of the pet."""
        return f"{self.name} ({self.species})"


@dataclass
class Task:
    """A single pet care task."""

    duration: int
    priority: Union[int, str]
    name: str
    pet: Pet
    notes: str = ""
    status: str = "pending"

    def __post_init__(self):
        """Initialize and validate task attributes after dataclass creation."""
        self.name = str(self.name).strip()
        self.duration = int(self.duration) if self.duration is not None else 0
        self.priority = self._normalize_priority(self.priority)
        self.status = str(self.status).strip().lower() if self.status else "pending"

    @staticmethod
    def _normalize_priority(priority: Union[int, str]) -> int:
        """Normalize priority to an integer scale 1 (low) - 3 (high)."""
        if isinstance(priority, str):
            mapping = {"low": 1, "medium": 2, "high": 3}
            normalized = priority.strip().lower()
            if normalized in mapping:
                return mapping[normalized]
            if normalized.isdigit():
                priority = int(normalized)

        if isinstance(priority, int):
            if 1 <= priority <= 3:
                return priority

        raise ValueError("priority must be one of: low/medium/high or 1-3")

    def priority_label(self) -> str:
        """Return the priority as a string label."""
        return {1: "low", 2: "medium", 3: "high"}[self.priority]

    def mark_complete(self):
        """Mark this task as completed."""
        self.status = "completed"

    def __str__(self):
        """Return a string representation of the task."""
        return f"{self.name} [{self.priority_label()}] - {self.duration}m ({self.pet.name})"

    @staticmethod
    def _normalize_priority(priority: Union[int, str]) -> int:
        """Normalize priority to an integer scale 1 (low) - 3 (high)."""
        if isinstance(priority, str):
            mapping = {"low": 1, "medium": 2, "high": 3}
            normalized = priority.strip().lower()
            if normalized in mapping:
                return mapping[normalized]
            if normalized.isdigit():
                priority = int(normalized)

        if isinstance(priority, int):
            if 1 <= priority <= 3:
                return priority

        raise ValueError("priority must be one of: low/medium/high or 1-3")

    def priority_label(self) -> str:
        """Return the priority as a string label."""
        return {1: "low", 2: "medium", 3: "high"}[self.priority]

    def __str__(self):
        """Return a string representation of the task."""
        return f"{self.name} [{self.priority_label()}] - {self.duration}m ({self.pet.name})"


class Owner:
    """Represents a pet owner and their preferences."""

    def __init__(self, times_available: str, preferences: str, pets: List[Pet]):
        """Initialize the owner with availability, preferences, and pets."""
        self._times_available = self._normalize_times(times_available)
        self._preferences = self._normalize_preferences(preferences)
        self._pets = pets or []

    @staticmethod
    def _normalize_times(times_available: Optional[str]) -> str:
        """Normalize the times available string."""
        if times_available is None:
            return ""
        return str(times_available).strip()

    @staticmethod
    def _normalize_preferences(preferences: Optional[str]) -> str:
        """Normalize the preferences string."""
        if preferences is None:
            return ""
        return str(preferences).strip().lower()

    def get_times_available(self) -> str:
        """Get the owner's available times."""
        return self._times_available

    def set_times_available(self, value: str):
        """Set the owner's available times."""
        self._times_available = self._normalize_times(value)

    def get_preferences(self) -> str:
        """Get the owner's preferences."""
        return self._preferences

    def set_preferences(self, value: str):
        """Set the owner's preferences."""
        self._preferences = self._normalize_preferences(value)

    def get_pets(self) -> List[Pet]:
        """Get the list of pets."""
        return list(self._pets)

    def set_pets(self, value: List[Pet]):
        """Set the list of pets."""
        self._pets = list(value) if value is not None else []


class Plan:
    """Generates a daily plan (schedule) based on owner constraints and tasks."""

    def __init__(self, owner: Owner, tasks: List[Task], schedule: str = ""):
        """Initialize the plan with owner, tasks, and optional schedule."""
        self.owner = owner
        self.tasks = tasks or []
        self.schedule = schedule

    def add_task(self, task: Task):
        """Add a task to the plan."""
        if not isinstance(task, Task):
            raise TypeError("add_task expects a Task instance")
        self.tasks.append(task)

    def edit_task(self, task: Task):
        """Replace an existing task with the same name and pet.

        This is a simple edit model for the purposes of the exercise.
        """
        for idx, existing in enumerate(self.tasks):
            if existing.name == task.name and existing.pet.name == task.pet.name:
                self.tasks[idx] = task
                return
        raise ValueError(f"Task not found: {task.name} for pet {task.pet.name}")

    def generate_schedule(self) -> str:
        """Build a textual schedule based on the owner's constraints."""
        window = self._parse_time_window(self.owner.get_times_available())
        if not window:
            # Default day: 08:00 - 18:00 (10 hours)
            start = datetime.strptime("08:00", "%H:%M")
            end = datetime.strptime("18:00", "%H:%M")
        else:
            start, end = window

        total_available_minutes = int((end - start).total_seconds() / 60)

        # Sort tasks by priority (high first) and then by duration, but allow owner preferences to tweak ordering.
        tasks = sorted(self.tasks, key=self._task_sort_key)

        scheduled_lines = []
        current_time = start
        remaining = total_available_minutes

        for task in tasks:
            if task.duration <= 0:
                scheduled_lines.append(f"SKIPPED (invalid duration): {task}")
                continue

            if task.duration <= remaining:
                end_time = current_time + timedelta(minutes=task.duration)
                scheduled_lines.append(
                    f"{current_time.strftime('%H:%M')} - {end_time.strftime('%H:%M')}: {task.name} ({task.pet.name}) [{task.priority_label()}]"
                )
                current_time = end_time
                remaining -= task.duration
            else:
                scheduled_lines.append(
                    f"NOT SCHEDULED (no time): {task.name} ({task.pet.name}) [{task.priority_label()}] - needs {task.duration}m"
                )

        self.schedule = "\n".join(scheduled_lines)
        return self.schedule

    def _task_sort_key(self, task: Task):
        """Sort tasks based on priority, duration, and owner preferences."""
        # higher priority first
        priority_key = -task.priority

        # respect preferences like 'short' or 'long' tasks first
        prefs = self.owner.get_preferences()
        if "short" in prefs:
            duration_key = task.duration
        elif "long" in prefs:
            duration_key = -task.duration
        else:
            duration_key = task.duration

        # for deterministic ordering, include name
        return (priority_key, duration_key, task.name)

    @staticmethod
    def _parse_time_window(times_available: str) -> Optional[tuple[datetime, datetime]]:
        """Parse a simple HH:MM-HH:MM time window.

        Returns a tuple (start, end) as datetimes on an arbitrary date.
        """
        if not times_available:
            return None

        # Accept formats like '08:00-18:00', '8-17', '8:30 - 17:15'
        parts = times_available.replace(" ", "").split("-")
        if len(parts) != 2:
            return None

        def parse_time(t: str) -> Optional[datetime]:
            for fmt in ("%H:%M", "%H"):
                try:
                    return datetime.strptime(t, fmt)
                except ValueError:
                    continue
            return None

        start = parse_time(parts[0])
        end = parse_time(parts[1])
        if not start or not end or end <= start:
            return None

        return start, end
