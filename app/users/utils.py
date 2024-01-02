from email_validator import EmailNotValidError, validate_email
from argon2 import PasswordHasher
from argon2.exceptions import VerifyMismatchError


def _validate_email(email):
    msg = ""
    valid = False
    try:
        valid = validate_email(email)
        email = valid.email
        valid = True
    except EmailNotValidError as e:
        msg = str(e)
    return valid, msg, email


def generate_hash(password_str: str):
    ph = PasswordHasher()
    return ph.hash(password_str)


def verify_hashed_password(hashed_password, raw_password_str) -> bool:
    ph = PasswordHasher()
    verified = False
    msg = ""
    try:
        verified = ph.verify(hashed_password, raw_password_str)
    except VerifyMismatchError:
        verified = False
        msg = "Invalid Password."
    except Exception as e:
        verified = False
        msg = f"Unexpected error: \n{e}"
    return verified, msg
