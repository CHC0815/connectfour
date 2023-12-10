import argparse

import connectfour.utils as utils
from agents.nstep import bot as nstep_bot
from agents.onestep import bot as onestep_bot
from agents.random_bot import bot as random_bot
from connectfour.Simulation import Simulation


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("-n", "--n-games", type=int, default=10, help="Number of games to play")
    args = parser.parse_args()

    agent1 = random_bot
    agent2 = onestep_bot

    sim = Simulation(agent1, agent2, args.n_games)
    sim.run()
    sim.print_results()


if __name__ == "__main__":
    main()
