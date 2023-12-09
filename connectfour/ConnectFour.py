from typing import Tuple

import numpy as np

import connectfour.utils as utils
from connectfour.Agent import Agent


class ConnectFourConfig:
    def __init__(self, rows, cols, inarow=4):
        self.rows = rows
        self.columns = cols
        self.inarow = inarow


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


class ConnectFour:
    def __init__(self, player1: Agent, player2: Agent):
        self.obs = Observation()
        self.config = ConnectFourConfig(6, 7)
        self.player1 = player1
        self.player2 = player2

    def reset(self):
        self.obs.reset()

    def step(self) -> Tuple[bool, bool, int]:
        bot = self.player1 if self.obs.player == 1 else self.player2
        col = bot(self.obs, self.config, self.obs.player)

        is_valid = self.obs.step(col, self.config)

        return is_valid, utils.check_win(self.obs, self.config, self.obs.player), self.obs.player
