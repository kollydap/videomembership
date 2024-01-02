from cassandra.cqlengine.models import Model
from cassandra.cqlengine import columns
import uuid
from . import utils


class User(Model):
    __keyspace__ = "video_membership_app"
    email = columns.Text(primary_key=True)
    user_id = columns.UUID(primary_key=True, default=uuid.uuid1)
    password = columns.Text()

    def __str__(self) -> str:
        return self.__repr__()

    def __repr__(self):
        return f"User(email={self.email},user_id={self.user_id})"

    def set_password(self, password_str: str, commit=False):
        hashed_password = utils.generate_hash(password_str=password_str)
        self.password = hashed_password
        if commit:
            self.save()
        return True

    def verify_password(self, password_str: str):
        hashed_password = self.password
        verified, _ = utils.verify_hashed_password(
            hashed_password=hashed_password, raw_password_str=password_str
        )
        return verified

    @staticmethod
    def create_user(email, password=None):
        q = User.objects.filter(email=email)
        if q.count() != 0:
            raise Exception("User already has an account!")
        valid, msg, email = utils._validate_email(email=email)
        if not valid:
            raise Exception(f"invalid email:{msg}")
        obj = User(email=email)
        obj.set_password(password)
        obj.save()
        return obj
