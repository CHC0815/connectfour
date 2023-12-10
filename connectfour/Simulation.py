import multiprocessing

import tqdm  # type: ignore

import connectfour.Agent as Agent
import connectfour.utils as utils
from connectfour.ConnectFour import ConnectFour


class Simulation:
    def __init__(self, agent1: Agent.Agent, agent2: Agent.Agent, n_runs: int):
        self.agent1 = agent1
        self.agent2 = agent2
        self.n_runs = n_runs

        self.player1_wins = 0
        self.palyer2_wins = 0
        self.draws = 0

    def print_results(self):
        print(
            f"Player 1 won {self.player1_wins} games ({self.player1_wins / self.n_runs * 100:.2f}%)"
        )
        print(
            f"Player 2 won {self.palyer2_wins} games ({self.palyer2_wins / self.n_runs * 100:.2f}%)"
        )
        print(f"Draws: {self.draws}")

    def run(self):
        pool = multiprocessing.Pool()
        who = []
        for result in tqdm.tqdm(
            pool.imap(
                self.sim_game, [(self.agent1, self.agent2, False, i) for i in range(self.n_runs)]
            ),
            total=self.n_runs,
        ):
            who.append(result)
        pool.close()

        self.player1_wins = who.count(1)
        self.palyer2_wins = who.count(2)
        self.draws = who.count(0)

    @staticmethod
    def sim_game(param: tuple[Agent.Agent, Agent.Agent, bool, int]) -> int:
        agent1, agent2, render, game_id = param
        env = ConnectFour(agent1, agent2)
        while True:
            valid_move, win, draw, player = env.step()
            if draw:
                return 0
            if not valid_move:
                return utils.opponent_mark(env.obs)
            if win:
                return player
