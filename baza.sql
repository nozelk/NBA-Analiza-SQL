CREATE TABLE IF NOT EXISTS players (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT NOT NULL UNIQUE,
    first_year INTEGER NOT NULL,
    last_year INTEGER NOT NULL,
    image_path TEXT NOT NULL
);

CREATE TABLE IF NOT EXISTS player_stats (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    player_id INTEGER NOT NULL,
    year INTEGER NOT NULL,
    FGM REAL,
    FGA REAL,
    FG_percent REAL,
    FTM REAL,
    FTA REAL,
    FT_percent REAL,
    FG3M REAL,
    FG3A REAL,
    FG3_percent REAL,
    OREB REAL,
    DREB REAL,
    REB REAL, 
    AST REAL, 
    PF REAL,  
    STL REAL, 
    TOV REAL, 
    BLK REAL, 
    PTS REAL, 
    SALARY INTEGER,
    FOREIGN KEY (player_id) REFERENCES players(id)
);

CREATE TABLE IF NOT EXISTS teams (
    id INTEGER PRIMARY KEY,
    full_name TEXT NOT NULL UNIQUE,
    logo_path TEXT NOT NULL,
    abbreviation TEXT,
    city TEXT,
    state TEXT,
    year_founded INTEGER
);


CREATE TABLE IF NOT EXISTS team_stats (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    team_id INTEGER NOT NULL,
    year INTEGER NOT NULL,
    WIN_percent REAL,
    FGM REAL,
    FGA REAL,
    FG_percent REAL,
    FTM REAL,
    FTA REAL,
    FT_percent REAL,
    FG3M REAL,
    FG3A REAL,
    FG3_percent REAL,
    OREB REAL,
    DREB REAL,
    REB REAL,
    AST REAL,
    PF REAL,
    STL REAL,
    TOV REAL,
    BLK REAL,
    PTS REAL,
    payroll INTEGER,       
    payroll_rank INTEGER,  
    FOREIGN KEY (team_id) REFERENCES teams(id)
);

CREATE TABLE IF NOT EXISTS salaries (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    player_id INTEGER NOT NULL,
    team_id INTEGER NOT NULL,
    year INTEGER NOT NULL,
    salary INTEGER NOT NULL,
    FOREIGN KEY (player_id) REFERENCES players(id),
    FOREIGN KEY (team_id) REFERENCES teams(id)
);