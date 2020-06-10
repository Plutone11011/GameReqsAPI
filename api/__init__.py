import time, os, sys
from flask import Flask
from api.db import db
from api.views import dml, query
from api.utils import commands


def create_app(test_config=None):
    # create and configure the app
    app = Flask(__name__, instance_relative_config=True)
    app.config.from_mapping(
       DATABASE=os.path.join(app.instance_path, 'flaskr.sqlite'),
    )
    print(app.config['DATABASE'])
    if test_config is None:
        # load the instance config, if it exists, when not testing
        app.config.from_pyfile('config.py', silent=True)
    else:
        # load the test config if passed in
        app.config.from_mapping(test_config)

#    ensure the instance folder exists
    try:
        os.makedirs(app.instance_path)
    except OSError:
        pass

    @app.route('/', methods=['GET'])
    def home():
        return '''<h1>Your PC benchmarking API</h1>
        <p>A prototype API to visualize the best games you can play with your current setup</p>'''

    register_endpoints(app)

    commands.init_app(app)
    return app


def register_endpoints(app):
    app.add_url_rule('/api/v1/games', 'insert_game', dml.insert_game,
                     provide_automatic_options=None, methods=['POST'])
    app.add_url_rule('/api/v1/games', 'get_every_game',
                     query.get_game,provide_automatic_options=None, methods=['GET'])
    app.add_url_rule('/api/v1/games', 'delete_game',
                     dml.delete_game, provide_automatic_options=None, methods=['DELETE'])
