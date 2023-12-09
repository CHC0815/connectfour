import numpy as np

import connectfour.utils as utils


class Observation:
    def __init__(self):
        self.board = np.zeros(42, dtype=int)
        self.player = 1

    def reset(self):
        self.board = np.zeros(42, dtype=int)
        self.player = 1

    def step(self, col, config) -> bool:
        if col not in utils.get_valid_moves(self, config):
            return False
        self.board = utils.drop_piece(
            self.board.reshape(config.rows, config.columns), col, self.player, config
        ).flatten()
        self.player = 1 if self.player == 2 else 2
        return True
