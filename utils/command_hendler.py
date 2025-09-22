from app.contacts import Contact, AddressBook
import re


class InsufficientArgumentsError(Exception):
    """Raised when not enough or too many arguments are provided for a command."""

    def __init__(self, message) -> None:
        self.message = message
        super().__init__(self.message)


class MissingRequiredArgumentError(Exception):
    """Raised when a required argument is not provided."""

    def __init__(self, message) -> None:
        self.message = message
        super().__init__(self.message)


class CommandHandler:
    PHONE_PATTERN = r"^\+\d{1,3}\d{6,12}$"
    EMAIL_PATTERN = r"^[\w\.-]+@[\w\.-]+\.[\w\.-]+$"

    def __init__(self, address_book: AddressBook) -> None:
        self.address_book = address_book

    @staticmethod
    def count_args(contact: Contact = None) -> int:
        if contact is None:
            return 0

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
        return bool(re.match(CommandHandler.PHONE_PATTERN, phone))

    @staticmethod
    def check_email(email) -> bool:
        return bool(re.match(CommandHandler.EMAIL_PATTERN, email))

    def handle_command(self, command: str, contact: Contact = None) -> bool | None:
        # Check count args
        fields_filled = self.count_args(contact)

        if command in ["exit", "quit", "q", "close"]:
            print("Goodbye")
            return False

        elif command == "add" and contact:
            if not 1 < fields_filled < 5:
                raise InsufficientArgumentsError(
                    f"{fields_filled} arguments entered (need 2–4 arguments besides the command)."
                )

            if contact.phone is None and contact.email is None:
                raise MissingRequiredArgumentError(
                    "Required argument not provided: phone or email.\n"
                )

            self.address_book.add_contact(contact)
            print(f"Contact added:\n{contact}")

        elif command == "phone" and contact:
            if fields_filled != 1:
                raise InsufficientArgumentsError(
                    f"{fields_filled} arguments entered (need 1 arguments besides the command)."
                )

            for person in self.address_book.data.values():
                if person.fullname == contact.fullname:
                    print(f"Phone number - {person.phone}.\n")

        elif command == "email" and contact:
            if fields_filled != 1:
                raise InsufficientArgumentsError(
                    f"{fields_filled} arguments entered (need 1 arguments besides the command)."
                )

            for person in self.address_book.data.values():
                if person.fullname == contact.fullname:
                    print(f"Person email - {person.email}.\n")

        elif command == "change_phone" and contact:
            if fields_filled != 2:
                raise InsufficientArgumentsError(
                    f"{fields_filled} arguments entered (need 2 arguments besides the command)."
                )
            if not self.check_phone(contact.phone):
                raise MissingRequiredArgumentError(
                    "Required argument not provided: phone.\n"
                )

            for person in self.address_book.data.values():
                if person.fullname == contact.fullname:
                    person.phone = contact.phone
                    print(f"Changed phone on {person.phone}.\n")

        elif command == "change_email" and contact:
            if fields_filled != 2:
                raise InsufficientArgumentsError(
                    f"{fields_filled} arguments entered (need 2 arguments besides the command)."
                )

            if not self.check_email(contact.email):
                raise MissingRequiredArgumentError(
                    "Required argument not provided: email.\n"
                )

            for person in self.address_book.data.values():
                if person.fullname == contact.fullname:
                    person.email = contact.email
                    print(f"Email changed on {person.email}.\n")

        elif command == "all":
            if fields_filled != 0:
                raise InsufficientArgumentsError(
                    f"{fields_filled} arguments entered (need 0 arguments besides the command)."
                )

            if not len(self.address_book.data.values()) > 0:
                print("Address book is empty.\n")
                return True

            for person in self.address_book.data.values():
                print(person)

        elif command in ["delete", "del"]:
            if not 0 < fields_filled < 2:
                raise InsufficientArgumentsError(
                    f"Invalid number of arguments: {fields_filled} entered (need 1 arguments besides the command)."
                )
            self.address_book.remove_contact(contact.fullname)
            print(f"Deleted contact: {contact.fullname}.\n")

        else:
            print("Invalid command!")
        return True
