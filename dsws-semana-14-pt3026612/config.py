import os
import logging
from logging.handlers import RotatingFileHandler

# Diretório base do projeto
basedir = os.path.abspath(os.path.dirname(__file__))

class Config:
    """
    Configurações gerais para a aplicação Flask.
    Variáveis de ambiente são usadas para dados sensíveis e valores padrão são definidos.
    """
    SECRET_KEY = os.getenv('SECRET_KEY') or 'uma-chave-secreta' # chave secreta
    SQLALCHEMY_TRACK_MODIFICATIONS = False # Desativa as notificações do SQLAlchemy para economizar recursos
    MAILGUN_API_KEY = os.getenv('MAILGUN_API_KEY') # API key para integração com Mailgun
    MAILGUN_API_URL = os.getenv('MAILGUN_API_URL') # URL da API do Mailgun
    MAILGUN_DOMAIN = os.getenv('MAILGUN_DOMAIN') # Domínio associado à conta Mailgun
    FLASKY_MAIL_SUBJECT_PREFIX = '[Flasky]' # Prefixo de e-mails enviados
    FLASKY_ADMIN = os.getenv('FLASKY_ADMIN') # Endereço de e-mail do administrador
    ENV = os.getenv('FLASK_CONFIG', 'development') # Ambiente (development, production, testing)
    print(MAILGUN_API_KEY)
    print(MAILGUN_API_URL)
    print(MAILGUN_DOMAIN)

    @staticmethod
    def init_app(app):
        """
        Método para inicializar configurações específicas.
        Adiciona configurações de logging básico.
        """
        if app.config['ENV'] not in ['development', 'testing', 'production']:
            raise RuntimeError("Ambiente não suportado! Use: development, testing ou production.")

        # Configuração básica de logging
        logging.basicConfig(level=logging.INFO)
        logger = logging.getLogger(__name__)
        logger.info(f'Configurando o ambiente: {app.config["ENV"]}')

        # Verifica se as variáveis de ambiente essenciais estão configuradas
        required_env_vars = ['MAILGUN_API_KEY', 'MAILGUN_API_URL', 'MAILGUN_DOMAIN']
        for var in required_env_vars:
            value = os.getenv(var)
            if not value:
                logger.warning(f'⚠️ A variável de ambiente {var} não está configurada.')
            else:
                print(f'{var}: {value}')

# Configuração para desenvolvimento
class DevelopmentConfig(Config):
    """
    Configuração para ambiente de desenvolvimento.
    Ativa o modo DEBUG e utiliza o banco SQLite local.
    """
    DEBUG = True
    SQLALCHEMY_DATABASE_URI = os.environ.get('DEV_DATABASE_URL') or \
        'sqlite:///' + os.path.join(basedir, 'data-dev.sqlite')

    @staticmethod
    def init_app(app):
        Config.init_app(app)
        logging.basicConfig(level=logging.DEBUG)  # Logs detalhados em desenvolvimento
        app.logger.debug("Configuração de desenvolvimento aplicada.")

# Configuração para testes
class TestingConfig(Config):
    """
    Configuração para ambiente de teste.
    Ativa o modo TESTING e utiliza o banco SQLite in-memory.
    """
    TESTING = True
    SQLALCHEMY_DATABASE_URI = os.environ.get('TEST_DATABASE_URL') or 'sqlite://'  # Banco de memória
    WTF_CSRF_ENABLED = False  # Desabilita CSRF para testes

# Configuração para produção
class ProductionConfig(Config):
    """
    Configuração para ambiente de produção.
    Define URI para o banco de dados e adiciona configuração de logging.
    """
    SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL') or \
        'sqlite:///' + os.path.join(basedir, 'data.sqlite')

    @staticmethod
    def init_app(app):
        """
        Inicializa configurações específicas de produção.
        Adicionar logging para arquivo.
        """
        Config.init_app(app)  # Chama a configuração básica

        # Validação de SECRET_KEY em produção
        if app.config['SECRET_KEY'] == 'uma-chave-secreta':
            raise RuntimeError("A SECRET_KEY não está configurada! Isso pode comprometer a segurança.")

        # Verifica variáveis essenciais de ambiente
        required_env_vars = ['MAILGUN_API_KEY', 'MAILGUN_API_URL', 'MAILGUN_DOMAIN']
        for var in required_env_vars:
            if not os.getenv(var):
                raise RuntimeError(f"A variável de ambiente {var} não está configurada e é essencial em produção!")

        # Configuração de logging para produção
        file_handler = RotatingFileHandler('flasky.log', maxBytes=100000, backupCount=10)  # Rotação de logs
        file_handler.setLevel(logging.WARNING)
        formatter = logging.Formatter('%(asctime)s - %(levelname)s - %(message)s')
        file_handler.setFormatter(formatter)
        app.logger.addHandler(file_handler)

        app.logger.info('Configurações de produção aplicadas com sucesso.')

# Dicionário para mapeamento das configurações por ambiente
config = {
    'development': DevelopmentConfig,
    'testing': TestingConfig,
    'production': ProductionConfig,
    'default': DevelopmentConfig
}
