from flask.cli import with_appcontext
import click
from flask import current_app
from flask import Flask, render_template, request, redirect, url_for, session
from flask_mysqldb import MySQL
import MySQLdb.cursors
import mysql.connector as sql

app = Flask(__name__)

mydb = None
mysql = MySQL(app)

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

@app.route('/login', methods =['GET', 'POST']) 
def login(): 
    # indicate the desired action to be performed for a given resource.
    if request.method == 'POST' and 'username' in request.form and 'password' in request.form: 
        username = request.form['username'] 
        password = request.form['pwd'] 
        cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor) 
        cursor.execute('SELECT * FROM users WHERE username = % s AND password = % s', (username, password, )) 
        #method returns a single record or None if no more rows are available.
        users = cursor.fetchone() 
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