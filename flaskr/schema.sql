CREATE TABLE test (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT UNIQUE NOT NULL,
    body TEXT NOT NULL,
    created INTEGER NOT NULL
);

CREATE TABLE sheet (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT UNIQUE NOT NULL,
    path TEXT UNIQUE NOT NULL,
    rows INTEGER DEFAULT 0,
    cols INTEGER DEFAULT 0,
    created INTEGER NOT NULL
);

CREATE TABLE run (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    test_id INTEGER NOT NULL,
    created INTEGER NOT NULL,
    results TEXT NOT NULL,
    sheet_id INTEGER NOT NULL,
    FOREIGN KEY (test_id) REFERENCES test (id)
    FOREIGN KEY (sheet_id) REFERENCES sheet (id)
);