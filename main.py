import argparse

import connectfour.utils as utils
from agents.nstep import bot as nstep_bot
from agents.onestep import bot as onestep_bot
from agents.random_bot import bot as random_bot
from connectfour.Simulation import Simulation


def get_agent(name):
    if name == "random":
        return random_bot
    elif name == "onestep":
        return onestep_bot
    elif name == "nstep":
        return nstep_bot
    else:
        return load_agent(name)


def load_agent(name):
    import os
    from importlib.machinery import SourceFileLoader

    if not os.path.isfile(name):
        raise FileNotFoundError("Agent {} not found".format(name))

    file = SourceFileLoader("agent", name).load_module()
    return file.bot


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
    args = parser.parse_args()

    agent1 = get_agent(args.agent1)
    agent2 = get_agent(args.agent2)

    sim = Simulation(agent1, agent2, args.n_games)
    sim.run()
    sim.print_results()


if __name__ == "__main__":
    main()
