class Command:
    """Generic command object"""

    __command = None

    def __init__(self, command) -> None:
        super().__init__()
        self.__command = command

    def get_command(self):
        return self.__command


class Start(Command):
    """Start command object"""

    def __init__(self, command: str = None) -> None:
        super().__init__(command=command)

    def __str__(self):
        return "START"


class Pause(Command):
    """Pause command object"""

    def __init__(self, command: str = None) -> None:
        super().__init__(command=command)

    def __str__(self):
        return "PAUSE"


class Abort(Command):
    """Abort command object"""

    def __init__(self, command: str = None) -> None:
        super().__init__(command=command)

    def __str__(self):
        return "ABORT"
