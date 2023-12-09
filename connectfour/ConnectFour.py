from typing import Tuple

import numpy as np

from connectfour.utils import check_win, drop_piece, get_valid_moves


class ConnectFour:
    def __init__(self, player1, player2):
        self.obs = np.zeros(42, dtype=int)
        self.config = {
            "rows": 7,
            "cols": 6,
        }
        self.player = 1
        self.player1 = player1
        self.player2 = player2

    def reset(self):
        self.obs = np.zeros(42, dtype=int)
        self.player = 1
        return self.obs

    def step(self) -> Tuple[bool, bool, int]:
        bot = self.player1 if self.player == 1 else self.player2
        col = bot(self.obs, self.config, self.player)
        if col not in get_valid_moves(self.obs, self.config):
            return False, False, self.player
        grid = drop_piece(self.obs, col, self.player, self.config)
        self.obs = grid.flatten()
        return True, check_win(self.obs, self.config, self.player), self.player
