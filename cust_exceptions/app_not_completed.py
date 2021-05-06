
class AppNotCompleted(Exception):

    def __init__(self, message=None, loc=None):
        self.message = message
        self.loc = loc
