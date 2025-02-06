import sqlite3

# Connect to the database
conn = sqlite3.connect("baseball_stats.db")
cursor = conn.cursor()

# Delete all data while keeping table structure
cursor.execute("DELETE FROM players;")
cursor.execute("DELETE FROM batting_stats;")
cursor.execute("DELETE FROM pitching_stats;")

# Commit and close
conn.commit()
conn.close()

print("Database has been reset.")
