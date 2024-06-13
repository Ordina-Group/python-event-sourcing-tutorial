import esdbclient

from connect_four import application, presentation
from connect_four.domain import board, game, result
from connect_four.persistence import eventstoredb

_CONNECTION_STRING = "esdb://localhost:2113?tls=false"


def _play() -> None:
    client = esdbclient.EventStoreDBClient(uri=_CONNECTION_STRING)
    repository = eventstoredb.GameRepository(client=client)
    app = application.ConnectFourApp(game_repository=repository)

    print("Welcome to a new game of Connect Four!")
    print("This version of the game uses EventStoreDB to store the game events.")
    print("========================================")
    print("Please enter the name of the players")
    player_one = input("Player 1: ")
    player_two = input("Player 2: ")
    game_id = app.create_game(player_one=player_one, player_two=player_two)

    print()
    print("========================================")
    print(f"Started a new game between {player_one} and {player_two}.")
    print(f"The game id is {game_id!r}", end="\n\n")

    game_state = app.get_game(game_id)
    while not game_state.is_finished:
        print(presentation.generate_board_string(game_state.board))
        print(f"Next player: {game_state.next_player}")
        move = game.Move(player=game_state.next_player, column=_get_move())
        app.make_move(game_id=game_id, move=move)
        game_state = app.get_game(game_id)
        print("\n\n")

    print(presentation.generate_board_string(game_state.board))

    print("That move finished the game and...")
    match game_state.result:
        case result.GameResult.PLAYER_ONE_WON:
            print(f"{player_one} has won!")
        case result.GameResult.PLAYER_TWO_WON:
            print(f"{player_two} has won!")
        case result.GameResult.TIED:
            print("it's a tie!")
        case _:
            raise ValueError("The game has ended but the result is not recognized.")

    print("\n\nThank you for playing Connect Four!")


def _get_move() -> board.Column:
    while True:
        column = input("Select column (A-G): ").strip().upper()
        try:
            return board.Column(column)
        except ValueError:
            print("Invalid column. Please try again.")


if __name__ == "__main__":
    _play()
