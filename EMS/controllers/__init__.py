from flask import render_template
from EMS.controllers import index, user

def register_all_routes(app):
    # Register all blueprint here
    app.register_blueprint(index.bp)
    app.register_blueprint(user.bp)
    # TODO: Add the rest of the blueprints here

    # Register the 404
    @app.errorhandler(404)
    def page404(e):
        return render_template("404.html")