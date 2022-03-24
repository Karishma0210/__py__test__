import json
import re
import pandas as pd

from helpers import get_attributes, is_attribute


class User:
    name = None
    surname = None
    age = None
    email = None
    user_id = None

    def __init__(self, name=None, surname=None, age=None, email=None, user_id=None):
        self.name = name
        self.surname = surname
        self.age = age
        self.email = email
        self.user_id = user_id

    def create_user(self, pretty_print=True):
        '''
        creates user and returns the created user's ID
        returns None for failure
        '''
        try:
            # get user_id
            users = User.get_users(pretty_print=False)
            last_user_id = users[-1].user_id if users else "VIA0000"
            user_id = "{}{:0>4.0f}".format(
                last_user_id[:3], int(last_user_id[3:]) + 1)
            self.user_id = user_id

            if pretty_print:
                print("New User created:\n{}".format(self.__dict__))

            # check for valid age
            try:
                _ = int(self.age)
            except ValueError:
                if pretty_print:
                    print("invalid age!!!\n{}".format(self.__dict__))
                return None

            # allow None or email pattern
            email_regex = re.compile(
                r'|([A-Za-z0-9]+[.-_])*[A-Za-z0-9]+@[A-Za-z0-9-]+(\.[A-Z|a-z]{2,})+')
            is_valid_email = re.fullmatch(email_regex, self.email)
            if not is_valid_email:
                if pretty_print:
                    print(":invalid email!!!\n{}".format(self.__dict__))
                return None

            return self
        except:
            # some error
            return None

    def save(self, filename="storage/users-data.json", pretty_print=True):
        users = User.get_users(pretty_print=False)
        users.append(self)
        User.save_users(users, filename)
        if pretty_print:
            print("successfully saved {}".format(self.__dict__))
        else:
            return self

    def to_json(self):
        return self.__dict__

    @staticmethod
    def save_users(users, filename="storage/users-data.json"):
        with open(filename, 'w') as file:
            json.dump(users, file, cls=UserEncoder)

    @staticmethod
    def get_users(filter_query=None, filename="storage/users-data.json", pretty_print=True):  # add query
        '''
        filter_query: A dictionary with keys as parameters and values as exact required value
            please note: due to limited time, I have not implemented filters with "AND" logic,
            but this will consider first exact match and return the results.
            pretty_print: will determine whether to show messages with user table or just return array of User objects
        '''
        users = None
        try:
            with open(filename, 'r') as file:
                users = json.load(file, object_hook=User.from_json)

        except FileNotFoundError:
            users = []

        if filter_query:
            query_results = []
            req_user_id = filter_query.get('user_id')
            req_name = filter_query.get('name')
            req_surname = filter_query.get('surname')
            req_email = filter_query.get('email')
            req_age_range = filter_query.get('age')

            for user in users:
                if (req_user_id) and (user.user_id == req_user_id):
                    query_results.append(user)
                    break
                if (req_name) and (user.name == req_name):
                    query_results.append(user)
                    break
                if (req_surname) and (user.name == req_surname):
                    query_results.append(user)
                    break
                if (req_email) and (user.email == req_email):
                    query_results.append(user)
                    break
                if (req_age_range) and (user.age >= req_age_range[0] and user.age < req_age_range[1]):
                    query_results.append(user)

            users = query_results
        if pretty_print:
            df = pd.DataFrame.from_records(
                [user.__dict__ for user in users])
            print(df.to_markdown())
        else:
            return users

    @staticmethod
    def update_user(user_id, update_options={}, filename="storage/users-data.json", pretty_print=True):
        '''
        user_id: user_id of the user to be updated
        update_options: dictionary containing attributes with updates.
                        do not include values not to be updated.
                        keys which are not attributes of the given class will be ignored.

        filename - location of the file
        pretty_print - Boolean to decide whether to print messages on console
        '''
        users = User.get_users(pretty_print=False, filename=filename)
        updated_user = None
        for i in range(len(users)):
            if users[i].user_id == user_id:
                for key, value in update_options.items():
                    if is_attribute(User, key):
                        users[i].__dict__[key] = value
                updated_user = users[i]
                break
        User.save_users(users)
        try:
            if pretty_print:
                print("\nUser successfully updated {}".format(
                    updated_user.__dict__))
            return updated_user
        except AttributeError:
            if pretty_print:
                print(
                    "\nuser with user id - {} not found.\nRefer current table for ID:\n".format(user_id))
                User.get_users()
            return None

    @staticmethod
    def delete_user(user_id, pretty_print=True):
        users = User.get_users(pretty_print=False)
        for i in range(len(users)):
            if users[i].user_id == user_id:
                _ = users.pop(i)
                User.save_users(users)
                break
        else:
            if pretty_print:
                print("user with user id - {} not found\n".format(user_id))
            else:
                return False
        if pretty_print:
            print("\nUser with id {} is successfully deleted".format(user_id))
        else:
            return User.get_users(pretty_print=pretty_print)

    @staticmethod
    def from_json(user_json):
        obj = User()
        for attribute in get_attributes(User):
            obj.__dict__[attribute] = user_json.get(attribute)
        return obj


class UserEncoder(json.JSONEncoder):
    def default(self, o):
        return o.__dict__
