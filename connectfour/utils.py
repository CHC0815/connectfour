import numpy as np


def opponent_mark(obs):
    """retuns the opponent's mark

    Args:
        obs: observation object

    Returns:
        int: 1 or 2
    """
    return 2 if obs.mark == 1 else 1


def drop_piece(grid, col, piece, config):
    """Drops a piece into a column in the grid

    Args:
        grid: The game board
        col: The column to drop the piece into
        piece: The piece of the player
        config: The game configuration

    Returns:
        grid: The game board with the piece dropped
    """
    next_grid = grid.copy()
    for row in range(config.rows - 1, -1, -1):
        if next_grid[row][col] == 0:
            break
    next_grid[row][col] = piece
    return next_grid


def get_valid_moves(obs, config):
    """Gets the valid moves for the current player

    Args:
        obs: observation object
        config: The game configuration

    Returns:
        list: A list of valid moves
    """
    valid_moves = [col for col in range(config.columns) if obs.board[col] == 0]
    return valid_moves


def check_win(obs, config, piece):
    """Checks if the current player has won

    Args:
        obs: observation object
        config: The game configuration
        piece: The player's piece

    Returns:
        bool: True if the player has won
    """
    # Convert the board to a 2D grid
    grid = np.asarray(obs.board).reshape(config.rows, config.columns)
    # horizontal
    for row in range(config.rows):
        for col in range(config.columns - (config.inarow - 1)):
            window = list(next_grid[row, col : col + config.inarow])
            if window.count(piece) == config.inarow:
                return True
    # vertical
    for row in range(config.rows - (config.inarow - 1)):
        for col in range(config.columns):
            window = list(next_grid[row : row + config.inarow, col])
            if window.count(piece) == config.inarow:
                return True
    # positive diagonal
    for row in range(config.rows - (config.inarow - 1)):
        for col in range(config.columns - (config.inarow - 1)):
            window = list(
                next_grid[range(row, row + config.inarow), range(col, col + config.inarow)]
            )
            if window.count(piece) == config.inarow:
                return True
    # negative diagonal
    for row in range(config.inarow - 1, config.rows):
        for col in range(config.columns - (config.inarow - 1)):
            window = list(
                next_grid[range(row, row - config.inarow, -1), range(col, col + config.inarow)]
            )
            if window.count(piece) == config.inarow:
                return True
    return False
