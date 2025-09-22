from utils.validate.validate_path import ValidatePath
from utils.file_handler import FileHandler
import sys
from utils.validate.get_validated_contact import get_validated_contact
from app.contacts import AddressBook, ContactNotFoundError
from utils.cli_handler import EmptyInputError
from utils.validate.validate_data import InvalidCommandError, InvalidArgumentError
from utils.command_hendler import (
    CommandHandler,
    InsufficientArgumentsError,
    MissingRequiredArgumentError,
)


def main(string_path: str) -> None:
    # Validate path (create if missing)
    path = ValidatePath(string_path)
    valid_path = path.validate_path()

    # Read file (create empty dict if missing)
    file_handler = FileHandler(valid_path)
    contacts_with_file = file_handler.read_file()

    # Initialize an AddressBook and populate it with contacts from the file
    address_book = AddressBook()
    address_book.data = contacts_with_file

    try:
        if len(sys.argv) > 1:
            # Get user input and parse it
            # Create a Contact object from the parsed input data
            user_input = " ".join(sys.argv[1:])
            command, contact = get_validated_contact(user_input)

            # Initialize a CommandHandler object and execute the action corresponding to the user's input command
            handler = CommandHandler(address_book)
            handler.handle_command(command, contact)
        else:
            while True:
                try:
                    # Get user input and parse it
                    # Create a Contact object from the parsed input data
                    user_input = input("Enter command or command with contact data: ")
                    command, contact = get_validated_contact(user_input)
                except (
                    EmptyInputError,
                    InvalidCommandError,
                    InvalidArgumentError,
                ) as error_message:
                    print(f"{error_message}\n")
                    continue

                try:
                    # Initialize a CommandHandler object and execute the action corresponding to the user's input command
                    handler = CommandHandler(address_book)
                    handler.handle_command(command, contact)
                except (
                    InsufficientArgumentsError,
                    MissingRequiredArgumentError,
                    ContactNotFoundError,
                ) as error_message:
                    print(f"{error_message}\n")
                    continue

                while True:
                    continue_program = (
                        input("Do you want to continue? [yes/no]: ").strip().lower()
                    )
                    print()
                    if continue_program not in ["yes", "no", "y", "n"]:
                        print(f'"{continue_program}" is not a valid option.\n')
                        continue
                    break

                if continue_program not in ["yes", "y"]:
                    print("Program finished.")
                    break

    finally:
        # Save the changes made to the current contact list to the file
        file_handler.update_contacts(address_book)
        file_handler.write_in_file()


if __name__ == "__main__":
    str_path = r"D:/assistant-bot/app/contacts/contacts.bin"
    main(str_path)
