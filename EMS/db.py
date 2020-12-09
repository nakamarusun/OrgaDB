from flask.cli import with_appcontext
import click
from flask import current_app
from flask import Flask, render_template, request, redirect, url_for, session
import mysql.connector as sql


mydb = None

def get_db():
    # Gets the mysql db object, reconnecting if its disconnected.
    if not mydb.is_connected():
        mydb.connect()

    return mydb

def init_db_connection(app):
    global mydb

    app.cli.add_command(init_db)
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

    #same as cursor = mysql.connect, but instead calling the function and called as cursor
    with get_db().cursor() as cursor:
        # Creates the table here
        # use datase name 
        with current_app.open_resource("schema.sql", "rt") as file:
            #loop and run, after ";"
            for line in file.read().split(";"):

                string = line.strip().replace("\n", " ")
                cursor.execute(string)    

    click.echo("Done reinitializing the database!")