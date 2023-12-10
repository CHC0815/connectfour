import multiprocessing

import connectfour.utils as utils
from agents.nstep import bot as nstep_bot
from agents.onestep import bot as onestep_bot
from agents.random_bot import bot as random_bot
from connectfour.Agent import Agent
from connectfour.ConnectFour import ConnectFour
from connectfour.display import PygameDisplay


def sim_game(param: tuple[Agent, Agent, bool, int]) -> int:
    agent1, agent2, render, game_id = param
    print(f"Starting Game: {game_id}")
    env = ConnectFour(agent1, agent2)
    while True:
        valid_move, win, draw, player = env.step()
        if draw:
            return 0
        if not valid_move:
            return utils.opponent_mark(env.obs)

        if win:
            return player


def main(n_games: int, render=False):
    agent1 = random_bot
    agent2 = nstep_bot
    pool = multiprocessing.Pool()
    who = []

    for result in pool.imap(sim_game, [(agent1, agent2, render, i) for i in range(n_games)]):
        who.append(result)

    pool.close()

    player_1_wins = who.count(1)
    print(f"Player 1 won {player_1_wins} games ({player_1_wins / n_games * 100:.2f}%)")
    print(
        f"Player 2 won {n_games - player_1_wins} games ({(n_games - player_1_wins) / n_games * 100:.2f}%)"
    )
    print(f"Draws: {who.count(0)}")


if __name__ == "__main__":
    main(100)
