from app.models import Users
import pytest

# Bu yazdigimizi functional testler sayilir,cunki kodun funksionalligin yoxlayir
# integration testler ise muxtelif appler arasinda testleri yoxlayir


def test_user_class(new_user):
    user, user_info = new_user

    for key, val in user_info.items():
        res = getattr(user, key)

        assert res == val


def test_user_class_with_invalid_data():
    user_info = {
        "test": "testvalue",
        "name": "Tural",
        "surname": "Muradov",
        "email": "test@mail.ru",
        "password": "12345"
    }

    with pytest.raises(TypeError):
        user = Users(**user_info)

    # for key, val in user_info.items():
    #     res = getattr(user, key)

    #     assert res == val


def test_update_user_class(new_user):
    user, user_info = new_user

    user_info["name"] = "Test"
    user.name = "Test"

    for key, val in user_info.items():
        res = getattr(user, key)

        assert res == val


def test_class_save_db(new_user, init_db):
    user, _ = new_user
    init_db.session.add(user)
    init_db.session.commit()

    user_in_db = init_db.session.query(Users).get(1)
    assert user_in_db.name == user.name

    user_info = {
        "name": "Rafiq",
        "surname": "Alimaerdenov",
        "email": "test1@mail.ru",
        "password": "12345"
    }

    user = Users(**user_info)
    user.save_db()
    user_in_db = init_db.session.query(Users).get(2)
    assert user_in_db.name == user.name
    assert user_in_db.created is not None

    new_user = Users(**user_info)
    assert new_user.save_db() is False

    user_info = {
        "name": None,
        "surname": "Alimaerdenov",
        "email": "test1@mail.ru",
        "password": "12345"
    }

    user = Users(**user_info)
    assert user.save_db() is False


def test_update_db(new_user, init_db):
    user, _ = new_user
    user.save_db()

    user = init_db.session.query(Users).get(1)

    user.update_db(name="Amir")

    assert user.name == "Amir"

    user = init_db.session.query(Users).get(1)
    assert user.name == "Amir"

    # user.update_db(name="")  # FIXME  bosh string gelende qebul edir

    # assert user.name == ""

    # user = init_db.session.query(Users).get(1)
    # assert user.name == "Amir"
