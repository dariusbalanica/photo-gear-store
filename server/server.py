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
logged_users_list = []

@app.route("/register")
def register():

    global cursor
    global user_id
    global username
    global logged_users_list

    connection = mysql.connector.connect(**config)
    cursor = connection.cursor()

    register_info = str(request.args.get("register info"))
    register_info_list = register_info.split(";")

    search_user = ("SELECT * FROM Users WHERE Name = %s OR Username = %s")
    search_user_data = (register_info_list[0], register_info_list[2])
    cursor.execute(search_user, search_user_data)

    result = cursor.fetchone()

    random_id = random.randrange(1, 100000)

    if result == None:

        add_user = ("INSERT INTO Users "
            "(UserID, Name, Email, Username, Password) VALUES (%s, %s, %s, %s, %s)")
        add_user_data = (random_id, register_info_list[0], \
        register_info_list[1], register_info_list[2], register_info_list[3])
        cursor.execute(add_user, add_user_data)
        connection.commit()

        user_id = random_id
        username = register_info_list[2]

        logged_users_list.append(user_id)

    else:

        user_id = 0
        username = "user taken"

    cursor.close()
    connection.close()

    return json.dumps({"user_id" : user_id, "username" : username})

@app.route("/log_in")
def log_in():

    global cursor
    global user_id
    global username
    global logged_users_list

    connection = mysql.connector.connect(**config)
    cursor = connection.cursor()

    log_in_info = str(request.args.get("log in info"))
    log_in_info_list = log_in_info.split(";")


    search_user = ("SELECT * FROM Users WHERE Username = %s AND Password = %s")
    search_user_data = (log_in_info_list[0], log_in_info_list[1])
    cursor.execute(search_user, search_user_data)

    result = cursor.fetchone()

    if result == None:

        username = "login error"

    else:

        username = log_in_info_list[0]
        user_id = result[0]

        logged_users_list.append(user_id)

    cursor.close()
    connection.close()

    return json.dumps({"user_id" : user_id, "username" : username})

@app.route("/products_list")
def products_list():

    global cursor

    connection = mysql.connector.connect(**config)
    cursor = connection.cursor()

    cursor.execute("SELECT ProductID, Name, Brand, Category, Price FROM Products")
    results = cursor.fetchall()

    cursor.close()
    connection.close()

    return json.dumps({"products" : results})

@app.route("/filter_products")
def filter_products():

    global cursor

    connection = mysql.connector.connect(**config)
    cursor = connection.cursor()

    filter_products_info = str(request.args.get("filter products info"))
    filter_products_info_list = filter_products_info.split(";")

    get_products = ("SELECT ProductID, Name, Brand, Category, Price FROM Products "
                   "WHERE Price BETWEEN %s and %s")
    get_products_data = (filter_products_info_list[0], filter_products_info_list[1])
    cursor.execute(get_products, get_products_data)
    results = cursor.fetchall()

    cursor.close()
    connection.close()

    return json.dumps({"products" : results})

@app.route("/sort_products")
def sort_products():

    global cursor

    connection = mysql.connector.connect(**config)
    cursor = connection.cursor()

    sort_products_info = str(request.args.get("sort products info"))
    sort_products_info_list = sort_products_info.split(";")

    get_products = ("SELECT ProductID, Name, Brand, Category, Price FROM Products "
                   "ORDER BY %s %s" % (sort_products_info_list[0], sort_products_info_list[1]))

    cursor.execute(get_products)
    results = cursor.fetchall()

    cursor.close()
    connection.close()

    return json.dumps({"products" : results})

@app.route("/add_to_cart")
def add_to_cart():

    global cursor

    connection = mysql.connector.connect(**config)
    cursor = connection.cursor()

    add_product_info = str(request.args.get("add product info"))
    user_id = str(request.args.get("user id"))
    username = str(request.args.get("username"))
    add_product_info_list = add_product_info.split(";")

    cursor.execute("SELECT * FROM Products WHERE ProductID = %s" % (add_product_info_list[0]))
    results = cursor.fetchone()

    if results == None:

        results = "unavailable"

    else:

        if results[-1] < int(add_product_info_list[1]):

            results = "out of stock"

        else:

            cursor.execute("SELECT * FROM Cart WHERE ProductID = %s and UserID = %s" % (add_product_info_list[0], user_id))
            cart_results = cursor.fetchone()

            if cart_results == None:

                add_product = ("INSERT INTO Cart "
                        "(UserID, ProductID, Quantity) VALUES (%s, %s, %s)")
                add_product_data = (user_id, add_product_info_list[0], add_product_info_list[1])
                cursor.execute(add_product, add_product_data)
                connection.commit()

            else:

                add_product = ("UPDATE Cart "
                        "SET Quantity = Quantity + %s WHERE ProductID = %s and UserID = %s")
                add_product_data = (add_product_info_list[1], add_product_info_list[0], user_id)
                cursor.execute(add_product, add_product_data)
                connection.commit()

            update_stock = ("UPDATE Products "
                    "SET Stock = %s WHERE ProductID = %s")
            update_stock_data = (results[-1] - int(add_product_info_list[1]), add_product_info_list[0])
            cursor.execute(update_stock, update_stock_data)
            connection.commit()

            results = "success"

    cursor.close()
    connection.close()

    return json.dumps({"cart" : results})

@app.route("/remove_from_cart")
def remove_from_cart():

    global cursor

    connection = mysql.connector.connect(**config)
    cursor = connection.cursor()

    remove_product_info = str(request.args.get("remove product info"))
    user_id = str(request.args.get("user id"))
    username = str(request.args.get("username"))
    remove_product_info_list = remove_product_info.split(";")

    cursor.execute("SELECT * FROM Cart WHERE ProductID = %s AND UserID = %s" % (remove_product_info_list[0], user_id))
    results = cursor.fetchone()

    if results == None:

        results = "not found"

    else:

        if results[-1] <= int(remove_product_info_list[1]):

            remove_product = ("DELETE FROM Cart "
                    "WHERE ProductID = %s AND UserID = %s")
            remove_product_data = (remove_product_info_list[0], user_id)
            cursor.execute(remove_product, remove_product_data)
            connection.commit()

        else:

            remove_product = ("UPDATE Cart "
                    "SET Quantity = Quantity - %s WHERE ProductID = %s and UserID = %s")
            remove_product_data = (remove_product_info_list[1], remove_product_info_list[0], user_id)
            cursor.execute(remove_product, remove_product_data)
            connection.commit()

        update_stock = ("UPDATE Products "
                "SET Stock = Stock + %s WHERE ProductID = %s")
        update_stock_data = (min(results[-1], int(remove_product_info_list[1])), remove_product_info_list[0])
        cursor.execute(update_stock, update_stock_data)
        connection.commit()

        results = "success"

    cursor.close()
    connection.close()

    return json.dumps({"cart" : results})

@app.route("/show_cart")
def show_cart():

    global cursor

    connection = mysql.connector.connect(**config)
    cursor = connection.cursor()

    user_id = str(request.args.get("user id"))
    username = str(request.args.get("username"))

    get_cart = ("SELECT Products.ProductID, Products.Name, Products.Price, Cart.Quantity FROM Products "
                   "INNER JOIN Cart ON Products.ProductID = Cart.ProductID WHERE Cart.UserID = %s" % (user_id))
    cursor.execute(get_cart)
    results = cursor.fetchall()

    if results == []:
        results = "empty"

    cursor.close()
    connection.close()

    return json.dumps({"cart": results})

@app.route("/buy_products")
def buy_products():

    global cursor

    connection = mysql.connector.connect(**config)
    cursor = connection.cursor()

    user_id = str(request.args.get("user id"))
    username = str(request.args.get("username"))

    cursor.execute("SELECT * FROM Cart WHERE UserID = %s" % (user_id))
    results = cursor.fetchall()

    if results == []:

        results = "empty"

    else:

        cursor.execute("DELETE FROM Cart WHERE UserID = %s" % (user_id))
        connection.commit()
        order_id = ''.join(random.choices(string.ascii_uppercase + string.digits, k = 30))

        add_product = ("INSERT INTO Orders "
                "(OrderID, UserID) VALUES (%s, %s)")
        add_product_data = (order_id, user_id)
        cursor.execute(add_product, add_product_data)
        connection.commit()

        results = order_id

    cursor.close()
    connection.close()

    return json.dumps({"buy": results})

@app.route("/log_out")
def log_out():

    global user_id
    global username
    global logged_users_list

    user_id = 0
    username = ""
    logged_users_list.remove(int(str(request.args.get("user_id"))))

    return json.dumps({"user_id" : 0, "username" : ""})

if __name__ == '__main__':
    app.run(host='0.0.0.0')

