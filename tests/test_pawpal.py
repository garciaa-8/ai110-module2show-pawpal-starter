from datetime import date

from pawpal_system import Pet, Task


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
