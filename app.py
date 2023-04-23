from flask import Flask, request, redirect, url_for, session, render_template
from main import main
from apscheduler.schedulers.background import BackgroundScheduler
from dotenv import load_dotenv
import os

load_dotenv()

app = Flask(__name__, template_folder='./frontend/templates',static_folder='./frontend/static')
app.secret_key = os.getenv('FLASK_SECRET_KEY')



@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        user_id = request.form['id']
        session['user_id'] = user_id
        user_password = request.form['password']
        session['user_password'] = user_password
        # agree = request.form.get('remember-me')
        # if agree:
        #     return 'ok'
        try:
            return redirect(url_for('index'))
        except:
            return 'ERROR'
    return render_template('signup.html')
    


@app.route('/index', methods=['GET', 'POST'])
def index():
    user_id = session.get('user_id')
    user_password = session.get('user_password')
    if request.method == 'GET':
        try:
            main(user_id, user_password)
            return f'<h1>已登記成功!</h1>'
        except:
            return redirect(url_for('login'))

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