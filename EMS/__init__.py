from flask import Flask
from EMS import db, controllers
from os import makedirs

# App factory
def create_app(conf:dict=None):
    app = Flask(__name__)
    
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

    return app