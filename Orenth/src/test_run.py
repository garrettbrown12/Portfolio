from unittest import result

from src.database import initialize_db, get_random_game_by_vibe, update_game_stats

conn = initialize_db()
cursor = conn.cursor()

cursor.execute("INSERT INTO games (name, vibe)VALUES (? , ?)",("Marvel Rivals", "exciting"))
conn.commit()

result = get_random_game_by_vibe(conn, "exciting"), update_game_stats(conn, "Marvel Rivals")

print(result)

cursor.execute("SELECT * FROM stats")

rows = cursor.fetchall()

print("\n--- Current Database Contents ---")
for row in rows:
    print(f"Game: {row[0]} | Times Played: {row[1]}")

conn.close()