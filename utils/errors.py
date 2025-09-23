class ErrorBot(Exception):
    """Base class for all custom exceptions in the bot."""

    def __init__(self, message: str) -> None:
        self.message = message
        super().__init__(self.message)


class EmptyInputError(ErrorBot):
    """Raised when the user provides an empty input."""


class InvalidCommandError(ErrorBot):
    """Raised when a non-existent command is entered"""


class InvalidArgumentError(ErrorBot):
    """Raised when invalid arguments are entered"""


class InsufficientArgumentsError(ErrorBot):
    """Raised when not enough or too many arguments are provided for a command."""


class MissingRequiredArgumentError(ErrorBot):
    """Raised when a required argument is not provided."""


class ContactNotFoundError(ErrorBot):
    """Raised when the provided contact name does not exist."""
