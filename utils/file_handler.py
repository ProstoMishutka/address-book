import pickle
from pathlib import Path
from typing import Dict, Any
from app.contacts import AddressBook
from app.logs import logger


class FileHandler:
    def __init__(self, path: Path, data: Dict[str, Any] = None) -> None:
        self.path = path
        self.data = data

    def read_file(self) -> Dict[str, Any]:
        # If the file exists and contains some data inside.
        if self.path.exists() and self.path.stat().st_size > 0:
            try:
                with self.path.open("rb") as file:
                    self.data = pickle.load(file)
                    logger.debug(f"Loaded file: {self.path}")
            except (pickle.UnpicklingError, OSError) as e:
                logger.warning(f"Error reading file {self.path}: {e}")

                self.data = {}
                logger.info("Created a new empty dictionary for storing contacts.")

        else:
            self.data = {}
            logger.info("Created a new empty dictionary for storing contacts.")
        return self.data

    def update_contacts(self, address_book: AddressBook) -> None:
        self.data.update(address_book.data)
        logger.info(f"Updated local dictionary with new data (contacts).")

    def write_in_file(self) -> None:
        with self.path.open("wb") as file:
            pickle.dump(self.data, file)
            logger.info(f"Wrote data to file: {self.path}")
