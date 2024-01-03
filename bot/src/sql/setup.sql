CREATE TABLE IF NOT EXISTS Users (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    username TEXT NOT NULL UNIQUE,
)
CREATE TABLE IF NOT EXISTS Games (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    width INTEGER NOT NULL,
    height INTEGER NOT NULL,
    player1 INTEGER NOT NULL,
    player2 INTEGER NOT NULL,
    winner INTEGER,
    message1_id INTEGER,
    message2_id INTEGER,
    board TEXT NOT NULL,
    FOREIGN KEY (player1) REFERENCES Users(id),
    FOREIGN KEY (player2) REFERENCES Users(id),

)
