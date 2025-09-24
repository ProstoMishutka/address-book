import re
from app.contacts import Contact, AddressBook
from utils.errors import (
    InsufficientArgumentsError,
    ContactNotFoundError,
    MissingRequiredArgumentError,
    InvalidArgumentError,
)
from app.logs import logger


class CommandHandler:
    """
    A class to handle commands for managing an address book.
    Provides methods for adding, retrieving, modifying, and deleting contacts.
    """

    PHONE_PATTERN = r"^\+\d{1,3}\d{6,12}$"
    EMAIL_PATTERN = r"^[\w\.-]+@[\w\.-]+\.[\w\.-]+$"

    def __init__(self, address_book: AddressBook) -> None:
        """
        Initialize CommandHandler with a given address book.

        :param address_book: The address book instance to work with.
        :type address_book: AddressBook
        """
        self.address_book = address_book

    @staticmethod
    def count_args(contact: Contact = None) -> int:
        """
        Count non-empty fields of the provided Contact object.

        :param contact: Contact instance to evaluate.
        :type contact: Contact, optional
        :return: The count of non-empty fields.
        :rtype: int
        """
        if contact is None:
            return 0

        # Count the non-empty fields of the Contact object.
        return sum(
            1
            for value in [
                contact.first_name,
                contact.last_name,
                contact.phone,
                contact.email,
            ]
            if value not in (None, "-")
        )

    def _find_contact(self, contact: Contact) -> Contact:
        """
        Find a contact in the address book by full name.

        :param contact: Contact instance with the full name to search for.
        :type contact: Contact
        :return: The matching contact.
        :rtype: Contact
        :raises ContactNotFoundError: If the contact does not exist.
        """
        for person in self.address_book.data.values():
            if person.fullname == contact.fullname:
                return person
        else:
            logger.warning(f'Contact "{contact.fullname}" does not exist.')
            raise ContactNotFoundError(f'Contact "{contact.fullname}" does not exist.')

    @staticmethod
    def check_phone(phone) -> bool:
        """
        Validate a phone number format using a regex pattern.

        :param phone: The phone number to validate.
        :type phone: str
        :return: True if the phone number is valid, False otherwise.
        :rtype: bool
        """
        return bool(re.match(CommandHandler.PHONE_PATTERN, phone))

    @staticmethod
    def check_email(email) -> bool:
        """
        Validate an email format using a regex pattern.

        :param email: The email address to validate.
        :type email: str
        :return: True if the email is valid, False otherwise.
        :rtype: bool
        """
        return bool(re.match(CommandHandler.EMAIL_PATTERN, email))

    def handle_exit(self):
        """
        Handle the exit command, stopping the program.

        :return: Always returns False to signal termination.
        :rtype: bool
        """
        print("Program finished.")
        logger.info("Program finished.")
        return False

    def handle_add(self, contact: Contact, fields_filled: int) -> None:
        """
        Add a new contact to the address book.

        :param contact: The contact to add.
        :type contact: Contact
        :param fields_filled: The number of non-empty fields provided.
        :type fields_filled: int
        :raises InsufficientArgumentsError: If the number of fields is invalid.
        :raises MissingRequiredArgumentError: If phone and email are missing.
        """
        if not 2 <= fields_filled <= 4:
            logger.warning(
                f"{fields_filled} arguments entered (need 2–4 arguments besides the command)."
            )
            raise InsufficientArgumentsError(
                f"{fields_filled} arguments entered (need 2–4 arguments besides the command)."
            )

        if contact.phone is None and contact.email is None:
            logger.warning("Required argument not provided: phone or email.")
            raise MissingRequiredArgumentError(
                "Required argument not provided: phone or email."
            )

        # Add contact to the address book and log the action
        self.address_book.add_contact(contact)
        logger.debug(f"Contact added: {repr(contact)}")
        print(f"Contact added:\n{contact}")

    def handle_phone(self, contact: Contact, fields_filled: int) -> None:
        """
        Retrieve the phone number of a contact.

        :param contact: The contact to search for.
        :type contact: Contact
        :param fields_filled: The number of non-empty fields provided.
        :type fields_filled: int
        :raises InsufficientArgumentsError: If the number of fields is invalid.
        :raises ContactNotFoundError: If the contact does not exist.
        """
        if not 1 <= fields_filled <= 2:
            logger.warning(
                f"{fields_filled} arguments entered (need 1-2 arguments besides the command)."
            )
            raise InsufficientArgumentsError(
                f"{fields_filled} arguments entered (need 1-2 arguments besides the command)."
            )

        person = self._find_contact(contact)
        logger.debug(f"Person phone: {person.phone}.")
        print(f"Person phone: {person.phone}.\n")
        return True

    def handle_email(self, contact: Contact, fields_filled: int) -> None:
        """
        Retrieve the email address of a contact.

        :param contact: The contact to search for.
        :type contact: Contact
        :param fields_filled: The number of non-empty fields provided.
        :type fields_filled: int
        :raises InsufficientArgumentsError: If the number of fields is invalid.
        :raises ContactNotFoundError: If the contact does not exist.
        """
        if not 1 <= fields_filled <= 2:
            logger.warning(
                f"{fields_filled} arguments entered (need 1-2 arguments besides the command)."
            )
            raise InsufficientArgumentsError(
                f"{fields_filled} arguments entered (need 1-2 arguments besides the command)."
            )

        person = self._find_contact(contact)
        logger.debug(f"Person email: {person.email}.")
        print(f"Person email: {person.email}.\n")
        return True

    def handle_change_phone(self, contact: Contact, fields_filled: int) -> None:
        """
        Change the phone number of an existing contact.

        :param contact: The contact whose phone will be changed.
        :type contact: Contact
        :param fields_filled: The number of non-empty fields provided.
        :type fields_filled: int
        :raises InsufficientArgumentsError: If the number of fields is invalid.
        :raises MissingRequiredArgumentError: If the phone field is missing.
        :raises InvalidArgumentError: If the phone number format is invalid.
        :raises ContactNotFoundError: If the contact does not exist.
        """
        if not 2 <= fields_filled <= 3:
            logger.warning(
                f"{fields_filled} arguments entered (need 2-3 arguments besides the command)."
            )
            raise InsufficientArgumentsError(
                f"{fields_filled} arguments entered (need 2-3 arguments besides the command)."
            )

        if contact.phone is None:
            logger.warning("Required argument not provided: phone.")
            raise MissingRequiredArgumentError("Required argument not provided: phone.")

        if not self.check_phone(contact.phone):
            logger.warning("Incorrect value entered.")
            raise InvalidArgumentError("Incorrect value entered.")

        person = self._find_contact(contact)
        person.phone = contact.phone
        logger.debug(f"{person.fullname} changed phone on {person.phone}.")
        print(f"Changed phone on {person.phone}.\n")
        return True

    def handle_change_email(self, contact: Contact, fields_filled: int) -> None:
        """
        Change the email address of an existing contact.

        :param contact: The contact whose email will be changed.
        :type contact: Contact
        :param fields_filled: The number of non-empty fields provided.
        :type fields_filled: int
        :raises InsufficientArgumentsError: If the number of fields is invalid.
        :raises MissingRequiredArgumentError: If the email field is missing.
        :raises InvalidArgumentError: If the email format is invalid.
        :raises ContactNotFoundError: If the contact does not exist.
        """
        if not 2 <= fields_filled <= 3:
            logger.warning(
                f"{fields_filled} arguments entered (need 2-3 arguments besides the command)."
            )
            raise InsufficientArgumentsError(
                f"{fields_filled} arguments entered (need 2-3 arguments besides the command)."
            )

        if contact.email is None:
            logger.warning("Required argument not provided: email.")
            raise MissingRequiredArgumentError("Required argument not provided: email.")

        if not self.check_email(contact.email):
            logger.warning("Incorrect value entered.")
            raise InvalidArgumentError("Incorrect value entered.")

        person = self._find_contact(contact)
        person.email = contact.email
        logger.debug(f"Email changed on {person.email}.")
        print(f"Email changed on {person.email}.\n")
        return True

    def handle_all(self, fields_filled: int) -> None:
        """
        Display all contacts in the address book, sorted by full name.

        :param fields_filled: Number of non-empty fields provided.
        :type fields_filled: int
        :raises InsufficientArgumentsError: If extra arguments are provided.

        The method prints all contacts in ascending order by full name.
        If the address book is empty, a message indicating this is displayed.
        """
        if fields_filled != 0:
            logger.warning(
                f"{fields_filled} arguments entered (need 0 arguments besides the command)."
            )
            raise InsufficientArgumentsError(
                f"{fields_filled} arguments entered (need 0 arguments besides the command)."
            )

        if not len(self.address_book.data.values()) > 0:
            logger.warning("Address book is empty.")
            print("Address book is empty.\n")
            return True

        # Print all contacts
        print("\nContacs \n" f"{'-' * 35}")
        for person in sorted(self.address_book.data.values(), key=lambda p: p.fullname):
            print(person)

    def handle_delete(self, contact: Contact, fields_filled: int) -> None:
        """
        Delete a contact from the address book.

        :param contact: The contact to delete.
        :type contact: Contact
        :param fields_filled: Number of non-empty fields provided.
        :type fields_filled: int
        :raises InsufficientArgumentsError: If invalid number of fields is provided.
        """
        if not 0 < fields_filled <= 2:
            logger.warning(
                f"Invalid number of arguments: {fields_filled} entered (need 1 arguments besides the command)."
            )
            raise InsufficientArgumentsError(
                f"Invalid number of arguments: {fields_filled} entered (need 1 arguments besides the command)."
            )

        # Remove contact from the address book and log the action
        self.address_book.remove_contact(contact.fullname)
        logger.debug(f"Contact {contact.fullname} deleted.")
        print(f"Deleted contact: {contact.fullname}.\n")

    def handle_command(self, command: str, contact: Contact = None) -> bool | None:
        """
        Handle a user command by routing it to the appropriate handler.

        :param command: The command to execute.
        :type command: str
        :param contact: Optional contact for commands that require it.
        :type contact: Contact, optional
        :return: False if the program should exit, True otherwise.
        :rtype: bool | None
        """

        # Count the number of non-empty fields in the contact
        fields_filled = self.count_args(contact)

        # Exit commands
        if command in ["exit", "quit", "q", "close"]:
            return self.handle_exit()

        # Add a new contact
        elif command == "add" and contact:
            self.handle_add(contact, fields_filled)

        # Retrieve phone of a contact
        elif command == "phone" and contact:
            self.handle_phone(contact, fields_filled)

        # Retrieve email of a contact
        elif command == "email" and contact:
            self.handle_email(contact, fields_filled)

        # Change phone of a contact
        elif command in ["change_phone", "c_p"] and contact:
            self.handle_change_phone(contact, fields_filled)

        # Change email of a contact
        elif command in ["change_email", "c_e"] and contact:
            self.handle_change_email(contact, fields_filled)

        # Show all contacts
        elif command == "all":
            self.handle_all(fields_filled)

        # Deleted a contact
        elif command in ["delete", "del"]:
            self.handle_delete(contact, fields_filled)

        else:
            logger.warning("Invalid command.")
            print("Invalid command!")
        return True
