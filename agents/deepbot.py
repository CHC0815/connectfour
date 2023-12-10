import numpy as np
from stable_baselines3 import PPO

import connectfour.utils as utils

model = PPO.load("models/ppo_connectfour")


def bot(obs, config):
    col, _ = model.predict(np.array(obs.board).reshape(1, config.rows, config.columns))
    return int(col)
