from flask import Flask
from flask_bootstrap import Bootstrap
from flask_moment import Moment
from flask_sqlalchemy import SQLAlchemy
from config import config
from flask_login import LoginManager

# Instâncias das extensões do Flask
bootstrap = Bootstrap()
moment = Moment()
db = SQLAlchemy()
login_manager = LoginManager()
login_manager.login_view = 'auth.login'

def create_app(config_name='default'):
    """
    Função factory para criar a aplicação Flask.

    :param config_name: Nome da configuração (development, testing, production)
    :return: Instância do aplicativo Flask configurada.
    """
    if config_name not in config:
        raise RuntimeError("Ambiente inválido! Use: development, testing ou production.")
    # Cria a instância principal do Flask
    app = Flask(__name__)
    # Carrega as configurações específicas para o ambiente
    app.config.from_object(config[config_name])
    config[config_name].init_app(app)

    # Inicializa as extensões do Flask
    bootstrap.init_app(app)
    moment.init_app(app)
    db.init_app(app)
    login_manager.init_app(app)

    # Registra o blueprint da seção principal
    from .main import main as main_blueprint
    app.register_blueprint(main_blueprint)

    from .auth import auth as auth_blueprint
    app.register_blueprint(auth_blueprint, url_prefix='/auth')

    return app