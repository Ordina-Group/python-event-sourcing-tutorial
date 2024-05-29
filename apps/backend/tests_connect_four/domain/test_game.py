from typing import Literal

import pytest

from connect_four.domain import game, exceptions, events


def test_game_cannot_be_started_twice() -> None:
    # GIVEN a game that has already been started
    game_obj = game.Game(player_one="player-1", player_two="player-2")
    game_obj.start_game()

    # WHEN the game is started for the second time
    # THEN a GameAlreadyStartedError is raised
    with pytest.raises(exceptions.GameAlreadyStartedError):
        game_obj.start_game()


def test_cannot_make_a_move_in_a_full_column() -> None:
    # GIVEN a started game
    game_obj = game.Game(player_one="player-1", player_two="player-2")
    game_obj.start_game()
    # AND events that filled up a specific column
    game_obj.events.extend(
        events.MoveMade(game_id=game_obj.id, player_id=f"player-{i % 2}", column="A")
        for i in range(1, 7)
    )

    # WHEN a move is made that would place another token in that column
    # THEN an InvalidMoveError is raised
    with pytest.raises(exceptions.InvalidMoveError):
        game_obj.make_move(game.Move(player="player-1", column="A", turn=7))


def test_player_cannot_make_move_out_of_order() -> None:
    # GIVEN a started game without moves
    game_obj = game.Game(player_one="player-1", player_two="player-2")
    game_obj.start_game()

    # WHEN player two tries to make a move out of order
    # THEN an InvalidMoveError is raised
    with pytest.raises(exceptions.InvalidMoveError):
        game_obj.make_move(game.Move(player="player-2", column="A", turn=1))
