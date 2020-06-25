import sqlite3, logging
from flask import current_app, g

from api.db.model import Game
from api.db.QueryBuilder import GameQueryBuilder


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


def insert_game(game: Game):
    cursor = get_cursor()

    t_game = (game.name, game.description, game.developer, game.ram_min,
            game.cpu_min, game.gpu_min, game.OS_min, game.storage_min,
            game.ram_rec, game.cpu_rec, game.gpu_rec, game.OS_rec,
            game.storage_rec)

    cursor.execute('''INSERT INTO Games(name,description,developer,ram_min,cpu_min,
    gpu_min,OS_min,storage_min,ram_rec,cpu_rec,gpu_rec,OS_rec,storage_rec) 
    VALUES(?,?,?,?,?,?,?,?,?,?,?,?,?)''', t_game)

    return cursor.lastrowid


def game_query(*args, **kwargs):
    """ executes query with keyword parameters
        given by url query and picks only columns defined in args"""
    cursor = get_cursor()
    results = []

    game_query_builder = GameQueryBuilder(*args)

    query_functions = {
        'name': game_query_builder.name_query,
        'page': game_query_builder.pagination_query,
        'filters': game_query_builder.filter_query
    }
    for k, v in kwargs.items():
        if v:
            query_functions[k](v)

    cursor.execute(str(game_query_builder.query_builder), tuple(game_query_builder.param_builder()))

    for row in cursor.fetchall():
        results.append(dict(row))
    return results


def update_game(game: Game):
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


def delete_game(id_game: int):
    cursor = get_cursor()

    if id_game:
        logging.warning("Deleting a game resource")
        cursor.execute('DELETE FROM Games WHERE id = ?', (id_game,))
    else:
        logging.warning("Deleting every row")
        cursor.execute('DELETE FROM Games')

    return cursor.rowcount