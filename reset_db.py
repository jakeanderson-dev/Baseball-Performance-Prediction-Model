import sqlite3

# Connect to the database
conn = sqlite3.connect("baseball_stats.db")
cursor = conn.cursor()

# Delete all data while keeping table structure
cursor.execute("DELETE FROM players;")
cursor.execute("DELETE FROM batting_stats;")
cursor.execute("DELETE FROM pitching_stats;")
cursor.execute("DELETE FROM player_urls;")

# Reset the AUTOINCREMENT counters
cursor.execute("DELETE FROM sqlite_sequence WHERE name='players';")
cursor.execute("DELETE FROM sqlite_sequence WHERE name='batting_stats';")
cursor.execute("DELETE FROM sqlite_sequence WHERE name='pitching_stats';")
cursor.execute("DELETE FROM sqlite_sequence WHERE name='player_urls';")

# Commit and close the transaction before running VACUUM
conn.commit()
conn.close()

# Open a new connection for VACUUM (must be outside a transaction)
conn = sqlite3.connect("baseball_stats.db")
cursor = conn.cursor()
cursor.execute("VACUUM;")
conn.close()

print("Database has been reset, and ID sequences have been reset to 1.")


