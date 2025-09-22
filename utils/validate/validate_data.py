import re


class InvalidCommandError(Exception):
    """Raised when a non-existent command is entered"""

    def __init__(self, message: str) -> None:
        self.message = message
        super().__init__(self.message)


class InvalidArgumentError(Exception):
    """Raised when invalid arguments are entered"""

    def __init__(self, message: str) -> None:
        self.message = message
        super().__init__(self.message)


class ValidateData:
    ALLOWED_COMMANDS = [
        "exit",
        "quit",
        "q",
        "close",
        "add",
        "phone",
        "email",
        "change",
        "change_fullname",
        "change_phone",
        "change_email",
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

        for item in self.args:
            if re.match(self.NAME_PATTERN, item):
                parts_name.append(item.strip().capitalize())
                continue

            if re.match(self.PHONE_PATTERN, item):
                self.phone = item.strip()
                continue

            if re.match(self.EMAIL_PATTERN, item):
                self.email = item.strip()
                continue

            raise InvalidArgumentError(f"Invalid argument detected: '{item}'")

        if len(parts_name) >= 1:
            self.first_name = parts_name[0]

        if len(parts_name) >= 2:
            self.last_name = parts_name[1]

    @staticmethod
    def validate_command(command: str) -> str:
        if command not in ValidateData.ALLOWED_COMMANDS:
            raise InvalidCommandError(f'Entered command does not exist: "{command}".')
        else:
            return command
