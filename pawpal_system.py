from __future__ import annotations

from dataclasses import dataclass, field
from datetime import date, datetime
from enum import Enum
from typing import Optional
from uuid import uuid4


class EventStatus(Enum):
	SCHEDULED = "scheduled"
	COMPLETED = "completed"
	SKIPPED = "skipped"


@dataclass
class Task:
	name: str
	description: str
	duration_minutes: int
	frequency: str
	priority: str
	is_completed: bool = False

	def mark_complete(self) -> None:
		"""Mark this task as completed."""
		self.is_completed = True


@dataclass
class Pet:
	name: str
	species: str
	birth_date: date
	tasks: list[Task] = field(default_factory=list)

	def add_task(self, task: Task) -> None:
		"""Add a task to this pet if it is not already present."""
		if not any(existing is task for existing in self.tasks):
			self.tasks.append(task)

	def get_tasks(self) -> list[Task]:
		"""Return this pet's tasks as a copy of its task list."""
		return list(self.tasks)


@dataclass
class CareEvent:
	event_id: str
	scheduled_at: datetime
	task: Task
	pet: Pet
	status: EventStatus = EventStatus.SCHEDULED
	completed_at: Optional[datetime] = None

	def reschedule(self, date_time: datetime) -> None:
		"""Move this event to a new scheduled date and time."""
		if self.status is not EventStatus.SCHEDULED:
			raise ValueError("Only scheduled events can be rescheduled")
		self.scheduled_at = date_time

	def mark_complete(self) -> None:
		"""Mark the event and its task complete and record the time."""
		if self.status is not EventStatus.SCHEDULED:
			raise ValueError("Only scheduled events can be completed")
		self.status = EventStatus.COMPLETED
		self.completed_at = datetime.now(tz=self.scheduled_at.tzinfo)
		self.task.mark_complete()


@dataclass
class Scheduler:
	events: list[CareEvent] = field(default_factory=list)

	def schedule(self, task: Task, pet: Pet, date_time: datetime) -> CareEvent:
		"""Create and store a scheduled event for a pet's task."""
		if not any(existing is task for existing in pet.tasks):
			raise ValueError("The task must belong to the pet before scheduling")
		event = CareEvent(
			event_id=str(uuid4()),
			scheduled_at=date_time,
			task=task,
			pet=pet,
		)
		self.events.append(event)
		return event

	def reschedule(self, event_id: str, date_time: datetime) -> None:
		"""Reschedule an event identified by its ID."""
		self._find_event(event_id).reschedule(date_time)

	def complete_event(
		self, event_id: str, owner: Optional[Owner] = None
	) -> None:
		"""Complete an event, optionally verifying its owner."""
		event = self._find_event(event_id)
		if owner is not None and not owner._owns_pet(event.pet):
			raise ValueError("The event does not belong to this owner")
		event.mark_complete()

	def get_upcoming_events(self, owner: Owner) -> list[CareEvent]:
		"""Return an owner's scheduled events in chronological order."""
		upcoming = [
			event
			for event in self.events
			if event.status is EventStatus.SCHEDULED
			and owner._owns_pet(event.pet)
			and event.scheduled_at >= datetime.now(tz=event.scheduled_at.tzinfo)
		]
		return sorted(upcoming, key=lambda event: event.scheduled_at)

	def get_event_history(self, owner: Owner) -> list[CareEvent]:
		"""Return an owner's completed or skipped events in date order."""
		history = [
			event
			for event in self.events
			if event.status is not EventStatus.SCHEDULED
			and owner._owns_pet(event.pet)
		]
		return sorted(
			history,
			key=lambda event: event.completed_at or event.scheduled_at,
		)

	def get_tasks(
		self, owner: Owner, include_completed: bool = True
	) -> list[Task]:
		"""Return an owner's tasks ordered by priority, duration, and name."""
		tasks = [
			task
			for pet in owner.pets
			for task in pet.tasks
			if include_completed or not task.is_completed
		]
		priority_order = {"high": 0, "medium": 1, "low": 2}
		return sorted(
			tasks,
			key=lambda task: (
				priority_order.get(task.priority.lower(), 3),
				task.duration_minutes,
				task.name.casefold(),
			),
		)

	def _find_event(self, event_id: str) -> CareEvent:
		"""Find an event by ID or raise a KeyError if absent."""
		for event in self.events:
			if event.event_id == event_id:
				return event
		raise KeyError(f"No care event found with id {event_id!r}")


@dataclass
class Owner:
	name: str
	scheduler: Scheduler
	pets: list[Pet] = field(default_factory=list)

	def add_pet(self, pet: Pet) -> None:
		"""Add a pet to this owner if it is not already present."""
		if not any(existing is pet for existing in self.pets):
			self.pets.append(pet)

	def get_all_tasks(self, include_completed: bool = True) -> list[Task]:
		"""Return this owner's tasks, optionally including completed ones."""
		return self.scheduler.get_tasks(self, include_completed)

	def schedule_event(
		self, pet: Pet, task: Task, date_time: datetime
	) -> CareEvent:
		"""Schedule a task for one of this owner's pets."""
		if not self._owns_pet(pet):
			raise ValueError("The pet must belong to this owner")
		return self.scheduler.schedule(task, pet, date_time)

	def complete_event(self, event_id: str) -> None:
		"""Complete one of this owner's scheduled events."""
		self.scheduler.complete_event(event_id, owner=self)

	def view_event_history(self) -> list[CareEvent]:
		"""Return this owner's event history."""
		return self.scheduler.get_event_history(self)

	def _owns_pet(self, pet: Pet) -> bool:
		"""Check whether this pet belongs to this owner."""
		return any(existing is pet for existing in self.pets)
