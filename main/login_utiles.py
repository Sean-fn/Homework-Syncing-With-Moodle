from merge_data import MergeData

def handle_successful_login(gCred, user_id, user_password):
    merge_data = MergeData(gCred, user_id, user_password)
    merge_data.run()
    return f'<h1>已登記成功!</h1><h3>請至<a href="https://calendar.google.com/calendar">google calendar</a>查看</h3>'

def handle_login_failure(error):
    return f'<h1>登記失敗!</h1><h3>{error}</h3>'