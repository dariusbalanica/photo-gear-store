CREATE DATABASE store;
USE store;

CREATE TABLE IF NOT EXISTS Products (
        ProductID INT,
        Name VARCHAR(100),
        Brand VARCHAR(100),
        Category VARCHAR(100),
        Price FLOAT,
        Stock INT
);

CREATE TABLE IF NOT EXISTS Users (
        UserID INT,
        Name VARCHAR(100),
        Email VARCHAR(100),
        Username VARCHAR(100),
        Password VARCHAR(100)
);

CREATE TABLE IF NOT EXISTS Cart (
        UserID INT,
        ProductID INT,
        Quantity INT,
        BeingOrdered INT
);

CREATE TABLE IF NOT EXISTS Orders (
        OrderID INT,
        UserID INT
);

INSERT INTO Products (ProductID, Name, Brand, Category, Price, Stock)
VALUES (100, "Nikon D5600", "Nikon", "Camere foto", 3599, 50);
INSERT INTO Products (ProductID, Name, Brand, Category, Price, Stock)
VALUES (101, "Nikon D780", "Nikon", "Camere foto", 11399, 20);
INSERT INTO Products (ProductID, Name, Brand, Category, Price, Stock)
VALUES (102, "Fujifilm XT-3", "Fujifilm", "Camere foto", 6999, 40);
INSERT INTO Products (ProductID, Name, Brand, Category, Price, Stock)
VALUES (103, "Sony A7 III", "Sony", "Camere foto", 12499, 15);

INSERT INTO Products (ProductID, Name, Brand, Category, Price, Stock)
VALUES (104, "Nikon AF-S DX Nikkor 16-80mm f/2.8-4E ED VR", "Nikon", "Obiective foto", 5298, 20);
INSERT INTO Products (ProductID, Name, Brand, Category, Price, Stock)
VALUES (105, "Nikon 50mm f/1.4G - Obiectiv AF-S NIKKOR", "Nikon", "Obiective foto", 2399, 30);
INSERT INTO Products (ProductID, Name, Brand, Category, Price, Stock)
VALUES (106, "Sony 24-70mm F2.8 GM Obiectiv Sony FE", "Sony", "Obiective foto", 9999, 23);
INSERT INTO Products (ProductID, Name, Brand, Category, Price, Stock)
VALUES (107, "Sony 10-18mm F4 OSS Obiectiv Sony E", "Sony", "Obiective foto", 3099, 50);
INSERT INTO Products (ProductID, Name, Brand, Category, Price, Stock)
VALUES (108, "Fujifilm 55-200mm F3.5-4.8 R LM OIS XF Obiectiv FujiFilm X", "Fujifilm", "Obiective foto", 3499, 40);

INSERT INTO Products (ProductID, Name, Brand, Category, Price, Stock)
VALUES (109, "Peak Design Everyday Backpack", "Peak Design", "Accesorii foto", 1249, 20);
INSERT INTO Products (ProductID, Name, Brand, Category, Price, Stock)
VALUES (110, "Manfrotto Befree Advanced Carbon Travel", "Manfrotto", "Accesorii foto", 1179, 50);
INSERT INTO Products (ProductID, Name, Brand, Category, Price, Stock)
VALUES (111, "Manfrotto MPMXPROC4 XPRO Monopied Carbon", "Manfrotto", "Accesorii foto", 785, 70);


