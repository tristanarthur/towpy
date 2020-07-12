class TextAnimation:

    ANIMATION_STYLE = {"NORMAL": 1, "REVERSE": -1}

    def __init__(self):
        self.duration = 0
        self.style = None



class TextObject:

    def __init__(self, text, pos):
        self.position = list(pos)
        self.default_text = self.__load_text(text)
        self.animations = {}
        self.hidden = False
        self.position_gridded = True
        self.event_handlers = []

    def update(self, dt):
        # This method should be overrided by child object
        pass

    def handle_events(self, events):
        # This method should be overrided by child object
        pass

    def __load_text(self, text):
        formatted_text = []
        if type(text) is str:
            formatted_text = text.split("\n")
        elif type(text) is list:
            formatted_text = text
        return formatted_text

    @staticmethod
    def load_from_file(self, file, pos):
        with open(file) as f:
            return TextObject(f.read(), pos)

    def get_current_frame(self):
        return self.default_text
