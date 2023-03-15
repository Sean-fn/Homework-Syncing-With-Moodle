from flask import Flask, request, redirect, url_for

app = Flask(__name__)

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        user_id = request.form['id']
        user_password = request.form['password']
        return redirect(url_for('index', id=user_id))
        return f'You entered ID: {user_id} and Password: {user_password}'
    with open('signup.html', 'r') as f:
        return f.read()
    

#@app.route('/index', methods=['POST'])
@app.route('/welcome/<id>', methods=['GET', 'POST'])
def index(id):
    if request.method == 'POST':
        google = request.form['id']
        return redirect(url_for('index', id=google))
    if request.method == 'GET':
        return f'<h1>Welcome, {id}!</h1>'
        with open('signup-1.html', 'r') as f:
            return f.read()

if __name__ == '__main__':
    app.run(debug=True)