"""PawPal+ core system: Task, Pet, Owner, and Scheduler classes."""

from dataclasses import dataclass, field


@dataclass
class Task:
    """A single pet care activity, like a walk or feeding."""

    title: str
    duration_minutes: int
    priority: str = "medium"
    time: str = ""
    frequency: str = "once"
    completed: bool = False

    def mark_complete(self) -> None:
        """Mark this task as completed."""
        pass


@dataclass
class Pet:
    """A pet and the care tasks it needs."""

    name: str
    species: str
    tasks: list[Task] = field(default_factory=list)

    def add_task(self, task: Task) -> None:
        """Add a care task to this pet."""
        pass

    def get_tasks(self) -> list[Task]:
        """Return this pet's tasks."""
        pass


class Owner:
    """A pet owner who manages one or more pets."""

    def __init__(self, name: str, available_minutes: int):
        self.name = name
        self.available_minutes = available_minutes
        self.pets: list[Pet] = []

    def add_pet(self, pet: Pet) -> None:
        """Add a pet to this owner."""
        pass

    def get_all_tasks(self) -> list[Task]:
        """Return every task across all of this owner's pets."""
        pass


class Scheduler:
    """Builds a daily care plan from an owner's pets and tasks."""

    def __init__(self, owner: Owner):
        self.owner = owner

    def generate_schedule(self) -> list[Task]:
        """Build a daily plan that fits the owner's available time."""
        pass

    def sort_by_time(self) -> list[Task]:
        """Return tasks sorted by their scheduled time."""
        pass

    def filter_by_status(self, completed: bool) -> list[Task]:
        """Return tasks that match the given completion status."""
        pass

    def explain_plan(self) -> str:
        """Explain why the schedule was built the way it was."""
        pass
