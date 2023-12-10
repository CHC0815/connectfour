import numpy as np
from stable_baselines3 import PPO


def bot(obs, config):
    model = PPO.load("models/ppo_connectfour")
    col, _ = model.predict(np.array(obs.board).reshape(1, config.rows, config.columns))
    return int(col)
