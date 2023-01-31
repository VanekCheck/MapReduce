from flask import Flask

from config import Config

from ClientServer.app.constants import DATABASE_URI
from ClientServer.app.models.db_config import db
from ClientServer.app.routes.auth_route import auth_route
from ClientServer.app.routes.file_route import file_route


# TODO: get file return file as formdata
# TODO: implement path functionality
# TODO: full management node functionality
# TODO: register validation
# TODO: refactor DataNode code and write a method to check if path exists


def create_app(config_class=Config):
    app = Flask(__name__)
    app.config.from_object(config_class)

    app.config['SQLALCHEMY_DATABASE_URI'] = DATABASE_URI
    db.init_app(app)

    app.register_blueprint(auth_route, name='auth_route', url_prefix='/auth')
    app.register_blueprint(file_route, name='file_route', url_prefix='/file')

    return app


if __name__ == '__main__':
    test_app = create_app()
    test_app.run(port=5020)
