
from flask import Flask
from config import Config
from ManagementServer.constants import DATABASE_URI
from ManagementServer.models.db_config import db
from ManagementServer.routes.data_node_route import data_node_route


def create_app(config_class=Config):
    app = Flask(__name__)
    app.config.from_object(config_class)

    app.config['SQLALCHEMY_DATABASE_URI'] = DATABASE_URI
    db.init_app(app)

    app.register_blueprint(data_node_route, name='file_route', url_prefix='/data-node')

    return app


if __name__ == '__main__':
    management_app = create_app()
    management_app.run(port=5030, debug=True)

# python app.py --port 5001
