"""PawPal+ system skeleton.

Class stubs generated from diagrams/uml.mmd. Data-style objects (Owner,
Pet, Task) use dataclasses; Schedule holds the planning logic. Method
bodies are intentionally left unimplemented (raise NotImplementedError)
so the structure matches the UML before behavior is filled in.
"""

from __future__ import annotations

from dataclasses import dataclass, field, replace
from datetime import date, timedelta


@dataclass
class Owner:
    """The person planning care, with their time budget and preferences."""

    name: str
    available_minutes: int = 0
    preferences: dict = field(default_factory=dict)
    pets: list = field(default_factory=list)

    def add_pet(self, pet) -> None:
        """Register a pet under this owner."""
        self.pets.append(pet)

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
    tasks: list = field(default_factory=list)

    def add_task(self, task) -> None:
        """Attach a care task to this pet."""
        self.tasks.append(task)

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
    frequency: str = "none"  # "none" | "daily" | "weekly"
    due_date: str = ""  # ISO date "YYYY-MM-DD"
    preferred_time: str = ""
    notes: str = ""
    completed: bool = False

    _STEP = {"daily": 1, "weekly": 7}

    def is_high_priority(self) -> bool:
        """Return True if this task is high priority."""
        return self.priority.lower() == "high"

    def is_recurring_task(self) -> bool:
        """Return True if this task repeats on a daily/weekly cadence."""
        return self.frequency.lower() in self._STEP

    def next_occurrence(self) -> "Task | None":
        """Build the next instance of a recurring task, or None if one-off.

        The new task's due_date is advanced from this task's due_date (or
        today if unset) by timedelta(days=...) — 1 day for "daily", 7 for
        "weekly" — so the arithmetic rolls over months/years correctly.
        """
        step = self._STEP.get(self.frequency.lower())
        if step is None:
            return None
        base = date.fromisoformat(self.due_date) if self.due_date else date.today()
        next_due = base + timedelta(days=step)
        return replace(self, due_date=next_due.isoformat(), completed=False)

    def mark_complete(self) -> "Task | None":
        """Mark this task done; return the next occurrence if recurring."""
        self.completed = True
        return self.next_occurrence()


@dataclass
class Schedule:
    """Builds and holds a day plan for one owner and pet."""

    date: str
    owner: Owner
    pet: Pet
    task_pool: list[Task] = field(default_factory=list)
    tasks: list[Task] = field(default_factory=list)

    _RANK = {"high": 0, "medium": 1, "low": 2}

    def generate_plan(self) -> None:
        """Select and order tasks from the pool into the day plan."""
        self.tasks = self.filter_tasks()

    def sort_tasks(self) -> list[Task]:
        """Order tasks by priority, then preferred time."""
        return sorted(
            self.task_pool,
            key=lambda t: (self._RANK.get(t.priority.lower(), 1), t.preferred_time),
        )

    def filter_tasks(self) -> list[Task]:
        """Keep sorted tasks that fit the owner's time budget."""
        planned, used = [], 0
        for task in self.sort_tasks():
            if used + task.duration_minutes <= self.owner.available_minutes:
                planned.append(task)
                used += task.duration_minutes
        return planned

    def sort_by_time(self) -> list[Task]:
        """Return the pool ordered by preferred_time ("HH:MM").

        Uses sorted() with a lambda key that turns each "HH:MM" string into
        total minutes so times sort chronologically regardless of formatting.
        Tasks with no preferred_time are pushed to the end.
        """

        def to_minutes(task: Task) -> int:
            if not task.preferred_time or ":" not in task.preferred_time:
                return 24 * 60  # unscheduled -> end of day
            hours, minutes = task.preferred_time.split(":", 1)
            try:
                return int(hours) * 60 + int(minutes)
            except ValueError:
                return 24 * 60  # malformed time -> end of day

        return sorted(self.task_pool, key=to_minutes)

    def filter_by_completion(self, completed: bool = True) -> list[Task]:
        """Return pool tasks whose completed flag matches ``completed``."""
        return [t for t in self.task_pool if t.completed == completed]

    def filter_by_pet(self, pet_name: str) -> list[Task]:
        """Return pool tasks belonging to the pet named ``pet_name``.

        Tasks don't store their pet directly, so we match against the tasks
        registered on that pet's own list.
        """
        pet_task_ids = {t.task_id for t in self.pet.tasks if self.pet.name == pet_name}
        return [t for t in self.task_pool if t.task_id in pet_task_ids]

    def explain_plan(self) -> str:
        """Return a terminal-friendly summary of the day plan."""
        lines = [f"Today's Schedule ({self.date}) for {self.pet.name}:"]
        for task in self.tasks:
            lines.append(
                f"  {task.preferred_time or '--:--'}  {task.name}"
                f"  ({task.duration_minutes} min, {task.priority})"
            )
        lines.append(f"  Total: {self.get_total_duration()} min")
        return "\n".join(lines)

    def add_task(self, task: Task) -> None:
        """Add a task to the pool."""
        self.task_pool.append(task)

    def remove_task(self, task_id: str) -> None:
        """Remove a task from the pool by id."""
        self.task_pool = [t for t in self.task_pool if t.task_id != task_id]

    def mark_task_complete(self, task_id: str) -> Task | None:
        """Complete a pooled task; auto-add its next occurrence if recurring.

        Returns the newly created follow-up task, or None for one-off tasks
        or an unknown id.
        """
        for task in self.task_pool:
            if task.task_id == task_id:
                follow_up = task.mark_complete()
                if follow_up is not None:
                    follow_up.task_id = f"{task.task_id}-next"
                    self.task_pool.append(follow_up)
                return follow_up
        return None

    def detect_conflicts(self) -> list[str]:
        """Return warning strings for tasks sharing a preferred_time.

        Lightweight, non-crashing check: group scheduled tasks by their
        "HH:MM" slot and flag any slot holding more than one task. Tasks
        with no preferred_time are ignored (nothing to clash on).
        """
        by_slot: dict[str, list[Task]] = {}
        for task in self.tasks:
            if task.preferred_time:
                by_slot.setdefault(task.preferred_time, []).append(task)

        warnings = []
        for slot, tasks in sorted(by_slot.items()):
            if len(tasks) > 1:
                names = ", ".join(t.name for t in tasks)
                warnings.append(
                    f"⚠️  Conflict at {slot}: {len(tasks)} tasks overlap ({names})"
                )
        return warnings

    def get_total_duration(self) -> int:
        """Return the total minutes of all scheduled tasks."""
        return sum(t.duration_minutes for t in self.tasks)

    def is_within_budget(self) -> bool:
        """Return True if the plan fits the owner's available time."""
        return self.get_total_duration() <= self.owner.available_minutes
