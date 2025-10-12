DROP TABLE IF EXISTS users;
DROP TABLE IF EXISTS grades;

CREATE TABLE users (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    username TEXT UNIQUE NOT NULL,
    password TEXT NOT NULL
);

CREATE TABLE grades (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    user_id INTEGER NOT NULL,
    course TEXT NOT NULL,
    grade INTEGER NOT NULL,
    FOREIGN KEY(user_id) REFERENCES users(id)
);

INSERT INTO users (username, password)
VALUES ('admin', '$2y$12$n49z0KWISMuMBwS1U54U5OnAPQum8F.UCSu5KwlxpGFoI6SxWRlXa');

INSERT INTO grades (user_id, course, grade) VALUES
(1, 'Mathematics I', 12),
(1, 'Data Structures', 14),
(1, 'Operating Systems', 9),
(1, 'Computer Networks', 16);
