# PawPal+ Project Reflection

## 1. System Design

1. Produce daily plans
2. Be able to add pets and owner info
3. Generate availability display

Step 2: 

Owner class - 
pet class
schedule
scheduler

**a. Initial design**
- Briefly describe your initial UML design.
- What classes did you include, and what responsibilities did you assign to each?

The Design has 4 classes
    Owner- name, available mins, preferences
      - can get available mins, add available times, and set preferences
  - 
    Schedule: date, owner, pet, task_pool, tasks

    -Pet: name, species, breed, age, special_needs

    -Task: task_id, name, category, duration_minutes, priority, is_recurring, preferred_time, notes

  


**b. Design changes**

- Did your design change during implementation?
- If yes, describe at least one change and why you made it.

---

## 2. Scheduling Logic and Tradeoffs

**a. Constraints and priorities**

- What constraints does your scheduler consider (for example: time, priority, preferences)?
- How did you decide which constraints mattered most?

**b. Tradeoffs**

My `detect_conflicts()` method only flags tasks that share the **exact same
`preferred_time`** (for example two tasks both set to `08:00`). It does *not*
account for overlapping durations — a 30-minute walk starting at `08:00` and a
task at `08:15` genuinely collide in real life, but my scheduler treats them as
conflict-free because their start strings differ.

This tradeoff is reasonable for the scenario because:

- **Simplicity and safety.** The exact-match check is a lightweight string
  comparison that groups tasks by slot and returns warning messages instead of
  crashing. There is no time-math to get wrong.
- **Fits the input.** Owners enter round, human-friendly times (`08:00`,
  `12:00`), so exact collisions are the common real-world case.
- **Cheap to extend later.** All conflict logic lives in one method, so upgrading
  to true overlap detection (using each task's `duration_minutes` to compare time
  ranges) is a localized change if the need arises.

The cost is that near-miss overlaps go undetected, so the warning is a helpful
heads-up rather than a guarantee of a clash-free day.

---

## 3. AI Collaboration

**a. How you used AI**

- How did you use AI tools during this project (for example: design brainstorming, debugging, refactoring)?
- What kinds of prompts or questions were most helpful?

**b. Judgment and verification**

- Describe one moment where you did not accept an AI suggestion as-is.
- How did you evaluate or verify what the AI suggested?

---

## 4. Testing and Verification

**a. What you tested**

- What behaviors did you test?
- Why were these tests important?

**b. Confidence**

- How confident are you that your scheduler works correctly?
- What edge cases would you test next if you had more time?

---

## 5. Reflection

**a. What went well**

- What part of this project are you most satisfied with?

**b. What you would improve**

- If you had another iteration, what would you improve or redesign?

**c. Key takeaway**

- What is one important thing you learned about designing systems or working with AI on this project?
