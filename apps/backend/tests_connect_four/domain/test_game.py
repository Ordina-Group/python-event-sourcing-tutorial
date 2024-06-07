from typing import Literal

import pytest

from connect_four.domain import events as domain_events
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
    # AND events that filled up a specific column
    game_obj.uncommitted_events.extend(
        events.MoveMade(game_id=game_obj.id, player_id=f"player-{i % 2}", column="A")
        for i in range(1, 7)
    )

    # WHEN a move is made that would place another token in that column
    # THEN an InvalidMoveError is raised
    with pytest.raises(exceptions.InvalidMoveError):
        game_obj.make_move(game.Move(player="player-1", column="A", turn=7))


def test_player_cannot_make_move_out_of_order() -> None:
    # GIVEN a started game without moves
    game_obj = game.Game()
    game_obj.start_game(player_one="player-1", player_two="player-2")

    # WHEN player two tries to make a move out of order
    # THEN an InvalidMoveError is raised
    with pytest.raises(exceptions.InvalidMoveError):
        game_obj.make_move(game.Move(player="player-2", column="A", turn=1))


def test_game_can_load_events() -> None:
    # GIVEN a game with a certain id
    game_obj = game.Game("id-1")
    # AND a GameStarted event
    events = [domain_events.GameStarted("id-1", "player-1", "player-2")]

    # WHEN the game loads these events
    game_obj.load_from_history(events)

    # THEN the state of the game reflects these events
    assert game_obj.player_one == "player-1"
    assert game_obj.player_two == "player-2"
