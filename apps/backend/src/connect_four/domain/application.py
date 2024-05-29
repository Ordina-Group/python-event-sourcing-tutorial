from __future__ import annotations
import uuid
from typing import Protocol

import attrs


@attrs.define
class ConnectFourApp:
    _game_repository: IGameRepository

    def create_game(self, player_one: str, player_two: str) -> str:
        """Create a new game.

        :param player_one: the ID of the first player
        :param player_two: the ID of the second player
        :return: the ID of the game that was created
        """
        game = Game(player_one, player_two)
        # self.games_repository.save(game)
        return game.id

    # def get_game(self, game_id: str) -> dict[str, str | list[str]]:
    #     """Get the current state of a game.
    #
    #     :param game_id: the ID of the game
    #     :return: the state of the game aggregate
    #     """
    #     return {
    #         "player_one": "id-1",
    #         "player_two": "id-2",
    #         "events": [],
    #     }


class IGameRepository(Protocol):
    def save(self, game: Game) -> None:
        """Save a game in the repository.

        :param game: The game to save
        """


# class GamesRepository:
#     def save(self, game: Game) -> None:
#         pass


@attrs.define
class Game:
    player_one: str
    player_two: str
    id: str = attrs.field(default=attrs.Factory(lambda: str(uuid.uuid4())))
