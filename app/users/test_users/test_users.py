import pytest, db
from users.models import User

@pytest.fixture(scope='module')
def setup():
    session = db.get_session()
    yield session
    q = User.objects.filter(email='test@test.com')
    if q.count() != 0:
        q.delete()
    session.shutdown()
    
def test_create_user():
    User.create_user(email="test@test.com", password="abc123")
    