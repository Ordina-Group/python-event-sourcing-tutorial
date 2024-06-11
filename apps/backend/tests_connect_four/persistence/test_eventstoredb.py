import esdbclient
from connect_four.domain import application, game
from connect_four.persistence import eventstoredb


def test_application_with_eventstoredb_stores_game_started_event() -> None:
    # GIVEN an eventstoredb client
    client = esdbclient.EventStoreDBClient(uri="esdb://localhost:2113?tls=false")
    # AND an eventstoredb-backed game repository using that client
    repository = eventstoredb.GameRepository(client)
    # AND a Connect Four application that uses that repository
    app = application.ConnectFourApp(repository)

    # WHEN a game is created
    game_id = app.create_game(player_one="player-1", player_two="player-2")

    # THEN the game has been persisted in the game's event stream
    recorded_events = client.get_stream(stream_name=f"game-{game_id}")
    assert len(recorded_events) == 1


def test_application_with_eventstoredb_can_get_a_game() -> None:
    # GIVEN an eventstoredb client
    client = esdbclient.EventStoreDBClient(uri="esdb://localhost:2113?tls=false")
    # AND an eventstoredb-backed game repository using that client
    repository = eventstoredb.GameRepository(client)
    # AND a Connect Four application that uses that repository
    app = application.ConnectFourApp(repository)
    # AND a game created for this application
    game_id = app.create_game(player_one="player-1", player_two="player-2")

    # WHEN the game state is retrieved from the repository
    game_state = app.get_game(game_id=game_id)

    # THEN the players are correct
    assert game_state["player_one"] == "player-1"
    assert game_state["player_two"] == "player-2"


def test_application_with_eventstoredb_stores_movemade_event() -> None:
    # GIVEN an eventstoredb client
    client = esdbclient.EventStoreDBClient(uri="esdb://localhost:2113?tls=false")
    # AND an eventstoredb-backed game repository using that client
    repository = eventstoredb.GameRepository(client)
    # AND a Connect Four application that uses that repository
    app = application.ConnectFourApp(repository)
    # AND a game is created
    game_id = app.create_game(player_one="player-1", player_two="player-2")

    # WHEN a move is made
    move = game.Move(player="player-1", column="A", turn=1)
    app.make_move(game_id=game_id, move=move)

    # THEN the game move been persisted in the game's event stream
    recorded_events = client.get_stream(stream_name=f"game-{game_id}")
    assert len(recorded_events) == 2

    # AND the game can be reconstructed
    game_state = app.get_game(game_id=game_id)

    # AND THE First move is player-1 in column A
    assert game_state["board"]["A"] == [game.Token.RED]
