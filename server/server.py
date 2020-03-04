from flask import Flask
import mysql.connector
import json
import string
import random
from flask import request

app = Flask(__name__)

# Datele folosite pentru conectarea la baza de date
config = {
    'user': 'root',
    'password': 'root',
    'host': 'db',
    'port': '3306',
    'database': 'store'
}

# Un cursor global utilizat pentru manipularea tabelelor din baza de date
cursor = None

# Functie care realizeaza afisarea produselor intr-un format human-readable,
# urmand sa fie apelata in momentul in care clientul face un request pe ruta specificata
@app.route("/")
def list_products():

    global cursor

    # Se realizeza conectarea la baza de date
    connection = mysql.connector.connect(**config)
    cursor = connection.cursor()

    # Este interogata tabela asociata produselor din cadrul magazinului
    cursor.execute("SELECT * FROM Products")
    results = [(ProductID, Name, Category, Price, Stock) for (ProductID, Name, Category, Price, Stock) in cursor]

    # Se inchide conexiunea la baza de date
    cursor.close()
    connection.close()

    # Se intoarce un json ce contine datele despre produse
    return json.dumps({"Products" : results})

# Functie care intoarce toate produsele adaugate in cosul de cumparaturi de
# catre un anumit user, identificat prin ID-ul sau trimis ca parametru, urmand
# sa fie apelata in momentul in care clientul face request pe ruta
# specificata
@app.route("/cart")
def list_cart():

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

if __name__ == '__main__':
    app.run(host='0.0.0.0')

