import numpy as np
import pygame  # type:ignore


class PygameDisplay:
    def __init__(self):
        pygame.init()
        self.screen = pygame.display.set_mode((480, 480))
        self.clock = pygame.time.Clock()
        self.running = True

    def render(self, obs, config):
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
