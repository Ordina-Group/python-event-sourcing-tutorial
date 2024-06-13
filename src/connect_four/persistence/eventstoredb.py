"""A game repository backed by EventStoreDB."""

from __future__ import annotations

import json

import attrs
import esdbclient

from connect_four.domain import board, events
from connect_four.domain import game as game_
from connect_four.domain import result as result_


@attrs.define
class GameRepository:
    """A repository for persisting games in EventStoreDB.

    This GameRepository implements the IGameRepository interface, as
    expected by the ConnectFourApp application service.

    See `connect_four.application.repository.IGameRepository` for the
    Protocol defining the required interface.
    """

    _client: esdbclient.EventStoreDBClient

    def add(self, game: game_.Game) -> None:
        """Add a game to the repository.

        :param game: The game to save
        :return: The ID of the game that was saved
        """
        events_to_append = [
            _map_domain_event_to_eventstore_event(event)
            for event in game.uncommited_events
        ]
        self._client.append_to_stream(
            stream_name=f"game-{game.id}",
            current_version=esdbclient.StreamState.ANY,
            events=events_to_append,
        )

    def get(self, game_id: str) -> game_.Game:
        """Get a game from the repository.

        :param game_id: The ID of the game
        :return: An instance of game after applying the stored events to
            ensure the game is in the correct state
        """
        domain_events = [
            _map_eventstore_event_to_domain_event(event)
            for event in self._client.get_stream(f"game-{game_id}")
        ]
        game = game_.Game(id=game_id)
        game.load_from_history(domain_events)
        return game


def _map_domain_event_to_eventstore_event(
    event: events.GameEvent,
) -> esdbclient.NewEvent:
    """Map a domain event to an eventstore event.

    :param event: the domain event to map
    :return: an eventstore event that can be persisted in EventStoreDB
    """
    match event:
        case events.GameStarted(player_one=player_one, player_two=player_two):
            data = {"player_one": player_one, "player_two": player_two}
            return esdbclient.NewEvent(
                type="GameStarted", data=json.dumps(data).encode("utf-8")
            )
        case events.MoveMade(player=player, column=column):
            data = {"player": player, "column": column.value}
            return esdbclient.NewEvent(
                type="MoveMade", data=json.dumps(data).encode("utf-8")
            )
        case events.GameFinished(result=result):
            data = {"result": result.value}
            return esdbclient.NewEvent(
                type="GameFinished", data=json.dumps(data).encode("utf-8")
            )
        case _:
            raise ValueError("Domain event not recognized.")


def _map_eventstore_event_to_domain_event(
    event: esdbclient.RecordedEvent,
) -> events.GameEvent:
    """Map an eventstore event to a domain event.

    :param event: the eventstore event to map
    :return: the equivalent domain event
    """
    match event:
        case esdbclient.RecordedEvent(type="GameStarted", data=data):
            data_dict = json.loads(data.decode("utf-8"))
            return events.GameStarted(
                player_one=data_dict["player_one"], player_two=data_dict["player_two"]
            )
        case esdbclient.RecordedEvent(type="MoveMade", data=data):
            data_dict = json.loads(data.decode("utf-8"))
            return events.MoveMade(
                player=data_dict["player"], column=board.Column(data_dict["column"])
            )
        case esdbclient.RecordedEvent(type="GameFinished", data=data):
            data_dict = json.loads(data.decode("utf-8"))
            return events.GameFinished(result=result_.GameResult(data_dict["result"]))
        case _:
            raise ValueError("Recorded Event not recognized.")
