from flask_api import db
from flask_api.database.models import Users

class Utiles:
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
        return Users.query.filter_by(user_id=user_id).first()

    def deleteData(data):
        '''delete data from database

        Args:
            data (object): data from database
        '''
        db.session.delete(data)
        db.session.commit()