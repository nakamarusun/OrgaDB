from flask import Flask
from EMS import db

# App factory
def create_app(conf:dict=None):
    app = Flask(__name__)
    
    # Load the configuration file if it is passed ^_^
    if conf:
        app.config.from_mapping(conf)

    # Loads the database configuration
    app.config.from_pyfile("db_config.py")

    # Inits the database
    db.init_db_connection(app)

    @app.route("/")
    def index():
        return "bruh"

    return app