import argparse

import connectfour.utils as utils
from connectfour.Simulation import Simulation


def main():
    built_in_agents = ["random", "onestep", "nstep"]

    parser = argparse.ArgumentParser()
    parser.add_argument("-n", "--n-games", type=int, default=10, help="Number of games to play")
    parser.add_argument(
        "-a1",
        "--agent1",
        type=str,
        default="random",
        help="Agent 1. Built-in agents: {}".format(built_in_agents)
        + ". Custom agents: path to agent file",
    )
    parser.add_argument(
        "-a2",
        "--agent2",
        type=str,
        default="random",
        help="Agent 2. Built-in agents: {}".format(built_in_agents)
        + ". Custom agents: path to agent file",
    )

    parser.add_argument("--train", help="Train the agent", type=bool, default=False)
    args = parser.parse_args()
    if args.train:
        import agents.drl as drl

        drl.train_bot()
        return

    agent1 = utils.get_agent(args.agent1)
    agent2 = utils.get_agent(args.agent2)

    sim = Simulation(agent1, agent2, args.n_games)
    sim.run()
    sim.print_results()


if __name__ == "__main__":
    main()
