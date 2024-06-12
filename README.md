# Event Sourcing Workshop

A workshop Event Sourcing for an office day of the Ordina Pythoneers.

## Outline

- [13:00] Introduction to Event Sourcing, including some background on Domain Modeling/DDD
- [13:30] Modeling the Game Events: Guided (& Simplified) Event Storming
- [14:00] Intro Exercise 1
- [14:10] Exercise 1 [Start game]
- [14:50] Discussion Exercise 1 and intro Exercise 2
- [15:00] Exercise 2 [Play the game]
- [15:30] Discussion Exercise 2 and intro Exercise 3
- [15:40] Exercise 3 [Persisting the events]
- [16:10] Ending Discussion/Q&A
- [16:30] Drinks

## Introduction to Event Sourcing

- What is Event Sourcing?
- Why would you use it?
- State vs Events (including persistence)
- Domain Modeling/DDD
- Implementing the core instead of using a library
- Overview of workshop

## Modeling the Game Events

- What are we modeling?
- Short introduction to Event Storming
- Guided Event Storming session (using Connect 4 live game)
- Resulting events

## Intro Exercises

- Where to find the exercises
- What to expect in Exercise 1
- Check out branch `intro-exercise-1`

## Exercise 1 [Start game]

1. Switch to the branch `01-exercise-start-game`


2. Open the file `src/connect_four/domain/game.py`. This file contains a stub of
   the `Game` aggregate that is the model for a game of Connect Four. This is
   the class that will track the events of the game and will have methods for
   the commands related to the game.


   As a first step, write an `__init__`-method for the `Game` class that sets
   two attributes, `player_one` and `player_two` that will hold the names of
   the players. As the game hasn't started yet, we do not yet know the names of
   the players, so assign a sensible default value to these attributes.


3. To start a `Game`, the class needs to support the "Start Game"-command. Add
   a method, `start_game`, that starts a game by assigning the names of the two
   players to the relevant attributes.


4. You may have noticed that we're currently still manipulating state. This is
   not what we want in an event-sourced system. Instead of manipulating state,
   we want to record events. Add an attribute, `events`, to the `Game` class
   that will hold the events of the game in a list.


5. Now that we have a list to store the events, change the `start_game` command
   to append an event to the `events` list instead of assigning the player names
   directly.


   This means that you will also have to define a `GameStarted` event in
   `src/connect_four/domain/events.py`. As we don't store state anymore--you did
   remove the attribute assignment, right?--the only way to persist the names
   of the players is to ensure that the event contains this information. So,
   make sure that you store this as a part of the event.


6. Congratulations, you've successfully persisted your information in an event
   instead of the state of the object. However, it's still very handy to have
   easy access to the current state while the `Game`-object is in memory. This
   is why we want to *apply* the event to the `Game` state.


   Write an `apply`-method that applies the consequences of `GameStarted` event
   to the `Game` instance. In this case, this means that we want to assign the
   names of the players stored in the event to the relevant attributes of the
   `Game` instance.


   This may feel a bit weird, but if you think about it, the state of the `Game`
   now reflects the occurrence of the event. Moreover, if you were to persist
   the event, you can now use this `apply`-method on a fresh instance of `Game`
   to recreate a `Game` with the exact same state. You can *replay* the events
   to recreate the state of the aggregate.


   Don't forget to call the `apply`-method with the event at the end of the
   `start_game` command.

Bonus exercise:

7.  What should happen if you issue a `start_game`-command for the second time
    on the same game? Implement a solution for this potential problem.

    Hint: Can you think of a *constraint* that would prevent a second command
    from creating a second `GameStarted`-event?


## Discussion Exercise 1 and intro Exercise 2

- Show finished solution
- What to expect in Exercise 2
- Check out branch `exercise-2-play-game`

## Exercise 2 [Play the game]

- Application service to play a move
- How to handle end of the game

## Discussion Exercise 2 and intro Exercise 3

- Show finished solution
- What to expect in Exercise 3
- Check out branch `exercise-3-persist-events`

## Exercise 3 [Persisting the events]

- Event store
- Persisting events through repository
- Loading events from the event store

# Ending Discussion/Q&A
- When to use & when not to use
- CQRS
- Snapshots
- Mention existing packages for event sourcing in Python
- Q&A

# Running the Connect Four application on your local machine

## Application

The application uses Poetry as a package management tool.

Use the command `poetry shell` to create a python shell.

Use the command `poetry run pytest` to run all the tests in the application.

## Running Eventstore DB on your local machine

> :warning: **If you are using a Apple Silicon Macbook**: Read below!
>
EvenstoreDB can be run on your local machine, using the supplied [Docker Compose](compose.yaml) file.
If you have docker installed in your local machine, you can start the EventstoreDB with the command:

```shell
docker compose up eventstore.db
```

Visit http://localhost:2113/ to view the EventstoreDB.

### EventstoreDB on Apple Silicon

For the Apple Silicon, EventstoreDB provides a different container.
Please edit the `compose.yaml` file, and see the instructions in this file.
