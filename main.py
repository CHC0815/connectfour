from connect_four.ConnectFour import ConnectFour  # type:ignore

from agents.random_bot import bot as random_bot


def main():
    agent1 = random_bot

    env = ConnectFour(agent1, agent1)

    while True:
        valid_move, win, player = env.step()
        if not valid_move:
            print(f"Invalid move from player {player}")
            break

        if win:
            print(f"Player {player} won!")
            break


if __name__ == "__main__":
    main()
