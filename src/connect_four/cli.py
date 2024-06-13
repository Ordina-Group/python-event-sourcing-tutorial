from connect_four import presentation
from connect_four.domain import board as domain_board
from connect_four.domain import game as domain_game
from connect_four.domain import result


def _play_in_memory() -> None:
    game = domain_game.Game()

    print("Please enter the name of the players.")
    player_one = input("Player 1: ")
    player_two = input("Player 2: ")
    game.start_game(player_one, player_two)
    print(f"Started a new game between {player_one} and {player_two}.")

    while not game.is_finished:
        print(presentation.generate_board_string(game.board))
        print(f"Next player: {game.next_player}")
        column = _get_move()
        move = domain_game.Move(
            player=game.next_player, column=domain_board.Column(column)
        )
        game.make_move(move)

    print(presentation.generate_board_string(game.board))
    print("The game has finished!")
    match game.result:
        case result.GameResult.PLAYER_ONE_WON:
            print(f"{player_one} has won!")
        case result.GameResult.PLAYER_TWO_WON:
            print(f"{player_two} has won!")
        case result.GameResult.TIED:
            print("It's a tie!")
        case _:
            raise ValueError("The game has ended but the result is not recognized.")

    print("Thank you for playing Connect Four!")


def _get_move() -> domain_board.Column:
    while True:
        column = input("Select column (A-G): ").strip().upper()
        try:
            return domain_board.Column(column)
        except ValueError:
            print("Invalid column. Please try again.")


def main() -> None:
    print("Welcome to a game of Connect Four!")
    print("Have fun...", end="\n\n")
    _play_in_memory()


if __name__ == "__main__":
    main()
