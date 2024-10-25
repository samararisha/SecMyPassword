# SecMyPass

## Description
SecMyPass is a password validation tool that checks the strength of passwords against a series of criteria, including length, complexity, and known breaches. The tool provides feedback on password strength and guides users in creating secure passwords.

## Features
- Checks for password length (minimum of 8 characters, maximum of 64 characters).
- Ensures passwords contain at least one lowercase letter, one uppercase letter, one digit, and one special character.
- Validates against common passwords using the "Have I Been Pwned?" API.
- Provides feedback on password strength.

## Requirements
To run SecMyPass, you need the following Python libraries:
- `re`: (Part of the standard library, no installation needed)
- `hashlib`: (Part of the standard library, no installation needed)
- `requests`: For making HTTP requests to the "Have I Been Pwned?" API.
- `colorama`: For color formatting in the terminal.

### Installation
You can install the required libraries using pip. Open your terminal and run the following commands:

```bash
pip install requests colorama
