# Exercise 3 [Persist the events]

- **Length:** 30-40 minutes 

All that buzz about persisting events instead of state, and we haven't even
persisted anything yet. Let's change that.

> [!IMPORTANT]
> You need to have an instance of EventStoreDB running locally for this
> exercise. You can start an instance using the `compose.yaml` file provided in
> the root of this repository.
>   
> You can find more information [here](/README.md#running-eventstoredb) in the
> README.

> [!TIP]
> EventStoreDB comes with a convenient web interface to check out the events
> you've stored: http://localhost:2113/.


## 3.1. Preparation

Switch to the branch `03-exercise-persisting-the-events`.

<br>

---

## 3.2. Exploring the repoverse

In the following exercises, you'll implement a `GameRepository` that persists
events in EventStoreDB and retrieves them.

We've provided a minimal application layer to make connecting the dots a bit
easier. You won't have to touch this layer, but it does contain an interface
that our `GameRepository` has to implement.

You can find there relevant files in [`/src/connect_four/application/`][application-directory].

It is used by the new CLI-client that you can run with:
```bash
poetry run python -m connect_four.cli
```

In addition to the application layer, we've also provided you with a stub for
the `GameRepository`.

1. Check out the stub in [`src/connect_four/persistence/`][esdb-game-repository]

<br>

<details>
  <summary><i>Writing tests for the repository</i></summary>

> The `GameRepository` expects an instance of the `EventStoreDBClient` to
> interact with EventStoreDB. You can inject an instance of the client like 
> this:
>   
> ```python
> import esdbclient
>   
> from connect_four.persistence import eventstoredb
>  
>   
> def test_game_repository() -> None:
>     client = esdbclient.EventStoreDBClient("esdb://localhost:2113?tls=false")
>     repo = eventstoredb.GameRepository(client=client)
> ```
>   
> One thing to keep in mind is that the running instance of `EventStoreDB` will
> not be cleaned between tests (or between test runs). This is not ideal, but we
> want you to interact with an actual event store.
> 
> As our game streams will use Game IDs in their names, which is a random UUIDs,
> this shouldn't cause too many issues for this tutorial. If you want to write
> integration tests for actual projects, you could consider using a test
> container or an in-memory event store that you restart between tests or test
> runs.
> 
> Alternatively, if this really bothers you, you can [inject][there-is-nothing-difficult-about-this] a test double.
</details>

[there-is-nothing-difficult-about-this]: https://www.youtube.com/clip/Ugkxk8enfYMInruaxQWXb90kVF3J9Jivgs9n

[application-directory]: /src/connect_four/application/
[esdb-game-repository]:  /src/connect_four/persistence/eventstoredb.py

<br>

---

## 3.3. If a game starts in the forest...

If a game starts in the forest and there's no repo to store the event, did it
truly start? Since we only store events, not state, the only way for a game to
be saved is by storing its events in an event store.

That's why the `start_game`-method of the application service creates a `Game`,
executes the `start_game`-command on the game, and then persists the events of
the game to the event store using the repository.

In this exercise, you will implement the persistence logic required to make the
`GaeRepository.add`-method store the events of a `Game` in EventStoreDB.

<br>

<details>
  <summary><i>Quick Example of Using the EventStoreDBClient</i></summary>

> Here's an example that appends events to a stream using the `EventStoreDBClient`:
>   
> ```python
> import esdbclient
>   
>   
> # You'll need to translate events to esdbclient events:
> event1 = esdbclient.NewEvent(type='EventType', data=b'{"data":"bytes"}')
>   
> # And a name for the event stream
> stream_name = "some-event-stream-name"
>   
> # Now you can append the NewEvent to the stream
> client = esdbclient.EventStoreDBClient("esdb://localhost:2113?tls=false")
> client.append_to_stream(
>     stream_name=stream_name,
>     current_version=esdbclient.StreamState.ANY,
>     events=[event1]
> )
> ```
>  
</details>

<br>

1. Add an implementation to `GameRepository.add` that persist a`Game` with only
   a `GameStarted`-event.

   This requires a few steps:
   1. Map a domain event to an `esdbclient.NewEvent` by extending the
      `_map_eventstore_event_to_domain_event` function and using it in the
      `add`-method. Hint: you can use the `json` module to serialize the event 
      data, although you do need to encode the string to bytes.
   2. Determine the stream name based on the game ID using `f"game-{game.id}"`.
   3. Append the event to the stream using the `EventStoreDBClient`.

<br>

> [!TIP]
> There's a test in `tests/persistence/test_game_repository.py` that you can use
> to test your implementation.

<br>

---

## 3.4. Now... where was I?

Having a great memory is no use if you can't retrieve anything. So, let's add
retrieval logic to the `GameRepository`.

<br>

<details>
  <summary><i>Quick Example of Retrieving Events</i></summary>

> Retrieving events from a stream is fairly straightforward:
> 
> ```python
> import esdbclient
> 
> client = esdbclient.EventStoreDBClient("esdb://localhost:2113?tls=false")
> recorded_events = client.get_stream("stream-name-here")
> ```
> 
> The `EventStoreDBClient.get_stream`-method will return a `tuple` with `RecordedEvent`-objects. Like
> `NewEvent`-objects, `RecordedEvent`-objects have a `type` and `data` attribute
> that you can use to recreate the domain event you stored.
</details>

<br>

1. Add logic to the `get`-method that retrieves the events in the game stream.

2. Extend `_map_eventstore_event_to_domain_event` to map a `RecordedEvent` 
   the domain event `GameStarted` and apply it to the events from step 1.

3. Create a `Game`-instance with the ID passed to `get`.

4. Add a helper method to the `Game`-class, `load_from_history`, that applies
   an iterable of events to the game and adds the events to the `events`-list
   of the game attribute.

5. Call the helper method from the repository's `get`-method with the events
   resurrected from the event store.

6. Now that you've recreated the `Game`-instance in the correct state, return
   it to the caller,

<br>

> [!TIP]
> There's a test in `tests/persistence/test_game_repository.py` that you can use
> to test your implementation. (You do have to remove the skip decorator.)

<br>

---

## 3.5. Show Me Your Moves

1. Now add support for persisting and retrieving `MoveMade` events by adding the
   mapping logic for this event to both mapping functions.

2. Remove the `skip` from the `test_game_repository_stores_move_made_events`
   test in `tests/persistence/test_game_repository.py` and notice that **it
   still fails when you run it!**

   As you can see, we've appended three rather than two events to the event
   stream. What's going on here?

<br>

---

### 3.6. Those who include history are forced to repeat it

The problem is that when the events of the `Game`-instance were persisted after
the move was made, the `Game.events` list contained two events: `GameStarted`
and `MoveMade`.

Since we are *appending* events to the event and the `GameStarted` event was
already stored when the game was created, persisting the entire `Game.events`
list will store another `GameStarted` event!

*This is obviously a problem.*

How would you solve this? Keep in mind that the `Game`-instance would be out of
sync if you were to omit historic events entirely. This is problematic because
we do want to be able to check constraints and perform other business logic that
relies on the historical events.

<br><br>

One solution to this problem is to separate the historical events from the
uncommitted events. This is the solution that we're going to implement here.

1. Replace the `events`-attribute of the `Game`-class with two attributes:
   `historical_events` and `uncommitted_events`.

2. Change the `load_from_history`-method to store the historical events in the
   `historical_events`-attribute.

3. Change the `process_event-method` so that it appends new events to the
   `uncommitted_events`-attribute.

4. Add a property, `events`, that returns the concatenation of the
   `historical_events` and `uncommitted_events`-attributes. Make sure to retain
   the proper order of events in the concatenation.

5. Change the `GameRepository.add`-method to store the `uncommitted_events` in
   the event stream instead of all the events.

6. Check if this solved the problem by rerunning the test from the previous
   exercise.

<br>

---

## 3.7. The end is nigh (of the workshop, not the game...)

Now add support for persisting and retrieving `GameFinished` events.

<br>

## 3.8. Connect Four: The Final Battle

That should be it. You've successfully implemented an event-sourced Connect Four
game.

You can play your game using the CLI-client:

```shell
poetry run python -m connect_four.cli
```

**If you did not finish your implementation, but still want to play the game,
switch to the solution branch `solution-03-exercise-persisting-the-events`.**

<br><br>

---

<p align="center">
   <a href="/exercises/exercise-02-play-the-game.md">⬅️ Back to exercise 2</a> | <a href="https://404-exercise-not-found.europython">Continue to exercise 404 ➡️</a>
</p>
