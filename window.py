import pygame
from sys import exit


class TextOnlyWindow:

    def __init__(self):
        if not pygame.get_init():
            pygame.init()
        self.running = True

        self.surface = pygame.display.set_mode((500, 500))
        pygame.display.set_caption("TOW.PY")

        self.clock = pygame.time.Clock()
        self.run_time = 0
        self.target_FPS = 15
        self.dt = 0

    def update(self):
        self.dt = self.clock.tick(self.target_FPS)
        self.run_time += self.dt

    def render(self):
        pygame.display.update()

    def run(self):
        while self.running:
            self.update()
            self.render()
        self.quit()

    def quit(self):
        if pygame.get_init():
            pygame.quit()


if __name__ == "__main__":
    TextOnlyWindow().run()
