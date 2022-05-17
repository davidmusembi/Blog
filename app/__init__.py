from flask import Flask
from config import config_options
from flask_sqlalchemy import SQLAlchemy
from flask_bootstrap import Bootstrap
from flask_login import LoginManager
from flask_uploads import UploadSet, configure_uploads, IMAGES

bootstrap = Bootstrap()
db = SQLAlchemy()
login_manager = LoginManager()
login_manager.session_protection = 'strong'
login_manager.login_view = 'auth.login'
photos = UploadSet('photos', IMAGES)


def create_app(config_name):
    app = Flask(__name__)

    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    app.config.from_object(config_options.get(config_name))

    # Initializing Flask Extensions
    bootstrap.init_app(app)
    db.init_app(app)
    login_manager.init_app(app)

    # configure UploadSet
    configure_uploads(app, photos)

    from app.main import main
    # from app.auth import auth
    # app.register_blueprint(auth)
    from app.auth import auth as auth_blueprint
    app.register_blueprint(main)
    app.add_url_rule('/', endpoint='main.index')
    app.register_blueprint(auth_blueprint, url_prefix='/authenticate')

    return app
