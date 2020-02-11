-- Delete the tables if they exist.
-- Disable foreign key checks, so the tables can
-- be dropped in arbitrary order.
PRAGMA foreign_keys=OFF;

DROP TABLE IF EXISTS customers;
DROP TABLE IF EXISTS tickets;
DROP TABLE IF EXISTS theaters;
DROP TABLE IF EXISTS movies;
DROP TABLE IF EXISTS performances;

PRAGMA foreign_keys=ON;

CREATE TABLE customers (
  username varchar(255),
  c_name varchar(255),
  password varchar(255),
  PRIMARY KEY (username)
 
);

CREATE TABLE tickets (
  id  TEXT DEFAULT (lower(hex(randomblob(16)))),
  performance_nbr int NOT NULL,
  username varchar(255) NOT NULL,

  PRIMARY KEY (id),
  FOREIGN KEY (performance_nbr) references performances(performance_nbr),
  FOREIGN KEY (username) references customers(username)
 
);

CREATE TABLE theaters (
  t_name varchar(255),
  capacity int,
  PRIMARY KEY (t_name)
  
);

CREATE TABLE movies (
  imdb_nbr varchar(255),
  title varchar(255),
  p_year int,
  PRIMARY KEY (imdb_nbr)
);

CREATE TABLE performances (
  performance_nbr iNT DEFAULT (lower(hex(randomblob(16)))),
  start_time TIME(0),
  imdb_nbr varchar(255) NOT NULL, 
  t_name varchar(255) NOT NULL,
  start_date DATE(0) NOT NULL,
  PRIMARY KEY (performance_nbr),
  FOREIGN KEY (imdb_nbr) references movies(imdb_nbr), 
  FOREIGN KEY (t_name) references theaters(t_name)
);



INSERT INTO customers
VALUES 
('alice', 'Alice', 'dobido'),
('bob', 'Bob', 'whatsinaname');

INSERT INTO theaters
VALUES
('Kino', 10),
('Södran', 16),
('Scandia', 100); 

INSERT INTO movies
VALUES 
('tt5580390', 'The shape of water', 2017),
('tt4975722', 'Moonlight', 2016),
('tt1895587', 'Spotlight', 2015),
('tt2562232', 'Birdman', 2014);








