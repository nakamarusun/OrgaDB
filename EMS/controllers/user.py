from flask import Blueprint,render_template

bp = Blueprint("user", __name__, url_prefix="/user")

@bp.route("/login")
def login():
    # TODO @bently: Create login
    login_text = True
    return render_template('login.html',login_text =login_text)

@bp.route("/register")
def register():
    # TODO @bently: Create register
    login_text = False
    return render_template('register.html', login_text=login_text)