from flask import Blueprint
from flask import Flask, render_template, request, redirect, url_for, session 

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
    return "finance: " + id

@bp.route("/<string:id>/inventory")
def inventory(id):

    # TODO: add /event/<id>/description
    # Inventory moment right there
    return "inventory: " + id

@bp.route("/<string:id>/members")
def members(id):

    # TODO: add /event/<id>/description
    # Show the memberrs associated with an event
    return "members: " + id

@bp.route("/<string:id>/feedback")
def feedback(id):

    # TODO: add /event/<id>/description
    # Shows all the FEEDBACKS!
    return "feedback: " + id

@bp.route("/new")
def add_new():

    # TODO: add /event/new
    # Add new event
    return """ Adding new """