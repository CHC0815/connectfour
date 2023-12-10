import connectfour.Agent as Agent
import connectfour.ConnectFourConfig as ConnectFourConfig
import connectfour.Observation as Observation
import connectfour.utils as utils


class TestEnvironment:
    def __init__(self):
        self.obs = Observation.Observation()
        self.config = ConnectFourConfig.ConnectFourConfig(6, 7)

    def init(self, bot: Agent.Agent, n: int) -> Observation.Observation:
        for _ in range(n):
            action = bot(self.obs, self.config)
            is_valid = self.obs.step(action, self.config)

        return self.obs
