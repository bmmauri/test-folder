class Command:
    """Generic command object"""
    pass


class Start(Command):
    """Start command object"""

    def __init__(self) -> None:
        super().__init__()

    def __str__(self):
        return "START"

