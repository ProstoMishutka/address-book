from pathlib import Path
from typing import Optional


class ValidatePath:
    def __init__(self, file_path_str: str) -> None:
        self.path = file_path_str

    def validate_path(self) -> Optional[Path]:
        try:
            file_path = Path(self.path).resolve()
        except OSError as e:
            print(f"Error resolving path: {e}")
            return None

        if not file_path.parent.exists():
            file_path.parent.mkdir(parents=True, exist_ok=True)
            print(f'Path - "{file_path}" created')

        self.path = file_path
        return self.path
