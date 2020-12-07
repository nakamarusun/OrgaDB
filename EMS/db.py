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
    msg = '' 
    # indicate the desired action to be performed for a given resource.
    if request.method == 'POST' and 'email' in request.form and 'password' in request.form: 
        email = request.form['mail']
        password = request.form['pwd'] 
        cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor) 
        cursor.execute('SELECT * FROM Login_cred WHERE email = % s AND password = % s', (email, password, )) 
        #method returns a single record or None if no more rows are available.
        Login_cred = cursor.fetchone() 
        if Login_cred: 
            session['loggedin'] = True
            session['id'] = Login_cred['id'] 
            session['email'] = Login_cred['mail'] 
            msg = 'Logged in successfully !'
            return render_template('home.html', msg = msg) 
        else: 
            msg = 'Wrong email / password'
    return render_template('base.html', msg = msg) 
  
@app.route('/logout') 
def logout(): 
    session.pop('loggedin', None) 
    session.pop('id', None) 
    session.pop('email', None) 
    return redirect(url_for('login')) 




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