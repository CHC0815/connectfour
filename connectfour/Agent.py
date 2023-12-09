from typing import Callable

from connectfour.ConnectFourConfig import ConnectFourConfig
from connectfour.Observation import Observation

Agent = Callable[[Observation, ConnectFourConfig, int], int]
