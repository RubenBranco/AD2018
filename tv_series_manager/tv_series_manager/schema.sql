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


INSERT INTO classification (id, initials, description) VALUES
  (1, "M", "Mau"),
  (2, "MM", "Mais ou menos"),
  (3, "S", "Suficiente"),
  (4, "B", "Bom"),
  (5, "MB", "Muito bom");

INSERT INTO category (id, name, description) VALUES
  (1, "Ação", "Ação"),
  (2, "Animação", "Animação"),
  (3, "Artes Marciais", "Artes Marciais"),
  (4, "Aventura", "Aventura"),
  (5, "Biografia", "Biografia"),
  (6, "Clássico", "Clássico"),
  (7, "Comédia", "Comédia"),
  (8, "Drama", "Drama"),
  (9, "Ficção científica", "Ficção científica"),
  (10, "Musical", "Musical"),
  (11, "Policial", "Policial"),
  (12, "Romance", "Romance"),
  (13, "Suspense", "Suspense"),
  (14, "Terror", "Terror");
