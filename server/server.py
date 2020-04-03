from flask import Flask
import mysql.connector
import json
import string
import random
from flask import request

app = Flask(__name__)

config = {
    'user': 'root',
    'password': 'root',
    'host': 'db',
    'port': '3306',
    'database': 'store'
}

cursor = None
user_id = 0
username = ""

@app.route("/register")
def register():

    global cursor
    global user_id
    global username

    connection = mysql.connector.connect(**config)
    cursor = connection.cursor()

    register_info = str(request.args.get("register info"))
    register_info_list = register_info.split(";")

    if user_id == 0:

        search_user = ("SELECT * FROM Users WHERE Name = %s OR Username = %s")
        search_user_data = (register_info_list[0], register_info_list[2])
        cursor.execute(search_user, search_user_data)

        result = cursor.fetchone()

        random_id = random.randrange(1, 10000)

        if result == None:

            add_user = ("INSERT INTO Users "
                "(UserID, Name, Email, Username, Password) VALUES (%s, %s, %s, %s, %s)")
            add_user_data = (random_id, register_info_list[0], \
            register_info_list[1], register_info_list[2], register_info_list[3])
            cursor.execute(add_user, add_user_data)
            connection.commit()

            user_id = random_id
            username = register_info_list[2]

        else:

            user_id = 0
            username = "user taken"

    else:

        username = "already logged in"

    cursor.close()
    connection.close()

    return json.dumps({"user_id" : user_id, "username" : username})

@app.route("/log_in")
def log_in():

    global cursor
    global user_id
    global username

    connection = mysql.connector.connect(**config)
    cursor = connection.cursor()

    log_in_info = str(request.args.get("log in info"))
    log_in_info_list = log_in_info.split(";")

    if user_id == 0:

        search_user = ("SELECT * FROM Users WHERE Username = %s AND Password = %s")
        search_user_data = (log_in_info_list[0], log_in_info_list[1])
        cursor.execute(search_user, search_user_data)

        result = cursor.fetchone()

        if result == None:

            username = "login error"

        else:

            username = log_in_info_list[0]
            user_id = result[0]

    else:

        username = "already logged in"

    cursor.close()
    connection.close()

    return json.dumps({"user_id" : user_id, "username" : username})

@app.route("/products_list")
def products_list():

    global cursor

    connection = mysql.connector.connect(**config)
    cursor = connection.cursor()

    cursor.execute("SELECT * FROM Products")
    results = [(ProductID, Name, Category, Price, Stock) for (ProductID, Name, Category, Price, Stock) in cursor]

    cursor.close()
    connection.close()

    return json.dumps({"Products" : results})

@app.route("/filter_products")
def filter_products():

    return None

@app.route("/sort_products")
def sort_products():

    return None

@app.route("/add_to_cart")
def add_to_cart():

    return None

@app.route("/remove_from_cart")
def remove_from_cart():

    return None

@app.route("/show_cart")
def show_cart():

    global cursor

    # Se realizeaza conectarea la baza de date
    connection = mysql.connector.connect(**config)
    cursor = connection.cursor()

    # Se primeste parametrul trimis prin cererea GET de la client (UserID-ul)
    user_info = str(request.args.get("UserID"))
    user_info_list = user_info.split()

    # Se cauta toate produsele adaugate in cos de catre userul respectiv
    cart = ("SELECT * FROM Cart WHERE UserID = %s")
    cart_data = (user_info_list[0])
    cursor.execute(cart, cart_data)

    result = cursor.fetchone()

    if result == None:
        cart_result = "No products in the cart for the given user!"
    else:
        cart_result = result

    # Se inchide conexiunea la baza de date
    cursor.close()
    connection.close()

    # Se intorc produsele asociate userului
    return json.dumps({"Cart Result": cart_result})

@app.route("/buy_products")
def buy_products():

    return None

@app.route("/log_out")
def log_out():

    global user_id
    global username

    if user_id == 0:

        username = "not logged in"

    else:

        user_id = 0
        username = ""

    return json.dumps({"user_id" : user_id, "username" : username})

if __name__ == '__main__':
    app.run(host='0.0.0.0')

