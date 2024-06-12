import pytest
from connect_four.domain import events, board
from connect_four.domain import exceptions, game


def test_game_cannot_be_started_twice() -> None:
    # GIVEN a game that has already been started
    game_obj = game.Game()
    game_obj.start_game(player_one="player-1", player_two="player-2")

    # WHEN the game is started for the second time
    # THEN a GameAlreadyStartedError is raised
    with pytest.raises(exceptions.GameAlreadyStartedError):
        game_obj.start_game(player_one="player-1", player_two="player-2")


def test_cannot_make_a_move_in_a_full_column() -> None:
    # GIVEN a started game
    game_obj = game.Game()
    game_obj.start_game(player_one="player-1", player_two="player-2")
    # AND an event history that filled up a specific column
    history = [
        events.MoveMade(
            game_id=game_obj.id, player_id=f"player-{i % 2}", column=board.Column("A")
        )
        for i in range(1, 7)
    ]
    game_obj.load_from_history(history)

    # WHEN a move is made that would place another token in that column
    # THEN an InvalidMoveError is raised
    with pytest.raises(exceptions.InvalidMoveError):
        game_obj.make_move(game.Move(player="player-1", column=board.Column("A")))


def test_player_cannot_make_move_out_of_order() -> None:
    # GIVEN a started game without moves
    game_obj = game.Game()
    game_obj.start_game(player_one="player-1", player_two="player-2")

    # WHEN player two tries to make a move out of order
    # THEN an InvalidMoveError is raised
    with pytest.raises(exceptions.InvalidMoveError):
        game_obj.make_move(game.Move(player="player-2", column=board.Column("A")))


def test_game_can_load_events() -> None:
    # GIVEN a game with a certain id
    game_obj = game.Game("id-1")
    # AND a GameStarted event
    historic_events = [events.GameStarted("id-1", "player-1", "player-2")]

    # WHEN the game loads these events
    game_obj.load_from_history(historic_events)

    # THEN the state of the game reflects these events
    assert game_obj.player_one == "player-1"
    assert game_obj.player_two == "player-2"


def test_winning_move_results_in_game_finished_event() -> None:
    # GIVEN a game
    game_obj = game.Game()
    # AND historic events that allow the game to be won with one move
    historic_events = [
        events.GameStarted("id-1", "p1", "p2"),
        events.MoveMade(game_id=game_obj.id, player_id="p1", column=board.Column("A")),
        events.MoveMade(game_id=game_obj.id, player_id="p2", column=board.Column("A")),
        events.MoveMade(game_id=game_obj.id, player_id="p1", column=board.Column("B")),
        events.MoveMade(game_id=game_obj.id, player_id="p2", column=board.Column("B")),
        events.MoveMade(game_id=game_obj.id, player_id="p1", column=board.Column("C")),
        events.MoveMade(game_id=game_obj.id, player_id="p2", column=board.Column("C")),
    ]
    game_obj.load_from_history(historic_events)
    # AND a move that will win the game for player 1
    move = game.Move(player="p1", column=board.Column("D"))

    # WHEN the move is made
    game_obj.make_move(move)

    # THEN a move event is created for the move
    move_made = events.MoveMade(
        game_id=game_obj.id, player_id="p1", column=board.Column("D")
    )
    assert move_made in game_obj.uncommitted_events
    # AND a GameFinished event indicating player 1 has won is created
    game_won = events.GameEnded(
        game_id=game_obj.id, result=events.GameResult.PLAYER_ONE_WON
    )
    assert game_won in game_obj.uncommitted_events
    # AND the game is marked as finished
    assert game_obj.is_finished


def test_non_winning_move_that_fills_the_board_results_in_game_tied_event() -> None:
    # GIVEN a game
    game_obj = game.Game()
    # AND historic events that allow the game to be tied with one move
    historic_events = [
        events.GameStarted("id-1", "p1", "p2"),
        events.MoveMade(game_id=game_obj.id, player_id="p1", column=board.Column("A")),
        events.MoveMade(game_id=game_obj.id, player_id="p2", column=board.Column("B")),
        events.MoveMade(game_id=game_obj.id, player_id="p1", column=board.Column("A")),
        events.MoveMade(game_id=game_obj.id, player_id="p2", column=board.Column("B")),
        events.MoveMade(game_id=game_obj.id, player_id="p1", column=board.Column("A")),
        events.MoveMade(game_id=game_obj.id, player_id="p2", column=board.Column("B")),
        events.MoveMade(game_id=game_obj.id, player_id="p1", column=board.Column("B")),
        events.MoveMade(game_id=game_obj.id, player_id="p2", column=board.Column("A")),
        events.MoveMade(game_id=game_obj.id, player_id="p1", column=board.Column("A")),
        events.MoveMade(game_id=game_obj.id, player_id="p2", column=board.Column("A")),
        events.MoveMade(game_id=game_obj.id, player_id="p1", column=board.Column("B")),
        events.MoveMade(game_id=game_obj.id, player_id="p2", column=board.Column("B")),
        events.MoveMade(game_id=game_obj.id, player_id="p1", column=board.Column("C")),
        events.MoveMade(game_id=game_obj.id, player_id="p2", column=board.Column("D")),
        events.MoveMade(game_id=game_obj.id, player_id="p1", column=board.Column("C")),
        events.MoveMade(game_id=game_obj.id, player_id="p2", column=board.Column("C")),
        events.MoveMade(game_id=game_obj.id, player_id="p1", column=board.Column("C")),
        events.MoveMade(game_id=game_obj.id, player_id="p2", column=board.Column("C")),
        events.MoveMade(game_id=game_obj.id, player_id="p1", column=board.Column("C")),
        events.MoveMade(game_id=game_obj.id, player_id="p2", column=board.Column("F")),
        events.MoveMade(game_id=game_obj.id, player_id="p1", column=board.Column("D")),
        events.MoveMade(game_id=game_obj.id, player_id="p2", column=board.Column("D")),
        events.MoveMade(game_id=game_obj.id, player_id="p1", column=board.Column("E")),
        events.MoveMade(game_id=game_obj.id, player_id="p2", column=board.Column("D")),
        events.MoveMade(game_id=game_obj.id, player_id="p1", column=board.Column("D")),
        events.MoveMade(game_id=game_obj.id, player_id="p2", column=board.Column("E")),
        events.MoveMade(game_id=game_obj.id, player_id="p1", column=board.Column("D")),
        events.MoveMade(game_id=game_obj.id, player_id="p2", column=board.Column("F")),
        events.MoveMade(game_id=game_obj.id, player_id="p1", column=board.Column("E")),
        events.MoveMade(game_id=game_obj.id, player_id="p2", column=board.Column("E")),
        events.MoveMade(game_id=game_obj.id, player_id="p1", column=board.Column("E")),
        events.MoveMade(game_id=game_obj.id, player_id="p2", column=board.Column("E")),
        events.MoveMade(game_id=game_obj.id, player_id="p1", column=board.Column("F")),
        events.MoveMade(game_id=game_obj.id, player_id="p2", column=board.Column("G")),
        events.MoveMade(game_id=game_obj.id, player_id="p1", column=board.Column("G")),
        events.MoveMade(game_id=game_obj.id, player_id="p2", column=board.Column("G")),
        events.MoveMade(game_id=game_obj.id, player_id="p1", column=board.Column("G")),
        events.MoveMade(game_id=game_obj.id, player_id="p2", column=board.Column("F")),
        events.MoveMade(game_id=game_obj.id, player_id="p1", column=board.Column("G")),
        events.MoveMade(game_id=game_obj.id, player_id="p2", column=board.Column("F")),
        events.MoveMade(game_id=game_obj.id, player_id="p1", column=board.Column("G")),
    ]
    game_obj.load_from_history(historic_events)
    # AND a move that will win the game for player 1
    move = game.Move(player="p2", column=board.Column("F"))

    # WHEN the move is made
    game_obj.make_move(move)

    # THEN a move event is created for the move
    move_made = events.MoveMade(
        game_id=game_obj.id, player_id="p2", column=board.Column("F")
    )
    assert move_made in game_obj.uncommitted_events
    # AND a GameFinished event indicating player 1 has won is created
    game_tied = events.GameEnded(game_id=game_obj.id, result=events.GameResult.TIED)
    assert game_tied in game_obj.uncommitted_events
    # AND the game is marked as finished
    assert game_obj.is_finished


def test_move_that_does_not_finish_game_does_not_emit_finish_related_event() -> None:
    # GIVEN an ongoing game
    game_obj = game.Game()
    game_obj.load_from_history(
        [
            events.GameStarted("id-1", "p1", "p2"),
            events.MoveMade(
                game_id=game_obj.id, player_id="p1", column=board.Column("A")
            ),
            events.MoveMade(
                game_id=game_obj.id, player_id="p2", column=board.Column("B")
            ),
        ]
    )
    # AND a move that does not finish the game
    move = game.Move(player="p1", column=board.Column("G"))

    # WHEN the move is made
    game_obj.make_move(move)

    # THEN the move made event is created
    mode_made = events.MoveMade(
        game_id=game_obj.id, player_id="p1", column=board.Column("G")
    )
    assert mode_made in game_obj.uncommitted_events
    # BUT no GameEnded event is created
    assert not any(
        isinstance(event, events.GameEnded) for event in game_obj.uncommitted_events
    )


def test_game_can_be_reconstructed_after_it_has_ended() -> None:
    # GIVEN a game
    game_obj = game.Game()
    # AND historic events that allow the game to be won with one move
    historic_events = [
        events.GameStarted("id-1", "p1", "p2"),
        events.MoveMade(game_id=game_obj.id, player_id="p1", column=board.Column("A")),
        events.MoveMade(game_id=game_obj.id, player_id="p2", column=board.Column("A")),
        events.MoveMade(game_id=game_obj.id, player_id="p1", column=board.Column("B")),
        events.MoveMade(game_id=game_obj.id, player_id="p2", column=board.Column("B")),
        events.MoveMade(game_id=game_obj.id, player_id="p1", column=board.Column("C")),
        events.MoveMade(game_id=game_obj.id, player_id="p2", column=board.Column("C")),
        events.MoveMade(game_id=game_obj.id, player_id="p1", column=board.Column("D")),
        events.GameEnded(game_id=game_obj.id, result=events.GameResult.PLAYER_ONE_WON),
    ]

    # WHEN the historic events are applied to the game
    game_obj.load_from_history(historic_events)

    # THEN the game state reflects that the game has ended
    assert game_obj.is_finished
    # AND the game has a result
    assert game_obj.result == events.GameResult.PLAYER_ONE_WON
