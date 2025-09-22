import pickle
from pathlib import Path
from typing import Dict, Any
from app.contacts import AddressBook


class FileHandler:
    def __init__(self, path: Path, data: Dict[str, Any] = None) -> None:
        self.path = path
        self.data = data

    def read_file(self) -> Dict[str, Any]:
        if self.path.exists() and self.path.stat().st_size > 0:
            try:
                with self.path.open("rb") as file:
                    self.data = pickle.load(file)
            except (pickle.UnpicklingError, OSError) as e:
                print(f"Error reading file {self.path}: {e}")
                self.data = {}

        else:
            self.data = {}
        return self.data

    def update_contacts(self, address_book: AddressBook) -> None:
        self.data.update(address_book.data)

    def write_in_file(self) -> None:
        with self.path.open("wb") as file:
            pickle.dump(self.data, file)
