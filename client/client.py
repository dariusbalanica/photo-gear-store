import requests
import sys
import json

user_id = 0

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
    print("| 10 - Exit                                              |")
    print("+--------------------------------------------------------+")

def start_client():

    global user_id

    print_client_menu()

    for line in sys.stdin:

        if line.rstrip() == "1":

            response = requests.get(sys.argv[1] + "/register")
            response_dict = json.loads(response.text)
            print(response_dict)

        elif line.rstrip() == "2":

            response = requests.get(sys.argv[1] + "/log_in")
            response_dict = json.loads(response.text)
            print(response_dict)

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

            print("> Exiting...")
            break

        else:

            print_client_menu()

start_client()
