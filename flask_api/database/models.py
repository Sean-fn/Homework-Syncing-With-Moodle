from flask_api import db

class User(db.Model):
    user_id = db.Column(db.Integer, primary_key=True, unique=True, nullable=False)
    student_password = db.Column(db.String(120), nullable=False)
    gCredentials = db.Column(db.String(120))