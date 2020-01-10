from nim import State, Move, apply, Player, parse_move, display_board
from hypothesis.strategies import text
from hypothesis import given
import pytest
from dataclasses import replace


def test_apply():
    board = [5, 1, 9]
    state = State(board, Player.P1)
    index = 0
    number = 5
    move = Move(index, number)
    new_state = apply(state, move)
    assert new_state != state
    assert new_state.board == [0, 1, 9]
    assert new_state.next_player is Player.P2
    assert new_state.message == ""


def test_apply2():
    board = [5, 1, 9]
    state = State(board, Player.P2, "DANGER")
    index = 0
    number = 3
    move = Move(index, number)
    new_state = apply(state, move)
    assert new_state != state
    assert new_state.board == [2, 1, 9]
    assert new_state.next_player is Player.P1
    assert new_state.message == ""


def test_apply_invalid_move_amount():
    board = [5, 1, 9]
    state = State(board, Player.P2)
    index = 0
    number = 6
    move = Move(index, number)
    new_state = apply(state, move)
    assert new_state == replace(state, message="Invalid amount")


def test_apply_invalid_move_index():
    board = [5, 1, 9]
    state = State(board, Player.P2)
    index = 4
    number = 5
    move = Move(index, number)
    new_state = apply(state, move)
    assert new_state == replace(state, message="Invalid index")


@pytest.mark.parametrize(
    "input_str,expected_output",
    [
        ("A 1", Move(0, 1)),
        ("A 2", Move(0, 2)),
        ("B 1", Move(1, 1)),
        ("b 3", Move(1, 3)),
        ("", None),
        ("0", None),
        ("000", None),
        ("A A", None),
        ("   ", None),
        ("A 0", None),
    ],
)
def test_parse_move(input_str, expected_output):
    assert parse_move(input_str) == expected_output


@given(text())
def test_parse_random_input(s):
    assert parse_move(s) is None


def test_display_board_one_empty():
    board = [0]
    assert display_board(board) == 'A: 🕳'

def test_display_board_multiple_empties():
    board = [0,0,0]
    assert display_board(board) == """\
A: 🕳
B: 🕳
C: 🕳"""


def test_display_board_one():
    board = [1]
    assert display_board(board) == 'A: 🍌'

def test_display_board_multiple():
    board = [0,3,2,1]
    assert display_board(board) == """\
A: 🕳
B: 🍌🍌🍌
C: 🍌🍌
D: 🍌"""
