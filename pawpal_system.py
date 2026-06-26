"""PawPal+ system skeleton.

Class stubs generated from diagrams/uml.mmd. Data-style objects use
dataclasses; the Scheduler holds the planning logic. Method bodies are
intentionally left unimplemented (raise NotImplementedError) so the
structure matches the UML before behavior is filled in.
"""

from __future__ import annotations

from dataclasses import dataclass, field
from datetime import date, time


@dataclass
class Task:
    """A single pet-care item to be scheduled."""

    title: str
    duration_minutes: int
    priority: str = "medium"  # "low" | "medium" | "high"
    completed: bool = False

    def priority_weight(self) -> int:
        """Convert the priority label into a sortable number."""
        raise NotImplementedError

    def mark_done(self) -> None:
        """Mark this task as completed."""
        raise NotImplementedError


@dataclass
class Pet:
    """A pet owned by an Owner, with its own care tasks."""

    name: str
    species: str
    tasks: list[Task] = field(default_factory=list)

    def add_task(self, task: Task) -> None:
        """Attach a care task to this pet."""
        raise NotImplementedError

    def daily_tasks(self) -> list[Task]:
        """Return the tasks that should be considered for today."""
        raise NotImplementedError


@dataclass
class Owner:
    """The person planning care for one or more pets."""

    name: str
    pets: list[Pet] = field(default_factory=list)
    preferences: dict = field(default_factory=dict)

    def add_pet(self, pet: Pet) -> None:
        """Register a pet under this owner."""
        raise NotImplementedError

    def list_pets(self) -> list[Pet]:
        """Return all pets owned."""
        raise NotImplementedError


@dataclass
class ScheduledTask:
    """A Task placed at a specific time slot, with an explanation."""

    task: Task
    start_time: time
    end_time: time
    reason: str = ""


@dataclass
class Schedule:
    """The produced plan for a single day."""

    day: date
    items: list[ScheduledTask] = field(default_factory=list)
    total_minutes: int = 0

    def add(self, task: Task, start: time) -> None:
        """Place a task into the schedule starting at the given time."""
        raise NotImplementedError

    def explain(self) -> str:
        """Return a human-readable explanation of why/when each task runs."""
        raise NotImplementedError


@dataclass
class Scheduler:
    """Turns a pet's tasks into an ordered daily Schedule."""

    available_minutes: int = 8 * 60
    priority_order: list[str] = field(
        default_factory=lambda: ["high", "medium", "low"]
    )

    def build_schedule(self, pet: Pet) -> Schedule:
        """Select and order a pet's tasks into a day plan."""
        raise NotImplementedError

    def sort_tasks(self, tasks: list[Task]) -> list[Task]:
        """Order tasks by priority (and any other constraints)."""
        raise NotImplementedError

    def fits(self, task: Task, used: int) -> bool:
        """Return True if the task fits within the remaining time budget."""
        raise NotImplementedError
