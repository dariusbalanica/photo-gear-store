CREATE DATABASE store;
USE store;

CREATE TABLE IF NOT EXISTS Products (
        ProductID INT,
        Name VARCHAR(100),
        Category VARCHAR(100),
        Price FLOAT,
        Stock INT
);

CREATE TABLE IF NOT EXISTS Users (
        UserID INT,
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

