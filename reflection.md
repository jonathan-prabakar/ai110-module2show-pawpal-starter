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
It considered priority, time budget, preferred time and recurrence. 
I decided on budget then priority then preferred time. Budget because it is the only real-life hard limit because if an owner can't spend more minutes than they have, it wouldn't be possible.


**b. Tradeoffs**
the detect_conflicts method only flags tasks that share the exact time and doesn't account for overlapping durations.
This tradeoff is reasonable because the exact-match check is lightweight string comparison that just returns warning messages instead of errors. Upgrading to true overlap detection is a local change that would be easy to implement. 


---

## 3. AI Collaboration

**a. How you used AI**

- How did you use AI tools during this project (for example: design brainstorming, debugging, refactoring)?
- What kinds of prompts or questions were most helpful?
  I used AI to write tests, functions, and create the skeleton of the app from the UMD that I had.

**b. Judgment and verification**

- Describe one moment where you did not accept an AI suggestion as-is.
- How did you evaluate or verify what the AI suggested?
There was a function that it redid which looked too Pythony. I compared the two functions and realized that the current function had less lines but still worked effectively and even inquired the AI about this.
---

## 4. Testing and Verification

**a. What you tested**

- What behaviors did you test? I tested empty data, sorting boundaries, budget filtering and recurring tasks
- Why were these tests important?
  I tested to confirm a completed daily task produced a next day task. A missing preferred time is sorted first but sort_by_time pushes it last

**b. Confidence**

- How confident are you that your scheduler works correctly?
- What edge cases would you test next if you had more time?
I'm confident that it works. I would provide AM or PM time and see how it would react
---

## 5. Reflection

**a. What went well**

- What part of this project are you most satisfied with?
I'm satisfied with the action flow of the app

**b. What you would improve**

- If you had another iteration, what would you improve or redesign?
  I would redesign the availability selection when entering the user

**c. Key takeaway**

- What is one important thing you learned about designing systems or working with AI on this project?
  I learned how to effectively go about creating an app from scratch to the UMD diagram to functions and testing edge cases