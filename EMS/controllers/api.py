from flask import Blueprint, render_template, request, current_app
from EMS.util import aes
from EMS import db
import mysql.connector
import json

bp = Blueprint("api", __name__, url_prefix="/api")

@bp.route("/form", methods=["POST"])
def forms():
    """ This route is a REST API that can be integrated to receive form data.
    The integration on Google App Script allows all the feedback form for events
    To be sent and received here. """
    
    # Get the POSTed data into a variable
    raw_data = request.get_data().decode("utf-8")

    # If the data posted begins with the prefix, then we can continue with decryption
    # because it's not garbage data.
    prefix = current_app.config.get("G_FORM_PREFIX")
    if raw_data.startswith(prefix):
        try:
            # Try to decrypt the data
            decrypted = aes.decrypt(raw_data[len(prefix):], current_app.config.get("G_FORM_SECRET").encode())

            # Parse the json data
            json_data = json.loads(decrypted)

            # Get the data, and put it into the database
            cursor = db.get_db().cursor()
            cursor.execute("INSERT INTO Feedback (Event_Id, Rating, Comments) VALUES (%s, %s, %s)", (
                json_data["event_id"],
                json_data["rating"],
                json_data["comment"],
            ))

            return "1"

        except (AssertionError, json.JSONDecodeError, KeyError, mysql.connector.Error) as e:
            # Error loading the data or inserting
            pass
    
    # Return 0 if data cannot be decrypted and inserted
    return "0"