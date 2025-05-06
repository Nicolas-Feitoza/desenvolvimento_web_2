from flask import Flask
from flask_bootstrap import Bootstrap
from flask_moment import Moment
from flask_sqlalchemy import SQLAlchemy
from config import config

# Instâncias das extensões do Flask
bootstrap = Bootstrap()
moment = Moment()
db = SQLAlchemy()

def create_app(config_name):
    """
    Função factory para criar a aplicação Flask.

    :param config_name: Nome da configuração (development, testing, production)
    :return: Instância do aplicativo Flask configurada.
    """
    app = Flask(__name__)  # Cria a instância principal do Flask
    app.config.from_object(config[config_name])  # Carrega as configurações específicas para o ambiente
    config[config_name].init_app(app)  # Inicializa as configurações específicas

    # Inicializa as extensões do Flask
    bootstrap.init_app(app)
    moment.init_app(app)
    db.init_app(app)

    # Registra o blueprint da seção principal
    from .main import main as main_blueprint
    app.register_blueprint(main_blueprint)

    return app
