from typing import Sequence, Optional
from string import ascii_uppercase
from dataclasses import replace
from random import randint
import enum
from dataclasses import dataclass


MAX_NUMBER_OF_HEAPS = 10


class Player(enum.Enum):
    P1 = enum.auto()
    P2 = enum.auto()


@dataclass(frozen=True)
class State:
    board: Sequence[int]
    next_player: Player
    message: str = ""


@dataclass(frozen=True)
class Move:
    index: int
    number: int


def apply(state: State, move: Move) -> State:
    if move.index >= len(state.board):
        return replace(state, message="Invalid index")
    if move.number > state.board[move.index]:
        return replace(state, message="Invalid amount")
    new_state = State(state.board.copy(), other_player(state.next_player))
    new_state.board[move.index] = new_state.board[move.index] - move.number
    return new_state


def other_player(player: Player) -> Player:
    return Player.P1 if player is Player.P2 else Player.P2


def generate_board(number_of_heaps: int) -> Sequence[int]:
    return [randint(1, 10) for _ in range(number_of_heaps)]


def parse_move(user_input: str) -> Optional[Move]:
    if len(user_input) != 3:
        return None
    if user_input[2] == '0':
        return None
    inputs = user_input.split(" ")
    try:
        return Move(ascii_uppercase.index(inputs[0].upper()), int(inputs[1]))
    except ValueError:
        return None


def display_board(board: Sequence[int]) -> str:
    str_list = []
    if len(board) == 1 and board[0] == 1:
        return 'A: 🍌'
    for i in range(len(board)):
        if board[i] == 0:
            str_list.append(f'{ascii_uppercase[i]}: 🕳')
        else:
            str_list.append(f'{ascii_uppercase[i]}: {"🍌" * board[i]}')
    return "\n".join(str_list)


def run():
    print(
        """
Welcome to Nim Game!
Don't forget: who picks the last piece, wins!

At each turn, player is asked to provide an input that I can understand.
It should be in the form of: `HeapName NumberOfItemsToRemove`

Examples: `A 3`, `B 1`


"""
    )
    number_of_heaps = int(
        input(
            f"How many heaps would you like? (at most {MAX_NUMBER_OF_HEAPS}): "
        )
    )
    if number_of_heaps > MAX_NUMBER_OF_HEAPS or number_of_heaps <= 0:
        print("...")
        return
    state = State(generate_board(number_of_heaps), Player.P1)
    while any(state.board):
        print(display_board(state.board))
        user_input = input(f"{state.next_player} please type your next move:")
        user_move = parse_move(user_input)
        if user_move is None:
            print("Invalid input. Please try again")
            continue
        state = apply(state, user_move)
    print(f"\n{other_player(state.next_player)} has won!\n🎉🎉🎉🎉🎉Congratulations!🎉🎉🎉🎉🎉")


if __name__ == "__main__":
    run()
