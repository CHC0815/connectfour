# import gymnasium as gym
import gym
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd  # type:ignore
from gym import spaces

import connectfour.utils as utils
from connectfour.ConnectFour import ConnectFour


class ConnectFourGym(gym.Env):
    def __init__(self, agent2="random"):
        self.env = ConnectFour(utils.get_agent("random"), utils.get_agent(agent2))
        self.rows = self.env.config.rows
        self.columns = self.env.config.columns
        # Learn about spaces here: http://gym.openai.com/docs/#spaces
        self.action_space = spaces.Discrete(self.columns)
        self.observation_space = spaces.Box(
            low=0, high=2, shape=(1, self.rows, self.columns), dtype=int  # type:ignore
        )
        # Tuple corresponding to the min and max possible rewards
        self.reward_range = (-10, 1)
        # StableBaselines throws error if these are not defined
        self.spec = None  # type:ignore
        self.metadata = None  # type:ignore

    def reset(self):
        self.obs = self.env.reset()
        return np.array(self.obs.board).reshape(1, self.rows, self.columns)

    def change_reward(self, old_reward, done):
        if old_reward == 1:  # The agent won the game
            return 1
        elif done:  # The opponent won the game
            return -1
        else:  # Reward 1/42
            return 1 / (self.rows * self.columns)

    def step(self, action):
        # Check if agent's move is valid
        is_valid = self.obs.board[int(action)] == 0
        if is_valid:  # Play the move
            # self.obs, old_reward, done, _ = self.env.step(int(action))
            self.obs, old_reward, done = self.env.training_step(int(action))
            reward = self.change_reward(old_reward, done)
            _ = {}
        else:  # End the game and penalize agent
            reward, done, _ = -10, True, {}
        return np.array(self.obs.board).reshape(1, self.rows, self.columns), reward, done, _


import torch as th
import torch.nn as nn
from stable_baselines3 import PPO
from stable_baselines3.common.torch_layers import BaseFeaturesExtractor


# Neural network for predicting action values
class CustomCNN(BaseFeaturesExtractor):
    def __init__(self, observation_space: spaces.Box, features_dim: int = 128):
        super(CustomCNN, self).__init__(observation_space, features_dim)  # type:ignore
        # CxHxW images (channels first)
        n_input_channels = observation_space.shape[0]
        self.cnn = nn.Sequential(
            nn.Conv2d(n_input_channels, 32, kernel_size=3, stride=1, padding=0),
            nn.ReLU(),
            nn.Conv2d(32, 64, kernel_size=3, stride=1, padding=0),
            nn.ReLU(),
            nn.Flatten(),
        )

        # Compute shape by doing one forward pass
        with th.no_grad():
            n_flatten = self.cnn(th.as_tensor(observation_space.sample()[None]).float()).shape[1]

        self.linear = nn.Sequential(nn.Linear(n_flatten, features_dim), nn.ReLU())

    def forward(self, observations: th.Tensor) -> th.Tensor:
        return self.linear(self.cnn(observations))


def train_bot():
    # Create ConnectFour environment
    env = ConnectFourGym(agent2="onestep")

    policy_kwargs = dict(
        features_extractor_class=CustomCNN,
    )
    # Initialize agent
    model = PPO("CnnPolicy", env, policy_kwargs=policy_kwargs, verbose=0)  # type:ignore

    # Train agent
    model.learn(total_timesteps=50000)

    model.save("models/ppo_connectfour")
