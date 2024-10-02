# pieces.py
"""Module containing the Piece classes for the 3D chess game."""

import logging
from abc import ABC, abstractmethod
from typing import Tuple, TYPE_CHECKING

from utils import is_clear_path

if TYPE_CHECKING:
    from board import Board

Position = Tuple[int, int, int]
logger = logging.getLogger(__name__)


class Piece(ABC):
    """Abstract base class for all chess pieces."""

    def __init__(self, color: str, position: Position):
        """
        Initializes a chess piece.

        :param color: 'W' for white or 'B' for black.
        :param position: A tuple representing the piece's position (x, y, z).
        """
        self.color = color
        self.position = position

    def is_valid_move(self, to_position: Position, board: 'Board') -> bool:
        """
        Checks if a move is valid by performing general checks and calling the piece-specific method.

        :param to_position: The destination position.
        :param board: The game board.
        :return: True if the move is valid, False otherwise.
        """
        if not board.is_within_bounds(to_position):
            logger.debug(f"Destination {to_position} is out of bounds.")
            return False

        if self.position == to_position:
            logger.debug("Destination is the same as the current position.")
            return False

        try:
            return self._is_valid_move(to_position, board)
        except Exception as e:
            logger.error(f"Error in move validation for {self.__class__.__name__}: {e}")
            return False

    @abstractmethod
    def _is_valid_move(self, to_position: Position, board: 'Board') -> bool:
        """
        Abstract method to be implemented by each piece type for move validation.

        :param to_position: The destination position.
        :param board: The game board.
        :return: True if the move is valid according to the piece's movement rules, False otherwise.
        """
        pass

    def __repr__(self):
        return f"{self.__class__.__name__}({self.color}, {self.position})"


class Pawn(Piece):
    """Class representing a Pawn."""

    def _is_valid_move(self, to_position: Position, board: 'Board') -> bool:
        """Checks if the pawn's move is valid."""
        fx, fy, fz = self.position
        tx, ty, tz = to_position

        direction = 1 if self.color == 'W' else -1
        dx = tx - fx
        dy = ty - fy
        dz = tz - fz

        # Forward move
        if dx == direction and dy == 0 and dz == 0 and not board.get_piece(to_position):
            return True
        # Diagonal capture
        elif dx == direction and abs(dy) == 1 and dz == 0:
            target_piece = board.get_piece(to_position)
            if target_piece and target_piece.color != self.color:
                return True
            else:
                logger.debug(f"Pawn cannot capture own piece or empty square at {to_position}")
                return False
        else:
            logger.debug(f"Invalid pawn move from {self.position} to {to_position}")
            return False


class Rook(Piece):
    """Class representing a Rook."""

    def _is_valid_move(self, to_position: Position, board: 'Board') -> bool:
        """Checks if the rook's move is valid."""
        fx, fy, fz = self.position
        tx, ty, tz = to_position

        # Rook moves along one axis
        if ((fx == tx) and (fy == ty) and (fz != tz)) or \
           ((fx == tx) and (fy != ty) and (fz == tz)) or \
           ((fx != tx) and (fy == ty) and (fz == tz)):
            if is_clear_path(board, self.position, to_position):
                target_piece = board.get_piece(to_position)
                if not target_piece or target_piece.color != self.color:
                    return True
                else:
                    logger.debug(f"Rook cannot capture own piece at {to_position}")
                    return False
            else:
                logger.debug(f"Path is not clear for rook from {self.position} to {to_position}")
                return False
        else:
            logger.debug(f"Invalid rook move from {self.position} to {to_position}")
            return False


class Knight(Piece):
    """Class representing a Knight."""

    def _is_valid_move(self, to_position: Position, board: 'Board') -> bool:
        """Checks if the knight's move is valid."""
        fx, fy, fz = self.position
        tx, ty, tz = to_position
        dx = abs(tx - fx)
        dy = abs(ty - fy)
        dz = abs(tz - fz)

        # The sum of the squares of the movement along each axis equals 5
        if dx**2 + dy**2 + dz**2 == 5:
            target_piece = board.get_piece(to_position)
            if not target_piece or target_piece.color != self.color:
                return True
            else:
                logger.debug(f"Knight cannot capture own piece at {to_position}")
                return False
        else:
            logger.debug(f"Invalid knight move from {self.position} to {to_position}")
            return False


class Bishop(Piece):
    """Class representing a Bishop."""

    def _is_valid_move(self, to_position: Position, board: 'Board') -> bool:
        """Checks if the bishop's move is valid."""
        fx, fy, fz = self.position
        tx, ty, tz = to_position
        dx = tx - fx
        dy = ty - fy
        dz = tz - fz

        # Bishop moves along diagonals
        if (abs(dx) == abs(dy) == abs(dz) != 0) or \
           (abs(dx) == abs(dy) != 0 and dz == 0) or \
           (abs(dx) == abs(dz) != 0 and dy == 0) or \
           (abs(dy) == abs(dz) != 0 and dx == 0):
            if is_clear_path(board, self.position, to_position):
                target_piece = board.get_piece(to_position)
                if not target_piece or target_piece.color != self.color:
                    return True
                else:
                    logger.debug(f"Bishop cannot capture own piece at {to_position}")
                    return False
            else:
                logger.debug(f"Path is not clear for bishop from {self.position} to {to_position}")
                return False
        else:
            logger.debug(f"Invalid bishop move from {self.position} to {to_position}")
            return False


class Queen(Piece):
    """Class representing a Queen."""

    def _is_valid_move(self, to_position: Position, board: 'Board') -> bool:
        """Checks if the queen's move is valid."""
        fx, fy, fz = self.position
        tx, ty, tz = to_position
        dx = tx - fx
        dy = ty - fy
        dz = tz - fz

        # Queen moves like Rook or Bishop
        if ((fx == tx) or (fy == ty) or (fz == tz)) or \
           (abs(dx) == abs(dy) == abs(dz) != 0) or \
           (abs(dx) == abs(dy) != 0 and dz == 0) or \
           (abs(dx) == abs(dz) != 0 and dy == 0) or \
           (abs(dy) == abs(dz) != 0 and dx == 0):
            if is_clear_path(board, self.position, to_position):
                target_piece = board.get_piece(to_position)
                if not target_piece or target_piece.color != self.color:
                    return True
                else:
                    logger.debug(f"Queen cannot capture own piece at {to_position}")
                    return False
            else:
                logger.debug(f"Path is not clear for queen from {self.position} to {to_position}")
                return False
        else:
            logger.debug(f"Invalid queen move from {self.position} to {to_position}")
            return False


class King(Piece):
    """Class representing a King."""

    def _is_valid_move(self, to_position: Position, board: 'Board') -> bool:
        """Checks if the king's move is valid."""
        fx, fy, fz = self.position
        tx, ty, tz = to_position
        dx = abs(tx - fx)
        dy = abs(ty - fy)
        dz = abs(tz - fz)

        # King moves one square in any direction
        if max(dx, dy, dz) == 1:
            target_piece = board.get_piece(to_position)
            if not target_piece or target_piece.color != self.color:
                # Note: Additional checks for check situations can be added here
                return True
            else:
                logger.debug(f"King cannot capture own piece at {to_position}")
                return False
        else:
            logger.debug(f"Invalid king move from {self.position} to {to_position}")
            return False


class PieceFactory:
    """Factory class to create chess pieces."""

    def create_piece(self, piece_type: str, color: str, position: Position) -> Piece:
        """
        Creates a chess piece of the given type, color, and position.

        :param piece_type: One of 'P', 'R', 'N', 'B', 'Q', 'K'.
        :param color: 'W' for white or 'B' for black.
        :param position: A tuple representing the piece's position (x, y, z).
        :return: An instance of a Piece subclass.
        :raises ValueError: If the piece type is invalid.
        """
        piece_classes = {
            'P': Pawn,
            'R': Rook,
            'N': Knight,
            'B': Bishop,
            'Q': Queen,
            'K': King,
        }
        piece_class = piece_classes.get(piece_type)
        if piece_class:
            piece = piece_class(color, position)
            logger.debug(f"Created {piece} at {position}")
            return piece
        else:
            logger.error(f"Unknown piece type: {piece_type}")
            raise ValueError(f"Unknown piece type: {piece_type}")
