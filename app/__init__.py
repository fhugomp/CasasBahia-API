from flask import Flask
import json
from datetime import date, time, datetime
from decimal import Decimal

def create_app():
    app = Flask(__name__)
    app.json_encoder = CustomJSONEncoder
    
    from .routes import api
    app.register_blueprint(api, url_prefix='/api')

    return app