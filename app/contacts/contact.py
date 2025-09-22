from typing import Optional


class Contact:
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
        if self.first_name and self.last_name:
            return f"{self.first_name} {self.last_name}"

        return self.first_name

    def __str__(self) -> str:
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
        return f"Contact({self.first_name!r}, {self.last_name!r}, {self.phone!r}, {self.email!r})"
