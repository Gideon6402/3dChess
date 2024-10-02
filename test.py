# test.py
"""Test suite for the 3D chess game."""

import unittest
import logging
from board import Board
from pieces import PieceFactory, Pawn, Rook, Knight, Bishop, Queen, King
from utils import is_clear_path
from typing import Tuple

Position = Tuple[int, int, int]
logger = logging.getLogger(__name__)


class TestChess3D(unittest.TestCase):
    """Test cases for the 3D chess game."""

    def setUp(self):
        """Sets up the test environment before each test."""
        self.board = Board()
        self.board._board.fill(None)
        self.board._pieces.clear()
        self.piece_factory = PieceFactory()

    # ---------------------------
    # Tests for Pawn Movement
    # ---------------------------
    def test_pawn_move_forward(self):
        """Tests that the pawn can move forward one square."""
        pawn = self.piece_factory.create_piece('P', 'W', (1, 1, 1))
        self.board.set_piece((1, 1, 1), pawn)

        # Valid forward move
        self.assertTrue(pawn.is_valid_move((2, 1, 1), self.board))

        # Move the pawn
        self.board.move_piece((1, 1, 1), (2, 1, 1))
        self.assertEqual(pawn.position, (2, 1, 1))

    def test_pawn_invalid_move(self):
        """Tests that the pawn cannot move backward or sideways."""
        pawn = self.piece_factory.create_piece('P', 'W', (1, 1, 1))
        self.board.set_piece((1, 1, 1), pawn)

        # Invalid backward move
        self.assertFalse(pawn.is_valid_move((0, 1, 1), self.board))

        # Invalid sideways move
        self.assertFalse(pawn.is_valid_move((1, 2, 1), self.board))

    def test_pawn_capture(self):
        """Tests that the pawn can capture an opponent's piece diagonally."""
        pawn = self.piece_factory.create_piece('P', 'W', (1, 1, 1))
        self.board.set_piece((1, 1, 1), pawn)
        enemy_piece = self.piece_factory.create_piece('P', 'B', (2, 2, 1))
        self.board.set_piece((2, 2, 1), enemy_piece)

        # Valid capture
        self.assertTrue(pawn.is_valid_move((2, 2, 1), self.board))

        # Move the pawn and capture
        self.board.move_piece((1, 1, 1), (2, 2, 1))
        self.assertEqual(pawn.position, (2, 2, 1))
        self.assertIsNone(self.board.get_piece((1, 1, 1)))
        self.assertIs(self.board.get_piece((2, 2, 1)), pawn)

    def test_pawn_blocked_forward(self):
        """Tests that the pawn cannot move forward if blocked."""
        pawn = self.piece_factory.create_piece('P', 'W', (1, 1, 1))
        self.board.set_piece((1, 1, 1), pawn)
        blocking_piece = self.piece_factory.create_piece('P', 'B', (2, 1, 1))
        self.board.set_piece((2, 1, 1), blocking_piece)

        # Cannot move forward because blocked
        self.assertFalse(pawn.is_valid_move((2, 1, 1), self.board))

    def test_pawn_capture_forward_invalid(self):
        """Tests that the pawn cannot capture forward."""
        pawn = self.piece_factory.create_piece('P', 'W', (1, 1, 1))
        self.board.set_piece((1, 1, 1), pawn)
        enemy_piece = self.piece_factory.create_piece('P', 'B', (2, 1, 1))
        self.board.set_piece((2, 1, 1), enemy_piece)

        # Cannot capture forward
        self.assertFalse(pawn.is_valid_move((2, 1, 1), self.board))

    # ---------------------------
    # Tests for Rook Movement
    # ---------------------------
    def test_rook_valid_moves(self):
        """Tests valid rook moves along axes."""
        rook = self.piece_factory.create_piece('R', 'W', (0, 0, 0))
        self.board.set_piece((0, 0, 0), rook)

        # Valid moves along X, Y, and Z axes
        self.assertTrue(rook.is_valid_move((5, 0, 0), self.board))  # Along X
        self.assertTrue(rook.is_valid_move((0, 3, 0), self.board))  # Along Y
        self.assertTrue(rook.is_valid_move((0, 0, 3), self.board))  # Along Z

    def test_rook_invalid_moves(self):
        """Tests invalid rook moves."""
        rook = self.piece_factory.create_piece('R', 'W', (0, 0, 0))
        self.board.set_piece((0, 0, 0), rook)

        # Invalid diagonal move
        self.assertFalse(rook.is_valid_move((1, 1, 0), self.board))

    def test_rook_blocked_path(self):
        """Tests that the rook cannot move through other pieces."""
        rook = self.piece_factory.create_piece('R', 'W', (0, 0, 0))
        self.board.set_piece((0, 0, 0), rook)
        blocking_piece = self.piece_factory.create_piece('P', 'B', (0, 0, 1))
        self.board.set_piece((0, 0, 1), blocking_piece)

        # Path is blocked along Z-axis
        self.assertFalse(rook.is_valid_move((0, 0, 3), self.board))

    def test_rook_capture(self):
        """Tests that the rook can capture opponent's piece."""
        rook = self.piece_factory.create_piece('R', 'W', (0, 0, 0))
        self.board.set_piece((0, 0, 0), rook)
        enemy_piece = self.piece_factory.create_piece('P', 'B', (0, 0, 3))
        self.board.set_piece((0, 0, 3), enemy_piece)

        # Valid capture
        self.assertTrue(rook.is_valid_move((0, 0, 3), self.board))

    # ---------------------------
    # Tests for Knight Movement
    # ---------------------------
    def test_knight_valid_moves(self):
        """Tests valid knight moves."""
        knight = self.piece_factory.create_piece('N', 'W', (1, 1, 1))
        self.board.set_piece((1, 1, 1), knight)

        # Valid L-shaped moves (sum of squares equals 5)
        valid_moves = [
            (2, 3, 1),
            (2, 1, 3),
            (3, 2, 1),
            (0, 3, 1),
            (0, 1, 3),
            (3, 0, 1),
            (1, 0, 3),
            (1, 3, 0),
            (3, 1, 0),
            (0, 2, 1),
            (1, 0, 0),
            (0, 1, 0),
        ]
        for move in valid_moves:
            self.assertTrue(knight.is_valid_move(move, self.board))

    def test_knight_invalid_moves(self):
        """Tests invalid knight moves."""
        knight = self.piece_factory.create_piece('N', 'W', (1, 1, 1))
        self.board.set_piece((1, 1, 1), knight)

        # Invalid move (not L-shaped)
        self.assertFalse(knight.is_valid_move((2, 2, 2), self.board))

    def test_knight_jumping(self):
        """Tests that the knight can jump over other pieces."""
        knight = self.piece_factory.create_piece('N', 'W', (1, 1, 1))
        self.board.set_piece((1, 1, 1), knight)
        blocking_piece = self.piece_factory.create_piece('P', 'B', (2, 1, 1))
        self.board.set_piece((2, 1, 1), blocking_piece)

        # Knight can still move to (3, 2, 1) by jumping over the blocking piece
        self.assertTrue(knight.is_valid_move((3, 2, 1), self.board))

    # ---------------------------
    # Tests for Bishop Movement
    # ---------------------------
    def test_bishop_valid_moves(self):
        """Tests valid bishop moves along diagonals."""
        bishop = self.piece_factory.create_piece('B', 'W', (0, 0, 0))
        self.board.set_piece((0, 0, 0), bishop)

        # Valid diagonal moves
        self.assertTrue(bishop.is_valid_move((3, 3, 3), self.board))  # Along main diagonal
        self.assertTrue(bishop.is_valid_move((3, 3, 0), self.board))  # Diagonal in XY plane
        self.assertTrue(bishop.is_valid_move((3, 0, 3), self.board))  # Diagonal in XZ plane
        self.assertTrue(bishop.is_valid_move((0, 3, 3), self.board))  # Diagonal in YZ plane

    def test_bishop_invalid_moves(self):
        """Tests invalid bishop moves."""
        bishop = self.piece_factory.create_piece('B', 'W', (0, 0, 0))
        self.board.set_piece((0, 0, 0), bishop)

        # Invalid straight move
        self.assertFalse(bishop.is_valid_move((3, 0, 0), self.board))

    def test_bishop_blocked_path(self):
        """Tests that the bishop cannot move through other pieces."""
        bishop = self.piece_factory.create_piece('B', 'W', (0, 0, 0))
        self.board.set_piece((0, 0, 0), bishop)
        blocking_piece = self.piece_factory.create_piece('P', 'B', (1, 1, 1))
        self.board.set_piece((1, 1, 1), blocking_piece)

        # Path is blocked along main diagonal
        self.assertFalse(bishop.is_valid_move((3, 3, 3), self.board))

    def test_bishop_capture(self):
        """Tests that the bishop can capture opponent's piece."""
        bishop = self.piece_factory.create_piece('B', 'W', (0, 0, 0))
        self.board.set_piece((0, 0, 0), bishop)
        enemy_piece = self.piece_factory.create_piece('P', 'B', (3, 3, 3))
        self.board.set_piece((3, 3, 3), enemy_piece)

        # Valid capture
        self.assertTrue(bishop.is_valid_move((3, 3, 3), self.board))

    # ---------------------------
    # Tests for Queen Movement
    # ---------------------------
    def test_queen_valid_moves(self):
        """Tests valid queen moves (combination of rook and bishop)."""
        queen = self.piece_factory.create_piece('Q', 'W', (0, 0, 0))
        self.board.set_piece((0, 0, 0), queen)

        # Valid rook-like moves
        self.assertTrue(queen.is_valid_move((5, 0, 0), self.board))
        self.assertTrue(queen.is_valid_move((0, 3, 0), self.board))
        self.assertTrue(queen.is_valid_move((0, 0, 3), self.board))

        # Valid bishop-like moves
        self.assertTrue(queen.is_valid_move((3, 3, 3), self.board))
        self.assertTrue(queen.is_valid_move((3, 3, 0), self.board))
        self.assertTrue(queen.is_valid_move((3, 0, 3), self.board))
        self.assertTrue(queen.is_valid_move((0, 3, 3), self.board))

    def test_queen_invalid_moves(self):
        """Tests invalid queen moves."""
        queen = self.piece_factory.create_piece('Q', 'W', (0, 0, 0))
        self.board.set_piece((0, 0, 0), queen)

        # Invalid knight-like move
        self.assertFalse(queen.is_valid_move((2, 1, 0), self.board))

    def test_queen_blocked_path(self):
        """Tests that the queen cannot move through other pieces."""
        queen = self.piece_factory.create_piece('Q', 'W', (0, 0, 0))
        self.board.set_piece((0, 0, 0), queen)
        blocking_piece = self.piece_factory.create_piece('P', 'B', (1, 0, 0))
        self.board.set_piece((1, 0, 0), blocking_piece)

        # Path is blocked along X-axis
        self.assertFalse(queen.is_valid_move((3, 0, 0), self.board))

    def test_queen_capture(self):
        """Tests that the queen can capture opponent's piece."""
        queen = self.piece_factory.create_piece('Q', 'W', (0, 0, 0))
        self.board.set_piece((0, 0, 0), queen)
        enemy_piece = self.piece_factory.create_piece('P', 'B', (3, 0, 0))
        self.board.set_piece((3, 0, 0), enemy_piece)

        # Valid capture
        self.assertTrue(queen.is_valid_move((3, 0, 0), self.board))

    # ---------------------------
    # Tests for King Movement
    # ---------------------------
    def test_king_valid_moves(self):
        """Tests valid king moves (one square in any direction)."""
        king = self.piece_factory.create_piece('K', 'W', (1, 1, 1))
        self.board.set_piece((1, 1, 1), king)

        # Valid moves to adjacent squares
        valid_moves = [
            (0, 1, 1),
            (2, 1, 1),
            (1, 0, 1),
            (1, 2, 1),
            (1, 1, 0),
            (1, 1, 2),
            (0, 0, 1),
            (0, 2, 1),
            (2, 0, 1),
            (2, 2, 1),
            (1, 0, 0),
            (1, 0, 2),
            (1, 2, 0),
            (1, 2, 2),
            (0, 1, 0),
            (0, 1, 2),
            (2, 1, 0),
            (2, 1, 2),
            (0, 0, 0),
            (0, 0, 2),
            (0, 2, 0),
            (0, 2, 2),
            (2, 0, 0),
            (2, 0, 2),
            (2, 2, 0),
            (2, 2, 2),
        ]
        for move in valid_moves:
            self.assertTrue(king.is_valid_move(move, self.board))

    def test_king_invalid_moves(self):
        """Tests invalid king moves."""
        king = self.piece_factory.create_piece('K', 'W', (1, 1, 1))
        self.board.set_piece((1, 1, 1), king)

        # Invalid move (more than one square away)
        self.assertFalse(king.is_valid_move((3, 1, 1), self.board))

    def test_king_capture(self):
        """Tests that the king can capture opponent's piece."""
        king = self.piece_factory.create_piece('K', 'W', (1, 1, 1))
        self.board.set_piece((1, 1, 1), king)
        enemy_piece = self.piece_factory.create_piece('P', 'B', (2, 1, 1))
        self.board.set_piece((2, 1, 1), enemy_piece)

        # Valid capture
        self.assertTrue(king.is_valid_move((2, 1, 1), self.board))

    # ---------------------------
    # Tests for is_clear_path Function
    # ---------------------------
    def test_is_clear_path(self):
        """Tests the is_clear_path function."""
        # Set up the board with a clear path
        self.board._pieces.clear()  # Clear the board
        self.board.set_piece((0, 0, 0), self.piece_factory.create_piece('R', 'W', (0, 0, 0)))
        self.assertTrue(is_clear_path(self.board, (0, 0, 0), (0, 3, 0)))

        # Place a blocking piece
        self.board.set_piece((0, 1, 0), self.piece_factory.create_piece('P', 'W', (0, 1, 0)))
        self.assertFalse(is_clear_path(self.board, (0, 0, 0), (0, 3, 0)))

    def test_is_clear_path_diagonal(self):
        """Tests is_clear_path on a diagonal path."""
        # Set up the board with a clear diagonal path
        self.board._pieces.clear()
        self.board.set_piece((0, 0, 0), self.piece_factory.create_piece('B', 'W', (0, 0, 0)))
        self.assertTrue(is_clear_path(self.board, (0, 0, 0), (3, 3, 3)))

        # Place a blocking piece
        self.board.set_piece((1, 1, 1), self.piece_factory.create_piece('P', 'W', (1, 1, 1)))
        self.assertFalse(is_clear_path(self.board, (0, 0, 0), (3, 3, 3)))

    def test_is_clear_path_invalid_movement(self):
        """Tests is_clear_path with invalid movement pattern."""
        self.board._pieces.clear()
        self.assertFalse(is_clear_path(self.board, (0, 0, 0), (2, 1, 0)))  # Not a straight line or diagonal

    # ---------------------------
    # Tests for is_game_over Method
    # ---------------------------
    def test_is_game_over(self):
        """Tests the is_game_over method."""
        # Set up a scenario where the opponent has no kings left
        self.board._pieces.clear()  # Clear the board
        # Place a single king for player 'W'
        king_position = (0, 0, 0)
        king = self.piece_factory.create_piece('K', 'W', king_position)
        self.board.set_piece(king_position, king)

        # Check if the game is over for opponent 'B'
        self.assertTrue(self.board.is_game_over('B'))

        # Add a king for 'B' and check again
        opponent_king_position = (7, 3, 3)
        opponent_king = self.piece_factory.create_piece('K', 'B', opponent_king_position)
        self.board.set_piece(opponent_king_position, opponent_king)

        self.assertFalse(self.board.is_game_over('B'))

    def test_is_game_over_multiple_kings(self):
        """Tests is_game_over with multiple kings."""
        self.board._pieces.clear()
        # Place two kings for 'B'
        king1 = self.piece_factory.create_piece('K', 'B', (7, 3, 3))
        king2 = self.piece_factory.create_piece('K', 'B', (7, 2, 2))
        self.board.set_piece((7, 3, 3), king1)
        self.board.set_piece((7, 2, 2), king2)

        # Remove one king and test
        self.board.set_piece((7, 3, 3), None)
        self.assertFalse(self.board.is_game_over('B'))

        # Remove second king and test
        self.board.set_piece((7, 2, 2), None)
        self.assertTrue(self.board.is_game_over('B'))

    # ---------------------------
    # Additional Tests
    # ---------------------------
    def test_move_piece(self):
        """Tests moving a piece on the board."""
        rook = self.piece_factory.create_piece('R', 'W', (0, 0, 0))
        self.board.set_piece((0, 0, 0), rook)

        # Move rook to an empty square
        self.assertTrue(self.board.move_piece((0, 0, 0), (0, 3, 0)))
        self.assertEqual(rook.position, (0, 3, 0))
        self.assertIsNone(self.board.get_piece((0, 0, 0)))
        self.assertIs(self.board.get_piece((0, 3, 0)), rook)

    def test_move_piece_invalid(self):
        """Tests moving a piece with an invalid move."""
        rook = self.piece_factory.create_piece('R', 'W', (0, 0, 0))
        self.board.set_piece((0, 0, 0), rook)

        # Attempt to move rook in an invalid way
        self.assertFalse(self.board.move_piece((0, 0, 0), (1, 1, 1)))
        self.assertEqual(rook.position, (0, 0, 0))
        self.assertIs(self.board.get_piece((0, 0, 0)), rook)

    def test_capture_own_piece(self):
        """Tests that a piece cannot capture a piece of the same color."""
        rook = self.piece_factory.create_piece('R', 'W', (0, 0, 0))
        pawn = self.piece_factory.create_piece('P', 'W', (0, 3, 0))
        self.board.set_piece((0, 0, 0), rook)
        self.board.set_piece((0, 3, 0), pawn)

        # Attempt to capture own piece
        self.assertFalse(rook.is_valid_move((0, 3, 0), self.board))

    def test_out_of_bounds_move(self):
        """Tests moving a piece out of the board bounds."""
        rook = self.piece_factory.create_piece('R', 'W', (0, 0, 0))
        self.board.set_piece((0, 0, 0), rook)

        # Move outside of bounds
        self.assertFalse(rook.is_valid_move((-1, 0, 0), self.board))
        self.assertFalse(rook.is_valid_move((0, 0, 4), self.board))

    def test_piece_factory_invalid_type(self):
        """Tests that the piece factory raises an error for invalid piece types."""
        with self.assertRaises(ValueError):
            self.piece_factory.create_piece('X', 'W', (0, 0, 0))

    def test_is_within_bounds(self):
        """Tests the is_within_bounds method of the Board."""
        self.assertTrue(self.board.is_within_bounds((0, 0, 0)))
        self.assertFalse(self.board.is_within_bounds((-1, 0, 0)))
        self.assertFalse(self.board.is_within_bounds((self.board._nx, 0, 0)))
        self.assertFalse(self.board.is_within_bounds((0, self.board._ny, 0)))
        self.assertFalse(self.board.is_within_bounds((0, 0, self.board._nz)))

    def test_set_piece_out_of_bounds(self):
        """Tests setting a piece out of bounds."""
        pawn = self.piece_factory.create_piece('P', 'W', (0, 0, 0))
        with self.assertLogs(level='WARNING') as cm:
            self.board.set_piece((-1, 0, 0), pawn)
        self.assertIn('Attempted to set piece at out-of-bounds position', ''.join(cm.output))


    def test_initialize_board(self):
        """Tests that the board initializes with the correct number of pieces."""
        self.board.initialize_board()
        total_pieces = len(self.board._pieces)

        # Calculate expected pieces based on initialization logic
        # For example:
        pawns_per_color = self.board._ny * self.board._nz  # Number of pawns per color
        main_pieces_per_color = 16  # Adjust based on actual main pieces placed
        expected_pieces = 2 * (pawns_per_color + main_pieces_per_color)

        self.assertEqual(total_pieces, expected_pieces)


    def test_visualize(self):
        """Tests that the visualize method runs without error."""
        try:
            self.board.visualize()
        except Exception as e:
            self.fail(f"Visualization failed with exception: {e}")


if __name__ == '__main__':
    logging.basicConfig(level=logging.WARNING)
    unittest.main()
