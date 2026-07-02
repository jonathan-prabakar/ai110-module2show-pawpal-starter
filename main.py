"""Testing ground: build a small scenario and print today's schedule."""

from pawpal_system import Owner, Pet, Task, Schedule

owner = Owner(name="Jordan", available_minutes=120)

mochi = Pet(name="Mochi", species="dog", breed="Shiba", age=3)
luna = Pet(name="Luna", species="cat", breed="Tabby", age=5)

tasks = [
    Task("t1", "Morning walk", "exercise", 30, "high", preferred_time="08:00"),
    Task("t2", "Feed breakfast", "feeding", 10, "high", preferred_time="08:30"),
    Task("t3", "Litter cleaning", "hygiene", 15, "medium", preferred_time="12:00"),
    Task("t4", "Evening play", "exercise", 20, "low", preferred_time="18:00"),
]

schedule = Schedule(date="2026-07-02", owner=owner, pet=mochi)
for task in tasks:
    schedule.add_task(task)

schedule.generate_plan()
print(schedule.explain_plan())
print(f"Within budget: {schedule.is_within_budget()}")
