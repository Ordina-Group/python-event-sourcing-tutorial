"""It's the journey that matters, not the destination...

Unless it's a game, then you need to know the destination. This module
holds a simple result enum to identify the three possible outcomes of a
game of Connect Four.
"""

import enum


class GameResult(enum.StrEnum):
    """The result of a game."""

    PLAYER_ONE_WON = "PLAYER_ONE_WON"
    TIED = "TIED"
    PLAYER_TWO_WON = "PLAYER_TWO_WON"
