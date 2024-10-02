import numpy as np
import matplotlib.pyplot as plt

# Define the dimensions of the chessboard
nx = 8  # Number of layers in the X-direction (height)
ny = 4  # Number of rows in the Y-direction
nz = 4  # Number of columns in the Z-direction

# Initialize the board
# Each cell can be empty ('  '), or contain a piece (e.g., 'WK' for White King)
board = np.full((nx, ny, nz), '  ', dtype=object)

# Define the pieces for each player
pieces = ['K', 'Q', 'R', 'B', 'N', 'P']  # King, Queen, Rook, Bishop, Knight, Pawn
players = ['W', 'B']  # White and Black

# Place initial pieces on the board
def initialize_board():
    # White pieces (Player W)
    # Place 2 kings and 2 queens in the middle cubes of layer 0
    board[0, 1, 1] = 'WK'
    board[0, 1, 2] = 'WQ'
    board[0, 2, 1] = 'WQ'
    board[0, 2, 2] = 'WK'

    # Place 4 rooks on the outer cubes of layer 0
    board[0, 0, 0] = 'WR'
    board[0, 0, 3] = 'WR'
    board[0, 3, 0] = 'WR'
    board[0, 3, 3] = 'WR'

    # Place knights and bishops logically on layer 0
    board[0, 0, 1] = 'WN'
    board[0, 0, 2] = 'WB'
    board[0, 3, 1] = 'WB'
    board[0, 3, 2] = 'WN'
    board[0, 1, 0] = 'WB'
    board[0, 2, 0] = 'WN'
    board[0, 1, 3] = 'WN'
    board[0, 2, 3] = 'WB'

    # Place pawns on layer 1
    for y in range(ny):
        for z in range(nz):
            board[1, y, z] = 'WP'

    # Black pieces (Player B)
    # Place 2 kings and 2 queens in the middle cubes of layer 7
    board[7, 1, 1] = 'BK'
    board[7, 1, 2] = 'BQ'
    board[7, 2, 1] = 'BQ'
    board[7, 2, 2] = 'BK'

    # Place 4 rooks on the outer cubes of layer 7
    board[7, 0, 0] = 'BR'
    board[7, 0, 3] = 'BR'
    board[7, 3, 0] = 'BR'
    board[7, 3, 3] = 'BR'

    # Place knights and bishops logically on layer 7
    board[7, 0, 1] = 'BN'
    board[7, 0, 2] = 'BB'
    board[7, 3, 1] = 'BB'
    board[7, 3, 2] = 'BN'
    board[7, 1, 0] = 'BB'
    board[7, 2, 0] = 'BN'
    board[7, 1, 3] = 'BN'
    board[7, 2, 3] = 'BB'

    # Place pawns on layer 6
    for y in range(ny):
        for z in range(nz):
            board[6, y, z] = 'BP'

# Function to visualize the board
def visualize_board():
    fig = plt.figure(figsize=(8, 10))
    ax = fig.add_subplot(111, projection='3d')
    x, y, z = np.indices((nx+1, ny+1, nz+1))

    # Define the positions of the cubes
    voxels = (x < nx) & (y < ny) & (z < nz)

    # Make the cubes fully transparent by setting facecolors to 'none'
    facecolors = np.zeros(voxels.shape + (4,))
    facecolors[..., -1] = 0  # Alpha channel set to 0 (fully transparent)

    # Set edge colors to gray with 50% transparency
    edgecolors = np.zeros(voxels.shape + (4,))
    edgecolors[..., :] = [0.5, 0.5, 0.5, 0.5]  # Gray color with 50% alpha

    # Plot the voxels with transparent faces and semi-transparent edges
    ax.voxels(voxels, facecolors=facecolors, edgecolors=edgecolors)

    # Plot the pieces
    for x_coord in range(nx):
        for y_coord in range(ny):
            for z_coord in range(nz):
                piece = board[x_coord, y_coord, z_coord]
                if piece.strip():
                    # Use red for one player and green for the other
                    if piece[0] == 'W':
                        color = 'red'
                    else:
                        color = 'green'
                    # Plot the piece as a text label
                    ax.text(
                        x_coord + 0.5, y_coord + 0.5, z_coord + 0.5,
                        piece[1], color=color, fontsize=12,
                        ha='center', va='center'
                    )

    # Set labels for the axes
    ax.set_xlabel('X-axis (Layers)')
    ax.set_ylabel('Y-axis (Rows)')
    ax.set_zlabel('Z-axis (Columns)')

    # Set the aspect ratio for better visualization
    ax.set_box_aspect([nx, ny, nz])

    # Set the ticks
    ax.set_xticks(range(nx))
    ax.set_yticks(range(ny))
    ax.set_zticks(range(nz))

    # Invert the X-axis to have layer 0 at the bottom
    ax.invert_xaxis()

    # Display the plot
    plt.show()

# Function to convert user input to board indices
def parse_move(move_str):
    try:
        # Expected format: x,y,z
        x_str, y_str, z_str = move_str.strip().split(',')
        return int(x_str), int(y_str), int(z_str)
    except ValueError:
        return None

# Function to check if a move is valid
def is_valid_move(player, from_pos, to_pos):
    fx, fy, fz = from_pos
    tx, ty, tz = to_pos

    # Check if from and to positions are within the board
    if not all(0 <= i < nx for i in [fx, tx]) or not all(0 <= i < ny for i in [fy, ty]) or not all(0 <= i < nz for i in [fz, tz]):
        return False, "Positions out of bounds."

    # Check if there is a piece at from_pos
    piece = board[fx, fy, fz]
    if piece.strip() == '' or piece[0] != player:
        return False, "No valid piece at the source position."

    # Check if the destination is occupied by the player's own piece
    dest_piece = board[tx, ty, tz]
    if dest_piece.strip() != '' and dest_piece[0] == player:
        return False, "Cannot capture your own piece."

    # Determine movement rules based on piece type
    piece_type = piece[1]
    dx = tx - fx
    dy = ty - fy
    dz = tz - fz

    # Check if movement is in one plane (only two axes can change)
    planes_moved = sum([dx != 0, dy != 0, dz != 0])
    if planes_moved > 2:
        return False, "Pieces can only move in one plane."

    # Movement logic for each piece
    if piece_type == 'P':  # Pawn
        direction = 1 if player == 'W' else -1
        # Forward move without capture
        if dx == direction and dy == 0 and dz == 0 and dest_piece.strip() == '':
            return True, ""
        # Diagonal capture in any one direction
        elif dx == direction and ((abs(dy) == 1 and dz == 0) or (dy == 0 and abs(dz) == 1)) and \
             dest_piece.strip() != '' and dest_piece[0] != player:
            return True, ""
        else:
            return False, "Invalid pawn move."
    elif piece_type == 'R':  # Rook
        if not ((dx == 0 and dy == 0 and dz != 0) or
                (dx == 0 and dy != 0 and dz == 0) or
                (dx != 0 and dy == 0 and dz == 0)):
            return False, "Invalid rook move."
        # Check for obstacles
        if not is_clear_path(from_pos, to_pos):
            return False, "Path is not clear."
        return True, ""
    elif piece_type == 'B':  # Bishop
        if not ((abs(dx) == abs(dy) and dz == 0) or
                (abs(dx) == abs(dz) and dy == 0) or
                (abs(dy) == abs(dz) and dx == 0)):
            return False, "Invalid bishop move."
        if not is_clear_path(from_pos, to_pos):
            return False, "Path is not clear."
        return True, ""
    elif piece_type == 'N':  # Knight
        moves = [
            (2, 1, 0), (1, 2, 0), (2, 0, 1), (1, 0, 2),
            (0, 2, 1), (0, 1, 2)
        ]
        if (abs(dx), abs(dy), abs(dz)) not in moves:
            return False, "Invalid knight move."
        return True, ""
    elif piece_type == 'Q':  # Queen
        # Combines Rook and Bishop moves
        valid_rook_move = ((dx == 0 and dy == 0 and dz != 0) or
                           (dx == 0 and dy != 0 and dz == 0) or
                           (dx != 0 and dy == 0 and dz == 0))
        valid_bishop_move = ((abs(dx) == abs(dy) and dz == 0) or
                             (abs(dx) == abs(dz) and dy == 0) or
                             (abs(dy) == abs(dz) and dx == 0))
        if not (valid_rook_move or valid_bishop_move):
            return False, "Invalid queen move."
        if not is_clear_path(from_pos, to_pos):
            return False, "Path is not clear."
        return True, ""
    elif piece_type == 'K':  # King
        if max(abs(dx), abs(dy), abs(dz)) != 1:
            return False, "Invalid king move."
        return True, ""
    else:
        return False, "Unknown piece type."

# Function to check if the path between from_pos and to_pos is clear
def is_clear_path(from_pos, to_pos):
    fx, fy, fz = from_pos
    tx, ty, tz = to_pos
    dx = np.sign(tx - fx)
    dy = np.sign(ty - fy)
    dz = np.sign(tz - fz)

    x, y, z = fx + dx, fy + dy, fz + dz
    while (x, y, z) != (tx, ty, tz):
        if board[x, y, z].strip() != '':
            return False
        x += dx if dx != 0 else 0
        y += dy if dy != 0 else 0
        z += dz if dz != 0 else 0
    return True

# Function to make a move
def make_move(player):
    while True:
        print(f"Player {player}'s turn.")
        from_str = input("Enter the position of the piece you want to move (x,y,z): ")
        to_str = input("Enter the position where you want to move the piece (x,y,z): ")

        from_pos = parse_move(from_str)
        to_pos = parse_move(to_str)

        if from_pos and to_pos:
            valid, message = is_valid_move(player, from_pos, to_pos)
            if valid:
                fx, fy, fz = from_pos
                tx, ty, tz = to_pos
                dest_piece = board[tx, ty, tz]
                # Check if capturing a king
                if dest_piece.strip() != '' and dest_piece[1] == 'K' and dest_piece[0] != player:
                    print(f"{player} captured a king!")
                # Move the piece
                board[tx, ty, tz] = board[fx, fy, fz]
                board[fx, fy, fz] = '  '
                print(f"Moved from {from_pos} to {to_pos}")
                break
            else:
                print(f"Invalid move: {message}")
        else:
            print("Invalid input format. Please enter coordinates as x,y,z.")

# Function to check for game over condition
def is_game_over(opponent):
    kings = 0
    for x in range(nx):
        for y in range(ny):
            for z in range(nz):
                piece = board[x, y, z]
                if piece == opponent + 'K':
                    kings += 1
    return kings < 2

# Main game loop
def play_game():
    initialize_board()
    turn = 0

    while True:
        visualize_board()
        current_player = players[turn % 2]
        opponent = players[(turn + 1) % 2]
        make_move(current_player)
        if is_game_over(opponent):
            print(f"Player {current_player} wins!")
            visualize_board()
            break
        turn += 1

# Start the game
if __name__ == "__main__":
    play_game()
