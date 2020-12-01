from flask import Flask

# App factory
def create_app(conf=None):
    app = Flask(__name__)
    
    return app