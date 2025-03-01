import sqlite3

def get_db():
    conn = sqlite3.connect('nba.db')
    conn.row_factory = sqlite3.Row
    return conn

def init_db():

    conn = get_db()
    cursor = conn.cursor()
    
    # Check if tables exist
    cursor.execute("SELECT name FROM sqlite_master WHERE type='table' AND (name='teams' OR name='players' OR name='team_stats' OR name='player_stats')")
    tables = cursor.fetchall()
    
    if len(tables) < 4:
        print("Database may be missing required tables. Please ensure it's properly initialized.")
    
    conn.close()