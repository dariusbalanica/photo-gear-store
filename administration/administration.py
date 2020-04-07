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

def adaugare_produs(ProductID, Name, Brand, Category, Price, Stock):

    global cursor

    add_product = ("INSERT INTO Products "
            "(ProductID, Name, Brand, Category, Price, Stock) "
            "VALUES (%s, %s, %s, %s, %s, %s)")
    product_data = (ProductID, Name, Brand, Category, Price, Stock)
    cursor.execute(add_product, product_data)

def actualizare_stoc(ProductID, Stock):

    global cursor

    update_stock = ("UPDATE Products SET Stock = %s WHERE ProductID = %s")
    update_stock_data = (Stock, ProductID)
    cursor.execute(update_stock, update_stock_data)

def anulare_comanda(OrderID):

    global cursor

    cancel_order = ("DELETE FROM Orders WHERE OrderID = %s")
    cancel_order_data = (OrderID, )
    cursor.execute(cancel_order, cancel_order_data)

def stergere_produs(ProductID):

    global cursor

    remove_product = ("DELETE FROM Products WHERE ProductID = %s")
    remove_product_data = (ProductID, )
    cursor.execute(remove_product, remove_product_data)

def afisare_produse():

    global cursor

    cursor.execute("SELECT * FROM Products")
    result = cursor.fetchall()
    print(tabulate(result, headers=["ProductID", "Name", "Brand", "Category", "Price", "Stock"], tablefmt='psql'))

def print_administration_menu():

    print("+-------------------- Administration --------------------+")
    print("| Usage (type one of the following numbers then ENTER):  |")
    print("+--------------------------------------------------------+")
    print("| 1 - Connect to the database                            |")
    print("| 2 - Products list (If connected to the database)       |")
    print("| 3 - Add product (If connected to the database)         |")
    print("| 4 - Update stock (If connected to the database)        |")
    print("| 5 - Cancel order (If connected to the database)        |")
    print("| 6 - Remove product (If connected to the database)      |")
    print("| 7 - Exit                                               |")
    print("+--------------------------------------------------------+")

def start_administration():

    global cursor

    print_administration_menu()

    for line in sys.stdin:

        if line.rstrip() == "1":

            print("nimic")

        elif line.rstrip() == "2":
            connection = mysql.connector.connect(**config)
            cursor = connection.cursor()

            afisare_produse()

            cursor.close()
            connection.close()
        elif line.rstrip() == "3":
            connection = mysql.connector.connect(**config)
            cursor = connection.cursor()

            print("> Enter product to add: ")
            print("> Format: <ProductID>;<Name>;<Brand>;<Category>;<Price>;<Stock>")

            for word in sys.stdin:

                words = word.rstrip().split(";")

                adaugare_produs(words[0], words[1], words[2], words[3], words[4], words[5])
                connection.commit()
                break

            cursor.close()
            connection.close()
        elif line.rstrip() == "4":
            connection = mysql.connector.connect(**config)
            cursor = connection.cursor()

            print("> Enter information to update the stock of the product: ")
            print("> Format: <ProductID>;<New Stock>")

            for word in sys.stdin:

                words = word.rstrip().split(";")

                actualizare_stoc(words[0], words[1])
                connection.commit()
                break

            cursor.close()
            connection.close()
        elif line.rstrip() == "5":
            connection = mysql.connector.connect(**config)
            cursor = connection.cursor()

            print("> Enter information to cancel a specific order: ")
            print("> Format: <OrderID>")

            for word in sys.stdin:

                words = word.rstrip().split(";")

                anulare_comanda(words[0])
                connection.commit()
                break

            cursor.close()
            connection.close()
        elif line.rstrip() == "6":
            connection = mysql.connector.connect(**config)
            cursor = connection.cursor()

            print("> Enter information to remove a specific product: ")
            print("> Format: <ProductID>")

            for word in sys.stdin:

                words = word.rstrip().split(";")

                stergere_produs(words[0])
                connection.commit()
                break

            cursor.close()
            connection.close()
        elif line.rstrip() == "7":

            print("> Exiting...")
            break

        else:

            print_administration_menu()

start_administration()

