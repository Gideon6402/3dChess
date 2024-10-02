# board.py
"""Module containing the Board class to manage game state."""

import numpy as np
import matplotlib.pyplot as plt
from typing import Optional, Tuple, Dict
import logging
from pieces import PieceFactory, Piece, King
from utils import is_clear_path

Position = Tuple[int, int, int]
logger = logging.getLogger(__name__)


class Board:
    """Represents the 3D chess board and manages game state."""

    def __init__(self, nx: int = 8, ny: int = 4, nz: int = 4, piece_factory: Optional[PieceFactory] = None):
        """
        Initializes the board with given dimensions and a piece factory.

        :param nx: Number of layers in the X-direction (depth).
        :param ny: Number of rows in the Y-direction.
        :param nz: Number of columns in the Z-direction.
        :param piece_factory: An instance of PieceFactory to create pieces.
        """
        self._nx = nx
        self._ny = ny
        self._nz = nz
        self._board: np.ndarray = np.full((nx, ny, nz), None, dtype=object)
        self._pieces: Dict[Position, Piece] = {}
        self._piece_factory = piece_factory or PieceFactory()
        self.initialize_board()

    def initialize_board(self) -> None:
        """Initializes the board with the starting positions of all pieces."""
        logger.info("Initializing the board.")

        # Place white pieces
        self._place_pieces('W', start_x=0)

        # Place black pieces
        self._place_pieces('B', start_x=self._nx - 1)

    def _place_pieces(self, color: str, start_x: int) -> None:
        """
        Places pieces on the board for a given color.

        :param color: 'W' for white or 'B' for black.
        :param start_x: The starting X-coordinate for the pieces.
        """
        direction = 1 if color == 'W' else -1

        # Place pawns
        pawn_row = start_x + direction
        for y in range(self._ny):
            for z in range(self._nz):
                position = (pawn_row, y, z)
                pawn = self._piece_factory.create_piece('P', color, position)
                self.set_piece(position, pawn)

        # Place rooks at the corners
        rook_positions = [
            (start_x, 0, 0),
            (start_x, 0, self._nz - 1),
            (start_x, self._ny - 1, 0),
            (start_x, self._ny - 1, self._nz - 1),
        ]
        for position in rook_positions:
            rook = self._piece_factory.create_piece('R', color, position)
            self.set_piece(position, rook)

        # Place knights next to rooks
        knight_positions = [
            (start_x, 0, 1),
            (start_x, 0, self._nz - 2),
            (start_x, self._ny - 1, 1),
            (start_x, self._ny - 1, self._nz - 2),
        ]
        for position in knight_positions:
            knight = self._piece_factory.create_piece('N', color, position)
            self.set_piece(position, knight)

        # Place bishops next to knights
        bishop_positions = [
            (start_x, 0, 2),
            (start_x, 0, self._nz - 3),
            (start_x, self._ny - 1, 2),
            (start_x, self._ny - 1, self._nz - 3),
        ]
        for position in bishop_positions:
            bishop = self._piece_factory.create_piece('B', color, position)
            self.set_piece(position, bishop)

        # Calculate central positions for queens and kings
        center_y = self._ny // 2
        center_z = self._nz // 2

        # Place queens
        queen_positions = [
            (start_x, center_y - 1, center_z - 1),
            (start_x, center_y - 1, center_z),
        ]
        for position in queen_positions:
            queen = self._piece_factory.create_piece('Q', color, position)
            self.set_piece(position, queen)

        # Place kings
        king_positions = [
            (start_x, center_y, center_z - 1),
            (start_x, center_y, center_z),
        ]
        for position in king_positions:
            king = self._piece_factory.create_piece('K', color, position)
            self.set_piece(position, king)

    def move_piece(self, from_pos: Position, to_pos: Position) -> bool:
        """Moves a piece from one position to another if the move is valid."""
        piece = self.get_piece(from_pos)
        if piece and piece.is_valid_move(to_pos, self):
            self.set_piece(to_pos, piece)
            self.set_piece(from_pos, None)
            piece.position = to_pos
            logger.info(f"Moved {piece} from {from_pos} to {to_pos}.")
            return True
        else:
            logger.warning(f"Failed to move piece from {from_pos} to {to_pos}.")
            return False


    def is_within_bounds(self, position: Position) -> bool:
        """Checks if a position is within the board boundaries."""
        x, y, z = position
        return 0 <= x < self._nx and 0 <= y < self._ny and 0 <= z < self._nz

    def get_piece(self, position: Position) -> Optional[Piece]:
        """Returns the piece at a given position, or None if empty."""
        return self._pieces.get(position)

    def set_piece(self, position: Position, piece: Optional[Piece]) -> None:
        """
        Sets a piece at a given position.

        :param position: A tuple (x, y, z).
        :param piece: An instance of Piece or None to clear the position.
        """
        if self.is_within_bounds(position):
            if piece:
                self._pieces[position] = piece
                self._board[position] = piece
                logger.debug(f"Placed {piece} at {position}.")
            else:
                self._pieces.pop(position, None)
                self._board[position] = None
                logger.debug(f"Cleared position {position}.")
        else:
            logger.warning(f"Attempted to set piece at out-of-bounds position {position}.")

    def visualize(self) -> None:
            """Visualizes the board using Matplotlib."""
            logger.info("Visualizing the board.")

            try:
                with plt.style.context('default'):
                    fig = plt.figure(figsize=(10, 7))
                    ax = fig.add_subplot(111, projection='3d')

                    # Set up the grid lines
                    ax.set_xticks(range(self._nx))
                    ax.set_yticks(range(self._ny))
                    ax.set_zticks(range(self._nz))
                    ax.set_xlim(-0.5, self._nx - 0.5)
                    ax.set_ylim(-0.5, self._ny - 0.5)
                    ax.set_zlim(-0.5, self._nz - 0.5)
                    ax.set_xlabel('X-axis (Layers)')
                    ax.set_ylabel('Y-axis (Rows)')
                    ax.set_zlabel('Z-axis (Columns)')
                    ax.set_title('3D Chess Board')

                    # Draw grid lines
                    for x in range(self._nx):
                        ax.plot([x, x], [0, self._ny - 1], [0, 0], color='gray', alpha=0.2)
                        ax.plot([x, x], [0, 0], [0, self._nz - 1], color='gray', alpha=0.2)
                    for y in range(self._ny):
                        ax.plot([0, self._nx - 1], [y, y], [0, 0], color='gray', alpha=0.2)
                        ax.plot([0, 0], [y, y], [0, self._nz - 1], color='gray', alpha=0.2)
                    for z in range(self._nz):
                        ax.plot([0, self._nx - 1], [0, 0], [z, z], color='gray', alpha=0.2)
                        ax.plot([0, 0], [0, self._ny - 1], [z, z], color='gray', alpha=0.2)

                    # Map piece types to markers and colors
                    marker_map = {
                        'P': 'o',  # Pawn
                        'R': 's',  # Rook
                        'N': '^',  # Knight
                        'B': 'D',  # Bishop
                        'Q': '*',  # Queen
                        'K': 'X',  # King
                    }
                    color_map = {
                        'W': 'white',
                        'B': 'black',
                    }
                    edge_color_map = {
                        'W': 'black',
                        'B': 'white',
                    }

                    # Plot each piece
                    for position, piece in self._pieces.items():
                        x, y, z = position
                        marker = marker_map.get(piece.__class__.__name__[0], 'o')
                        facecolor = color_map.get(piece.color, 'gray')
                        edgecolor = edge_color_map.get(piece.color, 'black')
                        ax.scatter(
                            x,
                            y,
                            z,
                            marker=marker,
                            s=200,  # Size of the marker
                            c=facecolor,
                            edgecolors=edgecolor,
                            linewidths=1.5,
                            alpha=0.9,
                        )
                        # Annotate the piece
                        ax.text(
                            x,
                            y,
                            z,
                            f"{piece.__class__.__name__[0]}",
                            color='red' if piece.color == 'W' else 'yellow',
                            fontsize=9,
                            ha='center',
                            va='center',
                        )

                    plt.tight_layout()
                    plt.show()
            except Exception as e:
                logger.error(f"Error during visualization: {e}")

    def is_game_over(self, opponent_color: str) -> bool:
        """
        Determines if the game is over.

        The game is considered over if the opponent has no kings left.

        :param opponent_color: The color of the opponent ('W' or 'B').
        :return: True if the game is over, False otherwise.
        """
        logger.info(f"Checking if the game is over for opponent color: {opponent_color}")

        try:
            # Get all pieces of the opponent's color
            opponent_pieces: List[Piece] = [
                piece for piece in self._pieces.values() if piece.color == opponent_color
            ]

            # Check if the opponent has any kings left
            opponent_kings = [piece for piece in opponent_pieces if isinstance(piece, King)]

            if not opponent_kings:
                logger.info(f"No kings left for opponent {opponent_color}. Game over.")
                return True
            else:
                logger.debug(f"Opponent {opponent_color} has {len(opponent_kings)} king(s) remaining.")
                return False
        except Exception as e:
            logger.error(f"Error while checking if game is over: {e}")
            return False
