from datetime import date, datetime, time, timedelta

from pawpal_system import Owner, Pet, Scheduler, Task


def main() -> None:
	scheduler = Scheduler()
	owner = Owner(name="Jordan", scheduler=scheduler)

	bailey = Pet(
		name="Bailey",
		species="Dog",
		birth_date=date(2021, 4, 12),
	)
	miso = Pet(
		name="Miso",
		species="Cat",
		birth_date=date(2022, 9, 3),
	)
	owner.add_pet(bailey)
	owner.add_pet(miso)

	evening_medication = Task(
		name="Medication",
		description="Give Bailey evening medication",
		duration_minutes=5,
		frequency="daily",
		priority="high",
	)
	morning_walk = Task(
		name="Morning walk",
		description="Walk Bailey around the neighborhood",
		duration_minutes=30,
		frequency="daily",
		priority="medium",
	)
	cat_breakfast = Task(
		name="Breakfast",
		description="Feed Miso breakfast",
		duration_minutes=10,
		frequency="daily",
		priority="high",
	)

	# Add and schedule in a deliberately unsorted order.
	bailey.add_task(evening_medication)
	bailey.add_task(morning_walk)
	miso.add_task(cat_breakfast)
	tomorrow = date.today() + timedelta(days=1)
	medication_event = owner.schedule_event(
		bailey, evening_medication, datetime.combine(tomorrow, time(18, 0))
	)
	owner.schedule_event(
		bailey, morning_walk, datetime.combine(tomorrow, time(8, 0))
	)
	breakfast_event = owner.schedule_event(
		miso, cat_breakfast, datetime.combine(tomorrow, time(8, 0))
	)

	print("Tasks sorted by priority, duration, and name:")
	for task in owner.get_all_tasks():
		print(
			f"- {task.priority.title()}: {task.name} "
			f"({task.duration_minutes} min)"
		)

	print(f"\nUpcoming schedule for {tomorrow:%A, %B %d, %Y}:")
	for event in scheduler.get_upcoming_events(owner):
		print(
			f"- {event.scheduled_at:%I:%M %p}: {event.task.name} "
			f"for {event.pet.name}"
		)

	conflict_warning = scheduler.get_conflict_warning(breakfast_event)
	if conflict_warning:
		print(f"WARNING: {conflict_warning}")
	else:
		print("No schedule conflicts found.")

	owner.complete_event(medication_event.event_id)
	print("\nCompleted tasks:")
	for task in scheduler.filter_tasks(owner, completed=True):
		print(f"- {task.name}")

	print("\nTasks for Bailey:")
	for task in scheduler.filter_tasks(owner, pet_name="Bailey"):
		print(f"- {task.name} ({task.priority})")


if __name__ == "__main__":
	main()
