import pickle
from pathlib import Path
from typing import Dict, Any
from app.contacts import AddressBook
from app.logs import logger


class FileHandler:
    """
    Handles reading, updating, and writing contact data to a file using pickle.
    """

    def __init__(self, path: Path, data: Dict[str, Any] = None) -> None:
        """
        Initialize a FileHandler object.

        :param path: Path to the file for storing contacts.
        :type path: Path
        :param data: Initial dictionary of contact data (optional).
        :type data: Dict[str, Any], optional
        """

        self.path = path
        self.data = data

    def read_file(self) -> Dict[str, Any]:
        """
        Read contact data from the file.

        If the file exists and contains data, loads it using pickle.
        Otherwise, initializes an empty dictionary.

        :return: Dictionary containing the contact data.
        :rtype: Dict[str, Any]
        """

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
        """
        Update the internal data dictionary with new contacts from an AddressBook.

        :param address_book: AddressBook object containing contacts to update.
        :type address_book: AddressBook
        """
        self.data.update(address_book.data)
        logger.info(f"Updated local dictionary with new data (contacts).")

    def write_in_file(self) -> None:
        """
        Write the internal data dictionary to the file using pickle.
        """
        with self.path.open("wb") as file:
            pickle.dump(self.data, file)
            logger.info(f"Wrote data to file: {self.path}")
