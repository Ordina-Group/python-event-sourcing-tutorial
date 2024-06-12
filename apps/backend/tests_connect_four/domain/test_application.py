import attrs
import pytest
from connect_four.domain import application, board, events, game


@attrs.define
class FakeGameRepository:
    games: dict[str, game.Game] = attrs.field(default=attrs.Factory(dict))

    def add(self, game_obj: game.Game) -> None:
        """"""
        self.games[game_obj.id] = game_obj

    def update(self, game_obj: game.Game) -> None:
        """"""
        self.games[game_obj.id] = game_obj

    def get(self, game_id: str) -> game.Game:
        return self.games[game_id]


@pytest.mark.parametrize(
    ("player_one", "player_two"), [("id_1", "id_2"), ("id_3", "id_4")]
)
def test_application_can_create_game(player_one: str, player_two: str) -> None:
    """"""
    # GIVEN an instance of a game repository
    repository = FakeGameRepository()
    # AND an instance of the application that uses the repository
    app = application.ConnectFourApp(repository)

    # WHEN a game is created
    game_id = app.create_game(player_one=player_one, player_two=player_two)

    # THEN a game_id is returned
    assert isinstance(game_id, str)
    # AND a game with that id was added to the repository
    game_obj = repository.games.get(game_id)
    assert game_obj.id == game_id
    assert game_obj.player_one == player_one
    assert game_obj.player_two == player_two
    # AND the game has a GameStarted event
    assert game_obj.events == [
        events.GameStarted(
            game_id=game_id, player_one=player_one, player_two=player_two
        )
    ]


def test_application_can_make_move_in_game():
    # GIVEN two players
    player_one = "id-1"
    player_two = "id-2"
    # AND a repository with a started game between the players
    repository = FakeGameRepository()
    game_obj = game.Game()
    game_obj.start_game(player_one=player_one, player_two=player_two)
    repository.add(game_obj)
    # AND an application that uses that repository
    app = application.ConnectFourApp(game_repository=repository)
    # AND a move to make
    move = game.Move(player=player_one, column="A", turn=1)

    # WHEN a move is made
    app.make_move(game_obj.id, move)

    # THEN the game has a new MoveMade event
    saved_game = repository.get(game_obj.id)
    assert saved_game.events[-1] == events.MoveMade(
        game_id=game_obj.id, player_id=player_one, column="A"
    )


@pytest.mark.parametrize(
    ("recorded_events", "board_state"),
    [
        pytest.param(
            [
                events.GameStarted(game_id="game-1", player_one="p1", player_two="p2"),
            ],
            {
                "A": [],
                "B": [],
                "C": [],
                "D": [],
                "E": [],
                "F": [],
                "G": [],
            },
            id="No moves",
        ),
        pytest.param(
            [
                events.GameStarted(game_id="game-1", player_one="p1", player_two="p2"),
                events.MoveMade(game_id="game-1", player_id="p1", column="A"),
            ],
            {
                "A": [board.Token.RED],
                "B": [],
                "C": [],
                "D": [],
                "E": [],
                "F": [],
                "G": [],
            },
            id="One moves",
        ),
        pytest.param(
            [
                events.GameStarted(game_id="game-1", player_one="p1", player_two="p2"),
                events.MoveMade(game_id="game-1", player_id="p1", column="A"),
                events.MoveMade(game_id="game-1", player_id="p2", column="A"),
            ],
            {
                "A": [board.Token.RED, board.Token.YELLOW],
                "B": [],
                "C": [],
                "D": [],
                "E": [],
                "F": [],
                "G": [],
            },
            id="Two moves",
        ),
    ],
)
def test_can_get_the_state_of_a_game(
    recorded_events: list[events.GameEvent],
    board_state: dict[str, list[str]],
) -> None:
    # GIVEN a repository with an existing game
    repository = FakeGameRepository()
    game_obj = game.Game(
        id="game-1",
    )
    game_obj.load_from_history(recorded_events)
    repository.add(game_obj)
    # AND an instance of the application that uses that repo
    app = application.ConnectFourApp(game_repository=repository)

    # WHEN the game state is retrieved
    game_state = app.get_game(game_id="game-1")

    # THEN the game state is as expected
    assert game_state == {"player_one": "p1", "player_two": "p2", "board": board_state}
