import pytest
from app.models import Users
from extensions.extension import db
from server import flask_app


@pytest.fixture  # butun test fayllarinda buna catmaq ucun
def new_user():
    user_info = {
        "name": "Tural",
        "surname": "Muradov",
        "email": "test@mail.ru",
        "password": "12345"
    }

    user = Users(**user_info)
    return user, user_info


@pytest.fixture
def app():
    yield flask_app


@pytest.fixture
def init_db(app):

    db.create_all()

    yield db

    db.close_all_sessions()
    db.drop_all()
