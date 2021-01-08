from flask import Blueprint, render_template, session, redirect, url_for
import EMS.db as db

bp = Blueprint("index", __name__, url_prefix="/")

# Register a login required before every request being made.
# This is so that the user has to login first before being
# able to access anything.
@bp.before_request
def prompt_login():
    if not session.get("loggedin", False):
        return redirect(url_for("user.login"))

@bp.route("/")
def index():
    # Get all the events taht is available for the current user.
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

    return render_template("index.html", event_dict=events)


@bp.route("/admin")
def admin():
    return render_template("admin.html")
