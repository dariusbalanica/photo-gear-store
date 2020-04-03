import requests
import sys
import json

user_id = 0
username = ""

def print_client_menu():

    print("+------------------------ Client ------------------------+")
    print("| Usage (type one of the following numbers then ENTER):  |")
    print("+--------------------------------------------------------+")
    print("| 1 - Register                                           |")
    print("| 2 - Log in                                             |")
    print("| 3 - Products list                                      |")
    print("| 4 - Filter products                                    |")
    print("| 5 - Sort products                                      |")
    print("| 6 - Add to cart                                        |")
    print("| 7 - Remove from cart                                   |")
    print("| 8 - Show cart                                          |")
    print("| 9 - Buy products                                       |")
    print("| 10 - Log out                                           |")
    print("| 11 - Exit                                              |")
    print("+--------------------------------------------------------+")

def print_logged_user():

    global user_id
    global username

    if user_id == 0:
        print("+--------------------------------------------------------+")
        print("|           You are not logged in right now!             |")
        print("+--------------------------------------------------------+")
    else:
        print("+--------------------------------------------------------+")
        print("|           Logged in as " + username + " " * (32 - len(username)) + "|")
        print("+--------------------------------------------------------+")

def start_client():

    global user_id
    global username

    print_logged_user()
    print_client_menu()

    for line in sys.stdin:

        if line.rstrip() == "1":

            print("+--------------------------------------------------------+")
            print("| Enter data to register:                                |")
            print("| Format: <name>;<email>;<username>;<password>           |")
            print("+--------------------------------------------------------+")

            for word in sys.stdin:
                register_info = word.rstrip()
                break

            response = requests.get(sys.argv[1] + "/register", params = {"register info" : register_info})
            response_dict = json.loads(response.text)

            if response_dict["username"] == "user taken":
                print("+--------------------------------------------------------+")
                print("| User already exists, please try again.                 |")
                print("+--------------------------------------------------------+")
                print_client_menu()
                continue
            elif response_dict["username"] == "already logged in":
                print("+--------------------------------------------------------+")
                print("| Already logged in as a user, please log out first.     |")
                print("+--------------------------------------------------------+")
                print_client_menu()
                continue

            username = response_dict["username"]
            user_id = response_dict["user_id"]

            print_logged_user()
            print_client_menu()

        elif line.rstrip() == "2":

            print("+--------------------------------------------------------+")
            print("| Enter data to log in:                                  |")
            print("| Format: <username>;<password>                          |")
            print("+--------------------------------------------------------+")

            for word in sys.stdin:
                log_in_info = word.rstrip()
                break

            response = requests.get(sys.argv[1] + "/log_in", params = {"log in info" : log_in_info})
            response_dict = json.loads(response.text)

            if response_dict["username"] == "login error":
                print("+--------------------------------------------------------+")
                print("| Unexistent user, or wrong credentials, try again.      |")
                print("+--------------------------------------------------------+")
                print_client_menu()
                continue
            elif response_dict["username"] == "already logged in":
                print("+--------------------------------------------------------+")
                print("| Already logged in as a user, please log out first.     |")
                print("+--------------------------------------------------------+")
                print_client_menu()
                continue

            username = response_dict["username"]
            user_id = response_dict["user_id"]

            print_logged_user()
            print_client_menu()

        elif line.rstrip() == "3":

            response = requests.get(sys.argv[1] + "/products_list")
            response_dict = json.loads(response.text)
            print(response_dict)

        elif line.rstrip() == "4":

            response = requests.get(sys.argv[1] + "/filter_products")
            response_dict = json.loads(response.text)
            print(response_dict)

        elif line.rstrip() == "5":

            response = requests.get(sys.argv[1] + "/sort_products")
            response_dict = json.loads(response.text)
            print(response_dict)

        elif line.rstrip() == "6":

            response = requests.get(sys.argv[1] + "/add_to_cart")
            response_dict = json.loads(response.text)
            print(response_dict)

        elif line.rstrip() == "7":

            response = requests.get(sys.argv[1] + "/remove_from_cart")
            response_dict = json.loads(response.text)
            print(response_dict)

        elif line.rstrip() == "8":

            response = requests.get(sys.argv[1] + "/show_cart")
            response_dict = json.loads(response.text)
            print(response_dict)

        elif line.rstrip() == "9":

            response = requests.get(sys.argv[1] + "/buy_products")
            response_dict = json.loads(response.text)
            print(response_dict)

        elif line.rstrip() == "10":

            response = requests.get(sys.argv[1] + "/log_out")
            response_dict = json.loads(response.text)

            if response_dict["username"] == "not logged in":

                print("+--------------------------------------------------------+")
                print("| Not logged in, no need to log out.                     |")
                print("+--------------------------------------------------------+")
                print_client_menu()
                continue

            else:

                print("+--------------------------------------------------------+")
                print("| Logging out...                                         |")
                print("+--------------------------------------------------------+")
                username = ""
                user_id = 0

            print_logged_user()
            print_client_menu()

        elif line.rstrip() == "11":

            print("> Exiting...")
            break

        else:

            print_client_menu()

start_client()
