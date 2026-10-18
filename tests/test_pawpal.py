from datetime import date, timedelta

from pawpal_system import Owner, Pet, Scheduler, Task


def make_scheduler(available_minutes: int = 120):
    """Build an owner with two pets and return (owner, rex, luna, scheduler)."""
    owner = Owner("Test", available_minutes=available_minutes)
    rex = Pet("Rex", "dog")
    luna = Pet("Luna", "cat")
    owner.add_pet(rex)
    owner.add_pet(luna)
    return owner, rex, luna, Scheduler(owner)


# ------------------------------------------------------------ basics
def test_mark_complete_changes_status():
    task = Task("Walk", 20)
    assert task.completed is False
    task.mark_complete()
    assert task.completed is True


def test_add_task_increases_task_count():
    pet = Pet("Rex", "dog")
    assert len(pet.get_tasks()) == 0
    pet.add_task(Task("Walk", 20))
    assert len(pet.get_tasks()) == 1


# ----------------------------------------------------------- sorting
def test_sort_by_time_returns_chronological_order():
    _, rex, luna, scheduler = make_scheduler()
    rex.add_task(Task("Evening play", 20, time="18:00"))
    rex.add_task(Task("Morning walk", 30, time="07:30"))
    luna.add_task(Task("Breakfast", 10, time="08:00"))

    times = [t.time for t in scheduler.sort_by_time()]
    assert times == ["07:30", "08:00", "18:00"]


def test_sort_by_time_puts_untimed_tasks_last():
    _, rex, _, scheduler = make_scheduler()
    rex.add_task(Task("No time set", 10))
    rex.add_task(Task("Morning walk", 30, time="07:30"))

    titles = [t.title for t in scheduler.sort_by_time()]
    assert titles == ["Morning walk", "No time set"]


# -------------------------------------------------------- recurrence
def test_daily_task_creates_next_day_task_when_completed():
    _, rex, _, scheduler = make_scheduler()
    walk = Task("Walk", 30, time="07:30", frequency="daily")
    rex.add_task(walk)

    new_task = scheduler.mark_task_complete(walk)

    assert walk.completed is True
    assert new_task is not None
    assert new_task.completed is False
    assert new_task.due_date == date.today() + timedelta(days=1)
    assert new_task.pet_name == "Rex"
    assert len(rex.get_tasks()) == 2


def test_weekly_task_creates_task_seven_days_later():
    _, rex, _, scheduler = make_scheduler()
    bath = Task("Bath", 25, frequency="weekly")
    rex.add_task(bath)

    new_task = scheduler.mark_task_complete(bath)

    assert new_task.due_date == date.today() + timedelta(days=7)


def test_one_time_task_does_not_repeat():
    _, rex, _, scheduler = make_scheduler()
    vet = Task("Vet visit", 60, frequency="once")
    rex.add_task(vet)

    assert scheduler.mark_task_complete(vet) is None
    assert len(rex.get_tasks()) == 1


# --------------------------------------------------------- conflicts
def test_detect_conflicts_flags_duplicate_times():
    _, rex, luna, scheduler = make_scheduler()
    rex.add_task(Task("Medicine", 5, time="08:00"))
    luna.add_task(Task("Breakfast", 10, time="08:00"))

    warnings = scheduler.detect_conflicts()

    assert len(warnings) == 1
    assert "08:00" in warnings[0]


def test_detect_conflicts_returns_nothing_for_different_times():
    _, rex, luna, scheduler = make_scheduler()
    rex.add_task(Task("Medicine", 5, time="08:00"))
    luna.add_task(Task("Breakfast", 10, time="08:30"))

    assert scheduler.detect_conflicts() == []


def test_completed_tasks_are_not_flagged_as_conflicts():
    _, rex, luna, scheduler = make_scheduler()
    done = Task("Medicine", 5, time="08:00")
    rex.add_task(done)
    luna.add_task(Task("Breakfast", 10, time="08:00"))
    done.mark_complete()

    assert scheduler.detect_conflicts() == []


# -------------------------------------------------- filtering / edges
def test_filter_by_pet_returns_only_that_pets_tasks():
    _, rex, luna, scheduler = make_scheduler()
    rex.add_task(Task("Walk", 30))
    luna.add_task(Task("Feed", 10))

    result = scheduler.filter_by_pet("Rex")

    assert [t.title for t in result] == ["Walk"]


def test_filter_by_status_separates_completed_and_pending():
    _, rex, _, scheduler = make_scheduler()
    done = Task("Walk", 30)
    rex.add_task(done)
    rex.add_task(Task("Feed", 10))
    done.mark_complete()

    assert [t.title for t in scheduler.filter_by_status(completed=True)] == ["Walk"]
    assert [t.title for t in scheduler.filter_by_status(completed=False)] == ["Feed"]


def test_pet_with_no_tasks_and_owner_with_no_pets():
    empty_owner = Owner("Nobody", available_minutes=60)
    scheduler = Scheduler(empty_owner)

    assert empty_owner.get_all_tasks() == []
    assert scheduler.generate_schedule() == []
    assert scheduler.sort_by_time() == []
    assert scheduler.detect_conflicts() == []


def test_schedule_respects_available_time_and_priority():
    _, rex, _, scheduler = make_scheduler(available_minutes=30)
    rex.add_task(Task("High", 20, priority="high", time="07:00"))
    rex.add_task(Task("Medium", 20, priority="medium", time="08:00"))
    rex.add_task(Task("Low", 10, priority="low", time="09:00"))

    titles = [t.title for t in scheduler.generate_schedule()]

    # High (20) fits, Medium (20) would exceed 30 minutes, Low (10) still fits.
    assert titles == ["High", "Low"]