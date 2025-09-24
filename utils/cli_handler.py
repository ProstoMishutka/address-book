from utils.errors import EmptyInputError
from app.logs import logger


class CLIHandler:
    """
    Handles parsing of raw user input into a command and its arguments.

    The class stores the user input string and provides a method to split it
    into a command and a list of arguments.
    """

    def __init__(self, user_input: str) -> None:
        """
        Handles parsing of raw user input into a command and its arguments.

        The class stores the user input string and provides a method to split it
        into a command and a list of arguments.
        """
        self.user_input = user_input.strip()
        self.command = None
        self.args = None

    def parse_input(self):
        """
        Parse the user input string into a command and arguments.

        Splits the input string by spaces, assigns the first part as the command,
        and the remaining parts as arguments. Raises EmptyInputError if the input
        string is empty.
        """
        parts = self.user_input.split()

        if not parts:
            logger.warning("User input is empty.")
            raise EmptyInputError("Input is empty. Input cannot be empty!")

        self.command = parts[0].lower().strip()
        self.args = parts[1:]
        logger.info(f"Parsed user input: command, contact(args).")
