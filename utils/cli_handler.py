from utils.errors import EmptyInputError
from app.logs import logger


class CLIHandler:
    def __init__(self, user_input: str) -> None:
        self.user_input = user_input.strip()
        self.command = None
        self.args = None

    def parse_input(self):
        parts = self.user_input.split()

        if not parts:
            logger.warning("User input is empty.")
            raise EmptyInputError("Input is empty. Input cannot be empty!")

        self.command = parts[0].lower().strip()
        self.args = parts[1:]
        logger.info(f"Parsed user input: command, contact(args).")
