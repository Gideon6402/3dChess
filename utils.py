# utils.py
"""Utility functions for the 3D chess game."""

from typing import Tuple, TYPE_CHECKING
import logging

if TYPE_CHECKING:
    from board import Board

Position = Tuple[int, int, int]
logger = logging.getLogger(__name__)


def parse_move(move_str: str) -> Position:
    """
    Parses a move string in the format 'x,y,z' and returns a position tuple.

    :param move_str: The move string.
    :return: A tuple (x, y, z).
    :raises ValueError: If the input format is invalid.
    """
    try:
        x_str, y_str, z_str = move_str.strip().split(',')
        return int(x_str), int(y_str), int(z_str)
    except ValueError:
        logger.error("Invalid input format. Please enter coordinates as x,y,z.")
        raise ValueError("Invalid input format. Please enter coordinates as x,y,z.")


def is_clear_path(board: 'Board', from_pos: Position, to_pos: Position) -> bool:
    """
    Checks if the path between two positions is clear.

    The function works for straight lines and diagonal paths in 3D space.
    It checks all the intermediate positions between from_pos and to_pos
    to ensure no other pieces are blocking the path.

    :param board: The game board.
    :param from_pos: Starting position (x, y, z).
    :param to_pos: Ending position (x, y, z).
    :return: True if the path is clear, False otherwise.
    """
    logger.debug(f"Checking path from {from_pos} to {to_pos} for obstructions.")

    try:
        fx, fy, fz = from_pos
        tx, ty, tz = to_pos
        dx = tx - fx
        dy = ty - fy
        dz = tz - fz

        steps = max(abs(dx), abs(dy), abs(dz))
        if steps == 0:
            logger.debug("From position and to position are the same.")
            return True

        x_step = dx // steps if dx != 0 else 0
        y_step = dy // steps if dy != 0 else 0
        z_step = dz // steps if dz != 0 else 0

        # Ensure the movement is along a straight line or diagonal
        if not (
            (dx == 0 or dy == 0 or dz == 0) or
            (abs(dx) == abs(dy) == abs(dz) != 0) or
            (abs(dx) == abs(dy) != 0 and dz == 0) or
            (abs(dx) == abs(dz) != 0 and dy == 0) or
            (abs(dy) == abs(dz) != 0 and dx == 0)
        ):
            logger.debug("Movement is not along a straight line or diagonal.")
            return False

        x, y, z = fx + x_step, fy + y_step, fz + z_step
        for step in range(1, steps):
            current_position = (x, y, z)
            if not board.is_within_bounds(current_position):
                logger.debug(f"Position {current_position} is out of bounds.")
                return False
            if board.get_piece(current_position):
                logger.debug(f"Path blocked by piece at {current_position}.")
                return False
            x += x_step
            y += y_step
            z += z_step

        logger.debug("Path is clear.")
        return True
    except Exception as e:
        logger.error(f"Error while checking path from {from_pos} to {to_pos}: {e}")
        return False
