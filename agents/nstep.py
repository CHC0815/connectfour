def bot(obs, config):
    # Your code here: Amend the agent!
    import random

    import numpy as np

    import connectfour.utils as utils

    ABP = True

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

    # Helper function for score_move: gets board at next step if agent drops piece in selected column
    def drop_piece(grid, col, mark, config):
        next_grid = grid.copy()
        for row in range(config.rows - 1, -1, -1):
            if next_grid[row][col] == 0:
                break
        next_grid[row][col] = mark  # type:ignore
        return next_grid

    # Uses minimax to calculate value of dropping piece in selected column
    def score_move(grid, col, mark, config, nsteps):
        next_grid = drop_piece(grid, col, mark, config)
        if ABP:
            return minimax_abp(next_grid, nsteps - 1, False, mark, config, -np.Inf, np.Inf)
        return minimax(next_grid, nsteps - 1, False, mark, config)

    # Helper function for minimax: checks if agent or opponent has four in a row in the window
    def is_terminal_window(window, config):
        return window.count(1) == config.inarow or window.count(2) == config.inarow

    # Helper function for minimax: checks if game has ended
    def is_terminal_node(grid, config):
        # Check for draw
        if list(grid[0, :]).count(0) == 0:
            return True
        # Check for win: horizontal, vertical, or diagonal
        # horizontal
        for row in range(config.rows):
            for col in range(config.columns - (config.inarow - 1)):
                window = list(grid[row, col : col + config.inarow])
                if is_terminal_window(window, config):
                    return True
        # vertical
        for row in range(config.rows - (config.inarow - 1)):
            for col in range(config.columns):
                window = list(grid[row : row + config.inarow, col])
                if is_terminal_window(window, config):
                    return True
        # positive diagonal
        for row in range(config.rows - (config.inarow - 1)):
            for col in range(config.columns - (config.inarow - 1)):
                window = list(
                    grid[range(row, row + config.inarow), range(col, col + config.inarow)]
                )
                if is_terminal_window(window, config):
                    return True
        # negative diagonal
        for row in range(config.inarow - 1, config.rows):
            for col in range(config.columns - (config.inarow - 1)):
                window = list(
                    grid[range(row, row - config.inarow, -1), range(col, col + config.inarow)]
                )
                if is_terminal_window(window, config):
                    return True
        return False

    # Minimax implementation
    def minimax(node, depth, maximizingPlayer, mark, config):
        is_terminal = is_terminal_node(node, config)
        valid_moves = [c for c in range(config.columns) if node[0][c] == 0]
        if depth == 0 or is_terminal:
            return get_heuristic(node, mark, config)
        if maximizingPlayer:
            value = -np.Inf
            for col in valid_moves:
                child = drop_piece(node, col, mark, config)
                value = max(value, minimax(child, depth - 1, False, mark, config))
            return value
        else:
            value = np.Inf
            for col in valid_moves:
                child = drop_piece(node, col, mark % 2 + 1, config)
                value = min(value, minimax(child, depth - 1, True, mark, config))
            return value

    # Minimax implementation with alpha-beta pruning
    def minimax_abp(node, depth, maximizingPlayer, mark, config, alpha, beta):
        is_terminal = is_terminal_node(node, config)
        valid_moves = [c for c in range(config.columns) if node[0][c] == 0]
        if depth == 0 or is_terminal:
            return get_heuristic(node, mark, config)

        if maximizingPlayer:
            best = -np.Inf
            for col in valid_moves:
                child = drop_piece(node, col, mark, config)
                value = minimax_abp(child, depth - 1, False, mark, config, alpha, beta)
                best = max(best, value)
                alpha = max(alpha, best)
                if beta <= alpha:
                    break
            return best
        else:
            best = np.Inf
            for col in valid_moves:
                child = drop_piece(node, col, mark % 2 + 1, config)
                value = minimax_abp(child, depth - 1, True, mark, config, alpha, beta)
                best = min(best, value)
                beta = min(beta, best)
                if beta <= alpha:
                    break
            return best

    # How deep to make the game tree: higher values take longer to run!
    N_STEPS = 3

    def agent(obs, config):
        # Get list of valid moves
        valid_moves = [c for c in range(config.columns) if obs.board[c] == 0]
        # Convert the board to a 2D grid
        grid = np.asarray(obs.board).reshape(config.rows, config.columns)
        # Use the heuristic to assign a score to each possible board in the next step
        scores = dict(
            zip(
                valid_moves,
                [score_move(grid, col, obs.player, config, N_STEPS) for col in valid_moves],
            )
        )
        # Get a list of columns (moves) that maximize the heuristic
        max_cols = [key for key in scores.keys() if scores[key] == max(scores.values())]
        # Select at random from the maximizing columns
        return random.choice(max_cols)

    return agent(obs, config)
