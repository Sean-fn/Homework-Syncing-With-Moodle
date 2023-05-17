from dotenv import load_dotenv
import os

from flask_api import create_app
from flask_api.common.utiles import createTables
from flask_api.database.models import db
from routes import Routes

load_dotenv()

app = create_app()
app.register_blueprint(Routes.main_bp)
db.init_app(app)

with app.app_context(): 
    createTables()
    print('TABLE USER CREATED')

if os.environ.get('FLASK_DEBUG') == 'development':
    app.debug = True

if __name__ == '__main__':
    app.run(port=8888, host='0.0.0.0')