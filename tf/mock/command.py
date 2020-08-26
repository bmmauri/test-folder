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
        return "START" if self.get_command() is None else f"START - {self.get_command()}"


class Stop(Command):
    """Start command object"""

    def __init__(self, command: str = None) -> None:
        super().__init__(command=command)

    def __str__(self):
        return "STOP" if self.get_command() is None else f"STOP - {self.get_command()}"


class Pause(Command):
    """Start command object"""

    def __init__(self, command: str = None) -> None:
        super().__init__(command=command)

    def __str__(self):
        return "PAUSE" if self.get_command() is None else f"PAUSE - {self.get_command()}"


class Abort(Command):
    """Start command object"""

    def __init__(self, command: str = None) -> None:
        super().__init__(command=command)

    def __str__(self):
        return "ABORT" if self.get_command() is None else f"ABORT - {self.get_command()}"

