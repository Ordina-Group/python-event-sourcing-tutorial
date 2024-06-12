import pytest
from connect_four.domain import board


@pytest.mark.parametrize("column_to_check", [*board.Column])
def test_board_indicates_that_column_is_full(column_to_check: board.Column) -> None:
    """The capacity of all columns can be checked."""
    # GIVEN a board state with a specific column at capacity
    board_state: dict[board.Column, list[board.Token]] = {
        board.Column.A: [],
        board.Column.B: [],
        board.Column.C: [],
        board.Column.D: [],
        board.Column.E: [],
        board.Column.F: [],
        board.Column.G: [],
        # Fill the column to check
        column_to_check: [
            board.Token.RED,
            board.Token.YELLOW,
            board.Token.RED,
            board.Token.YELLOW,
            board.Token.RED,
            board.Token.YELLOW,
        ],
    }
    # AND a board with that board state
    board_instance = board.Board(board_state=board_state)

    # WHEN a column that is full is checked for capacity
    has_capacity = board_instance.has_capacity_in_column(column_to_check)

    # THEN the board indicated that the column has no capacity left
    assert not has_capacity


@pytest.mark.parametrize(
    ("winning_state", "expected_winner"),
    [
        pytest.param(
            {
                board.Column.A: [
                    board.Token.RED,
                    board.Token.RED,
                    board.Token.RED,
                    board.Token.RED,
                ],
                board.Column.B: [
                    board.Token.YELLOW,
                    board.Token.YELLOW,
                    board.Token.YELLOW,
                ],
                board.Column.C: [],
                board.Column.D: [],
                board.Column.E: [],
                board.Column.F: [],
                board.Column.G: [],
            },
            board.Token.RED,
            id="red col A victory",
        ),
        pytest.param(
            {
                board.Column.A: [
                    board.Token.RED,
                    board.Token.RED,
                    board.Token.RED,
                ],
                board.Column.B: [
                    board.Token.YELLOW,
                    board.Token.YELLOW,
                    board.Token.YELLOW,
                    board.Token.YELLOW,
                ],
                board.Column.C: [],
                board.Column.D: [],
                board.Column.E: [],
                board.Column.F: [],
                board.Column.G: [board.Token.RED],
            },
            board.Token.YELLOW,
            id="yellow col B victory",
        ),
        pytest.param(
            {
                board.Column.A: [
                    board.Token.RED,
                    board.Token.YELLOW,
                ],
                board.Column.B: [
                    board.Token.RED,
                    board.Token.YELLOW,
                ],
                board.Column.C: [
                    board.Token.RED,
                    board.Token.YELLOW,
                ],
                board.Column.D: [
                    board.Token.RED,
                ],
                board.Column.E: [],
                board.Column.F: [],
                board.Column.G: [],
            },
            board.Token.RED,
            id="red row 1 victory",
        ),
        pytest.param(
            {
                board.Column.A: [
                    board.Token.RED,
                ],
                board.Column.B: [
                    board.Token.RED,
                    board.Token.YELLOW,
                ],
                board.Column.C: [
                    board.Token.RED,
                    board.Token.YELLOW,
                ],
                board.Column.D: [
                    board.Token.YELLOW,
                    board.Token.YELLOW,
                ],
                board.Column.E: [board.Token.RED, board.Token.YELLOW],
                board.Column.F: [],
                board.Column.G: [board.Token.RED],
            },
            board.Token.YELLOW,
            id="yellow row 2 with gap victory",
        ),
        pytest.param(
            {
                board.Column.A: [
                    board.Token.RED,
                ],
                board.Column.B: [
                    board.Token.YELLOW,
                    board.Token.RED,
                ],
                board.Column.C: [
                    board.Token.YELLOW,
                    board.Token.YELLOW,
                    board.Token.RED,
                ],
                board.Column.D: [
                    board.Token.RED,
                    board.Token.YELLOW,
                    board.Token.RED,
                    board.Token.RED,
                ],
                board.Column.E: [board.Token.YELLOW],
                board.Column.F: [],
                board.Column.G: [],
            },
            board.Token.RED,
            id="red forward diagonal victory",
        ),
        pytest.param(
            {
                board.Column.A: [
                    board.Token.RED,
                    board.Token.RED,
                    board.Token.RED,
                    board.Token.YELLOW,
                ],
                board.Column.B: [
                    board.Token.YELLOW,
                    board.Token.RED,
                    board.Token.YELLOW,
                ],
                board.Column.C: [
                    board.Token.RED,
                    board.Token.YELLOW,
                ],
                board.Column.D: [
                    board.Token.YELLOW,
                ],
                board.Column.E: [],
                board.Column.F: [],
                board.Column.G: [],
            },
            board.Token.YELLOW,
            id="yellow backward diagonal victory",
        ),
    ],
)
def test_winner_returns_winner_for_winning_board(
    winning_state: board.BoardState, expected_winner: board.Token
) -> None:
    """If a board is in a winning state, it returns the winner."""
    # GIVEN a board with a winning state
    board_instance = board.Board(board_state=winning_state)

    # WHEN the winner is retrieved
    winner = board_instance.get_winner()

    # THEN the winner is as expected
    assert winner == expected_winner


@pytest.mark.parametrize(
    "board_state",
    [
        pytest.param(
            {
                board.Column.A: [],
                board.Column.B: [],
                board.Column.C: [],
                board.Column.D: [],
                board.Column.E: [],
                board.Column.F: [],
                board.Column.G: [],
            },
            id="new game",
        ),
        pytest.param(
            {
                board.Column.A: [
                    board.Token.RED,
                    board.Token.RED,
                    board.Token.RED,
                ],
                board.Column.B: [
                    board.Token.YELLOW,
                    board.Token.YELLOW,
                    board.Token.YELLOW,
                ],
                board.Column.C: [],
                board.Column.D: [],
                board.Column.E: [],
                board.Column.F: [],
                board.Column.G: [],
            },
            id="ongoing game",
        ),
        pytest.param(
            {
                board.Column.A: [
                    board.Token.RED,
                    board.Token.RED,
                    board.Token.RED,
                    board.Token.YELLOW,
                    board.Token.RED,
                    board.Token.YELLOW,
                ],
                board.Column.B: [
                    board.Token.YELLOW,
                    board.Token.YELLOW,
                    board.Token.YELLOW,
                    board.Token.RED,
                    board.Token.RED,
                    board.Token.YELLOW,
                ],
                board.Column.C: [
                    board.Token.RED,
                    board.Token.RED,
                    board.Token.YELLOW,
                    board.Token.RED,
                    board.Token.YELLOW,
                    board.Token.RED,
                ],
                board.Column.D: [
                    board.Token.YELLOW,
                    board.Token.YELLOW,
                    board.Token.YELLOW,
                    board.Token.RED,
                    board.Token.RED,
                ],
                board.Column.E: [
                    board.Token.RED,
                    board.Token.YELLOW,
                    board.Token.RED,
                    board.Token.YELLOW,
                    board.Token.RED,
                    board.Token.YELLOW,
                ],
                board.Column.F: [
                    board.Token.YELLOW,
                    board.Token.YELLOW,
                    board.Token.RED,
                    board.Token.YELLOW,
                    board.Token.YELLOW,
                    board.Token.YELLOW,
                ],
                board.Column.G: [
                    board.Token.YELLOW,
                    board.Token.RED,
                    board.Token.YELLOW,
                    board.Token.RED,
                    board.Token.RED,
                    board.Token.RED,
                ],
            },
            id="tied game",
        ),
    ],
)
def test_winner_returns_none_for_board_without_a_winner(
    board_state: board.BoardState,
) -> None:
    """There is no winner if no one has won the game (yet)."""
    # GIVEN a board with a board state without a winner
    board_instance = board.Board(board_state=board_state)

    # WHEN the winner is retrieved
    winner = board_instance.get_winner()

    # THEN the winner is None
    assert winner is None


def test_full_returns_true_if_all_columns_are_filled() -> None:
    """The board knows if it has room for another move."""
    # GIVEN a board in which all columns are filled
    board_instance = board.Board(
        board_state={
            board.Column.A: [
                board.Token.RED,
                board.Token.RED,
                board.Token.RED,
                board.Token.YELLOW,
                board.Token.RED,
                board.Token.YELLOW,
            ],
            board.Column.B: [
                board.Token.YELLOW,
                board.Token.YELLOW,
                board.Token.YELLOW,
                board.Token.RED,
                board.Token.RED,
                board.Token.YELLOW,
            ],
            board.Column.C: [
                board.Token.RED,
                board.Token.RED,
                board.Token.YELLOW,
                board.Token.RED,
                board.Token.YELLOW,
                board.Token.RED,
            ],
            board.Column.D: [
                board.Token.YELLOW,
                board.Token.RED,
                board.Token.YELLOW,
                board.Token.YELLOW,
                board.Token.RED,
                board.Token.RED,
            ],
            board.Column.E: [
                board.Token.RED,
                board.Token.YELLOW,
                board.Token.RED,
                board.Token.YELLOW,
                board.Token.RED,
                board.Token.YELLOW,
            ],
            board.Column.F: [
                board.Token.YELLOW,
                board.Token.YELLOW,
                board.Token.RED,
                board.Token.YELLOW,
                board.Token.YELLOW,
                board.Token.YELLOW,
            ],
            board.Column.G: [
                board.Token.YELLOW,
                board.Token.RED,
                board.Token.YELLOW,
                board.Token.RED,
                board.Token.RED,
                board.Token.RED,
            ],
        }
    )

    # WHEN the is_full property is read
    result = board_instance.is_full

    # THEN the result is true
    assert result
