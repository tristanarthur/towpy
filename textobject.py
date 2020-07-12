class TextAnimation:

    ANIMATION_STYLE = {"NORMAL": 1, "REVERSE": -1}

    def __init__(self):
        self.duration = 0
        self.style = None



class TextObject:

    def __init__(self, text, pos, colour=(255, 255, 255), background=None):
        self.position = list(pos)
        self.default_text = self.__load_text(text, colour, background)
        self.animations = {}
        self.hidden = False
        self.position_gridded = True
        self.event_handlers = []
        self.current_frame = self.default_text

    def update(self, dt):
        # This method should be overrided by child object
        pass

    def handle_events(self, events):
        # This method should be overrided by child object
        pass

    def __load_text(self, text, colour, background):
        formatted_text = []
        if type(text) is str:
            formatted_text = text.split("\n")
        elif type(text) is list:
            formatted_text = text

        rich_text = []
        for i, line in enumerate(formatted_text):
            rich_text.append([])
            for char in line:
                rich_text[i].append([char, colour, background])

        return rich_text

    def render(self, surface, font):
        x, y = self.position

        # Snap to grid
        if self.position_gridded:
            x = x - (x % font.size(" ")[0])
            y = y - (y % font.size(" ")[1])

        # Must be stored for line restore point
        initial_x = x

        for line in self.current_frame:
            for char, colour, background in line:
                if char is not None:
                    surface.blit(font.render(char, False, colour, background), (x, y))
                x += font.size(" ")[0]
            # Reset x to start of object and move
            # y to next line
            x = initial_x
            y += font.size(" ")[1]

    def set_colour(self, colour):
        pass

    def set_background(self, colour):
        pass

    def set_colour_at(self, pos, colour):
        if (type(colour) is tuple and
            len(colour) == 3 and
            type(pos) is tuple and
            len(pos) == 2):
            self.default_text[pos[0]][pos[1]][1] = colour
        else:
            raise ValueError("Incorrect colour or position format!")

    def set_background_at(self, pos, colour):
        if (type(colour) is tuple and
            len(colour) == 3 and
            type(pos) is tuple and
            len(pos) == 2):
            self.default_text[pos[0]][pos[1]][2] = colour
        else:
            raise ValueError("Incorrect colour or position format!")

    @staticmethod
    def load_from_file(self, file, pos):
        with open(file) as f:
            return TextObject(f.read(), pos)
