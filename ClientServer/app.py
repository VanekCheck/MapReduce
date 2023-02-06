from flask import Flask

from config import Config

from ClientServer.constants import DATABASE_URI
from ClientServer.models.db_config import db
from ClientServer.routes.auth_route import auth_route
from ClientServer.routes.file_route import file_route
from ClientServer.routes.management_route import data_node_route


# TODO: get file return file as formdata
# TODO: connect management node
# TODO: register validation

def create_app(config_class=Config):
    app = Flask(__name__)
    app.config.from_object(config_class)

    app.config['SQLALCHEMY_DATABASE_URI'] = DATABASE_URI
    db.init_app(app)

    app.register_blueprint(auth_route, name='auth_route', url_prefix='/auth')
    app.register_blueprint(file_route, name='file_route', url_prefix='/file')
    app.register_blueprint(data_node_route, name='data_node_route', url_prefix='/data-node')

    return app


if __name__ == '__main__':
    test_app = create_app()
    test_app.run(port=5020, debug=True)
