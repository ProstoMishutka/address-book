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
    PHONE_PATTERN = r"^\+\d{1,3}\d{6,12}$"
    EMAIL_PATTERN = r"^[\w\.-]+@[\w\.-]+\.[\w\.-]+$"

    def __init__(self, address_book: AddressBook) -> None:
        self.address_book = address_book

    @staticmethod
    def count_args(contact: Contact = None) -> int:
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

    @staticmethod
    def check_phone(phone) -> bool:
        # Validate email format using regex
        return bool(re.match(CommandHandler.PHONE_PATTERN, phone))

    @staticmethod
    def check_email(email) -> bool:
        # Validate email format using regex
        return bool(re.match(CommandHandler.EMAIL_PATTERN, email))

    def handle_command(self, command: str, contact: Contact = None) -> bool | None:
        # Count the number of non-empty fields in the contact
        fields_filled = self.count_args(contact)

        # Exit commands
        if command in ["exit", "quit", "q", "close"]:
            print("Program finished.")
            logger.info("Program finished.")
            return False

        # Add a new contact
        elif command == "add" and contact:
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

        # Retrieve phone of a contact
        elif command == "phone" and contact:
            if not 1 <= fields_filled <= 2:
                logger.warning(
                    f"{fields_filled} arguments entered (need 1-2 arguments besides the command)."
                )
                raise InsufficientArgumentsError(
                    f"{fields_filled} arguments entered (need 1-2 arguments besides the command)."
                )

            for person in self.address_book.data.values():
                if person.fullname == contact.fullname:
                    logger.debug(f"Person phone - {person.phone}.")
                    print(f"Person phone - {person.phone}.\n")
                    return True
            else:
                logger.warning(f'Contact "{contact.fullname}" does not exist.')
                raise ContactNotFoundError(
                    f'Contact "{contact.fullname}" does not exist.'
                )

        # Retrieve email of a contact
        elif command == "email" and contact:
            if not 1 <= fields_filled <= 2:
                logger.warning(
                    f"{fields_filled} arguments entered (need 1-2 arguments besides the command)."
                )
                raise InsufficientArgumentsError(
                    f"{fields_filled} arguments entered (need 1-2 arguments besides the command)."
                )

            for person in self.address_book.data.values():
                if person.fullname == contact.fullname:
                    logger.debug(f"Person email - {person.email}.")
                    print(f"Person email - {person.email}.\n")
                    return True
            else:
                logger.warning(f'Contact "{contact.fullname}" does not exist.')
                raise ContactNotFoundError(
                    f'Contact "{contact.fullname}" does not exist.'
                )

        # Change phone of a contact
        elif command in ["change_phone", "c_p"] and contact:
            if not 2 <= fields_filled <= 3:
                logger.warning(
                    f"{fields_filled} arguments entered (need 2-3 arguments besides the command)."
                )
                raise InsufficientArgumentsError(
                    f"{fields_filled} arguments entered (need 2-3 arguments besides the command)."
                )

            if contact.phone:
                if not self.check_phone(contact.phone):
                    logger.warning("Required argument not provided: phone.")
                    raise MissingRequiredArgumentError(
                        "Required argument not provided: phone."
                    )
            logger.warning("Incorrect value entered.")
            raise InvalidArgumentError("Incorrect value entered.")

            for person in self.address_book.data.values():
                if person.fullname == contact.fullname:
                    person.phone = contact.phone
                    logger.debug(f"{person.fullname} changed phone on {person.phone}.")
                    print(f"Changed phone on {person.phone}.\n")
                    return True
            else:
                logger.warning(f'Contact "{contact.fullname}" does not exist.')
                raise ContactNotFoundError(
                    f'Contact "{contact.fullname}" does not exist.'
                )

        # Change email of a contact
        elif command in ["change_email", "c_e"] and contact:
            if not 2 <= fields_filled <= 3:
                logger.warning(
                    f"{fields_filled} arguments entered (need 2-3 arguments besides the command)."
                )
                raise InsufficientArgumentsError(
                    f"{fields_filled} arguments entered (need 2-3 arguments besides the command)."
                )
            if contact.email:
                if not self.check_email(contact.email):
                    logger.warning("Required argument not provided: email.")
                    raise MissingRequiredArgumentError(
                        "Required argument not provided: email."
                    )
            logger.warning("Incorrect value entered.")
            raise InvalidArgumentError("Incorrect value entered.")

            for person in self.address_book.data.values():
                if person.fullname == contact.fullname:
                    person.email = contact.email
                    logger.debug(f"Email changed on {person.email}.")
                    print(f"Email changed on {person.email}.\n")
                    return True
            else:
                logger.warning(f'Contact "{contact.fullname}" does not exist.')
                raise ContactNotFoundError(
                    f'Contact "{contact.fullname}" does not exist.'
                )

        # Show all contacts
        elif command == "all":
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
            for person in self.address_book.data.values():
                print(person)

        # Deleted a contact
        elif command in ["delete", "del"]:
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

        else:
            logger.warning("Invalid command.")
            print("Invalid command!")
        return True
