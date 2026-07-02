"""Simple tests for PawPal+ core behavior."""

import os
import sys

sys.path.insert(0, os.path.dirname(os.path.dirname(__file__)))

from pawpal_system import Pet, Task


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