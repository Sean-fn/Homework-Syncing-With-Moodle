from flask import Flask, request, redirect, url_for
from main import main
from apscheduler.schedulers.background import BackgroundScheduler

app = Flask(__name__)

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        user_id = request.form['id']
        user_password = request.form['password']
        try:
            main(user_id, user_password)
            return redirect(url_for('index', id=user_id))
        except:
            return '註冊失敗'
        # return f'You entered ID: {user_id} and Password: {user_password}'
    with open('signup.html', 'r') as f:
        return f.read()
    


#@app.route('/index', methods=['POST'])
@app.route('/welcome/<id>', methods=['GET', 'POST'])
def index(id):
    # if request.method == 'POST':
    #     google = request.form['id']
    #     return redirect(url_for('index', id=google))
    if request.method == 'GET':
        return f'<h1>{id}已登記成功!</h1>'
        with open('signup-1.html', 'r') as f:
            return f.read()
        

@app.route('/update_HW', methods=['GET', 'POST'])
def update_HW():
    if request.method == 'GET':
        try:
            for i, j in range(1, 10):
                main(i, j)
        except:
            return '更新失敗'

if __name__ == '__main__':
    scheduler = BackgroundScheduler()
    scheduler.add_job(update_HW, 'cron', hour=22, minute=0)
    scheduler.start()
    app.run()