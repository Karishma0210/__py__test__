import re
from classes.user import User

def quit_handler():
    print("Quiting from the system")
    quit()

def create_user_handler():
    print("Fill up required field for the user")
    print("*required")
    name = None
    while not name:
        name = input("name*:")
    surname = input("surname:")
    age, age_in = None, None
    while not age:
        age_in = input("age:")
        if age_in:
            try:
                age = int(age_in)
            except ValueError:
                print("enter numeric values")
        else:
            break
    
    email = None
    # allow None or email pattern
    email_regex = re.compile(r'|([A-Za-z0-9]+[.-_])*[A-Za-z0-9]+@[A-Za-z0-9-]+(\.[A-Z|a-z]{2,})+')
    is_valid_email = False
    while not is_valid_email:
        email = input("email:")
        is_valid_email = re.fullmatch(email_regex, email)
    
    user = User(name, surname, age, email)
    user.create_user()
    save_user_handler(user)
    
def save_user_handler(user):
    switcher = {
        0: quit_handler,
        1: user.save,
        2: discard
    }
    print("\nTo save this user - Press 1 ")
    print("To discard above user - Press 2")
    user_input = None
    while not user_input:
        try:
            user_input = int(input("Your input: "))
        except ValueError:
            print("Invalid value. Please press again!")
    selected_func = switcher.get(user_input, None)
    selected_func()

def discard():
    # since its not supposed to process the user
    pass
  
def get_users_handler():
    print("Below is the table for all the users:\n\n")
    User.get_users()
    user_input = input("\nYou want any specific filters in this? (y/n)").lower()
    if user_input.startswith('y'):
        filter_query = {}
        print("\nPlease leave blank for no filter in that field")
        filter_query["user_id"] = input("user_id: ").upper()
        filter_query["name"] = input("name: ")
        filter_query["surname"] = input("surname: ")
        filter_query["email"] = input("email: ")
        try:
            filter_query["age"] = (int(input("start - age: ")), int(input("max - age: ")))
        except ValueError:
            print("age filter will not be considered")
        
        User.get_users(filter_query=filter_query)
    
def update_user_handler():
    user_id = None
    while not user_id:
        user_id = input("Please enter the user id for updating record (format: 'VIA0001'): ")
        
    update_options = {}
    print("\nPlease leave blank for no update in that field")
    update_options["name"] = input("name: ")
    update_options["surname"] = input("surname: ")
    email = None
    # allow None or email pattern
    email_regex = re.compile(r'|([A-Za-z0-9]+[.-_])*[A-Za-z0-9]+@[A-Za-z0-9-]+(\.[A-Z|a-z]{2,})+')
    is_valid_email = False
    while not is_valid_email:
        email = input("email:")
        is_valid_email = re.fullmatch(email_regex, email)
    update_options["email"] = email
    
    try:
        update_options["age"] = int(input("age: "))
    except ValueError:
            print("age will not be updated")
    User.update_user(user_id, update_options=update_options)
    
    
    
def delete_user_handler():
    user_id = None
    while not user_id:
        user_id = input("Please enter the user id for deleting a record (format: 'VIA0001'): ")
    
    User.delete_user(user_id)
    