from typing import Tuple, Generic, List, NoReturn, final
from pygame import *


Position = Tuple[int, int]
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
        self.default_text = self.__load_text(text, colour, background)
        self.hidden = False
        self.position_gridded = True
        self.dimensions = [0, 0]

    def update(self, dt: int) -> NoReturn:
        """Update TextObject. This method is expected to be overrided.
 
        Arguments:
        dt -- Difference in ms between current and last frame.
        """
        pass

    def handle_events(self, events: "pygame.event.EventList") -> NoReturn:
        """Handle incoming pygame events. This method is expected to
        be overrided.

        Arguments:
        events -- A PyGame EventList with all events from queue of this frame.
        """
        pass

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
    def render(self, surface: "pygame.Surface", font: "pygame.font.Font",) -> NoReturn:
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
            x = x - (x % font.size(" ")[0])
            y = y - (y % font.size(" ")[1])

        # Must be stored for line restore point
        initial_x = x

        max_width = 0
        for line in self.default_text:
            for char, colour, background in line:
                max_width = max(max_width, len(line))
                if char is not None:
                    surface.blit(font.render(char, False, colour, background), (x, y))
                x += font.size(" ")[0]
            # Reset x to start of object and move
            # y to next line
            x = initial_x
            y += font.size(" ")[1]
        self.dimensions[0] = max_width * font.size("_")[0]
        self.dimensions[1] = len(self.default_text) * font.size(" ")[1]

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

    def point_collision(self, point_pos: Position) -> bool:
        if (
            self.position[0] <= point_pos[0]
            and self.position[1] <= point_pos[1]
            and self.position[0] + self.dimensions[0] >= point_pos[0]
            and self.position[1] + self.dimensions[1] >= point_pos[1]
        ):
            return True
        return False

    def other_collision(self, other: "TextObject") -> bool:
        if (
            self.position[0] <= other.position[0] + other.dimensions[0]
            and self.position[0] + self.dimensions[0] >= other.position[0]
            and self.position[1] <= other.position[1] + other.dimensions[1]
            and self.position[1] + self.dimensions[1] >= other.position[1]
        ):
            print("Collide!")
            return True
        return False
