# 📒 Address Book CLI Application <a name="top"></a>

A **command-line interface (CLI)** address book application built with Python.  
It allows users to **add, search, edit, and delete contacts**, while securely storing data in a binary file (`contacts.bin`).  

This project demonstrates:
- Clean architecture and modular design.
- Exception handling with custom error classes.
- File storage using Python's `pickle` module.
- Interactive and command-line usage.

---

## Contents
- [Features](#features)
- [Project Structure](#project-structure)
- [Requirements](#requirements)
- [Installation & Running](#installation--running)
- [Command Examples](#command-examples)
- [Example Of Saved File](#example-of-saved-file)
- [Error Handling](#error-handling)
- [Example Usage](#example-usage)
- [Modularity](#modularity)
- [License](#license)
- [Author](#author)

---

<h2 id="features">🚀 Features</h2>

- **Add a new contact** with a first name, last name, phone, and/or email.
- **Search contacts** by name to retrieve phone numbers or email addresses.
- **Edit contact information** (change phone number or email).
- **View all saved contacts** in a formatted display.
- **Delete contacts** by name.
- **Persistent storage** using a binary file (`contacts.bin`).
- **Interactive mode** or **single command-line execution**.
- **Validation for input data**:
  - Phone numbers must match: `+<country_code><number>` (e.g., `+123456789012`)
  - Emails must match a standard email format.
  - Names must contain only alphabetic characters, apostrophes, or hyphens.

---

<h2 id="project-structure">🗂️ Project Structure</h2>

```text
📂 assistant-bot/
├── app/
│   ├── contacts/
│   │   ├── contact.py
│   │   ├── address_book.py
│   │   └── contacts.bin       
│   └── logs/
│       ├── logger.py
│       └── app.log            
├── utils/
│   ├── validate/
│   │   ├── validate_path.py
│   │   └── validate_data.py
│   ├── file_handler.py
│   ├── contact_factory.py
│   ├── command_handler.py
│   ├── cli_handler.py
│   └── errors.py
├── main.py                   
└── README.md
```

---

<h2 id="requirements">⚙️ Requirements</h2>

- Python 3.10+
- No external libraries — only Python standard library is used.

---

<h2 id="installation--running">💻 Installation & Running</h2> 

1. Clone the repository:
```bash
git clone https://github.com/ProstoMishutka/address-book.git
cd address-book
```

2. (Optional) Create a virtual environment:
```bash
python -m venv .venv
source .venv/bin/activate   # Linux/Mac
.venv\Scripts\activate.bat  # Windows cmd
.venv\Scripts\Activate.ps1  # Windows PowerShell
```

3. Run the main program:
```bash
python main.py
```

---

<h2 id="command-examples">📝 Command Examples</h2> 

| Command                | Description                     | Example Usage                               |
|------------------------|---------------------------------|---------------------------------------------|
| add                    | Add a new contact               | add Jack Brown +1234567890 jack@example.com |
| phone                  | Show contact's phone number     | phone Jack Brown                            |
| email                  | Show contact's email            | email Jack Brown                            |
| change_phone or c_p    | Change contact's phone number   | change_phone Jack Brown +0987654321         |
| change_email or c_e    | Change contact's email          | change_email Jack Brown newmail@example.com |
| all                    | Display all saved contacts      | all                                         |
| delete or del          | Delete a contact                | delete Jack Brown                           |
| exit, q, close         | Exit the program                | exit                                        |

---

<h2 id="example-of-saved-file">📂 Example of Saved File</h2> 📂 Example of Saved File

Contacts are stored in **pickle** format in the file:
```text
app/contacts/contacts.bin
```
This file is automatically created during the first run of the program.

---

<h2 id="error-handling">⚠️ Error Handling</h2>

The program uses a custom exception system:

| Exception                      | When it occurs                                    |
|--------------------------------|---------------------------------------------------|
| EmptyInputError                | User did not enter anything                       |
| InvalidCommandError            | Entered a non-existent command                    |
| InvalidArgumentError           | Arguments do not match the required pattern       |
| InsufficientArgumentsError     | Too few or too many arguments                     |
| MissingRequiredArgumentError   | A required argument was not provided              |
| ContactNotFoundError           | The specified contact was not found               |

---

<h2 id="example-usage">🧪 Example Usage</h2>

1. Adding a contact
```text
> add Jack Brown +123456789012 jack@example.com
Contact added:
Fullname : Jack Brown
Phone    : +123456789012
Email    : jack@example.com
-----------------------------------
```

2. Changing phone number
```text
> change_phone Jack Brown +0987654321
Changed phone to +0987654321.
```

3. Viewing all contacts
```text
> all
Contacts
-----------------------------------
Fullname : Jack Brown
Phone    : +0987654321
Email    : jack@example.com
-----------------------------------
```

4. Deleting a contact
```text
> delete Jack Brown
Deleted contact: Jack Brown.
```

---

<h2 id="modularity">🧩 Modularity</h2>

The program is divided into logical modules:

- **Contact** — stores information about a contact.
- **AddressBook** — manages the collection of contacts.
- **CommandHandler** — processes user commands.
- **FileHandler** — handles saving data to a file.
- **ValidateData** — validates user input.

--- 


<h2 id="license">🧾 License</h2>

This project is distributed under the **MIT License**.  
You are free to use, modify, and distribute it.

---

<h2 id="author">🤝 Author</h2>

**Misha Patserkovskyi**  
Beginner Python Developer 🚀

[Back to top](#top)
