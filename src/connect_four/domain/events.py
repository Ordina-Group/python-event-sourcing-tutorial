from __future__ import annotations

import enum
from typing import Literal, Protocol

import attrs

from connect_four.domain import board


class GameEvent(Protocol):
    game_id: str


@attrs.define(frozen=True)
class MoveMade:
    game_id: str
    player_id: str
    column: board.Column


@attrs.define(frozen=True)
class GameStarted:
    game_id: str
    player_one: str
    player_two: str


class GameResult(enum.Enum):
    PLAYER_ONE_WON = "PLAYER_ONE_WON"
    TIED = "TIED"
    PLAYER_TWO_WON = "PLAYER_TWO_WON"


@attrs.define(frozen=True)
class GameEnded(GameEvent):
    game_id: str
    result: GameResult
