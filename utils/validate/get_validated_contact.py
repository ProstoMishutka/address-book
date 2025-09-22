from utils.cli_handler import CLIHandler
from .validate_data import ValidateData
from app.contacts import Contact
from typing import Optional, Tuple


def get_validated_contact(user_input: str) -> Tuple[Optional[str], Contact]:
    cli = CLIHandler(user_input)
    cli.parse_input()

    validate = ValidateData(cli.command, cli.args)

    command = validate.command if validate.command else None
    first_name = validate.first_name if validate.first_name else None
    last_name = validate.last_name if validate.last_name else None
    phone = validate.phone if validate.phone else None
    email = validate.email if validate.email else None

    contact = Contact(
        first_name=first_name, last_name=last_name, phone=phone, email=email
    )

    return command, contact
