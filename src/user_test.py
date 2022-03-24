import random
import string
from classes.user import User


class TestCreateUser:
    def test_user_with_valid_args(self):
        user = create_dummy_user()
        assert user

    def test_user_with_invalid_email(self):
        user = create_dummy_user(generate_invalid_email=True)
        assert user == None

    def test_user_with_invalid_age(self):
        user = create_dummy_user(generate_invalid_age=True)
        assert user == None

class TestSaveUser:
    def test_save_user_no_file(self):
        user = create_dummy_user()
        user = user.save()
        assert user
    
    def test_save_user_no_file(self):
        user = create_dummy_user()
        user = user.save()
        assert user == None

class TestReadUser:
    def test_read_users_without_filters(self):
        users = User.get_users(pretty_print=False)
        assert type(users) == list
        if len(users) > 1:
            assert type(users[0]) == User


class TestUpdateUser:
    def test_update_user_with_existing_id(self):
        user = create_dummy_user()
        assert user
        user = user.save(pretty_print=False)
        
        to_be_updated_user_json = {
            "name": "NameUpdate",
            "surname": "SurnameUpdate",
            "age": 99
        }
        updated_user = User.update_user(
            user.user_id, update_options=to_be_updated_user_json, pretty_print=False)

        updated_user_json = updated_user.to_json()

        keys = to_be_updated_user_json.keys()
        filtered_updated_user_json = dict(
            (k, updated_user_json[k]) for k in keys if k in to_be_updated_user_json)

        assert to_be_updated_user_json == filtered_updated_user_json


class TestDeleteUser:
    def test_delete_user_valid_id(self):
        user = create_dummy_user()
        user = user.save(pretty_print=False)
        assert user
        
        user_deleted = User.delete_user(user_id=user.user_id, pretty_print=False)
        assert user_deleted

    def test_delete_user_invalid_id(self):
        random_id = lambda: ''.join(
            random.choices(string.ascii_letters + string.digits, k=7))

        user_deleted = User.delete_user(
            user_id=random_id, pretty_print=False)
        assert not user_deleted

def create_dummy_user(generate_invalid_email=False, generate_invalid_age=False):
    random_letters = lambda: ''.join(random.choices(string.ascii_letters + string.digits, k=4))
    random_num = lambda: ''.join(random.choices(string.digits, k=2))
    
    valid_email = "test.email." + random_letters() + "@domain.com"
    invalid_email = random_letters() + "@" + random_letters()
    user_json = {
        "name": "TestName-" + random_letters(),
        "surname": "TestSurname-"+ random_letters(),
        "email": invalid_email if generate_invalid_email else valid_email,
        "age": random_letters() if generate_invalid_age else random_num()
    }

    user = User.from_json(user_json)
    rcved_user = user.create_user(pretty_print=False)
    # if you receive non null and non zero value then success
    return rcved_user
