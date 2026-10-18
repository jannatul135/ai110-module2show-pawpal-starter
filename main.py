"""Demo script: run with `python main.py` to see PawPal+ in the terminal."""

from pawpal_system import Owner, Pet, Scheduler, Task


def print_tasks(title: str, tasks: list[Task]) -> None:
    """Print a list of tasks as a readable table."""
    print(f"\n{title}")
    print(f"{'Time':<7}{'Pet':<9}{'Task':<20}{'Min':<5}{'Priority':<10}{'Due'}")
    print("-" * 62)
    for t in tasks:
        print(
            f"{t.time or '--:--':<7}{t.pet_name:<9}{t.title:<20}"
            f"{t.duration_minutes:<5}{t.priority:<10}{t.due_date}"
        )


def main() -> None:
    owner = Owner("Jannatul", available_minutes=90)
    rex = Pet("Rex", "dog")
    luna = Pet("Luna", "cat")
    owner.add_pet(rex)
    owner.add_pet(luna)

    # Tasks are added OUT OF ORDER on purpose; two share the 08:00 slot.
    play = Task("Play time", 20, priority="low", time="18:00")
    walk = Task("Morning walk", 30, priority="high", time="07:30", frequency="daily")
    medicine = Task("Give medicine", 5, priority="high", time="08:00")
    breakfast = Task("Feed breakfast", 10, priority="medium", time="08:00", frequency="daily")
    rex.add_task(play)
    rex.add_task(walk)
    rex.add_task(medicine)
    luna.add_task(breakfast)

    scheduler = Scheduler(owner)

    print_tasks("Today's Schedule", scheduler.generate_schedule())
    print("\n" + scheduler.explain_plan())

    print_tasks("All tasks sorted by time", scheduler.sort_by_time())
    print_tasks("Filter: Rex's tasks only", scheduler.filter_by_pet("Rex"))

    print("\nConflict check:")
    for warning in scheduler.detect_conflicts() or ["No conflicts found."]:
        print(f"  WARNING: {warning}")

    print("\nCompleting 'Morning walk' (repeats daily)...")
    next_task = scheduler.mark_task_complete(walk)
    print(f"  New task created for {next_task.due_date}: {next_task.title}")
    print_tasks("Filter: completed tasks", scheduler.filter_by_status(completed=True))
    print_tasks("Filter: pending tasks", scheduler.filter_by_status(completed=False))


if __name__ == "__main__":
    main()