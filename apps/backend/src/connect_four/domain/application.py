from __future__ import annotations
from typing import Protocol, TypedDict

import attrs

from connect_four.domain import game as game_models


@attrs.define
class ConnectFourApp:
    _game_repository: IGameRepository

    def create_game(self, player_one: str, player_two: str) -> str:
        """Create a new game and start it.

        :param player_one: the ID of the first player
        :param player_two: the ID of the second player
        :return: the ID of the game that was created
        """
        game = game_models.Game(player_one, player_two)
        game.start_game()
        self._game_repository.add(game)
        return game.id

    def make_move(self, game_id: str, move: game_models.Move) -> None:
        game = self._game_repository.get(game_id)
        game.make_move(move)

    def get_game(self, game_id: str) -> GameState:
        """Get the current state of a game.

        :param game_id: the ID of the game
        :return: the state of the game aggregate
        """
        game = self._game_repository.get(game_id)
        return GameState(
            player_one=game.player_one,
            player_two=game.player_two,
            board=game.board_state,
        )


class GameState(TypedDict):
    player_one: str
    player_two: str
    board: dict[str, list[game_models.Token]]


class IGameRepository(Protocol):
    def add(self, game: game_models.Game) -> None:
        """Add a game in the repository.

        :param game: The game to save
        """

    def get(self, game_id: str) -> game_models.Game:
        """Get a game from the repository.

        :param game_id: The ID of the game to get
        :return: The game with the given ID
        """
