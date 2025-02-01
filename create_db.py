import sqlite3
import os

# Remove existing database file if it exists
db_file = "player_stats.db"
if os.path.exists(db_file):
    os.remove(db_file)
    print("Old database deleted.")

# Connect to SQLite and create tables
conn = sqlite3.connect(db_file)
cursor = conn.cursor()

# Create table for player metadata
cursor.execute('''
    CREATE TABLE players (
        player_id INTEGER PRIMARY KEY AUTOINCREMENT,
        player_name TEXT UNIQUE,
        position TEXT,
        teams TEXT
    )
''')

# Create table for batters (renamed from hitters)
cursor.execute('''
    CREATE TABLE batters (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        player_id INTEGER,
        season TEXT,
        age INTEGER,
        team TEXT,
        league TEXT,
        war REAL,
        games INTEGER,
        plate_appearances INTEGER,
        at_bats INTEGER,
        runs INTEGER,
        hits INTEGER,
        doubles INTEGER,
        triples INTEGER,
        home_runs INTEGER,
        rbi INTEGER,
        stolen_bases INTEGER,
        caught_stealing INTEGER,
        walks INTEGER,
        strikeouts INTEGER,
        batting_avg REAL,
        obp REAL,
        slg REAL,
        ops REAL,
        ops_plus INTEGER,
        rOBA REAL,
        rbat_plus REAL,
        total_bases INTEGER,
        gidp INTEGER,
        hbp INTEGER,
        sacrifice_hits INTEGER,
        sacrifice_flies INTEGER,
        intentional_walks INTEGER,
        awards TEXT,
        FOREIGN KEY (player_id) REFERENCES players (player_id)
    )
''')

# Create table for pitchers
cursor.execute('''
    CREATE TABLE pitchers (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        player_id INTEGER,
        season TEXT,
        age INTEGER,
        team TEXT,
        league TEXT,
        war REAL,
        wins INTEGER,
        losses INTEGER,
        win_loss_perc REAL,
        games INTEGER,
        games_started INTEGER,
        complete_games INTEGER,
        shutouts INTEGER,
        saves INTEGER,
        innings_pitched REAL,
        hits_allowed INTEGER,
        runs_allowed INTEGER,
        earned_runs INTEGER,
        home_runs_allowed INTEGER,
        walks INTEGER,
        strikeouts INTEGER,
        era REAL,
        whip REAL,
        era_plus INTEGER,
        fip REAL,
        hr9 REAL,
        bb9 REAL,
        so9 REAL,
        so_w_ratio REAL,
        awards TEXT,
        FOREIGN KEY (player_id) REFERENCES players (player_id)
    )
''')

# Commit changes and close connection
conn.commit()
conn.close()

print("New database with players, batters, and pitchers tables created successfully!")


