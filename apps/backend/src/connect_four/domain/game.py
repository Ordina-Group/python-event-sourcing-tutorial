from __future__ import annotations

import enum
import uuid
from collections.abc import Iterator
from typing import Literal

import attrs

from connect_four.domain import events, exceptions


@attrs.define
class Game:
    player_one: str
    player_two: str
    id: str = attrs.field(default=attrs.Factory(lambda: str(uuid.uuid4())))
    events: list[events.GameEvent] = attrs.field(default=attrs.Factory(list))

    def start_game(self) -> None:
        """Start a game.

        This command starts a game and creates a GameStarted event.
        """
        if self.events:
            # If this game already has an event, it means that the game
            # has already been started.
            raise exceptions.GameAlreadyStartedError(
                f"Game {self.id!r} has already started."
            )

        self.events.append(
            events.GameStarted(self.id, self.player_one, self.player_two)
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

        self.events.append(
            events.MoveMade(game_id=self.id, player_id=move.player, column=move.column)
        )

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
    def made_move_events(self) -> Iterator[events.MoveMade]:
        for event in self.events:
            if isinstance(event, events.MoveMade):
                yield event


class Token(enum.Enum):
    RED = "RED"
    YELLOW = "YELLOW"


@attrs.define
class Board:
    _columns: dict[Literal["A", "B", "C", "D", "E", "F", "G"], list[str]] = attrs.field(
        default=attrs.Factory(
            lambda: {
                "A": [],
                "B": [],
                "C": [],
                "D": [],
                "E": [],
                "F": [],
                "G": [],
            }
        )
    )


@attrs.define(frozen=True)
class Move:
    player: str
    column: Literal["A", "B", "C", "D", "E", "F", "G"]
    turn: int
