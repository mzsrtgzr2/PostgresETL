import os
import glob
import psycopg2
import pandas as pd
from datetime import datetime
from sql_queries import *

from consts import (
    POSTGRES_CONNECTION_STR_DB)


def process_song_file(cur, filepath):
    """
    This function reads JSON files and read information of song
    and artist data and saves into song_data and artist_data
    Arguments:
    cur: Database Cursor
    filepath: location of JSON files
    Return: None
    """
    # open song file
    df = pd.read_json(filepath, lines=True)

    # insert song record
    song_data = df[['song_id', 'title', 'artist_id', 'year', 'duration']].values[0]
    cur.execute(song_table_insert, song_data)
    print(song_data)
    
    # insert artist record
    artist_data = df[[
        'artist_id', 'artist_name', 'artist_location', 'artist_latitude', 
        'artist_longitude']].values[0]
    cur.execute(artist_table_insert, artist_data)


def process_log_file(cur, filepath):
    """
    This function reads Log files and reads information of time, 
    user and songplay data and saves into time, user, songplay
    Arguments:
    cur: Database Cursor
    filepath: location of Log files
    Return: None
    """
    # open log file
    df = pd.read_json(filepath, lines=True)

    # filter by NextSong action
    df = df[df.page == 'NextSong']

    # convert timestamp column to datetime
    t = pd.to_datetime(df['ts'], unit='ms')
    
    # insert time data records
    time_data = tuple(
        zip(
            t, t.dt.hour.values, 
            t.dt.day.values, t.dt.weekofyear.values, 
            t.dt.month.values, t.dt.year.values, 
            t.dt.weekday.values)
    )
    column_labels = ('start_time,hour,day,week_of_year,month,year,weekday'.split(','))
    
    time_df = pd.DataFrame(time_data, columns=column_labels)

    for i, row in time_df.iterrows():
        cur.execute(time_table_insert, list(row))

    # load user table
    user_df = df[['userId', 'firstName', 'lastName', 'gender', 'level']]

    # insert user records
    for i, row in user_df.iterrows():
        cur.execute(user_table_insert, row)

    # insert songplay records
    for index, row in df.iterrows():
        
        # get songid and artistid from song and artist tables
        cur.execute(song_select, (row.song, row.artist, row.length))
        results = cur.fetchone()
        
        if results:
            songid, artistid = results
        else:
            songid, artistid = None, None

        # insert songplay record
        songplay_data = (
            datetime.fromtimestamp(row.ts/1000), row.userId, 
            row.level, songid, artistid, 
            row.sessionId, row.location, row.userAgent
        ) 
        cur.execute(songplay_table_insert, songplay_data)


def process_data(cur, conn, filepath, func):
    # get all files matching extension from directory
    all_files = []
    for root, dirs, files in os.walk(filepath):
        files = glob.glob(os.path.join(root,'*.json'))
        for f in files :
            all_files.append(os.path.abspath(f))

    # get total number of files found
    num_files = len(all_files)
    print('{} files found in {}'.format(num_files, filepath))

    # iterate over files and process
    for i, datafile in enumerate(all_files, 1):
        func(cur, datafile)
        conn.commit()
        print('{}/{} files processed.'.format(i, num_files))


def main():
    conn = psycopg2.connect(POSTGRES_CONNECTION_STR_DB.format('sparkifydb'))
    cur = conn.cursor()

    process_data(cur, conn, filepath='data/song_data', func=process_song_file)
    process_data(cur, conn, filepath='data/log_data', func=process_log_file)

    conn.close()


if __name__ == "__main__":
    main()
