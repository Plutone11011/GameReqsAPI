import sqlite3

import click
from flask import current_app, g
from flask.cli import with_appcontext


def get_db():
    if 'db' not in g:
        g.db = sqlite3.connect(
            current_app.config['DATABASE'],
            detect_types=sqlite3.PARSE_DECLTYPES
        )
        g.db.row_factory = sqlite3.Row

    return g.db


def close_db(e=None):
    db = g.pop('db', None)

    if db is not None:
        db.close()



def init_db():
    db = get_db()

    with current_app.open_resource('schema.sql') as f:
        db.executescript(f.read().decode('utf8'))

def insert_db():
    db = get_db()



@click.command('init-db')
@with_appcontext
def init_db_command():
    init_db()
    click.echo('Initialized the database.')

@click.command('insert')
@click.argument('name', nargs=1)
@click.argument('description', nargs=1)
@click.argument('minimum_req', nargs=5)
@click.argument('recommended_req', nargs=5)
@with_appcontext
def insert_db_command(name, description, minimum_req, recommended_req):
    #insert_db()
    click.echo('Name: %s'% name)
    click.echo('Description: %s'% description)
    for req in minimum_req:
        click.echo('Min req: %s'% req)
    for req in recommended_req:
        click.echo('Rec req: %s'% req)


def init_app(app):
    app.teardown_appcontext(close_db)
    app.cli.add_command(init_db_command)
    app.cli.add_command(insert_db_command)