from flask import Flask, request, redirect, url_for, session, render_template
from flask_sqlalchemy import SQLAlchemy 
from main import main
from apscheduler.schedulers.background import BackgroundScheduler
import json
from dotenv import load_dotenv
import os

load_dotenv()

app = Flask(__name__, template_folder='./frontend/templates',static_folder='./frontend/static')
app.secret_key = os.getenv('FLASK_SECRET_KEY')

db = SQLAlchemy()
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///user_info.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db.init_app(app)


'''create table user'''
class User(db.Model):
    user_id = db.Column(db.Integer, primary_key=True, unique=True, nullable=False)
    student_password = db.Column(db.String(120), nullable=False)
    gCredentials = db.Column(db.String(120), nullable=False)

    def storeData(data):
        db.session.add(data)
        db.session.commit()

with app.app_context():
    db.create_all()


@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        '''get user id and password'''
        user_id = request.form['id']
        session['user_id'] = user_id
        user_password = request.form['password']
        session['user_password'] = user_password
        gCred = GCalendar('').get_credentials()

        # if user_id == '' or user_password == '':
        #     print(db.session.query(User).all())
        #     print(db.select(User).all())
        #     return 'ERROR'
        
        '''store user id and password'''
        existing_user = User.query.filter_by(user_id=user_id).first()
        if not existing_user:
            data = User(user_id=user_id, student_password=user_password, gCredentials=gCred)
            User.storeData(data)

        '''go to index'''
        try:
            user = User.query.filter_by(user_id=user_id).first()
            session['gCred'] = user.gCredentials
            return redirect(url_for('index'))
        except:
            return 'ERROR'
    return render_template('signup.html')


@app.route('/index', methods=['GET', 'POST'])
def index():
    user_id = session.get('user_id')
    user_password = session.get('user_password')
    gCred = session.get('gCred')
    if gCred == None:
        gCred = ''
    if request.method == 'GET':
        try:
            main(user_id, user_password, gCred)
            print('登記成功')
            return f'<h1>已登記成功!</h1>'
        except Exception as e:
            print(e)
            return '登記失敗'

# @app.route('/update_HW', methods=['GET', 'POST'])
# def update_HW():
#     if request.method == 'GET':
#         try:
#             for i, j in range(1, 10):
#                 main(i, j)
#         except:
#             return '更新失敗'


if __name__ == '__main__':
    # scheduler = BackgroundScheduler()
    # scheduler.add_job(update_HW, 'cron', hour=22, minute=0)
    # scheduler.start()
    app.debug = True
    app.run()