import json

from merge_data.google_calendar.g_calendar import GCalendar
from flask_api.database.models import User
from flask_api.common.utiles import Utiles

def getGCredentials(user_id, user_password):
    '''if user id and password is empty:
    store user id, password and gCredentials
    if NOT empty:
    get the google credentials from database

    Args:
        user_id (string): user id of moodle
        user_password (string): user password of moodle

    Returns:

    '''
    user = User.query.filter_by(user_id=user_id).first()
    if user == None:
        gCredentials = ''
        #TODO: store only refesh token and so on
        data = User(user_id=user_id, student_password=user_password, gCredentials=str(gCredentials).replace("'", '"'))
        Utiles().insertData(data)
    else:
        gCredentials = json.loads(user.gCredentials)
    gCredentials = GCalendar(gCredentials).get_json_credentials()
    return gCredentials