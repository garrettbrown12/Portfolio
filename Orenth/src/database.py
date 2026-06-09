import sqlite3
import os
from idlelib import query


def initialize_db():
    #navigates to the project root folder (orenth) even when running from the src folder
    base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    db_path = os.path.join(base_dir, "games.db")

    #connect to the db (create if doesnt exist)
    connection = sqlite3.connect(db_path)
    cursor = connection.cursor()

    #create the 'games' table
    cursor.execute("""
            CREATE TABLE IF NOT EXISTS games (
                   id INTEGER PRIMARY KEY AUTOINCREMENT,
                   name TEXT NOT NULL,
                   vibe TEXT NOT NULL
                )
            """)

    #create the 'stats' table
    cursor.execute("""
                   CREATE TABLE IF NOT EXISTS stats (
                    game_name TEXT PRIMARY KEY,
                    times_played INTEGER DEFAULT 0
                     )
                """)
    connection.commit()
    return connection
    initialize_db()

def get_random_game_by_vibe(connection, vibe):
    cursor = connection.cursor()

    #used '?' as a placeholder to prevent SQL injection
    query = "SELECT name FROM games WHERE vibe = ? ORDER BY RANDOM() LIMIT 1"

    cursor.execute(query, (vibe,))
    result = cursor.fetchone()

    if result:
        return result[0] #returns just the game name
    else:
        return None #returns none if no games found for that vibe

def update_game_stats(connection, game_name):
    cursor = connection.cursor()

    cursor.execute("""
                   INSERT INTO stats (game_name, times_played) VALUES (?, 1)
                   ON CONFLICT (game_name) DO UPDATE SET times_played = times_played + 1
                   """, (game_name,))
    connection.commit()

def add_new_game(connection, game_name, vibe):
    cursor = connection.cursor()
    cursor.execute("INSERT INTO games (name, vibe) VALUES (?, ?)", (game_name, vibe))
    connection.commit()

def get_most_played_by_vibe(connection, vibe):
    cursor = connection.cursor()
    #join games and stats to find the highest count for the given vibe
    query = """
    SELECT g.name
    FROM games g
    JOIN stats s ON g.name = s.game_name
    WHERE g.vibe = ?
    ORDER BY s.times_played DESC 
    LIMIT 1
    """
    cursor.execute(query, (vibe,))
    result = cursor.fetchone()

    if result:
        return result[0] #returns the game name
    return None #returns none if no games or stats exist for that vibe

def reset_database(connection):
    cursor = connection.cursor()
    #drop tables to wipe everything
    cursor.execute("DROP TABLE IF EXISTS games")
    cursor.execute("DROP TABLE IF EXISTS stats")
    connection.commit()
    #re-initialize to recreate empty tables
    initialize_db()