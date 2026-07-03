"""Tests for PawPal+ core behavior: sorting, recurrence, conflicts, budget."""

import os
import sys
from datetime import date, timedelta

import pytest

sys.path.insert(0, os.path.dirname(os.path.dirname(__file__)))

from pawpal_system import Owner, Pet, Schedule, Task


# --------------------------------------------------------------------------- #
# Helpers
# --------------------------------------------------------------------------- #
def make_schedule(owner=None, pet=None, pool=None):
    owner = owner or Owner(name="Alex", available_minutes=120)
    pet = pet or Pet(name="Mochi", species="dog")
    sched = Schedule(date="2026-07-02", owner=owner, pet=pet)
    for t in pool or []:
        sched.add_task(t)
    return sched


# --------------------------------------------------------------------------- #
# Existing baseline
# --------------------------------------------------------------------------- #
def test_task_completion():
    task = Task("t1", "Morning walk", duration_minutes=30)
    assert task.completed is False
    task.mark_complete()
    assert task.completed is True


def test_task_addition_increases_count():
    pet = Pet(name="Mochi", species="dog")
    before = len(pet.tasks)
    pet.add_task(Task("t1", "Feed breakfast", duration_minutes=10))
    assert len(pet.tasks) == before + 1


# --------------------------------------------------------------------------- #
# Required core: sorting correctness (chronological order)
# --------------------------------------------------------------------------- #
def test_sort_by_time_chronological():
    pool = [
        Task("t1", "Evening walk", preferred_time="18:00"),
        Task("t2", "Breakfast", preferred_time="07:00"),
        Task("t3", "Lunch", preferred_time="12:30"),
    ]
    sched = make_schedule(pool=pool)
    ordered = [t.preferred_time for t in sched.sort_by_time()]
    assert ordered == ["07:00", "12:30", "18:00"]


# --------------------------------------------------------------------------- #
# Required core: recurrence logic (daily -> next day)
# --------------------------------------------------------------------------- #
def test_daily_recurrence_creates_next_day_task():
    task = Task(
        "t1", "Insulin shot",
        is_recurring=True, frequency="daily", due_date="2026-07-02",
    )
    follow_up = task.mark_complete()
    assert follow_up is not None
    assert follow_up.due_date == "2026-07-03"
    assert follow_up.completed is False
    assert task.completed is True


def test_mark_task_complete_appends_next_occurrence_to_pool():
    task = Task(
        "t1", "Insulin shot",
        is_recurring=True, frequency="daily", due_date="2026-07-02",
    )
    sched = make_schedule(pool=[task])
    follow_up = sched.mark_task_complete("t1")
    assert follow_up is not None
    assert follow_up.task_id == "t1-next"
    assert follow_up in sched.task_pool
    assert len(sched.task_pool) == 2


# --------------------------------------------------------------------------- #
# Required core: conflict detection (duplicate times)
# --------------------------------------------------------------------------- #
def test_detect_conflicts_flags_duplicate_times():
    a = Task("t1", "Walk", preferred_time="08:00")
    b = Task("t2", "Feed", preferred_time="08:00")
    sched = make_schedule()
    sched.tasks = [a, b]
    warnings = sched.detect_conflicts()
    assert len(warnings) == 1
    assert "08:00" in warnings[0]
    assert "Walk" in warnings[0] and "Feed" in warnings[0]


# --------------------------------------------------------------------------- #
# Additional happy paths
# --------------------------------------------------------------------------- #
def test_sort_tasks_by_priority():
    pool = [
        Task("t1", "Low", priority="low", preferred_time="09:00"),
        Task("t2", "High", priority="high", preferred_time="09:00"),
        Task("t3", "Medium", priority="medium", preferred_time="09:00"),
    ]
    sched = make_schedule(pool=pool)
    names = [t.name for t in sched.sort_tasks()]
    assert names == ["High", "Medium", "Low"]


def test_generate_plan_respects_budget():
    owner = Owner(name="Alex", available_minutes=45)
    pool = [
        Task("t1", "Walk", duration_minutes=30, priority="high"),
        Task("t2", "Groom", duration_minutes=30, priority="low"),
        Task("t3", "Feed", duration_minutes=10, priority="high"),
    ]
    sched = make_schedule(owner=owner, pool=pool)
    sched.generate_plan()
    ids = {t.task_id for t in sched.tasks}
    # High-priority walk (30) + feed (10) fit in 45; low groom (30) does not.
    assert ids == {"t1", "t3"}
    assert sched.is_within_budget()


# --------------------------------------------------------------------------- #
# Edge cases: empty / sparse data
# --------------------------------------------------------------------------- #
def test_empty_pool_no_crash():
    sched = make_schedule(pool=[])
    sched.generate_plan()
    assert sched.sort_tasks() == []
    assert sched.sort_by_time() == []
    assert sched.tasks == []
    assert sched.detect_conflicts() == []


def test_zero_budget_schedules_nothing():
    owner = Owner(name="Alex", available_minutes=0)
    pool = [Task("t1", "Walk", duration_minutes=30)]
    sched = make_schedule(owner=owner, pool=pool)
    sched.generate_plan()
    assert sched.tasks == []
    assert sched.is_within_budget() is True  # 0 <= 0


# --------------------------------------------------------------------------- #
# Edge cases: sorting boundaries
# --------------------------------------------------------------------------- #
def test_two_tasks_same_time_stable_and_flagged():
    a = Task("t1", "Walk", preferred_time="08:00")
    b = Task("t2", "Feed", preferred_time="08:00")
    sched = make_schedule(pool=[a, b])
    ordered = sched.sort_by_time()
    assert [t.task_id for t in ordered] == ["t1", "t2"]  # stable
    sched.tasks = ordered
    assert len(sched.detect_conflicts()) == 1


def test_sort_by_time_pushes_missing_time_to_end():
    pool = [
        Task("t1", "No time"),
        Task("t2", "Morning", preferred_time="07:00"),
    ]
    sched = make_schedule(pool=pool)
    assert [t.task_id for t in sched.sort_by_time()] == ["t2", "t1"]


def test_sort_by_time_accepts_single_digit_hour():
    pool = [
        Task("t1", "Late", preferred_time="7:30"),
        Task("t2", "Early", preferred_time="7:05"),
    ]
    sched = make_schedule(pool=pool)
    assert [t.task_id for t in sched.sort_by_time()] == ["t2", "t1"]


def test_sort_by_time_malformed_time_sorts_to_end():
    pool = [
        Task("t1", "Bad", preferred_time="8:00am"),
        Task("t2", "Good", preferred_time="07:00"),
    ]
    sched = make_schedule(pool=pool)
    # Malformed time is treated as end-of-day, so the valid task comes first.
    assert [t.task_id for t in sched.sort_by_time()] == ["t2", "t1"]


def test_unknown_priority_treated_as_medium():
    pool = [
        Task("t1", "Urgent", priority="urgent", preferred_time="09:00"),
        Task("t2", "High", priority="high", preferred_time="09:00"),
        Task("t3", "Low", priority="low", preferred_time="09:00"),
    ]
    sched = make_schedule(pool=pool)
    names = [t.name for t in sched.sort_tasks()]
    assert names == ["High", "Urgent", "Low"]  # urgent ranks as medium (1)


# --------------------------------------------------------------------------- #
# Edge cases: budget filtering
# --------------------------------------------------------------------------- #
def test_zero_duration_task_always_fits():
    owner = Owner(name="Alex", available_minutes=0)
    pool = [Task("t1", "Quick check", duration_minutes=0)]
    sched = make_schedule(owner=owner, pool=pool)
    sched.generate_plan()
    assert [t.task_id for t in sched.tasks] == ["t1"]


def test_task_exactly_equal_to_budget_included():
    owner = Owner(name="Alex", available_minutes=30)
    pool = [Task("t1", "Walk", duration_minutes=30)]
    sched = make_schedule(owner=owner, pool=pool)
    sched.generate_plan()
    assert [t.task_id for t in sched.tasks] == ["t1"]


def test_greedy_skip_lets_later_smaller_task_fit():
    owner = Owner(name="Alex", available_minutes=40)
    pool = [
        Task("t1", "Big", duration_minutes=50, priority="high"),
        Task("t2", "Small", duration_minutes=20, priority="high"),
    ]
    sched = make_schedule(owner=owner, pool=pool)
    sched.generate_plan()
    assert [t.task_id for t in sched.tasks] == ["t2"]


# --------------------------------------------------------------------------- #
# Edge cases: recurring tasks
# --------------------------------------------------------------------------- #
def test_one_off_task_has_no_next_occurrence():
    task = Task("t1", "Vet visit", frequency="none")
    assert task.next_occurrence() is None
    sched = make_schedule(pool=[task])
    assert sched.mark_task_complete("t1") is None
    assert len(sched.task_pool) == 1


def test_recurrence_without_due_date_uses_today():
    task = Task("t1", "Feed", is_recurring=True, frequency="daily")
    follow_up = task.next_occurrence()
    expected = (date.today() + timedelta(days=1)).isoformat()
    assert follow_up.due_date == expected


def test_weekly_recurrence_rolls_over_year():
    task = Task(
        "t1", "Bath", is_recurring=True, frequency="weekly",
        due_date="2026-12-31",
    )
    assert task.next_occurrence().due_date == "2027-01-07"


def test_double_completion_produces_chained_ids():
    task = Task(
        "t1", "Feed", is_recurring=True, frequency="daily",
        due_date="2026-07-02",
    )
    sched = make_schedule(pool=[task])
    first = sched.mark_task_complete("t1")
    assert first.task_id == "t1-next"
    second = sched.mark_task_complete("t1-next")
    assert second.task_id == "t1-next-next"
    ids = [t.task_id for t in sched.task_pool]
    assert ids == ["t1", "t1-next", "t1-next-next"]


def test_invalid_due_date_raises():
    task = Task(
        "t1", "Feed", is_recurring=True, frequency="daily",
        due_date="not-a-date",
    )
    with pytest.raises(ValueError):
        task.next_occurrence()


# --------------------------------------------------------------------------- #
# Edge cases: conflicts & filters
# --------------------------------------------------------------------------- #
def test_no_time_tasks_never_conflict():
    sched = make_schedule()
    sched.tasks = [Task("t1", "A"), Task("t2", "B")]
    assert sched.detect_conflicts() == []


def test_filter_by_pet_name_mismatch_returns_empty():
    pet = Pet(name="Mochi", species="dog")
    pet.add_task(Task("t1", "Walk"))
    sched = make_schedule(pet=pet, pool=[Task("t1", "Walk")])
    assert sched.filter_by_pet("Rex") == []
    assert [t.task_id for t in sched.filter_by_pet("Mochi")] == ["t1"]


def test_filter_by_completion_partitions():
    done = Task("t1", "Walk", completed=True)
    pending = Task("t2", "Feed", completed=False)
    sched = make_schedule(pool=[done, pending])
    assert [t.task_id for t in sched.filter_by_completion(True)] == ["t1"]
    assert [t.task_id for t in sched.filter_by_completion(False)] == ["t2"]
