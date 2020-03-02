-- Delete the tables if they exist.
-- Disable foreign key checks, so the tables can
-- be dropped in arbitrary order.
PRAGMA foreign_keys=OFF;

DROP TABLE IF EXISTS customers;
DROP TABLE IF EXISTS pallets;
DROP TABLE IF EXISTS cookies;
DROP TABLE IF EXISTS ingredients;
DROP TABLE IF EXISTS recipes;
DROP TABLE IF EXISTS orders;

PRAGMA foreign_keys=ON;

CREATE TABLE customers (
  name TEXT,
  id TEXT,
  adress TEXT,
  PRIMARY KEY (name)

);

CREATE TABLE pallets (
  id  TEXT DEFAULT (lower(hex(randomblob(16)))),
  blocked boolean NOT NULL,
  customer TEXT NOT NULL,
  date DATE NOT NULL,
  cookie TEXT NOT NULL,

  PRIMARY KEY (id) 

);

CREATE TABLE cookies (
  name TEXT,

  PRIMARY KEY (name)

);

CREATE TABLE ingredients (
  ingredient TEXT,
  
  PRIMARY KEY (ingredient)
);

CREATE TABLE recipes (
  cookie TEXT,
  ingredient TIME,
  quantity TIME NOT NULL,
  unit TIME NOT NULL,
  
  PRIMARY KEY (cookie)
);

DELETE FROM customers;
DELETE FROM pallets;
DELETE FROM ingredients;
DELETE FROM recipes;
DELETE FROM orders;
DELETE FROM cookies;


