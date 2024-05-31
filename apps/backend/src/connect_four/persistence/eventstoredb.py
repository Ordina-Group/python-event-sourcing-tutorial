from __future__ import annotations

import json

from connect_four.domain import game as game_model
from connect_four.domain import events as domain_events

import attrs

import esdbclient


@attrs.define
class GameRepository:
    _client: esdbclient.EventStoreDBClient

    def add(self, game: game_model.Game) -> None:
        """Add a game to the repository and persist its events.

        :param game: The game to persist
        """
        events = [
            _map_event_to_eventstore_event(event) for event in game.uncommitted_events
        ]
        self._client.append_to_stream(
            stream_name=f"game-{game.id}",
            current_version=esdbclient.StreamState.NO_STREAM,
            events=events,
        )


def _map_event_to_eventstore_event(
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
