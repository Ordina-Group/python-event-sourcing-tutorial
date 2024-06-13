"""Tests for the EventStoreDB-backed `GameRepository`"""

import json

import esdbclient
import pytest

from connect_four.application import application
from connect_four.domain import board, events
from connect_four.domain import game as game_
from connect_four.persistence import eventstoredb


def test_game_repository_stores_newly_started_game(
    esdb_client: esdbclient.EventStoreDBClient,
) -> None:
    """Starting a game stores a `GameStarted` event."""
    # GIVEN an instance of the GameRepository
    repository = eventstoredb.GameRepository(client=esdb_client)
    # AND an instance of the application service
    app = application.ConnectFourApp(game_repository=repository)

    # WHEN you create and store a new game using the app
    game_id = app.create_game(player_one="player_one", player_two="player_two")

    # THEN an `StartGame` event is stored in the EventStoreDB
    [event] = esdb_client.get_stream(f"game-{game_id}")
    assert event.type == "GameStarted"
    # AND the stored event contains the player names
    event_data = json.loads(event.data.decode("utf-8"))
    assert event_data == {"player_one": "player_one", "player_two": "player_two"}


@pytest.mark.skip("enable test for exercise 3.5")
def test_game_repository_recreates_stored_freshly_started_game(
    esdb_client: esdbclient.EventStoreDBClient,
) -> None:
    """Starting a game stores a `GameStarted` event."""
    # GIVEN an instance of the GameRepository
    repository = eventstoredb.GameRepository(client=esdb_client)
    # AND an instance of the application that uses the repository
    app = application.ConnectFourApp(game_repository=repository)
    # AND the id of a freshly started and stored game
    game_id = app.create_game(player_one="p1", player_two="p2")

    # WHEN you use the game id to retrieve the game from the repository
    game = repository.get(game_id)

    # THEN you get an instance of `Game`
    assert isinstance(game, game_.Game)
    # AND the game has the expected events
    assert game.events == [events.GameStarted(player_one="p1", player_two="p2")]
    # AND the state of the game is as expected
    assert game.id == game_id
    assert game.player_one == "p1"
    assert game.player_two == "p2"
    assert game.next_player == "p1"


@pytest.mark.skip("enable test for exercise 3.6")
def test_game_repository_stores_move_made_events(
    esdb_client: esdbclient.EventStoreDBClient,
) -> None:
    """Starting a game stores a `GameStarted` event."""
    # GIVEN an instance of the GameRepository
    repository = eventstoredb.GameRepository(client=esdb_client)
    # AND an instance of the application that uses the repository
    app = application.ConnectFourApp(game_repository=repository)
    # AND the id of a game that has been freshly started
    game_id = app.create_game(player_one="player_one", player_two="player_two")
    # AND a move that player on wants to make
    move = game_.Move(player="player_one", column=board.Column("A"))

    # WHEN you make a move using the application
    app.make_move(game_id=game_id, move=move)

    # THEN the event stream contains exactly two events
    stored_events = esdb_client.get_stream(f"game-{game_id}")
    assert len(stored_events) == 2
    # AND the last event is a MoveMade event
    move_made = stored_events[-1]
    assert move_made.type == "MoveMade"
    # AND the event contains the relevant move information
    event_data = json.loads(move_made.data.decode("utf-8"))
    assert event_data == {"player": "player_one", "column": "A"}
