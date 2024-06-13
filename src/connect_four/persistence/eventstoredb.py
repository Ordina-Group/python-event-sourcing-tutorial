"""A game repository backed by EventStoreDB."""

from __future__ import annotations

import attrs
import esdbclient

from connect_four.domain import events
from connect_four.domain import game as game_


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

    def get(self, game_id: str) -> game_.Game:
        """Get a game from the repository.

        :param game_id: The ID of the game
        :return: An instance of game after applying the stored events to
            ensure the game is in the correct state
        """


def _map_domain_event_to_eventstore_event(
    event: events.GameEvent,
) -> esdbclient.NewEvent:
    """Map a domain event to an eventstore event.

    :param event: the domain event to map
    :return: an eventstore event that can be persisted in EventStoreDB
    """


def _map_eventstore_event_to_domain_event(
    event: esdbclient.RecordedEvent,
) -> events.GameEvent:
    """Map an eventstore event to a domain event.

    :param event: the eventstore event to map
    :return: the equivalent domain event
    """
