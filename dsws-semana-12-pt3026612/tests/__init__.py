import os
import unittest
from app import create_app, db
from app.models import User, Role  # Importa seus modelos

# Configuração de ambiente de teste
class TestConfig:
    TESTING = True
    SQLALCHEMY_DATABASE_URI = os.environ.get('TEST_DATABASE_URL') or 'sqlite:///:memory:'
    WTF_CSRF_ENABLED = False  # Desabilita CSRF para testes

# Configura o ambiente e cria o aplicativo para testes
app = create_app('testing')
app.config.from_object(TestConfig)

# Contexto de teste para executar os testes de forma isolada
@app.before_first_request
def setup():
    db.create_all()  # Cria todas as tabelas antes dos testes

@app.before_request
def before_request():
    db.session.rollback()  # Faz rollback para garantir isolamento em cada teste

@app.teardown_request
def teardown_request(exception=None):
    db.session.remove()  # Remove a sessão após cada requisição/teste

# Adiciona todas as configurações necessárias e classes de testes
class TestCase(unittest.TestCase):
    def setUp(self):
        self.app = app.test_client()  # Client para realizar requisições
        self.client = app.test_client()  # Client para o Flask
        self.db = db  # Acesso ao banco de dados
        self.ctx = app.app_context()  # Contexto da aplicação
        self.ctx.push()

    def tearDown(self):
        db.session.remove()
        db.drop_all()  # Remove todas as tabelas após os testes

        self.ctx.pop()

# Importa os testes
from . import test_views, test_models
