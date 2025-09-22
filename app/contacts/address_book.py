from collections import UserDict
from .contact import Contact


class ContactNotFoundError(Exception):
    """Raised when the entered name does not match any existing contact."""

    def __init__(self, message):
        self.message = message
        super().__init__(self.message)


class AddressBook(UserDict):
    def add_contact(self, contact: Contact) -> None:
        if contact.fullname in self.data:
            raise ValueError("Contact already exists")
        self.data[contact.fullname] = contact

    def remove_contact(self, fullname: str) -> None:
        if fullname in self.data:
            del self.data[fullname]
        else:
            raise ContactNotFoundError(f'Contact "{fullname}" does not exist.')
