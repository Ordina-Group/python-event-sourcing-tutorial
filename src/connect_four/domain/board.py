"""A board class that implements some of the game logic."""

import enum
import itertools
from collections.abc import Iterator
from typing import Any, Final, Iterable, TypeAlias

import attrs
import more_itertools

from connect_four.domain import result

BoardState: TypeAlias = "dict[Column, list[Token]]"


class Column(enum.StrEnum):
    """A column in a board."""

    A = "A"
    B = "B"
    C = "C"
    D = "D"
    E = "E"
    F = "F"
    G = "G"


class Token(enum.StrEnum):
    """A token for a game of Connect Four."""

    RED = "RED"
    YELLOW = "YELLOW"


@attrs.define
class Board:
    """A "Connect Four"-board."""

    _board_state: BoardState = attrs.field(
        default=attrs.Factory(lambda: {col: [] for col in Column}),
    )

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

    def has_room_in_column(self, column: Column) -> bool:
        """Return `True` if the column has the capacity for a token.

        :param column: the column to check
        :return: True if the column has the capacity to receive a token,
          False otherwise
        """
        return len(self._board_state[column]) < _NUMBER_OF_ROWS

    def get_result(self) -> result.GameResult | None:
        """Get the result of this board if it's in a finished state."""
        if (winner := self._get_winner()) is not None:
            return (
                result.GameResult.PLAYER_ONE_WON
                if winner == Token.RED
                else result.GameResult.PLAYER_TWO_WON
            )
        if self._check_if_space_available():
            return result.GameResult.TIED
        return None

    # ------------------------------------------------------------------
    # Private methods that you don't have to pay attention to for this
    # workshop.

    def _get_winner(self) -> Token | None:
        """The winning token color or None if there is no winner."""
        sequences_to_check = [
            *self._get_columns(),
            *self._get_rows(),
            *self._get_diagonals(),
        ]
        for token_sequence in itertools.chain(sequences_to_check):
            if (winner := _get_winner(token_sequence)) is not None:
                return winner
        return None

    def _check_if_space_available(self) -> bool:
        """Whether the game ended in a tie."""
        return not any(self.has_room_in_column(col) for col in Column)

    def _get_columns(self) -> Iterator[list[Token | None]]:
        """Get an iterator that yields columns.

        To ensure a 6 rows by 7 columns board, the columns are padded
        with `None`-values if a column isn't completed filed. This makes
        transposing the board to rows and diagonals easier.
        """
        return (
            list(more_itertools.padded(col, fillvalue=None, n=_NUMBER_OF_ROWS))
            for col in self._board_state.values()
        )

    def _get_rows(self) -> Iterator[list[Token | None]]:
        """Get an iterator that yields columns."""
        return (list(row) for row in more_itertools.transpose(self._get_columns()))

    def _get_diagonals(self) -> Iterator[list[Token | None]]:
        """Get an iterator that yields diagonals."""
        board = list(self._get_columns())
        for diagonal in itertools.chain(_FORWARD_DIAGONALS, _BACKWARD_DIAGONALS):
            yield [board[col][row] for col, row in diagonal]


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


_NUMBER_OF_ROWS: Final = 6
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
