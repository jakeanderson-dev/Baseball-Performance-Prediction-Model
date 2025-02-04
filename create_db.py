import sqlite3

def create_database():
    conn = sqlite3.connect("baseball_stats.db")
    cursor = conn.cursor()
    
    # Create players table
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS players (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT UNIQUE,
            position TEXT,
            bats TEXT,
            throws TEXT,
            height_inches INTEGER,
            weight_lbs INTEGER
        )
    ''')
    
    # Create batting stats table
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS batting_stats (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            player_id INTEGER,
            season TEXT,
            age INTEGER,
            team TEXT,
            league TEXT,
            war REAL,
            g INTEGER,
            pa INTEGER,
            ab INTEGER,
            r INTEGER,
            h INTEGER,
            doubles INTEGER,
            triples INTEGER,
            hr INTEGER,
            rbi INTEGER,
            sb INTEGER,
            cs INTEGER,
            bb INTEGER,
            so INTEGER,
            ba REAL,
            obp REAL,
            slg REAL,
            ops REAL,
            ops_plus INTEGER,
            roba REAL,
            rbat_plus REAL,
            tb INTEGER,
            gidp INTEGER,
            hbp INTEGER,
            sh INTEGER,
            sf INTEGER,
            ibb INTEGER,
            position_played TEXT,
            awards TEXT,
            FOREIGN KEY (player_id) REFERENCES players(id)
        )
    ''')
    
    # Create pitching stats table
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS pitching_stats (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            player_id INTEGER,
            season TEXT,
            age INTEGER,
            team TEXT,
            league TEXT,
            war REAL,
            w INTEGER,
            l INTEGER,
            win_loss_pct REAL,
            era REAL,
            g INTEGER,
            gs INTEGER,
            gf INTEGER,
            cg INTEGER,
            sho INTEGER,
            sv INTEGER,
            ip REAL,
            h INTEGER,
            r INTEGER,
            er INTEGER,
            hr INTEGER,
            bb INTEGER,
            ibb INTEGER,
            so INTEGER,
            hbp INTEGER,
            bk INTEGER,
            wp INTEGER,
            bf INTEGER,
            era_plus INTEGER,
            fip REAL,
            whip REAL,
            h9 REAL,
            hr9 REAL,
            bb9 REAL,
            so9 REAL,
            so_bb_ratio REAL,
            awards TEXT,
            FOREIGN KEY (player_id) REFERENCES players(id)
        )
    ''')
    
    conn.commit()
    conn.close()
    print("Database and tables created successfully.")

if __name__ == "__main__":
    create_database()

