import random

import connectfour.utils as utils


def bot(obs, config):
    return random.choice(utils.get_valid_moves(obs, config))
