from datetime import date, datetime, time

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

	morning_walk = Task(
		name="Morning walk",
		description="Walk Bailey around the neighborhood",
		duration_minutes=30,
		frequency="daily",
		priority="high",
	)
	cat_breakfast = Task(
		name="Breakfast",
		description="Feed Miso breakfast",
		duration_minutes=10,
		frequency="daily",
		priority="high",
	)
	evening_medication = Task(
		name="Medication",
		description="Give Bailey evening medication",
		duration_minutes=5,
		frequency="daily",
		priority="high",
	)
	bailey.add_task(morning_walk)
	miso.add_task(cat_breakfast)
	bailey.add_task(evening_medication)

	today = date.today()
	owner.schedule_event(
		bailey, morning_walk, datetime.combine(today, time(8, 0))
	)
	owner.schedule_event(
		miso, cat_breakfast, datetime.combine(today, time(12, 0))
	)
	owner.schedule_event(
		bailey, evening_medication, datetime.combine(today, time(18, 0))
	)

	print(f"Today's Schedule - {today:%A, %B %d, %Y}")
	for event in sorted(scheduler.events, key=lambda item: item.scheduled_at):
		print(
			f"{event.scheduled_at:%I:%M %p} - {event.task.name} "
			f"for {event.pet.name} ({event.task.duration_minutes} min)"
		)


if __name__ == "__main__":
	main()
