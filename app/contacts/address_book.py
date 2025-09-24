from collections import UserDict
from .contact import Contact
from utils.errors import ContactNotFoundError
from app.logs import logger


class AddressBook(UserDict):
    """
    The AddressBook class inherits from UserDict and stores the user's contact information.

    Attributes:
        data (dict): A dictionary containing the user's contacts for later saving to a file.

    Methods:
        add_contact(contact): Adds a new contact to the dictionary.
        remove_contact(fullname): Removes a contact by the user's full name
    """

    def add_contact(self, contact: Contact) -> None:
        """
        Add a Contact object to the 'data' dictionary (inherited from UserDict).

        This method checks if a contact with the same full name already exists:
            - If it exists, raises an error indicating the contact already exists.
            - If it does not exist, adds the new contact to the dictionary.

        :param contact: Contact object to be added
        :type contact: Contact
        """
        if contact.fullname in self.data:
            logger.warning(f"Contact {contact.fullname} already exists.")
            raise ValueError(f"Contact {contact.fullname} already exists.")
        self.data[contact.fullname] = contact

    def remove_contact(self, fullname: str) -> None:
        """
        Remove a Contact object from the 'data' dictionary (inherited from UserDict).

        The method checks whether a contact with the specified full name exists:
            - If it exists, the contact is removed from the dictionary.
            - If it does not exist, raises an error indicating that the contact is not found in the address book.

        :param fullname: Full name of the Contact object to remove
        :type fullname: str
        """
        if fullname in self.data:
            del self.data[fullname]
        else:
            logger.warning(f"Contact not found: {fullname}")
            raise ContactNotFoundError(f'Contact "{fullname}" does not exist.')
