import sqlite3

import click
from flask import current_app, g
from flask.cli import with_appcontext


def get_db():
    if 'db' not in g:
        try:
            g.db = sqlite3.connect(
            current_app.config['DATABASE'],
            detect_types=sqlite3.PARSE_DECLTYPES
            )
        except sqlite3.Error as e:
            print('Connection error: ' + e)
            #send user a notification
        g.db.row_factory = sqlite3.Row

    return g.db


def close_db(e=None):
    db = g.pop('db', None)

    if db is not None:
        db.commit()
        db.close()


def get_cursor():
    db = get_db()
    return db.cursor()
    

def init_db():
    db = get_db()

    with current_app.open_resource('schema.sql') as f:
        db.executescript(f.read().decode('utf8'))

def insert_db(game :tuple):
    cursor = get_cursor()

    cursor.execute('''INSERT INTO Games(name,description, genre,developer,ram_min,cpu_min,
    gpu_min,OS_min,storage_min,ram_rec,cpu_rec,gpu_rec,OS_rec,storage_rec) 
    VALUES(?,?,?,?,?,?,?,?,?,?,?,?,?,?)''', game)


    return cursor.lastrowid

def readall_db():
    cursor = get_cursor()
    results = []

    cursor.execute('SELECT * FROM Games')
    for row in cursor.fetchall():
        results.append(tuple(row))

    return results

def deleteall_db():
    cursor = get_cursor()

    cursor.execute('DELETE FROM Games')

    return cursor.rowcount

@click.command('init-db')
@with_appcontext
def init_db_command():
    init_db()
    click.echo('Initialized the database.')


def init_app(app):
    app.teardown_appcontext(close_db)
    app.cli.add_command(init_db_command)