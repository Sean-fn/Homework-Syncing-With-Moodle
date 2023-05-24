import json

from merge_data.google_calendar.g_calendar import GCalendar
from flask_api.database.models import Users, MoodleData
from flask_api.common.utiles import Utiles
from 

def storeGCredentials(user_id, user_password):
    '''if user id and password is empty:
    store user id, password and gCredentials
    if NOT empty:
    get the google credentials from database

    Args:
        user_id (string): user id of moodle
        user_password (string): user password of moodle

    Returns:

    '''
    user = Users.query.filter_by(user_id=user_id).first()
    if user == None:
        gCredentials = ''
        #TODO: store only refesh token and so on
        #TODO: break down the code(insertData)
        data = Users(user_id=user_id, student_password=user_password, gCredentials=str(gCredentials).replace("'", '"'))
        Utiles().insertData(data)
    else:
        gCredentials = json.loads(user.gCredentials)
    gCredentials = GCalendar(gCredentials).get_json_credentials()
    return gCredentials

def storeMoodleData(user_id, data):
    '''store moodle data to database

    Args:
        user_id (string): user id of moodle
        moodle_data (dict): extracted moodle data

    Returns:

    '''
    user = Users.query.get(user_id)
    #TODO: Add exception handling

    for i in range(len(data['assessmentName'])):
        assessment = MoodleData(
            user_id=user.user_id,
            assessment_name=data['assessmentName'][i],
            assessment_due_date=data['assessmentDueDate'][i],
            assessment_due_time=data['assessmentDueTime'][i],
            assessment_detail=data['assessmentDetail'][i],
            assessment_url=data['assessmentUrl'][i]
        )
        db.session.add(assessment)

    db.session.commit()