import click
from flask.cli import with_appcontext

from api.db import db
from api.steamscraper import scraper
from scrapy.crawler import CrawlerProcess

@click.command('init-db')
@with_appcontext
def init_db_command():
    db.init_db()
    click.echo('Initialized the database.')

@click.command('init-scraper')
@with_appcontext
def run_spider():
    process = CrawlerProcess()

    process.crawl(scraper.SteamSpider)
    process.start() # the script will block here until the crawling is finished

def init_app(app):
    app.teardown_appcontext(db.close_db)
    app.cli.add_command(init_db_command)
    app.cli.add_command(run_spider)