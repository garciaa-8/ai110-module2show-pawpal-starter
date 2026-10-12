from __future__ import annotations

from dataclasses import dataclass, field
from datetime import date, datetime
from enum import Enum
from typing import Optional


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


@dataclass
class Pet:
	name: str
	species: str
	birth_date: date
	tasks: list[Task] = field(default_factory=list)

	def add_task(self, task: Task) -> None:
		pass

	def get_tasks(self) -> list[Task]:
		pass


@dataclass
class CareEvent:
	event_id: str
	scheduled_at: datetime
	task: Task
	pet: Pet
	status: EventStatus = EventStatus.SCHEDULED
	completed_at: Optional[datetime] = None

	def reschedule(self, date_time: datetime) -> None:
		pass

	def mark_complete(self) -> None:
		pass


@dataclass
class Scheduler:
	events: list[CareEvent] = field(default_factory=list)

	def schedule(self, task: Task, pet: Pet, date_time: datetime) -> CareEvent:
		pass

	def reschedule(self, event_id: str, date_time: datetime) -> None:
		pass

	def get_upcoming_events(self, owner_id: str) -> list[CareEvent]:
		pass

	def get_event_history(self, owner_id: str) -> list[CareEvent]:
		pass


@dataclass
class Owner:
	name: str
	pets: list[Pet] = field(default_factory=list)

	def add_pet(self, pet: Pet) -> None:
		pass

	def schedule_event(
		self, pet: Pet, task: Task, date_time: datetime
	) -> CareEvent:
		pass

	def complete_event(self, event_id: str) -> None:
		pass

	def view_event_history(self) -> list[CareEvent]:
		pass
