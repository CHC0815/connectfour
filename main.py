from agents.random_bot import bot as random_bot
from connectfour.ConnectFour import ConnectFour  # type:ignore
from connectfour.display import PygameDisplay  # type:ignore


def main():
    agent1 = random_bot

    env = ConnectFour(agent1, agent1)
    display = PygameDisplay()
    while True:
        valid_move, win, player = env.step()
        if not valid_move:
            print(f"Invalid move from player {player}")
            break

        if win:
            print(f"Player {player} won!")
            break

        display.render(env.obs, env.config)
        display.clock.tick(1)


if __name__ == "__main__":
    main()
