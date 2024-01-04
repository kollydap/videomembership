from .models import User
import datetime, jwt

AUTH_PRIVATE_KEY = None
AUTH_PUBLIC_KEY = None
AUTH_ALGO = "RS256"
ACCESS_TOKEN_VALIDITY_SECONDS = 24 * 60 * 60  # 24 hours
REFRESH_TOKEN_VALIDITY_SECONDS = 7 * 24 * 60 * 60  # 7 days
EMAIL_TOKEN_EXPIRE_IN_SECONDS = 10 * 60  # seconds

def authenticate(email, password):
    try:
        user_obj = User.objects.get(email=email)
    except Exception as e:
        user_obj = None
    if not user_obj.verify_password(password_str = password):
        return None
    return user_obj

def login(user_obj, expires = 5):
    raw_data={
        "user_id":f"{user_obj.id}",
        "role":"admin",
        "exp":datetime.datetime.utcnow() + datetime.timedelta(seconds=expires)
    }
    return jwt.emcode()

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
def generate_access_token(user_uid:int):
    return encode_jwt_data(data={"user_uid": user_uid})
