from merge_data import MergeData
# from flask_api.database.models import Users
from flask_api.common.utiles import Utiles
from main.dbUtiles import storeMoodleData

def handle_successful_login(gCred, user_id, user_password):
    
    merge_data = MergeData(gCred, user_id, user_password)
    data = merge_data.run()
    storeMoodleData(user_id, data)
    return f'<h1>已登記成功!</h1><h3>請至<a href="https://calendar.google.com/calendar">google calendar</a>查看</h3>'

def handle_login_failure(error):
    return f'<h1>登記失敗!</h1><h3>{error}</h3>'

def handle_delete_account(user_id):
    user = Utiles.queryUser(user_id)
    # user = Users.query.filter_by(user_id=user_id).first()
    if user == None:
        return f'<h1>無此帳號!</h1>'
    Utiles.deleteData(user)
    return f'<h1>已刪除{user_id}!</h1>'