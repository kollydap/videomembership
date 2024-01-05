from email_validator import EmailNotValidError, validate_email
from argon2 import PasswordHasher
from argon2.exceptions import VerifyMismatchError
import json, jwt
from pydantic import BaseModel, error_wrappers, ValidationError

from app.core.config import Settings

AUTH_PRIVATE_KEY = None
AUTH_PUBLIC_KEY = None
AUTH_ALGO = "RS256"
ACCESS_TOKEN_VALIDITY_SECONDS = 24 * 60 * 60  # 24 hours
REFRESH_TOKEN_VALIDITY_SECONDS = 7 * 24 * 60 * 60  # 7 days
EMAIL_TOKEN_EXPIRE_IN_SECONDS = 10 * 60  # seconds


def valid_schema_data_or_error(raw_data: dict, SchemaModel: BaseModel):
    data = {}
    errors = []
    error_str = ""

    try:
        # insted we validate incoming data against our PYDANTIC Signup model
        cleaned_data = SchemaModel(**raw_data)

        data = cleaned_data.dict()
    except error_wrappers.ValidationError as e:
        error_str = e.json()
    if error_str is not None:
        try:
            errors = json.loads(error_str)
        except Exception as e:
            errors = [{"loc": "non field error", "msg": "unknown error"}]
    return data, errors


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


def encode_jwt_data(data: dict):
    global AUTH_PRIVATE_KEY
    if not AUTH_PRIVATE_KEY:
        auth_settings = Settings()
        AUTH_PRIVATE_KEY = auth_settings.auth_private_key
    return jwt.encode(payload=data, key=AUTH_PRIVATE_KEY, algorithm=AUTH_ALGO)


def decode_jwt_data(encoded: str):
    global AUTH_PUBLIC_KEY
    if not AUTH_PUBLIC_KEY:
        auth_settings = Settings()
        AUTH_PUBLIC_KEY = auth_settings.auth_public_key
    return jwt.decode(jwt=encoded, key=AUTH_PUBLIC_KEY, algorithms=[AUTH_ALGO])


# change to uuid
def generate_access_token(user_uid: int):
    return encode_jwt_data(data={"user_uid": user_uid})
