

class CliException(Exception):

    def __init__(self, message):
        self.message = message

    def message(self):
        return self.message