import numpy as np

import agents.nstep as nstep
import agents.onestep as onestep
import agents.random_bot as random
from connectfour.ConnectFour import ConnectFourConfig, Observation


def opponent_mark(obs: Observation) -> int:
    """retuns the opponent's mark

    Args:
        obs: observation object

    Returns:
        int: 1 or 2
    """
    return 2 if obs.player == 1 else 1


def drop_piece(grid: np.ndarray, col: int, piece: int, config: ConnectFourConfig) -> np.ndarray:
    """Drops a piece into a column in the grid

    Args:
        grid: The game board
        col: The column to drop the piece into
        piece: The piece of the player
        config: The game configuration

    Returns:
        grid: The game board with the piece dropped
    """
    grid = grid.copy()
    for row in range(config.rows - 1, -1, -1):
        if grid[row][col] == 0:
            break
    grid[row][col] = piece  # type:ignore
    return grid


def get_valid_moves(obs: Observation, config: ConnectFourConfig) -> list[int]:
    """Gets the valid moves for the current player

    Args:
        obs: observation object
        config: The game configuration

    Returns:
        list: A list of valid moves
    """
    valid_moves = [col for col in range(config.columns) if obs.board[col] == 0]
    if len(valid_moves) == 0:
        return [-1]  # draw
    return valid_moves


def check_win(obs: Observation, config: ConnectFourConfig, piece: int) -> bool:
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
            window = list(grid[row, col : col + config.inarow])
            if window.count(piece) == config.inarow:
                return True
    # vertical
    for row in range(config.rows - (config.inarow - 1)):
        for col in range(config.columns):
            window = list(grid[row : row + config.inarow, col])
            if window.count(piece) == config.inarow:
                return True
    # positive diagonal
    for row in range(config.rows - (config.inarow - 1)):
        for col in range(config.columns - (config.inarow - 1)):
            window = list(grid[range(row, row + config.inarow), range(col, col + config.inarow)])
            if window.count(piece) == config.inarow:
                return True
    # negative diagonal
    for row in range(config.inarow - 1, config.rows):
        for col in range(config.columns - (config.inarow - 1)):
            window = list(
                grid[range(row, row - config.inarow, -1), range(col, col + config.inarow)]
            )
            if window.count(piece) == config.inarow:
                return True
    return False


def get_agent(name):
    if name == "random":
        return random.bot
    elif name == "onestep":
        return onestep.bot
    elif name == "nstep":
        return nstep.bot
    else:
        return load_agent(name)


def load_agent(name):
    import os
    from importlib.machinery import SourceFileLoader

    if not os.path.isfile(name):
        raise FileNotFoundError("Agent {} not found".format(name))

    file = SourceFileLoader("agent", name).load_module()
    return file.bot
