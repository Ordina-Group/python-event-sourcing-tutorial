# Exercise 1 [Start game]

- **Length:** 20-30 minutes 

---

## 1.1. Preparation

Switch to the branch `01-exercise-start-game`.

<br>

---

## 1.2. Initializing the aggregate

1. Open the file `src/connect_four/domain/game.py`. This file contains a stub of
   the `Game` aggregate that is the model for a game of Connect Four. 


2. Write an `__init__`-method for the `Game` aggregate that sets two attributes,
   `player_one` and `player_two`. As the game has not started yet, you don't
   have player names yet. Assign a reasonable default that indicates the absence
   of a value (i.e., don't introduce parameters for the player names).

*Note: You may or may not like this design decision, but it's made for
educational purposes. (Isn't it nice how easy it is to rationalise design
decisions?)* 

<br>

---

## 1.3. Starting a game with two players

To start a `Game`, the class needs to support the "Start Game"-command.

1. Add a method, `start_game`, that starts a game by assigning the names of the
   two players to the relevant attributes initialized in `__init__`.

<br>

---

## 1.4. An eventful state of being

You may have noticed that we're currently still relying on state. This is not
what we want in an event-sourced system. Instead of manipulating state, we want
to record events.

1. Add an attribute, `events`, to the `Game` class that will hold the events of
   the game in a list. Think of a place to initialize this attribute with a
   reasonable "empty" value.

<br>

---

## 1.5. Not only elephants have memory

Now that we have a list to store the events, we want to "emit" and track a
`GameStarted`-event instead of manipulating state.

1. Remove the assignment of players names in the `game_started`-method. That's
   right, we're not going to simply manipulate the `Game`-state.


2. Open `src/connect_four/domain/events.py` and look at the stub for the
   `GameStarted` event.


3. We still need to keep track of the player names in *some* way. (You did
   remove the attribute assignment in `start_game`, right?) The key insight here 
   is that the information is associated with the event: *We are starting a game 
   between two specific players.*

   This means that the only way to keep track of the player names is by
   attaching the relevant information to the event. Add two attributes to the
   `GameStarted`-event that allow us to track the player names.


4. Now go back to the `start_game`-method and ensure that it instantiates a
   `GameStarted`-event containing the right information. Append it to `events`
   list you added above to ensure that don't forget about this event!

<br>

---

## 1.6. Those who remember the past are able to repeat it 

Congratulations, you've successfully persisted your information in an event
instead of the state of the object. However, it's still very handy to have easy
access to the current state while the `Game`-object is in memory. This is why we
want to *apply* the event to the `Game` state.

1. Write an `apply`-method that applies the `GameStarted` event to the `Game`
   instance. In this case, this means that we want to assign the names of the
   players stored in the event to the relevant attributes of the `Game`
   instance.

2. Call the `apply`-method from the end of the `start_game`-method to ensure
   that this command has the expected effect on the game state. If you don't,
   the event history and the game state will be out-of-sync...

The steps above may feel a bit weird, but if you think about it, the state of
the `Game` now reflects that the event has happened. Moreover, if you were to
persist the **event** (not the state of the `Game`!), you can now use this
`apply`-method on a "fresh" instance of `Game` to recreate a `Game`-instance
with the exact same state as you have right now.

This is the magic of Event Sourcing: You *replay the events* to recreate the
state of the aggregate rather than persisting the state itself.

<br>

---

## Bonus exercise: Constraints are the best thing since sliced bread

What should happen if you issue a `start_game`-command for the second time on
the same game? Implement a solution for this potential problem.

Hint: Can you think of a *constraint* that would prevent a second command from
creating a second `GameStarted`-event?

<br><br>

---

<p align="center">
   <a href="/README.md">⬅️ Back to the README</a> | <a href="/exercises/exercise-02-play-the-game.md">Continue to exercise 2 ➡️</a>
</p>
