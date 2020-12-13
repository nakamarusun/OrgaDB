from flask import Blueprint,render_template

bp = Blueprint("user", __name__, url_prefix="/user")

@bp.route("/login")
def login():
    # TODO @bently: Create login
    return render_template('login.html')

@bp.route("/register")
def register():
    # TODO @bently: Create register
    return render_template('register.html')

@bp.route("/profile")
def profile():
    return render_template('profile.html')