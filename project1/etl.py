import os
import glob
import psycopg2
import pandas as pd
from sql_queries import *

"""
The Function accepts files in JSON format, reads song details and artist details; 
finally inserts records to songs and artists tables.

Args:
    cur: Database cursor.
    filepath: JSON file's location.

Returns:
    None
"""
def process_song_file(cur, filepath):
    # open song file
    df = pd.read_json(filepath, lines=True)

    # insert song record
    song_data = df.values

    for song in song_data:
        cur.execute(song_table_insert, [song[7], song[8], song[0], song[9], song[5]])
        # insert artist record
        artist_data = [song[0], song[4], song[2], song[1], song[3]]
        cur.execute(artist_table_insert, artist_data)

"""
The Function accepts files in JSON format, reads log details; 
finally inserts records to time, users and songplays tables.

Args:
    cur: Database cursor.
    filepath: JSON file's location.

Returns:
    None
"""
def process_log_file(cur, filepath):
    # open log file
    df = pd.read_json(filepath, lines=True)

    # filter by NextSong action
    df = df[df.page=="NextSong"]

    # convert timestamp column to datetime
    t = pd.to_datetime(df['ts'], unit='ms')
    
    # insert time data records
    time_data = (t.dt.time, t.dt.hour, t.dt.day, t.dt.week, t.dt.month, t.dt.year, t.dt.weekday)
    column_labels = ('start_time', 'hour', 'day', 'week', 'month', 'year', 'weekday')
    time_df = pd.DataFrame.from_dict(dict(zip(column_labels, time_data)))

    for i, row in time_df.iterrows():
        cur.execute(time_table_insert, list(row))

    # load user table
    user_df = df[['userId','firstName', 'lastName', 'gender', 'level']].drop_duplicates('userId')

    # insert user records
    for i, row in user_df.iterrows():
        cur.execute(user_table_insert, row)

    # insert songplay records
    for index, row in df.iterrows():
        
        # get songid and artistid from song and artist tables
        results = cur.execute(song_select, (row.song, row.artist, row.length))
        songid, artistid = results if results else None, None

        # insert songplay record
        songplay_data = (pd.to_datetime(int(row.ts//1000), unit='ms'), row.userId, row.level, songid, artistid, row.sessionId, row.location, row.userAgent)
        cur.execute(songplay_table_insert, songplay_data)

"""
The Function accepts folder path, process each file and pass it to process functions

Args:
    cur: Database cursor.
    conn: db connection.
    filepath: json folder path
    func: process function name

Returns:
    None
"""
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
    conn = psycopg2.connect("host=127.0.0.1 dbname=sparkifydb user=student password=student")
    cur = conn.cursor()

    process_data(cur, conn, filepath='data/song_data', func=process_song_file)
    process_data(cur, conn, filepath='data/log_data', func=process_log_file)

    conn.close()


if __name__ == "__main__":
    main()