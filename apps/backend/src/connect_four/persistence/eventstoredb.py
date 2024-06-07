from __future__ import annotations

import json

import attrs
import esdbclient

from connect_four.domain import events as domain_events
from connect_four.domain import game as game_model


@attrs.define
class GameRepository:
    _client: esdbclient.EventStoreDBClient

    def add(self, game: game_model.Game) -> None:
        """Add a game to the repository and persist its events.

        :param game: The game to persist
        """
        events = [
            _map_domain_event_to_eventstore_event(event)
            for event in game.uncommitted_events
        ]
        self._client.append_to_stream(
            stream_name=f"game-{game.id}",
            current_version=esdbclient.StreamState.NO_STREAM,
            events=events,
        )

    def get(self, game_id: str) -> game_model.Game:
        """Return the state of the game based on the game id."""
        eventstore_events = self._client.get_stream(
            stream_name=f"game-{game_id}",
        )
        events = [
            _map_eventstore_event_to_domain_event(event) for event in eventstore_events
        ]
        game = game_model.Game(game_id)
        game.load_from_history(events)
        return game


def _map_domain_event_to_eventstore_event(
    event: domain_events.GameEvent,
) -> esdbclient.NewEvent:
    match event:
        case domain_events.GameStarted(
            game_id=game_id, player_one=player_one, player_two=player_two
        ):
            data = {
                "game_id": game_id,
                "player_one": player_one,
                "player_two": player_two,
            }
            json_data = json.dumps(data)
            return esdbclient.NewEvent(
                type="GameStarted",
                data=json_data.encode("utf-8"),
            )
        case _:
            pass


def _map_eventstore_event_to_domain_event(
    event: esdbclient.RecordedEvent,
) -> domain_events.GameEvent:
    match event.type:
        case "GameStarted":
            data = json.loads(event.data)
            return domain_events.GameStarted(
                game_id=data["game_id"],
                player_one=data["player_one"],
                player_two=data["player_two"],
            )
