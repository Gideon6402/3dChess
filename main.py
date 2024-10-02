# game.py
"""Main module to run the 3D chess game."""

import logging
from board import Board
from utils import parse_move

logger = logging.getLogger(__name__)
logging.basicConfig(level=logging.INFO, format='%(levelname)s:%(message)s')


def make_move(board: Board, player_color: str) -> None:
    """
    Prompts the player to make a move.

    :param board: The game board.
    :param player_color: The color of the current player ('W' or 'B').
    """
    while True:
        try:
            print(f"Player {player_color}'s turn.")
            from_str = input("Enter the position of the piece you want to move (x,y,z): ")
            to_str = input("Enter the position where you want to move the piece (x,y,z): ")

            from_pos = parse_move(from_str)
            to_pos = parse_move(to_str)

            piece = board.get_piece(from_pos)
            if piece and piece.color == player_color:
                if piece.is_valid_move(to_pos, board):
                    if board.move_piece(from_pos, to_pos):
                        print(f"Moved from {from_pos} to {to_pos}")
                        logger.info(f"Player {player_color} moved from {from_pos} to {to_pos}.")
                        break
                    else:
                        print("Move failed.")
                        logger.warning(f"Player {player_color}'s move from {from_pos} to {to_pos} failed.")
                else:
                    print("Invalid move.")
                    logger.warning(f"Invalid move by {player_color} from {from_pos} to {to_pos}.")
            else:
                print("No valid piece at the source position.")
                logger.warning(f"No valid piece at {from_pos} for player {player_color}.")
        except ValueError as e:
            print(e)
            continue


def play_game() -> None:
    """Starts and runs the 3D chess game."""
    board = Board()
    turn = 0
    players = ['W', 'B']

    while True:
        board.visualize()
        current_player = players[turn % 2]
        opponent = players[(turn + 1) % 2]
        make_move(board, current_player)
        if board.is_game_over(opponent):
            print(f"Player {current_player} wins!")
            logger.info(f"Player {current_player} wins the game.")
            board.visualize()
            break
        turn += 1


if __name__ == "__main__":
    play_game()
