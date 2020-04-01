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

@app.route("/register")
def register():

    return None

@app.route("/log_in")
def log_in():

    return None

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

if __name__ == '__main__':
    app.run(host='0.0.0.0')

