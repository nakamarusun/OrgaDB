from flask import Blueprint, render_template, session, redirect, url_for

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
    return render_template("index.html")


@bp.route("/admin")
def admin():
    return render_template("admin.html")