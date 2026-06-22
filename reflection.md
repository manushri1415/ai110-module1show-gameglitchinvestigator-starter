# 💭 Reflection: Game Glitch Investigator

Answer each question in 3 to 5 sentences. Be specific and honest about what actually happened while you worked. This is about your process, not trying to sound perfect.

## 1. What was broken when you started?

- What did the game look like the first time you ran it?
- List at least two concrete bugs you noticed at the start  
  (for example: "the hints were backwards").
  The hints were backwards
  Attempts left seems to be changing
  incorrect "Go higher", "Go Lower"
  "Game over. Start a new game to try again." when clicked "New Game"
  shows attempts left:1 but the hint says out of attempts
  Attempts left: -1 

**Bug Reproduction Log**

Document at least 3 bugs you found. Add rows as needed.

| Input         | Expected Behavior | Actual Behavior | Console Output / Error |
|-------        |-------------------|-----------------|------------------------|
|50|90 |96 |99 |  Go lower, Num= 17 | Go Higher!        NORMAL                             
|40 | 60|80 | 90| Go Lower, Num=13 | Go HIGHER!         EASY
|50 |40 | 20| | Go HIGHER! nUM= 74 | Go lower           HARD

---

## 2. How did you use AI as a teammate?

- Which AI tools did you use on this project (for example: ChatGPT, Gemini, Copilot)?
- Give one example of an AI suggestion that was correct (including what the AI suggested and how you verified the result).
- Give one example of an AI suggestion that was incorrect or misleading (including what the AI suggested and how you verified the result).

--- Used Claude  
--- One suggestion AI gave me was to penalize the scores for high and low similarly and also suggested to make it into a clean single code snippet.
I noticed that the initial code penalty for too high score so I just verified and approved it.

---- The AI seemed to added a "guess the number from..." block twice even though it was in the code. I had to suggest to remove it. not sure how it got that idea. it did mess up a lot of code and I had to revisit some changes. 

## 3. Debugging and testing your fixes

- How did you decide whether a bug was really fixed?
- Describe at least one test you ran (manual or using pytest)  
  and what it showed you about your code.
- Did AI help you design or understand any tests? How?

--- I used Pytest to test and I manually ran the test when I ran the application.
--- I tried all the levels "easy, normal, hard" to ensure I was able to get the right number of attempts and hints
--- AI helped me design edge cases to test a single fix me issue. 

## 4. What did you learn about Streamlit and state?

- How would you explain Streamlit "reruns" and session state to a friend who has never used Streamlit?

--- Stremlit reruns the each script and session state keeps the information in tact until session ends.

## 5. Looking ahead: your developer habits

- What is one habit or strategy from this project that you want to reuse in future labs or projects?
  - This could be a testing habit, a prompting strategy, or a way you used Git.
- What is one thing you would do differently next time you work with AI on a coding task?
- In one or two sentences, describe how this project changed the way you think about AI generated code.

--- Pytest. I am new to python and used to work on Java more and I was suprised we have  PyTest which i similar to Junit tests
--- I ran into some more issues after my initial fixes, next time I should go over the issues more deeper and get all the fixe comments before solving them
--- Sometimes AI can mess things up. It did change and bring up more issues that I didn't expect. 