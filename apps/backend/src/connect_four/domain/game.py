from __future__ import annotations

import uuid
from collections.abc import Iterator
from typing import Literal

import attrs
from connect_four.domain import board
from connect_four.domain import events as domain_events
from connect_four.domain import exceptions


@attrs.define
class Game:
    id: str = attrs.field(default=attrs.Factory(lambda: str(uuid.uuid4())))
    player_one: str | None = None
    player_two: str | None = None
    committed_events: list[domain_events.GameEvent] = attrs.field(
        default=attrs.Factory(list)
    )
    uncommitted_events: list[domain_events.GameEvent] = attrs.field(
        default=attrs.Factory(list)
    )
    result: domain_events.GameResult | None = None
    _board: board.Board = attrs.field(init=False, default=attrs.Factory(board.Board))

    @property
    def events(self) -> list[domain_events.GameEvent]:
        return self.committed_events + self.uncommitted_events

    @property
    def is_finished(self) -> bool:
        """Whether the game has ended."""
        return self.result is not None

    def start_game(self, player_one: str, player_two: str) -> None:
        """Start a game.

        This command starts a game and creates a GameStarted event.
        """
        if self.events:
            # If this game already has an event, it means that the game
            # has already been started.
            raise exceptions.GameAlreadyStartedError(
                f"Game {self.id!r} has already started."
            )

        self.player_one, self.player_two = player_one, player_two
        self.uncommitted_events.append(
            domain_events.GameStarted(self.id, player_one, player_two)
        )

    def make_move(self, move: Move) -> None:
        """Make a move in the game.

        This command makes a move in the game and creates a MoveMade event.

        :param move: the move to make
        """
        if not self._board.has_capacity_in_column(board.Column(move.column)):
            raise exceptions.InvalidMoveError(
                f"Cannot make a move in column {move.column!r} because it is full."
            )
        if self._expected_next_player != move.player:
            raise exceptions.InvalidMoveError(
                f"Player {move.player!r} cannot make a move out of order."
            )

        move_event = domain_events.MoveMade(
            game_id=self.id, player_id=move.player, column=move.column
        )
        self.uncommitted_events.append(move_event)
        self._check_if_game_is_finished_after_move(move_event)

    def _check_if_game_is_finished_after_move(
        self, move_event: domain_events.MoveMade
    ) -> None:
        """Check if the game is finished and emit an event if so.

        :param move_event: The move that was just made.
        """
        self.apply(move_event)
        result = self._board.get_result()
        if result is not None:
            self.result = result
            game_ended = domain_events.GameEnded(game_id=self.id, result=result)
            self.uncommitted_events.append(game_ended)

    def load_from_history(self, events: list[domain_events.GameEvent]) -> None:
        """Load events into game.

        :param events: Events to be added and applied to the game
        """
        self.committed_events = events
        for event in events:
            self.apply(event)

    def apply(self, event: domain_events.GameEvent) -> None:
        """Apply event to the game."""
        match event:
            case domain_events.GameStarted():
                self.player_one = event.player_one
                self.player_two = event.player_two
            case domain_events.MoveMade():
                token = (
                    board.Token.RED
                    if event.player_id == self.player_one
                    else board.Token.YELLOW
                )
                column = board.Column(event.column)
                self._board.add_move(column, token)
            case domain_events.GameEnded(result=result):
                self.result = result

    @property
    def _expected_next_player(self) -> str:
        made_move_events = list(self.made_move_events)
        return self.player_one if len(made_move_events) % 2 == 0 else self.player_two

    @property
    def board(self) -> dict[str, list[board.Token]]:
        """The current state of the board."""
        board_state = self._board.board_state
        return {col: board_state[board.Column(col)] for col in "ABCDEFG"}

    @property
    def made_move_events(self) -> Iterator[domain_events.MoveMade]:
        for event in self.events:
            if isinstance(event, domain_events.MoveMade):
                yield event


@attrs.define(frozen=True)
class Move:
    player: str
    column: Literal["A", "B", "C", "D", "E", "F", "G"]
    turn: int
