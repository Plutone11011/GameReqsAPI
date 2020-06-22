import click, asyncio
from flask.cli import with_appcontext

from api.db import db
from api.steamscraper import request


@click.command('init-db')
@with_appcontext
def init_db_command():
    db.init()
    click.echo('Initialized the database.')


@click.command('init-scraper')
@with_appcontext
def run_spider():
    asyncio.run(request.run_requests())


def init_app(app):
    app.teardown_appcontext(db.close) # commit changes and close db connection after each request
    app.cli.add_command(init_db_command)
    app.cli.add_command(run_spider)