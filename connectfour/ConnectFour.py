from typing import Tuple

import numpy as np

import connectfour.Agent as Agent
import connectfour.utils as utils
from connectfour.ConnectFourConfig import ConnectFourConfig
from connectfour.Observation import Observation


class ConnectFour:
    def __init__(self, player1: Agent.Agent, player2: Agent.Agent):
        self.obs = Observation()
        self.config = ConnectFourConfig(6, 7)
        self.player1 = player1
        self.player2 = player2

    def reset(self):
        self.obs.reset()

    def step(self) -> Tuple[bool, bool, bool, int]:
        bot = self.player1 if self.obs.player == 1 else self.player2
        col = bot(self.obs, self.config, self.obs.player)

        # if is a draw
        if col == [-1] and utils.get_valid_moves(self.obs, self.config) == [-1]:
            return False, False, True, 0

        is_valid = self.obs.step(col, self.config)

        return (
            is_valid,
            utils.check_win(self.obs, self.config, self.obs.player),
            False,
            self.obs.player,
        )
