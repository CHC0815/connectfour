import numpy as np

import connectfour.utils as utils


def bot(obs, config):
    # Your code here: Amend the agent!
    import random

    def get_heuristic(grid, mark, config):
        num_threes = count_windows(grid, 3, mark, config)
        num_fours = count_windows(grid, 4, mark, config)
        num_threes_opp = count_windows(grid, 3, mark % 2 + 1, config)
        score = num_threes - 1e2 * num_threes_opp + 1e6 * num_fours
        return score

    # Helper function for get_heuristic: checks if window satisfies heuristic conditions
    def check_window(window, num_discs, piece, config):
        return window.count(piece) == num_discs and window.count(0) == config.inarow - num_discs

    # Helper function for get_heuristic: counts number of windows satisfying specified heuristic conditions
    def count_windows(grid, num_discs, piece, config):
        num_windows = 0
        # horizontal
        for row in range(config.rows):
            for col in range(config.columns - (config.inarow - 1)):
                window = list(grid[row, col : col + config.inarow])
                if check_window(window, num_discs, piece, config):
                    num_windows += 1
        # vertical
        for row in range(config.rows - (config.inarow - 1)):
            for col in range(config.columns):
                window = list(grid[row : row + config.inarow, col])
                if check_window(window, num_discs, piece, config):
                    num_windows += 1
        # positive diagonal
        for row in range(config.rows - (config.inarow - 1)):
            for col in range(config.columns - (config.inarow - 1)):
                window = list(
                    grid[range(row, row + config.inarow), range(col, col + config.inarow)]
                )
                if check_window(window, num_discs, piece, config):
                    num_windows += 1
        # negative diagonal
        for row in range(config.inarow - 1, config.rows):
            for col in range(config.columns - (config.inarow - 1)):
                window = list(
                    grid[range(row, row - config.inarow, -1), range(col, col + config.inarow)]
                )
                if check_window(window, num_discs, piece, config):
                    num_windows += 1
        return num_windows

    # Calculates score if agent drops piece in selected column
    def score_move(grid, col, mark, config):
        next_grid = utils.drop_piece(grid, col, mark, config)
        score = get_heuristic(next_grid, mark, config)
        return score

    def brain(obs, config, valid_moves):
        valid_moves = [c for c in range(config.columns) if obs.board[c] == 0]
        # Convert the board to a 2D grid
        grid = np.asarray(obs.board).reshape(config.rows, config.columns)
        # Use the heuristic to assign a score to each possible board in the next turn
        scores = dict(
            zip(valid_moves, [score_move(grid, col, obs.player, config) for col in valid_moves])
        )
        # Get a list of columns (moves) that maximize the heuristic
        max_cols = [key for key in scores.keys() if scores[key] == max(scores.values())]
        # Select at random from the maximizing columns
        return random.choice(max_cols)

    return brain(obs, config, utils.get_valid_moves(obs, config))
