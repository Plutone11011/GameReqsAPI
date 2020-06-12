import sqlite3
from flask import current_app, g

from api.utils.GameEnum import GameEnum
from api.utils.utils import convert_numeric_string, SQL_OPERATOR_URI_MAPPER


def get():
    if 'db' not in g:
        try:
            g.db = sqlite3.connect(current_app.config['DATABASE'], detect_types=sqlite3.PARSE_DECLTYPES)
        except sqlite3.Error as e:
            print('Connection error: ' + e)
#            send user a notification
        g.db.row_factory = sqlite3.Row

    return g.db


def close(e=None):
    db = g.pop('db', None)

    if db is not None:
        db.commit()
        db.close()


def get_cursor():
    db = get()
    return db.cursor()
    

def init():
    db = get()

    with current_app.open_resource('db/schema.sql') as f:
        db.executescript(f.read().decode('utf8'))


def insert(game :tuple):
    cursor = get_cursor()

    mutable_game = list(game)
    ram_min_num = convert_numeric_string(mutable_game[GameEnum.RAM_MIN])
    storage_min_num = convert_numeric_string(mutable_game[GameEnum.STORAGE_MIN])
    ram_rec_num = convert_numeric_string(mutable_game[GameEnum.RAM_REC])
    storage_rec_num = convert_numeric_string(mutable_game[GameEnum.STORAGE_REC])

    mutable_game[GameEnum.RAM_MIN] = ram_min_num
    mutable_game[GameEnum.STORAGE_MIN] = storage_min_num
    mutable_game[GameEnum.RAM_REC] = ram_rec_num
    mutable_game[GameEnum.STORAGE_REC] = storage_rec_num

    cursor.execute('''INSERT INTO Games(name,description,developer,ram_min,cpu_min,
    gpu_min,OS_min,storage_min,ram_rec,cpu_rec,gpu_rec,OS_rec,storage_rec) 
    VALUES(?,?,?,?,?,?,?,?,?,?,?,?,?)''', tuple(mutable_game))

    return cursor.lastrowid


def readall():
    cursor = get_cursor()
    results = []

    cursor.execute('SELECT * FROM Games')
    for row in cursor.fetchall():
        results.append(tuple(row))

    return results


def read_paginated(limit: int, last_id: int):
    cursor = get_cursor()
    results = []

    cursor.execute('SELECT * FROM Games WHERE id > ? ORDER BY id LIMIT ?', (last_id, limit))
    for row in cursor.fetchall():
        results.append(tuple(row))

    return results


def read_filtered_by_memory(filter_parameters):
    # handles both storage and ram in memory string
    cursor = get_cursor()
    results = []
    params = []

    query_string = 'SELECT * FROM Games WHERE '
    for i, filter_params in enumerate(filter_parameters):

        if i != len(filter_parameters) - 1:
            query_string += f'{str(filter_params.get("memory"))} {SQL_OPERATOR_URI_MAPPER[filter_params.get("op")]} ? AND '
        else:
            query_string += f'{str(filter_params.get("memory"))} {SQL_OPERATOR_URI_MAPPER[filter_params.get("op")]} ?'
        print(query_string)
        params.append(str(filter_params.get("value")))

    print()
    cursor.execute(query_string, tuple(params))

    for row in cursor.fetchall():
        results.append(tuple(row))

    return results


def deleteall():
    cursor = get_cursor()

    cursor.execute('DELETE FROM Games')

    return cursor.rowcount
