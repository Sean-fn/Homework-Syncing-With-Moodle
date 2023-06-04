import json

from merge_data.google_calendar.g_calendar import GCalendar
from flask_api.database.models import Users, MoodleData
from flask_api.common.utiles import Utiles
from flask_api import db

def storeUserData(user_id:str, user_password:str) -> str:
    '''if user id and password is empty:
    store user id, password and gCredentials
    if NOT empty:
    get the google credentials from database

    Args:
        user_id (string): user id of moodle
        user_password (string): user password of moodle

    Returns:
        String: refreshed google credentials
    '''
    user = Utiles.queryUser(user_id)

    if user == None:
        gCredentials = ''
    else:
        gCredentials = json.loads(user.gCredentials)
    gCredentials = GCalendar(gCredentials).get_json_credentials()
    
    '''store user id and password'''
    if not user:
        data = Users(user_id=user_id, student_password=user_password, gCredentials=str(gCredentials).replace("'", '"'))
        Utiles.insertData(data)
    return gCredentials

def storeMoodleData(user_id:str, data:dict) -> None:
    '''store moodle data to database

    Args:
        user_id (string): user id of moodle
        moodle_data (dict): extracted moodle data

    Returns:
        Bool: If the data stored unsucesfully, return False
    '''
    print('-----in storeMoodleData-----')
    user = Users.query.get(user_id)
    #TODO: Add exception handling
    for i in range(len(data['assessmentName'])):
        print('the current data = ', Utiles.queryMoodleData(user_id, data['assessmentName'][i]))
        if Utiles.queryMoodleData(user_id, data['assessmentName'][i]) == '<MoodleData '+data['assessmentName'][i]+'>':
            print('the data is already in the database')
            continue
        print('the i = ', i)
        print(data['assessmentName'][i])
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
    print('the length of the moodle data = ', len(user.moodle_data))
    print('-----out storeMoodleData-----')