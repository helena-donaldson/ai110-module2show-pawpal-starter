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
    time: str = ""
    recurrence: Optional[str] = None
    notes: str = ""
    status: str = "pending"

    def __post_init__(self):
        """Initialize and validate task attributes after dataclass creation."""
        self.name = str(self.name).strip()
        self.duration = int(self.duration) if self.duration is not None else 0
        self.priority = self._normalize_priority(self.priority)
        self.status = str(self.status).strip().lower() if self.status else "pending"
        self.time = self._normalize_time(self.time)
        self.recurrence = self._normalize_recurrence(self.recurrence)

    @staticmethod
    def _normalize_time(time_str: Optional[str]) -> str:
        """Normalize the time string to HH:MM format (24h)."""
        if not time_str:
            return ""

        value = str(time_str).strip()
        try:
            parsed = datetime.strptime(value, "%H:%M")
            return parsed.strftime("%H:%M")
        except ValueError:
            raise ValueError("time must be in HH:MM format")

    @staticmethod
    def _normalize_recurrence(recurrence: Optional[str]) -> Optional[str]:
        """Normalize recurrence values to a known set."""
        if not recurrence:
            return None

        normalized = str(recurrence).strip().lower()
        if normalized in {"daily", "weekly"}:
            return normalized

        raise ValueError("recurrence must be 'daily', 'weekly', or None")

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

    def mark_complete(self) -> Optional["Task"]:
        """Mark this task as completed.

        For recurring tasks, return a new Task instance representing the next occurrence.
        """
        self.status = "completed"
        return self.next_occurrence()

    def next_occurrence(self) -> Optional["Task"]:
        """Return a new Task for the next occurrence if recurrence is enabled."""
        if not self.recurrence:
            return None

        return Task(
            duration=self.duration,
            priority=self.priority,
            name=self.name,
            pet=self.pet,
            time=self.time,
            recurrence=self.recurrence,
            notes=self.notes,
            status="pending",
        )

    def __str__(self):
        """Return a string representation of the task."""
        time_part = f"{self.time} - " if self.time else ""
        return f"{time_part}{self.name} [{self.priority_label()}] - {self.duration}m ({self.pet.name})"


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

    def mark_task_complete(self, task: Task) -> Optional[Task]:
        """Mark a task complete and schedule its next occurrence if recurring."""
        next_task = task.mark_complete()
        if next_task:
            self.tasks.append(next_task)
        return next_task

    def filter_tasks(
        self, status: Optional[str] = None, pet_name: Optional[str] = None
    ) -> List[Task]:
        """Return the tasks filtered by completion status and/or pet name.

        If no filters are provided, all tasks are returned.
        """
        def matches(task: Task) -> bool:
            if status:
                if task.status.strip().lower() != status.strip().lower():
                    return False
            if pet_name:
                if task.pet.name.strip().lower() != pet_name.strip().lower():
                    return False
            return True

        return [task for task in self.tasks if matches(task)]

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

        # Sort tasks by time (if set), then by priority/duration
        tasks = self.sort_by_time()

        scheduled_lines: List[str] = []
        warnings: List[str] = []
        current_time = start
        remaining = total_available_minutes
        start_map: dict[datetime, List[Task]] = {}

        def _make_datetime_for_task_time(task_time: str) -> Optional[datetime]:
            if not task_time:
                return None
            try:
                parsed = datetime.strptime(task_time, "%H:%M")
            except ValueError:
                return None
            return datetime.combine(start.date(), parsed.time())

        for task in tasks:
            if task.duration <= 0:
                scheduled_lines.append(f"SKIPPED (invalid duration): {task}")
                continue

            task_start = _make_datetime_for_task_time(task.time)
            if task_start is None:
                task_start = current_time

            # Detect conflicts: same start time for any tasks.
            if task_start in start_map:
                warnings.append(
                    f"⚠️ Conflict: {task.name} ({task.pet.name}) shares start time {task_start.strftime('%H:%M')} "
                    f"with {', '.join(t.name for t in start_map[task_start])}."
                )
                start_map[task_start].append(task)
            else:
                start_map[task_start] = [task]

            end_time = task_start + timedelta(minutes=task.duration)

            # If we are scheduling in the past relative to the last scheduled end, warn
            if task_start < current_time:
                warnings.append(
                    f"⚠️ {task.name} ({task.pet.name}) starts at {task_start.strftime('%H:%M')}, "
                    f"which overlaps earlier task(s)."
                )

            # Only count this task against remaining time if it fits in the window.
            if task_start < end and task_start >= start and end_time <= end:
                scheduled_lines.append(
                    f"{task_start.strftime('%H:%M')} - {end_time.strftime('%H:%M')}: {task.name} ({task.pet.name}) [{task.priority_label()}]"
                )
                current_time = max(current_time, end_time)
                remaining = int((end - current_time).total_seconds() / 60)
            else:
                scheduled_lines.append(
                    f"NOT SCHEDULED (no time): {task.name} ({task.pet.name}) [{task.priority_label()}] - needs {task.duration}m"
                )

        if warnings:
            scheduled_lines.append("\nWARNINGS:")
            scheduled_lines.extend(warnings)

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

    def sort_by_time(self, tasks: Optional[List[Task]] = None) -> List[Task]:
        """Return tasks sorted by time, then by priority/duration.

        Tasks with explicit time are scheduled first (by time).
        Tasks without time follow (sorted by priority/duration and owner preferences).
        """
        tasks_list = tasks if tasks is not None else self.tasks

        tasks_with_time = []
        tasks_without_time = []

        for task in tasks_list:
            if task.time:
                tasks_with_time.append(task)
            else:
                tasks_without_time.append(task)

        # Sort tasks with explicit time by their HH:MM value
        def time_key(t: Task):
            try:
                return datetime.strptime(t.time, "%H:%M").time()
            except ValueError:
                return datetime.max.time()

        tasks_with_time.sort(key=time_key)

        # Sort tasks without time by priority/duration and owner preferences
        tasks_without_time.sort(key=self._task_sort_key)

        return tasks_with_time + tasks_without_time

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
