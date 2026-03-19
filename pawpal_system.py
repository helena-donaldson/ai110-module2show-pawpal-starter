from dataclasses import dataclass
from typing import List

@dataclass
class Pet:
    name: str

@dataclass
class Task:
    duration: int
    priority: int
    name: str

class Owner:
    def __init__(self, times_available: str, preferences: str, pets: List[Pet]):
        self.times_available = times_available
        self.preferences = preferences
        self.pets = pets

    def get_times_available(self):
        pass

    def set_times_available(self, value):
        pass

    def get_preferences(self):
        pass

    def set_preferences(self, value):
        pass

    def get_pets(self):
        pass

    def set_pets(self, value):
        pass

class Plan:
    def __init__(self, owner: Owner, tasks: List[Task], schedule: str):
        self.owner = owner
        self.tasks = tasks
        self.schedule = schedule

    def add_task(self, task: Task):
        pass

    def generate_schedule(self):
        pass

    def edit_task(self, task: Task):
        pass
