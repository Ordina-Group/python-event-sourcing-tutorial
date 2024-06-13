from connect_four.domain import game as domain_game


def _play_game() -> None:
    game = domain_game.Game()

    print("Please enter the name of the players.")
    player_one = input("Player 1: ")
    player_two = input("Player 2: ")
    game.start_game(player_one, player_two)
    print(f"Started a new game between {game.player_one} and {game.player_two}.")


def main() -> None:
    print("Welcome to a game of Connect Four!")
    print("Have fun...", end="\n\n")
    _play_game()


if __name__ == "__main__":
    main()
