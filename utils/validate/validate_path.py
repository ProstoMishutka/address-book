from pathlib import Path
from typing import Optional
from app.logs import logger


class ValidatePath:
    """
    Validates a file path and ensures its parent directory exists.

    If the directory does not exist, it will be created automatically.
    """

    def __init__(self, file_path_str: str | Path = None) -> None:
        """
        Initializes a ValidatePath object with the given file path.

        :param file_path_str: The file path to validate.
        :type file_path_str: str | Path, optional
        """

        self.path = file_path_str

    def validate_path(self) -> None | Optional[Path]:
        """
        Validates the file path and ensures its parent directory exists.

        Attempts to convert the stored path to a Path object. If the parent
        directory does not exist, it will be created.

        :returns: The validated Path object or None if an error occurred.
        :rtype: Path | None
        """

        try:
            self.path = Path(self.path)
        except OSError as e:
            logger.warning(f"Error resolving path: {e}")
            return None

        # If the directory does not exist — create it
        if not self.path.parent.exists():
            logger.warning(f"Directory does not exist: {self.path.parent}.")
            print()
            self.path.parent.mkdir(parents=True, exist_ok=True)
            logger.info(f"Directory created: {self.path.parent}.")
            print(f'Path directory - "{self.path.parent}" created')
        else:
            logger.info(f"The directory at path {self.path.parent} already exists.")

        return self.path
