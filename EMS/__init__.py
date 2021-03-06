from flask import Flask, session
from flask.helpers import url_for
from werkzeug.utils import redirect
from EMS import db, controllers, cache
from os import makedirs

# App factory
def create_app(conf:dict=None):
    app = Flask(__name__)
    app.secret_key = "EMSisThePog"
    # Load the configuration file if it is passed ^_^
    if conf: app.config.from_mapping(conf)

    # Loads the database configuration
    app.config.from_pyfile("db_config.py")

    # Inits the database
    db.init_db_connection(app)

    # Initializes all the instance folder
    try:
        makedirs(app.instance_path)
    except OSError:
        pass

    # Registers all the routes
    controllers.register_all_routes(app)

    # Initialize uncache
    cache.reg_static_uncache(app)
    
    return app