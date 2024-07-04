"""The `Game` aggregate root."""

from __future__ import annotations

import uuid
from collections.abc import Iterable

import attrs

import connect_four.domain.result
from connect_four.domain import board
from connect_four.domain import events as events_
from connect_four.domain import exceptions


@attrs.define
class Game:
    """A game of Connect Four."""

    id: str = attrs.field(default=attrs.Factory(lambda: str(uuid.uuid4())))
    player_one: str | None = None
    player_two: str | None = None
    next_player: str | None = None
    result: connect_four.domain.result.GameResult | None = None
    historical_events: list[events_.GameEvent] = attrs.field(
        default=attrs.Factory(list)
    )
    uncommited_events: list[events_.GameEvent] = attrs.field(
        default=attrs.Factory(list)
    )
    _board: board.Board = attrs.field(init=False, default=attrs.Factory(board.Board))

    @property
    def has_started(self) -> bool:
        """True if the game has been started.

        Since the `GameStarted` event is required to be the first event
        in the sequence of `Game`-events, we can simply check if there
        are any events for this game.
        """
        return bool(self.events)

    @property
    def events(self) -> list[events_.GameEvent]:
        """Both historical and uncommited events."""
        return self.historical_events + self.uncommited_events

    def start_game(self, player_one: str, player_two: str) -> None:
        """Start a game.

        :param player_one:
        :param player_two:
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
        self.uncommited_events.append(event)

    def make_move(self, move: Move) -> None:
        """Make a move in the game.

        :param move: the move to make
        """
        if not self.has_started:
            raise exceptions.InvalidMoveError(
                "The game must be started before a move can be made."
            )
        if self.is_finished:
            raise exceptions.InvalidMoveError(
                "The game must be ongoing to make a move."
            )
        if self.next_player != move.player:
            raise exceptions.InvalidMoveError(
                f"It must be the turn of {move.player!r} for that player to make a"
                f" move."
            )
        if not self._board.has_room_in_column(move.column):
            raise exceptions.InvalidMoveError(f"Column must have room for a token.")

        move_made = events_.MoveMade(move.player, move.column)
        self._process_event(move_made)
        self._check_if_game_is_finished()

    def _check_if_game_is_finished(self) -> None:
        """Check if the game is finished and emit an event if so."""
        if (result := self._board.get_result()) is None:
            return

        game_ended = events_.GameFinished(result)
        self._process_event(game_ended)

    def apply(self, event: events_.GameEvent) -> None:
        """Apply an event to the game aggregate.

        :param event: the event
        :raises ValueError: if the event is unknown
        """
        match event:
            case events_.GameStarted(player_one=player_one, player_two=player_two):
                self.player_one = player_one
                self.player_two = player_two
                self.next_player = player_one
            case events_.MoveMade(player=player, column=column):
                token = (
                    board.Token.RED if player == self.player_one else board.Token.YELLOW
                )
                self._board.add_move(column, token)
                self.next_player = (
                    self.player_two if player == self.player_one else self.player_one
                )
            case events_.GameFinished(result=result):
                self.result = result
                self.next_player = None
            case _:
                raise ValueError(f"Unknown event: {event}")

    def load_from_history(self, historic_events: Iterable[events_.GameEvent]) -> None:
        """Load the game state from historic events.

        :param historic_events: the historic events
        """
        self.historical_events = list(historic_events)
        for event in self.events:
            self.apply(event)

    @property
    def is_finished(self) -> bool:
        """Whether the game has ended."""
        return self.result is not None

    @property
    def board(self) -> board.BoardState:
        """The current state of the board."""
        return self._board.board_state


@attrs.define(frozen=True)
class Move:
    """A move in a game of Connect Four."""

    player: str
    column: board.Column
