import esdbclient

from connect_four.domain import application
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
