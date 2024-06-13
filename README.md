# Event Sourcing Workshop

A workshop Event Sourcing for an office day of the Ordina Pythoneers.

![Image of an event sourcing workshop](/event-sourcing-workshop.jpg)

# Local Setup

## Application

The application uses Poetry as a package management tool.

= Use the command `poetry install` install the dependencies.

- Use the command `poetry shell` to create a python shell.

- Use the command `poetry run pytest` to run all the tests in the application.

- Use the command `poetry run python -m connect_four.cli` to play the Connect
  Four game in the CLI. Note that this game will only be fun once you've
  actually implemented it during the workshop...

## Running EventstoreDB on your local machine

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

---

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

---

## Exercise 1 [Start game]

### 1.1. Preparation

Switch to the branch `01-exercise-start-game`

### 1.2. Initializing the aggregate

Open the file `src/connect_four/domain/game.py`. This file contains a stub of
the `Game` aggregate that is the model for a game of Connect Four. This is the
class that will track the events of the game and will have methods for the
commands related to the game.


As a first step, write an `__init__`-method for the `Game` class that sets two
attributes, `player_one` and `player_two` that will hold the names of the
players. As the game hasn't started yet, we do not yet know the names of the
players, so assign a sensible default value to these attributes.

### 1.3. Starting a game with two players

To start a `Game`, the class needs to support the "Start Game"-command. Add a
method, `start_game`, that starts a game by assigning the names of the two
players to the relevant attributes.

### 1.4. An eventful state of being

You may have noticed that we're currently still manipulating state. This is not
what we want in an event-sourced system. Instead of manipulating state, we want
to record events. Add an attribute, `events`, to the `Game` class that will hold
the events of the game in a list.

### 1.5. Not only elephants have memory

Now that we have a list to store the events, change the `start_game` command to
append an event to the `events` list instead of assigning the player names
directly. This means that you will also have to remove the assignments of the
player attributes from the method.

This means that you will also have to define a `GameStarted` event in
`src/connect_four/domain/events.py`. As we don't store state anymore--you did
remove the attribute assignment, right?--the only way to persist the names of
the players is to ensure that the event contains this information. So, make sure
that you store this as a part of the event.

### 1.6. Those who remember the past are able to repeat it 

Congratulations, you've successfully persisted your information in an event
instead of the state of the object. However, it's still very handy to have easy
access to the current state while the `Game`-object is in memory. This is why we
want to *apply* the event to the `Game` state.

Write an `apply`-method that applies the `GameStarted` event to the `Game`
instance. In this case, this means that we want to assign the names of the
players stored in the event to the relevant attributes of the `Game` instance.

This may feel a bit weird, but if you think about it, the state of the `Game`
now reflects that the event has happened. Moreover, if you were to persist the
event, you can now use this `apply`-method on a fresh instance of `Game` to
recreate a `Game` with the exact same state. You can *replay* the events to
recreate the state of the aggregate.

Don't forget to call the `apply`-method with the event at the end of the
`start_game` command otherwise the event history and the state will be out of
sync.

### Bonus exercise: Constraints are the best thing since sliced bread

What should happen if you issue a `start_game`-command for the second time on
the same game? Implement a solution for this potential problem.

Hint: Can you think of a *constraint* that would prevent a second command from
creating a second `GameStarted`-event?

---



## Exercise 2 [Play the game]

To make the game more exciting, we've implemented a CLI-client that allows you
to play a game of Connect Four. That is, if you manage to implement the
necessary commands and events.

Still, you may want to run the CLI-client from time to time to check your
progress. You can do this by running the following command:

```shell
poetry run python -m connect_four.cli
```

Of course, another way to check your progress is by writing unit tests. We've
already implemented a basic unit test for a game started constraint to give you
an idea of how to write tests for the `Game`-aggregate.

```shell
poetry run pytest
```

### 2.1. Preparation

Switch to the branch `02-exercise-play-the-game`.

### 2.2. You've got to move it, move it

What's a game without moves? To make a move in the game, a player has to be able
to issue a command that makes a move.


Write the implementation for the `make_move`-method. This command should create
a `MoveMade`-event and use the `_process_event`-method to apply the event to the
aggregate and append  it the `events` list.


Think about the data that you need to store in the event and the state such an
event should influence.

### 2.3. Don't speak out of turn

Making moves is great, but we need to be careful that players don't make moves
that are not allowed. Think about constraints like "For a player to make a move,
it **must** be the player's turn", "For a player to make a move, the game 
**must** not be finished", and "For a player to make a move, the selected column
**must** have room for an additional token".

Note: The check for the latter constraint can mostly be delegated the `Board`
class that we've implemented for you. It has `Board.has_room_in_column`-method
that checks if a column has room for a new token.

### 2.4. The end is nigh (of the game, not of the workshop...)

Now you can make a bunch of legal moves, but the game won't end. At some point,
the board will be completely full, but the game just won't stop. Are you not
tired of this game yet?

Help us get out of this infinite game by implementing a `GameFinished`-event. A
question that remains is how this event is triggered. Do you think we need a 
specific command for that?

In this case, a `GameFinished`-event simply follows a `MoveMade`-event if the
move results in a win for one of the players or a tie (i.e., the board filled up
without reaching a win-state).

The `GameFinished` event should contain the result of the game, but don't forget
to alsi update the state by applying the event.

Note: You don't have to implement the logic for determining if a player has won
or if the game is a tie. This logic is already implemented in the `get_result`
method of the`Board` class. If this method returns a `Result`, this means that
the game has ended; if it returns `None`, the game is still ongoing.

### 2.5. All work and no play makes the Pythoneers a dull group

Use the CLI to beat your pair programming partner or another colleague. Note
that winning is not optional.

```shell
poetry run python -m connect_four.cli
```

Hint: If you did not finish the previous exercises, but you still want to play
the game, switch to the solution branch `solution-02-exercise-play-the-game`.

---



## Exercise 3 [Persisting the events]

All that buzz about persisting events instead of state and we haven't even
persisted anything yet. In this exercise, we're going to store game events in
EventStoreDB and reconstruct games using events fetched from EventStoreDB.

Note that you need to run an instance of EventStoreDB locally for the exercises
below. You can start an instance using the `compose.yaml` file provided in the
root of this repository.

See [Local Setup](#local-setup) for more information on how to run EventStoreDB.

### 3.1. Preparation

Switch to the branch `03-exercise-persisting-the-events`.

### 3.2. Always remember to carry your ID

To persist events for specific games, we need to be able to identify specific
games. Add an `id`-attribute to the `Game`-class.


Note: for this workshop, it's okay to use a UUID that's generated when a game
is instantiated without an ID.

### 3.3. Exploring the repoverse

Now that we have an ID for the game, we can start persisting the game events in
EventStoreDB. To do this, you're going to implement a game repository that uses
an EventStoreDB client to persist and retrieve events.

We've provided you with a minimal application service to make interacting with
games easier. You can find the application service and the interface of the
game repository it expects in `src/connect_four/application/`.

You should not need to make changes to the application layer, but it is used by
the new CLI that you can use to test your implementation:

```bash
poetry run python -m connect_four.cli
```

In preparation of the next exercises, have a look at the stubs of the 
`GameRepository` in `src/connect_four/persistence/`.

Note that this repository expects an instance of the EventStoreDBClient to do
its work. If you're going to write tests, you can provide your repository with
one by injecting it:

```python
import esdbclient

from connect_four.persistence import eventstoredb

def test_game_repository() -> None:
    client = esdbclient.EventStoreDBClient("esdb://localhost:2113?tls=false")
    repo = eventstoredb.GameRepository(client=client)
```

### 3.4. If a game is started in the forest...

If a game is started in the forest and there's no repo te persist it, did it
truly exist? Since we only store events, not state, the only way for a game to
be saved is if we store its event in the event store.

That's why the `start_game`-method of the application service creates a Game,
executes the `start_game`-command on the game, and then persists the events of
the game to the event store using the repository.

Here's an example of how to append events to a stream using the
EventStoreDBClient:

```python
import esdbclient


# You'll need to translate events to esdbclient events:
event1 = esdbclient.NewEvent(type='EventType', data=b'{"data":"bytes"}')

# And a name for the event stream
stream_name = "some-event-stream-name"

# Now you can append the NewEvent to the stream
client = esdbclient.EventStoreDBClient("esdb://localhost:2113?tls=false")
client.append_to_stream(
    stream_name=stream_name,
    current_version=esdbclient.StreamState.ANY,
    events=[event1]
)
```

Add an implementation to `GameRepository.add` that persist a `Game` with only
a `GameStarted`-event.

You'll need a few steps:
- Map a domain event to an `esdbclient.NewEvent` by extending the
  `_map_eventstore_event_to_domain_event` function and using it in the
  `add`-method. Hint: you can use the `json` module to serialize the event data,
  although you do need to encode the string to bytes.
- Determine the stream name based on the game ID using `f"game-{game.id}"`.
- Append the event to the stream using the `EventStoreDBClient`.

There's a test in `tests/persistence/test_game_repository.py` that you can use
to test your implementation.

### 3.5. Now... where was I?

Having a great memory is no use if you can't recall anything. In this exercise,
you'll implement a method to retrieve a game from the repository. Since the only
thing we've stored is an event, we do need to make sure that our repository
creates a game and applies the events to it.

Retrieving events from a stream is fairly straightforward:

```python
import esdbclient

client = esdbclient.EventStoreDBClient("esdb://localhost:2113?tls=false")
recorded_events = client.get_stream("stream-name-here")
```

The `get_stream`-method will return a `tuple` with `RecordedEvent`-objects. Like
`NewEvent`-objects, `RecordedEvent`-objects have a `type` and `data` attribute
that you can use to recreate the domain event you stored.


1. Add logic to the `get`-method that retrieves the events in the game stream.
2. Extend `_map_eventstore_event_to_domain_event` to map a `RecordedEvent` 
   the domain event `GameStarted` and apply it to the events from step 1.
3. Create a `Game`-instance with the ID passed to `get`.
4. Add a helper method to the `Game`-class, `load_from_history`, that applies
   an iterable of events to the game and adds the events to the `events`-list
   of the game attribute.
5. Call the helper method from the repository's `get`-method with the events
   resurrected from the event store.
5. Now that you've recreated the `Game`-instance in the correct state, return
   it to the caller,

There's a test in `tests/persistence/test_game_repository.py` that you can use
to test your implementation. (You do have to remove the skip decorator.)


### 3.6. Show Me Your Moves

Now add support for persisting and retrieving `MoveMade` events by adding the
mapping logic for this event to both mapping functions.

After you've done that, remove the `skip` from the `test_game_repository_stores_move_made_events`
test in `tests/persistence/test_game_repository.py` and run the test to see if
it works as expect.

You'll notice that the test fails. There are now three not two events in the
stream. Can you figure out why?

We'll solve the problem in the next exercise.

### 3.7. Those who include history are forced to repeat it

The problem is that when the events of the `Game`-instance were persisted after
the move was made, the `Game.events` list contained two events: `GameStarted`
and `MoveMade`.

Since the `GameStarted`-event was already stored before the move was made but
was also added to the `event`-stream when the game was recreated before making
the move, saving the game after the move also saved another `GameStarted` event
to the stream.

This is obviously a problem.

How would you solve this? Keep in mind that the `Game`-instance would be out of
sync if were to omit historic events.

One solution to this problem is to separate the historical events from the
uncommited events. This is the solution that we're going to implement here.

- Replace the `events`-attribute of the `Game`-class with two attributes:
  `historical_events` and `uncommited_events`.
- Change the `load_from_history`-method to store the historical events in the
  `historical_events`-attribute.
- Change the `process_event-method` sp that it appends new events to the
  `uncmmited_events`-attribute.
- Add a property, `events`, that returns the concatenation of the
  `historical_events` and `uncommited_events`-attributes. Make sure to retain
  the proper order of events in the concatenation.
- Change the `GameRepository.add`-method to store the `uncommited_events` in the
  event stream instead of all the events.

Check if this solved the problem by rerunning the test from the previous
exercise.

### 3.8. The end is nigh (of the workshop, not of the game...)

Now add support for persisting and retrieving `GameFinished` events.

### 3.9. Connect Four: The Final Battle

That should be it. You've successfully implemented an event-sourced Connect Four
game.

You can play your game using the CLI-client:

```shell
poetry run python -m connect_four.cli
```

If you did not finish your implementation, but still want to play the game,
switch to the solution branch `solution-03-exercise-persisting-the-events`.

---

# Notes:

## Introduction to Event Sourcing

- What is Event Sourcing?
- Why would you use it?
- Domain Modeling/DDD
- State vs Events (including persistence)
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
- Check out branch `01-exercise-start-game`

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
