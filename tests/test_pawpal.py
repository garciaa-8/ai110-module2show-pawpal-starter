from datetime import date, datetime, timedelta

import pytest

from pawpal_system import Owner, Pet, Scheduler, Task


def test_task_mark_complete_updates_completion_status() -> None:
	task = Task(
		name="Medication",
		description="Give the morning dose",
		duration_minutes=5,
		frequency="daily",
		priority="high",
	)

	assert task.is_completed is False

	task.mark_complete()

	assert task.is_completed is True


def test_adding_task_increases_pet_task_count() -> None:
	pet = Pet(name="Milo", species="Cat", birth_date=date(2020, 1, 1))
	task = Task(
		name="Feeding",
		description="Serve breakfast",
		duration_minutes=10,
		frequency="daily",
		priority="high",
	)

	assert len(pet.get_tasks()) == 0

	pet.add_task(task)

	assert len(pet.get_tasks()) == 1
	assert pet.get_tasks()[0] is task


def test_scheduler_filters_tasks_by_status_and_pet_name() -> None:
	scheduler = Scheduler()
	owner = Owner(name="Jordan", scheduler=scheduler)
	miso = Pet(name="Miso", species="Cat", birth_date=date(2022, 1, 1))
	bailey = Pet(name="Bailey", species="Dog", birth_date=date(2021, 1, 1))
	owner.add_pet(miso)
	owner.add_pet(bailey)

	miso_pending = Task("Feeding", "Feed Miso", 10, "daily", "high")
	miso_completed = Task("Medication", "Dose Miso", 5, "daily", "high")
	bailey_completed = Task("Walk", "Walk Bailey", 30, "daily", "medium")
	miso.add_task(miso_pending)
	miso.add_task(miso_completed)
	bailey.add_task(bailey_completed)
	miso_completed.mark_complete()
	bailey_completed.mark_complete()

	assert scheduler.filter_tasks(owner, completed=True) == [
		miso_completed,
		bailey_completed,
	]
	assert scheduler.filter_tasks(owner, pet_name="mISO") == [
		miso_pending,
		miso_completed,
	]
	assert scheduler.filter_tasks(
		owner, completed=True, pet_name="Miso"
	) == [miso_completed]


@pytest.mark.parametrize(
	("frequency", "interval"),
	[("daily", timedelta(days=1)), ("weekly", timedelta(weeks=1))],
)
def test_completing_recurring_event_schedules_next_instance(
	frequency: str, interval: timedelta
) -> None:
	scheduler = Scheduler()
	owner = Owner(name="Jordan", scheduler=scheduler)
	pet = Pet(name="Miso", species="Cat", birth_date=date(2022, 1, 1))
	owner.add_pet(pet)
	task = Task("Medication", "Give a dose", 5, frequency, "high")
	pet.add_task(task)
	scheduled_at = datetime(2026, 10, 11, 8, 0)
	event = owner.schedule_event(pet, task, scheduled_at)

	owner.complete_event(event.event_id)

	assert task.is_completed is True
	assert len(pet.tasks) == 2
	next_task = pet.tasks[1]
	assert next_task is not task
	assert next_task.is_completed is False
	assert len(scheduler.events) == 2
	next_event = scheduler.events[1]
	assert next_event.task is next_task
	assert next_event.scheduled_at == scheduled_at + interval


def test_scheduler_finds_same_pet_and_cross_pet_time_conflicts() -> None:
	scheduler = Scheduler()
	owner = Owner(name="Jordan", scheduler=scheduler)
	bailey = Pet(name="Bailey", species="Dog", birth_date=date(2021, 1, 1))
	miso = Pet(name="Miso", species="Cat", birth_date=date(2022, 1, 1))
	owner.add_pet(bailey)
	owner.add_pet(miso)
	start = datetime(2026, 10, 12, 8, 0)

	def add_scheduled_task(
		pet: Pet, name: str, duration: int, start_time: datetime
	) -> None:
		task = Task(name, name, duration, "once", "medium")
		pet.add_task(task)
		owner.schedule_event(pet, task, start_time)

	add_scheduled_task(bailey, "Walk", 30, start)
	add_scheduled_task(bailey, "Grooming", 10, start + timedelta(minutes=15))
	add_scheduled_task(miso, "Feeding", 20, start + timedelta(hours=1))
	add_scheduled_task(bailey, "Medication", 10, start + timedelta(hours=1))
	add_scheduled_task(bailey, "Training", 10, start + timedelta(minutes=30))

	conflicts = scheduler.find_conflicts()
	conflicting_names = {
		frozenset((first.task.name, second.task.name))
		for first, second in conflicts
	}

	assert conflicting_names == {
		frozenset(("Walk", "Grooming")),
		frozenset(("Feeding", "Medication")),
	}


def test_conflict_warning_returns_message_without_raising() -> None:
	scheduler = Scheduler()
	owner = Owner(name="Jordan", scheduler=scheduler)
	pet = Pet(name="Miso", species="Cat", birth_date=date(2022, 1, 1))
	owner.add_pet(pet)
	start = datetime(2026, 10, 12, 8, 0)

	first_task = Task("Feeding", "Feed Miso", 20, "once", "high")
	pet.add_task(first_task)
	owner.schedule_event(pet, first_task, start)

	second_task = Task("Medication", "Dose Miso", 10, "once", "high")
	pet.add_task(second_task)
	second_event = owner.schedule_event(
		pet, second_task, start + timedelta(minutes=5)
	)

	warning = scheduler.get_conflict_warning(second_event)

	assert warning == (
		"Schedule conflict: Medication for Miso overlaps with Feeding for Miso."
	)
	assert scheduler.get_conflict_warning(scheduler.events[0]) is not None
