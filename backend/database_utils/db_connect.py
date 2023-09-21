# Imports
import psycopg2

# Connecting to database
conn = psycopg2.connect(
    host="localhost", database="triple_db", user="postgres", password="password"
)

# Create a new database session and return a connection object
cur = conn.cursor()

# Create table
cur.execute(
    """
CREATE TABLE player_data (
    id SERIAL PRIMARY KEY,
    PlayerName VARCHAR(255),
    GamesPlayed INT,
    MinutesPlayed INT,
    Points INT,
    Rebounds INT,
    Assists INT,
    Steals INT,
    Blocks INT,
    Turnovers INT,
    FieldGoals INT,
    FieldGoalAttempts INT,
    FreeThrows INT,
    FreeThrowAttempts INT
);
"""
)

conn.commit()
cur.close()
conn.close()
