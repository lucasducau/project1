CREATE TABLE reviews (
    id SERIAL PRIMARY KEY,
    dateandtime TIMESTAMP NOT NULL,
    isbn VARCHAR NOT NULL REFERENCES books,
    user_id INTEGER NOT NULL REFERENCES users,
    review_text VARCHAR NOT NULL

);

CREATE TABLE users(
  user_id SERIAL PRIMARY KEY,
  username VARCHAR NOT NULL UNIQUE,
  password VARCHAR NOT NULL
);

CREATE TABLE books (
  isbn PRIMARY KEY UNIQUE NOT NULL,
  title VARCHAR NOT NULL
  author VARCHAR NOT NULL,
  year INTEGER NOT NULL
);
