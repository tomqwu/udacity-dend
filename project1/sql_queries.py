# DROP TABLES

songplay_table_drop = "DROP TABLE IF EXISTS songplays;"
user_table_drop = "DROP TABLE IF EXISTS users;"
song_table_drop = "DROP TABLE IF EXISTS songs;"
artist_table_drop = "DROP TABLE IF EXISTS artiests;"
time_table_drop = "DROP TABLE IF EXISTS time;"

# CREATE TABLES

songplay_table_create = ("""
CREATE TABLE IF NOT EXISTS songplays ( 
    songplay_id SERIAL PRIMARY KEY,
    start_time TIME,
    user_id INTEGER,
    level TEXT,
    song_id TEXT,
    artist_id TEXT,
    session_id INTEGER,
    location TEXT,
    user_agent TEXT
);
""")

user_table_create = ("""
CREATE TABLE IF NOT EXISTS users (
    user_id INTEGER PRIMARY KEY,
    first_name TEXT,
    last_name TEXT,
    gender TEXT,
    level TEXT
);
""")

song_table_create = ("""
CREATE TABLE IF NOT EXISTS songs (
    song_id TEXT PRIMARY KEY,
    title TEXT,
    artist_id TEXT,
    year INTEGER,
    duration FLOAT8
);
""")

artist_table_create = ("""
CREATE TABLE IF NOT EXISTS artists (
    artist_id TEXT PRIMARY KEY,
    name TEXT,
    location TEXT, 
    lattitude FLOAT8,
    longitude FLOAT8
)
""")

time_table_create = ("""
CREATE TABLE IF NOT EXISTS time (
    start_time TIME,
    hour INTEGER,
    day INTEGER,
    week INTEGER,
    month INTEGER,
    year INTEGER,
    weekday INTEGER
)
""")

# INSERT RECORDS

songplay_table_insert = ("""
INSERT INTO songplays (
    start_time, 
    user_id, 
    level, 
    song_id, 
    artist_id, 
    session_id,
    location, 
    user_agent
)
VALUES (%s, %s, %s, %s, %s, %s, %s, %s)
""")

user_table_insert = ("""
INSERT INTO users (user_id, first_name, last_name, gender, level)
VALUES (%s, %s, %s, %s, %s)
ON CONFLICT ON CONSTRAINT users_pkey
DO NOTHING;
""")

song_table_insert = ("""
INSERT INTO songs (song_id, title, artist_id, year, duration)
VALUES (%s, %s, %s, %s, %s)
ON CONFLICT ON CONSTRAINT songs_pkey
DO NOTHING;
""")

artist_table_insert = ("""
INSERT INTO artists (artist_id, name, location, lattitude, longitude)
VALUES (%s, %s, %s, %s, %s)
ON CONFLICT ON CONSTRAINT artists_pkey
DO NOTHING;
""")


time_table_insert = ("""
INSERT INTO time (start_time, hour, day, week, month, year, weekday)
VALUES (%s, %s, %s, %s, %s, %s, %s)
""")

# FIND SONGS

song_select = ("""
SELECT s.song_id, a.artist_id 
FROM songs as s
LEFT JOIN artists as a
ON a.artist_id = s.artist_id
WHERE title LIKE %s AND name LIKE %s AND duration = %s
""")

# QUERY LISTS

create_table_queries = [songplay_table_create, user_table_create, song_table_create, artist_table_create, time_table_create]
drop_table_queries = [songplay_table_drop, user_table_drop, song_table_drop, artist_table_drop, time_table_drop]