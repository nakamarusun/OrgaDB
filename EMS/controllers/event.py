from flask import Blueprint
from flask import Flask, render_template, request, redirect, url_for, session
import EMS.db as db

bp = Blueprint("event", __name__, url_prefix="/event")

@bp.route("/")
def index():

    # TODO: Add /event
    # This should be the index page of /event.
    # So this should display all the events the user can see.
    return """ Bruh """

@bp.route("/<string:id>")
def event(id):

    # TODO: add /event/<id>
    # This should display the summary of the event
    return id

@bp.route("/<string:id>/description")
def description(id):

    # TODO: add /event/<id>/description
    # Displays the event description
    return "description: " + id

@bp.route("/<string:id>/finance")
def finance(id):

    # TODO: add /event/<id>/description
    # Displays the event's financy uh

    # Queries the database for necessary data to pass
    cursor = db.get_db().cursor()

    # First, we get the income
    fetch = cursor.execute(
        "SELECT e.Id, e.Name, Expense_Type, Amount, Expense_Date FROM Expenses e JOIN Events ev ON ev.Id=e.Event_Id WHERE Event_Id=%s;",
        (id,)
    )

    # List of income
    income_list = []
    for data in fetch.fetchall():
        income_list.append({
            "date": data[4],
            "name": data[1],
            "amount": data[3],
            "type": data[2]
        })
    
    # Get the expense
    fetch = cursor.execute(
        "SELECT i.Id, i.Name, Income_Type, Amount, Income_Date FROM Income i JOIN Events ev ON ev.Id=I.Event_Id WHERE Event_Id=%s;",
        (id,)
    )

    # And put to expense list
    expense_list = []
    for data in fetch.fetchall():
        expense_list.append({
            "date": data[4],
            "name": data[1],
            "amount": data[3],
            "type": data[2]
        })

    return render_template("finance.html", income_list=income_list, expense_list=expense_list)

@bp.route("/<string:id>/inventory")
def inventory(id):

    # TODO: add /event/<id>/description
    # Inventory moment right there
    return "inventory: " + id

@bp.route("/<string:id>/members")
def members(id):

    # TODO: add /event/<id>/description
    # Show the memberrs associated with an event

    # Queries the database for necessary data to pass
    cursor = db.get_db().cursor()

    # First, we get the committee list
    fetch = cursor.execute(
        "SELECT ec.Member_Id, m.Full_Name, ec.Member_Role FROM Event_Committee ec JOIN Members m ON ec.Member_Id=m.Id WHERE Event_Id=%s;",
        (id,)
    )

    # Committee list already includes volunteers, from the database.
    committee_list = []
    for data in fetch.fetchall():
        committee_list.append({
            "id": data[0],
            "name": data[1],
            "position": data[2]
        })

    # Get the guests
    fetch = cursor.execute(
        "SELECT Id, Full_Name FROM Guests WHERE Event_Id=%s;",
        (id,)
    )

    guest_list = []
    for data in fetch.fetchall():
        guest_list.append({
            "id": data[0],
            "name": data[1],
        })


    return render_template("members.html", committee_list=committee_list, guest_list=guest_list)

@bp.route("/<string:id>/feedback")
def feedback(id):

    # TODO: add /event/<id>/description
    # Shows all the FEEDBACKS!
    return "feedback: " + id

@bp.route("/new")
def add_new():

    # TODO: add /event/new
    # Add new event
    return render_template('new.html')