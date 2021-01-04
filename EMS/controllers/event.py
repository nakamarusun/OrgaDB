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

@bp.route("/<string:id>/description/update", methods=['POST'])
def update_description(id):
    """ POST method for updating the description """
    try:
        db_obj = db.get_db()

        # Update datbase
        cursor = db_obj.cursor()
        cursor.execute('UPDATE Events SET Event_Desc=%s WHERE Id=%s;', (request.form['description'], id,))

        # Commit
        db_obj.commit()

        return "1"
    
    except Exception:
        return "0"

@bp.route("/<string:id>/finance")
@check_id
def finance(id):

    # Queries the database for necessary data to pass
    cursor = db.get_db().cursor()

    # First, we get the income
    cursor.execute(
        "SELECT e.Id, e.Item_Name, Expense_Type, Amount, Expense_Date FROM Expenses e JOIN Events ev ON ev.Id=e.Event_Id WHERE Event_Id=%s;",
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
        "SELECT i.Id, i.Item_Name, Income_Type, Amount, Income_Date FROM Income i JOIN Events ev ON ev.Id=I.Event_Id WHERE Event_Id=%s;",
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

    # Get the sponsors
    cursor.execute(
        "SELECT Sponsor_Name FROM Sponsor WHERE Event_Id=%s;",
        (id,)
    )
    sponsor_list = [ d[0] for d in cursor.fetchall() ]

    return render_template("finance.html", income_list=income_list, expense_list=expense_list, sponsor_list=sponsor_list)

@bp.route("/<string:id>/finance/add", methods=['POST'])
def add_finance(id):
    """ POST method for updating the description """
    try:
        db_obj = db.get_db()

        # Update datbase
        cursor = db_obj.cursor()

        # Depending on the table selected (Income / Expense), insert the data.
        if request.form['activeTable'] == 0:
            cursor.execute('Insert INTO Income (Income_Type, Item_Name, Amount, Income_Date, Event_Id) VALUES (%s, %s, %s, %s);', (
                request.form['Type'],
                request.form['Name'],
                request.form['Amount'],
                request.form['Date'],
                id,
                ))

        elif request.form['activeTable'] == 1:
            cursor.execute('Insert INTO Expenses (Expense_Type, Item_Name, Amount, Expense_Date, Event_Id) VALUES (%s, %s, %s, %s);', (
                request.form['Type'],
                request.form['Name'],
                request.form['Amount'],
                request.form['Date'],
                id,
                ))

        # Commit
        db_obj.commit()

        return "1"
    
    except Exception:
        print(Exception)
        return "0"

@bp.route("/<string:id>/inventory")
@check_id
def inventory(id):

    # Queries the database for necessary data to pass
    cursor = db.get_db().cursor()

    # First, we get the committee list
    cursor.execute(
        "SELECT Inventory_Id, Item_Name, Item_Quantity, Sponsor_Name FROM Inventory i LEFT JOIN Sponsor s ON i.Sponsor_Id=s.Id WHERE i.Event_ID=%s;",
        (id,)
    )
    
    in_list = []
    for data in cursor.fetchall():
        in_list.append({
            "id": data[0],
            "name": data[1],
            "amount": data[2],
            "sponsor": data[3]
        })

    # Get the sponsors
    cursor.execute(
        "SELECT Sponsor_Name FROM Sponsor WHERE Event_Id=%s;",
        (id,)
    )
    sponsor_list = [ d[0] for d in cursor.fetchall() ]

    return render_template("inventory.html", in_list=in_list, sponsor_list=sponsor_list)

@bp.route("/<string:id>/inventory/add", methods=['POST'])
def add_inventory(id):

    try:
        db_obj = db.get_db()

        # Update datbase
        cursor = db_obj.cursor()
        cursor.execute('INSERT INTO Inventory (Item_Name, Item_Quantity, Sponsor_Id, Event_Id) VALUES (%s, %s, %s, %s);', (request.form['name'], request.form['amount'], 1, id,))

        # Commit
        db_obj.commit()

        return "1"
    except:
        print(Exception)
        return "0"

@bp.route("/<string:id>/members")
@check_id
def members(id):

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

@bp.route("/<string:id>/members/add", methods=['POST'])
def add_members(id):

    try:
        db_obj = db.get_db()

        # Update database
        cursor = db_obj.cursor()
        
        # TODO: Talk with aric how to this message
        if request.form['activeTable'] == 0:
            pass

        elif request.form['activeTable'] == 1:
            pass

        elif request.form['activeTable'] == 2:
            pass

        # Commit
        db_obj.commit()

        return "1"
    except:
        print(Exception)
        return "0"

@bp.route("/<string:id>/feedback")
@check_id
def feedback(id):

        # Queries the database for necessary data to pass
    cursor = db.get_db().cursor()

    # First, we get the committee list
    cursor.execute(
        "SELECT * FROM Feedback WHERE Event_ID=%s;",
        (id,)
    )
    
    f_list = []
    for data in cursor.fetchall():
        f_list.append({
            "id": data[0],
            "rating": data[1],
            "comments": data[2]
        })
    
    return render_template("feedback.html", f_list=f_list)

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

    return render_template('new.html')