import sqlite3, logging
from flask import current_app, g

from api.utils.utils import SQL_OPERATOR_URI_MAPPER
from api.db.model import Game


def get():
    if 'db' not in g:
        try:
            g.db = sqlite3.connect(current_app.config['DATABASE'], detect_types=sqlite3.PARSE_DECLTYPES)
        except sqlite3.Error as e:
            logging.critical('Connection error: ' + e)
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


def insert(game: Game):
    cursor = get_cursor()

    t_game = (game.name, game.description, game.developer, game.ram_min,
            game.cpu_min, game.gpu_min, game.OS_min, game.storage_min,
            game.ram_rec, game.cpu_rec, game.gpu_rec, game.OS_rec,
            game.storage_rec)

    cursor.execute('''INSERT INTO Games(name,description,developer,ram_min,cpu_min,
    gpu_min,OS_min,storage_min,ram_rec,cpu_rec,gpu_rec,OS_rec,storage_rec) 
    VALUES(?,?,?,?,?,?,?,?,?,?,?,?,?)''', t_game)

    return cursor.lastrowid


def query_where_clause_filter(filter_parameters):
    """ returns where clause of filtered query,
    handling both storage and ram in memory string """
    params = []

    query_string = 'WHERE '
    for i, filter_params in enumerate(filter_parameters):

        if i != len(filter_parameters) - 1:
            query_string += f'{str(filter_params.memory)} {SQL_OPERATOR_URI_MAPPER[filter_params.op]} ? AND '
        else:
            query_string += f'{str(filter_params.memory)} {SQL_OPERATOR_URI_MAPPER[filter_params.op]} ?'
        params.append(str(filter_params.value))

    return query_string, tuple(params)


def execute_query(*args, **kwargs):
    """ executes query with keyword parameters
        given by url query and picks only columns defined in args"""
    cursor = get_cursor()
    results = []

    if not args:
        query_string = 'SELECT * FROM Games '
    else:
        if len(args) == 3:
            query_string = f'SELECT id, {args[0]}, {args[1]}, {args[2]} FROM Games '
        elif len(args) == 5:
            query_string = f'SELECT id, {args[0]}, {args[1]}, {args[2]}, {args[3]}, {args[4]} FROM Games '
        else:
            query_string = 'SELECT * FROM Games '

    params_values = []
    if not kwargs:
        cursor.execute(query_string)
    else:
        if kwargs.get('name'):
            query_string += ' WHERE name = ?'
            params_values.append(kwargs.get('name'))
        else:
            if kwargs.get('filter_parameters'):
                query_s, params = query_where_clause_filter(kwargs.get('filter_parameters'))
                query_string += query_s
                for param in params:
                    params_values.append(param)
            if (kwargs.get('last_id') or kwargs.get('last_id') == 0) and (
                    kwargs.get('limit') or kwargs.get('limit') == 0):
                if not kwargs.get('filter_parameters'):
                    query_string += 'WHERE id > ? ORDER BY id LIMIT ?'
                else:
                    query_string += ' AND id > ? ORDER BY id LIMIT ?'
                params_values.append(kwargs.get('last_id'))
                params_values.append(kwargs.get('limit'))

        cursor.execute(query_string, tuple(params_values))

    for row in cursor.fetchall():
        results.append(dict(row))
    return results


def update(game: Game):
    cursor = get_cursor()

    t_game = (game.name, game.description, game.developer, game.ram_min,
              game.cpu_min, game.gpu_min, game.OS_min, game.storage_min,
              game.ram_rec, game.cpu_rec, game.gpu_rec, game.OS_rec,
              game.storage_rec, game.id_game)

    cursor.execute('''UPDATE Games SET name = ?, description = ?, developer = ?, 
                    ram_min = ?, cpu_min = ?, gpu_min = ?, OS_min = ?, storage_min = ?,
                    ram_rec = ?, cpu_rec = ?, gpu_rec = ?, OS_rec = ?, storage_rec = ?
                    WHERE id = ?''', t_game)
    return cursor.rowcount


def delete():
    cursor = get_cursor()

    logging.warning("Deleting every row")
    cursor.execute('DELETE FROM Games')

    return cursor.rowcount

def delete_game(id_game: int):
    cursor = get_cursor()

    logging.warning("Deleting a game")
    cursor.execute('DELETE FROM Games WHERE id = ?', (id_game,))

    return cursor.rowcount