from flask import Blueprint

bp = Blueprint("index", __name__, url_prefix="/")

@bp.route("/")
def index():
    # TODO @aric: Create index.html here and use render_template
    return "bruh"