import logging
import os
from flask import Flask, Blueprint
from flask_migrate import upgrade as _upgrade
from flask_cors import CORS

from deepstroy_model_service.basic_model_binding.messages_traffic_controller import MessagesTrafficController
from deepstroy_model_service.domain.data_access_layer.build_connection_string import build_connection_string
from deepstroy_model_service.domain.data_access_layer.db import db, migrate
from deepstroy_model_service.modules.predicts.predicts_routes import predict_blueprint


def create_app():
    """Application factory, used to create application"""
    app = Flask(__name__)
    app.config.from_object('deepstroy_model_service.config.flask_config')

    app.url_map.strict_slashes = False

    CORS(
        app,
    )

    app.config['SQLALCHEMY_DATABASE_URI'] = build_connection_string()
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

    register_blueprints(app)
    db.init_app(app)
    migrate.init_app(app, db)

    with app.app_context():
        _upgrade()

    os.system(f"unzip -j -qq model.pkl.zip/\*.zip -d model.pkl.zip")
    consuming_thread = MessagesTrafficController()
    consuming_thread.daemon = True
    consuming_thread.start()
    logging.warning("Start listening to the queue.")

    return app


def register_blueprints(app):
    """Register all blueprints for application"""
    results_service_blueprint = Blueprint('model-service', __name__, url_prefix='/model-service')
    results_service_blueprint.register_blueprint(predict_blueprint)

    app.register_blueprint(results_service_blueprint)
