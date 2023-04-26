from flask import Flask, request, redirect, url_for, session, render_template
from flask_sqlalchemy import SQLAlchemy 
from main import main
from apscheduler.schedulers.background import BackgroundScheduler
import json
from dotenv import load_dotenv
import os

from google_calendar.g_calendar import GCalendar
from flask_api import create_app, db
from flask_api.database.models import User
from flask_api.common.utiles import initDB, createTables, dropTables, insertData, updateData, queryUser, deleteData



load_dotenv()

app = create_app()
db.init_app(app)

with app.app_context():
    print('create table user')
    createTables()

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':

        '''get user id and password'''
        user_id = request.form['id']
        session['user_id'] = user_id
        user_password = request.form['password']
        session['user_password'] = user_password

        user = User.query.filter_by(user_id=user_id).first()
        # print('gCalendar', user.gCredentials)
        if user == None:
            gCredentials = ''
        else:
            gCredentials = json.loads(user.gCredentials)
        gCredentials = GCalendar(gCredentials).get_json_credentials()
        
        '''store user id and password'''
        #TODO: store only refesh token and so on
        existing_user = User.query.filter_by(user_id=user_id).first()
        if not existing_user:
            data = User(user_id=user_id, student_password=user_password, gCredentials=str(gCredentials).replace("'", '"'))
            insertData(data)

        try:
            session['gCred'] = gCredentials
            return redirect(url_for('index'))
        except:
            return 'ERROR'
    return render_template('signup.html')


@app.route('/index', methods=['GET', 'POST'])
def index():
    '''get session data'''
    user_id = session.get('user_id')
    user_password = session.get('user_password')
    gCred = session.get('gCred')

    if request.method == 'GET':
        try:
            main(user_id, user_password, gCred)
            return f'<h1>已登記成功!</h1>'
        except Exception as e:
            print(e)
            return f'<h1>登記失敗!</h1>'

@app.route('/update_HW', methods=['GET', 'POST'])
def update_HW():
    if request.method == 'GET':
        try:
            for i, j in range(1, 10):
                main(i, j)
        except:
            return '更新失敗'


if __name__ == '__main__':
    # scheduler = BackgroundScheduler()
    # scheduler.add_job(update_HW, 'cron', hour=22, minute=0)
    # scheduler.start()
    app.debug = True
    app.run()