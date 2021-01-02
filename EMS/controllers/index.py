from flask import Blueprint,render_template

bp = Blueprint("index", __name__, url_prefix="/")

@bp.route("/")
def index():
    # TODO @aric: Create index.html here and use render_template
<<<<<<< HEAD
    return render_template("index.html", debug = True)
=======
    return render_template("finance.html", debug = True)
>>>>>>> html_testing_ground
