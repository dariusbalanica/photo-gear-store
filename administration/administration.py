import mysql.connector
import json
import sys

config = {
    'user': 'root',
    'password': 'root',
    'host': 'db',
    'port': '3306',
    'database': 'store'
}

cursor = None

def adaugare_produs(ProductID, Name, Category, Price, Stock):

    global cursor

    add_product = ("INSERT INTO Products "
            "(ProductID, Name, Category, Price, Stock) "
            "VALUES (%s, %s, %s, %s, %s)")
    product_data = (ProductID, Name, Category, Price, Stock)
    cursor.execute(add_product, product_data)

def actualizare_stoc(ProductID, Stock):

    global cursor

    update_stock = ("UPDATE Products SET Stock = %s WHERE ProductID = %s")
    update_stock_data = (Stock, ProductID)
    cursor.execute(update_stock, update_stock_data)

def anulare_comanda(OrderID):

    global cursor
    cursor.execute("SELECT * FROM Products")
    products_results = [(ProductID, Name, Category, Price, Stock) for (ProductID, Name, Category, Price, Stock) in cursor]
    print("Products list:")
    print(products_results)


def afisare_produse():

    global cursor
    cursor.execute("SELECT * FROM Products")
    products_results = [(ProductID, Name, Category, Price, Stock) for (ProductID, Name, Category, Price, Stock) in cursor]
    print("Products list:")
    print(products_results)

def print_administration_menu():

    print("---------- Administration ----------")
    print("Usage (type one of the following numbers): ")
    print("1 - Connect to the database")
    print("2 - Products list (If connected to the database)")
    print("3 - Add Product (If connected to the database)")
    print("4 - Update stock (If connected to the database)")
    print("5 - Exit")
    print("------------------------------------")

def start_administration():

    global cursor

    db_connected = False

    print_administration_menu()

    for line in sys.stdin:

        if line.rstrip() == "1":

            if db_connected == False:

                connection = mysql.connector.connect(**config)
                cursor = connection.cursor()
                db_connected = True
                print("Connected to the database!")

        elif line.rstrip() == "2":

            afisare_produse()

        elif line.rstrip() == "3":

            print("> Enter product to add: ")
            print("> Format: <ProductID> <Name> <Category> <Price> <Stock>")

            for word in sys.stdin:

                words = word.rstrip().split()

                adaugare_produs(words[0], words[1], words[2], words[3], words[4])
                connection.commit()
                break

        elif line.rstrip() == "4":

            print("> Enter information to update the stock of the product: ")
            print("> Format: <ProductID> <New Stock>")

            for word in sys.stdin:

                words = word.rstrip().split()

                actualizare_stoc(words[0], words[1])
                connection.commit()
                break

        elif line.rstrip() == "5":

            print("> Exiting...")
            break

        else:

            print_administration_menu()

    cursor.close()
    connection.close()

start_administration()

