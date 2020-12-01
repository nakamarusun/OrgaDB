from flask.cli import with_appcontext
import click
from flask import current_app
import mysql.connector as sql

mydb = None

def get_db():
    # Gets the mysql db object, reconnecting if its disconnected.
    if not mydb.is_connected():
        mydb.connect()

    return mydb

def init_db_connection(app):
    global mydb

    # Establishes a connection to the sql server from the configuration.
    mydb = sql.connect(
        host=app.config.get('DATABASE_HOST'),
        user=app.config.get('DATABASE_USER'),
        password=app.config.get('DATABASE_PASS'),
        database=app.config.get('DATABASE_NAME')
    )

@click.command("init-db", help="Reinitialize the database table from schema.sql")
@with_appcontext
def init_db():

    # Initializes the database from schema.sql from the terminal.
    init_db(current_app)

    # TODO: Create tables from schema.sql here.
    ###########################################
    ###
    ###
    ###########################################

    click.echo("Done reinitializing the database!")