from flask import Blueprint
from flask import Flask, render_template, request, redirect, url_for, session, g
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

# This function is run before every "event" route.
# This is useful to get the current user's clearance level.
@bp.before_request
def update_privilege():
    cursor = db.get_db().cursor()

    cursor.execute("SELECT Event_Id, Clearance_Level FROM Clearance WHERE Member_Id=%s", (
        session['member_id'],
    ))
    
    # Gets the clearances
    clearances = cursor.fetchall()

    # And inserts it into the session variable
    for c in clearances:
        # The key is the id of the event, and the value is the clearance
        session['clearance'][c[0]] = c[1]


def check_id(func):
    # Decorator function to check first whether the id exist.
    # If it does not, then redirect to 404

    # Basically this decorator is used to fix flask, so that the function name is the
    # name of the original function instead of "wrapped."

    # This decorator also checks whether the user has privilege to read the event.

    # This function also gets the name of the event, and sets it to a global variable.
    @functools.wraps(func)
    def wrapped(id):
        # First, we check if the string is a number first. If it's not, don't bother checking.
        if not id.isnumeric():
            return render_template("404.html")
        
        # Second, we check whether the event exists in the database.
        cursor = db.get_db().cursor()
        cursor.execute('SELECT Id, Event_Name FROM Events WHERE Id=%s', (id,))
        fetch = cursor.fetchall()

        if fetch:
            # If the event is found,
            # Check whether the user can view the event.
            
            # If the user does not have any clearance in the database,
            # then the default is clearance 1
            if session['clearance'].get(int(id), 1) != "1":
                g.event_name = fetch[0][1]
                g.event_id = fetch[0][0]
                return func(id)

        # If none of the conditions is met, then return a 404
        return render_template("404.html")
            
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
        "SELECT Income_Date, Item_Name, Amount, Income_Type, Sponsor_Name, i.Id FROM Income i LEFT JOIN Sponsor s ON i.Sponsor_Id=s.Id WHERE Event_Id=%s;",
        (id,)
    )

    # List of income
    income_list = []
    for data in cursor.fetchall():
        income_list.append({
            "id": data[5],
            "date": data[0],
            "name": data[1],
            "amount": format_idr(data[2]),
            "type": data[3],
            "sponsor_name": data[4]
        })
    
    # Get the expense
    cursor.execute(
        "SELECT e.Id, e.Item_Name, Expense_Type, Amount, Expense_Date, e.Id FROM Expenses e JOIN Events ev ON ev.Id=e.Event_Id WHERE Event_Id=%s;",
        (id,)
    )

    # And put to expense list
    expense_list = []
    for data in cursor.fetchall():
        expense_list.append({
            "id": data[5],
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

    return render_template("finance.html",
        income_dict=income_list,
        expense_dict=expense_list,
        sponsor_list=sponsor_list,
        editPrivilege=session['clearance'].get(int(id), 1)=="3",
        addPrivilege=session['clearance'].get(int(id), 1)=="3"
    )

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
                cursor.execute("SELECT Id FROM Sponsor WHERE Sponsor_Name=%s", (request.form['Sponsor'],))
                sponsor_id = cursor.fetchall()[0][0]

            # Then, we can insert into income
            cursor.execute('Insert INTO Income (Income_Type, Item_Name, Amount, Income_Date, Event_Id, Sponsor_Id) VALUES (%s, %s, %s, %s, %s, %s);', (
                request.form['Type'],
                request.form['Name'],
                request.form['Amount'],
                request.form['Date'],
                id,
                sponsor_id,
            ))

        elif request.form['ActiveTable'] == "1":
            cursor.execute('Insert INTO Expenses (Expense_Type, Item_Name, Amount, Expense_Date, Event_Id) VALUES (%s, %s, %s, %s, %s);', (
                request.form['Type'],
                request.form['Name'],
                request.form['Amount'],
                request.form['Date'],
                id,
                ))

        # Commit
        db_obj.commit()

        return "1"
    
    except Exception as e:
        print(str(e))
        return "0"

@bp.route("/<string:id>/finance/delete", methods=['POST'])
def del_finance(id):
    # Deletes the entry based on the ID
    try:
        db_obj = db.get_db()

        # Delete from database
        cursor = db_obj.cursor()
        
        # Delete the event committee
        if request.form["ActiveTable"] == "0":
            cursor.execute("DELETE FROM Income WHERE Id=%s;", (
                request.form["ID"],
            ))

        # Delete the guest
        elif request.form["ActiveTable"] == "1":
            cursor.execute("DELETE FROM Expenses WHERE Id=%s;", (
                request.form["ID"],
            ))

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

    return render_template("inventory.html",
        inventory_dict=in_list,
        sponsor_list=sponsor_list,
        editPrivilege=session['clearance'].get(int(id), 1)=="3"
    )

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
            request.form['name'],
            request.form['amount'],
            sponsor_id,
            id,
        ))

        # Commit
        db_obj.commit()

        return "1"
    except Exception as e:
        print(str(e))
        return "0"

@bp.route("/<string:id>/inventory/delete", methods=['POST'])
def del_inventory(id):
    # Deletes the entry based on the ID
    try:
        db_obj = db.get_db()

        # Delete from database
        cursor = db_obj.cursor()
        
        # Delete the event committee
        if request.form["ActiveTable"] == "0":
            cursor.execute("DELETE FROM Inventory WHERE Inventory_Id=%s;", (
                request.form["ID"],
            ))

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

    return render_template("members.html",
        committee_dict=committee_list,
        volunteer_dict=volunteer_list,
        guest_dict=guest_list,
        editPrivilege=session['clearance'].get(int(id), 1)=="3"
    )

@bp.route("/<string:id>/members/add", methods=['POST'])
def add_members(id):

    try:
        db_obj = db.get_db()

        # Update database
        cursor = db_obj.cursor()
        
        if request.form['ActiveTable'] == "0" or request.form["ActiveTable"] == "1":
            # First, check whether the member exist specified in the ID
            cursor.execute(
                "SELECT * FROM Members WHERE Id=%s;", (
                    request.form['Id'],
            ))
            member = cursor.fetchall()[0]

            # If the member ID exist in the database, check whether the member already exist in
            # The committee level.
            cursor.execute(
                "SELECT * FROM Event_Committee WHERE Event_Id=%s AND Member_Id=%s;", (
                    id,
                    request.form['Id'],
            ))
            event_committee = cursor.fetchall()

            # If the member ID exists in the database, and not already available in the event_committee
            if member and not event_committee:
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
            
            else:
                return "0"

        elif request.form['ActiveTable'] == "2":
            
            # Insert the guest
            cursor.execute("INSERT INTO Guests (Full_Name, Email, Phone_Number, Category, Event_Id) VALUES (%s, %s, %s, %s, %s);", (
                request.form["name"],
                request.form["mail"],
                request.form["phone"],
                request.form["position"],
                id,
            ))
            
        # Commit
        db_obj.commit()

        return "1"
    except Exception as e:
        print(str(e))
        return "0"

@bp.route("/<string:id>/members/delete", methods=['POST'])
def del_members(id):
    # Deletes the entry based on the ID
    try:
        db_obj = db.get_db()

        # Delete from database
        cursor = db_obj.cursor()
        
        # Delete the event committee
        # Don't forget to delete the clearance too.
        if request.form["ActiveTable"] == "0" or request.form["ActiveTable"] == "1":
            cursor.execute("DELETE FROM Event_Committee WHERE Member_Id=%s AND Event_Id=%s;", (
                request.form["ID"],
                id,
            ))

            cursor.execute("DELETE FROM Clearance WHERE Member_Id=%s AND Event_Id=%s;", (
                request.form["ID"],
                id,
            ))

        # Delete the guest
        elif request.form["ActiveTable"] == "2":
            cursor.execute("DELETE FROM Guests WHERE Id=%s AND Event_Id=%s;", (
                request.form["ID"],
                id,
            ))

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

@bp.route("/<string:id>/admin")
@check_id
def admin(id):

    return render_template("admin.html")

@bp.route("/new", methods = ['POST', 'GET'] )
def add_new():
    if request.method == 'POST':
        event_name = request.form['event_name']
        venue = request.form['venue']
        budget = request.form['budget']
        description = request.form['desc']
        cursor = db.get_db().cursor()

        # Gets the ID to increment
        cursor.execute("SELECT MAX(Id) FROM Events;")

        fetch = cursor.fetchall()[0][0]
        event_id = fetch + 1 if fetch else 1

        cursor.execute('INSERT INTO Events (Id, Event_Name, Venue, Budget, Event_Desc) VALUES(%s, %s, %s, %s, %s)', (
            event_id,
            event_name,
            venue,
            budget,
            description,
        ))
        db.get_db().commit()
        return redirect(url_for('event.description', id=str(event_id)))

    return render_template('new.html')