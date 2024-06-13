import attrs


@attrs.define(frozen=True)
class GameStarted:
    """Event that is fired when a game is started."""
