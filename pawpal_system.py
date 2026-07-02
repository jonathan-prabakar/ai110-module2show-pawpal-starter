"""PawPal+ system skeleton.

Class stubs generated from diagrams/uml.mmd. Data-style objects (Owner,
Pet, Task) use dataclasses; Schedule holds the planning logic. Method
bodies are intentionally left unimplemented (raise NotImplementedError)
so the structure matches the UML before behavior is filled in.
"""

from __future__ import annotations

from dataclasses import dataclass, field


@dataclass
class Owner:
    """The person planning care, with their time budget and preferences."""

    name: str
    available_minutes: int = 0
    preferences: dict = field(default_factory=dict)

    def get_available_times(self) -> int:
        """Return the owner's available minutes for the day."""
        raise NotImplementedError

    def add_available_times(self, minutes: int) -> int:
        """Add to the owner's available time budget; return the new total."""
        raise NotImplementedError

    def set_preferences(self, prefs: dict) -> None:
        """Replace or update the owner's scheduling preferences."""
        raise NotImplementedError


@dataclass
class Pet:
    """A pet being cared for, with profile and special needs."""

    name: str
    species: str
    breed: str = ""
    age: int = 0
    special_needs: list = field(default_factory=list)

    def add_special_need(self, need: str) -> None:
        """Record a special care need for this pet."""
        raise NotImplementedError

    def get_profile(self) -> dict:
        """Return a summary profile of the pet."""
        raise NotImplementedError


@dataclass
class Task:
    """A single pet-care item that can be scheduled."""

    task_id: str
    name: str
    category: str = ""
    duration_minutes: int = 0
    priority: str = "medium"  # "low" | "medium" | "high"
    is_recurring: bool = False
    preferred_time: str = ""
    notes: str = ""

    def is_high_priority(self) -> bool:
        """Return True if this task is high priority."""
        raise NotImplementedError


@dataclass
class Schedule:
    """Builds and holds a day plan for one owner and pet."""

    date: str
    owner: Owner
    pet: Pet
    task_pool: list[Task] = field(default_factory=list)
    tasks: list[Task] = field(default_factory=list)

    def generate_plan(self) -> None:
        """Select and order tasks from the pool into the day plan."""
        raise NotImplementedError

    def sort_tasks(self) -> list[Task]:
        """Order tasks by priority (and any other constraints)."""
        raise NotImplementedError

    def filter_tasks(self) -> list[Task]:
        """Drop tasks that cannot or should not be scheduled."""
        raise NotImplementedError

    def explain_plan(self) -> str:
        """Return a human-readable explanation of why/when each task runs."""
        raise NotImplementedError

    def add_task(self, task: Task) -> None:
        """Add a task to the planned schedule."""
        raise NotImplementedError

    def remove_task(self, task_id: str) -> None:
        """Remove a task from the planned schedule by id."""
        raise NotImplementedError

    def get_total_duration(self) -> int:
        """Return the total minutes of all scheduled tasks."""
        raise NotImplementedError

    def is_within_budget(self) -> bool:
        """Return True if the plan fits the owner's available time."""
        raise NotImplementedError
