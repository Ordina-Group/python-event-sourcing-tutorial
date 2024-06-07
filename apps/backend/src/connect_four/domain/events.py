from __future__ import annotations

from typing import Literal, Protocol

import attrs


class GameEvent(Protocol):
    game_id: str


@attrs.define(frozen=True)
class MoveMade:
    game_id: str
    player_id: str
    column: Literal["A", "B", "C", "D", "E", "F", "G"]


@attrs.define(frozen=True)
class GameStarted:
    game_id: str
    player_one: str
    player_two: str
