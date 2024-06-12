import enum
import itertools
from collections.abc import Iterator
from typing import Any, Final, Iterable, Literal, TypeAlias

import attrs
import colorama
import more_itertools

from connect_four.domain import events

_NUMBER_OF_ROWS: Final = 6
BoardState: TypeAlias = "dict[Column, list[Token]]"
# These are hardcoded diagonals of the board to remove the need for an
# algorithmic approach. Only diagonals that are long enough to contain
# a winning sequence of tokens are included.
#
# As a sidenote, it is a nice puzzle to come up with a general solution
# for yielding the diagonals of a "list of lists"-style matrix in pure
# Python, but it's beyond the scope of this workshop :).
_FORWARD_DIAGONALS = [
    list(zip(range(0, 4), range(2, 6))),
    list(zip(range(0, 5), range(1, 6))),
    list(zip(range(0, 6), range(0, 6))),
    list(zip(range(1, 7), range(0, 6))),
    list(zip(range(2, 7), range(0, 5))),
    list(zip(range(3, 7), range(0, 4))),
]
_BACKWARD_DIAGONALS = [
    list(zip(range(0, 4), range(3, -1, -1))),
    list(zip(range(0, 5), range(4, -1, -1))),
    list(zip(range(0, 6), range(5, -1, -1))),
    list(zip(range(1, 7), range(5, -1, -1))),
    list(zip(range(2, 7), range(5, 0, -1))),
    list(zip(range(3, 7), range(5, 1, -1))),
]


class Column(enum.Enum):
    """A column in a board."""

    A = "A"
    B = "B"
    C = "C"
    D = "D"
    E = "E"
    F = "F"
    G = "G"


class Token(enum.Enum):
    """A token for a game of Connect Four."""

    RED = "RED"
    YELLOW = "YELLOW"


@attrs.define
class Board:
    """A "Connect Four"-board."""

    _board_state: BoardState = attrs.field(
        default=attrs.Factory(lambda: {col: [] for col in Column}),
    )

    def get_winner(self) -> Token | None:
        """The winning token color or None if there is no winner."""
        sequences_to_check = [*self.columns, *self.rows, *self.diagonals]
        for token_sequence in itertools.chain(sequences_to_check):
            if (winner := _get_winner(token_sequence)) is not None:
                return winner
        return None

    def get_result(self) -> events.GameResult | None:
        """Get the result of this board if it's in a finished state."""
        if (winner := self.get_winner()) is not None:
            return (
                events.GameResult.PLAYER_ONE_WON
                if winner == Token.RED
                else events.GameResult.PLAYER_TWO_WON
            )
        if self.is_full:
            return events.GameResult.TIED
        return None

    @property
    def is_full(self) -> bool:
        """Whether the game ended in a tie."""
        return not any(self.has_capacity_in_column(col) for col in Column)

    @property
    def columns(self) -> Iterator[list[Token | None]]:
        """An iterator that yields columns.

        To ensure a 6 rows by 7 columns board, the columns are padded
        with `None`-values if a column isn't completed filed. This makes
        transposing the board to rows and diagonals easier.
        """
        return (
            list(more_itertools.padded(col, fillvalue=None, n=_NUMBER_OF_ROWS))
            for col in self._board_state.values()
        )

    @property
    def rows(self) -> Iterator[list[Token | None]]:
        """An iterator that yields columns."""
        return (list(row) for row in more_itertools.transpose(self.columns))

    @property
    def diagonals(self) -> Iterator[list[Token | None]]:
        board = list(self.columns)
        for diagonal in itertools.chain(_FORWARD_DIAGONALS, _BACKWARD_DIAGONALS):
            yield [board[col][row] for col, row in diagonal]

    @property
    def board_state(self) -> BoardState:
        """A deep copy of the board state."""
        return attrs.asdict(self)["_board_state"]

    def add_move(self, column: Column, token: Token) -> None:
        """Add a token to the specified column.

        :param column: the receiving column
        :param token: the token to place in the column
        """
        self._board_state[column].append(token)

    def has_capacity_in_column(self, column: Column) -> bool:
        """Return `True` if the column has the capacity for a token.

        :param column: the column to check
        :return: True if the column has the capacity to receive a token,
          False otherwise
        """
        return len(self._board_state[column]) < _NUMBER_OF_ROWS

    def __str__(self) -> str:
        return _generate_board_string(self._board_state)


def _get_winner(tokens: Iterable[Token]) -> Token | None:
    """Check the iterable with tokens for a winning sequence.

    :param tokens: the sequence of tokens to check
    :return: the winning token color if the iterable contains a winning
      sequence of four connected tokens or None if the iterable does not
      contain a winning subsequence.
    """
    for group in more_itertools.sliding_window(tokens, 4):
        if group[0] is not None and _all_equal(group):
            return group[0]

    return None


def _all_equal(iterable: Iterable[Any]) -> bool:
    """Return True if all items in the iterable are equal.

    :param iterable: the iterable to check
    :return: True if all elements are equal to each other
    """
    return all(a == b for a, b in more_itertools.sliding_window(iterable, 2))


def _colorize_string(string: str, color: str) -> str:
    """Colorize a string.

    :param string: the string to colorize
    :param color: the color to use
    :return: the colorized string
    """
    return f"{color}{string}{colorama.Style.RESET_ALL}"


def _colorize_token(token: Token) -> str:
    """Colorize a token based on its type.

    :param token: the token to colorize
    :return: the colorized token
    """
    color = (
        colorama.Fore.LIGHTRED_EX
        if token == Token.RED
        else colorama.Fore.LIGHTYELLOW_EX
    )
    return _colorize_string("●", color)


def _generate_board_string(board_state: BoardState) -> str:
    """Generate a string representation of the board.

    :param board_state: the state of the board
    :return: a string representation of the board
    """
    board = [[" " for _ in range(7)] for _ in range(6)]

    # Fill the board based on the moves
    for col, player_moves in board_state.items():
        for row, player in enumerate(player_moves):
            board[5 - row][ord(col.value) - ord("A")] = _colorize_token(player)

    # Define the top border with column numbers
    # Define the top border with column numbers
    top_border = _colorize_string(
        "  A   B   C   D   E   F   G", colorama.Fore.LIGHTWHITE_EX
    )
    horizontal_border = _colorize_string(
        "╔═══╦═══╦═══╦═══╦═══╦═══╦═══╗", colorama.Fore.BLUE
    )
    row_separator = _colorize_string(
        "╠═══╬═══╬═══╬═══╬═══╬═══╬═══╣", colorama.Fore.BLUE
    )
    bottom_border = _colorize_string(
        "╚═══╩═══╩═══╩═══╩═══╩═══╩═══╝", colorama.Fore.BLUE
    )
    separator = _colorize_string("║", colorama.Fore.BLUE)

    # Generate the board string
    board_string = [top_border, horizontal_border]
    for row in board[:-1]:
        board_string.append(
            f"{separator} " + f" {separator} ".join(row) + f" {separator}"
        )
        board_string.append(row_separator)
    # Add the last row without a row separator afterward
    board_string.append(
        f"{separator} " + f" {separator} ".join(board[-1]) + f" {separator}"
    )
    board_string.append(bottom_border)

    return "\n".join(board_string)
