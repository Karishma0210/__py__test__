from classes.user import User

class TestCreateUser:
    def test_user_with_valid_args(self):
        user_json = {
            "name": "TestName",
            "surname": "TestSurname",
            "email": "test.email@domain.com",
            "age": 10
        }
        
        user = User.from_json(user_json)
        output = user.create_user()
        #if you receive non null and non zero value then success
        assert output
        
    def test_user_with_invalid_email(self):
        user_json = {
            "name": "TestName",
            "surname": "TestSurname",
            "email": "jj.ss",
            "age": 10
        }
        
        user = User.from_json(user_json)
        output = user.create_user()
        #you receive None for invalid user
        assert output == None
    
    def test_user_with_invalid_age(self):
        user_json = {
            "name": "TestName",
            "surname": "TestSurname",
            "email": "jj.ss@gmail.com",
            "age": "wrong_type"
        }
        
        user = User.from_json(user_json)
        output = user.create_user()
        #you receive None for invalid user
        assert output == None

