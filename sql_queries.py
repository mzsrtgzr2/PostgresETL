# TABLES
SONGPLAYS = 'songplays'
USERS = 'users'
SONGS = 'songs'
ARTISTS = 'artists'
TIMES = 'time'

# DROP TABLES

_DROP_FORMAT = 'DROP TABLE IF EXISTS {};'

songplay_table_drop = _DROP_FORMAT.format(SONGPLAYS)
user_table_drop = _DROP_FORMAT.format(USERS)
song_table_drop = _DROP_FORMAT.format(SONGS)
artist_table_drop = _DROP_FORMAT.format(ARTISTS)
time_table_drop = _DROP_FORMAT.format(TIMES)

# CREATE TABLES

_CREATE_FORMAT = 'CREATE TABLE IF NOT EXISTS {} ({});'

songplay_table_create = _CREATE_FORMAT.format(
    SONGPLAYS,
    'songplay_id varchar SERIAL NOT NULL, '
    'start_time timestamp NOT NULL, '
    'user_id varchar NOT NULL, '
    'level varchar, '
    'song_id varchar NOT NULL, '
    'artist_id varchar NOT NULL, '
    'session_id varchar NOT NULL, '
    'location varchar, user_agent varchar '
    'PRIMARY KEY (songplay_id)'
)

user_table_create = _CREATE_FORMAT.format(
    USERS,
    'user_id varchar NOT NULL, '
    'first_name varchar NOT NULL, '
    'last_name varchar NOT NULL, '
    'gender char, '
    'level varchar'
    'PRIMARY KEY (user_id)'
)

song_table_create = _CREATE_FORMAT.format(
    SONGS,
    'song_id varchar NOT NULL, title varchar NOT NULL, '
    'artist_id varchar NOT NULL, year int, duration float'
    'PRIMARY KEY (song_id)'
)

artist_table_create = _CREATE_FORMAT.format(
    ARTISTS,
    'artist_id varchar NOT NULL, name varchar NOT NULL, '
    'location varchar, latitude float, longitude float'
    'PRIMARY KEY (artist_id)'
)

time_table_create = _CREATE_FORMAT.format(
    TIMES,
    'start_time timestamp NOT NULL, hour int, day int , '
    'week int, month int, year int, weekday int'
    'PRIMARY KEY (start_time)'
)

# INSERT RECORDS

_INSERT_FORMAT = 'INSERT INTO {} ({}) VALUES ({})'

songplay_table_insert = _INSERT_FORMAT.format(
    SONGPLAYS,
    'start_time, user_id, level, song_id, artist_id, session_id, location, user_agent',
    ','.join(['%s'] * 8)
)

user_table_insert = _INSERT_FORMAT.format(
    USERS,
    'user_id, first_name, last_name, gender, level',
    ','.join(['%s'] * 5)
)

song_table_insert = _INSERT_FORMAT.format(
    SONGS,
    'song_id, title, artist_id, year, duration',
    ','.join(['%s'] * 5)
)

artist_table_insert = _INSERT_FORMAT.format(
    ARTISTS,
    'artist_id, name, location, latitude, longitude',
    ','.join(['%s'] * 5)
)

time_table_insert = _INSERT_FORMAT.format(
    TIMES,
    'start_time, hour, day, week, month, year, weekday',
    ','.join(['%s'] * 7)
)

# FIND SONGS

song_select = (f"""
SELECT song_id, {ARTISTS}.artist_id 
FROM {SONGS} JOIN {ARTISTS} on ({SONGS}.artist_id={ARTISTS}.artist_id) 
WHERE title=%s and name=%s and duration=%s
""")

# QUERY LISTS

create_table_queries = [songplay_table_create, user_table_create, song_table_create, artist_table_create, time_table_create]
drop_table_queries = [songplay_table_drop, user_table_drop, song_table_drop, artist_table_drop, time_table_drop]