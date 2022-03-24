import os
import pytest
from handler.user import create_user_handler, quit_handler, get_users_handler, update_user_handler, delete_user_handler

current_dir = os.path.dirname(__file__)
storage_loc = os.path.join(current_dir, 'storage/user-data.json')
   
def automated_test():
    print('\n\n')
    # TODO: write automated test from PyTest Library
    retcode = pytest.main()
    print("automated test successfully completed!")

def client_ui_test():
    print("\n\n")
    switcher = {
        1: create_user_handler,
        2: get_users_handler,
        3: update_user_handler,
        4: delete_user_handler,
        0: quit_handler
    }
    
    while True:
        print("\n\nINFO: You can press 0 anytime in the input for exiting")
        print("""
            Press 1 - to create a user,
            Press 2 - to get the users,
            Press 3 - to update a user,
            Press 4 - to delete a user
            """)
        user_input = None
        while user_input == None or user_input == '':
            try:
                user_input = int(input("Your input: "))
            except ValueError:
                print("Invalid value. Please press again!")
        selected_func = switcher.get(user_input, None)
        if(not selected_func):
            print("Opps! Please try again")
            continue
        selected_func()
    
    
    
def main():
    print("Hello!!! Welcome to Karishma's Technical Assesment for Python")
    print("So, we will perform CRUD operations on User class; this data will be stored in local storage under folder - {}".format(storage_loc))
    
    print("#"*50)
    print("{: >26}".format("BEGIN"))
    print("#"*50)
    
    print("\n\n")
    
    switcher = {
        1: automated_test,
        2: client_ui_test,
        0: quit_handler 
    }
    selected_func = None
    for current_try in range(5):
        print("INFO: You can press 0 anytime in the input for exiting")
        print("- Press 1 for automated testing with PyTest")
        print("- Press 2 to begin testing it manually")
        user_input = None
        while not user_input:
            try:
                user_input = int(input("Your input: "))
            except ValueError:
                print("Invalid value. Please press again!")
        selected_func = switcher.get(user_input, None)
        if(not selected_func):
            print("Opps! Please try again")
        else:
            break
    else:
        print("Maximum number of invalid inputs attempted!!!")
        quit_handler()
        #shut the program
        
    selected_func()


if __name__ == "__main__":
    main()