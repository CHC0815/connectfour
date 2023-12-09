from agents.random_bot import bot as random_bot
from connectfour.ConnectFour import ConnectFour
from connectfour.display import PygameDisplay


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
        display.clock.tick(10)

    while True:
        display.clock.tick(10)


if __name__ == "__main__":
    main()
