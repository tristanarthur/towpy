import pygame
from sys import exit
from textobject import TextObject


# TODO: Have font rendering being stored in text object instead of doing
#       it on every render frame <---- DO THIS
#       Will be useful as well because testing for collisions including mouse
#       collisions will be difficult with the current split


class TextOnlyWindow:

    def __init__(self):
        if not pygame.get_init():
            pygame.init()
        if not pygame.font.get_init():
            pygame.font.init()
        self.running = True

        self.surface = pygame.display.set_mode((500, 500))
        pygame.display.set_caption("TOW.PY")

        self.clock = pygame.time.Clock()
        self.run_time = 0
        self.target_FPS = 15
        self.dt = 0

        self.font = pygame.font.SysFont("monospace", 15)

        self.background_colour = (0, 0, 0)
        self.text_objects = []

    def __update(self):
        self.dt = self.clock.tick(self.target_FPS)
        self.run_time += self.dt

        events = pygame.event.get()
        for event in events:
            if event.type == pygame.QUIT:
                self.running = False

        for text_object in self.text_objects:
            text_object.update(self.dt)
            text_object.handle_events(events)

    def __render(self):
        self.surface.fill(self.background_colour)

        for text_object in self.text_objects:
            if not text_object.hidden:
                self.__render_object(text_object)

        pygame.display.update()

    def run(self):
        while self.running:
            self.__update()
            self.__render()
        self.quit()

    def quit(self):
        print("Goodbye!")
        if pygame.get_init():
            pygame.quit()

    def add_object(self, text_object):
        self.text_objects.append(text_object)

    def __render_object(self, text_object):
        x, y = text_object.position

        # Snap to grid
        if text_object.position_gridded:
            x = x - (x % self.font.size(" ")[0])
            y = y - (y % self.font.size(" ")[1])

        # Must be stored for line restore point
        initial_x = x

        for line in text_object.get_current_frame():
            for char in line:
                if char is not None:
                    self.surface.blit(self.font.render(char, False, (255, 255, 255)), (x, y))
                x += self.font.size(" ")[0]
            # Reset x to start of object and move
            # y to next line
            x = initial_x
            y += self.font.size(" ")[1]


    def set_background_colour(self, colour):
        if type(colour) is tuple and len(colour) == 3:
            self.background_colour = colour
        else:
            raise TypeError("Incorrect background colour format!")


if __name__ == "__main__":
    tow = TextOnlyWindow()
    tow.set_background_colour((100, 100, 100))

    a = TextObject([[" __ "],
                    ["|__|"]],
                    (50, 50))
    tow.add_object(a)

    b = TextObject("Hello\nMy\nName\nTree", (200, 200))
    tow.add_object(b)

    c = TextObject([["I", None, "I"],
                    ["I", "_", "I"]],
                    (100, 100))
    tow.add_object(c)

    tow.run()
