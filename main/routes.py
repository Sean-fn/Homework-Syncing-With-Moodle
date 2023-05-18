import json

from flask import Blueprint, request, redirect, url_for, session, render_template

from flask_api.database.models import User
from flask_api.common.utiles import Utiles
from merge_data.google_calendar.g_calendar import GCalendar
from merge_data import MergeData


main_bp = Blueprint('main', __name__)
utiles = Utiles()

class Routes:
    @staticmethod
    @main_bp.route('/', methods=['GET', 'POST'])
    def index():
        if request.method == 'POST':
            '''get user id and password
            '''
            user_id = request.form['id']
            session['user_id'] = user_id
            user_password = request.form['password']
            session['user_password'] = user_password

            '''if user id and password is empty:
            store user id, password and gCredentials
            if NOT empty:
            get the google credentials from database
            '''
            user = User.query.filter_by(user_id=user_id).first()
            if user == None:
                gCredentials = ''
                #TODO: store only refesh token and so on
                data = User(user_id=user_id, student_password=user_password, gCredentials=str(gCredentials).replace("'", '"'))
                utiles.insertData(data)
            else:
                gCredentials = json.loads(user.gCredentials)
            gCredentials = GCalendar(gCredentials).get_json_credentials()
            
            session['gCred'] = gCredentials
            return redirect(url_for('main.login'))
        return render_template('signup.html')

    @staticmethod
    @main_bp.route('/login', methods=['GET','POST'])
    def login():
        user_id = session.get('user_id')
        user_password = session.get('user_password')
        gCred = session.get('gCred')

        if request.method == 'GET':
            try:
                return handle_successful_login(gCred, user_id, user_password)
            except Exception as e:
                print('ERROR', e)
                return handle_login_failure(e)

def handle_successful_login(gCred, user_id, user_password):
    merge_data = MergeData(gCred, user_id, user_password)
    merge_data.run()
    return f'<h1>已登記成功!</h1><h3>請至<a href="https://calendar.google.com/calendar">google calendar</a>查看</h3>'

def handle_login_failure(error):
    return f'<h1>登記失敗!</h1><h3>{error}</h3>'

# def get_json_credentials(gCredentials):
    gCredentials = GCalendar(gCredentials).get_json_credentials()
    return gCredentials

Routes.main_bp = main_bp