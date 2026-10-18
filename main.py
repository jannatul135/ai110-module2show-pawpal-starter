"""Demo script: run with `python main.py` to see PawPal+ in the terminal."""

from pawpal_system import Owner, Pet, Scheduler, Task


def print_schedule(scheduler: Scheduler) -> None:
    """Print today's schedule as a readable table."""
    print("=" * 52)
    print(f"  Today's Schedule for {scheduler.owner.name}")
    print("=" * 52)
    print(f"{'Time':<7}{'Pet':<9}{'Task':<20}{'Min':<5}{'Priority'}")
    print("-" * 52)
    for task in scheduler.generate_schedule():
        time = task.time or "--:--"
        print(
            f"{time:<7}{task.pet_name:<9}{task.title:<20}"
            f"{task.duration_minutes:<5}{task.priority}"
        )
    print("-" * 52)
    print(scheduler.explain_plan())


def main() -> None:
    owner = Owner("Jannatul", available_minutes=90)

    rex = Pet("Rex", "dog")
    luna = Pet("Luna", "cat")
    owner.add_pet(rex)
    owner.add_pet(luna)

    rex.add_task(Task("Morning walk", 30, priority="high", time="07:30", frequency="daily"))
    rex.add_task(Task("Give medicine", 5, priority="high", time="08:00"))
    luna.add_task(Task("Feed breakfast", 10, priority="medium", time="08:15", frequency="daily"))
    luna.add_task(Task("Play time", 20, priority="low", time="18:00"))

    print_schedule(Scheduler(owner))


if __name__ == "__main__":
    main()