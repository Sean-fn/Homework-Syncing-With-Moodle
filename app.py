from dotenv import load_dotenv
import os

from flask_api import create_app
from main.routes import Routes

load_dotenv()

app = create_app()
app.register_blueprint(Routes.main_bp)

if os.environ.get('FLASK_DEBUG') in ['development', 'True']:
    app.debug = True

if __name__ == '__main__':
    app.run(port=8080, host='0.0.0.0')