"""The `Game` aggregate root."""

from __future__ import annotations

import attrs

import connect_four.domain.result
from connect_four.domain import board
from connect_four.domain import events as events_
from connect_four.domain import exceptions


@attrs.define
class Game:
    """A game of Connect Four."""

    player_one: str | None = None
    player_two: str | None = None
    next_player: str | None = None
    result: connect_four.domain.result.GameResult | None = None
    events: list[events_.GameEvent] = attrs.field(default=attrs.Factory(list))
    _board: board.Board = attrs.field(init=False, default=attrs.Factory(board.Board))

    @property
    def has_started(self) -> bool:
        """True if the game has been started.

        Since the `GameStarted` event is required to be the first event
        in the sequence of `Game`-events, we can simply check if there
        are any events for this game.
        """
        return bool(self.events)

    def start_game(self, player_one: str, player_two: str) -> None:
        """Start a game.

        :param player_one: the name of player one
        :param player_two: the name of player two
        """
        if self.has_started:
            raise exceptions.GameAlreadyStartedError("The game has already started.")

        game_started = events_.GameStarted(player_one, player_two)
        self._process_event(game_started)

    def _process_event(self, event: events_.GameEvent) -> None:
        """Apply the event and add it to the list of events.

        :param event: The event to process
        """
        self.apply(event)
        self.events.append(event)

    def make_move(self, move: Move) -> None:
        """Make a move in the game.

        :param move: the move to make
        """

    def apply(self, event: events_.GameEvent) -> None:
        """Apply an event to the game aggregate.

        :param event: the event
        :raises ValueError: if the event is unknown
        """
        match event:
            case events_.GameStarted(player_one=player_one, player_two=player_two):
                self.player_one = player_one
                self.player_two = player_two
            case _:
                raise ValueError(f"Unknown event: {event}")

    @property
    def is_finished(self) -> bool:
        """Whether the game has ended."""
        return False

    @property
    def board(self) -> board.BoardState:
        """The current state of the board."""
        return self._board.board_state


@attrs.define(frozen=True)
class Move:
    """A move in the game."""

    player: str
    column: board.Column
