from flask import Flask
import json
from datetime import date, time, datetime
from decimal import Decimal

class CustomJSONEncoder(json.JSONEncoder):
    def default(self, obj):
        if isinstance(obj, (datetime, date, time)):
            return obj.isoformat()
        if isinstance(obj, Decimal):
            return float(obj)
        return super().default(obj)


def create_app():
    app = Flask(__name__)
    app.json_encoder = CustomJSONEncoder
    
    from .routes import api
    app.register_blueprint(api, url_prefix='/api')

    return app