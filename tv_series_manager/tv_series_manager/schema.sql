PRAGMA foreign_keys = ON;

CREATE TABLE users (
  id INTEGER PRIMARY KEY,
  name VARCHAR(128),
  username VARCHAR(64),
  password VARCHAR(64)
);

CREATE TABLE classification (
  id INTEGER PRIMARY KEY,
  initials VARCHAR(10),
  description TEXT
);

CREATE TABLE category (
  id INTEGER PRIMARY KEY,
  name VARCHAR(20),
  description TEXT
);

CREATE TABLE list_series (
  user_id INTEGER,
  classification_id INTEGER,
  serie_id INTEGER,
  FOREIGN KEY(user_id) REFERENCES users(id),
  FOREIGN KEY(classification_id) REFERENCES classification(id),
  FOREIGN KEY(serie_id) REFERENCES serie(id)
);

CREATE TABLE serie (
  id INTEGER PRIMARY KEY,
  name VARCHAR(20),
  start_date DATE,
  synopse TEXT,
  category_id INTEGER,
  FOREIGN KEY(category_id) REFERENCES category(id)
);

CREATE TABLE episode (
  id INTEGER PRIMARY KEY,
  name TEXT,
  decription TEXT,
  serie_id INTEGER,
  FOREIGN KEY(serie_id) REFERENCES serie(id)
);