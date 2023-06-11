from merge_data import MergeData
from flask_api import db
from flask_api.database.models import Users
from main.dbUtils import storeMoodleData

def handle_successful_login(gCred:str, user_id:str, user_password:str)->str:
    '''handle successful login

    Args:
        gCred (str): google credentials
        user_id (str): user id of moodle
        user_password (str): user password of moodle

    Returns:
        str: html page
    '''
    merge_data = MergeData(gCred, user_id, user_password)
    data = merge_data.run()
    storeMoodleData(user_id, data)
    return f'<h1>已登記成功!</h1><h3>請至<a href="https://calendar.google.com/calendar">google calendar</a>查看</h3>'

def handle_login_failure(error:str)->str:
    '''handle login failure

    Args:
        error (str): error message
    
    Returns:
        str: html page
    '''
    return f'<h1>登記失敗!</h1><h3>{error}</h3>'

def handle_delete_account(user_id:str)->str:
    '''handle delete account

    Args:
        user_id (str): user id of moodle

    Returns:
        str: html page
    '''
    user = Users.query.filter_by(user_id=user_id).first()
    if user == None:
        return f'<h1>無此帳號!</h1>'
    db.session.delete(user)
    db.session.commit()
    return f'<h1>已刪除{user_id}!</h1>'