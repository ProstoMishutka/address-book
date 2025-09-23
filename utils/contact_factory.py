from utils.cli_handler import CLIHandler
from utils.validate.validate_data import ValidateData
from app.contacts import Contact
from typing import Optional, Tuple


def contact_factory(user_input: str) -> Tuple[Optional[str], Contact]:
    # Parsing the user input into a command and its arguments.
    cli = CLIHandler(user_input)
    cli.parse_input()

    # Validation of user input
    validate = ValidateData(cli.command, cli.args)

    # Extract validated command and contact details (first name, last name, phone, email) into separate variables.
    command = validate.command if validate.command else None
    first_name = validate.first_name if validate.first_name else None
    last_name = validate.last_name if validate.last_name else None
    phone = validate.phone if validate.phone else None
    email = validate.email if validate.email else None

    # Create a Contact object and pass the validated arguments to it.
    contact = Contact(
        first_name=first_name, last_name=last_name, phone=phone, email=email
    )

    return command, contact
