CREATE DATABASE flights;
use flights;

/*
Tabela cu zboruri, in care sunt retinute toate detaliile referitoare la zboruri,
conform enuntului 
 */
CREATE TABLE IF NOT EXISTS Flights (
	ID INT,
	Source VARCHAR(100),
	Destination VARCHAR(100),
	Hour INT,
	Day INT,
	Duration INT,
	Seats INT
);

/*
Tabela utila pentru operatiile de rezervare a zborurilor, in care sunt retinute 
capacitatea zborului si numarul de rezervari pentru un anumit zbor intr-un anumit 
moment de timp
 */
CREATE TABLE IF NOT EXISTS Booking_Capacity(
	Flight_ID INT,
	Flight_Capacity INT,
	Booked_Seats INT
);

/*
Tabela pentru evidenta rezervarilor, in care sunt retinute ID-ul rezervarii si 
un string ce reprezinta Id-urile zborurilor pentru care s-a efectuat rezervarea 
respectiva separate prin spatiu
 */
CREATE TABLE IF NOT EXISTS Reservations (
	Reservation_ID VARCHAR(100),
	Flights_IDs VARCHAR(100)
);

