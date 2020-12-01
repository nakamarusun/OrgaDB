from flask import Blueprint

bp = Blueprint("user", __name__, url_prefix="/user")

@bp.route("/login")
def login():
    # TODO @bently: Create login
    return "login"

@bp.route("/register")
def register():
    # TODO @bently: Create register
    return "register"