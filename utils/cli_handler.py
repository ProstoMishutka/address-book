class EmptyInputError(Exception):
    def __init__(self, message: str) -> None:
        self.message = message
        super().__init__(self.message)


class CLIHandler:
    def __init__(self, user_input: str) -> None:
        self.user_input = user_input.strip()
        self.command = None
        self.args = None

    def parse_input(self):
        parts = self.user_input.split()

        if not parts:
            raise EmptyInputError("Input is empty. Input cannot be empty!")

        self.command = parts[0].lower().strip()
        self.args = parts[1:]
