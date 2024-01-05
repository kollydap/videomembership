from .models import User
import datetime
import app.users.utils as user_utils


def authenticate(email, password):
    try:
        user_obj = User.objects.get(email=email)
    except Exception as e:
        user_obj = None
    if not user_obj.verify_password(password_str=password):
        return None
    return user_obj


def login(user_obj, expires=5):
    raw_data = {
        "user_id": f"{user_obj.id}",
        "role": "admin",
        "exp": datetime.datetime.utcnow() + datetime.timedelta(seconds=expires),
    }
    return user_utils.encode_jwt_data(data=raw_data)
    # return jwt.encode(payload=raw_data, key=AUTH_PRIVATE_KEY, algorithm=AUTH_ALGO)


def verify_userid(token):
    data = {}
    try:
        data = user_utils.decode_jwt_data(encoded=token)
    except Exception as e:
        print(e)
    if "user_id" not in data:
        return None
    return data
