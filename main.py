from app.logs import logger
from pathlib import Path
from utils.validate.validate_path import ValidatePath
from utils.file_handler import FileHandler
import sys
from utils.contact_factory import contact_factory
from app.contacts import AddressBook
from utils.command_handler import CommandHandler
from utils.errors import (
    InsufficientArgumentsError,
    MissingRequiredArgumentError,
    EmptyInputError,
    InvalidCommandError,
    InvalidArgumentError,
    ContactNotFoundError,
)


def main(string_path: str = None) -> None:
    PROJECT_PATH = Path(__file__).resolve().parent

    if string_path is None:
        directory_path = PROJECT_PATH / Path(r"app/contacts/contacts.bin")
        logger.warning(
            f'No file path was provided by the user. Using default path: "{directory_path.parent}".'
        )
        print()
        path = ValidatePath(directory_path)
    else:
        logger.info(
            f'File path entered by user for saving the address book: "{string_path}".'
        )
        path = ValidatePath(string_path + r"/contacts.bin")

    # Validate path (create if missing)
    valid_path = path.validate_path()

    # Read file (create empty dict if missing)
    file_handler = FileHandler(valid_path)
    contacts_with_file = file_handler.read_file()

    # Initialize an AddressBook and populate it with contacts from the file
    address_book = AddressBook()
    address_book.data = contacts_with_file
    logger.info(
        'Created a new AddressBook object and initialized its "data" field with the loaded data.'
    )

    try:
        if len(sys.argv) > 1:
            # Get user input and parse it
            # Create a Contact object from the parsed input data
            user_input = " ".join(sys.argv[1:])
            logger.info(
                "The program was launched via the command line, and the arguments were provided by the user as command-line arguments."
            )
            command, contact = contact_factory(user_input)

            # Initialize a CommandHandler object and execute the action corresponding to the user's input command
            handler = CommandHandler(address_book)
            handler.handle_command(command, contact)
        else:
            while True:
                try:
                    # Get user input and parse it
                    # Create a Contact object from the parsed input data
                    user_input = input("Enter command or command with contact data: ")
                    command, contact = contact_factory(user_input)
                except (
                    EmptyInputError,
                    InvalidCommandError,
                    InvalidArgumentError,
                    ContactNotFoundError,
                ) as error_message:
                    print(f"{error_message}\n")
                    continue

                try:
                    # Initialize a CommandHandler object and execute the action corresponding to the user's input command
                    handler = CommandHandler(address_book)
                    continue_value = handler.handle_command(command, contact)

                    # Exit from the program
                    if not continue_value:
                        break

                except (
                    InsufficientArgumentsError,
                    MissingRequiredArgumentError,
                    ContactNotFoundError,
                    InvalidArgumentError,
                ) as error_message:
                    print(f"{error_message}\n")
                    continue

    finally:
        # Save the changes made to the current contact list to the file
        file_handler.update_contacts(address_book)
        file_handler.write_in_file()


if __name__ == "__main__":
    logger.info("Program started")
    # Absolute path to the directory for storing the address book file
    str_path = None  # r"./address-book/"
    main(str_path)
