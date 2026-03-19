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

**b. Tradeoffs**

- Describe one tradeoff your scheduler makes.
- Why is that tradeoff reasonable for this scenario?

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
