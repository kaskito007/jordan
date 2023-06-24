import os
from flask import Flask
from flask_migrate import Migrate
from src.api.housekeepers import bp as housekeepers_bp
from src.api.tasks import bp as tasks_bp


# https://flask.palletsprojects.com/en/2.0.x/patterns/appfactories/


def create_app(test_config=None):
    app = Flask(__name__, instance_relative_config=True)
    app.config.from_mapping(
        SECRET_KEY='dev',
        SQLALCHEMY_DATABASE_URI='postgresql://postgres@localhost:5432/hotel',
        SQLALCHEMY_TRACK_MODIFICATIONS=False,
        SQLALCHEMY_ECHO=True
    )

    if test_config is None:
        # load the instance config, if it exists, when not testing
        app.config.from_pyfile('config.py', silent=True)
    else:
        # load the test config if passed in
        app.config.from_mapping(test_config)

    # ensure the instance folder exists
    try:
        os.makedirs(app.instance_path)
    except OSError:
        pass

    from src.models import db
    db.init_app(app)
    migrate = Migrate(app, db)

    from src.models import Housekeeper,Task
    app.register_blueprint(housekeepers_bp)
    app.register_blueprint(tasks_bp)

    @app.route('/')
    def hello_world():
        return 'Hello, World - Docker in VS Code!'

    return app
if __name__ == '__main__':
    app = create_app()
    app.run(debug=True, host='0.0.0.0')