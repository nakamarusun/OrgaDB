from flask import Blueprint
from flask import Flask, render_template, request, redirect, url_for, session 
from EMS import db
from EMS.util.extra import format_idr
import functools
import re

bp = Blueprint("event", __name__, url_prefix="/event")

# Register a login required before every request being made.
# This is so that the user has to login first before being
# able to access anything.
@bp.before_request
def prompt_login():
    if not session.get("loggedin", False):
        return redirect(url_for("user.login"))

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

@bp.route("/<string:id>/description")
@check_id
def description(id):

    cursor = db.get_db().cursor()
    cursor.execute('SELECT Event_Name, Event_Desc FROM Events WHERE Id=%s', (id,))
    fetch = cursor.fetchall()[0]
    
    return render_template("description.html", event_name=fetch[0], description_text=fetch[1])

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
        "SELECT Income_Date, Item_Name, Amount, Income_Type, Sponsor_Name FROM Income i LEFT JOIN Sponsor s ON i.Sponsor_Id=s.Id WHERE Event_Id=%s;",
        (id,)
    )

    # List of income
    income_list = []
    for data in cursor.fetchall():
        income_list.append({
            "date": data[0],
            "name": data[1],
            "amount": format_idr(data[2]),
            "type": data[3],
            "sponsor_name": data[4]
        })
    
    # Get the expense
    cursor.execute(
        "SELECT e.Id, e.Item_Name, Expense_Type, Amount, Expense_Date FROM Expenses e JOIN Events ev ON ev.Id=e.Event_Id WHERE Event_Id=%s;",
        (id,)
    )

    # And put to expense list
    expense_list = []
    for data in cursor.fetchall():
        expense_list.append({
            "date": data[4],
            "name": data[1],
            "amount": format_idr(data[3]),
            "type": data[2]
        })

    # Get the sponsors
    cursor.execute(
        "SELECT Sponsor_Name FROM Sponsor;"
    )
    sponsor_list = [ d[0] for d in cursor.fetchall() ]

    return render_template("finance.html", income_dict=income_list, expense_dict=expense_list, sponsor_list=sponsor_list)

@bp.route("/<string:id>/finance/add", methods=['POST'])
def add_finance(id):
    """ POST method for updating the description """
    try:
        db_obj = db.get_db()

        # Update datbase
        cursor = db_obj.cursor()

        # Depending on the table selected (Income / Expense), insert the data.
        if request.form['ActiveTable'] == "0":
            # Get the sponsor ID from the database
            sponsor_id = None
            if request.form['Sponsor'] != "None":
                cursor.execute("SELECT Id FROM Sponsor WHERE Sponsor_Name=%s", (request.form['Sponsor'].replace("+", " "),))
                sponsor_id = cursor.fetchall()[0][0]

            # Then, we can insert into income
            cursor.execute('Insert INTO Income (Income_Type, Item_Name, Amount, Income_Date, Event_Id, Sponsor_Id) VALUES (%s, %s, %s, %s, %s, %s);', (
                request.form['Type'].replace("+", " "),
                request.form['Name'].replace("+", " "),
                request.form['Amount'].replace("+", " "),
                request.form['Date'].replace("+", " "),
                id,
                sponsor_id,
            ))

        elif request.form['ActiveTable'] == "1":
            cursor.execute('Insert INTO Expenses (Expense_Type, Item_Name, Amount, Expense_Date, Event_Id) VALUES (%s, %s, %s, %s, %s);', (
                request.form['Type'].replace("+", " "),
                request.form['Name'].replace("+", " "),
                request.form['Amount'].replace("+", " "),
                request.form['Date'].replace("+", " "),
                id,
                ))

        # Commit
        db_obj.commit()

        return "1"
    
    except Exception as e:
        print(str(e))
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
        "SELECT Sponsor_Name FROM Sponsor;"
    )
    sponsor_list = [ d[0] for d in cursor.fetchall() ]

    return render_template("inventory.html", inventory_dict=in_list, sponsor_list=sponsor_list)

@bp.route("/<string:id>/inventory/add", methods=['POST'])
def add_inventory(id):

    try:
        db_obj = db.get_db()
        cursor = db_obj.cursor()

        # Get the sponsor ID, if available
        sponsor_id = None
        if request.form['sponsor'] != "None":
            cursor.execute("SELECT Id FROM Sponsor WHERE Sponsor_Name=%s", (request.form['sponsor'].replace("+", " "),))
            sponsor_id = cursor.fetchall()[0][0]

        # Update datbase
        cursor.execute('INSERT INTO Inventory (Item_Name, Item_Quantity, Sponsor_Id, Event_Id) VALUES (%s, %s, %s, %s);', (
            request.form['name'].replace("+", " "),
            request.form['amount'].replace("+", " "),
            sponsor_id,
            id,
        ))

        # Commit
        db_obj.commit()

        return "1"
    except Exception as e:
        print(str(e))
        return "0"

@bp.route("/<string:id>/members")
@check_id
def members(id):

    # Queries the database for necessary data to pass
    cursor = db.get_db().cursor()

    # First, we get the committee list
    cursor.execute(
        "SELECT Id, Full_Name, Member_Role, Clearance_Level, IsVolunteer FROM Members m LEFT JOIN Clearance c ON m.Id=c.Member_Id JOIN Event_Committee ec ON ec.Member_Id=m.Id WHERE c.Event_Id=%s AND ec.Event_id=%s;",
        (id, id,)
    )

    # Committee list already includes volunteers, from the database.
    committee_list = []
    volunteer_list = []
    for data in cursor.fetchall():

        # Checks whether the member is a volunteer.
        if not data[4]:
            committee_list.append({
                "id": data[0],
                "name": data[1],
                "position": data[2],
                "clearance": data[3]
            })
        else:
            volunteer_list.append({
                "id": data[0],
                "name": data[1],
                "position": data[2],
                "clearance": data[3]
            })

    # Get the guests
    cursor.execute(
        "SELECT Id, Full_Name, Category, Phone_Number, Email FROM Guests WHERE Event_Id=%s;",
        (id,)
    )

    guest_list = []
    for data in cursor.fetchall():
        guest_list.append({
            "id": data[0],
            "name": data[1],
            "category": data[2],
            "Phone_Number": data[3],
            "Email": data[4]
        })

    return render_template("members.html", committee_dict=committee_list, volunteer_dict=volunteer_list, guest_dict=guest_list)

@bp.route("/<string:id>/members/add", methods=['POST'])
def add_members(id):

    try:
        db_obj = db.get_db()

        # Update database
        cursor = db_obj.cursor()
        
        if request.form['ActiveTable'] == "0" or request.form["ActiveTable"] == "1":
            cursor.execute(
                "SELECT * FROM Members WHERE Id=%s;", (
                    request.form['Id'],
            ))
            member = cursor.fetchall()[0]

            # If the member ID exist in the database, then insert everything
            if member:
                # Insert the member first
                cursor.execute("INSERT INTO Event_Committee (Event_Id, Member_Id, Member_Role, IsVolunteer) VALUES (%s, %s, %s, %s);", (
                    id,
                    member[0],
                    request.form['Position'],
                    request.form['ActiveTable'] == "1", 
                ))

                # Then, insert the clearance level
                cursor.execute("INSERT INTO Clearance (Member_Id, Clearance_Level, Event_Id) VALUES (%s, %s, %s);", (
                    member[0],
                    request.form['Clearance'],
                    id,
                ))

        elif request.form['ActiveTable'] == "2":
            # TODO: Is not complete
            pass

        # Commit
        db_obj.commit()

        return "1"
    except Exception as e:
        print(str(e))
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
            "rating": data[1],
            "feedback_text": data[2]
        })
    
    return render_template("feedback.html", parent_list=f_list)

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