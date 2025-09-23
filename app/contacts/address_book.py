from collections import UserDict
from .contact import Contact
from utils.errors import ContactNotFoundError
from app.logs import logger


class AddressBook(UserDict):
    def add_contact(self, contact: Contact) -> None:
        if contact.fullname in self.data:
            logger.warning(f"Contact {contact.fullname} already exists.")
            raise ValueError(f"Contact {contact.fullname} already exists.")
        self.data[contact.fullname] = contact

    def remove_contact(self, fullname: str) -> None:
        if fullname in self.data:
            del self.data[fullname]
        else:
            logger.warning(f"Contact not found: {fullname}")
            raise ContactNotFoundError(f'Contact "{fullname}" does not exist.')
