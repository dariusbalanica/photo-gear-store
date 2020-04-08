import mysql.connector
import json
import sys
from tabulate import tabulate

config = {
    'user': 'root',
    'password': 'root',
    'host': 'db',
    'port': '3306',
    'database': 'store'
}

cursor = None

def add_product_func(ProductID, Name, Brand, Category, Price, Stock):

    global cursor

    add_product_func = ("INSERT INTO Products "
            "(ProductID, Name, Brand, Category, Price, Stock) "
            "VALUES (%s, %s, %s, %s, %s, %s)")
    product_data = (ProductID, Name, Brand, Category, Price, Stock)
    cursor.execute(add_product_func, product_data)

def update_stock_func(ProductID, Stock):

    global cursor

    update_stock = ("UPDATE Products SET Stock = %s WHERE ProductID = %s")
    update_stock_data = (Stock, ProductID)
    cursor.execute(update_stock, update_stock_data)

def cancel_order_func(OrderID):

    global cursor

    cancel_order = ("DELETE FROM Orders WHERE OrderID = %s")
    cancel_order_data = (OrderID, )
    cursor.execute(cancel_order, cancel_order_data)

def remove_product_func(ProductID):

    global cursor

    remove_product_func = ("DELETE FROM Products WHERE ProductID = %s")
    remove_product_func_data = (ProductID, )
    cursor.execute(remove_product_func, remove_product_data)

def show_products_func():

    global cursor

    cursor.execute("SELECT * FROM Products")
    result = cursor.fetchall()
    print(tabulate(result, headers=["ProductID", "Name", "Brand", "Category", "Price", "Stock"], tablefmt='psql'))

def print_administration_menu():

    print("+-------------------- Administration --------------------+")
    print("| Usage (type one of the following numbers then ENTER):  |")
    print("+--------------------------------------------------------+")
    print("| 1 - Products list                                      |")
    print("| 2 - Add product                                        |")
    print("| 3 - Update stock                                       |")
    print("| 4 - Cancel order                                       |")
    print("| 5 - Remove product                                     |")
    print("| 6 - Exit                                               |")
    print("+--------------------------------------------------------+")

def start_administration():

    global cursor

    print_administration_menu()

    for line in sys.stdin:

        if line.rstrip() == "1":
            connection = mysql.connector.connect(**config)
            cursor = connection.cursor()

            show_products_func()

            print_administration_menu()
            cursor.close()
            connection.close()
        elif line.rstrip() == "2":
            connection = mysql.connector.connect(**config)
            cursor = connection.cursor()

            print("+---------------------------------------------------------------+")
            print("| Enter data to add a product:                                  |")
            print("| Format: <ProductID>;<Name>;<Brand>;<Category>;<Price>;<Stock> |")
            print("+---------------------------------------------------------------+")

            for word in sys.stdin:

                words = word.rstrip().split(";")
                break

            if len(words) != 6 or "" in words:
                print("+--------------------------------------------------------+")
                print("| Invalid data formet                                    |")
                print("+--------------------------------------------------------+")
                print_administration_menu()
                continue

            add_product_func(words[0], words[1], words[2], words[3], words[4], words[5])
            connection.commit()

            print_administration_menu()
            cursor.close()
            connection.close()
        elif line.rstrip() == "3":
            connection = mysql.connector.connect(**config)
            cursor = connection.cursor()

            print("+---------------------------------------------------------------+")
            print("| Enter data to update the stock of a product:                  |")
            print("| Format: <ProductID>;<New Stock>                               |")
            print("+---------------------------------------------------------------+")

            for word in sys.stdin:

                words = word.rstrip().split(";")
                break

            if len(words) != 2 or "" in words:
                print("+--------------------------------------------------------+")
                print("| Invalid data formet                                    |")
                print("+--------------------------------------------------------+")
                print_administration_menu()
                continue

            update_stock_func(words[0], words[1])
            connection.commit()

            print_administration_menu()
            cursor.close()
            connection.close()
        elif line.rstrip() == "4":
            connection = mysql.connector.connect(**config)
            cursor = connection.cursor()

            print("+---------------------------------------------------------------+")
            print("| Enter information to cancel a specific order:                 |")
            print("| Format: <OrderID>                                             |")
            print("+---------------------------------------------------------------+")

            for word in sys.stdin:

                words = word.rstrip().split(";")
                break

            if len(words) != 1 or "" in words:
                print("+--------------------------------------------------------+")
                print("| Invalid data formet                                    |")
                print("+--------------------------------------------------------+")
                print_administration_menu()
                continue

            cancel_order_func(words[0])
            connection.commit()

            print_administration_menu()
            cursor.close()
            connection.close()
        elif line.rstrip() == "5":
            connection = mysql.connector.connect(**config)
            cursor = connection.cursor()

            print("+---------------------------------------------------------------+")
            print("| Enter information to remove a specific product:               |")
            print("| Format: <ProductID>                                           |")
            print("+---------------------------------------------------------------+")

            for word in sys.stdin:

                words = word.rstrip().split(";")
                break

            if len(words) != 1 or "" in words:
                print("+--------------------------------------------------------+")
                print("| Invalid data formet                                    |")
                print("+--------------------------------------------------------+")
                print_administration_menu()
                continue

            remove_product_func(words[0])
            connection.commit()

            print_administration_menu()
            cursor.close()
            connection.close()
        elif line.rstrip() == "6":

            print("+--------------------------------------------------------+")
            print("| Exiting...                                             |")
            print("+--------------------------------------------------------+")
            break

        else:

            print_administration_menu()

start_administration()

