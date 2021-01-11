from flask import Blueprint
from flask import Flask, render_template, request, redirect, url_for, session, flash
from EMS import db
from werkzeug.security import (check_password_hash, generate_password_hash)
import functools
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
        users = cursor.fetchall() 
        if users:
            # Gets the first row
            users = users[0]
            # Sets the internal session variables
            session['loggedin'] = True
            session['id'] = users[0]
            session['email'] = users[2]
            session['user_name'] = users[3]
            session['isadmin'] = users[4]
            session['member_id'] = users[5]

            # Sets an empty dictionary of clearances
            session['clearance'] = {}

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
        full_name = request.form['fullName']

        db_ref = db.get_db()
        cursor = db_ref.cursor()

        # Checks whether the email already exists in the database.
        cursor.execute('SELECT * FROM login_cred WHERE Email = %s', (email,)) 
        users = cursor.fetchall()
        if users: 
            msg = 'users already exists !'
        # most basic checks for email 
        elif not re.match(r'[^@]+@[^@]+\.[^@]+', email): 
            msg = 'Invalid email address !'
        elif not email or not password or not username: 
            msg = 'Please fill out the form !'
        else: 
            
            # Gets the maximum id number, then make a new id based on that.
            cursor.execute("SELECT MAX(Id) FROM Members;")
            fetch = cursor.fetchall()[0][0]
            cur_id = fetch + 1 if fetch else 1

            # First, inserts the details into the members table
            cursor.execute(
                "INSERT INTO Members (Id, Full_Name, Position) VALUES (%s, %s, 'Normal Member');",
                (cur_id, full_name,)
            )
            
            # Check whether an admin already exist in the database.
            # If an admin does not exist, then make this user an admin.
            cursor.execute(
                "SELECT * FROM Login_Cred WHERE IsAdmin=1;",
            )
            admin_not_exists = len(cursor.fetchall()) == 0

            # Then, it inserts into the login credentials
            hash = generate_password_hash(password, salt_length=20)
            cursor.execute("INSERT INTO login_cred (Pass, Email, Username, IsAdmin, Member_Id) VALUES (%s, %s, %s, %s, %s);", (
                hash,
                str(email),
                username,
                admin_not_exists,
                cur_id,)
            )

            db_ref.commit()
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
    session.pop('isadmin', None) 
    session.pop('member_id', None) 

    session.pop('clearance', None) 

    return redirect(url_for('index.index')) 


def login_required(view):
    # Decorator so that user that is not logged in gets redirected to the login page
    # Before doing anything that messes with the data

    @functools.wraps(view)
    def wrapped_view(**kwargs):
        if session.get("loggedin") == None:
            flash("Login required!", "Error")
            return redirect(url_for("user.login", referback=request.referrer))

        return view(**kwargs)

    return wrapped_view

@bp.route("/<string:id>/profile")
def profile_page(id):

    # TODO: Add /user/<id>/profile
    cursor = db.get_db().cursor()
    cursor.execute("SELECT Full_Name, Position, Username, Email FROM Members m LEFT JOIN Login_Cred l ON l.Member_Id=m.Id WHERE m.Id=%s;", (id,))

    fetch = cursor.fetchall()
    
    # Check whether the member exists
    if not fetch:
        return render_template("404.html")

    cursor.execute(
        """
        SELECT c.Member_Id, c.Event_Id, c.Clearance_Level, IsVolunteer, Member_Role, e.Event_name, e.Venue, e.Event_Desc
        FROM Event_Committee ec
        RIGHT JOIN Clearance c
        ON ec.Member_Id=c.Member_Id AND ec.Event_Id=c.Event_Id
        JOIN Events e ON c.Event_Id=e.Id
        WHERE c.Member_Id=%s;
        """, (
            id,
        )
    )
    event_dict = []
    
    # Get all the data necessary
    for e in cursor.fetchall():
            event_dict.append({
                "event_name": e[5],
                "event_description": e[7],
                "event_id": e[1],
                "clearance": e[2],
                "role": e[4],
                "venue": e[6]
            })

    return render_template("profile.html",
        fullname=fetch[0][0],
        position=fetch[0][1],
        email=fetch[0][3],
        username=fetch[0][2],
        event_dict=event_dict
    )
