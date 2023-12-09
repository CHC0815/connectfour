from typing import Callable

import connectfour.ConnectFour as cf

Agent = Callable[[cf.Observation, cf.ConnectFourConfig, int], int]
