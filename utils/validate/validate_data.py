import re
from utils.errors import InvalidCommandError, InvalidArgumentError
from app.logs import logger


class ValidateData:
    ALLOWED_COMMANDS = [
        "exit",
        "q",
        "close",
        "add",
        "phone",
        "email",
        "change_phone",
        "c_p",
        "change_email",
        "c_e",
        "all",
        "delete",
        "del",
    ]

    NAME_PATTERN = r"^[A-Za-z'-]+$"
    PHONE_PATTERN = r"^\+\d{1,3}\d{6,12}$"
    EMAIL_PATTERN = r"^[\w\.-]+@[\w\.-]+\.[\w\.-]+$"

    def __init__(self, command: str, args: list) -> None:
        self.command = self.validate_command(command)
        self.args = args
        self.first_name = None
        self.last_name = None
        self.phone = None
        self.email = None

        self.parse_args()

    def parse_args(self) -> None:
        parts_name = []

        # Parse the command arguments and classify them into first name, last name, phone, or email.
        # If an argument does not match any expected pattern, raise an InvalidArgumentError.
        # Assign first_name and last_name based on the order of name parts detected.
        for item in self.args:
            if re.match(self.NAME_PATTERN, item):
                parts_name.append(item.strip().capitalize())
                logger.debug(f"Detected name part: {item.strip().capitalize()}")
                continue

            if re.match(self.PHONE_PATTERN, item):
                self.phone = item.strip()
                logger.debug(f"Detected phone: {self.phone}")
                continue

            if re.match(self.EMAIL_PATTERN, item):
                self.email = item.strip()
                logger.debug(f"Detected email: {self.email}")
                continue

            logger.warning(f"Invalid argument detected: '{item}'")
            raise InvalidArgumentError(f"Invalid argument detected: '{item}'")

        # Determine first_name and last_name based on the parts_name list
        if len(parts_name) >= 1:
            self.first_name = parts_name[0]
            logger.debug(f"Set first_name: {self.first_name}")

        if len(parts_name) >= 2:
            self.last_name = parts_name[1]
            logger.debug(f"Set last_name: {self.last_name}")

    @staticmethod
    def validate_command(command: str) -> str:
        if command not in ValidateData.ALLOWED_COMMANDS:
            logger.warning(f"Invalid command detected: '{command}'")
            raise InvalidCommandError(f'Entered command does not exist: "{command}".')
        else:
            logger.info(f"Valid command detected: {command}.")
            return command
