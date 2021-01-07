from flask import Blueprint,render_template

bp = Blueprint("index", __name__, url_prefix="/")

@bp.route("/")
def index():
    # TODO @aric: Create index.html here and use render_template
    return render_template("admin.html", debug = True, editPrivilege = "1", addPrivilege=1)
