from flask import Blueprint
from flask import Flask, render_template, request, redirect, url_for, session 
from EMS import db
from werkzeug.security import (check_password_hash, generate_password_hash)
import random
import re 

bp = Blueprint("user", __name__, url_prefix="/user")

@bp.route("/login", methods =['GET', 'POST'])
def login():
    msg = '' 
    # indicate the desired action to be performed for a given resource.
    if request.method == 'POST': 
        email = request.form['mail'] 
        password = request.form['pwd'] 
        cursor = db.get_db().cursor()

        # Gets the email and password pair from the database.
        cursor.execute('SELECT * FROM login_cred WHERE Email = %s ', (email, )) 

        #method returns a single record or None if no more rows are available.
        users = cursor.fetchone() 
        if users:
            # Sets the internal session variables
            session['loggedin'] = True
            session['id'] = users[0]
            session['email'] = users[2]
            session['user_name'] = users[3]
            msg = 'Logged in successfully !'

            pass_hash = users[1]
    
            if check_password_hash(pass_hash, password):
                return redirect(url_for('index.index'))
            else:
                return redirect(url_for('user.login'))
        else:
            return redirect(url_for('user.login'))
    else:
        return render_template('login.html')

@bp.route("/register", methods =['GET', 'POST'])
def register(): 
    msg = '' 
    # when inputting the data, to check if it is exist or not 
    if request.method == 'POST': 
        # obtaining values
        email = request.form['mail']
        password = request.form['pwd']
        username = request.form['name']
        cursor = db.get_db().cursor()

        # Checks whether the email already exists in the database.
        cursor.execute('SELECT * FROM login_cred WHERE Email = %s', (email,)) 
        users = cursor.fetchone()
        if users: 
            msg = 'users already exists !'
        # most basic checks for email 
        elif not re.match(r'[^@]+@[^@]+\.[^@]+', email): 
            msg = 'Invalid email address !'
        elif not email or not password or not username: 
            msg = 'Please fill out the form !'
        else: 
            hash = generate_password_hash(password, salt_length=20)
            cursor.execute(" INSERT INTO login_cred (Pass, Email, Username) VALUES ('{}', '{}', '{}') ".format(
                hash,
                str(email),
                username))
            db.get_db().commit() 
            return redirect(url_for('user.login'))

    return render_template('register.html')

@bp.route('/logout') 
def logout(): 
    # Logs out the user from the session
    # By popping from the variables
    session.pop('loggedin', None) 
    session.pop('user_name', None)
    session.pop('id', None) 
    session.pop('email', None) 
    return redirect(url_for('index.index')) 

@bp.route("/<string:id>/profile")
def profile_page(id):

    # TODO: Add /user/<id>/profile
    return " User profile: " + id
