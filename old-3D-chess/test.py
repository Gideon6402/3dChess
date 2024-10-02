from main import *

# Function to run tests
def run_tests():
    print("Running tests...")

    # Test pawn movement
    print("Testing pawn movement...")
    initialize_board()
    board.fill('  ')  # Clear the board
    board[1, 0, 0] = 'WP'  # Place a white pawn at (1, 0, 0)
    # Test that pawn can move forward one square
    assert is_valid_move('W', (1, 0, 0), (2, 0, 0))[0], "Pawn forward move failed"
    # Test that pawn cannot move two squares forward
    assert not is_valid_move('W', (1, 0, 0), (3, 0, 0))[0], "Pawn moved too far"
    # Test that pawn cannot move sideways
    assert not is_valid_move('W', (1, 0, 0), (1, 1, 0))[0], "Pawn moved sideways"

    # Test pawn capturing
    print("Testing pawn capturing...")
    initialize_board()
    board.fill('  ')  # Clear the board
    board[1, 0, 0] = 'WP'  # White pawn
    board[2, 0, 1] = 'BP'  # Black pawn diagonally ahead
    # Test pawn capture
    assert is_valid_move('W', (1, 0, 0), (2, 0, 1))[0], "Pawn capture failed"

    # Test rook movement
    print("Testing rook movement...")
    initialize_board()
    board.fill('  ')  # Clear the board
    board[0, 0, 0] = 'WR'  # Place a white rook at (0, 0, 0)
    # Test vertical movement along Y-axis
    assert is_valid_move('W', (0, 0, 0), (0, 3, 0))[0], "Rook vertical move failed"
    # Test horizontal movement along Z-axis
    assert is_valid_move('W', (0, 0, 0), (0, 0, 3))[0], "Rook horizontal move failed"
    # Test movement along X-axis (layers)
    assert is_valid_move('W', (0, 0, 0), (7, 0, 0))[0], "Rook X-axis move failed"
    # Test invalid diagonal movement
    assert not is_valid_move('W', (0, 0, 0), (3, 3, 0))[0], "Rook diagonal move incorrectly allowed"

    # Test bishop movement
    print("Testing bishop movement...")
    initialize_board()
    board.fill('  ')  # Clear the board
    board[0, 0, 0] = 'WB'  # Place a white bishop at (0, 0, 0)
    # Test diagonal movement in YZ-plane
    assert is_valid_move('W', (0, 0, 0), (0, 3, 3))[0], "Bishop diagonal move in YZ-plane failed"
    # Test diagonal movement in XY-plane
    assert is_valid_move('W', (0, 0, 0), (3, 3, 0))[0], "Bishop diagonal move in XY-plane failed"
    # Test diagonal movement in XZ-plane
    assert is_valid_move('W', (0, 0, 0), (3, 0, 3))[0], "Bishop diagonal move in XZ-plane failed"
    # Test invalid movement
    assert not is_valid_move('W', (0, 0, 0), (3, 2, 1))[0], "Bishop invalid move incorrectly allowed"

    # Test knight movement
    print("Testing knight movement...")
    initialize_board()
    board.fill('  ')  # Clear the board
    board[0, 1, 1] = 'WN'  # Place a white knight at (0, 1, 1)

    # Valid knight moves (dx^2 + dy^2 + dz^2 == 5)
    valid_knight_moves = [
        (2, 1, 0),  # Move to (2, 2, 1)
        (2, -1, 0),  # Move to (2, 0, 1)
        (2, 0, 1),  # Move to (2, 1, 2)
        (2, 0, -1),  # Move to (2, 1, 0)
        (1, 2, 0),  # Move to (1, 3, 1)
        (1, -2, 0),  # Move to (1, -1, 1)
        (1, 0, 2),  # Move to (1, 1, 3)
        (1, 0, -2),  # Move to (1, 1, -1)
        (0, 2, 1),  # Move to (0, 3, 2)
        (0, -2, 1),  # Move to (0, -1, 2)
        (0, 1, 2),  # Move to (0, 2, 3)
        (0, -1, 2),  # Move to (0, 0, 3)
    ]

    # Test valid knight moves
    for dx, dy, dz in valid_knight_moves:
        to_pos = (0 + dx, 1 + dy, 1 + dz)
        # Check if the target position is within bounds
        if all(0 <= i < n for i, n in zip(to_pos, (nx, ny, nz))):
            valid, message = is_valid_move('W', (0, 1, 1), to_pos)
            assert valid, f"Knight valid move to {to_pos} incorrectly identified as invalid: {message}"
        else:
            # Move is off the board; ensure it's invalid
            valid, message = is_valid_move('W', (0, 1, 1), to_pos)
            assert not valid, f"Knight move to off-board position {to_pos} incorrectly identified as valid"

    # Invalid knight moves (dx^2 + dy^2 + dz^2 != 5)
    invalid_knight_moves = [
        (2, 2, 0),  # Move to (2, 3, 1)
        (0, 0, 0),  # Move to (0, 1, 1)
        (1, 1, 1),  # Move to (1, 2, 2)
        (3, 0, 0),  # Move to (3, 1, 1)
        (-1, -1, -1),  # Move to (-1, 0, 0)
    ]

    # Test invalid knight moves
    for dx, dy, dz in invalid_knight_moves:
        to_pos = (0 + dx, 1 + dy, 1 + dz)
        # Check if the target position is within bounds
        if all(0 <= i < n for i, n in zip(to_pos, (nx, ny, nz))):
            valid, message = is_valid_move('W', (0, 1, 1), to_pos)
            assert not valid, f"Knight invalid move to {to_pos} incorrectly identified as valid"
        else:
            # Move is off the board; ensure it's invalid
            valid, message = is_valid_move('W', (0, 1, 1), to_pos)
            assert not valid, f"Knight move to off-board position {to_pos} incorrectly identified as valid"
    # Test king movement
    print("Testing king movement...")
    initialize_board()
    board.fill('  ')  # Clear the board
    board[3, 3, 3] = 'WK'  # Place a white king at (3, 3, 3)
    # Test one-square movement
    assert is_valid_move('W', (3, 3, 3), (4, 3, 3))[0], "King move failed"
    # Test invalid movement (too far)
    assert not is_valid_move('W', (3, 3, 3), (5, 3, 3))[0], "King moved too far"

    # Test capturing
    print("Testing capturing...")
    initialize_board()
    board.fill('  ')  # Clear the board
    board[0, 0, 0] = 'WR'  # White rook
    board[0, 3, 0] = 'BP'  # Black pawn at (0, 3, 0)
    # Test that rook can capture
    assert is_valid_move('W', (0, 0, 0), (0, 3, 0))[0], "Rook capturing failed"

    # Test checkmate detection
    print("Testing checkmate detection...")
    initialize_board()
    board.fill('  ')  # Clear the board
    board[7, 0, 0] = 'BK'  # Black King at (7, 0, 0)
    board[6, 0, 0] = 'WQ'  # White Queen at (6, 0, 0), putting king in check
    board[6, 1, 0] = 'WR'  # White Rook at (6, 1, 0), supporting the queen
    # Check if the game recognizes checkmate
    assert is_game_over('B'), "Checkmate detection failed"

    print("All tests passed successfully.")



if __name__ == "__main__":
    run_tests()