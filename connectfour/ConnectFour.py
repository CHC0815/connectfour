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

    def reset(self) -> Observation:
        self.obs.reset()
        return self.obs

    def step(self, action: int) -> Tuple[bool, bool, bool, int]:
        # check if last game was a draw
        if utils.get_valid_moves(self.obs, self.config) == [-1]:
            return False, False, True, 0

        is_valid = self.obs.step(action, self.config)

        return (
            is_valid,
            utils.check_win(self.obs, self.config, self.obs.player),
            False,
            self.obs.player,
        )

    def training_step(self, action: int) -> Tuple[Observation, int, bool]:
        # check if last game was a draw
        if utils.get_valid_moves(self.obs, self.config) == [-1]:
            return self.obs, 0, True

        is_valid = self.obs.step(action, self.config)  # training step

        # if not a valid move report back to agent
        if not is_valid:
            return self.obs, 0, True

        # check if game is won
        win = utils.check_win(self.obs, self.config, self.obs.player)
        if win:
            return self.obs, 1, False

        # perform opponents move
        # check if last game was a draw
        if utils.get_valid_moves(self.obs, self.config) == [-1]:
            return self.obs, 0, True
        valid_moves = utils.get_valid_moves(self.obs, self.config)
        opponent_action = self.player2(self.obs, self.config)
        is_valid = self.obs.step(opponent_action, self.config)
        # not a valid move from opponent so the agent won
        if not is_valid:
            return self.obs, 1, False

        # check if the opponent won
        win = utils.check_win(self.obs, self.config, self.obs.player)
        if win:
            return self.obs, -1, True

        # not lost not won
        return self.obs, 0, False
