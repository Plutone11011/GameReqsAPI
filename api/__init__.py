import time, os
from flask import Flask
from . import db

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

    #ensure the instance folder exists
    try:
        os.makedirs(app.instance_path)
    except OSError:
        pass
    
    db.init_app(app)
    # a simple page that says hello
    @app.route('/', methods=['GET'])
    def home():
        return '''<h1>Your PC benchmarking API</h1>
        <p>A prototype API to visualize the best games you can play with your current setup</p>'''

    return app
