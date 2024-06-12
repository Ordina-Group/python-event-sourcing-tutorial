# Event Sourcing Workshop

A workshop Event Sourcing for an office day of the Ordina Pythoneers.

## Outline

[13:00] Introduction to Event Sourcing, including some background on Domain Modeling/DDD
[13:30] Modeling the Game Events: Guided (& Simplified) Event Storming
[14:00] Intro Exercise 1
[14:10] Exercise 1 [Start game]
[14:50] Discussion Exercise 1 and intro Exercise 2
[15:00] Exercise 2 [Play the game]
[15:30] Discussion Exercise 2 and intro Exercise 3
[15:40] Exercise 3 [Persisting the events]
[16:10] Ending Discussion/Q&A
[16:30] Drinks

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

- Application service to start a game
- Aggregate root of the game
- Start a game through the application service

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

> :warning: **If you are using a Apple silicon Macbook**: Read below!
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
