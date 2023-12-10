import numpy as np
import pygame  # type:ignore

from connectfour.ConnectFourConfig import ConnectFourConfig
from connectfour.Observation import Observation


class PygameDisplay:
    def __init__(self):
        pygame.init()
        self.screen = pygame.display.set_mode((480, 480))
        self.clock = pygame.time.Clock()
        self.running = True

    def render(self, obs: Observation, config: ConnectFourConfig):
        board = np.asarray(obs.board).reshape(config.rows, config.columns)
        self.screen.fill((0, 0, 0))
        for row in range(config.rows):
            for col in range(config.columns):
                if board[row][col] == 1:
                    pygame.draw.circle(self.screen, (255, 0, 0), (col * 66 + 33, row * 66 + 33), 26)
                elif board[row][col] == 2:
                    pygame.draw.circle(self.screen, (0, 255, 0), (col * 66 + 33, row * 66 + 33), 26)
        pygame.display.flip()

    def draw_victory(self, obs, config):
        board = np.asarray(obs.board).reshape(config.rows, config.columns)


class ConsoleFrame:
    def __init__(self, board):
        self.frame = ""
        for i in range(6):
            for j in range(7):
                mark = "o" if self.board[i * 7 + j] == 1 else "x"
                self.frame += mark + " "
            self.frame += "\n"

    def __str__(self) -> str:
        return self.frame

    def __repr__(self) -> str:
        return self.frame


class ConsoleDisplay:
    def __init__(self):
        self.steps: list[ConsoleFrame] = []

    def render(self, obs: Observation, config: ConnectFourConfig):
        self.steps.append(obs.board)

    def __str__(self) -> str:
        s = ""
        for step in self.steps:
            s += "-----------------\n"
            s += str(step) + "\n"
        return str(self.steps)
