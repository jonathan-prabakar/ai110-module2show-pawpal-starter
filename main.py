"""Testing ground: build a small scenario and print today's schedule."""

from pawpal_system import Owner, Pet, Task, Schedule

owner = Owner(name="Jordan", available_minutes=120)

mochi = Pet(name="Mochi", species="dog", breed="Shiba", age=3)
luna = Pet(name="Luna", species="cat", breed="Tabby", age=5)

# Added intentionally out of order to prove the sorting works.
tasks = [
    Task("t4", "Evening play", "exercise", 20, "low", preferred_time="18:00"),
    Task("t2", "Feed breakfast", "feeding", 10, "high", preferred_time="08:30"),
    Task("t3", "Litter cleaning", "hygiene", 15, "medium", preferred_time="12:00"),
    Task("t1", "Morning walk", "exercise", 30, "high", preferred_time="08:00"),
    # Deliberately scheduled at 08:00, same as the morning walk, to trigger a conflict.
    Task("t5", "Give medication", "health", 5, "high", preferred_time="08:00"),
]

mochi.tasks = list(tasks)  # register tasks on the pet for filter_by_pet

schedule = Schedule(date="2026-07-02", owner=owner, pet=mochi)
for task in tasks:
    schedule.add_task(task)

# Mark one done so completion filtering has something to show.
schedule.task_pool[3].mark_complete()  # Morning walk

schedule.generate_plan()
print(schedule.explain_plan())
print(f"Within budget: {schedule.is_within_budget()}\n")

conflicts = schedule.detect_conflicts()
if conflicts:
    print("Schedule warnings:")
    for warning in conflicts:
        print(f"  {warning}")
else:
    print("No scheduling conflicts.")
print()

print("Sorted by time (HH:MM):")
for task in schedule.sort_by_time():
    print(f"  {task.preferred_time}  {task.name}")

print("\nCompleted tasks:")
for task in schedule.filter_by_completion(True):
    print(f"  {task.name}")

print("\nNot yet completed:")
for task in schedule.filter_by_completion(False):
    print(f"  {task.name}")

print(f"\nTasks for {mochi.name}:")
for task in schedule.filter_by_pet("Mochi"):
    print(f"  {task.name}")
