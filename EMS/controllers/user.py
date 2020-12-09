from flask import Blueprint
from flask import Flask, render_template, request, redirect, url_for, session 
from EMS import db
import re 

bp = Blueprint("user", __name__, url_prefix="/user")

@bp.route("/login")
def login():
    # TODO @bently: Create login
    msg = '' 
    # indicate the desired action to be performed for a given resource.
    if request.method == 'POST' and 'mail' in request.form and 'pwd' in request.form: 
        email = request.form['mail']
        password = request.form['pwd'] 
        cursor = db.get_db().cursor()
        cursor.execute('SELECT * FROM Login_cred WHERE Email = % s AND Pass = % s', (email, password, )) 
        #method returns a single record or None if no more rows are available.
        Login_cred = cursor.fetchone() 
        if Login_cred: 
            session['loggedin'] = True
            session['id'] = Login_cred['id'] 
            session['email'] = Login_cred['mail'] 
            msg = 'Logged in successfully !'
            return render_template('base.html', msg = msg) 
        else: 
            msg = 'Wrong email / password'
    return render_template('login.html', msg = msg) 
  
    return "login"

@bp.route("/register")
def register():
    msg = '' 
    #when inputting the data, to check if it is exist or not 
    if request.method == 'POST' and 'mail' in request.form and 'pwd' in request.form:
        #obtaining value
        password = request.form['pwd'] 
        email = request.form['mail'] 
        cursor = db.get_db().cursor()
        cursor.execute('SELECT * FROM Login_Cred WHERE Email = % s', (email, )) 
        users = cursor.fetchone() 
        if users: 
            msg = 'users already exists !'
        # most basic checks for email 
        elif not re.match(r'[^@]+@[^@]+\.[^@]+', email): 
            msg = 'Invalid email address !'
        elif not email or not password or not email: 
            msg = 'Please fill out the form !'
        else: 
            cursor.execute('INSERT INTO Login_Cred VALUES (NULL, % s, % s)', (email, password, )) 
            db.connection.commit() 
            msg = 'You have successfully registered !'
    elif request.method == 'POST': 
        msg = 'Please fill out the form !'
    return render_template('register.html', msg = msg) 

@bp.route('/logout') 
def logout(): 
    session.pop('loggedin', None) 
    session.pop('id', None) 
    session.pop('email', None) 
    return redirect(url_for('user.register')) 