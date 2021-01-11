from flask import Blueprint, render_template, session, redirect, url_for
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
            "admin": "Yes" if x[4] == 1 else "No"
        })

    return render_template("all_member.html",
    editPrivilege=session['isadmin'],
    addPrivilege=session['isadmin'],
    event_dict=get_event_list(),
    all_member_dict=all_member
    )

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
