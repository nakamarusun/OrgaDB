from flask import Blueprint
from flask import Flask, render_template, request, redirect, url_for, session 
from EMS import db
import functools
import re

bp = Blueprint("event", __name__, url_prefix="/event")

def check_id(func):
    # Decorator function to check first whether the id exist.
    # If it does not, then redirect to 404

    # Basically this decorator is used to fix flask, so that the function name is the
    # name of the original function instead of "wrapped."
    @functools.wraps(func)
    def wrapped(id):
        # First, we check whether the event exists in the database.
        cursor = db.get_db().cursor()
        cursor.execute('SELECT * FROM Events WHERE Id=%s', (id,))
        fetch = cursor.fetchall()

        if not fetch:
            # Return 404
            return render_template("404.html")
        else:
            # Normal execution
            return func(id)
            
    return wrapped

@bp.route("/")
def index():

    # TODO: Add /event
    # This should be the index page of /event.
    # So this should display all the events the user can see.
    return """ Bruh """

@bp.route("/<string:id>")
@check_id
def event(id):

    # TODO: add /event/<id>
    # This should display the summary of the event
    return id

@bp.route("/<string:id>/description")
@check_id
def description(id):

    cursor = db.get_db().cursor()
    cursor.execute('SELECT Event_Name, Event_Desc FROM Events WHERE Id=%s', (id,))
    fetch = cursor.fetchall()[0]
    
    return render_template("description.html", title=fetch[0], desc=fetch[1])

@bp.route("/<string:id>/finance")
@check_id
def finance(id):

    # TODO: add /event/<id>/description
    # Displays the event's financy uh

    # Queries the database for necessary data to pass
    cursor = db.get_db().cursor()

    # First, we get the income
    cursor.execute(
        "SELECT e.Id, e.Other_Expense, Expense_Type, Amount, Expense_Date FROM Expenses e JOIN Events ev ON ev.Id=e.Event_Id WHERE Event_Id=%s;",
        (id,)
    )

    # List of income
    income_list = []
    for data in cursor.fetchall():
        income_list.append({
            "date": data[4],
            "name": data[1],
            "amount": data[3],
            "type": data[2]
        })
    
    # Get the expense
    cursor.execute(
        "SELECT i.Id, i.Other_Income, Income_Type, Amount, Income_Date FROM Income i JOIN Events ev ON ev.Id=I.Event_Id WHERE Event_Id=%s;",
        (id,)
    )

    # And put to expense list
    expense_list = []
    for data in cursor.fetchall():
        expense_list.append({
            "date": data[4],
            "name": data[1],
            "amount": data[3],
            "type": data[2]
        })

    return render_template("finance.html", income_list=income_list, expense_list=expense_list)

@bp.route("/<string:id>/inventory")
@check_id
def inventory(id):

    # TODO: add /event/<id>/description
    # Inventory moment right there
    return "inventory: " + id

@bp.route("/<string:id>/members")
@check_id
def members(id):

    # TODO: add /event/<id>/description
    # Show the memberrs associated with an event

    # Queries the database for necessary data to pass
    cursor = db.get_db().cursor()

    # First, we get the committee list
    cursor.execute(
        "SELECT ec.Member_Id, m.Full_Name, ec.Member_Role FROM Event_Committee ec JOIN Members m ON ec.Member_Id=m.Id WHERE Event_Id=%s;",
        (id,)
    )

    # Committee list already includes volunteers, from the database.
    committee_list = []
    for data in cursor.fetchall():
        committee_list.append({
            "id": data[0],
            "name": data[1],
            "position": data[2]
        })

    # Get the guests
    cursor.execute(
        "SELECT Id, Full_Name FROM Guests WHERE Event_Id=%s;",
        (id,)
    )

    guest_list = []
    for data in cursor.fetchall():
        guest_list.append({
            "id": data[0],
            "name": data[1],
        })


    return render_template("members.html", committee_list=committee_list, guest_list=guest_list)

@bp.route("/<string:id>/feedback")
@check_id
def feedback(id):

    # TODO: add /event/<id>/description
    # Shows all the FEEDBACKS!
    return "feedback: " + id

@bp.route("/new", methods = ['POST', 'GET'] )
def add_new():
    if request.method == 'POST':
        event_name = request.form['event_name']
        venue = request.form['venue']
        budget = request.form['budget']
        description = request.form['desc']
        cursor = db.get_db().cursor()

        cursor.execute('INSERT INTO Events (Event_Name, Venue, Budget, Event_Desc) VALUES(%s, %s, %s, %s)', (event_name, venue, budget, description))
        db.get_db().commit()
        return redirect(url_for('index.index'))
    # TODO: add /event/new
    # Add new event
    return render_template('new.html')