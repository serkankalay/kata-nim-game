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

class PlayingMode(enum.Enum):
    TwoPlayers = enum.auto()
    AgainstComputer = enum.auto()

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
    return [randint(1, 9) for _ in range(number_of_heaps)]


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
    return "\n".join(display_heaps(board))


def display_heaps(board: Sequence[int]) -> str:
    for i, num_items in enumerate(board):
        if num_items == 0:
            yield (f'{ascii_uppercase[i]}(0) : 🕳')
        else:
            yield (f'{ascii_uppercase[i]}({num_items}){" " if num_items < 10 else ""}: {"🔥" * num_items}')


def generate_move(board: Sequence[int]) -> Move:
    while True:
        return None
        # heap = randint(1, len(board))
        # if board[heap]:
        #      return

def run():
    print(
        """
Welcome to Nim Game!
Don't forget: who picks the last piece, WINS!
Description:
    NIM is a two-player turn-based game.
    There are certain number of heaps (you'll be decidin on this as well!), each containing a certain number of items.
    At each turn, the active player needs to decide:
        Which heap to take from, and
        How many items to take - note that at least 1 and at most the available number of items.
    

The active player is asked to provide the decision in a way I can understand.
It should be in the form of: `HeapName NumberOfItemsToTake`

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
