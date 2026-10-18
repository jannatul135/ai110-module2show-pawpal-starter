"""PawPal+ core system: Task, Pet, Owner, and Scheduler classes."""

from dataclasses import dataclass, field, replace
from datetime import date, timedelta

PRIORITY_ORDER = {"high": 3, "medium": 2, "low": 1}
RECURRENCE_DAYS = {"daily": 1, "weekly": 7}  # NEW: days until the next occurrence


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
        """Return a copy of this pet's tasks."""
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

    def _due_today(self) -> list[Task]:
        """Return pending tasks due today or earlier."""
        return [
            t for t in self.filter_by_status(completed=False)
            if t.due_date <= date.today()
        ]

    def generate_schedule(self) -> list[Task]:
        """Pick pending tasks by priority that fit the owner's time, ordered by time."""
        by_priority = sorted(
            self._due_today(),
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

    def filter_by_pet(self, pet_name: str) -> list[Task]:  # NEW
        """Return tasks belonging to the pet with the given name."""
        return [
            t for t in self.owner.get_all_tasks()
            if t.pet_name.lower() == pet_name.lower()
        ]

    def detect_conflicts(self) -> list[str]:  # NEW
        """Return a warning for each time slot with more than one pending task."""
        slots: dict[tuple, list[Task]] = {}
        for task in self.filter_by_status(completed=False):
            if task.time:
                slots.setdefault((task.due_date, task.time), []).append(task)

        warnings = []
        for (due, time), tasks in sorted(slots.items()):
            if len(tasks) > 1:
                names = ", ".join(f"{t.pet_name}: {t.title}" for t in tasks)
                warnings.append(f"Conflict at {time} on {due}: {names}")
        return warnings

    def mark_task_complete(self, task: Task) -> Task | None:  # NEW
        """Complete a task; if it repeats, add the next occurrence to its pet."""
        task.mark_complete()
        days = RECURRENCE_DAYS.get(task.frequency)
        if days is None:
            return None
        next_task = replace(
            task, completed=False, due_date=task.due_date + timedelta(days=days)
        )
        for pet in self.owner.pets:
            if pet.name == task.pet_name:
                pet.add_task(next_task)
                return next_task
        return None

    def explain_plan(self) -> str:
        """Explain why the schedule was built the way it was."""
        scheduled = self.generate_schedule()
        pending = self._due_today()
        minutes = sum(t.duration_minutes for t in scheduled)
        return (
            f"Scheduled {len(scheduled)} of {len(pending)} pending tasks "
            f"({minutes}/{self.owner.available_minutes} minutes). "
            "Higher-priority tasks are chosen first, then shorter ones, "
            "until the owner's time runs out."
        )