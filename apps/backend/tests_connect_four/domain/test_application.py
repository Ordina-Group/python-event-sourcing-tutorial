from connect_four.domain import application


def test_application_can_create_game() -> None:
    """"""
    # GIVEN an instance of the application
    app = application.ConnectFourApp()
    # AND the id of two players
    player_one = "id-1"
    player_two = "id-2"

    # WHEN a game is created
    game_id = app.create_game(player_one=player_one, player_two=player_two)

    # THEN the game is available
    assert app.get_game(game_id=game_id) == {
        "player_one": player_one,
        "player_two": player_two,
        "events": [],
    }


def test_application_can_create_game_2() -> None:
    """"""
    # GIVEN an instance of the application
    app = application.ConnectFourApp()
    # AND the id of two players
    player_one = "id-3"
    player_two = "id-4"

    # WHEN a game is created
    game_id = app.create_game(player_one=player_one, player_two=player_two)

    # THEN the game is available
    assert app.get_game(game_id=game_id) == {
        "player_one": player_one,
        "player_two": player_two,
        "events": [],
    }
