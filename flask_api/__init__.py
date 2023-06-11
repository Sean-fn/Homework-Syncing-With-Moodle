from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from dotenv import load_dotenv
import os

from flask_api.config import Config

load_dotenv()
db = SQLAlchemy()

def create_app():
    '''Creating flask app

    Returns:
        Flask: Flask app
    '''
    app = Flask(__name__, template_folder='../frontend/templates',static_folder='../frontend/static')
    app.secret_key = os.getenv("FLASK_SECRET_KEY")
    app.config['SQLALCHEMY_DATABASE_URI'] = os.environ.get("DATABASE_URL")
    app.config.from_object(Config)
    db.init_app(app)
    with app.app_context():
        db.create_all()

    return app