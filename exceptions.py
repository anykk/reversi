class GameOverException(Exception):
    """Game over exception."""
    pass


class MoveError(Exception):
    """Move error. It throws when player have some troubles with move."""
    def __init__(self, message):
        super().__init__()
        self.message = message

    def __str__(self):
        return f"MoveError: {self.message}."


class IllegalArgumentError(Exception):
    """It throws when some arguments are illegal."""
    def __init__(self, message):
        super().__init__()
        self.message = message

    def __str__(self):
        return f"IllegalArgumentError: {self.message}."


class SaveError(Exception):
    """It throws when player has some troubles with save."""
    def __init__(self, message):
        super().__init__()
        self.message = message

    def __str__(self):
        return f"SaveError: {self.message}."


class LoadError(Exception):
    """It throws when player has some troubles with load."""
    def __init__(self, message):
        super().__init__()
        self.message = message

    def __str__(self):
        return f"LoadError: {self.message}."


class NoMovesException(Exception):
    """It throws when next player can't move."""
    pass
