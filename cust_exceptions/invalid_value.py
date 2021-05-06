
class InvalidValue(Exception):

    def __init__(self, message, loc=None):
        self.message = message
        self.loc = loc
