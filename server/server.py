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
    'database': 'flights'
}

# Un cursor global utilizat pentru manipularea tabelelor din baza de date
cursor = None

# Functie care realizeaza afisarea zborurilor intr-un format human-readable,
# fiind apelata in momentul in care clientul face un request pe ruta specificata
@app.route("/")
def list_flights():

    global cursor

    # Se realizeza conectarea la baza de date
    connection = mysql.connector.connect(**config)
    cursor = connection.cursor()

    # Este interogata tabela asociata zborurilor
    cursor.execute("SELECT * FROM Flights")
    results = [(ID, Source, Destination, Hour, Day, Duration, Seats) for (ID, Source, Destination, Hour, Day, Duration, Seats) in cursor]

    # Se inchide conexiunea la baza de date
    cursor.close()
    connection.close()

    # Se intoarce un json ce contine datele despre zboruri obtinute anterior
    return json.dumps({"Flights" : results})

# Functie care intoarce un zbor disponibil dintre o sursa si o destinatie
# introduse de la tastatura, precum si luand in calcul ziua plecarii,
# fiind apelata in momentul in care clientul face request pe ruta
# specificata
@app.route("/find")
def get_optimal_route():

    global cursor

    # Se realizeaza conectarea la baza de date
    connection = mysql.connector.connect(**config)
    cursor = connection.cursor()

    # Se primesc parametrii trimisi prin cererea GET de la client,
    # fiind reprezentati de un string cu toate informatiile necesare
    # determinarii zborului dintre cele 2 locatii
    search_info = str(request.args.get("Search Info"))
    search_info_list = search_info.split()

    # Se cauta un zbor direct dintre sursa si destinatie, tinand cont de ziua plecarii
    search_route = ("SELECT * FROM Flights WHERE Source = %s AND Destination = %s AND Day = %s")
    search_route_data = (search_info_list[0], search_info_list[1], search_info_list[3])
    cursor.execute(search_route, search_route_data)

    result = cursor.fetchone()

    # Daca nu a fost gasita o ruta directa, se intoarce un mesaj de eroare,
    # dar daca a fost gasit un zbor care sa satisfaca conditiile, se retine
    # zborul respectiv
    if result == None:
        search_result = "No direct route found!"
    else:
        search_result = result

    # Se inchide conexiunea la baza de date
    cursor.close()
    connection.close()

    # Se intoarce rezultatul cautarii
    return json.dumps({"Search Result": search_result})

# Functie care gesioneaza efectuarea de rezervari pentru un anumit numar de
# zboruri, fiind apelata in momentul in care clientul face un request pe
# ruta specificata
@app.route("/book")
def book_ticket():

    global cursor

    # Se realizeaza conectarea la baza de date
    connection = mysql.connector.connect(**config)
    cursor = connection.cursor()

    # Se obtin parametrii trimisi de catre client prin cererea GET
    # (Un string format din ID-urile zborurilor pentru care se doreste
    # sa se faca rezervari, separate prin spatiu)
    flights_ids = str(request.args.get("Flights IDs"))
    # Se obtine o lista de ID-uri din string-ul initial
    flights_ids_list = flights_ids.split()
    available_flights = []

    # Se verifica daca mai exista locuri disponibile pentru zborurile dorite
    for flight_id in flights_ids_list:

        cursor.execute("SELECT Flight_Capacity, Booked_Seats FROM Booking_Capacity WHERE Flight_ID = %s", (flight_id, ))

        # Se extrag numarul de locuri rezervate pana in momentul curent si capacitatea avionului
        # pentru zborul curent
        (flight_capacity, booked_seats) = cursor.fetchone()
        # Se considera ca fiind disponibile in total 110% din locurile disponibile pentru zborul respectiv
        # in avion, conform politicilor companiilor aeriene si conform enuntului
        total_booking_capacity = int(1.1 * flight_capacity)

        # Daca mai exista locuri disponibile pentru zborul curent, se adauga acesta
        # la lista de zboruri disponibile
        if booked_seats < total_booking_capacity:
            available_flights.append(flight_id)

    # Daca toate zborurile primite de la client sunt disponibile
    if len(flights_ids_list) == len(available_flights):

        # Se efectueaza rezervarea pentru fiecare zbor in parte, actualizand
        # numarul de locuri disponibile
        for flight_id in flights_ids_list:

            cursor.execute("SELECT Flight_Capacity, Booked_Seats FROM Booking_Capacity WHERE Flight_ID = %s", (flight_id, ))
            (flight_capacity, booked_seats) = cursor.fetchone() #asa trimit zborul (prima inregistrare din cursor)

            updated_booked_seats = booked_seats + 1

            cursor.execute("UPDATE Booking_Capacity SET Booked_Seats = %s WHERE Flight_ID = %s", (updated_booked_seats, flight_id))
            connection.commit()

        # Se genereaza un ID de rezervare format dintr-un sir de 40 de caractere
        # alfanumerice generat aleator
        reservation_id =  "".join(random.choice(string.ascii_lowercase + string.digits) for _ in range(40))

        # Se actualizeaza tabela de rezervari cu noile informatii legate de ID-ul de rezervare
        # si de zborurile pentru care s-a facut rezervarea
        add_reservation = ("INSERT INTO Reservations "
            "(Reservation_ID, Flights_IDs) VALUES (%s, %s)")
        add_reservation_data = (reservation_id, flights_ids)
        cursor.execute(add_reservation, add_reservation_data)
        connection.commit()

    # Daca nu sunt toate zborurile disponibile, se intoarce sirul vid, conform enuntului
    else:

        reservation_id = ""

    # Se inchide conexiunea la baza de date
    cursor.close()
    connection.close()

    # Se intoarce ID-ul de rezervare corespunzator
    return json.dumps({"Reservation ID" : reservation_id})

# Functie care gesioneaza cumpararea biletelor rezervate anterior prin
# intermediul functiei book_ticket, pe baza ID-ului de rezervare generat,
# dar si a informatiilor legate de cardul bancar primit ca parametru,
# fiind apelata in momentul in care clientul face un request pe ruta
# specificata
@app.route("/buy")
def buy_tickets():

    global cursor

    # Se efectueaza conectarea la baza de date
    connection = mysql.connector.connect(**config)
    cursor = connection.cursor()

    # Se obtin informatiile primite ca parametru prin intermediul cererii GET
    # facuta de client
    buy_data = str(request.args.get("Buy Info"))
    buy_data_list = buy_data.split()

    # Se obtine ID-ul de rezervare corespunzator
    reservation_id = buy_data_list[0]

    # Se obtin ID-urile zborurilor pentru care s-a facut rezervarea
    cursor.execute("SELECT Flights_IDs FROM Reservations WHERE Reservation_ID = %s", (reservation_id, ))
    flights_ids = cursor.fetchone()[0].split()

    boarding_pass = ""

    # Se genereaza boarding pass-ul, format din datele specifice fiecarui zbor
    # pentru care se cumpara biletul
    for flight_id in flights_ids:

            cursor.execute("SELECT * FROM Flights WHERE ID = %s", (flight_id, ))
            results = cursor.fetchone()
            boarding_pass = boarding_pass + str(results) + " "


    # Se inchide conexiunea la baza de date
    cursor.close()
    connection.close()

    # Se intoarce boarding pass-ul generat anterior
    return json.dumps({"Boarding Pass" : boarding_pass})


if __name__ == '__main__':
    app.run(host='0.0.0.0')


