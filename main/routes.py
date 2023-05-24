import json

from flask import Blueprint, request, render_template

from flask_api.common.utiles import Utiles
from main.login_utiles import handle_successful_login, handle_login_failure, handle_delete_account
from main.dbUtiles import storeGCredentials


main_bp = Blueprint('main', __name__)
utiles = Utiles()

class Routes:
    @staticmethod
    @main_bp.route('/', methods=['GET', 'POST'])
    def index():
        if request.method == 'POST':
            '''get user informations
            '''
            user_id = request.form['id']
            user_password = request.form['password']
            gCredentials = storeGCredentials(user_id, user_password)

            try:
                return handle_successful_login(gCredentials, user_id, user_password)
            except Exception as e:
                print('ERROR', e)
                return handle_login_failure(e)
        
        return render_template('signup.html')
    
    #TODO: pops up error if the account not found
    @main_bp.route('/delete-account', methods=['GET','POST'])
    def delete_account():
        if request.method == 'POST':
            user_id = request.form['id']
            return handle_delete_account(user_id)
        return render_template('delete.html')

Routes.main_bp = main_bp