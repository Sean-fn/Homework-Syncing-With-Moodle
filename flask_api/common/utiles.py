from flask_api import db
from flask_api.database.models import User

def initDB():
    db.drop_all()
    db.create_all()

def createTables():
    db.create_all()

def dropTables():
    db.drop_all()
    
def insertData(data):
    db.session.add(data)
    db.session.commit()

def updateData():
    db.session.commit()

def queryUser(user_id):
    return User.query.filter_by(user_id=user_id).first()

def deleteData(data):
    db.session.delete(data)
    db.session.commit()