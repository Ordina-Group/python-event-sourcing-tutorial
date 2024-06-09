from __future__ import annotations

import enum
import uuid
from collections.abc import Iterator
from typing import Literal

import attrs
from connect_four.domain import events as domain_events
from connect_four.domain import exceptions


@attrs.define
class Game:
    id: str = attrs.field(default=attrs.Factory(lambda: str(uuid.uuid4())))
    player_one: str | None = attrs.field(default=None)
    player_two: str | None = attrs.field(default=None)
    committed_events: list[domain_events.GameEvent] = attrs.field(
        default=attrs.Factory(list)
    )
    uncommitted_events: list[domain_events.GameEvent] = attrs.field(
        default=attrs.Factory(list)
    )

    @property
    def events(self) -> list[domain_events.GameEvent]:
        return self.committed_events + self.uncommitted_events

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
        if len(self.board_state[move.column]) >= 6:
            raise exceptions.InvalidMoveError(
                f"Cannot make a move in column {move.column!r} because it is full."
            )
        if self._expected_next_player != move.player:
            raise exceptions.InvalidMoveError(
                f"Player {move.player!r} cannot make a move out of order."
            )

        self.uncommitted_events.append(
            domain_events.MoveMade(
                game_id=self.id, player_id=move.player, column=move.column
            )
        )

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
                ...

    @property
    def _expected_next_player(self) -> str:
        made_move_events = list(self.made_move_events)
        return self.player_one if len(made_move_events) % 2 == 0 else self.player_two

    @property
    def board_state(self) -> dict[str, list[Token]]:
        """The current state of the board."""
        board = {
            "A": [],
            "B": [],
            "C": [],
            "D": [],
            "E": [],
            "F": [],
            "G": [],
        }
        for event in self.made_move_events:
            token = Token.RED if event.player_id == self.player_one else Token.YELLOW
            board[event.column].append(token)
        return board

    @property
    def made_move_events(self) -> Iterator[domain_events.MoveMade]:
        for event in self.events:
            if isinstance(event, domain_events.MoveMade):
                yield event


class Token(enum.Enum):
    RED = "RED"
    YELLOW = "YELLOW"


@attrs.define(frozen=True)
class Move:
    player: str
    column: Literal["A", "B", "C", "D", "E", "F", "G"]
    turn: int
