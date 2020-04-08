import requests
import sys
import json
from tabulate import tabulate

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

            if user_id == 0:

                print("+--------------------------------------------------------+")
                print("| Enter data to register (or press just ENTER to quit):  |")
                print("| Format: <name>;<email>;<username>;<password>           |")
                print("+--------------------------------------------------------+")

                for word in sys.stdin:
                    register_info = word.rstrip()
                    break

                if len(register_info.split(";")) != 4 or "" in register_info.split(";"):
                    print("+--------------------------------------------------------+")
                    print("| Invalid data format                                    |")
                    print("+--------------------------------------------------------+")
                    print_client_menu()
                    continue

                response = requests.get(sys.argv[1] + "/register", params = {"register info" : register_info})
                response_dict = json.loads(response.text)

                if response_dict["username"] == "user taken":
                    print("+--------------------------------------------------------+")
                    print("| User already exists, please try again.                 |")
                    print("+--------------------------------------------------------+")
                    print_client_menu()
                    continue

                username = response_dict["username"]
                user_id = response_dict["user_id"]

            else:

                print("+--------------------------------------------------------+")
                print("| Already logged in as a user, please log out first.     |")
                print("+--------------------------------------------------------+")
                print_client_menu()
                continue

            print_logged_user()
            print_client_menu()

        elif line.rstrip() == "2":

            if user_id == 0:

                print("+--------------------------------------------------------+")
                print("| Enter data to log in:                                  |")
                print("| Format: <username>;<password>                          |")
                print("+--------------------------------------------------------+")

                for word in sys.stdin:
                    log_in_info = word.rstrip()
                    break

                if len(log_in_info.split(";")) != 2 or "" in log_in_info.split(";"):
                    print("+--------------------------------------------------------+")
                    print("| Invalid data format                                    |")
                    print("+--------------------------------------------------------+")
                    print_client_menu()
                    continue

                response = requests.get(sys.argv[1] + "/log_in", params = {"log in info" : log_in_info})
                response_dict = json.loads(response.text)

                if response_dict["username"] == "login error":
                    print("+--------------------------------------------------------+")
                    print("| Unexistent user, or wrong credentials, try again.      |")
                    print("+--------------------------------------------------------+")
                    print_client_menu()
                    continue

                username = response_dict["username"]
                user_id = response_dict["user_id"]

            else:

                print("+--------------------------------------------------------+")
                print("| Already logged in as a user, please log out first.     |")
                print("+--------------------------------------------------------+")
                print_client_menu()
                continue

            print_logged_user()
            print_client_menu()

        elif line.rstrip() == "3":

            response = requests.get(sys.argv[1] + "/products_list")
            response_dict = json.loads(response.text)
            print(tabulate(response_dict["products"], headers=["ProductID", "Name", "Brand", "Category", "Price"], tablefmt='psql'))

            print_logged_user()
            print_client_menu()

        elif line.rstrip() == "4":

            print("+--------------------------------------------------------+")
            print("| Enter data to filter products by price:                |")
            print("| Format: <minimum_price>;<maximum_price>                |")
            print("+--------------------------------------------------------+")

            for word in sys.stdin:
                filter_products_info = word.rstrip()
                break

            if len(filter_products_info.split(";")) != 2 or "" in filter_products_info.split(";"):
                print("+--------------------------------------------------------+")
                print("| Invalid data format                                    |")
                print("+--------------------------------------------------------+")
                print_client_menu()
                continue

            response = requests.get(sys.argv[1] + "/filter_products", params = {"filter products info" : filter_products_info})
            response_dict = json.loads(response.text)

            print(tabulate(response_dict["products"], headers=["ProductID", "Name", "Brand", "Category", "Price"], tablefmt='psql'))

            print_logged_user()
            print_client_menu()

        elif line.rstrip() == "5":

            print("+--------------------------------------------------------+")
            print("| Sort options: -parameter: Name, Brand, Category, Price |")
            print("|               -type: ASC, DESC                         |")
            print("| Enter data to sort products:                           |")
            print("| Format: <parameter>;<type>                             |")
            print("+--------------------------------------------------------+")

            for word in sys.stdin:
                sort_products_info = word.rstrip()
                break

            if len(sort_products_info.split(";")) != 2 or "" in sort_products_info.split(";"):
                print("+--------------------------------------------------------+")
                print("| Invalid data formet                                    |")
                print("+--------------------------------------------------------+")
                print_client_menu()
                continue

            response = requests.get(sys.argv[1] + "/sort_products", params = {"sort products info" : sort_products_info})
            response_dict = json.loads(response.text)

            print(tabulate(response_dict["products"], headers=["ProductID", "Name", "Brand", "Category", "Price"], tablefmt='psql'))

            print_logged_user()
            print_client_menu()

        elif line.rstrip() == "6":

            if user_id == 0:

                print("+--------------------------------------------------------+")
                print("| Not logged in, please log in first                     |")
                print("+--------------------------------------------------------+")
                print_client_menu()
                continue

            else:

                print("+--------------------------------------------------------+")
                print("| Enter data to add a product to cart:                   |")
                print("| Format: <product_id>;<quantity>                        |")
                print("+--------------------------------------------------------+")

                for word in sys.stdin:
                    add_product_info = word.rstrip()
                    break

                if len(add_product_info.split(";")) != 2 or "" in add_product_info.split(";"):
                    print("+--------------------------------------------------------+")
                    print("| Invalid data format                                    |")
                    print("+--------------------------------------------------------+")
                    print_client_menu()
                    continue

                response = requests.get(sys.argv[1] + "/add_to_cart", params = {"user id" : user_id, "username" : username, "add product info" : add_product_info})
                response_dict = json.loads(response.text)

                if response_dict["cart"] == "unavailable":
                    print("+--------------------------------------------------------+")
                    print("| Product unavailable                                    |")
                    print("+--------------------------------------------------------+")
                    print_client_menu()
                    continue
                elif response_dict["cart"] == "out of stock":
                    print("+--------------------------------------------------------+")
                    print("| Not enough items in stock                              |")
                    print("+--------------------------------------------------------+")
                    print_client_menu()
                    continue
                elif response_dict["cart"] == "success":
                    print("+--------------------------------------------------------+")
                    print("| Product successfully added to cart                     |")
                    print("+--------------------------------------------------------+")

            print_logged_user()
            print_client_menu()

        elif line.rstrip() == "7":

            if user_id == 0:

                print("+--------------------------------------------------------+")
                print("| Not logged in, please log in first                     |")
                print("+--------------------------------------------------------+")
                print_client_menu()
                continue

            else:

                print("+--------------------------------------------------------+")
                print("| Enter data to remove a product from cart:              |")
                print("| Format: <product_id>;<quantity_to_remove>              |")
                print("+--------------------------------------------------------+")

                for word in sys.stdin:
                    remove_product_info = word.rstrip()
                    break

                if len(remove_product_info.split(";")) != 2 or "" in remove_product_info.split(";"):
                    print("+--------------------------------------------------------+")
                    print("| Invalid data format                                    |")
                    print("+--------------------------------------------------------+")
                    print_client_menu()
                    continue

                response = requests.get(sys.argv[1] + "/remove_from_cart", params = {"user id" : user_id, "username" : username, "remove product info" : remove_product_info})
                response_dict = json.loads(response.text)

                if response_dict["cart"] == "not found":
                    print("+--------------------------------------------------------+")
                    print("| Product not in cart                                    |")
                    print("+--------------------------------------------------------+")
                    print_client_menu()
                    continue
                if response_dict["cart"] == "out of stock":
                    print("+--------------------------------------------------------+")
                    print("| Product out of stock                                   |")
                    print("+--------------------------------------------------------+")
                    print_client_menu()
                    continue
                elif response_dict["cart"] == "success":
                    print("+--------------------------------------------------------+")
                    print("| Product successfully removed from cart                 |")
                    print("+--------------------------------------------------------+")

            print_logged_user()
            print_client_menu()

        elif line.rstrip() == "8":

            if user_id == 0:

                print("+--------------------------------------------------------+")
                print("| Not logged in, please log in first                     |")
                print("+--------------------------------------------------------+")
                print_client_menu()
                continue

            else:

                response = requests.get(sys.argv[1] + "/show_cart", params = {"user id" : user_id, "username" : username})
                response_dict = json.loads(response.text)

                if response_dict["cart"] == "empty":

                    print("+--------------------------------------------------------+")
                    print("| Empty cart                                             |")
                    print("+--------------------------------------------------------+")
                    print_client_menu()
                    continue

            print(tabulate(response_dict["cart"], headers=["ProductID", "ProductName", "Price", "Quantity"], tablefmt='psql'))

            print_logged_user()
            print_client_menu()

        elif line.rstrip() == "9":

            if user_id == 0:

                print("+--------------------------------------------------------+")
                print("| Not logged in, please log in first                     |")
                print("+--------------------------------------------------------+")
                print_client_menu()
                continue

            else:

                print("+--------------------------------------------------------+")
                print("| Enter data to buy products in cart:                    |")
                print("| Format: <Name>;<Address>;<CardNumber>;<ExpDate>;<CVV>  |")
                print("+--------------------------------------------------------+")

                for word in sys.stdin:
                    buy_products_info = word.rstrip()
                    break

                if len(buy_products_info.split(";")) != 5 or "" in buy_products_info.split(";"):
                    print("+--------------------------------------------------------+")
                    print("| Invalid data format                                    |")
                    print("+--------------------------------------------------------+")
                    print_client_menu()
                    continue

                response = requests.get(sys.argv[1] + "/buy_products", params = {"user id" : user_id, "username" : username, "buy data" : buy_products_info})
                response_dict = json.loads(response.text)

                if response_dict["buy"] == "empty":

                    print("+--------------------------------------------------------+")
                    print("| Empty cart, please add products first                  |")
                    print("+--------------------------------------------------------+")
                    print_client_menu()
                    continue

                print("+--------------------------------------------------------+")
                print("| ReservationID: " + response_dict["buy"] + " " * (40 - len(response_dict["buy"])) + "|")
                print("+--------------------------------------------------------+")

            print_logged_user()
            print_client_menu()

        elif line.rstrip() == "10":

            if user_id == 0:

                print("+--------------------------------------------------------+")
                print("| Not logged in, no need to log out.                     |")
                print("+--------------------------------------------------------+")
                print_client_menu()
                continue

            else:

                response = requests.get(sys.argv[1] + "/log_out", params = {"user_id" : user_id, "username" : username})
                response_dict = json.loads(response.text)

                print("+--------------------------------------------------------+")
                print("| Logging out...                                         |")
                print("+--------------------------------------------------------+")
                username = response_dict["username"]
                user_id = response_dict["user_id"]

            print_logged_user()
            print_client_menu()

        elif line.rstrip() == "11":

            print("+--------------------------------------------------------+")
            print("| Exiting...                                             |")
            print("+--------------------------------------------------------+")
            user_id = 0
            username = ""
            break

        else:

            print_client_menu()

start_client()
