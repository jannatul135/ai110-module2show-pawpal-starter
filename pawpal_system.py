"""PawPal+ core system: Task, Pet, Owner, and Scheduler classes."""

from dataclasses import dataclass, field
from datetime import date

PRIORITY_ORDER = {"high": 3, "medium": 2, "low": 1}


@dataclass
class Task:
    """A single pet care activity, like a walk or feeding."""

    title: str
    duration_minutes: int
    priority: str = "medium"
    time: str = ""  # zero-padded "HH:MM", e.g. "09:00"
    frequency: str = "once"
    completed: bool = False
    pet_name: str = ""
    due_date: date = field(default_factory=date.today)

    def mark_complete(self) -> None:
        """Mark this task as completed."""
        self.completed = True


@dataclass
class Pet:
    """A pet and the care tasks it needs."""

    name: str
    species: str
    tasks: list[Task] = field(default_factory=list)

    def add_task(self, task: Task) -> None:
        """Add a care task to this pet and tag it with the pet's name."""
        task.pet_name = self.name
        self.tasks.append(task)

    def get_tasks(self) -> list[Task]:
        """Return this pet's tasks."""
        return list(self.tasks)


class Owner:
    """A pet owner who manages one or more pets."""

    def __init__(self, name: str, available_minutes: int):
        self.name = name
        self.available_minutes = available_minutes
        self.pets: list[Pet] = []

    def add_pet(self, pet: Pet) -> None:
        """Add a pet to this owner."""
        self.pets.append(pet)

    def get_all_tasks(self) -> list[Task]:
        """Return every task across all of this owner's pets."""
        all_tasks = []
        for pet in self.pets:
            all_tasks.extend(pet.get_tasks())
        return all_tasks


class Scheduler:
    """Builds a daily care plan from an owner's pets and tasks."""

    def __init__(self, owner: Owner):
        self.owner = owner

    def generate_schedule(self) -> list[Task]:
        """Pick pending tasks by priority that fit the owner's time, ordered by time."""
        pending = self.filter_by_status(completed=False)
        by_priority = sorted(
            pending,
            key=lambda t: (-PRIORITY_ORDER.get(t.priority, 0), t.duration_minutes),
        )
        chosen, minutes_used = [], 0
        for task in by_priority:
            if minutes_used + task.duration_minutes <= self.owner.available_minutes:
                chosen.append(task)
                minutes_used += task.duration_minutes
        return sorted(chosen, key=lambda t: (t.time == "", t.time))

    def sort_by_time(self) -> list[Task]:
        """Return all tasks sorted by time, with untimed tasks last."""
        return sorted(
            self.owner.get_all_tasks(), key=lambda t: (t.time == "", t.time)
        )

    def filter_by_status(self, completed: bool) -> list[Task]:
        """Return tasks that match the given completion status."""
        return [t for t in self.owner.get_all_tasks() if t.completed == completed]

    def detect_conflicts(self) -> list[str]:
        """Return warning messages for tasks scheduled at the same time."""
        pass

    def mark_task_complete(self, task: Task) -> None:
        """Complete a task and create the next one if it repeats."""
        pass

    def explain_plan(self) -> str:
        """Explain why the schedule was built the way it was."""
        scheduled = self.generate_schedule()
        pending = self.filter_by_status(completed=False)
        minutes = sum(t.duration_minutes for t in scheduled)
        return (
            f"Scheduled {len(scheduled)} of {len(pending)} pending tasks "
            f"({minutes}/{self.owner.available_minutes} minutes). "
            "Higher-priority tasks are chosen first, then shorter ones, "
            "until the owner's time runs out."
        )