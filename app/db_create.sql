DROP DATABASE IF EXISTS flask_api;
CREATE DATABASE  flask_api;
\c flask_api;
DROP TABLE IF EXISTS users;
CREATE TABLE users (
  id serial NOT NULL,
  email varchar(255)  NOT NULL default '',
  password varchar(255) NOT NULL,
  is_admin boolean NOT NULL);

INSERT INTO users (email, password, is_admin) VALUES ('manu', 'manu', FALSE);
INSERT INTO users (email, password, is_admin) VALUES ('bil', 'bil', FALSE);