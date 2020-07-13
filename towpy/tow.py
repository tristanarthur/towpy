import pygame
from sys import exit
from typing import Tuple, NoReturn
from .textobject import TextObject


Size = Tuple[int, int]
Colour = Tuple[int, int, int]


class TextOnlyWindow:
    def __init__(
        self,
        size: Size = (64, 32),
        caption: str = "TOW.PY",
        size_is_cells: bool = True,
        font_size: int = 15,
    ):
        if not pygame.get_init():
            pygame.init()
        if not pygame.font.get_init():
            pygame.font.init()
        self.running = True

        self.font = pygame.font.SysFont("monospace", font_size)

        if size_is_cells:
            size = (size[0] * self.font.size(" ")[0], size[1] * self.font.size(" ")[1])

        self.surface = pygame.display.set_mode(size)
        pygame.display.set_caption(caption)

        self.clock = pygame.time.Clock()
        self.run_time = 0
        self.target_FPS = 30
        self.dt = 0

        self.background_colour = (0, 0, 0)
        self.text_objects = []

    def update(self) -> NoReturn:
        """Update window and handle any events. Also push events to TextObjects."""
        self.dt = self.clock.tick(self.target_FPS)
        self.run_time += self.dt

        events = pygame.event.get()
        for event in events:
            if event.type == pygame.QUIT:
                self.running = False

        for text_object in self.text_objects:
            text_object.update(self.dt)
            text_object.handle_events(events)

    def render(self) -> NoReturn:
        """Clear surface, Render TextObjects, Update window"""
        self.surface.fill(self.background_colour)

        for text_object in self.text_objects:
            if not text_object.hidden:
                text_object.render(self.surface, self.font)

        pygame.display.update()

    def run(self) -> NoReturn:
        """Puts TOW into a update and render loop"""
        while self.running:
            self.update()
            self.render()
        self.quit()

    def quit(self) -> NoReturn:
        """Uninitialises pygame library if needed."""
        if pygame.get_init():
            pygame.quit()

    def add_object(self, text_object: TextObject) -> NoReturn:
        """Adds a new TextObject to the window.

        Arguments:
        text_object -- The TextObject to add to window.
        """
        self.text_objects.append(text_object)

    def set_background_colour(self, colour: Tuple) -> NoReturn:
        """Sets the background colour of the window.

        Arguments:
        colour -- (R, G, B) colour format for background.
        """
        if type(colour) is tuple and len(colour) == 3:
            self.background_colour = colour
        else:
            raise TypeError("Incorrect background colour format!")


if __name__ == "__main__":
    tow = TextOnlyWindow()
    tow.set_background_colour((100, 100, 100))

    a = TextObject([" __ ", "|__|"], (50, 50))
    tow.add_object(a)

    b = TextObject("Hello\nMy\nName\nTree", (200, 200))
    tow.add_object(b)

    c = TextObject(
        [[" ", None, " "], [" ", " ", " "]],
        (100, 100),
        colour=(255, 120, 120),
        background=(0, 0, 0),
    )
    c.set_background_at((1, 1), (120, 255, 120))
    tow.add_object(c)

    tow.run()
