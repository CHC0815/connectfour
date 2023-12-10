import connectfour.utils as utils
from agents.nstep import bot as nstep_bot
from agents.onestep import bot as onestep_bot
from agents.random_bot import bot as random_bot
from connectfour.Simulation import Simulation


def main(n_games: int):
    agent1 = random_bot
    agent2 = nstep_bot

    sim = Simulation(agent1, agent2, n_games)
    sim.run()
    sim.print_results()


if __name__ == "__main__":
    main(240)
