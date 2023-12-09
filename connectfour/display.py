import pygame  # type:ignore


class PygameDisplay:
    def __init__(self):
        pygame.init()
        self.screen = pygame.display.set_mode((1280, 720))
        self.clock = pygame.time.Clock()
        self.running = True

    def render(self, board, config):
        board = board.reshape(config.rows, config.columns)
        self.screen.fill((0, 0, 0))
        for row in range(config.rows):
            for col in range(config.cols):
                if board[row][col] == 1:
                    pygame.draw.circle(
                        self.screen, (255, 0, 0), (col * 100 + 50, row * 100 + 50), 40
                    )
                elif board[row][col] == 2:
                    pygame.draw.circle(
                        self.screen, (0, 255, 0), (col * 100 + 50, row * 100 + 50), 40
                    )
        pygame.display.flip()
        self.clock.tick(60)
