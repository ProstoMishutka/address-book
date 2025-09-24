from typing import Optional


class Contact:
    """
    Class representing a person's contact information.

    Attributes:
        first_name (str | None): The person's first name.
        last_name (str | None): The person's last name.
        phone (str | None): The person's phone number.
        email (str | None): The person's email address.

    Properties:
        fullname (str | None): Combines first_name and last_name into a full name.

    Methods:
        __str__(): Returns a user-friendly string representation of the contact.
        __repr__(): Returns a developer-friendly string representation of the contact.
    """

    def __init__(
        self,
        first_name: Optional[str],
        last_name: Optional[str],
        phone: Optional[str],
        email: Optional[str],
    ) -> None:

        self.first_name = first_name
        self.last_name = last_name
        self.phone = phone
        self.email = email

    @property
    def fullname(self) -> Optional[str]:
        """
        Property that generates the 'fullname' of a Contact object.

        Checks the object's fields:
            - If both first_name and last_name are present, returns fullname as "first_name last_name".
            - If only first_name is present, returns fullname containing just the first_name.
        """
        if self.first_name and self.last_name:
            return f"{self.first_name} {self.last_name}"

        return self.first_name

    def __str__(self) -> str:
        """
        Magic method __str__ that returns a user-friendly string representation of a Contact object.

        If any field of the Contact object is None, it is displayed as '-' in the output.
        """
        if self.fullname and self.phone and self.email:
            return (
                f"Fullname : {self.fullname}\n"
                f"Phone    : {self.phone}\n"
                f"Email    : {self.email}\n"
                f"{'-' * 35}"
            )

        elif self.fullname and self.phone is None and self.email:
            return (
                f"Fullname : {self.fullname}\n"
                f"Phone    : -\n"
                f"Email    : {self.email}\n"
                f"{'-' * 35}"
            )

        elif self.fullname and self.phone and self.email is None:
            return (
                f"Fullname : {self.fullname}\n"
                f"Phone    : {self.phone}\n"
                f"Email    : -\n"
                f"{'-' * 35}"
            )

        else:
            return f"No contact information found for the name {self.fullname}.\n"

    def __repr__(self) -> str:
        """
        Return a technical string representation of the Contact object suitable for debugging.

        The format is: Contact(first_name, last_name, phone, email)
        with each field shown using repr() to make the values explicit, including None.

        Returns:
            str: Technical representation of the Contact object.
        """
        return f"Contact({self.first_name!r}, {self.last_name!r}, {self.phone!r}, {self.email!r})"
