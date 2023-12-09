import random

from connectfour.utils import get_valid_moves  # type:ignore


def bot(obs, config, piece):
    return random.choice(get_valid_moves(obs, config))