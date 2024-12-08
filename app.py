from flask import Flask
from flasgger import Swagger
from flask_cors import CORS
from routes.api.notes import notes_bp



def create_app():
    app = Flask(__name__)

    app.config['SWAGGER'] = {
        'title': 'Notes API',
        'uiversion': 3
    }

    CORS(app)

    app.register_blueprint(notes_bp)
    Swagger(app)

    return app


app = create_app()

if __name__ == '__main__':
    app.run(debug=True)

