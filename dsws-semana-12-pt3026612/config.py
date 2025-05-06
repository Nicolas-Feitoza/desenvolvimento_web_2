import os
import logging

basedir = os.path.abspath(os.path.dirname(__file__))

class Config:
    SECRET_KEY = os.getenv('SECRET_KEY') or 'uma-chave-secreta'
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    MAILGUN_API_KEY = os.getenv('MAILGUN_API_KEY')
    MAILGUN_API_URL = os.getenv('MAILGUN_API_URL')
    MAILGUN_DOMAIN = os.getenv('MAILGUN_DOMAIN')
    FLASKY_MAIL_SUBJECT_PREFIX = '[Flasky]'
    FLASKY_ADMIN = os.getenv('FLASKY_ADMIN')
    ENV = os.getenv('ENV')

    @staticmethod
    def init_app(app):
        logging.basicConfig(level=logging.INFO)
        logger = logging.getLogger(__name__)
        logger.info(f'Configurando o ambiente: {app.config["ENV"]}')
        required_env_vars = ['MAILGUN_API_KEY', 'MAILGUN_API_URL', 'MAILGUN_DOMAIN']
        for var in required_env_vars:
            if not os.getenv(var):
                logger.warning(f'⚠️ A variável de ambiente {var} não está configurada.')

class DevelopmentConfig(Config):
    DEBUG = True
    SQLALCHEMY_DATABASE_URI = os.environ.get('DEV_DATABASE_URL') or \
        'sqlite:///' + os.path.join(basedir, 'data-dev.sqlite')


class TestingConfig(Config):
    TESTING = True
    SQLALCHEMY_DATABASE_URI = os.environ.get('TEST_DATABASE_URL') or \
        'sqlite://'  # SQLite in-memory for tests


class ProductionConfig(Config):
    SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL') or \
        'sqlite:///' + os.path.join(basedir, 'data.sqlite')

    @staticmethod
    def init_app(app):
        Config.init_app(app)  # Chamando o método de logging do Config
        file_handler = logging.FileHandler('flasky.log')
        file_handler.setLevel(logging.WARNING)
        formatter = logging.Formatter('%(asctime)s - %(levelname)s - %(message)s')
        file_handler.setFormatter(formatter)
        app.logger.addHandler(file_handler)

config = {
    'development': DevelopmentConfig,
    'testing': TestingConfig,
    'production': ProductionConfig,
    'default': DevelopmentConfig
}
