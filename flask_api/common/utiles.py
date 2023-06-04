from flask_api import db
from flask_api.database.models import Users, MoodleData as moo

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

    def queryMoodleData(user_id, assessment_name):
        return moo.query.filter_by(user_id=user_id, assessment_name=assessment_name).first()
    
    def queryAllMoodleDataByUserID(user_id):
        return moo.query.filter_by(user_id=user_id).all()

    def deleteData(data):
        '''delete data from database

        Args:
            data (object): data from database
        '''
        db.session.delete(data)
        db.session.commit()