from __future__ import annotations

import uuid
from typing import Literal

import attrs

from connect_four.domain import events


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
        self.events.append(
            events.GameStarted(self.id, self.player_one, self.player_two)
        )

    def make_move(self, move: Move) -> None:
        """Make a move in the game.

        This command makes a move in the game and creates a MoveMade event.
        """
        self.events.append(events.MoveMade(self.id, column=move.column))


@attrs.define(frozen=True)
class Move:
    player: str
    column: Literal["A", "B", "C", "D", "E", "F", "G"]
    turn: int
