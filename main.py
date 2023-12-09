import connectfour.utils as utils
from agents.random_bot import bot as random_bot
from connectfour.Agent import Agent
from connectfour.ConnectFour import ConnectFour
from connectfour.display import PygameDisplay


def sim_game(agent1: Agent, agent2: Agent, render: bool = False) -> int:
    env = ConnectFour(agent1, agent2)
    if render:
        display = PygameDisplay()
    while True:
        valid_move, win, draw, player = env.step()
        if draw:
            return 0
        if not valid_move:
            return utils.opponent_mark(env.obs)

        if win:
            return player
        if render:
            display.render(env.obs, env.config)  # type: ignore
            display.clock.tick(10)  # type:ignore


def main(n_games: int, render=False):
    agent1 = random_bot
    agent2 = random_bot
    who = []
    for _ in range(n_games):
        who.append(sim_game(agent1, agent2, render))

    player_1_wins = who.count(1)
    print(f"Player 1 won {player_1_wins} games ({player_1_wins / n_games * 100:.2f}%)")
    print(
        f"Player 2 won {n_games - player_1_wins} games ({(n_games - player_1_wins) / n_games * 100:.2f}%)"
    )
    print(f"Draws: {who.count(0)}")


if __name__ == "__main__":
    main(100)
