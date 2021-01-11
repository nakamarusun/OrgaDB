from flask import Blueprint, render_template, session, redirect, url_for, request
import EMS.db as db
from EMS.controllers.user import login_required

bp = Blueprint("index", __name__, url_prefix="/")

def get_event_list():
    # Gets the list of events the user have clearance to.
    cursor = db.get_db().cursor()
    cursor.execute("SELECT e.Id, Event_Name, Clearance_Level FROM Clearance c JOIN Events e ON c.Event_Id=e.Id WHERE c.Member_Id=%s;", (
        session["member_id"],
    ))

    events = []
    # Gets all the events available for the user
    for ev in cursor.fetchall():
        # If the clearance is not 1, then show the event
        if ev[2] != 1:
            events.append({
                "event_id": ev[0],
                "event_name": ev[1]
            })
    return events

# Register a login required before every request being made.
# This is so that the user has to login first before being
# able to access anything.
@bp.before_request
def prompt_login():
    if not session.get("loggedin", False):
        return redirect(url_for("user.login"))

@bp.route("/")
def index():
    return render_template("index.html", event_dict=get_event_list())

@bp.route("/members")
def all_members():

    # Gets all the members with the login cred.
    cursor = db.get_db().cursor()

    cursor.execute("SELECT m.Id, Full_Name, Position, Email, IsAdmin FROM Members m LEFT JOIN Login_Cred l ON m.Id=l.Member_Id;")
    all_member = []
    for x in cursor.fetchall():
        all_member.append({
            "id": x[0],
            "name": x[1],
            "position": x[2],
            "mail": x[3],
            "admin": "True" if x[4] == 1 else "False"
        })

    return render_template("all_member.html",
    editPrivilege=session['isadmin'],
    addPrivilege=session['isadmin'],
    event_dict=get_event_list(),
    all_member_dict=all_member
    )

@bp.route("/members/delete", methods=['POST'])
def del_all_members():
    try:
        
        # Do an additional check here so the user cant delete itself.
        if request.form["ActiveTable"] == "0" and session['isadmin'] and session['member_id'] != request.form['Id']:
            db_obj = db.get_db()
            cursor = db_obj.cursor()

            # Delete login cred table
            cursor.execute('DELETE FROM Login_Cred WHERE Member_Id=%s;', (
                request.form['Id'],
            ))

            # Then delete all reference regarding member_id
            cursor.execute('DELETE FROM Clearance WHERE Member_Id=%s;', (request.form['Id'],))
            cursor.execute('DELETE FROM Event_Committee WHERE Member_Id=%s;', (request.form['Id'],))

            # Delete the members table last.
            cursor.execute('DELETE FROM Members WHERE Id=%s;', (
                request.form['Id'],
            ))

            # Commit
            db_obj.commit()

        return "1"
    except Exception as e:
        print(str(e))
        pass

    return "0"

@bp.route("/members/add", methods=['POST'])
def new_all_members():
    try:
        
        if request.form["ActiveTable"] == "0" and session['isadmin']:
            db_obj = db.get_db()
            cursor = db_obj.cursor()

            # Insert the members table first,
            cursor.execute('INSERT INTO Members (Full_Name, Position) VALUES (%s, %s);', (
                request.form['Name'],
                request.form['Position'],
            ))

            # Commit
            db_obj.commit()

        return "1"
    except Exception as e:
        print(str(e))
        pass

    return "0"

@bp.route("/members/update", methods=['POST'])
def upd_all_members():
    try:
        
        if request.form["activeTable"] == "0" and session['isadmin']:
            db_obj = db.get_db()
            cursor = db_obj.cursor()

            # Update the members table first,
            cursor.execute('UPDATE Members SET Full_Name=%s, Position=%s WHERE Id=%s;', (
                request.form['Name'],
                request.form['Position'],
                request.form['Id'],
            ))

            # Then update the login cred
            cursor.execute('UPDATE Login_Cred SET Email=%s, IsAdmin=%s WHERE Member_Id=%s;', (
                request.form['Mail'],
                request.form['isAdmin'] == "True",
                request.form['Id'],
            ))

            # Commit
            db_obj.commit()

        return "1"
    except Exception as e:
        print(str(e))
        pass

    return "0"
        
@bp.route("/admin")
def admin():

    # Check whether the user is an admin.

    if session['isadmin']:
        # Delete the event, and everything that is related to it in the database.
        # Gets all the sponsors
        cursor = db.get_db().cursor()

        cursor.execute("SELECT Id, Sponsor_Name, Contact_Name, Sponsor_Address, Phone_Number, Sponsor_Type FROM Sponsor;")
        sponsor_list = []
        for x in cursor.fetchall():
            sponsor_list.append({
                "id": x[0],
                "name": x[1],
                "cname": x[2],
                "address": x[3],
                "phone": x[4],
                "type": x[5]
            })

        return render_template("admin.html",
        event_dict=get_event_list(),
        sponsor_dict=sponsor_list
        )

    else:
        # If user is not an admin then punish.
        return render_template("nobueno.html")

@bp.route("/members/add", methods=['POST'])
def new_admin():
    try:
        
        if request.form["ActiveTable"] == "0" and session['isadmin']:
            db_obj = db.get_db()
            cursor = db_obj.cursor()

            # Insert the members table first,
            cursor.execute('INSERT INTO Members (Full_Name, Position) VALUES (%s, %s);', (
                request.form['Name'],
                request.form['Position'],
            ))

            # Commit
            db_obj.commit()

        return "1"
    except Exception as e:
        print(str(e))
        pass

    return "0"