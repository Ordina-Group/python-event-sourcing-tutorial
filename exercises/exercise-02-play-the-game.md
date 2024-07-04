# Exercise 2 [Play the game]

- **Length:** 30-35 minutes 


<details>
  <summary><i>Check your progress with the Connect Four CLI!</i></summary>

> To make the game more exciting, we've implemented a CLI-client that allows you
> to play a game of Connect Four. That is, if you manage to implement the
> necessary commands and events.
>   
> Run the simply by executing the following command:
>  
> ```shell
> poetry run python -m connect_four.cli
> ```
>  
> Of course, another way to check your progress is by writing unit tests. We've
> already implemented a basic unit test for a game started constraint to give
> you an idea of how to write tests for the `Game`-aggregate.
>  
> ```shell
> poetry run pytest
> ```
</details>

<br>

---

### 2.1. Preparation

Switch to the branch `02-exercise-play-the-game`.

<br>

---

### 2.2. You've got to move it, move it

What's a game without moves? To make a move in the game, a player has to be able
to issue a command that makes a move.

1. Write the implementation for the `make_move`-method. This command should
   instantiate a `MoveMade`-event and use the `_process_event`-method to apply
   the event to the aggregate and append it the `events` list.

   Think about the data that you need to store in the event and the state such
   an event should influence.

<br>

---

### 2.3. Don't speak out of turn

Making moves is great, but we need to be careful that players don't make moves
that are not allowed. One such constraint is "For a player to make a move in a
specific column, that column **must** have room for another token."

1. Add a constraint to the `make_move`-method that prevents a player from
   placing a token in a column that's already full.

> [!TIP]
> The `Board`-class already provides a `has_room_in_column`-method that you can
> use to perform the check.

<br>

---

### 2.4. The end is nigh (of the game, not the workshop...)

Now you can make a bunch of moves. There's just one problem: This game will
never end. Once the board is full, every move you try to make will be rejected
by the constraint you just implemented, but the game still won't end.

That's why you're going to get us out of this infinite game by implementing a
`GameFinished`-event.

1. Add a `GameFinished`-event and add attributes for the information you think
   it should contain.

<details>
  <summary><i>Hint: What Information Do You Need To Store?</i></summary>

> Remember that we're never going to persist the state of an aggregate as-is,
> only the events that determined the state. This means that if you want to
> store the result of a game. you have to associate that information with the
> event.
>   
> How you store that information is a design choice. The game already "knows"
> who the players are, so you might just store "player a won", "player b won",
> or "game ended in a draw".
</details>

How will this event ever be triggered? In our case, this event is simply an
event that *sometimes* follows a `MoveMade`-event.

2. Check if a game has ended right after the `MoveMade`-event in the `make_move`
   command. If it has ended, emit a `GameFinished`-event. **Note:** the `Board`
   class has a `get_result`-method that you can use to check if the game has
   finished.

<br>

> [!IMPORTANT]
> Don't forget to apply the event to the `Game`-aggregate!

<br>

---

### 2.5. All work and no play makes Jack a dull boy

Use the CLI to beat another tutorial participant with the game you just
implemented.

```shell
poetry run python -m connect_four.cli
```

**If you did not finish the previous exercises, but you still want to play the
game, switch to the solution branch `solution-02-exercise-play-the-game`.**


<br><br>

---

<p align="center">
   <a href="/exercises/exercise-01-start-game.md">⬅️ Back to exercise 1</a> | <a href="/exercises/exercise-03-persist-the-events.md">Continue to exercise 3 ➡️</a>
</p>
