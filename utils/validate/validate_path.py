from pathlib import Path
from typing import Optional
from app.logs import logger


class ValidatePath:
    def __init__(self, file_path_str: str | Path = None) -> None:
        self.path = file_path_str

    def validate_path(self) -> None | Optional[Path]:
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
