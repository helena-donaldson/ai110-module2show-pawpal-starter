# PawPal+ Project Reflection

## 1. System Design

Three core actions:
- The user should be able to view the daily plan created by the app.
- The user should be able to add and edit pet care tasks
- The user should be able to enter information about the pet and the pet owner.

**a. Initial design**

- Briefly describe your initial UML design.
- What classes did you include, and what responsibilities did you assign to each?

My inital UML design included four classes: Owner, Pet, Plan, and Task. Plan controls much of the business logic; it generates the schedules based off its given task and a particular owner. Pet, Plan, and Owner mainly hold data with associated getters and setters methods. I included my brainstorming notes below to further elaborate on the responsibilities I assigned to everything.

Brainstorming:
Owner
- Attributes: Times availabe, Preferences, List of Pets
- Methods: Getters & Setters for all attributes
Pet
- Attribute: Name
- Methods: Getter & Setter for attribute
Plan
- Attributes: Owner, List of Tasks, Schedule (a string document)
- Methods: Add task, generate Schedule, Edit task

Task
- Attributes: Duration and Priority and name
- Methods: Getters & Setters for all attributes

**b. Design changes**

- Did your design change during implementation?
- If yes, describe at least one change and why you made it.

Yes, I did. I chaned the Task class by adding the attribute pet. This allows the relationship between what task to be associated with what pet to be more clear, as it is possible that there could be two grooming tasks but for two different dogs (for example).

---

## 2. Scheduling Logic and Tradeoffs

**a. Constraints and priorities**

- What constraints does your scheduler consider (for example: time, priority, preferences)?
- How did you decide which constraints mattered most?

My scheduler considers first (therefore mattering the most) the time at which the events occur- writing a message on the screen if two tasks have the same time. I feel like time is the most important factor because owners can't do two events at once, so it is the most limiting factor of what is available. It still considers priority and duration though, as secondary factors.

**b. Tradeoffs**

- Describe one tradeoff your scheduler makes.
- Why is that tradeoff reasonable for this scenario?

A tradeoff my scheduler makes is that it only considers preferences for short vs long tasks, that way it is more quanitifiable over what tasks should be preferenced vs. what should not be. It is a reasonable tradeoff because we were never give requirements specifically about what kind of preferences of owners we should take into account.

---

## 3. AI Collaboration

**a. How you used AI**

- How did you use AI tools during this project (for example: design brainstorming, debugging, refactoring)?
- What kinds of prompts or questions were most helpful?

I used AI for this project by helping design the plant uml,  generate test cases, and produce boiler plate code and beginning implementations. Prompts that were most helpful were prompts that were explicit with the requirements and that prompted it on what context to consider.

**b. Judgment and verification**

- Describe one moment where you did not accept an AI suggestion as-is.
- How did you evaluate or verify what the AI suggested?

So, when implementing schedule generation, the AI's first suggestion was inaccurate. It said that it considered task priority when it actually never did in the code. I evaluated the code by rereading the lines, and then when I prompted it to regenerate it with a consideration of priority, I re-traced it to ensure accuracy.

---

## 4. Testing and Verification

**a. What you tested**

- What behaviors did you test?
- Why were these tests important?

I tested that my sorting logic, recurring tasks, and conflict detection logic all occurred properly. These tests were important because they were
essential parts of the logic that allowed for the generation of the schedule, which is the essential feature of the application.

**b. Confidence**

- How confident are you that your scheduler works correctly?
- What edge cases would you test next if you had more time?

My confidence is a 4/5, with 5 being the highest, that the scheduler works correctly. If I had more time, I would add more edge cases that mix
priorities, overlapping times, and recurrences so that I was sure that there were no instances that the logic would break the scheduling algorithm.

---

## 5. Reflection

**a. What went well**

- What part of this project are you most satisfied with?

I am satisfied with the implementation of the sorting algorithm and the generation of schedules. I believe these were accomplished with flexibility, so the implementations could be added on to in the future.

**b. What you would improve**

- If you had another iteration, what would you improve or redesign?

I feel like the UI could be structured better- it is very long, and just one page, so the user has to scroll down a lot to accomplish all of the tasks. Instead, I would add separate pages for some of the tasks which I think is more intuitive.

**c. Key takeaway**

- What is one important thing you learned about designing systems or working with AI on this project?

I learned about the importance of verification. Sometimes the AI says that it accomplished something when it didn't. It is essential to be the human in the loop to verify accuracy and that the requirements are being met!
