from typing import Tuple, Generic, List, NoReturn, final
import config
from pygame import *


Position = Tuple[int, int]
Size = Tuple[int, int]
Colour = Tuple[int, int, int]
RichText = List[Tuple[Position, Colour, Colour]]


class TextObject:
    def __init__(
        self,
        text: Generic,
        pos: Position,
        colour: Colour = (255, 255, 255),
        background: Colour = None,
    ):
        self.position = list(pos)
        self.set_sprite(text, colour, background)
        self.hidden = False
        self.position_gridded = True
        self.components = []
        self.size = self.get_size()

    def update(self, dt: int) -> NoReturn:
        """Update TextObject. This method is expected to be overrided.

        Arguments:
        dt -- Difference in ms between current and last frame.
        """
        pass

    def handle_components(self, dt):
        for component in self.components:
            component.update(dt)

    @final
    def set_sprite(self, text, colour=(255, 255, 255), background=None):
        self.default_text = self.__load_text(text, colour, background)

    @final
    def __load_text(
        self, text: Generic, colour: Colour, background: Colour,
    ) -> RichText:
        """Loads inputted text into expected format for a text object.
        Expected format:
        [[[Position, Foreground Colour, Background Colour], [...], [...]]]
        List 1st dimension represents the entire string,
             2nd dimension represents a line of text,
             3rd dimension represents character attributes

        Arguments:
        text -- Some text format, e.g. string or list of chars to be converted.
        colour -- (R, G, B) colour format for font.
        background -- (R, G, B) colour format for background.
        """
        formatted_text = text
        # If string we need to break into list of lines
        if type(text) is str:
            formatted_text = text.split("\n")

        # Turns list into correctly formated RichText
        rich_text = []
        for i, line in enumerate(formatted_text):
            rich_text.append([])
            for char in line:
                rich_text[i].append([char, colour, background])

        return rich_text

    @final
    def render(self, surface: "pygame.Surface") -> NoReturn:
        """Render TextObject onto a pygame Surface. Due to the enforced
        limitations of this library every object uses the same font and font
        size. However, choice of colour is allowed. This is why a decision
        was made to pass font in as an argument rather than having each
        text object have its own font variable.

        TODO:
        * Have the TextObject pre render itself once and simply blit to correct
        position at render time.

        Arguments:
        surface -- A pygame surface object.
        font -- A pygame font object.
        """
        x, y = self.position

        # Snap to grid
        if self.position_gridded:
            x = x - (x % config.font.size(" ")[0])
            y = y - (y % config.font.size(" ")[1])

        # Must be stored for line restore point
        initial_x = x

        for line in self.default_text:
            for char, colour, background in line:
                if char is not None:
                    surface.blit(
                        config.font.render(char, False, colour, background), (x, y)
                    )
                x += config.font.size(" ")[0]
            # Reset x to start of object and move
            # y to next line
            x = initial_x
            y += config.font.size(" ")[1]

    @final
    def get_size(self) -> Size:
        """Function is not intended to be used outside of class. If you want
        to get dimensions use the class var. This funtion is used to recalculate
        size of object when sprite is changed only.
        """
        width = 0
        height = len(self.default_text) * config.font.size(" ")[1]
        for line in self.default_text:
            width = max(width, len(line))
        return (width * config.font.size(" ")[0], height)

    @final
    def set_colour(self, colour: Colour) -> NoReturn:
        """NOT IMPLEMENTED. Set the colour of entire TextObject

        Arguments:
        colour -- (R, G, B) colour format for font.
        """
        pass

    @final
    def set_background(self, colour: Colour) -> NoReturn:
        """NOT IMPLEMENTED. Set the background colour of entire TextObject.

        Arguments:
        colour -- (R, G, B) colour format for font.
        """
        pass

    @final
    def set_colour_at(self, pos: Position, colour: Colour) -> NoReturn:
        """Set the font colour of a character in the TextObject.

        Arguments:
        pos -- Relative coordinate of character to change colour of.
        colour -- (R, G, B) colour format for font.
        """
        if (
            type(colour) is tuple
            and len(colour) == 3
            and type(pos) is tuple
            and len(pos) == 2
        ):
            self.default_text[pos[0]][pos[1]][1] = colour
        else:
            raise ValueError("Incorrect colour or position format!")

    @final
    def set_background_at(self, pos: Position, colour: Colour) -> NoReturn:
        """Set the background colour of a character in the TextObject.

        Arguments:
        pos -- Relative coordinate of character to change colour of.
        colour -- (R, G, B) colour format for font.
        """
        if (
            type(colour) is tuple
            and len(colour) == 3
            and type(pos) is tuple
            and len(pos) == 2
        ):
            self.default_text[pos[0]][pos[1]][2] = colour
        else:
            raise ValueError("Incorrect colour or position format!")

    @final
    def load_from_file(
        self, file: str, colour: Colour, background: Colour
    ) -> "TextObject":
        """Loads a TextObject from a file. Basic way of storing complex sprites.

        Arguments:
        file -- Location of file to load from.
        pos -- Coordinate to initially place TextObject.
        """
        with open(file) as f:
            self.default_text = self.__load_text(f.read(), colour, background)

    def add_component(self, component):
        component.root = self
        self.components.append(component)
        self.__dict__[type(component).__name__.lower()] = component
