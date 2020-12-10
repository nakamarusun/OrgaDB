from flask import Blueprint
from flask import Flask, render_template, request, redirect, url_for, session 
from EMS import db
import random
import re 

bp = Blueprint("user", __name__, url_prefix="/user")

@bp.route("/login", methods =['GET', 'POST'])
def login():
    # TODO @bently: Create login
    msg = '' 
    # indicate the desired action to be performed for a given resource.
    print("bruh")
    if request.method == 'POST': 
        email = request.form['mail']
        print(email)
        password = request.form['pwd'] 
        print(password)
        cursor = db.get_db().cursor()
        cursor.execute('SELECT * FROM login_cred WHERE Email = %s AND Pass = %s', (email, password,)) 
        #method returns a single record or None if no more rows are available.
        Login_cred = cursor.fetchone() 
        if Login_cred: 
            session['id'] = Login_cred[1] 
            session['email'] = Login_cred[2] 
            msg = 'Logged in successfully !'
            return render_template('skeleton.html', msg = msg) 
        else: 
            msg = 'Wrong email / password'
    return render_template('login.html', msg = msg) 

@bp.route("/register", methods =['GET', 'POST'])
def register(): 
    msg = '' 
    #when inputting the data, to check if it is exist or not 
    if request.method == 'POST': 
        #obtaining values
        email = request.form['mail']
        password = request.form['pwd'] 
        cursor = db.get_db().cursor()
        cursor.execute('SELECT * FROM login_cred WHERE Email = %s', (email,)) 
        users = cursor.fetchone() 
        print(users)
        if users: 
            msg = 'users already exists !'
        # most basic checks for email 
        elif not re.match(r'[^@]+@[^@]+\.[^@]+', email): 
            msg = 'Invalid email address !'
        elif not email or not password : 
            msg = 'Please fill out the form !'
        else: 
            id = random.randint(0,9999)
            cursor.execute('INSERT INTO login_cred (Id, Pass, Email) VALUES (%s, %s, %s)', (id, password, email,)) 
            db.get_db().commit() 
            msg = 'You have successfully registered !'
    elif request.method == 'POST': 
        msg = 'Please fill out the form !'
    return render_template('register.html', msg = msg) 

@bp.route('/logout') 
def logout(): 
    session.pop('loggedin', None) 
    session.pop('id', None) 
    session.pop('email', None) 
    return redirect(url_for('login')) 
