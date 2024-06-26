# Exercise 2 [Play the game]

- **Length:** 30-40 minutes 

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
